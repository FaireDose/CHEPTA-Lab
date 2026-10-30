# Project plan

Revised 2026-10-29 following the owner's clarification of the intended engineering capability.

## Deliverable

Build a traceable dataset and an evaluated adaptation of an existing open model that can propose, simulate and compare process designs. Given a product, feed, constraints and objectives, it should explain which alternatives are defensible, what evidence is missing and which conditions change its recommendation. CHEPTA supplies calculations; the model selects and checks tool use. Competence on unfamiliar processes is an evaluation goal, not a capability guaranteed by a small training set.

Start from reactions documented in CHEPTA and papers whose models can actually be supported. Prepare separation-dependent cases while the required units are developed.

## Knowledge-guided dataset design

The [dataset architecture and diagrams](DATASET_DESIGN.md) define the updated workflow. Physical knowledge narrows operation choices before simulation. Process sequences are general; recovery and waste treatment are included only when relevant. Preserve original capacities for reproduction, normalize transferable evidence explicitly, and recalculate capacity-dependent equipment behaviour. The first [operation-decision draft](../dataset/drafts/ethyl-acetate-extraction/README.md) is prepared. Next map the engineering decisions to CHEPTA calculations, reusing existing property validation; route comparisons remain downstream verification tasks.

## Refinements

- Keep individual reproducible cases and add comparison records linking alternatives and sources.
- Declare a common basis: feed composition/quality, capacity, product purity/recovery, boundaries, utilities and economic year/location. Document transformations from each paper; do not rank unadjusted published costs.
- Separate fixed inputs, adjustable variables with justified bounds, uncertain parameters and missing information. These process variables are different from the model's trainable weights.
- Label literature facts, assumptions, simulator outputs and derived metrics separately. Numerical answers should come from executed tools with source evidence for decisions.
- Preserve different valid choices. A cheaper design may consume more energy or use less mature equipment. Report trade-offs and sensitivity; do not assign a universal winner.
- Store concise, checkable decision rationales and actual tool traces. Include rejected alternatives, failed calculations, requests for missing information and justified abstention. Never manufacture successful outputs.

## Milestones and acceptance gates

1. **Research catalogue — prepared.** Six families and eight source entries, with access, rights and capability gaps.
2. **One reactor benchmark — numerical work executed; review pending.** Reconstruct inputs, run pinned CHEPTA, independently integrate the equations, check units/balances and record discrepancies. The first ethanol case compares the upstream simplification with Table-12 adsorption terms. These are model variants of one route, not two complete process routes. It remains ineligible for training pending engineering/rights review and resolution of scope/units.
3. **Two routes to the same product.** Prepare the comparison specification before expanding the corpus. Provisional pair: conventional versus extraction-assisted ethyl acetate using Sulgan (2020) and Piotrowski–Kubica (2021). Audit original kinetics, establish a common basis and identify unit capabilities. Do not claim a runnable comparison until physical separation models and source inputs are available. If unsupported, preserve the gap and select another adequately supported pair.
4. **Approximately twenty reviewed examples.** A pilot target, not twenty independent processes or a guarantee of generalization. Include reproductions, sensitivities, fair comparisons, invalid requests, missing data and failure diagnosis. Keep related examples grouped.
5. **Baseline evaluation before fine-tuning.** Give an existing model retrieval and the same simulator tools intended for the adapted model. Measure specification validity, source accuracy, numerical checks, fair comparison, response to changed assumptions and appropriate abstention. Reserve unseen papers/process families; do not leak their variants into training.
6. **Dataset release and small training experiment.** After engineering/rights review, version the dataset with a dataset card on Hugging Face. Fine-tune only if the baseline reveals a learnable deficiency and sufficient reviewed examples exist. Compare base and adapted models with identical tools, retrieval and held-out tests. Report cost and failures as well as improvements.
7. **Demonstration and transfer.** Show the request, cited assumptions, actual calls, alternatives and conditional recommendation. Test selected tasks in another simulator before claiming transfer.

## How the model learns

We choose task inputs and reviewed target actions/answers. Fine-tuning adjusts the model's internal weights to learn those patterns; a pile of papers does not automatically establish engineering truth. Simulator results, sources and review determine acceptable targets. A separate optimizer may vary process settings within justified bounds; that is not model training.

New papers first enter the evidence register and retrieval collection. Reproduce and review their cases before adding a versioned dataset release. Retraining is a deliberate batch experiment after useful examples accumulate, not an automatic action for every paper. Re-run evaluations after changes, maintaining a separate untouched test set.

## Next work

- Review the ethanol source ledger, adsorption comparison, unit ambiguities and thermodynamic qualifications. Obtain underlying experimental data before claiming physical validation.
- Comparison ledger prepared: see [ethyl acetate audit](../comparisons/ethyl-acetate/README.md). Start with the 2021 S1/S2 pair at matched quality; retain Sulgan as the cross-paper extension. All 56 S1/S2 streams and 19 blocks are now extracted and balance-audited. Resolve flagged balances and energy/impurity/equipment inconsistencies before full-process execution.
- Retrieve and audit the methanol supporting information for a later full-process case.
- Recheck CHEPTA capabilities when adopting a new engine revision; keep old results tied to their original revision.

## Working arrangement and spending

GitHub holds plans, source metadata, runnable cases, tests and review history. Hugging Face is the later distribution channel for reviewed datasets, model adapters and a demo. Agents may draft and calculate; human engineering review is a distinct recorded step.

No training, rented GPU, paid API call, automatic scraping job or Hugging Face publication is started by this work. The previously discussed approximately USD 100 experiment is a planning allowance, not a purchase or guaranteed total cost.


## Property-model reuse

Reuse CHEPTA property models, parameter provenance and existing validation. Lab checks applicability to components, conditions and required calculation; it does not routinely remeasure or revalidate phase equilibrium. Investigate underlying data only for a concrete missing parameter, range violation or material disagreement. Process-level balance and performance checks still apply.
