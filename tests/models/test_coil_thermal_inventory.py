"""WI-059: independent conservation, dormant identity and approximation-domain checks."""
import importlib
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'work/active/WI-059_coil-thermal-and-total-support-inventory/evidence'


@pytest.fixture(scope='module')
def oracle():
    sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e'))
    return importlib.import_module('verify_stellaris')


def test_two_stage_energy_conservation_and_direct_supply(oracle):
    p = dict(oracle.IN)
    r = oracle._coil_thermal_inventory(p, 25, .5)
    hot_radiation = r['area_shield']*p['cryo_q_mli']
    hot_support = p['magnet_n_coils']*p['cryo_g_per_coil']*p['cryo_k_shield']*(300-77)
    lead_power = r['q_lead_cold']+r['q_lead_shield']
    assert r['q_cold']+r['q_shield'] == pytest.approx(hot_radiation+hot_support+lead_power, rel=1e-14)
    assert r['p_drive'] == pytest.approx(lead_power*1e-6+.0075, rel=1e-14)
    # Independent original-source witness from T005, before generated implementation.
    refrigeration = r['q_cold']*1e-6*280/(.2*20)+r['q_shield']*1e-6*223/(.2*77)
    assert refrigeration+r['p_drive']-.0075 == pytest.approx(1.331556430, rel=1e-9)


@pytest.mark.parametrize('temperature', [10, 20, 30])
def test_supported_cold_endpoints(oracle, temperature):
    r = oracle._coil_thermal_inventory(oracle.IN | {'T_cold_cryo': temperature}, 25, .5)
    assert r['q_cold'] > 0 and r['q_shield'] > 0


@pytest.mark.parametrize('change', [
    {'T_cold_cryo': 9}, {'T_cold_cryo': 31}, {'T_shield_cryo': 100},
    {'T_amb_cryo': 400}, {'f_carnot_shield': 0}, {'f_carnot_cryo': 1.01},
    {'cryo_q_mli': -1}, {'cryo_emittance': 100}, {'cryo_L0': float('nan')},
    {'cryo_sigma_SB': -1}, {'magnet_turn_current': float('inf')},
])
def test_unsupported_inventory_refuses(oracle, change):
    with pytest.raises(ValueError):
        oracle._coil_thermal_inventory(oracle.IN | change, 25, .5)


def test_disabled_inventory_does_not_evaluate_new_domain(oracle):
    p = oracle.IN | {'cryo_inventory_enabled': False, 'T_cold_cryo': 4,
                     'T_amb_cryo': 50, 'T_shield_cryo': -1, 'f_carnot_shield': 0}
    assert set(oracle._coil_thermal_inventory(p, 25, .5).values()) == {0.0}


def test_legacy_replay_preserves_entering_physics_and_non_tape_accounts(oracle):
    entering = json.loads((EVIDENCE/'entering_oracle.json').read_text())
    saved = oracle.IN.copy()
    try:
        oracle.IN.update(magnet_insulation_sheet_price=0., cryo_inventory_enabled=False, magnet_support_coefficient=0,
                         magnet_legacy_casing_fraction=1, cryo_joint_drive_fraction=0,
                         cryo_q_nuc_structure=0, structure_residual_fraction=1)
        actual = oracle.compute()
    finally:
        oracle.IN.clear(); oracle.IN.update(saved)
    # WI-060 changes the selected tape account and its declared capital descendants.
    from tests.models.current_mfe_regressions import WI040_CHANGED_ECONOMICS
    changed = set(WI040_CHANGED_ECONOMICS) | {'winding_pack', 'tape_procurement_cost',
        'conductor_cost_per_kAm_effective', 'cas30_capital'}
    for key, value in entering['outputs'].items():
        if key not in changed:
            assert actual[key] == pytest.approx(value, rel=1e-12, abs=1e-12), key


@pytest.fixture(scope='module')
def native_inventory():
    sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
    sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/pkg'))
    mod = importlib.import_module('stellarator_tea.modules.mfe_cryo_inventory.coil_thermal_inventory')
    impl = importlib.import_module('stellarator_tea.handwritten.mfe_cryo_inventory.coil_thermal_inventory_impl')
    return mod.Coil_Thermal_InventoryInput, impl.run_coil_thermal_inventory


