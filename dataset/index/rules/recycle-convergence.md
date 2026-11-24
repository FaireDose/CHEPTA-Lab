# Recycle convergence (generated; do not edit)

Recycle loops, tears, make-ups and flashes inside loops that do not close. 6 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Tighten the tolerance from a saved answer; a loose one showed 99.673 % where the settled plant gives 99.109 %**
  - From Lab's own plant: [ethyl-acetate-piotrowski-2021](../plants/ethyl-acetate-piotrowski-2021.md).
  - When: A recycle plant converges only at a loose tear tolerance such as 3e-4.
  - Do: Save the converged tear streams, restart from them at 1e-4 and then 1e-5, and compare each component's inventory in the recycles between the two answers.
  - Why: A component with no exit but the products (here the excess ethanol) can still be building up while the plant balance already closes to 0.02 %.
  - Check: Compare the recycle flows of the loose and the tight answer; a balance check alone did not show it.
  - Result: Product 99.673 % at 3e-4 against 99.109 % settled at 1e-5; the ethanol in the reactor feed rose from 14,629 to 17,455 kg/h. A run at 5e-4 had a 42 kg/h balance gap.
  - Judged on: A settled steady state (tear change and balance at a tight tolerance), not the product purity.
  - Summarises 4 rows of the plant's run log.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Piotrowski & Kubica 2021, *Integration of the Process for Production of…* (https://doi.org/10.3390/pr9081425), p. 14, Table A2 (continued), streams 23-25. <!-- ethyl-acetate-piotrowski-2021.lesson-tighten-tolerance-from-saved-answer -->

- **Feed-effluent exchangers add cycles: choose tears that break every cycle, and give a slow loop more iterations**
  - From Lab's own plant: [methanol-co2-campos-2022](../plants/methanol-co2-campos-2022.md).
  - When: A plant with gas recycles and feed-effluent exchangers is closed as one flowsheet.
  - Do: Mark tears on the recycles and on the streams the exchangers join (here five), start them from the published values, and raise the iteration limit while the change is still falling.
  - Why: Each exchanger joining two parts of the plant makes a cycle the recycles alone do not break; the loop is slow, not stuck.
  - Check: If the engine says the tears do not break every cycle, add the exchanger streams; compare the tear change between the last iterations.
  - Result: Recycle tears only: refused; five tears: the plant closed in 31 iterations with both purges, recycle 36-REC +2.7 % against [Campos et al. 2022](https://doi.org/10.3390/pr10081535); the loop alone needed more than 50 iterations (200 allowed).
  - Judged on: A closed plant with balances closed; the products are judged in the column lessons.
  - Summarises 6 rows of the plant's run log.
  - Status: worked — Lab ran it in CHEPTA (chepta@0.6.2) and it converged.
  - Source: Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 9-10, Section E (one-step process); Campos et al. 2022, *A Detailed Process and Techno-Economic Analysis of…* (https://doi.org/10.3390/pr10081535), supplement pp. 10-11, Section E (one-step process). <!-- methanol-co2-campos-2022.lesson-tears-break-every-cycle -->

- **Some flowsheet cases fail but all converge with another flash routine: suspect the flash, not the recycle solver**
  - When: In a parametric study some cases of a flowsheet fail, and swapping in another flash routine makes them all converge.
  - Do: Test the flash on the failing streams alone before changing the recycle solver.
  - Why: A phase-split calculation that jumps between iterations breaks the outer recycle loop.
  - Check: In CHEPTA, rerun each failing unit on its captured inlet with the same phases setting; if it fails alone, report it as a flash case. [Andreasen 2022](https://doi.org/10.3311/PPch.19678) says this indicates, not proves, the cause.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Andreasen 2022, *Evaluation of an Open-source Chemical Process Simulator…* (https://doi.org/10.3311/PPch.19678), Results, p. 508; Discussion, p. 509. <!-- andreasen-2022-dwsim-evaluation.flash-instability-not-solver -->

- **Recycle loop converged on total flow: check each component as well**
  - When: A recycle loop reports convergence, but compositions still drift or the plant balance does not close for one component.
  - Do: Check the closure of each tear stream (the recycle stream that is guessed and recomputed) component by component, not only its total flow. [Andreasen 2022](https://doi.org/10.3311/PPch.19678) accepted recycle balance errors below 1 kg/h.
  - Why: A tolerance on total flow can be met while one component is too high and another too low.
  - Check: In CHEPTA, compare each tear's component flows between two tolerances, and check the plant's component balance (fresh feed plus production equals products) for every component.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Andreasen 2022, *Evaluation of an Open-source Chemical Process Simulator…* (https://doi.org/10.3311/PPch.19678), Section 2, p. 506. <!-- andreasen-2022-dwsim-evaluation.recycle-tolerance-per-component -->

- **Recycle of unreacted feed grows without bound: the reactor is too small, the solver is not at fault**
  - When: In a reactor-separator-recycle loop with fixed reactor hold-up, the recycle flow keeps growing (the snowball effect).
  - Do: Check the reactor size against the feed rate before changing solver settings.
  - Why: With fixed reactor hold-up only more recycle can raise conversion, so the loop has no finite steady state.
  - Check: In CHEPTA, reduce the feed or enlarge the reactor and see whether the loop converges. [Larsson & Skogestad 2000](https://doi.org/10.4173/mic.2000.4.2) discuss this as a control and design problem; reading it as a simulation symptom is Lab's.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 6, p. 230. <!-- larsson-skogestad-2000-plantwide.snowball-means-reactor-too-small -->

- **Solvent loop does not close: choose the tear on purpose and add make-up streams**
  - When: A recycled solvent loop does not converge.
  - Do: Choose the tear stream (the recycle stream that is guessed and recomputed) deliberately, and add make-up streams for every component lost from the loop, such as solvent losses, calculated to close the balance.
  - Why: Losses drain the loop unless they are made up.
  - Check: In CHEPTA, check the solvent balance: make-up equals the losses in all outlets.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': process modelling and simulations. <!-- palomar-2024-il-process-simulation.tear-and-make-up -->
