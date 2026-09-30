"""REBCO_Conductor_CurrentModule Module Wrapper

TEAx module for REBCO_Conductor_Current calculation.

Conditional 20 K perpendicular-field REBCO current estimate. Reference current is A per 4 mm width at 20 T; full composite thickness fixed 56 micrometres. Width transfer is linear from 4 to 6 mm. Ic_tape=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor. Exponent 0.6 is independently source-based, not the selected-envelope sizing exponent. N_set=tape_length/conductor_length; N_ref=N_set*f_set/f_wp_vol. Critical currents=N*Ic_tape*cabling_factor*degradation_factor*sharing_factor; operating fractions=turn_current/critical_current. allowable_current=allowable_fraction*critical_current_reference; margin_fraction=allowable_fraction-operating_fraction_reference; margin_current=allowable_current-turn_current. All currents A; lengths m; temperature K; field T; fractions dimensionless. Series turns cancel in length ratios. Reference-conductor estimate is not a worst-coil or weakest-tape guarantee.
Typed manual completion enforces finite positive inputs and positive arithmetic, 20 K, 56e-6 m thickness, width 0.004..0.006 m, 20..32 T, retention factors and allowance in (0,1], switch exactly 0/1. Above 24 T requires switch 1 and emits field_extrapolated=1; 32 T is an engineering cutoff, not measurement authority. Refuse overflow/underflow. Finite negative margins are valid failures; exact zero passes. Material/orientation are positive assumed multipliers; retention factors act once on capacity, allowance only on allowable current/margins.
Nominal 200 A is a rounded manufacturing inference from 175 A times 1.13, not a measured 56 micrometre product guarantee. 20..24 T is an approximate empirical prediction; construction/criterion transfer and ideal sharing remain unqualified. No temperature law or local angle/strain model is implied.
Gate (WI-100 design section 2.1): enabled selects the law. At 1 the equations, domain refusals and outputs are unchanged and evaluation_defined is 1; at 0 every output, evaluation_defined included, is 0.0, returned before any domain check; any other value is refused (WI-080 gating pattern, mfe_viability.sysml:106-118).
*Source**: work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: Molodyk et al. 2021 doi:10.1038/s41598-021-81559-z pp.4,5,7 Fig.4; WI-062 design.md and source-design-review.md.
*Last Updated**: 2026-09-15

Inputs:
    - degradation_factor: degradation_factor parameter
    - conductor_length: conductor_length parameter
    - tape_length: tape_length parameter
    - reference_tape_current: reference_tape_current parameter
    - tape_width: tape_width parameter
    - allow_field_extrapolation: allow_field_extrapolation parameter
    - orientation_factor: orientation_factor parameter
    - allowable_fraction: allowable_fraction parameter
    - turn_current: turn_current parameter
    - material_factor: material_factor parameter
    - sharing_factor: sharing_factor parameter
    - f_set: f_set parameter
    - temperature: temperature parameter
    - tape_thickness: tape_thickness parameter
    - B_peak: B_peak parameter
    - cabling_factor: cabling_factor parameter
    - f_wp_vol: f_wp_vol parameter
    - enabled: enabled parameter

Outputs:
    - critical_current_reference: critical_current_reference result
    - critical_current_set: critical_current_set result
    - parallel_tapes_reference: parallel_tapes_reference result
    - operating_fraction_set: operating_fraction_set result
    - parallel_tapes_set: parallel_tapes_set result
    - field_extrapolated: field_extrapolated result
    - margin_fraction: margin_fraction result
    - tape_critical_current: tape_critical_current result
    - allowable_current: allowable_current result
    - margin_current: margin_current result
    - operating_fraction_reference: operating_fraction_reference result
    - evaluation_defined: evaluation_defined result

SysML Source: root-0/analyses/mfe_conductor_current.sysml:3

SysML Source: root-0/analyses/mfe_conductor_current.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_conductor_current/rebco_conductor_current_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.rebco_conductor_current_output import REBCO_Conductor_CurrentOutput


class REBCO_Conductor_CurrentInput(BaseModel):
    """Input model for REBCO_Conductor_CurrentModule.

    Attributes:
        degradation_factor: degradation_factor input
        conductor_length: conductor_length input
        tape_length: tape_length input
        reference_tape_current: reference_tape_current input
        tape_width: tape_width input
        allow_field_extrapolation: allow_field_extrapolation input
        orientation_factor: orientation_factor input
        allowable_fraction: allowable_fraction input
        turn_current: turn_current input
        material_factor: material_factor input
        sharing_factor: sharing_factor input
        f_set: f_set input
        temperature: temperature input
        tape_thickness: tape_thickness input
        B_peak: B_peak input
        cabling_factor: cabling_factor input
        f_wp_vol: f_wp_vol input
        enabled: enabled input
    """
    degradation_factor: float = Field(..., description="degradation_factor input")
    conductor_length: float = Field(..., description="conductor_length input")
    tape_length: float = Field(..., description="tape_length input")
    reference_tape_current: float = Field(..., description="reference_tape_current input")
    tape_width: float = Field(..., description="tape_width input")
    allow_field_extrapolation: float = Field(..., description="allow_field_extrapolation input")
    orientation_factor: float = Field(..., description="orientation_factor input")
    allowable_fraction: float = Field(..., description="allowable_fraction input")
    turn_current: float = Field(..., description="turn_current input")
    material_factor: float = Field(..., description="material_factor input")
    sharing_factor: float = Field(..., description="sharing_factor input")
    f_set: float = Field(..., description="f_set input")
    temperature: float = Field(..., description="temperature input")
    tape_thickness: float = Field(..., description="tape_thickness input")
    B_peak: float = Field(..., description="B_peak input")
    cabling_factor: float = Field(..., description="cabling_factor input")
    f_wp_vol: float = Field(..., description="f_wp_vol input")
    enabled: float = Field(..., description="enabled input")


class REBCO_Conductor_CurrentModule(ModuleBase[REBCO_Conductor_CurrentInput, REBCO_Conductor_CurrentOutput]):
    """TEAx module for REBCO_Conductor_Current calculation.

