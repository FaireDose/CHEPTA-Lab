# Recycle convergence (generated; do not edit)

Recycle loops, tears, make-ups and flashes inside loops that do not close. 4 rules. [All topics](../rules-readable.md)

Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.

- **Some flowsheet cases fail but all converge with another flash routine: suspect the flash, not the recycle solver**
  - When: In a parametric study some cases of a flowsheet fail, and swapping in another flash routine makes them all converge.
  - Do: Test the flash on the failing streams alone before changing the recycle solver.
  - Why: A phase-split calculation that jumps between iterations breaks the outer recycle loop.
  - Check: In CHEPTA, rerun each failing unit on its captured inlet with the same phases setting; if it fails alone, report it as a flash case. Andreasen 2022 says this indicates, not proves, the cause.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Andreasen 2022, *Evaluation of an Open-source Chemical Process Simulator…* (https://doi.org/10.3311/PPch.19678), Results, p. 508; Discussion, p. 509. <!-- andreasen-2022-dwsim-evaluation.flash-instability-not-solver -->

- **Recycle loop converged on total flow: check each component as well**
  - When: A recycle loop reports convergence, but compositions still drift or the plant balance does not close for one component.
  - Do: Check the closure of each tear stream (the recycle stream that is guessed and recomputed) component by component, not only its total flow. Andreasen 2022 accepted recycle balance errors below 1 kg/h.
  - Why: A tolerance on total flow can be met while one component is too high and another too low.
  - Check: In CHEPTA, compare each tear's component flows between two tolerances, and check the plant's component balance (fresh feed plus production equals products) for every component.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Andreasen 2022, *Evaluation of an Open-source Chemical Process Simulator…* (https://doi.org/10.3311/PPch.19678), Section 2, p. 506. <!-- andreasen-2022-dwsim-evaluation.recycle-tolerance-per-component -->

- **Recycle of unreacted feed grows without bound: the reactor is too small, the solver is not at fault**
  - When: In a reactor-separator-recycle loop with fixed reactor hold-up, the recycle flow keeps growing (the snowball effect).
  - Do: Check the reactor size against the feed rate before changing solver settings.
  - Why: With fixed reactor hold-up only more recycle can raise conversion, so the loop has no finite steady state.
  - Check: In CHEPTA, reduce the feed or enlarge the reactor and see whether the loop converges. Larsson & Skogestad 2000 discuss this as a control and design problem; reading it as a simulation symptom is Lab's.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Larsson & Skogestad 2000, *Plantwide control - A review and a…* (https://doi.org/10.4173/mic.2000.4.2), Section 6, p. 230. <!-- larsson-skogestad-2000-plantwide.snowball-means-reactor-too-small -->

- **Solvent loop does not close: choose the tear on purpose and add make-up streams**
  - When: A recycled solvent loop does not converge.
  - Do: Choose the tear stream (the recycle stream that is guessed and recomputed) deliberately, and add make-up streams for every component lost from the loop, such as solvent losses, calculated to close the balance.
  - Why: Losses drain the loop unless they are made up.
  - Check: In CHEPTA, check the solvent balance: make-up equals the losses in all outlets.
  - Status: lead — from the literature, not yet tested by Lab.
  - Source: Palomar et al. 2024, *Process Simulation and Optimization on Ionic Liquids* (https://doi.org/10.1021/acs.chemrev.3c00512), Section 'Methodology for Applying Process Simulations': process modelling and simulations. <!-- palomar-2024-il-process-simulation.tear-and-make-up -->
