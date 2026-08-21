"""DT_Fusion_PowerModule Module Wrapper

TEAx module for DT_Fusion_Power calculation.

D-T fusion power [MW] -- 0D bypass or profile-integrated (WI-022).

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
  the *diluted peak fuel densities* -- NOT 0.25*n_e^2, which would
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

EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
marked for revert -- see models/stellarator_migration_ledger.md): the
pinned codegen admits no function invocation in an executable
expression, so the model-resident Bosch-Hale peak statement that used
to sit in the body is carried here verbatim and the output is declared
without an expression (a manual interface; the handwritten impl above
is the executable meaning either way):
  theta     = T_i0 / (1 - T_i0*(1.51361e-2 + T_i0*(4.60643e-3 + T_i0*-1.06750e-4))
                     / (1 + T_i0*(7.51886e-2 + T_i0*(1.35000e-2 + T_i0*1.36600e-5))))
  xi        = ((34.3827^2) / (4*theta))^(1/3)
  sigv_peak = 1.17302e-9 * theta * sqrt(xi / (1124656 * T_i0^3)) * e^(-3*xi) * 1e-6
  p_fus     = n_D0 * n_T0 * sigv_peak * E_fus * V * 1e-6     (peak-form statement)

Inputs:
    - n_T0_in: n_T0_in parameter
    - n_e_in: n_e_in parameter
    - T_i0_in: T_i0_in parameter
    - V: V parameter
    - E_fus_in: E_fus_in parameter
    - sigma_v_in: sigma_v_in parameter
    - n_D0_in: n_D0_in parameter
    - alpha_T_in: alpha_T_in parameter
    - alpha_n_in: alpha_n_in parameter

Outputs:
    - p_fus: p_fus result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:132

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:132

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class DT_Fusion_PowerInput(BaseModel):
    """Input model for DT_Fusion_PowerModule.

    Attributes:
        n_T0_in: n_T0_in input
        n_e_in: n_e_in input
        T_i0_in: T_i0_in input
        V: V input
        E_fus_in: E_fus_in input
        sigma_v_in: sigma_v_in input
        n_D0_in: n_D0_in input
        alpha_T_in: alpha_T_in input
        alpha_n_in: alpha_n_in input
    """
    n_T0_in: float = Field(..., description="n_T0_in input")
    n_e_in: float = Field(..., description="n_e_in input")
    T_i0_in: float = Field(..., description="T_i0_in input")
    V: float = Field(..., description="V input")
    E_fus_in: float = Field(..., description="E_fus_in input")
    sigma_v_in: float = Field(..., description="sigma_v_in input")
    n_D0_in: float = Field(..., description="n_D0_in input")
    alpha_T_in: float = Field(..., description="alpha_T_in input")
    alpha_n_in: float = Field(..., description="alpha_n_in input")


class DT_Fusion_PowerModule(ModuleBase[DT_Fusion_PowerInput, Float]):
    """TEAx module for DT_Fusion_Power calculation.

D-T fusion power [MW] -- 0D bypass or profile-integrated (WI-022).

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
  the *diluted peak fuel densities* -- NOT 0.25*n_e^2, which would
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

EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
marked for revert -- see models/stellarator_migration_ledger.md): the
pinned codegen admits no function invocation in an executable
expression, so the model-resident Bosch-Hale peak statement that used
to sit in the body is carried here verbatim and the output is declared
without an expression (a manual interface; the handwritten impl above
is the executable meaning either way):
  theta     = T_i0 / (1 - T_i0*(1.51361e-2 + T_i0*(4.60643e-3 + T_i0*-1.06750e-4))
                     / (1 + T_i0*(7.51886e-2 + T_i0*(1.35000e-2 + T_i0*1.36600e-5))))
  xi        = ((34.3827^2) / (4*theta))^(1/3)
  sigv_peak = 1.17302e-9 * theta * sqrt(xi / (1124656 * T_i0^3)) * e^(-3*xi) * 1e-6
  p_fus     = n_D0 * n_T0 * sigv_peak * E_fus * V * 1e-6     (peak-form statement)

