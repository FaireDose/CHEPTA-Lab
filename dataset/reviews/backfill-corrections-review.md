# Review of PR #31: the corrections to the plant backfill

**AI full check (Claude Sonnet 5.5, 2026-11-20).** A separate AI review session: it is not the builder of PR #28 or #31
and not the first reviewer (Claude Opus 5.5, `backfill-plants-review.md`). It is not a person's check. The person's
spot check (below) is still to do, and only the maintainer records it.

Reviewed: branch `claude/lab-backfill-plants` at commit `1adecfe`, against `main` (`ca68c70`). Scope: only the
corrections: the 13 correcting rows, the 3 in-place edits, the new correction path in `scripts/kb.py` with its tests,
the schema change and proposal 0003 section F. The 133 rows of PR #28 were reviewed in the first review and not rechecked.

## What was checked

- **Diff against main:** no record row was deleted, no existing outcome changed, and `outcomes.lock.json` only gained
  lines (no line removed). Of the existing rows, exactly 3 differ: `col11-acid-flow-140.5-415da41` (limits),
  `open-reach-99.9-pct` (limits, obstacle, mechanism) and `paper-two-flashes-co2-recycle` (one evidence id added).
- **The 13 correcting rows** (11 ethyl acetate, 2 methanol, listed below): every number in the rows' limits against
  the `.output.json` files of the case results folders (S16 mass fractions from the component flows and the
  CHEPTA molecular weights; loop iterations, residuals and tolerances; error codes; time limits; balances), and against
  the case README where the README is the stated source.
- **Status rule (maintainer, 2026-11-20): a purity meets 99.90 wt % when it rounds to 99.90 at the paper's
  precision.** Applied to each row, see the table.
- **The correction path:** read the whole diff of `scripts/kb.py`, `tests/test_kb.py`, `corpus.schema.json` and
  section F; then tried to misuse it (below).
- **Reran:** `python scripts/kb.py check` (index current), `python scripts/dataset_pipeline.py validate` (OK),
  `python -m unittest discover -s tests` (104 tests, OK).

### Correcting rows: numbers and status

