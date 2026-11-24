# Lessons: ethyl-acetate-piotrowski-2021 (generated; do not edit)

What the plant taught, for a process engineer: each lesson summarises several runs or decisions below, with When / Do / Why / Check / Result, what it was judged against, its status and source. A lesson that holds beyond this plant is also on its topic page. The run log follows under "Runs behind these lessons"; its rows still count as the evidence. [All topics](../rules-readable.md)

Engine names: a number such as 0.6.2 is a CHEPTA release; 415da41 is an unreleased development version of CHEPTA (a commit), later than release 0.6.2 and not yet released. Results on it are labelled separately from the release's.

## absorber column (2)

- **Acid-stripping column of 8 stages: a reflux of 55,000 to 65,000 kg/h holds 0.005 % acid overhead**
  - When: Reactor vapour is washed by the recycled ester-rich organic phase in a column without condenser or reboiler ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425): 8 stages in Table 1, R/V 0.61).
  - Do: Scan the reflux around 60,000 kg/h and allow two liquids on the stages; 55,000 kg/h meets the acid limit narrowly, 60,000 with a wide margin.
  - Why: [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) ask for at least 14 stages for the limit; with 8 the reflux must do the work.
  - Check: Read the acid in the overhead at each reflux; on chepta 0.6.2 an irregular failure that a later engine converges is the solver, not the column.
  - Result: Acid 0.0036 % at 55,000, 0.0004 % at 60,000 and 65,000 kg/h; 0.055 % at 50,000 misses. On 0.6.2 four of the 12 scan points failed, two of them at the ends of the scan (45,000 and 70,000 kg/h); on 415da41 all 12 converge, but the acid at 70,000 kg/h is not reported.
  - Judged on: Acetic acid in the azeotrope at most 0.005 wt% ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Section 3.2).
  - Summarises 5 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), pp. 6-7, Section 3.2 and the text after Figure 3; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. <!-- ethyl-acetate-piotrowski-2021.lesson-acid-stripping-reflux -->

- **Once the recycles return wetter reflux, a second liquid forms in the acid-stripping column: allow two liquids**
  - When: The column runs on the plant's own recycles instead of the published inlets, and its reflux carries more water.
  - Do: Give the column phases VLL from the start, even if it ran with one liquid on the published inlets.
  - Why: The extra water puts stage 7 inside the two-liquid region.
  - Check: Look for a phase-split message naming a stage; rerun that stage's column alone with two liquids allowed.
  - Result: chepta 0.6.1 refused it (two liquids in an absorber not built); 0.6.2 converges with two liquids on stage 7.
  - Judged on: Convergence of the column on the plant's own inlets.
  - Summarises 2 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), pp. 6-7, Section 3.2 and the text after Figure 3. <!-- ethyl-acetate-piotrowski-2021.lesson-acid-stripping-two-liquids -->

## distillation (5)

- **Without acid, give the product column its purity, not the published flow, and allow time**
  - When: The ester product column runs on an acid-free feed and the published flow misses the purity slightly.
  - Do: Specify 99.90 mass % ester in the bottoms; expect a slow solve.
  - Why: Water is what remains in the product at the published flow (0.113 %, against 0.07 % in Table A2 of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425)); a slightly smaller product sends more of it overhead. Why CHEPTA leaves more water there than Chemcad is not established.
  - Check: Compare the product flow with Table A2 and read the water in the product.
  - Result: With the published flow 99.868 % ester and 0.113 % water; with the purity given it is met at a flow 0.5 % below it, water 0.084 %, in 610 s against 12 s.
  - Judged on: Ester purity 99.90 wt% (met with the purity given, missed at the published flow). Water 0.113 % (published flow) and 0.084 % (purity given) exceed the 0.03 % limit of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Section 3.4; whether that matters depends on the product specification of the application (maintainer, 2026-11-21).
  - Summarises 3 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.1) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 9, Section 3.4, paragraph after Figure 5. <!-- ethyl-acetate-piotrowski-2021.lesson-product-column-purity-spec-no-acid -->

- **Product column with a trace of acetic acid: set the bottoms flow about 1 % below the published flow**
  - When: The ester product column gets a feed with 0.01 % acetic acid ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), stream 13), and the acid, the heaviest component, can only leave with the product.
  - Do: Give the bottoms flow as the second specification, 140 to 140.5 kmol/h instead of 141.5. On chepta 0.6.2 a purity specification returned a wrong root (a 31.0 kmol/h product); it was not tried on 415da41.
  - Why: Water is the main impurity at the published flow (0.111 %), as it is without acid (0.113 %); a smaller product sends more water overhead. The acid, which can only leave with the product, adds about 0.02 points (0.022 %).
  - Check: Read the ester purity and the acid in the bottoms; with the purity given, check the product flow is near the published one.
  - Result: 140 kmol/h 99.922 %, 140.5 kmol/h 99.897 % (99.90 at the two decimals of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425)); 141 and 141.5 kmol/h fall short (99.873 and 99.848 %). On 0.6.2 only 139 kmol/h converged.
  - Judged on: Ester purity 99.90 wt% at the two decimals of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425). Water 0.044 % (140) and 0.066 % (140.5) exceed the 0.03 % limit of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Section 3.4; whether that matters depends on the product specification of the application (maintainer, 2026-11-21).
  - Summarises 8 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@415da41) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 9, Section 3.4, paragraph after Figure 5; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 11-16. <!-- ethyl-acetate-piotrowski-2021.lesson-product-column-trace-acid -->

- **Wastewater column: raise the distillate a few per cent to strip the ethanol; the acid stays in the water**
  - When: The wash water is distilled to recover ethanol and ester, and the bottoms must be nearly free of organics.
  - Do: Raise the distillate from 394.6 to about 400-410 kmol/h; specify the bottoms purity only once the feed is nearly acid-free.
  - Why: The acid of the feed leaves in the bottoms whatever the distillate, about 0.012 %.
  - Check: Read ethanol and acid in the bottoms separately.
  - Result: Ethanol 0.151 % at 394.6, 0.014 % at 400 and 0.003 % at 410 kmol/h; the acid stays 0.012 %, so the 0.01 % organics limit cannot hold with the published feed.
  - Judged on: Ethanol in the wastewater bottoms. The organics limit of 0.01 wt% ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Section 3.5) is missed through the feed's acid; it is not met in Table A2 of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) either.
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 10, Section 3.5; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. <!-- ethyl-acetate-piotrowski-2021.lesson-wastewater-column -->

