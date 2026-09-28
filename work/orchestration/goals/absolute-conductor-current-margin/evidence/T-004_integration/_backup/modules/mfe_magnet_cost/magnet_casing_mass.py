"""Magnet_Casing_MassModule Module Wrapper

TEAx module for Magnet_Casing_Mass calculation.

Casing steel mass per coil [kg] from the coil set's stored magnetic
energy, anchored at a reference (WI-044):

  m_casing = m_casing_ref * (W_mag / W_mag_ref)^0.78

Lion 2021 eq. 56, M_struct = 1.348 W_mag^0.78, "an empirical scaling
law from existing machines" (L607) that Stellarator-PROCESS uses for
the total coil support-structure mass because "the total mass is a
good proxy, both for the cost and the support structure complexity".
The source prints no units for the constant, so the constant is
absorbed by the anchor: m_casing_ref is the instance's casing mass at
its reference stored energy and only the exponent is carried. The
anchor keeps whatever seam the instance's reference carries (for
Stellaris the printed cast-part FLOOR, a knowing lower bound -- WI-035
design D5); the scale responds to the bore through W_mag and the seam
stays named at the binding. Disclosed limit (the source's own): the
law "does not show whether the design point has local unsupportable
forces" (L609).

*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2021_nf_stellarator_process.pdf-0012-18.png (eq. 56);
output.md L607 (the empirical law and its role), L609 (its limit)
*Basis**: reference casing mass scaled by the sourced W_mag^0.78 law;
concept-agnostic (MR-3) -- all values bound by instances

Inputs:
    - W_mag_ref: W_mag_ref parameter
    - m_casing_ref: m_casing_ref parameter
    - W_mag: W_mag parameter

Outputs:
    - m_casing: m_casing result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/magnet_casing_mass_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Magnet_Casing_MassInput(BaseModel):
    """Input model for Magnet_Casing_MassModule.

    Attributes:
        W_mag_ref: W_mag_ref input
        m_casing_ref: m_casing_ref input
        W_mag: W_mag input
    """
    W_mag_ref: float = Field(..., description="W_mag_ref input")
    m_casing_ref: float = Field(..., description="m_casing_ref input")
    W_mag: float = Field(..., description="W_mag input")


class Magnet_Casing_MassModule(ModuleBase[Magnet_Casing_MassInput, Float]):
    """TEAx module for Magnet_Casing_Mass calculation.

Casing steel mass per coil [kg] from the coil set's stored magnetic
energy, anchored at a reference (WI-044):

  m_casing = m_casing_ref * (W_mag / W_mag_ref)^0.78

Lion 2021 eq. 56, M_struct = 1.348 W_mag^0.78, "an empirical scaling
law from existing machines" (L607) that Stellarator-PROCESS uses for
the total coil support-structure mass because "the total mass is a
good proxy, both for the cost and the support structure complexity".
The source prints no units for the constant, so the constant is
absorbed by the anchor: m_casing_ref is the instance's casing mass at
its reference stored energy and only the exponent is carried. The
anchor keeps whatever seam the instance's reference carries (for
Stellaris the printed cast-part FLOOR, a knowing lower bound -- WI-035
design D5); the scale responds to the bore through W_mag and the seam
stays named at the binding. Disclosed limit (the source's own): the
law "does not show whether the design point has local unsupportable
forces" (L609).

*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2021_nf_stellarator_process.pdf-0012-18.png (eq. 56);
output.md L607 (the empirical law and its role), L609 (its limit)
*Basis**: reference casing mass scaled by the sourced W_mag^0.78 law;
concept-agnostic (MR-3) -- all values bound by instances

Inputs:
    - W_mag_ref: W_mag_ref parameter
    - m_casing_ref: m_casing_ref parameter
    - W_mag: W_mag parameter

Outputs:
    - m_casing: m_casing result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:103

    Calculation Specification:
        m_casing = m_casing_ref * (W_mag / W_mag_ref) ** 0.78
        
Documentation:
Casing steel mass per coil [kg] from the coil set's stored magnetic
energy, anchored at a reference (WI-044):

  m_casing = m_casing_ref * (W_mag / W_mag_ref)^0.78

Lion 2021 eq. 56, M_struct = 1.348 W_mag^0.78, "an empirical scaling
law from existing machines" (L607) that Stellarator-PROCESS uses for
the total coil support-structure mass because "the total mass is a
good proxy, both for the cost and the support structure complexity".
The source prints no units for the constant, so the constant is
absorbed by the anchor: m_casing_ref is the instance's casing mass at
its reference stored energy and only the exponent is carried. The
anchor keeps whatever seam the instance's reference carries (for
Stellaris the printed cast-part FLOOR, a knowing lower bound -- WI-035
design D5); the scale responds to the bore through W_mag and the seam
stays named at the binding. Disclosed limit (the source's own): the
law "does not show whether the design point has local unsupportable
forces" (L609).

*Source**: knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
*Ref**: images/lion_2021_nf_stellarator_process.pdf-0012-18.png (eq. 56);
output.md L607 (the empirical law and its role), L609 (its limit)
*Basis**: reference casing mass scaled by the sourced W_mag^0.78 law;
concept-agnostic (MR-3) -- all values bound by instances

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_cost.magnet_casing_mass_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Magnet_Casing_MassModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, W_mag_ref: float, m_casing_ref: float, W_mag: float    ) -> Magnet_Casing_MassInput:
        """Validate inputs and fill defaults.

        Args:
            W_mag_ref: W_mag_ref input
            m_casing_ref: m_casing_ref input
            W_mag: W_mag input

        Returns:
            Validated input model
        """
        return Magnet_Casing_MassInput(W_mag_ref=W_mag_ref, m_casing_ref=m_casing_ref, W_mag=W_mag)

    def run(
        self, W_mag_ref: float, m_casing_ref: float, W_mag: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            W_mag_ref: W_mag_ref input
            m_casing_ref: m_casing_ref input
            W_mag: W_mag input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(W_mag_ref, m_casing_ref, W_mag)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_cost.magnet_casing_mass_impl import (
            run_magnet_casing_mass,
        )

        # Execute implementation - returns single value
        m_casing = run_magnet_casing_mass(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(m_casing))
