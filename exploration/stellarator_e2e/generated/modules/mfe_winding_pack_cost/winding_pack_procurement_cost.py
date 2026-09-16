"""Winding_Pack_Procurement_CostModule Module Wrapper

TEAx module for Winding_Pack_Procurement_Cost calculation.

Additive full-composite tape procurement, external pack materials and winding operations. Casing and primary support remain separate accounts. Normative manual equations: tape_area = tape_width * tape_thickness; tape_length = tape_volume_in / tape_area; tape_cost = tape_length * tape_price_per_m; conductor_length = n_coils * I_coil * f_set * c_coil / turn_current; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Units: tape_volume_in m^3; width and full composite thickness m; tape_price_per_m dollars per metre of that complete purchased tape; tape_length individual tape metres. I_coil ampere-turns; turn_current A; conductor_length composite-conductor metres; winding_rate_1990 dollars1990/conductor-m; other costs dollars. The existing volume input already includes field-envelope quantity scaling. Never apply another envelope factor to tape price. Tape substrate/stabilizer are included in the complete tape purchase; external copper jacket, solder, steel and helium are separate. Winding operations are an inherited transfer assumption, not a complete factory quote. Detailed insulation inclusion in the inherited winding rate is uncertain; a conditional separate sheet-stock scenario is exposed. Spares, yield and integer tape counts remain unquantified.
Domain: all inputs and outputs finite; n_coils, c_coil, turn_current, tape_width, tape_thickness, cost_escalation and nonplanar_factor > 0; I_coil, tape_volume_in, tape_price_per_m, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Computed tape_area finite and positive; positive volume requires positive tape_length; positive length and price require positive tape_cost. Typed manual completion raises calculation- and quantity-named ValueError before invalid arithmetic and refuses nonfinite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: work/active/WI-060_tape-procurement-quantity-basis/design.md (volume/cross-section identity and conditional construction); knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-15

Inputs:
    - f_set: f_set parameter
    - winding_rate_1990: winding_rate_1990 parameter
    - material_cost_in: material_cost_in parameter
    - tape_thickness: tape_thickness parameter
    - n_coils: n_coils parameter
    - tape_width: tape_width parameter
    - tape_volume_in: tape_volume_in parameter
    - tape_price_per_m: tape_price_per_m parameter
    - c_coil: c_coil parameter
    - turn_current: turn_current parameter
    - I_coil: I_coil parameter
    - nonplanar_factor: nonplanar_factor parameter
    - cost_escalation: cost_escalation parameter

Outputs:
    - winding_fabrication_cost: winding_fabrication_cost result
    - tape_length: tape_length result
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
        tape_thickness: tape_thickness input
        n_coils: n_coils input
        tape_width: tape_width input
        tape_volume_in: tape_volume_in input
        tape_price_per_m: tape_price_per_m input
        c_coil: c_coil input
        turn_current: turn_current input
        I_coil: I_coil input
        nonplanar_factor: nonplanar_factor input
        cost_escalation: cost_escalation input
    """
    f_set: float = Field(..., description="f_set input")
    winding_rate_1990: float = Field(..., description="winding_rate_1990 input")
    material_cost_in: float = Field(..., description="material_cost_in input")
    tape_thickness: float = Field(..., description="tape_thickness input")
    n_coils: float = Field(..., description="n_coils input")
    tape_width: float = Field(..., description="tape_width input")
    tape_volume_in: float = Field(..., description="tape_volume_in input")
    tape_price_per_m: float = Field(..., description="tape_price_per_m input")
    c_coil: float = Field(..., description="c_coil input")
    turn_current: float = Field(..., description="turn_current input")
    I_coil: float = Field(..., description="I_coil input")
    nonplanar_factor: float = Field(..., description="nonplanar_factor input")
    cost_escalation: float = Field(..., description="cost_escalation input")


