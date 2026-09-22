from pydantic import Field
from simkit.config.schema import MultiOutput

class Ideal_Gas_CompressorOutput(MultiOutput):
    """Multi-output container for Ideal_Gas_Compressor.

Source: work/active/WI-087_aries-nominal-brayton-component-cycle/spec.md. Ref: accepted source/design review in work/orchestration/aries-transfer-experiment/evidence/power-conversion-review.md. Basis: AGENT nominal ideal-gas component approximation. pout=pin*r; Tout=Tin*(1+(r^((gamma-1)/gamma)-1)/eta); shaft=mdot*cp*(Tout-Tin)/1e6. NASA compressor thermodynamics, retained authority pointer in knowledge/research/pending/20260907-163520_primary-loop-cycle-closure-prework.md section D. Units: K, MPa, kg/s, J/(kg K), MW; efficiencies dimensionless. Typed completion enforces finite outputs and the explicit domain in the spec. Last Updated: 2026-09-21.

SysML Source: root-0/ideal_gas_brayton_components.sysml:3
    """
    pressure_out: float = Field(description="pressure_out output")
    shaft_demand: float = Field(description="shaft_demand output")
    temperature_out: float = Field(description="temperature_out output")
