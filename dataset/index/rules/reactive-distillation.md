# Reactive distillation and esterification (generated; do not edit)

Reaction and separation in one unit: feasibility, column design, catalysts, water-removing membranes. 29 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Excess acetic acid raises butanol conversion but makes the ester harder to purify: stay near 1:1**
  - When: You choose the acetic acid to n-butanol feed ratio of a butyl acetate reactor.
  - Do: Keep the feed near stoichiometric, as [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) did (1:1), unless the extra conversion is worth a harder product column.
  - Why: An excess of one reactant pushes the equilibrium further, but the excess must be removed from the product downstream.
  - Check: Scan the feed ratio and watch both conversion and the acid left in the ester. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) state the trade-off in words only, without a purification cost.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 4, p. 6 (Fig. 5b); Table 3, p. 8. <!-- al-rabiah-2022.acid-excess-raises-conversion-hurts-purification -->

- **Membrane reactor solved outside the simulator: treat its outlet as an input, not a result**
  - When: A source solved one unit in another program and fed its outlet to the flowsheet. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) did this for the membrane reactor (an ODE model, ordinary differential equations, in MATLAB, with water flux proportional to its concentration).
  - Do: Declare that outlet as an imposed boundary of the case. Compare only what the flowsheet itself computed.
  - Why: The flowsheet simulator never calculated that unit, so matching its outlet proves nothing about the simulation.
  - Check: List the imposed streams in the case and keep them out of the comparison table. This is Lab's rule for case boundaries, not one of [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 3, pp. 3-4 (Eqs. 7-12); Section 4, p. 7. <!-- al-rabiah-2022.membrane-reactor-model-imposed -->

- **Butyl acetate reactor stuck near 70% conversion: take the water out through a membrane**
  - When: n-Butanol and acetic acid react over Amberlyst-15 (an acidic ion-exchange resin) at 363 K with a 1:1 feed, and a plain fixed bed stops at about 70% butanol conversion.
  - Do: Fit the reactor with a water-selective hydroxy sodalite membrane (a zeolite membrane that lets water through) so water leaves as it forms. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) took organic losses through the membrane as negligible.
  - Why: Water is a product of the reaction; removing it shifts the equilibrium towards the ester.
  - Check: [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) solved the membrane reactor outside Aspen Plus (in MATLAB). In a Lab case take its outlet as an imposed input, not as a reproduced result, and compare the downstream column with their stream table.
  - Result: Butanol conversion rose from about 70% to 92% in their model, which is fitted to one laboratory study (R2 0.9973), not to an industrial membrane.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Sections 3-5, pp. 3-7 (Eqs. 7-12, Tables 1-3, Figs. 5a and 7); Abstract, p. 1. <!-- al-rabiah-2022.membrane-reactor-removes-water -->

- **Water-removal membrane in hot acid service: prefer zeolite-coated ceramic to polymer**
  - When: You choose a water-removal membrane for a hot reactive esterification mixture.
  - Do: Prefer zeolite-coated ceramic membranes (LTA or MFI type) to polymer films. Ceramic membranes can crack at large scale (Section 8.1).
  - Why: Inorganic supports resist swelling and chemical attack.
  - Check: Ask for long-term permeability data: a polyvinyl alcohol membrane is reported to lose up to 35% of its permeability in 1000 h.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Sections 5.1 and 8.1. <!-- hoff-eisenacher-2025-esterification-review.ceramic-vs-polymer-membranes -->

- **Esterification at equilibrium: remove water continuously, by reactive distillation or a membrane**
  - When: Esterification stops at equilibrium.
  - Do: Integrate water removal with the reaction: reactive distillation, or a pervaporation (membrane evaporation) or nanofiltration membrane in the reactor.
  - Why: Removing a product shifts the equilibrium, so conversion rises at milder conditions.
  - Check: Compare conversion with and without water removal in an equilibrium model.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Abstract; Sections 4.1 and 5. <!-- hoff-eisenacher-2025-esterification-review.water-removal-shifts-equilibrium -->

