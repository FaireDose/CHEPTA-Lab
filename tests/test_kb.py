"""Knowledge-base tests (docs/proposals/0003-knowledge-base.md). Changes exist only in memory or in temp folders."""
import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("kb", ROOT / "scripts/kb.py")
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)
p = kb.pipeline

EXAMPLE = "ethyl-acetate-piotrowski-2021.product-column-acid-at-paper-flow"


class KnowledgeBaseTests(unittest.TestCase):
    def setUp(self):
        self.corpus, self.origins = p.load_records()
        self.sources = {s["id"]: s for s in p.read_json(ROOT / "data/sources.json")["sources"]}

    def decision(self, key):
        return next(d for d in self.corpus["decisions"] if d["id"] == key)

    def clone(self, key, new_id, **outcome):
        row = copy.deepcopy(self.decision(key))
        row["id"] = new_id
        row["keys"]["outcome"].update(outcome)
        self.corpus["decisions"].append(row)
        return row

    def errors(self):
        return kb.check_keys(self.corpus)

    # --- the repository as committed ---

    def test_committed_records_are_valid(self):
        self.assertEqual(p.validate(self.corpus, self.sources), [])
        self.assertEqual(self.errors(), [])

    def test_index_is_current(self):
        # Fails whenever records or the register change without `python scripts/kb.py index`.
        self.assertEqual(kb.index_errors(self.corpus, self.origins), [])

    def test_index_size_follows_problems_not_rows(self):
        md, _ = kb.build_index(self.corpus, self.origins)
        before = md.splitlines()
        for i in range(500):
            self.clone(EXAMPLE, f"ethyl-acetate-piotrowski-2021.extra-{i}")
        after = kb.build_index(self.corpus, self.origins)[0].splitlines()
        self.assertEqual(len(after), len(before))
        self.assertLessEqual(sum(map(len, after)) - sum(map(len, before)), 5)  # only the counts grow

    # --- vocabulary ---

    def test_unknown_behaviour_refused(self):
        self.decision(EXAMPLE)["keys"]["behaviours"].append("azeotrope")
        self.assertTrue(any("unknown behaviour 'azeotrope'" in e for e in self.errors()))

    def test_unknown_operation_component_status_refused(self):
        k = self.decision(EXAMPLE)["keys"]
        k["operation_type"] = "column"
        k["components"].append("ethyl acetate")
        k["outcome"]["status"] = "maybe"
        found = " ".join(self.errors())
        for term in ("operation type 'column'", "component 'ethyl acetate'", "outcome status 'maybe'"):
            self.assertIn(term, found)

    def test_problem_must_be_a_register_row_with_its_level(self):
        k = self.decision(EXAMPLE)["keys"]
        k["level"] = "plant"
        self.assertTrue(any("differs from the register" in e for e in self.errors()))
        k["problem_id"] = "sep-not-in-register"
        self.assertTrue(any("not a row of data/ISSUES_AND_ROUTES.md" in e for e in self.errors()))

    def test_register_ids_are_read_from_first_column(self):
        rows = kb.register_rows()
        self.assertIn("sep-ester-alcohol-water-azeotrope", rows)
        self.assertEqual(rows["plant-recycles-makeup-purge"], "plant")
        self.assertNotIn("id", rows)

    # --- outcome rules ---

    def test_chepta_outcome_names_engine_matching_results_folder(self):
        o = self.decision(EXAMPLE)["keys"]["outcome"]
        o["engine"] = "chepta@0.6.1"
        self.assertTrue(any("chepta 0.6.2 folder" in e for e in self.errors()))
        o["engine"] = None
        self.assertTrue(any("names its engine" in e for e in self.errors()))

    def test_lab_inference_cannot_claim_worked(self):
        o = self.decision("ea-choose-extraction")["keys"]["outcome"]
        o["basis"] = "lab_inference"
        self.assertTrue(any("Lab inference" in e for e in self.errors()))

    def test_run_must_exist(self):
        self.decision(EXAMPLE)["keys"]["outcome"]["run_ids"].append(
            "cases/ethyl-acetate-piotrowski-2021/results-chepta-0.6.2/no-such-run")
        self.assertTrue(any("no-such-run" in e for e in self.errors()))

    def test_objective_number_must_come_from_its_evidence(self):
        self.decision(EXAMPLE)["keys"]["objective"]["targets"][0]["value"] = 99.95
        self.assertTrue(any("no number without a source" in e for e in self.errors()))

    # --- conflicts ---

    def test_same_problem_operation_different_conditions_is_not_disputed(self):
        # The two example rows: failed at 140-141.5 kmol/h, worked at 139 kmol/h.
        self.assertEqual(kb.disputes(self.corpus["decisions"]), [])

    def test_same_conditions_different_outcome_is_disputed_and_listed(self):
        self.clone(EXAMPLE, "other-case.same-column", status="worked")
        found = kb.disputes(self.corpus["decisions"])
        self.assertEqual(len(found), 1)
        self.assertEqual({r["id"] for r in found[0]["rows"]}, {EXAMPLE, "other-case.same-column"})
        self.assertTrue(any(e.startswith("disputed:") for e in self.errors()))
        # Nothing merged or deleted.
        self.assertEqual(sum(1 for d in self.corpus["decisions"] if d["id"] == EXAMPLE), 1)

    def test_dispute_acknowledged_by_one_side_passes_and_stays_listed(self):
        row = self.clone(EXAMPLE, "other-case.same-column", status="worked")
        row["keys"]["disputed_with"] = [EXAMPLE]
        self.assertEqual(self.errors(), [])
        self.assertEqual(len(kb.disputes(self.corpus["decisions"])), 1)
        md, _ = kb.build_index(self.corpus, self.origins)
        line = next(l for l in md.splitlines() if l.startswith("| sep-two-liquids-with-acetic-acid"))
        self.assertIn("| 1 |", line)

    def test_later_engine_adds_a_row_and_supersedes(self):
        row = self.clone(EXAMPLE, "ethyl-acetate-piotrowski-2021.product-column-acid-at-paper-flow-0.7.0",
                         status="worked", engine="chepta@0.7.0", run_ids=["ethanol-replay-038"])
        self.assertEqual(kb.disputes(self.corpus["decisions"]), [])
        self.assertEqual(kb.current_rows([self.decision(EXAMPLE), row]), [row])

    def test_paper_and_chepta_disagreeing_is_disputed(self):
        row = self.clone(EXAMPLE, "other-case.paper-says-worked", status="worked", basis="paper_simulation",
                         engine=None, run_ids=[])
        self.assertEqual(len(kb.disputes(self.corpus["decisions"])), 1)
        self.assertIn(row["id"], {r["id"] for r in kb.disputes(self.corpus["decisions"])[0]["rows"]})

    def test_editing_or_deleting_a_chepta_outcome_fails(self):
        lock = {"rows": kb.lock_entries(self.corpus)}
        self.decision(EXAMPLE)["keys"]["outcome"]["status"] = "worked"
        self.assertTrue(any("edited" in e for e in kb.lock_errors(self.corpus, lock)))
        self.corpus["decisions"] = [d for d in self.corpus["decisions"] if d["id"] != EXAMPLE]
        self.assertTrue(any("deleted" in e for e in kb.lock_errors(self.corpus, lock)))

    # --- files and namespaces ---

    def write(self, folder, name, rows, **extra):
        doc = {"schema_version": 1, "id": name, "groups": [], "blocks": [], "evidence": [], "decisions": rows,
               "runs": [], "tasks": []}
        doc.update(extra)
        (folder / f"{name}.json").write_text(json.dumps(doc))

    def test_loader_merges_files_and_enforces_namespace(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "pilot.json").write_text((ROOT / "dataset/records/pilot.json").read_text())
            row = copy.deepcopy(self.decision(EXAMPLE))
            row["id"] = "case-a.row"
            self.write(folder, "case-a", [row])
            corpus, origins = p.load_records(folder)
            self.assertEqual(origins["case-a.row"], "case-a")
            self.assertEqual(origins["ea-condition-feed"], "pilot")
            self.assertEqual(corpus["tasks"][0]["id"], p.read_json(ROOT / "dataset/records/pilot.json")["tasks"][0]["id"])
            row2 = copy.deepcopy(row)
            row2["id"] = "case-a.other"
            self.write(folder, "case-b", [row2])
            with self.assertRaisesRegex(ValueError, "must start with 'case-b.'"):
                p.load_records(folder)
            self.write(folder, "case-b", [], id="wrong")
            with self.assertRaisesRegex(ValueError, "id must be the file name"):
                p.load_records(folder)

    # --- held-out groups ---

    def test_held_out_rows_never_reach_index_or_query(self):
        group = next(g for g in self.corpus["groups"] if g["id"] == "ethyl-acetate")
        group["split"] = "test"
        hidden = kb.held_out(self.corpus)
        self.assertIn(EXAMPLE, hidden)
        self.assertIn("ea-azeotrope", hidden)
        md, js = kb.build_index(self.corpus, self.origins)
        self.assertNotIn("ethyl-acetate-piotrowski-2021", md + js)
        self.assertNotIn(EXAMPLE, json.dumps(kb.lock_entries(self.corpus)))
        self.assertTrue(all(p["rows"] == 0 for p in json.loads(js)["problems"]))
        self.assertEqual(kb.visible_decisions(self.corpus)[0], [])

    # --- query ---

    def run_kb(self, *argv):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = kb.main(list(argv))
        return code, out.getvalue()

    def test_query_filters_and_prints_compact_rows(self):
        code, out = self.run_kb("query", "--behaviour", "associating-acid-vapour", "--status", "failed")
        self.assertEqual(code, 0)
        self.assertIn(EXAMPLE, out)
        self.assertNotIn("below-paper-flow", out)
        self.assertIn("piotrowski-kubica-2021: Section 3.4", out)
        code, out = self.run_kb("query", "--components", "ethanol,water", "--status", "worked", "--json")
        ids = {r["id"] for r in json.loads(out)}
        self.assertIn("ea-choose-extraction", ids)
        self.assertNotIn(EXAMPLE, ids)
        code, out = self.run_kb("query", "--components", "methanol")
        self.assertIn("No matching rows", out)

    def test_problems_prints_only_matching_index_lines(self):
        code, out = self.run_kb("problems", "--behaviour", "associating-acid-vapour")
        self.assertIn("| sep-two-liquids-with-acetic-acid |", out)
        self.assertNotIn("| sep-ester-alcohol-water-azeotrope |", out)

    def test_show_gives_row_and_locators(self):
        code, out = self.run_kb("show", "ea-purification-constraints")
        data = json.loads(out)
        self.assertEqual(data["file"], "dataset/records/pilot.json")
        self.assertTrue(data["evidence"][0]["locators"])


if __name__ == "__main__":
    unittest.main()
