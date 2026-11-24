# Review of PR #34: lessons from the ethyl acetate and methanol plants

**AI full check (Claude Opus 5.5, 2026-11-24).** I am a separate AI review session, started by Lab's coordinator. I did
not build these rows. This is not a person's check. The person's spot check (end of this note) is still to do, and only
the maintainer records it.

Reviewed: branch `claude/lab-backfill-plants` at commit `71cbb52`. I checked these rows:
- the 27 lessons (rows with `keys.summarises`): 16 in `dataset/records/ethyl-acetate-piotrowski-2021.json` and 11 in
  `dataset/records/methanol-co2-campos-2022.json`;
- the 11 paper-design rows with `keys.plain` (6 ethyl acetate, 5 methanol);
- the generated pages `dataset/index/plants/*.md` and the "From Lab's own plant" entries under `dataset/index/rules/`.

I edited no record and no code.

## What was checked

- **Every lesson against the rows it summarises.** For all 27 lessons I listed each summarised row's status, engine,
  run ids, operation and limits. I compared every number, outcome and engine label in the plain fields and in
  `judged_on` with those rows. Where a lesson's claim rested on a run's input (the tear sets of `plant-a2` and
  `plant-a6`) or on the case README (the CO2-compression figure), I opened the run request or the README.
- **Paper numbers against the papers.** I downloaded both open-access articles and the methanol supplement into
  `raw_papers/review-lessons-2026-11-24/` (git-ignored, not committed). Their sha256 values are 0057df76… (Piotrowski &
  Kubica 2021), 8215079… (Campos et al. 2022), and the supplement zip 5b0b1c46…; the two article hashes match the
  ones the earlier review recorded. I extracted the text with `pdftotext -layout` and read each passage. I read the
  files as evidence only.
  - *Piotrowski & Kubica 2021, https://doi.org/10.3390/pr9081425*: Sections 3.2-3.5, Table 1, Table A2 (S2).
    - Table 1, S2: reactor 85-90 C, 300 m3, 13,586.2 kW; SCDS 5 with 8 stages, R/V 0.61; SCDS 15 with 18 stages,
      feed 9, R/D 2, reboiler 16,136.6 kW; HTXR 2 535.6 kW; EXTR 8 at 70 C, W/A 1.
    - Section 3.2: 0.005 wt% acid; at least 14 stages and R/V above 0.5.
    - Section 3.3: W/A 1-2 is the optimum; cooling to 20-30 C.
    - Section 3.4: 99.9 wt% ester, water below 0.03 wt%, ethanol below 0.04 wt%.
    - Section 3.5: organics below 0.01 wt%.
    - p. 3: about 17 % water released, about 7.8 % in the azeotrope, the organic phase above 93 %.
    - Table A2: streams 1-2 at 15 C; streams 5 and 6 with acid at 20.64 and 4.74 mass %, so 1 - 4.74/20.64 = 0.7703;
      stream 6 at 90 C; stream 11 at 87,314 kg/h with 1.86 % ethanol and 4.70 % water; stream 13 with 0.01 % acid;
      stream 16 at 141.5 kmol/h and 12,434 kg/h with 0.02 % ethanol, 0.07 % water, 99.90 % ester and 0.01 % acid;
      stream 21 at 394.6 kmol/h; stream 22 with 0.02 % ethanol and 0.01 % acid; streams 23, 25 and 17 at 95,797,
      20,000 and 17,478 kg/h.
    - The 0.022 % acid in the product follows from these numbers: 27,314 x 0.01 % / 12,434.
    - All agree with the rows, except finding m7.
  - *Campos et al. 2022, https://doi.org/10.3390/pr10081535, with supplement*:
    - Abstract: 28.5 % and 30.4 %.
    - p. 4: 70 bar; 33,000 tubes of 12.5 m and 3.75 cm.
    - p. 9: Peng-Robinson in the reactor, NRTL2 elsewhere.
    - p. 10: 30 stages, reflux ratio 2, feed above stage 24, partial condenser at 53 C.
    - Supplement Section E: FLASH3 at 30 C and 69.25 bar, FLASH4 at 30 C and 1 bar, purges of 2 % (1051 and
      51 kmol/h), HE4 to HE7 duties, 36-REC 51,504 kmol/h and 39-REC 2786 kmol/h.
    - Table S9: stream 16 at 32,021 kmol/h and 247.9 C; stream 24 at 11,488 kmol/h; 31-MEOH at 4542 kmol/h,
      30-WATER at 4581 kmol/h, gas distillate 32 at 289 kmol/h.
    - Table S10: 7.415 % methanol in stream 16; 18.545 % CO2 in stream 24; 1.285 % CO2 in stream 28; 99.667 %
      methanol; 99.985 % water.
    - Table S14: HE5 103.3 MW, HE7 24.2 MW, condenser 143.6 MW, reboiler 53.7 MW.
    - From Table S9, HE7 works out to 64,042 x 1.11 kJ/mol = 19.75 MW and HE5 to 9412 x 39.52 kJ/mol = 103.3 MW.
    - All agree with the rows, except finding M1.
