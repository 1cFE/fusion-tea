"""WI-092 development checks against the rebuilt package: mode-0 exact replay, mode-1 network, split pair, refusals.

Writes development-cases.json and migration-report.json into --evidence. Native execution only; no plant arithmetic.
"""
import argparse, json, sys, math
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'exploration/aries_integrated'))
import run as runner  # noqa: E402
P = runner.PREFIX
NEW_KEYS = {P + 'heat_exchangers__network_mode': 0.0, P + 'heat_exchangers__pbli_split_fraction': 0.85}
SEALED = ROOT / 'exploration/aries_integrated/studies/20260925-aries-reference-heat-electricity-reconciliation/results/cases.json'
FROZEN14 = ROOT / 'exploration/aries_integrated/studies/20260922-integrated-heat-electricity/results/cases.json'
parser = argparse.ArgumentParser(); parser.add_argument('--root', type=Path, required=True); parser.add_argument('--evidence', type=Path, required=True)
args = parser.parse_args(); args.root.mkdir(parents=True, exist_ok=True); args.evidence.mkdir(parents=True, exist_ok=True)
runtime = runner.load_runtime()
sealed = {c['case']: c for c in json.load(open(SEALED))['cases']}
entry_keys = set(json.loads((runner.PACKAGE / 'pipelines' / 'pipeline.yaml').read_text()) and []) if False else None
rows, migration = [], {'new_public_keys': NEW_KEYS, 'removed_public_keys': [], 'mode0_replays': []}

def execute(name, point_changes, note):
    row = runner.execute_case(name, point_changes, runtime, root=args.root)
    rows.append({'case': name, 'note': note, 'status': row['status'], 'changes': point_changes,
                 **({'error': row['error']} if row['status'] != 'evaluated' else {'outputs': row['outputs']}),
                 'effective_inputs': row['effective_inputs'], 'fingerprint': row['fingerprint']})
    return row

def compare(name, row, reference):
    ro = reference['outputs']; out = row['outputs']
    numeric = [k for k in ro if isinstance(ro[k], (int, float)) and not isinstance(ro[k], bool)]
    worst = 0.; bad = []
    for k in numeric:
        a, b = ro[k], out.get(k)
        if b is None: bad.append((k, 'missing')); continue
        rel = abs(a - b) / max(1e-300, abs(a)) if a != 0 else abs(b)
        worst = max(worst, rel)
        if rel > 1e-12: bad.append((k, a, b))
    rv = reference.get('verdicts') or {}
    native = {x['constraint_id']: x['status'] for x in out.get('constraint_report', {}).get('results', [])}
    verdicts_equal = (set(native) == set(rv) and all(native[k] == v for k, v in rv.items())) if rv else None
    migration['mode0_replays'].append({'case': name, 'numeric_channels': len(numeric), 'worst_relative': worst, 'exact_count': sum(ro[k] == out.get(k) for k in numeric),
                                       'mismatches': bad[:10], 'verdicts_equal': verdicts_equal, 'new_channels': len([k for k in out if k not in ro])})

# (a) mode-0 replay of the 27 sealed points (their full maps plus the two new keys at defaults)
for name, case in sealed.items():
    changes = {k: v for k, v in case['inputs'].items()} | NEW_KEYS
    row = execute('replay-' + name, changes, 'mode-0 replay of sealed point')
    if row['status'] == 'evaluated': compare('replay-' + name, row, case)
# (b) mode-1 at C3 inputs, split sweep incl. insufficient/sufficient pair, and at the original inputs
c3 = dict(sealed['combined-c3-partition']['inputs'])
for s in (0.55, 0.7, 0.8, 0.85, 0.9, 0.98):
    execute(f'network-c3-split-{s}', c3 | {P + 'heat_exchangers__network_mode': 1.0, P + 'heat_exchangers__pbli_split_fraction': s}, 'mode-1 network at C3 inputs')
orig = dict(sealed['nominal-source-assumed']['inputs'])
execute('network-original-split-0.85', orig | {P + 'heat_exchangers__network_mode': 1.0, P + 'heat_exchangers__pbli_split_fraction': 0.85}, 'mode-1 network at the original failing inputs')
c3_1800 = c3 | {P + 'cycle__selected_flow': 1800.0, P + 'heat_exchangers__network_mode': 1.0, P + 'heat_exchangers__pbli_split_fraction': 0.85}
execute('network-c3-1800', c3_1800, 'mode-1 at 1800 kg/s (compressor rating A6 expected exceeded)')
execute('network-c3-1800-rating-1800', c3_1800 | {P + 'compressor_capacity__selected_rating': 1800.0}, 'declared resized compressor alternative')
# (c) refusals
for name, ch in (('refuse-split-0', {P + 'heat_exchangers__pbli_split_fraction': 0.0, P + 'heat_exchangers__network_mode': 1.0}),
                 ('refuse-split-1', {P + 'heat_exchangers__pbli_split_fraction': 1.0, P + 'heat_exchangers__network_mode': 1.0}),
                 ('refuse-mode-2', {P + 'heat_exchangers__network_mode': 2.0})):
    execute(name, c3 | ch, 'expected domain refusal')
# (d) zero-UA definedness in mode 1 (divertor area 0 -> UA 0)
execute('network-c3-zero-divertor-area', c3 | {P + 'heat_exchangers__network_mode': 1.0, P + 'divertor_hx__selected_area': 0.0}, 'mode-1 zero divertor UA definedness')
(args.evidence / 'development-cases.json').write_text(json.dumps(rows, indent=1) + '\n')
(args.evidence / 'migration-report.json').write_text(json.dumps(migration, indent=1) + '\n')
summary = {'cases': len(rows), 'evaluated': sum(r['status'] == 'evaluated' for r in rows), 'refused': sum(r['status'] != 'evaluated' for r in rows),
           'mode0_worst_relative': max((m['worst_relative'] for m in migration['mode0_replays']), default=None),
           'mode0_all_verdicts_equal': all(m['verdicts_equal'] in (True, None) for m in migration['mode0_replays']),
           'mode0_replays': len(migration['mode0_replays'])}
print(json.dumps(summary, indent=1))
for r in rows:
    if r['status'] == 'evaluated' and not r['case'].startswith('replay-'):
        o = r['outputs']; g = lambda k: o.get(P + k, float('nan'))
        print('%-36s Tt %8.2f unmet %8.2f (he %6.2f pbli %6.2f div %6.2f) gross %8.2f net %8.2f' % (r['case'], g('heat_exchangers__evaluate__turbine_temperature'), g('heat_exchangers__evaluate__unmet_heat'), g('heat_exchangers__evaluate__he_unmet'), g('heat_exchangers__evaluate__pbli_unmet'), g('heat_exchangers__evaluate__divertor_unmet'), g('plant_ledger__evaluate__gross_electric'), g('plant_ledger__evaluate__net_electric')))
    elif r['status'] != 'evaluated':
        print('%-36s REFUSED: %s' % (r['case'], r['error'][:100]))