- **Ester purity short in the closed plant: not solved; the excess ethanol and the azeotrope's water load are the leads**
  - When: The closed plant settles but its ester product stays below 99.90 % while the column alone meets it.
  - Do: Lab tried trimming the excess ethanol feed, cooling the extraction to the cooling-water limit, more wash water and more distillate; none reached 99.90 %. Balance the ethanol and the water first.
  - Why: Lab's reading, a lead: excess ethanol can only leave with the product, so it builds up and wets the raffinate; the column's distillate leaves at the water azeotrope, so its flow sets how much water it can carry.
  - Check: Balance the excess reactant around the plant and the water around the product column before tuning the column; compare stage counts only on a settled plant.
  - Result: Best settled 99.666 % (extractor 20 C, ethanol feed 6,506 kg/h). W/A 1.13 99.118 %, no gain; feed stage 5 98.915 %; distillate 246 kmol/h 99.137 %, 260-280 failed on 0.6.2, 270 on 415da41 99.223 %. Stages only at the unsettled 3e-4: 36 and 38 gave 99.675 and 99.680 % against 99.672 %, 40 failed.
  - Judged on: Ester purity 99.90 wt% (not reached). Water in the product stays above the 0.03 % limit of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Section 3.4 in every run.
  - Summarises 10 rows of the run log below.
  - Status: failed — Lab's CHEPTA run (chepta@0.6.2) did not converge or missed its target.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 9, Section 3.4, paragraph after Figure 5; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 8, Section 3.3, last paragraph. <!-- ethyl-acetate-piotrowski-2021.lesson-purity-set-by-ethanol-and-water -->

- **Check that the published stream table meets its own limits before chasing them in the simulation**
  - When: A product limit is missed in CHEPTA and [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) claims to meet it.
  - Do: Balance the key impurity around the published column from its stream table first.
  - Why: In [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) the product column's distillate leaves at the water azeotrope, so the table itself leaves 0.07 % water against a 0.03 % limit, and all the feed's acid must reach the product (0.022 %, not the 0.01 % printed).
  - Check: Compare the published stream table with the text's claims and keep any disagreement.
  - Result: Two limits of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) are not met by its own Table A2 (product water; wastewater organics); a third is not decidable at two decimals (acid in the azeotrope, 0.01 % printed against 0.005 %).
  - Judged on: Whether the limits of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) can be met at its own settings; a reading of its tables, not a run.
  - Summarises 4 rows of the run log below.
  - Status: lead — a suggestion, not yet tested.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 11-16; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 9, Section 3.4, paragraph after Figure 5. <!-- ethyl-acetate-piotrowski-2021.lesson-audit-paper-column-balance -->

## extraction (2)

- **Extractor's mixed feed: an adiabatic mixer ran alone on chepta 0.6.2 but left too much vapour in the plant; keep it saturated liquid**
  - When: Hot distillate and the cooled azeotrope are mixed just before a liquid-liquid extractor.
  - Do: Give the mixer a saturated-liquid outlet (a small duty) and record the added heat.
  - Why: Mixing streams of different temperatures leaves a few per cent of vapour, and an extractor holds two liquids and no vapour.
  - Check: Read the mixer outlet's vapour fraction; in the loop it can grow.
  - Result: 0.6.1 refused 0.037 vapour fraction, and its saturated-liquid workaround (1 kW) ran; 0.6.2 accepted the adiabatic mixer alone, but in the open plant variant it reached 17 % vapour and was refused; the settled closed plant runs with the saturated-liquid mixer.
  - Judged on: The extractor accepting its feed. The run of the adiabatic mixer alone did not test the saturated-liquid mixer; the settled closed plant did.
  - Summarises 3 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 8, Section 3.3, last paragraph. <!-- ethyl-acetate-piotrowski-2021.lesson-extractor-feed-saturated -->

- **Water wash without a printed stage count: use two isothermal equilibrium stages at the outlet temperature**
  - When: [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) give the extractor's temperature (70 C) and water ratio but no stage count, and at 70 C the feed is mostly vapour in CHEPTA.
  - Do: Run countercurrent equilibrium stages at the outlet temperature (27 C) and choose the stage count that matches the raffinate's ethanol; say that this number is calibrated.
  - Why: At the published 70 C the feed is 78 % vapour and the extractor refuses it; the outlets are cooler.
  - Check: Compare the raffinate flow and water with Table A2, not the ethanol you calibrated on.
  - Result: Two stages: 1.87 against 1.86 mass % ethanol (calibrated); raffinate +2.6 % (0.6.1, no acid) and +3.3 %, water 4.85 against 4.70 % (0.6.2, with acid).
  - Judged on: The raffinate of Table A2 (stream 11); its ethanol is calibrated, its flow and water are compared.
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. <!-- ethyl-acetate-piotrowski-2021.lesson-extractor-isothermal-stages -->

## heat exchange (2)

- **Keep the trace of acetic acid in every two-liquid unit; do not drop it to make the flash converge**
  - When: Every washed stream holds about 0.01 % acetic acid and two liquids.
  - Do: Run the heaters, extractor and columns with the acid and two liquids together (chepta 0.6.2 or later).
  - Why: The acid's vapour dimerizes, and older releases could not combine that with a three-phase flash; dropping the acid hides where it ends up.
  - Check: Compare each duty with Table 1 of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), whose HTXR 18 and 19 duties are swapped (maintainer, 2026-11-12), and follow where the acid leaves.
  - Result: 0.6.1 refused every such stream, so Lab's 0.6.1 results drop the acid after column 5; 0.6.2 runs them. One heater still takes 3.3 times its printed duty because the mixture boils below 71 C.
  - Judged on: Running each unit with the acid present; duties compared with Table 1.
  - Summarises 3 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 5, Section 2.1. <!-- ethyl-acetate-piotrowski-2021.lesson-acid-with-two-liquids -->

