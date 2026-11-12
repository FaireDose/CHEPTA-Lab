#!/usr/bin/env python3
"""Lab's checks of the separator flash runs on chepta@0.6.0. Reads files only; never runs CHEPTA.

  regression   each converged run against CHEPTA's own earlier result for the same state, the separator table of
               upstream/2026-11-06-02-mhv1.md (parsed from the copied file, not retyped). Tolerance: half a unit of
               the last printed digit (the table is rounded). A regression check of CHEPTA against itself, not a
               validation: no measured data at this state is used.
  pairs        the pairs without parameters reported by the run against the table's last column.
  balances     Lab's component and energy balances of the flash (feed = vapour + liquid; feed H + duty = products H).
  method_notes what the run itself says about its parameters: per pair, its tier and set; whether the run carries a
               fit-quality flag for pairs that CHEPTA's own advice (in the plain-PR run) calls "fitted inside the rule,
               with a fit-quality warning"; source ids whose names name another pair (for CHEPTA to confirm).
  refusal      the SRK + gE (MHV1) run: the outcome the decision file states (refused for CO2 + water).
Usage: python3 cases/methanol-separator-flash/check_flash.py   (writes results-chepta-0.6.0/checks.json)
"""
import json
import re
from decimal import Decimal
from pathlib import Path

H = Path(__file__).resolve().parent
OUT = H / "results-chepta-0.6.0"
DECISION = H / "upstream/2026-11-06-02-mhv1.md"
ROWS = {"pr-kij": "PR, k_ij (a + b/T for CO2)", "pr-mhv1": "**PR + gE (MHV1)**", "srk-mhv1": "SRK + gE (MHV1)"}
COLUMNS = ["liquid_fraction", "carbon-dioxide", "hydrogen", "carbon-monoxide", "methanol", "water"]
SHORT = {"CO2": "carbon-dioxide", "H2": "hydrogen", "CO": "carbon-monoxide", "methanol": "methanol", "water": "water"}


def load(name):
    return json.loads((H / name).read_text())


def table():
    """The separator table of the decision file: {method label: [cells]}."""
    text = DECISION.read_text()
    start = text.index("**The separator flash**")
    rows = {}
    for line in text[start:].splitlines()[1:]:
        line = line.strip()
        if line.startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows[cells[0]] = cells[1:]
        elif rows and not line.startswith("|"):
            break
    ratio = re.search(r"H2 dissolved in the liquid: ([0-9.]+) times more", text[start:])
    return rows, (ratio.group(1) if ratio else None)


def half_unit(printed):
    return float(Decimal(1).scaleb(Decimal(printed).as_tuple().exponent) / 2)


def slug(name):
    return name.lower().replace(" ", "-")


def pair_key(pair):
    return frozenset(slug(p) for p in pair)


