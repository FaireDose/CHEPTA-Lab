#!/usr/bin/env python3
"""Write dataset/records/butyl-acetate-al-rabiah-2022.json: evidence blocks, evidence rows and decision rows of this case
(dataset table stage, before any CHEPTA plant run).

The blocks hash passages of two downloaded documents, which stay in the ignored raw_papers/ folder and are passed as
arguments (never committed):
  python3 cases/butyl-acetate-al-rabiah-2022/build_kb_rows.py raw_papers/al-rabiah-2022-dl/paper.txt \
      raw_papers/eastman-butyl-acetate-spec-dl/spec.txt
paper.txt and spec.txt are `pdftotext -layout` (poppler 24.02.0) of the publisher PDF (sha256 9e9ccb94...) and of
Eastman's sales specification 56-12 (sha256 c10ec356...). Rows are drafts written by an AI session; none is reviewed.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CASE = "butyl-acetate-al-rabiah-2022"
PAPER, SPEC = (Path(a).read_text(encoding="utf-8").split("\n") for a in sys.argv[1:3])
PDF_SHA = "9e9ccb94d58868a8165e95e1004ab82c63eccf2dafbf2c53c9cd7fb110167e33"
SPEC_SHA = "c10ec3564c1c7bfa0c45085ea0fa6e4d87796441c71968aeaa10c33e5f4ea9a8"
DATE = "2026-11-27"
JUDGED = " Judged at planning only: the rule shaped the plan; whether it helps in CHEPTA is for the run rows."
DRAFT = "Draft, written by an AI session from the case files (2026-11-27); not reviewed."


def blk(key, lines, locator, summary, src="paper"):
    a, b = lines
    text = PAPER if src == "paper" else SPEC
    frag = "\n".join(text[a - 1:b])
    base = {"paper": dict(source_id="al-rabiah-2022", source_url="https://mdpi-res.com/d_attachment/processes/processes-10-01801/article_deploy/processes-10-01801.pdf",
                          source_version="Publisher PDF, fetched 2026-11-27 (sha256 below; differs from the maintainer's copy of 2026-11-20)", document_sha256=PDF_SHA, file="paper.txt"),
            "spec": dict(source_id="eastman-butyl-acetate-salespec-56-12", source_url="https://salespec.eastman.com/supplemental/salespecs/71001046.pdf",
                         source_version="Sales Specification No. 56-12, effective 05/07/2008, fetched 2026-11-27", document_sha256=SPEC_SHA, file="spec.txt")}[src]
    return {"id": f"{CASE}.blk-{key}", "source_id": base["source_id"], "source_url": base["source_url"], "source_version": base["source_version"],
            "document_sha256": base["document_sha256"], "document_hash_kind": "archived_pdf", "locator": locator,
            "selector": f"{base['file']} lines {a}-{b} (pdftotext -layout of the PDF); UTF-8 lines joined by LF, no terminal LF",
            "source_fragment_sha256": hashlib.sha256(frag.encode("utf-8")).hexdigest(),
            "extraction_method": "pdftotext -layout (poppler 24.02.0) of the PDF; passage chosen by an AI session",
            "collected_on": DATE, "summary": summary, "target_revealing": False}


blocks = [
    blk("p1-uses", (36, 45), "Section 1, p.1", "Butyl acetate is a solvent for adhesives, lacquers, coatings and paints; an extraction agent or solvent in pharmaceuticals and cosmetics; used for fruit flavours; made by esterifying n-butanol with acetic acid over solid acids such as ion-exchange resins."),
    blk("p2-nrtl", (96, 108), "Section 2, Eq. 1, p.2", "BuOH + AA = BuAc + H2O, dH = -29.312 kJ/mol; NRTL selected for the vapour-liquid-liquid equilibrium, the NRTL model of Aspen Plus used."),
    blk("p3-azeotrope", (139, 145), "Section 2, p.3 (Figure 2)", "n-Butanol and water form an azeotrope (23.5 % butanol, 76.5 % water, 91.6 C, 364.7 K, Aspen); Shen et al. used 1,4-butanediol as the solvent to separate them; residue curve map at 101.3 kPa."),
    blk("p7-fig9", (446, 449), "Section 5, p.7 (Figure 9), membrane-reactor route", "n-Butanol and butyl acetate form an azeotrope at atmospheric pressure; the separation is possible at 304 kPa but needs many stages."),
    blk("p10-kinetics", (615, 639), "Section 6 and 6.1, Eqs. 13-15, p.10", "Conventional process: isothermal catalytic fixed bed, Aspen Plus, same capacity, catalyst and product purity as the other routes, inputs from refs. [20,23]; Amberlyst-15 rate law r = kF C_AA C_BuOH - kB C_BuAc C_H2O, kF = exp(11.472 - 6986.3/T), kB = exp(12.482 - 7937.7/T)."),
    blk("p11-plant", (684, 784), "Section 6.1, p.11 (text overlaid with figure captions in the extraction)", "92,500 t/yr; feeds 1 and 2 mixed with recycle 12 in V-101, pumped by P-101 to the fixed bed R-101 at 1:1; RPlug; maximum conversion ~70 %, 69.8 % within ~2.5 m; effluent pumped to 304 kPa by P-102 into T-101."),
    blk("p12-plant", (790, 802), "Section 6.1, p.12", "Ester leaves T-101 bottoms, cooled in E-101; acid, butanol and water overhead to extractive distillation with 1,4-butanediol at the top of T-102 (29 stages); water overhead to wastewater treatment; solvent and reactants (stream 11) to recovery column T-103; solvent recycled 'to the extractive distillation column (T-101)'; acid and butanol recycled to V-101."),
    blk("table6", (804, 812), "Table 6, p.12", "Conventional reactor: BuOH-to-AA 1:1, 363 K, feed pressure 284 kPa, 41 m3, Amberlyst-15."),
    blk("table7", (854, 879), "Table 7, p.14", "14 streams: T (K), P (kPa), enthalpy (kW), vapour fraction, mass (kg/h), component flows (kmol/h) of n-butanol, acetic acid, butyl acetate, water, solvent."),
    blk("p16-utilities", (977, 999), "Section 7.1 and Table 10, p.16", "Utilities: cooling water 293 K, LP steam 398 K, MP steam 448 K; conventional 218,729 MWh/yr MP steam and 215,504 MWh/yr cooling water; MR and RD heat duties 5208 and 3298 kW."),
    blk("eastman-spec", (1, 20), "Sales Specification No. 56-12, p.1 (single table)", "Eastman Butyl Acetate: n-butyl acetate 99.50 % min; acid as acetic 0.0100 % max; water 0.0500 % max; iBuOH + BuOH 0.25 % max; colour 5 max; non-volatile 0.005 g/100 mL max.", src="spec"),
]


def B(*k):
    return [f"{CASE}.blk-{x}" for x in k]


def q(name, value, unit, basis, qualifier="equal"):
    return {"name": name, "value": value, "unit": unit, "basis": basis, "qualifier": qualifier}


SIM = "Aspen Plus simulation (NRTL), not measured."
evidence = [
    {"id": f"{CASE}.ev-reactor", "block_ids": B("p10-kinetics", "p11-plant", "table6", "table7"),
     "claim": "A fixed bed of Amberlyst-15 (41 m3) at 363 K, feed 1:1 at 284 kPa (Table 6), converts 69.8 % of the butanol per pass (stream 3 to 4 of Table 7: 143.1 to 43.2 kmol/h butanol, 0.9 to 100.8 kmol/h ester); Aspen RPlug with the kinetics of Eqs. 13-15.",
     "classification": "author_reported_simulation", "conditions": ["363 K", "284 kPa feed", "Amberlyst-15"],
     "quantities": [q("temperature", 363, "K", "Table 6"), q("volume", 41, "m3", "Table 6"), q("butanol conversion per pass", 69.8, "%", "text p.11; streams 3 and 4")],
     "limits": [SIM, "Units of the rate law and the catalyst loading are not printed; the bed length (~2.5 m for 69.8 %) and Figures 12 and 14 (to 14 m) do not give the diameter."],
     "legacy_origin": None, "keys": {"problem_ids": ["rxn-butanol-esterification-fixed-bed"], "components": ["1-butanol", "acetic-acid", "n-butyl-acetate", "water"], "behaviours": ["equilibrium-limited-reaction", "exothermic-reaction"]}},
    {"id": f"{CASE}.ev-ester-column", "block_ids": B("p7-fig9", "p11-plant", "p12-plant", "table7"),
     "claim": "T-101 takes the reactor effluent (304 kPa) and gives butyl acetate as bottoms (99.9 kmol/h ester with 1.0 acid and 0.1 butanol, 444.9 K, 324 kPa) and acid, butanol and all the water overhead as a vapour distillate (411.1 K, 284 kPa).",
     "classification": "author_reported_simulation", "conditions": ["284 kPa top", "324 kPa bottoms"],
     "quantities": [q("ester in bottoms", 99.9, "kmol/h", "stream 6"), q("acid in bottoms", 1.0, "kmol/h", "stream 6"), q("bottoms temperature", 444.9, "K", "stream 6")],
     "limits": [SIM, "Stages, feed stage, reflux and condenser type of T-101 are not printed; the reason for the pressure is stated only for the membrane route's T-101 (Figure 9, p.7)."],
     "legacy_origin": None, "keys": {"problem_ids": ["sep-ester-from-close-boiling-acid-alcohol"], "components": ["1-butanol", "acetic-acid", "n-butyl-acetate", "water"], "behaviours": ["close-boiling", "azeotrope-min-boiling", "associating-acid-vapour", "trace-impurity-limit"]}},
    {"id": f"{CASE}.ev-extractive", "block_ids": B("p3-azeotrope", "p12-plant", "table7"),
     "claim": "The T-101 distillate (99.9 water, 43.1 butanol, 41.8 acid, 0.9 ester kmol/h) is separated in a 29-stage extractive column with 440.3 kmol/h of 1,4-butanediol fed at the top: water overhead (99.9 kmol/h with 0.1 butanol and 0.4 solvent), the rest with the solvent to a recovery column at 132-142 kPa whose bottoms (512.2 K) return the solvent.",
     "classification": "author_reported_simulation", "conditions": ["29 stages", "111-142 kPa"],
     "quantities": [q("solvent flow", 440.3, "kmol/h", "stream 9"), q("water overhead", 99.9, "kmol/h", "stream 10"), q("recovery column bottoms temperature", 512.2, "K", "stream 13")],
     "limits": [SIM, "T-103 stages and reflux not printed; the text says the solvent returns to T-101, Figure 11 draws it to T-102.", "Stream 9 is printed at 507.0 K although it is mixed from streams at 298.2 and 303.2 K."],
     "legacy_origin": None, "keys": {"problem_ids": ["sep-alcohol-water-azeotrope-heavy-solvent"], "components": ["water", "1-butanol", "acetic-acid", "bdo"], "behaviours": ["azeotrope-min-boiling", "azeotrope-heterogeneous", "associating-acid-vapour"]}},
    {"id": f"{CASE}.ev-recycles", "block_ids": B("p11-plant", "p12-plant", "table7", "p16-utilities"),
     "claim": "Two recycles: acid + butanol (85.7 kmol/h, stream 12) back to the feed vessel, and 1,4-butanediol (439.9 kmol/h, 4.4 mol per mol of ester) back to the extractive column with 0.4 kmol/h make-up equal to the solvent lost in the wastewater. Bottoms of T-102 (462.6 K) and T-103 (512.2 K) are hotter than the medium-pressure steam named (448 K).",
     "classification": "author_reported_simulation", "conditions": ["MP steam 448 K"],
     "quantities": [q("reactant recycle", 85.7, "kmol/h", "stream 12"), q("solvent recycle", 439.9, "kmol/h", "stream 14"), q("solvent make-up", 0.4, "kmol/h", "stream 8; 0.375 on Figure 11")],
     "limits": [SIM, "The stream table's enthalpy of stream 3 (V-101 outlet) equals that of the fresh feeds alone, and its temperature is theirs, although it contains the recycle."],
     "legacy_origin": None, "keys": {"problem_ids": ["plant-solvent-recycle-hot-bottoms"], "components": ["1-butanol", "acetic-acid", "bdo", "water"], "behaviours": ["recycle-loop", "purge-and-make-up"]}},
    {"id": f"{CASE}.ev-product-grade", "block_ids": B("p1-uses", "table7", "eastman-spec"),
     "claim": "The paper's product (stream 7) holds 99.42 wt % ester, 0.52 wt % acetic acid and 0.06 wt % butanol (Lab's arithmetic on Table 7) for solvent uses (coatings, adhesives, pharmaceuticals, flavours); a supplier's sales specification for butyl acetate asks 99.50 % min ester and 0.0100 % max acid as acetic.",
     "classification": "lab_inference", "conditions": ["mass basis"],
     "quantities": [q("ester in product", 99.42, "wt %", "stream 7, derived"), q("acid in product", 0.52, "wt %", "stream 7, derived"), q("ester, sales specification", 99.5, "%", "Eastman 56-12", "lower_bound"), q("acid as acetic, sales specification", 0.01, "%", "Eastman 56-12", "upper_bound")],
     "limits": ["The paper names no grade or customer; the specification is one supplier's (2008), not a standard. ASTM D4615 exists but was not read (paywalled)."],
     "legacy_origin": None, "keys": {"problem_ids": ["sep-ester-from-close-boiling-acid-alcohol"], "components": ["n-butyl-acetate", "acetic-acid", "1-butanol"], "behaviours": ["trace-impurity-limit"]}},
]

FOUR = ["acetic-acid", "1-butanol", "n-butyl-acetate", "water"]


def dec(key, ev, problem, level, op, comps, beh, cond, status, basis, plain, obstacle, mech, operation, change, alts, limits, rc, informed=None):
    keys = {"record_status": "draft", "kind": "case-decision", "problem_id": problem, "level": level, "operation_type": op, "components": comps,
            "behaviours": beh, "conditions": cond, "outcome": {"status": status, "basis": basis, "run_ids": [], "engine": None}, "plain": plain}
    if informed:
        keys["informed_by"] = [{"row": r, "helped": h, "note": n + JUDGED} for r, h, n in informed]
    return {"id": f"{CASE}.{key}", "evidence_ids": [f"{CASE}.{e}" for e in ev], "keys": keys, "obstacle": obstacle, "mechanism": mech,
            "operation": operation, "expected_change": change, "alternatives": alts, "limits": limits + [DRAFT], "verification_required": [],
            "rationale_classification": rc, "legacy_origin": None}


def P(title, when, do, why, check, note):
    return {"title": title, "when": when, "do": do, "why": why, "check": check, "note": note}


decisions = [
    # what the paper did
    dec("paper-fixed-bed-resin-363k", ["ev-reactor"], "rxn-butanol-esterification-fixed-bed", "reaction", "pfr", FOUR,
        ["equilibrium-limited-reaction", "exothermic-reaction"], ["al-rabiah-2022-conventional", "363-k", "1-to-1-feed", "amberlyst-15"], "worked", "paper_simulation",
        P("Butanol esterification: fixed bed of acid resin at 363 K with a 1:1 feed, about 70 % conversion per pass",
          "n-Butanol and acetic acid react to butyl acetate and water on a solid acid; the equilibrium limits one pass.",
          "Run a liquid fixed bed of Amberlyst-15 at 363 K and 1:1 (Table 6) and recycle the unreacted acid and butanol (Al-Rabiah et al. 2022).",
          "The reaction reaches about 70 % within a short bed; the remaining reactants are recovered downstream (p.11).",
          "Butanol 143.1 to 43.2 kmol/h, ester 0.9 to 100.8 kmol/h across the reactor (Table 7, streams 3 and 4).",
          "Numbers: Table 6 p.12 (Amberlyst-15, 363 K, 1:1, 284 kPa, 41 m3); p.11 (maximum about 70 %, 69.8 % within about 2.5 m); Table 7 streams 3 and 4 (butanol 143.1 to 43.2 kmol/h, ester 0.9 to 100.8 kmol/h)."),
        "Equilibrium-limited esterification.", "Kinetic fixed bed near equilibrium, unreacted reactants recycled.", "Aspen RPlug with Eqs. 13-15 (p.11).",
        "69.8 % butanol conversion per pass.", ["Membrane reactor removing water (same paper, 92.0 %)", "Reactive distillation with a decanter (same paper, >98 %)"],
        ["Why 363 K was chosen is not stated; Figure 13's kinetic curve peaks near 370-375 K (read from the figure).", "The kinetic law's units are not printed."], "author_stated"),
    dec("paper-ester-bottoms-at-pressure", ["ev-ester-column"], "sep-ester-from-close-boiling-acid-alcohol", "separation", "distillation", FOUR,
        ["close-boiling", "azeotrope-min-boiling", "associating-acid-vapour", "trace-impurity-limit"], ["al-rabiah-2022-conventional", "284-324-kpa"], "worked", "paper_simulation",
        P("Ester from its reactants: one column at about 300 kPa, ester as bottoms, acid, butanol and water overhead",
          "The reactor effluent holds butyl acetate (Tb 399 K) with close-boiling acetic acid (391 K) and butanol (391 K) and water.",
          "Take the ester as bottoms of T-101 at 284/324 kPa and everything else overhead as a vapour (Table 7).",
          "For their membrane route Al-Rabiah et al. 2022 say butanol and ester form an azeotrope at 1 atm and separate at 304 kPa (p.7); for the conventional T-101 they print no reason.",
          "Bottoms 99.9 ester, 1.0 acid, 0.1 butanol kmol/h at 444.9 K (stream 6).",
          "Numbers: Table 7 streams 4-6 (T-101 284/324 kPa; bottoms 99.9 ester, 1.0 acid, 0.1 butanol kmol/h, 444.9 K); p.7 (azeotrope at 1 atm, split at 304, about 300 kPa); boiling points 399, 391, 391 K rounded from chepta 0.6.3 components.json."),
        "Close-boiling reactants and a butanol-ester azeotrope.", "Pressure shifts the azeotrope; the ester is the heaviest.", "T-101, stages not printed.",
        "Ester 98.91 mol % (derived).", ["Reactive distillation (same paper)"], ["The acid left in the bottoms (1.0 kmol/h) sets the purity."], "mixed_explicitly_separated"),
    dec("paper-extractive-butanediol", ["ev-extractive"], "sep-alcohol-water-azeotrope-heavy-solvent", "separation", "extractive-distillation",
        ["water", "1-butanol", "acetic-acid", "bdo"], ["azeotrope-min-boiling", "azeotrope-heterogeneous", "associating-acid-vapour"], ["al-rabiah-2022-conventional", "29-stages", "solvent-to-feed-2.4"],
        "worked", "paper_simulation",
        P("Butanol-water azeotrope with acetic acid present: extractive distillation with 1,4-butanediol, then solvent recovery",
          "Water must leave a mixture of water, n-butanol and acetic acid, where butanol and water form an azeotrope (91.6 C at 101.3 kPa, Aspen).",
          "Feed 1,4-butanediol at the top of a 29-stage column (about 2.4 mol per mol of feed), take water overhead, recover the solvent in a second column and recycle the acid and butanol (Al-Rabiah et al. 2022, after Shen et al.).",
          "The heavy diol holds butanol and acid in the liquid; Al-Rabiah et al. 2022 follow an earlier design by Shen et al. (p.3).",
          "Water 99.9 kmol/h overhead with 0.1 butanol and 0.4 solvent (stream 10).",
          "Numbers: p.3 (azeotrope 91.6 C at 101.3 kPa, Aspen; 1,4-butanediol after Shen et al., ref. 20); p.12 (29 stages); Table 7 streams 5, 9-14 (solvent 440.3 kmol/h against 185.7 kmol/h feed, about 2.4 mol per mol; stream 10 water 99.9, butanol 0.1, solvent 0.4 kmol/h)."),
        "Minimum-boiling butanol-water azeotrope.", "A heavy polar solvent changes the relative volatility.", "T-102 extractive column and T-103 recovery column.",
        "Wastewater with 0.1 butanol and 0.4 solvent kmol/h.", ["Decanter on the heterogeneous azeotrope (used in the same paper's reactive distillation route)", "Membrane reactor (same paper)"],
        ["Why a decanter was not used here is not stated."], "author_stated"),
    dec("paper-two-recycles-hot-bottoms", ["ev-recycles"], "plant-solvent-recycle-hot-bottoms", "plant", "recycle",
        ["1-butanol", "acetic-acid", "bdo", "water"], ["recycle-loop", "purge-and-make-up"], ["al-rabiah-2022-conventional", "mp-steam-448-k"], "worked", "paper_simulation",
        P("Two recycles (reactants 85.7, solvent 440 kmol/h) and recovery-column bottoms at 512 K",
          "The plant recycles unreacted acid and butanol to the feed vessel and 1,4-butanediol to the extractive column.",
          "Close both loops; make up the solvent lost in the wastewater (0.4 kmol/h, stream 8).",
          "Unreacted reactants and the solvent are worth recovering (p.12).",
          "Recycle 12 = 85.7 kmol/h, solvent 14 = 439.9 kmol/h, make-up 0.4 kmol/h (Table 7); T-103 bottoms 512.2 K against MP steam at 448 K (p.16).",
          "Numbers: Table 7 (stream 12 85.7 kmol/h; stream 14 439.9, about 440 kmol/h; stream 8 0.4 kmol/h; stream 13 at 512.2 K, about 512 K); Figure 11; p.16 (MP steam 448 K)."),
        "Two recycles and a hot solvent bottoms.", "Recycle and make-up.", "Figure 11 loops.", "Both loops closed in the paper.", [],
        ["Reboilers of T-102 (462.6 K) and T-103 (512.2 K) cannot be heated by the 448 K steam the paper names: not explained."], "author_stated"),
]

# the plan (no run yet)
decisions += [
    dec("plan-property-method-nrtl", ["ev-extractive", "ev-ester-column"], "sep-alcohol-water-azeotrope-heavy-solvent", "separation", "extractive-distillation",
        ["acetic-acid", "1-butanol", "n-butyl-acetate", "water", "bdo"], ["two-liquid-phases", "associating-acid-vapour"], ["property-method", "chepta-0.6.3", "three-pairs-estimated", "planned"],
        "untested", "lab_inference",
        P("Plan: NRTL with an ideal vapour (acid dimer by chemical theory) for the whole plant; butanol + water from the LLE-fitted set",
          "Five polar components at 298-512 K and 111-324 kPa; butanol + water and ester + water form two liquids; acetic acid dimerizes in the vapour.",
          "Use NRTL everywhere with the 1-butanol + water set fitted-lladosa2008; let CHEPTA estimate the three missing pairs (acid + butanol, acid + diol, ester + diol) from Modified UNIFAC 2.0 and record its warning; UNIQUAC as a variant.",
          "An activity model fits these liquids and NRTL can show two liquids; CHEPTA 0.6.3 has fitted NRTL pairs for four of the ten pairs, databank pairs for three and none for three.",
          "Each result lists the pair tiers; CHEPTA's own warning that the NRTL diol + water set predicts a false split below about 323 K is checked at the column temperatures before T-102 is compared.",
          "Numbers: 298-512 K, 111-324 kPa (Table 7); chepta 0.6.3 binaries.json (1-butanol + water set fitted-lladosa2008, fitted to butanol-water liquid-liquid data); known-issues.json (diol + water split to 323.15 K, about 323 K); diol = 1,4-butanediol; column T-102; Modified UNIFAC 2.0."),
        "Pairs missing or of uneven quality.", "One activity model, the best set per pair.", "Property method for the plant.", "A plant that can be judged pair by pair.",
        ["UNIQUAC (variant)", "Wilson (cannot show two liquids)"], ["The paper's NRTL parameters are not printed."], "lab_inference",
        [("pasha-2021-biodiesel-process-design.nrtl-uniquac-polar", "yes", "Chose NRTL for polar liquids with two liquid phases; missing pairs from UNIFAC."),
         ("al-rabiah-2022.nrtl-vlle-for-ester-system", "yes", "The authors' own choice (NRTL for VLLE) agrees with it."),
         ("li-2017-ed-thermo-parameters.check-built-in-parameters", "partly", "Triggered for the diol + water pair, which CHEPTA itself flags; the other built-in pairs are reused, not revalidated (AGENTS.md)."),
         ("palomar-2024-il-process-simulation.validate-predictive-methods", "yes", "The three estimated pairs are the ones to look at against data if a column misses its target.")]),
    dec("plan-reactor-kinetic-then-imposed", ["ev-reactor"], "rxn-butanol-esterification-fixed-bed", "reaction", "pfr", FOUR,
        ["equilibrium-limited-reaction", "exothermic-reaction"], ["chepta-0.6.3", "planned", "isothermal-363-k"], "untested", "lab_inference",
        P("Plan: reactor first as a conversion reactor at 69.8 %, then a kinetic plug flow variant",
          "The rate law of Eqs. 13-15 has no printed units or catalyst loading.",
          "Start the plant with a conversion reactor at 363 K (extent 99.9 kmol/h from Table 7); try CHEPTA's plug flow reactor with Eqs. 13-15 as a variant once a concentration basis is chosen and stated.",
          "The conversion per pass sets only the size of the recycle; an imposed conversion is not a test of the reactor.",
          "Outlet against stream 4; reactor duty reported (Al-Rabiah et al. 2022 print none).",
          "Numbers: Table 6 (363 K); p.11 and Table 7 streams 3-4 (69.8 %; extent 99.9 kmol/h, derived); Eqs. 13-15 p.10; equilibrium constant about 5.0 from kF/kB at 363 K (Lab's arithmetic) against 3.51 (Eq. 4)."),
        "Kinetics without units.", "Impose the conversion.", "Conversion reactor, isothermal.", "Reactor outlet equal to stream 4 by construction.", ["Kinetic plug flow (variant)"],
        ["kF/kB gives an equilibrium constant near 5.0 at 363 K (Lab's arithmetic), against 3.51 in the membrane model."], "lab_inference",
        [("ethyl-acetate-piotrowski-2021.lesson-reactor-conversion-imposed", "yes", "Same situation: take the conversion per pass from the streams and say the reactor is not tested."),
         ("al-rabiah-2022.fixed-bed-conversion-near-70", "yes", "Sets the conversion and the recycle size to check (about 43 kmol/h of each reactant)."),
         ("al-rabiah-2022.kinetic-laws-imply-different-keq", "yes", "A warning for the kinetic variant: its implied equilibrium constant differs from the membrane model's."),
         ("al-rabiah-2022.equilibrium-conversion-falls-with-temperature", "partly", "Supports keeping 363 K; it cannot explain why not lower, which Figure 13 suggests is kinetics.")]),
    dec("plan-ester-column-purity-spec", ["ev-ester-column", "ev-product-grade"], "sep-ester-from-close-boiling-acid-alcohol", "separation", "distillation", FOUR,
        ["close-boiling", "azeotrope-min-boiling", "trace-impurity-limit"], ["chepta-0.6.3", "planned", "284-324-kpa"], "untested", "lab_inference",
        P("Plan: T-101 at the printed pressures, specified by the ester purity of the bottoms, condenser giving a vapour distillate",
          "T-101's stages and reflux are not printed; its distillate is printed as vapour.",
          "Keep 284/324 kPa; start from the membrane route's T-101 (42 stages, feed 21; Table 5) as an assumption; specify the bottoms purity (98.91 mol %) and the ester recovery; scan stages and reflux.",
          "Purities at the column ends matter more than the printed settings; the acid slip (1.0 kmol/h) has no other exit and sets the purity.",
          "Bottoms purity within the declared tolerance; the butanol-ester azeotrope at 101.3 and 300 kPa checked in CHEPTA first.",
          "Numbers: Table 7 streams 4-6 (T-101 at 284/324 kPa; acid 1.0 kmol/h in the bottoms; purity 98.91 mol %, derived); Table 5 p.10 (membrane route T-101: 42 stages, feed stage 21); azeotrope checks at 101.3 and 300 kPa (p.7 gives 304 kPa)."),
        "No column settings printed.", "Specify by purity.", "Rigorous column.", "Bottoms 98.91 mol % ester.", [],
        ["42 stages belongs to the membrane route's column (no water in its feed); an assumption here."], "lab_inference",
        [("al-rabiah-2022.butanol-ester-split-at-pressure", "yes", "Explains the pressure and gives a start for the stages."),
         ("al-rabiah-2022.acid-slip-sets-purity", "yes", "Do not over-purify: the acid slip sets the purity."),
         ("ethyl-acetate-piotrowski-2021.lesson-close-plant-purity-specs", "yes", "Specify by outlet purity, not by the paper's settings."),
         ("al-rabiah-2022.acid-excess-raises-conversion-hurts-purification", "partly", "Explains the near-1:1 feed; the trade-off is left for a later scan.")]),
    dec("plan-extractive-solvent-scan", ["ev-extractive"], "sep-alcohol-water-azeotrope-heavy-solvent", "separation", "extractive-distillation",
        ["water", "1-butanol", "acetic-acid", "bdo"], ["azeotrope-min-boiling", "associating-acid-vapour"], ["chepta-0.6.3", "planned", "29-stages"], "untested", "lab_inference",
        P("Plan: T-102 with 29 stages, solvent at the top, scan the solvent flow and the feed stage; check two liquids in T-101's condensate first",
          "T-102's feed stage, reflux and solvent temperature are not printed (stream 9's 507 K is inconsistent).",
          "Run T-102 on stream 5 and stream 9 with the solvent cooled as drawn (E-102 before M-101); feed stage near 13-14 (Figure 15); scan solvent flow around 440 kmol/h; specify water purity overhead and butanol recovery.",
          "The solvent ratio and its temperature decide whether water leaves pure; a decanter alternative depends on whether the condensate splits with 42 kmol/h acid present.",
          "Stream 10 water 99.5 mol % (0.1 butanol, 0.4 solvent) within the declared tolerance.",
          "Numbers: Table 7 streams 5, 9-11 (440.3, about 440 kmol/h; 507 K; stream 10: 99.9/0.1/0.4 kmol/h, 99.5 mol % water, derived; acid about 42 kmol/h); p.12 (29 stages); Figure 15 (stage 13-14, read); units T-101, T-102, E-102, M-101."),
        "Azeotrope with acid present.", "Heavy solvent.", "Rigorous extractive column.", "Water overhead, solvent and reactants as bottoms.", ["Decanter (to test)"],
        ["The feed stage is read from Figure 15, approximate."], "lab_inference",
        [("al-rabiah-2022.conventional-extractive-with-butanediol", "yes", "Gives the configuration; its two open points (stages, solvent destination) are resolved from Figure 11 here."),
         ("al-rabiah-2022.butanediol-circulation-ratio", "yes", "Sets the solvent scan around 2.4 mol per mol."),
         ("blahusiak-2018-separation-selection.solvent-boiling-gap-and-selectivity", "yes", "The diol boils about 100 K above the mixture (500.5 K against 373-399 K in CHEPTA), so regeneration is easy."),
         ("li-2017-ed-thermo-parameters.extractive-solvent-criteria", "partly", "The relative-volatility check with and without solvent is a cheap first CHEPTA test; the solvent itself is the paper's."),
         ("jankovic-2023-ipa-acetone-recovery.preconcentrate-before-extractive", "no", "Not applicable: the feed is not dilute (54 mol % water).")]),
    dec("plan-recycles-tears", ["ev-recycles"], "plant-solvent-recycle-hot-bottoms", "plant", "recycle",
        ["1-butanol", "acetic-acid", "bdo", "water", "n-butyl-acetate"], ["recycle-loop", "purge-and-make-up"], ["chepta-0.6.3", "planned"], "untested", "lab_inference",
        P("Plan: tear the two recycles (12 and 14), fix the fresh feeds and the solvent circulation, let the make-up follow",
          "Two loops: reactants to V-101, solvent to M-101; Al-Rabiah et al. 2022 fix the fresh feeds.",
          "Close the solvent loop first (T-102 + T-103 + E-102 + M-101), then the reactant loop; tears at 12 and 14; solvent circulation fixed, make-up equal to the loss; Broyden; per-component check; tighten from the saved answer; compare every flow (rule G).",
          "Fixing one flow inside each loop gives the missing specification; an unconsumed acid excess (0.8 kmol/h fresh) must leave with the product.",
          "Recycle 12 within 5 % of 85.7 kmol/h, solvent within 1 % of 440 kmol/h; no flow 10 times larger than in Table 7.",
          "Numbers: Table 7 streams 1, 2, 8, 12, 14 (100.1 butanol, 100.9 acid, 0.8 more; 85.7; 439.9, about 440 kmol/h); tolerances 5 % and 1 % (record.json); rule G (a flow 10 times larger); units T-102, T-103, E-102, M-101, V-101."),
        "Two recycles.", "Tears and fixed flows.", "Closed flowsheet.", "Both loops closed.", [], [], "lab_inference",
        [("larsson-skogestad-2000-plantwide.fix-a-recycle-flow", "yes", "Fix the solvent circulation."),
         ("andreasen-2022-dwsim-evaluation.recycle-tolerance-per-component", "yes", "Check the tears per component (acid and ester traces)."),
         ("ethyl-acetate-piotrowski-2021.lesson-product-flow-within-feed", "yes", "The ester cannot exceed what 100.1 kmol/h butanol forms."),
         ("ethyl-acetate-piotrowski-2021.lesson-tighten-tolerance-from-saved-answer", "yes", "Restart from the saved answer."),
         ("methanol-co2-campos-2022.lesson-tears-break-every-cycle", "yes", "Two cycles here; both tears must be marked."),
         ("larsson-skogestad-2000-plantwide.snowball-means-reactor-too-small", "partly", "Watch the reactant recycle for snowballing (rule G).")]),
    dec("plan-energy-checks", ["ev-recycles"], "plant-solvent-recycle-hot-bottoms", "plant", "heat-exchange",
        ["1-butanol", "acetic-acid", "bdo", "water", "n-butyl-acetate"], ["heat-recovery-potential"], ["chepta-0.6.3", "planned"], "untested", "lab_inference",
        P("Plan: duties from CHEPTA reported against the stream-table differences, not against the printed feed enthalpies",
          "The enthalpies of streams 1, 2 and 3 disagree with CHEPTA's formation-based reference by -142 to -192 kJ/mol; streams 3 and 9 are not adiabatic mixtures.",
          "Compare E-101, E-102 and the column net duties with the Table 7 differences (derived); report the reactor duty and the reboiler temperatures against the 448 K steam; treat Table 10 (27.3 MW steam at 8000 h/yr, derived) as reported only.",
          "Only the enthalpy differences of consistent streams can be compared.",
          "E-101 -998 kW, E-102 -6143 kW, T-102 net -3246 kW, T-103 net +1245 kW (derived).",
          "Numbers: STREAM_AUDIT.md from Table 7 (streams 1, 2, 3, 9; -142, -192 kJ/mol; -998, -6143, -3246, +1245 kW, derived); p.16 (448 K); Table 10 (27.3 MW at 8000 h/yr, derived); units E-101, E-102, T-102, T-103."),
        "Inconsistent enthalpies.", "Compare differences only.", "Energy comparison.", "Duties judged where the paper is consistent.", [], [], "lab_inference",
        [("methanol-co2-campos-2022.lesson-duty-against-stream-enthalpies", "yes", "Same check: a duty against the stream enthalpies around it."),
         ("chen-2018-abe-distillation.lower-pressure-of-sensitive-columns", "partly", "Different trigger, but a lower T-103 pressure is the obvious test of the 512 K bottoms against 448 K steam.")]),
]

doc = {"schema_version": 1, "id": CASE, "groups": [], "blocks": blocks, "evidence": evidence, "decisions": decisions, "runs": [], "tasks": []}
(ROOT / "dataset" / "records" / f"{CASE}.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
print(len(blocks), "blocks,", len(evidence), "evidence,", len(decisions), "decisions")
