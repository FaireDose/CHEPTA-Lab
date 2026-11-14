#!/usr/bin/env python3
"""Look for flows that have blown up in a converged CHEPTA plant (the maintainer, 2026-11-14): a converged loop can still
carry an inventory that has grown far from the paper's. No CHEPTA call; reads result files, writes blowout-check.json.
For each converged closed plant: every stream's mass flow and each component flow against Table A2 (ratio CHEPTA/paper),
the internal liquid and vapour flows of every column stage against the column's feed, the recycle (tear) streams, and
the plant balance (feeds 1, 2, 17 against products 16, 25, on CHEPTA's molar masses).
  python3 cases/ethyl-acetate-piotrowski-2021/check_blowout_062.py
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
R = H / "results-chepta-0.6.2"
PAPER = {int(r["stream"]): r for r in json.loads((H / "streams.json").read_text())["strategies"]["S2"]}
IDS = ["ethanol", "water", "ethyl-acetate", "acetic-acid"]
KEYS = ["ethanol", "water", "ethyl_acetate", "acetic_acid"]
FLAG = 1.5  # a stream or component more than 1.5x (or below 1/1.5 of) the paper's is flagged, where the paper's is not a trace
TRACE_KG_H = 50.0  # component flows below this in the paper are traces: compared, not flagged


def main():
    MW = {c: json.loads((R / f"info-{c}.output.json").read_text())["value"]["MW"] for c in IDS}
    man = json.loads((R / "run-manifest.json").read_text())
    closed = [r["id"] for r in man["runs"] if r["id"].startswith("plant62") and r["outcome"] == "ok" and not r["id"].endswith("-open")]
    out = {"method": __doc__.strip().splitlines()[0], "flag_ratio": FLAG, "trace_kg_h": TRACE_KG_H, "runs": {}}
    for rid in closed:
        v = json.loads((R / f"{rid}.output.json").read_text())["value"]
        S = v["streams"]
        rows, flags = [], []
        for sid, s in S.items():
            n = int(sid[1:])
            p = PAPER[n]
            m = {c: s["flow_kmol_h"].get(c, 0) * MW[c] for c in IDS}
            tot = sum(m.values())
            row = {"stream": n, "kg_h": tot, "paper_kg_h": p["mass_kg_h"], "ratio": tot / p["mass_kg_h"], "components": {}}
            if not (1 / FLAG <= row["ratio"] <= FLAG):
                flags.append(f"stream {n}: {tot:.0f} kg/h vs {p['mass_kg_h']:.0f}")
            for c, k in zip(IDS, KEYS):
                pk = p["mass_kg_h"] * p[k + "_mass_pct"] / 100
                row["components"][c] = {"kg_h": m[c], "paper_kg_h": pk, "ratio": (m[c] / pk) if pk else None}
                if pk >= TRACE_KG_H and not (1 / FLAG <= m[c] / pk <= FLAG):
                    flags.append(f"stream {n} {c}: {m[c]:.0f} kg/h vs {pk:.0f}")
            rows.append(row)
        cols = {}
        for bid, b in v["blocks"].items():
            if b.get("type") != "column" or "profile" not in b:
                continue
            prof = b["profile"]
            Lmax = max(st["L_kmol_h"] or 0 for st in prof)
            Vmax = max(st["V_kmol_h"] or 0 for st in prof)
            feed_kmol_h = sum(S[s]["F_kmol_h"] for s in S if any(x for x in (json.loads((R / f"{rid}.request.json").read_text())["input"]["flowsheet"]["streams"]) if x["id"] == s and x["to"].startswith(bid + ".")))
            two = [st["stage"] for st in prof if st.get("liquids")]
            cols[bid] = {"stages": len(prof), "max_L_kmol_h": Lmax, "max_V_kmol_h": Vmax, "feed_kmol_h": feed_kmol_h,
                         "max_L_over_feed": Lmax / feed_kmol_h, "max_V_over_feed": Vmax / feed_kmol_h, "two_liquid_stages": two,
                         "T_range_C": [min(st["T_K"] for st in prof) - 273.15, max(st["T_K"] for st in prof) - 273.15]}
            if Lmax / feed_kmol_h > 10 or Vmax / feed_kmol_h > 10:
                flags.append(f"{bid}: internal flow {max(Lmax, Vmax):.0f} kmol/h, more than 10x its feed {feed_kmol_h:.0f}")
        mass = lambda s: sum(S[s]["flow_kmol_h"].get(c, 0) * MW[c] for c in IDS)  # noqa: E731
        bal = {"in_kg_h": mass("S1") + mass("S2") + mass("S17"), "out_kg_h": mass("S16") + mass("S25")}
        bal["diff_kg_h"] = bal["in_kg_h"] - bal["out_kg_h"]
        out["runs"][rid] = {"loop": v["loops"], "plant_balance": bal, "balance_reported_by_chepta": v["balance"],
                            "flags": flags, "columns": cols, "streams": sorted(rows, key=lambda r: r["stream"])}
    (R / "blowout-check.json").write_text(json.dumps(out, indent=1) + "\n")
    for rid, c in out["runs"].items():
        print(f"== {rid}: balance in {c['plant_balance']['in_kg_h']:.1f} out {c['plant_balance']['out_kg_h']:.1f} kg/h")
        rs = sorted(c["streams"], key=lambda r: abs(r["ratio"] - 1), reverse=True)[:4]
        print("   largest stream deviations:", ", ".join(f"{r['stream']}: x{r['ratio']:.3f}" for r in rs))
        for b, x in c["columns"].items():
            print(f"   {b}: {x['stages']} stages, L max {x['max_L_kmol_h']:.0f}, V max {x['max_V_kmol_h']:.0f} kmol/h (feed {x['feed_kmol_h']:.0f}; x{max(x['max_L_over_feed'], x['max_V_over_feed']):.2f}), two liquids on {x['two_liquid_stages']}, T {x['T_range_C'][0]:.1f}-{x['T_range_C'][1]:.1f} C")
        print("   flags:", c["flags"] or "none")


if __name__ == "__main__":
    main()
