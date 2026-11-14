# CO2 + H2 to methanol plant (Lacerda de Oliveira Campos et al. 2022): one-step process, prepared for CHEPTA

| In one look | |
|---|---|
| Paper | Lacerda de Oliveira Campos, John, Beeskow, Herrera Delgado, Pitter, Dahmen & Sauer 2022, *Processes* 10, 1535, doi 10.3390/pr10081535 (CC BY 4.0). The **one-step process** (conventional synthesis loop); the paper's three-step process with intermediate condensation is a later variant |
| Plant | 39 blocks in Figure S1: CO2 compression in 3 stages with 2 knock-out drums, H2 compressor, feed-effluent exchangers, 2 parallel multitubular reactors (Cu/ZnO/Al2O3, LHHW kinetics, boiling-water cooled), high- and low-pressure flash drums, 2 % purges, recycle compressor, methanol column (30 stages, partial condenser); plus a fired heater burning the purges and a steam cycle with turbine (9 blocks). 61 streams. 4824 kmol/h CO2 and 14472 kmol/h H2 in; 145.7 t/h methanol (99.67 mol %) out |
| Transcribed | all 61 streams of supplement Tables S9-S10 (molar and mass flow, T, P, molar enthalpy, entropy, exergy, 7 mole %) in [streams.json](streams.json); all 39 blocks with every printed setting (reactor tubes and catalyst, flash conditions and sizes, column, purges, Table S14 duties, U and areas) in [equipment.json](equipment.json); each value with page and table |
| Paper's own balances | **all close** within the printed rounding (mass, moles, components; atoms in the reactors, burner and plant), every mole-% sum is 100, and the energy balances from the printed enthalpies match Table S14's duties, **except cooler HE7** (19.75 MW from the streams, 24.2 MW in Table S14) ([STREAM_AUDIT.md](STREAM_AUDIT.md)) |
| Simulated | **all units, three sections and the whole plant as one CHEPTA flowsheet, closed** (both recycles, both purges; run plant-a6 on chepta 0.6.2, 31 loop iterations, balances closed). Fired heater and steam cycle left out. 79 runs kept, 35 of them refusals or failures ([results-chepta-0.6.2/](results-chepta-0.6.2/), [COMPARISON.md](COMPARISON.md)) |
| Column ends (plant) | methanol 4548 kmol/h at **99.73 mol %** (paper 4542 at 99.67); water **99.999 mol %** (paper 99.985) |
| Differs most | FLASH3 liquid (stream 24) holds 3.4 % CO2 in CHEPTA against 18.5 % in the paper, so the CO2 recovered at 1 bar and recycled (39-REC) is 86 % smaller and the CO2 compression train carries 27-31 % less gas |
| HE7 | CHEPTA cools the paper's stream 22 to 30 C with **25.1 MW**: it supports Table S14 (24.2 MW), not the printed stream enthalpies (19.75 MW) |
| CHEPTA could not | start a column with a few ppm of CO or N2; meet a purity or recovery inside the range it scanned; go past 12 Newton iterations; approach 2 K in a counterflow exchanger without `zones: 10`; give a vapour and a liquid distillate (5 requests, [CAPABILITY_REQUESTS.md](CAPABILITY_REQUESTS.md)) |
| Reviewed by a person | no; draft, written by AI sessions on 2026-11-13 (transcription) and 2026-11-14 (runs). No AI review session yet |

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
| 1 | Table S14 vs Tables S9-S10 | HE7 (22 → 23, cooling water): 24.2 MW in Table S14, 19.75 MW from the stream enthalpies (−18 %). All other duties agree within 0.1 MW. The maintainer (2026-11-14): compare with the streams first; the run will show whether the authors' duty is wrong |
| 2 | Supplement p.10 vs the enthalpies | The text says stream 26 is heated in HE5; the enthalpies show HE5 heats the column feed 28 → 29 and HE6 heats 26 → 27 (as the text says two paragraphs earlier). Read as HE6 |
| 3 | Supplement p.11 vs Table S9 | Steam superheated "up to 542 °C"; 59W is 528.8 °C. Turbine outlet "155 °C" (labelled 59W in the text); 60W is 147.5 °C |
| 4 | Supplement p.11 vs Figure S1 / Table S14 | The condenser of the steam cycle is "HE13" in the text, HE8 in the figure and Table S14 |
| 5 | Supplement p.11 vs Table S9 | Turbine: 30.3 MW of electricity in the text; the enthalpy drop 59W → 60W is 31.40 MW (a generator or mechanical efficiency is not stated) |
| 6 | Figure S1 vs text | Recycle compressor labelled CP-REF in the figure, CP-REC in the text |

