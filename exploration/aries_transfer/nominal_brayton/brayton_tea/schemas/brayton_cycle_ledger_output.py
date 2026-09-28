from pydantic import Field
from simkit.config.schema import MultiOutput

class Brayton_Cycle_LedgerOutput(MultiOutput):
    """Multi-output container for Brayton_Cycle_Ledger.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. compressor_demand=W1+W2+W3; rejected_heat=-(Qic1+Qic2+Qpre); net_shaft=Wt-compressor_demand; shaft_efficiency=net_shaft/Qheater; energy_residual=Qheater-rejected_heat-net_shaft; total_pressure_ratio=pdischarge/pin. Cooling heats<=0, heater>0, shaft magnitudes>=0; signed net and residual preserved. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

SysML Source: root-0/ideal_gas_brayton_components.sysml:58
    """
    shaft_efficiency: float = Field(description="shaft_efficiency output")
    net_shaft: float = Field(description="net_shaft output")
    compressor_demand: float = Field(description="compressor_demand output")
    rejected_heat: float = Field(description="rejected_heat output")
    energy_residual: float = Field(description="energy_residual output")
    total_pressure_ratio: float = Field(description="total_pressure_ratio output")
