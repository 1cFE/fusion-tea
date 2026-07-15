"""Auto-generated implementation for MFE_Power_Balance_Calc.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml:4

SysML Expressions:
    p_alpha = 0.2002 * p_nrl
    p_neutron = p_nrl - p_alpha
    p_cool = p_tfcool + p_pfcool
    p_aux = p_trit + p_house
    p_coils = p_tf + p_pf
    p_th = mn * p_neutron + p_input + eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron)
    p_the = eta_th * p_th
    p_et = p_the
    p_pump = fpcppf * p_the
    p_sub = f_sub * p_the
    recirculating = p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input / eta_pin
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et
    
Documentation:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_power_balance.mfe_power_balance_calc import MFE_Power_Balance_CalcInput


def run_mfe_power_balance_calc(inputs: MFE_Power_Balance_CalcInput) -> tuple[float, float, float, float, float, float]:
    """Execute MFE_Power_Balance_Calc calculation.

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

SysML Expressions:
    p_alpha = 0.2002 * p_nrl
    p_neutron = p_nrl - p_alpha
    p_cool = p_tfcool + p_pfcool
    p_aux = p_trit + p_house
    p_coils = p_tf + p_pf
    p_th = mn * p_neutron + p_input + eta_th * (fpcppf * eta_p + f_sub) * (mn * p_neutron)
    p_the = eta_th * p_th
    p_et = p_the
    p_pump = fpcppf * p_the
    p_sub = f_sub * p_the
    recirculating = p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input / eta_pin
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et
    
Documentation:
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

Args:
    inputs: Input parameters validated against MFE_Power_Balance_CalcInput schema

Returns:
    tuple[float, ...]: (p_th, p_the, p_et, q_eng, rec_frac, p_net)

Example:
    >>> inputs = MFE_Power_Balance_CalcInput(...)
    >>> p_th, p_the, p_et, q_eng, rec_frac, p_net = run_mfe_power_balance_calc(inputs)
    """
    p_alpha = (0.2002 * inputs.p_nrl)
    p_aux = (inputs.p_trit + inputs.p_house)
    p_coils = (inputs.p_tf + inputs.p_pf)
    p_cool = (inputs.p_tfcool + inputs.p_pfcool)
    p_neutron = (inputs.p_nrl - p_alpha)
    p_th = (((inputs.mn * p_neutron) + inputs.p_input) + ((inputs.eta_th * ((inputs.fpcppf * inputs.eta_p) + inputs.f_sub)) * (inputs.mn * p_neutron)))
    p_the = (inputs.eta_th * p_th)
    p_et = p_the
    p_pump = (inputs.fpcppf * p_the)
    p_sub = (inputs.f_sub * p_the)
    recirculating = ((((((p_coils + p_pump) + p_sub) + p_aux) + p_cool) + inputs.p_cryo) + (inputs.p_input / inputs.eta_pin))
    q_eng = (p_et / recirculating)
    rec_frac = (1.0 / q_eng)
    p_net = ((1.0 - rec_frac) * p_et)
    return (
        p_th,
        p_the,
        p_et,
        q_eng,
        rec_frac,
        p_net,
    )
