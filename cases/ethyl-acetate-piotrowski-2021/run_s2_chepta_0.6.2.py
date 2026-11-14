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
EXIT_OF = {"ok": 0, "invalid_input": 2, "missing_data": 3, "unsupported": 4, "not_converged": 5, "cancelled": 6, "out_of_time": 7, "error": 8}
# round 2 (after the maintainer's advice, 2026-11-13): long plant runs executed once from the scratch folder (name there,
# --time-ms used); with S2_IMPORT_DIR set their outputs are copied instead of running them again
IMPORTS = {"plant62-R-dist-col15purity": ("rd", 3400000), "plant62-W-dist-col15purity": ("wd", 3400000),
           "plant62-R-dist-col15purity-direct": ("rdd", 3400000), "plant62-W-dist-col15purity-direct": ("wdd", 3400000),
           "plant62-R-bottoms-col15purity": ("p15R", 1600000), "plant62-R-purity-col15purity-warm": ("p15Rp", 1600000),
           "plant62-R-bottoms-col5-14stages": ("k14R", 1600000),
           "plant62-R-dist-col15purity-direct-tol1e-5": ("rddt", 7000000), "plant62-W-dist-col15purity-direct-tol1e-5": ("wddt", 7000000),
           "plant62-R-dist-col15purity-tol3e-4": ({"split16": "R", "spec11": "distillate", "spec15": "purity", "tolerance": 3e-4},
                                           "CLOSED: R (23 = 95,797 kg/h), column 11 distillate 230.4 kmol/h, column 15 on 99.99 % water; Broyden, tear tolerance 3e-4 (it plateaus near 2e-4)"),
    "plant62-W-dist-col15purity-tol5e-4": ({"split16": "W", "spec11": "distillate", "spec15": "purity", "tolerance": 5e-4},
                                           "CLOSED: W (25 = 20,000 kg/h), otherwise as plant62-R-dist-col15purity-tol3e-4; tear tolerance 5e-4"),
    "plant62-R-dist240-col15purity-tol3e-4": ({"split16": "R", "spec11": 240, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 240 kmol/h (tuned to the product purity)"),
    "plant62-R-dist245-col15purity-tol3e-4": ({"split16": "R", "spec11": 245, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 245 kmol/h"),
    "plant62-R-dist248-col15purity-tol3e-4": ({"split16": "R", "spec11": 248, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 248 kmol/h"),
    "plant62-R-dist255-col15purity-tol3e-4": ({"split16": "R", "spec11": 255, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 255 kmol/h"),
    "plant62-R-dist240-RD3.5-col15purity-tol3e-4": ({"split16": "R", "spec11": 240, "spec15": "purity", "tolerance": 3e-4, "reflux11": 3.5}, "as -dist240, column 11 R/D 3.5"),
    "plant62-R-dist240-RD4-col15purity-tol3e-4": ({"split16": "R", "spec11": 240, "spec15": "purity", "tolerance": 3e-4, "reflux11": 4}, "as -dist240, column 11 R/D 4"),
    "plant62-R-dist250-col15purity-tol3e-4": ({"split16": "R", "spec11": 250, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 250 kmol/h"),
    "plant62-R-dist260-col15purity-tol3e-4": ({"split16": "R", "spec11": 260, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 260 kmol/h"),
    "plant62-R-dist-col15d405-direct-tol1e-5": ("r405t", 7000000),
           "plant62-R-dist-col15purity-tol3e-4": ("rdt3", 3400000), "plant62-W-dist-col15purity-tol5e-4": ("wdt5", 3400000),
           "plant62-R-dist240-col15purity-tol3e-4": ("rd240", 3400000), "plant62-R-dist250-col15purity-tol3e-4": ("rd250", 3400000),
           "plant62-R-dist260-col15purity-tol3e-4": ("rd260", 3400000), "plant62-R-dist245-col15purity-tol3e-4": ("rd245", 3400000),
           "plant62-R-dist248-col15purity-tol3e-4": ("rd248", 3400000), "plant62-R-dist255-col15purity-tol3e-4": ("rd255", 3400000),
           "plant62-R-dist240-RD3.5-col15purity-tol3e-4": ("rd240r35", 3400000), "plant62-R-dist240-RD4-col15purity-tol3e-4": ("rd240r4", 3400000)}
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
        imp = IMPORTS.get(run_id)
        idir = os.environ.get("S2_IMPORT_DIR")
        if imp and idir and (Path(idir) / f"{imp[0]}.out.json").exists():
            # a long run already executed by this session with the same chepta 0.6.2 command line: its request must be
            # the same document (compared parsed); its output is copied unchanged and the manifest says so
            src_req = json.loads((Path(idir) / f"{imp[0]}.json").read_text())
            if src_req != req:
                sys.exit(f"{run_id}: the scratch request {imp[0]}.json differs from the request built here")
            out = (Path(idir) / f"{imp[0]}.out.json").read_text()
            p = subprocess.CompletedProcess([], returncode=EXIT_OF.get(json.loads(out).get("outcome"), 8), stdout=out, stderr="")
            note = (note + "; " if note else "") + (f"executed 2026-11-13 by this session as chepta request --time-ms {imp[1]} <file> "
                                                     "(the same request document); output copied unchanged into this folder")
        else:
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


PLANTS2 = {
    "plant62-R-bottoms-col5-14stages": ({"split16": "R", "spec11": "bottoms", "col5_stages": 14}, "column 5 with 14 stages (Section 3.2: 'a minimum number of 14 theoretical stages')"),
    "plant62-R-bottoms-col15purity": ({"split16": "R", "spec11": "bottoms", "spec15": "purity"}, "column 15 on its bottoms purity (99.99 mass % water, Section 3.5) instead of the distillate flow; column 11 bottoms 141.5 kmol/h"),
    "plant62-R-purity-col15purity-warm": ({"split16": "R", "spec11": "purity", "spec15": "purity", "guesses": "061"}, "both product columns on their purities (99.90 % ester, 99.99 % water)"),
    "plant62-R-dist-col15purity": ({"split16": "R", "spec11": "distillate", "spec15": "purity"}, "column 11 R/D 3 and distillate 230.4 kmol/h (product purity a result), column 15 on 99.99 % water; Broyden"),
    "plant62-W-dist-col15purity": ({"split16": "W", "spec11": "distillate", "spec15": "purity"}, "as plant62-R-dist-col15purity with 25 = 20,000 kg/h"),
    "plant62-R-dist-col15purity-direct": ({"split16": "R", "spec11": "distillate", "spec15": "purity", "method": "direct"}, "as plant62-R-dist-col15purity, direct substitution"),
    "plant62-W-dist-col15purity-direct": ({"split16": "W", "spec11": "distillate", "spec15": "purity", "method": "direct"}, "as plant62-W-dist-col15purity, direct substitution"),
    "plant62-R-dist-col15purity-direct-tol1e-5": ({"split16": "R", "spec11": "distillate", "spec15": "purity", "method": "direct", "tolerance": 1e-5}, "as -direct, tear tolerance 1e-5"),
    "plant62-W-dist-col15purity-direct-tol1e-5": ({"split16": "W", "spec11": "distillate", "spec15": "purity", "method": "direct", "tolerance": 1e-5}, "as -direct, tear tolerance 1e-5"),
    "plant62-R-dist-col15purity-tol3e-4": ({"split16": "R", "spec11": "distillate", "spec15": "purity", "tolerance": 3e-4},
                                           "CLOSED: R (23 = 95,797 kg/h), column 11 distillate 230.4 kmol/h, column 15 on 99.99 % water; Broyden, tear tolerance 3e-4 (it plateaus near 2e-4)"),
    "plant62-W-dist-col15purity-tol5e-4": ({"split16": "W", "spec11": "distillate", "spec15": "purity", "tolerance": 5e-4},
                                           "CLOSED: W (25 = 20,000 kg/h), otherwise as plant62-R-dist-col15purity-tol3e-4; tear tolerance 5e-4"),
    "plant62-R-dist240-col15purity-tol3e-4": ({"split16": "R", "spec11": 240, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 240 kmol/h (tuned to the product purity)"),
    "plant62-R-dist245-col15purity-tol3e-4": ({"split16": "R", "spec11": 245, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 245 kmol/h"),
    "plant62-R-dist248-col15purity-tol3e-4": ({"split16": "R", "spec11": 248, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 248 kmol/h"),
    "plant62-R-dist255-col15purity-tol3e-4": ({"split16": "R", "spec11": 255, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 255 kmol/h"),
    "plant62-R-dist240-RD3.5-col15purity-tol3e-4": ({"split16": "R", "spec11": 240, "spec15": "purity", "tolerance": 3e-4, "reflux11": 3.5}, "as -dist240, column 11 R/D 3.5"),
    "plant62-R-dist240-RD4-col15purity-tol3e-4": ({"split16": "R", "spec11": 240, "spec15": "purity", "tolerance": 3e-4, "reflux11": 4}, "as -dist240, column 11 R/D 4"),
    "plant62-R-dist250-col15purity-tol3e-4": ({"split16": "R", "spec11": 250, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 250 kmol/h"),
    "plant62-R-dist260-col15purity-tol3e-4": ({"split16": "R", "spec11": 260, "spec15": "purity", "tolerance": 3e-4}, "as -tol3e-4, column 11 distillate 260 kmol/h"),
    "plant62-R-dist-col15d405-direct-tol1e-5": ({"split16": "R", "spec11": "distillate", "spec15": 405, "method": "direct", "tolerance": 1e-5}, "column 15 distillate 405 kmol/h (from the column 15 isolated runs), direct, tolerance 1e-5"),
}


def isolate_requests():
    """Each separation block alone in CHEPTA, its inlet and outlet specifications varied (the maintainer, 2026-11-13)."""
    import copy
    J = {}
    c5 = dict(M.column5_spec(), phases="VLL")
    base = M.unit({"id": "SCDS5", "type": "column", "spec": c5}, [("in", 27), ("in", 6)], [("distillate", 8), ("bottoms", 7)])
    r2 = json.loads((OLD / "diag-scds5-round2-inlets-VLL.request.json").read_text())["input"]["flowsheet"]
    r2["blocks"][0]["spec"] = c5
    mw = {"ethanol": 46.069, "water": 18.015, "ethyl-acetate": 88.106, "acetic-acid": 60.052}  # scaling only
    for tag, d0 in (("paper", base), ("r2", r2)):
        for kg in (45000, 50000, 55000, 60000, 65000, 70000):
            d = copy.deepcopy(d0)
            for b in d["blocks"]:
                if b["id"] == "F27":
                    sp = b["spec"]
                    key = "flow_kg_h" if "flow_kg_h" in sp else "flow_kmol_h"
                    tot = sum(sp[key].values()) if key == "flow_kg_h" else sum(v * mw[k] for k, v in sp[key].items())
                    sp[key] = {k: v * kg / tot for k, v in sp[key].items()}
            J[f"iso-scds5-{tag}-reflux{kg}"] = d

    def col11(acid_pct, bottoms):
        f = M.feed_spec(13)
        fl = f["flow_kg_h"]
        tot = sum(fl.values())
        fl["acetic acid"] = tot * acid_pct / 100
        if acid_pct == 0:
            fl.pop("acetic acid")
        sp = M.column11_spec("flow", "VLL")
        sp["bottoms_kmol_h"] = bottoms
        blocks = [{"id": "SCDS11", "type": "column", "spec": sp}, {"id": "F13", "type": "feed", "spec": f},
                  {"id": "P14", "type": "product"}, {"id": "P16", "type": "product"}]
        streams = [{"id": "S13", "from": "F13.out", "to": "SCDS11.in"}, {"id": "S14", "from": "SCDS11.distillate", "to": "P14.in"},
                   {"id": "S16", "from": "SCDS11.bottoms", "to": "P16.in"}]
        return M.doc(blocks, streams, M.COMPONENTS if acid_pct > 0 else M.COMPONENTS_B)
    for a in (0, 0.001, 0.005, 0.01):
        J[f"iso-scds11-acid{a}-bottoms141.5"] = col11(a, 141.5)
    for b in (139, 140, 141):
        J[f"iso-scds11-acid0.01-bottoms{b}"] = col11(0.01, b)
        J[f"iso-scds11-acid0-bottoms{b}"] = col11(0, b)

    def col15(dist=None, purity=None):
        sp = M.column15_spec("VLL")
        if dist:
            sp["distillate_kmol_h"] = dist
        if purity:
            sp.pop("distillate_kmol_h")
            sp["bottoms_purity"] = {"component": "water", "value": purity, "basis": "mass"}
        return M.unit({"id": "SCDS15", "type": "column", "spec": sp}, [("in", 28)], [("distillate", 21), ("bottoms", 22)])
    for d in (380, 390, 394.6, 400, 410, 420):
        J[f"iso-scds15-distillate{d}"] = col15(dist=d)
    J["iso-scds15-purity0.9999"] = col15(purity=0.9999)
    return J


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
    if "isolate" in groups:
        run_parallel(R, [(k, fs(v)) for k, v in isolate_requests().items()])
    if "plant2" in groups:
        run_parallel(R, [(k, fs(build_plant(kw)), what) for k, (kw, what) in PLANTS2.items()])
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
        "plants": {k: {"kwargs": kw, "what": what} for k, (kw, what) in {**PLANTS, **PLANTS2}.items()},
        "plants_note": "open_recycles \"open\": streams 27 and 21 fed with Table A2 (27 as printed, 21 saturated liquid); guesses \"061\": tear guesses from 0.6.1 runs plant-a2-r01-A/B",
        "runs": [r for r in old["runs"] if r["id"] not in new_ids] + R.runs,
    }
    man_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