- **The purity target can change the best dehydration technology**
  - When: You choose a dehydration technology (for isobutanol, in a study cited by [Valentini & Vaccaro 2020](https://doi.org/10.3390/molecules25225264)).
  - Do: Compare the technologies at the actual purity target.
  - Why: Membrane area and distillation duty scale differently with purity.
  - Check: Rerun the comparison at your own purity.
  - Result: At 98.8 wt% isobutanol pervaporation ranked above azeotropic distillation; at 99.9 wt% distillation-assisted pervaporation with heat integration was clearly best (a cited result, not read by Lab).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.4. <!-- valentini-2020-azeotropes-waste.purity-decides-pervaporation -->

- **Reactive distillation for butyl acetate: acid fed above butanol, catalyst in the middle, ester out at the bottom**
  - When: You design a reactive column for acetic acid and n-butanol over Amberlyst-15 with a 1:1 feed.
  - Do: Use a two-feed column with a reactive middle section. [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801): 34 stages, catalyst on stages 5-24, acetic acid on stage 5 above butanol on stage 9, 100 kmol/h of each, reboiler 3.3 MW.
  - Why: Water leaves overhead as it forms and ester leaves at the bottom, so the reaction keeps moving past its equilibrium.
  - Check: The bottoms in Table 9 (97.2 kmol/h ester, 1.1 butanol) is 98.9 mol% or 99.3 mass % by Lab's arithmetic; the text says more than 99% without a basis. Catalyst hold-up per stage and the pressure profile are not printed, so expect to choose them.
  - Result: Conversion over 98%, ester as bottoms.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.2, pp. 13-15 (Table 8, Fig. 16). <!-- al-rabiah-2022.rd-column-configuration -->

- **Reactive distillation was the cheapest butyl acetate route, but it is harder to design and operate**
  - When: You choose between intensified butyl acetate routes.
  - Do: Prefer reactive distillation with a decanter on cost and energy, and plan for its more complex design and operation, which [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) point out.
  - Why: One unit does both the reaction and the separation.
  - Check: The costs are [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801)'s Aspen estimates (total capital USD 6,742,000 against 7,552,000, Table 12); compare on your own cost basis.
  - Result: Steam 26,388 MWh/a, capital 6.7 million USD against 7.6 million for the membrane route, payback 2.1 years.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 1, p. 2; Section 7.1, p. 16 (Table 10); Section 8, p. 18 (Table 12). <!-- al-rabiah-2022.rd-lower-capex-and-energy -->

- **Butyl acetate yield can rise from about 70% to 95% when water is removed during reaction**
  - When: Butyl acetate yield is limited by equilibrium.
  - Do: Remove water during the esterification.
  - Why: Water removal shifts the equilibrium towards the ester.
  - Check: [Hoff & Eisenacher 2025](https://doi.org/10.3390/ijms26157214) report this in one sentence from a cited study with acidic ionic-liquid catalysts, not read by Lab: treat it as an indication.
  - Result: Yields from about 70% up to 95%.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Section 6.1 (citing ref. 174). <!-- hoff-eisenacher-2025-esterification-review.butyl-acetate-yield-with-water-removal -->

- **Acid resin catalyst: its temperature limit sets the reactive zone's temperature and pressure**
  - When: You choose an ion-exchange resin catalyst for esterification, for example in reactive distillation.
  - Do: Choose the resin by its maximum service temperature: about 140 C for Amberlyst 15 and up to 190 C for Amberlyst 70, per [Hoff & Eisenacher 2025](https://doi.org/10.3390/ijms26157214). Set the column pressure so the reactive zone stays below it.
  - Why: Resins lose their acid groups when too hot.
  - Check: In CHEPTA, check the reactive stages' temperatures against the resin's limit.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Hoff & Eisenacher 2025, *Process Intensification Strategies for Esterification* (https://doi.org/10.3390/ijms26157214), Section 2.2.1 (Table 2). <!-- hoff-eisenacher-2025-esterification-review.resin-temperature-limit -->

- **First design of a reactive column: reactive zone where reactants are richest, shortcut the rest**
  - When: You need a starting design for a reactive distillation column.
  - Do: Put the reactive zone where reactant concentrations are highest. Estimate the non-reactive stages with Fenske-type shortcuts (minimum-stage equations), and the reactive stages as the reactive height divided by the catalytic packing's HETP (height equivalent to a theoretical plate).
  - Why: Conventional shortcuts give the separating sections; the catalytic packing sets the reactive height.
  - Check: Simulate the first design rigorously and adjust it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal p. 1268 (p. 7 of the TU Delft copy; guidelines of Subawalla and Fair). <!-- kiss-2024-rd-conceptual-methods.first-sizing -->

- **Reactive column with a large heat of reaction: plan energy integration between its sections**
  - When: The reaction on the reactive stages releases or absorbs much heat.
  - Do: Integrate energy between the reactive and separating sections. For slow, strongly endothermic reactions with small equilibrium constants, also integrate mass with the stripping section. For thermally neutral reactions mass integration alone is enough.
  - Why: Heat released or absorbed on the reactive stages changes the column's vapour and liquid flows.
  - Check: In CHEPTA, compare the vapour and liquid flow profiles with and without reaction.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Synthesis procedures, journal p. 1277 (p. 16 of the TU Delft copy; procedure of Huang et al.). <!-- kiss-2024-rd-conceptual-methods.heat-effect-integration -->

- **Place the reactive section so distillation carries a product away**
  - When: A reactive column is limited by equilibrium, or an azeotrope can form.
  - Do: Locate the reactive section so distillation removes a reaction product from the liquid and, where azeotropes exist, so the reaction consumes a component before its azeotrope can form.
  - Why: Removing a product shifts the equilibrium; consuming a component avoids its azeotrope.
  - Check: In CHEPTA, compare conversion and stage compositions for a few positions of the reactive zone.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal p. 1270 (p. 9 of the TU Delft copy). <!-- kiss-2024-rd-conceptual-methods.locate-reactive-section -->

- **Reactive column feeds: run neat with tight ratio control, or with 10-20% excess and a recovery column**
  - When: You set the reactant ratio of a reactive column.
  - Do: Either run neat (stoichiometric feeds) in one column, which is cheaper but needs precise balancing of the fresh feeds, or use 10 to 20% excess of one reactant with a recovery column for it.
  - Why: Any excess reactant must leave somewhere; in neat operation a small imbalance builds up in the column.
  - Check: In CHEPTA, offset the feed ratio slightly and watch whether a reactant accumulates in the column or the recycle.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal pp. 1270 and 1278 (pp. 9 and 17 of the TU Delft copy; after Luyben and Yu). <!-- kiss-2024-rd-conceptual-methods.neat-versus-excess-feed -->

- **Reactive distillation only works where the reaction, catalyst and separation windows overlap**
  - When: You consider combining a reaction and its separation in one column.
  - Do: Check that the temperature and pressure windows of the reaction, the catalyst and the separation overlap. If they do not, keep reactor and column separate, and judge integration on the whole process.
  - Why: One column imposes one pressure and a temperature profile on all three.
  - Check: Compare the column's stage temperatures at the chosen pressure with the catalyst's limit and the reaction's useful range.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal p. 1268 (p. 7 of the TU Delft copy). <!-- kiss-2024-rd-conceptual-methods.overlapping-windows -->

- **Too much reaction asked of the column: add a pre-reactor**
  - When: The reactive column has to deliver a large share of the conversion.
  - Do: Add a pre-reactor upstream to take part of the conversion. Find the best split between them by costing designs over a range of pre-reactor temperatures.
  - Why: An upstream reactor reaches equilibrium cheaply and leaves a smaller reactive section.
  - Check: Cost several pre-reactor temperatures and keep the cheapest.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal p. 1275 (p. 14 of the TU Delft copy; after Daniel and Jobson). <!-- kiss-2024-rd-conceptual-methods.pre-reactor -->

- **Reaction too slow on the reactive stages: raise the column pressure**
  - When: The reaction is too slow at the reactive column's temperatures.
  - Do: Raise the column pressure so the stages run hotter and the reaction faster, as long as the separation and the catalyst still allow it.
  - Why: Pressure sets the stage temperatures.
  - Check: In CHEPTA, scan the column pressure and check the reactive-zone temperatures against the catalyst limit, and the key relative volatility.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal p. 1269 (p. 8 of the TU Delft copy). <!-- kiss-2024-rd-conceptual-methods.raise-pressure-for-slow-reaction -->

- **Slow reaction: no reactive distillation; very easy separation: reactor plus flash**
  - When: You choose between a reactor followed by a separator and a reactive column.
  - Do: Place the system on a rate-against-volatility chart (the Schoenmakers diagram). A slow reaction makes reactive distillation unattractive; a very high relative volatility needs only a reactor and a flash. In between, reactive distillation is a candidate.
  - Why: Reaction rate and volatility decide whether extra stages help.
  - Check: The chart's axes are not quantified and [Kiss et al. 2024](https://doi.org/10.1002/jctb.7633) warn that it needs experience: confirm the choice with a simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Heuristic approaches, journal pp. 1268-1269 (pp. 7-8 of the TU Delft copy, Fig. 2). <!-- kiss-2024-rd-conceptual-methods.rate-versus-volatility -->

- **Reactive trays hold 10-15 cm of liquid: if you need more hold-up, add trays or widen the column**
  - When: The catalyst hold-up the reaction needs exceeds what a tray can hold.
  - Do: Keep the tray liquid height near 10 to 15 cm. If the needed hold-up implies more, add reactive trays or make the column wider than vapour loading requires.
  - Why: More liquid on a tray raises the pressure drop; tray hydraulics limit the liquid height.
  - Check: Divide the required hold-up per stage by the tray area to get the liquid height.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kiss et al. 2024, *Conceptual methods for synthesis of reactive distillation…* (https://doi.org/10.1002/jctb.7633), Journal p. 1274 (p. 13 of the TU Delft copy; after Luyben and Yu). <!-- kiss-2024-rd-conceptual-methods.tray-liquid-height -->

- **Reactive column: stay away from both minimum stages and minimum reflux**
  - When: You choose the stage count and reflux of a reactive column and catalyst cost matters.
  - Do: Choose a configuration between the two limits.
  - Why: Near minimum stages the column is short and wide, near minimum reflux tall and slim. Catalyst volume follows diameter and reactive height, and is lowest in between.
  - Check: Compute the catalyst volume at a few points along the stages-reflux curve.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.2, p. 270 (Fig. 8). <!-- muthia-2018-rd-applicability.avoid-extreme-configurations -->

- **Slow reaction in a reactive column: size the catalyst hold-up so Da/K is at least 2 to 5**
  - When: The reaction is kinetically limited and may need more reactive stages.
  - Do: Size catalyst hold-up and residence time so the Damkohler number (reaction rate relative to flow rate) divided by the equilibrium constant is at least 2 to 5.
  - Why: With enough hold-up the reaction behaves as at equilibrium: at Da/K of 5 or more the configuration equals the equilibrium one, at 2 or more it is within 10%.
  - Check: Compute Da/K from your kinetics, hold-up and feed rate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.2, p. 270 (Fig. 7; Fig. S5). <!-- muthia-2018-rd-applicability.da-over-keq-rule -->

- **Small equilibrium constant: expect more reactive stages and higher reflux**
  - When: The reaction's equilibrium constant is small.
  - Do: Allow more reactive stages and a higher reflux ratio.
  - Why: The products must be removed more completely on each stage.
  - Check: Compare your stage count and reflux with the map for your equilibrium constant.
  - Result: In the base case of [Muthia et al. 2018](https://doi.org/10.1016/j.cep.2018.04.001), at K = 0.01 the minimum is 22 stages and the minimum reflux ratio 11.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.1.2, p. 269 (Fig. 6). <!-- muthia-2018-rd-applicability.low-keq-more-stages-reflux -->

- **Light product close in volatility to a reactant: the feasible region shrinks**
  - When: The light product is hard to separate from a reactant.
  - Do: Check the product-reactant relative volatilities first.
  - Why: The reactant leaves with the product unless the separation is sharp.
  - Check: Compute the light product's relative volatility against each reactant with your property method.
  - Result: At K = 0.01, a relative volatility of 1.2 instead of 2 raised the reactive stages needed from 28 to 64.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 3.1.3, p. 269 (Fig. 6). <!-- muthia-2018-rd-applicability.product-reactant-volatility -->

- **Go or no-go on reactive distillation from three inputs: volatilities, equilibrium constant, kinetics**
  - When: You decide early whether reactive distillation is worth a rigorous study, for a reaction A + B to C + D with C the lightest and D the heaviest component.
  - Do: Read the relative volatilities, the equilibrium constant and the kinetics against the applicability maps of [Muthia et al. 2018](https://doi.org/10.1016/j.cep.2018.04.001) (reflux ratio against stages) before any rigorous simulation.
  - Why: Generic maps for this reaction class show where a feasible column exists.
  - Check: The maps are about +/-30% for real systems: confirm a go with a rigorous simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Muthia et al. 2018, *Novel method for mapping the applicability of…* (https://doi.org/10.1016/j.cep.2018.04.001), Section 2, pp. 264-266; Conclusions, p. 274. <!-- muthia-2018-rd-applicability.rd-map-needs-three-parameters -->

- **Butyl acetate reactive still: butanol runs short while acid and water stay in the liquid**
  - When: Reactants deplete unevenly in the liquid of an acetic acid and butanol reaction over a resin.
  - Do: Account for the acid and water held in the catalyst when you set the feed ratio.
  - Why: Water and acetic acid are fully miscible and both bind to the resin; butanol and the ester instead form two liquid phases with water.
  - Check: Compare the liquid reactant ratio with the fed ratio in your test or simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Orjuela et al. 2006, *Constructing residue curve maps for butyl acetate…* (https://doi.org/10.15446/ing.investig.v26n3.14745), Results, p. 30 (Fig. 3). <!-- orjuela-2006-butyl-acetate-rcm.acid-water-retained-butanol-depleted -->

- **Find the catalyst load where the reaction reaches equilibrium: raise it until the residue curves stop moving**
  - When: You do not know whether kinetics or equilibrium governs a reactive distillation.
  - Do: Scan the catalyst load in reactive residue-curve tests and increase it until the curves no longer change.
  - Why: At high catalyst load the reaction keeps pace with vaporisation, which marks the chemical-equilibrium regime.
  - Check: Treat the found load as the lowest at which a design may assume equilibrium.
  - Result: For this resin about 8 g, near 0.8 wt% sulfuric-acid equivalent ([Orjuela et al. 2006](https://doi.org/10.15446/ing.investig.v26n3.14745)).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Orjuela et al. 2006, *Constructing residue curve maps for butyl acetate…* (https://doi.org/10.15446/ing.investig.v26n3.14745), Results, p. 33 (Fig. 4, Table 3). <!-- orjuela-2006-butyl-acetate-rcm.catalyst-load-equilibrium-regime -->

- **Butyl acetate reactive column: the ester can be taken pure as bottom product**
  - When: Esterification of acetic acid with 1-butanol over an acid resin stops at equilibrium in a reactor.
  - Do: Use reactive distillation with butyl acetate as the bottom product.
  - Why: Water and the other light products are removed continuously, which drives the reaction on; the ester is the heaviest component, so the residue curves run towards it.
  - Check: [Orjuela et al. 2006](https://doi.org/10.15446/ing.investig.v26n3.14745) measured this in a laboratory batch still at 560 mmHg, not a continuous column: confirm it in a column simulation.
  - Result: Measured reactive residue curves (paths of a boiling, reacting liquid) end at butyl acetate, beyond the equilibrium conversion.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Orjuela et al. 2006, *Constructing residue curve maps for butyl acetate…* (https://doi.org/10.15446/ing.investig.v26n3.14745), Abstract, p. 26; Results, pp. 32-33 (Figs. 4-5). <!-- orjuela-2006-butyl-acetate-rcm.reactive-rcm-ester-in-bottoms -->

- **Ethylene oxide hydration in a reactive column: less diethylene glycol and less steam**
  - When: Ethylene oxide is hydrated to ethylene glycol, heavy glycols form when oxide meets glycol, and removing the water costs steam.
  - Do: Hydrate in a reactive distillation column, without catalyst.
  - Why: The volatile oxide stays dilute in the liquid on the reactive stages, which limits diethylene glycol, and the reaction heat helps boil off the water.
  - Check: In CHEPTA, compare the oxide concentration on the reactive stages and the diethylene glycol made with a tubular-reactor case.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Introduction, p. 3; Results, pp. 7-9. <!-- othman-2024-meg-reactive-distillation.rd-keeps-oxide-dilute -->

- **Reactive glycol column: feed the recycled water above the oxide**
  - When: Volatile ethylene oxide could escape overhead from the reactive column.
  - Do: Feed the recycled process water near the top (stage 2) and the aqueous oxide a little lower (stage 4).
  - Why: The water above the oxide feed catches and reacts with the rising oxide vapour before it reaches the condenser.
  - Check: In CHEPTA, check the oxide in the condenser vapour for a few feed locations.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Results, pp. 7-8 (Table 3, Fig. 10). <!-- othman-2024-meg-reactive-distillation.rd-water-fed-above-oxide -->
