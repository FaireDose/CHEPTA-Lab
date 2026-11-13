"""The S2 plant of Piotrowski & Kubica 2021 as ONE closed CHEPTA flowsheet, for chepta 0.6.2.

Builds on s2_model.py (unchanged, bound to the 0.6.1 runs) and adds what 0.6.2 makes possible:
  - all four components everywhere (no cut at stream 9): 0.6.2 holds two liquids with acetic acid;
  - feeds 1 and 2 at the printed 15 C: 0.6.2 continues the acid's records below 16.66 C with a warning;
  - splitters by flow (flow_kg_h, one outlet "rest"): stream 26 = 60,000 kg/h and stream 25 = 20,000 kg/h (Table A2);
  - MIX 7 a plain (adiabatic) mixer: 0.6.2's extractor accepts a feed with up to 10 % vapour;
  - column 5 with two liquids allowed on its stages (phases "VLL"), which 0.6.1 did not build for an absorber.
No CHEPTA call here. Settings that differ from s2_model.SETTINGS are listed in SETTINGS_062 (kind, locator, reason).
"""
import copy

import s2_model as M

T_FEED_C = 15.0  # Table A2 streams 1-3, as printed

SETTINGS_062 = [
    {"what": "feeds 1 and 2 temperature", "value": "15 C as printed", "kind": "paper", "locator": "Table A2 streams 1-3",
     "reason": "chepta 0.6.2 continues acetic acid's records below its triple point (16.66 C) with a warning listed in result.extrapolations; 0.6.1 refused it."},
    {"what": "components", "value": "ethanol, water, ethyl acetate, acetic acid in every block; no cut at stream 9", "kind": "paper",
     "locator": "Table A2 (acetic acid 0.00-0.01 mass % downstream of column 5)",
     "reason": "0.6.2 holds two liquids with acetic acid (VLLE with the acid's chemical theory)."},
    {"what": "splitter 9", "value": "stream 26 = 60,000 kg/h (flow_kg_h), stream 12 the rest", "kind": "paper", "locator": "Table A2 streams 26, 27",
     "reason": "The round 60,000 kg/h is read as the paper's flow specification; 0.6.2 has a splitter by flow."},
    {"what": "splitter 16", "value": "variant W: stream 25 = 20,000 kg/h (flow_kg_h), 23 the rest; variant R: stream 23 = 95,797 kg/h, 25 the rest", "kind": "paper",
     "locator": "Table A2 streams 22, 23, 25",
     "reason": "The round 20,000 kg/h is read as the paper's specification (variant W). The paper's own plant balance is 27 kg/h short (STREAM_EQUIPMENT_AUDIT.md: S2 plant -27 kg/h), so with feeds fixed, wastewater 25 fixed at 20,000 kg/h forces the product flow to 32,461 - 20,000 = 12,461 kg/h; variant R fixes the recycle 23 instead and lets the wastewater follow."},
    {"what": "MIX 7", "value": "as in 0.6.1: a mixer whose outlet is brought to saturated liquid (VF = 0), its duty reported; variant: adiabatic mixer", "kind": "assumed", "locator": "Figure 1 (MIX 7, no duty in Table 1)",
     "reason": "0.6.2's extractor takes a feed with up to 0.1 vapour fraction (the 0.6.1 refusal secB-mix7-adiabatic now runs), but inside the closed water loop the adiabatic mixer's outlet reached 0.17 vapour and the extractor refused it (BAD_INPUT); the saturated-liquid mixer of 0.6.1 is kept."},
    {"what": "SCDS 5", "value": "absorber-type column as before, phases VLL", "kind": "assumed",
     "locator": "runs diag-scds5-round2-inlets (PHASE_SPLIT on stage 7 with VL) and diag-scds5-round2-inlets-VLL",
     "reason": "With the plant's own recycles a second liquid forms on stage 7; 0.6.2 builds two liquids on an absorber's stages."},
    {"what": "SCDS 11 second specification", "value": "variant W: distillate 14 = 230.4 kmol/h (Table A2 stream 14), product purity a result; variant R: bottoms purity 99.90 mass % or bottoms 141.5 kmol/h", "kind": "paper + assumed",
     "locator": "Table A2 streams 14, 16; Section 3.4 p.8",
     "reason": "With variant W both product and wastewater flows are fixed by the balance, so the product column cannot also fix the product's flow or purity; its distillate flow is taken from the paper."},
    {"what": "tear streams", "value": "7, 15, 21, 24, 27 with Table A2 starting guesses; CHEPTA's Broyden method", "kind": "assumed",
     "reason": "Starting points only."},
]


