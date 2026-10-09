from pydantic import Field
from simkit.config.schema import MultiOutput

class Facility_Civil_CostOutput(MultiOutput):
    """Multi-output container for Facility_Civil_Cost.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Six installed-direct commodity products, original2018 and CPI-normalized2025 purchasing power. Disabled returns zero; no repeated installation.

SysML Source: root-0/analyses/mfe_facilities.sysml:667
    """
    sub_cost_2018: float = Field(description="sub_cost_2018 output")
    super_cost_2018: float = Field(description="super_cost_2018 output")
    cost_2025: float = Field(description="cost_2025 output")
    cost_2018: float = Field(description="cost_2018 output")
