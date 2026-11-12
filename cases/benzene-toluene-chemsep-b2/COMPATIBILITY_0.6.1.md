# Compatibility check: CHEPTA 0.6.1 against the B2 benzene + toluene column

Date: 2026-11-12. Status: draft engineering evidence; no human review is recorded. The book itself has not been opened by Lab; published numbers are CHEPTA's transcription.

## Verdict

**The 0.6.0 column is identical; two 0.6.0 refusals are now accepted; the purity specification now runs, but the columns it
builds do not agree with the book within the unchanged limits.** Limits (1 K and 0.02 mole fraction, from CHEPTA's
record, to be confirmed by the maintainer) were not loosened.

## How it was run

`chepta@0.6.1` (npm, integrity in `package-lock.json`), Node v22.23.4; `npx chepta request <file>`; `run_chepta_0.6.1.py`;
checks by `check_b2_0.6.1.py` (reads files only). Three requests are the 0.6.0 request files byte for byte; three are new.
The CHEPTA record (`upstream/`) is still the copy from tag v0.6.0; it was not re-copied from a 0.6.1 tag (not reachable from this session).
`results-chepta-0.6.0/` is untouched.

## Identical

`b2-pr` (reflux ratio 2, bottoms 5.874 mol/s): same outcome, same numbers. Only one leaf value of the output differs, a
solver timing text (101 ms to 96 ms); library label 0.6.0 to 0.6.1; databank hash unchanged (`39600609f82335b2`). Still ok, converged in 2
iterations, no warning; still 0.80 K (stage 8) and 0.018 (stage 8) from the book (limits 1 K, 0.02); same-equation check against CHEPTA's stored
reference solution unchanged; balances close.

## Newly accepted (0.6.0 refused them)

| Run | 0.6.0 | 0.6.1 |
|---|---|---|
| `b2-record-thermo-literal` (the record's thermo block as written, `sets: "default"`) | `invalid_input`: `sets: "0" is not a pair` | **ok**; same numbers as `b2-pr` exactly (0.80 K, 0.018). Lab's request about the unclear message is resolved by accepting it. |
| `b2-distillate-purity` (the 0.6.0 request, byte for byte: `column.distillate_purity {component, value}` and reflux ratio 2) | `unsupported`, `NOT_AVAILABLE` (purity is milestone M4) | **ok**: benzene distillate purity 0.925473 asked, 0.925473 observed (CHEPTA's design residual 5e-9). The old key is honoured. |

## The purity and recovery specifications (new runs, reflux ratio 2 kept, bottoms flow left to CHEPTA)

All values are CHEPTA's published-number inputs from the record; nothing typed. Observed from the profile by `check_b2_0.6.1.py`.

| Run | Specification asked | Reached | D / B (mol/s) | Boil-up ratio | Largest T difference from the book (limit 1 K) | Largest x difference from the book (limit 0.02) |
|---|---|---|---|---|---|---|
| `b2-pr` (0.6.0 specification) | reflux 2, B = 5.874 | (flows given) | 5.8731 / 5.8740 | 2.804 | 0.80 K (stage 8): within | 0.018 (stage 8): within |
| `b2-purity-spec` | benzene in distillate 0.925473 | 0.925473 | 5.5816 / 6.1655 | 2.536 | **2.82 K (stage 8): outside** | **0.073 (stage 8): outside** |
| `b2-bottoms-purity-spec` | toluene in bottoms 0.925408 | 0.925408 | 5.9872 / 5.7599 | 2.918 | 0.27 K (stage 3): within | **0.026 (stage 3): outside** |
| `b2-recovery-spec` | benzene recovery in distillate 0.925403 | 0.925403 | 5.9726 / 5.7745 | 2.903 | 0.22 K (stage 3): within | **0.024 (stage 3): outside** |

The book: D 5.8731, B 5.874, boil-up ratio 2.99954 (constant molar overflow; shown, not compared).

**Reading, honestly.** The specifications are met and balances close (checked by Lab). But the book's column has reflux 2 *and*
x_D = 0.9255 *and* D = 5.8731; CHEPTA's energy-balance column at reflux 2 and the same D reaches x_D = 0.9150 (that is the 0.018 difference
already seen on 0.6.0). Asking CHEPTA for the book's purity at reflux 2 therefore moves D to 5.58 mol/s and the profile away from the
book's by more than the limit. This is the difference between two property methods (and constant molar overflow), not shown to be a CHEPTA
defect, and the purity runs are **not a reproduction of the book's column**; they test the new specification feature only.
Convergence and met specifications do not establish physical accuracy. No limit was changed.

## Changed

Nothing in the `b2-pr` numbers. The refused runs above became accepted.

## Newly refused

None.

## Capability requests

None needed for this case. Open question for the maintainer: the limits (1 K, 0.02) still sit just around the 0.6.0 result;
they were chosen for the constant-molar-overflow difference and do not judge purity-specified columns.

## Unchanged and unresolved

The book not opened by Lab; the limits not confirmed; rights statement (p. 2) not checked; no measured data.
