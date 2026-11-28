# Dataset table: n-butyl acetate plant (Al-Rabiah et al. 2022), for the maintainer

Before any CHEPTA run. Paper: *Processes* 10, 1801 (2022), CC BY 4.0. n-Butanol + acetic acid to butyl acetate over
Amberlyst-15, 92,500 t/yr, simulated by the authors in Aspen Plus with NRTL. All numbers are the authors' simulation
unless marked **derived** (Lab's arithmetic, in STREAM_AUDIT.md). Written by an AI session on 2026-11-27; not checked
by a person.

## 1. Streams (Table 7, p.14; Figure 11, p.11), kmol/h

| Stream | What | Butanol | Acid | Ester | Water | Diol | T (K), P (kPa) |
|---|---|---:|---:|---:|---:|---:|---|
| 1, 2 | fresh acid, fresh butanol | 0 / 100.1 | 100.9 / 0 | | | | 298.2, 111 |
| 3 | reactor feed (with recycle) | 143.1 | 142.7 | 0.9 | 0 | 0 | 298.2, 111 |
| 4 | reactor outlet | 43.2 | 42.8 | 100.8 | 99.9 | 0 | 363.3, 304 |
| 5 | T-101 top (vapour) | 43.1 | 41.8 | 0.9 | 99.9 | 0 | 411.1, 284 |
| 6 / 7 | ester before / after cooler | 0.1 | 1.0 | 99.9 | 0 | 0 | 444.9, 324 / 308.2, 132 |
| 9 | solvent to T-102 | | | | | 440.3 | 507.0, 121 |
| 10 | wastewater | 0.1 | | | 99.9 | 0.4 | 373.1, 111 |
| 11 | T-102 bottoms | 43.0 | 41.8 | 0.9 | 0 | 439.9 | 462.6, 142 |
| 12 | acid + butanol recycle | 43.0 | 41.8 | 0.9 | | 0 | 393.6, 132 |
| 13 / 14 | solvent before / after cooler | | | | | 439.9 | 512.2, 142 / 303.2, 132 |
| 8 | solvent make-up | | | | | 0.4 | 298.2, 121 |

## 2. Units

| Unit | Printed | Missing |
|---|---|---|
| R-101 fixed bed | Amberlyst-15, 363 K, 1:1, feed 284 kPa, 41 m3 (Table 6); 69.8 % conversion (p.11); kinetics Eqs. 13-15 | units of the rate law, catalyst load, diameter, duty |
| T-101 ester column | pressures from its streams (284/324 kPa) | stages, feed stage, reflux, condenser |
| T-102 extractive | 29 stages, solvent at the top (p.12) | feed stage (13-14 read from Figure 15), reflux |
| T-103 solvent recovery | pressures from its streams (132/142 kPa) | stages, feed stage, reflux |
| E-101, E-102 | outlet T and P | duties (**derived**: -998 and -6143 kW) |
| Utilities | 218,729 MWh/yr steam, 215,504 MWh/yr cooling water (Table 10) | operating hours (8000 h/yr **derived**) |

## 3. Does the paper balance?

| Check | Result |
|---|---|
| Material, every block and the plant | **closes** (0.00 kmol/h; 13,510 kg/h in and out) |
| Reactor | extent 99.9 kmol/h, conversion 69.81 % (text 69.8 %) |
| Energy at V-101 (stream 3) | **does not close**: its enthalpy and temperature are the fresh feeds' alone (recycle's -9060 kW missing) |
| Energy at M-101 (stream 9) | **does not close**: it carries the uncooled solvent's enthalpy (E-102's 6143 kW missing), at 507 K |
| Fresh-feed enthalpies (1, 2) | **-192 and -142 kJ/mol** from CHEPTA's reference; streams 4, 7, 10, 14 agree |
| Text vs figures | 12 disagreements (README), e.g. solvent sent "to T-101" in the text; two pumps named P-102 |

## 4. Rule A (chepta 0.6.3): the plant can start

All five components are present (water, acetic acid with vapour dimer, 1-butanol, n-butyl acetate, 1,4-butanediol).
NRTL pairs: 4 fitted, 3 databank, **3 estimated** (acid + butanol, acid + diol, ester + diol), which rule A allows.
To watch: CHEPTA itself flags the NRTL diol + water set (false two liquids below 323 K); the diol's liquid heat
capacity is fitted only to 353 K but used to 512 K.

## 5. Rules C and D in short

- **Explained by the paper:** the catalyst; extractive distillation with the diol (azeotrope; after Shen et al.); the
  ester column's pressure (stated only for the other route: butanol-ester azeotrope at 1 atm).
- **Not explained, to be learnt by simulation:** 363 K; 284 kPa in the reactor; no decanter; the cooled solvent;
  the solvent ratio; the column pressures, with T-102 and T-103 bottoms (463, 512 K) hotter than the 448 K steam.
- **Product grade:** butyl acetate is a coatings, adhesives, pharmaceutical and flavour solvent (p.1). A supplier
  specification (Eastman 56-12) asks 99.50 % ester and at most 0.0100 % acid. The paper's product: 99.42 wt % ester
  (close) but **0.52 wt % acid** (52 times too much; the fresh acid excess has no other exit).

## 6. Planned in CHEPTA (next task, not run)

NRTL for the whole plant (butanol + water from the set fitted to its two-liquid data), UNIQUAC as a variant. Start at
the reactor inlet with the paper's recycle as a feed; one unit at a time; the solvent loop closed first, then the
reactant loop. Compared (declared now): product purity ±0.002, ester flow 1 %, T-101 top 2 %, wastewater purity
±0.003, recycle 5 %, bottoms temperatures 5 K, cooler duties 10 %.

## 7. Open questions for the maintainer (recommendation first)

1. **Product target:** match the paper's 98.91 mol % (acid 0.52 wt %), or aim at a sales grade (acid ≤0.01 %)?
   *Recommended:* match the paper; report the acid against the grade; a grade-meeting variant later, as design.
2. **Solvent temperature:** cool it in E-102 as drawn (303 K) or feed it hot as the table's stream 9 implies?
   *Recommended:* cooled as drawn; hot as a variant.
3. **Three estimated pairs:** run with Modified UNIFAC 2.0 estimates, or ask CHEPTA to fit them first (one open lead
   only, acid + butanol)? *Recommended:* run with the estimates and record CHEPTA's warning.
4. **Reactor:** conversion imposed from Table 7, kinetic plug flow only as a variant (rate-law units not printed)?
   *Recommended:* yes.
5. **Register:** is butanol esterification the same register problem as the ethanol one already there? *Recommended:*
   keep separate until a CHEPTA run shows the same behaviour.
6. **The comparison tolerances** (record.json) and **the four register rows** (proposed): approve or change.
