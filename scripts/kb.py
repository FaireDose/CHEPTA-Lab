#!/usr/bin/env python3
"""The knowledge base for process design (docs/proposals/0003-knowledge-base.md).

Read the index first (dataset/index/problems.md), then query; open a record file only for one row.

  python scripts/kb.py problems --behaviour azeotrope-min-boiling   only the index lines that match
  python scripts/kb.py query --behaviour azeotrope-min-boiling --components ethanol,water --status worked
  python scripts/kb.py query --operation distillation --symptom no-convergence   simulation knowledge
  python scripts/kb.py show <row id>        one row in full, with its locators and where it was used
  python scripts/kb.py terms                the controlled vocabulary
  python scripts/kb.py disputes             rows that disagree under the same conditions
  python scripts/kb.py index                regenerate dataset/index/ after changing records
  python scripts/kb.py check                keys, rights, conflicts, append-only lock, index up to date

Held-out (test split) groups never appear in the index or in any output of this script.
No model calls, no CHEPTA runs, no downloads.
"""
import argparse
import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("dataset_pipeline", ROOT / "scripts/dataset_pipeline.py")
pipeline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(pipeline)

REGISTER = ROOT / "data/ISSUES_AND_ROUTES.md"
SOURCES = ROOT / "data/sources.json"
INDEX_MD = ROOT / "dataset/index/problems.md"
INDEX_JSON = ROOT / "dataset/index/problems.json"
LOCK = ROOT / "dataset/index/outcomes.lock.json"
STATUSES_SHOWN = ("worked", "failed", "lead", "untested")
RULE_KINDS = ("design-rule", "simulation-rule")
RESULTS_DIR = re.compile(r"^results-chepta-([0-9]+\.[0-9]+\.[0-9]+)$")
QUOTED = re.compile(r"[\"“”«»]([^\"“”«»]+)[\"“”«»]")


# ---------- reading ----------

def vocabulary(path=pipeline.VOCABULARY):
    return pipeline.read_json(path)


def sources_catalogue(path=SOURCES):
    return {s["id"]: s for s in pipeline.read_json(path)["sources"]}


def register_rows(path=REGISTER):
    """{problem id: level} from the first two columns of the register's table."""
    rows, in_table = {}, False
    for line in Path(path).read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else None
        if not cells:
            in_table = False
            continue
        if cells[0] == "id":
            in_table = True
        elif in_table and not set(cells[0]) <= {"-", ":", " "}:
            rows[cells[0]] = cells[1]
    return rows


def engine_version(engine):
    m = re.fullmatch(r"chepta@([0-9]+)\.([0-9]+)\.([0-9]+)", engine or "")
    return tuple(int(x) for x in m.groups()) if m else None


def want(value):
    return [x.strip() for x in value.split(",") if x.strip()] if value else []


# ---------- groups and held-out rows ----------

def row_groups(row, kind, ix):
    """Groups a decision or evidence row belongs to: those holding its sources (evidence passages, rule source)."""
    evidence = [ix["evidence"][k] for k in row["evidence_ids"] if k in ix["evidence"]] if kind == "decisions" else [row]
    sources = {ix["blocks"][b]["source_id"] for e in evidence for b in e["block_ids"] if b in ix["blocks"]}
    if kind == "decisions" and row["keys"].get("source"):
        sources.add(row["keys"]["source"]["source_id"])
    return {g["id"] for g in ix["groups"].values() if sources & set(g["source_ids"])}, sources


def held_out(corpus):
    """Ids of decision and evidence rows that touch a test-split group: never shown to sessions."""
    ix = pipeline.indexes(corpus)
    test = {g["id"] for g in corpus["groups"] if g["split"] == "test"}
    hidden = set()
    for kind in ("evidence", "decisions"):
        for row in corpus[kind]:
            if row_groups(row, kind, ix)[0] & test:
                hidden.add(row["id"])
    return hidden


def visible_decisions(corpus):
    hidden = held_out(corpus)
    return [d for d in corpus["decisions"] if d["id"] not in hidden], hidden


