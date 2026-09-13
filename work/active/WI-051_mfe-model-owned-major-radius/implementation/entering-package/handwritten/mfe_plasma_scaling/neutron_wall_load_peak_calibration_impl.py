"""Auto-generated implementation for Neutron_Wall_Load_Peak_Calibration.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

SysML Expressions:
    ash_frac_in = 0.2002
    pi = 3.14159265358979
    A_ref = kappa_ref * 4.0 * pi ** 2 * R_ref * (a_ref + standoff_ref)
    p_n_ref = p_fus_ref * (1.0 - ash_frac_in)
    calibration = q_peak_ref * A_ref / p_n_ref + calibration_direct
    
Documentation:
Source-anchored peak calibration [1]: the multiplier that carries a
circular-torus AVERAGE neutron wall load onto a source's own printed
3D PEAK, evaluated at the source's design point (WI-041).

  A_ref       = kappa_ref * 4*pi^2 * R_ref * (a_ref + standoff_ref)  [m^2]
  p_n_ref     = p_fus_ref * (1 - ash_frac)                           [MW]
  calibration = q_peak_ref * A_ref / p_n_ref + calibration_direct    [1]

A_ref is the SAME circular-torus first-wall area the model's own
'MFE Radial Build' computes (wall_area = kappa*4*pi^2*R*vacuum_or),
evaluated at the source's printed radii and minimum standoff. So
calibration x ('Neutron Wall Load' at the source's power and geometry)
reproduces the source's printed peak exactly, whatever ash_frac both
share. Every factor is a printed source figure or the model's own
convention; nothing is a transferred peaking factor or a shaped-wall
area. The decomposition calibration = p_f x (A_torus / A_wall) is a
cross-check a concept records in its doc text, never an input.

CONSTANCY ASSUMPTION (stated): the calibration is fixed at the source's
design point and carried unchanged over sweeps of geometry, density,
temperature and current -- the wall's peaking factor and shape factor
are taken as constant. Re-anchoring at a new design point, or a sourced
peaking factor on a re-shaped wall, would change it.

Dormant-safe (the WI-024 / WI-039 additive-direct-term pattern): a
concept with no source peak binds q_peak_ref = 0 and calibration_direct
= 1.0, so the calibration is 1.0 and the peak equals the average; a
concept anchoring to a source binds its six reference facts and zeroes
calibration_direct. p_fus_ref must never be 0 (a dormant concept binds
1.0) so the division stays defined.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md; /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py (pin 0254385)
*Ref**: Table 2 image (images/page_002_table_0.png: peak neutron wall load, peak fusion power, radii); geometry.py:67-81 (torus surface area); work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md section 5 (the identity and its decomposition)
*Basis**: a source's printed 3D peak per unit of the model's own circular-torus average at the source's design point; MFE-generic
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.neutron_wall_load_peak_calibration import Neutron_Wall_Load_Peak_CalibrationInput


def run_neutron_wall_load_peak_calibration(inputs: Neutron_Wall_Load_Peak_CalibrationInput) -> float:
    """Execute Neutron_Wall_Load_Peak_Calibration calculation.

Source-anchored peak calibration [1]: the multiplier that carries a
circular-torus AVERAGE neutron wall load onto a source's own printed
3D PEAK, evaluated at the source's design point (WI-041).

  A_ref       = kappa_ref * 4*pi^2 * R_ref * (a_ref + standoff_ref)  [m^2]
  p_n_ref     = p_fus_ref * (1 - ash_frac)                           [MW]
  calibration = q_peak_ref * A_ref / p_n_ref + calibration_direct    [1]

