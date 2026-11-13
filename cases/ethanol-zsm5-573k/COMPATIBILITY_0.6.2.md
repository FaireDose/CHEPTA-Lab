# Compatibility check: CHEPTA 0.6.2 against the ethanol benchmark

Date: 2026-11-13. Status: draft engineering evidence; no human review is recorded. Not a validation against experiment.

## Verdict

**PASSES.** Same agreement as before, limits unchanged: all six reactor runs are accepted, converge, and give the same
numbers as 0.6.1 (and 0.6.0) to the last stored digit; the independent calculation (`verify.py`) passes with the same errors.
What is new is information only: 0.6.2 now **lists three extrapolations** in `value.extrapolations` and adds two warnings
about them. Nothing is newly refused or newly accepted.

## How it was run

- `chepta@0.6.2` from npm (integrity `sha512-yXI+yL84uXDfeUo7KBn7zbyb+acCzipXA9aSvDQijoKrCGyCyDOZ8o9Ym0XV/uFBMDITk/78mn6e9ubjKN0vMw==`, in `package-lock.json`), default options.
- `npx chepta request <request file>` per run; exit code 0 for all six. The six requests are **byte-identical** to the 0.6.1 (and 0.6.0) ones.
- New files: `results-chepta-0.6.2/` (requests, outputs, stderr, `run-manifest.json`, `comparison.json`, `verification.json`),
  `run_chepta_0.6.2.py`, `compare_chepta_0.6.2.py`. `results/`, `results-chepta-0.6.0/` and `results-chepta-0.6.1/` are untouched.
  `verify.py` ran with `results-chepta-0.6.2` as its argument (SciPy 1.17.0, NumPy 2.3.5 as pinned in `requirements-reference.txt`).

## Identical

| Run | Outcome 0.6.1 / 0.6.2 | Conversion (%) | Duty (kW) | Independent-check max relative error |
|---|---|---:|---:|---|
| upstream_simplified-wf0.38 | ok / ok | 0.337102 | 1.515985e-05 | 9.81e-08 |
| upstream_simplified-wf0.773 | ok / ok | 0.685136 | 3.079516e-05 | 2.5e-07 |
| upstream_simplified-wf1.166 | ok / ok | 1.032557 | 4.638658e-05 | 3.61e-07 |
| table12_adsorption-wf0.38 | ok / ok | 0.331163 | 1.504470e-05 | 2.35e-06 |
| table12_adsorption-wf0.773 | ok / ok | 0.661353 | 3.033289e-05 | 2.74e-06 |
| table12_adsorption-wf1.166 | ok / ok | 0.980123 | 4.536510e-05 | 3.07e-06 |

Numbers are the same before and after (`comparison.json`, every leaf value compared exactly). The only differences in each
output are three: the new `value.extrapolations` list, and the `warnings` lists of the two streams (two warnings added, none removed).

## Extrapolations and estimated pairs (every run)

All six runs list the **same three extrapolations** (`result.extrapolations`, i.e. `value.extrapolations`), each "an extrapolation, not data":

1. Ethylene, ideal-gas heat capacity at 573.15 K is 123.15 K above its range (103.99-450 K); the record's own Aly-Lee equation is evaluated beyond its range.
2. Diethyl ether, ideal-gas heat capacity at 573.15 K is 25.15 K above its range (270-548 K); same.
3. Ethanol + Water, PR k_ij set at 573.15 K is 204.97 K above its range (351.26-368.18 K); the set's temperature dependence is used as it is.

Item 3 was already a warning on 0.6.0 and 0.6.1; items 1 and 2 are new warnings (they were silent before). The numbers did not change, so
0.6.1 used the same extrapolated values without saying so. **Estimated pairs (`estimated_pairs`): none, in any of the six runs** (the field is absent).
The five missing PR k_ij pairs stay at k_ij = 0 with the old warning "a prediction without binary data"; 0.6.2's estimation from Modified UNIFAC 2.0
applies to NRTL/UNIQUAC/Wilson pairs, and this case uses Peng-Robinson.

## Changed / newly refused / newly accepted

Changed numbers: none. Newly refused: none. Newly accepted: none. Because no run was refused on 0.6.1, no run was repeated with
`strictRanges` or `missingPairs: "refuse"` (Lab did not try strict mode here; whether it would refuse the three extrapolations is **unknown**).

## Unchanged and unresolved

The 573 K range limits of ethanol + water, missing binary parameters, the source pressure-unit conventions, no experimental data,
and the missing human review (see `README.md` and `record.json`).
