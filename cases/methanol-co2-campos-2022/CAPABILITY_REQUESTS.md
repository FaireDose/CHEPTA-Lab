# Capability requests from the methanol case (chepta 0.6.2), for CHEPTA's sessions

**Status on CHEPTA's unreleased main, commit 415da41d531cd5b5701d0d13550f98c9888abced (to become 0.6.3), checked
2026-11-19:** see [the section at the end](#status-on-chepta-main-415da41-2026-11-19). In short: M1, M3 and M5 fixed;
M2 and M4 fixed on the inputs below but not on the plant's own streams; one new request, M6.

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

## Status on CHEPTA main 415da41 (2026-11-19)

Checked by a CHEPTA-Lab worker session on a source checkout of commit 415da41d531cd5b5701d0d13550f98c9888abced (its
package.json still says 0.6.2; Lab's pin is unchanged). Runs in [results-chepta-main-415da41/](results-chepta-main-415da41/),
made by [run_chepta_main_415da41.py](run_chepta_main_415da41.py); `rerun-<id>` is the 0.6.2 input file of that id, unchanged.

| Request | On 415da41 | Evidence (run, CHEPTA run id) |
|---|---|---|
| M1 column start with ppm of CO, N2 | **fixed for the column.** The column converges with H2, CO, N2 in its feed, with either condenser, alone and in the closed plant. The feed's own bubble point at 100 kPa is still refused with the same message (no claim that it exists) | rerun-u-column-partial-pr (run-mwo4qg3j-1, 6 Newton iterations), vl-column-full (run-mwo4pnmn-1), plant-vl-share-warm-nobypass (run-mwo51p8n-1); rerun-diag-feed29-bubble-plus-CO, -plus-N2, rerun-mini-bubble-CO-1000ppm still `NO_CONVERGENCE` |
| M2 purity / recovery inside the scanned range | **partly.** The refusal is now honest: `NO_CONVERGENCE`, "lies inside the range ... but the stage solver did not converge on the columns where it is met ... This is not a statement that the specification cannot be met" (was `OUT_OF_RANGE`). With the vapour + liquid condenser and the paper's feed the purity 99.985 % is met (2 iterations). On the 0.6.2 input files and on the plant's own column feed it is still not solved | vl-column-CO2-MeOH-H2O-purity (run-mwo4q2dt-1, ok); rerun-u-column-partial-flash53-purity (run-mwo4vppn-1), rerun-diag-column-recovery-0.99987 (run-mwo4x54v-1), plant-vl-share-warm-purity (run-mwo4xkfu-1), plant-vl-recovery: `NO_CONVERGENCE` |
| M3 Newton capped at 12 | **fixed.** `max_iterations` 5 and 100 are honoured and named in the message ("it stopped at its iteration limit (maxIterations = 100)") | rerun-diag-column-partialside-T53-CO2-MeOH-H2O-maxit100, -maxit5; plant-vl-boilup-maxit100. The side-draw column itself still does not converge; it is no longer needed (M5) |
| M4 2 K approach searched on 10 zones | **fixed on the paper's streams, not on the plant's.** u-he5-dTmin2 now solves without `zones` (114,535 kW, cold outlet 84.93 C; 0.6.2 with `zones: 10`: 114,966 kW, 84.99 C). With the streams 20 and 28 of Lab's converged plant it is refused as a temperature cross at the duty the search found | rerun-u-he5-dTmin2 (run-mwo4qufd-1, ok); **he5-a6streams-dTmin2** (run-mwo4xhko-1, below) |
| M5 vapour + liquid condenser | **added** (`condenser: "vapour_liquid"`, proposal 0026). Paper feed 29, 53 C, R 2, bottoms 4581: liquid distillate 4532.7 kmol/h at 99.835 % methanol, vapour 298.3 kmol/h (paper 4542 at 99.667 %, 289), 27 Newton iterations | vl-column-full (run-mwo4pnmn-1) |

### M4, still open: the approach search ends on a temperature cross

- **Input:** `results-chepta-main-415da41/he5-a6streams-dTmin2.request.json`: hx, `dTmin_K: 2`, default zones and
  arrangement (counterflow); hot = stream 20 and cold = stream 28 of Lab's converged plant (plant-a6, chepta 0.6.2: hot
  126.45 C, cold 30.0 C at 100 kPa, 9168 kmol/h, VF 0.04 at 72 C).
- **Outcome:** `invalid_input`, `BAD_INPUT`: "Heat exchanger HE5: Temperature cross: where 82150 kW of 96640 kW has left
  the hot side, the hot side is at 72.18 °C and the cold side at 72.46 °C. Heat cannot flow there: lower the duty, change
  an outlet." With `zones: 10` the same request returns 96,643 kW (he5-a6streams-dTmin2-zones10, run-mwo4xjwv-1), the
  duty the 20 zones call a cross. In the plant (plant-vl-he5-nozones, plant-vl-share-warm-nobypass-nozones) the loop stops
  on it at iteration 2.
- **Expected:** the duty at which the zones used for the answer give 2 K (somewhat below 96.6 MW), never a duty that the
  same exchanger then refuses as a cross; the repeated search with the full zones (heat-exchange.js, "M4, 2026-11-14")
  does not seem to be reached when the check throws a cross rather than returning an approach below 2 K.

### M6 (new). The vapour + liquid condenser given by its temperature does not converge where the same column exists

- **Input:** `results-chepta-main-415da41/vl-column-a6feed-T53.request.json`: the column alone (30 stages, feed 24,
  100 kPa, `condenser: "vapour_liquid"`, `condenser_T_K: 326.15`, reflux ratio 2, bottoms 4581 kmol/h, PR), fed with
  the column feed of Lab's converged plant (stream 29-col of plant-a6: 9167.9 kmol/h, CO2 0.2425 %, methanol 49.737 %,
  water 50.0205 %, 83.2 C, 100 kPa). The paper's own feed (CO2 1.285 %) converges.
