"""Facility_Civil_RollupModule Module Wrapper

TEAx module for Facility_Civil_Rollup calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Sum the actual25 civil component costs once.

Inputs:
    - cooling_hall_in: cooling_hall_in parameter
    - turbine_hall_in: turbine_hall_in parameter
    - cooling_link_in: cooling_link_in parameter
    - reactor_hall_in: reactor_hall_in parameter
    - control_in: control_in parameter
    - reactor_auxiliaries_in: reactor_auxiliaries_in parameter
    - power_supply_building_in: power_supply_building_in parameter
    - sector_link_west_in: sector_link_west_in parameter
    - fuel_building_in: fuel_building_in parameter
    - cryo_coldbox_in: cryo_coldbox_in parameter
    - sector_wing_west_in: sector_wing_west_in parameter
    - sector_link_east_in: sector_link_east_in parameter
    - sector_wing_south_in: sector_wing_south_in parameter
    - sector_link_south_in: sector_link_south_in parameter
    - sector_link_north_in: sector_link_north_in parameter
    - service_water_building_in: service_water_building_in parameter
    - cooling_annex_in: cooling_annex_in parameter
    - sector_wing_east_in: sector_wing_east_in parameter
    - maintenance_shop_in: maintenance_shop_in parameter
    - site_services_building_in: site_services_building_in parameter
    - electrical_building_in: electrical_building_in parameter
    - administration_in: administration_in parameter
    - security_in: security_in parameter
    - sector_wing_north_in: sector_wing_north_in parameter
    - cryo_compressors_in: cryo_compressors_in parameter

Outputs:
    - civil_capital: civil_capital result

SysML Source: root-0/analyses/mfe_facilities.sysml:717

SysML Source: root-0/analyses/mfe_facilities.sysml:717

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_facilities/facility_civil_rollup_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float


class Facility_Civil_RollupInput(BaseModel):
    """Input model for Facility_Civil_RollupModule.

    Attributes:
        cooling_hall_in: cooling_hall_in input
        turbine_hall_in: turbine_hall_in input
        cooling_link_in: cooling_link_in input
        reactor_hall_in: reactor_hall_in input
        control_in: control_in input
        reactor_auxiliaries_in: reactor_auxiliaries_in input
        power_supply_building_in: power_supply_building_in input
        sector_link_west_in: sector_link_west_in input
        fuel_building_in: fuel_building_in input
        cryo_coldbox_in: cryo_coldbox_in input
        sector_wing_west_in: sector_wing_west_in input
        sector_link_east_in: sector_link_east_in input
        sector_wing_south_in: sector_wing_south_in input
        sector_link_south_in: sector_link_south_in input
        sector_link_north_in: sector_link_north_in input
        service_water_building_in: service_water_building_in input
        cooling_annex_in: cooling_annex_in input
        sector_wing_east_in: sector_wing_east_in input
        maintenance_shop_in: maintenance_shop_in input
        site_services_building_in: site_services_building_in input
        electrical_building_in: electrical_building_in input
        administration_in: administration_in input
        security_in: security_in input
        sector_wing_north_in: sector_wing_north_in input
        cryo_compressors_in: cryo_compressors_in input
    """
    cooling_hall_in: float = Field(..., description="cooling_hall_in input")
    turbine_hall_in: float = Field(..., description="turbine_hall_in input")
    cooling_link_in: float = Field(..., description="cooling_link_in input")
    reactor_hall_in: float = Field(..., description="reactor_hall_in input")
    control_in: float = Field(..., description="control_in input")
    reactor_auxiliaries_in: float = Field(..., description="reactor_auxiliaries_in input")
    power_supply_building_in: float = Field(..., description="power_supply_building_in input")
    sector_link_west_in: float = Field(..., description="sector_link_west_in input")
    fuel_building_in: float = Field(..., description="fuel_building_in input")
    cryo_coldbox_in: float = Field(..., description="cryo_coldbox_in input")
    sector_wing_west_in: float = Field(..., description="sector_wing_west_in input")
    sector_link_east_in: float = Field(..., description="sector_link_east_in input")
    sector_wing_south_in: float = Field(..., description="sector_wing_south_in input")
    sector_link_south_in: float = Field(..., description="sector_link_south_in input")
    sector_link_north_in: float = Field(..., description="sector_link_north_in input")
    service_water_building_in: float = Field(..., description="service_water_building_in input")
    cooling_annex_in: float = Field(..., description="cooling_annex_in input")
    sector_wing_east_in: float = Field(..., description="sector_wing_east_in input")
    maintenance_shop_in: float = Field(..., description="maintenance_shop_in input")
    site_services_building_in: float = Field(..., description="site_services_building_in input")
    electrical_building_in: float = Field(..., description="electrical_building_in input")
    administration_in: float = Field(..., description="administration_in input")
    security_in: float = Field(..., description="security_in input")
    sector_wing_north_in: float = Field(..., description="sector_wing_north_in input")
    cryo_compressors_in: float = Field(..., description="cryo_compressors_in input")


class Facility_Civil_RollupModule(ModuleBase[Facility_Civil_RollupInput, Float]):
    """TEAx module for Facility_Civil_Rollup calculation.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Sum the actual25 civil component costs once.

