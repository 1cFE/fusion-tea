"""IFE_LCOEModule Module Wrapper

TEAx module for IFE_LCOE calculation.

Power balance and discounted cost/energy for an IFE power plant using
Hawker's 14-parameter discounted cash flow model.

The formula evaluates a full DCF over a construction period
(Yc years) and operational lifetime (N_op years). Capital costs
are spread evenly across construction; operating costs accrue
during operation. Both cost and energy streams are discounted
to present value.

IFE Present Value Factors supplies stable geometric factors, including
the exact-zero limit. This calculation multiplies each annual stream
by its supplied factor before the guarded price division.

Net electric power per Hawker Eq. 2.12-2.16:
  P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
where the factor of 2 approximates recirculating power as
2x driver power (driver + cooling).

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Equations 2.1-2.16 (complete LCOE model)
*Basis**: Hawker 2020 DCF LCOE model with 14 technology-agnostic parameters;
closed-form PVF replaces year-by-year iteration per DD-3.
Final guarded division is delegated to Generating Electricity Price.
*Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141-148 and following Eqs. 2.2-2.16
*Last Updated**: 2026-09-11

Inputs:
    - pvf_construction: pvf_construction parameter
    - thermal_efficiency_in: thermal_efficiency_in parameter
    - discount_rate_in: discount_rate_in parameter
    - driver_lifetime_shots: driver_lifetime_shots parameter
    - construction_years: construction_years parameter
    - availability_in: availability_in parameter
    - driver_cost_constant: driver_cost_constant parameter
    - om_cost_constant_in: om_cost_constant_in parameter
    - driver_efficiency: driver_efficiency parameter
    - plant_cost_constant_in: plant_cost_constant_in parameter
    - operational_years: operational_years parameter
    - yield_cost_constant: yield_cost_constant parameter
    - blanket_energy_multiple: blanket_energy_multiple parameter
    - target_cost_constant: target_cost_constant parameter
    - pvf_operation: pvf_operation parameter
    - gain_in: gain_in parameter
    - driver_energy: driver_energy parameter
    - frequency_in: frequency_in parameter

Outputs:
    - thermal_power: thermal_power result
    - fusion_energy_per_shot: fusion_energy_per_shot result
    - discounted_energy: discounted_energy result
    - net_electric_power_gw: net_electric_power_gw result
    - fusion_power: fusion_power result
    - shots_per_year: shots_per_year result
    - driver_recirculating_fraction: driver_recirculating_fraction result
    - other_parasitic_power: other_parasitic_power result
    - net_electric_power: net_electric_power result
    - discounted_cost: discounted_cost result
    - driver_electric_power: driver_electric_power result
    - annual_driver_replacement_cost: annual_driver_replacement_cost result
    - driver_capital_cost: driver_capital_cost result
    - thermal_power_gw: thermal_power_gw result
    - gross_electric_power: gross_electric_power result
    - total_recirculating_fraction: total_recirculating_fraction result
    - energy_on_target: energy_on_target result
    - driver_lifetime_years: driver_lifetime_years result

SysML Source: root-0/analyses/ife_lcoe.sysml:4

SysML Source: root-0/analyses/ife_lcoe.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ife_lcoe/ife_lcoe_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float
from ife_tea.schemas.ife_lcoe_output import IFE_LCOEOutput


class IFE_LCOEInput(BaseModel):
    """Input model for IFE_LCOEModule.

    Attributes:
        pvf_construction: pvf_construction input
        thermal_efficiency_in: thermal_efficiency_in input
        discount_rate_in: discount_rate_in input
        driver_lifetime_shots: driver_lifetime_shots input
        construction_years: construction_years input
        availability_in: availability_in input
        driver_cost_constant: driver_cost_constant input
        om_cost_constant_in: om_cost_constant_in input
        driver_efficiency: driver_efficiency input
        plant_cost_constant_in: plant_cost_constant_in input
        operational_years: operational_years input
        yield_cost_constant: yield_cost_constant input
        blanket_energy_multiple: blanket_energy_multiple input
        target_cost_constant: target_cost_constant input
        pvf_operation: pvf_operation input
        gain_in: gain_in input
        driver_energy: driver_energy input
        frequency_in: frequency_in input
    """
    pvf_construction: float = Field(..., description="pvf_construction input")
    thermal_efficiency_in: float = Field(..., description="thermal_efficiency_in input")
    discount_rate_in: float = Field(..., description="discount_rate_in input")
    driver_lifetime_shots: float = Field(..., description="driver_lifetime_shots input")
    construction_years: float = Field(..., description="construction_years input")
    availability_in: float = Field(..., description="availability_in input")
    driver_cost_constant: float = Field(..., description="driver_cost_constant input")
    om_cost_constant_in: float = Field(..., description="om_cost_constant_in input")
    driver_efficiency: float = Field(..., description="driver_efficiency input")
    plant_cost_constant_in: float = Field(..., description="plant_cost_constant_in input")
    operational_years: float = Field(..., description="operational_years input")
    yield_cost_constant: float = Field(..., description="yield_cost_constant input")
    blanket_energy_multiple: float = Field(..., description="blanket_energy_multiple input")
    target_cost_constant: float = Field(..., description="target_cost_constant input")
    pvf_operation: float = Field(..., description="pvf_operation input")
    gain_in: float = Field(..., description="gain_in input")
    driver_energy: float = Field(..., description="driver_energy input")
    frequency_in: float = Field(..., description="frequency_in input")


class IFE_LCOEModule(ModuleBase[IFE_LCOEInput, IFE_LCOEOutput]):
    """TEAx module for IFE_LCOE calculation.

