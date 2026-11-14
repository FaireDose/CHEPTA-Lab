#!/usr/bin/env python3
"""Write study-record.json for the one-step methanol plant on chepta 0.6.2, binding every file by sha256.

Reads the run manifest (run_chepta_0.6.2.py) and comparison.json (compare.py). Run after them:
  python3 cases/methanol-co2-campos-2022/build_study_record.py
Then python scripts/dataset_pipeline.py validate. No CHEPTA call; no number typed here except pointers and the
published values' printed text.
"""
import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
REL = H.relative_to(ROOT).as_posix()
R = H / "results-chepta-0.6.2"
MAN = json.loads((R / "run-manifest.json").read_text())
CMP = json.loads((R / "comparison.json").read_text())
SRC = "lacerda-campos-2022"
SIDX = {s["stream"]: i for i, s in enumerate(json.loads((H / "streams.json").read_text())["streams"])}
EIDX = {e["id"]: i for i, e in enumerate(json.loads((H / "equipment.json").read_text())["equipment"])}
CIDX = {r["id"]: i for i, r in enumerate(CMP["runs"])}
PLANT = "plant-a6"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


files = []


def add_file(fid, path, role, base=H):
    files.append({"id": fid, "path": (base / path).relative_to(ROOT).as_posix(), "sha256": sha(base / path), "role": role})


add_file("streams", "streams.json", "case_input")
add_file("equipment", "equipment.json", "case_input")
add_file("model", "model.py", "case_input")
add_file("runner", "run_chepta_0.6.2.py", "runner")
add_file("verifier", "compare.py", "verifier")
add_file("run-manifest", "results-chepta-0.6.2/run-manifest.json", "execution_manifest")
add_file("comparison", "results-chepta-0.6.2/comparison.json", "lab_check")
add_file("engine-lock", "package-lock.json", "engine_lock", base=ROOT)
add_file("case-readme", "README.md", "other")


def variant_of(rid):
    if rid.startswith(("diag-", "mini-")):
        return "diagnostics"
    if rid.startswith("u-"):
        return "units-paper-inlets"
    if rid.startswith("sec-"):
        return "sections-paper-inlets"
    return "plant-one-flowsheet"


runs = []
for i, r in enumerate(MAN["runs"]):
    rid = r["id"].lower()
    add_file(f"request.{rid}", r["request_file"], "request")
    has_result = (H / r["output_file"]).read_bytes().strip() != b""
    if has_result:
        add_file(f"result.{rid}", r["output_file"], "result")
    add_file(f"stderr.{rid}", r["stderr_file"], "other")
    note = None
    if r["outcome"] != "ok":
        note = (f"{r['exit_meaning']} (exit {r['exit_code']}): {r.get('error_code')}: {r.get('error_message')}" if r.get("error_code")
                else f"{r['exit_meaning']} (exit {r['exit_code']}); see the stderr file")
    runs.append({"id": rid, "execution_id": r["id"] if r["id"] != rid else None, "variant": variant_of(r["id"]), "engine": "chepta@0.6.2",
                 "interface": "command_line", "runner": "runner", "request": f"request.{rid}", "result": f"result.{rid}" if has_result else None,
                 "execution_record": {"file": "run-manifest", "pointer": f"/runs/{i}"},
                 "executed_at": {"file": "run-manifest", "pointer": f"/runs/{i}/started_at"}, "failure_note": note})
RUN_IDS = {r["id"] for r in runs}

values = []


def pub(vid, name, unit, pointer, locator, as_printed, file="streams"):
    values.append({"id": vid, "name": name, "unit": unit, "class": "published", "ref": {"file": file, "pointer": pointer},
                   "source": {"source_id": SRC, "locator": locator}, "as_printed": as_printed, "conversion": None,
                   "rationale": None, "method": None, "run_id": None, "unresolved_ids": []})


def sim(vid, name, unit, run, pointer):
    if run in RUN_IDS:
        values.append({"id": vid, "name": name, "unit": unit, "class": "simulated", "ref": {"file": f"result.{run}", "pointer": pointer},
                       "source": None, "as_printed": None, "conversion": None, "rationale": None, "method": None,
                       "run_id": run, "unresolved_ids": []})


