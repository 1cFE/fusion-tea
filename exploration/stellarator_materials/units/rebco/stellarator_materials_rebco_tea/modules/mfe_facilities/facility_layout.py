"""Facility_LayoutModule Module Wrapper

TEAx module for Facility_Layout calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Manual completion reuses the live calendar and emits the declared finite scalar contract; deterministic ledgers are diagnostics.

Inputs:
    - selected_site_services_building_height_in: selected_site_services_building_height_in parameter
    - selected_sector_link_east_width_in: selected_sector_link_east_width_in parameter
    - selected_cooling_helium_store_width_in: selected_cooling_helium_store_width_in parameter
    - selected_cooling_bundle_store_width_in: selected_cooling_bundle_store_width_in parameter
    - cooling_dirty_helium_positions_in: cooling_dirty_helium_positions_in parameter
    - salt_package_height_in: salt_package_height_in parameter
    - selected_site_services_building_width_in: selected_site_services_building_width_in parameter
    - selected_sector_wing_south_length_in: selected_sector_wing_south_length_in parameter
    - selected_service_water_building_length_in: selected_service_water_building_length_in parameter
    - dirty_buffer_positions_in: dirty_buffer_positions_in parameter
    - building_separation_in: building_separation_in parameter
    - cooling_internal_move_days_in: cooling_internal_move_days_in parameter
    - cooling_cross_width_in: cooling_cross_width_in parameter
    - provisional_envelope_scale_in: provisional_envelope_scale_in parameter
    - site_services_width_in: site_services_width_in parameter
    - hx_end_allowance_in: hx_end_allowance_in parameter
    - selected_sector_wing_south_width_in: selected_sector_wing_south_width_in parameter
    - selected_fuel_building_width_in: selected_fuel_building_width_in parameter
    - selected_sector_link_south_width_in: selected_sector_link_south_width_in parameter
    - selected_sector_wing_west_width_in: selected_sector_wing_west_width_in parameter
    - selected_sector_wing_east_length_in: selected_sector_wing_east_length_in parameter
    - selected_turbine_hall_height_in: selected_turbine_hall_height_in parameter
    - sector_join_days_in: sector_join_days_in parameter
    - selected_cryo_compressors_length_in: selected_cryo_compressors_length_in parameter
    - cooling_machine_stations_in: cooling_machine_stations_in parameter
    - cooling_prepare_stations_in: cooling_prepare_stations_in parameter
    - reactor_aux_length_in: reactor_aux_length_in parameter
    - selected_parcel_x_min_in: selected_parcel_x_min_in parameter
    - turbine_height_in: turbine_height_in parameter
    - selected_service_water_building_width_in: selected_service_water_building_width_in parameter
    - selected_cryo_coldbox_length_in: selected_cryo_coldbox_length_in parameter
    - calendar_unplanned_in: calendar_unplanned_in parameter
    - selected_cooling_hall_height_in: selected_cooling_hall_height_in parameter
    - n_mod_in: n_mod_in parameter
    - control_area_per_person_in: control_area_per_person_in parameter
    - administration_occupants_in: administration_occupants_in parameter
    - cooling_helium_count_in: cooling_helium_count_in parameter
    - selected_cryo_compressors_width_in: selected_cryo_compressors_width_in parameter
    - selected_cryo_coldbox_height_in: selected_cryo_coldbox_height_in parameter
    - cooling_aisle_width_in: cooling_aisle_width_in parameter
    - selected_cooling_hall_length_in: selected_cooling_hall_length_in parameter
    - sector_service_teams_in: sector_service_teams_in parameter
    - cooling_hold_days_in: cooling_hold_days_in parameter
    - service_water_height_in: service_water_height_in parameter
    - selected_service_water_building_height_in: selected_service_water_building_height_in parameter
    - cooling_dirty_bundle_positions_in: cooling_dirty_bundle_positions_in parameter
    - cooling_clean_salt_positions_in: cooling_clean_salt_positions_in parameter
    - selected_sector_link_west_height_in: selected_sector_link_west_height_in parameter
    - selected_sector_link_east_height_in: selected_sector_link_east_height_in parameter
    - waste_package_yield_in: waste_package_yield_in parameter
    - selected_administration_length_in: selected_administration_length_in parameter
    - cooling_prepare_bundle_days_in: cooling_prepare_bundle_days_in parameter
    - selected_administration_height_in: selected_administration_height_in parameter
    - selected_cryo_coldbox_width_in: selected_cryo_coldbox_width_in parameter
    - sector_headroom_in: sector_headroom_in parameter
    - initial_sector_start_days_in: initial_sector_start_days_in parameter
    - cooling_clean_bundle_positions_in: cooling_clean_bundle_positions_in parameter
    - selected_electrical_building_width_in: selected_electrical_building_width_in parameter
    - selected_power_supply_building_height_in: selected_power_supply_building_height_in parameter
    - hx_tube_length_in: hx_tube_length_in parameter
    - conventional_rebar_density_in: conventional_rebar_density_in parameter
    - selected_sector_wing_west_length_in: selected_sector_wing_west_length_in parameter
    - selected_sector_wing_west_height_in: selected_sector_wing_west_height_in parameter
    - selected_control_length_in: selected_control_length_in parameter
    - power_supply_length_in: power_supply_length_in parameter
    - component_remove_days_in: component_remove_days_in parameter
    - calendar_fluence_in: calendar_fluence_in parameter
    - cryo_coldbox_length_in: cryo_coldbox_length_in parameter
    - administration_area_per_person_in: administration_area_per_person_in parameter
    - selected_sector_wing_north_length_in: selected_sector_wing_north_length_in parameter
    - facilities_cost_mode_in: facilities_cost_mode_in parameter
    - selected_fuel_building_height_in: selected_fuel_building_height_in parameter
    - component_hold_days_in: component_hold_days_in parameter
    - selected_site_services_building_length_in: selected_site_services_building_length_in parameter
    - selected_sector_link_south_length_in: selected_sector_link_south_length_in parameter
    - selected_sector_link_west_length_in: selected_sector_link_west_length_in parameter
    - selected_reactor_auxiliaries_length_in: selected_reactor_auxiliaries_length_in parameter
    - selected_electrical_building_height_in: selected_electrical_building_height_in parameter
    - selected_control_height_in: selected_control_height_in parameter
    - external_access_width_in: external_access_width_in parameter
    - conventional_shop_width_in: conventional_shop_width_in parameter
    - cooling_machine_life_in: cooling_machine_life_in parameter
    - cooling_dirty_salt_positions_in: cooling_dirty_salt_positions_in parameter
    - power_supply_height_in: power_supply_height_in parameter
    - selected_sector_wing_north_width_in: selected_sector_wing_north_width_in parameter
    - security_area_per_person_in: security_area_per_person_in parameter
    - cooling_initial_receipt_lead_days_in: cooling_initial_receipt_lead_days_in parameter
    - service_water_width_in: service_water_width_in parameter
    - selected_cooling_link_height_in: selected_cooling_link_height_in parameter
    - selected_sector_link_west_width_in: selected_sector_link_west_width_in parameter
    - sector_count_in: sector_count_in parameter
    - cooling_bundle_life_in: cooling_bundle_life_in parameter
    - cooling_airlock_length_in: cooling_airlock_length_in parameter
    - fuel_length_in: fuel_length_in parameter
    - heat_rejection_width_in: heat_rejection_width_in parameter
    - cooldown_days_in: cooldown_days_in parameter
    - cryo_coldbox_width_in: cryo_coldbox_width_in parameter
    - cooling_bundle_stations_in: cooling_bundle_stations_in parameter
    - selected_cooling_link_length_in: selected_cooling_link_length_in parameter
    - cooling_headroom_in: cooling_headroom_in parameter
    - sector_clean_days_in: sector_clean_days_in parameter
    - reactor_aux_height_in: reactor_aux_height_in parameter
    - selected_sector_link_north_width_in: selected_sector_link_north_width_in parameter
    - selected_cooling_annex_north_depth_in: selected_cooling_annex_north_depth_in parameter
    - initial_receipt_lead_days_in: initial_receipt_lead_days_in parameter
    - onsite_ac_height_in: onsite_ac_height_in parameter
    - service_water_length_in: service_water_length_in parameter
    - cooling_initial_handoff_days_in: cooling_initial_handoff_days_in parameter
    - occupancy_height_in: occupancy_height_in parameter
    - minor_outer_radius_in: minor_outer_radius_in parameter
    - selected_cryo_compressors_height_in: selected_cryo_compressors_height_in parameter
    - cooling_prepare_machine_days_in: cooling_prepare_machine_days_in parameter
    - helium_package_height_in: helium_package_height_in parameter
    - reactor_aux_width_in: reactor_aux_width_in parameter
    - selected_sector_link_south_height_in: selected_sector_link_south_height_in parameter
    - component_prepare_days_in: component_prepare_days_in parameter
    - selected_cooling_hall_width_in: selected_cooling_hall_width_in parameter
    - selected_parcel_width_in: selected_parcel_width_in parameter
    - selected_control_width_in: selected_control_width_in parameter
    - clean_positions_in: clean_positions_in parameter
    - helium_package_width_in: helium_package_width_in parameter
    - occupancy_circulation_factor_in: occupancy_circulation_factor_in parameter
    - sector_route_clearance_in: sector_route_clearance_in parameter
    - calendar_count_in: calendar_count_in parameter
    - control_occupants_in: control_occupants_in parameter
    - selected_parcel_y_min_in: selected_parcel_y_min_in parameter
    - selected_cooling_annex_height_in: selected_cooling_annex_height_in parameter
    - cooling_salt_count_in: cooling_salt_count_in parameter
    - sector_test_days_in: sector_test_days_in parameter
    - component_width_in: component_width_in parameter
    - selected_maintenance_shop_width_in: selected_maintenance_shop_width_in parameter
    - selected_power_supply_building_width_in: selected_power_supply_building_width_in parameter
    - selected_power_supply_building_length_in: selected_power_supply_building_length_in parameter
    - sector_transport_days_in: sector_transport_days_in parameter
    - nuclear_wall_in: nuclear_wall_in parameter
    - selected_security_length_in: selected_security_length_in parameter
    - conventional_shop_length_in: conventional_shop_length_in parameter
    - sector_bays_in: sector_bays_in parameter
    - selected_reactor_hall_height_in: selected_reactor_hall_height_in parameter
    - selected_maintenance_shop_length_in: selected_maintenance_shop_length_in parameter
    - blanket_volume_in: blanket_volume_in parameter
    - cryo_compressors_length_in: cryo_compressors_length_in parameter
    - cooling_machine_process_days_in: cooling_machine_process_days_in parameter
    - cryo_coldbox_height_in: cryo_coldbox_height_in parameter
    - selected_parcel_length_in: selected_parcel_length_in parameter
    - nuclear_rebar_density_in: nuclear_rebar_density_in parameter
    - selected_cooling_link_width_in: selected_cooling_link_width_in parameter
    - selected_reactor_hall_length_in: selected_reactor_hall_length_in parameter
    - hx_shell_length_in: hx_shell_length_in parameter
    - calendar_mode_in: calendar_mode_in parameter
    - dirty_store_positions_in: dirty_store_positions_in parameter
    - turbine_width_in: turbine_width_in parameter
    - conventional_shop_height_in: conventional_shop_height_in parameter
    - selected_administration_width_in: selected_administration_width_in parameter
    - component_process_days_in: component_process_days_in parameter
    - selected_sector_wing_north_height_in: selected_sector_wing_north_height_in parameter
    - calendar_life_in: calendar_life_in parameter
    - cryo_compressors_height_in: cryo_compressors_height_in parameter
    - cooling_receipt_lead_days_in: cooling_receipt_lead_days_in parameter
    - selected_security_height_in: selected_security_height_in parameter
    - fuel_height_in: fuel_height_in parameter
    - selected_electrical_building_length_in: selected_electrical_building_length_in parameter
    - hx_shell_bore_in: hx_shell_bore_in parameter
    - hx_shell_wall_in: hx_shell_wall_in parameter
    - selected_turbine_hall_length_in: selected_turbine_hall_length_in parameter
    - conventional_floor_in: conventional_floor_in parameter
    - exterior_allowance_in: exterior_allowance_in parameter
    - selected_security_width_in: selected_security_width_in parameter
    - selected_reactor_hall_width_in: selected_reactor_hall_width_in parameter
    - security_occupants_in: security_occupants_in parameter
    - salt_package_width_in: salt_package_width_in parameter
    - selected_sector_link_north_height_in: selected_sector_link_north_height_in parameter
    - selected_turbine_hall_width_in: selected_turbine_hall_width_in parameter
    - selected_fuel_building_length_in: selected_fuel_building_length_in parameter
    - sector_split_days_in: sector_split_days_in parameter
    - selected_blanket_packages_per_sector_in: selected_blanket_packages_per_sector_in parameter
    - onsite_ac_width_in: onsite_ac_width_in parameter
    - recommission_days_in: recommission_days_in parameter
    - salt_package_length_in: salt_package_length_in parameter
    - selected_maintenance_shop_height_in: selected_maintenance_shop_height_in parameter
    - component_install_days_in: component_install_days_in parameter
    - calendar_availability_in: calendar_availability_in parameter
    - helium_package_length_in: helium_package_length_in parameter
    - selected_reactor_auxiliaries_width_in: selected_reactor_auxiliaries_width_in parameter
    - divertor_packages_per_sector_in: divertor_packages_per_sector_in parameter
    - selected_sector_wing_east_width_in: selected_sector_wing_east_width_in parameter
    - cooling_package_margin_in: cooling_package_margin_in parameter
    - component_receipt_lead_days_in: component_receipt_lead_days_in parameter
    - cooling_bundle_count_in: cooling_bundle_count_in parameter
    - cooling_clean_helium_positions_in: cooling_clean_helium_positions_in parameter
    - nuclear_roof_in: nuclear_roof_in parameter
    - cryo_compressors_width_in: cryo_compressors_width_in parameter
    - component_height_in: component_height_in parameter
    - nuclear_floor_in: nuclear_floor_in parameter
    - turbine_length_in: turbine_length_in parameter
    - selected_reactor_auxiliaries_height_in: selected_reactor_auxiliaries_height_in parameter
    - heat_rejection_length_in: heat_rejection_length_in parameter
    - major_radius_in: major_radius_in parameter
    - conventional_roof_in: conventional_roof_in parameter
    - component_length_in: component_length_in parameter
    - conventional_wall_in: conventional_wall_in parameter
    - calendar_years_in: calendar_years_in parameter
    - facilities_enabled_in: facilities_enabled_in parameter
    - cooling_field_cycle_days_in: cooling_field_cycle_days_in parameter
    - selected_cooling_salt_store_width_in: selected_cooling_salt_store_width_in parameter
    - component_handling_margin_in: component_handling_margin_in parameter
    - cooling_bundle_process_days_in: cooling_bundle_process_days_in parameter
    - calendar_outage_in: calendar_outage_in parameter
    - cooling_circuits_in: cooling_circuits_in parameter
    - site_services_length_in: site_services_length_in parameter
    - selected_sector_link_east_length_in: selected_sector_link_east_length_in parameter
    - fuel_width_in: fuel_width_in parameter
    - selected_sector_wing_south_height_in: selected_sector_wing_south_height_in parameter
    - site_services_height_in: site_services_height_in parameter
    - selected_sector_link_north_length_in: selected_sector_link_north_length_in parameter
    - selected_cooling_annex_length_in: selected_cooling_annex_length_in parameter
    - component_material_fraction_in: component_material_fraction_in parameter
    - selected_sector_wing_east_height_in: selected_sector_wing_east_height_in parameter
    - calendar_q_in: calendar_q_in parameter
    - power_supply_width_in: power_supply_width_in parameter
    - onsite_ac_length_in: onsite_ac_length_in parameter
    - selected_cooling_annex_width_in: selected_cooling_annex_width_in parameter

Outputs:
    - dirty_store_required: dirty_store_required result
    - electrical_building_required_length: electrical_building_required_length result
    - sector_link_north_clear_height: sector_link_north_clear_height result
    - reactor_auxiliaries_sub_formwork: reactor_auxiliaries_sub_formwork result
    - electrical_building_clear_height: electrical_building_clear_height result
    - dirty_store_positions_allocated: dirty_store_positions_allocated result
    - sector_wing_west_required_length: sector_wing_west_required_length result
    - cryo_compressors_sub_formwork: cryo_compressors_sub_formwork result
    - sector_wing_east_clear_length: sector_wing_east_clear_length result
    - sector_wing_east_super_rebar: sector_wing_east_super_rebar result
    - fuel_building_air_volume: fuel_building_air_volume result
    - turbine_hall_super_formwork: turbine_hall_super_formwork result
    - sector_link_north_clear_width: sector_link_north_clear_width result
    - sector_wing_north_required_width: sector_wing_north_required_width result
    - power_supply_building_clear_area: power_supply_building_clear_area result
    - control_required_height: control_required_height result
    - cooling_hall_clear_height: cooling_hall_clear_height result
    - administration_sub_concrete: administration_sub_concrete result
    - sector_wing_north_gross_area: sector_wing_north_gross_area result
    - administration_required_area: administration_required_area result
    - fuel_building_sub_rebar: fuel_building_sub_rebar result
    - sector_link_south_required_height: sector_link_south_required_height result
    - dirty_buffer_positions_allocated: dirty_buffer_positions_allocated result
    - sector_link_north_super_concrete: sector_link_north_super_concrete result
    - sector_wing_west_clear_length: sector_wing_west_clear_length result
    - cryo_coldbox_required_height: cryo_coldbox_required_height result
    - fuel_building_required_width: fuel_building_required_width result
    - required_parcel_x_min: required_parcel_x_min result
    - sector_wing_south_super_formwork: sector_wing_south_super_formwork result
    - control_clear_width: control_clear_width result
    - sector_link_north_gross_area: sector_link_north_gross_area result
    - electrical_building_super_formwork: electrical_building_super_formwork result
    - cooling_annex_gross_area: cooling_annex_gross_area result
    - replacement_ready_margin_days: replacement_ready_margin_days result
    - cooling_annex_sub_formwork: cooling_annex_sub_formwork result
    - maintenance_shop_clear_area: maintenance_shop_clear_area result
    - reactor_hall_gross_area: reactor_hall_gross_area result
    - control_air_volume: control_air_volume result
    - sector_wing_south_required_length: sector_wing_south_required_length result
    - site_services_building_sub_rebar: site_services_building_sub_rebar result
    - calendar_first_event_year: calendar_first_event_year result
    - site_services_building_super_concrete: site_services_building_super_concrete result
    - reactor_auxiliaries_gross_area: reactor_auxiliaries_gross_area result
    - reactor_hall_required_height: reactor_hall_required_height result
    - service_water_building_clear_height: service_water_building_clear_height result
    - sector_link_south_required_width: sector_link_south_required_width result
    - sector_link_west_clear_area: sector_link_west_clear_area result
    - occupancy_area_margin_m2: occupancy_area_margin_m2 result
    - power_supply_building_gross_area: power_supply_building_gross_area result
    - electrical_building_super_concrete: electrical_building_super_concrete result
    - required_parcel_y_max: required_parcel_y_max result
    - sector_link_south_super_concrete: sector_link_south_super_concrete result
    - site_services_building_sub_concrete: site_services_building_sub_concrete result
    - sector_link_south_sub_rebar: sector_link_south_sub_rebar result
    - cryo_compressors_clear_area: cryo_compressors_clear_area result
    - electrical_building_clear_width: electrical_building_clear_width result
    - sector_wing_east_super_concrete: sector_wing_east_super_concrete result
    - cooling_carrier_moves: cooling_carrier_moves result
    - cryo_coldbox_super_rebar: cryo_coldbox_super_rebar result
    - cryo_coldbox_super_formwork: cryo_coldbox_super_formwork result
    - cryo_coldbox_sub_formwork: cryo_coldbox_sub_formwork result
    - sector_wing_east_sub_rebar: sector_wing_east_sub_rebar result
    - power_supply_building_sub_rebar: power_supply_building_sub_rebar result
    - sector_link_south_clear_height: sector_link_south_clear_height result
    - dirty_buffer_required: dirty_buffer_required result
    - cooling_jobs_after_shutdown: cooling_jobs_after_shutdown result
    - service_water_building_super_rebar: service_water_building_super_rebar result
    - fuel_building_clear_area: fuel_building_clear_area result
    - cooling_link_clear_width: cooling_link_clear_width result
    - cooling_annex_super_formwork: cooling_annex_super_formwork result
    - site_services_building_required_width: site_services_building_required_width result
    - cooling_annex_required_height: cooling_annex_required_height result
    - reactor_auxiliaries_super_formwork: reactor_auxiliaries_super_formwork result
    - reactor_hall_clear_height: reactor_hall_clear_height result
    - sector_link_north_air_volume: sector_link_north_air_volume result
    - sector_wing_south_required_width: sector_wing_south_required_width result
    - control_sub_rebar: control_sub_rebar result
    - service_water_building_clear_area: service_water_building_clear_area result
    - sector_wing_west_clear_height: sector_wing_west_clear_height result
    - sector_wing_south_sub_rebar: sector_wing_south_sub_rebar result
    - sector_wing_south_required_height: sector_wing_south_required_height result
    - sector_link_west_super_concrete: sector_link_west_super_concrete result
    - administration_sub_rebar: administration_sub_rebar result
    - cooling_hall_clear_width: cooling_hall_clear_width result
    - exterior_envelope_qualified: exterior_envelope_qualified result
    - outage_required_days: outage_required_days result
    - security_clear_width: security_clear_width result
    - fuel_building_super_formwork: fuel_building_super_formwork result
    - power_supply_building_clear_width: power_supply_building_clear_width result
    - service_water_building_sub_concrete: service_water_building_sub_concrete result
    - cryo_compressors_super_formwork: cryo_compressors_super_formwork result
    - cryo_coldbox_clear_length: cryo_coldbox_clear_length result
    - cryo_compressors_required_length: cryo_compressors_required_length result
    - control_clear_length: control_clear_length result
    - calendar_last_event_year: calendar_last_event_year result
    - turbine_hall_clear_width: turbine_hall_clear_width result
    - controlled_air_volume: controlled_air_volume result
    - service_water_building_required_length: service_water_building_required_length result
    - cooling_replacement_ready_margin_days: cooling_replacement_ready_margin_days result
    - sector_link_west_air_volume: sector_link_west_air_volume result
    - sector_link_north_clear_area: sector_link_north_clear_area result
    - maintenance_shop_clear_length: maintenance_shop_clear_length result
    - blanket_packages_per_sector: blanket_packages_per_sector result
    - maintenance_shop_clear_height: maintenance_shop_clear_height result
    - cooling_hall_super_formwork: cooling_hall_super_formwork result
    - maintenance_shop_required_width: maintenance_shop_required_width result
    - sector_link_east_clear_area: sector_link_east_clear_area result
    - sector_wing_north_super_rebar: sector_wing_north_super_rebar result
    - turbine_hall_clear_height: turbine_hall_clear_height result
    - sector_width: sector_width result
    - service_water_building_clear_length: service_water_building_clear_length result
    - active: active result
    - maintenance_shop_sub_formwork: maintenance_shop_sub_formwork result
    - sector_wing_west_air_volume: sector_wing_west_air_volume result
    - site_services_building_clear_width: site_services_building_clear_width result
    - reactor_auxiliaries_required_height: reactor_auxiliaries_required_height result
    - cryo_compressors_sub_rebar: cryo_compressors_sub_rebar result
    - cooling_link_required_length: cooling_link_required_length result
    - sector_wing_north_sub_formwork: sector_wing_north_sub_formwork result
    - power_supply_building_required_width: power_supply_building_required_width result
    - sector_wing_west_super_concrete: sector_wing_west_super_concrete result
    - electrical_building_sub_formwork: electrical_building_sub_formwork result
    - turbine_hall_required_height: turbine_hall_required_height result
    - cryo_coldbox_clear_width: cryo_coldbox_clear_width result
    - sector_wing_east_sub_formwork: sector_wing_east_sub_formwork result
    - reactor_auxiliaries_air_volume: reactor_auxiliaries_air_volume result
    - sector_link_east_sub_rebar: sector_link_east_sub_rebar result
    - cooling_link_sub_concrete: cooling_link_sub_concrete result
    - security_required_height: security_required_height result
    - sector_wing_east_clear_area: sector_wing_east_clear_area result
    - site_services_building_clear_area: site_services_building_clear_area result
    - sector_link_north_required_height: sector_link_north_required_height result
    - cooling_annex_super_rebar: cooling_annex_super_rebar result
    - power_supply_building_sub_formwork: power_supply_building_sub_formwork result
    - cooling_link_air_volume: cooling_link_air_volume result
    - cryo_compressors_clear_height: cryo_compressors_clear_height result
    - maintenance_shop_super_concrete: maintenance_shop_super_concrete result
    - cooling_hall_sub_rebar: cooling_hall_sub_rebar result
    - sector_wing_east_sub_concrete: sector_wing_east_sub_concrete result
    - cooling_helium_queue_peak: cooling_helium_queue_peak result
    - fuel_building_clear_height: fuel_building_clear_height result
    - service_water_building_clear_width: service_water_building_clear_width result
    - sector_link_south_required_length: sector_link_south_required_length result
    - administration_clear_area: administration_clear_area result
    - cryo_coldbox_required_width: cryo_coldbox_required_width result
    - cooling_link_clear_area: cooling_link_clear_area result
    - site_services_building_sub_formwork: site_services_building_sub_formwork result
    - turbine_hall_super_rebar: turbine_hall_super_rebar result
    - cooling_salt_queue_peak: cooling_salt_queue_peak result
    - sector_link_south_air_volume: sector_link_south_air_volume result
    - cooling_dirty_bundle_required: cooling_dirty_bundle_required result
    - sector_wing_east_clear_width: sector_wing_east_clear_width result
    - sector_link_east_super_formwork: sector_link_east_super_formwork result
    - security_air_volume: security_air_volume result
    - reactor_auxiliaries_super_rebar: reactor_auxiliaries_super_rebar result
    - service_water_building_super_formwork: service_water_building_super_formwork result
    - reactor_hall_clear_length: reactor_hall_clear_length result
    - reactor_hall_sub_formwork: reactor_hall_sub_formwork result
    - sector_link_east_required_length: sector_link_east_required_length result
    - cooling_hall_clear_area: cooling_hall_clear_area result
    - sector_wing_west_sub_rebar: sector_wing_west_sub_rebar result
    - administration_air_volume: administration_air_volume result
    - turbine_hall_clear_length: turbine_hall_clear_length result
    - sector_link_south_clear_length: sector_link_south_clear_length result
    - sector_wing_east_clear_height: sector_wing_east_clear_height result
    - turbine_hall_clear_area: turbine_hall_clear_area result
    - sector_link_east_required_height: sector_link_east_required_height result
    - sector_wing_west_sub_formwork: sector_wing_west_sub_formwork result
    - service_water_building_required_height: service_water_building_required_height result
    - sector_link_south_super_rebar: sector_link_south_super_rebar result
    - control_gross_area: control_gross_area result
    - fuel_building_gross_area: fuel_building_gross_area result
    - sector_length: sector_length result
    - cooling_annex_sub_rebar: cooling_annex_sub_rebar result
    - cooling_annex_clear_area: cooling_annex_clear_area result
    - calendar_event_count: calendar_event_count result
    - sector_link_west_sub_formwork: sector_link_west_sub_formwork result
    - sector_wing_west_clear_width: sector_wing_west_clear_width result
    - security_sub_concrete: security_sub_concrete result
    - fuel_building_super_concrete: fuel_building_super_concrete result
    - cooling_clean_salt_allocated: cooling_clean_salt_allocated result
    - cryo_compressors_gross_area: cryo_compressors_gross_area result
    - sector_link_east_clear_length: sector_link_east_clear_length result
    - cooling_annex_air_volume: cooling_annex_air_volume result
    - cryo_coldbox_clear_area: cryo_coldbox_clear_area result
    - sector_wing_south_gross_area: sector_wing_south_gross_area result
    - cooling_outage_basis_resolved: cooling_outage_basis_resolved result
    - turbine_hall_required_width: turbine_hall_required_width result
    - sector_wing_north_clear_length: sector_wing_north_clear_length result
    - cryo_compressors_required_height: cryo_compressors_required_height result
    - turbine_hall_sub_concrete: turbine_hall_sub_concrete result
    - contamination_procedure_qualified: contamination_procedure_qualified result
    - cooling_hall_super_concrete: cooling_hall_super_concrete result
    - turbine_hall_super_concrete: turbine_hall_super_concrete result
    - control_super_rebar: control_super_rebar result
    - sector_link_north_sub_rebar: sector_link_north_sub_rebar result
    - maintenance_shop_sub_concrete: maintenance_shop_sub_concrete result
    - sector_link_south_clear_width: sector_link_south_clear_width result
    - parcel_area: parcel_area result
    - sector_wing_south_super_concrete: sector_wing_south_super_concrete result
    - cryo_coldbox_required_length: cryo_coldbox_required_length result
    - administration_clear_length: administration_clear_length result
    - sector_link_east_air_volume: sector_link_east_air_volume result
    - security_clear_height: security_clear_height result
    - sector_wing_south_clear_height: sector_wing_south_clear_height result
    - reactor_auxiliaries_clear_height: reactor_auxiliaries_clear_height result
    - packages_per_sector: packages_per_sector result
    - security_sub_rebar: security_sub_rebar result
    - maintenance_shop_required_length: maintenance_shop_required_length result
    - administration_required_height: administration_required_height result
    - sector_link_east_sub_concrete: sector_link_east_sub_concrete result
    - sector_wing_east_gross_area: sector_wing_east_gross_area result
    - sector_link_east_super_rebar: sector_link_east_super_rebar result
    - fuel_building_clear_length: fuel_building_clear_length result
    - security_super_rebar: security_super_rebar result
    - cryo_compressors_sub_concrete: cryo_compressors_sub_concrete result
    - service_water_building_super_concrete: service_water_building_super_concrete result
    - reactor_hall_sub_concrete: reactor_hall_sub_concrete result
    - service_water_building_sub_formwork: service_water_building_sub_formwork result
    - sector_link_east_sub_formwork: sector_link_east_sub_formwork result
    - security_sub_formwork: security_sub_formwork result
    - security_super_concrete: security_super_concrete result
    - sector_wing_west_clear_area: sector_wing_west_clear_area result
    - cryo_compressors_super_rebar: cryo_compressors_super_rebar result
    - control_clear_area: control_clear_area result
    - cooling_annex_super_concrete: cooling_annex_super_concrete result
    - control_super_formwork: control_super_formwork result
    - turbine_hall_sub_formwork: turbine_hall_sub_formwork result
    - electrical_building_air_volume: electrical_building_air_volume result
    - cooling_hall_air_volume: cooling_hall_air_volume result
    - sector_link_west_sub_rebar: sector_link_west_sub_rebar result
    - cooling_hall_required_height: cooling_hall_required_height result
    - sector_wing_east_air_volume: sector_wing_east_air_volume result
    - sector_wing_south_clear_area: sector_wing_south_clear_area result
    - sector_link_east_gross_area: sector_link_east_gross_area result
    - cooling_link_required_width: cooling_link_required_width result
    - outage_allowed_days: outage_allowed_days result
    - cooling_annex_clear_length: cooling_annex_clear_length result
    - sector_wing_north_sub_rebar: sector_wing_north_sub_rebar result
    - sector_link_west_super_formwork: sector_link_west_super_formwork result
    - initial_margin_days: initial_margin_days result
    - sector_wing_east_required_height: sector_wing_east_required_height result
    - sector_wing_east_required_length: sector_wing_east_required_length result
    - service_water_building_sub_rebar: service_water_building_sub_rebar result
    - site_services_building_clear_height: site_services_building_clear_height result
    - administration_clear_width: administration_clear_width result
    - maintenance_shop_clear_width: maintenance_shop_clear_width result
    - cooling_last_release_year: cooling_last_release_year result
    - sector_wing_north_required_height: sector_wing_north_required_height result
    - power_supply_building_clear_height: power_supply_building_clear_height result
    - reactor_hall_required_length: reactor_hall_required_length result
    - cooling_dirty_salt_allocated: cooling_dirty_salt_allocated result
    - reactor_hall_sub_rebar: reactor_hall_sub_rebar result
    - sector_link_east_clear_height: sector_link_east_clear_height result
    - cooling_hall_required_width: cooling_hall_required_width result
    - site_services_building_super_rebar: site_services_building_super_rebar result
    - sector_link_north_required_width: sector_link_north_required_width result
    - cryo_compressors_clear_width: cryo_compressors_clear_width result
    - turbine_hall_gross_area: turbine_hall_gross_area result
    - reactor_hall_required_width: reactor_hall_required_width result
    - sector_link_north_required_length: sector_link_north_required_length result
    - sector_link_west_clear_length: sector_link_west_clear_length result
    - control_sub_concrete: control_sub_concrete result
    - power_supply_building_super_concrete: power_supply_building_super_concrete result
    - electrical_building_required_height: electrical_building_required_height result
    - reactor_auxiliaries_super_concrete: reactor_auxiliaries_super_concrete result
    - site_services_building_gross_area: site_services_building_gross_area result
    - reactor_auxiliaries_required_length: reactor_auxiliaries_required_length result
    - fuel_building_super_rebar: fuel_building_super_rebar result
    - fuel_building_required_height: fuel_building_required_height result
    - cooling_initial_ready_margin_days: cooling_initial_ready_margin_days result
    - sector_link_east_required_width: sector_link_east_required_width result
    - electrical_building_sub_concrete: electrical_building_sub_concrete result
    - security_gross_area: security_gross_area result
    - sector_link_north_sub_concrete: sector_link_north_sub_concrete result
    - sector_wing_south_sub_concrete: sector_wing_south_sub_concrete result
    - cooling_annex_required_length: cooling_annex_required_length result
    - turbine_hall_required_length: turbine_hall_required_length result
    - geometry_fit_margin_m: geometry_fit_margin_m result
    - readiness_margin_days: readiness_margin_days result
    - sector_wing_north_air_volume: sector_wing_north_air_volume result
    - power_supply_building_air_volume: power_supply_building_air_volume result
    - total_gross_area: total_gross_area result
    - sector_wing_north_sub_concrete: sector_wing_north_sub_concrete result
    - cooling_annex_required_width: cooling_annex_required_width result
    - cryo_compressors_required_width: cryo_compressors_required_width result
    - required_parcel_x_max: required_parcel_x_max result
    - sector_wing_north_clear_area: sector_wing_north_clear_area result
    - cooling_bundle_queue_peak: cooling_bundle_queue_peak result
    - cooling_annex_clear_height: cooling_annex_clear_height result
    - power_supply_building_required_length: power_supply_building_required_length result
    - cooling_link_clear_length: cooling_link_clear_length result
    - initial_clean_required: initial_clean_required result
    - power_supply_building_super_rebar: power_supply_building_super_rebar result
    - capacity_margin_units: capacity_margin_units result
    - cooling_link_sub_rebar: cooling_link_sub_rebar result
    - reactor_hall_clear_area: reactor_hall_clear_area result
    - parcel_fit_margin_m: parcel_fit_margin_m result
    - sector_link_south_gross_area: sector_link_south_gross_area result
    - sector_link_north_super_rebar: sector_link_north_super_rebar result
    - sector_wing_south_super_rebar: sector_wing_south_super_rebar result
    - blanket_packages_required_per_sector: blanket_packages_required_per_sector result
    - cooling_dirty_helium_required: cooling_dirty_helium_required result
    - maintenance_shop_required_height: maintenance_shop_required_height result
    - total_air_volume: total_air_volume result
    - cryo_compressors_clear_length: cryo_compressors_clear_length result
    - service_water_building_required_width: service_water_building_required_width result
    - site_services_building_air_volume: site_services_building_air_volume result
    - sector_link_west_sub_concrete: sector_link_west_sub_concrete result
    - administration_super_rebar: administration_super_rebar result
    - security_super_formwork: security_super_formwork result
    - cryo_coldbox_sub_rebar: cryo_coldbox_sub_rebar result
    - sector_link_south_sub_concrete: sector_link_south_sub_concrete result
    - cooling_clean_bundle_required: cooling_clean_bundle_required result
    - cooling_clean_helium_allocated: cooling_clean_helium_allocated result
    - route_margin_m: route_margin_m result
    - sector_link_west_clear_width: sector_link_west_clear_width result
    - electrical_building_clear_area: electrical_building_clear_area result
    - sector_link_west_super_rebar: sector_link_west_super_rebar result
    - clean_positions_allocated: clean_positions_allocated result
    - cooling_link_sub_formwork: cooling_link_sub_formwork result
    - cryo_coldbox_air_volume: cryo_coldbox_air_volume result
    - cooling_hall_super_rebar: cooling_hall_super_rebar result
    - sector_wing_west_super_formwork: sector_wing_west_super_formwork result
    - reactor_auxiliaries_clear_area: reactor_auxiliaries_clear_area result
    - reactor_auxiliaries_sub_concrete: reactor_auxiliaries_sub_concrete result
    - fuel_building_required_length: fuel_building_required_length result
    - reactor_auxiliaries_sub_rebar: reactor_auxiliaries_sub_rebar result
    - sector_wing_west_sub_concrete: sector_wing_west_sub_concrete result
    - cooling_dirty_bundle_allocated: cooling_dirty_bundle_allocated result
    - cooling_hall_gross_area: cooling_hall_gross_area result
    - sector_link_south_sub_formwork: sector_link_south_sub_formwork result
    - sector_load_qualified: sector_load_qualified result
    - cryo_coldbox_clear_height: cryo_coldbox_clear_height result
    - sector_link_north_sub_formwork: sector_link_north_sub_formwork result
    - sector_wing_south_air_volume: sector_wing_south_air_volume result
    - outage_margin_days: outage_margin_days result
    - sector_wing_north_super_concrete: sector_wing_north_super_concrete result
    - cryo_coldbox_super_concrete: cryo_coldbox_super_concrete result
    - maintenance_shop_gross_area: maintenance_shop_gross_area result
    - site_services_building_required_height: site_services_building_required_height result
    - sector_wing_west_super_rebar: sector_wing_west_super_rebar result
    - sector_wing_north_clear_height: sector_wing_north_clear_height result
    - sector_link_south_super_formwork: sector_link_south_super_formwork result
    - sector_link_west_gross_area: sector_link_west_gross_area result
    - cooling_hall_clear_length: cooling_hall_clear_length result
    - sector_wing_west_required_width: sector_wing_west_required_width result
    - administration_super_concrete: administration_super_concrete result
    - sector_link_north_clear_length: sector_link_north_clear_length result
    - reactor_hall_super_concrete: reactor_hall_super_concrete result
    - administration_sub_formwork: administration_sub_formwork result
    - turbine_hall_sub_rebar: turbine_hall_sub_rebar result
    - site_services_building_clear_length: site_services_building_clear_length result
    - power_supply_building_sub_concrete: power_supply_building_sub_concrete result
    - reactor_hall_air_volume: reactor_hall_air_volume result
    - reactor_auxiliaries_clear_length: reactor_auxiliaries_clear_length result
    - administration_super_formwork: administration_super_formwork result
    - site_services_building_super_formwork: site_services_building_super_formwork result
    - administration_gross_area: administration_gross_area result
    - material_capacity_volume: material_capacity_volume result
    - cooling_annex_clear_width: cooling_annex_clear_width result
    - cooling_link_required_height: cooling_link_required_height result
    - cooling_link_gross_area: cooling_link_gross_area result
    - cost_mode: cost_mode result
    - cooling_clean_helium_required: cooling_clean_helium_required result
    - control_required_area: control_required_area result
    - cooling_link_clear_height: cooling_link_clear_height result
    - maintenance_shop_super_formwork: maintenance_shop_super_formwork result
    - sector_link_east_clear_width: sector_link_east_clear_width result
    - sector_wing_north_clear_width: sector_wing_north_clear_width result
    - maintenance_shop_sub_rebar: maintenance_shop_sub_rebar result
    - total_clear_area: total_clear_area result
    - cryo_compressors_air_volume: cryo_compressors_air_volume result
    - sector_wing_west_required_height: sector_wing_west_required_height result
    - reactor_hall_super_rebar: reactor_hall_super_rebar result
    - cooling_dirty_helium_allocated: cooling_dirty_helium_allocated result
    - sector_link_east_super_concrete: sector_link_east_super_concrete result
    - sector_wing_north_required_length: sector_wing_north_required_length result
    - turbine_hall_air_volume: turbine_hall_air_volume result
    - provisional_room_count: provisional_room_count result
    - sector_wing_south_clear_width: sector_wing_south_clear_width result
    - sector_link_west_required_height: sector_link_west_required_height result
    - sector_wing_south_clear_length: sector_wing_south_clear_length result
    - cooling_hall_sub_formwork: cooling_hall_sub_formwork result
    - cryo_coldbox_sub_concrete: cryo_coldbox_sub_concrete result
    - power_supply_building_super_formwork: power_supply_building_super_formwork result
    - fuel_building_sub_concrete: fuel_building_sub_concrete result
    - sector_link_south_clear_area: sector_link_south_clear_area result
    - security_clear_length: security_clear_length result
    - cooling_link_super_concrete: cooling_link_super_concrete result
    - reactor_auxiliaries_clear_width: reactor_auxiliaries_clear_width result
    - site_services_building_required_length: site_services_building_required_length result
    - cryo_compressors_super_concrete: cryo_compressors_super_concrete result
    - required_parcel_y_min: required_parcel_y_min result
    - sector_wing_east_required_width: sector_wing_east_required_width result
    - cryo_coldbox_gross_area: cryo_coldbox_gross_area result
    - cooling_hall_required_length: cooling_hall_required_length result
    - electrical_building_required_width: electrical_building_required_width result
    - fuel_building_clear_width: fuel_building_clear_width result
    - administration_clear_height: administration_clear_height result
    - security_required_area: security_required_area result
    - service_water_building_gross_area: service_water_building_gross_area result
    - electrical_building_gross_area: electrical_building_gross_area result
    - initial_ready_margin_days: initial_ready_margin_days result
    - power_supply_building_clear_length: power_supply_building_clear_length result
    - cooling_annex_sub_concrete: cooling_annex_sub_concrete result
    - sector_link_west_required_length: sector_link_west_required_length result
    - fuel_building_sub_formwork: fuel_building_sub_formwork result
    - power_supply_building_required_height: power_supply_building_required_height result
    - cooling_clean_bundle_allocated: cooling_clean_bundle_allocated result
    - unused_material_capacity: unused_material_capacity result
    - cooling_hall_sub_concrete: cooling_hall_sub_concrete result
    - maintenance_shop_super_rebar: maintenance_shop_super_rebar result
    - sector_wing_west_gross_area: sector_wing_west_gross_area result
    - service_water_building_air_volume: service_water_building_air_volume result
    - sector_link_north_super_formwork: sector_link_north_super_formwork result
    - sector_wing_south_sub_formwork: sector_wing_south_sub_formwork result
    - reactor_hall_clear_width: reactor_hall_clear_width result
    - sector_height: sector_height result
    - sector_wing_east_super_formwork: sector_wing_east_super_formwork result
    - cooling_link_super_rebar: cooling_link_super_rebar result
    - control_sub_formwork: control_sub_formwork result
    - maintenance_shop_air_volume: maintenance_shop_air_volume result
    - cooling_dirty_salt_required: cooling_dirty_salt_required result
    - control_clear_height: control_clear_height result
    - control_super_concrete: control_super_concrete result
    - cooling_link_super_formwork: cooling_link_super_formwork result
    - sector_link_west_clear_height: sector_link_west_clear_height result
    - electrical_building_super_rebar: electrical_building_super_rebar result
    - cooling_clean_salt_required: cooling_clean_salt_required result
    - electrical_building_clear_length: electrical_building_clear_length result
    - reactor_auxiliaries_required_width: reactor_auxiliaries_required_width result
    - electrical_building_sub_rebar: electrical_building_sub_rebar result
    - security_clear_area: security_clear_area result
    - reactor_hall_super_formwork: reactor_hall_super_formwork result
    - sector_link_west_required_width: sector_link_west_required_width result
    - sector_wing_north_super_formwork: sector_wing_north_super_formwork result

SysML Source: root-0/analyses/mfe_facilities.sysml:3

SysML Source: root-0/analyses/mfe_facilities.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_layout_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.primitives import Float
from stellarator_materials_rebco_tea.schemas.facility_layout_output import Facility_LayoutOutput


class Facility_LayoutInput(BaseModel):
    """Input model for Facility_LayoutModule.

    Attributes:
        selected_site_services_building_height_in: selected_site_services_building_height_in input
        selected_sector_link_east_width_in: selected_sector_link_east_width_in input
        selected_cooling_helium_store_width_in: selected_cooling_helium_store_width_in input
        selected_cooling_bundle_store_width_in: selected_cooling_bundle_store_width_in input
        cooling_dirty_helium_positions_in: cooling_dirty_helium_positions_in input
        salt_package_height_in: salt_package_height_in input
        selected_site_services_building_width_in: selected_site_services_building_width_in input
        selected_sector_wing_south_length_in: selected_sector_wing_south_length_in input
        selected_service_water_building_length_in: selected_service_water_building_length_in input
        dirty_buffer_positions_in: dirty_buffer_positions_in input
        building_separation_in: building_separation_in input
        cooling_internal_move_days_in: cooling_internal_move_days_in input
        cooling_cross_width_in: cooling_cross_width_in input
        provisional_envelope_scale_in: provisional_envelope_scale_in input
        site_services_width_in: site_services_width_in input
        hx_end_allowance_in: hx_end_allowance_in input
        selected_sector_wing_south_width_in: selected_sector_wing_south_width_in input
        selected_fuel_building_width_in: selected_fuel_building_width_in input
        selected_sector_link_south_width_in: selected_sector_link_south_width_in input
        selected_sector_wing_west_width_in: selected_sector_wing_west_width_in input
        selected_sector_wing_east_length_in: selected_sector_wing_east_length_in input
        selected_turbine_hall_height_in: selected_turbine_hall_height_in input
        sector_join_days_in: sector_join_days_in input
        selected_cryo_compressors_length_in: selected_cryo_compressors_length_in input
        cooling_machine_stations_in: cooling_machine_stations_in input
        cooling_prepare_stations_in: cooling_prepare_stations_in input
        reactor_aux_length_in: reactor_aux_length_in input
        selected_parcel_x_min_in: selected_parcel_x_min_in input
        turbine_height_in: turbine_height_in input
        selected_service_water_building_width_in: selected_service_water_building_width_in input
        selected_cryo_coldbox_length_in: selected_cryo_coldbox_length_in input
        calendar_unplanned_in: calendar_unplanned_in input
        selected_cooling_hall_height_in: selected_cooling_hall_height_in input
        n_mod_in: n_mod_in input
        control_area_per_person_in: control_area_per_person_in input
        administration_occupants_in: administration_occupants_in input
        cooling_helium_count_in: cooling_helium_count_in input
        selected_cryo_compressors_width_in: selected_cryo_compressors_width_in input
        selected_cryo_coldbox_height_in: selected_cryo_coldbox_height_in input
        cooling_aisle_width_in: cooling_aisle_width_in input
        selected_cooling_hall_length_in: selected_cooling_hall_length_in input
        sector_service_teams_in: sector_service_teams_in input
        cooling_hold_days_in: cooling_hold_days_in input
        service_water_height_in: service_water_height_in input
        selected_service_water_building_height_in: selected_service_water_building_height_in input
        cooling_dirty_bundle_positions_in: cooling_dirty_bundle_positions_in input
        cooling_clean_salt_positions_in: cooling_clean_salt_positions_in input
        selected_sector_link_west_height_in: selected_sector_link_west_height_in input
        selected_sector_link_east_height_in: selected_sector_link_east_height_in input
        waste_package_yield_in: waste_package_yield_in input
        selected_administration_length_in: selected_administration_length_in input
        cooling_prepare_bundle_days_in: cooling_prepare_bundle_days_in input
        selected_administration_height_in: selected_administration_height_in input
        selected_cryo_coldbox_width_in: selected_cryo_coldbox_width_in input
        sector_headroom_in: sector_headroom_in input
        initial_sector_start_days_in: initial_sector_start_days_in input
        cooling_clean_bundle_positions_in: cooling_clean_bundle_positions_in input
        selected_electrical_building_width_in: selected_electrical_building_width_in input
        selected_power_supply_building_height_in: selected_power_supply_building_height_in input
        hx_tube_length_in: hx_tube_length_in input
        conventional_rebar_density_in: conventional_rebar_density_in input
        selected_sector_wing_west_length_in: selected_sector_wing_west_length_in input
        selected_sector_wing_west_height_in: selected_sector_wing_west_height_in input
        selected_control_length_in: selected_control_length_in input
        power_supply_length_in: power_supply_length_in input
        component_remove_days_in: component_remove_days_in input
        calendar_fluence_in: calendar_fluence_in input
        cryo_coldbox_length_in: cryo_coldbox_length_in input
        administration_area_per_person_in: administration_area_per_person_in input
        selected_sector_wing_north_length_in: selected_sector_wing_north_length_in input
        facilities_cost_mode_in: facilities_cost_mode_in input
        selected_fuel_building_height_in: selected_fuel_building_height_in input
        component_hold_days_in: component_hold_days_in input
        selected_site_services_building_length_in: selected_site_services_building_length_in input
        selected_sector_link_south_length_in: selected_sector_link_south_length_in input
        selected_sector_link_west_length_in: selected_sector_link_west_length_in input
        selected_reactor_auxiliaries_length_in: selected_reactor_auxiliaries_length_in input
        selected_electrical_building_height_in: selected_electrical_building_height_in input
        selected_control_height_in: selected_control_height_in input
        external_access_width_in: external_access_width_in input
        conventional_shop_width_in: conventional_shop_width_in input
        cooling_machine_life_in: cooling_machine_life_in input
        cooling_dirty_salt_positions_in: cooling_dirty_salt_positions_in input
        power_supply_height_in: power_supply_height_in input
        selected_sector_wing_north_width_in: selected_sector_wing_north_width_in input
        security_area_per_person_in: security_area_per_person_in input
        cooling_initial_receipt_lead_days_in: cooling_initial_receipt_lead_days_in input
        service_water_width_in: service_water_width_in input
        selected_cooling_link_height_in: selected_cooling_link_height_in input
        selected_sector_link_west_width_in: selected_sector_link_west_width_in input
        sector_count_in: sector_count_in input
        cooling_bundle_life_in: cooling_bundle_life_in input
        cooling_airlock_length_in: cooling_airlock_length_in input
        fuel_length_in: fuel_length_in input
        heat_rejection_width_in: heat_rejection_width_in input
        cooldown_days_in: cooldown_days_in input
        cryo_coldbox_width_in: cryo_coldbox_width_in input
        cooling_bundle_stations_in: cooling_bundle_stations_in input
        selected_cooling_link_length_in: selected_cooling_link_length_in input
        cooling_headroom_in: cooling_headroom_in input
        sector_clean_days_in: sector_clean_days_in input
        reactor_aux_height_in: reactor_aux_height_in input
        selected_sector_link_north_width_in: selected_sector_link_north_width_in input
        selected_cooling_annex_north_depth_in: selected_cooling_annex_north_depth_in input
        initial_receipt_lead_days_in: initial_receipt_lead_days_in input
        onsite_ac_height_in: onsite_ac_height_in input
        service_water_length_in: service_water_length_in input
        cooling_initial_handoff_days_in: cooling_initial_handoff_days_in input
        occupancy_height_in: occupancy_height_in input
        minor_outer_radius_in: minor_outer_radius_in input
        selected_cryo_compressors_height_in: selected_cryo_compressors_height_in input
        cooling_prepare_machine_days_in: cooling_prepare_machine_days_in input
        helium_package_height_in: helium_package_height_in input
        reactor_aux_width_in: reactor_aux_width_in input
        selected_sector_link_south_height_in: selected_sector_link_south_height_in input
        component_prepare_days_in: component_prepare_days_in input
        selected_cooling_hall_width_in: selected_cooling_hall_width_in input
        selected_parcel_width_in: selected_parcel_width_in input
        selected_control_width_in: selected_control_width_in input
        clean_positions_in: clean_positions_in input
        helium_package_width_in: helium_package_width_in input
        occupancy_circulation_factor_in: occupancy_circulation_factor_in input
        sector_route_clearance_in: sector_route_clearance_in input
        calendar_count_in: calendar_count_in input
        control_occupants_in: control_occupants_in input
        selected_parcel_y_min_in: selected_parcel_y_min_in input
        selected_cooling_annex_height_in: selected_cooling_annex_height_in input
        cooling_salt_count_in: cooling_salt_count_in input
        sector_test_days_in: sector_test_days_in input
        component_width_in: component_width_in input
        selected_maintenance_shop_width_in: selected_maintenance_shop_width_in input
        selected_power_supply_building_width_in: selected_power_supply_building_width_in input
        selected_power_supply_building_length_in: selected_power_supply_building_length_in input
        sector_transport_days_in: sector_transport_days_in input
        nuclear_wall_in: nuclear_wall_in input
        selected_security_length_in: selected_security_length_in input
        conventional_shop_length_in: conventional_shop_length_in input
        sector_bays_in: sector_bays_in input
        selected_reactor_hall_height_in: selected_reactor_hall_height_in input
        selected_maintenance_shop_length_in: selected_maintenance_shop_length_in input
        blanket_volume_in: blanket_volume_in input
        cryo_compressors_length_in: cryo_compressors_length_in input
        cooling_machine_process_days_in: cooling_machine_process_days_in input
        cryo_coldbox_height_in: cryo_coldbox_height_in input
        selected_parcel_length_in: selected_parcel_length_in input
        nuclear_rebar_density_in: nuclear_rebar_density_in input
        selected_cooling_link_width_in: selected_cooling_link_width_in input
        selected_reactor_hall_length_in: selected_reactor_hall_length_in input
        hx_shell_length_in: hx_shell_length_in input
        calendar_mode_in: calendar_mode_in input
        dirty_store_positions_in: dirty_store_positions_in input
        turbine_width_in: turbine_width_in input
        conventional_shop_height_in: conventional_shop_height_in input
        selected_administration_width_in: selected_administration_width_in input
        component_process_days_in: component_process_days_in input
        selected_sector_wing_north_height_in: selected_sector_wing_north_height_in input
        calendar_life_in: calendar_life_in input
        cryo_compressors_height_in: cryo_compressors_height_in input
        cooling_receipt_lead_days_in: cooling_receipt_lead_days_in input
        selected_security_height_in: selected_security_height_in input
        fuel_height_in: fuel_height_in input
        selected_electrical_building_length_in: selected_electrical_building_length_in input
        hx_shell_bore_in: hx_shell_bore_in input
        hx_shell_wall_in: hx_shell_wall_in input
        selected_turbine_hall_length_in: selected_turbine_hall_length_in input
        conventional_floor_in: conventional_floor_in input
        exterior_allowance_in: exterior_allowance_in input
        selected_security_width_in: selected_security_width_in input
        selected_reactor_hall_width_in: selected_reactor_hall_width_in input
        security_occupants_in: security_occupants_in input
        salt_package_width_in: salt_package_width_in input
        selected_sector_link_north_height_in: selected_sector_link_north_height_in input
        selected_turbine_hall_width_in: selected_turbine_hall_width_in input
        selected_fuel_building_length_in: selected_fuel_building_length_in input
        sector_split_days_in: sector_split_days_in input
        selected_blanket_packages_per_sector_in: selected_blanket_packages_per_sector_in input
        onsite_ac_width_in: onsite_ac_width_in input
        recommission_days_in: recommission_days_in input
        salt_package_length_in: salt_package_length_in input
        selected_maintenance_shop_height_in: selected_maintenance_shop_height_in input
        component_install_days_in: component_install_days_in input
        calendar_availability_in: calendar_availability_in input
        helium_package_length_in: helium_package_length_in input
        selected_reactor_auxiliaries_width_in: selected_reactor_auxiliaries_width_in input
        divertor_packages_per_sector_in: divertor_packages_per_sector_in input
        selected_sector_wing_east_width_in: selected_sector_wing_east_width_in input
        cooling_package_margin_in: cooling_package_margin_in input
        component_receipt_lead_days_in: component_receipt_lead_days_in input
        cooling_bundle_count_in: cooling_bundle_count_in input
        cooling_clean_helium_positions_in: cooling_clean_helium_positions_in input
        nuclear_roof_in: nuclear_roof_in input
        cryo_compressors_width_in: cryo_compressors_width_in input
        component_height_in: component_height_in input
        nuclear_floor_in: nuclear_floor_in input
        turbine_length_in: turbine_length_in input
        selected_reactor_auxiliaries_height_in: selected_reactor_auxiliaries_height_in input
        heat_rejection_length_in: heat_rejection_length_in input
        major_radius_in: major_radius_in input
        conventional_roof_in: conventional_roof_in input
        component_length_in: component_length_in input
        conventional_wall_in: conventional_wall_in input
        calendar_years_in: calendar_years_in input
        facilities_enabled_in: facilities_enabled_in input
        cooling_field_cycle_days_in: cooling_field_cycle_days_in input
        selected_cooling_salt_store_width_in: selected_cooling_salt_store_width_in input
        component_handling_margin_in: component_handling_margin_in input
        cooling_bundle_process_days_in: cooling_bundle_process_days_in input
        calendar_outage_in: calendar_outage_in input
        cooling_circuits_in: cooling_circuits_in input
        site_services_length_in: site_services_length_in input
        selected_sector_link_east_length_in: selected_sector_link_east_length_in input
        fuel_width_in: fuel_width_in input
        selected_sector_wing_south_height_in: selected_sector_wing_south_height_in input
        site_services_height_in: site_services_height_in input
        selected_sector_link_north_length_in: selected_sector_link_north_length_in input
        selected_cooling_annex_length_in: selected_cooling_annex_length_in input
        component_material_fraction_in: component_material_fraction_in input
        selected_sector_wing_east_height_in: selected_sector_wing_east_height_in input
        calendar_q_in: calendar_q_in input
        power_supply_width_in: power_supply_width_in input
        onsite_ac_length_in: onsite_ac_length_in input
        selected_cooling_annex_width_in: selected_cooling_annex_width_in input
    """
    selected_site_services_building_height_in: float = Field(..., description="selected_site_services_building_height_in input")
    selected_sector_link_east_width_in: float = Field(..., description="selected_sector_link_east_width_in input")
    selected_cooling_helium_store_width_in: float = Field(..., description="selected_cooling_helium_store_width_in input")
    selected_cooling_bundle_store_width_in: float = Field(..., description="selected_cooling_bundle_store_width_in input")
    cooling_dirty_helium_positions_in: float = Field(..., description="cooling_dirty_helium_positions_in input")
    salt_package_height_in: float = Field(..., description="salt_package_height_in input")
    selected_site_services_building_width_in: float = Field(..., description="selected_site_services_building_width_in input")
    selected_sector_wing_south_length_in: float = Field(..., description="selected_sector_wing_south_length_in input")
    selected_service_water_building_length_in: float = Field(..., description="selected_service_water_building_length_in input")
    dirty_buffer_positions_in: float = Field(..., description="dirty_buffer_positions_in input")
    building_separation_in: float = Field(..., description="building_separation_in input")
    cooling_internal_move_days_in: float = Field(..., description="cooling_internal_move_days_in input")
    cooling_cross_width_in: float = Field(..., description="cooling_cross_width_in input")
    provisional_envelope_scale_in: float = Field(..., description="provisional_envelope_scale_in input")
    site_services_width_in: float = Field(..., description="site_services_width_in input")
    hx_end_allowance_in: float = Field(..., description="hx_end_allowance_in input")
    selected_sector_wing_south_width_in: float = Field(..., description="selected_sector_wing_south_width_in input")
    selected_fuel_building_width_in: float = Field(..., description="selected_fuel_building_width_in input")
    selected_sector_link_south_width_in: float = Field(..., description="selected_sector_link_south_width_in input")
    selected_sector_wing_west_width_in: float = Field(..., description="selected_sector_wing_west_width_in input")
    selected_sector_wing_east_length_in: float = Field(..., description="selected_sector_wing_east_length_in input")
    selected_turbine_hall_height_in: float = Field(..., description="selected_turbine_hall_height_in input")
    sector_join_days_in: float = Field(..., description="sector_join_days_in input")
    selected_cryo_compressors_length_in: float = Field(..., description="selected_cryo_compressors_length_in input")
    cooling_machine_stations_in: float = Field(..., description="cooling_machine_stations_in input")
    cooling_prepare_stations_in: float = Field(..., description="cooling_prepare_stations_in input")
    reactor_aux_length_in: float = Field(..., description="reactor_aux_length_in input")
    selected_parcel_x_min_in: float = Field(..., description="selected_parcel_x_min_in input")
    turbine_height_in: float = Field(..., description="turbine_height_in input")
    selected_service_water_building_width_in: float = Field(..., description="selected_service_water_building_width_in input")
    selected_cryo_coldbox_length_in: float = Field(..., description="selected_cryo_coldbox_length_in input")
    calendar_unplanned_in: float = Field(..., description="calendar_unplanned_in input")
    selected_cooling_hall_height_in: float = Field(..., description="selected_cooling_hall_height_in input")
    n_mod_in: float = Field(..., description="n_mod_in input")
    control_area_per_person_in: float = Field(..., description="control_area_per_person_in input")
    administration_occupants_in: float = Field(..., description="administration_occupants_in input")
    cooling_helium_count_in: float = Field(..., description="cooling_helium_count_in input")
    selected_cryo_compressors_width_in: float = Field(..., description="selected_cryo_compressors_width_in input")
    selected_cryo_coldbox_height_in: float = Field(..., description="selected_cryo_coldbox_height_in input")
    cooling_aisle_width_in: float = Field(..., description="cooling_aisle_width_in input")
    selected_cooling_hall_length_in: float = Field(..., description="selected_cooling_hall_length_in input")
    sector_service_teams_in: float = Field(..., description="sector_service_teams_in input")
    cooling_hold_days_in: float = Field(..., description="cooling_hold_days_in input")
    service_water_height_in: float = Field(..., description="service_water_height_in input")
    selected_service_water_building_height_in: float = Field(..., description="selected_service_water_building_height_in input")
    cooling_dirty_bundle_positions_in: float = Field(..., description="cooling_dirty_bundle_positions_in input")
    cooling_clean_salt_positions_in: float = Field(..., description="cooling_clean_salt_positions_in input")
    selected_sector_link_west_height_in: float = Field(..., description="selected_sector_link_west_height_in input")
    selected_sector_link_east_height_in: float = Field(..., description="selected_sector_link_east_height_in input")
    waste_package_yield_in: float = Field(..., description="waste_package_yield_in input")
    selected_administration_length_in: float = Field(..., description="selected_administration_length_in input")
    cooling_prepare_bundle_days_in: float = Field(..., description="cooling_prepare_bundle_days_in input")
    selected_administration_height_in: float = Field(..., description="selected_administration_height_in input")
    selected_cryo_coldbox_width_in: float = Field(..., description="selected_cryo_coldbox_width_in input")
    sector_headroom_in: float = Field(..., description="sector_headroom_in input")
    initial_sector_start_days_in: float = Field(..., description="initial_sector_start_days_in input")
    cooling_clean_bundle_positions_in: float = Field(..., description="cooling_clean_bundle_positions_in input")
    selected_electrical_building_width_in: float = Field(..., description="selected_electrical_building_width_in input")
    selected_power_supply_building_height_in: float = Field(..., description="selected_power_supply_building_height_in input")
    hx_tube_length_in: float = Field(..., description="hx_tube_length_in input")
    conventional_rebar_density_in: float = Field(..., description="conventional_rebar_density_in input")
    selected_sector_wing_west_length_in: float = Field(..., description="selected_sector_wing_west_length_in input")
    selected_sector_wing_west_height_in: float = Field(..., description="selected_sector_wing_west_height_in input")
    selected_control_length_in: float = Field(..., description="selected_control_length_in input")
    power_supply_length_in: float = Field(..., description="power_supply_length_in input")
    component_remove_days_in: float = Field(..., description="component_remove_days_in input")
    calendar_fluence_in: float = Field(..., description="calendar_fluence_in input")
    cryo_coldbox_length_in: float = Field(..., description="cryo_coldbox_length_in input")
    administration_area_per_person_in: float = Field(..., description="administration_area_per_person_in input")
    selected_sector_wing_north_length_in: float = Field(..., description="selected_sector_wing_north_length_in input")
    facilities_cost_mode_in: float = Field(..., description="facilities_cost_mode_in input")
    selected_fuel_building_height_in: float = Field(..., description="selected_fuel_building_height_in input")
    component_hold_days_in: float = Field(..., description="component_hold_days_in input")
    selected_site_services_building_length_in: float = Field(..., description="selected_site_services_building_length_in input")
    selected_sector_link_south_length_in: float = Field(..., description="selected_sector_link_south_length_in input")
    selected_sector_link_west_length_in: float = Field(..., description="selected_sector_link_west_length_in input")
    selected_reactor_auxiliaries_length_in: float = Field(..., description="selected_reactor_auxiliaries_length_in input")
    selected_electrical_building_height_in: float = Field(..., description="selected_electrical_building_height_in input")
    selected_control_height_in: float = Field(..., description="selected_control_height_in input")
    external_access_width_in: float = Field(..., description="external_access_width_in input")
    conventional_shop_width_in: float = Field(..., description="conventional_shop_width_in input")
    cooling_machine_life_in: float = Field(..., description="cooling_machine_life_in input")
    cooling_dirty_salt_positions_in: float = Field(..., description="cooling_dirty_salt_positions_in input")
    power_supply_height_in: float = Field(..., description="power_supply_height_in input")
    selected_sector_wing_north_width_in: float = Field(..., description="selected_sector_wing_north_width_in input")
    security_area_per_person_in: float = Field(..., description="security_area_per_person_in input")
    cooling_initial_receipt_lead_days_in: float = Field(..., description="cooling_initial_receipt_lead_days_in input")
    service_water_width_in: float = Field(..., description="service_water_width_in input")
    selected_cooling_link_height_in: float = Field(..., description="selected_cooling_link_height_in input")
    selected_sector_link_west_width_in: float = Field(..., description="selected_sector_link_west_width_in input")
    sector_count_in: float = Field(..., description="sector_count_in input")
    cooling_bundle_life_in: float = Field(..., description="cooling_bundle_life_in input")
    cooling_airlock_length_in: float = Field(..., description="cooling_airlock_length_in input")
    fuel_length_in: float = Field(..., description="fuel_length_in input")
    heat_rejection_width_in: float = Field(..., description="heat_rejection_width_in input")
    cooldown_days_in: float = Field(..., description="cooldown_days_in input")
    cryo_coldbox_width_in: float = Field(..., description="cryo_coldbox_width_in input")
    cooling_bundle_stations_in: float = Field(..., description="cooling_bundle_stations_in input")
    selected_cooling_link_length_in: float = Field(..., description="selected_cooling_link_length_in input")
    cooling_headroom_in: float = Field(..., description="cooling_headroom_in input")
    sector_clean_days_in: float = Field(..., description="sector_clean_days_in input")
    reactor_aux_height_in: float = Field(..., description="reactor_aux_height_in input")
    selected_sector_link_north_width_in: float = Field(..., description="selected_sector_link_north_width_in input")
    selected_cooling_annex_north_depth_in: float = Field(..., description="selected_cooling_annex_north_depth_in input")
    initial_receipt_lead_days_in: float = Field(..., description="initial_receipt_lead_days_in input")
    onsite_ac_height_in: float = Field(..., description="onsite_ac_height_in input")
    service_water_length_in: float = Field(..., description="service_water_length_in input")
    cooling_initial_handoff_days_in: float = Field(..., description="cooling_initial_handoff_days_in input")
    occupancy_height_in: float = Field(..., description="occupancy_height_in input")
    minor_outer_radius_in: float = Field(..., description="minor_outer_radius_in input")
    selected_cryo_compressors_height_in: float = Field(..., description="selected_cryo_compressors_height_in input")
    cooling_prepare_machine_days_in: float = Field(..., description="cooling_prepare_machine_days_in input")
    helium_package_height_in: float = Field(..., description="helium_package_height_in input")
    reactor_aux_width_in: float = Field(..., description="reactor_aux_width_in input")
    selected_sector_link_south_height_in: float = Field(..., description="selected_sector_link_south_height_in input")
    component_prepare_days_in: float = Field(..., description="component_prepare_days_in input")
    selected_cooling_hall_width_in: float = Field(..., description="selected_cooling_hall_width_in input")
    selected_parcel_width_in: float = Field(..., description="selected_parcel_width_in input")
    selected_control_width_in: float = Field(..., description="selected_control_width_in input")
    clean_positions_in: float = Field(..., description="clean_positions_in input")
    helium_package_width_in: float = Field(..., description="helium_package_width_in input")
    occupancy_circulation_factor_in: float = Field(..., description="occupancy_circulation_factor_in input")
    sector_route_clearance_in: float = Field(..., description="sector_route_clearance_in input")
    calendar_count_in: float = Field(..., description="calendar_count_in input")
    control_occupants_in: float = Field(..., description="control_occupants_in input")
    selected_parcel_y_min_in: float = Field(..., description="selected_parcel_y_min_in input")
    selected_cooling_annex_height_in: float = Field(..., description="selected_cooling_annex_height_in input")
    cooling_salt_count_in: float = Field(..., description="cooling_salt_count_in input")
    sector_test_days_in: float = Field(..., description="sector_test_days_in input")
    component_width_in: float = Field(..., description="component_width_in input")
    selected_maintenance_shop_width_in: float = Field(..., description="selected_maintenance_shop_width_in input")
    selected_power_supply_building_width_in: float = Field(..., description="selected_power_supply_building_width_in input")
    selected_power_supply_building_length_in: float = Field(..., description="selected_power_supply_building_length_in input")
    sector_transport_days_in: float = Field(..., description="sector_transport_days_in input")
    nuclear_wall_in: float = Field(..., description="nuclear_wall_in input")
    selected_security_length_in: float = Field(..., description="selected_security_length_in input")
    conventional_shop_length_in: float = Field(..., description="conventional_shop_length_in input")
    sector_bays_in: float = Field(..., description="sector_bays_in input")
    selected_reactor_hall_height_in: float = Field(..., description="selected_reactor_hall_height_in input")
    selected_maintenance_shop_length_in: float = Field(..., description="selected_maintenance_shop_length_in input")
    blanket_volume_in: float = Field(..., description="blanket_volume_in input")
    cryo_compressors_length_in: float = Field(..., description="cryo_compressors_length_in input")
    cooling_machine_process_days_in: float = Field(..., description="cooling_machine_process_days_in input")
    cryo_coldbox_height_in: float = Field(..., description="cryo_coldbox_height_in input")
    selected_parcel_length_in: float = Field(..., description="selected_parcel_length_in input")
    nuclear_rebar_density_in: float = Field(..., description="nuclear_rebar_density_in input")
    selected_cooling_link_width_in: float = Field(..., description="selected_cooling_link_width_in input")
    selected_reactor_hall_length_in: float = Field(..., description="selected_reactor_hall_length_in input")
    hx_shell_length_in: float = Field(..., description="hx_shell_length_in input")
    calendar_mode_in: float = Field(..., description="calendar_mode_in input")
    dirty_store_positions_in: float = Field(..., description="dirty_store_positions_in input")
    turbine_width_in: float = Field(..., description="turbine_width_in input")
    conventional_shop_height_in: float = Field(..., description="conventional_shop_height_in input")
    selected_administration_width_in: float = Field(..., description="selected_administration_width_in input")
    component_process_days_in: float = Field(..., description="component_process_days_in input")
    selected_sector_wing_north_height_in: float = Field(..., description="selected_sector_wing_north_height_in input")
    calendar_life_in: float = Field(..., description="calendar_life_in input")
    cryo_compressors_height_in: float = Field(..., description="cryo_compressors_height_in input")
    cooling_receipt_lead_days_in: float = Field(..., description="cooling_receipt_lead_days_in input")
    selected_security_height_in: float = Field(..., description="selected_security_height_in input")
    fuel_height_in: float = Field(..., description="fuel_height_in input")
    selected_electrical_building_length_in: float = Field(..., description="selected_electrical_building_length_in input")
    hx_shell_bore_in: float = Field(..., description="hx_shell_bore_in input")
    hx_shell_wall_in: float = Field(..., description="hx_shell_wall_in input")
    selected_turbine_hall_length_in: float = Field(..., description="selected_turbine_hall_length_in input")
    conventional_floor_in: float = Field(..., description="conventional_floor_in input")
    exterior_allowance_in: float = Field(..., description="exterior_allowance_in input")
    selected_security_width_in: float = Field(..., description="selected_security_width_in input")
    selected_reactor_hall_width_in: float = Field(..., description="selected_reactor_hall_width_in input")
    security_occupants_in: float = Field(..., description="security_occupants_in input")
    salt_package_width_in: float = Field(..., description="salt_package_width_in input")
    selected_sector_link_north_height_in: float = Field(..., description="selected_sector_link_north_height_in input")
    selected_turbine_hall_width_in: float = Field(..., description="selected_turbine_hall_width_in input")
    selected_fuel_building_length_in: float = Field(..., description="selected_fuel_building_length_in input")
    sector_split_days_in: float = Field(..., description="sector_split_days_in input")
    selected_blanket_packages_per_sector_in: float = Field(..., description="selected_blanket_packages_per_sector_in input")
    onsite_ac_width_in: float = Field(..., description="onsite_ac_width_in input")
    recommission_days_in: float = Field(..., description="recommission_days_in input")
    salt_package_length_in: float = Field(..., description="salt_package_length_in input")
    selected_maintenance_shop_height_in: float = Field(..., description="selected_maintenance_shop_height_in input")
    component_install_days_in: float = Field(..., description="component_install_days_in input")
    calendar_availability_in: float = Field(..., description="calendar_availability_in input")
    helium_package_length_in: float = Field(..., description="helium_package_length_in input")
    selected_reactor_auxiliaries_width_in: float = Field(..., description="selected_reactor_auxiliaries_width_in input")
    divertor_packages_per_sector_in: float = Field(..., description="divertor_packages_per_sector_in input")
    selected_sector_wing_east_width_in: float = Field(..., description="selected_sector_wing_east_width_in input")
    cooling_package_margin_in: float = Field(..., description="cooling_package_margin_in input")
    component_receipt_lead_days_in: float = Field(..., description="component_receipt_lead_days_in input")
    cooling_bundle_count_in: float = Field(..., description="cooling_bundle_count_in input")
    cooling_clean_helium_positions_in: float = Field(..., description="cooling_clean_helium_positions_in input")
    nuclear_roof_in: float = Field(..., description="nuclear_roof_in input")
    cryo_compressors_width_in: float = Field(..., description="cryo_compressors_width_in input")
    component_height_in: float = Field(..., description="component_height_in input")
    nuclear_floor_in: float = Field(..., description="nuclear_floor_in input")
    turbine_length_in: float = Field(..., description="turbine_length_in input")
    selected_reactor_auxiliaries_height_in: float = Field(..., description="selected_reactor_auxiliaries_height_in input")
    heat_rejection_length_in: float = Field(..., description="heat_rejection_length_in input")
    major_radius_in: float = Field(..., description="major_radius_in input")
    conventional_roof_in: float = Field(..., description="conventional_roof_in input")
    component_length_in: float = Field(..., description="component_length_in input")
    conventional_wall_in: float = Field(..., description="conventional_wall_in input")
    calendar_years_in: float = Field(..., description="calendar_years_in input")
    facilities_enabled_in: bool = Field(..., description="facilities_enabled_in input")
    cooling_field_cycle_days_in: float = Field(..., description="cooling_field_cycle_days_in input")
    selected_cooling_salt_store_width_in: float = Field(..., description="selected_cooling_salt_store_width_in input")
    component_handling_margin_in: float = Field(..., description="component_handling_margin_in input")
    cooling_bundle_process_days_in: float = Field(..., description="cooling_bundle_process_days_in input")
    calendar_outage_in: float = Field(..., description="calendar_outage_in input")
    cooling_circuits_in: float = Field(..., description="cooling_circuits_in input")
    site_services_length_in: float = Field(..., description="site_services_length_in input")
    selected_sector_link_east_length_in: float = Field(..., description="selected_sector_link_east_length_in input")
    fuel_width_in: float = Field(..., description="fuel_width_in input")
    selected_sector_wing_south_height_in: float = Field(..., description="selected_sector_wing_south_height_in input")
    site_services_height_in: float = Field(..., description="site_services_height_in input")
    selected_sector_link_north_length_in: float = Field(..., description="selected_sector_link_north_length_in input")
    selected_cooling_annex_length_in: float = Field(..., description="selected_cooling_annex_length_in input")
    component_material_fraction_in: float = Field(..., description="component_material_fraction_in input")
    selected_sector_wing_east_height_in: float = Field(..., description="selected_sector_wing_east_height_in input")
    calendar_q_in: float = Field(..., description="calendar_q_in input")
    power_supply_width_in: float = Field(..., description="power_supply_width_in input")
    onsite_ac_length_in: float = Field(..., description="onsite_ac_length_in input")
    selected_cooling_annex_width_in: float = Field(..., description="selected_cooling_annex_width_in input")


class Facility_LayoutModule(ModuleBase[Facility_LayoutInput, Facility_LayoutOutput]):
    """TEAx module for Facility_Layout calculation.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Manual completion reuses the live calendar and emits the declared finite scalar contract; deterministic ledgers are diagnostics.