def used_in(rows, origins):
    """Where each row was used: derived from the informed_by lists of the rows it informed."""
    uses = {}
    for d in rows:
        for entry in d["keys"].get("informed_by", []):
            uses.setdefault(entry["row"], []).append({"case": origins.get(d["id"], "?"), "row": d["id"],
                                                      "helped": entry["helped"], "note": entry["note"]})
    return uses


# ---------- conflicts ----------

def current_rows(rows):
    """Within one situation: every non-CHEPTA row, and the CHEPTA rows of the latest released engine
    (a later version adds a row and supersedes, it never overwrites)."""
    chepta = [r for r in rows if r["keys"]["outcome"]["basis"] == "chepta_run"]
    released = [engine_version(r["keys"]["outcome"]["engine"]) for r in chepta]
    latest = max((v for v in released if v), default=None)
    keep = [r for r in chepta if (engine_version(r["keys"]["outcome"]["engine"]) == latest)] if latest else chepta
    return [r for r in rows if r["keys"]["outcome"]["basis"] != "chepta_run"] + keep


def situation(d):
    k = d["keys"]
    return (k.get("problem_id", "-"), k.get("symptom", "-"), k["operation_type"], tuple(sorted(k["conditions"])))


def condition_sets(decisions):
    sets = {}
    for d in decisions:
        sets.setdefault(situation(d), []).append(d)
    return sets


def acknowledged(a, b):
    return b["id"] in a["keys"].get("disputed_with", []) or a["id"] in b["keys"].get("disputed_with", [])


def dispute_entry(key, rows, open_pairs, ack_pairs):
    return {"problem_id": key[0], "symptom": key[1], "operation_type": key[2], "conditions": list(key[3]),
            "rows": [{"id": r["id"], "status": r["keys"]["outcome"]["status"],
                      "basis": r["keys"]["outcome"]["basis"], "engine": r["keys"]["outcome"]["engine"]}
                     for r in sorted(rows, key=lambda r: r["id"])],
            "unacknowledged_pairs": open_pairs, "acknowledged_pairs": ack_pairs}


def disputes(decisions):
    """Disputed sets. A set of rows sharing problem (or symptom), operation and conditions is disputed when one says
    worked and another failed, or when two of its rows name each other in disputed_with (whatever their status,
    leads included). Acknowledged pairs whose rows sit in different sets form their own entry, keyed by the first row."""
    found, placed = [], set()
    for key, rows in sorted(condition_sets(decisions).items()):
        cur = sorted(current_rows(rows), key=lambda r: r["id"])
        worked = [r for r in cur if r["keys"]["outcome"]["status"] == "worked"]
        failed = [r for r in cur if r["keys"]["outcome"]["status"] == "failed"]
        open_pairs = [(a["id"], b["id"]) for a in worked for b in failed if not acknowledged(a, b)]
        ack_pairs = [(a["id"], b["id"]) for i, a in enumerate(cur) for b in cur[i + 1:] if acknowledged(a, b)]
        placed.update(ack_pairs)
        if (worked and failed) or ack_pairs:
            found.append(dispute_entry(key, cur, open_pairs, ack_pairs))
    current = {r["id"]: r for rows in condition_sets(decisions).values() for r in current_rows(rows)}
    for a in sorted(current.values(), key=lambda r: r["id"]):
        for other in a["keys"].get("disputed_with", []):
            b = current.get(other)
            if b is None:
                continue
            pair = tuple(sorted((a["id"], b["id"])))
            if pair not in placed:
                placed.add(pair)
                found.append(dispute_entry(situation(current[pair[0]]), [current[pair[0]], current[pair[1]]], [],
                                           [pair]))
    return found


# ---------- checks ----------

