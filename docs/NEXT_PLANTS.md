# The next three complete plants

Written 2026-11-13 by an AI worker session for the maintainer. Draft; no person has checked it.

**Why:** CHEPTA moves to 0.7 once Lab has simulated 4 complete flowsheets from papers, compared stream by stream
(the maintainer, 2026-11-13). Process 2 (ethyl acetate, Piotrowski & Kubica 2021) is the first. The other three are
processes 1, 3 and 4 of [reference/CANDIDATE_PROCESSES.md](reference/CANDIDATE_PROCESSES.md), each as a **complete
plant with a stream table**. A process is replaced only if no usable open plant-level paper exists (the maintainer,
2026-11-13, through the coordinator). **No CHEPTA run before the maintainer's go.**

**How the papers were found:** OpenAlex (open-access and licence filters), web search, Europe PMC and the publishers'
files, not limited to [reference/INITIAL_PAPERS.md](reference/INITIAL_PAPERS.md). Each candidate's licence and
tables were checked in the PDF itself. Criteria: open licence (CC BY first); reactor **and** separation; a full
stream table; unit specifications and duties; CHEPTA 0.6.2 can plausibly run the units and components (read from the
npm package `chepta@0.6.2`, not run).

## The decision in one table

| Process | Recommended paper | Usable as a complete plant? | Status |
|---|---|---|---|
| 1 CO2 to methanol | **Lacerda de Oliveira Campos et al. 2022** (CC BY 4.0) | **yes** | transcribed and audited: [cases/methanol-co2-campos-2022](../cases/methanol-co2-campos-2022/README.md) |
| 3 Ethanol to ethylene / diethyl ether | none usable as a complete plant (best: Tripodi et al. 2019, rights unclear, amine and PSA sections) | **no** | **replaced** (the maintainer, 2026-11-13: four different processes; neither Tripodi nor Šulgan) by **ethylene glycol from ethylene oxide, direct hydration: Shehata, Nady & Gad 2024** (CC BY 4.0), recommended below |
| 4 Cumene hydroperoxide to phenol / acetone | none found | **no**: no open paper with a plant flowsheet and a stream table; CHEPTA also lacks the side products (alpha-methylstyrene, acetophenone, dimethylbenzyl alcohol) | **replaced** by n-butyl acetate (Al-Rabiah et al. 2022, CC BY 4.0) |

Approved by the maintainer (2026-11-13): Campos 2022 for process 1, Al-Rabiah 2022 in place of process 4. Order: **1 methanol (Campos 2022)**, **4' butyl acetate (Al-Rabiah 2022)**, **3' ethylene glycol (Shehata 2024)**, if approved.

The four complete plants are the four processes of CANDIDATE_PROCESSES.md: process 2 is Piotrowski & Kubica 2021. The Šulgan 2020 ethyl acetate plant prepared in this pull request is **not one of the four**: it is a later second ethyl acetate plant (same family as Piotrowski).

## Dataset table, per process (2 or 3 candidates each)

### Process 1: CO2 to methanol

| Paper (licence) | What it gives for a stream-by-stream comparison | What is missing | Complete plant? |
|---|---|---|---|
| **Lacerda de Oliveira Campos et al. 2022**, *Processes* 10, 1535, doi 10.3390/pr10081535 (CC BY 4.0, article p.1; supplement has no separate statement) | **Full stream table**: supplement Tables S9-S10, pp.12-15, all 61 streams of the one-step process (kmol/h, t/h, T, P, molar enthalpy, entropy, exergy, 7 mole %); flowsheet Figure S1 p.10 with text pp.9-11; reactor geometry and catalyst, article p.4; property methods, article p.9; flash sizes Table S13 p.23; **duties, U and areas** Table S14 p.26; the three-step variant too (Tables S11-S12). Audit: all balances close; energy matches Table S14 except cooler HE7 | phases of the streams; reactor-coolant U; compressor efficiencies; second column specification; kinetic Table 1 reprinted from an ACS paper (reuse to check) | **yes** (recommended) |
| Medrano-García, Chagas & Guillén-Gosálbez 2025, *ACS Sust. Chem. Eng.*, doi 10.1021/acssuschemeng.5c01021 (CC BY 4.0) | Supporting information retrieved (Europe PMC, PMC12093377): process description (Sections A-B), life-cycle inventories per kg methanol (Tables S2-S8), hot and cold streams with T in/out and loads for heat integration (Tables S13-S15), exchanger network, costs (Tables S16-S30) | **no stream table** (no compositions or flows per stream); main article Figure 2(a) only | no |
| Borisut & Nuchitprasittichai 2019, *Front. Energy Res.* 7, 81, doi 10.3389/fenrg.2019.00081 (CC BY) | equipment and parameter values (Table 1), base case conditions (Table 2), optimized conditions (Table 4); a supplement exists, not retrieved | no stream table in the article; supplement contents unknown | not as read |

