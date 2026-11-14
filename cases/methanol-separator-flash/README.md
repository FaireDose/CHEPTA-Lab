# Methanol-loop separator flash: PR + gE (MHV1) against PR with k_ij, on chepta@0.6.0

| In one look | |
|---|---|
| Source | none: an example state from CHEPTA's own decision file, not a paper |
| Simulated | one high-pressure flash drum (CO2, H2, CO, methanol, water at 313 K, 5 MPa) with two methods |
| Complete flowsheet | no |
| CHEPTA version | `chepta@0.6.0` |
| Agreement | same numbers as CHEPTA's earlier result (a check that nothing changed, not a validation) |
| Refused | SRK + gE (MHV1) |
| Reviewed by a person | no |

Draft, 2026-11-11. Not reviewed by a person. Study record: [study-record.json](study-record.json).

## What was run

The high-pressure separator after a CO2-to-methanol reactor, as **one flash at an illustrative state taken from
CHEPTA's own decision file** [2026-11-06-02-mhv1.md](upstream/2026-11-06-02-mhv1.md) (copied unchanged from CHEPTA
v0.6.0): CO2, H2, CO, methanol, water = 0.2 / 0.5 / 0.05 / 0.15 / 0.1, 313 K, 5 MPa ([case-input.json](case-input.json);
100 kmol/h is Lab's basis). **It is not a reproduction of the methanol paper**: its supplement is not audited and no
paper condition is used.

Three requests through `npx chepta request` ([run_chepta_0.6.0.py](run_chepta_0.6.0.py)): feed → isothermal flash at
313 K and 5000 kPa → vapour and liquid.

## Results ([results-chepta-0.6.0/](results-chepta-0.6.0/), checks in [checks.json](results-chepta-0.6.0/checks.json))

| Method | Outcome | Liquid fraction | x CO2 | x H2 | x CO | x methanol | x water |
|---|---|---|---|---|---|---|---|
| PR + gE (MHV1) | ok | 0.2505 | 0.0247 | 0.00368 | 0.00056 | 0.5756 | 0.3955 |
| PR with k_ij | ok | 0.2534 | 0.0333 | 0.00115 | 0.00023 | 0.5736 | 0.3917 |
| SRK + gE (MHV1) | **unsupported** (exit 4) | – | – | – | – | – | – |

(Rounded here to the decision file's digits; the full numbers are in the output files.)

| Check | Verdict |
|---|---|
| Regression: both converged runs against the decision file's table (CHEPTA's own earlier result) | **same to every printed digit**; H2 in the liquid 3.2 times higher with MHV1, as the file says |
| Pairs without parameters | as the file says: MHV1: CO2 + H2, CO2 + CO, H2 + CO (gas + gas, g^E = 0); PR: CO2 + CO, H2 + methanol, H2 + water, CO + water (k_ij = 0) |
| Balances (Lab's own: components, energy) | closed (about 1e-14 kmol/h; 0 kW) |
| SRK + gE (MHV1) refused for CO2 + water | as the file says |

This is a **regression check of CHEPTA against itself**, not validation: no measured data at this state is used.

## Method qualifications and warnings, kept

| Method | What the run says |
|---|---|
| PR + gE (MHV1) | 7 pairs fitted inside the rule or from the databank; 3 gas + gas pairs without parameters (g^E = 0), one warning each; one warning "an NRTL set of the databank (fitted at low pressure), used inside the MHV1 rule" that does not name the pair (it is methanol + water) |
| PR with k_ij | 4 pairs with k_ij = 0; H2 + CO k_ij from data at 68–88 K used at 313 K; advice: "Above 10 bar, PR + gE (MHV1) is recommended", naming four MHV1 sets "with a fit-quality warning" |
| SRK + gE (MHV1) | refused: "Carbon dioxide + Water, a light gas with a polar liquid, has no NRTL parameters fitted inside the rule ... and none in the databank" |

**Found:** the fit-quality known issues of the four MHV1 sets (CO2 + methanol, CO2 + water, H2 + methanol, CO + water)
appear only in the *plain-PR* run's advice. The MHV1 run that uses them carries no such flag; their fit errors are
only inside each pair's source text (for example CO2 + water: 11.4 % in P). Also, some source ids attached to a pair
name another system (CO2 + water lists `pokki2018-furfural-gvl`; methanol + water lists two `zhang2019-2-propanol-...`
ids). These may be correct article ids; for CHEPTA to confirm.

## Candidate capability requests

| # | Request | CHEPTA's outcome and message |
|---|---|---|
| 1 | Carry each MHV1 set's fit-quality known issue as a warning or qualification in the result that uses it | `ok`, no flag in the MHV1 run (the plain-PR run's advice: "fitted inside the rule, with a fit-quality warning") |
| 2 | Name the pair in "an NRTL set of the databank (fitted at low pressure), used inside the MHV1 rule" | `ok`, warning without the pair |
| 3 | SRK + gE (MHV1) for CO2 + water (only if SRK is wanted; PR + gE (MHV1) already covers the separator) | `unsupported`, `NOT_AVAILABLE`: "SRK + gE (MHV1): Carbon dioxide + Water, a light gas with a polar liquid, has no NRTL parameters fitted inside the rule (src/data/mhv1.json) and none in the databank, so its solubility would rest on no data (proposal 0018). ..." |
| 4 | Check the source ids attached to CO2 + water, H2 + methanol, CO + methanol and methanol + water | `ok`; observation only |

## What the maintainer must check and decide

- Check that the state was copied correctly from the decision file (one line, case-input.json).
- Decide whether PR + gE (MHV1) is the separator method for the coming methanol case. Recommendation: yes, as CHEPTA
  decided, with request 1 so the fit-quality issues travel with the result; replace this illustrative state by the
  paper's once its supplement is audited.

Reproduce (repository root, after `npm ci`): `python3 cases/methanol-separator-flash/run_chepta_0.6.0.py`, then
`python3 cases/methanol-separator-flash/check_flash.py`. Re-running changes the result files and the hashes in the
study record; keep the committed results.

## Update 2026-11-12: chepta@0.6.1

Re-run on 0.6.1 ([COMPATIBILITY_0.6.1.md](COMPATIBILITY_0.6.1.md), [results-chepta-0.6.1/](results-chepta-0.6.1/)). Same flash numbers
and same regression result. The MHV1 run now carries the four fit-quality warnings and names the pair in the databank warning; the source ids
are unchanged; SRK + gE (MHV1) is still refused (`NOT_AVAILABLE`).

## Update 2026-11-13: H2 + CO k_ij = 0 and strictRanges, chepta@0.6.2 (draft, no human review)

CHEPTA's extrapolation warning is **kept**: in [pr-kij.output.json](results-chepta-0.6.2/pr-kij.output.json)
(`/value/extrapolations/0`) the H2 + CO PR k_ij set (fitted at 68.2–88.2 K, databank set `chemsep`) is used at 313 K,
224.8 K above its range. Per the maintainer's request, each 0.6.2 request was rerun once with that k_ij set to 0
(through `user_data`, source text "sensitivity assumption ... not data") and once with `options.strictRanges: true`.
New files beside the old ones, which are untouched: [results-chepta-0.6.2-kij0-strict/](results-chepta-0.6.2-kij0-strict/)
(runner [run_chepta_0.6.2_kij0_strict.py](run_chepta_0.6.2_kij0_strict.py); manifest `run-manifest.json`; every
difference leaf by leaf in `movement.json`). Run ids in the study record: `<method>-kij0.chepta-0.6.2`,
`<method>-strict.chepta-0.6.2`. k_ij = 0 is an assumption for this test, not a better value.

**k_ij(H2, CO) = 0** (old = `pr-kij`, new = `pr-kij-kij0`; flows in kmol/h on 100 kmol/h feed; relative = (new − old)/old):

| Quantity | Old | New | Absolute | Relative |
|---|---|---|---|---|
| Vapour flow | 74.66434 | 74.66401 | −3.3e-4 | −4.4e-6 |
| Liquid flow | 25.33566 | 25.33599 | +3.3e-4 | +1.3e-5 |
| Liquid CO flow | 5.8905e-3 | 5.8681e-3 | −2.2e-5 | **−3.8e-3** (largest) |
| Liquid H2 flow | 2.9025e-2 | 2.9023e-2 | −1.8e-6 | −6.3e-5 |
| Liquid CO2 flow | 0.84479 | 0.84502 | +2.4e-4 | +2.8e-4 |
| Vapour methanol flow | 0.46804 | 0.46793 | −1.0e-4 | −2.2e-4 |
| Vapour mole fraction CO | 0.066887 | 0.066888 | +5.9e-7 | +8.9e-6 |
| Liquid mole fraction CO | 2.3250e-4 | 2.3161e-4 | −8.9e-7 | −3.8e-3 |

All other component flows and fractions of both outlets move by less than 3e-4 relative (full list in
`movement.json`). The effect is far below the difference between the two methods (H2 in the liquid 3.2 times higher
with MHV1). **PR + gE (MHV1)** (`pr-mhv1-kij0`): outlets identical to the old run to every digit, because H2 + CO is
a gas + gas pair without an MHV1 set (g^E = 0) and the k_ij is not used; its qualification lists the pair with no set.
**SRK + gE (MHV1)** (`srk-mhv1-kij0`): still `unsupported`, `NOT_AVAILABLE`, exit 4 (CO2 + water). The `-kij0` run of
the plain-PR method reports the pair as `user` tier and no longer carries the extrapolation (the set is no longer used).

**strictRanges true**: `pr-mhv1-strict` ok, `pr-kij-strict` ok, `srk-mhv1-strict` unsupported (exit 4). In all three
the output `value`, `error` and `qualifications` are identical to the old runs. The strict mode did **not** refuse the
H2 + CO k_ij extrapolation: `pr-kij-strict` still lists the extrapolation (224.8 K above range) and returns the same
numbers. So in 0.6.2 `strictRanges` does not stop a pair set used outside its fitted temperature range in this
request (observation of three runs; the code's wording is that it refuses outside a record's range, so whether a pair
set counts as a record is a question for CHEPTA, not settled here).

Checked: the six runs executed and their outputs compared by script; balances of every ok run closed (material
≤ 1.4e-14 kmol/h, energy 0 kW, from each output's `checks`). Not checked: physical accuracy, no measured data.
Not a human review. Reproduce: `python3 cases/methanol-separator-flash/run_chepta_0.6.2_kij0_strict.py` (changes the
new result files and their hashes; keep the committed ones).