Inputs:
    - selected_site_services_building_height_in: selected_site_services_building_height_in parameter
    - selected_sector_link_east_width_in: selected_sector_link_east_width_in parameter
    - selected_cooling_helium_store_width_in: selected_cooling_helium_store_width_in parameter
    - selected_cooling_bundle_store_width_in: selected_cooling_bundle_store_width_in parameter
    - cooling_dirty_helium_positions_in: cooling_dirty_helium_positions_in parameter
    - salt_package_height_in: salt_package_height_in parameter
    - selected_site_services_building_width_in: selected_site_services_building_width_in parameter
    - selected_sector_wing_south_length_in: selected_sector_wing_south_length_in parameter
    - selected_service_water_building_length_in: selected_service_water_building_length_in parameter
    - dirty_buffer_positions_in: dirty_buffer_positions_in parameter
    - building_separation_in: building_separation_in parameter
    - cooling_internal_move_days_in: cooling_internal_move_days_in parameter
    - cooling_cross_width_in: cooling_cross_width_in parameter
    - provisional_envelope_scale_in: provisional_envelope_scale_in parameter
    - site_services_width_in: site_services_width_in parameter
    - hx_end_allowance_in: hx_end_allowance_in parameter
    - selected_sector_wing_south_width_in: selected_sector_wing_south_width_in parameter
    - selected_fuel_building_width_in: selected_fuel_building_width_in parameter
    - selected_sector_link_south_width_in: selected_sector_link_south_width_in parameter
    - selected_sector_wing_west_width_in: selected_sector_wing_west_width_in parameter
    - selected_sector_wing_east_length_in: selected_sector_wing_east_length_in parameter
    - selected_turbine_hall_height_in: selected_turbine_hall_height_in parameter
    - sector_join_days_in: sector_join_days_in parameter
    - selected_cryo_compressors_length_in: selected_cryo_compressors_length_in parameter
    - cooling_machine_stations_in: cooling_machine_stations_in parameter
    - cooling_prepare_stations_in: cooling_prepare_stations_in parameter
    - reactor_aux_length_in: reactor_aux_length_in parameter
    - selected_parcel_x_min_in: selected_parcel_x_min_in parameter
    - turbine_height_in: turbine_height_in parameter
    - selected_service_water_building_width_in: selected_service_water_building_width_in parameter
    - selected_cryo_coldbox_length_in: selected_cryo_coldbox_length_in parameter
    - calendar_unplanned_in: calendar_unplanned_in parameter
    - selected_cooling_hall_height_in: selected_cooling_hall_height_in parameter
    - n_mod_in: n_mod_in parameter
    - control_area_per_person_in: control_area_per_person_in parameter
    - administration_occupants_in: administration_occupants_in parameter
    - cooling_helium_count_in: cooling_helium_count_in parameter
    - selected_cryo_compressors_width_in: selected_cryo_compressors_width_in parameter
    - selected_cryo_coldbox_height_in: selected_cryo_coldbox_height_in parameter
    - cooling_aisle_width_in: cooling_aisle_width_in parameter
    - selected_cooling_hall_length_in: selected_cooling_hall_length_in parameter
    - sector_service_teams_in: sector_service_teams_in parameter
    - cooling_hold_days_in: cooling_hold_days_in parameter
    - service_water_height_in: service_water_height_in parameter
    - selected_service_water_building_height_in: selected_service_water_building_height_in parameter
    - cooling_dirty_bundle_positions_in: cooling_dirty_bundle_positions_in parameter
    - cooling_clean_salt_positions_in: cooling_clean_salt_positions_in parameter
    - selected_sector_link_west_height_in: selected_sector_link_west_height_in parameter
    - selected_sector_link_east_height_in: selected_sector_link_east_height_in parameter
    - waste_package_yield_in: waste_package_yield_in parameter
    - selected_administration_length_in: selected_administration_length_in parameter
    - cooling_prepare_bundle_days_in: cooling_prepare_bundle_days_in parameter
    - selected_administration_height_in: selected_administration_height_in parameter
    - selected_cryo_coldbox_width_in: selected_cryo_coldbox_width_in parameter
    - sector_headroom_in: sector_headroom_in parameter
    - initial_sector_start_days_in: initial_sector_start_days_in parameter
    - cooling_clean_bundle_positions_in: cooling_clean_bundle_positions_in parameter
    - selected_electrical_building_width_in: selected_electrical_building_width_in parameter
    - selected_power_supply_building_height_in: selected_power_supply_building_height_in parameter
    - hx_tube_length_in: hx_tube_length_in parameter
    - conventional_rebar_density_in: conventional_rebar_density_in parameter
    - selected_sector_wing_west_length_in: selected_sector_wing_west_length_in parameter
    - selected_sector_wing_west_height_in: selected_sector_wing_west_height_in parameter
    - selected_control_length_in: selected_control_length_in parameter
    - power_supply_length_in: power_supply_length_in parameter
    - component_remove_days_in: component_remove_days_in parameter
    - calendar_fluence_in: calendar_fluence_in parameter
    - cryo_coldbox_length_in: cryo_coldbox_length_in parameter
    - administration_area_per_person_in: administration_area_per_person_in parameter
    - selected_sector_wing_north_length_in: selected_sector_wing_north_length_in parameter
    - facilities_cost_mode_in: facilities_cost_mode_in parameter
    - selected_fuel_building_height_in: selected_fuel_building_height_in parameter
    - component_hold_days_in: component_hold_days_in parameter
    - selected_site_services_building_length_in: selected_site_services_building_length_in parameter
    - selected_sector_link_south_length_in: selected_sector_link_south_length_in parameter
    - selected_sector_link_west_length_in: selected_sector_link_west_length_in parameter
    - selected_reactor_auxiliaries_length_in: selected_reactor_auxiliaries_length_in parameter
    - selected_electrical_building_height_in: selected_electrical_building_height_in parameter
    - selected_control_height_in: selected_control_height_in parameter
    - external_access_width_in: external_access_width_in parameter
    - conventional_shop_width_in: conventional_shop_width_in parameter
    - cooling_machine_life_in: cooling_machine_life_in parameter
    - cooling_dirty_salt_positions_in: cooling_dirty_salt_positions_in parameter
    - power_supply_height_in: power_supply_height_in parameter
    - selected_sector_wing_north_width_in: selected_sector_wing_north_width_in parameter
    - security_area_per_person_in: security_area_per_person_in parameter
    - cooling_initial_receipt_lead_days_in: cooling_initial_receipt_lead_days_in parameter
    - service_water_width_in: service_water_width_in parameter
    - selected_cooling_link_height_in: selected_cooling_link_height_in parameter
    - selected_sector_link_west_width_in: selected_sector_link_west_width_in parameter
    - sector_count_in: sector_count_in parameter
    - cooling_bundle_life_in: cooling_bundle_life_in parameter
    - cooling_airlock_length_in: cooling_airlock_length_in parameter
    - fuel_length_in: fuel_length_in parameter
    - heat_rejection_width_in: heat_rejection_width_in parameter
    - cooldown_days_in: cooldown_days_in parameter
    - cryo_coldbox_width_in: cryo_coldbox_width_in parameter
    - cooling_bundle_stations_in: cooling_bundle_stations_in parameter
    - selected_cooling_link_length_in: selected_cooling_link_length_in parameter
    - cooling_headroom_in: cooling_headroom_in parameter
    - sector_clean_days_in: sector_clean_days_in parameter
    - reactor_aux_height_in: reactor_aux_height_in parameter
    - selected_sector_link_north_width_in: selected_sector_link_north_width_in parameter
    - selected_cooling_annex_north_depth_in: selected_cooling_annex_north_depth_in parameter
    - initial_receipt_lead_days_in: initial_receipt_lead_days_in parameter
    - onsite_ac_height_in: onsite_ac_height_in parameter
    - service_water_length_in: service_water_length_in parameter
    - cooling_initial_handoff_days_in: cooling_initial_handoff_days_in parameter
    - occupancy_height_in: occupancy_height_in parameter
    - minor_outer_radius_in: minor_outer_radius_in parameter
    - selected_cryo_compressors_height_in: selected_cryo_compressors_height_in parameter
    - cooling_prepare_machine_days_in: cooling_prepare_machine_days_in parameter
    - helium_package_height_in: helium_package_height_in parameter
    - reactor_aux_width_in: reactor_aux_width_in parameter
    - selected_sector_link_south_height_in: selected_sector_link_south_height_in parameter
    - component_prepare_days_in: component_prepare_days_in parameter
    - selected_cooling_hall_width_in: selected_cooling_hall_width_in parameter
    - selected_parcel_width_in: selected_parcel_width_in parameter
    - selected_control_width_in: selected_control_width_in parameter
    - clean_positions_in: clean_positions_in parameter
    - helium_package_width_in: helium_package_width_in parameter
    - occupancy_circulation_factor_in: occupancy_circulation_factor_in parameter
    - sector_route_clearance_in: sector_route_clearance_in parameter
    - calendar_count_in: calendar_count_in parameter
    - control_occupants_in: control_occupants_in parameter
    - selected_parcel_y_min_in: selected_parcel_y_min_in parameter
    - selected_cooling_annex_height_in: selected_cooling_annex_height_in parameter
    - cooling_salt_count_in: cooling_salt_count_in parameter
    - sector_test_days_in: sector_test_days_in parameter
    - component_width_in: component_width_in parameter
    - selected_maintenance_shop_width_in: selected_maintenance_shop_width_in parameter
    - selected_power_supply_building_width_in: selected_power_supply_building_width_in parameter
    - selected_power_supply_building_length_in: selected_power_supply_building_length_in parameter
    - sector_transport_days_in: sector_transport_days_in parameter
    - nuclear_wall_in: nuclear_wall_in parameter
    - selected_security_length_in: selected_security_length_in parameter
    - conventional_shop_length_in: conventional_shop_length_in parameter
    - sector_bays_in: sector_bays_in parameter
    - selected_reactor_hall_height_in: selected_reactor_hall_height_in parameter
    - selected_maintenance_shop_length_in: selected_maintenance_shop_length_in parameter
    - blanket_volume_in: blanket_volume_in parameter
    - cryo_compressors_length_in: cryo_compressors_length_in parameter
    - cooling_machine_process_days_in: cooling_machine_process_days_in parameter
    - cryo_coldbox_height_in: cryo_coldbox_height_in parameter
    - selected_parcel_length_in: selected_parcel_length_in parameter
    - nuclear_rebar_density_in: nuclear_rebar_density_in parameter
    - selected_cooling_link_width_in: selected_cooling_link_width_in parameter
    - selected_reactor_hall_length_in: selected_reactor_hall_length_in parameter
    - hx_shell_length_in: hx_shell_length_in parameter
    - calendar_mode_in: calendar_mode_in parameter
    - dirty_store_positions_in: dirty_store_positions_in parameter
    - turbine_width_in: turbine_width_in parameter
    - conventional_shop_height_in: conventional_shop_height_in parameter
    - selected_administration_width_in: selected_administration_width_in parameter
    - component_process_days_in: component_process_days_in parameter
    - selected_sector_wing_north_height_in: selected_sector_wing_north_height_in parameter
    - calendar_life_in: calendar_life_in parameter
    - cryo_compressors_height_in: cryo_compressors_height_in parameter
    - cooling_receipt_lead_days_in: cooling_receipt_lead_days_in parameter
    - selected_security_height_in: selected_security_height_in parameter
    - fuel_height_in: fuel_height_in parameter
    - selected_electrical_building_length_in: selected_electrical_building_length_in parameter
    - hx_shell_bore_in: hx_shell_bore_in parameter
    - hx_shell_wall_in: hx_shell_wall_in parameter
    - selected_turbine_hall_length_in: selected_turbine_hall_length_in parameter
    - conventional_floor_in: conventional_floor_in parameter
    - exterior_allowance_in: exterior_allowance_in parameter
    - selected_security_width_in: selected_security_width_in parameter
    - selected_reactor_hall_width_in: selected_reactor_hall_width_in parameter
    - security_occupants_in: security_occupants_in parameter
    - salt_package_width_in: salt_package_width_in parameter
    - selected_sector_link_north_height_in: selected_sector_link_north_height_in parameter
    - selected_turbine_hall_width_in: selected_turbine_hall_width_in parameter
    - selected_fuel_building_length_in: selected_fuel_building_length_in parameter
    - sector_split_days_in: sector_split_days_in parameter
    - selected_blanket_packages_per_sector_in: selected_blanket_packages_per_sector_in parameter
    - onsite_ac_width_in: onsite_ac_width_in parameter
    - recommission_days_in: recommission_days_in parameter
    - salt_package_length_in: salt_package_length_in parameter
    - selected_maintenance_shop_height_in: selected_maintenance_shop_height_in parameter
    - component_install_days_in: component_install_days_in parameter
    - calendar_availability_in: calendar_availability_in parameter
    - helium_package_length_in: helium_package_length_in parameter
    - selected_reactor_auxiliaries_width_in: selected_reactor_auxiliaries_width_in parameter
    - divertor_packages_per_sector_in: divertor_packages_per_sector_in parameter
    - selected_sector_wing_east_width_in: selected_sector_wing_east_width_in parameter
    - cooling_package_margin_in: cooling_package_margin_in parameter
    - component_receipt_lead_days_in: component_receipt_lead_days_in parameter
    - cooling_bundle_count_in: cooling_bundle_count_in parameter
    - cooling_clean_helium_positions_in: cooling_clean_helium_positions_in parameter
    - nuclear_roof_in: nuclear_roof_in parameter
    - cryo_compressors_width_in: cryo_compressors_width_in parameter
    - component_height_in: component_height_in parameter
    - nuclear_floor_in: nuclear_floor_in parameter
    - turbine_length_in: turbine_length_in parameter
    - selected_reactor_auxiliaries_height_in: selected_reactor_auxiliaries_height_in parameter
    - heat_rejection_length_in: heat_rejection_length_in parameter
    - major_radius_in: major_radius_in parameter
    - conventional_roof_in: conventional_roof_in parameter
    - component_length_in: component_length_in parameter
    - conventional_wall_in: conventional_wall_in parameter
    - calendar_years_in: calendar_years_in parameter
    - facilities_enabled_in: facilities_enabled_in parameter
    - cooling_field_cycle_days_in: cooling_field_cycle_days_in parameter
    - selected_cooling_salt_store_width_in: selected_cooling_salt_store_width_in parameter
    - component_handling_margin_in: component_handling_margin_in parameter
    - cooling_bundle_process_days_in: cooling_bundle_process_days_in parameter
    - calendar_outage_in: calendar_outage_in parameter
    - cooling_circuits_in: cooling_circuits_in parameter
    - site_services_length_in: site_services_length_in parameter
    - selected_sector_link_east_length_in: selected_sector_link_east_length_in parameter
    - fuel_width_in: fuel_width_in parameter
    - selected_sector_wing_south_height_in: selected_sector_wing_south_height_in parameter
    - site_services_height_in: site_services_height_in parameter
    - selected_sector_link_north_length_in: selected_sector_link_north_length_in parameter
    - selected_cooling_annex_length_in: selected_cooling_annex_length_in parameter
    - component_material_fraction_in: component_material_fraction_in parameter
    - selected_sector_wing_east_height_in: selected_sector_wing_east_height_in parameter
    - calendar_q_in: calendar_q_in parameter
    - power_supply_width_in: power_supply_width_in parameter
    - onsite_ac_length_in: onsite_ac_length_in parameter
    - selected_cooling_annex_width_in: selected_cooling_annex_width_in parameter

