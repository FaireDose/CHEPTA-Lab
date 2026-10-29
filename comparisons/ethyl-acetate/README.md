# Ethyl acetate: comparison specification and source audit

Status: draft specification; no full-process simulation; not training eligible. Checked 2026-10-29.

## Selection

Start with Piotrowski–Kubica's S1 (subcooled azeotrope and extractant recycle) versus S2 (classic process at comparable product/wastewater quality). These are alternative flowsheet configurations of the same chemistry. Keep Sulgan's conventional plant as the cross-paper extension. This refines the provisional cross-paper pair: first isolate configuration effects within one source, then test transfer across papers.

## Source-reported values

Piotrowski and Kubica (2021), [DOI](https://doi.org/10.3390/pr9081425), [open article PDF](https://pdfs.semanticscholar.org/7c7c/5cc0ac24fa96af9914932cdac35e5483b5be.pdf), CC BY 4.0. Values below transcribed from Table 2, printed p. 12; all are reported simulations, not CHEPTA outputs.

| Indicator | S1 improved | S2 classic | S3 classic |
|---|---:|---:|---:|
| Product quality, % | 99.9 | 99.9 | 98.0 |
| Ethanol, t/t product | 0.524 | 0.524 | 0.531 |
| Acetic acid, t/t product | 0.681 | 0.681 | 0.681 |
| Process water, t/t product | 1.42 | 1.42 | 2.18 |
| Heating, printed kW/t product | 3333.9 | 3704.7 | 3704.7 |
| Cooling, printed kW/t product | 3251.1 | 3621.9 | 3621.9 |
| Wastewater, t/t product | 1.61 | 1.61 | 2.36 |

Section 3.4 identifies product purity on a mass basis. Appendix A, Tables A1/A2, stream 16 gives S1/S2 product flows of 12,436/12,434 kg/h, both 99.90 mass% ethyl acetate. Feed streams 1/2 are 6,511 kg/h ethanol and 8,472 kg/h acetic acid at 15 °C and 1 bar in both cases. Stream 9 is 30 °C in S1 and 70 °C in S2. These tabulated temperatures are operating points, not validated optimization bounds.

## Discrepancies to preserve

- Table 2 labels S3 heat duty equal to S1 but prints S3 heating/cooling identical to S2. Section 2 describes equal rectification duties and increased reactor duty for S3. Resolve the system boundary and table labels before claiming equal total energy.
- Printed energy units kW/t product lack an explicit production-rate time basis. Do not silently relabel these as kWh/t or GJ/t.
- S1 vs S2 printed heating difference is 10.01% and cooling 10.24%, computed relative to S2. These ratios are arithmetic comparisons of the reported numbers, not verified engineering savings.
- Appendix product water is 0.04 mass% in S1 and 0.07% in S2, whereas Section 3.4 discusses a water limit below 0.03%. Matching overall purity alone does not establish compliance with all impurity limits.
- Equations 1–3 and the original Atalay kinetics require concentration/catalyst definitions and dimensional review. Do not infer rate units from the printed 1/min labels alone.

## Cross-paper comparison

Sulgan, Labovsky and Labovska (2020), [DOI](https://doi.org/10.3390/pr8121618), [open PDF](https://psecommunity.org/wp-content/plugins/wpor/includes/file/2107/LAPSE-2021.0623-1v1.pdf), CC BY 4.0. Section 2.4 sets 10 kmol/h of each raw reactant, 25 °C boundary streams, atmospheric pressure, and a 10 kmol/h product target at 99.9 mol% purity. It uses NRTL-HOC and non-equilibrium columns; the 2021 paper uses UNIQUAC (Section 2.1). These differences prevent direct ranking of published totals. Both conventional processes already include extraction/decanter functions: this is not “extraction versus no extraction.”

## Proposed common basis (Lab choices, not source facts)

- Compare S1/S2 first at 1 tonne/h of saleable product with at least 99.9 mass% ethyl acetate. Retain original flows and report specific quantities separately. Component-specific impurity limits require resolution before a feasible winner can be declared.
- Pure feed ethanol and acetic acid at the same temperature/pressure; initially preserve the shared 2021 feed conditions. Match recovery accounting and include water makeup, wastewater, all recycle/regeneration, heating and cooling.
- For Sulgan transfer, convert full component compositions between mole and mass fractions; do not equate 99.9 mol% with 99.9 mass%. Resimulate at the shared basis; linear scaling is only preliminary bookkeeping, not equipment design.
- Compare thermal demand, fresh feed/water and organic losses separately. No cost winner until shared utility prices, economic year, location, operating hours and equipment costing are specified.
- Treat azeotrope cooling temperature, water circulation, reflux, reactor residence time and recycle as candidate adjustable variables. Bounds remain unset pending source/phase/catalyst checks; published optima are not universal constraints.
- Vary utility assumptions and product impurity requirements after validation. Report trade-offs or abstain when evidence is insufficient.

## Execution gate and next work

The pinned CHEPTA revision c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2 returns unsupported for solve_column. See capability-check.json. This is a check of that revision only, not a claim about current main.

Before either plant runs: audit all Table A1/A2 streams and rounding balances; resolve kinetics and energy/quality inconsistencies; verify UNIQUAC binary sets against VLE/LLE data; implement or adopt verified distillation/extraction models and recycle convergence. Sulgan additionally needs an explicit treatment of vapor association and non-equilibrium column differences. Arbitrary component splitters cannot fill these gaps.

Next executable subtask: extract and independently balance the published S1/S2 stream tables, preserving residuals and incomplete boundaries. A full-plant comparison remains blocked; no ranking or accepted training label is generated.

Human engineering review and final rights review: pending. Attribution is retained; transcription and proposed comparison choices are our adaptation. No paper PDF is redistributed.
