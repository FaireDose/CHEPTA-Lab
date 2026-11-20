# Simulation practices for every case

Every worker that runs a plant or a unit in CHEPTA follows this page. The coordinator puts it in every case task and
checks the report against it (the maintainer, 2026-11-20: "you will be responsible to guide the workers to use this
skill of simulation practices").

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

1. **Run each unit alone, with the paper's inlet streams.** A unit that does not solve alone will not solve in the
   loop.
2. **Balance the paper around the unit first** (arithmetic on its stream table). The paper's own numbers can be
   inconsistent; find that before blaming CHEPTA.
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
   saturation where a unit refuses vapour.

### 2. Specifying the whole plant

6. **Count the plant's degrees of freedom, not only each unit's.** Do not fix both a feed and every outlet. Fix one
   flow inside the recycle and let an outlet follow.
7. **Never fix a product flow above what the reaction makes.**
8. **Specify columns by outlet purity where CHEPTA converges; else by a flow tuned to reach that purity (M).**
9. **Check the key component's balance around any column whose purity falls short.** Also check an excess reactant
   with no exit of its own: it builds up in the loop and sets the product purity. Check the feed ratio before tuning
   columns.

### 3. The recycle loop

10. **Mark every recycle as a tear stream, with a guess from the paper's table.**
11. **Broyden (the default) first.** Try direct substitution or Wegstein only if it fails.
12. **Set the tolerance to what the loop can reach. Then tighten it from the saved answer:** a loose tolerance can
    hide a slow build-up. Compare each component's inventory in the recycles between two tolerances.
13. **Save the converged recycle streams as starting values**, and start later runs from them. A start close to the
    answer is worth more than a different solver method.
14. **After convergence, look for blown-up flows:**
    - every stream against the paper's;
    - column internal flows against their feeds;
    - the plant balance per component, checked from the result.

### 4. What the case reports

- **The adjustment table** (one row per changed setting):

  | Unit | Setting | Paper | Ours | Change | Why | Runs |
  |---|---|---|---|---|---|---|

- **The comparison** stream by stream at the column ends, the recycles and the products, with the differences.
- **What did not help**, with its runs: it saves the next worker the same attempts.
- **Capability requests**, only those that pass the test above.
- **The case sheet from CHEPTA's own workbench** (drawing, stream table, duties) when the plant closes.

Keep every run, including failures, with CHEPTA's code and message. Never edit old results.