Power balance and discounted cost/energy for an IFE power plant using
Hawker's 14-parameter discounted cash flow model.

The formula evaluates a full DCF over a construction period
(Yc years) and operational lifetime (N_op years). Capital costs
are spread evenly across construction; operating costs accrue
during operation. Both cost and energy streams are discounted
to present value.

IFE Present Value Factors supplies stable geometric factors, including
the exact-zero limit. This calculation multiplies each annual stream
by its supplied factor before the guarded price division.

Net electric power per Hawker Eq. 2.12-2.16:
  P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
where the factor of 2 approximates recirculating power as
2x driver power (driver + cooling).

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Equations 2.1-2.16 (complete LCOE model)
*Basis**: Hawker 2020 DCF LCOE model with 14 technology-agnostic parameters;
closed-form PVF replaces year-by-year iteration per DD-3.
Final guarded division is delegated to Generating Electricity Price.
*Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141-148 and following Eqs. 2.2-2.16
*Last Updated**: 2026-09-11

Inputs:
    - pvf_construction: pvf_construction parameter
    - thermal_efficiency_in: thermal_efficiency_in parameter
    - discount_rate_in: discount_rate_in parameter
    - driver_lifetime_shots: driver_lifetime_shots parameter
    - construction_years: construction_years parameter
    - availability_in: availability_in parameter
    - driver_cost_constant: driver_cost_constant parameter
    - om_cost_constant_in: om_cost_constant_in parameter
    - driver_efficiency: driver_efficiency parameter
    - plant_cost_constant_in: plant_cost_constant_in parameter
    - operational_years: operational_years parameter
    - yield_cost_constant: yield_cost_constant parameter
    - blanket_energy_multiple: blanket_energy_multiple parameter
    - target_cost_constant: target_cost_constant parameter
    - pvf_operation: pvf_operation parameter
    - gain_in: gain_in parameter
    - driver_energy: driver_energy parameter
    - frequency_in: frequency_in parameter

Outputs:
    - thermal_power: thermal_power result
    - fusion_energy_per_shot: fusion_energy_per_shot result
    - discounted_energy: discounted_energy result
    - net_electric_power_gw: net_electric_power_gw result
    - fusion_power: fusion_power result
    - shots_per_year: shots_per_year result
    - driver_recirculating_fraction: driver_recirculating_fraction result
    - other_parasitic_power: other_parasitic_power result
    - net_electric_power: net_electric_power result
    - discounted_cost: discounted_cost result
    - driver_electric_power: driver_electric_power result
    - annual_driver_replacement_cost: annual_driver_replacement_cost result
    - driver_capital_cost: driver_capital_cost result
    - thermal_power_gw: thermal_power_gw result
    - gross_electric_power: gross_electric_power result
    - total_recirculating_fraction: total_recirculating_fraction result
    - energy_on_target: energy_on_target result
    - driver_lifetime_years: driver_lifetime_years result