def statement_errors(where, text, limits):
    """A rule's statement is Lab's short paraphrase, never copied text."""
    errors = []
    sentences = [s for s in re.split(r"[.!?](?:\s+|$)", text.strip()) if s.strip()]
    if len(text) > limits["max_characters"] or len(sentences) > limits["max_sentences"]:
        errors.append(f"{where}: statement longer than {limits['max_sentences']} sentences or "
                      f"{limits['max_characters']} characters; paraphrase it shortly and cite the locator")
    for quoted in QUOTED.findall(text):
        if len(quoted.split()) > limits["max_quoted_words"]:
            errors.append(f"{where}: statement quotes more than {limits['max_quoted_words']} words; "
                          "paraphrase instead of copying")
    return errors


def check_keys(corpus, vocab=None, register=None, sources=None, root=ROOT):
    vocab = vocab or vocabulary()
    register = register if register is not None else register_rows()
    sources = sources if sources is not None else sources_catalogue()
    ix = pipeline.indexes(corpus)
    names = set(vocab["components"]["names"])
    errors = []
    for problem, level in register.items():
        if level not in vocab["levels"]:
            errors.append(f"register row {problem}: level '{level}' is not in data/vocabulary.json")

    def terms(where, values, allowed, what):
        for v in values:
            if v not in allowed:
                errors.append(f"{where}: unknown {what} '{v}' (data/vocabulary.json; adding a term is a deliberate edit)")

    for d in corpus["decisions"]:
        k, where = d["keys"], d["id"]
        o, kind = k["outcome"], k["kind"]
        terms(where, [kind], vocab["row_kinds"], "row kind")
        terms(where, [k["operation_type"]], vocab["operation_types"], "operation type")
        terms(where, k["behaviours"], vocab["behaviours"], "behaviour")
        terms(where, k["components"], names, "component")
        terms(where, [o["status"]], vocab["outcome_statuses"], "outcome status")
        terms(where, [o["basis"]], vocab["outcome_bases"], "outcome basis")
        if "symptom" in k:
            terms(where, [k["symptom"]], vocab["symptoms"]["terms"], "symptom")
        # What each kind is keyed by.
        if kind == "case-decision":
            for field in ("problem_id", "level"):
                if field not in k:
                    errors.append(f"{where}: a case decision names its register {field}")
            if not d["evidence_ids"] or not k["components"]:
                errors.append(f"{where}: a case decision cites evidence and names its components")
            if o["basis"] == "textbook":
                errors.append(f"{where}: a case decision is not a textbook rule; use kind design-rule or simulation-rule")
        elif kind in RULE_KINDS:
            if o["basis"] != "textbook":
                errors.append(f"{where}: a rule row has basis textbook")
            if "source" not in k or "statement" not in k:
                errors.append(f"{where}: a rule row has a source (catalogue id and locator) and a short statement")
            if kind == "simulation-rule":
                if "symptom" not in k:
                    errors.append(f"{where}: a simulation rule is keyed by operation and symptom")
                if "problem_id" in k or "level" in k:
                    errors.append(f"{where}: a simulation rule does not belong to a register problem")
            elif not k["behaviours"] and "problem_id" not in k:
                errors.append(f"{where}: a design rule names the behaviours (or the register problem) it applies to")
        if "problem_id" in k:
            if k["problem_id"] not in register:
                errors.append(f"{where}: problem_id {k['problem_id']} is not a row of data/ISSUES_AND_ROUTES.md")
            elif register[k["problem_id"]] != k.get("level"):
                errors.append(f"{where}: level {k.get('level')} differs from the register's {register[k['problem_id']]}")
        if "level" in k:
            terms(where, [k["level"]], vocab["levels"], "level")
        # Sources and rights: every rule cites a catalogued source; a statement is a short paraphrase.
        if "source" in k:
            src = sources.get(k["source"]["source_id"])
            if src is None or not src.get("rights_status"):
                errors.append(f"{where}: source {k['source']['source_id']} must be in data/sources.json with its "
                              "rights status")
        if "statement" in k:
            if "source" not in k:
                errors.append(f"{where}: a statement needs its source and locator")
            errors.extend(statement_errors(where, k["statement"], vocab["statement_limits"]))
        # Outcome rules.
        if o["basis"] == "chepta_run":
            if not o["engine"] or not o["run_ids"]:
                errors.append(f"{where}: an outcome from a CHEPTA run names its engine and its run_ids")
        elif o["engine"] is not None:
            errors.append(f"{where}: engine is only for outcomes from a CHEPTA run")
        if o["status"] in ("worked", "failed") and o["basis"] == "lab_inference":
            errors.append(f"{where}: a Lab inference can only be untested or a lead")
        if o["status"] in ("worked", "failed") and o["basis"] == "textbook" and not d["evidence_ids"]:
            errors.append(f"{where}: a textbook rule without results of its own is a lead; a worked example "
                          "that worked or failed cites the evidence row holding its numbers")
        if o["status"] in ("untested", "lead") and (o["run_ids"] or o["basis"] == "chepta_run"):
            errors.append(f"{where}: an untested row or a lead has no runs")
        for run in o["run_ids"]:
            if "/" not in run:
                if run not in ix["runs"]:
                    errors.append(f"{where}: unknown corpus run {run}")
                continue
            parts = Path(run).parts
            if parts[0] != "cases" or ".." in parts or not (root / (run + ".output.json")).is_file():
                errors.append(f"{where}: run {run} needs cases/<case>/<results folder>/<run>.output.json")
            for part in parts:
                m = RESULTS_DIR.match(part)
                if m and o["engine"] != f"chepta@{m.group(1)}":
                    errors.append(f"{where}: run {run} is in a chepta {m.group(1)} folder but engine is {o['engine']}")
        objective = k.get("objective")
        if objective:
            terms(where, [objective["product"]], names, "component")
            for t in objective.get("targets", []):
                ev = ix["evidence"].get(t["evidence_id"])
                if ev is None:
                    errors.append(f"{where}: objective cites unknown evidence {t['evidence_id']}")
                elif t["evidence_id"] not in d["evidence_ids"]:
                    errors.append(f"{where}: objective evidence {t['evidence_id']} is not in the row's evidence_ids")
                elif not any(q["value"] == t["value"] and q["unit"] == t["unit"] for q in ev["quantities"]):
                    errors.append(f"{where}: objective {t['name']} {t['value']} {t['unit']} is not a quantity of "
                                  f"{t['evidence_id']} (no number without a source)")
        for other in k.get("disputed_with", []):
            if other not in ix["decisions"] or other == d["id"]:
                errors.append(f"{where}: disputed_with names unknown row {other}")
        for entry in k.get("informed_by", []):
            if entry["row"] not in ix["decisions"] or entry["row"] == d["id"]:
                errors.append(f"{where}: informed_by names unknown row {entry['row']}")
    for e in corpus["evidence"]:
        k = e.get("keys")
        if not k:
            continue
        for p in k["problem_ids"]:
            if p not in register:
                errors.append(f"{e['id']}: problem_id {p} is not a row of data/ISSUES_AND_ROUTES.md")
        terms(e["id"], k.get("components", []), names, "component")
        terms(e["id"], k.get("behaviours", []), vocab["behaviours"], "behaviour")
    for found in disputes(corpus["decisions"]):
        for a, b in found["unacknowledged_pairs"]:
            where = found["problem_id"] if found["problem_id"] != "-" else f"symptom {found['symptom']}"
            errors.append(f"disputed: {a} (worked) and {b} (failed) share {where}, operation "
                          f"{found['operation_type']} and conditions {found['conditions']}. Name the condition that "
                          "differs, or record the disagreement in keys.disputed_with of your own row. "
                          "Never merge or delete either row.")
    return errors


