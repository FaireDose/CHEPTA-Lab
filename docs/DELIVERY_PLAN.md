# CHEPTA-Lab delivery plan

Version 1, 2026-10-30. This is the controlling milestone plan; PROJECT_PLAN.md supplies the engineering principles and history. The owner requested a multidisciplinary plan with high performance and controlled token consumption. Three focused agent reviews covered engineering, AI research and software delivery. Agent review is not human engineering approval.

## 1. Finished means a bounded, reproducible release

CHEPTA-Lab v1 should be a literature-grounded engineering assistant for explicitly selected process families. Given feed state, product specifications and constraints, it explains the obstacle, proposes defensible operations, uses applicable CHEPTA calculations, checks results and identifies missing information. It must distinguish measured, published-simulation, assumed and calculated values.

Deliverables:
- A reviewed, versioned dataset with source attribution, conditions, units, alternatives and family-level splits.
- An executable evaluation harness with separately reported evidence, engineering and tool-use results.
- A thin connection to a pinned CHEPTA engine and a demonstration with actual calculations.
- At least two reproducible numerical cases and one connected reaction–separation example using supported physical models. Numerical reproduction and physical validation must be labeled separately.
- A base-model benchmark and one bounded adaptation study if the evidence justifies training. Publish the adapter only if it earns its place; an honest negative result remains a research deliverable.
- Reproduction instructions, dataset/model documentation, cost measurements and known failure cases.

Success is not competence on any possible flowsheet. Novel-process transfer remains an explicitly tested research claim. Generic profitability rankings, autonomous plant approval, training a foundation model from scratch and routine thermodynamic revalidation are outside v1.

A dataset/benchmark preview can ship earlier. If necessary separation units or engineering review are missing, label that deliverable a preview; do not declare the full v1 complete.

## 2. Starting position

At repository commit c6a7af65d4e1b1202ae0256d82d3e4fddc9d4818:
- Research catalogue: eight source entries and six candidate families; not all sources are suitable for redistribution or complete simulation.
- Canonical pilot: seven source blocks, nine evidence claims, three engineering decisions, three draft tasks and one reconstructed historical call/result record.
- Existing ethanol work: six executed numerical runs, with source-unit and physical-validation limitations.
- Schemas, draft/release gates and deterministic export exist. Twenty software tests passed in the preceding implementation.
- Zero accepted training tasks. No model trained, live assistant runtime, frozen evaluation, or demonstrated full reaction–separation workflow.

Keep four statuses separate in reports: software checks, source verification, engineering review and model evaluation.

## 3. Milestones and completion criteria

Numeric corpus targets below are proposed planning ranges, not evidence that a particular sample size guarantees model competence. Adjust them after the pilot, before opening the final test set.

