"""WI-099 magnet conductor alternatives through the generated magnet_materials_tea package.

Every test evaluates design section 6 case records through the reviewed study route (`case_point` -> stock
PreparedEvaluator), never the handwritten bodies directly. Covers the contract section 5 source-data and
anchor-reproduction tests with their tolerances, the MR-7 acceptance tests (insufficient/sufficient supplied
designs for acceptance, fit, copper, steel and capacity; field varied with hardware fixed; hardware isolation,
design D5; unsupported case per conductor with no ranking) and the design D1 reference-offer margins.
Run: .codex-test/run python -m pytest tests/models/test_magnet_materials.py
"""
from __future__ import annotations

import copy
import json
import math
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = json.loads((ROOT / 'work/active/WI-099_magnet-conductor-alternatives/reference-case.json').read_text())
PARTS = ('duty', 'economics', 'nb3sn', 'rebco')
STRAND_AREA = math.pi / 4 * 0.82e-3 ** 2  # m2; Tsui C (A T m-2) x whole-strand area = C1 (A T)
# Breschi et al. 2017 Table III (PDF p.24): p, q, Ca1, Ca2, eps0a (fraction), Bc20, Tc0, C1; expected Ic at
# (12 T, 6.7 K, -0.3 %) from check-nb3sn.md Recheck r3 item 7.
BRESCHI = {
    'Jastec TFJA7-8': ((0.84, 2.570, 47.02, 11.76, 0.00231, 32.35, 16.22, 33000.0), 125.83),
    'OST TFEU9': ((0.746, 2.335, 79.94, 45.04, 0.00207, 32.59, 16.26, 28622.88), 138.92),
    'BEAS TFEU10-12': ((0.549, 1.726, 133.95, 111.72, 0.00389, 30.66, 16.07, 13173.6), 111.98),
    'OST TFEU11-13': ((0.999, 2.581, 218.03, 187.61, 0.00156, 31.91, 16.12, 42910.56), 136.87),
    'Kiswire TFKO4-8': ((0.827, 2.488, 70.28, 32.91, 0.0044, 31.58, 15.95, 35986.0), 138.28),
    'Hitachi TFJA6L/9-10': ((0.979945, 2.561, 44.4841, 8.5389, 0.002525, 31.7556, 16.7055, 35557.3), 129.11),
    'ChMP TFRF4-7': ((0.519, 1.662, 49.62, 9.51, 0.00259, 29.52, 16.62, 15250.0), 126.99),
    'OST TFUS5R-7R': ((0.471, 1.670, 44.33, 0.0, 0.00194, 30.59, 16.16, 14928.0), 121.25),
    'Luvata TFUS7L-8': ((0.652, 2.000, 46.04, 0.0, 0.00216, 31.8, 16.16, 20292.0), 121.41),
    'WST TFCN5-6': ((0.578, 2.211, 47.52, 0.0, 0.00218, 34.22, 16.26, 20823.0), 127.31),
}
# Tsui & Hampshire 2012 Table 5 (full range), C converted to A*T per 0.82 mm strand.
BEAS2 = (0.489, 1.618, 226.93, 203.86, 0.00187, 30.28, 16.02, 2.227e10 * STRAND_AREA)
OST = (0.746, 2.335, 79.94, 45.04, 0.00207, 32.59, 16.26, 5.421e10 * STRAND_AREA)
LAW_KEYS = ('p', 'q', 'Ca1', 'Ca2', 'eps0a', 'Bc20', 'Tc0', 'C1')
# Stellaris Table 7 envelope per turn at anchor S: 0.36^2 m2 x 1e6 / 308 turns (design section 7, A2).
TABLE7_AREA = 0.36 ** 2 * 1e6 / 308
TABLE7 = dict(tape=0.09, copper=0.35, solder=0.12, steel=0.36, helium=0.08)


def same(a, b):
    return (math.isnan(a) and math.isnan(b)) or a == b


