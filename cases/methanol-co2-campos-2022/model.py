"""Requests for chepta 0.6.2 built from the transcriptions of Lacerda de Oliveira Campos et al. 2022 (one-step process).

Every setting is listed in SETTINGS with its kind (paper, derived, assumed) and its locator or reason. The streams are
streams.json (supplement Tables S9-S10); the blocks are equipment.json (Figure S1, Tables S13-S14, supplement pp.9-11).
The kinetics are Model-6p as printed in the article (Eqs. 8-11, p.8; Table 1, p.9, reprinted there from an ACS paper:
see KINETICS_RIGHTS) and confirmed against the Aspen form of supplement Tables S4-S8 (pp.6-8).

Units of the requests: K, kPa, kmol/h, kW, m. The paper: C, bar, kmol/h, MW.
"""
import copy
import json
from pathlib import Path

H = Path(__file__).resolve().parent
STREAMS = {s["stream"]: s for s in json.loads((H / "streams.json").read_text())["streams"]}

# paper key -> CHEPTA id; O2 only in the burner, which is not modelled (see SETTINGS)
COMP = {"CO2": "carbon-dioxide", "H2": "hydrogen", "CO": "carbon-monoxide", "CH3OH": "methanol", "H2O": "water",
        "N2": "nitrogen"}
COMPONENTS = list(COMP.values())
THERMO_PR = {"model": "PR"}
THERMO_MHV1 = {"model": "PR", "mixing": "MHV1"}

KINETICS_RIGHTS = ("Model-6p constants: article Table 1 (p.9) is 'Reprinted with permission from [19]. Copyright 2021 "
                   "American Chemical Society'; the same numbers are printed in the CC BY supplement in Aspen form "
                   "(Tables S4, S5, S7). Seven numbers of a rate law are used; whether they may be redistributed in "
                   "Lab's files is for the maintainer to decide (open decision in the README).")

SETTINGS = [
    # (what, value, kind, locator or reason)
    ("property method", "Peng-Robinson with CHEPTA's k_ij everywhere", "assumed",
     "paper: PR in the reactors, NRTL2 elsewhere (article p.9); CHEPTA has no NRTL pairs for H2, CO, N2 with methanol and water (README of the case); PR + MHV1 tried for the column and flashes"),
    ("compressor isentropic efficiency", 0.75, "assumed", "not printed; CHEPTA's typical value (NETL-PUB-22478)"),
    ("CP1/CP2/CP3 outlet pressures", "412, 1698, 7000 kPa", "paper", "Table S9 streams 3, 6, 9"),
    ("CP-H2 outlet", "7000 kPa", "paper", "Table S9 stream 12"),
    ("CP-REC outlet", "7000 kPa", "paper", "Table S9 stream 35; supplement p.10"),
    ("HE1 outlet", "30 C", "paper", "Table S9 stream 4; FLASH1 at 30 C (p.9)"),
    ("HE2 specification", "hot outlet 45 C", "paper", "Table S9 stream 7; FLASH2 at 45 C (p.9)"),
    ("HE3", "a cooler on the CO2 side to 111 C; the water side (51W -> 52W) is not modelled", "derived",
     "Table S9 stream 10; the steam cycle is left out of this case"),
    ("HE4 specification", "cold outlet 237.5 C", "paper", "Table S9 stream 14; supplement p.10"),
    ("SPLIT1", "fractions 0.5 / 0.5", "derived", "Table S9 streams 15 and 17 (36557 of 73113 kmol/h each)"),
    ("reactors", "two PFR blocks of 99,000 tubes, 12.5 m, 0.0375 m, bed 1050 kg/m3, dP 75 kPa", "paper",
     "article p.4 and supplement p.9-10; dP from Table S9 (70 -> 69.25 bar)"),
    ("reactor coolant", "boiling water 520.65 K (247.5 C), constant", "paper", "supplement p.10 (54W/56W, 38.07 bar)"),
    ("reactor overall U", "300 W/m2/K (runs at 150 and 1000)", "assumed",
     "not printed: the paper computes U along the tube (supplement Section B, Eqs. S24-S29, outer wall 1000 W/m2/K); the outlet is near the coolant temperature, so it should matter little: checked by the U runs"),
    ("kinetics", "Model-6p, phi_Zn = 0.10 (CO2/COx > 0.90)", "paper",
     "article Eqs. 8-11 (p.8), Table 1 (p.9); phi_Zn rule p.8; CO2/COx of stream 14 = 21.874/(21.874+1.515) = 0.935; Table S4 k = phi exp(A)/1000 = 181.211 confirms phi = 0.10"),
    ("HE5 specification", "minimum approach 2 K on 10 zones in sections and plant (hot outlet 62 C in run u-he5, cold outlet 82.9 C in run u-he5-cold82.9)", "assumed", "the paper fixes 21 at 62 C and 29 at 82.9 C (Table S9); in the loop both met a temperature cross in HE5 (runs sec-loop-a1, sec-loop-a3, sec-loop-direct, sec-loop-wegstein): CHEPTA's stream 20 cannot give that heat above about 70 C"),
    ("HE6 specification", "cold outlet 30 C in sections and plant (hot outlet 56.9 C in run u-he6)", "paper", "Table S9 streams 27 and 22; FLASH4 at 30 C (p.10); with the hot outlet fixed the loop stopped in HE6 (run sec-loop-a2)"),
    ("HE7", "cooler to 30 C (the outlet is the specification; the duty is compared)", "paper",
     "Table S9 stream 23; FLASH3 at 30 C, 69.25 bar (p.10); the maintainer 2026-11-14: compare on the streams first"),
    ("FLASH3, FLASH4", "30 C at 6925 kPa; 30 C at 100 kPa", "paper", "supplement p.10"),
    ("FLASH1, FLASH2", "30 C at 412 kPa; 45 C at 1698 kPa (adiabatic drums after the coolers)", "paper", "supplement p.9"),
    ("SPLIT2, SPLIT3 purge", 0.02, "paper", "supplement p.10"),
    ("valves", "to 100 kPa", "paper", "Table S9 streams 25, 41, 43"),
    ("column", "30 stages (CHEPTA: 1 the condenser, 30 the reboiler), feed on stage 24, reflux ratio 2, 100 kPa",
     "paper", "supplement p.10; stage numbering as Aspen's (condenser 1) assumed"),
    ("column second specification", "bottoms 4581 kmol/h (unit and section runs); in the plant the boil-up ratio 1.17155", "derived",
     "not printed as a specification; the boil-up ratio is CHEPTA's own at bottoms 4581 kmol/h (Table S9 stream 30) in run u-column-partial-flash53. Water recovery 0.99987 and bottoms purity 99.985 mol % were refused (runs plant-a3, plant-a4)"),
    ("column condenser", "see CONDENSER_VARIANTS", "assumed",
     "the paper's condenser gives a vapour and a liquid distillate at 53 C; CHEPTA's gives one or the other"),
    ("fired heater and steam cycle", "left out", "assumed",
     "equipment.json sections: may be left out of the first case; the purges leave as products"),
]


