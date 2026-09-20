"""Auto-generated implementation for Facility_Civil_Rollup.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_facilities.sysml:717

SysML Expressions:
    civil_capital = reactor_hall_in + sector_wing_east_in + sector_wing_north_in + sector_wing_west_in + sector_wing_south_in + sector_link_east_in + sector_link_north_in + sector_link_west_in + sector_link_south_in + cooling_hall_in + cooling_annex_in + cooling_link_in + turbine_hall_in + cryo_coldbox_in + cryo_compressors_in + fuel_building_in + reactor_auxiliaries_in + power_supply_building_in + electrical_building_in + service_water_building_in + maintenance_shop_in + site_services_building_in + administration_in + control_in + security_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Sum the actual25 civil component costs once.
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_facilities.facility_civil_rollup import Facility_Civil_RollupInput


def run_facility_civil_rollup(inputs: Facility_Civil_RollupInput) -> float:
    """Execute Facility_Civil_Rollup calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Sum the actual25 civil component costs once.

SysML Source: root-0/analyses/mfe_facilities.sysml:717

SysML Expressions:
    civil_capital = reactor_hall_in + sector_wing_east_in + sector_wing_north_in + sector_wing_west_in + sector_wing_south_in + sector_link_east_in + sector_link_north_in + sector_link_west_in + sector_link_south_in + cooling_hall_in + cooling_annex_in + cooling_link_in + turbine_hall_in + cryo_coldbox_in + cryo_compressors_in + fuel_building_in + reactor_auxiliaries_in + power_supply_building_in + electrical_building_in + service_water_building_in + maintenance_shop_in + site_services_building_in + administration_in + control_in + security_in
    
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Sum the actual25 civil component costs once.

Args:
    inputs: Input parameters validated against Facility_Civil_RollupInput schema

Returns:
    float: civil_capital

Example:
    >>> inputs = Facility_Civil_RollupInput(...)
    >>> result = run_facility_civil_rollup(inputs)
    """
    return ((((((((((((((((((((((((inputs.reactor_hall_in + inputs.sector_wing_east_in) + inputs.sector_wing_north_in) + inputs.sector_wing_west_in) + inputs.sector_wing_south_in) + inputs.sector_link_east_in) + inputs.sector_link_north_in) + inputs.sector_link_west_in) + inputs.sector_link_south_in) + inputs.cooling_hall_in) + inputs.cooling_annex_in) + inputs.cooling_link_in) + inputs.turbine_hall_in) + inputs.cryo_coldbox_in) + inputs.cryo_compressors_in) + inputs.fuel_building_in) + inputs.reactor_auxiliaries_in) + inputs.power_supply_building_in) + inputs.electrical_building_in) + inputs.service_water_building_in) + inputs.maintenance_shop_in) + inputs.site_services_building_in) + inputs.administration_in) + inputs.control_in) + inputs.security_in)
