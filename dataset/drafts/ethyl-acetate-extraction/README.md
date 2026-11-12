# First operation-selection example: extraction and feed conditioning

**Draft, unreviewed, not training eligible. No new extraction simulation has been run.**

The lesson is to identify a physical separation obstacle, shortlist a suitable mechanism, and define the evidence needed to verify it. It is not to copy a column sequence or prescribe cooling for every reaction.

## Input and proposed decision

The task supplies a normalized mixture composition and eventual ethyl-acetate purity target. It does not supply the author's flowsheet as the answer. The candidate is water extraction followed by phase separation, with temperature conditioning considered only when justified by equilibrium and utility constraints. Downstream operations must be chosen separately to meet the final specification.

The feed composition comes from S1 stream 9, before it is mixed with recycled stream 15. It is a scoped learning task, not the complete published extractor feed. No capacity is prescribed; the original 90,166 kg/h is retained solely for provenance. Normalization uses 1 kg of feed, an amount basis, not 1 kg/h. No equipment size or performance was scaled.

## Files

- [Evidence records](evidence.json): three source-linked claims with conditions and limitations.
- [Decision record](decision.json): task inputs separated from the proposed target and verification requirements. The inherited key `reviewed_target` is a template name only; `target_review_status` explicitly says unreviewed draft.
- [Basis](basis.json): original state and explicit normalization formula.
- [Evaluation prompts](evaluation-prompts.json): five unscored variations testing physical reasoning, missing information and capacity handling. These are related examples, not a held-out benchmark.
- [Research leads](research-leads.json): optional measurement lead, deferred unless a concrete CHEPTA data gap requires it.

## Evidence and attribution

Piotrowski and Kubica (2021), [DOI 10.3390/pr9081425](https://doi.org/10.3390/pr9081425), Sections 1.2, 2 and 3.3; Figure 4; Table A1. CC BY 4.0. Statements are paraphrased and assembled into a new draft task; the paper's simulation trends are not relabelled as our measurements. Published inconsistencies remain in the [stream/equipment audit](../../../cases/ethyl-acetate-piotrowski-2021/STREAM_EQUIPMENT_AUDIT.md).

Arce, Alonso and Vidal (1999), [DOI 10.1252/jcej.32.440](https://doi.org/10.1252/jcej.32.440), is an experimental-data lead. Only the publisher abstract was checked. Numerical tables and redistribution rights have not been reviewed. It is not an accepted evidence record and does not establish the cooling benefit quantitatively.

## What acceptance still requires

Reuse CHEPTA property models and existing validation after checking applicability; check the actual combined feed after water addition; verify phase fractions, ester recovery and ethanol removal; assess downstream purification and utility implications; complete engineering and rights review. Evidence may change the shortlist. Do not assume that a two-phase mixture exists at every composition or that an enriched organic phase meets final purity.

Metadata checks confirm references and normalization, not the engineering decision. No model has been trained on this draft.

## Updated scope

Reuse CHEPTA property models, parameter provenance and existing validation. Lab checks applicability to components, conditions and required calculation; it does not routinely remeasure or revalidate phase equilibrium. Investigate underlying data only for a concrete missing parameter, range violation or material disagreement. Process-level balance and performance checks still apply.

See [operation reasoning](OPERATION_REASONING.md) for the expanded process example.