class Row:
    """One evaluation, read through the reviewed interface's design-meaning names."""

    def __init__(self, evidence, interface):
        self.evidence, self.interface = evidence, interface

    def __getitem__(self, name):
        return self.evidence.outputs[self.interface['output_channels'][name]]

    def verdict(self, name):
        return self.evidence.responses[self.interface['constraint_ids'][name]]

    def named(self):
        return {name: self.evidence.outputs[channel] for name, channel in self.interface['output_channels'].items()}


@pytest.fixture(scope='module')
def evaluate(tmp_path_factory):
    teax = str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit')
    sys.path.insert(0, teax)
    from simkit.study.bridge import CandidateBridge
    from exploration.magnet_materials.studies import study_route as route
    prepared = route.prepare(route.PACKAGE_DIR, tmp_path_factory.mktemp('wi099-native'))
    bridge = CandidateBridge(prepared.entry_models)
    interface = route.interface()

    def run(changes=None, fixed=None):
        case = {part: copy.deepcopy(REFERENCE[part]) for part in PARTS}
        for dotted, value in (changes or {}).items():
            part, name = dotted.split('.')
            if name not in case[part]:
                raise KeyError(dotted)
            case[part][name] = value
        return Row(prepared.evaluate(bridge.build(route.case_point(case, fixed))), interface)

    yield run
    sys.path.remove(teax)


def strand(parameters, B, T, eps, **extra):
    """Changes that evaluate one Nb3Sn strand at (B, T_conductor = T, eps): nuclear rise 0, B_peak = B."""
    changes = {'nb3sn.' + key: value for key, value in zip(LAW_KEYS, parameters)}
    changes.update({'duty.B_peak': B, 'nb3sn.T_supply': T, 'nb3sn.nuclear_rise': 0.0, 'nb3sn.eps_intrinsic': eps,
                    'nb3sn.strand_diameter': 0.82e-3})
    changes.update(extra)
    return changes


# ----------------------------------------------------------------------------------------- source data (contract 5)

def test_tsui_beas2_iter_specification_point(evaluate):
    ic = evaluate(strand(BEAS2, 12.0, 4.22, 0.0))['nb3sn.conductor.ic_strand_op']
    assert ic == pytest.approx(201.30, abs=0.01)
    assert ic > 190.0  # ITER TF qualification specification, Tsui Table 1
    assert abs(ic - 197.0) <= 5.0  # Tsui Fig. 9(a) peak reading, plot tolerance


@pytest.mark.parametrize('B,T,eps,expected', [
    (12.0, 4.2, 0.0, 201.85), (12.0, 5.2, -0.003, 152.95), (12.0, 6.7, -0.003, 106.83), (8.0, 6.7, -0.003, 238.93),
    (12.0, 6.7, -0.006, 73.11), (8.0, 5.2, -0.003, 305.43), (9.0, 6.7, -0.003, 197.54), (9.0, 5.2, -0.003, 258.10),
    (10.0, 6.7, -0.003, 162.50), (10.0, 5.2, -0.003, 217.79), (11.0, 6.7, -0.003, 132.56), (11.0, 5.2, -0.003, 183.08)])
def test_beas2_check_a_points(evaluate, B, T, eps, expected):
    """check-nb3sn.md section 3 table and screen comparison (BEAS II, Tsui Table 5(c)), 0.01 A."""
    assert evaluate(strand(BEAS2, B, T, eps))['nb3sn.conductor.ic_strand_op'] == pytest.approx(expected, abs=0.01)


def test_ost_check_a_point(evaluate):
    """Tsui Table 5(a) with C x 0.82 mm strand area at (12 T, 6.7 K, -0.3 %): 138.94 A (check-nb3sn.md Recheck r2 item 6)."""
    assert evaluate(strand(OST, 12.0, 6.7, -0.003))['nb3sn.conductor.ic_strand_op'] == pytest.approx(138.94, abs=0.01)