Outputs:
    - dirty_store_required: dirty_store_required result
    - electrical_building_required_length: electrical_building_required_length result
    - sector_link_north_clear_height: sector_link_north_clear_height result
    - reactor_auxiliaries_sub_formwork: reactor_auxiliaries_sub_formwork result
    - electrical_building_clear_height: electrical_building_clear_height result
    - dirty_store_positions_allocated: dirty_store_positions_allocated result
    - sector_wing_west_required_length: sector_wing_west_required_length result
    - cryo_compressors_sub_formwork: cryo_compressors_sub_formwork result
    - sector_wing_east_clear_length: sector_wing_east_clear_length result
    - sector_wing_east_super_rebar: sector_wing_east_super_rebar result
    - fuel_building_air_volume: fuel_building_air_volume result
    - turbine_hall_super_formwork: turbine_hall_super_formwork result
    - sector_link_north_clear_width: sector_link_north_clear_width result
    - sector_wing_north_required_width: sector_wing_north_required_width result
    - power_supply_building_clear_area: power_supply_building_clear_area result
    - control_required_height: control_required_height result
    - cooling_hall_clear_height: cooling_hall_clear_height result
    - administration_sub_concrete: administration_sub_concrete result
    - sector_wing_north_gross_area: sector_wing_north_gross_area result
    - administration_required_area: administration_required_area result
    - fuel_building_sub_rebar: fuel_building_sub_rebar result
    - sector_link_south_required_height: sector_link_south_required_height result
    - dirty_buffer_positions_allocated: dirty_buffer_positions_allocated result
    - sector_link_north_super_concrete: sector_link_north_super_concrete result
    - sector_wing_west_clear_length: sector_wing_west_clear_length result
    - cryo_coldbox_required_height: cryo_coldbox_required_height result
    - fuel_building_required_width: fuel_building_required_width result
    - required_parcel_x_min: required_parcel_x_min result
    - sector_wing_south_super_formwork: sector_wing_south_super_formwork result
    - control_clear_width: control_clear_width result
    - sector_link_north_gross_area: sector_link_north_gross_area result
    - electrical_building_super_formwork: electrical_building_super_formwork result
    - cooling_annex_gross_area: cooling_annex_gross_area result
    - replacement_ready_margin_days: replacement_ready_margin_days result
    - cooling_annex_sub_formwork: cooling_annex_sub_formwork result
    - maintenance_shop_clear_area: maintenance_shop_clear_area result
    - reactor_hall_gross_area: reactor_hall_gross_area result
    - control_air_volume: control_air_volume result
    - sector_wing_south_required_length: sector_wing_south_required_length result
    - site_services_building_sub_rebar: site_services_building_sub_rebar result
    - calendar_first_event_year: calendar_first_event_year result
    - site_services_building_super_concrete: site_services_building_super_concrete result
    - reactor_auxiliaries_gross_area: reactor_auxiliaries_gross_area result
    - reactor_hall_required_height: reactor_hall_required_height result
    - service_water_building_clear_height: service_water_building_clear_height result
    - sector_link_south_required_width: sector_link_south_required_width result
    - sector_link_west_clear_area: sector_link_west_clear_area result
    - occupancy_area_margin_m2: occupancy_area_margin_m2 result
    - power_supply_building_gross_area: power_supply_building_gross_area result
    - electrical_building_super_concrete: electrical_building_super_concrete result
    - required_parcel_y_max: required_parcel_y_max result
    - sector_link_south_super_concrete: sector_link_south_super_concrete result
    - site_services_building_sub_concrete: site_services_building_sub_concrete result
    - sector_link_south_sub_rebar: sector_link_south_sub_rebar result
    - cryo_compressors_clear_area: cryo_compressors_clear_area result
    - electrical_building_clear_width: electrical_building_clear_width result
    - sector_wing_east_super_concrete: sector_wing_east_super_concrete result
    - cooling_carrier_moves: cooling_carrier_moves result
    - cryo_coldbox_super_rebar: cryo_coldbox_super_rebar result
    - cryo_coldbox_super_formwork: cryo_coldbox_super_formwork result
    - cryo_coldbox_sub_formwork: cryo_coldbox_sub_formwork result
    - sector_wing_east_sub_rebar: sector_wing_east_sub_rebar result
    - power_supply_building_sub_rebar: power_supply_building_sub_rebar result
    - sector_link_south_clear_height: sector_link_south_clear_height result
    - dirty_buffer_required: dirty_buffer_required result
    - cooling_jobs_after_shutdown: cooling_jobs_after_shutdown result
    - service_water_building_super_rebar: service_water_building_super_rebar result
    - fuel_building_clear_area: fuel_building_clear_area result
    - cooling_link_clear_width: cooling_link_clear_width result
    - cooling_annex_super_formwork: cooling_annex_super_formwork result
    - site_services_building_required_width: site_services_building_required_width result
    - cooling_annex_required_height: cooling_annex_required_height result
    - reactor_auxiliaries_super_formwork: reactor_auxiliaries_super_formwork result
    - reactor_hall_clear_height: reactor_hall_clear_height result
    - sector_link_north_air_volume: sector_link_north_air_volume result
    - sector_wing_south_required_width: sector_wing_south_required_width result
    - control_sub_rebar: control_sub_rebar result
    - service_water_building_clear_area: service_water_building_clear_area result
    - sector_wing_west_clear_height: sector_wing_west_clear_height result
    - sector_wing_south_sub_rebar: sector_wing_south_sub_rebar result
    - sector_wing_south_required_height: sector_wing_south_required_height result
    - sector_link_west_super_concrete: sector_link_west_super_concrete result
    - administration_sub_rebar: administration_sub_rebar result
    - cooling_hall_clear_width: cooling_hall_clear_width result
    - exterior_envelope_qualified: exterior_envelope_qualified result
    - outage_required_days: outage_required_days result
    - security_clear_width: security_clear_width result
    - fuel_building_super_formwork: fuel_building_super_formwork result
    - power_supply_building_clear_width: power_supply_building_clear_width result
    - service_water_building_sub_concrete: service_water_building_sub_concrete result
    - cryo_compressors_super_formwork: cryo_compressors_super_formwork result
    - cryo_coldbox_clear_length: cryo_coldbox_clear_length result
    - cryo_compressors_required_length: cryo_compressors_required_length result
    - control_clear_length: control_clear_length result
    - calendar_last_event_year: calendar_last_event_year result
    - turbine_hall_clear_width: turbine_hall_clear_width result
    - controlled_air_volume: controlled_air_volume result
    - service_water_building_required_length: service_water_building_required_length result
    - cooling_replacement_ready_margin_days: cooling_replacement_ready_margin_days result
    - sector_link_west_air_volume: sector_link_west_air_volume result
    - sector_link_north_clear_area: sector_link_north_clear_area result
    - maintenance_shop_clear_length: maintenance_shop_clear_length result
    - blanket_packages_per_sector: blanket_packages_per_sector result
    - maintenance_shop_clear_height: maintenance_shop_clear_height result
    - cooling_hall_super_formwork: cooling_hall_super_formwork result
    - maintenance_shop_required_width: maintenance_shop_required_width result
    - sector_link_east_clear_area: sector_link_east_clear_area result
    - sector_wing_north_super_rebar: sector_wing_north_super_rebar result
    - turbine_hall_clear_height: turbine_hall_clear_height result
    - sector_width: sector_width result
    - service_water_building_clear_length: service_water_building_clear_length result
    - active: active result
    - maintenance_shop_sub_formwork: maintenance_shop_sub_formwork result
    - sector_wing_west_air_volume: sector_wing_west_air_volume result
    - site_services_building_clear_width: site_services_building_clear_width result
    - reactor_auxiliaries_required_height: reactor_auxiliaries_required_height result
    - cryo_compressors_sub_rebar: cryo_compressors_sub_rebar result
    - cooling_link_required_length: cooling_link_required_length result
    - sector_wing_north_sub_formwork: sector_wing_north_sub_formwork result
    - power_supply_building_required_width: power_supply_building_required_width result
    - sector_wing_west_super_concrete: sector_wing_west_super_concrete result
    - electrical_building_sub_formwork: electrical_building_sub_formwork result
    - turbine_hall_required_height: turbine_hall_required_height result
    - cryo_coldbox_clear_width: cryo_coldbox_clear_width result
    - sector_wing_east_sub_formwork: sector_wing_east_sub_formwork result
    - reactor_auxiliaries_air_volume: reactor_auxiliaries_air_volume result
    - sector_link_east_sub_rebar: sector_link_east_sub_rebar result
    - cooling_link_sub_concrete: cooling_link_sub_concrete result
    - security_required_height: security_required_height result
    - sector_wing_east_clear_area: sector_wing_east_clear_area result
    - site_services_building_clear_area: site_services_building_clear_area result
    - sector_link_north_required_height: sector_link_north_required_height result
    - cooling_annex_super_rebar: cooling_annex_super_rebar result
    - power_supply_building_sub_formwork: power_supply_building_sub_formwork result
    - cooling_link_air_volume: cooling_link_air_volume result
    - cryo_compressors_clear_height: cryo_compressors_clear_height result
    - maintenance_shop_super_concrete: maintenance_shop_super_concrete result
    - cooling_hall_sub_rebar: cooling_hall_sub_rebar result
    - sector_wing_east_sub_concrete: sector_wing_east_sub_concrete result
    - cooling_helium_queue_peak: cooling_helium_queue_peak result
    - fuel_building_clear_height: fuel_building_clear_height result
    - service_water_building_clear_width: service_water_building_clear_width result
    - sector_link_south_required_length: sector_link_south_required_length result
    - administration_clear_area: administration_clear_area result
    - cryo_coldbox_required_width: cryo_coldbox_required_width result
    - cooling_link_clear_area: cooling_link_clear_area result
    - site_services_building_sub_formwork: site_services_building_sub_formwork result
    - turbine_hall_super_rebar: turbine_hall_super_rebar result
    - cooling_salt_queue_peak: cooling_salt_queue_peak result
    - sector_link_south_air_volume: sector_link_south_air_volume result
    - cooling_dirty_bundle_required: cooling_dirty_bundle_required result
    - sector_wing_east_clear_width: sector_wing_east_clear_width result
    - sector_link_east_super_formwork: sector_link_east_super_formwork result
    - security_air_volume: security_air_volume result
    - reactor_auxiliaries_super_rebar: reactor_auxiliaries_super_rebar result
    - service_water_building_super_formwork: service_water_building_super_formwork result
    - reactor_hall_clear_length: reactor_hall_clear_length result
    - reactor_hall_sub_formwork: reactor_hall_sub_formwork result
    - sector_link_east_required_length: sector_link_east_required_length result
    - cooling_hall_clear_area: cooling_hall_clear_area result
    - sector_wing_west_sub_rebar: sector_wing_west_sub_rebar result
    - administration_air_volume: administration_air_volume result
    - turbine_hall_clear_length: turbine_hall_clear_length result
    - sector_link_south_clear_length: sector_link_south_clear_length result
    - sector_wing_east_clear_height: sector_wing_east_clear_height result
    - turbine_hall_clear_area: turbine_hall_clear_area result
    - sector_link_east_required_height: sector_link_east_required_height result
    - sector_wing_west_sub_formwork: sector_wing_west_sub_formwork result
    - service_water_building_required_height: service_water_building_required_height result
    - sector_link_south_super_rebar: sector_link_south_super_rebar result
    - control_gross_area: control_gross_area result
    - fuel_building_gross_area: fuel_building_gross_area result
    - sector_length: sector_length result
    - cooling_annex_sub_rebar: cooling_annex_sub_rebar result
    - cooling_annex_clear_area: cooling_annex_clear_area result
    - calendar_event_count: calendar_event_count result
    - sector_link_west_sub_formwork: sector_link_west_sub_formwork result
    - sector_wing_west_clear_width: sector_wing_west_clear_width result
    - security_sub_concrete: security_sub_concrete result
    - fuel_building_super_concrete: fuel_building_super_concrete result
    - cooling_clean_salt_allocated: cooling_clean_salt_allocated result
    - cryo_compressors_gross_area: cryo_compressors_gross_area result
    - sector_link_east_clear_length: sector_link_east_clear_length result
    - cooling_annex_air_volume: cooling_annex_air_volume result
    - cryo_coldbox_clear_area: cryo_coldbox_clear_area result
    - sector_wing_south_gross_area: sector_wing_south_gross_area result
    - cooling_outage_basis_resolved: cooling_outage_basis_resolved result
    - turbine_hall_required_width: turbine_hall_required_width result
    - sector_wing_north_clear_length: sector_wing_north_clear_length result
    - cryo_compressors_required_height: cryo_compressors_required_height result
    - turbine_hall_sub_concrete: turbine_hall_sub_concrete result
    - contamination_procedure_qualified: contamination_procedure_qualified result
    - cooling_hall_super_concrete: cooling_hall_super_concrete result
    - turbine_hall_super_concrete: turbine_hall_super_concrete result
    - control_super_rebar: control_super_rebar result
    - sector_link_north_sub_rebar: sector_link_north_sub_rebar result
    - maintenance_shop_sub_concrete: maintenance_shop_sub_concrete result
    - sector_link_south_clear_width: sector_link_south_clear_width result
    - parcel_area: parcel_area result
    - sector_wing_south_super_concrete: sector_wing_south_super_concrete result
    - cryo_coldbox_required_length: cryo_coldbox_required_length result
    - administration_clear_length: administration_clear_length result
    - sector_link_east_air_volume: sector_link_east_air_volume result
    - security_clear_height: security_clear_height result
    - sector_wing_south_clear_height: sector_wing_south_clear_height result
    - reactor_auxiliaries_clear_height: reactor_auxiliaries_clear_height result
    - packages_per_sector: packages_per_sector result
    - security_sub_rebar: security_sub_rebar result
    - maintenance_shop_required_length: maintenance_shop_required_length result
    - administration_required_height: administration_required_height result
    - sector_link_east_sub_concrete: sector_link_east_sub_concrete result
    - sector_wing_east_gross_area: sector_wing_east_gross_area result
    - sector_link_east_super_rebar: sector_link_east_super_rebar result
    - fuel_building_clear_length: fuel_building_clear_length result
    - security_super_rebar: security_super_rebar result
    - cryo_compressors_sub_concrete: cryo_compressors_sub_concrete result
    - service_water_building_super_concrete: service_water_building_super_concrete result
    - reactor_hall_sub_concrete: reactor_hall_sub_concrete result
    - service_water_building_sub_formwork: service_water_building_sub_formwork result
    - sector_link_east_sub_formwork: sector_link_east_sub_formwork result
    - security_sub_formwork: security_sub_formwork result
    - security_super_concrete: security_super_concrete result
    - sector_wing_west_clear_area: sector_wing_west_clear_area result
    - cryo_compressors_super_rebar: cryo_compressors_super_rebar result
    - control_clear_area: control_clear_area result
    - cooling_annex_super_concrete: cooling_annex_super_concrete result
    - control_super_formwork: control_super_formwork result
    - turbine_hall_sub_formwork: turbine_hall_sub_formwork result
    - electrical_building_air_volume: electrical_building_air_volume result
    - cooling_hall_air_volume: cooling_hall_air_volume result
    - sector_link_west_sub_rebar: sector_link_west_sub_rebar result
    - cooling_hall_required_height: cooling_hall_required_height result
    - sector_wing_east_air_volume: sector_wing_east_air_volume result
    - sector_wing_south_clear_area: sector_wing_south_clear_area result
    - sector_link_east_gross_area: sector_link_east_gross_area result
    - cooling_link_required_width: cooling_link_required_width result
    - outage_allowed_days: outage_allowed_days result
    - cooling_annex_clear_length: cooling_annex_clear_length result
    - sector_wing_north_sub_rebar: sector_wing_north_sub_rebar result
    - sector_link_west_super_formwork: sector_link_west_super_formwork result
    - initial_margin_days: initial_margin_days result
    - sector_wing_east_required_height: sector_wing_east_required_height result
    - sector_wing_east_required_length: sector_wing_east_required_length result
    - service_water_building_sub_rebar: service_water_building_sub_rebar result
    - site_services_building_clear_height: site_services_building_clear_height result
    - administration_clear_width: administration_clear_width result
    - maintenance_shop_clear_width: maintenance_shop_clear_width result
    - cooling_last_release_year: cooling_last_release_year result
    - sector_wing_north_required_height: sector_wing_north_required_height result
    - power_supply_building_clear_height: power_supply_building_clear_height result
    - reactor_hall_required_length: reactor_hall_required_length result
    - cooling_dirty_salt_allocated: cooling_dirty_salt_allocated result
    - reactor_hall_sub_rebar: reactor_hall_sub_rebar result
    - sector_link_east_clear_height: sector_link_east_clear_height result
    - cooling_hall_required_width: cooling_hall_required_width result
    - site_services_building_super_rebar: site_services_building_super_rebar result
    - sector_link_north_required_width: sector_link_north_required_width result
    - cryo_compressors_clear_width: cryo_compressors_clear_width result
    - turbine_hall_gross_area: turbine_hall_gross_area result
    - reactor_hall_required_width: reactor_hall_required_width result
    - sector_link_north_required_length: sector_link_north_required_length result
    - sector_link_west_clear_length: sector_link_west_clear_length result
    - control_sub_concrete: control_sub_concrete result
    - power_supply_building_super_concrete: power_supply_building_super_concrete result
    - electrical_building_required_height: electrical_building_required_height result
    - reactor_auxiliaries_super_concrete: reactor_auxiliaries_super_concrete result
    - site_services_building_gross_area: site_services_building_gross_area result
    - reactor_auxiliaries_required_length: reactor_auxiliaries_required_length result
    - fuel_building_super_rebar: fuel_building_super_rebar result
    - fuel_building_required_height: fuel_building_required_height result
    - cooling_initial_ready_margin_days: cooling_initial_ready_margin_days result
    - sector_link_east_required_width: sector_link_east_required_width result
    - electrical_building_sub_concrete: electrical_building_sub_concrete result
    - security_gross_area: security_gross_area result
    - sector_link_north_sub_concrete: sector_link_north_sub_concrete result
    - sector_wing_south_sub_concrete: sector_wing_south_sub_concrete result
    - cooling_annex_required_length: cooling_annex_required_length result
    - turbine_hall_required_length: turbine_hall_required_length result
    - geometry_fit_margin_m: geometry_fit_margin_m result
    - readiness_margin_days: readiness_margin_days result
    - sector_wing_north_air_volume: sector_wing_north_air_volume result
    - power_supply_building_air_volume: power_supply_building_air_volume result
    - total_gross_area: total_gross_area result
    - sector_wing_north_sub_concrete: sector_wing_north_sub_concrete result
    - cooling_annex_required_width: cooling_annex_required_width result
    - cryo_compressors_required_width: cryo_compressors_required_width result
    - required_parcel_x_max: required_parcel_x_max result
    - sector_wing_north_clear_area: sector_wing_north_clear_area result
    - cooling_bundle_queue_peak: cooling_bundle_queue_peak result
    - cooling_annex_clear_height: cooling_annex_clear_height result
    - power_supply_building_required_length: power_supply_building_required_length result
    - cooling_link_clear_length: cooling_link_clear_length result
    - initial_clean_required: initial_clean_required result
    - power_supply_building_super_rebar: power_supply_building_super_rebar result
    - capacity_margin_units: capacity_margin_units result
    - cooling_link_sub_rebar: cooling_link_sub_rebar result
    - reactor_hall_clear_area: reactor_hall_clear_area result
    - parcel_fit_margin_m: parcel_fit_margin_m result
    - sector_link_south_gross_area: sector_link_south_gross_area result
    - sector_link_north_super_rebar: sector_link_north_super_rebar result
    - sector_wing_south_super_rebar: sector_wing_south_super_rebar result
    - blanket_packages_required_per_sector: blanket_packages_required_per_sector result
    - cooling_dirty_helium_required: cooling_dirty_helium_required result
    - maintenance_shop_required_height: maintenance_shop_required_height result
    - total_air_volume: total_air_volume result
    - cryo_compressors_clear_length: cryo_compressors_clear_length result
    - service_water_building_required_width: service_water_building_required_width result
    - site_services_building_air_volume: site_services_building_air_volume result
    - sector_link_west_sub_concrete: sector_link_west_sub_concrete result
    - administration_super_rebar: administration_super_rebar result
    - security_super_formwork: security_super_formwork result
    - cryo_coldbox_sub_rebar: cryo_coldbox_sub_rebar result
    - sector_link_south_sub_concrete: sector_link_south_sub_concrete result
    - cooling_clean_bundle_required: cooling_clean_bundle_required result
    - cooling_clean_helium_allocated: cooling_clean_helium_allocated result
    - route_margin_m: route_margin_m result
    - sector_link_west_clear_width: sector_link_west_clear_width result
    - electrical_building_clear_area: electrical_building_clear_area result
    - sector_link_west_super_rebar: sector_link_west_super_rebar result
    - clean_positions_allocated: clean_positions_allocated result
    - cooling_link_sub_formwork: cooling_link_sub_formwork result
    - cryo_coldbox_air_volume: cryo_coldbox_air_volume result
    - cooling_hall_super_rebar: cooling_hall_super_rebar result
    - sector_wing_west_super_formwork: sector_wing_west_super_formwork result
    - reactor_auxiliaries_clear_area: reactor_auxiliaries_clear_area result
    - reactor_auxiliaries_sub_concrete: reactor_auxiliaries_sub_concrete result
    - fuel_building_required_length: fuel_building_required_length result
    - reactor_auxiliaries_sub_rebar: reactor_auxiliaries_sub_rebar result
    - sector_wing_west_sub_concrete: sector_wing_west_sub_concrete result
    - cooling_dirty_bundle_allocated: cooling_dirty_bundle_allocated result
    - cooling_hall_gross_area: cooling_hall_gross_area result
    - sector_link_south_sub_formwork: sector_link_south_sub_formwork result
    - sector_load_qualified: sector_load_qualified result
    - cryo_coldbox_clear_height: cryo_coldbox_clear_height result
    - sector_link_north_sub_formwork: sector_link_north_sub_formwork result
    - sector_wing_south_air_volume: sector_wing_south_air_volume result
    - outage_margin_days: outage_margin_days result
    - sector_wing_north_super_concrete: sector_wing_north_super_concrete result
    - cryo_coldbox_super_concrete: cryo_coldbox_super_concrete result
    - maintenance_shop_gross_area: maintenance_shop_gross_area result
    - site_services_building_required_height: site_services_building_required_height result
    - sector_wing_west_super_rebar: sector_wing_west_super_rebar result
    - sector_wing_north_clear_height: sector_wing_north_clear_height result
    - sector_link_south_super_formwork: sector_link_south_super_formwork result
    - sector_link_west_gross_area: sector_link_west_gross_area result
    - cooling_hall_clear_length: cooling_hall_clear_length result
    - sector_wing_west_required_width: sector_wing_west_required_width result
    - administration_super_concrete: administration_super_concrete result
    - sector_link_north_clear_length: sector_link_north_clear_length result
    - reactor_hall_super_concrete: reactor_hall_super_concrete result
    - administration_sub_formwork: administration_sub_formwork result
    - turbine_hall_sub_rebar: turbine_hall_sub_rebar result
    - site_services_building_clear_length: site_services_building_clear_length result
    - power_supply_building_sub_concrete: power_supply_building_sub_concrete result
    - reactor_hall_air_volume: reactor_hall_air_volume result
    - reactor_auxiliaries_clear_length: reactor_auxiliaries_clear_length result
    - administration_super_formwork: administration_super_formwork result
    - site_services_building_super_formwork: site_services_building_super_formwork result
    - administration_gross_area: administration_gross_area result
    - material_capacity_volume: material_capacity_volume result
    - cooling_annex_clear_width: cooling_annex_clear_width result
    - cooling_link_required_height: cooling_link_required_height result
    - cooling_link_gross_area: cooling_link_gross_area result
    - cost_mode: cost_mode result
    - cooling_clean_helium_required: cooling_clean_helium_required result
    - control_required_area: control_required_area result
    - cooling_link_clear_height: cooling_link_clear_height result
    - maintenance_shop_super_formwork: maintenance_shop_super_formwork result
    - sector_link_east_clear_width: sector_link_east_clear_width result
    - sector_wing_north_clear_width: sector_wing_north_clear_width result
    - maintenance_shop_sub_rebar: maintenance_shop_sub_rebar result
    - total_clear_area: total_clear_area result
    - cryo_compressors_air_volume: cryo_compressors_air_volume result
    - sector_wing_west_required_height: sector_wing_west_required_height result
    - reactor_hall_super_rebar: reactor_hall_super_rebar result
    - cooling_dirty_helium_allocated: cooling_dirty_helium_allocated result
    - sector_link_east_super_concrete: sector_link_east_super_concrete result
    - sector_wing_north_required_length: sector_wing_north_required_length result
    - turbine_hall_air_volume: turbine_hall_air_volume result
    - provisional_room_count: provisional_room_count result
    - sector_wing_south_clear_width: sector_wing_south_clear_width result
    - sector_link_west_required_height: sector_link_west_required_height result
    - sector_wing_south_clear_length: sector_wing_south_clear_length result
    - cooling_hall_sub_formwork: cooling_hall_sub_formwork result
    - cryo_coldbox_sub_concrete: cryo_coldbox_sub_concrete result
    - power_supply_building_super_formwork: power_supply_building_super_formwork result
    - fuel_building_sub_concrete: fuel_building_sub_concrete result
    - sector_link_south_clear_area: sector_link_south_clear_area result
    - security_clear_length: security_clear_length result
    - cooling_link_super_concrete: cooling_link_super_concrete result
    - reactor_auxiliaries_clear_width: reactor_auxiliaries_clear_width result
    - site_services_building_required_length: site_services_building_required_length result
    - cryo_compressors_super_concrete: cryo_compressors_super_concrete result
    - required_parcel_y_min: required_parcel_y_min result
    - sector_wing_east_required_width: sector_wing_east_required_width result
    - cryo_coldbox_gross_area: cryo_coldbox_gross_area result
    - cooling_hall_required_length: cooling_hall_required_length result
    - electrical_building_required_width: electrical_building_required_width result
    - fuel_building_clear_width: fuel_building_clear_width result
    - administration_clear_height: administration_clear_height result
    - security_required_area: security_required_area result
    - service_water_building_gross_area: service_water_building_gross_area result
    - electrical_building_gross_area: electrical_building_gross_area result
    - initial_ready_margin_days: initial_ready_margin_days result
    - power_supply_building_clear_length: power_supply_building_clear_length result
    - cooling_annex_sub_concrete: cooling_annex_sub_concrete result
    - sector_link_west_required_length: sector_link_west_required_length result
    - fuel_building_sub_formwork: fuel_building_sub_formwork result
    - power_supply_building_required_height: power_supply_building_required_height result
    - cooling_clean_bundle_allocated: cooling_clean_bundle_allocated result
    - unused_material_capacity: unused_material_capacity result
    - cooling_hall_sub_concrete: cooling_hall_sub_concrete result
    - maintenance_shop_super_rebar: maintenance_shop_super_rebar result
    - sector_wing_west_gross_area: sector_wing_west_gross_area result
    - service_water_building_air_volume: service_water_building_air_volume result
    - sector_link_north_super_formwork: sector_link_north_super_formwork result
    - sector_wing_south_sub_formwork: sector_wing_south_sub_formwork result
    - reactor_hall_clear_width: reactor_hall_clear_width result
    - sector_height: sector_height result
    - sector_wing_east_super_formwork: sector_wing_east_super_formwork result
    - cooling_link_super_rebar: cooling_link_super_rebar result
    - control_sub_formwork: control_sub_formwork result
    - maintenance_shop_air_volume: maintenance_shop_air_volume result
    - cooling_dirty_salt_required: cooling_dirty_salt_required result
    - control_clear_height: control_clear_height result
    - control_super_concrete: control_super_concrete result
    - cooling_link_super_formwork: cooling_link_super_formwork result
    - sector_link_west_clear_height: sector_link_west_clear_height result
    - electrical_building_super_rebar: electrical_building_super_rebar result
    - cooling_clean_salt_required: cooling_clean_salt_required result
    - electrical_building_clear_length: electrical_building_clear_length result
    - reactor_auxiliaries_required_width: reactor_auxiliaries_required_width result
    - electrical_building_sub_rebar: electrical_building_sub_rebar result
    - security_clear_area: security_clear_area result
    - reactor_hall_super_formwork: reactor_hall_super_formwork result
    - sector_link_west_required_width: sector_link_west_required_width result
    - sector_wing_north_super_formwork: sector_wing_north_super_formwork result