def lock_entries(corpus):
    """Append-only parts (held-out rows left out): outcomes from CHEPTA runs, and every informed_by list."""
    rows, _ = visible_decisions(corpus)
    rows = sorted(rows, key=lambda d: d["id"])
    return {"outcomes": {d["id"]: copy.deepcopy(d["keys"]["outcome"]) for d in rows
                         if d["keys"]["outcome"]["basis"] == "chepta_run"},
            "informed_by": {d["id"]: copy.deepcopy(d["keys"]["informed_by"]) for d in rows
                            if d["keys"].get("informed_by")}}


def lock_errors(corpus, lock):
    errors, now = [], lock_entries(corpus)
    hidden = held_out(corpus)
    for key, outcome in lock.get("outcomes", {}).items():
        if key in hidden:
            continue
        if key not in now["outcomes"]:
            errors.append(f"{key}: an outcome from a CHEPTA run was deleted; rows are never deleted "
                          "(dataset/index/outcomes.lock.json)")
        elif now["outcomes"][key] != outcome:
            errors.append(f"{key}: an outcome from a CHEPTA run was edited; add a new row (for a new engine version, "
                          "new runs or a correction) instead of overwriting it")
    for key, entries in lock.get("informed_by", {}).items():
        if key in hidden:
            continue
        if now["informed_by"].get(key, [])[:len(entries)] != entries:
            errors.append(f"{key}: an informed_by entry was edited or deleted; the list is append-only")
    return errors