@pytest.mark.parametrize('label', sorted(BRESCHI))
def test_breschi_production_sets(evaluate, label):
    parameters, expected = BRESCHI[label]
    assert evaluate(strand(parameters, 12.0, 6.7, -0.003))['nb3sn.conductor.ic_strand_op'] == pytest.approx(expected, abs=0.01)


def test_reference_strand_is_production_median(evaluate):
    values = sorted(evaluate(strand(p, 12.0, 6.7, -0.003))['nb3sn.conductor.ic_strand_op'] for p, _ in BRESCHI.values())
    assert (values[4] + values[5]) / 2 == pytest.approx(127.15, abs=0.01)
    assert values[5] == pytest.approx(BRESCHI['WST TFCN5-6'][1], abs=0.01)


def test_wst_price_conversion_point_is_computed_but_unsupported(evaluate):
    """6 T, 4.2 K, eps 0: 680.48 A (check-nb3sn.md Recheck r3 item 9), below the law's supported field."""
    row = evaluate(strand(BRESCHI['WST TFCN5-6'][0], 6.0, 4.2, 0.0))
    assert row['nb3sn.conductor.ic_strand_op'] == pytest.approx(680.48, abs=0.01)
    assert row['nb3sn.conductor.status_code'] == 0.0 and row['nb3sn.conductor.acceptance_pass'] == 0.0


@pytest.mark.parametrize('B,digitizations', [(8.0, (2.11, 2.10)), (10.0, (1.85, 1.85)), (12.0, (1.61, 1.62)), (15.0, (1.33, 1.34))])
def test_rebco_shape_ratios_within_both_digitizations(evaluate, B, digitizations):
    """Molodyk Fig. 1a, 20 K, B||c: author and checker digitizations (check-rebco-cryo-cost.md section 1), +/-0.02."""
    row = evaluate({'duty.B_peak': B, 'rebco.T_supply': 20.0, 'rebco.nuclear_rise': 0.0})
    ratio = row['rebco.conductor.ic_tape_op'] / REFERENCE['rebco']['anchor_ic']
    assert all(abs(ratio - value) <= 0.02 for value in digitizations)


def test_rebco_shape_is_log_log_between_knots(evaluate):
    row = evaluate({'duty.B_peak': 9.0, 'rebco.T_supply': 20.0, 'rebco.nuclear_rise': 0.0})
    w = math.log(9.0 / 8.0) / math.log(10.0 / 8.0)
    assert row['rebco.conductor.ic_tape_op'] / 198.0 == pytest.approx(2.11 ** (1 - w) * 1.85 ** w, rel=1e-12)
    power = evaluate({'duty.B_peak': 9.0, 'rebco.T_supply': 20.0, 'rebco.nuclear_rise': 0.0, 'rebco.shape_mode': 1.0})
    assert power['rebco.conductor.ic_tape_op'] / 198.0 == pytest.approx((9.0 / 20.0) ** -0.6, rel=1e-12)


def test_construction_p_reproduces_eu_demo_layer_1(evaluate):
    """399 x 1 mm strands, J_Cu 93.4 A/mm2, steel 9.3635 mm2/kA, residual 1.1077 mm2/kA -> 2577.2 mm2 [relative 1e-6]."""
    changes = {'duty.B_peak': 12.04, 'nb3sn.n_elements': 399.0, 'nb3sn.strand_diameter': 1e-3, 'nb3sn.steel_per_kA_rule': 9.3635,
               'nb3sn.misc_area': 1.1077 * 104.95}
    rule = evaluate(changes)
    assert rule['duty.turn_current'] == pytest.approx(104950.0, rel=1e-12)
    supplied = evaluate(changes | {'nb3sn.cu_space': rule['nb3sn.area.cu_required'], 'nb3sn.steel_area': rule['nb3sn.area.steel_required']})
    assert supplied['nb3sn.area.net_area'] == pytest.approx(68 * 37.9, rel=1e-6)
    assert supplied['nb3sn.area.cu_margin'] == 0.0 and supplied['nb3sn.area.steel_margin'] == 0.0
    assert supplied['nb3sn.area.cu_required'] == pytest.approx((104950 / 93.4 - 399 * math.pi / 4 / 2) / 0.9, rel=1e-12)


