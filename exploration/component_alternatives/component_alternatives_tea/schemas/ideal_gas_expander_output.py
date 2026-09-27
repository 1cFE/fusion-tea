from pydantic import Field
from simkit.config.schema import MultiOutput

class Ideal_Gas_ExpanderOutput(MultiOutput):
    """Multi-output container for Ideal_Gas_Expander.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. Tout=Tin*(1-eta*(1-(pout/pin)^((gamma-1)/gamma))); shaft=mdot*cp*(Tin-Tout)/1e6. Ideal-gas isentropic expansion with supplied efficiency, focused independent design review. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

SysML Source: root-0/ideal_gas_brayton_components.sysml:16
    """
    pressure_out: float = Field(description="pressure_out output")
    shaft_produced: float = Field(description="shaft_produced output")
    temperature_out: float = Field(description="temperature_out output")
