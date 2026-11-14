# Ethyl acetate plant (Šulgan, Labovský & Labovská 2020): conventional set-up, prepared for CHEPTA

| In one look | |
|---|---|
| Paper | Šulgan, Labovský & Labovská 2020, *Processes* 8, 1618, doi 10.3390/pr8121618 (CC BY 4.0): ethyl acetate from ethanol and acetic acid; the **conventional set-up** (Figure 1), one of four designs in the paper |
| Plant | 19 blocks: CSTR, azeotropic column C1 (acid removal, with ethyl acetate as entrainer), decanter with wash water, product column C2, water column C3, 7 exchangers (4 heat-integrated), 4 mixers, 3 splitters; 32 streams; 5 recycles. 10 kmol/h each of ethanol and acetic acid in, 10 kmol/h ethyl acetate (99.9 mol %) out |
| Transcribed | all 32 streams of Table 1 (molar flow, 4 mole fractions, T, P, volume flow) in [streams.json](streams.json); all 19 blocks with every printed setting (Table 2 columns, CSTR, decanter, splitters, Table 9 duties) in [equipment.json](equipment.json); each value with its page and table |
| Paper's own balances | **all close within the rounding of the printed digits**: every block, the reactor's atoms, the plant, and every stream's mole fractions ([STREAM_AUDIT.md](STREAM_AUDIT.md)). The energy table agrees with its own totals. Four small disagreements between the text and the tables are kept below |
| Simulated | **nothing yet** (CHEPTA not run in this task) |
| Reviewed by a person | no; draft, written by an AI session on 2026-11-13 |

The paper's numbers are an Aspen Plus V10 simulation (NRTL-HOC, rate-based packed columns), not measurements:
agreement with CHEPTA, later, will be two models agreeing.

## Why this plant

Prepared first, then the task was corrected (the maintainer, 2026-11-13): the next plants are processes 1, 3 and 4. Process 2 is already covered by Piotrowski & Kubica 2021, so this plant is **not one of the first four**: it is kept as a later second ethyl acetate plant (same family; [docs/NEXT_PLANTS.md](../../docs/NEXT_PLANTS.md)). Its mixture is the one
of three rows of [data/ISSUES_AND_ROUTES.md](../../data/ISSUES_AND_ROUTES.md) (ethyl acetate + ethanol + water
azeotrope; acetic acid kept out of the ester; equilibrium-limited esterification), seen so far in one paper only, and
it takes them by other routes than Piotrowski & Kubica 2021: an azeotropic column with the product as entrainer
instead of an absorber-type column, and a decanter with water instead of a countercurrent extractor. Its two-liquid
streams (decanter, C2 top) carry **no acetic acid** in the paper's table, so the plant may close in CHEPTA where the
Piotrowski plant could not. It is in the same process family as the Piotrowski case: keep the two in one group for
any train/test split.

## Flowsheet (Figure 1, p.9; text pp.7-8 and p.11)

| Block | Type (paper) | In | Out | Settings printed |
|---|---|---|---|---|
| MIXAA, MIXETOH, MIXF | mixers | AA0 + W12; ETOH0 + D32; F11 + F21 | F11; F21; R1 | none |
| CSTR | CSTR, adiabatic, liquid-phase kinetics (Eq. 6, p.6) | R1 | P1 | residence time 200 min; liquid volume 8.9 m³ (a result); conversion of acetic acid 53.0 % (a result) |
| EX1 | heat-integrated exchanger | P1, W11 | P2, W12 | 25.01 kW (Table 9) |
| C1 | azeotropic distillation, 60 stages | P2 (stage 35), AZ (stage 34) | D11, W11 | R = 2; x_D11(AA) = 1e-5; x_W11(AA) = 0.70; 1135.23 / 1181.19 kW |
| MIXDEC | mixer | D11, H2OIN, D22, BYPASS, H2OREC | D12 | none |
| EX2 | cooler | D12 | D13 | 133.75 kW |
| DEC | decanter, 25 °C | D13 | ORG, H2OL | water/ester 4.1 mol/mol in D13; 0.85 kW |
| EX3 | heat-integrated exchanger | ORG, D21 | F2, D22 | 31.04 kW |
| C2 | distillation, 60 stages | F2 (stage 36) | D21, W21 | R = 5; x_W21(EtAc) = 0.999; 1212.97 / 1267.94 kW |
| SPETAC | splitter | W21 | AZ, W22 | AZ/W22 = 1 |
| EX7 | cooler | W22 | W23 (product) | 25.85 kW |
| SPBY | splitter | H2OL | BYPASS, F31 | bypass at most 20 % |
| EX4, EX5 | heat-integrated exchangers | F31, D31; F32, W31 | F32, D32; F33, W32 | 13.73; 131.31 kW |
| C3 | distillation, 30 stages | F33 (stage 18) | D31, W31 | R = 4; x_W31(H2O) = 0.999; x_D31(EtOH) = 0.56; 502.97 / 549.35 kW |
| SPH2O | splitter | W32 | H2OREC, H2OP1 | none |
| EX6 | cooler | H2OP1 | H2OP2 (wastewater) | 3.10 kW |

Column internals (packing, diameters, HETP, pressure drops) are in equipment.json. Duties are condenser / reboiler
for the columns, from Table 9 (p.23).

## What the audit found ([STREAM_AUDIT.md](STREAM_AUDIT.md), [balance-results.json](balance-results.json))

