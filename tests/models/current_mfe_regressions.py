"""Current MFE completion and bounded adaptations of frozen regression drivers."""

import importlib.util
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_EVIDENCE = ROOT / 'work/completed/20260914_WI-038_conductor-grade-lever/evidence'
STRUCTURE_EVIDENCE = ROOT / 'work/active/WI-057_stellaris-structural-decomposition/evidence/merge_onto_demo_maturation'
P = 'stellarator_09__stellaris__'
MR7_EVIDENCE = ROOT / 'work/active/WI-075_supplied-magnet-design-evaluation/evidence'
ROUND2_EVIDENCE = ROOT / 'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence'


def compose_interface_deltas(earlier, later):
    """Compose reviewed sequential ABI changes without adopting generated membership."""
    result = {}
    for added, retired in (
        ('added_parameters', 'retired_parameters'),
        ('added_numeric_channels', 'retired_numeric_channels'),
        ('added_structured_channels', 'retired_structured_channels'),
        ('added_predicates', 'retired_predicates'),
    ):
        result[added] = sorted((set(earlier[added]) - set(later[retired])) | set(later[added]))
        result[retired] = sorted((set(earlier[retired]) - set(later[added])) | set(later[retired]))
        assert not set(result[added]) & set(result[retired])
    result['added_local_bindings'] = {
        key: value for key, value in earlier['added_local_bindings'].items()
        if key not in later['retired_local_names']
    } | later['added_local_bindings']
    result['retired_local_names'] = sorted(
        (set(earlier['retired_local_names']) - set(later['added_local_bindings']))
        | set(later['retired_local_names']))
    assert not set(result['added_local_bindings']) & set(result['retired_local_names'])
    return result


ROUND2_DELTA = json.loads((ROUND2_EVIDENCE / 'interface-delta.json').read_text())
MR7_DELTA = compose_interface_deltas(
    json.loads((MR7_EVIDENCE / 'interface-delta.json').read_text()), ROUND2_DELTA)
COST_DESCENDANTS = json.loads((ROOT / 'work/active/WI-079_supplied-equipment-design-bases-for-residual-costs/evidence/regression-descendants.json').read_text())
ROUND2_CHANGED_CHANNELS = frozenset(COST_DESCENDANTS['changed_existing_numeric_channels'])
ROUND2_CHANGED_LOCALS = frozenset(COST_DESCENDANTS['changed_existing_local_names'])
MR7_PARAMETERS = frozenset(MR7_DELTA['added_parameters'])
MR7_RETIRED_PARAMETERS = frozenset(MR7_DELTA['retired_parameters'])
MR7_CHANNELS = frozenset(MR7_DELTA['added_numeric_channels'])
MR7_RETIRED_CHANNELS = frozenset(MR7_DELTA['retired_numeric_channels'])
MR7_PREDICATES = frozenset(MR7_DELTA['added_predicates'])
MR7_LOCALS = frozenset(MR7_DELTA['added_local_bindings'])
MR7_RETIRED_LOCALS = frozenset(MR7_DELTA['retired_local_names'])
CYCLE_PARTITION_PATH = ROOT / '.project/active/aries-comparison-preparation/current-readiness/regression-evidence/cycle-migration/contract-delta.json'
CYCLE_PARTITION = json.loads(CYCLE_PARTITION_PATH.read_text())
WI073_PARAMETERS = set(CYCLE_PARTITION['added_parameters'])
WI073_CHANNELS = set(CYCLE_PARTITION['added_channels'])
WI073_PREDICATES = set(CYCLE_PARTITION['added_predicates'])
WI073_LOCALS = set(CYCLE_PARTITION['added_locals'])
WI073_REPLAY = CYCLE_PARTITION['historical_controls']
WI073_REPLAY_LOCAL = CYCLE_PARTITION['historical_local_controls']


def extend_cycle_fixture(part):
    """Explicit additive WI-073 membership; retain every pre-existing expectation."""
    result = dict(part)
    if 'added_channels' in result:
        result['added_channels'] = sorted(set(result['added_channels']) | WI073_CHANNELS)
    if 'added_local_names' in result:
        result['added_local_names'] = sorted(set(result['added_local_names']) | WI073_LOCALS)
    # Only documented procurement descendants leave exact historical comparison.
    # Inputs select a fixed package now; physical timing and all other channels stay exact.
    for unchanged_key, changed_key, affected in (
        ('unaffected_exact_channels', 'changed_current_equation_channels', ROUND2_CHANGED_CHANNELS),
        ('unaffected_exact_locals', 'changed_current_equation_locals', ROUND2_CHANGED_LOCALS),
    ):
        if unchanged_key in result:
            moved = set(result[unchanged_key]) & affected
            result[unchanged_key] = sorted(set(result[unchanged_key]) - moved)
            result[changed_key] = sorted(set(result[changed_key]) | moved)
    return result

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
MR7_RADIUS_CASING = 63000.0 * (12.7 / 14.0) ** 0.78  # Explicit optional legacy construction for frozen R14 replay.
K_COIL_RETIRED = 1.968503937007874  # the retired WI-036 k_coil (25.0 / 12.7), the float the old oracle carried
WI058_PARAMETERS = {P + 'magnet__coil__c_coil_ref'}
WI058_RETIRED = {P + 'magnet__coil__k_coil'}
RECEIPT_EVIDENCE = ROOT / 'work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/integration'
# WI-069 reviewed ABI: thirteen controls replace the held I_total input.
WI069_PARAMETERS = {P + 'fuel_cycle__' + name for name in (
    'held_inventory', 'inventory_enabled', 'm_D_kg', 'reserve_fraction',
    's_per_year', 'shutdown_duration', 'startup_extension', 'tau_blanket',
    'tau_buffer', 'tau_extract', 'tau_feed', 'tau_process', 'tau_reserve')}
