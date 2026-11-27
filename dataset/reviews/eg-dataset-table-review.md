# Review of PR #36: ethylene glycol plant (Shehata et al. 2024), dataset-table stage

**AI full check (Claude Opus 5.5, 2026-11-27).** I am a separate AI review session, started by Lab's coordinator
(session_01FPbeWUJu4MrkqCuGX3UKYB). I did not build this case and I changed none of its files. This is not a person's
check. The person's spot check (end of this note) is still to do, and only the maintainer records it.

Reviewed: branch `claude/lab-eg-shehata` at commit `efdf39a`: `cases/ethylene-glycol-shehata-2024/` (streams.json,
equipment.json, audit_balances.py, balance-results.json, STREAM_AUDIT.md, record.json, README.md, DATASET_TABLE.md),
`dataset/records/ethylene-glycol-shehata-2024.json` (13 decision rows, 4 evidence rows, 7 blocks), the 4 new rows in
`data/ISSUES_AND_ROUTES.md`, `data/sources.json`, the regenerated index and the test change. No CHEPTA run was made in
the PR and none was made in this review.

**Result:** 2 major, 8 minor, 7 nits. Table 3 and the Fig. 5 labels are transcribed without error, and the balance audit
reproduces. The two major findings both concern the inputs of the first run. They do not affect the dataset table's
numbers.

## What was checked, and how

- **Source.** I downloaded the publisher PDF (https://www.nature.com/articles/s41598-024-77713-y.pdf) into
  `raw_papers/eg-review-dl/` (git-ignored, not committed). Its sha256 is `8bf58295…eb86e551`, the same as the
  builder's. Text came from `pdftotext -layout`. Fig. 5 is the embedded page-10 image (1985 x 1030 px, extracted with
  `pdfimages`); I read it whole and zoomed in on stream 17 and the Purification Tower. I read the paper as evidence only.
- **Table 3 (p.10), all 14 streams.** I checked every printed mass flow, molar flow and all 8 mole fractions
  against `streams.json` with a script: no differences (14/14). The as-printed strings ("1.10e+004", "22,270", "0.0" for
  stream 10) are kept.
- **Fig. 5 (p.10), T and P of all 30 streams.** All agree with the image, asterisks included. 17 is 156.5 C (zoomed);
  the figure misspells "MEG To Storge".
- **Connections on Fig. 5.** These are all as the builder reads them. The MEG product leaves the Purification Tower's condenser (a
  distillate; the zoom shows no side draw), DEG+TEG leaves the reboiler, and the energy streams attach as
  `equipment.json` says.
- **Table 1 (p.3), text pp.8-9, 13-14, Table 8 (p.14).** All 15 EO-MEG energy values and every Table 1 and p.8
  setting transcribed in `equipment.json` agree with the paper.
- **Balance audit.** I recomputed the audit with my own script rather than `audit_balances.py`. I get: recycle 11 − WATER REC water +2.94, EO
  +0.05 kmol/h; MEG column water +2.61 kmol/h; evaporator and column tops by difference 810.0 / 1203.9 / 1051.9 /
  6803.7 kmol/h (component sums; the audit's 1203.0 and 6802.0 use the printed totals, and the gap is the 0.9978
  fraction sum); extents 1131.395 / 19.8 / 8.8 kmol/h; EO conversion 87.19 %; evaporators 29.80 % of stream 4's water,
  the dehydration column 70.20 %; water/EO 8.127 / 8.349 / 9.323; plant water +3.477 kmol/h (with the audit's
  stoichiometry). The DEG+TEG share of the glycol product streams is 3.52 wt %, against the audit's 3.555 wt % on the
  formed glycols, and the paper's 3.56 wt % (p.14). Reactor volume 18.48 m3. Every figure the audit gives is reproduced. Rerunning
  `audit_balances.py` leaves `git status` clean.
- **Property data.** I read the pinned engine's data to test the method's reason: the `chepta@0.6.2` npm tarball, unpacked
  into my scratchpad. I read only `src/data/components.json` and `src/data/binaries.json`.
- **Knowledge base.** I opened all 19 `informed_by` links on the 8 plan rows with `kb.py show` and compared each with its rule's
  title, when, do and check. I read the 4 paper rows, the 4 evidence rows and the 4 register rows.
