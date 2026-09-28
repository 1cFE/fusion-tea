"""Native demand propagation against fixed offers and independent arithmetic."""
import json

import pytest
from tests.models.test_winding_pack_cost import ROOT, P, runtime_paths, evaluate  # noqa: F401

EVIDENCE = ROOT / 'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/propagation-acceptance.json'
THERMAL = ('q_source', 'loop_mdot_loop', 'loop_dp_loop', 'loop_w_fluid',
           'cooling_ihx_required_area', 'cooling_salt_pump_flow', 'cooling_salt_pump_shaft_MW',
           'matched_mdot_main_kg_s', 'matched_p_gross_MW', 'matched_main_UA_MW_K',
           'matched_reheat_UA_MW_K', 'cw_q_total_rejection_MW', 'cw_water_flow_kg_s',
           'cw_p_cooling_pump_electric_MW')
PRESERVED = ('cooling_ihx_installed_area', 'cooling_installed_total', 'cooling_spares_cost',
             'cooling_replacement_annual', 'cooling_primary_design', 'cooling_secondary_vendor',
             'turbine', 'heat_rejection', 'cryo_cost', 'aux_cost', 'power_supplies')
PHYSICS = ('p_aux_required', 'heat_coupled', 'divheat_q_target_peak', 'divheat_q_target_margin',
           'breeding_adequacy_production_rate', 'breeding_adequacy_required_tbr',
           'breeding_adequacy_numerical_margin')
CRYO = ('p_cold', 'thermal_q_shield', 'p_cryo', 'p_cryo_cold', 'p_cryo_shield',
        'capability_cold_stage_margin', 'capability_intercept_stage_margin')


@pytest.mark.codegen_available
def test_fixed_equipment_accepts_changing_requirements_without_resizing(evaluate):
    import oracle_entry as o
    cases = {
        'baseline': {},
        'density_low': {'n_e0': o.vs.IN['n_e0'] * .99},
        'density_high': {'n_e0': o.vs.IN['n_e0'] * 1.01},
        'support_heat_high': {'cryo_g_per_coil': o.vs.IN['cryo_g_per_coil'] * 1.2},
        'cold_cop_low': {'f_carnot_cryo': o.vs.IN['f_carnot_cryo'] * .9},
        'shield_cop_low': {'f_carnot_shield': o.vs.IN['f_carnot_shield'] * .9},
    }
    catalog = json.loads((ROOT / 'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    ids = {e['source_local_identity']: e['constraint_id'] for e in catalog['constraint_catalog']['concrete_entries']}
    native_rows, expected_rows, records = {}, {}, {}
    checked = THERMAL + PRESERVED + PHYSICS + CRYO
    checked += tuple(f'capability_{n}_{f}' for n in ('helium_flow', 'salt_flow', 'main_UA', 'water_flow')
                     for f in ('margin', 'defined'))
    for name, overrides in cases.items():
        public = {next(k for k, v in o.ENTRY_KEY_TO_ORACLE_INPUT.items() if v == key).removeprefix(P): value
                  for key, value in overrides.items()}
        native = evaluate(public)
        expected = o._compute(overrides)
        actual = {key: native.outputs[o.ORACLE_OUTPUT_TO_CHANNEL[key]] for key in checked}
        for key, value in actual.items():
            assert value == pytest.approx(expected[key], rel=1e-10, abs=1e-8), (name, key)
        required_heat_ok = expected['p_aux_required'] <= expected['heat_coupled']
        divertor_ok = expected['divheat_q_target_peak'] <= o.vs.IN['q_target_limit']
        breeding_ok = expected['breeding_adequacy_defined_flag'] >= 1 and expected['breeding_adequacy_numerical_margin'] >= 0
        predicates = {'sustainment_ok': required_heat_ok, 'divertor_heat_ok': divertor_ok, 'tbr_ok': breeding_ok}
        if name.startswith('density_'):
            for screen in ('helium_flow', 'salt_flow', 'main_UA', 'water_flow'):
                predicates[screen + '_capacity_ok'] = expected[f'capability_{screen}_capacity_ok']
        if name == 'support_heat_high':
            for screen in ('cold_stage', 'intercept_stage'):
                predicates[screen + '_capacity_ok'] = expected[f'capability_{screen}_capacity_ok']
        # Resolve actual assertion names from the catalog; names must exist.
        for predicate, passing in predicates.items():
            assert native.responses[ids[predicate]] == ('satisfied' if passing else 'violated'), (name, predicate)
        state = {g: native.outputs[o.ORACLE_OUTPUT_TO_CHANNEL[f'capability_{g}_state_supported']]
                 for g in ('helium', 'salt', 'steam', 'water', 'cryogenic')}
        records[name] = {'oracle_overrides': overrides, 'public_overrides': public, 'values': actual,
                         'state_supported': state, 'existing_predicates': {k: native.responses[ids[k]] for k in predicates},
                         'water_electric_boundary': {
                             'native_margin': native.outputs[o.ORACLE_OUTPUT_TO_CHANNEL['capability_water_electric_margin']],
                             'oracle_margin': expected['capability_water_electric_margin'],
                             'native_capacity_ok': native.outputs[o.ORACLE_OUTPUT_TO_CHANNEL['capability_water_electric_capacity_ok']],
                             'oracle_capacity_ok': expected['capability_water_electric_capacity_ok']}}
        native_rows[name], expected_rows[name] = actual, expected
    baseline = native_rows['baseline']
    for name in cases:
        for key in PRESERVED:
            assert native_rows[name][key] == baseline[key], (name, key)
    for name in ('density_low', 'density_high'):
        for key in THERMAL:
            assert native_rows[name][key] != baseline[key], (name, key)
        for key in ('p_aux_required', 'divheat_q_target_peak', 'breeding_adequacy_production_rate'):
            assert native_rows[name][key] != baseline[key], (name, key)
        assert not records[name]['state_supported']['helium']
        assert records[name]['state_supported']['salt']
        assert records[name]['state_supported']['steam']
        assert native_rows[name]['capability_helium_flow_defined'] == 0
        assert native_rows[name]['capability_salt_flow_defined'] == 1
        assert native_rows[name]['capability_main_UA_defined'] == 1
    for key in CRYO:
        assert native_rows['support_heat_high'][key] != baseline[key], key
    assert records['support_heat_high']['state_supported']['cryogenic']
    for name, electric in [('cold_cop_low', 'p_cryo_cold'), ('shield_cop_low', 'p_cryo_shield')]:
        assert native_rows[name][electric] > baseline[electric]
        for key in ('p_cold', 'thermal_q_shield', 'capability_cold_stage_margin', 'capability_intercept_stage_margin'):
            assert native_rows[name][key] == baseline[key], (name, key)
    EVIDENCE.write_text(json.dumps({'scope': 'Six fixed-offer native cases; independent selected-channel arithmetic and existing predicates.',
                                   'water_electric_boundary': 'Retained raw native/oracle outcomes; no tolerance applied to physical verdicts.',
                                   'cases': records}, indent=2) + '\n')
