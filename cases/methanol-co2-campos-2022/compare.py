#!/usr/bin/env python3
"""Compare the chepta 0.6.2 runs of the one-step methanol plant with the paper, stream by stream and duty by duty.

Reads results-chepta-0.6.2/*.output.json and the run manifest; writes results-chepta-0.6.2/comparison.json and
COMPARISON.md (generated; do not edit by hand). Published values: streams.json (Tables S9-S10) and equipment.json
(Table S14). Derived values (duties from the printed stream enthalpies) are computed here and labelled so.
  python3 cases/methanol-co2-campos-2022/compare.py
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
OUT = H / "results-chepta-0.6.2"
PAPER = {s["stream"]: s for s in json.loads((H / "streams.json").read_text())["streams"]}
EQUIP = {e["id"]: e for e in json.loads((H / "equipment.json").read_text())["equipment"]}
COMP = {"carbon-dioxide": "CO2", "hydrogen": "H2", "carbon-monoxide": "CO", "methanol": "CH3OH", "water": "H2O", "nitrogen": "N2"}
ORDER = ["H2", "CO", "CO2", "CH3OH", "H2O", "N2"]

# unit runs: CHEPTA stream id -> paper stream id
UNIT_MAP = {
    "u-mixer1": {"out-out": "2"}, "u-cp1": {"out-out": "3"}, "u-he1": {"out-out": "4"},
    "u-flash1": {"out-vapour": "5", "out-liquid": "40"}, "u-cp2": {"out-out": "6"},
    "u-he2": {"out-hot": "7", "out-cold": "36-REC"}, "u-flash2": {"out-vapour": "8", "out-liquid": "42"},
    "u-cp3": {"out-out": "9"}, "u-he3": {"out-out": "10"}, "u-cph2": {"out-out": "12"}, "u-mixer2": {"out-out": "13"},
    "u-he4": {"out-hot": "20", "out-cold": "14"},
    "u-reactor-U300": {"out-out": "16"}, "u-reactor-U150": {"out-out": "16"}, "u-reactor-U1000": {"out-out": "16"},
    "u-reactor-isothermal": {"out-out": "16"},
    "u-he5": {"out-hot": "21", "out-cold": "29"}, "u-he5-cold82.9": {"out-hot": "21", "out-cold": "29"},
    "u-he5-dTmin2": {"out-hot": "21", "out-cold": "29"}, "u-he5-dTmin2-zones10": {"out-hot": "21", "out-cold": "29"},
    "u-he6": {"out-hot": "22", "out-cold": "27"},
    "u-he7": {"out-out": "23"}, "u-he7-duty24.2MW": {"out-out": "23"}, "u-he7-duty19.75MW": {"out-out": "23"},
    "u-flash3": {"out-vapour": "33", "out-liquid": "24"}, "u-cprec": {"out-out": "35"},
    "u-valve1": {"out-out": "25"}, "u-valve3": {"out-out": "41"}, "u-valve2": {"out-out": "43"},
    "u-mixer4": {"out-out": "26"}, "u-flash4": {"out-vapour": "37", "out-liquid": "28"}, "u-mixer5": {"out-out": "39-REC"},
}
# paper block -> (CHEPTA block id, inlet streams, outlet streams) for duties from the printed enthalpies
DUTY_STREAMS = {
    "CP1": (["2"], ["3"]), "HE1": (["3"], ["4"]), "CP2": (["5"], ["6"]), "HE2": (["6"], ["7"]), "CP3": (["8"], ["9"]),
    "HE3": (["9"], ["10"]), "CPH2": (["11-H2"], ["12"]), "HE4": (["13"], ["14"]), "HE5": (["20"], ["21"]),
    "HE6": (["21"], ["22"]), "HE7": (["22"], ["23"]), "CPREC": (["34"], ["35"]), "REACTOR1": (["54W"], ["55W"]),
}
TABLE_S14 = {"HE1": 13.6, "HE2": 11.1, "HE3": 5.6, "HE4": 105.5, "HE5": 103.3, "HE6": 5.0, "HE7": 24.2}


def paper_duty_MW(block):
    ins, outs = DUTY_STREAMS[block]
    h = lambda ids: sum(PAPER[i]["molar_kmol_h"] * PAPER[i]["H_MJ_kmol"] for i in ids) / 3600
    d = h(outs) - h(ins)
    return -d if block == "REACTOR1" else d  # the reactor: the heat taken by its coolant, as a negative duty


def mol_pct(s):
    F = s["F_kmol_h"] or 1
    return {COMP[c]: 100 * v / F for c, v in s["flow_kmol_h"].items() if c in COMP}


def cmp_stream(sid, s):
    p = PAPER[sid]
    m = mol_pct(s)
    row = {"stream": sid, "chepta": {"F_kmol_h": s["F_kmol_h"], "T_C": s["T_K"] - 273.15, "P_bar": s["P_kPa"] / 100, "VF": s.get("VF"),
                                    "mol_pct": {k: m.get(k, 0.0) for k in ORDER}},
           "paper": {"F_kmol_h": p["molar_kmol_h"], "T_C": p["T_C"], "P_bar": p["P_bar"], "mol_pct": {k: p["mol_pct"][k] for k in ORDER},
                     "locator": p["locator"]}}
    row["diff"] = {"F_pct": 100 * (s["F_kmol_h"] - p["molar_kmol_h"]) / p["molar_kmol_h"] if p["molar_kmol_h"] else None,
                   "T_K": s["T_K"] - 273.15 - p["T_C"],
                   "mol_pct_points": {k: m.get(k, 0.0) - p["mol_pct"][k] for k in ORDER}}
    return row


def block_duties(v):
    out = {}
    for bid, b in (v.get("blocks") or {}).items():
        t = b.get("type")
        st = b.get("state") or {}
        if t == "hx":
            out[bid] = {"kind": "exchanged", "MW": st.get("duty_kW", 0) / 1000}
        elif t in ("heater", "compressor", "pfr", "flash"):
            out[bid] = {"kind": "duty" if t != "compressor" else "power", "MW": (b.get("duty_kW") or 0) / 1000}
        elif t == "column":
            out[bid] = {"kind": "column", "condenser_MW": -st.get("condenser_kW", 0) / 1000, "reboiler_MW": st.get("reboiler_kW", 0) / 1000,
                        "iterations": st.get("iterations")}
    return out


def main():
    man = json.loads((OUT / "run-manifest.json").read_text())
    res = {"source": "Lacerda de Oliveira Campos et al. 2022 (Processes 10, 1535), one-step process; published = Aspen Plus V10 simulation",
           "engine": man["engine"], "runs": []}
    for r in man["runs"]:
        f = OUT / f"{r['id']}.output.json"
        d = json.loads(f.read_text()) if f.exists() and f.read_text().strip() else {}
        v = d.get("value") or {}
        rec = {"id": r["id"], "chepta_run_id": r.get("chepta_run_id"), "outcome": r.get("outcome"), "exit_code": r.get("exit_code"),
               "error_code": r.get("error_code"), "error_message": r.get("error_message")}
        if d.get("outcome") == "ok" and "streams" in v:
            m = UNIT_MAP.get(r["id"].split("-r")[0] if r["id"] not in UNIT_MAP else r["id"])
            pairs = m.items() if m else [(k, k) for k in v["streams"] if k in PAPER]
            rec["streams"] = [cmp_stream(p, v["streams"][c]) for c, p in pairs if c in v["streams"]]
            rec["duties"] = block_duties(v)
            rec["extrapolations"] = [{"message": e.get("short"), "at_K": e.get("at"), "range": e.get("range"), "where": e.get("where")}
                                     for e in v.get("extrapolations") or []]
            rec["loops"] = v.get("loops")
            rec["balance"] = v.get("balance")
        res["runs"].append(rec)
    res["paper_duties_MW"] = {"table_S14": TABLE_S14, "from_printed_stream_enthalpies": {k: round(paper_duty_MW(k), 3) for k in DUTY_STREAMS}}
    (OUT / "comparison.json").write_text(json.dumps(res, indent=1) + "\n")
    write_md(res)


def f(x, n=1):
    return "" if x is None else f"{x:.{n}f}"


def write_md(res):
    L = ["# Comparison with the paper (generated by compare.py; do not edit)", "",
         "Published: Tables S9-S10 and S14 of the supplement (an Aspen Plus V10 simulation, not measurements). Simulated: chepta 0.6.2, run ids in each section. "
         "Derived: duties from the printed stream enthalpies. Differences are CHEPTA minus paper.", ""]
    for r in res["runs"]:
        L.append(f"## {r['id']} ({r['outcome']}{', ' + r['error_code'] if r.get('error_code') else ''}; CHEPTA run {r.get('chepta_run_id')})")
        L.append("")
        if r.get("error_message"):
            L += [f"> {r['error_message']}", ""]
        if r.get("streams"):
            L += ["| Stream | F CHEPTA / paper kmol/h | dF % | T CHEPTA / paper C | dT K | VF | mol % H2, CO, CO2, CH3OH, H2O, N2 (CHEPTA) | (paper) |",
                  "|---|---|---:|---|---:|---:|---|---|"]
            for s in r["streams"]:
                c, p, d = s["chepta"], s["paper"], s["diff"]
                L.append(f"| {s['stream']} | {f(c['F_kmol_h'])} / {f(p['F_kmol_h'])} | {f(d['F_pct'], 2)} | {f(c['T_C'], 2)} / {f(p['T_C'], 2)} | {f(d['T_K'], 2)} | {f(c['VF'], 4)} | "
                         + ", ".join(f(c["mol_pct"][k], 3) for k in ORDER) + " | " + ", ".join(f(p["mol_pct"][k], 3) for k in ORDER) + " |")
            L.append("")
        if r.get("duties"):
            L.append("Duties (MW): " + "; ".join(
                f"{k} {v['kind']} {f(v['MW'], 2)}" if "MW" in v else f"{k} condenser {f(v['condenser_MW'], 2)}, reboiler {f(v['reboiler_MW'], 2)} ({v['iterations']} Newton iterations)"
                for k, v in r["duties"].items()))
            L.append("")
        if r.get("extrapolations"):
            L.append("Extrapolations reported by CHEPTA (value.extrapolations; where = the blocks whose numbers rest on them):")
            L.append("")
            for e in r["extrapolations"]:
                L.append(f"- {e['message']} (at {f(e['at_K'], 2)} K; where: {', '.join(e['where'] or [])})")
            L.append("")
        if r.get("loops"):
            L.append("Loops: " + "; ".join(f"{', '.join(l.get('tears', []))}: {l.get('iterations')} iterations" for l in r["loops"]))
            L.append("")
    pd = res["paper_duties_MW"]
    L += ["## Paper duties", "", "| Block | Table S14 MW | From the printed stream enthalpies MW (derived) |", "|---|---:|---:|"]
    for k, v in pd["from_printed_stream_enthalpies"].items():
        L.append(f"| {k} | {pd['table_S14'].get(k, '')} | {v} |")
    (H / "COMPARISON.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
