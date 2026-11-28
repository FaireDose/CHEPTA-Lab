# Run log: butyl-acetate-al-rabiah-2022 (generated; do not edit)

Run log of the plant, not yet written as lessons. One line per decision or CHEPTA run, grouped by unit, best-supported first; the row id is in an HTML comment for `kb.py show`. A struck-through line was corrected by a later row and no longer counts; the correcting row gives its reason. [All topics](../rules-readable.md)

## distillation (2)

- **Ester from its reactants: one column at about 300 kPa, ester as bottoms, acid, butanol and water overhead**
  - When: The reactor effluent holds butyl acetate (Tb 399 K) with close-boiling acetic acid (391 K) and butanol (391 K) and water.
  - Do: Take the ester as bottoms of T-101 at 284/324 kPa and everything else overhead as a vapour (Table 7).
  - Why: For their membrane route [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) say butanol and ester form an azeotrope at 1 atm and separate at 304 kPa (p.7); for the conventional T-101 they print no reason.
  - Check: Bottoms 99.9 ester, 1.0 acid, 0.1 butanol kmol/h at 444.9 K (stream 6).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 5, p.7 (Figure 9), membrane-reactor route; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14. Numbers: Table 7 streams 4-6 (T-101 284/324 kPa; bottoms 99.9 ester, 1.0 acid, 0.1 butanol kmol/h, 444.9 K); p.7 (azeotrope at 1 atm, split at 304, about 300 kPa); boiling points 399, 391, 391 K rounded from chepta 0.6.3 components.json. <!-- butyl-acetate-al-rabiah-2022.paper-ester-bottoms-at-pressure -->
- **Plan: T-101 at the printed pressures, specified by the ester purity of the bottoms, condenser giving a vapour distillate**
  - When: T-101's stages and reflux are not printed; its distillate is printed as vapour.
  - Do: Keep 284/324 kPa; start from the membrane route's T-101 (42 stages, feed 21; Table 5) as an assumption; specify the bottoms purity (98.91 mol %) and the ester recovery; scan stages and reflux.
  - Why: Purities at the column ends matter more than the printed settings; the acid slip (1.0 kmol/h) has no other exit and sets the purity.
  - Check: Bottoms purity within the declared tolerance; the butanol-ester azeotrope at 101.3 and 300 kPa checked in CHEPTA first.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 5, p.7 (Figure 9), membrane-reactor route; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 1, p.1; Company 2008, *Eastman Butyl Acetate, Sales Specification No. 56-12* (https://www.eastman.com/supplemental/salespecs/71001046.pdf), Sales Specification No. 56-12, p.1 (single table). Numbers: Table 7 streams 4-6 (T-101 at 284/324 kPa; acid 1.0 kmol/h in the bottoms; purity 98.91 mol %, derived); Table 5 p.10 (membrane route T-101: 42 stages, feed stage 21); azeotrope checks at 101.3 and 300 kPa (p.7 gives 304 kPa). <!-- butyl-acetate-al-rabiah-2022.plan-ester-column-purity-spec -->

## extractive distillation (3)

- **Butanol-water azeotrope with acetic acid present: extractive distillation with 1,4-butanediol, then solvent recovery**
  - When: Water must leave a mixture of water, n-butanol and acetic acid, where butanol and water form an azeotrope (91.6 C at 101.3 kPa, Aspen).
  - Do: Feed 1,4-butanediol at the top of a 29-stage column (about 2.4 mol per mol of feed), take water overhead, recover the solvent in a second column and recycle the acid and butanol ([Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801), after Shen et al.).
  - Why: The heavy diol holds butanol and acid in the liquid; [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) follow an earlier design by Shen et al. (p.3).
  - Check: Water 99.9 kmol/h overhead with 0.1 butanol and 0.4 solvent (stream 10).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, p.3 (Figure 2); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14. Numbers: p.3 (azeotrope 91.6 C at 101.3 kPa, Aspen; 1,4-butanediol after Shen et al., ref. 20); p.12 (29 stages); Table 7 streams 5, 9-14 (solvent 440.3 kmol/h against 185.7 kmol/h feed, about 2.4 mol per mol; stream 10 water 99.9, butanol 0.1, solvent 0.4 kmol/h). <!-- butyl-acetate-al-rabiah-2022.paper-extractive-butanediol -->
- **Plan: T-102 with 29 stages, solvent at the top, scan the solvent flow and the feed stage; check two liquids in T-101's condensate first**
  - When: T-102's feed stage, reflux and solvent temperature are not printed (stream 9's 507 K is inconsistent).
  - Do: Run T-102 on stream 5 and stream 9 with the solvent cooled as drawn (E-102 before M-101); feed stage near 13-14 (Figure 15); scan solvent flow around 440 kmol/h; specify water purity overhead and butanol recovery.
  - Why: The solvent ratio and its temperature decide whether water leaves pure; a decanter alternative depends on whether the condensate splits with 42 kmol/h acid present.
  - Check: Stream 10 water 99.5 mol % (0.1 butanol, 0.4 solvent) within the declared tolerance.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, p.3 (Figure 2); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14. Numbers: Table 7 streams 5, 9-11 (440.3, about 440 kmol/h; 507 K; stream 10: 99.9/0.1/0.4 kmol/h, 99.5 mol % water, derived; acid about 42 kmol/h); p.12 (29 stages); Figure 15 (stage 13-14, read); units T-101, T-102, E-102, M-101. <!-- butyl-acetate-al-rabiah-2022.plan-extractive-solvent-scan -->
