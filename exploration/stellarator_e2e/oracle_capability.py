"""Independent WI-080 offered equipment arithmetic, without production imports.

Static interface metadata transcribed from WI-080/evidence/capability-contract.json.
Defaults are assumed offers captured at 53a0366a, not observed capacities.
Expected demands must come from the independent verify_stellaris calculation.
"""
import math

PUBLIC_DEFAULTS = {'heat_transport__rated_helium_suction_K': ('capability_heat_transport__rated_helium_suction_K',
                                            561.9353658449644),
 'heat_transport__rated_helium_suction_Pa': ('capability_heat_transport__rated_helium_suction_Pa',
                                             7699680.103536234),
 'heat_transport__rated_helium_discharge_Pa': ('capability_heat_transport__rated_helium_discharge_Pa',
                                               8000000.0),
 'heat_transport__rated_helium_hot_K': ('capability_heat_transport__rated_helium_hot_K', 773.15),
 'heat_transport__rated_helium_cp': ('capability_heat_transport__rated_helium_cp', 5193.0),
 'heat_transport__rated_helium_gamma': ('capability_heat_transport__rated_helium_gamma', 1.6666666666666667),
 'heat_transport__rated_salt_hot_C': ('capability_heat_transport__rated_salt_hot_C', 465.0),
 'heat_transport__rated_salt_return_C': ('capability_heat_transport__rated_salt_return_C', 269.6647299145299),
 'heat_transport__rated_salt_cp': ('capability_heat_transport__rated_salt_cp', 1.56),
 'turbine__rated_steam_main_pressure_MPa': ('capability_turbine__rated_steam_main_pressure_MPa', 6.2),
 'turbine__rated_steam_extraction_pressure_MPa': ('capability_turbine__rated_steam_extraction_pressure_MPa',
                                                  0.8),
 'turbine__rated_steam_steam_C': ('capability_turbine__rated_steam_steam_C', 445.0),
 'turbine__rated_steam_reheat_C': ('capability_turbine__rated_steam_reheat_C', 445.0),
 'turbine__rated_steam_condenser_C': ('capability_turbine__rated_steam_condenser_C', 42.0),
 'turbine__rated_steam_salt_hot_C': ('capability_turbine__rated_steam_salt_hot_C', 465.0),
 'turbine__rated_steam_salt_return_C': ('capability_turbine__rated_steam_salt_return_C', 269.6647299145299),
 'turbine__rated_steam_salt_cp': ('capability_turbine__rated_steam_salt_cp', 1.56),
 'heat_rejection__rated_water_inlet_C': ('capability_heat_rejection__rated_water_inlet_C', 25.0),
 'heat_rejection__rated_water_outlet_C': ('capability_heat_rejection__rated_water_outlet_C', 35.0),
 'heat_rejection__rated_water_condenser_C': ('capability_heat_rejection__rated_water_condenser_C', 42.0),
 'cryoplant__rated_cryogenic_cold_K': ('capability_cryoplant__rated_cryogenic_cold_K', 20.0),
 'cryoplant__rated_cryogenic_intercept_K': ('capability_cryoplant__rated_cryogenic_intercept_K', 77.0),
 'cryoplant__rated_cryogenic_ambient_K': ('capability_cryoplant__rated_cryogenic_ambient_K', 300.0),
 'heat_transport__helium_rated_dp_Pa': ('capability_heat_transport__helium_rated_dp_Pa', 300319.8964637657),
 'heat_transport__helium_rated_electric_MW': ('capability_heat_transport__helium_rated_electric_MW',
                                              6.26003337158886),
 'turbine__selected_gross_MWe': ('capability_turbine__selected_gross_MWe', 1219.9981701764736),
 'turbine__hp_turbine__rated_flow_kg_s': ('capability_turbine__hp_turbine__rated_flow_kg_s',
                                          1108.5733942490049),
 'turbine__hp_turbine__rated_shaft_MW': ('capability_turbine__hp_turbine__rated_shaft_MW', 507.1088862154872),
 'turbine__lp_turbine__rated_flow_kg_s': ('capability_turbine__lp_turbine__rated_flow_kg_s',
                                          881.3051322292799),
 'turbine__lp_turbine__rated_shaft_MW': ('capability_turbine__lp_turbine__rated_shaft_MW', 750.3619138014925),
 'turbine__main_steam_generator__installed_UA_MW_K': ('capability_turbine__main_steam_generator__installed_UA_MW_K',
                                                      41.07437838721364),
 'turbine__reheater__installed_UA_MW_K': ('capability_turbine__reheater__installed_UA_MW_K',
                                          11.18676341684029),
 'turbine__condenser__rated_rejection_MW': ('capability_turbine__condenser__rated_rejection_MW',
                                            2058.639911447174),
 'turbine__condensate_pump__rated_flow_kg_s': ('capability_turbine__condensate_pump__rated_flow_kg_s',
                                               881.3051322292799),
 'turbine__condensate_pump__rated_dp_MPa': ('capability_turbine__condensate_pump__rated_dp_MPa',
                                            0.7917904366),
 'turbine__condensate_pump__rated_electric_MW': ('capability_turbine__condensate_pump__rated_electric_MW',
                                                 0.9261383157389033),
 'turbine__feedwater_pump__rated_flow_kg_s': ('capability_turbine__feedwater_pump__rated_flow_kg_s',
                                              1108.5733942490049),
 'turbine__feedwater_pump__rated_dp_MPa': ('capability_turbine__feedwater_pump__rated_dp_MPa', 5.4),
 'turbine__feedwater_pump__rated_electric_MW': ('capability_turbine__feedwater_pump__rated_electric_MW',
                                                8.780822331904837),
 'heat_rejection__rated_rejection_MW': ('capability_heat_rejection__rated_rejection_MW', 2109.621069383624),
 'heat_rejection__rated_water_flow_kg_s': ('capability_heat_rejection__rated_water_flow_kg_s',
                                           50463.801850311946),
 'heat_rejection__rated_water_head_m': ('capability_heat_rejection__rated_water_head_m', 20.0),
 'heat_rejection__rated_water_electric_MW': ('capability_heat_rejection__rated_water_electric_MW',
                                             13.023180063562146),
 'cryoplant__rated_cold_W': ('capability_cryoplant__rated_cold_W', 21933.902368719853),
 'cryoplant__rated_intercept_W': ('capability_cryoplant__rated_intercept_W', 41599.953939961626),
 'cryoplant__rated_direct_electric_MW': ('capability_cryoplant__rated_direct_electric_MW', 0.0),
 'electric_plant__installed_gross_rating_MWe': ('selected_electric_plant_installed_gross_rating_MWe',
                                                1219.9981701764736),
 'power_supplies__rated_tf_MWe': ('capability_power_supplies__rated_tf_MWe', 0.050267327222555655),
 'power_supplies__rated_pf_MWe': ('capability_power_supplies__rated_pf_MWe', 0.0)}

