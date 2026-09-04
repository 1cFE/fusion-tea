"""Neutron_Wall_Load_PeakModule Module Wrapper

TEAx module for Neutron_Wall_Load_Peak calculation.

Peak neutron wall load [MW/m^2] on the first wall (WI-041):

  wall_load_peak = wall_load * calibration

wall_load is the forward-computed circular-torus average ('Neutron
Wall Load'); calibration is the source-anchored multiplier ('Neutron
Wall Load Peak Calibration'), 1.0 for a concept with no source peak.
The peak is what a peak design limit is compared against ('Neutron
Wall Load Limit') and what sets the fluence-limited in-vessel
lifetime ('Levelized Replacement Cost'): the source and its cited
method both set lifetime by the peak load, not the average.

*Source**: knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md
*Ref**: output.md line 88 ("the lifetime of the blanket is determined by the peak loads"); line 302 (the peaking factor q_max / <q> on the first wall)
*Basis**: peak = average x source-anchored calibration; MFE-generic

Inputs:
    - wall_load: wall_load parameter
    - calibration_in: calibration_in parameter

Outputs:
    - wall_load_peak: wall_load_peak result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:326

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:326

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/neutron_wall_load_peak_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Neutron_Wall_Load_PeakInput(BaseModel):
    """Input model for Neutron_Wall_Load_PeakModule.

    Attributes:
        wall_load: wall_load input
        calibration_in: calibration_in input
    """
    wall_load: float = Field(..., description="wall_load input")
    calibration_in: float = Field(..., description="calibration_in input")


class Neutron_Wall_Load_PeakModule(ModuleBase[Neutron_Wall_Load_PeakInput, Float]):
    """TEAx module for Neutron_Wall_Load_Peak calculation.

Peak neutron wall load [MW/m^2] on the first wall (WI-041):

  wall_load_peak = wall_load * calibration

wall_load is the forward-computed circular-torus average ('Neutron
Wall Load'); calibration is the source-anchored multiplier ('Neutron
Wall Load Peak Calibration'), 1.0 for a concept with no source peak.
The peak is what a peak design limit is compared against ('Neutron
Wall Load Limit') and what sets the fluence-limited in-vessel
lifetime ('Levelized Replacement Cost'): the source and its cited
method both set lifetime by the peak load, not the average.

*Source**: knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md
*Ref**: output.md line 88 ("the lifetime of the blanket is determined by the peak loads"); line 302 (the peaking factor q_max / <q> on the first wall)
*Basis**: peak = average x source-anchored calibration; MFE-generic

Inputs:
    - wall_load: wall_load parameter
    - calibration_in: calibration_in parameter

Outputs:
    - wall_load_peak: wall_load_peak result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:326

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:326

    Calculation Specification:
        wall_load_peak = wall_load * calibration_in
        
Documentation:
Peak neutron wall load [MW/m^2] on the first wall (WI-041):

  wall_load_peak = wall_load * calibration

wall_load is the forward-computed circular-torus average ('Neutron
Wall Load'); calibration is the source-anchored multiplier ('Neutron
Wall Load Peak Calibration'), 1.0 for a concept with no source peak.
The peak is what a peak design limit is compared against ('Neutron
Wall Load Limit') and what sets the fluence-limited in-vessel
lifetime ('Levelized Replacement Cost'): the source and its cited
method both set lifetime by the peak load, not the average.

*Source**: knowledge/sources/a_deterministic_method_for_the_fast_evaluation_and_2/output.md
*Ref**: output.md line 88 ("the lifetime of the blanket is determined by the peak loads"); line 302 (the peaking factor q_max / <q> on the first wall)
*Basis**: peak = average x source-anchored calibration; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.neutron_wall_load_peak_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Neutron_Wall_Load_PeakModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, wall_load: float, calibration_in: float    ) -> Neutron_Wall_Load_PeakInput:
        """Validate inputs and fill defaults.

        Args:
            wall_load: wall_load input
            calibration_in: calibration_in input

        Returns:
            Validated input model
        """
        return Neutron_Wall_Load_PeakInput(wall_load=wall_load, calibration_in=calibration_in)

    def run(
        self, wall_load: float, calibration_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            wall_load: wall_load input
            calibration_in: calibration_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(wall_load, calibration_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.neutron_wall_load_peak_impl import (
            run_neutron_wall_load_peak,
        )

        # Execute implementation - returns single value
        wall_load_peak = run_neutron_wall_load_peak(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(wall_load_peak))
