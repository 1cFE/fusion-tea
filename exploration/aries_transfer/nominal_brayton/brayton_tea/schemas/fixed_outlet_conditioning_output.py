from pydantic import Field
from simkit.config.schema import MultiOutput

class Fixed_Outlet_ConditioningOutput(MultiOutput):
    """Multi-output container for Fixed_Outlet_Conditioning.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=target; pout=pin; heat=mdot*cp*(target-Tin)/1e6. Heating role1 requires positive temperature rise; cooling role0 requires nonpositive rise. Signed heat into fluid. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

SysML Source: root-0/ideal_gas_brayton_components.sysml:29
    """
    heat_into_fluid: float = Field(description="heat_into_fluid output")
    temperature_out: float = Field(description="temperature_out output")
    pressure_out: float = Field(description="pressure_out output")
