"""Default supplied designs of the two WI-100 material instances (design sections 1.2 and 2.10; contract r4 section 5).

Writes exploration/stellarator_materials/reference_designs.json, the defaults the materials design files carry
(the WI-099 reference-case.json precedent). These are design-file defaults, not the study's offer policy: the policy
re-supplies every design it records, and the study never evaluates a package on generated defaults it did not name.

* REBCO (`rebco_material`): the contract section 6 basis bridge. The Stellaris supplied design unchanged, Round 1's
  REBCO tape on construction C at 50 kA and the reference field, and n_elements equal to the plant's own
  composition-implied tape count in 4 mm units: 1.5 x parallel_tapes_set (coordinator amendment A6; the plant's
  6 mm tape metres correspond to the set count, and the set/reference factor f_set/f_wp_vol is reported, not absorbed).
* Nb3Sn (`nb3sn_material`): the anchored-cell equal-duty 12 T design at R 12.7 m, 50 kA, construction P. The
  contract section 5 rules that act on the magnet and cryoplant are applied here in closed form, iterated to a fixed
  point on the radial allocation (the bore factor moves the field, the field moves the count and the steel rule, the
  gross area moves the pack side, the pack side moves the allocation): turns = ampere-turns / 50 kA rounded up; the
  smallest strand count meeting the temperature rule (Round 1's own body); construction P areas rounded up to 1e-6 mm2;
  pack side sqrt(turns x gross) rounded up to 5 mm; coil_t and interior_y by the allocation rule rounded up to 10 mm;
  m_support = 11,615.6 t x W_mag / 111 GJ; cold and intercept ratings from the fixed rating list at Round 1's staged
  loads. The plasma point, installed heating, package ratings and purchase costs and power classes are held at the
  Stellaris supplied values: they need plant evaluations (the policy's matched-power ladder and re-supply loop), which
  are the offer policy's, not this default's (design K22).

Every closed-form plant expression below repeats the model's own operation order (cited), so the numbers agree with
the generated package; the build's baseline execution and tests/models/test_stellarator_materials.py check them.
Run: .codex-test/run python exploration/stellarator_materials/make_reference_designs.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PIN_OUTPUTS = ROOT / 'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration/baseline.json'
PIN_INPUTS = ROOT / 'work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-probe/baseline-inputs.json'
ROUND1_DESIGN = 'models/designs/magnet_materials/magnet_subsystem.sysml'
ROUND1_BODIES = ROOT / 'exploration/magnet_materials/bodies/magnet_conductor_alternatives'
CONTRACT = 'work/orchestration/goals/magnet-material-comparison/evidence/plant-contract.md'
DESIGN = 'work/active/WI-100_stellarator-material-variants/design.md'
OUT = HERE / 'reference_designs.json'
P = 'stellarator_09__stellaris__'

# Contract r4 section 5 and Round 1's offer policy (exploration/magnet_materials/studies/offer_policy.py:43, 141-164).
RATINGS_W = (1e3, 1.5e3, 2e3, 3e3, 5e3, 7.5e3, 10e3, 15e3, 20e3, 30e3, 50e3, 75e3)
TURN_CURRENT = 50000.0
NB3SN_TARGET_B = 12.0
M_SUPPORT_ANCHOR_KG = 11615.6e3  # contract section 5 structure-mass rule
W_MAG_ANCHOR_J = 111e9
EPS_INTRINSIC_BASELINE = -0.003  # supplied by the manifest point, never by the file (K6)
A_S = 0.36 * 0.36 * 1e6 / 308.0  # Stellaris Table 7 envelope per turn, mm2 (WI-099 design A2)
CONSTRUCTION = {
    'P': dict(cabling_factor=0.97, cable_void=0.20, ins_fraction=0.237, J_cu_rule=93.4, cu_void=0.10, cu_per_kA_rule=0.0,
              steel_per_kA_rule=12.66, B_steel_ref=12.04, steel_B_scaling=1.0, misc_per_kA=1.1077, solder_per_kA=0.0),
    'C': dict(cabling_factor=1.0, cable_void=0.0, ins_fraction=0.0, J_cu_rule=0.0, cu_void=0.0,
              cu_per_kA_rule=0.35 * A_S / 50.0, steel_per_kA_rule=0.36 * A_S / 50.0, B_steel_ref=24.9, steel_B_scaling=1.0,
              misc_per_kA=0.08 * A_S / 50.0, solder_per_kA=0.12 * A_S / 50.0),
}
CONSTRUCTION_REF = {
    'P': 'contract r4 section 4 construction P (EU DEMO layer-1 calibrated); exploration/magnet_materials/studies/offer_policy.py:155-159',
    'C': 'contract r4 section 4 construction C, unrounded Stellaris Table 7 calibration (WI-099 design A2); exploration/magnet_materials/studies/offer_policy.py:141-164',
}
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def body(name):
    spec = importlib.util.spec_from_file_location('wi100_ref_' + name, ROUND1_BODIES / (name + '_impl.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.calculate


NB3SN = body('nb3sn_cable_critical_surface')
REBCO = body('rebco_cable_critical_surface')
AREA = body('winding_turn_area_screen')
COLD = body('magnet_cold_stage_load')


def round1_values():
    """Round 1 design-file values by part and attribute, with their line numbers."""
    part, found = None, {}
    for number, line in enumerate((ROOT / ROUND1_DESIGN).read_text().split('\n'), 1):
        match = re.match(r'\s*part (\w+) \{', line)
        if match:
            part = match.group(1)
        match = re.match(r'\s*attribute (\w+) : Real = ([-0-9.eE+]+) \{', line)
        if match:
            found[(part, match.group(1))] = (float(match.group(2)), number)
    return found


def round_up(x, step):
    """Round x up to the next multiple of step, guaranteeing the result is >= x."""
    k = math.ceil(x / step - 1e-12)
    while k * step < x:
        k += 1
    return round(k * step, 10)


def round_up_1e6(x):
    """Round up to the next 1e-6 mm2 (WI-099 design D1), guaranteeing the float result is >= x."""
    k = math.ceil(x * 1e6)
    r = k / 1e6
    while r < x:
        k += 1
        r = k / 1e6
    return r


def plant_geometry(pin, coil_t, turns, wp_side):
    """The plant's field, bore and volume chain at a supplied allocation, turns and pack side (model operation order)."""
    R = pin[P + 'plasma__R']
    vessel_or = PIN_OUT[P + 'rb__r_coil']  # the radial build's vessel_or at the held stack
    r_coil_centre = vessel_or + coil_t / 2.0  # mfe_plasma_scaling.sysml:145
    I_coil = turns * TURN_CURRENT  # 'Winding Operating State'
    B_axis = pin[P + 'magnet__field_calc__mu0'] * pin[P + 'magnet__coil__k_link'] * pin[P + 'magnet__coil__n_coils'] * I_coil / (
        pin[P + 'magnet__field_calc__two_pi'] * R)  # mfe_magnet_field.sysml:57
    R_ref, a_ref = pin[P + 'magnet__coil__R_ref'], pin[P + 'magnet__coil__a_coil_ref']
    bore_norm = (R / (R - r_coil_centre)) / (R_ref / (R_ref - a_ref))  # conductor_peak_field_impl.py
    B_peak = (B_axis * pin[P + 'magnet__coil__peak_ratio']) * bore_norm
    c_coil = pin[P + 'magnet__coil__c_coil_ref'] * (r_coil_centre / a_ref)  # mfe_magnet_field.sysml:215
    f_wp_vol, n_coils = pin[P + 'magnet__winding_pack__f_wp_vol'], pin[P + 'magnet__coil__n_coils']
    vol_cold_total = f_wp_vol * n_coils * wp_side * wp_side * c_coil + pin[P + 'magnet__vol_cold_cryo']  # :258
    W_mag = pin[P + 'magnet__casing__W_mag_ref'] * (I_coil / pin[P + 'magnet__coil__I_ref']) ** 2 * (
        r_coil_centre / a_ref) ** 2 * (R_ref / R)  # :361-362
    return dict(r_coil_centre=r_coil_centre, I_coil=I_coil, B_axis=B_axis, bore_norm=bore_norm, B_peak=B_peak, c_coil=c_coil,
                vol_cold_total=vol_cold_total, W_mag=W_mag)