WI069_RETIRED = {P + 'fuel_cycle__I_total'}
WI068_PARAMETERS = {P + 'buildings__' + name for name in ('facilities_enabled', 'facilities_cost_mode', 'facilities_capacity_mode', 'sector_count', 'sector_bays', 'sector_service_teams', 'exterior_allowance', 'sector_route_clearance', 'sector_headroom', 'component_width', 'component_height', 'component_length', 'component_handling_margin', 'component_material_fraction', 'divertor_packages_per_sector', 'waste_package_yield', 'component_remove_days', 'component_install_days', 'sector_clean_days', 'sector_test_days', 'sector_split_days', 'sector_join_days', 'sector_transport_days', 'cooldown_days', 'recommission_days', 'initial_receipt_lead_days', 'component_receipt_lead_days', 'component_prepare_days', 'component_process_days', 'component_hold_days', 'clean_positions', 'dirty_buffer_positions', 'dirty_store_positions', 'cooling_initial_receipt_lead_days', 'cooling_receipt_lead_days', 'cooling_hold_days', 'cooling_prepare_stations', 'cooling_machine_stations', 'cooling_bundle_stations', 'cooling_prepare_machine_days', 'cooling_prepare_bundle_days', 'cooling_machine_process_days', 'cooling_bundle_process_days', 'cooling_field_cycle_days', 'cooling_internal_move_days', 'cooling_clean_helium_positions', 'cooling_clean_salt_positions', 'cooling_clean_bundle_positions', 'cooling_dirty_helium_positions', 'cooling_dirty_salt_positions', 'cooling_dirty_bundle_positions', 'helium_package_length', 'helium_package_width', 'helium_package_height', 'salt_package_length', 'salt_package_width', 'salt_package_height', 'hx_end_allowance', 'cooling_package_margin', 'cooling_aisle_width', 'cooling_cross_width', 'cooling_headroom', 'cooling_airlock_length', 'nuclear_wall', 'nuclear_floor', 'nuclear_roof', 'nuclear_rebar_density', 'conventional_wall', 'conventional_floor', 'conventional_roof', 'conventional_rebar_density', 'building_separation', 'external_access_width', 'provisional_envelope_scale', 'administration_occupants', 'control_occupants', 'security_occupants', 'administration_area_per_person', 'control_area_per_person', 'security_area_per_person', 'occupancy_circulation_factor', 'occupancy_height', 'occupancy_aspect_ratio', 'heat_rejection_length', 'heat_rejection_width', 'turbine_length', 'turbine_width', 'turbine_height', 'cryo_coldbox_length', 'cryo_coldbox_width', 'cryo_coldbox_height', 'cryo_compressors_length', 'cryo_compressors_width', 'cryo_compressors_height', 'fuel_length', 'fuel_width', 'fuel_height', 'reactor_aux_length', 'reactor_aux_width', 'reactor_aux_height', 'power_supply_length', 'power_supply_width', 'power_supply_height', 'onsite_ac_length', 'onsite_ac_width', 'onsite_ac_height', 'service_water_length', 'service_water_width', 'service_water_height', 'conventional_shop_length', 'conventional_shop_width', 'conventional_shop_height', 'site_services_length', 'site_services_width', 'site_services_height', 'sub_concrete_rate', 'sub_formwork_rate', 'sub_rebar_rate', 'super_concrete_rate', 'super_formwork_rate', 'super_rebar_rate', 'civil_cpi_ratio', 'civil_rate_multiplier', 'tonne_interpretation_kg', 'ventilation_coefficient', 'ventilation_exponent', 'ventilation_cpi_ratio', 'land_rate_per_acre', 'retained_site_improvements')}
WI068_REPLAY = WI073_REPLAY | {P + 'fuel_cycle__inventory_enabled': False, P + 'fuel_cycle__held_inventory': 0.0, P + 'fuel_cycle__processing_enabled': False, P + 'buildings__facilities_enabled': False, P + 'buildings__facilities_cost_mode': 0.}
WI068_REPLAY_LOCAL = WI073_REPLAY_LOCAL | dict(inventory_inventory_enabled=False, inventory_held_inventory=0., processing_enabled=False, facility_facilities_enabled=False, facility_facilities_cost_mode=0.)
WI067_PARAMETERS = {P + 'heat_transport__' + name for name in (
    'equipment_enabled', 'equipment_cost_mode', 'secondary_energy_mode',
    'equipment_layout_multiplier', 'equipment_tube_wall', 'equipment_shell_wall',
    'equipment_accessory_mass', 'equipment_secondary_head', 'equipment_eta_p',
    'equipment_eta_motor', 'equipment_machine_life', 'equipment_bundle_life',
    'equipment_makeup_fraction', 'equipment_inventory_reserve',
    'equipment_removal_multiplier', 'equipment_saltprice_source_choice', 'equipment_costscale')}