## Maintainer's spot check (2026-11-14) and the answers

The maintainer checked three items selected by the building session (not by a separate AI review session, which has
not been done yet). Their findings, as written, and what the source shows:

| Item | Maintainer | Source | Status |
|---|---|---|---|
| HE7 duty (24.2 MW, Table S14) against its streams | "22 and 23 are for HE8, 21 and 22 are for HE7; the properties are Table S11, not S10" | Right for the **three-step** process (Figure S2, Table S11, supplement p.17: HE7 cools 21 → 22, HE8 cools 22 → 23; from Table S11, 21 → 22 is −46.24 MW against 46.3 MW for three-step HE7 in Table S14). This case is the **one-step** process: properties in Table S9 (pp.12-13), compositions in Table S10 (pp.14-15), and in Figure S1 and the text (supplement p.10, "finally by cooling water (HE7)") HE7 cools 22 → 23. The spot-check request did not say "one-step"; that was the building session's error in wording | **closed** (the maintainer, 2026-11-14): the one-step HE7 disagreement (19.75 MW from the streams against 24.2 MW in Table S14) is kept as a disagreement in the paper; the **streams are the basis** of the comparison, and the run will show whether the authors' duty or their stream enthalpies are off |
| Column feed, Table S10 p.14, streams 28 and 29 | 28 = 0, 0.001, 1.285, 50.041, 48.671, 0.002, 0; 29 the same | matches streams.json | confirmed by the maintainer |
| Reactor tubes, article p.4 | 22,000 tubes per reactor, 12.5 m, 3.75 cm | the article p.4 reads "33,000 tubes" (text layer and a 200 dpi render), the supplement p.9 "six reactor modules with 33000 tubes each" (99,000 per RPLUG block); 33,000 tubes × 12.5 m × 3.75 cm × 1050 kg/m³ = 478.4 t, the stated 478.13 t per module; 22,000 tubes would give 318.9 t | **closed**: 33,000 confirmed (the maintainer, 2026-11-14: "indeed there were 33000 tubes, my mistake") |

Side observation, outside this case: in the three-step process, Table S14 gives HE8 14.3 MW and HE9 37.9 MW, but the
Table S11 streams give 37.89 MW for 22 → 23 (HE8 in the text) and 12.79 MW for 23 → 24. Not transcribed; to note if
the three-step process is ever built.

## The runs on chepta 0.6.2 (2026-11-14)

[model.py](model.py) builds every request from [streams.json](streams.json) and [equipment.json](equipment.json); every
choice is in its `SETTINGS` list with its kind (paper, derived, assumed) and locator, copied into the
[run manifest](results-chepta-0.6.2/run-manifest.json). [run_chepta_0.6.2.py](run_chepta_0.6.2.py) sends them to
`chepta request` of Lab's pinned `chepta@0.6.2` and keeps every request, output (with CHEPTA's run id), stderr and exit
code; a rerun never overwrites a kept run. [compare.py](compare.py) writes [COMPARISON.md](COMPARISON.md) and
`comparison.json`, stream by stream; [build_study_record.py](build_study_record.py) writes [study-record.json](study-record.json).
The paper's numbers are an Aspen Plus V10 simulation (PR in the reactors, NRTL2 elsewhere), CHEPTA's are PR everywhere:
agreement is two models agreeing.

### What Lab had to choose

