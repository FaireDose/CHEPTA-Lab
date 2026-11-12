"""The classic ethyl acetate plant S2 of Piotrowski & Kubica 2021 (Processes 9, 1425, CC BY 4.0) as CHEPTA requests.

No CHEPTA call here: this module only builds the request documents from the case's transcriptions
(streams.json = Table A2, equipment.json = Table 1 and Figure 1). Every setting carries where it comes from:
  "paper"    a value printed in the paper (locator given),
  "derived"  calculated by Lab from printed values (the calculation given),
  "assumed"  chosen by Lab because the paper does not give it, or because CHEPTA refused the paper's value (reason given).
SETTINGS is written into the run manifest, so each run states what it was given.

Three levels of runs (run_s2_chepta_0.6.1.py):
  units      every unit alone, fed with the paper's own inlet streams (Table A2);
  sections   section A (reaction and azeotropic column, 4 components, recycle 7) and section B (extraction, product
             and wastewater columns, water loop; 3 components, recycles 15 and 24), each fed at the cut with the paper's
             streams;
  plant      the two sections coupled by Lab's script across the cut (streams 9, 21, 27), by successive substitution.
Why the cut: CHEPTA 0.6.1 refuses any two-liquid stream while acetic acid (vapour by the chemical theory) is a
component (PHASE_SPLIT / NOT_AVAILABLE, kept in the unit runs u-*). Section B is therefore run without acetic acid,
which the paper prints at 0.00-0.01 mass % downstream of the azeotropic column; the acetic acid dropped at the cut is
counted in every plant run.
Units of the requests: K, kPa, kg/h or kmol/h, kW (CHEPTA's).
"""
import json
from pathlib import Path

H = Path(__file__).resolve().parent
STREAMS = {int(r["stream"]): r for r in json.loads((H / "streams.json").read_text())["strategies"]["S2"]}
EQUIP = {e["id"]: e for e in json.loads((H / "equipment.json").read_text())["equipment"]}

COMPONENTS = ["ethanol", "water", "ethyl acetate", "acetic acid"]
COMPONENTS_B = ["ethanol", "water", "ethyl acetate"]
KEYS = ["ethanol", "water", "ethyl_acetate", "acetic_acid"]
IDS = ["ethanol", "water", "ethyl-acetate", "acetic-acid"]  # CHEPTA's component ids
C_TO_K = 273.15
P_KPA = 100.0  # Table A2 prints 1 bar for every stream (1 bar = 100 kPa)
T_ACID_FEED_C = 18.0  # assumed, see SETTINGS
T_EXTR_C = STREAMS[11]["T_C"]  # 27 C: the raffinate's outlet temperature, Table A2 stream 11 (assumed isothermal)
# molar masses only for the starting guesses of tear streams (kg/h -> kmol/h); never for a compared number
_MW_GUESS = [46.069, 18.015, 88.106, 60.052]

THERMO = {"model": "UNIQUAC", "vapour": "ideal"}

