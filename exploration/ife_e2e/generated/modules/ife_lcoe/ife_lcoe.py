"""IFE_LCOEModule Module Wrapper

TEAx module for IFE_LCOE calculation.

Levelized Cost of Electricity for an IFE power plant using
Hawker's 14-parameter discounted cash flow model.

The formula evaluates a full DCF over a construction period
(Yc years) and operational lifetime (N_op years). Capital costs
are spread evenly across construction; operating costs accrue
during operation. Both cost and energy streams are discounted
to present value.

Closed-form present value factors replace year-by-year iteration:
  PVF_con = (1 - (1+d)^(-Yc)) / d
  PVF_op  = (1+d)^(-Yc) * (1 - (1+d)^(-N_op)) / d

Net electric power per Hawker Eq. 2.12-2.16:
  P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
where the factor of 2 approximates recirculating power as
2x driver power (driver + cooling).

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Equations 2.1-2.16 (complete LCOE model)
*Basis**: Hawker 2020 DCF LCOE model with 14 technology-agnostic parameters;
closed-form PVF replaces year-by-year iteration per DD-3

Inputs:
    - availability: availability parameter
    - blanket_energy_multiple: blanket_energy_multiple parameter
    - discount_rate: discount_rate parameter
    - driver_cost_constant: driver_cost_constant parameter
    - driver_efficiency: driver_efficiency parameter
    - driver_energy: driver_energy parameter
    - driver_lifetime_shots: driver_lifetime_shots parameter
    - frequency: frequency parameter
    - gain: gain parameter
    - om_cost_constant: om_cost_constant parameter
    - plant_cost_constant: plant_cost_constant parameter
    - target_cost_constant: target_cost_constant parameter
    - thermal_efficiency: thermal_efficiency parameter
    - yield_cost_constant: yield_cost_constant parameter
    - construction_years: construction_years parameter
    - operational_years: operational_years parameter

Outputs:
    - lcoe: lcoe result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/ife_lcoe.sysml:4

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/ife_lcoe.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/ife_lcoe/ife_lcoe_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.primitives import Float


class IFE_LCOEInput(BaseModel):
    """Input model for IFE_LCOEModule.

    Attributes:
        availability: availability input
        blanket_energy_multiple: blanket_energy_multiple input
        discount_rate: discount_rate input
        driver_cost_constant: driver_cost_constant input
        driver_efficiency: driver_efficiency input
        driver_energy: driver_energy input
        driver_lifetime_shots: driver_lifetime_shots input
        frequency: frequency input
        gain: gain input
        om_cost_constant: om_cost_constant input
        plant_cost_constant: plant_cost_constant input
        target_cost_constant: target_cost_constant input
        thermal_efficiency: thermal_efficiency input
        yield_cost_constant: yield_cost_constant input
        construction_years: construction_years input
        operational_years: operational_years input
    """
    availability: float = Field(..., description="availability input")
    blanket_energy_multiple: float = Field(..., description="blanket_energy_multiple input")
    discount_rate: float = Field(..., description="discount_rate input")
    driver_cost_constant: float = Field(..., description="driver_cost_constant input")
    driver_efficiency: float = Field(..., description="driver_efficiency input")
    driver_energy: float = Field(..., description="driver_energy input")
    driver_lifetime_shots: float = Field(..., description="driver_lifetime_shots input")
    frequency: float = Field(..., description="frequency input")
    gain: float = Field(..., description="gain input")
    om_cost_constant: float = Field(..., description="om_cost_constant input")
    plant_cost_constant: float = Field(..., description="plant_cost_constant input")
    target_cost_constant: float = Field(..., description="target_cost_constant input")
    thermal_efficiency: float = Field(..., description="thermal_efficiency input")
    yield_cost_constant: float = Field(..., description="yield_cost_constant input")
    construction_years: float = Field(..., description="construction_years input")
    operational_years: float = Field(..., description="operational_years input")


class IFE_LCOEModule(ModuleBase[IFE_LCOEInput, Float]):
    """TEAx module for IFE_LCOE calculation.

