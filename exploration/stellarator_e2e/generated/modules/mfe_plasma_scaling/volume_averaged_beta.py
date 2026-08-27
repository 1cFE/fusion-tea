"""Volume_Averaged_BetaModule Module Wrapper

TEAx module for Volume_Averaged_Beta calculation.

Volume-averaged thermal plasma beta [1] from peak densities, peak
temperatures, profile exponents, and the axis-averaged field (WI-030).

  beta = 2 * mu0 * <p> / B^2
  <p>  = e_keV * Sigma_s n_s0 * T_s0 / (1 + alpha_n,s + alpha_T)   [Pa]

over s in {electrons, D, T, He ash}: ions at T_i0, electrons at T_e0;
fuel and ash share alpha_n, electrons carry alpha_n_e, one alpha_T for
all species. The 1/(1 + alpha_n + alpha_T) factor is the volume average
of (1-rho^2)^(alpha_n+alpha_T) over dV/V = 2*rho*d(rho) -- the same
u = 1 - rho^2 substitution 'DT Fusion Power' documents. Thermal only:
fast-particle pressure is excluded, so the value sits a few percent
under a source's printed equilibrium beta.

Concept-agnostic: any MFE instance with (1-rho^2)^alpha profiles binds
its own peaks and exponents; B enters the physics here, not only the
magnet cost (mfe_magnet_cost.sysml).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: tokamak.py:36-40 (_EV exact, KEV_TO_J; MU_0 1.25663706127e-6 --
this calc keeps the model's 1.25663706212e-6 from mfe_magnet_cost.sysml:41,
7e-10 apart); tokamak.py:117-126 (compute_beta_N: electron + ion pressure
over B^2 -- NOTE its mu0*n_e*(T_e + n_i T_i)/B^2 is half the standard
2*mu0*p/B^2 used here; the printed Stellaris 2.76 % validates the
standard form); images/page_007_eq_0.png, page_007_eq_1.png (Eqs. 2-3
profile forms); images/page_009_table_0.png (Table 5: vol. av. beta
2.76 % / 2.81 %, the cross-check)
*Basis**: beta = 2*mu0*<p>/B^2 with <p> the volume-averaged thermal
pressure of all species over (1-rho^2)^alpha profiles; MFE-generic

Inputs:
    - n_D0_in: n_D0_in parameter
    - mu0: mu0 parameter
    - alpha_n_in: alpha_n_in parameter
    - T_e0_in: T_e0_in parameter
    - alpha_n_e_in: alpha_n_e_in parameter
    - n_He0_in: n_He0_in parameter
    - alpha_T_in: alpha_T_in parameter
    - T_i0_in: T_i0_in parameter
    - e_keV: e_keV parameter
    - B_in: B_in parameter
    - n_e0_in: n_e0_in parameter
    - n_T0_in: n_T0_in parameter

Outputs:
    - beta: beta result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_scaling/volume_averaged_beta_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float


class Volume_Averaged_BetaInput(BaseModel):
    """Input model for Volume_Averaged_BetaModule.

    Attributes:
        n_D0_in: n_D0_in input
        mu0: mu0 input
        alpha_n_in: alpha_n_in input
        T_e0_in: T_e0_in input
        alpha_n_e_in: alpha_n_e_in input
        n_He0_in: n_He0_in input
        alpha_T_in: alpha_T_in input
        T_i0_in: T_i0_in input
        e_keV: e_keV input
        B_in: B_in input
        n_e0_in: n_e0_in input
        n_T0_in: n_T0_in input
    """
    n_D0_in: float = Field(..., description="n_D0_in input")
    mu0: float = Field(..., description="mu0 input")
    alpha_n_in: float = Field(..., description="alpha_n_in input")
    T_e0_in: float = Field(..., description="T_e0_in input")
    alpha_n_e_in: float = Field(..., description="alpha_n_e_in input")
    n_He0_in: float = Field(..., description="n_He0_in input")
    alpha_T_in: float = Field(..., description="alpha_T_in input")
    T_i0_in: float = Field(..., description="T_i0_in input")
    e_keV: float = Field(..., description="e_keV input")
    B_in: float = Field(..., description="B_in input")
    n_e0_in: float = Field(..., description="n_e0_in input")
    n_T0_in: float = Field(..., description="n_T0_in input")


class Volume_Averaged_BetaModule(ModuleBase[Volume_Averaged_BetaInput, Float]):
    """TEAx module for Volume_Averaged_Beta calculation.

