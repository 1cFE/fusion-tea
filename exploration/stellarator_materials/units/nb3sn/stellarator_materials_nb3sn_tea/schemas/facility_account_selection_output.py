from pydantic import Field
from simkit.config.schema import MultiOutput

class Facility_Account_SelectionOutput(MultiOutput):
    """Multi-output container for Facility_Account_Selection.

*Source**: work/active/WI-068_layout-based-facilities/design.md. **Ref**: account replacement map and component-owned aggregation. **Basis**: Select the complete priced facility account or the preserved grouped legacy account; layout validates the binary mode.

SysML Source: root-0/analyses/mfe_facilities.sysml:746
    """
    layout_buildings_capital: float = Field(description="layout_buildings_capital output")
    cost: float = Field(description="cost output")
    installed_facility_capital: float = Field(description="installed_facility_capital output")
