#!/usr/bin/env python3
"""Write study-record.json for the S2 runs on chepta 0.6.1, binding every file by sha256.

Reads the run manifest and comparison-s2.json written by run_s2_chepta_0.6.1.py and compare_s2.py. Run after them:
  python3 cases/ethyl-acetate-piotrowski-2021/build_study_record.py
Then python scripts/dataset_pipeline.py validate. No CHEPTA call; no number typed here except pointers.
"""
import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
ROOT = H.parents[1]
REL = H.relative_to(ROOT).as_posix()
R = H / "results-chepta-0.6.1"
MAN = json.loads((R / "run-manifest.json").read_text())
CMP = json.loads((R / "comparison-s2.json").read_text())
SRC = "piotrowski-kubica-2021"
S2 = json.loads((H / "streams.json").read_text())["strategies"]["S2"]
SIDX = {int(r["stream"]): i for i, r in enumerate(S2)}
EQ = json.loads((H / "equipment.json").read_text())["equipment"]
EIDX = {e["id"]: i for i, e in enumerate(EQ)}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


files = []


def add_file(fid, path, role):
    files.append({"id": fid, "path": f"{REL}/{path}", "sha256": sha(H / path), "role": role})


add_file("streams", "streams.json", "case_input")
add_file("equipment", "equipment.json", "case_input")
add_file("model", "s2_model.py", "case_input")
add_file("runner", "run_s2_chepta_0.6.1.py", "runner")
add_file("verifier", "compare_s2.py", "verifier")
add_file("run-manifest", "results-chepta-0.6.1/run-manifest.json", "execution_manifest")
add_file("comparison", "results-chepta-0.6.1/comparison-s2.json", "lab_check")
add_file("engine-lock", "chepta-0.6.1.npm-lock.json", "engine_lock")
add_file("case-readme", "README.md", "other")


def variant_of(rid):
    if rid.startswith("info-"):
        return "component-data"
    if rid in ("u-htxr2-15C", "u-htxr6-70C", "u-extr8-1stage-70C", "u3-extr8-1stage-70C", "secA-feeds-17C", "secB-mix7-adiabatic") or "-acid" in rid:
        return "as-printed-or-with-acid"
    if rid.startswith("u"):
        return "units-paper-inlets"
    if rid.startswith("secA"):
        return "section-a-paper-inlets"
    if rid.startswith("secB"):
        return "section-b-paper-inlets"
    return "plant-coupled"


runs = []
LID = lambda rid: rid.lower()  # noqa: E731  (study-record ids are lower case; execution_id keeps the runner's id)
for i, r in enumerate(MAN["runs"]):
    rid = LID(r["id"])
    add_file(f"request.{rid}", r["request_file"], "request")
    out = H / r["output_file"]
    has_result = out.read_bytes().strip() != b""
    if has_result:
        add_file(f"result.{rid}", r["output_file"], "result")
    add_file(f"stderr.{rid}", r["stderr_file"], "other")
    note = None
    if r["outcome"] != "ok":
        e = r["error"] or {}
        note = (f"{r['exit_meaning']} (exit {r['exit_code']}): {e.get('code')}: {e.get('message')}" if e else
                f"{r['exit_meaning']} (exit {r['exit_code']}); no result written; see the stderr file")
    runs.append({"id": rid, "execution_id": r["id"] if r["id"] != rid else None, "variant": variant_of(r["id"]), "engine": "chepta@0.6.1",
                 "interface": "command_line", "runner": "runner", "request": f"request.{rid}",
                 "result": f"result.{rid}" if has_result else None,
                 "execution_record": {"file": "run-manifest", "pointer": f"/runs/{i}"},
                 "executed_at": {"file": "run-manifest", "pointer": f"/runs/{i}/started_at"}, "failure_note": note})

coup = MAN.get("plant_coupling") or {}
FA, FB = (CMP["runs"]["plant-final"]["made_of"][k].lower() for k in "AB")  # once-through, round 1
values = []


def pub(vid, name, unit, file, pointer, locator, as_printed=None):
    values.append({"id": vid, "name": name, "unit": unit, "class": "published", "ref": {"file": file, "pointer": pointer},
                   "source": {"source_id": SRC, "locator": locator}, "as_printed": as_printed, "conversion": None,
                   "rationale": None, "method": None, "run_id": None, "unresolved_ids": []})