Volume-averaged thermal plasma beta [1] from peak densities, peak
temperatures, profile exponents, and the axis-averaged field (WI-030).

  beta = 2 * mu0 * <p> / B^2
  <p>  = e_keV * Sigma_s n_s0 * T_s0 / (1 + alpha_n,s + alpha_T)   [Pa]

over s in {electrons, D, T, He ash}: ions at T_i0, electrons at T_e0;
fuel and ash share alpha_n, electrons carry alpha_n_e, one alpha_T for
all species. The 1/(1 + alpha_n + alpha_T) factor is the volume average
of (1-rho^2)^(alpha_n+alpha_T) over dV/V = 2*rho*d(rho) -- the same
u = 1 - rho^2 substitution 'DT Fusion Power' documents. Thermal only:
fast-particle pressure is excluded, so the value sits a few percent
under a source's printed equilibrium beta.

Concept-agnostic: any MFE instance with (1-rho^2)^alpha profiles binds
its own peaks and exponents; B enters the physics here, not only the
magnet cost (mfe_magnet_cost.sysml).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: tokamak.py:36-40 (_EV exact, KEV_TO_J; MU_0 1.25663706127e-6 --
this calc keeps the model's 1.25663706212e-6 from mfe_magnet_cost.sysml:41,
7e-10 apart); tokamak.py:117-126 (compute_beta_N: electron + ion pressure
over B^2 -- NOTE its mu0*n_e*(T_e + n_i T_i)/B^2 is half the standard
2*mu0*p/B^2 used here; the printed Stellaris 2.76 % validates the
standard form); images/page_007_eq_0.png, page_007_eq_1.png (Eqs. 2-3
profile forms); images/page_009_table_0.png (Table 5: vol. av. beta
2.76 % / 2.81 %, the cross-check)
*Basis**: beta = 2*mu0*<p>/B^2 with <p> the volume-averaged thermal
pressure of all species over (1-rho^2)^alpha profiles; MFE-generic

Inputs:
    - n_D0_in: n_D0_in parameter
    - mu0: mu0 parameter
    - alpha_n_in: alpha_n_in parameter
    - T_e0_in: T_e0_in parameter
    - alpha_n_e_in: alpha_n_e_in parameter
    - n_He0_in: n_He0_in parameter
    - alpha_T_in: alpha_T_in parameter
    - T_i0_in: T_i0_in parameter
    - e_keV: e_keV parameter
    - B_in: B_in parameter
    - n_e0_in: n_e0_in parameter
    - n_T0_in: n_T0_in parameter

Outputs:
    - beta: beta result

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

    SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

    Calculation Specification:
        mu0 = 1.25663706212e-06
        e_keV = 1.602176634e-16
        p_e = n_e0_in * T_e0_in / (1.0 + alpha_n_e_in + alpha_T_in)
        p_fuel = (n_D0_in + n_T0_in) * T_i0_in / (1.0 + alpha_n_in + alpha_T_in)
        p_He = n_He0_in * T_i0_in / (1.0 + alpha_n_in + alpha_T_in)
        p_avg = (p_e + p_fuel + p_He) * e_keV
        beta = 2.0 * mu0 * p_avg / B_in ** 2
        
Documentation:
Volume-averaged thermal plasma beta [1] from peak densities, peak
temperatures, profile exponents, and the axis-averaged field (WI-030).

  beta = 2 * mu0 * <p> / B^2
  <p>  = e_keV * Sigma_s n_s0 * T_s0 / (1 + alpha_n,s + alpha_T)   [Pa]

over s in {electrons, D, T, He ash}: ions at T_i0, electrons at T_e0;
fuel and ash share alpha_n, electrons carry alpha_n_e, one alpha_T for
all species. The 1/(1 + alpha_n + alpha_T) factor is the volume average
of (1-rho^2)^(alpha_n+alpha_T) over dV/V = 2*rho*d(rho) -- the same
u = 1 - rho^2 substitution 'DT Fusion Power' documents. Thermal only:
fast-particle pressure is excluded, so the value sits a few percent
under a source's printed equilibrium beta.

