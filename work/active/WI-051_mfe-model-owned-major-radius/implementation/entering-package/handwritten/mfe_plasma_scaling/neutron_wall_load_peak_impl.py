"""Auto-generated implementation for Neutron_Wall_Load_Peak.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:326

SysML Expressions:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.neutron_wall_load_peak import Neutron_Wall_Load_PeakInput


def run_neutron_wall_load_peak(inputs: Neutron_Wall_Load_PeakInput) -> float:
    """Execute Neutron_Wall_Load_Peak calculation.

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

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:326

SysML Expressions:
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

Args:
    inputs: Input parameters validated against Neutron_Wall_Load_PeakInput schema

Returns:
    float: wall_load_peak

Example:
    >>> inputs = Neutron_Wall_Load_PeakInput(...)
    >>> result = run_neutron_wall_load_peak(inputs)
    """
    return (inputs.wall_load * inputs.calibration_in)
