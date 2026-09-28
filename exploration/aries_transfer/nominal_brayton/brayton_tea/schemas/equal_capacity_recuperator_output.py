from pydantic import Field
from simkit.config.schema import MultiOutput

class Equal_Capacity_RecuperatorOutput(MultiOutput):
    """Multi-output container for Equal_Capacity_Recuperator.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. heat=eps*mdot*cp*(Thot-Tcold)/1e6; Tcoldout=Tcold+eps*(Thot-Tcold); Thotout=Thot-eps*(Thot-Tcold). Equal heat-capacity rates and no heat loss. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

SysML Source: root-0/ideal_gas_brayton_components.sysml:41
    """
    transferred_heat: float = Field(description="transferred_heat output")
    hot_temperature_out: float = Field(description="hot_temperature_out output")
    cold_temperature_out: float = Field(description="cold_temperature_out output")
