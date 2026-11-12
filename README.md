# CHEPTA-Lab

**What this is.** We take processes from published papers, rebuild them in the simulator
[CHEPTA](https://github.com/FaireDose/CHEPTA), and record honestly what CHEPTA reproduces, what differs and what
CHEPTA cannot do yet. From those checked cases we write questions with checked answers: a dataset to test, and maybe
later to teach, an AI assistant that uses CHEPTA.

**Read first:** [How it works, in plain words](docs/HOW_IT_WORKS.md).

## Where things stand (2026-11-12)

| Case | Paper | What was simulated in CHEPTA | Complete flowsheet? | Agrees with the paper? | Reviewed by a person? |
|---|---|---|---|---|---|
| [Ethanol to ethylene](cases/ethanol-zsm5-573k/README.md) | Aali & Hadi 2023 | the reactor only (6 variants) | no | not compared with experiment; matches an independent calculation | no |
| [Benzene + toluene column](cases/benzene-toluene-chemsep-b2/README.md) | The ChemSep Book | one distillation column | no (a column example, not a plant) | yes, within 0.80 K and 0.018 mole fraction | no |
| [Methanol separator](cases/methanol-separator-flash/README.md) | none: an example state from CHEPTA's notes | one flash drum | no | not a paper case | no |
| [Ethyl acetate plant](cases/ethyl-acetate-piotrowski-2021/README.md) | Piotrowski & Kubica 2021 | **nothing run yet**; 56 streams and 19 units copied from the paper and their balances checked | not yet | – | no |

**No complete flowsheet from a paper has been simulated yet.** CHEPTA lacked what the plants need (columns with
purity targets, acetic acid in a column) until its release 0.6.1. **Next:** the complete ethyl acetate plant,
stream by stream against the paper.

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

`chepta@0.6.0` from npm, fixed in [package.json](package.json); details in [data/upstream.json](data/upstream.json).
Older runs keep the version they were made with.

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
