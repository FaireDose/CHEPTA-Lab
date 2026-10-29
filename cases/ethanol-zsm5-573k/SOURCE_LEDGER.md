# Source and assumptions ledger

Source: Narin A. Aali and Ghassan J. Hadi (2023), *Kinetic Study of Ethanol Dehydration to Ethylene and Diethyl Ether in Catalytic Packed Bed Reactor Over ZSM-5 Catalyst*, Diyala Journal of Engineering Sciences 16(2), 30–49. [DOI](https://doi.org/10.24237/djes.2023.16203), [publisher PDF](https://djes.info/index.php/djes/article/download/1139/920). Accessed 2026-10-29 through the publisher's PDF text; direct local download returned HTTP 403. No PDF redistributed. Page numbers below are printed page numbers. The first page states [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The transcribed subset and implementation below are adaptations; assumptions and differences are explicit. Final release rights review remains pending.

## Transcribed inputs at 573.15 K

| Quantity | Value | Source locator | Source units / interpretation |
|---|---:|---|---|
| k1 | 0.00868 | Table 9, p. 39 | mol/(g catalyst h), as printed; pressure convention below |
| k2 | 0.00308 | Table 9, p. 39 | mol/(g catalyst h), as printed |
| KA1 | 1.12604 | Table 9, p. 39 | atm^-1 |
| KA2 | 7.50044 | Table 9, p. 39 | atm^-1 |
| Keq1 | 361.8130 | Table 8, p. 38 | header says atm^-1; ambiguity below |
| Keq2 | 8.54626 | Table 8, p. 38 | header says atm^-1; ambiguity below |
| KE1 | 42.85514 | Table 12, p. 41 | atm^-1; E denotes diethyl ether |
| KW1 | 4.483844 | Table 12, p. 41 | atm^-1 |
| KI1 | 0.384379 | Table 12, p. 41 | atm^-1; unused because no inert |
| KE2 | 19.35379 | Table 12, p. 41 | atm^-1 |
| KW2 | 61.30879 | Table 12, p. 41 | atm^-1 |
| KO2 | 20.90733 | Table 12, p. 41 | atm^-1; O denotes ethylene |
| KI2 | 1.954347 | Table 12, p. 41 | atm^-1; unused because no inert |

These are reported fitted/estimated parameters, not new measurements. Table 12 supplies the additional parameters for the same Equations 4 and 14; Table 13 is a separate fit and is not mixed into this case.

## Equations and conventions

Equations 1–2, p. 32: ethanol ⇌ ethylene + water; 2 ethanol ⇌ diethyl ether + water. In the paper's notation A=ethanol, O=ethylene, W=water and E=diethyl ether.

The Table-12 variant implements Equation 4 (p. 32) and Equation 14 (p. 34), with zero inert partial pressure:

```
r1 = k1 (pA - pO pW/Keq1) / (1 + KA1 pA + KE1 pE + KW1 pW)
r2 = k2 KA2^2 (pA^2 - pW pE/Keq2) / (1 + KA2 pA + KE2 pE + KW2 pW + KO2 pO)^2
```

CHEPTA's upstream worked example keeps only the ethanol adsorption term in each denominator. Both variants use partial pressures numerically expressed in atm, p_i = y_i P_kPa / 101.325. Rate coefficients are converted by 1000/3600 = 1/3.6 from the paper's gram/hour basis to CHEPTA's kilogram/second basis. The independent reference instead retains mol/h and grams catalyst throughout.

**Unresolved dimensional convention:** Table 8 labels both equilibrium constants atm^-1, which does not reconcile directly with the different pressure powers in Equations 4 and 14. The printed k1 unit also omits an explicit pressure factor. This case preserves the reported numbers and numerical-atm convention; it does not silently establish a thermodynamic standard state or permit pressure-unit substitution. Resolve this before accepting an unrestricted kinetics training target.

## Boundary conditions and choices

| Input or choice | Classification | Evidence and scope |
|---|---|---|
| 573.15 K; 101.325 kPa | Selected source condition; pressure converted | Section 2, p. 31: 1 atm; selected temperature is tabulated |
| ZSM-5; temperature range 523.15–623.15 K | Source model scope | Section 2; catalyst formulation/Si:Al details require original experimental source |
| Pure ethanol, 1 mol/h | Normalized benchmark basis | Matches upstream fixture; purity also appears in Section 4.4. Absolute flow is not claimed as an experimental run |
| W/F = 0.38 and 1.166 g catalyst h/mol | Source-range endpoints | Section 2, p. 31 |
| W/F = 0.773 | Assumed interior test point | Arithmetic midpoint of endpoints; not a measured observation |
| Catalyst mass = (W/F) × 1 mol/h | Derived | 0.38, 0.773, 1.166 g |
| Tube diameter 0.01 m; bed density 700 kg/m3 | Assumed upstream geometry | Encodes catalyst mass through L = W/(density × area); not measured geometry |
| Isothermal, no pressure drop, one vapor phase | Model assumptions | Broadly consistent with Section 3; no transport/deactivation model |
| Peng–Robinson | Upstream reproduction choice | Rates use yP, not fugacity or concentration; PR does not determine these fixed-T/P kinetic flows |
| Dynamic total molar flow | CHEPTA/reference balance formulation | Composition changes with reaction; not the constant-velocity concentration model in paper Section 3/4.4 |

The run fixes temperature, pressure, feed quality and feed rate. Only W/F is varied within the reported interval. Temperature extrapolation, wet feeds, scale-up and catalyst substitutions are not authorized by this case. Bounds on uncertain parameters are unknown; none are invented.

## What remains unverified

- This is a reconstruction of rate equations under an explicitly selected reactor basis. Figure 8 instead uses Equation 39 with Equation 37/Table 14 and constant velocity. Our results are not a reproduction of that figure.
- Original experimental partial pressures/rates, uncertainty and catalyst detail from the underlying Ghassan work have not been obtained. Agreement between two numerical solvers is not agreement with experiments.
- CHEPTA reports five missing PR binary interaction pairs and an ethanol/water parameter outside its fitted temperature range. These warnings are retained in the stream outputs and verification report even though top-level warnings are empty. The fixed-T/P yP-based flow comparison does not validate enthalpy, duty, fugacity or downstream phase separation.
- Energy residual checks are internal accounting checks only. Mass residual has a small rounding contribution from tabulated molecular weights; the independent atom balance is also checked.
- Human engineering review and final dataset rights review are pending. Full-process costs, product purity, separation performance and a route winner are not established.
