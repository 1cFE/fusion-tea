"""Auto-generated implementation for Conductor_Peak_Field.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:328

SysML Expressions:
    B_peak = B_axis_in * peak_ratio_in
    
Documentation:
Peak magnetic field on the winding pack [T] from the axis-averaged field
and the coil set's peak/axis ratio (WI-030):

  B_peak = B_axis * peak_ratio

peak_ratio is a coil-geometry fact bound per instance (Stellaris:
24.9 T peak on the conductor at 9.0 T axis-averaged, Table 2 image);
it is the quantity a conductor ceiling ('Conductor Peak Field Limit')
is compared against. Kept as a calc, not an inline plant expression,
so the product is a module-graph edge the study tooling can trace and
no plant-level derived expression is introduced.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
conductor 24.9 T); defaults.py:597-603 (MagnetProperties.b_max,
"peak field ceiling at the conductor" -- the bounded quantity)
*Basis**: peak-on-winding = axis field x coil-set ratio; MFE-generic
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.conductor_peak_field import Conductor_Peak_FieldInput


def run_conductor_peak_field(inputs: Conductor_Peak_FieldInput) -> float:
    """Execute Conductor_Peak_Field calculation.

Peak magnetic field on the winding pack [T] from the axis-averaged field
and the coil set's peak/axis ratio (WI-030):

  B_peak = B_axis * peak_ratio

peak_ratio is a coil-geometry fact bound per instance (Stellaris:
24.9 T peak on the conductor at 9.0 T axis-averaged, Table 2 image);
it is the quantity a conductor ceiling ('Conductor Peak Field Limit')
is compared against. Kept as a calc, not an inline plant expression,
so the product is a module-graph edge the study tooling can trace and
no plant-level derived expression is introduced.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
conductor 24.9 T); defaults.py:597-603 (MagnetProperties.b_max,
"peak field ceiling at the conductor" -- the bounded quantity)
*Basis**: peak-on-winding = axis field x coil-set ratio; MFE-generic

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:328

SysML Expressions:
    B_peak = B_axis_in * peak_ratio_in
    
Documentation:
Peak magnetic field on the winding pack [T] from the axis-averaged field
and the coil set's peak/axis ratio (WI-030):

  B_peak = B_axis * peak_ratio

peak_ratio is a coil-geometry fact bound per instance (Stellaris:
24.9 T peak on the conductor at 9.0 T axis-averaged, Table 2 image);
it is the quantity a conductor ceiling ('Conductor Peak Field Limit')
is compared against. Kept as a calc, not an inline plant expression,
so the product is a module-graph edge the study tooling can trace and
no plant-level derived expression is introduced.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
/home/reid/1cfe/1costingfe/src/costingfe/defaults.py (pin 0254385)
*Ref**: images/page_002_table_0.png (Table 2: axis av. 9.0 T, peak
conductor 24.9 T); defaults.py:597-603 (MagnetProperties.b_max,
"peak field ceiling at the conductor" -- the bounded quantity)
*Basis**: peak-on-winding = axis field x coil-set ratio; MFE-generic

Args:
    inputs: Input parameters validated against Conductor_Peak_FieldInput schema

Returns:
    float: B_peak

Example:
    >>> inputs = Conductor_Peak_FieldInput(...)
    >>> result = run_conductor_peak_field(inputs)
    """
    return (inputs.B_axis_in * inputs.peak_ratio_in)
