# The next three complete plants

Written 2026-11-13 by an AI worker session for the maintainer. Draft; no person has checked it.

**Why:** CHEPTA moves to 0.7 once Lab has simulated 4 complete flowsheets from papers, compared stream by stream
(the maintainer, 2026-11-13). The first is the ethyl acetate plant of Piotrowski & Kubica 2021. This page picks the
next three and their order.

**How they were chosen**, criteria in order: (1) open licence that allows reuse; (2) a stream table (flows,
compositions, T, P) for the whole plant, in the paper or its supplement; (3) CHEPTA 0.6.2 can plausibly run its units
and components (checked against the documentation and code of the npm package `chepta@0.6.2`, read, not run);
(4) queue row E of [HANDOVER.md](HANDOVER.md): at least one plant whose downstream mixture overlaps a row of
[data/ISSUES_AND_ROUTES.md](../data/ISSUES_AND_ROUTES.md), and at least one unrelated plant; (5) 5 to 20 units.

Papers were found with OpenAlex (open-access, CC BY filter), web search and the publishers' files. Every
candidate's licence and stream table were looked at in the PDF itself, not taken from a search summary.

## Shortlist

| # | Paper | Licence | Stream table? | Units | Components (all in CHEPTA 0.6.2?) | What CHEPTA probably cannot do | Register overlap | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | Šulgan, Labovský & Labovská 2020, *Processes* 8, 1618 (ethyl acetate, conventional set-up) | CC BY 4.0 (p.32) | **yes**: Table 1, all 32 streams, molar flow, mole fractions, T, P (p.10); columns Table 2; duties Table 9 | 19 (CSTR, 3 columns, decanter, 7 exchangers, mixers, splitters) | ethanol, acetic acid, ethyl acetate, water (yes; all pairs fitted) | NRTL-HOC (CHEPTA: NRTL with dimerizing ideal vapour); rate-based packed columns (CHEPTA: equilibrium stages); column C1 may need two liquids with acetic acid near its top (refused today) | **3 rows**: ester + alcohol + water azeotrope; acid kept out of the ester; esterification equilibrium; recycles | **chosen, 1st** |
| 2 | Lacerda de Oliveira Campos et al. 2022, *Processes* 10, 1535 (CO2 + H2 to methanol, one-step loop) | CC BY 4.0 (main article, p.1); supplement from the publisher, licence not stated separately | **yes**: supplement Tables S9-S10, all 61 streams, molar and mass flow, T, P, molar enthalpy and entropy, mole % (supplement pp.12-15); also the three-step process (S11-S12) | about 25 in the loop and column (compressors, flash drums, LHHW plug-flow reactor, exchangers, valve, column), plus a fired heater and a steam cycle (about 10 more) | H2, CO, CO2, methanol, water, N2, O2 (yes) | the paper uses NRTL (with gases) outside the reactor: CHEPTA has no NRTL for the gas pairs, so PR or PR + gE (MHV1) instead; the methanol column with dissolved CO2 may be refused by an activity model and rests on fitted k_ij with PR; the kinetic table is reprinted from an ACS paper (rights of that table to check) | none of today's rows; methanol + water, as the methanol separator case | **chosen, 2nd** (the unrelated plant, and the known fallback in a better paper) |
| 3 | Al-Rabiah et al. 2022, *Processes* 10, 1801 (n-butyl acetate, conventional process) | CC BY 4.0 (p.1) | **yes**: Table 7, all 14 streams, component flows (kmol/h), T, P, enthalpy (kW), vapour fraction (p.14); also the membrane-reactor (Table 4) and reactive-distillation (Table 9) processes | about 10 (fixed-bed reactor, 3 columns, pumps, exchangers, vessel) | 1-butanol, acetic acid, n-butyl acetate, water, 1,4-butanediol (yes) | 3 of 10 pairs only predicted (butanol + acid, acid + butanediol, ester + butanediol); butanol + water form two liquids with acetic acid present (refused today); columns T-101 and T-103 of this process not specified (stages, reflux) | **different reaction, overlapping mixture**: ester + alcohol + water; acid kept out of the ester; esterification equilibrium; and it **uses extractive distillation** with a heavy solvent, today only a lead in the register | **chosen, 3rd** |
| 4 | Medrano-García, Chagas & Guillén-Gosálbez 2025, *ACS Sust. Chem. Eng.* (CO2 to methanol) | CC BY 4.0 | **no**: the supplement (from Europe PMC) has inventories, heat-exchanger stream lists and costs, no stream table | about 20 | as #2 | - | - | not chosen: no stream table (it was the fallback in data/candidates.json) |
| 5 | Šulgan, Labovský, Variny & Labovská 2021, *Processes* 9, 1380 (ethyl acetate with heat pumps) | CC BY 4.0 | yes, Tables A1-A4, but the conventional plant's table is "adapted from" #1 | as #1 plus heat pump | as #1 | as #1 | as #1 | not a separate plant: a variant of #1 (same group); later, a heat-integration question |
| 6 | Klafke, de Souza Jr. & Secchi 2016, *Braz. J. Chem. Eng.* 33(4), 985-1002 (toluene transalkylation, a plantwide benchmark) | CC BY 4.0 | **no**: equipment and kinetics only; streams in an M.Sc. thesis | about 8 | aromatics C6-C10, H2, light alkanes (the lumped C10 aromatics not in CHEPTA) | - | none | not chosen: no stream table |
| 7 | Trirahayu et al. 2022, *Fuels* 3, 563-579 (biodiesel from rubber seed oil) | CC BY 4.0 | **no**: parameters, equipment, utilities | about 15 | oil as a triglyceride, methyl esters, methanol, glycerol, water | - | methanol + water | not chosen: no stream table |
| 8 | Giuliano, Catizzone & Freda 2021, *IJERPH* 18, 807 (DME from digestate syngas) | CC BY 4.0 | **no**: a summary of results only | gasifier, cleaning, synthesis | solids and tars besides gases | gasification with solids | none | not chosen: no stream table |

