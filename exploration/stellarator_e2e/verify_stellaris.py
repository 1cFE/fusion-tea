"""Oracle for the Stellaris (concept-09) forward pass.

Pure-Python recompute of the entire SysML MFE plant chain, mirroring the calc
defs line-for-line (models/analyses/mfe_*.sysml + designs/generic_mfe/mfe_plant
+ designs/stellarator_09). Used to check the generated + teax-executed result and
to cross-check against the WI-018 oracle headline numbers.

All monetary values in dollars ($). Inputs are the Stellaris design-point bindings
read from stellarator_plant.sysml.
"""

import math

# WI-022 discretization contract — EXACT mirror of the handwritten impl
# (generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py). The
# runner asserts the generated pipeline against this at rel 1e-9; do not
# change one copy without the other.
N_INTERVALS = 200_000


def _sigv_dt(T_keV):
    """Bosch-Hale D-T reactivity <sigma*v> [m^3/s] (reactivity.py:54-70)."""
    T = max(T_keV, 1e-6)
    theta = T / (
        1.0
        - T * (1.51361e-2 + T * (4.60643e-3 + T * -1.06750e-4))
        / (1.0 + T * (7.51886e-2 + T * (1.35000e-2 + T * 1.36600e-5)))
    )
    xi = ((34.3827 * 34.3827) / (4.0 * theta)) ** (1.0 / 3.0)
    return (
        1.17302e-9 * theta
        * math.sqrt(xi / (1124656.0 * T * T * T))
        * math.exp(-3.0 * xi) * 1e-6
    )


def _profile_integral(alpha_n, alpha_T, T_i0):
    """I = trapezoid_{rho in [0,1]} (1-rho^2)^(2*alpha_n) * sigv_dt(T_i0*(1-rho^2)^alpha_T) * 2*rho."""
    acc = 0.0
    n = N_INTERVALS
    for i in range(n + 1):
        rho = i / n
        u = 1.0 - rho * rho
        f = (u ** (2.0 * alpha_n)) * _sigv_dt(T_i0 * (u ** alpha_T)) * 2.0 * rho
        acc += f if 0 < i < n else 0.5 * f
    return acc / n

# --- WI-037 sustainment mirrors (identical to plasma_sustainment_impl.py,
# same discretization/convergence contract; bit-exact bar) ---
ASH_TOL = 1e12
ASH_CAP = 200
KEV_TO_J = 1.602176634e-16


def _trapz_rho(f):
    acc = 0.0
    n = N_INTERVALS
    for i in range(n + 1):
        rho = i / n
        u = 1.0 - rho * rho
        v = f(u, rho)
        acc += v if 0 < i < n else 0.5 * v
    return acc / n


def _lz_w(T_keV):
    T = max(T_keV, 0.01)
    if T < 0.1:
        return 5.0e-31 * T ** -1.0
    if T < 1.0:
        return 1.5e-31 * T ** 0.5
    if T < 10.0:
        return 5.0e-31
    return 5.0e-31 * T ** -0.5


def _p_sync_albajar(T_e0, n_e0_20, B, R, a, kappa, R_w, alpha_n, alpha_T):
    A = R / a
    p_a0 = 6.04e3 * a * n_e0_20 / B
    correction = (1 - R_w) ** 0.62 / (
        1 + 0.12 * T_e0 / p_a0 ** 0.41 * (1 - R_w) ** 0.41
    ) ** 1.51
    beta_t = 2.0
    K = (
        (alpha_n + 3.87 * alpha_T + 1.46) ** (-0.79)
        * (1.98 + alpha_T) ** 1.36
        * beta_t ** 2.14
        * (beta_t ** 1.53 + 1.87 * alpha_T - 0.16) ** (-1.33)
    )
    G = 0.93 * (1 + 0.85 * math.exp(-0.82 * A))
    return (
        3.84e-8 * correction * R * a ** 1.38 * kappa ** 0.79
        * B ** 2.62 * n_e0_20 ** 0.38 * T_e0 * (16 + T_e0) ** 2.61 * K * G
    )


