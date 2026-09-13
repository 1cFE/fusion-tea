"""Auto-generated implementation for Coil_Set_Stored_Energy.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_magnet_field.sysml:244

SysML Expressions:
    W_mag = W_mag_ref * (I_coil / I_ref) ** 2 * (a_coil / a_coil_ref) ** 2 * (R_ref / R0)
    
Documentation:
Stored magnetic energy of the coil set [J] from the coil-set inductance
shape, anchored at a reference point (WI-044):

  W_mag = W_mag_ref * (I_coil / I_ref)^2 * (a_coil / a_coil_ref)^2 * (R_ref / R0)

Lion 2023 eq. 2.82 scales a stellarator coil set's inductance from a
reference point, L = L(C) (a_coil^2 / a_coil_ref^2) (R_ref / R): the
inductance of a filamentary coil set grows with the coil minor radius
squared and falls with the major radius at fixed shape. With
W_mag = 1/2 L I^2 (eq. 2.81 on the same page: per coil
E = L I^2 / (2 N)), the stored energy at fixed current and R grows with
the coil bore squared -- the one place the corpus prices a bigger coil
bore ("The stored magnetic energy scales with the coil minor radius",
Lion 2021 L764, the 30/50/60-coil study). L(C) is a configuration fact
computed in the codes' pre-processing and not printed for any instance
here, so the form is ANCHORED: W_mag_ref is the printed stored energy at
the reference current and geometry, and every ratio is exactly 1.0
there. a_coil is the coil-centre minor radius ('MFE Radial Build'
r_coil_centre). Disclosed limit: a changed coil count or shape is a
different L(C); this shape holds the configuration.

*Source**: knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0074-12.png
(eq. 2.82) and -0074-10.png (eq. 2.81) with output.md L1480 (the
inductance "calculated in the pre-processing step ... for a
reference point and can be scaled in Process according to");
lion_2021 output.md L764 (stored energy scales with the coil
minor radius)
*Basis**: reference stored energy scaled by the sourced inductance
shape and the current squared; concept-agnostic (MR-3) -- all
values bound by instances
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_magnet_field.coil_set_stored_energy import Coil_Set_Stored_EnergyInput


def run_coil_set_stored_energy(inputs: Coil_Set_Stored_EnergyInput) -> float:
    """Execute Coil_Set_Stored_Energy calculation.

Stored magnetic energy of the coil set [J] from the coil-set inductance
shape, anchored at a reference point (WI-044):

  W_mag = W_mag_ref * (I_coil / I_ref)^2 * (a_coil / a_coil_ref)^2 * (R_ref / R0)

Lion 2023 eq. 2.82 scales a stellarator coil set's inductance from a
reference point, L = L(C) (a_coil^2 / a_coil_ref^2) (R_ref / R): the
inductance of a filamentary coil set grows with the coil minor radius
squared and falls with the major radius at fixed shape. With
W_mag = 1/2 L I^2 (eq. 2.81 on the same page: per coil
E = L I^2 / (2 N)), the stored energy at fixed current and R grows with
the coil bore squared -- the one place the corpus prices a bigger coil
bore ("The stored magnetic energy scales with the coil minor radius",
Lion 2021 L764, the 30/50/60-coil study). L(C) is a configuration fact
computed in the codes' pre-processing and not printed for any instance
here, so the form is ANCHORED: W_mag_ref is the printed stored energy at
the reference current and geometry, and every ratio is exactly 1.0
there. a_coil is the coil-centre minor radius ('MFE Radial Build'
r_coil_centre). Disclosed limit: a changed coil count or shape is a
different L(C); this shape holds the configuration.

*Source**: knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0074-12.png
(eq. 2.82) and -0074-10.png (eq. 2.81) with output.md L1480 (the
inductance "calculated in the pre-processing step ... for a
reference point and can be scaled in Process according to");
lion_2021 output.md L764 (stored energy scales with the coil
minor radius)
*Basis**: reference stored energy scaled by the sourced inductance
shape and the current squared; concept-agnostic (MR-3) -- all
values bound by instances

SysML Source: root-0/analyses/mfe_magnet_field.sysml:244

SysML Expressions:
    W_mag = W_mag_ref * (I_coil / I_ref) ** 2 * (a_coil / a_coil_ref) ** 2 * (R_ref / R0)
    
Documentation:
Stored magnetic energy of the coil set [J] from the coil-set inductance
shape, anchored at a reference point (WI-044):

  W_mag = W_mag_ref * (I_coil / I_ref)^2 * (a_coil / a_coil_ref)^2 * (R_ref / R0)

Lion 2023 eq. 2.82 scales a stellarator coil set's inductance from a
reference point, L = L(C) (a_coil^2 / a_coil_ref^2) (R_ref / R): the
inductance of a filamentary coil set grows with the coil minor radius
squared and falls with the major radius at fixed shape. With
W_mag = 1/2 L I^2 (eq. 2.81 on the same page: per coil
E = L I^2 / (2 N)), the stored energy at fixed current and R grows with
the coil bore squared -- the one place the corpus prices a bigger coil
bore ("The stored magnetic energy scales with the coil minor radius",
Lion 2021 L764, the 30/50/60-coil study). L(C) is a configuration fact
computed in the codes' pre-processing and not printed for any instance
here, so the form is ANCHORED: W_mag_ref is the printed stored energy at
the reference current and geometry, and every ratio is exactly 1.0
there. a_coil is the coil-centre minor radius ('MFE Radial Build'
r_coil_centre). Disclosed limit: a changed coil count or shape is a
different L(C); this shape holds the configuration.

*Source**: knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/;
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2023_phd_thesis_stellarator_systems_code_models.pdf-0074-12.png
(eq. 2.82) and -0074-10.png (eq. 2.81) with output.md L1480 (the
inductance "calculated in the pre-processing step ... for a
reference point and can be scaled in Process according to");
lion_2021 output.md L764 (stored energy scales with the coil
minor radius)
*Basis**: reference stored energy scaled by the sourced inductance
shape and the current squared; concept-agnostic (MR-3) -- all
values bound by instances

Args:
    inputs: Input parameters validated against Coil_Set_Stored_EnergyInput schema

Returns:
    float: W_mag

Example:
    >>> inputs = Coil_Set_Stored_EnergyInput(...)
    >>> result = run_coil_set_stored_energy(inputs)
    """
    return (((inputs.W_mag_ref * ((inputs.I_coil / inputs.I_ref) ** 2)) * ((inputs.a_coil / inputs.a_coil_ref) ** 2)) * (inputs.R_ref / inputs.R0))
