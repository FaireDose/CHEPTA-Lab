#!/usr/bin/env python3
"""Lab's checks of the B2 runs on chepta@0.6.0. Reads files only; never runs CHEPTA.

Three checks of the converged run b2-pr, reported apart:
  1. same_equation  CHEPTA's result against CHEPTA's stored independent reference solution (reference_mesh.py, the
                    same property method and energy balances), with the record's numerical tolerances. Lab did not
                    re-execute reference_mesh.py: it compares with the stored solution (upstream/reference_mesh-B2.json).
  2. published      CHEPTA's result against the published ChemSep Book numbers as transcribed in CHEPTA's record, with
                    the record's agreement tolerances (1 K, 0.02 mole fraction). Agreement between two property
                    methods (the source used UNIFAC + Antoine with constant molar overflow), not experimental accuracy.
  3. balances       Lab's own component balances (overall and on every stage, from the profile) and the overall energy
                    balance (feed enthalpy + reboiler duty - condenser duty - product enthalpies).
And, for the two refused runs, whether the outcome is the one expected.
Usage: python3 cases/benzene-toluene-chemsep-b2/check_b2.py   (writes results-chepta-0.6.0/checks.json)
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
OUT = H / "results-chepta-0.6.0"
KMOL_H_PER_MOL_S = 3.6
KELVIN = 273.15
EXPECTED = {
    "b2-record-thermo-literal": {"outcome": "invalid_input", "why": "found on the first attempt: the record's thermo "
                                 "block carries sets: \"default\", which the request path does not take"},
    "b2-distillate-purity": {"outcome": "unsupported", "why": "CHEPTA docs/models/columns.md at v0.6.0: purity "
                             "specifications are not built yet (milestone M4)"},
}


def load(name):
    return json.loads((H / name).read_text())


def worst(pairs):
    """pairs: list of (label, observed, reference); returns the largest absolute difference and where."""
    rows = [{"where": w, "observed": o, "reference": r, "difference": o - r} for w, o, r in pairs]
    top = max(rows, key=lambda q: abs(q["difference"]))
    return {"max_abs_difference": abs(top["difference"]), "at": top["where"], "rows": rows}


def main():
    rec = load("upstream/B2-chemsep-benzene-toluene.json")
    ref = load("upstream/reference_mesh-B2.json")["case"]["rigorous"]
    out = load("results-chepta-0.6.0/b2-pr.output.json")
    comps = rec["components"]
    col, prof = out["value"]["column"], out["value"]["column"]["profile"]
    D, B = out["value"]["distillate"], out["value"]["bottoms"]
    num = rec["tolerances"]["numerical"]["engine_against_reference"]
    agree = rec["tolerances"]["agreement_with_published_example"]
    pub = rec["published"]

    # 1. Same equations: CHEPTA (JavaScript, Newton on MESH) against reference_mesh.py's stored solution.
    T = worst([(f"stage {s['stage']}", s["T_K"], q["T_K"]) for s, q in zip(prof, ref["stages"])])
    Lrel = worst([(f"stage {s['stage']}", s["L_kmol_h"] / KMOL_H_PER_MOL_S / q["L_mol_s"], 1.0)
                  for s, q in zip(prof, ref["stages"]) if q["L_mol_s"]])
    x = worst([(f"stage {s['stage']} {c}", s["x"][c], q["x"][i]) for s, q in zip(prof, ref["stages"])
               for i, c in enumerate(comps)])
    duties = worst([("condenser", col["condenser_kW"] * 1000 / ref["Q_condenser_W"], 1.0),
                    ("reboiler", col["reboiler_kW"] * 1000 / ref["Q_reboiler_W"], 1.0)])
    same = {"T_K": {**T, "tolerance": num["T_K_absolute"]},
            "L_relative": {**Lrel, "tolerance": num["flows_relative"]},
            "x": {**x, "tolerance": num["mole_fractions_absolute"]},
            "duties_relative": {**duties, "tolerance": num["duties_relative"]}}
    for v in same.values():
        v["passed"] = v["max_abs_difference"] <= v["tolerance"]

    # 2. Published numbers (another property method): T and benzene's x on every stage, x_D and x_B.
    pT = worst([(f"stage {s['stage']}", s["T_K"], tc + KELVIN) for s, tc in zip(prof, pub["T_C"])])
    px = worst([(f"stage {s['stage']}", s["x"][comps[0]], xb) for s, xb in zip(prof, pub["x_benzene"])]
               + [("distillate x_D", D["z"][0], pub["x_D"][0]), ("bottoms x_B", B["z"][0], pub["x_B"][0])])
    shown = {"D_mol_s": {"observed": col["D_kmol_h"] / KMOL_H_PER_MOL_S, "published": pub["D_mol_s"]},
             "B_mol_s": {"observed": col["B_kmol_h"] / KMOL_H_PER_MOL_S, "published": pub["B_mol_s"]},
             "reflux_ratio": {"observed": col["reflux_ratio"], "published": pub["reflux_ratio"]},
             "boilup_ratio": {"observed": col["boilup_ratio"], "published": pub["boilup_ratio"]},
             "feed_T_K": {"observed": out["value"]["feed"]["T_K"], "published": pub["feed_T_C"] + KELVIN}}
    for v in shown.values():
        v["difference"] = v["observed"] - v["published"]
    published = {"T_K": {**pT, "tolerance": agree["T_K_absolute"]},
                 "x_benzene": {**px, "tolerance": agree["mole_fractions_absolute"]},
                 "not_compared_shown_only": shown,
                 "note": "Tolerances from CHEPTA's record (agreement_with_published_example). The boil-up ratio and the "
                         "flows inside the column are not compared: the source assumed constant molar overflow, "
                         "CHEPTA solves energy balances. The published K column is not compared (the record's notes)."}
    for k in ("T_K", "x_benzene"):
        published[k]["passed"] = published[k]["max_abs_difference"] <= published[k]["tolerance"]

    # 3. Balances, computed by Lab from the result (kmol/h and kW).
    feed = out["value"]["feed"]["flow_kmol_h"]
    overall = {c: feed[c] - D["flow_kmol_h"][c] - B["flow_kmol_h"][c] for c in comps}
    n, fs = len(prof), {f["stage"] if isinstance(f, dict) else f for f in col["feed_stages"]}
    stage_res = []
    for j, s in enumerate(prof):
        for c in comps:
            inn = (prof[j - 1]["L_kmol_h"] * prof[j - 1]["x"][c] if j > 0 else 0) \
                + (prof[j + 1]["V_kmol_h"] * prof[j + 1]["y"][c] if j < n - 1 else 0) \
                + (feed[c] if s["stage"] in fs else 0)
            leave = s["L_kmol_h"] * s["x"][c] + (s["V_kmol_h"] * s["y"][c] if s["y"] else 0) \
                + (D["flow_kmol_h"][c] if j == 0 else 0)
            stage_res.append({"stage": s["stage"], "component": c, "residual_kmol_h": inn - leave})
    energy = out["value"]["feed"]["H_kW"] + col["reboiler_kW"] - col["condenser_kW"] - D["H_kW"] - B["H_kW"]
    F = sum(feed.values())
    tol_mat = 1e-8 * F  # CHEPTA's own stage tolerance, relative to the feed (record: balances_on_every_stage)
    tol_en = 1e-8 * F * KMOL_H_PER_MOL_S ** -1 * 10.0  # F (mol/s) x 10 kJ/mol x 1e-8, in kW
    balances = {
        "overall_component_kmol_h": overall,
        "overall_max_abs_kmol_h": max(abs(v) for v in overall.values()),
        "stage_component_max_abs_kmol_h": max(abs(r["residual_kmol_h"]) for r in stage_res),
        "stage_residuals": stage_res,
        "energy_kW": energy,
        "tolerances": {"material_kmol_h": tol_mat, "energy_kW": tol_en,
                       "basis": "the record's balances_on_every_stage: 1e-8 of the feed; energy 1e-8 x F x 10 kJ/mol"},
        "chepta_reported": {"material_kmol_h": out["checks"]["material_kmol_h"], "energy_kW": out["checks"]["energy_kW"]},
    }
    balances["passed"] = (balances["overall_max_abs_kmol_h"] <= tol_mat and balances["stage_component_max_abs_kmol_h"]
                          <= tol_mat and abs(energy) <= tol_en)

    refusals = []
    for rid, exp in EXPECTED.items():
        r = load(f"results-chepta-0.6.0/{rid}.output.json")
        refusals.append({"id": rid, "kind": "outcome", "expected": exp["outcome"], "why": exp["why"],
                         "observed": r["outcome"], "error": r.get("error"), "passed": r["outcome"] == exp["outcome"]})

    result = {
        "checked_by": "check_b2.py (Lab); reads files only",
        "tolerances": {"numerical": num, "agreement_with_published_example": agree},
        "checks": [
            {"id": "b2-pr", "kind": "same_equation", "result": same,
             "passed": all(v["passed"] for v in same.values())},
            {"id": "b2-pr", "kind": "published", "result": published,
             "passed": published["T_K"]["passed"] and published["x_benzene"]["passed"]},
            {"id": "b2-pr", "kind": "balances", "result": balances, "passed": balances["passed"]},
            {"id": "b2-pr", "kind": "warnings", "column_warnings": col["warnings"],
             "qualification_warnings": out["qualifications"]["warnings"],
             "expected_by_record": rec["expected"]["warnings"],
             "passed": col["warnings"] == rec["expected"]["warnings"]},
        ] + refusals,
    }
    (OUT / "checks.json").write_text(json.dumps(result, indent=2) + "\n")
    for c in result["checks"]:
        print(c["id"], c["kind"], "passed" if c["passed"] else "FAILED")


if __name__ == "__main__":
    main()