def _sustainment(p, V, B_axis):
    """Mirror of run_plasma_sustainment (same names, same statement order).

    WI-042: the helium ash follows the source's own rule -- Eq. A.5 applied
    pointwise with tau* uniform in rho, so n_He(rho) = n_He0 * S(rho) with S the
    fusion-rate shape -- the electrons close by quasi-neutrality pointwise, the
    ISS04 line average and the radiation integrals take the derived electron
    profile, and p_avg (the one volume-averaged thermal pressure) feeds both W
    and beta. Written from the WI-042 design (work/active/WI-042_sourced-helium-
    ash-profile/design.md, section Research findings and D1-D6).
    """
    n_e0 = p["n_e0"]
    T_i0 = p["T_i0"]
    a = p["a"]
    R = p["magnet_R0"]
    B = B_axis
    alpha_n = p["alpha_n"]
    alpha_T = p["alpha_T"]
    T_e0 = T_i0 / p["Ti_over_Te"]
    sigv_peak = _sigv_dt(T_i0)

    # The ash shape: the fusion-rate profile normalised to its peak, S(0) = 1.
    def S(u):
        return (u ** (2.0 * alpha_n)) * _sigv_dt(T_i0 * (u ** alpha_T)) / sigv_peak

    # Profile integrals that do not depend on the ash amount (computed once).
    I_line_fuel = _trapz_rho(lambda u, rho: u ** alpha_n)             # chord average of the fuel shape
    I_line_S = _trapz_rho(lambda u, rho: S(u))                         # chord average of the ash shape
    I_W_S = _trapz_rho(lambda u, rho: S(u) * (u ** alpha_T) * 2.0 * rho)   # <S u^alpha_T>_V
    I_vol_S = _trapz_rho(lambda u, rho: S(u) * 2.0 * rho)              # <S>_V
    fus_I = _profile_integral(alpha_n, alpha_T, T_i0)
    C_geo = (0.134 * p["f_ren"] * a ** 2.28 * B ** 0.84
             * p["iota_23"] ** 0.41 * R ** 0.64)

    def state(n_He0):
        n_fuel = n_e0 - 2.0 * n_He0
        if n_fuel <= 0.0:
            raise RuntimeError("oracle sustainment: non-positive fuel")
        n_D0 = n_T0 = 0.5 * n_fuel
        # Line-averaged density of the DERIVED electron profile (ISS04's n19);
        # the prefactor is re-evaluated at every iterate (WI-042 D3).
        n_bar19 = (2.0 * n_D0 * I_line_fuel + 2.0 * n_He0 * I_line_S) / 1e19
        C = C_geo * n_bar19 ** 0.54
        # The one volume-averaged thermal pressure [Pa]: the closed-form fuel
        # term plus the ash-weighted integral.
        p_avg = KEV_TO_J * (
            2.0 * n_D0 * (T_e0 + T_i0) / (1.0 + alpha_n + alpha_T)
            + n_He0 * (2.0 * T_e0 + T_i0) * I_W_S
        )
        W_th = 1.5 * p_avg * V * 1e-6
        tau_E = (C * W_th ** -0.61) ** (1.0 / 0.39)
        return n_D0, n_T0, W_th, tau_E, n_bar19, p_avg

    n_He0 = 0.0
    converged = False
    for _ in range(ASH_CAP):
        n_D0, n_T0, W_th, tau_E, n_bar19, p_avg = state(n_He0)
        n_He_new = (p["f_suppr_ash"] * p["tau_ratio_ash"] * tau_E
                    * n_D0 * n_T0 * sigv_peak)
        if abs(n_He_new - n_He0) < ASH_TOL:
            n_He0 = n_He_new
            converged = True
            break
        n_He0 = 0.5 * (n_He0 + n_He_new)
    if not converged:
        raise RuntimeError("oracle sustainment: ash fixed point did not converge")
    n_D0, n_T0, W_th, tau_E, n_bar19, p_avg = state(n_He0)
    p_fus = n_D0 * n_T0 * fus_I * p["E_fus"] * V * 1e-6

    # The derived electron profile and its diagnostics.
    def n_e(u):
        return 2.0 * n_D0 * (u ** alpha_n) + 2.0 * n_He0 * S(u)

    n_e_volav = 2.0 * n_D0 / (1.0 + alpha_n) + 2.0 * n_He0 * I_vol_S
    alpha_n_e_eff = n_e0 / n_e_volav - 1.0
    xs = []
    ys = []
    for k in range(1, 1701):
        rho_k = k / 2000.0
        u_k = 1.0 - rho_k * rho_k
        xs.append(math.log(u_k))
        ys.append(math.log(S(u_k)))
    mx = sum(xs) / 1700.0
    my = sum(ys) / 1700.0
    sxy = 0.0
    sxx = 0.0
    for x, y in zip(xs, ys):
        sxy += (x - mx) * (y - my)
        sxx += (x - mx) * (x - mx)
    alpha_He_eff = sxy / sxx

    p_brems = (5.35e-37 * p["Z_eff_core"]
               * _trapz_rho(lambda u, rho: (n_e(u) ** 2)
                            * math.sqrt(max(T_e0 * (u ** alpha_T), 1e-9)) * 2.0 * rho)
               * V * 1e-6)
    p_line = (p["f_W_core"]
              * _trapz_rho(lambda u, rho: (n_e(u) ** 2)
                           * _lz_w(T_e0 * (u ** alpha_T)) * 2.0 * rho)
              * V * 1e-6)
    p_sync = _p_sync_albajar(T_e0, n_e0 / 1e20, B, R, a,
                             p["kappa_sync"], p["R_w_sync"], alpha_n_e_eff, alpha_T)
    p_rad = p_brems + p_line + p_sync
    p_alpha_heat = p["f_alpha_fast"] * p["sustain_ash_frac"] * p_fus
    p_aux_required = p_rad + W_th / tau_E - p_alpha_heat
    return dict(n_bar19=n_bar19, n_He0=n_He0, n_D0=n_D0, n_T0=n_T0, T_e0=T_e0,
                W_th=W_th, tau_E=tau_E, p_brems=p_brems, p_line=p_line,
                p_sync=p_sync, p_rad=p_rad, p_alpha_heat=p_alpha_heat,
                p_aux_required=p_aux_required, p_avg=p_avg, n_e_volav=n_e_volav,
                alpha_n_e_eff=alpha_n_e_eff, alpha_He_eff=alpha_He_eff)


