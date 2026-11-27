#!/usr/bin/env python3
"""CO2 dissolved in the 70 bar separator liquid (FLASH3, stream 24) of Lacerda de Oliveira Campos et al. 2022, checked
against measured data read from NIST TRC's ThermoML archive files (downloaded by the person running this, into a folder
of their own; passed here as arguments, never fetched by this script):

  python3 -I cases/methanol-co2-campos-2022/co2_solubility_check.py XIA.json BEZANEHTAK.json XIE.json > OUT.json

  XIA.json        https://trc.nist.gov/ThermoML/10.1021/je049803i.json  (Xia et al. 2004, CO2 in methanol + water)
  BEZANEHTAK.json https://trc.nist.gov/ThermoML/10.1021/je0301491.json  (Bezanehtak et al. 2004, CO2 + H2 + methanol)
  XIE.json        https://trc.nist.gov/ThermoML/10.1021/je0498614.json  (Xie et al. 2005, CO2 + methanol + H2, 313.2 K)

Kinds: the data points are measured; mole fractions from molalities, interpolations and K values are derived (Lab);
the paper's values are an Aspen Plus V10 simulation (supplement Table S10, p.14, streams 23, 24, 33); CHEPTA's are
simulated (results-chepta-0.6.3/u-flash3-mhv1, results-chepta-0.6.2/u-flash3). Only the Python standard library.
"""
import json
import sys
from pathlib import Path

H = Path(__file__).resolve().parent
M_MEOH, M_W = 32.042, 18.015   # g/mol


def L(x):
    return x if isinstance(x, list) else [x]


def datasets(path):
    """Each ThermoML data set as rows of {column label: value}; labels name the quantity, component and phase."""
    j = json.loads(Path(path).read_text())
    names = {i: L(c["sCommonName"])[0] for i, c in enumerate(L(j["Compound"]), 1)}

    def leaf(d):
        for k, v in d.items():
            if k == "tml_elements":
                continue
            if isinstance(v, dict):
                return leaf(v)
            if isinstance(v, str) and k.startswith("e"):
                return v
        return "?"

    out = []
    for ds in L(j["PureOrMixtureData"]):
        cols = {}
        for v in L(ds.get("Variable", [])):
            vid = v["VariableID"]
            comp = names.get(vid.get("RegNum", {}).get("nOrgNum"), "")
            cols[("v", v["nVarNumber"])] = f"{leaf(vid['VariableType'])}|{comp}|{v.get('VarPhaseID', {}).get('eVarPhase', '')}"
        for p in L(ds["Property"]):
            pid = p["Property-MethodID"]
            comp = names.get(pid.get("RegNum", {}).get("nOrgNum"), "")
            cols[("p", p["nPropNumber"])] = f"{leaf(pid['PropertyGroup'])}|{comp}|{p.get('PropPhaseID', {}).get('ePropPhase', '')}"
        rows = []
        for nv in L(ds["NumValues"]):
            r = {cols[("v", v["nVarNumber"])]: v["nVarValue"] for v in L(nv.get("VariableValue", []))}
            r.update({cols[("p", p["nPropNumber"])]: p["nPropValue"] for p in L(nv.get("PropertyValue", []))})
            rows.append(r)
        out.append({"components": [names[c["RegNum"]["nOrgNum"]] for c in L(ds["Component"])], "columns": list(cols.values()), "rows": rows})
    return out


def interp(x, pts):
    pts = sorted(pts)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (x - x0) / (x1 - x0) * (y1 - y0)
    raise ValueError(f"{x} outside {pts[0][0]}-{pts[-1][0]}")


