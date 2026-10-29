# Stream and equipment audit

Piotrowski and Kubica (2021), DOI 10.3390/pr9081425, CC BY 4.0. Tables A1/A2 (pp.13–14), Table 1 (p.11), Figure 1 (p.4). Source values are reported simulations, not measurements or CHEPTA results. All 28 streams per strategy are in [streams.json](streams.json). All 19 blocks and available settings are in [equipment.json](equipment.json).

Run `python comparisons/ethyl-acetate/audit_balances.py` from the repository root. No third-party Python packages required. Raw numbers are preserved; no balancing corrections or composition normalization are applied.

## Balance results

Residuals below are outlet minus inlet. The envelope assumes nearest rounding at the printed precision; an exceeded envelope is an unresolved inconsistency, not proof of which entry is wrong. Reactive boundaries are checked by mass and atoms, not conservation of each reacting species.

| Strategy | Boundary | Mass residual kg/h | Within mass/component/atom rounding envelopes |
|---|---|---:|---|
| S1 | 1 | 0.000 | Yes |
| S1 | 2 | 0.000 | Yes |
| S1 | 3 | -4.000 | No |
| S1 | 4 | 0.000 | Yes |
| S1 | 5 | 0.000 | Yes |
| S1 | 6 | 0.000 | Yes |
| S1 | 7 | -1.000 | Yes |
| S1 | 8 | 0.000 | Yes |
| S1 | 9 | 1.000 | Yes |
| S1 | 10 | 0.000 | Yes |
| S1 | 11 | 0.000 | Yes |
| S1 | 12 | 0.000 | Yes |
| S1 | 13 | 0.000 | Yes |
| S1 | 14 | 0.000 | Yes |
| S1 | 15 | 0.000 | Yes |
| S1 | 16 | 0.000 | Yes |
| S1 | 17 | 0.000 | Yes |
| S1 | 18 | 0.000 | Yes |
| S1 | 19 | -7.000 | No |
| S1 | plant | -11.000 | No |
| S2 | 1 | 0.000 | Yes |
| S2 | 2 | 0.000 | Yes |
| S2 | 3 | -8.000 | No |
| S2 | 4 | 0.000 | Yes |
| S2 | 5 | 0.000 | Yes |
| S2 | 6 | 0.000 | Yes |
| S2 | 7 | -4.000 | No |
| S2 | 8 | -15.000 | No |
| S2 | 9 | 0.000 | Yes |
| S2 | 10 | 0.000 | Yes |
| S2 | 11 | 0.000 | Yes |
| S2 | 12 | 0.000 | Yes |
| S2 | 13 | 1.000 | Yes |
| S2 | 14 | 0.000 | Yes |
| S2 | 15 | -1.000 | Yes |
| S2 | 16 | 0.000 | Yes |
| S2 | 17 | 0.000 | Yes |
| S2 | 18 | 0.000 | Yes |
| S2 | 19 | 0.000 | Yes |
| S2 | plant | -27.000 | No |

Full residuals and bounds: [balance-results.json](balance-results.json). Atom weights and stream molar-flow consistency checks are recorded there. Nominally zero source fractions may hide trace components; no catalyst stream is represented. The external boundary assumes feeds 1, 2, 17 and products 16, 25 shown in Figure 1.

## Selected equipment

| Block | Function | Inlet streams | Outlet streams |
|---|---|---|---|
| 1 | mixer | [1, 2] | [3] |
| 2 | heater | [3] | [4] |
| 3 | mixer | [4, 7, 21] | [5] |
| 4 | reactor-evaporator | [5] | [6] |
| 5 | azeotropic column | [6, 27] | [7, 8] |
| 6 | condenser/cooler | [8] | [9] |
| 7 | mixer | [9, 15] | [10] |
| 8 | extractor | [10, 19] | [11, 20] |
| 9 | splitter | [11] | [12, 26] |
| 10 | heater | [12] | [13] |
| 11 | product column | [13] | [14, 16] |
| 12 | cooler | [14] | [15] |
| 13 | mixer | [17, 24] | [18] |
| 14 | transfer block; exact type unconfirmed | [18] | [19] |
| 15 | wastewater column | [28] | [21, 22] |
| 16 | splitter | [22] | [23, 25] |
| 17 | cooler | [23] | [24] |
| 18 | heater | [26] | [27] |
| 19 | heater | [20] | [28] |

Table 1 specifies a 300 m3 reactor-evaporator, 85–90 °C; columns 5/11/15 have 8/35/18 stages and feed stages 8/15/9. Column 5 uses R/V=0.62 (S1), 0.61 (S2); columns 11/15 use R/D=3/2 in both. Seven heater/cooler blocks have reported duties. These are published selections, not new equipment sizing or procurement recommendations. Block 14 is retained as an unidentified transfer block rather than assigned an unsupported equipment type.

## Discrepancies and remaining specifications

- Table 1 column 5 has 8 stages; Section 3.2 says at least 14. The selected product-column feed stage 15 also differs from the discussion of stages 4–6. Stage numbering or design revision requires clarification.
- Table 1 extractor temperatures 30/70 °C match feed conditioning, while organic outlet temperatures are 21/27 °C and aqueous outlets 24/41 °C. Do not impose Table 1 as an isothermal extractor temperature without resolving this.
- Table A1 stream 28 differs slightly from stream 20 across a heater; preserve the discrepancy. The balance calculation determines whether printed rounding explains it.
- Product water limits and energy-table inconsistencies from the comparison README remain unresolved. Neither strategy is accepted as a compliant design.
- Missing: catalyst loading/rate definitions, full property parameters, extractor stage model, column efficiencies/internals/diameters, utility temperatures, exchanger areas/U, pressure drops and mechanical specifications. A flowsheet symbol is not a complete equipment specification.
- Next: resolve failed balance rows against the original Chemcad files or author clarification before generating executable training targets. Do not tune a simulator to compensate for conflicting stream entries.

Engineering review: pending. Training eligibility: false. This audit checks published data, not a new process simulation.