def construction_areas(kind, I, B, elem_cu):
    c = CONSTRUCTION[kind]
    if c['J_cu_rule'] > 0:
        cu = max(0.0, I / c['J_cu_rule'] - elem_cu) / (1 - c['cu_void'])
    else:
        cu = c['cu_per_kA_rule'] * I / 1000
    steel = c['steel_per_kA_rule'] * (I / 1000) * (B / c['B_steel_ref'] if c['steel_B_scaling'] == 1 else 1.0)
    areas = dict(cabling_factor=c['cabling_factor'], cable_void=c['cable_void'], cu_space=round_up_1e6(cu),
                 steel_area=round_up_1e6(steel), misc_area=round_up_1e6(c['misc_per_kA'] * I / 1000),
                 solder_area=round_up_1e6(c['solder_per_kA'] * I / 1000) if c['solder_per_kA'] > 0 else 0.0,
                 ins_fraction=c['ins_fraction'], J_cu_rule=c['J_cu_rule'], cu_void=c['cu_void'],
                 cu_per_kA_rule=c['cu_per_kA_rule'], steel_per_kA_rule=c['steel_per_kA_rule'], B_steel_ref=c['B_steel_ref'],
                 steel_B_scaling=c['steel_B_scaling'])
    return areas, dict(cu_required=cu, steel_required=steel)