- **Pure acetic acid fed below its triple point: expect extrapolated acid data and a heater duty a few per cent high**
  - When: A feed of pure acetic acid is printed at 15 C ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Table A2), below the acid's triple point of 289.81 K in CHEPTA's record.
  - Do: On chepta 0.6.2 run it as printed and read the extrapolations CHEPTA lists; on 0.6.1, which refuses it, start the feed at 18 C.
  - Why: The acid's liquid heat capacity, vapour pressure and heat of vaporization are continued below their measured range.
  - Check: Compare the feed heater duty with Table 1 and keep the extrapolation list with the run.
  - Result: 0.6.2: 573.9 kW against 535.6 kW (+7.2 %); 0.6.1 from 18 C: 543.9 kW (+1.6 %).
  - Judged on: Running the printed feed at all; the heater duty of Table 1 (535.6 kW) is a comparison, not a target.
  - Summarises 2 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 4, Section 2, first paragraph. <!-- ethyl-acetate-piotrowski-2021.lesson-cold-acid-feed -->

## reactor evaporator (1)

- **Reactor-evaporator without a usable rate law: impose the conversion per pass from the streams; it does not set the product**
  - When: The kinetics of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) cannot be reused (catalyst concentration and concentration units are missing) and the reactor boils off its products as they form.
  - Do: Model it as a conversion reactor with an all-vapour outlet, taking the acid conversion per pass from the inlet and outlet streams of [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) (Table A2, streams 5 and 6: 0.7703).
  - Why: The unreacted acid returns from the next column until it is used up, so the conversion per pass changes only the size of that recycle.
  - Check: Compare the outlet temperature and duty with [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) (Lab on chepta 0.6.1: 89.0 C against 90 C, duty +6.3 %), then vary the conversion per pass in the closed plant.
  - Result: Conversion per pass 0.80 and 0.74 gave 99.112 and 99.113 % ester against 99.109 %: the product does not move.
  - Judged on: The product purity of the closed plant, unchanged by the conversion per pass; the reactor is not predicted.
  - Summarises 3 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 4, Section 2, first paragraph; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. <!-- ethyl-acetate-piotrowski-2021.lesson-reactor-conversion-imposed -->

## recycle (4)

- **Close the ester plant on outlet purities, not on the published column settings**
  - When: The whole plant with all five recycles does not converge with the column specifications printed in [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425).
  - Do: Give the wastewater column its bottoms purity (99.99 % water), the product column its distillate flow, and fix one flow inside the water recycle; let the wastewater follow.
  - Why: With the published settings the plant is over-specified (141.5 kmol/h of product against 141.07 kmol/h of ester the feeds form), and on chepta 0.6.2 column 5 failed; purities keep each column on its target as the recycles move.
  - Check: Count the plant's free variables, then compare every stream with Table A2 and look for blown-up flows.
  - Result: With the published specifications every closed variant failed: 9 on 0.6.2, all in column 5; 9 on 415da41, two at the reactor short of ethanol, two in column 11, the rest slow or in a wrong phase. With the purity specifications the plant settled, every stream within -1.2 to +6.5 % of Table A2, wastewater 19,919 kg/h by itself.
  - Judged on: A closed, settled plant with balances closed; the product purity is judged in the lesson on short product purity in the closed plant.
  - Summarises 8 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 23-25. <!-- ethyl-acetate-piotrowski-2021.lesson-close-plant-purity-specs -->

- **Hold an excess reactant with no exit by a design specification on its feed, aimed at its limit in the product**
  - When: An excess reactant can leave only with the product, and trimming its feed by hand in steps of a few kg/h fails to converge.
  - Do: Let a design specification vary that feed for the reactant's limit in the product (here 0.04 % ethanol), starting from a settled answer.
  - Why: The design specification finds the feed that hand steps only bracketed; aiming it at the purity instead ran out of time.
  - Check: Read the feed found, the solves and the time; then raise the next limiting setting by hand.
  - Result: Ethanol feed 6,506.23 kg/h found in 8 solves and 108 min, 0.040 % ethanol; product 99.473 %, then 99.561 % with the distillate raised to 260 kmol/h; 99.90 % as the target ran out of time after 3 h.
  - Judged on: Ethanol in the product at most 0.04 wt% ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Section 3.4): met. The ester purity of 99.90 wt% is not met (99.473 %).
  - Summarises 5 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@415da41) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 9, Section 3.4, paragraph after Figure 5. <!-- ethyl-acetate-piotrowski-2021.lesson-hold-excess-reactant-by-design-spec -->

- **Never fix a product flow above what the fresh feeds can form, nor every outlet of a closed plant**
  - When: A printed product flow or two round outlet flows are taken as specifications of a recycle plant.
  - Do: Fix one flow inside the recycle and let one outlet follow; check that a fixed product flow is below the product the feeds can form.
  - Why: 141.5 kmol/h of product exceeds the 141.07 kmol/h of ester the feeds form, so the reactor starves; with the feeds and both outlets fixed the product flow is set by the balance and the column cannot also hold its purity.
  - Check: Before running, compare each fixed flow with the feeds and the stoichiometry.
  - Result: With 141.5 kmol/h the loop stopped (reactor short of ethanol); with recycle 23 fixed the plant settled and the wastewater found 19,919 kg/h by itself.
  - Judged on: A closed plant that converges; the product purity is judged in the lesson on short product purity in the closed plant.
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 23-25; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 11-16. <!-- ethyl-acetate-piotrowski-2021.lesson-product-flow-within-feed -->