- **Precision rule.** 140.5 kmol/h at 99.897 % is said to meet 99.90 wt %; 141 and 141.5 kmol/h at 99.873 % and
  99.848 % are said to miss it; methanol at 99.835 % and 99.728 % is said to meet 99.67 mol %. All are stated
  correctly.
- **Statuses against `judged_on`.** I checked every lesson's status against the objective it names.
- **Commands** (run on `71cbb52`, results exactly):
  - `python scripts/validate_catalog.py`: "Catalogue OK: 41 sources, 8 candidate families; 0 accepted training
    examples." Exit 0.
  - `python scripts/dataset_pipeline.py validate`: `"valid": true` (decisions 305, evidence 30, blocks 29, tasks 3;
    each task lists its release blockers). Exit 0.
  - `python -m unittest discover -s tests`: "Ran 124 tests … OK". Exit 0.
  - `python scripts/kb.py check`: `{"rows_by_kind": {"case-decision": 144, "design-rule": 127, "simulation-rule":
    34}, "disputed_sets": 2, "index": "current"}`. Exit 0.

**Not checked:** I did not rerun any simulation. I recomputed no simulated number from the run outputs: the earlier
review (`backfill-plants-review.md`) did that for the rows, and here I checked the lessons against the rows. I also did
not look at Figures 2-7 of Piotrowski & Kubica 2021.

**Counts:** 4 major, 11 minor, 5 nits. No lesson hides a failed run outright. Two lessons leave out results that
weaken their claim (M2, and part of m2). One lesson rests on a wrong reading of the paper (M1).

## Major

**M1. `methanol-co2-campos-2022.lesson-reactor-u-assumed`: Campos et al. 2022 does print the heat-transfer
coefficient.**
- *What is wrong:* The title says "without a printed U" and the When says the heat-transfer coefficient is not given.
- *Evidence:*
  - Campos et al. 2022, p. 13-14, Section 3.1.1, gives the value for the selected one-step condition:
    "Uz=0 = 160 W·m−2·K−1 and Uz=12.5 = 150 W·m−2·K−1 … the average value was used (Uavg = 155 W·m−2·K−1)".
  - Supplement Section E gives the coolant at 247.5 C, which Lab already uses (520.65 K).
  - Lab's 300 W/m2/K is about twice the published value.
  - The result still holds: the U 150 run is close to 155 and moves the outlet by only 0.40 K. The lesson's reason
    for assuming U is what is wrong.
  - The same mistake is older than this PR: the summarised row `reactor-lhhw-u-assumed-062-c2` has the obstacle "The
    reactor's heat-transfer coefficient is not printed", and `cases/methanol-co2-campos-2022/README.md` line 85
    says "not printed".
- *Fix:*
  - Rewrite the lesson as: "Campos et al. 2022 print U = 155 W/m2/K (average of 160 and 150, p. 13-14). Lab ran
    300, 150 and 1000; the outlet moves by 0.40 K and up to 0.035 points over that range."
  - Better still, run U = 155 and quote that run as the comparison with the paper.
  - The obstacle and limits of the row are not protected by the lock, so they can be corrected in place. Correct
    the case README too.

