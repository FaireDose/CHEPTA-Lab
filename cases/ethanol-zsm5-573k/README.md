# Ethanol / ZSM-5: first executed draft benchmark

| In one look | |
|---|---|
| Paper | Aali & Hadi 2023 (ethanol dehydration over ZSM-5, 573 K) |
| Simulated | the catalytic plug-flow reactor only, two kinetic variants at three catalyst loadings (6 runs) |
| Complete flowsheet | no: no separation section |
| CHEPTA version | commit c1adf6b (2026-10-29), re-run on `chepta@0.6.0` with identical numbers ([COMPATIBILITY_0.6.0.md](COMPATIBILITY_0.6.0.md)) |
| Agreement | matches an independent Python calculation; not compared with the paper's experiments |
| Open | the paper's pressure units; ethanol + water parameters used outside their temperature range |
| Reviewed by a person | no |

**Status: numerical checks passed; human review pending; not eligible for training.**

The first step now has runnable inputs, actual CHEPTA outputs, an independent calculation and a source audit. It compares an existing implementation with a more complete adsorption expression. These are two model variants of one reactor, not two competing complete process routes.

## What ran

CHEPTA commit `c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2`, using its `solve_flowsheet` JSON dispatcher. Pure ethanol, 1 mol/h, 573.15 K, 101.325 kPa; isothermal PFR without pressure drop. Three W/F values within the reported interval. The upstream variant omits product adsorption; the second adds Table-12 terms to Equations 4 and 14 using the same Table-8/9 constants.

| Run | Ethanol conversion (%) | Largest component relative difference vs independent ODE |
|---|---:|---:|
| upstream_simplified-wf0.38 | 0.337102 | 9.81e-08 |
| upstream_simplified-wf0.773 | 0.685136 | 2.5e-07 |
| upstream_simplified-wf1.166 | 1.032557 | 3.61e-07 |
| table12_adsorption-wf0.38 | 0.331163 | 2.35e-06 |
| table12_adsorption-wf0.773 | 0.661353 | 2.74e-06 |
| table12_adsorption-wf1.166 | 0.980123 | 3.07e-06 |

At W/F = 1.166 g catalyst h/mol, including product adsorption changes conversion by -5.078% relative to the simplified result. Both calculations converge and pass atom balances. This establishes sensitivity to an assumption, not which prediction matches experiment.

## Re-run on the released package

On 2026-11-11 the same six requests were re-run on `chepta@0.6.0` with unchanged numbers; see [COMPATIBILITY_0.6.0.md](COMPATIBILITY_0.6.0.md) and `results-chepta-0.6.0/`. The results above and everything below describe the original commit-`c1adf6b` runs.

## Evidence

- [Input values](input.json) and [source/units/assumptions ledger](SOURCE_LEDGER.md), including the additional constants found in Table 12.
- [Run manifest](results/run-manifest.json): six calls, versions, key source hashes and paths to unabridged requests/outputs.
- [Independent verification](results/verification.json): separate species-flow ODE, component comparisons, atom/mass checks and internal energy closure. Thresholds and their rationale are recorded.
- [Case record](record.json): draft status, engineering decisions, limitations and pending reviews.
- [Study record](study-record.json): draft hand-over to CHEPTA ([proposal 0002](../../docs/proposals/0002-study-record.md)); indexes the six requests and results above by path and sha256 without changing them.

The targeted upstream ethanol test also passed (1 test, 0 failures). The independent check here uses SciPy DOP853 in mol/h and grams catalyst; CHEPTA integrates reaction extents along reactor length. Neither comparison uses experimental outlet observations.

## Reproduce

Use Node 24 and Python 3 with NumPy/SciPy. Observed Python package versions are in verification.json; pinned reproduction dependencies are in requirements-reference.txt. From the CHEPTA-Lab repository root:

```bash
git clone https://github.com/FaireDose/CHEPTA.git ../CHEPTA-reference
git -C ../CHEPTA-reference checkout c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2
python -m venv .venv
.venv/bin/python -m pip install -r cases/ethanol-zsm5-573k/requirements-reference.txt
node cases/ethanol-zsm5-573k/run.mjs ../CHEPTA-reference
.venv/bin/python cases/ethanol-zsm5-573k/verify.py
python scripts/validate_catalog.py
```

No engine build or npm installation was needed for these source-module calls. Rerunning overwrites this case's generated results; Git retains earlier versions. Generated `*.request.json` files can also be passed directly to CHEPTA's dispatcher. These are API flowsheet requests, not claimed as workbench project-save files. The initial execution used an archive requested by full commit, so its manifest has a null Git-observed revision and records key file hashes; normal Git checkouts are checked against the expected HEAD.

## Acceptance gaps and learning target

The PDF's pressure-unit conventions need resolution. The paper's Figure 8 uses another model, so it is not reproduced here. Original experimental data and catalyst details are still needed. PR stream warnings include missing pairs and an ethanol/water parameter outside its fit range. The fixed-T/P rate expressions use yP; numerical agreement does not validate duties or phase equilibrium. These qualifications remain in the saved outputs even where top-level warnings are empty.

The eventual example should teach: inspect all relevant source tables; distinguish a simplification from the published rate model; quantify its effect; preserve warnings; and stop short of an unsupported engineering recommendation. Human engineering and final release rights reviews remain pending. No model was trained and no paid compute was used.

## Update 2026-11-12: chepta@0.6.1

The six runs were repeated on 0.6.1: identical numbers and warnings ([COMPATIBILITY_0.6.1.md](COMPATIBILITY_0.6.1.md), [results-chepta-0.6.1/](results-chepta-0.6.1/)).
