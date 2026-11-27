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

**The maintainer's rules (2026-11-27; full text in SIMULATION_PRACTICES.md, rules A to H):**
- A. No plant starts until every chemical, property and needed pair parameter is in the pinned CHEPTA. List and report what is missing first. Pairs may be estimated by a CHEPTA predictive method; a missing component may not.
- B. Build one unit at a time from a chosen start (feed, reactor inlet or pre-treatment). Check each unit's mass balance before the next. Work around a failure, then find out why. Close each recycle when the build reaches it. If a unit sends a stream back and the flowsheet then continues, solve that recycle first, if possible, before adding the next units. Explain any other order.
- C. Record why each new design choice was made (paper text, literature, or what later units show).
- D. Near a purity specification, find the product's real use (what the factory is for; grades differ) and what that use accepts (literature, standards, datasheets) before chasing digits. Judge flows too.
- E. One property method for the whole plant, chosen for CHEPTA, not copied from the paper. A column or unit may have its own where CHEPTA allows it and it clearly helps.
- F. For each capability request, judge whether it is likely to be solved and name the alternative available today.
- G. After each closed loop, compare every flow with the paper's: a flow 10 or 100 times larger is probably a mistake.
- H. Report each run's time.

**Run a paper case in this order**

1. Read the engine pin. Declare the boundary, fixed inputs, adjustable settings, target streams, units and tolerances. Check that the release covers the components, phases and parameter ranges.
2. Audit the source balances. Run each unit on the paper’s inlets and settings. Keep the result or refusal as the baseline.
3. Connect the units in sections. Count independent specifications for the plant. Close each cycle with a tear (a stream whose inlet is guessed and recomputed). Use the pinned solver’s automatic selection or supply a tear set with defensible guesses. Start with its default, Broyden on 0.6.2.
4. When a unit fails, capture its actual inlet from the loop. Reproduce the failure alone. Check phase, units, bounds and specifications before varying a setting inside its justified range. Record the smallest successful adjustment and every failed run.
5. Tighten the recycle tolerance from the saved state. Compare each tear’s component flows, external balances, duties, purity and recovery. Report solve status, target verdicts and agreement with independent evidence separately.
6. Pair a design target with a free variable and justified bounds. On 0.6.2, run a series of explicit requests and keep each result. Flowsheet-wide `designSpecs` is documented on [upstream commit 415da41](https://github.com/FaireDose/CHEPTA/blob/415da41d531cd5b5701d0d13550f98c9888abced/docs/models/flowsheet.md). Label any test of that commit separately from the release.

**When a unit fails or misses a target, look up what is known first** (in this order, never the record files whole):
1. the "Simulation" section of `dataset/index/problems.md`: one line per operation and symptom;
2. `python scripts/kb.py query --operation distillation --symptom no-convergence` (symptoms: `python scripts/kb.py terms`);
3. `python scripts/kb.py show <row id>` for one row.
If a row informed what you tried, add `{"row": <its id>, "helped": "yes|no|partly", "note": ...}` to `keys.informed_by`
of your own case row, never to the rule's row. Add what your case learned as a keyed row with a `symptom`.

**Capability requests.** If no nearby feasible setting works, reduce the issue to one input and include the version, exact response, expected behaviour and evidence. A balance violation or contradiction with a documented contract can demonstrate an implementation problem. A difference from another simulator calls for checking assumptions and property data. Comparison with measurements addresses physical accuracy. [Oberkampf & Trucano, verification and validation benchmarks](https://doi.org/10.1016/j.nucengdes.2007.02.032)

**Keep:** every run, failures included, with CHEPTA's code and message and the CHEPTA version or commit. Never edit
old results.

**Open only when needed:**

| For | Go to |
|---|---|
| A worked example with every run (the ethyl acetate plant) | [cases/ethyl-acetate-piotrowski-2021/CONVERGENCE_PRACTICES.md](../../../cases/ethyl-acetate-piotrowski-2021/CONVERGENCE_PRACTICES.md) |
| What the pinned CHEPTA can do | CHEPTA's docs at the pinned tag (the npm package has none): [v0.6.2/docs](https://github.com/FaireDose/CHEPTA/tree/v0.6.2/docs), `models/` and `decisions/`; the pin is in [package.json](../../../package.json) |
| How a case compares with its paper | a case's README or COMPARISON.md, e.g. [methanol](../../../cases/methanol-co2-campos-2022/README.md) |
| The case sheet (CHEPTA's own drawing and tables) | [docs/HANDOVER.md](../../../docs/HANDOVER.md), queue item 0 |
