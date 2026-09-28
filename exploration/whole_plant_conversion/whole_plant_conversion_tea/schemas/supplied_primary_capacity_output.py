from pydantic import Field
from simkit.config.schema import MultiOutput

class Supplied_Primary_CapacityOutput(MultiOutput):
    """Multi-output container for Supplied_Primary_Capacity.

*Source**: work/active/WI-098_whole-plant-conversion-comparison/design.md. **Reference**: accepted r2 and capture correction. **Basis**: [AGENT] conditional supplied source, USD2025; assumptions remain explicit. **Last Updated**: 2026-09-27. Complete normative numerical semantics: exploration/whole_plant_conversion/bodies/whole_plant_conversion_accounts/supplied_primary_capacity_impl.py; reviewed equations in design/configuration.

SysML Source: root-0/whole_plant_conversion_accounts.sysml:127
    """
    electric_margin_MW: float = Field(description="electric_margin_MW output")
    pressure_margin_Pa: float = Field(description="pressure_margin_Pa output")
    flow_margin_kg_s: float = Field(description="flow_margin_kg_s output")
    inventory_supported: float = Field(description="inventory_supported output")