def K(c):
    return c + 273.15


def paper(sid):
    return STREAMS[sid]


def flows(sid, scale=1.0):
    s = STREAMS[sid]
    return {COMP[k]: round(s["molar_kmol_h"] * v / 100 * scale, 6) for k, v in s["mol_pct"].items() if k in COMP and v > 0}


def feed(bid, sid, **over):
    s = STREAMS[sid]
    spec = {"flow_kmol_h": flows(sid), "T_K": round(K(s["T_C"]), 4), "P_kPa": round(s["P_bar"] * 100, 4)}
    spec.update(over)
    return {"id": bid, "type": "feed", "spec": spec}


def guess(sid):
    s = STREAMS[sid]
    return {"flow_kmol_h": flows(sid), "T_K": round(K(s["T_C"]), 4), "P_kPa": round(s["P_bar"] * 100, 4)}


def prod(bid):
    return {"id": bid, "type": "product"}


def doc(blocks, streams, thermo=None, reactions=None, solver=None):
    d = {"components": COMPONENTS, "thermo": copy.deepcopy(thermo or THERMO_PR), "blocks": blocks, "streams": streams}
    if reactions:
        d["reactions"] = reactions
    if solver:
        d["solver"] = solver
    return d


def req(d):
    return {"capability": "solve_flowsheet", "input": {"flowsheet": d}}


def st(sid, a, b, **kw):
    s = {"id": sid, "from": a, "to": b}
    s.update(kw)
    return s


# ---------------------------------------------------------------------------------------------------------------
# Kinetics: Model-6p (article Eqs. 8-11, p.8; Table 1, p.9). Fugacities in bar = f (kPa) / 100.
FB = {"H2": "(f['hydrogen']/100)", "CO2": "(f['carbon-dioxide']/100)", "CO": "(f['carbon-monoxide']/100)",
      "M": "(f['methanol']/100)", "W": "(f['water']/100)"}
THETA = (f"(1/(K2*{FB['H2']}^0.5*{FB['CO2']}+1))*(1/(K3*{FB['H2']}^(-0.5)*{FB['W']}+1))")
KEQ1 = "(T^(-4.481)*exp(4755.7/T+8.369))"     # bar^-2, Table 1
KEQ2 = "(T^(-1.097)*exp(-5337.4/T+12.569))"   # -, Table 1
MODEL6P = {"A2": 14.41, "A3": 29.13, "EA2_J_mol": 94730.0, "EA3_J_mol": 132790.0, "K2": 0.1441, "K3": 49.44, "phi_Zn": 0.10}


