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

**The knowledge base: read the index, then query** ([proposal 0003](../../../docs/proposals/0003-knowledge-base.md)).
Never read the record files whole. In this order:
1. `dataset/index/problems.md` (one line per register problem: operations, behaviours, worked/failed/lead/untested,
   disputes, papers, files), or only the matching lines: `python scripts/kb.py problems --behaviour two-liquid-phases`.
2. `python scripts/kb.py query --problem <id>` (or `--behaviour`, `--components ethanol,water`, `--operation`,
   `--status worked`): compact rows with ids, conditions and source locators.
3. `python scripts/kb.py show <row id>` for one row in full. Open `dataset/records/<case>.json` only to edit your own case.

Rows come in three kinds: `case-decision` (what a Lab case tried), `design-rule` (a book's or review's rule or worked
example, basis `textbook`; a lead unless it has its own results) and `simulation-rule` (keyed by operation and
symptom; see solving-simulations). Terms are controlled: `python scripts/kb.py terms`. Reuse what worked and what failed under comparable conditions, and
say where the conditions differ. A disputed row (`kb.py disputes`) is a disagreement to report, not to settle.

**Adding what a case taught:** in `dataset/records/<case>.json` (ids start with `<case>.`), one decision row per
operation tried, with `keys`: register `problem_id`, level, operation type, CHEPTA component names, behaviours,
conditions, optional objective (numbers only from an evidence row) and outcome (status, basis, run ids, engine). A
later CHEPTA version adds a row, never edits one; a wrong locked row is corrected by a new row with `keys.corrects`
and `keys.correction_reason` (proposal 0003, section F). When a plant is done, write its
lessons: rows with `keys.summarises` and plain fields, judged on a named specification (section G). When a row from the knowledge base shaped your choice, record it
in your own row's `keys.informed_by` (row, helped yes/no/partly, note); the index counts these, and that is how the
maintainer judges whether book knowledge helps. A rule from a book or review is a short paraphrase (2 sentences at
most, never copied text) with its catalogued source and locator. Then `python scripts/kb.py index` and the checks.

**Steps still to build** (do not pretend they exist): rank the shortlist on a common basis once costs exist
(CHEPTA 0.7). The ethyl acetate and methanol plants are backfilled as draft rows (2026-11-20), not yet reviewed.

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