### Process 3: ethanol to ethylene / diethyl ether

| Paper (licence) | What it gives | What is missing | Complete plant? |
|---|---|---|---|
| Tripodi, Belotti & Rossetti 2019, *ACS Sust. Chem. Eng.*, doi 10.1021/acssuschemeng.9b02579. Accepted manuscript in the University of Milan repository (air.unimi.it/handle/2434/699658): "Open Access dal 05/08/2020"; the repository's default licence is CC BY-SA "salvo diversa indicazione"; the publisher's version is restricted | Stream reports for four sections, Tables 9-12 (pp.40-42 of the manuscript; P, T, mass flow and component flows in t/h); mass and energy balances Table 7 (p.37); block data Table 8 (p.39); kinetics Table 3 (p.36); property methods Table 2 (p.35); a 100 kt/a plant | **rights**: whether an ACS accepted manuscript may be reused is to be checked; components partly lumped ("Lights", "Heavies"); CO2 removal by amines (electrolyte NRTL; CHEPTA refuses amines in columns) and PSA (no CHEPTA unit); cryogenic purification | **no as published**; reactor + compression + ethanol recovery (Tables 9-10) could be a partial plant |
| Van der Borght et al. 2019, *Catalysts* 9, 921, doi 10.3390/catal9110921 (CC BY 4.0) | Industrial reactor: transport limitations Table 1, thermodynamics Table 2, operating conditions Table 3, performance Table 4; Figure 1 is a plant sketch taken from another source | no stream table; no separation units simulated | no (reactor only) |
| Maia, Demuner, Secchi & Biscaia 2016, *Braz. J. Chem. Eng.* 33(3), 479-490, doi 10.1590/0104-6632.20160333s20150139 (CC BY 4.0) | dynamic fixed-bed reactor model, Tables 1-5 | no stream table; separation only described | no (reactor only) |
| Not usable: Chen, Kuo, Lobo & Ierapetritou 2024, *Green Chem.* 26, 2903, doi 10.1039/d3gc03858k (CC BY-NC 3.0; ethylene from ethane, not ethanol); Aali & Hadi 2023 (kinetics only); Mohsenzadeh et al. 2017, doi 10.1002/cben.201600025 (CC BY-NC-ND, so excluded from a commercially reusable release; not read); Mash Attar 2022, *Int. J. Chem.* 14(2) (CC BY, diethyl ether; no stream table) | | | no |

### Process 4: cumene hydroperoxide to phenol / acetone

| Paper (licence) | What it gives | What is missing | Complete plant? |
|---|---|---|---|
| J. Phys.: Conf. Ser. 1096, 012197 (2018), doi 10.1088/1742-6596/1096/1/012197 (CC BY 3.0) | a mathematical model of the hydroperoxide decomposition unit; reaction parameters Table 1 | no flowsheet with streams; no separation | no |
| J. Phys.: Conf. Ser. 1096, 012191 (2018), doi 10.1088/1742-6596/1096/1/012191 (CC BY 3.0) | a model of one fractionation column; loads along the column Table 1 | no plant, no stream table | no |
| Phenol-acetone plant simulations in the closed literature (e.g. doi 10.1016/0009-2509(92)87085-5) | | closed access | no |
| Whole cumene-to-phenol route: *J. Chem. Eng. Res. Prog.* 2024, doi 10.9767/jcerp.20276 (CC BY-SA), cumene oxidation to the hydroperoxide | energy study of the oxidation section (abstract read only) | not the cleavage and purification; CC BY-SA (share-alike) | no |

**Replacement for process 4: n-butyl acetate, Al-Rabiah et al. 2022.** Reason: no open plant paper for process 4,
and CHEPTA lacks its side products.

| Paper (licence) | What it gives | What is missing | Complete plant? |
|---|---|---|---|
| **Al-Rabiah, Alqahtani, Al Darwish & Bin Naqyah 2022**, *Processes* 10, 1801, doi 10.3390/pr10091801 (CC BY 4.0, p.1) | **Full stream table** of the conventional process, Table 7 p.14: 14 streams, component flows (kmol/h), T, P, enthalpy (kW), vapour fraction; reactor Table 6 and kinetics Eqs. 13-15 (pp.11-12); also the membrane-reactor (Table 4, equipment Table 5) and reactive-distillation (Table 9) processes | stages and reflux of columns T-101 and T-103 (only T-102: 29 stages); 3 of 10 binary pairs only predicted in CHEPTA 0.6.2; butanol + water two liquids with acetic acid (refused by CHEPTA today) | **yes, with assumed column settings** |

Why this replacement: it **overlaps the register** (ester + alcohol + water; acetic acid kept out of the ester;
esterification equilibrium; [data/ISSUES_AND_ROUTES.md](../data/ISSUES_AND_ROUTES.md)) through a **different
reaction**, and uses extractive distillation with a heavy solvent, today only a lead in the register.

