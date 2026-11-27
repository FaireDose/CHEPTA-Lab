# Ethylene glycol by direct hydration of ethylene oxide (Shehata, Nady & Gad 2024): prepared for CHEPTA

| In one look | |
|---|---|
| Paper | Shehata, Nady, Gad, Shoaib & Bhran 2024, *Sci. Rep.* 14, 28375, doi 10.1038/s41598-024-77713-y (CC BY 4.0, p.19). The **direct hydration plant** (Fig. 5, Table 3); the paper's ethylene carbonate route and ethylene oxidation section are outside this case |
| Plant | 21 blocks on Fig. 5 plus three adjust blocks: two mixers, feed/product exchanger E-105, feed heater E-100, hydration reactor, three valves and evaporators (1600, 804.5, 400 kPa) each with a vapour cooler, vacuum dehydration column (15 trays, 15/20 kPa), vacuum MEG column (26 trays, 12.5/13 kPa), water mixer, chiller, two pumps, one recycle. 1160 kmol/h EO and 1130 kmol/h water in; 1113 kmol/h MEG (0.9977) and 20.43 kmol/h DEG + TEG out; 9870 kmol/h of water recycled |
| Transcribed | the 14 streams of Table 3 (mass t/yr, kmol/h, 8 mole fractions) and the T and P printed on Fig. 5 for 30 streams in [streams.json](streams.json); every block, connection, setting of Table 1 and p.8, and the 15 energy streams of Table 8 in [equipment.json](equipment.json); each value with its locator and as printed |
| Paper's own balances | **close within rounding except in three places**: the water recycle (11 is 3 kmol/h above WATER REC), and so the plant's water (+3.5 kmol/h); the MEG column, whose feed has no water (0.0) while its products carry 0.0023 (2.6 kmol/h). Two streams' mole fractions do not sum to 1 (MEG Column FEED 0.9978, DEG+TEG 1.0023). Everything else, reactor atoms included, closes ([STREAM_AUDIT.md](STREAM_AUDIT.md)) |
| Text against tables | 11 disagreements kept (below), among them the feed heater (4.446 MW in the text, 44,462.57 kW in Table 8), the evaporators' share of the water (75 % in the text, 29.8 % from Table 3) and the reactor selectivity (85/15 in Table 1, 98/2 from Table 3) |
| Simulated | **nothing** (no CHEPTA run in this task: the dataset table goes to the maintainer first, docs/HANDOVER.md queue item 5) |
| For the maintainer | [DATASET_TABLE.md](DATASET_TABLE.md): one page with streams, units, what is known and missing, the planned blocks and method, open questions |
| Reviewed | AI full check (Claude Opus 5.5, 2026-11-27): [dataset/reviews/eg-dataset-table-review.md](../../dataset/reviews/eg-dataset-table-review.md), 2 major, 8 minor, 7 nits, fixed or answered in its "Follow-up by the builder". **Person spot check: not yet** (the maintainer records it). Draft, written by an AI session on 2026-11-27 |

The paper's numbers are an Aspen HYSYS 11 simulation ("glycol package", conversion reactors; Table 1, p.3), not
measurements: agreement with CHEPTA, later, will be two models agreeing.

## Why this plant

Process 3' of [docs/NEXT_PLANTS.md](../../docs/NEXT_PLANTS.md), approved by the maintainer on 2026-11-13 in place of
ethanol to ethylene / diethyl ether. It brings what the two closed plants lack: heavy side products from consecutive
reactions, a multiple-effect evaporator train, vacuum columns with a heat-sensitive product, and a large liquid
recycle. Its mixture overlaps no register row yet; four new rows are added (below).

## Flowsheet (Fig. 5, p.10; Table 1, p.3; text pp.6 and 8)