STATES = {'helium': ('heat_transport',
            'helium_offered_conditions',
            'p:cooling_enabled',
            [('r:loop_T_comp_in', 'capability_heat_transport__rated_helium_suction_K'),
             ('r:cooling_circulator_suction_Pa', 'capability_heat_transport__rated_helium_suction_Pa'),
             ('p:loop_p', 'capability_heat_transport__rated_helium_discharge_Pa'),
             ('r:loop_T_out', 'capability_heat_transport__rated_helium_hot_K'),
             ('p:loop_cp', 'capability_heat_transport__rated_helium_cp'),
             ('p:loop_gamma', 'capability_heat_transport__rated_helium_gamma')]),
 'salt': ('heat_transport',
          'salt_offered_conditions',
          'p:cooling_enabled',
          [('p:matched_salt_hot_C', 'capability_heat_transport__rated_salt_hot_C'),
           ('r:cooling_salt_return_C', 'capability_heat_transport__rated_salt_return_C'),
           ('p:matched_salt_cp_kJ_kgK', 'capability_heat_transport__rated_salt_cp')]),
 'steam': ('turbine',
           'steam_offered_conditions',
           'r:matched_active',
           [('p:matched_main_pressure_MPa', 'capability_turbine__rated_steam_main_pressure_MPa'),
            ('p:matched_extraction_pressure_MPa', 'capability_turbine__rated_steam_extraction_pressure_MPa'),
            ('p:matched_steam_temperature_C', 'capability_turbine__rated_steam_steam_C'),
            ('p:matched_reheat_temperature_C', 'capability_turbine__rated_steam_reheat_C'),
            ('p:matched_condenser_temperature_C', 'capability_turbine__rated_steam_condenser_C'),
            ('p:matched_salt_hot_C', 'capability_turbine__rated_steam_salt_hot_C'),
            ('r:cooling_salt_return_C', 'capability_turbine__rated_steam_salt_return_C'),
            ('p:matched_salt_cp_kJ_kgK', 'capability_turbine__rated_steam_salt_cp')]),
 'water': ('heat_rejection',
           'water_offered_conditions',
           'r:cw_active',
           [('p:cw_water_inlet_C', 'capability_heat_rejection__rated_water_inlet_C'),
            ('p:cw_water_outlet_C', 'capability_heat_rejection__rated_water_outlet_C'),
            ('r:matched_t_condensate_C', 'capability_heat_rejection__rated_water_condenser_C')]),
 'cryogenic': ('cryoplant',
               'cryogenic_offered_conditions',
               None,
               [('p:T_cold_cryo', 'capability_cryoplant__rated_cryogenic_cold_K'),
                ('p:T_shield_cryo', 'capability_cryoplant__rated_cryogenic_intercept_K'),
                ('p:T_amb_cryo', 'capability_cryoplant__rated_cryogenic_ambient_K')])}

