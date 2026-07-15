"""DT_Fusion_PowerModule Module Wrapper

TEAx module for DT_Fusion_Power calculation.

D-T fusion power [MW] from density, reactivity, and plasma volume.

  P_fus = (1/4) * n_e^2 * <sigma*v> * E_fus * V * 1e-6   [W -> MW]

The factor 1/4 = n_D*n_T / n_e^2 for a 50/50 D-T mix. Reactivity
<sigma*v> enters as the input `sigma_v` [m^3/s] — the Bosch-Hale
temperature fit is NOT reproduced here (it needs exp(), outside the
codegen envelope). E_fus is the per-event D-T fusion energy in Joules
(an input; = 17.58 MeV * 1.602176634e-13 J/MeV in the source).

Fusion power rises with n_e and with V (hence with R via 'Plasma
Geometry'), satisfying SV-017. Density and reactivity are inputs;
the machine -> density closure is a downstream design-layer concern.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:102-114 (compute_fusion_power)
*Basis**: Standard 0D D-T fusion power; MFE-generic

Inputs:
    - n_e: n_e parameter
    - sigma_v: sigma_v parameter
    - E_fus: E_fus parameter
    - V: V parameter

Outputs:
    - p_fus: p_fus result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:31

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:31

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class DT_Fusion_PowerInput(BaseModel):
    """Input model for DT_Fusion_PowerModule.

    Attributes:
        n_e: n_e input
        sigma_v: sigma_v input
        E_fus: E_fus input
        V: V input
    """
    n_e: float = Field(..., description="n_e input")
    sigma_v: float = Field(..., description="sigma_v input")
    E_fus: float = Field(..., description="E_fus input")
    V: float = Field(..., description="V input")


class DT_Fusion_PowerModule(ModuleBase[DT_Fusion_PowerInput, Float]):
    """TEAx module for DT_Fusion_Power calculation.

D-T fusion power [MW] from density, reactivity, and plasma volume.

  P_fus = (1/4) * n_e^2 * <sigma*v> * E_fus * V * 1e-6   [W -> MW]

The factor 1/4 = n_D*n_T / n_e^2 for a 50/50 D-T mix. Reactivity
<sigma*v> enters as the input `sigma_v` [m^3/s] — the Bosch-Hale
temperature fit is NOT reproduced here (it needs exp(), outside the
codegen envelope). E_fus is the per-event D-T fusion energy in Joules
(an input; = 17.58 MeV * 1.602176634e-13 J/MeV in the source).

Fusion power rises with n_e and with V (hence with R via 'Plasma
Geometry'), satisfying SV-017. Density and reactivity are inputs;
the machine -> density closure is a downstream design-layer concern.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:102-114 (compute_fusion_power)
*Basis**: Standard 0D D-T fusion power; MFE-generic

Inputs:
    - n_e: n_e parameter
    - sigma_v: sigma_v parameter
    - E_fus: E_fus parameter
    - V: V parameter

Outputs:
    - p_fus: p_fus result

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:31

    SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:31

    Calculation Specification:
        p_fus = 0.25 * n_e ** 2 * sigma_v * E_fus * V * 1e-06
        
Documentation:
D-T fusion power [MW] from density, reactivity, and plasma volume.

  P_fus = (1/4) * n_e^2 * <sigma*v> * E_fus * V * 1e-6   [W -> MW]

The factor 1/4 = n_D*n_T / n_e^2 for a 50/50 D-T mix. Reactivity
<sigma*v> enters as the input `sigma_v` [m^3/s] — the Bosch-Hale
temperature fit is NOT reproduced here (it needs exp(), outside the
codegen envelope). E_fus is the per-event D-T fusion energy in Joules
(an input; = 17.58 MeV * 1.602176634e-13 J/MeV in the source).

Fusion power rises with n_e and with V (hence with R via 'Plasma
Geometry'), satisfying SV-017. Density and reactivity are inputs;
the machine -> density closure is a downstream design-layer concern.

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py
*Ref**: tokamak.py:102-114 (compute_fusion_power)
*Basis**: Standard 0D D-T fusion power; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.dt_fusion_power_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "DT_Fusion_PowerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, n_e: float, sigma_v: float, E_fus: float, V: float    ) -> DT_Fusion_PowerInput:
        """Validate inputs and fill defaults.

        Args:
            n_e: n_e input
            sigma_v: sigma_v input
            E_fus: E_fus input
            V: V input

        Returns:
            Validated input model
        """
        return DT_Fusion_PowerInput(n_e=n_e, sigma_v=sigma_v, E_fus=E_fus, V=V)

    def run(
        self, n_e: float, sigma_v: float, E_fus: float, V: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            n_e: n_e input
            sigma_v: sigma_v input
            E_fus: E_fus input
            V: V input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(n_e, sigma_v, E_fus, V)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.dt_fusion_power_impl import (
            run_dt_fusion_power,
        )

        # Execute implementation - returns single value
        p_fus = run_dt_fusion_power(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(p_fus))
