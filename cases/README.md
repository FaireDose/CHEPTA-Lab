# Cases

One folder per process or unit studied. Each holds the inputs with their sources, CHEPTA's outputs as returned, the
comparison with the source, and a study record (`study-record.json`, the case's lab notebook page; see
[docs/HOW_IT_WORKS.md](../docs/HOW_IT_WORKS.md)). Each README starts with an "In one look" table.

| Case | Source | Simulated | Complete flowsheet? | Agreement | Reviewed? |
|---|---|---|---|---|---|
| [ethanol-zsm5-573k](ethanol-zsm5-573k/README.md) | Aali & Hadi 2023 | reactor only | no | matches an independent calculation | no |
| [benzene-toluene-chemsep-b2](benzene-toluene-chemsep-b2/README.md) | The ChemSep Book | one column | no | within 0.80 K, 0.018 (book's specifications); purity-specified runs on 0.6.1 outside those limits | no |
| [methanol-separator-flash](methanol-separator-flash/README.md) | CHEPTA's own notes | one flash drum | no | same as CHEPTA's earlier result (0.6.0 and 0.6.1) | no |
| [ethyl-acetate-piotrowski-2021](ethyl-acetate-piotrowski-2021/README.md) | Piotrowski & Kubica 2021 | classic plant S2: all 19 units and 28 streams (chepta 0.6.1); on 0.6.2 the whole plant as one flowsheet with all recycles | **not closed (BLOCKED on 0.6.2)**: column 5 `NO_CONVERGENCE` inside the closed loop; plant compared once through (0.6.1) | azeotrope stream within 0.01 %, product +0.3 %, 7 of 11 duties within 7 % (0.6.1); units with acetic acid on 0.6.2 agree as well; reactor conversion taken from the paper | no |

## A new case

A complete flowsheet from one paper: the paper's streams and units with page and table, run through the released
CHEPTA's command line, compared stream by stream, every refusal and warning kept, then a study record. Results are
never edited by hand, and older runs keep their CHEPTA version.
