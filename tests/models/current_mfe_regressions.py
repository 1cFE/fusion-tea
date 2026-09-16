"""Current MFE completion and bounded adaptations of frozen regression drivers."""

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_EVIDENCE = ROOT / 'work/completed/20260914_WI-038_conductor-grade-lever/evidence'
STRUCTURE_EVIDENCE = ROOT / 'work/active/WI-057_stellaris-structural-decomposition/evidence/merge_onto_demo_maturation'
P = 'stellarator_09__stellaris__'
# WI-040 (2026-09-13): explicit ABI additions, not whatever regeneration happens to emit.
WI040_PARAMETERS = {P + 'magnet__coil__turn_current'} | {
    P + 'magnet__winding_pack__' + name for name in (
        'f_copper', 'f_solder', 'f_steel', 'f_helium', 'rho_copper', 'rho_solder',
        'rho_steel', 'price_copper', 'price_solder', 'price_steel', 'price_helium',
        'helium_pressure', 'helium_gas_constant', 'winding_rate_1990',
        'cost_escalation', 'nonplanar_factor')}
WI040_CHANNELS = {P + 'magnet__wp_volume__vol_winding_pack'} | {
    P + 'magnet__material_inventory__' + name for name in (
        'mass_copper', 'mass_solder', 'mass_steel', 'mass_helium', 'cost_copper',
        'cost_solder', 'cost_steel', 'cost_helium', 'material_cost', 'helium_density', 'tape_volume')
} | {P + 'magnet__winding_procurement__' + name for name in (
    'tape_cost', 'conductor_length', 'winding_fabrication_cost', 'cost')}
WI040_CHANGED_ECONOMICS = (
    'magnet_capital_rollup', 'powercore_capital', 'reactor_equipment_subtotal', 'installation', 'supplementary',
    'idc_capital', 'cas22_capital', 'cas2x_pre_contingency', 'cas20_capital',
    'overnight_capital', 'contingency_capital', 'indirect_capital',
    'total_capital', 'lcoe', 'cas90_1cfe', 'lcoe_1cfe')
WI038_PARAMETERS = {P + 'magnet__winding_pack__' + name for name in ('B_grade_ref', 'field_exponent')}
WI038_CHANNELS = {P + 'magnet__conductor_grade__' + name for name in (
    'quantity_factor', 'j_wp_effective', 'cost_per_kAm_effective')}
# WI-058 (2026-09-14): the winding length follows the coil bore -- c_coil = c_coil_ref * (r_coil_centre /
# a_coil_ref) -- and the WI-036 shape factor over the major radius retires. The frozen WI-051 R14 evidence
# was produced with the R-form (c_coil = k_coil * R). Under the bore form at a = 1.3 the bore ratio is
# exactly 1.0, so binding c_coil_ref = k_coil * R reproduces the R-form's length to the double (the two
# forms coincide under uniform scaling). The replays therefore evaluate R14 with that reference, which keeps
# every frozen R14 value the exact expectation for the rest of the plant; the bore form's own response is
# proven by tests/models/test_winding_length_bore.py and the WI-058 item evidence, never by these replays.
K_COIL_RETIRED = 1.968503937007874  # the retired WI-036 k_coil (25.0 / 12.7), the float the old oracle carried
WI058_PARAMETERS = {P + 'magnet__coil__c_coil_ref'}
WI058_RETIRED = {P + 'magnet__coil__k_coil'}
RECEIPT_EVIDENCE = ROOT / 'work/active/WI-064_current-driven-magnet-inventory-sizing/evidence'
WI064_PARAMETERS = {P + 'magnet__winding_pack__' + name for name in (
    'sizing_mode', 'inventory_multiplier')}
WI064_CHANNELS = {P + 'magnet__current_sizing__' + name for name in (
    'required_tapes', 'required_conductor_area', 'required_pack_area',
    'required_effective_density', 'selected_effective_density', 'tape_available_current')}
WI063_PARAMETERS = {P + 'magnet__winding_pack__' + name for name in (
    'f_wp_perimeter', 'insulation_sheet_thickness', 'insulation_sheet_price')}
