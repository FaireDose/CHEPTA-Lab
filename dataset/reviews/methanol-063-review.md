# Review: the Campos et al. 2022 methanol plant on chepta 0.6.3 (PR #37)

**AI full check (Claude, Anthropic; a review session separate from the builder's; 2026-11-27).** This is not a
person's check. Person spot check: **pending** (items below). The specific model identifier is left out of this file
under the session's rule against model identifiers in pushed files; the coordinating session has it.

Branch reviewed: `claude/lab-methanol-063` at 3b68272 (against `origin/main`). Scope:
`cases/methanol-co2-campos-2022/results-chepta-0.6.3/` (README, 52 requests, outputs, summaries, manifest,
co2-solubility-check.json), `CAPABILITY_REQUESTS.md` section "chepta 0.6.3" (M7, M8, M9), the 18 new rows of
`dataset/records/methanol-co2-campos-2022.json` (13 run rows, 1 corrected open row, 1 corrected lesson, 3 new lessons),
`dataset/index/outcomes.lock.json`, and the 0.6.3 pin (package.json, package-lock.json, data/upstream.json,
data/archive/package-lock-chepta-0.6.2.json). Nothing in the PR was changed.

Counts: **3 major, 5 minor, 3 nit.**

## How it was checked

- Every number in the 0.6.3 README tables, the 18 records rows and the 4 lessons, against the full results
  (`<id>.output.json`), read with my own scripts (not the builder's), and the 0.6.2 comparison values against
  `results-chepta-0.6.2/`.
- The paper: article and supplement downloaded again into `raw_papers/review-063-paper/` (git-ignored; sha256
  8215079335f3... and 015d60b56ef5..., the same as the study record). Supplement Table S9 (p.12), Table S10 (p.14-15),
  Table S14 (p.26); article pp.13-14 for U.
- The measured CO2 data: the three ThermoML files downloaded again into `raw_papers/review-063-thermoml/`; sha256 equal
  to the builder's (Xia 9d248558...0b0561, Bezanehtak f0637187...bc3f92, Xie 0525ee29...59ec22). Parsed with my own
  script (`python3 -I`), not with `co2_solubility_check.py`.
- Commands, all run on the branch: `python scripts/validate_catalog.py` (exit 0: "Catalogue OK: 44 sources, 8
  candidate families; 0 accepted training examples."), `python scripts/dataset_pipeline.py validate` (exit 0,
  `"valid": true`, 324 decisions), `python -m unittest discover -s tests` (127 tests, OK), `python scripts/kb.py check`
  (exit 0, `"index": "current"`, 2 disputed sets).
- `npm ci` (chepta 0.6.3, integrity sha512-sGOG6fD7...), then four requests rerun from their request files:
  mini-ph-H2-CO2-H2O-mhv1 (M7), mini-tp-cp3-300K-7000kPa-mhv1 (M8), u-flash3-mhv1, mini-ph-H2-CO2-H2O-pr. Each gave the
  same input hash, the same `value` and the same `error` (code and message) as the committed output. Reruns are in the
  review session's scratch folder, not committed.
- One extra run by the reviewer (not in the PR): a T-P flash of 99.99 % water + 0.01 % methanol at 100 kPa on PR,
  at 372.76, 373.5, 374.0, 374.2, 374.5 K: liquid up to 374.0 K, vapour from 374.2 K.

## Major

### 1. M9 and the column rows call reachable specifications unreachable

- **Where:** CAPABILITY_REQUESTS.md M9 (title, Evidence, Expected); results-chepta-0.6.3/README.md, column scan
  paragraph ("the paper's 0.96115 is just outside CHEPTA's column") and the M9 row; records row
  `column-specs-at-paper-values-063` ("The recovery 0.96115 lies above the most the liquid distillate can take ...
  about 0.9608"); lesson `lesson-column-reboiler-temperature-063` (`why`).
- **What is wrong:** the builder's own converged columns bracket five of the six time-outs:

  | Converged run | bottoms/feed | methanol recovery to 31-MEOH | bottoms methanol/water |
  |---|---:|---:|---:|
  | col-mhv1-ratioB5e-05 | 0.47336 | **0.96274** | 5.00e-5 |
  | col-mhv1-B4581 | 0.48672 | 0.96079 | 7.53e-5 |
  | col-mhv1-TB374.0 | 0.48727 | 0.95972 | 1.16e-3 |
  | col-mhv1-BF0.488 | 0.48800 | 0.95826 | 2.67e-3 |

  (derived by the reviewer from the outputs' stream flows.) So the recovery 0.96115 (between 0.96274 and 0.96079), the
  ratio 1.5e-4 and 5e-4 (between 7.5e-5 and 1.16e-3), the flow ratio 0.485 (between 0.47336 and 0.48672) and 0.48672
  (= the B4581 run itself) are all inside the reachable range. Only recovery 0.965 is above every converged point.
  The "at most about 0.9608" bound holds only at bottoms 4581; with a smaller bottoms flow the vapour share falls
  (3.72 % in ratioB5e-05) and the recovery rises.
- **Effect:** M9 tells CHEPTA the wrong failure: a specification inside the reachable range runs out of time instead of
  converging (a contradiction, which does pass the request test), not "at or just beyond its reachable value". The
  lesson's reason for the reboiler temperature ("the ... recovery specifications at the published values run out of
  time", with the recovery unreachable) rests partly on it.
- **Fix:** restate M9 as "a reachable flow ratio, recovery or component ratio, bracketed by converged columns, runs out
  of time", with the bracket table above as evidence; drop the 0.9608 bound or limit it to bottoms 4581. Correct
  `column-specs-at-paper-values-063` with a new `-c1` row (`keys.corrects`, `correction_reason`), not by editing it.

### 2. The chosen column specification misses the objective the lesson names; the paper's own bottoms flow meets it

- **Where:** README adjustment table (COLUMN, reboiler 374.0 K) and the closed-plant table; records rows
  `column-reboiler-temperature-063`, `plant-closed-pr-063`; lesson `lesson-column-reboiler-temperature-063`
  (`objective.judged_on`: "99.667 % methanol, 99.985 % water").
- **What is wrong:** judged on that objective, the bottoms flow at the paper's 4581 kmol/h is closer on both ends, in the
  closed plant and alone:

  | Run | 31-MEOH methanol % | 30-WATER water % |
  |---|---:|---:|
  | Paper (Table S10, p.14) | 99.667 | 99.985 |
  | plant-pr (reboiler 374.0 K) | 99.835 (+0.168) | 99.929 (-0.056) |
  | plant-pr-warm-B4581 (bottoms 4581) | 99.717 (+0.050) | 99.9996 (+0.015) |
  | col-mhv1-TB374.0 alone | 99.831 | 99.884 (-0.101) |
  | col-mhv1-B4581 alone | 99.827 | 99.9925 (+0.008) |

  plant-pr-warm-B4581 converged (16 iterations, balance passed). SIMULATION_PRACTICES step 8 says "Specify columns by
  outlet purity where CHEPTA converges; else by a flow tuned to reach that purity"; the bottoms flow is the paper's value
  and already reaches the purity. The temperature scan stopped at 374.0 K (99.88 %) and 374.5 K (refused, range ends at
  374.171 K); nothing between 374.0 and 374.171 K was run, which is where 99.985 % lies (the reviewer's water flash: PR
  boils 99.99 % water between 374.0 and 374.2 K at 100 kPa). The lesson's status "worked" and its `do` ("scan the
  reboiler temperature just below it") are not supported on its named objective. The README's reason for the
  shift (CHEPTA's water boils about 1.4 K above 99.6 C) is right: confirmed by the reviewer's flash (real water at
  100 kPa boils at 99.6 C, 372.76 K).
- **Fix:** either use the bottoms flow (4581, or one tuned to 99.985 %) for the reported plant, or scan 374.05-374.15 K
  and choose by the purities; state in the adjustment table why the chosen spec beats the other on the objective. Correct
  the lesson with a `-c1` row.

### 3. The "engine commit 8b8b64f with local changes" is CHEPTA-Lab's own commit

- **Where:** README first paragraph and "Not done" list; CAPABILITY_REQUESTS.md 0.6.3 header ("the result header
  reports commit 8b8b64f with local changes").
- **What is wrong:** 8b8b64f is CHEPTA-Lab's "Merge pull request #35 from FaireDose/claude/lab-next-steps"
  (`git log -1 8b8b64fb`). chepta's CLI (`node_modules/chepta/bin/chepta.mjs`, lines 90-99) runs `git rev-parse HEAD`
  and `git status` in the package's parent folder; installed under Lab's `node_modules/`, git finds Lab's repository. My
  rerun of u-flash3-mhv1 reports `commit: 3b682726...` = Lab's current HEAD, `local_changes: false`. The README also says
  "every summary in this folder, which.engine" shows it; since commit 36c855c every committed summary shows
  `commit: null, local_changes: null`.
- **Effect:** a non-existent engine-version disagreement is reported to CHEPTA and left "unresolved".
- **Fix:** say the engine is identified by the npm integrity hash; drop the commit difference from "Not done". Optionally
  report to CHEPTA (with the two lines above) that the CLI reports the host repository's commit when installed as a
  dependency.

## Minor

1. **U 300 variant "same streams within 0.6 kmol/h and 0.013 points"** (README, variants paragraph; records row
   `plant-closed-pr-063`). True for the products (31-MEOH 0.54, 30-WATER 0.51, 39-REC 0.09 kmol/h); the loop streams
   differ by about 104 kmol/h (36-REC 103.2, 33 105.3, 19-23 104.4), purge 2.1, stream 24 0.96 kmol/h; largest
   composition difference 0.026 points (plant-pr against plant-pr-warm-U300). Fix: "the products within 0.6 kmol/h;
   the recycle within 0.2 %".
2. **3.41 % labelled as 0.6.2's unit result** (records row `property-method-pr-mhv1-063`, first limit: "PR k_ij on 0.6.2:
   3.41 %"). The 0.6.2 unit run u-flash3 gives 3.366 % (co2-solubility-check.json); 3.41 % is the closed plant
   (plant-a6, plant-pr). The README table has it right (0.0337). Fix in a `-c1` row.
3. **The temperature limit of the CO2 comparison is stated but not sized.** Xia's own 354.35 K points allow an estimate:
   a van 't Hoff fit of x_CO2/P over the low-pressure points (313.75 and 354.35 K) gives for the 1:1 solvent at 303.15 K
   about 0.021 at 1226 kPa and 0.024 at 1420 kPa (reviewer, derived; assumes ln(x/P) linear in 1/T). That supports the
   builder's reading (PR + MHV1's 2.35 % at its own 1420 kPa; the paper's 18.5 % about nine times 0.021) and would make
   "somewhat more at 303.15 K" a number. The interpolation itself is fair: x/P of the 1:1 points is 0.0148-0.0152 per MPa
   from 831 to 7072 kPa, so linear in pressure is adequate, and I reproduced 0.0183 and 0.0212. Measured and simulated
   are kept apart in every table.
4. **Summaries regenerated after the runs, not recorded.** Commit 36c855c rewrote every `<id>.summary.json`
   (`which.engine` from 8b8b64f/true to null/null, absolute to relative paths). The outputs are byte-identical (manifest
   sha256: 0 mismatches over all 52 runs), but the manifest note says only that outputs were renamed. Fix: note the
   regeneration and its command.
5. **The duty table omits HE6, and stream 13's temperature.** HE6 is 1.20 MW in plant-pr against 5.0 MW in Table S14,
   and the README's explanation of HE7 relies on HE6. Stream 13 (reactor feed) is 66.95 C against the paper's 81.4 C
   (Table S9). Fix: add both rows with the differences.

## Nit

1. "the measured gas has no H2 or N2 (Xia, Xie)": the Xie 2005 file has two H2 data sets (CO2 + methanol + H2, 313.2 K),
   CO2-rich (x_CO2 0.40-0.87) at 8.8-21.8 MPa, far from the separator. Say "the data sets used".
2. The interrupted first BF0.48672 attempt had its request file removed (manifest `interrupted`). Keep it, or say it was
   identical apart from the time limit.
3. HE5 alone on the paper's streams carries 113.9 MW (paper 103.3 MW); the README reports only its approach.

## Verified as correct

- Closed plant plant-pr: 29 iterations, 315 s, balance passed; 31-MEOH 4540.8 kmol/h at 99.835 % (CO2 0.165 %);
  30-WATER 4589.6 at 99.929 %, 100.85 C; 32 38.6 kmol/h at 38.1 % CO2; 24 9523 kmol/h at 3.41 % CO2; 39-REC 394.5;
  36-REC 52,795; 44-PURGE 1077.5; 13 72,477; 16 7.498 % methanol; 2 5218.5; condenser 148.0 MW, reboiler 64.7 MW;
  HE4 114.1, HE5 93.7, HE7 28.7 MW; HE5 smallest approach 2.000 K (zones 2.28 K); CP1-3 7.90, 7.87, 7.75 MW. plant-pr-warm
  identical in 19 iterations. plant-pr-warm-B4581: 4549.4 at 99.717 %, water 99.9996 %.
- Paper values: Table S9/S10 (31-MEOH 4542, 99.667, 0.316, 0.016; 30-WATER 4581, 99.985, 99.6 C; 32 289, 36.909 %;
  24 11,488, 18.545 %; 33 17.704 % CO2, 73.238 % H2, 69.25 bar; 39-REC 2786; 36-REC 51,504; 44-PURGE 1051; 13 73,113;
  16 7.415 %, 247.9 C; 2 7610); Table S14 (HE4 105.5, HE5 103.3, HE7 24.2, condenser 143.6, reboiler 53.7 MW); article
  pp.13-14: U(z=0) 160, U(z=12.5) 150, average 155 W/m2/K used because Aspen takes one value. The 0.6.3 README's U row
  corrects the sealed README's "not printed" correctly.
- Reactor: U155 PR 247.96 C, 7.539 %, 35.8 MW; MHV1 247.95 C, 7.637 %, 37.0 MW; 0.6.2 U150 247.97 C, 7.540 %; U300
  247.74 C, 7.529 %.
- Column scan: all 16 rows (flows, purities, temperatures, times, codes, messages) as in the README; vapour share 3.91 %
  (paper 3.86 %, derived) and 0.96115 = 4542 × 0.99667 / (9412 × 0.50041).
- CO2: paper K 0.955 and p_CO2 1226 kPa; Xia 1:1 points (mole-fraction solvent 0.4999, molality per kg solvent, as the
  ThermoML variables say), 0.0183 and 0.0212, 0.108 at 7072 kPa, pure methanol 0.064; Xie 0.068; Bezanehtak six
  points, x 0.047-0.115, K 2.30-5.74; CO2 vapour pressure about 7.2 MPa at 30 C and about 67 bar at 300 K.
- M7 and M8: inputs as stated, codes and messages exactly as quoted, reproduced on 0.6.3; controls as stated (PR P-H ok;
  MHV1 T-P ok; the three binaries ok; PR one liquid at 300 K, 7000 kPa). Both pass the request test: no nearby setting
  exists for a P-H flash failure that stops every mixer, valve and exchanger, and PR + MHV1 is CHEPTA's advised method.
  Unit messages: HE4, HE5, HE6 40.0036 K at 6925 kPa; MIXER1 84.234 K; MIXER4 67.08 K; VALVE1 66.92 K.
- Manifest: 52 runs, 33 ok and 19 not (10 not_converged, 6 out_of_time, 2 unsupported, 1 invalid_input); every
  request has an entry; sha256 of every file matches.
- Correction path: `open-co2-solubility-hp-flash-c1` and `lesson-dissolved-co2-sets-co2-recycle-c1` carry
  `keys.corrects` and `correction_reason`; the original rows are unchanged against main and list `corrected_by`.
  outcomes.lock.json against main: outcomes 124 to 141, informed_by 0 to 2, corrections 21 to 23, indexed 306 to 324;
  nothing removed or changed. All four lessons have the plain shape (title, when, do, why, check, result) and an
  `objective.judged_on`; on their objectives three hold (MHV1 failed, as recorded; closed plant meets the methanol
  product; CO2 against measured data) and the column lesson does not (major 2).
- Pin: package.json and package-lock.json at 0.6.3 with integrity; the archived 0.6.2 lock is byte-identical to main's
  package-lock.json (sha256 869f7e37...), and the study records point to it. The sealed case README is unchanged (sha256
  3f3b4910..., as sealed).

## Items for the person's spot check

1. **Largest effect: major 2, the column's third specification.** Compare plant-pr and plant-pr-warm-B4581 (`31-MEOH`,
   `30-WATER` in `value.streams` of each `.output.json`) with Table S10 p.14 (99.667 % methanol, 99.985 % water), and
   decide which specification the case should report.
2. **Least sure: the measured CO2 basis.** Check in the Xia 2004 ThermoML file (doi 10.1021/je049803i, data set 1,
   313.75 K, solvent 0.4999) the eight 1:1 points from 242 to 7072 kPa, the molality-to-mole-fraction conversion, and the
   interpolation at 1226 kPa (0.0183); and the paper's stream 24 (18.545 %) and 33 (17.704 %, 69.25 bar) in Table S10.
3. **At random: HE5 in plant-pr.** `value.blocks.HE5.sizing`: duty 93,681 kW, `dT_min_K` 2.000, `dT_min_zones_K` 2.277;
   the README gives 93.7 MW, 2.000 K (zones 2.28 K).

Record when done: "person spot check (items 1-3, date)". If an item is wrong, the case goes back for a full recheck
by a new review session (AGENTS.md).
