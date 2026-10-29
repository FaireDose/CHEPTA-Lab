# CHEPTA-Lab

Engineering simulation cases and training data for AI assistants that use CHEPTA and, eventually, other simulators.

**Current stage: research catalogue, dataset preparation and one executed draft reactor benchmark. No model has been trained. No case is yet a validated training example.**

## Start here

1. [Candidate processes](docs/CANDIDATE_PROCESSES.md): six reaction families, required units and blockers.
2. [Initial papers](docs/INITIAL_PAPERS.md): five priority papers, two additional paper leads and one book reference.
3. [Project plan](docs/PROJECT_PLAN.md): the agreed goal and next tasks.
4. [First executed case](cases/ethanol-zsm5-573k/README.md): two model variants, six runs and independent checks.
5. [Dataset guide](dataset/README.md): what one checked example must contain.

## How this relates to CHEPTA

[CHEPTA](https://github.com/FaireDose/CHEPTA) owns the simulator. This repository owns literature screening, process cases, training examples and evaluations. We reuse CHEPTA's engine rather than copy it.

The initial audit is pinned to CHEPTA commit [c1adf6bab522](https://github.com/FaireDose/CHEPTA/commit/c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2) on 2026-10-29. Its JSON dispatcher exists; its column engine explicitly reports that it is not built yet. The ethanol reactor benchmark has now been executed through the dispatcher; other capability findings remain a source audit.

## Repository contents

- `data/sources.json`: source metadata, exact locators, access checks and rights status.
- `data/candidates.json`: case readiness, dependencies and outstanding work.
- `data/upstream.json`: the CHEPTA revision behind the audit.
- `dataset/example.template.json`: an empty example template, not training data.
- `cases/`: executable draft cases, source ledgers and numerical verification.
- `scripts/validate_catalog.py`: consistency checks for the catalogue.
- `docs/`: the readable research plan and source audit.

Run the metadata checks with Python 3 (no extra packages):

```bash
python scripts/validate_catalog.py
```

Passing these checks means the catalogue is internally consistent. It does not verify a paper's numbers or validate a simulation.

## First milestone

The first ethanol benchmark has been run and numerically checked. Human review, source-unit resolution and experimental validation remain pending. Next, prepare two process routes on a common basis before expanding the reviewed collection or renting training hardware.

GitHub is the working record. A checked dataset release can later be published on Hugging Face, followed by a model adaptation and evaluation. No paid compute or external publication is configured here.

See [source and licensing policy](docs/LICENSING.md). Repository, dataset and model licensing are separate decisions; third-party material retains its own terms.


## First process comparison

[Ethyl acetate comparison audit](comparisons/ethyl-acetate/README.md): source values, a proposed common basis, discrepancies and execution gates. Two configurations are specified; full-plant simulation remains blocked at the pinned revision.

## Dataset architecture

See [the dataset map and diagrams](docs/DATASET_DESIGN.md) for physical evidence, justified operation selection, general process sequences and capacity normalization. Templates are draft scaffolds; existing cases retain their original schema versions.
