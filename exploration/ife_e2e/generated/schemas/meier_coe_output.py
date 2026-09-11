from pydantic import Field
from simkit.config.schema import MultiOutput

class Meier_COEOutput(MultiOutput):
    """Multi-output container for Meier_COE.

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
    """
    energy_denominator: float = Field(description="energy_denominator output")
    annualized_cost: float = Field(description="annualized_cost output")
