from pydantic import Field
from simkit.config.schema import MultiOutput

class MFE_Power_Balance_CalcOutput(MultiOutput):
    """Multi-output container for MFE_Power_Balance_Calc.

MFE (Magnetic Fusion Energy) power balance for tokamaks and
stellarators: fusion power -> net electric power, engineering Q, and
recirculating power fraction.

Power flow:
  - Alpha / neutron split of fusion power (D-T, inlined)
  - Thermal power = neutron heating + input + recovered pumping heat
  - Thermal electric via the conversion efficiency eta_th
  - Recirculating power: coils + pumping + subsystems + auxiliary
    + cooling + cryo + wall-plug heating
  - Engineering Q = gross electric / recirculating

Two documented deviations from the base PyFECONS balance:
  1. Direct energy conversion (p_dee, eta_de) is dropped, as in the
     archived revival base and the WI-009 spec (out of scope).
  2. The fuel-type-dependent 'Alpha Power Calc' is replaced by an
     inlined D-T alpha fraction (see p_alpha below) so this calc stays
     flat and codegen-safe (no nested calc invocation).
The top-level q_eng / rec_frac / p_net relations follow current
1costingFE (physics.py:324-328), not the older archived q_eng
numerator.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:183-328 (mfe_forward_power_balance)
*Basis**: Steady-state MFE power flow; tokamak/stellarator-generic

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml:4
    """
    p_th: float = Field(description="p_th output")
    p_the: float = Field(description="p_the output")
    p_et: float = Field(description="p_et output")
    q_eng: float = Field(description="q_eng output")
    rec_frac: float = Field(description="rec_frac output")
    p_net: float = Field(description="p_net output")
