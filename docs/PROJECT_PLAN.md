# Project plan

## Goal

Build a dataset, then fine-tune an existing open model to specify, run, check and explain process simulations. CHEPTA performs calculations; the model must learn appropriate tool use and engineering decisions. Generalization to unfamiliar processes and other simulators is a testable objective, not a current capability.

## Agreed starting point

Use reaction examples documented by CHEPTA. Find openly accessible supporting process papers. Prefer processes whose required units and methods are available. Prepare literature and specifications for separation-dependent cases now, but do not claim execution until the required units exist and have been checked.

## Milestones

1. **Initial catalogue (this setup).** Six families and eight source entries, with access, rights and capability gaps. Five priority research papers; two additional paper leads/reference-only entries; one textbook.
2. **One checked case.** Source and units ledger; independent reconstruction; actual CHEPTA run; balances, method/range checks and reference comparison; human review. Start with an existing reactor and a separate full-process specification.
3. **Approximately twenty reviewed examples.** Include variations, invalid specifications, missing data and failure diagnosis. A source audit decides how many defensible examples can actually be made.
4. **Dataset release.** Select code/data licenses, audit provenance, group related cases before splitting, publish a dataset card and a reproducible release on Hugging Face.
5. **Small fine-tuning experiment.** Compare base model and adaptation with identical simulator access on held-out problems. Report failures, numerical accuracy and cost.
6. **Demonstration and broader transfer.** Show request, tool calls, results and references. Reproduce selected tasks with a second simulator before claiming simulator-independent competence.

## Next tasks

- Obtain Aali–Hadi's full paper and recheck the upstream ethanol example's equations, unit conversions and assumptions.
- Obtain the Medrano-Garcia methanol supporting information; separate the synthesis loop from final purification.
- Extract a specification ledger for Sulgan's conventional ethyl-acetate plant. Audit NRTL-HOC, rate-based columns and kinetic provenance before mapping it to CHEPTA.
- Recheck CHEPTA capabilities at the start of implementation; the audited commit is recorded in data/upstream.json.
- Keep the cumene, benzene and HMF cases deferred until their source/data blockers are resolved.

## Working arrangement and spending

GitHub holds code, process cases and research history. Hugging Face will hold checked dataset/model releases and eventually a demonstration. Agents can prepare code and draft examples; scripts handle repetitive runs. Human engineering review is recorded separately.

No training, paid services, Hugging Face upload or automatic scraping job is started by this setup. The previously discussed approximately USD 100 experiment is a planning allowance, not a purchase or a guaranteed total cost.