SysML Source: root-0/analyses/mfe_facilities.sysml:3

    SysML Source: root-0/analyses/mfe_facilities.sysml:3

    Calculation Specification:
        facilities_enabled_in = false
        facilities_cost_mode_in = 0.0
        sector_count_in = 4.0
        sector_bays_in = 4.0
        sector_service_teams_in = 2.0
        exterior_allowance_in = 2.0
        sector_route_clearance_in = 6.0
        sector_headroom_in = 3.0
        component_width_in = 4.0
        component_height_in = 2.0
        component_length_in = 2.0
        component_handling_margin_in = 0.5
        component_material_fraction_in = 0.5
        divertor_packages_per_sector_in = 4.0
        waste_package_yield_in = 1.0
        component_remove_days_in = 0.5
        component_install_days_in = 0.5
        sector_clean_days_in = 7.0
        sector_test_days_in = 7.0
        sector_split_days_in = 7.0
        sector_join_days_in = 7.0
        sector_transport_days_in = 2.0
        cooldown_days_in = 30.0
        recommission_days_in = 30.0
        initial_receipt_lead_days_in = 180.0
        initial_sector_start_days_in = -120.0
        component_receipt_lead_days_in = 90.0
        component_prepare_days_in = 1.0
        component_process_days_in = 1.0
        component_hold_days_in = 365.25
        clean_positions_in = 36.0
        dirty_buffer_positions_in = 18.0
        dirty_store_positions_in = 36.0
        cooling_initial_receipt_lead_days_in = 180.0
        cooling_initial_handoff_days_in = -30.0
        cooling_receipt_lead_days_in = 90.0
        cooling_hold_days_in = 365.25
        cooling_prepare_stations_in = 2.0
        cooling_machine_stations_in = 2.0
        cooling_bundle_stations_in = 2.0
        cooling_prepare_machine_days_in = 0.5
        cooling_prepare_bundle_days_in = 1.0
        cooling_machine_process_days_in = 2.0
        cooling_bundle_process_days_in = 5.0
        cooling_field_cycle_days_in = 0.2
        cooling_internal_move_days_in = 0.1
        cooling_clean_helium_positions_in = 29.0
        cooling_clean_salt_positions_in = 29.0
        cooling_clean_bundle_positions_in = 14.0
        cooling_dirty_helium_positions_in = 28.0
        cooling_dirty_salt_positions_in = 28.0
        cooling_dirty_bundle_positions_in = 14.0
        helium_package_length_in = 6.0
        helium_package_width_in = 3.0
        helium_package_height_in = 4.0
        salt_package_length_in = 3.0
        salt_package_width_in = 2.0
        salt_package_height_in = 3.0
        hx_end_allowance_in = 2.0
        cooling_package_margin_in = 1.0
        cooling_aisle_width_in = 6.0
        cooling_cross_width_in = 17.0
        cooling_headroom_in = 9.0
        cooling_airlock_length_in = 17.0
        nuclear_wall_in = 2.0
        nuclear_floor_in = 1.0
        nuclear_roof_in = 1.0
        nuclear_rebar_density_in = 150.0
        conventional_wall_in = 0.3
        conventional_floor_in = 0.3
        conventional_roof_in = 0.2
        conventional_rebar_density_in = 100.0
        building_separation_in = 10.0
        external_access_width_in = 12.0
        provisional_envelope_scale_in = 1.0
        administration_occupants_in = 200.0
        control_occupants_in = 30.0
        security_occupants_in = 10.0
        administration_area_per_person_in = 12.0
        control_area_per_person_in = 15.0
        security_area_per_person_in = 12.0
        occupancy_circulation_factor_in = 1.3
        occupancy_height_in = 4.0
        heat_rejection_length_in = 100.0
        heat_rejection_width_in = 60.0
        turbine_length_in = 60.0
        turbine_width_in = 20.0
        turbine_height_in = 15.0
        cryo_coldbox_length_in = 20.0
        cryo_coldbox_width_in = 12.0
        cryo_coldbox_height_in = 10.0
        cryo_compressors_length_in = 30.0
        cryo_compressors_width_in = 12.0
        cryo_compressors_height_in = 8.0
        fuel_length_in = 30.0
        fuel_width_in = 20.0
        fuel_height_in = 8.0
        reactor_aux_length_in = 30.0
        reactor_aux_width_in = 20.0
        reactor_aux_height_in = 10.0
        power_supply_length_in = 20.0
        power_supply_width_in = 10.0
        power_supply_height_in = 8.0
        onsite_ac_length_in = 16.0
        onsite_ac_width_in = 8.0
        onsite_ac_height_in = 6.0
        service_water_length_in = 20.0
        service_water_width_in = 15.0
        service_water_height_in = 8.0
        conventional_shop_length_in = 20.0
        conventional_shop_width_in = 15.0
        conventional_shop_height_in = 8.0
        site_services_length_in = 20.0
        site_services_width_in = 10.0
        site_services_height_in = 6.0
        n_mod_in = 0.0
        major_radius_in = 0.0
        minor_outer_radius_in = 0.0
        blanket_volume_in = 0.0
        calendar_q_in = 0.0
        calendar_fluence_in = 0.0
        calendar_years_in = 0.0
        calendar_outage_in = 0.0
        calendar_unplanned_in = 0.0
        calendar_mode_in = 0.0
        calendar_life_in = 0.0
        calendar_count_in = 0.0
        calendar_availability_in = 0.0
        cooling_circuits_in = 0.0
        cooling_helium_count_in = 0.0
        cooling_salt_count_in = 0.0
        cooling_bundle_count_in = 0.0
        cooling_machine_life_in = 0.0
        cooling_bundle_life_in = 0.0
        hx_shell_bore_in = 0.0
        hx_shell_wall_in = 0.0
        hx_shell_length_in = 0.0
        hx_tube_length_in = 0.0
        selected_reactor_hall_length_in = 0.0
        selected_reactor_hall_width_in = 0.0
        selected_reactor_hall_height_in = 0.0
        selected_sector_wing_east_length_in = 0.0
        selected_sector_wing_east_width_in = 0.0
        selected_sector_wing_east_height_in = 0.0
        selected_sector_wing_north_length_in = 0.0
        selected_sector_wing_north_width_in = 0.0
        selected_sector_wing_north_height_in = 0.0
        selected_sector_wing_west_length_in = 0.0
        selected_sector_wing_west_width_in = 0.0
        selected_sector_wing_west_height_in = 0.0
        selected_sector_wing_south_length_in = 0.0
        selected_sector_wing_south_width_in = 0.0
        selected_sector_wing_south_height_in = 0.0
        selected_sector_link_east_length_in = 0.0
        selected_sector_link_east_width_in = 0.0
        selected_sector_link_east_height_in = 0.0
        selected_sector_link_north_length_in = 0.0
        selected_sector_link_north_width_in = 0.0
        selected_sector_link_north_height_in = 0.0
        selected_sector_link_west_length_in = 0.0
        selected_sector_link_west_width_in = 0.0
        selected_sector_link_west_height_in = 0.0
        selected_sector_link_south_length_in = 0.0
        selected_sector_link_south_width_in = 0.0
        selected_sector_link_south_height_in = 0.0
        selected_cooling_hall_length_in = 0.0
        selected_cooling_hall_width_in = 0.0
        selected_cooling_hall_height_in = 0.0
        selected_cooling_annex_length_in = 0.0
        selected_cooling_annex_width_in = 0.0
        selected_cooling_annex_height_in = 0.0
        selected_cooling_link_length_in = 0.0
        selected_cooling_link_width_in = 0.0
        selected_cooling_link_height_in = 0.0
        selected_turbine_hall_length_in = 0.0
        selected_turbine_hall_width_in = 0.0
        selected_turbine_hall_height_in = 0.0
        selected_cryo_coldbox_length_in = 0.0
        selected_cryo_coldbox_width_in = 0.0
        selected_cryo_coldbox_height_in = 0.0
        selected_cryo_compressors_length_in = 0.0
        selected_cryo_compressors_width_in = 0.0
        selected_cryo_compressors_height_in = 0.0
        selected_fuel_building_length_in = 0.0
        selected_fuel_building_width_in = 0.0
        selected_fuel_building_height_in = 0.0
        selected_reactor_auxiliaries_length_in = 0.0
        selected_reactor_auxiliaries_width_in = 0.0
        selected_reactor_auxiliaries_height_in = 0.0
        selected_power_supply_building_length_in = 0.0
        selected_power_supply_building_width_in = 0.0
        selected_power_supply_building_height_in = 0.0
        selected_electrical_building_length_in = 0.0
        selected_electrical_building_width_in = 0.0
        selected_electrical_building_height_in = 0.0
        selected_service_water_building_length_in = 0.0
        selected_service_water_building_width_in = 0.0
        selected_service_water_building_height_in = 0.0
        selected_maintenance_shop_length_in = 0.0
        selected_maintenance_shop_width_in = 0.0
        selected_maintenance_shop_height_in = 0.0
        selected_site_services_building_length_in = 0.0
        selected_site_services_building_width_in = 0.0
        selected_site_services_building_height_in = 0.0
        selected_administration_length_in = 0.0
        selected_administration_width_in = 0.0
        selected_administration_height_in = 0.0
        selected_control_length_in = 0.0
        selected_control_width_in = 0.0
        selected_control_height_in = 0.0
        selected_security_length_in = 0.0
        selected_security_width_in = 0.0
        selected_security_height_in = 0.0
        selected_cooling_helium_store_width_in = 0.0
        selected_cooling_salt_store_width_in = 0.0
        selected_cooling_bundle_store_width_in = 0.0
        selected_cooling_annex_north_depth_in = 0.0
        selected_blanket_packages_per_sector_in = 0.0
        selected_parcel_x_min_in = 0.0
        selected_parcel_y_min_in = 0.0
        selected_parcel_length_in = 0.0
        selected_parcel_width_in = 0.0
        
