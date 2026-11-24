# Separation choice and distillation design (generated; do not edit)

Which separation to use, column pressure, sequences, extraction, absorbers. 30 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Packed absorbers and strippers: size the diameter for 60-80% of flooding**
  - When: You size a packed absorber or stripper.
  - Do: Size the diameter for 60 to 80% of the flooding capacity, and the packed height from earlier studies or a height-to-diameter ratio.
  - Why: Too close to flooding loses operability; too far wastes column.
  - Check: Check the fractional capacity at your highest vapour and liquid loads.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': operation unit design. <!-- palomar-2024-il-process-simulation.packed-column-capacity -->

- **Regeneration under vacuum: count the vacuum compressor's energy**
  - When: A regeneration column runs under vacuum.
  - Do: Model the vacuum system as a compressor that returns the vapour to atmospheric pressure, and count its energy in the utilities.
  - Why: A vacuum system is a compressor; leaving it out makes vacuum operation look cheaper than it is.
  - Check: In CHEPTA, add a compressor on the vacuum column's vapour and include its work in the energy comparison.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': process modelling and simulations. <!-- palomar-2024-il-process-simulation.vacuum-energy-counted -->

- **Butyl acetate purity near 99 mol% is set by the acetic acid excess, not by the column**
  - When: You try to match the ester purity of the conventional or the membrane-reactor route.
  - Do: Match the purity through the acid slip: about 1 kmol/h acetic acid (the small acid excess of the fresh feed) leaves with about 100 kmol/h ester in the bottoms. Do not over-purify the column to reach it.
  - Why: The unconsumed acid excess has no other exit, so it ends in the bottoms with the ester.
  - Check: The purities 99.0 and 98.9 mol% are Lab's arithmetic on Tables 4 and 7; [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) state 99.0 mol% for the membrane route. Table 4's stream labels disagree with the text (stream 1 is called butanol but holds 101 kmol/h acid): check before transcribing.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 4, p. 9 (streams 1, 2, 6); Table 7, p. 14 (streams 1, 2, 6). <!-- al-rabiah-2022.acid-slip-sets-purity -->

- **Butanol and butyl acetate form an azeotrope at 101 kPa: split them at about 300 kPa**
  - When: Unreacted n-butanol must be separated from butyl acetate after the reactor, and the two form an azeotrope at atmospheric pressure.
  - Do: Run the column at about 300 kPa, where the split is possible, with ester as bottoms and unreacted butanol and acid overhead for recycle. Expect many stages: [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) used 42 stages, feed on stage 21, reboiler 5.2 MW.
  - Why: Raising the pressure moves the azeotrope away from the composition you need to cross.
  - Check: In CHEPTA, confirm the azeotrope at 101 kPa and that it has moved at 300 kPa before building the column. Table 4 of [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) prints the bottoms at 3.2 kPa against 284 kPa overhead, probably a misprint: check before transcribing.
  - Result: Ester at 99.0 mol% as bottoms.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 5, pp. 7-10 (Figs. 9-10, Tables 4-5). <!-- al-rabiah-2022.butanol-ester-split-at-pressure -->

- **Count column duties early: the three-column butyl acetate route needed about eight times the steam of reactive distillation**
  - When: You rank routes where low conversion and an azeotrope multiply the number of columns.
  - Do: Estimate each route's column duties early, before detailed design.
  - Why: More columns and more recycled material mean more liquid to boil.
  - Check: The ratios 8.3 (against reactive distillation) and 5.2 (against the membrane route) are Lab's arithmetic on Table 10 of [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801); the attribution to the columns is theirs.
  - Result: Medium-pressure steam 218,729 MWh/a for the conventional route.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 7.1, p. 16 (Table 10). <!-- al-rabiah-2022.conventional-steam-heavy -->

- **Do not design for a sharper split than the product needs**
  - When: The required purity is close to the feed composition.
  - Do: Set purities to what the product needs and accept a non-sharp split.
  - Why: Minimum reflux depends on the purity required; a sharp split costs much more reboiler duty.
  - Check: In CHEPTA, scan the purity specification and record the reboiler duty at each point.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.1, p. 304 (Fig. 4). <!-- blahusiak-2018-separation-selection.relax-purity -->

