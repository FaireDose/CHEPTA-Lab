# Ethyl acetate plant (Piotrowski & Kubica 2021): classic design S2 on chepta 0.6.1

| In one look | |
|---|---|
| Paper | Piotrowski & Kubica 2021, Processes 9, 1425 (CC BY 4.0): ethyl acetate from ethanol and acetic acid; the classic plant S2 |
| Simulated | **all 19 units and 28 streams of S2** in `chepta@0.6.1` through its command line: each unit alone with the paper's inlets, the two halves of the plant with their recycles, and the plant once through |
| Complete flowsheet | **once through, not closed.** Acetic acid forces a cut at stream 9 (CHEPTA cannot hold two liquids with acetic acid); Lab's script joins the halves, and the second pass stops in column 5 (a second liquid would form on stage 7) |
| Agrees with the paper | azeotrope stream 9 within 0.01 % in flow and 0.01 mass % points; product 12,467 vs 12,434 kg/h; 7 of 11 duties within 7 % (reactor +6.9 %, its conversion taken from the paper; HTXR 2, 6, 17; column 15 condenser and reboiler; column 11 condenser) |
| Differs | product column reboiler −12 to −19 % (CHEPTA boils 45 % of the feed in the heater before it); wastewater-column bottoms 0.15 mass % ethanol vs 0.02 %; water back to the reactor 8.2 vs 5.2 mass %; HTXR 18 and 19 duties look exchanged in the paper |
| CHEPTA could not | two liquids with acetic acid; two liquids in an absorber-type column; acetic acid below 16.66 C; an adiabatic extractor; a reactor-evaporator (7 capability requests below) |
| Reviewed by a person | no; draft, written by an AI session on 2026-11-12 |

Study record: [study-record.json](study-record.json). Runs and CHEPTA's answers, unchanged:
[results-chepta-0.6.1/](results-chepta-0.6.1/) (56 runs, refusals included; [run-manifest.json](results-chepta-0.6.1/run-manifest.json)),
comparison: [comparison-s2.json](results-chepta-0.6.1/comparison-s2.json). Register rows this case feeds:
[data/ISSUES_AND_ROUTES.md](../../data/ISSUES_AND_ROUTES.md).

## What was run

[s2_model.py](s2_model.py) builds every request from the transcriptions [streams.json](streams.json) (Table A2) and
[equipment.json](equipment.json) (Table 1, Figure 1); every setting is listed there and in the run manifest with its
kind (paper, derived, assumed), locator and reason. [run_s2_chepta_0.6.1.py](run_s2_chepta_0.6.1.py) sends them to
`chepta request` of the released package `chepta@0.6.1` (installed with npm outside the repository; Lab's
`package.json` pin is not changed here; lock entry [chepta-0.6.1.npm-lock.json](chepta-0.6.1.npm-lock.json)).
[compare_s2.py](compare_s2.py) compares stream by stream. Property method: UNIQUAC with CHEPTA's own fitted pair
sets, ideal-gas vapour with CHEPTA's acetic acid dimers (the paper: UNIQUAC in Chemcad 7, parameters not printed).

| Level | Runs | What it shows |
|---|---|---|
| Units | `u-*` (4 components), `u3-*` (without acetic acid) | each unit fed with the paper's own inlet streams |
| Sections | `secA-paper-inlets` (feeds, HTXR 2, MIX 3, reactor, column 5, HTXR 6, recycle 7); `secB-paper-inlets-extr1..8` (extractor, splitters, columns 11 and 15, water loop, recycles 15 and 24) | each half with its own recycles, fed at the cut with the paper's streams |
| Plant | `plant-a1-*`, `plant-a2-*`, `diag-*` | section A with the paper's 21 and 27, then B with CHEPTA's own stream 9 (once through); round 2 fails in column 5 |

### What Lab had to choose (the main ones; all in s2_model.py)