| Row (prefix `ethyl-acetate-piotrowski-2021.` or `methanol-co2-campos-2022.`) | Result |
|---|---|
| `ds-start-distillate-250-260-415da41-c1` | Numbers agree. 99.520 / 99.561 % (250 / 260, `new-plant-dsinit-*` and `new-plant-ds-ethanol0.0004-*`, identical streams); 99.666 %, 0.296 % water, 0.038 % ethanol, 16 iterations, residual 3.66e-7, tolerance 1e-5, balance 6.4e-5 kmol/h for `plant62-settled-extr20C-ethanol6506`, the same in the 0.6.2 and 415da41 folders. `failed`/`purity-short` is right (99.67 and 99.56 round below 99.90). Problem 1 below. |
| `col11-acid-paper-flow-415da41-converges-140` | 99.922 %, water 0.044 %: agrees. Meets 99.90, `worked` follows the rule. |
| `col11-acid-paper-flow-415da41-purity-short-141-141.5` | 99.8725 % (141) and 99.8481 % (141.5), water 0.111 % at 141.5: agrees. They read 99.87 and 99.85: `failed` follows the rule. |
| `plant-paper-column-specs-415da41-c1` | All 9 run ids resolve. 4 `NO_CONVERGENCE` (R-bottoms and -wegstein stop in column 11; W-dist-warm and -col5iter100 stop at the reactor, 141.548 needed against 141.333 kmol/h in), 4 `OUT_OF_TIME` at 1,500 s (W-dist, R-bottoms-direct, R-bottoms-warm, R-purity-direct), 1 `PHASE_SPLIT` in column 5 (col5VL, iteration 7): all as stated. The row keeps symptom `no-convergence` for all 9. Problem 5. |
| `plant-variant-w-both-round-flows-062-c1` | 99.465 % ester, 4 iterations, residual 4.99e-4, tolerance 5e-4, material balance 2.23 kmol/h (the README's 42 kg/h): agrees. `failed`/`recycle-drift` matches the sibling `plant-purity-specs-loose-tolerance-062`. |
| `col5-reflux-scan-415da41-c1` | All 12 run ids resolve and all 12 end `ok`. On 0.6.2 exactly 4 of the 12 fail (paper 45,000 and 70,000; r2 45,000 and 55,000): "the 4 that failed on 0.6.2" is right. |
| `col5-reflux-scan-meets-limit-062-c1` | Acid in stream 8: 0.00358 % (55,000), 0.00042 % (60,000), 0.00044 % (65,000), 0.0552 % at 50,000 (misses 0.005 %): agrees. Run ids 55, 60 and 65 thousand exist; 50,000 cited by path in the text. `worked` is right for these three. |
| `col11-distillate-260-280-settled-415da41-dist260` / `-dist270` / `-dist280` | 260: `OUT_OF_TIME` at 3,400 s, iteration 23, change 7.67e-4: agrees. 270: converged, 99.2232 % ester, 0.6987 % water: agrees. 280: `NO_CONVERGENCE`, column 15 cannot keep 99.99 % water: agrees. Symptoms `slow`, `purity-short`, `no-convergence` are right. |
| `col11-more-stages-062-c1` | 36 and 38 stages: 99.675 and 99.680 % at tolerance 3e-4, one loop iteration; 40 stages `NO_CONVERGENCE`: agrees. The "unsettled" wording is right. |
| `plant-closed-062-c1` (methanol) | 31 iterations; 31-MEOH 4548.3 kmol/h, 99.728 %; 30-WATER 99.999 %; 36-REC 52,898 against 51,504 (+2.7 %); stream 32 38.556 kmol/h against the paper's 289 (-87 %); 39-REC 394.5 against 2786 (-85.8 %): agrees (the row writes 395, see nit). `worked` is right: 99.728 % methanol meets the paper's 99.67 mol %. |
| `reactor-lhhw-u-assumed-062-c1` (methanol) | The U 300 numbers agree. **The correction itself is wrong,** problem 2. |

### In-place edits

- `open-reach-99.9-pct` (`lab_inference`, not locked): the new text agrees with the runs (99.666 % and 99.561 %), and
  the limits say it was a plain edit and why. Allowed by section F.
- `paper-two-flashes-co2-recycle` (`paper_simulation`): adds `ev-column-feed` for the 1.285 mol % CO2 in stream 28.
  Allowed. I did not recheck that evidence row's source fragment (first review, PR #28).
- `col11-acid-flow-140.5-415da41` (`chepta_run`, **locked outcome**): only `limits` changed; the outcome (status,
  basis, run ids, engine) is identical, so the lock holds. 99.8969 % ester, 0.0664 % water, 0.0221 % acid agree. The
  maintainer's rule makes `worked` right (99.8969 rounds to 99.90). The new note records the decision as "relayed by
  the Lab coordinator", not as the maintainer's own words; the maintainer should confirm it (the first review's
  record line says the same). The water 0.066 % above the 0.03 % limit is stated.

## Problems found

Severity: **major** means the correction path or a correction can mislead on a result that matters. **Minor** means
inaccurate or incomplete but the conclusion stands. **Nit** means wording or bookkeeping.

### Major

1. **The correction path cannot be used to edit or delete a locked outcome, but it can be used to hide one silently**
   (`scripts/kb.py`, section F). The lock covers only `keys.outcome` of CHEPTA-run rows and `informed_by`. `corrects`
   and `correction_reason` are not locked, and `check_keys` does not look at what a correcting row is. I tried each of
   these on a copy of the loaded corpus; `check_keys` and `lock_errors` returned no error in any of them:
   - An unrelated row (a methanol `paper_simulation` row) given `corrects:
     ethyl-acetate-piotrowski-2021.plant-purity-specs-loose-tolerance-062` withdraws that locked failed row from the
     counts and the disputes. Nothing requires the correcting row to share the target's case, problem id, operation or
     objective, nor to be a CHEPTA-run row (which would at least lock it).
   - `corrects` and `correction_reason` deleted from an existing correcting row (for example
     `plant-variant-w-both-round-flows-062-c1`) restores the withdrawn row, with no lock error: the corrected row
     comes back as current. The reverse, adding `corrects` to an old row, also passes.
   - A cycle of three (A corrects B, B corrects C, C corrects A) is accepted and withdraws all three, although the
     rule says "two rows cannot correct each other" (only a 2-cycle is checked).
   - The section F text says "the lock check still refuses any silent edit or deletion". That holds for the outcome
     of the corrected row, not for the correction itself.
   - `tests/test_kb.py` has no test for these cases, and the tests cover only a correction that clones the target.
   - What it would take: add `corrects` and `correction_reason` of CHEPTA-run rows to the lock (they are then
     append-only like `informed_by`); require the same case (id prefix) and the same `problem_id` or
     `operation_type` as the target; refuse any cycle, and refuse a correction whose target is itself a correction
     of the correcting row; add tests; and make section F say what the lock covers. Not done here, as instructed.
   Nothing in PR #31's own corrections uses these gaps: all 13 correcting rows are in the same case as their target, and
   all 13 are CHEPTA-run rows (so their outcomes are locked and in the lock file); I did not check problem id or
   operation for each, only that the targets are the rows the reasons describe.