- **Choosing how to split two components: go by their relative volatility**
  - When: You must separate two components and know their relative volatility (alpha, how much more volatile one is than the other) at column conditions.
  - Do: Between about 1.3 and 10, use ordinary distillation. Consider a solvent to raise alpha only while alpha is below about 3. Below about 1.3, look at heat-pumped distillation or a solvent-based separation (extractive distillation or extraction) instead.
  - Why: Minimum reflux rises steeply as alpha falls towards one, so condenser and reboiler duties grow out of proportion.
  - Check: Work out alpha with the property method you will use, at both the top and the bottom of the column, since it changes along the column. In CHEPTA, flash the feed at column pressure and compare vapour and liquid compositions.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.1, p. 304 (Figs. 2-3). <!-- blahusiak-2018-separation-selection.volatility-ranges -->

- **Recover a used solvent or burn it: compare the recovery energy with the energy of making it**
  - When: You decide the fate of a waste solvent.
  - Do: Compare the energy of recovering it by distillation with the energy embodied in producing it. Tetrahydrofuran is worth recovering; diethyl ether is better incinerated.
  - Why: The energy needed to produce a solvent differs strongly between solvents.
  - Check: Estimate the recovery column's duty per kg of solvent and compare it with the production energy from a tool such as the ETH tool described by [Byrne et al. 2016](https://doi.org/10.1186/s40508-016-0051-z).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Byrne et al. 2016, *Tools and techniques for solvent selection* (https://doi.org/10.1186/s40508-016-0051-z), Recovery or incineration (ETH tool), p. 4. <!-- byrne-2016-solvent-selection-guides.recover-or-incinerate -->

