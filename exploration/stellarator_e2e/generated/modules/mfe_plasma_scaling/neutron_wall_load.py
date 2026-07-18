"""Neutron_Wall_LoadModule Module Wrapper

TEAx module for Neutron_Wall_Load calculation.

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

Inputs:
    - p_fus: p_fus parameter
    - ash_frac: ash_frac parameter
    - wall_area: wall_area parameter

Outputs:
    - wall_load: wall_load result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:204

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:204

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/neutron_wall_load_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Neutron_Wall_LoadInput(BaseModel):
    """Input model for Neutron_Wall_LoadModule.

    Attributes:
        p_fus: p_fus input
        ash_frac: ash_frac input
        wall_area: wall_area input
    """
    p_fus: float = Field(..., description="p_fus input")
    ash_frac: float = Field(..., description="ash_frac input")
    wall_area: float = Field(..., description="wall_area input")


class Neutron_Wall_LoadModule(ModuleBase[Neutron_Wall_LoadInput, Float]):
    """TEAx module for Neutron_Wall_Load calculation.

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

Inputs:
    - p_fus: p_fus parameter
    - ash_frac: ash_frac parameter
    - wall_area: wall_area parameter

Outputs:
    - wall_load: wall_load result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:204

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:204

    Calculation Specification:
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

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.neutron_wall_load_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Neutron_Wall_LoadModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_fus: float, ash_frac: float, wall_area: float    ) -> Neutron_Wall_LoadInput:
        """Validate inputs and fill defaults.

        Args:
            p_fus: p_fus input
            ash_frac: ash_frac input
            wall_area: wall_area input

        Returns:
            Validated input model
        """
        return Neutron_Wall_LoadInput(p_fus=p_fus, ash_frac=ash_frac, wall_area=wall_area)

    def run(
        self, p_fus: float, ash_frac: float, wall_area: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            p_fus: p_fus input
            ash_frac: ash_frac input
            wall_area: wall_area input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_fus, ash_frac, wall_area)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.neutron_wall_load_impl import (
            run_neutron_wall_load,
        )

        # Execute implementation - returns single value
        wall_load = run_neutron_wall_load(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(wall_load))