| Setting | Paper | Used | Why |
|---|---|---|---|
| Reactor KREA 4 | CSTR with a rate law (Eqs. 1-3, p.5-6), 300 m³, 85-90 C | conversion of acetic acid per pass 0.7703, outlet saturated vapour | catalyst concentration and units of the rate law missing; CHEPTA has no reactor-evaporator. **Derived from Table A2 streams 5 and 6: the reactor is not predicted** |
| Feeds 1 and 2 | 15 C (Table A2) | 18 C | pure acetic acid at 15 C is below its triple point (289.81 K in CHEPTA's record): refused; 17 C still refused after mixing (runs u-htxr2-15C, secA-feeds-17C) |
| Column 5 | 8 stages, feed 8, R/V 0.61 (Table 1); "at least 14" (p.7) | absorber-type column, 8 equilibrium stages, reflux 27 on stage 1, vapour 6 on stage 8 | Figure 1 shows no condenser or reboiler; R/V follows from 60,000/98,380 = 0.610 |
| HTXR 6 outlet | 70 C | saturated liquid | at 70 C and 100 kPa CHEPTA finds 72 % vapour (run u-htxr6-70C) |
| Extractor EXTR 8 | 70 C, W/A 1 (Table 1); outlets 27 and 41 C | **2 equilibrium stages, isothermal 27 C** | stage count not in the paper: 2 matches stream 11's ethanol (1.87 vs 1.86 mass %), so that number is calibrated, not compared (runs u3-extr8-1..8stage); 70 C: the paper's feed is 78 % vapour there (refused), and with a liquid feed the outlets boil (ok, no warning) |
| MIX 7 | mixer | mixer with outlet saturated liquid (1 kW) | adiabatic mixing leaves 3.7 % vapour and the extractor refuses any vapour (run secB-mix7-adiabatic) |
| Splitters 9, 16 | 60,000 and 20,000 kg/h | fractions 0.68718 and 0.17272 | CHEPTA's splitter takes fractions only |
| Column 11 | 35 stages, feed 15, R/D 3; purity > 99.9 mass % | the same; second specification bottoms 141.5 kmol/h (plant), or 99.90 mass % (unit run); two liquids allowed | stage numbering assumed as CHEPTA's (1 condenser, 35 reboiler) |
| Column 15 | 18 stages, feed 9, R/D 2 | the same, distillate 394.6 kmol/h | second specification not printed |
| Block 14 | not named | pump without pressure rise | Figure 1 symbol; streams 18 = 19 |
| Section B | acetic acid 0.00-0.01 mass % | without acetic acid | every two-liquid stream with acetic acid is refused (runs `*-acid`); CHEPTA's own column 5 leaves 0.0004 mass % acid in stream 8 (0.007 kmol/h dropped at the cut) |

## Results against the paper (Table A2, Table 1)

The paper's numbers are a Chemcad 7 simulation, not measurements: agreement is two models agreeing.

### Units fed with the paper's inlets

| Unit | Compared | CHEPTA | Paper | Difference |
|---|---|---:|---:|---:|
| HTXR 2 | duty (from 18 C) | 543.9 kW | 535.6 kW | +1.6 % |
| KREA 4 (conversion imposed) | outlet T; duty | 89.0 C; 14,437 kW | 90 C; 13,586.2 kW | −1.0 K; +6.3 % |
| KREA 4 as an equilibrium reactor at 90 C (other unit, for reference) | acetic acid in vapour 6 | 3.21 mass % | 4.74 | the paper's outlet holds more acid than CHEPTA's chemical and phase equilibrium at 90 C |
| Column 5 | overhead 8 flow; ethyl acetate | 98,994 kg/h; 84.53 % | 98,380; 84.78 % | +0.6 %; −0.25 points |
| Column 5 | acetic acid overhead (limit 0.005 %, p.6) | 0.000 % | 0.01 % | CHEPTA meets the limit, the paper's own stream prints above it |
| Column 5 | bottoms 7 flow; T | 14,293 kg/h; 88.5 C | 14,912; 88 C | −4.2 %; +0.5 K |
| HTXR 6 | duty; outlet T | −14,734 kW; 69.8 C | −14,855.8 kW; 70 C | −0.8 %; −0.2 K |
| EXTR 8 (2 stages, 27 C) | raffinate 11 flow; water; ethyl acetate | 89,563 kg/h; 4.61 %; 93.53 % | 87,314; 4.70; 93.43 | +2.6 %; −0.09; +0.10 points |
| EXTR 8 | ethyl acetate lost to the water phase 20 | 9.30 % | 10.72 % | −1.4 points |
| HTXR 10 | duty to 71 C | 2354 kW (45 % vaporized) | 713.5 kW | ×3.3: CHEPTA's mixture boils below 71 C |
| Column 11, bottoms flow fixed | product purity; water | 99.868 %; 0.113 % | 99.90; 0.07 (limit 0.03, p.8) | misses the purity by 0.03 points |
| Column 11, purity 99.90 % fixed (610 s) | product flow; water; reboiler | 12,367 kg/h; 0.084 %; 7529 kW | 12,434; 0.07; 9219.2 | −0.5 %; +0.014 points; −18 % |
| Column 11 | condenser | −9114 to −9140 kW | −9180.3 | −0.4 to −0.7 % |
| HTXR 18 | duty | 1580 kW | 4332.9 kW | see "paper's own discrepancies" |
| HTXR 19 | duty (paper inlet at 41 C) | 5681 kW | 1541.1 kW | idem |
| Column 15 | distillate 21 flow; condenser; reboiler | 23,315 kg/h; −12,105 kW; 14,919 kW | 23,405; −12,127.2; 16,136.6 | −0.4 %; −0.2 %; −7.5 % |
| Column 15 | ethanol in the bottoms (limit 0.01 % organics, p.10) | 0.151 % | 0.02 % | ×7 |
| HTXR 17 | duty | −8869.3 kW | −8869.3 kW | 0.0 % |

### Sections and the plant once through (run plant-a2-r01-A then -B; sections alone agree to the same digits)

| Stream or unit | CHEPTA | Paper | Difference |
|---|---:|---:|---:|
| 9 azeotrope to extraction | 98,388 kg/h; 8.53 / 6.69 / 84.78 mass % ethanol/water/ester | 98,380; 8.53 / 6.68 / 84.78 | +0.01 % |
| 7 column 5 bottoms to reactor | 14,771 kg/h; ethanol 8.86 % | 14,912; 5.86 % | −0.9 %; +3.0 points |
| 6 reactor vapour | 88.6 C | 90 C | −1.4 K |
| KREA 4 duty | 14,522 kW | 13,586.2 kW | +6.9 % |
| 11 raffinate | 91,068 kg/h | 87,314 | +4.3 % |
| 27 reflux to column 5 | 62,580 kg/h | 60,000 | +4.3 % |
| **16 product** | **12,467 kg/h, 100.00 mass % ethyl acetate** (flow fixed at 141.5 kmol/h) | 12,434; 99.90 % | +0.3 %; the limits of p.8 are met |
| 21 wastewater distillate to reactor | 21,407 kg/h; water 8.17 % | 23,405; 5.19 % | −8.5 %; +3.0 points |
| 25 wastewater | 19,412 kg/h; 0.002 % ethanol | 20,000; 0.02 % | −2.9 % |
| Column 11 condenser; reboiler | −9702; 8087 kW | −9180.3; 9219.2 | +5.7 %; −12.3 % |
| Column 15 condenser; reboiler | −12,348; 15,481 kW | −12,127.2; 16,136.6 | +1.8 %; −4.1 % |
| HTXR 17 | −8612 kW | −8869.3 | −2.9 % |

**Why the loop is not closed.** In round 2 section A receives CHEPTA's own reflux 27 and wastewater distillate 21
(8.2 % water instead of 5.2 %). Column 5 then does not converge (attempts a1 and a2, `NO_CONVERGENCE`); alone with the
same inlets it reports why: "a second liquid would form on stage 7" (`PHASE_SPLIT`, run diag-scds5-round2-inlets),
and with two liquids allowed: "an absorber holds a vapour and one liquid (phases "VL"); two liquids on its stages
(phases "VLL") are not built yet" (`NOT_AVAILABLE`, run diag-scds5-round2-inlets-VLL). A closed S2 plant in CHEPTA
needs capability requests 1 and 2.

### The paper's own discrepancies (kept, not resolved)

- Table 1 (p.11) heater duties HTXR 18 and HTXR 19 look exchanged: HTXR 18 heats stream 26 (60,000 kg/h, 27 to 70 C,
  sensible heat only) yet prints 4332.9 kW, and HTXR 19 heats stream 20 (139,203 kg/h of mostly water, 41 to 70 C)
  yet prints 1541.1 kW. CHEPTA gives 1580 and 5681 kW. S1 shows the same pattern (6088 / 1595 kW). Lab's inference,
  to be checked.
- Acetic acid in the azeotrope: the limit is 0.005 mass % (p.6), the paper's stream 8 prints 0.01 %.
- Wastewater bottoms: < 0.01 % organics required (p.10), stream 22 prints 0.03 %.
- Product water: < 0.03 % required (p.8), stream 16 prints 0.07 %.
- Column 5: 8 stages in Table 1, "at least 14" in Section 3.2; column 11 feed stage 15 in Table 1, "between the 6th
  and 4th" in Section 3.4.
- Pure acetic acid fed at 15 C, below its melting point.
- The earlier ones below (energy units of Table 2, S3 labels, kinetics) stand.

## Capability requests for CHEPTA (from this case)

| # | Request | CHEPTA 0.6.1's outcome and message | Evidence |
|---|---|---|---|
| 1 | Vapour-liquid-liquid equilibrium with acetic acid's chemical theory: flash, heater, column stages ("VLL") | `unsupported` `PHASE_SPLIT`: "the three-phase flash needs an activity model without the acid chemical theory"; column: `NOT_AVAILABLE` "two liquids on the stages (phases "VLL") need an activity model ... without the dimerizing acids' chemical theory" | runs u-htxr10-acid, u-htxr12-acid, u-htxr18-acid, u-htxr19-acid, u-scds11-acid-VL, u-scds11-acid-VLL, u-extr8-*-acid, diag-scds5-round2-inlets |
| 2 | Two liquids on the stages of an absorber/stripper configuration | `unsupported` `NOT_AVAILABLE`: "an absorber holds a vapour and one liquid (phases "VL"); two liquids on its stages (phases "VLL") are not built yet." | diag-scds5-round2-inlets-VLL |
| 3 | Liquid enthalpy of acetic acid slightly below its triple point, at least in a mixture | `invalid_input` `OUT_OF_RANGE`: "Acetic acid: its liquid heat-capacity record starts at 289.81 K, so its liquid enthalpy below it cannot be calculated." | u-htxr2-15C, secA-feeds-17C |
| 4 | Extraction block: (a) stage energy balances (adiabatic extractor); (b) accept a feed with a little vapour that condenses at the stage temperature | (b) `invalid_input` `BAD_INPUT`: "the feed is partly vapour (vapour fraction 0.03713 at 342.9 K and 100 kPa); the stages hold two liquids and no vapour." | secB-mix7-adiabatic, u3-extr8-1stage-70C-feed70C |
| 5 | Extraction block at a temperature where the outlets boil returns `ok` without a warning (raffinate vapour fraction 0.051 at 70 C) | `ok`, no warning | u3-extr8-1stage-70C |
| 6 | A reactor-evaporator (boiling reacting liquid, vapour the only outlet), or a CSTR with a vapour draw | not in the capability list (no request possible) | paper Section 2, Figure 1 |
| 7 | A splitter by flow, or a flowsheet design specification (make-up water to hold W/A = 1) | not available (splitter: `fractions` only) | s2_model.py, splitters 9 and 16 |

Minor: column 11 with a mass purity specification and two liquids took 610 s (12 s with a flow specification).

## What the maintainer should spot-check (at most 3)

1. **Largest effect:** Table 1, p.11: are the duties of HTXR 18 (4332.9 kW) and HTXR 19 (1541.1 kW) exchanged?
   Compare with Table A2 streams 20, 26, 27, 28 (pp.13-14).
2. **Least certain:** the reactor's acetic acid conversion 0.7703 = 1 − 4.74/20.64 (Table A2 streams 5 and 6, same
   53,292 kg/h). The whole of section A rests on it.
