"""Independent oracle scan and diagnostic edges before fixing the native sample."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry as oe, study_route as route
from scripts.study.verify import derive_verdict, package_input_values

H = Path(__file__).resolve().parents[1]
R = H / 'results'
P = route.P
read = lambda path: json.loads(path.read_text())


def write(name, value):
    (R / name).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


assert read(R / 'preflight_results.json')['outcome'] == 'pass'
params = package_input_values(route.PACKAGE_DIR)
catalog = route._catalog_by_constraint_id(route.PACKAGE_DIR)
bindings = oe.operand_bindings()
fit = next(cid for cid, row in catalog.items() if row['source_local_identity'] == 'wp_fit_ok')
expected = read(H / 'preparation/expected-fit-interface.json')
rows = read(H / 'preparation/unique-proposals.json')


def evaluate(point):
    channels = oe.evaluate(point)
    assert len(channels) == expected['expected_oracle_mapped_outputs']
    verdicts = {cid: ('satisfied' if derive_verdict(cid, entry, bindings, point, params, channels)[0]
                     else 'violated') for cid, entry in catalog.items()}
    return {'channels': channels, 'verdicts': verdicts,
            'feasible_18': all(v == 'satisfied' for cid, v in verdicts.items() if cid != fit),
            'fit_satisfied': verdicts[fit] == 'satisfied',
            'full_satisfied': all(v == 'satisfied' for v in verdicts.values())}


out = [row | evaluate(row['point']) for row in rows]
write('oracle-scan.json', {'scope': 'Independent candidate oracle scan before native sample; not native execution',
                         'rows': out, 'feasible_18': sum(r['feasible_18'] for r in out),
                         'feasible_19': sum(r['full_satisfied'] for r in out)})
feasible = [row for row in out if row['full_satisfied']]
anchor = next((row for row in feasible if row['point'][P + 'magnet__winding_pack__j_wp'] == params[P + 'magnet__winding_pack__j_wp']), None)
anchor = anchor or (feasible[0] if feasible else next(row for row in out if row['feasible_18']))
edges = []
for group in read(H / 'axes.json')['groups']:
    keys = [row['key'] for row in group['keys']]
    assert len(keys) == 1
    key = keys[0]
    values = sorted({row['point'][key] for row in rows})
    for edge, value in [('low', values[0]), ('high', values[-1])]:
        point = anchor['point'] | {key: value}
        result = evaluate(point)
        violated = [catalog[cid]['source_local_identity'] for cid, status in result['verdicts'].items() if status != 'satisfied']
        edges.append({'axis': group['axis'], 'edge': edge, 'value': value,
                      'point': point, 'caught': bool(violated), 'violated': violated, **result})
write('edge-scan.json', {'anchor_proposal_id': anchor['proposal_id'], 'anchor_point': anchor['point'],
                        'anchor_feasible_18': anchor['feasible_18'], 'anchor_feasible_19': anchor['full_satisfied'],
                        'edges': edges, 'interpretation': 'Caught means a predicate fails at this endpoint from the stated anchor. These are oracle-only sensitivity diagnostics, not native cases or located continuous boundaries.'})
print('Candidate scan:', len(out), 'unique cases;', sum(r['feasible_18'] for r in out), 'old-predicate passes;', len(feasible), 'all-predicate passes; edge anchor', anchor['proposal_id'])