| Block | Type as drawn | In | Out | Settings printed |
|---|---|---|---|---|
| MIX-102, MIX-100 | mixers | WATER MKUP + 11; Water FEED + Ethylene Oxid | Water FEED; 2 | none |
| E-105 | feed/product exchanger | 2 (cold), 21 (hot) | 22, MEG To Storage | outlets 41.12 C and 34.65 C (Fig. 5); no duty |
| E-100 | feed heater | 22 | 3 (*200 C, *3480 kPa) | 44,462.57 kW (Table 8); "4.446 MW" (p.8) |
| Hydration Reactor | conversion reactor, vapour (10) and liquid (4) outlets | 3 | 10 (0 kmol/h), 4 | 85/15 MEG/(DEG+TEG) selectivity (Table 1); plug flow 77.8 m x 0.55 m, 199 C, 3480 kPa, 3 min, "endothermic" (p.8); Q-100 -32,917.29 kW (Table 8) |
| VLV-100, EVA_1, E-102 | valve, evaporator, vapour cooler | 4 | 5 (liquid), 17 (cooled vapour 7) | 1600 kPa; Q1 8,879.99 kW; "First Effect" 8,348.11 kW |
| VLV-101, EVA_2, E-104 | same | 5 | 6, 20 | 804.5 kPa; Q2 3,839.25 kW; "Second Effect" 12,793.01 kW |
| VLV-102, EVA_3, E-103 | same | 6 | 1, 19 | 400 kPa; Q3 5,037.75 kW; "Third Effect" 11,709.60 kW |
| ADJ-1, ADJ-2, ADJ-3 | HYSYS adjust blocks | - | - | targets not printed |
| Dehydration Tower | column, condenser + reboiler | 1 | Water Rec 5 (50.74 C, 15 kPa), MEG Column FEED (149 C, 20 kPa) | 15 sieve trays, 15/20 kPa (Table 1); "85 mm Hg" (p.8); 107,392.75 / 94,108.24 kW |
| Purification Tower | column, condenser + reboiler | MEG Column FEED | MEG (136.7 C, 12.5 kPa), DEG+TEG (190 C, 13 kPa) | 26 sieve trays, 12.5/13 kPa (Table 1); MEG "as a side stream" (p.8); 21,513.56 / 20,870.47 kW |
| P-101 | pump | MEG | 21 (*1900 kPa) | 47.13 kW |
| MIX-101, E-101, P-100, RCY-1 | water mixer, chiller, pump, recycle | 10, 17, 20, 19, Water Rec 5 | WATER REC, 12 (0.7706 C, 10 kPa), 13 (*3500 kPa), 11 | Q-104 16,645.27 kW; Q-105 231.27 kW |

