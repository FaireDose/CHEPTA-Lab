# Proposal 0002: the study record

Status: draft for the maintainer's decision, 2026-11-11. Answers CHEPTA ROADMAP rule 5 ("a small shared study record"). Implemented as a draft: [schema](../../dataset/schemas/study-record.schema.json), [validator](../../scripts/study_record.py), [tests](../../tests/test_study_record.py) and one [worked example](../../cases/ethanol-zsm5-573k/study-record.json). Nothing here is reviewed by a person.

## What a study record is

A study is one engineering question worked on with CHEPTA: for example "how much does including the Table-12 adsorption terms change ethanol conversion at 573.15 K?". The study record is one JSON file, written by Lab, that hands the whole study to CHEPTA's design-study view (G6): which case and papers, which CHEPTA, what was asked, what came back, what was checked, what was assumed, what is still missing and who has reviewed it.

It is an **index, not a copy**. CHEPTA's request and result files stay exactly as CHEPTA wrote them; the record names each file with its path and its sha256 hash. A number that CHEPTA or a Lab check produced is never typed into the record: the record holds a *pointer* to where it sits in the file (for example `/value/streams/product/T_K` in a result file). If any file changes by one byte, the hash no longer matches and the validator fails.

## The fields

| Field | What it holds | Why |
|---|---|---|
| `study_record` | Format version (now 1) | A reader refuses a version it does not know |
| `id`, `case_id`, `title`, `question`, `status` | Study name, the Lab case, the question asked; `draft`, `accepted` or `withdrawn` | One case can hold several studies |
| `sources` | Source ids from `data/sources.json`; evidence ids from the canonical corpus | Reuses Lab's existing source blocks and evidence ids; no new citation format |
| `files` | Every file the study relies on: path, sha256, role (request, result, runner, manifest, Lab check, source ledger, case input, cost result) | Binds the record to exact bytes |
| `engines` | CHEPTA release (or a full commit between releases, saying so), the request path `CHEPTA.run`, contracts version, result format (`chepta_result`) | ROADMAP rules 1 and 6: old runs keep their engine |
| `variants` | Model variants, each with its declared modifications: simplified model, substituted unit, opened recycle, relaxed target, changed input | P6 asks that these be recorded |
| `runs` | One entry per CHEPTA call: variant, engine, interface (library, command line or MCP server), the request file, the result file (or none, with a failure note) | Several runs, failures included |
| `values` | Inputs and outputs worth naming, each with a class (below), a pointer into a file and its unit | Keeps the five kinds of number apart |
| `constraint_declaration`, `constraints` | Product and operating limits, where they are read in the result, the limit and tolerance with their origin, and when they were declared | P6: "meets the constraints declared before the run" |
| `constraint_results` | For each constraint and run: met, not met or not evaluated | The validator recomputes every verdict from the files |
| `checks` | Lab's own checks (for example an independent ODE solution), pointing into the check file | CHEPTA's own residuals stay in its result's `checks` |
| `warning_notes` | Where the warnings sit in each result, and Lab's reading of them | Warnings are not copied; G6 reads them from the result |
| `assumptions`, `unresolved_inputs` | Model assumptions; missing or ambiguous inputs, each marked blocking or not, with the next action | Missing information stays visible |
| `cost_coverage` | `not_costed`, `complete_within_scope`, `partial` (with what it excludes) or `unavailable` | ROADMAP cost rules; nothing more about costs |
| `corpus_links` | Ids of related training tasks and replayed runs in `dataset/records/pilot.json` | The validator checks that they use the same files |
| `reviews` | The existing review shape (scope, reviewer, human or agent, decision, digest, date, notes) | A review is bound to the study digest; any later edit voids it |
| `limitations` | What the study does not show | Plain statements for the reader |

## Five kinds of number