Levelized Cost of Electricity for an IFE power plant using
Hawker's 14-parameter discounted cash flow model.

The formula evaluates a full DCF over a construction period
(Yc years) and operational lifetime (N_op years). Capital costs
are spread evenly across construction; operating costs accrue
during operation. Both cost and energy streams are discounted
to present value.

Closed-form present value factors replace year-by-year iteration:
  PVF_con = (1 - (1+d)^(-Yc)) / d
  PVF_op  = (1+d)^(-Yc) * (1 - (1+d)^(-N_op)) / d

Net electric power per Hawker Eq. 2.12-2.16:
  P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
where the factor of 2 approximates recirculating power as
2x driver power (driver + cooling).

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Equations 2.1-2.16 (complete LCOE model)
*Basis**: Hawker 2020 DCF LCOE model with 14 technology-agnostic parameters;
closed-form PVF replaces year-by-year iteration per DD-3

Inputs:
    - availability: availability parameter
    - blanket_energy_multiple: blanket_energy_multiple parameter
    - discount_rate: discount_rate parameter
    - driver_cost_constant: driver_cost_constant parameter
    - driver_efficiency: driver_efficiency parameter
    - driver_energy: driver_energy parameter
    - driver_lifetime_shots: driver_lifetime_shots parameter
    - frequency: frequency parameter
    - gain: gain parameter
    - om_cost_constant: om_cost_constant parameter
    - plant_cost_constant: plant_cost_constant parameter
    - target_cost_constant: target_cost_constant parameter
    - thermal_efficiency: thermal_efficiency parameter
    - yield_cost_constant: yield_cost_constant parameter
    - construction_years: construction_years parameter
    - operational_years: operational_years parameter

Outputs:
    - lcoe: lcoe result

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/ife_lcoe.sysml:4

    SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/ife_lcoe.sysml:4

    Calculation Specification:
        construction_years = 5.0
        operational_years = 40.0
        energy_on_target = driver_efficiency * driver_energy
        fusion_energy_per_shot = gain * energy_on_target
        net_electric_power = driver_energy * frequency * (thermal_efficiency * blanket_energy_multiple * gain * driver_efficiency - 2.0)
        net_electric_kw = net_electric_power / 1000.0
        shots_per_year = 31557600.0 * frequency * availability
        driver_lifetime_years = driver_lifetime_shots / shots_per_year
        annual_capital_cost = (plant_cost_constant * net_electric_kw + yield_cost_constant * fusion_energy_per_shot / 1000000000.0 + driver_cost_constant * driver_energy) / construction_years
        annual_operating_cost = target_cost_constant * shots_per_year + om_cost_constant * net_electric_kw + driver_cost_constant * driver_energy / driver_lifetime_years
        annual_energy = 8760.0 * net_electric_kw * availability / 1000.0
        discount_factor_con = (1.0 + discount_rate) ** construction_years
        pvf_construction = (1.0 - 1.0 / discount_factor_con) / discount_rate
        discount_factor_op = (1.0 + discount_rate) ** operational_years
        pvf_operation = 1.0 / discount_factor_con * (1.0 - 1.0 / discount_factor_op) / discount_rate
        lcoe = (annual_capital_cost * pvf_construction + annual_operating_cost * pvf_operation) / (annual_energy * pvf_operation)
        
Documentation:
Levelized Cost of Electricity for an IFE power plant using
Hawker's 14-parameter discounted cash flow model.

The formula evaluates a full DCF over a construction period
(Yc years) and operational lifetime (N_op years). Capital costs
are spread evenly across construction; operating costs accrue
during operation. Both cost and energy streams are discounted
to present value.

Closed-form present value factors replace year-by-year iteration:
  PVF_con = (1 - (1+d)^(-Yc)) / d
  PVF_op  = (1+d)^(-Yc) * (1 - (1+d)^(-N_op)) / d