**M2. `ethyl-acetate-piotrowski-2021.lesson-purity-set-by-ethanol-and-water` (tagged `applies-beyond-plant`): the
claim is too wide, and part of it rests on runs that had not settled.**
- *What is wrong:*
  - The status is `failed`: none of the recommended actions reached 99.90 %. Yet the lesson is put forward as a rule
    beyond this plant, and its Do reads as a proven recipe.
  - The claim that "adding stages … does not help" comes from the 36- and 38-stage runs (99.675 and 99.680 %
    against 99.672 %). The summarised row `col11-more-stages-062-c1` says these were "all from the saved start at
    the unsettled tolerance 3e-4 (not the settled 99.109 %)". The lesson does not say so, although its sister lesson
    `lesson-tighten-tolerance-from-saved-answer` shows that the 3e-4 answers of this plant are wrong by 0.56 points.
  - The Result leaves out three summarised outcomes:
    - 40 stages did not converge;
    - on 415da41 the 270 kmol/h distillate converged at 99.223 % (row `col11-distillate-260-280-settled-415da41-dist270`);
    - raising the wash water to W/A 1.13 gave 99.118 %, no gain (row `wash-water-raised-062`).
  - The Result says "260-280 kmol/h … did not converge on 0.6.2". That is true, but on its own it reads as if these
    distillates were never reached.
- *Fix:*
  - Either drop `applies-beyond-plant`, or keep only the general part: an excess reactant whose only exit is the
    product builds up in the recycle, so balance it before tuning the column. Label that part a lead, not a result.
  - State that the stage comparison was made at 3e-4, before the plant had settled.
  - Add the 40-stage, 415da41 270 kmol/h and W/A 1.13 outcomes.

**M3. `ethyl-acetate-piotrowski-2021.lesson-product-column-purity-spec-no-acid`: a missed limit is not stated.**
- *What is wrong:* `judged_on` reads only "Ester purity 99.90 wt%". The summarised rows show water at 0.113 % (at
  the published flow) and 0.084 % (with the purity given). Both are above the 0.03 wt% water limit of Piotrowski &
  Kubica 2021, Section 3.4 (p. 9). The maintainer's rule of 2026-11-21 asks that every other missed limit be stated
  with its source. The sister lesson `lesson-product-column-trace-acid` does this; this one does not.