def splitter_by_flow(first_kg_h=None, second_kg_h=None):
    """Two outlets in the order of the flowsheet's streams; one of them "rest"."""
    return {"flow_kg_h": [first_kg_h if first_kg_h is not None else "rest", second_kg_h if second_kg_h is not None else "rest"]}


def plant(split16="W", spec11="distillate", phases5="VLL", phases11="VLL", phases15="VLL", extractor_stages=2,
          T_feed_C=T_FEED_C, thermo_extra=None, max_iter=200, method=None, open_recycles=None, guesses=None, mix7="VF0", split9="flow", col5_max_iter=None, col5_stages=None, spec15="distillate", tolerance=None):
    """open_recycles: None for the closed plant; else {27: feed spec, 21: feed spec}: streams 27 and 21 enter as feeds
    (given) and leave as products, the outer recycles opened (used to find starting guesses, never compared as the plant).
    guesses: {stream number: {flow_kmol_h, T_K, P_kPa}} starting guesses of the tear streams (else Table A2)."""
    C = M.COMPONENTS
    s9 = splitter_by_flow(None, M.STREAMS[26]["mass_kg_h"]) if split9 == "flow" else {"fractions": M.split9()}  # S12 (rest), S26 (60,000)
    if split16 == "W":
        s16 = splitter_by_flow(None, M.STREAMS[25]["mass_kg_h"])  # outlets: S23 (rest), S25 (20,000)
    elif split16 == "R":
        s16 = splitter_by_flow(M.STREAMS[23]["mass_kg_h"], None)  # S23 (95,797), S25 (rest)
    else:
        s16 = {"fractions": M.split16()}
    c5 = M.column5_spec()
    if col5_stages:  # Section 3.2 p.7: "a minimum number of 14 theoretical stages"; vapour 6 on the last stage
        c5["stages"] = col5_stages
        c5["feed_stage"] = [1, col5_stages]
    if phases5:
        c5["phases"] = phases5
    if col5_max_iter:
        c5["max_iterations"] = col5_max_iter
    c11 = M.column11_spec("flow" if spec11 == "bottoms" else "purity", phases11)
    if spec11 == "distillate":
        c11.pop("bottoms_purity", None)
        c11["distillate_kmol_h"] = M.STREAMS[14]["molar_kmol_h"]
    c15 = M.column15_spec(phases15)
    if spec15 == "purity":  # Section 3.5 p.10: bottoms "less than 0.01% of its weight in organic compounds"
        c15.pop("distillate_kmol_h")
        c15["bottoms_purity"] = {"component": "water", "value": 0.9999, "basis": "mass"}
    elif isinstance(spec15, (int, float)):  # a distillate flow other than the paper's (column 15 isolated runs)
        c15["distillate_kmol_h"] = spec15
    B = [
        {"id": "F1", "type": "feed", "spec": M.feed_spec(1, C, T_C=T_feed_C)},
        {"id": "F2", "type": "feed", "spec": M.feed_spec(2, C, T_C=T_feed_C)},
        {"id": "F17", "type": "feed", "spec": M.feed_spec(17, C)},
        {"id": "MIX1", "type": "mixer"},
        {"id": "HTXR2", "type": "heater", "spec": M.heater(4)},
        {"id": "MIX3", "type": "mixer"},
        {"id": "KREA4", "type": "conversion-reactor", "spec": M.reactor_spec()},
        {"id": "SCDS5", "type": "column", "spec": c5},
        {"id": "HTXR6", "type": "heater", "spec": {"VF": 0, "P_kPa": M.P_KPA}},
        {"id": "MIX7", "type": "mixer"} if mix7 == "adiabatic" else {"id": "MIX7", "type": "heater", "spec": {"VF": 0, "P_kPa": M.P_KPA}},
        {"id": "EXTR8", "type": "extraction", "spec": M.extractor_spec(extractor_stages)},
        {"id": "SPLIT9", "type": "splitter", "spec": s9},
        {"id": "HTXR10", "type": "heater", "spec": M.heater(13)},
        {"id": "SCDS11", "type": "column", "spec": c11},
        {"id": "HTXR12", "type": "heater", "spec": {"duty_kW": M.EQUIP[12]["S2"]["duty_kW"], "P_kPa": M.P_KPA}},
        {"id": "MIX13", "type": "mixer"},
        {"id": "PUMP14", "type": "pump", "spec": {"P_kPa": M.P_KPA}},
        {"id": "SCDS15", "type": "column", "spec": c15},
        {"id": "SPLIT16", "type": "splitter", "spec": s16},
        {"id": "HTXR17", "type": "heater", "spec": M.heater(24)},
        {"id": "HTXR18", "type": "heater", "spec": M.heater(27)},
        {"id": "HTXR19", "type": "heater", "spec": M.heater(28)},
        {"id": "P16", "type": "product"}, {"id": "P25", "type": "product"},
    ]
    S = [("S1", "F1.out", "MIX1.in"), ("S2", "F2.out", "MIX1.in"), ("S3", "MIX1.out", "HTXR2.in"),
         ("S4", "HTXR2.out", "MIX3.in"), ("S7", "SCDS5.bottoms", "MIX3.in"), ("S21", "SCDS15.distillate", "MIX3.in"),
         ("S5", "MIX3.out", "KREA4.in"), ("S27", "HTXR18.out", "SCDS5.in"), ("S6", "KREA4.out", "SCDS5.in"),
         ("S8", "SCDS5.distillate", "HTXR6.in"), ("S9", "HTXR6.out", "MIX7.in"), ("S15", "HTXR12.out", "MIX7.in"),
         ("S10", "MIX7.out", "EXTR8.feed"), ("S19", "PUMP14.out", "EXTR8.solvent"),
         ("S11", "EXTR8.raffinate", "SPLIT9.in"), ("S20", "EXTR8.extract", "HTXR19.in"),
         ("S12", "SPLIT9.out", "HTXR10.in"), ("S26", "SPLIT9.out", "HTXR18.in"),
         ("S13", "HTXR10.out", "SCDS11.in"), ("S14", "SCDS11.distillate", "HTXR12.in"), ("S16", "SCDS11.bottoms", "P16.in"),
         ("S17", "F17.out", "MIX13.in"), ("S24", "HTXR17.out", "MIX13.in"), ("S18", "MIX13.out", "PUMP14.in"),
         ("S28", "HTXR19.out", "SCDS15.in"), ("S22", "SCDS15.bottoms", "SPLIT16.in"),
         ("S23", "SPLIT16.out", "HTXR17.in"), ("S25", "SPLIT16.out", "P25.in")]
    tears = (7, 15, 21, 24, 27)
    if open_recycles:
        B += [{"id": "F27", "type": "feed", "spec": open_recycles[27]}, {"id": "F21", "type": "feed", "spec": open_recycles[21]},
              {"id": "P27", "type": "product"}, {"id": "P21", "type": "product"}]
        S = [s for s in S if s[0] not in ("S27", "S21")]
        S += [("S27", "F27.out", "SCDS5.in"), ("S27o", "HTXR18.out", "P27.in"), ("S21", "F21.out", "MIX3.in"),
              ("S21o", "SCDS15.distillate", "P21.in")]
        tears = (7, 15, 24)
    # SCDS5's inlets in this order: reflux 27 (stage 1), then the vapour 6 (stage 8)
    d = M.doc(B, _streams(S, tears, C, ("S27", "S6"), guesses), C, reactions=True)
    d["solver"] = {"maxIterations": max_iter}
    if method:
        d["solver"]["method"] = method
    if tolerance:
        d["solver"]["tolerance"] = tolerance
    if thermo_extra:
        d["thermo"].update(thermo_extra)
    return d


