#!/usr/bin/env python3
"""Run the B2 column (benzene + toluene, The ChemSep Book, sections 1.2-1.3) on the pinned npm package chepta@0.6.2
through its command line (`npx chepta request <file>`), as an assistant would. results-chepta-0.6.1/ is not touched.

Runs:
  b2-pr, b2-record-thermo-literal, b2-distillate-purity   all six 0.6.1 requests, copied byte for byte from
                           results-chepta-0.6.1/ (the same requests, to see what changed). The last one uses the
                           key `distillate_purity` inside `column`, as the 0.6.0 attempt did.
  b2-purity-spec           new: the purity as 0.6.2's documentation gives it, column.specifications
                           [{kind: "purity", product: "distillate", component: benzene, value: published x_D}] with the
                           reflux ratio 2 kept and the bottoms flow left open (the 0.6.0 request, in the new form)
  b2-bottoms-purity-spec   new: bottoms toluene purity = published x_B(toluene), reflux ratio 2 kept
  b2-recovery-spec         new: benzene recovery in the distillate = published d(benzene) / feed benzene, reflux 2 kept
Values come from CHEPTA's record (copied unchanged to upstream/); no number is typed here. Every output is kept,
refusals included. Usage (repository root, after `npm ci`): python3 cases/benzene-toluene-chemsep-b2/run_chepta_0.6.2.py
"""
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
OLD = H / "results-chepta-0.6.1"
OUT = H / "results-chepta-0.6.2"
RECORD = H / "upstream/B2-chemsep-benzene-toluene.json"
EXIT = {0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}
REUSED = ["b2-pr", "b2-record-thermo-literal", "b2-distillate-purity", "b2-purity-spec", "b2-bottoms-purity-spec", "b2-recovery-spec"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def new_requests(rec):
    base = json.loads((OLD / "b2-pr.request.json").read_text())
    comps, pub = rec["components"], rec["published"]
    feed_benzene = base["input"]["feed"]["flow_kmol_h"][comps[0]]
    out = {}

    def variant(spec):
        r = json.loads(json.dumps(base))
        del r["input"]["column"]["bottoms_kmol_h"]
        r["input"]["column"]["specifications"] = [spec]
        return r
    out["b2-purity-spec"] = variant({"kind": "purity", "product": "distillate", "component": comps[0],
                                     "value": pub["x_D"][0]})
    out["b2-bottoms-purity-spec"] = variant({"kind": "purity", "product": "bottoms", "component": comps[1],
                                             "value": pub["x_B"][1]})
    out["b2-recovery-spec"] = variant({"kind": "recovery", "product": "distillate", "component": comps[0],
                                       "value": pub["d_mol_s"][0] * 3.6 / feed_benzene})  # mol/s x 3.6 = kmol/h
    return out


def main():
    OUT.mkdir(exist_ok=True)
    lock = json.loads((ROOT / "package-lock.json").read_text())["packages"]["node_modules/chepta"]
    version = subprocess.run(["npx", "chepta", "--version"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if version != "0.6.2" or lock["version"] != "0.6.2":
        sys.exit(f"Expected chepta 0.6.2, found CLI {version} / lock {lock['version']}")
    rec = json.loads(RECORD.read_text())
    todo = []
    for rid in REUSED:
        req = OUT / f"{rid}.request.json"
        shutil.copyfile(OLD / f"{rid}.request.json", req)
        todo.append((rid, req, True))
    runs = []
    for rid, req, reused in todo:
        rel = req.relative_to(ROOT)
        p = subprocess.run(["npx", "chepta", "request", str(rel)], cwd=ROOT, capture_output=True, text=True)
        (OUT / f"{rid}.output.json").write_text(p.stdout)
        (OUT / f"{rid}.stderr.txt").write_text(p.stderr)
        result = json.loads(p.stdout) if p.stdout.strip() else {}
        runs.append({"id": rid, "command": f"npx chepta request {rel}", "exit_code": p.returncode,
                     "exit_meaning": EXIT.get(p.returncode, "unknown"), "outcome": result.get("outcome"),
                     "error": result.get("error"), "request_identical_to_0.6.1": reused,
                     "request_file": f"results-chepta-0.6.2/{rid}.request.json",
                     "output_file": f"results-chepta-0.6.2/{rid}.output.json",
                     "stderr_file": f"results-chepta-0.6.2/{rid}.stderr.txt",
                     "request_file_sha256": sha(req.read_bytes()), "output_file_sha256": sha(p.stdout.encode())})
    manifest = {
        "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "engine": {"package": "chepta", "version": version, "resolved": lock["resolved"],
                   "integrity": lock["integrity"], "licence": lock.get("license")},
        "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
        "npm": subprocess.run(["npm", "--version"], capture_output=True, text=True).stdout.strip(),
        "interface": "command line: npx chepta request <file>; exit codes 0 ok, 2 invalid_input, 3 missing_data, "
                     "4 unsupported, 5 not_converged, 6 cancelled, 7 out_of_time, 8 error, 1 the command line itself",
        "input": {"file": "upstream/B2-chemsep-benzene-toluene.json", "sha256": sha(RECORD.read_bytes()),
                  "copied_from": "https://github.com/FaireDose/CHEPTA, tag v0.6.0 (commit 5112c71f3f251100fe7d9d676412f48c543bc739), "
                                 "validation/data/columns/B2-chemsep-benzene-toluene.json, byte-identical; "
                                 "not re-copied from a newer tag (not reachable from this session)"},
        "unit_conversion": "flows in mol/s (CHEPTA's record) x 3.6 = kmol/h (CHEPTA's request unit)",
        "runs": runs,
    }
    (OUT / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for r in runs:
        print(r["id"], "exit", r["exit_code"], r["outcome"], (r["error"] or {}).get("code", ""), (r["error"] or {}).get("message", "")[:200])


if __name__ == "__main__":
    main()