`*` is kept as printed on Fig. 5 (Lab reads it as HYSYS's mark of a specified value). Connections are Lab's reading of
the drawing; equipment.json holds every setting with its locator.

## What the audit found ([STREAM_AUDIT.md](STREAM_AUDIT.md), [balance-results.json](balance-results.json))

Run `python cases/ethylene-glycol-shehata-2024/audit_balances.py` from the repository root (no third-party packages).
Tolerances are the sums of the rounding bounds of the printed digits (stream 4 is printed "1.10e+004", ±50 kmol/h).

- **Reactor** (with the mixers and feed exchangers, whose streams are not in Table 3): total -0.005 kmol/h, C -0.51,
  H -0.52, O -0.005 kmol/h; extents 1131.39 (Eq. 5), 19.8 (Eq. 6), 8.8 (Eq. 7) kmol/h; EO conversion per pass 87.2 %
  (all derived).
- **Evaporators and dehydration column:** the tops are not printed; by difference 810, 1203, 1052 and 6802 kmol/h
  (from the printed totals; 810.0, 1203.9, 1051.9, 6803.7 from the component flows), none negative beyond rounding.
  A weak check: stream 4's ±50 kmol/h is about ±6 % of EVA_1's vapour. Their sum against WATER REC closes for every component (largest MEG -1.03 kmol/h,
  tolerance 6.7).
- **Water recycle** (WATER REC to 11): **+3.0 kmol/h of water, tolerance 1.0: does not close** (HYSYS's recycle
  tolerance).
- **MEG column:** total +0.43 kmol/h (within 1.0), DEG and TEG close; **water +2.61 kmol/h, tolerance 0.11: does not
  close** (feed 0.0, products 0.0023). The feed's fractions sum to 0.9978 and the heavy product's to 1.0023: the
  missing 0.0022 in the feed and the extra 0.0023 in DEG+TEG look like the same water, misplaced (Lab's reading, not a
  correction).
- **Plant:** atoms close (C -0.38, H +6.2, O +3.3 kmol/h within 4.9, 13.0, 4.6); **water +3.48 kmol/h against 0.72:
  does not close**, the recycle's 3 kmol/h carried through. Mass 626,000 in, 626,470 t/yr out (+0.075 %).
- **Hours per year:** every stream's printed mass and moles give 8755-8768 h/yr: Table 3 uses 8760 h/yr (derived).

### The paper's text against its tables (kept, not fixed)

| # | Item | Table or figure | Text |
|---|---|---|---|
| 1 | Feed heater duty | 44,462.57 kW (Table 8) | 4.446 MW (p.8) |
| 2 | Water removed by the evaporators | 29.8 % of stream 4's water (derived from Table 3) | about 75 % (p.8) |
| 3 | Reactor selectivity | 98.2 % of the glycols formed are MEG, 96.5 wt % (derived from Table 3); p.13's "96 wt% yield of MEG" agrees | 85 / 15 (Table 1) |
| 4 | Reactor model | conversion reactor (Table 1), vessel icon on Fig. 5 | plug flow reactor 77.8 m x 0.55 m (p.8) |
| 5 | Dehydration column pressure | 15 / 20 kPa (Table 1, Fig. 5) | 85 mm Hg = 11.33 kPa (p.8, converted) |
| 6 | MEG draw | MEG at the condenser pressure 12.5 kPa, no other top product on Fig. 5 | side stream (p.8) |
| 7 | Heavy product temperature | DEG+TEG 190 C (Fig. 5) | MEG column below 170 C (p.8) |
| 8 | Water to EO (approximate, a soft disagreement) | 8.13 (all water / all EO at the reactor inlet), 8.35 (recycle water / fresh EO), 9.32 (all water / fresh EO, close to a nominal 10:1), derived | 10:1 (pp.6, 8) |
| 9 | Heat of reaction | Q-100 -32,917.29 kW; the paper's own total (the signed sum of Table 8 is 322,961.68 kW, the text's 323 MW, p.14) treats it as heat removed | "endothermic" (p.8); the knowledge-base record shehata-2024-meg-routes already notes this sentence disagrees with the usual chemistry |
| 10 | Heating of the water section | Q1 + Q2 + Q3 + DEH REQ Q = 111.87 MW (derived); 219.258 MW only with the condenser DEH CON Q added | "219.258 MW for heating purposes" (p.14) |
| 11 | Direct minus indirect energy | 323 - 54.7 = 268.3 MW from the text's own totals (p.14, derived) | "279 megawatts" (abstract, p.1) |

Also: feed heated to 200 C on Fig. 5, to 270 C in the block diagram text (p.6); Eq. 7 prints DEG as C4H10O4 and TEG as
C6H14O5 (p.6; the audit's C6H14O4 is Lab's); p.8 names E-105 and E-100 together before the 4.446 MW;
the text says the vapour of each effect heats the next (p.8), but the model has separate heat inputs (Q2 3,839 kW
against the first effect's condenser 8,348 kW); the text names chilled water for E-105 (p.8), Fig. 5 draws process
streams on both sides. Table 8 matches the text where the text names it: the signed total (323 MW), the evaporators
(17.76 MW), the MEG column (20.87 / 21.51 MW).

## Components and property method (no run yet)

| Paper | CHEPTA | Note |
|---|---|---|
| H2O, EO, MEG, DEG | water, ethylene-oxide, ethylene-glycol, diethylene-glycol | in CHEPTA 0.6.2 (data/vocabulary.json) |
| TEG | **none** | needs user data: molar mass, critical constants and acentric factor, a vapour-pressure correlation valid at 13-20 kPa, ideal-gas heat capacity, liquid density, enthalpy of vaporization and of formation, and NRTL pairs with water, MEG and DEG (or UNIFAC groups). Open sources to check: NIST Chemistry WebBook (CAS 112-27-6), ChemSep v8.3's pure-component databank (CHEPTA already uses it, Artistic License 2.0 as CHEPTA records), open VLE measurements. **No value entered.** Fallback: lump into DEG, declared |
| O2, ethylene, CO2 | left out | 0.0 in every stream of Table 3 |

**Method: NRTL** in every block (activity model, ideal-gas vapour), **Wilson as a variant**. The paper used HYSYS's
glycol package, whose model is not printed. Reason, from chepta 0.6.2's own data files (`components.json`,
`binaries.json` in the npm package of the pin, read without running CHEPTA):