def _streams(S, tears, comps, order_first=(), guesses=None):
    """As s2_model._streams, accepting stream ids with a suffix (S27o: the opened outlet of stream 27)."""
    S = sorted(S, key=lambda s: order_first.index(s[0]) if s[0] in order_first else len(order_first))
    out = []
    for sid, a, b in S:
        st = {"id": sid, "from": a, "to": b}
        n = int(sid[1:].rstrip("o"))
        if n in tears and not sid.endswith("o"):
            st["tear"] = True
            st["guess"] = (guesses or {}).get(n) or M.guess(n, comps)
        out.append(st)
    return out


def with_options(req, **opts):
    r = copy.deepcopy(req)
    r["options"] = opts
    return r


def section_b4(s9, s25_kg_h=None, s23_kg_h=None, spec11="distillate", spec15="distillate", phases11="VLL", phases15="VLL",
               extractor_stages=2):
    """The downstream half (MIX 7 to the water loop) with all four components, fed with CHEPTA's own stream 9 (a feed
    {flow_kmol_h, T_K or VF, P_kPa}); streams 21 and 27 leave as products (the outer recycles open). Used to see how the
    wastewater flow 25 moves the column purities when the closed plant does not converge; never compared as the plant."""
    C = M.COMPONENTS
    s16 = splitter_by_flow(s23_kg_h, None) if s23_kg_h else splitter_by_flow(None, s25_kg_h)
    c11 = M.column11_spec("flow" if spec11 == "bottoms" else "purity", phases11)
    if spec11 == "distillate":
        c11.pop("bottoms_purity", None)
        c11["distillate_kmol_h"] = M.STREAMS[14]["molar_kmol_h"]
    c15 = M.column15_spec(phases15)
    if spec15 == "purity":
        c15.pop("distillate_kmol_h")
        c15["bottoms_purity"] = {"component": "water", "value": 0.9999, "basis": "mass"}
    B = [
        {"id": "F9", "type": "feed", "spec": s9},
        {"id": "F17", "type": "feed", "spec": M.feed_spec(17, C)},
        {"id": "MIX7", "type": "heater", "spec": {"VF": 0, "P_kPa": M.P_KPA}},
        {"id": "EXTR8", "type": "extraction", "spec": M.extractor_spec(extractor_stages)},
        {"id": "SPLIT9", "type": "splitter", "spec": splitter_by_flow(None, M.STREAMS[26]["mass_kg_h"])},
        {"id": "HTXR10", "type": "heater", "spec": M.heater(13)},
        {"id": "SCDS11", "type": "column", "spec": c11},
        {"id": "HTXR12", "type": "heater", "spec": {"duty_kW": M.EQUIP[12]["S2"]["duty_kW"], "P_kPa": M.P_KPA}},
        {"id": "MIX13", "type": "mixer"},
        {"id": "PUMP14", "type": "pump", "spec": {"P_kPa": M.P_KPA}},
        {"id": "SCDS15", "type": "column", "spec": c15},
        {"id": "SPLIT16", "type": "splitter", "spec": s16},
        {"id": "HTXR17", "type": "heater", "spec": M.heater(24)},
        {"id": "HTXR18", "type": "heater", "spec": M.heater(27)},
        {"id": "HTXR19", "type": "heater", "spec": M.heater(28)},
        {"id": "P16", "type": "product"}, {"id": "P25", "type": "product"}, {"id": "P27", "type": "product"}, {"id": "P21", "type": "product"},
    ]
    S = [("S9", "F9.out", "MIX7.in"), ("S15", "HTXR12.out", "MIX7.in"),
         ("S10", "MIX7.out", "EXTR8.feed"), ("S19", "PUMP14.out", "EXTR8.solvent"),
         ("S11", "EXTR8.raffinate", "SPLIT9.in"), ("S20", "EXTR8.extract", "HTXR19.in"),
         ("S12", "SPLIT9.out", "HTXR10.in"), ("S26", "SPLIT9.out", "HTXR18.in"), ("S27", "HTXR18.out", "P27.in"),
         ("S13", "HTXR10.out", "SCDS11.in"), ("S14", "SCDS11.distillate", "HTXR12.in"), ("S16", "SCDS11.bottoms", "P16.in"),
         ("S17", "F17.out", "MIX13.in"), ("S24", "HTXR17.out", "MIX13.in"), ("S18", "MIX13.out", "PUMP14.in"),
         ("S28", "HTXR19.out", "SCDS15.in"), ("S21", "SCDS15.distillate", "P21.in"), ("S22", "SCDS15.bottoms", "SPLIT16.in"),
         ("S23", "SPLIT16.out", "HTXR17.in"), ("S25", "SPLIT16.out", "P25.in")]
    d = M.doc(B, _streams(S, (15, 24), C), C)
    return d