# --- Stellaris design-point inputs (from stellarator_plant.sysml bindings) ---
IN = dict(
    # geometry (WI-022 errata rebind: a = 1.3 per the Table 2 image; f_shape
    # targets the printed V = 425, Table 5 image)
    R=12.7, a=1.3, kappa=1.0, pi=3.14159265358979,
    f_shape=1.0031567,
    # radial-build layer thicknesses [m] (WI-021): steady_state_stellarator.yaml
    # (blanket/ht_shield/structure/vessel) + RadialBuild defaults (rest)
    vacuum_t=0.10, firstwall_t=0.05, blanket_t=0.80, reflector_t=0.20,
    ht_shield_t=0.20, structure_t=0.15, gap1_t=0.10, vessel_t=0.10,
    coil_t=0.30, gap2_t=0.10, lt_shield_t=0.15,
    # fusion power (WI-022: sigma_v = 0 -> profile-integrated path; n_e is
    # reference-only in profile mode; profile referents per the spec)
    n_e=3.17e20, sigma_v=0.0, E_fus=2.817e-12,
    T_i0=14.63, alpha_n=0.33, alpha_T=1.19,
    # WI-037: n_D0/n_T0/T_e0/n_He0 retired -- computed by the sustainment
    # chain below (quasi-neutral fuel, converged A.5/A.6 ash, held Ti/Te
    # ratio). n_e0 and T_i0 are the operating-point levers.
    n_e0=5.06e20,   # WI-042: alpha_n_e retired -- the electron profile is derived
    # WI-037 sustainment held facts (image-verified; see stellarator_plant
    # bindings): Fig. 11(a) read, Tables 2/4/5, raw PDF sec. 2.5.
    iota_23=0.92, f_ren=1.0, f_alpha_fast=0.95, tau_ratio_ash=8.0,
    f_suppr_ash=0.5, Z_eff_core=1.20, f_W_core=7.76e-6, Ti_over_Te=0.95,
    sustain_ash_frac=0.2002, R_w_sync=0.6, kappa_sync=1.0,
    beta_mu0=1.25663706212e-6,  # 'Volume-Averaged Beta' default (e_keV retired at WI-042)
    # power balance
    mn=1.2, eta_th=0.333, eta_p=0.5,
    # Heating power chain (WI-039). Wall-plug is the entry point; the source
    # prints the coupled 50 MW, and 100.0 is that value divided by this chain's
    # own stated efficiencies (0.50 x 1.00). eta_couple = 1.00 is the stated
    # deposition assumption (all gyrotron output reaches the plasma), not a
    # sourced coupling figure -- see stellarator_plant.sysml eta_couple_heat.
    p_wallplug_heat=100.0, eta_source_heat=0.50, eta_couple_heat=1.00,
    p_delivered_direct_heat=0.0, p_coupled_direct_heat=0.0,
    # p_pump: 1cfe upstream default 1.0 (1costingFE steady_state_stellarator.yaml:21,
    #   WI-019); re-based to 195.0 by WI-033 [OWNER 2026-08-28] (helium-primary
    #   circulator basis, 6% of p_th; work/completed/20260828_WI-033_p-pump-rebase/).
    #   The oracle mirrors the model's held design-point bindings (module docstring);
    #   edit made under explicit owner ruling 2026-08-29, GSTH Item 6 round p-pump-fence.
    p_pump=195.0, f_sub=0.03,
    # p_tf = 0.0 (WI-024): modeled zero for the SC coil set (recirc_power_factor
    #   = 0 in 1cfe's own SC model; ~7.5 kW joint loss counted as 20 K heat in
    #   the cryo chain). The old 111.0 mapped a phantom "conduction power to
    #   coils" row (111 is the stored magnetic energy in GJ), zeroed at WI-023.
    p_tf=0.0, p_pf=0.0, p_tfcool=15.0, p_pfcool=0.0,
    p_trit=10.0, p_house=4.0,
    # Cryoplant electrical chain (WI-024): derived p_cryo replaces the retired
    #   1cfe generic default 0.8. q_nuc 35.5 W/m^3 (Table 6 image), vol_cold
    #   136.56 m^3 (computed, Table 8 cross-sections x 8 x 25 m), p_fixed
    #   0.0075 MW (sec. 2.9 joints), f_uplift 1.0 (lower-bound seam, D6),
    #   T_cold 20 K (sec. 2.9), T_amb 300 K (D4 assumption), f_carnot 0.20
    #   (THE assumption, D4), p_cryo_direct 0.0 (0.8 default retired, D2).
    q_nuc_cryo=35.5, vol_cold_cryo=0.0, p_fixed_cryo=0.0075,  # WI-036: additive slot; the pack volume is computed
    f_uplift_cryo=1.0, T_cold_cryo=20.0, T_amb_cryo=300.0, f_carnot_cryo=0.20,
    p_cryo_direct=0.0,
    # magnet — B = 9.0 (WI-023): axis-averaged B_0 printed in the Table 2/5
    #   images (the old 5.86 cited a phantom Table 3 text row).
    # magnet (WI-035, inversion): B is COMPUTED from the coil-set current; the
    #   held magnet_B=9.0 is retired. Lever and coil-set facts mirror the
    #   stellarator_plant bindings (Table 2/8 images; design D2/D3/D4/D5).
    magnet_G=78.95683520871486, magnet_R0=12.7,
    magnet_cost_per_kAm=50.0, magnet_coil_markup=5.87,  # 1cfe-form comparison channel
    magnet_n_coils=48.0, magnet_I_coil=15400000.0,
    magnet_k_link=0.7731331164622419, magnet_two_pi=6.283185307179586,
    magnet_f_set=0.8701298701298701, magnet_k_sigma=0.6102331403536223,
    # WI-036: the winding pack is SIZED by the current it carries and the winding
    # length follows machine scale, so wp_side and c_coil are computed here too --
    # the oracle mirrors the model's chain independently. j_wp and k_coil are the
    # float64s of the printed pairs (15.4 MA / 360 mm; 25 m / 12.7 m).
    magnet_j_wp=118.8271604938272, magnet_k_coil=1.9685039370078741,
    magnet_f_wp_vol=0.8780864197530865,
    # WI-036 conductor check: pack modulus, tape load-sharing (from the source's own
    # 600 MPa / <0.2% pair), and the axial irreversible-strain limit.
    magnet_E_wp=200000000000.0, magnet_f_cond=0.6666666666666666,
    magnet_eps_cond_allow=0.004,
    magnet_sigma_allow=800000000.0, magnet_f_wp_fab=6.65,
    magnet_m_casing=63000.0, magnet_steel_price=6.0, magnet_f_steel_fab=3.0,
    # conductor facts (WI-030): peak/axis ratio 24.9/9.0 as its float64 value; REBCO
    # ceiling bound to the Stellaris design value (owner 2026-08-21)
    magnet_peak_ratio=2.7666666666666666, magnet_B_max=24.9,
    mu0=1.25663706212e-6,
    # blanket / shield / structure / vessel / power supplies (unit costs in $)
    # volumes now forward-computed from the radial build (WI-021)
    blanket_unit_cost=600000.0, blanket_structure_factor=1.0,
    shield_unit_cost=740000.0, shield_scale=1.0,
    structure_unit_cost=150000.0,
    vessel_unit_cost=720000.0,
    power_supplies_base=80000000.0,
    p_th_ref=2500.0, p_et_ref=1100.0, alpha_06=0.6, alpha_05=0.5, alpha_07=0.7,
    # divertor
    divertor_base=60000000.0, divertor_p_th_ref=1000.0, divertor_alpha=0.5,
    # heating (ECRH-only)
    heating_ecrh_per_mw=5282900.0,  # p_ecrh retired (WI-039): the chain supplies it
    # BOP per-MW rates ($/MW)
    turbine_per_mw=202840.0, electric_per_mw=86400.0,
    heat_rej_per_mw=35060.0, misc_per_mw=52590.0, n_mod=1.0,
    # forward-computed direct accounts (WI-025) — CAS21 grouped base sums,
    # CAS10 fixed adders, CAS70 O&M reference (concept inputs, $; the stale
    # buildings/preconstruction/annual_om constants are retired)
    bldg_fixed_base=168500000.0, bldg_fus_base=288000000.0,
    bldg_staff_base=9000000.0, bldg_the_base=58000000.0,
    bldg_th_base=26000000.0, bldg_et_base=29000000.0,
    bldg_p_fus_ref=2300.0,  # p_the_ref = p_et_ref = 1100 (no DEC), reused below
    precon_fixed_base=16000000.0, land_intensity=0.25, land_cost=10000.0,
    ref_net_power=1000.0,
    om_annual_ref=54900000.0, om_alpha=0.5, om_direct=0.0,
    # special_materials_capital now computed from blanket_vol (WI-021)
    # rollup rates / financing
    contingency_rate=0.10, indirect_fraction=0.20,
    reference_construction_time=6.0, construction_years=8.0,
    availability=0.85, discount_rate=0.07,
    operational_years=30.0,
    # WI-028 CAS22 tail + CAS40 + CAS50 + CAS28 bases ($; M$ x 1e6) and their
    # account-structural refs/exponents (instance bindings + library defaults).
    remote_handling_base=150000000.0, concept_scale=1.0, rh_p_et_ref=1100.0, rh_alpha=0.5,
    installation_frac=0.14,
    coolant_primary_base=166000000.0, coolant_intermediate_base=40600000.0,
    coolant_ref_net=1000.0, coolant_p_th_ref=3500.0, coolant_alpha=0.55,
    aux_per_mw=1100.0, aux_cryo_base=200000000.0, aux_p_cryo_ref=30.0, aux_alpha=0.7,
    waste_base=1960000.0, waste_ref=1000.0, waste_alpha=1.0,
    fuel_handling_base=120000000.0, fuel_ref=1000.0, fuel_alpha=0.7,
    other_rpe_base=11500000.0, other_ref=1000.0, other_alpha=0.8,
    inc_base=85000000.0, inc_ref=3500.0, inc_alpha=0.65,
    owner_base=41200000.0, owner_ref=1000.0, owner_alpha=0.5,
    supp_spares_frac=0.03, supp_startup_base=40000000.0, supp_decom_base=272000000.0,
    supp_shipping_frac=0.015, supp_tax_frac=0.01, supp_insurance_frac=0.015,
    supp_contingency_rate=0.0,  # CAS50 c59 internal contingency: library default 0.0 (not instance-bound)
    cas28_capital=5000000.0,
    # ---- WI-029 annual-cost side: CAS71 / CAS72 / CAS80 instance bindings ----
    inflation_rate=0.02,
    fuel_cost_per_rxn=1.7260641119988767e-23, fuel_q_eff=17.58,
    mev_to_joules=1.6021766339999998e-13,
    burn_fraction=0.05, fuel_recovery=0.99,
    fluence_limit=18.0,
    # WI-041 source-anchored peak calibration: six printed Stellaris facts (each
    # confirmed against its page image) and the dormant direct term, zeroed.
    wall_peak_q_ref=4.05, wall_peak_p_fus_ref=2700.0, wall_peak_R_ref=12.7,
    wall_peak_a_ref=1.3, wall_peak_kappa_ref=1.0, wall_peak_standoff_ref=0.10,
    wall_peak_calibration_direct=0.0,
)