def der(vid, name, unit, pointer, method, run=None):
    values.append({"id": vid, "name": name, "unit": unit, "class": "derived", "ref": {"file": "comparison", "pointer": pointer},
                   "source": None, "as_printed": None, "conversion": None, "rationale": None, "method": method,
                   "run_id": run, "unresolved_ids": []})


def ass(vid, name, unit, file, pointer, why, run=None):
    values.append({"id": vid, "name": name, "unit": unit, "class": "assumed", "ref": {"file": file, "pointer": pointer},
                   "source": None, "as_printed": None, "conversion": None, "rationale": why, "method": None,
                   "run_id": run, "unresolved_ids": []})


s = lambda sid: f"/streams/{SIDX[sid]}"  # noqa: E731
pub("paper-meoh-purity", "Methanol product 31-MEOH, methanol", "mol %", s("31-MEOH") + "/mol_pct/CH3OH", "Supplement Table S10, p.15, row 31-MEOH", "99.667")
pub("paper-meoh-flow", "Methanol product 31-MEOH, molar flow", "kmol/h", s("31-MEOH") + "/molar_kmol_h", "Supplement Table S9, p.13, row 31-MEOH", "4542")
pub("paper-water-purity", "Water product 30-WATER, water", "mol %", s("30-WATER") + "/mol_pct/H2O", "Supplement Table S10, p.15, row 30-WATER", "99.985")
pub("paper-24-co2", "FLASH3 liquid 24, CO2", "mol %", s("24") + "/mol_pct/CO2", "Supplement Table S10, p.14, row 24", "18.545")
pub("paper-16-meoh", "Reactor outlet 16, methanol", "mol %", s("16") + "/mol_pct/CH3OH", "Supplement Table S10, p.14, row 16", "7.415")
pub("paper-he7-duty", "HE7 duty (Table S14)", "MW", f"/equipment/{EIDX['HE7']}/specification/duty_MW/value", "Supplement Table S14, p.26, one-step", "24.2", file="equipment")
der("paper-he7-from-streams", "HE7 duty from the printed enthalpies of streams 22 and 23", "MW", "/paper_duties_MW/from_printed_stream_enthalpies/HE7",
    "compare.py: sum of F x H (Table S9) out minus in")
sim("chepta-he7-duty", "HE7 duty, paper stream 22 cooled to 30 C (CHEPTA)", "kW", "u-he7", "/value/blocks/HE7/duty_kW")
sim("chepta-reactor-16-meoh", "Reactor outlet methanol flow, paper stream 15 in (CHEPTA, U 300)", "kmol/h", "u-reactor-u300", "/value/streams/out-out/flow_kmol_h/methanol")
sim("chepta-flash3-24-co2", "FLASH3 liquid, CO2 flow, paper stream 23 in (CHEPTA)", "kmol/h", "u-flash3", "/value/streams/out-liquid/flow_kmol_h/carbon-dioxide")
sim("chepta-column-meoh", "Liquid distillate after the 53 C flash, methanol flow (CHEPTA, paper stream 29 in)", "kmol/h", "u-column-partial-flash53", "/value/streams/31-MEOH/flow_kmol_h/methanol")
if PLANT in RUN_IDS:
    sim("chepta-plant-meoh", "Methanol product 31-MEOH, methanol flow (CHEPTA, whole plant)", "kmol/h", PLANT, "/value/streams/31-MEOH/flow_kmol_h/methanol")
    sim("chepta-plant-meoh-total", "Methanol product 31-MEOH, total flow (CHEPTA, whole plant)", "kmol/h", PLANT, "/value/streams/31-MEOH/F_kmol_h")
    sim("chepta-plant-water", "Water product 30-WATER, water flow (CHEPTA, whole plant)", "kmol/h", PLANT, "/value/streams/30-WATER/flow_kmol_h/water")
ass("reactor-u", "Overall heat-transfer coefficient of the reactor tubes", "W/m2/K", "request.u-reactor-u300", "/input/flowsheet/blocks/1/spec/coolant/U_W_m2K",
    "Not printed (the paper computes U along the tube, supplement Section B). Runs at 150 and 1000 W/m2/K move the outlet by less than 0.5 K and 0.05 mol-% points.", "u-reactor-u300")
