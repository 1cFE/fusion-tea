"""Radial_Density_ProfileModule Module Wrapper

TEAx module for Radial_Density_Profile calculation.

Local density [m^-3] at a supplied normalized radial coordinate.
amplitude_in is an equation coefficient, not an axis, peak or mean density.
density=(amplitude-edge)*(1-rho^p)^q*(h+(1-h)*rho^2)+edge.
The typed manual completion enforces finite inputs, amplitude>0,
0<=edge<=amplitude, 0<=rho<=1, p>0, q>0 and 0<=h<=1;
nonfinite intermediates or output are refused. This mathematical domain
is not an empirical plasma validity claim. All six inputs are supplied
choices; the calculation selects no profile amplitude or hardware.
Source equation is used here for the authorized post-reveal comparison;
no ARIES-specific shape or amplitude is embedded in this reusable logic.
*Source**: work/active/WI-081_aries-hollow-finite-edge-density-profile/spec.md
*Reference**: Lyon 2008 Eq. (3), printed p701; retained primary image
.project/active/aries-comparison-preparation/post-reveal-preparation/mapping/evidence/lyon-p701.png;
work/orchestration/aries-transfer-experiment/evidence/profile-review.md
*Last Updated**: 2026-09-21

Inputs:
    - hollowness_in: hollowness_in parameter
    - edge_density_in: edge_density_in parameter
    - rho_in: rho_in parameter
    - radial_exponent_in: radial_exponent_in parameter
    - amplitude_in: amplitude_in parameter
    - profile_exponent_in: profile_exponent_in parameter

Outputs:
    - density: density result

SysML Source: root-0/radial_density_profile.sysml:4

SysML Source: root-0/radial_density_profile.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/radial_density_profile/radial_density_profile_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float


class Radial_Density_ProfileInput(BaseModel):
    """Input model for Radial_Density_ProfileModule.

    Attributes:
        hollowness_in: hollowness_in input
        edge_density_in: edge_density_in input
        rho_in: rho_in input
        radial_exponent_in: radial_exponent_in input
        amplitude_in: amplitude_in input
        profile_exponent_in: profile_exponent_in input
    """
    hollowness_in: float = Field(..., description="hollowness_in input")
    edge_density_in: float = Field(..., description="edge_density_in input")
    rho_in: float = Field(..., description="rho_in input")
    radial_exponent_in: float = Field(..., description="radial_exponent_in input")
    amplitude_in: float = Field(..., description="amplitude_in input")
    profile_exponent_in: float = Field(..., description="profile_exponent_in input")


class Radial_Density_ProfileModule(ModuleBase[Radial_Density_ProfileInput, Float]):
    """TEAx module for Radial_Density_Profile calculation.

Local density [m^-3] at a supplied normalized radial coordinate.
amplitude_in is an equation coefficient, not an axis, peak or mean density.
density=(amplitude-edge)*(1-rho^p)^q*(h+(1-h)*rho^2)+edge.
The typed manual completion enforces finite inputs, amplitude>0,
0<=edge<=amplitude, 0<=rho<=1, p>0, q>0 and 0<=h<=1;
nonfinite intermediates or output are refused. This mathematical domain
is not an empirical plasma validity claim. All six inputs are supplied
choices; the calculation selects no profile amplitude or hardware.
Source equation is used here for the authorized post-reveal comparison;
no ARIES-specific shape or amplitude is embedded in this reusable logic.
*Source**: work/active/WI-081_aries-hollow-finite-edge-density-profile/spec.md
*Reference**: Lyon 2008 Eq. (3), printed p701; retained primary image
.project/active/aries-comparison-preparation/post-reveal-preparation/mapping/evidence/lyon-p701.png;
work/orchestration/aries-transfer-experiment/evidence/profile-review.md
*Last Updated**: 2026-09-21

Inputs:
    - hollowness_in: hollowness_in parameter
    - edge_density_in: edge_density_in parameter
    - rho_in: rho_in parameter
    - radial_exponent_in: radial_exponent_in parameter
    - amplitude_in: amplitude_in parameter
    - profile_exponent_in: profile_exponent_in parameter

Outputs:
    - density: density result

SysML Source: root-0/radial_density_profile.sysml:4

    SysML Source: root-0/radial_density_profile.sysml:4

    Calculation Specification:
        density = (amplitude_in - edge_density_in) * (1.0 - rho_in ** radial_exponent_in) ** profile_exponent_in * (hollowness_in + (1.0 - hollowness_in) * rho_in ** 2.0) + edge_density_in
        
Documentation:
Local density [m^-3] at a supplied normalized radial coordinate.
amplitude_in is an equation coefficient, not an axis, peak or mean density.
density=(amplitude-edge)*(1-rho^p)^q*(h+(1-h)*rho^2)+edge.
The typed manual completion enforces finite inputs, amplitude>0,
0<=edge<=amplitude, 0<=rho<=1, p>0, q>0 and 0<=h<=1;
nonfinite intermediates or output are refused. This mathematical domain
is not an empirical plasma validity claim. All six inputs are supplied
choices; the calculation selects no profile amplitude or hardware.
Source equation is used here for the authorized post-reveal comparison;
no ARIES-specific shape or amplitude is embedded in this reusable logic.
*Source**: work/active/WI-081_aries-hollow-finite-edge-density-profile/spec.md
*Reference**: Lyon 2008 Eq. (3), printed p701; retained primary image
.project/active/aries-comparison-preparation/post-reveal-preparation/mapping/evidence/lyon-p701.png;
work/orchestration/aries-transfer-experiment/evidence/profile-review.md
*Last Updated**: 2026-09-21

    IMPLEMENTATION: See aries_integrated.handwritten.radial_density_profile.radial_density_profile_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Radial_Density_ProfileModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, hollowness_in: float, edge_density_in: float, rho_in: float, radial_exponent_in: float, amplitude_in: float, profile_exponent_in: float    ) -> Radial_Density_ProfileInput:
        """Validate inputs and fill defaults.

        Args:
            hollowness_in: hollowness_in input
            edge_density_in: edge_density_in input
            rho_in: rho_in input
            radial_exponent_in: radial_exponent_in input
            amplitude_in: amplitude_in input
            profile_exponent_in: profile_exponent_in input

        Returns:
            Validated input model
        """
        return Radial_Density_ProfileInput(hollowness_in=hollowness_in, edge_density_in=edge_density_in, rho_in=rho_in, radial_exponent_in=radial_exponent_in, amplitude_in=amplitude_in, profile_exponent_in=profile_exponent_in)

    def run(
        self, hollowness_in: float, edge_density_in: float, rho_in: float, radial_exponent_in: float, amplitude_in: float, profile_exponent_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            hollowness_in: hollowness_in input
            edge_density_in: edge_density_in input
            rho_in: rho_in input
            radial_exponent_in: radial_exponent_in input
            amplitude_in: amplitude_in input
            profile_exponent_in: profile_exponent_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(hollowness_in, edge_density_in, rho_in, radial_exponent_in, amplitude_in, profile_exponent_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.radial_density_profile.radial_density_profile_impl import (
            run_radial_density_profile,
        )

        # Execute implementation - returns single value
        density = run_radial_density_profile(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(density))
