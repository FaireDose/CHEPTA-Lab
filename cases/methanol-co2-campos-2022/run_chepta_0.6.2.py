#!/usr/bin/env python3
"""Run the one-step CO2-to-methanol plant (Lacerda de Oliveira Campos et al. 2022) on chepta@0.6.2 through its command
line (`chepta request <file>`), as an assistant would. The requests are built by model.py.

Groups (MEOH_GROUPS, comma-separated; default all): units, columns, sections, plant, extra.
MEOH_ONLY=id1,id2 runs only those run ids (of the groups chosen). Every output is kept, refusals and failures
included; the run manifest is merged with the runs already recorded.

CHEPTA: the package pinned in Lab's package.json (chepta 0.6.2), node_modules/.bin/chepta after `npm ci`, or CHEPTA_BIN.
  python3 cases/methanol-co2-campos-2022/run_chepta_0.6.2.py
"""
import datetime
import hashlib
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import model as M  # noqa: E402

VERSION = "0.6.2"
OUT = H / f"results-chepta-{VERSION}"
EXIT = {-9: "stopped by Lab (wall time)", 0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}
TIME_MS = os.environ.get("MEOH_TIME_MS", "900000")
WALL_S = int(os.environ.get("MEOH_WALL_S", "1200"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Runner:
    def __init__(self, cmd):
        self.cmd, self.runs = cmd, []

    def run(self, run_id, req, note=""):
        only = os.environ.get("MEOH_ONLY")
        if only and run_id not in only.split(","):
            return None
        if (OUT / f"{run_id}.output.json").exists():  # never overwrite a kept run: a rerun gets a suffix
            k = 2
            while (OUT / f"{run_id}-r{k}.output.json").exists():
                k += 1
            run_id = f"{run_id}-r{k}"
        f = OUT / f"{run_id}.request.json"
        f.write_text(json.dumps(req, indent=2) + "\n")
        t0 = datetime.datetime.now(datetime.timezone.utc)
        try:
            p = subprocess.run(self.cmd + ["request", "--time-ms", TIME_MS, str(f)], capture_output=True, text=True, timeout=WALL_S)
        except subprocess.TimeoutExpired as e:
            p = subprocess.CompletedProcess(e.cmd, returncode=-9, stdout="",
                                            stderr=f"Stopped by Lab's runner after {WALL_S} s of wall time (CHEPTA's --time-ms {TIME_MS} had not stopped it).\n")
        (OUT / f"{run_id}.output.json").write_text(p.stdout)
        (OUT / f"{run_id}.stderr.txt").write_text(p.stderr)
        try:
            res = json.loads(p.stdout) if p.stdout.strip() else {}
        except json.JSONDecodeError:
            res = {}
        err = res.get("error") or {}
        self.runs.append({"id": run_id, "note": note, "command": f"chepta request --time-ms {TIME_MS} {f.relative_to(H)}",
                          "started_at": t0.isoformat(), "exit_code": p.returncode, "exit_meaning": EXIT.get(p.returncode, "unknown"),
                          "outcome": res.get("outcome"), "error_code": err.get("code"), "error_message": err.get("message"),
                          "chepta_run_id": (res.get("run") or {}).get("id"), "elapsed_ms": (res.get("run") or {}).get("elapsed_ms"),
                          "request_file": f"{OUT.name}/{run_id}.request.json", "output_file": f"{OUT.name}/{run_id}.output.json",
                          "stderr_file": f"{OUT.name}/{run_id}.stderr.txt",
                          "request_file_sha256": sha(f.read_bytes()), "output_file_sha256": sha(p.stdout.encode())})
        print(run_id, "exit", p.returncode, res.get("outcome"), err.get("code", ""), (err.get("message") or "")[:300], flush=True)
        return res


def chepta_cmd():
    if os.environ.get("CHEPTA_BIN"):
        return shlex.split(os.environ["CHEPTA_BIN"])
    local = H.parent.parent / "node_modules" / ".bin" / "chepta"
    return [str(local)] if local.exists() else ["npx", "--yes", f"chepta@{VERSION}"]


def main():
    OUT.mkdir(exist_ok=True)
    cmd = chepta_cmd()
    v = subprocess.run(cmd + ["--version"], capture_output=True, text=True).stdout.strip()
    if VERSION not in v:
        sys.exit(f"expected chepta {VERSION}, got {v!r}")
    groups = os.environ.get("MEOH_GROUPS", "units,columns,sections,plant,extra").split(",")
    R = Runner(cmd)
    if "units" in groups:
        for rid, rq in M.unit_runs().items():
            R.run(rid, rq)
    if "columns" in groups:
        for rid, rq in M.column_runs().items():
            R.run(rid, rq)
    if "sections" in groups:
        for rid, rq in M.section_runs().items():
            R.run(rid, rq)
    if "plant" in groups:
        for rid, rq in M.plant_runs().items():
            R.run(rid, rq)
    if "extra" in groups:
        for rid, rq in M.extra_runs().items():
            R.run(rid, rq)
    man_f = OUT / "run-manifest.json"
    old = json.loads(man_f.read_text()) if man_f.exists() else {"runs": []}
    new_ids = {r["id"] for r in R.runs}
    runs = [r for r in old["runs"] if r["id"] not in new_ids] + R.runs
    man = {"engine": f"chepta {v} (npm package, Lab's package.json pin)", "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
           "interface": "chepta request --time-ms N <file> (command line)", "source": "Lacerda de Oliveira Campos et al. 2022, Processes 10, 1535 (CC BY 4.0)",
           "model_py_sha256": sha((H / "model.py").read_bytes()), "settings": [list(s) for s in M.SETTINGS],
           "kinetics_rights": M.KINETICS_RIGHTS, "runs": sorted(runs, key=lambda r: r["started_at"])}
    man_f.write_text(json.dumps(man, indent=1) + "\n")


if __name__ == "__main__":
    main()