- **Tighten the tolerance from a saved answer; a loose one showed 99.673 % where the settled plant gives 99.109 %**
  - When: A recycle plant converges only at a loose tear tolerance such as 3e-4.
  - Do: Save the converged tear streams, restart from them at 1e-4 and then 1e-5, and compare each component's inventory in the recycles between the two answers.
  - Why: A component with no exit but the products (here the excess ethanol) can still be building up while the plant balance already closes to 0.02 %.
  - Check: Compare the recycle flows of the loose and the tight answer; a balance check alone did not show it.
  - Result: Product 99.673 % at 3e-4 against 99.109 % settled at 1e-5; the ethanol in the reactor feed rose from 14,629 to 17,455 kg/h. A run at 5e-4 had a 42 kg/h balance gap.
  - Judged on: A settled steady state (tear change and balance at a tight tolerance), not the product purity.
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 23-25. <!-- ethyl-acetate-piotrowski-2021.lesson-tighten-tolerance-from-saved-answer -->

## Runs behind these lessons

One line per decision or CHEPTA run, grouped by unit, best-supported first; the row id is in an HTML comment for `kb.py show`. A struck-through line was corrected by a later row and no longer counts; the correcting row gives its reason.

### absorber column (7)

- **Column 5 alone, 8 equilibrium stages, reflux 27 on stage 1, vapour 6 on stage 8, the paper's inlets. Expected: Azeotrope overhead within the acid limit.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, paper inlets, eight stages, one liquid. <!-- ethyl-acetate-piotrowski-2021.col5-paper-inlets-061 -->
- **All 12 iso-scds5 requests of 0.6.2 (reflux 45,000-70,000 kg/h, paper's and round-2 vapour) sent again unchanged. Expected: Convergence across the scan.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, reflux scan 45000 to 70000 kg h, paper and round 2 vapour. Correction: Review item 6, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row said all 12 iso-scds5 runs converge but listed 4. <!-- ethyl-acetate-piotrowski-2021.col5-reflux-scan-415da41-c1; corrects ethyl-acetate-piotrowski-2021.col5-reflux-scan-415da41 -->
- **Column 5 alone, paper's vapour 6, reflux 27 at 55,000, 60,000 and 65,000 kg/h, phases VLL. Expected: Acid in the azeotrope below 0.005 wt%.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, paper vapour 6, reflux 55000 to 65000 kg h. Correction: Review item 6, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row cited the 50,000 kg/h result (0.055 %, misses the limit) without its run id. <!-- ethyl-acetate-piotrowski-2021.col5-reflux-scan-meets-limit-062-c1; corrects ethyl-acetate-piotrowski-2021.col5-reflux-scan-meets-limit-062 -->
- **The 0.6.1 request sent again unchanged (phases VLL). Expected: Column converges with two liquids on stage 7.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, round 2 plant inlets, second liquid on stage 7. <!-- ethyl-acetate-piotrowski-2021.col5-round2-inlets-two-liquids-062 -->
- **Strip the unreacted acid from the reactor vapour with washed ester as reflux**
  - When: Reactor vapour carries acetic acid that must stay out of the ester azeotrope.
  - Do: Use a column without condenser or reboiler: reactor vapour at the bottom, the recycled ester-rich organic phase as reflux on stage 1 ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425): 8 stages, R/V 0.61).
  - Why: The acid goes down with the liquid back to the reactor; the azeotrope goes up.
  - Check: Acid in the azeotrope at most 0.005 wt%; [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) ask for at least 14 stages for that in the text but give 8 in Table 1.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), pp. 6-7, Section 3.2 and the text after Figure 3; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 3, Section 1.2, purification stage (1); Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. <!-- ethyl-acetate-piotrowski-2021.paper-azeotropic-column-acid-stripping -->
- **Column 5 alone at 45,000 and 70,000 kg/h of reflux (paper's vapour), 45,000 and 55,000 kg/h (CHEPTA's round-2 vapour). Expected: Convergence across the scan.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, reflux 45000 or 70000 kg h or round 2 vapour 55000. <!-- ethyl-acetate-piotrowski-2021.col5-reflux-scan-irregular-062 -->
- **Column 5 alone with CHEPTA's round-2 inlets, phases VL then VLL. Expected: Column converges with two liquids on stage 7.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3. When: unit alone, round 2 plant inlets, second liquid on stage 7. <!-- ethyl-acetate-piotrowski-2021.col5-round2-inlets-two-liquids-061 -->
- ~~**The same four requests. Expected: Convergence across the scan.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3.~~ When: unit alone, reflux 45000 or 70000 kg h or round 2 vapour 55000. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.col5-reflux-scan-415da41; corrected by ethyl-acetate-piotrowski-2021.col5-reflux-scan-415da41-c1 -->
- ~~**Column 5 alone, paper's vapour 6, reflux 27 at 55,000, 60,000 and 65,000 kg/h, phases VLL. Expected: Acid in the azeotrope below 0.005 wt%.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, pp. 6-7, Section 3.2 and the text after Figure 3.~~ When: unit alone, paper vapour 6, reflux 55000 to 65000 kg h. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.col5-reflux-scan-meets-limit-062; corrected by ethyl-acetate-piotrowski-2021.col5-reflux-scan-meets-limit-062-c1 -->

### azeotropic distillation (1)

- **Recycle the ester-rich organic phase to carry the reaction water overhead**
  - When: The reaction releases more water than the ternary azeotrope can carry.
  - Do: Return part of the extractor's organic phase to the acid-stripping column as its reflux.
  - Why: The organic phase is richer in ester than the azeotrope (>93 %), so it binds the excess water ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425): about 17 % water released against about 7.8 % in the azeotrope by the literature they cite, 8.2 % in their own Section 3.2).
  - Check: Watch the water in the reactor: it must not accumulate.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 3, Section 1.2, purification stage (1). Passage reread on 2026-11-24: Piotrowski & Kubica 2021, p. 3 (about 7.8 % water, citing their refs 8 and 29) and Section 3.2 (the azeotrope with 8.2 % water). <!-- ethyl-acetate-piotrowski-2021.paper-organic-phase-as-azeotropic-agent -->

### distillation (22)

