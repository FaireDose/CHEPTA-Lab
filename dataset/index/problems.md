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
| distillation | no-convergence | 1/1/0/0 | 0 | 1 | 0/0/0 | ethyl-acetate-piotrowski-2021 |
| distillation | purity-short | 0/0/1/0 | 0 | 1 | 0/0/0 | kooijman-taylor-2006-chemsep-book |

## General design rules: one line per operation

| operation | behaviours | W/F/L/U | P | used y/p/n | files |
|---|---|---|---|---|---|
| (none yet) | - | - | - | - | - |
