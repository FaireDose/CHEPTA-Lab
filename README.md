# CHEPTA-Lab

**What this is.** We take processes from published papers, rebuild them in the simulator
[CHEPTA](https://github.com/FaireDose/CHEPTA), and record honestly what CHEPTA reproduces, what differs and what
CHEPTA cannot do yet. From those checked cases we write questions with checked answers: a dataset to test, and maybe
later to teach, an AI assistant that uses CHEPTA.

**Read first:** [How it works, in plain words](docs/HOW_IT_WORKS.md).

## Where things stand (2026-11-13)

| Case | Paper | What was simulated in CHEPTA | Complete flowsheet? | Agrees with the paper? | Reviewed by a person? |
|---|---|---|---|---|---|
| [Ethanol to ethylene](cases/ethanol-zsm5-573k/README.md) | Aali & Hadi 2023 | the reactor only (6 variants); same numbers on CHEPTA 0.6.1 and 0.6.2 (0.6.2 lists three extrapolations) | no | not compared with experiment; matches an independent calculation | no |
| [Benzene + toluene column](cases/benzene-toluene-chemsep-b2/README.md) | The ChemSep Book | one distillation column | no (a column example, not a plant) | yes with the book's own specifications, within 0.80 K and 0.018 mole fraction. With purity or recovery specifications (new in 0.6.1) the column is **not** within those limits, also on 0.6.2 (same numbers) | no |
| [Methanol separator](cases/methanol-separator-flash/README.md) | none: an example state from CHEPTA's notes | one flash drum; same numbers on CHEPTA 0.6.1 and 0.6.2 (0.6.2 lists one extrapolation, the H2 + CO k_ij) | no | not a paper case | no |
| [Ethyl acetate plant](cases/ethyl-acetate-piotrowski-2021/README.md) | Piotrowski & Kubica 2021 | the classic plant (S2): all 19 units and 28 streams, CHEPTA 0.6.1 | **once through, not closed**: cut at stream 9, because CHEPTA cannot yet do two liquids with acetic acid | azeotrope within 0.01 %, product within 0.3 %, 7 of 11 duties within 7 %; the reactor conversion is taken from the paper | no |

**First complete flowsheet from a paper: the ethyl acetate plant**, run once through. Closing its recycles needs two
liquid phases with acetic acid, which CHEPTA is building now (Lab's request). Problems the plant shows, and the
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

`chepta@0.6.2` from npm (since 2026-11-13), fixed in [package.json](package.json); details in [data/upstream.json](data/upstream.json).
The ethanol, B2 and methanol cases were re-run on it with default options; each has a `COMPATIBILITY_0.6.2.md` saying what is identical,
changed, newly refused or newly accepted, and which extrapolations and estimated pairs each run used. (The ethyl acetate plant still
states 0.6.1 above until its own re-run is merged.) 0.6.2 continues outside a record's range with a warning instead of refusing, and estimates
missing activity-model pairs from Modified UNIFAC 2.0; none of the three cases used an estimated pair. Older runs keep the version they were made
with (0.6.0 and 0.6.1 results sit beside the 0.6.2 ones).

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
