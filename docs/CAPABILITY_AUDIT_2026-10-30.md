# P01 — CHEPTA capability audit and initial scope

Date: 2026-10-30. Status: source audit complete for the selected scope; runtime confirmation pending. This completes P01's capability matrix, not all M0 acceptance work.

Engine pinned to [4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce](https://github.com/FaireDose/CHEPTA/commit/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce). Earlier runs remain pinned to c1adf6bab5220bbb334e90e16a8fe20d1ea66ac2. This audit does not migrate or overwrite them.

## Initial family scope

| Family | Useful initial tasks | Current capability | Remaining gate | Next owner/action |
|---|---|---|---|---|
| Ethanol → ethylene/diethyl ether | Explain kinetic-model differences; replay the existing isothermal PFR; diagnose warnings | PFR and expression kinetics documented; six historical Lab runs exist | Source pressure units, applicability warnings and experimental evidence remain unresolved. Current-revision replay has not run. Full downstream purification is not established. | Engineering/source review: P02 narrows and reviews the historical task. Software: P03 replays it separately at the new pin. |
| Ethyl acetate esterification | Evidence-backed separation selection; equilibrium reaction calculations; ordinary-column subproblems | Equilibrium/reactive-flash reactor and rigorous VL/VLL columns exist | Multistage LL extraction is explicitly unsupported. Reactive flash is not reactive distillation. Dimerizing-acid column chemistry is unsupported. Existing S1/S2 source discrepancies and paper-specific kinetics/specifications still need review. | Engineering: retain conditional selection; do not promise complete S1/S2 reproduction. |
| CO₂ → methanol | Reaction-equilibrium explanation; later cooling/flash/recycle subproblems | Equilibrium/Gibbs reactors and generic flash/recycle infrastructure documented | The target paper's kinetic PFR is not reproduced by an equilibrium reactor. Supplement inputs, kinetics and full product specifications still need extraction/review. | Literature: resolve paper model inputs before numerical targets. |

These three families are the initial collection scope, not three supported complete plants. Expand after independent source coverage and actual runtime evidence.

## Interface and operation matrix

All availability labels below describe inspected source, not new runtime results.

| Need | Finding at this revision | Evidence |
|---|---|---|
| Capability discovery and typed requests | Registered capability metadata includes status and input schema; solve_column is now available. | dispatcher.js: capabilities(), solve_column registration |
| Project and degree-of-freedom checks | check_project and flowsheet_status are registered. Unit specStatus checks specification freedom. | dispatcher.js; units.js: specStatus; flowsheet.js: flowsheetStatus |
| Port names and writable fields | unitTypes()/unitType() expose registered ports and specKeys internally; no dedicated generic unit-metadata dispatcher capability was found in the inspected dispatcher. Build a small pinned metadata view for the adapter. | units.js: registerUnit, unitTypes, unknownSpecKey |
| Ordinary distillation | Shortcut and rigorous MESH; rigorous takes stages/feed stages plus two independent operating specifications. Direct purity targets remain unsupported; assess resulting purity externally. | column.js: checkSpec, RIGOROUS_SPECS; columns.md |
| Two liquids/decanter | VLL activity-model column stages and condenser decanter implemented; decanter takes one operating specification. This does not establish LL extraction support. | column.js; columns.md |
| Extraction, absorption/stripping, reactive distillation | LL extraction explicitly refused. Absorber/stripper configurations are described as future work; no paper reproduction claim. Reaction inside a column is not established by the inspected interface. | column.js: extraction refusal; columns.md introduction |
| Flash and liquid split | Flash block exposes vapour, liquid and optional liquid2; applicability depends on method and data. Multistage extraction is a separate operation. | units.js: flash registration |
| Recycles | Marked tears and guesses; Broyden, Wegstein or direct methods. Automatic tear selection refuses beyond four tears unless supplied explicitly. | flowsheet.js: chooseTears, solveFlowsheet |
| Warm starts | Low-level solveCascade accepts a previous solution. The inspected column wrapper does not pass it, and start is absent from specKeys. Do not advertise request-level warm starts. | engine.js: startU; column.js: SPEC_KEYS and solveCascade call |
| Checkpoints | No durable checkpoint API found in the inspected request path. Lab should save versioned requests/responses and retain its last successful configuration. This is not internal solver-state recovery. | dispatcher.js; column.js |
| Failure and warning retention | Dispatcher distinguishes invalid_input, missing_data, unsupported and not_converged; output includes balances, column residuals, qualifications and warnings. Preserve nested observations too. | dispatcher.js: OUTCOMES, solvedFlowsheet |
| Thermodynamics | Reuse existing CHEPTA method/data selection and validation. Check the exact mixture, range and mode for each case; package presence alone proves no process coverage. | columns.md; reactions.md |

## Concrete second numerical case selected

Use the existing **B2 benzene/toluene ChemSep column** as P03's second numerical case alongside ethanol. It adds a separation benchmark without waiting for a complete reaction–separation paper reconstruction. It is a unit benchmark outside the three reaction families, not another independent reaction process.

Inputs and comparison limits come from the pinned upstream record:
[validation/data/columns/B2-chemsep-benzene-toluene.json](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/validation/data/columns/B2-chemsep-benzene-toluene.json).
The record attributes the published example to The ChemSep Book, §§1.2–1.3, with precise figure/page locators. Lab has inspected the upstream transcription; direct source and release-rights review remain pending.

Preserve the source's capacity for reproduction. Convert its mol/s flows to kmol/h explicitly (multiply by 3.6). Run the pinned PR method; record that the source used another property method and constant molar overflow. Separate same-equation numerical verification from agreement with published values. Use the actual pinned record's comparison limits (1 K and 0.02 absolute mole fraction), not the tighter numbers still mentioned in parts of upstream prose. These are inter-model agreement limits, not experimental accuracy.

P03 acceptance: actual calls and engine hashes; published-profile comparisons; component/energy balances; all warnings; one intentional invalid or unsupported request; last-successful-artifact preservation. No numerical result is claimed here.

## Blocker priority and continuation

1. **P03 / software:** acquire the pinned runtime and build the thin local adapter; execute ethanol and B2 without paid model calls.
2. **P02 / engineering and sources:** prepare human-review packets for current claims and tasks; preserve source uncertainties and qualify outputs.
3. **M0 / coordinator:** map each eventual v1 performance claim to a task-specific rubric and an accountable reviewer. Human reviewer identity is still unassigned.
4. **M5 / engineering:** a complete process remains gated by applicable unit modes, source reconciliation and a full-process acceptance contract.

A source audit can establish interface support or an explicit refusal. Only actual execution can establish these Lab requests run. This packet neither approves training rows nor deploys a public service.

## Inspected source locations

All links are pinned to the audited engine:
- [Dispatcher](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/src/api/dispatcher.js)
- [Unit registry and specification checks](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/src/units/units.js)
- [Flowsheet solver](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/src/flowsheet/flowsheet.js)
- [Column wrapper](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/src/units/columns/column.js)
- [Column engine](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/src/units/columns/engine.js)
- [Column methods and limitations](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/docs/models/columns.md)
- [Reaction examples and validation references](https://github.com/FaireDose/CHEPTA/blob/4a8a9cfb13ea46f5d0747dc65e25ab45a5d9e1ce/docs/models/reactions.md)
