"""DT_Fusion_PowerModule Module Wrapper

TEAx module for DT_Fusion_Power calculation.

D-T fusion power [MW] — 0D bypass or profile-integrated (WI-022).

MODE (bypass rule, selected by sigma_v alone):
  sigma_v > 0  ->  0D form (exact legacy contract):
      p_fus = 0.25 * n_e^2 * sigma_v * E_fus * V * 1e-6   [W -> MW]
  sigma_v = 0 (default)  ->  profile-integrated form:
      p_fus = n_D0 * n_T0 * I * E_fus * V * 1e-6
      I = integral_0^1  u^(2*alpha_n) * sigv_dt(T_i0 * u^alpha_T) du
  with u = 1 - rho^2 (dV/V = 2*rho*d(rho), so the rho-integral of the
  profile product reduces to the u-integral above), profiles
  n(rho) = n0*(1-rho^2)^alpha_n and T(rho) = T0*(1-rho^2)^alpha_T
  (Stellaris Eqs. 2-3, image-verified). The fuel term is n_D*n_T with
  the *diluted peak fuel densities* — NOT 0.25*n_e^2, which would
  double-count helium ash and impurities. If sigma_v > 0 and profile
  inputs are also bound, the bypass wins.

EXECUTABLE SEMANTIC (Rung B, WI-022): the Bosch-Hale curve needs
exp(), so this calc is routed to the handwritten codegen stage
(manual_required); the generated handwritten impl is normative and is
guarded bit-exact by the oracle (verify_stellaris.py). Discretization
contract for the impl and oracle: trapezoidal rule in rho over [0,1],
N = 200,000 intervals, temperature floor 1e-6 keV, pure-Python
float64. The intermediates below state the Bosch-Hale evaluation at
T_i0 (sigv_peak) in the model itself; e^x is written as e ** x
because the KerML standard library has sqrt but no exp.

Fusion power rises with n_e / the fuel densities and with V (hence
with R via 'Plasma Geometry'), satisfying SV-017. Densities,
temperature, and exponents are inputs; the machine -> profile closure
(ISS04 confinement solve) is out of scope (Rung C).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py;
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py
*Ref**: tokamak.py:102-114 (compute_fusion_power, the 0D bypass
form); reactivity.py:54-70 (sigv_dt Bosch-Hale D-T coefficients);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/
stellaris-design-details/images/page_007_eq_0.png and
page_007_eq_1.png (Eqs. 2-3 profile forms, image-verified);
stellaris-design-details.md Appendix A line 2912 (the source's own
0.5D volume-integrated power balance this reproduces)
*Basis**: profile-integrated D-T fusion power over (1-rho^2)^alpha
profiles with an exact 0D bypass; MFE-generic (flat/0D concepts
bind sigma_v > 0 and ignore the profile inputs)

Inputs:
    - n_e: n_e parameter
    - sigma_v: sigma_v parameter
    - E_fus: E_fus parameter
    - V: V parameter
    - n_D0: n_D0 parameter
    - n_T0: n_T0 parameter
    - T_i0: T_i0 parameter
    - alpha_n: alpha_n parameter
    - alpha_T: alpha_T parameter

Outputs:
    - p_fus: p_fus result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:125

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:125

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
        n_D0: n_D0 input
        n_T0: n_T0 input
        T_i0: T_i0 input
        alpha_n: alpha_n input
        alpha_T: alpha_T input
    """
    n_e: float = Field(..., description="n_e input")
    sigma_v: float = Field(..., description="sigma_v input")
    E_fus: float = Field(..., description="E_fus input")
    V: float = Field(..., description="V input")
    n_D0: float = Field(..., description="n_D0 input")
    n_T0: float = Field(..., description="n_T0 input")
    T_i0: float = Field(..., description="T_i0 input")
    alpha_n: float = Field(..., description="alpha_n input")
    alpha_T: float = Field(..., description="alpha_T input")


