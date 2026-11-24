# Proposal 0003: the knowledge base for process design

Status: draft for the maintainer's decision, 2026-11-20; amended the same day so that knowledge from books and
reviews (rules, heuristics, worked examples) enters on the same keys (section E). Implemented as a draft: [vocabulary](../../data/vocabulary.json),
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
| `kind` | `case-decision`, `design-rule` or `simulation-rule` (section E) | The vocabulary |
| `problem_id` | A row of the register (required for case decisions, optional for design rules, never for simulation rules) | The first column of [data/ISSUES_AND_ROUTES.md](../../data/ISSUES_AND_ROUTES.md) |
| `level` | separation, reaction or plant, with `problem_id` | The vocabulary, and the register row's own level |
| `symptom` | Simulation symptom (required for simulation rules, optional otherwise) | The vocabulary |
| `operation_type` | distillation, extraction, decanter, ... | The vocabulary |
| `components` | CHEPTA component names (`ethyl-acetate`, not `ethyl acetate`); may be empty for a rule | The vocabulary, seeded from the case results |
| `behaviours` | azeotrope-min-boiling, two-liquid-phases, ... | The vocabulary |
| `conditions` | Short tags for what makes this row's situation specific (feed, flow, standalone or in the plant, acid present) | Lower-case tags; free, not controlled (see "To decide") |
| `objective` | Optional: product and targets; each number names the evidence row that holds it | The number must be a quantity of that evidence row |
| `outcome` | `status` (worked, failed, untested, lead), `basis` (measured, paper_simulation, chepta_run, lab_inference, textbook), `run_ids`, `engine` | Rules below |
| `source`, `statement` | For rules: catalogue source id and locator; Lab's own paraphrase | Section E |
| `informed_by` | Optional, append-only: rows that informed this one, each with helped yes/no/partly and a note | Must exist; locked |
| `record_status` | `draft` (the only value today: decisions have no review path yet) | |
| `disputed_with` | Optional: rows this one disagrees with | Must exist |

Outcome rules: a CHEPTA outcome names its engine (`chepta@0.6.2`) and its runs; a run is either a corpus run id or
`cases/<case>/<results folder>/<run>` whose `.output.json` exists, and a run in `results-chepta-X.Y.Z` must carry
engine `chepta@X.Y.Z`. A Lab inference can only be untested or a lead (the register's rule: a route counts as usable
only when a paper or a CHEPTA run shows it). Evidence rows may carry optional keys (`problem_ids`, components,
behaviours) so a passage can count for a problem without a decision.
An outcome is judged against the objective the row names; every other limit it misses is stated in the row with its
source, and is never generalised into a rule without the application's specification (the maintainer, 2026-11-21).

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
  listed (`python scripts/kb.py disputes`) and counted in the index. Rows that name each other in
  `disputed_with` count as a disputed set whatever their status, so a disagreement between two leads (two books'
  rules) is counted too (amendment, 2026-11-20). A paper that worked and a CHEPTA run that failed
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
| 2 | [dataset/index/problems.md](../../dataset/index/problems.md): problems, then operation × symptom, then general rules by operation; or only matching problem lines: `kb.py problems --behaviour ...` | ~500 tokens | ~30 tokens a line: ~9,000 for 300 problems, plus at most operations × symptoms (20 × 7) and one line per operation; a few hundred filtered |
| 3 | `kb.py query --problem ... --status ...` or `--operation ... --symptom ...`: three lines a row with ids, conditions and locators | ~160 tokens a row | at most 20 rows by default, ~3,000 |
| 4 | `kb.py show <id>`: one row with its evidence and locators | ~1,300 tokens | the same |
| 5 | The record file itself, only to edit your own case | pilot.json ~7,700 tokens | one case's file |

The index grows with the number of problems and operation × symptom pairs, not rows (tests check both). It is generated, never edited:
`python -m unittest` fails when it is stale, so any change to records or the register forces `kb.py index`.

## E. Knowledge from books and reviews (amendment, 2026-11-20)

The maintainer wants rules, heuristics and worked examples from books and papers on process development and
simulation in the same knowledge base, not only what Lab's own cases showed.

