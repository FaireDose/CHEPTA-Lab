# Rule A handover for CHEPTA: n-butyl acetate plant (Al-Rabiah et al. 2022)

Written 2026-11-27 by a CHEPTA-Lab worker session (Claude), before any plant run; not reviewed by a person.
Rule A: docs/SIMULATION_PRACTICES.md. Pinned engine: chepta 0.6.3 (Lab's package.json). Plant range: 298.2-512.2 K,
111-324 kPa (Table 7 of the paper). No CHEPTA code was changed or run beyond `component_info`.

**Verdict: no component is missing; nothing blocks the plant.** Three pairs are missing and will be estimated, which
rule A allows. One databank pair and three liquid heat-capacity records need watching. This file is therefore a
**watch list and a data lead list**, not a request to add components. It goes to CHEPTA only if the maintainer wants
the three pairs fitted before the runs.

## Components (chepta 0.6.3, `component_info`, results in results-chepta-0.6.3/component-info/)

| Paper | CHEPTA id | Present | Records over the plant's range |
|---|---|---|---|
| n-Butanol | `1-butanol` | yes | vapour pressure fitted 278.15-563.05 K; liquid heat capacity to 390.81 K, used to 462.6 K (extrapolated, warned) |
| Acetic acid | `acetic-acid` | yes, vapour dimer by chemical theory | vapour pressure 290-523.15 K; liquid heat capacity to 400 K, used to 462.6 K (warned) |
| Butyl acetate | `n-butyl-acetate` | yes | all records cover 444.9 K, the hottest stream holding it |
| Water | `water` | yes | all records cover the range |
| 1,4-Butanediol (the solvent) | `bdo` | yes | liquid heat capacity 283.15-353.15 K only (measured data), used to 512.2 K: the plant's largest extrapolation. Above the record CHEPTA uses the ideal-gas path minus the heat of vaporization (src/thermo/system.js), with a warning |

Each component has formation enthalpy (ideal gas, ChemSep), heat of vaporization, ideal-gas heat capacity, liquid
density and UNIQUAC r, q, and Modified UNIFAC 2.0 groups.

## Pairs under NRTL (the planned method), chepta 0.6.3 binaries.json

| Pair | Tier | Note |
|---|---|---|
| acetic acid + water | fitted (Chang et al. 2005, 101.33 kPa) | default set |
| acetic acid + butyl acetate | fitted (Lladosa et al. 2008, 101.3 kPa) | |
| butanol + butyl acetate | fitted (Lladosa et al. 2008, 101.3 kPa) | |
| butanol + 1,4-butanediol | fitted (Yang et al. 2016, 70.0 kPa, bubble temperatures) | |
| butanol + water | databank by default; set `fitted-lladosa2008` fitted to the two-liquid point and azeotrope | Lab plans the fitted set; CHEPTA's known-issues: AAD 1.64 K, use with care |
| butyl acetate + water | databank (ChemSep) | CHEPTA's known-issues: split not fitted to the measured articles |
| 1,4-butanediol + water | databank (ChemSep) | **CHEPTA's known-issues: the NRTL set predicts two liquids at 273.15-323.15 K where the pair is measured as one liquid; "choose another set or another model".** The UNIQUAC set carries no such note |
| acetic acid + butanol | **missing**: estimated by Modified UNIFAC 2.0 | the two react; measurements need care |
| acetic acid + 1,4-butanediol | **missing**: estimated | the two can esterify too (Lab's note, not checked) |
| butyl acetate + 1,4-butanediol | **missing**: estimated | |

UNIQUAC has the same coverage (4 fitted, 3 databank, 3 missing). Wilson cannot show two liquids.

## Where open data for the three estimated pairs could come from (leads, none read in full)

| Pair | Lead | Access and licence | Status |
|---|---|---|---|
| acetic acid + n-butanol | Muñoz & Krähenbühl, *J. Chem. Eng. Data* 46 (2001) 120-124, doi 10.1021/je000033u: isobaric VLE at 26.65 and 53.33 kPa, Wilson/UNIQUAC/NRTL fitted, Hayden-O'Connell vapour (from a search-result summary, not opened) | ACS, paywalled; whether its data are in the NIST TRC ThermoML Archive (open to read) is to check | lead |
| acetic acid + 1,4-butanediol | none found in one web search (2026-11-27) | - | none |
| butyl acetate + 1,4-butanediol | none found; a 2,3-butanediol + butyl acetate study at 101.3 kPa exists (another isomer, not a substitute) | - | none |

No value was taken from any of these. If CHEPTA wants them fitted, the ThermoML Archive is the first place to look,
as for the other pairs of this list.

## What to check in the first run task (step 0 of the run plan)

1. Each pair's tier as CHEPTA reports it in a result, with the three estimated pairs named.
2. Whether the NRTL 1,4-butanediol + water set splits between 300 and 470 K (the temperatures of T-102 and T-103).
   If it does at a column's temperatures, use UNIQUAC as that column's own method (rule E allows it) and record why.
3. The liquid heat-capacity extrapolation warnings (bdo above 353.15 K, butanol above 390.81 K, acid above 400 K).
