#!/usr/bin/env python3
"""Run the illustrative methanol-loop separator flash (case-input.json, a state from CHEPTA's decision file
2026-11-06-02-mhv1.md, not from a paper) on the pinned npm package chepta@0.6.0 through its command line
(`npx chepta request <file>`), with three property methods:
  pr-mhv1   "PR + gE (MHV1)": thermo { model: "PR", mixing: "MHV1" }   (the method CHEPTA chose for the separator)
  pr-kij    plain PR with its k_ij: thermo { model: "PR" }             (for comparison)
  srk-mhv1  "SRK + gE (MHV1)": thermo { model: "SRK", mixing: "MHV1" } (expected refused: no SRK set for CO2 + water)
Each request is a one-flash flowsheet: feed at the separator state, isothermal flash at the same T and P, two products.
Every output is kept, refusals included. Usage (repository root, after `npm ci`):
  python3 cases/methanol-separator-flash/run_chepta_0.6.0.py
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
CASE = H / "case-input.json"
EXIT = {0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}
METHODS = {
    "pr-mhv1": {"model": "PR", "mixing": "MHV1"},
    "pr-kij": {"model": "PR"},
    "srk-mhv1": {"model": "SRK", "mixing": "MHV1"},
}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def flowsheet(case, thermo):
    comps = case["components"]
    flows = {c: z * case["basis_kmol_h"] for c, z in zip(comps, case["z"])}
    return {
        "components": comps,
        "thermo": thermo,
        "blocks": [
            {"id": "F1", "type": "feed", "spec": {"flow_kmol_h": flows, "T_K": case["T_K"], "P_kPa": case["P_kPa"]}},
            {"id": "V1", "type": "flash", "spec": {"T_K": case["T_K"], "P_kPa": case["P_kPa"]}},
            {"id": "P1", "type": "product"},
            {"id": "P2", "type": "product"},
        ],
        "streams": [
            {"id": "S1", "from": "F1.out", "to": "V1.in"},
            {"id": "S2", "from": "V1.vapour", "to": "P1.in"},
            {"id": "S3", "from": "V1.liquid", "to": "P2.in"},
        ],
    }


def main():
    OUT.mkdir(exist_ok=True)
    lock = json.loads((ROOT / "package-lock.json").read_text())["packages"]["node_modules/chepta"]
    version = subprocess.run(["npx", "chepta", "--version"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if version != "0.6.0" or lock["version"] != "0.6.0":
        sys.exit(f"Expected chepta 0.6.0, found CLI {version} / lock {lock['version']}")
    case = json.loads(CASE.read_text())
    runs = []
    for run_id, thermo in METHODS.items():
        req = OUT / f"{run_id}.request.json"
        req.write_text(json.dumps({"capability": "solve_flowsheet", "input": {"flowsheet": flowsheet(case, thermo)}},
                                  indent=2) + "\n")
        rel = req.relative_to(ROOT)
        p = subprocess.run(["npx", "chepta", "request", str(rel)], cwd=ROOT, capture_output=True, text=True)
        (OUT / f"{run_id}.output.json").write_text(p.stdout)
        (OUT / f"{run_id}.stderr.txt").write_text(p.stderr)
        result = json.loads(p.stdout) if p.stdout.strip() else {}
        runs.append({"id": run_id, "thermo": thermo, "command": f"npx chepta request {rel}",
                     "exit_code": p.returncode, "exit_meaning": EXIT.get(p.returncode, "unknown"),
                     "outcome": result.get("outcome"), "error": result.get("error"),
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
        "input": {"file": "case-input.json", "sha256": sha(CASE.read_bytes())},
        "runs": runs,
    }
    (OUT / "run-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for r in runs:
        print(r["id"], "exit", r["exit_code"], r["outcome"], (r["error"] or {}).get("code", ""))


if __name__ == "__main__":
    main()
