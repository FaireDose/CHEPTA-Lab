# Lessons from four process-simulation AI papers

Reviewed 2026-10-30. These are selective additions to the existing knowledge-guided methodology, not a new architecture. **Documentation adopted; runtime checks and evaluation experiments below are not implemented by this review.** No records become accepted and no model training starts.

## Sources and reading scope

Read the main-text methods, results and limitations. Supplementary packages and independent code reproduction were outside this review. Preprint findings are tied to the versions below, not assumed identical to later journal versions.

| ID | Paper and inspected version | Relevant locations |
|---|---|---|
| ETH | [Text-to-flowsheet: an LLM-assisted pipeline for expert-level digitization and automated simulation of chemical processes](https://doi.org/10.1039/D6DD00060F), published article; full text through [NCBI BioC](https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_xml/PMC13251679/unicode) | §§2.1–2.3, 3.1–3.3 |
| BASF | [Context is all you need: Towards autonomous model-based process design using agentic AI in flowsheet simulations](https://arxiv.org/html/2603.12813v1), arXiv v1 | §§3.1–3.4, 4.4 |
| DTU | [Large Language Model Agent for User-friendly Chemical Process Simulations](https://arxiv.org/html/2601.11650v2), arXiv v2 | §3 tool table, §§5.1–5.2, 6 |
| ECUST | [From Text to Simulation: A Multi-Agent LLM Workflow for Automated Chemical Process Design](https://arxiv.org/html/2601.06776v1), arXiv v1 | Method; Dataset; Ablation Study, Table 3 |

These are methodological references, not imported training examples. Any later reuse of their datasets, source descriptions or code needs the license of the exact material checked separately.

## What the papers establish—and what they do not

**ETH:** structured text extraction precedes simulation. The expert comparison concerns topology, not proof of optimal engineering. Simulation may simplify models or leave recycles open; those changes are recorded. In the phenol-to-aniline example, the property model misses a described azeotrope. This supports explicit fidelity tracking and targeted investigation of contradictions, not routine repetition of all thermo validation.

**BASF:** engineering design and simulator-language implementation receive different context. Unit-by-unit execution preserves successful solutions; column initialization and recycle closure have conditional recipes. Its selected demonstrations support this workflow, not universal process-design competence.

**DTU:** correct numerical extraction can coexist with unsupported interpretations, including an untested claim of an optimal feed stage. Tool-interface limitations also impede construction. Calculation correctness, interpretation quality and interface capability therefore need separate checks.

**ECUST:** requirements, topology, parameters and evaluation are separated. Its descriptions vary in completeness. Table 3 reports increasing branching from 3 to 5 raises token usage from 994.7K to 1325.6K while convergence changes from 80.3% to 80.6%. These are that study's results, not CHEPTA cost estimates. We do not adopt its tree search or weighted quality score.

## CHEPTA-Lab adaptations

The following are our proposed controls, informed by the findings above. Use existing canonical records and IDs; do not create a second corpus or store private model reasoning.

### 1. A concise engineering handoff before simulator implementation

For each shortlisted operation, assemble a reviewable view of existing evidence and decisions:

- Required stream change and the product/constraint it serves.
- Physical mechanism, applicable conditions and evidence IDs.
- Feed, outlets and connections; known specifications, unknowns and allowed assumptions.
- Candidate CHEPTA capability, remaining degrees of freedom and the result needed to accept the step.

Simulator syntax belongs in the implementation stage. One agent may perform both stages; additional permanent agents are not required. Unknown mandatory specifications trigger targeted retrieval or clarification. Existing CHEPTA thermodynamics and validation remain the default.

### 2. Preserve the original design through every execution attempt

Keep the source flowsheet, proposed design and executed configuration distinguishable. Record each added, removed or substituted unit, disconnected recycle, inferred setting or changed specification, with reason and evidence. A numerical initial guess is not a source fact.

Build and diagnose incrementally where the engine supports it. Preserve the last successful configuration and retain failed runs. Check ports, writable variables, units and specification freedom before making changes. Initialization recipes are capability-dependent.

A shortcut model may support initialization or a scoped material-balance exercise. It cannot establish rigorous energy demand, separation feasibility or performance of the original connected process. An opened recycle or relaxed purity target cannot silently turn the original task into a success.

### 3. Review conclusions independently of successful tool execution

For each consequential output claim, identify whether it is source-reported, computed, assumed or a hypothesis, and link its support. Compute derived quantities with code, preserving units and bases. Inspect every requested product specification and relevant warning.

Use “feasible among the evaluated alternatives” when that is what was demonstrated. “Optimal” requires a declared objective, constraints, comparison/search scope and appropriate qualification. Correct tool values alone cannot support such a conclusion.

### 4. Evaluate distinct capabilities and missing-information behaviour

Keep three evaluation tracks separate:

1. Reproduction of a supplied flowsheet.
2. Extraction of a flowsheet from a source description.
3. Engineering selection for a new feed/specification.

Score source fidelity, physical justification, executable configuration, achieved specifications and unsupported claims separately. Engineering selection allows defensible alternatives; exact agreement with one published topology is not the success criterion.

Add paired complete/under-specified tasks to the development set: the second omits a necessary input and tests whether the model identifies it instead of inventing it. Both variants stay in their parent family split. An optional later component-name masking experiment can probe dependence on familiar names, provided physical, reaction and hazard information remains sufficient and tool responses do not reveal the mapping.

## Delivery hooks and concrete acceptance examples

| Existing packet/milestone | Added acceptance example |
|---|---|
| P01 / M0 capability audit | Identify which ports, variables, specification checks, checkpoint and recycle operations the pinned engine actually exposes; mark unsupported behaviour explicitly. |
| P02 / M1 reviewed pilot | Prepare one handoff from current records and classify its consequential claims; any absent author rationale stays unknown. |
| P03 / M2 runtime | Execute a successful step followed by a failing change; preserve the earlier artifact and return the failure/warnings without fabricating observations. |
| P05 / M3 baseline | A converged run with one unmet product requirement fails performance evaluation. An untested “optimal” claim fails interpretation review. Compare methods at declared token/tool budgets. |
| M3 development tasks | Remove a necessary specification from a complete task; test targeted clarification or a conditional response. Do not leak its reference value through context. |
| M5 connected process | Opening a required recycle or substituting a separator is visible and cannot pass the original performance contract solely because the revised model converges. |

These acceptance examples become executable checks when the relevant component is implemented. Until then, apply them in human review and mark automation pending.

## Scope discipline

Retain knowledge-led shortlisting, capacity normalization with fresh sizing when needed, and task-specific acceptance. Do not add exhaustive topology/recycle search, a new graph database, routine property revalidation, or immediate fine-tuning. Store full execution artifacts, but retrieve only necessary values, units and relevant warnings into agent context.

Next action: incorporate these criteria into P01's capability matrix, then prepare P02's first handoff and review packet. This review does not bypass the existing order of work or the full-process export block.
