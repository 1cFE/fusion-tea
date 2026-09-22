"""Five real TEAx cases plus independent balance and exact reuse checks."""
import json
import math
from pathlib import Path
from types import SimpleNamespace
from decimal import Decimal, localcontext
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-082_aries-existing-component-transfer-proof/evidence'
package = HERE / 'fuel_tea'
runtime = HERE / 'runtime'
runtime.mkdir(exist_ok=True)
module, fingerprint = ProvisionalPackageLoader(package_dir=package, package_name='fuel_tea', link_root=runtime / 'link').load()
registry = module.create_fuel_tea_registry()
# Comparison only: execute the existing function body with its type import remapped.
# Main results above/below always come from the generated package's actual TEAx pipeline.
baseline_file = ROOT / 'exploration/stellarator_e2e/generated/handwritten/mfe_fuel_cycle/fuel_cycle_flows_impl.py'
baseline_namespace = {}
exec(compile(baseline_file.read_text().replace('from stellarator_tea.', 'from fuel_tea.'), str(baseline_file), 'exec'), baseline_namespace)
run_fuel_cycle_flows = baseline_namespace['run_fuel_cycle_flows']
from fuel_tea.schemas.fuel_cycle_flows_output import Fuel_Cycle_FlowsOutput

cases = [('reference', 2436., 2e22, True, True), ('inadequate', 2436., 1e22, True, False), ('double_load', 4872., 2e22, True, False), ('half_load', 1218., 2e22, True, True), ('unsupported', 2436., 2e22, False, False)]
records = []
flowprefix = 'aries_fuel_reuse__fuel_system__flows__'
capprefix = 'aries_fuel_reuse__processing__capacity__'
for name, load, rating, supported, expected_ok in cases:
    case = runtime / name
    case.mkdir(exist_ok=True)
    spec = yaml.safe_load((package / 'pipelines/pipeline.yaml').read_text())
    entries = spec['modules']['entry_fusion']['inputs']
    effective = {}
    for key, binding in entries.items():
        schema, relative = binding.split(' ', 1)
        values = json.loads((package / 'pipelines' / relative).read_text())
        if key == 'fuel_reuse_params':
            values.update({'aries_fuel_reuse__fuel_system__fusion_load_mw': load, 'aries_fuel_reuse__processing__selected_rating_atoms_s': rating, 'aries_fuel_reuse__processing__assumed_conditions_supported': supported})
        if key == 'mfe_viability_params':
            values = {k: bool(v) for k, v in values.items()}
        path = case / (key + '.json')
        path.write_text(json.dumps(values, indent=2) + '\n')
        entries[key] = schema + ' ' + str(path)
        effective.update(values)
    pipeline = case / 'pipeline.yaml'
    pipeline.write_text(yaml.safe_dump(spec, sort_keys=False))
    result = execute_pipeline(pipeline, case / 'outputs', registry=registry, custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
    out = result.outputs
    flow_inputs = SimpleNamespace(p_fus_in=load, q_eff_in=17.58, mev_to_joules_in=1.6021766339999998e-13, burn_fraction_in=.05, t_recycle_in=.99, tbr_available_in=0., eta_extract_in=1., lambda_T_in=1.782785958230312e-09, I_total_in=0., G_stock_in=0., m_T_kg_in=5.008267663228036e-27, s_per_fpy_in=31536000.)
    baseline = dict(zip(Fuel_Cycle_FlowsOutput.model_fields, run_fuel_cycle_flows(flow_inputs)))
    for key, value in baseline.items():
        assert out[flowprefix + key] == value, (name, key, value, out[flowprefix + key])
    with localcontext() as context:
        context.prec = 50
        burn_expected = float(Decimal(str(load)) * Decimal(10)**6 / (Decimal('17.58') * Decimal('1.6021766339999998e-13')))
    burn, inject, exhaust, loss = [out[flowprefix + k] for k in ['burn_rate', 'inject_rate', 'exhaust_rate', 'loss_rate']]
    assert math.isclose(burn, burn_expected, rel_tol=2e-15)
    assert math.isclose(inject, burn + exhaust, rel_tol=2e-15)
    assert math.isclose(loss, .01 * exhaust, rel_tol=2e-15)
    assert out[capprefix + 'margin'] == rating - exhaust
    assert out[capprefix + 'capacity_ok'] is expected_ok
    assert out[capprefix + 'supported'] is supported
    assert out[capprefix + 'evaluation_defined'] == float(supported)
    assert effective['aries_fuel_reuse__processing__selected_rating_atoms_s'] == rating
    dump = {k: v.model_dump(mode='json') if hasattr(v, 'model_dump') else v for k,v in out.items()}
    report = dump['constraint_report']
    assert report['assessed_entry_count'] == 1
    assert report['results'][0]['status'] == ('satisfied' if expected_ok else 'violated')
    assert report['results'][0]['observed']['defined_in'] == float(supported)
    records.append({'case': name, 'fusion_load_MW': load, 'selected_rating_atoms_s': rating, 'conditions_supported_assumption': supported, 'expected_capacity_ok': expected_ok, 'outputs': dump, 'effective_inputs': effective, 'exact_baseline_flow_comparisons': len(baseline), 'independent_checks_passed': True})
reference = records[0]['outputs'][flowprefix + 'exhaust_rate']
assert records[2]['outputs'][flowprefix + 'exhaust_rate'] == 2 * reference
assert records[3]['outputs'][flowprefix + 'exhaust_rate'] == reference / 2
payload = {'claim': 'Conditioned tritium-flow and supplied scalar capacity reuse only; breeding channels are out of scope placeholders, not predictions.', 'fingerprint': str(fingerprint), 'cases': records, 'checks_passed': True}
(EVIDENCE / 'results.json').write_text(json.dumps(payload, indent=2) + '\n')
print(json.dumps({'checks_passed': True, 'cases': len(records), 'exhaust_atoms_s': reference, 'reference_margin_atoms_s': records[0]['outputs'][capprefix + 'margin']}, indent=2))
