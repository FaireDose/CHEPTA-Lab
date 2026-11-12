# Dataset

**In one look.** A dataset item is a question with a checked answer, built from a case (see
[docs/HOW_IT_WORKS.md](../docs/HOW_IT_WORKS.md), section 3). Today: **3 draft items, 0 accepted.** An item is
accepted only after a person has reviewed its sources, its engineering and its licence.

| File or folder | What it is |
|---|---|
| [records/pilot.json](records/pilot.json) | All items, with the evidence (paper passages) and decisions they rest on. The one true list |
| [schemas/](schemas/) | The required structure of items and of study records |
| [PIPELINE.md](PIPELINE.md) | How items are checked and exported, and what each kind needs before acceptance |
| [drafts/](drafts/) | Working notes for future items (ethyl acetate extraction) |
| `*.template.json`, [contracts/](contracts/), [COLLECTION_LOG.md](COLLECTION_LOG.md) | Older templates and the collection log, kept for the record |

---

## Earlier notes

There are currently **zero accepted training examples**. The catalogue is research metadata, not a dataset of correct engineering answers.

Use [PIPELINE.md](PIPELINE.md) and the canonical records in [records/pilot.json](records/pilot.json) for new training tasks. The legacy example template still describes full simulation cases, which should record:

1. The user's engineering request and which information is missing.
2. Referenced inputs with original units and a page/table/equation locator.
3. Component and reaction identities, catalyst and rate basis, property method and valid operating range.
4. Concise engineering decisions, assumptions and alternatives.
5. Executable input files plus the simulator commit/version.
6. Actual tool calls and tool outputs, including warnings and failed attempts.
7. Material/element/energy checks and an independent numerical or experimental comparison with justified tolerances.
8. Human engineering review and a source-rights review.

Keep measured data, source-reported simulations, our simulations and assumptions labelled separately. Do not put invented successful outputs in an example.

Only release tasks after the checks appropriate to their claims are complete. Literature explanation and conditional-selection tasks do not require an artificial simulation; numerical claims require actual runs and comparison. All tasks require source, human engineering, rights and context review. Store related variations under the same family/source group when splitting training and evaluation data. Reserve unseen processes to test transfer.

The exporter now generates explicitly labeled review previews and gated releases. It uses actual saved request/response artifacts for the ethanol replay. No training configuration or model run has been started.


## Comparison examples

Use `comparison.template.json` for alternatives producing the same product. Populate `alternatives` with entries shaped like `alternative_record_contract`, then remove that explanatory contract from the completed record. Declare a common basis and record the evidence for all normalization. Keep objectives, fixed inputs, adjustable variables and their bounds distinct. Uncertain inputs without defensible bounds remain unknown.

A correct target may be a conditional recommendation, a trade-off or a request for missing information. Do not label the paper author's preferred option as the universal best route. Evaluate changed objectives/constraints and unseen process families as well as numerical reproduction. See the revised project plan for release and training gates.

The ethanol case in `cases/` is an executed draft, not accepted training data. Its two kinetic variants are not two complete process routes.

## Dataset architecture

See [the dataset map and diagrams](../docs/reference/DATASET_DESIGN.md) for physical evidence, justified operation selection, general process sequences and capacity normalization. Templates are draft scaffolds; existing cases retain their original schema versions.

## First operation-selection draft

[Ethyl acetate extraction and feed conditioning](drafts/ethyl-acetate-extraction/README.md) links physical evidence to a provisional decision, explicit normalization and five evaluation prompts. No new simulation or acceptance is claimed.
