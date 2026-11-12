# Compatibility check: CHEPTA 0.6.1 against the methanol separator flash

Date: 2026-11-12. Status: draft engineering evidence; no human review is recorded. A regression of CHEPTA against its own earlier result at an illustrative state, not a paper case and not a validation.

## Verdict

**Same numbers, richer warnings, same refusal.** All three runs gave the outcome they gave on 0.6.0. The two converged runs
(PR + gE (MHV1), plain PR) have the same flash results to the last stored digit and still match the decision file's table
within its printed digits. What changed is information, not numbers: the MHV1 run now carries the fit-quality warnings
Lab asked for, and the pair warning now names its pair. SRK + gE (MHV1) is still refused, as expected. Lab's own balance
checks pass.

## How it was run

`chepta@0.6.1` (npm, integrity in `package-lock.json`), Node v22.23.4, npm 10.9.9; `npx chepta request <file>` per run;
requests built by `run_chepta_0.6.1.py` from `case-input.json` (the 0.6.0 script with the version changed, nothing else); checks by
`check_flash_0.6.1.py` (the 0.6.0 checker pointed at the new folder). The request files are byte-identical to the 0.6.0 ones.
`results-chepta-0.6.0/` is untouched.

## Identical

| Run | Outcome 0.6.0 / 0.6.1 | Flash numbers | Other values that differ |
|---|---|---|---|
| pr-mhv1 | ok / ok | identical (liquid fraction 0.2505, same x to the last stored digit) | the warnings and quality notes below; `databank_hash` and library label |
| pr-kij | ok / ok | identical (liquid fraction 0.2534) | only the library label (0.6.0 to 0.6.1); same warnings, same pair list |
| srk-mhv1 | unsupported / unsupported | no result, as before | only the library label and the message text below |

Regression against the decision file's table: pr-kij and pr-mhv1 pass at the same tolerance as on 0.6.0 (half a unit of the
last printed digit); the "3.2 times more H2 in the liquid" ratio passes; the pairs without parameters are as the file states;
component and energy balances close (checks in `results-chepta-0.6.1/checks.json`).

## Changed (CHEPTA's answers to Lab's requests from the 0.6.0 run)

| Lab request | 0.6.0 | 0.6.1 |
|---|---|---|
| Carry each MHV1 set's fit-quality known issue in the result that uses it | no flag in the MHV1 run | **done**: four `Fit quality of the MHV1 set for ...` warnings on every stream (CO2 + methanol, CO2 + water, H2 + methanol, CO + water) and a `quality_warning` field on those four pairs in `qualifications.pairs`. They are the four pairs the plain-PR advice already named. Example: CO2 + water "AAD 11.4 % in P (max 60.6 %), 7.9 % in the gas solubility, 4 of 573 points without a bubble pressure, 6.4 points over the gate of 5 %". |
| Name the pair in "an NRTL set of the databank (fitted at low pressure), used inside the MHV1 rule" | warning without the pair | **done**: "Methanol + Water: an NRTL set of the databank (fitted at low pressure), used inside the MHV1 rule" |
| Check the source ids attached to CO2 + water, H2 + methanol, CO + methanol, methanol + water | `pokki2018-furfural-gvl` and `schuler2012-carbon-dioxide-methanol` listed under CO2 + water; `wu2019-carbon-dioxide-methanol` under H2 + methanol and CO + methanol; two `zhang2019-2-propanol-...` ids under methanol + water | **no change in the output**: the same ids appear. CHEPTA's coordinator has said they are a naming artefact and the data are right (HANDOVER); Lab has not verified that against the articles. Left open. |
| SRK + gE (MHV1) for CO2 + water | `unsupported`, `NOT_AVAILABLE` | **still `unsupported`, `NOT_AVAILABLE`** (exit 4). The message now also lists the pairs fitted so far and says to give the pair's parameters in `mixing.nrtl`, or use SRK with its k_ij. Lab did not try supplying parameters. |

Also changed: `databank_hash` of the MHV1 run `cc2386f26b9cdea3` to `dd211d35a9d924dd` (the databank changed; Lab did not
investigate what, and the flash numbers did not change). The warning list of the MHV1 run is 4 longer: the four fit-quality warnings were added, and
the unnamed databank warning was replaced by the named one (5 added, 1 removed in all).

## Newly refused / newly accepted

Newly refused: none. Newly accepted: none. Not applicable to this flash: purity and recovery specifications, side draws and
acetic acid (columns only); measured VLE points were not looked for here (no measured data at this state is used).

## Unchanged and unresolved

The state is CHEPTA's illustration, not the methanol paper's (its supplement is not audited); no measured equilibrium is
used; the three gas + gas pairs still have g^E = 0; the fit-quality figures are CHEPTA's own, quoted, not checked by Lab.
