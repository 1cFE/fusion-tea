from pydantic import Field
from simkit.config.schema import MultiOutput

class IFE_LCOEOutput(MultiOutput):
    """Multi-output container for IFE_LCOE.

Power balance and discounted cost/energy for an IFE power plant using
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
closed-form PVF replaces year-by-year iteration per DD-3.
Final guarded division is delegated to Generating Electricity Price.
*Reference**: Hawker Eqs. 2.1-2.16
*Last Updated**: 2026-09-10

SysML Source: root-0/analyses/ife_lcoe.sysml:4
    """
    thermal_power: float = Field(description="thermal_power output")
    fusion_energy_per_shot: float = Field(description="fusion_energy_per_shot output")
    discounted_energy: float = Field(description="discounted_energy output")
    net_electric_power_gw: float = Field(description="net_electric_power_gw output")
    fusion_power: float = Field(description="fusion_power output")
    shots_per_year: float = Field(description="shots_per_year output")
    driver_recirculating_fraction: float = Field(description="driver_recirculating_fraction output")
    other_parasitic_power: float = Field(description="other_parasitic_power output")
    net_electric_power: float = Field(description="net_electric_power output")
    discounted_cost: float = Field(description="discounted_cost output")
    driver_electric_power: float = Field(description="driver_electric_power output")
    annual_driver_replacement_cost: float = Field(description="annual_driver_replacement_cost output")
    driver_capital_cost: float = Field(description="driver_capital_cost output")
    thermal_power_gw: float = Field(description="thermal_power_gw output")
    gross_electric_power: float = Field(description="gross_electric_power output")
    total_recirculating_fraction: float = Field(description="total_recirculating_fraction output")
    energy_on_target: float = Field(description="energy_on_target output")
    driver_lifetime_years: float = Field(description="driver_lifetime_years output")
