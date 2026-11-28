#!/usr/bin/env python3
"""Audit the paper's own balances: Al-Rabiah et al. 2022, conventional butyl acetate process (Table 7, Figure 11).

Reads streams.json and equipment.json (this folder) and, for the enthalpy reference only, the component records of
the pinned CHEPTA package (give the path of its src/data/components.json as the first argument; without it the
enthalpy-reference check is skipped). Writes balance-results.json and STREAM_AUDIT.md. No CHEPTA run.

  python3 cases/butyl-acetate-al-rabiah-2022/audit_balances.py /path/to/node_modules/chepta/src/data/components.json

Residuals are outlet minus inlet (minus generation by reaction), kmol/h. Table 7 prints flows to 0.1 kmol/h, so each
printed value is +/-0.05; the tolerance of a residual is the sum of those bounds. Enthalpies are printed to 1 kW
(+/-0.5 kW each). Every number of the paper is an Aspen Plus simulation, not a measurement; inconsistencies are kept,
not corrected.
"""
import json
import math
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
S = {s["id"]: s for s in json.load(open(H / "streams.json"))["streams"]}
COMPS = ["1-butanol", "acetic-acid", "n-butyl-acetate", "water", "bdo"]
# reaction BuOH + AA -> BuAc + H2O (Eq. 1)
NU = {"1-butanol": -1, "acetic-acid": -1, "n-butyl-acetate": 1, "water": 1, "bdo": 0}
# molar masses from IUPAC conventional atomic weights (derived): C 12.011, H 1.008, O 15.999
ATOMS = {"1-butanol": (4, 10, 1), "acetic-acid": (2, 4, 2), "n-butyl-acetate": (6, 12, 2), "water": (0, 2, 1), "bdo": (4, 10, 2)}
MW = {k: 12.011 * c + 1.008 * h + 15.999 * o for k, (c, h, o) in ATOMS.items()}
HALF = 0.05

out = {"source": "Table 7, p.14 and Figure 11, p.11 of Al-Rabiah et al. 2022 (Aspen Plus simulation)",
       "molar_masses_g_mol (derived, IUPAC conventional atomic weights)": {k: round(v, 3) for k, v in MW.items()},
       "blocks": [], "energy": [], "streams": [], "notes": []}


def block(name, ins, outs, extent=0.0):
    res, tol = {}, {}
    for c in COMPS:
        r = sum(S[o]["kmol_h"][c] for o in outs) - sum(S[i]["kmol_h"][c] for i in ins) - NU[c] * extent
        res[c] = round(r, 4)
        tol[c] = HALF * (len(ins) + len(outs))
    mass_in = sum(S[i]["mass_kg_h"] for i in ins)
    mass_out = sum(S[o]["mass_kg_h"] for o in outs)
    ok = all(abs(res[c]) <= tol[c] + 1e-9 for c in COMPS)
    d = {"block": name, "in": ins, "out": outs, "reaction_extent_kmol_h": extent, "component_residual_kmol_h": res,
         "tolerance_kmol_h": tol[COMPS[0]], "within_rounding": ok, "mass_in_kg_h": mass_in, "mass_out_kg_h": mass_out,
         "mass_residual_kg_h": mass_out - mass_in}
    out["blocks"].append(d)
    return d


# reaction extent from stream 3 -> 4 (butyl acetate formed)
ext = S["4"]["kmol_h"]["n-butyl-acetate"] - S["3"]["kmol_h"]["n-butyl-acetate"]
block("V-101 (1 + 2 + 12 -> 3)", ["1", "2", "12"], ["3"])
block("P-101 + R-101 + P-102 (3 -> 4), one reaction", ["3"], ["4"], ext)
block("T-101 (4 -> 5 + 6)", ["4"], ["5", "6"])
block("valve + E-101 (6 -> 7)", ["6"], ["7"])
block("M-101 (8 + 14 -> 9)", ["8", "14"], ["9"])
block("T-102 (5 + 9 -> 10 + 11)", ["5", "9"], ["10", "11"])
block("T-103 (11 -> 12 + 13)", ["11"], ["12", "13"])
block("E-102 (13 -> 14)", ["13"], ["14"])
ext_plant = S["7"]["kmol_h"]["n-butyl-acetate"] + S["10"]["kmol_h"]["n-butyl-acetate"]
block("Plant (1 + 2 + 8 -> 7 + 10), one reaction", ["1", "2", "8"], ["7", "10"], ext_plant)

