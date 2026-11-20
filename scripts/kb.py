#!/usr/bin/env python3
"""The knowledge base for process design (docs/proposals/0003-knowledge-base.md).

Read the index first (dataset/index/problems.md), then query; open a record file only for one row.

  python scripts/kb.py problems --behaviour azeotrope-min-boiling   only the index lines that match
  python scripts/kb.py query --behaviour azeotrope-min-boiling --components ethanol,water --status worked
  python scripts/kb.py show <row id>        one row in full, with its evidence locators
  python scripts/kb.py terms                the controlled vocabulary
  python scripts/kb.py disputes             rows that disagree under the same conditions
  python scripts/kb.py index                regenerate dataset/index/ after changing records
  python scripts/kb.py check                keys, conflicts, outcome lock, index up to date

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
INDEX_MD = ROOT / "dataset/index/problems.md"
INDEX_JSON = ROOT / "dataset/index/problems.json"
LOCK = ROOT / "dataset/index/outcomes.lock.json"
STATUSES_SHOWN = ("worked", "failed", "lead", "untested")
RESULTS_DIR = re.compile(r"^results-chepta-([0-9]+\.[0-9]+\.[0-9]+)$")


# ---------- reading ----------

def vocabulary(path=pipeline.VOCABULARY):
    return pipeline.read_json(path)


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


# ---------- groups and held-out rows ----------

def row_groups(row, kind, ix):
    """Groups a decision or evidence row belongs to: those holding the sources of its evidence passages."""
    evidence = [ix["evidence"][k] for k in row["evidence_ids"] if k in ix["evidence"]] if kind == "decisions" else [row]
    sources = {ix["blocks"][b]["source_id"] for e in evidence for b in e["block_ids"] if b in ix["blocks"]}
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


# ---------- conflicts ----------

def current_rows(rows):
    """Within one problem + operation + conditions: every non-CHEPTA row, and the CHEPTA rows of the latest
    released engine (a later version adds a row and supersedes, it never overwrites)."""
    chepta = [r for r in rows if r["keys"]["outcome"]["basis"] == "chepta_run"]
    released = [engine_version(r["keys"]["outcome"]["engine"]) for r in chepta]
    latest = max((v for v in released if v), default=None)
    keep = [r for r in chepta if (engine_version(r["keys"]["outcome"]["engine"]) == latest)] if latest else chepta
    return [r for r in rows if r["keys"]["outcome"]["basis"] != "chepta_run"] + keep


def condition_sets(decisions):
    sets = {}
    for d in decisions:
        k = d["keys"]
        sets.setdefault((k["problem_id"], k["operation_type"], tuple(sorted(k["conditions"]))), []).append(d)
    return sets


def disputes(decisions):
    """Sets of rows with the same problem, operation and conditions where one says worked and another failed."""
    found = []
    for key, rows in sorted(condition_sets(decisions).items()):
        cur = current_rows(rows)
        worked = [r for r in cur if r["keys"]["outcome"]["status"] == "worked"]
        failed = [r for r in cur if r["keys"]["outcome"]["status"] == "failed"]
        if not (worked and failed):
            continue
        open_pairs = [(a["id"], b["id"]) for a in worked for b in failed
                      if b["id"] not in a["keys"].get("disputed_with", [])
                      and a["id"] not in b["keys"].get("disputed_with", [])]
        found.append({"problem_id": key[0], "operation_type": key[1], "conditions": list(key[2]),
                      "rows": [{"id": r["id"], "status": r["keys"]["outcome"]["status"],
                                "basis": r["keys"]["outcome"]["basis"], "engine": r["keys"]["outcome"]["engine"]}
                               for r in sorted(cur, key=lambda r: r["id"])],
                      "unacknowledged_pairs": open_pairs})
    return found


# ---------- checks ----------

def check_keys(corpus, vocab=None, register=None, root=ROOT):
    vocab = vocab or vocabulary()
    register = register if register is not None else register_rows()
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
        o = k["outcome"]
        if k["problem_id"] not in register:
            errors.append(f"{where}: problem_id {k['problem_id']} is not a row of data/ISSUES_AND_ROUTES.md")
        elif register[k["problem_id"]] != k["level"]:
            errors.append(f"{where}: level {k['level']} differs from the register's {register[k['problem_id']]}")
        terms(where, [k["level"]], vocab["levels"], "level")
        terms(where, [k["operation_type"]], vocab["operation_types"], "operation type")
        terms(where, k["behaviours"], vocab["behaviours"], "behaviour")
        terms(where, k["components"], names, "component")
        terms(where, [o["status"]], vocab["outcome_statuses"], "outcome status")
        terms(where, [o["basis"]], vocab["outcome_bases"], "outcome basis")
        if o["basis"] == "chepta_run":
            if not o["engine"] or not o["run_ids"]:
                errors.append(f"{where}: an outcome from a CHEPTA run names its engine and its run_ids")
        elif o["engine"] is not None:
            errors.append(f"{where}: engine is only for outcomes from a CHEPTA run")
        if o["status"] in ("worked", "failed") and o["basis"] == "lab_inference":
            errors.append(f"{where}: a Lab inference can only be untested or a lead")
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
            errors.append(f"disputed: {a} (worked) and {b} (failed) share problem {found['problem_id']}, operation "
                          f"{found['operation_type']} and conditions {found['conditions']}. Name the condition that "
                          "differs, or record the disagreement in keys.disputed_with of your own row. "
                          "Never merge or delete either row.")
    return errors


def lock_entries(corpus):
    """Outcomes from CHEPTA runs, which are append-only (held-out rows are left out)."""
    rows, hidden = visible_decisions(corpus)
    return {d["id"]: copy.deepcopy(d["keys"]["outcome"]) for d in sorted(rows, key=lambda d: d["id"])
            if d["keys"]["outcome"]["basis"] == "chepta_run"}


def lock_errors(corpus, lock):
    errors, now = [], lock_entries(corpus)
    hidden = held_out(corpus)
    for key, outcome in lock.get("rows", {}).items():
        if key in hidden:
            continue
        if key not in now:
            errors.append(f"{key}: an outcome from a CHEPTA run was deleted; rows are never deleted "
                          "(dataset/index/outcomes.lock.json)")
        elif now[key] != outcome:
            errors.append(f"{key}: an outcome from a CHEPTA run was edited; add a new row (for a new engine version, "
                          "new runs or a correction) instead of overwriting it")
    return errors


# ---------- index ----------

def build_index(corpus, origins, register=None):
    register = register if register is not None else register_rows()
    ix = pipeline.indexes(corpus)
    rows, hidden = visible_decisions(corpus)
    sets = condition_sets(rows)
    current = {r["id"] for group in sets.values() for r in current_rows(group)}
    dispute_count = {}
    for found in disputes(rows):
        dispute_count[found["problem_id"]] = dispute_count.get(found["problem_id"], 0) + 1
    problems = []
    for problem, level in register.items():
        mine = [d for d in rows if d["keys"]["problem_id"] == problem]
        keyed_evidence = [e for e in corpus["evidence"] if e["id"] not in hidden
                          and problem in e.get("keys", {}).get("problem_ids", [])]
        papers, files = set(), set()
        for d in mine:
            papers |= row_groups(d, "decisions", ix)[1]
            files.add(origins.get(d["id"], "?"))
        for e in keyed_evidence:
            papers |= row_groups(e, "evidence", ix)[1]
            files.add(origins.get(e["id"], "?"))
        counts = {s: sum(1 for d in mine if d["id"] in current and d["keys"]["outcome"]["status"] == s)
                  for s in STATUSES_SHOWN}
        problems.append({
            "id": problem, "level": level,
            "behaviours": sorted({b for d in mine for b in d["keys"]["behaviours"]}
                                 | {b for e in keyed_evidence for b in e["keys"].get("behaviours", [])}),
            "components": sorted({c for d in mine for c in d["keys"]["components"]}
                                 | {c for e in keyed_evidence for c in e["keys"].get("components", [])}),
            "operations": sorted({d["keys"]["operation_type"] for d in mine}),
            "rows": len(mine), "counts": counts, "superseded": len(mine) - sum(1 for d in mine if d["id"] in current),
            "disputed": dispute_count.get(problem, 0), "papers": len(papers), "files": sorted(files)})
    data = {"about": "Generated by python scripts/kb.py index from dataset/records/ and data/ISSUES_AND_ROUTES.md. "
                     "Do not edit. Held-out groups are left out.",
            "problems": problems}
    lines = ["# Knowledge-base index (generated; do not edit)", "",
             "Made by `python scripts/kb.py index` from dataset/records/ and data/ISSUES_AND_ROUTES.md; held-out "
             "groups left out. One line per problem. Next: `python scripts/kb.py query --problem <id>` (or "
             "`--behaviour`, `--components`, `--operation`, `--status`, `--level`), then `python scripts/kb.py show "
             "<row id>`. Terms: `python scripts/kb.py terms`.", "",
             "W/F/L/U: rows worked / failed / lead / untested (for CHEPTA runs, the latest engine per condition). "
             "D: disputed sets. P: papers. Files: dataset/records/<file>.json.", "",
             "| problem | level | operations | behaviours | W/F/L/U | D | P | files |",
             "|---|---|---|---|---|---|---|---|"]
    for p in problems:
        c = p["counts"]
        lines.append(f"| {p['id']} | {p['level']} | {','.join(p['operations']) or '-'} | "
                     f"{','.join(p['behaviours']) or '-'} | {c['worked']}/{c['failed']}/{c['lead']}/{c['untested']} | "
                     f"{p['disputed']} | {p['papers']} | {','.join(p['files']) or '-'} |")
    return "\n".join(lines) + "\n", json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def index_errors(corpus, origins):
    md, js = build_index(corpus, origins)
    stale = [path for path, text in ((INDEX_MD, md), (INDEX_JSON, js))
             if not path.is_file() or path.read_text() != text]
    errors = [f"{p.relative_to(ROOT)} is stale: run python scripts/kb.py index" for p in stale]
    lock = pipeline.read_json(LOCK) if LOCK.is_file() else {"rows": {}}
    missing = [k for k in lock_entries(corpus) if k not in lock["rows"]]
    if missing:
        errors.append(f"outcome lock misses {', '.join(missing)}: run python scripts/kb.py index")
    return errors + lock_errors(corpus, lock)


def check_all(corpus, origins):
    errors = check_keys(corpus)
    if not errors:
        errors = index_errors(corpus, origins)
    rows, _ = visible_decisions(corpus)
    return errors, {"decisions_with_keys": len(rows), "disputed_sets": len(disputes(rows)),
                    "index": "current" if not errors else "see errors"}


def write_index(corpus, origins):
    lock = pipeline.read_json(LOCK) if LOCK.is_file() else {"rows": {}}
    errors = lock_errors(corpus, lock)
    if errors:
        raise ValueError("\n".join(errors))
    rows = dict(lock.get("rows", {}))
    rows.update({k: v for k, v in lock_entries(corpus).items() if k not in rows})
    lock = {"about": "Append-only record of outcomes from CHEPTA runs, written by python scripts/kb.py index. "
                     "Editing or deleting such an outcome in dataset/records/ fails the checks: add a new row instead. "
                     "Changing this file by hand is a deliberate correction; say why in the commit.",
            "rows": dict(sorted(rows.items()))}
    md, js = build_index(corpus, origins)
    INDEX_MD.parent.mkdir(parents=True, exist_ok=True)
    INDEX_MD.write_text(md)
    INDEX_JSON.write_text(js)
    LOCK.write_text(json.dumps(lock, indent=2, ensure_ascii=False) + "\n")


# ---------- query ----------

def matches(d, args):
    k = d["keys"]
    want = lambda value: [x.strip() for x in value.split(",") if x.strip()] if value else []
    return ((not args.problem or k["problem_id"] == args.problem)
            and (not args.level or k["level"] == args.level)
            and (not args.operation or k["operation_type"] in want(args.operation))
            and (not args.status or k["outcome"]["status"] in want(args.status))
            and (not args.basis or k["outcome"]["basis"] in want(args.basis))
            and all(b in k["behaviours"] for b in want(args.behaviour))
            and all(c in k["components"] for c in want(args.components)))


def locators(d, ix):
    out = []
    for key in d["evidence_ids"]:
        e = ix["evidence"].get(key)
        for b in (e["block_ids"] if e else []):
            block = ix["blocks"].get(b)
            if block:
                out.append(f"{block['source_id']}: {block['locator']}")
    return sorted(set(out))


def compact(d, ix, origins):
    k, o = d["keys"], d["keys"]["outcome"]
    status = f"{o['status']} ({o['basis']}{', ' + o['engine'] if o['engine'] else ''})"
    runs = f" | runs: {len(o['run_ids'])}" if o["run_ids"] else ""
    return (f"{d['id']} | {k['problem_id']} | {k['operation_type']} | {status} | {','.join(k['components'])} | "
            f"cond: {','.join(k['conditions']) or '-'}{runs} | file: {origins.get(d['id'], '?')}\n"
            f"    {d['operation']}\n    src: {'; '.join(locators(d, ix)) or '-'}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    q = sub.add_parser("query", help="compact matching rows")
    for name in ("problem", "level", "operation", "status", "basis", "behaviour", "components"):
        q.add_argument(f"--{name}", help="comma-separated list" if name != "problem" else None)
    q.add_argument("--limit", type=int, default=20)
    q.add_argument("--json", action="store_true")
    pr = sub.add_parser("problems", help="index lines that match")
    for name in ("level", "behaviour", "components", "operation"):
        pr.add_argument(f"--{name}", help="comma-separated list")
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
            print(f"outcome statuses: {', '.join(v['outcome_statuses'])}")
            print(f"outcome bases: {', '.join(v['outcome_bases'])}")
            print(f"components: {', '.join(v['components']['names'])}")
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
        if args.command == "problems":
            want = lambda value: [x.strip() for x in value.split(",") if x.strip()] if value else []
            md = INDEX_MD.read_text().splitlines()
            data = pipeline.read_json(INDEX_JSON)["problems"]
            keep = {p["id"] for p in data
                    if (not args.level or p["level"] in want(args.level))
                    and all(b in p["behaviours"] for b in want(args.behaviour))
                    and all(c in p["components"] for c in want(args.components))
                    and all(o in p["operations"] for o in want(args.operation))}
            header = [l for l in md if l.startswith("| problem") or l.startswith("|---")]
            body = [l for l in md if l.startswith("| ") and l.split(" | ")[0][2:] in keep]
            print("\n".join(header + body) if body else "No matching problems.")
            return 0
        if args.command == "disputes":
            print(json.dumps(disputes(rows), indent=1) if disputes(rows) else "No disputed rows.")
            return 0
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
                              "evidence": evidence}, indent=1, ensure_ascii=False))
            return 0
        found = sorted((d for d in rows if matches(d, args)), key=lambda d: d["id"])
        if args.json:
            print(json.dumps([{"id": d["id"], "file": origins.get(d["id"]), "keys": d["keys"],
                               "operation": d["operation"], "locators": locators(d, ix)} for d in found[:args.limit]],
                             indent=1, ensure_ascii=False))
        else:
            print("\n".join(compact(d, ix, origins) for d in found[:args.limit]) or "No matching rows.")
            if len(found) > args.limit:
                print(f"... {len(found) - args.limit} more; narrow the query or raise --limit.")
        return 0
    except (ValueError, OSError, KeyError) as exc:
        print(exc, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
