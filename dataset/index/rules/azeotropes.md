# Azeotropes and two liquid phases (generated; do not edit)

Breaking azeotropes: entrainers, solvents, decanters, pressure swing. 27 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Esterification limited by water: remove the water azeotropically as it forms**
  - When: Water limits the conversion of an esterification.
  - Do: Couple the reaction with azeotropic water removal.
  - Why: Water leaves as it forms, so the equilibrium shifts towards the ester.
  - Check: Compare conversion with and without water removal in an equilibrium model.
  - Result: A shorter reaction and higher conversion; a study cited by [Guo & Wang 2019](https://doi.org/10.4236/aces.2019.94024), not read by Lab, reports 2.7% higher conversion for isoamyl acetate than ordinary water separation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Guo & Wang 2019, *Research Progress on Azeotropic Distillation Technology* (https://doi.org/10.4236/aces.2019.94024), Section 2.3, p. 337. <!-- guo-wang-2019-azeotropic-distillation.azeotropic-water-removal-in-esterification -->

- **Azeotropic distillation: prefer an entrainer that forms two liquids, so a decanter recovers it**
  - When: You choose an entrainer (an added component that breaks the azeotrope) for azeotropic distillation.
  - Do: Prefer one that forms two liquid phases with the mixture, so that a decanter separates it and returns it to the column.
  - Why: The decanter does part of the separation without heat. Homogeneous azeotropic distillation recirculates more azeotrope and uses more energy.
  - Check: In CHEPTA, set phases: "VLL" and check that the condensed overhead splits into two liquids at decanter temperature.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Guo & Wang 2019, *Research Progress on Azeotropic Distillation Technology* (https://doi.org/10.4236/aces.2019.94024), Section 1, p. 334. <!-- guo-wang-2019-azeotropic-distillation.prefer-heterogeneous-entrainer -->

- **Ethanol dehydration: cyclohexane or hexane as entrainer; isooctane and toluene cost over 15% more**
  - When: You choose an entrainer for dehydrating a dilute ethanol broth (6 mol%) at atmospheric pressure.
  - Do: Prefer cyclohexane or hexane. Compare individually optimised processes for each solvent, not one fixed design.
  - Why: Each solvent changes the topology, the decanter split and the duties.
  - Check: [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482) used NRTL with Aspen databank parameters (APV88) in their own optimisation: compare CHEPTA's azeotropes with theirs before reusing the ranking.
  - Result: Cyclohexane and hexane gave the same annual cost within estimate accuracy; isooctane and toluene cost over 15% more. Solvent make-up was below 0.4% of cost.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.1, pp. 9-10 (Fig. 4). <!-- kruber-skiborowski-2022-heteroazeotropic-init.ethanol-solvent-screen -->

- **Flat cost optimum: use the freedom to meet other constraints**
  - When: You must pick one design from many near-optimal ones.
  - Do: Use the flat optimum to trade larger columns against lower energy, or to meet other constraints.
  - Why: Stages and reflux trade off: nearly all Pareto-optimal designs (best trade-offs) fell within 5% of the minimum annual cost, while capital and operating cost shifted by about 20%.
  - Check: Cost a few designs along the trade-off before fixing one.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.2, p. 11 (Fig. 6); Section 3.2.1, p. 14 (Fig. 9). <!-- kruber-skiborowski-2022-heteroazeotropic-init.flat-cost-optimum -->

- **Heteroazeotropic distillation needs a heterogeneous azeotrope: two columns and a decanter**
  - When: You want to break an azeotrope by heteroazeotropic distillation.
  - Do: Check that the mixture forms a heterogeneous azeotrope (one that splits into two liquids); such an azeotrope is always minimum-boiling. Then use the usual process: a simple column and a heteroazeotropic column with a decanter, each giving one product as bottoms.
  - Why: The decanter crosses the distillation boundary (a line a column profile cannot cross) by splitting the liquid.
  - Check: In CHEPTA, set phases: "VLL" and confirm that the azeotrope splits into two liquids. Alternatives: extractive or pressure-swing distillation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 1; Section 2.1, p. 4 (Fig. 1). <!-- kruber-skiborowski-2022-heteroazeotropic-init.heteroazeotrope-prerequisite -->

- **No general rule for pre-concentration: run the feed scan for your case**
  - When: You want to reuse a pre-concentration rule from another mixture.
  - Do: Run the feed-composition scan for the case at hand.
  - Why: Each mixture's cost curve has its own shape: in the 1,4-dioxane case cost falls almost linearly with feed concentration, unlike the other two cases of [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482).
  - Check: Plot specific cost against feed concentration and look for a knee.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.3.2, p. 18 (Fig. 13). <!-- kruber-skiborowski-2022-heteroazeotropic-init.no-general-preconcentration-heuristic -->

- **Dilute ethanol: pre-concentrating to about 20 mol% may pay**
  - When: The ethanol feed to heteroazeotropic dehydration is very dilute.
  - Do: Consider a pre-concentration step near the knee of the cost curve, about 20 mol% ethanol. For a feed already in the flat region, such as the ethyl acetate case of [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482), it would not pay.
  - Why: At low feed concentration most of the cost goes to handling water: specific cost falls steeply up to about 20 mol% and then flattens.
  - Check: A cited study found the saving too small for an extra column, and [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482) leave it open: run your own feed-composition scan.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.3, pp. 12-13 (Fig. 7); Section 3.2.2, p. 15 (Fig. 10). <!-- kruber-skiborowski-2022-heteroazeotropic-init.preconcentrate-dilute-ethanol -->

- **Heteroazeotropic solvent choice: simple indicators mislead, so screen with a process model**
  - When: You choose a solvent for heteroazeotropic distillation.
  - Do: Screen solvents with a process model, not on selectivity alone.
  - Why: Three ternary topologies, with four, three or two azeotropes, cover most cases (about 26%, 8% and 21% of 1365 surveyed mixtures, cited by [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482)). Their several azeotropes and distillation regions defeat simple indicators.
  - Check: Compare individually optimised processes for each solvent.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 2; Section 2.2, p. 6 (Fig. 2). <!-- kruber-skiborowski-2022-heteroazeotropic-init.three-common-topologies -->

- **Acetic acid from water: heterogeneous azeotropic distillation with butyl acetate as entrainer**
  - When: Acetic acid and water form no azeotrope but are close-boiling.
  - Do: Use heterogeneous azeotropic distillation with n-butyl acetate as entrainer. For dilute feeds add a preconcentrator column.
  - Why: The entrainer carries water overhead as a heterogeneous azeotrope that splits in a decanter.
  - Check: In CHEPTA, set phases: "VLL" and check the water-ester split in the decanter.
  - Result: A study cited by [Valentini & Vaccaro 2020](https://doi.org/10.3390/molecules25225264), not read by Lab, cut annual cost by 55% against plain distillation.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.2. <!-- valentini-2020-azeotropes-waste.butyl-acetate-entrainer-for-acid-water -->

- **Screening heterogeneous entrainers: miscibility gap, azeotrope composition, temperature gaps**
  - When: You choose among many candidate entrainers.
  - Do: Screen on three criteria before simulating: the width of the miscibility gap (the two-liquid region), the composition of the azeotrope each forms, and the temperature gaps to the other azeotropes.
  - Why: These properties decide the decanter split and whether the column is feasible.
  - Check: Compute the three criteria with the property method for each candidate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.2 (cited screening of 60 candidates). <!-- valentini-2020-azeotropes-waste.entrainer-screening-criteria -->

- **Heterogeneous azeotropic distillation can be built as a dividing-wall column**
  - When: Azeotropic distillation uses a lot of energy.
  - Do: Consider a heterogeneous azeotropic dividing-wall column (one shell with an internal wall).
  - Why: Thermal coupling avoids remixing.
  - Check: Compare with the two-column process on the same basis.
  - Result: About 33% less energy and 20% lower annual cost in a solvent-recovery case cited by [Valentini & Vaccaro 2020](https://doi.org/10.3390/molecules25225264), not read by Lab.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.2. <!-- valentini-2020-azeotropes-waste.heteroazeotropic-dwc -->

- **Solvent waste with several azeotropes and water: use the water as the entrainer**
  - When: An aqueous solvent waste holds several azeotropes.
  - Do: Use hybrid extractive-heterogeneous azeotropic distillation, with the water already present as the entrainer.
  - Why: Water acts as the extractive agent and forms separable heterogeneous azeotropes, so no new component is added.
  - Check: Map the azeotropes of the mixture first.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Valentini & Vaccaro 2020, *Azeotropes as Powerful Tool for Waste Minimization…* (https://doi.org/10.3390/molecules25225264), Section 2.3. <!-- valentini-2020-azeotropes-waste.water-as-auto-entrainer -->

- **Reactive column overhead: decant, draw off the water, return all the organic phase as reflux**
  - When: The overhead of a butyl acetate reactive column condenses into water and an organic (butanol and ester) phase.
  - Do: Condense into a decanter, draw the water phase off as wastewater (about 102 kmol/h in [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801)) and return the whole organic phase to the column as reflux. The conventional route uses extractive distillation with a solvent instead.
  - Why: Water and the butanol-ester phase split into two liquids, so water leaves without taking the reactants and the ester with it.
  - Check: In CHEPTA, set phases: "VLL" on the decanter and compare the water phase's flow and composition with stream 3 of Table 9.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 6.2, p. 15 (Fig. 16, Table 9 stream 3). <!-- al-rabiah-2022.rd-decanter-returns-organic -->

- **In butyl acetate reactive distillation most ester is lost in the decanter's water phase, not the bottoms**
  - When: You check product losses and wastewater load of a reactive column with a decanter.
  - Do: Check the aqueous phase composition when matching [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801): per 100 kmol/h of each feed, their wastewater carries about 1.5 kmol/h ester, 1.3 acid and 0.2 butanol.
  - Why: Ester, acid and water are partly soluble in each other, so the water phase carries some of each.
  - Check: In CHEPTA, compare the decanter's water phase with stream 3 of Table 9. That it holds more ester than the bottoms loses is Lab's reading of the table.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 9, p. 15 (streams 3-4). <!-- al-rabiah-2022.rd-loss-in-water-phase -->

- **Alcohol-water heteroazeotrope: a decanter with two strippers gives both pure**
  - When: An alcohol and water form a heterogeneous azeotrope (one that splits into two liquids), as isobutanol does.
  - Do: Condense into a decanter. Strip the organic layer in one column to get dry alcohol at its bottom, and the aqueous layer in another to get water at its bottom. Return both overheads to the decanter.
  - Why: The two liquids lie on either side of the azeotrope, so each stripper works inside its own region.
  - Check: Shown for isobutanol; 1-butanol and water form the same kind of azeotrope, a transfer not tested here. In CHEPTA, set phases: "VLL" on the decanter and check the two liquid compositions.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Fu et al. 2021, *Assessment of extraction options for a next-generation…* (https://doi.org/10.1002/elsc.202000090), Introduction (Fig. 1). <!-- fu-2021-isobutanol-recovery.decanter-with-two-strippers -->

- **Azeotrope building up in an azeotropic dehydration column: add a partial condenser before the decanter**
  - When: In azeotropic dehydration (of acetic acid, in a study cited by [Guo & Wang 2019](https://doi.org/10.4236/aces.2019.94024)) the azeotrope accumulates in the column.
  - Do: Put a partial condenser between the column top and the decanter.
  - Why: Part of the overhead is condensed and handled before the decanter, so the azeotrope stops building up in the column.
  - Check: A cited result not read by Lab: compare the column profiles with and without the partial condenser in a simulation.
  - Result: Less accumulation and lower energy use.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Guo & Wang 2019, *Research Progress on Azeotropic Distillation Technology* (https://doi.org/10.4236/aces.2019.94024), Section 2.2, p. 336. <!-- guo-wang-2019-azeotropic-distillation.partial-condenser-before-decanter -->

- **Conceptual cost estimate: say whether the decanter is costed**
  - When: You cost a heteroazeotropic process at the concept stage.
  - Do: State the decanter as uncosted, or estimate its disengagement time (how long the two liquids need to separate) and size it.
  - Why: The decanter's size depends on a disengagement time that is usually not yet known.
  - Check: List the uncosted units with the cost estimate.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.1, p. 5. <!-- kruber-skiborowski-2022-heteroazeotropic-init.decanter-uncosted-in-concept -->

- **Heavy liquid product limits conversion: reactors in series with decanters between them**
  - When: A heavy product phase (glycerol in biodiesel) limits conversion, and a reactant harms the catalyst at high concentration.
  - Do: Put decanters between reactors in series to remove the product phase as it forms, and add the reactant in stages.
  - Why: Removing the product phase and dosing the reactant keep conditions favourable for conversion and catalyst life.
  - Check: In CHEPTA, set phases: "VLL" on the decanters and check that the glycerol phase separates.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design of biodiesel production using biocatalyst'. <!-- pasha-2021-biodiesel-process-design.staged-decanting -->

- **Start the 1,4-butanediol extractive column at about 2.4 mol solvent per mol feed**
  - When: You transcribe or design the extractive column of the conventional butyl acetate route and need a first solvent flow.
  - Do: Start from [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801)'s stream table: about 440 kmol/h of 1,4-butanediol against about 186 kmol/h of distillate (100 water, 43 butanol, 42 acid), roughly 2.4 mol per mol.
  - Why: The column needs enough solvent on every stage above the feed to break the azeotrope.
  - Check: The ratio is Lab's arithmetic (440.3 / 185.7, Table 7). In CHEPTA, scan the solvent flow around it and record where water purity and butanol recovery are met.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Table 7, p. 14 (streams 5, 9, 13). <!-- al-rabiah-2022.butanediol-circulation-ratio -->

- **Water with butanol and acetic acid in a recycle: extractive distillation with 1,4-butanediol**
  - When: In the conventional butyl acetate route the first column's distillate holds water with unreacted butanol and acid, and butanol forms an azeotrope with water.
  - Do: Feed 1,4-butanediol (a heavy polar solvent) at the top of an extractive column (29 stages in [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801)). Water leaves overhead to treatment; a recovery column returns the solvent and sends acid and butanol back to the reactor. Alternative: reactive distillation with a decanter needs no solvent.
  - Why: The heavy solvent holds butanol and acid back in the liquid, so water distils off.
  - Check: [Al-Rabiah et al. 2022](https://doi.org/10.3390/pr10091801) print no stage numbers or reflux for the first and the recovery column, and their text sends the solvent to T-101 where Fig. 11 suggests T-102. Resolve both before transcribing.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, p. 3 (Fig. 2); Section 6.1, p. 12 (Figs. 11 and 15); Table 7, p. 14. <!-- al-rabiah-2022.conventional-extractive-with-butanediol -->

- **Extractive solvent: boiling at least 50 C above the mixture, chosen on selectivity before capacity**
  - When: You screen solvents for an extractive separation.
  - Do: Choose a solvent that boils at least 50 C above the mixture, and weigh selectivity (how well it tells the two components apart) above capacity (how much it dissolves).
  - Why: A large boiling gap keeps the solvent from forming an azeotrope or a pinch during regeneration.
  - Check: Check for azeotropes between the solvent and each component with the property method before simulating the column.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Blahušiak et al. 2018, *Insights into the selection and design of…* (https://doi.org/10.1016/j.seppur.2017.10.026), Section 2.4, p. 311; Conclusions, p. 317. <!-- blahusiak-2018-separation-selection.solvent-boiling-gap-and-selectivity -->

- **Isopropanol stuck at its azeotrope with water: extractive distillation with ethylene glycol, solvent about 1.1 times the feed by mass**
  - When: You need dry isopropanol from a pre-concentrated isopropanol-water stream, which plain distillation cannot take past the azeotrope.
  - Do: Feed ethylene glycol near the top of an extractive column. Isopropanol leaves overhead; glycol and water leave at the bottom to a solvent-recovery column that returns the glycol. Scan the solvent-to-feed mass ratio: [Janković et al. 2023](https://doi.org/10.1002/jctb.7576) found 1.1 gave the lowest energy for the two columns together.
  - Why: Ethylene glycol holds water back in the liquid, so isopropanol becomes the more volatile component and distils overhead.
  - Check: In CHEPTA, scan the solvent-to-feed ratio around 1.1 and record the summed reboiler duty of both columns and the isopropanol purity. If the minimum lies far from 1.1, compare the property methods before changing the design.
  - Result: Isopropanol at 99.8 wt% overhead, with both columns at atmospheric pressure.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 720 (Fig. 5b). Lab reread Results, p. 721 on 2026-11-20 (ratio on a mass basis, for columns C4 and C5). <!-- jankovic-2023-ipa-acetone-recovery.ethylene-glycol-solvent-ratio -->

- **Dilute isopropanol: pre-concentrate to about 86 wt% before extractive dehydration**
  - When: The isopropanol stream to be dehydrated is dilute (about 31 wt% in [Janković et al. 2023](https://doi.org/10.1002/jctb.7576)).
  - Do: Pre-concentrate in a plain column first. Scan the distillate target and take the minimum of total energy; it fell up to about 86 wt% isopropanol, which was chosen.
  - Why: Getting closer to the azeotrope costs more in the pre-concentrator but less in dehydration, so the sum has a minimum.
  - Check: Stay below the homogeneous azeotrope (87.17 mass % isopropanol at 80.23 C, Table 1). In CHEPTA, scan the distillate purity and add the duties of both steps.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Recovery of high-purity products, p. 720 (Fig. 5a); Table 1, p. 716. <!-- jankovic-2023-ipa-acetone-recovery.preconcentrate-before-extractive -->

- **Picking an extractive solvent: high boiling, stable, easy to recover, low toxicity; screen by the volatility it adds**
  - When: You choose a solvent for extractive distillation.
  - Do: Pick one that boils well above the mixture, is thermally stable, easy to recover and of low toxicity. Screen candidates by how much they raise the key relative volatility, and by residue curve maps (how a boiling liquid's composition moves) free of distillation boundaries.
  - Why: The solvent works by changing the activity coefficients of the key pair.
  - Check: In CHEPTA, compute the key pair's relative volatility with and without the solvent.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2017, *Phase Behavior and Thermodynamic Model Parameters in…* (https://doi.org/10.1038/s41598-017-09088-2), Introduction. <!-- li-2017-ed-thermo-parameters.extractive-solvent-criteria -->

- **Tetrahydrofuran and water: extractive distillation was cheaper at steady state, but weigh control too**
  - When: You compare extractive and pressure-swing distillation for tetrahydrofuran and water on cost.
  - Do: Compare on annual cost and on controllability; expect a trade-off, not a single winner, as [Mtogo et al. 2021](https://doi.org/10.1021/acsomega.1c04606) argue.
  - Why: Extractive distillation used less energy at steady state in a study cited by [Mtogo et al. 2021](https://doi.org/10.1021/acsomega.1c04606), not read by Lab.
  - Check: Recompute both annual costs on the same basis.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Mtogo et al. 2021, *Comparison of Controllability Features of Extractive and…* (https://doi.org/10.1021/acsomega.1c04606), Introduction. <!-- mtogo-2021-ed-vs-psd.ed-cheaper-steady-state -->

- **Tetrahydrofuran and water: pressure-swing distillation was easier to control than extractive distillation**
  - When: You choose between pressure-swing and extractive distillation for tetrahydrofuran and water.
  - Do: Weigh controllability together with cost.
  - Why: The added solvent of extractive distillation brings more interactions and longer time constants, which complicate control.
  - Check: Compare both routes' responses to feed disturbances in a dynamic model; a steady-state simulation alone cannot show controllability.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Mtogo et al. 2021, *Comparison of Controllability Features of Extractive and…* (https://doi.org/10.1021/acsomega.1c04606), Conclusions. <!-- mtogo-2021-ed-vs-psd.psd-better-controllability -->

- **Pressure-swing distillation: only for an azeotrope that moves with pressure, and heat-integrate the two columns**
  - When: You want to break an azeotrope without adding a third component.
  - Do: Check that the azeotrope composition moves with pressure. Then use two columns at different pressures, heat integrated.
  - Why: Changing the pressure moves the azeotrope, so each column can pass it. Without heat integration it uses more energy than extractive distillation.
  - Check: In CHEPTA, compute the azeotrope at both pressures and confirm that it moves enough.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Mtogo et al. 2021, *Comparison of Controllability Features of Extractive and…* (https://doi.org/10.1021/acsomega.1c04606), Introduction; Conclusions. <!-- mtogo-2021-ed-vs-psd.psd-needs-pressure-sensitive-azeotrope -->
