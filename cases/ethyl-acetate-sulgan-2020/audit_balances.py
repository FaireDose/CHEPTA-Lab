"""Audit the published stream table of Sulgan et al. (2020), conventional set-up, without simulation.

Reads streams.json (Table 1) and equipment.json (Figure 1) and checks, per block and for the plant:
total molar flow, each component's molar flow (non-reactive blocks), atoms C, H, O (the CSTR and the plant),
the sum of each stream's mole fractions, and that splitter outlets keep the inlet composition.
Nothing is normalized or corrected. '-' in the table (null here) is taken as 0 with the rounding allowance of 0.0000.
Run from the repository root: python cases/ethyl-acetate-sulgan-2020/audit_balances.py
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parent
src = json.loads((R / "streams.json").read_text())
equipment = json.loads((R / "equipment.json").read_text())["equipment"]
S = {s["stream"]: s for s in src["streams"]}
COMP = ["water", "acetic_acid", "ethyl_acetate", "ethanol"]
# atoms C, H, O per molecule: H2O, CH3COOH, CH3COOC2H5, C2H5OH
ATOMS = {"water": (0, 2, 1), "acetic_acid": (2, 4, 2), "ethyl_acetate": (4, 8, 2), "ethanol": (2, 6, 1)}
DN, DX = 0.005, 0.00005  # half of the last printed digit: kmol/h (2 decimals), mole fraction (4 decimals)


def x(s, c):
    v = S[s]["x_" + c]
    return 0.0 if v is None else v


def flow(s, c):
    return S[s]["molar_kmol_h"] * x(s, c)


def flow_err(s, c):
    return DN * x(s, c) + S[s]["molar_kmol_h"] * DX + DN * DX


def check(name, ins, outs, reactive):
    missing = [s for s in ins + outs if s not in S]
    if missing:
        return {"block": name, "inlets": ins, "outlets": outs, "skipped": f"streams not in Table 1: {missing}"}
    ss = ins + outs
    tot = sum(S[s]["molar_kmol_h"] for s in outs) - sum(S[s]["molar_kmol_h"] for s in ins)
    tot_b = DN * len(ss)
    res = {c: sum(flow(s, c) for s in outs) - sum(flow(s, c) for s in ins) for c in COMP}
    bnd = {c: sum(flow_err(s, c) for s in ss) for c in COMP}
    atom = [sum(res[c] * ATOMS[c][a] for c in COMP) for a in range(3)]
    atom_b = [sum(bnd[c] * ATOMS[c][a] for c in COMP) for a in range(3)]
    ok_tot = abs(tot) <= tot_b + 1e-9
    ok_comp = all(abs(res[c]) <= bnd[c] + 1e-9 for c in COMP)
    ok_atom = all(abs(r) <= b + 1e-9 for r, b in zip(atom, atom_b))
    out = {"block": name, "inlets": ins, "outlets": outs, "reactive": reactive,
           "total_residual_kmol_h": round(tot, 6), "total_bound_kmol_h": round(tot_b, 6), "total_within": ok_tot,
           "component_residual_kmol_h": {c: round(res[c], 6) for c in COMP},
           "component_bound_kmol_h": {c: round(bnd[c], 6) for c in COMP},
           "atom_residual_kmol_h": dict(zip("CHO", (round(a, 6) for a in atom))),
           "atom_bound_kmol_h": dict(zip("CHO", (round(a, 6) for a in atom_b))), "atoms_within": ok_atom}
    if reactive:
        # one equimolar reaction: extent from each species (outlet - inlet) / nu
        nu = {"acetic_acid": -1, "ethanol": -1, "ethyl_acetate": 1, "water": 1}
        out["extent_from_each_species_kmol_h"] = {c: round(res[c] / nu[c], 6) for c in COMP}
        out["within_envelope"] = ok_tot and ok_atom
    else:
        out["components_within"] = ok_comp
        out["within_envelope"] = ok_tot and ok_comp and ok_atom
    return out


blocks = []
for e in equipment:
    if e["type"] == "hx":  # check each side of a two-stream exchanger separately
        for i, o in zip(e["inlets"], e["outlets"]):
            blocks.append(check(f"{e['id']} ({i}->{o})", [i], [o], False))
    else:
        blocks.append(check(e["id"], e["inlets"], e["outlets"], e["type"] == "cstr"))
blocks.append(check("plant (AA0, ETOH0, H2OIN -> W23, H2OP1)", ["AA0", "ETOH0", "H2OIN"], ["W23", "H2OP1"], True))
blocks.append(check("CSTR + C1 (R1, AZ -> D11, W11) less EX1", ["R1", "AZ"], ["D11", "W11"], True))

stream_checks = []
for s in S.values():
    total = sum(x(s["stream"], c) for c in COMP)
    stream_checks.append({"stream": s["stream"], "sum_of_mole_fractions": round(total, 6),
                          "within": abs(total - 1) <= 4 * DX + 1e-9})

splitters = []
for e in equipment:
    if e["type"] == "splitter":
        i = e["inlets"][0]
        for o in e["outlets"]:
            d = {c: round(x(o, c) - x(i, c), 6) for c in COMP}
            splitters.append({"block": e["id"], "inlet": i, "outlet": o, "fraction_difference": d,
                              "same_composition": all(abs(v) <= 2 * DX + 1e-9 for v in d.values())})
    if e["id"] == "SPBY":
        frac = S["BYPASS"]["molar_kmol_h"] / S["H2OL"]["molar_kmol_h"]
        splitters.append({"block": "SPBY", "derived": "BYPASS / H2OL", "value": round(frac, 5), "paper_limit": "at most 0.20 (p.11)"})
    if e["id"] == "SPETAC":
        splitters.append({"block": "SPETAC", "derived": "AZ / W22", "value": S["AZ"]["molar_kmol_h"] / S["W22"]["molar_kmol_h"], "paper": "1 (p.8)"})

water_ratio = flow("D13", "water") / flow("D13", "ethyl_acetate")
conv = (flow("R1", "acetic_acid") - flow("P1", "acetic_acid")) / flow("R1", "acetic_acid")
derived = {
    "D13_water_to_EtAc_mole_ratio": {"value": round(water_ratio, 3), "paper": "4.1 (p.8)"},
    "CSTR_acetic_acid_conversion_per_pass": {"value": round(conv, 4), "paper": "53.0 % (p.8)"},
    "decanter_EtAc_recovery_to_ORG": {"value": round(flow("ORG", "ethyl_acetate") / flow("D13", "ethyl_acetate"), 4), "paper": "over 90 % (p.8)"},
    "C2_EtAc_recovery_to_W21": {"value": round(flow("W21", "ethyl_acetate") / flow("F2", "ethyl_acetate"), 4), "paper": "63.2 % (p.8)"},
}

# Energy: Table 9 (p.23) duties, as transcribed in equipment.json, against Table 9's own totals and the text (p.21-22)
E = {e["id"]: e["specification"] for e in equipment}
cond = sum(E[c]["condenser_duty_kW"]["value"] for c in ("C1", "C2", "C3"))
reb = sum(E[c]["reboiler_duty_kW"]["value"] for c in ("C1", "C2", "C3"))
integrated = sum(E[h]["duty_kW"]["value"] for h in ("EX1", "EX3", "EX4", "EX5"))
external_cool = cond + E["DEC"]["duty_kW"]["value"] + sum(E[h]["duty_kW"]["value"] for h in ("EX2", "EX6", "EX7"))
energy = {
    "cooling_external_sum_kW": {"value": round(external_cool, 2), "paper": "OEC Q_C 3014.72 (Table 9; heat-integrated exchangers excluded)"},
    "heating_sum_kW": {"value": round(reb, 2), "paper": "OEC Q_W 2998.48 (Table 9)"},
    "heat_integrated_exchangers_kW": {"value": round(integrated, 2), "paper": "EX1, EX3, EX4, EX5 marked b (no external energy)"},
    "condensers_sum_kW": {"value": round(cond, 2), "paper": "2851 kW (p.21)"},
    "condensers_share_of_cooling_pct": {"value": round(100 * cond / external_cool, 2), "paper": "94.6 % (p.21)"},
    "C3_reboiler_share_of_heating_pct": {"value": round(100 * E["C3"]["reboiler_duty_kW"]["value"] / reb, 2), "paper": "18.4 % (p.21)"},
    "C1_C2_reboilers_share_of_heating_pct": {"value": round(100 * (reb - E["C3"]["reboiler_duty_kW"]["value"]) / reb, 2), "paper": "81.6 % (p.21)"},
    "EX2_EX6_EX7_cooling_kW": {"value": round(sum(E[h]["duty_kW"]["value"] for h in ("EX2", "EX6", "EX7")), 2), "paper": "less than 164 kW (p.21)"},
}

report = {
    "energy_table_checks": energy,
    "method": "outlet minus inlet, molar; original values, nothing normalized",
    "rounding_model": "nearest rounding at the printed precision: flows +/-0.005 kmol/h, mole fractions +/-0.00005; bounds are sums over the streams of a block (conservative), not statistics",
    "dash_convention": src["dash_convention"],
    "balances": blocks, "streams": stream_checks, "splitters": splitters, "derived": derived}
(R / "balance-results.json").write_text(json.dumps(report, indent=2) + "\n")

lines = ["# Stream table audit (Sulgan et al. 2020, conventional set-up)", "",
         "Generated by [audit_balances.py](audit_balances.py) from [streams.json](streams.json) (Table 1, p.10) and "
         "[equipment.json](equipment.json) (Figure 1, p.9). The paper's numbers are an Aspen Plus simulation, not "
         "measurements. Residuals are outlet minus inlet in kmol/h. 'Within' means within the rounding of the printed "
         "digits; outside it is an inconsistency of the paper's own table, kept, not corrected.", "",
         "## Blocks", "", "| Block | In | Out | Total residual | Largest component (or atom) residual | Within rounding |",
         "|---|---|---|---:|---|---|"]
for b in blocks:
    if "skipped" in b:
        lines.append(f"| {b['block']} | {', '.join(b['inlets'])} | {', '.join(b['outlets'])} | - | {b['skipped']} | not checked |")
        continue
    if b["reactive"]:
        k, v = max(b["atom_residual_kmol_h"].items(), key=lambda kv: abs(kv[1]))
        big = f"atom {k}: {v:+.4f}"
    else:
        k, v = max(b["component_residual_kmol_h"].items(), key=lambda kv: abs(kv[1]))
        big = f"{k}: {v:+.4f}"
    lines.append(f"| {b['block']} | {', '.join(b['inlets'])} | {', '.join(b['outlets'])} | {b['total_residual_kmol_h']:+.3f} | {big} | {'yes' if b['within_envelope'] else '**no**'} |")
lines += ["", "## Streams: sum of mole fractions", ""]
bad = [s for s in stream_checks if not s["within"]]
lines.append("All 32 sums are 1 within rounding." if not bad else
             "Outside rounding: " + ", ".join(f"{s['stream']} ({s['sum_of_mole_fractions']})" for s in bad) + "; all others are 1 within rounding.")
lines += ["", "## Splitters", ""]
for s in splitters:
    if "outlet" in s:
        lines.append(f"- {s['block']}: {s['inlet']} -> {s['outlet']}: same composition {'yes' if s['same_composition'] else '**no**'}")
    else:
        lines.append(f"- {s['block']}: {s['derived']} = {s['value']} (paper: {s.get('paper_limit', s.get('paper'))})")
lines += ["", "## Derived from the table, against the paper's text", "", "| Quantity | From Table 1 | Paper says |", "|---|---:|---|"]
for k, v in derived.items():
    lines.append(f"| {k} | {v['value']} | {v['paper']} |")
lines += ["", "## Energy table (Table 9, p.23) against its totals and the text", "", "| Quantity | From Table 9 | Paper says |", "|---|---:|---|"]
for k, v in energy.items():
    lines.append(f"| {k} | {v['value']} | {v['paper']} |")
lines.append("")
(R / "STREAM_AUDIT.md").write_text("\n".join(lines))
print("\n".join(lines))