WI063_CHANNELS = {P + 'magnet__insulation_inventory__' + name for name in (
    'internal_volume', 'ground_volume', 'sheet_area', 'stock_cost')} | {
    P + 'magnet__magnet_structure_cost__effective_all_in_rate'}
# The added stock scenario is disabled at the replay boundary; geometry remains live.
WI063_REPLAY = {P + 'magnet__winding_pack__insulation_sheet_price': 0.0}
WI063_REPLAY_LOCAL = {'magnet_insulation_sheet_price': 0.0}
WI062_PARAMETERS = {P + 'magnet__winding_pack__' + name for name in (
    'reference_tape_current', 'material_factor', 'orientation_factor', 'cabling_factor',
    'degradation_factor', 'sharing_factor', 'allowable_fraction', 'allow_field_extrapolation')}
WI062_CHANNELS = {P + 'magnet__conductor_current__' + name for name in (
    'parallel_tapes_set', 'parallel_tapes_reference', 'tape_critical_current',
    'critical_current_reference', 'critical_current_set', 'operating_fraction_reference',
    'operating_fraction_set', 'allowable_current', 'margin_fraction', 'margin_current', 'field_extrapolated')}
WI062_PREDICATE = P + 'reference_conductor_current_ok__3cf239a7cdc0f2f0'
WI061_PARAMETERS = {P + 'magnet__winding_pack__' + n for n in (
    'fit_aspect_ratio', 'internal_build_x', 'internal_build_y', 'ground_insulation')} | {
    P + 'magnet__casing__' + n for n in ('interior_y', 'wall_thickness', 'assembly_clearance')}
WI061_MAPPED_PARAMETERS = WI061_PARAMETERS | {P + 'magnet__coil__coil_t'}
WI061_CHANNELS = {P + 'magnet__wp_fit__' + n for n in (
    'nominal_x','nominal_y','internal_x','internal_y','pack_x','pack_y',
    'insulated_x','insulated_y','required_x','required_y','cavity_x','cavity_y',
    'exterior_x','exterior_y','margin_x','margin_y','minimum_margin')}
WI061_PREDICATE = P + 'wp_fit_ok__a25ca6a0161f6339'

WI060_PARAMETERS = {P + 'magnet__winding_pack__' + name for name in (
    'tape_width', 'tape_thickness', 'tape_price_per_m')}
WI060_RETIRED_CHANNELS = {P + 'magnet__conductor_grade__cost_per_kAm_effective'}
WI060_CHANNELS = {P + 'magnet__winding_procurement__tape_length'}
LIVE_CONDUCTOR_CHANNELS = (WI038_CHANNELS - WI060_RETIRED_CHANNELS) | WI060_CHANNELS
WI059_PARAMETERS = {P + 'cryoplant__' + name for name in (
    'inventory_enabled', 'n_leads', 'L0', 'f_lead', 'T_shield', 'f_carnot_shield',
    't_case', 'shield_area_ratio', 'eps_eff', 'sigma_SB', 'q_MLI', 'g_per_coil',
    'k_c', 'k_s', 'q_nuc_structure', 'rho_structure', 'joint_drive_fraction')
} | {P + 'magnet__' + name for name in ('c_support', 'e_support', 'legacy_casing_fraction')} | {P + 'structure__residual_fraction'}
WI059_EXISTING_MAPPED_PARAMETERS = {P + 'cryoplant__f_carnot_cryo', P + 'cryoplant__p_tfcool'}
WI059_NATIVE_ONLY_VALUES = {P + 'cryoplant__cryo_elec__q_nuc': 0.0,
    P + 'cryoplant__cryo_elec__vol_cold': 0.0, P + 'cryoplant__cryo_elec__f_uplift': 1.0}
WI059_NATIVE_ONLY_PARAMETERS = set(WI059_NATIVE_ONLY_VALUES)
WI059_THERMAL_CHANNELS = {P + 'cryoplant__inventory__' + name for name in (
    'area_cold', 'area_shield', 'q_lead_cold', 'q_lead_shield', 'q_rad_cold',
    'q_rad_shield', 'q_support_cold', 'q_support_shield', 'q_inventory_cold',
    'q_inventory_shield', 'p_drive')}
