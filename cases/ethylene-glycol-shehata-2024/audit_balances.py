#!/usr/bin/env python3
"""Audit the paper's own balances: Shehata et al. 2024, direct hydration plant (Table 3, Fig. 5, Table 8).

Reads streams.json and equipment.json from this folder, writes balance-results.json and STREAM_AUDIT.md.
No third-party packages, no CHEPTA. Residuals are outlet minus inlet. A residual is "within rounding" when it is
no larger than the sum of the rounding bounds of the printed digits of every flow and mole fraction involved.
Nothing in the paper is corrected; disagreements are listed.
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = json.loads((HERE / "streams.json").read_text())
E = json.loads((HERE / "equipment.json").read_text())
ST = {s["stream"]: s for s in S["streams"]}
C = ["oxygen", "ethylene", "water", "ethylene_oxide", "carbon_dioxide", "MEG", "DEG", "TEG"]

# Molar masses from IUPAC conventional atomic weights (C 12.011, H 1.008, O 15.999; IUPAC 2021 table, abridged).
AW = {"C": 12.011, "H": 1.008, "O": 15.999}
FORMULA = {"oxygen": {"O": 2}, "ethylene": {"C": 2, "H": 4}, "water": {"H": 2, "O": 1},
           "ethylene_oxide": {"C": 2, "H": 4, "O": 1}, "carbon_dioxide": {"C": 1, "O": 2},
           "MEG": {"C": 2, "H": 6, "O": 2}, "DEG": {"C": 4, "H": 10, "O": 3}, "TEG": {"C": 6, "H": 14, "O": 4}}
MW = {c: sum(AW[a] * n for a, n in f.items()) for c, f in FORMULA.items()}


def half_unit(printed):
    """Half of the last printed significant place, e.g. '1.10e+004' -> 50, '9870' -> 0.5, '0.0155' -> 0.00005."""
    p = printed.replace(",", "").replace("*", "").lower()
    mant, _, exp = p.partition("e")
    exp = int(exp) if exp else 0
    decimals = len(mant.split(".")[1]) if "." in mant else 0
    return 0.5 * 10 ** (exp - decimals)


def half_unit_fraction(printed):
    """Mole fractions are printed to 4 decimals; '0.0' and '1.0' are read as exact to that precision too."""
    return min(half_unit(printed), 0.00005)


def flows(name):
    s = ST[name]
    F = s["molar_kmol_h"]
    dF = half_unit(s["molar_as_printed"])
    out = {}
    for c in C:
        x = s["mole_fraction"][c]
        dx = half_unit_fraction(s["mole_fraction_as_printed"][c])
        out[c] = (F * x, abs(x) * dF + F * dx + dF * dx)
    return out


def total(name):
    s = ST[name]
    return s["molar_kmol_h"], half_unit(s["molar_as_printed"])


def combine(names, sign=1):
    res = {c: [0.0, 0.0] for c in C}
    for n in names:
        for c, (v, d) in flows(n).items():
            res[c][0] += sign * v
            res[c][1] += d
    return res


def r(v, n=4):
    return None if v is None else round(v, n)


results = {"source": S["locator"], "molar_masses_g_mol": {c: r(v) for c, v in MW.items()}, "blocks": [],
           "stream_sums": [], "mass_checks": [], "derived_vs_text": [], "energy": {}, "inconsistencies": []}

# 1. Mole-fraction sums
for s in S["streams"]:
    if not s["in_table_3"]:
        continue
    tot = sum(s["mole_fraction"].values())
    tol = sum(half_unit_fraction(v) for v in s["mole_fraction_as_printed"].values())
    results["stream_sums"].append({"stream": s["stream"], "sum": r(tot, 5), "tolerance": r(tol, 5),
                                   "within_rounding": abs(tot - 1) <= tol})

# 2. Mass flow from moles: hours per year implied by each stream
for s in S["streams"]:
    if not s["in_table_3"] or not s["molar_kmol_h"]:
        continue
    kg_h = sum(s["molar_kmol_h"] * s["mole_fraction"][c] * MW[c] for c in C)
    hours = s["mass_t_yr"] * 1000 / kg_h
    results["mass_checks"].append({"stream": s["stream"], "kg_h_from_moles": r(kg_h, 1), "t_yr_printed": s["mass_t_yr"],
                                   "implied_hours_per_year": r(hours, 1), "deviation_from_8760_h_pct": r((hours / 8760 - 1) * 100, 2)})


def block(name, ins, outs, reaction=None, note=None):
    a = combine(outs)
    b = combine(ins)
    row = {"block": name, "in": ins, "out": outs, "components": {}, "note": note}
    worst = 0.0
    ok = True
    for c in C:
        res = a[c][0] - b[c][0]
        if reaction:
            res -= reaction.get(c, 0.0)
        tol = a[c][1] + b[c][1]
        row["components"][c] = {"residual_kmol_h": r(res), "tolerance_kmol_h": r(tol), "within_rounding": abs(res) <= tol}
        ok &= abs(res) <= tol
    tin = sum(total(n)[0] for n in ins)
    tout = sum(total(n)[0] for n in outs)
    ttol = sum(total(n)[1] for n in ins + outs)
    gen = sum(reaction.values()) if reaction else 0.0
    row["total"] = {"in": r(tin, 3), "out": r(tout, 3), "net_generation": r(gen, 3), "residual": r(tout - tin - gen, 3),
                    "tolerance": r(ttol, 3), "within_rounding": abs(tout - tin - gen) <= ttol}
    row["all_within_rounding"] = ok and row["total"]["within_rounding"]
    if reaction:
        for atom in "CHO":
            ain = sum(flows(n)[c][0] * FORMULA[c].get(atom, 0) for n in ins for c in C)
            aout = sum(flows(n)[c][0] * FORMULA[c].get(atom, 0) for n in outs for c in C)
            atol = sum(flows(n)[c][1] * FORMULA[c].get(atom, 0) for n in ins + outs for c in C)
            row[f"atom_{atom}"] = {"residual_kmol_h": r(aout - ain), "tolerance": r(atol), "within_rounding": abs(aout - ain) <= atol}
    results["blocks"].append(row)
    return row


# 3. Reactor: inlet = MIX-102 + MIX-100 (streams Water FEED, 2, 22, 3 not in Table 3), outlet 4 + 10.
f4 = flows("4"); fin = combine(["WATER MKUP", "11", "Ethylene Oxid"])
ext_teg = f4["TEG"][0] - fin["TEG"][0]
ext_deg = f4["DEG"][0] - fin["DEG"][0] + ext_teg
ext_meg = f4["MEG"][0] - fin["MEG"][0] + ext_deg
reaction = {"ethylene_oxide": -(ext_meg + ext_deg + ext_teg), "water": -ext_meg, "MEG": ext_meg - ext_deg,
            "DEG": ext_deg - ext_teg, "TEG": ext_teg}
rx = block("Hydration Reactor with MIX-102, MIX-100, E-105 cold side, E-100", ["WATER MKUP", "11", "Ethylene Oxid"], ["4", "10"],
           reaction=reaction, note="Extents of Eqs. 5-7 fitted from the glycols of stream 4; EO and water then check the fit.")
rx["extents_kmol_h"] = {"Eq5_MEG": r(ext_meg, 2), "Eq6_DEG": r(ext_deg, 2), "Eq7_TEG": r(ext_teg, 2)}
eo_in = fin["ethylene_oxide"][0]
eo_conv = ext_meg + ext_deg + ext_teg

# 4. Evaporator train and dehydration column: vapours by difference (not printed)
vap = {}
for name, feed, liq in (("EVA_1 (via VLV-100)", "4", "5"), ("EVA_2 (via VLV-101)", "5", "6"), ("EVA_3 (via VLV-102)", "6", "1"),
                        ("Dehydration Tower", "1", "MEG Column FEED")):
    a, b = flows(feed), flows(liq)
    v = {c: a[c][0] - b[c][0] for c in C}
    tol = {c: a[c][1] + b[c][1] for c in C}
    tot = total(feed)[0] - total(liq)[0]
    vap[name] = v
    neg = [c for c in C if v[c] < -tol[c]]
    results["blocks"].append({"block": name, "in": [feed], "out": [liq, "top product by difference (not printed)"],
                              "top_by_difference_kmol_h": {c: r(v[c], 2) for c in C if abs(v[c]) > 1e-9},
                              "top_total_kmol_h": r(tot, 1), "tolerance_kmol_h": {c: r(tol[c], 2) for c in C if tol[c] > 0.01},
                              "negative_beyond_rounding": neg, "all_within_rounding": not neg,
                              "note": "Outlet top stream not in Table 3: computed as feed minus liquid; only a negative flow beyond rounding would be an inconsistency."})

# 5. Water loop: sum of tops (17, 20, 19, Water Rec 5) + 10 against WATER REC
tops = {c: sum(v[c] for v in vap.values()) for c in C}
wr = flows("WATER REC"); f10 = flows("10")
tol = {c: wr[c][1] + flows("4")[c][1] + flows("MEG Column FEED")[c][1] + f10[c][1] for c in C}
row = {"block": "MIX-101 (with the four tops by difference)", "in": ["10", "17", "20", "19", "Water Rec 5"], "out": ["WATER REC"], "components": {}}
okall = True
for c in C:
    res = wr[c][0] - tops[c] - f10[c][0]
    row["components"][c] = {"residual_kmol_h": r(res), "tolerance_kmol_h": r(tol[c]), "within_rounding": abs(res) <= tol[c]}
    okall &= abs(res) <= tol[c]
row["all_within_rounding"] = okall
row["note"] = "Equivalent to stream 4 minus MEG Column FEED against WATER REC."
results["blocks"].append(row)

block("E-101 + P-100 + RCY-1 (WATER REC -> 11)", ["WATER REC"], ["11"], note="Recycle tear: HYSYS's RCY-1 inlet (13) and outlet (11).")
block("Purification Tower", ["MEG Column FEED"], ["DEG+TEG", "MEG"])
block("P-101 (MEG -> 21)", ["MEG"], ["21"])
block("E-105 hot side (21 -> MEG To Storage)", ["21"], ["MEG To Storage"])

# 6. Plant: reactions over the whole boundary
fin = combine(["WATER MKUP", "Ethylene Oxid"]); fout = combine(["MEG To Storage", "DEG+TEG", "10"])
pt = fout["TEG"][0]; pd = fout["DEG"][0] + pt; pm = fout["MEG"][0] + pd
plant = block("Plant (WATER MKUP, Ethylene Oxid -> MEG To Storage, DEG+TEG)", ["WATER MKUP", "Ethylene Oxid"], ["MEG To Storage", "DEG+TEG", "10"],
              reaction={"ethylene_oxide": -(pm + pd + pt), "water": -pm, "MEG": pm - pd, "DEG": pd - pt, "TEG": pt},
              note="Extents fitted from the glycols leaving; EO and water then check them.")
mass_in = sum(ST[n]["mass_t_yr"] for n in ("WATER MKUP", "Ethylene Oxid"))
mass_out = sum(ST[n]["mass_t_yr"] for n in ("MEG To Storage", "DEG+TEG", "10"))
plant["mass_t_yr"] = {"in": mass_in, "out": mass_out, "residual": r(mass_out - mass_in, 1), "residual_pct": r((mass_out / mass_in - 1) * 100, 3)}

# 7. Derived quantities against the text
w4 = flows("4")["water"][0]; w1 = flows("1")["water"][0]
w_feed = flows("WATER MKUP")["water"][0] + flows("11")["water"][0]
eo_feed = flows("Ethylene Oxid")["ethylene_oxide"][0] + flows("11")["ethylene_oxide"][0]
glycols = ext_meg - ext_deg + ext_deg - ext_teg + ext_teg
L, D = 77.8, 0.55
meg_t = ST["MEG To Storage"]["mass_t_yr"]; heavy_t = ST["DEG+TEG"]["mass_t_yr"]
derived = [
    ("water removed in the three evaporators, share of the water in stream 4", (w4 - w1) / w4 * 100, "%", "about 75 % (p.8)"),
    ("water to EO at the reactor inlet, all water / all EO (11 + WATER MKUP + Ethylene Oxid)", w_feed / eo_feed, "mol/mol", "10:1 (pp.5, 8)"),
    ("recycled water (11) / fresh EO", flows("11")["water"][0] / flows("Ethylene Oxid")["ethylene_oxide"][0], "mol/mol", "10:1 cycle water to EO (p.8)"),
    ("all water / fresh EO", w_feed / flows("Ethylene Oxid")["ethylene_oxide"][0], "mol/mol", "10:1 (p.8)"),
    ("EO conversion per pass", eo_conv / eo_in * 100, "%", "not printed"),
    ("MEG share of the glycols formed (molar)", (ext_meg - ext_deg) / glycols * 100, "%", "85 % (Table 1, p.3)"),
    ("share of converted EO that became MEG", (ext_meg - ext_deg) / eo_conv * 100, "%", "85 % MEG, 15 % DEG + TEG (Table 1, p.3)"),
    ("reactor volume from 77.8 m x 0.55 m", math.pi / 4 * D ** 2 * L, "m3", "not printed; residence time 3 min (p.8) needs the liquid density at 199 C, left to the CHEPTA run"),
    ("DEG + TEG mass share of the glycol products", heavy_t / (meg_t + heavy_t) * 100, "wt %", "3.56 wt % (p.14)"),
    ("dehydration column vacuum in the text, converted", 85 * 0.133322, "kPa", "Table 1: 15 kPa condenser, 20 kPa reboiler (p.3)"),
    ("MEG product", meg_t, "t/yr", "600,000 t/yr (p.2)"),
]
for name, v, unit, text in derived:
    results["derived_vs_text"].append({"quantity": name, "derived": r(v, 3), "unit": unit, "paper_says": text})

# 8. Energy (Table 8) against the text
en = {e["name"]: e["value_kW"] for e in E["energy_streams"]["streams"]}
evap = en["Q1"] + en["Q2"] + en["Q3"]
watsep = evap + en["DEH CON Q"] + en["DEH REQ Q"]
pos = sum(v for v in en.values() if v > 0)
absum = sum(abs(v) for v in en.values())
results["energy"] = {
    "evaporators_Q1_Q2_Q3_kW": r(evap, 2), "text_evaporators_MW": 17.8,
    "water_separation_Q1_Q2_Q3_DEHCON_DEHREQ_kW": r(watsep, 2), "text_water_separation_MW": 219.258,
    "glycol_column_reboiler_condenser_kW": [en["MEG Q"], en["MEG CON Q"]], "text_MW": [20.87, 21.51],
    "sum_of_positive_entries_kW": r(pos, 2), "sum_of_absolute_entries_kW": r(absum, 2), "text_total_MW": 323,
    "feed_heater_table_8_kW": en["Feed Heater Duty"], "feed_heater_text_MW": 4.446,
    "effect_condensers_vs_next_evaporator_kW": {"First Effect vs Q2": [en["First Effect"], en["Q2"]], "Second Effect vs Q3": [en["Second Effect"], en["Q3"]]},
    "reactor_Q-100_kW": en["Q-100"],
}

# 9. Temperatures against the 170 C limit (p.8)
results["temperature_limit"] = [{"stream": n, "T_C": ST[n]["T_C"], "above_170_C": ST[n]["T_C"] > 170}
                                for n in ("MEG Column FEED", "MEG", "DEG+TEG")]

(HERE / "balance-results.json").write_text(json.dumps(results, indent=1) + "\n")

# Markdown
L = ["# Stream table audit (Shehata et al. 2024, direct hydration of ethylene oxide)", "",
     "Generated by [audit_balances.py](audit_balances.py) from [streams.json](streams.json) (Table 3 and Fig. 5, p.10) and "
     "[equipment.json](equipment.json) (Fig. 5, Table 1 p.3, text p.8, Table 8 p.14). The paper's numbers are an Aspen HYSYS 11 "
     "simulation, not measurements. Residuals are outlet minus inlet (minus net generation by reaction) in kmol/h. "
     "'Within rounding' means within the sum of the rounding bounds of the printed digits; outside it is an inconsistency "
     "of the paper's own table, kept, not corrected. Molar masses from IUPAC conventional atomic weights (derived).", "",
     "## Blocks", "", "| Block | In | Out | Total residual (tolerance) | Component residual furthest from its tolerance | Within rounding |", "|---|---|---|---:|---|---|"]
for b in results["blocks"]:
    if "components" in b:
        worst = max(b["components"].items(), key=lambda kv: abs(kv[1]["residual_kmol_h"]) / max(kv[1]["tolerance_kmol_h"], 1e-9))
        tot = b.get("total")
        t = f"{tot['residual']:+.3f} ({tot['tolerance']:.3f})" if tot else "-"
        L.append(f"| {b['block']} | {', '.join(b['in'])} | {', '.join(b['out'])} | {t} | {worst[0]}: {worst[1]['residual_kmol_h']:+.4f} ({worst[1]['tolerance_kmol_h']:.4f}) | {'yes' if b['all_within_rounding'] else '**no**'} |")
    else:
        top = ", ".join(f"{c} {v:+.2f}" for c, v in b["top_by_difference_kmol_h"].items())
        L.append(f"| {b['block']} | {b['in'][0]} | {b['out'][0]} + top by difference: {b['top_total_kmol_h']} kmol/h ({top}) | - | negative beyond rounding: {', '.join(b['negative_beyond_rounding']) or 'none'} | {'yes' if b['all_within_rounding'] else '**no**'} |")
for b in results["blocks"]:
    for a in "CHO":
        if f"atom_{a}" in b:
            x = b[f"atom_{a}"]
            L.append(f"\n{b['block']}: atom {a} residual {x['residual_kmol_h']:+.3f} kmol/h (tolerance {x['tolerance']:.3f}), within rounding: {'yes' if x['within_rounding'] else 'no'}.")
    if "extents_kmol_h" in b:
        L.append(f"\nReaction extents fitted from stream 4 (kmol/h): {b['extents_kmol_h']}.")
    if "mass_t_yr" in b:
        m = b["mass_t_yr"]
        L.append(f"\nPlant mass: in {m['in']:.0f} t/yr, out {m['out']:.0f} t/yr, residual {m['residual']:+.0f} t/yr ({m['residual_pct']:+.3f} %).")
L += ["", "## Streams: sum of mole fractions", ""]
bad = [x for x in results["stream_sums"] if not x["within_rounding"]]
L.append(f"{len(results['stream_sums']) - len(bad)} of {len(results['stream_sums'])} sums are 1 within rounding." +
         ("" if not bad else " Not: " + "; ".join(f"{x['stream']} {x['sum']}" for x in bad) + "."))
L += ["", "## Mass flow from the moles: hours per year implied", "", "| Stream | kg/h from moles | t/yr printed | implied h/yr | vs 8760 h |", "|---|---:|---:|---:|---:|"]
for m in results["mass_checks"]:
    L.append(f"| {m['stream']} | {m['kg_h_from_moles']} | {m['t_yr_printed']:g} | {m['implied_hours_per_year']} | {m['deviation_from_8760_h_pct']:+.2f} % |")
L += ["", "## Derived from the table, against the paper's text", "", "| Quantity | Derived | Unit | Paper says |", "|---|---:|---|---|"]
for d in results["derived_vs_text"]:
    L.append(f"| {d['quantity']} | {d['derived']} | {d['unit']} | {d['paper_says']} |")
e = results["energy"]
L += ["", "## Energy (Table 8, p.14) against the text", "",
      f"- Evaporators Q1 + Q2 + Q3 = {e['evaporators_Q1_Q2_Q3_kW']:.0f} kW; text 17.8 MW (p.8).",
      f"- Water separation Q1 + Q2 + Q3 + DEH CON Q + DEH REQ Q = {e['water_separation_Q1_Q2_Q3_DEHCON_DEHREQ_kW']:.0f} kW; text 219.258 MW (p.14).",
      f"- Glycol column MEG Q / MEG CON Q = {e['glycol_column_reboiler_condenser_kW'][0]} / {e['glycol_column_reboiler_condenser_kW'][1]} kW; text 20.87 / 21.51 MW (p.14).",
      f"- Sum of the positive entries {e['sum_of_positive_entries_kW']:.0f} kW; of all absolute values {e['sum_of_absolute_entries_kW']:.0f} kW; text total 323 MW (p.14).",
      f"- Feed heater: Table 8 {e['feed_heater_table_8_kW']} kW; text 4.446 MW (p.8): a factor of 10.",
      f"- Condenser of each effect against the next evaporator's heat input: First Effect {e['effect_condensers_vs_next_evaporator_kW']['First Effect vs Q2'][0]} kW vs Q2 {e['effect_condensers_vs_next_evaporator_kW']['First Effect vs Q2'][1]} kW; Second Effect {e['effect_condensers_vs_next_evaporator_kW']['Second Effect vs Q3'][0]} kW vs Q3 {e['effect_condensers_vs_next_evaporator_kW']['Second Effect vs Q3'][1]} kW. The HYSYS model keeps them as separate energy streams; the text says the vapour of each effect heats the next (p.8).",
      f"- Reactor Q-100 = {e['reactor_Q-100_kW']} kW (sign convention not stated); the text calls the reaction endothermic (p.8).", "",
      "## Temperatures against the 170 C limit (p.8)", ""]
for t in results["temperature_limit"]:
    L.append(f"- {t['stream']}: {t['T_C']} C{' (above 170 C)' if t['above_170_C'] else ''}")
(HERE / "STREAM_AUDIT.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
