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
    - p_nrl: p_nrl parameter
    - p_input: p_input parameter
    - mn: mn parameter
    - eta_th: eta_th parameter
    - eta_p: eta_p parameter
    - eta_pin: eta_pin parameter
    - p_pump: p_pump parameter
    - f_sub: f_sub parameter
    - p_tf: p_tf parameter
    - p_pf: p_pf parameter
    - p_tfcool: p_tfcool parameter
    - p_pfcool: p_pfcool parameter
    - p_trit: p_trit parameter
    - p_house: p_house parameter
    - p_cryo: p_cryo parameter

Outputs:
    - p_th: p_th result
    - p_the: p_the result
    - p_et: p_et result
    - q_eng: q_eng result
    - rec_frac: rec_frac result
    - p_net: p_net result

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
        p_nrl: p_nrl input
        p_input: p_input input
        mn: mn input
        eta_th: eta_th input
        eta_p: eta_p input
        eta_pin: eta_pin input
        p_pump: p_pump input
        f_sub: f_sub input
        p_tf: p_tf input
        p_pf: p_pf input
        p_tfcool: p_tfcool input
        p_pfcool: p_pfcool input
        p_trit: p_trit input
        p_house: p_house input
        p_cryo: p_cryo input
    """
    p_nrl: float = Field(..., description="p_nrl input")
    p_input: float = Field(..., description="p_input input")
    mn: float = Field(..., description="mn input")
    eta_th: float = Field(..., description="eta_th input")
    eta_p: float = Field(..., description="eta_p input")
    eta_pin: float = Field(..., description="eta_pin input")
    p_pump: float = Field(..., description="p_pump input")
    f_sub: float = Field(..., description="f_sub input")
    p_tf: float = Field(..., description="p_tf input")
    p_pf: float = Field(..., description="p_pf input")
    p_tfcool: float = Field(..., description="p_tfcool input")
    p_pfcool: float = Field(..., description="p_pfcool input")
    p_trit: float = Field(..., description="p_trit input")
    p_house: float = Field(..., description="p_house input")
    p_cryo: float = Field(..., description="p_cryo input")


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
    - p_nrl: p_nrl parameter
    - p_input: p_input parameter
    - mn: mn parameter
    - eta_th: eta_th parameter
    - eta_p: eta_p parameter
    - eta_pin: eta_pin parameter
    - p_pump: p_pump parameter
    - f_sub: f_sub parameter
    - p_tf: p_tf parameter
    - p_pf: p_pf parameter
    - p_tfcool: p_tfcool parameter
    - p_pfcool: p_pfcool parameter
    - p_trit: p_trit parameter
    - p_house: p_house parameter
    - p_cryo: p_cryo parameter

Outputs:
    - p_th: p_th result
    - p_the: p_the result
    - p_et: p_et result
    - q_eng: q_eng result
    - rec_frac: rec_frac result
    - p_net: p_net result

SysML Source: root-0/analyses/mfe_power_balance.sysml:4

    SysML Source: root-0/analyses/mfe_power_balance.sysml:4

    Calculation Specification:
        p_alpha = 3.52 / 17.58 * p_nrl
        p_neutron = p_nrl - p_alpha
        p_cool = p_tfcool + p_pfcool
        p_aux = p_trit + p_house
        p_coils = p_tf + p_pf
        p_th = mn * p_neutron + p_alpha + p_input + eta_p * p_pump
        p_the = eta_th * p_th
        p_et = p_the
        p_sub = f_sub * p_et
        recirculating = p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input / eta_pin
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
    TEAx automatically extracts p_th, p_the, p_et, q_eng, rec_frac, p_net fields to separate channels.
    """

    name: str = "MFE_Power_Balance_CalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_nrl: float, p_input: float, mn: float, eta_th: float, eta_p: float, eta_pin: float, p_pump: float, f_sub: float, p_tf: float, p_pf: float, p_tfcool: float, p_pfcool: float, p_trit: float, p_house: float, p_cryo: float    ) -> MFE_Power_Balance_CalcInput:
        """Validate inputs and fill defaults.

        Args:
            p_nrl: p_nrl input
            p_input: p_input input
            mn: mn input
            eta_th: eta_th input
            eta_p: eta_p input
            eta_pin: eta_pin input
            p_pump: p_pump input
            f_sub: f_sub input
            p_tf: p_tf input
            p_pf: p_pf input
            p_tfcool: p_tfcool input
            p_pfcool: p_pfcool input
            p_trit: p_trit input
            p_house: p_house input
            p_cryo: p_cryo input

        Returns:
            Validated input model
        """
        return MFE_Power_Balance_CalcInput(p_nrl=p_nrl, p_input=p_input, mn=mn, eta_th=eta_th, eta_p=eta_p, eta_pin=eta_pin, p_pump=p_pump, f_sub=f_sub, p_tf=p_tf, p_pf=p_pf, p_tfcool=p_tfcool, p_pfcool=p_pfcool, p_trit=p_trit, p_house=p_house, p_cryo=p_cryo)

    def run(
        self, p_nrl: float, p_input: float, mn: float, eta_th: float, eta_p: float, eta_pin: float, p_pump: float, f_sub: float, p_tf: float, p_pf: float, p_tfcool: float, p_pfcool: float, p_trit: float, p_house: float, p_cryo: float    ) -> ModuleResult[MFE_Power_Balance_CalcOutput]:
        """Execute calculation.

        Args:
            p_nrl: p_nrl input
            p_input: p_input input
            mn: mn input
            eta_th: eta_th input
            eta_p: eta_p input
            eta_pin: eta_pin input
            p_pump: p_pump input
            f_sub: f_sub input
            p_tf: p_tf input
            p_pf: p_pf input
            p_tfcool: p_tfcool input
            p_pfcool: p_pfcool input
            p_trit: p_trit input
            p_house: p_house input
            p_cryo: p_cryo input

        Returns:
            Module result with MFE_Power_Balance_CalcOutput (p_th, p_the, p_et, q_eng, rec_frac, p_net)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_nrl, p_input, mn, eta_th, eta_p, eta_pin, p_pump, f_sub, p_tf, p_pf, p_tfcool, p_pfcool, p_trit, p_house, p_cryo)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_power_balance.mfe_power_balance_calc_impl import (
            run_mfe_power_balance_calc,
        )

        # Execute implementation - returns tuple of values
        p_th, p_the, p_et, q_eng, rec_frac, p_net = run_mfe_power_balance_calc(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=MFE_Power_Balance_CalcOutput(
                p_th=p_th,
                p_the=p_the,
                p_et=p_et,
                q_eng=q_eng,
                rec_frac=rec_frac,
                p_net=p_net,
            )
        )