SysML Source: root-0/analyses/ife_lcoe.sysml:4

    SysML Source: root-0/analyses/ife_lcoe.sysml:4

    Calculation Specification:
        construction_years = 5.0
        operational_years = 40.0
        energy_on_target = driver_efficiency * driver_energy
        fusion_energy_per_shot = gain_in * energy_on_target
        fusion_power = fusion_energy_per_shot * frequency_in
        thermal_power = blanket_energy_multiple * fusion_power
        thermal_power_gw = thermal_power / 1000000000.0
        gross_electric_power = thermal_efficiency_in * thermal_power
        driver_electric_power = driver_energy * frequency_in
        other_parasitic_power = driver_electric_power
        net_electric_power = gross_electric_power - driver_electric_power - other_parasitic_power
        net_electric_power_gw = net_electric_power / 1000000000.0
        driver_recirculating_fraction = driver_electric_power / gross_electric_power
        total_recirculating_fraction = (driver_electric_power + other_parasitic_power) / gross_electric_power
        net_electric_kw = net_electric_power / 1000.0
        shots_per_year = 31557600.0 * frequency_in * availability_in
        driver_lifetime_years = driver_lifetime_shots / shots_per_year
        driver_capital_cost = driver_cost_constant * driver_energy
        annual_driver_replacement_cost = driver_capital_cost / driver_lifetime_years
        annual_capital_cost = (plant_cost_constant_in * net_electric_kw + yield_cost_constant * fusion_energy_per_shot / 1000000000.0 + driver_capital_cost) / construction_years
        annual_operating_cost = target_cost_constant * shots_per_year + om_cost_constant_in * net_electric_kw + annual_driver_replacement_cost
        annual_energy = 8760.0 * net_electric_kw * availability_in / 1000.0
        discounted_cost = annual_capital_cost * pvf_construction + annual_operating_cost * pvf_operation
        discounted_energy = annual_energy * pvf_operation
        
Documentation:
Power balance and discounted cost/energy for an IFE power plant using
Hawker's 14-parameter discounted cash flow model.

The formula evaluates a full DCF over a construction period
(Yc years) and operational lifetime (N_op years). Capital costs
are spread evenly across construction; operating costs accrue
during operation. Both cost and energy streams are discounted
to present value.

IFE Present Value Factors supplies stable geometric factors, including
the exact-zero limit. This calculation multiplies each annual stream
by its supplied factor before the guarded price division.

Net electric power per Hawker Eq. 2.12-2.16:
  P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