conv = ext / S["3"]["kmol_h"]["1-butanol"]
out["reactor"] = {"extent_kmol_h": round(ext, 2), "butanol_conversion_per_pass": round(conv, 4),
                  "text_p11": "69.8 %",
                  "feed_ratio_BuOH_to_AA_stream3": round(S["3"]["kmol_h"]["1-butanol"] / S["3"]["kmol_h"]["acetic-acid"], 4),
                  "fresh_ratio_AA_to_BuOH": round(S["1"]["kmol_h"]["acetic-acid"] / S["2"]["kmol_h"]["1-butanol"], 4),
                  "reaction_heat_kW (derived: extent x 29.312 kJ/mol, Eq. 1)": round(ext * 29.312 / 3.6, 1)}

# streams: mass from moles, mole fraction sums are trivially 1 (component flows printed)
for sid, s in S.items():
    n = sum(s["kmol_h"].values())
    m = sum(s["kmol_h"][c] * MW[c] for c in COMPS)
    out["streams"].append({"id": sid, "kmol_h": round(n, 2), "kg_h_from_moles": round(m, 1), "kg_h_printed": s["mass_kg_h"],
                           "difference_%": round(100 * (s["mass_kg_h"] - m) / m, 3) if m else None,
                           "molar_enthalpy_kJ_mol (derived)": round(s["enthalpy_kW"] * 3.6 / n, 1) if n else None})

# product
p = S["7"]["kmol_h"]
n7 = sum(p.values()); m7 = sum(p[c] * MW[c] for c in COMPS)
out["product_7"] = {"mole_fraction_BuAc": round(p["n-butyl-acetate"] / n7, 5), "mass_fraction_BuAc": round(p["n-butyl-acetate"] * MW["n-butyl-acetate"] / m7, 5),
                    "mass_fraction_acetic_acid": round(p["acetic-acid"] * MW["acetic-acid"] / m7, 5),
                    "mass_fraction_butanol": round(p["1-butanol"] * MW["1-butanol"] / m7, 5),
                    "mass_fraction_water": 0.0, "figure_label": "99.0% BuAc, 100 km/h"}
# operating hours
bu_t_h = p["n-butyl-acetate"] * MW["n-butyl-acetate"] / 1000
out["hours"] = {"92500 t/yr over the ester in stream 7 (h/yr)": round(92500 / bu_t_h, 0),
                "92500 t/yr over all of stream 7 (h/yr)": round(92500 / (S["7"]["mass_kg_h"] / 1000), 0),
                "MR steam 41668 MWh/yr over MR heat duty 5208 kW (h/yr)": round(41668 / 5.208, 0),
                "basis": "Table 10 and p.16; the paper does not print its operating hours"}
hrs = 8000.0
out["utilities_conventional_MW_at_8000_h"] = {"steam": round(218729 / hrs, 2), "cooling_water": round(215504 / hrs, 2)}


# energy, per block: sum(H out) - sum(H in) = duty + work (kW)
def energy(name, ins, outs, comment):
    hin = sum(S[i]["enthalpy_kW"] for i in ins); hout = sum(S[o]["enthalpy_kW"] for o in outs)
    out["energy"].append({"block": name, "H_in_kW": hin, "H_out_kW": hout, "H_out_minus_H_in_kW": hout - hin,
                          "rounding_kW": 0.5 * (len(ins) + len(outs)), "reading": comment})


