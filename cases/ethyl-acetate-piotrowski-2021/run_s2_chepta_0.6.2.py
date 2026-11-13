#!/usr/bin/env python3
"""Run the classic ethyl acetate plant S2 (Piotrowski & Kubica 2021) on chepta@0.6.2 through its command line
(`chepta request <file>`), and try to close it as one flowsheet.

Groups (S2_GROUPS, comma-separated; default all):
  info       component_info of the 4 components (CHEPTA's molar masses, used by compare_s2_062.py)
  rerun      every request that 0.6.1 refused or failed, sent UNCHANGED (the request files of results-chepta-0.6.1)
  units      new unit runs that 0.6.1 could not do (acid with two liquids, feeds at 15 C)
  plant      the whole plant as one closed flowsheet (s2_model_062.plant), in its variants
  policy     the closed plant again with options.strictRanges true and with thermo.missingPairs "refuse"
Only runs named in S2_ONLY (comma-separated) are run when it is set. Every output is kept, refusals and failures
included; the run manifest is merged when only some runs are made.

CHEPTA: the released npm package chepta@0.6.2, installed outside the repository (npm install chepta@0.6.2 in a
separate folder; Lab's package.json and data/upstream.json are not changed). Give its command line with CHEPTA_BIN.
  CHEPTA_BIN=/path/node_modules/.bin/chepta python3 cases/ethyl-acetate-piotrowski-2021/run_s2_chepta_0.6.2.py
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
import s2_model_062 as P  # noqa: E402

VERSION = "0.6.2"
OUT = H / f"results-chepta-{VERSION}"
OLD = H / "results-chepta-0.6.1"
EXIT = {-9: "stopped by Lab (wall time)", 0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}
TIME_MS = os.environ.get("S2_TIME_MS", "3000000")
WALL_S = int(TIME_MS) // 1000 + 300
RERUN = ["u-htxr2-15C", "u-extr8-1stage-70C", "u-extr8-1stage-27C-acid", "u-htxr10-acid", "u-scds11-acid-VL",
         "u-scds11-acid-VLL", "u-htxr12-acid", "u-htxr18-acid", "u-htxr19-acid", "u3-scds11-bottomsflow-VL",
         "secA-feeds-17C", "secB-mix7-adiabatic", "plant-a2-r02-A", "diag-scds5-round2-inlets",
         "diag-scds5-round2-inlets-VLL", "u3-extr8-1stage-70C-feed70C"]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def summary(res):
    """What a run says about the new defaults: extrapolations and estimated pairs (lists of short texts)."""
    v = res.get("value") or {}
    q = res.get("qualifications") or {}
    ex = v.get("extrapolations") or []
    est = q.get("estimated_pairs") or q.get("estimatedPairs") or []
    tiers = sorted({p.get("tier") for p in q.get("pairs", []) if p.get("tier")})
    return {"extrapolations": [e.get("short") or e.get("message") for e in ex],
            "estimated_pairs": est, "pair_tiers": tiers, "missing_pairs": q.get("missing_pairs", [])}


class Runner:
    def __init__(self, cmd):
        self.cmd, self.runs = cmd, []

    def run(self, run_id, req, note=None):
        only = os.environ.get("S2_ONLY")
        if only and run_id not in only.split(","):
            return None
        f = OUT / f"{run_id}.request.json"
        f.write_text(json.dumps(req, indent=2) + "\n")
        t0 = datetime.datetime.now(datetime.timezone.utc)
        try:
            p = subprocess.run(self.cmd + ["request", "--time-ms", TIME_MS, str(f)], capture_output=True, text=True, timeout=WALL_S)
        except subprocess.TimeoutExpired as e:
            p = subprocess.CompletedProcess(e.cmd, returncode=-9, stdout="",
                                            stderr=f"Stopped by Lab's runner after {WALL_S} s of wall time (CHEPTA's limit --time-ms {TIME_MS} had not stopped it).\n")
        (OUT / f"{run_id}.output.json").write_text(p.stdout)
        (OUT / f"{run_id}.stderr.txt").write_text(p.stderr)
        res = json.loads(p.stdout) if p.stdout.strip() else {}
        rec = {"id": run_id, "command": f"chepta request --time-ms {TIME_MS} {f.relative_to(H)}", "chepta_version": VERSION,
               "started_at": t0.isoformat(), "exit_code": p.returncode, "exit_meaning": EXIT.get(p.returncode, "unknown"),
               "outcome": res.get("outcome"), "error": res.get("error"), "chepta_run_id": (res.get("run") or {}).get("id"),
               "elapsed_ms": (res.get("run") or {}).get("elapsed_ms"),
               "request_file": f"{OUT.name}/{run_id}.request.json", "output_file": f"{OUT.name}/{run_id}.output.json",
               "stderr_file": f"{OUT.name}/{run_id}.stderr.txt",
               "request_file_sha256": sha(f.read_bytes()), "output_file_sha256": sha(p.stdout.encode()), **summary(res)}
        if note:
            rec["note"] = note
        self.runs.append(rec)
        e = res.get("error") or {}
        print(run_id, "exit", p.returncode, res.get("outcome"), e.get("code", ""), (e.get("message") or "")[:200], flush=True)
        return res


def fs(doc):
    return {"capability": "solve_flowsheet", "input": {"flowsheet": doc}}


def unit_requests():
    """New unit runs: what 0.6.1 could not do, with acetic acid as a component."""
    U = {}
    U["u62-extr8-2stage-acid"] = M.unit({"id": "EXTR8", "type": "extraction", "spec": M.extractor_spec(2)},
                                        [("feed", 10), ("solvent", 19)], [("raffinate", 11), ("extract", 20)])
    U["u62-scds11-acid-purity"] = M.unit({"id": "SCDS11", "type": "column", "spec": M.column11_spec("purity", "VLL")}, [("in", 13)], [("distillate", 14), ("bottoms", 16)])
    sp = M.column11_spec("flow", "VLL")
    sp.pop("bottoms_kmol_h")
    sp["distillate_kmol_h"] = M.STREAMS[14]["molar_kmol_h"]
    U["u62-scds11-acid-distillate"] = M.unit({"id": "SCDS11", "type": "column", "spec": sp}, [("in", 13)], [("distillate", 14), ("bottoms", 16)])
    U["u62-scds11-noacid-bottomsflow"] = M.unit({"id": "SCDS11", "type": "column", "spec": M.column11_spec("flow", "VLL")}, [("in", 13)], [("distillate", 14), ("bottoms", 16)], M.COMPONENTS_B)
    U["u62-scds15-acid-VLL"] = M.unit({"id": "SCDS15", "type": "column", "spec": M.column15_spec("VLL")}, [("in", 28)], [("distillate", 21), ("bottoms", 22)])
    c5 = dict(M.column5_spec(), phases="VLL")
    U["u62-scds5-VLL"] = M.unit({"id": "SCDS5", "type": "column", "spec": c5}, [("in", 27), ("in", 6)], [("distillate", 8), ("bottoms", 7)])
    U["secA62-paper-inlets-15C"] = M.section_a(T_feeds_C=P.T_FEED_C)  # section A as in 0.6.1, feeds at the printed 15 C
    return U


def guesses_061():
    """Tear-stream starting guesses from CHEPTA's own once-through plant on 0.6.1 (runs plant-a2-r01-A and -B)."""
    a = json.loads((OLD / "plant-a2-r01-A.output.json").read_text())["value"]["streams"]
    b = json.loads((OLD / "plant-a2-r01-B.output.json").read_text())["value"]["streams"]
    return {7: M.as_guess(a["S7"]), 15: M.as_guess(b["S15"]), 24: M.as_guess(b["S24"]), 27: M.as_guess(b["S27"]), 21: M.as_guess(b["S21"])}