A_ref is the SAME circular-torus first-wall area the model's own
'MFE Radial Build' computes (wall_area = kappa*4*pi^2*R*vacuum_or),
evaluated at the source's printed radii and minimum standoff. So
calibration x ('Neutron Wall Load' at the source's power and geometry)
reproduces the source's printed peak exactly, whatever ash_frac both
share. Every factor is a printed source figure or the model's own
convention; nothing is a transferred peaking factor or a shaped-wall
area. The decomposition calibration = p_f x (A_torus / A_wall) is a
cross-check a concept records in its doc text, never an input.

CONSTANCY ASSUMPTION (stated): the calibration is fixed at the source's
design point and carried unchanged over sweeps of geometry, density,
temperature and current -- the wall's peaking factor and shape factor
are taken as constant. Re-anchoring at a new design point, or a sourced
peaking factor on a re-shaped wall, would change it.

Dormant-safe (the WI-024 / WI-039 additive-direct-term pattern): a
concept with no source peak binds q_peak_ref = 0 and calibration_direct
= 1.0, so the calibration is 1.0 and the peak equals the average; a
concept anchoring to a source binds its six reference facts and zeroes
calibration_direct. p_fus_ref must never be 0 (a dormant concept binds
1.0) so the division stays defined.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md; /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py (pin 0254385)
*Ref**: Table 2 image (images/page_002_table_0.png: peak neutron wall load, peak fusion power, radii); geometry.py:67-81 (torus surface area); work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md section 5 (the identity and its decomposition)
*Basis**: a source's printed 3D peak per unit of the model's own circular-torus average at the source's design point; MFE-generic

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

SysML Expressions:
    ash_frac_in = 0.2002
    pi = 3.14159265358979
    A_ref = kappa_ref * 4.0 * pi ** 2 * R_ref * (a_ref + standoff_ref)
    p_n_ref = p_fus_ref * (1.0 - ash_frac_in)
    calibration = q_peak_ref * A_ref / p_n_ref + calibration_direct
    
Documentation:
Source-anchored peak calibration [1]: the multiplier that carries a
circular-torus AVERAGE neutron wall load onto a source's own printed
3D PEAK, evaluated at the source's design point (WI-041).

  A_ref       = kappa_ref * 4*pi^2 * R_ref * (a_ref + standoff_ref)  [m^2]
  p_n_ref     = p_fus_ref * (1 - ash_frac)                           [MW]
  calibration = q_peak_ref * A_ref / p_n_ref + calibration_direct    [1]

A_ref is the SAME circular-torus first-wall area the model's own
'MFE Radial Build' computes (wall_area = kappa*4*pi^2*R*vacuum_or),
evaluated at the source's printed radii and minimum standoff. So
calibration x ('Neutron Wall Load' at the source's power and geometry)
reproduces the source's printed peak exactly, whatever ash_frac both
share. Every factor is a printed source figure or the model's own
convention; nothing is a transferred peaking factor or a shaped-wall
area. The decomposition calibration = p_f x (A_torus / A_wall) is a
cross-check a concept records in its doc text, never an input.

CONSTANCY ASSUMPTION (stated): the calibration is fixed at the source's
design point and carried unchanged over sweeps of geometry, density,
temperature and current -- the wall's peaking factor and shape factor
are taken as constant. Re-anchoring at a new design point, or a sourced
peaking factor on a re-shaped wall, would change it.

Dormant-safe (the WI-024 / WI-039 additive-direct-term pattern): a
concept with no source peak binds q_peak_ref = 0 and calibration_direct
= 1.0, so the calibration is 1.0 and the peak equals the average; a
concept anchoring to a source binds its six reference facts and zeroes
calibration_direct. p_fus_ref must never be 0 (a dormant concept binds
1.0) so the division stays defined.

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md; /home/reid/1cfe/1costingfe/src/costingfe/layers/geometry.py (pin 0254385)
*Ref**: Table 2 image (images/page_002_table_0.png: peak neutron wall load, peak fusion power, radii); geometry.py:67-81 (torus surface area); work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md section 5 (the identity and its decomposition)
*Basis**: a source's printed 3D peak per unit of the model's own circular-torus average at the source's design point; MFE-generic

Args:
    inputs: Input parameters validated against Neutron_Wall_Load_Peak_CalibrationInput schema

Returns:
    float: calibration

Example:
    >>> inputs = Neutron_Wall_Load_Peak_CalibrationInput(...)
    >>> result = run_neutron_wall_load_peak_calibration(inputs)
    """
    A_ref = ((((inputs.kappa_ref * 4.0) * (inputs.pi ** 2)) * inputs.R_ref) * (inputs.a_ref + inputs.standoff_ref))
    p_n_ref = (inputs.p_fus_ref * (1.0 - inputs.ash_frac_in))
    return (((inputs.q_peak_ref * A_ref) / p_n_ref) + inputs.calibration_direct)