WI067_REPLAY = WI068_REPLAY | {P + 'heat_transport__equipment_enabled': False,
               P + 'heat_transport__equipment_cost_mode': 0.,
               P + 'heat_transport__secondary_energy_mode': 0.}
WI067_REPLAY_LOCAL = WI068_REPLAY_LOCAL | dict(cooling_enabled=False, cooling_cost_mode=0., cooling_energy_mode=0.)
WI066_RETIRED = {P + 'blanket__tbr'}
WI066_PREDICATE = P + 'tbr_ok__2cd198f674d413e4'
WI066_CHANGED = {P + 'fuel_cycle__fuel__tbr_margin'}
WI066_CHANNELS = {P + 'blanket__breeding__' + name for name in (
    'tbr_li6', 'tbr_li7', 'tbr_mean', 'tbr_std_error', 'interpolation_allowance',
    'tbr_lower', 'defined_flag')} | {P + 'breeding_adequacy__' + name for name in (
    'required_tbr', 'design_margin', 'fuel_margin', 'numerical_margin', 'production_rate',
    'extracted_supply_rate', 'extraction_loss_rate', 'recycle_loss_rate', 'decay_rate',
    'stock_growth_rate', 'balance_rate', 'defined_flag')}

WI065_PARAMETERS = {P + 'divertor__target_capture_fraction'}
WI065_CHANNELS = {P + 'divertor__divheat__' + name for name in (
    'p_rad_total', 'p_rad_edge', 'p_target_deposited', 'p_nonrad_uncaptured',
    'peak_equivalent_area', 'peak_equivalent_area_defined', 'f_rad_edge_defined',
    'power_account_valid')}
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
WI059_REPLAY = WI067_REPLAY | WI063_REPLAY | {
    P + 'cryoplant__inventory_enabled': False, P + 'magnet__m_support': 0.0,
    P + 'magnet__legacy_casing_fraction': 1.0, P + 'structure__residual_fraction': 1.0,
    P + 'cryoplant__joint_drive_fraction': 0.0, P + 'cryoplant__q_nuc_structure': 0.0}
WI059_REPLAY_LOCAL = WI067_REPLAY_LOCAL | WI063_REPLAY_LOCAL | dict(cryo_inventory_enabled=False, magnet_support_mass=0.0,
    magnet_legacy_casing_fraction=1.0, structure_residual_fraction=1.0,
    cryo_joint_drive_fraction=0.0, cryo_q_nuc_structure=0.0)


def wi059_replay(overrides):
    return oracle_local_overrides(WI059_REPLAY) | dict(overrides)


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
        ('baseline', {}), ('R14', {P + 'plasma__R': 14.0, P + 'magnet__coil__c_coil_ref': K_COIL_RETIRED * 14.0, P + 'magnet__casing__m_casing': MR7_RADIUS_CASING}))}  # WI-058: the R-form's length at R14
    assert changed.isdisjoint(WI040_CHANNELS)
    for name in oracle:
        assert changed | WI040_CHANNELS <= oracle[name].keys()
    frozen = json.loads((translated / 'frozen-results.json').read_text())
    direct = json.loads((translated / 'direct-entering.json').read_text())
    for name, ref in (('baseline', 'baseline'), ('R14', 'tied_R14')):
        replacement = {k: oracle[name][k] for k in (changed | WI040_CHANNELS | WI060_CHANNELS | WI061_CHANNELS | WI062_CHANNELS | WI063_CHANNELS | WI064_CHANNELS | WI065_CHANNELS) - MR7_RETIRED_CHANNELS}
        replacement.update({k:v for k,v in wi059_native_additions(frozen['cases'][ref]['native']['outputs'], oracle_entry.vs.IN).items() if k not in MR7_RETIRED_CHANNELS})
        frozen['cases'][ref]['native']['outputs'].update(replacement)
        direct['results'][name]['single']['outputs'].update(replacement)
    (translated / 'frozen-results.json').write_text(json.dumps(frozen, indent=2) + '\n')
    (translated / 'direct-entering.json').write_text(json.dumps(direct, indent=2) + '\n')
    expected = json.loads((translated / 'expectations.json').read_text())
    expected['channels'] = sorted((set(expected['channels']) | WI040_CHANNELS | LIVE_CONDUCTOR_CHANNELS | WI059_CHANNELS | WI061_CHANNELS | WI062_CHANNELS | WI063_CHANNELS | WI064_CHANNELS | WI065_CHANNELS) - MR7_RETIRED_CHANNELS)
    (translated / 'expectations.json').write_text(json.dumps(expected, indent=2) + '\n')
    return changed | WI040_CHANNELS | WI059_CHANNELS | WI060_CHANNELS | WI061_CHANNELS | WI062_CHANNELS | WI063_CHANNELS | WI064_CHANNELS | WI065_CHANNELS


