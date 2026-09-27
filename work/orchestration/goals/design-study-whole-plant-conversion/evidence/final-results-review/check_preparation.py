"""Independent finite-catalog, identity and admission-proof checks; no model edits."""
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from exploration.whole_plant_conversion.studies import report_results as reporter
from exploration.whole_plant_conversion.studies import proposals, scenarios

HERE = Path(__file__).resolve().parent
RECORD = ROOT / 'exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion'
PREP = RECORD / 'preparation'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
canonical = lambda x: hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()
freeze = read(PREP / 'candidate-freeze.json')
for path, expected in freeze['artifact_sha256'].items():
    assert sha(PREP / path) == expected, path
for path, expected in freeze['code_sha256'].items():
    assert sha(ROOT / path) == expected, path
base = read(PREP / 'baseline.json')['point']
points = read(PREP / 'proposed-points.json')['cases']
members = read(PREP / 'case-membership.json')['cases']
oracle = {r['point_id']: r for r in read(PREP / 'oracle-scan.json')['cases']}
predicates = read(PREP / 'predicate-catalog.json')
deps = read(PREP / 'predicate-input-dependencies.json')['predicates']
by_id = {p['point_id']: p for p in points}
by_alias = {a['case']: a for a in members}
assert len(by_id) == len(points) == 2496
assert len(by_alias) == len(members) == 2651
assert len(base) == 637
for p in points:
    assert set(p['point']) == set(base)
    assert canonical(p['point']) == p['point_id']
    assert oracle[p['point_id']]['status'] == 'evaluated'
    for a in p['aliases']:
        assert by_alias[a['case']] == a | {'point_id': p['point_id']}
assert all(r['status'] == 'evaluated' for r in oracle.values())
counts = collections.Counter((r['scenario'], r['branch'], r['source_MW']) for r in members if r['role'] in ('gas_catalog', 'steam_connector_catalog'))
for scenario, sources in [('nominal', (2500., 2800., 3000.)), ('gas-favourable', (2500., 2800.)), ('steam-favourable', (2500., 2800.))]:
    for source in sources:
        assert counts[(scenario, 'gas', source)] == 125
        assert counts[(scenario, 'steam', source)] == 24

# The reporting input partition must never mark an input of a shared predicate
# as exclusive to one technology, nor require the opposite technology for a
# branch predicate. Dependency sets conservatively include whole calculation inputs.
partition_violations = []
for cid, entry in predicates.items():
    allowed = {'shared', entry['branch']}
    for key in deps[cid]:
        if reporter.input_branch(key) not in allowed:
            partition_violations.append((cid, key, reporter.input_branch(key)))
assert not partition_violations, partition_violations

audit_counts = {}
for filename, key in [('admission-audit.json', 'nominal_offer'), ('interaction-admission-audit.json', 'case')]:
    rows = read(PREP / filename)['cases']
    count = collections.Counter()
    for row in rows:
        original = oracle[by_alias[row[key]]['point_id']]
        branch = row['branch']
        assert row['nominal_failed_predicates'] == original['failed'][branch]
        if row['disposition'] == 'excluded_by_invariant_failed_predicate':
            fixed = row['invariant_failed_predicates']
            assert fixed
            assert all(cid in original['failed'][branch] and not set(row['changed_inputs']).intersection(deps[cid]) for cid in fixed)
        else:
            assert row['disposition'] == 'still_excluded_after_oracle_evaluation'
            result = oracle[row['point_id']]
            assert not result['eligible'][branch]
            assert result['failed'][branch] == row['failed_predicates']
        count[row['disposition']] += 1
    audit_counts[filename] = dict(count)

