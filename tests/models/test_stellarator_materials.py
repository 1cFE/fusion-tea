"""WI-100 plant-level conductor material packages (design section 6.1) through the generated packages.

Tests run through the package route `exploration/stellarator_materials/studies/study_route.py` (stock strict loader,
`StudyRunner`) unless marked [direct]: a direct test uses the route's own `prepare()` and the stock `PreparedEvaluator` on
typed inputs, without `validate_proposal` (design D8), because it must set a pinned reference key or a final key.

Three packages, one plant each (probe P2: codegen refuses two instances of 'MFE Power Plant'; the K21 fallback):
reference (the staged Stellaris instance), rebco and nb3sn. The Nb3Sn default design at R 12.7 m (12 T, 4.3 T on axis
with the Stellaris plasma) refuses (nonpositive IHX terminal approach; design K22), so Nb3Sn cases here supply a test
plasma density n_e0 = 4.0e20 at which the plant evaluates; the offer policy, not this module, supplies coherent designs.

Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python -m pytest tests/models/test_stellarator_materials.py'
"""
from __future__ import annotations

import importlib.util
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
if os.environ.get('STOP_PARSER_TEAX_ROOT'):
    sys.path.insert(0, str(Path(os.environ['STOP_PARSER_TEAX_ROOT']) / 'packages/teax-simkit'))
from exploration.stellarator_materials.studies import study_route as route  # noqa: E402

BUILD = ROOT / 'work/active/WI-100_stellarator-material-variants/build'
DESIGNS = json.loads((ROOT / 'exploration/stellarator_materials/reference_designs.json').read_text())['designs']
PIN = json.loads(route.PIN_PATH.read_text())
REF, RE, NB = (route.UNITS[u].prefix for u in ('reference', 'rebco', 'nb3sn'))
NB3SN_TEST = {'magnet__conductor__eps_intrinsic_in': -0.003, 'plasma__n_e0': 4.0e20}
ROUND1 = ROOT / 'exploration/magnet_materials/bodies/magnet_conductor_alternatives'
PROTECTED = ['models', 'exploration/stellarator_e2e', 'exploration/magnet_materials']  # plus the one additive registration below

pytestmark = pytest.mark.skipif(not os.environ.get('STOP_PARSER_TEAX_ROOT'), reason='needs the sealed teax runtime')


