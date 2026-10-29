"""Audit rounded published streams, without normalization or simulator execution."""
import json
from pathlib import Path
R=Path(__file__).resolve().parent
source=json.loads((R/'streams.json').read_text());equipment=json.loads((R/'equipment.json').read_text())['equipment']
names=['ethanol','water','ethyl_acetate','acetic_acid']
# Consistent atomic weights (g/mol); used only for derived atom balances and molar checks.
atoms=[[2,6,1],[0,2,1],[4,8,2],[2,4,2]];aw=[12.011,1.008,15.999]
mw=[sum(a*b for a,b in zip(row,aw)) for row in atoms]
report={'method':'out minus in; original mass fractions retained, not renormalized','rounding_model':'Nearest rounding assumed: mass flow +/-0.5 kg/h, mass percentage +/-0.005 percentage points. Bounds are conservative triangle sums, not statistical uncertainty or proof of accuracy.','atomic_weights_g_mol':dict(zip(['C','H','O'],aw)),'strategies':{}}
for strategy,rows in source['strategies'].items():
 d={int(x['stream']):x for x in rows}
 def comp(s,j):return d[s]['mass_kg_h']*d[s][names[j]+'_mass_pct']/100
 def err(s,j):return .5*d[s][names[j]+'_mass_pct']/100+d[s]['mass_kg_h']*.00005+.5*.00005
 checks=[]
 for e in equipment+[{'id':'plant','type':'reactive boundary','inlets':[1,2,17],'outlets':[16,25]}]:
  ins,outs=e['inlets'],e['outlets'];ss=ins+outs
  delta=sum(d[i]['mass_kg_h'] for i in outs)-sum(d[i]['mass_kg_h'] for i in ins)
  residual=[sum(comp(i,j) for i in outs)-sum(comp(i,j) for i in ins) for j in range(4)]
  cb=[sum(err(i,j) for i in ss) for j in range(4)]
  ar=[sum(residual[j]/mw[j]*atoms[j][a] for j in range(4)) for a in range(3)]
  ab=[sum(cb[j]/mw[j]*atoms[j][a] for j in range(4)) for a in range(3)]
  reactive=e['id'] in [4,'plant']
  passed=abs(delta)<=len(ss)*.5+1e-8 and all(abs(x)<=b+1e-8 for x,b in zip(ar,ab)) and (reactive or all(abs(x)<=b+1e-8 for x,b in zip(residual,cb)))
  checks.append({'block':e['id'],'inlets':ins,'outlets':outs,'reactive':reactive,'mass_residual_kg_h':delta,'mass_rounding_bound_kg_h':len(ss)*.5,'component_residual_kg_h':dict(zip(names,residual)),'component_rounding_bounds_kg_h':dict(zip(names,cb)),'atom_residual_kmol_atoms_h':dict(zip(['C','H','O'],ar)),'atom_rounding_bounds':dict(zip(['C','H','O'],ab)),'within_rounding_envelope':passed})
 stream_checks=[]
 for s,x in d.items():
  calc=sum(comp(s,j)/mw[j] for j in range(4));bound=sum(err(s,j)/mw[j] for j in range(4))+.05
  stream_checks.append({'stream':s,'mass_percent_sum':sum(x[n+'_mass_pct'] for n in names),'derived_kmol_h':calc,'reported_kmol_h':x['molar_kmol_h'],'difference_kmol_h':calc-x['molar_kmol_h'],'rounding_bound_kmol_h':bound,'within_rounding_envelope':abs(calc-x['molar_kmol_h'])<=bound})
 report['strategies'][strategy]={'balances':checks,'streams':stream_checks}
(R/'balance-results.json').write_text(json.dumps(report,indent=2)+'\n')
lines=['# Stream and equipment audit','', 'Piotrowski and Kubica (2021), DOI 10.3390/pr9081425, CC BY 4.0. Tables A1/A2 (pp.13–14), Table 1 (p.11), Figure 1 (p.4). Source values are reported simulations, not measurements or CHEPTA results. All 28 streams per strategy are in [streams.json](streams.json). All 19 blocks and available settings are in [equipment.json](equipment.json).','', 'Run `python comparisons/ethyl-acetate/audit_balances.py` from the repository root. No third-party Python packages required. Raw numbers are preserved; no balancing corrections or composition normalization are applied.','', '## Balance results','', 'Residuals below are outlet minus inlet. The envelope assumes nearest rounding at the printed precision; an exceeded envelope is an unresolved inconsistency, not proof of which entry is wrong. Reactive boundaries are checked by mass and atoms, not conservation of each reacting species.','', '| Strategy | Boundary | Mass residual kg/h | Within mass/component/atom rounding envelopes |','|---|---|---:|---|']
for s,r in report['strategies'].items():
 for b in r['balances']:lines.append(f"| {s} | {b['block']} | {b['mass_residual_kg_h']:.3f} | {'Yes' if b['within_rounding_envelope'] else 'No'} |")
lines+=['','Full residuals and bounds: [balance-results.json](balance-results.json). Atom weights and stream molar-flow consistency checks are recorded there. Nominally zero source fractions may hide trace components; no catalyst stream is represented. The external boundary assumes feeds 1, 2, 17 and products 16, 25 shown in Figure 1.','', '## Selected equipment','', '| Block | Function | Inlet streams | Outlet streams |','|---|---|---|---|']
for e in equipment:lines.append(f"| {e['id']} | {e['type']} | {e['inlets']} | {e['outlets']} |")
lines+=['', 'Table 1 specifies a 300 m3 reactor-evaporator, 85–90 °C; columns 5/11/15 have 8/35/18 stages and feed stages 8/15/9. Column 5 uses R/V=0.62 (S1), 0.61 (S2); columns 11/15 use R/D=3/2 in both. Seven heater/cooler blocks have reported duties. These are published selections, not new equipment sizing or procurement recommendations. Block 14 is retained as an unidentified transfer block rather than assigned an unsupported equipment type.','', '## Discrepancies and remaining specifications','', '- Table 1 column 5 has 8 stages; Section 3.2 says at least 14. The selected product-column feed stage 15 also differs from the discussion of stages 4–6. Stage numbering or design revision requires clarification.','- Table 1 extractor temperatures 30/70 °C match feed conditioning, while organic outlet temperatures are 21/27 °C and aqueous outlets 24/41 °C. Do not impose Table 1 as an isothermal extractor temperature without resolving this.','- Table A1 stream 28 differs slightly from stream 20 across a heater; preserve the discrepancy. The balance calculation determines whether printed rounding explains it.','- Product water limits and energy-table inconsistencies from the comparison README remain unresolved. Neither strategy is accepted as a compliant design.','- Missing: catalyst loading/rate definitions, full property parameters, extractor stage model, column efficiencies/internals/diameters, utility temperatures, exchanger areas/U, pressure drops and mechanical specifications. A flowsheet symbol is not a complete equipment specification.','- Next: resolve failed balance rows against the original Chemcad files or author clarification before generating executable training targets. Do not tune a simulator to compensate for conflicting stream entries.','', 'Engineering review: pending. Training eligibility: false. This audit checks published data, not a new process simulation.']
(R/'STREAM_EQUIPMENT_AUDIT.md').write_text('\n'.join(lines)+'\n')
for s,r in report['strategies'].items():
 print(s,'balance exceptions',[(b['block'],round(b['mass_residual_kg_h'],3)) for b in r['balances'] if not b['within_rounding_envelope']]);print('molar exceptions',[(x['stream'],round(x['difference_kmol_h'],3)) for x in r['streams'] if not x['within_rounding_envelope']])
