# Knowledge-base index (generated; do not edit)

People: the same rows as plain sentences are in [rules-readable.md](rules-readable.md).

Made by `python scripts/kb.py index` from dataset/records/ and data/ISSUES_AND_ROUTES.md; held-out groups left out. Next: `python scripts/kb.py query` with `--problem`, `--behaviour`, `--components`, `--operation`, `--symptom`, `--kind` or `--status`, then `python scripts/kb.py show <row id>`. Terms: `python scripts/kb.py terms`.

W/F/L/U: rows worked / failed / lead / untested (for CHEPTA runs, the latest engine per condition). D: disputed sets (worked against failed, or rows naming each other in disputed_with). P: sources (papers, books). Used y/p/n: later cases it helped / partly / not. Files: dataset/records/<file>.json.

## Design: one line per register problem

| problem | level | operations | behaviours | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|---|---|
| sep-ester-alcohol-water-azeotrope | separation | azeotropic-distillation,distillation,extraction,extractive-distillation,heat-exchange | azeotrope-min-boiling,component-without-exit,trace-impurity-limit,two-liquid-phases | 8/12/2/1 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021,pilot |
| sep-two-liquids-with-acetic-acid | separation | distillation,extraction,heat-exchange | associating-acid-vapour,azeotrope-min-boiling,two-liquid-phases | 4/2/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| sep-acid-stripping-from-ester-vapour | separation | absorber-column | associating-acid-vapour,azeotrope-min-boiling,equilibrium-limited-reaction,recycle-loop,trace-impurity-limit,two-liquid-phases | 4/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| rxn-esterification-equilibrium-limited | reaction | heat-exchange,reactor-evaporator | equilibrium-limited-reaction,recycle-loop | 4/0/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| plant-recycles-makeup-purge | plant | distillation,purge,recycle | associating-acid-vapour,component-without-exit,purge-and-make-up,recycle-loop,trace-impurity-limit,two-liquid-phases | 7/10/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| rxn-co2-hydrogenation-methanol | reaction | pfr | equilibrium-limited-reaction,exothermic-reaction | 2/0/0/0 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| sep-co2-dissolved-in-methanol-water | separation | flash | non-condensable-gas,purge-and-make-up,recycle-loop | 2/1/0/1 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| sep-methanol-water-with-dissolved-gases | separation | distillation | non-condensable-gas,purge-and-make-up,recycle-loop | 5/7/0/1 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| plant-gas-recycle-with-purge | plant | purge,recycle | non-condensable-gas,purge-and-make-up,recycle-loop | 3/2/0/0 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| plant-feed-effluent-heat-recovery | plant | heat-exchange | heat-recovery-potential,non-condensable-gas,purge-and-make-up,recycle-loop | 3/4/1/0 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |

## Simulation: one line per operation and symptom

| operation | symptom | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|
| absorber-column | no-convergence | 0/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| absorber-column | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | palomar-2024-il-process-simulation |
| absorber-column | wrong-phase | 1/0/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| distillation | no-convergence | 1/9/4/0 | 0 | 4 | 0/0/0 | ethyl-acetate-piotrowski-2021,henrique-2020-dwc-simulation,methanol-co2-campos-2022,steffen-2024-rd-modelling-review |
| distillation | purity-short | 0/8/1/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,kooijman-taylor-2006-chemsep-book |
| distillation | slow | 1/0/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| distillation | wrong-phase | 0/0/2/0 | 0 | 2 | 0/0/0 | palomar-2024-il-process-simulation,pasha-2021-biodiesel-process-design |
| extraction | feed-refused | 1/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| extraction | no-convergence | 0/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| extraction | purity-short | 0/2/1/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,grisales-2017-abe-extraction |
| extraction | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | fu-2021-isobutanol-recovery |
| extractive-distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | li-2017-ed-thermo-parameters |
| extractive-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | li-2017-ed-thermo-parameters |
| flash | feed-refused | 0/1/0/0 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| flash | no-convergence | 0/0/1/0 | 0 | 1 | 0/0/0 | andreasen-2022-dwsim-evaluation |
| heat-exchange | feed-refused | 2/2/0/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,methanol-co2-campos-2022 |
| heat-exchange | section-fails | 0/2/0/0 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| reactive-distillation | no-convergence | 0/0/2/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | purity-short | 0/0/2/0 | 0 | 2 | 0/0/0 | othman-2024-meg-reactive-distillation,steffen-2024-rd-modelling-review |
| reactive-distillation | slow | 0/0/1/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | othman-2024-meg-reactive-distillation |
| recycle | no-convergence | 0/3/2/0 | 0 | 3 | 0/0/0 | ethyl-acetate-piotrowski-2021,larsson-skogestad-2000-plantwide,palomar-2024-il-process-simulation |
| recycle | purity-short | 0/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| recycle | recycle-drift | 1/1/1/0 | 0 | 2 | 0/0/0 | andreasen-2022-dwsim-evaluation,ethyl-acetate-piotrowski-2021 |
| recycle | section-fails | 0/2/0/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,methanol-co2-campos-2022 |
| recycle | slow | 1/2/0/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,methanol-co2-campos-2022 |

