#!/usr/bin/env python3
"""Validate CHEPTA-Lab study records (docs/proposals/0002-study-record.md).

Checks the schema, file hashes, references and pointers, value classes, constraint verdicts and review
binding. It reads files already in the repository; it never runs CHEPTA, downloads anything or approves a review.
"""
import argparse
import hashlib
import json
import math
from datetime import date
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "dataset/schemas/study-record.schema.json"
CORPUS = ROOT / "dataset/records/pilot.json"
OUTCOMES = {"ok", "invalid_input", "missing_data", "unsupported", "not_converged", "cancelled", "out_of_time", "error"}
REQUIRED_SCOPES = ("engineering", "rights", "source_accuracy")
COLLECTIONS = ("files", "engines", "variants", "runs", "values", "constraints", "checks",
               "warning_notes", "assumptions", "unresolved_inputs")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def read_json(path):
    def invalid(value):
        raise ValueError(f"Non-finite JSON value: {value}")
    return json.loads(Path(path).read_text(), parse_constant=invalid)


def study_digest(record):
    """What a review approves: everything except the reviews and status. Files are bound by their hashes."""
    return hashlib.sha256(canonical({k: v for k, v in record.items() if k not in {"reviews", "status"}}).encode()).hexdigest()


def resolve(document, pointer):
    """RFC 6901 JSON pointer. Raises KeyError when the pointer does not resolve."""
    node = document
    if pointer == "":
        return node
    for part in pointer[1:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            if not part.isdigit() or int(part) >= len(node):
                raise KeyError(pointer)
            node = node[int(part)]
        elif isinstance(node, dict) and part in node:
            node = node[part]
        else:
            raise KeyError(pointer)
    return node


def is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def verdict(constraint, observed):
    if not is_number(observed):
        return "not_evaluated"
    op, tol = constraint["operator"], (constraint["tolerance"] or {"value": 0})["value"]
    if op == "equal":
        ok = abs(observed - constraint["target"]) <= tol
    elif op == "at_most":
        ok = observed <= constraint["upper"] + tol
    elif op == "at_least":
        ok = observed >= constraint["lower"] - tol
    else:
        ok = constraint["lower"] - tol <= observed <= constraint["upper"] + tol
    return "met" if ok else "not_met"


def validate(record, sources, root=ROOT, corpus=None):
    """Return a list of error messages; empty means valid. `sources` maps source id to its catalogue entry."""
    schema = read_json(SCHEMA)
    Draft202012Validator.check_schema(schema)
    errors = [f"schema {list(e.absolute_path)}: {e.message}" for e in Draft202012Validator(schema).iter_errors(record)]
    if errors:
        return errors
    ix = {}
    for name in COLLECTIONS:
        ix[name] = {row["id"]: row for row in record[name]}
        if len(ix[name]) != len(record[name]):
            errors.append(f"duplicate id in {name}")

    # Files: inside the repository, unchanged since the record was written (sha256 of the bytes).
    docs = {}
    for f in record["files"]:
        path = (root / f["path"]).resolve()
        if not path.is_relative_to(root.resolve()):
            errors.append(f"file {f['id']}: path escapes the repository")
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            errors.append(f"file {f['id']}: missing {f['path']}")
            continue
        if hashlib.sha256(raw).hexdigest() != f["sha256"]:
            errors.append(f"file {f['id']}: sha256 differs from {f['path']} (changed since the record was written)")
        if path.suffix == ".json":
            try:
                docs[f["id"]] = read_json(path)
            except ValueError as exc:
                errors.append(f"file {f['id']}: {exc}")
    if errors:
        return errors

    def role(fid):
        return ix["files"][fid]["role"] if fid in ix["files"] else None

    def lookup(ref, where):
        if ref["file"] not in ix["files"]:
            errors.append(f"{where}: unknown file {ref['file']}")
        elif ref["file"] not in docs:
            errors.append(f"{where}: file {ref['file']} is not JSON")
        else:
            try:
                return True, resolve(docs[ref["file"]], ref["pointer"])
            except KeyError:
                errors.append(f"{where}: pointer {ref['pointer']} not found in {ref['file']}")
        return False, None

    # Sources and links to the canonical corpus.
    for key in record["sources"]["source_ids"]:
        if key not in sources:
            errors.append(f"unknown source {key}")
    corpus = corpus if corpus is not None else read_json(CORPUS)
    corpus_ix = {name: {row["id"]: row for row in corpus[name]} for name in ("evidence", "tasks", "runs")}
    for key in record["sources"]["evidence_ids"]:
        if key not in corpus_ix["evidence"]:
            errors.append(f"unknown evidence {key}")
    for key in record["corpus_links"]["task_ids"]:
        if key not in corpus_ix["tasks"]:
            errors.append(f"unknown corpus task {key}")
    hashes = {f["sha256"] for f in record["files"]}
    for key in record["corpus_links"]["run_ids"]:
        run = corpus_ix["runs"].get(key)
        if run is None:
            errors.append(f"unknown corpus run {key}")
            continue
        for call in run["calls"]:
            for part in ("request", "response"):
                if call[part]["sha256"] not in hashes:
                    errors.append(f"corpus run {key}: {part} {call[part]['path']} is not one of this study's files")

    # Engines: a release, or a full commit between releases (ROADMAP rule 1).
    for eng in record["engines"]:
        if eng["pin"] == "release" and not eng["release"]:
            errors.append(f"engine {eng['id']}: pin 'release' needs a release version")
        if eng["pin"] == "commit_between_releases" and not eng["commit"]:
            errors.append(f"engine {eng['id']}: pin between releases needs a full commit")
        if eng["engine_file_hashes"]:
            lookup(eng["engine_file_hashes"], f"engine {eng['id']}")

    # Runs: CHEPTA's request and result exactly as written to disk, failures included.
    run_dates = {}
    for run in record["runs"]:
        where = f"run {run['id']}"
        if run["variant"] not in ix["variants"]:
            errors.append(f"{where}: unknown variant {run['variant']}")
        eng = ix["engines"].get(run["engine"])
        if eng is None:
            errors.append(f"{where}: unknown engine {run['engine']}")
        if run["runner"] is not None and role(run["runner"]) != "runner":
            errors.append(f"{where}: runner must be a file with role 'runner'")
        if role(run["request"]) != "request" or run["request"] not in docs:
            errors.append(f"{where}: request must be a JSON file with role 'request'")
            continue
        request = docs[run["request"]]
        if not isinstance(request, dict) or "capability" not in request or "input" not in request:
            errors.append(f"{where}: request is not a CHEPTA request (capability, input)")
            continue
        if run["result"] is None:
            if not run["failure_note"]:
                errors.append(f"{where}: a run without a result needs a failure_note")
        elif role(run["result"]) != "result" or run["result"] not in docs:
            errors.append(f"{where}: result must be a JSON file with role 'result'")
        else:
            result = docs[run["result"]]
            if eng is not None and result.get("chepta_result") != eng["result_format"]:
                errors.append(f"{where}: result format differs from engine {eng['id']} (chepta_result)")
            if result.get("capability") != request["capability"]:
                errors.append(f"{where}: result capability differs from the request")
            if result.get("outcome") not in OUTCOMES:
                errors.append(f"{where}: unknown outcome {result.get('outcome')!r}")
            elif result["outcome"] != "ok" and not run["failure_note"]:
                errors.append(f"{where}: outcome {result['outcome']} needs a failure_note")
        if run["execution_record"]:
            found, entry = lookup(run["execution_record"], where)
            if found and isinstance(entry, dict) and "id" in entry and entry["id"] != run["id"]:
                errors.append(f"{where}: execution record is for {entry['id']}")
        found, stamp = lookup(run["executed_at"], where)
        if found:
            try:
                run_dates[run["id"]] = date.fromisoformat(str(stamp)[:10])
            except ValueError:
                errors.append(f"{where}: executed_at is not a date")

    # Values: every number is a pointer into a file; its class decides what else must be stated.
    for value in record["values"]:
        where = f"value {value['id']}"
        found, number = lookup(value["ref"], where)
        cls = value["class"]
        if cls in ("measured", "published"):
            if not value["source"]:
                errors.append(f"{where}: {cls} value needs a source and locator")
            elif value["source"]["source_id"] not in record["sources"]["source_ids"]:
                errors.append(f"{where}: source is not listed in sources")
        if cls == "assumed" and not value["rationale"]:
            errors.append(f"{where}: assumed value needs a rationale")
        if cls == "derived" and not value["method"]:
            errors.append(f"{where}: derived value needs a method")
        if cls == "simulated":
            run = next((r for r in record["runs"] if r["id"] == value["run_id"]), None)
            if run is None or value["ref"]["file"] != run["result"]:
                errors.append(f"{where}: simulated value must point into its run's CHEPTA result")
        if cls in ("simulated", "derived") and value["source"]:
            errors.append(f"{where}: {cls} value must not cite a paper as its source")
        if value["run_id"] is not None and value["run_id"] not in ix["runs"]:
            errors.append(f"{where}: unknown run {value['run_id']}")
        for key in value["unresolved_ids"]:
            if key not in ix["unresolved_inputs"]:
                errors.append(f"{where}: unknown unresolved input {key}")
        if found and cls != "simulated" and not is_number(number):
            errors.append(f"{where}: pointer does not resolve to a number")

    # Constraints: declared with their origin, then compared with every run.
    for c in record["constraints"]:
        where = f"constraint {c['id']}"
        need = {"equal": ("target",), "at_most": ("upper",), "at_least": ("lower",), "between": ("lower", "upper")}[c["operator"]]
        for field in ("target", "lower", "upper"):
            if (field in need) != (c[field] is not None):
                errors.append(f"{where}: operator {c['operator']} uses exactly {', '.join(need)}")
        if c["operator"] == "equal" and c["tolerance"] is None:
            errors.append(f"{where}: an equality needs a stated tolerance")
        origin = c["origin"]
        if origin["class"] in ("measured", "published"):
            if origin["source_id"] not in record["sources"]["source_ids"] or not origin["locator"]:
                errors.append(f"{where}: {origin['class']} limit needs a listed source and locator")
        elif not origin["rationale"]:
            errors.append(f"{where}: assumed limit needs a rationale")
    declared = date.fromisoformat(record["constraint_declaration"]["declared_on"])
    if record["constraint_declaration"]["timing"] == "before_runs":
        for key, when in run_dates.items():
            if declared > when:
                errors.append(f"constraints declared on {declared} cannot precede run {key} executed on {when}")
    seen = set()
    for res in record["constraint_results"]:
        where = f"constraint result {res['constraint_id']}/{res['run_id']}"
        pair = (res["constraint_id"], res["run_id"])
        if pair in seen:
            errors.append(f"{where}: duplicate")
        seen.add(pair)
        c, run = ix["constraints"].get(res["constraint_id"]), ix["runs"].get(res["run_id"])
        if c is None or run is None:
            errors.append(f"{where}: unknown constraint or run")
            continue
        observed = None
        source = {"result": run["result"], "request": run["request"]}.get(c["observe"]["in"])
        if c["observe"]["in"] == "execution_record":
            if run["execution_record"]:
                _, entry = lookup(run["execution_record"], where)
                try:
                    observed = resolve(entry, c["observe"]["pointer"])
                except KeyError:
                    pass
        elif source in docs:
            try:
                observed = resolve(docs[source], c["observe"]["pointer"])
            except KeyError:
                pass
        expected = verdict(c, observed)
        if res["verdict"] != expected:
            errors.append(f"{where}: verdict {res['verdict']} but the files give {expected}")
        if res["verdict"] == "not_evaluated" and not res["note"]:
            errors.append(f"{where}: not_evaluated needs a note")

    # Lab's own checks, warning notes, assumptions, cost files.
    for chk in record["checks"]:
        where = f"check {chk['id']}"
        if chk["run_id"] not in ix["runs"]:
            errors.append(f"{where}: unknown run")
        if role(chk["ref"]["file"]) not in ("lab_check", "verifier"):
            errors.append(f"{where}: must point into a Lab check file, not a CHEPTA result")
        found, entry = lookup(chk["ref"], where)
        if found and isinstance(entry, dict) and "id" in entry and entry["id"] != chk["run_id"]:
            errors.append(f"{where}: points to the check of {entry['id']}")
        if chk["tolerances"]:
            lookup(chk["tolerances"], where)
    for note in record["warning_notes"]:
        for key in note["run_ids"]:
            run = ix["runs"].get(key)
            if run is None or run["result"] is None:
                errors.append(f"warning note {note['id']}: run {key} unknown or has no result")
                continue
            for pointer in note["pointers"]:
                lookup({"file": run["result"], "pointer": pointer}, f"warning note {note['id']}")
    targets = set(ix["variants"]) | set(ix["runs"]) | set(ix["values"])
    for a in record["assumptions"]:
        for key in a["applies_to"]:
            if key not in targets:
                errors.append(f"assumption {a['id']}: unknown target {key}")
    cost = record["cost_coverage"]
    if cost["status"] == "not_costed" and (cost["scope"] or cost["missing_items"] or cost["result_files"]):
        errors.append("cost coverage: not_costed carries no scope, items or files")
    if cost["status"] in ("complete_within_scope", "partial") and not (cost["scope"] and cost["result_files"]):
        errors.append("cost coverage: a cost result needs its scope and result files")
    if cost["status"] == "partial" and not cost["missing_items"]:
        errors.append("cost coverage: a partial cost lists what it excludes")
    for key in cost["result_files"]:
        if role(key) != "cost_result":
            errors.append(f"cost coverage: {key} is not a cost result file")

    # Acceptance: only a person, on the current content.
    if record["status"] == "accepted":
        errors.extend(f"accepted study: {reason}" for reason in acceptance_blockers(record))
    return errors


def acceptance_blockers(record):
    stamp = study_digest(record)
    reasons = []
    for scope in REQUIRED_SCOPES:
        if not any(r["scope"] == scope and r["reviewer_type"] == "human" and r["decision"] == "approved"
                   and r["review_digest"] == stamp for r in record["reviews"]):
            reasons.append(f"current human {scope} review missing")
    if record["constraint_declaration"]["timing"] != "before_runs":
        reasons.append("constraints were not declared before the runs")
    if any(u["blocking"] for u in record["unresolved_inputs"]):
        reasons.append("blocking unresolved inputs remain")
    pairs = {(r["constraint_id"], r["run_id"]) for r in record["constraint_results"] if r["verdict"] != "not_evaluated"}
    if any((c["id"], run["id"]) not in pairs for c in record["constraints"] for run in record["runs"]):
        reasons.append("some constraints are not evaluated for every run")
    return reasons


def find_records(root=ROOT):
    return sorted((root / "cases").glob("*/study-record.json"))


def validate_all(root=ROOT, paths=None):
    sources = {s["id"]: s for s in read_json(root / "data/sources.json")["sources"]}
    report, errors = [], []
    for path in paths or find_records(root):
        try:
            record = read_json(path)
            problems = validate(record, sources, root)
        except (ValueError, OSError, KeyError, TypeError) as exc:
            problems, record = [str(exc)], {}
        errors.extend(f"{path}: {p}" for p in problems)
        if not problems:
            report.append({"path": str(Path(path).resolve().relative_to(root.resolve())), "id": record["id"],
                           "status": record["status"], "study_digest": study_digest(record),
                           "runs": len(record["runs"]), "acceptance_blockers": acceptance_blockers(record)})
    return report, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="study records (default: cases/*/study-record.json)")
    args = parser.parse_args()
    report, errors = validate_all(paths=args.paths)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print(json.dumps({"valid": True, "study_records": report}, indent=2))


if __name__ == "__main__":
    main()
