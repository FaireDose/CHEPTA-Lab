"""Study-record validator tests. Synthetic reviews and failed runs exist only in memory or a temporary folder."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("study_record", ROOT / "scripts/study_record.py")
s = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s)
RECORD = ROOT / "cases/ethanol-zsm5-573k/study-record.json"


class StudyRecordTests(unittest.TestCase):
    def setUp(self):
        self.record = s.read_json(RECORD)
        self.sources = {x["id"]: x for x in s.read_json(ROOT / "data/sources.json")["sources"]}

    def errors(self, record=None, root=ROOT):
        return s.validate(record or self.record, self.sources, root)

    def test_ethanol_example_valid_and_draft(self):
        self.assertEqual(self.errors(), [])
        self.assertEqual(self.record["status"], "draft")
        self.assertEqual(self.record["reviews"], [])
        self.assertEqual(len(self.record["runs"]), 18)
        self.assertEqual({r["engine"] for r in self.record["runs"]}, {"chepta-c1adf6b", "chepta@0.6.0", "chepta@0.6.1"})

    def test_every_run_file_is_the_existing_file(self):
        manifest = s.read_json(ROOT / "cases/ethanol-zsm5-573k/results/run-manifest.json")
        files = {f["id"]: f for f in self.record["files"]}
        for run, entry in zip(self.record["runs"], manifest["runs"]):
            self.assertEqual(files[run["request"]]["path"], "cases/ethanol-zsm5-573k/" + entry["request_file"])
            self.assertEqual(files[run["result"]]["path"], "cases/ethanol-zsm5-573k/" + entry["output_file"])

    def test_rerun_files_are_the_0_6_0_files(self):
        manifest = s.read_json(ROOT / "cases/ethanol-zsm5-573k/results-chepta-0.6.0/run-manifest.json")
        files = {f["id"]: f for f in self.record["files"]}
        new = [r for r in self.record["runs"] if r["engine"] == "chepta@0.6.0"]
        self.assertEqual(len(new), 6)
        for run, entry in zip(new, manifest["runs"]):
            self.assertEqual(run["execution_id"], entry["id"])
            self.assertEqual(files[run["result"]]["sha256"], entry["output_file_sha256"])

    def test_rerun_files_are_the_0_6_1_files(self):
        manifest = s.read_json(ROOT / "cases/ethanol-zsm5-573k/results-chepta-0.6.1/run-manifest.json")
        files = {f["id"]: f for f in self.record["files"]}
        new = [r for r in self.record["runs"] if r["engine"] == "chepta@0.6.1"]
        self.assertEqual(len(new), 6)
        for run, entry in zip(new, manifest["runs"]):
            self.assertEqual(run["execution_id"], entry["id"])
            self.assertEqual(files[run["result"]]["sha256"], entry["output_file_sha256"])

    def test_release_pin_must_match_lock_file(self):
        engine = next(e for e in self.record["engines"] if e["pin"] == "release")
        engine["release"] = "0.6.1"
        errors = self.errors()
        self.assertTrue(any("lock entry does not give release 0.6.1" in e for e in errors))
        self.assertTrue(any("reports library 0.6.0" in e for e in errors))

    def test_release_pin_needs_lock(self):
        next(e for e in self.record["engines"] if e["pin"] == "release")["lock"] = None
        self.assertTrue(any("names its lock-file entry" in e for e in self.errors()))

    def test_earlier_verifier_version_is_recorded(self):
        old = [c for c in self.record["checks"] if c["kind"] == "independent_reference_solution"
               and c["run_id"].startswith("upstream") and "chepta-0.6." not in c["run_id"]]
        self.assertTrue(old and all(c["verifier"]["earlier_version"] for c in old))

    def test_changed_file_is_detected(self):
        self.record["files"][-1]["sha256"] = "0" * 64
        self.assertTrue(any("sha256 differs" in e for e in self.errors()))

    def test_path_outside_repository_refused(self):
        self.record["files"][0]["path"] = "../outside.json"
        self.assertTrue(any("escapes" in e for e in self.errors()))

    def test_simulated_number_cannot_be_typed_in(self):
        value = next(v for v in self.record["values"] if v["class"] == "simulated")
        value["value"] = 0.99
        self.assertTrue(any("schema" in e for e in self.errors()))

    def test_simulated_value_must_point_into_its_result(self):
        value = next(v for v in self.record["values"] if v["class"] == "simulated")
        value["ref"] = {"file": "case-input", "pointer": "/T_K"}
        self.assertTrue(any("its run's CHEPTA result" in e for e in self.errors()))

    def test_published_value_needs_source(self):
        value = next(v for v in self.record["values"] if v["class"] == "published")
        value["source"] = None
        self.assertTrue(any("needs a source" in e for e in self.errors()))

    def test_assumed_value_needs_rationale(self):
        value = next(v for v in self.record["values"] if v["class"] == "assumed")
        value["rationale"] = None
        self.assertTrue(any("needs a rationale" in e for e in self.errors()))

    def test_bad_pointer_detected(self):
        self.record["values"][0]["ref"]["pointer"] = "/no_such_key"
        self.assertTrue(any("not found" in e for e in self.errors()))

    def test_unknown_source_detected(self):
        self.record["sources"]["source_ids"].append("no-such-source")
        self.assertTrue(any("unknown source" in e for e in self.errors()))

    def test_wrong_verdict_detected(self):
        self.record["constraint_results"][0]["verdict"] = "not_met"
        self.assertTrue(any("the files give met" in e for e in self.errors()))

    def test_tightened_constraint_turns_not_met(self):
        c = next(c for c in self.record["constraints"] if c["id"] == "wf-within-source-range")
        c["upper"] = 1.0
        errors = self.errors()
        self.assertTrue(any("wf-within-source-range" in e and "give not_met" in e for e in errors))

    def test_constraints_cannot_claim_declaration_before_runs_afterwards(self):
        self.record["constraint_declaration"]["timing"] = "before_runs"
        self.assertTrue(any("cannot precede" in e for e in self.errors()))

    def test_interface_state_refused(self):
        self.record["workbench"] = {"layout": {"R": [10, 20]}}
        self.assertTrue(any("schema" in e for e in self.errors()))

    def test_accepted_without_human_review_refused(self):
        self.record["status"] = "accepted"
        self.assertTrue(any("human engineering review missing" in e for e in self.errors()))

    def test_agent_review_and_stale_review_do_not_count(self):
        record = self.record
        stamp = s.study_digest(record)
        record["reviews"] = [{"scope": scope, "reviewer": "SYNTHETIC UNIT TEST ONLY", "reviewer_type": "agent",
                              "decision": "approved", "review_digest": stamp, "date": "2026-11-11",
                              "notes": "Not an actual review"} for scope in s.REQUIRED_SCOPES]
        self.assertEqual(len(s.acceptance_blockers(record)), 5)
        for review in record["reviews"]:
            review["reviewer_type"] = "human"
        self.assertNotIn("current human engineering review missing", s.acceptance_blockers(record))
        record["limitations"].append("A later edit.")
        self.assertIn("current human engineering review missing", s.acceptance_blockers(record))

    def test_cost_coverage_rules(self):
        self.record["cost_coverage"] = {"status": "partial", "scope": "reactor only", "missing_items": [], "result_files": []}
        errors = self.errors()
        self.assertTrue(any("needs its scope and result files" in e for e in errors))
        self.assertTrue(any("lists what it excludes" in e for e in errors))

    def test_corpus_run_must_use_the_same_files(self):
        self.record["files"] = [f for f in self.record["files"] if f["id"] != "result.upstream_simplified-wf0.38"]
        self.assertTrue(self.errors())

    def test_failed_run_is_kept_with_a_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / "data", root / "data")
            shutil.copytree(ROOT / "cases/ethanol-zsm5-573k", root / "cases/ethanol-zsm5-573k")
            shutil.copy(ROOT / "package-lock.json", root / "package-lock.json")
            failed = {"chepta_result": 1, "capability": "solve_flowsheet", "outcome": "not_converged",
                      "error": {"code": "NOT_CONVERGED", "message": "synthetic test failure", "where": []},
                      "reproduction": {}, "run": {}}
            path = root / "cases/ethanol-zsm5-573k/results/synthetic-failed.output.json"
            path.write_text(json.dumps(failed))
            record = copy.deepcopy(self.record)
            record["files"].append({"id": "result.failed", "path": str(path.relative_to(root)),
                                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "role": "result"})
            run = dict(record["runs"][0], id="failed-run", result="result.failed", failure_note=None,
                       execution_record=None)
            record["runs"].append(run)
            errors = s.validate(record, self.sources, root)
            self.assertTrue(any("needs a failure_note" in e for e in errors))
            run["failure_note"] = "Kept as a failure; not hidden."
            record["constraint_results"].append({"constraint_id": "reactor-temperature", "run_id": "failed-run",
                                                 "verdict": "not_evaluated", "note": "No result value."})
            self.assertEqual(s.validate(record, self.sources, root), [])


if __name__ == "__main__":
    unittest.main()