def reactions():
    m = MODEL6P
    r1 = (f"exp({m['A2']}-{m['EA2_J_mol']}/(R*T))*phi*{THETA}*{FB['H2']}^1.5*{FB['CO2']}"
          f"*(1-{FB['M']}*{FB['W']}/({FB['H2']}^3*{FB['CO2']}*{KEQ1}))")
    r2 = (f"exp({m['A3']}-{m['EA3_J_mol']}/(R*T))*phi*{THETA}*{FB['CO2']}*{FB['W']}"
          f"*(1-{FB['CO']}*{FB['W']}/({FB['H2']}*{FB['CO2']}*{KEQ2}))")
    consts = {"phi": m["phi_Zn"], "K2": m["K2"], "K3": m["K3"]}
    src = "Model-6p, Lacerda de Oliveira Campos et al. 2022, article Eqs. 8-11 (p.8) and Table 1 (p.9); fit range 210-260 C, 20-60 bar (p.8)"
    return [
        {"id": "R1", "name": "CO2 hydrogenation", "stoichiometry": {"carbon-dioxide": -1, "hydrogen": -3, "methanol": 1, "water": 1},
         "phase": "vapour", "rate": {"form": "expression", "rate": r1, "constants": consts, "per": "catalyst-mass",
                                     "T_K": [483.15, 533.15], "source": src}},
        {"id": "R2", "name": "reverse water-gas shift", "stoichiometry": {"carbon-dioxide": -1, "hydrogen": -1, "carbon-monoxide": 1, "water": 1},
         "phase": "vapour", "rate": {"form": "expression", "rate": r2, "constants": consts, "per": "catalyst-mass",
                                     "T_K": [483.15, 533.15], "source": src}},
    ]


def reactor_spec(U=300.0, tubes=99000):
    return {"reactions": [{"reaction": "R1"}, {"reaction": "R2"}], "L_m": 12.5, "D_m": 0.0375, "tubes": tubes,
            "bed_kg_m3": 1050, "coolant": {"U_W_m2K": U, "T_K": 520.65}, "pressureDrop": {"dP_kPa": 75}}


# ---------------------------------------------------------------------------------------------------------------
# Column variants (the paper: partial vapour-liquid condenser at 53 C, vapour 32 and liquid 31-MEOH)
def column_spec(variant, second):
    base = {"mode": "rigorous", "stages": 30, "feed_stage": 24, "reflux_ratio": 2, "P_kPa": 100}
    if variant == "total":       # total condenser; its liquid distillate is then flashed at 53 C (FLASH-COND)
        base["condenser"] = "total"
    elif variant == "partial":   # partial condenser: one vapour distillate (32 and 31 together)
        base["condenser"] = "partial"
    elif variant == "partial-side":  # vapour distillate = 32; liquid side draw from stage 2 = 31-MEOH
        base["condenser"] = "partial"
        base["side_draws"] = [{"stage": 2, "phase": "liquid", "flow_kmol_h": second.pop("side_kmol_h")}]
    base.update(second)
    return base


# ---------------------------------------------------------------------------------------------------------------
# Single units fed with the paper's inlet streams
def single(block, inlets, outports, thermo=None, rx=None):
    """block: dict without ports; inlets: [(paper stream, port)]; outports: [port]."""
    blocks = [feed(f"F{i}", sid) for i, (sid, _) in enumerate(inlets)] + [block] + [prod(f"P{i}") for i in range(len(outports))]
    streams = [st(f"in{i}-{sid}", f"F{i}.out", f"{block['id']}.{port}") for i, (sid, port) in enumerate(inlets)]
    streams += [st(f"out-{port}", f"{block['id']}.{port}", f"P{i}.in") for i, port in enumerate(outports)]
    return req(doc(blocks, streams, thermo=thermo, reactions=rx))


