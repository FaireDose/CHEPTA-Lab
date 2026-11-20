---
name: solving-simulations
description: Use before running any unit or plant in CHEPTA for CHEPTA-Lab (a column, a flash, a reactor, a recycle loop, a design specification), and when a run fails, misses a purity or is slow. How to make a flowsheet converge and match a paper, and when to file a capability request.
---

# Solving simulations in CHEPTA

The full practice, with its reasons, is [docs/SIMULATION_PRACTICES.md](../../../docs/SIMULATION_PRACTICES.md). Read it
the first time you run a case.

**The principle (the maintainer).** The paper's settings belong to the paper's thermodynamics:
- Match purities, recoveries and the balances. The plant must converge, even with small deviations from the paper.
- Scan each setting around the paper's value, and take the smallest change that works.
- Record every change in the case's adjustment table: unit, setting, paper, ours, change, why, runs.

**The order:**
1. Each unit alone on the paper's inlets.
2. Balance the paper around the unit, then scan its settings and test the paper's thermodynamic statements in CHEPTA.
3. Count the plant's degrees of freedom. Specify columns by purity where CHEPTA converges.
4. Tear streams with guesses from the paper; Broyden first.
5. Tighten the tolerance from the saved answer, then save the converged values as starting values.
6. Check for blown-up flows and for components building up in the loop.
7. Use a design specification (CHEPTA `designSpecs`) instead of tuning a feed or a flow by hand.

**Capability requests:** only when no setting near the paper's works, or CHEPTA contradicts itself. Each request has
one small input file, CHEPTA's exact outcome and what it should have done. A gap to a paper's own simulation (Aspen,
Chemcad) is a thermodynamics question for CHEPTA, not a bug: only measured data can show CHEPTA wrong.

**Keep:** every run, failures included, with CHEPTA's code and message and the CHEPTA version or commit. Never edit
old results.

**Open only when needed:**

| For | Go to |
|---|---|
| A worked example with every run (the ethyl acetate plant) | [cases/ethyl-acetate-piotrowski-2021/CONVERGENCE_PRACTICES.md](../../../cases/ethyl-acetate-piotrowski-2021/CONVERGENCE_PRACTICES.md) |
| What the pinned CHEPTA can do | CHEPTA's docs at the pinned tag (the npm package has none): [v0.6.2/docs](https://github.com/FaireDose/CHEPTA/tree/v0.6.2/docs), `models/` and `decisions/`; the pin is in [package.json](../../../package.json) |
| How a case compares with its paper | a case's README or COMPARISON.md, e.g. [methanol](../../../cases/methanol-co2-campos-2022/README.md) |
| The case sheet (CHEPTA's own drawing and tables) | [docs/HANDOVER.md](../../../docs/HANDOVER.md), queue item 0 |
