"""Auto-generated implementation for Winding_Pack_Stress.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_field.sysml:48

SysML Expressions:
    sigma_wp = k_sigma * I_coil * B_peak_in / wp_side
    
Documentation:
Mean winding-pack stress scale [Pa] in the J x B x d form (WI-035):

  sigma_wp = k_sigma * I_coil * B_peak_in / wp_side

Force density (current x field) over the load-bearing dimension --
the standard mean-stress scale for a winding. k_sigma is a held
coil-set structural concentration fact (float64 anchored at the
printed worst-coil pair: <650 MPa at I 15.4 MA, B_peak 24.9 T,
side 0.36 m; the printed "<650" bound is taken AS the value,
conservative). The operand responds as I * B_peak / side --
quadratic in coil current once B_peak follows the derived field --
so the paired limit pushes back on both field choice and winding-pack
sizing (rubric Row 3 P3).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: "Peak stress on WP
[MPa] <650"; I, side lengths); raw.pdf sec. 2.9 structural
analysis (peak stresses ~600 MPa, axisymmetric I x B model)
*Basis**: J x B x d mean-stress scale with a held, sourced
concentration fact; concept-agnostic (MR-3)
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_field.winding_pack_stress import Winding_Pack_StressInput


def run_winding_pack_stress(inputs: Winding_Pack_StressInput) -> float:
    """Execute Winding_Pack_Stress calculation.

Mean winding-pack stress scale [Pa] in the J x B x d form (WI-035):

  sigma_wp = k_sigma * I_coil * B_peak_in / wp_side

Force density (current x field) over the load-bearing dimension --
the standard mean-stress scale for a winding. k_sigma is a held
coil-set structural concentration fact (float64 anchored at the
printed worst-coil pair: <650 MPa at I 15.4 MA, B_peak 24.9 T,
side 0.36 m; the printed "<650" bound is taken AS the value,
conservative). The operand responds as I * B_peak / side --
quadratic in coil current once B_peak follows the derived field --
so the paired limit pushes back on both field choice and winding-pack
sizing (rubric Row 3 P3).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: "Peak stress on WP
[MPa] <650"; I, side lengths); raw.pdf sec. 2.9 structural
analysis (peak stresses ~600 MPa, axisymmetric I x B model)
*Basis**: J x B x d mean-stress scale with a held, sourced
concentration fact; concept-agnostic (MR-3)

SysML Source: root-0/analyses/mfe_magnet_field.sysml:48

SysML Expressions:
    sigma_wp = k_sigma * I_coil * B_peak_in / wp_side
    
Documentation:
Mean winding-pack stress scale [Pa] in the J x B x d form (WI-035):

  sigma_wp = k_sigma * I_coil * B_peak_in / wp_side

Force density (current x field) over the load-bearing dimension --
the standard mean-stress scale for a winding. k_sigma is a held
coil-set structural concentration fact (float64 anchored at the
printed worst-coil pair: <650 MPa at I 15.4 MA, B_peak 24.9 T,
side 0.36 m; the printed "<650" bound is taken AS the value,
conservative). The operand responds as I * B_peak / side --
quadratic in coil current once B_peak follows the derived field --
so the paired limit pushes back on both field choice and winding-pack
sizing (rubric Row 3 P3).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: images/page_022_table_0.png (Table 8: "Peak stress on WP
[MPa] <650"; I, side lengths); raw.pdf sec. 2.9 structural
analysis (peak stresses ~600 MPa, axisymmetric I x B model)
*Basis**: J x B x d mean-stress scale with a held, sourced
concentration fact; concept-agnostic (MR-3)

Args:
    inputs: Input parameters validated against Winding_Pack_StressInput schema

Returns:
    float: sigma_wp

Example:
    >>> inputs = Winding_Pack_StressInput(...)
    >>> result = run_winding_pack_stress(inputs)
    """
    return (((inputs.k_sigma * inputs.I_coil) * inputs.B_peak_in) / inputs.wp_side)