energy("V-101 (1 + 2 + 12 -> 3)", ["1", "2", "12"], ["3"], "an adiabatic mixer should give 0")
energy("V-101 without the recycle (1 + 2 -> 3)", ["1", "2"], ["3"], "0 here means stream 3's enthalpy is that of the fresh feeds alone")
energy("P-101 + R-101 + P-102 (3 -> 4)", ["3"], ["4"], "reactor duty + pump work, if 3 were consistent")
energy("P-101 + R-101 + P-102 (1 + 2 + 12 -> 4)", ["1", "2", "12"], ["4"], "reactor duty + pump work with the recycle's enthalpy included")
energy("T-101 (4 -> 5 + 6)", ["4"], ["5", "6"], "Q_reboiler + Q_condenser (net)")
energy("valve + E-101 (6 -> 7)", ["6"], ["7"], "E-101 duty")
energy("M-101 (8 + 14 -> 9)", ["8", "14"], ["9"], "an adiabatic mixer should give 0")
energy("M-101 read as 8 + 13 -> 9", ["8", "13"], ["9"], "0 here means stream 9 was mixed from the uncooled solvent 13")
energy("T-102 (5 + 9 -> 10 + 11)", ["5", "9"], ["10", "11"], "Q_reboiler + Q_condenser (net)")
energy("T-103 (11 -> 12 + 13)", ["11"], ["12", "13"], "Q_reboiler + Q_condenser (net)")
energy("E-102 (13 -> 14)", ["13"], ["14"], "E-102 duty")
energy("Plant (1 + 2 + 8 -> 7 + 10)", ["1", "2", "8"], ["7", "10"], "net heat added to the whole plant (all duties + work)")

# temperatures that cannot come from mixing
out["notes"].append("Stream 3 is printed at 298.2 K, the temperature of the fresh feeds, although it contains the recycle 12 at 393.6 K (Table 7).")
out["notes"].append("Stream 9 is printed at 507.0 K, but it is mixed from 8 (298.2 K) and 14 (303.2 K); 507 K lies between 13 (512.2 K) and 8.")

# enthalpy reference: CHEPTA 0.6.3 records (ideal-gas formation enthalpy minus DIPPR106 heat of vaporization at 298.15 K)
if len(sys.argv) > 1:
    comps = json.load(open(sys.argv[1]))["components"]
    ref = {}
    for c in COMPS:
        r = comps[c]
        hv = r["properties"]["heatOfVaporization"]
        k = hv["coefficients"]; tr = 298.15 / hv["Tc_K"]
        e = k.get("B", 0) + k.get("C", 0) * tr + k.get("D", 0) * tr ** 2 + k.get("E", 0) * tr ** 3
        dhv = k["A"] * (1 - tr) ** e / 1000
        hf = r["formation"]["Hf_ig_J_mol"] / 1000
        ref[c] = {"Hf_ig_298_kJ_mol": hf, "dHvap_298_kJ_mol": round(dhv, 2), "liquid_reference_298_kJ_mol": round(hf - dhv, 1)}
    out["enthalpy_reference (derived from chepta 0.6.3 components.json)"] = ref
    checks = []
    for sid, main in [("1", "acetic-acid"), ("2", "1-butanol"), ("7", "n-butyl-acetate"), ("10", "water"), ("14", "bdo")]:
        s = S[sid]; n = sum(s["kmol_h"].values())
        hm = s["enthalpy_kW"] * 3.6 / n
        # composition-weighted liquid reference (sensible heat from 298 K left out: streams 1, 2 at 298.2 K; 7 at 308.2 K;
        # 10 at 373.1 K; 14 at 303.2 K)
        hr = sum(s["kmol_h"][c] * ref[c]["liquid_reference_298_kJ_mol"] for c in COMPS) / n
        checks.append({"stream": sid, "main_component": main, "T_K": s["T_K"], "paper_kJ_mol": round(hm, 1),
                       "reference_liquid_298_kJ_mol": round(hr, 1), "difference_kJ_mol": round(hm - hr, 1)})
    out["enthalpy_check"] = checks
    # Lab's estimate only: reactor section duty if streams 1 and 2 carried the reference liquid enthalpy at 298 K
    h1 = sum(S["1"]["kmol_h"][c] * ref[c]["liquid_reference_298_kJ_mol"] for c in COMPS) / 3.6
    h2 = sum(S["2"]["kmol_h"][c] * ref[c]["liquid_reference_298_kJ_mol"] for c in COMPS) / 3.6
    out["reactor_duty_estimate"] = {
        "H1_reference_kW": round(h1), "H2_reference_kW": round(h2), "H12_paper_kW": S["12"]["enthalpy_kW"], "H4_paper_kW": S["4"]["enthalpy_kW"],
        "H4_minus_inlets_kW": round(S["4"]["enthalpy_kW"] - h1 - h2 - S["12"]["enthalpy_kW"]),
        "status": "derived by Lab, not the paper's; the acetic acid reference is uncertain (its CHEPTA heat of vaporization is the apparent value of a dimerizing vapour), so this only shows the sign and order of magnitude"}
    # the reaction enthalpy the stream table implies, from streams 1, 2 (liquid, 298.2 K) and the reference for products
    out["notes"].append("Reaction enthalpy implied by the molar enthalpies of streams 1, 2, 7 and 10 (derived, mixed temperatures): see enthalpy_check; Eq. 1 gives -29.312 kJ/mol.")