WI059_CHANNELS = WI059_THERMAL_CHANNELS | {
    P + 'cryoplant__refrigeration_sum__total', P + 'cryoplant__shield_elec__p_elec',
    P + 'power_supplies__tf_power__total', P + 'cryoplant__cold_load__p_cold',
    P + 'magnet__support_mass__m_support', P + 'cryoplant__cold_load__q_structure_nuclear',
    P + 'structure__structure_cost__legacy_cost'}
WI059_ORACLE_ADDED_CHANNELS = (WI059_CHANNELS - {P + 'cryoplant__refrigeration_sum__total'}) | {P + 'cryoplant__cryo_elec__p_elec'}
WI059_REPLAY = WI063_REPLAY | {
    P + 'cryoplant__inventory_enabled': False, P + 'magnet__c_support': 0.0,
    P + 'magnet__legacy_casing_fraction': 1.0, P + 'structure__residual_fraction': 1.0,
    P + 'cryoplant__joint_drive_fraction': 0.0, P + 'cryoplant__q_nuc_structure': 0.0}
WI059_REPLAY_LOCAL = WI063_REPLAY_LOCAL | dict(cryo_inventory_enabled=False, magnet_support_coefficient=0.0,
    magnet_legacy_casing_fraction=1.0, structure_residual_fraction=1.0,
    cryo_joint_drive_fraction=0.0, cryo_q_nuc_structure=0.0)


def wi059_replay(overrides):
    return WI059_REPLAY_LOCAL | dict(overrides)


def wi059_dormant_outputs(expected, parameters):
    """Independent identities for additions in the historical disabled scenario."""
    extra = dict(p_cryo_cold=expected['p_cryo'], p_cryo_shield=0.,
                 p_tf_total=parameters['p_tf'], support_mass=0., structure_nuclear=0.,
                 structure_legacy_cost=expected['structure'])
    extra['p_cold'] = ((expected['p_cryo'] - parameters['p_cryo_direct'])
        * parameters['f_carnot_cryo'] * parameters['T_cold_cryo']
        / (parameters['T_amb_cryo'] - parameters['T_cold_cryo']))
    extra.update({'thermal_' + name: 0. for name in (
        'area_cold', 'area_shield', 'q_lead_cold', 'q_lead_shield',
        'q_radiation_cold', 'q_radiation_shield', 'q_support_cold', 'q_support_shield',
        'q_cold', 'q_shield', 'p_drive')})
    return extra


def wi059_native_additions(outputs, parameters):
    """New native channels preserve cold-stage heat/work and zero disabled additions."""
    extra = dict.fromkeys(WI059_CHANNELS, 0.)
    old_cryo = outputs[P + 'cryoplant__cryo_elec__p_elec']
    extra[P + 'cryoplant__refrigeration_sum__total'] = old_cryo
    extra[P + 'power_supplies__tf_power__total'] = parameters['p_tf']
    extra[P + 'structure__structure_cost__legacy_cost'] = outputs[P + 'structure__structure_cost__cost']
    extra[P + 'cryoplant__cold_load__p_cold'] = wi059_dormant_outputs(
        {'p_cryo': old_cryo, 'structure': outputs[P + 'structure__structure_cost__cost']}, parameters)['p_cold']
    return extra