| Milestone | Concrete deliverable | Exit criterion | Lead and dependency |
|---|---|---|---|
| M0 — Scope and acceptance | Select initial families; current CHEPTA capability matrix; task rubric; prioritized blocker register | Every v1 claim maps to evidence, required tools, acceptance checks and an owner. Mark explanations, numerical benchmarks and physical-performance claims separately. | Coordinator + engineering; first |
| M1 — Trustworthy pilot | About 20 reviewed tasks from 4–6 independent cases; source/evidence packets and explicit exclusions | Reviewers can reproduce attribution and transformations; every released task meets its scope-specific gate. Resolve or narrow ethanol claims around unit conventions. Preserve failures. | Literature + engineering; M0 |
| M2 — Real tool integration | Thin pinned-engine adapter, recorded calls/results, limits and failure handling | At least two supported numerical cases run reproducibly through the same interface available to the assistant. Hashes, version, warnings and comparisons retained. An unsupported unit yields an explicit limitation. | Software; M0; parallel with M1 |
| M3 — Frozen evaluation and baseline | Family-grouped development/test manifests; reproducible scoring; base model with evidence and tools | Same conditions can be rerun. Record errors by cause and actual usage. Test supplied-evidence reasoning separately from retrieval/tool performance. Freeze test material before training variants are generated. | AI research + engineering; M1 and M2 |
| M4 — Targeted corpus expansion | Roughly 100–200 reviewed training tasks; coverage inventory; common-basis comparisons | Collection addresses measured baseline weaknesses. Aim for 12–20 independent cases over 4–6 families, including held-out material, where sources permit. No row-level split of related papers or variants. | Literature + engineering; M3 |
| M5 — Connected process demonstration | One reaction–separation flowsheet and complete process acceptance contract | Real supported units; component/element balances, appropriate energy accounting, all purity/impurity/recovery constraints, utility feasibility, recycle behavior if present, and sensitivity assessed. References and tolerances stated before comparison. | CHEPTA integration + engineering; M2 and required upstream units |
| M6 — Controlled adaptation decision | One small supervised adaptation study, only for learnable failures | Compare base and adapted model under identical evidence/tool access and inference budgets. Choose on development data; evaluate final test after settings are locked. Keep the stronger system. | AI research; M3 and M4 |
| M7 — Release and demonstration | Versioned GitHub release, dataset card, reproducible demo, evaluation/failure report, optional adapter | Another person can reproduce the documented examples. Rights/review complete. V1 capability claims match results and M5 is complete. External publication follows the owner's release decision. | Coordinator; M5 plus evaluation outcome |

A “case” is a distinct physical problem with a supported basis, not a paraphrased question. Related cases can still belong to one dependent source cluster. Report cases, source clusters, families and task rows separately.

M3 may begin with a small provisional development benchmark. Expand and freeze the final holdout manifest once coverage permits. Initial goal: 30–50 evaluation tasks on held-out material, separate from the training target. One held-out family supports only a limited transfer claim. Report raw counts and uncertainty; many questions from one paper are not independent evidence.

## 4. Dependencies and schedule

M0 leads into two concurrent streams: M1 evidence/review and M2 runtime. They converge at M3. M4 then targets observed deficiencies; M6 is conditional. M5 can progress alongside corpus work but is blocked by genuinely missing CHEPTA physics. M7 requires all claimed capabilities, not just documentation completion.

Indicative planning window: 8–12 active weeks for an evaluated research release, assuming regular working sessions, timely human review, usable literature and available required units. This is not a delivery commitment for missing simulator development. Re-estimate after M1 from measured throughput.

- Initial 1–2 weeks: scope, source review packets, first accepted tasks, thin adapter and measured work costs.
- Following 2–3 weeks: independent cases, evaluation harness and base-model measurements.
- Following 2–4 weeks: targeted collection, connected-process work and any bounded adaptation.
- Final 1–2 weeks: locked evaluation, reproduction check and release preparation.

These intervals overlap. Lack of review capacity or separation support extends the schedule; increasing the number of agents cannot remove those dependencies. If a blocker persists, deliver the explicitly narrower research preview and record the remaining v1 gate.

## 5. Engineering acceptance

For each case, define the supplied information, variable roles, objectives, constraints, source precision, expected results and allowable disagreement before execution.

Use the transferable decision structure:
state → obstacle → physical mechanism → candidate operation → expected change → limits → verification.

A published route is one supported solution, not an automatic optimum. Alternatives need a shared feed/specification/boundary basis. Explain why a choice changes with impurities, utilities, recovery objectives, uncertainty or capacity. Keep fixed inputs, adjustable variables, uncertain parameters and missing information distinct.

Retain paper flow rates for reproduction and normalized quantities for transfer. Recalculate sizing, residence time, heat-transfer limits and pressure drop when capacity changes. Do not infer mixture separability from pure-component boiling points alone.

Link to CHEPTA's existing property models, parameter provenance and validation. Investigate underlying thermo data only for a specific missing parameter, range violation or material discrepancy. Do not substitute arbitrary splits for missing separation models.

For process performance, make tolerances depend on model scope, source precision and conservation checks, rather than one universal percentage. Preserve mismatches; classify source transcription, source inconsistency, model difference, solver problem and missing specification separately.

