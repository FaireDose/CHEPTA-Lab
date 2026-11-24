# Review of the plain fields on the 160 literature rules (PR #33)

**AI full check (Claude Opus 5.5, 2026-11-24).** A separate AI review session: it did not write PR #33. It is not a
person's check. The person's spot check (last section) is still to do, and only the maintainer records it.

Reviewed: `main` at `c60ea64` (PR #33 merged; the record files are identical to the PR head `1a8e4bb`). Scope: the
`keys.plain` fields (title, when, do, why, check, result, note) of the 160 `design-rule` and `simulation-rule` rows
in `dataset/records/`, all files except `pilot.json`, `ethyl-acetate-piotrowski-2021.json` and
`methanol-co2-campos-2022.json`. No row was changed by this review.

## What was checked

- **All 160 rows against their own row:** every plain field read next to the row's statement, limits, mechanism,
  operation, evidence and locator: whether it adds a number, strengthens a claim or drops a condition, whether Why is
  physically right, whether Check is a real check, and whether an engineer can act on it without the source.
  `python scripts/kb.py check` passes (index current; numbers, row ids and bare "the paper" checked by the tool).
- **Against the source text**, rereading the passage at the locator. The four maintainer PDFs in
  `raw_papers/maintainer-upload-2026-11-20/`; open-access copies downloaded for this review into
  `raw_papers/ai-review-2026-11-21/<source>/` (Europe PMC full-text XML, or the PDF OpenAlex lists; ignored by git;
  read as evidence only). In addition, a script compared every number in the plain fields with the source text: the
  only numbers not found in a source are Lab's own arithmetic, which the rows already label (5.0, 2.4, 185.7, 8.3,
  5.2, 98.9, 99.3), roundings (31.2 for 31.17, 402 for 401.5, 5.2 and 3.3 MW for 5208 and 3298 kW, 6.7 and 7.6
  million for USD 6,742,000 and 7,552,000) and one value that differs from the source (304 kPa printed as "about 300",
  below).

  | Source | Rows | Rows compared with the passage |
  |---|---|---|
  | Al-Rabiah et al. 2022 (maintainer PDF) | 19 | 19 |
  | Kruber & Skiborowski 2022 (maintainer PDF) | 18 | 15 |
  | Janković et al. 2023 (maintainer PDF) | 13 | 13 |
  | Park et al. 2022 (maintainer PDF) | 8 | 8 |
  | Blahušiak et al. 2018 | 7 | 6 |
  | Valentini & Vaccaro 2020 | 5 | 5 |
  | Hoff & Eisenacher 2025 | 5 | 4 |
  | Larsson & Skogestad 2000 | 5 | 4 |
  | Muthia et al. 2018 | 5 | 4 |
  | Othman 2024 | 5 | 4 |
  | Palomar et al. 2024 | 5 | 4 |
  | Pasha et al. 2021 | 5 | 3 |
  | Shehata et al. 2024 | 6 | 4 |
  | Steffen et al. 2024 | 6 | 3 |
  | Byrne et al. 2016, Fu et al. 2021, Mtogo et al. 2021, Orjuela et al. 2006 | 3 each | 3 each |
  | Li et al. 2017, Grisales Díaz & Olivar Tost 2017, Guo & Wang 2019 | 3 each | 2 each |
  | Ali et al. 2022, Chen et al. 2018, Andreasen 2022 | 4, 2, 2 | 2, 2, 1 |
  | Kiss et al. 2024, Henrique et al. 2020, Li et al. 2023, Kooijman & Taylor 2006 | 9, 4, 5, 1 | 0: no copy reachable from this session (the publisher download was refused here); checked against their own rows only |

  In all, 119 rows were compared with the source passage, spread over 24 of the 28 sources.
