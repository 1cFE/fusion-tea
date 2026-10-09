"""Reproduce WI-096 salt-count component evidence, without package execution.

Uses original WI-067/WI-078 fixtures and retained WI-080 native source tuple.
This checks bit preservation and count/price behavior; native assembly validation
is separate. Run via .codex-test/run python <this-file> --out <fresh-path>.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import re
import struct

ROOT = Path(__file__).resolve().parents[4]
OLD_BODY = Path('exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py')
NEW_BODY = Path('exploration/component_alternatives/bodies/cooling_equipment_selected_pumps/cooling_equipment_with_selected_salt_pump_count_impl.py')
OLD_MODEL = Path('models/library/analyses/mfe_cooling_equipment.sysml')
NEW_MODEL = Path('models/library/analyses/cooling_equipment_selected_pumps.sysml')
INTERFACE = Path('work/active/WI-067_installed-cooling-equipment-costs/evidence/equipment-interface.json')
SELECTED = Path('work/active/WI-078_supplied-cooling-design-point-evaluation/evidence/selected-defaults.json')
BASELINE = Path('work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exact(left, right):
    if isinstance(left, bool) or isinstance(right, bool):
        return type(left) is type(right) and left is right
    return struct.pack('!d', left) == struct.pack('!d', right)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    old, new = load(OLD_BODY, 'original'), load(NEW_BODY, 'selected_count')
    fixture = {x['name']: x['default'] for x in json.loads((ROOT / INTERFACE).read_text())['inputs']}
    fixture.update(json.loads((ROOT / SELECTED).read_text())['selected_inputs'])
    fixture.update(enabled=True, stainless_fabrication_usd2017_per_kg=310.)
    baseline = json.loads((ROOT / BASELINE).read_text())['outputs']
    prefix = 'stellarator_09__stellaris__heat_transport__primary_loop__'
    nominal = fixture | {'n_loops': 14.}
    for target, source in {'mdot_loop': 'mdot_loop', 'dp_loop': 'dp_loop', 'helium_suction_K': 'T_comp_in', 'helium_hot_K': 'T_out', 'primary_shaft_MW': 'w_fluid', 'primary_electric_MW': 'p_elec', 'q_ihx_MW': 'q_ihx'}.items():
        nominal[target] = baseline[prefix + source]
    cases = {
        'retained_fixture': fixture,
        'retained_native_source_nominal': nominal,
        'adverse_duty_110_percent': nominal | {'q_ihx_MW': nominal['q_ihx_MW'] * 1.1},
        'adverse_ten_circuits': nominal | {'n_loops': 10.},
        'zero_discount': nominal | {'discount': 0.},
        'dormant': {'enabled': False},
    }
    replay = {}
    for name, inputs in cases.items():
        before = old.calculate(inputs)
        after = new.calculate(inputs | {'salt_pumps_per_circuit': 2})
        mismatches = [key for key in before if not exact(before[key], after[key])]
        assert not mismatches, (name, mismatches)
        replay[name] = {'original_inputs': inputs, 'new_input': {'salt_pumps_per_circuit': 2}, 'old_outputs': before, 'new_outputs': after, 'bit_exact_old_output_count': len(before), 'mismatches': mismatches}

    # New salt-count changes must not reach primary physics, geometry, work or stock.
    held = ('salt_flow', 'salt_shaft_MW', 'salt_electric_MW', 'conversion_heat_MW', 'salt_return_C', 'ihx_installed_area', 'ihx_required_area', 'hx_purchase', 'secondary_pipe_purchase', 'salt_inventory_mass', 'salt_inventory_cost', 'secondary_spare', 'primary_vendor', 'primary_installation', 'primary_spare', 'circulator_count', 'circulator_flow', 'circulator_shaft_MW', 'circulator_electric_MW', 'bundle_event_purchase', 'bundle_event_installation', 'bundle_event_removal')
    offers = []
    for n in (10, 11, 12, 14):
        for flow in (225., 250.):
            values = nominal | {'n_loops': n, 'salt_design_flow_kg_s': flow}
            ref = new.calculate(values | {'salt_pumps_per_circuit': 2})
            for k in (2, 3, 4):
                row = new.calculate(values | {'salt_pumps_per_circuit': k})
                assert all(exact(row[key], ref[key]) for key in held)
                assert row['salt_pump_count'] == n * k
                assert math.isclose(row['secondary_vendor'], ref['secondary_vendor'] * k / 2, rel_tol=1e-15)
                assert row['salt_machine_event_purchase'] == row['secondary_vendor']
                assert row['salt_machine_event_installation'] == row['secondary_installation']
                assert row['salt_machine_event_removal'] == row['secondary_installation'] * values['removal_multiplier']
                assert row['salt_pump_electric_MW'] == row['salt_electric_MW'] / (n * k)
                assert row['total_salt_flow_kg_s'] == values['q_ihx_MW'] * 1e6 / (1560 * 195)
                assert math.isclose(row['installed_total_UA_MW_K'], n * 267.8 / ((35 - 19.3) / math.log(35 / 19.3)), rel_tol=1e-15)
                changed = new.calculate(values | {'salt_pumps_per_circuit': k, 'q_ihx_MW': values['q_ihx_MW'] * 1.1})
                for key in ('secondary_vendor', 'secondary_spare', 'salt_inventory_cost', 'salt_machine_event_purchase', 'salt_machine_event_installation', 'salt_machine_event_removal', 'installed_total'):
                    assert exact(changed[key], row[key]), key
                offers.append({'n': n, 'k': k, 'selected_flow_kg_s': flow, 'per_pump_flow_kg_s': row['salt_pump_flow'], 'flow_margin_kg_s': flow - row['salt_pump_flow'], 'operating_shaft_hp': row['pump_shaft_hp'], 'selected_shaft_hp': row['design_pump_shaft_hp'], 'operating_type_ok': row['pump_type_ok'], 'selected_type_ok': row['design_pump_type_ok'], 'active_purchase': row['secondary_vendor'], 'one_spare_purchase': row['secondary_spare'], 'salt_machine_event_purchase': row['salt_machine_event_purchase'], 'salt_machine_event_installation': row['salt_machine_event_installation'], 'salt_machine_event_removal': row['salt_machine_event_removal']})
    refusals = []
    for k in (0, -1, 2.5, True, float('nan'), float('inf')):
        try:
            new.calculate(nominal | {'salt_pumps_per_circuit': k})
        except ValueError as error:
            refusals.append({'count': str(k), 'refusal': str(error)})
        else:
            raise AssertionError(('invalid count accepted', k))

    old_order = re.findall(r'out attribute (\w+)\s*:', (ROOT / OLD_MODEL).read_text())
    new_order = re.findall(r'out attribute (\w+)\s*:', (ROOT / NEW_MODEL).read_text())
    assert new_order[:len(old_order)] == old_order
    assert set(new_order) == set(new.OUTPUT_NAMES)
    assert len(new_order) == len(new.OUTPUT_NAMES)
    inputs_old = re.findall(r'in attribute (\w+)\s*:', (ROOT / OLD_MODEL).read_text())
    inputs_new = re.findall(r'in attribute (\w+)\s*:', (ROOT / NEW_MODEL).read_text())
    assert set(inputs_new) - set(inputs_old) == {'salt_pumps_per_circuit_in'}
    assert set(inputs_old).issubset(inputs_new)
    paths = (OLD_BODY, NEW_BODY, OLD_MODEL, NEW_MODEL, INTERFACE, SELECTED, BASELINE)
    receipt = {'scope': 'Component calculate execution and textual SysML ABI census; native package integration remains separate.', 'provenance_sha256': {str(path): hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths}, 'input_additions': ['salt_pumps_per_circuit_in'], 'output_additions': new_order[len(old_order):], 'old_output_count': len(old_order), 'new_output_count': len(new_order), 'old_sysml_output_order': old_order, 'new_sysml_output_order': new_order, 'mapping_output_order': list(new.OUTPUT_NAMES), 'replay': replay, 'offers': offers, 'invalid_count_refusals': refusals, 'held_outputs_across_count': list(held)}
    args.out.write_text(json.dumps(receipt, indent=2, allow_nan=False) + '\n')
    for old_path, new_path, suffix in ((OLD_BODY, NEW_BODY, 'body'), (OLD_MODEL, NEW_MODEL, 'sysml')):
        diff = ''.join(difflib.unified_diff((ROOT / old_path).read_text().splitlines(True), (ROOT / new_path).read_text().splitlines(True), fromfile=str(old_path), tofile=str(new_path)))
        args.out.with_name(args.out.stem + '-' + suffix + '.diff').write_text(diff)
    print(json.dumps({'old_outputs': len(old_order), 'new_outputs': len(new_order), 'bit_exact_cases': len(replay), 'count_design_offer_cases': len(offers), 'invalid_count_refusals': len(refusals), 'receipt': str(args.out)}))


if __name__ == '__main__':
    main()
