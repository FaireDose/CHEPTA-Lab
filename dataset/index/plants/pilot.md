# Run log: pilot (generated; do not edit)

Run log of the plant, not yet written as lessons. One line per decision or CHEPTA run, grouped by unit, best-supported first; the row id is in an HTML comment for `kb.py show`. A struck-through line was corrected by a later row and no longer counts; the correcting row gives its reason. [All topics](../rules-readable.md)

## distillation (1)

- **Set purification conditions against all product limits together. Expected: A specification-compliant candidate with quantified recovery and duty.** worked, paper's simulation; Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 3.4, final paragraph. When: product column after wash, piotrowski 2021 plant s2. <!-- ea-purification-constraints -->

## extraction (1)

- **Shortlist water extraction if two-liquid feasibility and recovery constraints permit. Expected: Enrich the ester-rich phase before further purification.** worked, paper's simulation; Piotrowski & Kubica 2021, Section 1.2, opening paragraph; Piotrowski & Kubica 2021, Section 1.2, purification step (2); Piotrowski & Kubica 2021, Section 3.3, final paragraph. When: water wash of azeotrope, piotrowski 2021 plant s2. <!-- ea-choose-extraction -->

## heat exchange (1)

- **Consider cooling before extraction within available utility limits. Expected: Case-supported enrichment; quantify actual recovery and duties before claiming a benefit.** worked, paper's simulation; Piotrowski & Kubica 2021, Section 3.3, paragraph after Figure 4; Piotrowski & Kubica 2021, Section 3.3, final paragraph. When: cooling before water extraction, piotrowski 2021 plant s2. <!-- ea-condition-feed -->
