"""Shared by the per-case compare_chepta_0.6.2.py scripts: 0.6.1 against 0.6.2 for every run of a case."""
import json
IGNORE = ('/run/', '/reproduction/library')

def deep(a, b, path=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: out.append((f'{path}/{k}', '<absent>', b[k]))
            elif k not in b: out.append((f'{path}/{k}', a[k], '<absent>'))
            else: out += deep(a[k], b[k], f'{path}/{k}')
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): out += deep(x, y, f'{path}[{i}]')
    elif a != b:
        out.append((path, a, b))
    return out

def find(o, key, path=''):
    out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key: out.append((path + '/' + k, v))
            out += find(v, key, path + '/' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o): out += find(v, key, f'{path}[{i}]')
    return out

def compare(H):
    new_m = json.loads((H / 'results-chepta-0.6.2/run-manifest.json').read_text())
    rows = []
    for r in new_m['runs']:
        o = json.loads((H / f"results-chepta-0.6.1/{r['id']}.output.json").read_text())
        n = json.loads((H / f"results-chepta-0.6.2/{r['id']}.output.json").read_text())
        diffs = [d for d in deep(o, n) if not d[0].startswith(IGNORE)]
        ex = [x for p, v in find(n, 'extrapolations') for x in v]
        ep = [x for key in ('estimatedPairs', 'estimated_pairs') for p, v in find(n, key) for x in v]
        rows.append({'id': r['id'], 'outcome_old': o['outcome'], 'outcome_new': n['outcome'],
                     'error_old': o.get('error'), 'error_new': n.get('error'),
                     'identical_except_run_block_and_library_label': not diffs,
                     'number_of_differing_values': len(diffs),
                     'differences': [[d[0], str(d[1])[:400], str(d[2])[:400]] for d in diffs[:40]],
                     'extrapolations_new': [x.get('message') or x.get('short') for x in ex],
                     'estimated_pairs_new': ep,
                     'estimated_pairs_field_present': bool(find(n, 'estimatedPairs') or find(n, 'estimated_pairs'))})
    (H / 'results-chepta-0.6.2/comparison.json').write_text(json.dumps(rows, indent=2) + '\n')
    for x in rows:
        print(x['id'], x['outcome_old'], '->', x['outcome_new'], 'identical' if x['identical_except_run_block_and_library_label'] else f"{x['number_of_differing_values']} differences",
              'extrapolations', len(x['extrapolations_new']), 'estimated', len(x['estimated_pairs_new']))