def native_parameters(oracle):
    p = oracle.IN
    return dict(inventory_enabled=True, T_cold=p['T_cold_cryo'], T_shield=p['T_shield_cryo'],
                T_amb=p['T_amb_cryo'], f_carnot_cold=p['f_carnot_cryo'], f_carnot_shield=p['f_carnot_shield'],
                n_coils=48, c_coil=25, wp_side=.5, I_turn=50000, n_leads=12,
                L0=p['cryo_L0'], sigma_SB=p['cryo_sigma_SB'], f_lead=p['cryo_f_lead'],
                t_case=p['cryo_t_case'], shield_area_ratio=p['cryo_shield_area_ratio'],
                eps_eff=p['cryo_emittance'], q_MLI=p['cryo_q_mli'], g_per_coil=p['cryo_g_per_coil'],
                k_c=p['cryo_k_cold'], k_s=p['cryo_k_shield'], joint_drive_fraction=1, p_joint=.0075)


def test_native_inventory_matches_independent_component_oracle(native_inventory, oracle):
    cls, run = native_inventory
    names = ('q_radiation_cold', 'q_radiation_shield', 'q_lead_shield', 'q_support_cold',
             'q_shield', 'q_lead_cold', 'area_shield', 'q_support_shield', 'q_cold', 'area_cold', 'p_drive')
    for temperature in (10, 20, 30):
        params = native_parameters(oracle) | {'T_cold': temperature}
        actual = dict(zip(names, run(cls(**params)), strict=True))
        expected = oracle._coil_thermal_inventory(oracle.IN | {'T_cold_cryo': temperature}, 25, .5)
        assert actual == pytest.approx(expected, rel=1e-12)


@pytest.mark.parametrize('changes', [{'T_cold': 9}, {'T_cold': 31}, {'T_shield': 100},
                                    {'T_amb': 400}, {'f_carnot_cold': 0}, {'eps_eff': 100}])
def test_native_inventory_refuses_unsupported_scenarios(native_inventory, oracle, changes):
    cls, run = native_inventory
    with pytest.raises(ValueError):
        run(cls(**(native_parameters(oracle) | changes)))


def test_native_inventory_dormant_early_exit(native_inventory, oracle):
    cls, run = native_inventory
    params = native_parameters(oracle) | {'inventory_enabled': False, 'T_cold': 4,
                                          'T_amb': 50, 'T_shield': -1, 'f_carnot_shield': 0}
    assert set(run(cls(**params))) == {0.0}


@pytest.mark.parametrize('change', [
    {'cryo_rho_structure': 0}, {'cryo_q_nuc_structure': -1},
    {'magnet_support_coefficient': -1}, {'magnet_support_exponent': 0},
    {'magnet_legacy_casing_fraction': 1.1}, {'structure_residual_fraction': -1},
])
def test_new_support_inputs_refuse_nonphysical_domain(oracle, change):
    saved=oracle.IN.copy()
    try:
        oracle.IN.update(change)
        with pytest.raises(ValueError, match='oracle coil support'):
            oracle.compute()
    finally:
        oracle.IN.clear(); oracle.IN.update(saved)


def test_total_shield_balance_allows_outgoing_radiation_with_other_heat(oracle):
    p=oracle.IN | {'cryo_q_mli': 0}
    r=oracle._coil_thermal_inventory(p,25,.5)
    assert r['q_radiation_shield'] < 0 < r['q_shield']



def test_study_route_preserves_the_authored_boolean_control():
    from exploration.stellarator_e2e.studies import study_route as route
    key=route.P+'cryoplant__inventory_enabled'
    assert route.validate_proposal({key:False}) == {key:False}
    assert route.validate_proposal({key:False})[key] is False
    assert route.validate_proposal({route.P+'plasma__R':False}) is None


def test_turn_current_changes_lead_heat_but_not_geometry_heat(native_inventory, oracle):
    cls,run=native_inventory
    base=run(cls(**native_parameters(oracle)))
    half=run(cls(**(native_parameters(oracle)|{'I_turn':25000})))
    # Wrapper tuple positions: cold lead5, shield lead2; radiation0/1, supports3/7.
    assert half[5] == pytest.approx(base[5]/2)
    assert half[2] == pytest.approx(base[2]/2)
    assert [half[i] for i in (0,1,3,7)] == [base[i] for i in (0,1,3,7)]
    assert half[10]-.0075 == pytest.approx((base[10]-.0075)/2)