SCREENS = {'helium_flow': ('heat_transport', 'helium', 'p:mdot_loop_rated', 'r:loop_mdot_loop', None),
 'helium_pumping': ('heat_transport',
                    'helium',
                    'p:cooling_helium_design_shaft_MW',
                    'r:cooling_circulator_shaft_MW',
                    None),
 'helium_pressure_rise': ('heat_transport',
                          'helium',
                          'p:capability_heat_transport__helium_rated_dp_Pa',
                          'r:loop_dp_loop',
                          None),
 'helium_electric': ('heat_transport',
                     'helium',
                     'p:capability_heat_transport__helium_rated_electric_MW',
                     'r:cooling_circulator_electric_MW',
                     None),
 'salt_flow': ('heat_transport', 'salt', 'p:cooling_salt_design_flow_kg_s', 'r:cooling_salt_pump_flow', None),
 'salt_head': ('heat_transport', 'salt', 'p:cooling_salt_design_head_m', 'p:cooling_secondary_head', None),
 'salt_shaft': ('heat_transport',
                'salt',
                'r:cooling_salt_design_shaft_MW',
                'r:cooling_salt_pump_shaft_MW',
                None),
 'salt_electric': ('heat_transport', 'salt', 'r:cooling_salt_design_electric_MW', 'x:salt_electric', None),
 'turbine_gross': ('turbine', None, 'p:capability_turbine__selected_gross_MWe', 'r:p_the', None),
 'hp_flow': ('turbine',
             'steam',
             'p:capability_turbine__hp_turbine__rated_flow_kg_s',
             'r:matched_mdot_main_kg_s',
             None),
 'hp_shaft': ('turbine',
              'steam',
              'p:capability_turbine__hp_turbine__rated_shaft_MW',
              'r:matched_p_hp_shaft_MW',
              None),
 'lp_flow': ('turbine',
             'steam',
             'p:capability_turbine__lp_turbine__rated_flow_kg_s',
             'r:matched_mdot_reheat_kg_s',
             None),
 'lp_shaft': ('turbine',
              'steam',
              'p:capability_turbine__lp_turbine__rated_shaft_MW',
              'r:matched_p_lp_shaft_MW',
              None),
 'main_UA': ('turbine',
             'steam',
             'p:capability_turbine__main_steam_generator__installed_UA_MW_K',
             'r:matched_main_UA_MW_K',
             'r:matched_main_UA_available'),
 'reheat_UA': ('turbine',
               'steam',
               'p:capability_turbine__reheater__installed_UA_MW_K',
               'r:matched_reheat_UA_MW_K',
               'r:matched_reheat_UA_available'),
 'condenser_rejection': ('turbine',
                         'steam',
                         'p:capability_turbine__condenser__rated_rejection_MW',
                         'r:matched_q_condenser_MW',
                         None),
 'condensate_flow': ('turbine',
                     'steam',
                     'p:capability_turbine__condensate_pump__rated_flow_kg_s',
                     'r:matched_mdot_condensate_kg_s',
                     None),
 'condensate_pressure_rise': ('turbine',
                              'steam',
                              'p:capability_turbine__condensate_pump__rated_dp_MPa',
                              'x:condensate_dp',
                              None),
 'condensate_electric': ('turbine',
                         'steam',
                         'p:capability_turbine__condensate_pump__rated_electric_MW',
                         'r:matched_p_condensate_electric_MW',
                         None),
 'feedwater_flow': ('turbine',
                    'steam',
                    'p:capability_turbine__feedwater_pump__rated_flow_kg_s',
                    'r:matched_mdot_heater_kg_s',
                    None),
 'feedwater_pressure_rise': ('turbine',
                             'steam',
                             'p:capability_turbine__feedwater_pump__rated_dp_MPa',
                             'x:feedwater_dp',
                             None),
 'feedwater_electric': ('turbine',
                        'steam',
                        'p:capability_turbine__feedwater_pump__rated_electric_MW',
                        'r:matched_p_feedwater_electric_MW',
                        None),
 'water_rejection': ('heat_rejection',
                     'water',
                     'p:capability_heat_rejection__rated_rejection_MW',
                     'r:cw_q_total_rejection_MW',
                     None),
 'water_flow': ('heat_rejection',
                'water',
                'p:capability_heat_rejection__rated_water_flow_kg_s',
                'r:cw_water_flow_kg_s',
                None),
 'water_head': ('heat_rejection',
                'water',
                'p:capability_heat_rejection__rated_water_head_m',
                'p:cw_head_m',
                None),
 'water_electric': ('heat_rejection',
                    'water',
                    'p:capability_heat_rejection__rated_water_electric_MW',
                    'r:cw_p_cooling_pump_electric_MW',
                    None),
 'cold_stage': ('cryoplant', 'cryogenic', 'p:capability_cryoplant__rated_cold_W', 'x:cold_W', None),
 'intercept_stage': ('cryoplant',
                     'cryogenic',
                     'p:capability_cryoplant__rated_intercept_W',
                     'r:thermal_q_shield',
                     'p:cryo_inventory_enabled'),
 'direct_electric': ('cryoplant',
                     None,
                     'p:capability_cryoplant__rated_direct_electric_MW',
                     'p:p_cryo_direct',
                     None),
 'electric_gross': ('electric_plant',
                    None,
                    'p:selected_electric_plant_installed_gross_rating_MWe',
                    'r:p_et',
                    None),
 'magnet_tf_electric': ('power_supplies',
                        None,
                        'p:capability_power_supplies__rated_tf_MWe',
                        'r:p_tf_total',
                        None),
 'magnet_pf_electric': ('power_supplies', None, 'p:capability_power_supplies__rated_pf_MWe', 'p:p_pf', None)}

