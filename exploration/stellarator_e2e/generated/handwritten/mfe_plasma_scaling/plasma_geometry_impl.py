"""Auto-generated implementation for Plasma_Geometry.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

SysML Expressions:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.plasma_geometry import Plasma_GeometryInput


def run_plasma_geometry(inputs: Plasma_GeometryInput) -> float:
    """Execute Plasma_Geometry calculation.

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

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:4

SysML Expressions:
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

Args:
    inputs: Input parameters validated against Plasma_GeometryInput schema

Returns:
    float: V

Example:
    >>> inputs = Plasma_GeometryInput(...)
    >>> result = run_plasma_geometry(inputs)
    """
    return (((((2.0 * (inputs.pi ** 2)) * inputs.R_in) * (inputs.a_in ** 2)) * inputs.kappa_in) * inputs.f_shape_in)