def wi066_evaluation(channels):
    """Independent compound predicate; report margins are absent for compound roots."""
    observed = {'defined_in': channels[P + 'breeding_adequacy__defined_flag'],
                'numerical_margin_in': channels[P + 'breeding_adequacy__numerical_margin']}
    value = observed['defined_in'] >= 1.0 and observed['numerical_margin_in'] >= 0.0
    return dict(constraint_id=WI066_PREDICATE, actual_value=value,
                status='satisfied' if value else 'violated', margin=None, observed=observed)


def restate_wi066_breeding(translated):
    """Restate only new breeding outputs, fuel margin and its predicate in TEMP copies.

    R14 is outside the response domain: zero carrier outputs and a violated predicate
    are compared explicitly. Frozen archives and every other predicate stay unchanged.
    """
    import sys
    sys.path.insert(0, str(ROOT / 'exploration/stellarator_e2e/studies'))
    import oracle_entry
    frozen = json.loads((translated / 'frozen-results.json').read_text())
    direct = json.loads((translated / 'direct-entering.json').read_text())
    for name, ref, change in [('baseline', 'baseline', {}), ('R14', 'tied_R14', {
            P + 'plasma__R': 14.0, P + 'magnet__coil__c_coil_ref': K_COIL_RETIRED * 14.0, P + 'magnet__casing__m_casing': MR7_RADIUS_CASING})]:
        channels = oracle_entry.evaluate(WI059_REPLAY | change)
        replacement = {key: channels[key] for key in WI066_CHANNELS | WI066_CHANGED}
        evaluation = wi066_evaluation(channels)
        native = frozen['cases'][ref]['native']
        native['outputs'].update(replacement)
        native['responses'][WI066_PREDICATE] = evaluation['status']
        raw = direct['results'][name]['single']['outputs']
        raw.update(replacement)
        raw[WI066_PREDICATE + '__evaluation'] = evaluation
        for report in (native['report'], raw['constraint_report']):
            matches = [i for i, row in enumerate(report['results']) if row['constraint_id'] == WI066_PREDICATE]
            assert len(matches) == 1
            report['results'][matches[0]] = evaluation
            # The historical cases already contain unrelated violations; keep their headline.
            assert report['headline'] == 'violation'
    (translated / 'frozen-results.json').write_text(json.dumps(frozen, indent=2) + '\n')
    (translated / 'direct-entering.json').write_text(json.dumps(direct, indent=2) + '\n')
    path = translated / 'expectations.json'
    expected = json.loads(path.read_text())
    expected['channels'] = sorted(set(expected['channels']) | WI066_CHANNELS)
    path.write_text(json.dumps(expected, indent=2) + '\n')
    return WI066_CHANNELS | WI066_CHANGED


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
    entering_parameters = json.loads(translate_names(
        (historical / 'entering-package/contracts/model_contract.json').read_text(), forward))['parameters']
    # A parameter's group is part of its identity. Round 2 retires library-default
    # price coefficients as well as instance literals; use the original declared
    # group for each explicitly ledgered retirement, never a guessed plant group.
    retired_identities = [[entry['param_group'], entry['qualified_name']]
                          for entry in entering_parameters
                          if entry['qualified_name'] in ALL_RETIRED_PARAMETERS]
    expectations['contract_delta']['remove'] = sorted(
        expectations['contract_delta']['remove'] + retired_identities)
    # MR-7 explicitly retires derived selection outputs. Only temporary replay
    # copies project them out; every surviving frozen physical value is retained.
    expectations['channels'] = sorted(set(expectations['channels']) - MR7_RETIRED_CHANNELS)
    expectations['ratios'] = {k:v for k,v in expectations['ratios'].items() if P+k not in MR7_RETIRED_CHANNELS}
    expectations['anchors'] = [k for k in expectations['anchors'] if P+k not in MR7_RETIRED_PARAMETERS]
    for filename in ('frozen-results.json', 'direct-entering.json'):
        path = out / filename
        doc = json.loads(path.read_text())
        def project(value):
            if isinstance(value, dict):
                return {k:project(v) for k,v in value.items() if k not in MR7_RETIRED_CHANNELS}
            if isinstance(value, list):
                return [project(v) for v in value]
            return value
        path.write_text(json.dumps(project(doc), indent=2)+'\n')
    # Refuse a translation the live package cannot honour: every surviving name must resolve.
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
    # The current WI-080 wrapper owns the seed receipt; historical tools also use inventory().
    module.inventory = module.recipe().inventory
    module.SEEDS = RECEIPT_EVIDENCE / "candidate-seeds.json"
    return module