def main(xia, bez, xie):
    S = {s["stream"]: s for s in json.loads((H / "streams.json").read_text())["streams"]}
    paper = {k: S[k]["mol_pct"]["CO2"] / 100 for k in ("23", "24", "33")}
    P_sep = S["33"]["P_bar"] * 100   # kPa
    p_co2_paper = paper["33"] * P_sep
    mh = json.loads((H / "results-chepta-0.6.3/u-flash3-mhv1.output.json").read_text())["value"]["streams"]
    pr = json.loads((H / "results-chepta-0.6.2/u-flash3.output.json").read_text())["value"]["streams"]

    def x(streams, sid, c="carbon-dioxide"):
        s = streams[sid]
        return s["flow_kmol_h"].get(c, 0) / s["F_kmol_h"]
    sim = {"PR + MHV1 (chepta 0.6.3, run u-flash3-mhv1)": {"x_CO2_liquid": x(mh, "out-liquid"), "y_CO2_vapour": x(mh, "out-vapour")},
           "PR k_ij (chepta 0.6.2, run u-flash3)": {"x_CO2_liquid": x(pr, "out-liquid"), "y_CO2_vapour": x(pr, "out-vapour")}}
    p_co2_mhv1 = sim["PR + MHV1 (chepta 0.6.3, run u-flash3-mhv1)"]["y_CO2_vapour"] * P_sep

    # Xia 2004: molality of CO2 per kg of (methanol + water) against total pressure; solvent given CO2-free
    xd = datasets(xia)[0]
    T, SOLV, MOL, P = xd["columns"]
    def xia_curve(Tk, xs):
        mm = xs * M_MEOH + (1 - xs) * M_W
        return [(r[P], r[MOL] / (r[MOL] + 1000 / mm)) for r in xd["rows"] if r[T] == Tk and r[SOLV] == xs]
    c11 = xia_curve(313.75, 0.4999)
    c_meoh = xia_curve(313.75, 1)
    solvent_paper = S["24"]["mol_pct"]["CH3OH"] / (S["24"]["mol_pct"]["CH3OH"] + S["24"]["mol_pct"]["H2O"])
    xia_out = {
        "source": "Xia et al. 2004, doi 10.1021/je049803i, ThermoML data set 1 (measured); mole fractions converted by Lab (derived)",
        "T_K": 313.75, "solvent_methanol_mole_fraction_CO2_free": 0.4999,
        "paper_stream_24_solvent_methanol_mole_fraction_CO2_free (derived)": round(solvent_paper, 4),
        "points_P_kPa_xCO2": [(p, round(v, 5)) for p, v in sorted(c11)],
        "x_CO2_at_paper_pCO2 (derived, linear in total P)": {"p_CO2_kPa": round(p_co2_paper, 1), "x_CO2": round(interp(p_co2_paper, c11), 4)},
        "x_CO2_at_chepta_mhv1_pCO2 (derived)": {"p_CO2_kPa": round(p_co2_mhv1, 1), "x_CO2": round(interp(p_co2_mhv1, c11), 4)},
        "highest_point_pure_CO2_gas": {"P_kPa": max(c11)[0], "x_CO2": round(max(c11)[1], 4)},
        "pure_methanol_at_paper_pCO2 (derived)": round(interp(p_co2_paper, c_meoh), 4),
        "note": "Gas phase CO2 with the solvent's own vapour (no H2, N2); total pressure is used for the CO2 partial pressure, which overstates it by the solvent vapour (about 20 kPa at 313.75 K, Raoult estimate, assumed), so the interpolated x_CO2 is slightly low. 313.75 K is 10.6 K above the separator's 303.15 K: solubility rises as temperature falls.",
    }
    # Bezanehtak 2004: CO2 + H2 + methanol (no water), liquid x and vapour y measured together
    bd = [d for d in datasets(bez) if len(d["rows"]) > 100][0]
    cT, cP, cx, cxh, cyh, cy = bd["columns"]
    near = [r for r in bd["rows"] if 0.68 <= r[cyh] <= 0.76 and 4000 <= r[cP] <= 7000]
    bez_out = {"source": "Bezanehtak et al. 2004, doi 10.1021/je0301491, ThermoML data set 2 (measured)",
               "selection": "vapour H2 0.68-0.76, 4-7 MPa (the separator: H2 0.73 in the gas, 6.9 MPa)",
               "points_T_K_P_kPa_xCO2_yH2_yCO2": [(r[cT], r[cP], r[cx], r[cyh], r[cy]) for r in sorted(near, key=lambda r: (r[cT], r[cP]))],
               "K_CO2 range (derived)": [round(min(r[cy] / r[cx] for r in near), 2), round(max(r[cy] / r[cx] for r in near), 2)],
               "note": "Pure methanol as solvent: more CO2 dissolves than in 1:1 methanol + water (Xia 2004 at 313.75 K: pure methanol about 3.5 times the 1:1 solvent at the same pressure), so these are upper bounds for stream 24."}
    xe = [d for d in datasets(xie) if d["components"] == ["methanol", "carbon dioxide"] or len(d["columns"]) == 2][0]
    xie_out = {"source": "Xie et al. 2005, doi 10.1021/je0498614, ThermoML data set 1 (measured): CO2 + methanol bubble pressures, 313.2 K",
               "points_xCO2_P_kPa": [(r[xe["columns"][0]], r[xe["columns"][1]]) for r in xe["rows"]],
               "x_CO2_at_paper_pCO2 (derived)": round(interp(p_co2_paper, [(r[xe["columns"][1]], r[xe["columns"][0]]) for r in xe["rows"]]), 4),
               "note": "Pure methanol: an upper bound for the 1:1 solvent."}
    out = {
        "what": "CO2 in the FLASH3 liquid (stream 24, 30 C, 69.25 bar): the paper's Aspen simulation, CHEPTA, and measured solubility",
        "paper (simulated, Aspen Plus V10 NRTL2; supplement Table S10 p.14)": {
            "x_CO2_stream_24": paper["24"], "y_CO2_stream_33": paper["33"], "z_CO2_stream_23": paper["23"],
            "K_CO2 = y/x (derived)": round(paper["33"] / paper["24"], 3), "p_CO2_gas_kPa (derived)": round(p_co2_paper, 1)},
        "chepta (simulated)": {k: {kk: round(vv, 5) for kk, vv in v.items()} | {"K_CO2 (derived)": round(v["y_CO2_vapour"] / v["x_CO2_liquid"], 2)} for k, v in sim.items()},
        "measured": {"xia_2004": xia_out, "bezanehtak_2004": bez_out, "xie_2005": xie_out},
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main(*sys.argv[1:4])