def allocation(pin, wp_side, internal):
    """Contract section 5: wp_side x (1 + internal) + 2 ground + 2 clearance + 2 wall, rounded up to 10 mm."""
    raw = wp_side * (1 + internal) + 2 * pin[P + 'magnet__winding_pack__ground_insulation'] + 2 * pin[
        P + 'magnet__casing__assembly_clearance'] + 2 * pin[P + 'magnet__casing__wall_thickness']
    return round_up(raw, 0.01), raw


def cold_inputs(pin, law, T_cold, geometry, wp_side):
    """Round 1 cold-stage inputs at the plant's own static terms ('Staged Static Loads', library expression order)."""
    n_coils, t_case = pin[P + 'magnet__coil__n_coils'], pin[P + 'cryoplant__t_case']
    T_shield, T_amb = pin[P + 'cryoplant__T_shield'], pin[P + 'cryoplant__T_amb_cryo']
    area_cold = n_coils * geometry['c_coil'] * 4.0 * (wp_side + 2.0 * t_case)
    q_radiation = area_cold * pin[P + 'cryoplant__eps_eff'] * pin[P + 'cryoplant__sigma_SB'] * (T_shield ** 4 - T_cold ** 4)
    conduction_ref = n_coils * pin[P + 'cryoplant__g_per_coil'] * pin[P + 'cryoplant__k_c'] * (T_shield - law['T_conduction_ref'])
    shield_static = (pin[P + 'cryoplant__shield_area_ratio'] * area_cold * pin[P + 'cryoplant__q_MLI'] - q_radiation
                     + n_coils * pin[P + 'cryoplant__g_per_coil'] * pin[P + 'cryoplant__k_s'] * (T_amb - T_shield) - conduction_ref)
    q_nuc = pin[P + 'magnet__winding_pack__q_nuc_cryo']
    q_structure = pin[P + 'cryoplant__q_nuc_structure'] * pin[P + 'magnet__m_support'] / pin[P + 'cryoplant__rho_structure']
    x = dict(T_supply=T_cold, T_shield=T_shield, T_amb=T_amb, turn_current=TURN_CURRENT,
             nuclear_density=q_nuc + q_structure / geometry['vol_cold_total'], cold_volume=geometry['vol_cold_total'],
             radiation_ref=q_radiation, conduction_ref=conduction_ref, T_conduction_ref=law['T_conduction_ref'],
             n_leads=pin[P + 'cryoplant__n_leads'], f_lead=pin[P + 'cryoplant__f_lead'], L0=pin[P + 'cryoplant__L0'],
             p_joint_ref=pin[P + 'cryoplant__p_fixed_cryo'] * 1e6, I_joint_ref=law['I_joint_ref'], shield_static=shield_static,
             load_multiplier=law['load_multiplier'])
    x.update({k: law['nist_' + k] for k in ('k_a', 'k_b', 'k_c', 'k_d', 'k_e', 'k_f', 'k_g', 'k_h', 'k_i')})
    return x


def listed(q):
    return next(r for r in RATINGS_W if r >= q)


PIN_OUT = json.loads(PIN_OUTPUTS.read_text())['outputs']