| Setting | Paper | Used | Why |
|---|---|---|---|
| Property method | PR in the reactors, NRTL2 elsewhere (article p.9) | PR with CHEPTA's k_ij everywhere | CHEPTA has no NRTL pairs for the gases with methanol and water; PR + MHV1 is refused for methanol + N2 (runs u-flash3-mhv1, u-column-*-mhv1, `NOT_AVAILABLE`) |
| Reactor kinetics | Model-6p (article Eqs. 8-11, p.8; Table 1, p.9), phi_Zn 0.10 for CO2/COx > 0.90 (p.8) | the same, written as CHEPTA rate expressions on fugacities (kPa / 100 = bar), per kg of catalyst | CO2/COx of stream 14 is 0.935; Table S4's k = phi exp(A2)/1000 = 181.211 confirms phi = 0.10 |
| Reactor heat transfer | U computed along the tube (supplement Section B); coolant boiling at 247.5 C | U 300 W/m2/K (assumed), coolant 520.65 K | not printed; U 150 and 1000 move the outlet by 0.4 K and 0.04 mol % points (runs u-reactor-U*) |
| Compressors | efficiency not printed | CHEPTA's 0.75 | outlets 7-14 K hotter than the paper's (CP-REC 0.0 K) |
| HE4, HE5, HE6 | outlets in Table S9 | HE4 cold outlet 237.5 C; HE5 minimum approach 2 K on 10 zones; HE6 cold outlet 30 C | with the paper's outlets the loop met a temperature cross in HE5 (runs sec-loop-a1, -a3, -direct, -wegstein): CHEPTA's hot stream cannot give that heat above about 70 C; HE6 by its hot outlet stopped (sec-loop-a2); HE5 by its approach needs `zones: 10` (request M4) |
| HE3, reactors' water side, fired heater, steam cycle | modelled | left out; HE3 a cooler to 111 C; coolant at constant temperature | equipment.json: may be left out of the first case; the purges leave as products |
| Column | 30 stages, feed above stage 24, reflux 2, partial vapour-liquid condenser at 53 C (p.10) | partial condenser (all distillate vapour), reflux 2, bottoms 4581 kmol/h (stream 30), then a flash at 53 C giving 32 and 31-MEOH | one distillate only in CHEPTA (request M5); a purity or recovery specification is refused (M2); the boil-up ratio stopped in the loop (plant-a5) |
| Column feed traces | H2, CO, N2 at 0 to 20 ppm in 29 | sent round the column to the 53 C flash | the column cannot start with them (request M1); the paper sends 98.6-99.9 % of each to 32 (Table S2) |
| Tear streams | not printed | 19, 35, 26, 28, 39-REC with the paper's values as guesses; 200 iterations, tolerance 1e-7 | HE2, HE4, HE5, HE6 each join two parts of the plant, so the recycles alone do not break every cycle (plant, plant-a2) |

### Results against the paper

Units fed with the paper's streams (runs u-*):

| Unit | CHEPTA | Paper | Difference |
|---|---:|---:|---:|
| Reactor (U 300), outlet 16: flow; T; methanol | 31,958 kmol/h; 247.7 C; 7.53 mol % | 32,021; 247.9; 7.415 | -0.2 %; -0.2 K; +0.11 points |
| Reactor heat to the coolant | 35.8 MW | 35.0 MW (55W - 54W, derived) | +2.3 % |
| HE7, 22 -> 30 C | **25.1 MW** | 24.2 (Table S14); 19.75 (stream enthalpies, derived) | +3.8 %; +27 % |
| HE7 with 24.2 MW / 19.75 MW | outlet 31.05 C / 36.06 C | 30 C | |
| HE4; HE5 (hot to 62 C); HE6; HE2 | 105.2; 108.1; 5.27; 11.14 MW | 105.5; 103.3; 5.0; 11.1 | -0.3 %; +4.6 %; +5.4 %; +0.4 % |
| FLASH3 liquid 24: flow; CO2 | 9468 kmol/h; 3.37 mol % | 11,488; 18.545 | -17.6 %; -15.2 points |
| FLASH1, FLASH2 liquids 40, 42 | 255, 113 kmol/h | 276, 196 | -7.5 %, -42 % (less CO2 dissolved) |
| FLASH4 at 1 bar: vapour 37; liquid 28 | 2640; 9320 kmol/h | 2548; 9412 | +3.6 %; -1.0 % |
| VALVE1 outlet 25 | 5.0 C | 18.5 C | -13.5 K (more CO2 flashes in CHEPTA) |
| Column (paper feed 29, traces bypassed) + 53 C flash: 31-MEOH; 30-WATER; 32 | 4533 kmol/h at 99.835 %; 4581 at 99.998 %; 298 | 4542 at 99.667 %; 4581 at 99.985 %; 289 | -0.2 %; +0.17 and +0.013 points; +3.2 % |
| Condenser + 53 C flash; reboiler | 151.0 MW; 62.6 MW | 143.6; 53.7 (Table S14) | +5 %; +17 % |