def sim(vid, name, unit, run, pointer):
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


st = lambda n: f"/strategies/S2/{SIDX[n]}"  # noqa: E731
pub("paper-product-kg-h", "Product stream 16, mass flow (paper, S2)", "kg/h", "streams", st(16) + "/mass_kg_h", "Table A2, p.14, stream 16", "12,434")
pub("paper-product-ea", "Product stream 16, ethyl acetate (paper, S2)", "mass %", "streams", st(16) + "/ethyl_acetate_mass_pct", "Table A2, p.14, stream 16")
pub("paper-product-water", "Product stream 16, water (paper, S2)", "mass %", "streams", st(16) + "/water_mass_pct", "Table A2, p.14, stream 16")
pub("paper-azeotrope-kg-h", "Azeotrope stream 9, mass flow (paper, S2)", "kg/h", "streams", st(9) + "/mass_kg_h", "Table A2, p.13, stream 9", "98,380")
pub("paper-raffinate-kg-h", "Raffinate stream 11, mass flow (paper, S2)", "kg/h", "streams", st(11) + "/mass_kg_h", "Table A2, p.14, stream 11", "87,314")
pub("paper-wastewater-kg-h", "Wastewater stream 25, mass flow (paper, S2)", "kg/h", "streams", st(25) + "/mass_kg_h", "Table A2, p.14, stream 25", "20,000")
pub("paper-krea4-duty", "Reactor-evaporator KREA 4 heat duty (paper, S2)", "kW", "equipment", f"/equipment/{EIDX[4]}/S2/duty_kW", "Table 1, p.11", "13,586.2")
pub("paper-htxr6-duty", "Condenser HTXR 6 duty (paper, S2)", "kW", "equipment", f"/equipment/{EIDX[6]}/S2/duty_kW", "Table 1, p.11", "−14,855.8")
pub("paper-scds11-reboiler", "Product column SCDS 11 reboiler duty (paper, S2)", "kW", "equipment", f"/equipment/{EIDX[11]}/S2/condenser_reboiler_duty_kW/1", "Table 1, p.11", "9219.2")
pub("paper-scds15-reboiler", "Wastewater column SCDS 15 reboiler duty (paper, S2)", "kW", "equipment", f"/equipment/{EIDX[15]}/S2/condenser_reboiler_duty_kW/1", "Table 1, p.11", "16,136.6")
pub("paper-htxr10-duty", "Heater HTXR 10 duty (paper, S2)", "kW", "equipment", f"/equipment/{EIDX[10]}/S2/duty_kW", "Table 1, p.11", "713.5")
pub("paper-htxr18-duty", "Heater HTXR 18 duty (paper, S2)", "kW", "equipment", f"/equipment/{EIDX[18]}/S2/duty_kW", "Table 1, p.11", "4332.9")
der("acid-triple-point-k", "Lowest temperature of CHEPTA's acetic acid liquid heat-capacity record (its triple point)", "K",
    "/acid_record_Tmin_K", "CHEPTA run info-acetic-acid, properties[liquidHeatCapacity].Tmin_K, copied by compare_s2.py", "info-acetic-acid")
