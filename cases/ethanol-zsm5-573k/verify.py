#!/usr/bin/env python3
"""Independent species-flow ODE in mol/h and grams catalyst; no CHEPTA imports.
Numerical implementation check, not experimental or thermodynamic validation.
"""
import json
import platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
c = json.loads((HERE / 'input.json').read_text())
k = c['constants']
manifest = json.loads((HERE / 'results/run-manifest.json').read_text())
# Columns: ethanol, ethylene, water, diethyl ether. Rows: C, H, O.
atoms = np.array([[2,2,0,4], [6,4,2,10], [1,0,1,1]], dtype=float)
feed = np.array([c['feed_mol_h'],0,0,0], dtype=float)
checks = []
for entry in manifest['runs']:
    full = entry['variant'] == 'table12_adsorption'
    def derivative(W_g, F):
        a,o,w,e = F / sum(F) * c['P_kPa']/101.325
        d1, d2 = 1+k['KA1']*a, 1+k['KA2']*a
        if full:
            d1 += k['KE1']*e+k['KW1']*w
            d2 += k['KE2']*e+k['KW2']*w+k['KO2']*o
        r1 = k['k1']*(a-o*w/k['Keq1'])/d1
        r2 = k['k2']*k['KA2']**2*(a*a-w*e/k['Keq2'])/d2**2
        return [-r1-2*r2, r1, r1+r2, r2]
    ref = solve_ivp(derivative, (0,entry['W_kg']*1000), feed, method='DOP853', rtol=1e-11, atol=1e-13)
    if not ref.success:
        raise RuntimeError(ref.message)
    out = json.loads((HERE / entry['output_file']).read_text())
    if out['outcome'] != 'ok':
        raise RuntimeError(f"Failed CHEPTA run: {entry['id']}")
    streams = out['value']['streams']
    calc = np.array([streams['product']['flow_kmol_h'][s]*1000 for s in c['components']])
    expected = ref.y[:,-1]
    rel = np.abs(calc-expected)/np.maximum(np.abs(expected),1e-12)
    elemental_relative = np.abs(atoms @ (calc-feed))/(atoms@feed)
    mass_relative = abs(streams['product']['mass_kg_h']/streams['feed']['mass_kg_h']-1)
    energy = abs(out['checks']['energy_kW'])
    inlet = derivative(0,feed)
    profile = out['value']['blocks']['R']['reaction']['kinetic']['profile']
    rate_error = max(abs(profile[0]['rates'][0]*3.6-inlet[1]), abs(profile[0]['rates'][1]*3.6-inlet[3]))
    passed = bool(np.all(rel < 1e-5) and np.all(elemental_relative < 1e-10)
                  and mass_relative < 1e-6 and energy < 1e-10 and rate_error < 1e-12
                  and np.all(calc >= 0) and 0 <= 1-calc[0]/feed[0] <= 1
                  and streams['product']['VF'] == 1)
    checks.append({'id':entry['id'],'passed':passed,
      'CHEPTA_outlet_mol_h':dict(zip(c['components'],calc.tolist())),
      'reference_outlet_mol_h':dict(zip(c['components'],expected.tolist())),
      'conversion_percent':float(100*(1-calc[0]/feed[0])),
      'ethylene_yield_mol_per_mol_feed':float(calc[1]/feed[0]),
      'ethylene_selectivity_ethanol_equivalent':float(calc[1]/(feed[0]-calc[0])),
      'max_component_relative_error':float(max(rel)),
      'max_element_relative_residual':float(max(elemental_relative)),
      'mass_relative_residual':mass_relative,'internal_energy_residual_kW':energy,
      'inlet_rate_max_abs_error_mol_gcat_h':rate_error,
      'stream_warnings':sorted(set(w for s in streams.values() for w in s.get('warnings',[])))})
result={'status':'passed' if all(x['passed'] for x in checks) else 'failed',
  'scope':'Independent numerical implementation; no experimental or independent thermodynamic validation.',
  'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
  'reference_method':'DOP853; mol/h species balances versus grams catalyst',
  'tolerances':{'component_relative':1e-5,'element_relative':1e-10,'mass_relative':1e-6,'internal_energy_kW':1e-10,'inlet_rate_absolute_mol_gcat_h':1e-12},
  'tolerance_rationale':'Component tolerance matches the upstream benchmark; tighter reference integration isolates solver error. Exact stoichiometry checks elements. Mass tolerance allows rounded databank molecular weights. Energy checks internal closure only.',
  'checks':checks}
(HERE / 'results/verification.json').write_text(json.dumps(result,indent=2)+'\n')
for r in checks:
    print(f"{r['id']}: conversion={r['conversion_percent']:.8f}%, max relative error={r['max_component_relative_error']:.3g}, passed={r['passed']}")
if result['status'] != 'passed':
    raise SystemExit(1)
