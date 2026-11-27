# Knowledge-base index (generated; do not edit)

People: the same rows as plain sentences are in [rules-readable.md](rules-readable.md).

Made by `python scripts/kb.py index` from dataset/records/ and data/ISSUES_AND_ROUTES.md; held-out groups left out. Next: `python scripts/kb.py query` with `--problem`, `--behaviour`, `--components`, `--operation`, `--symptom`, `--kind` or `--status`, then `python scripts/kb.py show <row id>`. Terms: `python scripts/kb.py terms`.

W/F/L/U: rows worked / failed / lead / untested (for CHEPTA runs, the latest engine per condition). D: disputed sets (worked against failed, or rows naming each other in disputed_with). P: sources (papers, books). Used y/p/n: later cases it helped / partly / not. Files: dataset/records/<file>.json.

## Design: one line per register problem

| problem | level | operations | behaviours | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|---|---|
| sep-ester-alcohol-water-azeotrope | separation | azeotropic-distillation,distillation,extraction,extractive-distillation,heat-exchange | azeotrope-min-boiling,component-without-exit,trace-impurity-limit,two-liquid-phases | 8/14/2/1 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021,pilot |
| sep-two-liquids-with-acetic-acid | separation | distillation,extraction,heat-exchange | associating-acid-vapour,azeotrope-min-boiling,two-liquid-phases | 5/3/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| sep-acid-stripping-from-ester-vapour | separation | absorber-column | associating-acid-vapour,azeotrope-min-boiling,equilibrium-limited-reaction,recycle-loop,trace-impurity-limit,two-liquid-phases | 5/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| rxn-esterification-equilibrium-limited | reaction | heat-exchange,reactor-evaporator | equilibrium-limited-reaction,recycle-loop | 4/0/0/0 | 0 | 1 | 1/0/0 | ethyl-acetate-piotrowski-2021 |
| plant-recycles-makeup-purge | plant | distillation,purge,recycle | associating-acid-vapour,component-without-exit,purge-and-make-up,recycle-loop,trace-impurity-limit,two-liquid-phases | 6/13/0/0 | 0 | 1 | 3/0/0 | ethyl-acetate-piotrowski-2021 |
| rxn-co2-hydrogenation-methanol | reaction | pfr | equilibrium-limited-reaction,exothermic-reaction | 2/0/0/0 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| sep-co2-dissolved-in-methanol-water | separation | flash | non-condensable-gas,purge-and-make-up,recycle-loop | 2/1/0/1 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| sep-methanol-water-with-dissolved-gases | separation | distillation | non-condensable-gas,purge-and-make-up,recycle-loop | 5/7/0/1 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| plant-gas-recycle-with-purge | plant | purge,recycle | non-condensable-gas,purge-and-make-up,recycle-loop | 3/2/0/0 | 0 | 1 | 1/0/0 | methanol-co2-campos-2022 |
| plant-feed-effluent-heat-recovery | plant | heat-exchange | heat-recovery-potential,non-condensable-gas,purge-and-make-up,recycle-loop | 3/4/1/0 | 0 | 1 | 1/1/0 | methanol-co2-campos-2022 |
| rxn-ethylene-oxide-hydration-heavy-glycols | reaction | pfr | side-products | 1/0/0/1 | 0 | 1 | 0/0/0 | ethylene-glycol-shehata-2024 |
| sep-water-from-dilute-glycol | separation | distillation,flash | dilute-product,heat-sensitive | 1/0/0/3 | 0 | 1 | 0/0/0 | ethylene-glycol-shehata-2024 |
| sep-glycol-homologues-heat-sensitive | separation | distillation | heat-sensitive,side-products | 1/0/0/2 | 0 | 1 | 0/0/0 | ethylene-glycol-shehata-2024 |
| plant-large-water-recycle | plant | heat-exchange,recycle | heat-recovery-potential,purge-and-make-up,recycle-loop | 1/0/0/3 | 0 | 1 | 0/0/0 | ethylene-glycol-shehata-2024 |

## Simulation: one line per operation and symptom

