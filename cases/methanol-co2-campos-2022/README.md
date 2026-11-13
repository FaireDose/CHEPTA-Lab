# CO2 + H2 to methanol plant (Lacerda de Oliveira Campos et al. 2022): one-step process, prepared for CHEPTA

| In one look | |
|---|---|
| Paper | Lacerda de Oliveira Campos, John, Beeskow, Herrera Delgado, Pitter, Dahmen & Sauer 2022, *Processes* 10, 1535, doi 10.3390/pr10081535 (CC BY 4.0). The **one-step process** (conventional synthesis loop); the paper's three-step process with intermediate condensation is a later variant |
| Plant | 39 blocks in Figure S1: CO2 compression in 3 stages with 2 knock-out drums, H2 compressor, feed-effluent exchangers, 2 parallel multitubular reactors (Cu/ZnO/Al2O3, LHHW kinetics, boiling-water cooled), high- and low-pressure flash drums, 2 % purges, recycle compressor, methanol column (30 stages, partial condenser); plus a fired heater burning the purges and a steam cycle with turbine (9 blocks). 61 streams. 4824 kmol/h CO2 and 14472 kmol/h H2 in; 145.7 t/h methanol (99.67 mol %) out |
| Transcribed | all 61 streams of supplement Tables S9-S10 (molar and mass flow, T, P, molar enthalpy, entropy, exergy, 7 mole %) in [streams.json](streams.json); all 39 blocks with every printed setting (reactor tubes and catalyst, flash conditions and sizes, column, purges, Table S14 duties, U and areas) in [equipment.json](equipment.json); each value with page and table |
| Paper's own balances | **all close** within the printed rounding (mass, moles, components; atoms in the reactors, burner and plant), every mole-% sum is 100, and the energy balances from the printed enthalpies match Table S14's duties, **except cooler HE7** (19.75 MW from the streams, 24.2 MW in Table S14) ([STREAM_AUDIT.md](STREAM_AUDIT.md)) |
| Simulated | **nothing yet** (CHEPTA not run; the maintainer's go is needed first) |
| Reviewed by a person | no; draft, written by an AI session on 2026-11-13 |

The paper's numbers are an Aspen Plus V10 simulation (Peng-Robinson in the reactors, NRTL2 elsewhere), not
measurements: agreement with CHEPTA, later, will be two models agreeing.

## Why this plant

Process 1 of [docs/reference/CANDIDATE_PROCESSES.md](../../docs/reference/CANDIDATE_PROCESSES.md), chosen in
[docs/NEXT_PLANTS.md](../../docs/NEXT_PLANTS.md): the only open CO2-to-methanol paper found with a full stream table.
The first candidate, Medrano-García et al. 2025, has none (its supplement holds inventories and costs). It is unrelated
to the ester plants (gas phase, 70 bar, equation of state, compressors, a kinetic plug-flow reactor), and its flash
drums are the real-plant counterpart of the [methanol separator case](../methanol-separator-flash/README.md).

## What the audit found

Run `python cases/methanol-co2-campos-2022/audit_balances.py` from the repository root (no third-party packages).

- Every block closes in mass, moles and each component (atoms C, H, O, N for the reactors and burner) within
  ±0.5 kmol/h, ±0.0005 mole %, ±0.05 t/h; masses recomputed from the compositions are within 1.1 % of the printed
  ones (largest: 45-PURGE).
- Energy from the printed molar enthalpies: HE1 −13.59 MW (Table S14 13.6), HE2, HE3, HE4, HE5, HE6 hot and cold
  sides cancel and match Table S14 (11.1, 5.6, 105.5, 103.3, 5.0 MW), HE8 −41.84 (41.8), column reboiler minus
  condenser −89.89 MW (53.7 − 143.6 = −89.9); reactors with their coolant, mixers, valves, flashes and burner
  adiabatic within rounding. Compressor work from the enthalpies: 10.93, 10.61, 10.81, 11.94 (H2), 0.57 (recycle) MW.
- Derived: both purges 2.00 % (text: 2 %); the reactor feed split 0.500; CO2 conversion per pass 0.285 (abstract:
  28.5 %).

### Disagreements kept, not fixed

| # | Where | What |
|---|---|---|
| 1 | Table S14 vs Tables S9-S10 | HE7 (22 → 23, cooling water): 24.2 MW in Table S14, 19.75 MW from the stream enthalpies (−18 %). All other duties agree within 0.1 MW |
| 2 | Supplement p.10 vs the enthalpies | The text says stream 26 is heated in HE5; the enthalpies show HE5 heats the column feed 28 → 29 and HE6 heats 26 → 27 (as the text says two paragraphs earlier). Read as HE6 |
| 3 | Supplement p.11 vs Table S9 | Steam superheated "up to 542 °C"; 59W is 528.8 °C. Turbine outlet "155 °C" (labelled 59W in the text); 60W is 147.5 °C |
| 4 | Supplement p.11 vs Figure S1 / Table S14 | The condenser of the steam cycle is "HE13" in the text, HE8 in the figure and Table S14 |
| 5 | Supplement p.11 vs Table S9 | Turbine: 30.3 MW of electricity in the text; the enthalpy drop 59W → 60W is 31.40 MW (a generator or mechanical efficiency is not stated) |
| 6 | Figure S1 vs text | Recycle compressor labelled CP-REF in the figure, CP-REC in the text |

## What is not in the paper (to choose and record when the plant is run)

- Phases or vapour fractions of the streams (only the steam leaving the reboiler: 0.47).
- The reactor's heat-transfer coefficient to the boiling water (not found in the pages read); compressor
  efficiencies; the column's second specification (only stages, feed stage, reflux ratio 2 and the condenser
  temperature are given) and stage numbering.