def unit_runs():
    R = {}
    R["u-cp1"] = single({"id": "CP1", "type": "compressor", "spec": {"P_kPa": 412}}, [("2", "in")], ["out"])
    R["u-he1"] = single({"id": "HE1", "type": "heater", "spec": {"T_K": K(30)}}, [("3", "in")], ["out"])
    R["u-flash1"] = single({"id": "FLASH1", "type": "flash", "spec": {"T_K": K(30), "P_kPa": 412}}, [("4", "in")], ["vapour", "liquid"])
    R["u-cp2"] = single({"id": "CP2", "type": "compressor", "spec": {"P_kPa": 1698}}, [("5", "in")], ["out"])
    R["u-he2"] = single({"id": "HE2", "type": "hx", "spec": {"T_hot_out_K": K(45)}}, [("6", "hot"), ("35", "cold")], ["hot", "cold"])
    R["u-flash2"] = single({"id": "FLASH2", "type": "flash", "spec": {"T_K": K(45), "P_kPa": 1698}}, [("7", "in")], ["vapour", "liquid"])
    R["u-cp3"] = single({"id": "CP3", "type": "compressor", "spec": {"P_kPa": 7000}}, [("8", "in")], ["out"])
    R["u-he3"] = single({"id": "HE3", "type": "heater", "spec": {"T_K": K(111)}}, [("9", "in")], ["out"])
    R["u-cph2"] = single({"id": "CPH2", "type": "compressor", "spec": {"P_kPa": 7000}}, [("11-H2", "in")], ["out"])
    R["u-mixer2"] = single({"id": "MIXER2", "type": "mixer", "spec": {}}, [("10", "in"), ("12", "in"), ("36-REC", "in")], ["out"])
    R["u-he4"] = single({"id": "HE4", "type": "hx", "spec": {"T_cold_out_K": K(237.5)}}, [("19", "hot"), ("13", "cold")], ["hot", "cold"])
    for U in (300, 150, 1000):
        R[f"u-reactor-U{U}"] = single({"id": "REACTOR1", "type": "pfr", "spec": reactor_spec(U)}, [("15", "in")], ["out"], rx=reactions())
    R["u-reactor-isothermal"] = single({"id": "REACTOR1", "type": "pfr", "spec": {**{k: v for k, v in reactor_spec().items() if k != "coolant"}, "T_K": K(247.9)}},
                                       [("15", "in")], ["out"], rx=reactions())
    R["u-he5"] = single({"id": "HE5", "type": "hx", "spec": {"T_hot_out_K": K(62)}}, [("20", "hot"), ("28", "cold")], ["hot", "cold"])
    R["u-he5-cold82.9"] = single({"id": "HE5", "type": "hx", "spec": {"T_cold_out_K": K(82.9)}}, [("20", "hot"), ("28", "cold")], ["hot", "cold"])
    R["u-he5-dTmin2"] = single({"id": "HE5", "type": "hx", "spec": {"dTmin_K": 2}}, [("20", "hot"), ("28", "cold")], ["hot", "cold"])
    R["u-he5-dTmin2-zones10"] = single({"id": "HE5", "type": "hx", "spec": {"dTmin_K": 2, "zones": 10}}, [("20", "hot"), ("28", "cold")], ["hot", "cold"])
    R["u-he6"] = single({"id": "HE6", "type": "hx", "spec": {"T_hot_out_K": K(56.9)}}, [("21", "hot"), ("26", "cold")], ["hot", "cold"])
    R["u-he7"] = single({"id": "HE7", "type": "heater", "spec": {"T_K": K(30)}}, [("22", "in")], ["out"])
    R["u-he7-duty24.2MW"] = single({"id": "HE7", "type": "heater", "spec": {"duty_kW": -24200}}, [("22", "in")], ["out"])
    R["u-he7-duty19.75MW"] = single({"id": "HE7", "type": "heater", "spec": {"duty_kW": -19750}}, [("22", "in")], ["out"])
    R["u-flash3"] = single({"id": "FLASH3", "type": "flash", "spec": {"T_K": K(30), "P_kPa": 6925}}, [("23", "in")], ["vapour", "liquid"])
    R["u-flash3-mhv1"] = single({"id": "FLASH3", "type": "flash", "spec": {"T_K": K(30), "P_kPa": 6925}}, [("23", "in")], ["vapour", "liquid"], thermo=THERMO_MHV1)
    R["u-cprec"] = single({"id": "CPREC", "type": "compressor", "spec": {"P_kPa": 7000}}, [("34", "in")], ["out"])
    R["u-valve1"] = single({"id": "VALVE1", "type": "valve", "spec": {"P_kPa": 100}}, [("24", "in")], ["out"])
    R["u-valve3"] = single({"id": "VALVE3", "type": "valve", "spec": {"P_kPa": 100}}, [("40", "in")], ["out"])
    R["u-valve2"] = single({"id": "VALVE2", "type": "valve", "spec": {"P_kPa": 100}}, [("42", "in")], ["out"])
    R["u-mixer4"] = single({"id": "MIXER4", "type": "mixer", "spec": {}}, [("25", "in"), ("41", "in"), ("43", "in")], ["out"])
    R["u-flash4"] = single({"id": "FLASH4", "type": "flash", "spec": {"T_K": K(30), "P_kPa": 100}}, [("27", "in")], ["vapour", "liquid"])
    R["u-mixer5"] = single({"id": "MIXER5", "type": "mixer", "spec": {}}, [("38", "in"), ("32", "in")], ["out"])
    R["u-mixer1"] = single({"id": "MIXER1", "type": "mixer", "spec": {}}, [("1-CO2", "in"), ("39-REC", "in")], ["out"])
    return R