- **Plan: NRTL with an ideal vapour (acid dimer by chemical theory) for the whole plant; butanol + water from the LLE-fitted set**
  - When: Five polar components at 298-512 K and 111-324 kPa; butanol + water and ester + water form two liquids; acetic acid dimerizes in the vapour.
  - Do: Use NRTL everywhere with the 1-butanol + water set fitted-lladosa2008; let CHEPTA estimate the three missing pairs (acid + butanol, acid + diol, ester + diol) from Modified UNIFAC 2.0 and record its warning; UNIQUAC as a variant.
  - Why: An activity model fits these liquids and NRTL can show two liquids; CHEPTA 0.6.3 has fitted NRTL pairs for four of the ten pairs, databank pairs for three and none for three.
  - Check: Each result lists the pair tiers; CHEPTA's own warning that the NRTL diol + water set predicts a false split below about 323 K is checked at the column temperatures before T-102 is compared.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, p.3 (Figure 2); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 5, p.7 (Figure 9), membrane-reactor route; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction). Numbers: 298-512 K, 111-324 kPa (Table 7); chepta 0.6.3 binaries.json (1-butanol + water set fitted-lladosa2008, fitted to butanol-water liquid-liquid data); known-issues.json (diol + water split to 323.15 K, about 323 K); diol = 1,4-butanediol; column T-102; Modified UNIFAC 2.0. <!-- butyl-acetate-al-rabiah-2022.plan-property-method-nrtl -->

## heat exchange (1)

- **Plan: duties from CHEPTA reported against the stream-table differences, not against the printed feed enthalpies**
  - When: The enthalpies of streams 1, 2 and 3 disagree with CHEPTA's formation-based reference by -142 to -192 kJ/mol; streams 3 and 9 are not adiabatic mixtures.
  - Do: Compare E-101, E-102 and the column net duties with the Table 7 differences (derived); report the reactor duty and the reboiler temperatures against the 448 K steam; treat Table 10 (27.3 MW steam at 8000 h/yr, derived) as reported only.
  - Why: Only the enthalpy differences of consistent streams can be compared.
  - Check: E-101 -998 kW, E-102 -6143 kW, T-102 net -3246 kW, T-103 net +1245 kW (derived).
  - Status: untested — Lab's idea, not yet tested.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 7.1 and Table 10, p.16. Numbers: STREAM_AUDIT.md from Table 7 (streams 1, 2, 3, 9; -142, -192 kJ/mol; -998, -6143, -3246, +1245 kW, derived); p.16 (448 K); Table 10 (27.3 MW at 8000 h/yr, derived); units E-101, E-102, T-102, T-103. <!-- butyl-acetate-al-rabiah-2022.plan-energy-checks -->

## pfr (2)

