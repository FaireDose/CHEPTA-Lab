# Lessons: methanol-co2-campos-2022 (generated; do not edit)

What the plant taught, for a process engineer: each lesson summarises several runs or decisions below, with When / Do / Why / Check / Result, what it was judged against, its status and source. A lesson that holds beyond this plant is also on its topic page. The run log follows under "Runs behind these lessons"; its rows still count as the evidence. [All topics](../rules-readable.md)

Engine names: a number such as 0.6.2 is a CHEPTA release; 415da41 is an unreleased development version of CHEPTA (a commit), later than release 0.6.2 and not yet released. Results on it are labelled separately from the release's.

## distillation (5)

- **Methanol column in the loop: give it the bottoms flow, not a purity, recovery or boil-up**
  - When: [Campos et al. 2022](https://doi.org/10.3390/pr10081535) gives only stages, feed stage, reflux ratio and condenser temperature, and the column needs a second specification.
  - Do: Fix the bottoms flow at the published water product (4581 kmol/h) and check the purity that results.
  - Why: On chepta 0.6.2 a purity or recovery was refused inside the range CHEPTA itself scanned.
  - Check: Read the water purity in the bottoms against the published 99.985 mol %.
  - Result: With the bottoms flow the column converges at 99.998 % water; a purity or recovery was refused, a boil-up ratio failed in the loop, and the purity given in the plant still fails on 415da41.
  - Judged on: Methanol purity 99.67 mol% of the liquid distillate (met).
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process). <!-- methanol-co2-campos-2022.lesson-column-bottoms-flow-spec -->

- **Column feed with ppm of H2, CO or N2: on chepta 0.6.2 send the traces round the column; on 415da41 they can go through**
  - When: The methanol-water column feed holds a few ppm of permanent gases and the column will not start.
  - Do: On 0.6.2 split the traces off before the column and join them to its vapour. This is a workaround, an imposed split of ppm traces, not the column of [Campos et al. 2022](https://doi.org/10.3390/pr10081535); rerun without it on a later engine (on 415da41 the column converges with them).
  - Why: The feed's bubble point at 1 bar cannot be found with the gases present, and the column starts from it.
  - Check: Remove one gas at a time to find the one that blocks the start; 10 ppm of CO alone was enough.
  - Result: Without the gases the column converges in 6-7 iterations; on 415da41 it converges with them in 6.
  - Judged on: A converged column; the products are judged in the lesson on the condenser with vapour and liquid distillates.
  - Summarises 3 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process). <!-- methanol-co2-campos-2022.lesson-column-light-gas-traces -->

- **Specify the methanol column by its reboiler temperature, moved by the model's own water boiling point**
  - When: A methanol column whose published bottoms temperature (99.6 C) is below the model's boiling point of nearly pure water at the column pressure.
  - Do: Find the model's bottoms temperature at the published purity (a bottoms-flow run), and scan the reboiler temperature just below it; record the shift as an adjustment.
  - Why: A stage temperature fixes the bottoms quality directly; at the published 99.6 C the model's bottoms are only 99.009 % water, and the flow, ratio and recovery specifications at the published values run out of time on chepta 0.6.3.
  - Check: The bottoms purity at the chosen temperature, and that the temperature lies inside the range the engine reports (356.672 to 374.171 K here).
  - Result: 374.0 K (+1.25 K): 99.884 % water alone and 99.929 % in the closed plant, methanol 99.831 %; the bottoms/feed ratio 0.48672, the recovery 0.96115 and the ratio 1.5e-4 stopped at 300 s.
  - Judged on: The methanol and water products of [Campos et al. 2022](https://doi.org/10.3390/pr10081535) (Table S10): 99.667 % methanol, 99.985 % water.
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.3) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. <!-- methanol-co2-campos-2022.lesson-column-reboiler-temperature-063 -->

- **On chepta 415da41 (request M6 open): fix a condenser with little vapour in the recycle plant by its vapour share, not its temperature**
  - When: A vapour-liquid condenser specified by its temperature converges on the published feed but not on the plant's own, lower-CO2 feed.
  - Do: Take the vapour share (here 0.008406) or vapour flow (38.56 kmol/h) from a converged answer and specify that; check the condenser lands at the published temperature.
  - Why: A workaround for one engine: the column exists at 53 C on that feed, but the temperature specification does not start there when the vapour is under 1 %. The share comes from Lab's own plant, solved with the flash workaround.
  - Check: Run the column alone on the plant's feed with each specification.
  - Result: With 53 C every closed variant failed; with the vapour share the plant converged in 47 iterations (2 from a warm start), condenser at 53.005 C, balance check passed.
  - Judged on: A closed plant with the condenser configuration of [Campos et al. 2022](https://doi.org/10.3390/pr10081535); their 53 C specification itself is not yet used (request M6).
  - Summarises 5 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@415da41) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process). <!-- methanol-co2-campos-2022.lesson-condenser-by-vapour-share -->