SETTINGS = [
    {"what": "property method", "value": "UNIQUAC liquid, ideal-gas vapour; CHEPTA applies its chemical theory (dimers) to acetic acid in the vapour; CHEPTA's default UNIQUAC pair sets",
     "kind": "paper + assumed", "locator": "Section 2.1, p.5 (UNIQUAC for VLE and LLE)",
     "reason": "The paper names UNIQUAC but prints neither its parameters (Chemcad 7's) nor the vapour model. CHEPTA's own UNIQUAC sets are reused (AGENTS.md)."},
    {"what": "pressure", "value": "100 kPa everywhere, no pressure drop", "kind": "paper",
     "locator": "Table A2, column 'Pres. Bar' = 1 for every stream, pp.13-14",
     "reason": "Section 2 (p.4) says 'atmospheric pressure' (101.325 kPa, 1.3 % higher); the printed 1 bar is used."},
    {"what": "feeds 1, 2 and 17", "value": "Table A2 mass flows and compositions; 17 is at 20 C", "kind": "paper", "locator": "Table A2 streams 1, 2, 17, pp.13-14"},
    {"what": "feeds 1 (ethanol) and 2 (acetic acid) temperature", "value": f"{T_ACID_FEED_C} C instead of the printed 15 C", "kind": "assumed",
     "locator": "Table A2 streams 1-3 (15 C); CHEPTA runs u-htxr2-15C and secA-feeds-15C-17C (refused)",
     "reason": "Pure acetic acid at 15 C is below its triple point (289.81 K = 16.66 C in CHEPTA's ChemSep-based record), and CHEPTA refuses a liquid with acetic acid below that temperature even mixed with ethanol (OUT_OF_RANGE). The two feeds cool by about 1 K on mixing, so 18 C, the lowest whole degree for which CHEPTA's MIX 1 outlet (about 17.0 C) stays above it, is used for both (17 C was refused, run secA-feeds-17C). Effect: HTXR 2 heats from about 17 C instead of 15 C."},
    {"what": "HTXR 2 outlet", "value": "70 C", "kind": "paper", "locator": "Table A2 stream 4"},
    {"what": "KREA 4 reaction", "value": "ethanol + acetic acid -> ethyl acetate + water (liquid), acetic acid conversion per pass 0.7703",
     "kind": "derived", "locator": "Table A2 streams 5 and 6",
     "reason": "1 - (53292 x 4.74 %)/(53292 x 20.64 %) = 0.7703. The paper's kinetics (Eqs. 1-3, pp.5-6, after Atalay) cannot be used: the catalyst concentration and the units of C are not given; CHEPTA has no reactor-evaporator (a boiling, reacting liquid whose only outlet is its vapour). The reactor's conversion is therefore IMPOSED from the paper, not predicted; its outlet temperature and duty are results."},
    {"what": "KREA 4 outlet", "value": "saturated vapour (VF = 1) at 100 kPa", "kind": "paper",
     "locator": "Section 2, p.4 ('The vapors from the reactor (Stream 6)'); Table A2 streams 5 and 6 both 53,292 kg/h",
     "reason": "Everything that enters leaves as vapour; the printed 90 C is compared, not imposed."},
    {"what": "SCDS 5 azeotropic column", "value": "absorber-type column, no condenser or reboiler, 8 equilibrium stages, reflux 27 on stage 1, reactor vapour 6 on stage 8, adiabatic",
     "kind": "paper + assumed", "locator": "Table 1 p.11 (8 stages, feed stage 8, R/V 0.61); Section 3.2 p.6 ('reactor vapors are fed to the last stage ... reflux (Stream 27) ... onto the first stage'); Figure 1 p.4 (no condenser or reboiler drawn)",
     "reason": "Stage efficiency not given: equilibrium stages assumed. R/V = 0.61 is not a setting here: it equals stream 27 over stream 8 on mass (60000/98380 = 0.610, derived). Section 3.2 asks for at least 14 stages; Table 1 says 8 (paper's discrepancy kept)."},
    {"what": "HTXR 6 outlet", "value": "saturated liquid (VF = 0) at 100 kPa", "kind": "assumed",
     "locator": "Table A2 streams 8, 9 (both printed 70 C); CHEPTA run u-htxr6-70C",
     "reason": "At the printed 70 C and 100 kPa CHEPTA finds stream 8's composition 72 % vapour (just above its bubble point); the stream goes to an extractor, so total condensation is taken. Its temperature is compared with 70 C."},
    {"what": "cut between sections A and B", "value": "acetic acid removed from stream 9 and not a component of section B", "kind": "assumed",
     "locator": "Table A2: acetic acid 0.01 mass % in streams 9-13, 16, 18-20, 22-28, 0.00 % in 14, 15, 21; CHEPTA runs u-htxr10, u-htxr12, u-htxr18, u-htxr19, u-scds11-* (refused)",
     "reason": "With acetic acid present CHEPTA refuses every stream that holds two liquids (the three-phase flash with the acid chemical theory is not built). The acid dropped is reported in every run; it is not replaced by a split."},
    {"what": "MIX 7", "value": "a mixer whose outlet is brought to saturated liquid (VF = 0): CHEPTA's heater block with two inlets; its duty is reported", "kind": "assumed",
     "locator": "Figure 1 p.4 (MIX 7, no duty); Table A2 stream 10 (70 C, the extractor's feed); CHEPTA run secB-mix7-adiabatic (refused)",
     "reason": "Adiabatic mixing of the saturated azeotrope 9 and the product column distillate 15 leaves a few % vapour in CHEPTA, and CHEPTA's Extraction block refuses a feed with any vapour (BAD_INPUT), although its stages are at 27 C. The small condensing duty this adds is not in the paper and is reported."},
    {"what": "EXTR 8 extractor", "value": f"countercurrent equilibrium stages, isothermal at {T_EXTR_C:g} C; organic 10 the feed, water 19 the solvent",
     "kind": "paper + assumed", "locator": "Table 1 p.11 (70 C, W/A = 1); Table A2 streams 11 (27 C) and 20 (41 C); CHEPTA run u-extr8-*-70C (refused)",
     "reason": "Table 1's 70 C is not usable as the stage temperature: the paper's feed at 70 C and 100 kPa is 77 % vapour in CHEPTA (refused, run u3-extr8-1stage-70C-feed70C), and with a saturated-liquid feed the 70 C extractor runs (u3-extr8-1stage-70C) but its outlets are partly vapour (raffinate VF 0.05), which CHEPTA returns as ok without a warning. The paper's own outlets (27 C organic, 41 C aqueous) imply an adiabatic extractor, which CHEPTA's isothermal block cannot do; 27 C, where the raffinate leaves, is taken, with a 41 C variant. W/A = 1 is not a setting: stream 19 / stream 10 = 113276/113256 = 1.000 (derived)"},
    {"what": "EXTR 8 number of stages", "value": "not given in the paper; 1 to 8 stages run, plant run with the number stated in the run manifest", "kind": "assumed",
     "reason": "The paper gives no stage count, efficiency or contactor type for EXTR 8."},
    {"what": "splitter 9", "value": "fraction to stream 26 = 60000/87314 = 0.68718", "kind": "derived",
     "locator": "Table A2 streams 11, 26", "reason": "The round 60,000 kg/h suggests a flow specification in Chemcad; CHEPTA's splitter takes fractions only."},
    {"what": "HTXR 18 outlet", "value": "70 C", "kind": "paper", "locator": "Table A2 stream 27"},
    {"what": "HTXR 10 outlet", "value": "71 C", "kind": "paper", "locator": "Table A2 stream 13"},
    {"what": "SCDS 11 product column", "value": "35 stages (1 the condenser, 35 the reboiler), feed stage 15, total condenser, R/D = 3, bottoms 141.5 kmol/h (Table A2 stream 16); two liquids allowed on the stages (VLL)",
     "kind": "paper + assumed", "locator": "Table 1 p.11 (35 stages, feed 15, R/D 3); Section 3.4 p.8 ('purity greater than 99.9 %', 'EA content in the product (99.9 wt%)'); Table A2 stream 16",
     "reason": "Chemcad's stage count assumed to include condenser and reboiler, as CHEPTA's does. Total condenser assumed (stream 14 all recycled). Section 3.4 places the best feed between stages 4 and 6, Table 1 says 15 (paper's discrepancy kept). The product purity is then a result, compared with 99.90 mass %. Variant (unit run u3-scds11-purity): the purity 99.90 mass % (Section 3.4) in place of the bottoms flow."},
    {"what": "HTXR 12", "value": "duty 0 kW", "kind": "paper", "locator": "Table 1 p.11 (S2: 0)"},
    {"what": "block 14", "value": "pump to 100 kPa (no pressure rise)", "kind": "assumed",
     "locator": "Figure 1 p.4 (grey round symbol between MIX 13 and EXTR 8); streams 18 and 19 identical in Table A2",
     "reason": "The paper does not name block 14; its symbol looks like Chemcad's pump. It changes nothing in Table A2."},
    {"what": "HTXR 19 outlet", "value": "70 C", "kind": "paper", "locator": "Table A2 stream 28"},
    {"what": "SCDS 15 wastewater column", "value": "18 stages, feed stage 9, total condenser, R/D = 2, distillate 394.6 kmol/h",
     "kind": "paper + assumed", "locator": "Table 1 p.11 (18 stages, feed 9, R/D 2); Table A2 stream 21",
     "reason": "The paper does not say which second specification Chemcad used; stream 21's molar flow is taken. Section 3.5 (p.10) asks < 0.01 wt% organics in the bottoms, but stream 22 prints 0.03 wt% (paper's discrepancy kept)."},
    {"what": "splitter 16", "value": "fraction to wastewater 25 = 20000/115797 = 0.17272", "kind": "derived",
     "locator": "Table A2 streams 22, 25",
     "reason": "A fixed wastewater flow with a fixed fresh water feed has no steady state unless they match exactly; with a fraction the water loop settles. Stream 25's flow is compared with 20,000 kg/h."},
    {"what": "HTXR 17 outlet", "value": "20 C", "kind": "paper", "locator": "Table A2 stream 24"},
    {"what": "streams 8 (VF = 1), 9, 10, 14, 15, 21, 23 (VF = 0) as feeds of unit runs", "value": "saturated (VF given) where the printed temperature lies at or above CHEPTA's bubble point; stream 3 at 18 C (see feeds 1 and 2)", "kind": "assumed",
     "reason": "Condensates printed at 70-71 C; see HTXR 6."},
    {"what": "tear streams and the coupling across the cut", "value": "starting guesses from Table A2; successive substitution of streams 9, 21, 27 by Lab's script",
     "kind": "assumed", "reason": "Starting points only; a converged answer does not depend on them."},
]