def operating_acceptance(destination, historical):
    # Keep all historical scenario execution and assertions. Replace its generator
    # dependency with the current reviewed WI-067 completion inventory.
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
    """Project ten explicit added checks out of historical eighteen-check comparisons."""
    import copy
    result = copy.deepcopy(report)
    excluded = {WI061_PREDICATE, WI062_PREDICATE} | FACILITY_PREDICATES | WI073_PREDICATES | MR7_PREDICATES
    assert {r['constraint_id'] for r in result['results']} == CURRENT_PREDICATES
    added = [r for r in result['results'] if r['constraint_id'] in excluded]
    assert len(added) == len(excluded)
    assert result['assessed_entry_count'] == reference['assessed_entry_count'] + len(excluded)
    result['results'] = [r for r in result['results'] if r['constraint_id'] not in excluded]
    result['assessed_entry_count'] -= len(excluded)
    for key in ('authored_usage_total', 'applicable_gate_total', 'assessed_gate_count'):
        assert result['coverage'][key] == reference['coverage'][key] + len(excluded)
        result['coverage'][key] -= len(excluded)
    # Catalog identity necessarily differs when its ten added entries are projected out.
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
    finance |= restate_wi066_breeding(translated)
    finance |= restate_current_radius_additions(translated)
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
                                f"{{x[1] for x in delta['added']}}=={ALL_ADDED_PARAMETERS!r}")
            # WI-058: evaluate R14 at the R-form's length (see K_COIL_RETIRED) so the frozen row stays exact.
            text = replace_once(text, "('R14',{P+'plasma__R':14.0})",
                                f"('R14',{{P+'plasma__R':14.0,P+'magnet__coil__c_coil_ref':{K_COIL_RETIRED * 14.0!r},P+'magnet__casing__m_casing':{MR7_RADIUS_CASING!r}}})")
        if name in ('native', 'direct'):
            text = 'from tests.models.current_mfe_regressions import pre_fit_report, WI061_PREDICATE, WI062_PREDICATE, FACILITY_PREDICATES, WI073_PREDICATES, MR7_PREDICATES, patch_historical_input_files\n' + text
        if name == 'native':
            text = replace_once(text, "assert a['responses']==b['responses']", "assert {k:v for k,v in a['responses'].items() if k not in ({WI061_PREDICATE, WI062_PREDICATE} | FACILITY_PREDICATES | WI073_PREDICATES | MR7_PREDICATES)}==b['responses']")
            text = text.replace("a['report']==b['report']", "pre_fit_report(a['report'], b['report'])==b['report']")
        if name == 'direct':
            text = replace_once(text, "assert set(raw)==set(expected)", "assert set(raw)-{cid+'__evaluation' for cid in ({WI061_PREDICATE, WI062_PREDICATE} | FACILITY_PREDICATES | WI073_PREDICATES | MR7_PREDICATES)}==set(expected)\n        raw['constraint_report'] = pre_fit_report(raw['constraint_report'], expected['constraint_report'])")
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
            text = replace_once(text, "f=scratch/'inputs/stellarator_plant_params.json'; values=json.loads(f.read_text()); values.update(change); f.write_text(json.dumps(values))", f"patch_historical_input_files(scratch/'inputs', {WI059_REPLAY!r} | change)")
            # WI-058: evaluate R14 at the R-form's length (see K_COIL_RETIRED) so the frozen row stays exact.
            text = replace_once(text, "'R14':{P+'plasma__R':14.0,",
                                f"'R14':{{P+'plasma__R':14.0,P+'magnet__coil__c_coil_ref':{K_COIL_RETIRED * 14.0!r},P+'magnet__casing__m_casing':{MR7_RADIUS_CASING!r},")
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
        if name == 'cli_checks':
            text = replace_once(text, "    assert r.returncode==(1 if args else 0)", f"""    if not args:
        assert r.returncode == 1
        assert 'assessed_entry_count {34 + len(ROUND2_DELTA['added_predicates']) - len(ROUND2_DELTA['retired_predicates'])} != 20' in r.stderr
        assert r.stdout.count('*** DEVIATION') == 8
        for anchor in ('total capital $', 'LCOE $/MWh', 'p_net MW', 'q_eng', 'rec_frac', 'magnet %', 'CAS70 $/yr', 'CAS80 $/yr', 'lcoe_1cfe $/MWh (comparison)'):
            assert anchor in r.stdout, anchor
        rows[-1]['compatibility'] = 'unsupported historical nine-anchor/twenty-predicate calibration'
    else:
        assert r.returncode == 1""")
            text = replace_once(text, "print('PASS actual CLI baseline and exact old-key alone/equal/conflicting/zero refusal')", "print('KNOWN INCOMPATIBILITY historical CLI baseline; PASS actual CLI old-key alone/equal/conflicting/zero refusal')")
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

