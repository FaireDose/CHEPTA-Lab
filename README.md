# CHEPTA-Lab

**What this is.** We take processes from published papers, rebuild them in the simulator
[CHEPTA](https://github.com/FaireDose/CHEPTA), and record honestly what CHEPTA reproduces, what differs and what
CHEPTA cannot do yet. From those checked cases we write questions with checked answers: a dataset to test, and maybe
later to teach, an AI assistant that uses CHEPTA.

**Read first:** [How it works, in plain words](docs/HOW_IT_WORKS.md).

## Where things stand (2026-11-20)

- **Two complete plants from papers run closed in CHEPTA 0.6.2:**
  - ethyl acetate (Piotrowski & Kubica 2021): product 99.11 % against the paper's 99.90 %;
  - CO2 to methanol (Lacerda de Oliveira Campos et al. 2022): with labelled workarounds.
- **Two more plants are chosen:** ethylene glycol and butyl acetate ([docs/CANDIDATE_PROCESSES.md](docs/CANDIDATE_PROCESSES.md)).
  CHEPTA moves to 0.7 once all four have run.
- **Every case**, with its agreement and review state: [cases/README.md](cases/README.md).
- **What the cases taught**, problem by problem: [data/ISSUES_AND_ROUTES.md](data/ISSUES_AND_ROUTES.md).
- **Dataset:** 3 draft questions with answers, **0 accepted**; accepted means reviewed ([dataset/](dataset/README.md)).

## Folders

| Folder | What is in it |
|---|---|
| [cases/](cases/README.md) | One folder per process or unit studied: its inputs, CHEPTA's outputs, the comparison with the paper, and a study record (the case's lab notebook page) |
| [dataset/](dataset/README.md) | The questions with checked answers, and the tools that check and export them |
| [data/](data/README.md) | The list of papers (with access and licence), the candidate processes, the CHEPTA version Lab uses |
| [docs/](docs/README.md) | How it works, the simulation practices, the process design method, the plant choice, the coordinator's handover; earlier plans in docs/reference/ |
| [.claude/skills/](.claude/skills/) | Three short guides for AI sessions (solving simulations, building cases, process design), each pointing to the detailed files |
| `scripts/`, `tests/` | The checking programs and their tests |
| [AGENTS.md](AGENTS.md) | The rules for anyone (person or AI) working here |

## The CHEPTA version Lab uses

`chepta@0.6.2` from npm, fixed in [package.json](package.json); details in [data/upstream.json](data/upstream.json). Older
runs keep the version they were made with. Checks of CHEPTA's unreleased code (for example commit 415da41, before
0.6.3) sit in their own `results-chepta-main-<commit>/` folders and never replace a case's result.

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