Human review concentrates on consequential assumptions, applicability, source interpretation and final target acceptance. Agents prepare concise packets and critiques. A single human review session may cover several required review scopes; the current pipeline records each explicitly.

## 6. Evaluation and training decisions

Use comparable experiments:
A. Base model with supplied evidence.
B. Base model with the intended retrieval and CHEPTA tools.
C. Adapted model with the same retrieval, tools and resource limits as B, if training is justified.

A isolates reasoning from retrieval. B vs C tests the adaptation benefit. Fix corpus version, engine revision, tool contracts, model settings and scoring policy.

Record:
- Citation support and applicability.
- Valid operation rationale and satisfaction of stated constraints.
- Correct calls, interpretation and reporting of tool warnings.
- Numerical/specification checks where the task requires them.
- Detection of missing inputs, appropriate abstention and handling of failed calculations.
- Latency, tokens, tool calls and cost per successful task.

Define severity classes before scoring. Invented successful calculations, concealed failed specifications and unqualified unsupported-method claims are critical failures. Release requires resolving known critical failures in the declared demonstration suite; absence in a small test is not a general safety guarantee.

AI research should predeclare the primary comparison and acceptable regressions after the first baseline. Prefer paired task results and family-level summaries; report uncertainty and insufficient power rather than inventing an improvement guarantee.

If errors come from missing facts, bad retrieval or unsupported units, fix those before training. If behavior is the problem, try one adapter configuration and at most one justified development-set revision in the first study. Stop unproductive training sweeps. Never select hyperparameters using the final test results.

## 7. Team and token operating rules

The roles are responsibilities, not six permanent agents.

| Role | Work | When to use stronger reasoning |
|---|---|---|
| Coordinator/architect | Backlog, contracts, dependencies, integration and release decisions | Cross-component design or conflicting requirements |
| Literature/data worker | Screen sources, extract blocks, preserve provenance | Ambiguous units, equations, contradictory sources |
| Engineering reviewer agent | Challenge applicability, decision rationale and comparisons | Consequential physical assumptions and alternative selection |
| Software developer | Parsers, adapter, checks and evaluation runner | Substantial implementation/debugging |
| AI researcher | Benchmark, error analysis, training experiment | Experimental design and interpretation |
| Human owner/reviewer | Scope, engineering acceptance and release decision | Review the evidence packet, not every agent conversation |

Normally use one author and one targeted reviewer, with at most two independent work packets running concurrently. Use additional agents only for clearly separable tasks. Avoid a new orchestration framework; use the existing repository, small scripts and a backlog.

Each packet contains:
ID; objective; exact input files/revisions; permitted changes; deliverable; acceptance checks; dependency; resource allowance; stop condition.

Each completion report contains:
outcome; changed files; evidence; checks actually run; unresolved issues; measured usage or “unavailable”; next action.

Efficiency rules:
1. Parse a document once and cache by content hash. Preserve exact table/equation context; retrieve the relevant blocks for later work.
2. Give workers a short task packet, not the entire conversation or repository.
3. Use scripts for arithmetic, units, balances, hashes, schema validation, deduplication and repeated exports.
4. Use inexpensive processing for clear extraction; reserve stronger reasoning for ambiguous science, architecture and experimental decisions. Select actual models only after a measured comparison on our tasks.
5. Write concise evidence-linked rationales, not long speculative narratives.
6. Review deltas and disputes; do not ask every agent to reread every paper. One independent agent review does not replace human acceptance.
7. Batch source screening before expensive full-text extraction. Rank acquisition by whether it resolves a milestone blocker or a missing physical mechanism.
8. Preserve outputs and failed attempts. Reprocess only changed inputs or affected dependencies.
9. After two unsuccessful attempts at the same blocker, stop the loop and report evidence plus a different approach.
10. Limit work in progress to what can be reviewed in the next batch. Do not stockpile hundreds of unreviewed tasks.

