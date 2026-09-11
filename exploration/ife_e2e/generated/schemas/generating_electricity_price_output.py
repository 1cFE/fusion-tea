from pydantic import Field
from simkit.config.schema import MultiOutput

class Generating_Electricity_PriceOutput(MultiOutput):
    """Multi-output container for Generating_Electricity_Price.

Guard only the final price division, using actual net power in W.
If net_power > 0, price = numerator / denominator and generating = 1.
Otherwise price = 0 and generating = 0. Zero price is an invalid sentinel.
Consumers must require generating = 1 and satisfied net_positive before ranking.
The numerator and denominator retain the bound channel's units: Hawker
discounted dollars/MWh or Meier annualized billion dollars/scaled energy
giving 1988 cents/kWh. generating is a dimensionless Real restricted to 0/1.
Implemented by the native handwritten completion because the pinned
arithmetic renderer does not support this conditional. No finance is duplicated.

*Source**: knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md,
knowledge/sources/economic_studies_for_heavy_ion_fusion_electric_power_plants/output.md
*Reference**: Hawker Eq. 2.1 and Eqs. 2.12-2.16; Meier Eq. 1
*Basis**: [DERIVED] A generating price requires strictly positive net output.
*Last Updated**: 2026-09-10

SysML Source: root-0/analyses/ife_lcoe.sysml:141
    """
    price: float = Field(description="price output")
    generating: float = Field(description="generating output")