- **A condenser with vapour and liquid distillates: where only one distillate exists, use a partial condenser and a flash at its temperature**
  - When: The column of [Campos et al. 2022](https://doi.org/10.3390/pr10081535) has a partial condenser at 53 C with a gas and a liquid distillate, and the engine offers one distillate only.
  - Do: Take all the distillate as vapour, then flash it at 53 C into liquid product and gas; state that the reflux composition differs.
  - Why: The product split is the condenser's equilibrium; a liquid side draw under a temperature-set stage did not start.
  - Check: Compare the liquid product, the gas and the duties with [Campos et al. 2022](https://doi.org/10.3390/pr10081535); rerun with a real vapour-liquid condenser when the engine has one.
  - Result: Methanol 4533 kmol/h at 99.835 % (paper 4542 at 99.667 %); on 415da41 the vapour-liquid condenser gives 4532.7 kmol/h at 99.835 %.
  - Judged on: Methanol purity 99.67 mol% (met); the condenser and reboiler duties are 5 % and 17 % above Table S14.
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. <!-- methanol-co2-campos-2022.lesson-vapour-liquid-condenser-by-flash -->

## flash (2)

- **In a methanol loop, check the CO2 dissolved at 70 bar against measured solubility: the published 18.5 mol % is not physical**
  - Correction: The lesson left the 70 bar CO2 split open as a difference between two models. Measured data (Xia et al. 2004, Bezanehtak et al. 2004, Xie et al. 2005; results-chepta-0.6.3/README.md, 2026-11-27) show the paper's 18.5 % is not physical, so the lesson's advice changes from 'settle it first' to 'compare with the measured basis, not the paper'.
  - When: The 70 bar flash liquid of [Campos et al. 2022](https://doi.org/10.3390/pr10081535) holds 0.1855 CO2 with K 0.955, far more than any model CHEPTA offers.
  - Do: Compare the flash liquid with measured CO2 solubility in methanol + water near the flash conditions before tuning anything toward the recycle of [Campos et al. 2022](https://doi.org/10.3390/pr10081535); use the method that follows the data (PR + MHV1 here).
  - Why: The CO2 released at 1 bar returns to the CO2 compressor, so the recycle and the compression follow from the high-pressure solubility; a wrong published solubility makes the published recycle wrong too.
  - Check: [Xia et al. 2004](https://doi.org/10.1021/je049803i) at 313.75 K: about 0.018 to 0.021 at the flash's CO2 partial pressure, 0.108 under 7072 kPa of CO2; pure methanol under H2 at most 0.115, K at least 2.3 ([Bezanehtak et al. 2004](https://doi.org/10.1021/je0301491)).
  - Result: PR + MHV1 gives 2.35 % and PR 3.41 %, against 18.545 % in [Campos et al. 2022](https://doi.org/10.3390/pr10081535); the CO2 recycle is 394.5 against 2786 kmol/h.
  - Judged on: Measured CO2 solubility in methanol + water ([Xia et al. 2004](https://doi.org/10.1021/je049803i)) and in methanol under H2 ([Bezanehtak et al. 2004](https://doi.org/10.1021/je0301491), [Xie et al. 2005](https://doi.org/10.1021/je0498614)), against the 70 bar flash of [Campos et al. 2022](https://doi.org/10.3390/pr10081535).
  - Summarises 3 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.3) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, stream 24; Xia et al. 2004, *Solubility of CO2 in* (https://doi.org/10.1021/je049803i), ThermoML data set 1: T 313.75 K, solvent methanol mole fraction 0.4999 (CO2-free), 8 points; Bezanehtak et al. 2004, *Vapor-Liquid Equilibrium for the Carbon Dioxide +…* (https://doi.org/10.1021/je0301491), ThermoML data set 2 (142 points): the 6 points with vapour H2 0.68-0.76 and 4-7 MPa; Xie et al. 2005, *Bubble and Dew Point Measurements of the…* (https://doi.org/10.1021/je0498614), ThermoML data set 1: CO2 + methanol bubble pressures at 313.2 K, 7 points. <!-- methanol-co2-campos-2022.lesson-dissolved-co2-sets-co2-recycle-c1; corrects methanol-co2-campos-2022.lesson-dissolved-co2-sets-co2-recycle -->

- **H2, CO, CO2 and N2 with methanol and water: use Peng-Robinson with fitted k_ij where no NRTL pairs exist**
  - When: [Campos et al. 2022](https://doi.org/10.3390/pr10081535) use NRTL2 outside the reactor, but CHEPTA has no NRTL pairs for the gases with methanol and water.
  - Do: Use Peng-Robinson with CHEPTA's fitted CO2 + methanol and CO2 + water k_ij everywhere; PR + MHV1 is refused because methanol + N2 has no NRTL pair.
  - Why: An activity model needs pairs for every gas with the solvents; the equation of state rests on its k_ij instead.
  - Check: List the extrapolated k_ij sets CHEPTA reports, and compare the dissolved CO2 of the high-pressure flash first (see the lesson on the dissolved CO2 that sets the CO2 recycle).
  - Result: Every flash runs; FLASH4 vapour +3.6 % and liquid -1.0 %, but the 69.25 bar flash liquid is 9468 against 11,488 kmol/h and holds 3.37 % CO2 against 18.545 %.
  - Judged on: Running every flash with a property method CHEPTA supports; the flash outlets of Table S10 are compared.
  - Summarises 2 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 9, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, stream 24. <!-- methanol-co2-campos-2022.lesson-gases-with-pr-kij -->

- ~~**In a methanol loop the CO2 dissolved at 70 bar sets the low-pressure CO2 recycle: check it against measured solubility first**~~ Corrected by a later row, listed with the corrected version; this one no longer counts.
  - When: The high-pressure flash liquid of the simulation and of [Campos et al. 2022](https://doi.org/10.3390/pr10081535) differ in dissolved CO2.
  - Do: Before comparing the loop, compare the CO2 solubility in methanol + water near 30 C and 70 bar with measured data for both models.
  - Why: The CO2 released at 1 bar goes back to the CO2 compressor, so its amount follows from the high-pressure solubility.
  - Check: Compare the CO2 recycle and the CO2 compression duty only after the solubility is settled.
  - Result: CHEPTA 3.4 against 18.5 mol % CO2 in the flash liquid; the CO2 recycle is 394.47 against 2786 kmol/h (-86 %) and the CO2 compression carries 27-31 % less gas.
  - Judged on: Which CO2 split is physical; not yet checked against measured data.
  - Summarises 4 rows of the run log below.
  - Status: untested — Lab's idea, not yet tested.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, stream 24; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 9, Section 2.5. <!-- methanol-co2-campos-2022.lesson-dissolved-co2-sets-co2-recycle; corrected by methanol-co2-campos-2022.lesson-dissolved-co2-sets-co2-recycle-c1 -->

## heat exchange (2)

- **When a paper's duty and its stream enthalpies disagree, run the exchanger on its inlet and see which one it supports**
  - When: A cooler's duty in [Campos et al. 2022](https://doi.org/10.3390/pr10081535) (Table S14) and the duty from its printed stream enthalpies differ.
  - Do: Cool the printed inlet to the printed outlet temperature; also give each duty and read the outlet temperature.
  - Why: Every other duty matched its streams, so one printed number is likely wrong.
  - Check: Compare per-kelvin heat with the neighbouring exchanger on the same stream.
  - Result: 25.1 MW to 30 C supports 24.2 MW (Table S14), not 19.75 MW (from the enthalpies); 24.2 MW gives 31.05 C, 19.75 MW 36.06 C.
  - Judged on: Which printed duty the simulation supports; two models agreeing, not a measurement.
  - Summarises 2 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 26, Table S14, HE7; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process). <!-- methanol-co2-campos-2022.lesson-duty-against-stream-enthalpies -->

- **Feed-effluent exchanger with a condensing hot side and a boiling cold side: specify a 2 K minimum approach, not the published outlets**
  - When: The published outlet temperatures for an exchanger inside the loop lead to a temperature cross.
  - Do: Give the exchanger a minimum approach of 2 K (on chepta 0.6.2 with 10 zones); give the small trim exchanger its cold outlet, not its hot outlet.
  - Why: With CHEPTA's properties the hot stream cannot give the published heat above about 70 C, and the zones decide where the internal pinch is found.
  - Check: Read the duty and the cold outlet; check that the same duty is accepted with the default zones.
  - Result: 114,966 kW against 103.3 MW in Table S14 (+11 %), cold outlet 84.99 against 82.9 C (Table S9) with 10 zones; on 415da41 the published streams work without zones, but the plant's own streams still meet a cross.
  - Judged on: An exchanger that converges inside the loop. Its duty, 114,966 kW, is 11 % above the 103.3 MW of HE5 in Table S14 of [Campos et al. 2022](https://doi.org/10.3390/pr10081535), and its cold outlet, 84.99 C, is above the 82.9 C of stream 29 (Table S9).
  - Summarises 7 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), pp. 4-5, Section 2.1, one-step process. Passage reread on 2026-11-24: Campos et al. 2022, supplement Table S14 (HE5, 103.3 MW) and Table S9 (stream 29, the column feed after HE5, at 82.9 C). <!-- methanol-co2-campos-2022.lesson-feed-effluent-exchanger-approach -->

## pfr (1)

- **Boiling-water-cooled tubular reactor: the outlet hardly moves with U between 150 and 1000 W/m2/K; the published 155 lies in that range**
  - When: [Campos et al. 2022](https://doi.org/10.3390/pr10081535) give the kinetics, the tubes (33,000 of 12.5 m and 3.75 cm per module, 70 bar) and U: 160 at the inlet, 150 W/m2/K at the outlet, 155 used (pp. 13-14).
  - Do: Use the published U with the coolant at its boiling temperature. Lab missed the printed value, assumed 300 W/m2/K and bounded it with 150 and 1000.
  - Why: With boiling water on the shell the tubes run near the coolant temperature, so U matters little.
  - Check: Compare the outlet flow, temperature and methanol with the published reactor outlet; rerun at the published U.
  - Result: U 300: flow -0.2 %, -0.2 K, methanol 7.53 against 7.415 mol %; U 150 (nearest the published 155) against 1000: 0.40 K and up to 0.035 points (hydrogen). No run at 155 itself.
  - Judged on: The reactor outlet 16 of [Campos et al. 2022](https://doi.org/10.3390/pr10081535) (Table S10).
  - Summarises 2 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 4, Section 2.1; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 1, Abstract. <!-- methanol-co2-campos-2022.lesson-reactor-u-assumed -->

## recycle (4)

- **The closed methanol plant matches Campos et al. 2022 at the column ends; compare the CO2 loop separately**
  - When: The whole plant converges and is compared stream by stream with [Campos et al. 2022](https://doi.org/10.3390/pr10081535).
  - Do: Report the products and the main recycle first, then the CO2 loop with its property-method caveat.
  - Why: The products depend on the reactor and the column, the CO2 loop on the dissolved CO2.
  - Check: Compare 31-MEOH, 30-WATER, 36-REC, 32 and 39-REC with Table S10.
  - Result: Methanol 4548 kmol/h at 99.728 % (paper 4542 at 99.667 %); water 99.9994 %; gas distillate 38.56 against 289 kmol/h and CO2 recycle 394.47 against 2786 kmol/h.
  - Judged on: Methanol purity 99.67 mol% (met); the CO2 recycle differs through the dissolved CO2 (see the lesson on the CO2 dissolved at 70 bar).
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5. <!-- methanol-co2-campos-2022.lesson-closed-plant-ends-agree -->

- **On chepta 0.6.3 the methanol plant closes with the published condenser, column feed and HE5 approach**
  - When: The workarounds of earlier engines (a vapour share, gases bypassed, extra exchanger zones, an assumed U) are no longer needed.
  - Do: Remove each workaround, keep the published U of 155, and close the plant from the published tear guesses; compare the product ends first.
  - Why: The engine now starts a condenser fixed by its temperature, starts a column with ppm gases and holds the approach along the whole exchanger.
  - Check: Balance check passed; HE5 at 2.000 K along the exchanger; condenser at 53 C.
  - Result: 29 loop iterations; methanol 4540.8 kmol/h at 99.835 % (published 4542 at 99.667 %), water 99.929 % (99.985 %); the CO2 recycle stays 394.5 kmol/h, on PR, not on PR + MHV1.
  - Judged on: The methanol product of [Campos et al. 2022](https://doi.org/10.3390/pr10081535) (4542 kmol/h at 99.667 %), with its condenser at 53 C, the gas traces in the column feed and a 2 K approach in HE5.
  - Summarises 4 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.3) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. <!-- methanol-co2-campos-2022.lesson-closed-plant-paper-specs-063 -->

- **Feed-effluent exchangers add cycles: choose tears that break every cycle, and give a slow loop more iterations**
  - When: A plant with gas recycles and feed-effluent exchangers is closed as one flowsheet.
  - Do: Choose tears that cut each exchanger's cycle; how many is not the test. Start them from the published values and raise the iteration limit while the change is still falling.
  - Why: Each exchanger joining two parts of the plant makes a cycle the recycles alone do not break; the loop is slow, not stuck.
  - Check: If the engine says the tears do not break every cycle, move a tear onto a stream inside the exchanger's cycle; compare the tear change between the last iterations.
  - Result: Recycle tears only, and five tears including 36-REC: refused. Moving that tear to the stream on the far side of HE2: closed in 31 iterations with both purges, 36-REC +2.7 % against [Campos et al. 2022](https://doi.org/10.3390/pr10081535); the loop alone needed more than 50 iterations (200 allowed).
  - Judged on: A closed plant with balances closed; the products are judged in the lessons on the methanol column and the closed plant.
  - Summarises 6 rows of the run log below.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process). <!-- methanol-co2-campos-2022.lesson-tears-break-every-cycle -->

- **On chepta 0.6.3, PR + MHV1 runs this plant's flashes but not its enthalpy-specified units: report, do not work around**
  - When: A methanol plant with H2, CO2 and water moves to PR + MHV1 after the flashes look right on it.
  - Do: Run each unit alone on the published inlets on the new method before the plant; reduce a refusal to the smallest input with a control on the old method.
  - Why: The plant stops at its first mixer, so only the unit runs show that every mixer, valve and exchanger fails the same way, and the small input makes the request testable.
  - Check: The adiabatic heater on H2 + CO2 + water at 33 C and 100 kPa: refused on PR + MHV1, ok on PR and with the temperature given.
  - Result: Flashes, compressors, HE2, HE7 and the reactor run; HE4, HE5, HE6, MIXER1, MIXER4, VALVE1 stop with no physical root (31.4 to 84.2 K); the plant stops at MIXER1 or at CP3 (300 K, 7000 kPa).
  - Judged on: A closed one-step plant of [Campos et al. 2022](https://doi.org/10.3390/pr10081535) on PR + MHV1, the method CHEPTA advises for it.
  - Summarises 4 rows of the run log below.
  - Status: failed — Lab's CHEPTA run (chepta@0.6.3) did not converge or missed its target.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 9, Section 2.5. <!-- methanol-co2-campos-2022.lesson-mhv1-ph-flash-063 -->

## Runs behind these lessons

One line per decision or CHEPTA run, grouped by unit, best-supported first; the row id is in an HTML comment for `kb.py show`. A struck-through line was corrected by a later row and no longer counts; the correcting row gives its reason.

### distillation (19)

- **Paper's feed without the traces, partial condenser, reflux 2, bottoms 4581 kmol/h, then flash at 53 C. Expected: The paper's 31-MEOH, 30-WATER and 32.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 gases bypassed, partial condenser then flash 53 c, bottoms 4581 kmol h. <!-- methanol-co2-campos-2022.column-gases-bypassed-flash53-062 -->
- **Column alone, plant-a6's stream 29. Expected: A converged column near 53 C.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, plant a6 column feed low co2, vapour liquid condenser share or vapour flow. <!-- methanol-co2-campos-2022.column-plant-feed-by-share-415da41 -->
- **Column on the paper's full feed, partial condenser. Expected: A converged column.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, paper feed 29 with ppm gases, one distillate. <!-- methanol-co2-campos-2022.column-ppm-gases-415da41 -->
- **Column alone on feed 29, PR + MHV1. Expected: A specification by what matters.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 with ppm gases, vapour liquid condenser 53 c, reboiler temperature specified. <!-- methanol-co2-campos-2022.column-reboiler-temperature-063 -->
- **Column alone on feed 29, PR + MHV1. Expected: Know which specifications converge.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 with ppm gases, vapour liquid condenser 53 c, ratio or recovery off paper value. <!-- methanol-co2-campos-2022.column-specs-off-paper-values-063 -->
- **Column alone on the paper's feed 29, with and without the traces; also reflux 2.1273 (2 over the whole distillate). Expected: The paper's 31-MEOH and 32.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 with ppm gases, vapour liquid condenser 53 c, bottoms 4581 kmol h. <!-- methanol-co2-campos-2022.column-vapour-liquid-condenser-alone-415da41 -->
- **Column alone on the paper's feed 29 with its traces. Expected: A baseline for the respecification.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 with ppm gases, vapour liquid condenser 53 c, bottoms 4581 kmol h. <!-- methanol-co2-campos-2022.column-vl-bottoms-4581-063 -->
- **Methanol-water column with dissolved CO2: partial condenser with a gas and a liquid distillate**
  - When: The column feed still holds CO2 and traces of H2, CO and N2.
  - Do: Use 30 stages, feed above stage 24, reflux ratio 2, and a partial condenser at 53 C with liquid and vapour distillates ([Campos et al. 2022](https://doi.org/10.3390/pr10081535)).
  - Why: The gases leave in the vapour distillate and methanol as liquid.
  - Check: Methanol 99.67 mol %, water 99.99 mol %.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 10, Section 2.5; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. <!-- methanol-co2-campos-2022.paper-column-vapour-liquid-condenser -->
- **Whole plant on PR. Expected: The paper's condenser specification.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, vapour liquid condenser 53 c. <!-- methanol-co2-campos-2022.plant-condenser-at-53c-063 -->
- **Whole plant, Broyden, from the paper's start and from plant-a6's tears; also with the traces through the column. Expected: A closed plant with the paper's condenser configuration.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: closed plant, vapour liquid condenser vapour share 0.008406. <!-- methanol-co2-campos-2022.plant-condenser-by-vapour-share-415da41 -->
- **Column alone, plant-a6's stream 29. Expected: A converged column.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, plant a6 column feed low co2, vapour liquid condenser 53 c. <!-- methanol-co2-campos-2022.column-plant-feed-at-53c-415da41 -->
- **30 stages, feed 24, reflux 2, bottoms 4581 kmol/h, PR. Expected: A converged column.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, paper feed 29 with ppm gases, one distillate. <!-- methanol-co2-campos-2022.column-ppm-gases-062 -->
- **Column alone and in the plant. Expected: A converged column at the purity.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 gases bypassed, bottoms water purity or recovery specified. <!-- methanol-co2-campos-2022.column-purity-or-recovery-spec-062 -->
- **Column alone, with and without the traces. Expected: Both distillates from one column.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: unit alone, liquid side draw stage 2, stage 1 at 53 c. <!-- methanol-co2-campos-2022.column-side-draw-for-liquid-distillate-062 -->
- **Column alone on feed 29, PR + MHV1. Expected: Converge or be refused with the range.** failed, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: unit alone, paper feed 29 with ppm gases, vapour liquid condenser 53 c, ratio or recovery at paper value. <!-- methanol-co2-campos-2022.column-specs-at-paper-values-063 -->
- **Whole plant. Expected: A closed plant.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, column boil up ratio 1.17155. <!-- methanol-co2-campos-2022.plant-boilup-spec-062 -->
- **Whole plant with the new condenser. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, vapour liquid condenser 53 c. <!-- methanol-co2-campos-2022.plant-condenser-at-53c-415da41 -->
- **Closed plant with the condenser by its vapour share. Expected: A closed plant.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32. When: closed plant, vapour liquid condenser vapour share 0.008406, bottoms water 99.985 specified. <!-- methanol-co2-campos-2022.plant-purity-spec-415da41 -->
- **Not run: rerun plant-vl on the release that answers M6. Expected: The paper's configuration and specification together.** untested, Lab's reasoning; Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, vapour liquid condenser 53 c after m6. <!-- methanol-co2-campos-2022.open-condenser-temperature-spec -->

### flash (5)

- **Compared both models with measured data (co2_solubility_check.py). Expected: Know which split is physical.** worked, measured; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, stream 24; Xia et al. 2004, ThermoML data set 1: T 313.75 K, solvent methanol mole fraction 0.4999 (CO2-free), 8 points; Bezanehtak et al. 2004, ThermoML data set 2 (142 points): the 6 points with vapour H2 0.68-0.76 and 4-7 MPa; Xie et al. 2005, ThermoML data set 1: CO2 + methanol bubble pressures at 313.2 K, 7 points. When: flash 30 c 69.25 bar, co2 in liquid 3.4 vs 18.5 mol pct. Correction: The row called the 3.4 against 18.5 mol % difference a property-method difference that Lab does not judge without data. Measured data (Xia et al. 2004, Bezanehtak et al. 2004, Xie et al. 2005; results-chepta-0.6.3/README.md, 2026-11-27) now judge it: the paper's 18.5 % is about nine times the measured basis and its K below 1 is not physical; the comparison of the CO2 recycle is made against the measured basis, not the paper. <!-- methanol-co2-campos-2022.open-co2-solubility-hp-flash-c1; corrects methanol-co2-campos-2022.open-co2-solubility-hp-flash -->
- **Release the dissolved gases in two flashes, 70 bar then 1 bar, and recycle the low-pressure CO2**
  - When: The condensate of the 70 bar loop holds dissolved CO2 and light gases.
  - Do: Flash at 30 C and 69.25 bar, let the liquid down to 1 bar and flash at 30 C again; recycle that gas to the CO2 feed less a 2 % purge ([Campos et al. 2022](https://doi.org/10.3390/pr10081535)).
  - Why: Keeps the gases out of the methanol column.
  - Check: The column feed should hold about 1.285 mol % CO2.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), pp. 4-5, Section 2.1, one-step process; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, stream 24; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 14, Table S10, stream 28. <!-- methanol-co2-campos-2022.paper-two-flashes-co2-recycle -->
- **Every flash on the paper's inlets with PR. Expected: The paper's flash outlets.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 9, Section 2.5; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, stream 24. When: unit alone, paper inlet, peng robinson fitted kij. <!-- methanol-co2-campos-2022.property-method-pr-everywhere-062 -->
- **FLASH1 to FLASH4 alone on the paper's inlets. Expected: The dissolved CO2 from a method that follows measured solubility.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, stream 24; Campos et al. 2022, p. 9, Section 2.5; Xia et al. 2004, ThermoML data set 1: T 313.75 K, solvent methanol mole fraction 0.4999 (CO2-free), 8 points; Bezanehtak et al. 2004, ThermoML data set 2 (142 points): the 6 points with vapour H2 0.68-0.76 and 4-7 MPa; Xie et al. 2005, ThermoML data set 1: CO2 + methanol bubble pressures at 313.2 K, 7 points. When: unit alone, paper inlet, peng robinson mhv1. <!-- methanol-co2-campos-2022.property-method-pr-mhv1-063 -->
- **FLASH3 and the column with PR + MHV1. Expected: An answer with NRTL in the mixing rule.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 9, Section 2.5. When: unit alone, paper inlet, peng robinson mhv1. <!-- methanol-co2-campos-2022.property-method-pr-mhv1-062 -->
- ~~**Not run: compare both against measured CO2 solubility in methanol + water near 30 C and 70 bar. Expected: Know which split is physical before the loop is compared on CO2.** untested, Lab's reasoning; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, stream 24; Campos et al. 2022, p. 9, Section 2.5.~~ When: flash 30 c 69.25 bar, co2 in liquid 3.4 vs 18.5 mol pct. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- methanol-co2-campos-2022.open-co2-solubility-hp-flash; corrected by methanol-co2-campos-2022.open-co2-solubility-hp-flash-c1 -->

### heat exchange (13)

- **HE5 alone, dTmin 2 K, zones 10. Expected: A 2 K approach.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, zones 10. <!-- methanol-co2-campos-2022.he5-min-approach-10-zones-062 -->
- **HE5 alone on the paper's streams 20 and 28, PR. Expected: A 2 K approach without the workaround.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones. <!-- methanol-co2-campos-2022.he5-min-approach-default-zones-063 -->
- **HE5 alone on the paper's streams. Expected: A 2 K approach.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones. <!-- methanol-co2-campos-2022.he5-min-approach-default-zones-415da41 -->
- **HE5 alone on plant-a6's streams, PR. Expected: A 2 K approach on the plant's streams.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones, plant a6 streams. <!-- methanol-co2-campos-2022.he5-plant-streams-default-zones-063 -->
- **HE7 on the paper's stream 22. Expected: One of the two duties confirmed.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement p. 26, Table S14, HE7; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process). When: unit alone, paper stream 22 to 30 c. <!-- methanol-co2-campos-2022.he7-cooling-duty-062 -->
- **Cool the reactor effluent through three feed-effluent exchangers before cooling water**
  - When: The reactor effluent near 248 C must be cooled to 30 C while three cold streams need heat.
  - Do: Heat the reactor feed, the column feed and the low-pressure flash feed with the effluent, then cool the rest with water ([Campos et al. 2022](https://doi.org/10.3390/pr10081535)).
  - Why: Recovers the reaction heat inside the plant.
  - Check: The cooling-water duty of Table S14 (24.2 MW) and the stream enthalpies disagree; see the lesson on a duty that disagrees with its stream enthalpies.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), pp. 4-5, Section 2.1, one-step process; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement p. 26, Table S14, HE7; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process). <!-- methanol-co2-campos-2022.paper-feed-effluent-exchangers -->
- **Five small flowsheets of one heater. Expected: Isolate the condition that fails.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 9, Section 2.5. When: minimal input, h2 co2 water controls. <!-- methanol-co2-campos-2022.ph-flash-controls-063 -->
- **HE5 alone on the paper's streams 20 and 28, and in the loop. Expected: The largest duty at a 2 K approach.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones. <!-- methanol-co2-campos-2022.he5-min-approach-default-zones-062 -->
- **The synthesis loop section with Broyden, direct substitution and Wegstein. Expected: A closed loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: synthesis loop section, exchangers by paper outlet temperatures. <!-- methanol-co2-campos-2022.he5-paper-outlets-in-loop-062 -->
- **HE5 alone and in the closed plant. Expected: A 2 K approach.** failed, CHEPTA run (chepta@415da41); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: he5 min approach 2 k, default zones, plant a6 streams. <!-- methanol-co2-campos-2022.he5-plant-streams-default-zones-415da41 -->
- **Synthesis loop section. Expected: A closed loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, pp. 4-5, Section 2.1, one-step process. When: synthesis loop section, he6 by hot outlet. <!-- methanol-co2-campos-2022.he6-by-hot-outlet-062 -->
- **HE4, HE5, HE6, MIXER1, MIXER4, VALVE1 alone; an adiabatic heater on H2 + CO2 + water. Expected: Units that run as on PR.** failed, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 9, Section 2.5. When: unit alone, paper inlet, peng robinson mhv1, ph flash. <!-- methanol-co2-campos-2022.ph-flash-mhv1-gases-water-063 -->
- **A reading of Tables S9 and S14 with run u-he7; not checked with the authors. Expected: Use the stream table as the comparison basis (the maintainer, 2026-11-14) and treat HE7's printed outlet enthalpy with care.** lead, Lab's reasoning; Campos et al. 2022, supplement p. 26, Table S14, HE7; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process). When: campos 2022 one step process, he7 24.2 vs 19.75 mw. <!-- methanol-co2-campos-2022.open-he7-stream-enthalpy -->

### pfr (3)

- **CO2 hydrogenation to methanol: boiling-water-cooled multitubular reactors at 70 bar with gas recycle**
  - When: CO2 and H2 react to methanol and water, exothermic and limited by equilibrium.
  - Do: Use parallel modules of 33,000 tubes (12.5 m, 3.75 cm), Cu/ZnO/Al2O3, at 70 bar, cooled by boiling water ([Campos et al. 2022](https://doi.org/10.3390/pr10081535)), and recycle the unconverted gas.
  - Why: High pressure favours methanol; boiling water holds the tubes near isothermal.
  - Check: Single-pass CO2 conversion 28.5 % against 30.4 % at equilibrium ([Campos et al. 2022](https://doi.org/10.3390/pr10081535), abstract).
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 4, Section 2.1; Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), p. 1, Abstract. <!-- methanol-co2-campos-2022.paper-multitubular-reactor-70-bar -->
- **Reactor on the paper's inlet, U 300, 150 and 1000, and isothermal. Expected: The paper's outlet 16.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 4, Section 2.1; Campos et al. 2022, p. 1, Abstract; Campos et al. 2022, pp. 13-14, Section 3.1.1. When: unit alone, paper inlet, lhhw model 6p on fugacities, coolant constant 247.5 c, u 150 to 1000 w m2 k, u 155 printed. Correction: Review finding M1, dataset/reviews/plant-lessons-review.md (PR #34, AI full check 2026-11-24): Campos et al. 2022 do print U, 160 and 150 W/m2/K along the tube and 155 used (pp. 13-14); the c2 row said it is not printed. The runs and their outcome are unchanged. <!-- methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c3; corrects methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c2 -->
- **Reactor alone on the paper's stream 15, PR and PR + MHV1. Expected: The reactor at the published U.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 4, Section 2.1; Campos et al. 2022, pp. 13-14, Section 3.1.1. When: unit alone, paper inlet, lhhw model 6p on fugacities, coolant constant 247.5 c, u 155 printed. <!-- methanol-co2-campos-2022.reactor-u155-063 -->
- ~~**Reactor on the paper's inlet, U 300, 150 and 1000, and isothermal. Expected: The paper's outlet 16.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 4, Section 2.1; Campos et al. 2022, p. 1, Abstract.~~ When: unit alone, paper inlet, lhhw model 6p on fugacities, coolant constant 247.5 c, u 150 to 1000 w m2 k. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- methanol-co2-campos-2022.reactor-lhhw-u-assumed-062; corrected by methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c1 -->
- ~~**Reactor on the paper's inlet, U 300, 150 and 1000, and isothermal. Expected: The paper's outlet 16.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 4, Section 2.1; Campos et al. 2022, p. 1, Abstract.~~ When: unit alone, paper inlet, lhhw model 6p on fugacities, coolant constant 247.5 c, u 150 to 1000 w m2 k. Correction: Review item 8, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): U 150 and 1000 move the outlet by 0.40 K and about 0.02 points (0.021 in methanol, at most 0.024 in any component), not 0.04 points. The case README line 85 has the same figure; it is sha256-bound and left unchanged. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c1; corrected by methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c2; corrects methanol-co2-campos-2022.reactor-lhhw-u-assumed-062 -->
- ~~**Reactor on the paper's inlet, U 300, 150 and 1000, and isothermal. Expected: The paper's outlet 16.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, p. 4, Section 2.1; Campos et al. 2022, p. 1, Abstract.~~ When: unit alone, paper inlet, lhhw model 6p on fugacities, coolant constant 247.5 c, u 150 to 1000 w m2 k. Correction: Review problem 2, dataset/reviews/backfill-corrections-review.md (PR #32, AI full check 2026-11-20): the c1 row said 'about 0.02 points', taking methanol only; across components U 150 against U 1000 moves H2 by 0.035 points, so the original '0.04 points' was right to one figure. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c2; corrected by methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c3; corrects methanol-co2-campos-2022.reactor-lhhw-u-assumed-062-c1 -->

### purge (1)

- **Purge 2 % of each flash gas to bound the inerts in the recycle**
  - When: N2, CO and excess H2 build up in the gas recycle.
  - Do: Purge 2 % of the high-pressure and 2 % of the low-pressure flash gas, recycle the rest, and burn the purges ([Campos et al. 2022](https://doi.org/10.3390/pr10081535)).
  - Why: A fixed purge fraction bounds the inert inventory.
  - Check: Purges 1051 and 51 kmol/h.
  - Status: worked — shown by the paper's own simulation; Lab's runs of it are in the run log of this plant.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), pp. 4-5, Section 2.1, one-step process. <!-- methanol-co2-campos-2022.paper-purge-2-pct -->

### recycle (7)

- **Synthesis loop section, Broyden. Expected: A converged loop.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: synthesis loop section, he5 min approach 2 k zones 10. <!-- methanol-co2-campos-2022.loop-iteration-limit-062 -->
- **Whole plant as one CHEPTA flowsheet (fired heater and steam cycle left out), Broyden. Expected: The paper's products and recycles.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32; Campos et al. 2022, p. 10, Section 2.5. When: closed plant, five tears 19 35 26 28 39 rec, column bottoms 4581 kmol h, traces bypassed, he5 min approach 2 k zones 10. Correction: Review nits 7 and 8, dataset/reviews/backfill-corrections-review.md (PR #32, AI full check 2026-11-20): 39-REC is 394.47 kmol/h (not 395) and 30-WATER 99.9994 mol % water in run plant-a6. <!-- methanol-co2-campos-2022.plant-closed-062-c2; corrects methanol-co2-campos-2022.plant-closed-062-c1 -->
- **Whole plant, Broyden, from the paper's start and from the 415da41 plant's tears; also bottoms 4581 and U 300. Expected: A closed plant with the paper's specifications.** worked, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 10, Section 2.5; Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32; Campos et al. 2022, supplement pp. 9-10, Section E (one-step process). When: closed plant, peng robinson fitted kij, five tears 19 35 26 28 39 rec, vapour liquid condenser 53 c, traces through column, he5 min approach 2 k default zones, u 155 printed, reboiler 374 k. <!-- methanol-co2-campos-2022.plant-closed-pr-063 -->
- **plant-a6 on CHEPTA main 415da41. Expected: Same answer.** worked, CHEPTA run (chepta@415da41); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, five tears 19 35 26 28 39 rec, column bottoms 4581 kmol h, traces bypassed, he5 min approach 2 k zones 10. <!-- methanol-co2-campos-2022.plant-rerun-a6-415da41 -->
- **Synthesis loop section, Broyden. Expected: A converged loop.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: synthesis loop section, iterations 50. <!-- methanol-co2-campos-2022.loop-50-iterations-062 -->
- **Whole plant and two sections, PR + MHV1. Expected: A closed plant on PR + MHV1.** failed, CHEPTA run (chepta@0.6.3); Campos et al. 2022, p. 9, Section 2.5. When: closed plant, peng robinson mhv1. <!-- methanol-co2-campos-2022.plant-mhv1-063 -->
- **Whole plant, tears 19, 36-REC, 26, 39-REC, then also 28. Expected: A closed plant.** failed, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process). When: closed plant, tears on recycles only. <!-- methanol-co2-campos-2022.plant-tears-recycles-only-062 -->
- ~~**Whole plant as one CHEPTA flowsheet (fired heater and steam cycle left out), Broyden. Expected: The paper's products and recycles.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32; Campos et al. 2022, p. 10, Section 2.5.~~ When: closed plant, five tears 19 35 26 28 39 rec, column bottoms 4581 kmol h, traces bypassed, he5 min approach 2 k zones 10. Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- methanol-co2-campos-2022.plant-closed-062; corrected by methanol-co2-campos-2022.plant-closed-062-c1 -->
- ~~**Whole plant as one CHEPTA flowsheet (fired heater and steam cycle left out), Broyden. Expected: The paper's products and recycles.** worked, CHEPTA run (chepta@0.6.2); Campos et al. 2022, supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, supplement pp. 10-11, Section E (one-step process); Campos et al. 2022, supplement p. 14, Table S10, streams 30-WATER, 31-MEOH, 32; Campos et al. 2022, p. 10, Section 2.5.~~ When: closed plant, five tears 19 35 26 28 39 rec, column bottoms 4581 kmol h, traces bypassed, he5 min approach 2 k zones 10. Correction: Review item 7, dataset/reviews/backfill-plants-review.md (PR #30, AI full check 2026-11-20): the row gave 31-MEOH, 30-WATER, 36-REC and 39-REC but not the gas distillate 32 (38.6 against 289 kmol/h). Corrected by a later row, listed with the corrected version; this one no longer counts. <!-- methanol-co2-campos-2022.plant-closed-062-c1; corrected by methanol-co2-campos-2022.plant-closed-062-c2; corrects methanol-co2-campos-2022.plant-closed-062 -->
