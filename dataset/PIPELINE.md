# Evidence-to-training pipeline

Implemented pilot, 2026-10-30. There are **zero accepted training tasks**. This pipeline prepares data; it does not train a model or execute CHEPTA.

## Canonical records

[records/pilot.json](records/pilot.json) is the single canonical corpus for this pilot. Add new records to this corpus so split checks see all families and sources together. Do not create independently released corpora that bypass those checks. Every collection has stable IDs and is validated against [schemas/corpus.schema.json](schemas/corpus.schema.json).

| Collection | Contents |
|---|---|
| `blocks` | Source URL/version, document hash, exact locator, extraction selector/hash and known answer exposure |
| `evidence` | Claims, supporting blocks, classification, quantities with units/bases, conditions and limitations |
| `decisions` | Obstacle, mechanism, operation, expected change, alternatives and required verification |
| `runs` | Engine provenance and hashed request, response, manifest, runner, verification and tool-contract artifacts |
| `tasks` | Model-visible input, separate target/rubric, dependencies, blockers and revision-bound reviews |
| `groups` | Family/source grouping and explicit train/development/test assignment |

The source catalogue remains in `data/sources.json`; original process cases and normalized bases remain in `cases/` and `dataset/drafts/`. They are referenced research material, not automatically included training examples. Corpus schema v1 is separate from legacy case/template versions.

Source blocks identify paragraphs, equations, table cells or figure elements through their locators. This pilot annotates seven text blocks from the existing publisher HTML snapshot. It does not yet contain a general PDF parser or image extractor. The original HTML/text extraction software version was not recorded; that limitation is explicit. Document and fragment hashes identify the inspected snapshot, but the current validator cannot re-fetch and confirm the publisher content. Human source review remains required.

## Task-specific acceptance

Every released task requires an accepted status, no unresolved blockers, assigned split and human approvals for source accuracy, engineering, rights and context. A single engineering review can cover several scopes; each scope is recorded explicitly. Agent checks never impersonate a human reviewer.

| Claim/task | Additional requirement |
|---|---|
| Literature explanation | Claims supported by source passages; no invented author rationale; no simulation required |
| Conditional next-operation selection | State assumptions, missing specifications and applicability limits; allow defensible alternatives; no unsupported performance promises |
| Numerical benchmark/tool use | Actual request and response, execution manifest, tool contract, runner, engine provenance and numerical verification |
| Full process performance | **Blocked in this pilot.** A dedicated balance/specification/performance acceptance contract is still required |

Source-reported numerical values can appear as attributed evidence with units. They are not new CHEPTA results. A model-generated statement that a new design achieves a value belongs to a calculated-result task and must pass its execution checks.

Reuse CHEPTA's property models, parameter provenance and validation. Check applicability rather than routinely repeating phase-equilibrium validation. Convergence and numerical agreement alone do not establish physical accuracy.

## Review binding

The validator prints a `review_digest` for each task. It covers the task content, linked evidence/decisions/runs and source metadata. To review a task:

1. Resolve substantive blockers, revise the task and inspect its rendered preview.
2. Check sources, conditions, units, alternatives and context exposure; review the execution artifacts where required.
3. Record the actual reviewer, date, scope, decision, notes and current digest in `reviews`.
4. Set `status` to `accepted` only after all required checks and split assignment are complete.

Changing the target or a linked claim invalidates earlier approvals. Approval records are an audit trail, not cryptographic identity verification. These checks do not automatically establish that a person's scientific judgment is correct.

## Commands

From the repository root, with Python 3.10 or newer:

```bash
python -m pip install -r requirements-dataset.txt
python scripts/validate_catalog.py
python scripts/dataset_pipeline.py validate
python -m unittest discover -s tests
python scripts/dataset_pipeline.py preview --out /tmp/chepta-lab-review-v1
```

The preview contains `review-preview.jsonl`, `provenance.jsonl` and `manifest.json`. Each preview row is labeled `preview_only`, with its release blockers. **Do not train on previews.** A fresh output directory is required so old release files cannot remain beside a preview.

After there are genuinely accepted tasks and assigned groups:

```bash
python scripts/dataset_pipeline.py release --out /tmp/chepta-lab-release-v1
```

The command currently refuses because no task qualifies. It never promotes a draft. Accepted tasks with broken gates cause validation to fail, while ordinary drafts are listed as exclusions.

Training rows are written only to `train.jsonl`. Development and test examples have separate `*.inputs.jsonl` and `*.targets.jsonl` files: learner inputs contain neither reference answers nor future tool observations. Provenance stays in a sidecar. The manifest records corpus/source/schema/exporter hashes, group assignments and output hashes. Identical content and exporter produce identical output; no current timestamps are injected.

The chat format is a model-neutral intermediate export. Before training, adapt it to the selected model's chat template and tool support; verify assistant-only loss masking and token limits. Tool outputs are observations, not invented targets. No trainer integration is claimed yet.

## Actual tool observations

The ethanol example reconstructs one call/result pair from the already executed `upstream_simplified-wf0.38` benchmark. It is explicitly a historical replay, not an autonomous-agent session. The user input supplies the calculation request, so it demonstrates dispatch and interpretation rather than independent flowsheet construction.

The exporter loads the full original response, including nested stream warnings. It verifies artifact hashes, manifest paths, capability and reported numerical-check status. These integrity checks do not rerun the simulator or independently repeat the numerical integration.

`contracts/chepta-run.v1.json` describes a function-shaped wrapper around CHEPTA's JSON dispatcher. It is an export contract, not a hosted endpoint or installed chatbot integration. A future runtime adapter must call the actual pinned engine and return its observations.

## Splits and leakage

Both current family groups are `unassigned`. A demonstration with two families is not a credible generalization benchmark. Choose the evaluation split after sufficient independent coverage exists, before adding task/capacity variants, and preserve that manifest for future releases.

The validator prevents a source or family from spanning different splits, catches identical document hashes across splits, and excludes explicitly answer-revealing blocks from selection inputs. It does not detect every paraphrase, related paper, or indirect clue. Human context review must check those, including the prompt, quantities, constraints and references.

The current tasks use supplied evidence or an explicit replay request. They do not measure autonomous literature retrieval. Keep a later retrieval benchmark separate and disclose which documents are searchable.

## Migration and remaining work

The legacy decision template and extraction decision now use `target`, replacing `reviewed_target`, and increment to legacy schema version 2. Their review status remains pending. Canonical records include `legacy_origin` pointers where relevant; historical source notes, raw process values and normalization are retained.

The implemented subset is schemas, canonical records, task gates, review binding, a historical trace and deterministic exports. Remaining work: human review, independent process coverage, frozen evaluation splits, retrieval indexing, a live simulator adapter, full-process acceptance gates and baseline/model evaluation. Collecting more papers does not automatically trigger retraining.

## Additional review criteria from related work

Use [the methods review](../docs/RELATED_WORK_METHODS.md) for the concrete checklist and delivery hooks. During review, distinguish reported, computed, assumed and hypothetical claims; check every requested specification and qualify any optimality assertion. Track changes between the source/proposed design and executed configuration, including simplified units and open recycles.

These requirements are not new schema fields or validator guarantees in the current pilot. Attach them to review preparation until versioned support is implemented. Do not use convergence of a relaxed or simplified case to approve performance of the original process. Paired missing-information evaluation tasks must share their parent's family split. No task status, approval, export gate or training readiness changes with this documentation update.