# ---------- index ----------

def summary(rows, current, uses, ix, origins):
    papers, files = set(), set()
    for d in rows:
        papers |= row_groups(d, "decisions", ix)[1]
        files.add(origins.get(d["id"], "?"))
    used = [u for d in rows for u in uses.get(d["id"], [])]
    return {"rows": len(rows),
            "counts": {s: sum(1 for d in rows if d["id"] in current and d["keys"]["outcome"]["status"] == s)
                       for s in STATUSES_SHOWN},
            "superseded": sum(1 for d in rows if d["id"] not in current),
            "papers": len(papers), "files": sorted(files),
            "used": {h: sum(1 for u in used if u["helped"] == h) for h in ("yes", "partly", "no")}}


def build_index(corpus, origins, register=None):
    register = register if register is not None else register_rows()
    ix = pipeline.indexes(corpus)
    rows, hidden = visible_decisions(corpus)
    current = {r["id"] for group in condition_sets(rows).values() for r in current_rows(group)}
    uses = used_in(rows, origins)
    found = disputes(rows)
    problems = []
    for problem, level in register.items():
        mine = [d for d in rows if d["keys"].get("problem_id") == problem]
        keyed_evidence = [e for e in corpus["evidence"] if e["id"] not in hidden
                          and problem in e.get("keys", {}).get("problem_ids", [])]
        s = summary(mine, current, uses, ix, origins)
        for e in keyed_evidence:
            s["files"] = sorted(set(s["files"]) | {origins.get(e["id"], "?")})
        s["papers"] = len({src for d in mine for src in row_groups(d, "decisions", ix)[1]}
                          | {src for e in keyed_evidence for src in row_groups(e, "evidence", ix)[1]})
        problems.append({"id": problem, "level": level,
                         "operations": sorted({d["keys"]["operation_type"] for d in mine}),
                         "behaviours": sorted({b for d in mine for b in d["keys"]["behaviours"]}
                                              | {b for e in keyed_evidence for b in e["keys"].get("behaviours", [])}),
                         "components": sorted({c for d in mine for c in d["keys"]["components"]}
                                              | {c for e in keyed_evidence for c in e["keys"].get("components", [])}),
                         "disputed": sum(1 for f in found if f["problem_id"] == problem), **s})
    pairs = {}
    for d in rows:
        if "symptom" in d["keys"]:
            pairs.setdefault((d["keys"]["operation_type"], d["keys"]["symptom"]), []).append(d)
    simulation = [{"operation": op, "symptom": sym,
                   "disputed": sum(1 for f in found if f["operation_type"] == op and f["symptom"] == sym),
                   **summary(group, current, uses, ix, origins)} for (op, sym), group in sorted(pairs.items())]
    general = {}
    for d in rows:
        if d["keys"]["kind"] == "design-rule" and "problem_id" not in d["keys"]:
            general.setdefault(d["keys"]["operation_type"], []).append(d)
    design = [{"operation": op, "behaviours": sorted({b for d in group for b in d["keys"]["behaviours"]}),
               "disputed": sum(1 for f in found if f["operation_type"] == op and f["problem_id"] == "-"
                               and f["symptom"] == "-"),
               **summary(group, current, uses, ix, origins)} for op, group in sorted(general.items())]
    data = {"about": "Generated by python scripts/kb.py index from dataset/records/ and data/ISSUES_AND_ROUTES.md. "
                     "Do not edit. Held-out groups are left out.",
            "problems": problems, "simulation": simulation, "general_design_rules": design}

    def counts(p):
        c, u = p["counts"], p["used"]
        return f"{c['worked']}/{c['failed']}/{c['lead']}/{c['untested']}", f"{u['yes']}/{u['partly']}/{u['no']}"

    lines = ["# Knowledge-base index (generated; do not edit)", "",
             "Made by `python scripts/kb.py index` from dataset/records/ and data/ISSUES_AND_ROUTES.md; held-out "
             "groups left out. Next: `python scripts/kb.py query` with `--problem`, `--behaviour`, `--components`, "
             "`--operation`, `--symptom`, `--kind` or `--status`, then `python scripts/kb.py show <row id>`. "
             "Terms: `python scripts/kb.py terms`.", "",
             "W/F/L/U: rows worked / failed / lead / untested (for CHEPTA runs, the latest engine per condition). "
             "D: disputed sets (worked against failed, or rows naming each other in disputed_with). P: sources (papers, books). Used y/p/n: later cases it helped / partly / not. "
             "Files: dataset/records/<file>.json.", "",
             "## Design: one line per register problem", "",
             "| problem | level | operations | behaviours | W/F/L/U | D | P | used y/p/n | files |",
             "|---|---|---|---|---|---|---|---|---|"]
    for p in problems:
        wflu, used = counts(p)
        lines.append(f"| {p['id']} | {p['level']} | {','.join(p['operations']) or '-'} | "
                     f"{','.join(p['behaviours']) or '-'} | {wflu} | {p['disputed']} | {p['papers']} | {used} | "
                     f"{','.join(p['files']) or '-'} |")
    lines += ["", "## Simulation: one line per operation and symptom", "",
              "| operation | symptom | W/F/L/U | D | P | used y/p/n | files |", "|---|---|---|---|---|---|---|"]
    for p in simulation:
        wflu, used = counts(p)
        lines.append(f"| {p['operation']} | {p['symptom']} | {wflu} | {p['disputed']} | {p['papers']} | {used} | "
                     f"{','.join(p['files'])} |")
    lines += ["", "## General design rules: one line per operation", "",
              "| operation | behaviours | W/F/L/U | D | P | used y/p/n | files |", "|---|---|---|---|---|---|---|"]
    if not design:
        lines.append("| (none yet) | - | - | - | - | - | - |")
    for p in design:
        wflu, used = counts(p)
        lines.append(f"| {p['operation']} | {','.join(p['behaviours']) or '-'} | {wflu} | {p['disputed']} | {p['papers']} | {used} | "
                     f"{','.join(p['files'])} |")
    return "\n".join(lines) + "\n", json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def read_lock():
    return pipeline.read_json(LOCK) if LOCK.is_file() else {"outcomes": {}, "informed_by": {}}


