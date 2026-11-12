#!/usr/bin/env python3
"""Re-run the six ethanol requests (the 0.6.0 requests, byte for byte) on the pinned npm package chepta (see /package.json)
through `npx chepta request`. Old requests are copied unchanged; nothing in results/ or results-chepta-0.6.0/ is touched.
Usage (repository root, after `npm ci`): python3 cases/ethanol-zsm5-573k/run_chepta_0.6.1.py"""
import hashlib, json, shutil, subprocess, sys, datetime
from pathlib import Path
H = Path(__file__).resolve().parent
ROOT = H.parents[1]
NEW = H/'results-chepta-0.6.1'; NEW.mkdir(exist_ok=True)
old = json.loads((H/'results-chepta-0.6.0/run-manifest.json').read_text())  # the 0.6.0 runs and their (byte-identical) requests
lock = json.loads((ROOT/'package-lock.json').read_text())['packages']['node_modules/chepta']
sha = lambda b: hashlib.sha256(b).hexdigest()
version = subprocess.run(['npx','chepta','--version'],cwd=ROOT,capture_output=True,text=True).stdout.strip()
if version != '0.6.1' or lock['version'] != '0.6.1':
    sys.exit(f'Expected chepta 0.6.1, found CLI {version} / lock {lock["version"]}')
runs = []
for r in old['runs']:
    id_ = r['id']
    src = H/'results-chepta-0.6.0'/f'{id_}.request.json'; req = NEW/f'{id_}.request.json'
    shutil.copyfile(src, req)  # format unchanged: byte-identical copy
    p = subprocess.run(['npx','chepta','request',str(req.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
    (NEW/f'{id_}.output.json').write_text(p.stdout)
    (NEW/f'{id_}.stderr.txt').write_text(p.stderr)
    outcome = json.loads(p.stdout)['outcome'] if p.stdout.strip() else None
    runs.append({**{k:r[k] for k in ('id','variant','W_over_F_gcat_h_mol','W_kg','L_m')},
      'command': f'npx chepta request cases/ethanol-zsm5-573k/results-chepta-0.6.1/{id_}.request.json',
      'exit_code': p.returncode, 'outcome': outcome,
      'request_changed_from_0.6.0': req.read_bytes() != src.read_bytes(),
      'request_file': f'results-chepta-0.6.1/{id_}.request.json',
      'output_file': f'results-chepta-0.6.1/{id_}.output.json',
      'stderr_file': f'results-chepta-0.6.1/{id_}.stderr.txt',
      'request_file_sha256': sha(req.read_bytes()), 'output_file_sha256': sha(p.stdout.encode())})
manifest = {'executed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'engine': {'package':'chepta','version':version,'resolved':lock['resolved'],'integrity':lock['integrity'],'licence':lock.get('license')},
  'node': subprocess.run(['node','--version'],capture_output=True,text=True).stdout.strip(),
  'npm': subprocess.run(['npm','--version'],capture_output=True,text=True).stdout.strip(),
  'interface': 'command line: npx chepta request <file>; exit codes 0 ok, 2 invalid_input, 3 missing_data, 4 unsupported, 5 not_converged',
  'previous_engine': 'chepta@0.6.0', 'previous_manifest': 'results-chepta-0.6.0/run-manifest.json (unchanged)',
  'input_sha256': old['input_sha256'], 'runs': runs}
(NEW/'run-manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
for r in runs: print(r['id'], 'exit', r['exit_code'], r['outcome'], 'request changed:', r['request_changed_from_0.6.0'])
sys.exit(1 if any(r['exit_code'] for r in runs) else 0)
