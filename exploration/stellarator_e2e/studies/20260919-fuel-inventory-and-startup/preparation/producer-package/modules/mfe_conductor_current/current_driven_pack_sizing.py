"""Current_Driven_Pack_SizingModule Module Wrapper

TEAx module for Current_Driven_Pack_Sizing calculation.

Optional continuous reference-conductor inventory sizing, using the unchanged WI-062 conditional performance law: Ia=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor*cabling_factor*degradation_factor*sharing_factor [A]. At=tape_width*tape_thickness [m^2]; ft=1-f_copper-f_solder-f_steel-f_helium. Nreq=turn_current/(allowable_fraction*Ia); Acond=Nreq*At/ft [m^2]; Apack=(I_coil/turn_current)*Acond [m^2]; jreq=I_coil/(Apack*1e6) [A/mm^2]. Mode0 selects legacy_effective_density exactly; mode1 selects jreq/inventory_multiplier. Multiplier >=1 adds physical inventory without changing acceptance. Mode is exactly0/1. All positive inputs/intermediates finite and positive, non-tape fractions nonnegative, ft in(0,1]. Retention/allowance in(0,1]. Same 20 K, 56 micrometre composite, 4..6 mm, 20..32 T domain; above24 T requires extrapolation permission. Refuse arithmetic overflow/underflow. Actual independent allocation determines peak field first; no geometry feedback. Continuous counts and conditional material transfer do not qualify a manufactured winding. Legacy grade diagnostics remain unchanged.
*Source**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/source-design-review.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Last Updated**: 2026-09-15

Inputs:
    - inventory_multiplier: inventory_multiplier parameter
    - legacy_effective_density: legacy_effective_density parameter
    - I_coil: I_coil parameter
    - sizing_mode: sizing_mode parameter
    - f_solder: f_solder parameter
    - allowable_fraction: allowable_fraction parameter
    - turn_current: turn_current parameter
    - sharing_factor: sharing_factor parameter
    - tape_width: tape_width parameter
    - allow_field_extrapolation: allow_field_extrapolation parameter
    - temperature: temperature parameter
    - B_peak: B_peak parameter
    - f_copper: f_copper parameter
    - reference_tape_current: reference_tape_current parameter
    - material_factor: material_factor parameter
    - cabling_factor: cabling_factor parameter
    - orientation_factor: orientation_factor parameter
    - tape_thickness: tape_thickness parameter
    - f_steel: f_steel parameter
    - degradation_factor: degradation_factor parameter
    - f_helium: f_helium parameter

Outputs:
    - required_tapes: required_tapes result
    - required_conductor_area: required_conductor_area result
    - required_pack_area: required_pack_area result
    - required_effective_density: required_effective_density result
    - selected_effective_density: selected_effective_density result
    - tape_available_current: tape_available_current result

SysML Source: root-0/analyses/mfe_conductor_current.sysml:39

SysML Source: root-0/analyses/mfe_conductor_current.sysml:39

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_conductor_current/current_driven_pack_sizing_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.current_driven_pack_sizing_output import Current_Driven_Pack_SizingOutput


class Current_Driven_Pack_SizingInput(BaseModel):
    """Input model for Current_Driven_Pack_SizingModule.

    Attributes:
        inventory_multiplier: inventory_multiplier input
        legacy_effective_density: legacy_effective_density input
        I_coil: I_coil input
        sizing_mode: sizing_mode input
        f_solder: f_solder input
        allowable_fraction: allowable_fraction input
        turn_current: turn_current input
        sharing_factor: sharing_factor input
        tape_width: tape_width input
        allow_field_extrapolation: allow_field_extrapolation input
        temperature: temperature input
        B_peak: B_peak input
        f_copper: f_copper input
        reference_tape_current: reference_tape_current input
        material_factor: material_factor input
        cabling_factor: cabling_factor input
        orientation_factor: orientation_factor input
        tape_thickness: tape_thickness input
        f_steel: f_steel input
        degradation_factor: degradation_factor input
        f_helium: f_helium input
    """
    inventory_multiplier: float = Field(..., description="inventory_multiplier input")
    legacy_effective_density: float = Field(..., description="legacy_effective_density input")
    I_coil: float = Field(..., description="I_coil input")
    sizing_mode: float = Field(..., description="sizing_mode input")
    f_solder: float = Field(..., description="f_solder input")
    allowable_fraction: float = Field(..., description="allowable_fraction input")
    turn_current: float = Field(..., description="turn_current input")
    sharing_factor: float = Field(..., description="sharing_factor input")
    tape_width: float = Field(..., description="tape_width input")
    allow_field_extrapolation: float = Field(..., description="allow_field_extrapolation input")
    temperature: float = Field(..., description="temperature input")
    B_peak: float = Field(..., description="B_peak input")
    f_copper: float = Field(..., description="f_copper input")
    reference_tape_current: float = Field(..., description="reference_tape_current input")
    material_factor: float = Field(..., description="material_factor input")
    cabling_factor: float = Field(..., description="cabling_factor input")
    orientation_factor: float = Field(..., description="orientation_factor input")
    tape_thickness: float = Field(..., description="tape_thickness input")
    f_steel: float = Field(..., description="f_steel input")
    degradation_factor: float = Field(..., description="degradation_factor input")
    f_helium: float = Field(..., description="f_helium input")


class Current_Driven_Pack_SizingModule(ModuleBase[Current_Driven_Pack_SizingInput, Current_Driven_Pack_SizingOutput]):
    """TEAx module for Current_Driven_Pack_Sizing calculation.