def kg_h(n, comps=COMPONENTS):
    """Component mass flows (kg/h) of Table A2 stream n: printed total x printed mass %, not renormalized."""
    s = STREAMS[n]
    return {c: s["mass_kg_h"] * s[k + "_mass_pct"] / 100 for c, k in zip(COMPONENTS, KEYS) if c in comps}


def feed_spec(n, comps=COMPONENTS, T_C=None, VF=None):
    f = {"flow_kg_h": {c: v for c, v in kg_h(n, comps).items() if v > 0}, "P_kPa": P_KPA}
    if VF is not None:
        f["VF"] = VF
    else:
        f["T_K"] = (STREAMS[n]["T_C"] if T_C is None else T_C) + C_TO_K
    return f


# how each paper stream is given as a feed of a unit run: saturated where the printed T is at its bubble/dew point
FEED_OVERRIDE = {2: {"T_C": T_ACID_FEED_C}, 3: {"T_C": T_ACID_FEED_C}, 8: {"VF": 1}, 9: {"VF": 0}, 10: {"VF": 0}, 14: {"VF": 0}, 15: {"VF": 0}, 21: {"VF": 0}, 23: {"VF": 0}}


def guess(n, comps=COMPONENTS):
    s = STREAMS[n]
    return {"flow_kmol_h": {c: v / m for (c, v), m in zip(kg_h(n).items(), _MW_GUESS) if c in comps},
            "T_K": s["T_C"] + C_TO_K, "P_kPa": P_KPA}