def column_runs():
    R = {}
    second = {"bottoms_kmol_h": 4581}
    for var, thermo in (("partial", THERMO_PR), ("total", THERMO_PR), ("partial", THERMO_MHV1), ("total", THERMO_MHV1)):
        tag = "pr" if thermo is THERMO_PR else "mhv1"
        R[f"u-column-{var}-{tag}"] = single({"id": "COLUMN", "type": "column", "spec": column_spec(var, dict(second))},
                                            [("29", "in")], ["distillate", "bottoms"], thermo=thermo)
    R["u-column-partial-side-pr"] = single({"id": "COLUMN", "type": "column", "spec": column_spec("partial-side", {"bottoms_kmol_h": 4581, "side_kmol_h": 4542})},
                                           [("29", "in")], ["distillate", "bottoms", "side"])
    return R


# ---------------------------------------------------------------------------------------------------------------
# The plant, as one flowsheet. Sections are the same flowsheet cut at paper streams (feeds) and products.
def plant_blocks(column_variant="partial", thermo=None, column_second=None, U=300.0, eff=None, bypass=True):
    """Blocks and streams of the whole one-step plant (without the fired heater and the steam cycle)."""
    e = {} if eff is None else {"efficiency": eff}
    col2 = column_second or {"reflux_ratio": 2, "boilup_ratio": 1.17155}
    B = [
        feed("F-CO2", "1-CO2"), feed("F-H2", "11-H2"),
        {"id": "MIXER1", "type": "mixer", "spec": {}},
        {"id": "CP1", "type": "compressor", "spec": {"P_kPa": 412, **e}},
        {"id": "HE1", "type": "heater", "spec": {"T_K": K(30)}},
        {"id": "FLASH1", "type": "flash", "spec": {"T_K": K(30), "P_kPa": 412}},
        {"id": "CP2", "type": "compressor", "spec": {"P_kPa": 1698, **e}},
        {"id": "HE2", "type": "hx", "spec": {"T_hot_out_K": K(45)}},
        {"id": "FLASH2", "type": "flash", "spec": {"T_K": K(45), "P_kPa": 1698}},
        {"id": "CP3", "type": "compressor", "spec": {"P_kPa": 7000, **e}},
        {"id": "HE3", "type": "heater", "spec": {"T_K": K(111)}},
        {"id": "CPH2", "type": "compressor", "spec": {"P_kPa": 7000, **e}},
        {"id": "MIXER2", "type": "mixer", "spec": {}},
        {"id": "HE4", "type": "hx", "spec": {"T_cold_out_K": K(237.5)}},
        {"id": "SPLIT1", "type": "splitter", "spec": {"fractions": [0.5, 0.5]}},
        {"id": "REACTOR1", "type": "pfr", "spec": reactor_spec(U)},
        {"id": "REACTOR2", "type": "pfr", "spec": reactor_spec(U)},
        {"id": "MIXER3", "type": "mixer", "spec": {}},
        {"id": "HE5", "type": "hx", "spec": {"dTmin_K": 2, "zones": 10}},
        {"id": "HE6", "type": "hx", "spec": {"T_cold_out_K": K(30)}},
        {"id": "HE7", "type": "heater", "spec": {"T_K": K(30)}},
        {"id": "FLASH3", "type": "flash", "spec": {"T_K": K(30), "P_kPa": 6925}},
        {"id": "SPLIT2", "type": "splitter", "spec": {"fractions": [0.02, 0.98]}},
        {"id": "CPREC", "type": "compressor", "spec": {"P_kPa": 7000, **e}},
        {"id": "VALVE1", "type": "valve", "spec": {"P_kPa": 100}},
        {"id": "VALVE2", "type": "valve", "spec": {"P_kPa": 100}},
        {"id": "VALVE3", "type": "valve", "spec": {"P_kPa": 100}},
        {"id": "MIXER4", "type": "mixer", "spec": {}},
        {"id": "FLASH4", "type": "flash", "spec": {"T_K": K(30), "P_kPa": 100}},
        {"id": "SPLIT3", "type": "splitter", "spec": {"fractions": [0.02, 0.98]}},
        {"id": "COLUMN", "type": "column", "spec": column_spec(column_variant, dict(col2))},
        {"id": "MIXER5", "type": "mixer", "spec": {}},
        prod("P-44-PURGE"), prod("P-45-PURGE"), prod("P-30-WATER"), prod("P-31-MEOH"),
    ]
    S = [
        st("1-CO2", "F-CO2.out", "MIXER1.in"),
        st("2", "MIXER1.out", "CP1.in"), st("3", "CP1.out", "HE1.in"), st("4", "HE1.out", "FLASH1.in"),
        st("5", "FLASH1.vapour", "CP2.in"), st("40", "FLASH1.liquid", "VALVE3.in"),
        st("6", "CP2.out", "HE2.hot"), st("7", "HE2.hot", "FLASH2.in"),
        st("8", "FLASH2.vapour", "CP3.in"), st("42", "FLASH2.liquid", "VALVE2.in"),
        st("9", "CP3.out", "HE3.in"), st("10", "HE3.out", "MIXER2.in"),
        st("11-H2", "F-H2.out", "CPH2.in"), st("12", "CPH2.out", "MIXER2.in"),
        st("13", "MIXER2.out", "HE4.cold"), st("14", "HE4.cold", "SPLIT1.in"),
        st("15", "SPLIT1.out", "REACTOR1.in"), st("17", "SPLIT1.out", "REACTOR2.in"),
        st("16", "REACTOR1.out", "MIXER3.in"), st("18", "REACTOR2.out", "MIXER3.in"),
        st("19", "MIXER3.out", "HE4.hot", tear=True, guess=guess("19")), st("20", "HE4.hot", "HE5.hot"), st("21", "HE5.hot", "HE6.hot"),
        st("22", "HE6.hot", "HE7.in"), st("23", "HE7.out", "FLASH3.in"),
        st("33", "FLASH3.vapour", "SPLIT2.in"), st("24", "FLASH3.liquid", "VALVE1.in"),
        st("44-PURGE", "SPLIT2.out", "P-44-PURGE.in"), st("34", "SPLIT2.out", "CPREC.in"),
        st("35", "CPREC.out", "HE2.cold", tear=True, guess=guess("35")), st("36-REC", "HE2.cold", "MIXER2.in"),
        st("25", "VALVE1.out", "MIXER4.in"), st("41", "VALVE3.out", "MIXER4.in"), st("43", "VALVE2.out", "MIXER4.in"),
        st("26", "MIXER4.out", "HE6.cold", tear=True, guess=guess("26")), st("27", "HE6.cold", "FLASH4.in"),
        st("37", "FLASH4.vapour", "SPLIT3.in"), st("28", "FLASH4.liquid", "HE5.cold", tear=True, guess=guess("28")),
        st("45-PURGE", "SPLIT3.out", "P-45-PURGE.in"), st("38", "SPLIT3.out", "MIXER5.in"),
        st("39-REC", "MIXER5.out", "MIXER1.in", tear=True, guess=guess("39-REC")),
        st("30-WATER", "COLUMN.bottoms", "P-30-WATER.in"),
    ]
    # The column: the paper's partial vapour-liquid condenser at 53 C is CHEPTA's condenser (total, or partial with all
    # the distillate as vapour) followed by a flash at 53 C and 100 kPa, whose vapour is 32 and liquid 31-MEOH (assumed).
    # bypass: H2, CO and N2 (8 ppm to 20 ppm of stream 29) go round the column to the top flash, because CHEPTA's column
    # cannot start with them (runs diag-feed29-*, capability request); the paper sends 98.6-99.9 % of each to stream 32
    # (supplement Table S2).
    if bypass:
        B += [{"id": "TRACES", "type": "separator", "spec": {"fractions": {c: ([1, 0] if c in ("hydrogen", "carbon-monoxide", "nitrogen") else [0, 1]) for c in COMPONENTS}}},
              {"id": "MIX-TOP", "type": "mixer", "spec": {}}]
        S += [st("29", "HE5.cold", "TRACES.in"), st("29-gas", "TRACES.out", "MIX-TOP.in"), st("29-col", "TRACES.out", "COLUMN.in"),
              st("D", "COLUMN.distillate", "MIX-TOP.in"), st("D2", "MIX-TOP.out", "FLASH-COND.in")]
    else:
        S += [st("29", "HE5.cold", "COLUMN.in"), st("D", "COLUMN.distillate", "FLASH-COND.in")]
    B += [{"id": "FLASH-COND", "type": "flash", "spec": {"T_K": K(53), "P_kPa": 100}}]
    S += [st("32", "FLASH-COND.vapour", "MIXER5.in"), st("31-MEOH", "FLASH-COND.liquid", "P-31-MEOH.in")]
    return B, S


