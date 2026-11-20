# Knowledge-base index (generated; do not edit)

People: the same rows as plain sentences are in [rules-readable.md](rules-readable.md).

Made by `python scripts/kb.py index` from dataset/records/ and data/ISSUES_AND_ROUTES.md; held-out groups left out. Next: `python scripts/kb.py query` with `--problem`, `--behaviour`, `--components`, `--operation`, `--symptom`, `--kind` or `--status`, then `python scripts/kb.py show <row id>`. Terms: `python scripts/kb.py terms`.

W/F/L/U: rows worked / failed / lead / untested (for CHEPTA runs, the latest engine per condition). D: disputed sets (worked against failed, or rows naming each other in disputed_with). P: sources (papers, books). Used y/p/n: later cases it helped / partly / not. Files: dataset/records/<file>.json.

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
| absorber-column | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | palomar-2024-il-process-simulation |
| azeotropic-distillation | no-convergence | 0/0/7/0 | 0 | 1 | 0/0/0 | kruber-skiborowski-2022-heteroazeotropic-init |
| azeotropic-distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | kruber-skiborowski-2022-heteroazeotropic-init |
| azeotropic-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | kruber-skiborowski-2022-heteroazeotropic-init |
| distillation | no-convergence | 1/1/5/0 | 0 | 4 | 0/0/0 | ethyl-acetate-piotrowski-2021,henrique-2020-dwc-simulation,kruber-skiborowski-2022-heteroazeotropic-init,steffen-2024-rd-modelling-review |
| distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | kooijman-taylor-2006-chemsep-book |
| distillation | wrong-phase | 0/0/3/0 | 0 | 3 | 0/0/0 | jankovic-2023-ipa-acetone-recovery,palomar-2024-il-process-simulation,pasha-2021-biodiesel-process-design |
| extraction | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | grisales-2017-abe-extraction |
| extraction | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | fu-2021-isobutanol-recovery |
| extractive-distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | li-2017-ed-thermo-parameters |
| extractive-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | li-2017-ed-thermo-parameters |
| flash | no-convergence | 0/0/1/0 | 0 | 1 | 0/0/0 | andreasen-2022-dwsim-evaluation |
| reactive-distillation | no-convergence | 0/0/2/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | purity-short | 0/0/2/0 | 0 | 2 | 0/0/0 | othman-2024-meg-reactive-distillation,steffen-2024-rd-modelling-review |
| reactive-distillation | slow | 0/0/1/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | wrong-phase | 0/0/2/0 | 0 | 2 | 0/0/0 | al-rabiah-2022,othman-2024-meg-reactive-distillation |
| recycle | no-convergence | 0/0/2/0 | 0 | 2 | 0/0/0 | larsson-skogestad-2000-plantwide,palomar-2024-il-process-simulation |
| recycle | recycle-drift | 0/0/1/0 | 0 | 1 | 0/0/0 | andreasen-2022-dwsim-evaluation |

## General design rules: one line per operation