def test_construction_c_reproduces_stellaris_table_7(evaluate):
    """Anchor S, 50 kA and 24.9 T, unrounded per-kA calibration (design section 7, A2) -> 420.779220779 mm2 [relative 1e-6]."""
    per_kA = {name: fraction * TABLE7_AREA / 50 for name, fraction in TABLE7.items()}
    for name, rounded in (('copper', 2.945), ('solder', 1.010), ('helium', 0.673), ('steel', 3.030)):
        assert per_kA[name] == pytest.approx(rounded, abs=5e-4)  # contract section 4 rounded display values
    changes = {'duty.coils': 48.0, 'duty.turns': 308.0, 'duty.turn_length': 321600 / (48 * 308), 'duty.available_area': TABLE7_AREA,
               'duty.I_ref': 50000.0, 'duty.B_ref': 24.9, 'duty.B_peak': 24.9, 'rebco.shape_mode': 1.0,
               'rebco.n_elements': 100.0, 'rebco.tape_width': TABLE7['tape'] * TABLE7_AREA / (100 * 56e-6 * 1e6),
               'rebco.cabling_factor': 1.0, 'rebco.cable_void': 0.0, 'rebco.ins_fraction': 0.0, 'rebco.J_cu_rule': 0.0,
               'rebco.cu_void': 0.0, 'rebco.cu_per_kA_rule': per_kA['copper'], 'rebco.steel_per_kA_rule': per_kA['steel'],
               'rebco.B_steel_ref': 24.9, 'rebco.steel_B_scaling': 1.0, 'rebco.solder_area': per_kA['solder'] * 50,
               'rebco.misc_area': per_kA['helium'] * 50, 'rebco.cu_space': per_kA['copper'] * 50, 'rebco.steel_area': per_kA['steel'] * 50}
    row = evaluate(changes)
    assert row['rebco.area.gross_area'] == pytest.approx(420.779220779, rel=1e-6)
    assert row['rebco.area.cu_required'] == pytest.approx(TABLE7['copper'] * TABLE7_AREA, rel=1e-12)
    assert row['rebco.area.steel_required'] == pytest.approx(TABLE7['steel'] * TABLE7_AREA, rel=1e-12)
    assert row['rebco.area.fit_margin'] == pytest.approx(0.0, abs=1e-9)
    assert row['rebco.inventory.conductor_length'] == pytest.approx(321600.0, rel=1e-12)


def test_carnot_specific_power(evaluate):
    row = evaluate()
    assert row['nb3sn.refrigeration.carnot_specific_power'] == pytest.approx(65.67, abs=0.01)
    assert row['rebco.refrigeration.carnot_specific_power'] == pytest.approx(14.00, abs=0.01)


