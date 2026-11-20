# Proposal 0003: the knowledge base for process design

Status: draft for the maintainer's decision, 2026-11-20. Implemented as a draft: [vocabulary](../../data/vocabulary.json),
keys in the [corpus schema](../../dataset/schemas/corpus.schema.json), [kb.py](../../scripts/kb.py), the loader in
[dataset_pipeline.py](../../scripts/dataset_pipeline.py), [tests](../../tests/test_kb.py) and a generated
[index](../../dataset/index/problems.md). Nothing here is reviewed by a person.

## The aim

After about 200 plants the dataset should hold about 10,000 rows that an AI agent uses to propose a new process
quickly (the maintainer, 2026-11-20). Two requirements:

1. With 10,000 rows, entries must not conflict.
2. An agent does not read everything. It reads a short index first, then only the rows it needs, every time.

Until now two stores did not talk to each other: the issues and routes register (markdown, keyed by problem) and
`dataset/records/pilot.json` (blocks, evidence, decisions, runs, tasks).

## A. One key system for both stores

Every decision row now carries `keys`:

| Key | What it holds | Checked against |
|---|---|---|
| `problem_id` | A row of the register | The first column of [data/ISSUES_AND_ROUTES.md](../../data/ISSUES_AND_ROUTES.md) |
| `level` | separation, reaction or plant | The vocabulary, and the register row's own level |
| `operation_type` | distillation, extraction, decanter, ... | The vocabulary |
| `components` | CHEPTA component names (`ethyl-acetate`, not `ethyl acetate`) | The vocabulary, seeded from the case results |
| `behaviours` | azeotrope-min-boiling, two-liquid-phases, ... | The vocabulary |
| `conditions` | Short tags for what makes this row's situation specific (feed, flow, standalone or in the plant, acid present) | Lower-case tags; free, not controlled (see "To decide") |
| `objective` | Optional: product and targets; each number names the evidence row that holds it | The number must be a quantity of that evidence row |
| `outcome` | `status` (worked, failed, untested, lead), `basis` (measured, paper_simulation, chepta_run, lab_inference), `run_ids`, `engine` | Rules below |
| `record_status` | `draft` (the only value today: decisions have no review path yet) | |
| `disputed_with` | Optional: rows this one disagrees with | Must exist |

Outcome rules: a CHEPTA outcome names its engine (`chepta@0.6.2`) and its runs; a run is either a corpus run id or
`cases/<case>/<results folder>/<run>` whose `.output.json` exists, and a run in `results-chepta-X.Y.Z` must carry
engine `chepta@X.Y.Z`. A Lab inference can only be untested or a lead (the register's rule: a route counts as usable
only when a paper or a CHEPTA run shows it). Evidence rows may carry optional keys (`problem_ids`, components,
behaviours) so a passage can count for a problem without a decision.

The three October decisions are upgraded, not left as legacy: all three are keyed to
`sep-ester-alcohol-water-azeotrope` as the paper's own simulated route (worked, paper_simulation). Two example rows,
labelled draft, show a CHEPTA outcome: the ester product column with 0.01 mass % acetic acid under chepta 0.6.2 fails
at 140 to 141.5 kmol/h and works at 139 kmol/h (problem `sep-two-liquids-with-acetic-acid`). The ethyl acetate and
methanol plants are not otherwise added.

## B. Conflict rules, enforced by `python scripts/dataset_pipeline.py validate`

- **Controlled vocabulary** in `data/vocabulary.json`. Unknown terms are refused. Adding a term is a deliberate edit
  of that one file; renaming or deleting a used term breaks the rows that use it, so it cannot happen silently.
- **Namespaced ids.** Each record file other than the legacy `pilot.json` has its file name as its id, and every row
  id in it starts with `<file name>.`. Two workers on two cases can never pick the same id. Duplicates are still refused.
- **Disputes.** Rows with the same problem, operation and conditions are compared. If one says worked and another
  failed, the validator stops and lists both, unless one of them names the other in `disputed_with`. The fix is to
  name the condition that differs, or to record the disagreement; never to merge or delete. Acknowledged disputes stay
  listed (`python scripts/kb.py disputes`) and counted in the index. A paper that worked and a CHEPTA run that failed
  under the same conditions is a dispute on purpose: it is a disagreement to keep (AGENTS.md).
- **Engine versions.** Within the same problem, operation and conditions, a CHEPTA row of a later release supersedes
  an earlier one in the counts; it is not a dispute. Outcomes from CHEPTA runs are append-only: `kb.py index` records
  them in `dataset/index/outcomes.lock.json`, and editing or deleting one afterwards fails the checks. A new version
  adds a row. Correcting a genuine mistake means editing the lock by hand, which shows in the diff.
- **Held-out groups** (split `test`, AGENTS.md rule 7): a decision or evidence row belongs to the groups that hold its
  passages' sources. Rows touching a test group never appear in the index, the lock or any `kb.py` output.

## C. Files that scale

`dataset/records/<case>.json`, one file per case (or group), same layout as the corpus. The pipeline loads every file
in the folder and checks them together, so split leakage is still caught across files. A case's worker edits only its
own file; rows may cite evidence in other files. `pilot.json` stays as the legacy file holding both October groups.

## D. Reading, in order

| Layer | What | Size today | Size at ~300 problems / 10,000 rows |
|---|---|---|---|
| 1 | The skill (process-design ~1,300 tokens, building-cases ~900) | ~900-1,300 tokens | the same |
| 2 | [dataset/index/problems.md](../../dataset/index/problems.md), or only its matching lines: `kb.py problems --behaviour ...` | ~320 tokens | ~30 tokens a problem, ~9,000 in full, a few hundred filtered |
| 3 | `kb.py query --problem ... --status ...`: three lines a row with ids, conditions and locators | ~160 tokens a row | at most 20 rows by default, ~3,000 |
| 4 | `kb.py show <id>`: one row with its evidence and locators | ~1,300 tokens | the same |
| 5 | The record file itself, only to edit your own case | pilot.json ~7,700 tokens | one case's file |

The index grows with the number of problems, not rows (a test checks this). It is generated, never edited:
`python -m unittest` fails when it is stale, so any change to records or the register forces `kb.py index`.

## To decide

1. **Condition tags free or controlled?** Free tags let two workers describe the same condition differently, which
   hides a dispute. Recommendation: keep them free until about 20 cases, then list the tags that recur and control them.
2. **Should the register's markdown columns move into keyed rows?** Today the register keeps its prose and the
   dataset keys to its ids. Recommendation: keep both; the register is for people, the keys for agents. Generate the
   register's "seen in" counts from the index once the plants are backfilled.
3. **Where held-out cases live.** The index hides them, but their record files are still in this repository, where
   CHEPTA's sessions could read them. Recommendation: keep test-split record files out of this repository (a separate
   private one) before the first held-out evaluation.
4. **Review of decision rows.** `record_status` has only `draft`. Recommendation: reuse the task review path (AI full
   check plus a person's spot check) for decision rows when the plants are backfilled.
5. **Automatic reading.** The skills tell agents to read the index first; the stale-index test makes it current.
   Recommendation: if sessions still skip it, add a session-start hook that prints `kb.py problems` filtered by the
   case's components.
