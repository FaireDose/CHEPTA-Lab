# Initial simulation-training sources

Checked 2026-10-29. This is a screening register, not extracted training data. Full text access and reuse permission are recorded separately. No paper PDF is redistributed in this repository.

## aali-hadi-2023

**Kinetic Study of Ethanol Dehydration to Ethylene and Diethyl Ether in Catalytic Packed Bed Reactor Over ZSM-5 Catalyst**

Narin A. Aali; Ghassan J. Hadi; 2023. DOI: [10.24237/djes.2023.16203](https://doi.org/10.24237/djes.2023.16203).

[Source / open copy](https://www.djes.info/index.php/djes/article/view/1139)

- Access checked: publisher full PDF; CC BY 4.0 stated on p. 30. Corpus status: `attribution_required`.
- Equations 4/14 and Tables 8/9/12 have been transcribed and used in a draft benchmark.
- The upstream simplification omits product adsorption terms available in Table 12. Both versions were executed at three catalyst loadings and independently checked.
- Pressure-unit conventions and original experimental evidence remain unresolved. Human engineering review is pending.
- See the [source ledger and values](../../cases/ethanol-zsm5-573k/SOURCE_LEDGER.md) and [executed case](../../cases/ethanol-zsm5-573k/README.md).

## medrano-garcia-2025

**Integrating the Reverse Boudouard Reaction for a More Efficient Green Methanol Synthesis from CO2 and Renewable Energy**

Juan D. Medrano-García; Marina T. Chagas; Gonzalo Guillén-Gosálbez; 2025. DOI: [10.1021/acssuschemeng.5c01021](https://doi.org/10.1021/acssuschemeng.5c01021).

[Source / open copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC12093377/)

- Access checked: `full_text`.
- License: CC-BY-4.0 (main article). Corpus status: `attribution_required`.
- Use: Baseline CO2-to-methanol plant: reactor, condensation, recycle/purge and purification.
- Inspect: Methods: process simulation; Figure 2(a); Supporting Information, sections A/B: design and simulation results (identified, not retrieved).
- Remaining work: Retrieve supporting information and audit kinetics, thermodynamics, stream specifications and column data.
- Limitation: Select the green-methanol baseline only; biomass and reverse-Boudouard sections are outside the first case.
- Limitation: Supporting PDF fetch failed; its detailed specifications and rights remain unaudited.
- Limitation: CHEPTA's equilibrium example is not the paper's kinetic PFR.

## sulgan-2020

**Multi-Aspect Comparison of Ethyl Acetate Production Pathways: Reactive Distillation Process Integration and Intensification via Mechanical and Chemical Approach**

Branislav Šulgan; Juraj Labovský; Zuzana Labovská; 2020. DOI: [10.3390/pr8121618](https://doi.org/10.3390/pr8121618).

[Source / open copy](https://psecommunity.org/wp-content/plugins/wpor/includes/file/2107/LAPSE-2021.0623-1v1.pdf)

- Access checked: `full_text`.
- License: CC-BY-4.0. Corpus status: `attribution_required`.
- Use: Detailed conventional ethyl-acetate plant for a later complete flowsheet case.
- Inspect: Sections 2.1–2.3: thermodynamics, kinetics, equipment; Section 3.1; Figure 1; Tables 1–2: conventional process; Section 4.1; Table 9: energy.
- Remaining work: Audit the conventional CSTR case first; map each property and kinetic input to an open source and document method differences.
- Limitation: Uses NRTL-HOC and non-equilibrium column models; initial CHEPTA equilibrium-stage columns alone will not reproduce the same model.
- Limitation: Some property inputs originate in external databases; article access does not establish rights to redistribute those databases.
- Limitation: Reactive-distillation variants are later work.

## van-der-borght-2019

**First-Principles-Based Simulation of an Industrial Ethanol Dehydration Reactor**

Kristof Van der Borght; Konstantinos Alexopoulos; Kenneth Toch; Joris W. Thybaut; Guy B. Marin; Vladimir V. Galvita; 2019. DOI: [10.3390/catal9110921](https://doi.org/10.3390/catal9110921).

[Source / open copy](https://biblio.ugent.be/publication/8635037/file/8673958.pdf)

- Access checked: `full_text`.
- License: CC-BY-4.0. Corpus status: `attribution_required`.
- Use: Industrial reactor extension and tests of model applicability.
- Inspect: Figure 1: plant context; Table 1: transport limitations; Tables 2–4: kinetic thermodynamics, operating conditions and performance.
- Remaining work: Inventory the complete reaction network, species, catalyst assumptions and transport requirements before choosing a reproducible subset.
- Limitation: Microkinetic network and transport analysis differ from Aali–Hadi's two-reaction model.
- Limitation: The plant diagram is context; it is not proof that all downstream column specifications are supplied.
- Limitation: C3+ products cannot be silently omitted or replaced.

## piotrowski-kubica-2021

**Integration of the Process for Production of Ethyl Acetate by an Enhanced Extraction Process**

Wojciech Piotrowski; Robert Kubica; 2021. DOI: [10.3390/pr9081425](https://doi.org/10.3390/pr9081425).

[Source / open copy](https://www.mdpi.com/2227-9717/9/8/1425)

- Access checked: `full_text`.
- License: CC-BY-4.0. Corpus status: `attribution_required`.
- Use: Alternative ethyl-acetate route and literature for extraction decisions.
- Inspect: Figure 1; Section 2: process layout; Sections 2.1–2.2: UNIQUAC and kinetics; Equations 1–3; Section 3: reaction and separation studies.
- Remaining work: Resolve rate-law definitions and identify extraction specifications; keep this as an extension of the ethyl-acetate family.
- Limitation: Multistage extraction and distillation are not available at the audited CHEPTA commit.
- Limitation: Kinetic concentration basis, catalyst dependence and units need checking against the original reference before transcription.

## yoo-2021

**Effects of Reactor Type on the Economy of the Ethanol Dehydration Process: Multitubular vs. Adiabatic Reactors**

Kee-Youn Yoo; 2021. DOI: [10.9713/kcer.2021.59.3.467](https://doi.org/10.9713/kcer.2021.59.3.467).

[Source / open copy](https://www.kiche.or.kr/journal/kcer/view/all/59/3/467)

- Access checked: `publisher_abstract`.
- License: CC-BY-NC-3.0. Corpus status: `reference_only`.
- Use: Background comparison connecting reactor choice to separation needs.
- Inspect: Publisher abstract and license statement; full PDF not reviewed.
- Remaining work: Keep bibliographic reference only in this release.
- Limitation: Non-commercial license: excluded from the initial commercially reusable training corpus pending permission or a separate rights assessment.

## rawlings-ekerdt

**Chemical Reactor Analysis and Design Fundamentals, second edition**

James B. Rawlings; John G. Ekerdt. 

[Source / open copy](https://sites.engineering.ucsb.edu/~jbraw/chemreacfun/)

- Access checked: `author_download_page`.
- License: Copyright notice; no open reuse license verified. Corpus status: `reference_only`.
- Use: Provenance of existing CHEPTA reactor demonstrations.
- Inspect: Example 4.2 (cumene hydroperoxide); 4.4 (generic PFR); 4.5 (benzene pyrolysis), as cited by CHEPTA.
- Remaining work: Review the relevant edition and obtain permission or replace copied teaching material with independently authored, sourced cases.
- Limitation: Free reading does not establish redistribution rights.
- Limitation: The generic A → B + C example must not be presented as validated industrial ethane kinetics.

## kirbaslar-2001

**Esterification of Acetic Acid with Ethanol Catalysed by an Acidic Ion-Exchange Resin**

Ş. İsmail Kırbaşlar; Z. Barış Baykal; Umur Dramur; 2001. 

[Source / open copy](https://online-journals.tubitak.gov.tr/engineering/abstract.htm?id=5026)

- Access checked: `search_metadata_only`.
- License: Not verified. Corpus status: `needs_review`.
- Use: Lead corresponding to CHEPTA's unresolved Amberlyst-15 kinetics source.
- Inspect: Turkish Journal of Engineering and Environmental Sciences 25, 569–577; full text not retrieved.
- Remaining work: Locate an accessible publisher or authorized repository copy and check its reuse terms.
- Limitation: Direct publisher access failed; no kinetic parameters accepted from search snippets.


