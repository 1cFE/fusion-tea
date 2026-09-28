from pydantic import Field
from simkit.config.schema import MultiOutput

class MatchOutput(MultiOutput):
    """Multi-output container for Match.

SysML Source: root-0/probe.sysml:7
    """
    gross_out: float = Field(description="gross_out output")
    state_h: float = Field(description="state_h output")
    pump_out: float = Field(description="pump_out output")
