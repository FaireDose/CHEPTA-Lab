# Knowledge-base index (generated; do not edit)

Made by `python scripts/kb.py index` from dataset/records/ and data/ISSUES_AND_ROUTES.md; held-out groups left out. One line per problem. Next: `python scripts/kb.py query --problem <id>` (or `--behaviour`, `--components`, `--operation`, `--status`, `--level`), then `python scripts/kb.py show <row id>`. Terms: `python scripts/kb.py terms`.

W/F/L/U: rows worked / failed / lead / untested (for CHEPTA runs, the latest engine per condition). D: disputed sets. P: papers. Files: dataset/records/<file>.json.

| problem | level | operations | behaviours | W/F/L/U | D | P | files |
|---|---|---|---|---|---|---|---|
| sep-ester-alcohol-water-azeotrope | separation | distillation,extraction,heat-exchange | azeotrope-min-boiling,trace-impurity-limit,two-liquid-phases | 3/0/0/0 | 0 | 1 | pilot |
| sep-two-liquids-with-acetic-acid | separation | distillation | associating-acid-vapour,azeotrope-min-boiling,two-liquid-phases | 1/1/0/0 | 0 | 1 | ethyl-acetate-piotrowski-2021 |
| sep-acid-stripping-from-ester-vapour | separation | - | - | 0/0/0/0 | 0 | 0 | - |
| rxn-esterification-equilibrium-limited | reaction | - | - | 0/0/0/0 | 0 | 0 | - |
| plant-recycles-makeup-purge | plant | - | - | 0/0/0/0 | 0 | 0 | - |