- **Column 11 alone, bottoms 140.5 kmol/h (paper 141.5). Expected: 99.90 wt% ester.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140.5 kmol h, uniquac vll. <!-- ethyl-acetate-piotrowski-2021.col11-acid-flow-140.5-415da41 -->
- **Column 11 alone, paper's stream 13 with 0.01 % acid, bottoms 140 kmol/h (the 0.6.2 request sent again unchanged). Expected: Convergence; ester as bottoms.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 kmol h, uniquac vll. Correction: Review problem 5, dataset/reviews/backfill-corrections-review.md (PR #32, AI full check 2026-11-20): a worked row read as a success under the failure symptom no-convergence in kb.py query; the symptom is dropped. Limits unchanged (the water-limit question is with the maintainer). <!-- ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41-converges-140-c1; corrects ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41-converges-140 -->
- **Column 11 alone on the paper's stream 13 without acid, product purity 99.90 wt%. Expected: 99.90 wt% ester at a product flow near the paper's.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, no acetic acid, purity 99.9 specified. <!-- ethyl-acetate-piotrowski-2021.col11-no-acid-purity-spec-061 -->
- **Column 15 alone, distillate 400 and 410 kmol/h (+1.4 to +3.9 %). Expected: Ethanol in the bottoms near zero.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, distillate 400 to 410 kmol h. <!-- ethyl-acetate-piotrowski-2021.col15-distillate-400-410-062 -->
- **Distil the wash water to recover ethanol and ester and return them to the reactor**
  - When: The extractor's water phase holds ethanol and ester.
  - Do: Distil it (18 stages, feed 9, R/D 2 in [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Table 1), return the distillate to the reactor and split the bottoms into wash water and wastewater.
  - Why: Recovers the raw materials and keeps organics out of the wastewater.
  - Check: Organics in the wastewater below 0.01 wt% ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425)); their own table prints 0.03 %.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 10, Section 3.5; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. <!-- ethyl-acetate-piotrowski-2021.paper-wastewater-column -->