Conditional 20 K perpendicular-field REBCO current estimate. Reference current is A per 4 mm width at 20 T; full composite thickness fixed 56 micrometres. Width transfer is linear from 4 to 6 mm. Ic_tape=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor. Exponent 0.6 is independently source-based, not the selected-envelope sizing exponent. N_set=tape_length/conductor_length; N_ref=N_set*f_set/f_wp_vol. Critical currents=N*Ic_tape*cabling_factor*degradation_factor*sharing_factor; operating fractions=turn_current/critical_current. allowable_current=allowable_fraction*critical_current_reference; margin_fraction=allowable_fraction-operating_fraction_reference; margin_current=allowable_current-turn_current. All currents A; lengths m; temperature K; field T; fractions dimensionless. Series turns cancel in length ratios. Reference-conductor estimate is not a worst-coil or weakest-tape guarantee.
Typed manual completion enforces finite positive inputs and positive arithmetic, 20 K, 56e-6 m thickness, width 0.004..0.006 m, 20..32 T, retention factors and allowance in (0,1], switch exactly 0/1. Above 24 T requires switch 1 and emits field_extrapolated=1; 32 T is an engineering cutoff, not measurement authority. Refuse overflow/underflow. Finite negative margins are valid failures; exact zero passes. Material/orientation are positive assumed multipliers; retention factors act once on capacity, allowance only on allowable current/margins.
Nominal 200 A is a rounded manufacturing inference from 175 A times 1.13, not a measured 56 micrometre product guarantee. 20..24 T is an approximate empirical prediction; construction/criterion transfer and ideal sharing remain unqualified. No temperature law or local angle/strain model is implied.
Gate (WI-100 design section 2.1): enabled selects the law. At 1 the equations, domain refusals and outputs are unchanged and evaluation_defined is 1; at 0 every output, evaluation_defined included, is 0.0, returned before any domain check; any other value is refused (WI-080 gating pattern, mfe_viability.sysml:106-118).
*Source**: work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: Molodyk et al. 2021 doi:10.1038/s41598-021-81559-z pp.4,5,7 Fig.4; WI-062 design.md and source-design-review.md.
*Last Updated**: 2026-09-15

