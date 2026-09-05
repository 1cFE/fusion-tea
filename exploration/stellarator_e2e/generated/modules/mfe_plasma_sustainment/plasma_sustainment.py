"""Plasma_SustainmentModule Module Wrapper

TEAx module for Plasma_Sustainment calculation.

Operating-point sustainment chain (WI-037; profiles WI-042): from the
machine (a, R, iota_2/3, axis field B), the operating-point levers
(peak electron density n_e0, peak ion temperature T_i0), and installed
physics facts, compute the required sustained plasma-coupled heating
power and the forward ash/fuel state. Temperature and density remain
design levers; the machine pushes back through the paired
'Sustainment Limit' (mfe_viability.sysml) on the computed
p_aux_required.

PROFILES (Stellaris Eqs. 2-3 and the source's own ash rule; WI-042):
  u        = 1 - rho^2;  dV/V = 2 rho d(rho)
  T_i(rho) = T_i0 * u^alpha_T;   T_e(rho) = T_e0 * u^alpha_T
  n_D(rho) = n_T(rho) = n_D0 * u^alpha_n           (the fuel exponent)
  S(rho)   = u^(2 alpha_n) * sigv_dt(T_i(rho)) / sigv_dt(T_i0)
             (the fusion-rate shape, S(0) = 1)
  n_He(rho) = n_He0 * S(rho)
             -- Eq. A.5 applied pointwise with the particle-to-energy
             confinement ratio uniform in rho ("helium ash profiles are
             obtained using a fixed ratio of particle-to-energy
             confinement time", raw PDF p. 9): the ash follows the
             fusion-rate profile, scaled to the converged peak below.
             NEVER a bound exponent -- the shape is computed from the
             rule at every lever point, so it holds for any geometry
             [OWNER 2026-09-05: "make sure this scales up for larger
             stellarators"].
  n_e(rho) = n_D + n_T + 2 n_He = 2 n_D0 u^alpha_n + 2 n_He0 S(rho)
             (quasi-neutrality pointwise; trace W at f_W ~ 1e-5
             neglected in the charge sum; n_e(0) = n_e0, the lever)

CHAIN (each stage an output; all evaluated at the same lever point):

  T_e0     = T_i0 / r_TiTe                                  [keV]
  I_line_n = integral_0^1 u^alpha_n d rho
  I_line_S = integral_0^1 S(rho) d rho
  I_W_S    = integral_0^1 S(rho) u^alpha_T 2 rho d rho   ( = <S u^alpha_T>_V )
  I_vol_S  = integral_0^1 S(rho) 2 rho d rho             ( = <S>_V )
  n_bar19  = (2 n_D0 I_line_n + 2 n_He0 I_line_S) / 1e19  [1e19 m^-3]
             (line-averaged density of the DERIVED electron profile --
             ISS04's n19 takes its "usual meaning"; the vol-av reading
             misses the printed tau_E by -23%, goal learning L-001)
  ASH FIXED POINT (A.5/A.6, peak form, damped):
    n_D0 = n_T0 = (n_e0 - 2*n_He0) / 2      (quasi-neutrality at the peak)
    p_avg  = e_keV * ( 2 n_D0 (T_e0 + T_i0) / (1+alpha_n+alpha_T)
                     + n_He0 (2 T_e0 + T_i0) * I_W_S )          [Pa]
             -- the ONE volume-averaged thermal pressure of the plant:
             <n_e T_e + (n_D + n_T + n_He) T_i>_V over the derived
             profiles; 'Volume-Averaged Beta' reads it (WI-042 D2)
    W_th   = 1.5e-6 * p_avg * V                                 [MJ]
             (W = 3/2 <p>_V V, the sister code's definition: Lion 2021
             Eqs. 8-11 / Lion 2023 Eqs. 2.10-2.13, thermal, species sum,
             effective-radius element -- linked to this source by its
             Appendix A ancestry, never cited as this source's own)
    tau_E  = (C * W_th^-0.61)^(1/0.39)                          [s]
             C = 0.134*f_ren*a^2.28*B^0.84*iota_23^0.41
n_bar19^0.54*R^0.64
           (ISS04 Eq. A.7 with the source's own P = W/tau_E
           substitution -- the closed form behind Eq. A.8; C is
           re-evaluated at every iterate because n_bar19 now
           depends on the ash, WI-042 D3)
  n_He0 <- f_suppr * tau_ratio * tau_E * n_D0*n_T0*sigv_dt(T_i0)
           (Eq. A.5 helium balance x Eq. A.6 suppression; with tau*
           uniform in rho the peak and the shape are one equation)
DERIVED PROFILE DIAGNOSTICS (outputs; nothing downstream reads them):
  n_e_volav     = 2 n_D0 / (1+alpha_n) + 2 n_He0 I_vol_S      [m^-3]
  alpha_n_e_eff = n_e0 / n_e_volav - 1                        [1]
           (the vol-av/peak relation <n>/n0 = 1/(1+alpha) that bound
           the retired point-A exponent 0.596 from the printed pair
           3.17/5.06; here derived, 0.5953 at point A)
  alpha_He_eff  = least-squares slope of ln S(rho_k) on ln u_k over
           the 1,700 nodes rho_k = k/2000, k = 1..1700 (rho <= 0.85)
           -- the ash shape's effective power-law exponent (4.05 at
           point A; 4.7 at 10 keV, 3.5 at 20 keV: it moves with T_i0)
RADIATION (composed; profile-integrated over the DERIVED n_e(rho)):
  p_brems = 5.35e-37 * Z_eff * V
int n_e(rho)^2 * sqrt(T_e(rho)) dV'             [MW]
    p_line  = f_W * V * int n_e(rho)^2 * L_z_W(T_e(rho)) dV'    [MW]
              (L_z_W: piecewise coronal cooling-curve fit)
    p_sync  = Albajar (2001) formula at kappa_sync, R_w_sync with the
              density-profile parameter alpha_n_e_eff (WI-042 D4) [MW]
    p_rad   = p_brems + p_line + p_sync
  BALANCE (Eq. A.2/A.3):
    p_alpha_heat   = f_alpha * ash_frac * p_fus_internal          [MW]
             p_fus_internal: the identical profile-integrated
             Bosch-Hale evaluation as 'DT Fusion Power' at
             (n_D0, n_T0, T_i0) -- same algorithm, same contract
    p_aux_required = p_rad + W_th/tau_E - p_alpha_heat            [MW]

DORMANT (no-ash) CASE (WI-042 D6): an instance binding tau_ratio = 0
or f_suppr = 0 converges to n_He0 = 0 at the first iterate; then
n_e = 2 n_D0 u^alpha_n, every ash-weighted term vanishes, p_avg and
W_th reduce to the fuel-only closed form Sigma_s n_s0 T_s0 /
(1 + alpha_n + alpha_T), and alpha_n_e_eff = alpha_n. No switch.

EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): exp(), numerical
integrals, and the damped fixed point route this calc to the
handwritten codegen stage (manual_required); the generated handwritten
impl is normative and is guarded bit-exact by the oracle.
Discretization/convergence contract (mirrored exactly in the oracle):
trapezoidal rule in rho over [0,1], N = 200,000 intervals for every
profile integral (the fusion integral, I_line_n, I_line_S, I_W_S,
I_vol_S, the radiation integrals), temperature floor 1e-6 keV,
pure-Python float64; ash fixed point by damped half-step iteration
n_He0 <- 0.5*(n_He0 + F(n_He0)) from n_He0 = 0, absolute tolerance
1e12 m^-3, iteration cap 200; non-convergence, non-positive fuel
density, or a non-finite intermediate RAISES -- fail loudly, never
clamp (amended MR-WI037-2).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
(equations; every value image-verified -- the iter-01 AND iter-02
text tables are corrupted, the raw PDF and page images govern);
knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
(p. 9, p. 32 Appendix A, read from page renders -- WI-042);
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
(Lion et al. 2021, Eqs. 8-11: the W definition) and
knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
(Lion 2023, Eqs. 2.10-2.13), both registered at d4059ef1;
/home/reid/1cfe/1costingfe/src/costingfe/layers/radiation.py (pin 0254385);
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py (pin 0254385)
*Ref**: images/page_031_eq_6.png (Eq. A.7 ISS04), page_031_eq_7.png
(Eq. A.8, the P = W/tau_E rewriting this closed form reproduces);
page_031_eq_1.png / page_031_eq_2.png (Eq. A.2/A.3 balance);
page_031_eq_4.png / page_031_eq_5.png (Eq. A.5 helium balance,
A.6 suppression); raw PDF p. 9 col. 2 ("Helium ash profiles are
obtained using a fixed ratio of particle-to-energy confinement
time") and p. 32 ("tau*_alpha = rho* tau_E, where we use rho* ~ 8"),
the pointwise reading of A.5 (WI-042); iter-02 raw PDF appendix A
text ("replace the heating power by the ratio of plasma energy
divided by the energy confinement time"); radiation.py:260,275
(bremsstrahlung 5.35e-37*Z_eff*n^2*sqrt(T)), radiation.py:83-96
(W cooling-curve fit), radiation.py:180-241 (Albajar synchrotron,
eqs 13/15 of Albajar 2001); reactivity.py:54-70 (Bosch-Hale
sigv_dt); goal evidence work/orchestration/goals/
stored-energy-basis/evidence/w_counterfactual/
attribution_sourced_definition.json at 5cc30ac0 (the rule at the
printed peaks reproduces n_e0 5.04 / <n_e> 3.16 vs printed
5.06 / 3.17, W 524.5 MJ at the model's exponents; learnings
L-002/L-003) and work/active/WI-042_sourced-helium-ash-profile/
prototype/ (cross-checks at point A after WI-042: W +3.0 % vs the
printed 504.65, <n_e> +0.1 %, p_fus -1.8 %, tau_E +6.6 %, n_He0
+8 % -- the printed (W, tau_E) pair does not close the source's
own balance, L-002; nothing tuned)
*Basis**: steady-state 0D power balance over the source's own profile
rules -- power-law fuel and temperature profiles, the ash on the
fusion-rate profile (A.5 pointwise), electrons by quasi-neutrality
-- with ISS04 confinement in the source's own closed form, the
printed ash chain, and composed radiation; concept-agnostic (MR-3)
-- machine values, levers, and quality facts bound by instances

Inputs:
    - iota_23_in: iota_23_in parameter
    - Z_eff_in: Z_eff_in parameter
    - ash_frac_in: ash_frac_in parameter
    - alpha_T_in: alpha_T_in parameter
    - kappa_sync_in: kappa_sync_in parameter
    - V: V parameter
    - n_e0_in: n_e0_in parameter
    - T_i0_in: T_i0_in parameter
    - f_suppr_in: f_suppr_in parameter
    - R_in: R_in parameter
    - tau_ratio_in: tau_ratio_in parameter
    - f_ren_in: f_ren_in parameter
    - f_W_in: f_W_in parameter
    - E_fus_in: E_fus_in parameter
    - alpha_n_in: alpha_n_in parameter
    - B_in: B_in parameter
    - f_alpha_in: f_alpha_in parameter
    - r_TiTe_in: r_TiTe_in parameter
    - R_w_sync_in: R_w_sync_in parameter
    - a_in: a_in parameter

Outputs:
    - n_bar19: n_bar19 result
    - n_T0: n_T0 result
    - W_th: W_th result
    - p_avg: p_avg result
    - p_brems: p_brems result
    - n_He0: n_He0 result
    - n_D0: n_D0 result
    - alpha_n_e_eff: alpha_n_e_eff result
    - p_aux_required: p_aux_required result
    - p_rad: p_rad result
    - p_alpha_heat: p_alpha_heat result
    - tau_E: tau_E result
    - p_sync: p_sync result
    - p_line: p_line result
    - n_e_volav: n_e_volav result
    - alpha_He_eff: alpha_He_eff result
    - T_e0: T_e0 result

SysML Source: root-0/analyses/mfe_plasma_sustainment.sysml:4

SysML Source: root-0/analyses/mfe_plasma_sustainment.sysml:4

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.primitives import Float
from stellarator_tea.schemas.plasma_sustainment_output import Plasma_SustainmentOutput


class Plasma_SustainmentInput(BaseModel):
    """Input model for Plasma_SustainmentModule.

    Attributes:
        iota_23_in: iota_23_in input
        Z_eff_in: Z_eff_in input
        ash_frac_in: ash_frac_in input
        alpha_T_in: alpha_T_in input
        kappa_sync_in: kappa_sync_in input
        V: V input
        n_e0_in: n_e0_in input
        T_i0_in: T_i0_in input
        f_suppr_in: f_suppr_in input
        R_in: R_in input
        tau_ratio_in: tau_ratio_in input
        f_ren_in: f_ren_in input
        f_W_in: f_W_in input
        E_fus_in: E_fus_in input
        alpha_n_in: alpha_n_in input
        B_in: B_in input
        f_alpha_in: f_alpha_in input
        r_TiTe_in: r_TiTe_in input
        R_w_sync_in: R_w_sync_in input
        a_in: a_in input
    """
    iota_23_in: float = Field(..., description="iota_23_in input")
    Z_eff_in: float = Field(..., description="Z_eff_in input")
    ash_frac_in: float = Field(..., description="ash_frac_in input")
    alpha_T_in: float = Field(..., description="alpha_T_in input")
    kappa_sync_in: float = Field(..., description="kappa_sync_in input")
    V: float = Field(..., description="V input")
    n_e0_in: float = Field(..., description="n_e0_in input")
    T_i0_in: float = Field(..., description="T_i0_in input")
    f_suppr_in: float = Field(..., description="f_suppr_in input")
    R_in: float = Field(..., description="R_in input")
    tau_ratio_in: float = Field(..., description="tau_ratio_in input")
    f_ren_in: float = Field(..., description="f_ren_in input")
    f_W_in: float = Field(..., description="f_W_in input")
    E_fus_in: float = Field(..., description="E_fus_in input")
    alpha_n_in: float = Field(..., description="alpha_n_in input")
    B_in: float = Field(..., description="B_in input")
    f_alpha_in: float = Field(..., description="f_alpha_in input")
    r_TiTe_in: float = Field(..., description="r_TiTe_in input")
    R_w_sync_in: float = Field(..., description="R_w_sync_in input")
    a_in: float = Field(..., description="a_in input")


class Plasma_SustainmentModule(ModuleBase[Plasma_SustainmentInput, Plasma_SustainmentOutput]):
    """TEAx module for Plasma_Sustainment calculation.