def main():
    case = load("case-input.json")
    rows, ratio_printed = table()
    checks, liquid = [], {}
    advice_flagged = None
    for rid, label in ROWS.items():
        r = load(f"results-chepta-0.6.0/{rid}.output.json")
        cells = rows[label]
        if r["outcome"] != "ok":
            checks.append({"id": rid, "kind": "refusal", "decision_file_says": cells[0], "observed": r["outcome"],
                           "error": r.get("error"),
                           "passed": r["outcome"] == "unsupported" and "Carbon dioxide + Water" in r["error"]["message"]})
            continue
        v = r["value"]
        S1, S2, S3 = (v["streams"][k] for k in ("S1", "S2", "S3"))
        observed = {"liquid_fraction": S3["F_kmol_h"] / S1["F_kmol_h"],
                    **{c: S3["z"][i] for i, c in enumerate(S3["components"])}}
        liquid[rid] = observed
        reg = []
        for name, printed in zip(COLUMNS, cells[:6]):
            tol = half_unit(printed) * 1.0000001
            reg.append({"quantity": name if name == "liquid_fraction" else f"x {name}", "printed": printed,
                        "observed": observed[name], "difference": observed[name] - float(printed), "tolerance": tol,
                        "passed": abs(observed[name] - float(printed)) <= tol})
        checks.append({"id": rid, "kind": "regression", "against": f"{DECISION.name}, separator table, row '{label}'",
                       "rows": reg, "passed": all(x["passed"] for x in reg)})

        # pairs without parameters: the run's qualifications against the table's last column
        printed_pairs = re.sub(r"\(.*?\)", "", cells[6]).split(",")
        expected = sorted(sorted(SHORT[x.strip()] for x in p.split("+")) for p in printed_pairs)
        got = sorted(sorted(slug(x) for x in p) for p in r["qualifications"]["missing_pairs"])
        checks.append({"id": rid, "kind": "pairs_without_parameters", "printed": cells[6], "observed": got,
                       "expected": expected, "passed": got == expected})

        # balances by Lab
        comp = {c: S1["flow_kmol_h"][c] - S2["flow_kmol_h"][c] - S3["flow_kmol_h"][c] for c in S1["components"]}
        duty = v["blocks"]["V1"]["duty_kW"]
        energy = S1["H_kW"] + duty - S2["H_kW"] - S3["H_kW"]
        tol_mat, tol_en = 1e-9 * S1["F_kmol_h"], 1e-6
        checks.append({"id": rid, "kind": "balances", "component_kmol_h": comp, "energy_kW": energy,
                       "flash_duty_kW": duty, "tolerances": {"material_kmol_h": tol_mat, "energy_kW": tol_en,
                                                             "basis": "Lab's choice: 1e-9 of the feed; 1e-6 kW"},
                       "chepta_reported": v["balance"],
                       "passed": max(abs(x) for x in comp.values()) <= tol_mat and abs(energy) <= tol_en})

        if rid == "pr-kij":  # CHEPTA's advice in the plain-PR run names the MHV1 sets with a fit-quality warning
            advice = next((w for w in S1["warnings"] if w.startswith("Above 10 bar, PR + gE (MHV1)")), "")
            advice_flagged = sorted(sorted(slug(x) for x in m.split(" + "))
                                    for m in re.findall(r"([A-Z][a-z]+(?: [a-z]+)? \+ [A-Z][a-z]+(?: [a-z]+)?): fitted "
                                                        r"inside the rule, with a fit-quality warning", advice))

    # what the MHV1 run itself says about each pair (read from its stream S1, which carries the pair sources)
    mhv1 = load("results-chepta-0.6.0/pr-mhv1.output.json")
    text = json.dumps(mhv1)
    pairs = []
    for p in mhv1["value"]["streams"]["S1"]["sources"]:
        names = [slug(x) for x in p["pair"]]
        other = [s for s in p["source_ids"] if not all(n in s for n in names)
                 and s not in ("nist-thermoml-archive", "iapws-g7-04")]
        pairs.append({"pair": names, "set": p["set"], "tier": p["tier"],
                      "flagged_fit_quality_by_chepta_advice_in_pr_kij": sorted(names) in (advice_flagged or []),
                      "source_ids_naming_another_system": other})
    checks.append({"id": "pr-mhv1", "kind": "method_notes", "pairs": pairs,
                   "pairs_flagged_fit_quality_in_pr_kij_advice": advice_flagged,
                   "pr_mhv1_output_mentions_fit_quality": ("fit-quality" in text) or ("quality_warning" in text),
                   "pr_mhv1_warnings_S1": mhv1["value"]["streams"]["S1"]["warnings"],
                   "pr_mhv1_qualification_warnings": mhv1["qualifications"]["warnings"],
                   "note": "Observation, not a pass/fail check: the fit-quality known issues of the MHV1 sets appear in "
                           "the plain-PR run's advice, not in the MHV1 run's own warnings or qualifications.",
                   "passed": True})

    # derived: how much more H2 dissolves under MHV1 than under plain PR, against the decision file's "3.2 times"
    ratio = liquid["pr-mhv1"]["hydrogen"] / liquid["pr-kij"]["hydrogen"]
    checks.append({"id": "pr-mhv1", "kind": "derived_ratio",
                   "quantity": "x_H2 in the liquid, PR + gE (MHV1) over plain PR", "observed": ratio,
                   "printed": ratio_printed, "tolerance": half_unit(ratio_printed),
                   "passed": abs(ratio - float(ratio_printed)) <= half_unit(ratio_printed)})

    result = {"checked_by": "check_flash.py (Lab); reads files only",
              "case_input": {"T_K": case["T_K"], "P_kPa": case["P_kPa"]},
              "tolerances": {"regression": "half a unit of the last printed digit of the decision file's table"},
              "checks": checks}
    (OUT / "checks.json").write_text(json.dumps(result, indent=2) + "\n")
    for c in checks:
        print(c["id"], c["kind"], "passed" if c["passed"] else "FAILED")


if __name__ == "__main__":
    main()
