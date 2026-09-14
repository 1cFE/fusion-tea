"""Coil_Set_Stored_EnergyModule Module Wrapper

TEAx module for Coil_Set_Stored_Energy calculation.

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

Inputs:
    - R0: R0 parameter
    - I_coil: I_coil parameter
    - R_ref: R_ref parameter
    - W_mag_ref: W_mag_ref parameter
    - a_coil: a_coil parameter
    - I_ref: I_ref parameter
    - a_coil_ref: a_coil_ref parameter

Outputs:
    - W_mag: W_mag result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:264

SysML Source: root-0/analyses/mfe_magnet_field.sysml:264

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/coil_set_stored_energy_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Coil_Set_Stored_EnergyInput(BaseModel):
    """Input model for Coil_Set_Stored_EnergyModule.

    Attributes:
        R0: R0 input
        I_coil: I_coil input
        R_ref: R_ref input
        W_mag_ref: W_mag_ref input
        a_coil: a_coil input
        I_ref: I_ref input
        a_coil_ref: a_coil_ref input
    """
    R0: float = Field(..., description="R0 input")
    I_coil: float = Field(..., description="I_coil input")
    R_ref: float = Field(..., description="R_ref input")
    W_mag_ref: float = Field(..., description="W_mag_ref input")
    a_coil: float = Field(..., description="a_coil input")
    I_ref: float = Field(..., description="I_ref input")
    a_coil_ref: float = Field(..., description="a_coil_ref input")


class Coil_Set_Stored_EnergyModule(ModuleBase[Coil_Set_Stored_EnergyInput, Float]):
    """TEAx module for Coil_Set_Stored_Energy calculation.

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

Inputs:
    - R0: R0 parameter
    - I_coil: I_coil parameter
    - R_ref: R_ref parameter
    - W_mag_ref: W_mag_ref parameter
    - a_coil: a_coil parameter
    - I_ref: I_ref parameter
    - a_coil_ref: a_coil_ref parameter

Outputs:
    - W_mag: W_mag result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:264

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:264

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_field.coil_set_stored_energy_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Coil_Set_Stored_EnergyModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, R0: float, I_coil: float, R_ref: float, W_mag_ref: float, a_coil: float, I_ref: float, a_coil_ref: float    ) -> Coil_Set_Stored_EnergyInput:
        """Validate inputs and fill defaults.

        Args:
            R0: R0 input
            I_coil: I_coil input
            R_ref: R_ref input
            W_mag_ref: W_mag_ref input
            a_coil: a_coil input
            I_ref: I_ref input
            a_coil_ref: a_coil_ref input

        Returns:
            Validated input model
        """
        return Coil_Set_Stored_EnergyInput(R0=R0, I_coil=I_coil, R_ref=R_ref, W_mag_ref=W_mag_ref, a_coil=a_coil, I_ref=I_ref, a_coil_ref=a_coil_ref)

    def run(
        self, R0: float, I_coil: float, R_ref: float, W_mag_ref: float, a_coil: float, I_ref: float, a_coil_ref: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            R0: R0 input
            I_coil: I_coil input
            R_ref: R_ref input
            W_mag_ref: W_mag_ref input
            a_coil: a_coil input
            I_ref: I_ref input
            a_coil_ref: a_coil_ref input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(R0, I_coil, R_ref, W_mag_ref, a_coil, I_ref, a_coil_ref)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.coil_set_stored_energy_impl import (
            run_coil_set_stored_energy,
        )

        # Execute implementation - returns single value
        W_mag = run_coil_set_stored_energy(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(W_mag))
