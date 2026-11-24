# Heat integration (generated; do not edit)

Pinch analysis, heat pumps, vapour recompression, using process heat. 15 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Include reboilers and condensers in the pinch analysis, and keep each column on one side of the pinch**
  - When: You run a pinch analysis (heat-recovery targeting) on a plant with columns.
  - Do: Include every reboiler and condenser in the stream data. Place each column entirely above or entirely below the pinch (the temperature where heat recovery is tightest).
  - Why: A column that straddles the pinch moves heat across it.
  - Check: Plot each column's reboiler and condenser temperatures against the pinch temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Pinch analysis of the full system, p. 15. <!-- ali-2022-eg-plant-pinch.columns-in-pinch-analysis -->

- **Steam turbine or other heat engine: let it reject its heat below the pinch**
  - When: You integrate a heat engine such as a steam turbine into the plant's heat network.
  - Do: Position it with the grand composite curve (net heat flow against temperature) so that it rejects heat below the pinch.
  - Why: Heat rejected below the pinch replaces heat that would otherwise go to cooling.
  - Check: Check on the grand composite curve that the engine's exhaust temperature lies below the pinch.
  - Result: About another 6% less external cooling in [Ali et al. 2022](https://doi.org/10.2478/pjct-2022-0009)'s plant.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Conclusion, p. 19 (grand composite curve). <!-- ali-2022-eg-plant-pinch.heat-engine-below-pinch -->

- **Ethylene glycol plant: use the ethylene oxide reactor's surplus heat in the glycol section**
  - When: One section exports heat (the exothermic ethylene oxidation) while another imports it (glycol dehydration and separation).
  - Do: Heat-integrate the reaction section with the glycol section.
  - Why: Matching a heat source with a heat sink replaces external utilities on both sides.
  - Check: Run a pinch analysis (heat-recovery targeting) on the whole plant, columns included, to get the targets.
  - Result: In [Ali et al. 2022](https://doi.org/10.2478/pjct-2022-0009)'s plant the retrofit targets cut external heating by about 93% and cooling by about 45%.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Conclusion, p. 19. <!-- ali-2022-eg-plant-pinch.integrate-eo-reactor-with-glycol-section -->

- **Never move heat across the pinch**
  - When: You design the heat exchanger network after a pinch analysis.
  - Do: Never transfer heat across the pinch. At the pinch, match streams so the hot stream's heat-capacity flow (mass flow times heat capacity) is no larger than the cold stream's above the pinch and no smaller below it.
  - Why: Heat moved across the pinch must be supplied again as hot utility and removed again as cold utility, so it costs twice.
  - Check: Compare the network's utility use with the pinch targets; any excess points to a match across the pinch.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Ali et al. 2022, *Retrofitting Heat Exchanger Network of Industrial Ethylene…* (https://doi.org/10.2478/pjct-2022-0009), Heat exchanger network rules, p. 16. <!-- ali-2022-eg-plant-pinch.no-transfer-across-pinch -->

- **Heat pump on a column: worth it when reboiler duty is above about 10 times the compressor work**
  - When: You consider vapour recompression for a column.
  - Do: Divide the reboiler duty by the compressor work. Above about 10 a heat pump pays; below about 5 it does not.
  - Why: Compressor work grows with the temperature lift, so heat pumps suit close-boiling columns with a small top-to-bottom temperature difference.
  - Check: Estimate the compressor work from the condenser and reboiler temperatures before adding the heat pump.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Heat pumps, p. 313 (Fig. 15). <!-- blahusiak-2018-separation-selection.heat-pump-criterion -->

- **Dilute recovery: minimise external energy first, then check the cost**
  - When: You set the design objective early for recovering products from a dilute broth.
  - Do: Minimise external energy as the design objective, then check the costs.
  - Why: Operating cost, mostly energy, outweighs capital except for very short payback periods ([Janković et al. 2023](https://doi.org/10.1002/jctb.7576)).
  - Check: Confirm with a cost estimate that capital stays the smaller share at your payback period.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Methods, p. 715. <!-- jankovic-2023-ipa-acetone-recovery.minimise-energy-as-cost-proxy -->

- **Column with a small temperature lift and a big reboiler: use mechanical vapour recompression**
  - When: A column's top and bottom temperatures are close and its reboiler duty is large (about 22 MW for the vacuum column of [Janković et al. 2023](https://doi.org/10.1002/jctb.7576)).
  - Do: Compress the overhead vapour and use it to boil the bottoms (mechanical vapour recompression, a heat pump). It pays when its coefficient of performance (heat delivered per unit of work) clearly exceeds the electricity-to-heat price factor.
  - Why: Compressed overhead vapour condenses hot enough to boil the bottoms, and a small temperature lift needs little compressor work.
  - Check: Work out the coefficient of performance from the column's top and bottom temperatures and compare it with your site's factor.
  - Result: Coefficient of performance 8.8 for the vacuum column, against an assumed factor of 2.5: much lower energy use.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Vacuum distillation, p. 717; Methods, p. 716. <!-- jankovic-2023-ipa-acetone-recovery.mvr-when-temperatures-close -->

- **Wide temperature span across a column: no vapour recompression; boil its bottoms with the hot recovered solvent instead**
  - When: Extractive and solvent-recovery columns have a wide top-to-bottom temperature span.
  - Do: Do not use vapour recompression on them. Use the hot solvent from the recovery column, which must be cooled before reuse anyway, to boil part of the extractive column's bottoms.
  - Why: A heat pump across a large temperature lift needs too much compressor work, while the solvent's heat is free.
  - Check: Check that the solvent is hotter than the extractive column's bottoms by a workable approach.
  - Result: 16-17% less external heat for the extractive column ([Janković et al. 2023](https://doi.org/10.1002/jctb.7576)).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 720. <!-- jankovic-2023-ipa-acetone-recovery.no-mvr-wide-temperature-span -->

- **Subcooled column feed after a vacuum step: preheat it with process heat**
  - When: The vacuum overhead becomes a subcooled liquid after pumping to atmospheric pressure and feeds the next column.
  - Do: Preheat it with hot water bottoms or hot solvent, heat that must be removed anyway.
  - Why: A subcooled feed must first be heated inside the column, which adds to the reboiler duty.
  - Check: Compare the reboiler duty with and without the preheat in your simulation.
  - Result: The acetone column's reboiler duty fell by 12-41% ([Janković et al. 2023](https://doi.org/10.1002/jctb.7576)).
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 721. <!-- jankovic-2023-ipa-acetone-recovery.preheat-subcooled-feed -->

- **Heat pump or multi-effect: let the heat-to-electricity price ratio decide**
  - When: You rank recovery designs that use heat pumps (electricity) against multi-effect desorption (steam).
  - Do: Report the ranking with the utility prices it assumes. Cheap heat favours multi-effect desorption; cheap electricity favours the heat-pump designs.
  - Why: Heat pumps run on electricity and multi-effect on steam, so their order flips with the price ratio.
  - Check: Recompute the ranking at your own site's prices.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Economic evaluation, p. 722. <!-- jankovic-2023-ipa-acetone-recovery.price-ratio-decides-configuration -->

- **Feed the first column's distillate to the next column as vapour**
  - When: The first column's distillate is condensed, then reboiled again in the heteroazeotropic column.
  - Do: Send the distillate as vapour, without condensing it.
  - Why: The vapour's latent heat goes straight into the second column.
  - Check: Compare the second column's reboiler duty with a liquid and with a vapour feed.
  - Result: Reboiler duty about 59% lower (163 against 402 kW) in the 1,4-dioxane case.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.3, p. 16 (Fig. 11). <!-- kruber-skiborowski-2022-heteroazeotropic-init.vapour-distillate-feed -->

- **Thermally coupled columns against simple ones: compare with heat integration included**
  - When: You choose between thermally coupled complex columns and sequences of simple columns.
  - Do: Include heat integration in both options before comparing them.
  - Why: Without heat integration coupled columns win by a wide margin; heat integration recovers much of what coupling saves, so the gap narrows a lot.
  - Check: Run the pinch targets for both options.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2023, *Synthesis and optimization of energy integrated advanced…* (https://doi.org/10.1016/j.seppur.2023.123717), Abstract, p. 1. <!-- li-2023-distillation-sequences.coupled-columns-vs-heat-integration -->

- **Biodiesel plants: pinch analysis cut utilities by about 11-16%**
  - When: A biodiesel plant with several distillation steps uses much heating and cooling.
  - Do: Apply pinch analysis (heat-recovery targeting) to match hot and cold streams.
  - Why: Matching hot and cold streams recovers heat.
  - Check: Compare your utility use with the pinch targets.
  - Result: Heating and cooling utilities fell by roughly 11 to 16% in studies cited by [Pasha et al. 2021](https://doi.org/10.1186/s13068-021-01977-z), not read by Lab.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Heat integration'. <!-- pasha-2021-biodiesel-process-design.pinch-savings-biodiesel -->

- **Carbonation of ethylene oxide is strongly exothermic: raise low-pressure steam from it**
  - When: Heat must be removed from the carbonate reactors.
  - Do: Use the reactor cooling to raise low-pressure steam.
  - Why: The heat removed is at a useful temperature.
  - Check: Check that the reactor temperature lies far enough above the steam's saturation temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'MEG production via indirect EO hydration process', pp. 7-8. <!-- shehata-2024-meg-routes.carbonation-heat-to-steam -->

- **Dilute glycol: multi-effect evaporators first, vacuum column last**
  - When: A dilute glycol solution after hydration needs most of its water boiled off.
  - Do: Remove most of the water in evaporators at falling pressure, each heated by the vapour of the one before, then finish in a vacuum dehydration column.
  - Why: Reusing each evaporator's vapour to heat the next divides the steam demand.
  - Check: In CHEPTA, check that each evaporator still has a positive temperature difference at its pressure.
  - Result: In [Shehata et al. 2024](https://doi.org/10.1038/s41598-024-77713-y)'s simulation the evaporators take about 75% of the water and only the first uses steam.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Shehata et al. 2024, *A comparative study of mono ethylene glycol…* (https://doi.org/10.1038/s41598-024-77713-y), Section 'MEG production via direct EO hydration process', p. 8 (Fig. 5). <!-- shehata-2024-meg-routes.evaporator-train-before-vacuum-column -->