- The NRTL2 and Peng-Robinson parameters (Aspen databank, not printed).
- Rights: Table 1 of the article (kinetic parameters, Model-6p) is "reprinted with permission" from an ACS paper:
  check before transcribing it; this case has not copied it.

## What CHEPTA 0.6.2 can probably do, and probably not

From the documentation and code of the npm package `chepta@0.6.2` (read outside the repository) and the methanol
separator case. **Nothing was run.**

| Part | Expectation | Why |
|---|---|---|
| Property method | **differs** outside the reactor: CHEPTA has no NRTL parameters for the gas pairs (MISSING_DATA for CO2, H2, CO with methanol and water) and no UNIQUAC for CO2; use PR with k_ij or PR + gE (MHV1) everywhere | checked with `CHEPTA.system` in 0.6.2: PR has fitted k_ij for CO2 + methanol and CO2 + water; H2 + methanol, H2 + water, CO + water, CO + CO2 and water + N2 are 0 |
| Compressors, valves, mixers, splitters, flashes, heaters, exchangers | probably yes | all are CHEPTA units; flash at 69.25 bar ran in the separator case |
| Reactors | probably yes: CHEPTA's `pfr` takes tubes, length, diameter, LHHW rates and a coolant (U, T) | src/units/kinetic-reactors.js; U must be assumed; the kinetic table's reuse to check |
| Column | **uncertain**: an activity model refuses CO2 above its critical temperature in a mixed solvent; PR rests on its k_ij; a partial condenser with a vapour and a liquid distillate to check | src/units/columns/column.js, gasSolubilityCheck |
| Burner | probably yes as a conversion reactor (H2, CO, methanol burned with 15 % excess air) | src/units/reactors.js |
| Steam cycle | probably yes (pump, expander, heaters) but with water through the flowsheet's property method, not the steam tables | to check |

## Files

| File | What |
|---|---|
| [streams.json](streams.json) | Tables S9-S10, 61 streams, unchanged |
| [equipment.json](equipment.json) | Figure S1 connections and every printed setting, with locators |
| [audit_balances.py](audit_balances.py) | the audit |
| [balance-results.json](balance-results.json), [STREAM_AUDIT.md](STREAM_AUDIT.md) | its results, generated |

PDFs not in the repository: article sha256 `8215079335f33a55bf972db7e365275e51cdaff4f8cfc685603f1359f4b0447d`,
supplement sha256 `015d60b56ef5d6c0f418257004b39e8053dd7dadeb79d49e284f6dbd3b1a2245` (both from mdpi-res.com).
