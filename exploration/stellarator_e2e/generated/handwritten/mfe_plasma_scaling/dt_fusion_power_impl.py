"""Auto-generated implementation for DT_Fusion_Power.

AUTO_IMPLEMENTED = True

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:31

SysML Expressions:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.dt_fusion_power import DT_Fusion_PowerInput


def run_dt_fusion_power(inputs: DT_Fusion_PowerInput) -> float:
    """Execute DT_Fusion_Power calculation.

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

SysML Source: /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/models/analyses/mfe_plasma_scaling.sysml:31

SysML Expressions:
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

Args:
    inputs: Input parameters validated against DT_Fusion_PowerInput schema

Returns:
    float: p_fus

Example:
    >>> inputs = DT_Fusion_PowerInput(...)
    >>> result = run_dt_fusion_power(inputs)
    """
    return (((((0.25 * (inputs.n_e ** 2)) * inputs.sigma_v) * inputs.E_fus) * inputs.V) * 1e-06)