| Class | Meaning | What the record must also state |
|---|---|---|
| measured | A measurement from a source | Source id and exact locator |
| published | A value a paper reports (fitted parameter, author's simulation, stated condition) | Source id, locator, the value as printed and any conversion |
| assumed | A choice made by Lab or by the upstream example | The reason |
| simulated | A CHEPTA output | Pointer into that run's own result file; nothing else allowed |
| derived | Calculated by Lab from other values | The method (script and formula) and a pointer to the stored result |

Every value, of every class, is a pointer into a hashed file; even published inputs are pointers into the case input file, whose source is cited. The only literal numbers in a record are the limits and tolerances of declared constraints, each with its own origin (published with a locator, or assumed with a reason).

## Constraints: declared before, compared after

Before a run, Lab writes each product or operating constraint: what is limited (for example ethylene purity in stream `product`), where to read it in the result (a pointer), the operator (equal within a tolerance, at most, at least, between), the limit and its origin, and the declaration date. After the runs, the record states a verdict per constraint and run. The validator reads the observed number from the file and refuses a verdict that disagrees. A failed run gets `not_evaluated` with a note, never `met`.

The validator also refuses `before_runs` if the declaration date is later than a run's execution date. A study whose constraints were written afterwards says `reconstructed_after_runs` and cannot be accepted as a P6 demonstration. The ethanol example is honestly marked this way.

## What it leaves out

No interface state (layout, positions, selected tabs, workbench settings: the schema refuses unknown keys). No copied numbers, warnings or result text. No new property data or parameters (CHEPTA's own provenance applies). No cost detail beyond coverage. No mapping to other plant-file formats, no Process Atlas, no evaluation or training material. A study record does not make anything training data; tasks keep their own gates in the corpus.

## Several runs, re-runs and versions

One study holds all its runs: variants, operating points, failures. A re-run on a new CHEPTA release is added as new runs with a new engine entry and new result files, kept beside the old ones; the old runs are never overwritten (ROADMAP rule 6).

**Versioning rule.** The format number (`study_record`) increases whenever a change would make an older reader reject or misread a record; old records keep their number and are never edited to upgrade them. A record that replaces another names it in `supersedes` (path and sha256). Acceptance is bound to the study digest (sha256 of everything except reviews and status), so any edit after review needs a new review.

## The worked example

[cases/ethanol-zsm5-573k/study-record.json](../../cases/ethanol-zsm5-573k/study-record.json) indexes the existing six runs on CHEPTA commit c1adf6b without changing them: 19 files, 39 values, 4 constraints with 24 verdicts (all `met`, recomputed from the files), 6 independent checks, 4 assumptions and 4 unresolved inputs (the pressure-unit convention blocks acceptance). The validator lists why it is not acceptable: no human reviews, constraints reconstructed after the runs, one blocking unresolved input.

Checked: `python scripts/study_record.py`, `python scripts/dataset_pipeline.py validate` (now also checks study records), `python scripts/validate_catalog.py`, `python -m unittest discover -s tests` (39 tests, 19 new). Not checked: that G6 can display it (G6 does not exist yet), and anything on chepta@0.6.0.

Found while converting: the manifest's `request_sha256` is the hash of a compact re-serialization, not of the request file on disk. The study record uses the file's own hash; the manifest is unchanged.

## Questions for the maintainer

| # | Question | Recommendation |
|---|---|---|
| 1 | Where do the records live: next to each case (`cases/<case>/study-record.json`) or in one folder? | Next to the case, as here; the validator finds them all |
| 2 | The chepta@0.6.0 re-run of ethanol (separate pull request): new runs in this same record, or a new record that supersedes it? | Same study, new runs with a second engine entry, written to a new results folder (for example `results-0.6.0/`) so the old files and their hashes stay. If that pull request rewrites `results/`, this record's hash check fails, which is the intended alarm; whichever merges second updates the record |
| 3 | Which reviews must a study have before `accepted`? | Human engineering, source accuracy and rights, each on the current digest, as now; a review by another model is recorded as `agent` and never counts (rule 7) |
| 4 | Should CHEPTA own a copy of this schema for G6? | No copy: CHEPTA reads the schema from a pinned Lab commit and refuses unknown format numbers; agree a change policy like the project format's |
| 5 | Do tolerances on equality constraints need a source? | Allow `assumed` with a stated reason (as in the example), but a person checks them at engineering review |
| 6 | Should the study record also carry measured performance values for comparison with experiment? | Yes, later, as `comparison_with_source` checks once a case has experimental data; no field change is needed |