def plant(column_variant="partial", thermo=None, solver=None, **kw):
    B, S = plant_blocks(column_variant, thermo, **kw)
    return req(doc(B, S, thermo=thermo, reactions=reactions(), solver=solver))


def section(keep, column_variant="partial", thermo=None, solver=None, drop_tears=(), **kw):
    """The plant cut to the blocks in `keep`: a stream into a kept block from outside becomes a feed with the paper's
    values; a stream from a kept block to outside goes to a product."""
    B, S = plant_blocks(column_variant, thermo, **kw)
    blocks = [b for b in B if b["id"] in keep]
    streams = []
    for s in S:
        a, b = s["from"].split(".")[0], s["to"].split(".")[0]
        if a in keep and b in keep:
            s = dict(s)
            if s["id"] in drop_tears:
                s.pop("tear", None)
            streams.append(s)
        elif b in keep and a not in keep:
            blocks.append(feed(f"F-{s['id']}", s["id"]))
            streams.append(st(s["id"], f"F-{s['id']}.out", s["to"]))
        elif a in keep and b not in keep:
            blocks.append(prod(f"P-{s['id']}"))
            streams.append(st(s["id"], s["from"], f"P-{s['id']}.in"))
    return req(doc(blocks, streams, thermo=thermo, reactions=reactions(), solver=solver))


