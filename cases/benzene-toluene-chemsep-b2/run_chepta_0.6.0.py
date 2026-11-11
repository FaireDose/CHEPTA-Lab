#!/usr/bin/env python3
"""Run CHEPTA's B2 column (benzene + toluene, The ChemSep Book, sections 1.2-1.3) on the pinned npm package
chepta@0.6.0 through its command line (`npx chepta request <file>`), as an assistant would.

The requests are built here from CHEPTA's own record, copied unchanged to upstream/B2-chemsep-benzene-toluene.json:
no number is typed in this script except the unit factor 3.6 (mol/s to kmol/h). Three requests:
  b2-pr                    the column as in CHEPTA's record and test: PR, reflux ratio 2, bottoms flow (expected ok)
  b2-record-thermo-literal the record's "thermo" block as written (model and sets), not as CHEPTA's test passes it
  b2-distillate-purity     intentional: a direct distillate purity in place of the bottoms flow (expected unsupported:
                           purity specifications are CHEPTA milestone M4, not in 0.6.0)
Every output is kept, refusals included. Usage (repository root, after `npm ci`):
  python3 cases/benzene-toluene-chemsep-b2/run_chepta_0.6.0.py
"""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
OUT = H / "results-chepta-0.6.0"
KMOL_H_PER_MOL_S = 3.6  # 1 mol/s = 3600 mol/h = 3.6 kmol/h
RECORD = H / "upstream/B2-chemsep-benzene-toluene.json"
EXIT = {0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def requests(rec):
    comps, f = rec["components"], rec["column"]["feed"]
    specs = {s["kind"]: s for s in rec["specs"]}
    feed = {"flow_kmol_h": {c: z * f["flow_mol_s"] * KMOL_H_PER_MOL_S for c, z in zip(comps, f["z"])},
            "P_kPa": rec["pressure_kPa"], "VF": 0}  # q = 1: saturated liquid at the column pressure
    column = {"mode": "rigorous", "stages": rec["column"]["stages"], "feed_stage": f["stage"],
              "condenser": rec["column"]["condenser"], "P_kPa": rec["pressure_kPa"],
              "reflux_ratio": specs["reflux_ratio"]["value"],
              "bottoms_kmol_h": specs["bottoms_flow_mol_s"]["value"] * KMOL_H_PER_MOL_S}
    base = {"components": comps, "thermo": {"model": rec["thermo"]["model"]}, "feed": feed, "column": column}
    literal = json.loads(json.dumps(base))
    literal["thermo"] = {k: v for k, v in rec["thermo"].items() if k != "kind"}  # "kind" is the record's, not a thermo key
    purity = json.loads(json.dumps(base))
    del purity["column"]["bottoms_kmol_h"]
    purity["column"]["distillate_purity"] = {"component": comps[0], "value": rec["published"]["x_D"][0]}
    return {
        "b2-pr": base,
        "b2-record-thermo-literal": literal,
        "b2-distillate-purity": purity,
    }


def main():
    OUT.mkdir(exist_ok=True)
    lock = json.loads((ROOT / "package-lock.json").read_text())["packages"]["node_modules/chepta"]
    version = subprocess.run(["npx", "chepta", "--version"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if version != "0.6.0" or lock["version"] != "0.6.0":
        sys.exit(f"Expected chepta 0.6.0, found CLI {version} / lock {lock['version']}")
    rec = json.loads(RECORD.read_text())
    runs = []
    for run_id, inp in requests(rec).items():
        req = OUT / f"{run_id}.request.json"
        req.write_text(json.dumps({"capability": "solve_column", "input": inp}, indent=2) + "\n")
        rel = req.relative_to(ROOT)
        p = subprocess.run(["npx", "chepta", "request", str(rel)], cwd=ROOT, capture_output=True, text=True)
        (OUT / f"{run_id}.output.json").write_text(p.stdout)
        (OUT / f"{run_id}.stderr.txt").write_text(p.stderr)
        result = json.loads(p.stdout) if p.stdout.strip() else {}
        runs.append({"id": run_id, "command": f"npx chepta request {rel}", "exit_code": p.returncode,
                     "exit_meaning": EXIT.get(p.returncode, "unknown"), "outcome": result.get("outcome"),
                     "error": result.get("error"),
                     "request_file": f"results-chepta-0.6.0/{run_id}.request.json",
                     "output_file": f"results-chepta-0.6.0/{run_id}.output.json",
                     "stderr_file": f"results-chepta-0.6.0/{run_id}.stderr.txt",
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
                                 "validation/data/columns/B2-chemsep-benzene-toluene.json, byte-identical"},
        "unit_conversion": "flows in mol/s (CHEPTA's record, from The ChemSep Book) x 3.6 = kmol/h (CHEPTA's request unit)",
        "runs": runs,
    }
    (OUT / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for r in runs:
        print(r["id"], "exit", r["exit_code"], r["outcome"], (r["error"] or {}).get("code", ""))


if __name__ == "__main__":
    main()