if FA and FB:
    sim("chepta-product-kmol-h", "Product stream 16, molar flow (CHEPTA, plant once through)", "kmol/h", FB, "/value/streams/S16/F_kmol_h")
    sim("chepta-azeotrope-kg-h", "Azeotrope stream 9, mass flow (CHEPTA, plant once through)", "kg/h", FA, "/value/streams/S9/mass_kg_h")
    sim("chepta-raffinate-kg-h", "Raffinate stream 11, mass flow (CHEPTA, plant once through)", "kg/h", FB, "/value/streams/S11/mass_kg_h")
    sim("chepta-wastewater-kg-h", "Wastewater stream 25, mass flow (CHEPTA, plant once through)", "kg/h", FB, "/value/streams/S25/mass_kg_h")
    sim("chepta-krea4-duty", "Reactor KREA 4 duty (CHEPTA, plant once through; conversion imposed from the paper)", "kW", FA, "/value/blocks/KREA4/duty_kW")
    sim("chepta-htxr6-duty", "Condenser HTXR 6 duty (CHEPTA, plant once through)", "kW", FA, "/value/blocks/HTXR6/duty_kW")
    sim("chepta-scds11-reboiler", "Product column reboiler duty (CHEPTA, plant once through)", "kW", FB, "/value/blocks/SCDS11/state/reboiler_kW")
    sim("chepta-scds15-reboiler", "Wastewater column reboiler duty (CHEPTA, plant once through)", "kW", FB, "/value/blocks/SCDS15/state/reboiler_kW")
    der("chepta-product-ea", "Product stream 16, ethyl acetate (CHEPTA, plant once through)", "mass %", "/product_checks_plant_final/EA_mass_pct",
        "compare_s2.py: CHEPTA's component flows x CHEPTA's molar masses (runs info-*)", FB)
    der("chepta-product-water", "Product stream 16, water (CHEPTA, plant once through)", "mass %", "/product_checks_plant_final/water_mass_pct",
        "compare_s2.py: CHEPTA's component flows x CHEPTA's molar masses (runs info-*)", FB)
    ass("plant-extractor-stages", "Equilibrium stages of EXTR 8 in the coupled plant", "-", f"request.{FB}",
        "/input/flowsheet/blocks/3/spec/stages",
        "The paper gives no stage count. Chosen from the unit runs u3-extr8-1..8stage as the count whose raffinate ethanol is closest to the paper's stream 11 (2 stages: 1.87 vs 1.86 mass %); stream 11's ethanol is therefore calibrated, not an independent comparison.", FB)
    ass("feed-temperature", "Ethanol and acetic acid feed temperature", "K", f"request.{FA}", "/input/flowsheet/blocks/1/spec/T_K",
        "The paper's 15 C is below acetic acid's triple point in CHEPTA's record (refused, OUT_OF_RANGE); 18 C keeps the mixed feed above it.", FA)

variants = [
    {"id": "component-data", "description": "CHEPTA's component records of the four components (molar masses, property ranges).", "modifications": []},
    {"id": "as-printed-or-with-acid", "description": "The paper's values as printed (15 C acid feed, 70 C condensate and extractor, adiabatic MIX 7) or downstream units with acetic acid as a component: kept to record CHEPTA's refusals.", "modifications": []},
    {"id": "units-paper-inlets", "description": "Every unit alone, its inlets the paper's Table A2 streams; downstream of column 5 (u3-*) without acetic acid.",
     "modifications": [{"kind": "other", "description": "Acetic acid (0.00-0.01 mass % in the paper) dropped from the inlets of the u3-* runs."}]},
    {"id": "section-a-paper-inlets", "description": "Section A (feeds, HTXR 2, MIX 3, KREA 4, SCDS 5, HTXR 6, recycle 7), streams 21 and 27 from Table A2.",
     "modifications": [{"kind": "other", "description": "Reactor conversion imposed from the paper's streams 5 and 6; feeds at 18 C."}]},
    {"id": "section-b-paper-inlets", "description": "Section B (MIX 7, EXTR 8, splitters 9 and 16, columns 11 and 15, water loop, heaters), stream 9 from Table A2 without acetic acid; 1 to 8 extractor stages.",
     "modifications": [{"kind": "other", "description": "Three components; extractor isothermal at 27 C; MIX 7 outlet saturated liquid."}]},
    {"id": "plant-coupled", "description": "The whole plant: sections A and B coupled across streams 9, 21 and 27 by Lab's runner (successive substitution).",
     "modifications": [{"kind": "other", "description": "The coupling across the cut is Lab's script, not a CHEPTA flowsheet; acetic acid leaving section A in stream 9 is dropped and reported."}]},
]

constraints = [
    {"id": "scds11-reflux", "kind": "operating", "quantity": "Product column SCDS 11 reflux ratio R/D", "unit": "-",
     "observe": {"in": "result", "pointer": "/value/blocks/SCDS11/state/reflux_ratio"}, "operator": "equal", "target": 3,
     "lower": None, "upper": None, "tolerance": {"value": 1e-6, "class": "assumed", "rationale": "A specification: a converged column holds it to round-off."},
     "origin": {"class": "published", "source_id": SRC, "locator": "Table 1, p.11", "rationale": None}},
    {"id": "scds15-reflux", "kind": "operating", "quantity": "Wastewater column SCDS 15 reflux ratio R/D", "unit": "-",
     "observe": {"in": "result", "pointer": "/value/blocks/SCDS15/state/reflux_ratio"}, "operator": "equal", "target": 2,
     "lower": None, "upper": None, "tolerance": {"value": 1e-6, "class": "assumed", "rationale": "A specification: a converged column holds it to round-off."},
     "origin": {"class": "published", "source_id": SRC, "locator": "Table 1, p.11", "rationale": None}},
]
constraint_results = []
if FB:
    for c in constraints:
        res = json.loads((H / f"results-chepta-0.6.1/{CMP['runs']['plant-final']['made_of']['B']}.output.json").read_text())
        obs = res["value"]["blocks"][c["observe"]["pointer"].split("/")[3]]["state"]["reflux_ratio"]
        ok = abs(obs - c["target"]) <= c["tolerance"]["value"]
        constraint_results.append({"constraint_id": c["id"], "run_id": FB, "verdict": "met" if ok else "not_met", "note": None})