SEC_COMPRESSION = {"F-CO2", "MIXER1", "CP1", "HE1", "FLASH1", "CP2", "HE2", "FLASH2", "CP3", "HE3"}
SEC_LOOP = {"F-H2", "CPH2", "MIXER2", "HE4", "SPLIT1", "REACTOR1", "REACTOR2", "MIXER3", "HE5", "HE6", "HE7", "FLASH3",
            "SPLIT2", "CPREC", "HE2", "P-44-PURGE"}
SEC_PURIFICATION = {"VALVE1", "VALVE2", "VALVE3", "MIXER4", "HE6", "FLASH4", "SPLIT3", "HE5", "COLUMN", "FLASH-COND",
                    "MIXER5", "P-45-PURGE", "P-30-WATER", "P-31-MEOH", "TRACES", "MIX-TOP"}
SEC_COLUMN = {"TRACES", "COLUMN", "MIX-TOP", "FLASH-COND", "P-30-WATER", "P-31-MEOH"}


def section_runs():
    R = {}
    R["u-column-partial-flash53"] = section(SEC_COLUMN, column_second={"reflux_ratio": 2, "bottoms_kmol_h": 4581})
    R["u-column-total-flash53"] = section(SEC_COLUMN, column_variant="total", column_second={"reflux_ratio": 2, "bottoms_kmol_h": 4581})
    R["sec-compression"] = section(SEC_COMPRESSION)
    R["sec-loop"] = section(SEC_LOOP)
    R["diag-column-recovery-0.99987"] = section(SEC_COLUMN, column_second={"reflux_ratio": 2, "specifications": [{"kind": "recovery", "product": "bottoms", "component": "water", "value": 0.99987}]})
    R["u-column-partial-flash53-purity"] = section(SEC_COLUMN, column_second={"reflux_ratio": 2, "specifications": [{"kind": "purity", "product": "bottoms", "component": "water", "value": 0.99985, "basis": "mole"}]})
    R["sec-loop-it200"] = section(SEC_LOOP, solver={"maxIterations": 200, "tolerance": 1e-7})
    R["sec-loop-direct"] = section(SEC_LOOP, solver={"method": "direct", "maxIterations": 300})
    R["sec-loop-wegstein"] = section(SEC_LOOP, solver={"method": "wegstein", "maxIterations": 300})
    R["sec-purification"] = section(SEC_PURIFICATION, column_second={"reflux_ratio": 2, "bottoms_kmol_h": 4581}, drop_tears=("26", "28"))
    return R


def plant_runs():
    R = {}
    R["plant-a5"] = plant(solver={"maxIterations": 200, "tolerance": 1e-7})
    R["plant-a6"] = plant(solver={"maxIterations": 200, "tolerance": 1e-7}, column_second={"reflux_ratio": 2, "bottoms_kmol_h": 4581})
    return R


def with_components(r, comps):
    """The same request with only these components (the others' flows dropped from every feed)."""
    r = copy.deepcopy(r)
    fsd = r["input"]["flowsheet"]
    fsd["components"] = comps
    for b in fsd["blocks"]:
        if b["type"] == "feed":
            b["spec"]["flow_kmol_h"] = {k: v for k, v in b["spec"]["flow_kmol_h"].items() if k in comps}
    return r