Inputs:
    - degradation_factor: degradation_factor parameter
    - conductor_length: conductor_length parameter
    - tape_length: tape_length parameter
    - reference_tape_current: reference_tape_current parameter
    - tape_width: tape_width parameter
    - allow_field_extrapolation: allow_field_extrapolation parameter
    - orientation_factor: orientation_factor parameter
    - allowable_fraction: allowable_fraction parameter
    - turn_current: turn_current parameter
    - material_factor: material_factor parameter
    - sharing_factor: sharing_factor parameter
    - f_set: f_set parameter
    - temperature: temperature parameter
    - tape_thickness: tape_thickness parameter
    - B_peak: B_peak parameter
    - cabling_factor: cabling_factor parameter
    - f_wp_vol: f_wp_vol parameter
    - enabled: enabled parameter

Outputs:
    - critical_current_reference: critical_current_reference result
    - critical_current_set: critical_current_set result
    - parallel_tapes_reference: parallel_tapes_reference result
    - operating_fraction_set: operating_fraction_set result
    - parallel_tapes_set: parallel_tapes_set result
    - field_extrapolated: field_extrapolated result
    - margin_fraction: margin_fraction result
    - tape_critical_current: tape_critical_current result
    - allowable_current: allowable_current result
    - margin_current: margin_current result
    - operating_fraction_reference: operating_fraction_reference result
    - evaluation_defined: evaluation_defined result

SysML Source: root-0/analyses/mfe_conductor_current.sysml:3

    SysML Source: root-0/analyses/mfe_conductor_current.sysml:3

    Calculation Specification:
        enabled = 1.0
        