def test_ballarino_single_segment_lead_heat(evaluate):
    """sqrt(L0 (300^2 - T^2)) per kA: 46.95 W/kA at 4.2 K and 46.85 W/kA at 20 K [0.01] (check-rebco-cryo-cost.md section 5).
    The upper lead temperature is set to 300 K through the fixed intercept temperature (ambient 301 K keeps the stages ordered)."""
    one_lead = {'duty.I_ref': 1000.0, 'duty.B_ref': 10.0, 'duty.B_peak': 10.0}
    for material in ('nb3sn', 'rebco'):
        one_lead |= {f'{material}.f_lead': 1.0, f'{material}.n_leads': 1.0}
    fixed = {f'{m}.{k}': v for m in ('nb3sn', 'rebco') for k, v in (('T_shield', 300.0), ('T_amb', 301.0))}
    row = evaluate(one_lead | {'nb3sn.T_supply': 4.2}, fixed)
    assert row['nb3sn.cold_load.q_leads'] == pytest.approx(46.95, abs=0.01)
    assert row['rebco.cold_load.q_leads'] == pytest.approx(46.85, abs=0.01)
    staged = evaluate(one_lead)  # reference 77 K intercept: 12.03 W/kA at 4.5 K, 11.64 W/kA at 20 K (contract section 6)
    assert staged['nb3sn.cold_load.q_leads'] == pytest.approx(12.03, abs=0.01)
    assert staged['rebco.cold_load.q_leads'] == pytest.approx(11.64, abs=0.01)


def test_316_conductivity_integral(evaluate):
    row = evaluate()
    assert row['nb3sn.cold_load.k_integral'] == pytest.approx(326.0, rel=0.005)
    assert row['rebco.cold_load.k_integral'] == pytest.approx(307.4, rel=0.005)


def test_green_efficiency_at_18_kw(evaluate):
    row = evaluate({'nb3sn.rating_cold': 18000.0})
    assert row['nb3sn.refrigeration.eta_cold'] == pytest.approx(0.155 * 18 ** 0.23, rel=1e-9)
    assert round(100 * row['nb3sn.refrigeration.eta_cold'], 1) == 30.1  # contract prints 30.2 %; 15.5 x 18^0.23 = 30.14 %


def test_anchor_s_cold_inventory_at_20_k(evaluate):
    """Stellaris 20 K inventory reconstructs its 21.93 kW rating [0.1 %] (contract section 6)."""
    row = evaluate({'duty.I_ref': 50000.0, 'duty.B_ref': 12.0, 'duty.B_peak': 12.0, 'rebco.T_supply': 20.0,
                    'rebco.nuclear_density': 35.5, 'rebco.cold_volume': 136.56, 'rebco.radiation_ref': 270.0,
                    'rebco.conduction_ref': 590.0, 'rebco.T_conduction_ref': 20.0, 'rebco.n_leads': 12.0, 'rebco.f_lead': 1.25,
                    'rebco.p_joint_ref': 7500.0, 'rebco.I_joint_ref': 50000.0, 'rebco.load_multiplier': 1.0})
    assert row['rebco.cold_load.q_cold'] == pytest.approx(21933.902368719853, rel=1e-3)
    assert row['rebco.cold_load.q_nuclear'] == pytest.approx(4850.0, abs=10.0)
    assert row['rebco.cold_load.q_leads'] == pytest.approx(8730.0, abs=10.0)
    assert row['rebco.cold_load.q_conduction'] == 590.0


# ------------------------------------------------------------------------------------------- MR-7 acceptance tests

HARDWARE = ('inventory.conductor_length', 'inventory.element_length', 'inventory.element_mass', 'inventory.cu_mass',
            'inventory.steel_mass', 'inventory.solder_mass', 'inventory.sc_cost', 'inventory.materials_cost',
            'inventory.winding_capital', 'refrigeration.refrigerator_capital', 'refrigeration.R_equiv_kW', 'refrigeration.eta_cold')


def test_reference_offers_meet_their_allowances(evaluate):
    """Design D1: policy areas rounded up to 1e-6 mm2, so reference margins are at allowance (>= 0) at the reference duty."""
    row = evaluate()
    for material in ('nb3sn', 'rebco'):
        for margin in ('cu_margin', 'steel_margin'):
            assert 0.0 <= row[f'{material}.area.{margin}'] <= 1e-6
        assert all(row.verdict(f'{material}.{name}') == 'satisfied' for name in ('acceptance_ok', 'fit_ok', 'copper_ok', 'steel_ok', 'capacity_ok'))
        assert row[f'{material}.all_pass'] == 1.0
    assert row['pair.rankable'] == 1.0 and row['pair.pair_status'] == 1.0


