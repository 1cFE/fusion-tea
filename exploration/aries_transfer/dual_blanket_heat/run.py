"""Execute conditioned heat branches and independently check accounting/capacity."""
import json
import math
from decimal import Decimal, localcontext
from pathlib import Path
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-086_aries-dual-blanket-heat-accounting/evidence'
package = HERE / 'heat_tea'
runtime = HERE / 'runtime'
runtime.mkdir(exist_ok=True)
module, fingerprint = ProvisionalPackageLoader(package_dir=package, package_name='heat_tea', link_root=runtime / 'link').load()
registry = module.create_heat_tea_registry()
base = json.loads((package / 'inputs/dual_blanket_heat_params.json').read_text())
P = 'aries_dual_blanket_heat__'
from heat_tea.schemas.dual_blanket_heat_params import DualBlanketHeatParams
assert not any('absent_' in key for key in base)
assert not any('absent_' in key for key in DualBlanketHeatParams.model_fields)
assert [key for key in base if 'exchange' in key] == [P + 'inter_coolant_exchange__transferred_heat_mw']

def primitive(value):
    return value.model_dump(mode='json') if hasattr(value, 'model_dump') else value

def execute(name, overrides):
    case = runtime / name
    case.mkdir(exist_ok=True)
    values = {**base, **overrides}
    for branch in ('helium', 'pbli'):
        for field in ('assumed_conditions_supported', 'scenario_applicable', 'duty_available'):
            key = P + branch + '__' + field
            values[key] = bool(values[key])
    inputs = case / 'inputs.json'
    inputs.write_text(json.dumps(values, indent=2) + '\n')
    pipeline = yaml.safe_load((package / 'pipelines/pipeline.yaml').read_text())
    pipeline['modules']['entry_fusion']['inputs']['dual_blanket_heat_params'] = 'DualBlanketHeatParams ' + str(inputs)
    target = case / 'pipeline.yaml'
    target.write_text(yaml.safe_dump(pipeline, sort_keys=False))
    result = execute_pipeline(target, case / 'outputs', registry=registry, custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
    return values, {k: primitive(v) for k,v in result.outputs.items()}

scenarios = [
    ('source_boundaries', {}, (True, True)),
    ('smaller_helium_rating', {P + 'helium__offered_duty_mw': 1100.}, (False, True)),
    ('smaller_pbli_rating', {P + 'pbli__offered_duty_mw': 1400.}, (True, False)),
    ('higher_deposition_fixed_hardware', {P + 'helium__deposited_heat_mw': 1034., P + 'pbli__deposited_heat_mw': 1710.5}, (False, False)),
    ('changed_internal_exchange', {P + 'inter_coolant_exchange__transferred_heat_mw': 200.}, (False, True)),
    ('zero_helium_friction', {P + 'helium__recovered_friction_mw': 0.}, (True, True)),
    ('unsupported_helium_conditions', {P + 'helium__assumed_conditions_supported': False}, (False, True)),
]
records = []
for name, overrides, expected in scenarios:
    values, out = execute(name, overrides)
    assert out[P + 'inter_coolant_exchange__absent_boundary_exchange_mw__absent_boundary_exchange_mw'] == 0.0
    with localcontext() as context:
        context.prec = 50
        d = lambda field: Decimal(str(values[P + field]))
        exchange = d('inter_coolant_exchange__transferred_heat_mw')
        dep_he, dep_pb = d('helium__deposited_heat_mw'), d('pbli__deposited_heat_mw')
        fric_he, fric_pb = d('helium__recovered_friction_mw'), d('pbli__recovered_friction_mw')
        heat_he, heat_pb = dep_he + exchange + fric_he, dep_pb - exchange + fric_pb
        checked = {P + 'helium__heat__delivered_heat': heat_he, P + 'pbli__heat__delivered_heat': heat_pb,
            P + 'blanket_ledger__energy__delivered_total': heat_he + heat_pb,
            P + 'blanket_ledger__energy__deposited_total': dep_he + dep_pb,
            P + 'blanket_ledger__energy__friction_total': fric_he + fric_pb,
            P + 'blanket_ledger__energy__energy_residual': Decimal(0)}
        for key, number in checked.items():
            assert math.isclose(out[key], float(number), rel_tol=2e-15, abs_tol=1e-12), (name, key, out[key], number)
    for branch, heat, expected_ok in zip(('helium', 'pbli'), (heat_he, heat_pb), expected):
        prefix = P + branch + '__'
        supported = values[prefix + 'assumed_conditions_supported']
        rating = values[prefix + 'offered_duty_mw']
        assert out[prefix + 'capacity__margin'] == rating - float(heat)
        assert out[prefix + 'capacity__capacity_ok'] is expected_ok
        assert out[prefix + 'capacity__supported'] is supported
        assert out[prefix + 'capacity__evaluation_defined'] == float(supported)
        assert rating == overrides.get(prefix + 'offered_duty_mw', base[prefix + 'offered_duty_mw'])
    report = out['constraint_report']
    assert report['assessed_entry_count'] == 2
    for evaluation in report['results']:
        index = 0 if '__helium__' in evaluation['constraint_id'] else 1
        assert evaluation['status'] == ('satisfied' if expected[index] else 'violated')
    records.append({'case': name, 'effective_inputs': values, 'outputs': out, 'source_deposition_residual_MW': out[P + 'blanket_ledger__energy__deposited_total'] - 2496., 'independent_heat_comparisons': len(checked), 'expected_capacity_ok': list(expected)})
ledger = P + 'blanket_ledger__energy__'
assert records[0]['source_deposition_residual_MW'] == -1.
assert records[4]['outputs'][ledger + 'delivered_total'] == records[0]['outputs'][ledger + 'delivered_total']
assert records[0]['outputs'][ledger + 'delivered_total'] - records[5]['outputs'][ledger + 'delivered_total'] == 141.

invalids = [
    ('negative_deposition', {P + 'helium__deposited_heat_mw': -1.}, 'deposited_heat_in'),
    ('negative_transfer', {P + 'inter_coolant_exchange__transferred_heat_mw': -1.}, 'exchange_in'),
    ('negative_friction', {P + 'helium__recovered_friction_mw': -1.}, 'recovered_friction_in'),
    ('negative_net_branch', {P + 'inter_coolant_exchange__transferred_heat_mw': 2000.}, 'delivered heat'),
    ('nonfinite_deposition', {P + 'pbli__deposited_heat_mw': float('inf')}, 'finite'),
    ('nonfinite_transfer', {P + 'inter_coolant_exchange__transferred_heat_mw': float('nan')}, 'finite'),
    ('infinite_transfer', {P + 'inter_coolant_exchange__transferred_heat_mw': float('inf')}, 'finite'),
    ('extra_absent_direction', {P + 'helium__absent_outgoing_exchange_mw': 1.}, 'Extra inputs'),
    ('negative_capacity', {P + 'helium__offered_duty_mw': -1.}, 'rating'),
    ('nonfinite_capacity', {P + 'pbli__offered_duty_mw': float('inf')}, 'rating'),
    ('overflow_heat', {P + 'helium__deposited_heat_mw': 1e308, P + 'helium__recovered_friction_mw': 1e308}, 'finite'),
]
refusals = []
for name, overrides, message in invalids:
    try:
        execute(name, overrides)
    except Exception as exc:
        assert message in str(exc), (name, type(exc).__name__, str(exc))
        refusals.append({'case': name, 'overrides': {k: str(v) if not math.isfinite(v) else v for k,v in overrides.items()}, 'exception': type(exc).__name__, 'message': str(exc)})
    else:
        raise AssertionError('invalid case returned: ' + name)

# The generated ledger wrapper must preserve negative as well as positive residuals.
from heat_tea.modules.dual_circuit_heat_accounting.dual_circuit_heat_ledger import Dual_Circuit_Heat_LedgerModule
signed = []
for duty in (9., 11.):
    result = Dual_Circuit_Heat_LedgerModule().run(duty_1_in=duty, duty_2_in=10., deposition_1_in=10., deposition_2_in=10., friction_1_in=0., friction_2_in=0.)
    assert result.data.energy_residual == duty - 10.
    signed.append(result.data.energy_residual)
payload = {'claim': 'Source-conditioned two-blanket-branch heat accounting and hypothetical scalar capacities; not hydraulic/equipment or whole-plant prediction.', 'fingerprint': str(fingerprint), 'cases': records, 'refusals': refusals, 'generated_wrapper_signed_residuals_MW': signed, 'all_checks_passed': True}
(EVIDENCE / 'results.json').write_text(json.dumps(payload, indent=2, allow_nan=False) + '\n')
summary = [{'case': r['case'], 'helium_MW': r['outputs'][P + 'helium__heat__delivered_heat'], 'pbli_MW': r['outputs'][P + 'pbli__heat__delivered_heat'], 'total_MW': r['outputs'][ledger + 'delivered_total'], 'energy_residual_MW': r['outputs'][ledger + 'energy_residual'], 'source_residual_MW': r['source_deposition_residual_MW'], 'capacity_ok': r['expected_capacity_ok']} for r in records]
print(json.dumps({'cases': summary, 'independent_heat_comparisons': sum(r['independent_heat_comparisons'] for r in records), 'native_refusals': len(refusals), 'signed_residuals_MW': signed, 'all_checks_passed': True}, indent=2))