- *Evidence:* rows `col11-no-acid-paper-flow-061` ("0.113 % water") and `col11-no-acid-purity-spec-061` ("water
  0.084 %").
- *Also:* The Why ("CHEPTA's thermodynamics differ slightly from Chemcad's, so the published flow no longer gives the
  published purity") is not in either row. It is a guess. The audit lesson shows that the published Table A2 itself
  has 0.07 % water in the product.
- *Fix:*
  - Add to `judged_on`: "Water 0.113 % and 0.084 % exceed the 0.03 % limit of Piotrowski & Kubica 2021, Section 3.4;
    whether that matters depends on the product specification of the application."
  - Mark the Why as Lab's inference, or replace it with what the rows show.

**M4. `ethyl-acetate-piotrowski-2021.lesson-product-column-trace-acid`: the Why puts the shortfall on the acid, but
the rows show water causes most of it.**
- *What is wrong:* The Why says "All the acid of the feed ends in the product, so a product as large as the
  published one is too dilute." The rows say otherwise:
  - At 141.5 kmol/h the product is 99.848 % with 0.111 % water (row `…purity-short-141-141.5`). Acid accounts for
    only about 0.02 points of the shortfall: 0.022 %, as the audit lesson works out.
  - Without any acid the same column at the published flow also misses: 99.868 % with 0.113 % water (row
    `col11-no-acid-paper-flow-061`).
  - So lowering the bottoms flow works mainly by sending more water overhead, not by concentrating the acid less.
  - The Do also says "do not give the purity, which returns a wrong answer". That rests on one 0.6.2 run (row
    `col11-acid-purity-spec-062`), but the lesson's engine is 415da41, where a purity specification was not tried.
- *Fix:*
  - Rewrite the Why: "Water is the main impurity at the published flow (0.111 %), even without acid (0.113 %). A
    smaller product sends more water overhead, and the acid, which can only leave with the product, adds about
    0.02 points."
  - Say "on chepta 0.6.2 a purity specification returned a wrong root (31.0 kmol/h); not tried on 415da41".

## Minor

**m1. `ethyl-acetate-piotrowski-2021.lesson-extractor-feed-saturated`: the run does not test the recommended
action.**
- *What is wrong:* The lesson's only run, `rerun-secB-mix7-adiabatic`, is the *adiabatic* mixer, which 0.6.2
  accepted. The lesson recommends a saturated-liquid mixer, which is not what that run tested. Its status `worked`
  is therefore not the outcome of the action it recommends (proposal 0003, section G).
- *Fix:* Cite runs that used the saturated-liquid mixer: for example the settled closed plant, or the 0.6.1
  workaround run, if it is added to a summarised row. Alternatively, rephrase the lesson as "an adiabatic mixer
  worked alone on 0.6.2 but was refused in the open plant (17 % vapour)".

**m2. `ethyl-acetate-piotrowski-2021.lesson-acid-stripping-reflux`: the title says "55,000 kg/h or more", which is
wider than the runs show.**
- *What is wrong:* On the lesson's engine (0.6.2), 70,000 kg/h did not converge (row `col5-reflux-scan-irregular-062`).
  No acid value above 65,000 kg/h is given for any engine. The margin at 55,000 kg/h (0.0036 % against 0.005 %) is
  small for a recommendation to "take the lowest that meets the limit with margin".
- *Fix:* Say "55,000 to 65,000 kg/h", and add "acid at 70,000 kg/h on 415da41 not reported".

**m3. `methanol-co2-campos-2022.lesson-tears-break-every-cycle`: "five tears" is not what made the difference.**
- *What is wrong:* The refused run `plant-a2` already had five tears (19, 36-REC, 26, 28, 39-REC). Its error lists
  them: "The streams marked as tear streams (19, 36-REC, 26, 28, 39-REC) do not break every cycle". The accepted run
  `plant-a6` used 19, **35**, 26, 28, 39-REC (case README, tear-streams row). What made the difference was moving one
  tear from 36-REC to 35, on the far side of HE2, not the number of tears.
- *Fix:* Result: "Recycle tears only, and also five tears including 36-REC: refused. Tears 19, 35, 26, 28 and
  39-REC: closed in 31 iterations." Do: "choose tears that cut each exchanger's cycle; how many is not the test."
  The general rule itself is sound.

**m4. `methanol-co2-campos-2022.lesson-feed-effluent-exchanger-approach`: the comparison with Table S14 is missing.**
- *What is wrong:* `judged_on` says the duty "is compared with Table S14", but no comparison is given. Table S14
  gives HE5 at 103.3 MW. Lab's 114,966 kW is 11.3 % higher, and its cold outlet of 84.99 C is above stream 29's
  82.9 C (Table S9).
- *Fix:* Add "114,966 kW against 103.3 MW in Table S14 (+11 %); cold outlet 84.99 against 82.9 C".

**m5. `methanol-co2-campos-2022.lesson-condenser-by-vapour-share` (tagged `applies-beyond-plant`): the claim is too
wide, and the text says "the paper".**
- *What is wrong:*
  - The rows show a CHEPTA solver limitation on one unreleased commit: request M6 is open, and the column alone
    converges at 53.005 C when given its vapour share. The title states it as a general rule ("not by its
    temperature"). In other simulators, or once M6 is fixed, the temperature specification may be the right choice.
  - The vapour share 0.008406 comes from Lab's own converged `plant-a6`, which was solved with the flash workaround.
  - `judged_on` says "the paper's condenser configuration; the paper's 53 C specification", against the rule that
    papers are named.
- *Fix:*
  - Scope the title to "on chepta 415da41 (request M6 open)", or drop `applies-beyond-plant`. The general part
    could be: restart a hard specification from a converged answer's equivalent specification.
  - Write "Campos et al. 2022" in `judged_on`. `kb.py check` does not look at `judged_on`; a check could be added.

**m6. `methanol-co2-campos-2022.lesson-column-light-gas-traces`: the bypass is a component split, and the lesson
does not say so.**
- *What is wrong:* On 0.6.2 the Do takes the ppm gases out before the column and joins them to its vapour. That is a
  split that bypasses the column's physics. AGENTS.md forbids presenting such a split as a reproduction. The row
  `column-gases-bypassed-flash53-062` calls it a workaround, but the lesson does not.
- *Fix:* Add: "a workaround (an imposed split of ppm traces), not the paper's column; rerun without it on a later
  engine (415da41 converges with them)".

**m7. `ethyl-acetate-piotrowski-2021.paper-wash-ratio-1-to-2`: the case (S2) runs at 70 C, not "cooled to 20-30 C".**
- *What is wrong:* The 20-30 C comes from Section 3.3 and belongs to the improved strategy S1 (Table 1: EXTR 8 at
  30 C). In S2, the strategy Lab reproduces, Table 1 gives EXTR 8 at 70 C. The lesson
  `lesson-extractor-isothermal-stages` quotes 70 C, so a reader sees two temperatures with no explanation.
- *Fix:* "cooled to 20-30 C in Piotrowski & Kubica 2021's improved strategy S1 (Section 3.3); their strategy S2,
  reproduced here, extracts at 70 C (Table 1)".

**m8. `ethyl-acetate-piotrowski-2021.lesson-close-plant-purity-specs`: the Why gives only one reason, and the rows
show others.**
- *What is wrong:* The Why says "the published settings belong to its own thermodynamics". The summarised row
  `plant-paper-column-specs-415da41-c1-no-convergence` shows something else for two of its four 415da41 variants:
  they stopped at the reactor because 141.5 kmol/h of product exceeds the 141.07 kmol/h of ester the feeds form, an
  over-specification (the subject of `lesson-product-flow-within-feed`). Four more variants ran out of time.
- *Fix:* "With the published settings the plant is over-specified (product flow above the ester formed) and, on
  0.6.2, column 5 failed; purities keep each column on its target."

**m9. `ethyl-acetate-piotrowski-2021.lesson-audit-paper-column-balance`: a third limit is left out.**
- *What is wrong:* The Result lists two limits that Table A2 does not meet. A third is unproven at the printed
  precision: the acid in the azeotrope, streams 8 and 9 at 0.01 % against the 0.005 % limit of Section 3.2. The
  summarised paper row `paper-azeotropic-column-acid-stripping` already notes this.
- *Fix:* Add "acid in the azeotrope: 0.01 % printed against 0.005 %, not decidable at two decimals".

**m10. Readability across 7 lessons: "415da41" is not explained.** It appears in the title or result of
`lesson-acid-stripping-reflux`, `lesson-close-plant-purity-specs`, `lesson-column-light-gas-traces`,
`lesson-vapour-liquid-condenser-by-flash`, `lesson-column-bottoms-flow-spec` and
`lesson-feed-effluent-exchanger-approach`, and is the engine of `lesson-condenser-by-vapour-share`. A chemical
engineer who does not program will not know it is an unreleased CHEPTA development commit. The plant pages do not
explain it either.
- *Fix:* Add one line at the top of each plant page: "415da41 is an unreleased development version of CHEPTA,
  between releases 0.6.2 and the next". Or write "CHEPTA development version 415da41" in the plain text.

**m11. `ethyl-acetate-piotrowski-2021.lesson-acid-with-two-liquids`: a known discrepancy and the 0.6.1 workaround
are not mentioned.**
- *What is wrong:* The Check says "compare each duty with Table 1", but the summarised row
  `acid-two-liquids-units-062` records that the HTXR 18 and 19 duties are swapped in Table 1 (maintainer,
  2026-11-12), so a reader doing the check would find a false mismatch. The row `acid-two-liquids-units-061` records
  that the 0.6.1 results dropped the acid after column 5, and the lesson does not say so either.
- *Fix:* Add "HTXR 18 and 19 are swapped in Table 1" and "on 0.6.1 Lab dropped the acid after column 5".

## Nits

- **n1** `ethyl-acetate-piotrowski-2021.lesson-reactor-conversion-imposed`: the Check quotes "89.0 C against 90 C,
  duty +6.3 %". These come from the 0.6.1 run `u-krea4-conversion` (row `reactor-conversion-imposed-061`), but the
  lesson's engine is 0.6.2. Add "(chepta 0.6.1)".
- **n2** Several cross-references point to a position or a vague name. Examples: "see the reactor lesson above" (row
  `paper-reactor-evaporator`), "see the cooler lesson" (`paper-feed-effluent-exchangers`), "judged in another
  lesson", "see the flash lesson", "see the open question". On a topic page these lessons sit apart, so the
  reference does not resolve. Name the lesson's title instead.
- **n3** `methanol-co2-campos-2022.lesson-gases-with-pr-kij`: next to the 3.37 % CO2, give the FLASH3 liquid flow
  too (9468 against 11,488 kmol/h, -18 %; row `property-method-pr-everywhere-062`).
- **n4** `ethyl-acetate-piotrowski-2021.paper-organic-phase-as-azeotropic-agent`: the "about 7.8 %" water comes from
  Piotrowski & Kubica 2021's literature summary (p. 3, citing their refs 8 and 29). Their own Section 3.2 gives the
  azeotrope as 8.2 % water. Mention both.
- **n5** `ethyl-acetate-piotrowski-2021.lesson-acid-stripping-reflux`: the Check says "a failure between converged
  neighbours is the solver". Two of the four 0.6.2 failures (45,000 and 70,000 kg/h with the published vapour) are
  at the ends of the scan, not between neighbours. Say "an irregular failure that a later engine converges".

## Question 5: are the 6 lessons marked `applies-beyond-plant` general?

| Lesson | Verdict |
|---|---|
| `ethyl-acetate…lesson-product-flow-within-feed` | General: a degrees-of-freedom and stoichiometry check. Supported by the rows. |
| `ethyl-acetate…lesson-tighten-tolerance-from-saved-answer` | General, and well supported (99.673 % against 99.109 %, ethanol 14,629 to 17,455 kg/h). |
| `ethyl-acetate…lesson-hold-excess-reactant-by-design-spec` | General as a technique. One run, and the plant's purity was not met (stated). Acceptable. |
| `methanol…lesson-tears-break-every-cycle` | General principle; the stated fact needs correcting (m3). |
| `ethyl-acetate…lesson-purity-set-by-ethanol-and-water` | **Too wide** (M2): a failed outcome and runs that had not settled. |
| `methanol…lesson-condenser-by-vapour-share` | **Too wide** (m5): a workaround for one engine (M6). |

## Rows found faithful (no finding)

**Ethyl acetate:** `lesson-cold-acid-feed`, `lesson-acid-stripping-two-liquids`, `lesson-extractor-isothermal-stages`,
`lesson-wastewater-column`, `lesson-product-flow-within-feed`, `lesson-tighten-tolerance-from-saved-answer`,
`lesson-hold-excess-reactant-by-design-spec`; paper rows `paper-azeotropic-column-acid-stripping`,
`paper-wastewater-column`, `paper-water-loop-round-flows`.

**Methanol:** `lesson-dissolved-co2-sets-co2-recycle` (the "27-31 % less gas" matches the case README, line 11),
`lesson-vapour-liquid-condenser-by-flash` (+5 % and +17 % match 151.0/143.6 and 62.6/53.7 MW),
`lesson-column-bottoms-flow-spec`, `lesson-duty-against-stream-enthalpies`, `lesson-closed-plant-ends-agree`; all
five paper rows.

## Items for the person's spot check

These are chosen by this AI review; the person checks them. Nothing below records a person's check.

1. **Largest effect on results: M2.** In the record, compare the Result of
   `ethyl-acetate-piotrowski-2021.lesson-purity-set-by-ethanol-and-water` with the limits of row
   `col11-more-stages-062-c1`, which says "from the saved start at the unsettled tolerance 3e-4". Then decide
   whether this failed lesson should be offered beyond the plant. It goes onto a topic page and will guide future
   plants.
2. **Least sure: m5.** Is `methanol-co2-campos-2022.lesson-condenser-by-vapour-share` a general lesson or a CHEPTA
   workaround? This is a judgement on scope; the facts are not in dispute (request M6 is open; the column alone
   converges at 53.005 C with the vapour share).
3. **Picked at random** (Python `random.SystemRandom` over the findings other than items 1 and 2): **m6**, the
   ppm-gas bypass in `methanol-co2-campos-2022.lesson-column-light-gas-traces`. Is it acceptable as a stated
   workaround, and does the lesson need to call it an imposed split?

Also worth a look if there is time: **M1**, the easiest finding to confirm. Campos et al. 2022, p. 14, first lines:
"Uavg = 155 W·m−2·K−1".

Record when done: **person spot check (items, date)**, by the maintainer.