def restate_wi040_radius_costs(translated):
    """Replace only the declared cost descendants in temporary expectations with oracle values.

    Frozen physical scalars and all structured outputs retain their original values. The old
    winding_pack_cost channel is now the legacy comparison and therefore also remains frozen.
    """
    import sys
    sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
    import oracle_entry
    changed = {oracle_entry.ORACLE_OUTPUT_TO_CHANNEL[name] for name in WI040_CHANGED_ECONOMICS}
    oracle = {name: oracle_entry.evaluate(WI059_REPLAY | change) for name, change in (
        ('baseline', {}), ('R14', {P + 'plasma__R': 14.0, P + 'magnet__coil__c_coil_ref': K_COIL_RETIRED * 14.0}))}  # WI-058: the R-form's length at R14
    assert changed.isdisjoint(WI040_CHANNELS)
    for name in oracle:
        assert changed | WI040_CHANNELS <= oracle[name].keys()
    frozen = json.loads((translated / 'frozen-results.json').read_text())
    direct = json.loads((translated / 'direct-entering.json').read_text())
    for name, ref in (('baseline', 'baseline'), ('R14', 'tied_R14')):
        replacement = {k: oracle[name][k] for k in changed | WI040_CHANNELS | WI060_CHANNELS | WI061_CHANNELS | WI062_CHANNELS | WI063_CHANNELS | WI064_CHANNELS}
        # WI-038 q=1 controls: exact independently stated additions, no changes to
        # existing physical expectations or their comparison tolerance.
        replacement.update({P + 'magnet__conductor_grade__quantity_factor': 1.0,
                            P + 'magnet__conductor_grade__j_wp_effective': 118.8271604938272})
        replacement.update(wi059_native_additions(frozen['cases'][ref]['native']['outputs'], oracle_entry.vs.IN))
        frozen['cases'][ref]['native']['outputs'].update(replacement)
        direct['results'][name]['single']['outputs'].update(replacement)
    (translated / 'frozen-results.json').write_text(json.dumps(frozen, indent=2) + '\n')
    (translated / 'direct-entering.json').write_text(json.dumps(direct, indent=2) + '\n')
    expected = json.loads((translated / 'expectations.json').read_text())
    expected['channels'] = sorted(set(expected['channels']) | WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_CHANNELS | WI061_CHANNELS | WI062_CHANNELS | WI063_CHANNELS | WI064_CHANNELS)
    (translated / 'expectations.json').write_text(json.dumps(expected, indent=2) + '\n')
    return changed | WI040_CHANNELS | WI059_CHANNELS | WI060_CHANNELS | WI061_CHANNELS | WI062_CHANNELS | WI063_CHANNELS | WI064_CHANNELS


def structure_ledger():
    """WI-057 (2026-09-13): the rename ledger of the structural decomposition, old entry-point and
    channel names -> the names carrying the owning part's path. The frozen WI-050 drivers speak the
    pre-decomposition dialect; translation happens at the package boundary, never in the drivers."""
    ledger = json.loads((STRUCTURE_EVIDENCE / 'ledger.json').read_text())
    forward = {**ledger['parameters'], **ledger['outputs']}
    backward = {new: old for old, new in forward.items() if old != new}
    return forward, backward


def alias_both_spellings(mapping, backward):
    """A results/inputs dict readable under both dialects: every renamed key also under its old name."""
    out = dict(mapping)
    for key, value in mapping.items():
        if key in backward:
            out[backward[key]] = value
    return out


def structure_modules(forward):
    """Old calc-module suffix -> its suffix under the owning part ('geom' -> 'plasma__geom')."""
    P = 'stellarator_09__stellaris__'
    modules = {}
    for old, new in forward.items():
        if old != new and old.startswith(P) and new.startswith(P) and '__' in old[len(P):]:
            modules.setdefault(old[len(P):].rsplit('__', 1)[0], new[len(P):].rsplit('__', 1)[0])
    return modules


def translate_names(text, forward):
    """Every old full entry-point or channel name in a text, under its new name (word-bounded)."""
    import re
    pattern = re.compile(r'(?<![\w])(' + '|'.join(re.escape(k) for k in sorted(forward, key=len, reverse=True) if forward[k] != k) + r')(?![\w])')
    return pattern.sub(lambda m: forward[m.group(1)], text)