Inputs:
    - cooling_hall_in: cooling_hall_in parameter
    - turbine_hall_in: turbine_hall_in parameter
    - cooling_link_in: cooling_link_in parameter
    - reactor_hall_in: reactor_hall_in parameter
    - control_in: control_in parameter
    - reactor_auxiliaries_in: reactor_auxiliaries_in parameter
    - power_supply_building_in: power_supply_building_in parameter
    - sector_link_west_in: sector_link_west_in parameter
    - fuel_building_in: fuel_building_in parameter
    - cryo_coldbox_in: cryo_coldbox_in parameter
    - sector_wing_west_in: sector_wing_west_in parameter
    - sector_link_east_in: sector_link_east_in parameter
    - sector_wing_south_in: sector_wing_south_in parameter
    - sector_link_south_in: sector_link_south_in parameter
    - sector_link_north_in: sector_link_north_in parameter
    - service_water_building_in: service_water_building_in parameter
    - cooling_annex_in: cooling_annex_in parameter
    - sector_wing_east_in: sector_wing_east_in parameter
    - maintenance_shop_in: maintenance_shop_in parameter
    - site_services_building_in: site_services_building_in parameter
    - electrical_building_in: electrical_building_in parameter
    - administration_in: administration_in parameter
    - security_in: security_in parameter
    - sector_wing_north_in: sector_wing_north_in parameter
    - cryo_compressors_in: cryo_compressors_in parameter

Outputs:
    - civil_capital: civil_capital result

SysML Source: root-0/analyses/mfe_facilities.sysml:717

    SysML Source: root-0/analyses/mfe_facilities.sysml:717

    Calculation Specification:
        civil_capital = reactor_hall_in + sector_wing_east_in + sector_wing_north_in + sector_wing_west_in + sector_wing_south_in + sector_link_east_in + sector_link_north_in + sector_link_west_in + sector_link_south_in + cooling_hall_in + cooling_annex_in + cooling_link_in + turbine_hall_in + cryo_coldbox_in + cryo_compressors_in + fuel_building_in + reactor_auxiliaries_in + power_supply_building_in + electrical_building_in + service_water_building_in + maintenance_shop_in + site_services_building_in + administration_in + control_in + security_in
        