# WI-070 reviewed additions; source rows remain public instance parameters.
WI070_PARAMETERS = {P + "fuel_cycle__processing_" + key for key in ['enabled', 'source_conditions', 'capacity_margin', 'price_multiplier', 'reference_flow', 'exponent', 'target_cpi', 'transfer_cpi', 'transfer_capital', 'transfer_installation', 'cleanup_cpi', 'cleanup_capital', 'cleanup_installation', 'distiller_cpi', 'distiller_capital', 'distiller_installation', 'containment_cpi', 'containment_capital', 'containment_installation']}
WI070_CHANNELS = {P + "fuel_cycle__processing_cost__" + key for key in ['flow_kg_s', 'capacity_kg_s', 'plant_capacity_kg_s', 'flow_ratio', 'scaling_factor', 'transfer_reference_capital', 'transfer_reference_installation', 'transfer_capital', 'transfer_installation', 'cleanup_reference_capital', 'cleanup_reference_installation', 'cleanup_capital', 'cleanup_installation', 'distiller_reference_capital', 'distiller_reference_installation', 'distiller_capital', 'distiller_installation', 'containment_reference_capital', 'containment_reference_installation', 'containment_capital', 'containment_installation', 'equipment_total', 'installation_total', 'module_total', 'new_total', 'cost', 'defined_flag']} | {P + "shipping_scope__fuel_installation_exclusion"}

# WI-071 one shared source-rate entry; no added output producer.
WI071_PARAMETERS = {P + 'heat_transport__equipment_stainless_fabrication_usd2017_per_kg'}


# Reviewed 2026-09-19 exact partitions: names/provenance only, never output snapshots.
PARTITION_PATH = ROOT / '.project/active/aries-comparison-preparation/current-readiness/regression-evidence/partitions.json'
PARTITIONS = json.loads(PARTITION_PATH.read_text())
# The Round 1 fixture remains immutable; the reviewed additive ledger is applied in memory.
PARTITIONS['fixture_partitions'] = {k: extend_cycle_fixture(v) for k,v in PARTITIONS['fixture_partitions'].items()}
for key in ('current_numeric_channels', 'current_structured_channels', 'current_predicates'):
    PARTITIONS[key] = CYCLE_PARTITION[key]
CURRENT_NUMERIC = (frozenset(PARTITIONS['current_numeric_channels']) - MR7_RETIRED_CHANNELS) | MR7_CHANNELS
CURRENT_STRUCTURED = (frozenset(PARTITIONS['current_structured_channels']) - set(MR7_DELTA['retired_structured_channels'])) | set(MR7_DELTA['added_structured_channels'])
CURRENT_PREDICATES = (frozenset(PARTITIONS['current_predicates']) - set(MR7_DELTA['retired_predicates'])) | MR7_PREDICATES
FACILITY_PREDICATES = frozenset(PARTITIONS['added_predicates']['WI-068'])
# Retired mode zero was dormant in this historical replay; no selection is replayed.
POST_WI065_REPLAY = {k:v for k,v in (PARTITIONS['post_WI065_historical_controls'] | WI073_REPLAY).items() if k != P+'buildings__facilities_capacity_mode'}
CURRENT_ADDITIONS = WI073_CHANNELS | set().union(*(set(PARTITIONS['groups'][name]['channels']) for name in ('WI-066','WI-067','WI-068','WI-069','WI-070')))


def historical_point(changes=None):
    return POST_WI065_REPLAY | dict(changes or {})


def oracle_local_overrides(point):
    import sys
    for directory in (ROOT / "exploration/stellarator_e2e", ROOT / "exploration/stellarator_e2e/studies"):
        if str(directory) not in sys.path:
            sys.path.insert(0, str(directory))
    import oracle_entry
    return oracle_entry._oracle_overrides(point)


def assert_current_predicates(row, point, expected=None):
    """All current predicates use exact operators on current independent/native operands."""
    import oracle_entry
    import study_route
    from scripts.study.verify import derive_verdict, package_input_values
    params = package_input_values(study_route.PACKAGE_DIR)
    catalog = study_route._catalog_by_constraint_id(study_route.PACKAGE_DIR)
    assert set(catalog) == CURRENT_PREDICATES
    if expected is None:
        expected = oracle_entry.evaluate(point)
    bindings = oracle_entry.operand_bindings()
    for values in (row.outputs, expected):
        verdicts = {cid: 'satisfied' if derive_verdict(cid, entry, bindings, point, params, values)[0] else 'violated'
                    for cid, entry in catalog.items()}
        actual = {cid: row.responses[cid] for cid in CURRENT_PREDICATES}
        assert verdicts == actual
    assert set(row.responses) == CURRENT_PREDICATES | {'headline'}
    assert row.responses['headline'] == ('satisfied' if all(v == 'satisfied' for v in actual.values()) else 'violated')


