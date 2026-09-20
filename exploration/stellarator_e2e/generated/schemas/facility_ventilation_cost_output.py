from pydantic import Field
from simkit.config.schema import MultiOutput

class Facility_Ventilation_CostOutput(MultiOutput):
    """Multi-output container for Facility_Ventilation_Cost.

Source: work/active/WI-068_layout-based-facilities/design.md; layout-capacity-design.md; evidence/facility-contract.md. Ref: released geometry, capacity, exact civil takeoff and account boundary. Basis: conditional conceptual scenario; unqualified shielding/loading/transport and explicit provisional equipment envelopes. Historical PROCESS1990 empirical nuclear-ventilation relation; does not qualify airflow.

SysML Source: root-0/analyses/mfe_facilities.sysml:702
    """
    cost_2025: float = Field(description="cost_2025 output")
    cost_1990: float = Field(description="cost_1990 output")