def body(name):
    spec = importlib.util.spec_from_file_location('wi100_test_' + name, ROUND1 / (name + '_impl.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.calculate


# ------------------------------------------------------------------------------------------------ evaluators

class Result:
    def __init__(self, unit, outputs, verdicts, inputs=None, state='completed', candidate=None):
        self.unit, self.outputs, self.verdicts, self.inputs, self.state, self.candidate = unit, outputs, verdicts, inputs, state, candidate
        self.prefix = route.UNITS[unit].prefix

    def __getitem__(self, suffix):
        return self.outputs[self.prefix + suffix]

    def verdict(self, local):
        return self.verdicts[local]


class Direct:
    """[direct] evaluator: the route's prepare() and the stock evaluator, no validate_proposal (D8)."""

    _cache = {}

    def __init__(self, unit):
        from exploration.stellarator_materials.studies.study_route import prepare
        self.unit = unit
        self.prepared = prepare(unit)
        document = route.interface(unit)
        self.entry = document['entry_keys']
        defaults = {}
        for path in sorted((route.UNITS[unit].package_dir / 'inputs').glob('*.json')):
            defaults.update(json.loads(path.read_text()))
        self.base = {k: defaults[k] for k in self.entry} | document['baseline_point']
        self.booleans = route.boolean_keys(unit)
        self.catalog = route._catalog_by_constraint_id(route.UNITS[unit].package_dir)

    @classmethod
    def of(cls, unit):
        if unit not in cls._cache:
            cls._cache[unit] = cls(unit)
        return cls._cache[unit]

    def evaluate(self, overrides=None):
        from simkit.study.bridge import CandidateBridge
        P = route.UNITS[self.unit].prefix
        point = dict(self.base) | {P + k: v for k, v in (overrides or {}).items()}
        typed = {k: (bool(v) if k in self.booleans else float(v)) for k, v in point.items()}
        evidence = self.prepared.evaluate(CandidateBridge(self.prepared.entry_models).build(typed))
        verdicts = {self.catalog[cid]['source_local_identity']: s for cid, s in evidence.responses.items() if cid != 'headline'}
        return Result(self.unit, dict(evidence.outputs), verdicts)


_ROUTE_CACHE = {}


def run_route(unit, labelled):
    """Run labelled proposals (suffix -> value) through the route; returns {label: Result} (cached per proposal)."""
    P = route.UNITS[unit].prefix
    todo = {label: {P + k: v for k, v in over.items()} for label, over in labelled.items()
            if (unit, json.dumps(over, sort_keys=True)) not in _ROUTE_CACHE}
    if todo:
        work = Path(tempfile.mkdtemp(prefix='wi100-route-'))
        study = f'wi100-test-{unit}-{abs(hash(json.dumps(sorted(todo.items()), sort_keys=True, default=str))) % 10**10}'
        cases, db = route.run_points(unit, study, list(todo.values()), work)
        failures = route.failure_texts(db)
        assert len(cases) == len(todo)
        for (label, proposal), case in zip(todo.items(), cases):
            for key, value in proposal.items():
                assert float(case.inputs[key]) == float(value), (label, key)
            verdicts = route.short_verdicts(unit, case) if case.state == 'completed' else {}
            result = Result(unit, dict(case.outputs), verdicts, dict(case.inputs), case.state, case.candidate_id)
            result.failure = failures.get(case.candidate_id)
            _ROUTE_CACHE[(unit, json.dumps(labelled[label], sort_keys=True))] = result
    return {label: _ROUTE_CACHE[(unit, json.dumps(over, sort_keys=True))] for label, over in labelled.items()}


def one(unit, overrides):
    return run_route(unit, {'x': overrides})['x']


def rebco(**overrides):
    return one('rebco', overrides)


def nb3sn(**overrides):
    return one('nb3sn', NB3SN_TEST | overrides)


def pipeline(unit):
    return yaml.safe_load((route.UNITS[unit].package_dir / 'pipelines/pipeline.yaml').read_text())['modules']


def source(value):
    """The producer key of a pipeline input spelled '<type> <source>'."""
    return value.split(' ', 1)[1].removesuffix('.root')


# ------------------------------------------------------------------------------------------------ 1 reference

def test_1_reference_reproduces_the_pin_bit_for_bit():
    point = route.interface('reference')['baseline_point']
    case = one('reference', {k.removeprefix(REF): v for k, v in point.items()})
    parity = route.reference_parity(case.outputs, {cid: s for cid, s in _raw_verdicts('reference', case).items()})
    assert parity['missing'] == [] and parity['unequal'] == {} and parity['verdict_unequal'] == {}
    assert parity['added'] == [REF + 'magnet__conductor_current__evaluation_defined'] and parity['declared_delta_ok']
    assert case['lcoe_calc__lcoe'] == PIN['outputs'][REF + 'lcoe_calc__lcoe']
    delta = route.interface('reference')['partition']['reference_declared_delta']
    assert {k: point[k] for k in delta} == {REF + 'magnet__coil__arm_slope': 0.0, REF + 'magnet__coil__arm_x_ref': 0.0,
                                           REF + 'magnet__rebco_law_enabled': 1.0}
    recorded = json.loads((BUILD / 'regression/baseline-parity.json').read_text())
    assert recorded['bit_for_bit'] is True


def _raw_verdicts(unit, result):
    by_local = {v: k for k, v in route.interface(unit)['constraints'].items()}
    return {by_local[local]: status for local, status in result.verdicts.items()}


def test_1_protected_paths_are_unchanged():
    status = subprocess.run(['git', 'status', '--porcelain', '--'] + PROTECTED, cwd=ROOT, capture_output=True, text=True, check=True)
    assert status.stdout == ''
    diff = subprocess.run(['git', 'diff', '--stat', '--'] + PROTECTED, cwd=ROOT, capture_output=True, text=True, check=True)
    assert diff.stdout == ''
    registry = subprocess.run(['git', 'diff', '-U0', '--', 'tests/model_families.py'], cwd=ROOT, capture_output=True, text=True,
                              check=True).stdout.splitlines()
    removed = [line for line in registry if line.startswith('-') and not line.startswith('---')]
    added = [line for line in registry if line.startswith('+') and not line.startswith('+++')]
    assert removed == [] and all('stellarator_materials' in line or line[1:].startswith('#') or line == '+' for line in added)
    preservation = json.loads((BUILD / 'regression/preservation.json').read_text())
    assert preservation['changed'] == [] and preservation['files'] > 0


# ------------------------------------------------------------------------------------------------ 2 gating

LAW_OUTPUTS = ('parallel_tapes_set', 'parallel_tapes_reference', 'tape_critical_current', 'critical_current_reference',
               'critical_current_set', 'operating_fraction_reference', 'operating_fraction_set', 'allowable_current',
               'margin_fraction', 'margin_current', 'field_extrapolated')


def test_2_gate_zero_returns_zeros_and_satisfies_the_old_check_direct():
    direct = Direct.of('reference')
    on = direct.evaluate()
    assert on['magnet__conductor_current__evaluation_defined'] == 1.0
    off = direct.evaluate({'magnet__rebco_law_enabled': 0.0})
    assert all(off['magnet__conductor_current__' + name] == 0.0 for name in LAW_OUTPUTS)
    assert off['magnet__conductor_current__evaluation_defined'] == 0.0
    assert on.verdict('reference_conductor_current_ok') == 'violated'
    assert off.verdict('reference_conductor_current_ok') == 'satisfied'  # 0 >= 0: why E6 re-points it in the materials


def test_2_gate_refuses_values_other_than_zero_and_one_direct():
    from simkit.evaluation.failure import EvaluationFailed
    with pytest.raises(EvaluationFailed, match='enabled must be 0 or 1'):
        Direct.of('reference').evaluate({'magnet__rebco_law_enabled': 0.5})


def test_2_route_refuses_pinned_and_final_keys():
    with pytest.raises(route.RouteError, match='pinned'):
        route.proposal_validator('reference')({REF + 'magnet__rebco_law_enabled': 0.0})
    for unit, prefix in (('rebco', RE), ('nb3sn', NB)):
        for suffix in route.FINAL_SUFFIXES:
            with pytest.raises(route.RouteError, match='final'):
                route.proposal_validator(unit)({prefix + suffix: 0.0} | ({NB + 'magnet__conductor__eps_intrinsic_in': -0.003} if unit == 'nb3sn' else {}))
    with pytest.raises(route.RouteError, match='K6'):
        route.proposal_validator('nb3sn')({NB + 'plasma__n_e0': 4.0e20})
    with pytest.raises(route.RouteError, match='one material per case'):
        route.proposal_validator('rebco')({NB + 'magnet__n_elements': 400.0})


# ------------------------------------------------------------------------------------------------ 3 arm slot

def test_3_arm_at_zero_slope_is_bitwise_the_constant_ratio_direct():
    direct = Direct.of('reference')
    rng = random.Random(100)
    for _ in range(3):
        R, wp_side = rng.uniform(11.5, 13.5), rng.uniform(0.32, 0.42)
        for x_ref in (0.0, 35.278, 1e3):
            row = direct.evaluate({'plasma__R': R, 'magnet__winding_pack__wp_side': wp_side, 'magnet__coil__arm_x_ref': x_ref})
            a_coil, a_ref = row['rb__r_coil_centre'], direct.base[REF + 'magnet__coil__a_coil_ref']
            R_ref = direct.base[REF + 'magnet__coil__R_ref']
            bore_norm = (R / (R - a_coil)) / (R_ref / (R_ref - a_ref))
            expected = (row['magnet__field_calc__B_axis'] * direct.base[REF + 'magnet__coil__peak_ratio']) * bore_norm
            assert row['magnet__peak_field_calc__B_peak'] == expected


def test_3_arm_on_the_rebco_instance_and_its_sign():
    cases = run_route('rebco', {'arm': {'magnet__coil__arm_slope': 0.0641},
                                'big_pack': {'magnet__coil__arm_slope': 0.0641, 'magnet__winding_pack__wp_side': 12.7 / 30.0}})
    x = 12.7 / 0.35999999999999993
    expected = 24.899999999999995 * (1 + 0.0641 * (x - 35.278) / 2.7666666666666666)
    assert cases['arm']['magnet__peak_field_calc__B_peak'] == pytest.approx(expected, rel=1e-12)
    assert cases['arm']['magnet__peak_field_calc__B_peak'] == pytest.approx(24.89987, abs=1e-5)
    assert cases['big_pack']['magnet__peak_field_calc__B_peak'] < cases['arm']['magnet__peak_field_calc__B_peak']
    assert cases['arm']['magnet__pack_field__R_over_sqrt_A_wp'] == pytest.approx(x, rel=1e-15)


# ------------------------------------------------------------------------------------------------ 4 staged cryo

def test_4a_seam_wiring_and_values():
    for unit, prefix in (('rebco', RE), ('nb3sn', NB)):
        spec = pipeline(unit)
        assert source(spec[prefix + 'pb']['inputs']['p_cryo']) == prefix + 'cryoplant__refrigeration__p_in_total_MW'
        assert source(spec[prefix + 'power_supplies__tf_power']['inputs']['p_b']) == prefix + 'cryoplant__staged_drive__p_drive'
        assert source(spec[prefix + 'magnet__magnet_capital_rollup']['inputs']['winding_cost']) == prefix + 'magnet__winding_sum__cost'
        assert source(spec[prefix + 'cryoplant__cold_stage_capability']['inputs']['demand_in']) == prefix + 'cryoplant__cold_stage__q_cold'
        assert source(spec[prefix + 'cryoplant__intercept_stage_capability']['inputs']['demand_in']) == prefix + 'cryoplant__cold_stage__q_shield'
        assert source(spec[prefix + 'cryoplant__aux_cooling']['inputs']['purchase_cost_in']) == prefix + 'cryoplant__refrigeration__refrigerator_capital'
    spec = pipeline('reference')
    assert source(spec[REF + 'magnet__magnet_capital_rollup']['inputs']['winding_cost']) == REF + 'magnet__winding_procurement__cost'
    assert source(spec[REF + 'pb']['inputs']['p_cryo']) == REF + 'cryoplant__refrigeration_sum__total'
    row = rebco()
    assert row['power_supplies__tf_power__total'] == 0.0 + row['cryoplant__staged_drive__p_drive']
    assert row['cryoplant__aux_cooling__cryo_cost'] == row['cryoplant__refrigeration__refrigerator_capital']
    assert row['magnet__magnet_capital_rollup__capital_cost'] == pytest.approx(
        row['magnet__winding_sum__cost'] + row['magnet__magnet_structure_cost__cost'] + row['magnet__insulation_inventory__stock_cost'], rel=1e-15)


BRIDGE_MAP = {'cryoplant__refrigeration__p_in_cold': ('cryoplant__cryo_elec__p_elec', 1e6),  # W against MW
              'cryoplant__refrigeration__p_in_shield': ('cryoplant__shield_elec__p_elec', 1e6),
              'cryoplant__refrigeration__p_in_total_MW': ('cryoplant__refrigeration_sum__total', 1.0),
              'cryoplant__cold_stage__q_cold': ('cryoplant__cold_load_W_demand_conversion__demand', 1.0),
              'cryoplant__cold_stage__q_shield': ('cryoplant__inventory__q_inventory_shield', 1.0),
              'cryoplant__staged_drive__p_drive': ('cryoplant__inventory__p_drive', 1.0)}
ETA_REFERENCE = {'cryoplant__eta_mode': 1.0, 'cryoplant__eta_const': 0.20}


def test_4b_identity_under_the_reference_selection():
    row = rebco(**ETA_REFERENCE)
    for mine, (pinned, scale) in BRIDGE_MAP.items():
        assert row[mine] == pytest.approx(scale * PIN['outputs'][REF + pinned], rel=1e-9), mine
    # coordinator amendment A1: the staged conduction is the plant's k_c support conductance, 590.28 W at the pin
    assert row['cryoplant__cold_stage__q_conduction'] == pytest.approx(590.28, abs=0.01)
    assert row['cryoplant__static_loads__q_radiation'] == pytest.approx(266.68, abs=0.01)
    assert row['cryoplant__cold_stage__q_nuclear'] == pytest.approx(35.5 * 136.56, rel=1e-12)  # A2 term is zero at the pin


def test_4c_green_efficiency_moves_only_the_cold_electricity_and_its_dependents():
    fixed, green = rebco(**ETA_REFERENCE), rebco()
    for name in ('cryoplant__refrigeration__p_in_shield', 'cryoplant__cold_stage__q_cold', 'cryoplant__cold_stage__q_shield',
                 'cryoplant__staged_drive__p_drive', 'cryoplant__refrigeration__refrigerator_capital'):
        assert fixed[name] == green[name], name
    assert fixed['cryoplant__refrigeration__p_in_cold'] != green['cryoplant__refrigeration__p_in_cold']
    assert fixed['pb__p_net'] != green['pb__p_net']


def _graph(unit):
    spec = pipeline(unit)
    produced, consumers, reads = {}, {}, {}
    for name, module in spec.items():
        for value in (module.get('outputs') or {}).values():
            produced[value.split(' ', 1)[1]] = name
        for value in (module.get('inputs') or {}).values():
            src = source(value)
            key = src.split('.', 1)[1] if '.' in src and src.split('.', 1)[0].endswith('_params') else src
            reads.setdefault(name, set()).add(key)
            consumers.setdefault(key, set()).add(name)
    return spec, produced, consumers, reads


def test_4d_bridge_parity_outside_the_pipeline_descendants_of_the_edited_producers():
    """Review R6: the changed set is the generated-pipeline descendants of the edited producers (the variant calcs and
    seams, the gated law, the disabled inventory, the calculated cryo capital, and every supplied value that differs)."""
    reference, material = one('reference', {}), rebco(**ETA_REFERENCE)
    spec, produced, consumers, reads = _graph('rebco')
    ref_spec = pipeline('reference')
    ref_point = route.interface('reference')['baseline_point']
    mat_point = route.interface('rebco')['baseline_point'] | {RE + k: v for k, v in ETA_REFERENCE.items()}
    seeds = set()
    for name, module in spec.items():
        twin = REF + name.removeprefix(RE)
        if twin not in ref_spec:
            seeds.add(name)
            continue
        mine = {k: source(v).split('.')[-1].removeprefix(RE) for k, v in (module.get('inputs') or {}).items()}
        theirs = {k: source(v).split('.')[-1].removeprefix(REF) for k, v in (ref_spec[twin].get('inputs') or {}).items()}
        if mine != theirs:
            seeds.add(name)
    changed_keys = {k for k, v in mat_point.items() if ref_point.get(REF + k.removeprefix(RE)) != v}
    changed_keys |= {k for k in route.interface('rebco')['entry_keys'] if k not in mat_point}
    for key in changed_keys:
        seeds |= consumers.get(key, set())
    changed, frontier = set(seeds), list(seeds)
    while frontier:
        module = frontier.pop()
        for value in (spec[module].get('outputs') or {}).values():
            for consumer in consumers.get(value.split(' ', 1)[1], ()):
                if consumer not in changed:
                    changed.add(consumer)
                    frontier.append(consumer)
    compared = moved = 0
    for channel, value in material.outputs.items():
        twin = REF + channel.removeprefix(RE)
        if twin not in reference.outputs or produced.get(channel) in changed:
            continue
        compared += 1
        if value != reference.outputs[twin] and not (value != value and reference.outputs[twin] != reference.outputs[twin]):
            moved += 1
            assert value == reference.outputs[twin], (channel, value, reference.outputs[twin])
    print(f'4d: {compared} channels compared bit for bit, {len(changed)} changed-set modules of {len(spec)}')
    assert compared > 700 and moved == 0


# ------------------------------------------------------------------------------------------------ 5 MR-7 pairs

def _smallest_rebco_count(row):
    law = body('rebco_cable_critical_surface')
    x = {k.removeprefix(RE + 'magnet__'): v for k, v in route.interface('rebco')['baseline_point'].items()
         if k.startswith(RE + 'magnet__') and k.count('__') == 3}
    B = row['magnet__peak_field_calc__B_peak']
    inputs = dict(n_tapes=1.0, tape_width=x['tape_width'], tape_thickness=x['tape_thickness'],
                  tape_copper_fraction=x['tape_copper_fraction'], turn_current=50000.0, B_peak=B, T_supply=20.0,
                  nuclear_rise=x['nuclear_rise'], margin_rise=x['margin_rise'], anchor_ic=x['anchor_ic'],
                  shape_mode=1.0 if B > x['B_knot_max'] else 0.0, **{k: x[k] for k in ('g8', 'g10', 'g12', 'g15', 'g20', 'alpha',
                  'T_star', 'degradation', 'fraction_rule', 'acceptance_rule', 'B_knot_min', 'B_knot_max', 'B_law_min', 'B_law_max',
                  'T_law_min', 'T_law_max')})
    n = int(50000.0 / (0.8 * law(inputs)['ic_cable_op']))
    while law(inputs | {'n_tapes': float(n)})['acceptance_margin'] < 0:
        n += 1
    while law(inputs | {'n_tapes': float(n - 1)})['acceptance_margin'] >= 0:
        n -= 1
    return n


def _follows_supplied(low, high, same_hardware=True):
    for name in ('magnet__inventory__element_length', 'magnet__inventory__sc_cost', 'magnet__inventory__materials_cost',
                 'magnet__wp_volume__vol_cold_total'):
        if same_hardware:
            assert low[name] == high[name], name


def test_5_acceptance_pairs_follow_the_supplied_count():
    n_re = _smallest_rebco_count(rebco())
    pair = run_route('rebco', {'low': {'magnet__n_elements': float(math.floor(0.9 * n_re))}, 'high': {'magnet__n_elements': float(n_re)}})
    assert pair['low'].verdict('acceptance_ok') == 'violated' and pair['high'].verdict('acceptance_ok') == 'satisfied'
    assert pair['high']['magnet__inventory__element_length'] / pair['low']['magnet__inventory__element_length'] == pytest.approx(
        n_re / math.floor(0.9 * n_re), rel=1e-12)
    n_nb = DESIGNS['nb3sn_material']['magnet']['values']['n_elements']
    pair = run_route('nb3sn', {'low': NB3SN_TEST | {'magnet__n_elements': float(math.floor(0.9 * n_nb))}, 'high': NB3SN_TEST})
    assert pair['low'].verdict('acceptance_ok') == 'violated' and pair['high'].verdict('acceptance_ok') == 'satisfied'
    assert pair['high']['magnet__inventory__sc_cost'] / pair['low']['magnet__inventory__sc_cost'] == pytest.approx(
        n_nb / math.floor(0.9 * n_nb), rel=1e-12)
    assert pair['low']['magnet__peak_field_calc__B_peak'] == pair['high']['magnet__peak_field_calc__B_peak']  # field unchanged


def test_5_pack_area_pair():
    base = nb3sn()
    turns, gross = base.inputs.get(NB + 'magnet__coil__reference_turns', DESIGNS['nb3sn_material']['existing']['values'][
        'magnet.coil.reference_turns']), base['magnet__area__gross_area']
    tight = 0.999 * math.sqrt(turns * gross * 1e-6)
    pair = run_route('nb3sn', {'low': NB3SN_TEST | {'magnet__winding_pack__wp_side': tight}, 'high': NB3SN_TEST})
    assert pair['low'].verdict('pack_area_ok') == 'violated' and pair['high'].verdict('pack_area_ok') == 'satisfied'
    assert pair['low']['magnet__area__gross_area'] == pair['high']['magnet__area__gross_area']  # supplied areas unchanged


def test_5_fit_pairs():
    values = DESIGNS['nb3sn_material']['existing']['values']
    pair = run_route('nb3sn', {'coil_low': NB3SN_TEST | {'magnet__coil__coil_t': values['magnet.coil.coil_t'] - 0.02},
                               'y_low': NB3SN_TEST | {'magnet__casing__interior_y': 0.55}, 'high': NB3SN_TEST})
    assert pair['coil_low'].verdict('wp_fit_ok') == 'violated' and pair['y_low'].verdict('wp_fit_ok') == 'violated'
    assert pair['high'].verdict('wp_fit_ok') == 'satisfied'
    assert pair['y_low']['magnet__inventory__element_length'] == pair['high']['magnet__inventory__element_length']


def test_5_capacity_pairs():
    base = nb3sn()
    drive = base['power_supplies__tf_power__total']
    cases = run_route('nb3sn', {
        'cold_low': NB3SN_TEST | {'cryoplant__rated_cold_W': 20000.0},
        'intercept_low': NB3SN_TEST | {'cryoplant__rated_intercept_W': 30000.0},
        'tf_low': NB3SN_TEST | {'power_supplies__rated_tf_MWe': 0.95 * drive},
        'tf_high': NB3SN_TEST | {'power_supplies__rated_tf_MWe': 1.05 * drive}})
    assert base.verdict('capacity_ok') == 'satisfied' and base.verdict('cold_stage_capacity_ok') == 'satisfied'
    assert cases['cold_low'].verdict('capacity_ok') == 'violated' and cases['cold_low'].verdict('cold_stage_capacity_ok') == 'violated'
    assert base.verdict('intercept_stage_capacity_ok') == 'satisfied'
    assert cases['intercept_low'].verdict('intercept_stage_capacity_ok') == 'violated'
    assert cases['tf_low'].verdict('magnet_tf_electric_capacity_ok') == 'violated'
    assert cases['tf_high'].verdict('magnet_tf_electric_capacity_ok') == 'satisfied'
    for row in cases.values():  # the rating is supplied: loads and hardware are unchanged by it
        assert row['cryoplant__cold_stage__q_cold'] == base['cryoplant__cold_stage__q_cold']
        assert row['magnet__inventory__sc_cost'] == base['magnet__inventory__sc_cost']


def test_5_copper_and_steel_pairs():
    base = rebco()
    cu, steel = base['magnet__area__cu_required'], base['magnet__area__steel_required']
    cases = run_route('rebco', {'cu_low': {'magnet__cu_space': 0.99 * cu}, 'cu_at': {'magnet__cu_space': cu},
                                'steel_low': {'magnet__steel_area': 0.99 * steel}, 'steel_at': {'magnet__steel_area': steel}})
    assert cases['cu_low'].verdict('copper_ok') == 'violated' and cases['cu_at'].verdict('copper_ok') == 'satisfied'
    assert cases['steel_low'].verdict('steel_ok') == 'violated' and cases['steel_at'].verdict('steel_ok') == 'satisfied'
    assert cases['cu_low']['magnet__area__cu_required'] == cu  # the requirement does not follow the supplied area


def test_5_ampere_floor_pair_across_the_binding_pack_side():
    design = {'plasma__R': 22.0, 'plasma__a': 2.2, 'magnet__coil__peak_ratio': 2.12, 'plasma__n_e0': 2.2e20}
    cases = run_route('rebco', {'small': design | {'magnet__winding_pack__wp_side': 0.46},
                                'large': design | {'magnet__winding_pack__wp_side': 0.50}})
    small, large = cases['small'], cases['large']
    assert small['magnet__peak_field_calc__B_peak'] == large['magnet__peak_field_calc__B_peak']  # arm off: pack does not move it
    binding = 4e-7 * math.pi * small['magnet__winding_state__I_coil'] / (4 * small['magnet__peak_field_calc__B_peak'])
    assert 0.46 < binding < 0.50 and binding == pytest.approx(0.48, abs=0.01)
    assert small.verdict('ampere_floor_ok') == 'violated' and large.verdict('ampere_floor_ok') == 'satisfied'
    assert small['magnet__pack_field__ampere_floor'] == pytest.approx(
        1.25663706212e-6 * small['magnet__winding_state__I_coil'] / (4 * 0.46), rel=1e-14)


# ------------------------------------------------------------------------------------------------ 6 hardware fixed

def test_6_turn_current_moves_demand_not_hardware():
    cases = run_route('rebco', {'base': {}, 'up': {'magnet__coil__turn_current': 55000.0}, 'down': {'magnet__coil__turn_current': 45000.0}})
    base = cases['base']
    for label in ('up', 'down'):
        row = cases[label]
        for name in ('magnet__peak_field_calc__B_peak', 'magnet__conductor__acceptance_margin', 'cryoplant__cold_stage__q_leads',
                     'cryoplant__cold_stage__q_joints'):
            assert row[name] != base[name], (label, name)
        for name in ('magnet__inventory__element_length', 'magnet__inventory__sc_cost', 'magnet__inventory__materials_cost',
                     'magnet__wp_volume__vol_cold_total'):
            assert row[name] == base[name], (label, name)
        # the ratings are supplied and not re-sized: each screen margin is the same rating less the moved demand
        point = route.interface('rebco')['baseline_point']
        assert row['cryoplant__cold_stage_capability__margin'] + row['cryoplant__cold_stage__q_cold'] == pytest.approx(
            point[RE + 'cryoplant__rated_cold_W'], rel=1e-12)
        assert row['cryoplant__intercept_stage_capability__margin'] + row['cryoplant__cold_stage__q_shield'] == pytest.approx(
            point[RE + 'cryoplant__rated_intercept_W'], rel=1e-12)
        assert RE + 'magnet__n_elements' not in row.inputs  # the supplied count stays at the design value


# ------------------------------------------------------------------------------------------------ 7 unsupported

def test_7_unsupported_is_a_status_never_an_exception():
    nb = nb3sn(magnet__coil__reference_turns=183.0)
    assert 14.5 < nb['magnet__peak_field_calc__B_peak'] < 15.5
    assert nb['magnet__conductor__status_code'] == 0.0 and nb['magnet__conductor__supported'] == 0.0
    assert nb.verdict('acceptance_ok') == 'violated' and route.material_flags('nb3sn', nb.outputs, nb.verdicts)['unsupported']
    re_ = rebco(magnet__coil__reference_turns=322.0)
    assert re_['magnet__peak_field_calc__B_peak'] > 26.0
    assert re_['magnet__conductor__status_code'] == 0.0 and re_.verdict('acceptance_ok') == 'violated'
    assert all(math.isfinite(re_['magnet__conductor__' + n]) for n in ('ic_cable_op', 'operating_fraction', 'acceptance_margin', 'T_cs'))


def test_7_domain_refusal_is_a_failed_evaluation_with_its_text():
    refused = rebco(magnet__coil__coil_t=20.0)
    assert refused.state == 'execution_failed'
    assert 'live clearance R_in - a_coil_in must be > 0' in json.dumps(refused.failure)


# ------------------------------------------------------------------------------------------------ 8 anchors

TABLE7_AREA = 0.36 ** 2 * 1e6 / 308


def test_8_stellaris_table_7_on_the_rebco_instance():
    tapes_ref = PIN['outputs'][REF + 'magnet__conductor_current__parallel_tapes_reference']
    row = rebco(magnet__n_elements=1.5 * tapes_ref)
    assert row['magnet__area__gross_area'] == pytest.approx(420.779220779, rel=1e-6)
    assert row['magnet__adapter__pack_area_per_turn'] == pytest.approx(TABLE7_AREA, rel=1e-12)


def test_8_eu_demo_layer_1_on_the_nb3sn_instance_all_outputs_finite():
    demo = {'magnet__coil__reference_turns': 70.0, 'magnet__coil__turn_current': 104950.0, 'magnet__n_elements': 399.0,
            'magnet__strand_diameter': 0.001, 'magnet__steel_per_kA_rule': 982.7 / 104.95, 'magnet__steel_B_scaling': 0.0,
            'magnet__misc_area': 1.1077 * 104.95}
    rule = nb3sn(**demo)
    # 70 x 104,950 A = 7.3465 MA against the 147-turn design's 7.35 MA at the Nb3Sn geometry: 12.07 T (design text: about 11.9 T)
    assert rule['magnet__peak_field_calc__B_peak'] == pytest.approx(
        DESIGNS['nb3sn_material']['diagnostics']['B_peak'] * (70 * 104950.0) / (147 * 50000.0), rel=1e-12)
    supplied = nb3sn(**demo, magnet__cu_space=rule['magnet__area__cu_required'], magnet__steel_area=rule['magnet__area__steel_required'])
    assert supplied['magnet__area__net_area'] == pytest.approx(68 * 37.9, rel=1e-6)  # 2577.2 mm2 (WI-099 anchor)
    assert supplied['magnet__area__cu_margin'] == 0.0 and supplied['magnet__area__steel_margin'] == 0.0
    nonfinite = sorted(k for k, v in supplied.outputs.items() if isinstance(v, float) and not math.isfinite(v))
    assert nonfinite == []


# ------------------------------------------------------------------------------------------------ 9 pack share

def test_9_pack_area_margin_is_the_pack_share_identity():
    for row, prefix in ((rebco(), RE), (nb3sn(), NB)):
        turns = row.inputs.get(prefix + 'magnet__coil__reference_turns') or route.interface(row.unit)['baseline_point'][
            prefix + 'magnet__coil__reference_turns']
        wp = row.inputs.get(prefix + 'magnet__winding_pack__wp_side') or route.interface(row.unit)['baseline_point'][
            prefix + 'magnet__winding_pack__wp_side']
        expected = (wp * wp * 1e6 - turns * row['magnet__area__gross_area']) / turns
        assert row['magnet__area__fit_margin'] == pytest.approx(expected, rel=1e-12, abs=1e-9)


# ------------------------------------------------------------------------------------------------ 10 build

def test_10_build_receipts():
    receipt = json.loads((BUILD / 'build-hashes.json').read_text())
    for unit, record in receipt['units'].items():
        assert record['fixed_point'] is True and record['positional_bindings']
        emitted, installed = set(record['body_set']['emitted_stubs']), set(record['body_set']['installed'])
        assert emitted <= installed
        assert installed - emitted == set(record['body_set']['preserved_reasons']) | {'mfe_account_costs/financial_factors.py'}
        assert ('magnet_material_variants/rebco_shape_branch_impl.py' in emitted) == (unit == 'rebco')
        assert {r['modified'] for r in record['bodies'] if r.get('modified')} == {'B1', 'B2'}
        unbound = {(b['usage'], name) for b in record['positional_bindings'] for name in b['unbound']}
        assert unbound == ({('conductor', 'eps_intrinsic_in'), ('pack_field', 'mu0_in')} if unit != 'reference' else set())
    for name, removed in (('B1', {'-def run_rebco_conductor_current(inputs: REBCO_Conductor_CurrentInput) -> tuple[float, float, float, '
                                   'float, float, float, float, float, float, float, float]:'}),
                          ('B2', {'-    return (inputs.B_axis_in * inputs.peak_ratio_in) * bore_norm'})):
        diff = (BUILD / 'bodies' / f'{name}.diff').read_text().split('\n')
        assert {line for line in diff if line.startswith('-') and not line.startswith('---')} == removed


# ------------------------------------------------------------------------------------------------ 11 cheap checks

def test_11_rebco_band_edges():
    at = lambda B: 50000.0 * B / 24.899999999999995
    cases = run_route('rebco', {'b20': {'magnet__coil__turn_current': at(20.0) * (1 - 1e-12)},
                                'b2001': {'magnet__coil__turn_current': at(20.01)},
                                'b25': {'magnet__coil__turn_current': at(25.0) * (1 - 1e-12)},
                                'b2501': {'magnet__coil__turn_current': at(25.01)}})
    assert cases['b20']['magnet__shape_branch__shape_mode'] == 0.0 and cases['b2001']['magnet__shape_branch__shape_mode'] == 1.0
    lo, hi = cases['b20']['magnet__conductor__ic_cable_op'], cases['b2001']['magnet__conductor__ic_cable_op']
    assert abs(hi - lo) / lo < 1e-3
    assert cases['b25']['magnet__conductor__status_code'] == 1.0 and cases['b2501']['magnet__conductor__status_code'] == 0.0


def test_11_nb3sn_strain_separation():
    spec, produced, consumers, reads = _graph('nb3sn')
    cases = run_route('nb3sn', {'base': NB3SN_TEST, 'allow': NB3SN_TEST | {'magnet__winding_pack__eps_cond_allow': 3.0e-4},  # eps_cond is 3.41e-4
                                'intrinsic': NB3SN_TEST | {'magnet__conductor__eps_intrinsic_in': -0.006}})
    base = cases['base']
    moved = {k for k, v in cases['allow'].outputs.items() if v != base.outputs[k]}
    assert moved == set()
    assert {k for k, v in cases['allow'].verdicts.items() if v != base.verdicts[k]} == {'cond_strain_ok'}
    assert base.verdict('cond_strain_ok') == 'satisfied' and cases['allow'].verdict('cond_strain_ok') == 'violated'
    downstream, frontier = {NB + 'magnet__conductor'}, [NB + 'magnet__conductor']
    while frontier:
        module = frontier.pop()
        for value in (spec[module].get('outputs') or {}).values():
            for consumer in consumers.get(value.split(' ', 1)[1], ()):
                if consumer not in downstream:
                    downstream.add(consumer)
                    frontier.append(consumer)
    moved = {k for k, v in cases['intrinsic'].outputs.items() if v != base.outputs[k] and not (v != v and base.outputs[k] != base.outputs[k])}
    assert moved and all(produced.get(k) in downstream for k in moved)
    assert NB + 'magnet__conductor__T_cs' in moved


def test_11_nb3sn_envelope_is_a_flag_not_a_failure():
    row = nb3sn(magnet__coil__reference_turns=159.0, magnet__coil__turn_current=50000.0 * 13.08 / 13.059341323570045)
    assert row['magnet__peak_field_calc__B_peak'] == pytest.approx(13.08, abs=1e-6)
    assert row.verdict('peak_field_ok') == 'violated'
    flags = route.material_flags('nb3sn', row.outputs, row.verdicts)
    assert flags['envelope_flag'] is True and flags['unsupported'] is False
    assert flags['extrapolated'] is True  # status 2 (edge band up to 13.5 T), amendment A4


# ------------------------------------------------------------------------------------------------ 12 witness

def test_12_split_packages_isolate_the_materials_and_the_baseline_record_replays():
    """D4 under the P2 fallback: a case evaluates one package, so a REBCO case cannot touch Nb3Sn; the REBCO baseline
    record written by the build replays bit for bit."""
    with pytest.raises(route.RouteError):
        route.proposal_validator('rebco')({NB + 'magnet__conductor__eps_intrinsic_in': -0.003})
    record = json.loads((ROOT / 'exploration/stellarator_materials/studies/rebco/baseline/baseline_result.json').read_text())
    replay = one('rebco', {k.removeprefix(RE): v for k, v in record['point'].items()})
    assert replay.outputs == record['channels']
    assert 'baseline_refusal' in route.interface('nb3sn')  # design K22: the Nb3Sn default awaits the offer policy


# ------------------------------------------------------------------------------------------------ 13 closure

ROLLUP_OPERANDS = {  # every operand each rollup reads in the generated pipeline; an unlisted account fails the test
    'magnet__magnet_capital_rollup': {'WINDING', 'magnet__magnet_structure_cost__cost', 'magnet__insulation_inventory__stock_cost'},
    'powercore_capital': {'magnet__magnet_capital_rollup__capital_cost', 'heating__heating_cost__cost', 'divertor__divertor_cost__cost',
                          'blanket__blanket_cost__cost', 'shield__shield_cost__cost', 'structure__structure_cost__cost',
                          'vessel__vessel_cost__cost', 'power_supplies__power_supplies_cost__cost'},
    'bop_capital': {'turbine__turbine_cost__cost', 'electric_plant__electric_cost__cost', 'heat_rejection__heat_rejection_cost__cost',
                    'misc_plant__misc_cost__cost'},
    'cas22_capital': {'powercore_capital__powercore_capital', 'remote_handling__cost', 'installation__cost',
                      'heat_transport__cooling_selection__cost', 'cryoplant__aux_cooling__cost', 'waste__cost',
                      'fuel_cycle__processing_cost__cost', 'other_rpe__cost', 'inc_cost__cost'},
    'cas2x_pre_contingency': {'buildings__facility_accounts__cost', 'cas22_capital__cas22_capital', 'bop_capital__bop_capital',
                              'special_materials_capital__special_materials_capital', 'cas28_capital'},
    'cas20_capital': {'cas2x_pre_contingency__cas2x_pre_contingency', 'contingency__cost'},
    'total_capital': {'facility_preconstruction__cost', 'cas20_capital__cas20_capital', 'indirect__cost', 'owner__cost',
                      'supplementary__cost'},
    'cas70_calc': {'cas71_calc__levelized', 'cooling_annual__cas72_total', 'cas80_calc__levelized'},
}


def _rollup_wiring(unit, winding):
    spec, P = pipeline(unit), route.UNITS[unit].prefix
    for module, expected in ROLLUP_OPERANDS.items():
        read = {source(v).split('.')[-1].removeprefix(P) for v in spec[P + module]['inputs'].values()}
        assert read == {winding if k == 'WINDING' else k for k in expected}, (unit, module)


def _closure(row, winding):
    _rollup_wiring(row.unit, winding)
    o = lambda name: row[name]
    magnet = o('magnet__magnet_capital_rollup__capital_cost')
    assert magnet == pytest.approx(o(winding) + o('magnet__magnet_structure_cost__cost') + o('magnet__insulation_inventory__stock_cost'), rel=1e-9)
    powercore = magnet + sum(o(n) for n in ('heating__heating_cost__cost', 'divertor__divertor_cost__cost', 'blanket__blanket_cost__cost',
                                            'shield__shield_cost__cost', 'structure__structure_cost__cost', 'vessel__vessel_cost__cost',
                                            'power_supplies__power_supplies_cost__cost'))
    assert o('powercore_capital__powercore_capital') == pytest.approx(powercore, rel=1e-9)
    bop = sum(o(n) for n in ('turbine__turbine_cost__cost', 'electric_plant__electric_cost__cost',
                             'heat_rejection__heat_rejection_cost__cost', 'misc_plant__misc_cost__cost'))
    assert o('bop_capital__bop_capital') == pytest.approx(bop, rel=1e-9)
    aux = o('cryoplant__aux_cooling__cost')
    assert aux == pytest.approx(o('cryoplant__aux_cooling__aux_cost') + o('cryoplant__aux_cooling__cryo_cost'), rel=1e-12)
    cas22 = powercore + sum(o(n) for n in ('remote_handling__cost', 'installation__cost', 'heat_transport__cooling_selection__cost',
                                           'waste__cost', 'fuel_cycle__processing_cost__cost', 'other_rpe__cost', 'inc_cost__cost')) + aux
    assert o('cas22_capital__cas22_capital') == pytest.approx(cas22, rel=1e-9)
    cas28 = row.inputs.get(row.prefix + 'cas28_capital') if row.inputs else None
    cas28 = cas28 if cas28 is not None else route.interface(row.unit)['baseline_point'][row.prefix + 'cas28_capital']
    cas2x = o('buildings__facility_accounts__cost') + cas22 + bop + o('special_materials_capital__special_materials_capital') + cas28
    assert o('cas2x_pre_contingency__cas2x_pre_contingency') == pytest.approx(cas2x, rel=1e-9)
    cas20 = cas2x + o('contingency__cost')
    assert o('cas20_capital__cas20_capital') == pytest.approx(cas20, rel=1e-9)
    total = o('facility_preconstruction__cost') + cas20 + o('indirect__cost') + o('owner__cost') + o('supplementary__cost')
    assert o('overnight_capital__overnight_capital') == pytest.approx(total, rel=1e-9)
    assert o('total_capital__total_capital') == pytest.approx(total, rel=1e-9)
    annual = o('cas71_calc__levelized') + o('cooling_annual__cas72_total') + o('cas80_calc__levelized')
    assert o('cas70_calc__annual_total') == pytest.approx(annual, rel=1e-9)
    point = route.interface(row.unit)['baseline_point'] | (row.inputs or {})
    d, N, Yc = (float(point[row.prefix + k]) for k in ('discount_rate', 'operational_years', 'construction_years'))
    crf = 1.0 / N if d == 0 else d / -math.expm1(-N * math.log1p(d))
    lcoe = (total * math.exp(Yc / 2.0 * math.log1p(d)) * crf + annual) / (8760.0 * o('pb__p_net') * o('calendar__availability'))
    assert o('lcoe_calc__lcoe') == pytest.approx(lcoe, rel=1e-9)


def test_13_decomposition_closes_to_lcoe():
    _closure(rebco(), 'magnet__winding_sum__cost')
    _closure(nb3sn(), 'magnet__winding_sum__cost')
    _closure(one('reference', {}), 'magnet__winding_procurement__cost')
    row = rebco()
    assert row['magnet__winding_sum__cost'] == pytest.approx(row['magnet__inventory__sc_cost'] + row['magnet__inventory__materials_cost']
                                                             + row['magnet__material_inventory__cost_helium']
                                                             + row['magnet__winding_procurement__winding_fabrication_cost'], rel=1e-15)