def assert_historical_native(name, row, old_outputs, old_responses, point):
    """Retain every unaffected native value; independently verify changed/new values."""
    import math
    import oracle_entry
    part = PARTITIONS['fixture_partitions'][name]
    retired = set(old_outputs) & MR7_RETIRED_CHANNELS
    unchanged = set(part['unaffected_exact_channels']) - retired
    changed = set(part['changed_current_equation_channels']) - retired
    added = (set(part['added_channels']) - MR7_RETIRED_CHANNELS) | MR7_CHANNELS
    assert not unchanged & changed
    assert set(old_outputs) == unchanged | changed | retired
    assert set(row.outputs) == CURRENT_NUMERIC == (set(old_outputs) - retired) | added
    for key in unchanged:
        assert row.outputs[key] == old_outputs[key], (name, key, row.outputs[key], old_outputs[key])
    expected = oracle_entry.evaluate(point)
    assert changed | added <= expected.keys()
    for key in expected:
        assert math.isclose(row.outputs[key], expected[key], rel_tol=1e-9, abs_tol=1e-9), (name,key,row.outputs[key],expected[key])
    for key, value in (old_responses or {}).items():
        if key != WI066_PREDICATE and key != 'headline':
            assert row.responses[key] == value, (name,key)
    assert_current_predicates(row, point)


# WI-072 exposes existing independent quantities without changing native outputs.
WI072_LOCALS = {'coverage_' + name for name in (
    'annual_total','cas70','cas71_crf','cas71_levelized','cas80_crf','cas80_levelized',
    'cooling_cost_mode','cooling_energy_mode','cooling_consumables','cooling_replacements',
    'cooling_shipping','coil_length','wp_side','cold_volume','blanket_volume','outer_radius',
    'coil_inner_radius','shield_volume','structure_volume','vessel_volume','wall_area','replacement_event')}
PROFILE_MAPPED = {P+'plasma__'+key for key in ('alpha_n','alpha_T','f_shape')}
ALL_ADDED_PARAMETERS = (WI038_PARAMETERS | WI040_PARAMETERS | WI058_PARAMETERS | WI059_PARAMETERS |
    WI059_NATIVE_ONLY_PARAMETERS | WI060_PARAMETERS | WI061_PARAMETERS | WI062_PARAMETERS |
    WI063_PARAMETERS | WI064_PARAMETERS | WI065_PARAMETERS | WI067_PARAMETERS | WI068_PARAMETERS |
    WI069_PARAMETERS | WI070_PARAMETERS | WI071_PARAMETERS | WI073_PARAMETERS)
ALL_ADDED_PARAMETERS = (ALL_ADDED_PARAMETERS - MR7_RETIRED_PARAMETERS) | MR7_PARAMETERS
ALL_RETIRED_PARAMETERS = WI058_RETIRED | WI066_RETIRED | WI069_RETIRED | MR7_RETIRED_PARAMETERS
_entering_contract = json.loads((STRUCTURE_EVIDENCE/'contract_before.json').read_text())
_forward, _ = structure_ledger()
CURRENT_PARAMETERS = ({_forward.get(x['qualified_name'], x['qualified_name']) for x in _entering_contract['parameters']}
                      - ALL_RETIRED_PARAMETERS) | ALL_ADDED_PARAMETERS


def assert_local_partition(name, actual, historical):
    """Exact local membership and unchanged values; alias/changed equations checked separately."""
    import math
    part = PARTITIONS['fixture_partitions'][name]
    changed=set(part['changed_current_equation_locals']); unchanged=set(part['unaffected_exact_locals'])
    assert set(historical) == changed | unchanged
    assert set(actual) == ((set(historical) - {'conductor_cost_per_kAm_effective'}) | set(part['added_local_names']) | WI072_LOCALS | WI073_LOCALS | MR7_LOCALS) - MR7_RETIRED_LOCALS
    changed -= MR7_RETIRED_LOCALS
    unchanged -= MR7_RETIRED_LOCALS
    for key in unchanged:
        if name == 'coil-thermal-local-0':
            import pytest
            assert actual[key] == pytest.approx(historical[key],rel=1e-12,abs=1e-12), (name,key,actual[key],historical[key])
        else:
            assert actual[key] == historical[key], (name,key,actual[key],historical[key])
    for alias, canonical in PARTITIONS['local_alias_equalities'].items():
        assert actual[alias] == actual[canonical]
    return changed