- **Product column 11 run alone on the paper's stream 13 with 0.01 mass % acetic acid, bottoms flow specified at 139 kmol/h. Expected: Ethyl acetate as the bottoms, meeting the paper's product purity.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 2.1, property-method justification. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 139 kmol h, uniquac vll. <!-- ethyl-acetate-piotrowski-2021.product-column-acid-below-paper-flow -->
- **Column 11 alone, paper's stream 13 with 0.01 % acid, bottoms 141 and 141.5 kmol/h (the paper's flow). Expected: Convergence; ester as bottoms.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 141 to 141.5 kmol h, uniquac vll. Correction: Review item 3, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row was worked with the 99.9 % objective, but at 141 and 141.5 kmol/h the purity is 99.873 % and 99.848 %. Split into this row and -converges-140. <!-- ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41-purity-short-141-141.5; corrects ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41 -->
- **Column 11 alone, paper's stream 13 with acid, product purity 99.90 wt%. Expected: Product near 141.5 kmol/h.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, purity 99.9 specified. <!-- ethyl-acetate-piotrowski-2021.col11-acid-purity-spec-062 -->
- **Settled closed plant, distillate 260, 270, 280 kmol/h. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 260 to 280 kmol h. <!-- ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-062 -->
- **Settled closed plant, column 11 distillate 260 kmol/h (the 0.6.2 request sent again unchanged). Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 260 kmol h. Correction: Review item 11, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row's symptom was purity-short, but only 270 kmol/h converged short of the purity; 260 ended OUT_OF_TIME and 280 NO_CONVERGENCE. Split by run. <!-- ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41-dist260; corrects ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41 -->
- **Settled closed plant, column 11 distillate 270 kmol/h (the 0.6.2 request sent again unchanged). Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 270 kmol h. Correction: Review item 11, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row's symptom was purity-short, but only 270 kmol/h converged short of the purity; 260 ended OUT_OF_TIME and 280 NO_CONVERGENCE. Split by run. <!-- ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41-dist270; corrects ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41 -->
- **Settled closed plant, column 11 distillate 280 kmol/h (the 0.6.2 request sent again unchanged). Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 280 kmol h. Correction: Review item 11, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row's symptom was purity-short, but only 270 kmol/h converged short of the purity; 260 ended OUT_OF_TIME and 280 NO_CONVERGENCE. Split by run. <!-- ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41-dist280; corrects ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41 -->
- **Settled closed plant, distillate 246 kmol/h. Expected: Less water in the product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 distillate 246 kmol h. <!-- ethyl-acetate-piotrowski-2021.col11-distillate-raised-settled-062 -->
- **Settled closed plant, feed stage 5. Expected: Higher purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, column 11 feed stage 5. <!-- ethyl-acetate-piotrowski-2021.col11-feed-stage-5-062 -->
- **Closed plant from the saved start, tolerance 3e-4, 36, 38, 40 stages. Expected: Higher purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant saved start, column 11 36 to 40 stages. Correction: Review item 12, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the '+0.01 point' is measured from the unsettled 99.672 % answer at tolerance 3e-4, not from the settled 99.109 %. <!-- ethyl-acetate-piotrowski-2021.col11-more-stages-062-c1; corrects ethyl-acetate-piotrowski-2021.col11-more-stages-062 -->
- **Column 11 alone on the paper's stream 13 without acid. Expected: 99.90 wt% ester.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5; Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: standalone product column, paper stream 13 feed, no acetic acid, bottoms flow 141.5 kmol h. <!-- ethyl-acetate-piotrowski-2021.col11-no-acid-paper-flow-061 -->
- **Column 15 alone, paper's feed 28, R/D 2, distillate 394.6 kmol/h. Expected: Bottoms below 0.01 wt% organics.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, distillate 394.6 kmol h. <!-- ethyl-acetate-piotrowski-2021.col15-paper-distillate-062 -->
- **Column 15 alone with the paper's feed and acid. Expected: A converged column at the purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 10, Section 3.5. When: unit alone, paper feed 28, bottoms water 99.99 specified. <!-- ethyl-acetate-piotrowski-2021.col15-purity-spec-062 -->
- **Distillate 250 and 260 kmol/h, with and without the ethanol design specification. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant ethanol feed 6506.23, column 11 distillate 250 to 260 kmol h. Correction: Review problem 3, dataset/reviews/backfill-corrections-review.md (PR #32, AI full check 2026-11-20): the c1 row cited 99.666 % without its run id; the run plant62-settled-extr20C-ethanol6506 (415da41 folder; the 0.6.2 copy is identical) is added to run_ids. <!-- ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41-c2; corrects ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41-c1 -->
- **From the design-specification answer. Expected: Purer product.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: closed plant ethanol feed 6506.23, column 11 distillate 270 kmol h. <!-- ethyl-acetate-piotrowski-2021.ds-start-distillate-270-415da41 -->
- **Product column 11 run alone on the paper's stream 13 with 0.01 mass % acetic acid, bottoms flow specified at 140, 141 and 141.5 kmol/h. Expected: Ethyl acetate as the bottoms, meeting the paper's product purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, Section 3.4, paragraph after Figure 6; Piotrowski & Kubica 2021, Section 2.1, property-method justification. When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 to 141.5 kmol h, uniquac vll. <!-- ethyl-acetate-piotrowski-2021.product-column-acid-at-paper-flow -->
- **A reading of Table A2 and Section 3.4 by Lab; confirmed as a table error for the acid by the maintainer (spot check, 2026-11-13). Expected: A future case should not take the paper's 99.90 % as reachable at its own settings.** lead, Lab's reasoning; Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: piotrowski 2021 plant s2, paper column 11 water balance. <!-- ethyl-acetate-piotrowski-2021.open-paper-col11-water-balance -->
- ~~**Column 11 alone, paper's stream 13 with 0.01 % acid, bottoms 140, 141 and 141.5 kmol/h. Expected: Convergence; ester as bottoms.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5.~~ When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 to 141.5 kmol h, uniquac vll. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41; corrected by ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41-converges-140, ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41-purity-short-141-141.5 -->
- ~~**Column 11 alone, paper's stream 13 with 0.01 % acid, bottoms 140 kmol/h (the 0.6.2 request sent again unchanged). Expected: Convergence; ester as bottoms.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5.~~ When: standalone product column, paper stream 13 feed, acetic acid 0.01 mass pct, bottoms flow 140 kmol h, uniquac vll. Correction: Review item 3, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row was worked with the 99.9 % objective, but only its 140 kmol/h run meets it; 141 and 141.5 kmol/h fall short (99.873 %, 99.848 %). Split into this row and -purity-short-141-141.5. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41-converges-140; corrected by ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41-converges-140-c1; corrects ethyl-acetate-piotrowski-2021.col11-acid-paper-flow-415da41 -->
- ~~**Settled closed plant, distillate 260, 270, 280 kmol/h. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5.~~ When: closed plant settled, column 11 distillate 260 to 280 kmol h. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41; corrected by ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41-dist260, ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41-dist270, ethyl-acetate-piotrowski-2021.col11-distillate-260-280-settled-415da41-dist280 -->
- ~~**Closed plant from the saved start, tolerance 3e-4, 36, 38, 40 stages. Expected: Higher purity.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5.~~ When: closed plant saved start, column 11 36 to 40 stages. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.col11-more-stages-062; corrected by ethyl-acetate-piotrowski-2021.col11-more-stages-062-c1 -->
- ~~**Distillate 250 and 260 kmol/h, with and without the ethanol design specification. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5.~~ When: closed plant ethanol feed 6506.23, column 11 distillate 250 to 260 kmol h. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41; corrected by ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41-c1 -->
- ~~**Distillate 250 and 260 kmol/h, with and without the ethanol design specification. Expected: Product near 99.9 %.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5.~~ When: closed plant ethanol feed 6506.23, column 11 distillate 250 to 260 kmol h. Correction: Review item 1, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row called 99.561 % the best closed answer; the settled run plant62-settled-extr20C-ethanol6506 gives 99.666 %. The error came from the case README line 121 ('best closed-plant answer on main'), which is sha256-bound in the study record and is left unchanged. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41-c1; corrected by ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41-c2; corrects ethyl-acetate-piotrowski-2021.ds-start-distillate-250-260-415da41 -->

### extraction (10)

- **EXTR 8 with 1-8 stages at 27 C, W/A 1, without acetic acid; 2 stages chosen. Expected: The raffinate of Table A2 (stream 11).** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph. When: unit alone, paper inlets, two equilibrium stages, isothermal 27 c, no acetic acid. <!-- ethyl-acetate-piotrowski-2021.extractor-two-stages-27c-061 -->
- **EXTR 8, 2 stages, 27 C, the paper's inlets with acid. Expected: The raffinate of Table A2.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, two equilibrium stages, isothermal 27 c. <!-- ethyl-acetate-piotrowski-2021.extractor-with-acid-062 -->
- **The 0.6.1 request sent again unchanged. Expected: Extractor accepts its feed.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: section b, mix 7 adiabatic. <!-- ethyl-acetate-piotrowski-2021.mixer-before-extractor-adiabatic-062 -->
- **Wash the azeotrope with 1 to 2 kg of water per kg**
  - When: Ethanol must be removed from the ester-ethanol-water azeotrope before the product column.
  - Do: Wash with a water-to-azeotrope mass ratio between 1 and 2 ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) use 1 in Table 1). Their improved strategy S1 cools to 20-30 C (Section 3.3); strategy S2, reproduced here, extracts at 70 C (Table 1).
  - Why: More water enriches the organic phase in ester but loses ester and makes more wastewater to distil.
  - Check: Compare the raffinate's ester and water with the product column's needs.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. Passage reread on 2026-11-24: Piotrowski & Kubica 2021, Section 3.3 (20-30 C, W/A 1-2) and Table 1 (EXTR 8 at 70 C in strategy S2, at 30 C in S1). <!-- ethyl-acetate-piotrowski-2021.paper-wash-ratio-1-to-2 -->
