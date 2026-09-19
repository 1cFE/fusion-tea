"""Describe retained native evidence; no plant evaluator or sweep implementation."""
import csv
import json
import math
from pathlib import Path
import sys

H = Path(__file__).resolve().parents[1]
ROOT = H.parents[3]
R = H / 'results'
P = 'stellarator_09__stellaris__'
sys.path.insert(0, str(ROOT))
from scripts.study import indicators

read = lambda path: json.loads(path.read_text())
def write(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')
def key(point):
    return json.dumps({k: float(v) for k, v in point.items()}, sort_keys=True)

assert read(R / 'oracle-all-points.json')['outcome'] == 'pass'
props = {key(row['point']): row for row in read(H / 'preparation/proposals.json')}
raw = read(R / 'native-cases.json')
catalog = read(R / 'predicate-catalog.json')
by_case = {props[key(case['inputs'])]['id']: case for case in raw}
names = {
    'fusion_MW': 'plasma__fusion__p_fus', 'net_MW': 'pb__p_net',
    'availability': 'calendar__availability',
    'flow_kg_day': 'fuel_cycle__inventory__dt_processor_kg_day',
    'annual_exhaust_kg_T': 'fuel_cycle__inventory__annual_exhaust_kg',
    'startup_kg_T': 'fuel_cycle__inventory__startup_conservative_kg',
    'inventory_defined': 'fuel_cycle__inventory__defined_flag',
    'equipment': 'fuel_cycle__processing_cost__equipment_total',
    'installation': 'fuel_cycle__processing_cost__installation_total',
    'processing_selected': 'fuel_cycle__processing_cost__cost',
    'processing_legacy': 'fuel_cycle__fuel_handling__cost',
    'processing_defined': 'fuel_cycle__processing_cost__defined_flag',
    'capacity_kg_s': 'fuel_cycle__processing_cost__capacity_kg_s',
    'CAS22': 'cas22_capital__cas22_capital', 'CAS20': 'cas20_capital__cas20_capital',
    'supplementary': 'supplementary__cost',
    'installation_shipping_exclusion': 'shipping_scope__fuel_installation_exclusion',
    'shipping_base': 'shipping_scope__remaining_shipping_base',
    'total_capital': 'total_capital__total_capital',
    'annual_fuel_raw': 'fuel_cycle__fuel_calc__annual_fuel',
    'annual_fuel_levelized': 'cas80_calc__levelized',
    'LCOE': 'lcoe_calc__lcoe', 'LCOE_1cfe': 'lcoe_1cfe_calc__lcoe',
}
rows = []
for proposal in read(H / 'preparation/proposals.json'):
    case = by_case[proposal['id']]
    row = {'id': proposal['id'], 'family': proposal['family'], 'candidate_id': case['candidate_id']}
    row.update({name: case['outputs'][P + suffix] for name, suffix in names.items()})
    row['failed'] = ';'.join(catalog[cid]['source_local_identity'] for cid, status in case['verdicts'].items() if status != 'satisfied')
    row.update(case['verdicts'])
    rows.append(row)
write(R / 'interpreted-cases.json', rows)
with (R / 'points.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)
numeric = read(H / 'preparation/required-channels.json')
with (R / 'all-native-channels.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=['id', 'candidate_id'] + numeric)
    writer.writeheader()
    for identity, case in by_case.items():
        writer.writerow({'id': identity, 'candidate_id': case['candidate_id']} | {k: case['outputs'][k] for k in numeric})
by = {row['id']: row for row in rows}
b, old = by['reference'], by['legacy-reference']
graph = indicators.build_graph(indicators.read_pipelines(ROOT / 'exploration/stellarator_e2e/generated'))
cost_reachable, _ = indicators.reachable_channels({P + 'fuel_cycle__processing_enabled'}, graph)
outside = sorted(set(by_case['reference']['outputs']) - cost_reachable)
checks = []

def unchanged(left, right, channels, label, verdicts=False):
    a, z = by_case[left], by_case[right]
    differences = [k for k in channels if a['outputs'][k] != z['outputs'][k]]
    statuses_equal = a['verdicts'] == z['verdicts']
    checks.append({'check': label, 'left': left, 'right': right, 'channel_count': len(channels),
                   'channels': list(channels), 'differences': differences,
                   'verdicts_equal': statuses_equal, 'require_verdict_equality': verdicts,
                   'outcome': 'pass' if not differences and (statuses_equal or not verdicts) else 'fail'})

pairs = []
for identity in by:
    if not identity.startswith('legacy-'):
        continue
    active = identity.removeprefix('legacy-')
    unchanged(active, identity, outside, 'Matched account control: all outputs outside processing descendant graph', True)
    pairs.append({'active': active, 'legacy': identity, **{name: by[active][name] - by[identity][name] for name in
                  ('processing_selected', 'CAS22', 'CAS20', 'supplementary', 'total_capital', 'annual_fuel_raw', 'LCOE', 'LCOE_1cfe')}})

inlet_channels = [P + 'fuel_cycle__inventory__dt_processor_kg_s',
                  P + 'fuel_cycle__processing_cost__flow_kg_s',
                  P + 'fuel_cycle__processing_cost__capacity_kg_s',
                  P + 'fuel_cycle__processing_cost__cost']
for identity, row in by.items():
    if row['family'] in ('recovery', 'downtime'):
        unchanged('reference', identity, inlet_channels, 'Running inlet and processing price invariant')
    if row['family'] in ('price', 'margin', 'containment-date'):
        unchanged('reference', identity, outside, 'Assumption-only change preserves upstream/non-descendant outputs', True)
        unchanged('reference', identity, [P + 'fuel_cycle__processing_cost__flow_kg_s'], 'Assumption-only change preserves actual inlet')
    if row['family'] == 'containment-date':
        channels = [P + f'fuel_cycle__processing_cost__{part}_{field}' for part in ('transfer', 'cleanup', 'distiller') for field in ('capital', 'installation', 'reference_capital', 'reference_installation')]
        unchanged('reference', identity, channels, 'Containment year changes no other source row')
write(R / 'matched-account-deltas.json', pairs)
write(R / 'invariance-checks.json', {'outcome': 'pass' if all(x['outcome'] == 'pass' for x in checks) else 'fail', 'checks': checks,
      'interpretation': 'Graph closure selects all scalar outputs outside processing-cost downstream influence. Exact equality at matched native points is checked; this is observational invariance, not physical qualification.'})
assert all(x['outcome'] == 'pass' for x in checks), 'Native isolation check failed; retain evidence'
legacy_burn = []
for identity in ('legacy-burn-0.025', 'legacy-burn-0.1'):
    a, z = by_case['legacy-reference']['outputs'], by_case[identity]['outputs']
    changed = {k: {'reference': a[k], 'changed': z[k]} for k in a if a[k] != z[k]}
    legacy_burn.append({'id': identity, 'all_changed_outputs': changed,
                       'total_capital_unchanged': a[P + names['total_capital']] == z[P + names['total_capital']],
                       'processing_cost_unchanged': a[P + names['processing_selected']] == z[P + names['processing_selected']]})
write(R / 'legacy-burn-attribution.json', legacy_burn)
summary = {'cases': len(rows), 'wholeplant_satisfied': sum(not row['failed'] for row in rows),
           'reference': b, 'legacy_reference': old,
           'ranges': {name: {'min': min(row[name] for row in rows), 'max': max(row[name] for row in rows)} for name in names},
           'predicate_counts': {cid: {status: sum(case['verdicts'][cid] == status for case in raw) for status in ('satisfied', 'violated', 'indeterminate')} for cid in catalog}}
write(R / 'summary.json', summary)

lines = ['# Throughput-priced conventional exhaust processing', '',
f'The represented process now prices the reference running inlet of **{b["flow_kg_day"]:.6f} kg D+T/day** at **${b["processing_selected"]/1e6:.3f} million**: ${b["equipment"]/1e6:.3f} million equipment and ${b["installation"]/1e6:.3f} million direct installation. These are limited historical subsystem costs expressed in 2025 CPI purchasing power, not modern quotations or a complete fuel plant.', '',
f'At the identical physical reference point, selecting the legacy account instead gives ${old["processing_selected"]/1e6:.3f} million. The selected method reduces total plant capital by ${(old["total_capital"]-b["total_capital"])/1e6:.3f} million and lifecycle LCOE by ${old["LCOE"]-b["LCOE"]:.6f}/MWh, from ${old["LCOE"]:.6f} to ${b["LCOE"]:.6f}/MWh. The separate 1costingFE-form LCOE changes from ${old["LCOE_1cfe"]:.6f} to ${b["LCOE_1cfe"]:.6f}/MWh. The difference includes the downstream generic charges and installation freight exclusion.', '',
f'**None of the {len(rows)} cases satisfies every plant screen.** The reference fails {b["failed"].replace(";", ", ")}. The lower estimate is conditional accounting evidence; it does not establish breeding self-sufficiency or feasible operation. [Native points](results/points.csv), [all numeric native outputs](results/all-native-channels.csv), and [complete raw cases and verdicts](results/native-cases.json) supply every reported result.', '',
'## Scope and capacity', '',
'The inlet is equal-atom-rate D/T exhaust before recovery loss. Tritium-only mass and total gas mass are different quantities. Equipment capacity uses running flow; availability changes annual amounts. The four rows cover internal transfer pumps, cleanup, cryogenic isotope separation and limited secondary containment. Their common 0.3 exponent follows the accepted historical source. Source-like feed impurities, conditioning and separation service remain declared applicability premises.', '',
'The source price contains some package-local controls and direct installation. It does not purchase torus vacuum pumping, complete fueling hardware, storage, blanket extraction/conditioning, plant-wide detritiation or complete safety and containment. Civil buildings/ventilation and the existing supervisory I&C allowance retain separate scope. The latter is an uncalibrated residual under the stated allocation. No unsupported remainder of the legacy fuel account is retained.', '',
'The new account enters the existing CAS22 summand once. Source direct installation is excluded from generic shipping after the same CAS29 contingency; other generic charges remain. [Account contract](preparation/references/account-reconciliation.md) and [reviewed design](preparation/references/design.md) state these boundaries.', '',
'## Actual drivers and controls', '',
'| Case | Running D+T kg/day | Selected process M$ | Raw annual fuel $/yr | LCOE $/MWh | Comparison LCOE $/MWh |',
'|---|---:|---:|---:|---:|---:|']
for row in rows:
    lines.append(f'| {row["id"]} | {row["flow_kg_day"]:.6f} | {row["processing_selected"]/1e6:.6f} | {row["annual_fuel_raw"]:.2f} | {row["LCOE"]:.6f} | {row["LCOE_1cfe"]:.6f} |')
lo, hi = by['burn-0.025'], by['burn-0.1']
ol, oh = by['legacy-burn-0.025'], by['legacy-burn-0.1']
lines += ['', f'At fixed plasma inputs, changing single-pass burn from 0.025 to 0.10 changes running inlet from {lo["flow_kg_day"]:.6f} to {hi["flow_kg_day"]:.6f} kg D+T/day and process capital from ${lo["processing_selected"]/1e6:.6f} to ${hi["processing_selected"]/1e6:.6f} million. Burn also changes the existing recurring-fuel correction. In legacy mode process capital and total plant capital stay fixed, while raw annual fuel changes from ${ol["annual_fuel_raw"]:.2f} to ${oh["annual_fuel_raw"]:.2f}; its CAS80 levelization changes LCOE from ${ol["LCOE"]:.6f} to ${oh["LCOE"]:.6f}/MWh. The new-method burn response therefore includes both processing capital and recurring fuel. [Changed-output attribution](results/legacy-burn-attribution.json) retains all differences.', '',
'The held recurring-price recovery factor is 0.99. It appears in the existing correction 1 + (1−burn)/burn × (1−fuel_recovery), which becomes 1.39, 1.19 and 1.09 at the three burn values. Physical t_recycle is a separate input. Its two sensitivity cases reduce losses and change breeding adequacy, but leave inlet demand, processing price and recurring-price input unchanged. This study does not introduce a newly coupled recurring-cost recovery model.', '',
'The density cases change fusion power through the native plasma calculation. They also change other plant systems, net power and electricity output, so their entire LCOE movement is not attributable to fuel processing. Matched account deltas below isolate the cost-method change at each operating point.', '',
'| Identical physical point | New minus legacy process M$ | Total capital M$ | Lifecycle LCOE $/MWh | Comparison LCOE $/MWh |',
'|---|---:|---:|---:|---:|']
for pair in pairs:
    lines.append(f'| {pair["active"]} | {pair["processing_selected"]/1e6:.6f} | {pair["total_capital"]/1e6:.6f} | {pair["LCOE"]:.6f} | {pair["LCOE_1cfe"]:.6f} |')
lines += ['', 'All matched controls preserve the complete scalar-output set outside the processing cost’s downstream graph and every physical predicate verdict. [Exact comparison evidence](results/invariance-checks.json) lists all compared channels. Recurring fuel and computed startup stock are unchanged within each old/new pair. CAS50 startup purchase remains its existing power proxy; the new processing account does not purchase computed startup stock again.', '',
'## Monetary and process-assumption sensitivity', '',
'Price multiplier 0.5/1/2 is an engineered stress range, not a confidence interval. Capacity margin 1/1.25/1.5 sizes above actual inlet and follows the source exponent; it buys no demonstrated spare train or reliability. Both leave the physical producer unchanged. Containment CPI 65.2/82.4/96.5 means the actual 1978/1980/1982 expenditure-date scenarios, not calendar years represented numerically as CPI. These cases change only the containment row’s conversion and downstream sums; the three other source rows stay identical.', '',
'Downtime 0/0.1/0.5 leaves running inlet and processing price unchanged, while reducing availability, annual processing and electricity output. The resulting LCOE change is a utilization effect. The studied finite points are sensitivities; no feasible boundary or optimum is claimed.', '',
'## Verification, attempts and limits', '',
f'The completed retry retains all {len(rows)} native cases. The independent arithmetic implementation compares {read(R/"oracle-all-points.json")["scalar_comparisons"]} mapped scalar values and {read(R/"oracle-all-points.json")["predicate_comparisons"]} predicate verdicts; all pass. The generic verifier also passes. The {len(read(H/"preparation/coverage.json")["unmapped_numeric"])} numeric channels outside the oracle map are named in [coverage](preparation/coverage.json). Shared source assumptions and neutron-transport data are not independent physical validation. The executor authored the independent cost oracle; final certification belongs to the non-author reviewer.', '',
'Attempt 1 admitted 15 active cases and rejected five JSON-Boolean legacy proposals before native evaluation because the stock route’s Boolean allowlist omitted the new switch. The original store and artifacts remain; [attempt record](results/attempt-1/attempt.json) and [proposal admission evidence](results/attempt-1/results/proposal-admission-issue.json) disclose the rejection. The coordinator authorized the same five false values as numeric 0.0, supported by the existing route. The equivalent 20-point list was re-scanned and executed in a fresh store. No model/shared-route change or feasibility filtering occurred; the relocated attempt backup is not claimed cold-reproducible.', '',
'The integration receipt reports an omitted read-set coverage check. The indicator tool checks its own read set, which does not close that integration limitation. Static L2 remains unresolved, and WI-070 added three instances of the known L6 dot-expression diagnostic; native execution checks the corresponding flow, shipping and applicability bindings without claiming static validation passes. Boolean serializer warnings remain disclosed in the retained verification logs.', '',
'This record supplies no qualified feed composition, process reliability, vendor price, independent economic uncertainty calibration or whole-plant feasibility result. It has not received final independent study/rubric certification.']
(H / 'report.md').write_text('\n'.join(lines) + '\n')
print(f'Exported {len(rows)} cases, matched deltas, invariance checks, attribution and report')