OPEN = "open"  # marker: streams 27 and 21 fed from Table A2 (outer recycles opened)
PLANTS = {
    # id: (kwargs of s2_model_062.plant, what it is)
    "plant62-W-dist": ({"split16": "W", "spec11": "distillate"}, "closed; 26 = 60,000 kg/h and 25 = 20,000 kg/h (the paper's two round flows); column 11 R/D 3 and distillate 230.4 kmol/h; Broyden"),
    "plant62-R-bottoms": ({"split16": "R", "spec11": "bottoms"}, "closed; 26 = 60,000 kg/h, 23 = 95,797 kg/h (25 the rest); column 11 R/D 3 and bottoms 141.5 kmol/h; Broyden"),
    "plant62-R-bottoms-direct": ({"split16": "R", "spec11": "bottoms", "method": "direct"}, "as plant62-R-bottoms, direct substitution"),
    "plant62-R-bottoms-wegstein": ({"split16": "R", "spec11": "bottoms", "method": "wegstein"}, "as plant62-R-bottoms, Wegstein"),
    "plant62-R-bottoms-col5VL": ({"split16": "R", "spec11": "bottoms", "phases5": None}, "as plant62-R-bottoms, column 5 with one liquid (VL)"),
    "plant62-R-purity-direct": ({"split16": "R", "spec11": "purity", "method": "direct"}, "closed; 23 = 95,797 kg/h; column 11 R/D 3 and product 99.90 mass %; direct substitution"),
    "plant62-R-bottoms-warm": ({"split16": "R", "spec11": "bottoms", "guesses": "061"}, "as plant62-R-bottoms, tear guesses from CHEPTA's own 0.6.1 once-through streams"),
    "plant62-W-dist-warm": ({"split16": "W", "spec11": "distillate", "guesses": "061"}, "as plant62-W-dist, tear guesses from CHEPTA's own 0.6.1 once-through streams"),
    "plant62-R-bottoms-warm-col5iter100": ({"split16": "R", "spec11": "bottoms", "guesses": "061", "col5_max_iter": 100},
                                           "as plant62-R-bottoms-warm, column 5 max_iterations 100"),
    "plant62-R-bottoms-mix7adiabatic-open": ({"split16": "R", "spec11": "bottoms", "mix7": "adiabatic", "open_recycles": OPEN},
                                             "streams 27 and 21 fed from Table A2 (outer recycles open); MIX 7 adiabatic"),
    "plant62-R-bottoms-open": ({"split16": "R", "spec11": "bottoms", "open_recycles": OPEN}, "streams 27 and 21 fed from Table A2 (outer recycles open)"),
    "plant62-frac-bottoms-open": ({"split9": "frac", "split16": "frac", "spec11": "bottoms", "open_recycles": OPEN},
                                  "outer recycles open; both splitters by the fractions of 0.6.1"),
}


