# Benzene + toluene column (The ChemSep Book, CHEPTA's B2 record) on chepta@0.6.0

| In one look | |
|---|---|
| Source | The ChemSep Book (Kooijman & Taylor, 2nd ed.), as transcribed in CHEPTA's validation record B2 |
| Simulated | one 10-stage distillation column, benzene + toluene |
| Complete flowsheet | no: a column example, not a plant |
| CHEPTA version | `chepta@0.6.0` |
| Agreement | within 0.80 K and 0.018 mole fraction of the book's profile (limits 1 K, 0.02) |
| Refused | a distillate purity specification (comes in CHEPTA 0.6.1) |
| Reviewed by a person | no; the book itself not yet opened by Lab |

Draft, 2026-11-11. Not reviewed by a person. Study record: [study-record.json](study-record.json).

## What was run

CHEPTA's own validation record of the worked example of *The ChemSep Book* (Kooijman and Taylor, 2nd ed., 2006,
§§1.2–1.3) was copied unchanged from CHEPTA v0.6.0 to [upstream/](upstream/). Lab built three requests from it
([run_chepta_0.6.0.py](run_chepta_0.6.0.py)) and ran them through the command line `npx chepta request` of the pinned
package `chepta@0.6.0`.

| | Value | Where it comes from |
|---|---|---|
| Column | 10 stages (1 = total condenser, 10 = partial reboiler), feed on stage 5, 1.1 atm = 111.4575 kPa, no pressure drop | the book, pp. 11, 14–16, as transcribed by CHEPTA |
| Feed | 11.7471 mol/s, equimolar, saturated liquid | p. 14, as transcribed |
| Specifications | reflux ratio 2; bottoms 5.874 mol/s | p. 17, as transcribed |
| Capacity | kept as in the book: mol/s × 3.6 = kmol/h (feed 42.29 kmol/h, bottoms 21.1464 kmol/h) | Lab's conversion, in the runner |
| Property method | Peng-Robinson with the benzene + toluene k_ij fitted by CHEPTA (Li et al. 2014), energy balances on every stage | CHEPTA's record |
| Property method of the book | UNIFAC with ChemSep's Antoine equations, **constant molar overflow** | p. 13, as transcribed |

**The book has not been opened by Lab.** Every published number here is CHEPTA's transcription. The direct check
against the book is **pending, for the maintainer**.

## Results ([results-chepta-0.6.0/](results-chepta-0.6.0/), checks in [checks.json](results-chepta-0.6.0/checks.json))

| Run | What it asks | CHEPTA's answer |
|---|---|---|
| `b2-pr` | the column as in CHEPTA's record and test | **ok**, converged in 2 iterations, no warning |
| `b2-record-thermo-literal` | the same, with the record's `thermo` block copied as written (`sets: "default"`) | **invalid_input** (exit 2): `sets: "0" is not a pair` |
| `b2-distillate-purity` | intentional: a benzene distillate purity (the published x_D) in place of the bottoms flow | **unsupported** (exit 4): purity specifications come with milestone M4 |

The two kinds of agreement are kept apart:

| Check | Compared with | Largest difference | Limit | Verdict |
|---|---|---|---|---|
| Same equations | CHEPTA's stored independent solution (`reference_mesh.py`, same method) | T: about 1e-12 K; x: about 1e-14 | 1e-5 K; 1e-7 | agrees (numerical round-off) |
| Published profile: stage temperatures | the book, Figure 1.19 | 0.80 K (stage 8) | 1 K | within the limit |
| Published profile: benzene mole fraction (stages, x_D, x_B) | the book, Figures 1.20–1.21 | 0.018 (stage 8) | 0.02 | within the limit, close to it |
| Balances (Lab's own) | component balances overall and on every stage; overall energy balance | about 1e-13 kmol/h; about 1e-13 kW | 1e-8 of the feed | closed |

Shown, not compared (the book assumed constant molar overflow, CHEPTA solves energy balances): boil-up ratio 2.80
against 2.99954 published; distillate and bottoms flows equal to the book's (they are specifications).

Limits from CHEPTA's record itself (1 K, 0.02 absolute mole fraction). They measure **agreement between two property
methods, not accuracy against measurements**, and CHEPTA's record says they were chosen "for the maintainer to
confirm". The Lab result (0.80 K, 0.018) is the same as CHEPTA's own record states.

## What agreed, what did not

- Agreed: CHEPTA's command line reproduces CHEPTA's own reference solution to round-off; the profile is within the
  record's limits of the book's; balances close; no warning.
- Did not run: a direct purity specification (refused as not built, expected).
- Friction found: CHEPTA's own record cannot be passed as written; the message points at `"0"` (the first letter of
  `"default"`), not at the key `sets`.

## Candidate capability requests

| # | Request | CHEPTA's outcome and message |
|---|---|---|
| 1 | Direct purity (and recovery) specifications on a rigorous column | `unsupported`, `NOT_AVAILABLE`: "Column C1: purity specifications come with milestone M4 of proposal 0015; give flows, ratios or duties instead." (already in work, M4) |
| 2 | A clearer message when `thermo.sets` is a string (or accept `"default"` as in CHEPTA's own records) | `invalid_input`, `BAD_INPUT`: "sets: \"0\" is not a pair; write it as \"component+component\", e.g. \"acetone+chloroform\"." (minor) |

## What the maintainer must check and decide

- Check the transcribed set-up and Figures 1.19–1.21 against the book, and its public-domain statement (p. 2).
- Confirm the agreement limits (1 K, 0.02). Recommendation: keep them; the result sits just inside, so any change in
  CHEPTA that moves the column further is seen.

Reproduce (repository root, after `npm ci`): `python3 cases/benzene-toluene-chemsep-b2/run_chepta_0.6.0.py`, then
`python3 cases/benzene-toluene-chemsep-b2/check_b2.py`. Re-running writes new files and changes the hashes in the
study record (run ids and times differ); keep the committed results.