- **CHEPTA features named in Check** against the CHEPTA v0.6.2 tag (`git clone --branch v0.6.2`): `docs/models/`
  (columns, equilibrium, reactions, flowsheet, heat exchangers), `docs/schema/project-9.json` (the block keys),
  `docs/METHOD_SELECTION.md`, `docs/DECISIONS.md` and `src/units/units.js`, `src/units/columns/column.js`.
- Not checked: the cited studies behind "a cited result" rows (none was opened); figures read only from their
  numbers in the text, not from the plotted curves.

## Problems by severity

### Major: Check sends the engineer to a CHEPTA feature that does not exist

**1. A reactive column in CHEPTA (13 rows).** CHEPTA 0.6.2 has no reactive distillation: the column block has no
reaction keys (`docs/schema/project-9.json`), `src/units/columns/column.js` has none, and the programme decision says
"Reactive distillation: later" (`docs/decisions/2026-11-04-08-program-after-m4.md`). These Check lines say "In CHEPTA,
..." about reactive stages, a reactive zone or a reactive column:

- `kiss-2024-rd-conceptual-methods.raise-pressure-for-slow-reaction`, `.heat-effect-integration`,
  `.neat-versus-excess-feed`, `.locate-reactive-section`
- `othman-2024-meg-reactive-distillation.rd-keeps-oxide-dilute`, `.rd-water-fed-above-oxide`,
  `.rd-multiple-steady-states-oxide-overhead`
- `hoff-eisenacher-2025-esterification-review.resin-temperature-limit`
- `steffen-2024-rd-modelling-review.simpler-model-first`, `.multiple-steady-states`
- `al-rabiah-2022.nrtl-vlle-for-ester-system` ("on the decanter and the column": the column is the reactive one),
  `al-rabiah-2022.rd-decanter-returns-organic` and `al-rabiah-2022.rd-loss-in-water-phase` (both compare with the
  reactive column's stream 3, which CHEPTA cannot compute)
- Borderline: `kiss-2024-rd-conceptual-methods.overlapping-windows` and `muthia-2018-rd-applicability.*` do not name
  CHEPTA and can be done with a non-reactive column or by hand; no change needed.

Suggested wording, for example for `kiss-...raise-pressure-for-slow-reaction`: "CHEPTA 0.6.2 has no reactive column.
Scan the pressure of the non-reactive column in CHEPTA, read the stage temperatures where the reactive zone would sit,
and compare them with the catalyst limit and the rate you need." For the Al-Rabiah decanter rows: "CHEPTA 0.6.2 has no
reactive column; flash the overhead of Table 9 (streams 3 + organic reflux) in a flash drum and compare its water
phase with stream 3."

**2. Hoff & Eisenacher, butyl acetate yield (`hoff-eisenacher-2025-esterification-review.butyl-acetate-yield-with-water-removal`).**
The review's sentence (Section 7.1, "Technological Scale-Up of Membrane Reactors", not Section 6.1, which is on
mechanochemical esterification) says that catalytically active membranes such as Nafion tubes raised the n-butyl
acetate yield from 70% to up to 95% by simultaneous water removal [174]. The row and its plain Check say "acidic
ionic-liquid catalysts": that comes from the title of ref. 174 (Tao et al. 2011, Brønsted acidic ionic liquids), not
from the review's text. The statement, the locator and the plain Check need correcting. Suggested Check: "Hoff &
Eisenacher 2025 report this in one sentence for catalytically active membranes (Nafion tubes), citing a study Lab has
not read: treat it as an indication." This is a statement and locator error as well as a plain one.

### Moderate

