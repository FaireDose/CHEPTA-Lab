# How the S2 plant was made to converge in CHEPTA 0.6.2 (practices used, with the runs that show them)

Draft, written by an AI session (2026-11-14) from the runs in [results-chepta-0.6.2/](results-chepta-0.6.2/); not
reviewed by a person. Each practice names the runs that show it working or failing. The maintainer's advice of
2026-11-13 (marked **M**) shaped round 2: the plant must converge even with small deviations from the tables; the
purities at the column ends matter more than the flows; where the plant blocks, isolate the block in CHEPTA and vary
its specifications.

## Before the plant

1. **Each block alone first, with the paper's inlets** (runs `u62-*`, `rerun-*`). A block that does not solve alone
   will not solve in the loop.
2. **Balance the paper around the block** (arithmetic on Table A2) before blaming the simulator (**M**). Column 5:
   27 + 6 = 8 + 7 within 3 kg/h per component, so its settings are consistent. Column 11: the acid of feed 13 cannot
   leave as printed (0.022 % in the product, not 0.01 %). Column 15: the feed's acid alone breaks the 0.01 % organics
   limit.
3. **Vary the block's inlet and outlet specifications in CHEPTA** (**M**; runs `iso-*`) to find where it converges and
   where it meets the paper's limit. Column 5 meets the acid limit from about 55,000 kg/h of reflux; column 15 needs
   400-410 kmol/h of distillate for ethanol below 0.01 %; column 11 converges with the acid only below 140 kmol/h of
   product.
4. **Allow two liquids (`phases: "VLL"`) wherever they can form**; with one liquid CHEPTA refuses (`PHASE_SPLIT`), and
   column 11 in the closed plant holds two liquids on 31 of its 35 stages.
5. **A mixer feeding the extractor brought to saturated liquid** (a heater with `VF: 0`): the adiabatic mixer reached
   17 % vapour inside the loop and the extractor refuses more than 10 % (run plant62-R-bottoms-mix7adiabatic-open).

## Specifying the whole plant

6. **Count the plant's degrees of freedom, not only each block's.** With both feeds and the fresh water fixed, fixing
   the wastewater (25 = 20,000 kg/h) and the product (141.5 kmol/h) as well over-specifies the plant (the paper's own
   balance is 27 kg/h short). Fix one round flow inside the recycle (23 = 95,797 kg/h) and let the outlet follow: the
   wastewater then comes out at 19,959-19,983 kg/h by itself.
7. **Never fix a product flow above what the reaction makes.** With the product at 141.5 kmol/h (more than the 141.07
   kmol/h of ester formed), or the column 11 distillate at 260 kmol/h, the loop slowly runs out of ethanol and the
   reactor refuses (runs plant62-R-bottoms-col15purity, plant62-R-dist260-*).
8. **Specify the separation columns by their outlet purities where CHEPTA converges, else by a flow tuned to reach
   them** (**M**). Column 15 on 99.99 % water in its bottoms converged in the loop; column 11 on its 99.90 % purity
   refused (`OUT_OF_RANGE`), so its distillate flow was tuned instead (230.4 → 240 kmol/h).
9. **Check the key component's balance around the column whose purity is short.** Column 11's distillate leaves at the
   water azeotrope (8.52 % water), so the water it can carry is fixed by its flow; CHEPTA's wetter raffinate brings
   1,360 kg/h of water (paper 1,284), so the distillate must be about 246-247 kmol/h for the 0.03 % water limit. More
   stages do not change this (36 and 38 stages: 99.675 and 99.680 %).

## The recycle loop

10. **Mark every recycle as a tear stream with a guess from the paper** (here 7, 15, 21, 24, 27, Table A2). Guesses
    from CHEPTA's own once-through run (0.6.1) did not help more than the paper's.
11. **Broyden (CHEPTA's default) first.** It reaches about 2e-4 change per iteration in 6 iterations, then may jump
    and break a column. Direct substitution did not fail but did not finish in 57 or 117 minutes (`OUT_OF_TIME`, no
    progress reported); Wegstein was no better.
12. **Set the tolerance to what the loop can reach, then check the balance yourself.** The loop plateaus near 2e-4;
    CHEPTA's default 1e-8 is never reached. At 3e-4 CHEPTA accepts it, and loosens its own balance check with it
    (1000 × tolerance), so the plant balance is checked from the result: feeds 1 + 2 + 17 against products 16 + 25,
    within 6-8 kg/h of 32,461 kg/h (0.02 %).
    **But a loose tolerance can hide a slow build-up: tighten it from the saved start.** Started from the 3e-4 answer,
    the loop converged further at 1e-4 (16 iterations, change 3.3e-5, balance within 0.2 kg/h), and the ethanol
    circulating through the reactor and column 15 had grown by about 19 % (reactor feed 5: 14,629 → 17,455 kg/h of
    ethanol; stream 21: 7,415 → 9,976 kg/h). The feeds bring about 0.2 kmol/h more ethanol than the reaction uses; its
    only exits are the product and the wastewater, which at 3e-4 carried 5 kg/h and at 1e-4 carried 12 kg/h. The product
    fell from 99.67 to 99.11 % (water 0.30 → 0.81 %, the extra ethanol making the raffinate wetter). A plant balance
    that closes to 0.02 % does not show this: compare each component's inventory in the recycles between two
    tolerances (run plant62-best-init-tol1e-4).
13. **Save the converged recycle streams as starting values** ([init-closed-plant-chepta-0.6.2-settled.json](init-closed-plant-chepta-0.6.2-settled.json),
    the default of `s2_model_062.init_guesses()`): the same plant then converges in 1 iteration instead of 6 (run
    plant62-best-init), and column 11 converges at a distillate (246 kmol/h) that failed from a cold start. A start
    close to the answer is worth more than a different convergence method.
14. **After it converges, look for blown-up flows** ([check_blowout_062.py](check_blowout_062.py),
    [blowout-check.json](results-chepta-0.6.2/blowout-check.json)): every stream against the paper, the column stage
    flows against their feeds, the two-liquid zones, the plant balance. Here every stream is within 0.90-1.05 of the
    paper's, column internal flows at most 2.9 times their feed; the one flag is the ester in stream 7 (243 kg/h vs
    547). Also compare the recycle inventories between two tolerances (practice 12): within one answer nothing looked
    blown up, yet the ethanol inventory was still rising.
15. **Mind an excess reactant with no exit of its own.** With the conversion fixed per pass, any ethanol the reaction
    does not use circulates until the product and wastewater carry it out; that inventory sets the reactor feed and
    the product's purity.

## What did not help

- More stages: column 5 with 14 (fails on the first pass), column 11 with 40 (fails); column 11 with 36 or 38 changes
  the product by 0.01 point.
- A column's `max_iterations` (column 5 still reports 12 Newton iterations).
- Column 5 with one liquid (fails earlier).
- A higher reflux in column 11 (R/D 3.5: worse product, 99.62 %; R/D 4: fails).
- Opening the outer recycles (27 and 21 fed from Table A2) to find guesses: the half-plant is then over-specified and
  its water loop drifts (runs `*-open`).