2. **`methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c1` withdraws a roughly correct row for a reason the runs do
   not support.** The corrected row said U 150 and 1000 move the outlet "by 0.4 K and 0.04 points". The correction
   reason says "about 0.02 points (0.021 in methanol, at most 0.024 in any component)". From
   `u-reactor-U150` and `u-reactor-U1000` (stream `out-out`, mol %):

   | Component | U 150 | U 1000 | Difference |
   |---|---|---|---|
   | H2 | 59.984 | 60.019 | **0.035** |
   | CO2 | 17.793 | 17.807 | 0.014 |
   | CO | 1.761 | 1.758 | 0.003 |
   | Methanol | 7.540 | 7.519 | 0.021 |
   | Water | 7.263 | 7.240 | 0.023 |
   | N2 | 5.659 | 5.657 | 0.002 |
   | T (K) | | | 0.40 |

   The largest move is 0.035 points (H2), which the original "0.04 points" states to one significant figure. The new
   limits say "about 0.02 points (0.021 in methanol)", which understates the largest component. The first review's
   nit 8 (U150 against U1000 in methanol only) was applied without checking the other components. Suggested:
   withdraw the correction or add a new row that gives all components, saying "up to 0.035 points (H2), 0.021 in
   methanol, 0.40 K", with `correction_reason` fixed. Because the corrected row is locked and the correcting row
   is a CHEPTA-run row, this needs another correcting row (`-c2`).

### Minor

3. **`ds-start-distillate-250-260-415da41-c1` cites 99.666 % without its run id.** The `run_ids` are the four
   99.52 / 99.56 % runs; `plant62-settled-extr20C-ethanol6506` appears only in the text, and the headline number of the
   correction is not in the row's locked run list.
   Suggested: a correcting `-c2`, or a separate worked/failed row for the 99.666 % run with its id (both folders).
4. **`plant-paper-column-specs-415da41-c1` is one row with symptom `no-convergence` for 9 runs of 3 kinds** (4
   `NO_CONVERGENCE`, 4 `OUT_OF_TIME`, 1 `PHASE_SPLIT`). Item 11 of the first review was split by run; this one was not,
   so the index counts the 4 time-outs under no-convergence. The text is accurate; the symptom is the coarse part.
5. **`col11-acid-paper-flow-415da41-converges-140` keeps symptom `no-convergence` on a `worked` row.** It is the symptom the
   row addresses (the convergence failure at 0.6.2), so it is consistent with the other rows, but the row now reads as a
   success under a failure symptom in `kb.py query`.
6. **The note on `col11-acid-flow-140.5-415da41` and the same status of `-converges-140` both leave the water limit
   (0.03 %) unmet while `worked`.** This follows the maintainer's ruling for 140.5, whose objective is the purity only.
   Not an error; the reader should know that "worked" here is the purity target.

### Nits

7. `plant-closed-062-c1` writes "39-REC 395": the run gives 394.47 kmol/h (the README says 395 in one table and 394.5 in
   another; the first review said 394). Use 394.
8. `plant-closed-062-c1` gives 30-WATER as 99.999 %; the README says 99.9995 %. Both are the same at the paper's
   precision (99.985).
9. The `corrects` pattern in the schema allows any id string; the existence check is in `kb.py`, so
    `dataset_pipeline.py validate` alone does not catch a wrong id. Only `kb.py check` does.

## Spot check for the maintainer (2 items)