DEFAULTS = {key: value for key, value in PUBLIC_DEFAULTS.values()}
# Generated literal Boolean inputs can only withhold capacity credit. They are
# administrative masks, separate from the 49 supplied physical offer fields.
FLAG_DEFAULTS = {}
for name, (owner, group, rating, demand, available) in SCREENS.items():
    fields = (['applicable_in', 'conditions_supported_in'] if group is None else [])
    if available is None:
        fields.append('demand_available_in')
    for field in fields:
        suffix = f'{owner}__{name}_capability__{field}'
        FLAG_DEFAULTS[suffix] = ('capability_flag_' + suffix, True)
CRYO_ENABLED_SUFFIX = 'cryoplant__cryogenic_offered_conditions__enabled_in'
FLAG_DEFAULTS[CRYO_ENABLED_SUFFIX] = ('capability_flag_' + CRYO_ENABLED_SUFFIX, True)
DEFAULTS.update({key: value for key, value in FLAG_DEFAULTS.values()})
PREFIX = 'stellarator_09__stellaris__'
OUTPUT_MAP = {}
for name, (owner, group, rating, demand, available) in SCREENS.items():
    for field in ('margin', 'defined'):
        native_field = 'evaluation_defined' if field == 'defined' else field
        OUTPUT_MAP[f'capability_{name}_{field}'] = f'{PREFIX}{owner}__{name}_capability__{native_field}'
    for field in ('applicable', 'supported', 'capacity_ok'):
        OUTPUT_MAP[f'capability_{name}_{field}'] = f'{PREFIX}{owner}__{name}_capability__{field}'
for group, (owner, calc, enabled, pairs) in STATES.items():
    for field in ('applicable', 'supported', 'defined'):
        OUTPUT_MAP[f'capability_{group}_state_{field}'] = f'{PREFIX}{owner}__{calc}__{"evaluation_defined" if field == "defined" else field}'