def _oracle_levelized_replacement_cost(cost_per_event, q_n, fluence_limit,
                                       availability, interest_rate,
                                       operational_years):
    """ORACLE MIRROR of the CAS72 handwritten rung — an independent statement
    of the same guarded chain, NOT an import of the impl.

    Guards carried verbatim from 1cfe (model.py:102-111, economics.py:53-75):
      * inner  max(q_n, 1e-6)          — keeps the 1/q_n gradient finite
      * clip   (0.5, n * availability) — floor first, then cap (jnp.clip order)
      * outer  max(0, ceil(n/t) - 1)   — the first core is capital, not a replacement
    """
    # WI-041: q_n is the wall load handed in -- the plant's PEAK (the oracle
    # computes its own peak below and passes it here); the neutron-power lines
    # that used to sit here are gone with the three inputs they needed.
    fpy_raw = fluence_limit / max(q_n, 1e-6)                      # inner max
    fpy_cap = operational_years * availability
    core_lifetime_fpy = min(max(fpy_raw, 0.5), fpy_cap)           # clip
    core_lifetime_cal = core_lifetime_fpy / availability
    s = (1.0 + interest_rate) ** (-core_lifetime_cal)
    n_rep = max(0.0, float(math.ceil(operational_years / core_lifetime_cal)) - 1.0)
    pv = cost_per_event * s * (1.0 - s ** n_rep) / (1.0 - s)
    disc_pow_n = (1.0 + interest_rate) ** operational_years
    crf = interest_rate * disc_pow_n / (disc_pow_n - 1.0)
    return crf * pv