def build_plant(kw):
    kw = dict(kw)
    if kw.get("open_recycles") == OPEN:
        kw["open_recycles"] = {27: M.feed_spec(27), 21: M.feed_spec(21, VF=0)}
    if kw.get("guesses") == "061":
        kw["guesses"] = guesses_061()
    return P.plant(**kw)


def run_parallel(R, jobs):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(int(os.environ.get("S2_PARALLEL", "3"))) as ex:
        list(ex.map(lambda j: R.run(*j), jobs))


def main():
    cmd = shlex.split(os.environ.get("CHEPTA_BIN", f"npx --yes chepta@{VERSION}"))
    version = subprocess.run(cmd + ["--version"], capture_output=True, text=True).stdout.strip()
    if version != VERSION:
        sys.exit(f"Expected chepta {VERSION}, found {version!r}")
    OUT.mkdir(exist_ok=True)
    groups = os.environ.get("S2_GROUPS", "info,rerun,units,plant,policy").split(",")
    R = Runner(cmd)
    if "info" in groups:
        for c in M.IDS:
            R.run(f"info-{c}", {"capability": "component_info", "input": {"component": c}})
    if "rerun" in groups:
        run_parallel(R, [(f"rerun-{rid}", json.loads((OLD / f"{rid}.request.json").read_text()), f"the request of 0.6.1 run {rid}, unchanged")
                         for rid in RERUN])
    if "units" in groups:
        run_parallel(R, [(k, fs(v)) for k, v in unit_requests().items()])
    if "plant" in groups:
        run_parallel(R, [(k, fs(build_plant(kw)), what) for k, (kw, what) in PLANTS.items()])
    if "policy" in groups:
        base = os.environ.get("S2_POLICY_BASE", "plant62-W-dist")
        kw = PLANTS[base][0]
        jobs = [(f"{base}-strictRanges", P.with_options(fs(build_plant(kw)), strictRanges=True), f"{base} with options.strictRanges true"),
                (f"{base}-refusePairs", fs(build_plant({**kw, "thermo_extra": {"missingPairs": "refuse"}})), f"{base} with thermo.missingPairs refuse")]
        # the same two policies on converged runs that carry extrapolations (the closed plant does not converge)
        u = json.loads((OLD / "u-htxr2-15C.request.json").read_text())
        jobs.append(("u-htxr2-15C-strictRanges", P.with_options(u, strictRanges=True), "0.6.1 request u-htxr2-15C with options.strictRanges true"))
        u2 = json.loads((OLD / "u-htxr2-15C.request.json").read_text())
        u2["input"]["flowsheet"]["thermo"]["missingPairs"] = "refuse"
        jobs.append(("u-htxr2-15C-refusePairs", u2, "0.6.1 request u-htxr2-15C with thermo.missingPairs refuse"))
        x = fs(unit_requests()["u62-extr8-2stage-acid"])
        jobs.append(("u62-extr8-2stage-acid-strictRanges", P.with_options(x, strictRanges=True), "u62-extr8-2stage-acid with options.strictRanges true"))
        # the flowsheet's own switch, solver.strictRanges (src/flowsheet/flowsheet.js), in case request.options is not passed on
        b = build_plant(kw)
        b["solver"]["strictRanges"] = True
        jobs.append((f"{base}-solverStrict", fs(b), f"{base} with flowsheet solver.strictRanges true"))
        u3 = json.loads((OLD / "u-htxr2-15C.request.json").read_text())
        u3["input"]["flowsheet"]["solver"]["strictRanges"] = True
        jobs.append(("u-htxr2-15C-solverStrict", u3, "0.6.1 request u-htxr2-15C with flowsheet solver.strictRanges true"))
        run_parallel(R, jobs)
    man_path = OUT / "run-manifest.json"
    old = json.loads(man_path.read_text()) if man_path.exists() else {"runs": []}
    new_ids = {r["id"] for r in R.runs}
    pkg = Path(cmd[-1]).resolve().parents[1] / "package.json" if os.environ.get("CHEPTA_BIN") else None
    manifest = {
        "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "engine": {"package": "chepta", "version": version, "resolved": f"https://registry.npmjs.org/chepta/-/chepta-{VERSION}.tgz",
                   "integrity": "sha512-yXI+yL84uXDfeUo7KBn7zbyb+acCzipXA9aSvDQijoKrCGyCyDOZ8o9Ym0XV/uFBMDITk/78mn6e9ubjKN0vMw==",
                   "lock_file": "chepta-0.6.2.npm-lock.json",
                   "installed_with": "npm install chepta@0.6.2 in a separate folder; Lab's package.json, package-lock.json and data/upstream.json not changed",
                   "package_json_sha256": sha(pkg.read_bytes()) if pkg and pkg.exists() else None},
        "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
        "interface": "command line: chepta request <file>; exit codes 0 ok, 2 invalid_input, 3 missing_data, 4 unsupported, "
                     "5 not_converged, 6 cancelled, 7 out_of_time, 8 error, 1 the command line itself",
        "source": {"paper": "Piotrowski & Kubica 2021, Processes 9, 1425, doi 10.3390/pr9081425, CC BY 4.0",
                   "transcriptions": {n: sha((H / n).read_bytes()) for n in ("streams.json", "equipment.json", "s2_model.py", "s2_model_062.py")}},
        "settings": M.SETTINGS,
        "settings_062": P.SETTINGS_062,
        "plants": {k: {"kwargs": kw, "what": what} for k, (kw, what) in PLANTS.items()},
        "plants_note": "open_recycles \"open\": streams 27 and 21 fed with Table A2 (27 as printed, 21 saturated liquid); guesses \"061\": tear guesses from 0.6.1 runs plant-a2-r01-A/B",
        "runs": [r for r in old["runs"] if r["id"] not in new_ids] + R.runs,
    }
    man_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
