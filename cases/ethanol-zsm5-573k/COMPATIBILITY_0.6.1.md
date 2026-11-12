# Compatibility check: CHEPTA 0.6.1 against the ethanol benchmark

Date: 2026-11-12. Status: draft engineering evidence; no human review is recorded. Not a validation against experiment.

## Verdict

**Identical.** The six reactor runs were accepted by `chepta@0.6.1`, converged, and gave the same numbers, the same
warnings and the same parameter sets as `chepta@0.6.0`, to the last stored digit. Nothing is changed, newly refused or
newly accepted for this case. The independent calculation (`verify.py`) passes with the same errors.

What this does not show: one reactor type, one property method (Peng-Robinson), one case. Matching numbers mean the
engine did not change *here*; they say nothing about agreement with experiment.

## How it was run

- `chepta@0.6.1` from npm (integrity `sha512-hB6c1spJtKTqa0wJFGiQGm1cWRTrPZhWCbw+rB3lV7FYLvTNNfRRE91nOTZ2ZGvqt3t13w15vvKQe1wIlWcaMw==`, from `package-lock.json`), Node v22.23.4, npm 10.9.9.
- Command per run: `npx chepta request <request file>`; exit code 0 for all six.
- The six requests are **byte-identical** to the 0.6.0 ones (manifest: `request_changed_from_0.6.0: false`).
- New files: `results-chepta-0.6.1/` (requests, outputs, empty stderr, `run-manifest.json`, `comparison.json`,
  `verification.json`), `run_chepta_0.6.1.py`, `compare_chepta_0.6.1.py`. `results/` (commit `c1adf6b`) and
  `results-chepta-0.6.0/` are untouched. `verify.py` ran with `results-chepta-0.6.1` as its argument (SciPy 1.17.0, as before).

## Identical

| Run | Outcome 0.6.0 / 0.6.1 | Conversion (%) 0.6.0 = 0.6.1 | Duty (kW) 0.6.0 = 0.6.1 | Other differing values | Independent-check max relative error 0.6.0 = 0.6.1 |
|---|---|---:|---:|---:|---|
| upstream_simplified-wf0.38 | ok / ok | 0.337102 | 1.515985e-05 | 0 | 9.81e-08 |
| upstream_simplified-wf0.773 | ok / ok | 0.685136 | 3.079516e-05 | 0 | 2.5e-07 |
| upstream_simplified-wf1.166 | ok / ok | 1.032557 | 4.638658e-05 | 0 | 3.61e-07 |
| table12_adsorption-wf0.38 | ok / ok | 0.331163 | 1.504470e-05 | 0 | 2.35e-06 |
| table12_adsorption-wf0.773 | ok / ok | 0.661353 | 3.033289e-05 | 0 | 2.74e-06 |
| table12_adsorption-wf1.166 | ok / ok | 0.980123 | 4.536510e-05 | 0 | 3.07e-06 |

`comparison.json` compares every leaf value of each output pair (the run id and library label excepted): 0 differences in all
six. The seven warnings per run (five "No PR k_ij", the Ethanol + Water range warning at 573.15 K, and the polar-liquid
method advice) are word for word the same as in 0.6.0: 0 added, 0 removed. The `databank_hash` is the same
(`852b926c89fa84fa`) and so is the `input_hash`; only `reproduction.library` reads 0.6.1.

## Changed

Nothing in the outputs. (The `run` block, the run id and timings differ by nature.)

## Newly refused / newly accepted

None. No capability was exercised that 0.6.0 had refused: this case does not use columns, purity specifications or
acetic acid.

## Unchanged and unresolved

The 573 K range warning for ethanol + water, missing binary parameters, the source pressure-unit conventions, no
experimental data, and the missing human review (see `README.md` and `record.json`).
