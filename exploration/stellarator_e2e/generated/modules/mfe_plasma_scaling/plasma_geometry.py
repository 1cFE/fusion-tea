"""Plasma_GeometryModule Module Wrapper

TEAx module for Plasma_Geometry calculation.

Plasma volume [m^3].

  V = 2 * pi^2 * R * a^2 * kappa * f_shape

The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus
volume. f_shape is a dimensionless shape/packing factor: 1.0 for a pure
torus (tokamak, and the 1costingFE torus geometry), < 1 for a shaped
stellarator plasma whose twisted, non-circular cross-section encloses
less volume than the torus of the same R, a, kappa. Concept-agnostic:
R is major radius, a is minor radius, kappa is elongation, and the
concept sets f_shape (default 1.0 leaves any existing torus consumer
and the Anchor A handshake unchanged).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
*Basis**: elongated-torus volume with a concept shape factor; MFE-generic

Inputs:
    - f_shape_in: f_shape_in parameter
    - pi: pi parameter
    - R_in: R_in parameter
    - a_in: a_in parameter
    - kappa_in: kappa_in parameter

Outputs:
    - V: V result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/plasma_geometry_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Plasma_GeometryInput(BaseModel):
    """Input model for Plasma_GeometryModule.

    Attributes:
        f_shape_in: f_shape_in input
        pi: pi input
        R_in: R_in input
        a_in: a_in input
        kappa_in: kappa_in input
    """
    f_shape_in: float = Field(..., description="f_shape_in input")
    pi: float = Field(..., description="pi input")
    R_in: float = Field(..., description="R_in input")
    a_in: float = Field(..., description="a_in input")
    kappa_in: float = Field(..., description="kappa_in input")


class Plasma_GeometryModule(ModuleBase[Plasma_GeometryInput, Float]):
    """TEAx module for Plasma_Geometry calculation.

Plasma volume [m^3].

  V = 2 * pi^2 * R * a^2 * kappa * f_shape

The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus
volume. f_shape is a dimensionless shape/packing factor: 1.0 for a pure
torus (tokamak, and the 1costingFE torus geometry), < 1 for a shaped
stellarator plasma whose twisted, non-circular cross-section encloses
less volume than the torus of the same R, a, kappa. Concept-agnostic:
R is major radius, a is minor radius, kappa is elongation, and the
concept sets f_shape (default 1.0 leaves any existing torus consumer
and the Anchor A handshake unchanged).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
*Basis**: elongated-torus volume with a concept shape factor; MFE-generic

Inputs:
    - f_shape_in: f_shape_in parameter
    - pi: pi parameter
    - R_in: R_in parameter
    - a_in: a_in parameter
    - kappa_in: kappa_in parameter

Outputs:
    - V: V result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

    Calculation Specification:
        f_shape_in = 1.0
        pi = 3.14159265358979
        V = 2.0 * pi ** 2 * R_in * a_in ** 2 * kappa_in * f_shape_in
        
Documentation:
Plasma volume [m^3].

  V = 2 * pi^2 * R * a^2 * kappa * f_shape

The elongated-torus term (2*pi^2*R*a^2*kappa) is the smooth-torus
volume. f_shape is a dimensionless shape/packing factor: 1.0 for a pure
torus (tokamak, and the 1costingFE torus geometry), < 1 for a shaped
stellarator plasma whose twisted, non-circular cross-section encloses
less volume than the torus of the same R, a, kappa. Concept-agnostic:
R is major radius, a is minor radius, kappa is elongation, and the
concept sets f_shape (default 1.0 leaves any existing torus consumer
and the Anchor A handshake unchanged).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume, the f_shape = 1.0 torus term)
*Basis**: elongated-torus volume with a concept shape factor; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.plasma_geometry_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Plasma_GeometryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, f_shape_in: float, pi: float, R_in: float, a_in: float, kappa_in: float    ) -> Plasma_GeometryInput:
        """Validate inputs and fill defaults.

        Args:
            f_shape_in: f_shape_in input
            pi: pi input
            R_in: R_in input
            a_in: a_in input
            kappa_in: kappa_in input

        Returns:
            Validated input model
        """
        return Plasma_GeometryInput(f_shape_in=f_shape_in, pi=pi, R_in=R_in, a_in=a_in, kappa_in=kappa_in)

    def run(
        self, f_shape_in: float, pi: float, R_in: float, a_in: float, kappa_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            f_shape_in: f_shape_in input
            pi: pi input
            R_in: R_in input
            a_in: a_in input
            kappa_in: kappa_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(f_shape_in, pi, R_in, a_in, kappa_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.plasma_geometry_impl import (
            run_plasma_geometry,
        )

        # Execute implementation - returns single value
        V = run_plasma_geometry(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(V))
