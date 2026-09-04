"""Neutron_Wall_Load_Peak_CalibrationModule Module Wrapper

TEAx module for Neutron_Wall_Load_Peak_Calibration calculation.

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

Inputs:
    - calibration_direct: calibration_direct parameter
    - R_ref: R_ref parameter
    - pi: pi parameter
    - a_ref: a_ref parameter
    - kappa_ref: kappa_ref parameter
    - p_fus_ref: p_fus_ref parameter
    - standoff_ref: standoff_ref parameter
    - q_peak_ref: q_peak_ref parameter
    - ash_frac_in: ash_frac_in parameter

Outputs:
    - calibration: calibration result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/neutron_wall_load_peak_calibration_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Neutron_Wall_Load_Peak_CalibrationInput(BaseModel):
    """Input model for Neutron_Wall_Load_Peak_CalibrationModule.

    Attributes:
        calibration_direct: calibration_direct input
        R_ref: R_ref input
        pi: pi input
        a_ref: a_ref input
        kappa_ref: kappa_ref input
        p_fus_ref: p_fus_ref input
        standoff_ref: standoff_ref input
        q_peak_ref: q_peak_ref input
        ash_frac_in: ash_frac_in input
    """
    calibration_direct: float = Field(..., description="calibration_direct input")
    R_ref: float = Field(..., description="R_ref input")
    pi: float = Field(..., description="pi input")
    a_ref: float = Field(..., description="a_ref input")
    kappa_ref: float = Field(..., description="kappa_ref input")
    p_fus_ref: float = Field(..., description="p_fus_ref input")
    standoff_ref: float = Field(..., description="standoff_ref input")
    q_peak_ref: float = Field(..., description="q_peak_ref input")
    ash_frac_in: float = Field(..., description="ash_frac_in input")


class Neutron_Wall_Load_Peak_CalibrationModule(ModuleBase[Neutron_Wall_Load_Peak_CalibrationInput, Float]):
    """TEAx module for Neutron_Wall_Load_Peak_Calibration calculation.

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

Inputs:
    - calibration_direct: calibration_direct parameter
    - R_ref: R_ref parameter
    - pi: pi parameter
    - a_ref: a_ref parameter
    - kappa_ref: kappa_ref parameter
    - p_fus_ref: p_fus_ref parameter
    - standoff_ref: standoff_ref parameter
    - q_peak_ref: q_peak_ref parameter
    - ash_frac_in: ash_frac_in parameter

Outputs:
    - calibration: calibration result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.neutron_wall_load_peak_calibration_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Neutron_Wall_Load_Peak_CalibrationModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, calibration_direct: float, R_ref: float, pi: float, a_ref: float, kappa_ref: float, p_fus_ref: float, standoff_ref: float, q_peak_ref: float, ash_frac_in: float    ) -> Neutron_Wall_Load_Peak_CalibrationInput:
        """Validate inputs and fill defaults.

        Args:
            calibration_direct: calibration_direct input
            R_ref: R_ref input
            pi: pi input
            a_ref: a_ref input
            kappa_ref: kappa_ref input
            p_fus_ref: p_fus_ref input
            standoff_ref: standoff_ref input
            q_peak_ref: q_peak_ref input
            ash_frac_in: ash_frac_in input

        Returns:
            Validated input model
        """
        return Neutron_Wall_Load_Peak_CalibrationInput(calibration_direct=calibration_direct, R_ref=R_ref, pi=pi, a_ref=a_ref, kappa_ref=kappa_ref, p_fus_ref=p_fus_ref, standoff_ref=standoff_ref, q_peak_ref=q_peak_ref, ash_frac_in=ash_frac_in)

    def run(
        self, calibration_direct: float, R_ref: float, pi: float, a_ref: float, kappa_ref: float, p_fus_ref: float, standoff_ref: float, q_peak_ref: float, ash_frac_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            calibration_direct: calibration_direct input
            R_ref: R_ref input
            pi: pi input
            a_ref: a_ref input
            kappa_ref: kappa_ref input
            p_fus_ref: p_fus_ref input
            standoff_ref: standoff_ref input
            q_peak_ref: q_peak_ref input
            ash_frac_in: ash_frac_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(calibration_direct, R_ref, pi, a_ref, kappa_ref, p_fus_ref, standoff_ref, q_peak_ref, ash_frac_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.neutron_wall_load_peak_calibration_impl import (
            run_neutron_wall_load_peak_calibration,
        )

        # Execute implementation - returns single value
        calibration = run_neutron_wall_load_peak_calibration(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(calibration))
