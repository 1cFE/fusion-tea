"""Auto-generated implementation for Meier_COE.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/hif_economics.sysml:88

SysML Expressions:
    annualized_cost = 0.113 * total_capital_billions
    energy_denominator = 0.0876 * availability_in * net_electric_power_gw_in
    
Documentation:
Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%). Exposes the numerator and
energy denominator for Generating Electricity Price.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = 8760 hr/yr * 1e6 kW/GW / (1e9 dollars/billion * 100 cents/dollar),
the scaled energy denominator when cost is in billions and price in cents/kWh.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Eq. 1 (lines 76-102)
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.
"""

AUTO_IMPLEMENTED = True

from ife_tea.modules.hif_economics.meier_coe import Meier_COEInput


def run_meier_coe(inputs: Meier_COEInput) -> tuple[float, float]:
    """Execute Meier_COE calculation.

Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%). Exposes the numerator and
energy denominator for Generating Electricity Price.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = 8760 hr/yr * 1e6 kW/GW / (1e9 dollars/billion * 100 cents/dollar),
the scaled energy denominator when cost is in billions and price in cents/kWh.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Eq. 1 (lines 76-102)
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

SysML Source: root-0/analyses/hif_economics.sysml:88

SysML Expressions:
    annualized_cost = 0.113 * total_capital_billions
    energy_denominator = 0.0876 * availability_in * net_electric_power_gw_in
    
Documentation:
Cost of Electricity from Meier's engineering-economic model.
Combines fixed charge rate (8.3%) and O&M rate (3%) into a
single capital charge rate (11.3%). Exposes the numerator and
energy denominator for Generating Electricity Price.

Constants: 0.113 = R + M (8.3% fixed charge + 3% O&M),
0.0876 = 8760 hr/yr * 1e6 kW/GW / (1e9 dollars/billion * 100 cents/dollar),
the scaled energy denominator when cost is in billions and price in cents/kWh.

*Source**: knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Eq. 1 (lines 76-102)
*Last Updated**: 2026-09-10
*Basis**: Meier 1986 COE formula. Year-dollars: 1988$.

Args:
    inputs: Input parameters validated against Meier_COEInput schema

Returns:
    tuple[float, ...]: (energy_denominator, annualized_cost)

Example:
    >>> inputs = Meier_COEInput(...)
    >>> energy_denominator, annualized_cost = run_meier_coe(inputs)
    """
    return (
        ((0.0876 * inputs.availability_in) * inputs.net_electric_power_gw_in),  # energy_denominator
        (0.113 * inputs.total_capital_billions),  # annualized_cost
    )
