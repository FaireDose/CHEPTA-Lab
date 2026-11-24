# Column convergence (generated; do not edit)

Columns that fail, are slow or miss a target: starting profiles, solvers, steady states. 22 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Unit misses purity in the plant: fix it alone first with a design specification, then connect**
  - When: A separation unit misses its purity once connected in the plant.
  - Do: Simulate and size each separation unit alone first. Reach its purity or recovery with a design specification that adjusts one variable, or a sensitivity scan, before connecting the whole process.
  - Why: Fixing units alone separates unit problems from loop problems.
  - Check: In CHEPTA, pair each target with one free variable and bounds, and keep each run.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': process modelling and simulations. <!-- palomar-2024-il-process-simulation.units-alone-then-design-spec -->

- **Guess the heteroazeotropic recycle from a mass balance, not from defaults**
  - When: The recycle composition and flow of a two-column process with a decanter are unknown.
  - Do: Solve an overall mass balance first: pure bottom products, a top vapour at the lowest-boiling heteroazeotrope, and a decanter splitting it into its two liquids, with the solvent-lean liquid recycled. Use the result as the tear guess (the recycle stream's starting value).
  - Why: The heteroazeotrope and its liquid split fix the overhead and the recycle to a first approximation.
  - Check: In CHEPTA, give this balance as the tear stream's starting value and compare the first iteration with it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, p. 7 (steps 2-3, Fig. 3b-c). <!-- kruber-skiborowski-2022-heteroazeotropic-init.mass-balance-estimate-of-recycle -->

- **Converged design far off the trend may be a poor local optimum: nudge the feed stage or stage count**
  - When: One optimised design sits well off the trend of its neighbours.
  - Do: Change the initial feed stage or the total number of stages slightly and re-solve.
  - Why: The final fixing of stage locations can land in a worse local optimum.
  - Check: Compare the re-solved design with its neighbours.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.1.2, p. 12; Section 3.3.1, p. 17. <!-- kruber-skiborowski-2022-heteroazeotropic-init.outliers-from-integer-fixing -->

- **Start the heteroazeotropic column from a profile joining azeotrope, saddle and bottom product**
  - When: A column crossing a two-liquid region fails from a flat or constant starting profile.
  - Do: Initialise with a piecewise-linear composition profile joining the lowest-boiling heteroazeotrope, the saddle of its distillation region and the bottom product. Check the phases on each stage before solving the full column.
  - Why: At total reflux the profile follows the region's singular points, so this start lies close to the solution.
  - Check: Lab has not checked whether CHEPTA accepts a stage-by-stage starting profile; if not, start from the closest converged column.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, p. 7 (step 5, Fig. 3e); Section 3.1.1, pp. 10-11 (Fig. 5). <!-- kruber-skiborowski-2022-heteroazeotropic-init.piecewise-initial-profile -->

- **Stages switching between one and two liquids break a gradient solver: hide the split inside the property call**
  - When: A gradient-based solver meets discontinuities as stages change between one and two liquids.
  - Do: Treat each three-phase stage as a quasi vapour-liquid stage on the overall liquid, and do the two-liquid split only inside the property calculation.
  - Why: The column equations then see a smooth function, while the liquid split is still computed.
  - Check: This is a solver design choice. In CHEPTA, note which stages switch between one and two liquids when a run fails, and report it with the failure.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.1, pp. 4-5. <!-- kruber-skiborowski-2022-heteroazeotropic-init.quasi-vle-for-three-phase-stages -->

- **Scanning feed composition widely: re-initialise for each interval**
  - When: A feed-composition scan fails or gives outliers away from the first feed.
  - Do: Re-initialise the column for each interval of feed composition instead of reusing one start.
  - Why: The required stage numbers vary a lot, so a start built for one feed lies far from the solution for another.
  - Check: In CHEPTA, start each scan interval from a run converged near that feed.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.2.2, p. 16. <!-- kruber-skiborowski-2022-heteroazeotropic-init.reinitialise-for-feed-changes -->

- **Even one heteroazeotropic column is hard: fix the organic reflux before adding the second column**
  - When: A heteroazeotropic column does not converge.
  - Do: Fix the organic reflux and recycle estimates before adding the second column. Do not read a failure as a property error alone.
  - Why: Such a column can have several steady states and its products are very sensitive to the organic reflux. Luyben's careful manual start of ethanol dehydration still ended unconverged (cited by [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482)).
  - Check: In CHEPTA, scan the organic reflux around the published value and record where the column converges.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 1, p. 2 (ref. 11). <!-- kruber-skiborowski-2022-heteroazeotropic-init.single-column-already-hard -->

- **Heteroazeotropic recycle hard to close: allow a small purge**
  - When: The recycle through the decanter is not robust.
  - Do: Allow a small optional purge. In the 1,4-dioxane and benzene case of [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482) the optimisation relied on 0.8% of the feed.
  - Why: A purge removes accumulating material and loosens the recycle. [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482) link the need for it to a poorer initial profile estimate.
  - Check: In CHEPTA, record the purge flow and the product lost with it, and try to remove the purge once the loop converges.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 3.3, p. 16. <!-- kruber-skiborowski-2022-heteroazeotropic-init.small-purge-aids-robustness -->

- **Before building a heteroazeotropic column, map every azeotrope**
  - When: You set up a heteroazeotropic column (one with a decanter on top where two liquids form), and it starts far from a feasible profile.
  - Do: Compute and classify every azeotrope as a node or a saddle (points where residue curves start, end or turn). These singular points show which profiles a column can reach at total reflux and guide the starting profile.
  - Why: The mixture's topology bounds what column profiles are possible.
  - Check: In CHEPTA, check each azeotrope's temperature and composition against [Kruber & Skiborowski 2022](https://doi.org/10.3390/pr10081482) or measured data before the first column run.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, pp. 5-7 (step 1, Figs. 2-3). <!-- kruber-skiborowski-2022-heteroazeotropic-init.topology-first -->

- **Equation-oriented solve fails from poor estimates: start it from a short dynamic run**
  - When: An equation-oriented solver (one that solves all equations at once) fails from a poor starting point.
  - Do: Run a short dynamic simulation and use its final values as the initial guess for the steady state.
  - Why: A dynamic run moves all variables towards the steady state.
  - Check: Lab has not checked whether CHEPTA can run dynamically; if not, start from the closest converged steady state.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Introduction, p. 151. <!-- henrique-2020-dwc-simulation.dynamic-run-for-initial-guess -->

- **Dividing-wall column does not converge: model it as a pump-around pair of columns**
  - When: Your simulator has no dividing-wall column model (one shell with an internal wall), and the coupled-column version does not converge.
  - Do: Represent the dividing wall with the pump-around arrangement rather than the four-column arrangement.
  - Why: The pump-around form has fewer interconnecting recycles.
  - Check: In CHEPTA, build the pump-around version and compare its products with the four-column one where both converge.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Henrique et al. 2020, *Divided Wall Column Modeling and Simulation in…* (https://doi.org/10.15255/CABEQ.2020.1824), Introduction, p. 150 (Fig. 1). <!-- henrique-2020-dwc-simulation.pump-around-representation -->

- **Column converges but misses its purity: check balances and stage profiles before changing settings**
  - When: A column converges but misses its purity or recovery target.
  - Do: Check each component's balance around the column, and compare the stage temperature, flow and composition profiles with a reference, not only the products.
  - Why: Balances and stage profiles show the section or stage where the separation departs from the target; the end products alone hide it.
  - Check: In CHEPTA, compare the run's stage profiles with the reference case and find the stage where they diverge before changing a setting.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kooijman & Taylor 2006, *The ChemSep Book, second edition* (https://www.chemsep.org/downloads/docs/book2.pdf), Sections 1.2-1.3, pp. 9-20, Figures 1.18-1.21 (balances, profiles, stream table), as transcribed by CHEPTA. Lab has not reread the source for this summary. <!-- kooijman-taylor-2006-chemsep-book.column-misses-target-check-balances-and-profiles -->

- **Build up the simple column step by step: flash, fixed column, then optimise**
  - When: A column model solved all at once from a poor start fails.
  - Do: Flash the mixed feed (fresh feed plus recycle) first, then solve the stage model with a fixed structure, and only then minimise duty. Raise the model's complexity one step at a time.
  - Why: Each harder sub-problem starts close to the solution of the easier one before it.
  - Check: In CHEPTA, keep each step's converged result and start the next step from it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Kruber & Skiborowski 2022, *Topology-Based Initialization for the Optimization-Based Design of…* (https://doi.org/10.3390/pr10081482), Section 2.2, p. 7 (step 4, Fig. 3d). <!-- kruber-skiborowski-2022-heteroazeotropic-init.simple-column-flash-then-solve -->

- **Newton iterations diverge: improve the start or damp the step**
  - When: A Newton-type column solver diverges.
  - Do: Improve the starting values, or damp the Newton step (relaxation) so it takes smaller moves.
  - Why: Full Newton steps overshoot far from the solution, and the method fails where several solutions exist.
  - Check: In CHEPTA, look at the solver's residual history: residuals that grow point to a poor start.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Numerical methods, p. 18. <!-- steffen-2024-rd-modelling-review.newton-needs-good-start -->

- **Rate-based column model fails: check the mass-transfer data and compare with the equilibrium-stage result**
  - When: A rate-based (non-equilibrium) stage model does not converge.
  - Do: Check the mass-transfer correlations, and compare with the equilibrium-stage result.
  - Why: Rate-based models have more equations with stiffer coupling than equilibrium-stage models.
  - Check: Converge the equilibrium-stage column first and use it as the reference.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Equilibrium and non-equilibrium models, p. 15. <!-- steffen-2024-rd-modelling-review.rate-based-harder -->

- **Simulated extraction needs fewer columns than reality: do not assume infinite selectivity**
  - When: An extraction model assumes the extractant takes no water, and the downstream columns come out smaller than expected.
  - Do: Use measured distribution coefficients (how a component divides between the two liquids). Real selectivities (about 300 in [Grisales Díaz & Olivar Tost 2017](https://doi.org/10.1186/s40643-017-0142-z)) carry water into the extract, which then needs extra distillation.
  - Why: At finite selectivity some water is always co-extracted.
  - Check: Check the water content of the simulated extract against measured partition data.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Grisales Díaz & Olivar Tost 2017, *Techno-economic analysis of extraction-based separation systems for…* (https://doi.org/10.1186/s40643-017-0142-z), Methods: 'Extractant selection'. <!-- grisales-2017-abe-extraction.finite-selectivity -->

- **Regressed and built-in parameters can change the design: volatility off by a factor 1.84, cost by about 45%**
  - When: Simulated purity or cost is far from what was expected.
  - Do: Use parameters regressed from measured data where the built-in ones disagree with the data.
  - Why: Relative volatility is sensitive to the interaction parameters.
  - Check: Compare the key pair's relative volatility from both parameter sets.
  - Result: For benzene and cyclohexane with NMP (a polar extractive solvent), relative volatility differed by a factor of 1.84 and annual cost by about 45%.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Li et al. 2017, *Phase Behavior and Thermodynamic Model Parameters in…* (https://doi.org/10.1038/s41598-017-09088-2), Conclusion. <!-- li-2017-ed-thermo-parameters.parameters-change-economics -->

- **Reactive glycol column converged but misses the target: it may be on the wrong steady state**
  - When: A converged reactive column for ethylene glycol misses its target.
  - Do: Look for other steady states before changing settings: restart from different estimates or scan a setting.
  - Why: Several steady states exist for the same inputs, and one of them accumulates ethylene oxide at the top (earlier modelling studies cited by [Othman 2024](https://doi.org/10.31031/pps.2024.06.000637)).
  - Check: In CHEPTA, check the oxide at the top stage: a high value points to the wrong branch.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Othman 2024, *Process Modelling and Simulation of Reactive Distillation…* (https://doi.org/10.31031/pps.2024.06.000637), Introduction, p. 2 (citing earlier modelling studies). <!-- othman-2024-meg-reactive-distillation.rd-multiple-steady-states-oxide-overhead -->

- **Homotopy continuation is robust but slow: keep it for cases with no good start**
  - When: A robust solving method is too slow for scans.
  - Do: Use Newton or Broyden from good estimates as the default; keep homotopy continuation (a chain of easier problems ending in the real one) for cases where no good start can be found.
  - Why: Continuation solves the modified system many times, so it costs much more computation.
  - Check: Time both methods on one case before choosing one for a scan.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Numerical methods, p. 18; Initial estimates, pp. 22-23. <!-- steffen-2024-rd-modelling-review.homotopy-robust-but-costly -->

- **Reactive column does not converge from defaults: start from straight-line temperatures and constant flows**
  - When: The reactive column solver fails from its default estimates.
  - Do: Start from a straight-line temperature profile between the bubble point of the mixed feed at the condenser and its dew point at the reboiler, with constant molar flows and a reaction extent peaking at the feed stage.
  - Why: Physically shaped profiles start the solver near a solution.
  - Check: Lab has not checked whether CHEPTA accepts such a starting profile; if not, start from a converged simpler case.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Initial estimates, p. 21. <!-- steffen-2024-rd-modelling-review.initial-profiles -->

- **Reactive column converged but misses its target: look for other steady states**
  - When: A converged reactive column misses its target.
  - Do: Scan a parameter or restart from different initial estimates, and find the steady states before accepting one.
  - Why: Reactive columns often have several solutions for the same inputs (output multiplicity).
  - Check: In CHEPTA, record each branch found and which one meets the target.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Initial estimates, p. 22. <!-- steffen-2024-rd-modelling-review.multiple-steady-states -->

- **Full reactive model fails: converge a simpler model first and start from it**
  - When: The full reactive column model does not converge.
  - Do: Converge a simpler model first, the column without reaction or with ideal K-values (ideal vapour-liquid ratios), then use its result to start the full model.
  - Why: A simpler model gives profiles close to those of the full one.
  - Check: In CHEPTA, keep the simpler run and start the full run from it.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Steffen et al. 2024, *A Systematic Review of the Literature on…* (https://doi.org/10.5772/intechopen.1005434), Initial estimates, p. 21. <!-- steffen-2024-rd-modelling-review.simpler-model-first -->
