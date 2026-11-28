# n-Butyl acetate, conventional process (Al-Rabiah et al. 2022): prepared for CHEPTA

**In one look**

| | |
|---|---|
| Source | Al-Rabiah, Alqahtani, Al Darwish & Bin Naqyah 2022, *Processes* 10, 1801, doi 10.3390/pr10091801 (CC BY 4.0, p.1) |
| Process | n-butanol + acetic acid to n-butyl acetate over Amberlyst-15 in a fixed bed; ester column; extractive distillation with 1,4-butanediol; solvent recovery; 92,500 t/yr (p.11); Aspen Plus, NRTL |
| Stage | **dataset table** (docs/HANDOVER.md): transcribed, audited, rule A checked. **No CHEPTA plant run.** |
| Material balances | **close within rounding** at every block and over the plant (13,510 kg/h in and out) |
| Energy balances | **do not close** at the two mixers (streams 3 and 9); the fresh feeds' enthalpies disagree with CHEPTA's reference |
| Rule A | all 5 components in chepta 0.6.3; 3 of 10 pairs estimated (allowed); the plant can start |
| Rule D | the paper's product: 99.42 wt % ester, **0.52 wt % acetic acid** (derived) against 99.50 % min and 0.0100 % max in a supplier's sales specification |
| Reviewed? | no; written by an AI session on 2026-11-27 |

For the maintainer: [DATASET_TABLE.md](DATASET_TABLE.md) (one page, with the open questions).

## Flowsheet (Figure 11, p.11; text pp.11-12; Tables 6-7)

Fresh acetic acid (1, 100.9 kmol/h) and n-butanol (2, 100.1 kmol/h) mix with the recycle 12 (85.7 kmol/h of acid and
butanol) in V-101 (stream 3), are pumped (P-101) to the fixed bed R-101 (Amberlyst-15, 41 m3, 363 K, feed 284 kPa,
Table 6), which converts 69.8 % of the butanol. P-102 sends the effluent (4, 304 kPa) to T-101: ester bottoms (6,
444.9 K, 324 kPa) cooled in E-101 to the product (7, 308.2 K); acid, butanol and all the water overhead as a vapour
(5, 411.1 K, 284 kPa) to T-102. T-102 (29 stages) takes 1,4-butanediol at the top (9, 440.3 kmol/h); water leaves
overhead (10, to wastewater treatment), solvent + butanol + acid as bottoms (11) to T-103. T-103 returns the acid and
butanol (12) to V-101 and the solvent (13, 512.2 K) through E-102 (14, 303.2 K) and M-101, where the make-up (8) joins.

Connections were read from Figure 11 by the AI session ([equipment.json](equipment.json)); streams in
[streams.json](streams.json) with CHEPTA component ids.

## What the audit found ([STREAM_AUDIT.md](STREAM_AUDIT.md), [balance-results.json](balance-results.json))

- Every block's component balance closes to 0.00 kmol/h (tolerance 0.10-0.25); mass in = mass out at every block.
- Reactor: extent 99.9 kmol/h, butanol conversion 69.81 % (text: 69.8 %); BuOH/AA 1.0028 in stream 3 (Table 6: 1:1);
  fresh acid 0.8 kmol/h above the butanol, and that excess leaves with the product (1.0 kmol/h acid in stream 7).
- Energy, mixers: V-101's outlet enthalpy equals the fresh feeds alone (the recycle's -9060 kW is missing) and its
  temperature is theirs (298.2 K, although the recycle is at 393.6 K). M-101's outlet (9, 507.0 K) has the enthalpy of
  the *uncooled* solvent 13 plus make-up, exactly, not of 14 (303.2 K) plus make-up: as printed, E-102's 6143 kW of
  cooling is not in the solvent fed to T-102.
- Energy, molar enthalpies: streams 7, 10 and 14 agree with CHEPTA's formation-based liquid reference within the
  sensible heat (+7, +7, -2 kJ/mol); the fresh acid (1) and butanol (2) do not (-192 and -142 kJ/mol). Stream 4 agrees
  (Lab's check, not in the table). The error is therefore in the feed rows, not in Aspen's reference state.
- Duties derived from Table 7 (the paper prints none): E-101 -998 kW, E-102 -6143 kW, T-101 net +2692 kW, T-102 net
  -3246 kW, T-103 net +1245 kW. Lab's estimate of the reactor section with corrected feeds: about -205 kW (heat removed),
  against 813 kW released by the reaction.
- Operating hours (not printed): 92,500 t/yr over stream 7's ester gives 7971 h/yr; the membrane route's utilities give
  8001 h/yr. At 8000 h/yr, Table 10 means 27.3 MW of steam and 26.9 MW of cooling water.
- Product: 98.91 mol %, 99.42 wt % ester (Figure 11 says "99.0% BuAc", "100 km/h").

### The paper's text and figures against its tables (kept, not fixed)

1. Stream 3: enthalpy and temperature of the fresh feeds only (above).
2. Stream 9: enthalpy and temperature of the uncooled solvent (above).
3. Streams 1 and 2: molar enthalpies far from the reference (above).
4. p.12 sends the recovered solvent "to the extractive distillation column (T-101)"; Figure 11 draws it to T-102.
5. Figure 11 names two pumps P-102 (reactor outlet and recycle).
6. Reactor feed pressure 284 kPa (Table 6) against 304 kPa at P-102's outlet after the reactor (p.11); P-101's outlet
   not printed.
7. p.11 cites "Equations (17)-(19)"; the paper has 15 equations.
8. Reactor ~2.5 m long for 69.8 % (p.11), but Figures 12 and 14 run to 14 m; 41 m3 at 2.5 m would need about 4.6 m
   diameter (derived). Figure 12's legend (BuOH blue, BuAc orange) does not match its curves (orange falls from 143,
   the butanol; purple rises to 100, the ester).
