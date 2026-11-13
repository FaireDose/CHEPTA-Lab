# CHEPTA-Lab

**What this is.** We take processes from published papers, rebuild them in the simulator
[CHEPTA](https://github.com/FaireDose/CHEPTA), and record honestly what CHEPTA reproduces, what differs and what
CHEPTA cannot do yet. From those checked cases we write questions with checked answers: a dataset to test, and maybe
later to teach, an AI assistant that uses CHEPTA.

**Read first:** [How it works, in plain words](docs/HOW_IT_WORKS.md).

## Where things stand (2026-11-12)

| Case | Paper | What was simulated in CHEPTA | Complete flowsheet? | Agrees with the paper? | Reviewed by a person? |
|---|---|---|---|---|---|
| [Ethanol to ethylene](cases/ethanol-zsm5-573k/README.md) | Aali & Hadi 2023 | the reactor only (6 variants); same numbers on CHEPTA 0.6.1 | no | not compared with experiment; matches an independent calculation | no |
| [Benzene + toluene column](cases/benzene-toluene-chemsep-b2/README.md) | The ChemSep Book | one distillation column | no (a column example, not a plant) | yes with the book's own specifications, within 0.80 K and 0.018 mole fraction. With purity or recovery specifications (new in 0.6.1) the column is **not** within those limits | no |
| [Methanol separator](cases/methanol-separator-flash/README.md) | none: an example state from CHEPTA's notes | one flash drum; same numbers on CHEPTA 0.6.1, now with fit-quality warnings | no | not a paper case | no |
| [Ethyl acetate plant](cases/ethyl-acetate-piotrowski-2021/README.md) | Piotrowski & Kubica 2021 | the classic plant (S2): all 19 units and 28 streams, CHEPTA 0.6.1; on CHEPTA 0.6.2 the whole plant as one flowsheet with all recycles | **not closed**: on 0.6.2 the plant is one flowsheet with acetic acid everywhere, but column 5 does not converge inside the closed loop; compared once through (0.6.1) | azeotrope within 0.01 %, product within 0.3 %, 7 of 11 duties within 7 %; the reactor conversion is taken from the paper | no |

**First complete flowsheet from a paper: the ethyl acetate plant**, run once through. CHEPTA 0.6.2 now does two liquid
phases with acetic acid, so the whole plant is one CHEPTA flowsheet; it does not yet converge (column 5 inside the
closed loop; capability requests 8 to 12 in the case README). Problems the plant shows, and the
routes used for them, are in [data/ISSUES_AND_ROUTES.md](data/ISSUES_AND_ROUTES.md). **Next:** questions with checked
answers from this plant.

**Dataset:** 3 draft questions with answers, **0 accepted** (accepted means reviewed by you). See
[dataset/](dataset/README.md).

## Folders

| Folder | What is in it |
|---|---|
| [cases/](cases/README.md) | One folder per process or unit studied: its inputs, CHEPTA's outputs, the comparison with the paper, and a study record (the case's lab notebook page) |
| [dataset/](dataset/README.md) | The questions with checked answers, and the tools that check and export them |
| [data/](data/README.md) | The list of papers (with access and licence), the candidate processes, the CHEPTA version Lab uses |
| [docs/](docs/README.md) | Explanations and plans: how it works, where we are heading, the coordinator's handover, earlier planning documents |
| `scripts/`, `tests/` | The checking programs and their tests |
| [AGENTS.md](AGENTS.md) | The rules for anyone (person or AI) working here |

## The CHEPTA version Lab uses

`chepta@0.6.1` from npm (since 2026-11-12), fixed in [package.json](package.json); details in [data/upstream.json](data/upstream.json).
All three cases were re-run on it; each case has a `COMPATIBILITY_0.6.1.md` saying what is identical, changed, newly
refused or newly accepted. Older runs keep the version they were made with (0.6.0 results sit beside the 0.6.1 ones).

## Checks

```bash
python scripts/validate_catalog.py          # the list of papers and processes is consistent
python scripts/dataset_pipeline.py validate # dataset items and study records are complete and unchanged
python -m unittest discover -s tests        # the checking programs work
```

Passing these checks means the files are consistent. It does not mean a number is right: that needs a person to
compare it with its source.

## Licences

Code: MIT ([LICENSE](LICENSE)). The dataset licence is not decided yet. Papers keep their own terms; see
[docs/LICENSING.md](docs/LICENSING.md). Security: [SECURITY.md](SECURITY.md).