REACTION = {"id": "R1", "name": "esterification", "phase": "liquid",
            "stoichiometry": {"ethanol": -1, "acetic-acid": -1, "ethyl-acetate": 1, "water": 1}}


def acid_conversion():
    """Derived from Table A2: acetic acid in stream 6 over stream 5 (the same total mass flow)."""
    return 1 - kg_h(6)["acetic acid"] / kg_h(5)["acetic acid"]


def reactor_spec():
    return {"reactions": [{"reaction": "R1", "key": "acetic-acid", "conversion": round(acid_conversion(), 4)}], "VF": 1, "P_kPa": P_KPA}


def column5_spec():
    e = EQUIP[5]["S2"]
    return {"mode": "rigorous", "configuration": "absorber", "stages": e["stages"], "feed_stage": [1, e["feed_stage"]], "P_kPa": P_KPA}


def column11_spec(second="purity", phases="VLL"):
    e = EQUIP[11]["S2"]
    spec = {"mode": "rigorous", "stages": e["stages"], "feed_stage": e["feed_stage"], "condenser": "total", "P_kPa": P_KPA,
            "reflux_ratio": e["reflux_ratio"]}
    if second == "purity":
        spec["bottoms_purity"] = {"component": "ethyl acetate", "value": STREAMS[16]["ethyl_acetate_mass_pct"] / 100, "basis": "mass"}
    else:
        spec["bottoms_kmol_h"] = STREAMS[16]["molar_kmol_h"]
    if phases:
        spec["phases"] = phases
    return spec