- **Three row kinds.** `case-decision` is what we had. `design-rule` is a general rule or worked example on choosing
  operations (for example "relative volatility below about 1.1: consider extractive distillation"); it is keyed by
  behaviours, operation and condition tags, and by a register problem only when it is about one. Rules with no
  problem get their own index section, one line per operation. `simulation-rule` is how to make a unit or plant
  converge or meet a target (for example from the ChemSep book); it never belongs to a register problem.
- **Basis `textbook`**, for rule rows only: a book's or review's rule or worked example, with a chapter, section,
  page, table or example locator. A rule without results of its own is a `lead`. A worked example can be `worked` or
  `failed` only when it cites the evidence row that holds its numbers.
- **Simulation rules are keyed by operation and symptom.** Symptoms are controlled: `feed-refused`, `section-fails`,
  `recycle-drift`, `purity-short` (the four rows of the troubleshooting table in
  [docs/SIMULATION_PRACTICES.md](../SIMULATION_PRACTICES.md)), plus `no-convergence`, `wrong-phase` and `slow`, which
  name CHEPTA outcomes seen in the cases. A case row may carry a symptom too, so what a case tried for a
  non-converging column sits next to the book's advice. The index's second section has one line per operation and
  symptom; `kb.py query --symptom` reads it.
- **Usefulness.** The coordinator asked for an append-only `used_in` list on the rule. It is stored the other way
  round: the case row that was informed records `informed_by: [{row, helped: yes/no/partly, note}]` in its own file,
  and `kb.py show` and the index derive the rule's `used_in` (case, row, helped, note) from those. Why: a worker then
  edits only its own case file, so two workers using the same rule never edit the same file and never collide. The
  lists are append-only through the lock: an entry once indexed cannot be edited or removed. The index counts uses
  (helped yes / partly / no) per problem, per operation and symptom, and per general rule.
- **Rights.** A rule row holds Lab's own short paraphrase (`statement`, at most 2 sentences and 300 characters, no
  quotation longer than 6 words) and the locator, never copied text. Its source must be in `data/sources.json` with a
  rights status; a statement without a source is refused. A source still `needs_review` may be cited in the knowledge
  base but its rows stay out of releases.
- **Example rows (draft, one each):** a design rule from the review section of Piotrowski & Kubica 2021 (p. 3:
  extractive distillation and pervaporation are named for the ester azeotrope but each needs a second method; a lead)
  and a simulation rule from the ChemSep book (a column that converges but misses a target: check balances and stage
  profiles; a lead, as cited in the troubleshooting table, the book not opened by Lab). The two chepta 0.6.2 example
  rows now carry the symptom `no-convergence`. No other book content is added.

- **Plain fields for people (amendment, 2026-11-21).** The maintainer found the rules unreadable. A rule row may
  carry `keys.plain`: `title` (one action line, the way a senior engineer would say it), `when`, `do`, `why`,
  `check` (in CHEPTA where it applies), optional `result` and `note`. `kb.py check` refuses "the paper", "the
  authors" or "the review" without a name, row ids, fields over 450 characters (title 140), and any number that is
  not in the row's statement, limits, evidence or locator, or in a `note` naming the passage Lab reread;
  `note: "source not reread"` marks a row written from the statement alone. `rules-readable.md` renders these rows
  as title, the five lines, a plain status and "Source: Author Year, *short title* (link), locator"; other rows keep
  the one-line form. problems.md, problems.json and `kb.py query` are unchanged, so agents read as before.
- **Pages for people by topic (amendment, 2026-11-21).** `rules-readable.md` is a short front page: how to read,
  then a table of topics with a line on each and its number of rules. `kb.py` puts every plain rule on exactly one
  page under `dataset/index/rules/`, by the first topic in `TOPICS` its keys match (symptom for simulation rules,
  then operation; safety by its condition tag), best-supported first, at most `TOPIC_MAX` (30) rules a page (a test
  enforces it: split a topic when it grows). Rules not yet in plain words get their own page. Case decisions go to
  `dataset/index/plants/<case>.md`, grouped by unit and marked as a run log, not yet lessons. Row ids are in HTML
  comments. The stale-index test covers every page, and refuses leftover pages.

## F. Corrections (amendment, 2026-11-20)

PR #28 was merged before its AI review (PR #30) finished, so some wrong outcomes were already in the append-only
lock. A locked row is never edited; it is corrected by a new row:

- The correcting row carries `keys.corrects: <row id>` and `keys.correction_reason` (why, citing the review note).
  Checks (`kb.py check`; the target's existence also in `dataset_pipeline.py validate`): the target must exist, must
  not be the row itself and must be in the same record file; a reason is required; corrections must not form a
  cycle of any length (a chain, where a correction is itself corrected, is fine). Several rows may correct one row
  (a split).
- `kb.py` treats the corrected row as **withdrawn**: left out of the counts, the current rows and the disputes,
  counted as `withdrawn` in `problems.json`, struck through on the topic and plant pages under `dataset/index/` ("corrected by a later row", with both ids in the row's HTML comment; the correcting row shows its reason), and
  marked `WITHDRAWN` in `kb.py query` (`corrected_by` in `show` and `--json`). It stays in the record file unchanged.
- **What the lock protects** (`dataset/index/outcomes.lock.json`, written by `kb.py index`): the outcome of every
  CHEPTA-run row, every `informed_by` list, every correction (`corrects` with `correction_reason`) and the ids of
  all indexed rows. After indexing, editing or removing a locked outcome, an `informed_by` entry or a correction
  fails `kb.py check`, and so does adding `keys.corrects` to a row that was already indexed. The lock does not
  protect a row's text (`limits`, `operation`, ...) or the outcome of a row that is not a CHEPTA run; those may be
  edited in place, and the row's limits say so.
- Tests (`tests/test_kb.py`): a correction passes and keeps the corrected row; an edit or deletion of the corrected
  row still fails; a correction to a missing row, to itself or without a reason is refused; the counts move as
  expected; a correction from another record file is refused; changing, removing or adding a correction after
  indexing fails; a cycle of three is refused; `dataset_pipeline.py validate` refuses an unknown target.

## G. Lessons from Lab's own plants (amendment, 2026-11-21)

The plants' run logs record every attempt; a senior engineer needs what they taught. A **lesson** is a case-decision
row of the plant's own record file that summarises several of its rows:

- `keys.summarises` lists the rows (at least two, all in the same record file, none of them a lesson). Its
  `plain` fields (title, When / Do / Why / Check / Result) are required, and every number in them must appear in
  the lesson's own text or in the rows it summarises. Its `run_ids` must be runs of those rows, from one engine,
  so its status is the outcome of the action it recommends on those runs.
- `keys.objective.judged_on` says in plain words what the status was judged against. Every other limit the runs
  miss is stated there or in the result, with its source, and never generalised (the maintainer, 2026-11-21).
- A lesson is not counted again in the index (W/F/L/U count the rows it summarises; `problems.json` gives the
  number of lessons). Locked rows are neither withdrawn nor edited: they stay in the run log as the evidence.
- The plant page `dataset/index/plants/<case>.md` lists the lessons first, grouped by unit, then the run log under
  "Runs behind these lessons". A lesson with the condition tag `applies-beyond-plant` also appears on its topic page,
  marked "From Lab's own plant", placed as a simulation rule if it has a symptom, else as a design rule.
- Papers named in any plain field must be catalogued sources, written as the page cites them ("Piotrowski &
  Kubica 2021"); `kb.py check` refuses others, and the pages link each name to its DOI. The paper-design rows of the
  two plants carry plain fields too.
- Tests: a lesson passes and renders first; unknown, foreign or lesson rows in `summarises` are refused (also by
  `dataset_pipeline.py validate`); a run or a number not in its rows is refused; `judged_on` is required; lessons
  do not change the counts; an uncatalogued paper name is refused.

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
5. **Which books first, and their rights.** The ChemSep book is `needs_review` (public domain per CHEPTA's
   record, not checked by Lab). Recommendation: before adding book rules, the maintainer picks 2 or 3 books or reviews
   with clear rights, and Lab adds rules only as they bear on the next two plants, recording `informed_by` so their use
   can be judged afterwards.
6. **Symptom list.** Seven terms, four from the troubleshooting table. Recommendation: keep them until a case shows a
   symptom none of them fits, then add one.
7. **Automatic reading.** The skills tell agents to read the index first; the stale-index test makes it current.
   Recommendation: if sessions still skip it, add a session-start hook that prints `kb.py problems` filtered by the
   case's components.