class DT_Fusion_PowerModule(ModuleBase[DT_Fusion_PowerInput, Float]):
    """TEAx module for DT_Fusion_Power calculation.

D-T fusion power [MW] — 0D bypass or profile-integrated (WI-022).

MODE (bypass rule, selected by sigma_v alone):
  sigma_v > 0  ->  0D form (exact legacy contract):
      p_fus = 0.25 * n_e^2 * sigma_v * E_fus * V * 1e-6   [W -> MW]
  sigma_v = 0 (default)  ->  profile-integrated form:
      p_fus = n_D0 * n_T0 * I * E_fus * V * 1e-6
      I = integral_0^1  u^(2*alpha_n) * sigv_dt(T_i0 * u^alpha_T) du
  with u = 1 - rho^2 (dV/V = 2*rho*d(rho), so the rho-integral of the
  profile product reduces to the u-integral above), profiles
  n(rho) = n0*(1-rho^2)^alpha_n and T(rho) = T0*(1-rho^2)^alpha_T
  (Stellaris Eqs. 2-3, image-verified). The fuel term is n_D*n_T with
  the *diluted peak fuel densities* — NOT 0.25*n_e^2, which would
  double-count helium ash and impurities. If sigma_v > 0 and profile
  inputs are also bound, the bypass wins.

EXECUTABLE SEMANTIC (Rung B, WI-022): the Bosch-Hale curve needs
exp(), so this calc is routed to the handwritten codegen stage
(manual_required); the generated handwritten impl is normative and is
guarded bit-exact by the oracle (verify_stellaris.py). Discretization
contract for the impl and oracle: trapezoidal rule in rho over [0,1],
N = 200,000 intervals, temperature floor 1e-6 keV, pure-Python
float64. The intermediates below state the Bosch-Hale evaluation at
T_i0 (sigv_peak) in the model itself; e^x is written as e ** x
because the KerML standard library has sqrt but no exp.

Fusion power rises with n_e / the fuel densities and with V (hence
with R via 'Plasma Geometry'), satisfying SV-017. Densities,
temperature, and exponents are inputs; the machine -> profile closure
(ISS04 confinement solve) is out of scope (Rung C).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py;
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py
*Ref**: tokamak.py:102-114 (compute_fusion_power, the 0D bypass
form); reactivity.py:54-70 (sigv_dt Bosch-Hale D-T coefficients);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/
stellaris-design-details/images/page_007_eq_0.png and
page_007_eq_1.png (Eqs. 2-3 profile forms, image-verified);
stellaris-design-details.md Appendix A line 2912 (the source's own
0.5D volume-integrated power balance this reproduces)
*Basis**: profile-integrated D-T fusion power over (1-rho^2)^alpha
profiles with an exact 0D bypass; MFE-generic (flat/0D concepts
bind sigma_v > 0 and ignore the profile inputs)

Inputs:
    - n_e: n_e parameter
    - sigma_v: sigma_v parameter
    - E_fus: E_fus parameter
    - V: V parameter
    - n_D0: n_D0 parameter
    - n_T0: n_T0 parameter
    - T_i0: T_i0 parameter
    - alpha_n: alpha_n parameter
    - alpha_T: alpha_T parameter

Outputs:
    - p_fus: p_fus result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:125

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:125

    Calculation Specification:
        sigma_v = 0.0
        n_D0 = 0.0
        n_T0 = 0.0
        T_i0 = 1.0
        alpha_n = 0.0
        alpha_T = 0.0
        theta = T_i0 / (1.0 - T_i0 * (0.0151361 + T_i0 * (0.00460643 + T_i0 * -0.00010675)) / (1.0 + T_i0 * (0.0751886 + T_i0 * (0.0135 + T_i0 * 1.366e-05))))
        xi = (34.3827 * 34.3827 / (4.0 * theta)) ** (1.0 / 3.0)
        sigv_peak = 1.17302e-09 * theta * sqrt(xi / (1124656.0 * T_i0 ** 3)) * 2.718281828459045 ** (-3.0 * xi) * 1e-06
        p_fus = n_D0 * n_T0 * sigv_peak * E_fus * V * 1e-06
        
Documentation:
D-T fusion power [MW] — 0D bypass or profile-integrated (WI-022).

MODE (bypass rule, selected by sigma_v alone):
  sigma_v > 0  ->  0D form (exact legacy contract):
      p_fus = 0.25 * n_e^2 * sigma_v * E_fus * V * 1e-6   [W -> MW]
  sigma_v = 0 (default)  ->  profile-integrated form:
      p_fus = n_D0 * n_T0 * I * E_fus * V * 1e-6
      I = integral_0^1  u^(2*alpha_n) * sigv_dt(T_i0 * u^alpha_T) du
  with u = 1 - rho^2 (dV/V = 2*rho*d(rho), so the rho-integral of the
  profile product reduces to the u-integral above), profiles
  n(rho) = n0*(1-rho^2)^alpha_n and T(rho) = T0*(1-rho^2)^alpha_T
  (Stellaris Eqs. 2-3, image-verified). The fuel term is n_D*n_T with
  the *diluted peak fuel densities* — NOT 0.25*n_e^2, which would
  double-count helium ash and impurities. If sigma_v > 0 and profile
  inputs are also bound, the bypass wins.

EXECUTABLE SEMANTIC (Rung B, WI-022): the Bosch-Hale curve needs
exp(), so this calc is routed to the handwritten codegen stage
(manual_required); the generated handwritten impl is normative and is
guarded bit-exact by the oracle (verify_stellaris.py). Discretization
contract for the impl and oracle: trapezoidal rule in rho over [0,1],
N = 200,000 intervals, temperature floor 1e-6 keV, pure-Python
float64. The intermediates below state the Bosch-Hale evaluation at
T_i0 (sigv_peak) in the model itself; e^x is written as e ** x
because the KerML standard library has sqrt but no exp.

Fusion power rises with n_e / the fuel densities and with V (hence
with R via 'Plasma Geometry'), satisfying SV-017. Densities,
temperature, and exponents are inputs; the machine -> profile closure
(ISS04 confinement solve) is out of scope (Rung C).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py;
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py
*Ref**: tokamak.py:102-114 (compute_fusion_power, the 0D bypass
form); reactivity.py:54-70 (sigv_dt Bosch-Hale D-T coefficients);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/
stellaris-design-details/images/page_007_eq_0.png and
page_007_eq_1.png (Eqs. 2-3 profile forms, image-verified);
stellaris-design-details.md Appendix A line 2912 (the source's own
0.5D volume-integrated power balance this reproduces)
*Basis**: profile-integrated D-T fusion power over (1-rho^2)^alpha
profiles with an exact 0D bypass; MFE-generic (flat/0D concepts
bind sigma_v > 0 and ignore the profile inputs)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.dt_fusion_power_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "DT_Fusion_PowerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, n_e: float, sigma_v: float, E_fus: float, V: float, n_D0: float, n_T0: float, T_i0: float, alpha_n: float, alpha_T: float    ) -> DT_Fusion_PowerInput:
        """Validate inputs and fill defaults.

        Args:
            n_e: n_e input
            sigma_v: sigma_v input
            E_fus: E_fus input
            V: V input
            n_D0: n_D0 input
            n_T0: n_T0 input
            T_i0: T_i0 input
            alpha_n: alpha_n input
            alpha_T: alpha_T input

        Returns:
            Validated input model
        """
        return DT_Fusion_PowerInput(n_e=n_e, sigma_v=sigma_v, E_fus=E_fus, V=V, n_D0=n_D0, n_T0=n_T0, T_i0=T_i0, alpha_n=alpha_n, alpha_T=alpha_T)

    def run(
        self, n_e: float, sigma_v: float, E_fus: float, V: float, n_D0: float, n_T0: float, T_i0: float, alpha_n: float, alpha_T: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            n_e: n_e input
            sigma_v: sigma_v input
            E_fus: E_fus input
            V: V input
            n_D0: n_D0 input
            n_T0: n_T0 input
            T_i0: T_i0 input
            alpha_n: alpha_n input
            alpha_T: alpha_T input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(n_e, sigma_v, E_fus, V, n_D0, n_T0, T_i0, alpha_n, alpha_T)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.dt_fusion_power_impl import (
            run_dt_fusion_power,
        )

        # Execute implementation - returns single value
        p_fus = run_dt_fusion_power(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(p_fus))
