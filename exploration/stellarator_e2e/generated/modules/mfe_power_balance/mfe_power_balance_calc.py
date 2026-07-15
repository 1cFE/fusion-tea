"""MFE_Power_Balance_CalcModule Module Wrapper

TEAx module for MFE_Power_Balance_Calc calculation.

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

Inputs:
    - p_nrl: p_nrl parameter
    - p_input: p_input parameter
    - mn: mn parameter
    - eta_th: eta_th parameter
    - eta_p: eta_p parameter
    - eta_pin: eta_pin parameter
    - fpcppf: fpcppf parameter
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

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml:4

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml:4

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
        fpcppf: fpcppf input
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
    fpcppf: float = Field(..., description="fpcppf input")
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

Inputs:
    - p_nrl: p_nrl parameter
    - p_input: p_input parameter
    - mn: mn parameter
    - eta_th: eta_th parameter
    - eta_p: eta_p parameter
    - eta_pin: eta_pin parameter
    - fpcppf: fpcppf parameter
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

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml:4

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml:4

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_power_balance.mfe_power_balance_calc_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts p_th, p_the, p_et, q_eng, rec_frac, p_net fields to separate channels.
    """

    name: str = "MFE_Power_Balance_CalcModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_nrl: float, p_input: float, mn: float, eta_th: float, eta_p: float, eta_pin: float, fpcppf: float, f_sub: float, p_tf: float, p_pf: float, p_tfcool: float, p_pfcool: float, p_trit: float, p_house: float, p_cryo: float    ) -> MFE_Power_Balance_CalcInput:
        """Validate inputs and fill defaults.

        Args:
            p_nrl: p_nrl input
            p_input: p_input input
            mn: mn input
            eta_th: eta_th input
            eta_p: eta_p input
            eta_pin: eta_pin input
            fpcppf: fpcppf input
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
        return MFE_Power_Balance_CalcInput(p_nrl=p_nrl, p_input=p_input, mn=mn, eta_th=eta_th, eta_p=eta_p, eta_pin=eta_pin, fpcppf=fpcppf, f_sub=f_sub, p_tf=p_tf, p_pf=p_pf, p_tfcool=p_tfcool, p_pfcool=p_pfcool, p_trit=p_trit, p_house=p_house, p_cryo=p_cryo)

    def run(
        self, p_nrl: float, p_input: float, mn: float, eta_th: float, eta_p: float, eta_pin: float, fpcppf: float, f_sub: float, p_tf: float, p_pf: float, p_tfcool: float, p_pfcool: float, p_trit: float, p_house: float, p_cryo: float    ) -> ModuleResult[MFE_Power_Balance_CalcOutput]:
        """Execute calculation.

        Args:
            p_nrl: p_nrl input
            p_input: p_input input
            mn: mn input
            eta_th: eta_th input
            eta_p: eta_p input
            eta_pin: eta_pin input
            fpcppf: fpcppf input
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
        validated_inputs = self.validate_and_fill_default(p_nrl, p_input, mn, eta_th, eta_p, eta_pin, fpcppf, f_sub, p_tf, p_pf, p_tfcool, p_pfcool, p_trit, p_house, p_cryo)

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