| operation | behaviours | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|
| absorber-column | non-condensable-gas | 0/0/2/0 | 0 | 1 | 0/0/0 | palomar-2024-il-process-simulation |
| azeotropic-distillation | azeotrope-heterogeneous,azeotrope-min-boiling,close-boiling,dilute-product,equilibrium-limited-reaction,two-liquid-phases | 0/0/12/0 | 0 | 3 | 0/0/0 | guo-wang-2019-azeotropic-distillation,kruber-skiborowski-2022-heteroazeotropic-init,valentini-2020-azeotropes-waste |
| cstr | equilibrium-limited-reaction | 0/0/2/0 | 0 | 2 | 0/0/0 | hoff-eisenacher-2025-esterification-review,pasha-2021-biodiesel-process-design |
| decanter | azeotrope-heterogeneous,equilibrium-limited-reaction,trace-impurity-limit,two-liquid-phases | 0/0/6/0 | 0 | 5 | 0/0/0 | al-rabiah-2022,fu-2021-isobutanol-recovery,guo-wang-2019-azeotropic-distillation,kruber-skiborowski-2022-heteroazeotropic-init,pasha-2021-biodiesel-process-design |
| distillation | azeotrope-min-boiling,close-boiling,dilute-product,hazardous-component,heat-sensitive,recycle-loop,side-products,trace-impurity-limit,zeotropic-multicomponent | 0/0/19/0 | 1 | 8 | 0/0/0 | al-rabiah-2022,blahusiak-2018-separation-selection,byrne-2016-solvent-selection-guides,chen-2018-abe-distillation,henrique-2020-dwc-simulation,jankovic-2023-ipa-acetone-recovery,li-2023-distillation-sequences,shehata-2024-meg-routes |
| equilibrium-reactor | equilibrium-limited-reaction,exothermic-reaction | 0/0/1/0 | 0 | 1 | 0/0/0 | al-rabiah-2022 |
| extraction | associating-acid-vapour,azeotrope-heterogeneous,close-boiling,dilute-product,hazardous-component,two-liquid-phases | 0/0/8/0 | 0 | 4 | 0/0/0 | blahusiak-2018-separation-selection,byrne-2016-solvent-selection-guides,fu-2021-isobutanol-recovery,grisales-2017-abe-extraction |
| extractive-distillation | azeotrope-min-boiling,close-boiling,dilute-product,recycle-loop | 0/0/7/0 | 0 | 5 | 0/0/0 | al-rabiah-2022,blahusiak-2018-separation-selection,jankovic-2023-ipa-acetone-recovery,li-2017-ed-thermo-parameters,mtogo-2021-ed-vs-psd |
| flash | dilute-product,non-condensable-gas | 0/0/1/0 | 0 | 1 | 0/0/0 | jankovic-2023-ipa-acetone-recovery |
| heat-integration | azeotrope-heterogeneous,azeotrope-min-boiling,close-boiling,dilute-product,exothermic-reaction,heat-recovery-potential,heat-sensitive,zeotropic-multicomponent | 0/0/15/0 | 0 | 7 | 0/0/0 | ali-2022-eg-plant-pinch,blahusiak-2018-separation-selection,jankovic-2023-ipa-acetone-recovery,kruber-skiborowski-2022-heteroazeotropic-init,li-2023-distillation-sequences,pasha-2021-biodiesel-process-design,shehata-2024-meg-routes |
| membrane | equilibrium-limited-reaction | 0/0/3/0 | 0 | 1 | 0/0/0 | al-rabiah-2022 |
| pervaporation | azeotrope-heterogeneous,equilibrium-limited-reaction | 0/0/3/0 | 0 | 2 | 0/0/0 | hoff-eisenacher-2025-esterification-review,valentini-2020-azeotropes-waste |
| pfr | equilibrium-limited-reaction,exothermic-reaction,recycle-loop,side-products | 0/0/4/0 | 0 | 3 | 0/0/0 | al-rabiah-2022,othman-2024-meg-reactive-distillation,shehata-2024-meg-routes |
| pressure-swing-distillation | azeotrope-min-boiling | 0/0/2/0 | 0 | 1 | 0/0/0 | mtogo-2021-ed-vs-psd |
| process-route | azeotrope-min-boiling,equilibrium-limited-reaction,hazardous-component | 0/0/10/0 | 0 | 2 | 0/0/0 | al-rabiah-2022,park-2022-inherently-safer-design |
| purge | non-condensable-gas,purge-and-make-up,recycle-loop | 0/0/1/0 | 0 | 1 | 0/0/0 | larsson-skogestad-2000-plantwide |
| reactive-distillation | azeotrope-min-boiling,close-boiling,endothermic-reaction,equilibrium-limited-reaction,exothermic-reaction,side-products,two-liquid-phases | 0/0/23/0 | 0 | 6 | 0/0/0 | al-rabiah-2022,hoff-eisenacher-2025-esterification-review,kiss-2024-rd-conceptual-methods,muthia-2018-rd-applicability,orjuela-2006-butyl-acetate-rcm,othman-2024-meg-reactive-distillation |
| recycle | equilibrium-limited-reaction,recycle-loop,side-products,trace-impurity-limit | 0/0/7/0 | 1 | 5 | 0/0/0 | al-rabiah-2022,chen-2018-abe-distillation,larsson-skogestad-2000-plantwide,pasha-2021-biodiesel-process-design,shehata-2024-meg-routes |