Run `python cases/ethyl-acetate-sulgan-2020/audit_balances.py` from the repository root (no third-party packages).

- Every block closes in total moles and in each component within the printed rounding (±0.005 kmol/h, ±0.00005 in
  mole fraction); the CSTR and the plant close in C, H and O atoms; every stream's mole fractions sum to 1.
- Derived from Table 1 and matching the text: conversion per pass 0.5301 (p.8: 53.0 %); water/ester in D13 4.099
  (4.1); decanter ester recovery 0.907 (over 90 %); C2 ester recovery 0.632 (63.2 %); bypass 0.19997 of H2OL (at
  most 20 %); AZ/W22 = 1.
- Table 9 adds up to its own totals (3014.72 kW cooling without the heat-integrated exchangers, 2998.48 kW heating).

### Disagreements kept, not fixed

| # | Where | What |
|---|---|---|
| 1 | p.7 vs Table 1 | The text says C1's bottoms W11 "contains unreacted acetic acid and water"; Table 1 prints W11 as 70.00 % acetic acid, 29.96 % ethyl acetate, 0.04 % ethanol and **no water**. The table balances (C1 closes in water and in ester), so the text is probably loose; to keep in mind when comparing C1 |
| 2 | p.8 vs Table 2 | Text: packings of 25 mm and 35 mm in C1; Table 2: 25 mm and 38 mm |
| 3 | Table 2 | The reaction-mixture feed of C1 is labelled "f P12"; Figure 1 and Table 1 call that stream P2 (read here as P2) |
| 4 | p.21 vs Table 9 | Text: C3 takes 18.4 % of the heating and C1 + C2 81.6 %; Table 9 gives 18.32 % and 81.68 % |
| 5 | Figure 1 | Stream H2OP2 (after EX6) is drawn but not in Table 1; the plant boundary uses H2OP1 |

## What is not in the paper (needed later, to be chosen and recorded when the plant is run)

- Mass flows, enthalpies and phases of the streams (only F33 is marked as vapour + liquid); stream T and P only.
- The concentration of the sulfuric acid catalyst; the units of the activation energy 41,868 (kJ/kmol assumed by
  Lab, with R in kJ/(kmol K): to check). CHEPTA's rate law takes mol/(m³ s) and mol/m³, so the paper's
  kmol-based constants convert (second order: k divided by 1000).
- C2's second specification (only the bottoms purity is printed); the condenser types; stage numbering (Aspen's
  convention assumed: 1 = condenser).
- The NRTL-HOC parameters (Aspen databank, not printed).
- Exchanger areas, U, pressure drops; all columns at 101.3 kPa with packing pressure drops in Table 2.

## What CHEPTA 0.6.2 can probably do, and probably not

From CHEPTA 0.6.2's documentation and code (npm package `chepta@0.6.2`, installed outside the repository for
reading only) and from the Piotrowski case on 0.6.1. **Nothing was run**; each line is an expectation to test.

| Part | Expectation | Why |
|---|---|---|
| Property method | **differs**: CHEPTA has NRTL or UNIQUAC with an ideal vapour that dimerizes acetic acid; no Hayden-O'Connell | 0.6.2 README, "Models"; all six pairs have fitted NRTL and UNIQUAC sets in 0.6.2 |
| CSTR with Eq. 6 | probably yes: CHEPTA's `cstr` takes a liquid volume (8.9 m³ from the paper) and an adiabatic duty (0), with a power-law rate | src/units/kinetic-reactors.js. The 8.9 m³ is the paper's result, not its input (200 min residence was the input) |
| C1 | **uncertain**: a full column (condenser and reboiler) with acetic acid on the lower stages; if a second liquid appears near the top while acid is present, CHEPTA refuses (two liquids with acetic acid, request 1 of the Piotrowski case, being built) | data/ISSUES_AND_ROUTES.md, row sep-two-liquids-with-acetic-acid |
| Decanter, C2, C3 | probably yes: no acetic acid in these streams (Table 1); two liquids without the acid worked in 0.6.1 | Piotrowski runs u3-extr8-*, u3-scds11-* |
| Columns as equilibrium stages | **differs**: the paper's columns are rate-based packed columns; CHEPTA solves equilibrium stages. The stage numbers in Table 2 are the paper's own counts | p.6, Section 2.3 |
| Recycles (5) | probably yes with tear streams; splitters take fractions (AZ/W22 = 1 is a fraction 0.5; the bypass 0.19997) | Piotrowski sections A and B |
| x_D11(AA) = 1e-5 | uncertain: a very tight purity specification | 0.6.1 purity specifications worked but missed the B2 limits |

## Files

| File | What |
|---|---|
| [streams.json](streams.json) | Table 1, 32 streams, unchanged; '-' stored as null |
| [equipment.json](equipment.json) | Figure 1 connections and every printed setting, with locators |
| [audit_balances.py](audit_balances.py) | the audit (reads the two files above) |
| [balance-results.json](balance-results.json), [STREAM_AUDIT.md](STREAM_AUDIT.md) | its results, generated |

The paper's PDF (sha256 `bf5dae4b4990116a190b15f111fac3c59cba4f452e081f94a0ab19293935cb51`, from mdpi-res.com) is
not in the repository. Next step: build the CHEPTA requests from these two files and run the plant, unit by unit then
whole, on the pinned CHEPTA, as in the Piotrowski case.