3. **At random:** Table 1, S2 column 11: 35 stages, feed stage 15, R/D 3, condenser −9180.3 kW, reboiler 9219.2 kW.

## Reproduce

From the repository root, with chepta 0.6.1 installed (`npm install --no-save chepta@0.6.1`, or set `CHEPTA_BIN`):
`python3 cases/ethyl-acetate-piotrowski-2021/run_s2_chepta_0.6.1.py` (groups with `S2_GROUPS`; attempt label
`S2_PLANT_ATTEMPT`), then `compare_s2.py` and `build_study_record.py`. Re-running writes new files and changes the
study record's hashes; the committed request files are the record of what was run (s2_model.py was extended between
groups of runs; its hash in the manifest is the last one).

(This folder was `comparisons/ethyl-acetate/` until 2026-11-12.)

## Earlier specification (2026-10-29, unchanged below)

Status then: draft specification; no full-process simulation; not training eligible. Checked 2026-10-29.

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

Stream and equipment audit completed: see [56 streams, 19 blocks and balance results](STREAM_EQUIPMENT_AUDIT.md). Next resolve flagged balances and conflicting equipment specifications. A full-plant comparison remains blocked; no ranking or accepted training label is generated.

Human engineering review and final rights review: pending. Attribution is retained; transcription and proposed comparison choices are our adaptation. No paper PDF is redistributed.
