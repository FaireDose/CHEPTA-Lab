# Ethyl acetate plant (Piotrowski & Kubica 2021): classic design S2 on chepta 0.6.1 and 0.6.2

| In one look | |
|---|---|
| Paper | Piotrowski & Kubica 2021, Processes 9, 1425 (CC BY 4.0): ethyl acetate from ethanol and acetic acid; the classic plant S2 |
| Simulated | **all 19 units and 28 streams of S2** through CHEPTA's command line: on `chepta@0.6.1` each unit alone, the two halves and the plant once through (56 runs); on `chepta@0.6.2` every 0.6.1 refusal again, the units with acetic acid, each separation column alone with its specifications varied, and **the whole plant as one flowsheet with all five recycles**, with more stages and tighter tolerances, the paper's thermodynamic statements and the ethanol balance (134 runs) |
| Complete flowsheet | **Closed and settled on 0.6.2.** One CHEPTA flowsheet, acetic acid everywhere (no cut), all five recycles, splitters by flow (26 = 60,000 kg/h; recycle 23 = 95,797 kg/h), feeds at 15 C, column 15 on its bottoms purity, column 11 on R/D 3 and its distillate flow. Settled at a tear tolerance of 1e-5 (change 2.1e-6), plant balance within 0.1 kg/h of 32,461 kg/h. **Product 99.11-99.14 mass % ethyl acetate, not the paper's 99.90 %.** Starting values saved: [init-closed-plant-chepta-0.6.2-settled.json](init-closed-plant-chepta-0.6.2-settled.json) |
| Agrees with the paper | (settled closed plant, run plant62-best-init1e-4-tol1e-5) every stream within −1.2 to +6.5 % of Table A2 in flow (no blown-up flow); wastewater 25 19,919 vs 20,000 kg/h (it follows by itself); product 12,542 vs 12,434 kg/h (+0.9 %); acid in the azeotrope 0.0000 % (limit 0.005 %); wastewater organics 0.010 % (limit 0.01 %); HTXR 6 +4.7 %, HTXR 17 0.0 %, column 11 condenser +3.6 %, column 15 reboiler +7.1 %. (0.6.1, once through) azeotrope 9 within 0.01 % |
| Differs | (settled closed plant) product 99.11 % ester with 0.81 % water (paper 99.90 %, water limit 0.03 %); more ethanol circulates than in the paper (azeotrope 8: 11.6 vs 8.5 %; stream 21: 40.0 vs 31.1 %), which wets the raffinate (5.05 vs 4.70 % water) and overloads column 11 with water; reactor duty +12.9 % (conversion from the paper); column 15 condenser +16 %; column 11 reboiler −21 %. In the paper itself: the acid of column 11's feed must leave in the product (0.022 %, not 0.01 %), and column 15's 0.01 % organics limit cannot hold with the feed's acid |
| CHEPTA could not | (0.6.2) converge the loop at its default tolerance from a cold start; converge column 11 in the loop at the distillate flows that would remove the water (245-255 kmol/h from a cold start; 260-280 even from the settled start); column 5 converges and fails irregularly on neighbouring inputs; column 11 does not converge with a trace of acetic acid near the paper's product flow; column 11 on a purity answers a contradictory `OUT_OF_RANGE`; `strictRanges` did not refuse the 15 C feed; `missingPairs` not accepted in a flowsheet; an `OUT_OF_TIME` loop reports no progress (requests 8-14) |
| Reviewed by a person | no full review; the maintainer spot-checked 3 items of the 0.6.2 part on 2026-11-13 (below). Draft, written by AI sessions on 2026-11-12 (0.6.1) and 2026-11-13/14 (0.6.2) |

Study record: [study-record.json](study-record.json). Runs and CHEPTA's answers, unchanged:
[results-chepta-0.6.1/](results-chepta-0.6.1/) (56 runs, [run-manifest.json](results-chepta-0.6.1/run-manifest.json),
[comparison-s2.json](results-chepta-0.6.1/comparison-s2.json)) and [results-chepta-0.6.2/](results-chepta-0.6.2/)
(134 runs, [run-manifest.json](results-chepta-0.6.2/run-manifest.json), [comparison-s2.json](results-chepta-0.6.2/comparison-s2.json)).
Register rows this case feeds: [data/ISSUES_AND_ROUTES.md](../../data/ISSUES_AND_ROUTES.md).