| # | Why chosen | Item | What to compare, and where |
|---|---|---|---|
| 1 | Largest effect on the results; a corrected item | `ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41-c1` (replaces the headline closed-plant answer) | Stream S16 in `cases/ethyl-acetate-piotrowski-2021/results-chepta-main-415da41/plant62-settled-extr20C-ethanol6506.output.json` (99.666 % ester, 0.296 % water, tolerance 1e-5, 16 iterations) against `new-plant-dsinit-dist260.output.json` (99.561 %). Is 99.666 % the best settled closed answer? Also whether a corrected number that is not in `run_ids` is acceptable (problem 3). |
| 2 | Least sure: the one correction I disagree with | `methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c1` (problem 2) | The `out-out` stream in `cases/methanol-co2-campos-2022/results-chepta-0.6.2/u-reactor-U150.output.json` and `u-reactor-U1000.output.json`: H2 59.984 against 60.019 mol %. Does "the outlet moves by 0.04 points" (the original) or "about 0.02 points" (the correction) describe it? |

**AI full check (Claude Sonnet 5.5, 2026-11-20).** Person spot check: not yet done; to be recorded by the maintainer
with the items and the date. Not recorded here on the maintainer's behalf.

If a spot-checked item is wrong, AGENTS.md requires a full recheck: the case is corrected, then a new AI review
session (not this reviewer, not the builder) checks everything again and includes the corrected item in its spot check.

## Follow-up check (Claude Sonnet 5.5, 2026-11-21)

Checked: `claude/lab-backfill-plants` at `e894f86` merged into this branch. `python scripts/kb.py check` (index
current) and `python -m unittest discover -s tests` (108 tests) pass. Only whether my findings are fixed was checked;
the new rows' numbers were compared with the run outputs where they changed.

| Finding | Result |
|---|---|
| Major 1, attempts a-d, rerun on a copy of the corpus | **Fixed.** (a) an existing methanol row given `corrects` on an EA row: refused twice (other record file; added to an indexed row). The same with an existing EA row: refused by the lock. (b) removing or editing `corrects`/`correction_reason` of an existing correcting row: lock error. (c) a 3-cycle: refused by `check_keys` and the lock. (d) deleting a correcting or a corrected row, or editing a corrected outcome: lock errors. `dataset_pipeline.py validate` also refuses an unknown target. Section F now says what the lock covers and does not. |
| Major 2 | **Fixed** by `reactor-lhhw-u-assumed-062-c2`: all six components and 0.40 K listed, H2 0.035 points; the numbers match the runs. |
| Minor 3 | **Fixed** by `ds-start-distillate-250-260-415da41-c2`: `plant62-settled-extr20C-ethanol6506` is now in `run_ids`. |
| Minor 4 | **Fixed**: split into `-c1-no-convergence` (4 runs), `-c1-slow` (4 runs, OUT_OF_TIME) and `-c1-wrong-phase` (col5VL, PHASE_SPLIT); the run sets and texts match the outputs. |
| Minor 5 | **Fixed** by `col11-acid-paper-flow-415da41-converges-140-c1` (symptom dropped). |
| Minor 6 | Unchanged on purpose (water limit, pending the maintainer). |
| Nits 7, 8, 10 | **Fixed**: `plant-closed-062-c2` gives 394.47 and 30-WATER 99.9994 % (run: 99.99944). The validator now checks the target. Nit 9 was withdrawn from the note. |

One gap remains, not a regression: a **new** correcting row in the same record file is checked only for existence, a
reason, no cycle and the same file. Nothing requires the same problem or operation as the target (a test row for a
different problem, `plant-recycles-makeup-purge`, was accepted at `check`). Once the row is indexed the lock protects it,
and the change is visible in the PR diff, so the review of the new row is the control. Minor.

## What was not checked

- Whether the CHEPTA results are physically right (no measured data consulted).
- The source passages of the 133 rows of PR #28 (the first review did that), the unchanged rows and the regenerated
  index beyond `kb.py check` reporting it current.
- That the 0.6.2 and 415da41 copies of a run are identical beyond the streams, loops and input hash I compared for
  `plant62-settled-extr20C-ethanol6506` (same input hash, same S16, different wall time).
- The held-out status of any row: the index hides held-out groups and none of the corrected rows is in one.