where the factor of 2 approximates recirculating power as
2x driver power (driver + cooling).

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Equations 2.1-2.16 (complete LCOE model)
*Basis**: Hawker 2020 DCF LCOE model with 14 technology-agnostic parameters;
closed-form PVF replaces year-by-year iteration per DD-3.
Final guarded division is delegated to Generating Electricity Price.
*Reference**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md:141-148 and following Eqs. 2.2-2.16
*Last Updated**: 2026-09-11

    IMPLEMENTATION: See ife_tea.handwritten.ife_lcoe.ife_lcoe_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts thermal_power, fusion_energy_per_shot, discounted_energy, net_electric_power_gw, fusion_power, shots_per_year, driver_recirculating_fraction, other_parasitic_power, net_electric_power, discounted_cost, driver_electric_power, annual_driver_replacement_cost, driver_capital_cost, thermal_power_gw, gross_electric_power, total_recirculating_fraction, energy_on_target, driver_lifetime_years fields to separate channels.
    """

    name: str = "IFE_LCOEModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pvf_construction: float, thermal_efficiency_in: float, discount_rate_in: float, driver_lifetime_shots: float, construction_years: float, availability_in: float, driver_cost_constant: float, om_cost_constant_in: float, driver_efficiency: float, plant_cost_constant_in: float, operational_years: float, yield_cost_constant: float, blanket_energy_multiple: float, target_cost_constant: float, pvf_operation: float, gain_in: float, driver_energy: float, frequency_in: float    ) -> IFE_LCOEInput:
        """Validate inputs and fill defaults.

        Args:
            pvf_construction: pvf_construction input
            thermal_efficiency_in: thermal_efficiency_in input
            discount_rate_in: discount_rate_in input
            driver_lifetime_shots: driver_lifetime_shots input
            construction_years: construction_years input
            availability_in: availability_in input
            driver_cost_constant: driver_cost_constant input
            om_cost_constant_in: om_cost_constant_in input
            driver_efficiency: driver_efficiency input
            plant_cost_constant_in: plant_cost_constant_in input
            operational_years: operational_years input
            yield_cost_constant: yield_cost_constant input
            blanket_energy_multiple: blanket_energy_multiple input
            target_cost_constant: target_cost_constant input
            pvf_operation: pvf_operation input
            gain_in: gain_in input
            driver_energy: driver_energy input
            frequency_in: frequency_in input

        Returns:
            Validated input model
        """
        return IFE_LCOEInput(pvf_construction=pvf_construction, thermal_efficiency_in=thermal_efficiency_in, discount_rate_in=discount_rate_in, driver_lifetime_shots=driver_lifetime_shots, construction_years=construction_years, availability_in=availability_in, driver_cost_constant=driver_cost_constant, om_cost_constant_in=om_cost_constant_in, driver_efficiency=driver_efficiency, plant_cost_constant_in=plant_cost_constant_in, operational_years=operational_years, yield_cost_constant=yield_cost_constant, blanket_energy_multiple=blanket_energy_multiple, target_cost_constant=target_cost_constant, pvf_operation=pvf_operation, gain_in=gain_in, driver_energy=driver_energy, frequency_in=frequency_in)

    def run(
        self, pvf_construction: float, thermal_efficiency_in: float, discount_rate_in: float, driver_lifetime_shots: float, construction_years: float, availability_in: float, driver_cost_constant: float, om_cost_constant_in: float, driver_efficiency: float, plant_cost_constant_in: float, operational_years: float, yield_cost_constant: float, blanket_energy_multiple: float, target_cost_constant: float, pvf_operation: float, gain_in: float, driver_energy: float, frequency_in: float    ) -> ModuleResult[IFE_LCOEOutput]:
        """Execute calculation.

        Args:
            pvf_construction: pvf_construction input
            thermal_efficiency_in: thermal_efficiency_in input
            discount_rate_in: discount_rate_in input
            driver_lifetime_shots: driver_lifetime_shots input
            construction_years: construction_years input
            availability_in: availability_in input
            driver_cost_constant: driver_cost_constant input
            om_cost_constant_in: om_cost_constant_in input
            driver_efficiency: driver_efficiency input
            plant_cost_constant_in: plant_cost_constant_in input
            operational_years: operational_years input
            yield_cost_constant: yield_cost_constant input
            blanket_energy_multiple: blanket_energy_multiple input
            target_cost_constant: target_cost_constant input
            pvf_operation: pvf_operation input
            gain_in: gain_in input
            driver_energy: driver_energy input
            frequency_in: frequency_in input

        Returns:
            Module result with IFE_LCOEOutput (thermal_power, fusion_energy_per_shot, discounted_energy, net_electric_power_gw, fusion_power, shots_per_year, driver_recirculating_fraction, other_parasitic_power, net_electric_power, discounted_cost, driver_electric_power, annual_driver_replacement_cost, driver_capital_cost, thermal_power_gw, gross_electric_power, total_recirculating_fraction, energy_on_target, driver_lifetime_years)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pvf_construction, thermal_efficiency_in, discount_rate_in, driver_lifetime_shots, construction_years, availability_in, driver_cost_constant, om_cost_constant_in, driver_efficiency, plant_cost_constant_in, operational_years, yield_cost_constant, blanket_energy_multiple, target_cost_constant, pvf_operation, gain_in, driver_energy, frequency_in)

        # Import handwritten implementation
        from ife_tea.handwritten.ife_lcoe.ife_lcoe_impl import (
            run_ife_lcoe,
        )

        # Execute implementation - returns tuple of values
        thermal_power, fusion_energy_per_shot, discounted_energy, net_electric_power_gw, fusion_power, shots_per_year, driver_recirculating_fraction, other_parasitic_power, net_electric_power, discounted_cost, driver_electric_power, annual_driver_replacement_cost, driver_capital_cost, thermal_power_gw, gross_electric_power, total_recirculating_fraction, energy_on_target, driver_lifetime_years = run_ife_lcoe(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=IFE_LCOEOutput(
                thermal_power=thermal_power,
                fusion_energy_per_shot=fusion_energy_per_shot,
                discounted_energy=discounted_energy,
                net_electric_power_gw=net_electric_power_gw,
                fusion_power=fusion_power,
                shots_per_year=shots_per_year,
                driver_recirculating_fraction=driver_recirculating_fraction,
                other_parasitic_power=other_parasitic_power,
                net_electric_power=net_electric_power,
                discounted_cost=discounted_cost,
                driver_electric_power=driver_electric_power,
                annual_driver_replacement_cost=annual_driver_replacement_cost,
                driver_capital_cost=driver_capital_cost,
                thermal_power_gw=thermal_power_gw,
                gross_electric_power=gross_electric_power,
                total_recirculating_fraction=total_recirculating_fraction,
                energy_on_target=energy_on_target,
                driver_lifetime_years=driver_lifetime_years,
            )
        )
