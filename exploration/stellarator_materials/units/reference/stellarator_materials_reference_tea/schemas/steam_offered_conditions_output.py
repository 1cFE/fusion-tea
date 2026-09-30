from pydantic import Field
from simkit.config.schema import MultiOutput

class Steam_Offered_ConditionsOutput(MultiOutput):
    """Multi-output container for Steam_Offered_Conditions.

Point-rating applicability: finite actual/supplied values match when equal or separated by at most 8*max(ulp(actual),ulp(supplied)); fixed numerical identity only, no public tolerance or physical envelope. Disabled returns unsupported/undefined; no inferred envelope. **Source**: work/active/WI-080_supplied-thermal-equipment-capability-and-demand-checks/evidence/capability-contract.json **Reference**: round2/architecture-review.md; entering-model checkpoint 53a0366a. **Basis**: [AGENT] assumed offered capability at declared conditions; captured design, not vendor qualification. **Last Updated**: 2026-09-20

SysML Source: root-0/analyses/mfe_viability.sysml:38
    """
    supported: bool = Field(description="supported output")
    applicable: bool = Field(description="applicable output")
    evaluation_defined: float = Field(description="evaluation_defined output")