Documentation:
*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Sum the actual25 civil component costs once.

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_facilities.facility_civil_rollup_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Facility_Civil_RollupModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, cooling_hall_in: float, turbine_hall_in: float, cooling_link_in: float, reactor_hall_in: float, control_in: float, reactor_auxiliaries_in: float, power_supply_building_in: float, sector_link_west_in: float, fuel_building_in: float, cryo_coldbox_in: float, sector_wing_west_in: float, sector_link_east_in: float, sector_wing_south_in: float, sector_link_south_in: float, sector_link_north_in: float, service_water_building_in: float, cooling_annex_in: float, sector_wing_east_in: float, maintenance_shop_in: float, site_services_building_in: float, electrical_building_in: float, administration_in: float, security_in: float, sector_wing_north_in: float, cryo_compressors_in: float    ) -> Facility_Civil_RollupInput:
        """Validate inputs and fill defaults.

        Args:
            cooling_hall_in: cooling_hall_in input
            turbine_hall_in: turbine_hall_in input
            cooling_link_in: cooling_link_in input
            reactor_hall_in: reactor_hall_in input
            control_in: control_in input
            reactor_auxiliaries_in: reactor_auxiliaries_in input
            power_supply_building_in: power_supply_building_in input
            sector_link_west_in: sector_link_west_in input
            fuel_building_in: fuel_building_in input
            cryo_coldbox_in: cryo_coldbox_in input
            sector_wing_west_in: sector_wing_west_in input
            sector_link_east_in: sector_link_east_in input
            sector_wing_south_in: sector_wing_south_in input
            sector_link_south_in: sector_link_south_in input
            sector_link_north_in: sector_link_north_in input
            service_water_building_in: service_water_building_in input
            cooling_annex_in: cooling_annex_in input
            sector_wing_east_in: sector_wing_east_in input
            maintenance_shop_in: maintenance_shop_in input
            site_services_building_in: site_services_building_in input
            electrical_building_in: electrical_building_in input
            administration_in: administration_in input
            security_in: security_in input
            sector_wing_north_in: sector_wing_north_in input
            cryo_compressors_in: cryo_compressors_in input

        Returns:
            Validated input model
        """
        return Facility_Civil_RollupInput(cooling_hall_in=cooling_hall_in, turbine_hall_in=turbine_hall_in, cooling_link_in=cooling_link_in, reactor_hall_in=reactor_hall_in, control_in=control_in, reactor_auxiliaries_in=reactor_auxiliaries_in, power_supply_building_in=power_supply_building_in, sector_link_west_in=sector_link_west_in, fuel_building_in=fuel_building_in, cryo_coldbox_in=cryo_coldbox_in, sector_wing_west_in=sector_wing_west_in, sector_link_east_in=sector_link_east_in, sector_wing_south_in=sector_wing_south_in, sector_link_south_in=sector_link_south_in, sector_link_north_in=sector_link_north_in, service_water_building_in=service_water_building_in, cooling_annex_in=cooling_annex_in, sector_wing_east_in=sector_wing_east_in, maintenance_shop_in=maintenance_shop_in, site_services_building_in=site_services_building_in, electrical_building_in=electrical_building_in, administration_in=administration_in, security_in=security_in, sector_wing_north_in=sector_wing_north_in, cryo_compressors_in=cryo_compressors_in)

    def run(
        self, cooling_hall_in: float, turbine_hall_in: float, cooling_link_in: float, reactor_hall_in: float, control_in: float, reactor_auxiliaries_in: float, power_supply_building_in: float, sector_link_west_in: float, fuel_building_in: float, cryo_coldbox_in: float, sector_wing_west_in: float, sector_link_east_in: float, sector_wing_south_in: float, sector_link_south_in: float, sector_link_north_in: float, service_water_building_in: float, cooling_annex_in: float, sector_wing_east_in: float, maintenance_shop_in: float, site_services_building_in: float, electrical_building_in: float, administration_in: float, security_in: float, sector_wing_north_in: float, cryo_compressors_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            cooling_hall_in: cooling_hall_in input
            turbine_hall_in: turbine_hall_in input
            cooling_link_in: cooling_link_in input
            reactor_hall_in: reactor_hall_in input
            control_in: control_in input
            reactor_auxiliaries_in: reactor_auxiliaries_in input
            power_supply_building_in: power_supply_building_in input
            sector_link_west_in: sector_link_west_in input
            fuel_building_in: fuel_building_in input
            cryo_coldbox_in: cryo_coldbox_in input
            sector_wing_west_in: sector_wing_west_in input
            sector_link_east_in: sector_link_east_in input
            sector_wing_south_in: sector_wing_south_in input
            sector_link_south_in: sector_link_south_in input
            sector_link_north_in: sector_link_north_in input
            service_water_building_in: service_water_building_in input
            cooling_annex_in: cooling_annex_in input
            sector_wing_east_in: sector_wing_east_in input
            maintenance_shop_in: maintenance_shop_in input
            site_services_building_in: site_services_building_in input
            electrical_building_in: electrical_building_in input
            administration_in: administration_in input
            security_in: security_in input
            sector_wing_north_in: sector_wing_north_in input
            cryo_compressors_in: cryo_compressors_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(cooling_hall_in, turbine_hall_in, cooling_link_in, reactor_hall_in, control_in, reactor_auxiliaries_in, power_supply_building_in, sector_link_west_in, fuel_building_in, cryo_coldbox_in, sector_wing_west_in, sector_link_east_in, sector_wing_south_in, sector_link_south_in, sector_link_north_in, service_water_building_in, cooling_annex_in, sector_wing_east_in, maintenance_shop_in, site_services_building_in, electrical_building_in, administration_in, security_in, sector_wing_north_in, cryo_compressors_in)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_facilities.facility_civil_rollup_impl import (
            run_facility_civil_rollup,
        )

        # Execute implementation - returns single value
        civil_capital = run_facility_civil_rollup(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(civil_capital))
