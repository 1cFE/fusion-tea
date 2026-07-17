"""Auto-generated implementation for Neutron_Wall_Load.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:157

SysML Expressions:
    ash_frac = 0.2002
    wall_load = p_fus * (1.0 - ash_frac) / wall_area
    
Documentation:
First-wall neutron wall load [MW/m^2] from fusion power and wall area.

  wall_load = p_fus * (1 - ash_frac) / wall_area

The neutron power is the fusion power times the neutron energy fraction
(1 - ash_frac). ash_frac is the charged-particle (alpha/ash) share of the
D-T fusion energy: 0.2002 = E_alpha / Q = 3.52 MeV / 17.58 MeV. wall_load
is the neutron power divided by the load-bearing wall area, the standard
first-wall damage/lifetime driver. Concept-agnostic: any MFE first wall.

This makes neutron wall load forward-computable from the power balance
(p_fus) and the plasma/first-wall geometry (wall_area), so the viability
'Neutron Wall Load Limit' can be checked without an injected value.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:31 (E_ALPHA_DT=3.52, Q_DT=17.58), physics.py:177-179
(ash_frac = (E_total-E_neutron)/E_total; p_neutron = p_fus*(1-ash_frac))
*Basis**: Neutron wall load = neutron power / wall area; MFE-generic
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.neutron_wall_load import Neutron_Wall_LoadInput


def run_neutron_wall_load(inputs: Neutron_Wall_LoadInput) -> float:
    """Execute Neutron_Wall_Load calculation.

First-wall neutron wall load [MW/m^2] from fusion power and wall area.

  wall_load = p_fus * (1 - ash_frac) / wall_area

The neutron power is the fusion power times the neutron energy fraction
(1 - ash_frac). ash_frac is the charged-particle (alpha/ash) share of the
D-T fusion energy: 0.2002 = E_alpha / Q = 3.52 MeV / 17.58 MeV. wall_load
is the neutron power divided by the load-bearing wall area, the standard
first-wall damage/lifetime driver. Concept-agnostic: any MFE first wall.

This makes neutron wall load forward-computable from the power balance
(p_fus) and the plasma/first-wall geometry (wall_area), so the viability
'Neutron Wall Load Limit' can be checked without an injected value.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:31 (E_ALPHA_DT=3.52, Q_DT=17.58), physics.py:177-179
(ash_frac = (E_total-E_neutron)/E_total; p_neutron = p_fus*(1-ash_frac))
*Basis**: Neutron wall load = neutron power / wall area; MFE-generic

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:157

SysML Expressions:
    ash_frac = 0.2002
    wall_load = p_fus * (1.0 - ash_frac) / wall_area
    
Documentation:
First-wall neutron wall load [MW/m^2] from fusion power and wall area.

  wall_load = p_fus * (1 - ash_frac) / wall_area

The neutron power is the fusion power times the neutron energy fraction
(1 - ash_frac). ash_frac is the charged-particle (alpha/ash) share of the
D-T fusion energy: 0.2002 = E_alpha / Q = 3.52 MeV / 17.58 MeV. wall_load
is the neutron power divided by the load-bearing wall area, the standard
first-wall damage/lifetime driver. Concept-agnostic: any MFE first wall.

This makes neutron wall load forward-computable from the power balance
(p_fus) and the plasma/first-wall geometry (wall_area), so the viability
'Neutron Wall Load Limit' can be checked without an injected value.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/physics.py
*Ref**: physics.py:31 (E_ALPHA_DT=3.52, Q_DT=17.58), physics.py:177-179
(ash_frac = (E_total-E_neutron)/E_total; p_neutron = p_fus*(1-ash_frac))
*Basis**: Neutron wall load = neutron power / wall area; MFE-generic

Args:
    inputs: Input parameters validated against Neutron_Wall_LoadInput schema

Returns:
    float: wall_load

Example:
    >>> inputs = Neutron_Wall_LoadInput(...)
    >>> result = run_neutron_wall_load(inputs)
    """
    return ((inputs.p_fus * (1.0 - inputs.ash_frac)) / inputs.wall_area)
