"""WI-079 independently supplied procurement defaults and validation.

Defaults are the explicitly assumed offers captured once at 53a0366a; they are
not vendor quotations or runtime sizing. Equations remain in verify_stellaris.
"""
import math

PUBLIC_DEFAULTS = {'turbine__purchase_cost_per_module': ('selected_turbine_purchase_cost_per_module', 247464428.83859593),
 'heat_rejection__purchase_cost_per_module': ('selected_heat_rejection_purchase_cost_per_module',
                                              115939531.80564217),
 'power_supplies__purchase_cost_per_module': ('selected_power_supplies_purchase_cost_per_module',
                                              86013482.74180616),
 'divertor__purchase_cost_per_module': ('selected_divertor_purchase_cost_per_module',
                                        109109123.15593052),
 'cryoplant__purchase_cost_per_module': ('selected_cryoplant_purchase_cost_per_module',
                                         31478692.121086925),
 'blanket__cost_thermal_class_MW': ('selected_blanket_cost_thermal_class_MW', 3306.8890988488924),
 'shield__cost_thermal_class_MW': ('selected_shield_cost_thermal_class_MW', 3306.8890988488924),
 'structure__cost_gross_class_MWe': ('selected_structure_cost_gross_class_MWe', 1219.9981701764736),
 'vessel__cost_gross_class_MWe': ('selected_vessel_cost_gross_class_MWe', 1219.9981701764736),
 'misc_plant__cost_gross_class_MWe': ('selected_misc_plant_cost_gross_class_MWe', 1219.9981701764736),
 'remote_handling_cost_gross_class_MWe': ('selected_remote_handling_cost_gross_class_MWe',
                                          1219.9981701764736),
 'cryoplant__aux_cost_thermal_class_MW': ('selected_cryoplant_aux_cost_thermal_class_MW',
                                          3306.8890988488924),
 'waste_cost_thermal_class_MW': ('selected_waste_cost_thermal_class_MW', 3306.8890988488924),
 'other_rpe_cost_net_class_MWe': ('selected_other_rpe_cost_net_class_MWe', 850.0653006674999),
 'inc_cost_thermal_class_MW': ('selected_inc_cost_thermal_class_MW', 3306.8890988488924),
 'owner_cost_net_class_MWe': ('selected_owner_cost_net_class_MWe', 850.0653006674999),
 'startup_cost_net_class_MWe': ('selected_startup_cost_net_class_MWe', 850.0653006674999),
 'decom_cost_net_class_MWe': ('selected_decom_cost_net_class_MWe', 850.0653006674999),
 'om_staffing_net_class_MWe': ('selected_om_staffing_net_class_MWe', 850.0653006674999),
 'buildings__legacy_cost_fusion_class_MW': ('selected_buildings_legacy_cost_fusion_class_MW',
                                            2652.5632625175904),
 'buildings__legacy_cost_gross_class_MWe': ('selected_buildings_legacy_cost_gross_class_MWe',
                                            1219.9981701764736),
 'buildings__legacy_cost_thermal_electric_class_MWe': ('selected_buildings_legacy_cost_thermal_electric_class_MWe',
                                                       1219.9981701764736),
 'buildings__legacy_cost_thermal_class_MW': ('selected_buildings_legacy_cost_thermal_class_MW',
                                             3306.8890988488924),
 'precon_legacy_cost_net_class_MWe': ('selected_precon_legacy_cost_net_class_MWe', 850.0653006674999),
 'heat_transport__legacy_cost_net_class_MWe': ('selected_heat_transport_legacy_cost_net_class_MWe',
                                               850.0653006674999),
 'heat_transport__legacy_cost_thermal_class_MW': ('selected_heat_transport_legacy_cost_thermal_class_MW',
                                                  3306.8890988488924),
 'fuel_cycle__legacy_cost_net_class_MWe': ('selected_fuel_cycle_legacy_cost_net_class_MWe',
                                           850.0653006674999)}

PUBLIC_DEFAULTS["electric_plant__installed_gross_rating_MWe"] = ("selected_electric_plant_installed_gross_rating_MWe", 1219.9981701764736)
DEFAULTS = {name:value for name,value in PUBLIC_DEFAULTS.values()}

def validate(parameters):
    for key in DEFAULTS:
        value = parameters[key]
        if not math.isfinite(value) or value < 0:
            raise ValueError('supplied procurement value must be finite and nonnegative: ' + key)
    if parameters['n_mod'] != 1:
        raise ValueError('supplied package procurement currently supports one module')