- **Checks run** (on the PR branch, before adding this file):
  - `python scripts/validate_catalog.py`: exit 0, "Catalogue OK: 41 sources, 8 candidate families; 0 accepted training
    examples."
  - `python scripts/dataset_pipeline.py validate`: exit 0, `"valid": true` (groups 2, blocks 37, evidence 35,
    decisions 319, runs 1, tasks 3).
  - `python -m unittest discover -s tests`: 127 tests, OK.
  - `python scripts/kb.py check`: exit 0, `{"rows_by_kind": {"case-decision": 158, "design-rule": 127,
    "simulation-rule": 34}, "disputed_sets": 2, "index": "current"}`.

## The builder's nine text/table disagreements

| # | Item | Real? | Note |
|---|---|---|---|
| 1 | Feed heater 4.446 MW (p.8) vs 44,462.57 kW (Table 8) | yes | p.8 names E-105 and E-100 together "with a duty of 4.446 MW" |
| 2 | Evaporators remove 75 % (p.8) vs 29.8 % | yes | recomputed 29.80 %. The dehydration column takes 70.2 %, so the text's figure may belong to the column (my reading) |
| 3 | Selectivity 85/15 (Table 1) vs 98.2 % molar | yes | not 85/15 on a mass basis either (96.5 wt % MEG). p.13 says "96 wt% yield of MEG", which agrees with Table 3 (nit 2) |
| 4 | Conversion reactor (Table 1, 'C' icon) vs plug flow 77.8 m x 0.55 m (p.8) | yes | |
| 5 | 85 mm Hg = 11.33 kPa (p.8) vs 15/20 kPa | yes | 85 x 0.133322 = 11.332 kPa |
| 6 | Side stream (p.8) vs distillate (Fig. 5) | yes | confirmed on the zoomed image |
| 7 | DEG+TEG 190 C vs the 170 C limit (p.8) | yes | |
| 8 | 10:1 vs 8.13 / 8.35 / 9.32 | partly | 9.32 is within 7 % of a nominal "10:1"; a soft disagreement (nit 4) |
| 9 | "Endothermic" (p.8) vs Q-100 −32,917.29 kW | yes | strengthened by minor finding 1: the paper's own energy total counts Q-100 as negative |

The README lists one more disagreement that does not hold: Table 8 against the 323 MW total (minor finding 1). The
README missed these: what "219.258 MW for heating" contains, the abstract's 279 MW (minor finding 2), and Eq. 7's TEG
formula (nit 1).

## Major

**M1. The fresh EO feed is at its saturation point, so "149.6 C, 3534 kPa" does not fix its phase.**
- *Location:* `record.json` `fixed_inputs[0]` ("Ethylene Oxid: 1160 kmol/h, pure EO, 149.6 C, 3534 kPa");
  DATASET_TABLE.md section 1; run plan step 1.
- *What is wrong:* the fresh EO is given by T and P only. These two values sit on EO's vapour-pressure curve. CHEPTA
  could therefore start the plant with vapour EO, or with a phase that flips between runs.
- *Evidence:* Fig. 5 (p.10) prints "149.6 C" without an asterisk and "*3534 kPa" with one. On the builder's own
  reading of the asterisk (`streams.json` "asterisk"), HYSYS computed the temperature from the pressure and a second
  specification, most likely a vapour fraction (my reading). CHEPTA 0.6.2's EO vapour pressure (`components.json`,
  DIPPR101 fitted to CoolProp, maximum deviation 0.094 %) gives 3537.8 kPa at 149.6 C (derived). The stream is 0.11 %
  below that, inside the fit's own uncertainty: pure EO there is saturated. Its latent heat then decides MIX-100's
  outlet (19.65 C) and part of the energy behind the feed-heater check.
- *Suggested fix:* give the fresh EO as P = 3534 kPa with liquid fraction 1 (bubble point), and keep T = 149.6 C only as a
  comparison. Record this as Lab's reading of Fig. 5. Add the same check (phase of each specified stream) to run plan
  step 1.

**M2. The property method's reason does not hold as written, and the pinned engine has no NRTL pair for any EO
binary.**
- *Location:* `record.json` `property_method.reason`; README "Components and property method"; KB row
  `ethylene-glycol-shehata-2024.plan-property-method-nrtl` (When: "below 10 bar outside the reactor").