def main():
    pin = json.loads(PIN_INPUTS.read_text())
    r1 = round1_values()
    cite = lambda part, name: f'{ROUND1_DESIGN}:{r1[(part, name)][1]}'
    val = lambda part, name: r1[(part, name)][0]
    designs = {}

    # ---- shared cryoplant facts (design section 2.7; Round 1 nb3sn/rebco blocks carry identical values) ----
    def cryo_law(part):
        law = {'nist_' + k: val(part, k) for k in ('k_a', 'k_b', 'k_c', 'k_d', 'k_e', 'k_f', 'k_g', 'k_h', 'k_i')}
        law.update({k: val(part, k) for k in ('load_multiplier', 'eta_mode', 'eta_const', 'green_a', 'green_b', 'capital_mode',
                                              'green_c', 'green_d', 'T_green')})
        law['usd2015_to_2021'] = val('economics', 'usd2015_to_2021')
        law['T_conduction_ref'] = 20.0
        law['I_joint_ref'] = 50000.0
        refs = {'nist_' + k: cite(part, k) for k in ('k_a', 'k_b', 'k_c', 'k_d', 'k_e', 'k_f', 'k_g', 'k_h', 'k_i')}
        refs.update({k: cite(part, k) for k in ('load_multiplier', 'eta_mode', 'eta_const', 'green_a', 'green_b', 'capital_mode',
                                                'green_c', 'green_d', 'T_green')})
        refs['usd2015_to_2021'] = cite('economics', 'usd2015_to_2021')
        refs['T_conduction_ref'] = 'models/designs/stellarator_09/stellarator_plant.sysml:1387 (the plant k_c segment basis, 20 K)'
        refs['I_joint_ref'] = 'models/designs/stellarator_09/stellarator_plant.sysml:1416 with :202 (joint losses at 50 kA)'
        return law, refs

    # ================================================================ REBCO basis bridge
    geometry = plant_geometry(pin, pin[P + 'magnet__coil__coil_t'], pin[P + 'magnet__coil__reference_turns'],
                              pin[P + 'magnet__winding_pack__wp_side'])
    assert geometry['B_peak'] == PIN_OUT[P + 'magnet__peak_field_calc__B_peak'], geometry['B_peak']
    tapes_set = PIN_OUT[P + 'magnet__conductor_current__parallel_tapes_set']
    tapes_ref = PIN_OUT[P + 'magnet__conductor_current__parallel_tapes_reference']
    width_ratio = pin[P + 'magnet__winding_pack__tape_width'] / val('rebco', 'tape_width')
    n_rebco = tapes_set * width_ratio
    law = {k: val('rebco', k) for k in ('tape_width', 'tape_thickness', 'tape_copper_fraction', 'nuclear_rise', 'margin_rise',
                                         'anchor_ic', 'g8', 'g10', 'g12', 'g15', 'g20', 'alpha', 'T_star', 'degradation',
                                         'fraction_rule', 'acceptance_rule', 'B_knot_min', 'B_knot_max', 'B_law_min',
                                         'T_law_min', 'T_law_max', 'element_density', 'element_price_per_m')}
    refs = {k: cite('rebco', k) for k in law}
    law['B_law_max'] = 25.0
    refs['B_law_max'] = f'{CONTRACT} section 4 (F10: B_law_max 25 T, beyond both declared law extents, admitted to carry the reference)'
    elem = REBCO(dict(n_tapes=n_rebco, tape_width=law['tape_width'], tape_thickness=law['tape_thickness'],
                      tape_copper_fraction=law['tape_copper_fraction'], turn_current=TURN_CURRENT, B_peak=geometry['B_peak'],
                      T_supply=20.0, nuclear_rise=law['nuclear_rise'], margin_rise=law['margin_rise'], anchor_ic=law['anchor_ic'],
                      shape_mode=1.0 if geometry['B_peak'] > law['B_knot_max'] else 0.0, g8=law['g8'], g10=law['g10'],
                      g12=law['g12'], g15=law['g15'], g20=law['g20'], alpha=law['alpha'], T_star=law['T_star'],
                      degradation=law['degradation'], fraction_rule=law['fraction_rule'], acceptance_rule=law['acceptance_rule'],
                      B_knot_min=law['B_knot_min'], B_knot_max=law['B_knot_max'], B_law_min=law['B_law_min'],
                      B_law_max=law['B_law_max'], T_law_min=law['T_law_min'], T_law_max=law['T_law_max']))
    areas, gen = construction_areas('C', TURN_CURRENT, geometry['B_peak'], elem['element_copper_area'])
    cryo, cryo_refs = cryo_law('rebco')
    bindings = dict(n_elements=n_rebco, **{k: v for k, v in law.items()}, **areas)
    binding_refs = {**refs, **{k: CONSTRUCTION_REF['C'] for k in areas},
                    'n_elements': f'{DESIGN} section 2.10 and coordinator amendment A6: 1.5 x parallel_tapes_set '
                                  f'(pin output magnet__conductor_current__parallel_tapes_set = {tapes_set!r}, 6 mm tapes) in 4 mm units'}
    designs['rebco_material'] = dict(
        label='basis bridge (contract r4 section 6): the Stellaris supplied design with Round 1 REBCO on construction C; '
              'a reconciliation point, expected to fail acceptance, not a ranked design',
        magnet=dict(values=bindings, references=binding_refs),
        coil=dict(values=dict(arm_x_ref=35.278), references=dict(arm_x_ref=f'{CONTRACT} section 3.2 (arm anchor, C); evidence/check-field-relations.md Relation 2')),
        cryoplant=dict(values=cryo, references=cryo_refs),
        existing=dict(values={'cryoplant.T_cold_cryo': 20.0, 'cryoplant.rated_cryogenic_cold_K': 20.0,
                              'magnet.winding_pack.B_max': 25.0, 'magnet.winding_pack.eps_cond_allow': 0.004},
                      references={'cryoplant.T_cold_cryo': f'{CONTRACT} section 4 (REBCO supply 20 K); unchanged Stellaris value',
                                  'cryoplant.rated_cryogenic_cold_K': 'matches the supply temperature (design E8)',
                                  'magnet.winding_pack.B_max': f'{CONTRACT} sections 3.2 and 4 (supplied REBCO envelope 25.0 T, a flag)',
                                  'magnet.winding_pack.eps_cond_allow': 'Stellaris strain screen 0.4 percent, unchanged (contract section 4)'}),
        manifest_point={'magnet__conductor__eps_intrinsic_in': None},
        diagnostics=dict(B_peak=geometry['B_peak'], parallel_tapes_set=tapes_set, parallel_tapes_reference=tapes_ref,
                         set_to_reference_factor=tapes_ref / tapes_set,
                         f_set_over_f_wp_vol=pin[P + 'magnet__coil__f_set'] / pin[P + 'magnet__winding_pack__f_wp_vol'],
                         acceptance_margin=elem['acceptance_margin'], operating_fraction=elem['operating_fraction'],
                         status_code=elem['status_code'], element_area_total=elem['element_area_total'],
                         construction_generation=gen, pack_share_per_turn=pin[P + 'magnet__winding_pack__wp_side'] ** 2 * 1e6 / 308.0))

    # ================================================================ Nb3Sn equal-duty 12 T
    law = {k: val('nb3sn', k) for k in ('strand_diameter', 'strand_copper_fraction', 'p', 'q', 'C1', 'Ca1', 'Ca2', 'eps0a', 'Bc20',
                                         'Tc0', 'nuclear_rise', 'margin_rise', 'fraction_rule', 'acceptance_rule', 'B_law_min',
                                         'B_law_max', 'B_design_max', 'B_edge_max', 'T_law_min', 'T_law_max', 'eps_min', 'eps_max',
                                         'element_density', 'element_price_per_m')}
    refs = {k: cite('nb3sn', k) for k in law}
    T_cold = 4.5
    coil_t = pin[P + 'magnet__coil__coil_t']
    history = []
    for _ in range(50):
        g0 = plant_geometry(pin, coil_t, 1.0, 1.0)
        # target peak under the design's own bore factor: B_peak is linear in the ampere-turns at fixed geometry
        at_target = NB3SN_TARGET_B / (g0['B_peak'] / g0['I_coil'])
        turns = float(math.ceil(at_target / TURN_CURRENT - 1e-12))
        geometry = plant_geometry(pin, coil_t, turns, 1.0)
        B = geometry['B_peak']
        base = dict(strand_diameter=law['strand_diameter'], strand_copper_fraction=law['strand_copper_fraction'],
                    turn_current=TURN_CURRENT, B_peak=B, T_supply=T_cold, **{k: law[k] for k in (
                        'nuclear_rise', 'margin_rise', 'p', 'q', 'C1', 'Ca1', 'Ca2', 'eps0a', 'Bc20', 'Tc0', 'fraction_rule',
                        'acceptance_rule', 'B_law_min', 'B_law_max', 'B_design_max', 'B_edge_max', 'T_law_min', 'T_law_max',
                        'eps_min', 'eps_max')}, eps_intrinsic=EPS_INTRINSIC_BASELINE)
        n = 1
        # smallest integer strand count meeting the acceptance rule (Round 1 offer policy, smallest_n)
        T_rule = T_cold + law['nuclear_rise'] + law['margin_rise']
        guess = NB3SN(dict(base, n_strands=1.0))
        s = guess['ic_strand_op']
        n = max(1, int(TURN_CURRENT / max(s, 1e-9)) - 2) if s > 0 else 1
        while NB3SN(dict(base, n_strands=float(n)))['acceptance_margin'] < 0:
            n += 1
        while n > 1 and NB3SN(dict(base, n_strands=float(n - 1)))['acceptance_margin'] >= 0:
            n -= 1
        cond = NB3SN(dict(base, n_strands=float(n)))
        areas, gen = construction_areas('P', TURN_CURRENT, B, cond['element_copper_area'])
        screen = AREA(dict(turn_current=TURN_CURRENT, B_peak=B, available_area=1.0, element_area=cond['element_area_total'],
                           element_copper_area=cond['element_copper_area'], **{k: areas[k] for k in (
                               'cabling_factor', 'cable_void', 'cu_space', 'steel_area', 'misc_area', 'solder_area',
                               'ins_fraction', 'J_cu_rule', 'cu_void', 'cu_per_kA_rule', 'steel_per_kA_rule', 'B_steel_ref',
                               'steel_B_scaling')}))
        wp_side = round_up(math.sqrt(turns * screen['gross_area'] * 1e-6), 0.005)
        new_coil_t, raw_x = allocation(pin, wp_side, pin[P + 'magnet__winding_pack__internal_build_x'])
        interior_y, raw_y = allocation(pin, wp_side, pin[P + 'magnet__winding_pack__internal_build_y'])
        history.append(dict(coil_t=coil_t, turns=turns, B_peak=B, n=n, gross=screen['gross_area'], wp_side=wp_side,
                            new_coil_t=new_coil_t))
        if new_coil_t == coil_t:
            break
        coil_t = new_coil_t
    else:
        raise AssertionError(f'no fixed point: {history}')
    geometry = plant_geometry(pin, coil_t, turns, wp_side)
    assert geometry['B_peak'] == B
    m_support = M_SUPPORT_ANCHOR_KG * (geometry['W_mag'] / W_MAG_ANCHOR_J)
    cryo, cryo_refs = cryo_law('nb3sn')
    pin_local = dict(pin)
    pin_local[P + 'magnet__m_support'] = m_support
    cold = COLD(cold_inputs(pin_local, cryo, T_cold, geometry, wp_side))
    bindings = dict(n_elements=float(n), **law, **areas)
    binding_refs = {**refs, **{k: CONSTRUCTION_REF['P'] for k in areas},
                    'n_elements': 'smallest strand count meeting the Nb3Sn temperature rule at the design field and 5.2 K with '
                                  'eps_intrinsic -0.003 (Round 1 offer rule, contract r4 section 5)'}
    designs['nb3sn_material'] = dict(
        label='anchored-cell equal-duty 12 T design at R 12.7 m, 50 kA, construction P; magnet and cryoplant rules of '
              'contract section 5 applied, plasma, heating, packages and classes held at the Stellaris values (K22)',
        magnet=dict(values=bindings, references=binding_refs),
        coil=dict(values=dict(arm_x_ref=35.278), references=dict(arm_x_ref=f'{CONTRACT} section 3.2 (arm anchor, C); evidence/check-field-relations.md Relation 2')),
        cryoplant=dict(values=cryo, references=cryo_refs),
        existing=dict(values={'magnet.coil.reference_turns': turns, 'magnet.coil.coil_t': coil_t,
                              'magnet.winding_pack.wp_side': wp_side, 'magnet.casing.interior_y': interior_y,
                              'magnet.m_support': m_support, 'magnet.winding_pack.B_max': 13.0,
                              'magnet.winding_pack.eps_cond_allow': 0.003,
                              'cryoplant.T_cold_cryo': T_cold, 'cryoplant.rated_cryogenic_cold_K': T_cold,
                              'cryoplant.rated_cold_W': listed(cold['q_cold']), 'cryoplant.rated_intercept_W': listed(cold['q_shield'])},
                      references={'magnet.coil.reference_turns': 'ampere-turns for 12 T peak under the design bore factor / 50 kA, rounded up (contract section 5)',
                                  'magnet.coil.coil_t': 'pack side plus 2 ground plus 2 clearance plus 2 wall, rounded up to 10 mm (contract section 5)',
                                  'magnet.winding_pack.wp_side': 'sqrt of turns times the construction P gross area per turn, rounded up to 5 mm (contract section 5)',
                                  'magnet.casing.interior_y': 'the allocation rule with the internal y fraction, rounded up to 10 mm (contract section 5)',
                                  'magnet.m_support': '11615.6 t times W_mag over 111 GJ, the unsourced stored-energy scaling (contract section 5)',
                                  'magnet.winding_pack.B_max': f'{CONTRACT} sections 3.2 and 4 (supplied Nb3Sn envelope 13.0 T, a flag)',
                                  'magnet.winding_pack.eps_cond_allow': 'unsourced allowable 0.3 percent (contract section 4, F11); screened only',
                                  'cryoplant.T_cold_cryo': f'{CONTRACT} section 4 (Nb3Sn supply 4.5 K)',
                                  'cryoplant.rated_cryogenic_cold_K': 'matches the supply temperature (design E8)',
                                  'cryoplant.rated_cold_W': 'smallest listed rating at or above the staged cold load (contract section 5 fixed list)',
                                  'cryoplant.rated_intercept_W': 'smallest listed rating at or above the staged intercept load (contract section 5 fixed list)'}),
        manifest_point={'magnet__conductor__eps_intrinsic_in': EPS_INTRINSIC_BASELINE},
        diagnostics=dict(fixed_point=history, B_peak=B, B_axis=geometry['B_axis'], I_coil=geometry['I_coil'],
                         W_mag=geometry['W_mag'], vol_cold_total=geometry['vol_cold_total'], c_coil=geometry['c_coil'],
                         r_coil_centre=geometry['r_coil_centre'], acceptance_margin=cond['acceptance_margin'],
                         acceptance_margin_n_minus_1=NB3SN(dict(base, n_strands=float(n - 1)))['acceptance_margin'],
                         status_code=cond['status_code'], T_cs=cond['T_cs'], gross_area=screen['gross_area'],
                         pack_share_per_turn=wp_side ** 2 * 1e6 / turns, construction_generation=gen,
                         fit_raw_x=raw_x, fit_raw_y=raw_y, staged_q_cold=cold['q_cold'], staged_q_shield=cold['q_shield'],
                         held_at_stellaris=['plasma point (R, a, n_e0, T_i0)', 'installed heating', 'package ratings and purchase costs',
                                            'power classes', 'power_supplies.rated_tf_MWe']))
    doc = dict(note=__doc__.split('\n\n')[0], generator='exploration/stellarator_materials/make_reference_designs.py',
               sources={str(p.relative_to(ROOT)): sha(p) for p in (PIN_INPUTS, PIN_OUTPUTS, ROOT / ROUND1_DESIGN,
                        ROUND1_BODIES / 'nb3sn_cable_critical_surface_impl.py', ROUND1_BODIES / 'rebco_cable_critical_surface_impl.py',
                        ROUND1_BODIES / 'winding_turn_area_screen_impl.py', ROUND1_BODIES / 'magnet_cold_stage_load_impl.py')},
               designs=designs)
    OUT.write_text(json.dumps(doc, indent=1) + '\n')
    for name, d in designs.items():
        print(name, json.dumps(d['existing']['values']), 'n_elements', d['magnet']['values']['n_elements'])
        print('  diagnostics', {k: v for k, v in d['diagnostics'].items() if k not in ('fixed_point',)})


if __name__ == '__main__':
    main()
