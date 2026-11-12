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
