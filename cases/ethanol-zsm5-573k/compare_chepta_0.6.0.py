#!/usr/bin/env python3
"""Compare old (c1adf6b) and new (chepta 0.6.0) outputs of the six ethanol runs.
Writes results-chepta-0.6.0/comparison.json. Reads files only; no CHEPTA imports."""
import json
from pathlib import Path
H = Path(__file__).resolve().parent
old_m = json.loads((H/'results/run-manifest.json').read_text())
comps = ['ethanol','ethylene','water','diethyl-ether']

def deep(a, b, path=''):
    """Every leaf difference: (path, old, new). Numbers are compared exactly."""
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a)|set(b)):
            if k not in a: out.append((f'{path}/{k}', '<absent>', b[k]))
            elif k not in b: out.append((f'{path}/{k}', a[k], '<absent>'))
            else: out += deep(a[k], b[k], f'{path}/{k}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): out += deep(x, y, f'{path}[{i}]')
    elif a != b:
        out.append((path, a, b))
    return out

def warnings(o):
    w = set()
    for s in o['value']['streams'].values(): w |= set(s.get('warnings', []))
    for k in ('warnings',):
        w |= set(o.get(k) or [])
    w |= set(o.get('qualifications', {}).get('warnings', []))
    return sorted(w)

rows = []
for r in old_m['runs']:
    o = json.loads((H/r['output_file']).read_text())
    n = json.loads((H/f"results-chepta-0.6.0/{r['id']}.output.json").read_text())
    po, pn = o['value']['streams']['product'], n['value']['streams']['product']
    fo = [po['flow_kmol_h'][c]*1000 for c in comps]; fn = [pn['flow_kmol_h'][c]*1000 for c in comps]
    conv = lambda f: 100*(1-f[0]/1.0)
    diffs = [d for d in deep(o, n) if not d[0].startswith(('/run/', '/reproduction/library', '/reproduction/databank_hash'))]
    wo, wn = warnings(o), warnings(n)
    rows.append({'id': r['id'], 'outcome_old': o['outcome'], 'outcome_new': n['outcome'],
      'outlet_mol_h_old': dict(zip(comps, fo)), 'outlet_mol_h_new': dict(zip(comps, fn)),
      'conversion_percent_old': conv(fo), 'conversion_percent_new': conv(fn),
      'duty_kW_old': o['value']['blocks']['R']['duty_kW'], 'duty_kW_new': n['value']['blocks']['R']['duty_kW'],
      'energy_check_kW_old': o['checks']['energy_kW'], 'energy_check_kW_new': n['checks']['energy_kW'],
      'warnings_old': wo, 'warnings_new': wn,
      'warnings_added': sorted(set(wn)-set(wo)), 'warnings_removed': sorted(set(wo)-set(wn)),
      'library_old': o['reproduction']['library'], 'library_new': n['reproduction']['library'],
      'databank_hash_old': o['reproduction']['databank_hash'], 'databank_hash_new': n['reproduction']['databank_hash'],
      'number_of_other_differing_values': len(diffs), 'other_differences': [list(map(str, d)) for d in diffs[:50]]})
(H/'results-chepta-0.6.0/comparison.json').write_text(json.dumps(rows, indent=2)+'\n')
for x in rows:
    print(x['id'], x['outcome_old'], x['outcome_new'], f"conv {x['conversion_percent_old']:.6f} -> {x['conversion_percent_new']:.6f}",
          'duty', x['duty_kW_old'], x['duty_kW_new'], 'diffs', x['number_of_other_differing_values'],
          '+w', len(x['warnings_added']), '-w', len(x['warnings_removed']), 'nwarn', len(x['warnings_old']), len(x['warnings_new']))