Operating-point sustainment chain (WI-037; profiles WI-042): from the
machine (a, R, iota_2/3, axis field B), the operating-point levers
(peak electron density n_e0, peak ion temperature T_i0), and installed
physics facts, compute the required sustained plasma-coupled heating
power and the forward ash/fuel state. Temperature and density remain
design levers; the machine pushes back through the paired
'Sustainment Limit' (mfe_viability.sysml) on the computed
p_aux_required.

PROFILES (Stellaris Eqs. 2-3 and the source's own ash rule; WI-042):
  u        = 1 - rho^2;  dV/V = 2 rho d(rho)
  T_i(rho) = T_i0 * u^alpha_T;   T_e(rho) = T_e0 * u^alpha_T
  n_D(rho) = n_T(rho) = n_D0 * u^alpha_n           (the fuel exponent)
  S(rho)   = u^(2 alpha_n) * sigv_dt(T_i(rho)) / sigv_dt(T_i0)
             (the fusion-rate shape, S(0) = 1)
  n_He(rho) = n_He0 * S(rho)
             -- Eq. A.5 applied pointwise with the particle-to-energy
             confinement ratio uniform in rho ("helium ash profiles are
             obtained using a fixed ratio of particle-to-energy
             confinement time", raw PDF p. 9): the ash follows the
             fusion-rate profile, scaled to the converged peak below.
             NEVER a bound exponent -- the shape is computed from the
             rule at every lever point, so it holds for any geometry
             [OWNER 2026-09-05: "make sure this scales up for larger
             stellarators"].
  n_e(rho) = n_D + n_T + 2 n_He = 2 n_D0 u^alpha_n + 2 n_He0 S(rho)
             (quasi-neutrality pointwise; trace W at f_W ~ 1e-5
             neglected in the charge sum; n_e(0) = n_e0, the lever)

CHAIN (each stage an output; all evaluated at the same lever point):

  T_e0     = T_i0 / r_TiTe                                  [keV]
  I_line_n = integral_0^1 u^alpha_n d rho
  I_line_S = integral_0^1 S(rho) d rho
  I_W_S    = integral_0^1 S(rho) u^alpha_T 2 rho d rho   ( = <S u^alpha_T>_V )
  I_vol_S  = integral_0^1 S(rho) 2 rho d rho             ( = <S>_V )
  n_bar19  = (2 n_D0 I_line_n + 2 n_He0 I_line_S) / 1e19  [1e19 m^-3]
             (line-averaged density of the DERIVED electron profile --
             ISS04's n19 takes its "usual meaning"; the vol-av reading
             misses the printed tau_E by -23%, goal learning L-001)
  ASH FIXED POINT (A.5/A.6, peak form, damped):
    n_D0 = n_T0 = (n_e0 - 2*n_He0) / 2      (quasi-neutrality at the peak)
    p_avg  = e_keV * ( 2 n_D0 (T_e0 + T_i0) / (1+alpha_n+alpha_T)
                     + n_He0 (2 T_e0 + T_i0) * I_W_S )          [Pa]
             -- the ONE volume-averaged thermal pressure of the plant:
             <n_e T_e + (n_D + n_T + n_He) T_i>_V over the derived
             profiles; 'Volume-Averaged Beta' reads it (WI-042 D2)
    W_th   = 1.5e-6 * p_avg * V                                 [MJ]
             (W = 3/2 <p>_V V, the sister code's definition: Lion 2021
             Eqs. 8-11 / Lion 2023 Eqs. 2.10-2.13, thermal, species sum,
             effective-radius element -- linked to this source by its
             Appendix A ancestry, never cited as this source's own)
    tau_E  = (C * W_th^-0.61)^(1/0.39)                          [s]
             C = 0.134*f_ren*a^2.28*B^0.84*iota_23^0.41
n_bar19^0.54*R^0.64
           (ISS04 Eq. A.7 with the source's own P = W/tau_E
           substitution -- the closed form behind Eq. A.8; C is
           re-evaluated at every iterate because n_bar19 now
           depends on the ash, WI-042 D3)
  n_He0 <- f_suppr * tau_ratio * tau_E * n_D0*n_T0*sigv_dt(T_i0)
           (Eq. A.5 helium balance x Eq. A.6 suppression; with tau*
           uniform in rho the peak and the shape are one equation)
DERIVED PROFILE DIAGNOSTICS (outputs; nothing downstream reads them):
  n_e_volav     = 2 n_D0 / (1+alpha_n) + 2 n_He0 I_vol_S      [m^-3]
  alpha_n_e_eff = n_e0 / n_e_volav - 1                        [1]
           (the vol-av/peak relation <n>/n0 = 1/(1+alpha) that bound
           the retired point-A exponent 0.596 from the printed pair
           3.17/5.06; here derived, 0.5953 at point A)
  alpha_He_eff  = least-squares slope of ln S(rho_k) on ln u_k over
           the 1,700 nodes rho_k = k/2000, k = 1..1700 (rho <= 0.85)
           -- the ash shape's effective power-law exponent (4.05 at
           point A; 4.7 at 10 keV, 3.5 at 20 keV: it moves with T_i0)
RADIATION (composed; profile-integrated over the DERIVED n_e(rho)):
  p_brems = 5.35e-37 * Z_eff * V
int n_e(rho)^2 * sqrt(T_e(rho)) dV'             [MW]
    p_line  = f_W * V * int n_e(rho)^2 * L_z_W(T_e(rho)) dV'    [MW]
              (L_z_W: piecewise coronal cooling-curve fit)
    p_sync  = Albajar (2001) formula at kappa_sync, R_w_sync with the
              density-profile parameter alpha_n_e_eff (WI-042 D4) [MW]
    p_rad   = p_brems + p_line + p_sync
  BALANCE (Eq. A.2/A.3):
    p_alpha_heat   = f_alpha * ash_frac * p_fus_internal          [MW]
             p_fus_internal: the identical profile-integrated
             Bosch-Hale evaluation as 'DT Fusion Power' at
             (n_D0, n_T0, T_i0) -- same algorithm, same contract
    p_aux_required = p_rad + W_th/tau_E - p_alpha_heat            [MW]

DORMANT (no-ash) CASE (WI-042 D6): an instance binding tau_ratio = 0
or f_suppr = 0 converges to n_He0 = 0 at the first iterate; then
n_e = 2 n_D0 u^alpha_n, every ash-weighted term vanishes, p_avg and
W_th reduce to the fuel-only closed form Sigma_s n_s0 T_s0 /
(1 + alpha_n + alpha_T), and alpha_n_e_eff = alpha_n. No switch.

EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): exp(), numerical
integrals, and the damped fixed point route this calc to the
handwritten codegen stage (manual_required); the generated handwritten
impl is normative and is guarded bit-exact by the oracle.
Discretization/convergence contract (mirrored exactly in the oracle):
trapezoidal rule in rho over [0,1], N = 200,000 intervals for every
profile integral (the fusion integral, I_line_n, I_line_S, I_W_S,
I_vol_S, the radiation integrals), temperature floor 1e-6 keV,
pure-Python float64; ash fixed point by damped half-step iteration
n_He0 <- 0.5*(n_He0 + F(n_He0)) from n_He0 = 0, absolute tolerance
1e12 m^-3, iteration cap 200; non-convergence, non-positive fuel
density, or a non-finite intermediate RAISES -- fail loudly, never
clamp (amended MR-WI037-2).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
(equations; every value image-verified -- the iter-01 AND iter-02
text tables are corrupted, the raw PDF and page images govern);
knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
(p. 9, p. 32 Appendix A, read from page renders -- WI-042);
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
(Lion et al. 2021, Eqs. 8-11: the W definition) and
knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
(Lion 2023, Eqs. 2.10-2.13), both registered at d4059ef1;
/home/reid/1cfe/1costingfe/src/costingfe/layers/radiation.py (pin 0254385);
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py (pin 0254385)
*Ref**: images/page_031_eq_6.png (Eq. A.7 ISS04), page_031_eq_7.png
(Eq. A.8, the P = W/tau_E rewriting this closed form reproduces);
page_031_eq_1.png / page_031_eq_2.png (Eq. A.2/A.3 balance);
page_031_eq_4.png / page_031_eq_5.png (Eq. A.5 helium balance,
A.6 suppression); raw PDF p. 9 col. 2 ("Helium ash profiles are
obtained using a fixed ratio of particle-to-energy confinement
time") and p. 32 ("tau*_alpha = rho* tau_E, where we use rho* ~ 8"),
the pointwise reading of A.5 (WI-042); iter-02 raw PDF appendix A
text ("replace the heating power by the ratio of plasma energy
divided by the energy confinement time"); radiation.py:260,275
(bremsstrahlung 5.35e-37*Z_eff*n^2*sqrt(T)), radiation.py:83-96
(W cooling-curve fit), radiation.py:180-241 (Albajar synchrotron,
eqs 13/15 of Albajar 2001); reactivity.py:54-70 (Bosch-Hale
sigv_dt); goal evidence work/orchestration/goals/
stored-energy-basis/evidence/w_counterfactual/
attribution_sourced_definition.json at 5cc30ac0 (the rule at the
printed peaks reproduces n_e0 5.04 / <n_e> 3.16 vs printed
5.06 / 3.17, W 524.5 MJ at the model's exponents; learnings
L-002/L-003) and work/active/WI-042_sourced-helium-ash-profile/
prototype/ (cross-checks at point A after WI-042: W +3.0 % vs the
printed 504.65, <n_e> +0.1 %, p_fus -1.8 %, tau_E +6.6 %, n_He0
+8 % -- the printed (W, tau_E) pair does not close the source's
own balance, L-002; nothing tuned)
*Basis**: steady-state 0D power balance over the source's own profile
rules -- power-law fuel and temperature profiles, the ash on the
fusion-rate profile (A.5 pointwise), electrons by quasi-neutrality
-- with ISS04 confinement in the source's own closed form, the
printed ash chain, and composed radiation; concept-agnostic (MR-3)
-- machine values, levers, and quality facts bound by instances

Inputs:
    - iota_23_in: iota_23_in parameter
    - Z_eff_in: Z_eff_in parameter
    - ash_frac_in: ash_frac_in parameter
    - alpha_T_in: alpha_T_in parameter
    - kappa_sync_in: kappa_sync_in parameter
    - V: V parameter
    - n_e0_in: n_e0_in parameter
    - T_i0_in: T_i0_in parameter
    - f_suppr_in: f_suppr_in parameter
    - R_in: R_in parameter
    - tau_ratio_in: tau_ratio_in parameter
    - f_ren_in: f_ren_in parameter
    - f_W_in: f_W_in parameter
    - E_fus_in: E_fus_in parameter
    - alpha_n_in: alpha_n_in parameter
    - B_in: B_in parameter
    - f_alpha_in: f_alpha_in parameter
    - r_TiTe_in: r_TiTe_in parameter
    - R_w_sync_in: R_w_sync_in parameter
    - a_in: a_in parameter

Outputs:
    - n_bar19: n_bar19 result
    - n_T0: n_T0 result
    - W_th: W_th result
    - p_avg: p_avg result
    - p_brems: p_brems result
    - n_He0: n_He0 result
    - n_D0: n_D0 result
    - alpha_n_e_eff: alpha_n_e_eff result
    - p_aux_required: p_aux_required result
    - p_rad: p_rad result
    - p_alpha_heat: p_alpha_heat result
    - tau_E: tau_E result
    - p_sync: p_sync result
    - p_line: p_line result
    - n_e_volav: n_e_volav result
    - alpha_He_eff: alpha_He_eff result
    - T_e0: T_e0 result

SysML Source: root-0/analyses/mfe_plasma_sustainment.sysml:4

    SysML Source: root-0/analyses/mfe_plasma_sustainment.sysml:4

    Calculation Specification:
        ash_frac_in = 0.2002
        R_w_sync_in = 0.6
        kappa_sync_in = 1.0
        
Documentation:
Operating-point sustainment chain (WI-037; profiles WI-042): from the
machine (a, R, iota_2/3, axis field B), the operating-point levers
(peak electron density n_e0, peak ion temperature T_i0), and installed
physics facts, compute the required sustained plasma-coupled heating
power and the forward ash/fuel state. Temperature and density remain
design levers; the machine pushes back through the paired
'Sustainment Limit' (mfe_viability.sysml) on the computed
p_aux_required.

PROFILES (Stellaris Eqs. 2-3 and the source's own ash rule; WI-042):
  u        = 1 - rho^2;  dV/V = 2 rho d(rho)
  T_i(rho) = T_i0 * u^alpha_T;   T_e(rho) = T_e0 * u^alpha_T
  n_D(rho) = n_T(rho) = n_D0 * u^alpha_n           (the fuel exponent)
  S(rho)   = u^(2 alpha_n) * sigv_dt(T_i(rho)) / sigv_dt(T_i0)
             (the fusion-rate shape, S(0) = 1)
  n_He(rho) = n_He0 * S(rho)
             -- Eq. A.5 applied pointwise with the particle-to-energy
             confinement ratio uniform in rho ("helium ash profiles are
             obtained using a fixed ratio of particle-to-energy
             confinement time", raw PDF p. 9): the ash follows the
             fusion-rate profile, scaled to the converged peak below.
             NEVER a bound exponent -- the shape is computed from the
             rule at every lever point, so it holds for any geometry
             [OWNER 2026-09-05: "make sure this scales up for larger
             stellarators"].
  n_e(rho) = n_D + n_T + 2 n_He = 2 n_D0 u^alpha_n + 2 n_He0 S(rho)
             (quasi-neutrality pointwise; trace W at f_W ~ 1e-5
             neglected in the charge sum; n_e(0) = n_e0, the lever)

CHAIN (each stage an output; all evaluated at the same lever point):

  T_e0     = T_i0 / r_TiTe                                  [keV]
  I_line_n = integral_0^1 u^alpha_n d rho
  I_line_S = integral_0^1 S(rho) d rho
  I_W_S    = integral_0^1 S(rho) u^alpha_T 2 rho d rho   ( = <S u^alpha_T>_V )
  I_vol_S  = integral_0^1 S(rho) 2 rho d rho             ( = <S>_V )
  n_bar19  = (2 n_D0 I_line_n + 2 n_He0 I_line_S) / 1e19  [1e19 m^-3]
             (line-averaged density of the DERIVED electron profile --
             ISS04's n19 takes its "usual meaning"; the vol-av reading
             misses the printed tau_E by -23%, goal learning L-001)
  ASH FIXED POINT (A.5/A.6, peak form, damped):
    n_D0 = n_T0 = (n_e0 - 2*n_He0) / 2      (quasi-neutrality at the peak)
    p_avg  = e_keV * ( 2 n_D0 (T_e0 + T_i0) / (1+alpha_n+alpha_T)
                     + n_He0 (2 T_e0 + T_i0) * I_W_S )          [Pa]
             -- the ONE volume-averaged thermal pressure of the plant:
             <n_e T_e + (n_D + n_T + n_He) T_i>_V over the derived
             profiles; 'Volume-Averaged Beta' reads it (WI-042 D2)
    W_th   = 1.5e-6 * p_avg * V                                 [MJ]
             (W = 3/2 <p>_V V, the sister code's definition: Lion 2021
             Eqs. 8-11 / Lion 2023 Eqs. 2.10-2.13, thermal, species sum,
             effective-radius element -- linked to this source by its
             Appendix A ancestry, never cited as this source's own)
    tau_E  = (C * W_th^-0.61)^(1/0.39)                          [s]
             C = 0.134*f_ren*a^2.28*B^0.84*iota_23^0.41
n_bar19^0.54*R^0.64
           (ISS04 Eq. A.7 with the source's own P = W/tau_E
           substitution -- the closed form behind Eq. A.8; C is
           re-evaluated at every iterate because n_bar19 now
           depends on the ash, WI-042 D3)
  n_He0 <- f_suppr * tau_ratio * tau_E * n_D0*n_T0*sigv_dt(T_i0)
           (Eq. A.5 helium balance x Eq. A.6 suppression; with tau*
           uniform in rho the peak and the shape are one equation)
DERIVED PROFILE DIAGNOSTICS (outputs; nothing downstream reads them):
  n_e_volav     = 2 n_D0 / (1+alpha_n) + 2 n_He0 I_vol_S      [m^-3]
  alpha_n_e_eff = n_e0 / n_e_volav - 1                        [1]
           (the vol-av/peak relation <n>/n0 = 1/(1+alpha) that bound
           the retired point-A exponent 0.596 from the printed pair
           3.17/5.06; here derived, 0.5953 at point A)
  alpha_He_eff  = least-squares slope of ln S(rho_k) on ln u_k over
           the 1,700 nodes rho_k = k/2000, k = 1..1700 (rho <= 0.85)
           -- the ash shape's effective power-law exponent (4.05 at
           point A; 4.7 at 10 keV, 3.5 at 20 keV: it moves with T_i0)
RADIATION (composed; profile-integrated over the DERIVED n_e(rho)):
  p_brems = 5.35e-37 * Z_eff * V
int n_e(rho)^2 * sqrt(T_e(rho)) dV'             [MW]
    p_line  = f_W * V * int n_e(rho)^2 * L_z_W(T_e(rho)) dV'    [MW]
              (L_z_W: piecewise coronal cooling-curve fit)
    p_sync  = Albajar (2001) formula at kappa_sync, R_w_sync with the
              density-profile parameter alpha_n_e_eff (WI-042 D4) [MW]
    p_rad   = p_brems + p_line + p_sync
  BALANCE (Eq. A.2/A.3):
    p_alpha_heat   = f_alpha * ash_frac * p_fus_internal          [MW]
             p_fus_internal: the identical profile-integrated
             Bosch-Hale evaluation as 'DT Fusion Power' at
             (n_D0, n_T0, T_i0) -- same algorithm, same contract
    p_aux_required = p_rad + W_th/tau_E - p_alpha_heat            [MW]

DORMANT (no-ash) CASE (WI-042 D6): an instance binding tau_ratio = 0
or f_suppr = 0 converges to n_He0 = 0 at the first iterate; then
n_e = 2 n_D0 u^alpha_n, every ash-weighted term vanishes, p_avg and
W_th reduce to the fuel-only closed form Sigma_s n_s0 T_s0 /
(1 + alpha_n + alpha_T), and alpha_n_e_eff = alpha_n. No switch.

EXECUTABLE SEMANTIC (Rung B, WI-022 pattern): exp(), numerical
integrals, and the damped fixed point route this calc to the
handwritten codegen stage (manual_required); the generated handwritten
impl is normative and is guarded bit-exact by the oracle.
Discretization/convergence contract (mirrored exactly in the oracle):
trapezoidal rule in rho over [0,1], N = 200,000 intervals for every
profile integral (the fusion integral, I_line_n, I_line_S, I_W_S,
I_vol_S, the radiation integrals), temperature floor 1e-6 keV,
pure-Python float64; ash fixed point by damped half-step iteration
n_He0 <- 0.5*(n_He0 + F(n_He0)) from n_He0 = 0, absolute tolerance
1e12 m^-3, iteration cap 200; non-convergence, non-positive fuel
density, or a non-finite intermediate RAISES -- fail loudly, never
clamp (amended MR-WI037-2).

*Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md
(equations; every value image-verified -- the iter-01 AND iter-02
text tables are corrupted, the raw PDF and page images govern);
knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf
(p. 9, p. 32 Appendix A, read from page renders -- WI-042);
knowledge/sources/a_general_stellarator_version_of_the_systems_code_process/
(Lion et al. 2021, Eqs. 8-11: the W definition) and
knowledge/sources/systems_code_models_for_stellarator_fusion_power_plants_and/
(Lion 2023, Eqs. 2.10-2.13), both registered at d4059ef1;
/home/reid/1cfe/1costingfe/src/costingfe/layers/radiation.py (pin 0254385);
/home/reid/1cfe/1costingfe/src/costingfe/layers/reactivity.py (pin 0254385)
*Ref**: images/page_031_eq_6.png (Eq. A.7 ISS04), page_031_eq_7.png
(Eq. A.8, the P = W/tau_E rewriting this closed form reproduces);
page_031_eq_1.png / page_031_eq_2.png (Eq. A.2/A.3 balance);
page_031_eq_4.png / page_031_eq_5.png (Eq. A.5 helium balance,
A.6 suppression); raw PDF p. 9 col. 2 ("Helium ash profiles are
obtained using a fixed ratio of particle-to-energy confinement
time") and p. 32 ("tau*_alpha = rho* tau_E, where we use rho* ~ 8"),
the pointwise reading of A.5 (WI-042); iter-02 raw PDF appendix A
text ("replace the heating power by the ratio of plasma energy
divided by the energy confinement time"); radiation.py:260,275
(bremsstrahlung 5.35e-37*Z_eff*n^2*sqrt(T)), radiation.py:83-96
(W cooling-curve fit), radiation.py:180-241 (Albajar synchrotron,
eqs 13/15 of Albajar 2001); reactivity.py:54-70 (Bosch-Hale
sigv_dt); goal evidence work/orchestration/goals/
stored-energy-basis/evidence/w_counterfactual/
attribution_sourced_definition.json at 5cc30ac0 (the rule at the
printed peaks reproduces n_e0 5.04 / <n_e> 3.16 vs printed
5.06 / 3.17, W 524.5 MJ at the model's exponents; learnings
L-002/L-003) and work/active/WI-042_sourced-helium-ash-profile/
prototype/ (cross-checks at point A after WI-042: W +3.0 % vs the
printed 504.65, <n_e> +0.1 %, p_fus -1.8 %, tau_E +6.6 %, n_He0
+8 % -- the printed (W, tau_E) pair does not close the source's
own balance, L-002; nothing tuned)
*Basis**: steady-state 0D power balance over the source's own profile
rules -- power-law fuel and temperature profiles, the ash on the
fusion-rate profile (A.5 pointwise), electrons by quasi-neutrality
-- with ISS04 confinement in the source's own closed form, the
printed ash chain, and composed radiation; concept-agnostic (MR-3)
-- machine values, levers, and quality facts bound by instances

    IMPLEMENTATION: See stellarator_tea.handwritten.mfe_plasma_sustainment.plasma_sustainment_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts n_bar19, n_T0, W_th, p_avg, p_brems, n_He0, n_D0, alpha_n_e_eff, p_aux_required, p_rad, p_alpha_heat, tau_E, p_sync, p_line, n_e_volav, alpha_He_eff, T_e0 fields to separate channels.
    """

    name: str = "Plasma_SustainmentModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, iota_23_in: float, Z_eff_in: float, ash_frac_in: float, alpha_T_in: float, kappa_sync_in: float, V: float, n_e0_in: float, T_i0_in: float, f_suppr_in: float, R_in: float, tau_ratio_in: float, f_ren_in: float, f_W_in: float, E_fus_in: float, alpha_n_in: float, B_in: float, f_alpha_in: float, r_TiTe_in: float, R_w_sync_in: float, a_in: float    ) -> Plasma_SustainmentInput:
        """Validate inputs and fill defaults.

        Args:
            iota_23_in: iota_23_in input
            Z_eff_in: Z_eff_in input
            ash_frac_in: ash_frac_in input
            alpha_T_in: alpha_T_in input
            kappa_sync_in: kappa_sync_in input
            V: V input
            n_e0_in: n_e0_in input
            T_i0_in: T_i0_in input
            f_suppr_in: f_suppr_in input
            R_in: R_in input
            tau_ratio_in: tau_ratio_in input
            f_ren_in: f_ren_in input
            f_W_in: f_W_in input
            E_fus_in: E_fus_in input
            alpha_n_in: alpha_n_in input
            B_in: B_in input
            f_alpha_in: f_alpha_in input
            r_TiTe_in: r_TiTe_in input
            R_w_sync_in: R_w_sync_in input
            a_in: a_in input

        Returns:
            Validated input model
        """
        return Plasma_SustainmentInput(iota_23_in=iota_23_in, Z_eff_in=Z_eff_in, ash_frac_in=ash_frac_in, alpha_T_in=alpha_T_in, kappa_sync_in=kappa_sync_in, V=V, n_e0_in=n_e0_in, T_i0_in=T_i0_in, f_suppr_in=f_suppr_in, R_in=R_in, tau_ratio_in=tau_ratio_in, f_ren_in=f_ren_in, f_W_in=f_W_in, E_fus_in=E_fus_in, alpha_n_in=alpha_n_in, B_in=B_in, f_alpha_in=f_alpha_in, r_TiTe_in=r_TiTe_in, R_w_sync_in=R_w_sync_in, a_in=a_in)

    def run(
        self, iota_23_in: float, Z_eff_in: float, ash_frac_in: float, alpha_T_in: float, kappa_sync_in: float, V: float, n_e0_in: float, T_i0_in: float, f_suppr_in: float, R_in: float, tau_ratio_in: float, f_ren_in: float, f_W_in: float, E_fus_in: float, alpha_n_in: float, B_in: float, f_alpha_in: float, r_TiTe_in: float, R_w_sync_in: float, a_in: float    ) -> ModuleResult[Plasma_SustainmentOutput]:
        """Execute calculation.

        Args:
            iota_23_in: iota_23_in input
            Z_eff_in: Z_eff_in input
            ash_frac_in: ash_frac_in input
            alpha_T_in: alpha_T_in input
            kappa_sync_in: kappa_sync_in input
            V: V input
            n_e0_in: n_e0_in input
            T_i0_in: T_i0_in input
            f_suppr_in: f_suppr_in input
            R_in: R_in input
            tau_ratio_in: tau_ratio_in input
            f_ren_in: f_ren_in input
            f_W_in: f_W_in input
            E_fus_in: E_fus_in input
            alpha_n_in: alpha_n_in input
            B_in: B_in input
            f_alpha_in: f_alpha_in input
            r_TiTe_in: r_TiTe_in input
            R_w_sync_in: R_w_sync_in input
            a_in: a_in input

        Returns:
            Module result with Plasma_SustainmentOutput (n_bar19, n_T0, W_th, p_avg, p_brems, n_He0, n_D0, alpha_n_e_eff, p_aux_required, p_rad, p_alpha_heat, tau_E, p_sync, p_line, n_e_volav, alpha_He_eff, T_e0)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(iota_23_in, Z_eff_in, ash_frac_in, alpha_T_in, kappa_sync_in, V, n_e0_in, T_i0_in, f_suppr_in, R_in, tau_ratio_in, f_ren_in, f_W_in, E_fus_in, alpha_n_in, B_in, f_alpha_in, r_TiTe_in, R_w_sync_in, a_in)

        # Import handwritten implementation
        from stellarator_tea.handwritten.mfe_plasma_sustainment.plasma_sustainment_impl import (
            run_plasma_sustainment,
        )

        # Execute implementation - returns tuple of values
        n_bar19, n_T0, W_th, p_avg, p_brems, n_He0, n_D0, alpha_n_e_eff, p_aux_required, p_rad, p_alpha_heat, tau_E, p_sync, p_line, n_e_volav, alpha_He_eff, T_e0 = run_plasma_sustainment(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Plasma_SustainmentOutput(
                n_bar19=n_bar19,
                n_T0=n_T0,
                W_th=W_th,
                p_avg=p_avg,
                p_brems=p_brems,
                n_He0=n_He0,
                n_D0=n_D0,
                alpha_n_e_eff=alpha_n_e_eff,
                p_aux_required=p_aux_required,
                p_rad=p_rad,
                p_alpha_heat=p_alpha_heat,
                tau_E=tau_E,
                p_sync=p_sync,
                p_line=p_line,
                n_e_volav=n_e_volav,
                alpha_He_eff=alpha_He_eff,
                T_e0=T_e0,
            )
        )
