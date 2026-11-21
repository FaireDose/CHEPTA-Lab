# Rules and decisions in plain words (generated; do not edit)

Each rule starts with what to do in one line. Below it: When (the situation you recognise), Do (what to do, with the source's numbers), Why (the mechanism), Check (how to verify it, in CHEPTA where it applies), Result (what the source got, where it reports one), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested; worked and failed rows cite a paper, a measurement or a CHEPTA run. Rows not yet rewritten in this shape are one line each: the statement, its status and source, then the conditions under which it holds. The row id is in small text for lookup. This page is for people and grows with every row: agents keep using problems.md and `python scripts/kb.py query`, which stay short.

## By register problem

### sep ester alcohol water azeotrope (separation)

- **Shortlist water extraction if two-liquid feasibility and recovery constraints permit. Expected: Enrich the ester-rich phase before further purification.** worked, paper's simulation; Piotrowski & Kubica 2021, Section 1.2, opening paragraph; Piotrowski & Kubica 2021, Section 1.2, purification step (2); Piotrowski & Kubica 2021, Section 3.3, final paragraph. When: water wash of azeotrope, piotrowski 2021 plant s2. <sub>ea-choose-extraction</sub>
- **Consider cooling before extraction within available utility limits. Expected: Case-supported enrichment; quantify actual recovery and duties before claiming a benefit.** worked, paper's simulation; Piotrowski & Kubica 2021, Section 3.3, paragraph after Figure 4; Piotrowski & Kubica 2021, Section 3.3, final paragraph. When: cooling before water extraction, piotrowski 2021 plant s2. <sub>ea-condition-feed</sub>
- **Set purification conditions against all product limits together. Expected: A specification-compliant candidate with quantified recovery and duty.** worked, paper's simulation; Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 3.4, final paragraph. When: product column after wash, piotrowski 2021 plant s2. <sub>ea-purification-constraints</sub>
- **Column 11 alone on the paper's stream 13 without acid, product purity 99.90 wt%. Expected: 99.90 wt% ester at a product flow near the paper's.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, no acetic acid, purity 99.9 specified. <sub>ethyl-acetate-piotrowski-2021.col11-no-acid-purity-spec-061</sub>
- **EXTR 8 with 1-8 stages at 27 C, W/A 1, without acetic acid; 2 stages chosen. Expected: The raffinate of Table A2 (stream 11).** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph. When: unit alone, paper inlets, two equilibrium stages, isothermal 27 c, no acetic acid. <sub>ethyl-acetate-piotrowski-2021.extractor-two-stages-27c-061</sub>
- **The 0.6.1 request sent again unchanged. Expected: Extractor accepts its feed.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: section b, mix 7 adiabatic. <sub>ethyl-acetate-piotrowski-2021.mixer-before-extractor-adiabatic-062</sub>
- **Part of the organic phase (stream 26) returned to column 5 as reflux; the rest goes to the product column. Expected: All reaction water leaves overhead as azeotrope, none accumulates in the reactor.** worked, paper's simulation; Piotrowski & Kubica 2021, p. 3, Section 1.2, purification stage (1). When: piotrowski 2021 plant s2, organic phase recycled as reflux. <sub>ethyl-acetate-piotrowski-2021.paper-organic-phase-as-azeotropic-agent</sub>
- **Water-to-azeotrope mass ratio 1 in S2 (Table 1); the paper's sensitivity gives 1 to 2 as the optimum. Expected: Enough ethanol removed from the organic phase without excessive ester loss.** worked, paper's simulation; Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, p. 11, Table 1. When: piotrowski 2021 plant s2, water to azeotrope 1 to 2. <sub>ethyl-acetate-piotrowski-2021.paper-wash-ratio-1-to-2</sub>
- **Settled closed plant, distillate 260, 270, 280 kmol/h. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 260 to 280 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-062</sub>
- **Settled closed plant, distillate 260, 270, 280 kmol/h. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 260 to 280 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41</sub>
- **Settled closed plant, distillate 246 kmol/h. Expected: Less water in the product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 246 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-distillate-raised-settled-062</sub>
- **Settled closed plant, feed stage 5. Expected: Higher purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 feed stage 5. <sub>ethyl-acetate-piotrowski-2021.col11-feed-stage-5-062</sub>
- **Closed plant from the saved start, tolerance 3e-4, 36, 38, 40 stages. Expected: Higher purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant saved start, column 11 36 to 40 stages. <sub>ethyl-acetate-piotrowski-2021.col11-more-stages-062</sub>
- **Column 11 alone on the paper's stream 13 without acid. Expected: 99.90 wt% ester.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5; Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: standalone product column, paper stream 13 feed, no acetic acid, bottoms flow 141.5 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-no-acid-paper-flow-061</sub>
- **Distillate 250 and 260 kmol/h, with and without the ethanol design specification. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant ethanol feed 6506.23, column 11 distillate 250 to 260 kmol h. <sub>ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41</sub>
- **From the design-specification answer. Expected: Purer product.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: closed plant ethanol feed 6506.23, column 11 distillate 270 kmol h. <sub>ethyl-acetate-piotrowski-2021.ds-start-distillate-270-415da41</sub>
- **Settled closed plant, extractor at 20 C (Lab's 27 C). Expected: Drier raffinate.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, extractor 20 c. <sub>ethyl-acetate-piotrowski-2021.extractor-20c-062</sub>
- **Settled closed plant, 3 and 4 extractor stages. Expected: Drier raffinate.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: closed plant settled, extractor 3 or 4 stages. <sub>ethyl-acetate-piotrowski-2021.extractor-more-stages-062</sub>
- **EXTR 8 at 70 C with the paper's feed, and with a liquid feed. Expected: Two liquid outlets.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: unit alone, paper temperature 70 c. <sub>ethyl-acetate-piotrowski-2021.extractor-paper-70c-061</sub>
- **Section B with MIX 7 adiabatic. Expected: Extractor accepts its feed.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: section b, mix 7 adiabatic. <sub>ethyl-acetate-piotrowski-2021.mixer-before-extractor-adiabatic-061</sub>
- **Settled closed plant, recycle 23 = 121,000 kg/h (W/A 1.13) and 144,000 kg/h (1.4); also with feed stage 5. Expected: Drier raffinate, purer product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, recycle 23 raised wa 1.13 to 1.4. <sub>ethyl-acetate-piotrowski-2021.wash-water-raised-062</sub>
- **A reading of Table A2 and Section 3.4 by Lab; confirmed as a table error for the acid by the maintainer (spot check, 2026-11-13). Expected: A future case should not take the paper's 99.90 % as reachable at its own settings.** lead, Lab's reasoning; Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: piotrowski 2021 plant s2, paper column 11 water balance. <sub>ethyl-acetate-piotrowski-2021.open-paper-col11-water-balance</sub>
- **The paper's literature review names extractive distillation with a heavy solvent, and pervaporation, for this azeotrope, and rejects both because each needs a second method to reach product purity.** lead, book or review; Piotrowski & Kubica 2021, Section 1.2, p. 3 (literature review, refs 23-28). When: named in literature review. <sub>ethyl-acetate-piotrowski-2021.review-extractive-distillation-needs-second-step</sub>
- **Not run: needs a column flow as a design-specification variable (request 16) and convergence of column 11/15 at higher loads (requests 13, 19). Expected: 99.90 % ester with water below 0.03 %.** untested, Lab's reasoning; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5; Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph. When: closed plant, drier raffinate and more distillate. <sub>ethyl-acetate-piotrowski-2021.open-reach-99.9-pct</sub>

### sep two liquids with acetic acid (separation)

- **The 0.6.1 requests sent again unchanged. Expected: Duties and outlets of Table 1 and Table A2.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, acetic acid 0.01 mass pct. <sub>ethyl-acetate-piotrowski-2021.acid-two-liquids-units-062</sub>
- **Column 11 alone, bottoms 140.5 kmol/h (paper 141.5). Expected: 99.90 wt% ester.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140.5 kmol h, uniquac vll. <sub>ethyl-acetate-piotrowski-2021.col11-acid-flow-140.5-415da41</sub>
- **Column 11 alone, paper's stream 13 with 0.01 % acid, bottoms 140, 141 and 141.5 kmol/h. Expected: Convergence; ester as bottoms.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 to 141.5 kmol h, uniquac vll. <sub>ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41</sub>
- **EXTR 8, 2 stages, 27 C, the paper's inlets with acid. Expected: The raffinate of Table A2.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, two equilibrium stages, isothermal 27 c. <sub>ethyl-acetate-piotrowski-2021.extractor-with-acid-062</sub>
- **Product column 11 run alone on the paper's stream 13 with 0.01 mass % acetic acid, bottoms flow specified at 139 kmol/h. Expected: Ethyl acetate as the bottoms, meeting the paper's product purity.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 2.1, property-method justification. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 139 kmol h, uniquac vll. <sub>ethyl-acetate-piotrowski-2021.product-column-acid-below-paper-flow</sub>
- **Heaters 10, 12, 18, 19 and the extractor with the paper's inlets including the acid. Expected: Duties and outlets of Table 1 and Table A2.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, acetic acid 0.01 mass pct. <sub>ethyl-acetate-piotrowski-2021.acid-two-liquids-units-061</sub>
- **Column 11 alone, paper's stream 13 with acid, product purity 99.90 wt%. Expected: Product near 141.5 kmol/h.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, purity 99.9 specified. <sub>ethyl-acetate-piotrowski-2021.col11-acid-purity-spec-062</sub>
- **Product column 11 run alone on the paper's stream 13 with 0.01 mass % acetic acid, bottoms flow specified at 140, 141 and 141.5 kmol/h. Expected: Ethyl acetate as the bottoms, meeting the paper's product purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 2.1, property-method justification. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 to 141.5 kmol h, uniquac vll. <sub>ethyl-acetate-piotrowski-2021.product-column-acid-at-paper-flow</sub>

### sep acid stripping from ester vapour (separation)

- **Column 5 alone, 8 equilibrium stages, reflux 27 on stage 1, vapour 6 on stage 8, the paper's inlets. Expected: Azeotrope overhead within the acid limit.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, paper inlets, eight stages, one liquid. <sub>ethyl-acetate-piotrowski-2021.col5-paper-inlets-061</sub>
- **The same four requests. Expected: Convergence across the scan.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, reflux 45000 or 70000 kg h or round 2 vapour 55000. <sub>ethyl-acetate-piotrowski-2021.col5-reflux-scan-415da41</sub>
- **Column 5 alone, paper's vapour 6, reflux 27 at 55,000, 60,000 and 65,000 kg/h, phases VLL. Expected: Acid in the azeotrope below 0.005 wt%.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, paper vapour 6, reflux 55000 to 65000 kg h. <sub>ethyl-acetate-piotrowski-2021.col5-reflux-scan-meets-limit-062</sub>
- **The 0.6.1 request sent again unchanged (phases VLL). Expected: Column converges with two liquids on stage 7.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, round 2 plant inlets, second liquid on stage 7. <sub>ethyl-acetate-piotrowski-2021.col5-round2-inlets-two-liquids-062</sub>
- **Column 5: reactor vapour on the last stage, organic phase of the extractor (60,000 kg/h) on stage 1; Table 1: 8 stages, R/V 0.61. Expected: Azeotrope overhead with acid below 0.005 wt%; acid-rich bottoms to the reactor.** worked, paper's simulation; Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3; Piotrowski & Kubica 2021, p. 3, Section 1.2, purification stage (1); Piotrowski & Kubica 2021, p. 11, Table 1. When: piotrowski 2021 plant s2, no condenser no reboiler, washed ester as reflux. <sub>ethyl-acetate-piotrowski-2021.paper-azeotropic-column-acid-stripping</sub>
- **Column 5 alone at 45,000 and 70,000 kg/h of reflux (paper's vapour), 45,000 and 55,000 kg/h (CHEPTA's round-2 vapour). Expected: Convergence across the scan.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, reflux 45000 or 70000 kg h or round 2 vapour 55000. <sub>ethyl-acetate-piotrowski-2021.col5-reflux-scan-irregular-062</sub>
- **Column 5 alone with CHEPTA's round-2 inlets, phases VL then VLL. Expected: Column converges with two liquids on stage 7.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, round 2 plant inlets, second liquid on stage 7. <sub>ethyl-acetate-piotrowski-2021.col5-round2-inlets-two-liquids-061</sub>

### rxn esterification equilibrium limited (reaction)

- **The 0.6.1 requests sent again unchanged. Expected: The heater duty of Table 1 (535.6 kW).** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: feeds at 15 c, pure acetic acid below triple point. <sub>ethyl-acetate-piotrowski-2021.acid-feed-15c-062</sub>
- **Reactor-evaporator at 85-90 C and atmospheric pressure, 300 m3 (Table 1), vapour to column 5, column 5 bottoms back to the reactor. Expected: High overall acid conversion with the acid recycled until used up.** worked, paper's simulation; Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph; Piotrowski & Kubica 2021, p. 11, Table 1. When: piotrowski 2021 plant s2, boiling reacting liquid, atmospheric pressure. <sub>ethyl-acetate-piotrowski-2021.paper-reactor-evaporator</sub>
- **Conversion of acetic acid per pass 0.7703 = 1 - 4.74/20.64 (Table A2 streams 5 and 6), saturated-vapour outlet, the paper's inlet stream 5. Expected: The paper's reactor outlet and duty, without predicting the reaction.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph; Piotrowski & Kubica 2021, p. 11, Table 1. When: conversion imposed 0.7703, all vapour outlet, paper inlet stream 5. <sub>ethyl-acetate-piotrowski-2021.reactor-conversion-imposed-061</sub>
- **Closed settled plant with the conversion per pass 0.80 and 0.74 (paper's streams: 0.7703). Expected: Product unchanged if the reactor is not the limit.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: closed plant settled, conversion per pass 0.74 to 0.80. <sub>ethyl-acetate-piotrowski-2021.reactor-conversion-per-pass-sensitivity-062</sub>
- **Feeds 1 and 2 at 15 C (Table A2), also 17 C after mixing. Expected: The heater duty of Table 1 (535.6 kW).** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: feeds at 15 c, pure acetic acid below triple point. <sub>ethyl-acetate-piotrowski-2021.acid-feed-15c-061</sub>

### plant recycles makeup purge (plant)

- **Column 15 alone, distillate 400 and 410 kmol/h (+1.4 to +3.9 %). Expected: Ethanol in the bottoms near zero.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, distillate 400 to 410 kmol h. <sub>ethyl-acetate-piotrowski-2021.col15-distillate-400-410-062</sub>
- **Settled start, F1 bracketed 6,503.5-6,507.5 kg/h. Expected: Ethanol limit met.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, design spec ethanol feed for 0.04 pct ethanol. <sub>ethyl-acetate-piotrowski-2021.design-spec-ethanol-feed-415da41</sub>
- **Column 15: 18 stages, feed 9, R/D 2 (Table 1); distillate 21 back to the reactor; bottoms split into wash-water recycle and wastewater. Expected: Wastewater bottoms below 0.01 wt% organics; ethanol and ester recovered.** worked, paper's simulation; Piotrowski & Kubica 2021, p. 10, Section 3.5; Piotrowski & Kubica 2021, p. 11, Table 1. When: piotrowski 2021 plant s2, wastewater distillate to reactor. <sub>ethyl-acetate-piotrowski-2021.paper-wastewater-column</sub>
- **Wastewater 25 = 20,000 kg/h, recycle 23 = 95,797 kg/h, fresh water 17 = 17,478 kg/h (Table A2). Expected: A closed wash-water loop with one wastewater exit.** worked, paper's simulation; Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: piotrowski 2021 plant s2, wastewater 20000 kg h, fresh water make up. <sub>ethyl-acetate-piotrowski-2021.paper-water-loop-round-flows</sub>
- **Plant once through (round 1), splitters by fractions. Expected: Streams near Table A2.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: two sections coupled by script, once through, acid dropped downstream of column 5. <sub>ethyl-acetate-piotrowski-2021.plant-once-through-061</sub>
- **Same specifications, saved starting values (init-closed-plant-chepta-0.6.2-settled.json). Expected: A settled closed plant.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, saved start tolerance 1e 5. <sub>ethyl-acetate-piotrowski-2021.plant-purity-specs-settled-062</sub>
- **Settled plant; also the cold start at the default tolerance. Expected: Same answer.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, saved start tolerance 1e 5. <sub>ethyl-acetate-piotrowski-2021.plant-settled-415da41</sub>
- **Variant W: splitter 16 fixes 25 = 20,000 kg/h, tolerance 5e-4. Expected: Closed plant with the paper's wastewater.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, wastewater 25 fixed 20000 kg h, feeds fixed, tear tolerance 5e 4. <sub>ethyl-acetate-piotrowski-2021.plant-variant-w-both-round-flows-062</sub>
- **Column 15 alone, paper's feed 28, R/D 2, distillate 394.6 kmol/h. Expected: Bottoms below 0.01 wt% organics.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, distillate 394.6 kmol h. <sub>ethyl-acetate-piotrowski-2021.col15-paper-distillate-062</sub>
- **Column 15 alone with the paper's feed and acid. Expected: A converged column at the purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, bottoms water 99.99 specified. <sub>ethyl-acetate-piotrowski-2021.col15-purity-spec-062</sub>
- **Settled start, with and without F1 as a second variable. Expected: 99.90 % ester.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, design spec varies column 11 distillate. <sub>ethyl-acetate-piotrowski-2021.design-spec-column-distillate-415da41</sub>
- **Settled start, Brent. Expected: 99.90 % ester.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, design spec ethanol feed for 99.9 pct ester. <sub>ethyl-acetate-piotrowski-2021.design-spec-ester-purity-415da41</sub>
- **Settled closed plant, ethanol feed 6,506 kg/h; also with the extractor at 20 C (6,506 and 6,508 kg/h). Expected: Product purity near 99.9 %.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, ethanol feed 6506 to 6508 kg h, extractor 27 or 20 c. <sub>ethyl-acetate-piotrowski-2021.ethanol-feed-trimmed-062</sub>
- **Settled closed plant, ethanol feed 6,503 and 6,500 kg/h. Expected: Purer product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant settled, ethanol feed 6500 to 6503 kg h. <sub>ethyl-acetate-piotrowski-2021.ethanol-feed-trimmed-further-062</sub>
- **Broyden, direct substitution, Wegstein, warm starts from 0.6.1's streams; column 5 with one liquid or max_iterations 100. Expected: A closed plant near Table A2.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. <sub>ethyl-acetate-piotrowski-2021.plant-paper-column-specs-062</sub>
- **The same closed variants. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. <sub>ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41</sub>
- **Closed plant, column 15 on its bottoms purity, column 11 bottoms 141.5 kmol/h. Expected: Closed plant.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: closed plant, column 15 bottoms purity, column 11 bottoms 141.5 kmol h. <sub>ethyl-acetate-piotrowski-2021.plant-product-flow-above-ester-formed-062</sub>
- **Closed plant, column 15 on 99.99 % water in its bottoms, column 11 on R/D 3 and distillate 240 kmol/h, recycle 23 fixed, tolerance 3e-4. Expected: A steady-state plant.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, tear tolerance 3e 4. <sub>ethyl-acetate-piotrowski-2021.plant-purity-specs-loose-tolerance-062</sub>
- **Section A again with CHEPTA's reflux 27 and wastewater distillate 21. Expected: The loop closes by successive passes.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: two sections coupled by script, round 2 own recycles. <sub>ethyl-acetate-piotrowski-2021.plant-round2-061</sub>

### rxn co2 hydrogenation methanol (reaction)

- **Six parallel modules of 33,000 tubes (12.5 m, 3.75 cm), Cu/ZnO/Al2O3, 70 bar, boiling water on the shell. Expected: Single-pass CO2 conversion near equilibrium (28.5 % against 30.4 %).** worked, paper's simulation; Campos et al. 2022, p. 4, Section 2.1; Campos et al. 2022, p. 1, Abstract. When: campos 2022 one step process, 70 bar, boiling water cooled tubes. <sub>methanol-co2-campos-2022.paper-multitubular-reactor-70-bar</sub>
- **Reactor on the paper's inlet, U 300, 150 and 1000, and isothermal. Expected: The paper's outlet 16.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 4, Section 2.1; Campos et al. 2022, p. 1, Abstract. When: unit alone, paper inlet, lhhw model 6p on fugacities, coolant constant 247.5 c, u 150 to 1000 w m2 k. <sub>methanol-co2-campos-2022.reactor-lhhw-u-assumed-062</sub>

### sep co2 dissolved in methanol water (separation)

- **FLASH3 at 30 C, 69.25 bar; valve to 1 bar; FLASH4 at 30 C; FLASH4 gas (less 2 %) mixed with the column's gas distillate and the CO2 feed. Expected: Column feed nearly free of gases (1.285 mol % CO2 in stream 28).** worked, paper's simulation; Campos et al. 2022, pp. 4-5, Section 2.1, one-step process; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, stream 24. When: campos 2022 one step process, flash 30 c 69.25 bar then 1 bar. <sub>methanol-co2-campos-2022.paper-two-flashes-co2-recycle</sub>
- **Every flash on the paper's inlets with PR. Expected: The paper's flash outlets.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 9, Section 2.5; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, stream 24. When: unit alone, paper inlet, peng robinson fitted kij. <sub>methanol-co2-campos-2022.property-method-pr-everywhere-062</sub>
- **FLASH3 and the column with PR + MHV1. Expected: An answer with NRTL in the mixing rule.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 9, Section 2.5. When: unit alone, paper inlet, peng robinson mhv1. <sub>methanol-co2-campos-2022.property-method-pr-mhv1-062</sub>
- **Not run: compare both against measured CO2 solubility in methanol + water near 30 C and 70 bar. Expected: Know which split is physical before the loop is compared on CO2.** untested, Lab's reasoning; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, stream 24; Campos et al. 2022, p. 9, Section 2.5. When: flash 30 c 69.25 bar, co2 in liquid 3.4 vs 18.5 mol pct. <sub>methanol-co2-campos-2022.open-co2-solubility-hp-flash</sub>

### sep methanol water with dissolved gases (separation)

- **Paper's feed without the traces, partial condenser, reflux 2, bottoms 4581 kmol/h, then flash at 53 C. Expected: The paper's 31-MEOH, 30-WATER and 32.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 gases bypassed, partial condenser then flash 53 c, bottoms 4581 kmol h. <sub>methanol-co2-campos-2022.column-gases-bypassed-flash53-062</sub>
- **Column alone, plant-a6's stream 29. Expected: A converged column near 53 C.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, plant a6 column feed low co2, vapour liquid condenser share or vapour flow. <sub>methanol-co2-campos-2022.column-plant-feed-by-share-415da41</sub>
- **Column on the paper's full feed, partial condenser. Expected: A converged column.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, paper feed 29 with ppm gases, one distillate. <sub>methanol-co2-campos-2022.column-ppm-gases-415da41</sub>
- **Column alone on the paper's feed 29, with and without the traces; also reflux 2.1273 (2 over the whole distillate). Expected: The paper's 31-MEOH and 32.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 with ppm gases, vapour liquid condenser 53 c, bottoms 4581 kmol h. <sub>methanol-co2-campos-2022.column-vapour-liquid-condenser-alone-415da41</sub>
- **30 stages, feed above stage 24, reflux ratio 2, condenser 53 C with liquid and vapour distillates, kettle reboiler. Expected: Methanol 99.67 mol %, water 99.99 mol %.** worked, paper's simulation; Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: campos 2022 one step process, partial condenser 53 c liquid and vapour distillate. <sub>methanol-co2-campos-2022.paper-column-vapour-liquid-condenser</sub>
- **Whole plant, Broyden, from the paper's start and from plant-a6's tears; also with the traces through the column. Expected: A closed plant with the paper's condenser configuration.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: closed plant, vapour liquid condenser vapour share 0.008406. <sub>methanol-co2-campos-2022.plant-condenser-by-vapour-share-415da41</sub>
- **Column alone, plant-a6's stream 29. Expected: A converged column.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, plant a6 column feed low co2, vapour liquid condenser 53 c. <sub>methanol-co2-campos-2022.column-plant-feed-at-53c-415da41</sub>
- **30 stages, feed 24, reflux 2, bottoms 4581 kmol/h, PR. Expected: A converged column.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, paper feed 29 with ppm gases, one distillate. <sub>methanol-co2-campos-2022.column-ppm-gases-062</sub>
- **Column alone and in the plant. Expected: A converged column at the purity.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 gases bypassed, bottoms water purity or recovery specified. <sub>methanol-co2-campos-2022.column-purity-or-recovery-spec-062</sub>
- **Column alone, with and without the traces. Expected: Both distillates from one column.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, liquid side draw stage 2, stage 1 at 53 c. <sub>methanol-co2-campos-2022.column-side-draw-for-liquid-distillate-062</sub>
- **Whole plant. Expected: A closed plant.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, column boil up ratio 1.17155. <sub>methanol-co2-campos-2022.plant-boilup-spec-062</sub>
- **Whole plant with the new condenser. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, vapour liquid condenser 53 c. <sub>methanol-co2-campos-2022.plant-condenser-at-53c-415da41</sub>
- **Closed plant with the condenser by its vapour share. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: closed plant, vapour liquid condenser vapour share 0.008406, bottoms water 99.985 specified. <sub>methanol-co2-campos-2022.plant-purity-spec-415da41</sub>
- **Not run: rerun plant-vl on the release that answers M6. Expected: The paper's configuration and specification together.** untested, Lab's reasoning; Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, vapour liquid condenser 53 c after m6. <sub>methanol-co2-campos-2022.open-condenser-temperature-spec</sub>

### plant gas recycle with purge (plant)

- **Synthesis loop section, Broyden. Expected: A converged loop.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: synthesis loop section, he5 min approach 2 k zones 10. <sub>methanol-co2-campos-2022.loop-iteration-limit-062</sub>
- **2 % of the high-pressure flash gas and 2 % of the low-pressure flash gas purged and burned. Expected: Bounded inert inventory; recycle about 2.7 times the fresh gas.** worked, paper's simulation; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: campos 2022 one step process, purge 2 pct both flash gases. <sub>methanol-co2-campos-2022.paper-purge-2-pct</sub>
- **Whole plant as one CHEPTA flowsheet (fired heater and steam cycle left out), Broyden. Expected: The paper's products and recycles.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32; Campos et al. 2022, p. 10, Section 2.5. When: closed plant, five tears 19 35 26 28 39 rec, column bottoms 4581 kmol h, traces bypassed, he5 min approach 2 k zones 10. <sub>methanol-co2-campos-2022.plant-closed-062</sub>
- **plant-a6 on CHEPTA main 415da41. Expected: Same answer.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, five tears 19 35 26 28 39 rec, column bottoms 4581 kmol h, traces bypassed, he5 min approach 2 k zones 10. <sub>methanol-co2-campos-2022.plant-rerun-a6-415da41</sub>
- **Synthesis loop section, Broyden. Expected: A converged loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: synthesis loop section, iterations 50. <sub>methanol-co2-campos-2022.loop-50-iterations-062</sub>
- **Whole plant, tears 19, 36-REC, 26, 39-REC, then also 28. Expected: A closed plant.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, tears on recycles only. <sub>methanol-co2-campos-2022.plant-tears-recycles-only-062</sub>

### plant feed effluent heat recovery (plant)

- **HE5 alone, dTmin 2 K, zones 10. Expected: A 2 K approach.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, zones 10. <sub>methanol-co2-campos-2022.he5-min-approach-10-zones-062</sub>
- **HE5 alone on the paper's streams. Expected: A 2 K approach.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones. <sub>methanol-co2-campos-2022.he5-min-approach-default-zones-415da41</sub>
- **HE7 on the paper's stream 22. Expected: One of the two duties confirmed.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement p. 26, Table S14, HE7; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process). When: unit alone, paper stream 22 to 30 c. <sub>methanol-co2-campos-2022.he7-cooling-duty-062</sub>
- **HE4 heats the reactor feed, HE5 the column feed, HE6 the low-pressure flash feed; HE7 with cooling water to 30 C. Expected: Less utility use.** worked, paper's simulation; Campos et al. 2022, pp. 4-5, Section 2.1, one-step process; Campos et al. 2022, supplement p. 26, Table S14, HE7; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process). When: campos 2022 one step process, he4 he5 he6 then cooling water. <sub>methanol-co2-campos-2022.paper-feed-effluent-exchangers</sub>
- **HE5 alone on the paper's streams 20 and 28, and in the loop. Expected: The largest duty at a 2 K approach.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones. <sub>methanol-co2-campos-2022.he5-min-approach-default-zones-062</sub>
- **The synthesis loop section with Broyden, direct substitution and Wegstein. Expected: A closed loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: synthesis loop section, exchangers by paper outlet temperatures. <sub>methanol-co2-campos-2022.he5-paper-outlets-in-loop-062</sub>
- **HE5 alone and in the closed plant. Expected: A 2 K approach.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones, plant a6 streams. <sub>methanol-co2-campos-2022.he5-plant-streams-default-zones-415da41</sub>
- **Synthesis loop section. Expected: A closed loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: synthesis loop section, he6 by hot outlet. <sub>methanol-co2-campos-2022.he6-by-hot-outlet-062</sub>
- **A reading of Tables S9 and S14 with run u-he7; not checked with the authors. Expected: Use the stream table as the comparison basis (the maintainer, 2026-11-14) and treat HE7's printed outlet enthalpy with care.** lead, Lab's reasoning; Campos et al. 2022, supplement p. 26, Table S14, HE7; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process). When: campos 2022 one step process, he7 24.2 vs 19.75 mw. <sub>methanol-co2-campos-2022.open-he7-stream-enthalpy</sub>

## By operation and simulation symptom

### absorber column: no convergence

- **The same four requests. Expected: Convergence across the scan.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, reflux 45000 or 70000 kg h or round 2 vapour 55000. <sub>ethyl-acetate-piotrowski-2021.col5-reflux-scan-415da41</sub>
- **Column 5 alone at 45,000 and 70,000 kg/h of reflux (paper's vapour), 45,000 and 55,000 kg/h (CHEPTA's round-2 vapour). Expected: Convergence across the scan.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, reflux 45000 or 70000 kg h or round 2 vapour 55000. <sub>ethyl-acetate-piotrowski-2021.col5-reflux-scan-irregular-062</sub>

### absorber column: purity short

- **Unit misses purity in the plant: fix it alone first with a design specification, then connect**
  - When: A separation unit misses its purity once connected in the plant.
  - Do: Simulate and size each separation unit alone first. Reach its purity or recovery with a design specification that adjusts one variable, or a sensitivity scan, before connecting the whole process.
  - Why: Fixing units alone separates unit problems from loop problems.
  - Check: In CHEPTA, pair each target with one free variable and bounds, and keep each run.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': process modelling and simulations. <sub>palomar-2024-il-process-simulation.units-alone-then-design-spec</sub>

### absorber column: wrong phase

- **The 0.6.1 request sent again unchanged (phases VLL). Expected: Column converges with two liquids on stage 7.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, round 2 plant inlets, second liquid on stage 7. <sub>ethyl-acetate-piotrowski-2021.col5-round2-inlets-two-liquids-062</sub>
- **Column 5 alone with CHEPTA's round-2 inlets, phases VL then VLL. Expected: Column converges with two liquids on stage 7.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, round 2 plant inlets, second liquid on stage 7. <sub>ethyl-acetate-piotrowski-2021.col5-round2-inlets-two-liquids-061</sub>

### azeotropic distillation: no convergence

- **Guess the heteroazeotropic recycle from a mass balance, not from defaults**
  - When: The recycle composition and flow of a two-column process with a decanter are unknown.
  - Do: Solve an overall mass balance first: pure bottom products, a top vapour at the lowest-boiling heteroazeotrope, and a decanter splitting it into its two liquids, with the solvent-lean liquid recycled. Use the result as the tear guess (the recycle stream's starting value).
  - Why: The heteroazeotrope and its liquid split fix the overhead and the recycle to a first approximation.
  - Check: In CHEPTA, give this balance as the tear stream's starting value and compare the first iteration with it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, p. 7 (steps 2-3, Fig. 3b-c). <sub>kruber-skiborowski-2022-heteroazeotropic-init.mass-balance-estimate-of-recycle</sub>
- **Start the heteroazeotropic column from a profile joining azeotrope, saddle and bottom product**
  - When: A column crossing a two-liquid region fails from a flat or constant starting profile.
  - Do: Initialise with a piecewise-linear composition profile joining the lowest-boiling heteroazeotrope, the saddle of its distillation region and the bottom product. Check the phases on each stage before solving the full column.
  - Why: At total reflux the profile follows the region's singular points, so this start lies close to the solution.
  - Check: Lab has not checked whether CHEPTA accepts a stage-by-stage starting profile; if not, start from the closest converged column.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, p. 7 (step 5, Fig. 3e); Section 3.1.1, pp. 10-11 (Fig. 5). <sub>kruber-skiborowski-2022-heteroazeotropic-init.piecewise-initial-profile</sub>
- **Stages switching between one and two liquids break a gradient solver: hide the split inside the property call**
  - When: A gradient-based solver meets discontinuities as stages change between one and two liquids.
  - Do: Treat each three-phase stage as a quasi vapour-liquid stage on the overall liquid, and do the two-liquid split only inside the property calculation.
  - Why: The column equations then see a smooth function, while the liquid split is still computed.
  - Check: This is a solver design choice. In CHEPTA, note which stages switch between one and two liquids when a run fails, and report it with the failure.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.1, pp. 4-5. <sub>kruber-skiborowski-2022-heteroazeotropic-init.quasi-vle-for-three-phase-stages</sub>
- **Scanning feed composition widely: re-initialise for each interval**
  - When: A feed-composition scan fails or gives outliers away from the first feed.
  - Do: Re-initialise the column for each interval of feed composition instead of reusing one start.
  - Why: The required stage numbers vary a lot, so a start built for one feed lies far from the solution for another.
  - Check: In CHEPTA, start each scan interval from a run converged near that feed.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.2.2, p. 16. <sub>kruber-skiborowski-2022-heteroazeotropic-init.reinitialise-for-feed-changes</sub>
- **Even one heteroazeotropic column is hard: fix the organic reflux before adding the second column**
  - When: A heteroazeotropic column does not converge.
  - Do: Fix the organic reflux and recycle estimates before adding the second column. Do not read a failure as a property error alone.
  - Why: Such a column can have several steady states and its products are very sensitive to the organic reflux. Luyben's careful manual start of ethanol dehydration still ended unconverged (cited by Kruber & Skiborowski 2022).
  - Check: In CHEPTA, scan the organic reflux around the published value and record where the column converges.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 2 (ref. 11). <sub>kruber-skiborowski-2022-heteroazeotropic-init.single-column-already-hard</sub>
- **Heteroazeotropic recycle hard to close: allow a small purge**
  - When: The recycle through the decanter is not robust.
  - Do: Allow a small optional purge. In the 1,4-dioxane and benzene case of Kruber & Skiborowski 2022 the optimisation relied on 0.8% of the feed.
  - Why: A purge removes accumulating material and loosens the recycle. Kruber & Skiborowski 2022 link the need for it to a poorer initial profile estimate.
  - Check: In CHEPTA, record the purge flow and the product lost with it, and try to remove the purge once the loop converges.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.3, p. 16. <sub>kruber-skiborowski-2022-heteroazeotropic-init.small-purge-aids-robustness</sub>
- **Before building a heteroazeotropic column, map every azeotrope**
  - When: You set up a heteroazeotropic column (one with a decanter on top where two liquids form), and it starts far from a feasible profile.
  - Do: Compute and classify every azeotrope as a node or a saddle (points where residue curves start, end or turn). These singular points show which profiles a column can reach at total reflux and guide the starting profile.
  - Why: The mixture's topology bounds what column profiles are possible.
  - Check: In CHEPTA, check each azeotrope's temperature and composition against Kruber & Skiborowski 2022 or measured data before the first column run.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, pp. 5-7 (step 1, Figs. 2-3). <sub>kruber-skiborowski-2022-heteroazeotropic-init.topology-first</sub>

### azeotropic distillation: purity short

- **Converged design far off the trend may be a poor local optimum: nudge the feed stage or stage count**
  - When: One optimised design sits well off the trend of its neighbours.
  - Do: Change the initial feed stage or the total number of stages slightly and re-solve.
  - Why: The final fixing of stage locations can land in a worse local optimum.
  - Check: Compare the re-solved design with its neighbours.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.2, p. 12; Section 3.3.1, p. 17. <sub>kruber-skiborowski-2022-heteroazeotropic-init.outliers-from-integer-fixing</sub>

### azeotropic distillation: wrong phase

- **Column with water and an organic phase gives odd profiles: allow two liquids on every stage**
  - When: A column whose liquid can split into two phases (for example water with an organic entrainer, in heteroazeotropic distillation) is computed with vapour-liquid equilibrium only, or its stage profiles look wrong.
  - Do: Test phase stability (whether a liquid would rather split into two) on every stage, and allow vapour-liquid-liquid equilibrium there. Kruber & Skiborowski 2022 cite earlier work showing that leaving out the second liquid can give substantial errors.
  - Why: On a stage that really holds two liquids, a one-liquid calculation gets the wrong equilibrium, and so the wrong compositions, flows and balance.
  - Check: In CHEPTA, set phases: "VLL" on the column and the decanter, then see which stages report two liquids and compare the decanter's two liquid compositions with those of Kruber & Skiborowski 2022.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 2 (refs. 17-18); Section 2.1, p. 4. Lab reread Section 1, p. 2 on 2026-11-20. <sub>kruber-skiborowski-2022-heteroazeotropic-init.phase-stability-every-stage</sub>

### distillation: no convergence

- **Column 11 alone, paper's stream 13 with 0.01 % acid, bottoms 140, 141 and 141.5 kmol/h. Expected: Convergence; ester as bottoms.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 to 141.5 kmol h, uniquac vll. <sub>ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41</sub>
- **Product column 11 run alone on the paper's stream 13 with 0.01 mass % acetic acid, bottoms flow specified at 139 kmol/h. Expected: Ethyl acetate as the bottoms, meeting the paper's product purity.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 2.1, property-method justification. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 139 kmol h, uniquac vll. <sub>ethyl-acetate-piotrowski-2021.product-column-acid-below-paper-flow</sub>
- **Column on the paper's full feed, partial condenser. Expected: A converged column.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, paper feed 29 with ppm gases, one distillate. <sub>methanol-co2-campos-2022.column-ppm-gases-415da41</sub>
- **Settled closed plant, distillate 260, 270, 280 kmol/h. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 260 to 280 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-062</sub>
- **From the design-specification answer. Expected: Purer product.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: closed plant ethanol feed 6506.23, column 11 distillate 270 kmol h. <sub>ethyl-acetate-piotrowski-2021.ds-start-distillate-270-415da41</sub>
- **Product column 11 run alone on the paper's stream 13 with 0.01 mass % acetic acid, bottoms flow specified at 140, 141 and 141.5 kmol/h. Expected: Ethyl acetate as the bottoms, meeting the paper's product purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 2.1, property-method justification. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 to 141.5 kmol h, uniquac vll. <sub>ethyl-acetate-piotrowski-2021.product-column-acid-at-paper-flow</sub>
- **Column alone, plant-a6's stream 29. Expected: A converged column.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, plant a6 column feed low co2, vapour liquid condenser 53 c. <sub>methanol-co2-campos-2022.column-plant-feed-at-53c-415da41</sub>
- **30 stages, feed 24, reflux 2, bottoms 4581 kmol/h, PR. Expected: A converged column.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, paper feed 29 with ppm gases, one distillate. <sub>methanol-co2-campos-2022.column-ppm-gases-062</sub>
- **Column alone, with and without the traces. Expected: Both distillates from one column.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, liquid side draw stage 2, stage 1 at 53 c. <sub>methanol-co2-campos-2022.column-side-draw-for-liquid-distillate-062</sub>
- **Whole plant. Expected: A closed plant.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, column boil up ratio 1.17155. <sub>methanol-co2-campos-2022.plant-boilup-spec-062</sub>
- **Whole plant with the new condenser. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, vapour liquid condenser 53 c. <sub>methanol-co2-campos-2022.plant-condenser-at-53c-415da41</sub>
- **Closed plant with the condenser by its vapour share. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: closed plant, vapour liquid condenser vapour share 0.008406, bottoms water 99.985 specified. <sub>methanol-co2-campos-2022.plant-purity-spec-415da41</sub>
- **Equation-oriented solve fails from poor estimates: start it from a short dynamic run**
  - When: An equation-oriented solver (one that solves all equations at once) fails from a poor starting point.
  - Do: Run a short dynamic simulation and use its final values as the initial guess for the steady state.
  - Why: A dynamic run moves all variables towards the steady state.
  - Check: Lab has not checked whether CHEPTA can run dynamically; if not, start from the closest converged steady state.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Introduction, p. 151. <sub>henrique-2020-dwc-simulation.dynamic-run-for-initial-guess</sub>
- **Dividing-wall column does not converge: model it as a pump-around pair of columns**
  - When: Your simulator has no dividing-wall column model (one shell with an internal wall), and the coupled-column version does not converge.
  - Do: Represent the dividing wall with the pump-around arrangement rather than the four-column arrangement.
  - Why: The pump-around form has fewer interconnecting recycles.
  - Check: In CHEPTA, build the pump-around version and compare its products with the four-column one where both converge.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Introduction, p. 150 (Fig. 1). <sub>henrique-2020-dwc-simulation.pump-around-representation</sub>
- **Build up the simple column step by step: flash, fixed column, then optimise**
  - When: A column model solved all at once from a poor start fails.
  - Do: Flash the mixed feed (fresh feed plus recycle) first, then solve the stage model with a fixed structure, and only then minimise duty. Raise the model's complexity one step at a time.
  - Why: Each harder sub-problem starts close to the solution of the easier one before it.
  - Check: In CHEPTA, keep each step's converged result and start the next step from it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, p. 7 (step 4, Fig. 3d). <sub>kruber-skiborowski-2022-heteroazeotropic-init.simple-column-flash-then-solve</sub>
- **Newton iterations diverge: improve the start or damp the step**
  - When: A Newton-type column solver diverges.
  - Do: Improve the starting values, or damp the Newton step (relaxation) so it takes smaller moves.
  - Why: Full Newton steps overshoot far from the solution, and the method fails where several solutions exist.
  - Check: In CHEPTA, look at the solver's residual history: residuals that grow point to a poor start.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Numerical methods, p. 18. <sub>steffen-2024-rd-modelling-review.newton-needs-good-start</sub>
- **Rate-based column model fails: check the mass-transfer data and compare with the equilibrium-stage result**
  - When: A rate-based (non-equilibrium) stage model does not converge.
  - Do: Check the mass-transfer correlations, and compare with the equilibrium-stage result.
  - Why: Rate-based models have more equations with stiffer coupling than equilibrium-stage models.
  - Check: Converge the equilibrium-stage column first and use it as the reference.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Equilibrium and non-equilibrium models, p. 15. <sub>steffen-2024-rd-modelling-review.rate-based-harder</sub>

### distillation: purity short

- **Settled closed plant, distillate 260, 270, 280 kmol/h. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 260 to 280 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41</sub>
- **Settled closed plant, distillate 246 kmol/h. Expected: Less water in the product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 246 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-distillate-raised-settled-062</sub>
- **Settled closed plant, feed stage 5. Expected: Higher purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 feed stage 5. <sub>ethyl-acetate-piotrowski-2021.col11-feed-stage-5-062</sub>
- **Closed plant from the saved start, tolerance 3e-4, 36, 38, 40 stages. Expected: Higher purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant saved start, column 11 36 to 40 stages. <sub>ethyl-acetate-piotrowski-2021.col11-more-stages-062</sub>
- **Column 11 alone on the paper's stream 13 without acid. Expected: 99.90 wt% ester.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5; Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: standalone product column, paper stream 13 feed, no acetic acid, bottoms flow 141.5 kmol h. <sub>ethyl-acetate-piotrowski-2021.col11-no-acid-paper-flow-061</sub>
- **Column 15 alone, paper's feed 28, R/D 2, distillate 394.6 kmol/h. Expected: Bottoms below 0.01 wt% organics.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, distillate 394.6 kmol h. <sub>ethyl-acetate-piotrowski-2021.col15-paper-distillate-062</sub>
- **Column 15 alone with the paper's feed and acid. Expected: A converged column at the purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, bottoms water 99.99 specified. <sub>ethyl-acetate-piotrowski-2021.col15-purity-spec-062</sub>
- **Distillate 250 and 260 kmol/h, with and without the ethanol design specification. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant ethanol feed 6506.23, column 11 distillate 250 to 260 kmol h. <sub>ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41</sub>
- **Column converges but misses its purity: check balances and stage profiles before changing settings**
  - When: A column converges but misses its purity or recovery target.
  - Do: Check each component's balance around the column, and compare the stage temperature, flow and composition profiles with a reference, not only the products.
  - Why: Balances and stage profiles show the section or stage where the separation departs from the target; the end products alone hide it.
  - Check: In CHEPTA, compare the run's stage profiles with the reference case and find the stage where they diverge before changing a setting.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kooijman & Taylor 2006, *The ChemSep Book, second edition* (https://www.chemsep.org/downloads/docs/book2.pdf), Sections 1.2-1.3, pp. 9-20, Figures 1.18-1.21 (balances, profiles, stream table), as transcribed by CHEPTA. Lab has not reread the source for this summary. <sub>kooijman-taylor-2006-chemsep-book.column-misses-target-check-balances-and-profiles</sub>

### distillation: slow

- **Column 11 alone on the paper's stream 13 without acid, product purity 99.90 wt%. Expected: 99.90 wt% ester at a product flow near the paper's.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, no acetic acid, purity 99.9 specified. <sub>ethyl-acetate-piotrowski-2021.col11-no-acid-purity-spec-061</sub>

### distillation: wrong phase

- **Acetic acid in the vapour or lithium bromide brine: choose property methods that can handle them**
  - When: A broth recovery with acetic acid present, or with a lithium bromide brine loop, gives wrong phases or volatilities.
  - Do: With acetic acid, use NRTL with Hayden-O'Connell vapour association (a model of acid pairs in the vapour), as Janković et al. 2023 did. With lithium bromide brine, regress an electrolyte NRTL model (with Redlich-Kwong vapour) on binary data, since no ready parameter set fits.
  - Why: Acetic acid forms dimers in the vapour, which changes its volatility. The salt needs an electrolyte model.
  - Check: Check that CHEPTA's property method covers vapour association and electrolytes for your components before relying on it. The fitted parameters are in the Supporting Information of Janković et al. 2023, not read by Lab.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Vacuum distillation, p. 717; Pass-through distillation, p. 718. <sub>jankovic-2023-ipa-acetone-recovery.acid-and-brine-property-methods</sub>
- **Predictive property method (UNIFAC- or COSMO-type): check it against data first**
  - When: A design relies on phase behaviour or properties from a predictive model, for example for ionic liquids or other unusual molecules.
  - Do: Check the method against measured data over a wide range of the property before a design relies on it.
  - Why: Group-contribution and COSMO methods can err for unusual molecules.
  - Check: Lab relies on CHEPTA's property provenance; this check matters where a method lacks data for the case's components.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': definition of thermodynamic model and property validation. <sub>palomar-2024-il-process-simulation.validate-predictive-methods</sub>
- **Polar mixtures such as glycerol, methanol and water: NRTL or UNIQUAC, with UNIFAC for missing pairs**
  - When: A mixture contains polar components and some binary parameters are missing.
  - Do: Use an activity-coefficient model, NRTL or UNIQUAC, and fill the missing binary pairs with UNIFAC (group-contribution) estimates, as Pasha et al. 2021 describe.
  - Why: Activity models describe non-ideal liquids; UNIFAC fills the gaps.
  - Check: Estimated pairs are guesses until checked against data: find out which pairs CHEPTA has from data and which are predicted.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design and simulation'. <sub>pasha-2021-biodiesel-process-design.nrtl-uniquac-polar</sub>

### extraction: feed refused

- **The 0.6.1 request sent again unchanged. Expected: Extractor accepts its feed.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: section b, mix 7 adiabatic. <sub>ethyl-acetate-piotrowski-2021.mixer-before-extractor-adiabatic-062</sub>
- **EXTR 8 at 70 C with the paper's feed, and with a liquid feed. Expected: Two liquid outlets.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: unit alone, paper temperature 70 c. <sub>ethyl-acetate-piotrowski-2021.extractor-paper-70c-061</sub>
- **Section B with MIX 7 adiabatic. Expected: Extractor accepts its feed.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: section b, mix 7 adiabatic. <sub>ethyl-acetate-piotrowski-2021.mixer-before-extractor-adiabatic-061</sub>

### extraction: no convergence

- **Settled closed plant, 3 and 4 extractor stages. Expected: Drier raffinate.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: closed plant settled, extractor 3 or 4 stages. <sub>ethyl-acetate-piotrowski-2021.extractor-more-stages-062</sub>

### extraction: purity short

- **Settled closed plant, extractor at 20 C (Lab's 27 C). Expected: Drier raffinate.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, extractor 20 c. <sub>ethyl-acetate-piotrowski-2021.extractor-20c-062</sub>
- **Settled closed plant, recycle 23 = 121,000 kg/h (W/A 1.13) and 144,000 kg/h (1.4); also with feed stage 5. Expected: Drier raffinate, purer product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, recycle 23 raised wa 1.13 to 1.4. <sub>ethyl-acetate-piotrowski-2021.wash-water-raised-062</sub>
- **Simulated extraction needs fewer columns than reality: do not assume infinite selectivity**
  - When: An extraction model assumes the extractant takes no water, and the downstream columns come out smaller than expected.
  - Do: Use measured distribution coefficients (how a component divides between the two liquids). Real selectivities (about 300 in Grisales Díaz & Olivar Tost 2017) carry water into the extract, which then needs extra distillation.
  - Why: At finite selectivity some water is always co-extracted.
  - Check: Check the water content of the simulated extract against measured partition data.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Grisales Díaz & Olivar Tost 2017, *Techno-economic analysis of extraction-based separation systems for…* (https://doi.org/10.1186/s40643-017-0142-z), Methods: 'Extractant selection'. <sub>grisales-2017-abe-extraction.finite-selectivity</sub>

### extraction: wrong phase

- **Salt in the liquid phases: use an electrolyte activity model**
  - When: Liquid phases contain dissolved salt and the liquid-liquid split comes out wrong.
  - Do: Correlate the liquid-liquid equilibrium with an electrolyte activity model that has ion-pair parameters, as Fu et al. 2021 did with e-NRTL (electrolyte NRTL).
  - Why: Ions change the activities in ways a molecular model misses.
  - Check: Whether CHEPTA 0.6.2 has an electrolyte model was not checked: check before planning a case with salts.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Fu et al. 2021, *Assessment of extraction options for a next-generation…* (https://doi.org/10.1002/elsc.202000090), Section 'Modeling of the liquid-liquid equilibria'; Concluding remarks. <sub>fu-2021-isobutanol-recovery.electrolyte-model</sub>

### extractive distillation: purity short

- **Regressed and built-in parameters can change the design: volatility off by a factor 1.84, cost by about 45%**
  - When: Simulated purity or cost is far from what was expected.
  - Do: Use parameters regressed from measured data where the built-in ones disagree with the data.
  - Why: Relative volatility is sensitive to the interaction parameters.
  - Check: Compare the key pair's relative volatility from both parameter sets.
  - Result: For benzene and cyclohexane with NMP (a polar extractive solvent), relative volatility differed by a factor of 1.84 and annual cost by about 45%.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2017, *Phase Behavior and Thermodynamic Model Parameters in…* (https://doi.org/10.1038/s41598-017-09088-2), Conclusion. <sub>li-2017-ed-thermo-parameters.parameters-change-economics</sub>

### extractive distillation: wrong phase

- **Simulation shows an azeotrope the data do not: check the built-in binary parameters**
  - When: A simulated azeotrope or phase behaviour does not appear in measured data.
  - Do: Compare the predicted vapour-liquid equilibrium with measured data for the key binaries before designing. Li et al. 2017 found built-in NRTL values predicting a toluene and DMF (dimethylformamide) azeotrope that experiments do not show.
  - Why: Stored interaction parameters may be fitted outside the range or to poor data.
  - Check: Lab relies on CHEPTA's parameter provenance and looks into data only on such a concrete disagreement (AGENTS.md): record the disagreement when you find one.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2017, *Phase Behavior and Thermodynamic Model Parameters in…* (https://doi.org/10.1038/s41598-017-09088-2), Introduction (Fig. 1). <sub>li-2017-ed-thermo-parameters.check-built-in-parameters</sub>

### flash: feed refused

- **FLASH3 and the column with PR + MHV1. Expected: An answer with NRTL in the mixing rule.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 9, Section 2.5. When: unit alone, paper inlet, peng robinson mhv1. <sub>methanol-co2-campos-2022.property-method-pr-mhv1-062</sub>

### flash: no convergence

- **Some flowsheet cases fail but all converge with another flash routine: suspect the flash, not the recycle solver**
  - When: In a parametric study some cases of a flowsheet fail, and swapping in another flash routine makes them all converge.
  - Do: Test the flash on the failing streams alone before changing the recycle solver.
  - Why: A phase-split calculation that jumps between iterations breaks the outer recycle loop.
  - Check: In CHEPTA, rerun each failing unit on its captured inlet with the same phases setting; if it fails alone, report it as a flash case. Andreasen 2022 says this indicates, not proves, the cause.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Andreasen 2022, *Evaluation of an Open-source Chemical Process Simulator…* (https://doi.org/10.3311/PPch.19678), Results, p. 508; Discussion, p. 509. <sub>andreasen-2022-dwsim-evaluation.flash-instability-not-solver</sub>

### heat exchange: feed refused

- **The 0.6.1 requests sent again unchanged. Expected: The heater duty of Table 1 (535.6 kW).** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: feeds at 15 c, pure acetic acid below triple point. <sub>ethyl-acetate-piotrowski-2021.acid-feed-15c-062</sub>
- **The 0.6.1 requests sent again unchanged. Expected: Duties and outlets of Table 1 and Table A2.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, acetic acid 0.01 mass pct. <sub>ethyl-acetate-piotrowski-2021.acid-two-liquids-units-062</sub>
- **HE5 alone on the paper's streams. Expected: A 2 K approach.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones. <sub>methanol-co2-campos-2022.he5-min-approach-default-zones-415da41</sub>
- **Feeds 1 and 2 at 15 C (Table A2), also 17 C after mixing. Expected: The heater duty of Table 1 (535.6 kW).** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: feeds at 15 c, pure acetic acid below triple point. <sub>ethyl-acetate-piotrowski-2021.acid-feed-15c-061</sub>
- **Heaters 10, 12, 18, 19 and the extractor with the paper's inlets including the acid. Expected: Duties and outlets of Table 1 and Table A2.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, acetic acid 0.01 mass pct. <sub>ethyl-acetate-piotrowski-2021.acid-two-liquids-units-061</sub>
- **HE5 alone on the paper's streams 20 and 28, and in the loop. Expected: The largest duty at a 2 K approach.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones. <sub>methanol-co2-campos-2022.he5-min-approach-default-zones-062</sub>
- **HE5 alone and in the closed plant. Expected: A 2 K approach.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones, plant a6 streams. <sub>methanol-co2-campos-2022.he5-plant-streams-default-zones-415da41</sub>

### heat exchange: section fails

- **The synthesis loop section with Broyden, direct substitution and Wegstein. Expected: A closed loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: synthesis loop section, exchangers by paper outlet temperatures. <sub>methanol-co2-campos-2022.he5-paper-outlets-in-loop-062</sub>
- **Synthesis loop section. Expected: A closed loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: synthesis loop section, he6 by hot outlet. <sub>methanol-co2-campos-2022.he6-by-hot-outlet-062</sub>

### reactive distillation: no convergence

- **Reactive column does not converge from defaults: start from straight-line temperatures and constant flows**
  - When: The reactive column solver fails from its default estimates.
  - Do: Start from a straight-line temperature profile between the bubble point of the mixed feed at the condenser and its dew point at the reboiler, with constant molar flows and a reaction extent peaking at the feed stage.
  - Why: Physically shaped profiles start the solver near a solution.
  - Check: Lab has not checked whether CHEPTA accepts such a starting profile; if not, start from a converged simpler case.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Initial estimates, p. 21. <sub>steffen-2024-rd-modelling-review.initial-profiles</sub>
- **Full reactive model fails: converge a simpler model first and start from it**
  - When: The full reactive column model does not converge.
  - Do: Converge a simpler model first, the column without reaction or with ideal K-values (ideal vapour-liquid ratios), then use its result to start the full model.
  - Why: A simpler model gives profiles close to those of the full one.
  - Check: In CHEPTA, keep the simpler run and start the full run from it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Initial estimates, p. 21. <sub>steffen-2024-rd-modelling-review.simpler-model-first</sub>

### reactive distillation: purity short

- **Reactive glycol column converged but misses the target: it may be on the wrong steady state**
  - When: A converged reactive column for ethylene glycol misses its target.
  - Do: Look for other steady states before changing settings: restart from different estimates or scan a setting.
  - Why: Several steady states exist for the same inputs, and one of them accumulates ethylene oxide at the top (earlier modelling studies cited by Othman 2024).
  - Check: In CHEPTA, check the oxide at the top stage: a high value points to the wrong branch.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Introduction, p. 2 (citing earlier modelling studies). <sub>othman-2024-meg-reactive-distillation.rd-multiple-steady-states-oxide-overhead</sub>
- **Reactive column converged but misses its target: look for other steady states**
  - When: A converged reactive column misses its target.
  - Do: Scan a parameter or restart from different initial estimates, and find the steady states before accepting one.
  - Why: Reactive columns often have several solutions for the same inputs (output multiplicity).
  - Check: In CHEPTA, record each branch found and which one meets the target.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Initial estimates, p. 22. <sub>steffen-2024-rd-modelling-review.multiple-steady-states</sub>

### reactive distillation: slow

- **Homotopy continuation is robust but slow: keep it for cases with no good start**
  - When: A robust solving method is too slow for scans.
  - Do: Use Newton or Broyden from good estimates as the default; keep homotopy continuation (a chain of easier problems ending in the real one) for cases where no good start can be found.
  - Why: Continuation solves the modified system many times, so it costs much more computation.
  - Check: Time both methods on one case before choosing one for a scan.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Numerical methods, p. 18; Initial estimates, pp. 22-23. <sub>steffen-2024-rd-modelling-review.homotopy-robust-but-costly</sub>

### reactive distillation: wrong phase

- **Butanol, acetic acid, butyl acetate and water: use NRTL and allow two liquids**
  - When: You simulate the butyl acetate system, whose column overhead splits into a water phase and an organic phase in a decanter.
  - Do: Use an activity model such as NRTL (non-random two-liquid model) with a vapour-liquid-liquid calculation, as Al-Rabiah et al. 2022 did. Lab's reading: a vapour-liquid-only calculation cannot reproduce the decanter split that the reactive column relies on.
  - Why: The mixture is strongly non-ideal. Wherever water and the organic phase meet, a three-phase flash is needed.
  - Check: In CHEPTA, set phases: "VLL" on the decanter and the column and check that two liquids form at the decanter. Al-Rabiah et al. 2022 do not print their NRTL parameters (Aspen databank), and CHEPTA 0.6.2 has some of these pairs only predicted, so compare the decanter compositions before trusting them.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, p. 2; Section 6.2, p. 15 (decanter). <sub>al-rabiah-2022.nrtl-vlle-for-ester-system</sub>
- **Glycol and water: use a property method that handles association, and check for two liquids on the stages**
  - When: Glycols and water associate (form hydrogen bonds), which simple models describe poorly.
  - Do: Use an association-capable property method, as Othman 2024 did with the cubic-plus-association (CPA) equation of state, and check phase stability on the stages.
  - Why: An association term represents the hydrogen bonding.
  - Check: CHEPTA's own property methods and their applicability govern Lab runs: check that the method chosen covers glycol and water at the column's conditions.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Model, p. 3. <sub>othman-2024-meg-reactive-distillation.cpa-for-glycol-water</sub>

### recycle: no convergence

- **Settled closed plant, ethanol feed 6,503 and 6,500 kg/h. Expected: Purer product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant settled, ethanol feed 6500 to 6503 kg h. <sub>ethyl-acetate-piotrowski-2021.ethanol-feed-trimmed-further-062</sub>
- **Broyden, direct substitution, Wegstein, warm starts from 0.6.1's streams; column 5 with one liquid or max_iterations 100. Expected: A closed plant near Table A2.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. <sub>ethyl-acetate-piotrowski-2021.plant-paper-column-specs-062</sub>
- **The same closed variants. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. <sub>ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41</sub>
- **Closed plant, column 15 on its bottoms purity, column 11 bottoms 141.5 kmol/h. Expected: Closed plant.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: closed plant, column 15 bottoms purity, column 11 bottoms 141.5 kmol h. <sub>ethyl-acetate-piotrowski-2021.plant-product-flow-above-ester-formed-062</sub>
- **Recycle of unreacted feed grows without bound: the reactor is too small, the solver is not at fault**
  - When: In a reactor-separator-recycle loop with fixed reactor hold-up, the recycle flow keeps growing (the snowball effect).
  - Do: Check the reactor size against the feed rate before changing solver settings.
  - Why: With fixed reactor hold-up only more recycle can raise conversion, so the loop has no finite steady state.
  - Check: In CHEPTA, reduce the feed or enlarge the reactor and see whether the loop converges. Larsson & Skogestad 2000 discuss this as a control and design problem; reading it as a simulation symptom is Lab's.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 6, p. 230. <sub>larsson-skogestad-2000-plantwide.snowball-means-reactor-too-small</sub>
- **Solvent loop does not close: choose the tear on purpose and add make-up streams**
  - When: A recycled solvent loop does not converge.
  - Do: Choose the tear stream (the recycle stream that is guessed and recomputed) deliberately, and add make-up streams for every component lost from the loop, such as solvent losses, calculated to close the balance.
  - Why: Losses drain the loop unless they are made up.
  - Check: In CHEPTA, check the solvent balance: make-up equals the losses in all outlets.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': process modelling and simulations. <sub>palomar-2024-il-process-simulation.tear-and-make-up</sub>

### recycle: purity short

- **Settled closed plant, ethanol feed 6,506 kg/h; also with the extractor at 20 C (6,506 and 6,508 kg/h). Expected: Product purity near 99.9 %.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, ethanol feed 6506 to 6508 kg h, extractor 27 or 20 c. <sub>ethyl-acetate-piotrowski-2021.ethanol-feed-trimmed-062</sub>

### recycle: recycle drift

- **Same specifications, saved starting values (init-closed-plant-chepta-0.6.2-settled.json). Expected: A settled closed plant.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, saved start tolerance 1e 5. <sub>ethyl-acetate-piotrowski-2021.plant-purity-specs-settled-062</sub>
- **Settled plant; also the cold start at the default tolerance. Expected: Same answer.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, saved start tolerance 1e 5. <sub>ethyl-acetate-piotrowski-2021.plant-settled-415da41</sub>
- **Closed plant, column 15 on 99.99 % water in its bottoms, column 11 on R/D 3 and distillate 240 kmol/h, recycle 23 fixed, tolerance 3e-4. Expected: A steady-state plant.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, tear tolerance 3e 4. <sub>ethyl-acetate-piotrowski-2021.plant-purity-specs-loose-tolerance-062</sub>
- **Recycle loop converged on total flow: check each component as well**
  - When: A recycle loop reports convergence, but compositions still drift or the plant balance does not close for one component.
  - Do: Check the closure of each tear stream (the recycle stream that is guessed and recomputed) component by component, not only its total flow. Andreasen 2022 accepted recycle balance errors below 1 kg/h.
  - Why: A tolerance on total flow can be met while one component is too high and another too low.
  - Check: In CHEPTA, compare each tear's component flows between two tolerances, and check the plant's component balance (fresh feed plus production equals products) for every component.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Andreasen 2022, *Evaluation of an Open-source Chemical Process Simulator…* (https://doi.org/10.3311/PPch.19678), Section 2, p. 506. <sub>andreasen-2022-dwsim-evaluation.recycle-tolerance-per-component</sub>

### recycle: section fails

- **Section A again with CHEPTA's reflux 27 and wastewater distillate 21. Expected: The loop closes by successive passes.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: two sections coupled by script, round 2 own recycles. <sub>ethyl-acetate-piotrowski-2021.plant-round2-061</sub>
- **Whole plant, tears 19, 36-REC, 26, 39-REC, then also 28. Expected: A closed plant.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, tears on recycles only. <sub>methanol-co2-campos-2022.plant-tears-recycles-only-062</sub>

### recycle: slow

- **Synthesis loop section, Broyden. Expected: A converged loop.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: synthesis loop section, he5 min approach 2 k zones 10. <sub>methanol-co2-campos-2022.loop-iteration-limit-062</sub>
- **Settled start, Brent. Expected: 99.90 % ester.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, design spec ethanol feed for 99.9 pct ester. <sub>ethyl-acetate-piotrowski-2021.design-spec-ester-purity-415da41</sub>
- **Synthesis loop section, Broyden. Expected: A converged loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: synthesis loop section, iterations 50. <sub>methanol-co2-campos-2022.loop-50-iterations-062</sub>

## General design rules by operation

### absorber column

- **Packed absorbers and strippers: size the diameter for 60-80% of flooding**
  - When: You size a packed absorber or stripper.
  - Do: Size the diameter for 60 to 80% of the flooding capacity, and the packed height from earlier studies or a height-to-diameter ratio.
  - Why: Too close to flooding loses operability; too far wastes column.
  - Check: Check the fractional capacity at your highest vapour and liquid loads.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': operation unit design. <sub>palomar-2024-il-process-simulation.packed-column-capacity</sub>
- **Regeneration under vacuum: count the vacuum compressor's energy**
  - When: A regeneration column runs under vacuum.
  - Do: Model the vacuum system as a compressor that returns the vapour to atmospheric pressure, and count its energy in the utilities.
  - Why: A vacuum system is a compressor; leaving it out makes vacuum operation look cheaper than it is.
  - Check: In CHEPTA, add a compressor on the vacuum column's vapour and include its work in the energy comparison.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': process modelling and simulations. <sub>palomar-2024-il-process-simulation.vacuum-energy-counted</sub>

### azeotropic distillation

- **Esterification limited by water: remove the water azeotropically as it forms**
  - When: Water limits the conversion of an esterification.
  - Do: Couple the reaction with azeotropic water removal.
  - Why: Water leaves as it forms, so the equilibrium shifts towards the ester.
  - Check: Compare conversion with and without water removal in an equilibrium model.
  - Result: A shorter reaction and higher conversion; a study cited by Guo & Wang 2019, not read by Lab, reports 2.7% higher conversion for isoamyl acetate than ordinary water separation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Guo & Wang 2019, *Research Progress on Azeotropic Distillation Technology* (https://doi.org/10.4236/aces.2019.94024), Section 2.3, p. 337. <sub>guo-wang-2019-azeotropic-distillation.azeotropic-water-removal-in-esterification</sub>
- **Azeotropic distillation: prefer an entrainer that forms two liquids, so a decanter recovers it**
  - When: You choose an entrainer (an added component that breaks the azeotrope) for azeotropic distillation.
  - Do: Prefer one that forms two liquid phases with the mixture, so that a decanter separates it and returns it to the column.
  - Why: The decanter does part of the separation without heat. Homogeneous azeotropic distillation recirculates more azeotrope and uses more energy.
  - Check: In CHEPTA, set phases: "VLL" and check that the condensed overhead splits into two liquids at decanter temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Guo & Wang 2019, *Research Progress on Azeotropic Distillation Technology* (https://doi.org/10.4236/aces.2019.94024), Section 1, p. 334. <sub>guo-wang-2019-azeotropic-distillation.prefer-heterogeneous-entrainer</sub>
- **Ethanol dehydration: cyclohexane or hexane as entrainer; isooctane and toluene cost over 15% more**
  - When: You choose an entrainer for dehydrating a dilute ethanol broth (6 mol%) at atmospheric pressure.
  - Do: Prefer cyclohexane or hexane. Compare individually optimised processes for each solvent, not one fixed design.
  - Why: Each solvent changes the topology, the decanter split and the duties.
  - Check: Kruber & Skiborowski 2022 used NRTL with Aspen databank parameters (APV88) in their own optimisation: compare CHEPTA's azeotropes with theirs before reusing the ranking.
  - Result: Cyclohexane and hexane gave the same annual cost within estimate accuracy; isooctane and toluene cost over 15% more. Solvent make-up was below 0.4% of cost.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.1, pp. 9-10 (Fig. 4). <sub>kruber-skiborowski-2022-heteroazeotropic-init.ethanol-solvent-screen</sub>
- **Flat cost optimum: use the freedom to meet other constraints**
  - When: You must pick one design from many near-optimal ones.
  - Do: Use the flat optimum to trade larger columns against lower energy, or to meet other constraints.
  - Why: Stages and reflux trade off: nearly all Pareto-optimal designs (best trade-offs) fell within 5% of the minimum annual cost, while capital and operating cost shifted by about 20%.
  - Check: Cost a few designs along the trade-off before fixing one.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.2, p. 11 (Fig. 6); Section 3.2.1, p. 14 (Fig. 9). <sub>kruber-skiborowski-2022-heteroazeotropic-init.flat-cost-optimum</sub>
- **Heteroazeotropic distillation needs a heterogeneous azeotrope: two columns and a decanter**
  - When: You want to break an azeotrope by heteroazeotropic distillation.
  - Do: Check that the mixture forms a heterogeneous azeotrope (one that splits into two liquids); such an azeotrope is always minimum-boiling. Then use the usual process: a simple column and a heteroazeotropic column with a decanter, each giving one product as bottoms.
  - Why: The decanter crosses the distillation boundary (a line a column profile cannot cross) by splitting the liquid.
  - Check: In CHEPTA, set phases: "VLL" and confirm that the azeotrope splits into two liquids. Alternatives: extractive or pressure-swing distillation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 1; Section 2.1, p. 4 (Fig. 1). <sub>kruber-skiborowski-2022-heteroazeotropic-init.heteroazeotrope-prerequisite</sub>
- **No general rule for pre-concentration: run the feed scan for your case**
  - When: You want to reuse a pre-concentration rule from another mixture.
  - Do: Run the feed-composition scan for the case at hand.
  - Why: Each mixture's cost curve has its own shape: in the 1,4-dioxane case cost falls almost linearly with feed concentration, unlike the other two cases of Kruber & Skiborowski 2022.
  - Check: Plot specific cost against feed concentration and look for a knee.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.3.2, p. 18 (Fig. 13). <sub>kruber-skiborowski-2022-heteroazeotropic-init.no-general-preconcentration-heuristic</sub>
- **Dilute ethanol: pre-concentrating to about 20 mol% may pay**
  - When: The ethanol feed to heteroazeotropic dehydration is very dilute.
  - Do: Consider a pre-concentration step near the knee of the cost curve, about 20 mol% ethanol. For a feed already in the flat region, such as the ethyl acetate case of Kruber & Skiborowski 2022, it would not pay.
  - Why: At low feed concentration most of the cost goes to handling water: specific cost falls steeply up to about 20 mol% and then flattens.
  - Check: A cited study found the saving too small for an extra column, and Kruber & Skiborowski 2022 leave it open: run your own feed-composition scan.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.3, pp. 12-13 (Fig. 7); Section 3.2.2, p. 15 (Fig. 10). <sub>kruber-skiborowski-2022-heteroazeotropic-init.preconcentrate-dilute-ethanol</sub>
- **Heteroazeotropic solvent choice: simple indicators mislead, so screen with a process model**
  - When: You choose a solvent for heteroazeotropic distillation.
  - Do: Screen solvents with a process model, not on selectivity alone.
  - Why: Three ternary topologies, with four, three or two azeotropes, cover most cases (about 26%, 8% and 21% of 1365 surveyed mixtures, cited by Kruber & Skiborowski 2022). Their several azeotropes and distillation regions defeat simple indicators.
  - Check: Compare individually optimised processes for each solvent.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 2; Section 2.2, p. 6 (Fig. 2). <sub>kruber-skiborowski-2022-heteroazeotropic-init.three-common-topologies</sub>
- **Acetic acid from water: heterogeneous azeotropic distillation with butyl acetate as entrainer**
  - When: Acetic acid and water form no azeotrope but are close-boiling.
  - Do: Use heterogeneous azeotropic distillation with n-butyl acetate as entrainer. For dilute feeds add a preconcentrator column.
  - Why: The entrainer carries water overhead as a heterogeneous azeotrope that splits in a decanter.
  - Check: In CHEPTA, set phases: "VLL" and check the water-ester split in the decanter.
  - Result: A study cited by Valentini & Vaccaro 2020, not read by Lab, cut annual cost by 55% against plain distillation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.2. <sub>valentini-2020-azeotropes-waste.butyl-acetate-entrainer-for-acid-water</sub>
- **Screening heterogeneous entrainers: miscibility gap, azeotrope composition, temperature gaps**
  - When: You choose among many candidate entrainers.
  - Do: Screen on three criteria before simulating: the width of the miscibility gap (the two-liquid region), the composition of the azeotrope each forms, and the temperature gaps to the other azeotropes.
  - Why: These properties decide the decanter split and whether the column is feasible.
  - Check: Compute the three criteria with the property method for each candidate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.2 (cited screening of 60 candidates). <sub>valentini-2020-azeotropes-waste.entrainer-screening-criteria</sub>
- **Heterogeneous azeotropic distillation can be built as a dividing-wall column**
  - When: Azeotropic distillation uses a lot of energy.
  - Do: Consider a heterogeneous azeotropic dividing-wall column (one shell with an internal wall).
  - Why: Thermal coupling avoids remixing.
  - Check: Compare with the two-column process on the same basis.
  - Result: About 33% less energy and 20% lower annual cost in a solvent-recovery case cited by Valentini & Vaccaro 2020, not read by Lab.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.2. <sub>valentini-2020-azeotropes-waste.heteroazeotropic-dwc</sub>
- **Solvent waste with several azeotropes and water: use the water as the entrainer**
  - When: An aqueous solvent waste holds several azeotropes.
  - Do: Use hybrid extractive-heterogeneous azeotropic distillation, with the water already present as the entrainer.
  - Why: Water acts as the extractive agent and forms separable heterogeneous azeotropes, so no new component is added.
  - Check: Map the azeotropes of the mixture first.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.3. <sub>valentini-2020-azeotropes-waste.water-as-auto-entrainer</sub>

### cstr

- **Esterification catalyst: prefer a solid acid to a dissolved mineral acid**
  - When: You choose a catalyst for esterification.
  - Do: Prefer a solid acid catalyst where its temperature limit allows.
  - Why: A dissolved acid is active but corrodes equipment, cannot be recovered and stays in the product, adding purification steps. A solid catalyst stays in the reactor.
  - Check: Check the solid catalyst's temperature limit against the reaction temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Sections 2.1 and 2.2. <sub>hoff-eisenacher-2025-esterification-review.homogeneous-acid-drawbacks</sub>
- **Large continuous plant: stirred tanks in series, not one tank**
  - When: A continuous reactor gives lower conversion than the batch process.
  - Do: Use stirred tanks in series.
  - Why: One tank is fully back-mixed; tanks in series approach plug flow and batch-like conversion.
  - Check: In CHEPTA, compare the conversion of one, two and three stirred tanks of the same total volume.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design of biodiesel production using chemical catalyst'. <sub>pasha-2021-biodiesel-process-design.continuous-cstrs-in-series</sub>

### decanter

- **Reactive column overhead: decant, draw off the water, return all the organic phase as reflux**
  - When: The overhead of a butyl acetate reactive column condenses into water and an organic (butanol and ester) phase.
  - Do: Condense into a decanter, draw the water phase off as wastewater (about 102 kmol/h in Al-Rabiah et al. 2022) and return the whole organic phase to the column as reflux. The conventional route uses extractive distillation with a solvent instead.
  - Why: Water and the butanol-ester phase split into two liquids, so water leaves without taking the reactants and the ester with it.
  - Check: In CHEPTA, set phases: "VLL" on the decanter and compare the water phase's flow and composition with stream 3 of Table 9.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.2, p. 15 (Fig. 16, Table 9 stream 3). <sub>al-rabiah-2022.rd-decanter-returns-organic</sub>
- **In butyl acetate reactive distillation most ester is lost in the decanter's water phase, not the bottoms**
  - When: You check product losses and wastewater load of a reactive column with a decanter.
  - Do: Check the aqueous phase composition when matching Al-Rabiah et al. 2022: per 100 kmol/h of each feed, their wastewater carries about 1.5 kmol/h ester, 1.3 acid and 0.2 butanol.
  - Why: Ester, acid and water are partly soluble in each other, so the water phase carries some of each.
  - Check: In CHEPTA, compare the decanter's water phase with stream 3 of Table 9. That it holds more ester than the bottoms loses is Lab's reading of the table.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 9, p. 15 (streams 3-4). <sub>al-rabiah-2022.rd-loss-in-water-phase</sub>
- **Alcohol-water heteroazeotrope: a decanter with two strippers gives both pure**
  - When: An alcohol and water form a heterogeneous azeotrope (one that splits into two liquids), as isobutanol does.
  - Do: Condense into a decanter. Strip the organic layer in one column to get dry alcohol at its bottom, and the aqueous layer in another to get water at its bottom. Return both overheads to the decanter.
  - Why: The two liquids lie on either side of the azeotrope, so each stripper works inside its own region.
  - Check: Shown for isobutanol; 1-butanol and water form the same kind of azeotrope, a transfer not tested here. In CHEPTA, set phases: "VLL" on the decanter and check the two liquid compositions.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Fu et al. 2021, *Assessment of extraction options for a next-generation…* (https://doi.org/10.1002/elsc.202000090), Introduction (Fig. 1). <sub>fu-2021-isobutanol-recovery.decanter-with-two-strippers</sub>
- **Azeotrope building up in an azeotropic dehydration column: add a partial condenser before the decanter**
  - When: In azeotropic dehydration (of acetic acid, in a study cited by Guo & Wang 2019) the azeotrope accumulates in the column.
  - Do: Put a partial condenser between the column top and the decanter.
  - Why: Part of the overhead is condensed and handled before the decanter, so the azeotrope stops building up in the column.
  - Check: A cited result not read by Lab: compare the column profiles with and without the partial condenser in a simulation.
  - Result: Less accumulation and lower energy use.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Guo & Wang 2019, *Research Progress on Azeotropic Distillation Technology* (https://doi.org/10.4236/aces.2019.94024), Section 2.2, p. 336. <sub>guo-wang-2019-azeotropic-distillation.partial-condenser-before-decanter</sub>
- **Conceptual cost estimate: say whether the decanter is costed**
  - When: You cost a heteroazeotropic process at the concept stage.
  - Do: State the decanter as uncosted, or estimate its disengagement time (how long the two liquids need to separate) and size it.
  - Why: The decanter's size depends on a disengagement time that is usually not yet known.
  - Check: List the uncosted units with the cost estimate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.1, p. 5. <sub>kruber-skiborowski-2022-heteroazeotropic-init.decanter-uncosted-in-concept</sub>
- **Heavy liquid product limits conversion: reactors in series with decanters between them**
  - When: A heavy product phase (glycerol in biodiesel) limits conversion, and a reactant harms the catalyst at high concentration.
  - Do: Put decanters between reactors in series to remove the product phase as it forms, and add the reactant in stages.
  - Why: Removing the product phase and dosing the reactant keep conditions favourable for conversion and catalyst life.
  - Check: In CHEPTA, set phases: "VLL" on the decanters and check that the glycerol phase separates.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design of biodiesel production using biocatalyst'. <sub>pasha-2021-biodiesel-process-design.staged-decanting</sub>

### distillation

- **Butyl acetate purity near 99 mol% is set by the acetic acid excess, not by the column**
  - When: You try to match the ester purity of the conventional or the membrane-reactor route.
  - Do: Match the purity through the acid slip: about 1 kmol/h acetic acid (the small acid excess of the fresh feed) leaves with about 100 kmol/h ester in the bottoms. Do not over-purify the column to reach it.
  - Why: The unconsumed acid excess has no other exit, so it ends in the bottoms with the ester.
  - Check: The purities 99.0 and 98.9 mol% are Lab's arithmetic on Tables 4 and 7; Al-Rabiah et al. 2022 state 99.0 mol% for the membrane route. Table 4's stream labels disagree with the text (stream 1 is called butanol but holds 101 kmol/h acid): check before transcribing.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 4, p. 9 (streams 1, 2, 6); Table 7, p. 14 (streams 1, 2, 6). <sub>al-rabiah-2022.acid-slip-sets-purity</sub>
- **Butanol and butyl acetate form an azeotrope at 101 kPa: split them at about 300 kPa**
  - When: Unreacted n-butanol must be separated from butyl acetate after the reactor, and the two form an azeotrope at atmospheric pressure.
  - Do: Run the column at about 300 kPa, where the split is possible, with ester as bottoms and unreacted butanol and acid overhead for recycle. Expect many stages: Al-Rabiah et al. 2022 used 42 stages, feed on stage 21, reboiler 5.2 MW.
  - Why: Raising the pressure moves the azeotrope away from the composition you need to cross.
  - Check: In CHEPTA, confirm the azeotrope at 101 kPa and that it has moved at 300 kPa before building the column. Table 4 of Al-Rabiah et al. 2022 prints the bottoms at 3.2 kPa against 284 kPa overhead, probably a misprint: check before transcribing.
  - Result: Ester at 99.0 mol% as bottoms.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 5, pp. 7-10 (Figs. 9-10, Tables 4-5). <sub>al-rabiah-2022.butanol-ester-split-at-pressure</sub>
- **Count column duties early: the three-column butyl acetate route needed about eight times the steam of reactive distillation**
  - When: You rank routes where low conversion and an azeotrope multiply the number of columns.
  - Do: Estimate each route's column duties early, before detailed design.
  - Why: More columns and more recycled material mean more liquid to boil.
  - Check: The ratios 8.3 (against reactive distillation) and 5.2 (against the membrane route) are Lab's arithmetic on Table 10 of Al-Rabiah et al. 2022; the attribution to the columns is theirs.
  - Result: Medium-pressure steam 218,729 MWh/a for the conventional route.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 7.1, p. 16 (Table 10). <sub>al-rabiah-2022.conventional-steam-heavy</sub>
- **Do not design for a sharper split than the product needs**
  - When: The required purity is close to the feed composition.
  - Do: Set purities to what the product needs and accept a non-sharp split.
  - Why: Minimum reflux depends on the purity required; a sharp split costs much more reboiler duty.
  - Check: In CHEPTA, scan the purity specification and record the reboiler duty at each point.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.1, p. 304 (Fig. 4). <sub>blahusiak-2018-separation-selection.relax-purity</sub>
- **Choosing how to split two components: go by their relative volatility**
  - When: You must separate two components and know their relative volatility (alpha, how much more volatile one is than the other) at column conditions.
  - Do: Between about 1.3 and 10, use ordinary distillation. Consider a solvent to raise alpha only while alpha is below about 3. Below about 1.3, look at heat-pumped distillation or a solvent-based separation (extractive distillation or extraction) instead.
  - Why: Minimum reflux rises steeply as alpha falls towards one, so condenser and reboiler duties grow out of proportion.
  - Check: Work out alpha with the property method you will use, at both the top and the bottom of the column, since it changes along the column. In CHEPTA, flash the feed at column pressure and compare vapour and liquid compositions.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.1, p. 304 (Figs. 2-3). <sub>blahusiak-2018-separation-selection.volatility-ranges</sub>
- **Recover a used solvent or burn it: compare the recovery energy with the energy of making it**
  - When: You decide the fate of a waste solvent.
  - Do: Compare the energy of recovering it by distillation with the energy embodied in producing it. Tetrahydrofuran is worth recovering; diethyl ether is better incinerated.
  - Why: The energy needed to produce a solvent differs strongly between solvents.
  - Check: Estimate the recovery column's duty per kg of solvent and compare it with the production energy from a tool such as the ETH tool described by Byrne et al. 2016.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Byrne et al. 2016, *Tools and techniques for solvent selection* (https://doi.org/10.1186/s40508-016-0051-z), Recovery or incineration (ETH tool), p. 4. <sub>byrne-2016-solvent-selection-guides.recover-or-incinerate</sub>
- **Columns whose split improves at lower pressure: lower it, keeping the condenser above ambient**
  - When: Columns need high reflux and offer few heat-integration matches.
  - Do: Check each column's sensitivity to pressure. Lower the pressure where the split improves, but keep each condenser above ambient temperature.
  - Why: Lower pressure raises relative volatility and shifts column temperatures, which can widen the temperature differences for heat integration.
  - Check: In CHEPTA, scan the column pressure and record reflux, duties and condenser temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Chen et al. 2018, *Novel distillation process for effective and stable…* (https://doi.org/10.1186/s13068-018-1284-8), Methods: 'Decreasing the column pressure'. <sub>chen-2018-abe-distillation.lower-pressure-of-sensitive-columns</sub>
- **Sizing a dividing-wall column: optimise trays, reflux and both split ratios together**
  - When: You replace a two-column sequence for a sharp three-component split with a dividing-wall column.
  - Do: Optimise the number of trays, the reflux and the liquid and vapour split ratios (how flows divide either side of the wall) together.
  - Why: Fewer trays can match the split, but with too few the reflux rises steeply, and the split ratios set the internal flows.
  - Check: Scan trays and both split ratios and record reflux and duty at each point.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Conclusions, p. 165. <sub>henrique-2020-dwc-simulation.dwc-trays-reflux-splits</sub>
- **Three-component split: a prefractionator or dividing wall saves energy by avoiding remixing**
  - When: You separate a three-component mixture by distillation.
  - Do: Use a fully coupled (Petlyuk) arrangement, or its single-shell equivalent, a dividing-wall column, where the prefractionator does only a rough split.
  - Why: In a plain sequence the middle component is remixed, which wastes separation work; most of the coupled arrangement's saving comes from avoiding that.
  - Check: Compare the total duty with the best sequence of simple columns.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Introduction, p. 150. <sub>henrique-2020-dwc-simulation.prefractionator-avoids-remixing</sub>
- **Acetone, isopropanol and water: take acetone off first**
  - When: After the first concentration step you must split acetone, isopropanol and water.
  - Do: Use the direct sequence: take the most volatile product, acetone, as distillate of the first product column, and leave isopropanol and water for the azeotrope steps.
  - Why: Acetone is the lightest component and forms no azeotrope with the others (Table 1 of Janković et al. 2023).
  - Check: In CHEPTA, confirm that the property method shows no acetone azeotrope with water or isopropanol before fixing the sequence.
  - Result: Acetone at 99.8 wt% with 100% recovery.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, pp. 719-720. <sub>jankovic-2023-ipa-acetone-recovery.acetone-first</sub>
- **Broth with live cells: make the first separation a vacuum distillation at fermentation temperature**
  - When: Products must be recovered from a very dilute fermentation broth whose microorganisms should survive and go back to the fermenter.
  - Do: Keep the first separation at the fermentation temperature (30 C) by vacuum distillation, with the condenser at about 0.03 bar. Return the bottoms, holding the cells and most of the water, to the fermenter. Alternative: pass-through distillation.
  - Why: Low pressure lowers the boiling temperature to what the cells tolerate.
  - Check: Janković et al. 2023 cite, but did not test, that microbes survive the vacuum. In CHEPTA, check that the bottoms temperature at your column pressure stays at 30 C or below.
  - Result: Products recovered; cells and water recycled.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Methods, p. 715; Results, Vacuum distillation, p. 717. <sub>jankovic-2023-ipa-acetone-recovery.cold-first-separation-for-live-cells</sub>
- **Products from broth with over 94 wt% water cost about 1.3-2.0 kWh per kg: use this as a sanity check**
  - When: You judge whether a recovery route for a dilute broth is viable.
  - Do: Use these figures as an order-of-magnitude check of your design's primary energy per kg product.
  - Why: Handling the water dominates the energy of dilute recovery.
  - Check: The figures are Janković et al. 2023's simulations with heat pumping and heat integration. A much higher value in your design suggests looking for missing heat recovery.
  - Result: Isopropanol and acetone at 1.3-2.0 kWh primary energy per kg product; the vacuum design stays under 2 or 3 kWh/kg at 2.5 or 1.2 wt% products.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Abstract, p. 714; Results, Sustainability metrics, p. 723 (Table 5). <sub>jankovic-2023-ipa-acetone-recovery.dilute-energy-scale</sub>
- **Very low column pressure puts the condenser below cooling-water temperature: chilled water, or pass-through distillation**
  - When: A vacuum column's condenser falls below cooling-water temperature (about 10 C at 0.032 bar in Janković et al. 2023).
  - Do: Either pay for chilled water, or use pass-through distillation: absorb the vapour into lithium bromide brine and desorb it at higher pressure, where it condenses with cooling water.
  - Why: The absorbent loop separates evaporation at low pressure from condensation at higher pressure.
  - Check: Compare the condenser temperature at your pressure with the cooling-water supply temperature.
  - Result: With pass-through distillation, condensation at about 41 C and 0.2 bar.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Vacuum distillation, p. 717; Pass-through distillation, p. 718. <sub>jankovic-2023-ipa-acetone-recovery.vacuum-condenser-needs-chilled-water</sub>
- **Classic sequencing rule: leave the hardest split to last**
  - When: You choose the order of splits in a distillation sequence.
  - Do: Leave the most difficult split to last.
  - Why: A difficult split needs a high reflux ratio, which is cheaper with fewer components present.
  - Check: Li et al. 2023 report this classic rule and then qualify it: compare sequences quantitatively.
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule under this heading disagrees with this one; both are kept.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Section 2, p. 5. <sub>li-2023-distillation-sequences.hardest-split-last</sub>
- **The hardest split can also pay early: compare sequences by optimisation**
  - When: You choose the order of splits in a distillation sequence.
  - Do: Compare sequences quantitatively, by optimisation, rather than by a fixed rule.
  - Why: Two effects oppose: the high reflux of a difficult split, and the non-key components present during it, which inflate the column flows. Li et al. 2023 find the balance depends on the case.
  - Check: Screen with shortcut models plus heat integration, then simulate the best few rigorously.
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule under this heading disagrees with this one; both are kept.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Section 2, p. 5. <sub>li-2023-distillation-sequences.hardest-split-not-always-last</sub>
- **Choose column pressure so the condenser can use cooling water**
  - When: A column's condenser temperature would need refrigeration.
  - Do: Raise the column pressure until the condenser can use cooling water, and set it together with the heat integration.
  - Why: Higher pressure raises the condensing temperature.
  - Check: In CHEPTA, scan the pressure and record condenser and reboiler temperatures against your utilities.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Section 2, p. 5. <sub>li-2023-distillation-sequences.pressure-for-cooling-water</sub>
- **Many sequences to compare: screen with shortcut models and heat integration, simulate only the best few**
  - When: There are too many distillation sequences to simulate rigorously.
  - Do: Screen with shortcut column models (Fenske-Underwood-Gilliland) combined with heat-exchanger network synthesis, and simulate only the best few rigorously.
  - Why: For zeotropic mixtures (no azeotropes) shortcuts rank sequences as rigorous models do.
  - Check: Li et al. 2023 showed this for zeotropic hydrocarbons only: do not rely on it for azeotropic mixtures without a rigorous check.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Abstract, p. 1; Conclusions, p. 14. <sub>li-2023-distillation-sequences.shortcut-screening</sub>
- **Ethylene glycol via ethylene carbonate: far fewer heavy glycols and less water than direct hydration**
  - When: Direct hydration forces a large water excess and makes heavy glycols.
  - Do: Consider routing through ethylene carbonate; its hydrolysis needs water close to stoichiometric.
  - Why: The carbonate intermediate hydrolyses selectively with little water, so purification needs less water removal and simpler heavy-glycol handling.
  - Check: These are simulation numbers without an evidence row in Lab: check them against the stream tables before reuse.
  - Result: Heavy glycols 1,532 against 22,270 t/a in Shehata et al. 2024's simulations.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'Indirect hydration process', p. 6; 'MEG production via indirect EO hydration process', p. 9. <sub>shehata-2024-meg-routes.carbonate-route-fewer-heavy-glycols</sub>
- **Glycol columns under vacuum, so the bottoms stay below about 170 C**
  - When: Glycol would degrade at the temperatures of atmospheric distillation.
  - Do: Run the dehydration and product columns under vacuum so the bottoms stay below the degradation temperature (170 C in Shehata et al. 2024). Draw the product glycol from the side; heavier glycols leave at the bottom.
  - Why: Lower pressure lowers the boiling temperatures.
  - Check: In CHEPTA, check the reboiler temperature at the chosen pressure.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'MEG production via direct EO hydration process', p. 8. <sub>shehata-2024-meg-routes.vacuum-glycol-columns</sub>

### equilibrium reactor

- **Butyl acetate equilibrium: a hotter reactor gives lower, not higher, conversion**
  - When: You want more conversion from the esterification of n-butanol with acetic acid in a plain reactor.
  - Do: Do not raise the temperature to beat the equilibrium limit. Remove a product instead.
  - Why: The reaction is mildly exothermic (about -29 kJ/mol), so its equilibrium shifts back as temperature rises (Le Chatelier).
  - Check: In CHEPTA, scan an equilibrium reactor's temperature and confirm that conversion falls as temperature rises. Al-Rabiah et al. 2022 show the curve in Fig. 1 only, not as a table.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, pp. 2-3 (Eq. 1, Fig. 1); Section 6.1, p. 12 (Fig. 13). <sub>al-rabiah-2022.equilibrium-conversion-falls-with-temperature</sub>

### extraction

- **Acetic acid from water: use a solvent-based separation, with water leaving at the top**
  - When: You recover acetic acid from water.
  - Do: Prefer extraction or a solvent-based distillation (extractive or azeotropic). In either distillation water leaves at the top, because the acid is the heavy component.
  - Why: Acetic acid and water have a low relative volatility and a tangent pinch (the equilibrium curve nearly touches the diagonal) at high acid purity, so plain distillation is costly.
  - Check: In CHEPTA, tabulate the acid-water equilibrium at high acid purity to see the pinch, using vapour association for the acid where the method offers it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 3.4, p. 316. <sub>blahusiak-2018-separation-selection.acetic-acid-water-solvent-based</sub>
- **One component dilute in a large stream: try extraction or extractive distillation before plain distillation**
  - When: The feed is strongly asymmetric: the component you want is dilute in a large stream.
  - Do: Consider an affinity separation (one using a solvent's preference for a component), liquid-liquid extraction or extractive distillation, before plain distillation.
  - Why: Distillation must vaporise the bulk, so its internal efficiency is low on such feeds.
  - Check: Compare the reboiler duty per kg of recovered component with the energy of the extraction route.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.1, p. 304; Conclusions, p. 317. <sub>blahusiak-2018-separation-selection.avoid-distillation-for-dilute-feeds</sub>
- **Light solvent for acetic acid extraction, such as ethyl acetate: it takes water along, but the water splits out on cooling**
  - When: You extract acetic acid from water with a low-boiling solvent such as ethyl acetate.
  - Do: Expect much co-extracted water, and use the solvent-water heterogeneous azeotrope (one that separates into two liquids) in a decanter during solvent regeneration.
  - Why: The azeotrope splits into a solvent phase and a water phase on cooling, so less has to be boiled.
  - Check: In CHEPTA, set phases: "VLL" on the regeneration decanter and check that the condensed overhead splits into two liquids.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 3.4, p. 316 (Fig. 20). <sub>blahusiak-2018-separation-selection.low-boiling-solvent-coextracts-water</sub>
- **Need an ether solvent: use 2-methyltetrahydrofuran or tert-butyl methyl ether**
  - When: A process needs an ether solvent and tetrahydrofuran or diethyl ether are candidates.
  - Do: Use 2-methyltetrahydrofuran or tert-butyl methyl ether instead of tetrahydrofuran and diethyl ether.
  - Why: Safer ethers exist that do a similar job (Byrne et al. 2016).
  - Check: Check with the property method that the substitute gives the solubility and phase behaviour you need.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Byrne et al. 2016, *Tools and techniques for solvent selection* (https://doi.org/10.1186/s40508-016-0051-z), Unified guides, p. 9. <sub>byrne-2016-solvent-selection-guides.ether-substitutes</sub>
- **Choosing a solvent or entrainer: start from the green list of the pharmaceutical guides**
  - When: You choose a solvent or entrainer and want to avoid health, safety and environmental problems.
  - Do: Prefer solvents rated green across the Pfizer, GSK and Sanofi guides: water, n-propyl and isopropyl acetate, 1- and 2-butanol. Justify any undesirable one: chlorinated solvents, NMP, DMF and DMAc (polar aprotic solvents), benzene, hexane, 1,4-dioxane, diethyl ether.
  - Why: The solvents' health, safety and environmental ratings differ widely.
  - Check: NMP and DMF, rated undesirable here, are the extractive solvents studied in Li et al. 2017: report the trade-off if a case uses them.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Byrne et al. 2016, *Tools and techniques for solvent selection* (https://doi.org/10.1186/s40508-016-0051-z), Unified guides, pp. 8-9 (Figs. 6-7). <sub>byrne-2016-solvent-selection-guides.green-and-undesirable-solvents</sub>
- **Alcohol from water: add a salting-out salt such as potassium carbonate before distillation**
  - When: You recover an alcohol (isobutanol in Fu et al. 2021) from water.
  - Do: Add a strong salting-out salt (one that pushes organics out of water), such as potassium carbonate, then distil.
  - Why: The ions bind water and push the alcohol out; the salt stays in the aqueous phase.
  - Check: This needs an electrolyte property model: check that one is available before planning the case.
  - Result: Higher alcohol partition and dehydration, and less energy than solvent extraction.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Fu et al. 2021, *Assessment of extraction options for a next-generation…* (https://doi.org/10.1002/elsc.202000090), Concluding remarks. <sub>fu-2021-isobutanol-recovery.salting-out</sub>
- **Mixed extractants: choose boiling points so regeneration needs no extra column**
  - When: You regenerate a mixture of extractants after liquid-liquid extraction.
  - Do: Pick extractants whose boiling points let regeneration take each one overhead or at the bottom without an extra column.
  - Why: The boiling order fixes the regeneration sequence.
  - Check: List the boiling points of products and extractants and draw the regeneration sequence before simulating.
  - Result: A heavier biocompatible extractant cut the regeneration section from three columns to two (Grisales Díaz & Olivar Tost 2017).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Grisales Díaz & Olivar Tost 2017, *Techno-economic analysis of extraction-based separation systems for…* (https://doi.org/10.1186/s40643-017-0142-z), Methods: 'Extractant selection'. <sub>grisales-2017-abe-extraction.extractant-boiling-for-fewer-columns</sub>
- **Dilute product stream: its concentration sets the energy per kg**
  - When: You recover a product from a dilute stream and the energy per kg is high.
  - Do: Raise the product concentration fed to separation (the upstream yield) where possible, before optimising the separation.
  - Why: Energy scales with the solvent or water handled per unit of product.
  - Check: Plot energy per kg product against feed concentration in your simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Grisales Díaz & Olivar Tost 2017, *Techno-economic analysis of extraction-based separation systems for…* (https://doi.org/10.1186/s40643-017-0142-z), Conclusions. <sub>grisales-2017-abe-extraction.feed-concentration-dominates</sub>

### extractive distillation

- **Start the 1,4-butanediol extractive column at about 2.4 mol solvent per mol feed**
  - When: You transcribe or design the extractive column of the conventional butyl acetate route and need a first solvent flow.
  - Do: Start from Al-Rabiah et al. 2022's stream table: about 440 kmol/h of 1,4-butanediol against about 186 kmol/h of distillate (100 water, 43 butanol, 42 acid), roughly 2.4 mol per mol.
  - Why: The column needs enough solvent on every stage above the feed to break the azeotrope.
  - Check: The ratio is Lab's arithmetic (440.3 / 185.7, Table 7). In CHEPTA, scan the solvent flow around it and record where water purity and butanol recovery are met.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p. 14 (streams 5, 9, 13). <sub>al-rabiah-2022.butanediol-circulation-ratio</sub>
- **Water with butanol and acetic acid in a recycle: extractive distillation with 1,4-butanediol**
  - When: In the conventional butyl acetate route the first column's distillate holds water with unreacted butanol and acid, and butanol forms an azeotrope with water.
  - Do: Feed 1,4-butanediol (a heavy polar solvent) at the top of an extractive column (29 stages in Al-Rabiah et al. 2022). Water leaves overhead to treatment; a recovery column returns the solvent and sends acid and butanol back to the reactor. Alternative: reactive distillation with a decanter needs no solvent.
  - Why: The heavy solvent holds butanol and acid back in the liquid, so water distils off.
  - Check: Al-Rabiah et al. 2022 print no stage numbers or reflux for the first and the recovery column, and their text sends the solvent to T-101 where Fig. 11 suggests T-102. Resolve both before transcribing.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, p. 3 (Fig. 2); Section 6.1, p. 12 (Figs. 11 and 15); Table 7, p. 14. <sub>al-rabiah-2022.conventional-extractive-with-butanediol</sub>
- **Extractive solvent: boiling at least 50 C above the mixture, chosen on selectivity before capacity**
  - When: You screen solvents for an extractive separation.
  - Do: Choose a solvent that boils at least 50 C above the mixture, and weigh selectivity (how well it tells the two components apart) above capacity (how much it dissolves).
  - Why: A large boiling gap keeps the solvent from forming an azeotrope or a pinch during regeneration.
  - Check: Check for azeotropes between the solvent and each component with the property method before simulating the column.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.4, p. 311; Conclusions, p. 317. <sub>blahusiak-2018-separation-selection.solvent-boiling-gap-and-selectivity</sub>
- **Isopropanol stuck at its azeotrope with water: extractive distillation with ethylene glycol, solvent about 1.1 times the feed by mass**
  - When: You need dry isopropanol from a pre-concentrated isopropanol-water stream, which plain distillation cannot take past the azeotrope.
  - Do: Feed ethylene glycol near the top of an extractive column. Isopropanol leaves overhead; glycol and water leave at the bottom to a solvent-recovery column that returns the glycol. Scan the solvent-to-feed mass ratio: Janković et al. 2023 found 1.1 gave the lowest energy for the two columns together.
  - Why: Ethylene glycol holds water back in the liquid, so isopropanol becomes the more volatile component and distils overhead.
  - Check: In CHEPTA, scan the solvent-to-feed ratio around 1.1 and record the summed reboiler duty of both columns and the isopropanol purity. If the minimum lies far from 1.1, compare the property methods before changing the design.
  - Result: Isopropanol at 99.8 wt% overhead, with both columns at atmospheric pressure.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 720 (Fig. 5b). Lab reread Results, p. 721 on 2026-11-20 (ratio on a mass basis, for columns C4 and C5). <sub>jankovic-2023-ipa-acetone-recovery.ethylene-glycol-solvent-ratio</sub>
- **Dilute isopropanol: pre-concentrate to about 86 wt% before extractive dehydration**
  - When: The isopropanol stream to be dehydrated is dilute (about 31 wt% in Janković et al. 2023).
  - Do: Pre-concentrate in a plain column first. Scan the distillate target and take the minimum of total energy; it fell up to about 86 wt% isopropanol, which was chosen.
  - Why: Getting closer to the azeotrope costs more in the pre-concentrator but less in dehydration, so the sum has a minimum.
  - Check: Stay below the homogeneous azeotrope (87.17 mass % isopropanol at 80.23 C, Table 1). In CHEPTA, scan the distillate purity and add the duties of both steps.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 720 (Fig. 5a); Table 1, p. 716. <sub>jankovic-2023-ipa-acetone-recovery.preconcentrate-before-extractive</sub>
- **Picking an extractive solvent: high boiling, stable, easy to recover, low toxicity; screen by the volatility it adds**
  - When: You choose a solvent for extractive distillation.
  - Do: Pick one that boils well above the mixture, is thermally stable, easy to recover and of low toxicity. Screen candidates by how much they raise the key relative volatility, and by residue curve maps (how a boiling liquid's composition moves) free of distillation boundaries.
  - Why: The solvent works by changing the activity coefficients of the key pair.
  - Check: In CHEPTA, compute the key pair's relative volatility with and without the solvent.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2017, *Phase Behavior and Thermodynamic Model Parameters in…* (https://doi.org/10.1038/s41598-017-09088-2), Introduction. <sub>li-2017-ed-thermo-parameters.extractive-solvent-criteria</sub>
- **Tetrahydrofuran and water: extractive distillation was cheaper at steady state, but weigh control too**
  - When: You compare extractive and pressure-swing distillation for tetrahydrofuran and water on cost.
  - Do: Compare on annual cost and on controllability; expect a trade-off, not a single winner, as Mtogo et al. 2021 argue.
  - Why: Extractive distillation used less energy at steady state in a study cited by Mtogo et al. 2021, not read by Lab.
  - Check: Recompute both annual costs on the same basis.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Mtogo et al. 2021, *Comparison of Controllability Features of Extractive and…* (https://doi.org/10.1021/acsomega.1c04606), Introduction. <sub>mtogo-2021-ed-vs-psd.ed-cheaper-steady-state</sub>

### flash

- **Broth with dissolved CO2: degas it first and recapture any product it strips**
  - When: The fermentation broth holds dissolved CO2 and goes to a vacuum recovery train.
  - Do: Add a degassing step under reduced pressure first, and recover any product it strips with water in a small stripping column.
  - Why: Gas that does not condense would load the vacuum system and the condensers.
  - Check: Janković et al. 2023 propose this without simulating it. Measure the gas in your feed and the product lost with it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Full recovery processes, p. 721. <sub>jankovic-2023-ipa-acetone-recovery.degas-before-recovery</sub>

### heat integration

- **Include reboilers and condensers in the pinch analysis, and keep each column on one side of the pinch**
  - When: You run a pinch analysis (heat-recovery targeting) on a plant with columns.
  - Do: Include every reboiler and condenser in the stream data. Place each column entirely above or entirely below the pinch (the temperature where heat recovery is tightest).
  - Why: A column that straddles the pinch moves heat across it.
  - Check: Plot each column's reboiler and condenser temperatures against the pinch temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Pinch analysis of the full system, p. 15. <sub>ali-2022-eg-plant-pinch.columns-in-pinch-analysis</sub>
- **Steam turbine or other heat engine: let it reject its heat below the pinch**
  - When: You integrate a heat engine such as a steam turbine into the plant's heat network.
  - Do: Position it with the grand composite curve (net heat flow against temperature) so that it rejects heat below the pinch.
  - Why: Heat rejected below the pinch replaces heat that would otherwise go to cooling.
  - Check: Check on the grand composite curve that the engine's exhaust temperature lies below the pinch.
  - Result: About another 6% less external cooling in Ali et al. 2022's plant.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Conclusion, p. 19 (grand composite curve). <sub>ali-2022-eg-plant-pinch.heat-engine-below-pinch</sub>
- **Ethylene glycol plant: use the ethylene oxide reactor's surplus heat in the glycol section**
  - When: One section exports heat (the exothermic ethylene oxidation) while another imports it (glycol dehydration and separation).
  - Do: Heat-integrate the reaction section with the glycol section.
  - Why: Matching a heat source with a heat sink replaces external utilities on both sides.
  - Check: Run a pinch analysis (heat-recovery targeting) on the whole plant, columns included, to get the targets.
  - Result: In Ali et al. 2022's plant the retrofit targets cut external heating by about 93% and cooling by about 45%.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Conclusion, p. 19. <sub>ali-2022-eg-plant-pinch.integrate-eo-reactor-with-glycol-section</sub>
- **Never move heat across the pinch**
  - When: You design the heat exchanger network after a pinch analysis.
  - Do: Never transfer heat across the pinch. At the pinch, match streams so the hot stream's heat-capacity flow (mass flow times heat capacity) is no larger than the cold stream's above the pinch and no smaller below it.
  - Why: Heat moved across the pinch must be supplied again as hot utility and removed again as cold utility, so it costs twice.
  - Check: Compare the network's utility use with the pinch targets; any excess points to a match across the pinch.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Heat exchanger network rules, p. 16. <sub>ali-2022-eg-plant-pinch.no-transfer-across-pinch</sub>
- **Heat pump on a column: worth it when reboiler duty is above about 10 times the compressor work**
  - When: You consider vapour recompression for a column.
  - Do: Divide the reboiler duty by the compressor work. Above about 10 a heat pump pays; below about 5 it does not.
  - Why: Compressor work grows with the temperature lift, so heat pumps suit close-boiling columns with a small top-to-bottom temperature difference.
  - Check: Estimate the compressor work from the condenser and reboiler temperatures before adding the heat pump.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Heat pumps, p. 313 (Fig. 15). <sub>blahusiak-2018-separation-selection.heat-pump-criterion</sub>
- **Dilute recovery: minimise external energy first, then check the cost**
  - When: You set the design objective early for recovering products from a dilute broth.
  - Do: Minimise external energy as the design objective, then check the costs.
  - Why: Operating cost, mostly energy, outweighs capital except for very short payback periods (Janković et al. 2023).
  - Check: Confirm with a cost estimate that capital stays the smaller share at your payback period.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Methods, p. 715. <sub>jankovic-2023-ipa-acetone-recovery.minimise-energy-as-cost-proxy</sub>
- **Column with a small temperature lift and a big reboiler: use mechanical vapour recompression**
  - When: A column's top and bottom temperatures are close and its reboiler duty is large (about 22 MW for the vacuum column of Janković et al. 2023).
  - Do: Compress the overhead vapour and use it to boil the bottoms (mechanical vapour recompression, a heat pump). It pays when its coefficient of performance (heat delivered per unit of work) clearly exceeds the electricity-to-heat price factor.
  - Why: Compressed overhead vapour condenses hot enough to boil the bottoms, and a small temperature lift needs little compressor work.
  - Check: Work out the coefficient of performance from the column's top and bottom temperatures and compare it with your site's factor.
  - Result: Coefficient of performance 8.8 for the vacuum column, against an assumed factor of 2.5: much lower energy use.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Vacuum distillation, p. 717; Methods, p. 716. <sub>jankovic-2023-ipa-acetone-recovery.mvr-when-temperatures-close</sub>
- **Wide temperature span across a column: no vapour recompression; boil its bottoms with the hot recovered solvent instead**
  - When: Extractive and solvent-recovery columns have a wide top-to-bottom temperature span.
  - Do: Do not use vapour recompression on them. Use the hot solvent from the recovery column, which must be cooled before reuse anyway, to boil part of the extractive column's bottoms.
  - Why: A heat pump across a large temperature lift needs too much compressor work, while the solvent's heat is free.
  - Check: Check that the solvent is hotter than the extractive column's bottoms by a workable approach.
  - Result: 16-17% less external heat for the extractive column (Janković et al. 2023).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 720. <sub>jankovic-2023-ipa-acetone-recovery.no-mvr-wide-temperature-span</sub>
- **Subcooled column feed after a vacuum step: preheat it with process heat**
  - When: The vacuum overhead becomes a subcooled liquid after pumping to atmospheric pressure and feeds the next column.
  - Do: Preheat it with hot water bottoms or hot solvent, heat that must be removed anyway.
  - Why: A subcooled feed must first be heated inside the column, which adds to the reboiler duty.
  - Check: Compare the reboiler duty with and without the preheat in your simulation.
  - Result: The acetone column's reboiler duty fell by 12-41% (Janković et al. 2023).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 721. <sub>jankovic-2023-ipa-acetone-recovery.preheat-subcooled-feed</sub>
- **Heat pump or multi-effect: let the heat-to-electricity price ratio decide**
  - When: You rank recovery designs that use heat pumps (electricity) against multi-effect desorption (steam).
  - Do: Report the ranking with the utility prices it assumes. Cheap heat favours multi-effect desorption; cheap electricity favours the heat-pump designs.
  - Why: Heat pumps run on electricity and multi-effect on steam, so their order flips with the price ratio.
  - Check: Recompute the ranking at your own site's prices.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Economic evaluation, p. 722. <sub>jankovic-2023-ipa-acetone-recovery.price-ratio-decides-configuration</sub>
- **Feed the first column's distillate to the next column as vapour**
  - When: The first column's distillate is condensed, then reboiled again in the heteroazeotropic column.
  - Do: Send the distillate as vapour, without condensing it.
  - Why: The vapour's latent heat goes straight into the second column.
  - Check: Compare the second column's reboiler duty with a liquid and with a vapour feed.
  - Result: Reboiler duty about 59% lower (163 against 402 kW) in the 1,4-dioxane case.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.3, p. 16 (Fig. 11). <sub>kruber-skiborowski-2022-heteroazeotropic-init.vapour-distillate-feed</sub>
- **Thermally coupled columns against simple ones: compare with heat integration included**
  - When: You choose between thermally coupled complex columns and sequences of simple columns.
  - Do: Include heat integration in both options before comparing them.
  - Why: Without heat integration coupled columns win by a wide margin; heat integration recovers much of what coupling saves, so the gap narrows a lot.
  - Check: Run the pinch targets for both options.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Abstract, p. 1. <sub>li-2023-distillation-sequences.coupled-columns-vs-heat-integration</sub>
- **Biodiesel plants: pinch analysis cut utilities by about 11-16%**
  - When: A biodiesel plant with several distillation steps uses much heating and cooling.
  - Do: Apply pinch analysis (heat-recovery targeting) to match hot and cold streams.
  - Why: Matching hot and cold streams recovers heat.
  - Check: Compare your utility use with the pinch targets.
  - Result: Heating and cooling utilities fell by roughly 11 to 16% in studies cited by Pasha et al. 2021, not read by Lab.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Heat integration'. <sub>pasha-2021-biodiesel-process-design.pinch-savings-biodiesel</sub>
- **Carbonation of ethylene oxide is strongly exothermic: raise low-pressure steam from it**
  - When: Heat must be removed from the carbonate reactors.
  - Do: Use the reactor cooling to raise low-pressure steam.
  - Why: The heat removed is at a useful temperature.
  - Check: Check that the reactor temperature lies far enough above the steam's saturation temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'MEG production via indirect EO hydration process', pp. 7-8. <sub>shehata-2024-meg-routes.carbonation-heat-to-steam</sub>
- **Dilute glycol: multi-effect evaporators first, vacuum column last**
  - When: A dilute glycol solution after hydration needs most of its water boiled off.
  - Do: Remove most of the water in evaporators at falling pressure, each heated by the vapour of the one before, then finish in a vacuum dehydration column.
  - Why: Reusing each evaporator's vapour to heat the next divides the steam demand.
  - Check: In CHEPTA, check that each evaporator still has a positive temperature difference at its pressure.
  - Result: In Shehata et al. 2024's simulation the evaporators take about 75% of the water and only the first uses steam.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'MEG production via direct EO hydration process', p. 8 (Fig. 5). <sub>shehata-2024-meg-routes.evaporator-train-before-vacuum-column</sub>

### membrane

- **Excess acetic acid raises butanol conversion but makes the ester harder to purify: stay near 1:1**
  - When: You choose the acetic acid to n-butanol feed ratio of a butyl acetate reactor.
  - Do: Keep the feed near stoichiometric, as Al-Rabiah et al. 2022 did (1:1), unless the extra conversion is worth a harder product column.
  - Why: An excess of one reactant pushes the equilibrium further, but the excess must be removed from the product downstream.
  - Check: Scan the feed ratio and watch both conversion and the acid left in the ester. Al-Rabiah et al. 2022 state the trade-off in words only, without a purification cost.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 4, p. 6 (Fig. 5b); Table 3, p. 8. <sub>al-rabiah-2022.acid-excess-raises-conversion-hurts-purification</sub>
- **Membrane reactor solved outside the simulator: treat its outlet as an input, not a result**
  - When: A source solved one unit in another program and fed its outlet to the flowsheet. Al-Rabiah et al. 2022 did this for the membrane reactor (an ODE model, ordinary differential equations, in MATLAB, with water flux proportional to its concentration).
  - Do: Declare that outlet as an imposed boundary of the case. Compare only what the flowsheet itself computed.
  - Why: The flowsheet simulator never calculated that unit, so matching its outlet proves nothing about the simulation.
  - Check: List the imposed streams in the case and keep them out of the comparison table. This is Lab's rule for case boundaries, not one of Al-Rabiah et al. 2022.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 3, pp. 3-4 (Eqs. 7-12); Section 4, p. 7. <sub>al-rabiah-2022.membrane-reactor-model-imposed</sub>
- **Butyl acetate reactor stuck near 70% conversion: take the water out through a membrane**
  - When: n-Butanol and acetic acid react over Amberlyst-15 (an acidic ion-exchange resin) at 363 K with a 1:1 feed, and a plain fixed bed stops at about 70% butanol conversion.
  - Do: Fit the reactor with a water-selective hydroxy sodalite membrane (a zeolite membrane that lets water through) so water leaves as it forms. Al-Rabiah et al. 2022 took organic losses through the membrane as negligible.
  - Why: Water is a product of the reaction; removing it shifts the equilibrium towards the ester.
  - Check: Al-Rabiah et al. 2022 solved the membrane reactor outside Aspen Plus (in MATLAB). In a Lab case take its outlet as an imposed input, not as a reproduced result, and compare the downstream column with their stream table.
  - Result: Butanol conversion rose from about 70% to 92% in their model, which is fitted to one laboratory study (R2 0.9973), not to an industrial membrane.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Sections 3-5, pp. 3-7 (Eqs. 7-12, Tables 1-3, Figs. 5a and 7); Abstract, p. 1. <sub>al-rabiah-2022.membrane-reactor-removes-water</sub>

### pervaporation

- **Water-removal membrane in hot acid service: prefer zeolite-coated ceramic to polymer**
  - When: You choose a water-removal membrane for a hot reactive esterification mixture.
  - Do: Prefer zeolite-coated ceramic membranes (LTA or MFI type) to polymer films. Ceramic membranes can crack at large scale (Section 8.1).
  - Why: Inorganic supports resist swelling and chemical attack.
  - Check: Ask for long-term permeability data: a polyvinyl alcohol membrane is reported to lose up to 35% of its permeability in 1000 h.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Sections 5.1 and 8.1. <sub>hoff-eisenacher-2025-esterification-review.ceramic-vs-polymer-membranes</sub>
- **Esterification at equilibrium: remove water continuously, by reactive distillation or a membrane**
  - When: Esterification stops at equilibrium.
  - Do: Integrate water removal with the reaction: reactive distillation, or a pervaporation (membrane evaporation) or nanofiltration membrane in the reactor.
  - Why: Removing a product shifts the equilibrium, so conversion rises at milder conditions.
  - Check: Compare conversion with and without water removal in an equilibrium model.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Abstract; Sections 4.1 and 5. <sub>hoff-eisenacher-2025-esterification-review.water-removal-shifts-equilibrium</sub>
- **The purity target can change the best dehydration technology**
  - When: You choose a dehydration technology (for isobutanol, in a study cited by Valentini & Vaccaro 2020).
  - Do: Compare the technologies at the actual purity target.
  - Why: Membrane area and distillation duty scale differently with purity.
  - Check: Rerun the comparison at your own purity.
  - Result: At 98.8 wt% isobutanol pervaporation ranked above azeotropic distillation; at 99.9 wt% distillation-assisted pervaporation with heat integration was clearly best (a cited result, not read by Lab).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.4. <sub>valentini-2020-azeotropes-waste.purity-decides-pervaporation</sub>

### pfr

- **Butyl acetate in a fixed bed levels off near 70% conversion: plan to recycle both reactants**
  - When: A conventional fixed-bed reactor over Amberlyst-15 (an acidic ion-exchange resin) at 363 K with a 1:1 acid to butanol feed.
  - Do: Size the bed for a near-equilibrium outlet: more bed adds nothing once conversion levels off (within about 2.5 m in Al-Rabiah et al. 2022). Plan to separate and recycle the unreacted acid and butanol.
  - Why: The reactor reaches equilibrium quickly, at about 70% butanol conversion per pass.
  - Check: Check that the reactor outlet sits near 69.8% butanol conversion and that the recycle carries about 43 kmol/h of each reactant per 100 kmol/h fresh feed (Table 7 of Al-Rabiah et al. 2022).
  - Result: Conversion 69.8% with a 41 m3 reactor and 284 kPa feed pressure (Table 6); about 43 kmol/h each of acid and alcohol left to recycle.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, pp. 10-12 (Table 6, Fig. 14); Table 7, p. 14 (streams 3-4). <sub>al-rabiah-2022.fixed-bed-conversion-near-70</sub>
- **Two Amberlyst-15 rate laws for butyl acetate disagree on the equilibrium: use one model for all routes**
  - When: You compare butyl acetate routes that use different published rate laws for the same resin catalyst at 363 K.
  - Do: Use one consistent kinetic and equilibrium model across the routes, or report the difference. In Al-Rabiah et al. 2022 the fixed-bed law implies an equilibrium constant of about 5.0 (Lab's ratio of the forward and backward rate constants), while the membrane-reactor law uses 3.51.
  - Why: The two laws come from different literature sources. A larger equilibrium constant alone makes a route look better.
  - Check: Recompute the ratio from Eqs. 14-15 at 363 K before using it: the units of the rate constants are not printed and the concentration bases may differ.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 3, p. 3 (Eqs. 2-4); Section 6.1, p. 10 (Eqs. 13-15). <sub>al-rabiah-2022.kinetic-laws-imply-different-keq</sub>
- **Conventional glycol reactor: an adiabatic tube with a large water excess**
  - When: Back-mixing would bring product glycol into contact with fresh oxide.
  - Do: Use an adiabatic tubular reactor in turbulent flow without back-mixing, fed with oxide diluted in a large water excess.
  - Why: Plug flow keeps the residence time narrow, which limits further reaction of glycol with oxide and avoids oxide vapour breakthrough.
  - Check: In CHEPTA, model it as a plug-flow reactor and check the selectivity to monoethylene glycol.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Introduction, p. 2 (Fig. 1). <sub>othman-2024-meg-reactive-distillation.tubular-reactor-no-backmixing</sub>
- **Ethylene oxide hydration without catalyst: use a large water excess, and plan to evaporate it**
  - When: In non-catalytic hydration of ethylene oxide, glycol reacts further with the oxide to di- and triethylene glycol.
  - Do: Feed the hydration reactor with a high water to oxide ratio: 10 to 25 mol per mol oxide in the literature cited by Shehata et al. 2024, 10 in their simulation.
  - Why: Dilution makes the oxide meet water rather than glycol.
  - Check: Count the water to be evaporated downstream: it is the price of the selectivity.
  - Result: Higher monoethylene glycol selectivity, and a much larger water load.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'Indirect hydration process', p. 6; 'MEG production via direct EO hydration process', p. 8. <sub>shehata-2024-meg-routes.direct-hydration-water-excess</sub>

### pressure swing distillation

- **Tetrahydrofuran and water: pressure-swing distillation was easier to control than extractive distillation**
  - When: You choose between pressure-swing and extractive distillation for tetrahydrofuran and water.
  - Do: Weigh controllability together with cost.
  - Why: The added solvent of extractive distillation brings more interactions and longer time constants, which complicate control.
  - Check: Compare both routes' responses to feed disturbances in a dynamic model; a steady-state simulation alone cannot show controllability.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Mtogo et al. 2021, *Comparison of Controllability Features of Extractive and…* (https://doi.org/10.1021/acsomega.1c04606), Conclusions. <sub>mtogo-2021-ed-vs-psd.psd-better-controllability</sub>
- **Pressure-swing distillation: only for an azeotrope that moves with pressure, and heat-integrate the two columns**
  - When: You want to break an azeotrope without adding a third component.
  - Do: Check that the azeotrope composition moves with pressure. Then use two columns at different pressures, heat integrated.
  - Why: Changing the pressure moves the azeotrope, so each column can pass it. Without heat integration it uses more energy than extractive distillation.
  - Check: In CHEPTA, compute the azeotrope at both pressures and confirm that it moves enough.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Mtogo et al. 2021, *Comparison of Controllability Features of Extractive and…* (https://doi.org/10.1021/acsomega.1c04606), Introduction; Conclusions. <sub>mtogo-2021-ed-vs-psd.psd-needs-pressure-sensitive-azeotrope</sub>

### process route

- **Membrane-reactor route for butyl acetate loses on cost because of its butanol-ester column; it may win above about 95% conversion**
  - When: You compare a membrane-reactor route with reactive distillation for butyl acetate.
  - Do: Prefer reactive distillation unless the membrane reactor can exceed about 95% conversion. Al-Rabiah et al. 2022 state this threshold without showing a calculation.
  - Why: Unconverted butanol must be split from the ester in an energy-hungry column. Higher conversion shrinks that column.
  - Check: Redo the route comparison at the conversion your membrane can really reach.
  - Result: Return on investment 23.1% against 31.2%, payback 2.7 against 2.1 years (membrane route against reactive distillation).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 8, pp. 17-18 (Table 12); Section 9, p. 18. <sub>al-rabiah-2022.membrane-route-cost-set-by-column</sub>
- **Butyl acetate route: shortlist reactive distillation first, then a membrane reactor; the reactor with three columns came last**
  - When: You choose a route to n-butyl acetate from acetic acid and n-butanol. The reaction is limited by equilibrium and butanol forms an azeotrope with water.
  - Do: Shortlist reactive distillation (reaction and distillation in one column) and a membrane reactor against the conventional fixed-bed reactor with three columns. Al-Rabiah et al. 2022 compared all three in Aspen Plus at equal capacity (92,500 t/a) and equal product purity.
  - Why: Doing reaction and separation together loses less conversion to equilibrium and needs fewer columns.
  - Check: Compare routes on the same capacity, purity, property method and cost basis. Al-Rabiah et al. 2022 used NRTL and their own cost estimates (CEPCI 2021); all three routes are their simulations, not plant data.
  - Result: Reactive distillation first, the membrane reactor second, the conventional route last, on steam use, CO2 and cost.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Sections 7.1, 7.2 and 8, pp. 16-18 (Table 10, Figs. 18-19, Table 12). <sub>al-rabiah-2022.route-ranking-rd-mr-conventional</sub>
- **Detailed safety indices belong to detailed engineering, not the concept stage**
  - When: You choose a safety method for the current stage of design.
  - Do: Use simple indicator-based indices early. Keep indices that need equipment, complexity and vulnerability data, such as the inherent system safety index, for detailed engineering.
  - Why: The data these methods need differ by stage.
  - Check: Check that the index's inputs are available at your stage.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.3, p. 466. <sub>park-2022-inherently-safer-design.detailed-indices-later</sub>
- **Missing flash point or flammability limits for a pure organic: estimate them from simple correlations and label them**
  - When: Flash point, heat of combustion or flammability limits are missing for a pure organic compound.
  - Do: Estimate them with simple regressions on atom counts, molar mass and normal boiling point. Label the values as estimated and replace them with data later.
  - Why: The correlations use molecular data that are readily known.
  - Check: Treat the upper flammability limit with most caution, as it is the least reliable, and keep estimated and measured values apart.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.2.2, pp. 464-466 (Eqs. 1-4, Figs. 1-2). <sub>park-2022-inherently-safer-design.estimate-missing-flammability-data</sub>
- **Remove or reduce a hazard before adding protection**
  - When: A hazard is to be handled by add-on safety devices.
  - Do: Apply the four principles when choosing operations: intensify (less hazardous inventory), substitute (a safer material), attenuate (milder conditions), simplify.
  - Why: A hazard that is not there cannot be released; Park et al. 2022 call safety devices much less reliable.
  - Check: For each hazardous stream, write down which principle was tried.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 1, p. 463. <sub>park-2022-inherently-safer-design.four-principles-before-devices</sub>
- **Safety index scores are indicative only**
  - When: You present a safety index ranking.
  - Do: Report index rankings as indicative.
  - Why: Indicators and their weights are expert choices, not fitted to incidents: an analysis of 94 CSB (US Chemical Safety Board) incident reports found too much missing data to fix them.
  - Check: State the weights used next to the ranking.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.2.1, p. 464; Section 4, p. 468. <sub>park-2022-inherently-safer-design.indicators-not-yet-validated</sub>
- **Mixture flammability: treat estimates with caution**
  - When: You estimate the hazard of a process stream that is a mixture.
  - Do: Flag mixture estimates as uncertain.
  - Why: Mixture flammability does not follow the pure components proportionally, and few data exist to check it.
  - Check: Look for measured data on the actual mixture before relying on an estimate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 3.2, p. 467. <sub>park-2022-inherently-safer-design.mixture-flammability-caution</sub>
- **Rank alternatives early with a safety index built from chemical and process indicators**
  - When: You compare routes, units or streams on safety with little data.
  - Do: Build an index from chemical indicators (flammability, explosiveness, toxicity) and process indicators (pressure, temperature), all known from a simple flowsheet. Park et al. 2022 count 22 hazard-based, 33 risk-based and 18 cost-based tools.
  - Why: These indicators are available at the concept stage.
  - Check: Report the ranking as indicative: the indicators' weights are not yet verified against incident data.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.1, p. 464. <sub>park-2022-inherently-safer-design.rank-alternatives-with-indicators</sub>
- **Consider inherent safety from the first flowsheet**
  - When: You are in conceptual design, before the route and configuration are fixed.
  - Do: Screen the routes for inherent safety now.
  - Why: Once technology and configuration are fixed, changes are costly; Park et al. 2022 hold inherently safer design to be the most cost-effective risk reduction.
  - Check: Record a safety ranking next to the cost ranking of the routes.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Abstract and Section 1, p. 463. <sub>park-2022-inherently-safer-design.safety-from-first-flowsheet</sub>
- **Judge safety together with cost, sustainability and resilience**
  - When: A safety index alone is used to choose a route.
  - Do: Combine safety with life-cycle cost, sustainability and resilience, for example in one return-on-investment metric.
  - Why: Design trade-offs are made under several constraints at once.
  - Check: Show how the route ranking changes when safety is included.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Park et al. 2022, *Progress in Inherently Safer Design for Chemical…* (https://doi.org/10.3303/CET2290078), Section 2.3, p. 466; Section 3.1, p. 467. <sub>park-2022-inherently-safer-design.safety-with-cost-and-life-cycle</sub>

### purge

- **Inert in a gas recycle: the purge sets its level**
  - When: An inert builds up in a gas recycle loop.
  - Do: Size or adjust the purge to the inert concentration you want.
  - Why: Only the purge removes the inert.
  - Check: In CHEPTA, scan the purge fraction and record the inert concentration in the loop and the reactant lost with the purge.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 6, p. 230. <sub>larsson-skogestad-2000-plantwide.purge-sets-inert-level</sub>

### reactive distillation

- **Reactive distillation for butyl acetate: acid fed above butanol, catalyst in the middle, ester out at the bottom**
  - When: You design a reactive column for acetic acid and n-butanol over Amberlyst-15 with a 1:1 feed.
  - Do: Use a two-feed column with a reactive middle section. Al-Rabiah et al. 2022: 34 stages, catalyst on stages 5-24, acetic acid on stage 5 above butanol on stage 9, 100 kmol/h of each, reboiler 3.3 MW.
  - Why: Water leaves overhead as it forms and ester leaves at the bottom, so the reaction keeps moving past its equilibrium.
  - Check: The bottoms in Table 9 (97.2 kmol/h ester, 1.1 butanol) is 98.9 mol% or 99.3 mass % by Lab's arithmetic; the text says more than 99% without a basis. Catalyst hold-up per stage and the pressure profile are not printed, so expect to choose them.
  - Result: Conversion over 98%, ester as bottoms.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.2, pp. 13-15 (Table 8, Fig. 16). <sub>al-rabiah-2022.rd-column-configuration</sub>
- **Reactive distillation was the cheapest butyl acetate route, but it is harder to design and operate**
  - When: You choose between intensified butyl acetate routes.
  - Do: Prefer reactive distillation with a decanter on cost and energy, and plan for its more complex design and operation, which Al-Rabiah et al. 2022 point out.
  - Why: One unit does both the reaction and the separation.
  - Check: The costs are Al-Rabiah et al. 2022's Aspen estimates (total capital USD 6,742,000 against 7,552,000, Table 12); compare on your own cost basis.
  - Result: Steam 26,388 MWh/a, capital 6.7 million USD against 7.6 million for the membrane route, payback 2.1 years.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 1, p. 2; Section 7.1, p. 16 (Table 10); Section 8, p. 18 (Table 12). <sub>al-rabiah-2022.rd-lower-capex-and-energy</sub>
- **Butyl acetate yield can rise from about 70% to 95% when water is removed during reaction**
  - When: Butyl acetate yield is limited by equilibrium.
  - Do: Remove water during the esterification.
  - Why: Water removal shifts the equilibrium towards the ester.
  - Check: Hoff & Eisenacher 2025 report this in one sentence from a cited study with acidic ionic-liquid catalysts, not read by Lab: treat it as an indication.
  - Result: Yields from about 70% up to 95%.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Section 6.1 (citing ref. 174). <sub>hoff-eisenacher-2025-esterification-review.butyl-acetate-yield-with-water-removal</sub>
- **Acid resin catalyst: its temperature limit sets the reactive zone's temperature and pressure**
  - When: You choose an ion-exchange resin catalyst for esterification, for example in reactive distillation.
  - Do: Choose the resin by its maximum service temperature: about 140 C for Amberlyst 15 and up to 190 C for Amberlyst 70, per Hoff & Eisenacher 2025. Set the column pressure so the reactive zone stays below it.
  - Why: Resins lose their acid groups when too hot.
  - Check: In CHEPTA, check the reactive stages' temperatures against the resin's limit.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Section 2.2.1 (Table 2). <sub>hoff-eisenacher-2025-esterification-review.resin-temperature-limit</sub>
- **First design of a reactive column: reactive zone where reactants are richest, shortcut the rest**
  - When: You need a starting design for a reactive distillation column.
  - Do: Put the reactive zone where reactant concentrations are highest. Estimate the non-reactive stages with Fenske-type shortcuts (minimum-stage equations), and the reactive stages as the reactive height divided by the catalytic packing's HETP (height equivalent to a theoretical plate).
  - Why: Conventional shortcuts give the separating sections; the catalytic packing sets the reactive height.
  - Check: Simulate the first design rigorously and adjust it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal p. 1268 (p. 7 of the TU Delft copy; guidelines of Subawalla and Fair). <sub>kiss-2024-rd-conceptual-methods.first-sizing</sub>
- **Reactive column with a large heat of reaction: plan energy integration between its sections**
  - When: The reaction on the reactive stages releases or absorbs much heat.
  - Do: Integrate energy between the reactive and separating sections. For slow, strongly endothermic reactions with small equilibrium constants, also integrate mass with the stripping section. For thermally neutral reactions mass integration alone is enough.
  - Why: Heat released or absorbed on the reactive stages changes the column's vapour and liquid flows.
  - Check: In CHEPTA, compare the vapour and liquid flow profiles with and without reaction.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Synthesis procedures, journal p. 1277 (p. 16 of the TU Delft copy; procedure of Huang et al.). <sub>kiss-2024-rd-conceptual-methods.heat-effect-integration</sub>
- **Place the reactive section so distillation carries a product away**
  - When: A reactive column is limited by equilibrium, or an azeotrope can form.
  - Do: Locate the reactive section so distillation removes a reaction product from the liquid and, where azeotropes exist, so the reaction consumes a component before its azeotrope can form.
  - Why: Removing a product shifts the equilibrium; consuming a component avoids its azeotrope.
  - Check: In CHEPTA, compare conversion and stage compositions for a few positions of the reactive zone.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal p. 1270 (p. 9 of the TU Delft copy). <sub>kiss-2024-rd-conceptual-methods.locate-reactive-section</sub>
- **Reactive column feeds: run neat with tight ratio control, or with 10-20% excess and a recovery column**
  - When: You set the reactant ratio of a reactive column.
  - Do: Either run neat (stoichiometric feeds) in one column, which is cheaper but needs precise balancing of the fresh feeds, or use 10 to 20% excess of one reactant with a recovery column for it.
  - Why: Any excess reactant must leave somewhere; in neat operation a small imbalance builds up in the column.
  - Check: In CHEPTA, offset the feed ratio slightly and watch whether a reactant accumulates in the column or the recycle.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal pp. 1270 and 1278 (pp. 9 and 17 of the TU Delft copy; after Luyben and Yu). <sub>kiss-2024-rd-conceptual-methods.neat-versus-excess-feed</sub>
- **Reactive distillation only works where the reaction, catalyst and separation windows overlap**
  - When: You consider combining a reaction and its separation in one column.
  - Do: Check that the temperature and pressure windows of the reaction, the catalyst and the separation overlap. If they do not, keep reactor and column separate, and judge integration on the whole process.
  - Why: One column imposes one pressure and a temperature profile on all three.
  - Check: Compare the column's stage temperatures at the chosen pressure with the catalyst's limit and the reaction's useful range.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal p. 1268 (p. 7 of the TU Delft copy). <sub>kiss-2024-rd-conceptual-methods.overlapping-windows</sub>
- **Too much reaction asked of the column: add a pre-reactor**
  - When: The reactive column has to deliver a large share of the conversion.
  - Do: Add a pre-reactor upstream to take part of the conversion. Find the best split between them by costing designs over a range of pre-reactor temperatures.
  - Why: An upstream reactor reaches equilibrium cheaply and leaves a smaller reactive section.
  - Check: Cost several pre-reactor temperatures and keep the cheapest.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal p. 1275 (p. 14 of the TU Delft copy; after Daniel and Jobson). <sub>kiss-2024-rd-conceptual-methods.pre-reactor</sub>
- **Reaction too slow on the reactive stages: raise the column pressure**
  - When: The reaction is too slow at the reactive column's temperatures.
  - Do: Raise the column pressure so the stages run hotter and the reaction faster, as long as the separation and the catalyst still allow it.
  - Why: Pressure sets the stage temperatures.
  - Check: In CHEPTA, scan the column pressure and check the reactive-zone temperatures against the catalyst limit, and the key relative volatility.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal p. 1269 (p. 8 of the TU Delft copy). <sub>kiss-2024-rd-conceptual-methods.raise-pressure-for-slow-reaction</sub>
- **Slow reaction: no reactive distillation; very easy separation: reactor plus flash**
  - When: You choose between a reactor followed by a separator and a reactive column.
  - Do: Place the system on a rate-against-volatility chart (the Schoenmakers diagram). A slow reaction makes reactive distillation unattractive; a very high relative volatility needs only a reactor and a flash. In between, reactive distillation is a candidate.
  - Why: Reaction rate and volatility decide whether extra stages help.
  - Check: The chart's axes are not quantified and Kiss et al. 2024 warn that it needs experience: confirm the choice with a simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal pp. 1268-1269 (pp. 7-8 of the TU Delft copy, Fig. 2). <sub>kiss-2024-rd-conceptual-methods.rate-versus-volatility</sub>
- **Reactive trays hold 10-15 cm of liquid: if you need more hold-up, add trays or widen the column**
  - When: The catalyst hold-up the reaction needs exceeds what a tray can hold.
  - Do: Keep the tray liquid height near 10 to 15 cm. If the needed hold-up implies more, add reactive trays or make the column wider than vapour loading requires.
  - Why: More liquid on a tray raises the pressure drop; tray hydraulics limit the liquid height.
  - Check: Divide the required hold-up per stage by the tray area to get the liquid height.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal p. 1274 (p. 13 of the TU Delft copy; after Luyben and Yu). <sub>kiss-2024-rd-conceptual-methods.tray-liquid-height</sub>
- **Reactive column: stay away from both minimum stages and minimum reflux**
  - When: You choose the stage count and reflux of a reactive column and catalyst cost matters.
  - Do: Choose a configuration between the two limits.
  - Why: Near minimum stages the column is short and wide, near minimum reflux tall and slim. Catalyst volume follows diameter and reactive height, and is lowest in between.
  - Check: Compute the catalyst volume at a few points along the stages-reflux curve.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.2, p. 270 (Fig. 8). <sub>muthia-2018-rd-applicability.avoid-extreme-configurations</sub>
- **Slow reaction in a reactive column: size the catalyst hold-up so Da/K is at least 2 to 5**
  - When: The reaction is kinetically limited and may need more reactive stages.
  - Do: Size catalyst hold-up and residence time so the Damkohler number (reaction rate relative to flow rate) divided by the equilibrium constant is at least 2 to 5.
  - Why: With enough hold-up the reaction behaves as at equilibrium: at Da/K of 5 or more the configuration equals the equilibrium one, at 2 or more it is within 10%.
  - Check: Compute Da/K from your kinetics, hold-up and feed rate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.2, p. 270 (Fig. 7; Fig. S5). <sub>muthia-2018-rd-applicability.da-over-keq-rule</sub>
- **Small equilibrium constant: expect more reactive stages and higher reflux**
  - When: The reaction's equilibrium constant is small.
  - Do: Allow more reactive stages and a higher reflux ratio.
  - Why: The products must be removed more completely on each stage.
  - Check: Compare your stage count and reflux with the map for your equilibrium constant.
  - Result: In the base case of Muthia et al. 2018, at K = 0.01 the minimum is 22 stages and the minimum reflux ratio 11.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.1.2, p. 269 (Fig. 6). <sub>muthia-2018-rd-applicability.low-keq-more-stages-reflux</sub>
- **Light product close in volatility to a reactant: the feasible region shrinks**
  - When: The light product is hard to separate from a reactant.
  - Do: Check the product-reactant relative volatilities first.
  - Why: The reactant leaves with the product unless the separation is sharp.
  - Check: Compute the light product's relative volatility against each reactant with your property method.
  - Result: At K = 0.01, a relative volatility of 1.2 instead of 2 raised the reactive stages needed from 28 to 64.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.1.3, p. 269 (Fig. 6). <sub>muthia-2018-rd-applicability.product-reactant-volatility</sub>
- **Go or no-go on reactive distillation from three inputs: volatilities, equilibrium constant, kinetics**
  - When: You decide early whether reactive distillation is worth a rigorous study, for a reaction A + B to C + D with C the lightest and D the heaviest component.
  - Do: Read the relative volatilities, the equilibrium constant and the kinetics against the applicability maps of Muthia et al. 2018 (reflux ratio against stages) before any rigorous simulation.
  - Why: Generic maps for this reaction class show where a feasible column exists.
  - Check: The maps are about +/-30% for real systems: confirm a go with a rigorous simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 2, pp. 264-266; Conclusions, p. 274. <sub>muthia-2018-rd-applicability.rd-map-needs-three-parameters</sub>
- **Butyl acetate reactive still: butanol runs short while acid and water stay in the liquid**
  - When: Reactants deplete unevenly in the liquid of an acetic acid and butanol reaction over a resin.
  - Do: Account for the acid and water held in the catalyst when you set the feed ratio.
  - Why: Water and acetic acid are fully miscible and both bind to the resin; butanol and the ester instead form two liquid phases with water.
  - Check: Compare the liquid reactant ratio with the fed ratio in your test or simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Orjuela et al. 2006, *Constructing residue curve maps for butyl acetate…* (https://doi.org/10.15446/ing.investig.v26n3.14745), Results, p. 30 (Fig. 3). <sub>orjuela-2006-butyl-acetate-rcm.acid-water-retained-butanol-depleted</sub>
- **Find the catalyst load where the reaction reaches equilibrium: raise it until the residue curves stop moving**
  - When: You do not know whether kinetics or equilibrium governs a reactive distillation.
  - Do: Scan the catalyst load in reactive residue-curve tests and increase it until the curves no longer change.
  - Why: At high catalyst load the reaction keeps pace with vaporisation, which marks the chemical-equilibrium regime.
  - Check: Treat the found load as the lowest at which a design may assume equilibrium.
  - Result: For this resin about 8 g, near 0.8 wt% sulfuric-acid equivalent (Orjuela et al. 2006).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Orjuela et al. 2006, *Constructing residue curve maps for butyl acetate…* (https://doi.org/10.15446/ing.investig.v26n3.14745), Results, p. 33 (Fig. 4, Table 3). <sub>orjuela-2006-butyl-acetate-rcm.catalyst-load-equilibrium-regime</sub>
- **Butyl acetate reactive column: the ester can be taken pure as bottom product**
  - When: Esterification of acetic acid with 1-butanol over an acid resin stops at equilibrium in a reactor.
  - Do: Use reactive distillation with butyl acetate as the bottom product.
  - Why: Water and the other light products are removed continuously, which drives the reaction on; the ester is the heaviest component, so the residue curves run towards it.
  - Check: Orjuela et al. 2006 measured this in a laboratory batch still at 560 mmHg, not a continuous column: confirm it in a column simulation.
  - Result: Measured reactive residue curves (paths of a boiling, reacting liquid) end at butyl acetate, beyond the equilibrium conversion.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Orjuela et al. 2006, *Constructing residue curve maps for butyl acetate…* (https://doi.org/10.15446/ing.investig.v26n3.14745), Abstract, p. 26; Results, pp. 32-33 (Figs. 4-5). <sub>orjuela-2006-butyl-acetate-rcm.reactive-rcm-ester-in-bottoms</sub>
- **Ethylene oxide hydration in a reactive column: less diethylene glycol and less steam**
  - When: Ethylene oxide is hydrated to ethylene glycol, heavy glycols form when oxide meets glycol, and removing the water costs steam.
  - Do: Hydrate in a reactive distillation column, without catalyst.
  - Why: The volatile oxide stays dilute in the liquid on the reactive stages, which limits diethylene glycol, and the reaction heat helps boil off the water.
  - Check: In CHEPTA, compare the oxide concentration on the reactive stages and the diethylene glycol made with a tubular-reactor case.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Introduction, p. 3; Results, pp. 7-9. <sub>othman-2024-meg-reactive-distillation.rd-keeps-oxide-dilute</sub>
- **Reactive glycol column: feed the recycled water above the oxide**
  - When: Volatile ethylene oxide could escape overhead from the reactive column.
  - Do: Feed the recycled process water near the top (stage 2) and the aqueous oxide a little lower (stage 4).
  - Why: The water above the oxide feed catches and reacts with the rising oxide vapour before it reaches the condenser.
  - Check: In CHEPTA, check the oxide in the condenser vapour for a few feed locations.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Results, pp. 7-8 (Table 3, Fig. 10). <sub>othman-2024-meg-reactive-distillation.rd-water-fed-above-oxide</sub>

### recycle

- **After a 92% membrane reactor, one column and a small recycle are enough**
  - When: Unreacted reactants leave a butyl acetate membrane reactor at high conversion per pass.
  - Do: Use a single column that returns its distillate (about 9 kmol/h each of butanol and acid, with about 1 kmol/h each of ester and water) to the feed vessel.
  - Why: High conversion per pass leaves little to recycle.
  - Check: Compare your recycle with streams 3 and 5 of Table 4. Lab's comparison: about 9 kmol/h of each reactant per 100 kmol/h fresh feed, against about 43 in the conventional route.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 5, p. 7; Table 4, p. 9 (streams 3 and 5). <sub>al-rabiah-2022.membrane-route-single-column-recycle</sub>
- **An intermediate impurity builds up at column tops: recycle those distillates upstream, at an optimised rate**
  - When: An intermediate-boiling impurity (ethanol in the acetone-butanol-ethanol distillation of Chen et al. 2018) accumulates at the tops of downstream columns.
  - Do: Recycle those distillates to the upstream column that removes the impurity, and optimise the recycle rate.
  - Why: The impurity has no exit unless it is returned to the column that can remove it. Too little recycle lets it into the product; too much costs energy.
  - Check: In CHEPTA, scan the recycle rate and record product purity and total duty.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Chen et al. 2018, *Novel distillation process for effective and stable…* (https://doi.org/10.1186/s13068-018-1284-8), Methods: 'Recycling the distillates'; Conclusions. <sub>chen-2018-abe-distillation.recycle-distillate-against-build-up</sub>
- **Build a flowsheet in Douglas's order**
  - When: You start a new flowsheet.
  - Do: Decide batch or continuous first, then the input-output structure, the recycle structure, the separation system and finally energy integration.
  - Why: Each level fixes what the next one needs.
  - Check: Before simulating, write down the decision taken at each level.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 5, p. 227. <sub>larsson-skogestad-2000-plantwide.douglas-hierarchy</sub>
- **Luyben's rule: fix one flow in each liquid recycle loop**
  - When: Recycle flows run away in a plant with liquid recycles.
  - Do: Fix one flow in each liquid recycle loop, as Luyben recommends (reported by Larsson & Skogestad 2000).
  - Why: A fixed flow stops disturbances circulating and avoids the snowball effect.
  - Check: Larsson & Skogestad 2000 themselves dispute this: fixing the recycle flow carries an economic penalty (see their rule on keeping the reactor full).
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule under this heading disagrees with this one; both are kept.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Sections 5 and 6, pp. 228 and 230. <sub>larsson-skogestad-2000-plantwide.fix-a-recycle-flow</sub>
- **Liquid reactor in a recycle loop: keep it full rather than fixing the recycle flow**
  - When: You choose what to fix in a liquid-phase reactor-recycle loop.
  - Do: Keep the reactor hold-up at its maximum.
  - Why: Larger hold-up gives more conversion per pass and the smallest recycle; fixing the recycle flow instead costs money.
  - Check: For gas-phase loops Larsson & Skogestad 2000 note that letting the hold-up (pressure) float can be optimal.
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule under this heading disagrees with this one; both are kept.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 6, p. 230. <sub>larsson-skogestad-2000-plantwide.keep-reactor-full</sub>
- **Design from the reactor outwards**
  - When: You start a flowsheet.
  - Do: Choose the reactor and catalyst first, then add the separations and recycles.
  - Why: The reactor effluent defines the separation problem: the reaction step sets the purity reached and how hard purification will be.
  - Check: Fix the reactor outlet composition before designing the separation train.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design and simulation'. <sub>pasha-2021-biodiesel-process-design.design-from-reactor-outwards</sub>
- **Ethylene carbonate route: recycle the CO2 released in hydrolysis back to carbonation**
  - When: Carbon dioxide is a reactant in carbonation and a product of the hydrolysis that follows.
  - Do: Separate the released CO2, compress it and recycle it to carbonation, with a small make-up for losses.
  - Why: Closing the loop leaves only the losses to replace.
  - Check: In CHEPTA, check the CO2 balance of the loop: make-up equals losses.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'Indirect hydration process', p. 7; 'MEG production via indirect EO hydration process', p. 8 (Fig. 6). <sub>shehata-2024-meg-routes.carbonate-route-co2-recycle</sub>