ass("compressor-efficiency", "Isentropic efficiency of the compressors", "-", "run-manifest", "/settings/1/1",
    "Not printed; CHEPTA's typical value 0.75 is used (no key in the spec). The compressor outlets are 7-14 K hotter than the paper's.", "u-cp1")

variants = [
    {"id": "units-paper-inlets", "description": "Every unit alone, fed with the paper's Table S9-S10 streams.", "modifications": []},
    {"id": "sections-paper-inlets", "description": "Compression, synthesis loop (with its recycle and purge), purification (with column); streams entering from outside the section are the paper's.",
     "modifications": [{"kind": "other", "description": "Column with CHEPTA's partial condenser and a flash at 53 C; H2, CO and N2 traces bypass the column."}]},
    {"id": "plant-one-flowsheet", "description": "The whole one-step plant as one CHEPTA flowsheet, with both recycles and both purges; the fired heater and steam cycle are left out.",
     "modifications": [{"kind": "other", "description": "Exchangers HE4, HE5, HE6 by their cold-side targets or approach; reactor coolant at constant 247.5 C; column by reflux and boil-up ratio."}]},
    {"id": "diagnostics", "description": "Runs that isolate a CHEPTA refusal (column start with trace gases, specification searches, column iteration limit).", "modifications": []},
]

checks = [{"id": f"compare.{r['id'].lower()}", "run_id": r["id"].lower(), "kind": "comparison_with_source", "ref": {"file": "comparison", "pointer": f"/runs/{CIDX[r['id']]}"},
           "method": "compare.py: every CHEPTA stream against Tables S9-S10 (flow, T, mol %), duties against Table S14 and the printed stream enthalpies",
           "scope": "Published simulation (Aspen Plus V10; PR in the reactors, NRTL2 elsewhere) against CHEPTA 0.6.2 with PR everywhere: two models agreeing or not, not measurements.",
           "tolerances": None, "verifier": {"file": "verifier", "earlier_version": None}}
          for r in CMP["runs"] if r.get("streams")]

