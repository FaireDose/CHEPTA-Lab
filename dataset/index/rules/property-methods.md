# Property methods (generated; do not edit)

Wrong phases or volatilities: which thermodynamic model and parameters to use and check. 8 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Column with water and an organic phase gives odd profiles: allow two liquids on every stage**
  - When: A column whose liquid can split into two phases (for example water with an organic entrainer, in heteroazeotropic distillation) is computed with vapour-liquid equilibrium only, or its stage profiles look wrong.
  - Do: Test phase stability (whether a liquid would rather split into two) on every stage, and allow vapour-liquid-liquid equilibrium there. Kruber & Skiborowski 2022 cite earlier work showing that leaving out the second liquid can give substantial errors.
  - Why: On a stage that really holds two liquids, a one-liquid calculation gets the wrong equilibrium, and so the wrong compositions, flows and balance.
  - Check: In CHEPTA, set phases: "VLL" on the column and the decanter, then see which stages report two liquids and compare the decanter's two liquid compositions with those of Kruber & Skiborowski 2022.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 2 (refs. 17-18); Section 2.1, p. 4. Lab reread Section 1, p. 2 on 2026-11-20. <!-- kruber-skiborowski-2022-heteroazeotropic-init.phase-stability-every-stage -->

- **Acetic acid in the vapour or lithium bromide brine: choose property methods that can handle them**
  - When: A broth recovery with acetic acid present, or with a lithium bromide brine loop, gives wrong phases or volatilities.
  - Do: With acetic acid, use NRTL with Hayden-O'Connell vapour association (a model of acid pairs in the vapour), as Janković et al. 2023 did. With lithium bromide brine, regress an electrolyte NRTL model (with Redlich-Kwong vapour) on binary data, since no ready parameter set fits.
  - Why: Acetic acid forms dimers in the vapour, which changes its volatility. The salt needs an electrolyte model.
  - Check: Check that CHEPTA's property method covers vapour association and electrolytes for your components before relying on it. The fitted parameters are in the Supporting Information of Janković et al. 2023, not read by Lab.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Janković et al. 2023, *Advanced purification of isopropanol and acetone from…* (https://doi.org/10.1002/jctb.7576), Results, Vacuum distillation, p. 717; Pass-through distillation, p. 718. <!-- jankovic-2023-ipa-acetone-recovery.acid-and-brine-property-methods -->

- **Predictive property method (UNIFAC- or COSMO-type): check it against data first**
  - When: A design relies on phase behaviour or properties from a predictive model, for example for ionic liquids or other unusual molecules.
  - Do: Check the method against measured data over a wide range of the property before a design relies on it.
  - Why: Group-contribution and COSMO methods can err for unusual molecules.
  - Check: Lab relies on CHEPTA's property provenance; this check matters where a method lacks data for the case's components.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': definition of thermodynamic model and property validation. <!-- palomar-2024-il-process-simulation.validate-predictive-methods -->

- **Polar mixtures such as glycerol, methanol and water: NRTL or UNIQUAC, with UNIFAC for missing pairs**
  - When: A mixture contains polar components and some binary parameters are missing.
  - Do: Use an activity-coefficient model, NRTL or UNIQUAC, and fill the missing binary pairs with UNIFAC (group-contribution) estimates, as Pasha et al. 2021 describe.
  - Why: Activity models describe non-ideal liquids; UNIFAC fills the gaps.
  - Check: Estimated pairs are guesses until checked against data: find out which pairs CHEPTA has from data and which are predicted.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Pasha et al. 2021, *An overview to process design, simulation and…* (https://doi.org/10.1186/s13068-021-01977-z), Section 'Process design and simulation'. <!-- pasha-2021-biodiesel-process-design.nrtl-uniquac-polar -->

- **Salt in the liquid phases: use an electrolyte activity model**
  - When: Liquid phases contain dissolved salt and the liquid-liquid split comes out wrong.
  - Do: Correlate the liquid-liquid equilibrium with an electrolyte activity model that has ion-pair parameters, as Fu et al. 2021 did with e-NRTL (electrolyte NRTL).
  - Why: Ions change the activities in ways a molecular model misses.
  - Check: Whether CHEPTA 0.6.2 has an electrolyte model was not checked: check before planning a case with salts.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Fu et al. 2021, *Assessment of extraction options for a next-generation…* (https://doi.org/10.1002/elsc.202000090), Section 'Modeling of the liquid-liquid equilibria'; Concluding remarks. <!-- fu-2021-isobutanol-recovery.electrolyte-model -->

- **Simulation shows an azeotrope the data do not: check the built-in binary parameters**
  - When: A simulated azeotrope or phase behaviour does not appear in measured data.
  - Do: Compare the predicted vapour-liquid equilibrium with measured data for the key binaries before designing. Li et al. 2017 found built-in NRTL values predicting a toluene and DMF (dimethylformamide) azeotrope that experiments do not show.
  - Why: Stored interaction parameters may be fitted outside the range or to poor data.
  - Check: Lab relies on CHEPTA's parameter provenance and looks into data only on such a concrete disagreement (AGENTS.md): record the disagreement when you find one.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2017, *Phase Behavior and Thermodynamic Model Parameters in…* (https://doi.org/10.1038/s41598-017-09088-2), Introduction (Fig. 1). <!-- li-2017-ed-thermo-parameters.check-built-in-parameters -->

- **Butanol, acetic acid, butyl acetate and water: use NRTL and allow two liquids**
  - When: You simulate the butyl acetate system, whose column overhead splits into a water phase and an organic phase in a decanter.
  - Do: Use an activity model such as NRTL (non-random two-liquid model) with a vapour-liquid-liquid calculation, as Al-Rabiah et al. 2022 did. Lab's reading: a vapour-liquid-only calculation cannot reproduce the decanter split that the reactive column relies on.
  - Why: The mixture is strongly non-ideal. Wherever water and the organic phase meet, a three-phase flash is needed.
  - Check: In CHEPTA, set phases: "VLL" on the decanter and the column and check that two liquids form at the decanter. Al-Rabiah et al. 2022 do not print their NRTL parameters (Aspen databank), and CHEPTA 0.6.2 has some of these pairs only predicted, so compare the decanter compositions before trusting them.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Al-Rabiah et al. 2022, *Novel Process for Butyl Acetate Production via…* (https://doi.org/10.3390/pr10091801), Section 2, p. 2; Section 6.2, p. 15 (decanter). <!-- al-rabiah-2022.nrtl-vlle-for-ester-system -->

- **Glycol and water: use a property method that handles association, and check for two liquids on the stages**
  - When: Glycols and water associate (form hydrogen bonds), which simple models describe poorly.
  - Do: Use an association-capable property method, as Othman 2024 did with the cubic-plus-association (CPA) equation of state, and check phase stability on the stages.
  - Why: An association term represents the hydrogen bonding.
  - Check: CHEPTA's own property methods and their applicability govern Lab runs: check that the method chosen covers glycol and water at the column's conditions.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Model, p. 3. <!-- othman-2024-meg-reactive-distillation.cpa-for-glycol-water -->
