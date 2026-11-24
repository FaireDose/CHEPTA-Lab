# Reactors, routes and recycles (generated; do not edit)

Reactor type, route choice, reactant recycles and purges. 19 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

Engine names: a number such as 0.6.2 is a CHEPTA release; 415da41 is an unreleased development version of CHEPTA (a commit), later than release 0.6.2 and not yet released. Results on it are labelled separately from the release's.

- **Hold an excess reactant with no exit by a design specification on its feed, aimed at its limit in the product**
  - From Lab's own plant: [ethyl-acetate-piotrowski-2021](../plants/ethyl-acetate-piotrowski-2021.md).
  - When: An excess reactant can leave only with the product, and trimming its feed by hand in steps of a few kg/h fails to converge.
  - Do: Let a design specification vary that feed for the reactant's limit in the product (here 0.04 % ethanol), starting from a settled answer.
  - Why: The design specification finds the feed that hand steps only bracketed; aiming it at the purity instead ran out of time.
  - Check: Read the feed found, the solves and the time; then raise the next limiting setting by hand.
  - Result: Ethanol feed 6,506.23 kg/h found in 8 solves and 108 min, 0.040 % ethanol; product 99.473 %, then 99.561 % with the distillate raised to 260 kmol/h; 99.90 % as the target ran out of time after 3 h.
  - Judged on: Ethanol in the product at most 0.04 wt% ([Piotrowski & Kubica 2021](https://doi.org/10.3390/pr9081425), Section 3.4): met. The ester purity of 99.90 wt% is not met (99.473 %).
  - Summarises 5 rows of the plant's run log.
  - Status: worked — Lab ran it in CHEPTA (chepta@415da41) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 9, Section 3.4, paragraph after Figure 5. <!-- ethyl-acetate-piotrowski-2021.lesson-hold-excess-reactant-by-design-spec -->

- **Never fix a product flow above what the fresh feeds can form, nor every outlet of a closed plant**
  - From Lab's own plant: [ethyl-acetate-piotrowski-2021](../plants/ethyl-acetate-piotrowski-2021.md).
  - When: A printed product flow or two round outlet flows are taken as specifications of a recycle plant.
  - Do: Fix one flow inside the recycle and let one outlet follow; check that a fixed product flow is below the product the feeds can form.
  - Why: 141.5 kmol/h of product exceeds the 141.07 kmol/h of ester the feeds form, so the reactor starves; with the feeds and both outlets fixed the product flow is set by the balance and the column cannot also hold its purity.
  - Check: Before running, compare each fixed flow with the feeds and the stoichiometry.
  - Result: With 141.5 kmol/h the loop stopped (reactor short of ethanol); with recycle 23 fixed the plant settled and the wastewater found 19,919 kg/h by itself.
  - Judged on: A closed plant that converges; the product purity is judged in the lesson on short product purity in the closed plant.
  - Summarises 4 rows of the plant's run log.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 23-25; Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 11-16. <!-- ethyl-acetate-piotrowski-2021.lesson-product-flow-within-feed -->

- **Esterification catalyst: prefer a solid acid to a dissolved mineral acid**
  - When: You choose a catalyst for esterification.
  - Do: Prefer a solid acid catalyst where its temperature limit allows.
  - Why: A dissolved acid is active but corrodes equipment, cannot be recovered and stays in the product, adding purification steps. A solid catalyst stays in the reactor.
  - Check: Check the solid catalyst's temperature limit against the reaction temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Sections 2.1 and 2.2. <!-- hoff-eisenacher-2025-esterification-review.homogeneous-acid-drawbacks -->

- **Large continuous plant: stirred tanks in series, not one tank**
  - When: A continuous reactor gives lower conversion than the batch process.
  - Do: Use stirred tanks in series.
  - Why: One tank is fully back-mixed; tanks in series approach plug flow and batch-like conversion.
  - Check: In CHEPTA, compare the conversion of one, two and three stirred tanks of the same total volume.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design of biodiesel production using chemical catalyst'. <!-- pasha-2021-biodiesel-process-design.continuous-cstrs-in-series -->

- **Butyl acetate equilibrium: a hotter reactor gives lower, not higher, conversion**
  - When: You want more conversion from the esterification of n-butanol with acetic acid in a plain reactor.
  - Do: Do not raise the temperature to beat the equilibrium limit. Remove a product instead.
  - Why: The reaction is mildly exothermic (about -29 kJ/mol), so its equilibrium shifts back as temperature rises (Le Chatelier).
  - Check: In CHEPTA, scan an equilibrium reactor's temperature and confirm that conversion falls as temperature rises. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) show the curve in Fig. 1 only, not as a table.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, pp. 2-3 (Eq. 1, Fig. 1); Section 6.1, p. 12 (Fig. 13). <!-- al-rabiah-2022.equilibrium-conversion-falls-with-temperature -->

- **Butyl acetate in a fixed bed levels off near 70% conversion: plan to recycle both reactants**
  - When: A conventional fixed-bed reactor over Amberlyst-15 (an acidic ion-exchange resin) at 363 K with a 1:1 acid to butanol feed.
  - Do: Size the bed for a near-equilibrium outlet: more bed adds nothing once conversion levels off (within about 2.5 m in [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801)). Plan to separate and recycle the unreacted acid and butanol.
  - Why: The reactor reaches equilibrium quickly, at about 70% butanol conversion per pass.
  - Check: Check that the reactor outlet sits near 69.8% butanol conversion and that the recycle carries about 43 kmol/h of each reactant per 100 kmol/h fresh feed (Table 7 of [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801)).
  - Result: Conversion 69.8% with a 41 m3 reactor and 284 kPa feed pressure (Table 6); about 43 kmol/h each of acid and alcohol left to recycle.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.1, pp. 10-12 (Table 6, Fig. 14); Table 7, p. 14 (streams 3-4). <!-- al-rabiah-2022.fixed-bed-conversion-near-70 -->

- **Two Amberlyst-15 rate laws for butyl acetate disagree on the equilibrium: use one model for all routes**
  - When: You compare butyl acetate routes that use different published rate laws for the same resin catalyst at 363 K.
  - Do: Use one consistent kinetic and equilibrium model across the routes, or report the difference. In [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) the fixed-bed law implies an equilibrium constant of about 5.0 (Lab's ratio of the forward and backward rate constants), while the membrane-reactor law uses 3.51.
  - Why: The two laws come from different literature sources. A larger equilibrium constant alone makes a route look better.
  - Check: Recompute the ratio from Eqs. 14-15 at 363 K before using it: the units of the rate constants are not printed and the concentration bases may differ.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 3, p. 3 (Eqs. 2-4); Section 6.1, p. 10 (Eqs. 13-15). <!-- al-rabiah-2022.kinetic-laws-imply-different-keq -->

- **Conventional glycol reactor: an adiabatic tube with a large water excess**
  - When: Back-mixing would bring product glycol into contact with fresh oxide.
  - Do: Use an adiabatic tubular reactor in turbulent flow without back-mixing, fed with oxide diluted in a large water excess.
  - Why: Plug flow keeps the residence time narrow, which limits further reaction of glycol with oxide and avoids oxide vapour breakthrough.
  - Check: In CHEPTA, model it as a plug-flow reactor and check the selectivity to monoethylene glycol.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Introduction, p. 2 (Fig. 1). <!-- othman-2024-meg-reactive-distillation.tubular-reactor-no-backmixing -->

- **Ethylene oxide hydration without catalyst: use a large water excess, and plan to evaporate it**
  - When: In non-catalytic hydration of ethylene oxide, glycol reacts further with the oxide to di- and triethylene glycol.
  - Do: Feed the hydration reactor with a high water to oxide ratio: 10 to 25 mol per mol oxide in the literature cited by [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y), 10 in their simulation.
  - Why: Dilution makes the oxide meet water rather than glycol.
  - Check: Count the water to be evaporated downstream: it is the price of the selectivity.
  - Result: Higher monoethylene glycol selectivity, and a much larger water load.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'Indirect hydration process', p. 6; 'MEG production via direct EO hydration process', p. 8. <!-- shehata-2024-meg-routes.direct-hydration-water-excess -->

- **Membrane-reactor route for butyl acetate loses on cost because of its butanol-ester column; it may win above about 95% conversion**
  - When: You compare a membrane-reactor route with reactive distillation for butyl acetate.
  - Do: Prefer reactive distillation unless the membrane reactor can exceed about 95% conversion. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) state this threshold without showing a calculation.
  - Why: Unconverted butanol must be split from the ester in an energy-hungry column. Higher conversion shrinks that column.
  - Check: Redo the route comparison at the conversion your membrane can really reach.
  - Result: Return on investment 23.1% against 31.2%, payback 2.7 against 2.1 years (membrane route against reactive distillation).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 8, pp. 17-18 (Table 12); Section 9, p. 18. <!-- al-rabiah-2022.membrane-route-cost-set-by-column -->

- **Butyl acetate route: shortlist reactive distillation first, then a membrane reactor; the reactor with three columns came last**
  - When: You choose a route to n-butyl acetate from acetic acid and n-butanol. The reaction is limited by equilibrium and butanol forms an azeotrope with water.
  - Do: Shortlist reactive distillation (reaction and distillation in one column) and a membrane reactor against the conventional fixed-bed reactor with three columns. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) compared all three in Aspen Plus at equal capacity (92,500 t/a) and equal product purity.
  - Why: Doing reaction and separation together loses less conversion to equilibrium and needs fewer columns.
  - Check: Compare routes on the same capacity, purity, property method and cost basis. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) used NRTL and their own cost estimates (CEPCI 2021); all three routes are their simulations, not plant data.
  - Result: Reactive distillation first, the membrane reactor second, the conventional route last, on steam use, CO2 and cost.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Sections 7.1, 7.2 and 8, pp. 16-18 (Table 10, Figs. 18-19, Table 12). <!-- al-rabiah-2022.route-ranking-rd-mr-conventional -->