record = {
    "study_record": 1,
    "id": "methanol-co2-campos-2022-one-step-chepta-0.6.2",
    "case_id": "methanol-co2-campos-2022",
    "title": "One-step CO2-to-methanol plant of Lacerda de Oliveira Campos et al. 2022 on chepta@0.6.2, stream by stream",
    "question": "Run every unit, then the sections, then the whole one-step plant with its recycles and purges as one flowsheet in the released chepta 0.6.2 through its command line; compare with the supplement's Tables S9-S10 and S14; record what CHEPTA refuses.",
    "status": "draft",
    "written_on": "2026-11-14",
    "written_by": "CHEPTA-Lab worker session (Claude); runs executed by this session on chepta@0.6.2",
    "supersedes": None,
    "sources": {"source_ids": [SRC], "evidence_ids": [],
                "note": "Paper numbers from streams.json (Tables S9-S10) and equipment.json (Figure S1, Tables S13-S14), transcribed 2026-11-13; the article (sha256 8215079335f3...) and supplement (sha256 015d60b56ef5...) were downloaded again for this study into raw_papers/ (not redistributed). Kinetics: article Eqs. 8-11 and Table 1 (rights of Table 1: see README)."},
    "files": files,
    "engines": [{"id": "chepta@0.6.2", "package": "chepta", "release": "0.6.2", "commit": None, "pin": "release",
                 "commit_observed": False, "engine_file_hashes": None,
                 "lock": {"file": "engine-lock", "pointer": "/packages/node_modules~1chepta"},
                 "request_path": "CHEPTA.run", "contracts": "v1", "result_format": 1,
                 "note": "Lab's package.json pin (chepta 0.6.2), installed with npm ci; called through its command line, chepta request --time-ms N <file>."}],
    "variants": variants,
    "runs": runs,
    "values": values,
    "constraint_declaration": {"timing": "reconstructed_after_runs", "declared_on": "2026-11-14",
                               "basis": "No constraint is declared: the column ends are compared in comparison.json, not tested against a limit."},
    "constraints": [],
    "product_constraints_note": "The paper states the methanol product purity 99.67 mol % (supplement p.10) as a result, not a limit; compared in comparison.json.",
    "constraint_results": [],
    "checks": checks,
    "warning_notes": [{"id": "pr-kij-extrapolations", "run_ids": [PLANT, "u-flash3"],
                       "pointers": ["/value/extrapolations"],
                       "note": "CHEPTA reports k_ij sets used outside their data range in every run (H2 + CO up to 433 K above, H2 + N2, CO + N2, CO2 + N2, CO2 + methanol, CO2 + water, CO + methanol) and CO's ideal-gas heat capacity 21 K above its range in the reactors. Each run's list, with the blocks it applies to, is in comparison.json and COMPARISON.md. The warnings are kept, not removed."}],
    "assumptions": [
        {"id": "pr-everywhere", "statement": "Peng-Robinson with CHEPTA's k_ij is the method of every unit.", "applies_to": ["units-paper-inlets", "sections-paper-inlets", "plant-one-flowsheet"],
         "basis": "The paper uses NRTL2 outside the reactors (article p.9); CHEPTA has no NRTL pairs for the gases with methanol and water, and PR + MHV1 lacks methanol + N2 (runs u-flash3-mhv1, u-column-*-mhv1)."},
        {"id": "column-condenser", "statement": "The paper's partial vapour-liquid condenser at 53 C is CHEPTA's partial condenser (all distillate as vapour, reflux ratio 2) followed by a flash at 53 C.",
         "applies_to": ["sections-paper-inlets", "plant-one-flowsheet"], "basis": "CHEPTA's column has one distillate, vapour or liquid; the product split of the flash is the paper's condenser equilibrium, the reflux composition is not."},
        {"id": "trace-bypass", "statement": "H2, CO and N2 in the column feed (8 to 20 ppm each) bypass the column to the 53 C flash.",
         "applies_to": ["sections-paper-inlets", "plant-one-flowsheet"], "basis": "CHEPTA's column cannot start with them (runs diag-feed29-*, diag-column-*); the paper sends 98.6-99.9 % of each to stream 32 (supplement Table S2)."},
        {"id": "no-steam-cycle", "statement": "Fired heater, steam cycle and the water sides of HE3 and the reactors are left out; the reactor coolant is at a constant 247.5 C.",
         "applies_to": ["plant-one-flowsheet"], "basis": "equipment.json: may be left out of the first case."},
    ],
    "unresolved_inputs": [
        {"id": "reactor-u", "item": "Overall U of the reactor tubes.", "consequence": "Assumed 300 W/m2/K; insensitive in runs at 150 and 1000.", "blocking": False, "next_action": "None needed for this case."},
        {"id": "compressor-efficiency", "item": "Isentropic efficiencies of the five compressors.", "consequence": "Outlet temperatures 7-14 K above the paper's with 0.75.", "blocking": False, "next_action": "Could be back-calculated from Table S9 temperatures; not done."},
        {"id": "he7-duty", "item": "HE7: Table S14 24.2 MW against 19.75 MW from the printed enthalpies of streams 22 and 23.", "consequence": "CHEPTA gives 25.1 MW for 22 -> 30 C (run u-he7): it supports Table S14.", "blocking": False, "next_action": "Spot check by the maintainer."},
        {"id": "kinetics-rights", "item": "Table 1 of the article (Model-6p constants) is reprinted with permission from an ACS paper.", "consequence": "The constants are in model.py and the request files.", "blocking": False, "next_action": "Maintainer's decision (README)."},
    ],
    "cost_coverage": {"status": "not_costed", "scope": None, "missing_items": [], "result_files": []},
    "corpus_links": {"task_ids": [], "run_ids": []},
    "reviews": [],
    "limitations": [
        "Agreement with the paper is agreement between two simulators (Aspen Plus V10 with NRTL2 and PR; CHEPTA 0.6.2 with PR), not with measurements.",
        "Fired heater and steam cycle not modelled.",
        "No separate AI review session yet and no person's spot check of this study; draft only.",
    ],
}
(H / "study-record.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
print("study-record.json:", len(files), "files,", len(runs), "runs,", len(values), "values")