### Replacement for process 3: another classic process (to decide)

The maintainer (2026-11-13): four **different** processes, to find more kinds of issues in CHEPTA; neither Tripodi
nor Šulgan. Searched: cumene, ethylbenzene/styrene, acetone from isopropanol, isopropanol, MTBE/ETBE, ethylene
glycol, formaldehyde, VCM, cyclohexane, allyl chloride, maleic anhydride, toluene HDA, ethanol from ethylene, acetic
acid, DME (OpenAlex with a CC BY filter and a full-text search for "stream table"; CC BY journals).

| Paper (licence) | What it gives | What is missing | New kinds of issues for CHEPTA | Verdict |
|---|---|---|---|---|
| **Shehata, Nady & Gad 2024**, *Sci. Rep.* 14, 28375, doi 10.1038/s41598-024-77713-y (CC BY 4.0, p.19): monoethylene glycol by **direct hydration of ethylene oxide** (Aspen HYSYS 11) | **Stream table** Table 3 (p.10): 14 streams of the direct-hydration plant, molar flow (kmol/h), mass flow (t/yr), mole fractions of water, EO, MEG, DEG, TEG; flowsheet Fig. 5 (p.10); unit specifications Table 1 (p.3: trays and pressures of the dehydration and MEG columns); reactor in the text (p.8: plug flow, 77.8 m × 0.55 m, 199 °C, 3480 kPa, 3 min; outlet distribution); three-effect evaporator 17.8 MW, dehydration column at 85 mm Hg (p.8); energy streams Table 8 (p.14) | **T and P of each stream not in Table 3** (a few in the text); no kinetics (an outlet distribution instead); triethylene glycol is **not a CHEPTA component** (user data needed); the table shows small inconsistencies to audit (e.g. water 0 in the MEG column feed but 0.0023 in its products) | heavy side products (DEG, TEG); a **multiple-effect evaporator**; **vacuum columns** and a **side draw**; a large water recycle (water/EO 10:1) | **recommended** |
| Yalçın 2025, *Int. J. Energy Res.* 2025, doi 10.1155/er/2393398 (CC BY per OpenAlex): toluene hydrodealkylation to benzene, techno-economic | not seen: the publisher refused the download from this session (HTTP 403) | everything unverified | gas-phase recycle with purge, a heavy side product (biphenyl), H2/CH4 with aromatics (Peng-Robinson) | to check: the maintainer could download it; if it has a full stream table it is a strong alternative |
| Odunlami et al. 2022, *Nigerian Res. J. Eng. Environ. Sci.* 7(1), 363-368, doi 10.5281/zenodo.6726535 (CC BY 4.0): acetone from isopropanol | equipment Table 1, stream Table 2 (an image) | no columns (reactor, separator only); the text gives the product as 96.47 % hydrogen | - | no |
| Prestigiacomo, Proietto, Giaconia et al. 2024, *Energy Convers. Manage. X* 22, 100546 (CC BY): ethylbenzene to styrene with solar heat | reactor design Tables 1-4, costs | reactor only, no stream table | - | no |
| Chen, Kuo, Lobo & Ierapetritou 2024, *Green Chem.* 26, 2903 (CC BY-NC 3.0): ethylene from ethane | | non-commercial; ethane routes | - | no |

## Other candidates considered

| Paper | Why not chosen |
|---|---|
| Šulgan, Labovský & Labovská 2020, *Processes* 8, 1618 (CC BY 4.0), ethyl acetate, conventional | process 2 is already covered by Piotrowski & Kubica 2021. Transcribed and audited before the task was corrected ([cases/ethyl-acetate-sulgan-2020](../cases/ethyl-acetate-sulgan-2020/README.md)); kept as a **later second ethyl acetate plant** (same family), not in the first four |
| Šulgan et al. 2021, *Processes* 9, 1380 (CC BY) | heat-pump variant of Šulgan 2020 |
| Klafke, de Souza Jr. & Secchi 2016, *Braz. J. Chem. Eng.* 33(4) (CC BY 4.0), toluene transalkylation | no stream table |
| Trirahayu et al. 2022, *Fuels* 3, 563-579 (CC BY), biodiesel | no stream table |
| Giuliano, Catizzone & Freda 2021, *IJERPH* 18, 807 (CC BY), DME from syngas | no stream table |

## What to decide

1. **Process 1:** approved (Campos 2022). The go to run it is still to give.
2. **Process 3:** replace it by ethylene glycol from ethylene oxide (Shehata, Nady & Gad 2024) (recommended), or
   first have the HDA paper (Yalçın 2025) downloaded and checked.
3. **Process 4:** approved (butyl acetate, Al-Rabiah 2022).
