#!/usr/bin/env python3
"""Check research metadata. This does not validate simulations or licensing."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def validate(sources, cases, upstream):
    errors = []
    def ids(rows, kind):
        seen = set()
        for row in rows:
            key = row.get("id")
            if not isinstance(key, str) or not key:
                errors.append(f"{kind}: missing id")
            elif key in seen:
                errors.append(f"{kind}: duplicate id {key}")
            seen.add(key)
        return seen
    source_ids = ids(sources, "source")
    ids(cases, "case")
    for source in sources:
        key = source.get("id")
        for field in ("title", "authors", "url", "open_copy_url", "access_verified",
                      "license", "rights_status", "locators", "next_action", "checked_on"):
            if not source.get(field):
                errors.append(f"{key}: missing {field}")
        for field in ("url", "open_copy_url"):
            if not str(source.get(field, "")).startswith("https://"):
                errors.append(f"{key}: {field} must be an HTTPS reference")
        if source.get("rights_status") not in {"attribution_required", "needs_review", "reference_only"}:
            errors.append(f"{key}: unknown rights_status")
    statuses = {"candidate_partial", "blocked_units_and_methods", "blocked_source_and_data"}
    for case in cases:
        key = case.get("id")
        if case.get("status") not in statuses:
            errors.append(f"{key}: unknown catalogue status")
        for source_id in case.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"{key}: unknown source {source_id}")
        for field in ("family", "title", "scope", "blockers", "next_action", "upstream_paths"):
            if not case.get(field):
                errors.append(f"{key}: missing {field}")
        if case.get("upstream_commit") != upstream.get("commit"):
            errors.append(f"{key}: upstream commit differs from audit")
        # This file is a research queue, never an accepted training dataset.
        if case.get("training_eligible") is not False:
            errors.append(f"{key}: research catalogue entries must not be training-eligible")
        if case.get("simulation_status") != "not_run" or case.get("engineering_review") != "pending":
            errors.append(f"{key}: execution/review claims require a separate evidenced case record")
        if not case.get("source_ids") and case.get("status") != "blocked_source_and_data":
            errors.append(f"{key}: a source-free case must be blocked")
    return errors

def main():
    sources = json.loads((ROOT / "data/sources.json").read_text())["sources"]
    cases = json.loads((ROOT / "data/candidates.json").read_text())["candidates"]
    upstream = json.loads((ROOT / "data/upstream.json").read_text())
    errors = validate(sources, cases, upstream)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Catalogue OK: {len(sources)} sources, {len(cases)} candidate families; 0 accepted training examples.")
    print("Metadata checks only; no simulation or engineering validation performed.")

if __name__ == "__main__":
    main()
