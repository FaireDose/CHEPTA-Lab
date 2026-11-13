#!/usr/bin/env python3
"""Compare the chepta 0.6.2 runs of plant S2 with the paper (Table A2 streams, Table 1 duties) and with 0.6.1.

Reads results-chepta-0.6.2/*.output.json and run-manifest.json (and the 0.6.1 manifest for the re-runs); writes
results-chepta-0.6.2/comparison-s2.json and prints the tables used in the README. No CHEPTA call.
Mass fractions from CHEPTA's component flows and CHEPTA 0.6.2's own molar masses (runs info-*). Differences are
CHEPTA minus paper. Every compared number carries the extrapolations CHEPTA listed for the block that made it
(result.value.extrapolations, field "where") and the run's estimated (predicted) pairs (qualifications.estimated_pairs).
  python3 cases/ethyl-acetate-piotrowski-2021/compare_s2_062.py
"""
import json
from pathlib import Path

import compare_s2 as C1

H = Path(__file__).resolve().parent
R = H / "results-chepta-0.6.2"
OLD = H / "results-chepta-0.6.1"
IDS = C1.IDS


def mw():
    return {c: json.loads((R / f"info-{c}.output.json").read_text())["value"]["MW"] for c in IDS}


def producers(req):
    """Stream id -> the block it comes from (its 'from' port's block)."""
    return {s["id"]: s["from"].split(".")[0] for s in req["input"]["flowsheet"]["streams"]}


def flags_for(res, block):
    ex = [e.get("short") for e in res["value"].get("extrapolations", []) if block in (e.get("where") or [])]
    est = [e.get("pair") for e in (res.get("qualifications") or {}).get("estimated_pairs", [])]
    return {"extrapolated": ex, "estimated_pairs": est}


def compare_run(res, req, MW):
    prod = producers(req)
    rows = []
    for sid, s in res["value"]["streams"].items():
        base = sid[1:].rstrip("o")
        if not base.isdigit():
            continue
        n = int(base)
        if n not in C1.PAPER:
            continue
        c, p = C1.stream_view(s, MW), C1.paper_view(n)
        rows.append({"stream": n, "id": sid, "chepta": c, "paper": p, "dT_K": c["T_C"] - p["T_C"], "dkg_h": c["kg_h"] - p["kg_h"],
                     "rel_kg_h": (c["kg_h"] - p["kg_h"]) / p["kg_h"],
                     "dmass_pct_points": {k: c["mass_pct"][k] - p["mass_pct"][k] for k in IDS},
                     "depends_on": flags_for(res, prod.get(sid, ""))})
    duties = C1.compare_duties(res)
    for d in duties:
        bid = d["block"].replace(" condenser", "").replace(" reboiler", "").replace(" ", "")
        d["depends_on"] = flags_for(res, bid)
    return {"streams": sorted(rows, key=lambda r: r["stream"]), "duties": duties,
            "extrapolations_all": [e.get("short") for e in res["value"].get("extrapolations", [])],
            "estimated_pairs_all": (res.get("qualifications") or {}).get("estimated_pairs", [])}


def main():
    MW = mw()
    man = json.loads((R / "run-manifest.json").read_text())
    old = {r["id"]: r for r in json.loads((OLD / "run-manifest.json").read_text())["runs"]}
    out = {"method": "CHEPTA 0.6.2 minus paper; mass % from CHEPTA's component flows and CHEPTA 0.6.2's molar masses (runs info-*); "
                     "paper = Table A2 and Table 1 of Piotrowski & Kubica 2021, S2. depends_on: the extrapolations CHEPTA listed for the block "
                     "that made the stream (result.value.extrapolations[].where) and the run's estimated pairs",
           "molar_masses_from_chepta": MW, "reruns": [], "outcomes": [], "runs": {}}
    for r in man["runs"]:
        e = r.get("error") or {}
        out["outcomes"].append({"id": r["id"], "outcome": r["outcome"], "code": e.get("code"), "message": e.get("message"),
                                "elapsed_ms": r.get("elapsed_ms"), "extrapolations": r.get("extrapolations", []),
                                "estimated_pairs": r.get("estimated_pairs", []), "note": r.get("note")})
        if r["id"].startswith("rerun-"):
            o = old[r["id"][6:]]
            oe = o.get("error") or {}
            out["reruns"].append({"run_061": o["id"], "outcome_061": o["outcome"], "code_061": oe.get("code"),
                                  "run_062": r["id"], "outcome_062": r["outcome"], "code_062": e.get("code"),
                                  "message_062": e.get("message"), "extrapolations_062": r.get("extrapolations", [])})
        if r["outcome"] != "ok" or r["id"].startswith("info-"):
            continue
        res = json.loads((R / f"{r['id']}.output.json").read_text())
        if "streams" not in res.get("value", {}):
            continue
        req = json.loads((R / f"{r['id']}.request.json").read_text())
        out["runs"][r["id"]] = compare_run(res, req, MW)
    (R / "comparison-s2.json").write_text(json.dumps(out, indent=1) + "\n")
    print("== re-runs of the 0.6.1 refusals")
    for x in out["reruns"]:
        print(f"  {x['run_061']:32s} {x['outcome_061']}/{x['code_061']} -> {x['outcome_062']}/{x['code_062']}  extrap {len(x['extrapolations_062'])}")
    print("== all outcomes")
    for x in out["outcomes"]:
        print(f"  {x['id']:42s} {x['outcome']}/{x['code']}  {(x['message'] or '')[:160]}")
    for rid, c in out["runs"].items():
        if rid.startswith("rerun-u3") or rid.startswith("info"):
            continue
        print(f"\n== {rid}  (extrapolations {len(c['extrapolations_all'])}, estimated pairs {len(c['estimated_pairs_all'])})")
        for r in c["streams"]:
            ch, pa = r["chepta"], r["paper"]
            fl = " X" if r["depends_on"]["extrapolated"] else ""
            print(f"  {r['id']:<4s} T {ch['T_C']:6.1f}/{pa['T_C']:5.0f} C  m {ch['kg_h']:9.0f}/{pa['kg_h']:7.0f} ({100*r['rel_kg_h']:+5.1f}%)  "
                  + " ".join(f"{k[:4]} {ch['mass_pct'][k]:6.3f}/{pa['mass_pct'][k]:5.2f}" for k in IDS) + f"  VF {ch['VF']}{fl}")
        for d in c["duties"]:
            fl = " X" if d["depends_on"]["extrapolated"] else ""
            print(f"  {d['block']:18s} {d['chepta_kW']:9.1f} / {d['paper_kW']:9.1f} kW" + (f" ({100*d['rel']:+.1f}%)" if d['rel'] is not None else "") + fl)


if __name__ == "__main__":
    main()
