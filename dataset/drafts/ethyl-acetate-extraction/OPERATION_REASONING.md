# Why these operations were selected

Six linked draft decisions from Piotrowski and Kubica (2021), [DOI](https://doi.org/10.3390/pr9081425), CC BY 4.0. Source explanations are paraphrased; Lab adds conditional questions and calculation requirements. No alternatives have been numerically ranked.

| Decision | Purpose and mechanism | What CHEPTA should calculate |
|---|---|---|
| acid-recovery | Separate and retain reactant while forwarding the ester-containing mixture. | Column composition profile, acid carryover and recycle balance. |
| extraction | Partition ethanol into the aqueous phase and enrich the organic phase in ester. | Phase split at mixed-feed conditions, component recovery and stage requirements. |
| conditioning | The authors report improved organic-phase enrichment after cooling; this is conditional, not a universal cooling rule. | Heater/cooler duty plus extraction and downstream duties at feasible utility conditions. |
| product-purification | Use the changed composition to reach final product specifications. | Purity and recovery together with reflux, stages, feed location and duty. |
| aqueous-organics-recovery | Reduce material losses and return useful components; water reuse is specific to this case. | Recovered organics, water quality, duty and effect of recycle on the reactor. |
| recycle-integration | The paper returns acid and recovered organics to reaction and part of the organic phase to the initial column. | Converged flowsheet balances, impurity accumulation and changed equipment loads. |

Exact source sections, reconsideration questions and draft status are in [operation-decisions.json](operation-decisions.json).

## How to use this knowledge

For a new mixture, identify the obstacle and select a suitable mechanism using known mixture behaviour and constraints. Assemble only the operations needed to meet that task. Do not reproduce all six steps automatically. Capacity is specified separately when sizing is needed.

The initial extraction example starts with stream 9 after acid recovery; the acid-recovery decision is contextual and must not be inserted ahead of that task without changing its input boundary. Cooling is a conditional supporting operation. Recovery and recycle are optional process requirements, not mandatory steps for every chemistry.

## Reuse and execution

Reuse CHEPTA property models, parameter provenance and existing validation. Lab checks applicability to components, conditions and required calculation; it does not routinely remeasure or revalidate phase equilibrium. Investigate underlying data only for a concrete missing parameter, range violation or material disagreement. Process-level balance and performance checks still apply.

At the pinned revision c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2, [method guidance](https://github.com/FaireDose/CHEPTA/blob/c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2/docs/METHOD_SELECTION.md) discusses NRTL/UNIQUAC for polar liquids and two-liquid systems. This is method guidance, not proof of complete parameter coverage. The existing [column capability check](../../../cases/ethyl-acetate-piotrowski-2021/capability-check.json) reports unsupported at that revision. A thermodynamic model and a multistage equipment solver are different capabilities. Recheck both when selecting the revision for execution.

Next work: attach existing CHEPTA model/range evidence to the chosen calculation and prepare an executable process case when its required unit capabilities exist. No new experimental-data search is required by default. Published balance discrepancies remain recorded for reproduction; they do not prevent extracting the authors’ explanations.

Status: six decision records drafted; no new simulator run, no accepted training examples.