- **Inert in a gas recycle: the purge sets its level**
  - When: An inert builds up in a gas recycle loop.
  - Do: Size or adjust the purge to the inert concentration you want.
  - Why: Only the purge removes the inert.
  - Check: In CHEPTA, scan the purge fraction and record the inert concentration in the loop and the reactant lost with the purge.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 6, p. 230. <!-- larsson-skogestad-2000-plantwide.purge-sets-inert-level -->

- **After a 92% membrane reactor, one column and a small recycle are enough**
  - When: Unreacted reactants leave a butyl acetate membrane reactor at high conversion per pass.
  - Do: Use a single column that returns its distillate (about 9 kmol/h each of butanol and acid, with about 1 kmol/h each of ester and water) to the feed vessel.
  - Why: High conversion per pass leaves little to recycle.
  - Check: Compare your recycle with streams 3 and 5 of Table 4. Lab's comparison: about 9 kmol/h of each reactant per 100 kmol/h fresh feed, against about 43 in the conventional route.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 5, p. 7; Table 4, p. 9 (streams 3 and 5). <!-- al-rabiah-2022.membrane-route-single-column-recycle -->

- **An intermediate impurity builds up at column tops: recycle those distillates upstream, at an optimised rate**
  - When: An intermediate-boiling impurity (ethanol in the acetone-butanol-ethanol distillation of [Chen et al. 2018](https://doi.org/10.1186/s13068-018-1284-8)) accumulates at the tops of downstream columns.
  - Do: Recycle those distillates to the upstream column that removes the impurity, and optimise the recycle rate.
  - Why: The impurity has no exit unless it is returned to the column that can remove it. Too little recycle lets it into the product; too much costs energy.
  - Check: In CHEPTA, scan the recycle rate and record product purity and total duty.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Chen et al. 2018, *Novel distillation process for effective and stable…* (https://doi.org/10.1186/s13068-018-1284-8), Methods: 'Recycling the distillates'; Conclusions. <!-- chen-2018-abe-distillation.recycle-distillate-against-build-up -->

- **Build a flowsheet in Douglas's order**
  - When: You start a new flowsheet.
  - Do: Decide batch or continuous first, then the input-output structure, the recycle structure, the separation system and finally energy integration.
  - Why: Each level fixes what the next one needs.
  - Check: Before simulating, write down the decision taken at each level.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 5, p. 227. <!-- larsson-skogestad-2000-plantwide.douglas-hierarchy -->

- **Luyben's rule: fix one flow in each liquid recycle loop**
  - When: Recycle flows run away in a plant with liquid recycles.
  - Do: Fix one flow in each liquid recycle loop, as Luyben recommends (reported by [Larsson & Skogestad 2000](https://doi.org/10.4173/mic.2000.4.2)).
  - Why: A fixed flow stops disturbances circulating and avoids the snowball effect.
  - Check: [Larsson & Skogestad 2000](https://doi.org/10.4173/mic.2000.4.2) themselves dispute this: fixing the recycle flow carries an economic penalty (see their rule on keeping the reactor full).
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule disagrees with this one; both are kept.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Sections 5 and 6, pp. 228 and 230. <!-- larsson-skogestad-2000-plantwide.fix-a-recycle-flow -->

- **Liquid reactor in a recycle loop: keep it full rather than fixing the recycle flow**
  - When: You choose what to fix in a liquid-phase reactor-recycle loop.
  - Do: Keep the reactor hold-up at its maximum.
  - Why: Larger hold-up gives more conversion per pass and the smallest recycle; fixing the recycle flow instead costs money.
  - Check: For gas-phase loops [Larsson & Skogestad 2000](https://doi.org/10.4173/mic.2000.4.2) note that letting the hold-up (pressure) float can be optimal.
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule disagrees with this one; both are kept.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 6, p. 230. <!-- larsson-skogestad-2000-plantwide.keep-reactor-full -->

- **Design from the reactor outwards**
  - When: You start a flowsheet.
  - Do: Choose the reactor and catalyst first, then add the separations and recycles.
  - Why: The reactor effluent defines the separation problem: the reaction step sets the purity reached and how hard purification will be.
  - Check: Fix the reactor outlet composition before designing the separation train.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design and simulation'. <!-- pasha-2021-biodiesel-process-design.design-from-reactor-outwards -->

- **Ethylene carbonate route: recycle the CO2 released in hydrolysis back to carbonation**
  - When: Carbon dioxide is a reactant in carbonation and a product of the hydrolysis that follows.
  - Do: Separate the released CO2, compress it and recycle it to carbonation, with a small make-up for losses.
  - Why: Closing the loop leaves only the losses to replace.
  - Check: In CHEPTA, check the CO2 balance of the loop: make-up equals losses.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'Indirect hydration process', p. 7; 'MEG production via indirect EO hydration process', p. 8 (Fig. 6). <!-- shehata-2024-meg-routes.carbonate-route-co2-recycle -->
