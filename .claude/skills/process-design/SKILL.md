---
name: process-design
description: Use when choosing a process route or separation sequence from raw materials and objectives (product, purity, recovery, scale, constraints), when explaining why a paper chose its operations, when writing design or selection questions, or when adding what a case taught to the issues and routes register. How a senior process engineer decides, and what Lab has learned so far.
---

# Process design: from raw materials and objectives to a flowsheet

CHEPTA's end goal: given the raw materials and what is wanted, propose a flowsheet and explain it. The method is
[docs/PROCESS_DESIGN.md](../../../docs/PROCESS_DESIGN.md). Read its "Knowledge-guided design steps" and "What comes
from papers" first.

**The method:**
1. Define the feed (composition, state), the products (purity, recovery), the constraints and the capacity.
2. Identify the physical obstacle: an azeotrope, two liquids, an associating acid, a heat-sensitive product, an
   equilibrium-limited reaction, a component with no exit.
3. Shortlist the operations the mixture's behaviour allows, and say why the others are excluded.
4. Connect them so each stream meets its specification. Add recycle, recovery and waste treatment only when needed.
5. Check the shortlist by simulation (the solving-simulations skill). Compare on a common basis; report trade-offs,
   not a universal winner.

**Objectives change the answer.** The same mixture with a different purity, scale, energy price or constraint can need
a different separation. Design questions test exactly that.

**What Lab has learned:** [data/ISSUES_AND_ROUTES.md](../../../data/ISSUES_AND_ROUTES.md). One row per problem, at
the level where it occurs:
- separation rows, keyed by the mixture and its behaviour, so different reactions with similar products meet;
- reaction rows;
- plant rows.

Each row gives the route each paper used and the other routes. "Seen in" counts papers, not runs. A route counts as
usable only when a paper or a CHEPTA run shows it working; an AI's suggestion is only a lead. Every new case adds or
extends rows.

**The knowledge base: the dataset.** [dataset/records/pilot.json](../../../dataset/records/pilot.json) is one
file that links each link of the evidence chain to the next. Its structure is checked by
[dataset/schemas/corpus.schema.json](../../../dataset/schemas/corpus.schema.json).

| Record | One row is | Today (2026-11-20) |
|---|---|---|
| `blocks` | a source passage, with its locator | 7 |
| `evidence` | a claim with its conditions, quantities and limits | 9 |
| `decisions` | **obstacle → mechanism → operation → expected change**, with alternatives, limits and what must be verified: the design knowledge itself | 3 |
| `runs` | an actual CHEPTA request and answer | 1 |
| `tasks` | a question with its checked answer, for testing an assistant | 3 drafts |

All of it is still from October and covers ethyl acetate extraction and the ethanol reactor. The closed ethyl acetate
and methanol plants have **not** been added yet: their lessons are only in the register and the case READMEs. Every
new case should add its decisions, evidence and runs here, each linked to its register row.

**Steps to add as the knowledge base grows** (not built yet; do not pretend they exist):
6. Find analogous cases: decisions whose obstacle and mixture behaviour match the new feed and objective.
7. Reuse what worked, and what failed, under comparable conditions. Flag where the conditions differ.
8. Rank the shortlist on a common basis once costs exist (CHEPTA 0.7).
9. (Room for further steps.)

**Label each rationale:** author-stated, independently supported, simulation-tested, or unresolved. Never invent an
author's reason.

**Open only when needed:**

| For | Go to |
|---|---|
| A worked example: why each ethyl acetate operation was chosen | [dataset/drafts/ethyl-acetate-extraction/OPERATION_REASONING.md](../../../dataset/drafts/ethyl-acetate-extraction/OPERATION_REASONING.md) |
| Comparing routes fairly (common basis, fixed and adjustable variables) | [docs/reference/PROJECT_PLAN.md](../../../docs/reference/PROJECT_PLAN.md), "Refinements" |
| Lessons from AI process-design papers (handoff, evaluation) | [docs/reference/RELATED_WORK_METHODS.md](../../../docs/reference/RELATED_WORK_METHODS.md) |
| Which property method for which mixture | CHEPTA's [METHOD_SELECTION.md](https://github.com/FaireDose/CHEPTA/blob/v0.6.2/docs/METHOD_SELECTION.md) at the pinned tag |

For a new route, work from the overall material balance through reactor/recycle, separation and heat recovery. Use the [separation screening table](../../../docs/PROCESS_DESIGN.md#screen-a-separation) to choose the first calculation that could rule out each route. Hand [solving-simulations](../solving-simulations/SKILL.md) the chosen boundary, a common comparison basis, the adjustable variables and explicit pass criteria. If a missing property could reverse the shortlist, name that property and the evidence needed to resolve it.
