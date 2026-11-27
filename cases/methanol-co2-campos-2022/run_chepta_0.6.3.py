#!/usr/bin/env python3
"""The one-step CO2-to-methanol plant (Lacerda de Oliveira Campos et al. 2022) on chepta@0.6.3, the release pinned in
Lab's package.json. Only the runs that CHEPTA's 0.6.3 advice changes are run (the maintainer, relayed 2026-11-27: do
not re-run the 0.6.2 tests to compare):

- thermo PR + gE (MHV1) in place of PR with k_ij (CHEPTA lab-notes-0.6.3, advice 2; feature 10);
- the methanol column specified by what matters (a reboiler temperature, a flow ratio, a recovery, a component ratio)
  in place of the bottoms flow 4581 kmol/h (advice 3; feature 6), each scanned around the paper's value;
- HE5 by its 2 K approach without `zones: 10` (advice 4; feature 9);
- the reactors at the paper's average U, 155 W/m2/K (article pp. 13-14: U 160 at the inlet, 150 at the outlet, the
  average given to Aspen), in place of the assumed 300;
- the closed plant with all of these, on PR + MHV1 (CHEPTA's known limit: MIXER1 and CP3) and on PR.

Every run is called with `chepta request FILE --summary --out FILE.output.json`: the full result is kept unchanged in
`<id>.output.json`, the summary (stdout) in `<id>.summary.json`, stderr in `<id>.stderr.txt`. A rerun never overwrites
a kept run. Run from the repository root after `npm ci`:

  python3 cases/methanol-co2-campos-2022/run_chepta_0.6.3.py            # all
  MEOH_ONLY=id1,id2 python3 ...                                         # only those ids
"""
import copy
import datetime
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import model as M  # noqa: E402
import run_chepta_main_415da41 as V  # noqa: E402  (plant_vl, column_alone, warm: request builders only)

VERSION = "0.6.3"
OUT = H / f"results-chepta-{VERSION}"
OLD415 = H / "results-chepta-main-415da41"
EXIT = {-9: "stopped by Lab (wall time)", 0: "ok", 2: "invalid_input", 3: "missing_data", 4: "unsupported", 5: "not_converged",
        6: "cancelled", 7: "out_of_time", 8: "error", 1: "command line error"}
TIME_MS = os.environ.get("MEOH_TIME_MS", "1200000")
WALL_S = int(os.environ.get("MEOH_WALL_S", "1500"))
MHV1 = M.THERMO_MHV1
U_PAPER = 155.0   # W/m2/K, article p.14 (Uavg); Uz=0 160 (p.13), Uz=12.5 150 (p.14)

# Paper values the column specifications are scanned around (derived from Table S9/S10, streams 29, 30-WATER, 31-MEOH)
F29 = 9412.0
B30 = 4581.0
MEOH_FEED = F29 * 0.50041                       # 4709.9 kmol/h
MEOH_31 = 4542.0 * 0.99667                      # 4526.9 kmol/h
REC_MEOH_31 = round(MEOH_31 / MEOH_FEED, 5)     # 0.96114, methanol to the liquid distillate (derived)
FLOW_RATIO_B_F = round(B30 / F29, 5)            # 0.48672 (derived)
RATIO_B_MEOH_W = round(0.015 / 99.985, 6)       # 0.00015 methanol/water in 30-WATER (derived; 0.015 % printed to 3 decimals)

