"""MFE_Power_Balance_CalcModule Module Wrapper

TEAx module for MFE_Power_Balance_Calc calculation.

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

Inputs:
    - p_tfcool_in: p_tfcool_in parameter
    - p_cryo: p_cryo parameter
    - p_nrl: p_nrl parameter
    - f_sub_in: f_sub_in parameter
    - p_pfcool_in: p_pfcool_in parameter
    - eta_p_in: eta_p_in parameter
    - p_pf_in: p_pf_in parameter
    - p_wallplug_in: p_wallplug_in parameter
    - p_house_in: p_house_in parameter
    - mn_in: mn_in parameter
    - eta_th_in: eta_th_in parameter
    - p_tf_in: p_tf_in parameter
    - p_pump_in: p_pump_in parameter
    - p_input_in: p_input_in parameter
    - p_trit_in: p_trit_in parameter

Outputs:
    - p_the: p_the result
    - p_et: p_et result
    - q_eng: q_eng result
    - p_th: p_th result
    - p_net: p_net result
    - rec_frac: rec_frac result

SysML Source: root-0/analyses/mfe_power_balance.sysml:4

SysML Source: root-0/analyses/mfe_power_balance.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_power_balance/mfe_power_balance_calc_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.mfe_power_balance_calc_output import MFE_Power_Balance_CalcOutput


class MFE_Power_Balance_CalcInput(BaseModel):
    """Input model for MFE_Power_Balance_CalcModule.

    Attributes:
        p_tfcool_in: p_tfcool_in input
        p_cryo: p_cryo input
        p_nrl: p_nrl input
        f_sub_in: f_sub_in input
        p_pfcool_in: p_pfcool_in input
        eta_p_in: eta_p_in input
        p_pf_in: p_pf_in input
        p_wallplug_in: p_wallplug_in input
        p_house_in: p_house_in input
        mn_in: mn_in input
        eta_th_in: eta_th_in input
        p_tf_in: p_tf_in input
        p_pump_in: p_pump_in input
        p_input_in: p_input_in input
        p_trit_in: p_trit_in input
    """
    p_tfcool_in: float = Field(..., description="p_tfcool_in input")
    p_cryo: float = Field(..., description="p_cryo input")
    p_nrl: float = Field(..., description="p_nrl input")
    f_sub_in: float = Field(..., description="f_sub_in input")
    p_pfcool_in: float = Field(..., description="p_pfcool_in input")
    eta_p_in: float = Field(..., description="eta_p_in input")
    p_pf_in: float = Field(..., description="p_pf_in input")
    p_wallplug_in: float = Field(..., description="p_wallplug_in input")
    p_house_in: float = Field(..., description="p_house_in input")
    mn_in: float = Field(..., description="mn_in input")
    eta_th_in: float = Field(..., description="eta_th_in input")
    p_tf_in: float = Field(..., description="p_tf_in input")
    p_pump_in: float = Field(..., description="p_pump_in input")
    p_input_in: float = Field(..., description="p_input_in input")
    p_trit_in: float = Field(..., description="p_trit_in input")


class MFE_Power_Balance_CalcModule(ModuleBase[MFE_Power_Balance_CalcInput, MFE_Power_Balance_CalcOutput]):
    """TEAx module for MFE_Power_Balance_Calc calculation.

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

Inputs:
    - p_tfcool_in: p_tfcool_in parameter
    - p_cryo: p_cryo parameter
    - p_nrl: p_nrl parameter
    - f_sub_in: f_sub_in parameter
    - p_pfcool_in: p_pfcool_in parameter
    - eta_p_in: eta_p_in parameter
    - p_pf_in: p_pf_in parameter
    - p_wallplug_in: p_wallplug_in parameter
    - p_house_in: p_house_in parameter
    - mn_in: mn_in parameter
    - eta_th_in: eta_th_in parameter
    - p_tf_in: p_tf_in parameter
    - p_pump_in: p_pump_in parameter
    - p_input_in: p_input_in parameter
    - p_trit_in: p_trit_in parameter

Outputs:
    - p_the: p_the result
    - p_et: p_et result
    - q_eng: q_eng result
    - p_th: p_th result
    - p_net: p_net result
    - rec_frac: rec_frac result

