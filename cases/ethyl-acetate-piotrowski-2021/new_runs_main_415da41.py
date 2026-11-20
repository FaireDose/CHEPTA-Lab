#!/usr/bin/env python3
"""New request files for CHEPTA main 415da41 (unreleased; to become 0.6.3): what its new options allow.

Each new request is a 0.6.2 request of results-chepta-0.6.2/ (named as `base`) with the changes listed in `change`,
written to requests-main-415da41-new/<id>.request.json with a sidecar <id>.why.json (base, change, reason). They are
sent by scripts/rerun_chepta_requests.py --extra-dir requests-main-415da41-new and kept in results-chepta-main-415da41/
with the reruns. No CHEPTA call here; no result is edited.

  python3 cases/ethyl-acetate-piotrowski-2021/new_runs_main_415da41.py
"""
import copy
import json
from pathlib import Path

H = Path(__file__).resolve().parent
SRC = H / "results-chepta-0.6.2"
OUT = H / "requests-main-415da41-new"


def base(name):
    return json.loads((SRC / f"{name}.request.json").read_text())


def block(req, bid):
    return next(b for b in req["input"]["flowsheet"]["blocks"] if b["id"] == bid)


def design_spec(req, target, tol, lo=6490.0, hi=6515.0, guess=6511.0, solves=20):
    f = req["input"]["flowsheet"]
    f["designSpecs"] = [{"id": "DS_ETHANOL", "label": "ethanol feed F1 varied to hold product S16's quality",
                         "vary": {"block": "F1", "key": "flow_kg_h", "component": "ethanol", "min": lo, "max": hi, "guess": guess},
                         "target": target, "tolerance": tol}]
    f["solver"]["designSpecIterations"] = {"bracket": 8, "solve": solves}
    return req


RUNS = {}


def add(rid, base_name, change, reason, fn):
    r = fn(copy.deepcopy(base(base_name)))
    RUNS[rid] = (r, {"base": base_name, "change": change, "reason": reason})


# --- 3a. Column 11 alone at settings that should reach 99.9 % ester (the paper's feed 13 with its 0.01 % acid) ---
for B in (140.5, 140.0):
    add(f"new-iso-scds11-acid0.01-bottoms{B}", "iso-scds11-acid0.01-bottoms141.5", f"SCDS11 bottoms_kmol_h 141.5 -> {B}",
        "0.6.2 without acid: 99.9 % ester at about 140.5 kmol/h of product (iso-scds11-acid0-*); with acid it did not converge at 140-141.5",
        lambda r, B=B: (block(r, "SCDS11")["spec"].update({"bottoms_kmol_h": B}), r)[1])

# --- 3c. feed_second_liquid. No column feed of the plant holds a second liquid at its own T and P (no
# state.feed_second_liquid, no FEED_TWO_LIQUIDS in any rerun). The raffinate 11 does at 27 C with the flowsheet's sets
# (CHEPTA's METHOD_SPLIT warning on EXTR8), so column 11 is fed once with it unheated: a SENSITIVITY test of the option,
# not the paper's case (the paper heats it to 71 C, HTXR 10). And once at 71 C with "top", where nothing should bypass.
def _f13(r, T_K=None, mode=None):
    c = block(r, "SCDS11")["spec"]
    c["bottoms_kmol_h"] = 140.5
    if mode:
        c["feed_second_liquid"] = mode
    if T_K:
        block(r, "F13")["spec"]["T_K"] = T_K
    return r


for mode in ("stages", "top", "bottom"):
    add(f"new-iso-scds11-acid0.01-bottoms140.5-feed27C-{mode}", "iso-scds11-acid0.01-bottoms141.5",
        f"SCDS11 bottoms 140.5 kmol/h; feed 13 at 300.15 K (27 C, the raffinate unheated) instead of 344.15 K; feed_second_liquid {mode!r}",
        "sensitivity: a column feed with two liquids, to try feed_second_liquid; not the paper's case",
        lambda r, mode=mode: _f13(r, 300.15, mode))
add("new-iso-scds11-acid0.01-bottoms140.5-top", "iso-scds11-acid0.01-bottoms141.5",
    "SCDS11 bottoms 140.5 kmol/h; feed_second_liquid 'top' (feed 13 at the paper's 71 C)",
    "the option where the feed holds one liquid: nothing should bypass the stages", lambda r: _f13(r, None, "top"))

# --- 3b. The closed plant with a design specification on the ethanol feed (request 15) ---
ESTER, ETOH = "ethyl-acetate", "ethanol"
add("new-plant-ds-ester0.999", "plant62-best-init1e-4-tol1e-5",
    "designSpecs: F1 ethanol flow_kg_h in [6490, 6515] (guess 6511) to hold S16 ethyl acetate mass fraction 0.999 (tolerance 1e-5); "
    "solver.designSpecIterations {bracket 8, solve 20}",
    "request 15: the paper's product purity (Section 3.4) held by the ethanol make-up inside the settled closed plant",
    lambda r: design_spec(r, {"stream": "S16", "quantity": "mass_fraction", "component": ESTER, "value": 0.999}, 1e-5))
add("new-plant-ds-extr20C-ester0.999", "plant62-settled-extr20C",
    "as new-plant-ds-ester0.999, on the plant with the extractor at 20 C (round 5)",
    "round 5: 20 C and 6,506 kg/h gave 99.666 %; can the ethanol feed alone reach 99.9 % there",
    lambda r: design_spec(r, {"stream": "S16", "quantity": "mass_fraction", "component": ESTER, "value": 0.999}, 1e-5))
add("new-plant-ds-ethanol0.0004", "plant62-best-init1e-4-tol1e-5",
    "designSpecs: F1 ethanol flow_kg_h in [6490, 6515] (guess 6511) to hold S16 ethanol mass fraction 0.0004 (tolerance 1e-5)",
    "the paper's ethanol limit in the product (< 0.04 %, Section 3.4): the excess ethanol's only exit (round 4)",
    lambda r: design_spec(r, {"stream": "S16", "quantity": "mass_fraction", "component": ETOH, "value": 0.0004}, 1e-5))


def main():
    OUT.mkdir(exist_ok=True)
    for rid, (r, why) in RUNS.items():
        (OUT / f"{rid}.request.json").write_text(json.dumps(r, indent=2) + "\n")
        (OUT / f"{rid}.why.json").write_text(json.dumps(why, indent=1) + "\n")
        print(rid)


if __name__ == "__main__":
    main()