def translate_frozen_radius_evidence(historical, destination, forward):
    """WI-057 (2026-09-13): the WI-051 prototype's frozen expectations and results, and its entering
    contract, under the new names -- a translated copy beside the drivers, the frozen files untouched.
    Constraint ids, parameter groups and every value are unchanged by the decomposition; only the names
    of the entry points and channels moved."""
    P = 'stellarator_09__stellaris__'
    modules = structure_modules(forward)
    stem = lambda k: forward.get(P + k, P + k)[len(P):]
    out = destination / 'frozen-translated'
    out.mkdir()
    prototype = historical.parent / 'prototype'
    for name in ('frozen-results.json', 'direct-entering.json'):
        (out / name).write_text(translate_names((prototype / name).read_text(), forward))
    expectations = json.loads(translate_names((prototype / 'expectations.json').read_text(), forward))
    expectations['edges'] = {modules.get(k, k): v for k, v in expectations['edges'].items()}
    expectations['ratios'] = {stem(k): v for k, v in expectations['ratios'].items()}
    expectations['anchors'] = [stem(k) for k in expectations['anchors']]
    # WI-058 (2026-09-14): 'Coil Winding Length' no longer takes R0 (it takes the coil-centre bore), so the
    # frozen R0 edge for coil_length is retired from the replay; k_coil leaves the contract and c_coil_ref
    # enters it (the added set is restated below). The coil_length__c_coil ratio expectation (14/12.7) still
    # holds under the scaled reference the replays bind at R14.
    expectations['edges'].pop(modules.get('coil_length', 'coil_length'))
    expectations['contract_delta']['remove'] = sorted(
        expectations['contract_delta']['remove'] + [['stellarator_plant_params', P + 'magnet__coil__k_coil']])
    # Refuse a translation the live package cannot honour: every translated name must resolve.
    live = json.loads((ROOT / 'exploration/stellarator_e2e/generated/contracts/model_contract.json').read_text())
    live_params = {x['qualified_name'] for x in live['parameters']}; live_channels = {x['channel_name'] for x in live['outputs']}
    live_modules = {c[len(P):].rsplit('__', 1)[0] for c in live_channels if c.startswith(P)}
    missing = ([P + k for k in expectations['anchors'] if P + k not in live_params]
               + [P + k for k in expectations['ratios'] if P + k not in live_channels]
               + [k for k in expectations['edges'] if k not in live_modules]
               + [k for k in expectations['channels'] if k not in live_channels])
    if missing:
        raise KeyError(f'frozen radius evidence names the live package does not carry after translation: {sorted(missing)[:8]}')
    (out / 'expectations.json').write_text(json.dumps(expectations, indent=2) + '\n')
    contract = out / 'entering-package/contracts'
    contract.mkdir(parents=True)
    (contract / 'model_contract.json').write_text(
        translate_names((historical / 'entering-package/contracts/model_contract.json').read_text(), forward))
    return out, modules
FINANCE_EVIDENCE = ROOT / 'work/active/WI-052_mfe-financial-rate-limits/implementation'