def column15_spec(phases=None):
    e = EQUIP[15]["S2"]
    spec = {"mode": "rigorous", "stages": e["stages"], "feed_stage": e["feed_stage"], "condenser": "total", "P_kPa": P_KPA,
            "reflux_ratio": e["reflux_ratio"], "distillate_kmol_h": STREAMS[21]["molar_kmol_h"]}
    if phases:
        spec["phases"] = phases
    return spec


def extractor_spec(stages, T_C=T_EXTR_C):
    return {"stages": stages, "T_K": T_C + C_TO_K, "P_kPa": P_KPA}


def split9():
    return [STREAMS[12]["mass_kg_h"] / STREAMS[11]["mass_kg_h"], STREAMS[26]["mass_kg_h"] / STREAMS[11]["mass_kg_h"]]


def split16():
    return [STREAMS[23]["mass_kg_h"] / STREAMS[22]["mass_kg_h"], STREAMS[25]["mass_kg_h"] / STREAMS[22]["mass_kg_h"]]


def heater(n_out):
    return {"T_K": STREAMS[n_out]["T_C"] + C_TO_K, "P_kPa": P_KPA}


def doc(blocks, streams, comps=COMPONENTS, reactions=False):
    d = {"components": comps, "thermo": dict(THERMO), "blocks": blocks, "streams": streams, "solver": {"maxIterations": 200}}
    if reactions:
        d["reactions"] = [REACTION]
    return d


def unit(block, inlets, outlets, comps=COMPONENTS, reactions=False, literal=False):
    """One unit alone: each inlet a Feed holding the paper's stream (port, stream number), each outlet a Product.
    literal: the printed temperature even where FEED_OVERRIDE would replace it (to keep CHEPTA's refusal on record)."""
    blocks, streams = [block], []
    for port, n in inlets:
        blocks.append({"id": f"F{n}", "type": "feed", "spec": feed_spec(n, comps, **({} if literal else FEED_OVERRIDE.get(n, {})))})
        streams.append({"id": f"S{n}", "from": f"F{n}.out", "to": f"{block['id']}.{port}"})
    for port, n in outlets:
        blocks.append({"id": f"P{n}", "type": "product"})
        streams.append({"id": f"S{n}", "from": f"{block['id']}.{port}", "to": f"P{n}.in"})
    return doc(blocks, streams, comps, reactions)


EXTR_STAGES = (1, 2, 3, 4, 5, 8)


