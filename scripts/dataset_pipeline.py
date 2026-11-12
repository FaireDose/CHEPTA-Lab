#!/usr/bin/env python3
"""Validate canonical records and export review previews or gated dataset releases.

No model calls, simulation execution, downloads, or automatic review approvals.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "dataset/schemas/corpus.schema.json"
COLLECTIONS = ("groups", "blocks", "evidence", "decisions", "runs", "tasks")
SCOPES = {"source_accuracy", "engineering", "rights", "context"}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def read_json(path):
    def invalid(value):
        raise ValueError(f"Non-finite JSON value: {value}")
    return json.loads(Path(path).read_text(), parse_constant=invalid)


def safe_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Artifact escapes repository: {relative}")
    return path


def artifact_data(root, artifact):
    path = safe_path(root, artifact["path"])
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != artifact["sha256"]:
        raise ValueError(f"Artifact hash mismatch: {artifact['path']}")
    return raw


def indexes(corpus):
    return {name: {row["id"]: row for row in corpus[name]} for name in COLLECTIONS}


def dependencies(task, ix):
    decisions = [ix["decisions"][key] for key in task["target"]["decision_ids"]]
    ev_ids = set(task["input"]["evidence_ids"] + task["target"]["evidence_ids"])
    for decision in decisions:
        ev_ids.update(decision["evidence_ids"])
    evidence = [ix["evidence"][key] for key in sorted(ev_ids)]
    block_ids = {key for row in evidence for key in row["block_ids"]}
    return {
        "decisions": sorted(decisions, key=lambda row: row["id"]),
        "evidence": evidence,
        "blocks": [ix["blocks"][key] for key in sorted(block_ids)],
        "runs": [ix["runs"][key] for key in sorted(task["target"]["run_ids"])],
    }


def review_digest(task, ix, sources):
    # Approval is bound to content AND linked evidence, engine artifacts and source metadata.
    reviewed = {k: v for k, v in task.items() if k not in {"reviews", "status"}}
    return digest({"task": reviewed, "dependencies": dependencies(task, ix),
                   "sources": [sources[key] for key in sorted(task["source_ids"])]})


def current(task, stamp, scope, reviewer_type):
    return [r for r in task["reviews"] if r["scope"] == scope and r["reviewer_type"] == reviewer_type
            and r["review_digest"] == stamp]


def full_human_path(task, stamp):
    # Original path: a person approves every scope.
    return [f"current human {scope} review missing" for scope in sorted(SCOPES)
            if not any(r["decision"] == "approved" for r in current(task, stamp, scope, "human"))]


def ai_spot_check_path(task, stamp):
    # AI full check by a separate session + a person's spot check of the 2-3 items the AI selected.
    ai = [r for r in current(task, stamp, "full_check", "ai_model") if r["decision"] == "approved"]
    valid = []
    for r in ai:
        items = r.get("selected_items", [])
        ids = [i["id"] for i in items]
        if (r.get("model") and r.get("model_family") and r.get("review_session")
                and r.get("case_built_in_session") and r["review_session"] != r["case_built_in_session"]
                and 2 <= len(items) <= 3 and len(set(ids)) == len(ids)):
            valid.append(r)
    if not valid:
        return ["current AI full check missing (needs model, family, a review session different from the "
                "building session, and 2 or 3 selected items with reasons)"]
    reasons = []
    ai_review = valid[0]
    ids = {i["id"] for i in ai_review["selected_items"]}
    spots = current(task, stamp, "spot_check", "human")
    if not spots:
        return ["current person spot check missing"]
    if any(d["decision"] == "rejected" for r in spots for d in r.get("item_decisions", [])):
        return ["a spot-checked item was rejected; the whole case needs a full recheck"]
    if not any(r["decision"] == "approved" and {d["item_id"] for d in r.get("item_decisions", [])} == ids
               and all(d["decision"] == "approved" for d in r["item_decisions"]) for r in spots):
        reasons.append("person spot check must approve exactly the items the AI selected")
    return reasons


def held_out_reasons(task, stamp):
    # Test split: a person or an AI model of another family than Claude must have checked the cases.
    ok = any(r["decision"] == "approved" and (
        r["reviewer_type"] == "human" or
        (r["reviewer_type"] == "ai_model" and r.get("model_family", "claude").strip().lower() not in {"claude", "anthropic"}))
        for r in task["reviews"] if r["scope"] == "independent_evaluation" and r["review_digest"] == stamp)
    return [] if ok else ["held-out task needs a current independent evaluation review by a person "
                          "or an AI model of another family than Claude"]


def review_reasons(task, stamp, split):
    path_a = full_human_path(task, stamp)
    if not path_a:
        return []  # full human review: a person checked every scope, held-out cases included
    path_b = ai_spot_check_path(task, stamp)
    if path_b:
        used_b = any(r["scope"] in {"full_check", "spot_check"} for r in task["reviews"])
        return path_b if used_b else path_a
    return held_out_reasons(task, stamp) if split == "test" else []


def eligibility(task, ix, sources):
    reasons = list(task["blockers"])
    if task["status"] != "accepted":
        reasons.append("task is draft")
    if ix["groups"][task["split_group"]]["split"] == "unassigned":
        reasons.append("split is unassigned")
    stamp = review_digest(task, ix, sources)
    reasons.extend(review_reasons(task, stamp, ix["groups"][task["split_group"]]["split"]))
    for key in task["source_ids"]:
        if sources[key]["rights_status"] != "attribution_required":
            reasons.append(f"source {key} is not eligible for the initial reusable release")
    if task["claim_scope"] != "literature_reasoning" and not task["target"]["run_ids"]:
        reasons.append("calculated target has no executed run")
    # This pilot only defines numerical-benchmark checks. Full process gates need their own contract.
    if task["claim_scope"] == "process_performance":
        reasons.append("process-performance acceptance contract is not implemented")
    return sorted(set(reasons))


def validate(corpus, sources, root=ROOT):
    schema = read_json(SCHEMA)
    Draft202012Validator.check_schema(schema)
    errors = [f"schema {list(e.absolute_path)}: {e.message}"
              for e in Draft202012Validator(schema).iter_errors(corpus)]
    if errors:
        return errors
    ix = indexes(corpus)
    for name in COLLECTIONS:
        if len(ix[name]) != len(corpus[name]):
            errors.append(f"duplicate ID in {name}")
    for block in corpus["blocks"]:
        if block["source_id"] not in sources:
            errors.append(f"unknown source: {block['source_id']}")
    for row in corpus["evidence"]:
        for key in row["block_ids"]:
            if key not in ix["blocks"]:
                errors.append(f"{row['id']}: unknown block {key}")
    for row in corpus["decisions"]:
        for key in row["evidence_ids"]:
            if key not in ix["evidence"]:
                errors.append(f"{row['id']}: unknown evidence {key}")
    for task in corpus["tasks"]:
        for field, keys in (("groups", [task["split_group"]]),
                            ("evidence", task["input"]["evidence_ids"] + task["target"]["evidence_ids"]),
                            ("decisions", task["target"]["decision_ids"]),
                            ("runs", task["target"]["run_ids"])):
            for key in keys:
                if key not in ix[field]:
                    errors.append(f"{task['id']}: unknown {field} reference {key}")
        if any(key not in sources for key in task["source_ids"]):
            errors.append(f"{task['id']}: unknown source")
    if errors:
        return errors
    # Related sources/families may never acquire different partitions, even through extra group IDs.
    assignments = {}
    for group in corpus["groups"]:
        for key in group["source_ids"]:
            if key not in sources:
                errors.append(f"{group['id']}: unknown group source {key}")
        for key in ["family:" + group["family"]] + ["source:" + s for s in group["source_ids"]]:
            if key in assignments and assignments[key] != group["split"]:
                errors.append(f"split leakage across {key}")
            assignments[key] = group["split"]
    document_splits = {}
    for task in corpus["tasks"]:
        group = ix["groups"][task["split_group"]]
        deps = dependencies(task, ix)
        if task["family"] != group["family"] or not set(task["source_ids"]) <= set(group["source_ids"]):
            errors.append(f"{task['id']}: family/source does not belong to its group")
        dependency_sources = {b["source_id"] for b in deps["blocks"]}
        dependency_sources.update(s for run in deps["runs"] for s in run["source_ids"])
        if not dependency_sources <= set(task["source_ids"]):
            errors.append(f"{task['id']}: undeclared dependency sources")
        if any(run["family"] != task["family"] for run in deps["runs"]):
            errors.append(f"{task['id']}: run family differs from task family")
        for block in deps["blocks"]:
            key = block["document_sha256"]
            if key in document_splits and document_splits[key] != group["split"]:
                errors.append("split leakage across duplicate document hash")
            document_splits[key] = group["split"]
        if task["task_type"] == "select_next":
            for key in task["input"]["evidence_ids"]:
                if any(ix["blocks"][b]["target_revealing"] for b in ix["evidence"][key]["block_ids"]):
                    errors.append(f"{task['id']}: target-revealing evidence in selection input")
        if task["target"]["answer"].strip() in task["input"]["prompt"]:
            errors.append(f"{task['id']}: target copied into prompt")
        if task["task_type"] != "tool_use" and task["target"]["run_ids"]:
            errors.append(f"{task['id']}: run traces require tool_use task")
        if task["task_type"] == "tool_use":
            if task["claim_scope"] == "literature_reasoning" or len(deps["runs"]) != 1:
                errors.append(f"{task['id']}: tool task requires one numerical run")
            elif task["input"]["request_artifact"] != deps["runs"][0]["calls"][0]["request"]:
                errors.append(f"{task['id']}: replay input differs from executed request")
        elif task["input"]["request_artifact"] is not None:
            errors.append(f"{task['id']}: unexpected request artifact")
        if task["status"] == "accepted":
            errors.extend(f"{task['id']}: {reason}" for reason in eligibility(task, ix, sources))
    for run in corpus["runs"]:
        try:
            artifacts = [run[key] for key in ("tool_contract", "manifest", "runner", "verification")]
            artifacts += [c[k] for c in run["calls"] for k in ("request", "response")]
            for artifact in artifacts:
                artifact_data(root, artifact)
            contract = read_json(safe_path(root, run["tool_contract"]["path"]))["function"]
            manifest = read_json(safe_path(root, run["manifest"]["path"]))
            if run["engine_commit_requested"] != manifest["engine_commit_requested"] or run["engine_commit_observed"] != manifest["engine_commit_observed"]:
                errors.append(f"{run['id']}: engine revision disagrees with manifest")
            executions = [r for r in manifest["runs"] if r["id"] == run["execution_id"]]
            if len(executions) != 1 or len(run["calls"]) != 1:
                errors.append(f"{run['id']}: pilot replay requires exactly one recorded execution")
                continue
            execution = executions[0]
            # Manifest paths are relative to the case directory, above results/.
            case_root = Path(run["manifest"]["path"]).parent.parent
            call = run["calls"][0]
            for key, original in (("request", "request_file"), ("response", "output_file")):
                if call[key]["path"] != str(case_root / execution[original]):
                    errors.append(f"{run['id']}: {key} is not the manifest artifact")
            request = read_json(safe_path(root, call["request"]["path"]))
            response = read_json(safe_path(root, call["response"]["path"]))
            if call["tool"] != contract["name"]:
                errors.append(f"{run['id']}: tool contract name mismatch")
            errors.extend(f"{run['id']}: request {e.message}" for e in Draft202012Validator(contract["parameters"]).iter_errors(request))
            if response.get("outcome") != execution["outcome"] or response.get("capability") != request["capability"]:
                errors.append(f"{run['id']}: response differs from manifest/capability")
            verification = read_json(safe_path(root, run["verification"]["path"]))
            checks = [c for c in verification["checks"] if c["id"] == run["execution_id"]]
            if len(checks) != 1 or not checks[0]["passed"] or verification["status"] != "passed":
                errors.append(f"{run['id']}: numerical benchmark checks did not pass")
        except (KeyError, ValueError, OSError, TypeError) as exc:
            errors.append(f"{run['id']}: {exc}")
    return errors


def render(task, ix, root=ROOT):
    # Only this allowlist becomes learner context. Targets, reviews and decision records stay hidden.
    visible = dict(task["input"])
    visible.pop("request_artifact")
    visible["evidence"] = [
        {"id": key, "claim": ix["evidence"][key]["claim"],
         "classification": ix["evidence"][key]["classification"],
         "conditions": ix["evidence"][key]["conditions"],
         "quantities": ix["evidence"][key]["quantities"],
         "limits": ix["evidence"][key]["limits"],
         "references": [{"source_id": ix["blocks"][b]["source_id"],
                         "url": ix["blocks"][b]["source_url"],
                         "locator": ix["blocks"][b]["locator"]}
                        for b in ix["evidence"][key]["block_ids"]]}
        for key in task["input"]["evidence_ids"]]
    if task["input"]["request_artifact"]:
        visible["request"] = read_json(safe_path(root, task["input"]["request_artifact"]["path"]))
    messages = [{"role": "system", "content": "Use evidence and actual tool observations. State assumptions, missing information and applicability limits. Do not invent numerical results."},
                {"role": "user", "content": canonical(visible)}]
    tools = []
    for key in task["target"]["run_ids"]:
        run = ix["runs"][key]
        tools.append(read_json(safe_path(root, run["tool_contract"]["path"])))
        for call in run["calls"]:
            request = read_json(safe_path(root, call["request"]["path"]))
            response = read_json(safe_path(root, call["response"]["path"]))
            messages.append({"role": "assistant", "tool_calls": [{"id": call["id"], "type": "function",
                "function": {"name": call["tool"], "arguments": canonical(request)}}]})
            messages.append({"role": "tool", "tool_call_id": call["id"], "content": canonical(response)})
    messages.append({"role": "assistant", "content": task["target"]["answer"]})
    return {"id": task["id"], "messages": messages, "tools": tools}


def build(corpus, sources, root=ROOT, preview=False):
    errors = validate(corpus, sources, root)
    if errors:
        raise ValueError("\n".join(errors))
    ix = indexes(corpus)
    files = {}
    rows, excluded, provenance = {}, [], []
    included = 0
    for task in sorted(corpus["tasks"], key=lambda row: row["id"]):
        reasons = eligibility(task, ix, sources)
        if reasons and not preview:
            excluded.append({"id": task["id"], "reasons": reasons})
            continue
        row = render(task, ix, root)
        split = ix["groups"][task["split_group"]]["split"]
        if preview:
            row.update({"preview_only": True, "release_blockers": reasons})
            rows.setdefault("review-preview.jsonl", []).append(row)
        elif split == "train":
            rows.setdefault("train.jsonl", []).append(row)
        else:
            # Evaluation inputs contain neither reference answers nor future observations.
            rows.setdefault(f"{split}.inputs.jsonl", []).append({**row, "messages": row["messages"][:2]})
            rows.setdefault(f"{split}.targets.jsonl", []).append({"id": task["id"], "target": task["target"],
                "reference_trajectory": row["messages"][2:]})
        provenance.append({"id": task["id"], "revision": task["revision"], "split": split,
                           "source_ids": task["source_ids"], "review_digest": review_digest(task, ix, sources),
                           "dependencies": dependencies(task, ix), "reviews": task["reviews"]})
        included += 1
    if not included and not preview:
        raise ValueError("No eligible tasks. Use preview for draft review; do not train on previews.")
    for path, records in rows.items():
        files[path] = "".join(canonical(row) + "\n" for row in records)
    files["provenance.jsonl"] = "".join(canonical(row) + "\n" for row in provenance)
    files["manifest.json"] = json.dumps({"schema_version": 1, "preview_only": preview,
        "corpus_sha256": digest(corpus), "sources_sha256": digest(sources),
        "schema_sha256": hashlib.sha256(SCHEMA.read_bytes()).hexdigest(),
        "exporter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "groups": corpus["groups"], "included": included, "excluded": excluded,
        "file_sha256": {p: hashlib.sha256(v.encode()).hexdigest() for p, v in sorted(files.items())}},
        indent=2, sort_keys=True) + "\n"
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "preview", "release"])
    parser.add_argument("--corpus", type=Path, default=ROOT / "dataset/records/pilot.json")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    corpus = read_json(args.corpus)
    sources = {s["id"]: s for s in read_json(ROOT / "data/sources.json")["sources"]}
    try:
        errors = validate(corpus, sources)
        if errors:
            raise ValueError("\n".join(errors))
        ix = indexes(corpus)
        if args.command == "validate":
            report = [{"id": t["id"], "review_digest": review_digest(t, ix, sources),
                       "release_blockers": eligibility(t, ix, sources)} for t in corpus["tasks"]]
            # Study records (docs/proposals/0002-study-record.md) are checked here too, so one command covers both.
            spec = importlib.util.spec_from_file_location("study_record", ROOT / "scripts/study_record.py")
            study_record = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(study_record)
            studies, study_errors = study_record.validate_all()
            if study_errors:
                raise ValueError("\n".join(study_errors))
            print(json.dumps({"valid": True, "counts": {k: len(corpus[k]) for k in COLLECTIONS}, "tasks": report,
                              "study_records": studies}, indent=2))
            return
        if args.out is None:
            raise ValueError("--out is required; choose a new output directory")
        files = build(corpus, sources, preview=args.command == "preview")
        # Never mix a preview with stale release files, or overwrite an earlier release.
        if args.out.exists():
            raise ValueError("Output directory already exists; use a fresh directory")
        args.out.mkdir(parents=True)
        for path, content in files.items():
            (args.out / path).write_text(content)
        print(f"Wrote {args.command} to {args.out}. No training was started.")
    except (ValueError, OSError, KeyError) as exc:
        parser.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
