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

Lab pins released CHEPTA versions: the current pin is the npm package [`chepta@0.6.0`](https://www.npmjs.com/package/chepta/v/0.6.0) (published 2026-11-11, MIT; exact version in `package.json`, integrity hash in `package-lock.json` and `data/upstream.json`; install with `npm ci`). The [compatibility check](cases/ethanol-zsm5-573k/COMPATIBILITY_0.6.0.md) re-ran the six ethanol runs on it with unchanged numbers and one reworded warning. The first audit and the original ethanol runs used CHEPTA commit [c1adf6bab522](https://github.com/FaireDose/CHEPTA/commit/c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2) of 2026-10-29, kept as history in `data/upstream.json`; old results keep that engine version. The source audits (capabilities, columns) were done on earlier revisions and have not been re-run on 0.6.0.

## Repository contents

- `data/sources.json`: source metadata, exact locators, access checks and rights status.
- `data/candidates.json`: case readiness, dependencies and outstanding work.
- `data/upstream.json`: the current CHEPTA pin (npm package) and the earlier audited commit.
- `package.json`, `package-lock.json`: exact engine pin; `node_modules/` is not committed.
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

See [source and licensing policy](docs/LICENSING.md) and [security and integrity](SECURITY.md). The code is under the MIT License ([LICENSE](LICENSE)); the dataset license is still to be decided. Repository, dataset and model licensing are separate decisions; third-party material retains its own terms.


## First process comparison

[Ethyl acetate comparison audit](comparisons/ethyl-acetate/README.md): source values, a proposed common basis, discrepancies and execution gates. Two configurations are specified; full-plant simulation remains blocked at the pinned revision.

## Dataset architecture

See [the dataset map and diagrams](docs/DATASET_DESIGN.md) for physical evidence, justified operation selection, general process sequences and capacity normalization. Templates are draft scaffolds; existing cases retain their original schema versions.

## Evidence-to-training pilot

The [pipeline guide](dataset/PIPELINE.md) explains schemas, task-specific review and deterministic exports. [Initial collection](dataset/COLLECTION_LOG.md): 7 source blocks, 9 evidence records, 3 decisions, 1 historical execution trace and 3 draft tasks. No accepted training examples.

```bash
python -m pip install -r requirements-dataset.txt
python scripts/dataset_pipeline.py validate
python -m unittest discover -s tests
python scripts/dataset_pipeline.py preview --out /tmp/chepta-lab-preview-v1
```

Use a new output directory for each export. Previews are for review only; release currently refuses because all tasks are drafts.

## Delivery milestones

See [the delivery plan](docs/DELIVERY_PLAN.md) for the bounded v1 deliverable, milestone acceptance criteria, engineering/AI responsibilities, token controls and the next five work packets. Current collection and software checks are a pilot; engineering acceptance and model performance remain unproven.

## Current capability audit

[P01 capability matrix, 2026-10-30](docs/CAPABILITY_AUDIT_2026-10-30.md) inspects CHEPTA revision `4a8a9cfb13ea`. Ordinary rigorous and VLL columns now exist; LL extraction and direct column purity specifications remain unsupported. The earlier audit and executed runs above describe their original revision. Initial collection scope: ethanol dehydration, ethyl acetate and CO2-to-methanol. The second numerical case selected for runtime integration is the upstream ChemSep benzene/toluene column. New-revision runtime execution and engineering acceptance remain pending.