Provisional context allowances: routine extraction packets approximately 4–8k input tokens and 1–2k output tokens; complex review up to approximately 20k input and 4k output tokens before reassessment. These are starting caps for orchestration where supported, not a reason to omit required equations, units or constraints. Provider usage may exceed context estimates; distinguish measured usage from estimates.

## 8. Resource measurement and spending

Calibrate on the first five completed packets. Record provider/model version, input/output/cache usage when available, tool calls, elapsed time, human review time, accepted/rejected results and rework.

Primary efficiency measures:
- Tokens and paid cost per accepted independent case.
- Reviewed tasks per human review hour.
- Rework/rejection rate and reason.
- Evaluation success at a fixed inference/tool budget.

Do not optimize the price per generated answer while lowering acceptance quality. Cache/retrieval savings must be measured; no percentage saving is promised.

There is no defensible total monetary estimate yet. Calculate a batch quote from measured token usage and current provider rates, plus separate GPU/runtime costs and review effort. Mark usage unavailable when tools do not expose it. Before paid training, prepare the exact configuration, maximum runtime/cost and stop rule within the owner's spending limit. This plan authorizes no purchase or background job.

Do not collect more of a saturated case type merely to meet a row target. Prefer a paper resolving a missing specification, applicable alternative or failed benchmark.

## 9. Immediate work packets

| ID | Deliverable | Done when |
|---|---|---|
| P01 | Scope/capability matrix for 3 candidate families, expandable to 4–6 after screening | Read current CHEPTA code at a pinned revision; identify supported, partial and blocked tasks without claiming model-name coverage proves applicability |
| P02 | Review packet for the 9 current evidence claims and 3 tasks | Source passages, numerical bases, inference labels, known disagreements and reviewer questions are inspectable; no automatic human approval |
| P03 | Thin runtime adapter plus one real request/response replay | Actual pinned engine executes; full warnings and failures preserved; historical replay clearly distinguished from autonomous design |
| P04 | One additional independent source/case addressing a concrete coverage gap | Accessible source, reusable material, extractable inputs and a task-specific acceptance path recorded |
| P05 | Small development evaluation and cost ledger | Existing model assessed on reviewed tasks with declared context; errors separated from runtime/data gaps; no final test tuning |

Run P01 first; P02 and P03 may then proceed independently. P04 follows the coverage decision; P05 needs reviewed task material and the runtime. These are queued work packets, not claims that those milestones are already complete.

## 10. Repository and publication

GitHub remains the working source of truth for evidence metadata, scripts, runs, reviews and decisions. Hugging Face is the distribution channel for a reviewed dataset, an optional useful adapter and a demo. Keep sensitive or non-redistributable source documents outside public releases; resolve rights for exact exported material.

Document source composition, collection methods, intended uses, limitations, evaluation splits and licenses in the dataset card. Training export needs model-specific chat-template and loss-mask verification before a run; the current intermediate JSONL alone does not establish trainer compatibility.

Primary implementation references checked on 2026-10-30:
- [Hugging Face dataset cards](https://huggingface.co/docs/hub/datasets-cards)
- [Hugging Face TRL SFT trainer](https://huggingface.co/docs/trl/sft_trainer)

Publication value should come from the checked engineering cases, reproducible results and candid error analysis. Training a model is one experiment within that deliverable, not proof of engineering competence.

## 11. Research-informed acceptance refinements

[The four-paper methods review](RELATED_WORK_METHODS.md) adds concrete checks to P01–P05 and M5 without adding milestones. Require an engineering handoff before simulator implementation; preserve original versus modified configurations; evaluate conclusions independently of numerical execution; and distinguish reproduction, extraction and new-design tasks.

These are adopted requirements, not implemented runtime features. Full-process export remains blocked. P01 must establish which capabilities exist before P03 implements engine-dependent initialization or checkpoint behaviour. M3 includes a missing-specification task pair and an unsupported-optimality check. M5 must reject a claimed success obtained only by silently opening a required recycle, relaxing a target or replacing a rigorous separator with a prescribed split.
