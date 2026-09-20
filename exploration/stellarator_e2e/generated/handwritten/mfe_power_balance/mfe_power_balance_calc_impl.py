"""Auto-generated implementation for MFE_Power_Balance_Calc.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_power_balance.sysml:4

SysML Expressions:
    p_wallplug_in = 0.0
    p_cycle_pumps_in = 0.0
    p_cooling_water_in = 0.0
    p_alpha = 3.52 / 17.58 * p_nrl
    p_neutron = p_nrl - p_alpha
    p_cool = p_tfcool_in + p_pfcool_in
    p_aux = p_trit_in + p_house_in
    p_coils = p_tf_in + p_pf_in
    p_th = mn_in * p_neutron + p_alpha + p_input_in + q_recovered_in
    p_the = eta_th_in * p_th
    p_et = p_the
    p_sub = f_sub_in * p_et
    recirculating = p_coils + p_pump_total_in + p_sub + p_aux + p_cool + p_cryo + p_wallplug_in + p_cycle_pumps_in + p_cooling_water_in
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et
    
Documentation:
WI-050: coupled auxiliary heat and wall-plug draw describe the same
sustained operating state. Installed heating remains a procurement and
capacity concern outside this balance. All powers are MW.
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

WI-045 (goal plant-closure): the recovered term arrives as
q_recovered_in from 'Primary Coolant Loop' (the loop's fluid work when
the loop is live; eta_p_direct * p_pump_direct when it is dormant) at
the position eta_p * p_pump occupied, and the pump draw arrives as
p_pump_total_in (loop_live * p_elec + p_pump_direct) at the position
p_pump occupied. In the dormant mode both are the old held scalars to
the bit, so this calc's sums are unchanged in every operand and
position; the credit's meaning is unchanged. The reactor's source heat
without the credit is published by 'Reactor Source Heat' below.

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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_power_balance.mfe_power_balance_calc import MFE_Power_Balance_CalcInput


def run_mfe_power_balance_calc(inputs: MFE_Power_Balance_CalcInput) -> tuple[float, float, float, float, float, float]:
    """Execute MFE_Power_Balance_Calc calculation.

WI-050: coupled auxiliary heat and wall-plug draw describe the same
sustained operating state. Installed heating remains a procurement and
capacity concern outside this balance. All powers are MW.
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

WI-045 (goal plant-closure): the recovered term arrives as
q_recovered_in from 'Primary Coolant Loop' (the loop's fluid work when
the loop is live; eta_p_direct * p_pump_direct when it is dormant) at
the position eta_p * p_pump occupied, and the pump draw arrives as
p_pump_total_in (loop_live * p_elec + p_pump_direct) at the position
p_pump occupied. In the dormant mode both are the old held scalars to
the bit, so this calc's sums are unchanged in every operand and
position; the credit's meaning is unchanged. The reactor's source heat
without the credit is published by 'Reactor Source Heat' below.

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

SysML Expressions:
    p_wallplug_in = 0.0
    p_cycle_pumps_in = 0.0
    p_cooling_water_in = 0.0
    p_alpha = 3.52 / 17.58 * p_nrl
    p_neutron = p_nrl - p_alpha
    p_cool = p_tfcool_in + p_pfcool_in
    p_aux = p_trit_in + p_house_in
    p_coils = p_tf_in + p_pf_in
    p_th = mn_in * p_neutron + p_alpha + p_input_in + q_recovered_in
    p_the = eta_th_in * p_th
    p_et = p_the
    p_sub = f_sub_in * p_et
    recirculating = p_coils + p_pump_total_in + p_sub + p_aux + p_cool + p_cryo + p_wallplug_in + p_cycle_pumps_in + p_cooling_water_in
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et
    
Documentation:
WI-050: coupled auxiliary heat and wall-plug draw describe the same
sustained operating state. Installed heating remains a procurement and
capacity concern outside this balance. All powers are MW.
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

WI-045 (goal plant-closure): the recovered term arrives as
q_recovered_in from 'Primary Coolant Loop' (the loop's fluid work when
the loop is live; eta_p_direct * p_pump_direct when it is dormant) at
the position eta_p * p_pump occupied, and the pump draw arrives as
p_pump_total_in (loop_live * p_elec + p_pump_direct) at the position
p_pump occupied. In the dormant mode both are the old held scalars to
the bit, so this calc's sums are unchanged in every operand and
position; the credit's meaning is unchanged. The reactor's source heat
without the credit is published by 'Reactor Source Heat' below.

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

Args:
    inputs: Input parameters validated against MFE_Power_Balance_CalcInput schema

Returns:
    tuple[float, ...]: (p_the, p_et, q_eng, p_th, p_net, rec_frac)

Example:
    >>> inputs = MFE_Power_Balance_CalcInput(...)
    >>> p_the, p_et, q_eng, p_th, p_net, rec_frac = run_mfe_power_balance_calc(inputs)
    """
    p_aux = (inputs.p_trit_in + inputs.p_house_in)
    p_coils = (inputs.p_tf_in + inputs.p_pf_in)
    p_cool = (inputs.p_tfcool_in + inputs.p_pfcool_in)
    p_alpha = ((3.52 / 17.58) * inputs.p_nrl)
    p_neutron = (inputs.p_nrl - p_alpha)
    p_th = ((((inputs.mn_in * p_neutron) + p_alpha) + inputs.p_input_in) + inputs.q_recovered_in)
    p_the = (inputs.eta_th_in * p_th)
    p_et = p_the
    p_sub = (inputs.f_sub_in * p_et)
    recirculating = ((((((((p_coils + inputs.p_pump_total_in) + p_sub) + p_aux) + p_cool) + inputs.p_cryo) + inputs.p_wallplug_in) + inputs.p_cycle_pumps_in) + inputs.p_cooling_water_in)
    q_eng = (p_et / recirculating)
    rec_frac = (1.0 / q_eng)
    return (
        p_the,
        p_et,
        q_eng,
        p_th,
        ((1.0 - rec_frac) * p_et),  # p_net
        rec_frac,
    )
