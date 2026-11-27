# Run log: ethylene-glycol-shehata-2024 (generated; do not edit)

Run log of the plant, not yet written as lessons. One line per decision or CHEPTA run, grouped by unit, best-supported first; the row id is in an HTML comment for `kb.py show`. A struck-through line was corrected by a later row and no longer counts; the correcting row gives its reason. [All topics](../rules-readable.md)

## distillation (6)

- **Water from a dilute glycol solution: three evaporators at falling pressure, then a vacuum column**
  - When: The reactor effluent holds 88.03 mol % water and 10.24 mol % MEG.
  - Do: Flash it in three evaporators at 1600, 804.5 and 400 kPa, then finish in a 15-tray column at 15/20 kPa ([Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, Table 1).
  - Why: The evaporators take part of the water at higher pressure; the column under vacuum keeps the glycol bottoms cool.
  - Check: MEG column feed carries no water in Table 3; the column duties are 107.4 / 94.1 MW (Table 8).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 5, 'Direct hydration of ethylene oxide' (Fig. 3a description, Eqs. 5-7); Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 8, p. 14, EO-MEG rows; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: Fig. 5 (1600, 804.5, 400 kPa; stream 5 is the first evaporator's liquid), Table 1 (15 trays, 15/20 kPa), Table 3 (stream 4: 88.03 % water, 10.24 % MEG), Table 8 (DEH CON Q 107392.75 kW, DEH REQ Q 94108.24 kW, i.e. 107.4 / 94.1 MW). <!-- ethylene-glycol-shehata-2024.paper-evaporators-and-vacuum-dehydration -->
- **MEG from DEG and TEG: a 26-tray column at 12.5-13 kPa**
  - When: MEG must be parted from the heavier glycols without passing 170 C.
  - Do: Distil at 12.5/13 kPa in 26 sieve trays ([Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y), Table 1).
  - Why: Vacuum lowers the boiling temperatures.
  - Check: MEG 0.9977 mol fraction (Table 3); DEG+TEG bottoms at 190 C in Fig. 5.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 1, p. 3: general assumptions and the direct hydration row; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: Table 1 (26 sieve trays, condenser 12.5 kPa, reboiler 13 kPa), Table 3 (MEG 0.9977), Fig. 5 (DEG+TEG 190 C). <!-- ethylene-glycol-shehata-2024.paper-vacuum-glycol-column -->
- **Plan: specify the vacuum dehydration column by its outlets, not by settings Shehata et al. 2024 does not print**
  - When: 15 trays at 15/20 kPa; feed tray, reflux and distillate not printed.
  - Do: Specify by bottoms water (the published 0 mol fraction cannot be met exactly; scan a small limit) and by distillate flow near 6802 kmol/h (derived); scan feed tray and reflux.
  - Why: The published purities and flows are what CHEPTA should match; its column settings are not given.
  - Check: Bottoms temperature against the published 149 C and the 170 C limit; duties against Table 8 (107.4 / 94.1 MW).
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 5, 'Direct hydration of ethylene oxide' (Fig. 3a description, Eqs. 5-7); Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 8, p. 14, EO-MEG rows; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: bottoms water 0 (Table 3, MEG Column FEED); distillate 6802 kmol/h derived (STREAM_AUDIT.md); 149 C (Fig. 5); 170 C (p. 8); 107.4 / 94.1 MW (Table 8). <!-- ethylene-glycol-shehata-2024.plan-dehydration-column-specs -->
- **Plan: MEG column with MEG as the distillate as drawn; a side-draw variant only if the maintainer chooses it**
  - When: Text says side stream, Fig. 5 shows MEG at the condenser pressure and no other top product.
  - Do: Run 26 stages at 12.5/13 kPa with MEG as distillate specified by purity 0.9977 or flow 1113 kmol/h; compare the bottoms temperature with 190 C and with the 170 C limit.
  - Why: Fig. 5 and the printed pressures agree with a distillate; a side draw would need a top product [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y) does not print.
  - Check: MEG purity and flow; DEG+TEG composition; reboiler and condenser 20.87 / 21.51 MW.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 1, p. 3: general assumptions and the direct hydration row; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: 20.87 / 21.51 MW reboiler / condenser (p. 14); 0.9977, 1113 kmol/h (Table 3); 190 C (Fig. 5); 12.5/13 kPa (Table 1). <!-- ethylene-glycol-shehata-2024.plan-meg-column-distillate-first -->
- **Plan: NRTL for water and the glycols, after checking which pairs CHEPTA has and which it estimates**
  - When: Water, ethylene oxide, MEG, DEG (and TEG) below 10 bar outside the reactor; HYSYS used its glycol package (Table 1).
  - Do: Use NRTL (activity model, ideal-gas vapour) for every unit; first list each pair's source in CHEPTA (databank, fitted, or estimated from Modified UNIFAC 2.0) and compare the key ones (water + MEG, MEG + DEG) with measured data.
  - Why: Associating polar liquids below 10 bar are an activity-model case in CHEPTA's method guide; CPA, the method one glycol paper used, is not in CHEPTA 0.6.2.
  - Check: Every result carries the pairs' tier; estimated pairs are flagged before comparison.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 5, 'Direct hydration of ethylene oxide' (Fig. 3a description, Eqs. 5-7); Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 8, p. 14, EO-MEG rows; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: CHEPTA METHOD_SELECTION.md at v0.6.2 (activity model for polar liquids below 10 bar; Modified UNIFAC 2.0 for missing pairs). <!-- ethylene-glycol-shehata-2024.plan-property-method-nrtl -->
- **Plan: triethylene glycol is not a CHEPTA component; supply it as user data or declare a lumping**
  - When: [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y) carries triethylene glycol (0.08 mol % of the reactor outlet, 44 mol % of the heavy-glycol product), but CHEPTA has no such component.
  - Do: Give CHEPTA triethylene glycol as a user component from an open source with its pure-component constants, vapour pressure, heat capacity and pairs; if none is usable, lump it into DEG and say so in every comparison.
  - Why: Without it, the heavy product and the purification column cannot be compared.
  - Check: The DEG+TEG stream composition and the bottoms temperature.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 1, p. 3: general assumptions and the direct hydration row; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: Table 3 (TEG 0.0008 in stream 4, i.e. 0.08 mol %; 0.4396 in DEG+TEG, i.e. 44 mol %). <!-- ethylene-glycol-shehata-2024.plan-teg-user-component -->

## flash (1)

- **Plan: each evaporator as a valve and a heated flash at the published pressure, its vapour cooled**
  - When: Three evaporators with valves, heat inputs Q1-Q3 and a condenser on each vapour.
  - Do: Run VLV + flash at 1600, 804.5 and 400 kPa with the printed duty (8880, 3839, 5038 kW), and scan the duty to match the liquid flows of streams 5, 6 and 1; cool each vapour to the printed outlet temperature.
  - Why: Matching the liquid flows (the water removed) matters more than the duty, which belongs to HYSYS's property model.
  - Check: Liquid flows 10190, 8987 and 7935 kmol/h; vapours by difference 810, 1203 and 1052 kmol/h (derived).
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 5, 'Direct hydration of ethylene oxide' (Fig. 3a description, Eqs. 5-7); Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 8, p. 14, EO-MEG rows; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: duties Q1 8879.99, Q2 3839.25, Q3 5037.75 kW, rounded 8880, 3839, 5038 (Table 8); liquids 10190, 8987, 7935 kmol/h (Table 3, streams 5, 6, 1); vapours 810, 1203, 1052 kmol/h derived by difference (STREAM_AUDIT.md). <!-- ethylene-glycol-shehata-2024.plan-evaporators-as-flashes -->

## heat exchange (2)

- **Plan: E-105 specified by the product's outlet temperature (34.65 C)**
  - When: E-105 cools the MEG product (137.1 to 34.65 C) against the cold reactor feed (19.65 to 41.12 C); no duty printed.
  - Do: Specify the hot outlet at 34.65 C and compare the cold outlet with 41.12 C; scan the outlet if the approach is too close.
  - Why: Both sides are liquid without phase change, so an outlet temperature is a safe specification.
  - Check: Cold outlet temperature against 41.12 C.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: Fig. 5 (21 at 137.1 C, MEG To Storage 34.65 C, 2 at 19.65 C, 22 at 41.12 C). <!-- ethylene-glycol-shehata-2024.plan-e105-by-hot-outlet -->
- **Plan: run the feed heater on its printed inlet and outlet to see whether it supports 44.46 MW (Table 8) or 4.446 MW (text)**
  - When: [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y) prints the feed heater duty as 4.446 MW (p. 8) and 44462.57 kW (Table 8).
  - Do: Heat the reactor feed from 41.12 C to 200 C at the published pressures (its composition from MIX-100, derived) and read the duty; then give each duty and read the outlet temperature.
  - Why: A unit run on the printed states tells which printed duty is consistent.
  - Check: CHEPTA duty against both values.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 1, p. 3: general assumptions and the direct hydration row; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10. Numbers: 4.446 MW (p. 8); 44462.57 kW, i.e. 44.46 MW (Table 8); 41.12 C (stream 22) and 200 C (stream 3), Fig. 5. <!-- ethylene-glycol-shehata-2024.plan-feed-heater-duty-check -->

## pfr (2)

- **Ethylene oxide hydration: liquid reactor at 199 C and 3480 kPa with about 10 mol water per mol oxide**
  - When: Ethylene oxide reacts with water to MEG, and with MEG and DEG to the heavier glycols.
  - Do: Run the reactor in the liquid at 199 C and 3480 kPa with about 10 mol of water per mol oxide ([Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y), p. 8).
  - Why: The water excess makes the oxide meet water rather than glycol.
  - Check: Outlet 88.03 / 1.55 / 10.24 / 0.10 / 0.08 mol % water / EO / MEG / DEG / TEG (Table 3, stream 4).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 1, p. 3: general assumptions and the direct hydration row; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10. Numbers: Shehata et al. 2024, p. 8 (199 C, 3480 kPa, water to EO 10:1) and Table 3, stream 4 (p. 10). <!-- ethylene-glycol-shehata-2024.paper-reactor-water-excess -->
- **Plan: no rate law, so impose the reactor's extents from the published streams**
  - When: [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y) gives no kinetics: HYSYS used a conversion reactor and Table 3 gives the outlet.
  - Do: Model the reactor as a conversion reactor with the three reactions and the extents fitted from Table 3 (1131.4, 19.8 and 8.8 kmol/h for Eqs. 5, 6, 7; derived), at 199 C and 3480 kPa, liquid outlet.
  - Why: Imposing what the published streams show is the only reactor [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y) support; the reactor is then not an independent test.
  - Check: The outlet equals stream 4 by construction; the reactor duty (Q-100 -32.9 MW) is the comparison.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 1, p. 3: general assumptions and the direct hydration row; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), p. 8, 'MEG production via direct EO hydration process'; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10. Numbers: extents 1131.4, 19.8 and 8.8 kmol/h for Eqs. 5, 6 and 7 derived from Table 3 (cases/ethylene-glycol-shehata-2024/STREAM_AUDIT.md); Q-100 -32917.29 kW, i.e. -32.9 MW (Table 8). <!-- ethylene-glycol-shehata-2024.plan-reactor-conversion-from-table3 -->

## recycle (2)

- **Water recycle about 8.5 times the fresh oxide, with a fresh-water make-up for the water reacted**
  - When: The reactor needs about 10 mol water per mol oxide but only 1 mol reacts.
  - Do: Collect all evaporator vapours and the column distillate, cool, pump and return them; add fresh water for what reacts ([Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, Table 3).
  - Why: Only the water consumed and lost with the products must be fresh.
  - Check: Stream 11 9870 kmol/h; WATER MKUP 1130 kmol/h; fresh EO 1160 kmol/h (Table 3).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: Table 3 (11: 9870 kmol/h; WATER MKUP 1130; Ethylene Oxid 1160; MEG 1113), Fig. 5 (streams 5 and 12, 13). <!-- ethylene-glycol-shehata-2024.paper-water-recycle -->
- **Plan: tear the water recycle at stream 11, fix one flow in the loop, let the make-up follow**
  - When: A water loop of about 9870 kmol/h with 1130 kmol/h fresh water, and E-105 joining the MEG product to the reactor feed (a second cycle).
  - Do: Tear stream 11 (and the E-105 cold outlet 22) from the Table 3 / Fig. 5 values; fix the fresh EO at 1160 kmol/h and the recycle (or the reactor water/EO ratio) and let the fresh water follow; Broyden first; check each component of the tear, then tighten from the saved answer.
  - Why: With every outlet and the make-up fixed, the water balance over-specifies the plant; the published own loop leaves 3 kmol/h open.
  - Check: Tear closure per component; water make-up against 1130 kmol/h; MEG product against 1113 kmol/h.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Table 3, p. 10; Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Fig. 5, p. 10. Numbers: streams 11 and 22 of Fig. 5 (p. 10); recycle mismatch 3 kmol/h and fresh EO 1160, make-up 1130, MEG 1113 kmol/h from Table 3 (p. 10). <!-- ethylene-glycol-shehata-2024.plan-water-loop-tear-and-make-up -->