Net electric power per Hawker Eq. 2.12-2.16:
  P_e = E_d * f * (mu_th * E_b * G * mu_d - 2)
where the factor of 2 approximates recirculating power as
2x driver power (driver + cooling).

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md
*Ref**: Equations 2.1-2.16 (complete LCOE model)
*Basis**: Hawker 2020 DCF LCOE model with 14 technology-agnostic parameters;
closed-form PVF replaces year-by-year iteration per DD-3

    IMPLEMENTATION: See ife_tea.handwritten.ife_lcoe.ife_lcoe_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "IFE_LCOEModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, availability: float, blanket_energy_multiple: float, discount_rate: float, driver_cost_constant: float, driver_efficiency: float, driver_energy: float, driver_lifetime_shots: float, frequency: float, gain: float, om_cost_constant: float, plant_cost_constant: float, target_cost_constant: float, thermal_efficiency: float, yield_cost_constant: float, construction_years: float, operational_years: float    ) -> IFE_LCOEInput:
        """Validate inputs and fill defaults.

        Args:
            availability: availability input
            blanket_energy_multiple: blanket_energy_multiple input
            discount_rate: discount_rate input
            driver_cost_constant: driver_cost_constant input
            driver_efficiency: driver_efficiency input
            driver_energy: driver_energy input
            driver_lifetime_shots: driver_lifetime_shots input
            frequency: frequency input
            gain: gain input
            om_cost_constant: om_cost_constant input
            plant_cost_constant: plant_cost_constant input
            target_cost_constant: target_cost_constant input
            thermal_efficiency: thermal_efficiency input
            yield_cost_constant: yield_cost_constant input
            construction_years: construction_years input
            operational_years: operational_years input

        Returns:
            Validated input model
        """
        return IFE_LCOEInput(availability=availability, blanket_energy_multiple=blanket_energy_multiple, discount_rate=discount_rate, driver_cost_constant=driver_cost_constant, driver_efficiency=driver_efficiency, driver_energy=driver_energy, driver_lifetime_shots=driver_lifetime_shots, frequency=frequency, gain=gain, om_cost_constant=om_cost_constant, plant_cost_constant=plant_cost_constant, target_cost_constant=target_cost_constant, thermal_efficiency=thermal_efficiency, yield_cost_constant=yield_cost_constant, construction_years=construction_years, operational_years=operational_years)

    def run(
        self, availability: float, blanket_energy_multiple: float, discount_rate: float, driver_cost_constant: float, driver_efficiency: float, driver_energy: float, driver_lifetime_shots: float, frequency: float, gain: float, om_cost_constant: float, plant_cost_constant: float, target_cost_constant: float, thermal_efficiency: float, yield_cost_constant: float, construction_years: float, operational_years: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            availability: availability input
            blanket_energy_multiple: blanket_energy_multiple input
            discount_rate: discount_rate input
            driver_cost_constant: driver_cost_constant input
            driver_efficiency: driver_efficiency input
            driver_energy: driver_energy input
            driver_lifetime_shots: driver_lifetime_shots input
            frequency: frequency input
            gain: gain input
            om_cost_constant: om_cost_constant input
            plant_cost_constant: plant_cost_constant input
            target_cost_constant: target_cost_constant input
            thermal_efficiency: thermal_efficiency input
            yield_cost_constant: yield_cost_constant input
            construction_years: construction_years input
            operational_years: operational_years input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(availability, blanket_energy_multiple, discount_rate, driver_cost_constant, driver_efficiency, driver_energy, driver_lifetime_shots, frequency, gain, om_cost_constant, plant_cost_constant, target_cost_constant, thermal_efficiency, yield_cost_constant, construction_years, operational_years)

        # Import handwritten implementation
        from ife_tea.handwritten.ife_lcoe.ife_lcoe_impl import (
            run_ife_lcoe,
        )

        # Execute implementation - returns single value
        lcoe = run_ife_lcoe(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(lcoe))
