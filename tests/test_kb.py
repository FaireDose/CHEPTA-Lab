"""Knowledge-base tests (docs/proposals/0003-knowledge-base.md). Changes exist only in memory or in temp folders."""
import contextlib
import copy
import importlib.util
import io
import json
import re
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

    # The case decisions that existed before the plants were backfilled (proposal 0003's examples).
    EXAMPLE_CASES = {EXAMPLE, "ethyl-acetate-piotrowski-2021.product-column-acid-below-paper-flow",
                     "ea-choose-extraction", "ea-condition-feed", "ea-purification-constraints"}

    def only_example_rules(self):
        """Keep the example case decisions and the two example rules, so exact index lines do not depend on
        how many literature rules or backfilled plant rows are committed."""
        self.corpus["decisions"] = [d for d in self.corpus["decisions"]
                                    if d["id"] in self.EXAMPLE_CASES or d["id"] in (self.RULE, self.SIM)]

    # --- the repository as committed ---

    def test_committed_records_are_valid(self):
        self.assertEqual(p.validate(self.corpus, self.sources), [])
        self.assertEqual(self.errors(), [])

    def test_index_is_current(self):
        # Fails whenever records or the register change without `python scripts/kb.py index`.
        self.assertEqual(kb.index_errors(self.corpus, self.origins), [])

    def pages(self):
        return kb.build_pages(self.corpus, self.origins)

    def test_readable_pages_for_people(self):
        pages = self.pages()
        for path, text in pages.items():  # all current; index_errors also checks them
            self.assertEqual(path.read_text(), text, path)
        # A row without plain fields keeps the one-line rendering.
        rule = copy.deepcopy(self.decision(self.SIM))
        del rule["keys"]["plain"]
        line = kb.readable_line(rule, p.indexes(self.corpus), self.sources)
        self.assertTrue(line.startswith(f"- **{rule['keys']['statement']}** lead, book or review; Kooijman & Taylor 2006, "))
        self.assertTrue(line.endswith(f"<!-- {rule['id']} -->"))
        self.assertIn("When: rigorous column.", line)
        # Row ids never appear in visible text, only in HTML comments.
        ids = {d["id"] for d in self.corpus["decisions"]}
        for text in pages.values():
            self.assertNotIn("<sub>", text)
            for l in text.splitlines():
                visible = re.sub(r"<!--.*?-->", "", l)
                self.assertFalse(any(i in visible for i in ids if "." in i), l)
        self.assertIn("rules-readable.md", kb.build_index(self.corpus, self.origins)[0].splitlines()[2])
        # A stale page, a missing page or a leftover page is reported, and held-out rows never appear.
        self.decision(self.SIM)["keys"]["plain"]["title"] = "Changed for the test"
        self.assertTrue(any("rules/column-convergence.md is stale" in e for e in kb.index_errors(self.corpus, self.origins)))
        with tempfile.TemporaryDirectory() as tmp:
            old = (kb.RULES_DIR, kb.PLANTS_DIR)
            kb.RULES_DIR, kb.PLANTS_DIR = Path(tmp) / "rules", Path(tmp) / "plants"
            try:
                self.assertTrue(all(not p_.is_file() for p_ in kb.page_errors(self.corpus, self.origins)
                                    if p_ != kb.INDEX_READABLE))
                kb.RULES_DIR.mkdir()
                (kb.RULES_DIR / "old-topic.md").write_text("left over")
                self.assertIn(kb.RULES_DIR / "old-topic.md", kb.page_errors(self.corpus, self.origins))
            finally:
                kb.RULES_DIR, kb.PLANTS_DIR = old
        self.corpus["groups"].append({"id": "chemsep-book", "family": "chemsep-book",
                                      "source_ids": ["kooijman-taylor-2006-chemsep-book"], "split": "test"})
        self.assertFalse(any(self.SIM in t for t in self.pages().values()))

    def test_front_page_is_short_and_lists_every_page(self):
        pages = self.pages()
        front = pages[kb.INDEX_READABLE]
        self.assertLessEqual(len(front.splitlines()), 40)
        for path in pages:
            if path != kb.INDEX_READABLE:
                self.assertIn(f"({path.parent.name}/{path.name})", front)

    def test_every_rule_on_exactly_one_topic_page_and_pages_stay_short(self):
        pages = self.pages()
        rules = [d for d in kb.visible_decisions(self.corpus)[0] if d["keys"]["kind"] in kb.RULE_KINDS]
        topic_pages = {path: text for path, text in pages.items() if path.parent == kb.RULES_DIR}
        for d in rules:
            on = [path for path, text in topic_pages.items() if f"<!-- {d['id']} -->" in text]
            self.assertEqual(len(on), 1, d["id"])
            if d["keys"].get("plain"):
                self.assertEqual(on[0].stem, kb.topic_of(d))
        self.assertNotIn(kb.RULES_DIR / "other.md", pages)  # no rule falls through the topics
        for path, text in topic_pages.items():
            self.assertLessEqual(text.count("\n- **"), kb.TOPIC_MAX, path)
        # Best-supported first.
        order = {s: i for i, s in enumerate(kb.STATUSES_SHOWN)}
        for path, text in topic_pages.items():
            on = sorted((text.index(f"<!-- {d['id']} -->"), order[d["keys"]["outcome"]["status"]])
                        for d in rules if f"<!-- {d['id']} -->" in text)
            ranks = [r for _, r in on]
            self.assertEqual(ranks, sorted(ranks), path)

    def test_case_decisions_only_on_plant_pages_grouped_by_unit(self):
        pages = self.pages()
        cases = [d for d in kb.visible_decisions(self.corpus)[0] if d["keys"]["kind"] == "case-decision"]
        for d in cases:
            on = [path for path, text in pages.items() if f"<!-- {d['id']} -->" in text]
            self.assertEqual(on, [kb.PLANTS_DIR / f"{self.origins[d['id']]}.md"], d["id"])
        page = pages[kb.PLANTS_DIR / "ethyl-acetate-piotrowski-2021.md"]
        self.assertIn("Run log of the plant, not yet written as lessons.", page)
        self.assertIn("## distillation (", page)

    # --- plain fields for people ---

    def test_plain_rule_renders_title_fields_status_and_source(self):
        rule = self.decision(self.SIM)
        plain = rule["keys"]["plain"]
        page = self.pages()[kb.RULES_DIR / "column-convergence.md"].splitlines()
        i = page.index(f"- **{plain['title']}**")
        block = page[i:i + 7]
        self.assertEqual([l.split(":")[0] for l in block[1:]],
                         ["  - When", "  - Do", "  - Why", "  - Check", "  - Status", "  - Source"])
        self.assertEqual(block[5], "  - Status: lead — from the literature, not yet tested by Lab.")
        self.assertTrue(block[6].startswith("  - Source: Kooijman & Taylor 2006, *The ChemSep Book, second edition* "
                                            "(https://www.chemsep.org/downloads/docs/book2.pdf), Sections 1.2-1.3"))
        self.assertIn("Lab has not reread the source for this summary.", block[6])
        self.assertTrue(block[6].endswith(f"<!-- {rule['id']} -->"))
        # A DOI becomes a link, and a result line is printed where there is one.
        row = self.decision("al-rabiah-2022.membrane-reactor-removes-water")
        text = kb.readable_line(row, p.indexes(self.corpus), self.sources)
        self.assertIn("(https://doi.org/10.3390/pr10091801)", text)
        self.assertIn(f"  - Result: {row['keys']['plain']['result']}", text)

    def test_every_literature_rule_outside_the_case_files_has_plain_fields(self):
        cases = {"pilot", "ethyl-acetate-piotrowski-2021", "methanol-co2-campos-2022"}
        missing = [d["id"] for d in self.corpus["decisions"] if d["keys"]["kind"] in kb.RULE_KINDS
                   and self.origins.get(d["id"]) not in cases and "plain" not in d["keys"]]
        self.assertEqual(missing, [])

    def test_rendered_plain_text_names_its_sources(self):
        page = "\n".join(self.pages().values())
        for line in page.splitlines():
            if line.startswith(("  - When", "  - Do", "  - Why", "  - Check", "  - Result")) or \
                    (line.startswith("- **") and not line.rstrip().endswith("-->")):
                self.assertIsNone(kb.BARE_REFERENCE.search(line), line)

    def test_plain_bare_reference_refused(self):
        plain = self.decision(self.SIM)["keys"]["plain"]
        plain["do"] = "Do what the paper says."
        self.assertTrue(any("without naming it" in e for e in self.errors()))
        plain["do"] = "Do what the paper (Kooijman & Taylor 2006, https://www.chemsep.org) says."
        self.assertFalse(any("without naming it" in e for e in self.errors()))
        plain["why"] = "The authors' reason."
        self.assertTrue(any("plain.why says" in e for e in self.errors()))

    def test_plain_number_must_come_from_the_row(self):
        plain = self.decision(self.SIM)["keys"]["plain"]
        plain["result"] = "Purity rose to 99.7 mol%."
        self.assertTrue(any("gives 99.7" in e for e in self.errors()))
        plain["note"] = "Lab reread p. 12 on 2026-11-20 (99.7 mol%)."  # a passage reread names the number
        self.assertFalse(any("gives 99.7" in e for e in self.errors()))
        plain["result"] = "CO2 and m3 are formulas and units, not numbers."
        self.assertFalse(any("gives" in e for e in self.errors()))

    def test_plain_no_ids_short_one_paragraph(self):
        plain = self.decision(self.SIM)["keys"]["plain"]
        plain["check"] = f"See {EXAMPLE}."
        self.assertTrue(any("names a row id" in e for e in self.errors()))
        plain["check"] = "Line one.\nLine two."
        self.assertTrue(any("one short paragraph" in e for e in self.errors()))
        plain["check"] = "x" * 451
        self.assertTrue(any("one short paragraph" in e for e in self.errors()))

    def test_plain_schema_requires_the_five_fields(self):
        plain = self.decision(self.SIM)["keys"]["plain"]
        del plain["check"]
        self.assertTrue(p.validate(self.corpus, self.sources))
        plain["check"], plain["extra"] = "Check it.", "not allowed"
        self.assertTrue(p.validate(self.corpus, self.sources))

    def test_index_size_follows_problems_not_rows(self):
        md, _ = kb.build_index(self.corpus, self.origins)
        before = md.splitlines()
        for i in range(500):
            self.clone(EXAMPLE, f"ethyl-acetate-piotrowski-2021.extra-{i}")
        after = kb.build_index(self.corpus, self.origins)[0].splitlines()
        self.assertEqual(len(after), len(before))
        self.assertLessEqual(sum(map(len, after)) - sum(map(len, before)), 10)  # only the counts grow

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
        self.only_example_rules()
        # The two example rows: failed at 140-141.5 kmol/h, worked at 139 kmol/h.
        self.assertEqual(kb.disputes(self.corpus["decisions"]), [])

    def test_same_conditions_different_outcome_is_disputed_and_listed(self):
        self.only_example_rules()
        self.clone(EXAMPLE, "other-case.same-column", status="worked")
        found = kb.disputes(self.corpus["decisions"])
        self.assertEqual(len(found), 1)
        self.assertEqual({r["id"] for r in found[0]["rows"]}, {EXAMPLE, "other-case.same-column"})
        self.assertTrue(any(e.startswith("disputed:") for e in self.errors()))
        # Nothing merged or deleted.
        self.assertEqual(sum(1 for d in self.corpus["decisions"] if d["id"] == EXAMPLE), 1)

    def test_dispute_acknowledged_by_one_side_passes_and_stays_listed(self):
        self.only_example_rules()
        row = self.clone(EXAMPLE, "other-case.same-column", status="worked")
        row["keys"]["disputed_with"] = [EXAMPLE]
        self.assertEqual(self.errors(), [])
        self.assertEqual(len(kb.disputes(self.corpus["decisions"])), 1)
        md, _ = kb.build_index(self.corpus, self.origins)
        line = next(l for l in md.splitlines() if l.startswith("| sep-two-liquids-with-acetic-acid"))
        self.assertIn("| 1 |", line)

    def test_later_engine_adds_a_row_and_supersedes(self):
        self.only_example_rules()
        row = self.clone(EXAMPLE, "ethyl-acetate-piotrowski-2021.product-column-acid-at-paper-flow-0.7.0",
                         status="worked", engine="chepta@0.7.0", run_ids=["ethanol-replay-038"])
        self.assertEqual(kb.disputes(self.corpus["decisions"]), [])
        self.assertEqual(kb.current_rows([self.decision(EXAMPLE), row]), [row])

    def test_paper_and_chepta_disagreeing_is_disputed(self):
        self.only_example_rules()
        row = self.clone(EXAMPLE, "other-case.paper-says-worked", status="worked", basis="paper_simulation",
                         engine=None, run_ids=[])
        self.assertEqual(len(kb.disputes(self.corpus["decisions"])), 1)
        self.assertIn(row["id"], {r["id"] for r in kb.disputes(self.corpus["decisions"])[0]["rows"]})

    def test_acknowledged_pair_between_leads_is_counted(self):
        self.only_example_rules()
        a = self.clone(self.RULE, "ethyl-acetate-piotrowski-2021.rule-a")
        b = self.clone(self.RULE, "ethyl-acetate-piotrowski-2021.rule-b")
        del a["keys"]["problem_id"], a["keys"]["level"], b["keys"]["problem_id"], b["keys"]["level"]
        self.assertEqual(kb.disputes(self.corpus["decisions"]), [])  # two leads alone are not a dispute
        a["keys"]["disputed_with"] = [b["id"]]
        self.assertEqual(self.errors(), [])
        found = kb.disputes(self.corpus["decisions"])
        self.assertEqual([f["acknowledged_pairs"] for f in found], [[(a["id"], b["id"])]])
        self.assertEqual(found[0]["unacknowledged_pairs"], [])
        md, js = kb.build_index(self.corpus, self.origins)
        line = next(l for l in md.splitlines() if l.startswith("| extractive-distillation |"))
        self.assertIn("| 0/0/2/0 | 1 |", line)
        # A pair naming each other across different conditions still counts once, under the first row.
        b["keys"]["conditions"] = b["keys"]["conditions"] + ["other-condition"]
        found = kb.disputes(self.corpus["decisions"])
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["acknowledged_pairs"], [(a["id"], b["id"])])

    def test_committed_lead_disputes_are_listed(self):
        pairs = {p for f in kb.disputes(self.corpus["decisions"]) for p in f["acknowledged_pairs"]}
        self.assertIn(("li-2023-distillation-sequences.hardest-split-last",
                       "li-2023-distillation-sequences.hardest-split-not-always-last"), pairs)
        self.assertIn(("larsson-skogestad-2000-plantwide.fix-a-recycle-flow",
                       "larsson-skogestad-2000-plantwide.keep-reactor-full"), pairs)

    def test_editing_or_deleting_a_chepta_outcome_fails(self):
        lock = kb.lock_entries(self.corpus)
        self.decision(EXAMPLE)["keys"]["outcome"]["status"] = "worked"
        self.assertTrue(any("edited" in e for e in kb.lock_errors(self.corpus, lock)))
        self.corpus["decisions"] = [d for d in self.corpus["decisions"] if d["id"] != EXAMPLE]
        self.assertTrue(any("deleted" in e for e in kb.lock_errors(self.corpus, lock)))

    # --- row kinds, textbook basis, symptoms (amendment of 2026-11-20) ---

    SIM = "kooijman-taylor-2006-chemsep-book.column-misses-target-check-balances-and-profiles"
    RULE = "ethyl-acetate-piotrowski-2021.review-extractive-distillation-needs-second-step"

    def test_committed_rule_rows_have_their_kinds(self):
        self.assertEqual(self.decision(self.SIM)["keys"]["kind"], "simulation-rule")
        self.assertEqual(self.decision(self.RULE)["keys"]["outcome"]["basis"], "textbook")

    def test_case_decision_needs_problem_and_evidence(self):
        k = self.decision("ea-choose-extraction")["keys"]
        del k["problem_id"]
        self.decision("ea-choose-extraction")["evidence_ids"] = []
        found = " ".join(self.errors())
        self.assertIn("names its register problem_id", found)
        self.assertIn("cites evidence", found)

    def test_simulation_rule_keyed_by_symptom_not_problem(self):
        k = self.decision(self.SIM)["keys"]
        k["problem_id"], k["level"] = "sep-ester-alcohol-water-azeotrope", "separation"
        self.assertTrue(any("does not belong to a register problem" in e for e in self.errors()))
        del k["problem_id"], k["level"], k["symptom"]
        self.assertTrue(any("keyed by operation and symptom" in e for e in self.errors()))

    def test_unknown_symptom_and_kind_refused(self):
        k = self.decision(self.SIM)["keys"]
        k["symptom"], k["kind"] = "stuck", "tip"
        found = " ".join(self.errors())
        self.assertIn("unknown symptom 'stuck'", found)
        self.assertIn("unknown row kind 'tip'", found)

    def test_rule_without_results_cannot_claim_worked(self):
        self.decision(self.RULE)["keys"]["outcome"]["status"] = "worked"
        self.assertTrue(any("without results of its own is a lead" in e for e in self.errors()))

    def test_textbook_basis_only_for_rules(self):
        self.decision("ea-choose-extraction")["keys"]["outcome"]["basis"] = "textbook"
        self.assertTrue(any("not a textbook rule" in e for e in self.errors()))
        self.decision(self.SIM)["keys"]["outcome"]["basis"] = "lab_inference"
        self.assertTrue(any("rule row has basis textbook" in e for e in self.errors()))

    def test_query_by_symptom_and_kind(self):
        code, out = self.run_kb("query", "--operation", "distillation", "--symptom", "purity-short")
        self.assertIn(self.SIM, out)
        self.assertNotIn(EXAMPLE, out)
        code, out = self.run_kb("query", "--kind", "design-rule", "--json", "--limit", "1000")
        rows = json.loads(out)
        self.assertIn(self.RULE, [r["id"] for r in rows])
        self.assertTrue(rows and all(r["keys"]["kind"] == "design-rule" for r in rows))

    def test_index_has_one_line_per_operation_and_symptom(self):
        self.only_example_rules()
        md, js = kb.build_index(self.corpus, self.origins)
        self.assertIn("| distillation | purity-short |", md)
        before = md.splitlines()
        for i in range(200):
            self.clone(self.SIM, f"kooijman-taylor-2006-chemsep-book.extra-{i}")
        after = kb.build_index(self.corpus, self.origins)[0].splitlines()
        self.assertEqual(len(after), len(before))
        row = copy.deepcopy(self.decision(self.SIM))
        row["id"], row["keys"]["symptom"] = "kooijman-taylor-2006-chemsep-book.slow", "slow"
        self.corpus["decisions"].append(row)
        self.assertEqual(len(kb.build_index(self.corpus, self.origins)[0].splitlines()), len(before) + 1)

    def test_general_design_rule_without_problem_goes_to_its_own_section(self):
        self.only_example_rules()
        k = self.decision(self.RULE)["keys"]
        del k["problem_id"], k["level"]
        self.assertEqual(self.errors(), [])
        md, _ = kb.build_index(self.corpus, self.origins)
        self.assertIn("| extractive-distillation | azeotrope-min-boiling | 0/0/1/0 |", md)
        k["behaviours"] = []
        self.assertTrue(any("names the behaviours" in e for e in self.errors()))

    # --- usefulness: informed_by on the using row, shown as used_in of the rule ---

    def use(self, helped="yes", note="SYNTHETIC UNIT TEST ONLY"):
        k = self.decision(EXAMPLE)["keys"]
        k.setdefault("informed_by", []).append({"row": self.SIM, "helped": helped, "note": note})
        return k

    def test_used_in_derived_and_counted(self):
        self.only_example_rules()
        self.use("yes")
        self.use("partly")
        self.assertEqual(self.errors(), [])
        uses = kb.used_in(self.corpus["decisions"], self.origins)[self.SIM]
        self.assertEqual([(u["case"], u["row"], u["helped"]) for u in uses],
                         [("ethyl-acetate-piotrowski-2021", EXAMPLE, "yes"),
                          ("ethyl-acetate-piotrowski-2021", EXAMPLE, "partly")])
        md, _ = kb.build_index(self.corpus, self.origins)
        self.assertIn("| distillation | purity-short | 0/0/1/0 | 0 | 1 | 1/1/0 |", md)
        code, out = self.run_kb("show", self.SIM)
        self.assertEqual(json.loads(out)["used_in"], [])  # the committed records have no uses yet

    def test_informed_by_unknown_row_refused(self):
        self.use()["informed_by"][0]["row"] = "no-such-row"
        self.assertTrue(any("informed_by names unknown row" in e for e in self.errors()))

    def test_informed_by_is_append_only(self):
        k = self.use("yes")
        lock = kb.lock_entries(self.corpus)
        self.use("no")  # appending is fine
        self.assertEqual(kb.lock_errors(self.corpus, lock), [])
        k["informed_by"][0]["helped"] = "partly"
        self.assertTrue(any("append-only" in e for e in kb.lock_errors(self.corpus, lock)))
        k["informed_by"] = []
        del k["informed_by"]
        self.assertTrue(any("append-only" in e for e in kb.lock_errors(self.corpus, lock)))

    # --- rights: short paraphrase, catalogued source ---

    def test_statement_without_source_refused(self):
        k = self.decision("ea-choose-extraction")["keys"]
        k["statement"] = "Wash the azeotrope with water."
        self.assertTrue(any("statement needs its source" in e for e in self.errors()))

    def test_long_statement_refused(self):
        k = self.decision(self.SIM)["keys"]
        k["statement"] = "First sentence. Second sentence. Third sentence."
        self.assertTrue(any("longer than 2 sentences" in e for e in self.errors()))
        k["statement"] = "x" * 301
        self.assertTrue(any("300 characters" in e for e in self.errors()))

    def test_quoted_text_refused(self):
        k = self.decision(self.SIM)["keys"]
        k["statement"] = 'The book says "check the balances and then compare every stage profile carefully".'
        self.assertTrue(any("paraphrase instead of copying" in e for e in self.errors()))

    def test_rule_source_must_be_catalogued(self):
        k = self.decision(self.SIM)["keys"]
        k["source"]["source_id"] = "some-uncatalogued-book"
        self.assertTrue(any("must be in data/sources.json" in e for e in self.errors()))
        del k["source"]
        self.assertTrue(any("has a source" in e for e in self.errors()))

    def test_rule_from_a_held_out_source_is_hidden(self):
        self.only_example_rules()
        self.corpus["groups"].append({"id": "chemsep-book", "family": "chemsep-book",
                                      "source_ids": ["kooijman-taylor-2006-chemsep-book"], "split": "test"})
        self.assertIn(self.SIM, kb.held_out(self.corpus))
        md, _ = kb.build_index(self.corpus, self.origins)
        self.assertNotIn("purity-short", md)

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
        self.only_example_rules()
        group = next(g for g in self.corpus["groups"] if g["id"] == "ethyl-acetate")
        group["split"] = "test"
        hidden = kb.held_out(self.corpus)
        self.assertIn(EXAMPLE, hidden)
        self.assertIn("ea-azeotrope", hidden)
        md, js = kb.build_index(self.corpus, self.origins)
        self.assertNotIn("ethyl-acetate-piotrowski-2021", md + js)
        self.assertNotIn(EXAMPLE, json.dumps(kb.lock_entries(self.corpus)))
        self.assertTrue(all(p["rows"] == 0 for p in json.loads(js)["problems"]))
        # Only the book's simulation rule stays visible: its source is in no test group.
        self.assertEqual([d["id"] for d in kb.visible_decisions(self.corpus)[0]], [self.SIM])

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
        code, out = self.run_kb("query", "--components", "benzene")
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