json.dump(out, open(H / "balance-results.json", "w"), indent=1)

# report
L = ["# Stream table audit (Al-Rabiah et al. 2022, conventional butyl acetate process)", "",
     "Generated by [audit_balances.py](audit_balances.py) from [streams.json](streams.json) (Table 7, p.14) and "
     "[equipment.json](equipment.json) (Figure 11 p.11, Table 6 p.12, text pp.10-12, Table 10 p.16). The paper's numbers are an "
     "Aspen Plus simulation, not measurements. Residuals are outlet minus inlet (minus generation by the one reaction) in kmol/h; "
     "'within rounding' means within the sum of the +/-0.05 kmol/h bounds of the printed values. Inconsistencies are kept, not corrected. "
     "Molar masses from IUPAC conventional atomic weights (derived).", "",
     "## Material balance per block", "",
     "| Block | Largest component residual (kmol/h) | Tolerance | Within rounding | Mass in / out (kg/h) |", "|---|---|---:|---|---|"]
for d in out["blocks"]:
    c = max(d["component_residual_kmol_h"], key=lambda k: abs(d["component_residual_kmol_h"][k]))
    L.append(f"| {d['block']} | {c}: {d['component_residual_kmol_h'][c]:+.2f} | {d['tolerance_kmol_h']:.2f} | "
             f"{'yes' if d['within_rounding'] else '**no**'} | {d['mass_in_kg_h']} / {d['mass_out_kg_h']} ({d['mass_residual_kg_h']:+}) |")
r = out["reactor"]
L += ["", f"Reactor: extent {r['extent_kmol_h']} kmol/h (derived from stream 3 -> 4); butanol conversion per pass "
      f"{100 * r['butanol_conversion_per_pass']:.2f} % (text p.11: 69.8 %); BuOH/AA in stream 3 = {r['feed_ratio_BuOH_to_AA_stream3']} "
      f"(Table 6: 1:1); fresh AA/BuOH = {r['fresh_ratio_AA_to_BuOH']}; heat of reaction released {r['reaction_heat_kW (derived: extent x 29.312 kJ/mol, Eq. 1)']} kW (derived from Eq. 1).", "",
      "## Energy per block (stream enthalpies of Table 7)", "",
      "| Block | H in (kW) | H out (kW) | Out - in (kW) | Reading |", "|---|---:|---:|---:|---|"]