Documentation:
Conditional 20 K perpendicular-field REBCO current estimate. Reference current is A per 4 mm width at 20 T; full composite thickness fixed 56 micrometres. Width transfer is linear from 4 to 6 mm. Ic_tape=reference_tape_current*(tape_width/0.004)*(B_peak/20)^(-0.6)*material_factor*orientation_factor. Exponent 0.6 is independently source-based, not the selected-envelope sizing exponent. N_set=tape_length/conductor_length; N_ref=N_set*f_set/f_wp_vol. Critical currents=N*Ic_tape*cabling_factor*degradation_factor*sharing_factor; operating fractions=turn_current/critical_current. allowable_current=allowable_fraction*critical_current_reference; margin_fraction=allowable_fraction-operating_fraction_reference; margin_current=allowable_current-turn_current. All currents A; lengths m; temperature K; field T; fractions dimensionless. Series turns cancel in length ratios. Reference-conductor estimate is not a worst-coil or weakest-tape guarantee.
Typed manual completion enforces finite positive inputs and positive arithmetic, 20 K, 56e-6 m thickness, width 0.004..0.006 m, 20..32 T, retention factors and allowance in (0,1], switch exactly 0/1. Above 24 T requires switch 1 and emits field_extrapolated=1; 32 T is an engineering cutoff, not measurement authority. Refuse overflow/underflow. Finite negative margins are valid failures; exact zero passes. Material/orientation are positive assumed multipliers; retention factors act once on capacity, allowance only on allowable current/margins.
Nominal 200 A is a rounded manufacturing inference from 175 A times 1.13, not a measured 56 micrometre product guarantee. 20..24 T is an approximate empirical prediction; construction/criterion transfer and ideal sharing remain unqualified. No temperature law or local angle/strain model is implied.
Gate (WI-100 design section 2.1): enabled selects the law. At 1 the equations, domain refusals and outputs are unchanged and evaluation_defined is 1; at 0 every output, evaluation_defined included, is 0.0, returned before any domain check; any other value is refused (WI-080 gating pattern, mfe_viability.sysml:106-118).
*Source**: work/orchestration/goals/absolute-conductor-current-margin/evidence/performance-research.md
*Reference**: Molodyk et al. 2021 doi:10.1038/s41598-021-81559-z pp.4,5,7 Fig.4; WI-062 design.md and source-design-review.md.
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_conductor_current.rebco_conductor_current_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts critical_current_reference, critical_current_set, parallel_tapes_reference, operating_fraction_set, parallel_tapes_set, field_extrapolated, margin_fraction, tape_critical_current, allowable_current, margin_current, operating_fraction_reference, evaluation_defined fields to separate channels.
    """

    name: str = "REBCO_Conductor_CurrentModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, degradation_factor: float, conductor_length: float, tape_length: float, reference_tape_current: float, tape_width: float, allow_field_extrapolation: float, orientation_factor: float, allowable_fraction: float, turn_current: float, material_factor: float, sharing_factor: float, f_set: float, temperature: float, tape_thickness: float, B_peak: float, cabling_factor: float, f_wp_vol: float, enabled: float    ) -> REBCO_Conductor_CurrentInput:
        """Validate inputs and fill defaults.

        Args:
            degradation_factor: degradation_factor input
            conductor_length: conductor_length input
            tape_length: tape_length input
            reference_tape_current: reference_tape_current input
            tape_width: tape_width input
            allow_field_extrapolation: allow_field_extrapolation input
            orientation_factor: orientation_factor input
            allowable_fraction: allowable_fraction input
            turn_current: turn_current input
            material_factor: material_factor input
            sharing_factor: sharing_factor input
            f_set: f_set input
            temperature: temperature input
            tape_thickness: tape_thickness input
            B_peak: B_peak input
            cabling_factor: cabling_factor input
            f_wp_vol: f_wp_vol input
            enabled: enabled input

        Returns:
            Validated input model
        """
        return REBCO_Conductor_CurrentInput(degradation_factor=degradation_factor, conductor_length=conductor_length, tape_length=tape_length, reference_tape_current=reference_tape_current, tape_width=tape_width, allow_field_extrapolation=allow_field_extrapolation, orientation_factor=orientation_factor, allowable_fraction=allowable_fraction, turn_current=turn_current, material_factor=material_factor, sharing_factor=sharing_factor, f_set=f_set, temperature=temperature, tape_thickness=tape_thickness, B_peak=B_peak, cabling_factor=cabling_factor, f_wp_vol=f_wp_vol, enabled=enabled)

    def run(
        self, degradation_factor: float, conductor_length: float, tape_length: float, reference_tape_current: float, tape_width: float, allow_field_extrapolation: float, orientation_factor: float, allowable_fraction: float, turn_current: float, material_factor: float, sharing_factor: float, f_set: float, temperature: float, tape_thickness: float, B_peak: float, cabling_factor: float, f_wp_vol: float, enabled: float    ) -> ModuleResult[REBCO_Conductor_CurrentOutput]:
        """Execute calculation.

        Args:
            degradation_factor: degradation_factor input
            conductor_length: conductor_length input
            tape_length: tape_length input
            reference_tape_current: reference_tape_current input
            tape_width: tape_width input
            allow_field_extrapolation: allow_field_extrapolation input
            orientation_factor: orientation_factor input
            allowable_fraction: allowable_fraction input
            turn_current: turn_current input
            material_factor: material_factor input
            sharing_factor: sharing_factor input
            f_set: f_set input
            temperature: temperature input
            tape_thickness: tape_thickness input
            B_peak: B_peak input
            cabling_factor: cabling_factor input
            f_wp_vol: f_wp_vol input
            enabled: enabled input

        Returns:
            Module result with REBCO_Conductor_CurrentOutput (critical_current_reference, critical_current_set, parallel_tapes_reference, operating_fraction_set, parallel_tapes_set, field_extrapolated, margin_fraction, tape_critical_current, allowable_current, margin_current, operating_fraction_reference, evaluation_defined)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(degradation_factor, conductor_length, tape_length, reference_tape_current, tape_width, allow_field_extrapolation, orientation_factor, allowable_fraction, turn_current, material_factor, sharing_factor, f_set, temperature, tape_thickness, B_peak, cabling_factor, f_wp_vol, enabled)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_conductor_current.rebco_conductor_current_impl import (
            run_rebco_conductor_current,
        )

        # Execute implementation - returns tuple of values
        critical_current_reference, critical_current_set, parallel_tapes_reference, operating_fraction_set, parallel_tapes_set, field_extrapolated, margin_fraction, tape_critical_current, allowable_current, margin_current, operating_fraction_reference, evaluation_defined = run_rebco_conductor_current(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=REBCO_Conductor_CurrentOutput(
                critical_current_reference=critical_current_reference,
                critical_current_set=critical_current_set,
                parallel_tapes_reference=parallel_tapes_reference,
                operating_fraction_set=operating_fraction_set,
                parallel_tapes_set=parallel_tapes_set,
                field_extrapolated=field_extrapolated,
                margin_fraction=margin_fraction,
                tape_critical_current=tape_critical_current,
                allowable_current=allowable_current,
                margin_current=margin_current,
                operating_fraction_reference=operating_fraction_reference,
                evaluation_defined=evaluation_defined,
            )
        )