| operation | symptom | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|
| absorber-column | no-convergence | 1/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| absorber-column | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | palomar-2024-il-process-simulation |
| absorber-column | wrong-phase | 1/0/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| azeotropic-distillation | no-convergence | 0/0/7/0 | 0 | 1 | 0/0/0 | kruber-skiborowski-2022-heteroazeotropic-init |
| azeotropic-distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | kruber-skiborowski-2022-heteroazeotropic-init |
| azeotropic-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | kruber-skiborowski-2022-heteroazeotropic-init |
| distillation | no-convergence | 1/10/5/0 | 0 | 5 | 0/0/0 | ethyl-acetate-piotrowski-2021,henrique-2020-dwc-simulation,kruber-skiborowski-2022-heteroazeotropic-init,methanol-co2-campos-2022,steffen-2024-rd-modelling-review |
| distillation | purity-short | 0/9/1/0 | 0 | 2 | 1/0/0 | ethyl-acetate-piotrowski-2021,kooijman-taylor-2006-chemsep-book |
| distillation | slow | 1/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| distillation | wrong-phase | 0/0/3/0 | 0 | 3 | 2/0/0 | jankovic-2023-ipa-acetone-recovery,palomar-2024-il-process-simulation,pasha-2021-biodiesel-process-design |
| extraction | feed-refused | 1/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| extraction | no-convergence | 0/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| extraction | purity-short | 0/2/1/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,grisales-2017-abe-extraction |
| extraction | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/0 | fu-2021-isobutanol-recovery |
| extractive-distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | li-2017-ed-thermo-parameters |
| extractive-distillation | wrong-phase | 0/0/1/0 | 0 | 1 | 0/0/1 | li-2017-ed-thermo-parameters |
| flash | feed-refused | 0/1/0/0 | 0 | 1 | 0/0/0 | methanol-co2-campos-2022 |
| flash | no-convergence | 0/0/1/0 | 0 | 1 | 1/0/0 | andreasen-2022-dwsim-evaluation |
| heat-exchange | feed-refused | 2/2/0/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,methanol-co2-campos-2022 |
| heat-exchange | section-fails | 0/2/0/0 | 0 | 1 | 0/1/0 | methanol-co2-campos-2022 |
| purge | recycle-drift | 0/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| reactive-distillation | no-convergence | 0/0/2/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | purity-short | 0/0/2/0 | 0 | 2 | 0/0/0 | othman-2024-meg-reactive-distillation,steffen-2024-rd-modelling-review |
| reactive-distillation | slow | 0/0/1/0 | 0 | 1 | 0/0/0 | steffen-2024-rd-modelling-review |
| reactive-distillation | wrong-phase | 0/0/2/0 | 0 | 2 | 0/0/1 | al-rabiah-2022,othman-2024-meg-reactive-distillation |
| recycle | no-convergence | 0/3/2/0 | 0 | 3 | 1/0/0 | ethyl-acetate-piotrowski-2021,larsson-skogestad-2000-plantwide,palomar-2024-il-process-simulation |
| recycle | purity-short | 0/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| recycle | recycle-drift | 1/1/1/0 | 0 | 2 | 2/0/0 | andreasen-2022-dwsim-evaluation,ethyl-acetate-piotrowski-2021 |
| recycle | section-fails | 0/2/0/0 | 0 | 2 | 1/0/0 | ethyl-acetate-piotrowski-2021,methanol-co2-campos-2022 |
| recycle | slow | 1/3/0/0 | 0 | 2 | 0/0/0 | ethyl-acetate-piotrowski-2021,methanol-co2-campos-2022 |
| recycle | wrong-phase | 0/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |

## General design rules: one line per operation

