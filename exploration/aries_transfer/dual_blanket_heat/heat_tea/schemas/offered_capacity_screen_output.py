from pydantic import Field
from simkit.config.schema import MultiOutput

class Offered_Capacity_ScreenOutput(MultiOutput):
    """Multi-output container for Offered_Capacity_Screen.

Strict rating minus demand at separately checked offered conditions. The guarded native completion rejects nonfinite/negative ratings and active demands, reports undefined if inactive, unsupported or demand unavailable, and never snaps margins. No equipment qualification is implied. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

SysML Source: root-0/mfe_viability.sysml:106
    """
    evaluation_defined: float = Field(description="evaluation_defined output")
    margin: float = Field(description="margin output")
    applicable: bool = Field(description="applicable output")
    supported: bool = Field(description="supported output")
    capacity_ok: bool = Field(description="capacity_ok output")
