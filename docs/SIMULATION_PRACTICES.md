# Simulation practices for every case

Every worker that runs a plant or a unit in CHEPTA follows this page. The coordinator puts it in every case task and
checks the report against it (the maintainer, 2026-11-20: "you will be responsible to guide the workers to use this
skill of simulation practices").

AI sessions reach this page through the solving-simulations skill (`.claude/skills/solving-simulations/`).

It was drawn from the ethyl acetate plant, which the maintainer worked through with a worker on 2026-11-13 and 14. The
details and the runs that show each point are in
[cases/ethyl-acetate-piotrowski-2021/CONVERGENCE_PRACTICES.md](../cases/ethyl-acetate-piotrowski-2021/CONVERGENCE_PRACTICES.md).
**M** marks the maintainer's own advice.

## The principle

**The paper's settings belong to the paper's thermodynamics (M, 2026-11-19).** The authors chose a condenser
temperature, an approach temperature, a reflux ratio or a distillate flow with their own property model and simulator.
CHEPTA's model is slightly different, so the same setting can fail, or can converge to a different purity. So:

- **Match what matters**: product purities and recoveries, the limits the paper states, and the mass and energy
  balance. The paper's setting itself is a starting point, not a target.
- **The plant must converge, even with small deviations from the paper's tables (M, 2026-11-13).** Purities at the
  column ends matter more than flows.
- **Scan each setting around the paper's value** to find where CHEPTA converges and where it meets the targets. Take
  the smallest change that works.
- **Record every adjustment** in the case's adjustment table (below): the paper's value, ours, the size of the change,
  why, and the runs. An adjustment is never hidden and never presented as the paper's value.
- **A small adjustment that works is not a CHEPTA bug.** A capability request goes to CHEPTA only when no setting near
  the paper's works, or when CHEPTA's answer contradicts itself. Its message must contain one small input file,
  CHEPTA's exact outcome and what CHEPTA should have done.

## The steps

### 1. Each unit alone

1. **Audit the paper around the unit** on a common flow, composition and energy basis. Include stoichiometric production or consumption for reacting species, or check conserved elements.
2. **Run each unit on the paper’s inlet streams.** Keep the source settings for the first attempt. If the connected unit fails later, replay its actual inlet as well. A recycle can change the inlet phase and composition.
3. **Scan the unit's settings around the paper's values (M):**
   - condenser temperature;
   - reflux ratio;
   - distillate or bottoms flow;
   - purity;
   - exchanger approach;
   - flash temperature and pressure;
   - the number of stages if the paper gives a range.
   Note where it converges, where it meets the paper's purity or limit, and where it fails.
4. **Test the paper's own thermodynamic statements in CHEPTA:**
   - an azeotrope;
   - a solubility;
   - a trend the authors describe.
   This separates a property difference (adjust the setting) from a balance that cannot work in either model.
5. **Allow every phase that can form** (two liquids: `phases: "VLL"`). Bring a stream that must be liquid to
   the required phase only when conditioning is physically justified. Record any added heater or cooler, its duty and the resulting change to the source flowsheet.

### 2. Specifying the whole plant

6. **Count the plant's degrees of freedom, not only each unit's.** Do not fix both a feed and every outlet. Fix one
   flow inside the recycle and let an outlet follow only when that choice supplies a missing independent specification. Write down which flow or other result is then free.
7. **Bound the target component flow.** Its flow in net product cannot exceed its fresh-feed input plus net production after accounting for other exits. A total product stream can also contain impurities.
8. **Specify columns by outlet purity where CHEPTA converges; else by a flow tuned to reach that purity (M).**
9. **Check the key component's balance around any column whose purity falls short.** Also check an excess reactant
   with no exit of its own: it builds up in the loop and sets the product purity. Check the feed ratio before tuning
   columns.

### 3. The recycle loop

10. **Choose tears that break every cycle.** On 0.6.2 CHEPTA selects a set automatically if none are marked. Mark streams explicitly when the published states give better guesses. The five marked tears in the ester case are one worked example. [CHEPTA 0.6.2, flowsheet solver](https://github.com/FaireDose/CHEPTA/blob/v0.6.2/docs/models/flowsheet.md#flowsheet-solver-layer-5)
11. **Broyden (the default) first.** Try direct substitution or Wegstein only if it fails.
12. **Set the tolerance to what the loop can reach. Then tighten it from the saved answer:** a loose tolerance can
    hide a slow build-up. Compare each component's inventory in the recycles between two tolerances.
13. **Save the converged recycle streams as starting values**, and start later runs from them. A start close to the
    answer is worth more than a different solver method.
14. **After convergence, look for blown-up flows:**
    - every stream against the paper's;
    - column internal flows against their feeds;
    - each nonreacting component and each conserved element across the plant boundary, with energy inputs and outputs on a common reference basis.

### Troubleshooting from the observed symptom

| What the agent observes | Next check | Evidence to keep |
|---|---|---|
| The first unit refuses the given feed | Check pressure units and composition basis, then expected phases, parameter coverage and operating range. Inspect an isolated flash or equilibrium point when a missing parameter, extrapolation or material mismatch affects the decision. | Actual inlet, method, parameter warning and unit response. Carlson, “Don’t gamble with physical properties for simulations”, *Chem. Eng. Prog.* 92(10), 35–46 (1996) |
| Units run separately but a section fails | Check connectivity, independent specifications and bounds. Propagate a once-through solution downstream before reconnecting the recycle. Use the first failing inlet to isolate the unit. | Section boundary, guesses, failing inlet and residual if reported. [Lee et al., §4.7](https://doi.org/10.1002/amp2.10095) · [IDAES diagnostics workflow](https://idaes-pse.readthedocs.io/en/stable/explanations/model_diagnostics/index.html) |
| The loop closes but purity drifts when the tolerance is tightened | Inspect the component with the largest change in recycle flow and identify its net exits. In the ester case, tightening from a saved state moved product purity from 99.67 to 99.11 mass %. | Both run IDs, achieved tolerances, component flows and the product verdict. [Ester case, practice 12](../cases/ethyl-acetate-piotrowski-2021/CONVERGENCE_PRACTICES.md) |
| A column converges but misses a target | Check the key component balance and compare stage temperature and composition profiles as well as end products. Check duties where enthalpies and reference states are comparable. | Residual or solver status, balance residuals in engineering units and the target deviation. [Kooijman & Taylor, The ChemSep Book, §§1.2–1.3](https://www.chemsep.org/downloads/docs/book2.pdf) |

Set the allowed adjustment range from the paper, model validity or an explicitly reasoned assumption. Keep mandatory product and operating limits fixed. When scanning a target, record which feasible points bracket it and any intervening failures or phase changes. If no feasible bracket emerges, report the tested range and the unmet target. The [ethyl acetate adjustment history](../cases/ethyl-acetate-piotrowski-2021/README.md) illustrates the distinction between a solvable setting and a feasible product.

### 4. What the case reports

- **The adjustment table** (one row per changed setting):

  | Unit | Setting | Paper | Ours | Change | Why | Runs |
  |---|---|---|---|---|---|---|

- **The comparison** stream by stream at the column ends, the recycles and the products, with the differences.
- **What did not help**, with its runs: it saves the next worker the same attempts.
- **Capability requests**, only those that pass the test above.
- **The case sheet from CHEPTA's own workbench** (drawing, stream table, duties) when the plant closes.

Keep every run, including failures, with CHEPTA's code and message. Never edit old results.