| operation | behaviours | W/F/L/U | D | P | used y/p/n | files |
|---|---|---|---|---|---|---|
| absorber-column | non-condensable-gas | 0/0/2/0 | 0 | 1 | 0/0/0 | palomar-2024-il-process-simulation |
| azeotropic-distillation | azeotrope-heterogeneous,azeotrope-min-boiling,close-boiling,dilute-product,equilibrium-limited-reaction,two-liquid-phases | 0/0/12/0 | 0 | 3 | 0/0/0 | guo-wang-2019-azeotropic-distillation,kruber-skiborowski-2022-heteroazeotropic-init,valentini-2020-azeotropes-waste |
| cstr | equilibrium-limited-reaction | 0/0/2/0 | 0 | 2 | 0/0/0 | hoff-eisenacher-2025-esterification-review,pasha-2021-biodiesel-process-design |
| decanter | azeotrope-heterogeneous,equilibrium-limited-reaction,trace-impurity-limit,two-liquid-phases | 0/0/6/0 | 0 | 5 | 0/0/0 | al-rabiah-2022,fu-2021-isobutanol-recovery,guo-wang-2019-azeotropic-distillation,kruber-skiborowski-2022-heteroazeotropic-init,pasha-2021-biodiesel-process-design |
| distillation | azeotrope-min-boiling,close-boiling,dilute-product,hazardous-component,heat-sensitive,recycle-loop,side-products,trace-impurity-limit,zeotropic-multicomponent | 0/0/19/0 | 1 | 8 | 1/1/3 | al-rabiah-2022,blahusiak-2018-separation-selection,byrne-2016-solvent-selection-guides,chen-2018-abe-distillation,henrique-2020-dwc-simulation,jankovic-2023-ipa-acetone-recovery,li-2023-distillation-sequences,shehata-2024-meg-routes |
| equilibrium-reactor | equilibrium-limited-reaction,exothermic-reaction | 0/0/1/0 | 0 | 1 | 0/0/0 | al-rabiah-2022 |
| extraction | associating-acid-vapour,azeotrope-heterogeneous,close-boiling,dilute-product,hazardous-component,two-liquid-phases | 0/0/8/0 | 0 | 4 | 0/0/0 | blahusiak-2018-separation-selection,byrne-2016-solvent-selection-guides,fu-2021-isobutanol-recovery,grisales-2017-abe-extraction |
| extractive-distillation | azeotrope-min-boiling,close-boiling,dilute-product,recycle-loop | 0/0/7/0 | 0 | 5 | 0/0/0 | al-rabiah-2022,blahusiak-2018-separation-selection,jankovic-2023-ipa-acetone-recovery,li-2017-ed-thermo-parameters,mtogo-2021-ed-vs-psd |
| flash | dilute-product,non-condensable-gas | 0/0/1/0 | 0 | 1 | 0/0/0 | jankovic-2023-ipa-acetone-recovery |
| heat-integration | azeotrope-heterogeneous,azeotrope-min-boiling,close-boiling,dilute-product,exothermic-reaction,heat-recovery-potential,heat-sensitive,zeotropic-multicomponent | 0/0/15/0 | 0 | 7 | 0/1/0 | ali-2022-eg-plant-pinch,blahusiak-2018-separation-selection,jankovic-2023-ipa-acetone-recovery,kruber-skiborowski-2022-heteroazeotropic-init,li-2023-distillation-sequences,pasha-2021-biodiesel-process-design,shehata-2024-meg-routes |
| membrane | equilibrium-limited-reaction | 0/0/3/0 | 0 | 1 | 0/0/0 | al-rabiah-2022 |
| pervaporation | azeotrope-heterogeneous,equilibrium-limited-reaction | 0/0/3/0 | 0 | 2 | 0/0/0 | hoff-eisenacher-2025-esterification-review,valentini-2020-azeotropes-waste |
| pfr | equilibrium-limited-reaction,exothermic-reaction,recycle-loop,side-products | 0/0/4/0 | 0 | 3 | 0/2/0 | al-rabiah-2022,othman-2024-meg-reactive-distillation,shehata-2024-meg-routes |
| pressure-swing-distillation | azeotrope-min-boiling | 0/0/2/0 | 0 | 1 | 0/0/0 | mtogo-2021-ed-vs-psd |
| process-route | azeotrope-min-boiling,equilibrium-limited-reaction,hazardous-component | 0/0/10/0 | 0 | 2 | 0/0/0 | al-rabiah-2022,park-2022-inherently-safer-design |
| purge | non-condensable-gas,purge-and-make-up,recycle-loop | 0/0/1/0 | 0 | 1 | 0/0/0 | larsson-skogestad-2000-plantwide |
| reactive-distillation | azeotrope-min-boiling,close-boiling,endothermic-reaction,equilibrium-limited-reaction,exothermic-reaction,side-products,two-liquid-phases | 0/0/23/0 | 0 | 6 | 0/0/0 | al-rabiah-2022,hoff-eisenacher-2025-esterification-review,kiss-2024-rd-conceptual-methods,muthia-2018-rd-applicability,orjuela-2006-butyl-acetate-rcm,othman-2024-meg-reactive-distillation |
| recycle | equilibrium-limited-reaction,recycle-loop,side-products,trace-impurity-limit | 0/0/7/0 | 1 | 5 | 1/0/0 | al-rabiah-2022,chen-2018-abe-distillation,larsson-skogestad-2000-plantwide,pasha-2021-biodiesel-process-design,shehata-2024-meg-routes |
