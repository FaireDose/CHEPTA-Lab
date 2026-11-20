# Knowledge-base index (generated; do not edit)

Made by `python scripts/kb.py index` from dataset/records/ and data/ISSUES_AND_ROUTES.md; held-out groups left out. Next: `python scripts/kb.py query` with `--problem`, `--behaviour`, `--components`, `--operation`, `--symptom`, `--kind` or `--status`, then `python scripts/kb.py show <row id>`. Terms: `python scripts/kb.py terms`.

W/F/L/U: rows worked / failed / lead / untested (for CHEPTA runs, the latest engine per condition). D: disputed sets. P: sources (papers, books). Used y/p/n: later cases it helped / partly / not. Files: dataset/records/<file>.json.

## Design: one line per register problem

| problem | level | operations | behaviours | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|---|---|
| sep-ester-alcohol-water-azeotrope | separation | distillation,extraction,extractive-distillation,heat-exchange | azeotrope-min-boiling,trace-impurity-limit,two-liquid-phases | 3/0/1/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021,pilot |
| sep-two-liquids-with-acetic-acid | separation | distillation | associating-acid-vapour,azeotrope-min-boiling,two-liquid-phases | 1/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| sep-acid-stripping-from-ester-vapour | separation | - | - | 0/0/0/0 | 0 | 0 | 0/0/0 | - |
| rxn-esterification-equilibrium-limited | reaction | - | - | 0/0/0/0 | 0 | 0 | 0/0/0 | - |
| plant-recycles-makeup-purge | plant | - | - | 0/0/0/0 | 0 | 0 | 0/0/0 | - |

## Simulation: one line per operation and symptom

| operation | symptom | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|
| distillation | no-convergence | 1/1/2/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,steffen-2024-rd-modelling-review |
| distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | kooijman-taylor-2006-chemsep-book |
| extractive-distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | li-2017-ed-thermo-parameters |
| extractive-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | li-2017-ed-thermo-parameters |
| flash | no-convergence | 0/0/1/0 | 0 | 1 | 0/0/0 | andreasen-2022-dwsim-evaluation |
| reactive-distillation | no-convergence | 0/0/2/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | purity-short | 0/0/2/0 | 0 | 2 | 0/0/0 | othman-2024-meg-reactive-distillation,steffen-2024-rd-modelling-review |
| reactive-distillation | slow | 0/0/1/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | othman-2024-meg-reactive-distillation |
| recycle | no-convergence | 0/0/1/0 | 0 | 1 | 0/0/0 | larsson-skogestad-2000-plantwide |
| recycle | recycle-drift | 0/0/1/0 | 0 | 1 | 0/0/0 | andreasen-2022-dwsim-evaluation |

## General design rules: one line per operation

| operation | behaviours | W/F/L/U | P | used y/p/n | files |
|---|---|---|---|---|---|
| azeotropic-distillation | azeotrope-heterogeneous,equilibrium-limited-reaction,two-liquid-phases | 0/0/2/0 | 1 | 0/0/0 | guo-wang-2019-azeotropic-distillation |
| cstr | equilibrium-limited-reaction | 0/0/1/0 | 1 | 0/0/0 | hoff-eisenacher-2025-esterification-review |
| decanter | azeotrope-heterogeneous | 0/0/1/0 | 1 | 0/0/0 | guo-wang-2019-azeotropic-distillation |
| distillation | close-boiling,heat-sensitive,side-products,zeotropic-multicomponent | 0/0/6/0 | 2 | 0/0/0 | li-2023-distillation-sequences,shehata-2024-meg-routes |
| extractive-distillation | azeotrope-min-boiling,close-boiling | 0/0/2/0 | 2 | 0/0/0 | li-2017-ed-thermo-parameters,mtogo-2021-ed-vs-psd |
| heat-integration | exothermic-reaction,heat-sensitive,zeotropic-multicomponent | 0/0/3/0 | 2 | 0/0/0 | li-2023-distillation-sequences,shehata-2024-meg-routes |
| pervaporation | equilibrium-limited-reaction | 0/0/2/0 | 1 | 0/0/0 | hoff-eisenacher-2025-esterification-review |
| pfr | exothermic-reaction,side-products | 0/0/2/0 | 2 | 0/0/0 | othman-2024-meg-reactive-distillation,shehata-2024-meg-routes |
| pressure-swing-distillation | azeotrope-min-boiling | 0/0/2/0 | 1 | 0/0/0 | mtogo-2021-ed-vs-psd |
| purge | non-condensable-gas,purge-and-make-up,recycle-loop | 0/0/1/0 | 1 | 0/0/0 | larsson-skogestad-2000-plantwide |
| reactive-distillation | close-boiling,endothermic-reaction,equilibrium-limited-reaction,exothermic-reaction,side-products,two-liquid-phases | 0/0/17/0 | 5 | 0/0/0 | hoff-eisenacher-2025-esterification-review,kiss-2024-rd-conceptual-methods,muthia-2018-rd-applicability,orjuela-2006-butyl-acetate-rcm,othman-2024-meg-reactive-distillation |
| recycle | recycle-loop | 0/0/4/0 | 2 | 0/0/0 | larsson-skogestad-2000-plantwide,shehata-2024-meg-routes |
