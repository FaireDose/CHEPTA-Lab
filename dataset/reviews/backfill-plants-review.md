# Review of PR #28: backfill of the ethyl acetate and methanol plants

**AI full check (Claude Opus 5.5, 2026-11-20).** This is a separate AI review session; it did not build the rows.
It is not a person's check. The person's spot check (below) is still to do, and only the maintainer records it.

Reviewed: branch `claude/lab-backfill-plants` at commit `62237f8`. The rows in
`dataset/records/ethyl-acetate-piotrowski-2021.json` and `dataset/records/methanol-co2-campos-2022.json`, the 5 new
register rows in `data/ISSUES_AND_ROUTES.md`, the edits to `tests/test_kb.py`, the line in the process-design skill and
the regenerated index.

## What was checked

- **133 new rows:** 92 decision rows (57 ethyl acetate, 35 methanol), 20 evidence rows and 21 source blocks.
- **Source blocks:** I downloaded the article PDF of each paper and the methanol supplement (zip) into `raw_papers/`.
  Their sha256 values match the blocks: 8215079…, 0057df76…, and 015d60b5… for the PDF inside the zip. I extracted
  the text with `pdftotext -layout` and recomputed all 21 `source_fragment_sha256` values from the stated line ranges.
  **All 21 match.** I read each passage against its evidence claim and quantities. All agree, including the S2
  values of Table 1 and Table A2, the purities in Table S10, HE7 at 24.2 MW in Table S14, 70 bar, 33,000 tubes and
  the 2 % purges. I also checked numbers that rows cite without an evidence row against the paper:
  - fresh water 17 = 17,478 kg/h;
  - 36-REC = 51,504 kmol/h against 1-CO2 + 11-H2 = 4,824 + 14,472 kmol/h, a ratio of 2.67;
  - 248 C (stream 16 is at 247.9 C);
  - 1.285 mol % CO2 in stream 28;
  - six reactor modules (supplement p.9).
- **Run ids:** every `run_ids` entry resolves to an `.output.json`. For each one I checked CHEPTA's outcome and code
  (`ok`/`done` or the error code) against the row's `status`, its symptom, and the engine implied by the results
  folder. The `chepta@415da41` labels match the folder `results-chepta-main-415da41` and the schema pattern.
