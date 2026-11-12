#!/usr/bin/env python3
"""Lab's checks of the B2 runs on chepta@0.6.1. Reads files only; never runs CHEPTA. results-chepta-0.6.1/checks.json.

For every converged run: published-profile agreement with the SAME limits as for 0.6.0 (1 K, 0.02 mole fraction, from
CHEPTA's record; nothing loosened), Lab's own balances, and whether the specification asked for was reached.
Runs with the 0.6.0 specifications (reflux ratio 2, bottoms flow) also: same-equation agreement with CHEPTA's stored
reference solution, and a comparison with the 0.6.0 output (every leaf value, except run id and library/databank labels).
Not a validation against measurements: the published numbers come from another property method.
"""
import importlib.util
import json
from pathlib import Path

H = Path(__file__).resolve().parent
OUT = H / "results-chepta-0.6.1"
K = 3.6
KELVIN = 273.15
spec = importlib.util.spec_from_file_location("check_b2", H / "check_b2.py")
b2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2)


def load(name):
    return json.loads((H / name).read_text())


def deep(a, b, path=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append((f"{path}/{k}", "<absent>", b[k]))
            elif k not in b:
                out.append((f"{path}/{k}", a[k], "<absent>"))
            else:
                out += deep(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            out += deep(x, y, f"{path}[{i}]")
    elif a != b:
        out.append((path, a, b))
    return out


def main():
    rec = load("upstream/B2-chemsep-benzene-toluene.json")
    ref = load("upstream/reference_mesh-B2.json")["case"]["rigorous"]
    comps, pub = rec["components"], rec["published"]
    num = rec["tolerances"]["numerical"]["engine_against_reference"]
    agree = rec["tolerances"]["agreement_with_published_example"]
    manifest = load("results-chepta-0.6.1/run-manifest.json")
    results = []
    for run in manifest["runs"]:
        rid = run["id"]
        o = load(f"results-chepta-0.6.1/{rid}.output.json")
        entry = {"id": rid, "outcome": o["outcome"], "exit_code": run["exit_code"],
                 "request_identical_to_0.6.0": run["request_identical_to_0.6.0"]}
        if o["outcome"] != "ok":
            entry["error"] = o.get("error")
            results.append(entry)
            continue
        col, prof = o["value"]["column"], o["value"]["column"]["profile"]
        D, B = o["value"]["distillate"], o["value"]["bottoms"]
        # published profile, same limits as 0.6.0
        pT = b2.worst([(f"stage {s['stage']}", s["T_K"], tc + KELVIN) for s, tc in zip(prof, pub["T_C"])])
        px = b2.worst([(f"stage {s['stage']}", s["x"][comps[0]], xb) for s, xb in zip(prof, pub["x_benzene"])]
                      + [("distillate x_D", D["z"][0], pub["x_D"][0]), ("bottoms x_B", B["z"][0], pub["x_B"][0])])
        pT["tolerance"], px["tolerance"] = agree["T_K_absolute"], agree["mole_fractions_absolute"]
        pT["passed"], px["passed"] = pT["max_abs_difference"] <= pT["tolerance"], px["max_abs_difference"] <= px["tolerance"]
        entry["published"] = {"T_K": pT, "x_benzene": px, "limits_from": "CHEPTA's record, unchanged from the 0.6.0 check",
                              "not_compared_shown_only": {
                                  "D_mol_s": {"observed": col["D_kmol_h"] / K, "published": pub["D_mol_s"]},
                                  "B_mol_s": {"observed": col["B_kmol_h"] / K, "published": pub["B_mol_s"]},
                                  "reflux_ratio": {"observed": col["reflux_ratio"], "published": pub["reflux_ratio"]},
                                  "boilup_ratio": {"observed": col["boilup_ratio"], "published": pub["boilup_ratio"]}}}
        # balances
        feed = o["value"]["feed"]["flow_kmol_h"]
        overall = {c: feed[c] - D["flow_kmol_h"][c] - B["flow_kmol_h"][c] for c in comps}
        n, fs = len(prof), {f["stage"] if isinstance(f, dict) else f for f in col["feed_stages"]}
        stage = []
        for j, s in enumerate(prof):
            for c in comps:
                inn = (prof[j - 1]["L_kmol_h"] * prof[j - 1]["x"][c] if j > 0 else 0) \
                    + (prof[j + 1]["V_kmol_h"] * prof[j + 1]["y"][c] if j < n - 1 else 0) + (feed[c] if s["stage"] in fs else 0)
                leave = s["L_kmol_h"] * s["x"][c] + (s["V_kmol_h"] * s["y"][c] if s["y"] else 0) \
                    + (D["flow_kmol_h"][c] if j == 0 else 0)
                stage.append(inn - leave)
        energy = o["value"]["feed"]["H_kW"] + col["reboiler_kW"] - col["condenser_kW"] - D["H_kW"] - B["H_kW"]
        F = sum(feed.values())
        tol_mat, tol_en = 1e-8 * F, 1e-8 * F / K * 10.0
        bal = {"overall_max_abs_kmol_h": max(abs(v) for v in overall.values()),
               "stage_component_max_abs_kmol_h": max(abs(v) for v in stage), "energy_kW": energy,
               "tolerances": {"material_kmol_h": tol_mat, "energy_kW": tol_en},
               "chepta_reported": {"material_kmol_h": o["checks"]["material_kmol_h"], "energy_kW": o["checks"]["energy_kW"]}}
        bal["passed"] = bal["overall_max_abs_kmol_h"] <= tol_mat and bal["stage_component_max_abs_kmol_h"] <= tol_mat and abs(energy) <= tol_en
        entry["balances"] = bal
        entry["warnings"] = {"column": col["warnings"], "qualifications": o["qualifications"]["warnings"]}
        # the specification asked for, as reached (observed from the profile products)
        req = load(f"results-chepta-0.6.1/{rid}.request.json")["input"]["column"]
        asked = req.get("specifications") or ([{"kind": "distillate_purity", **req["distillate_purity"]}] if "distillate_purity" in req else [])
        reached = []
        for s in asked:
            kind, val = s["kind"], s["value"]
            if kind in ("distillate_purity", "purity") and s.get("product", "distillate") == "distillate":
                obs = D["z"][comps.index(s["component"])]
            elif kind == "purity":
                obs = B["z"][comps.index(s["component"])]
            else:  # recovery of the component in the distillate
                obs = D["flow_kmol_h"][s["component"]] / feed[s["component"]]
            reached.append({"spec": s, "asked": val, "observed": obs, "difference": obs - val})
        entry["specification_reached"] = reached
        entry["chepta_design_residual"] = o["checks"]["columns"]["C1"]["residuals"].get("design_specifications")
        if rid in ("b2-pr", "b2-record-thermo-literal"):
            T = b2.worst([(f"stage {s['stage']}", s["T_K"], q["T_K"]) for s, q in zip(prof, ref["stages"])])
            x = b2.worst([(f"stage {s['stage']} {c}", s["x"][c], q["x"][i]) for s, q in zip(prof, ref["stages"]) for i, c in enumerate(comps)])
            entry["same_equation"] = {"T_K": {**T, "tolerance": num["T_K_absolute"], "passed": T["max_abs_difference"] <= num["T_K_absolute"]},
                                      "x": {**x, "tolerance": num["mole_fractions_absolute"], "passed": x["max_abs_difference"] <= num["mole_fractions_absolute"]}}
        if rid == "b2-pr":
            old = load("results-chepta-0.6.0/b2-pr.output.json")
            diffs = [d for d in deep(old, o) if not d[0].startswith(("/run/", "/reproduction/"))]
            entry["against_0.6.0"] = {"other_differing_values": len(diffs), "differences": [list(map(str, d)) for d in diffs[:20]],
                                      "library_old_new": [old["reproduction"]["library"], o["reproduction"]["library"]]}
        results.append(entry)
    (OUT / "checks.json").write_text(json.dumps({"checked_by": "check_b2_0.6.1.py (Lab); reads files only", "checks": results}, indent=2) + "\n")
    for e in results:
        if e["outcome"] != "ok":
            print(e["id"], e["outcome"], e["error"]["code"]); continue
        p = e["published"]
        print(e["id"], "T %.3f/%s x %.4f/%s" % (p["T_K"]["max_abs_difference"], p["T_K"]["passed"], p["x_benzene"]["max_abs_difference"], p["x_benzene"]["passed"]),
              "bal", e["balances"]["passed"], [round(r["difference"], 9) for r in e["specification_reached"]],
              e.get("against_0.6.0", {}).get("other_differing_values"))


if __name__ == "__main__":
    main()