Concept-agnostic: any MFE instance with (1-rho^2)^alpha profiles binds
its own peaks and exponents; B enters the physics here, not only the
magnet cost (mfe_magnet_cost.sysml).

*Source**: /home/reid/1cfe/1costingfe/src/costingfe/layers/tokamak.py (pin 0254385);
knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
*Ref**: tokamak.py:36-40 (_EV exact, KEV_TO_J; MU_0 1.25663706127e-6 --
this calc keeps the model's 1.25663706212e-6 from mfe_magnet_cost.sysml:41,
7e-10 apart); tokamak.py:117-126 (compute_beta_N: electron + ion pressure
over B^2 -- NOTE its mu0*n_e*(T_e + n_i T_i)/B^2 is half the standard
2*mu0*p/B^2 used here; the printed Stellaris 2.76 % validates the
standard form); images/page_007_eq_0.png, page_007_eq_1.png (Eqs. 2-3
profile forms); images/page_009_table_0.png (Table 5: vol. av. beta
2.76 % / 2.81 %, the cross-check)
*Basis**: beta = 2*mu0*<p>/B^2 with <p> the volume-averaged thermal
pressure of all species over (1-rho^2)^alpha profiles; MFE-generic

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_scaling.volume_averaged_beta_impl
    for manual implementation.

    NOTE: Single-output module - returns Float directly (no MultiOutput needed).
    """

    name: str = "Volume_Averaged_BetaModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, n_D0_in: float, mu0: float, alpha_n_in: float, T_e0_in: float, alpha_n_e_in: float, n_He0_in: float, alpha_T_in: float, T_i0_in: float, e_keV: float, B_in: float, n_e0_in: float, n_T0_in: float    ) -> Volume_Averaged_BetaInput:
        """Validate inputs and fill defaults.

        Args:
            n_D0_in: n_D0_in input
            mu0: mu0 input
            alpha_n_in: alpha_n_in input
            T_e0_in: T_e0_in input
            alpha_n_e_in: alpha_n_e_in input
            n_He0_in: n_He0_in input
            alpha_T_in: alpha_T_in input
            T_i0_in: T_i0_in input
            e_keV: e_keV input
            B_in: B_in input
            n_e0_in: n_e0_in input
            n_T0_in: n_T0_in input

        Returns:
            Validated input model
        """
        return Volume_Averaged_BetaInput(n_D0_in=n_D0_in, mu0=mu0, alpha_n_in=alpha_n_in, T_e0_in=T_e0_in, alpha_n_e_in=alpha_n_e_in, n_He0_in=n_He0_in, alpha_T_in=alpha_T_in, T_i0_in=T_i0_in, e_keV=e_keV, B_in=B_in, n_e0_in=n_e0_in, n_T0_in=n_T0_in)

    def run(
        self, n_D0_in: float, mu0: float, alpha_n_in: float, T_e0_in: float, alpha_n_e_in: float, n_He0_in: float, alpha_T_in: float, T_i0_in: float, e_keV: float, B_in: float, n_e0_in: float, n_T0_in: float    ) -> ModuleResult[Float]:
        """Execute calculation.

        Args:
            n_D0_in: n_D0_in input
            mu0: mu0 input
            alpha_n_in: alpha_n_in input
            T_e0_in: T_e0_in input
            alpha_n_e_in: alpha_n_e_in input
            n_He0_in: n_He0_in input
            alpha_T_in: alpha_T_in input
            T_i0_in: T_i0_in input
            e_keV: e_keV input
            B_in: B_in input
            n_e0_in: n_e0_in input
            n_T0_in: n_T0_in input

        Returns:
            Module result with Float (single-output mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(n_D0_in, mu0, alpha_n_in, T_e0_in, alpha_n_e_in, n_He0_in, alpha_T_in, T_i0_in, e_keV, B_in, n_e0_in, n_T0_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_scaling.volume_averaged_beta_impl import (
            run_volume_averaged_beta,
        )

        # Execute implementation - returns single value
        beta = run_volume_averaged_beta(validated_inputs)

        # Single output - return Float directly (RootModel[float])
        # TEAx assigns entire return value to the one channel declared in YAML
        return ModuleResult(data=Float(beta))