def restate_current_radius_additions(translated):
    """Only reviewed changed/new names receive independent current expectations."""
    import oracle_entry
    frozen=json.loads((translated/'frozen-results.json').read_text())
    direct=json.loads((translated/'direct-entering.json').read_text())
    replaced=set()
    for name,ref,change in [('baseline','baseline',{}),('R14','tied_R14',{P+'plasma__R':14.,P+'magnet__coil__c_coil_ref':K_COIL_RETIRED*14., P+'magnet__casing__m_casing':MR7_RADIUS_CASING})]:
        part=PARTITIONS['fixture_partitions']['radius-'+ref]
        keys=(set(part['added_channels']) | set(part['changed_current_equation_channels']) | MR7_CHANNELS) - MR7_RETIRED_CHANNELS
        independent=oracle_entry.evaluate(WI059_REPLAY | change)
        assert keys <= independent.keys()
        replacements={key:independent[key] for key in keys}
        frozen['cases'][ref]['native']['outputs'].update(replacements)
        direct['results'][name]['single']['outputs'].update(replacements)
        replaced |= keys
    (translated/'frozen-results.json').write_text(json.dumps(frozen,indent=2)+'\n')
    (translated/'direct-entering.json').write_text(json.dumps(direct,indent=2)+'\n')
    path=translated/'expectations.json'; expected=json.loads(path.read_text())
    assert set(expected['channels']) | replaced == CURRENT_NUMERIC
    expected['channels']=sorted(CURRENT_NUMERIC)
    path.write_text(json.dumps(expected,indent=2)+'\n')
    return replaced

# WI-066 geometry/breeding and existing finance inputs newly admitted by the oracle.
LATER_MAPPED_EXISTING = {P+key:local for key,local in {
    'blanket__blanket_t':'blanket_t', 'blanket__first_wall__firstwall_t':'firstwall_t',
    'blanket__first_wall__fluence_limit':'fluence_limit', 'blanket__first_wall__vacuum_t':'vacuum_t',
    'blanket__reflector_t':'reflector_t', 'contingency_rate':'contingency_rate',
    'plasma__kappa':'kappa', 'shield__ht_shield_t':'ht_shield_t', 'structure__structure_t':'structure_t',
    'tbr_floor':'tbr_floor', 'vessel__gap1_t':'gap1_t', 'vessel__vessel_t':'vessel_t',
}.items()}


def patch_historical_input_files(directory, changes):
    """Temporary replay copies: resolve each override's actual declared group."""
    files={p:json.loads(p.read_text()) for p in Path(directory).glob('*.json')}
    for key,value in changes.items():
        owners=[path for path,data in files.items() if key in data]
        if not owners:
            # Historical retired-key probes deliberately exercise schema refusal.
            owners=[Path(directory)/'stellarator_plant_params.json']
        assert len(owners)==1,(key,owners)
        files[owners[0]][key]=value
    for path,data in files.items():
        path.write_text(json.dumps(data)+'\n')

# Additional consumer partitions independently reviewed after the complete scope run.
ADDITIONAL_DOMAIN = {k: extend_cycle_fixture(v) for k,v in json.loads((PARTITION_PATH.parent / 'additional-domain-partitions.json').read_text())['fixture_partitions'].items()}
ADDITIONAL_MAPPING = json.loads((PARTITION_PATH.parent / 'additional-domain-mapping-ledger.json').read_text())
ADDITIONAL_MAPPING['mapped_input_keys'] = sorted(set(ADDITIONAL_MAPPING['mapped_input_keys']) | WI073_PARAMETERS)
ADDITIONAL_MAPPING['added_input_keys'] = sorted(set(ADDITIONAL_MAPPING['added_input_keys']) | WI073_PARAMETERS)
ADDITIONAL_MAPPING['unchanged_input_bindings'].update(CYCLE_PARTITION['added_input_bindings'])
ADDITIONAL_MAPPING['added_output_bindings'].update(CYCLE_PARTITION['added_locals'])
ADDITIONAL_MAPPING['mapped_numeric_channels'] = sorted(CURRENT_NUMERIC)
ADDITIONAL_MAPPING['numeric_channel_count'] = len(CURRENT_NUMERIC)
FINANCE_DEPENDENCIES = json.loads((PARTITION_PATH.parent / 'additional-financial-dependencies.json').read_text())
FINANCE_DEPENDENCIES['unchanged_channels'] = sorted(set(FINANCE_DEPENDENCIES['unchanged_channels']) | set(CYCLE_PARTITION['new_rate_invariant_channels']))
LEGACY_COOLING_FACILITIES = WI073_REPLAY | {P + key: value for key, value in {
    'heat_transport__equipment_enabled': False, 'heat_transport__equipment_cost_mode': 0.0,
    'heat_transport__secondary_energy_mode': 0.0, 'buildings__facilities_enabled': False,
    'buildings__facilities_cost_mode': 0.0}.items()}
