"""The engine pin in data/upstream.json must match package.json and package-lock.json."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("catalog", ROOT / "scripts/validate_catalog.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
load = lambda name: json.loads((ROOT / name).read_text())


class PinTests(unittest.TestCase):
    def setUp(self):
        self.up, self.pkg, self.lock = load("data/upstream.json"), load("package.json"), load("package-lock.json")

    def test_repository_pin_is_consistent(self):
        self.assertEqual(v.validate_pin(self.up, self.pkg, self.lock), [])

    def test_range_instead_of_exact_version_is_refused(self):
        pkg = copy.deepcopy(self.pkg)
        pkg["dependencies"]["chepta"] = "^" + self.up["pin"]["version"]
        self.assertTrue(v.validate_pin(self.up, pkg, self.lock))

    def test_integrity_mismatch_is_refused(self):
        lock = copy.deepcopy(self.lock)
        lock["packages"]["node_modules/chepta"]["integrity"] = "sha512-wrong"
        self.assertTrue(v.validate_pin(self.up, self.pkg, lock))

    def test_missing_pin_or_history_is_refused(self):
        up = copy.deepcopy(self.up)
        del up["history"]
        self.assertTrue(v.validate_pin(up, self.pkg, self.lock))
        del up["pin"]
        self.assertTrue(v.validate_pin(up, self.pkg, self.lock))

    def test_old_commit_remains_in_history(self):
        self.assertIn(self.up["commit"], [h.get("commit") for h in self.up["history"]])


if __name__ == "__main__":
    unittest.main()
