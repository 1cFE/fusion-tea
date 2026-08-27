"""Auto-generated implementation for Volume_Averaged_Beta.

AUTO_IMPLEMENTED = True

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

SysML Expressions:
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
"""

AUTO_IMPLEMENTED = True

from stellarator_tea.modules.mfe_plasma_scaling.volume_averaged_beta import Volume_Averaged_BetaInput


def run_volume_averaged_beta(inputs: Volume_Averaged_BetaInput) -> float:
    """Execute Volume_Averaged_Beta calculation.

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

SysML Source: root-0/analyses/mfe_plasma_scaling.sysml:257

SysML Expressions:
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

Args:
    inputs: Input parameters validated against Volume_Averaged_BetaInput schema

Returns:
    float: beta

Example:
    >>> inputs = Volume_Averaged_BetaInput(...)
    >>> result = run_volume_averaged_beta(inputs)
    """
    p_fuel = (((inputs.n_D0_in + inputs.n_T0_in) * inputs.T_i0_in) / ((1.0 + inputs.alpha_n_in) + inputs.alpha_T_in))
    p_He = ((inputs.n_He0_in * inputs.T_i0_in) / ((1.0 + inputs.alpha_n_in) + inputs.alpha_T_in))
    p_e = ((inputs.n_e0_in * inputs.T_e0_in) / ((1.0 + inputs.alpha_n_e_in) + inputs.alpha_T_in))
    p_avg = (((p_e + p_fuel) + p_He) * inputs.e_keV)
    return (((2.0 * inputs.mu0) * p_avg) / (inputs.B_in ** 2))