def unit_requests():
    U = {}
    B = COMPONENTS_B
    # --- refusals kept on record: the paper's values as printed, with acetic acid as a component
    U["u-htxr2-15C"] = unit({"id": "HTXR2", "type": "heater", "spec": heater(4)}, [("in", 3)], [("out", 4)], literal=True)
    U["u-htxr6-70C"] = unit({"id": "HTXR6", "type": "heater", "spec": heater(9)}, [("in", 8)], [("out", 9)], literal=True)
    U["u-extr8-1stage-70C"] = unit({"id": "EXTR8", "type": "extraction", "spec": extractor_spec(1, 70)},
                                   [("feed", 10), ("solvent", 19)], [("raffinate", 11), ("extract", 20)])
    U["u-extr8-1stage-27C-acid"] = unit({"id": "EXTR8", "type": "extraction", "spec": extractor_spec(1)},
                                        [("feed", 10), ("solvent", 19)], [("raffinate", 11), ("extract", 20)])
    U["u-htxr10-acid"] = unit({"id": "HTXR10", "type": "heater", "spec": heater(13)}, [("in", 12)], [("out", 13)])
    U["u-scds11-acid-VL"] = unit({"id": "SCDS11", "type": "column", "spec": column11_spec("flow", None)}, [("in", 13)], [("distillate", 14), ("bottoms", 16)])
    U["u-scds11-acid-VLL"] = unit({"id": "SCDS11", "type": "column", "spec": column11_spec("flow", "VLL")}, [("in", 13)], [("distillate", 14), ("bottoms", 16)])
    U["u-htxr12-acid"] = unit({"id": "HTXR12", "type": "heater", "spec": {"duty_kW": EQUIP[12]["S2"]["duty_kW"], "P_kPa": P_KPA}}, [("in", 14)], [("out", 15)])
    U["u-htxr18-acid"] = unit({"id": "HTXR18", "type": "heater", "spec": heater(27)}, [("in", 26)], [("out", 27)])
    U["u-htxr19-acid"] = unit({"id": "HTXR19", "type": "heater", "spec": heater(28)}, [("in", 20)], [("out", 28)])
    # --- section A units (4 components)
    U["u-htxr2"] = unit({"id": "HTXR2", "type": "heater", "spec": heater(4)}, [("in", 3)], [("out", 4)])
    U["u-krea4-conversion"] = unit({"id": "KREA4", "type": "conversion-reactor", "spec": reactor_spec()}, [("in", 5)], [("out", 6)], reactions=True)
    U["u-krea4-equilibrium-90C"] = unit({"id": "KREA4", "type": "equilibrium-reactor",
                                          "spec": {"reactions": [{"reaction": "R1"}], "phases": 2, "T_K": 90 + C_TO_K, "P_kPa": P_KPA}},
                                         [("in", 5)], [("out", 6)], reactions=True)
    U["u-scds5"] = unit({"id": "SCDS5", "type": "column", "spec": column5_spec()}, [("in", 27), ("in", 6)], [("distillate", 8), ("bottoms", 7)])
    U["u-htxr6"] = unit({"id": "HTXR6", "type": "heater", "spec": {"VF": 0, "P_kPa": P_KPA}}, [("in", 8)], [("out", 9)])
    U["u-pump14"] = unit({"id": "PUMP14", "type": "pump", "spec": {"P_kPa": P_KPA}}, [("in", 18)], [("out", 19)])
    U["u-htxr17"] = unit({"id": "HTXR17", "type": "heater", "spec": heater(24)}, [("in", 23)], [("out", 24)])
    # --- section B units (3 components, acetic acid dropped from the paper's streams)
    for n in EXTR_STAGES:
        U[f"u3-extr8-{n}stage"] = unit({"id": "EXTR8", "type": "extraction", "spec": extractor_spec(n)},
                                       [("feed", 10), ("solvent", 19)], [("raffinate", 11), ("extract", 20)], B)
    U["u3-extr8-1stage-70C"] = unit({"id": "EXTR8", "type": "extraction", "spec": extractor_spec(1, 70)},
                                    [("feed", 10), ("solvent", 19)], [("raffinate", 11), ("extract", 20)], B)
    U["u3-extr8-1stage-70C-feed70C"] = unit({"id": "EXTR8", "type": "extraction", "spec": extractor_spec(1, 70)},
                                            [("feed", 10), ("solvent", 19)], [("raffinate", 11), ("extract", 20)], B, literal=True)
    U["u3-extr8-1stage-41C"] = unit({"id": "EXTR8", "type": "extraction", "spec": extractor_spec(1, STREAMS[20]["T_C"])},
                                    [("feed", 10), ("solvent", 19)], [("raffinate", 11), ("extract", 20)], B)
    U["u3-htxr10"] = unit({"id": "HTXR10", "type": "heater", "spec": heater(13)}, [("in", 12)], [("out", 13)], B)
    U["u3-scds11-purity"] = unit({"id": "SCDS11", "type": "column", "spec": column11_spec("purity")}, [("in", 13)], [("distillate", 14), ("bottoms", 16)], B)
    U["u3-scds11-bottomsflow"] = unit({"id": "SCDS11", "type": "column", "spec": column11_spec("flow")}, [("in", 13)], [("distillate", 14), ("bottoms", 16)], B)
    U["u3-scds11-bottomsflow-VL"] = unit({"id": "SCDS11", "type": "column", "spec": column11_spec("flow", None)}, [("in", 13)], [("distillate", 14), ("bottoms", 16)], B)
    U["u3-htxr12"] = unit({"id": "HTXR12", "type": "heater", "spec": {"duty_kW": EQUIP[12]["S2"]["duty_kW"], "P_kPa": P_KPA}}, [("in", 14)], [("out", 15)], B)
    U["u3-htxr18"] = unit({"id": "HTXR18", "type": "heater", "spec": heater(27)}, [("in", 26)], [("out", 27)], B)
    U["u3-htxr19"] = unit({"id": "HTXR19", "type": "heater", "spec": heater(28)}, [("in", 20)], [("out", 28)], B)
    U["u3-scds15"] = unit({"id": "SCDS15", "type": "column", "spec": column15_spec()}, [("in", 28)], [("distillate", 21), ("bottoms", 22)], B)
    U["u3-scds15-VLL"] = unit({"id": "SCDS15", "type": "column", "spec": column15_spec("VLL")}, [("in", 28)], [("distillate", 21), ("bottoms", 22)], B)
    return U