def diag_runs():
    R = {}
    col = column_runs()["u-column-total-pr"]
    R["diag-feed29-bubble"] = single({"id": "B", "type": "flash", "spec": {"VF": 0, "P_kPa": 100}}, [("29", "in")], ["vapour", "liquid"])
    R["diag-feed29-flash"] = single({"id": "B", "type": "flash", "spec": {"T_K": K(82.9), "P_kPa": 100}}, [("29", "in")], ["vapour", "liquid"])
    R["diag-column-total-no-H2"] = with_components(col, [c for c in COMPONENTS if c != "hydrogen"])
    R["diag-column-total-CO2-MeOH-H2O"] = with_components(col, ["carbon-dioxide", "methanol", "water"])
    R["diag-column-total-MeOH-H2O"] = with_components(col, ["methanol", "water"])
    bub = R["diag-feed29-bubble"]
    R["diag-feed29-bubble-plus-CO"] = with_components(bub, ["carbon-dioxide", "carbon-monoxide", "methanol", "water"])
    R["diag-feed29-bubble-plus-N2"] = with_components(bub, ["carbon-dioxide", "methanol", "water", "nitrogen"])
    R["diag-feed29-bubble-CO2-MeOH-H2O"] = with_components(bub, ["carbon-dioxide", "methanol", "water"])
    # the smallest input that shows the fault: methanol and water with 10 ppm CO, a bubble point at 100 kPa
    mini = {"components": ["carbon-monoxide", "methanol", "water"], "thermo": {"model": "PR"},
            "blocks": [{"id": "F1", "type": "feed", "spec": {"flow_kmol_h": {"methanol": 50, "water": 50, "carbon-monoxide": 0.001}, "T_K": 330, "P_kPa": 100}},
                       {"id": "B1", "type": "flash", "spec": {"VF": 0, "P_kPa": 100}}, prod("P1"), prod("P2")],
            "streams": [st("S1", "F1.out", "B1.in"), st("S2", "B1.vapour", "P1.in"), st("S3", "B1.liquid", "P2.in")]}
    R["mini-bubble-CO-10ppm"] = req(mini)
    ps = single({"id": "COLUMN", "type": "column", "spec": {"mode": "rigorous", "stages": 30, "feed_stage": 24, "P_kPa": 100,
                 "condenser": "partial", "side_draws": [{"stage": 2, "phase": "liquid", "flow_kmol_h": 4542}], "bottoms_kmol_h": 4581,
                 "specifications": [{"kind": "stage_temperature", "stage": 1, "T_K": K(53)}]}},
                [("29", "in")], ["distillate", "bottoms", "side"])
    R["diag-column-partialside-T53-full"] = ps
    psr = copy.deepcopy(ps)
    cs = psr["input"]["flowsheet"]["blocks"][1]["spec"]
    cs.pop("specifications"); cs["reflux_ratio"] = 49.15   # L1 = 2 x (289 + 4542) + 4542 = 14204 kmol/h over 289 (derived)
    R["diag-column-partialside-R49-full"] = psr
    R["diag-column-partialside-R49-CO2-MeOH-H2O"] = with_components(psr, ["carbon-dioxide", "methanol", "water"])
    psm = copy.deepcopy(psr); psm["input"]["flowsheet"]["blocks"][1]["spec"]["max_iterations"] = 100
    R["diag-column-partialside-R49-full-maxit100"] = psm
    R["diag-column-partialside-T53-CO2-MeOH-H2O"] = with_components(ps, ["carbon-dioxide", "methanol", "water"])
    m100 = with_components(ps, ["carbon-dioxide", "methanol", "water"])
    m100["input"]["flowsheet"]["blocks"][1]["spec"]["max_iterations"] = 100
    R["diag-column-partialside-T53-CO2-MeOH-H2O-maxit100"] = m100
    m5 = copy.deepcopy(m100); m5["input"]["flowsheet"]["blocks"][1]["spec"]["max_iterations"] = 5
    R["diag-column-partialside-T53-CO2-MeOH-H2O-maxit5"] = m5
    R["diag-column-partialside-T53-plus-CO"] = with_components(ps, ["carbon-dioxide", "carbon-monoxide", "methanol", "water"])
    R["diag-column-partialside-T53-plus-N2"] = with_components(ps, ["carbon-dioxide", "methanol", "water", "nitrogen"])
    m2 = copy.deepcopy(mini); m2["blocks"][0]["spec"]["flow_kmol_h"]["carbon-monoxide"] = 0.1
    R["mini-bubble-CO-1000ppm"] = req(m2)
    m3 = copy.deepcopy(mini); m3["blocks"][1]["spec"] = {"T_K": 340, "P_kPa": 100}
    R["mini-flash-TP-CO-10ppm"] = req(m3)
    return R


def extra_runs():
    return diag_runs()
