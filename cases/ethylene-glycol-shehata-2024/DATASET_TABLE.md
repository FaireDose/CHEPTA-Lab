# Dataset table: ethylene glycol plant (Shehata, Nady & Gad 2024), for the maintainer

Before any CHEPTA run (docs/HANDOVER.md, queue item 5). Paper: *Sci. Rep.* 14, 28375 (2024), CC BY 4.0. Direct
hydration of ethylene oxide (EO) to monoethylene glycol (MEG), 600,000 t/yr, simulated by the authors in Aspen HYSYS 11.
All numbers below are the authors' simulation unless marked **derived** (Lab's arithmetic, in STREAM_AUDIT.md).
Written by an AI session on 2026-11-27; not checked by a person.

## 1. Streams (Table 3 and Fig. 5, p.10)

| Stream | What | kmol/h | Main content (mole fraction) | T, P (Fig. 5) |
|---|---|---:|---|---|
| Ethylene Oxid | fresh EO | 1160 | EO 1.0 | 149.6 C, 3534 kPa |
| WATER MKUP | fresh water | 1130 | water 1.0 | 30 C, 3500 kPa |
| 11 | recycled water | 9870 | water 0.9812, EO 0.0173, MEG 0.0015 | 1.13 C, 3500 kPa |
| 4 | reactor outlet | 11,000 | water 0.8803, MEG 0.1024, EO 0.0155, DEG 0.0010, TEG 0.0008 | 199 C, 3480 kPa |
| 10 | reactor vapour | 0 | - | 199 C, 3480 kPa |
| 5, 6, 1 | liquid after evaporators 1, 2, 3 | 10,190; 8987; 7935 | MEG 0.110, 0.124, 0.140 | 202.8 / 175 / 150 C; 1600 / 804.5 / 400 kPa |
| WATER REC | all vapours, mixed | 9867 | water 0.9812, EO 0.0173 | 48.17 C, 15 kPa |
| MEG Column FEED | dry glycols | 1133 | MEG 0.9802, DEG 0.0097, TEG 0.0079 | 149 C, 20 kPa |
| MEG = 21 = MEG To Storage | product | 1113 | MEG 0.9977, water 0.0023 | 136.7 C / 137.1 C / 34.65 C |
| DEG+TEG | heavy product | 20.43 | DEG 0.5373, TEG 0.4396, MEG 0.0231 | 190 C, 13 kPa |

16 more streams on Fig. 5 have T and P but no flow (the evaporator vapours, the column distillate, the feed train).

## 2. Units and their printed specifications

| Unit | Printed | Missing |
|---|---|---|
| Hydration reactor | 199 C, 3480 kPa; conversion reactor; outlet = stream 4; (text) plug flow 77.8 m x 0.55 m, 3 min | **kinetics**; which selectivity is right (85/15 in Table 1, 98/2 from Table 3) |
| Feed heater E-100 | 44,462.57 kW (Table 8), 4.446 MW (text) | which of the two |
| 3 evaporators | 1600, 804.5, 400 kPa; 8,880, 3,839, 5,038 kW | targets of the 3 adjust blocks; vapour flows (derived by difference) |
| Dehydration column | 15 trays, 15/20 kPa; 107.4 / 94.1 MW | feed tray, reflux, distillate rate |
| MEG column | 26 trays, 12.5/13 kPa; 21.5 / 20.9 MW | feed tray, reflux; side draw (text) or distillate (Fig. 5) |
| Exchangers, pumps | outlet T and P on Fig. 5; chiller 16.6 MW | E-105 duty (two process sides) |

## 3. Does the paper balance?

| Check | Result |
|---|---|
| Reactor (atoms C, H, O) | **closes** within rounding |
| Evaporators + dehydration column, against the mixed water | **closes** |
| Water recycle (WATER REC 9867 against 11 at 9870) | **does not close: 3 kmol/h water** |
| MEG column water (feed 0.0, products 0.0023) | **does not close: 2.6 kmol/h** |
| Whole plant (atoms; mass +0.075 %) | atoms close; **water +3.5 kmol/h** (the recycle's 3 kmol/h) |
| Mole fractions summing to 1 | 12 of 14; MEG Column FEED 0.9978, DEG+TEG 1.0023 |

## 4. Planned in CHEPTA (next task, not run)

| Item | Plan |
|---|---|
| Components | water, ethylene-oxide, ethylene-glycol, diethylene-glycol; **TEG is not in CHEPTA** |
| Property method | NRTL everywhere, after listing each pair's source; HYSYS used its "glycol package" |
| Reactor | conversion reactor with the three reactions and the extents from Table 3 (derived: 1131.4, 19.8, 8.8 kmol/h); not an independent test |
| Evaporators | valve + flash at the printed pressure, duty scanned to match the liquid flows |
| Columns | rigorous columns at the printed pressures and stages, specified by their outlets |
| Plant | tears at 11 and 22; fresh EO fixed; one water-loop flow fixed, make-up free |
| Compared | MEG purity (±0.001) and flow (±1 %), heavy product, evaporator liquids (±1 %), recycle, bottoms temperatures, duties (reported) |

## 5. Open questions for the maintainer (recommendation first)

1. **TEG:** supply it as user data from an open source (NIST WebBook, ChemSep databank; licences to check), or lump it
   into DEG and say so? *Recommended:* user data if a citable open set exists for every property; otherwise lump and
   leave the heavy-product comparison unevaluated.
2. **MEG draw:** distillate as Fig. 5 shows, or side stream as the text says? *Recommended:* distillate first, side
   draw as a variant.
3. **Feed heater:** compare with Table 8 (44.46 MW) or the text (4.446 MW)? *Recommended:* run the heater on its
   printed inlet and outlet and report which it supports; the sensible heat of about 254 t/h warmed by 159 K points to
   Table 8 (Lab's rough reasoning, to be confirmed by the run).
4. **Water loop:** fix the make-up at 1130 kmol/h as the paper did, or fix a recycle flow and let the make-up follow?
   *Recommended:* the second, with the paper's choice as a variant.
5. **Comparison tolerances** (record.json): approve or change.
6. **EO above its critical temperature in the reactor?** If CHEPTA's activity model refuses EO at 199 C, run the
   reactor at the paper's outlet only through the conversion block, or ask CHEPTA? *Recommended:* first see what the
   pinned release does; file a capability request only if no setting near the paper's works.