for e in out["energy"]:
    L.append(f"| {e['block']} | {e['H_in_kW']} | {e['H_out_kW']} | {e['H_out_minus_H_in_kW']:+} | {e['reading']} |")
L += ["", "Mixer temperatures: " + " ".join(out["notes"][:2]), ""]
if "enthalpy_check" in out:
    L += ["## Molar enthalpies of nearly pure streams against CHEPTA's data", "",
          "Reference: CHEPTA 0.6.3 ideal-gas formation enthalpy minus its heat of vaporization at 298.15 K (ChemSep records; derived by Lab, "
          "sensible heat from 298 K not included, so a few kJ/mol of difference is expected for streams 7, 10 and 14). Aspen's own reference "
          "state is not printed.", "",
          "| Stream | Main component | T (K) | Paper (kJ/mol, derived) | Reference liquid 298 K (kJ/mol) | Difference |", "|---|---|---:|---:|---:|---:|"]
    for c in out["enthalpy_check"]:
        L.append(f"| {c['stream']} | {c['main_component']} | {c['T_K']} | {c['paper_kJ_mol']} | {c['reference_liquid_298_kJ_mol']} | {c['difference_kJ_mol']:+} |")
    rd = out["reactor_duty_estimate"]
    L += ["", "Streams 7, 10 and 14 agree with the reference within the sensible heat; the fresh feeds 1 and 2 do not (by -192 and -142 kJ/mol), "
          "so stream 3 (= 1 + 2 in enthalpy) and the whole-plant energy balance inherit the error. Acetic acid's reference is itself uncertain "
          "(apparent heat of vaporization of a dimerizing vapour), but not by 190 kJ/mol.", "",
          f"Lab's estimate only: with streams 1 and 2 at the reference ({rd['H1_reference_kW']} and {rd['H2_reference_kW']} kW), the reactor "
          f"section (V-101 to P-102) would give H4 - (H1 + H2 + H12) = {rd['H4_minus_inlets_kW']:+} kW, i.e. a small net heat removal, against "
          "813 kW released by the reaction (Eq. 1). The paper prints no reactor duty.", ""]
L += ["## Streams: printed mass against the moles", "", "| Stream | kmol/h | kg/h from moles | kg/h printed | difference % | kJ/mol (derived) |", "|---|---:|---:|---:|---:|---:|"]
for s in out["streams"]:
    L.append(f"| {s['id']} | {s['kmol_h']} | {s['kg_h_from_moles']} | {s['kg_h_printed']} | {s['difference_%']} | {s['molar_enthalpy_kJ_mol (derived)']} |")
pr = out["product_7"]; h = out["hours"]
L += ["", "## Product and capacity", "",
      f"Stream 7: butyl acetate {100 * pr['mole_fraction_BuAc']:.2f} mol %, {100 * pr['mass_fraction_BuAc']:.2f} wt %; acetic acid "
      f"{100 * pr['mass_fraction_acetic_acid']:.2f} wt %; butanol {100 * pr['mass_fraction_butanol']:.3f} wt %; water 0 (derived; Figure 11 label '99.0% BuAc').", "",
      f"Operating hours implied (the paper prints none): 92,500 t/yr over the ester in stream 7 gives {h['92500 t/yr over the ester in stream 7 (h/yr)']:.0f} h/yr; "
      f"over all of stream 7, {h['92500 t/yr over all of stream 7 (h/yr)']:.0f} h/yr; the membrane-reactor utilities (41,668 MWh/yr over 5208 kW) give "
      f"{h['MR steam 41668 MWh/yr over MR heat duty 5208 kW (h/yr)']:.0f} h/yr. At 8000 h/yr the conventional plant's Table 10 means "
      f"{out['utilities_conventional_MW_at_8000_h']['steam']} MW of steam and {out['utilities_conventional_MW_at_8000_h']['cooling_water']} MW of cooling water (derived).", ""]
(H / "STREAM_AUDIT.md").write_text("\n".join(L))
print("\n".join(L))