9. Solvent make-up 0.375 kmol/h (Figure 11) against 0.4 (Table 7); the 34 kg/h of Table 7 matches 0.375.
10. T-101 distillate printed as vapour (vapour fraction 1) while Figure 11 draws a reflux drum and pump.
11. Bottoms of T-102 (462.6 K) and T-103 (512.2 K) are hotter than the medium-pressure steam named (448 K, p.16);
    T-101's (444.9 K) is 3 K below it.
12. The fixed-bed kinetics imply an equilibrium constant near 5.0 at 363 K (kF/kB, Lab's arithmetic), the membrane
    model 3.51 (Eq. 4); units of Eqs. 13-15 are not printed.

## Rule A: components and property method ([CHEPTA_COMPONENT_REQUEST.md](CHEPTA_COMPONENT_REQUEST.md))

| Item | chepta 0.6.3 |
|---|---|
| Components | water, acetic-acid (vapour dimer), 1-butanol, n-butyl-acetate, bdo (1,4-butanediol): **all present** |
| Records over 298-512 K | all present; liquid heat capacity extrapolated for bdo (record to 353.15 K, used to 512.2 K), butanol (390.81 K) and acid (400 K): CHEPTA continues by the ideal-gas path and warns |
| NRTL pairs | 4 fitted (acid + water, acid + ester, butanol + ester, butanol + diol); 3 databank (butanol + water, ester + water, diol + water); **3 estimated** by Modified UNIFAC 2.0 (acid + butanol, acid + diol, ester + diol) |
| Flagged by CHEPTA | NRTL diol + water: predicts two liquids at 273-323 K where measured as one liquid |

**Method (rule E):** NRTL with an ideal vapour and CHEPTA's acid dimerization, for the whole plant; butanol + water
from the set `fitted-lladosa2008`; UNIQUAC as a whole-plant variant; a column-level method for T-102/T-103 only if
the diol + water split appears at their temperatures. Reasons in [record.json](record.json).

## Rule C: why the paper chose what it chose

| Choice | Reason, with its source | Label | What simulations must show |
|---|---|---|---|
| Fixed bed of Amberlyst-15 | solid acids such as ion-exchange resins catalyse the reaction (p.1); the same catalyst in all routes (p.10) | author-stated | - |
| 363 K | not stated. Equilibrium conversion falls with temperature (Figure 1, Figure 13); the kinetic curve of Figure 13 peaks near 370-375 K (read from the figure) | unresolved | kinetic variant: conversion against temperature |
| 1:1 feed (acid 0.8 % in excess) | for the membrane route: an acid excess raises conversion but makes purification harder (p.6, Figure 5b) | author-stated for the other route; Lab applies it | scan the ratio, watch the acid in the product |
| Reactor at 284 kPa | not stated | unresolved | bubble pressure of stream 3 at 363 K |
| T-101 at 284/324 kPa, ester as bottoms first | for the membrane route's T-101: butanol and ester form an azeotrope at 1 atm and separate at 304 kPa with many stages (p.7, Figure 9); the ester is the heaviest of the four (chepta 0.6.3 boiling points: 399.1, 391.05, 390.7, 373.1 K) | author-stated for the other route; sequence Lab's inference | azeotrope at 101.3 and 304 kPa in CHEPTA |
| Extractive distillation with 1,4-butanediol | butanol and water form an azeotrope; Shen et al. used 1,4-butanediol (p.3, Figure 2) | author-stated | relative volatility with and without solvent |
| No decanter (the same paper's reactive distillation uses one) | not stated | unresolved | does condensed stream 5 split into two liquids with 41.8 kmol/h acid present? |
| Solvent cooled in E-102 to 303 K | not stated; and the table's stream 9 looks uncooled | unresolved | T-102 with cold and with hot solvent |
| Solvent about 2.4 mol per mol of T-102 feed | not stated | unresolved | scan the solvent flow |
| T-102 at 111/142 kPa, T-103 at 132/142 kPa | not stated | unresolved | T-103 at lower pressure: bottoms temperature against 448 K steam |

## Rule D: what the product is for, and what that grade accepts

- **Use (p.1):** a solvent for adhesives, lacquers, coatings and paints; an extraction agent or solvent in
  pharmaceuticals and cosmetics; fruit flavours. The paper names no market or grade for its plant.
- **A grade, with its source:** Eastman Butyl Acetate, Sales Specification No. 56-12 (2008; data/sources.json
  `eastman-butyl-acetate-salespec-56-12`): n-butyl acetate 99.50 % min; acid as acetic 0.0100 % max; water 0.0500 %
  max; isobutanol + butanol 0.25 % max. ASTM D4615 (n-butyl acetate, all grades; coatings solvents) exists but was
  not read (paywalled); a food-grade specification (JECFA no. 127) was not found.
- **The paper's product against it (derived from Table 7):** ester 99.42 wt % (0.08 short: close); acid 0.52 wt %
  (**52 times the limit: not close**); butanol 0.064 wt % (passes); water 0 (passes).
- **Consequence for the runs:** match the paper's purity (98.91 mol %) for the reproduction, and report the acid
  against 0.0100 % separately. Reaching a sales grade would need a design change (the acid excess has no other exit):
  a question for the maintainer, not chased in the reproduction.
- **Wastewater (stream 10):** 99.9 water, 0.1 butanol, 0.4 diol kmol/h: about 2.4 wt % organics (derived), sent to
  treatment (p.12). What a treatment plant accepts was not looked up: open.

## Run plan for the next task (docs/SIMULATION_PRACTICES.md, rules B, E, G, H)

Full plan and the comparisons declared before runs: [record.json](record.json) (`run_plan`, `comparisons_declared`).

| Step | What |
|---|---|
| 0 | Property checks, no plant: pair tiers; diol + water split at 300-470 K; butanol-water azeotrope (p.3: 91.6 C, 23.5 %); butanol-ester azeotrope at 101.3 and 304 kPa; two liquids in condensed stream 5; bubble pressure of stream 3 at 363 K; extrapolation warnings |
| 1 | Start at the reactor inlet: fresh feeds + the paper's recycle 12 as a fixed feed (the reactor is imposed, so every downstream unit gets the paper's flows); stream 4 as T-101's feed only if the reactor step fails |
| 2 | One unit at a time: V-101, P-101, R-101 (conversion reactor, extent 99.9 kmol/h, 363 K), P-102, T-101 (bottoms purity), valves, E-101, M-101 (paper's solvent as feed), T-102, T-103, E-102 |
| 3 | Close the solvent loop when E-102 is reached (tear 14; circulation fixed, make-up free); then the reactant loop (tear 12) |
| 4 | Whole plant against the declared comparisons; rule G on every stream; rule H timing of every run |
| 5 | Variants: kinetic plug flow reactor; UNIQUAC; T-103 at lower pressure; hot solvent as printed |

Main tolerances (declared 2026-11-27, before runs): product purity ±0.002 mole fraction; ester flow 1 %; T-101
distillate flows 2 % or 0.5 kmol/h; wastewater purity ±0.003; recycle 12 within 5 %; bottoms temperatures 5 K;
E-101 and E-102 duties 10 %.

### Adjustment table

| Unit | Setting | Paper | Ours | Change | Why | Runs |
|---|---|---|---|---|---|---|
| (none yet) | | | | | | |

## Knowledge base

- Rows of this case: `dataset/records/butyl-acetate-al-rabiah-2022.json` (11 evidence blocks, 5 evidence rows,
  4 paper rows, 6 plan rows), all drafts. Plan rows record in `informed_by` which rules helped (planning judgement only).
- Register rows proposed, **awaiting the maintainer** (data/ISSUES_AND_ROUTES.md): `rxn-butanol-esterification-fixed-bed`
  (possibly the same problem as `rxn-esterification-equilibrium-limited`: the maintainer decides),
  `sep-ester-from-close-boiling-acid-alcohol`, `sep-alcohol-water-azeotrope-heavy-solvent`,
  `plant-solvent-recycle-hot-bottoms`.
- Rows of the same paper already in the base (al-rabiah-2022.*) were reused, not copied.

## Files

| File | What |
|---|---|
| streams.json | Table 7, 14 streams, as printed, CHEPTA ids |
| equipment.json | blocks and connections (Figure 11), Table 6, kinetics, assumptions, utilities |
| audit_balances.py | the audit (`python3 audit_balances.py <chepta>/src/data/components.json`) |
| STREAM_AUDIT.md, balance-results.json | its results |
| CHEPTA_COMPONENT_REQUEST.md | rule A handover |
| results-chepta-0.6.3/component-info/ | `component_info` requests and results, chepta 0.6.3 |
| record.json | pre-run record: boundary, method, comparisons declared, run plan |
| build_kb_rows.py | writes the knowledge-base rows (hashes of passages of the ignored PDF text) |
| DATASET_TABLE.md | one page for the maintainer |

The PDF (sha256 9e9ccb94...) and the supplier specification are in the ignored `raw_papers/` folder, not committed.
