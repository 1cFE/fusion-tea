"""Winding_Pack_Procurement_CostModule Module Wrapper

TEAx module for Winding_Pack_Procurement_Cost calculation.

Additive composite-tape procurement, non-tape material procurement and winding operations. Casing and primary structure remain separate accounts. Normative manual-completion equations: K = n_coils * I_coil * f_set * c_coil / 1000 [kA m]; tape_cost = K * cost_per_kAm; conductor_length = 1000 * K / turn_current [m]; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Inputs: n_coils and f_set dimensionless; I_coil ampere-turns; c_coil m; cost_per_kAm dollars/(kA m); turn_current A; winding_rate_1990 dollars1990/m; escalation and nonplanar factor dimensionless; material_cost_in dollars. Outputs: costs dollars, conductor_length m of composite conductor (not tape metres). Winding operations are not a complete factory quote or a labor-only rate. Steel sheath charges would overlap explicit pack steel; unresolved fixed cable and insulation quantities are omitted. Rate transfer to REBCO is an assumption.
Domain: every input and output finite; n_coils, c_coil, turn_current, cost_escalation and nonplanar_factor > 0; I_coil, cost_per_kAm, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic and refuses non-finite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-13

Inputs:
    - f_set: f_set parameter
    - winding_rate_1990: winding_rate_1990 parameter
    - material_cost_in: material_cost_in parameter
    - n_coils: n_coils parameter
    - c_coil: c_coil parameter
    - turn_current: turn_current parameter
    - cost_per_kAm: cost_per_kAm parameter
    - I_coil: I_coil parameter
    - nonplanar_factor: nonplanar_factor parameter
    - cost_escalation: cost_escalation parameter

Outputs:
    - winding_fabrication_cost: winding_fabrication_cost result
    - cost: cost result
    - tape_cost: tape_cost result
    - conductor_length: conductor_length result

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_winding_pack_cost/winding_pack_procurement_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.winding_pack_procurement_cost_output import Winding_Pack_Procurement_CostOutput


class Winding_Pack_Procurement_CostInput(BaseModel):
    """Input model for Winding_Pack_Procurement_CostModule.

    Attributes:
        f_set: f_set input
        winding_rate_1990: winding_rate_1990 input
        material_cost_in: material_cost_in input
        n_coils: n_coils input
        c_coil: c_coil input
        turn_current: turn_current input
        cost_per_kAm: cost_per_kAm input
        I_coil: I_coil input
        nonplanar_factor: nonplanar_factor input
        cost_escalation: cost_escalation input
    """
    f_set: float = Field(..., description="f_set input")
    winding_rate_1990: float = Field(..., description="winding_rate_1990 input")
    material_cost_in: float = Field(..., description="material_cost_in input")
    n_coils: float = Field(..., description="n_coils input")
    c_coil: float = Field(..., description="c_coil input")
    turn_current: float = Field(..., description="turn_current input")
    cost_per_kAm: float = Field(..., description="cost_per_kAm input")
    I_coil: float = Field(..., description="I_coil input")
    nonplanar_factor: float = Field(..., description="nonplanar_factor input")
    cost_escalation: float = Field(..., description="cost_escalation input")


class Winding_Pack_Procurement_CostModule(ModuleBase[Winding_Pack_Procurement_CostInput, Winding_Pack_Procurement_CostOutput]):
    """TEAx module for Winding_Pack_Procurement_Cost calculation.

Additive composite-tape procurement, non-tape material procurement and winding operations. Casing and primary structure remain separate accounts. Normative manual-completion equations: K = n_coils * I_coil * f_set * c_coil / 1000 [kA m]; tape_cost = K * cost_per_kAm; conductor_length = 1000 * K / turn_current [m]; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Inputs: n_coils and f_set dimensionless; I_coil ampere-turns; c_coil m; cost_per_kAm dollars/(kA m); turn_current A; winding_rate_1990 dollars1990/m; escalation and nonplanar factor dimensionless; material_cost_in dollars. Outputs: costs dollars, conductor_length m of composite conductor (not tape metres). Winding operations are not a complete factory quote or a labor-only rate. Steel sheath charges would overlap explicit pack steel; unresolved fixed cable and insulation quantities are omitted. Rate transfer to REBCO is an assumption.
Domain: every input and output finite; n_coils, c_coil, turn_current, cost_escalation and nonplanar_factor > 0; I_coil, cost_per_kAm, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic and refuses non-finite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-13