Searches that found nothing usable: ethanol dehydrogenation to ethyl acetate (the ideal overlap without acetic acid:
no open paper with a stream table found), dimethyl ether from methanol, toluene hydrodealkylation (open papers found
are CC BY-SA or without stream tables), styrene, cumene, ethylene glycol.

## The choice and the order

| Order | Plant | Why this one | Why in this place |
|---|---|---|---|
| 1 | **Šulgan 2020, ethyl acetate, conventional** | The best-specified plant found: the whole stream table closes within rounding (checked, [case audit](../cases/ethyl-acetate-sulgan-2020/STREAM_AUDIT.md)), every column has stages, feed stages, reflux and specifications, every unit has its duty. It meets three register rows a second time, by other routes (azeotropic column with the product as entrainer; decanter with water) | Its two-liquid streams carry no acetic acid, so it may be the first plant CHEPTA **closes** with all its recycles, on 0.6.2 already. Same chemistry as the first plant, so the property work is known. **Caveat:** same process family as Piotrowski: one train/test group, so it adds a paper but not a new family |
| 2 | **Campos 2022, CO2 to methanol** | Unrelated to the esters (gas phase, high pressure, equation of state, compressors, an LHHW kinetic reactor), so the test set does not become narrow. The richest stream table found (61 streams with enthalpies). Builds on the methanol separator case, whose method question (PR + gE) it answers in a real plant | Second because it is larger (about 25 units without the steam cycle; Lab may scope the fired heater and the steam cycle out, saying so) and its column may need a CHEPTA request |
| 3 | **Al-Rabiah 2022, butyl acetate, conventional** | Exactly what row E asks: a **different reaction** whose downstream mixture overlaps the ester + alcohol + water rows, and a route (extractive distillation) that would turn a register lead into a route with a paper | Last because it is the weakest: predicted pairs, two liquids with acetic acid (the same CHEPTA gap as Piotrowski), and two of its columns are not specified, so some settings would be assumed |

With the Piotrowski plant this makes 4 complete plants from 4 papers in 3 process families (ethyl acetate twice,
methanol, butyl acetate). If the maintainer wants a fourth family instead of the second ethyl acetate plant, the
order becomes Campos, Al-Rabiah, then a new search; no other open paper with a full stream table was found today.

## What to decide

Approve the three plants and their order (recommended: as above), or ask for a wider search for an unrelated plant
in place of Šulgan.
