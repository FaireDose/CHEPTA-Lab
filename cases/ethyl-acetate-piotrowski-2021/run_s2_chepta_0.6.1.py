#!/usr/bin/env python3
"""Run the classic ethyl acetate plant S2 (Piotrowski & Kubica 2021) on chepta@0.6.1 through its command line
(`chepta request <file>`), as an assistant would. The requests are built by s2_model.py from the case's transcriptions.

Groups (S2_GROUPS, comma-separated; default all):
  info      component_info of the 4 components (CHEPTA's molar masses, used by compare_s2.py)
  units     every unit alone with the paper's inlet streams (u-*, u3-*), refusals included
  sections  section A and section B alone, fed at the cut with the paper's streams 9, 21, 27 (secA-*, secB-*)
  diag      column 5 alone with the inlets of round 2 of the coupling (diag-*)
  plant     the whole plant: sections A and B coupled across the cut by this script (successive substitution of
            streams 9, 21 and 27, at most PLANT_MAX_ITER rounds), every round's requests and results kept (plant-*)
Every output is kept, refusals and failures included. The run manifest is merged when only some groups are run.

CHEPTA: the released npm package chepta@0.6.1. Lab's package.json may pin another version; this script does not use
it. Give the command line with CHEPTA_BIN (for example node_modules/.bin/chepta after `npm install --no-save
chepta@0.6.1`), or leave it unset for `npx --yes chepta@0.6.1`. The version is checked before any run.
  python3 cases/ethyl-acetate-piotrowski-2021/run_s2_chepta_0.6.1.py
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
import s2_model as M  # noqa: E402

VERSION = "0.6.1"
OUT = H / f"results-chepta-{VERSION}"
EXIT = {-9: "stopped by Lab (wall time)", 0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}
TIME_MS = "900000"
WALL_S = 1200  # Lab's own wall-time stop, in case CHEPTA does not stop at TIME_MS
PLANT_STAGES = int(os.environ.get("S2_PLANT_STAGES", "2"))
PLANT_MAX_ITER = 30
ATTEMPT = os.environ.get("S2_PLANT_ATTEMPT", "a2")
WARM = ATTEMPT != "a1"  # attempt a1 restarted every tear stream from the paper's values; later attempts warm-start
PLANT_TOL = 1e-4  # largest relative change of a cut stream's component flow (of its total flow) between rounds


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Runner:
    def __init__(self, cmd):
        self.cmd, self.runs = cmd, []

    def run(self, run_id, req):
        only = os.environ.get("S2_ONLY")
        if only and run_id not in only.split(","):
            return None
        f = OUT / f"{run_id}.request.json"
        f.write_text(json.dumps(req, indent=2) + "\n")
        t0 = datetime.datetime.now(datetime.timezone.utc)
        try:
            p = subprocess.run(self.cmd + ["request", "--time-ms", TIME_MS, str(f)], capture_output=True, text=True,
                               timeout=WALL_S)
        except subprocess.TimeoutExpired as e:  # CHEPTA did not stop at its own limit: Lab stops it and keeps the record
            p = subprocess.CompletedProcess(e.cmd, returncode=-9, stdout="",
                                            stderr=f"Stopped by Lab's runner after {WALL_S} s of wall time (CHEPTA's limit --time-ms {TIME_MS} had not stopped it).\n")
        (OUT / f"{run_id}.output.json").write_text(p.stdout)
        (OUT / f"{run_id}.stderr.txt").write_text(p.stderr)
        res = json.loads(p.stdout) if p.stdout.strip() else {}
        self.runs.append({"id": run_id, "command": f"chepta request --time-ms {TIME_MS} {f.relative_to(H)}",
                          "started_at": t0.isoformat(), "exit_code": p.returncode, "exit_meaning": EXIT.get(p.returncode, "unknown"),
                          "outcome": res.get("outcome"), "error": res.get("error"), "chepta_run_id": (res.get("run") or {}).get("id"),
                          "elapsed_ms": (res.get("run") or {}).get("elapsed_ms"),
                          "request_file": f"{OUT.name}/{run_id}.request.json", "output_file": f"{OUT.name}/{run_id}.output.json",
                          "stderr_file": f"{OUT.name}/{run_id}.stderr.txt",
                          "request_file_sha256": sha(f.read_bytes()), "output_file_sha256": sha(p.stdout.encode())})
        print(run_id, "exit", p.returncode, res.get("outcome"), (res.get("error") or {}).get("code", ""), flush=True)
        return res


def fs(doc):
    return {"capability": "solve_flowsheet", "input": {"flowsheet": doc}}


def change(a, b):
    """Largest change of a component flow between two streams, relative to the larger total flow."""
    keys = set(a["flow_kmol_h"]) | set(b["flow_kmol_h"])
    tot = max(a["F_kmol_h"], b["F_kmol_h"], 1e-12)
    return max(abs(a["flow_kmol_h"].get(k, 0) - b["flow_kmol_h"].get(k, 0)) for k in keys) / tot


def plant(R):
    """Successive substitution across the cut: A(27, 21) -> 9 -> B(9) -> 27, 21 -> A ... Returns the coupling record."""
    s27 = s21 = None  # first round: the paper's streams 27 and 21
    ga = gb = None  # tear-stream guesses: the paper's in round 1, then the previous round's converged streams
    prev, history = None, []
    tag = f"plant-{ATTEMPT}"
    for it in range(1, PLANT_MAX_ITER + 1):
        a = R.run(f"{tag}-r{it:02d}-A", fs(M.section_a(s27, s21, guesses=ga)))
        if a.get("outcome") != "ok":
            return {"converged": False, "rounds": it, "history": history, "stopped": f"section A refused in round {it}"}
        s9 = a["value"]["streams"]["S9"]
        acid_dropped = s9["flow_kmol_h"].get("acetic-acid", 0.0)
        f9 = M.as_feed(s9, M.COMPONENTS_B)
        f9.pop("T_K")
        f9["VF"] = 0  # the saturated liquid of HTXR 6 (the dropped trace acid moves its bubble point negligibly)
        b = R.run(f"{tag}-r{it:02d}-B", fs(M.section_b(PLANT_STAGES, f9, guesses=gb)))
        if b.get("outcome") != "ok":
            return {"converged": False, "rounds": it, "history": history, "stopped": f"section B refused in round {it}"}
        bs = b["value"]["streams"]
        if WARM:
            ga = {7: M.as_guess(a["value"]["streams"]["S7"])}
            gb = {15: M.as_guess(bs["S15"]), 24: M.as_guess(bs["S24"])}
        s27 = M.as_feed(bs["S27"], M.COMPONENTS_B)
        s21 = M.as_feed(bs["S21"], M.COMPONENTS_B)
        s21.pop("T_K")
        s21["VF"] = 0
        cur = {"S9": s9, "S27": bs["S27"], "S21": bs["S21"]}
        d = {k: change(cur[k], prev[k]) for k in cur} if prev else None
        history.append({"round": it, "acetic_acid_dropped_at_cut_kmol_h": acid_dropped, "max_relative_change": d})
        print("  round", it, d, flush=True)
        prev = cur
        if d and max(d.values()) < PLANT_TOL:
            return {"converged": True, "rounds": it, "history": history, "tolerance": PLANT_TOL,
                    "final": {"A": f"{tag}-r{it:02d}-A", "B": f"{tag}-r{it:02d}-B"}}
    return {"converged": False, "rounds": PLANT_MAX_ITER, "history": history, "stopped": "round limit"}


def main():
    cmd = shlex.split(os.environ.get("CHEPTA_BIN", f"npx --yes chepta@{VERSION}"))
    version = subprocess.run(cmd + ["--version"], capture_output=True, text=True).stdout.strip()
    if version != VERSION:
        sys.exit(f"Expected chepta {VERSION}, found {version!r}")
    OUT.mkdir(exist_ok=True)
    groups = os.environ.get("S2_GROUPS", "info,units,sections,plant").split(",")
    R = Runner(cmd)
    coupling = None
    if "info" in groups:
        for c in M.IDS:
            R.run(f"info-{c}", {"capability": "component_info", "input": {"component": c}})
    if "units" in groups:
        for k, v in M.unit_requests().items():
            R.run(k, fs(v))
    if "sections" in groups:
        R.run("secA-feeds-17C", fs(M.section_a(T_feeds_C=17)))  # refusal kept on record
        R.run("secA-paper-inlets", fs(M.section_a()))
        R.run("secB-mix7-adiabatic", fs(M.section_b(PLANT_STAGES, mix7_adiabatic=True)))  # refusal kept on record
        for n in M.EXTR_STAGES:
            R.run(f"secB-paper-inlets-extr{n}", fs(M.section_b(n)))
    if "plant" in groups:
        coupling = plant(R)
    if "diag" in groups:  # column 5 alone with the inlets it met in round 2 of attempt a2 (why the coupling stops)
        ra = json.loads((OUT / "plant-a2-r01-A.output.json").read_text())["value"]["streams"]
        rb = json.loads((OUT / "plant-a2-r01-B.output.json").read_text())["value"]["streams"]
        f27 = M.as_feed(rb["S27"], M.COMPONENTS)
        f6 = M.as_feed(ra["S6"], M.COMPONENTS)
        f6.pop("T_K")
        f6["VF"] = 1
        blocks = [{"id": "SCDS5", "type": "column", "spec": M.column5_spec()}, {"id": "F27", "type": "feed", "spec": f27},
                  {"id": "F6", "type": "feed", "spec": f6}, {"id": "P8", "type": "product"}, {"id": "P7", "type": "product"}]
        streams = [{"id": "S27", "from": "F27.out", "to": "SCDS5.in"}, {"id": "S6", "from": "F6.out", "to": "SCDS5.in"},
                   {"id": "S8", "from": "SCDS5.distillate", "to": "P8.in"}, {"id": "S7", "from": "SCDS5.bottoms", "to": "P7.in"}]
        R.run("diag-scds5-round2-inlets", fs(M.doc(blocks, streams)))
        vll = dict(M.column5_spec(), phases="VLL")
        blocks[0] = {"id": "SCDS5", "type": "column", "spec": vll}
        R.run("diag-scds5-round2-inlets-VLL", fs(M.doc(blocks, streams)))
    man_path = OUT / "run-manifest.json"
    old = json.loads(man_path.read_text()) if man_path.exists() else {"runs": []}
    new_ids = {r["id"] for r in R.runs}
    if "plant" in groups:  # a new run of an attempt replaces that attempt's rounds; other attempts are kept
        old["runs"] = [r for r in old["runs"] if not r["id"].startswith(f"plant-{ATTEMPT}-")]
    pkg = Path(cmd[-1]).resolve().parents[1] / "package.json" if os.environ.get("CHEPTA_BIN") else None
    manifest = {
        "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "engine": {"package": "chepta", "version": version, "resolved": f"https://registry.npmjs.org/chepta/-/chepta-{VERSION}.tgz",
                   "integrity": "sha512-hB6c1spJtKTqa0wJFGiQGm1cWRTrPZhWCbw+rB3lV7FYLvTNNfRRE91nOTZ2ZGvqt3t13w15vvKQe1wIlWcaMw==",
                   "lock_file": "chepta-0.6.1.npm-lock.json",
                   "installed_with": "npm install chepta@0.6.1 in a separate folder; Lab's package.json and package-lock.json not changed",
                   "package_json_sha256": sha(pkg.read_bytes()) if pkg and pkg.exists() else None},
        "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
        "interface": "command line: chepta request <file>; exit codes 0 ok, 2 invalid_input, 3 missing_data, 4 unsupported, "
                     "5 not_converged, 6 cancelled, 7 out_of_time, 8 error, 1 the command line itself",
        "source": {"paper": "Piotrowski & Kubica 2021, Processes 9, 1425, doi 10.3390/pr9081425, CC BY 4.0",
                   "transcriptions": {"streams.json": sha((H / "streams.json").read_bytes()),
                                      "equipment.json": sha((H / "equipment.json").read_bytes()),
                                      "s2_model.py": sha((H / "s2_model.py").read_bytes())}},
        "settings": M.SETTINGS,
        "plant_extractor_stages": PLANT_STAGES,
        "plant_couplings": {**old.get("plant_couplings", {}), **({ATTEMPT: {**coupling, "warm_start": WARM}} if coupling else {})},
        "plant_coupling": ({**coupling, "attempt": ATTEMPT} if coupling else old.get("plant_coupling")),
        "runs": [r for r in old["runs"] if r["id"] not in new_ids] + R.runs,
    }
    man_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
