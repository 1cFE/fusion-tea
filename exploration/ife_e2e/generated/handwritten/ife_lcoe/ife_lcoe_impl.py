"""Auto-generated implementation for IFE_LCOE.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/ife_lcoe.sysml:4

SysML Expressions:
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
    discount_factor_con = (1.0 + discount_rate_in) ** construction_years
    pvf_construction = (1.0 - 1.0 / discount_factor_con) / discount_rate_in
    discount_factor_op = (1.0 + discount_rate_in) ** operational_years
    pvf_operation = 1.0 / discount_factor_con * (1.0 - 1.0 / discount_factor_op) / discount_rate_in
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
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.ife_lcoe.ife_lcoe import IFE_LCOEInput


def run_ife_lcoe(inputs: IFE_LCOEInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    """Execute IFE_LCOE calculation.

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

SysML Expressions:
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
    discount_factor_con = (1.0 + discount_rate_in) ** construction_years
    pvf_construction = (1.0 - 1.0 / discount_factor_con) / discount_rate_in
    discount_factor_op = (1.0 + discount_rate_in) ** operational_years
    pvf_operation = 1.0 / discount_factor_con * (1.0 - 1.0 / discount_factor_op) / discount_rate_in
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

Args:
    inputs: Input parameters validated against IFE_LCOEInput schema

Returns:
    tuple[float, ...]: (thermal_power, fusion_energy_per_shot, discounted_energy, net_electric_power_gw, fusion_power, shots_per_year, driver_recirculating_fraction, other_parasitic_power, net_electric_power, discounted_cost, driver_electric_power, annual_driver_replacement_cost, driver_capital_cost, thermal_power_gw, gross_electric_power, total_recirculating_fraction, energy_on_target, driver_lifetime_years)

Example:
    >>> inputs = IFE_LCOEInput(...)
    >>> thermal_power, fusion_energy_per_shot, discounted_energy, net_electric_power_gw, fusion_power, shots_per_year, driver_recirculating_fraction, other_parasitic_power, net_electric_power, discounted_cost, driver_electric_power, annual_driver_replacement_cost, driver_capital_cost, thermal_power_gw, gross_electric_power, total_recirculating_fraction, energy_on_target, driver_lifetime_years = run_ife_lcoe(inputs)
    """
    discount_factor_op = ((1.0 + inputs.discount_rate_in) ** inputs.operational_years)
    shots_per_year = ((31557600.0 * inputs.frequency_in) * inputs.availability_in)
    discount_factor_con = ((1.0 + inputs.discount_rate_in) ** inputs.construction_years)
    pvf_construction = ((1.0 - (1.0 / discount_factor_con)) / inputs.discount_rate_in)
    pvf_operation = (((1.0 / discount_factor_con) * (1.0 - (1.0 / discount_factor_op))) / inputs.discount_rate_in)
    driver_electric_power = (inputs.driver_energy * inputs.frequency_in)
    other_parasitic_power = driver_electric_power
    driver_capital_cost = (inputs.driver_cost_constant * inputs.driver_energy)
    energy_on_target = (inputs.driver_efficiency * inputs.driver_energy)
    fusion_energy_per_shot = (inputs.gain_in * energy_on_target)
    fusion_power = (fusion_energy_per_shot * inputs.frequency_in)
    thermal_power = (inputs.blanket_energy_multiple * fusion_power)
    gross_electric_power = (inputs.thermal_efficiency_in * thermal_power)
    net_electric_power = ((gross_electric_power - driver_electric_power) - other_parasitic_power)
    net_electric_kw = (net_electric_power / 1000.0)
    annual_capital_cost = ((((inputs.plant_cost_constant_in * net_electric_kw) + ((inputs.yield_cost_constant * fusion_energy_per_shot) / 1000000000.0)) + driver_capital_cost) / inputs.construction_years)
    annual_energy = (((8760.0 * net_electric_kw) * inputs.availability_in) / 1000.0)
    driver_lifetime_years = (inputs.driver_lifetime_shots / shots_per_year)
    annual_driver_replacement_cost = (driver_capital_cost / driver_lifetime_years)
    annual_operating_cost = (((inputs.target_cost_constant * shots_per_year) + (inputs.om_cost_constant_in * net_electric_kw)) + annual_driver_replacement_cost)
    return (
        thermal_power,
        fusion_energy_per_shot,
        (annual_energy * pvf_operation),  # discounted_energy
        (net_electric_power / 1000000000.0),  # net_electric_power_gw
        fusion_power,
        shots_per_year,
        (driver_electric_power / gross_electric_power),  # driver_recirculating_fraction
        other_parasitic_power,
        net_electric_power,
        ((annual_capital_cost * pvf_construction) + (annual_operating_cost * pvf_operation)),  # discounted_cost
        driver_electric_power,
        annual_driver_replacement_cost,
        driver_capital_cost,
        (thermal_power / 1000000000.0),  # thermal_power_gw
        gross_electric_power,
        ((driver_electric_power + other_parasitic_power) / gross_electric_power),  # total_recirculating_fraction
        energy_on_target,
        driver_lifetime_years,
    )
