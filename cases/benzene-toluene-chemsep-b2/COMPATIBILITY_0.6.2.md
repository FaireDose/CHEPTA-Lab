# Compatibility check: CHEPTA 0.6.2 against the B2 benzene + toluene column

Date: 2026-11-13. Status: draft engineering evidence; no human review is recorded. The book itself has not been opened by Lab; published numbers are CHEPTA's transcription.

## Verdict

**PASSES (same agreement as on 0.6.1, limits unchanged).** The six runs gave the same outcome and the same numbers as on 0.6.1:
`b2-pr` is within 0.80 K and 0.018 mole fraction of the book (limits 1 K and 0.02, from CHEPTA's record, unconfirmed by the maintainer, **not loosened**);
the purity- and recovery-specified columns are, as on 0.6.1, **still not within those limits** (listed below). Nothing is newly refused or newly accepted.

## How it was run

`chepta@0.6.2` (npm, integrity in `package-lock.json`), default options; `npx chepta request <file>`; `run_chepta_0.6.2.py`; checks by
`check_b2_0.6.2.py` (reads files only, same limits and same checks as for 0.6.1); `compare_chepta_0.6.2.py` against the 0.6.1 outputs.
All six requests are the 0.6.1 request files byte for byte. The CHEPTA record (`upstream/`) is still the copy from tag v0.6.0; not re-copied.
`results-chepta-0.6.0/` and `results-chepta-0.6.1/` are untouched.

## Identical

Every leaf value of every output equals the 0.6.1 output, except the run block and the library label, and (in five of six) one solver-timing
text (for example "2 iterations, 96 ms" to "2 iterations, 93 ms"). Outcome ok / ok in all six. Balances close (Lab's check passes); same-equation
check against CHEPTA's stored reference solution unchanged for `b2-pr` and `b2-record-thermo-literal`.

| Run | Specification | Largest T difference from the book (limit 1 K) | Largest x difference from the book (limit 0.02) |
|---|---|---|---|
| `b2-pr` | reflux 2, B = 5.874 mol/s | 0.80 K: within | 0.018: within |
| `b2-record-thermo-literal` | same, record's thermo block literally | 0.80 K: within | 0.018: within |
| `b2-distillate-purity` | old `distillate_purity` key, reflux 2 | **2.82 K: outside** | **0.073: outside** |
| `b2-purity-spec` | benzene in distillate 0.925473 | **2.82 K: outside** | **0.073: outside** |
| `b2-bottoms-purity-spec` | toluene in bottoms 0.925408 | 0.27 K: within | **0.026: outside** |
| `b2-recovery-spec` | benzene recovery 0.925403 | 0.22 K: within | **0.024: outside** |

(The reading of these numbers is in `COMPATIBILITY_0.6.1.md`: the purity runs test the specification feature; they are not a reproduction of the book's column. Not repeated here, not changed.)

## Extrapolations and estimated pairs (every run)

`result.extrapolations`: **not present in any of the six column outputs** (the field does not appear; the flowsheet runs of the other two cases do carry it).
So Lab cannot say from these files whether the column path checks property ranges at all; it is **unknown**. The runs carry no warning.
`estimated_pairs` / `info.estimatedPairs`: **none**; the one pair (benzene + toluene) is still qualified "fitted" (set fitted-li2014), not estimated.
No run used a predicted pair or a reported extrapolation.

## Changed / newly refused / newly accepted

Changed numbers: none. Newly refused: none. Newly accepted: none. No run was refused on 0.6.1, so none was repeated with `strictRanges` or
`missingPairs: "refuse"` (not tried; whether strict mode changes anything here is unknown).

## Unchanged and unresolved

The book not opened by Lab; the limits not confirmed (they still sit just around the 0.6.0 result and were chosen for the constant-molar-overflow
difference); rights statement (p. 2) not checked; no measured data.
