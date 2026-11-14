#!/usr/bin/env python3
"""Sensitivity runs on chepta@0.6.2 (the maintainer, 2026-11-13), beside results-chepta-0.6.2/ (old files never edited).
Reuses the flowsheets of run_chepta_0.6.2.py and adds, per method:
  <id>-kij0    user_data pair "hydrogen+carbon-monoxide" with PR k_ij = 0 (CHEPTA's own value is a set fitted at 68-88 K)
  <id>-strict  request.options.strictRanges = true (refuse outside a record's range)
Output: results-chepta-0.6.2-kij0-strict/ (requests, outputs, stderr, run-manifest.json, movement.json).
Usage (repository root, after `npm ci`): python3 cases/methanol-separator-flash/run_chepta_0.6.2_kij0_strict.py"""
import datetime, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
spec = importlib.util.spec_from_file_location("base", H / "run_chepta_0.6.2.py")
base = importlib.util.module_from_spec(spec); spec.loader.exec_module(base)
OUT = H / "results-chepta-0.6.2-kij0-strict"
USER = {"pairs": {"hydrogen+carbon-monoxide": {"PR": {"kij": 0},
        "source": {"name": "sensitivity assumption, k_ij = 0 (maintainer, 2026-11-13); not data"}}}}
sha = lambda b: hashlib.sha256(b).hexdigest()


def run(rid, base_id, case, extra, runs):
    req = OUT / f"{rid}.request.json"
    inp = {"flowsheet": base.flowsheet(case, base.METHODS[base_id])}
    body = {"capability": "solve_flowsheet", "input": inp}
    if "user_data" in extra: inp["user_data"] = extra["user_data"]
    if "options" in extra: body["options"] = extra["options"]
    req.write_text(json.dumps(body, indent=2) + "\n")
    rel = req.relative_to(ROOT)
    p = subprocess.run(["npx", "chepta", "request", str(rel)], cwd=ROOT, capture_output=True, text=True)
    (OUT / f"{rid}.output.json").write_text(p.stdout); (OUT / f"{rid}.stderr.txt").write_text(p.stderr)
    r = json.loads(p.stdout) if p.stdout.strip() else {}
    runs.append({"id": rid, "base_run": base_id, "change": extra, "command": f"npx chepta request {rel}",
                 "exit_code": p.returncode, "exit_meaning": base.EXIT.get(p.returncode, "unknown"),
                 "outcome": r.get("outcome"), "error": r.get("error"),
                 "request_file_sha256": sha(req.read_bytes()), "output_file_sha256": sha(p.stdout.encode())})
    print(rid, p.returncode, r.get("outcome"), (r.get("error") or {}).get("code", ""))


def flows(path):
    d = json.loads(path.read_text())
    if d.get("outcome") != "ok": return None
    s = d["value"]["streams"]
    return {k: {"F": s[k]["F_kmol_h"], "flow": s[k]["flow_kmol_h"], "z": dict(zip(s[k]["components"], s[k]["z"]))}
            for k in ("S2", "S3")}


def main():
    OUT.mkdir(exist_ok=True)
    version = subprocess.run(["npx", "chepta", "--version"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if version != "0.6.2": sys.exit(f"Expected chepta 0.6.2, found {version}")
    case = json.loads(base.CASE.read_text())
    runs = []
    for b in base.METHODS:
        run(f"{b}-kij0", b, case, {"user_data": USER}, runs)
        run(f"{b}-strict", b, case, {"options": {"strictRanges": True}}, runs)
    (OUT / "run-manifest.json").write_text(json.dumps({
        "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(), "engine": {"package": "chepta", "version": version},
        "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
        "input": {"file": "case-input.json", "sha256": sha(base.CASE.read_bytes())}, "runs": runs}, indent=2) + "\n")
    mv = {}
    for b in base.METHODS:
        o, n = flows(base.OUT / f"{b}.output.json"), flows(OUT / f"{b}-kij0.output.json")
        if not (o and n): mv[b] = "no comparison (a run not ok)"; continue
        m = {}
        for s in ("S2", "S3"):
            m[s] = {"F_kmol_h": {"old": o[s]["F"], "new": n[s]["F"], "abs": n[s]["F"] - o[s]["F"],
                                 "rel": (n[s]["F"] - o[s]["F"]) / o[s]["F"] if o[s]["F"] else None},
                    "components": {}}
            for c in o[s]["flow"]:
                for key, a, bb in (("flow_kmol_h", o[s]["flow"][c], n[s]["flow"][c]), ("x", o[s]["z"][c], n[s]["z"][c])):
                    m[s]["components"].setdefault(c, {})[key] = {"old": a, "new": bb, "abs": bb - a, "rel": (bb - a) / a if a else None}
        mv[b] = m
    (OUT / "movement.json").write_text(json.dumps(mv, indent=1) + "\n")


if __name__ == "__main__":
    main()
