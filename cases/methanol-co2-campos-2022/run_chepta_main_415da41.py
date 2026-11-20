#!/usr/bin/env python3
"""Check CHEPTA's unreleased main, commit 415da41d531cd5b5701d0d13550f98c9888abced (to become 0.6.3), on the one-step
methanol plant (Lacerda de Oliveira Campos et al. 2022). Lab's released pin stays chepta 0.6.2 (package.json); this
script runs a source checkout of that commit through its command line, `node <checkout>/bin/chepta.mjs request`.

What it runs (into results-chepta-main-415da41/, never overwriting a kept run):
- the paper's vapour + liquid condenser (53 C, reflux ratio 2) in place of the 0.6.2 workaround M5 (partial condenser
  + 53 C flash), on the column alone and in the closed plant;
- each other workaround removed one at a time on top of that: M1 (traces bypass the column), M2 (bottoms fixed at
  4581 kmol/h), M4 (HE5 searched on 10 zones), M3 (Newton capped at 12 iterations);
- the small input files of capability requests M1-M4 again, unchanged from results-chepta-0.6.2/.

  CHEPTA_SRC=/path/to/CHEPTA-checkout python3 cases/methanol-co2-campos-2022/run_chepta_main_415da41.py
  MEOH_ONLY=id1,id2 runs only those ids.
The requests are built from model.py (unchanged) plus the variants below; every request file records the commit.
"""
import copy
import datetime
import json
import os
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import model as M  # noqa: E402
import hashlib  # noqa: E402