- **Outcome:** `not_converged`, `NO_CONVERGENCE`: "Newton from the bubble-point start ... (12 iterations ...: the
  residual fell only from 0.0599 to 0.05859 ...); continuation in the relative volatilities (stopped at 0 % of the way
  ...); Newton resumed ... (100 iterations in all ...: 88 iterations were not enough) ... With the vapour + liquid condenser
  the reflux ratio is the reflux over the liquid distillate (L1 / U1): a small liquid distillate (a large vapour share)
  means a small reflux; give the reflux by another specification ...".
- **Evidence the column exists:** the same input with `vapour_distillate_kmol_h: 38.56` or `vapour_share: 0.008406`
  in place of the temperature converges in 4 Newton iterations at **53.005 C** (vl-column-a6feed-V38.56, run-mwo4wbrw-1;
  vl-column-a6feed-share, run-mwo4wfg6-1). The hint in the message does not apply: the vapour share is 0.8 %, not large.
- **Effect on the plant:** every closed-plant run with `condenser_T_K` stops in the column (plant-vl, -nobypass,
  -R2.1273, -he5-nozones, -purity, -boilup, -warm, -warm-direct, -recovery): from the paper's start at loop iteration 3,
  after a Broyden step; started from Lab's converged plant on the first pass. With `vapour_share` the plant converges
  (plant-vl-share-warm, 2 loop iterations; plant-vl-share-warm-nobypass, with the traces in the column).
- **Expected:** with the temperature given, start from the column that the other two specifications reach (for example
  solve first at a vapour share from a flash of the top vapour at that temperature, then switch the specification, as
  the form already does when the user switches); and name the low-CO2 case in the message rather than "a large vapour
  share".

## chepta 0.6.3 (2026-11-27)

Runs in [results-chepta-0.6.3/](results-chepta-0.6.3/README.md), Lab's pin `chepta@0.6.3` (npm; the result header
reports commit 8b8b64f with local changes, the release notes b6598a5). Only the runs the 0.6.3 advice changes were made.

### The earlier requests on 0.6.3

| Request | On 0.6.3 | Runs |
|---|---|---|
| M1 column start with ppm of H2, CO, N2 | **answered**: the column alone and the closed plant run with the traces in the feed | col-*, plant-pr |
| M2 purity or recovery refused inside the scanned range | **partly**: a recovery of 0.955 and a component ratio of 5e-5 converge; at the paper's values they run out of time (M9) | col-mhv1-recMeOH*, col-mhv1-ratioB* |
| M3 Newton capped at 12 | not re-run (answered on 415da41) | |
| M4 2 K approach | **answered**: without `zones`, on the paper's streams and on the 0.6.2 plant's streams (2.000 K along the exchanger) and in the closed plant | u-he5-dTmin2-pr, u-he5-a6streams-dTmin2-pr, plant-pr |
| M5 vapour + liquid condenser | in use | |
| M6 condenser by its temperature in the closed plant | **answered**: the closed plant converges with the paper's 53 C from the paper's start (29 iterations) | plant-pr, plant-pr-warm |

### M7 (new). A P-H flash on PR + MHV1 finds no physical root for H2 + CO2 + water