- Water, EO, MEG and DEG are polar, associating liquids with no light gas: an activity model, as CHEPTA's method guide
  (v0.6.2) recommends.
- The plant spans 10-3534 kPa. The feed train, reactor and pumps (3450-3534 kPa) hold liquid only, but **EVA_1 makes
  vapour at 1600 kPa and 202.8 C** with an ideal-gas vapour.
- **EVA_1, the reactor (199 C) and streams 3 and 15 (200, 199.2 C) are above EO's critical temperature** (468.92 K =
  195.77 C in chepta 0.6.2); the method guide's rule 1 says an activity model needs every liquid component below it.
- Pairs in chepta 0.6.2: water + MEG NRTL fitted (Kamihama 2012, 101.3 kPa); DEG + MEG NRTL fitted (Yang 2014, 40 kPa);
  DEG + water NRTL from the ChemSep databank; **EO + water only Wilson** (ChemSep databank); **EO + MEG and EO + DEG
  none**. Under NRTL every EO pair is estimated from Modified UNIFAC 2.0; under Wilson, EO + water is from the databank
  and the EO + glycol pairs are still estimated.
- NRTL stays the main method because it carries the fitted glycol pairs; Wilson is a variant (one liquid; no split is
  expected, Lab's expectation). CPA is not in CHEPTA 0.6.2.
- Fitted pairs are reused, not revalidated (AGENTS.md); data are looked at only for the estimated EO pairs (and TEG) and
  for water + MEG, which is fitted at 101.3 kPa and used at 15-20 kPa (its temperature range to confirm).

**Fresh EO:** given as P = 3534 kPa with liquid fraction 1 (bubble point), T = 149.6 C kept as a comparison only. On
Fig. 5 only the pressure carries the asterisk, and chepta 0.6.2's EO vapour pressure at 149.6 C is 3537.8 kPa (derived),
0.11 % from 3534 kPa: the stream is saturated, so T and P would not fix its phase.

## Run plan for the next task (docs/SIMULATION_PRACTICES.md)

The full plan, fixed inputs, adjustable settings and the comparison criteria declared before the runs are in
[record.json](record.json). In short:

1. Before any unit is compared: see what the pinned CHEPTA does with EO above its critical temperature in the
   reactor, streams 3 and 15 and EVA_1, under NRTL and Wilson, and list each pair's tier (no run in this PR).
2. Each unit alone on the paper's inlets, checking the phase of every specified stream (fresh EO at its bubble
   point): reactor as a conversion reactor with Table 3's extents (no kinetics);
   feed heater on 22 to 3 to see which duty it supports; evaporators as valve + flash, scanning the duty to match
   streams 5, 6, 1; both vacuum columns specified by their outlets (MEG as distillate, as drawn); E-105 by its hot
   outlet.
3. Sections, then the plant: MIX-101's outlet pressure set explicitly and WATER REC's phase checked (probably partly
   vapour: Raoult bubble pressure 17.4 kPa at 48.17 C against 15 kPa printed, derived; E-101 then condenses EO-bearing
   vapour at 10 kPa); tears at 11 and 22, fresh EO fixed, one flow in the water loop fixed and the make-up
   free; Broyden first; per-component tear check; tighten from the saved answer.
4. Compare with the declared criteria; fill the adjustment table below; a capability request only when no setting
   near the paper's works.

### Adjustment table

| Unit | Setting | Paper | Ours | Change | Why | Runs |
|---|---|---|---|---|---|---|
| (none yet) | | | | | | |

## Knowledge base