- **Columns whose split improves at lower pressure: lower it, keeping the condenser above ambient**
  - When: Columns need high reflux and offer few heat-integration matches.
  - Do: Check each column's sensitivity to pressure. Lower the pressure where the split improves, but keep each condenser above ambient temperature.
  - Why: Lower pressure raises relative volatility and shifts column temperatures, which can widen the temperature differences for heat integration.
  - Check: In CHEPTA, scan the column pressure and record reflux, duties and condenser temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Chen et al. 2018, *Novel distillation process for effective and stable…* (https://doi.org/10.1186/s13068-018-1284-8), Methods: 'Decreasing the column pressure'. <!-- chen-2018-abe-distillation.lower-pressure-of-sensitive-columns -->

- **Sizing a dividing-wall column: optimise trays, reflux and both split ratios together**
  - When: You replace a two-column sequence for a sharp three-component split with a dividing-wall column.
  - Do: Optimise the number of trays, the reflux and the liquid and vapour split ratios (how flows divide either side of the wall) together.
  - Why: Fewer trays can match the split, but with too few the reflux rises steeply, and the split ratios set the internal flows.
  - Check: Scan trays and both split ratios and record reflux and duty at each point.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Conclusions, p. 165. <!-- henrique-2020-dwc-simulation.dwc-trays-reflux-splits -->

- **Three-component split: a prefractionator or dividing wall saves energy by avoiding remixing**
  - When: You separate a three-component mixture by distillation.
  - Do: Use a fully coupled (Petlyuk) arrangement, or its single-shell equivalent, a dividing-wall column, where the prefractionator does only a rough split.
  - Why: In a plain sequence the middle component is remixed, which wastes separation work; most of the coupled arrangement's saving comes from avoiding that.
  - Check: Compare the total duty with the best sequence of simple columns.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Introduction, p. 150. <!-- henrique-2020-dwc-simulation.prefractionator-avoids-remixing -->

- **Acetone, isopropanol and water: take acetone off first**
  - When: After the first concentration step you must split acetone, isopropanol and water.
  - Do: Use the direct sequence: take the most volatile product, acetone, as distillate of the first product column, and leave isopropanol and water for the azeotrope steps.
  - Why: Acetone is the lightest component and forms no azeotrope with the others (Table 1 of [Janković et al. 2023](https://doi.org/10.1002/jctb.7576)).
  - Check: In CHEPTA, confirm that the property method shows no acetone azeotrope with water or isopropanol before fixing the sequence.
  - Result: Acetone at 99.8 wt% with 100% recovery.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, pp. 719-720. <!-- jankovic-2023-ipa-acetone-recovery.acetone-first -->

- **Broth with live cells: make the first separation a vacuum distillation at fermentation temperature**
  - When: Products must be recovered from a very dilute fermentation broth whose microorganisms should survive and go back to the fermenter.
  - Do: Keep the first separation at the fermentation temperature (30 C) by vacuum distillation, with the condenser at about 0.03 bar. Return the bottoms, holding the cells and most of the water, to the fermenter. Alternative: pass-through distillation.
  - Why: Low pressure lowers the boiling temperature to what the cells tolerate.
  - Check: [Janković et al. 2023](https://doi.org/10.1002/jctb.7576) cite, but did not test, that microbes survive the vacuum. In CHEPTA, check that the bottoms temperature at your column pressure stays at 30 C or below.
  - Result: Products recovered; cells and water recycled.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Methods, p. 715; Results, Vacuum distillation, p. 717. <!-- jankovic-2023-ipa-acetone-recovery.cold-first-separation-for-live-cells -->

- **Products from broth with over 94 wt% water cost about 1.3-2.0 kWh per kg: use this as a sanity check**
  - When: You judge whether a recovery route for a dilute broth is viable.
  - Do: Use these figures as an order-of-magnitude check of your design's primary energy per kg product.
  - Why: Handling the water dominates the energy of dilute recovery.
  - Check: The figures are [Janković et al. 2023](https://doi.org/10.1002/jctb.7576)'s simulations with heat pumping and heat integration. A much higher value in your design suggests looking for missing heat recovery.
  - Result: Isopropanol and acetone at 1.3-2.0 kWh primary energy per kg product; the vacuum design stays under 2 or 3 kWh/kg at 2.5 or 1.2 wt% products.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Abstract, p. 714; Results, Sustainability metrics, p. 723 (Table 5). <!-- jankovic-2023-ipa-acetone-recovery.dilute-energy-scale -->

- **Very low column pressure puts the condenser below cooling-water temperature: chilled water, or pass-through distillation**
  - When: A vacuum column's condenser falls below cooling-water temperature (about 10 C at 0.032 bar in [Janković et al. 2023](https://doi.org/10.1002/jctb.7576)).
  - Do: Either pay for chilled water, or use pass-through distillation: absorb the vapour into lithium bromide brine and desorb it at higher pressure, where it condenses with cooling water.
  - Why: The absorbent loop separates evaporation at low pressure from condensation at higher pressure.
  - Check: Compare the condenser temperature at your pressure with the cooling-water supply temperature.
  - Result: With pass-through distillation, condensation at about 41 C and 0.2 bar.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Vacuum distillation, p. 717; Pass-through distillation, p. 718. <!-- jankovic-2023-ipa-acetone-recovery.vacuum-condenser-needs-chilled-water -->

- **Classic sequencing rule: leave the hardest split to last**
  - When: You choose the order of splits in a distillation sequence.
  - Do: Leave the most difficult split to last.
  - Why: A difficult split needs a high reflux ratio, which is cheaper with fewer components present.
  - Check: [Li et al. 2023](https://doi.org/10.1016/j.seppur.2023.123717) report this classic rule and then qualify it: compare sequences quantitatively.
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule disagrees with this one; both are kept.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Section 2, p. 5. <!-- li-2023-distillation-sequences.hardest-split-last -->

- **The hardest split can also pay early: compare sequences by optimisation**
  - When: You choose the order of splits in a distillation sequence.
  - Do: Compare sequences quantitatively, by optimisation, rather than by a fixed rule.
  - Why: Two effects oppose: the high reflux of a difficult split, and the non-key components present during it, which inflate the column flows. [Li et al. 2023](https://doi.org/10.1016/j.seppur.2023.123717) find the balance depends on the case.
  - Check: Screen with shortcut models plus heat integration, then simulate the best few rigorously.
  - Status: lead — from the literature, not yet tested by Lab.
  - Another rule disagrees with this one; both are kept.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Section 2, p. 5. <!-- li-2023-distillation-sequences.hardest-split-not-always-last -->

- **Choose column pressure so the condenser can use cooling water**
  - When: A column's condenser temperature would need refrigeration.
  - Do: Raise the column pressure until the condenser can use cooling water, and set it together with the heat integration.
  - Why: Higher pressure raises the condensing temperature.
  - Check: In CHEPTA, scan the pressure and record condenser and reboiler temperatures against your utilities.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Section 2, p. 5. <!-- li-2023-distillation-sequences.pressure-for-cooling-water -->

- **Many sequences to compare: screen with shortcut models and heat integration, simulate only the best few**
  - When: There are too many distillation sequences to simulate rigorously.
  - Do: Screen with shortcut column models (Fenske-Underwood-Gilliland) combined with heat-exchanger network synthesis, and simulate only the best few rigorously.
  - Why: For zeotropic mixtures (no azeotropes) shortcuts rank sequences as rigorous models do.
  - Check: [Li et al. 2023](https://doi.org/10.1016/j.seppur.2023.123717) showed this for zeotropic hydrocarbons only: do not rely on it for azeotropic mixtures without a rigorous check.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Abstract, p. 1; Conclusions, p. 14. <!-- li-2023-distillation-sequences.shortcut-screening -->

- **Ethylene glycol via ethylene carbonate: far fewer heavy glycols and less water than direct hydration**
  - When: Direct hydration forces a large water excess and makes heavy glycols.
  - Do: Consider routing through ethylene carbonate; its hydrolysis needs water close to stoichiometric.
  - Why: The carbonate intermediate hydrolyses selectively with little water, so purification needs less water removal and simpler heavy-glycol handling.
  - Check: These are simulation numbers without an evidence row in Lab: check them against the stream tables before reuse.
  - Result: Heavy glycols 1,532 against 22,270 t/a in [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y)'s simulations.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'Indirect hydration process', p. 6; 'MEG production via indirect EO hydration process', p. 9. <!-- shehata-2024-meg-routes.carbonate-route-fewer-heavy-glycols -->

- **Glycol columns under vacuum, so the bottoms stay below about 170 C**
  - When: Glycol would degrade at the temperatures of atmospheric distillation.
  - Do: Run the dehydration and product columns under vacuum so the bottoms stay below the degradation temperature (170 C in [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y)). Draw the product glycol from the side; heavier glycols leave at the bottom.
  - Why: Lower pressure lowers the boiling temperatures.
  - Check: In CHEPTA, check the reboiler temperature at the chosen pressure.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'MEG production via direct EO hydration process', p. 8. <!-- shehata-2024-meg-routes.vacuum-glycol-columns -->

- **Acetic acid from water: use a solvent-based separation, with water leaving at the top**
  - When: You recover acetic acid from water.
  - Do: Prefer extraction or a solvent-based distillation (extractive or azeotropic). In either distillation water leaves at the top, because the acid is the heavy component.
  - Why: Acetic acid and water have a low relative volatility and a tangent pinch (the equilibrium curve nearly touches the diagonal) at high acid purity, so plain distillation is costly.
  - Check: In CHEPTA, tabulate the acid-water equilibrium at high acid purity to see the pinch, using vapour association for the acid where the method offers it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 3.4, p. 316. <!-- blahusiak-2018-separation-selection.acetic-acid-water-solvent-based -->

- **One component dilute in a large stream: try extraction or extractive distillation before plain distillation**
  - When: The feed is strongly asymmetric: the component you want is dilute in a large stream.
  - Do: Consider an affinity separation (one using a solvent's preference for a component), liquid-liquid extraction or extractive distillation, before plain distillation.
  - Why: Distillation must vaporise the bulk, so its internal efficiency is low on such feeds.
  - Check: Compare the reboiler duty per kg of recovered component with the energy of the extraction route.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.1, p. 304; Conclusions, p. 317. <!-- blahusiak-2018-separation-selection.avoid-distillation-for-dilute-feeds -->

- **Light solvent for acetic acid extraction, such as ethyl acetate: it takes water along, but the water splits out on cooling**
  - When: You extract acetic acid from water with a low-boiling solvent such as ethyl acetate.
  - Do: Expect much co-extracted water, and use the solvent-water heterogeneous azeotrope (one that separates into two liquids) in a decanter during solvent regeneration.
  - Why: The azeotrope splits into a solvent phase and a water phase on cooling, so less has to be boiled.
  - Check: In CHEPTA, set phases: "VLL" on the regeneration decanter and check that the condensed overhead splits into two liquids.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 3.4, p. 316 (Fig. 20). <!-- blahusiak-2018-separation-selection.low-boiling-solvent-coextracts-water -->

- **Need an ether solvent: use 2-methyltetrahydrofuran or tert-butyl methyl ether**
  - When: A process needs an ether solvent and tetrahydrofuran or diethyl ether are candidates.
  - Do: Use 2-methyltetrahydrofuran or tert-butyl methyl ether instead of tetrahydrofuran and diethyl ether.
  - Why: Safer ethers exist that do a similar job ([Byrne et al. 2016](https://doi.org/10.1186/s40508-016-0051-z)).
  - Check: Check with the property method that the substitute gives the solubility and phase behaviour you need.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Byrne et al. 2016, *Tools and techniques for solvent selection* (https://doi.org/10.1186/s40508-016-0051-z), Unified guides, p. 9. <!-- byrne-2016-solvent-selection-guides.ether-substitutes -->

- **Choosing a solvent or entrainer: start from the green list of the pharmaceutical guides**
  - When: You choose a solvent or entrainer and want to avoid health, safety and environmental problems.
  - Do: Prefer solvents rated green across the Pfizer, GSK and Sanofi guides: water, n-propyl and isopropyl acetate, 1- and 2-butanol. Justify any undesirable one: chlorinated solvents, NMP, DMF and DMAc (polar aprotic solvents), benzene, hexane, 1,4-dioxane, diethyl ether.
  - Why: The solvents' health, safety and environmental ratings differ widely.
  - Check: NMP and DMF, rated undesirable here, are the extractive solvents studied in [Li et al. 2017](https://doi.org/10.1038/s41598-017-09088-2): report the trade-off if a case uses them.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Byrne et al. 2016, *Tools and techniques for solvent selection* (https://doi.org/10.1186/s40508-016-0051-z), Unified guides, pp. 8-9 (Figs. 6-7). <!-- byrne-2016-solvent-selection-guides.green-and-undesirable-solvents -->

- **Alcohol from water: add a salting-out salt such as potassium carbonate before distillation**
  - When: You recover an alcohol (isobutanol in [Fu et al. 2021](https://doi.org/10.1002/elsc.202000090)) from water.
  - Do: Add a strong salting-out salt (one that pushes organics out of water), such as potassium carbonate, then distil.
  - Why: The ions bind water and push the alcohol out; the salt stays in the aqueous phase.
  - Check: This needs an electrolyte property model: check that one is available before planning the case.
  - Result: Higher alcohol partition and dehydration, and less energy than solvent extraction.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Fu et al. 2021, *Assessment of extraction options for a next-generation…* (https://doi.org/10.1002/elsc.202000090), Concluding remarks. <!-- fu-2021-isobutanol-recovery.salting-out -->

- **Mixed extractants: choose boiling points so regeneration needs no extra column**
  - When: You regenerate a mixture of extractants after liquid-liquid extraction.
  - Do: Pick extractants whose boiling points let regeneration take each one overhead or at the bottom without an extra column.
  - Why: The boiling order fixes the regeneration sequence.
  - Check: List the boiling points of products and extractants and draw the regeneration sequence before simulating.
  - Result: A heavier biocompatible extractant cut the regeneration section from three columns to two ([Grisales Díaz & Olivar Tost 2017](https://doi.org/10.1186/s40643-017-0142-z)).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Grisales Díaz & Olivar Tost 2017, *Techno-economic analysis of extraction-based separation systems for…* (https://doi.org/10.1186/s40643-017-0142-z), Methods: 'Extractant selection'. <!-- grisales-2017-abe-extraction.extractant-boiling-for-fewer-columns -->

- **Dilute product stream: its concentration sets the energy per kg**
  - When: You recover a product from a dilute stream and the energy per kg is high.
  - Do: Raise the product concentration fed to separation (the upstream yield) where possible, before optimising the separation.
  - Why: Energy scales with the solvent or water handled per unit of product.
  - Check: Plot energy per kg product against feed concentration in your simulation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Grisales Díaz & Olivar Tost 2017, *Techno-economic analysis of extraction-based separation systems for…* (https://doi.org/10.1186/s40643-017-0142-z), Conclusions. <!-- grisales-2017-abe-extraction.feed-concentration-dominates -->

- **Broth with dissolved CO2: degas it first and recapture any product it strips**
  - When: The fermentation broth holds dissolved CO2 and goes to a vacuum recovery train.
  - Do: Add a degassing step under reduced pressure first, and recover any product it strips with water in a small stripping column.
  - Why: Gas that does not condense would load the vacuum system and the condensers.
  - Check: [Janković et al. 2023](https://doi.org/10.1002/jctb.7576) propose this without simulating it. Measure the gas in your feed and the product lost with it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Full recovery processes, p. 721. <!-- jankovic-2023-ipa-acetone-recovery.degas-before-recovery -->