- **Numbers from runs:** I recomputed about 60 of the simulated numbers in the rows' `limits` from the run outputs.
  Mass or mole fractions came from the component flows (product 16, wastewater 22, 31-MEOH, 30-WATER, 32, 36-REC,
  39-REC, FLASH3 liquid, reactor outlet); duties came from `energy` or the column state. Among them:
  - every product purity of columns 11 and 15 and of the closed plants;
  - the reboiler duties of column 15;
  - the design-specification result (F1 6,506.23 kg/h, 8 solves, bracket 6,503.5-6,507.5);
  - plant-a6 and its reruns;
  - the column alone with the 53 C flash and with the vapour-liquid condenser;
  - u-flash3 and u-flash4;
  - HE7 (25.1 MW to 30 C; 31.05 C at 24.2 MW; 36.06 C at 19.75 MW);
  - HE5 (84.99 C with 10 zones, 84.93 C on 415da41, the cross at 72.18/72.46 C on the plant's streams);
  - the reactor at U 150, 300 and 1000.

  Numbers I did not recompute from runs I checked against the case READMEs and COMPARISON.md. Iteration counts and
  wall times I checked only where the output reports them.
- **Basis and kinds of numbers:** `paper_simulation` rows carry no run ids; `chepta_run` rows carry an engine;
  `lab_inference` rows are marked as inference. Lab-derived values are labelled as derived: HE7 at 19.75 MW, the per-pass
  conversion 0.7703 and the 141.07 kmol/h of ester formed. None of these is passed off as the paper's.
- **Checks rerun on the PR branch:** `python scripts/validate_catalog.py` OK; `python scripts/dataset_pipeline.py
  validate` OK; `python scripts/kb.py check` says the index is current; `python -m unittest discover -s tests` ran 100
  tests, OK.
- **Register rows and tests:** read in full, below.

## Problems found

Severity: **major** means a row claims more than its runs show, on a result that matters. **Minor** means a row is
inaccurate or incomplete but the conclusion stands. **Nit** means wording or bookkeeping.

**Why this matters before merging:** `kb.py index` copies each CHEPTA-run outcome into
`dataset/index/outcomes.lock.json`, and a later edit of that outcome fails the checks. Correct the statuses before
the PR merges, or the corrections will need deliberate edits of the lock file.

### Major

1. **`ethyl-acetate-piotrowski-2021.open-reach-99.9-pct` and `….ds-start-distillate-250-260-415da41` understate the
   best closed-plant answer.**
   - What the rows say: "In the closed CHEPTA plant the product stops at 99.56 % (water 0.40 %)", and 99.561 % is
     "the best closed answer".
   - The evidence: `plant62-settled-extr20C-ethanol6506` (extractor at 20 C, ethanol feed 6,506 kg/h, tolerance 1e-5,
     converged) gives **99.666 % ester, 0.296 % water, 0.038 % ethanol**, on 0.6.2 and identically on 415da41. That is
     higher than the 99.561 % of `new-plant-dsinit-dist260`. The ethanol-feed-trimmed-062 row quotes the 99.666 % itself.
   - Where the error came from: the case README, line 121, says "Best closed-plant answer on main: 99.561 %". The
     backfill copied it and dropped "on main", but the 99.666 % run also exists on main.
   - Suggested correction:
     - Best settled closed answer: 99.666 % (cold extractor plus trimmed ethanol feed).
     - Best with the ethanol held by a design specification and column 11's distillate raised: 99.561 %.
     - Untried: the cold extractor, the design specification and the raised distillate together.
     - Correct README lines 51 and 121 in the same way. Both are
       outside this PR, but they are the source of the error.

2. **`ethyl-acetate-piotrowski-2021.col11-acid-flow-140.5-415da41` is `worked`, but its target is not met.**
   - The objective is 99.9 wt% ester (ev-product). The run `new-iso-scds11-acid0.01-bottoms140.5` gives **99.8970 %**
     ester and 0.066 % water; the water limit is 0.03 %.
   - The row's own limits say "water still above the 0.03 % limit".
   - Rounded to two decimals the purity is 99.90 %, and the README adjustment table treats it as met. Neither is
     stated in the row.
   - Suggested correction: `failed` with `purity-short`, noting it misses 99.90 % by 0.003 points. Alternatively,
     keep `worked` but state the rounding convention and that the water limit is missed. The 140 kmol/h run (99.922 %,
     water 0.044 %) is the one that meets the purity.

3. **`ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41` is `worked` with the 99.9 % purity objective.**
   - Of its three runs, only 140 kmol/h meets the purity (99.922 %). The other two fall short: 141 kmol/h gives
     99.873 % and the paper's 141.5 kmol/h gives 99.848 %.
   - The limits say so, but the index counts the row as `worked` for `sep-two-liquids-with-acetic-acid` with that
     objective.
   - Suggested correction, either:
     - split it into a `worked` row (convergence, or 140 kmol/h) and a `failed`/`purity-short` row (141 and
       141.5 kmol/h); or
     - drop the purity objective and state that the row records convergence only.

### Minor

4. **`ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41` leaves out failed runs and overstates the
   result.**
   - The 0.6.2 row lists 9 runs; the 415da41 row lists 7.
   - It leaves out `plant62-R-purity-direct` (`OUT_OF_TIME`) and `plant62-R-bottoms-col5VL`. The second stops with
     `PHASE_SPLIT` **in column 5** at iteration 7, which contradicts the row's "column 5 passes".
   - 4 of the 9 runs end `OUT_OF_TIME` (time limit 1,500 s), not `NO_CONVERGENCE`. The row's symptom and text give
     only the convergence failure.
   - Suggested correction: add both runs; say "column 5 passes except in the variant with column 5 at one liquid
     (PHASE_SPLIT)"; mention the time-outs, for example with symptom `slow` noted in the text.

5. **`ethyl-acetate-piotrowski-2021.plant-variant-w-both-round-flows-062` is `worked` at tolerance 5e-4.**
   - Its balance is off by 42 kg/h (0.13 %).
   - The sibling row `plant-purity-specs-loose-tolerance-062` is `failed` because an answer at 3e-4 had not settled,
     the case's own lesson.
   - The two rows apply different standards. Suggested correction: add a limit saying the variant was not settled at
     a tight tolerance, or mark it `failed` with `recycle-drift` to match the sibling.

6. **`ethyl-acetate-piotrowski-2021.col5-reflux-scan-415da41`** says "All 12 iso-scds5 runs converge" but lists 4 run
   ids. Suggested correction: list all 12, or say "the 4 that failed on 0.6.2 now converge (all 12 do; README)".
   `col5-reflux-scan-meets-limit-062` cites the 50,000 kg/h result (0.055 %, misses the limit) without its run id.

7. **`methanol-co2-campos-2022.plant-closed-062`** gives 31-MEOH, 30-WATER, 36-REC and 39-REC but not the gas
   distillate 32.
   - In plant-a6, 32 is **38.6 kmol/h against the paper's 289 (−87 %)**.
   - This follows from the same CO2 split as 39-REC and is part of the comparison. Suggested correction: add it.

### Nits

8. `methanol-co2-campos-2022.reactor-lhhw-u-assumed-062` says U 150 and 1000 move the outlet by "0.04 points". In the
   runs, U 150 and U 1000 differ by 0.021 points in methanol, at most 0.024 in any component, and 0.40 K. The README
   line 85 has the same figure; "about 0.02 points" is what the runs show.
9. `methanol-co2-campos-2022.paper-two-flashes-co2-recycle` cites "1.285 mol % CO2 in stream 28" (correct, Table S10).
   No evidence row holds that number. Add a block for stream 28 or cite it from an evidence row.
10. Failed rows without a symptom:
    - `ethyl-acetate-piotrowski-2021.col11-acid-purity-spec-062` (another root: 31 kmol/h at 99.90 %);
    - `….design-spec-column-distillate-415da41` (`BAD_INPUT`: variable not allowed);
    - `methanol-co2-campos-2022.column-purity-or-recovery-spec-062` (`OUT_OF_RANGE` inside the stated range).

    The symptom is optional, and none of the 7 terms fits "a specification met by a wrong root". Proposal 0003 says
    to add a term when a case shows one: worth raising with the maintainer.
11. `ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41` has symptom `purity-short`, but 2 of its 3
    runs failed: 260 with `OUT_OF_TIME` and 280 with `NO_CONVERGENCE`. Only 270 is purity-short.
12. `ethyl-acetate-piotrowski-2021.col11-more-stages-062`: the "+0.01 point" is measured from the unsettled 99.67 %
    answer at tolerance 3e-4, not from the settled 99.109 %. The row states the tolerance; adding "from the unsettled
    baseline" would prevent a misreading.
13. Register row `plant-gas-recycle-with-purge` names only "CHEPTA 0.6.2" in "seen in", although the 415da41 runs
    `plant-vl-*` and `rerun-plant-a6` also close the loop.
14. `tests/test_kb.py`: the "no matching rows" query moved from `methanol` to `benzene`. Benzene is in the component
    vocabulary, so the test will break when a benzene case is added. A component outside the vocabulary, or a
    combination no row has, would be stable. The `EXAMPLE_CASES` filter is sound: it pins the exact index lines to
    the rows that existed before the backfill.

### Not problems (checked, noted for the record)

- **The 5 new register rows fit:**
  - one problem per row, at the right level;
  - "seen in" counts 1 paper each;
  - routes and "None from a source" are honest;
  - the CHEPTA column matches the runs: u-reactor-U300 gives −0.2 % flow, −0.2 K and +0.11 points; 3.4 against
    18.5 mol % CO2 and −86 %; 31 iterations; the HE5 cross; the 415da41 results for M4 and M6.
- **The CO2-solubility row** (`open-co2-solubility-hp-flash`, register `sep-co2-dissolved-in-methanol-water`) is
  correctly kept as an unresolved property-method difference, not a capability request. Its consequences match
  plant-a6: 39-REC is 394 against 2,786 kmol/h.
- **Disagreements in the papers are recorded, not settled:** column 5 has 14 stages in the text but 8 in Table 1;
  column 11's water and acid balance; HE7 (24.2 MW against 19.75 MW derived); the reflux ratio's basis.
  - Figure 3 of the methanol article says "three reactor modules", but the supplement says six (each RPLUG block
    stands for three). The rows' "six" is right.
- **Failed attempts are kept** (0.6.1, 0.6.2 and 415da41), and each later engine version is a new row, not an edit.
- **`acid-feed-15c-062`** (`worked`) and **`col15-purity-spec-062`** (correct `OUT_OF_RANGE`) state their caveats.

## Spot check for the maintainer (2-3 items)

| # | Why chosen | Item | What to compare, and where |
|---|---|---|---|
| 1 | Largest effect on the results: the headline closed-plant purity | `ethyl-acetate-piotrowski-2021.open-reach-99.9-pct`, `….ds-start-distillate-250-260-415da41` (problem 1) | Stream S16 in `cases/ethyl-acetate-piotrowski-2021/results-chepta-main-415da41/plant62-settled-extr20C-ethanol6506.output.json` (99.666 %, 0.296 % water) against `new-plant-dsinit-dist260.output.json` (99.561 %, 0.399 %). Is 99.666 % the best settled closed answer, and is "stops at 99.56 %" wrong? Also README line 121. |
| 2 | Least sure: a convention, not a fact | `ethyl-acetate-piotrowski-2021.col11-acid-flow-140.5-415da41` (problem 2) | S16 in `…/results-chepta-main-415da41/new-iso-scds11-acid0.01-bottoms140.5.output.json`: 99.897 % ester, 0.066 % water, against the 99.9 wt% and 0.03 % limits (paper p.9, Section 3.4). Does a target met at two-decimal rounding count as `worked`? The answer decides problems 2 and 3. |
| 3 | Picked at random (uniform draw over the 92 new decision rows) | `methanol-co2-campos-2022.plant-purity-spec-415da41` | `cases/methanol-co2-campos-2022/results-chepta-main-415da41/plant-vl-share-warm-purity.output.json`: `NO_CONVERGENCE`, "inside the range ... the stage solver did not converge". And `vl-column-CO2-MeOH-H2O-purity.output.json`: 30-WATER 99.9850 mol % water, the paper's 99.985 (Table S10). I found this row correct. |

**Person spot check (items, date):** not yet done; for the maintainer to record.

If a spot-checked item turns out wrong, AGENTS.md requires a full recheck: the rows are corrected, then a new AI
review session (not this reviewer, not the builder) checks everything again and includes the corrected item in its
spot check.

## What was not checked

- Whether the CHEPTA results are physically right: no measured data were consulted (for example the CO2 solubility
  at 70 bar).
- The other EA rows already on main before this PR (the 3 October decisions and the 2 example rows). For example,
  `product-column-acid-at-paper-flow` still cites `ea-impurity-limits`.
- The index files beyond `kb.py check` reporting them current. Wall times, which I took from the READMEs.
