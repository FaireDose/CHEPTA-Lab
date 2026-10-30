# Initial canonical data collection

Collection/annotation date: 2026-10-30. **Started: 7 source blocks, 9 evidence claims, 3 engineering decisions, 1 historical execution record and 3 draft tasks.** These are not nine new papers and are not accepted training examples.

The collection uses Piotrowski and Kubica's [2021 ethyl acetate paper](https://doi.org/10.3390/pr9081425), together with the existing executed ethanol benchmark based on [Aali and Hadi, 2023](https://doi.org/10.24237/djes.2023.16203). Source attribution and rights metadata remain in `data/sources.json`; release review is pending.

## What was collected

| Evidence ID | Source locator | Information captured |
|---|---|---|
| `ea-azeotrope` | Section 1.2, opening paragraph | Azeotropy as a separation obstacle |
| `ea-extraction` | Section 1.2, purification step 2 | Water washing to remove ethanol and enrich the organic phase |
| `ea-cooling` | Section 3.3, paragraph after Figure 4 | Cooling rationale; reported achievable range 20–30 °C, constrained by cooling-water temperature |
| `ea-wash-tradeoff` | Section 3.3, final paragraph | More wash water trades enrichment against ester loss and recovery burden |
| `ea-wash-ratio` | Section 3.3, final paragraph | Reported favorable water/azeotrope mass ratio 1–2 kg/kg |
| `ea-impurity-limits` | Section 3.4, paragraph after Figure 6 | Ester purity 99.9 wt%; water below 0.03 wt%; ethanol below 0.04 wt% |
| `ea-reflux-limits` | Same paragraph | Reported R/D 1.5 for ester purity, above 2.25 for impurity limits, favorable interval 3–3.5 |
| `ea-feed-location` | Section 3.4, final paragraph | Reported favorable feed location between stages 4 and 6 |
| `ea-thermo-choice` | Section 2.1, final sentences | Authors' reason for choosing UNIQUAC for mixture equilibria |

These are case-specific source descriptions or simulation findings. R/D mass/molar convention and stage numbering need resolution before reproducing those settings. The values are stored with units, bases and qualifiers. No new simulation numbers were invented or calculated for this collection.

The first three claims refine existing draft material. Additional records separate previously combined trade-offs and add explicit numerical specification and design information. We keep source findings distinct from our engineering inferences about when to reconsider a choice.

## Engineering decisions and learning tasks

Three linked decisions address feed conditioning, conditional extraction selection, and meeting all purification constraints together.

| Draft task | Learner input | Expected behavior |
|---|---|---|
| Explain extraction cooling | Published trend and loss/recovery trade-off | Explain why cooling can help, then state utility and process limits |
| Select next with missing data | Mixture identities and azeotropic obstacle; missing feed state and specifications | Request the missing information before a final choice; do not invent a solvent ratio or guaranteed purity |
| Interpret ethanol benchmark | Existing explicit CHEPTA request | Make the matching call, read the actual response and preserve physical-validation qualifications |

The selection exercise does not expose the author's extraction route in learner context. The target focuses on the justified request for missing information; the reviewer rubric allows a separately supported candidate but does not require copying one published equipment sequence.

## Source and execution checks

- Annotated the existing publisher HTML/text snapshot rather than claiming a newly downloaded document. Direct publisher fetch was rate-limited during this pass; the earlier full snapshot remained available. Each source block records the snapshot hash, exact source locator, text selector and fragment hash.
- The original HTML-to-text extraction software version is unknown. This is recorded rather than reconstructed from memory. Selected facts were manually checked against the available text.
- Kept existing temperature/balance discrepancies as qualifications. They do not prevent drafting a narrowly supported explanation, but cannot be silently ignored in reproduction.
- Linked the ethanol execution manifest, runner, request, complete response and independent numerical-check artifact by hash. The original manifest records a requested engine revision and key file hashes but no locally observed Git commit; the replay preserves that qualification.
- No new engine run, human approval, trained model or Hugging Face release was produced by this collection.

## Next collection priorities

1. Review these concise claims and the three rendered tasks; resolve any inaccurate attribution or hidden-answer clues.
2. Extend the same ethyl acetate case with table-cell and stream-connectivity evidence, retaining original and normalized bases already in the repository.
3. Add a genuinely independent source/process family from the research catalogue. This improves coverage more than generating many paraphrases of the current case.
4. Assign a held-out family set before expanding variants, then measure an existing model with the intended evidence and simulator access.