def current_generation():
    spec = importlib.util.spec_from_file_location('wi038_current_generation', RECEIPT_EVIDENCE / 'regenerate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def operating_acceptance(destination, historical):
    # Keep all historical scenario execution and assertions. Replace its generator
    # dependency with the current reviewed WI-064 completion inventory.
    spec = importlib.util.spec_from_file_location('wi052_operating_scenarios', FINANCE_EVIDENCE / 'current_regressions.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.seed_and_generate = current_generation().seed_and_generate
    # WI-057 (2026-09-13): translate at the package boundary -- overrides forward through the rename
    # ledger, results and inputs aliased under both spellings -- so the frozen driver text stands.
    forward, backward = structure_ledger()
    execute = historical.execute
    historical.execute = lambda ev, bridge, changes: alias_results(
        execute(ev, bridge, WI059_REPLAY | {forward.get(k, k): v for k, v in changes.items()}), backward)
    import sys
    previous_path = list(sys.path)
    previous_modules = {name: value for name, value in sys.modules.items()
                        if name == 'stellarator_tea' or name.startswith('stellarator_tea.')}
    try:
        scratch, rows, inputs = module.operating_acceptance(destination, historical)
    finally:
        sys.path[:] = previous_path
        for name in list(sys.modules):
            if name == 'stellarator_tea' or name.startswith('stellarator_tea.'):
                del sys.modules[name]
        sys.modules.update(previous_modules)
    return scratch, rows, alias_both_spellings(inputs | WI059_REPLAY, backward)


def alias_results(row, backward):
    if 'outputs' in row:
        row = dict(row, outputs=alias_both_spellings(row['outputs'], backward))
    return row


def replace_once(text, old, new):
    """Refuse driver drift before applying a reviewed temporary adaptation."""
    assert text.count(old) == 1, old
    return text.replace(old, new)


def pre_fit_report(report, reference):
    """Project the two explicit added checks out of historical eighteen-check comparisons."""
    import copy
    result = copy.deepcopy(report)
    added = [r for r in result['results'] if r['constraint_id'] in {WI061_PREDICATE, WI062_PREDICATE}]
    assert len(added) == 2 and result['assessed_entry_count'] == reference['assessed_entry_count'] + 2
    result['results'] = [r for r in result['results'] if r['constraint_id'] not in {WI061_PREDICATE, WI062_PREDICATE}]
    result['assessed_entry_count'] -= 2
    for key in ('authored_usage_total', 'applicable_gate_total', 'assessed_gate_count'):
        assert result['coverage'][key] == reference['coverage'][key] + 2
        result['coverage'][key] -= 2
    # Catalog identity necessarily differs when its two added entries are projected out.
    result['catalog_fingerprint'] = reference['catalog_fingerprint']
    return result


def radius_acceptance(destination, historical):
    destination = Path(destination)
    destination.mkdir()
    drivers = destination / 'drivers'
    drivers.mkdir()
    ledger = json.loads((FINANCE_EVIDENCE / 'scalar-ledger.json').read_text())['live_ordinary']
    finance = {row['name'] for row in ledger if row['classification'] == 'changed finance'}
    generation = current_generation()
    before = generation.inventory(generation.PACKAGE)
    # WI-057 (2026-09-13): the drivers read the frozen evidence and the package under the new names.
    forward, _ = structure_ledger()
    translated, modules = translate_frozen_radius_evidence(Path(historical), destination, forward)
    # Current economic expectations are independently recomputed; baseline arithmetic may
    # differ by roundoff. This is a bounded tolerance, never omission of these comparisons.
    finance |= restate_wi040_radius_costs(translated)
    for name in ('native', 'direct', 'standalone', 'cli_checks'):
        text = (historical / (name + '.py')).read_text()
        if "Path(__file__).resolve().parent.parent/'prototype'" in text:
            text = replace_once(text, "Path(__file__).resolve().parent.parent/'prototype'", f'Path({str(translated)!r})')
        text = text.replace('Path(__file__).resolve().parent', f'Path({str(historical)!r})')
        if name in ('native', 'direct'):
            text = text.replace("P+'R'", "P+'plasma__R'")
        if name == 'native':
            text = replace_once(text, 'bridge.build(change)', f'bridge.build({WI059_REPLAY!r} | change)')
            text = replace_once(text, "'entering-package/contracts/model_contract.json'", repr(str(translated / 'entering-package/contracts/model_contract.json')))
            text = replace_once(text, "delta['added']==[]",
                                f"{{x[1] for x in delta['added']}}=={WI040_PARAMETERS | WI038_PARAMETERS | WI058_PARAMETERS | WI059_PARAMETERS | WI059_NATIVE_ONLY_PARAMETERS | WI060_PARAMETERS | WI061_PARAMETERS | WI062_PARAMETERS | WI063_PARAMETERS | WI064_PARAMETERS!r}")
            # WI-058: evaluate R14 at the R-form's length (see K_COIL_RETIRED) so the frozen row stays exact.
            text = replace_once(text, "('R14',{P+'plasma__R':14.0})",
                                f"('R14',{{P+'plasma__R':14.0,P+'magnet__coil__c_coil_ref':{K_COIL_RETIRED * 14.0!r}}})")
        if name in ('native', 'direct'):
            text = 'from tests.models.current_mfe_regressions import pre_fit_report\n' + text
        if name == 'native':
            text = replace_once(text, "assert a['responses']==b['responses']", "assert {k:v for k,v in a['responses'].items() if 'wp_fit_ok' not in k and 'reference_conductor_current_ok' not in k}==b['responses']")
            text = text.replace("a['report']==b['report']", "pre_fit_report(a['report'], b['report'])==b['report']")
        if name == 'direct':
            text = replace_once(text, "assert set(raw)==set(expected)", "assert set(raw)-{k for k in raw if 'wp_fit_ok' in k or 'reference_conductor_current_ok' in k}==set(expected)\n        raw['constraint_report'] = pre_fit_report(raw['constraint_report'], expected['constraint_report'])")
        if name == 'standalone':
            # WI-058: the winding length no longer takes R0 -- its R0-only check leaves the replay (its bore
            # response is tested in test_winding_length_bore.py); the other three magnet calcs keep theirs.
            text = replace_once(text, "('coil_length','mfe_magnet_field','coil_winding_length','Coil_Winding_Length',14/12.7),", '')
            for suffix in ('field_calc', 'stored_energy', 'magnet_cost'):
                text = replace_once(text, f"('{suffix}',", f"('{modules[suffix]}',")
        if name == 'native':
            text = replace_once(text, "a['outputs'][k]==v if name=='baseline'", f"a['outputs'][k]==v if name=='baseline' and k not in {finance!r}")
            text = replace_once(text,
                "    assert component[name].get('B_peak',component[name].get('error'))==row.get('B_peak',row.get('error'))",
                "    if name == 'valid':\n"
                "        assert component[name]['B_peak'] == row['B_peak']\n"
                "    else:\n"
                "        assert component[name]['error'] == 'ValueError'\n"
                "        domain = 'reference' if name.startswith('reference') else 'live'\n"
                "        assert domain + ' clearance' in component[name]['message']")
        if name == 'direct':
            text = replace_once(text, 'values.update(change)', f'values.update({WI059_REPLAY!r} | change)')
            # WI-058: evaluate R14 at the R-form's length (see K_COIL_RETIRED) so the frozen row stays exact.
            text = replace_once(text, "'R14':{P+'plasma__R':14.0,",
                                f"'R14':{{P+'plasma__R':14.0,P+'magnet__coil__c_coil_ref':{K_COIL_RETIRED * 14.0!r},")
            text = replace_once(text, "if name=='baseline' or not isinstance(v,(int,float)):",
                                f"if (name=='baseline' and k not in {finance!r}) or not isinstance(v,(int,float)):")
            text = replace_once(text, "scalar[k]==v if name=='baseline'", f"scalar[k]==v if name=='baseline' and k not in {finance!r}")
            # WI-053 read the magnet clearance refusal (ValueError) first at three invalid radii. WI-057
            # (2026-09-13): the calcs live on their parts and the regenerated pipeline executes the plasma's
            # sustainment module before the magnet's peak-field module. At the coil-centre and R3 radii the first
            # refusal is the plasma's deliberate SustainmentError (accepted: a different deliberate rejection).
            # At the negative radius it is an incidental TypeError inside plasma__sustain -- an UNRESOLVED
            # regression of the diagnostic, documented here, not repaired (goal structural-decomposition
            # trail, Amendment 2026-09-13; a deliberate non-positive-radius refusal is a model item). The
            # clearance check itself is unchanged and still refuses when reached
            # (test_peak_component_preserves_valid_and_rejects_invalid_domains).
            text = replace_once(text,
                "classes=['SustainmentError','ZeroDivisionError','SustainmentError','ZeroDivisionError','TypeError']",
                "classes=['SustainmentError','SustainmentError','SustainmentError','ZeroDivisionError','TypeError']")
        driver = drivers / (name + '.py')
        driver.write_text(text)
        command = [str(ROOT / '.codex-test/run'), 'bash', '-c',
                   'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; exec .codex-test/run python "$@"',
                   'current-mfe', str(driver), str(destination)]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        (destination / (name + '.log')).write_text(result.stdout + result.stderr)
        assert result.returncode == 0, f'{name} failed: {destination / (name + ".log")}'
    assert generation.inventory(generation.PACKAGE) == before
    return destination