**3. `phases: "VLL"` on a decanter (9 rows).** In CHEPTA 0.6.2 `phases` is a key of the column only (`"VL"` or
`"VLL"`, with `condenser: "decanter"` for a decanter on the column). A stand-alone decanter is a `flash` block, which
has no `phases` key: it finds two liquids by itself and gives the second on its optional `liquid2` outlet
(`src/units/units.js`; `docs/models/equilibrium.md`, "Every liquid returned is tested against a second liquid").
Rows: `al-rabiah-2022.nrtl-vlle-for-ester-system`, `.rd-decanter-returns-organic`,
`blahusiak-2018-separation-selection.low-boiling-solvent-coextracts-water`,
`fu-2021-isobutanol-recovery.decanter-with-two-strippers`,
`guo-wang-2019-azeotropic-distillation.prefer-heterogeneous-entrainer`,
`kruber-skiborowski-2022-heteroazeotropic-init.phase-stability-every-stage`, `.heteroazeotrope-prerequisite`,
`pasha-2021-biodiesel-process-design.staged-decanting`,
`valentini-2020-azeotropes-waste.butyl-acetate-entrainer-for-acid-water`. Suggested wording: "In CHEPTA, use a flash
drum at decanter temperature with its liquid2 outlet connected (it finds two liquids by itself), or a column with
phases: "VLL" and condenser: "decanter"; check that two liquids form." (Two liquids with acetic acid's chemical theory
are accepted in v0.6.2, decision 2026-11-12-02, although `docs/models/columns.md` line 111 still says refused.)

**4. Janković et al. 2023, MVR (`jankovic-2023-ipa-acetone-recovery.mvr-when-temperatures-close`).** Do says the
coefficient of performance must exceed "the electricity-to-heat price factor", and Check compares it with "your site's
factor". The 2.5 of Janković et al. (Methods, p. 716; p. 717) is an electrical-to-thermal energy conversion factor
("accounts for the overall energy efficiency"), a primary-energy factor, not a price ratio. Prices enter separately
(their p. 722, the heat-to-electricity cost ratio, which another row covers). Suggested Do: "It saves primary energy
when its coefficient of performance clearly exceeds the factor that converts electricity to primary heat (2.5
assumed); whether it saves money depends on your heat and electricity prices." Check: "...compare it with 2.5, then
with your price ratio."

**5. Valentini & Vaccaro 2020, purity and pervaporation (`valentini-2020-azeotropes-waste.purity-decides-pervaporation`).**
Section 2.4 says: at 98.8 wt% isobutanol pervaporation is preferred to azeotropic distillation; at 99.9 wt% the order
of those two is unclear; distillation-assisted pervaporation with heat integration is the best option *in both cases*.
The row (statement and Result) presents the hybrid as best only at 99.9 wt%, and the title says the best technology
changes with purity, which this example does not show (the best stays the same; the ranking of the others moves).
Suggested Result: "At 98.8 wt% isobutanol pervaporation ranked above azeotropic distillation, at 99.9 wt% their order
was unclear; distillation-assisted pervaporation with heat integration was best at both (a cited result, not read by
Lab)." Title: "The purity target can change the ranking of dehydration technologies".

**6. Orjuela et al. 2006, ester as bottoms (`orjuela-2006-butyl-acetate-rcm.reactive-rcm-ester-in-bottoms`).** Lost
condition: the Conclusions say pure butyl acetate is obtained as bottoms for various feed conditions *except
with an excess of butanol*, where the system tends to azeotropic conditions; Results p. 33 says an equimolar
acid-butanol feed allows pure ester. Suggested When/Do addition: "...with an equimolar feed or an acid excess; with a
butanol excess the residue curves end at an azeotrope and pure ester is not reached (Orjuela et al. 2006)."

**7. Orjuela et al. 2006, catalyst load (`orjuela-2006-butyl-acetate-rcm.catalyst-load-equilibrium-regime`).** Result
gives "about 8 g, near 0.8 wt% sulfuric-acid equivalent" (p. 33: the simple-distillation curves barely change above
8 g). The Conclusions state the equilibrium regime at about 6 wt% Lewatit K-2431, equivalent to 1.42 wt%
H2SO4, and p. 33 adds that loads above 16 g caused operating problems (liquid absorbed in the resin). The row should
give both statements and the upper limit, or say which it uses and why. The reviewer could not reconcile 8 g with
6 wt% (the charge mass was not checked); see spot check item 2.