def _streams(S, tears, comps, order_first=(), guesses=None):
    S = sorted(S, key=lambda s: order_first.index(s[0]) if s[0] in order_first else len(order_first))
    out = []
    for sid, a, b in S:
        st = {"id": sid, "from": a, "to": b}
        n = int(sid[1:])
        if n in tears:
            st["tear"] = True
            st["guess"] = (guesses or {}).get(n) or guess(n, comps)
        out.append(st)
    return out


def section_a(s27=None, s21=None, T_feeds_C=T_ACID_FEED_C, guesses=None):
    """Reaction and azeotropic column. s27, s21: feeds {flow_kmol_h by CHEPTA id, T_K, P_kPa} from section B, else the paper's."""
    f27 = s27 or feed_spec(27)
    f21 = s21 or feed_spec(21, VF=0)
    B = [
        {"id": "F1", "type": "feed", "spec": feed_spec(1, T_C=T_feeds_C)},
        {"id": "F2", "type": "feed", "spec": feed_spec(2, T_C=T_feeds_C)},
        {"id": "F27", "type": "feed", "spec": f27},
        {"id": "F21", "type": "feed", "spec": f21},
        {"id": "MIX1", "type": "mixer"},
        {"id": "HTXR2", "type": "heater", "spec": heater(4)},
        {"id": "MIX3", "type": "mixer"},
        {"id": "KREA4", "type": "conversion-reactor", "spec": reactor_spec()},
        {"id": "SCDS5", "type": "column", "spec": column5_spec()},
        {"id": "HTXR6", "type": "heater", "spec": {"VF": 0, "P_kPa": P_KPA}},
        {"id": "P9", "type": "product"},
    ]
    S = [("S1", "F1.out", "MIX1.in"), ("S2", "F2.out", "MIX1.in"), ("S3", "MIX1.out", "HTXR2.in"),
         ("S4", "HTXR2.out", "MIX3.in"), ("S7", "SCDS5.bottoms", "MIX3.in"), ("S21", "F21.out", "MIX3.in"),
         ("S5", "MIX3.out", "KREA4.in"), ("S27", "F27.out", "SCDS5.in"), ("S6", "KREA4.out", "SCDS5.in"),
         ("S8", "SCDS5.distillate", "HTXR6.in"), ("S9", "HTXR6.out", "P9.in")]
    # SCDS5's inlets in this order: reflux 27 (stage 1), then the vapour 6 (stage 8)
    return doc(B, _streams(S, (7,), COMPONENTS, ("S27", "S6"), guesses), COMPONENTS, reactions=True)


