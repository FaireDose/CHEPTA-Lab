# Rules in plain words (generated; do not edit)

Pick a topic below; each page lists its rules, best-supported first.
Each rule starts with what to do in one line, then When (the situation you recognise), Do, Why, Check (how to verify it, in CHEPTA where it applies) and Result (what the source got), then its status and source with page. A lead is a rule from the literature that Lab has not yet tested.
Agents use [problems.md](problems.md) and `python scripts/kb.py query` instead; the plants' run logs are listed at the end.

| Topic | What it covers | Rules |
|---|---|---|
| [Property methods](rules/property-methods.md) | Wrong phases or volatilities: which thermodynamic model and parameters to use and check | 8 |
| [Recycle convergence](rules/recycle-convergence.md) | Recycle loops, tears, make-ups and flashes inside loops that do not close | 6 |
| [Column convergence](rules/column-convergence.md) | Columns that fail, are slow or miss a target: starting profiles, solvers, steady states | 22 |
| [Inherent safety](rules/safety.md) | Safer routes from the first flowsheet: principles, indices and missing hazard data | 8 |
| [Heat integration](rules/heat-integration.md) | Pinch analysis, heat pumps, vapour recompression, using process heat | 15 |
| [Reactive distillation and esterification](rules/reactive-distillation.md) | Reaction and separation in one unit: feasibility, column design, catalysts, water-removing membranes | 29 |
| [Azeotropes and two liquid phases](rules/azeotropes.md) | Breaking azeotropes: entrainers, solvents, decanters, pressure swing | 27 |
| [Reactors, routes and recycles](rules/reactors-recycles.md) | Reactor type, route choice, reactant recycles and purges | 19 |
| [Separation choice and distillation design](rules/separation-choice.md) | Which separation to use, column pressure, sequences, extraction, absorbers | 30 |
| [Rules not yet in plain words](rules/not-yet-plain.md) | Literature rules still in their one-line form, until they are rewritten | 1 |

## The plants: lessons, then their run logs

| Case | Lessons | Rows in the run log |
|---|---|---|
| [ethyl-acetate-piotrowski-2021](plants/ethyl-acetate-piotrowski-2021.md) | 16 | 64 |
| [methanol-co2-campos-2022](plants/methanol-co2-campos-2022.md) | 14 | 48 |
| [pilot](plants/pilot.md) | - | 3 |
