"""Conductor_StrainModule Module Wrapper

TEAx module for Conductor_Strain calculation.

Strain in the HTS tape stack [1] (WI-036, D4):

  eps_cond = f_cond * sigma_wp / E_wp

The conductor is checked separately from the structure because every
surveyed HTS fusion design -- the Stellaris source included -- runs
two checks, a stress check against the structure and a strain check
against the conductor, and this model previously ran only the first.
REBCO is brittle; its performance is governed by strain.

f_cond is a load-sharing factor calibrated from the source's own
reported pair: the winding pack peaks at ~600 MPa von Mises while the
HTS stack strain stays below 0.2%, so the stack sees about two-thirds
of the pack-average strain -- the soldered Cu jacket offloads it.
Both anchors are printed *bounds* taken as values, so the operand
over-estimates strain; that conservatism is disclosed, not corrected.

Honest limit: von Mises is not uniaxial stress and a pack-level stress
is not local tape stress. This is a composition standing in for a
finite-element result the source does not publish, calibrated from the
source's own numbers rather than assumed (the k_sigma convention
applied to a second quantity).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
*Ref**: raw.pdf p. 24 (winding-pack peak von Mises ~600 MPa; HTS
stack peak strain below 0.2% "within acceptable limits, even when
adding strain from bending"); output.md:173,197 (Barth, Mondonico
& Senatore 2015: irreversible strain by manufacturer at 4.2 K/19 T,
SuperOx 0.45-0.47% the lowest of five; "Remaining below 0.4%
strain, there are no discernible differences")
*Basis**: pack-average strain scaled by a sourced load-sharing
factor; concept-agnostic (MR-3)

Inputs:
    - E_wp: E_wp parameter
    - f_cond: f_cond parameter
    - sigma_wp: sigma_wp parameter

Outputs:
    - eps_cond: eps_cond result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:197

SysML Source: root-0/analyses/mfe_magnet_field.sysml:197

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_field/conductor_strain_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Conductor_StrainInput(BaseModel):
    """Input model for Conductor_StrainModule.

    Attributes:
        E_wp: E_wp input
        f_cond: f_cond input
        sigma_wp: sigma_wp input
    """
    E_wp: float = Field(..., description="E_wp input")
    f_cond: float = Field(..., description="f_cond input")
    sigma_wp: float = Field(..., description="sigma_wp input")


class Conductor_StrainModule(ModuleBase[Conductor_StrainInput, Float]):
    """TEAx module for Conductor_Strain calculation.

Strain in the HTS tape stack [1] (WI-036, D4):

  eps_cond = f_cond * sigma_wp / E_wp

The conductor is checked separately from the structure because every
surveyed HTS fusion design -- the Stellaris source included -- runs
two checks, a stress check against the structure and a strain check
against the conductor, and this model previously ran only the first.
REBCO is brittle; its performance is governed by strain.

f_cond is a load-sharing factor calibrated from the source's own
reported pair: the winding pack peaks at ~600 MPa von Mises while the
HTS stack strain stays below 0.2%, so the stack sees about two-thirds
of the pack-average strain -- the soldered Cu jacket offloads it.
Both anchors are printed *bounds* taken as values, so the operand
over-estimates strain; that conservatism is disclosed, not corrected.

Honest limit: von Mises is not uniaxial stress and a pack-level stress
is not local tape stress. This is a composition standing in for a
finite-element result the source does not publish, calibrated from the
source's own numbers rather than assumed (the k_sigma convention
applied to a second quantity).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
*Ref**: raw.pdf p. 24 (winding-pack peak von Mises ~600 MPa; HTS
stack peak strain below 0.2% "within acceptable limits, even when
adding strain from bending"); output.md:173,197 (Barth, Mondonico
& Senatore 2015: irreversible strain by manufacturer at 4.2 K/19 T,
SuperOx 0.45-0.47% the lowest of five; "Remaining below 0.4%
strain, there are no discernible differences")
*Basis**: pack-average strain scaled by a sourced load-sharing
factor; concept-agnostic (MR-3)

Inputs:
    - E_wp: E_wp parameter
    - f_cond: f_cond parameter
    - sigma_wp: sigma_wp parameter

Outputs:
    - eps_cond: eps_cond result

SysML Source: root-0/analyses/mfe_magnet_field.sysml:197

    SysML Source: root-0/analyses/mfe_magnet_field.sysml:197

    Calculation Specification:
        eps_cond = f_cond * sigma_wp / E_wp
        
Documentation:
Strain in the HTS tape stack [1] (WI-036, D4):

  eps_cond = f_cond * sigma_wp / E_wp

The conductor is checked separately from the structure because every
surveyed HTS fusion design -- the Stellaris source included -- runs
two checks, a stress check against the structure and a strain check
against the conductor, and this model previously ran only the first.
REBCO is brittle; its performance is governed by strain.

f_cond is a load-sharing factor calibrated from the source's own
reported pair: the winding pack peaks at ~600 MPa von Mises while the
HTS stack strain stays below 0.2%, so the stack sees about two-thirds
of the pack-average strain -- the soldered Cu jacket offloads it.
Both anchors are printed *bounds* taken as values, so the operand
over-estimates strain; that conservatism is disclosed, not corrected.

Honest limit: von Mises is not uniaxial stress and a pack-level stress
is not local tape stress. This is a composition standing in for a
finite-element result the source does not publish, calibrated from the
source's own numbers rather than assumed (the k_sigma convention
applied to a second quantity).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md;
knowledge/sources/electro_mechanical_properties_of_rebco_coated_conductors/
*Ref**: raw.pdf p. 24 (winding-pack peak von Mises ~600 MPa; HTS
stack peak strain below 0.2% "within acceptable limits, even when
adding strain from bending"); output.md:173,197 (Barth, Mondonico
& Senatore 2015: irreversible strain by manufacturer at 4.2 K/19 T,
SuperOx 0.45-0.47% the lowest of five; "Remaining below 0.4%
strain, there are no discernible differences")
*Basis**: pack-average strain scaled by a sourced load-sharing
factor; concept-agnostic (MR-3)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_magnet_field.conductor_strain_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Conductor_StrainModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, E_wp: float, f_cond: float, sigma_wp: float    ) -> Conductor_StrainInput:
        """Validate inputs and fill defaults.

        Args:
            E_wp: E_wp input
            f_cond: f_cond input
            sigma_wp: sigma_wp input

        Returns:
            Validated input model
        """
        return Conductor_StrainInput(E_wp=E_wp, f_cond=f_cond, sigma_wp=sigma_wp)

    def run(
        self, E_wp: float, f_cond: float, sigma_wp: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            E_wp: E_wp input
            f_cond: f_cond input
            sigma_wp: sigma_wp input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(E_wp, f_cond, sigma_wp)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_magnet_field.conductor_strain_impl import (
            run_conductor_strain,
        )

        # Execute implementation - returns single value
        eps_cond = run_conductor_strain(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(eps_cond))
