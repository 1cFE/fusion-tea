"""WI-075 normative seed tests; native regenerated route is a separate gate."""
from __future__ import annotations
import importlib.util
import math
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
SEEDS = ROOT / 'work/active/WI-075_supplied-magnet-design-evaluation/seeds'


def load_seed(name):
    spec = importlib.util.spec_from_file_location('wi075_' + name, SEEDS / (name + '_impl.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

STATE = load_seed('winding_operating_state')
PROCUREMENT = load_seed('winding_pack_procurement_cost')
HARDWARE = dict(reference_turns=308., wp_side=.36)
PURCHASE = dict(n_coils=48., reference_turns=308., f_set=.8701298701298701, c_coil=25.,
                tape_volume_in=12., tape_width=.006, tape_thickness=56e-6, tape_price_per_m=20.,
                winding_rate_1990=480., cost_escalation=2.558530986993114,
                nonplanar_factor=1.9, material_cost_in=2000000.)


def test_installed_turn_identity_and_area_units():
    assert STATE.calculate(HARDWARE | {'turn_current': 50000.}) == pytest.approx(
        dict(I_coil=15400000., j_wp_effective=15400000./129600.))


def test_fixed_hardware_excitation_does_not_change_procurement():
    purchase = PROCUREMENT.calculate(PURCHASE)
    states = [STATE.calculate(HARDWARE | {'turn_current': current}) for current in (42000., 46000.)]
    assert states[1]['I_coil']/states[0]['I_coil'] == pytest.approx(46/42)
    assert states[1]['j_wp_effective']/states[0]['j_wp_effective'] == pytest.approx(46/42)
    assert PROCUREMENT.calculate(PURCHASE) == purchase
    assert purchase['conductor_length'] == pytest.approx(48*308*.8701298701298701*25)


def test_low_high_supplied_pack_current_margin_and_procurement():
    # Existing law, supported 22 T, 20 K, 6 mm x 56 um; ideal retention scenario.
    current = 50000.*22./24.9
    margins = []
    rows = []
    for side in (.20, .60):
        volume = .8780864197530865 * 48 * side**2 * 25
        tape_fraction = 1-.35-.12-.36-.08
        row = PROCUREMENT.calculate(PURCHASE | {'tape_volume_in': volume*tape_fraction})
        n_reference = (row['tape_length']/row['conductor_length'])*PURCHASE['f_set']/.8780864197530865
        tape_capacity = 200.*(.006/.004)*(22./20.)**(-.6)
        margins.append(.8-current/(n_reference*tape_capacity))
        rows.append(row)
        state = STATE.calculate(HARDWARE | {'wp_side':side, 'turn_current':current})
        assert state['I_coil'] == 308.*current
    assert margins[0] < 0 < margins[1]
    assert rows[1]['tape_length']/rows[0]['tape_length'] == pytest.approx(9.)
    assert rows[1]['conductor_length'] == rows[0]['conductor_length']
    assert rows[1]['winding_fabrication_cost'] == rows[0]['winding_fabrication_cost']


def test_optional_density_construction_replays_as_supplied_design():
    current, density, turn_current = 15400000., 119., 50000.
    selected = dict(reference_turns=current/turn_current, wp_side=math.sqrt(current/density)/1000.)
    state = STATE.calculate(selected | {'turn_current':turn_current})
    assert state == pytest.approx(dict(I_coil=current,j_wp_effective=density))
    assert STATE.calculate(selected | {'turn_current':turn_current*.9})['I_coil'] == pytest.approx(current*.9)


@pytest.mark.parametrize('key', ['reference_turns','turn_current','wp_side'])
@pytest.mark.parametrize('bad', [0.,-1.,float('nan'),float('inf'),True])
def test_invalid_supplied_state_rejected(key,bad):
    with pytest.raises(ValueError, match=key):
        STATE.calculate(HARDWARE | {'turn_current':50000.,key:bad})


@pytest.mark.parametrize('changes', [dict(reference_turns=1e308),dict(wp_side=1e200),
                                      dict(wp_side=1e-200),dict(reference_turns=1e-300,turn_current=1e-300)])
def test_state_overflow_and_underflow_refused(changes):
    with pytest.raises(ValueError):
        STATE.calculate(HARDWARE | {'turn_current':50000.} | changes)


@pytest.mark.parametrize('key', ['reference_turns','n_coils','c_coil','tape_width','tape_thickness'])
@pytest.mark.parametrize('bad', [0.,-1.,float('nan')])
def test_procurement_invalid_hardware_refused(key,bad):
    with pytest.raises(ValueError):
        PROCUREMENT.calculate(PURCHASE | {key:bad})


def test_procurement_zero_priced_tape_and_winding_valid():
    out = PROCUREMENT.calculate(PURCHASE | {'tape_volume_in':0.,'winding_rate_1990':0.,'material_cost_in':0.})
    assert out['cost'] == 0.
    assert out['conductor_length'] > 0


def test_procurement_turns_change_labor_not_supplied_tape():
    base = PROCUREMENT.calculate(PURCHASE)
    twice = PROCUREMENT.calculate(PURCHASE | {'reference_turns':616.})
    assert twice['conductor_length'] == 2*base['conductor_length']
    assert twice['winding_fabrication_cost'] == 2*base['winding_fabrication_cost']
    assert twice['tape_length'] == base['tape_length']


@pytest.fixture
def independent_oracle(monkeypatch):
    import importlib
    monkeypatch.syspath_prepend(str(ROOT / 'exploration/stellarator_e2e'))
    oracle = importlib.import_module('verify_stellaris')
    baseline = dict(oracle.IN)
    def run(**changes):
        monkeypatch.setattr(oracle, 'IN', baseline | changes)
        return oracle.compute()
    return run


def test_independent_oracle_fixed_hardware_excitation(independent_oracle):
    rows = [independent_oracle(magnet_turn_current=50000*field/24.9, magnet_allow_field_extrapolation=0.)
            for field in (21.,23.)]
    for key in ('coverage_wp_side','support_mass','m_casing','tape_length','conductor_length',
                'winding_fabrication_cost','winding_pack','magnet_structure','magnet_capital_rollup',
                'thermal_area_cold','conductor_parallel_tapes_reference'):
        assert rows[0][key] == rows[1][key], key
    for key in ('winding_I_coil','winding_j_wp_effective','B_peak','sigma_wp','W_mag',
                'thermal_q_lead_cold','conductor_margin_fraction'):
        assert rows[0][key] != rows[1][key], key


def test_independent_oracle_supplied_pack_straddles_current_capacity(independent_oracle):
    rows = [independent_oracle(magnet_wp_side=side,magnet_turn_current=50000*22/24.9,
                              magnet_allow_field_extrapolation=0.) for side in (.20,.60)]
    assert rows[0]['conductor_margin_fraction'] < 0 < rows[1]['conductor_margin_fraction']
    assert rows[0]['coverage_wp_side'] == .20
    assert rows[1]['coverage_wp_side'] == .60
    assert rows[1]['tape_length']/rows[0]['tape_length'] == pytest.approx(9.)
    assert rows[0]['conductor_length'] == rows[1]['conductor_length']
    assert rows[0]['fit_minimum_margin'] > 0 > rows[1]['fit_minimum_margin']


def test_independent_oracle_mass_propagates_without_excitation_selection(independent_oracle):
    a = independent_oracle(magnet_support_mass=100000.,cryo_q_nuc_structure=10.)
    b = independent_oracle(magnet_support_mass=200000.,cryo_q_nuc_structure=10.)
    assert b['structure_nuclear'] == 2*a['structure_nuclear']
    assert b['magnet_structure'] == 2*a['magnet_structure']
    for key in ('B_peak','winding_I_coil','tape_length'):
        assert a[key] == b[key]
    c = independent_oracle(magnet_m_casing=1000.,magnet_legacy_casing_fraction=1.)
    d = independent_oracle(magnet_m_casing=2000.,magnet_legacy_casing_fraction=1.)
    assert d['magnet_structure']-c['magnet_structure'] == pytest.approx(48*1000*18)
    with pytest.raises(ValueError,match='mass'):
        independent_oracle(magnet_m_casing=-1.,magnet_legacy_casing_fraction=0.)


@pytest.mark.parametrize('key', ['magnet_I_coil','magnet_j_wp','magnet_sizing_mode',
                                'magnet_inventory_multiplier','magnet_support_coefficient','magnet_m_casing_ref'])
def test_independent_oracle_retired_controls_rejected(independent_oracle,key):
    with pytest.raises(ValueError,match='retired magnet oracle inputs'):
        independent_oracle(**{key:1.})


@pytest.mark.parametrize('field', [19.,33.])
def test_independent_oracle_keeps_current_performance_domain(independent_oracle,field):
    with pytest.raises(ValueError):
        independent_oracle(magnet_turn_current=50000*field/24.9)