def compute():
    p = IN
    # --- Plasma Geometry ---
    V = 2.0 * (p["pi"] ** 2) * p["R"] * (p["a"] ** 2) * p["kappa"] * p["f_shape"]
    # --- MFE Radial Build (WI-021; geometry.py torus branch) ---
    vacuum_or = p["a"] + p["vacuum_t"]
    firstwall_or = vacuum_or + p["firstwall_t"]
    blanket_or = firstwall_or + p["blanket_t"]
    reflector_or = blanket_or + p["reflector_t"]
    ht_shield_or = reflector_or + p["ht_shield_t"]
    structure_or = ht_shield_or + p["structure_t"]
    gap1_or = structure_or + p["gap1_t"]
    vessel_or = gap1_or + p["vessel_t"]
    coil_or = vessel_or + p["coil_t"]
    gap2_or = coil_or + p["gap2_t"]
    lt_shield_or = gap2_or + p["lt_shield_t"]
    C = p["kappa"] * 2.0 * (p["pi"] ** 2) * p["R"]
    firstwall_vol = C * ((firstwall_or ** 2) - (vacuum_or ** 2))
    blanket_layer_vol = C * ((blanket_or ** 2) - (firstwall_or ** 2))
    reflector_vol = C * ((reflector_or ** 2) - (blanket_or ** 2))
    ht_shield_vol = C * ((ht_shield_or ** 2) - (reflector_or ** 2))
    lt_shield_vol = C * ((lt_shield_or ** 2) - (gap2_or ** 2))
    blanket_vol = firstwall_vol + blanket_layer_vol + reflector_vol
    shield_vol = ht_shield_vol + lt_shield_vol
    structure_vol = C * ((structure_or ** 2) - (ht_shield_or ** 2))
    vessel_vol = C * ((vessel_or ** 2) - (gap1_or ** 2))
    wall_area = p["kappa"] * 4.0 * (p["pi"] ** 2) * p["R"] * vacuum_or
    r_coil = vessel_or
    # CAS27 PbLi inventory keyed to the computed blanket volume (WI-021)
    special_materials_capital = blanket_vol * 0.50 * 9400.0 * 5.0
    # --- Coil-set field, peak field, winding-pack stress (WI-035; moved ahead
    # of the plasma chain at WI-037 because sustainment reads B_axis) ---
    B_axis = (p["mu0"] * p["magnet_k_link"] * p["magnet_n_coils"] * p["magnet_I_coil"]
              / (p["magnet_two_pi"] * p["magnet_R0"]))
    B_peak = B_axis * p["magnet_peak_ratio"]
    # WI-036: the pack sizes itself from the current, and the winding length from
    # machine scale; both were held inputs before this item.
    wp_side = (p["magnet_I_coil"] / p["magnet_j_wp"]) ** 0.5 / 1000.0
    c_coil = p["magnet_k_coil"] * p["magnet_R0"]
    sigma_wp = p["magnet_k_sigma"] * p["magnet_I_coil"] * B_peak / wp_side
    # WI-036: the conductor's own operand, checked separately from the structure's.
    eps_cond = p["magnet_f_cond"] * sigma_wp / p["magnet_E_wp"]
    # WI-036: a wider pack now costs cold mass, which reaches the cryoplant.
    vol_cold_total = (p["magnet_f_wp_vol"] * p["magnet_n_coils"] * wp_side * wp_side
                      * c_coil + p["vol_cold_cryo"])

    # --- Plasma Sustainment (WI-037): computed ash, quasi-neutral fuel,
    # ISS04 tau_E, composed radiation, required sustained heating ---
    sust = _sustainment(p, V, B_axis)

    # --- DT Fusion Power (WI-022: 0D bypass or profile-integrated; WI-037:
    # the fuel peaks are the sustainment chain's computed values) ---
    if p["sigma_v"] > 0.0:
        p_fus = 0.25 * (p["n_e"] ** 2) * p["sigma_v"] * p["E_fus"] * V * 1.0e-6
    else:
        integral = _profile_integral(p["alpha_n"], p["alpha_T"], p["T_i0"])
        p_fus = sust["n_D0"] * sust["n_T0"] * integral * p["E_fus"] * V * 1.0e-6
    # --- MFE Power Balance (WI-019 faithful form; physics.py:290-328) ---
    p_alpha = (3.52 / 17.58) * p_fus
    p_neutron = p_fus - p_alpha
    p_cool = p["p_tfcool"] + p["p_pfcool"]
    p_aux = p["p_trit"] + p["p_house"]
    p_coils = p["p_tf"] + p["p_pf"]
    # Heating power chain (WI-039), written from the WI-039 design's stated
    # equations rather than from the generated module:
    #   p_delivered      = p_wallplug * eta_source + p_delivered_direct
    #   p_coupled        = p_wallplug * eta_source * eta_couple + p_coupled_direct
    #   eta_pin_eff      = eta_source * eta_couple
    #   p_wallplug_total = p_wallplug + p_coupled_direct / eta_pin_eff
    heat_eta_pin_eff = p["eta_source_heat"] * p["eta_couple_heat"]
    heat_delivered = (p["p_wallplug_heat"] * p["eta_source_heat"]
                      + p["p_delivered_direct_heat"])
    heat_coupled = (p["p_wallplug_heat"] * p["eta_source_heat"] * p["eta_couple_heat"]
                    + p["p_coupled_direct_heat"])
    heat_wallplug_total = (p["p_wallplug_heat"]
                           + p["p_coupled_direct_heat"] / heat_eta_pin_eff)
    p_th = (p["mn"] * p_neutron + p_alpha + heat_coupled
            + p["eta_p"] * p["p_pump"])
    p_the = p["eta_th"] * p_th
    p_et = p_the
    p_sub = p["f_sub"] * p_et
    # Cryoplant electrical chain (WI-024) — mirrors the generated
    # cryoplant_electrical_power_impl.py statement forms verbatim (bit-exact):
    cop_carnot = (p["T_cold_cryo"] / (p["T_amb_cryo"] - p["T_cold_cryo"]))
    cop = (p["f_carnot_cryo"] * cop_carnot)
    p_cold = ((((p["q_nuc_cryo"] * vol_cold_total) * 1e-06) + p["p_fixed_cryo"]) * p["f_uplift_cryo"])
    p_cryo = ((p_cold / cop) + p["p_cryo_direct"])
    recirculating = (p_coils + p["p_pump"] + p_sub + p_aux + p_cool + p_cryo
                     + heat_wallplug_total)
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et

    # --- Account costs ($) ---
    total_kAm = (p["magnet_G"] * B_axis * p["magnet_R0"] * r_coil
                 / (p["mu0"] * 1000.0))
    magnet = total_kAm * p["magnet_cost_per_kAm"] * p["magnet_coil_markup"]
    # WI-035 decomposed magnet accounts (design D4/D5/D6); `magnet` above stays
    # the 1cfe-form comparison channel, the rollup enters the powercore sum.
    kAm_wind = p["magnet_n_coils"] * p["magnet_I_coil"] * p["magnet_f_set"] * c_coil / 1000.0
    winding_pack = kAm_wind * p["magnet_cost_per_kAm"] * p["magnet_f_wp_fab"]
    magnet_structure = p["magnet_n_coils"] * p["magnet_m_casing"] * p["magnet_steel_price"] * p["magnet_f_steel_fab"]
    magnet_capital_rollup = winding_pack + magnet_structure
    blanket = (p["blanket_unit_cost"] * p["blanket_structure_factor"] * blanket_vol
               * (p_th / p["p_th_ref"]) ** p["alpha_06"])
    shield = (p["shield_unit_cost"] * shield_vol * p["shield_scale"]
              * (p_th / p["p_th_ref"]) ** p["alpha_06"])
    structure = (p["structure_unit_cost"] * structure_vol
                 * (p_et / p["p_et_ref"]) ** p["alpha_05"])
    vessel = (p["vessel_unit_cost"] * vessel_vol
              * (p_et / p["p_et_ref"]) ** p["alpha_06"])
    power_supplies = p["power_supplies_base"] * (p_et / p["p_et_ref"]) ** p["alpha_07"]
    divertor = p["divertor_base"] * (p_th / p["divertor_p_th_ref"]) ** p["divertor_alpha"]
    heating = p["heating_ecrh_per_mw"] * heat_delivered  # ECRH-only; others zero
    turbine = p["n_mod"] * p_the * p["turbine_per_mw"]
    electric = p["n_mod"] * p_et * p["electric_per_mw"]
    heat_rejection = p["n_mod"] * p_th * p["heat_rej_per_mw"]
    misc = p["n_mod"] * p_et * p["misc_per_mw"]

    # Forward-computed direct accounts (WI-025) — mirror the generated
    # buildings_cost / precon_cost / om_cost impl statement forms verbatim
    # (bit-exact); p_the_ref = p_et_ref = 1100 (no DEC), n_mod frozen at 1.
    buildings = (((((p["bldg_fixed_base"]
        + (p["bldg_fus_base"] * ((p_fus * p["n_mod"]) / p["bldg_p_fus_ref"])))
        + (p["bldg_staff_base"] * (((p_et * p["n_mod"]) / p["p_et_ref"]) ** 0.5)))
        + (p["bldg_the_base"] * ((p_the * p["n_mod"]) / p["p_et_ref"])))
        + (p["bldg_th_base"] * ((p_th * p["n_mod"]) / p["p_th_ref"])))
        + (p["bldg_et_base"] * ((p_et * p["n_mod"]) / p["p_et_ref"])))
    precon = (((p["land_intensity"] * (((p_net * p["n_mod"]) * p["ref_net_power"]) ** 0.5))
               * p["land_cost"]) + p["precon_fixed_base"])
    # Unlevelized annual O&M (WI-025). WI-029 levelizes it into CAS71 below;
    # it is no longer the DCF numerator itself.
    annual_om_unlevelized = ((p["om_annual_ref"] * (((p_net * p["n_mod"]) / p["ref_net_power"]) ** p["om_alpha"]))
                 + p["om_direct"])

    powercore_capital = (magnet_capital_rollup + heating + divertor + blanket + shield
                         + structure + vessel + power_supplies)
    bop_capital = turbine + electric + heat_rejection + misc

    # --- WI-028 rebuilt overnight assembly (mirrors mfe_plant.sysml D2) ---
    n = p["n_mod"]
    # CAS22 tail accounts ($)
    remote_handling = (p["remote_handling_base"] * p["concept_scale"]
                       * (p_et / p["rh_p_et_ref"]) ** p["rh_alpha"])
    reactor_equipment_subtotal = powercore_capital + remote_handling
    installation = p["installation_frac"] * reactor_equipment_subtotal
    coolant = (p["coolant_primary_base"] * (n * p_net / p["coolant_ref_net"])
               + p["coolant_intermediate_base"] * (n * p_th / p["coolant_p_th_ref"]) ** p["coolant_alpha"])
    # WI-035 D7: the aux and cryoplant terms as their own channels; sum bit-identical.
    aux_cost = p["aux_per_mw"] * (n * p_th)
    cryo_cost = p["aux_cryo_base"] * (p_cryo / p["aux_p_cryo_ref"]) ** p["aux_alpha"]
    aux_cooling = aux_cost + cryo_cost
    waste = p["waste_base"] * (n * p_th / p["waste_ref"]) ** p["waste_alpha"]
    fuel_handling = p["fuel_handling_base"] * (n * p_net / p["fuel_ref"]) ** p["fuel_alpha"]
    other_rpe = p["other_rpe_base"] * (n * p_net / p["other_ref"]) ** p["other_alpha"]
    inc = p["inc_base"] * (n * p_th / p["inc_ref"]) ** p["inc_alpha"]
    cas22_tail_capital = (remote_handling + installation + coolant + aux_cooling
                          + waste + fuel_handling + other_rpe + inc)
    cas22_capital = powercore_capital + cas22_tail_capital
    cas28_capital = p["cas28_capital"]
    # cas2x -> contingency -> cas20 -> indirect -> cas30 (CAS10 NOT in cas2x)
    cas2x_pre_contingency = (buildings + cas22_capital + bop_capital
                             + special_materials_capital + cas28_capital)
    contingency_capital = p["contingency_rate"] * cas2x_pre_contingency
    cas20_capital = cas2x_pre_contingency + contingency_capital
    cas30_capital = (p["indirect_fraction"] * cas20_capital
                     * (p["construction_years"] / p["reference_construction_time"]))
    cas23_to_28_capital = bop_capital + special_materials_capital + cas28_capital
    # CAS40 owner + CAS50 supplementary at overnight (no CAS29/CAS30 on them)
    owner = p["owner_base"] * (n * p_net / p["owner_ref"]) ** p["owner_alpha"]
    supplementary = ((p["supp_shipping_frac"] * cas20_capital
                      + p["supp_spares_frac"] * cas23_to_28_capital
                      + p["supp_tax_frac"] * cas20_capital
                      + p["supp_insurance_frac"] * (cas20_capital + cas30_capital)
                      + p["supp_startup_base"] * (n * p_net / p["ref_net_power"])
                      + p["supp_decom_base"] * (n * p_net / p["ref_net_power"]))
                     * (1.0 + p["supp_contingency_rate"]))
    # CAS10 (precon) enters at overnight (no CAS29/CAS30)
    overnight_capital = (precon + cas20_capital + cas30_capital + owner + supplementary)
    # CAS60 IDC reported line (Option C: NOT summed into total_capital)
    f_idc = ((1.0 + p["discount_rate"]) ** p["construction_years"] - 1.0) \
        / (p["discount_rate"] * p["construction_years"]) - 1.0
    idc_capital = f_idc * overnight_capital
    total_capital = overnight_capital  # Option C
    # legacy aliases (retained for downstream comparison rows)
    indirect_capital = cas30_capital

    # --- WI-029 annual-cost side: CAS71 / CAS72 / CAS80 ---------------------
    # INDEPENDENT re-derivation of the same chains the generated pipeline runs.
    # The CAS72 block below is the ORACLE MIRROR of the handwritten Rung-B impl
    # (generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py)
    # and deliberately carries every 1cfe guard VERBATIM — clip(., 0.5, n*avail),
    # the inner max(q_n, 1e-6), and the outer max(0, ceil(n/t) - 1). A mirror
    # that dropped the guards would be blind to exactly the divergence it
    # exists to catch. It is written out here, not imported from the impl,
    # so the rel-1e-9 assert in run_stellaris_single.py is not vacuous.
    i_rate = p["discount_rate"]
    n_life = p["operational_years"]
    g_infl = p["inflation_rate"]
    t_c = p["construction_years"]

    def _levelized_annual_cost(annual_cost):
        """economics.py:13-50 — growing-annuity PV annuitized by CRF."""
        disc_pow_n_l = (1.0 + i_rate) ** n_life
        crf_l = i_rate * disc_pow_n_l / (disc_pow_n_l - 1.0)
        a1 = annual_cost * (1.0 + g_infl) ** t_c
        pv_l = (a1 * (1.0 - ((1.0 + g_infl) / (1.0 + i_rate)) ** n_life)
                / (i_rate - g_infl))
        return crf_l * pv_l

    cas71_annual = _levelized_annual_cost(annual_om_unlevelized)

    # CAS80 raw annual DT fuel (costs.py:476-544, DT branch), then levelized.
    annual_fuel_raw = (n * p_fus * (3600.0 * 8760.0) * 1.0e6 * p["availability"]
                       * p["fuel_cost_per_rxn"]
                       / (p["fuel_q_eff"] * p["mev_to_joules"]))
    burn_correction = (1.0 + (1.0 - p["burn_fraction"]) / p["burn_fraction"]
                       * (1.0 - p["fuel_recovery"]))
    annual_fuel = annual_fuel_raw * burn_correction
    cas80_annual = _levelized_annual_cost(annual_fuel)

    # --- Neutron wall load: average, source-anchored calibration, peak (WI-041) ---
    # Written from the WI-041 design's table, not transcribed from the generated
    # modules: the average over the oracle's own wall_area; the calibration from
    # the six reference facts through the oracle's own torus-area convention at
    # the source's point; the peak as their product. The peak is what the fence
    # compares and what CAS72's lifetime reads.
    wall_load = p_fus * (1.0 - 0.2002) / wall_area
    A_ref = (p["wall_peak_kappa_ref"] * 4.0 * (p["pi"] ** 2) * p["wall_peak_R_ref"]
             * (p["wall_peak_a_ref"] + p["wall_peak_standoff_ref"]))
    p_n_ref = p["wall_peak_p_fus_ref"] * (1.0 - 0.2002)
    wall_peak_calibration = (p["wall_peak_q_ref"] * A_ref / p_n_ref
                             + p["wall_peak_calibration_direct"])
    wall_load_peak = wall_load * wall_peak_calibration

    replacement_cost_per_event = (blanket + divertor) * n
    cas72_annual = _oracle_levelized_replacement_cost(
        cost_per_event=replacement_cost_per_event,
        q_n=wall_load_peak,
        fluence_limit=p["fluence_limit"], availability=p["availability"],
        interest_rate=i_rate, operational_years=n_life,
    )
    cas70_annual = cas71_annual + cas72_annual
    annual_om = cas70_annual + cas80_annual   # the DCF numerator (WI-029)

    # --- LCOE DCF ($/MWh) ---
    d = p["discount_rate"]
    N = p["operational_years"]
    discount_pow_n = (1.0 + d) ** N
    crf = d * discount_pow_n / (discount_pow_n - 1.0)
    idc_factor = (1.0 + d) ** (p["construction_years"] / 2.0)
    annual_capital = total_capital * idc_factor * crf
    annual_energy_mwh = 8760.0 * p_net * p["availability"]
    lcoe = (annual_capital + annual_om) / annual_energy_mwh

    # --- WI-029 Option (ii): 1cfe-form comparison channels ------------------
    # crf_71 is the CRF the CAS71 levelization computes; the pipeline reuses
    # that same channel, so the mirror reads it the same way.
    disc_pow_n_71 = (1.0 + i_rate) ** n_life
    crf_71 = i_rate * disc_pow_n_71 / (disc_pow_n_71 - 1.0)
    cas90_1cfe = crf_71 * (overnight_capital + idc_capital)
    lcoe_1cfe = ((cas90_1cfe + cas70_annual + cas80_annual)
                 / (8760.0 * p_net * n * p["availability"]))

    # --- Volume-averaged thermal beta and conductor peak field (WI-030) ---
    # WI-042: beta reads the sustainment chain's one volume-averaged pressure
    # ('Volume-Averaged Beta' on p_avg_in) -- W and beta share <p> by construction.
    # WI-035: beta reads the computed axis field (B_peak computed above).
    beta = 2.0 * p["beta_mu0"] * sust["p_avg"] / (B_axis ** 2)

    return dict(
        V=V, p_fus=p_fus, p_th=p_th, p_the=p_the, p_et=p_et,
        p_cryo=p_cryo,  # derived cryoplant electrical (WI-024 chain output)
        q_eng=q_eng, rec_frac=rec_frac, p_net=p_net, wall_load=wall_load,
        wall_peak_calibration=wall_peak_calibration, wall_load_peak=wall_load_peak,  # WI-041
        beta=beta, B_peak=B_peak,  # WI-030 physics channels
        B_axis=B_axis, sigma_wp=sigma_wp,  # WI-035 field + stress channels
        eps_cond=eps_cond,  # WI-036 conductor strain operand
        # WI-037 sustainment channels
        n_bar19=sust["n_bar19"], n_He0=sust["n_He0"], n_D0=sust["n_D0"],
        n_T0=sust["n_T0"], T_e0=sust["T_e0"], W_th=sust["W_th"],
        tau_E=sust["tau_E"], p_brems=sust["p_brems"], p_line=sust["p_line"],
        p_sync=sust["p_sync"], p_rad=sust["p_rad"],
        p_alpha_heat=sust["p_alpha_heat"], p_aux_required=sust["p_aux_required"],
        # WI-042 derived-profile channels
        p_avg=sust["p_avg"], n_e_volav=sust["n_e_volav"],
        alpha_n_e_eff=sust["alpha_n_e_eff"], alpha_He_eff=sust["alpha_He_eff"],
        # WI-039 heating-chain channels
        heat_eta_pin_eff=heat_eta_pin_eff, heat_delivered=heat_delivered,
        heat_coupled=heat_coupled, heat_wallplug_total=heat_wallplug_total,
        winding_pack=winding_pack, magnet_structure=magnet_structure,
        magnet_capital_rollup=magnet_capital_rollup,
        aux_cost=aux_cost, cryo_cost=cryo_cost,  # WI-035 aux split
        magnet=magnet, heating=heating, divertor=divertor, blanket=blanket,
        shield=shield, structure=structure, vessel=vessel,
        power_supplies=power_supplies, turbine=turbine, electric=electric,
        heat_rejection=heat_rejection, misc=misc,
        buildings=buildings, precon=precon,  # forward-computed (WI-025)
        annual_om=annual_om,                 # forward-computed (WI-025)
        special_materials=special_materials_capital,
        powercore_capital=powercore_capital, bop_capital=bop_capital,
        # WI-028 CAS22 tail + CAS40 + CAS50 + CAS60 accounts ($)
        remote_handling=remote_handling, installation=installation,
        coolant=coolant, aux_cooling=aux_cooling, waste=waste,
        fuel_handling=fuel_handling, other_rpe=other_rpe, inc=inc,
        owner=owner, supplementary=supplementary, idc_capital=idc_capital,
        cas22_capital=cas22_capital, cas28_capital=cas28_capital,
        # WI-028 rebuilt rollup aggregates ($)
        cas2x_pre_contingency=cas2x_pre_contingency, cas20_capital=cas20_capital,
        cas30_capital=cas30_capital, cas23_to_28_capital=cas23_to_28_capital,
        overnight_capital=overnight_capital,
        contingency_capital=contingency_capital,
        indirect_capital=indirect_capital, total_capital=total_capital, lcoe=lcoe,
        # WI-029 annual-cost side + Option-(ii) comparison channels ($/yr, $/MWh)
        annual_om_unlevelized=annual_om_unlevelized, annual_fuel=annual_fuel,
        cas71_annual=cas71_annual, cas72_annual=cas72_annual,
        cas70_annual=cas70_annual, cas80_annual=cas80_annual,
        cas90_1cfe=cas90_1cfe, lcoe_1cfe=lcoe_1cfe,
    )


if __name__ == "__main__":
    r = compute()
    for k, v in r.items():
        print(f"{k:22s} {v:,.4f}")