**Verdict (2026-11-14, chepta 0.6.2): BLOCKED on the product purity.** The plant closes and settles as one CHEPTA
flowsheet (all recycles; tear change 2.1e-6; balance within 0.1 kg/h); every stream is within −1.2 to +6.5 % of the
paper's flow, the azeotrope and the wastewater meet their limits, but the product is 99.11 mass % ethyl acetate (0.81 %
water) against the paper's 99.90 % (water limit 0.03 %). The column 11 water balance shows why: its distillate leaves at
the water azeotrope (8.52 % water), so removing the water that CHEPTA's wetter raffinate brings needs about 255-280
kmol/h of distillate, and column 11 does not converge in the loop there (`NO_CONVERGENCE`, runs
plant62-best-init1e-4-tol1e-5-dist260/270/280). More stages do not help (36 and 38 stages: +0.01 point).
An earlier answer of this day (99.67 %, at a loose tolerance of 3e-4) had not settled: the ethanol inventory was still
rising (below, round 3).
Round 4: the purity is set by the plant's ethanol balance (excess ethanol must leave with the product); 5 kg/h less
ethanol feed gives 99.50 %; holding 99.9 % needs a design specification on the ethanol feed (request 15).
First verdict (2026-11-13, before the maintainer's advice): BLOCKED by `NO_CONVERGENCE` in column 5 in every closed
variant with the paper's own column specifications (runs plant62-* of the first table below).

## On chepta 0.6.2 (2026-11-13): closing the plant

Runner [run_s2_chepta_0.6.2.py](run_s2_chepta_0.6.2.py), flowsheet [s2_model_062.py](s2_model_062.py) (it reuses
[s2_model.py](s2_model.py), unchanged), comparison [compare_s2_062.py](compare_s2_062.py). `chepta@0.6.2` installed with
npm in a separate folder (lock entry [chepta-0.6.2.npm-lock.json](chepta-0.6.2.npm-lock.json)); Lab's `package.json`
and `data/upstream.json` not changed. Every run's version, extrapolations and estimated pairs are in the run manifest.

### The 0.6.1 refusals, sent again unchanged

| 0.6.1 run | 0.6.1 | 0.6.2 | What it means |
|---|---|---|---|
| u-htxr10-acid, u-htxr12-acid, u-htxr18-acid, u-htxr19-acid | `PHASE_SPLIT` | ok | heaters with two liquids and acetic acid work |
| u-extr8-1stage-27C-acid, u-extr8-1stage-70C | `PHASE_SPLIT` | ok | the extractor with acetic acid works (at 70 C its outlets still boil, see request 5 of 0.6.1) |
| diag-scds5-round2-inlets-VLL | `NOT_AVAILABLE` | ok, two liquids on stage 7 | two liquids in the absorber-type column 5 work |
| u-htxr2-15C, secA-feeds-17C | `OUT_OF_RANGE` | ok, with 6-7 extrapolations listed | feeds at the printed 15 C run; acetic acid's vapour pressure, liquid heat capacity and heat of vaporization are continued below their range |
| secB-mix7-adiabatic | `BAD_INPUT` (vapour to the extractor) | ok | the extractor takes up to 10 % vapour |
| u-scds11-acid-VLL (product column, paper's stream 13 with 0.01 % acid, bottoms 141.5 kmol/h) | `NOT_AVAILABLE` | **`NO_CONVERGENCE`** | no longer refused, but not solved |
| u-scds11-acid-VL, u3-scds11-bottomsflow-VL, diag-scds5-round2-inlets (phases "VL") | `PHASE_SPLIT` | `PHASE_SPLIT` | correct: one liquid was asked where two form |
| u3-extr8-1stage-70C-feed70C | `BAD_INPUT` | `BAD_INPUT` | correct: the feed is 78 % vapour |
| plant-a2-r02-A (section A, round 2, column 5 "VL") | `NO_CONVERGENCE` | `NO_CONVERGENCE` | the same request; with "VLL" the column alone converges (above) |

### Units with acetic acid against the paper (0.6.2, the paper's inlets)

X: CHEPTA listed an extrapolation for the block or for a stream the number rests on. No pair was estimated in any run
(all six UNIQUAC pairs are fitted sets; `estimated_pairs` empty everywhere).

| Unit (run) | Compared | CHEPTA 0.6.2 | Paper | Difference |
|---|---|---:|---:|---:|
| HTXR 2 from 15 C (rerun-u-htxr2-15C) | duty | 573.9 kW **X** | 535.6 kW | +7.2 % (0.6.1 from 18 C: +1.6 %) |
| Section A, feeds 15 C (secA62-paper-inlets-15C) | azeotrope 9; reactor duty | 98,388 kg/h; 14,522 kW **X** | 98,380; 13,586.2 | +0.01 %; +6.9 % (as 0.6.1) |
| Column 5, two liquids allowed (u62-scds5-VLL) | overhead 8; ester; bottoms 7 | 98,994 kg/h; 84.53 %; 14,293 kg/h **X** | 98,380; 84.78; 14,912 | +0.6 %; −0.25 points; −4.2 % (as 0.6.1: one liquid at the paper's inlets) |
| EXTR 8, 2 stages, 27 C, with acid (u62-extr8-2stage-acid) | raffinate 11; ethanol; water | 90,220 kg/h; 1.89 %; 4.85 % | 87,314; 1.86; 4.70 | +3.3 %; +0.03; +0.15 points (0.6.1 without acid: +2.6 %) |
| EXTR 8 | ester lost to the water 20 | 9.08 % | 10.72 % | −1.6 points |
| HTXR 10 with acid (rerun-u-htxr10-acid) | duty to 71 C | 2342.5 kW **X** (45 % vaporized) | 713.5 kW | ×3.3, as 0.6.1 |
| HTXR 18 / HTXR 19 with acid | duty | 1579.7 / 5680.6 kW | 4332.9 / 1541.1 kW | exchanged in the paper, as before |
| Column 15, two liquids allowed, with acid (u62-scds15-acid-VLL) | distillate 21; condenser; reboiler | 23,315 kg/h; −12,105 kW; 14,920 kW **X** | 23,405; −12,127.2; 16,136.6 | −0.4 %; −0.2 %; −7.5 % |
| Column 15 | bottoms ethanol; acetic acid | 0.151 %; 0.012 % **X** | 0.02; 0.01 | ×7 ethanol, as 0.6.1 |
| Column 11 with acid, bottoms 141.5 kmol/h (rerun-u-scds11-acid-VLL) or distillate 230.4 kmol/h (u62-scds11-acid-distillate) | — | `NO_CONVERGENCE` | — | the same column without the acid converges (u62-scds11-noacid-bottomsflow: 99.868 %, as 0.6.1) |
| Column 11 with acid, product 99.90 mass % given (u62-scds11-acid-purity) | product 16 | 2,731 kg/h (31.0 kmol/h), 99.90 % ester, 0.100 % acid **X** | 12,434 kg/h (141.5 kmol/h) | −78 %: CHEPTA meets the purity with a small product that holds all the acid; another root of the same specification |

Extrapolations CHEPTA listed (kinds, over all runs): acetic acid's vapour pressure, liquid heat capacity and heat of
vaporization below their range (15-16 C feeds); ethyl acetate's vapour pressure and ideal-gas heat capacity below 290 /
298 K; the ethanol + acetic acid UNIQUAC set below its range (cold feeds and extractor); the water + ethyl acetate
UNIQUAC set above 343.55 K (hot stages and heaters, as 0.6.1 warned). Per run: the manifest's `extrapolations`.

### The plant as one flowsheet (all five recycles)

One CHEPTA flowsheet, four components in every block, the reactor-evaporator as CHEPTA's conversion reactor with an
all-vapour outlet (`VF: 1`), recycles 7, 15, 21, 24 and 27 as CHEPTA tear streams. Splitter 9: stream 26 = 60,000
kg/h (`flow_kg_h`). Splitter 16: stream 25 = 20,000 kg/h (variant W) or stream 23 = 95,797 kg/h, 25 the rest (variant
R). With W both product and wastewater flows are fixed by the plant balance (the paper's own balance is 27 kg/h short,
[audit](STREAM_EQUIPMENT_AUDIT.md)), so column 11 takes its distillate flow from the paper (230.4 kmol/h) instead of
the product flow or purity. MIX 7 brings its outlet to saturated liquid as on 0.6.1 (adiabatic, its outlet reached 17 %
vapour in the loop and the extractor refused it).

| Run | Variant | Outcome | Tear change per iteration before the stop |
|---|---|---|---|
| plant62-W-dist | W, Broyden | `NO_CONVERGENCE` in SCDS5 at iteration 3 | 7.2 %, 1.1 % |
| plant62-R-bottoms | R, column 11 bottoms 141.5 kmol/h, Broyden | idem, iteration 3 | 11.8 %, 1.1 % |
| plant62-R-bottoms-direct / -wegstein | direct substitution / Wegstein | idem, iteration 5 / 4 | down to 0.15 % / 0.18 % |
| plant62-R-bottoms-warm, plant62-W-dist-warm | tear guesses from CHEPTA's own 0.6.1 once-through streams | idem, iteration 4 | down to 0.18 % / 0.44 % |
| plant62-R-purity-direct | R, product 99.90 mass % | idem, iteration 3 | 40 %, 23 % |
| plant62-R-bottoms-col5VL | column 5 one liquid | idem, iteration 2 | 11.8 % |
| plant62-R-bottoms-warm-col5iter100 | column 5 `max_iterations` 100 | idem, iteration 2 (still 12 Newton iterations reported) | 11.5 % |
| plant62-R-bottoms-open, -mix7adiabatic-open, plant62-frac-bottoms-open | 27 and 21 fed from Table A2 | water loop: extractor "one liquid" at iteration 50; extractor feed 17 % vapour; column 11 `NO_CONVERGENCE` | — |

Every closed variant passes column 11 (with CHEPTA's own, nearly acid-free stream 13), column 15 and the extractor in
its first iterations; each stops in column 5, whose message suggests turning on two liquids although they are on
(`phases: "VLL"`). Column 5 alone with the inlets of round 2 of 0.6.1 converges on 0.6.2 in 7 iterations with two
liquids on stage 7. **Lab did not close the loop by any other means** (no component split, no cut).

### Strict data and missing pairs (0.6.2's new defaults)

| Run | Setting | Outcome |
|---|---|---|
| plant62-W-dist-strictRanges, -solverStrict | `options.strictRanges: true`; `solver.strictRanges: true` | `NO_CONVERGENCE` in column 5, as without |
| u-htxr2-15C-strictRanges, -solverStrict | the same, on the 15 C feed | **ok, 6 extrapolations listed**: not refused, although 0.6.1 refused it and 0.6.2 says strict mode "restores the refusals" |
| u62-extr8-2stage-acid-strictRanges | `options.strictRanges: true` | ok, 2 extrapolations listed |
| plant62-W-dist-refusePairs, u-htxr2-15C-refusePairs | `thermo.missingPairs: "refuse"` | `BAD_INPUT`: "flowsheet.thermo: unknown key "missingPairs". Known: model, vapour, sets, prefer, solids, mixing." No number changes: no pair was estimated anyway |

### Capability requests to CHEPTA from 0.6.2

| # | Request | Outcome and message | Evidence |
|---|---|---|---|
| 8 | Column 5 (absorber, 8 stages, VLL, acetic acid) inside the closed plant: Newton stops after 12 iterations and the continuation at 0 % | `not_converged` `NO_CONVERGENCE` (above); the message advises turning on VLL although it is on | plant62-* (10 closed runs) |
| 9 | Product column 11 (35 stages, R/D 3, VLL) with 0.01 mass % acetic acid in the feed | `NO_CONVERGENCE` with the bottoms or distillate flow; with the purity given a 31 kmol/h root | rerun-u-scds11-acid-VLL, u62-scds11-acid-distillate, u62-scds11-acid-purity |
| 10 | `strictRanges: true` does not refuse the acid feed at 15 C (request.options and solver) | `ok` with 6 extrapolations | u-htxr2-15C-strictRanges, u-htxr2-15C-solverStrict |
| 11 | `missingPairs` cannot be given in a flowsheet | `invalid_input` `BAD_INPUT` "flowsheet.thermo: unknown key "missingPairs"" | plant62-W-dist-refusePairs |
| 12 | A column's `max_iterations` does not raise the 12 Newton iterations reported | column 5 still "12 iterations" | plant62-R-bottoms-warm-col5iter100 |

### Round 2 (the maintainer's advice, 2026-11-13): each separation block alone, then the plant again

The maintainer: the plant must converge even with small deviations from the tables, and the purities at the ends of
the distillation columns matter more than the flows; where the plant blocks, isolate the block in CHEPTA and vary its
inlet and outlet specifications to tell a CHEPTA problem from one inherent to the paper. Runs `iso-*` (each block
alone, the paper's inlets, two liquids allowed) and `plant62-*-col15*` (the plant again).

**Is 20,000 kg/h a specification?** The paper does not say so (searched: Sections 2, 3.3, 3.5, Tables 1, 2, A1-A3).
Tables A1-A3 show it behaves like one: wastewater 25 is round in all three plants (S1 20,000; S2 20,000; S3 30,000
kg/h) while the fresh water 17 is not (17,464; 17,478; 27,618 kg/h), and stream 26 is round too (60,000 in S1 and
S2). Lab's reading: 25 (and 26) were set, and 17 is the make-up that closes the water balance. Table 2's "Wastewater
1.61 t/t product" is 20,000 / 12,434 = 1.608. CHEPTA has no make-up controller (a design specification on a feed), so
variant W fixes 25 with 17 fixed, and the product flow then follows from the balance.

**Column 5 alone** (`iso-scds5-*`, reflux 27 varied, vapour 6 the paper's or CHEPTA's own of round 2):

| Reflux 27 | Paper's vapour 6: acid in 8 (limit 0.005 %, p.6) | CHEPTA's round-2 vapour 6 |
|---|---|---|
| 45,000 kg/h | `NO_CONVERGENCE` | `NO_CONVERGENCE` |
| 50,000 | 0.055 % (misses the limit) | 0.035 % |
| 55,000 | 0.0036 % | `NO_CONVERGENCE` |
| 60,000 (paper) | 0.0004 % | 0.0000 % |
| 65,000 | 0.0004 % | 0.0000 % |
| 70,000 | `NO_CONVERGENCE` (three-phase flash, K-values) | 0.0000 % |

The paper's column balances (Table A2, 27 + 6 = 8 + 7 within 3 kg/h per component) and its 60,000 kg/h meets the acid
limit with margin; with 8 stages about 55,000 kg/h (R/V 0.58) is the least that does (the paper's R/V > 0.5 is for 14
stages). **CHEPTA's problem, not the paper's:** the column converges and fails irregularly on neighbouring inputs
(55,000 with the round-2 vapour), which is what stops the closed plant (request 8).

**Column 11 alone** (`iso-scds11-*`, the paper's feed 13, R/D 3, product flow given):

| Product 16 | Without acetic acid | With the paper's 0.01 % acid (also 0.001 and 0.005 % at 141.5) |
|---|---|---|
| 139 kmol/h | 99.998 mass % ester | 99.978 % ester, **0.022 % acid** |
| 140 | 99.942 % | `NO_CONVERGENCE` |
| 141 | 99.892 % | `NO_CONVERGENCE` |
| 141.5 (paper) | 99.868 % (water 0.113 %) | `NO_CONVERGENCE` |

**Inherent to the paper:** acetic acid is the heaviest component; all of feed 13's acid (0.01 % of 27,314 = 2.7 kg/h)
leaves in the product, 0.022 mass %, not the 0.01 % printed for stream 16 (stream 14 prints 0.00 %). The maintainer
(spot check, 2026-11-13): "something is wrong in the table: either stream 16 is higher than 0.01 or a part is also in
14"; CHEPTA puts it all in 16. CHEPTA reaches 99.9 % ester at about 140.5 kmol/h, not the paper's 141.5.
**CHEPTA's problem:** a trace of acid (even 0.001 %) stops the column near the paper's product flow (request 9).

**Column 15 alone** (`iso-scds15-*`, the paper's feed 28, R/D 2, distillate varied):

| Distillate 21 | Ethanol in bottoms 22 | Acid in 22 | Reboiler |
|---|---|---|---|
| 380 kmol/h | 0.650 % | 0.012 % | 14,369 kW |
| 394.6 (paper) | 0.151 % | 0.012 % | 14,920 kW |
| 400 | 0.014 % | 0.012 % | 15,120 kW |
| 410 | 0.003 % | 0.012 % | 15,467 kW |
| water 99.99 % given | `OUT_OF_RANGE` (correct: the acid alone is 0.012 %) | | |

**Inherent to the paper:** the acid of feed 28 leaves in the bottoms, so "less than 0.01 % organics" (Section 3.5)
cannot hold with 0.01 % acid in the feed; the paper's own stream 22 prints 0.03 %. For ethanol CHEPTA needs a
distillate of about 400-410 kmol/h (paper 394.6) and a reboiler of 15,100-15,500 kW (paper 16,136.6).

**The plant again with the purity specifications** (column 15 on 99.99 % water in its bottoms, column 11 on R/D 3 and
its distillate so the product purity is a result):

| Run | Specifications | Outcome | Product 16 | Balance (Lab) |
|---|---|---|---|---|
| plant62-R-bottoms-col15purity | column 11 bottoms 141.5 kmol/h | `NO_CONVERGENCE` at iteration 9: the reactor runs short of ethanol (the product takes more than the 141.07 kmol/h of ester formed) | — | — |
| plant62-R-purity-col15purity-warm | column 11 on 99.90 % ester | `OUT_OF_RANGE` in column 11: "cannot be 0.999 ... it stays between 0.943249 and 1" (contradictory; request 13) | — | — |
| plant62-R-dist-col15purity (Broyden), -direct, -direct-tol1e-5; W likewise | column 11 distillate 230.4 kmol/h | Broyden: change down to 2.2e-4 then a jump, column 5 or 11 fails (iteration 10 / 20); direct: `OUT_OF_TIME` after 57 min and 117 min, no progress reported (request 14) | — | — |
| plant62-R-dist-col15d405-direct-tol1e-5 | column 15 distillate 405 kmol/h | `NO_CONVERGENCE` in column 5 at iteration 3 | — | — |
| **plant62-R-dist-col15purity-tol3e-4** | R, column 11 distillate 230.4, column 15 99.99 % water, tolerance 3e-4 | **ok**, 6 iterations | 12,496 kg/h, 99.473 % ester, 0.491 % water | in 32,461, out 32,455 kg/h |
| **plant62-W-dist-col15purity-tol5e-4** | W (25 = 20,000 kg/h), tolerance 5e-4 | **ok**, 4 iterations | 12,503 kg/h, 99.465 %, 0.497 % water | out 42 kg/h above in (0.13 %; loose tolerance) |
| **plant62-R-dist240-col15purity-tol3e-4** | as R, column 11 distillate 240 kmol/h | **ok**, 6 iterations | **12,470 kg/h, 99.673 %, 0.301 % water** | in 32,461, out 32,453 kg/h |
| plant62-R-dist240-RD3.5-col15purity-tol3e-4 | distillate 240, R/D 3.5 | ok, 10 iterations | 12,478 kg/h, 99.615 %, 0.368 % water | energy balance off by 112 kW |
| plant62-R-dist245, -248, -250, -255, -dist240-RD4 | tuning column 11 further | `NO_CONVERGENCE` in column 11 at iteration 2-3 (request 13) | — | — |
| plant62-R-dist260-col15purity-tol3e-4 | distillate 260 | `NO_CONVERGENCE`: the reactor runs short of ethanol at iteration 10 | — | — |

The closed plant at tolerance 3e-4 (plant62-R-dist240-col15purity-tol3e-4) against the paper; **not settled**: see
round 3, where the settled plant's product is 99.11 %, not 99.67 %. Every number rests on 7 listed extrapolations (acid and ester records below their range at the 15 C feeds; water + ethyl acetate UNIQUAC set above
343.55 K on hot stages); no pair estimated.

| Stream or unit | CHEPTA, closed plant | Paper (Table A2, Table 1) | Difference |
|---|---:|---:|---:|
| 6 reactor vapour | 50,489 kg/h; 89.6 C | 53,292; 90 C | −5.3 %; −0.4 K |
| 7 column 5 bottoms | 14,399 kg/h | 14,912 | −3.4 % |
| 8 azeotrope | 96,090 kg/h; ester 84.12 %; acid 0.0000 % | 98,380; 84.78; 0.01 (limit 0.005) | −2.3 %; −0.66 points; meets the limit |
| 11 raffinate | 87,986 kg/h; ester 93.22 % | 87,314; 93.43 | +0.8 %; −0.21 points |
| **16 product** | **12,470 kg/h; 99.673 % ester, 0.301 % water, 0.026 % ethanol** | 12,434; 99.90; 0.07; 0.02 (limits ≥ 99.9, < 0.03 water, < 0.04 ethanol) | +0.3 %; **−0.23 points; water ×10 the limit** |
| 21 wastewater distillate to the reactor | 21,114 kg/h; ethanol 35.1 % | 23,405; 31.06 | −9.8 %; +4.1 points |
| 25 wastewater | 19,983 kg/h; organics 0.010 % | 20,000; 0.03 (limit < 0.01) | −0.1 %; at the limit |
| KREA 4 duty (conversion from the paper) | 14,363 kW | 13,586.2 | +5.7 % |
| HTXR 2 (from 15 C) | 581 kW | 535.6 | +8.5 % (extrapolated acid data) |
| HTXR 6 | −14,577 kW | −14,855.8 | −1.9 % |
| HTXR 17 | −8871 kW | −8869.3 | 0.0 % |
| HTXR 18 / 19 | 1528 / 7274 kW | 4332.9 / 1541.1 | exchanged in the paper; 19 also heats from 27 C, not 41 C (isothermal extractor) |
| Column 11 condenser; reboiler | −9493; 7648 kW | −9180.3; 9219.2 | +3.4 %; −17 % |
| Column 15 condenser; reboiler | −11,494; 14,781 kW | −12,127.2; 16,136.6 | −5.2 %; −8.4 % |

What it shows: CHEPTA can carry the whole plant with acetic acid through all recycles; the column outlets that the
paper's limits concern are met for the azeotrope and the wastewater; the product purity is not, because the
column 11 settings that would reach it do not converge in CHEPTA.

### Capability requests to CHEPTA from round 2

| # | Request | Outcome and message | Evidence |
|---|---|---|---|
| 15 | **Global design specifications for the flowsheet** (the maintainer, 2026-11-14: "like in Aspen or HYSYS, a master tab where you set fixed targets and the variables to vary"): a flowsheet-level list of targets (any stream or block result: a product's purity or component content, a flow, a temperature, a duty) and of manipulated variables (any input anywhere: a feed's flow, a splitter's flow, a column's reflux or distillate, a heater's temperature), each with bounds, solved together with the recycle loops and reported with the achieved values and the variables' final values; and **sensitivity tables** (one or two inputs swept, chosen results tabulated; Aspen's Sensitivity, HYSYS's Case Study), each point started from the last. Here: the ethanol feed varied to hold the product's ethanol below 0.04 % or its purity at 99.9 %, and the sweeps of this case (ethanol feed, extractor temperature, W/A, column 11 distillate) run in one request instead of one run each. Refines request 7 | not available; by hand, ethanol feed 6,506 kg/h gives 99.50 % and smaller steps fail to converge; every sweep in this case needed one run per point | plant62-settled-ethanol*, plant62-settled-extr*, plant62-settled-WA*, plant62-*-dist2* |
| 13 | Column 11 (35 stages, VLL) inside the closed plant: no convergence when its distillate is raised to 245-255 kmol/h or its R/D to 4; on a bottoms purity a contradictory refusal | `NO_CONVERGENCE` at loop iteration 2-3; `OUT_OF_RANGE` "the mass fraction of Ethyl acetate in the bottoms cannot be 0.999 ... it stays between 0.943249 (at 24.25) and 1 (at 117.6)" | plant62-R-dist245/248/250/255-*, plant62-R-dist240-RD4-*, plant62-R-purity-col15purity-warm |
| 14 | A loop stopped by its time limit reports nothing of its progress (iterations, tear change) | `OUT_OF_TIME` "The calculation did not finish within limits.time_ms ..." | plant62-*-direct, plant62-*-direct-tol1e-5 |
| (8) | Column 5: converges and fails irregularly on neighbouring inputs | see the column 5 table above | iso-scds5-* |
| (note) | The recycle loop plateaus near 2e-4 relative change with Broyden; CHEPTA's default tolerance (1e-8) is not reached, so a closed answer needs a loose tolerance, and its own balance check is then loosened with it (1000 × tolerance) | — | plant62-*-tol3e-4 |

### Round 3 (the maintainer, 2026-11-14): saved starting values, more stages, a check for blown-up flows

**Saved starting values.** The converged recycle streams (7, 15, 21, 24, 27) are kept as starting values for a redo:
[init-closed-plant-chepta-0.6.2-settled.json](init-closed-plant-chepta-0.6.2-settled.json) (the settled plant; the
default of `s2_model_062.init_guesses()`) and [init-closed-plant-chepta-0.6.2.json](init-closed-plant-chepta-0.6.2.json)
(the 3e-4 answer, not settled). Each names its run and the sha256 of its output. CHEPTA's columns take no starting
profiles; their converged stage profiles are in the run outputs. From the saved start the plant converges in 1
iteration instead of 6 (run plant62-best-init), and column 11 converges at a distillate of 246 kmol/h, which failed from
a cold start.

**More stages** (from the saved start, tolerance 3e-4):

| Run | Change | Product 16 | Outcome |
|---|---|---|---|
| plant62-best-init | none (35 stages in column 11) | 99.672 %, 0.302 % water | ok, 1 iteration |
| plant62-best-init-col11-36st | column 11 with 36 stages | 99.675 % | ok |
| plant62-best-init-col11-38st | 38 stages | 99.680 % | ok |
| plant62-best-init-col11-40st | 40 stages | — | `NO_CONVERGENCE` in column 11 |
| plant62-best-init-col11-40st-dist230 | 40 stages, distillate 230.4 kmol/h | 99.486 % | ok |
| plant62-best-init-col5-9st | column 5 with 9 stages | 99.668 %; acid in 8 0.0000 % | ok |
| plant62-best-init-col15-19st | column 15 with 19 stages | 99.672 %; wastewater organics 0.010 % | ok |

More stages change the product by at most 0.01 point: the limit is column 11's water balance, not its stage count.
Its distillate leaves at the water azeotrope, 8.52 % water at every flow, so the water it can carry overhead is fixed
by the distillate flow; the rest goes down with the product. Paper: feed 13 brings 1,284 kg/h of water, the distillate
takes 1,275, the product 9 (Table A2). CHEPTA, closed plant: feed 13 brings 1,360-1,411 kg/h (its raffinate is wetter,
4.86-5.05 % water against 4.70 %), the distillate at 240 kmol/h takes 1,322 kg/h. Two liquids sit on stages 1-31 of 35
of column 11 in the closed plant (the water front near the bottom), against stage 1 only in the column alone at 139
kmol/h of product.

**Blown-up flows?** ([check_blowout_062.py](check_blowout_062.py) → [blowout-check.json](results-chepta-0.6.2/blowout-check.json):
every stream and component against Table A2, column stage flows against their feeds, two-liquid zones, the plant
balance.) Within each converged answer nothing is blown up: every stream is within 0.90-1.07 of the paper's flow,
the largest column internal flow is 2.9 times its feed, and the only flag is the ester in stream 7 (243-265 kg/h vs 547).
**But the loose-tolerance answer had not settled.** From its saved start, a tolerance of 1e-4 took 16 more iterations
(change 3.3e-5; balance within 0.2 kg/h) and 1e-5 one more (change 2.1e-6, the same numbers):

| | Tolerance 3e-4 (run plant62-R-dist240-col15purity-tol3e-4) | Settled, 1e-5 (run plant62-best-init1e-4-tol1e-5) | Paper |
|---|---:|---:|---:|
| Ethanol in the reactor feed 5 | 14,629 kg/h | 17,455 | 14,650 |
| Ethanol in stream 21 (to the reactor) | 7,415 kg/h | 9,976 | 7,270 |
| Water in feed 13 to column 11 | 1,359 kg/h | 1,411 | 1,284 |
| Ethanol leaving (product + wastewater) | 5 kg/h | 12 kg/h | 6.5 |
| Product 16 | 99.673 % ester, 0.301 % water | **99.109 %, 0.813 %** | 99.90, 0.07 |
| Plant balance | 7.5 kg/h | 0.1 kg/h | 27 kg/h short |

The feeds bring about 0.2 kmol/h more ethanol than the reaction uses (conversion fixed per pass); its only exits are the
product and the wastewater, so ethanol builds up in the reactor-column 5-extractor-column 15 loop until they carry it
out. A plant balance that closes to 0.02 % did not show it; comparing the recycle inventories between two tolerances
did.

The settled plant against the paper (run plant62-best-init1e-4-tol1e-5; 7 extrapolations listed, no pair estimated):

| Stream or unit | CHEPTA, settled closed plant | Paper (Table A2, Table 1) | Difference |
|---|---:|---:|---:|
| 6 reactor vapour | 54,637 kg/h; 88.5 C | 53,292; 90 C | +2.5 %; −1.5 K |
| 7 column 5 bottoms | 14,726 kg/h | 14,912 | −1.2 % |
| 8 azeotrope | 99,911 kg/h; ester 81.38 %, ethanol 11.58 %; acid 0.0000 % | 98,380; 84.78, 8.53; 0.01 (limit 0.005) | +1.6 %; limit met |
| 11 raffinate | 87,931 kg/h; water 5.05 % | 87,314; 4.70 | +0.7 %; +0.35 points |
| **16 product** | **12,542 kg/h; 99.109 % ester, 0.813 % water, 0.078 % ethanol** | 12,434; 99.90; 0.07; 0.02 | +0.9 %; **−0.79 points** |
| 21 wastewater distillate | 24,927 kg/h; ethanol 40.0 % | 23,405; 31.06 | +6.5 % |
| 25 wastewater | 19,919 kg/h; organics 0.010 % | 20,000; 0.03 (limit < 0.01) | −0.4 % |
| KREA 4 duty | 15,340 kW | 13,586.2 | +12.9 % |
| HTXR 6; HTXR 17 | −15,555; −8871 kW | −14,855.8; −8869.3 | +4.7 %; 0.0 % |
| Column 11 condenser; reboiler | −9514; 7256 kW | −9180.3; 9219.2 | +3.6 %; −21 % |
| Column 15 condenser; reboiler | −14,111; 17,279 kW | −12,127.2; 16,136.6 | +16 %; +7.1 % |

With column 11's distillate at 246 kmol/h (settled, run plant62-best-init1e-4-tol1e-5-dist246) the product is 99.137 %;
at 260, 270 and 280 kmol/h column 11 does not converge (iterations 3-11).

The practices used to make the plant converge, and what did not help: [CONVERGENCE_PRACTICES.md](CONVERGENCE_PRACTICES.md).

### Round 4 (the maintainer, 2026-11-14): thermodynamics, or a setup before column 11?

The question: column 11 works as an engine; is the short purity due to CHEPTA's thermodynamics against the paper's
(nothing to do), or to a setup before the column? The paper prints no UNIQUAC parameters (Section 2.1 names Calvar,
ref. 30, for vapour-liquid and Arce, ref. 31, for liquid-liquid data; CHEPTA uses Calvar's ethanol + ethyl acetate set
too, and Roque 2018 for the ternary liquid-liquid). What it does print was tested in CHEPTA (runs `thermo-*`):

| Paper's statement | CHEPTA 0.6.2 | Verdict |
|---|---|---|
| Ternary azeotrope 83.1 % ester, 8.7 % ethanol, 8.2 % water (pp.3, 6, ref. 22) | at that composition bubble and dew points 0.07-0.08 K apart (70.08 C at 101.325 kPa), two liquids at the bubble point | **agrees** (an azeotrope); CHEPTA puts it on the two-liquid boundary |
| Organic phase > 93 % ester (p.4); stream 11 93.43 % ester, 4.70 % water at 27 C | 2 stages, W/A 1: 93.25 %, 4.85 % water | close; **CHEPTA's organic phase is wetter by 0.15 points** |
| Cooling 10 C raises the ester in the organic phase by about 0.15 points; 50 → 20 C by about 0.45 (Section 3.3, Figure 4) | 50 → 20 C: 92.62 → 93.41 %, +0.79 points (0.24-0.29 per 10 C) | **CHEPTA's liquid-liquid split is about 1.7 times as temperature-sensitive** |
| More wash water raises the ester in the organic phase (Section 3.3) | W/A 1 / 1.5 / 2: 93.25 / 94.29 / 94.78 %; water 4.85 / 4.64 / 4.53 % | agrees |
| Column 11 at a fixed product rate: 99.9 % from R/D 1.5; water < 0.03 % and ethanol < 0.04 % from R/D 2.25; best feed between stages 4 and 6 (Section 3.4) | the paper's feed 13, 141.5 kmol/h: R/D 1.5 / 2.25 / 3 / 5: 99.574 / 99.825 / 99.868 / 99.882 %; ethanol falls 0.334 → 0.003 %, **water stays 0.11 %**; feed stage 4-6: +0.01 point | the trends agree; the water does not follow R/D in either model |

**The water limit cannot be met from the paper's own column 11 balance** (an inconsistency in the paper): its distillate
leaves at the water azeotrope, so the water it carries is fixed by its flow. Table A2: feed 13 brings 1,283.8 kg/h of
water, distillate 14 takes 1,275.2, product 16 keeps 8.6 kg/h, 0.07 %, against the 0.03 % limit and the text's claim
that R/D above 2.25 meets it. CHEPTA's distillate holds 8.52 % water against the paper's 8.57 %: the difference in
thermodynamics adds about 5 kg/h.

**Setups tried before and in column 11** (closed plant, settled start, tolerance 1e-5):

| Run | Change | Product 16 | Note |
|---|---|---|---|
| plant62-best-init1e-4-tol1e-5 | the settled plant | 99.109 %, 0.813 % water, 0.078 % ethanol | reference |
| plant62-settled-feed11-5 | column 11 fed on stage 5 (Section 3.4) | 98.915 %, 1.007 % water | worse: more ethanol stays in the loop |
| plant62-settled-WA1.2 | recycle 23 = 121,000 kg/h (W/A 1.13) | 99.118 %, 0.805 % water | no gain: the ethanol in the loop rises (reactor feed 21,199 kg/h of ethanol) and the raffinate is as wet |
| plant62-settled-WA1.4 | recycle 23 = 144,000 kg/h | `NO_CONVERGENCE`: the extractor's feeds become one liquid | the ethanol inventory runs away |
| plant62-settled-WA1.2-feed11-5 | both | `NO_CONVERGENCE`: column 15 cannot reach 99.99 % water | idem |
| **plant62-settled-ethanol6506** | **sensitivity: ethanol feed 6,506 kg/h** (paper 6,511; its 141.3 kmol/h spans 6,507-6,512) | **99.498 %, 0.464 % water, 0.038 % ethanol** | ethanol in the reactor feed 15,533 kg/h (paper 14,650); reactor duty 14,667 kW (+8.0 %) |
| plant62-settled-ethanol6503, -6500 | ethanol feed 6,503 / 6,500 kg/h | `NO_CONVERGENCE` in column 15 / column 11 while iterating | — |

**What sets the purity is the plant's ethanol balance, not column 11 and mostly not the thermodynamics.** The feeds
bring 141.33 kmol/h of ethanol and 141.08 kmol/h of acetic acid; the acid is used up (conversion per pass fixed), so
about 0.25 kmol/h (11.6 kg/h) of ethanol is never used and can only leave with the product and the wastewater (2 kg/h).
Ethanol therefore accumulates in the reactor-column 5-extractor-column 15 loop until about 10 kg/h leaves in the
product (0.078 %, above the 0.04 % limit); that inventory wets the raffinate (ethanol raises water's solubility in the
organic phase, p.4) and overloads column 11 with water. Five kg/h less ethanol feed (−0.08 %) lifts the product by 0.4
points. The paper's products carry 6.5 kg/h of ethanol, and its own plant balance is 27 kg/h short, so Table A2 cannot
fix this balance to the precision that decides the purity. A real plant (and probably Chemcad) would trim the ethanol
make-up to the product's quality; CHEPTA has no design specification on a feed (request 15: global design specifications and sensitivity tables, as in Aspen or HYSYS).

## On chepta 0.6.1 (2026-11-12): what was run

[s2_model.py](s2_model.py) builds every request from the transcriptions [streams.json](streams.json) (Table A2) and
[equipment.json](equipment.json) (Table 1, Figure 1); every setting is listed there and in the run manifest with its
kind (paper, derived, assumed), locator and reason. [run_s2_chepta_0.6.1.py](run_s2_chepta_0.6.1.py) sends them to
`chepta request` of the released package `chepta@0.6.1` (installed with npm outside the repository; Lab's
`package.json` pin is not changed here; lock entry [chepta-0.6.1.npm-lock.json](chepta-0.6.1.npm-lock.json)).
[compare_s2.py](compare_s2.py) compares stream by stream. Property method: UNIQUAC with CHEPTA's own fitted pair
sets, ideal-gas vapour with CHEPTA's acetic acid dimers (the paper: UNIQUAC in Chemcad 7, parameters not printed).

| Level | Runs | What it shows |
|---|---|---|
| Units | `u-*` (4 components), `u3-*` (without acetic acid) | each unit fed with the paper's own inlet streams |
| Sections | `secA-paper-inlets` (feeds, HTXR 2, MIX 3, reactor, column 5, HTXR 6, recycle 7); `secB-paper-inlets-extr1..8` (extractor, splitters, columns 11 and 15, water loop, recycles 15 and 24) | each half with its own recycles, fed at the cut with the paper's streams |
| Plant | `plant-a1-*`, `plant-a2-*`, `diag-*` | section A with the paper's 21 and 27, then B with CHEPTA's own stream 9 (once through); round 2 fails in column 5 |

### What Lab had to choose (the main ones; all in s2_model.py)

| Setting | Paper | Used | Why |
|---|---|---|---|
| Reactor KREA 4 | CSTR with a rate law (Eqs. 1-3, p.5-6), 300 m³, 85-90 C | conversion of acetic acid per pass 0.7703, outlet saturated vapour | catalyst concentration and units of the rate law missing. The reactor-evaporator is CHEPTA's conversion reactor with an all-vapour outlet (`VF: 1`, duty computed; CHEPTA's coordinator, 2026-11-12), which needs the conversion given. **Derived from Table A2 streams 5 and 6: the reactor is not predicted** |
| Feeds 1 and 2 | 15 C (Table A2) | 18 C | pure acetic acid at 15 C is below its triple point (289.81 K in CHEPTA's record): refused; 17 C still refused after mixing (runs u-htxr2-15C, secA-feeds-17C) |
| Column 5 | 8 stages, feed 8, R/V 0.61 (Table 1); "at least 14" (p.7) | absorber-type column, 8 equilibrium stages, reflux 27 on stage 1, vapour 6 on stage 8 | Figure 1 shows no condenser or reboiler; R/V follows from 60,000/98,380 = 0.610 |
| HTXR 6 outlet | 70 C | saturated liquid | at 70 C and 100 kPa CHEPTA finds 72 % vapour (run u-htxr6-70C) |
| Extractor EXTR 8 | 70 C, W/A 1 (Table 1); outlets 27 and 41 C | **2 equilibrium stages, isothermal 27 C** | stage count not in the paper: 2 matches stream 11's ethanol (1.87 vs 1.86 mass %), so that number is calibrated, not compared (runs u3-extr8-1..8stage); 70 C: the paper's feed is 78 % vapour there (refused), and with a liquid feed the outlets boil (ok, no warning) |
| MIX 7 | mixer | mixer with outlet saturated liquid (1 kW) | adiabatic mixing leaves 3.7 % vapour and the extractor refuses any vapour (run secB-mix7-adiabatic) |
| Splitters 9, 16 | 60,000 and 20,000 kg/h | fractions 0.68718 and 0.17272 | CHEPTA's splitter takes fractions only |
| Column 11 | 35 stages, feed 15, R/D 3; purity > 99.9 mass % | the same; second specification bottoms 141.5 kmol/h (plant), or 99.90 mass % (unit run); two liquids allowed | stage numbering assumed as CHEPTA's (1 condenser, 35 reboiler) |
| Column 15 | 18 stages, feed 9, R/D 2 | the same, distillate 394.6 kmol/h | second specification not printed |
| Block 14 | not named | pump without pressure rise | Figure 1 symbol; streams 18 = 19 |
| Section B | acetic acid 0.00-0.01 mass % | without acetic acid | every two-liquid stream with acetic acid is refused (runs `*-acid`); CHEPTA's own column 5 leaves 0.0004 mass % acid in stream 8 (0.007 kmol/h dropped at the cut) |

## Results against the paper (Table A2, Table 1)

The paper's numbers are a Chemcad 7 simulation, not measurements: agreement is two models agreeing.

### Units fed with the paper's inlets

| Unit | Compared | CHEPTA | Paper | Difference |
|---|---|---:|---:|---:|
| HTXR 2 | duty (from 18 C) | 543.9 kW | 535.6 kW | +1.6 % |
| KREA 4 (conversion imposed) | outlet T; duty | 89.0 C; 14,437 kW | 90 C; 13,586.2 kW | −1.0 K; +6.3 % |
| KREA 4 as an equilibrium reactor at 90 C (other unit, for reference) | acetic acid in vapour 6 | 3.21 mass % | 4.74 | the paper's outlet holds more acid than CHEPTA's chemical and phase equilibrium at 90 C |
| Column 5 | overhead 8 flow; ethyl acetate | 98,994 kg/h; 84.53 % | 98,380; 84.78 % | +0.6 %; −0.25 points |
| Column 5 | acetic acid overhead (limit 0.005 %, p.6) | 0.000 % | 0.01 % | CHEPTA meets the limit, the paper's own stream prints above it |
| Column 5 | bottoms 7 flow; T | 14,293 kg/h; 88.5 C | 14,912; 88 C | −4.2 %; +0.5 K |
| HTXR 6 | duty; outlet T | −14,734 kW; 69.8 C | −14,855.8 kW; 70 C | −0.8 %; −0.2 K |
| EXTR 8 (2 stages, 27 C) | raffinate 11 flow; water; ethyl acetate | 89,563 kg/h; 4.61 %; 93.53 % | 87,314; 4.70; 93.43 | +2.6 %; −0.09; +0.10 points |
| EXTR 8 | ethyl acetate lost to the water phase 20 | 9.30 % | 10.72 % | −1.4 points |
| HTXR 10 | duty to 71 C | 2354 kW (45 % vaporized) | 713.5 kW | ×3.3: CHEPTA's mixture boils below 71 C |
| Column 11, bottoms flow fixed | product purity; water | 99.868 %; 0.113 % | 99.90; 0.07 (limit 0.03, p.8) | misses the purity by 0.03 points |
| Column 11, purity 99.90 % fixed (610 s) | product flow; water; reboiler | 12,367 kg/h; 0.084 %; 7529 kW | 12,434; 0.07; 9219.2 | −0.5 %; +0.014 points; −18 % |
| Column 11 | condenser | −9114 to −9140 kW | −9180.3 | −0.4 to −0.7 % |
| HTXR 18 | duty | 1580 kW | 4332.9 kW | see "paper's own discrepancies" |
| HTXR 19 | duty (paper inlet at 41 C) | 5681 kW | 1541.1 kW | idem |
| Column 15 | distillate 21 flow; condenser; reboiler | 23,315 kg/h; −12,105 kW; 14,919 kW | 23,405; −12,127.2; 16,136.6 | −0.4 %; −0.2 %; −7.5 % |
| Column 15 | ethanol in the bottoms (limit 0.01 % organics, p.10) | 0.151 % | 0.02 % | ×7 |
| HTXR 17 | duty | −8869.3 kW | −8869.3 kW | 0.0 % |

### Sections and the plant once through (run plant-a2-r01-A then -B; sections alone agree to the same digits)

| Stream or unit | CHEPTA | Paper | Difference |
|---|---:|---:|---:|
| 9 azeotrope to extraction | 98,388 kg/h; 8.53 / 6.69 / 84.78 mass % ethanol/water/ester | 98,380; 8.53 / 6.68 / 84.78 | +0.01 % |
| 7 column 5 bottoms to reactor | 14,771 kg/h; ethanol 8.86 % | 14,912; 5.86 % | −0.9 %; +3.0 points |
| 6 reactor vapour | 88.6 C | 90 C | −1.4 K |
| KREA 4 duty | 14,522 kW | 13,586.2 kW | +6.9 % |
| 11 raffinate | 91,068 kg/h | 87,314 | +4.3 % |
| 27 reflux to column 5 | 62,580 kg/h | 60,000 | +4.3 % |
| **16 product** | **12,467 kg/h, 100.00 mass % ethyl acetate** (flow fixed at 141.5 kmol/h) | 12,434; 99.90 % | +0.3 %; the limits of p.8 are met |
| 21 wastewater distillate to reactor | 21,407 kg/h; water 8.17 % | 23,405; 5.19 % | −8.5 %; +3.0 points |
| 25 wastewater | 19,412 kg/h; 0.002 % ethanol | 20,000; 0.02 % | −2.9 % |
| Column 11 condenser; reboiler | −9702; 8087 kW | −9180.3; 9219.2 | +5.7 %; −12.3 % |
| Column 15 condenser; reboiler | −12,348; 15,481 kW | −12,127.2; 16,136.6 | +1.8 %; −4.1 % |
| HTXR 17 | −8612 kW | −8869.3 | −2.9 % |

**Why the loop is not closed.** In round 2 section A receives CHEPTA's own reflux 27 and wastewater distillate 21
(8.2 % water instead of 5.2 %). Column 5 then does not converge (attempts a1 and a2, `NO_CONVERGENCE`); alone with the
same inlets it reports why: "a second liquid would form on stage 7" (`PHASE_SPLIT`, run diag-scds5-round2-inlets),
and with two liquids allowed: "an absorber holds a vapour and one liquid (phases "VL"); two liquids on its stages
(phases "VLL") are not built yet" (`NOT_AVAILABLE`, run diag-scds5-round2-inlets-VLL). A closed S2 plant in CHEPTA
needs capability requests 1 and 2.

### The paper's own discrepancies (kept, not resolved)

- Table 1 (p.11) heater duties HTXR 18 and HTXR 19 are exchanged (confirmed by the maintainer's spot check, 2026-11-12): HTXR 18 heats stream 26 (60,000 kg/h, 27 to 70 C,
  sensible heat only) yet prints 4332.9 kW, and HTXR 19 heats stream 20 (139,203 kg/h of mostly water, 41 to 70 C)
  yet prints 1541.1 kW. CHEPTA gives 1580 and 5681 kW. S1 shows the same pattern (6088 / 1595 kW). Lab's inference,
  to be checked.
- Acetic acid in the azeotrope: the limit is 0.005 mass % (p.6), the paper's stream 8 prints 0.01 %.
- Wastewater bottoms: < 0.01 % organics required (p.10), stream 22 prints 0.03 %.
- Product water: < 0.03 % required (p.8), stream 16 prints 0.07 %.
- Column 5: 8 stages in Table 1, "at least 14" in Section 3.2; column 11 feed stage 15 in Table 1, "between the 6th
  and 4th" in Section 3.4.
- Pure acetic acid fed at 15 C, below its melting point.
- Column 11 (Table A2): its feed 13 holds 0.01 % acetic acid (2.7 kg/h), the heaviest component, which must leave in
  the product: 0.022 %, not the 0.01 % printed for stream 16 (stream 14 prints 0.00 %). Confirmed as a table error by the
  maintainer (2026-11-13); CHEPTA runs iso-scds11-acid0.01-bottoms139.
- Column 11 (Section 3.4 against Table A2): the text says water below 0.03 % is met for R/D above 2.25, but Table A2's
  own column balance (water in 13: 1,283.8 kg/h; in 14: 1,275.2) leaves 0.07 % in the product at R/D 3.
- Ethanol balance: the feeds bring about 11.6 kg/h more ethanol than the reaction uses; the products of Table A2 carry
  6.5 kg/h; the plant balance is 27 kg/h short. The closed plant's purity depends on this balance to a few kg/h.
- Column 15 (Section 3.5, p.10): "less than 0.01 % organics" in the bottoms cannot hold with 0.01 % acetic acid in its
  feed 28; the acid alone leaves 0.012 % (runs iso-scds15-*), and the paper's stream 22 prints 0.03 %.
- The earlier ones below (energy units of Table 2, S3 labels, kinetics) stand.

## Capability requests for CHEPTA (from the 0.6.1 runs)

Status on 0.6.2 (2026-11-13): 1, 2, 3 and 4(b) done (above), 7 done (splitter by flow); 4(a) and 5 not re-checked; 6
declined by CHEPTA (the conversion reactor with `VF: 1` is the reactor-evaporator).

| # | Request | CHEPTA 0.6.1's outcome and message | Evidence |
|---|---|---|---|
| 1 | Vapour-liquid-liquid equilibrium with acetic acid's chemical theory: flash, heater, column stages ("VLL") | `unsupported` `PHASE_SPLIT`: "the three-phase flash needs an activity model without the acid chemical theory"; column: `NOT_AVAILABLE` "two liquids on the stages (phases "VLL") need an activity model ... without the dimerizing acids' chemical theory" | runs u-htxr10-acid, u-htxr12-acid, u-htxr18-acid, u-htxr19-acid, u-scds11-acid-VL, u-scds11-acid-VLL, u-extr8-*-acid, diag-scds5-round2-inlets |
| 2 | Two liquids on the stages of an absorber/stripper configuration | `unsupported` `NOT_AVAILABLE`: "an absorber holds a vapour and one liquid (phases "VL"); two liquids on its stages (phases "VLL") are not built yet." | diag-scds5-round2-inlets-VLL |
| 3 | Liquid enthalpy of acetic acid slightly below its triple point, at least in a mixture | `invalid_input` `OUT_OF_RANGE`: "Acetic acid: its liquid heat-capacity record starts at 289.81 K, so its liquid enthalpy below it cannot be calculated." | u-htxr2-15C, secA-feeds-17C |
| 4 | Extraction block: (a) stage energy balances (adiabatic extractor); (b) accept a feed with a little vapour that condenses at the stage temperature | (b) `invalid_input` `BAD_INPUT`: "the feed is partly vapour (vapour fraction 0.03713 at 342.9 K and 100 kPa); the stages hold two liquids and no vapour." | secB-mix7-adiabatic, u3-extr8-1stage-70C-feed70C |
| 5 | Extraction block at a temperature where the outlets boil returns `ok` without a warning (raffinate vapour fraction 0.051 at 70 C) | `ok`, no warning | u3-extr8-1stage-70C |
| 6 | A reactor-evaporator (boiling reacting liquid, vapour the only outlet), or a CSTR with a vapour draw | declined: it is CHEPTA's conversion reactor with `VF: 1` (used here); a kinetic version is not available | paper Section 2, Figure 1 |
| 7 | A splitter by flow, or a flowsheet design specification (make-up water to hold W/A = 1) | not available (splitter: `fractions` only) | s2_model.py, splitters 9 and 16 |

Minor: column 11 with a mass purity specification and two liquids took 610 s (12 s with a flow specification).

## What the maintainer should spot-check (at most 3)

**Person spot check, 2026-11-13 (the maintainer, on the three items below):** item 1: "check in the paper if the 20k
is a spec, otherwise do some simulations around this number; it seems set since it is a round number" (checked: not
stated in the paper; round in all three plants while the fresh water is not; the closed plant with recycle 23 fixed
gives 19,959-19,983 kg/h by itself); item 2: "something is wrong in the table: either stream 16 is higher than 0.01 or
a part is also in 14" (CHEPTA puts all the acid in 16: 0.022 %); item 3: "numbers are ok". The maintainer's general
guidance: the plant must converge even with small deviations from the tables, and the purities at the ends of the
columns matter more than the flows. No AI full check has been done; no review is recorded in the study record.

For the 0.6.2 part (2026-11-13), chosen by the session that built it (no separate AI review yet):

1. **Largest effect:** Table A2 (pp.13-14), streams 22, 23, 25: wastewater 25 = 20,000 kg/h and recycle 23 = 95,797
   kg/h, and the plant total (feeds 1 + 2 + 17 = 32,461 kg/h against products 16 + 25 = 32,434 kg/h). If 20,000 is
   the paper's specification, the product flow follows from the balance and column 11 cannot also hold 99.9 %.
2. **Least certain:** column 11 with the purity given (run u62-scds11-acid-purity) returns a 31 kmol/h product at
   99.90 mass % holding 0.100 % acetic acid. Is the paper's stream 16 (0.01 % acid, 0.07 % water, 0.02 % ethanol;
   Table A2 p.14) consistent with all the acid of stream 13 (0.01 % of 27,314 kg/h) leaving in the product?
3. **At random:** Table 1 (p.11), column 15: 18 stages, feed stage 9, R/D 2, condenser −12,127.2 kW, reboiler
   16,136.6 kW (compared with run u62-scds15-acid-VLL).

For the 0.6.1 part (2026-11-12):

1. **Largest effect:** Table 1, p.11: are the duties of HTXR 18 (4332.9 kW) and HTXR 19 (1541.1 kW) exchanged?
   Compare with Table A2 streams 20, 26, 27, 28 (pp.13-14).
2. **Least certain:** the reactor's acetic acid conversion 0.7703 = 1 − 4.74/20.64 (Table A2 streams 5 and 6, same
   53,292 kg/h). The whole of section A rests on it.
3. **At random:** Table 1, S2 column 11: 35 stages, feed stage 15, R/D 3, condenser −9180.3 kW, reboiler 9219.2 kW.

**Person spot check, 2026-11-12:** the maintainer checked items 1, 2 and 3 above and confirmed all three (HTXR 18 and
19 duties exchanged in Table 1; conversion 0.7703 from streams 5 and 6; column 11 settings as listed). These items were
chosen by the session that built the case, not by a separate AI review session; the AI full check required by AGENTS.md
has not been done, so the case stays a draft and no review is recorded in study-record.json.

## Reproduce

0.6.2: `npm install chepta@0.6.2` in a separate folder, then
`CHEPTA_BIN=<folder>/node_modules/.bin/chepta python3 cases/ethyl-acetate-piotrowski-2021/run_s2_chepta_0.6.2.py`
(groups `S2_GROUPS`, one run `S2_ONLY`, parallel `S2_PARALLEL`), then `compare_s2_062.py` and `build_study_record.py`.

0.6.1: from the repository root, with chepta 0.6.1 installed (`npm install --no-save chepta@0.6.1`, or set `CHEPTA_BIN`):
`python3 cases/ethyl-acetate-piotrowski-2021/run_s2_chepta_0.6.1.py` (groups with `S2_GROUPS`; attempt label
`S2_PLANT_ATTEMPT`), then `compare_s2.py` and `build_study_record.py`. Re-running writes new files and changes the
study record's hashes; the committed request files are the record of what was run (s2_model.py was extended between
groups of runs; its hash in the manifest is the last one).

(This folder was `comparisons/ethyl-acetate/` until 2026-11-12.)

## Earlier specification (2026-10-29, unchanged below)

Status then: draft specification; no full-process simulation; not training eligible. Checked 2026-10-29.

## Selection

Start with Piotrowski–Kubica's S1 (subcooled azeotrope and extractant recycle) versus S2 (classic process at comparable product/wastewater quality). These are alternative flowsheet configurations of the same chemistry. Keep Sulgan's conventional plant as the cross-paper extension. This refines the provisional cross-paper pair: first isolate configuration effects within one source, then test transfer across papers.

## Source-reported values

Piotrowski and Kubica (2021), [DOI](https://doi.org/10.3390/pr9081425), [open article PDF](https://pdfs.semanticscholar.org/7c7c/5cc0ac24fa96af9914932cdac35e5483b5be.pdf), CC BY 4.0. Values below transcribed from Table 2, printed p. 12; all are reported simulations, not CHEPTA outputs.

| Indicator | S1 improved | S2 classic | S3 classic |
|---|---:|---:|---:|
| Product quality, % | 99.9 | 99.9 | 98.0 |
| Ethanol, t/t product | 0.524 | 0.524 | 0.531 |
| Acetic acid, t/t product | 0.681 | 0.681 | 0.681 |
| Process water, t/t product | 1.42 | 1.42 | 2.18 |
| Heating, printed kW/t product | 3333.9 | 3704.7 | 3704.7 |
| Cooling, printed kW/t product | 3251.1 | 3621.9 | 3621.9 |
| Wastewater, t/t product | 1.61 | 1.61 | 2.36 |

Section 3.4 identifies product purity on a mass basis. Appendix A, Tables A1/A2, stream 16 gives S1/S2 product flows of 12,436/12,434 kg/h, both 99.90 mass% ethyl acetate. Feed streams 1/2 are 6,511 kg/h ethanol and 8,472 kg/h acetic acid at 15 °C and 1 bar in both cases. Stream 9 is 30 °C in S1 and 70 °C in S2. These tabulated temperatures are operating points, not validated optimization bounds.

## Discrepancies to preserve

- Table 2 labels S3 heat duty equal to S1 but prints S3 heating/cooling identical to S2. Section 2 describes equal rectification duties and increased reactor duty for S3. Resolve the system boundary and table labels before claiming equal total energy.
- Printed energy units kW/t product lack an explicit production-rate time basis. Do not silently relabel these as kWh/t or GJ/t.
- S1 vs S2 printed heating difference is 10.01% and cooling 10.24%, computed relative to S2. These ratios are arithmetic comparisons of the reported numbers, not verified engineering savings.
- Appendix product water is 0.04 mass% in S1 and 0.07% in S2, whereas Section 3.4 discusses a water limit below 0.03%. Matching overall purity alone does not establish compliance with all impurity limits.
- Equations 1–3 and the original Atalay kinetics require concentration/catalyst definitions and dimensional review. Do not infer rate units from the printed 1/min labels alone.

## Cross-paper comparison

Sulgan, Labovsky and Labovska (2020), [DOI](https://doi.org/10.3390/pr8121618), [open PDF](https://psecommunity.org/wp-content/plugins/wpor/includes/file/2107/LAPSE-2021.0623-1v1.pdf), CC BY 4.0. Section 2.4 sets 10 kmol/h of each raw reactant, 25 °C boundary streams, atmospheric pressure, and a 10 kmol/h product target at 99.9 mol% purity. It uses NRTL-HOC and non-equilibrium columns; the 2021 paper uses UNIQUAC (Section 2.1). These differences prevent direct ranking of published totals. Both conventional processes already include extraction/decanter functions: this is not “extraction versus no extraction.”

## Proposed common basis (Lab choices, not source facts)

- Compare S1/S2 first at 1 tonne/h of saleable product with at least 99.9 mass% ethyl acetate. Retain original flows and report specific quantities separately. Component-specific impurity limits require resolution before a feasible winner can be declared.
- Pure feed ethanol and acetic acid at the same temperature/pressure; initially preserve the shared 2021 feed conditions. Match recovery accounting and include water makeup, wastewater, all recycle/regeneration, heating and cooling.
- For Sulgan transfer, convert full component compositions between mole and mass fractions; do not equate 99.9 mol% with 99.9 mass%. Resimulate at the shared basis; linear scaling is only preliminary bookkeeping, not equipment design.
- Compare thermal demand, fresh feed/water and organic losses separately. No cost winner until shared utility prices, economic year, location, operating hours and equipment costing are specified.
- Treat azeotrope cooling temperature, water circulation, reflux, reactor residence time and recycle as candidate adjustable variables. Bounds remain unset pending source/phase/catalyst checks; published optima are not universal constraints.
- Vary utility assumptions and product impurity requirements after validation. Report trade-offs or abstain when evidence is insufficient.

## Execution gate and next work

The pinned CHEPTA revision c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2 returns unsupported for solve_column. See capability-check.json. This is a check of that revision only, not a claim about current main.

Before either plant runs: audit all Table A1/A2 streams and rounding balances; resolve kinetics and energy/quality inconsistencies; verify UNIQUAC binary sets against VLE/LLE data; implement or adopt verified distillation/extraction models and recycle convergence. Sulgan additionally needs an explicit treatment of vapor association and non-equilibrium column differences. Arbitrary component splitters cannot fill these gaps.

Stream and equipment audit completed: see [56 streams, 19 blocks and balance results](STREAM_EQUIPMENT_AUDIT.md). Next resolve flagged balances and conflicting equipment specifications. A full-plant comparison remains blocked; no ranking or accepted training label is generated.

Human engineering review and final rights review: pending. Attribution is retained; transcription and proposed comparison choices are our adaptation. No paper PDF is redistributed.