- **Butanol esterification: fixed bed of acid resin at 363 K with a 1:1 feed, about 70 % conversion per pass**
  - When: n-Butanol and acetic acid react to butyl acetate and water on a solid acid; the equilibrium limits one pass.
  - Do: Run a liquid fixed bed of Amberlyst-15 at 363 K and 1:1 (Table 6) and recycle the unreacted acid and butanol ([Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801)).
  - Why: The reaction reaches about 70 % within a short bed; the remaining reactants are recovered downstream (p.11).
  - Check: Butanol 143.1 to 43.2 kmol/h, ester 0.9 to 100.8 kmol/h across the reactor (Table 7, streams 3 and 4).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6 and 6.1, Eqs. 13-15, p.10; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 6, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14. Numbers: Table 6 p.12 (Amberlyst-15, 363 K, 1:1, 284 kPa, 41 m3); p.11 (maximum about 70 %, 69.8 % within about 2.5 m); Table 7 streams 3 and 4 (butanol 143.1 to 43.2 kmol/h, ester 0.9 to 100.8 kmol/h). <!-- butyl-acetate-al-rabiah-2022.paper-fixed-bed-resin-363k -->
- **Plan: reactor first as a conversion reactor at 69.8 %, then a kinetic plug flow variant**
  - When: The rate law of Eqs. 13-15 has no printed units or catalyst loading.
  - Do: Start the plant with a conversion reactor at 363 K (extent 99.9 kmol/h from Table 7); try CHEPTA's plug flow reactor with Eqs. 13-15 as a variant once a concentration basis is chosen and stated.
  - Why: The conversion per pass sets only the size of the recycle; an imposed conversion is not a test of the reactor.
  - Check: Outlet against stream 4; reactor duty reported ([Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) print none).
  - Status: untested — Lab's idea, not yet tested.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6 and 6.1, Eqs. 13-15, p.10; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 6, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14. Numbers: Table 6 (363 K); p.11 and Table 7 streams 3-4 (69.8 %; extent 99.9 kmol/h, derived); Eqs. 13-15 p.10; equilibrium constant about 5.0 from kF/kB at 363 K (Lab's arithmetic) against 3.51 (Eq. 4). <!-- butyl-acetate-al-rabiah-2022.plan-reactor-kinetic-then-imposed -->

## recycle (2)

- **Two recycles (reactants 85.7, solvent 440 kmol/h) and recovery-column bottoms at 512 K**
  - When: The plant recycles unreacted acid and butanol to the feed vessel and 1,4-butanediol to the extractive column.
  - Do: Close both loops; make up the solvent lost in the wastewater (0.4 kmol/h, stream 8).
  - Why: Unreacted reactants and the solvent are worth recovering (p.12).
  - Check: Recycle 12 = 85.7 kmol/h, solvent 14 = 439.9 kmol/h, make-up 0.4 kmol/h (Table 7); T-103 bottoms 512.2 K against MP steam at 448 K (p.16).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 7.1 and Table 10, p.16. Numbers: Table 7 (stream 12 85.7 kmol/h; stream 14 439.9, about 440 kmol/h; stream 8 0.4 kmol/h; stream 13 at 512.2 K, about 512 K); Figure 11; p.16 (MP steam 448 K). <!-- butyl-acetate-al-rabiah-2022.paper-two-recycles-hot-bottoms -->
- **Plan: tear the two recycles (12 and 14), fix the fresh feeds and the solvent circulation, let the make-up follow**
  - When: Two loops: reactants to V-101, solvent to M-101; [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) fix the fresh feeds.
  - Do: Close the solvent loop first (T-102 + T-103 + E-102 + M-101), then the reactant loop; tears at 12 and 14; solvent circulation fixed, make-up equal to the loss; Broyden; per-component check; tighten from the saved answer; compare every flow (rule G).
  - Why: Fixing one flow inside each loop gives the missing specification; an unconsumed acid excess (0.8 kmol/h fresh) must leave with the product.
  - Check: Recycle 12 within 5 % of 85.7 kmol/h, solvent within 1 % of 440 kmol/h; no flow 10 times larger than in Table 7.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.11 (text overlaid with figure captions in the extraction); Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, p.12; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p.14; Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 7.1 and Table 10, p.16. Numbers: Table 7 streams 1, 2, 8, 12, 14 (100.1 butanol, 100.9 acid, 0.8 more; 85.7; 439.9, about 440 kmol/h); tolerances 5 % and 1 % (record.json); rule G (a flow 10 times larger); units T-102, T-103, E-102, M-101, V-101. <!-- butyl-acetate-al-rabiah-2022.plan-recycles-tears -->