Inputs:
    - f_set: f_set parameter
    - winding_rate_1990: winding_rate_1990 parameter
    - material_cost_in: material_cost_in parameter
    - n_coils: n_coils parameter
    - c_coil: c_coil parameter
    - turn_current: turn_current parameter
    - cost_per_kAm: cost_per_kAm parameter
    - I_coil: I_coil parameter
    - nonplanar_factor: nonplanar_factor parameter
    - cost_escalation: cost_escalation parameter

Outputs:
    - winding_fabrication_cost: winding_fabrication_cost result
    - cost: cost result
    - tape_cost: tape_cost result
    - conductor_length: conductor_length result

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42

    SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42

    Calculation Specification:
        See documentation:
Additive composite-tape procurement, non-tape material procurement and winding operations. Casing and primary structure remain separate accounts. Normative manual-completion equations: K = n_coils * I_coil * f_set * c_coil / 1000 [kA m]; tape_cost = K * cost_per_kAm; conductor_length = 1000 * K / turn_current [m]; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Inputs: n_coils and f_set dimensionless; I_coil ampere-turns; c_coil m; cost_per_kAm dollars/(kA m); turn_current A; winding_rate_1990 dollars1990/m; escalation and nonplanar factor dimensionless; material_cost_in dollars. Outputs: costs dollars, conductor_length m of composite conductor (not tape metres). Winding operations are not a complete factory quote or a labor-only rate. Steel sheath charges would overlap explicit pack steel; unresolved fixed cable and insulation quantities are omitted. Rate transfer to REBCO is an assumption.
Domain: every input and output finite; n_coils, c_coil, turn_current, cost_escalation and nonplanar_factor > 0; I_coil, cost_per_kAm, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Typed manual completion raises ValueError naming the calculation and offending quantity before arithmetic and refuses non-finite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-13

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_procurement_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts winding_fabrication_cost, cost, tape_cost, conductor_length fields to separate channels.
    """

    name: str = "Winding_Pack_Procurement_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, f_set: float, winding_rate_1990: float, material_cost_in: float, n_coils: float, c_coil: float, turn_current: float, cost_per_kAm: float, I_coil: float, nonplanar_factor: float, cost_escalation: float    ) -> Winding_Pack_Procurement_CostInput:
        """Validate inputs and fill defaults.

        Args:
            f_set: f_set input
            winding_rate_1990: winding_rate_1990 input
            material_cost_in: material_cost_in input
            n_coils: n_coils input
            c_coil: c_coil input
            turn_current: turn_current input
            cost_per_kAm: cost_per_kAm input
            I_coil: I_coil input
            nonplanar_factor: nonplanar_factor input
            cost_escalation: cost_escalation input

        Returns:
            Validated input model
        """
        return Winding_Pack_Procurement_CostInput(f_set=f_set, winding_rate_1990=winding_rate_1990, material_cost_in=material_cost_in, n_coils=n_coils, c_coil=c_coil, turn_current=turn_current, cost_per_kAm=cost_per_kAm, I_coil=I_coil, nonplanar_factor=nonplanar_factor, cost_escalation=cost_escalation)

    def run(
        self, f_set: float, winding_rate_1990: float, material_cost_in: float, n_coils: float, c_coil: float, turn_current: float, cost_per_kAm: float, I_coil: float, nonplanar_factor: float, cost_escalation: float    ) -> ModuleResult[Winding_Pack_Procurement_CostOutput]:
        """Execute calculation.

        Args:
            f_set: f_set input
            winding_rate_1990: winding_rate_1990 input
            material_cost_in: material_cost_in input
            n_coils: n_coils input
            c_coil: c_coil input
            turn_current: turn_current input
            cost_per_kAm: cost_per_kAm input
            I_coil: I_coil input
            nonplanar_factor: nonplanar_factor input
            cost_escalation: cost_escalation input

        Returns:
            Module result with Winding_Pack_Procurement_CostOutput (winding_fabrication_cost, cost, tape_cost, conductor_length)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(f_set, winding_rate_1990, material_cost_in, n_coils, c_coil, turn_current, cost_per_kAm, I_coil, nonplanar_factor, cost_escalation)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_procurement_cost_impl import (
            run_winding_pack_procurement_cost,
        )

        # Execute implementation - returns tuple of values
        winding_fabrication_cost, cost, tape_cost, conductor_length = run_winding_pack_procurement_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Pack_Procurement_CostOutput(
                winding_fabrication_cost=winding_fabrication_cost,
                cost=cost,
                tape_cost=tape_cost,
                conductor_length=conductor_length,
            )
        )
