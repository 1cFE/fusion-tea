"""Auto-generated implementation for IFE_LCOE.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/ife_lcoe.sysml:4

SysML Expressions:
    construction_years = LiteralRationalEvaluation()
    operational_years = LiteralRationalEvaluation()
    energy_on_target = driver_efficiency * driver_energy
    fusion_energy_per_shot = gain * energy_on_target
    net_electric_power = driver_energy * frequency * thermal_efficiency * blanket_energy_multiple * gain * driver_efficiency - LiteralRationalEvaluation()
    net_electric_kw = net_electric_power / LiteralRationalEvaluation()
    shots_per_year = LiteralRationalEvaluation() * frequency * availability
    driver_lifetime_years = driver_lifetime_shots / shots_per_year
    annual_capital_cost = plant_cost_constant * net_electric_kw + yield_cost_constant * fusion_energy_per_shot / LiteralRationalEvaluation() + driver_cost_constant * driver_energy / construction_years
    annual_operating_cost = target_cost_constant * shots_per_year + om_cost_constant * net_electric_kw + driver_cost_constant * driver_energy / driver_lifetime_years
    annual_energy = LiteralRationalEvaluation() * net_electric_kw * availability / LiteralRationalEvaluation()
    discount_factor_con = LiteralRationalEvaluation() + discount_rate ** construction_years
    pvf_construction = LiteralRationalEvaluation() - LiteralRationalEvaluation() / discount_factor_con / discount_rate
    discount_factor_op = LiteralRationalEvaluation() + discount_rate ** operational_years
    pvf_operation = LiteralRationalEvaluation() / discount_factor_con * LiteralRationalEvaluation() - LiteralRationalEvaluation() / discount_factor_op / discount_rate
    lcoe = annual_capital_cost * pvf_construction + annual_operating_cost * pvf_operation / annual_energy * pvf_operation
    
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
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.ife_lcoe.ife_lcoe import IFE_LCOEInput


def run_ife_lcoe(inputs: IFE_LCOEInput) -> float:
    """Execute IFE_LCOE calculation.

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

SysML Source: /home/reid/1cfe/fusion-tea/exploration/ife_e2e/models/analyses/ife_lcoe.sysml:4

SysML Expressions:
    construction_years = LiteralRationalEvaluation()
    operational_years = LiteralRationalEvaluation()
    energy_on_target = driver_efficiency * driver_energy
    fusion_energy_per_shot = gain * energy_on_target
    net_electric_power = driver_energy * frequency * thermal_efficiency * blanket_energy_multiple * gain * driver_efficiency - LiteralRationalEvaluation()
    net_electric_kw = net_electric_power / LiteralRationalEvaluation()
    shots_per_year = LiteralRationalEvaluation() * frequency * availability
    driver_lifetime_years = driver_lifetime_shots / shots_per_year
    annual_capital_cost = plant_cost_constant * net_electric_kw + yield_cost_constant * fusion_energy_per_shot / LiteralRationalEvaluation() + driver_cost_constant * driver_energy / construction_years
    annual_operating_cost = target_cost_constant * shots_per_year + om_cost_constant * net_electric_kw + driver_cost_constant * driver_energy / driver_lifetime_years
    annual_energy = LiteralRationalEvaluation() * net_electric_kw * availability / LiteralRationalEvaluation()
    discount_factor_con = LiteralRationalEvaluation() + discount_rate ** construction_years
    pvf_construction = LiteralRationalEvaluation() - LiteralRationalEvaluation() / discount_factor_con / discount_rate
    discount_factor_op = LiteralRationalEvaluation() + discount_rate ** operational_years
    pvf_operation = LiteralRationalEvaluation() / discount_factor_con * LiteralRationalEvaluation() - LiteralRationalEvaluation() / discount_factor_op / discount_rate
    lcoe = annual_capital_cost * pvf_construction + annual_operating_cost * pvf_operation / annual_energy * pvf_operation
    
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

Args:
    inputs: Input parameters validated against IFE_LCOEInput schema

Returns:
    float: lcoe

Example:
    >>> inputs = IFE_LCOEInput(...)
    >>> result = run_ife_lcoe(inputs)
    """
    discount_factor_con = ((1.0 + inputs.discount_rate) ** inputs.construction_years)
    discount_factor_op = ((1.0 + inputs.discount_rate) ** inputs.operational_years)
    energy_on_target = (inputs.driver_efficiency * inputs.driver_energy)
    fusion_energy_per_shot = (inputs.gain * energy_on_target)
    net_electric_power = ((inputs.driver_energy * inputs.frequency) * ((((inputs.thermal_efficiency * inputs.blanket_energy_multiple) * inputs.gain) * inputs.driver_efficiency) - 2.0))
    net_electric_kw = (net_electric_power / 1000.0)
    annual_capital_cost = ((((inputs.plant_cost_constant * net_electric_kw) + ((inputs.yield_cost_constant * fusion_energy_per_shot) / 1000000000.0)) + (inputs.driver_cost_constant * inputs.driver_energy)) / inputs.construction_years)
    annual_energy = (((8760.0 * net_electric_kw) * inputs.availability) / 1000.0)
    pvf_construction = ((1.0 - (1.0 / discount_factor_con)) / inputs.discount_rate)
    pvf_operation = (((1.0 / discount_factor_con) * (1.0 - (1.0 / discount_factor_op))) / inputs.discount_rate)
    shots_per_year = ((31557600.0 * inputs.frequency) * inputs.availability)
    driver_lifetime_years = (inputs.driver_lifetime_shots / shots_per_year)
    annual_operating_cost = (((inputs.target_cost_constant * shots_per_year) + (inputs.om_cost_constant * net_electric_kw)) + ((inputs.driver_cost_constant * inputs.driver_energy) / driver_lifetime_years))
    return (((annual_capital_cost * pvf_construction) + (annual_operating_cost * pvf_operation)) / (annual_energy * pvf_operation))
