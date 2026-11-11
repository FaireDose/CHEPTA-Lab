# Compatibility check: CHEPTA 0.6.0 against the ethanol benchmark

Date: 2026-11-11. Status: draft engineering evidence; no human review is recorded. Not a validation against experiment.

## Verdict

**Lab can move its pin to `chepta@0.6.0` for this benchmark.** All six runs were accepted by the released package, converged, and gave the **same numbers to the last stored digit** as the old commit `c1adf6b`. The independent calculation (`verify.py`) passes with the same errors as before. The only change we found in outcomes, numbers or warnings is **one reworded warning** (details below).

What this does *not* show: only one reactor type, one thermodynamic method (Peng-Robinson) and one case were exercised. It says nothing about the column, extraction, ethyl acetate or CO2 work, which the old pin could not run anyway. Matching numbers show the engine did not change here, not that the numbers match experiment.

## How it was run

- Package `chepta@0.6.0` from npm, MIT licence, exact pin in `package.json`; integrity `sha512-i3/U78TPzz93Y0Cp2/WZ+VjhdxSDY6oX5AZdbRDe5kL08P0NVAGKQRGRJyihUJ7SPTgYZzZlz738keuYBpHtFg==` (from `package-lock.json`). Node v22.23.4, npm 10.9.9.
- Command per run: `npx chepta request <request file>`. Exit code 0 for all six runs.
- **Request format: unchanged.** The six old request files were copied byte for byte (the manifest records `request_changed_from_old: false`); the package accepted them as they are.
- New files: `results-chepta-0.6.0/` (requests, outputs, empty stderr files, `run-manifest.json`, `comparison.json`, `verification.json`). Old `results/` is untouched and keeps engine commit `c1adf6b`.
- Scripts: `run_chepta_0.6.0.py` (runs and manifest), `compare_chepta_0.6.0.py` (old-versus-new comparison), `verify.py` (now takes an optional results folder; default unchanged).

## Per-run results (simulated values; ethanol feed 1 mol/h)

Conversion = 100 × (1 − ethanol outlet / ethanol feed). "Outlet" differences are the largest absolute difference over the four components in mol/h. Duty is the reactor heat duty reported by CHEPTA (kW).

| Run | Outcome old / new | Conversion old (%) | Conversion new (%) | Difference | Largest outlet difference | Duty old (kW) | Duty new (kW) | Difference | Independent-check max relative error old / new |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| upstream_simplified-wf0.38 | ok / ok | 0.337102 | 0.337102 | 0 | 0 | 1.515985e-05 | 1.515985e-05 | 0 | 9.81e-08 / 9.81e-08 |
| upstream_simplified-wf0.773 | ok / ok | 0.685136 | 0.685136 | 0 | 0 | 3.079516e-05 | 3.079516e-05 | 0 | 2.5e-07 / 2.5e-07 |
| upstream_simplified-wf1.166 | ok / ok | 1.032557 | 1.032557 | 0 | 0 | 4.638658e-05 | 4.638658e-05 | 0 | 3.61e-07 / 3.61e-07 |
| table12_adsorption-wf0.38 | ok / ok | 0.331163 | 0.331163 | 0 | 0 | 1.504470e-05 | 1.504470e-05 | 0 | 2.35e-06 / 2.35e-06 |
| table12_adsorption-wf0.773 | ok / ok | 0.661353 | 0.661353 | 0 | 0 | 3.033289e-05 | 3.033289e-05 | 0 | 2.74e-06 / 2.74e-06 |
| table12_adsorption-wf1.166 | ok / ok | 0.980123 | 0.980123 | 0 | 0 | 4.536510e-05 | 4.536510e-05 | 0 | 3.07e-06 / 3.07e-06 |

Differences are exactly zero in the stored 64-bit numbers (`comparison.json` compares every leaf value of the outputs, not just these columns). The reported element, mass and energy balance residuals are also unchanged. The independent check (`results-chepta-0.6.0/verification.json`) passed for all six runs with its original tolerances (SciPy 1.17.0 both times).

## Warnings per run (old 7, new 7, in every run)

The same seven warnings appear on the feed and product streams in every run. Counted per run: **6 unchanged, 1 reworded (counted as 1 removed and 1 added), 0 purely new, 0 purely removed.**

Unchanged (kept, still relevant):
1. Five "No PR k_ij" warnings: Ethanol+Ethylene, Ethanol+Diethyl ether, Ethylene+Diethyl ether, Ethylene+Water, Water+Diethyl ether use k_ij = 0, a prediction without binary data.
2. "k_ij of Ethanol + Water (-0.0931) comes from data at 351.26-368.18 K; 573.15 K is outside that range." The reaction is at 573.15 K. This range warning is unresolved; the benchmark's phase-behaviour inputs are not validated at this temperature. All streams here are vapour, which limits but does not remove the concern.

| | Text |
|---|---|
| Removed (old) | "PR for a mixture with polar components (Ethanol, Water, Diethyl ether) is not the recommended method for their liquid: below about 10 bar an activity model (NRTL or UNIQUAC) describes it better; above 10 bar PSRK or a cubic equation with Wong-Sandler or MHV2 mixing rules, which CHEPTA does not have yet (docs/METHOD_SELECTION.md)." |
| Added (new) | Same first part, then: "above 10 bar a cubic equation with a gE mixing rule (PSRK, Wong-Sandler, MHV2), in CHEPTA "PR + gE (MHV1)" or "SRK + gE (MHV1)" (mixing: "MHV1"), which takes the pairs' NRTL sets into the equation of state (docs/METHOD_SELECTION.md)." |

Reading: the warning is the same warning, now pointing to an MHV1 mixing option that 0.6.0 has and the old commit did not. We did not change the method (the requests still use plain PR), so this wording change does not affect any number. The advice itself applies to the liquid phase above about 10 bar; this benchmark is at 1 atm with a vapour product. We did not test the suggested alternative method.

Also unchanged in the outputs: `qualifications` (same pairs, same tiers, no notes). Different identifiers only: `reproduction.library` 0.4.0 → 0.6.0, `reproduction.databank_hash` 70b7222aab73671b → 852b926c89fa84fa (the databank content changed between versions; **we did not investigate what changed in it**, and none of the values used by these runs changed), the run id and the elapsed time. The `input_hash` (8b39b8a12c146480) is identical.

## Failures and disagreements

None found: no refused run, no non-zero exit code, no changed number. If the databank change matters for other components, only a run that uses them can show it.

## Candidate capability requests

No run was refused, so nothing is required for this case. Two things to consider, not requested:
- Whether the ethanol/ethylene/ether/water case should be re-run with the new "PR + gE (MHV1)" option, as the reworded warning suggests. This only matters if a liquid phase becomes part of a case.
- A way to see what changed in the databank between versions (its hash changed; the release notes were not read for this check).

## What remains unchanged and unresolved

Source pressure-unit conventions, original experimental data, the 573 K range warning, missing binary parameters and human engineering review (all in `README.md` and `record.json` of this case). Old results and old manifest keep engine commit `c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2`.