- **Input:** `results-chepta-0.6.3/mini-ph-H2-CO2-H2O-mhv1.request.json`: components hydrogen, carbon dioxide, water;
  `thermo: { model: "PR", mixing: "MHV1" }`; feed 1.55 / 76.245 / 2.139 kmol/h (the mole % of stream 39-REC, supplement
  Table S10, p.15), 306.15 K, 100 kPa; a heater with `duty_kW: 0` (adiabatic, a P-H flash).
- **Outcome:** `not_converged`, `NO_CONVERGENCE`: "Heater / cooler H1: PR: no physical root at 31.355135405253932 K,
  100 kPa."
- **Evidence:** the same input on PR (k_ij) returns 306.15 K (mini-ph-H2-CO2-H2O-pr, ok); on PR + MHV1 with `T_K: 306.15`
  in place of the duty it is ok (mini-tp-H2-CO2-H2O-mhv1); H2 + water, CO2 + water, H2 + CO2 alone on PR + MHV1 are ok
  (mini-ph-*-mhv1). The inlet's own state is found (the feed solves), so the temperature search of the P-H flash goes
  to 31 K for an enthalpy that 306.15 K has. On the paper's inlets the same message stops MIXER1 (84.2 K), MIXER4,
  VALVE1 (67 K), HE4, HE5, HE6 (40.0 K at 6925 kPa); in the plant and the two sections it is the first stop
  (plant-mhv1, sec-compression-mhv1, sec-loop-mhv1).
- **Expected:** the P-H flash returns 306.15 K for its own inlet enthalpy (zero duty), as on PR; a temperature search
  bounded to where the method has physical roots.

### M8 (new). A T-P flash on PR + MHV1 is refused as a possible liquid-liquid split

- **Input:** `results-chepta-0.6.3/mini-tp-cp3-300K-7000kPa-mhv1.request.json`: the six components, PR + MHV1, the
  composition CHEPTA reported for CP3 in run plant-mhv1-warm (`error.details.z`: CO2 0.98195, H2 0.00162, CO 0.00009,
  methanol 0.01166, water 0.00439, N2 0.00029), 100 kmol/h, a flash at 300 K and 7000 kPa.
- **Outcome:** `unsupported`, `PHASE_SPLIT`: "Flash drum FL: PR flash at 300.00 K and 7000.00 kPa: the feed is not
  stable as one phase (tangent-plane distance -0.6174), but no vapour-liquid split was found; it may split into two
  liquids, which is not supported yet with an equation of state."
- **Evidence:** on PR (k_ij) the same flash gives one liquid, 100 kmol/h (mini-tp-cp3-300K-7000kPa-pr). Nearly pure CO2
  at 300 K and 70 bar is just above its vapour pressure (about 67 bar), a liquid; a tangent-plane distance of -0.62 on
  one liquid of 98 % CO2 points to the MHV1 mixture term rather than to a second liquid. CP3's inlet is 45 C, 1698 kPa;
  why CP3 flashes at 300 K and 7000 kPa (a start of its outlet search?) is not visible in the result.
- **Expected:** one liquid (or a VL split if it exists) as on PR, or the refusal with the phase found.

### M9 (new). A column specification at or just beyond its reachable value runs out of time

- **Input:** `results-chepta-0.6.3/col-mhv1-BF0.48672.request.json` (the column alone on the paper's feed 29, PR + MHV1,
  vapour + liquid condenser at 53 C, R 2, `{ kind: "flow_ratio", numerator: "bottoms", denominator: "feed", value:
  0.48672 }`); also col-mhv1-recMeOH0.96115 (`recovery` of methanol in the liquid distillate) and col-mhv1-ratioB0.00015
  (`component_ratio` methanol/water in the bottoms).
- **Outcome:** `out_of_time`, `OUT_OF_TIME`: "The calculation did not finish within limits.time_ms = 300000 ms, and
  was stopped." No `details.best`. col-mhv1-BF0.485 ran out at 1,200,000 ms.
- **Evidence:** the flow ratio 0.48672 is bottoms 4581 kmol/h, which converges in 21 s as `bottoms_kmol_h`
  (col-mhv1-B4581, 99.9925 % water); 0.488 converges in 37 s. A recovery of 0.96115 lies above the most the liquid
  distillate can take at 53 C (about 0.9608, derived from col-mhv1-B4581: the vapour distillate carries 3.91 % of the
  feed methanol), and the reboiler temperature beyond its range is refused at once with the range (col-mhv1-TB374.5,
  `OUT_OF_RANGE`).
- **Expected:** a ratio that is a flow converges as the flow does; an unreachable recovery or ratio is refused with its
  reachable range, as the stage temperature is; a time-out reports the best point (feature 2).