@pytest.mark.parametrize('material', ['nb3sn', 'rebco'])
def test_current_margin_insufficient_and_sufficient(evaluate, material):
    n_ref = REFERENCE[material]['n_elements']
    rows = {n: evaluate({f'{material}.n_elements': float(n)}) for n in (math.floor(0.9 * n_ref), n_ref)}
    low, ref = rows[math.floor(0.9 * n_ref)], rows[n_ref]
    assert low.verdict(f'{material}.acceptance_ok') == 'violated' and ref.verdict(f'{material}.acceptance_ok') == 'satisfied'
    assert low[f'{material}.conductor.supported'] == 1.0  # a failed, supported evaluation, not an unsupported one
    for n, row in rows.items():  # evaluated as supplied, never resized; inventory and cost follow the supplied count
        assert row[f'{material}.inventory.element_length'] == n * row[f'{material}.inventory.conductor_length']
        assert row[f'{material}.inventory.sc_cost'] == pytest.approx(n * row[f'{material}.inventory.conductor_length']
                                                                     * REFERENCE[material]['element_price_per_m'], rel=1e-12)
    assert low['pair.rankable'] == 0.0 and ref['pair.rankable'] == 1.0


@pytest.mark.parametrize('material', ['nb3sn', 'rebco'])
def test_fit_insufficient_and_sufficient(evaluate, material):
    """A supplied design with 1500 mm2 more steel per turn no longer fits the envelope; steel inventory follows it."""
    extra = REFERENCE[material]['steel_area'] + 1500.0
    big, ref = evaluate({f'{material}.steel_area': extra}), evaluate()
    assert big.verdict(f'{material}.fit_ok') == 'violated' and ref.verdict(f'{material}.fit_ok') == 'satisfied'
    assert big.verdict(f'{material}.steel_ok') == 'satisfied'
    assert big[f'{material}.area.fit_margin'] < 0 < ref[f'{material}.area.fit_margin']
    assert big[f'{material}.inventory.steel_mass'] / ref[f'{material}.inventory.steel_mass'] == pytest.approx(
        extra / REFERENCE[material]['steel_area'], rel=1e-12)
    assert big['pair.rankable'] == 0.0


@pytest.mark.parametrize('material', ['nb3sn', 'rebco'])
def test_protection_copper_insufficient_and_sufficient(evaluate, material):
    space = REFERENCE[material]['cu_space']
    low, ref = evaluate({f'{material}.cu_space': 0.9 * space}), evaluate()
    assert low.verdict(f'{material}.copper_ok') == 'violated' and ref.verdict(f'{material}.copper_ok') == 'satisfied'
    assert low[f'{material}.area.cu_required'] == ref[f'{material}.area.cu_required']  # requirement from duty, not from the offer
    assert low[f'{material}.inventory.cu_mass'] == pytest.approx(0.9 * ref[f'{material}.inventory.cu_mass'], rel=1e-12)


@pytest.mark.parametrize('material', ['nb3sn', 'rebco'])
def test_structural_steel_insufficient_and_sufficient(evaluate, material):
    area = REFERENCE[material]['steel_area']
    low, ref = evaluate({f'{material}.steel_area': 0.9 * area}), evaluate()
    assert low.verdict(f'{material}.steel_ok') == 'violated' and ref.verdict(f'{material}.steel_ok') == 'satisfied'
    assert low[f'{material}.area.steel_required'] == ref[f'{material}.area.steel_required']
    assert low[f'{material}.inventory.steel_mass'] == pytest.approx(0.9 * ref[f'{material}.inventory.steel_mass'], rel=1e-12)


