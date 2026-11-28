# Cases

One folder per process or unit studied. Each holds the inputs with their sources, CHEPTA's outputs as returned, the
comparison with the source, and a study record (`study-record.json`, the case's lab notebook page; see
[docs/HOW_IT_WORKS.md](../docs/HOW_IT_WORKS.md)). Each README starts with an "In one look" table.

| Case | Source | Simulated | Complete flowsheet? | Agreement | Reviewed? |
|---|---|---|---|---|---|
| [ethanol-zsm5-573k](ethanol-zsm5-573k/README.md) | Aali & Hadi 2023 | reactor only | no | matches an independent calculation | no |
| [benzene-toluene-chemsep-b2](benzene-toluene-chemsep-b2/README.md) | The ChemSep Book | one column | no | within 0.80 K, 0.018 (book's specifications); purity-specified runs (0.6.1 and 0.6.2) outside those limits; same numbers on 0.6.2 | no |
| [methanol-separator-flash](methanol-separator-flash/README.md) | CHEPTA's own notes | one flash drum | no | same as CHEPTA's earlier result (0.6.0, 0.6.1 and 0.6.2) | no |
| [ethyl-acetate-piotrowski-2021](ethyl-acetate-piotrowski-2021/README.md) | Piotrowski & Kubica 2021 | classic plant S2: all 19 units and 28 streams (chepta 0.6.1); on 0.6.2 the whole plant as one flowsheet with all recycles | **closed and settled on 0.6.2** (balance within 0.1 kg/h); BLOCKED on the product purity: 99.11 % vs 99.90 % | azeotrope stream within 0.01 %, product +0.3 %, 7 of 11 duties within 7 % (0.6.1); units with acetic acid on 0.6.2 agree as well; reactor conversion taken from the paper | no |
| [methanol-co2-campos-2022](methanol-co2-campos-2022/README.md) | Lacerda de Oliveira Campos et al. 2022 | one-step plant (without fired heater and steam cycle) as one closed CHEPTA flowsheet, chepta 0.6.2 | plant converges with workarounds (trace bypass, fixed column bottoms) | methanol 99.73 vs 99.67 mol %, water 99.999 vs 99.985; FLASH3 liquid CO2 3.4 vs 18.5 %, CO2 recycle -86 %; HE7 supports Table S14; 5 capability requests | no |
| [ethyl-acetate-sulgan-2020](ethyl-acetate-sulgan-2020/README.md) | Šulgan, Labovský & Labovská 2020 | nothing yet: conventional set-up transcribed (32 streams, 19 units) and its balances audited | not run yet | the paper's own table closes within rounding | no |
| [ethylene-glycol-shehata-2024](ethylene-glycol-shehata-2024/README.md) | Shehata, Nady & Gad 2024 | nothing yet: direct hydration plant transcribed (14 streams of Table 3, T and P of 30 streams on Fig. 5, 21 blocks) and its balances audited; dataset table for the maintainer | not run yet | the paper's table closes except the water recycle (3 kmol/h) and the MEG column's water (2.6 kmol/h); 11 text-table disagreements | AI full check only |
| [butyl-acetate-al-rabiah-2022](butyl-acetate-al-rabiah-2022/README.md) | Al-Rabiah et al. 2022 | nothing yet: conventional plant transcribed (14 streams of Table 7, 14 blocks of Figure 11) and its balances audited; rule A checked on chepta 0.6.3 (all components present, 3 pairs estimated); dataset table for the maintainer | not run yet | material balances close everywhere; energy does not at the two mixers (streams 3 and 9) and in the fresh-feed enthalpies; 12 text-figure-table disagreements | no |

## A new case

A complete flowsheet from one paper: the paper's streams and units with page and table, run through the released
CHEPTA's command line, compared stream by stream, every refusal and warning kept, then a study record. Results are
never edited by hand, and older runs keep their CHEPTA version. The steps are in the building-cases skill
([.claude/skills/building-cases/SKILL.md](../.claude/skills/building-cases/SKILL.md)); running CHEPTA follows the
solving-simulations skill.

## Before the first run

Write down the comparison while the published values and the simulation inputs are still easy to tell apart. Use the existing case notes and study record. [Study record proposal, “Constraints: declared before, compared after”](../docs/proposals/0002-study-record.md#constraints-declared-before-compared-after)

| Record | What the next agent needs |
|---|---|
| Boundary and basis | Paper variant, included units, omitted sections, stream IDs, mass or mole basis, wet or dry basis where relevant, flow units and the reference state for duties. |
| Fixed inputs and adjusted settings | Mark values imposed directly from the source. Preserve the first request and result. For each adjusted setting, record its range, reason and run IDs. |
| Independent comparisons | Name the output, stream, unit, limit or comparison tolerance, and its source before execution. For trace impurities use an absolute deviation on the stated basis. Explain tolerances from printed precision, measurement uncertainty or the decision being made. Keep the solver’s tolerance separate. |
| Evidence and verdict | Describe whether the reference is a measurement, another simulation or an independent calculation. Report the observed discrepancy and whether the predeclared criterion was met. If the run failed, record its error and leave the target unevaluated. Mark retrospective criteria as reconstructed. |

For example, the ester case imposes reactor conversion from the paper. Agreement on conversion gives no independent test of the reactor model. Its simulated product purity **is** a comparison and the shortfall is part of the result. The methanol case similarly states the fired heater and steam cycle were outside the simulated boundary. [Ester case](ethyl-acetate-piotrowski-2021/README.md) · [Methanol case](methanol-co2-campos-2022/README.md)

Preserve the evidence chain from source location through conversion, exact input, engine version and output to each reported comparison. When a published duty conflicts with the printed stream enthalpies, preserve both source values and the arithmetic. Record which value each subsequent conclusion uses. A separate reviewer should be able to reconstruct the comparison. [Sandve et al. (2013), rules 1, 3 and 9](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285) · [Oberkampf & Trucano, verification and validation benchmarks](https://doi.org/10.1016/j.nucengdes.2007.02.032) · [Methanol case, HE7](methanol-co2-campos-2022/STREAM_AUDIT.md)