SETTINGS_063 = [
    ("property method (0.6.3 runs)", "PR + gE (MHV1), thermo {model: PR, mixing: MHV1}; PR with k_ij kept for comparison", "assumed",
     "CHEPTA lab-notes-0.6.3 advice 2 and feature 10 (decisions 2026-11-20-01, 2026-11-25-01); paper: PR in the reactors, NRTL2 elsewhere (article p.9)"),
    ("reactor overall U (0.6.3 runs)", f"{U_PAPER} W/m2/K, constant", "paper",
     "article p.13-14: 'Uz=0 = 160 W m-2 K-1 and Uz=12.5 = 150 ... the average value was used (Uavg = 155)'"),
    ("HE5 (0.6.3 runs)", "dTmin_K 2, no zones key", "assumed", "CHEPTA lab-notes-0.6.3 advice 4, feature 9; the paper fixes 21 at 62 C and 29 at 82.9 C"),
    ("column (0.6.3 runs)", "condenser vapour_liquid at 53 C, reflux ratio 2 (over the liquid distillate), and one of: reboiler_T_K, flow_ratio bottoms/feed, recovery of methanol in the liquid distillate, component_ratio methanol/water in the bottoms",
     "paper + derived", f"supplement p.10 (30 stages, feed 24, R 2, 53 C); derived from Table S9/S10: B/F {FLOW_RATIO_B_F}, methanol recovery to 31-MEOH {REC_MEOH_31}, bottoms methanol/water {RATIO_B_MEOH_W}; 30-WATER at 99.6 C"),
    ("column feed traces (0.6.3 runs)", "H2, CO, N2 through the column (no bypass)", "paper", "Table S10 stream 29"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def thermo(r, th):
    r = copy.deepcopy(r)
    r["input"]["flowsheet"]["thermo"] = copy.deepcopy(th)
    return r


def set_block(r, bid, spec):
    for b in r["input"]["flowsheet"]["blocks"]:
        if b["id"] == bid:
            b["spec"] = spec
    return r


def reactor(U, th):
    return M.single({"id": "REACTOR1", "type": "pfr", "spec": M.reactor_spec(U)}, [("15", "in")], ["out"], thermo=th, rx=M.reactions())


def column(second, th=MHV1, T_K=V.T53, **extra):
    """The paper's feed 29 (all six components) into the vapour + liquid column."""
    return thermo(V.column_alone(None, second, T_K, **extra), th)


def plant(th, second, U=U_PAPER, he5=None, bypass=False, column_extra=None, solver=None, warm=False):
    r = V.plant_vl(bypass=bypass, second=second, he5=he5 or {"dTmin_K": 2}, solver=solver, column_extra=column_extra)
    r = thermo(r, th)
    for b in r["input"]["flowsheet"]["blocks"]:
        if b["type"] == "pfr":
            b["spec"]["coolant"]["U_W_m2K"] = U
    if warm:   # tears from Lab's converged 415da41 plant (plant-vl-share-warm-nobypass): a start only
        old = json.loads((OLD415 / "plant-vl-share-warm-nobypass.output.json").read_text())["value"]["streams"]
        for s in r["input"]["flowsheet"]["streams"]:
            if s.get("tear"):
                t = old[s["id"]]
                s["guess"] = {"flow_kmol_h": {k: round(v, 6) for k, v in t["flow_kmol_h"].items() if v > 0}, "T_K": round(t["T_K"], 4), "P_kPa": t["P_kPa"]}
    return r


def runs():
    R = {}
    # --- 1. units on the paper's inlets, PR + MHV1 (the separator first)
    for rid in ("u-flash3", "u-flash1", "u-flash2", "u-flash4", "u-valve1", "u-mixer1", "u-mixer4", "u-cp1", "u-cp2", "u-cp3",
                "u-cprec", "u-he7", "u-he4", "u-he6", "u-he2"):
        R[f"{rid}-mhv1"] = thermo(M.unit_runs()[rid], MHV1)
    # --- 2. HE5 by its 2 K approach, no zones: paper streams; and the 0.6.2 plant's streams (where the loop met the cross)
    he5 = M.single({"id": "HE5", "type": "hx", "spec": {"dTmin_K": 2}}, [("20", "hot"), ("28", "cold")], ["hot", "cold"])
    R["u-he5-dTmin2-pr"] = he5
    R["u-he5-dTmin2-mhv1"] = thermo(he5, MHV1)
    R["u-he5-a6streams-dTmin2-pr"] = json.loads((OLD415 / "he5-a6streams-dTmin2.request.json").read_text())
    # --- 3. reactor at the paper's U (PR as the paper's reactors; MHV1 as the plant)
    R["u-reactor-U155-pr"] = reactor(U_PAPER, M.THERMO_PR)
    R["u-reactor-U155-mhv1"] = reactor(U_PAPER, MHV1)
    # --- 4. the column alone, paper feed 29 with its traces, vapour + liquid condenser at 53 C, R 2, MHV1
    R["col-mhv1-B4581"] = column({"reflux_ratio": 2, "bottoms_kmol_h": B30})
    for T in (372.75, 373.15, 373.5, 374.0, 374.5):   # 30-WATER at 99.6 C = 372.75 K
        R[f"col-mhv1-TB{T}"] = column({"reflux_ratio": 2, "reboiler_T_K": T})
    for v in (0.485, FLOW_RATIO_B_F, 0.488):
        R[f"col-mhv1-BF{v}"] = column({"reflux_ratio": 2, "specifications": [{"kind": "flow_ratio", "numerator": "bottoms", "denominator": "feed", "value": v}]})
    for v in (0.955, REC_MEOH_31, 0.965):
        R[f"col-mhv1-recMeOH{v}"] = column({"reflux_ratio": 2, "specifications": [{"kind": "recovery", "product": "distillate", "component": "methanol", "value": v}]})
    for v in (5e-5, RATIO_B_MEOH_W, 5e-4):
        R[f"col-mhv1-ratioB{v}"] = column({"reflux_ratio": 2, "specifications": [{"kind": "component_ratio", "product": "bottoms", "component": "methanol",
                                                                                   "relative_to": "water", "value": v, "basis": "mole"}]})
    R["col-pr-B4581"] = column({"reflux_ratio": 2, "bottoms_kmol_h": B30}, th=M.THERMO_PR)
    R.update(mini_runs())
    return R


def mini_runs():
    """The smallest input found for the PR + MHV1 failure 'PR: no physical root' (Lab's search, 2026-11-27: stream 39-REC
    with one component left out at a time, then H2 + water with each other component): an adiabatic heater (a P-H flash)
    on H2 + CO2 + water in 39-REC's proportions (Table S10, mole %), 33 C, 100 kPa. Controls: the same on PR; the same
    with a temperature specification (a T-P flash); H2 + water alone; CO2 + water alone."""
    R = {}
    s = M.STREAMS["39-REC"]["mol_pct"]
    def heater(flows, spec, th):
        d = {"components": list(flows), "thermo": copy.deepcopy(th),
             "blocks": [{"id": "F1", "type": "feed", "spec": {"flow_kmol_h": flows, "T_K": 306.15, "P_kPa": 100}},
                        {"id": "H1", "type": "heater", "spec": spec}, M.prod("P1")],
             "streams": [M.st("S1", "F1.out", "H1.in"), M.st("S2", "H1.out", "P1.in")]}
        return M.req(d)
    tri = {"hydrogen": s["H2"], "carbon-dioxide": s["CO2"], "water": s["H2O"]}
    R["mini-ph-H2-CO2-H2O-mhv1"] = heater(tri, {"duty_kW": 0}, MHV1)
    R["mini-ph-H2-CO2-H2O-pr"] = heater(tri, {"duty_kW": 0}, M.THERMO_PR)
    R["mini-tp-H2-CO2-H2O-mhv1"] = heater(tri, {"T_K": 306.15}, MHV1)
    R["mini-ph-H2-H2O-mhv1"] = heater({"hydrogen": s["H2"], "water": s["H2O"]}, {"duty_kW": 0}, MHV1)
    R["mini-ph-CO2-H2O-mhv1"] = heater({"carbon-dioxide": s["CO2"], "water": s["H2O"]}, {"duty_kW": 0}, MHV1)
    R["mini-ph-H2-CO2-mhv1"] = heater({"hydrogen": s["H2"], "carbon-dioxide": s["CO2"]}, {"duty_kW": 0}, MHV1)
    # The CP3 refusal of run plant-mhv1-warm: its error.details give the composition, 300 K and 7000 kPa. A T-P flash of
    # that composition (100 kmol/h), on PR + MHV1 and on PR.
    z = dict(zip(M.COMPONENTS, [0.9819458298265241, 0.0016241502835352437, 8.945224963864467e-05, 0.011663991081144956,
                                0.004390135968595245, 0.0002864405905617678]))
    for tag, th in (("mhv1", MHV1), ("pr", M.THERMO_PR)):
        d = {"components": M.COMPONENTS, "thermo": copy.deepcopy(th),
             "blocks": [{"id": "F1", "type": "feed", "spec": {"flow_kmol_h": {k: round(100 * v, 8) for k, v in z.items()}, "T_K": 318.15, "P_kPa": 1698}},
                        {"id": "FL", "type": "flash", "spec": {"T_K": 300, "P_kPa": 7000}}, M.prod("P1"), M.prod("P2")],
             "streams": [M.st("S1", "F1.out", "FL.in"), M.st("S2", "FL.vapour", "P1.in"), M.st("S3", "FL.liquid", "P2.in")]}
        R[f"mini-tp-cp3-300K-7000kPa-{tag}"] = M.req(d)
    return R


# The column's second and third specifications in the plant, chosen from the column scan (results-chepta-0.6.3/README.md,
# adjustment table): reflux ratio 2 (paper) and the reboiler at 374.0 K (paper 99.6 C = 372.75 K; +1.25 K)
COL2_PLANT = {"reflux_ratio": 2, "reboiler_T_K": 374.0}


def plant_runs(second):
    """The closed plant and two sections with the column specified by `second`."""
    R = {}
    R["plant-mhv1"] = plant(MHV1, second)
    R["plant-mhv1-warm"] = plant(MHV1, second, warm=True)
    R["plant-pr"] = plant(M.THERMO_PR, second)
    R["plant-pr-warm"] = plant(M.THERMO_PR, second, warm=True)
    R["plant-pr-warm-B4581"] = plant(M.THERMO_PR, {"reflux_ratio": 2, "bottoms_kmol_h": B30}, warm=True)
    R["plant-pr-warm-U300"] = plant(M.THERMO_PR, second, U=300.0, warm=True)
    # sections on MHV1 with the paper's streams at the cuts
    for name, keep in (("compression", M.SEC_COMPRESSION), ("loop", M.SEC_LOOP)):
        r = thermo(M.section(keep), MHV1)
        for b in r["input"]["flowsheet"]["blocks"]:
            if b["type"] == "pfr":
                b["spec"]["coolant"]["U_W_m2K"] = U_PAPER
            if b["id"] == "HE5":
                b["spec"] = {"dTmin_K": 2}
        R[f"sec-{name}-mhv1"] = r
    return R


def run_one(cmd, rid, rq, done):
    run_id = rid
    if (OUT / f"{run_id}.output.json").exists():
        k = 2
        while (OUT / f"{rid}-r{k}.output.json").exists():
            k += 1
        run_id = f"{rid}-r{k}"
    f = OUT / f"{run_id}.request.json"
    f.write_text(json.dumps(rq, indent=2) + "\n")
    res_f = OUT / f"{run_id}.output.json"
    t0 = datetime.datetime.now(datetime.timezone.utc)
    try:
        p = subprocess.run(cmd + ["request", "--time-ms", TIME_MS, "--summary", "--out", str(res_f), str(f)],
                           capture_output=True, text=True, timeout=WALL_S)
    except subprocess.TimeoutExpired as e:
        p = subprocess.CompletedProcess(e.cmd, returncode=-9, stdout="",
                                        stderr=f"Stopped by Lab's runner after {WALL_S} s of wall time (CHEPTA's --time-ms {TIME_MS} had not stopped it).\n")
    (OUT / f"{run_id}.summary.json").write_text(p.stdout)
    (OUT / f"{run_id}.stderr.txt").write_text(p.stderr)
    try:
        res = json.loads(res_f.read_text()) if res_f.exists() else {}
    except json.JSONDecodeError:
        res = {}
    if not res_f.exists():
        res_f.write_text("")
    err = res.get("error") or {}
    rec = {"id": run_id, "command": f"chepta request --time-ms {TIME_MS} --summary --out {res_f.relative_to(H)} {f.relative_to(H)}",
           "started_at": t0.isoformat(), "exit_code": p.returncode, "exit_meaning": EXIT.get(p.returncode, "unknown"),
           "outcome": res.get("outcome"), "error_code": err.get("code"), "error_message": err.get("message"),
           "chepta_run_id": (res.get("run") or {}).get("id"), "elapsed_ms": (res.get("run") or {}).get("elapsed_ms"),
           "request_file": f"{OUT.name}/{run_id}.request.json", "output_file": f"{OUT.name}/{run_id}.output.json",
           "summary_file": f"{OUT.name}/{run_id}.summary.json", "stderr_file": f"{OUT.name}/{run_id}.stderr.txt",
           "request_file_sha256": sha(f.read_bytes()), "output_file_sha256": sha(res_f.read_bytes())}
    done.append(rec)
    print(run_id, "exit", p.returncode, res.get("outcome"), err.get("code", ""), (err.get("message") or "")[:300], flush=True)
    man_f = OUT / "run-manifest.json"
    old = json.loads(man_f.read_text()) if man_f.exists() else {"runs": []}
    ids = {r["id"] for r in done}
    man = {"engine": f"chepta {VERSION} (npm, Lab's pin; tag v0.6.3 = commit b6598a5)",
           "node": subprocess.run(["node", "--version"], capture_output=True, text=True).stdout.strip(),
           "interface": "chepta request --time-ms N --summary --out RESULT <file> (command line)",
           "source": "Lacerda de Oliveira Campos et al. 2022, Processes 10, 1535 (CC BY 4.0)",
           "model_py_sha256": sha((H / "model.py").read_bytes()), "runner_sha256": sha(Path(__file__).read_bytes()),
           "settings": [list(s) for s in M.SETTINGS] + [list(s) for s in V.VL_SETTINGS] + [list(s) for s in SETTINGS_063],
           "note": "model.py's SETTINGS describe the 0.6.2 runs; the 0.6.3 settings that replace them are the last entries",
           "kinetics_rights": M.KINETICS_RIGHTS,
           "runs": sorted([r for r in old["runs"] if r["id"] not in ids] + done, key=lambda r: r["started_at"])}
    man_f.write_text(json.dumps(man, indent=1) + "\n")


def main():
    OUT.mkdir(exist_ok=True)
    local = H.parent.parent / "node_modules" / ".bin" / "chepta"
    cmd = [str(local)]
    v = subprocess.run(cmd + ["--version"], capture_output=True, text=True).stdout.strip()
    if v != VERSION:
        sys.exit(f"expected chepta {VERSION} in node_modules, got {v!r}; run npm ci")
    only = os.environ.get("MEOH_ONLY")
    R = runs()
    R.update(plant_runs(COL2_PLANT))
    done = []
    for rid, rq in R.items():
        if only and rid not in only.split(","):
            continue
        run_one(cmd, rid, rq, done)


if __name__ == "__main__":
    main()
