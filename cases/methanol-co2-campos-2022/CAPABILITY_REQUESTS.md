# Capability requests from the methanol case (chepta 0.6.2), for CHEPTA's sessions

Written 2026-11-14 by a CHEPTA-Lab worker session. Each request names one small input file in
[results-chepta-0.6.2/](results-chepta-0.6.2/) that shows the fault with `chepta request --time-ms 900000 <file>`,
CHEPTA's exact outcome, and what CHEPTA should have done. The files carry no held-out evaluation material.

## M1. The column cannot start when its feed holds a few ppm of a light gas

- **Input:** `diag-feed29-bubble-plus-CO.request.json`. A flash at VF 0 and 100 kPa of the paper's column feed (CO2 1.285 %,
  methanol 50.04 %, water 48.67 %, CO 10 ppm), PR. The same column feed with all six components, in a column:
  `u-column-partial-pr.request.json` (30 stages, partial condenser, reflux 2, bottoms 4581 kmol/h).
- **Outcome:** `not_converged`, `NO_CONVERGENCE`: "PR bubble temperature at P = 100 kPa: no two-phase solution found
  (non-finite residual from Wilson's K-values, and no sign change found between 89.8 and 748.0 K). The state is probably
  at or above the mixture's critical region ...". The column stops there, before any stage iteration, with either
  condenser (runs u-column-partial-pr, u-column-total-pr, u-column-partial-side-pr, diag-column-partialside-R49-full and
  -maxit100).
- **Evidence it is the start, not the column:** without H2, CO and N2 the same column converges in 6 to 7 Newton
  iterations (runs diag-column-total-CO2-MeOH-H2O, diag-column-partialside-R49-CO2-MeOH-H2O, u-column-partial-flash53).
  10 ppm of CO alone or 20 ppm of N2 alone is enough (diag-feed29-bubble-plus-CO, -plus-N2). The paper's Aspen column ran
  with these traces and sent 98.6 to 99.9 % of each to the gas distillate (supplement Table S2). The feed is 86 % vapour
  at its own temperature (u-column-partial-flash53, stream 29, VF 0.863).
- **What CHEPTA should do:** start the column without the feed's bubble point when it does not exist or is not found
  (for example from a T-P flash of the feed, or with the non-condensable gases placed in the top vapour), at least with a
  partial condenser. Whether a bubble point of that feed exists at 100 kPa is not claimed here; the message could say
  which component makes it fail.
- **Lab's workaround:** a component separator sends H2, CO and N2 round the column to the 53 C flash (`TRACES` in the plant).

## M2. Column design specifications refused as "out of range" although the value lies in the range CHEPTA scanned

- **Input:** `u-column-partial-flash53-purity.request.json` (paper feed 29 without the traces, 30 stages, feed 24, partial
  condenser, reflux 2, bottoms purity water 0.99985 mole). Also `diag-column-recovery-0.99987.request.json` (water
  recovery in the bottoms 0.99987).
- **Outcome:** `invalid_input`, `OUT_OF_RANGE`: "the mole fraction of Water in the bottoms cannot be 0.99985 in this
  column with reflux_ratio 2 given: over the whole range of the distillate flow (1046 to 2588 mol/s, 9 columns solved) it
  stays between 0.811208 (at 1046) and 1 (at 2588)." And for the recovery: "stays between 0.0205455 (at 2588) and 1 (at
  1046)"; details: Newton "stopped falling" at 0.9998641 against 0.99987 asked.
- **Why it is a fault:** both asked values lie inside the range CHEPTA states. The same column with bottoms 4581 kmol/h
  converges and gives water 99.998 mol % in the bottoms (run u-column-partial-flash53), so the purity 99.985 % is reachable.
- **What CHEPTA should do:** bracket the asked value between the scanned columns that straddle it and solve there; refuse
  only when the value is outside the range found, and then say so.
- **Lab's workaround:** reflux ratio 2 and bottoms 4581 kmol/h (the paper's stream 30) in the plant; a boil-up ratio
  (1.17155, CHEPTA's own) converged alone but not inside the plant loop (run plant-a5).

## M3. The column's Newton stops at 12 iterations whatever max_iterations says (confirms ethyl acetate request 12)

- **Input:** `diag-column-partialside-T53-CO2-MeOH-H2O-maxit100.request.json` and `...-maxit5.request.json` (the same
  column, 3 components, partial condenser, liquid side draw 4542 kmol/h on stage 2, bottoms 4581 kmol/h, stage 1 at 53 C).
- **Outcome:** both `NO_CONVERGENCE`. With `max_iterations: 5` the message says "Newton from the bubble-point start ...
  (5 iterations ...)"; with `max_iterations: 100` it says "(12 iterations ...)", as without the key. Inside the plant the
  same stop: run plant-a5, "Newton ... (12 iterations, 945 ms: the residual fell only from 0.05682 to 0.0147 in 12
  iterations)".
- **What CHEPTA should do:** honour max_iterations above 12, or say in the message that 12 is a fixed limit of the first
  start.

## M4. The minimum-approach exchanger refuses a counterflow exchanger and calls it "crossflow"

- **Input:** `u-he5-dTmin2.request.json`: hx, hot paper stream 20 (133.2 C, 64042 kmol/h, PR), cold paper stream 28
  (30 C), `dTmin_K: 2`, default arrangement (counterflow).
- **Outcome:** `invalid_input`, `BAD_INPUT`: "Heat exchanger HE5: a crossflow exchanger reaches its limit at 115000 kW,
  where the smallest temperature difference is still 1.65 K: it cannot approach 2 K. Put more shells in series, use
  counterflow, or give a larger minimum approach."
- **Why it is a fault:** src/units/heat-exchange.js, exchangerApproach, searches the duty with 10 zones and checks the
  result with the default zones, which find a tighter internal pinch (condensing hot side, boiling cold side); the
  message names "crossflow" for any arrangement other than shell-and-tube. With `zones: 10` the same request is solved
  (run u-he5-dTmin2-zones10: 114,966 kW, cold outlet 84.99 C).
- **What CHEPTA should do:** search with the zones it checks with (or refine the zones and search again), and name the
  arrangement actually used.
- **Lab's workaround:** `zones: 10` on HE5 in the plant.

## M5. A partial condenser with a vapour and a liquid distillate (feature)

- The paper's column (supplement p.10) has a "partial vapor-liquid condenser at 53 C": gas distillate 32 (289 kmol/h) and
  liquid distillate 31-MEOH (4542 kmol/h). CHEPTA's column has one distillate, vapour (partial) or liquid (total).
- **Lab's workaround:** partial condenser with all the distillate as vapour, then a flash at 53 C (the product split
  is the condenser's equilibrium; the reflux composition differs). A liquid side draw from stage 2 with a stage-1
  temperature specification did not start (runs diag-column-partialside-T53-*).
- **What CHEPTA could add:** a condenser that gives both distillates, specified by its temperature or by the vapour
  distillate flow.

Not requested (noted only): PR + MHV1 refuses the system because methanol + nitrogen has no NRTL parameters inside the
rule (runs u-flash3-mhv1, u-column-*-mhv1, `NOT_AVAILABLE`); the refusal is correct and documented.
