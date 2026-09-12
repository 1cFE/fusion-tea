"""Auto-generated implementation for Coil_Set_Axis_Field.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

SysML Expressions:
    mu0 = 1.25663706212e-06
    two_pi = 6.283185307179586
    B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)
    
Documentation:
Axis-averaged on-axis field [T] from the coil set's current and
geometry (WI-035, inversion ruling 2026-08-30):

  B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)

k_link is a held coil-set transfer fact (float64 of the printed set),
bundling two printed facts: the per-coil current distribution
(set mean / peak = 643.2/739.2 = 0.870, Table 8 image) and the
axis-linkage of the total (571.5/643.2 = 0.888) -- the modular-coil
shaping current that does not link the magnetic axis (WI-032:
Ampere's law on axis is a lower bound for modular QI coils). At the
Stellaris design set (48 coils, 15.4 MA, R0 12.7 m) the computed
B_axis is 9.0 T minus one ulp; no float64 k_link reproduces 9.0
exactly (+/-6-ulp search), and the low side is bound deliberately so
the conductor-ceiling verdict cannot flip on rounding.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
work/completed/20260827_WI-032_cold-volume-basis/spec.md
*Ref**: images/page_002_table_0.png (Table 2: axis av. field 9.0 T,
peak coil current 15.4 MA, 48 coils, R 12.7 m);
images/page_022_table_0.png (Table 8: per-coil ampere-turns);
WI-032 spec sec. "What G is" (the linkage decomposition)
*Basis**: Ampere's law on the axis with a held, sourced coil-set
linkage fact; concept-agnostic (MR-3) -- all values bound by instances
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_field.coil_set_axis_field import Coil_Set_Axis_FieldInput


def run_coil_set_axis_field(inputs: Coil_Set_Axis_FieldInput) -> float:
    """Execute Coil_Set_Axis_Field calculation.

Axis-averaged on-axis field [T] from the coil set's current and
geometry (WI-035, inversion ruling 2026-08-30):

  B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)

k_link is a held coil-set transfer fact (float64 of the printed set),
bundling two printed facts: the per-coil current distribution
(set mean / peak = 643.2/739.2 = 0.870, Table 8 image) and the
axis-linkage of the total (571.5/643.2 = 0.888) -- the modular-coil
shaping current that does not link the magnetic axis (WI-032:
Ampere's law on axis is a lower bound for modular QI coils). At the
Stellaris design set (48 coils, 15.4 MA, R0 12.7 m) the computed
B_axis is 9.0 T minus one ulp; no float64 k_link reproduces 9.0
exactly (+/-6-ulp search), and the low side is bound deliberately so
the conductor-ceiling verdict cannot flip on rounding.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
work/completed/20260827_WI-032_cold-volume-basis/spec.md
*Ref**: images/page_002_table_0.png (Table 2: axis av. field 9.0 T,
peak coil current 15.4 MA, 48 coils, R 12.7 m);
images/page_022_table_0.png (Table 8: per-coil ampere-turns);
WI-032 spec sec. "What G is" (the linkage decomposition)
*Basis**: Ampere's law on the axis with a held, sourced coil-set
linkage fact; concept-agnostic (MR-3) -- all values bound by instances

SysML Source: root-0/analyses/mfe_magnet_field.sysml:4

SysML Expressions:
    mu0 = 1.25663706212e-06
    two_pi = 6.283185307179586
    B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)
    
Documentation:
Axis-averaged on-axis field [T] from the coil set's current and
geometry (WI-035, inversion ruling 2026-08-30):

  B_axis = mu0 * k_link * n_coils * I_coil / (two_pi * R0)

k_link is a held coil-set transfer fact (float64 of the printed set),
bundling two printed facts: the per-coil current distribution
(set mean / peak = 643.2/739.2 = 0.870, Table 8 image) and the
axis-linkage of the total (571.5/643.2 = 0.888) -- the modular-coil
shaping current that does not link the magnetic axis (WI-032:
Ampere's law on axis is a lower bound for modular QI coils). At the
Stellaris design set (48 coils, 15.4 MA, R0 12.7 m) the computed
B_axis is 9.0 T minus one ulp; no float64 k_link reproduces 9.0
exactly (+/-6-ulp search), and the low side is bound deliberately so
the conductor-ceiling verdict cannot flip on rounding.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
work/completed/20260827_WI-032_cold-volume-basis/spec.md
*Ref**: images/page_002_table_0.png (Table 2: axis av. field 9.0 T,
peak coil current 15.4 MA, 48 coils, R 12.7 m);
images/page_022_table_0.png (Table 8: per-coil ampere-turns);
WI-032 spec sec. "What G is" (the linkage decomposition)
*Basis**: Ampere's law on the axis with a held, sourced coil-set
linkage fact; concept-agnostic (MR-3) -- all values bound by instances

Args:
    inputs: Input parameters validated against Coil_Set_Axis_FieldInput schema

Returns:
    float: B_axis

Example:
    >>> inputs = Coil_Set_Axis_FieldInput(...)
    >>> result = run_coil_set_axis_field(inputs)
    """
    return ((((inputs.mu0 * inputs.k_link) * inputs.n_coils) * inputs.I_coil) / (inputs.two_pi * inputs.R0))