class Winding_Pack_Procurement_CostModule(ModuleBase[Winding_Pack_Procurement_CostInput, Winding_Pack_Procurement_CostOutput]):
    """TEAx module for Winding_Pack_Procurement_Cost calculation.

Additive full-composite tape procurement, external pack materials and winding operations. Casing and primary support remain separate accounts. Normative manual equations: tape_area = tape_width * tape_thickness; tape_length = tape_volume_in / tape_area; tape_cost = tape_length * tape_price_per_m; conductor_length = n_coils * I_coil * f_set * c_coil / turn_current; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Units: tape_volume_in m^3; width and full composite thickness m; tape_price_per_m dollars per metre of that complete purchased tape; tape_length individual tape metres. I_coil ampere-turns; turn_current A; conductor_length composite-conductor metres; winding_rate_1990 dollars1990/conductor-m; other costs dollars. The existing volume input already includes field-envelope quantity scaling. Never apply another envelope factor to tape price. Tape substrate/stabilizer are included in the complete tape purchase; external copper jacket, solder, steel and helium are separate. Winding operations are an inherited transfer assumption, not a complete factory quote. Detailed insulation inclusion in the inherited winding rate is uncertain; a conditional separate sheet-stock scenario is exposed. Spares, yield and integer tape counts remain unquantified.
Domain: all inputs and outputs finite; n_coils, c_coil, turn_current, tape_width, tape_thickness, cost_escalation and nonplanar_factor > 0; I_coil, tape_volume_in, tape_price_per_m, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Computed tape_area finite and positive; positive volume requires positive tape_length; positive length and price require positive tape_cost. Typed manual completion raises calculation- and quantity-named ValueError before invalid arithmetic and refuses nonfinite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: work/active/WI-060_tape-procurement-quantity-basis/design.md (volume/cross-section identity and conditional construction); knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-15

Inputs:
    - f_set: f_set parameter
    - winding_rate_1990: winding_rate_1990 parameter
    - material_cost_in: material_cost_in parameter
    - tape_thickness: tape_thickness parameter
    - n_coils: n_coils parameter
    - tape_width: tape_width parameter
    - tape_volume_in: tape_volume_in parameter
    - tape_price_per_m: tape_price_per_m parameter
    - c_coil: c_coil parameter
    - turn_current: turn_current parameter
    - I_coil: I_coil parameter
    - nonplanar_factor: nonplanar_factor parameter
    - cost_escalation: cost_escalation parameter

Outputs:
    - winding_fabrication_cost: winding_fabrication_cost result
    - tape_length: tape_length result
    - cost: cost result
    - tape_cost: tape_cost result
    - conductor_length: conductor_length result

SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42

    SysML Source: root-0/analyses/mfe_winding_pack_cost.sysml:42

    Calculation Specification:
        See documentation:
Additive full-composite tape procurement, external pack materials and winding operations. Casing and primary support remain separate accounts. Normative manual equations: tape_area = tape_width * tape_thickness; tape_length = tape_volume_in / tape_area; tape_cost = tape_length * tape_price_per_m; conductor_length = n_coils * I_coil * f_set * c_coil / turn_current; winding_fabrication_cost = conductor_length * winding_rate_1990 * cost_escalation * nonplanar_factor; cost = tape_cost + material_cost_in + winding_fabrication_cost.
Units: tape_volume_in m^3; width and full composite thickness m; tape_price_per_m dollars per metre of that complete purchased tape; tape_length individual tape metres. I_coil ampere-turns; turn_current A; conductor_length composite-conductor metres; winding_rate_1990 dollars1990/conductor-m; other costs dollars. The existing volume input already includes field-envelope quantity scaling. Never apply another envelope factor to tape price. Tape substrate/stabilizer are included in the complete tape purchase; external copper jacket, solder, steel and helium are separate. Winding operations are an inherited transfer assumption, not a complete factory quote. Detailed insulation inclusion in the inherited winding rate is uncertain; a conditional separate sheet-stock scenario is exposed. Spares, yield and integer tape counts remain unquantified.
Domain: all inputs and outputs finite; n_coils, c_coil, turn_current, tape_width, tape_thickness, cost_escalation and nonplanar_factor > 0; I_coil, tape_volume_in, tape_price_per_m, winding_rate_1990 and material_cost_in >= 0; 0 < f_set <= 1. Computed tape_area finite and positive; positive volume requires positive tape_length; positive length and price require positive tape_cost. Typed manual completion raises calculation- and quantity-named ValueError before invalid arithmetic and refuses nonfinite results.
*Source**: knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md; knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md.
*Reference**: work/active/WI-060_tape-procurement-quantity-basis/design.md (volume/cross-section identity and conditional construction); knowledge/sources/ukaea_process_original_cost_model_superconducting_tf_coil/output.md:4307-4433 (acc2221 additive conductor/winding/casing accounts); knowledge/sources/ukaea_process_cost_variable_definitions_and_historical/output.md:2724-2731 (ucwindtf 480 dollars1990/m).
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_procurement_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts winding_fabrication_cost, tape_length, cost, tape_cost, conductor_length fields to separate channels.
    """

    name: str = "Winding_Pack_Procurement_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, f_set: float, winding_rate_1990: float, material_cost_in: float, tape_thickness: float, n_coils: float, tape_width: float, tape_volume_in: float, tape_price_per_m: float, c_coil: float, turn_current: float, I_coil: float, nonplanar_factor: float, cost_escalation: float    ) -> Winding_Pack_Procurement_CostInput:
        """Validate inputs and fill defaults.

        Args:
            f_set: f_set input
            winding_rate_1990: winding_rate_1990 input
            material_cost_in: material_cost_in input
            tape_thickness: tape_thickness input
            n_coils: n_coils input
            tape_width: tape_width input
            tape_volume_in: tape_volume_in input
            tape_price_per_m: tape_price_per_m input
            c_coil: c_coil input
            turn_current: turn_current input
            I_coil: I_coil input
            nonplanar_factor: nonplanar_factor input
            cost_escalation: cost_escalation input

        Returns:
            Validated input model
        """
        return Winding_Pack_Procurement_CostInput(f_set=f_set, winding_rate_1990=winding_rate_1990, material_cost_in=material_cost_in, tape_thickness=tape_thickness, n_coils=n_coils, tape_width=tape_width, tape_volume_in=tape_volume_in, tape_price_per_m=tape_price_per_m, c_coil=c_coil, turn_current=turn_current, I_coil=I_coil, nonplanar_factor=nonplanar_factor, cost_escalation=cost_escalation)

    def run(
        self, f_set: float, winding_rate_1990: float, material_cost_in: float, tape_thickness: float, n_coils: float, tape_width: float, tape_volume_in: float, tape_price_per_m: float, c_coil: float, turn_current: float, I_coil: float, nonplanar_factor: float, cost_escalation: float    ) -> ModuleResult[Winding_Pack_Procurement_CostOutput]:
        """Execute calculation.

        Args:
            f_set: f_set input
            winding_rate_1990: winding_rate_1990 input
            material_cost_in: material_cost_in input
            tape_thickness: tape_thickness input
            n_coils: n_coils input
            tape_width: tape_width input
            tape_volume_in: tape_volume_in input
            tape_price_per_m: tape_price_per_m input
            c_coil: c_coil input
            turn_current: turn_current input
            I_coil: I_coil input
            nonplanar_factor: nonplanar_factor input
            cost_escalation: cost_escalation input

        Returns:
            Module result with Winding_Pack_Procurement_CostOutput (winding_fabrication_cost, tape_length, cost, tape_cost, conductor_length)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(f_set, winding_rate_1990, material_cost_in, tape_thickness, n_coils, tape_width, tape_volume_in, tape_price_per_m, c_coil, turn_current, I_coil, nonplanar_factor, cost_escalation)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_winding_pack_cost.winding_pack_procurement_cost_impl import (
            run_winding_pack_procurement_cost,
        )

        # Execute implementation - returns tuple of values
        winding_fabrication_cost, tape_length, cost, tape_cost, conductor_length = run_winding_pack_procurement_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Winding_Pack_Procurement_CostOutput(
                winding_fabrication_cost=winding_fabrication_cost,
                tape_length=tape_length,
                cost=cost,
                tape_cost=tape_cost,
                conductor_length=conductor_length,
            )
        )