## General design rules: one line per operation

| operation | behaviours | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|
| absorber-column | non-condensable-gas | 0/0/2/0 | 0 | 1 | 0/0/0 | palomar-2024-il-process-simulation |
| azeotropic-distillation | azeotrope-heterogeneous,azeotrope-min-boiling,close-boiling,equilibrium-limited-reaction,two-liquid-phases | 0/0/6/0 | 0 | 2 | 0/0/0 | guo-wang-2019-azeotropic-distillation,valentini-2020-azeotropes-waste |
| cstr | equilibrium-limited-reaction | 0/0/2/0 | 0 | 2 | 0/0/0 | hoff-eisenacher-2025-esterification-review,pasha-2021-biodiesel-process-design |
| decanter | azeotrope-heterogeneous,equilibrium-limited-reaction,two-liquid-phases | 0/0/3/0 | 0 | 3 | 0/0/0 | fu-2021-isobutanol-recovery,guo-wang-2019-azeotropic-distillation,pasha-2021-biodiesel-process-design |
| distillation | close-boiling,hazardous-component,heat-sensitive,side-products,trace-impurity-limit,zeotropic-multicomponent | 0/0/12/0 | 1 | 6 | 0/0/0 | blahusiak-2018-separation-selection,byrne-2016-solvent-selection-guides,chen-2018-abe-distillation,henrique-2020-dwc-simulation,li-2023-distillation-sequences,shehata-2024-meg-routes |
| extraction | associating-acid-vapour,azeotrope-heterogeneous,close-boiling,dilute-product,hazardous-component,two-liquid-phases | 0/0/8/0 | 0 | 4 | 0/0/0 | blahusiak-2018-separation-selection,byrne-2016-solvent-selection-guides,fu-2021-isobutanol-recovery,grisales-2017-abe-extraction |
| extractive-distillation | azeotrope-min-boiling,close-boiling | 0/0/3/0 | 0 | 3 | 0/0/0 | blahusiak-2018-separation-selection,li-2017-ed-thermo-parameters,mtogo-2021-ed-vs-psd |
| heat-integration | close-boiling,exothermic-reaction,heat-recovery-potential,heat-sensitive,zeotropic-multicomponent | 0/0/9/0 | 0 | 5 | 0/0/0 | ali-2022-eg-plant-pinch,blahusiak-2018-separation-selection,li-2023-distillation-sequences,pasha-2021-biodiesel-process-design,shehata-2024-meg-routes |
| pervaporation | azeotrope-heterogeneous,equilibrium-limited-reaction | 0/0/3/0 | 0 | 2 | 0/0/0 | hoff-eisenacher-2025-esterification-review,valentini-2020-azeotropes-waste |
| pfr | exothermic-reaction,side-products | 0/0/2/0 | 0 | 2 | 0/0/0 | othman-2024-meg-reactive-distillation,shehata-2024-meg-routes |
| pressure-swing-distillation | azeotrope-min-boiling | 0/0/2/0 | 0 | 1 | 0/0/0 | mtogo-2021-ed-vs-psd |
| purge | non-condensable-gas,purge-and-make-up,recycle-loop | 0/0/1/0 | 0 | 1 | 0/0/0 | larsson-skogestad-2000-plantwide |
| reactive-distillation | azeotrope-min-boiling,close-boiling,endothermic-reaction,equilibrium-limited-reaction,exothermic-reaction,side-products,two-liquid-phases | 0/0/21/0 | 0 | 5 | 0/0/0 | hoff-eisenacher-2025-esterification-review,kiss-2024-rd-conceptual-methods,muthia-2018-rd-applicability,orjuela-2006-butyl-acetate-rcm,othman-2024-meg-reactive-distillation |
| recycle | recycle-loop,side-products,trace-impurity-limit | 0/0/6/0 | 1 | 4 | 0/0/0 | chen-2018-abe-distillation,larsson-skogestad-2000-plantwide,pasha-2021-biodiesel-process-design,shehata-2024-meg-routes |