### Minor

- `al-rabiah-2022.butanol-ester-split-at-pressure`: "about 300 kPa" in title, Do and Check (and in the statement);
  Al-Rabiah et al. (Section 5, p. 7, Fig. 9b) print 304 kPa. Say 304 kPa.
- `al-rabiah-2022.rd-loss-in-water-phase`: title "most ester is lost in the decanter's water phase, not the bottoms"
  reads oddly: the bottoms ester is the product. Say "the ester lost leaves with the decanter's water phase (1.5 kmol/h);
  the bottoms lose butanol (1.1 kmol/h), not ester".
- `blahusiak-2018-separation-selection.heat-pump-criterion`: "Above about 10 a heat pump pays" is stronger than the
  source ("should be considered beneficial", p. 313, Plesu's Carnot criterion Tcond/(Treb − Tcond)). Say "is worth
  considering" and note that the ratio is the Carnot bound from the two temperatures.
- `mtogo-2021-ed-vs-psd.psd-needs-pressure-sensitive-azeotrope`: Why implies heat-integrated pressure swing beats
  extractive distillation on energy; Mtogo et al. say only that heat integration reduces it significantly.
  `mtogo-2021-ed-vs-psd.ed-cheaper-steady-state`: Why says "used less energy"; the cited study (Ghuge et al.) found a
  lower total annual cost.
- `hoff-eisenacher-2025-esterification-review.resin-temperature-limit`: Why "Resins lose their acid groups when too
  hot" is true (desulfonation) but not in the review's passage; mark it as Lab's.
- `othman-2024-meg-reactive-distillation.tubular-reactor-no-backmixing`: Why credits plug flow with avoiding oxide
  breakthrough; Othman (p. 2) credits the high water-to-oxide ratio.
- `othman-2024-meg-reactive-distillation.rd-multiple-steady-states-oxide-overhead` and
  `larsson-skogestad-2000-plantwide.fix-a-recycle-flow` (Why "stops disturbances circulating"): mechanisms that are
  Lab's reading, not marked as such.
- `guo-wang-2019-azeotropic-distillation.partial-condenser-before-decanter`: the source says "part of the condensation
  unit was set between the top of the dehydration tower and the phase separator" (Section 2.2): "partial condenser"
  is a plausible reading of the English, and Why is Lab's; say so.
- `park-2022-inherently-safer-design.four-principles-before-devices`, `.safety-from-first-flowsheet`: "much less
  reliable" is Kletz 1985 as cited by Park et al.; name it "Kletz, cited by Park et al. 2022".
- `fu-2021-isobutanol-recovery.salting-out`, `.electrolyte-model` and
  `jankovic-2023-ipa-acetone-recovery.acid-and-brine-property-methods`: "not checked" is allowed, but the v0.6.2 docs
  answer it: electrolyte models are not available (`docs/METHOD_SELECTION.md`: "not available yet", roadmap M5).
  The acid's vapour association is available as a chemical theory of dimerization, not Hayden-O'Connell.
- `henrique-2020-dwc-simulation.pump-around-representation` ("In CHEPTA, build the pump-around version"): CHEPTA has
  no dividing-wall model; a pump-around pair needs side draws and returns, which the column has (M4), but Lab has not
  checked that it converges. Say so.
- `steffen-2024-rd-modelling-review.newton-needs-good-start`: CHEPTA reports the final residuals (`state.residuals`,
  `docs/models/columns.md`), not a residual history; say "look at the residuals and iteration count it reports".
- `palomar-2024-il-process-simulation.units-alone-then-design-spec`: in CHEPTA 0.6.2 a design specification is a
  column's (`specifications`, purity/recovery/flow/stage temperature in place of one of its two variables); name it.
- `kiss-2024-rd-conceptual-methods.tray-liquid-height`: When says "catalyst hold-up"; the statement is about liquid
  hold-up on the tray.
- `jankovic-2023-ipa-acetone-recovery.ethylene-glycol-solvent-ratio`: the note rereads p. 721, the locator says p. 720;
  add p. 721 to the locator.
- `grisales-2017-abe-extraction.finite-selectivity`: checked; the title ("simulated extraction needs fewer columns than
  reality") is supported by the source (simulations assuming infinite selectivity needed fewer distillation units).

### Checked and found right (examples)

All Al-Rabiah numbers (92,500 t/a; −29.3 kJ/mol; 69.8% at about 2.5 m and 41 m3; 92%; R2 0.9973; 42 stages, feed 21,
5208 kW; ROI 23.1% and 31.17%, payback 2.7 and 2.1 years; 95%; 29 stages; 440.3 and 185.7 kmol/h; 218,729 and 26,388
MWh/a; 34 stages, reactive 5-24, feeds on 5 and 9; 101.6 kmol/h; Table 9 losses; capital costs); Lab's 5.0 ratio
recomputed (exp(1.611) = 5.0). Janković (0.032 bar and 10 °C; 22 MW; COP 8.8; 31.1 wt%; 86 wt%; 87.17 wt% at 80.23 °C;
ratio 1.1 by mass; 16-17%; 12-41%; 1.348-2.043 kWh/kg). Kruber & Skiborowski (APV88; >15%; <0.4%; 5% and 20%; 20 mol%;
Waltermann; 0.8% purge; 163.3 against 401.5 kW; 26%, 8.4%, 21% of 1365; Luyben's unconverged start; disengagement
time). Park (22, 33, 18 tools; 94 CSB reports; UFL least reliable; ISSI). Muthia (22 and 11; 28 to 64; Da/Keq 5 and 2,
10%; 30%). Shehata, Pasha, Palomar, Li 2017, Byrne, Fu, Larsson & Skogestad, Steffen, Valentini (55%, 60 candidates,
33.1% and 20%), Ali (93.3%, 45.5%, 6%), Andreasen (1 kg/h). The physics of the Why lines was found correct except
where listed above.

## For the maintainer's spot check

Record the result as "person spot check (items, date)". If an item is wrong, the whole set goes back for a recheck by
a new AI review session.

1. **Largest effect: reactive distillation is not in CHEPTA 0.6.2** (problem 1, 13 rows). Compare the Check line of
   `kiss-2024-rd-conceptual-methods.raise-pressure-for-slow-reaction` (page `dataset/index/rules/reactive-distillation.md`)
   with CHEPTA v0.6.2: the column keys in `docs/schema/project-9.json` (no reaction) and
   `docs/decisions/2026-11-04-08-program-after-m4.md` ("Reactive distillation: later"). If the reviewer is wrong,
   problem 1 is void; if right, 13 Check lines send an engineer to a run that cannot be made.
2. **Least sure: Orjuela et al. 2006, catalyst load** (problem 7). Compare Result "about 8 g, near 0.8 wt%
   sulfuric-acid equivalent" with the paper (Spanish, `raw_papers/ai-review-2026-11-21/orjuela-2006-butyl-acetate-rcm/p0.pdf`,
   or https://doi.org/10.15446/ing.investig.v26n3.14745): p. 33, the paragraph after Figure 4 ("por encima de 8g"),
   and the Conclusions ("alrededor del 6%", "1,42 % de H2SO4"). Are they the same load in two units, or two
   different findings?
3. **Random (seed 20261124 over the 160 ids): `guo-wang-2019-azeotropic-distillation.azeotropic-water-removal-in-esterification`.**
   The reviewer found it right. Compare its Result ("2.7% higher conversion for isoamyl acetate than ordinary water
   separation") with Guo & Wang 2019, Section 2.3, p. 337 (Wei et al. [26]; https://doi.org/10.4236/aces.2019.94024).
