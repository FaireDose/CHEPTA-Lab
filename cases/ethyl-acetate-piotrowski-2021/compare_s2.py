#!/usr/bin/env python3
"""Compare CHEPTA 0.6.1 runs of plant S2 with the paper (Table A2 streams, Table 1 duties), stream by stream.

Reads results-chepta-0.6.1/*.output.json and run-manifest.json; writes results-chepta-0.6.1/comparison-s2.json and
prints the tables used in the README. No CHEPTA call. Mass fractions of CHEPTA streams are calculated from CHEPTA's
component flows (kmol/h) and CHEPTA's own molar masses (run info-components). Differences are CHEPTA minus paper.
The paper's values are a published simulation (Chemcad 7), not measurements: agreement means two models agree.
  python3 cases/ethyl-acetate-piotrowski-2021/compare_s2.py
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = H / "results-chepta-0.6.1"
PAPER = {int(r["stream"]): r for r in json.loads((H / "streams.json").read_text())["strategies"]["S2"]}
EQUIP = {e["id"]: e["S2"] for e in json.loads((H / "equipment.json").read_text())["equipment"]}
IDS = ["ethanol", "water", "ethyl-acetate", "acetic-acid"]
KEYS = ["ethanol", "water", "ethyl_acetate", "acetic_acid"]

# Heaters and coolers of Table 1, and the duties of the reactor and the columns (Table 1, p.11)
DUTIES = {"HTXR2": ("HTXR 2", EQUIP[2]["duty_kW"]), "HTXR6": ("HTXR 6", EQUIP[6]["duty_kW"]),
          "HTXR10": ("HTXR 10", EQUIP[10]["duty_kW"]), "HTXR12": ("HTXR 12", EQUIP[12]["duty_kW"]),
          "HTXR17": ("HTXR 17", EQUIP[17]["duty_kW"]), "HTXR18": ("HTXR 18", EQUIP[18]["duty_kW"]),
          "HTXR19": ("HTXR 19", EQUIP[19]["duty_kW"]), "KREA4": ("KREA 4", EQUIP[4]["duty_kW"])}
COLUMNS = {"SCDS11": EQUIP[11]["condenser_reboiler_duty_kW"], "SCDS15": EQUIP[15]["condenser_reboiler_duty_kW"]}
LIMITS = {"product_EA_mass_pct_min": (99.9, "Section 3.4, p.8: 'required purity greater than 99.9 %'; 'required EA content in the product (99.9 wt%)'"),
          "product_water_mass_pct_max": (0.03, "Section 3.4, p.8: 'water content, which should be less than 0.03 wt%'"),
          "product_ethanol_mass_pct_max": (0.04, "Section 3.4, p.8: 'ethanol content that should be less than 0.04 wt%'"),
          "azeotrope_acetic_acid_mass_pct_max": (0.005, "Section 3.2, p.6: 'should not contain more than 0.005 wt%' (distillate of SCDS 5)"),
          "wastewater_organics_mass_pct_max": (0.01, "Section 3.5, p.10: 'bottom product must contain less than 0.01% of its weight in organic compounds'")}


def mw():
    out = {}
    for c in IDS:
        d = json.loads((R / f"info-{c}.output.json").read_text())
        out[c] = d["value"]["MW"]
    return out


def stream_view(s, MW):
    m = {c: s["flow_kmol_h"].get(c, 0.0) * MW[c] for c in IDS}
    tot = sum(m.values())
    return {"T_C": s["T_K"] - 273.15, "VF": s.get("VF"), "kmol_h": s["F_kmol_h"], "kg_h": tot,
            "mass_pct": {c: 100 * v / tot if tot else 0.0 for c, v in m.items()},
            "phases": [p["type"] for p in s.get("phases", [])]}


def paper_view(n):
    p = PAPER[n]
    return {"T_C": p["T_C"], "kmol_h": p["molar_kmol_h"], "kg_h": p["mass_kg_h"],
            "mass_pct": {c: p[k + "_mass_pct"] for c, k in zip(IDS, KEYS)}}


def compare_streams(res, MW):
    rows = []
    for sid, s in res["value"]["streams"].items():
        n = int(sid[1:])
        c, p = stream_view(s, MW), paper_view(n)
        rows.append({"stream": n, "chepta": c, "paper": p,
                     "dT_K": c["T_C"] - p["T_C"], "dkg_h": c["kg_h"] - p["kg_h"],
                     "rel_kg_h": (c["kg_h"] - p["kg_h"]) / p["kg_h"],
                     "dmass_pct_points": {k: c["mass_pct"][k] - p["mass_pct"][k] for k in IDS}})
    return sorted(rows, key=lambda r: r["stream"])


def compare_duties(res):
    rows = []
    for bid, b in res["value"]["blocks"].items():
        if bid in DUTIES:
            name, paper = DUTIES[bid]
            rows.append({"block": name, "chepta_kW": b["duty_kW"], "paper_kW": paper,
                         "rel": (b["duty_kW"] - paper) / paper if paper else None})
        if bid in COLUMNS:
            st = b["state"]
            pc, pr = COLUMNS[bid]
            rows.append({"block": f"{bid[:4]} {bid[4:]} condenser", "chepta_kW": -st["condenser_kW"], "paper_kW": pc,
                         "rel": (-st["condenser_kW"] - pc) / pc})
            rows.append({"block": f"{bid[:4]} {bid[4:]} reboiler", "chepta_kW": st["reboiler_kW"], "paper_kW": pr,
                         "rel": (st["reboiler_kW"] - pr) / pr})
    return rows


def main():
    MW = mw()
    man = json.loads((R / "run-manifest.json").read_text())
    out = {"method": "CHEPTA minus paper; mass % from CHEPTA's component flows and CHEPTA's molar masses (runs info-*); "
                     "paper = Table A2 (streams) and Table 1 (duties) of Piotrowski & Kubica 2021, S2",
           "molar_masses_from_chepta": MW, "limits": {k: {"value": v, "locator": loc} for k, (v, loc) in LIMITS.items()},
           "runs": {}}
    acid = json.loads((R / "info-acetic-acid.output.json").read_text())["value"]["properties"]
    out["acid_record_Tmin_K"] = next(p["Tmin_K"] for p in acid if p["key"] == "liquidHeatCapacity")
    for run in man["runs"]:
        if run["outcome"] != "ok" or run["id"].startswith("info-"):
            continue
        res = json.loads((R / f"{run['id']}.output.json").read_text())
        if "streams" not in res["value"]:
            continue
        out["runs"][run["id"]] = {"streams": compare_streams(res, MW), "duties": compare_duties(res)}
    coup = man.get("plant_coupling") or {}
    # The coupled plant did not converge (round 2 of every attempt stops in column 5). What is compared is round 1 of
    # attempt a2: section A with the paper's streams 21 and 27, then section B fed with CHEPTA's own stream 9, a
    # once-through pass of the whole plant.
    final = coup.get("final") if coup.get("converged") else {"A": f"plant-{coup['attempt']}-r01-A", "B": f"plant-{coup['attempt']}-r01-B"}
    if final:
        a = json.loads((R / f"{final['A']}.output.json").read_text())
        b = json.loads((R / f"{final['B']}.output.json").read_text())
        sa, sb = compare_streams(a, MW), compare_streams(b, MW)
        # streams 1-8 from section A; 9-28 from section B (21 and 27 enter section A as its feeds, equal to B's outlets
        # of the round before, within the coupling tolerance)
        streams = [r for r in sa if r["stream"] <= 8] + [r for r in sb if r["stream"] >= 9]
        out["runs"]["plant-final"] = {"made_of": final, "converged_coupling": bool(coup.get("converged")), "streams": sorted(streams, key=lambda r: r["stream"]),
                                      "duties": compare_duties(a) + compare_duties(b),
                                      "acetic_acid_in_S9_dropped_kmol_h": coup["history"][0]["acetic_acid_dropped_at_cut_kmol_h"]}
        t = {r["stream"]: r for r in streams}
        p16 = t[16]["chepta"]["mass_pct"]
        out["product_checks_plant_final"] = {
            "EA_mass_pct": p16["ethyl-acetate"], "water_mass_pct": p16["water"], "ethanol_mass_pct": p16["ethanol"],
            "EA_meets_99_9": p16["ethyl-acetate"] >= 99.9, "water_meets_0_03": p16["water"] <= 0.03,
            "ethanol_meets_0_04": p16["ethanol"] <= 0.04,
            "S8_acetic_acid_mass_pct": t[8]["chepta"]["mass_pct"]["acetic-acid"],
            "wastewater_organics_mass_pct": 100 - t[25]["chepta"]["mass_pct"]["water"]}
    (R / "comparison-s2.json").write_text(json.dumps(out, indent=1) + "\n")
    for rid, c in out["runs"].items():
        print(f"\n== {rid}")
        for r in c["streams"]:
            ch, pa = r["chepta"], r["paper"]
            print(f"  S{r['stream']:<3d} T {ch['T_C']:6.1f}/{pa['T_C']:5.0f} C  m {ch['kg_h']:9.0f}/{pa['kg_h']:7.0f} ({100*r['rel_kg_h']:+5.1f}%)  "
                  + " ".join(f"{k[:4]} {ch['mass_pct'][k]:6.2f}/{pa['mass_pct'][k]:5.2f}" for k in IDS) + f"  VF {ch['VF']}")
        for d in c["duties"]:
            print(f"  {d['block']:18s} {d['chepta_kW']:9.1f} / {d['paper_kW']:9.1f} kW" + (f" ({100*d['rel']:+.1f}%)" if d['rel'] is not None else ""))


if __name__ == "__main__":
    main()