# The eight price/service scenarios omit nominal failures. Independently verify
# that each omitted offer retains at least one price-independent failed predicate.
price_prunes = 0
source_prunes = 0
algebraic_price_prunes = collections.Counter()
nominal = [a for a in members if a['scenario'] == 'nominal']
for alias in nominal:
    branch = alias['branch']
    point = by_id[alias['point_id']]['point']
    initial = oracle[alias['point_id']]
    choices = [r['chosen'] for r in proposals.sensitivity_catalog(point) if '-quote-' in r['case'] or '-recurring-' in r['case']]
    if alias['source_MW'] == 3000.:
        choices += [r['choices'] for r in scenarios.common_scenarios(base)]
    elif initial['eligible'][branch]:
        continue
    for choice in choices:
        changed = {proposals.P + k for k, v in choice.items() if point[proposals.P + k] != v}
        fixed = any(not changed.intersection(deps[cid]) for cid in initial['failed'][branch])
        if not fixed:
            # Conservative dependency sets include all ledger inputs, including
            # prices. The reviewed ledger's export and annual delivery equations
            # contain no quote/service operand. An existing nonpositive operating
            # export therefore remains an exclusion under these price changes.
            allowed = set(proposals.GAS_QUOTE_KEYS) | set(proposals.STEAM_QUOTE_KEYS)
            allowed |= {b + '_ledger__' + f for b in ('gas', 'steam') for f in ('annual_service_fraction', 'replacement_fraction')}
            assert set(choice) <= allowed, (alias['case'], choice)
            channel = proposals.P + branch + '_operating__evaluate__net_export_MW'
            annual = proposals.P + branch + '_operating__evaluate__annual_net_grid_MWh'
            if initial['outputs'][channel] <= 0 or initial['outputs'][annual] <= 0:
                algebraic_price_prunes[branch + '_nonpositive_delivery'] += 1
            else:
                # The retained cooling equipment body applies costscale only to
                # currency/price expressions. Pump quantities, shaft/electric
                # ratings and motor/type predicates use flow/head/efficiency.
                mechanical = ('salt_shaft_capacity', 'salt_flow_capacity', 'salt_electric_capacity')
                def physical_steam_predicate(cid):
                    owner = predicates[cid]['owner']
                    return owner in mechanical or (owner.startswith('steam_') and owner.endswith('_capacity')) or owner == 'steam_conditions' or any(fragment in cid for fragment in ('steam_transport__motor_factor_ok_required__', 'steam_transport__pump_type_ok_required__', 'steam_transport__ihx_capacity_ok_required__'))
                mechanical_failure = any(physical_steam_predicate(cid) for cid in initial['failed'][branch])
                assert branch == 'steam' and mechanical_failure, (alias['case'], initial['failed'][branch])
                assert all(v > 0 for v in choice.values())
                algebraic_price_prunes['steam_price_independent_physical_failure'] += 1
        if alias['source_MW'] == 3000.: source_prunes += 1
        else: price_prunes += 1

# Every declared ranking group uses exactly the same shared input map across
# both branches and all offered hardware choices. No result selection is used.
shared = collections.defaultdict(set)
for a in members:
    if a['role'] in reporter.RANKING_ROLES:
        p = by_id[a['point_id']]['point']
        common = {k: v for k, v in p.items() if reporter.input_branch(k) == 'shared'}
        shared[(a['scenario'], a['source_MW'])].add(canonical(common))
assert all(len(s) == 1 for s in shared.values())
result = dict(status='pass', preparation_freeze_sha256=sha(PREP / 'candidate-freeze.json'),
              unique_points=len(points), aliases=len(members), oracle_points=len(oracle),
              full_catalog_counts={str(k): v for k, v in counts.items()},
              predicate_partition=dict(collections.Counter(p['branch'] for p in predicates.values())),
              dependency_partition_violations=partition_violations, audited_pruning=audit_counts,
              additional_price_service_invariant_prunes=price_prunes,
              price_prunes_using_reviewed_net_power_algebra=dict(algebraic_price_prunes),
              source3000_invariant_prunes=source_prunes,
              ranking_groups_with_single_common_input_map=len(shared))
(HERE / 'preparation-checks.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
