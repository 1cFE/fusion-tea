package whole_plant_conversion_accounts {
    private import ScalarValues::*;
    private import costed_component::*;
    part def 'Supplied Plant Account' :> 'Costed Component' { doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */ }
    calc def 'Actual Exchanger Approaches' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/actual_exchanger_approaches_impl.py; reviewed equations in design/configuration. */
        in attribute primary_hot_in : Real;
        in attribute primary_exchanger_return_in : Real;
        in attribute secondary_in_in : Real;
        in attribute secondary_out_in : Real;
        out attribute hot_gap : Real;
        out attribute cold_gap : Real;
    }
    calc def 'Captured Reactor Offer' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/captured_reactor_offer_impl.py; reviewed equations in design/configuration. */
        in attribute capture_id_in : Real;
        out attribute magnet_capital : Real;
        out attribute tape_cost : Real;
        out attribute material_cost : Real;
        out attribute insulation_cost : Real;
        out attribute winding_cost : Real;
        out attribute support_cost : Real;
        out attribute coil_drive_MW : Real;
        out attribute refrigeration_MW : Real;
        out attribute cold_W : Real;
        out attribute intercept_W : Real;
        out attribute fit_margin : Real;
        out attribute current_margin : Real;
        out attribute peak_field : Real;
        out attribute strain : Real;
        out attribute stress_Pa : Real;
        out attribute field_extrapolated : Real;
        out attribute cold_rating_W : Real;
        out attribute intercept_rating_W : Real;
        out attribute axis_field : Real;
        out attribute turn_current_A : Real;
        out attribute nuclear_heating_W_m3 : Real;
        out attribute nuclear_transport_qualified : Real;
        out attribute global_construction_qualified : Real;
        out attribute cold_volume_m3 : Real;
        out attribute inventory_cold_W : Real;
        out attribute fixed_cold_MW : Real;
        out attribute intercept_inventory_W : Real;
        out attribute cold_temperature_K : Real;
        out attribute intercept_temperature_K : Real;
        out attribute ambient_temperature_K : Real;
        out attribute cold_carnot_fraction : Real;
        out attribute intercept_carnot_fraction : Real;
        out attribute cold_margin_W : Real;
        out attribute intercept_margin_W : Real;
        out attribute field_margin_T : Real;
        out attribute strain_margin : Real;
        out attribute stress_margin_Pa : Real;
        out attribute identity_supported : Real;
    }
    calc def 'Conditional Cryogenic Demand' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/conditional_cryogenic_demand_impl.py; reviewed equations in design/configuration. */
        in attribute q_nuc_W_m3_in : Real;
        in attribute extra_cold_W_in : Real;
        in attribute cold_volume_m3_in : Real;
        in attribute inventory_cold_W_in : Real;
        in attribute fixed_cold_MW_in : Real;
        in attribute intercept_inventory_W_in : Real;
        in attribute cold_temperature_K_in : Real;
        in attribute intercept_temperature_K_in : Real;
        in attribute ambient_temperature_K_in : Real;
        in attribute cold_carnot_fraction_in : Real;
        in attribute intercept_carnot_fraction_in : Real;
        in attribute cold_rating_W_in : Real;
        in attribute intercept_rating_W_in : Real;
        out attribute cold_W : Real;
        out attribute intercept_W : Real;
        out attribute cold_electric_MW : Real;
        out attribute intercept_electric_MW : Real;
        out attribute refrigeration_MW : Real;
        out attribute cold_margin_W : Real;
        out attribute intercept_margin_W : Real;
        out attribute q_nuc_capacity_W_m3 : Real;
        out attribute extra_cold_capacity_W : Real;
        out attribute nuclear_transport_qualified : Real;
        out attribute domain_supported : Real;
    }
    calc def 'Fuel Supply Accounts' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/fuel_supply_accounts_impl.py; reviewed equations in design/configuration. */
        in attribute fusion_MW_in : Real;
        in attribute availability_in : Real;
        in attribute burn_fraction_in : Real;
        in attribute recycle_in : Real;
        in attribute tbr_in : Real;
        in attribute extraction_in : Real;
        in attribute stock_kg_in : Real;
        in attribute startup_required_kg_in : Real;
        in attribute processing_capacity_kg_s_in : Real;
        in attribute decay_in : Real;
        in attribute seconds_year_in : Real;
        in attribute m_T_in : Real;
        in attribute m_D_in : Real;
        in attribute m_Li6_in : Real;
        in attribute q_eff_in : Real;
        in attribute MeV_J_in : Real;
        in attribute tritium_price_in : Real;
        in attribute deuterium_price_in : Real;
        in attribute li6_price_in : Real;
        out attribute reaction_rate : Real;
        out attribute burn_kg_s : Real;
        out attribute loss_kg_s : Real;
        out attribute processing_kg_s : Real;
        out attribute stock_margin : Real;
        out attribute processing_margin : Real;
        out attribute annual_T_need : Real;
        out attribute annual_T_bred : Real;
        out attribute annual_T_external : Real;
        out attribute annual_T_surplus : Real;
        out attribute annual_D_kg : Real;
        out attribute annual_Li6_kg : Real;
        out attribute annual_T_cost : Real;
        out attribute annual_D_cost : Real;
        out attribute annual_Li6_cost : Real;
        out attribute annual_fuel : Real;
        out attribute initial_T_cost : Real;
        out attribute self_sufficiency_margin : Real;
        out attribute D_atom_residual : Real;
        out attribute T_atom_residual : Real;
        out attribute Li6_atom_residual : Real;
        out attribute domain_supported : Real;
    }
    calc def 'Supplied Primary Capacity' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_primary_capacity_impl.py; reviewed equations in design/configuration. */
        in attribute pressure_rating_Pa_in : Real;
        in attribute pressure_demand_Pa_in : Real;
        in attribute electric_rating_MW_in : Real;
        in attribute electric_demand_MW_in : Real;
        in attribute path_flow_rating_in : Real;
        in attribute path_flow_demand_in : Real;
        in attribute path_count_in : Real;
        out attribute pressure_margin_Pa : Real;
        out attribute electric_margin_MW : Real;
        out attribute flow_margin_kg_s : Real;
        out attribute inventory_supported : Real;
    }
    calc def 'Supplied Source Basis' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_source_basis_impl.py; reviewed equations in design/configuration. */
        in attribute q_source_MW_in : Real;
        in attribute deposited_heating_MW_in : Real;
        in attribute neutron_multiplier_in : Real;
        in attribute heating_source_efficiency_in : Real;
        in attribute heating_coupling_efficiency_in : Real;
        in attribute heating_coupled_rating_in : Real;
        in attribute heating_wall_rating_in : Real;
        in attribute fusion_envelope_MW_in : Real;
        in attribute wall_reference_in : Real;
        in attribute wall_fusion_reference_in : Real;
        in attribute divertor_limit_in : Real;
        in attribute alpha_proxy_in : Real;
        in attribute alpha_retention_in : Real;
        in attribute radiation_fraction_in : Real;
        in attribute divertor_peaking_in : Real;
        in attribute divertor_area_in : Real;
        out attribute fusion_MW : Real;
        out attribute reconstructed_source_MW : Real;
        out attribute source_residual : Real;
        out attribute source_qualified : Real;
        out attribute heating_wall_MW : Real;
        out attribute heating_loss_MW : Real;
        out attribute heating_coupled_margin : Real;
        out attribute heating_wall_margin : Real;
        out attribute wall_load : Real;
        out attribute divertor_load : Real;
        out attribute divertor_margin : Real;
        out attribute fusion_envelope_margin : Real;
        out attribute domain_supported : Real;
    }
    calc def 'Temperature Kelvin' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/temperature_kelvin_impl.py; reviewed equations in design/configuration. */
        in attribute celsius_in : Real;
        out attribute value : Real;
    }
    calc def 'Whole Plant Capital Accounts' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_capital_accounts_impl.py; reviewed equations in design/configuration. */
        in attribute land_in : Real;
        in attribute facilities_in : Real;
        in attribute magnet_in : Real;
        in attribute heating_in : Real;
        in attribute divertor_in : Real;
        in attribute blanket_in : Real;
        in attribute shield_in : Real;
        in attribute structure_in : Real;
        in attribute vessel_in : Real;
        in attribute power_supplies_in : Real;
        in attribute remote_handling_in : Real;
        in attribute installation_in : Real;
        in attribute primary_circulators_in : Real;
        in attribute primary_pipes_in : Real;
        in attribute primary_spares_in : Real;
        in attribute primary_helium_in : Real;
        in attribute cryoplant_in : Real;
        in attribute auxiliary_rejection_in : Real;
        in attribute waste_in : Real;
        in attribute fuel_processing_in : Real;
        in attribute other_reactor_in : Real;
        in attribute reactor_controls_in : Real;
        in attribute shared_electrical_in : Real;
        in attribute miscellaneous_in : Real;
        in attribute pbl_initial_in : Real;
        in attribute owner_in : Real;
        in attribute digital_twin_in : Real;
        in attribute source_installation_allowance_in : Real;
        in attribute tritium_initial_in : Real;
        in attribute capital_1_in : Real;
        in attribute capital_2_in : Real;
        in attribute capital_3_in : Real;
        in attribute capital_4_in : Real;
        in attribute capital_5_in : Real;
        in attribute capital_6_in : Real;
        in attribute capital_7_in : Real;
        in attribute capital_8_in : Real;
        in attribute capital_9_in : Real;
        in attribute capital_10_in : Real;
        in attribute controller_capital_in : Real;
        in attribute salt_spare_in : Real;
        in attribute salt_vendor_in : Real;
        in attribute steam_branch_in : Real;
        in attribute contingency_rate_in : Real;
        in attribute indirect_rate_in : Real;
        in attribute freight_rate_in : Real;
        in attribute general_spares_rate_in : Real;
        in attribute tax_rate_in : Real;
        in attribute insurance_rate_in : Real;
        in attribute commissioning_rate_in : Real;
        in attribute construction_years_in : Real;
        out attribute common_purchases : Real;
        out attribute branch_purchases : Real;
        out attribute direct_base : Real;
        out attribute equipment_base : Real;
        out attribute freight_base : Real;
        out attribute general_spares_base : Real;
        out attribute tax_base : Real;
        out attribute insurance_base : Real;
        out attribute overhaul_base : Real;
        out attribute salvage_base : Real;
        out attribute contingency : Real;
        out attribute indirect : Real;
        out attribute freight : Real;
        out attribute general_spares : Real;
        out attribute tax : Real;
        out attribute insurance : Real;
        out attribute nonfuel_commissioning : Real;
        out attribute cas20 : Real;
        out attribute cas30 : Real;
        out attribute cas50 : Real;
        out attribute initial_capital : Real;
        out attribute reconciliation_residual : Real;
        out attribute domain_supported : Real;
    }
    calc def 'Whole Plant Lifecycle Ledger' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_lifecycle_ledger_impl.py; reviewed equations in design/configuration. */
        in attribute initial_capital_in : Real;
        in attribute salvage_base_in : Real;
        in attribute overhaul_base_in : Real;
        in attribute magnet_capital_in : Real;
        in attribute blanket_capital_in : Real;
        in attribute divertor_capital_in : Real;
        in attribute pbl_capital_in : Real;
        in attribute helium_capital_in : Real;
        in attribute wall_load_in : Real;
        in attribute annual_export_MWh_in : Real;
        in attribute annual_net_grid_MWh_in : Real;
        in attribute annual_import_cost_in : Real;
        in attribute annual_fuel_in : Real;
        in attribute conversion_annual_service_in : Real;
        in attribute conversion_annual_makeup_in : Real;
        in attribute conversion_replacement_pv_in : Real;
        in attribute rate_in : Real;
        in attribute years_in : Real;
        in attribute availability_in : Real;
        in attribute construction_years_in : Real;
        in attribute routine_om_in : Real;
        in attribute routine_fraction_in : Real;
        in attribute wall_life_in : Real;
        in attribute magnet_life_in : Real;
        in attribute blanket_outage_in : Real;
        in attribute magnet_outage_in : Real;
        in attribute other_outage_in : Real;
        in attribute blanket_removal_fraction_in : Real;
        in attribute magnet_removal_fraction_in : Real;
        in attribute pbl_refill_fraction_in : Real;
        in attribute primary_event_in : Real;
        in attribute primary_life_in : Real;
        in attribute helium_makeup_fraction_in : Real;
        in attribute overhaul_fraction_in : Real;
        in attribute overhaul_year_in : Real;
        in attribute dismantle_fraction_in : Real;
        in attribute salvage_fraction_in : Real;
        out attribute initial_financed_capital : Real;
        out attribute annual_source_service : Real;
        out attribute annual_service : Real;
        out attribute annual_makeup : Real;
        out attribute annual_expense : Real;
        out attribute blanket_life_years : Real;
        out attribute magnet_life_years : Real;
        out attribute blanket_events : Real;
        out attribute magnet_events : Real;
        out attribute primary_events : Real;
        out attribute blanket_replacement_pv : Real;
        out attribute magnet_replacement_pv : Real;
        out attribute primary_replacement_pv : Real;
        out attribute overhaul_pv : Real;
        out attribute source_replacement_pv : Real;
        out attribute conversion_replacement_pv : Real;
        out attribute terminal_pv : Real;
        out attribute annual_expense_pv : Real;
        out attribute total_cost_pv : Real;
        out attribute energy_pv : Real;
        out attribute lcoe_USD2025_MWh : Real;
        out attribute outage_years : Real;
        out attribute outage_margin : Real;
        out attribute domain_supported : Real;
        out attribute economic_defined : Real;
        out attribute cost_residual : Real;
    }
    calc def 'Whole Plant Operating Ledger' {
        doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/whole_plant_operating_ledger_impl.py; reviewed equations in design/configuration. */
        in attribute conversion_net_MW_in : Real;
        in attribute primary_electric_MW_in : Real;
        in attribute primary_fluid_MW_in : Real;
        in attribute heating_wall_MW_in : Real;
        in attribute deposited_heating_MW_in : Real;
        in attribute coil_drive_MW_in : Real;
        in attribute refrigeration_MW_in : Real;
        in attribute cold_W_in : Real;
        in attribute intercept_W_in : Real;
        in attribute tf_cooling_MW_in : Real;
        in attribute pf_cooling_MW_in : Real;
        in attribute fuel_vacuum_MW_in : Real;
        in attribute house_MW_in : Real;
        in attribute reactor_controls_MW_in : Real;
        in attribute residual_MW_in : Real;
        in attribute auxiliary_electric_MW_in : Real;
        in attribute auxiliary_rating_MW_in : Real;
        in attribute auxiliary_water_C_in : Real;
        in attribute availability_in : Real;
        in attribute import_price_in : Real;
        out attribute upstream_electric_MW : Real;
        out attribute net_export_MW : Real;
        out attribute standby_MW : Real;
        out attribute annual_export_MWh : Real;
        out attribute annual_import_MWh : Real;
        out attribute annual_net_grid_MWh : Real;
        out attribute annual_import_cost : Real;
        out attribute auxiliary_heat_MW : Real;
        out attribute auxiliary_margin_MW : Real;
        out attribute primary_motor_loss_MW : Real;
        out attribute power_residual : Real;
        out attribute domain_supported : Real;
    }
    constraint def 'Whole Plant Nonnegative' { doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */ in metric_in : Real; metric_in >= 0.0 }
    constraint def 'Whole Plant Positive' { doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */ in metric_in : Real; metric_in > 0.0 }
    constraint def 'Whole Plant Supported' { doc /* **Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. */ in metric_in : Real; metric_in >= 1.0 }
}
