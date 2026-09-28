"""Execute supplied inventory scenarios through native TEAx, verify decimal balances."""
import json
import math
from decimal import Decimal, localcontext
from pathlib import Path
import yaml
from simkit.core.pipeline import execute_pipeline
from simkit.evaluation.package_load import ProvisionalPackageLoader

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'work/active/WI-084_aries-sector-constituent-inventory/evidence'
package = HERE / 'inventory_tea'
runtime = HERE / 'runtime'
runtime.mkdir(exist_ok=True)
module, fingerprint = ProvisionalPackageLoader(package_dir=package, package_name='inventory_tea', link_root=runtime / 'link').load()
registry = module.create_inventory_tea_registry()
base = json.loads((package / 'inputs/constituent_inventory_params.json').read_text())
P = 'aries_constituent_inventory__'
regions = ('full', 'behind_divertor', 'tapered')
materials = ('lipb', 'sic_insert', 'ferritic_steel')

def primitive(value):
    return value.model_dump(mode='json') if hasattr(value, 'model_dump') else value

def execute(name, overrides):
    case = runtime / name
    case.mkdir(exist_ok=True)
    values = {**base, **overrides}
    inputs = case / 'inputs.json'
    inputs.write_text(json.dumps(values, indent=2) + '\n')
    pipeline = yaml.safe_load((package / 'pipelines/pipeline.yaml').read_text())
    pipeline['modules']['entry_fusion']['inputs']['constituent_inventory_params'] = 'ConstituentInventoryParams ' + str(inputs)
    target = case / 'pipeline.yaml'
    target.write_text(yaml.safe_dump(pipeline, sort_keys=False))
    result = execute_pipeline(target, case / 'outputs', registry=registry, custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
    return values, {k: primitive(v) for k,v in result.outputs.items()}

def verify(values, out):
    comparisons = 0
    def check(key, expected):
        nonlocal comparisons
        assert math.isclose(out[key], float(expected), rel_tol=3e-15, abs_tol=1e-12), (key, out[key], expected)
        comparisons += 1
    with localcontext() as context:
        context.prec = 50
        aggregate = {k: Decimal(0) for k in ('volume', 'known_mass', 'source_price_subtotal', 'unquantified_volume')}
        for region in regions:
            prefix = P + region + '__'
            get = lambda name: Decimal(str(values[prefix + name]))
            volume = get('midpoint_area_basis') * get('coverage') * get('thickness')
            check(prefix + 'layer__volume', volume)
            mass = price = fraction = Decimal(0)
            for material in materials:
                m = material + '__'
                v = volume * get(m + 'volume_fraction')
                kg = v * get(m + 'material_density')
                dollars = kg * get(m + 'component_rate')
                check(prefix + m + 'inventory__constituent_volume', v)
                check(prefix + m + 'inventory__known_mass', kg)
                check(prefix + m + 'inventory__source_price_subtotal', dollars)
                mass += kg
                price += dollars
                fraction += get(m + 'volume_fraction')
            unquantified = volume * get('helium_fraction')
            assert fraction + get('helium_fraction') == 1
            for key, number in {'represented_fraction': fraction, 'known_mass': mass, 'source_price_subtotal': price, 'unquantified_volume': unquantified}.items():
                check(prefix + 'recipe__' + key, number)
            aggregate['volume'] += volume
            aggregate['known_mass'] += mass
            aggregate['source_price_subtotal'] += price
            aggregate['unquantified_volume'] += unquantified
        for key, number in aggregate.items():
            check(P + 'reference_blanket_subset__totals__' + key, number)
    return comparisons

scenarios = [
    ('lower_taper', {}),
    ('upper_taper', {P + 'tapered__thickness': .543}),
    ('double_area', {P + r + '__midpoint_area_basis': 2. for r in regions}),
    ('full_lipb_double_price', {P + 'full__lipb__component_rate': 34.2}),
    ('zero_area', {P + r + '__midpoint_area_basis': 0. for r in regions}),
]
records = []
for name, overrides in scenarios:
    values, out = execute(name, overrides)
    comparisons = verify(values, out)
    assert values == {**base, **overrides}
    records.append({'case': name, 'effective_inputs': values, 'outputs': out, 'independent_comparisons': comparisons})
total_prefix = P + 'reference_blanket_subset__totals__'
for key in ('volume', 'known_mass', 'source_price_subtotal', 'unquantified_volume'):
    assert records[2]['outputs'][total_prefix + key] == 2 * records[0]['outputs'][total_prefix + key]
for key, value in records[0]['outputs'].items():
    if not key.endswith('source_price_subtotal'):
        assert records[3]['outputs'][key] == value, key
price_delta = records[3]['outputs'][total_prefix + 'source_price_subtotal'] - records[0]['outputs'][total_prefix + 'source_price_subtotal']
assert math.isclose(price_delta, records[0]['outputs'][P + 'full__lipb__inventory__source_price_subtotal'], rel_tol=1e-14)

invalids = [
    ('negative_area', {P + 'full__midpoint_area_basis': -1.}, 'area_basis'),
    ('negative_thickness', {P + 'full__thickness': -1.}, 'thickness'),
    ('invalid_coverage', {P + 'full__coverage': 1.01}, 'coverage'),
    ('negative_density', {P + 'full__lipb__material_density': -1.}, 'density'),
    ('zero_density', {P + 'full__lipb__material_density': 0.}, 'density'),
    ('negative_rate', {P + 'full__lipb__component_rate': -1.}, 'unit_price'),
    ('invalid_fraction', {P + 'full__lipb__volume_fraction': 1.01}, 'fraction'),
    ('invalid_recipe', {P + 'full__helium_fraction': .09}, 'recipe fractions'),
    ('invalid_recipe_zero_volume', {P + 'full__midpoint_area_basis': 0., P + 'full__helium_fraction': .09}, 'recipe fractions'),
    ('invalid_partition', {P + 'full__coverage': .7}, 'sector coverages'),
    ('invalid_partition_zero_volume', {**{P + r + '__midpoint_area_basis': 0. for r in regions}, P + 'full__coverage': .7}, 'sector coverages'),
    ('nonfinite_area', {P + 'full__midpoint_area_basis': float('nan')}, 'finite'),
    ('nonfinite_density', {P + 'full__lipb__material_density': float('inf')}, 'finite'),
    ('overflow_mass', {P + 'full__midpoint_area_basis': 1e308}, 'finite'),
]
refusals = []
for name, overrides, expected in invalids:
    try:
        execute(name, overrides)
    except Exception as exc:
        assert expected in str(exc), (name, type(exc).__name__, str(exc))
        refusals.append({'case': name, 'overrides': {k: str(v) if not math.isfinite(v) else v for k,v in overrides.items()}, 'exception': type(exc).__name__, 'message': str(exc)})
    else:
        raise AssertionError('unsupported native case returned a result: ' + name)

payload = {'claim': 'Supplied normalized geometry; Table II reference recipe; known non-helium mass and unmapped source-rate subtotal only.', 'fingerprint': str(fingerprint), 'cases': records, 'refusals': refusals, 'all_checks_passed': True}
(EVIDENCE / 'results.json').write_text(json.dumps(payload, indent=2, allow_nan=False) + '\n')
summary = [{'case': r['case'], **{k: r['outputs'][total_prefix + k] for k in ('volume', 'known_mass', 'source_price_subtotal', 'unquantified_volume')}} for r in records]
print(json.dumps({'cases': summary, 'independent_comparisons': sum(r['independent_comparisons'] for r in records), 'native_refusals': len(refusals), 'all_checks_passed': True}, indent=2))
