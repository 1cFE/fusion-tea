from pydantic import Field
from simkit.config.schema import MultiOutput

class Conditional_Cryogenic_DemandOutput(MultiOutput):
    """Multi-output container for Conditional_Cryogenic_Demand.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/conditional_cryogenic_demand_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:56
    """
    intercept_W: float = Field(description="intercept_W output")
    extra_cold_capacity_W: float = Field(description="extra_cold_capacity_W output")
    domain_supported: float = Field(description="domain_supported output")
    refrigeration_MW: float = Field(description="refrigeration_MW output")
    nuclear_transport_qualified: float = Field(description="nuclear_transport_qualified output")
    intercept_margin_W: float = Field(description="intercept_margin_W output")
    cold_W: float = Field(description="cold_W output")
    cold_electric_MW: float = Field(description="cold_electric_MW output")
    intercept_electric_MW: float = Field(description="intercept_electric_MW output")
    cold_margin_W: float = Field(description="cold_margin_W output")
    q_nuc_capacity_W_m3: float = Field(description="q_nuc_capacity_W_m3 output")