The whole plant as one flowsheet (run plant-a6, CHEPTA run run-mwgbv28a-1):

| Stream | CHEPTA | Paper | Difference |
|---|---:|---:|---:|
| **31-MEOH** | 4548 kmol/h, methanol **99.728 %**, CO2 0.165, water 0.107 | 4542, 99.667, 0.316, 0.016 | +0.14 %; +0.06 points |
| **30-WATER** | 4581 kmol/h (fixed), water **99.999 %** | 4581, 99.985 | +0.014 points |
| 13 reactor feed; 16 reactor outlet | 72,580; 31,750 kmol/h, methanol 7.49 % | 73,113; 32,021, 7.415 % | -0.7 %; -0.9 % |
| 36-REC recycle; 44-PURGE | 52,898; 1080 kmol/h | 51,504; 1051 | +2.7 %; +2.7 % |
| 24 FLASH3 liquid | 9522 kmol/h, CO2 3.41 % | 11,488, 18.545 % | -17 % |
| 32 gas distillate | 38.6 kmol/h | 289 | -87 % (column feed 0.24 % CO2 against 1.285 %) |
| 39-REC CO2 recycle; 45-PURGE | 395; 7.3 kmol/h | 2786; 51 | -86 % |
| 2 to 10 CO2 compression | 5219 to 5210 kmol/h | 7610 to 7138 | -27 to -31 % |
| HE7; HE4; HE5 | 25.6; 114.3; 96.6 MW | 24.2; 105.5; 103.3 | +6 %; +8 %; -6 % |
| Compressors CP1, CP2, CP3 | 7.9, 7.9, 7.8 MW | 10.93, 10.61, 10.81 (stream enthalpies, derived) | the smaller CO2 recycle |

Reading: the reactor and the column ends agree closely; the loop differs where CO2 dissolves in the 70 bar flash
liquid. That is a property-method difference (the paper's NRTL2 parameters are not printed; CHEPTA's PR k_ij for CO2 +
methanol and CO2 + water are fitted to data, `fitted-naidoo2008-etal`, `fitted-bermejo2005-etal`). Lab does not judge
which is right without data; it is the first item to spot-check against the source.

### HE7 (the maintainer, 2026-11-14: compare on the streams first)

On the streams: the paper's own stream enthalpies give 19.75 MW for 22 -> 23, and CHEPTA gives 25.1 MW for the same
inlet to the same 30 C (run u-he7), with outlet vapour fraction 0.852. From the paper's numbers alone (derived): HE6
cools stream 21 by 5.1 K for 4.98 MW (0.98 MW/K); HE7 would cool the same stream a further 26.9 K for 19.75 MW (0.73
MW/K), although more methanol and water condense at the lower temperatures; Table S14's 24.2 MW gives 0.90 MW/K, and
CHEPTA 0.93. **CHEPTA supports Table S14's duty.** Lab's inference, not checked with the authors: the printed enthalpy of stream 22 or 23 is the more likely error.
The paper's other duties all match its stream enthalpies (STREAM_AUDIT.md), so this is one number.

### Extrapolations (H2 + CO and the others), per run

CHEPTA's warnings are kept. Every run's `value.extrapolations`, with the blocks each applies to, is listed in
[COMPARISON.md](COMPARISON.md). In the plant (plant-a6) the H2 + CO k_ij set (fitted at 68.2-88.2 K) is used up to
520.9 K (432.7 K above) in every block; also H2 + N2 (407.9 K above), CO + N2 (398.9), CO2 + N2 (227.7), CO + methanol
(148.0), CO2 + water (127.7), CO2 + methanol (125.9), and CO's ideal-gas heat capacity (20.9 K above 500 K) in HE4,
the reactors and MIXER3. At FLASH3 (303.1 K, run u-flash3): H2 + CO 215.0 K above, H2 + N2 190.2, CO + N2 181.2,
CO2 + N2 10.0. The H2 + CO k_ij = 0 rerun of the separator flash is a separate queued task (HANDOVER item 6).

### Capability requests

Five, each with one small input file, CHEPTA's outcome and what it should do: [CAPABILITY_REQUESTS.md](CAPABILITY_REQUESTS.md).
M1 column start with ppm of CO or N2; M2 purity/recovery refused inside the scanned range; M3 Newton stops at 12
iterations whatever `max_iterations` says above 12 (5 is honoured; ethyl acetate request 12 confirmed); M4 the 2 K
approach search uses 10 zones and calls a counterflow exchanger "crossflow"; M5 a condenser with vapour and liquid
distillates.

