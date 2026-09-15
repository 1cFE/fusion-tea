"""Plasma_GeometryModule Module Wrapper

TEAx module for Plasma_Geometry calculation.

Plasma volume [m^3] and aspect ratio [1].

  V = 2 * pi^2 * R * a^2 * kappa * f_shape
  A = R / a                                  (reported, WI-044)

The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus
volume. f_shape is the dimensionless ratio of the concept's plasma
volume to this reference torus volume. It is 1.0 for the pure torus
(including the 1costingFE torus geometry); a shaped plasma may have a
ratio above or below 1 for its chosen R, a and kappa. Concept-agnostic:
R is major radius, a is minor radius, kappa is elongation, and the
concept sets f_shape (default 1.0 leaves any existing torus consumer
and the Anchor A handshake unchanged).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
*Basis**: elongated-torus volume with a concept shape factor; MFE-generic

Inputs:
    - pi: pi parameter
    - R_in: R_in parameter
    - a_in: a_in parameter
    - kappa_in: kappa_in parameter
    - f_shape_in: f_shape_in parameter

Outputs:
    - A: A result
    - V: V result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/plasma_geometry_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.plasma_geometry_output import Plasma_GeometryOutput


class Plasma_GeometryInput(BaseModel):
    """Input model for Plasma_GeometryModule.

    Attributes:
        pi: pi input
        R_in: R_in input
        a_in: a_in input
        kappa_in: kappa_in input
        f_shape_in: f_shape_in input
    """
    pi: float = Field(..., description="pi input")
    R_in: float = Field(..., description="R_in input")
    a_in: float = Field(..., description="a_in input")
    kappa_in: float = Field(..., description="kappa_in input")
    f_shape_in: float = Field(..., description="f_shape_in input")


class Plasma_GeometryModule(ModuleBase[Plasma_GeometryInput, Plasma_GeometryOutput]):
    """TEAx module for Plasma_Geometry calculation.

Plasma volume [m^3] and aspect ratio [1].

  V = 2 * pi^2 * R * a^2 * kappa * f_shape
  A = R / a                                  (reported, WI-044)

The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus
volume. f_shape is the dimensionless ratio of the concept's plasma
volume to this reference torus volume. It is 1.0 for the pure torus
(including the 1costingFE torus geometry); a shaped plasma may have a
ratio above or below 1 for its chosen R, a and kappa. Concept-agnostic:
R is major radius, a is minor radius, kappa is elongation, and the
concept sets f_shape (default 1.0 leaves any existing torus consumer
and the Anchor A handshake unchanged).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
*Basis**: elongated-torus volume with a concept shape factor; MFE-generic

Inputs:
    - pi: pi parameter
    - R_in: R_in parameter
    - a_in: a_in parameter
    - kappa_in: kappa_in parameter
    - f_shape_in: f_shape_in parameter

Outputs:
    - A: A result
    - V: V result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

    Calculation Specification:
        f_shape_in = 1.0
        pi = 3.14159265358979
        V = 2.0 * pi ** 2 * R_in * a_in ** 2 * kappa_in * f_shape_in
        A = R_in / a_in
        
Documentation:
Plasma volume [m^3] and aspect ratio [1].

  V = 2 * pi^2 * R * a^2 * kappa * f_shape
  A = R / a                                  (reported, WI-044)

The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus
volume. f_shape is the dimensionless ratio of the concept's plasma
volume to this reference torus volume. It is 1.0 for the pure torus
(including the 1costingFE torus geometry); a shaped plasma may have a
ratio above or below 1 for its chosen R, a and kappa. Concept-agnostic:
R is major radius, a is minor radius, kappa is elongation, and the
concept sets f_shape (default 1.0 leaves any existing torus consumer
and the Anchor A handshake unchanged).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
*Basis**: elongated-torus volume with a concept shape factor; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.plasma_geometry_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts A, V fields to separate channels.
    """

    name: str = "Plasma_GeometryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pi: float, R_in: float, a_in: float, kappa_in: float, f_shape_in: float    ) -> Plasma_GeometryInput:
        """Validate inputs and fill defaults.

        Args:
            pi: pi input
            R_in: R_in input
            a_in: a_in input
            kappa_in: kappa_in input
            f_shape_in: f_shape_in input

        Returns:
            Validated input model
        """
        return Plasma_GeometryInput(pi=pi, R_in=R_in, a_in=a_in, kappa_in=kappa_in, f_shape_in=f_shape_in)

    def run(
        self, pi: float, R_in: float, a_in: float, kappa_in: float, f_shape_in: float    ) -> ModuleResult[Plasma_GeometryOutput]:
        """Execute calculation.

        Args:
            pi: pi input
            R_in: R_in input
            a_in: a_in input
            kappa_in: kappa_in input
            f_shape_in: f_shape_in input

        Returns:
            Module result with Plasma_GeometryOutput (A, V)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pi, R_in, a_in, kappa_in, f_shape_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.plasma_geometry_impl import (
            run_plasma_geometry,
        )

        # Execute implementation - returns tuple of values
        A, V = run_plasma_geometry(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Plasma_GeometryOutput(
                A=A,
                V=V,
            )
        )