def index_errors(corpus, origins):
    md, js = build_index(corpus, origins)
    stale = [path for path, text in ((INDEX_MD, md), (INDEX_JSON, js))
             if not path.is_file() or path.read_text() != text]
    errors = [f"{p.relative_to(ROOT)} is stale: run python scripts/kb.py index" for p in stale]
    lock, now = read_lock(), lock_entries(corpus)
    missing = [k for k in now["outcomes"] if k not in lock.get("outcomes", {})]
    missing += [k for k, v in now["informed_by"].items() if lock.get("informed_by", {}).get(k) != v]
    if missing:
        errors.append(f"outcome lock misses {', '.join(sorted(set(missing)))}: run python scripts/kb.py index")
    return errors + lock_errors(corpus, lock)


def check_all(corpus, origins):
    errors = check_keys(corpus)
    if not errors:
        errors = index_errors(corpus, origins)
    rows, _ = visible_decisions(corpus)
    kinds = {}
    for d in rows:
        kinds[d["keys"]["kind"]] = kinds.get(d["keys"]["kind"], 0) + 1
    return errors, {"rows_by_kind": kinds, "disputed_sets": len(disputes(rows)),
                    "index": "current" if not errors else "see errors"}


def write_index(corpus, origins):
    lock = read_lock()
    errors = lock_errors(corpus, lock)
    if errors:
        raise ValueError("\n".join(errors))
    now = lock_entries(corpus)
    outcomes = dict(lock.get("outcomes", {}))
    outcomes.update({k: v for k, v in now["outcomes"].items() if k not in outcomes})
    informed = dict(lock.get("informed_by", {}))
    informed.update(now["informed_by"])  # lock_errors has checked that the old entries are a prefix
    lock = {"about": "Append-only parts of the records, written by python scripts/kb.py index: outcomes from CHEPTA "
                     "runs and informed_by lists. Editing or deleting one in dataset/records/ fails the checks: add a "
                     "new row or entry instead. Changing this file by hand is a deliberate correction; say why in the "
                     "commit.",
            "outcomes": dict(sorted(outcomes.items())), "informed_by": dict(sorted(informed.items()))}
    md, js = build_index(corpus, origins)
    INDEX_MD.parent.mkdir(parents=True, exist_ok=True)
    INDEX_MD.write_text(md)
    INDEX_JSON.write_text(js)
    LOCK.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")