def section_b(extractor_stages, s9=None, phases11="VLL", phases15=None, spec11="flow", mix7_adiabatic=False, guesses=None):
    """Extraction, product and wastewater columns, water loop; 3 components. s9: feed from section A, else the paper's."""
    comps = COMPONENTS_B
    f9 = s9 or feed_spec(9, comps, VF=0)
    B = [
        {"id": "F9", "type": "feed", "spec": f9},
        {"id": "F17", "type": "feed", "spec": feed_spec(17, comps)},
        {"id": "MIX7", "type": "mixer"} if mix7_adiabatic else {"id": "MIX7", "type": "heater", "spec": {"VF": 0, "P_kPa": P_KPA}},
        {"id": "EXTR8", "type": "extraction", "spec": extractor_spec(extractor_stages)},
        {"id": "SPLIT9", "type": "splitter", "spec": {"fractions": split9()}},
        {"id": "HTXR10", "type": "heater", "spec": heater(13)},
        {"id": "SCDS11", "type": "column", "spec": column11_spec(spec11, phases11)},
        {"id": "HTXR12", "type": "heater", "spec": {"duty_kW": EQUIP[12]["S2"]["duty_kW"], "P_kPa": P_KPA}},
        {"id": "MIX13", "type": "mixer"},
        {"id": "PUMP14", "type": "pump", "spec": {"P_kPa": P_KPA}},
        {"id": "SCDS15", "type": "column", "spec": column15_spec(phases15)},
        {"id": "SPLIT16", "type": "splitter", "spec": {"fractions": split16()}},
        {"id": "HTXR17", "type": "heater", "spec": heater(24)},
        {"id": "HTXR18", "type": "heater", "spec": heater(27)},
        {"id": "HTXR19", "type": "heater", "spec": heater(28)},
        {"id": "P16", "type": "product"}, {"id": "P25", "type": "product"},
        {"id": "P27", "type": "product"}, {"id": "P21", "type": "product"},
    ]
    S = [("S9", "F9.out", "MIX7.in"), ("S15", "HTXR12.out", "MIX7.in"),
         ("S10", "MIX7.out", "EXTR8.feed"), ("S19", "PUMP14.out", "EXTR8.solvent"),
         ("S11", "EXTR8.raffinate", "SPLIT9.in"), ("S20", "EXTR8.extract", "HTXR19.in"),
         ("S12", "SPLIT9.out", "HTXR10.in"), ("S26", "SPLIT9.out", "HTXR18.in"), ("S27", "HTXR18.out", "P27.in"),
         ("S13", "HTXR10.out", "SCDS11.in"), ("S14", "SCDS11.distillate", "HTXR12.in"), ("S16", "SCDS11.bottoms", "P16.in"),
         ("S17", "F17.out", "MIX13.in"), ("S24", "HTXR17.out", "MIX13.in"), ("S18", "MIX13.out", "PUMP14.in"),
         ("S28", "HTXR19.out", "SCDS15.in"), ("S21", "SCDS15.distillate", "P21.in"), ("S22", "SCDS15.bottoms", "SPLIT16.in"),
         ("S23", "SPLIT16.out", "HTXR17.in"), ("S25", "SPLIT16.out", "P25.in")]
    return doc(B, _streams(S, (15, 24), comps, (), guesses), comps)


def as_feed(stream, comps):
    """A CHEPTA result stream as a feed of the other section (component flows, T, P); acetic acid dropped for section B."""
    ids = [IDS[COMPONENTS.index(c)] for c in comps]
    fl = {i: stream["flow_kmol_h"].get(i, 0.0) for i in ids}
    return {"flow_kmol_h": {i: v for i, v in fl.items() if v > 0}, "T_K": stream["T_K"], "P_kPa": stream["P_kPa"]}


def as_guess(stream):
    """A converged CHEPTA stream as the starting guess of the same tear stream in the next round (warm start)."""
    return {"flow_kmol_h": {k: v for k, v in stream["flow_kmol_h"].items() if v > 0}, "T_K": stream["T_K"], "P_kPa": stream["P_kPa"]}
