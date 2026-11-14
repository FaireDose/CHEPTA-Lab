"""Audit the published one-step stream table of Lacerda de Oliveira Campos et al. (2022), without simulation.

Reads streams.json (supplement Tables S9-S10) and equipment.json (Figure S1, Tables S13-S14) and checks, per block:
total mass (t/h), total moles where no reaction, each component's moles (non-reactive blocks), atoms C, H, O, N
(reactors, burner, plant), and the energy balance from the printed molar enthalpies (sum n*H out - in, MW), compared
with the duties of Table S14; for two-stream exchangers the hot and cold sides must cancel. Nothing is corrected.
Run from the repository root: python cases/methanol-co2-campos-2022/audit_balances.py
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
src = json.loads((R / "streams.json").read_text())
eqdoc = json.loads((R / "equipment.json").read_text())
S = {s["stream"]: s for s in src["streams"]}
C = ["H2", "CO", "CO2", "CH3OH", "H2O", "N2", "O2"]
ATOMS = {"H2": (0, 2, 0, 0), "CO": (1, 0, 1, 0), "CO2": (1, 0, 2, 0), "CH3OH": (1, 4, 1, 0), "H2O": (0, 2, 1, 0),
         "N2": (0, 0, 0, 2), "O2": (0, 0, 2, 0)}
MW = {"H2": 2.016, "CO": 28.010, "CO2": 44.009, "CH3OH": 32.042, "H2O": 18.015, "N2": 28.014, "O2": 31.998}
DN, DX = 0.5, 0.0005  # printed: whole kmol/h; mole % with 3 decimals


def n(s): return S[s]["molar_kmol_h"]
def x(s, c): return S[s]["mol_pct"][c] / 100
def cf(s, c): return n(s) * x(s, c)
def cerr(s, c): return DN * x(s, c) + n(s) * DX / 100


def block(name, ins, outs, reactive, duty=None, pair=False):
    ss = ins + outs
    out = {"block": name, "inlets": ins, "outlets": outs}
    dm = sum(S[s]["mass_t_h"] for s in outs) - sum(S[s]["mass_t_h"] for s in ins)
    out["mass_residual_t_h"] = round(dm, 3)
    out["mass_bound_t_h"] = round(0.05 * len(ss), 3)
    res = {c: sum(cf(s, c) for s in outs) - sum(cf(s, c) for s in ins) for c in C}
    bnd = {c: sum(cerr(s, c) for s in ss) for c in C}
    atom = [sum(res[c] * ATOMS[c][a] for c in C) for a in range(4)]
    atom_b = [sum(bnd[c] * ATOMS[c][a] for c in C) for a in range(4)]
    out["atom_residual_kmol_h"] = dict(zip("CHON", (round(v, 2) for v in atom)))
    out["atom_bound_kmol_h"] = dict(zip("CHON", (round(v, 2) for v in atom_b)))
    ok = abs(dm) <= 0.05 * len(ss) + 1e-9 and all(abs(a) <= b + 1e-9 for a, b in zip(atom, atom_b))
    if not reactive:
        tot = sum(n(s) for s in outs) - sum(n(s) for s in ins)
        out["mole_residual_kmol_h"] = round(tot, 2)
        out["component_residual_kmol_h"] = {c: round(res[c], 2) for c in C}
        out["component_bound_kmol_h"] = {c: round(bnd[c], 2) for c in C}
        ok = ok and abs(tot) <= DN * len(ss) and all(abs(res[c]) <= bnd[c] + 1e-9 for c in C)
    else:
        out["generation_kmol_h"] = {c: round(res[c], 1) for c in C}
    out["within_rounding"] = ok
    dH = (sum(n(s) * S[s]["H_MJ_kmol"] for s in outs) - sum(n(s) * S[s]["H_MJ_kmol"] for s in ins)) / 3600
    out["enthalpy_change_MW"] = round(dH, 2)
    # rounding of n (+/-0.5 kmol/h) and H (+/-0.005 MJ/kmol) only
    out["enthalpy_bound_MW"] = round(sum(DN * abs(S[s]["H_MJ_kmol"]) + n(s) * 0.005 for s in ss) / 3600, 2)
    if duty is not None:
        out["table_S14_duty_MW"] = duty
    if pair:
        sides = []
        for i, o in zip(ins, outs):
            sides.append({"side": f"{i} -> {o}", "MW": round((n(o) * S[o]["H_MJ_kmol"] - n(i) * S[i]["H_MJ_kmol"]) / 3600, 2)})
        out["sides"] = sides
    return out


blocks = []
for e in eqdoc["equipment"]:
    d = e["specification"].get("duty_MW", {}).get("value")
    if e["id"] == "COLUMN":
        d = {"condenser": e["specification"]["condenser_duty_MW"]["value"], "reboiler": e["specification"]["reboiler_duty_MW"]["value"]}
    blocks.append(block(e["id"], e["inlets"], e["outlets"], e["type"] in ("pfr", "burner"), d, e["type"] == "hx"))
blocks.append(block("plant (1-CO2, 11-H2, 46-AIR -> 30-WATER, 31-MEOH, 49-FLUE)", ["1-CO2", "11-H2", "46-AIR"], ["30-WATER", "31-MEOH", "49-FLUE"], True))

streams = []
for s in S.values():
    tot = sum(s["mol_pct"].values())
    mass = n(s["stream"]) * sum(x(s["stream"], c) * MW[c] for c in C) / 1000
    streams.append({"stream": s["stream"], "sum_mol_pct": round(tot, 3), "sum_within": abs(tot - 100) <= 7 * 0.0005 + 1e-9,
                    "mass_from_composition_t_h": round(mass, 2), "mass_printed_t_h": s["mass_t_h"],
                    "mass_difference_pct": round(100 * (mass - s["mass_t_h"]) / s["mass_t_h"], 2)})

derived = {
    "purge_44_over_33": {"value": round(n("44-PURGE") / n("33"), 4), "paper": "2 % (Supplement p.10)"},
    "purge_45_over_37": {"value": round(n("45-PURGE") / n("37"), 4), "paper": "2 % (Supplement p.10)"},
    "split_15_over_14": {"value": round(n("15") / n("14"), 4), "paper": "not printed (two RPLUG blocks in parallel)"},
    "CO2_single_pass_conversion": {"value": round((cf("14", "CO2") - cf("19", "CO2")) / cf("14", "CO2"), 4), "paper": "28.5 % for the conventional process (article abstract, p.1)"},
    "methanol_product_t_h": {"value": S["31-MEOH"]["mass_t_h"], "paper": "methanol 99.67 mol % (Supplement p.11)"},
    "reboiler_minus_condenser_from_column_enthalpies_MW": {"value": None, "paper": "Table S14: 53.7 - 143.6 = -89.9"},
}
col = next(b for b in blocks if b["block"] == "COLUMN")
derived["reboiler_minus_condenser_from_column_enthalpies_MW"]["value"] = col["enthalpy_change_MW"]

report = {"method": "outlet minus inlet; printed values, nothing normalized",
          "rounding_model": "flows +/-0.5 kmol/h, mole % +/-0.0005, mass +/-0.05 t/h, H +/-0.005 MJ/kmol; bounds summed over the streams of a block",
          "molar_masses_g_mol": MW, "balances": blocks, "streams": streams, "derived": derived}
(R / "balance-results.json").write_text(json.dumps(report, indent=2) + "\n")

L = ["# Stream table audit (Lacerda de Oliveira Campos et al. 2022, one-step process)", "",
     "Generated by [audit_balances.py](audit_balances.py) from [streams.json](streams.json) (supplement Tables S9-S10) "
     "and [equipment.json](equipment.json) (Figure S1, Tables S13-S14). The numbers are an Aspen Plus simulation, not "
     "measurements. Residuals are outlet minus inlet. 'Within rounding' covers mass, moles, components (or atoms for "
     "reactors and the burner) at the printed digits. Enthalpy change = sum of n*H out minus in, from the printed "
     "molar enthalpies; for a heater it is the duty, for an exchanger the two sides should cancel, for a compressor "
     "it is the work, for an adiabatic block it should be zero.", "",
     "| Block | Mass residual t/h | Within rounding | Enthalpy change MW (bound) | Table S14 duty MW | Exchanger sides MW |",
     "|---|---:|---|---:|---|---|"]
for b in blocks:
    sides = "; ".join(f"{s['side']}: {s['MW']:+.2f}" for s in b.get("sides", []))
    L.append(f"| {b['block']} | {b['mass_residual_t_h']:+.2f} | {'yes' if b['within_rounding'] else '**no**'} | {b['enthalpy_change_MW']:+.2f} ({b['enthalpy_bound_MW']}) | {b.get('table_S14_duty_MW', '')} | {sides} |")
bad = [s for s in streams if not s["sum_within"]]
L += ["", "## Streams", "", ("All 61 mole-% sums are 100 within rounding." if not bad else "Mole-% sums off: " + ", ".join(f"{s['stream']} ({s['sum_mol_pct']})" for s in bad)),
      "", "Mass from composition (molar masses in balance-results.json) against the printed mass, largest differences:", ""]
for s in sorted(streams, key=lambda s: -abs(s["mass_difference_pct"]))[:5]:
    L.append(f"- {s['stream']}: {s['mass_from_composition_t_h']} vs {s['mass_printed_t_h']} t/h ({s['mass_difference_pct']:+.2f} %)")
L += ["", "## Derived from the tables, against the text", "", "| Quantity | From the tables | Paper says |", "|---|---:|---|"]
for k, v in derived.items():
    L.append(f"| {k} | {v['value']} | {v['paper']} |")
L.append("")
(R / "STREAM_AUDIT.md").write_text("\n".join(L))
print("\n".join(L))