EXIT = {-9: "stopped by Lab (wall time)", 0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


COMMIT = "415da41d531cd5b5701d0d13550f98c9888abced"
OUT = H / "results-chepta-main-415da41"
OLD = H / "results-chepta-0.6.2"
TIME_MS = os.environ.get("MEOH_TIME_MS", "900000")
WALL_S = int(os.environ.get("MEOH_WALL_S", "1500"))
SRC = Path(os.environ.get("CHEPTA_SRC", "/home/user/chepta-main-415da41/src"))
T53 = M.K(53)

VL_SETTINGS = [
    ("column condenser (this check)", "condenser 'vapour_liquid', condenser_T_K 326.15 (53 C)", "paper",
     "supplement p.10: partial vapour-liquid condenser at 53 C; CHEPTA proposal 0026, new on main 415da41"),
    ("reflux ratio basis", "2 over the liquid distillate (CHEPTA's definition, L1/U1); a run with 2.1273 = 2 x (4542 + 289) / 4542 over the liquid distillate, i.e. 2 over the whole distillate",
     "assumed", "the paper prints 'reflux ratio 2' (p.10) without saying over which distillate; Aspen's definition for this condenser is not checked here"),
]


# ------------------------------------------------------------------------------------------------------------------
# Requests
def vl_column(second, T_K=T53, **extra):
    s = {"mode": "rigorous", "stages": 30, "feed_stage": 24, "P_kPa": 100, "condenser": "vapour_liquid", "condenser_T_K": T_K}
    s.update(second)
    s.update(extra)
    return {k: v for k, v in s.items() if v is not None}


def plant_vl(bypass=True, second=None, he5=None, solver=None, column_extra=None):
    """The closed plant (model.plant_blocks) with the column's vapour + liquid condenser in place of the partial condenser
    and FLASH-COND: liquid distillate -> 31-MEOH; vapour distillate -> 32 -> MIXER5. With bypass, H2, CO and N2 of
    stream 29 go round the column and join 32 (workaround M1)."""
    B, S = M.plant_blocks("partial", None, column_second={"reflux_ratio": 2, "bottoms_kmol_h": 4581}, bypass=bypass)
    second = second if second is not None else {"reflux_ratio": 2, "bottoms_kmol_h": 4581}
    B = [b for b in B if b["id"] != "FLASH-COND"]
    for b in B:
        if b["id"] == "COLUMN":
            b["spec"] = vl_column(second, **(column_extra or {}))
        if b["id"] == "HE5" and he5 is not None:
            b["spec"] = he5
    S = [s for s in S if s["id"] not in ("D", "D2", "32", "31-MEOH")]
    S.append(M.st("31-MEOH", "COLUMN.distillate", "P-31-MEOH.in"))
    if bypass:
        S += [M.st("32-col", "COLUMN.vapour_distillate", "MIX-TOP.in"), M.st("32", "MIX-TOP.out", "MIXER5.in")]
    else:
        S.append(M.st("32", "COLUMN.vapour_distillate", "MIXER5.in"))
    return M.req(M.doc(B, S, reactions=M.reactions(), solver=solver or {"maxIterations": 200, "tolerance": 1e-7}))


def warm(r):
    """The same request with the tear streams' guesses taken from Lab's converged 0.6.2 plant (run plant-a6, CHEPTA run
    run-mwgbv28a-1) in place of the paper's values: a start only; the converged answer does not depend on it."""
    r = copy.deepcopy(r)
    a6 = json.loads((OLD / "plant-a6.output.json").read_text())["value"]["streams"]
    for s in r["input"]["flowsheet"]["streams"]:
        if s.get("tear"):
            t = a6[s["id"]]
            s["guess"] = {"flow_kmol_h": {k: round(v, 6) for k, v in t["flow_kmol_h"].items() if v > 0}, "T_K": round(t["T_K"], 4), "P_kPa": t["P_kPa"]}
    return r


def column_alone(comps=None, second=None, T_K=T53, **extra):
    """The paper's column feed 29 into the vapour + liquid column; comps limits the components (None: all six)."""
    r = M.single({"id": "COLUMN", "type": "column", "spec": vl_column(second or {"reflux_ratio": 2, "bottoms_kmol_h": 4581}, T_K, **extra)},
                 [("29", "in")], ["distillate", "vapour_distillate", "bottoms"])
    r["input"]["flowsheet"]["streams"] = [dict(s, id={"out-distillate": "31-MEOH", "out-vapour_distillate": "32", "out-bottoms": "30-WATER"}.get(s["id"], s["id"]))
                                          for s in r["input"]["flowsheet"]["streams"]]
    return M.with_components(r, comps) if comps else r


def runs():
    R = {}
    tri = ["carbon-dioxide", "methanol", "water"]
    S2 = {"reflux_ratio": 2, "bottoms_kmol_h": 4581}
    # --- the column alone (paper feed 29)
    R["vl-column-CO2-MeOH-H2O"] = column_alone(tri)
    R["vl-column-CO2-MeOH-H2O-R2.1273"] = column_alone(tri, {"reflux_ratio": 2.1273, "bottoms_kmol_h": 4581})
    R["vl-column-full"] = column_alone()                               # with H2, CO, N2 traces (M1)
    R["vl-column-CO2-MeOH-H2O-purity"] = column_alone(tri, {"reflux_ratio": 2, "specifications": [
        {"kind": "purity", "product": "bottoms", "component": "water", "value": 0.99985, "basis": "mole"}]})   # M2
    R["vl-column-CO2-MeOH-H2O-boilup"] = column_alone(tri, {"reflux_ratio": 2, "boilup_ratio": 1.17155})
    # --- the closed plant
    R["plant-vl"] = plant_vl()                                         # M5 replaced; M1, M2, M4 workarounds kept
    R["plant-vl-nobypass"] = plant_vl(bypass=False)                    # M1 removed
    R["plant-vl-purity"] = plant_vl(second={"reflux_ratio": 2, "specifications": [
        {"kind": "purity", "product": "bottoms", "component": "water", "value": 0.99985, "basis": "mole"}]})  # M2 removed
    R["plant-vl-recovery"] = plant_vl(second={"reflux_ratio": 2, "specifications": [
        {"kind": "recovery", "product": "bottoms", "component": "water", "value": 0.99987}]})                  # M2, recovery
    R["plant-vl-boilup"] = plant_vl(second={"reflux_ratio": 2, "boilup_ratio": 1.17155})                     # plant-a5 again (M3)
    R["plant-vl-boilup-maxit100"] = plant_vl(second={"reflux_ratio": 2, "boilup_ratio": 1.17155}, column_extra={"max_iterations": 100})
    R["plant-vl-he5-nozones"] = plant_vl(he5={"dTmin_K": 2})            # M4 removed
    R["plant-vl-R2.1273"] = plant_vl(second={"reflux_ratio": 2.1273, "bottoms_kmol_h": 4581})
    # --- the same, started from the converged 0.6.2 plant's tear streams (plant-vl stopped on Broyden's extrapolated guess)
    R["plant-vl-warm"] = warm(R["plant-vl"])
    R["plant-vl-direct"] = plant_vl(solver={"method": "direct", "maxIterations": 300, "tolerance": 1e-7})
    R["plant-vl-warm-direct"] = warm(R["plant-vl-direct"])
    # --- the column alone fed with the 0.6.2 plant's column feed (29-col of plant-a6: CO2 0.24 %, not the paper's 1.285 %),
    #     with each of the condenser's three specifications (53 C; the vapour flow and share of plant-a6's 53 C flash)
    a6 = json.loads((OLD / "plant-a6.output.json").read_text())["value"]["streams"]
    f29 = a6["29-col"]
    a6feed = {"flow_kmol_h": {k: round(v, 6) for k, v in f29["flow_kmol_h"].items() if v > 0}, "T_K": round(f29["T_K"], 4), "P_kPa": f29["P_kPa"]}
    v32, l31 = a6["32"]["F_kmol_h"], a6["31-MEOH"]["F_kmol_h"]
    for tag, extra in (("T53", {}), ("V38.56", {"vapour_distillate_kmol_h": round(v32, 2)}), ("share", {"vapour_share": round(v32 / (v32 + l31), 6)})):
        r = column_alone(tri)
        r["input"]["flowsheet"]["blocks"][0]["spec"] = a6feed
        cs = r["input"]["flowsheet"]["blocks"][1]["spec"]
        if extra:
            cs.pop("condenser_T_K")
            cs.update(extra)
        R[f"vl-column-a6feed-{tag}"] = r
    # --- the plant with the condenser fixed by its vapour flow or vapour share in place of 53 C (workaround for M6; values
    #     from plant-a6's 53 C flash), started from plant-a6; CHEPTA's design specifications cannot vary a column key
    sh = round(v32 / (v32 + l31), 6)
    R["plant-vl-V38.56-warm"] = warm(plant_vl(column_extra={"vapour_distillate_kmol_h": round(v32, 2), "condenser_T_K": None}))
    R["plant-vl-share"] = plant_vl(column_extra={"vapour_share": sh, "condenser_T_K": None})   # from the paper's guesses
    R["plant-vl-share-warm"] = warm(plant_vl(column_extra={"vapour_share": sh, "condenser_T_K": None}))
    R["plant-vl-share-warm-nobypass"] = warm(plant_vl(bypass=False, column_extra={"vapour_share": sh, "condenser_T_K": None}))
    R["plant-vl-share-warm-nobypass-nozones"] = warm(plant_vl(bypass=False, he5={"dTmin_K": 2}, column_extra={"vapour_share": sh, "condenser_T_K": None}))
    R["plant-vl-share-warm-purity"] = warm(plant_vl(second={"reflux_ratio": 2, "specifications": [
        {"kind": "purity", "product": "bottoms", "component": "water", "value": 0.99985, "basis": "mole"}]}, column_extra={"vapour_share": sh, "condenser_T_K": None}))
    # --- HE5 alone (2 K approach, default zones) fed with plant-a6's streams 20 and 28 (M4 inside the loop)
    def a6s(sid):
        t = a6[sid]
        return {"flow_kmol_h": {k: round(v, 6) for k, v in t["flow_kmol_h"].items() if v > 0}, "T_K": round(t["T_K"], 4), "P_kPa": t["P_kPa"]}
    for tag, he in (("dTmin2", {"dTmin_K": 2}), ("dTmin2-zones10", {"dTmin_K": 2, "zones": 10})):
        r = M.single({"id": "HE5", "type": "hx", "spec": he}, [("20", "hot"), ("28", "cold")], ["hot", "cold"])
        r["input"]["flowsheet"]["blocks"][0]["spec"] = a6s("20")
        r["input"]["flowsheet"]["blocks"][1]["spec"] = a6s("28")
        R[f"he5-a6streams-{tag}"] = r
    # --- the 0.6.2 capability-request inputs, unchanged
    for rid in ("diag-feed29-bubble-plus-CO", "diag-feed29-bubble-plus-N2", "mini-bubble-CO-1000ppm", "u-column-partial-pr",
                "u-column-partial-flash53-purity", "diag-column-recovery-0.99987",
                "diag-column-partialside-T53-CO2-MeOH-H2O-maxit100", "diag-column-partialside-T53-CO2-MeOH-H2O-maxit5",
                "u-he5-dTmin2", "plant-a6"):
        R[f"rerun-{rid}"] = json.loads((OLD / f"{rid}.request.json").read_text())
    return R


# ------------------------------------------------------------------------------------------------------------------
def main():
    OUT.mkdir(exist_ok=True)
    head = subprocess.run(["git", "-C", str(SRC), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != COMMIT:
        sys.exit(f"expected CHEPTA checkout at {COMMIT}, got {head!r}")
    cmd = ["node", str(SRC / "bin" / "chepta.mjs")]
    v = subprocess.run(cmd + ["--version"], capture_output=True, text=True).stdout.strip()
    only = os.environ.get("MEOH_ONLY")
    done = []
    for rid, rq in runs().items():
        if only and rid not in only.split(","):
            continue
        run_id = rid
        if (OUT / f"{run_id}.output.json").exists():
            k = 2
            while (OUT / f"{rid}-r{k}.output.json").exists():
                k += 1
            run_id = f"{rid}-r{k}"
        rq = copy.deepcopy(rq)
        f = OUT / f"{run_id}.request.json"
        f.write_text(json.dumps(rq, indent=2) + "\n")
        t0 = datetime.datetime.now(datetime.timezone.utc)
        try:
            p = subprocess.run(cmd + ["request", "--time-ms", TIME_MS, str(f)], capture_output=True, text=True, timeout=WALL_S)
        except subprocess.TimeoutExpired as e:
            p = subprocess.CompletedProcess(e.cmd, returncode=-9, stdout="",
                                            stderr=f"Stopped by Lab's runner after {WALL_S} s of wall time (CHEPTA's --time-ms {TIME_MS} had not stopped it).\n")
        (OUT / f"{run_id}.output.json").write_text(p.stdout)
        # CHEPTA refuses unknown request keys, so the commit is recorded in the stderr file's first line and the manifest
        (OUT / f"{run_id}.stderr.txt").write_text(f"# CHEPTA-Lab: run on CHEPTA main {COMMIT} (unreleased); CHEPTA's stderr follows\n" + p.stderr)
        try:
            res = json.loads(p.stdout) if p.stdout.strip() else {}
        except json.JSONDecodeError:
            res = {}
        err = res.get("error") or {}
        rec = {"id": run_id, "chepta_commit": COMMIT, "command": f"node <CHEPTA {COMMIT[:7]}>/bin/chepta.mjs request --time-ms {TIME_MS} {f.relative_to(H)}",
               "started_at": t0.isoformat(), "exit_code": p.returncode, "exit_meaning": EXIT.get(p.returncode, "unknown"),
               "outcome": res.get("outcome"), "error_code": err.get("code"), "error_message": err.get("message"),
               "chepta_run_id": (res.get("run") or {}).get("id"), "elapsed_ms": (res.get("run") or {}).get("elapsed_ms"),
               "request_file": f"{OUT.name}/{run_id}.request.json", "output_file": f"{OUT.name}/{run_id}.output.json",
               "stderr_file": f"{OUT.name}/{run_id}.stderr.txt",
               "request_file_sha256": sha(f.read_bytes()), "output_file_sha256": sha(p.stdout.encode())}
        done.append(rec)
        print(run_id, "exit", p.returncode, res.get("outcome"), err.get("code", ""), (err.get("message") or "")[:400], flush=True)
        man_f = OUT / "run-manifest.json"
        old = json.loads(man_f.read_text()) if man_f.exists() else {"runs": []}
        ids = {r["id"] for r in done}
        man = {"engine": f"CHEPTA main {COMMIT} (source checkout, unreleased; its package.json says {v}); Lab's pin stays chepta 0.6.2",
               "chepta_commit": COMMIT, "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
               "interface": "node bin/chepta.mjs request --time-ms N <file> (command line)",
               "source": "Lacerda de Oliveira Campos et al. 2022, Processes 10, 1535 (CC BY 4.0)",
               "model_py_sha256": sha((H / "model.py").read_bytes()), "runner_sha256": sha(Path(__file__).read_bytes()),
               "settings": [list(s) for s in M.SETTINGS] + [list(s) for s in VL_SETTINGS], "kinetics_rights": M.KINETICS_RIGHTS,
               "runs": sorted([r for r in old["runs"] if r["id"] not in ids] + done, key=lambda r: r["started_at"])}
        man_f.write_text(json.dumps(man, indent=1) + "\n")


if __name__ == "__main__":
    main()