Inputs:
    - n_T0_in: n_T0_in parameter
    - n_e_in: n_e_in parameter
    - T_i0_in: T_i0_in parameter
    - V: V parameter
    - E_fus_in: E_fus_in parameter
    - sigma_v_in: sigma_v_in parameter
    - n_D0_in: n_D0_in parameter
    - alpha_T_in: alpha_T_in parameter
    - alpha_n_in: alpha_n_in parameter

Outputs:
    - p_fus: p_fus result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:132

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:132

    Calculation Specification:
        sigma_v_in = 0.0
        n_D0_in = 0.0
        n_T0_in = 0.0
        T_i0_in = 1.0
        alpha_n_in = 0.0
        alpha_T_in = 0.0
        
Documentation:
D-T fusion power [MW] -- 0D bypass or profile-integrated (WI-022).

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
  the *diluted peak fuel densities* -- NOT 0.25*n_e^2, which would
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

EXACT-ROUTE FORM (stellarator-model-migration, 2026-08-21; Class B,
marked for revert -- see models/stellarator_migration_ledger.md): the
pinned codegen admits no function invocation in an executable
expression, so the model-resident Bosch-Hale peak statement that used
to sit in the body is carried here verbatim and the output is declared
without an expression (a manual interface; the handwritten impl above
is the executable meaning either way):
  theta     = T_i0 / (1 - T_i0*(1.51361e-2 + T_i0*(4.60643e-3 + T_i0*-1.06750e-4))
                     / (1 + T_i0*(7.51886e-2 + T_i0*(1.35000e-2 + T_i0*1.36600e-5))))
  xi        = ((34.3827^2) / (4*theta))^(1/3)
  sigv_peak = 1.17302e-9 * theta * sqrt(xi / (1124656 * T_i0^3)) * e^(-3*xi) * 1e-6
  p_fus     = n_D0 * n_T0 * sigv_peak * E_fus * V * 1e-6     (peak-form statement)

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.dt_fusion_power_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "DT_Fusion_PowerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, n_T0_in: float, n_e_in: float, T_i0_in: float, V: float, E_fus_in: float, sigma_v_in: float, n_D0_in: float, alpha_T_in: float, alpha_n_in: float    ) -> DT_Fusion_PowerInput:
        """Validate inputs and fill defaults.

        Args:
            n_T0_in: n_T0_in input
            n_e_in: n_e_in input
            T_i0_in: T_i0_in input
            V: V input
            E_fus_in: E_fus_in input
            sigma_v_in: sigma_v_in input
            n_D0_in: n_D0_in input
            alpha_T_in: alpha_T_in input
            alpha_n_in: alpha_n_in input

        Returns:
            Validated input model
        """
        return DT_Fusion_PowerInput(n_T0_in=n_T0_in, n_e_in=n_e_in, T_i0_in=T_i0_in, V=V, E_fus_in=E_fus_in, sigma_v_in=sigma_v_in, n_D0_in=n_D0_in, alpha_T_in=alpha_T_in, alpha_n_in=alpha_n_in)

    def run(
        self, n_T0_in: float, n_e_in: float, T_i0_in: float, V: float, E_fus_in: float, sigma_v_in: float, n_D0_in: float, alpha_T_in: float, alpha_n_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            n_T0_in: n_T0_in input
            n_e_in: n_e_in input
            T_i0_in: T_i0_in input
            V: V input
            E_fus_in: E_fus_in input
            sigma_v_in: sigma_v_in input
            n_D0_in: n_D0_in input
            alpha_T_in: alpha_T_in input
            alpha_n_in: alpha_n_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(n_T0_in, n_e_in, T_i0_in, V, E_fus_in, sigma_v_in, n_D0_in, alpha_T_in, alpha_n_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.dt_fusion_power_impl import (
            run_dt_fusion_power,
        )

        # Execute implementation - returns single value
        p_fus = run_dt_fusion_power(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(p_fus))