Each planned decision is a row in [dataset/records/ethylene-glycol-shehata-2024.json](../../dataset/records/ethylene-glycol-shehata-2024.json)
with the rules that informed it (`informed_by`, judged at planning: whether they help in CHEPTA is for the run rows):

| Decision | Rules that informed it | Helped (planning) |
|---|---|---|
| NRTL, EO pairs estimated, Wilson variant | pasha-2021 nrtl-uniquac-polar; li-2017 check-built-in-parameters; palomar-2024 validate-predictive-methods; othman-2024 cpa-for-glycol-water | yes, **no** (not triggered; fitted pairs are reused), yes, **no** (CPA not in CHEPTA) |
| TEG as user data or lumped | **none applied** (no row on a component missing from the engine) | - |
| Reactor with extents from Table 3 | ethyl acetate lesson-reactor-conversion-imposed; shehata-2024-meg-routes direct-hydration-water-excess; othman-2024 tubular-reactor-no-backmixing | yes, partly, partly |
| Evaporators as valve + flash | shehata-2024-meg-routes evaporator-train-before-vacuum-column; andreasen-2022 flash-instability-not-solver | partly (its 75 % is not in Table 3), yes |
| Dehydration column by outlets | shehata-2024-meg-routes vacuum-glycol-columns; chen-2018 lower-pressure-of-sensitive-columns; jankovic-2023 vacuum-condenser-needs-chilled-water; ethyl acetate lesson-close-plant-purity-specs; kooijman-taylor column-misses-target | yes, **no** (different trigger; the published pressure is kept), **no** (condenser at 51 C), yes, yes |
| MEG column, MEG as distillate | shehata-2024-meg-routes vacuum-glycol-columns; chen-2018 lower-pressure | partly (its side draw conflicts with Fig. 5; its 170 C is not met by the paper itself), **no** (different trigger) |
| Water loop: tears, one flow fixed, make-up free | larsson-skogestad fix-a-recycle-flow; palomar tear-and-make-up; andreasen recycle-tolerance-per-component; ethyl acetate lesson-product-flow-within-feed and lesson-tighten-tolerance; methanol lesson-tears-break-every-cycle | yes (all) |
| Feed heater duty check | methanol lesson-duty-against-stream-enthalpies | yes |
| E-105 by hot outlet | methanol lesson-feed-effluent-exchanger-approach | partly (liquid both sides) |

Two knowledge-base rows from this paper (shehata-2024-meg-routes) disagree with its own tables: the evaporators'
"about 75 %" (29.8 % from Table 3) and "product glycol drawn from the side" (Fig. 5 shows a distillate); the second
also gives a 170 C limit the paper's own column exceeds (190 C). They are reported, not edited. Register rows added to [data/ISSUES_AND_ROUTES.md](../../data/ISSUES_AND_ROUTES.md):
rxn-ethylene-oxide-hydration-heavy-glycols, sep-water-from-dilute-glycol, sep-glycol-homologues-heat-sensitive,
plant-large-water-recycle. They are proposed, awaiting the maintainer's approval.

## Files

| File | What |
|---|---|
| [streams.json](streams.json) | Table 3 (14 streams) and Fig. 5's T and P (30 streams), as printed |
| [equipment.json](equipment.json) | Fig. 5 blocks and connections, Table 1, p.6, p.8 and p.13 settings, Table 8 |
| [audit_balances.py](audit_balances.py) | the audit; writes [balance-results.json](balance-results.json) and [STREAM_AUDIT.md](STREAM_AUDIT.md) |
| [record.json](record.json) | the pre-run case record: boundary, components, method, fixed and adjustable inputs, comparisons declared before runs, run plan. A study record (proposal 0002) needs a run; the first run task writes it |
| [DATASET_TABLE.md](DATASET_TABLE.md) | the one-page dataset table for the maintainer |

PDF not in the repository: sha256 `8bf58295c2e1cb0da811e6c1040917f921dbb1260c6b506dd2f772f8eb86e551`
(www.nature.com, fetched 2026-11-27). Fig. 5 labels were read from the embedded image of page 10 (pdfimages, sha256 in
the knowledge-base block `ethylene-glycol-shehata-2024.blk-fig5`).