- **Settled closed plant, extractor at 20 C (Lab's 27 C). Expected: Drier raffinate.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, extractor 20 c. <!-- ethyl-acetate-piotrowski-2021.extractor-20c-062 -->
- **Settled closed plant, 3 and 4 extractor stages. Expected: Drier raffinate.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: closed plant settled, extractor 3 or 4 stages. <!-- ethyl-acetate-piotrowski-2021.extractor-more-stages-062 -->
- **EXTR 8 at 70 C with the paper's feed, and with a liquid feed. Expected: Two liquid outlets.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: unit alone, paper temperature 70 c. <!-- ethyl-acetate-piotrowski-2021.extractor-paper-70c-061 -->
- **Section B with MIX 7 adiabatic. Expected: Extractor accepts its feed.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 3, Section 1.2, first paragraph. When: section b, mix 7 adiabatic. <!-- ethyl-acetate-piotrowski-2021.mixer-before-extractor-adiabatic-061 -->
- **Settled closed plant, recycle 23 = 121,000 kg/h (W/A 1.13) and 144,000 kg/h (1.4); also with feed stage 5. Expected: Drier raffinate, purer product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, recycle 23 raised wa 1.13 to 1.4. <!-- ethyl-acetate-piotrowski-2021.wash-water-raised-062 -->
- **Not run: needs a column flow as a design-specification variable (request 16) and convergence of column 11/15 at higher loads (requests 13, 19). Expected: 99.90 % ester with water below 0.03 %.** untested, Lab's reasoning; Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5; Piotrowski & Kubica 2021, p. 8, Section 3.3, last paragraph. When: closed plant, drier raffinate and more distillate. <!-- ethyl-acetate-piotrowski-2021.open-reach-99.9-pct -->

### heat exchange (4)

- **The 0.6.1 requests sent again unchanged. Expected: The heater duty of Table 1 (535.6 kW).** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: feeds at 15 c, pure acetic acid below triple point. <!-- ethyl-acetate-piotrowski-2021.acid-feed-15c-062 -->
- **The 0.6.1 requests sent again unchanged. Expected: Duties and outlets of Table 1 and Table A2.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, acetic acid 0.01 mass pct. <!-- ethyl-acetate-piotrowski-2021.acid-two-liquids-units-062 -->
- **Feeds 1 and 2 at 15 C (Table A2), also 17 C after mixing. Expected: The heater duty of Table 1 (535.6 kW).** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: feeds at 15 c, pure acetic acid below triple point. <!-- ethyl-acetate-piotrowski-2021.acid-feed-15c-061 -->
- **Heaters 10, 12, 18, 19 and the extractor with the paper's inlets including the acid. Expected: Duties and outlets of Table 1 and Table A2.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 5, Section 2.1. When: unit alone, paper inlets, acetic acid 0.01 mass pct. <!-- ethyl-acetate-piotrowski-2021.acid-two-liquids-units-061 -->

### purge (2)

- **Close the wash-water loop with one wastewater purge and a fresh-water make-up**
  - When: Wash water circulates between the extractor and the wastewater column.
  - Do: Recycle most of the bottoms (95,797 kg/h in [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425)), purge 20,000 kg/h as wastewater and add fresh water.
  - Why: Water formed by the reaction and the make-up need one exit.
  - Check: Lab's reading: the round 20,000 kg/h is a specification and the fresh water closes the balance; [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425) do not say so.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 23-25. <!-- ethyl-acetate-piotrowski-2021.paper-water-loop-round-flows -->
- **Variant W: splitter 16 fixes 25 = 20,000 kg/h, tolerance 5e-4. Expected: Closed plant with the paper's wastewater.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, wastewater 25 fixed 20000 kg h, feeds fixed, tear tolerance 5e 4. Correction: Review item 5, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row was worked at tolerance 5e-4 with a 42 kg/h balance gap, while the sibling at 3e-4 is failed because a loose answer had not settled; the same standard applies here. <!-- ethyl-acetate-piotrowski-2021.plant-variant-w-both-round-flows-062-c1; corrects ethyl-acetate-piotrowski-2021.plant-variant-w-both-round-flows-062 -->
- ~~**Variant W: splitter 16 fixes 25 = 20,000 kg/h, tolerance 5e-4. Expected: Closed plant with the paper's wastewater.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25.~~ When: closed plant, wastewater 25 fixed 20000 kg h, feeds fixed, tear tolerance 5e 4. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.plant-variant-w-both-round-flows-062; corrected by ethyl-acetate-piotrowski-2021.plant-variant-w-both-round-flows-062-c1 -->

### reactor evaporator (3)

- **Reversible esterification: boil the products off in a reactor-evaporator and recycle the acid**
  - When: Ethanol and acetic acid react to an equilibrium-limited ester near 90 C at atmospheric pressure.
  - Do: React in a boiling reactor-evaporator (85-90 C, 300 m3 in [Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Table 1) so the products leave as vapour; return the acid-rich bottoms of the next column.
  - Why: Taking the products out as they form shifts the equilibrium; the acid is recycled until it is used up.
  - Check: Lab modelled it as a conversion reactor with an all-vapour outlet; see the lesson on the reactor-evaporator without a usable rate law.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 4, Section 2, first paragraph; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 11, Table 1. <!-- ethyl-acetate-piotrowski-2021.paper-reactor-evaporator -->
- **Conversion of acetic acid per pass 0.7703 = 1 - 4.74/20.64 (Table A2 streams 5 and 6), saturated-vapour outlet, the paper's inlet stream 5. Expected: The paper's reactor outlet and duty, without predicting the reaction.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph; Piotrowski & Kubica 2021, p. 11, Table 1. When: conversion imposed 0.7703, all vapour outlet, paper inlet stream 5. <!-- ethyl-acetate-piotrowski-2021.reactor-conversion-imposed-061 -->
- **Closed settled plant with the conversion per pass 0.80 and 0.74 (paper's streams: 0.7703). Expected: Product unchanged if the reactor is not the limit.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 4, Section 2, first paragraph. When: closed plant settled, conversion per pass 0.74 to 0.80. <!-- ethyl-acetate-piotrowski-2021.reactor-conversion-per-pass-sensitivity-062 -->

### recycle (15)

- **Settled start, F1 bracketed 6,503.5-6,507.5 kg/h. Expected: Ethanol limit met.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, design spec ethanol feed for 0.04 pct ethanol. <!-- ethyl-acetate-piotrowski-2021.design-spec-ethanol-feed-415da41 -->
- **Plant once through (round 1), splitters by fractions. Expected: Streams near Table A2.** worked, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: two sections coupled by script, once through, acid dropped downstream of column 5. <!-- ethyl-acetate-piotrowski-2021.plant-once-through-061 -->
- **Same specifications, saved starting values (init-closed-plant-chepta-0.6.2-settled.json). Expected: A settled closed plant.** worked, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, saved start tolerance 1e 5. <!-- ethyl-acetate-piotrowski-2021.plant-purity-specs-settled-062 -->
- **Settled plant; also the cold start at the default tolerance. Expected: Same answer.** worked, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, saved start tolerance 1e 5. <!-- ethyl-acetate-piotrowski-2021.plant-settled-415da41 -->
- **Settled start, with and without F1 as a second variable. Expected: 99.90 % ester.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, design spec varies column 11 distillate. <!-- ethyl-acetate-piotrowski-2021.design-spec-column-distillate-415da41 -->
- **Settled start, Brent. Expected: 99.90 % ester.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, design spec ethanol feed for 99.9 pct ester. <!-- ethyl-acetate-piotrowski-2021.design-spec-ester-purity-415da41 -->
- **Settled closed plant, ethanol feed 6,506 kg/h; also with the extractor at 20 C (6,506 and 6,508 kg/h). Expected: Product purity near 99.9 %.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant settled, ethanol feed 6506 to 6508 kg h, extractor 27 or 20 c. <!-- ethyl-acetate-piotrowski-2021.ethanol-feed-trimmed-062 -->
- **Settled closed plant, ethanol feed 6,503 and 6,500 kg/h. Expected: Purer product.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant settled, ethanol feed 6500 to 6503 kg h. <!-- ethyl-acetate-piotrowski-2021.ethanol-feed-trimmed-further-062 -->
- **Broyden, direct substitution, Wegstein, warm starts from 0.6.1's streams; column 5 with one liquid or max_iterations 100. Expected: A closed plant near Table A2.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. <!-- ethyl-acetate-piotrowski-2021.plant-paper-column-specs-062 -->
- **Closed plant with the paper's column specifications on 415da41: the 4 variants that end NO_CONVERGENCE. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. Correction: Review problem 4, dataset/reviews/backfill-corrections-review.md (PR #32, AI full check 2026-11-20): one row with symptom no-convergence held 9 runs of 3 kinds (4 NO_CONVERGENCE, 4 OUT_OF_TIME, 1 PHASE_SPLIT); split by symptom. <!-- ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1-no-convergence; corrects ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1 -->
- **Closed plant with the paper's column specifications on 415da41: the 4 variants that end OUT_OF_TIME. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. Correction: Review problem 4, dataset/reviews/backfill-corrections-review.md (PR #32, AI full check 2026-11-20): one row with symptom no-convergence held 9 runs of 3 kinds (4 NO_CONVERGENCE, 4 OUT_OF_TIME, 1 PHASE_SPLIT); split by symptom. <!-- ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1-slow; corrects ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1 -->
- **Closed plant with the paper's column specifications on 415da41, column 5 with one liquid asked (phases VL). Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: closed plant, one flowsheet five tears, paper column specifications. Correction: Review problem 4, dataset/reviews/backfill-corrections-review.md (PR #32, AI full check 2026-11-20): one row with symptom no-convergence held 9 runs of 3 kinds (4 NO_CONVERGENCE, 4 OUT_OF_TIME, 1 PHASE_SPLIT); split by symptom. <!-- ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1-wrong-phase; corrects ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1 -->
- **Closed plant, column 15 on its bottoms purity, column 11 bottoms 141.5 kmol/h. Expected: Closed plant.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 11-16. When: closed plant, column 15 bottoms purity, column 11 bottoms 141.5 kmol h. <!-- ethyl-acetate-piotrowski-2021.plant-product-flow-above-ester-formed-062 -->
- **Closed plant, column 15 on 99.99 % water in its bottoms, column 11 on R/D 3 and distillate 240 kmol/h, recycle 23 fixed, tolerance 3e-4. Expected: A steady-state plant.** failed, CHEPTA run (chepta@0.6.2); Piotrowski & Kubica 2021, p. 9, Section 3.4, paragraph after Figure 5. When: closed plant, column 15 bottoms water 99.99, column 11 distillate 240 kmol h, recycle 23 fixed 95797 kg h, tear tolerance 3e 4. <!-- ethyl-acetate-piotrowski-2021.plant-purity-specs-loose-tolerance-062 -->
- **Section A again with CHEPTA's reflux 27 and wastewater distillate 21. Expected: The loop closes by successive passes.** failed, CHEPTA run (chepta@0.6.1); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25. When: two sections coupled by script, round 2 own recycles. <!-- ethyl-acetate-piotrowski-2021.plant-round2-061 -->
- ~~**The same closed variants. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25.~~ When: closed plant, one flowsheet five tears, paper column specifications. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41; corrected by ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1 -->
- ~~**The same closed variants. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Piotrowski & Kubica 2021, p. 14, Table A2 (continued), streams 23-25.~~ When: closed plant, one flowsheet five tears, paper column specifications. Correction: Review item 4, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row left out plant62-R-purity-direct and plant62-R-bottoms-col5VL and said column 5 passes; col5VL stops with PHASE_SPLIT in column 5, and 4 of the 9 runs end OUT_OF_TIME, not NO_CONVERGENCE. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1; corrected by ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1-no-convergence, ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1-slow, ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41-c1-wrong-phase; corrects ethyl-acetate-piotrowski-2021.plant-paper-column-specs-415da41 -->
