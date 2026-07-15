"""Auto-generated implementation for Plasma_Geometry.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:4

SysML Expressions:
    pi = 3.14159265358979
    V = 2.0 * pi ** 2 * R * a ** 2 * kappa
    
Documentation:
Plasma volume of an elongated torus [m^3].

  V = 2 * pi^2 * R * a^2 * kappa

Concept-agnostic geometry: applies to any toroidal MFE plasma
(tokamak or stellarator). R is major radius, a is minor radius,
kappa is elongation.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume)
*Basis**: Standard elongated-torus volume; MFE-generic
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.plasma_geometry import Plasma_GeometryInput


def run_plasma_geometry(inputs: Plasma_GeometryInput) -> float:
    """Execute Plasma_Geometry calculation.

Plasma volume of an elongated torus [m^3].

  V = 2 * pi^2 * R * a^2 * kappa

Concept-agnostic geometry: applies to any toroidal MFE plasma
(tokamak or stellarator). R is major radius, a is minor radius,
kappa is elongation.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume)
*Basis**: Standard elongated-torus volume; MFE-generic

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:4

SysML Expressions:
    pi = 3.14159265358979
    V = 2.0 * pi ** 2 * R * a ** 2 * kappa
    
Documentation:
Plasma volume of an elongated torus [m^3].

  V = 2 * pi^2 * R * a^2 * kappa

Concept-agnostic geometry: applies to any toroidal MFE plasma
(tokamak or stellarator). R is major radius, a is minor radius,
kappa is elongation.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:172-174 (_plasma_volume)
*Basis**: Standard elongated-torus volume; MFE-generic

Args:
    inputs: Input parameters validated against Plasma_GeometryInput schema

Returns:
    float: V

Example:
    >>> inputs = Plasma_GeometryInput(...)
    >>> result = run_plasma_geometry(inputs)
    """
    return ((((2.0 * (inputs.pi ** 2)) * inputs.R) * (inputs.a ** 2)) * inputs.kappa)
