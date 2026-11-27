# The one-step methanol plant on chepta 0.6.3 (2026-11-27)

Lacerda de Oliveira Campos et al. 2022, *Processes* 10, 1535 (doi 10.3390/pr10081535, CC BY 4.0). Engine: Lab's pin
`chepta@0.6.3` from npm (package.json; package-lock.json integrity sha512-sGOG6fD7...), tag v0.6.3 = commit b6598a5 by
CHEPTA's notes. Reporting note for CHEPTA: the result header's `which.engine.commit` is not CHEPTA's commit. Installed
under Lab's `node_modules/`, the command line runs `git rev-parse HEAD` in Lab's own repository, so the runs report
Lab's commit 8b8b64f (the merge of Lab's PR #35), with `local_changes: true`. There is no engine disagreement. The
summaries regenerated with `chepta summary` (below) report `commit: null`.

Only what CHEPTA's 0.6.3 advice changes was run (the maintainer, relayed by Lab's coordinating session on 2026-11-27:
do not re-run the 0.6.2 tests to compare). The case README is sealed and unchanged; it describes the 0.6.2 and 415da41
work. Draft, written by an AI session; **no review by a person or by a separate AI session**.

Files: every run as `<id>.request.json`, `<id>.output.json` (CHEPTA's full result, unchanged), `<id>.summary.json`
(`chepta summary`), `<id>.stderr.txt`; [run-manifest.json](run-manifest.json) (command, time limit, exit code, CHEPTA run
id, sha256 of each file). Runner: [../run_chepta_0.6.3.py](../run_chepta_0.6.3.py); CO2 check:
[../co2_solubility_check.py](../co2_solubility_check.py) and [co2-solubility-check.json](co2-solubility-check.json).
54 runs (two added after the AI review: col-mhv1-TB374.1, plant-pr-B4581), 19 refusals or failures. Kinds: CHEPTA's numbers are **simulated**; the paper's are an Aspen Plus V10
**simulation** (PR in the reactors, NRTL2 elsewhere); the ThermoML points are **measured**; interpolations, K values and
recoveries are **derived** by Lab.

## In one look

| Item | Outcome on 0.6.3 |
|---|---|
| Thermo PR + gE (MHV1) | T-P flashes, compressors, HE2, HE7, the reactor and the column run. **Every unit solved through a P-H flash on these mixtures fails**: MIXER1, MIXER4, VALVE1, HE4, HE5, HE6 alone on the paper's inlets (`NO_CONVERGENCE`, "PR: no physical root at 40-84 K"). Smallest input: H2 + CO2 + water, an adiabatic heater at 33 C, 100 kPa |
| Closed plant on PR + MHV1 | **does not converge**: from the paper's start it stops at MIXER1 (`NO_CONVERGENCE`, "PR: no physical root at 84.2 K, 100 kPa"); from the 415da41 plant's tears at CP3 (`PHASE_SPLIT`, PR flash at 300 K and 7000 kPa). CHEPTA's known limit, its first 0.6.4 item; not worked around |
| Closed plant on PR (k_ij) with every other 0.6.3 change | **converges** from the paper's start (current result plant-pr-B4581: 28 loop iterations, 750 s, balance passed): vapour + liquid condenser at the paper's 53 C (M6 answered), H2/CO/N2 through the column (no bypass), HE5 at 2 K without `zones`, reactors at U 155, column bottoms at the paper's 4581 kmol/h. Methanol 99.717 % (paper 99.667), water 99.9996 % (99.985) |
| Separator CO2 | PR + MHV1: **2.35 mol %** in stream 24; PR: 3.41 %; measured basis about 2 %; the paper 18.5 % (section below) |
| HE5 at 2 K without `zones: 10` | solves on the paper's streams (113.9 MW; paper 103.3 MW, Table S14) and on the 0.6.2 plant's streams (93.5 MW; 415da41 refused them as a cross); smallest difference along the exchanger 2.000 K, at the zone boundaries 2.27-2.49 K |
| Reactor at U 155 | outlet 247.96 C, methanol 7.539 % (PR); 0.6.2 at U 150: 247.97 C, 7.540 %; paper 247.9 C, 7.415 % |
| Column specification | chosen by the purities (SIMULATION_PRACTICES: match purities, not the paper's settings). The paper's bottoms flow 4581 kmol/h meets both product purities best and is the current result. The reboiler temperature (scanned 372.75-374.1 K) converges but falls short on water purity. A flow ratio, a methanol recovery and a component ratio that converged columns already satisfy run out of time (M9) |

## Adjustment table (docs/SIMULATION_PRACTICES.md)

Settings that differ from the paper in the 0.6.3 runs. The 0.6.2 rows still apply where not replaced (case README,
"What Lab had to choose").

| Unit | Setting | Paper | Ours | Change | Why | Runs |
|---|---|---|---|---|---|---|
| all | property method | PR in the reactors, NRTL2 elsewhere (article p.9) | PR + MHV1 for units and the plant attempt; PR (k_ij) for the closed plant | method | CHEPTA advice 2; no NRTL pairs for the gases. PR + MHV1 cannot close the plant on 0.6.3 (above), so the closed plant is on PR | u-*-mhv1, plant-mhv1*, plant-pr* |
| REACTOR1, 2 | overall U | 160 inlet, 150 outlet, 155 average used (article pp.13-14) | 155, constant | none (0.6.2 assumed 300) | the paper's own average; CHEPTA takes one U, as Aspen did | u-reactor-U155-*, plant-pr*; U 300 kept as plant-pr-warm-U300 |
| HE5 | specification | hot outlet 62 C, cold outlet 82.9 C (Table S9) | `dTmin_K: 2`, no `zones` | approach in place of an outlet (unchanged from 0.6.2); `zones: 10` dropped | the paper's outlets cross in CHEPTA's loop (0.6.2 runs); feature 9 holds 2 K along the exchanger | u-he5-*, plant-pr* |
| COLUMN | second and third specification (current result) | reflux ratio 2, condenser 53 C, vapour + liquid distillate (supplement p.10); 30-WATER 4581 kmol/h, 99.985 % water, 99.6 C (Table S9/S10) | reflux ratio 2 (over the liquid distillate), condenser 53 C, **bottoms 4581 kmol/h** | none on the flow (the paper's value) | judged on the purities of Campos et al. 2022 (99.667 % methanol, 99.985 % water): in the plant 99.717 / 99.9996 %, closer on both ends than the reboiler variant (99.835 / 99.929 %); alone 99.827 / 99.9925 % | col-mhv1-B4581, plant-pr-B4581, plant-pr-warm-B4581 |
| COLUMN | reboiler temperature (scanned variant, not the current result) | 30-WATER at 99.6 C | 372.75 to 374.1 K scanned; 374.0 K used in plant-pr | +1.25 K at 374.0 K | at the paper's 99.6 C the bottoms are 99.0 % water: CHEPTA's bottoms at 99.99 % water sit at 101.0 C, its water boiling about 1.4 K above 99.6 C at 100 kPa. 374.0 K: 99.884 % alone, 99.929 % in the plant; 374.1 K: 99.952 % alone; 374.5 K refused (range to 374.171 K). 99.985 % lies between 374.1 and 374.171 K, not run | col-mhv1-TB*, plant-pr, plant-pr-warm, plant-pr-warm-U300 |
| COLUMN | gas traces | in the feed (Table S10, 29) | in the feed | none (0.6.2 bypassed them) | the 0.6.3 column starts with them | col-*, plant-pr* |
| COLUMN | condenser | 53 C | 53 C | none (415da41 needed the vapour share 0.0084) | 0.6.3 starts the temperature-specified condenser | plant-pr* |

### Column scan (paper feed 29 with its traces, 30 stages, feed 24, 100 kPa, R 2, 53 C, PR + MHV1)

| Run | Third specification | Outcome | 31-MEOH kmol/h, methanol % | 30-WATER kmol/h, water % | Time |
|---|---|---|---|---|---|
| **col-mhv1-B4581** | **bottoms 4581 kmol/h (current)** | ok | 4533.0, 99.827 | 4581.0, 99.9925 (101.01 C) | 21 s |
| col-mhv1-TB372.75 | reboiler 372.75 K (paper's 99.6 C) | ok | 4487.1, 99.831 | 4626.7, 99.009 | 30 s |
| col-mhv1-TB373.15 | 373.15 K | ok | 4500.4, 99.831 | 4613.4, 99.294 | 33 s |
| col-mhv1-TB373.5 | 373.5 K | ok | 4511.9, 99.831 | 4602.0, 99.539 | 32 s |
| col-mhv1-TB374.0 | 374.0 K | ok | 4527.8, 99.831 | 4586.2, 99.884 | 69 s |
| col-mhv1-TB374.1 | 374.1 K (after review) | ok | 4531.0, 99.831 | 4583.0, 99.952 | 96 s |
| col-mhv1-TB374.5 | 374.5 K | `OUT_OF_RANGE`: "stays between 356.672 ... and 374.171" with R 2 | | | |
| col-mhv1-BF0.485 | flow ratio bottoms/feed 0.485 | `OUT_OF_TIME` at 1200 s | | | |
| col-mhv1-BF0.48672 | 0.48672 (= 4581/9412, derived) | `OUT_OF_TIME` at 300 s | | | |
| col-mhv1-BF0.488 | 0.488 | ok | 4520.9, 99.831 | 4593.1, 99.734 | 37 s |
| col-mhv1-recMeOH0.955 | methanol recovery to the liquid distillate 0.955 | ok | 4505.5, 99.831 | 4608.4, 99.403 | 72 s |
| col-mhv1-recMeOH0.96115 | 0.96115 (paper, derived: 4542 × 0.99667 / (9412 × 0.50041)) | `OUT_OF_TIME` at 300 s | | | |
| col-mhv1-recMeOH0.965 | 0.965 | `OUT_OF_TIME` at 300 s | | | |
| col-mhv1-ratioB5e-05 | bottoms methanol/water 5e-5 | ok | 4665.9, **97.182** | 4455.2, 99.995 | 289 s |
| col-mhv1-ratioB0.00015 | 1.5e-4 (paper, derived: 0.015/99.985) | `OUT_OF_TIME` at 300 s | | | |
| col-mhv1-ratioB0.0005 | 5e-4 | `OUT_OF_TIME` at 300 s | | | |
| col-pr-B4581 | bottoms 4581, PR | ok | 4532.7, 99.835 | 4581.0, 99.9981 | 8 s |

All converged columns: vapour distillate 32 about 298 kmol/h at 38.0 % CO2 (paper 289, 36.9 %). Derived from
col-mhv1-B4581: the 53 C vapour takes 3.91 % of the feed methanol (paper 3.86 %). The time-outs are not unreachable
values: converged columns bracket five of the six (methanol recovery 0.95826 to 0.96274, bottoms/feed 0.47336 to
0.48800, bottoms methanol/water 5.0e-5 to 2.67e-3; table in M9); only the recovery 0.965 lies outside. The first BF0.48672 attempt (1200 s limit)
was stopped by Lab before it finished and has no result; its request file was removed. It was identical to the kept
col-mhv1-BF0.48672.request.json: the time limit is a command-line flag (`--time-ms`), not part of the request. It was
rerun at 300 s (manifest, `interrupted`).

## The closed plant against the paper

Current result: **plant-pr-B4581** (PR, the paper's start, column bottoms 4581 kmol/h; 28 loop iterations, 750 s,
balance check passed, largest component imbalance 0.0009 kmol/h). The same specification from the 415da41 plant's
tears (plant-pr-warm-B4581, 16 iterations) gives the same streams. The reboiler variant (plant-pr, 374.0 K; 29
iterations) is kept for comparison. Simulated against simulated.

| Stream | **0.6.3 plant-pr-B4581 (current)** | 0.6.3 plant-pr (reboiler 374.0 K) | 0.6.2 plant-a6 | Paper (Table S9/S10, S14) |
|---|---:|---:|---:|---:|
| **31-MEOH** | 4549.4 kmol/h, methanol **99.717 %**, CO2 0.165, water 0.118 | 4540.8, 99.835, 0.165, 0.000 | 4548.3, 99.728 | 4542, 99.667, CO2 0.316, water 0.016 |
| **30-WATER** | 4581.0 kmol/h, water **99.9996 %**, 101.02 C | 4589.6, 99.929, 100.85 C | 4581.0, 99.999 | 4581, 99.985, 99.6 C |
| 32 vapour distillate | 38.6 kmol/h, CO2 38.2 % | 38.6, 38.1 % | 38.6 | 289, 36.9 % |
| 24 FLASH3 liquid | 9523 kmol/h, CO2 3.41 % | 9523, 3.41 % | 9522, 3.41 % | 11,488, 18.545 % |
| 39-REC CO2 recycle | 394.4 kmol/h | 394.5 | 394.5 | 2786 |
| 36-REC; 44-PURGE | 52,795; 1077.4 | 52,795; 1077.5 | 52,898; 1080 | 51,504; 1051 |
| 13 reactor feed: flow; T | 72,476 kmol/h; 66.94 C | 72,477; 66.95 C | 72,580 | 73,113; 81.4 C |
| 16 reactor outlet methanol | 7.498 % | 7.498 % | 7.485 % | 7.415 % |
| 2 CO2 compression feed | 5218.4 kmol/h | 5218.5 | 5219 | 7610 |
| condenser; reboiler | 148.3; 65.0 MW | 148.0; 64.7 | 96.5 + 49.4 (flash); 59.6 | 143.6; 53.7 |
| HE4; HE5; HE6; HE7 | 114.1; 93.7; 1.20; 28.7 MW | 114.1; 93.7; 1.20; 28.7 | 114.3; 96.6; -; 25.6 | 105.5; 103.3; 5.0; 24.2 |
| HE5 smallest approach | 2.000 K (zones 2.28 K) | 2.000 K (2.28 K) | 2 K on 10 zones | |
| CP1, CP2, CP3 | 7.90, 7.87, 7.75 MW | 7.90, 7.87, 7.75 | 7.9, 7.9, 7.8 | 10.93, 10.61, 10.81 (from the enthalpies, derived) |
| reactors, each | 35.3 MW to the coolant | 35.3 | | 35.0 (55W - 54W, derived) |

Variant plant-pr-warm-U300 (reboiler 374.0 K, U 300 in place of 155; 42 iterations): against plant-pr the products are
within 0.6 kmol/h (31-MEOH 0.54, 30-WATER 0.51, 39-REC 0.09 kmol/h) and the recycle within 0.2 % (36-REC 103 kmol/h,
stream 33 105 kmol/h); the largest composition difference is 0.026 points (the reviewer's check).

Reading: the methanol and water ends agree with the paper within 0.05 and 0.015 points; the loop still differs where
CO2 dissolves at 70 bar, and on the measured data that difference is the paper's, not CHEPTA's (next section). HE6 is
1.20 MW (paper 5.0): it heats stream 26 to 30 C, and CHEPTA's 26 enters at 25.8 C (paper 18.9 C) because less dissolved
CO2 flashes in VALVE1. HE7 is 28.7 MW (paper 24.2) because HE5 takes 2.9 MW less than on 0.6.2 (the approach now holds
along the exchanger) and HE6 takes little. Stream 13 enters HE4 at 66.9 C (paper 81.4 C): the recycle 36-REC leaves HE2
at 47.5 C (paper 56.7 C); Lab's reading, not checked further: HE2's hot side, the CO2 train (5218 against 7610 kmol/h), carries less heat.

## CO2 in the separator liquid: measured basis against the paper's simulation

Do not tune toward the paper's 18.5 % (CHEPTA advice 1). Checked by Lab against the open ThermoML files (sha256:
Xia 9d248558...0b0561, Bezanehtak f0637187...bc3f92, Xie 0525ee29...59ec22; downloaded 2026-11-27 into
`raw_papers/`, not committed); [co2-solubility-check.json](co2-solubility-check.json).

| Basis | Conditions | x_CO2 in the liquid | K_CO2 = y/x |
|---|---|---:|---:|
| Paper, stream 24 (Aspen NRTL2, simulated; Table S10 p.14) | 30 C, 69.25 bar; gas 33 at y_CO2 0.177 (p_CO2 1226 kPa, derived) | **0.1855** | **0.955** (derived) |
| CHEPTA 0.6.3, PR + MHV1 (simulated; u-flash3-mhv1) | the paper's stream 23 | **0.0235** | 8.74 |
| CHEPTA 0.6.2, PR k_ij (simulated; u-flash3) | the same | 0.0337 | 6.05 |
| Xia et al. 2004, brought to 303.15 K (derived, van 't Hoff form between 313.75 and 354.35 K) | 1:1 solvent, 1226 / 1420 kPa | 0.0215 / 0.025 | |
| Xia et al. 2004 (measured; doi 10.1021/je049803i), 1:1 methanol + water (paper's stream 24 solvent: 0.506 methanol, derived) | 313.75 K, at p_CO2 1226 kPa (interpolated, derived) | **0.018** | |
| Xia et al. 2004 | 313.75 K, at CHEPTA's p_CO2 1420 kPa | 0.021 | |
| Xia et al. 2004 | 313.75 K, **7072 kPa of nearly pure CO2** | 0.108 | |
| Xia et al. 2004, pure methanol (upper bound) | 313.75 K, 1226 kPa | 0.064 | |
| Xie et al. 2005 (measured; doi 10.1021/je0498614), CO2 + methanol (upper bound) | 313.2 K, 1226 kPa (interpolated) | 0.068 | |
| Bezanehtak et al. 2004 (measured; doi 10.1021/je0301491), CO2 + H2 + methanol, no water (upper bound) | 278-298 K, 4-7 MPa, gas 70-75 % H2 | 0.047-0.115 | 2.3-5.7 |

Reading. The paper's liquid holds more CO2 than its own feed and gas: K below 1, although CO2's partial pressure
(1.23 MPa) is far below its vapour pressure at 30 C (about 7.2 MPa) and the gas is 73 % H2. Even under 7 MPa of nearly pure CO2, the 1:1 solvent holds 10.8 %; pure methanol under
H2-rich gas holds at most 11.5 % at 4-7 MPa. At the separator's CO2 partial pressure the measured 1:1 value is about
2 % (1.8-2.1 % at 313.75 K). Brought to the separator's 303.15 K with Xia's own 354.35 K points (derived by Lab and,
independently, by the reviewer: mean x/P of the 1:1 points up to 3.6 MPa, 0.01462 per MPa at 313.75 K and 0.00802 at
354.35 K, ln(x/P) taken as linear in 1/T): about **0.0215 at 1226 kPa and 0.025 at 1420 kPa**. PR + MHV1's 2.35 % at its
own 1420 kPa is consistent with that; PR's 3.37 % (unit run) is high; the paper's 18.5 % is about nine times the
measured basis. Limits: the data sets used have no H2 or N2 in the gas (Xia; the Xie binary set; Xie's H2 sets are
CO2-rich liquids at 8.8-21.8 MPa, far from the separator); the interpolation is linear in total pressure, which includes
about 20 kPa of solvent vapour (Raoult estimate, assumed; x/P of the 1:1 points is 0.0148-0.0152 per MPa from 831 to
7072 kPa, so linear is adequate); the 303.15 K values rest on the assumed temperature form. CHEPTA's own fit statistics (its
lab-notes-0.6.3: PR + MHV1 within 7.9 % on all 221 Xia points) were not re-checked by Lab beyond the 1:1 points above.

## Capability requests for CHEPTA (0.6.3)

Each with one small input file in this folder; full text in [../CAPABILITY_REQUESTS.md](../CAPABILITY_REQUESTS.md),
section "chepta 0.6.3".

| # | Request | Input | Outcome (code and message) | Evidence |
|---|---|---|---|---|
| M7 | P-H flash on PR + MHV1 fails for H2 + CO2 + water | mini-ph-H2-CO2-H2O-mhv1 (adiabatic heater, 33 C, 100 kPa, 39-REC's proportions) | `NO_CONVERGENCE`: "Heater / cooler H1: PR: no physical root at 31.355135405253932 K, 100 kPa." | the same on PR: ok (mini-ph-H2-CO2-H2O-pr); the same with T given on MHV1: ok (mini-tp-...); each pair alone: ok; in the plant it is CHEPTA's known MIXER1 stop, and on the paper's inlets VALVE1, MIXER4, HE4, HE5, HE6 fail the same way |
| M8 | T-P flash on PR + MHV1 refused as a possible liquid-liquid split | mini-tp-cp3-300K-7000kPa-mhv1 (CP3's composition from plant-mhv1-warm's `error.details`, 300 K, 7000 kPa) | `PHASE_SPLIT`: "PR flash at 300.00 K and 7000.00 kPa: the feed is not stable as one phase (tangent-plane distance -0.6174), but no vapour-liquid split was found; it may split into two liquids ..." | on PR: one liquid (mini-tp-cp3-...-pr); 98.2 % CO2 at 70 bar and 300 K is above CO2's vapour pressure (about 67 bar), so one liquid or a VL split is expected, not a refusal |
| M9 | a reachable flow ratio, recovery or component ratio, bracketed by converged columns, runs out of time | col-mhv1-BF0.48672, col-mhv1-recMeOH0.96115, col-mhv1-ratioB0.00015 | `OUT_OF_TIME` at 300 s (BF0.485 at 1200 s), no `details.best` | the ratio 0.48672 is the bottoms flow 4581 kmol/h, which converges in 21 s; converged columns bracket 0.485, 0.96115, 1.5e-4 and 5e-4 (table in CAPABILITY_REQUESTS.md); an out-of-range reboiler temperature is refused at once with its range (col-mhv1-TB374.5) |

## Not done, or unknown

- The CO2 recycle, the compression train and every duty downstream of FLASH3 on PR + MHV1: the plant does not close.
- Whether the paper's 18.5 % comes from NRTL2 parameters or a transcription error in the paper: not known; the
  measured data say only that it is not physical.
- `compare.py` and COMPARISON.md describe the 0.6.2 and 415da41 runs and were not regenerated.
- The 0.6.2 and 415da41 runs were not repeated (the maintainer's instruction).
- The reboiler temperature between 374.1 and 374.171 K, where the paper's 99.985 % water lies: not run (the bottoms
  flow already meets the purities).