- *What is wrong:*
  1. "Below 10 bar outside the reactor" is false. EVA_1 flashes at 1600 kPa and 202.8 C (Fig. 5, streams 5, 7, 15).
     The feed train and both pumps run at 3450-3534 kPa.
  2. The record says the activity model's 10 bar limit "does not bear" because these blocks carry no gas. But EVA_1
     makes a vapour (810 kmol/h by difference) at 16 bar with an ideal-gas vapour model.
  3. In CHEPTA 0.6.2 `binaries.json`:
     - EO + water has only a Wilson pair (ChemSep databank, tier "databank");
     - EO + MEG and EO + DEG have no pair at all;
     - water + MEG NRTL is fitted to 101.3 kPa data (Kamihama 2012);
     - DEG + MEG NRTL is fitted to 40 kPa bubble temperatures (Yang 2014);
     - DEG + water NRTL is from the ChemSep databank.

     Under NRTL, every EO pair would therefore be estimated by Modified UNIFAC 2.0. Yet EO is what the evaporators and the
     recycle mostly carry besides water (79.8 kmol/h of EO in EVA_1's vapour; 1.73 mol % in the recycle).
  4. EO's critical temperature in CHEPTA is 468.92 K (195.77 C). EVA_1 (202.8 C), the reactor (199 C) and streams 3 and
     15 (200 C, 199.2 C) are above it. The record already flags the reactor and EVA_1 as "to check", which is right.
- *Evidence:* Fig. 5 p.10; chepta 0.6.2 `src/data/binaries.json`, `src/data/components.json` (read 2026-11-27).
- *Suggested fix:*
  - Correct the reason: the method range is 10-3534 kPa, with VLE at up to 1600 kPa above EO's critical temperature.
  - Keep NRTL if wanted, but say now that all EO pairs will be estimated. Add a Wilson variant: it has a databank EO + water pair and the
    glycol pairs, and no liquid split is expected.
  - The KB row is locked (append-only), so correct it with a new row (`keys.corrects`, `keys.correction_reason`).

  The NRTL choice itself is defensible. Its stated reason is not.

## Minor

**m1. The 323 MW total is not a disagreement: it is the signed sum of Table 8.**
- *Location:* README line 82 ("355.9 MW (positive) or 388.8 MW (absolute) against 323 MW"); STREAM_AUDIT.md "Energy";
  `audit_balances.py` lines 214 and 268; `record.json` `missing_inputs` ("the sign convention of Table 8").
- *Evidence:* the 15 EO-MEG entries of Table 8 (p.14) sum, with signs, to 322,961.68 kW, the text's "323 MW" (p.14).
  The EC-MEG entries likewise sum to 54,663.36 kW, the text's "54.7 MW" (p.14). So the paper totals Q-100 as
  −32.9 MW: heat leaving the reactor. That fits an exothermic reaction and contradicts the "endothermic" of p.8.
- *Suggested fix:* report the signed sum as matching. Reword disagreement 9 to "the paper's own total treats Q-100 as
  heat removed". Keep "sign convention not stated" only for the individual entries.

**m2. Two more text/table disagreements were missed.**
- *Location:* STREAM_AUDIT.md "Energy"; README disagreement table.
- *Evidence:*
  - (a) p.14: the water separation section "consumes 219.258 MW for heating purposes". The builder's sum that
    reproduces it includes DEH CON Q (107,392.75 kW), the column's condenser: a cooling duty. Without it the heating is
    111.87 MW (derived).
  - (b) The abstract (p.1) says the direct route uses "279 megawatts" more than the indirect. The text's totals give
    323 − 54.7 = 268.3 MW (derived from p.14).
- *Suggested fix:* add both, as kept and not fixed.

**m3. The Shehata rule `vacuum-glycol-columns` and the paper row `paper-vacuum-glycol-column` are called "worked"
although the paper's own column breaks their condition.**
- *Location:* `dataset/records/ethylene-glycol-shehata-2024.json`, row `paper-vacuum-glycol-column` (When: "without
  passing 170 C"; Status: worked, basis paper simulation). The plan rows cite `shehata-2024-meg-routes.vacuum-glycol-columns`
  with helped "yes" (dehydration) and "partly" (MEG column; the note names only the side draw).
- *Evidence:* DEG+TEG leaves at 190 C at 13 kPa (Fig. 5, p.10), above the 170 C of p.8.
- *Suggested fix:* by a new row, either reword the When (vacuum lowers the bottoms temperature, here to 190 C) or set
  the status to what the evidence shows (the paper's own column exceeds its stated limit). In the MEG-column note, say
  that the rule's 170 C is not met by the paper itself.

**m4. `chen-2018-abe-distillation.lower-pressure-of-sensitive-columns` is cited "helped: yes" twice for a rule it does
not state.**
- *Location:* `informed_by` of `plan-dehydration-column-specs` ("Lower pressure for a heat-sensitive bottoms") and
  `plan-meg-column-distillate-first` ("Pressure kept low for the 170 C limit").
- *Evidence:* the rule (`kb.py show`) is about columns "whose split improves at lower pressure", for when columns need high reflux
  and offer few heat-integration matches. It says nothing about heat-sensitive bottoms. Neither plan lowers a pressure:
  both keep the paper's.
- *Suggested fix:* in a new row (the lock forbids edits), record helped "no" with the reason "different trigger; the plan
  keeps the paper's pressure", or drop the link from the count.

**m5. `li-2017-ed-thermo-parameters.check-built-in-parameters` is used to justify a routine revalidation that
AGENTS.md rules out.**
- *Location:* `plan-property-method-nrtl` (Do: "compare the key ones (water + MEG, MEG + DEG) with measured data";
  `informed_by` li-2017, helped "yes"); `record.json` `to_check_before_the_first_run[2]`.
- *Evidence:*
  - AGENTS.md: Lab "does not routinely remeasure or revalidate phase equilibrium", and investigates data "only for a
    concrete missing parameter, range violation or material disagreement".
  - The li-2017 row's own check says the same, and its When needs a simulated behaviour the data do not show.
  - In chepta 0.6.2 both pairs are already fitted to measured data (Kamihama 2012; Yang 2014).
- *Suggested fix:* limit the data check to the pairs that are estimated (the EO pairs, TEG) or out of range. A range
  question exists for water + MEG: fitted at 101.3 kPa, used at 15-20 kPa and about 50-150 C (my reading of the fit's
  T range; to confirm from the data file). Record li-2017 as helped "no" (not triggered) in a new row.

**m6. The four register rows were added while the HANDOVER still lists them as waiting for the maintainer.**
- *Location:* `data/ISSUES_AND_ROUTES.md` (4 new rows); `docs/HANDOVER.md` line 149: "Waiting for the maintainer: …
  the 6 register problems proposed for ethylene glycol and butyl acetate".
- *Evidence:* the four problems are real for this plant, each with locators that check out:
  - consecutive glycol reactions: Eqs. 6-7 (p.6) and Table 3;
  - water removal: Table 3, Fig. 5 and Table 8, where it is the plant's largest energy use;
  - vacuum homologue split at 190 C: Fig. 5 and Table 1;
  - the 8.5:1 water recycle: Table 3.

  The open question is approval, not substance.
- *Suggested fix:* the coordinator confirms that the maintainer approved them. Otherwise mark the four rows
  "proposed, awaiting the maintainer" in the register's preamble.

**m7. WATER REC is probably two-phase, and the plan does not say so.**
- *Location:* `record.json` (E-101 as an adjustable outlet temperature; run plan step 4); register row
  `plant-large-water-recycle`.
- *Evidence:* MIX-101 joins liquids at 1495, 895 and 395 kPa with the 15 kPa distillate, and its outlet is printed at
  15 kPa (Fig. 5). That matches HYSYS's mixer default of the lowest inlet pressure (my reading). At 48.17 C, Raoult's
  law with chepta 0.6.2's vapour pressures gives a bubble pressure of 17.4 kPa for WATER REC's 0.9812 water / 0.0173 EO
  (derived; activity coefficients of EO in water above 1 would raise it). That is above 15 kPa, so the stream is partly
  vapour. At E-101's outlet (0.77 C, 10 kPa) it is 1.8 kPa, all liquid. E-101 thus condenses EO-bearing vapour at
  vacuum; it is not a plain chiller.
- *Suggested fix:* in the run plan, set MIX-101's outlet pressure explicitly and check the phase of WATER REC. Add
  "condenses the EO-bearing vapour at 10 kPa" to the register row's route.

**m8. "p.5" locators should be p.6.**
- *Location:* `equipment.json` (lines 235, 243, 251), README lines 24, 76, 79 and 149, STREAM_AUDIT.md line 64,
  `balance-results.json` line 800, KB block `blk-p5-direct` and its rows, and the register row
  `rxn-ethylene-oxide-hydration-heavy-glycols` ("p. 5 (Eqs. 5-7)").
- *Evidence:* the section "Direct hydration of ethylene oxide" (Fig. 3a description, Eqs. 5-7, "20 °C to 270 °C",
  effluent at 199 °C, "10:1") follows the page-5 footer and sits on p.6 of the PDF. Fig. 3 is on p.6.
- *Suggested fix:* change to p.6 (the KB block through a new row if it is locked).

## Nits

1. **Eq. 7 has two misprints, not one.** It prints TEG as C6H14O5 as well as DEG as C4H10O4 (p.6). The audit's TEG
   formula C6H14O4 is Lab's, not the paper's; say so (README "Also:" line, `audit_balances.py` `FORMULA`).
2. **Disagreement 3 has support in the text.** "96 wt% yield of MEG" (p.13) agrees with Table 3 (96.5 wt % of the
   formed glycols are MEG, derived) and against Table 1's 85/15. Add it as supporting text.
3. **The commit message miscounts.** It says `informed_by` is on 9 rows; it is on 8 (the TEG row has none, as the
   README says).
4. **Disagreement 8 is soft.** 9.32 (all water / fresh EO) is close to a nominal "10:1". Label it approximate rather
   than in conflict.
5. **The evaporator checks by difference are weak.** Stream 4 is printed to three figures (±50 kmol/h), about ±6 % of
   EVA_1's 810 kmol/h vapour. Say so beside the "closes" in the README, so that it is not read as a strong check.
6. **`othman-2024-meg-reactive-distillation.cpa-for-glycol-water` is generous at "partly".** CPA is not in CHEPTA and
   the plan compares with nothing CPA-based. "no" (not usable in the engine) fits the note better.
7. **Small unlabelled stub on top of the condenser.** The Purification Tower's condenser has one on Fig. 5. It is
   probably a zero-flow vapour outlet (my reading); it does not change the distillate reading.

## Kinds of numbers, and invented values

Kinds of numbers are kept apart throughout:
- Every paper number is labelled a HYSYS simulation (`classification`, README, evidence rows `author_reported_simulation`).
- Lab's arithmetic is marked "derived".
- The asterisk reading is marked as Lab's.
- The paper's Table 5 property "validation" is not used as plant data.

No TEG property is entered anywhere: I searched for TEG values and found only Table 3's mole fractions and the formula
(nit 1). No CHEPTA output is claimed.

## For the person's spot check (2 or 3 items; the maintainer records it)

1. **M2: largest effect on the results.** In chepta 0.6.2 `src/data/binaries.json`, look for an NRTL pair for
   ethylene-oxide + water (I found only Wilson, ChemSep databank) and for any EO + glycol pair (I found none). Also
   confirm EVA_1 at 1600 kPa on Fig. 5 against "below 10 bar outside the reactor" in `record.json`.
2. **M1: the item I was least sure of.** Fig. 5 (p.10): is "149.6 C" printed without an asterisk and "*3534 kPa" with
   one? I compared against CHEPTA's EO vapour pressure (3537.8 kPa at 149.6 C, derived). If HYSYS specified T rather
   than a vapour fraction, M1 drops to minor.
3. **m5: picked at random** (`secrets.choice` over the minor findings). Is checking water + MEG and MEG + DEG against
   measured data, as the plan says, a routine revalidation that AGENTS.md excludes, given that both pairs are already
   fitted to measured data in chepta 0.6.2?

Record them as "person spot check (items, date)" beside "AI full check (Claude Opus 5.5, 2026-11-27)". If any of the
three is wrong, the case goes back for a full recheck (AGENTS.md).

## Follow-up by the builder (2026-11-27)

Written by the session that built the case, not by the reviewer. The rows of `dataset/records/ethylene-glycol-shehata-2024.json`
were not on main, so they were rewritten in place and their lock entries rebuilt from main's lock (main's entries
unchanged); no correcting rows were needed. Before rewriting, the builder read chepta 0.6.2's `components.json` and
`binaries.json` from the npm package of the pin (integrity as in package-lock.json) and confirmed the review's data: EO's
critical temperature 468.92 K; EO + water only a Wilson pair; no EO + MEG or EO + DEG pair; EO vapour pressure 3537.8
kPa at 149.6 C; Raoult bubble pressure of WATER REC 17.4 kPa at 48.17 C. No CHEPTA run.

| Finding | Done |
|---|---|
| M1 fresh EO saturated | Fixed: `record.json` fixed input is P = 3534 kPa with liquid fraction 1, T kept as comparison, with the reason; run plan step 1 checks the phase of every specified stream; README, DATASET_TABLE |
| M2 property-method reason | Fixed: reason rewritten (10-3534 kPa; vapour at 1600 kPa; reactor, streams 3, 15 and EVA_1 above EO's critical temperature; pair list; EO pairs estimated under NRTL); Wilson variant added; run plan step 0 is the check of what CHEPTA does with EO there. KB row `plan-property-method-nrtl` rewritten in place (unmerged) rather than corrected by a new row |
| m1 323 MW is the signed sum | Fixed: audit reports the signed sum as matching; disagreement 9 reworded; `record.json` keeps "sign convention not stated" for the entries only |
| m2 219.258 MW and 279 MW | Fixed: added as disagreements 10 and 11 (README, STREAM_AUDIT.md, DATASET_TABLE) |
| m3 vacuum-glycol-column "worked" at 190 C | Fixed: paper row's When, Why and Check reworded and a limit added (the separation worked, the 170 C limit did not); MEG-column plan note says the rule's 170 C is not met by the paper itself. Status kept "worked" (MEG 0.9977 reached) |
| m4 chen-2018 twice | Fixed: helped "no" on both, "different trigger; the published pressure is kept" |
| m5 li-2017 and routine revalidation | Fixed: helped "no" (not triggered); data check limited to the estimated EO pairs, TEG and the water + MEG range question; `record.json` and README say fitted pairs are reused (AGENTS.md) |
| m6 register rows awaiting approval | Partly: rows kept, as the coordinator asked; marked "proposed, awaiting the maintainer's approval" in the register's preamble, the README and DATASET_TABLE (question 7) |
| m7 WATER REC two-phase | Fixed: run plan sets MIX-101's outlet pressure and checks WATER REC's phase; register row and the water-loop plan row say E-101 condenses EO-bearing vapour at 10 kPa |
| m8 p.5 -> p.6 | Fixed: equipment.json, README, audit text, register row; KB block renamed `blk-p6-direct` (unmerged) |
| nit 1 Eq. 7 | Fixed: both misprints recorded (equipment.json, README); the audit's TEG formula labelled Lab's |
| nit 2 96 wt % | Fixed: p.13 added as support (equipment.json, README, register row, paper reactor row) |
| nit 3 commit message count | Not fixed: the pushed commit is not rewritten; the right count is 8 plan rows with `informed_by` (README says so) |
| nit 4 disagreement 8 soft | Fixed: labelled approximate |
| nit 5 weak check by difference | Fixed: README and STREAM_AUDIT.md say so, with the component-sum tops |
| nit 6 othman "partly" | Fixed: helped "no" |
| nit 7 condenser stub | Fixed: noted in equipment.json as Lab's reading |

## Follow-up check by the reviewer (2026-11-27)

**AI follow-up check (Claude Opus 5.5, 2026-11-27).** This is the same reviewer session; it is not a person's check. I
reviewed commit `0deb2f2` (the builder's fixes, on top of `3f71dae`). I read the diff of all 16 changed files and
changed none of them.

**Item by item**, against the builder's table above:

| Finding | Builder says | Confirmed? |
|---|---|---|
| M1 fresh EO saturated | fixed | **confirmed**: `record.json` fixes P = 3534 kPa at liquid fraction 1 and keeps T as a comparison, with the reason; run plan step 1 checks the phase of every specified stream |
| M2 property-method reason | fixed | **confirmed**: the reason now states 10-3534 kPa, vapour at 1600 kPa, and the reactor, streams 3 and 15 and EVA_1 above 468.92 K; the pair list matches chepta 0.6.2 `binaries.json` entry by entry; there is a Wilson variant; step 0 checks EO above its critical temperature |
| m1 323 MW signed sum | fixed | **confirmed** (322,961.68 kW; disagreement 9 reworded; `missing_inputs` narrowed to the individual entries) |
| m2 219.258 and 279 MW | fixed | **confirmed** (111,865 kW heating without DEH CON Q; 323 − 54.7 = 268.3 MW) |
| m3 vacuum-glycol-column at 190 C | fixed | **confirmed**: When, Why, Check and the limit now say 190 C is above the paper's 170 C. Keeping "worked" for the separation itself (MEG 0.9977) is acceptable now that the limit is explicit |
| m4 chen-2018 | fixed | **confirmed** (helped "no" on both) |
| m5 li-2017 | fixed | **confirmed**: helped "no"; data are looked at only for the estimated EO pairs, TEG and the water + MEG range question, which follows AGENTS.md |
| m6 register rows awaiting approval | partly | **confirmed as described**: the rows are kept and marked "proposed, awaiting the maintainer's approval". Whether to keep them in the register before approval is the coordinator's call |
| m7 WATER REC two-phase | fixed | **confirmed** (run plan step 4, register row, water-loop plan row) |
| m8 p.5 → p.6 | fixed | **confirmed**: no "p.5" locator for the direct-hydration section remains; the block is now `blk-p6-direct` |
| nits 1, 2, 4, 5, 6, 7 | fixed | **confirmed** |
| nit 3 commit message count | not fixed | **accepted**: the pushed commit is not rewritten; the README gives the right count (8) |

**No new errors.** I rechecked every number the fixes add against the paper or against chepta 0.6.2's data: 3537.8 kPa,
468.92 K, 17.4 kPa, 111,865 kW, 268.3 MW, 3.555 wt % (22,270 / 626,470), 96 wt % on p.13, the six pair entries, and
"ChemSep v8.3 … Artistic License 2.0" (chepta 0.6.2 `src/data/LICENSES.md`). All are correct.
- The relabelled "DEG+TEG stream as a share of the two product streams' printed mass" now describes its 3.555 correctly.
- Locked rows were rewritten in place rather than corrected by new rows. This is acceptable because they were never on
  main. I compared `dataset/index/outcomes.lock.json` at main (`8b8b64f`) with `0deb2f2`: every main entry is
  unchanged. The 306 main ids are all still in `indexed`, and the only additions are the 13 ethylene glycol ids and
  their 8 `informed_by` lists.

**The builder's correction of my review: confirmed.** In chepta 0.6.2 there is no EO + MEG or EO + DEG pair in any model,
Wilson included; EO + water has Wilson only. My review already said "no pair at all", but my M2 fix ("Wilson … the
glycol pairs") meant the pairs among water, MEG and DEG. Under Wilson the EO + glycol pairs are still estimated, as
`record.json` now says.

**Checks** at `0deb2f2`:
- `validate_catalog.py`: exit 0.
- `dataset_pipeline.py validate`: exit 0, `"valid": true`.
- `unittest`: 127 tests, OK.
- `kb.py check`: exit 0, index current (case-decision 158, design-rule 127, simulation-rule 34, disputed sets 2).

**chepta 0.6.3.** I fetched `npm pack chepta@0.6.3` into my scratchpad (shasum `8dc18177…6e59f3`) and compared its
`src/data/components.json` and `src/data/binaries.json` with 0.6.2's:
- **Components:** the records of water, ethylene-oxide, ethylene-glycol and diethylene-glycol are identical in every
  field. triethylene-glycol is in neither version.
- **Pairs:** every pair among these components is identical in both versions (NRTL, UNIQUAC and Wilson for water + MEG,
  DEG + MEG and DEG + water; Wilson only for EO + water). Neither version has EO + MEG or EO + DEG.

So the property-method reason's data hold for 0.6.3 unchanged. Only the version label "0.6.2" in `record.json` and the
KB row would need "(unchanged in 0.6.3)" when the pin moves. I did not read 0.6.3's code, method guide or UNIFAC data.

**Final items for the person's spot check** (unchanged in substance; check them on the fixed files):
1. **M2: largest effect on the results.** chepta 0.6.2 (or 0.6.3) `binaries.json`: no NRTL pair for EO + water and
   no pair at all for EO + glycol; EVA_1 at 1600 kPa on Fig. 5. Then check that `record.json`'s new reason says this.
2. **M1: the item I was least sure of.** Fig. 5: "149.6 C" without an asterisk, "*3534 kPa" with one; and whether
   fixing the EO feed by P and liquid fraction 1 is the right reading.
3. **m5: picked at random.** Whether the revised plan (data looked at only for estimated or out-of-range pairs)
   now follows AGENTS.md.
