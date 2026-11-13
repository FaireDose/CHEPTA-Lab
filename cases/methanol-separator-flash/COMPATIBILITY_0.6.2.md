# Compatibility check: CHEPTA 0.6.2 against the methanol separator flash

Date: 2026-11-13. Status: draft engineering evidence; no human review is recorded. A regression of CHEPTA against its own earlier result at an illustrative state, not a paper case and not a validation.

## Verdict

**PASSES (same numbers, same warnings, same refusal).** The two converged runs give the same flash results as on 0.6.1 and still match the
decision file's table within its printed digits; SRK + gE (MHV1) is still refused with the same code and message. One difference: the plain-PR
run now lists one extrapolation in `value.extrapolations` (details below). Lab's balance checks pass.

## How it was run

`chepta@0.6.2` (npm, integrity in `package-lock.json`), default options; `npx chepta request <file>`; requests built by `run_chepta_0.6.2.py`
(the 0.6.1 script with the version changed, nothing else); checks by `check_flash_0.6.2.py` (the 0.6.1 checker pointed at the new folder); `compare_chepta_0.6.2.py` against the 0.6.1 outputs.
The request files are byte-identical to the 0.6.1 ones. `results-chepta-0.6.0/` and `results-chepta-0.6.1/` are untouched.

## Identical

| Run | Outcome 0.6.1 / 0.6.2 | Flash numbers | Other values that differ |
|---|---|---|---|
| pr-mhv1 | ok / ok | identical (liquid fraction 0.2505) | only a new empty `value.extrapolations: []`; same warnings, same four fit-quality warnings |
| pr-kij | ok / ok | identical (liquid fraction 0.2534) | only the new `value.extrapolations` (one entry); same seven stream warnings |
| srk-mhv1 | unsupported / unsupported | no result, as before | nothing (message and code identical, exit 4) |

Regression against the decision file's table (half a unit of the last printed digit), the "3.2 times more H2" ratio, the pairs without
parameters, and the component and energy balances all pass (`results-chepta-0.6.2/checks.json`).

## Extrapolations and estimated pairs (every run)

- **pr-mhv1**: `extrapolations` = [] (empty); `estimated_pairs`: none.
- **pr-kij**: one extrapolation: Hydrogen + Carbon monoxide, PR k_ij set at 313 K is 224.8 K above its range (68.2-88.2 K); the set's temperature dependence is used as it is. "An extrapolation, not data." It is in `value.extrapolations` only; the stream warning list is unchanged (the same fact was already in Lab's notes on 0.6.0/0.6.1 from the pair's source range). `estimated_pairs`: none.
- **srk-mhv1**: refused, no result; none.

No run used an estimated (predicted) pair. The three gas + gas pairs in the MHV1 run still have g^E = 0 and the CO2 + water pair is still not
covered by SRK + gE (MHV1): the refusal is **not** removed by the new Modified UNIFAC 2.0 estimation (`missingPairs` was left at the default; Lab did not try `"refuse"` or `"ideal"`).

## Changed / newly refused / newly accepted

Changed numbers: none. Newly refused: none. Newly accepted: none. No run was refused on 0.6.1 for a range or a missing pair that 0.6.2 now accepts
(the SRK refusal remains), so no strict-mode repeat was needed; not tried, effect unknown.

## Unchanged and unresolved

The state is CHEPTA's illustration, not the methanol paper's; no measured equilibrium is used; the source ids attached to four pairs (naming artefact claimed by CHEPTA's coordinator) are unverified;
the fit-quality figures are CHEPTA's own, quoted, not checked by Lab.