# ---------- query ----------

def matches(d, args):
    k = d["keys"]
    return ((not args.problem or k.get("problem_id") == args.problem)
            and (not args.level or k.get("level") == args.level)
            and (not args.kind or k["kind"] in want(args.kind))
            and (not args.operation or k["operation_type"] in want(args.operation))
            and (not args.symptom or k.get("symptom") in want(args.symptom))
            and (not args.status or k["outcome"]["status"] in want(args.status))
            and (not args.basis or k["outcome"]["basis"] in want(args.basis))
            and all(b in k["behaviours"] for b in want(args.behaviour))
            and all(c in k["components"] for c in want(args.components)))


def locators(d, ix):
    out = []
    if d["keys"].get("source"):
        out.append(f"{d['keys']['source']['source_id']}: {d['keys']['source']['locator']}")
    for key in d["evidence_ids"]:
        e = ix["evidence"].get(key)
        for b in (e["block_ids"] if e else []):
            block = ix["blocks"].get(b)
            if block:
                out.append(f"{block['source_id']}: {block['locator']}")
    return sorted(set(out))


def compact(d, ix, origins, uses):
    k, o = d["keys"], d["keys"]["outcome"]
    status = f"{o['status']} ({o['basis']}{', ' + o['engine'] if o['engine'] else ''})"
    where = k.get("problem_id") or (f"symptom {k['symptom']}" if "symptom" in k else "general")
    extra = f" | runs: {len(o['run_ids'])}" if o["run_ids"] else ""
    used = uses.get(d["id"], [])
    if used:
        extra += f" | used: {len(used)} (yes {sum(1 for u in used if u['helped'] == 'yes')})"
    return (f"{d['id']} | {k['kind']} | {where} | {k['operation_type']} | {status} | "
            f"{','.join(k['components']) or '-'} | cond: {','.join(k['conditions']) or '-'}{extra} | "
            f"file: {origins.get(d['id'], '?')}\n"
            f"    {k.get('statement') or d['operation']}\n    src: {'; '.join(locators(d, ix)) or '-'}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    pr = sub.add_parser("problems", help="index lines that match")
    for name in ("level", "behaviour", "components", "operation"):
        pr.add_argument(f"--{name}", help="comma-separated list")
    q = sub.add_parser("query", help="compact matching rows")
    for name in ("problem", "level", "kind", "operation", "symptom", "status", "basis", "behaviour", "components"):
        q.add_argument(f"--{name}", help="comma-separated list" if name != "problem" else None)
    q.add_argument("--limit", type=int, default=20)
    q.add_argument("--json", action="store_true")
    s = sub.add_parser("show", help="one row in full")
    s.add_argument("id")
    for name in ("terms", "disputes", "index", "check"):
        sub.add_parser(name)
    args = parser.parse_args(argv)
    try:
        if args.command == "terms":
            v = vocabulary()
            for key in ("levels", "behaviours", "operation_types"):
                print(f"{key}: {', '.join(v[key])}")
            print(f"row kinds: {', '.join(v['row_kinds'])}")
            print(f"symptoms: {', '.join(v['symptoms']['terms'])}")
            print(f"outcome statuses: {', '.join(v['outcome_statuses'])}")
            print(f"outcome bases: {', '.join(v['outcome_bases'])}")
            print(f"components: {', '.join(v['components']['names'])}")
            return 0
        if args.command == "problems":
            md = INDEX_MD.read_text().splitlines()
            data = pipeline.read_json(INDEX_JSON)["problems"]
            keep = {p["id"] for p in data
                    if (not args.level or p["level"] in want(args.level))
                    and all(b in p["behaviours"] for b in want(args.behaviour))
                    and all(c in p["components"] for c in want(args.components))
                    and all(o in p["operations"] for o in want(args.operation))}
            header = md[md.index("## Design: one line per register problem") + 2:][:2]
            body = [l for l in md if l.startswith("| ") and l.split(" | ")[0][2:] in keep]
            print("\n".join(header + body) if body else "No matching problems.")
            return 0
        corpus, origins = pipeline.load_records()
        ix = pipeline.indexes(corpus)
        rows, hidden = visible_decisions(corpus)
        if args.command == "check":
            errors, report = check_all(corpus, origins)
            print("\n".join(errors) if errors else json.dumps(report))
            return 1 if errors else 0
        if args.command == "index":
            errors = check_keys(corpus)
            if errors:
                raise ValueError("\n".join(errors))
            write_index(corpus, origins)
            print(f"Wrote {INDEX_MD.relative_to(ROOT)}, {INDEX_JSON.relative_to(ROOT)}, {LOCK.relative_to(ROOT)}")
            return 0
        if args.command == "disputes":
            found = disputes(rows)
            print(json.dumps(found, indent=1) if found else "No disputed rows.")
            return 0
        uses = used_in(rows, origins)
        if args.command == "show":
            row = next((d for d in rows if d["id"] == args.id), None)
            if row is None:
                print(f"No visible row {args.id}.")
                return 1
            evidence = [{"id": e, "claim": ix["evidence"][e]["claim"], "classification": ix["evidence"][e]["classification"],
                         "quantities": ix["evidence"][e]["quantities"], "conditions": ix["evidence"][e]["conditions"],
                         "locators": [f"{ix['blocks'][b]['source_id']}: {ix['blocks'][b]['locator']}"
                                      for b in ix["evidence"][e]["block_ids"]]}
                        for e in row["evidence_ids"] if e in ix["evidence"] and e not in hidden]
            print(json.dumps({"file": f"dataset/records/{origins.get(row['id'], '?')}.json", "row": row,
                              "evidence": evidence, "used_in": uses.get(row["id"], [])}, indent=1, ensure_ascii=False))
            return 0
        found = sorted((d for d in rows if matches(d, args)), key=lambda d: d["id"])
        if args.json:
            print(json.dumps([{"id": d["id"], "file": origins.get(d["id"]), "keys": d["keys"],
                               "operation": d["operation"], "locators": locators(d, ix),
                               "used_in": uses.get(d["id"], [])} for d in found[:args.limit]],
                             indent=1, ensure_ascii=False))
        else:
            print("\n".join(compact(d, ix, origins, uses) for d in found[:args.limit]) or "No matching rows.")
            if len(found) > args.limit:
                print(f"... {len(found) - args.limit} more; narrow the query or raise --limit.")
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
