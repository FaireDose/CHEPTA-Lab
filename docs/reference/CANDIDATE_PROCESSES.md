# Candidate reaction processes

Audit: 2026-10-29, CHEPTA [c1adf6bab522](https://github.com/FaireDose/CHEPTA/commit/c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2).

**None of these is training-ready.** Existing reactor tests are evidence of an upstream example, not a newly reproduced full flowsheet. Unit lists below are implementation candidates, not confirmation of every required mode or property.

| Priority | Process | Starting scope | What blocks the complete process |
|---|---|---|---|
| 1 | CO2 to methanol | Reactor, cooling, flash, recycle and purge | Paper kinetics/specifications audit; distillation for purified product |
| 2 | Ethyl acetate esterification | Existing equilibrium reactor; later conventional kinetic CSTR plant | Columns, mixture phase behavior, vapor association, rate-based versus equilibrium-stage methods |
| 3 | Ethanol to ethylene/diethyl ether | Existing catalytic PFR example | Source-unit/experimental review; downstream columns; industrial network/transport audit |
| 4 | Cumene hydroperoxide to phenol/acetone | Existing teaching CSTR | Open process paper, source rights, mixture data and purification |
| 5 | Benzene pyrolysis | Deferred | p-Terphenyl ideal-gas heat capacity and process source |
| 6 | HMF to levulinic/formic acids | Deferred | Levulinic-acid ideal-gas heat capacity and process source |

## Important source distinctions

- The methanol paper uses a kinetic PFR. Replacing it with CHEPTA's existing equilibrium example creates a different case, which must be labelled.
- The Sulgan ethyl-acetate paper's conventional plant is the first target. Its reactive-distillation alternatives need additional capabilities beyond ordinary separation columns.
- The two ethanol reactor papers use different model detail. Do not transplant catalyst parameters or collapse side products without a documented change of scope.
- CHEPTA's generic A → B + C textbook test uses named chemicals as stand-ins. It is not accepted here as evidence for real industrial ethane kinetics.
- A component splitter is not a substitute for a missing physical separation model.

See [the machine-readable records](../../data/candidates.json) for source IDs, existing unit types, blockers and next actions. CHEPTA provenance: [worked examples](https://github.com/FaireDose/CHEPTA/blob/c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2/docs/models/reactions.md), [column engine](https://github.com/FaireDose/CHEPTA/blob/c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2/src/units/columns/engine.js), [dispatcher](https://github.com/FaireDose/CHEPTA/blob/c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2/src/api/dispatcher.js).

First reactor work is executed: [ethanol benchmark](../../cases/ethanol-zsm5-573k/README.md), with six runs and numerical checks. The family is only partially reproduced. Next prepare a common-basis process-route comparison and continue the methanol supplement audit.
