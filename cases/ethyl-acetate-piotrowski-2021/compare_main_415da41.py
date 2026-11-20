#!/usr/bin/env python3
"""Plant S2 on CHEPTA main 415da41 against the same requests on chepta 0.6.2: outcomes and the numbers the README
quotes (product 16 purity, water and ethanol; azeotrope 8 acid; wastewater 25 flow and organics; key duties), and every
warning code CHEPTA returned. Reads results-chepta-0.6.2/ and results-chepta-main-415da41/ (and the generic
comparison-with-results-chepta-0.6.2.json of scripts/compare_chepta_reruns.py); writes
results-chepta-main-415da41/comparison-s2-main-415da41.json and prints one line per run. No CHEPTA call.
Mass fractions from CHEPTA's component flows and chepta 0.6.2's molar masses (runs info-*, unchanged on main).
  python3 cases/ethyl-acetate-piotrowski-2021/compare_main_415da41.py
"""
import json
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import compare_s2 as C1  # noqa: E402

A, B = H / "results-chepta-0.6.2", H / "results-chepta-main-415da41"
IDS = C1.IDS


def mw():
    return {c: json.loads((A / f"info-{c}.output.json").read_text())["value"]["MW"] for c in IDS}


def view(o, MW):
    if not o or o.get("outcome") != "ok":
        return None
    v = o["value"]
    s = v.get("streams") or {}
    out = {}
    for n in ("S16", "S8", "S25", "S13", "S11", "S5", "S21"):
        if n in s:
            sv = C1.stream_view(s[n], MW)
            out[n] = {"kg_h": round(sv["kg_h"], 1), **{f"{c}_mass_pct": round(sv["mass_pct"][c], 4) for c in IDS}}
    bl = v.get("blocks") or {}
    out["duties_kW"] = {k: round(b.get("duty_kW"), 1) for k, b in bl.items() if isinstance(b, dict) and b.get("duty_kW")}
    lp = v.get("loops") or []
    out["loop_iterations"] = [x.get("iterations") for x in lp]
    out["balance_warnings"] = (v.get("balance") or {}).get("warnings")
    if v.get("designSpecs"):
        out["designSpecs"] = v["designSpecs"]
    return out


def warnings(o):
    acc = {}

    def walk(x, inside=False):
        if isinstance(x, dict):
            if inside and x.get("code"):
                acc[x["code"]] = acc.get(x["code"], 0) + 1
            for k, w in x.items():
                walk(w, inside or k == "warnings")
        elif isinstance(x, list):
            for w in x:
                walk(w, inside)
    walk(o)
    return acc


def load(p):
    try:
        return json.loads(p.read_text()) if p.exists() and p.read_text().strip() else {}
    except json.JSONDecodeError:
        return {}


def main():
    MW = mw()
    man = json.loads((B / "run-manifest.json").read_text())
    rows = []
    for r in man["runs"]:
        rid = r["id"]
        o1, o2 = load(A / f"{rid}.output.json"), load(B / f"{rid}.output.json")
        e1, e2 = o1.get("error") or {}, o2.get("error") or {}
        row = {"id": rid, "new": r.get("new", False), "outcome_062": o1.get("outcome"), "code_062": e1.get("code"),
               "outcome_main": o2.get("outcome"), "code_main": e2.get("code"), "message_main": e2.get("message"),
               "warnings_062": warnings(o1), "warnings_main": warnings(o2), "chepta_062": view(o1, MW), "chepta_main": view(o2, MW)}
        rows.append(row)
        p1 = (row["chepta_062"] or {}).get("S16", {}).get("ethyl-acetate_mass_pct")
        p2 = (row["chepta_main"] or {}).get("S16", {}).get("ethyl-acetate_mass_pct")
        print(f"{rid}: {row['outcome_062']}/{row['code_062']} -> {row['outcome_main']}/{row['code_main']}; "
              f"ester in 16: {p1} -> {p2}; warnings main {row['warnings_main']}")
    (B / "comparison-s2-main-415da41.json").write_text(json.dumps(
        {"method": __doc__.split("\n\n")[0], "chepta_commit": man.get("chepta_commit"), "molar_masses": MW, "runs": rows}, indent=1) + "\n")


if __name__ == "__main__":
    main()