CONVERSIONS = {
    'salt_electric': ('heat_transport', 'salt_electric_demand_conversion'),
    'condensate_dp': ('turbine', 'condensate_pressure_rise_demand_conversion'),
    'feedwater_dp': ('turbine', 'feedwater_pressure_rise_demand_conversion'),
    'cold_W': ('cryoplant', 'cold_load_W_demand_conversion'),
}
for name, (owner, calc) in CONVERSIONS.items():
    OUTPUT_MAP[f'capability_{name}_converted_demand'] = f'{PREFIX}{owner}__{calc}__demand'


def _boolean(value):
    if value not in (False, True, 0, 1):
        raise ValueError('capability flag must be Boolean')
    return bool(value)


def same_state(actual, rated):
    """Eight-ULP identity allowance for independent floating-point state paths."""
    if not math.isfinite(actual) or not math.isfinite(rated):
        raise ValueError('nonfinite offered state')
    return actual == rated or abs(actual - rated) <= 8 * max(math.ulp(actual), math.ulp(rated))


def screen(rating, demand, applicable=True, supported=True, available=True):
    """Strict capacity comparison; disabled equipment earns no adequacy credit."""
    applicable, supported, available = map(_boolean, (applicable, supported, available))
    if not math.isfinite(rating) or rating < 0:
        raise ValueError('supplied capability must be finite and nonnegative')
    if applicable and (not math.isfinite(demand) or demand < 0):
        raise ValueError('active capability demand must be finite and nonnegative')
    margin = rating - demand if applicable else 0.0
    if not math.isfinite(margin):
        raise ValueError('nonfinite capability margin')
    defined = applicable and supported and available
    return dict(margin=margin, defined=float(defined), applicable=applicable,
                supported=defined, capacity_ok=defined and margin >= 0)


def evaluate(parameters, independently_computed_results):
    """Return named scalars using independent demands and supplied offers only."""
    p, r = parameters, independently_computed_results
    salt_active = _boolean(p['cooling_enabled']) and _boolean(p['cooling_energy_mode'])
    flags = {suffix: _boolean(p[key]) for suffix, (key, _) in FLAG_DEFAULTS.items()}
    if salt_active and r['cooling_salt_pump_count'] <= 0:
        raise ValueError('active salt pump count must be positive')
    extras = {
        'salt_electric': (r['cooling_salt_electric_MW'] / r['cooling_salt_pump_count']
                          if salt_active else 0.0),
        'condensate_dp': (r['matched_p_condensate_pumped_MPa'] - r['matched_p_condensate_MPa']
                          if r['matched_active'] else 0.0),
        'feedwater_dp': (r['matched_p_feed_MPa'] - r['matched_p_heater_MPa']
                        if r['matched_active'] else 0.0),
        'cold_W': r['p_cold'] * 1e6,
    }
    def get(ref):
        if ref is None:
            return True
        scope, name = ref.split(':', 1)
        return {'p': p, 'r': r, 'x': extras}[scope][name]

    output, conditions = {}, {}
    for group, (owner, calc, enabled, pairs) in STATES.items():
        applicable = _boolean(get(enabled))
        if group == 'cryogenic':
            applicable = applicable and flags[CRYO_ENABLED_SUFFIX]
        if group in ('helium', 'salt'):
            mode = _boolean(p['loop_live' if group == 'helium' else 'cooling_energy_mode'])
            applicable = applicable and mode
        supported = False
        if applicable:
            values = [(get(actual), p[rated]) for actual, rated in pairs]
            if any(not math.isfinite(v) for pair in values for v in pair):
                raise ValueError('nonfinite offered state: ' + group)
            supported = all(same_state(actual, rated) for actual, rated in values)
        conditions[group] = applicable, supported
        for key, value in dict(applicable=applicable, supported=supported, defined=float(supported)).items():
            output[f'capability_{group}_state_{key}'] = value
    for name, (owner, group, rating, demand, available) in SCREENS.items():
        applicable, supported = conditions[group] if group else (True, True)
        prefix = f'{owner}__{name}_capability__'
        applicable = applicable and flags.get(prefix + 'applicable_in', True)
        supported = supported and flags.get(prefix + 'conditions_supported_in', True)
        available = get(available) and flags.get(prefix + 'demand_available_in', True)
        values = screen(get(rating), get(demand), applicable, supported, available)
        output.update({f'capability_{name}_{key}': value for key, value in values.items()})
    output.update({f'capability_{name}_converted_demand': value for name, value in extras.items()})
    return output
