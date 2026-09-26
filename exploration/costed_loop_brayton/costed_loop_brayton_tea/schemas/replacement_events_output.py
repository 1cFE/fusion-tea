from pydantic import Field
from simkit.config.schema import MultiOutput

class Replacement_EventsOutput(MultiOutput):
    """Multi-output container for Replacement_Events.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

SysML Source: root-0/integrated_equipment_costs.sysml:66
    """
    lifetime_total: float = Field(description="lifetime_total output")
    interval_years: float = Field(description="interval_years output")
    event_cost: float = Field(description="event_cost output")
    last_event_year: float = Field(description="last_event_year output")
    annual_reserve: float = Field(description="annual_reserve output")
    first_event_year: float = Field(description="first_event_year output")
    event_count: float = Field(description="event_count output")