@pytest.mark.parametrize('material', ['nb3sn', 'rebco'])
def test_refrigerator_capacity_insufficient_and_sufficient(evaluate, material):
    """The next lower listed rating (20 kW) is insufficient; capital follows the installed rating, not the demand."""
    low, ref = evaluate({f'{material}.rating_cold': 20000.0}), evaluate()
    assert low.verdict(f'{material}.capacity_ok') == 'violated' and ref.verdict(f'{material}.capacity_ok') == 'satisfied'
    assert low[f'{material}.cold_load.q_cold'] == ref[f'{material}.cold_load.q_cold']
    assert low[f'{material}.refrigeration.refrigerator_capital'] / ref[f'{material}.refrigeration.refrigerator_capital'] == pytest.approx(
        (20000.0 / REFERENCE[material]['rating_cold']) ** 0.65, rel=1e-12)
    assert low['pair.rankable'] == 0.0


def test_field_varied_with_hardware_fixed(evaluate):
    """At fixed geometry the supplied offers stay put while the field moves: margins, requirements and demand change;
    inventory, conductor cost and refrigerator capital do not."""
    rows = {B: evaluate({'duty.B_peak': B}) for B in (8.0, 10.0, 12.0)}
    for material in ('nb3sn', 'rebco'):
        for name in HARDWARE:
            assert rows[8.0][f'{material}.{name}'] == rows[12.0][f'{material}.{name}'], (material, name)
        for name in ('conductor.acceptance_margin', 'conductor.operating_fraction', 'area.cu_required', 'area.steel_required',
                     'cold_load.q_cold', 'refrigeration.capacity_margin'):
            assert rows[8.0][f'{material}.{name}'] != rows[12.0][f'{material}.{name}'], (material, name)
        assert rows[8.0][f'{material}.area.steel_margin'] > 0 > rows[12.0][f'{material}.area.steel_margin']
    assert rows[12.0]['duty.turn_current'] / rows[8.0]['duty.turn_current'] == pytest.approx(1.5, rel=1e-12)


def _changed(a, b):
    left, right = a.named(), b.named()
    return {name for name in left if not same(left[name], right[name])}


def test_element_count_changes_only_conductor_dependent_outputs(evaluate):
    """Design D5: the strand count moves the conductor, area, element inventory and cost, never the cold chain or REBCO."""
    changed = _changed(evaluate(), evaluate({'nb3sn.n_elements': 500.0}))
    allowed_prefixes = ('nb3sn.conductor.', 'nb3sn.area.', 'nb3sn.inventory.', 'nb3sn.annualized.', 'pair.')
    assert changed and all(name.startswith(allowed_prefixes) for name in changed), sorted(changed)
    assert {'nb3sn.conductor.ic_cable_op', 'nb3sn.inventory.element_length', 'nb3sn.inventory.sc_cost',
            'nb3sn.area.fit_margin'} <= changed
    assert not any(name.startswith(('nb3sn.cold_load.', 'nb3sn.refrigeration.', 'rebco.', 'duty.')) for name in changed)


def test_rating_changes_only_refrigerator_outputs(evaluate):
    """Design D5: the installed rating moves refrigerator capital, capacity margin and efficiency (and the power it
    implies), never the conductor, winding, cold load or the other material."""
    changed = _changed(evaluate(), evaluate({'rebco.rating_cold': 50000.0}))
    allowed = {'rebco.refrigeration.' + name for name in ('eta_cold', 'p_in_cold', 'p_in_total_MW', 'R_equiv_kW', 'refrigerator_capital',
                                                         'capacity_margin', 'capacity_pass', 'green_extrapolated')}
    allowed |= {'rebco.annualized.capital_total', 'rebco.annualized.annual_electricity', 'rebco.annualized.annualized_cost',
                'pair.cost_difference', 'pair.breakeven_rebco_price_per_m', 'pair.breakeven_rebco_price_per_kAm'}
    assert {'rebco.refrigeration.refrigerator_capital', 'rebco.refrigeration.capacity_margin', 'rebco.refrigeration.eta_cold'} <= changed
    assert changed <= allowed, sorted(changed - allowed)