checks = []
for rid in CMP["runs"]:
    if rid == "plant-final":
        continue
    checks.append({"id": f"compare.{LID(rid)}", "run_id": LID(rid), "kind": "comparison_with_source",
                   "ref": {"file": "comparison", "pointer": f"/runs/{rid}"},
                   "method": "compare_s2.py: every CHEPTA stream against Table A2 (T, mass flow, mass %), duties against Table 1",
                   "scope": "Published simulation (Chemcad 7, UNIQUAC) against CHEPTA 0.6.1: agreement between two models, not with measurements.",
                   "tolerances": None, "verifier": {"file": "verifier", "earlier_version": None}})
if FB:
    checks.append({"id": "compare.plant-final", "run_id": FB, "kind": "comparison_with_source",
                   "ref": {"file": "comparison", "pointer": "/runs/plant-final"},
                   "method": "compare_s2.py: streams 1-8 from the final section A run, 9-28 from the final section B run, against Table A2; duties against Table 1",
                   "scope": "The coupled plant (Lab's coupling across the cut at stream 9).", "tolerances": None,
                   "verifier": {"file": "verifier", "earlier_version": None}})

warn_runs = [r["id"] for r in runs if r["result"] and r["id"] in ("u-krea4-conversion", "u-scds5")]
record = {
    "study_record": 1,
    "id": "ethyl-acetate-piotrowski-2021-s2-chepta-0.6.1",
    "case_id": "ethyl-acetate-piotrowski-2021",
    "title": "Classic ethyl acetate plant S2 of Piotrowski & Kubica 2021 on chepta@0.6.1, stream by stream",
    "question": "Build every unit and stream of the paper's classic plant S2 in the released chepta 0.6.1 through its command line, compare CHEPTA's streams and duties with the paper's Appendix Table A2 and Table 1, and record what CHEPTA refuses.",
    "status": "draft",
    "written_on": "2026-11-12",
    "written_by": "CHEPTA-Lab worker session (Claude); runs executed by this session on chepta@0.6.1",
    "supersedes": None,
    "sources": {"source_ids": [SRC], "evidence_ids": [],
                "note": "Every paper number comes from streams.json (Table A2) and equipment.json (Table 1, Figure 1), transcribed 2026-10-29 and audited (STREAM_EQUIPMENT_AUDIT.md); the PDF (sha256 0057df76..., the same as recorded in streams.json) was re-read for this study and is not redistributed."},
    "files": files,
    "engines": [{"id": "chepta@0.6.1", "package": "chepta", "release": "0.6.1", "commit": None, "pin": "release",
                 "commit_observed": False, "engine_file_hashes": None,
                 "lock": {"file": "engine-lock", "pointer": "/packages/node_modules~1chepta"},
                 "request_path": "CHEPTA.run", "contracts": "v1", "result_format": 1,
                 "note": "Released npm package installed with npm in a separate folder (its lock file copied as chepta-0.6.1.npm-lock.json); Lab's package.json pin was not changed by this study. Called through its command line, chepta request <file>."}],
    "variants": variants,
    "runs": runs,
    "values": values,
    "constraint_declaration": {"timing": "reconstructed_after_runs", "declared_on": "2026-11-12",
                               "basis": "The constraints restate the paper's column specifications (Table 1). Product limits are compared in comparison-s2.json, not declared here."},
    "constraints": constraints,
    "product_constraints_note": "The product limits of the paper (at least 99.9 mass % ethyl acetate, below 0.03 mass % water and 0.04 mass % ethanol, Section 3.4 p.8) are on a mass basis, which CHEPTA's result does not print; compare_s2.py converts CHEPTA's component flows with CHEPTA's molar masses and records the verdicts in comparison-s2.json (product_checks_plant_final).",
    "constraint_results": constraint_results,
    "checks": checks,
    "warning_notes": [{"id": "uniquac-range", "run_ids": warn_runs or [runs[0]["id"]],
                       "pointers": ["/value/streams"],
                       "note": "CHEPTA warns that its UNIQUAC water + ethyl acetate set comes from data at 273.35-343.55 K and is used above it (the reactor vapour, column 5's lower stages, the bottoms of column 15). Results there rest on extrapolated parameters."}],
    "assumptions": [
        {"id": "conversion-imposed", "statement": "The reactor's acetic acid conversion per pass (0.7703) is imposed from the paper's streams 5 and 6; the reactor outlet composition is therefore not a prediction.",
         "applies_to": ["section-a-paper-inlets", "plant-coupled", "units-paper-inlets"], "basis": "Paper Eqs. 1-3 lack the catalyst concentration and units; CHEPTA has no reactor-evaporator."},
        {"id": "cut-at-stream-9", "statement": "Section B is run without acetic acid; the two sections are coupled by Lab's script.",
         "applies_to": ["section-b-paper-inlets", "plant-coupled"], "basis": "CHEPTA 0.6.1 refuses two liquids with acetic acid present (runs *-acid)."},
        {"id": "extractor-isothermal", "statement": "EXTR 8 is isothermal at 27 C with 2 equilibrium stages (stage count chosen to match the paper's stream 11 ethanol).",
         "applies_to": ["plant-coupled"], "basis": "Table 1's 70 C is refused (the feed boils); the paper's outlets at 27 and 41 C imply an adiabatic extractor, which CHEPTA does not have."},
    ],
    "unresolved_inputs": [
        {"id": "kinetics", "item": "Catalyst concentration and concentration units of the paper's rate law (Eqs. 1-3, after Atalay).", "consequence": "The reactor cannot be predicted; its conversion is taken from the paper.", "blocking": False, "next_action": "Read Atalay (ref. 36) for the catalyst basis; needs a reactor-evaporator in CHEPTA as well."},
        {"id": "extractor-design", "item": "Number of stages, contactor type and energy balance of EXTR 8.", "consequence": "The stage count is calibrated; the extract leaves at 27 C instead of 41 C, so HTXR 19 duty is not comparable.", "blocking": False, "next_action": "None in the paper; an adiabatic extraction block in CHEPTA would remove one assumption."},
        {"id": "paper-heater-duties", "item": "Table 1's duties of HTXR 18 and HTXR 19 look exchanged: HTXR 18 (stream 26, 60,000 kg/h, 27 to 70 C) prints 4332.9 kW and HTXR 19 (stream 20, 139,203 kg/h, 41 to 70 C) 1541.1 kW, while CHEPTA gives 1580 and 5681 kW for them (unit runs); S1 shows the same pattern. HTXR 10 heats stream 11's composition with 26 W per kg/h, HTXR 18 with 72 W per kg/h as printed.", "consequence": "HTXR 18 and 19 are not compared as printed; the totals of Table 2 are unaffected by a label swap.", "blocking": False, "next_action": "Confirmed by the maintainer's spot check (2026-11-12): the two duties are exchanged in Table 1. Ask the authors."},
    ],
    "cost_coverage": {"status": "not_costed", "scope": None, "missing_items": [], "result_files": []},
    "corpus_links": {"task_ids": [], "run_ids": []},
    "reviews": [],
    "limitations": [
        "Agreement with the paper is agreement between two simulators (Chemcad 7 and CHEPTA 0.6.1, both UNIQUAC with different parameters), not with measurements.",
        "The reactor's conversion is imposed from the paper; reactor outlet composition is not predicted.",
        "The whole plant is not one CHEPTA flowsheet: acetic acid forces a cut at stream 9, closed by Lab's script.",
        "The extractor is isothermal at 27 C with a calibrated stage count; the paper's extractor is adiabatic at an unknown stage count.",
        "No separate AI review session yet; draft only. The maintainer spot-checked and confirmed 3 items chosen by the building session (2026-11-12: HTXR 18/19 duties exchanged in Table 1, reactor conversion 0.7703, column 11 settings); this is not recorded as a review.",
    ],
}
(H / "study-record.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
print("study-record.json:", len(files), "files,", len(runs), "runs,", len(values), "values")