SysML Source: root-0/analyses/mfe_power_balance.sysml:4

    SysML Source: root-0/analyses/mfe_power_balance.sysml:4

    Calculation Specification:
        p_wallplug_in = 0.0
        p_alpha = 3.52 / 17.58 * p_nrl
        p_neutron = p_nrl - p_alpha
        p_cool = p_tfcool_in + p_pfcool_in
        p_aux = p_trit_in + p_house_in
        p_coils = p_tf_in + p_pf_in
        p_th = mn_in * p_neutron + p_alpha + p_input_in + eta_p_in * p_pump_in
        p_the = eta_th_in * p_th
        p_et = p_the
        p_sub = f_sub_in * p_et
        recirculating = p_coils + p_pump_in + p_sub + p_aux + p_cool + p_cryo + p_wallplug_in
        q_eng = p_et / recirculating
        rec_frac = 1.0 / q_eng
        p_net = (1.0 - rec_frac) * p_et
        
Documentation:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_power_balance.mfe_power_balance_calc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts p_the, p_et, q_eng, p_th, p_net, rec_frac fields to separate channels.
    """

    name: str = "MFE_Power_Balance_CalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_tfcool_in: float, p_cryo: float, p_nrl: float, f_sub_in: float, p_pfcool_in: float, eta_p_in: float, p_pf_in: float, p_wallplug_in: float, p_house_in: float, mn_in: float, eta_th_in: float, p_tf_in: float, p_pump_in: float, p_input_in: float, p_trit_in: float    ) -> MFE_Power_Balance_CalcInput:
        """Validate inputs and fill defaults.

        Args:
            p_tfcool_in: p_tfcool_in input
            p_cryo: p_cryo input
            p_nrl: p_nrl input
            f_sub_in: f_sub_in input
            p_pfcool_in: p_pfcool_in input
            eta_p_in: eta_p_in input
            p_pf_in: p_pf_in input
            p_wallplug_in: p_wallplug_in input
            p_house_in: p_house_in input
            mn_in: mn_in input
            eta_th_in: eta_th_in input
            p_tf_in: p_tf_in input
            p_pump_in: p_pump_in input
            p_input_in: p_input_in input
            p_trit_in: p_trit_in input

        Returns:
            Validated input model
        """
        return MFE_Power_Balance_CalcInput(p_tfcool_in=p_tfcool_in, p_cryo=p_cryo, p_nrl=p_nrl, f_sub_in=f_sub_in, p_pfcool_in=p_pfcool_in, eta_p_in=eta_p_in, p_pf_in=p_pf_in, p_wallplug_in=p_wallplug_in, p_house_in=p_house_in, mn_in=mn_in, eta_th_in=eta_th_in, p_tf_in=p_tf_in, p_pump_in=p_pump_in, p_input_in=p_input_in, p_trit_in=p_trit_in)

    def run(
        self, p_tfcool_in: float, p_cryo: float, p_nrl: float, f_sub_in: float, p_pfcool_in: float, eta_p_in: float, p_pf_in: float, p_wallplug_in: float, p_house_in: float, mn_in: float, eta_th_in: float, p_tf_in: float, p_pump_in: float, p_input_in: float, p_trit_in: float    ) -> ModuleResult[MFE_Power_Balance_CalcOutput]:
        """Execute calculation.

        Args:
            p_tfcool_in: p_tfcool_in input
            p_cryo: p_cryo input
            p_nrl: p_nrl input
            f_sub_in: f_sub_in input
            p_pfcool_in: p_pfcool_in input
            eta_p_in: eta_p_in input
            p_pf_in: p_pf_in input
            p_wallplug_in: p_wallplug_in input
            p_house_in: p_house_in input
            mn_in: mn_in input
            eta_th_in: eta_th_in input
            p_tf_in: p_tf_in input
            p_pump_in: p_pump_in input
            p_input_in: p_input_in input
            p_trit_in: p_trit_in input

        Returns:
            Module result with MFE_Power_Balance_CalcOutput (p_the, p_et, q_eng, p_th, p_net, rec_frac)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_tfcool_in, p_cryo, p_nrl, f_sub_in, p_pfcool_in, eta_p_in, p_pf_in, p_wallplug_in, p_house_in, mn_in, eta_th_in, p_tf_in, p_pump_in, p_input_in, p_trit_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_power_balance.mfe_power_balance_calc_impl import (
            run_mfe_power_balance_calc,
        )

        # Execute implementation - returns tuple of values
        p_the, p_et, q_eng, p_th, p_net, rec_frac = run_mfe_power_balance_calc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=MFE_Power_Balance_CalcOutput(
                p_the=p_the,
                p_et=p_et,
                q_eng=q_eng,
                p_th=p_th,
                p_net=p_net,
                rec_frac=rec_frac,
            )
        )