def test_evaluation_is_repeatable_and_leaves_supplied_design_unchanged(evaluate):
    first, second = evaluate(), evaluate()
    assert first.named() == second.named()
    assert first['nb3sn.inventory.element_length'] == REFERENCE['nb3sn']['n_elements'] * first['nb3sn.inventory.conductor_length']
    assert first['rebco.refrigeration.capacity_margin'] == REFERENCE['rebco']['rating_cold'] - first['rebco.cold_load.q_cold']


# --------------------------------------------------------------------------------------- statuses and unsupported

@pytest.mark.parametrize('B,status', [(8.0, 1.0), (12.2, 1.0), (13.0, 2.0), (13.5, 2.0), (14.0, 3.0), (14.5, 3.0)])
def test_nb3sn_status_bands_and_pair_status(evaluate, B, status):
    row = evaluate({'duty.B_peak': B})
    assert row['nb3sn.conductor.status_code'] == status and row['nb3sn.conductor.supported'] == 1.0
    assert row['rebco.conductor.status_code'] == 1.0
    assert row['pair.pair_status'] == status


def test_nb3sn_unsupported_field_has_no_verdict_pass_or_ranking(evaluate):
    row = evaluate({'duty.B_peak': 15.0})
    assert row['nb3sn.conductor.status_code'] == 0.0 and row['nb3sn.conductor.supported'] == 0.0
    assert row['nb3sn.conductor.acceptance_pass'] == 0.0 and row.verdict('nb3sn.acceptance_ok') == 'violated'
    assert row['rebco.conductor.status_code'] == 1.0
    assert row['pair.rankable'] == 0.0 and row['pair.pair_status'] == 0.0


@pytest.mark.parametrize('changes', [{'nb3sn.eps_intrinsic': -0.012}, {'nb3sn.T_supply': 11.5}])
def test_nb3sn_unsupported_strain_and_temperature(evaluate, changes):
    row = evaluate(changes)
    assert row['nb3sn.conductor.status_code'] == 0.0 and row.verdict('nb3sn.acceptance_ok') == 'violated'
    assert row['pair.rankable'] == 0.0 and row['pair.pair_status'] == 0.0


def test_rebco_unsupported_temperature_has_no_verdict_pass_or_ranking(evaluate):
    row = evaluate({'rebco.T_supply': 50.0})  # conductor 50.7 K, above the exponential law's 50 K
    assert row['rebco.conductor.status_code'] == 0.0 and row['rebco.conductor.supported'] == 0.0
    assert math.isfinite(row['rebco.conductor.ic_tape_op'])
    assert row['rebco.conductor.acceptance_pass'] == 0.0 and row.verdict('rebco.acceptance_ok') == 'violated'
    assert row['nb3sn.conductor.status_code'] == 1.0
    assert row['pair.rankable'] == 0.0 and row['pair.pair_status'] == 0.0


def test_rebco_outside_measured_knots_is_unsupported_and_undefined(evaluate):
    row = evaluate({'duty.B_peak': 22.0})
    assert row['rebco.conductor.status_code'] == 0.0 and row.verdict('rebco.acceptance_ok') == 'violated'
    assert math.isnan(row['rebco.conductor.ic_tape_op']) and math.isnan(row['pair.breakeven_rebco_price_per_kAm'])
    assert row['pair.rankable'] == 0.0 and row['pair.pair_status'] == 0.0
    extension = evaluate({'duty.B_peak': 22.0, 'rebco.shape_mode': 1.0})  # power-law sensitivity is supported to 24 T
    assert extension['rebco.conductor.status_code'] == 1.0


def test_invalid_rule_selector_is_refused(evaluate):
    from simkit.evaluation.evaluator import EvaluationFailed
    with pytest.raises(EvaluationFailed):
        evaluate({'nb3sn.acceptance_rule': 0.5})