Documentation:
Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Manual completion reuses the live calendar and emits the declared finite scalar contract; deterministic ledgers are diagnostics.

    IMPLEMENTATION: See stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_layout_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts dirty_store_required, electrical_building_required_length, sector_link_north_clear_height, reactor_auxiliaries_sub_formwork, electrical_building_clear_height, dirty_store_positions_allocated, sector_wing_west_required_length, cryo_compressors_sub_formwork, sector_wing_east_clear_length, sector_wing_east_super_rebar, fuel_building_air_volume, turbine_hall_super_formwork, sector_link_north_clear_width, sector_wing_north_required_width, power_supply_building_clear_area, control_required_height, cooling_hall_clear_height, administration_sub_concrete, sector_wing_north_gross_area, administration_required_area, fuel_building_sub_rebar, sector_link_south_required_height, dirty_buffer_positions_allocated, sector_link_north_super_concrete, sector_wing_west_clear_length, cryo_coldbox_required_height, fuel_building_required_width, required_parcel_x_min, sector_wing_south_super_formwork, control_clear_width, sector_link_north_gross_area, electrical_building_super_formwork, cooling_annex_gross_area, replacement_ready_margin_days, cooling_annex_sub_formwork, maintenance_shop_clear_area, reactor_hall_gross_area, control_air_volume, sector_wing_south_required_length, site_services_building_sub_rebar, calendar_first_event_year, site_services_building_super_concrete, reactor_auxiliaries_gross_area, reactor_hall_required_height, service_water_building_clear_height, sector_link_south_required_width, sector_link_west_clear_area, occupancy_area_margin_m2, power_supply_building_gross_area, electrical_building_super_concrete, required_parcel_y_max, sector_link_south_super_concrete, site_services_building_sub_concrete, sector_link_south_sub_rebar, cryo_compressors_clear_area, electrical_building_clear_width, sector_wing_east_super_concrete, cooling_carrier_moves, cryo_coldbox_super_rebar, cryo_coldbox_super_formwork, cryo_coldbox_sub_formwork, sector_wing_east_sub_rebar, power_supply_building_sub_rebar, sector_link_south_clear_height, dirty_buffer_required, cooling_jobs_after_shutdown, service_water_building_super_rebar, fuel_building_clear_area, cooling_link_clear_width, cooling_annex_super_formwork, site_services_building_required_width, cooling_annex_required_height, reactor_auxiliaries_super_formwork, reactor_hall_clear_height, sector_link_north_air_volume, sector_wing_south_required_width, control_sub_rebar, service_water_building_clear_area, sector_wing_west_clear_height, sector_wing_south_sub_rebar, sector_wing_south_required_height, sector_link_west_super_concrete, administration_sub_rebar, cooling_hall_clear_width, exterior_envelope_qualified, outage_required_days, security_clear_width, fuel_building_super_formwork, power_supply_building_clear_width, service_water_building_sub_concrete, cryo_compressors_super_formwork, cryo_coldbox_clear_length, cryo_compressors_required_length, control_clear_length, calendar_last_event_year, turbine_hall_clear_width, controlled_air_volume, service_water_building_required_length, cooling_replacement_ready_margin_days, sector_link_west_air_volume, sector_link_north_clear_area, maintenance_shop_clear_length, blanket_packages_per_sector, maintenance_shop_clear_height, cooling_hall_super_formwork, maintenance_shop_required_width, sector_link_east_clear_area, sector_wing_north_super_rebar, turbine_hall_clear_height, sector_width, service_water_building_clear_length, active, maintenance_shop_sub_formwork, sector_wing_west_air_volume, site_services_building_clear_width, reactor_auxiliaries_required_height, cryo_compressors_sub_rebar, cooling_link_required_length, sector_wing_north_sub_formwork, power_supply_building_required_width, sector_wing_west_super_concrete, electrical_building_sub_formwork, turbine_hall_required_height, cryo_coldbox_clear_width, sector_wing_east_sub_formwork, reactor_auxiliaries_air_volume, sector_link_east_sub_rebar, cooling_link_sub_concrete, security_required_height, sector_wing_east_clear_area, site_services_building_clear_area, sector_link_north_required_height, cooling_annex_super_rebar, power_supply_building_sub_formwork, cooling_link_air_volume, cryo_compressors_clear_height, maintenance_shop_super_concrete, cooling_hall_sub_rebar, sector_wing_east_sub_concrete, cooling_helium_queue_peak, fuel_building_clear_height, service_water_building_clear_width, sector_link_south_required_length, administration_clear_area, cryo_coldbox_required_width, cooling_link_clear_area, site_services_building_sub_formwork, turbine_hall_super_rebar, cooling_salt_queue_peak, sector_link_south_air_volume, cooling_dirty_bundle_required, sector_wing_east_clear_width, sector_link_east_super_formwork, security_air_volume, reactor_auxiliaries_super_rebar, service_water_building_super_formwork, reactor_hall_clear_length, reactor_hall_sub_formwork, sector_link_east_required_length, cooling_hall_clear_area, sector_wing_west_sub_rebar, administration_air_volume, turbine_hall_clear_length, sector_link_south_clear_length, sector_wing_east_clear_height, turbine_hall_clear_area, sector_link_east_required_height, sector_wing_west_sub_formwork, service_water_building_required_height, sector_link_south_super_rebar, control_gross_area, fuel_building_gross_area, sector_length, cooling_annex_sub_rebar, cooling_annex_clear_area, calendar_event_count, sector_link_west_sub_formwork, sector_wing_west_clear_width, security_sub_concrete, fuel_building_super_concrete, cooling_clean_salt_allocated, cryo_compressors_gross_area, sector_link_east_clear_length, cooling_annex_air_volume, cryo_coldbox_clear_area, sector_wing_south_gross_area, cooling_outage_basis_resolved, turbine_hall_required_width, sector_wing_north_clear_length, cryo_compressors_required_height, turbine_hall_sub_concrete, contamination_procedure_qualified, cooling_hall_super_concrete, turbine_hall_super_concrete, control_super_rebar, sector_link_north_sub_rebar, maintenance_shop_sub_concrete, sector_link_south_clear_width, parcel_area, sector_wing_south_super_concrete, cryo_coldbox_required_length, administration_clear_length, sector_link_east_air_volume, security_clear_height, sector_wing_south_clear_height, reactor_auxiliaries_clear_height, packages_per_sector, security_sub_rebar, maintenance_shop_required_length, administration_required_height, sector_link_east_sub_concrete, sector_wing_east_gross_area, sector_link_east_super_rebar, fuel_building_clear_length, security_super_rebar, cryo_compressors_sub_concrete, service_water_building_super_concrete, reactor_hall_sub_concrete, service_water_building_sub_formwork, sector_link_east_sub_formwork, security_sub_formwork, security_super_concrete, sector_wing_west_clear_area, cryo_compressors_super_rebar, control_clear_area, cooling_annex_super_concrete, control_super_formwork, turbine_hall_sub_formwork, electrical_building_air_volume, cooling_hall_air_volume, sector_link_west_sub_rebar, cooling_hall_required_height, sector_wing_east_air_volume, sector_wing_south_clear_area, sector_link_east_gross_area, cooling_link_required_width, outage_allowed_days, cooling_annex_clear_length, sector_wing_north_sub_rebar, sector_link_west_super_formwork, initial_margin_days, sector_wing_east_required_height, sector_wing_east_required_length, service_water_building_sub_rebar, site_services_building_clear_height, administration_clear_width, maintenance_shop_clear_width, cooling_last_release_year, sector_wing_north_required_height, power_supply_building_clear_height, reactor_hall_required_length, cooling_dirty_salt_allocated, reactor_hall_sub_rebar, sector_link_east_clear_height, cooling_hall_required_width, site_services_building_super_rebar, sector_link_north_required_width, cryo_compressors_clear_width, turbine_hall_gross_area, reactor_hall_required_width, sector_link_north_required_length, sector_link_west_clear_length, control_sub_concrete, power_supply_building_super_concrete, electrical_building_required_height, reactor_auxiliaries_super_concrete, site_services_building_gross_area, reactor_auxiliaries_required_length, fuel_building_super_rebar, fuel_building_required_height, cooling_initial_ready_margin_days, sector_link_east_required_width, electrical_building_sub_concrete, security_gross_area, sector_link_north_sub_concrete, sector_wing_south_sub_concrete, cooling_annex_required_length, turbine_hall_required_length, geometry_fit_margin_m, readiness_margin_days, sector_wing_north_air_volume, power_supply_building_air_volume, total_gross_area, sector_wing_north_sub_concrete, cooling_annex_required_width, cryo_compressors_required_width, required_parcel_x_max, sector_wing_north_clear_area, cooling_bundle_queue_peak, cooling_annex_clear_height, power_supply_building_required_length, cooling_link_clear_length, initial_clean_required, power_supply_building_super_rebar, capacity_margin_units, cooling_link_sub_rebar, reactor_hall_clear_area, parcel_fit_margin_m, sector_link_south_gross_area, sector_link_north_super_rebar, sector_wing_south_super_rebar, blanket_packages_required_per_sector, cooling_dirty_helium_required, maintenance_shop_required_height, total_air_volume, cryo_compressors_clear_length, service_water_building_required_width, site_services_building_air_volume, sector_link_west_sub_concrete, administration_super_rebar, security_super_formwork, cryo_coldbox_sub_rebar, sector_link_south_sub_concrete, cooling_clean_bundle_required, cooling_clean_helium_allocated, route_margin_m, sector_link_west_clear_width, electrical_building_clear_area, sector_link_west_super_rebar, clean_positions_allocated, cooling_link_sub_formwork, cryo_coldbox_air_volume, cooling_hall_super_rebar, sector_wing_west_super_formwork, reactor_auxiliaries_clear_area, reactor_auxiliaries_sub_concrete, fuel_building_required_length, reactor_auxiliaries_sub_rebar, sector_wing_west_sub_concrete, cooling_dirty_bundle_allocated, cooling_hall_gross_area, sector_link_south_sub_formwork, sector_load_qualified, cryo_coldbox_clear_height, sector_link_north_sub_formwork, sector_wing_south_air_volume, outage_margin_days, sector_wing_north_super_concrete, cryo_coldbox_super_concrete, maintenance_shop_gross_area, site_services_building_required_height, sector_wing_west_super_rebar, sector_wing_north_clear_height, sector_link_south_super_formwork, sector_link_west_gross_area, cooling_hall_clear_length, sector_wing_west_required_width, administration_super_concrete, sector_link_north_clear_length, reactor_hall_super_concrete, administration_sub_formwork, turbine_hall_sub_rebar, site_services_building_clear_length, power_supply_building_sub_concrete, reactor_hall_air_volume, reactor_auxiliaries_clear_length, administration_super_formwork, site_services_building_super_formwork, administration_gross_area, material_capacity_volume, cooling_annex_clear_width, cooling_link_required_height, cooling_link_gross_area, cost_mode, cooling_clean_helium_required, control_required_area, cooling_link_clear_height, maintenance_shop_super_formwork, sector_link_east_clear_width, sector_wing_north_clear_width, maintenance_shop_sub_rebar, total_clear_area, cryo_compressors_air_volume, sector_wing_west_required_height, reactor_hall_super_rebar, cooling_dirty_helium_allocated, sector_link_east_super_concrete, sector_wing_north_required_length, turbine_hall_air_volume, provisional_room_count, sector_wing_south_clear_width, sector_link_west_required_height, sector_wing_south_clear_length, cooling_hall_sub_formwork, cryo_coldbox_sub_concrete, power_supply_building_super_formwork, fuel_building_sub_concrete, sector_link_south_clear_area, security_clear_length, cooling_link_super_concrete, reactor_auxiliaries_clear_width, site_services_building_required_length, cryo_compressors_super_concrete, required_parcel_y_min, sector_wing_east_required_width, cryo_coldbox_gross_area, cooling_hall_required_length, electrical_building_required_width, fuel_building_clear_width, administration_clear_height, security_required_area, service_water_building_gross_area, electrical_building_gross_area, initial_ready_margin_days, power_supply_building_clear_length, cooling_annex_sub_concrete, sector_link_west_required_length, fuel_building_sub_formwork, power_supply_building_required_height, cooling_clean_bundle_allocated, unused_material_capacity, cooling_hall_sub_concrete, maintenance_shop_super_rebar, sector_wing_west_gross_area, service_water_building_air_volume, sector_link_north_super_formwork, sector_wing_south_sub_formwork, reactor_hall_clear_width, sector_height, sector_wing_east_super_formwork, cooling_link_super_rebar, control_sub_formwork, maintenance_shop_air_volume, cooling_dirty_salt_required, control_clear_height, control_super_concrete, cooling_link_super_formwork, sector_link_west_clear_height, electrical_building_super_rebar, cooling_clean_salt_required, electrical_building_clear_length, reactor_auxiliaries_required_width, electrical_building_sub_rebar, security_clear_area, reactor_hall_super_formwork, sector_link_west_required_width, sector_wing_north_super_formwork fields to separate channels.
    """

    name: str = "Facility_LayoutModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, selected_site_services_building_height_in: float, selected_sector_link_east_width_in: float, selected_cooling_helium_store_width_in: float, selected_cooling_bundle_store_width_in: float, cooling_dirty_helium_positions_in: float, salt_package_height_in: float, selected_site_services_building_width_in: float, selected_sector_wing_south_length_in: float, selected_service_water_building_length_in: float, dirty_buffer_positions_in: float, building_separation_in: float, cooling_internal_move_days_in: float, cooling_cross_width_in: float, provisional_envelope_scale_in: float, site_services_width_in: float, hx_end_allowance_in: float, selected_sector_wing_south_width_in: float, selected_fuel_building_width_in: float, selected_sector_link_south_width_in: float, selected_sector_wing_west_width_in: float, selected_sector_wing_east_length_in: float, selected_turbine_hall_height_in: float, sector_join_days_in: float, selected_cryo_compressors_length_in: float, cooling_machine_stations_in: float, cooling_prepare_stations_in: float, reactor_aux_length_in: float, selected_parcel_x_min_in: float, turbine_height_in: float, selected_service_water_building_width_in: float, selected_cryo_coldbox_length_in: float, calendar_unplanned_in: float, selected_cooling_hall_height_in: float, n_mod_in: float, control_area_per_person_in: float, administration_occupants_in: float, cooling_helium_count_in: float, selected_cryo_compressors_width_in: float, selected_cryo_coldbox_height_in: float, cooling_aisle_width_in: float, selected_cooling_hall_length_in: float, sector_service_teams_in: float, cooling_hold_days_in: float, service_water_height_in: float, selected_service_water_building_height_in: float, cooling_dirty_bundle_positions_in: float, cooling_clean_salt_positions_in: float, selected_sector_link_west_height_in: float, selected_sector_link_east_height_in: float, waste_package_yield_in: float, selected_administration_length_in: float, cooling_prepare_bundle_days_in: float, selected_administration_height_in: float, selected_cryo_coldbox_width_in: float, sector_headroom_in: float, initial_sector_start_days_in: float, cooling_clean_bundle_positions_in: float, selected_electrical_building_width_in: float, selected_power_supply_building_height_in: float, hx_tube_length_in: float, conventional_rebar_density_in: float, selected_sector_wing_west_length_in: float, selected_sector_wing_west_height_in: float, selected_control_length_in: float, power_supply_length_in: float, component_remove_days_in: float, calendar_fluence_in: float, cryo_coldbox_length_in: float, administration_area_per_person_in: float, selected_sector_wing_north_length_in: float, facilities_cost_mode_in: float, selected_fuel_building_height_in: float, component_hold_days_in: float, selected_site_services_building_length_in: float, selected_sector_link_south_length_in: float, selected_sector_link_west_length_in: float, selected_reactor_auxiliaries_length_in: float, selected_electrical_building_height_in: float, selected_control_height_in: float, external_access_width_in: float, conventional_shop_width_in: float, cooling_machine_life_in: float, cooling_dirty_salt_positions_in: float, power_supply_height_in: float, selected_sector_wing_north_width_in: float, security_area_per_person_in: float, cooling_initial_receipt_lead_days_in: float, service_water_width_in: float, selected_cooling_link_height_in: float, selected_sector_link_west_width_in: float, sector_count_in: float, cooling_bundle_life_in: float, cooling_airlock_length_in: float, fuel_length_in: float, heat_rejection_width_in: float, cooldown_days_in: float, cryo_coldbox_width_in: float, cooling_bundle_stations_in: float, selected_cooling_link_length_in: float, cooling_headroom_in: float, sector_clean_days_in: float, reactor_aux_height_in: float, selected_sector_link_north_width_in: float, selected_cooling_annex_north_depth_in: float, initial_receipt_lead_days_in: float, onsite_ac_height_in: float, service_water_length_in: float, cooling_initial_handoff_days_in: float, occupancy_height_in: float, minor_outer_radius_in: float, selected_cryo_compressors_height_in: float, cooling_prepare_machine_days_in: float, helium_package_height_in: float, reactor_aux_width_in: float, selected_sector_link_south_height_in: float, component_prepare_days_in: float, selected_cooling_hall_width_in: float, selected_parcel_width_in: float, selected_control_width_in: float, clean_positions_in: float, helium_package_width_in: float, occupancy_circulation_factor_in: float, sector_route_clearance_in: float, calendar_count_in: float, control_occupants_in: float, selected_parcel_y_min_in: float, selected_cooling_annex_height_in: float, cooling_salt_count_in: float, sector_test_days_in: float, component_width_in: float, selected_maintenance_shop_width_in: float, selected_power_supply_building_width_in: float, selected_power_supply_building_length_in: float, sector_transport_days_in: float, nuclear_wall_in: float, selected_security_length_in: float, conventional_shop_length_in: float, sector_bays_in: float, selected_reactor_hall_height_in: float, selected_maintenance_shop_length_in: float, blanket_volume_in: float, cryo_compressors_length_in: float, cooling_machine_process_days_in: float, cryo_coldbox_height_in: float, selected_parcel_length_in: float, nuclear_rebar_density_in: float, selected_cooling_link_width_in: float, selected_reactor_hall_length_in: float, hx_shell_length_in: float, calendar_mode_in: float, dirty_store_positions_in: float, turbine_width_in: float, conventional_shop_height_in: float, selected_administration_width_in: float, component_process_days_in: float, selected_sector_wing_north_height_in: float, calendar_life_in: float, cryo_compressors_height_in: float, cooling_receipt_lead_days_in: float, selected_security_height_in: float, fuel_height_in: float, selected_electrical_building_length_in: float, hx_shell_bore_in: float, hx_shell_wall_in: float, selected_turbine_hall_length_in: float, conventional_floor_in: float, exterior_allowance_in: float, selected_security_width_in: float, selected_reactor_hall_width_in: float, security_occupants_in: float, salt_package_width_in: float, selected_sector_link_north_height_in: float, selected_turbine_hall_width_in: float, selected_fuel_building_length_in: float, sector_split_days_in: float, selected_blanket_packages_per_sector_in: float, onsite_ac_width_in: float, recommission_days_in: float, salt_package_length_in: float, selected_maintenance_shop_height_in: float, component_install_days_in: float, calendar_availability_in: float, helium_package_length_in: float, selected_reactor_auxiliaries_width_in: float, divertor_packages_per_sector_in: float, selected_sector_wing_east_width_in: float, cooling_package_margin_in: float, component_receipt_lead_days_in: float, cooling_bundle_count_in: float, cooling_clean_helium_positions_in: float, nuclear_roof_in: float, cryo_compressors_width_in: float, component_height_in: float, nuclear_floor_in: float, turbine_length_in: float, selected_reactor_auxiliaries_height_in: float, heat_rejection_length_in: float, major_radius_in: float, conventional_roof_in: float, component_length_in: float, conventional_wall_in: float, calendar_years_in: float, facilities_enabled_in: bool, cooling_field_cycle_days_in: float, selected_cooling_salt_store_width_in: float, component_handling_margin_in: float, cooling_bundle_process_days_in: float, calendar_outage_in: float, cooling_circuits_in: float, site_services_length_in: float, selected_sector_link_east_length_in: float, fuel_width_in: float, selected_sector_wing_south_height_in: float, site_services_height_in: float, selected_sector_link_north_length_in: float, selected_cooling_annex_length_in: float, component_material_fraction_in: float, selected_sector_wing_east_height_in: float, calendar_q_in: float, power_supply_width_in: float, onsite_ac_length_in: float, selected_cooling_annex_width_in: float    ) -> Facility_LayoutInput:
        """Validate inputs and fill defaults.

        Args:
            selected_site_services_building_height_in: selected_site_services_building_height_in input
            selected_sector_link_east_width_in: selected_sector_link_east_width_in input
            selected_cooling_helium_store_width_in: selected_cooling_helium_store_width_in input
            selected_cooling_bundle_store_width_in: selected_cooling_bundle_store_width_in input
            cooling_dirty_helium_positions_in: cooling_dirty_helium_positions_in input
            salt_package_height_in: salt_package_height_in input
            selected_site_services_building_width_in: selected_site_services_building_width_in input
            selected_sector_wing_south_length_in: selected_sector_wing_south_length_in input
            selected_service_water_building_length_in: selected_service_water_building_length_in input
            dirty_buffer_positions_in: dirty_buffer_positions_in input
            building_separation_in: building_separation_in input
            cooling_internal_move_days_in: cooling_internal_move_days_in input
            cooling_cross_width_in: cooling_cross_width_in input
            provisional_envelope_scale_in: provisional_envelope_scale_in input
            site_services_width_in: site_services_width_in input
            hx_end_allowance_in: hx_end_allowance_in input
            selected_sector_wing_south_width_in: selected_sector_wing_south_width_in input
            selected_fuel_building_width_in: selected_fuel_building_width_in input
            selected_sector_link_south_width_in: selected_sector_link_south_width_in input
            selected_sector_wing_west_width_in: selected_sector_wing_west_width_in input
            selected_sector_wing_east_length_in: selected_sector_wing_east_length_in input
            selected_turbine_hall_height_in: selected_turbine_hall_height_in input
            sector_join_days_in: sector_join_days_in input
            selected_cryo_compressors_length_in: selected_cryo_compressors_length_in input
            cooling_machine_stations_in: cooling_machine_stations_in input
            cooling_prepare_stations_in: cooling_prepare_stations_in input
            reactor_aux_length_in: reactor_aux_length_in input
            selected_parcel_x_min_in: selected_parcel_x_min_in input
            turbine_height_in: turbine_height_in input
            selected_service_water_building_width_in: selected_service_water_building_width_in input
            selected_cryo_coldbox_length_in: selected_cryo_coldbox_length_in input
            calendar_unplanned_in: calendar_unplanned_in input
            selected_cooling_hall_height_in: selected_cooling_hall_height_in input
            n_mod_in: n_mod_in input
            control_area_per_person_in: control_area_per_person_in input
            administration_occupants_in: administration_occupants_in input
            cooling_helium_count_in: cooling_helium_count_in input
            selected_cryo_compressors_width_in: selected_cryo_compressors_width_in input
            selected_cryo_coldbox_height_in: selected_cryo_coldbox_height_in input
            cooling_aisle_width_in: cooling_aisle_width_in input
            selected_cooling_hall_length_in: selected_cooling_hall_length_in input
            sector_service_teams_in: sector_service_teams_in input
            cooling_hold_days_in: cooling_hold_days_in input
            service_water_height_in: service_water_height_in input
            selected_service_water_building_height_in: selected_service_water_building_height_in input
            cooling_dirty_bundle_positions_in: cooling_dirty_bundle_positions_in input
            cooling_clean_salt_positions_in: cooling_clean_salt_positions_in input
            selected_sector_link_west_height_in: selected_sector_link_west_height_in input
            selected_sector_link_east_height_in: selected_sector_link_east_height_in input
            waste_package_yield_in: waste_package_yield_in input
            selected_administration_length_in: selected_administration_length_in input
            cooling_prepare_bundle_days_in: cooling_prepare_bundle_days_in input
            selected_administration_height_in: selected_administration_height_in input
            selected_cryo_coldbox_width_in: selected_cryo_coldbox_width_in input
            sector_headroom_in: sector_headroom_in input
            initial_sector_start_days_in: initial_sector_start_days_in input
            cooling_clean_bundle_positions_in: cooling_clean_bundle_positions_in input
            selected_electrical_building_width_in: selected_electrical_building_width_in input
            selected_power_supply_building_height_in: selected_power_supply_building_height_in input
            hx_tube_length_in: hx_tube_length_in input
            conventional_rebar_density_in: conventional_rebar_density_in input
            selected_sector_wing_west_length_in: selected_sector_wing_west_length_in input
            selected_sector_wing_west_height_in: selected_sector_wing_west_height_in input
            selected_control_length_in: selected_control_length_in input
            power_supply_length_in: power_supply_length_in input
            component_remove_days_in: component_remove_days_in input
            calendar_fluence_in: calendar_fluence_in input
            cryo_coldbox_length_in: cryo_coldbox_length_in input
            administration_area_per_person_in: administration_area_per_person_in input
            selected_sector_wing_north_length_in: selected_sector_wing_north_length_in input
            facilities_cost_mode_in: facilities_cost_mode_in input
            selected_fuel_building_height_in: selected_fuel_building_height_in input
            component_hold_days_in: component_hold_days_in input
            selected_site_services_building_length_in: selected_site_services_building_length_in input
            selected_sector_link_south_length_in: selected_sector_link_south_length_in input
            selected_sector_link_west_length_in: selected_sector_link_west_length_in input
            selected_reactor_auxiliaries_length_in: selected_reactor_auxiliaries_length_in input
            selected_electrical_building_height_in: selected_electrical_building_height_in input
            selected_control_height_in: selected_control_height_in input
            external_access_width_in: external_access_width_in input
            conventional_shop_width_in: conventional_shop_width_in input
            cooling_machine_life_in: cooling_machine_life_in input
            cooling_dirty_salt_positions_in: cooling_dirty_salt_positions_in input
            power_supply_height_in: power_supply_height_in input
            selected_sector_wing_north_width_in: selected_sector_wing_north_width_in input
            security_area_per_person_in: security_area_per_person_in input
            cooling_initial_receipt_lead_days_in: cooling_initial_receipt_lead_days_in input
            service_water_width_in: service_water_width_in input
            selected_cooling_link_height_in: selected_cooling_link_height_in input
            selected_sector_link_west_width_in: selected_sector_link_west_width_in input
            sector_count_in: sector_count_in input
            cooling_bundle_life_in: cooling_bundle_life_in input
            cooling_airlock_length_in: cooling_airlock_length_in input
            fuel_length_in: fuel_length_in input
            heat_rejection_width_in: heat_rejection_width_in input
            cooldown_days_in: cooldown_days_in input
            cryo_coldbox_width_in: cryo_coldbox_width_in input
            cooling_bundle_stations_in: cooling_bundle_stations_in input
            selected_cooling_link_length_in: selected_cooling_link_length_in input
            cooling_headroom_in: cooling_headroom_in input
            sector_clean_days_in: sector_clean_days_in input
            reactor_aux_height_in: reactor_aux_height_in input
            selected_sector_link_north_width_in: selected_sector_link_north_width_in input
            selected_cooling_annex_north_depth_in: selected_cooling_annex_north_depth_in input
            initial_receipt_lead_days_in: initial_receipt_lead_days_in input
            onsite_ac_height_in: onsite_ac_height_in input
            service_water_length_in: service_water_length_in input
            cooling_initial_handoff_days_in: cooling_initial_handoff_days_in input
            occupancy_height_in: occupancy_height_in input
            minor_outer_radius_in: minor_outer_radius_in input
            selected_cryo_compressors_height_in: selected_cryo_compressors_height_in input
            cooling_prepare_machine_days_in: cooling_prepare_machine_days_in input
            helium_package_height_in: helium_package_height_in input
            reactor_aux_width_in: reactor_aux_width_in input
            selected_sector_link_south_height_in: selected_sector_link_south_height_in input
            component_prepare_days_in: component_prepare_days_in input
            selected_cooling_hall_width_in: selected_cooling_hall_width_in input
            selected_parcel_width_in: selected_parcel_width_in input
            selected_control_width_in: selected_control_width_in input
            clean_positions_in: clean_positions_in input
            helium_package_width_in: helium_package_width_in input
            occupancy_circulation_factor_in: occupancy_circulation_factor_in input
            sector_route_clearance_in: sector_route_clearance_in input
            calendar_count_in: calendar_count_in input
            control_occupants_in: control_occupants_in input
            selected_parcel_y_min_in: selected_parcel_y_min_in input
            selected_cooling_annex_height_in: selected_cooling_annex_height_in input
            cooling_salt_count_in: cooling_salt_count_in input
            sector_test_days_in: sector_test_days_in input
            component_width_in: component_width_in input
            selected_maintenance_shop_width_in: selected_maintenance_shop_width_in input
            selected_power_supply_building_width_in: selected_power_supply_building_width_in input
            selected_power_supply_building_length_in: selected_power_supply_building_length_in input
            sector_transport_days_in: sector_transport_days_in input
            nuclear_wall_in: nuclear_wall_in input
            selected_security_length_in: selected_security_length_in input
            conventional_shop_length_in: conventional_shop_length_in input
            sector_bays_in: sector_bays_in input
            selected_reactor_hall_height_in: selected_reactor_hall_height_in input
            selected_maintenance_shop_length_in: selected_maintenance_shop_length_in input
            blanket_volume_in: blanket_volume_in input
            cryo_compressors_length_in: cryo_compressors_length_in input
            cooling_machine_process_days_in: cooling_machine_process_days_in input
            cryo_coldbox_height_in: cryo_coldbox_height_in input
            selected_parcel_length_in: selected_parcel_length_in input
            nuclear_rebar_density_in: nuclear_rebar_density_in input
            selected_cooling_link_width_in: selected_cooling_link_width_in input
            selected_reactor_hall_length_in: selected_reactor_hall_length_in input
            hx_shell_length_in: hx_shell_length_in input
            calendar_mode_in: calendar_mode_in input
            dirty_store_positions_in: dirty_store_positions_in input
            turbine_width_in: turbine_width_in input
            conventional_shop_height_in: conventional_shop_height_in input
            selected_administration_width_in: selected_administration_width_in input
            component_process_days_in: component_process_days_in input
            selected_sector_wing_north_height_in: selected_sector_wing_north_height_in input
            calendar_life_in: calendar_life_in input
            cryo_compressors_height_in: cryo_compressors_height_in input
            cooling_receipt_lead_days_in: cooling_receipt_lead_days_in input
            selected_security_height_in: selected_security_height_in input
            fuel_height_in: fuel_height_in input
            selected_electrical_building_length_in: selected_electrical_building_length_in input
            hx_shell_bore_in: hx_shell_bore_in input
            hx_shell_wall_in: hx_shell_wall_in input
            selected_turbine_hall_length_in: selected_turbine_hall_length_in input
            conventional_floor_in: conventional_floor_in input
            exterior_allowance_in: exterior_allowance_in input
            selected_security_width_in: selected_security_width_in input
            selected_reactor_hall_width_in: selected_reactor_hall_width_in input
            security_occupants_in: security_occupants_in input
            salt_package_width_in: salt_package_width_in input
            selected_sector_link_north_height_in: selected_sector_link_north_height_in input
            selected_turbine_hall_width_in: selected_turbine_hall_width_in input
            selected_fuel_building_length_in: selected_fuel_building_length_in input
            sector_split_days_in: sector_split_days_in input
            selected_blanket_packages_per_sector_in: selected_blanket_packages_per_sector_in input
            onsite_ac_width_in: onsite_ac_width_in input
            recommission_days_in: recommission_days_in input
            salt_package_length_in: salt_package_length_in input
            selected_maintenance_shop_height_in: selected_maintenance_shop_height_in input
            component_install_days_in: component_install_days_in input
            calendar_availability_in: calendar_availability_in input
            helium_package_length_in: helium_package_length_in input
            selected_reactor_auxiliaries_width_in: selected_reactor_auxiliaries_width_in input
            divertor_packages_per_sector_in: divertor_packages_per_sector_in input
            selected_sector_wing_east_width_in: selected_sector_wing_east_width_in input
            cooling_package_margin_in: cooling_package_margin_in input
            component_receipt_lead_days_in: component_receipt_lead_days_in input
            cooling_bundle_count_in: cooling_bundle_count_in input
            cooling_clean_helium_positions_in: cooling_clean_helium_positions_in input
            nuclear_roof_in: nuclear_roof_in input
            cryo_compressors_width_in: cryo_compressors_width_in input
            component_height_in: component_height_in input
            nuclear_floor_in: nuclear_floor_in input
            turbine_length_in: turbine_length_in input
            selected_reactor_auxiliaries_height_in: selected_reactor_auxiliaries_height_in input
            heat_rejection_length_in: heat_rejection_length_in input
            major_radius_in: major_radius_in input
            conventional_roof_in: conventional_roof_in input
            component_length_in: component_length_in input
            conventional_wall_in: conventional_wall_in input
            calendar_years_in: calendar_years_in input
            facilities_enabled_in: facilities_enabled_in input
            cooling_field_cycle_days_in: cooling_field_cycle_days_in input
            selected_cooling_salt_store_width_in: selected_cooling_salt_store_width_in input
            component_handling_margin_in: component_handling_margin_in input
            cooling_bundle_process_days_in: cooling_bundle_process_days_in input
            calendar_outage_in: calendar_outage_in input
            cooling_circuits_in: cooling_circuits_in input
            site_services_length_in: site_services_length_in input
            selected_sector_link_east_length_in: selected_sector_link_east_length_in input
            fuel_width_in: fuel_width_in input
            selected_sector_wing_south_height_in: selected_sector_wing_south_height_in input
            site_services_height_in: site_services_height_in input
            selected_sector_link_north_length_in: selected_sector_link_north_length_in input
            selected_cooling_annex_length_in: selected_cooling_annex_length_in input
            component_material_fraction_in: component_material_fraction_in input
            selected_sector_wing_east_height_in: selected_sector_wing_east_height_in input
            calendar_q_in: calendar_q_in input
            power_supply_width_in: power_supply_width_in input
            onsite_ac_length_in: onsite_ac_length_in input
            selected_cooling_annex_width_in: selected_cooling_annex_width_in input

        Returns:
            Validated input model
        """
        return Facility_LayoutInput(selected_site_services_building_height_in=selected_site_services_building_height_in, selected_sector_link_east_width_in=selected_sector_link_east_width_in, selected_cooling_helium_store_width_in=selected_cooling_helium_store_width_in, selected_cooling_bundle_store_width_in=selected_cooling_bundle_store_width_in, cooling_dirty_helium_positions_in=cooling_dirty_helium_positions_in, salt_package_height_in=salt_package_height_in, selected_site_services_building_width_in=selected_site_services_building_width_in, selected_sector_wing_south_length_in=selected_sector_wing_south_length_in, selected_service_water_building_length_in=selected_service_water_building_length_in, dirty_buffer_positions_in=dirty_buffer_positions_in, building_separation_in=building_separation_in, cooling_internal_move_days_in=cooling_internal_move_days_in, cooling_cross_width_in=cooling_cross_width_in, provisional_envelope_scale_in=provisional_envelope_scale_in, site_services_width_in=site_services_width_in, hx_end_allowance_in=hx_end_allowance_in, selected_sector_wing_south_width_in=selected_sector_wing_south_width_in, selected_fuel_building_width_in=selected_fuel_building_width_in, selected_sector_link_south_width_in=selected_sector_link_south_width_in, selected_sector_wing_west_width_in=selected_sector_wing_west_width_in, selected_sector_wing_east_length_in=selected_sector_wing_east_length_in, selected_turbine_hall_height_in=selected_turbine_hall_height_in, sector_join_days_in=sector_join_days_in, selected_cryo_compressors_length_in=selected_cryo_compressors_length_in, cooling_machine_stations_in=cooling_machine_stations_in, cooling_prepare_stations_in=cooling_prepare_stations_in, reactor_aux_length_in=reactor_aux_length_in, selected_parcel_x_min_in=selected_parcel_x_min_in, turbine_height_in=turbine_height_in, selected_service_water_building_width_in=selected_service_water_building_width_in, selected_cryo_coldbox_length_in=selected_cryo_coldbox_length_in, calendar_unplanned_in=calendar_unplanned_in, selected_cooling_hall_height_in=selected_cooling_hall_height_in, n_mod_in=n_mod_in, control_area_per_person_in=control_area_per_person_in, administration_occupants_in=administration_occupants_in, cooling_helium_count_in=cooling_helium_count_in, selected_cryo_compressors_width_in=selected_cryo_compressors_width_in, selected_cryo_coldbox_height_in=selected_cryo_coldbox_height_in, cooling_aisle_width_in=cooling_aisle_width_in, selected_cooling_hall_length_in=selected_cooling_hall_length_in, sector_service_teams_in=sector_service_teams_in, cooling_hold_days_in=cooling_hold_days_in, service_water_height_in=service_water_height_in, selected_service_water_building_height_in=selected_service_water_building_height_in, cooling_dirty_bundle_positions_in=cooling_dirty_bundle_positions_in, cooling_clean_salt_positions_in=cooling_clean_salt_positions_in, selected_sector_link_west_height_in=selected_sector_link_west_height_in, selected_sector_link_east_height_in=selected_sector_link_east_height_in, waste_package_yield_in=waste_package_yield_in, selected_administration_length_in=selected_administration_length_in, cooling_prepare_bundle_days_in=cooling_prepare_bundle_days_in, selected_administration_height_in=selected_administration_height_in, selected_cryo_coldbox_width_in=selected_cryo_coldbox_width_in, sector_headroom_in=sector_headroom_in, initial_sector_start_days_in=initial_sector_start_days_in, cooling_clean_bundle_positions_in=cooling_clean_bundle_positions_in, selected_electrical_building_width_in=selected_electrical_building_width_in, selected_power_supply_building_height_in=selected_power_supply_building_height_in, hx_tube_length_in=hx_tube_length_in, conventional_rebar_density_in=conventional_rebar_density_in, selected_sector_wing_west_length_in=selected_sector_wing_west_length_in, selected_sector_wing_west_height_in=selected_sector_wing_west_height_in, selected_control_length_in=selected_control_length_in, power_supply_length_in=power_supply_length_in, component_remove_days_in=component_remove_days_in, calendar_fluence_in=calendar_fluence_in, cryo_coldbox_length_in=cryo_coldbox_length_in, administration_area_per_person_in=administration_area_per_person_in, selected_sector_wing_north_length_in=selected_sector_wing_north_length_in, facilities_cost_mode_in=facilities_cost_mode_in, selected_fuel_building_height_in=selected_fuel_building_height_in, component_hold_days_in=component_hold_days_in, selected_site_services_building_length_in=selected_site_services_building_length_in, selected_sector_link_south_length_in=selected_sector_link_south_length_in, selected_sector_link_west_length_in=selected_sector_link_west_length_in, selected_reactor_auxiliaries_length_in=selected_reactor_auxiliaries_length_in, selected_electrical_building_height_in=selected_electrical_building_height_in, selected_control_height_in=selected_control_height_in, external_access_width_in=external_access_width_in, conventional_shop_width_in=conventional_shop_width_in, cooling_machine_life_in=cooling_machine_life_in, cooling_dirty_salt_positions_in=cooling_dirty_salt_positions_in, power_supply_height_in=power_supply_height_in, selected_sector_wing_north_width_in=selected_sector_wing_north_width_in, security_area_per_person_in=security_area_per_person_in, cooling_initial_receipt_lead_days_in=cooling_initial_receipt_lead_days_in, service_water_width_in=service_water_width_in, selected_cooling_link_height_in=selected_cooling_link_height_in, selected_sector_link_west_width_in=selected_sector_link_west_width_in, sector_count_in=sector_count_in, cooling_bundle_life_in=cooling_bundle_life_in, cooling_airlock_length_in=cooling_airlock_length_in, fuel_length_in=fuel_length_in, heat_rejection_width_in=heat_rejection_width_in, cooldown_days_in=cooldown_days_in, cryo_coldbox_width_in=cryo_coldbox_width_in, cooling_bundle_stations_in=cooling_bundle_stations_in, selected_cooling_link_length_in=selected_cooling_link_length_in, cooling_headroom_in=cooling_headroom_in, sector_clean_days_in=sector_clean_days_in, reactor_aux_height_in=reactor_aux_height_in, selected_sector_link_north_width_in=selected_sector_link_north_width_in, selected_cooling_annex_north_depth_in=selected_cooling_annex_north_depth_in, initial_receipt_lead_days_in=initial_receipt_lead_days_in, onsite_ac_height_in=onsite_ac_height_in, service_water_length_in=service_water_length_in, cooling_initial_handoff_days_in=cooling_initial_handoff_days_in, occupancy_height_in=occupancy_height_in, minor_outer_radius_in=minor_outer_radius_in, selected_cryo_compressors_height_in=selected_cryo_compressors_height_in, cooling_prepare_machine_days_in=cooling_prepare_machine_days_in, helium_package_height_in=helium_package_height_in, reactor_aux_width_in=reactor_aux_width_in, selected_sector_link_south_height_in=selected_sector_link_south_height_in, component_prepare_days_in=component_prepare_days_in, selected_cooling_hall_width_in=selected_cooling_hall_width_in, selected_parcel_width_in=selected_parcel_width_in, selected_control_width_in=selected_control_width_in, clean_positions_in=clean_positions_in, helium_package_width_in=helium_package_width_in, occupancy_circulation_factor_in=occupancy_circulation_factor_in, sector_route_clearance_in=sector_route_clearance_in, calendar_count_in=calendar_count_in, control_occupants_in=control_occupants_in, selected_parcel_y_min_in=selected_parcel_y_min_in, selected_cooling_annex_height_in=selected_cooling_annex_height_in, cooling_salt_count_in=cooling_salt_count_in, sector_test_days_in=sector_test_days_in, component_width_in=component_width_in, selected_maintenance_shop_width_in=selected_maintenance_shop_width_in, selected_power_supply_building_width_in=selected_power_supply_building_width_in, selected_power_supply_building_length_in=selected_power_supply_building_length_in, sector_transport_days_in=sector_transport_days_in, nuclear_wall_in=nuclear_wall_in, selected_security_length_in=selected_security_length_in, conventional_shop_length_in=conventional_shop_length_in, sector_bays_in=sector_bays_in, selected_reactor_hall_height_in=selected_reactor_hall_height_in, selected_maintenance_shop_length_in=selected_maintenance_shop_length_in, blanket_volume_in=blanket_volume_in, cryo_compressors_length_in=cryo_compressors_length_in, cooling_machine_process_days_in=cooling_machine_process_days_in, cryo_coldbox_height_in=cryo_coldbox_height_in, selected_parcel_length_in=selected_parcel_length_in, nuclear_rebar_density_in=nuclear_rebar_density_in, selected_cooling_link_width_in=selected_cooling_link_width_in, selected_reactor_hall_length_in=selected_reactor_hall_length_in, hx_shell_length_in=hx_shell_length_in, calendar_mode_in=calendar_mode_in, dirty_store_positions_in=dirty_store_positions_in, turbine_width_in=turbine_width_in, conventional_shop_height_in=conventional_shop_height_in, selected_administration_width_in=selected_administration_width_in, component_process_days_in=component_process_days_in, selected_sector_wing_north_height_in=selected_sector_wing_north_height_in, calendar_life_in=calendar_life_in, cryo_compressors_height_in=cryo_compressors_height_in, cooling_receipt_lead_days_in=cooling_receipt_lead_days_in, selected_security_height_in=selected_security_height_in, fuel_height_in=fuel_height_in, selected_electrical_building_length_in=selected_electrical_building_length_in, hx_shell_bore_in=hx_shell_bore_in, hx_shell_wall_in=hx_shell_wall_in, selected_turbine_hall_length_in=selected_turbine_hall_length_in, conventional_floor_in=conventional_floor_in, exterior_allowance_in=exterior_allowance_in, selected_security_width_in=selected_security_width_in, selected_reactor_hall_width_in=selected_reactor_hall_width_in, security_occupants_in=security_occupants_in, salt_package_width_in=salt_package_width_in, selected_sector_link_north_height_in=selected_sector_link_north_height_in, selected_turbine_hall_width_in=selected_turbine_hall_width_in, selected_fuel_building_length_in=selected_fuel_building_length_in, sector_split_days_in=sector_split_days_in, selected_blanket_packages_per_sector_in=selected_blanket_packages_per_sector_in, onsite_ac_width_in=onsite_ac_width_in, recommission_days_in=recommission_days_in, salt_package_length_in=salt_package_length_in, selected_maintenance_shop_height_in=selected_maintenance_shop_height_in, component_install_days_in=component_install_days_in, calendar_availability_in=calendar_availability_in, helium_package_length_in=helium_package_length_in, selected_reactor_auxiliaries_width_in=selected_reactor_auxiliaries_width_in, divertor_packages_per_sector_in=divertor_packages_per_sector_in, selected_sector_wing_east_width_in=selected_sector_wing_east_width_in, cooling_package_margin_in=cooling_package_margin_in, component_receipt_lead_days_in=component_receipt_lead_days_in, cooling_bundle_count_in=cooling_bundle_count_in, cooling_clean_helium_positions_in=cooling_clean_helium_positions_in, nuclear_roof_in=nuclear_roof_in, cryo_compressors_width_in=cryo_compressors_width_in, component_height_in=component_height_in, nuclear_floor_in=nuclear_floor_in, turbine_length_in=turbine_length_in, selected_reactor_auxiliaries_height_in=selected_reactor_auxiliaries_height_in, heat_rejection_length_in=heat_rejection_length_in, major_radius_in=major_radius_in, conventional_roof_in=conventional_roof_in, component_length_in=component_length_in, conventional_wall_in=conventional_wall_in, calendar_years_in=calendar_years_in, facilities_enabled_in=facilities_enabled_in, cooling_field_cycle_days_in=cooling_field_cycle_days_in, selected_cooling_salt_store_width_in=selected_cooling_salt_store_width_in, component_handling_margin_in=component_handling_margin_in, cooling_bundle_process_days_in=cooling_bundle_process_days_in, calendar_outage_in=calendar_outage_in, cooling_circuits_in=cooling_circuits_in, site_services_length_in=site_services_length_in, selected_sector_link_east_length_in=selected_sector_link_east_length_in, fuel_width_in=fuel_width_in, selected_sector_wing_south_height_in=selected_sector_wing_south_height_in, site_services_height_in=site_services_height_in, selected_sector_link_north_length_in=selected_sector_link_north_length_in, selected_cooling_annex_length_in=selected_cooling_annex_length_in, component_material_fraction_in=component_material_fraction_in, selected_sector_wing_east_height_in=selected_sector_wing_east_height_in, calendar_q_in=calendar_q_in, power_supply_width_in=power_supply_width_in, onsite_ac_length_in=onsite_ac_length_in, selected_cooling_annex_width_in=selected_cooling_annex_width_in)

    def run(
        self, selected_site_services_building_height_in: float, selected_sector_link_east_width_in: float, selected_cooling_helium_store_width_in: float, selected_cooling_bundle_store_width_in: float, cooling_dirty_helium_positions_in: float, salt_package_height_in: float, selected_site_services_building_width_in: float, selected_sector_wing_south_length_in: float, selected_service_water_building_length_in: float, dirty_buffer_positions_in: float, building_separation_in: float, cooling_internal_move_days_in: float, cooling_cross_width_in: float, provisional_envelope_scale_in: float, site_services_width_in: float, hx_end_allowance_in: float, selected_sector_wing_south_width_in: float, selected_fuel_building_width_in: float, selected_sector_link_south_width_in: float, selected_sector_wing_west_width_in: float, selected_sector_wing_east_length_in: float, selected_turbine_hall_height_in: float, sector_join_days_in: float, selected_cryo_compressors_length_in: float, cooling_machine_stations_in: float, cooling_prepare_stations_in: float, reactor_aux_length_in: float, selected_parcel_x_min_in: float, turbine_height_in: float, selected_service_water_building_width_in: float, selected_cryo_coldbox_length_in: float, calendar_unplanned_in: float, selected_cooling_hall_height_in: float, n_mod_in: float, control_area_per_person_in: float, administration_occupants_in: float, cooling_helium_count_in: float, selected_cryo_compressors_width_in: float, selected_cryo_coldbox_height_in: float, cooling_aisle_width_in: float, selected_cooling_hall_length_in: float, sector_service_teams_in: float, cooling_hold_days_in: float, service_water_height_in: float, selected_service_water_building_height_in: float, cooling_dirty_bundle_positions_in: float, cooling_clean_salt_positions_in: float, selected_sector_link_west_height_in: float, selected_sector_link_east_height_in: float, waste_package_yield_in: float, selected_administration_length_in: float, cooling_prepare_bundle_days_in: float, selected_administration_height_in: float, selected_cryo_coldbox_width_in: float, sector_headroom_in: float, initial_sector_start_days_in: float, cooling_clean_bundle_positions_in: float, selected_electrical_building_width_in: float, selected_power_supply_building_height_in: float, hx_tube_length_in: float, conventional_rebar_density_in: float, selected_sector_wing_west_length_in: float, selected_sector_wing_west_height_in: float, selected_control_length_in: float, power_supply_length_in: float, component_remove_days_in: float, calendar_fluence_in: float, cryo_coldbox_length_in: float, administration_area_per_person_in: float, selected_sector_wing_north_length_in: float, facilities_cost_mode_in: float, selected_fuel_building_height_in: float, component_hold_days_in: float, selected_site_services_building_length_in: float, selected_sector_link_south_length_in: float, selected_sector_link_west_length_in: float, selected_reactor_auxiliaries_length_in: float, selected_electrical_building_height_in: float, selected_control_height_in: float, external_access_width_in: float, conventional_shop_width_in: float, cooling_machine_life_in: float, cooling_dirty_salt_positions_in: float, power_supply_height_in: float, selected_sector_wing_north_width_in: float, security_area_per_person_in: float, cooling_initial_receipt_lead_days_in: float, service_water_width_in: float, selected_cooling_link_height_in: float, selected_sector_link_west_width_in: float, sector_count_in: float, cooling_bundle_life_in: float, cooling_airlock_length_in: float, fuel_length_in: float, heat_rejection_width_in: float, cooldown_days_in: float, cryo_coldbox_width_in: float, cooling_bundle_stations_in: float, selected_cooling_link_length_in: float, cooling_headroom_in: float, sector_clean_days_in: float, reactor_aux_height_in: float, selected_sector_link_north_width_in: float, selected_cooling_annex_north_depth_in: float, initial_receipt_lead_days_in: float, onsite_ac_height_in: float, service_water_length_in: float, cooling_initial_handoff_days_in: float, occupancy_height_in: float, minor_outer_radius_in: float, selected_cryo_compressors_height_in: float, cooling_prepare_machine_days_in: float, helium_package_height_in: float, reactor_aux_width_in: float, selected_sector_link_south_height_in: float, component_prepare_days_in: float, selected_cooling_hall_width_in: float, selected_parcel_width_in: float, selected_control_width_in: float, clean_positions_in: float, helium_package_width_in: float, occupancy_circulation_factor_in: float, sector_route_clearance_in: float, calendar_count_in: float, control_occupants_in: float, selected_parcel_y_min_in: float, selected_cooling_annex_height_in: float, cooling_salt_count_in: float, sector_test_days_in: float, component_width_in: float, selected_maintenance_shop_width_in: float, selected_power_supply_building_width_in: float, selected_power_supply_building_length_in: float, sector_transport_days_in: float, nuclear_wall_in: float, selected_security_length_in: float, conventional_shop_length_in: float, sector_bays_in: float, selected_reactor_hall_height_in: float, selected_maintenance_shop_length_in: float, blanket_volume_in: float, cryo_compressors_length_in: float, cooling_machine_process_days_in: float, cryo_coldbox_height_in: float, selected_parcel_length_in: float, nuclear_rebar_density_in: float, selected_cooling_link_width_in: float, selected_reactor_hall_length_in: float, hx_shell_length_in: float, calendar_mode_in: float, dirty_store_positions_in: float, turbine_width_in: float, conventional_shop_height_in: float, selected_administration_width_in: float, component_process_days_in: float, selected_sector_wing_north_height_in: float, calendar_life_in: float, cryo_compressors_height_in: float, cooling_receipt_lead_days_in: float, selected_security_height_in: float, fuel_height_in: float, selected_electrical_building_length_in: float, hx_shell_bore_in: float, hx_shell_wall_in: float, selected_turbine_hall_length_in: float, conventional_floor_in: float, exterior_allowance_in: float, selected_security_width_in: float, selected_reactor_hall_width_in: float, security_occupants_in: float, salt_package_width_in: float, selected_sector_link_north_height_in: float, selected_turbine_hall_width_in: float, selected_fuel_building_length_in: float, sector_split_days_in: float, selected_blanket_packages_per_sector_in: float, onsite_ac_width_in: float, recommission_days_in: float, salt_package_length_in: float, selected_maintenance_shop_height_in: float, component_install_days_in: float, calendar_availability_in: float, helium_package_length_in: float, selected_reactor_auxiliaries_width_in: float, divertor_packages_per_sector_in: float, selected_sector_wing_east_width_in: float, cooling_package_margin_in: float, component_receipt_lead_days_in: float, cooling_bundle_count_in: float, cooling_clean_helium_positions_in: float, nuclear_roof_in: float, cryo_compressors_width_in: float, component_height_in: float, nuclear_floor_in: float, turbine_length_in: float, selected_reactor_auxiliaries_height_in: float, heat_rejection_length_in: float, major_radius_in: float, conventional_roof_in: float, component_length_in: float, conventional_wall_in: float, calendar_years_in: float, facilities_enabled_in: bool, cooling_field_cycle_days_in: float, selected_cooling_salt_store_width_in: float, component_handling_margin_in: float, cooling_bundle_process_days_in: float, calendar_outage_in: float, cooling_circuits_in: float, site_services_length_in: float, selected_sector_link_east_length_in: float, fuel_width_in: float, selected_sector_wing_south_height_in: float, site_services_height_in: float, selected_sector_link_north_length_in: float, selected_cooling_annex_length_in: float, component_material_fraction_in: float, selected_sector_wing_east_height_in: float, calendar_q_in: float, power_supply_width_in: float, onsite_ac_length_in: float, selected_cooling_annex_width_in: float    ) -> ModuleResult[Facility_LayoutOutput]:
        """Execute calculation.

        Args:
            selected_site_services_building_height_in: selected_site_services_building_height_in input
            selected_sector_link_east_width_in: selected_sector_link_east_width_in input
            selected_cooling_helium_store_width_in: selected_cooling_helium_store_width_in input
            selected_cooling_bundle_store_width_in: selected_cooling_bundle_store_width_in input
            cooling_dirty_helium_positions_in: cooling_dirty_helium_positions_in input
            salt_package_height_in: salt_package_height_in input
            selected_site_services_building_width_in: selected_site_services_building_width_in input
            selected_sector_wing_south_length_in: selected_sector_wing_south_length_in input
            selected_service_water_building_length_in: selected_service_water_building_length_in input
            dirty_buffer_positions_in: dirty_buffer_positions_in input
            building_separation_in: building_separation_in input
            cooling_internal_move_days_in: cooling_internal_move_days_in input
            cooling_cross_width_in: cooling_cross_width_in input
            provisional_envelope_scale_in: provisional_envelope_scale_in input
            site_services_width_in: site_services_width_in input
            hx_end_allowance_in: hx_end_allowance_in input
            selected_sector_wing_south_width_in: selected_sector_wing_south_width_in input
            selected_fuel_building_width_in: selected_fuel_building_width_in input
            selected_sector_link_south_width_in: selected_sector_link_south_width_in input
            selected_sector_wing_west_width_in: selected_sector_wing_west_width_in input
            selected_sector_wing_east_length_in: selected_sector_wing_east_length_in input
            selected_turbine_hall_height_in: selected_turbine_hall_height_in input
            sector_join_days_in: sector_join_days_in input
            selected_cryo_compressors_length_in: selected_cryo_compressors_length_in input
            cooling_machine_stations_in: cooling_machine_stations_in input
            cooling_prepare_stations_in: cooling_prepare_stations_in input
            reactor_aux_length_in: reactor_aux_length_in input
            selected_parcel_x_min_in: selected_parcel_x_min_in input
            turbine_height_in: turbine_height_in input
            selected_service_water_building_width_in: selected_service_water_building_width_in input
            selected_cryo_coldbox_length_in: selected_cryo_coldbox_length_in input
            calendar_unplanned_in: calendar_unplanned_in input
            selected_cooling_hall_height_in: selected_cooling_hall_height_in input
            n_mod_in: n_mod_in input
            control_area_per_person_in: control_area_per_person_in input
            administration_occupants_in: administration_occupants_in input
            cooling_helium_count_in: cooling_helium_count_in input
            selected_cryo_compressors_width_in: selected_cryo_compressors_width_in input
            selected_cryo_coldbox_height_in: selected_cryo_coldbox_height_in input
            cooling_aisle_width_in: cooling_aisle_width_in input
            selected_cooling_hall_length_in: selected_cooling_hall_length_in input
            sector_service_teams_in: sector_service_teams_in input
            cooling_hold_days_in: cooling_hold_days_in input
            service_water_height_in: service_water_height_in input
            selected_service_water_building_height_in: selected_service_water_building_height_in input
            cooling_dirty_bundle_positions_in: cooling_dirty_bundle_positions_in input
            cooling_clean_salt_positions_in: cooling_clean_salt_positions_in input
            selected_sector_link_west_height_in: selected_sector_link_west_height_in input
            selected_sector_link_east_height_in: selected_sector_link_east_height_in input
            waste_package_yield_in: waste_package_yield_in input
            selected_administration_length_in: selected_administration_length_in input
            cooling_prepare_bundle_days_in: cooling_prepare_bundle_days_in input
            selected_administration_height_in: selected_administration_height_in input
            selected_cryo_coldbox_width_in: selected_cryo_coldbox_width_in input
            sector_headroom_in: sector_headroom_in input
            initial_sector_start_days_in: initial_sector_start_days_in input
            cooling_clean_bundle_positions_in: cooling_clean_bundle_positions_in input
            selected_electrical_building_width_in: selected_electrical_building_width_in input
            selected_power_supply_building_height_in: selected_power_supply_building_height_in input
            hx_tube_length_in: hx_tube_length_in input
            conventional_rebar_density_in: conventional_rebar_density_in input
            selected_sector_wing_west_length_in: selected_sector_wing_west_length_in input
            selected_sector_wing_west_height_in: selected_sector_wing_west_height_in input
            selected_control_length_in: selected_control_length_in input
            power_supply_length_in: power_supply_length_in input
            component_remove_days_in: component_remove_days_in input
            calendar_fluence_in: calendar_fluence_in input
            cryo_coldbox_length_in: cryo_coldbox_length_in input
            administration_area_per_person_in: administration_area_per_person_in input
            selected_sector_wing_north_length_in: selected_sector_wing_north_length_in input
            facilities_cost_mode_in: facilities_cost_mode_in input
            selected_fuel_building_height_in: selected_fuel_building_height_in input
            component_hold_days_in: component_hold_days_in input
            selected_site_services_building_length_in: selected_site_services_building_length_in input
            selected_sector_link_south_length_in: selected_sector_link_south_length_in input
            selected_sector_link_west_length_in: selected_sector_link_west_length_in input
            selected_reactor_auxiliaries_length_in: selected_reactor_auxiliaries_length_in input
            selected_electrical_building_height_in: selected_electrical_building_height_in input
            selected_control_height_in: selected_control_height_in input
            external_access_width_in: external_access_width_in input
            conventional_shop_width_in: conventional_shop_width_in input
            cooling_machine_life_in: cooling_machine_life_in input
            cooling_dirty_salt_positions_in: cooling_dirty_salt_positions_in input
            power_supply_height_in: power_supply_height_in input
            selected_sector_wing_north_width_in: selected_sector_wing_north_width_in input
            security_area_per_person_in: security_area_per_person_in input
            cooling_initial_receipt_lead_days_in: cooling_initial_receipt_lead_days_in input
            service_water_width_in: service_water_width_in input
            selected_cooling_link_height_in: selected_cooling_link_height_in input
            selected_sector_link_west_width_in: selected_sector_link_west_width_in input
            sector_count_in: sector_count_in input
            cooling_bundle_life_in: cooling_bundle_life_in input
            cooling_airlock_length_in: cooling_airlock_length_in input
            fuel_length_in: fuel_length_in input
            heat_rejection_width_in: heat_rejection_width_in input
            cooldown_days_in: cooldown_days_in input
            cryo_coldbox_width_in: cryo_coldbox_width_in input
            cooling_bundle_stations_in: cooling_bundle_stations_in input
            selected_cooling_link_length_in: selected_cooling_link_length_in input
            cooling_headroom_in: cooling_headroom_in input
            sector_clean_days_in: sector_clean_days_in input
            reactor_aux_height_in: reactor_aux_height_in input
            selected_sector_link_north_width_in: selected_sector_link_north_width_in input
            selected_cooling_annex_north_depth_in: selected_cooling_annex_north_depth_in input
            initial_receipt_lead_days_in: initial_receipt_lead_days_in input
            onsite_ac_height_in: onsite_ac_height_in input
            service_water_length_in: service_water_length_in input
            cooling_initial_handoff_days_in: cooling_initial_handoff_days_in input
            occupancy_height_in: occupancy_height_in input
            minor_outer_radius_in: minor_outer_radius_in input
            selected_cryo_compressors_height_in: selected_cryo_compressors_height_in input
            cooling_prepare_machine_days_in: cooling_prepare_machine_days_in input
            helium_package_height_in: helium_package_height_in input
            reactor_aux_width_in: reactor_aux_width_in input
            selected_sector_link_south_height_in: selected_sector_link_south_height_in input
            component_prepare_days_in: component_prepare_days_in input
            selected_cooling_hall_width_in: selected_cooling_hall_width_in input
            selected_parcel_width_in: selected_parcel_width_in input
            selected_control_width_in: selected_control_width_in input
            clean_positions_in: clean_positions_in input
            helium_package_width_in: helium_package_width_in input
            occupancy_circulation_factor_in: occupancy_circulation_factor_in input
            sector_route_clearance_in: sector_route_clearance_in input
            calendar_count_in: calendar_count_in input
            control_occupants_in: control_occupants_in input
            selected_parcel_y_min_in: selected_parcel_y_min_in input
            selected_cooling_annex_height_in: selected_cooling_annex_height_in input
            cooling_salt_count_in: cooling_salt_count_in input
            sector_test_days_in: sector_test_days_in input
            component_width_in: component_width_in input
            selected_maintenance_shop_width_in: selected_maintenance_shop_width_in input
            selected_power_supply_building_width_in: selected_power_supply_building_width_in input
            selected_power_supply_building_length_in: selected_power_supply_building_length_in input
            sector_transport_days_in: sector_transport_days_in input
            nuclear_wall_in: nuclear_wall_in input
            selected_security_length_in: selected_security_length_in input
            conventional_shop_length_in: conventional_shop_length_in input
            sector_bays_in: sector_bays_in input
            selected_reactor_hall_height_in: selected_reactor_hall_height_in input
            selected_maintenance_shop_length_in: selected_maintenance_shop_length_in input
            blanket_volume_in: blanket_volume_in input
            cryo_compressors_length_in: cryo_compressors_length_in input
            cooling_machine_process_days_in: cooling_machine_process_days_in input
            cryo_coldbox_height_in: cryo_coldbox_height_in input
            selected_parcel_length_in: selected_parcel_length_in input
            nuclear_rebar_density_in: nuclear_rebar_density_in input
            selected_cooling_link_width_in: selected_cooling_link_width_in input
            selected_reactor_hall_length_in: selected_reactor_hall_length_in input
            hx_shell_length_in: hx_shell_length_in input
            calendar_mode_in: calendar_mode_in input
            dirty_store_positions_in: dirty_store_positions_in input
            turbine_width_in: turbine_width_in input
            conventional_shop_height_in: conventional_shop_height_in input
            selected_administration_width_in: selected_administration_width_in input
            component_process_days_in: component_process_days_in input
            selected_sector_wing_north_height_in: selected_sector_wing_north_height_in input
            calendar_life_in: calendar_life_in input
            cryo_compressors_height_in: cryo_compressors_height_in input
            cooling_receipt_lead_days_in: cooling_receipt_lead_days_in input
            selected_security_height_in: selected_security_height_in input
            fuel_height_in: fuel_height_in input
            selected_electrical_building_length_in: selected_electrical_building_length_in input
            hx_shell_bore_in: hx_shell_bore_in input
            hx_shell_wall_in: hx_shell_wall_in input
            selected_turbine_hall_length_in: selected_turbine_hall_length_in input
            conventional_floor_in: conventional_floor_in input
            exterior_allowance_in: exterior_allowance_in input
            selected_security_width_in: selected_security_width_in input
            selected_reactor_hall_width_in: selected_reactor_hall_width_in input
            security_occupants_in: security_occupants_in input
            salt_package_width_in: salt_package_width_in input
            selected_sector_link_north_height_in: selected_sector_link_north_height_in input
            selected_turbine_hall_width_in: selected_turbine_hall_width_in input
            selected_fuel_building_length_in: selected_fuel_building_length_in input
            sector_split_days_in: sector_split_days_in input
            selected_blanket_packages_per_sector_in: selected_blanket_packages_per_sector_in input
            onsite_ac_width_in: onsite_ac_width_in input
            recommission_days_in: recommission_days_in input
            salt_package_length_in: salt_package_length_in input
            selected_maintenance_shop_height_in: selected_maintenance_shop_height_in input
            component_install_days_in: component_install_days_in input
            calendar_availability_in: calendar_availability_in input
            helium_package_length_in: helium_package_length_in input
            selected_reactor_auxiliaries_width_in: selected_reactor_auxiliaries_width_in input
            divertor_packages_per_sector_in: divertor_packages_per_sector_in input
            selected_sector_wing_east_width_in: selected_sector_wing_east_width_in input
            cooling_package_margin_in: cooling_package_margin_in input
            component_receipt_lead_days_in: component_receipt_lead_days_in input
            cooling_bundle_count_in: cooling_bundle_count_in input
            cooling_clean_helium_positions_in: cooling_clean_helium_positions_in input
            nuclear_roof_in: nuclear_roof_in input
            cryo_compressors_width_in: cryo_compressors_width_in input
            component_height_in: component_height_in input
            nuclear_floor_in: nuclear_floor_in input
            turbine_length_in: turbine_length_in input
            selected_reactor_auxiliaries_height_in: selected_reactor_auxiliaries_height_in input
            heat_rejection_length_in: heat_rejection_length_in input
            major_radius_in: major_radius_in input
            conventional_roof_in: conventional_roof_in input
            component_length_in: component_length_in input
            conventional_wall_in: conventional_wall_in input
            calendar_years_in: calendar_years_in input
            facilities_enabled_in: facilities_enabled_in input
            cooling_field_cycle_days_in: cooling_field_cycle_days_in input
            selected_cooling_salt_store_width_in: selected_cooling_salt_store_width_in input
            component_handling_margin_in: component_handling_margin_in input
            cooling_bundle_process_days_in: cooling_bundle_process_days_in input
            calendar_outage_in: calendar_outage_in input
            cooling_circuits_in: cooling_circuits_in input
            site_services_length_in: site_services_length_in input
            selected_sector_link_east_length_in: selected_sector_link_east_length_in input
            fuel_width_in: fuel_width_in input
            selected_sector_wing_south_height_in: selected_sector_wing_south_height_in input
            site_services_height_in: site_services_height_in input
            selected_sector_link_north_length_in: selected_sector_link_north_length_in input
            selected_cooling_annex_length_in: selected_cooling_annex_length_in input
            component_material_fraction_in: component_material_fraction_in input
            selected_sector_wing_east_height_in: selected_sector_wing_east_height_in input
            calendar_q_in: calendar_q_in input
            power_supply_width_in: power_supply_width_in input
            onsite_ac_length_in: onsite_ac_length_in input
            selected_cooling_annex_width_in: selected_cooling_annex_width_in input

        Returns:
            Module result with Facility_LayoutOutput (dirty_store_required, electrical_building_required_length, sector_link_north_clear_height, reactor_auxiliaries_sub_formwork, electrical_building_clear_height, dirty_store_positions_allocated, sector_wing_west_required_length, cryo_compressors_sub_formwork, sector_wing_east_clear_length, sector_wing_east_super_rebar, fuel_building_air_volume, turbine_hall_super_formwork, sector_link_north_clear_width, sector_wing_north_required_width, power_supply_building_clear_area, control_required_height, cooling_hall_clear_height, administration_sub_concrete, sector_wing_north_gross_area, administration_required_area, fuel_building_sub_rebar, sector_link_south_required_height, dirty_buffer_positions_allocated, sector_link_north_super_concrete, sector_wing_west_clear_length, cryo_coldbox_required_height, fuel_building_required_width, required_parcel_x_min, sector_wing_south_super_formwork, control_clear_width, sector_link_north_gross_area, electrical_building_super_formwork, cooling_annex_gross_area, replacement_ready_margin_days, cooling_annex_sub_formwork, maintenance_shop_clear_area, reactor_hall_gross_area, control_air_volume, sector_wing_south_required_length, site_services_building_sub_rebar, calendar_first_event_year, site_services_building_super_concrete, reactor_auxiliaries_gross_area, reactor_hall_required_height, service_water_building_clear_height, sector_link_south_required_width, sector_link_west_clear_area, occupancy_area_margin_m2, power_supply_building_gross_area, electrical_building_super_concrete, required_parcel_y_max, sector_link_south_super_concrete, site_services_building_sub_concrete, sector_link_south_sub_rebar, cryo_compressors_clear_area, electrical_building_clear_width, sector_wing_east_super_concrete, cooling_carrier_moves, cryo_coldbox_super_rebar, cryo_coldbox_super_formwork, cryo_coldbox_sub_formwork, sector_wing_east_sub_rebar, power_supply_building_sub_rebar, sector_link_south_clear_height, dirty_buffer_required, cooling_jobs_after_shutdown, service_water_building_super_rebar, fuel_building_clear_area, cooling_link_clear_width, cooling_annex_super_formwork, site_services_building_required_width, cooling_annex_required_height, reactor_auxiliaries_super_formwork, reactor_hall_clear_height, sector_link_north_air_volume, sector_wing_south_required_width, control_sub_rebar, service_water_building_clear_area, sector_wing_west_clear_height, sector_wing_south_sub_rebar, sector_wing_south_required_height, sector_link_west_super_concrete, administration_sub_rebar, cooling_hall_clear_width, exterior_envelope_qualified, outage_required_days, security_clear_width, fuel_building_super_formwork, power_supply_building_clear_width, service_water_building_sub_concrete, cryo_compressors_super_formwork, cryo_coldbox_clear_length, cryo_compressors_required_length, control_clear_length, calendar_last_event_year, turbine_hall_clear_width, controlled_air_volume, service_water_building_required_length, cooling_replacement_ready_margin_days, sector_link_west_air_volume, sector_link_north_clear_area, maintenance_shop_clear_length, blanket_packages_per_sector, maintenance_shop_clear_height, cooling_hall_super_formwork, maintenance_shop_required_width, sector_link_east_clear_area, sector_wing_north_super_rebar, turbine_hall_clear_height, sector_width, service_water_building_clear_length, active, maintenance_shop_sub_formwork, sector_wing_west_air_volume, site_services_building_clear_width, reactor_auxiliaries_required_height, cryo_compressors_sub_rebar, cooling_link_required_length, sector_wing_north_sub_formwork, power_supply_building_required_width, sector_wing_west_super_concrete, electrical_building_sub_formwork, turbine_hall_required_height, cryo_coldbox_clear_width, sector_wing_east_sub_formwork, reactor_auxiliaries_air_volume, sector_link_east_sub_rebar, cooling_link_sub_concrete, security_required_height, sector_wing_east_clear_area, site_services_building_clear_area, sector_link_north_required_height, cooling_annex_super_rebar, power_supply_building_sub_formwork, cooling_link_air_volume, cryo_compressors_clear_height, maintenance_shop_super_concrete, cooling_hall_sub_rebar, sector_wing_east_sub_concrete, cooling_helium_queue_peak, fuel_building_clear_height, service_water_building_clear_width, sector_link_south_required_length, administration_clear_area, cryo_coldbox_required_width, cooling_link_clear_area, site_services_building_sub_formwork, turbine_hall_super_rebar, cooling_salt_queue_peak, sector_link_south_air_volume, cooling_dirty_bundle_required, sector_wing_east_clear_width, sector_link_east_super_formwork, security_air_volume, reactor_auxiliaries_super_rebar, service_water_building_super_formwork, reactor_hall_clear_length, reactor_hall_sub_formwork, sector_link_east_required_length, cooling_hall_clear_area, sector_wing_west_sub_rebar, administration_air_volume, turbine_hall_clear_length, sector_link_south_clear_length, sector_wing_east_clear_height, turbine_hall_clear_area, sector_link_east_required_height, sector_wing_west_sub_formwork, service_water_building_required_height, sector_link_south_super_rebar, control_gross_area, fuel_building_gross_area, sector_length, cooling_annex_sub_rebar, cooling_annex_clear_area, calendar_event_count, sector_link_west_sub_formwork, sector_wing_west_clear_width, security_sub_concrete, fuel_building_super_concrete, cooling_clean_salt_allocated, cryo_compressors_gross_area, sector_link_east_clear_length, cooling_annex_air_volume, cryo_coldbox_clear_area, sector_wing_south_gross_area, cooling_outage_basis_resolved, turbine_hall_required_width, sector_wing_north_clear_length, cryo_compressors_required_height, turbine_hall_sub_concrete, contamination_procedure_qualified, cooling_hall_super_concrete, turbine_hall_super_concrete, control_super_rebar, sector_link_north_sub_rebar, maintenance_shop_sub_concrete, sector_link_south_clear_width, parcel_area, sector_wing_south_super_concrete, cryo_coldbox_required_length, administration_clear_length, sector_link_east_air_volume, security_clear_height, sector_wing_south_clear_height, reactor_auxiliaries_clear_height, packages_per_sector, security_sub_rebar, maintenance_shop_required_length, administration_required_height, sector_link_east_sub_concrete, sector_wing_east_gross_area, sector_link_east_super_rebar, fuel_building_clear_length, security_super_rebar, cryo_compressors_sub_concrete, service_water_building_super_concrete, reactor_hall_sub_concrete, service_water_building_sub_formwork, sector_link_east_sub_formwork, security_sub_formwork, security_super_concrete, sector_wing_west_clear_area, cryo_compressors_super_rebar, control_clear_area, cooling_annex_super_concrete, control_super_formwork, turbine_hall_sub_formwork, electrical_building_air_volume, cooling_hall_air_volume, sector_link_west_sub_rebar, cooling_hall_required_height, sector_wing_east_air_volume, sector_wing_south_clear_area, sector_link_east_gross_area, cooling_link_required_width, outage_allowed_days, cooling_annex_clear_length, sector_wing_north_sub_rebar, sector_link_west_super_formwork, initial_margin_days, sector_wing_east_required_height, sector_wing_east_required_length, service_water_building_sub_rebar, site_services_building_clear_height, administration_clear_width, maintenance_shop_clear_width, cooling_last_release_year, sector_wing_north_required_height, power_supply_building_clear_height, reactor_hall_required_length, cooling_dirty_salt_allocated, reactor_hall_sub_rebar, sector_link_east_clear_height, cooling_hall_required_width, site_services_building_super_rebar, sector_link_north_required_width, cryo_compressors_clear_width, turbine_hall_gross_area, reactor_hall_required_width, sector_link_north_required_length, sector_link_west_clear_length, control_sub_concrete, power_supply_building_super_concrete, electrical_building_required_height, reactor_auxiliaries_super_concrete, site_services_building_gross_area, reactor_auxiliaries_required_length, fuel_building_super_rebar, fuel_building_required_height, cooling_initial_ready_margin_days, sector_link_east_required_width, electrical_building_sub_concrete, security_gross_area, sector_link_north_sub_concrete, sector_wing_south_sub_concrete, cooling_annex_required_length, turbine_hall_required_length, geometry_fit_margin_m, readiness_margin_days, sector_wing_north_air_volume, power_supply_building_air_volume, total_gross_area, sector_wing_north_sub_concrete, cooling_annex_required_width, cryo_compressors_required_width, required_parcel_x_max, sector_wing_north_clear_area, cooling_bundle_queue_peak, cooling_annex_clear_height, power_supply_building_required_length, cooling_link_clear_length, initial_clean_required, power_supply_building_super_rebar, capacity_margin_units, cooling_link_sub_rebar, reactor_hall_clear_area, parcel_fit_margin_m, sector_link_south_gross_area, sector_link_north_super_rebar, sector_wing_south_super_rebar, blanket_packages_required_per_sector, cooling_dirty_helium_required, maintenance_shop_required_height, total_air_volume, cryo_compressors_clear_length, service_water_building_required_width, site_services_building_air_volume, sector_link_west_sub_concrete, administration_super_rebar, security_super_formwork, cryo_coldbox_sub_rebar, sector_link_south_sub_concrete, cooling_clean_bundle_required, cooling_clean_helium_allocated, route_margin_m, sector_link_west_clear_width, electrical_building_clear_area, sector_link_west_super_rebar, clean_positions_allocated, cooling_link_sub_formwork, cryo_coldbox_air_volume, cooling_hall_super_rebar, sector_wing_west_super_formwork, reactor_auxiliaries_clear_area, reactor_auxiliaries_sub_concrete, fuel_building_required_length, reactor_auxiliaries_sub_rebar, sector_wing_west_sub_concrete, cooling_dirty_bundle_allocated, cooling_hall_gross_area, sector_link_south_sub_formwork, sector_load_qualified, cryo_coldbox_clear_height, sector_link_north_sub_formwork, sector_wing_south_air_volume, outage_margin_days, sector_wing_north_super_concrete, cryo_coldbox_super_concrete, maintenance_shop_gross_area, site_services_building_required_height, sector_wing_west_super_rebar, sector_wing_north_clear_height, sector_link_south_super_formwork, sector_link_west_gross_area, cooling_hall_clear_length, sector_wing_west_required_width, administration_super_concrete, sector_link_north_clear_length, reactor_hall_super_concrete, administration_sub_formwork, turbine_hall_sub_rebar, site_services_building_clear_length, power_supply_building_sub_concrete, reactor_hall_air_volume, reactor_auxiliaries_clear_length, administration_super_formwork, site_services_building_super_formwork, administration_gross_area, material_capacity_volume, cooling_annex_clear_width, cooling_link_required_height, cooling_link_gross_area, cost_mode, cooling_clean_helium_required, control_required_area, cooling_link_clear_height, maintenance_shop_super_formwork, sector_link_east_clear_width, sector_wing_north_clear_width, maintenance_shop_sub_rebar, total_clear_area, cryo_compressors_air_volume, sector_wing_west_required_height, reactor_hall_super_rebar, cooling_dirty_helium_allocated, sector_link_east_super_concrete, sector_wing_north_required_length, turbine_hall_air_volume, provisional_room_count, sector_wing_south_clear_width, sector_link_west_required_height, sector_wing_south_clear_length, cooling_hall_sub_formwork, cryo_coldbox_sub_concrete, power_supply_building_super_formwork, fuel_building_sub_concrete, sector_link_south_clear_area, security_clear_length, cooling_link_super_concrete, reactor_auxiliaries_clear_width, site_services_building_required_length, cryo_compressors_super_concrete, required_parcel_y_min, sector_wing_east_required_width, cryo_coldbox_gross_area, cooling_hall_required_length, electrical_building_required_width, fuel_building_clear_width, administration_clear_height, security_required_area, service_water_building_gross_area, electrical_building_gross_area, initial_ready_margin_days, power_supply_building_clear_length, cooling_annex_sub_concrete, sector_link_west_required_length, fuel_building_sub_formwork, power_supply_building_required_height, cooling_clean_bundle_allocated, unused_material_capacity, cooling_hall_sub_concrete, maintenance_shop_super_rebar, sector_wing_west_gross_area, service_water_building_air_volume, sector_link_north_super_formwork, sector_wing_south_sub_formwork, reactor_hall_clear_width, sector_height, sector_wing_east_super_formwork, cooling_link_super_rebar, control_sub_formwork, maintenance_shop_air_volume, cooling_dirty_salt_required, control_clear_height, control_super_concrete, cooling_link_super_formwork, sector_link_west_clear_height, electrical_building_super_rebar, cooling_clean_salt_required, electrical_building_clear_length, reactor_auxiliaries_required_width, electrical_building_sub_rebar, security_clear_area, reactor_hall_super_formwork, sector_link_west_required_width, sector_wing_north_super_formwork)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(selected_site_services_building_height_in, selected_sector_link_east_width_in, selected_cooling_helium_store_width_in, selected_cooling_bundle_store_width_in, cooling_dirty_helium_positions_in, salt_package_height_in, selected_site_services_building_width_in, selected_sector_wing_south_length_in, selected_service_water_building_length_in, dirty_buffer_positions_in, building_separation_in, cooling_internal_move_days_in, cooling_cross_width_in, provisional_envelope_scale_in, site_services_width_in, hx_end_allowance_in, selected_sector_wing_south_width_in, selected_fuel_building_width_in, selected_sector_link_south_width_in, selected_sector_wing_west_width_in, selected_sector_wing_east_length_in, selected_turbine_hall_height_in, sector_join_days_in, selected_cryo_compressors_length_in, cooling_machine_stations_in, cooling_prepare_stations_in, reactor_aux_length_in, selected_parcel_x_min_in, turbine_height_in, selected_service_water_building_width_in, selected_cryo_coldbox_length_in, calendar_unplanned_in, selected_cooling_hall_height_in, n_mod_in, control_area_per_person_in, administration_occupants_in, cooling_helium_count_in, selected_cryo_compressors_width_in, selected_cryo_coldbox_height_in, cooling_aisle_width_in, selected_cooling_hall_length_in, sector_service_teams_in, cooling_hold_days_in, service_water_height_in, selected_service_water_building_height_in, cooling_dirty_bundle_positions_in, cooling_clean_salt_positions_in, selected_sector_link_west_height_in, selected_sector_link_east_height_in, waste_package_yield_in, selected_administration_length_in, cooling_prepare_bundle_days_in, selected_administration_height_in, selected_cryo_coldbox_width_in, sector_headroom_in, initial_sector_start_days_in, cooling_clean_bundle_positions_in, selected_electrical_building_width_in, selected_power_supply_building_height_in, hx_tube_length_in, conventional_rebar_density_in, selected_sector_wing_west_length_in, selected_sector_wing_west_height_in, selected_control_length_in, power_supply_length_in, component_remove_days_in, calendar_fluence_in, cryo_coldbox_length_in, administration_area_per_person_in, selected_sector_wing_north_length_in, facilities_cost_mode_in, selected_fuel_building_height_in, component_hold_days_in, selected_site_services_building_length_in, selected_sector_link_south_length_in, selected_sector_link_west_length_in, selected_reactor_auxiliaries_length_in, selected_electrical_building_height_in, selected_control_height_in, external_access_width_in, conventional_shop_width_in, cooling_machine_life_in, cooling_dirty_salt_positions_in, power_supply_height_in, selected_sector_wing_north_width_in, security_area_per_person_in, cooling_initial_receipt_lead_days_in, service_water_width_in, selected_cooling_link_height_in, selected_sector_link_west_width_in, sector_count_in, cooling_bundle_life_in, cooling_airlock_length_in, fuel_length_in, heat_rejection_width_in, cooldown_days_in, cryo_coldbox_width_in, cooling_bundle_stations_in, selected_cooling_link_length_in, cooling_headroom_in, sector_clean_days_in, reactor_aux_height_in, selected_sector_link_north_width_in, selected_cooling_annex_north_depth_in, initial_receipt_lead_days_in, onsite_ac_height_in, service_water_length_in, cooling_initial_handoff_days_in, occupancy_height_in, minor_outer_radius_in, selected_cryo_compressors_height_in, cooling_prepare_machine_days_in, helium_package_height_in, reactor_aux_width_in, selected_sector_link_south_height_in, component_prepare_days_in, selected_cooling_hall_width_in, selected_parcel_width_in, selected_control_width_in, clean_positions_in, helium_package_width_in, occupancy_circulation_factor_in, sector_route_clearance_in, calendar_count_in, control_occupants_in, selected_parcel_y_min_in, selected_cooling_annex_height_in, cooling_salt_count_in, sector_test_days_in, component_width_in, selected_maintenance_shop_width_in, selected_power_supply_building_width_in, selected_power_supply_building_length_in, sector_transport_days_in, nuclear_wall_in, selected_security_length_in, conventional_shop_length_in, sector_bays_in, selected_reactor_hall_height_in, selected_maintenance_shop_length_in, blanket_volume_in, cryo_compressors_length_in, cooling_machine_process_days_in, cryo_coldbox_height_in, selected_parcel_length_in, nuclear_rebar_density_in, selected_cooling_link_width_in, selected_reactor_hall_length_in, hx_shell_length_in, calendar_mode_in, dirty_store_positions_in, turbine_width_in, conventional_shop_height_in, selected_administration_width_in, component_process_days_in, selected_sector_wing_north_height_in, calendar_life_in, cryo_compressors_height_in, cooling_receipt_lead_days_in, selected_security_height_in, fuel_height_in, selected_electrical_building_length_in, hx_shell_bore_in, hx_shell_wall_in, selected_turbine_hall_length_in, conventional_floor_in, exterior_allowance_in, selected_security_width_in, selected_reactor_hall_width_in, security_occupants_in, salt_package_width_in, selected_sector_link_north_height_in, selected_turbine_hall_width_in, selected_fuel_building_length_in, sector_split_days_in, selected_blanket_packages_per_sector_in, onsite_ac_width_in, recommission_days_in, salt_package_length_in, selected_maintenance_shop_height_in, component_install_days_in, calendar_availability_in, helium_package_length_in, selected_reactor_auxiliaries_width_in, divertor_packages_per_sector_in, selected_sector_wing_east_width_in, cooling_package_margin_in, component_receipt_lead_days_in, cooling_bundle_count_in, cooling_clean_helium_positions_in, nuclear_roof_in, cryo_compressors_width_in, component_height_in, nuclear_floor_in, turbine_length_in, selected_reactor_auxiliaries_height_in, heat_rejection_length_in, major_radius_in, conventional_roof_in, component_length_in, conventional_wall_in, calendar_years_in, facilities_enabled_in, cooling_field_cycle_days_in, selected_cooling_salt_store_width_in, component_handling_margin_in, cooling_bundle_process_days_in, calendar_outage_in, cooling_circuits_in, site_services_length_in, selected_sector_link_east_length_in, fuel_width_in, selected_sector_wing_south_height_in, site_services_height_in, selected_sector_link_north_length_in, selected_cooling_annex_length_in, component_material_fraction_in, selected_sector_wing_east_height_in, calendar_q_in, power_supply_width_in, onsite_ac_length_in, selected_cooling_annex_width_in)

        # Import handwritten implementation
        from stellarator_materials_rebco_tea.handwritten.mfe_facilities.facility_layout_impl import (
            run_facility_layout,
        )

        # Execute implementation - returns tuple of values
        dirty_store_required, electrical_building_required_length, sector_link_north_clear_height, reactor_auxiliaries_sub_formwork, electrical_building_clear_height, dirty_store_positions_allocated, sector_wing_west_required_length, cryo_compressors_sub_formwork, sector_wing_east_clear_length, sector_wing_east_super_rebar, fuel_building_air_volume, turbine_hall_super_formwork, sector_link_north_clear_width, sector_wing_north_required_width, power_supply_building_clear_area, control_required_height, cooling_hall_clear_height, administration_sub_concrete, sector_wing_north_gross_area, administration_required_area, fuel_building_sub_rebar, sector_link_south_required_height, dirty_buffer_positions_allocated, sector_link_north_super_concrete, sector_wing_west_clear_length, cryo_coldbox_required_height, fuel_building_required_width, required_parcel_x_min, sector_wing_south_super_formwork, control_clear_width, sector_link_north_gross_area, electrical_building_super_formwork, cooling_annex_gross_area, replacement_ready_margin_days, cooling_annex_sub_formwork, maintenance_shop_clear_area, reactor_hall_gross_area, control_air_volume, sector_wing_south_required_length, site_services_building_sub_rebar, calendar_first_event_year, site_services_building_super_concrete, reactor_auxiliaries_gross_area, reactor_hall_required_height, service_water_building_clear_height, sector_link_south_required_width, sector_link_west_clear_area, occupancy_area_margin_m2, power_supply_building_gross_area, electrical_building_super_concrete, required_parcel_y_max, sector_link_south_super_concrete, site_services_building_sub_concrete, sector_link_south_sub_rebar, cryo_compressors_clear_area, electrical_building_clear_width, sector_wing_east_super_concrete, cooling_carrier_moves, cryo_coldbox_super_rebar, cryo_coldbox_super_formwork, cryo_coldbox_sub_formwork, sector_wing_east_sub_rebar, power_supply_building_sub_rebar, sector_link_south_clear_height, dirty_buffer_required, cooling_jobs_after_shutdown, service_water_building_super_rebar, fuel_building_clear_area, cooling_link_clear_width, cooling_annex_super_formwork, site_services_building_required_width, cooling_annex_required_height, reactor_auxiliaries_super_formwork, reactor_hall_clear_height, sector_link_north_air_volume, sector_wing_south_required_width, control_sub_rebar, service_water_building_clear_area, sector_wing_west_clear_height, sector_wing_south_sub_rebar, sector_wing_south_required_height, sector_link_west_super_concrete, administration_sub_rebar, cooling_hall_clear_width, exterior_envelope_qualified, outage_required_days, security_clear_width, fuel_building_super_formwork, power_supply_building_clear_width, service_water_building_sub_concrete, cryo_compressors_super_formwork, cryo_coldbox_clear_length, cryo_compressors_required_length, control_clear_length, calendar_last_event_year, turbine_hall_clear_width, controlled_air_volume, service_water_building_required_length, cooling_replacement_ready_margin_days, sector_link_west_air_volume, sector_link_north_clear_area, maintenance_shop_clear_length, blanket_packages_per_sector, maintenance_shop_clear_height, cooling_hall_super_formwork, maintenance_shop_required_width, sector_link_east_clear_area, sector_wing_north_super_rebar, turbine_hall_clear_height, sector_width, service_water_building_clear_length, active, maintenance_shop_sub_formwork, sector_wing_west_air_volume, site_services_building_clear_width, reactor_auxiliaries_required_height, cryo_compressors_sub_rebar, cooling_link_required_length, sector_wing_north_sub_formwork, power_supply_building_required_width, sector_wing_west_super_concrete, electrical_building_sub_formwork, turbine_hall_required_height, cryo_coldbox_clear_width, sector_wing_east_sub_formwork, reactor_auxiliaries_air_volume, sector_link_east_sub_rebar, cooling_link_sub_concrete, security_required_height, sector_wing_east_clear_area, site_services_building_clear_area, sector_link_north_required_height, cooling_annex_super_rebar, power_supply_building_sub_formwork, cooling_link_air_volume, cryo_compressors_clear_height, maintenance_shop_super_concrete, cooling_hall_sub_rebar, sector_wing_east_sub_concrete, cooling_helium_queue_peak, fuel_building_clear_height, service_water_building_clear_width, sector_link_south_required_length, administration_clear_area, cryo_coldbox_required_width, cooling_link_clear_area, site_services_building_sub_formwork, turbine_hall_super_rebar, cooling_salt_queue_peak, sector_link_south_air_volume, cooling_dirty_bundle_required, sector_wing_east_clear_width, sector_link_east_super_formwork, security_air_volume, reactor_auxiliaries_super_rebar, service_water_building_super_formwork, reactor_hall_clear_length, reactor_hall_sub_formwork, sector_link_east_required_length, cooling_hall_clear_area, sector_wing_west_sub_rebar, administration_air_volume, turbine_hall_clear_length, sector_link_south_clear_length, sector_wing_east_clear_height, turbine_hall_clear_area, sector_link_east_required_height, sector_wing_west_sub_formwork, service_water_building_required_height, sector_link_south_super_rebar, control_gross_area, fuel_building_gross_area, sector_length, cooling_annex_sub_rebar, cooling_annex_clear_area, calendar_event_count, sector_link_west_sub_formwork, sector_wing_west_clear_width, security_sub_concrete, fuel_building_super_concrete, cooling_clean_salt_allocated, cryo_compressors_gross_area, sector_link_east_clear_length, cooling_annex_air_volume, cryo_coldbox_clear_area, sector_wing_south_gross_area, cooling_outage_basis_resolved, turbine_hall_required_width, sector_wing_north_clear_length, cryo_compressors_required_height, turbine_hall_sub_concrete, contamination_procedure_qualified, cooling_hall_super_concrete, turbine_hall_super_concrete, control_super_rebar, sector_link_north_sub_rebar, maintenance_shop_sub_concrete, sector_link_south_clear_width, parcel_area, sector_wing_south_super_concrete, cryo_coldbox_required_length, administration_clear_length, sector_link_east_air_volume, security_clear_height, sector_wing_south_clear_height, reactor_auxiliaries_clear_height, packages_per_sector, security_sub_rebar, maintenance_shop_required_length, administration_required_height, sector_link_east_sub_concrete, sector_wing_east_gross_area, sector_link_east_super_rebar, fuel_building_clear_length, security_super_rebar, cryo_compressors_sub_concrete, service_water_building_super_concrete, reactor_hall_sub_concrete, service_water_building_sub_formwork, sector_link_east_sub_formwork, security_sub_formwork, security_super_concrete, sector_wing_west_clear_area, cryo_compressors_super_rebar, control_clear_area, cooling_annex_super_concrete, control_super_formwork, turbine_hall_sub_formwork, electrical_building_air_volume, cooling_hall_air_volume, sector_link_west_sub_rebar, cooling_hall_required_height, sector_wing_east_air_volume, sector_wing_south_clear_area, sector_link_east_gross_area, cooling_link_required_width, outage_allowed_days, cooling_annex_clear_length, sector_wing_north_sub_rebar, sector_link_west_super_formwork, initial_margin_days, sector_wing_east_required_height, sector_wing_east_required_length, service_water_building_sub_rebar, site_services_building_clear_height, administration_clear_width, maintenance_shop_clear_width, cooling_last_release_year, sector_wing_north_required_height, power_supply_building_clear_height, reactor_hall_required_length, cooling_dirty_salt_allocated, reactor_hall_sub_rebar, sector_link_east_clear_height, cooling_hall_required_width, site_services_building_super_rebar, sector_link_north_required_width, cryo_compressors_clear_width, turbine_hall_gross_area, reactor_hall_required_width, sector_link_north_required_length, sector_link_west_clear_length, control_sub_concrete, power_supply_building_super_concrete, electrical_building_required_height, reactor_auxiliaries_super_concrete, site_services_building_gross_area, reactor_auxiliaries_required_length, fuel_building_super_rebar, fuel_building_required_height, cooling_initial_ready_margin_days, sector_link_east_required_width, electrical_building_sub_concrete, security_gross_area, sector_link_north_sub_concrete, sector_wing_south_sub_concrete, cooling_annex_required_length, turbine_hall_required_length, geometry_fit_margin_m, readiness_margin_days, sector_wing_north_air_volume, power_supply_building_air_volume, total_gross_area, sector_wing_north_sub_concrete, cooling_annex_required_width, cryo_compressors_required_width, required_parcel_x_max, sector_wing_north_clear_area, cooling_bundle_queue_peak, cooling_annex_clear_height, power_supply_building_required_length, cooling_link_clear_length, initial_clean_required, power_supply_building_super_rebar, capacity_margin_units, cooling_link_sub_rebar, reactor_hall_clear_area, parcel_fit_margin_m, sector_link_south_gross_area, sector_link_north_super_rebar, sector_wing_south_super_rebar, blanket_packages_required_per_sector, cooling_dirty_helium_required, maintenance_shop_required_height, total_air_volume, cryo_compressors_clear_length, service_water_building_required_width, site_services_building_air_volume, sector_link_west_sub_concrete, administration_super_rebar, security_super_formwork, cryo_coldbox_sub_rebar, sector_link_south_sub_concrete, cooling_clean_bundle_required, cooling_clean_helium_allocated, route_margin_m, sector_link_west_clear_width, electrical_building_clear_area, sector_link_west_super_rebar, clean_positions_allocated, cooling_link_sub_formwork, cryo_coldbox_air_volume, cooling_hall_super_rebar, sector_wing_west_super_formwork, reactor_auxiliaries_clear_area, reactor_auxiliaries_sub_concrete, fuel_building_required_length, reactor_auxiliaries_sub_rebar, sector_wing_west_sub_concrete, cooling_dirty_bundle_allocated, cooling_hall_gross_area, sector_link_south_sub_formwork, sector_load_qualified, cryo_coldbox_clear_height, sector_link_north_sub_formwork, sector_wing_south_air_volume, outage_margin_days, sector_wing_north_super_concrete, cryo_coldbox_super_concrete, maintenance_shop_gross_area, site_services_building_required_height, sector_wing_west_super_rebar, sector_wing_north_clear_height, sector_link_south_super_formwork, sector_link_west_gross_area, cooling_hall_clear_length, sector_wing_west_required_width, administration_super_concrete, sector_link_north_clear_length, reactor_hall_super_concrete, administration_sub_formwork, turbine_hall_sub_rebar, site_services_building_clear_length, power_supply_building_sub_concrete, reactor_hall_air_volume, reactor_auxiliaries_clear_length, administration_super_formwork, site_services_building_super_formwork, administration_gross_area, material_capacity_volume, cooling_annex_clear_width, cooling_link_required_height, cooling_link_gross_area, cost_mode, cooling_clean_helium_required, control_required_area, cooling_link_clear_height, maintenance_shop_super_formwork, sector_link_east_clear_width, sector_wing_north_clear_width, maintenance_shop_sub_rebar, total_clear_area, cryo_compressors_air_volume, sector_wing_west_required_height, reactor_hall_super_rebar, cooling_dirty_helium_allocated, sector_link_east_super_concrete, sector_wing_north_required_length, turbine_hall_air_volume, provisional_room_count, sector_wing_south_clear_width, sector_link_west_required_height, sector_wing_south_clear_length, cooling_hall_sub_formwork, cryo_coldbox_sub_concrete, power_supply_building_super_formwork, fuel_building_sub_concrete, sector_link_south_clear_area, security_clear_length, cooling_link_super_concrete, reactor_auxiliaries_clear_width, site_services_building_required_length, cryo_compressors_super_concrete, required_parcel_y_min, sector_wing_east_required_width, cryo_coldbox_gross_area, cooling_hall_required_length, electrical_building_required_width, fuel_building_clear_width, administration_clear_height, security_required_area, service_water_building_gross_area, electrical_building_gross_area, initial_ready_margin_days, power_supply_building_clear_length, cooling_annex_sub_concrete, sector_link_west_required_length, fuel_building_sub_formwork, power_supply_building_required_height, cooling_clean_bundle_allocated, unused_material_capacity, cooling_hall_sub_concrete, maintenance_shop_super_rebar, sector_wing_west_gross_area, service_water_building_air_volume, sector_link_north_super_formwork, sector_wing_south_sub_formwork, reactor_hall_clear_width, sector_height, sector_wing_east_super_formwork, cooling_link_super_rebar, control_sub_formwork, maintenance_shop_air_volume, cooling_dirty_salt_required, control_clear_height, control_super_concrete, cooling_link_super_formwork, sector_link_west_clear_height, electrical_building_super_rebar, cooling_clean_salt_required, electrical_building_clear_length, reactor_auxiliaries_required_width, electrical_building_sub_rebar, security_clear_area, reactor_hall_super_formwork, sector_link_west_required_width, sector_wing_north_super_formwork = run_facility_layout(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Facility_LayoutOutput(
                dirty_store_required=dirty_store_required,
                electrical_building_required_length=electrical_building_required_length,
                sector_link_north_clear_height=sector_link_north_clear_height,
                reactor_auxiliaries_sub_formwork=reactor_auxiliaries_sub_formwork,
                electrical_building_clear_height=electrical_building_clear_height,
                dirty_store_positions_allocated=dirty_store_positions_allocated,
                sector_wing_west_required_length=sector_wing_west_required_length,
                cryo_compressors_sub_formwork=cryo_compressors_sub_formwork,
                sector_wing_east_clear_length=sector_wing_east_clear_length,
                sector_wing_east_super_rebar=sector_wing_east_super_rebar,
                fuel_building_air_volume=fuel_building_air_volume,
                turbine_hall_super_formwork=turbine_hall_super_formwork,
                sector_link_north_clear_width=sector_link_north_clear_width,
                sector_wing_north_required_width=sector_wing_north_required_width,
                power_supply_building_clear_area=power_supply_building_clear_area,
                control_required_height=control_required_height,
                cooling_hall_clear_height=cooling_hall_clear_height,
                administration_sub_concrete=administration_sub_concrete,
                sector_wing_north_gross_area=sector_wing_north_gross_area,
                administration_required_area=administration_required_area,
                fuel_building_sub_rebar=fuel_building_sub_rebar,
                sector_link_south_required_height=sector_link_south_required_height,
                dirty_buffer_positions_allocated=dirty_buffer_positions_allocated,
                sector_link_north_super_concrete=sector_link_north_super_concrete,
                sector_wing_west_clear_length=sector_wing_west_clear_length,
                cryo_coldbox_required_height=cryo_coldbox_required_height,
                fuel_building_required_width=fuel_building_required_width,
                required_parcel_x_min=required_parcel_x_min,
                sector_wing_south_super_formwork=sector_wing_south_super_formwork,
                control_clear_width=control_clear_width,
                sector_link_north_gross_area=sector_link_north_gross_area,
                electrical_building_super_formwork=electrical_building_super_formwork,
                cooling_annex_gross_area=cooling_annex_gross_area,
                replacement_ready_margin_days=replacement_ready_margin_days,
                cooling_annex_sub_formwork=cooling_annex_sub_formwork,
                maintenance_shop_clear_area=maintenance_shop_clear_area,
                reactor_hall_gross_area=reactor_hall_gross_area,
                control_air_volume=control_air_volume,
                sector_wing_south_required_length=sector_wing_south_required_length,
                site_services_building_sub_rebar=site_services_building_sub_rebar,
                calendar_first_event_year=calendar_first_event_year,
                site_services_building_super_concrete=site_services_building_super_concrete,
                reactor_auxiliaries_gross_area=reactor_auxiliaries_gross_area,
                reactor_hall_required_height=reactor_hall_required_height,
                service_water_building_clear_height=service_water_building_clear_height,
                sector_link_south_required_width=sector_link_south_required_width,
                sector_link_west_clear_area=sector_link_west_clear_area,
                occupancy_area_margin_m2=occupancy_area_margin_m2,
                power_supply_building_gross_area=power_supply_building_gross_area,
                electrical_building_super_concrete=electrical_building_super_concrete,
                required_parcel_y_max=required_parcel_y_max,
                sector_link_south_super_concrete=sector_link_south_super_concrete,
                site_services_building_sub_concrete=site_services_building_sub_concrete,
                sector_link_south_sub_rebar=sector_link_south_sub_rebar,
                cryo_compressors_clear_area=cryo_compressors_clear_area,
                electrical_building_clear_width=electrical_building_clear_width,
                sector_wing_east_super_concrete=sector_wing_east_super_concrete,
                cooling_carrier_moves=cooling_carrier_moves,
                cryo_coldbox_super_rebar=cryo_coldbox_super_rebar,
                cryo_coldbox_super_formwork=cryo_coldbox_super_formwork,
                cryo_coldbox_sub_formwork=cryo_coldbox_sub_formwork,
                sector_wing_east_sub_rebar=sector_wing_east_sub_rebar,
                power_supply_building_sub_rebar=power_supply_building_sub_rebar,
                sector_link_south_clear_height=sector_link_south_clear_height,
                dirty_buffer_required=dirty_buffer_required,
                cooling_jobs_after_shutdown=cooling_jobs_after_shutdown,
                service_water_building_super_rebar=service_water_building_super_rebar,
                fuel_building_clear_area=fuel_building_clear_area,
                cooling_link_clear_width=cooling_link_clear_width,
                cooling_annex_super_formwork=cooling_annex_super_formwork,
                site_services_building_required_width=site_services_building_required_width,
                cooling_annex_required_height=cooling_annex_required_height,
                reactor_auxiliaries_super_formwork=reactor_auxiliaries_super_formwork,
                reactor_hall_clear_height=reactor_hall_clear_height,
                sector_link_north_air_volume=sector_link_north_air_volume,
                sector_wing_south_required_width=sector_wing_south_required_width,
                control_sub_rebar=control_sub_rebar,
                service_water_building_clear_area=service_water_building_clear_area,
                sector_wing_west_clear_height=sector_wing_west_clear_height,
                sector_wing_south_sub_rebar=sector_wing_south_sub_rebar,
                sector_wing_south_required_height=sector_wing_south_required_height,
                sector_link_west_super_concrete=sector_link_west_super_concrete,
                administration_sub_rebar=administration_sub_rebar,
                cooling_hall_clear_width=cooling_hall_clear_width,
                exterior_envelope_qualified=exterior_envelope_qualified,
                outage_required_days=outage_required_days,
                security_clear_width=security_clear_width,
                fuel_building_super_formwork=fuel_building_super_formwork,
                power_supply_building_clear_width=power_supply_building_clear_width,
                service_water_building_sub_concrete=service_water_building_sub_concrete,
                cryo_compressors_super_formwork=cryo_compressors_super_formwork,
                cryo_coldbox_clear_length=cryo_coldbox_clear_length,
                cryo_compressors_required_length=cryo_compressors_required_length,
                control_clear_length=control_clear_length,
                calendar_last_event_year=calendar_last_event_year,
                turbine_hall_clear_width=turbine_hall_clear_width,
                controlled_air_volume=controlled_air_volume,
                service_water_building_required_length=service_water_building_required_length,
                cooling_replacement_ready_margin_days=cooling_replacement_ready_margin_days,
                sector_link_west_air_volume=sector_link_west_air_volume,
                sector_link_north_clear_area=sector_link_north_clear_area,
                maintenance_shop_clear_length=maintenance_shop_clear_length,
                blanket_packages_per_sector=blanket_packages_per_sector,
                maintenance_shop_clear_height=maintenance_shop_clear_height,
                cooling_hall_super_formwork=cooling_hall_super_formwork,
                maintenance_shop_required_width=maintenance_shop_required_width,
                sector_link_east_clear_area=sector_link_east_clear_area,
                sector_wing_north_super_rebar=sector_wing_north_super_rebar,
                turbine_hall_clear_height=turbine_hall_clear_height,
                sector_width=sector_width,
                service_water_building_clear_length=service_water_building_clear_length,
                active=active,
                maintenance_shop_sub_formwork=maintenance_shop_sub_formwork,
                sector_wing_west_air_volume=sector_wing_west_air_volume,
                site_services_building_clear_width=site_services_building_clear_width,
                reactor_auxiliaries_required_height=reactor_auxiliaries_required_height,
                cryo_compressors_sub_rebar=cryo_compressors_sub_rebar,
                cooling_link_required_length=cooling_link_required_length,
                sector_wing_north_sub_formwork=sector_wing_north_sub_formwork,
                power_supply_building_required_width=power_supply_building_required_width,
                sector_wing_west_super_concrete=sector_wing_west_super_concrete,
                electrical_building_sub_formwork=electrical_building_sub_formwork,
                turbine_hall_required_height=turbine_hall_required_height,
                cryo_coldbox_clear_width=cryo_coldbox_clear_width,
                sector_wing_east_sub_formwork=sector_wing_east_sub_formwork,
                reactor_auxiliaries_air_volume=reactor_auxiliaries_air_volume,
                sector_link_east_sub_rebar=sector_link_east_sub_rebar,
                cooling_link_sub_concrete=cooling_link_sub_concrete,
                security_required_height=security_required_height,
                sector_wing_east_clear_area=sector_wing_east_clear_area,
                site_services_building_clear_area=site_services_building_clear_area,
                sector_link_north_required_height=sector_link_north_required_height,
                cooling_annex_super_rebar=cooling_annex_super_rebar,
                power_supply_building_sub_formwork=power_supply_building_sub_formwork,
                cooling_link_air_volume=cooling_link_air_volume,
                cryo_compressors_clear_height=cryo_compressors_clear_height,
                maintenance_shop_super_concrete=maintenance_shop_super_concrete,
                cooling_hall_sub_rebar=cooling_hall_sub_rebar,
                sector_wing_east_sub_concrete=sector_wing_east_sub_concrete,
                cooling_helium_queue_peak=cooling_helium_queue_peak,
                fuel_building_clear_height=fuel_building_clear_height,
                service_water_building_clear_width=service_water_building_clear_width,
                sector_link_south_required_length=sector_link_south_required_length,
                administration_clear_area=administration_clear_area,
                cryo_coldbox_required_width=cryo_coldbox_required_width,
                cooling_link_clear_area=cooling_link_clear_area,
                site_services_building_sub_formwork=site_services_building_sub_formwork,
                turbine_hall_super_rebar=turbine_hall_super_rebar,
                cooling_salt_queue_peak=cooling_salt_queue_peak,
                sector_link_south_air_volume=sector_link_south_air_volume,
                cooling_dirty_bundle_required=cooling_dirty_bundle_required,
                sector_wing_east_clear_width=sector_wing_east_clear_width,
                sector_link_east_super_formwork=sector_link_east_super_formwork,
                security_air_volume=security_air_volume,
                reactor_auxiliaries_super_rebar=reactor_auxiliaries_super_rebar,
                service_water_building_super_formwork=service_water_building_super_formwork,
                reactor_hall_clear_length=reactor_hall_clear_length,
                reactor_hall_sub_formwork=reactor_hall_sub_formwork,
                sector_link_east_required_length=sector_link_east_required_length,
                cooling_hall_clear_area=cooling_hall_clear_area,
                sector_wing_west_sub_rebar=sector_wing_west_sub_rebar,
                administration_air_volume=administration_air_volume,
                turbine_hall_clear_length=turbine_hall_clear_length,
                sector_link_south_clear_length=sector_link_south_clear_length,
                sector_wing_east_clear_height=sector_wing_east_clear_height,
                turbine_hall_clear_area=turbine_hall_clear_area,
                sector_link_east_required_height=sector_link_east_required_height,
                sector_wing_west_sub_formwork=sector_wing_west_sub_formwork,
                service_water_building_required_height=service_water_building_required_height,
                sector_link_south_super_rebar=sector_link_south_super_rebar,
                control_gross_area=control_gross_area,
                fuel_building_gross_area=fuel_building_gross_area,
                sector_length=sector_length,
                cooling_annex_sub_rebar=cooling_annex_sub_rebar,
                cooling_annex_clear_area=cooling_annex_clear_area,
                calendar_event_count=calendar_event_count,
                sector_link_west_sub_formwork=sector_link_west_sub_formwork,
                sector_wing_west_clear_width=sector_wing_west_clear_width,
                security_sub_concrete=security_sub_concrete,
                fuel_building_super_concrete=fuel_building_super_concrete,
                cooling_clean_salt_allocated=cooling_clean_salt_allocated,
                cryo_compressors_gross_area=cryo_compressors_gross_area,
                sector_link_east_clear_length=sector_link_east_clear_length,
                cooling_annex_air_volume=cooling_annex_air_volume,
                cryo_coldbox_clear_area=cryo_coldbox_clear_area,
                sector_wing_south_gross_area=sector_wing_south_gross_area,
                cooling_outage_basis_resolved=cooling_outage_basis_resolved,
                turbine_hall_required_width=turbine_hall_required_width,
                sector_wing_north_clear_length=sector_wing_north_clear_length,
                cryo_compressors_required_height=cryo_compressors_required_height,
                turbine_hall_sub_concrete=turbine_hall_sub_concrete,
                contamination_procedure_qualified=contamination_procedure_qualified,
                cooling_hall_super_concrete=cooling_hall_super_concrete,
                turbine_hall_super_concrete=turbine_hall_super_concrete,
                control_super_rebar=control_super_rebar,
                sector_link_north_sub_rebar=sector_link_north_sub_rebar,
                maintenance_shop_sub_concrete=maintenance_shop_sub_concrete,
                sector_link_south_clear_width=sector_link_south_clear_width,
                parcel_area=parcel_area,
                sector_wing_south_super_concrete=sector_wing_south_super_concrete,
                cryo_coldbox_required_length=cryo_coldbox_required_length,
                administration_clear_length=administration_clear_length,
                sector_link_east_air_volume=sector_link_east_air_volume,
                security_clear_height=security_clear_height,
                sector_wing_south_clear_height=sector_wing_south_clear_height,
                reactor_auxiliaries_clear_height=reactor_auxiliaries_clear_height,
                packages_per_sector=packages_per_sector,
                security_sub_rebar=security_sub_rebar,
                maintenance_shop_required_length=maintenance_shop_required_length,
                administration_required_height=administration_required_height,
                sector_link_east_sub_concrete=sector_link_east_sub_concrete,
                sector_wing_east_gross_area=sector_wing_east_gross_area,
                sector_link_east_super_rebar=sector_link_east_super_rebar,
                fuel_building_clear_length=fuel_building_clear_length,
                security_super_rebar=security_super_rebar,
                cryo_compressors_sub_concrete=cryo_compressors_sub_concrete,
                service_water_building_super_concrete=service_water_building_super_concrete,
                reactor_hall_sub_concrete=reactor_hall_sub_concrete,
                service_water_building_sub_formwork=service_water_building_sub_formwork,
                sector_link_east_sub_formwork=sector_link_east_sub_formwork,
                security_sub_formwork=security_sub_formwork,
                security_super_concrete=security_super_concrete,
                sector_wing_west_clear_area=sector_wing_west_clear_area,
                cryo_compressors_super_rebar=cryo_compressors_super_rebar,
                control_clear_area=control_clear_area,
                cooling_annex_super_concrete=cooling_annex_super_concrete,
                control_super_formwork=control_super_formwork,
                turbine_hall_sub_formwork=turbine_hall_sub_formwork,
                electrical_building_air_volume=electrical_building_air_volume,
                cooling_hall_air_volume=cooling_hall_air_volume,
                sector_link_west_sub_rebar=sector_link_west_sub_rebar,
                cooling_hall_required_height=cooling_hall_required_height,
                sector_wing_east_air_volume=sector_wing_east_air_volume,
                sector_wing_south_clear_area=sector_wing_south_clear_area,
                sector_link_east_gross_area=sector_link_east_gross_area,
                cooling_link_required_width=cooling_link_required_width,
                outage_allowed_days=outage_allowed_days,
                cooling_annex_clear_length=cooling_annex_clear_length,
                sector_wing_north_sub_rebar=sector_wing_north_sub_rebar,
                sector_link_west_super_formwork=sector_link_west_super_formwork,
                initial_margin_days=initial_margin_days,
                sector_wing_east_required_height=sector_wing_east_required_height,
                sector_wing_east_required_length=sector_wing_east_required_length,
                service_water_building_sub_rebar=service_water_building_sub_rebar,
                site_services_building_clear_height=site_services_building_clear_height,
                administration_clear_width=administration_clear_width,
                maintenance_shop_clear_width=maintenance_shop_clear_width,
                cooling_last_release_year=cooling_last_release_year,
                sector_wing_north_required_height=sector_wing_north_required_height,
                power_supply_building_clear_height=power_supply_building_clear_height,
                reactor_hall_required_length=reactor_hall_required_length,
                cooling_dirty_salt_allocated=cooling_dirty_salt_allocated,
                reactor_hall_sub_rebar=reactor_hall_sub_rebar,
                sector_link_east_clear_height=sector_link_east_clear_height,
                cooling_hall_required_width=cooling_hall_required_width,
                site_services_building_super_rebar=site_services_building_super_rebar,
                sector_link_north_required_width=sector_link_north_required_width,
                cryo_compressors_clear_width=cryo_compressors_clear_width,
                turbine_hall_gross_area=turbine_hall_gross_area,
                reactor_hall_required_width=reactor_hall_required_width,
                sector_link_north_required_length=sector_link_north_required_length,
                sector_link_west_clear_length=sector_link_west_clear_length,
                control_sub_concrete=control_sub_concrete,
                power_supply_building_super_concrete=power_supply_building_super_concrete,
                electrical_building_required_height=electrical_building_required_height,
                reactor_auxiliaries_super_concrete=reactor_auxiliaries_super_concrete,
                site_services_building_gross_area=site_services_building_gross_area,
                reactor_auxiliaries_required_length=reactor_auxiliaries_required_length,
                fuel_building_super_rebar=fuel_building_super_rebar,
                fuel_building_required_height=fuel_building_required_height,
                cooling_initial_ready_margin_days=cooling_initial_ready_margin_days,
                sector_link_east_required_width=sector_link_east_required_width,
                electrical_building_sub_concrete=electrical_building_sub_concrete,
                security_gross_area=security_gross_area,
                sector_link_north_sub_concrete=sector_link_north_sub_concrete,
                sector_wing_south_sub_concrete=sector_wing_south_sub_concrete,
                cooling_annex_required_length=cooling_annex_required_length,
                turbine_hall_required_length=turbine_hall_required_length,
                geometry_fit_margin_m=geometry_fit_margin_m,
                readiness_margin_days=readiness_margin_days,
                sector_wing_north_air_volume=sector_wing_north_air_volume,
                power_supply_building_air_volume=power_supply_building_air_volume,
                total_gross_area=total_gross_area,
                sector_wing_north_sub_concrete=sector_wing_north_sub_concrete,
                cooling_annex_required_width=cooling_annex_required_width,
                cryo_compressors_required_width=cryo_compressors_required_width,
                required_parcel_x_max=required_parcel_x_max,
                sector_wing_north_clear_area=sector_wing_north_clear_area,
                cooling_bundle_queue_peak=cooling_bundle_queue_peak,
                cooling_annex_clear_height=cooling_annex_clear_height,
                power_supply_building_required_length=power_supply_building_required_length,
                cooling_link_clear_length=cooling_link_clear_length,
                initial_clean_required=initial_clean_required,
                power_supply_building_super_rebar=power_supply_building_super_rebar,
                capacity_margin_units=capacity_margin_units,
                cooling_link_sub_rebar=cooling_link_sub_rebar,
                reactor_hall_clear_area=reactor_hall_clear_area,
                parcel_fit_margin_m=parcel_fit_margin_m,
                sector_link_south_gross_area=sector_link_south_gross_area,
                sector_link_north_super_rebar=sector_link_north_super_rebar,
                sector_wing_south_super_rebar=sector_wing_south_super_rebar,
                blanket_packages_required_per_sector=blanket_packages_required_per_sector,
                cooling_dirty_helium_required=cooling_dirty_helium_required,
                maintenance_shop_required_height=maintenance_shop_required_height,
                total_air_volume=total_air_volume,
                cryo_compressors_clear_length=cryo_compressors_clear_length,
                service_water_building_required_width=service_water_building_required_width,
                site_services_building_air_volume=site_services_building_air_volume,
                sector_link_west_sub_concrete=sector_link_west_sub_concrete,
                administration_super_rebar=administration_super_rebar,
                security_super_formwork=security_super_formwork,
                cryo_coldbox_sub_rebar=cryo_coldbox_sub_rebar,
                sector_link_south_sub_concrete=sector_link_south_sub_concrete,
                cooling_clean_bundle_required=cooling_clean_bundle_required,
                cooling_clean_helium_allocated=cooling_clean_helium_allocated,
                route_margin_m=route_margin_m,
                sector_link_west_clear_width=sector_link_west_clear_width,
                electrical_building_clear_area=electrical_building_clear_area,
                sector_link_west_super_rebar=sector_link_west_super_rebar,
                clean_positions_allocated=clean_positions_allocated,
                cooling_link_sub_formwork=cooling_link_sub_formwork,
                cryo_coldbox_air_volume=cryo_coldbox_air_volume,
                cooling_hall_super_rebar=cooling_hall_super_rebar,
                sector_wing_west_super_formwork=sector_wing_west_super_formwork,
                reactor_auxiliaries_clear_area=reactor_auxiliaries_clear_area,
                reactor_auxiliaries_sub_concrete=reactor_auxiliaries_sub_concrete,
                fuel_building_required_length=fuel_building_required_length,
                reactor_auxiliaries_sub_rebar=reactor_auxiliaries_sub_rebar,
                sector_wing_west_sub_concrete=sector_wing_west_sub_concrete,
                cooling_dirty_bundle_allocated=cooling_dirty_bundle_allocated,
                cooling_hall_gross_area=cooling_hall_gross_area,
                sector_link_south_sub_formwork=sector_link_south_sub_formwork,
                sector_load_qualified=sector_load_qualified,
                cryo_coldbox_clear_height=cryo_coldbox_clear_height,
                sector_link_north_sub_formwork=sector_link_north_sub_formwork,
                sector_wing_south_air_volume=sector_wing_south_air_volume,
                outage_margin_days=outage_margin_days,
                sector_wing_north_super_concrete=sector_wing_north_super_concrete,
                cryo_coldbox_super_concrete=cryo_coldbox_super_concrete,
                maintenance_shop_gross_area=maintenance_shop_gross_area,
                site_services_building_required_height=site_services_building_required_height,
                sector_wing_west_super_rebar=sector_wing_west_super_rebar,
                sector_wing_north_clear_height=sector_wing_north_clear_height,
                sector_link_south_super_formwork=sector_link_south_super_formwork,
                sector_link_west_gross_area=sector_link_west_gross_area,
                cooling_hall_clear_length=cooling_hall_clear_length,
                sector_wing_west_required_width=sector_wing_west_required_width,
                administration_super_concrete=administration_super_concrete,
                sector_link_north_clear_length=sector_link_north_clear_length,
                reactor_hall_super_concrete=reactor_hall_super_concrete,
                administration_sub_formwork=administration_sub_formwork,
                turbine_hall_sub_rebar=turbine_hall_sub_rebar,
                site_services_building_clear_length=site_services_building_clear_length,
                power_supply_building_sub_concrete=power_supply_building_sub_concrete,
                reactor_hall_air_volume=reactor_hall_air_volume,
                reactor_auxiliaries_clear_length=reactor_auxiliaries_clear_length,
                administration_super_formwork=administration_super_formwork,
                site_services_building_super_formwork=site_services_building_super_formwork,
                administration_gross_area=administration_gross_area,
                material_capacity_volume=material_capacity_volume,
                cooling_annex_clear_width=cooling_annex_clear_width,
                cooling_link_required_height=cooling_link_required_height,
                cooling_link_gross_area=cooling_link_gross_area,
                cost_mode=cost_mode,
                cooling_clean_helium_required=cooling_clean_helium_required,
                control_required_area=control_required_area,
                cooling_link_clear_height=cooling_link_clear_height,
                maintenance_shop_super_formwork=maintenance_shop_super_formwork,
                sector_link_east_clear_width=sector_link_east_clear_width,
                sector_wing_north_clear_width=sector_wing_north_clear_width,
                maintenance_shop_sub_rebar=maintenance_shop_sub_rebar,
                total_clear_area=total_clear_area,
                cryo_compressors_air_volume=cryo_compressors_air_volume,
                sector_wing_west_required_height=sector_wing_west_required_height,
                reactor_hall_super_rebar=reactor_hall_super_rebar,
                cooling_dirty_helium_allocated=cooling_dirty_helium_allocated,
                sector_link_east_super_concrete=sector_link_east_super_concrete,
                sector_wing_north_required_length=sector_wing_north_required_length,
                turbine_hall_air_volume=turbine_hall_air_volume,
                provisional_room_count=provisional_room_count,
                sector_wing_south_clear_width=sector_wing_south_clear_width,
                sector_link_west_required_height=sector_link_west_required_height,
                sector_wing_south_clear_length=sector_wing_south_clear_length,
                cooling_hall_sub_formwork=cooling_hall_sub_formwork,
                cryo_coldbox_sub_concrete=cryo_coldbox_sub_concrete,
                power_supply_building_super_formwork=power_supply_building_super_formwork,
                fuel_building_sub_concrete=fuel_building_sub_concrete,
                sector_link_south_clear_area=sector_link_south_clear_area,
                security_clear_length=security_clear_length,
                cooling_link_super_concrete=cooling_link_super_concrete,
                reactor_auxiliaries_clear_width=reactor_auxiliaries_clear_width,
                site_services_building_required_length=site_services_building_required_length,
                cryo_compressors_super_concrete=cryo_compressors_super_concrete,
                required_parcel_y_min=required_parcel_y_min,
                sector_wing_east_required_width=sector_wing_east_required_width,
                cryo_coldbox_gross_area=cryo_coldbox_gross_area,
                cooling_hall_required_length=cooling_hall_required_length,
                electrical_building_required_width=electrical_building_required_width,
                fuel_building_clear_width=fuel_building_clear_width,
                administration_clear_height=administration_clear_height,
                security_required_area=security_required_area,
                service_water_building_gross_area=service_water_building_gross_area,
                electrical_building_gross_area=electrical_building_gross_area,
                initial_ready_margin_days=initial_ready_margin_days,
                power_supply_building_clear_length=power_supply_building_clear_length,
                cooling_annex_sub_concrete=cooling_annex_sub_concrete,
                sector_link_west_required_length=sector_link_west_required_length,
                fuel_building_sub_formwork=fuel_building_sub_formwork,
                power_supply_building_required_height=power_supply_building_required_height,
                cooling_clean_bundle_allocated=cooling_clean_bundle_allocated,
                unused_material_capacity=unused_material_capacity,
                cooling_hall_sub_concrete=cooling_hall_sub_concrete,
                maintenance_shop_super_rebar=maintenance_shop_super_rebar,
                sector_wing_west_gross_area=sector_wing_west_gross_area,
                service_water_building_air_volume=service_water_building_air_volume,
                sector_link_north_super_formwork=sector_link_north_super_formwork,
                sector_wing_south_sub_formwork=sector_wing_south_sub_formwork,
                reactor_hall_clear_width=reactor_hall_clear_width,
                sector_height=sector_height,
                sector_wing_east_super_formwork=sector_wing_east_super_formwork,
                cooling_link_super_rebar=cooling_link_super_rebar,
                control_sub_formwork=control_sub_formwork,
                maintenance_shop_air_volume=maintenance_shop_air_volume,
                cooling_dirty_salt_required=cooling_dirty_salt_required,
                control_clear_height=control_clear_height,
                control_super_concrete=control_super_concrete,
                cooling_link_super_formwork=cooling_link_super_formwork,
                sector_link_west_clear_height=sector_link_west_clear_height,
                electrical_building_super_rebar=electrical_building_super_rebar,
                cooling_clean_salt_required=cooling_clean_salt_required,
                electrical_building_clear_length=electrical_building_clear_length,
                reactor_auxiliaries_required_width=reactor_auxiliaries_required_width,
                electrical_building_sub_rebar=electrical_building_sub_rebar,
                security_clear_area=security_clear_area,
                reactor_hall_super_formwork=reactor_hall_super_formwork,
                sector_link_west_required_width=sector_link_west_required_width,
                sector_wing_north_super_formwork=sector_wing_north_super_formwork,
            )
        )
