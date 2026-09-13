from pydantic import Field
from simkit.config.schema import MultiOutput

class Plasma_GeometryOutput(MultiOutput):
    """Multi-output container for Plasma_Geometry.

Plasma volume [m^3] and aspect ratio [1].

  V = 2 * pi^2 * R * a^2 * kappa * f_shape
  A = R / a                                  (reported, WI-044)

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
    """
    A: float = Field(description="A output")
    V: float = Field(description="V output")