### Not kept as intended

The first successful `sec-purification` run (HE6 by its hot outlet) was overwritten by the next run of the same id
before the runner was changed to never overwrite; the kept `sec-purification` run is the later one (HE6 by its cold
outlet). Kinetics rights: Model-6p's seven constants are in model.py and the request files (see the decision below).

## What the maintainer should spot-check (at most 3; chosen by the building session, not by an AI review session)

1. **Largest effect:** supplement Table S10, p.14, row 24: CO2 18.545 mol % in the FLASH3 liquid (30 C, 69.25 bar).
   CHEPTA gives 3.4 %; the whole CO2 recycle (39-REC) follows from it.
2. **Least certain:** HE7: Table S14, p.26 (24.2 MW) against Table S9, pp.12-13, streams 22 (-109.12 MJ/kmol) and 23
   (-110.23 MJ/kmol), 64,042 kmol/h. CHEPTA 25.1 MW.
3. **At random:** article Table 1, p.9, and Eqs. 8-11, p.8: A2 14.41, A3 29.13, E_A2 94.73, E_A3 132.79 kJ/mol, K2 0.1441,
   K3 49.44; phi_Zn 0.10 (p.8).

## Decisions for the maintainer

| # | Decision | Recommendation |
|---|---|---|
| 1 | Keep Model-6p's constants (article Table 1, "reprinted with permission" from ACS) in Lab's files? | Keep: seven numbers of a rate law; the same constants are recoverable from the CC BY supplement (Tables S4, S5, S7). Keep this case out of a commercial training release until rights are reviewed |
| 2 | Accept the plant with the workarounds (trace bypass, bottoms fixed at 4581 kmol/h, HE5 by approach on 10 zones) until CHEPTA answers M1-M4? | Accept as the case's current result; rerun when CHEPTA releases the fixes |
| 3 | The CO2 solubility in the 70 bar flash (3.4 % against 18.5 %) | Record as a disagreement; look for measured CO2 + methanol + water solubility only if the maintainer wants the loop to match |

## What is not in the paper (to choose and record when the plant is run)

- Phases or vapour fractions of the streams (only the steam leaving the reboiler: 0.47).
- The reactor's heat-transfer coefficient to the boiling water (not found in the pages read); compressor
  efficiencies; the column's second specification (only stages, feed stage, reflux ratio 2 and the condenser
  temperature are given) and stage numbering.
- The NRTL2 and Peng-Robinson parameters (Aspen databank, not printed).
- Rights: Table 1 of the article (kinetic parameters, Model-6p) is "reprinted with permission" from an ACS paper:
  check before transcribing it; this case has not copied it.

## What CHEPTA 0.6.2 could probably do (written before the runs, 2026-11-13; kept)

From the documentation and code of the npm package `chepta@0.6.2` and the methanol separator case, before any run. The
runs above replace it: the reactor and the units worked; the column needed workarounds.

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
| [model.py](model.py), [run_chepta_0.6.2.py](run_chepta_0.6.2.py) | the requests and the runner |
| [results-chepta-0.6.2/](results-chepta-0.6.2/) | every request, output and stderr, the run manifest, comparison.json |
| [compare.py](compare.py), [COMPARISON.md](COMPARISON.md) | the comparison, generated |
| [CAPABILITY_REQUESTS.md](CAPABILITY_REQUESTS.md) | requests M1-M5 for CHEPTA |
| [build_study_record.py](build_study_record.py), [study-record.json](study-record.json) | the study record |

Reproduce from the repository root: `npm ci`, then `python3 cases/methanol-co2-campos-2022/run_chepta_0.6.2.py`
(groups with `MEOH_GROUPS`, single runs with `MEOH_ONLY`; a rerun gets a new id), `compare.py`, `build_study_record.py`.
The committed request files are the record of what was run: model.py changed between attempts.

PDFs not in the repository: article sha256 `8215079335f33a55bf972db7e365275e51cdaff4f8cfc685603f1359f4b0447d`,
supplement sha256 `015d60b56ef5d6c0f418257004b39e8053dd7dadeb79d49e284f6dbd3b1a2245` (both from mdpi-res.com).
