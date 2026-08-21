from pydantic import Field
from simkit.config.schema import MultiOutput

class MFE_Power_Balance_CalcOutput(MultiOutput):
    """Multi-output container for MFE_Power_Balance_Calc.

MFE (Magnetic Fusion Energy) power balance for tokamaks and
stellarators: fusion power -> net electric power, engineering Q, and
recirculating power fraction. Faithful to 1costingFE
mfe_forward_power_balance in the DEC-free, non-radiation-limited
regime (validity conditions below).

Power flow:
  - Alpha / neutron split of fusion power (D-T, inlined)
  - Thermal power = blanket neutron heating + charged-particle (alpha)
    power reaching the wall + heating power + recovered pumping heat
  - Thermal electric via the conversion efficiency eta_th
  - Recirculating power: coils + pumping + subsystems + auxiliary
    + cooling + cryo + wall-plug heating
  - Engineering Q = gross electric / recirculating

Thermal power derivation (WI-019): 1costingFE step 7 is
  p_th = mn*p_neutron + p_rad + p_wall + eta_p*p_pump   (physics.py:303)
with p_wall = p_ash + p_input_eff - p_rad at f_dec = 0
(physics.py:290-299), so p_rad cancels and
  p_th = mn*p_neutron + p_alpha + p_input + eta_p*p_pump.
Charged-particle power reaches the wall as radiation or as transport;
both are recovered thermally, so no radiation model is needed here.

Validity conditions (documented regime, WI-019 MR-WI019-4):
  1. f_dec = 0 -- no direct energy conversion (standing WI-009
     deviation, out of scope).
  2. p_rad - p_alpha <= p_input -- non-radiation-limited, so
     p_input_eff = p_input (physics.py:290). Deep margin for D-T
     (Anchor A point: p_rad 25.7 vs p_alpha 517 MW). Enforcement as
     a viability constraint is deferred to the predictive-physics
     item, which introduces p_rad to the model.

One further documented deviation from 1costingFE: the fuel-type
ash/neutron split (physics.py:160-181) is replaced by the inlined
D-T ratio 3.52/17.58 (p_alpha below; 1costingFE calls it p_ash) so
this calc stays flat and codegen-safe (no nested calc invocation).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:290-328 (steps 4-14, mfe_forward_power_balance)
*Basis**: Steady-state MFE power flow; tokamak/stellarator-generic

SysML Source: root-0/analyses/mfe_power_balance.sysml:4
    """
    p_the: float = Field(description="p_the output")
    p_et: float = Field(description="p_et output")
    q_eng: float = Field(description="q_eng output")
    p_th: float = Field(description="p_th output")
    p_net: float = Field(description="p_net output")
    rec_frac: float = Field(description="rec_frac output")
