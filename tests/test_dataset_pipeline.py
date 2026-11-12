"""Release-boundary tests. Synthetic approvals exist only in memory in these tests."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("pipeline", ROOT / "scripts/dataset_pipeline.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.corpus = p.read_json(ROOT / "dataset/records/pilot.json")
        self.sources = {s["id"]: s for s in p.read_json(ROOT / "data/sources.json")["sources"]}

    def approve_for_test(self, index=0, split="train"):
        task = self.corpus["tasks"][index]
        group = next(g for g in self.corpus["groups"] if g["id"] == task["split_group"])
        group["split"] = split
        task["status"] = "accepted"
        task["blockers"] = []
        stamp = p.review_digest(task, p.indexes(self.corpus), self.sources)
        task["reviews"] = [{"scope": scope, "reviewer": "SYNTHETIC UNIT TEST ONLY",
                            "reviewer_type": "human", "decision": "approved", "review_digest": stamp,
                            "date": "2026-10-30", "notes": "Not an actual review"} for scope in p.SCOPES]
        return task

    def ai_spot_setup(self, split="train", family="Claude", spot="approved"):
        task = self.approve_for_test(split=split)
        stamp = p.review_digest(task, p.indexes(self.corpus), self.sources)
        items = [{"id": "i1", "what": "x", "why": "largest_effect"},
                 {"id": "i2", "what": "y", "why": "least_certain"},
                 {"id": "i3", "what": "z", "why": "random"}]
        base = {"review_digest": stamp, "date": "2026-11-12", "notes": "SYNTHETIC UNIT TEST ONLY"}
        task["reviews"] = [
            dict(base, scope="full_check", reviewer="test-model", reviewer_type="ai_model",
                 decision="approved", model="test-model", model_family=family,
                 review_session="rev-1", case_built_in_session="build-1", selected_items=items),
            dict(base, scope="spot_check", reviewer="SYNTHETIC PERSON", reviewer_type="human",
                 decision="approved" if spot == "approved" else "changes_requested",
                 item_decisions=[{"item_id": i["id"], "decision": "approved"} for i in items[:2]]
                 + [{"item_id": "i3", "decision": spot}])]
        return task

    def blockers(self, task):
        ix = p.indexes(self.corpus)
        return p.eligibility(task, ix, self.sources)

    def test_ai_full_check_plus_spot_check_accepted(self):
        task = self.ai_spot_setup()
        self.assertEqual(self.blockers(task), [])
        self.assertEqual(p.validate(self.corpus, self.sources), [])

    def test_missing_spot_check_refused(self):
        task = self.ai_spot_setup()
        task["reviews"] = task["reviews"][:1]
        self.assertTrue(any("spot check" in r for r in self.blockers(task)))

    def test_rejected_spot_item_refused(self):
        task = self.ai_spot_setup(spot="rejected")
        self.assertTrue(any("rejected" in r for r in self.blockers(task)))

    def test_ai_check_labelled_human_refused(self):
        task = self.ai_spot_setup()
        task["reviews"][0]["reviewer_type"] = "human"
        self.assertTrue(self.blockers(task))

    def test_spot_check_labelled_ai_refused(self):
        task = self.ai_spot_setup()
        task["reviews"][1]["reviewer_type"] = "ai_model"
        self.assertTrue(self.blockers(task))

    def test_ai_check_from_building_session_refused(self):
        task = self.ai_spot_setup()
        task["reviews"][0]["review_session"] = "build-1"
        self.assertTrue(self.blockers(task))

    def test_held_out_needs_independent_review(self):
        task = self.ai_spot_setup(split="test")
        self.assertTrue(any("held-out" in r for r in self.blockers(task)))
        stamp = task["reviews"][0]["review_digest"]
        extra = {"scope": "independent_evaluation", "reviewer": "claude-x", "reviewer_type": "ai_model",
                 "model": "claude-x", "model_family": "Claude", "decision": "approved",
                 "review_digest": stamp, "date": "2026-11-12", "notes": "SYNTHETIC"}
        task["reviews"].append(extra)
        self.assertTrue(any("held-out" in r for r in self.blockers(task)))
        task["reviews"][-1] = dict(extra, model="other-x", model_family="Other")
        self.assertEqual(self.blockers(task), [])

    def test_old_full_human_review_still_accepted(self):
        task = self.approve_for_test()
        self.assertEqual(self.blockers(task), [])

    def test_stale_digest_refused_for_ai_path(self):
        task = self.ai_spot_setup()
        task["revision"] = task["revision"] + 1
        self.assertTrue(self.blockers(task))

    def test_real_pilot_valid_but_no_release(self):
        self.assertEqual(p.validate(self.corpus, self.sources), [])
        with self.assertRaisesRegex(ValueError, "No eligible tasks"):
            p.build(self.corpus, self.sources)

    def test_preview_deterministic_and_marked(self):
        first = p.build(self.corpus, self.sources, preview=True)
        self.assertEqual(first, p.build(copy.deepcopy(self.corpus), self.sources, preview=True))
        self.assertNotIn("train.jsonl", first)
        rows = [json.loads(line) for line in first["review-preview.jsonl"].splitlines()]
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(r["preview_only"] and r["release_blockers"] for r in rows))

    def test_literature_explanation_can_pass_without_simulation(self):
        task = self.approve_for_test()
        self.assertFalse(task["target"]["run_ids"])
        files = p.build(self.corpus, self.sources)
        self.assertEqual(len(files["train.jsonl"].splitlines()), 1)
        self.assertEqual(len(json.loads(files["manifest.json"])["excluded"]), 2)

    def test_accepted_flag_alone_never_suffices(self):
        self.corpus["tasks"][0]["status"] = "accepted"
        self.assertTrue(any("human engineering" in e for e in p.validate(self.corpus, self.sources)))

    def test_agent_is_not_human_review(self):
        task = self.approve_for_test()
        for review in task["reviews"]:
            review["reviewer_type"] = "agent"
        self.assertTrue(p.validate(self.corpus, self.sources))

    def test_target_edit_invalidates_review(self):
        task = self.approve_for_test()
        task["target"]["answer"] += " Extra assertion."
        self.assertTrue(any("current human" in e for e in p.validate(self.corpus, self.sources)))

    def test_linked_evidence_edit_invalidates_review(self):
        self.approve_for_test()
        next(e for e in self.corpus["evidence"] if e["id"] == "ea-cooling")["claim"] += " Changed."
        self.assertTrue(any("current human" in e for e in p.validate(self.corpus, self.sources)))

    def test_source_rights_change_invalidates_review(self):
        self.approve_for_test()
        self.sources["piotrowski-kubica-2021"]["rights_status"] = "reference_only"
        self.assertTrue(any("not eligible" in e for e in p.validate(self.corpus, self.sources)))

    def test_numeric_claim_cannot_use_literature_gate(self):
        task = self.corpus["tasks"][0]
        task["claim_scope"] = "numerical_benchmark"
        self.approve_for_test()
        self.assertTrue(any("no executed run" in e for e in p.validate(self.corpus, self.sources)))

    def test_family_cannot_cross_splits(self):
        self.corpus["groups"][0]["split"] = "train"
        group = copy.deepcopy(self.corpus["groups"][0])
        group.update(id="same-family-test", split="test")
        self.corpus["groups"].append(group)
        self.assertTrue(any("split leakage" in e for e in p.validate(self.corpus, self.sources)))

    def test_selection_input_rejects_known_answer_evidence(self):
        self.corpus["tasks"][1]["input"]["evidence_ids"] = ["ea-extraction"]
        self.assertTrue(any("target-revealing" in e for e in p.validate(self.corpus, self.sources)))

    def test_unknown_reference_fails(self):
        self.corpus["tasks"][0]["target"]["evidence_ids"].append("nonexistent")
        self.assertTrue(any("unknown evidence" in e for e in p.validate(self.corpus, self.sources)))

    def test_run_cannot_silently_change_process_family(self):
        self.corpus["runs"][0]["family"] = "unrelated-process"
        self.assertTrue(any("run family differs" in e for e in p.validate(self.corpus, self.sources)))

    def test_quantity_requires_units_and_basis(self):
        quantity = next(e for e in self.corpus["evidence"] if e["quantities"])["quantities"][0]
        del quantity["unit"]
        self.assertTrue(any("schema" in e for e in p.validate(self.corpus, self.sources)))

    def test_duplicate_id_fails(self):
        self.corpus["evidence"].append(copy.deepcopy(self.corpus["evidence"][0]))
        self.assertTrue(p.validate(self.corpus, self.sources))

    def test_artifact_tampering_fails(self):
        self.corpus["runs"][0]["calls"][0]["response"]["sha256"] = "0" * 64
        self.assertTrue(any("hash mismatch" in e for e in p.validate(self.corpus, self.sources)))

    def test_artifact_path_traversal_fails(self):
        self.corpus["runs"][0]["calls"][0]["request"]["path"] = "../outside.json"
        self.assertTrue(any("escapes repository" in e for e in p.validate(self.corpus, self.sources)))

    def test_replay_preserves_actual_response_and_links(self):
        task = self.corpus["tasks"][2]
        row = p.render(task, p.indexes(self.corpus))
        call, observed = row["messages"][2:4]
        self.assertEqual(call["tool_calls"][0]["id"], observed["tool_call_id"])
        path = self.corpus["runs"][0]["calls"][0]["response"]["path"]
        self.assertEqual(json.loads(observed["content"]), p.read_json(ROOT / path))
        self.assertIn("warnings", observed["content"])

    def test_evaluation_inputs_hide_answer_and_future_observation(self):
        task = self.approve_for_test(index=2, split="test")
        files = p.build(self.corpus, self.sources)
        row = json.loads(files["test.inputs.jsonl"])
        self.assertEqual([m["role"] for m in row["messages"]], ["system", "user"])
        self.assertNotIn(task["target"]["answer"], files["test.inputs.jsonl"])
        self.assertNotIn("chepta_result", files["test.inputs.jsonl"])
        self.assertIn("test.targets.jsonl", files)

    def test_nonfinite_json_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text('{"value": NaN}')
            with self.assertRaisesRegex(ValueError, "Non-finite"):
                p.read_json(path)


if __name__ == "__main__":
    unittest.main()