Optional continuous reference-conductor inventory sizing, using the unchanged WI-062 conditional performance law: Ia=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor*cabling_factor*degradation_factor*sharing_factor [A]. At=tape_width*tape_thickness [m^2]; ft=1-f_copper-f_solder-f_steel-f_helium. Nreq=turn_current/(allowable_fraction*Ia); Acond=Nreq*At/ft [m^2]; Apack=(I_coil/turn_current)*Acond [m^2]; jreq=I_coil/(Apack*1e6) [A/mm^2]. Mode0 selects legacy_effective_density exactly; mode1 selects jreq/inventory_multiplier. Multiplier >=1 adds physical inventory without changing acceptance. Mode is exactly0/1. All positive inputs/intermediates finite and positive, non-tape fractions nonnegative, ft in(0,1]. Retention/allowance in(0,1]. Same 20 K, 56 micrometre composite, 4..6 mm, 20..32 T domain; above24 T requires extrapolation permission. Refuse arithmetic overflow/underflow. Actual independent allocation determines peak field first; no geometry feedback. Continuous counts and conditional material transfer do not qualify a manufactured winding. Legacy grade diagnostics remain unchanged.
*Source**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/source-design-review.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Last Updated**: 2026-09-15

Inputs:
    - inventory_multiplier: inventory_multiplier parameter
    - legacy_effective_density: legacy_effective_density parameter
    - I_coil: I_coil parameter
    - sizing_mode: sizing_mode parameter
    - f_solder: f_solder parameter
    - allowable_fraction: allowable_fraction parameter
    - turn_current: turn_current parameter
    - sharing_factor: sharing_factor parameter
    - tape_width: tape_width parameter
    - allow_field_extrapolation: allow_field_extrapolation parameter
    - temperature: temperature parameter
    - B_peak: B_peak parameter
    - f_copper: f_copper parameter
    - reference_tape_current: reference_tape_current parameter
    - material_factor: material_factor parameter
    - cabling_factor: cabling_factor parameter
    - orientation_factor: orientation_factor parameter
    - tape_thickness: tape_thickness parameter
    - f_steel: f_steel parameter
    - degradation_factor: degradation_factor parameter
    - f_helium: f_helium parameter

Outputs:
    - required_tapes: required_tapes result
    - required_conductor_area: required_conductor_area result
    - required_pack_area: required_pack_area result
    - required_effective_density: required_effective_density result
    - selected_effective_density: selected_effective_density result
    - tape_available_current: tape_available_current result

SysML Source: root-0/analyses/mfe_conductor_current.sysml:39

    SysML Source: root-0/analyses/mfe_conductor_current.sysml:39

    Calculation Specification:
        See documentation:
Optional continuous reference-conductor inventory sizing, using the unchanged WI-062 conditional performance law: Ia=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor*cabling_factor*degradation_factor*sharing_factor [A]. At=tape_width*tape_thickness [m^2]; ft=1-f_copper-f_solder-f_steel-f_helium. Nreq=turn_current/(allowable_fraction*Ia); Acond=Nreq*At/ft [m^2]; Apack=(I_coil/turn_current)*Acond [m^2]; jreq=I_coil/(Apack*1e6) [A/mm^2]. Mode0 selects legacy_effective_density exactly; mode1 selects jreq/inventory_multiplier. Multiplier >=1 adds physical inventory without changing acceptance. Mode is exactly0/1. All positive inputs/intermediates finite and positive, non-tape fractions nonnegative, ft in(0,1]. Retention/allowance in(0,1]. Same 20 K, 56 micrometre composite, 4..6 mm, 20..32 T domain; above24 T requires extrapolation permission. Refuse arithmetic overflow/underflow. Actual independent allocation determines peak field first; no geometry feedback. Continuous counts and conditional material transfer do not qualify a manufactured winding. Legacy grade diagnostics remain unchanged.
*Source**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: work/active/WI-064_current-driven-magnet-inventory-sizing/spec.md; work/orchestration/goals/joint-magnet-sizing-feasibility/evidence/source-design-review.md; work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_conductor_current.current_driven_pack_sizing_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts required_tapes, required_conductor_area, required_pack_area, required_effective_density, selected_effective_density, tape_available_current fields to separate channels.
    """

    name: str = "Current_Driven_Pack_SizingModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, inventory_multiplier: float, legacy_effective_density: float, I_coil: float, sizing_mode: float, f_solder: float, allowable_fraction: float, turn_current: float, sharing_factor: float, tape_width: float, allow_field_extrapolation: float, temperature: float, B_peak: float, f_copper: float, reference_tape_current: float, material_factor: float, cabling_factor: float, orientation_factor: float, tape_thickness: float, f_steel: float, degradation_factor: float, f_helium: float    ) -> Current_Driven_Pack_SizingInput:
        """Validate inputs and fill defaults.

        Args:
            inventory_multiplier: inventory_multiplier input
            legacy_effective_density: legacy_effective_density input
            I_coil: I_coil input
            sizing_mode: sizing_mode input
            f_solder: f_solder input
            allowable_fraction: allowable_fraction input
            turn_current: turn_current input
            sharing_factor: sharing_factor input
            tape_width: tape_width input
            allow_field_extrapolation: allow_field_extrapolation input
            temperature: temperature input
            B_peak: B_peak input
            f_copper: f_copper input
            reference_tape_current: reference_tape_current input
            material_factor: material_factor input
            cabling_factor: cabling_factor input
            orientation_factor: orientation_factor input
            tape_thickness: tape_thickness input
            f_steel: f_steel input
            degradation_factor: degradation_factor input
            f_helium: f_helium input

        Returns:
            Validated input model
        """
        return Current_Driven_Pack_SizingInput(inventory_multiplier=inventory_multiplier, legacy_effective_density=legacy_effective_density, I_coil=I_coil, sizing_mode=sizing_mode, f_solder=f_solder, allowable_fraction=allowable_fraction, turn_current=turn_current, sharing_factor=sharing_factor, tape_width=tape_width, allow_field_extrapolation=allow_field_extrapolation, temperature=temperature, B_peak=B_peak, f_copper=f_copper, reference_tape_current=reference_tape_current, material_factor=material_factor, cabling_factor=cabling_factor, orientation_factor=orientation_factor, tape_thickness=tape_thickness, f_steel=f_steel, degradation_factor=degradation_factor, f_helium=f_helium)

    def run(
        self, inventory_multiplier: float, legacy_effective_density: float, I_coil: float, sizing_mode: float, f_solder: float, allowable_fraction: float, turn_current: float, sharing_factor: float, tape_width: float, allow_field_extrapolation: float, temperature: float, B_peak: float, f_copper: float, reference_tape_current: float, material_factor: float, cabling_factor: float, orientation_factor: float, tape_thickness: float, f_steel: float, degradation_factor: float, f_helium: float    ) -> ModuleResult[Current_Driven_Pack_SizingOutput]:
        """Execute calculation.

        Args:
            inventory_multiplier: inventory_multiplier input
            legacy_effective_density: legacy_effective_density input
            I_coil: I_coil input
            sizing_mode: sizing_mode input
            f_solder: f_solder input
            allowable_fraction: allowable_fraction input
            turn_current: turn_current input
            sharing_factor: sharing_factor input
            tape_width: tape_width input
            allow_field_extrapolation: allow_field_extrapolation input
            temperature: temperature input
            B_peak: B_peak input
            f_copper: f_copper input
            reference_tape_current: reference_tape_current input
            material_factor: material_factor input
            cabling_factor: cabling_factor input
            orientation_factor: orientation_factor input
            tape_thickness: tape_thickness input
            f_steel: f_steel input
            degradation_factor: degradation_factor input
            f_helium: f_helium input

        Returns:
            Module result with Current_Driven_Pack_SizingOutput (required_tapes, required_conductor_area, required_pack_area, required_effective_density, selected_effective_density, tape_available_current)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(inventory_multiplier, legacy_effective_density, I_coil, sizing_mode, f_solder, allowable_fraction, turn_current, sharing_factor, tape_width, allow_field_extrapolation, temperature, B_peak, f_copper, reference_tape_current, material_factor, cabling_factor, orientation_factor, tape_thickness, f_steel, degradation_factor, f_helium)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_conductor_current.current_driven_pack_sizing_impl import (
            run_current_driven_pack_sizing,
        )

        # Execute implementation - returns tuple of values
        required_tapes, required_conductor_area, required_pack_area, required_effective_density, selected_effective_density, tape_available_current = run_current_driven_pack_sizing(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Current_Driven_Pack_SizingOutput(
                required_tapes=required_tapes,
                required_conductor_area=required_conductor_area,
                required_pack_area=required_pack_area,
                required_effective_density=required_effective_density,
                selected_effective_density=selected_effective_density,
                tape_available_current=tape_available_current,
            )
        )
