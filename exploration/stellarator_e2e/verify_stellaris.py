"""Oracle for the Stellaris (concept-09) forward pass.

Pure-Python recompute of the entire SysML MFE plant chain, mirroring the calc
defs line-for-line (models/analyses/mfe_*.sysml + designs/generic_mfe/mfe_plant
+ designs/stellarator_09). Used to check the generated + teax-executed result and
to cross-check against the WI-018 oracle headline numbers.

All monetary values in dollars ($). Inputs are the Stellaris design-point bindings
read from stellarator_plant.sysml.
"""

import math

import oracle_finance as finance
import oracle_breeding as breeding_oracle
import oracle_cooling as cooling_oracle
import oracle_matched_cycle as matched_cycle_oracle
import oracle_facilities as facilities_oracle
import oracle_fuel_inventory as inventory_oracle
import oracle_fuel_processing as processing_oracle

# WI-022 discretization contract — EXACT mirror of the handwritten impl
# (generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py). The
# runner asserts the generated pipeline against this at rel 1e-9; do not
# change one copy without the other.
N_INTERVALS = 200_000


def divertor_account(*, alpha, auxiliary, core_radiation, radiation_fraction,
                     capture_fraction, reference_peak, reference_power, limit,
                     radius, reference_radius, auxiliary_required, installed):
    """Independent WI-065 account; source profile implies area, not a new area lever.

    Source: goal divertor-peak-heat-load/evidence/entering-account.md and its
    original Stellaris p15 witness. This oracle uses aggregate conservation and
    the existing load normalization, without importing generated code.
    """
    quantities = locals().copy()
    if any(not math.isfinite(v) for v in quantities.values()):
        raise ValueError('divertor oracle: nonfinite input')
    nonnegative = (alpha, core_radiation, reference_peak, limit, installed)
    if min(nonnegative) < 0 or min(reference_power, radius, reference_radius) <= 0:
        raise ValueError('divertor oracle: invalid power or normalization')
    if not (0 <= radiation_fraction <= 1 and 0 <= capture_fraction <= 1):
        raise ValueError('divertor oracle: invalid fraction')
    if reference_peak > 0 and capture_fraction == 0:
        raise ValueError('divertor oracle: positive peak with zero capture')
    absorbed = alpha + auxiliary
    if absorbed < 0:
        raise ValueError('divertor oracle: negative absorbed heating')
    if core_radiation > absorbed:
        raise ValueError('divertor oracle: core radiation exceeds absorbed heating')
    separatrix = absorbed - core_radiation
    radiated = radiation_fraction * absorbed
    edge = radiated - core_radiation
    nonradiated = absorbed - radiated
    deposited = capture_fraction * nonradiated
    missed = nonradiated - deposited
    edge_fraction = edge / separatrix if separatrix > 0 else 0.0
    peak = reference_peak * nonradiated / reference_power
    area = capture_fraction * reference_power / reference_peak if reference_peak > 0 else 0.0
    result = dict(p_heat_abs=absorbed, p_sep=separatrix,
                  f_rad_edge=edge_fraction, f_rad_edge_in_range=edge_fraction*(1-edge_fraction),
                  p_target_nonrad=nonradiated, q_target_peak=peak,
                  q_target_peak_area_scaled=peak*reference_radius/radius,
                  q_target_margin=limit-peak,
                  p_heat_operating_minus_installed=auxiliary_required-installed,
                  p_rad_total=radiated, p_rad_edge=edge, p_target_deposited=deposited,
                  p_nonrad_uncaptured=missed, peak_equivalent_area=area,
                  peak_equivalent_area_defined=float(reference_peak > 0),
                  f_rad_edge_defined=float(separatrix > 0),
                  power_account_valid=float(edge >= 0 and auxiliary >= 0))
    if any(not math.isfinite(v) for v in result.values()):
        raise ValueError('divertor oracle: nonfinite arithmetic')
    positive_expected = ((reference_peak > 0, area),
                         (radiation_fraction > 0 and absorbed > 0, radiated),
                         (radiation_fraction < 1 and absorbed > 0, nonradiated),
                         (capture_fraction > 0 and nonradiated > 0, deposited),
                         (capture_fraction < 1 and nonradiated > 0, missed),
                         (reference_peak > 0 and nonradiated > 0, peak),
                         (peak > 0, result['q_target_peak_area_scaled']))
    if any(expected and value <= 0 for expected, value in positive_expected):
        raise ValueError('divertor oracle: positive quantity underflow')
    return result


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
    if B_axis == 0.0:
        raise RuntimeError("oracle sustainment: B_axis must be nonzero for synchrotron and confinement equations")
    n_e0 = p["n_e0"]
    T_i0 = p["T_i0"]
    a = p["a"]
    R = p["R"]
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
    fit_aspect_ratio=1., fit_internal_x=0., fit_internal_y=.025,
    fit_ground=.003, fit_wall=.025, fit_clearance=.002, fit_interior_y=.4,
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
    mn=1.2,
    # WI-045 (goal plant-closure): eta_th, eta_p and p_pump are retired as held
    # scalars. The loop and the cycle are computed below; the five flags/directs
    # select the mode -- live at the instance; the round's compatibility arm binds
    # loop_live 0, cycle_live 0, p_pump_direct 195.0, eta_p_direct 0.5,
    # eta_th_direct 0.333 and reproduces the WI-044 pin bit-for-bit (packet s. 3).
    loop_live=1.0, cycle_live=1.0, p_pump_direct=0.0, eta_p_direct=0.0, eta_th_direct=0.0,
    # The representative circuit (Moscato 2017 reference; WI-045 design D1-D2) and
    # the fit (Kovari 2016 Table 4, helium-primary Rankine row; D4). Mirrors the
    # instance bindings in stellarator_plant.sysml.
    loop_T_in=573.15, loop_dT_blanket=200.0, loop_cp=5193.0, loop_gamma=1.6666666666666667,
    loop_p=8.0e6, n_loops=14.0, mdot_loop_ref=225.07777777777778, dp_loop_ref=329187.1856931558,
    f_loss=1.0, eta_is=0.772796639536644, eta_drive=1.0,
    dT_approach=20.0, a_fit=0.1802, b_fit=0.7823, T_offset_fit=273.0,
    T2_min=384.0, T2_max=642.0, delta_eta=0.0,
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
    #   WI-045 (goal plant-closure): the held 195.0 lives in p_pump_direct above
    #   (0.0 while the loop is live); the loop's own draw replaces it.
    f_sub=0.03,
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
    # WI-062: conditional 20 K perpendicular-field 4 mm / 20 T statistical reference.
    # Source and construction limits: work/active/WI-062_absolute-conductor-current-margin/design.md.
    magnet_reference_tape_current=200.0, magnet_material_factor=1.0,
    magnet_orientation_factor=1.0, magnet_cabling_factor=1.0,
    magnet_degradation_factor=1.0, magnet_sharing_factor=1.0,
    magnet_allowable_fraction=0.8, magnet_allow_field_extrapolation=1.0,
    magnet_G=78.95683520871486,
    magnet_tape_width=0.006, magnet_tape_thickness=0.000056, magnet_tape_price_per_m=20.0,
    magnet_cost_per_kAm=50.0, magnet_coil_markup=5.87,  # 1cfe-form comparison channel
    magnet_n_coils=48.0, magnet_I_coil=15400000.0,
    magnet_k_link=0.7731331164622419, magnet_two_pi=6.283185307179586,
    magnet_f_set=0.8701298701298701, magnet_k_sigma=0.6102331403536223,
    # WI-036: the winding pack is SIZED by the current it carries and the winding
    # length follows machine scale, so wp_side and c_coil are computed here too --
    # the oracle mirrors the model's chain independently. j_wp and c_coil_ref are the
    # float64s of the printed pairs (15.4 MA / 360 mm; 25 m / 12.7 m).
    # WI-058: the winding length follows the coil bore -- c_coil = c_coil_ref * (r_coil_centre /
    # a_coil_ref), anchored at the printed 25 m at the reference bore; k_coil (25.0 / 12.7 over R,
    # WI-036 D3) retires.
    magnet_j_wp=118.8271604938272, magnet_c_coil_ref=25.0,
    magnet_sizing_mode=0.0, magnet_inventory_multiplier=1.0,
    # WI-038: conditional 20 K relative REBCO field law. Reference density is
    # held fixed in the priced-transfer claim; 20–30 T is an extrapolative study window.
    magnet_B_grade_ref=24.9, magnet_field_exponent=0.6,
    magnet_f_wp_vol=0.8780864197530865,
    # WI-036 conductor check: pack modulus, tape load-sharing (from the source's own
    # 600 MPa / <0.2% pair), and the axial irreversible-strain limit.
    magnet_E_wp=200000000000.0, magnet_f_cond=0.6666666666666666,
    magnet_eps_cond_allow=0.004,
    magnet_sigma_allow=800000000.0, magnet_f_wp_fab=6.65,
    # WI-040 design.md: Table 7 image composition; sourced densities and explicit
    # procurement proxies. Winding operations are PROCESS 1990 $/m escalated to
    # estimated 2026 purchasing power, not a complete factory quotation.
    magnet_f_copper=0.35, magnet_f_solder=0.12, magnet_f_steel=0.36, magnet_f_helium=0.08,
    magnet_rho_copper=8940.0, magnet_rho_solder=8390.0, magnet_rho_steel=8000.0,
    magnet_price_copper=11.0, magnet_price_solder=29.23 / 0.45359237,
    magnet_price_steel=6.0,
    magnet_price_helium=(14.0 * 2077.2644 * 288.15 / 101325.0) * (334.4 / 313.7),
    magnet_helium_pressure=1.5e6, magnet_helium_gas_constant=2077.2644,
    magnet_turn_current=50000.0, magnet_winding_rate_1990=480.0,
    magnet_cost_escalation=334.4 / 130.7, magnet_nonplanar_factor=1.9,
    magnet_steel_price=6.0, magnet_f_steel_fab=3.0,
    # WI-063: conditional sheet stock, independent of ground/process unknowns.
    magnet_f_wp_perimeter=0.9351851851851851,
    magnet_insulation_sheet_thickness=0.0005,
    magnet_insulation_sheet_price=61.67720668774671,
    # WI-059: total-support fit (MJ/tonne convention inferred from later thesis).
    magnet_support_coefficient=1.348, magnet_support_exponent=0.78,
    magnet_legacy_casing_fraction=0.0, structure_residual_fraction=1.0,
    cryo_inventory_enabled=True, T_shield_cryo=77.0, f_carnot_shield=0.20,
    cryo_n_leads=12.0, cryo_L0=2.45e-8, cryo_sigma_SB=5.670374419e-8, cryo_f_lead=1.25, cryo_t_case=0.10,
    cryo_shield_area_ratio=1.2, cryo_emittance=0.05, cryo_q_mli=1.0,
    cryo_g_per_coil=0.04, cryo_k_cold=5.39362701769, cryo_k_shield=12.12875814211,
    cryo_joint_drive_fraction=1.0, cryo_q_nuc_structure=0.0, cryo_rho_structure=8000.0,
    # WI-044 coil-bore anchors (the reference point at which the printed magnet facts
    # were read; every sourced shape is normalised to exactly 1.0 there). The held
    # magnet_m_casing is retired: the casing mass is computed from the stored energy.
    magnet_m_casing_ref=63000.0,          # the printed cast-part floor (WI-035 D5 seam)
    magnet_W_mag_ref=111000000000.0,      # Table 2: stored magnetic energy 111 GJ
    magnet_I_ref=15400000.0,              # Table 2: peak coil current 15.4 MA
    magnet_R_ref=12.7,                    # Table 2: major radius
    magnet_a_coil_ref=3.1500000000000004, # the executed coil-centre radius at a = 1.3
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
    # WI-046 (goal plant-closure round 1, 2026-09-08): availability retired as an input --
    # the lifecycle calendar produces it. availability_direct 0.0 = the live calendar;
    # a value in (0, 1] selects the retired periodic chain at that availability (the
    # compatibility bridge: 0.85 reproduces every pre-WI-046 channel to the bit).
    availability_direct=0.0, outage_years=0.5833333333333334, unplanned_fraction=0.0,
    coil_life_fpy=10.0,
    discount_rate=0.07,
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
    # ---- WI-047 (goal plant-closure round 1, 2026-09-08): the fuel-cycle flows, the
    # divertor heat ledger and the exhaust gas load -- the thirteen instance facts.
    # t_recycle READS the cost factor fuel_recovery as the physical recovery of the
    # unburned stream (an owner decision surfaced, goal.md Reserved gates 5); the
    # inventory now follows the WI-069 conditional residence scenario; the divertor case is
    # the source's pessimistic transport case at fixed geometry; p_exhaust 1.0 Pa is
    # DECLARED, not sourced (the required speed is the throughput's own value).
    tbr_floor=1.05,  # WI-066: achieved breeding is computed; this policy floor is retained
    t_recycle=0.99, eta_extract=1.0, lambda_T=1.782785958230312e-09,
    G_stock=0.0, m_T_kg=5.008267663228036e-27,
    f_rad_total=0.9, q_target_ref=9.5, p_nonrad_ref=50.0, q_target_limit=10.0,
    target_capture_fraction=0.99,  # paired with the high source profile; WI-065
    R_ref_divertor=12.7, T_gas=300.0, p_exhaust=1.0,
    # library defaults the two calcs carry (entry points of the LIBRARY_DEFAULT kind)
    s_per_fpy=31536000.0, k_B=1.380649e-23,
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
    n_rep = max(0.0, float(math.ceil(operational_years / core_lifetime_cal)) - 1.0)
    pv = finance.dated_pv(cost_per_event, interest_rate,
                          [k * core_lifetime_cal for k in range(1, int(n_rep) + 1)])
    crf = finance.crf(interest_rate, operational_years)
    return crf * pv


def _oracle_lifecycle_calendar(cost_per_event, q_n, fluence_limit, interest_rate,
                               operational_years, outage_years, unplanned_fraction,
                               coil_life_fpy, availability_direct):
    """ORACLE DERIVATION of 'Lifecycle Calendar' (WI-046, design D1) -- the CLOSED FORM,
    independent of the handwritten impl's interval walk (never an import of it).

    Live mode (availability_direct == 0): the event dates are t_k = k*L/b + (k-1)*d for
    every k whose restart t_k + d falls strictly before N (L = fluence/q_n, b = 1 - u);
    the productive time, downtimes, PV, CAS72, coil margin and the year-binned energy
    ratio are derived FROM THE DATES. Held mode (0 < availability_direct <= 1): the
    retired periodic chain through _oracle_levelized_replacement_cost, with the design's
    D2 readings for the non-cost outputs. Invalid inputs raise, as the impl does.
    """
    N, d, u, C, i = (operational_years, outage_years, unplanned_fraction,
                     cost_per_event, interest_rate)
    if not math.isfinite(availability_direct) or availability_direct < 0.0 or availability_direct > 1.0:
        raise ValueError(f"oracle calendar: availability_direct {availability_direct!r} outside [0, 1]")
    if availability_direct > 0.0:
        A = availability_direct
        cost = _oracle_levelized_replacement_cost(
            cost_per_event=C, q_n=q_n, fluence_limit=fluence_limit, availability=A,
            interest_rate=i, operational_years=N)
        core_lifetime_fpy = min(max(fluence_limit / max(q_n, 1e-6), 0.5), N * A)
        core_lifetime_cal = core_lifetime_fpy / A
        n_rep = max(0.0, float(math.ceil(N / core_lifetime_cal)) - 1.0)
        pv = finance.dated_pv(C, i, [k * core_lifetime_cal for k in range(1, int(n_rep) + 1)])
        F = N * A
        return dict(availability=A, coil_life_margin_fpy=coil_life_fpy - F, replacement_pv=pv,
                    planned_downtime_yr=0.0, terminal_downtime_yr=0.0,
                    unplanned_downtime_yr=N - F, productive_fpy=F, dated_energy_ratio=1.0,
                    cas72_annual=cost, n_replacements=n_rep, physical_life_fpy=core_lifetime_fpy,
                    events=[k * core_lifetime_cal for k in range(1, int(n_rep) + 1)])
    for name, v in dict(q_n=q_n, fluence_limit=fluence_limit, N=N, d=d, u=u, C=C, i=i,
                        coil_life=coil_life_fpy).items():
        if not math.isfinite(v):
            raise ValueError(f"oracle calendar: non-finite input {name}={v!r}")
    if (N <= 0.0 or fluence_limit <= 0.0 or q_n < 0.0 or d < 0.0 or C < 0.0
            or not (0.0 <= u < 1.0) or i <= -1.0):
        raise ValueError("oracle calendar: input outside domain")
    b = 1.0 - u
    L = math.inf if q_n == 0.0 else fluence_limit / q_n
    events = []
    k = 1
    while True:
        t_k = k * L / b + (k - 1) * d
        if t_k >= N or t_k + d >= N:
            break
        events.append(t_k)
        k += 1
    K = len(events)
    t_next = (K + 1) * L / b + K * d          # the next limit's date
    # online segments (the calendar's production intervals), from the dates
    segments = []
    start = 0.0
    for t_k in events:
        segments.append((start, t_k))
        start = t_k + d
    if t_next < N:                             # limit reached, restart not strictly before N
        segments.append((start, t_next))
        online = (K + 1) * L / b
        T_term = N - t_next
    else:                                      # the horizon ends mid-run
        segments.append((start, N))
        online = N - K * d
        T_term = 0.0
    F = b * online
    T_p = K * d
    T_u = u * online
    pv = finance.dated_pv(C, i, events)
    crf = finance.crf(i, N)
    # the year-binned energy ratio (design D3): year y covers (y-1, y]
    if F == 0.0:
        raise ValueError("oracle calendar: zero productive time -- energy undefined")
    n_years = int(math.ceil(N - 1e-12))
    E_avg = F / N
    num = den = 0.0
    for y in range(1, n_years + 1):
        y0, y1 = float(y - 1), min(float(y), N)
        on_y = sum(max(0.0, min(s1, y1) - max(s0, y0)) for s0, s1 in segments)
        disc = finance.growth(i, -y)
        num += b * on_y * disc
        den += E_avg * (y1 - y0) * disc
    return dict(availability=F / N, coil_life_margin_fpy=coil_life_fpy - F, replacement_pv=pv,
                planned_downtime_yr=T_p, terminal_downtime_yr=T_term, unplanned_downtime_yr=T_u,
                productive_fpy=F, dated_energy_ratio=num / den, cas72_annual=crf * pv,
                n_replacements=float(K), physical_life_fpy=L, events=events)


def _validate_winding_pack_magnitudes(current, density):
    if not math.isfinite(current) or current < 0.0:
        raise ValueError("oracle Winding Pack Sizing: I_coil must be finite and nonnegative")
    if not math.isfinite(density) or density <= 0.0:
        raise ValueError("oracle Winding Pack Sizing: j_wp must be finite and positive")


def _winding_pack_side(current, density):
    """Size a square pack in metres from current A and density A/mm²."""
    _validate_winding_pack_magnitudes(current, density)
    return (current / density) ** 0.5 / 1000.0


def _conductor_field_capability(B_design, B_reference, field_exponent, j_reference):
    """Relative envelope quantity and density; no economic multiplier."""
    facts = dict(B_design=B_design, B_reference=B_reference, field_exponent=field_exponent,
                 j_reference=j_reference)
    for name, value in facts.items():
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f'oracle Conductor Field Capability: invalid {name}')
    ratio = B_design / B_reference
    if not math.isfinite(ratio) or ratio <= 0:
        raise ValueError('oracle Conductor Field Capability: invalid field_ratio')
    try:
        quantity = ratio ** field_exponent
    except OverflowError as exc:
        raise ValueError('oracle Conductor Field Capability: invalid quantity_factor') from exc
    if not math.isfinite(quantity) or quantity <= 0:
        raise ValueError('oracle Conductor Field Capability: invalid quantity_factor')
    result = dict(quantity_factor=quantity, j_wp_effective=j_reference / quantity)
    for name, value in result.items():
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f'oracle Conductor Field Capability: invalid {name}')
    return result


def _primary_loop_mass_flow(source_heat, cp, temperature_rise):
    """Return kg/s from source heat MW, specific heat J/kg/K and rise K."""
    if not math.isfinite(cp) or cp <= 0.0:
        raise ValueError("oracle Primary Coolant Loop: cp must be finite and positive")
    if not math.isfinite(temperature_rise) or temperature_rise <= 0.0:
        raise ValueError("oracle Primary Coolant Loop: dT_blanket must be finite and positive")
    return source_heat * 1.0e6 / (cp * temperature_rise)


def _winding_material_inventory(p, volume):
    """Independent WI-040 mass procurement, excluding tape and extra cold volume."""
    facts = {name.removeprefix("magnet_"): value for name, value in p.items()
             if name.startswith("magnet_") and name.removeprefix("magnet_") in {
                 "f_copper", "f_solder", "f_steel", "f_helium", "rho_copper",
                 "rho_solder", "rho_steel", "price_copper", "price_solder",
                 "price_steel", "price_helium", "helium_pressure", "helium_gas_constant"}}
    facts.update(volume_in=volume, temperature=p["T_cold_cryo"])
    for name, value in facts.items():
        positive = name.startswith("rho_") or name in {
            "helium_pressure", "helium_gas_constant", "temperature"}
        if not math.isfinite(value) or (value <= 0.0 if positive else value < 0.0):
            raise ValueError(f"oracle Winding Pack Material Inventory: invalid {name}")
        if name.startswith("f_") and value >= 1.0:
            raise ValueError(f"oracle Winding Pack Material Inventory: invalid {name}")
    fraction = sum(facts["f_" + material] for material in ("copper", "solder", "steel", "helium"))
    if fraction >= 1.0:
        raise ValueError("oracle Winding Pack Material Inventory: fraction sum must be less than one")
    helium_density = facts["helium_pressure"] / (facts["helium_gas_constant"] * facts["temperature"])
    # Keep the authored subtraction sequence: its last bit matters at a zero
    # current-margin predicate. The summed fraction above still checks the domain.
    result = {"helium_density": helium_density, "tape_volume": volume * (
        1.0 - facts["f_copper"] - facts["f_solder"] - facts["f_steel"] - facts["f_helium"])}
    for material in ("copper", "solder", "steel", "helium"):
        density = helium_density if material == "helium" else facts["rho_" + material]
        mass = volume * facts["f_" + material] * density
        result["mass_" + material] = mass
        result["cost_" + material] = mass * facts["price_" + material]
    result["material_cost"] = sum(result["cost_" + material] for material in ("copper", "solder", "steel", "helium"))
    for name, value in result.items():
        if not math.isfinite(value):
            raise ValueError(f"oracle Winding Pack Material Inventory: non-finite {name}")
    return result


def _winding_procurement(p, circumference, material_cost, tape_volume):
    """Direct volume/area purchase from independently computed material inventory."""
    names = ("n_coils", "I_coil", "f_set", "tape_width", "tape_thickness", "tape_price_per_m", "turn_current",
             "winding_rate_1990", "cost_escalation", "nonplanar_factor")
    facts = {name: p["magnet_" + name] for name in names}
    facts.update(c_coil=circumference, material_cost_in=material_cost, tape_volume_in=tape_volume)
    nonnegative = {"I_coil", "tape_volume_in", "tape_price_per_m", "winding_rate_1990", "material_cost_in"}
    for name, value in facts.items():
        if not math.isfinite(value) or (value < 0.0 if name in nonnegative else value <= 0.0):
            raise ValueError(f"oracle Winding Pack Procurement Cost: invalid {name}")
    if facts["f_set"] > 1.0:
        raise ValueError("oracle Winding Pack Procurement Cost: invalid f_set")
    kam = facts["n_coils"] * facts["I_coil"] * facts["f_set"] * circumference / 1000.0
    area = facts['tape_width'] * facts['tape_thickness']
    if not math.isfinite(area) or area <= 0:
        raise ValueError('oracle Winding Pack Procurement Cost: invalid tape_area')
    tape_length = tape_volume / area
    if not math.isfinite(tape_length) or (tape_volume > 0 and tape_length <= 0):
        raise ValueError('oracle Winding Pack Procurement Cost: invalid tape_length')
    tape_cost = tape_length * facts['tape_price_per_m']
    if not math.isfinite(tape_cost) or (tape_length > 0 and facts['tape_price_per_m'] > 0 and tape_cost <= 0):
        raise ValueError('oracle Winding Pack Procurement Cost: invalid tape_cost')
    length = kam * 1000.0 / facts["turn_current"]
    fabrication = length * facts["winding_rate_1990"] * facts["cost_escalation"] * facts["nonplanar_factor"]
    result = dict(tape_length=tape_length, tape_cost=tape_cost, conductor_length=length,
                  winding_fabrication_cost=fabrication, cost=tape_cost + material_cost + fabrication)
    for name, value in result.items():
        if not math.isfinite(value):
            raise ValueError(f"oracle Winding Pack Procurement Cost: non-finite {name}")
    return result


def _insulation_inventory(p, circumference, pack_side, volume):
    """Independent area/perimeter integration for the declared extra-layer scenario.

    Ground is geometry only. Sheet stock includes laminate resin, not installation.
    The effective side distribution is held as physical design inputs change.
    """
    positive = {'circumference': circumference, 'pack_side': pack_side,
        'n_coils': p['magnet_n_coils'], 'aspect_ratio': p['fit_aspect_ratio'],
        'perimeter_factor': p['magnet_f_wp_perimeter'],
        'sheet_thickness': p['magnet_insulation_sheet_thickness']}
    nonnegative = {'volume': volume, 'fx': p['fit_internal_x'],
        'fy': p['fit_internal_y'], 'ground': p['fit_ground'],
        'sheet_price': p['magnet_insulation_sheet_price']}
    for name, value in positive.items():
        if not math.isfinite(value) or value <= 0:
            raise ValueError('oracle insulation: invalid ' + name)
    for name, value in nonnegative.items():
        if not math.isfinite(value) or value < 0:
            raise ValueError('oracle insulation: invalid ' + name)
    if p['magnet_f_wp_perimeter'] > 1:
        raise ValueError('oracle insulation: perimeter_factor exceeds reference maximum')
    def checked(name, value, must_positive=False):
        if not math.isfinite(value) or value < 0 or (must_positive and value == 0):
            raise ValueError('oracle insulation: invalid ' + name)
        return value
    fx, fy = p['fit_internal_x'], p['fit_internal_y']
    # Integrate strips and their corner once; do not subtract near-equal envelopes.
    increment = checked('sheet_fraction', math.fsum([fx, fy, fx*fy]), fx > 0 or fy > 0)
    sheet = checked('internal_volume', volume*increment, volume > 0 and increment > 0)
    root = math.sqrt(p['fit_aspect_ratio'])
    x = checked('mean_x', pack_side*root*p['magnet_f_wp_perimeter'], True)
    y = checked('mean_y', pack_side/root*p['magnet_f_wp_perimeter'], True)
    path = checked('coil_path', p['magnet_n_coils']*circumference, True)
    t = p['fit_ground']
    side_shell = checked('ground_sides', 2*t*(x*(1+fx)+y*(1+fy)), t > 0)
    corners = checked('ground_corners', 4*t*t, t > 0)
    ground = checked('ground_volume', path*math.fsum([side_shell,corners]), t > 0)
    area = checked('sheet_area', sheet/p['magnet_insulation_sheet_thickness'], sheet > 0)
    cost = checked('stock_cost', area*p['magnet_insulation_sheet_price'],
                   area > 0 and p['magnet_insulation_sheet_price'] > 0)
    return dict(internal_volume=sheet, ground_volume=ground, sheet_area=area, stock_cost=cost)


def _coil_thermal_inventory(p, circumference, pack_side):
    """WI-059 independent heat balances; reviewed source forms and scenario inputs.

    Warm refrigeration removes incoming heat minus heat passed to the cold stage.
    Direct Joule electricity is separate from the work needed to refrigerate it.
    Disabled inventory exits before the fixed-endpoint approximation is evaluated.
    """
    names = ('area_cold', 'area_shield', 'q_lead_cold', 'q_lead_shield',
             'q_radiation_cold', 'q_radiation_shield', 'q_support_cold',
             'q_support_shield', 'q_cold', 'q_shield', 'p_drive')
    if not p['cryo_inventory_enabled']:
        return dict.fromkeys(names, 0.0)
    tc, ts, ta = p['T_cold_cryo'], p['T_shield_cryo'], p['T_amb_cryo']
    if not (10 <= tc <= 30 and ts == 77 and ta == 300):
        raise ValueError('oracle coil inventory: require 10 <= T_cold <= 30, T_shield = 77, T_amb = 300 K')
    if not all(0 < p[k] <= 1 for k in ('f_carnot_cryo', 'f_carnot_shield')):
        raise ValueError('oracle coil inventory: require 0 < Carnot fractions <= 1')
    if any(not math.isfinite(p[k]) or p[k] <= 0 for k in ('cryo_L0', 'cryo_sigma_SB')):
        raise ValueError('oracle coil inventory: positive finite physical constants required')
    if not math.isfinite(p['magnet_turn_current']):
        raise ValueError('oracle coil inventory: finite turn current required')
    if any(not math.isfinite(x) or x < 0 for x in (circumference, pack_side)):
        raise ValueError('oracle coil inventory: nonnegative finite surface geometry required')
    nonnegative = ('magnet_n_coils', 'cryo_n_leads', 'cryo_f_lead', 'cryo_t_case',
                   'cryo_shield_area_ratio', 'cryo_emittance', 'cryo_q_mli',
                   'cryo_g_per_coil', 'cryo_k_cold', 'cryo_k_shield',
                   'cryo_joint_drive_fraction', 'p_fixed_cryo')
    if any(not math.isfinite(p[k]) or p[k] < 0 for k in nonnegative):
        raise ValueError('oracle coil inventory: nonnegative finite scenario inputs required')
    if not 0 <= p['cryo_emittance'] <= 1:
        raise ValueError('oracle coil inventory: require 0 <= emittance <= 1')
    area = p['magnet_n_coils'] * circumference * 4 * (pack_side + 2*p['cryo_t_case'])
    shield_area = p['cryo_shield_area_ratio'] * area
    lead_factor = p['cryo_f_lead'] * p['cryo_n_leads'] * abs(p['magnet_turn_current'])
    lead_cold = lead_factor * math.sqrt(p['cryo_L0']*(ts*ts-tc*tc))
    lead_shield = lead_factor * math.sqrt(p['cryo_L0']*(ta*ta-ts*ts))
    radiation_cold = area*p['cryo_emittance']*p['cryo_sigma_SB']*(ts**4-tc**4)
    radiation_shield = shield_area*p['cryo_q_mli']-radiation_cold
    bridge = p['magnet_n_coils']*p['cryo_g_per_coil']
    support_cold = bridge*p['cryo_k_cold']*(ts-tc)
    support_shield = bridge*p['cryo_k_shield']*(ta-ts)-support_cold
    warm = lead_shield+radiation_shield+support_shield
    if not all(math.isfinite(x) for x in (area, shield_area, lead_cold, lead_shield, radiation_cold, radiation_shield, support_cold, support_shield, warm)):
        raise ValueError('oracle coil inventory: nonfinite derived heat or area')
    if warm < 0:
        raise ValueError('oracle coil inventory: negative warm net heat')
    return dict(area_cold=area, area_shield=shield_area,
                q_lead_cold=lead_cold, q_lead_shield=lead_shield,
                q_radiation_cold=radiation_cold, q_radiation_shield=radiation_shield,
                q_support_cold=support_cold, q_support_shield=support_shield,
                q_cold=lead_cold+radiation_cold+support_cold, q_shield=warm,
                p_drive=(lead_cold+lead_shield)*1e-6+p['cryo_joint_drive_fraction']*p['p_fixed_cryo'])


def _current_driven_sizing(p, field, legacy_density):
    """WI-064 independent inversion: tape capacity per composite area sets density.

    Required quantities are minimum continuous reference-conductor inventory;
    extra inventory is a physical multiplier, never an acceptance relaxation.
    """
    mode = p['magnet_sizing_mode']
    multiplier = p['magnet_inventory_multiplier']
    if mode not in (0, 1) or not math.isfinite(multiplier) or multiplier < 1:
        raise ValueError('oracle current sizing: invalid mode or inventory multiplier')
    fractions = [p['magnet_f_' + k] for k in ('copper', 'solder', 'steel', 'helium')]
    if any(not math.isfinite(v) or v < 0 for v in fractions) or sum(fractions) >= 1:
        raise ValueError('oracle current sizing: invalid composition')
    for value in (legacy_density, p['magnet_I_coil'], p['magnet_turn_current']):
        if not math.isfinite(value) or value <= 0:
            raise ValueError('oracle current sizing: invalid loading')
    # The independently implemented existing performance/domain calculation supplies
    # single-tape current only; no generated sizing or final inventory is consumed.
    capacity = _conductor_current(p, field, 1.0, 1.0)['tape_critical_current']
    for factor in ('cabling_factor', 'degradation_factor', 'sharing_factor'):
        capacity *= p['magnet_' + factor]
    tape_area = p['magnet_tape_width'] * p['magnet_tape_thickness']
    try:
        # Preserve the authored continuous-inventory operation sequence rather
        # than algebraically cancelling it at an exact acceptance boundary.
        required_tapes = p['magnet_turn_current'] / (p['magnet_allowable_fraction'] * capacity)
        conductor_area = required_tapes * tape_area / (1-sum(fractions))
        pack_area = (p['magnet_I_coil'] / p['magnet_turn_current']) * conductor_area
        density = p['magnet_I_coil'] / (pack_area * 1e6)
        selected = legacy_density if mode == 0 else density / multiplier
    except (ZeroDivisionError, OverflowError) as exc:
        raise ValueError('oracle current sizing: invalid arithmetic') from exc
    out = dict(required_tapes=required_tapes, required_conductor_area=conductor_area,
               required_pack_area=pack_area, required_effective_density=density,
               selected_effective_density=selected, tape_available_current=capacity)
    if any(not math.isfinite(v) or v <= 0 for v in out.values()):
        raise ValueError('oracle current sizing: nonpositive/nonfinite output')
    return out


def _winding_fit(p, selected_area=None):
    """Independent area-demand construction and conditional available-space screen."""
    pos = ('fit_aspect_ratio', 'fit_wall', 'fit_interior_y', 'coil_t')
    nonneg = ('fit_internal_x', 'fit_internal_y', 'fit_ground', 'fit_clearance')
    for key in pos + nonneg:
        if not math.isfinite(p[key]) or (p[key] <= 0 if key in pos else p[key] < 0):
            raise ValueError('oracle winding fit: invalid ' + key)
    # Reconstruct the demand directly rather than reading native sizing/fit intermediates.
    factor = (p['magnet_B_max'] / p['magnet_B_grade_ref']) ** p['magnet_field_exponent']
    area = (p['magnet_I_coil'] / (p['magnet_j_wp'] / factor) / 1e6
            if selected_area is None else selected_area)
    if not math.isfinite(area) or area <= 0:
        raise ValueError('oracle winding fit: invalid nominal area')
    side = math.sqrt(area)
    orientation = math.sqrt(p['fit_aspect_ratio'])
    result = {'nominal_x': side * orientation, 'nominal_y': side / orientation,
              'cavity_x': p['coil_t'] - 2*p['fit_wall'], 'cavity_y': p['fit_interior_y'],
              'exterior_x': p['coil_t'], 'exterior_y': p['fit_interior_y'] + 2*p['fit_wall']}
    for axis in ('x', 'y'):
        nominal = result['nominal_' + axis]
        added = nominal * p['fit_internal_' + axis]
        if p['fit_internal_' + axis] > 0 and added == 0:
            raise ValueError('oracle winding fit: internal_' + axis + ' underflow')
        result['internal_' + axis] = added
        result['pack_' + axis] = nominal + added
        result['insulated_' + axis] = nominal + added + 2*p['fit_ground']
        result['required_' + axis] = nominal + added + 2*p['fit_ground'] + 2*p['fit_clearance']
        result['margin_' + axis] = result['cavity_' + axis] - result['required_' + axis]
    for key, value in result.items():
        if not math.isfinite(value) or (value <= 0 and not key.startswith(('margin_', 'internal_'))):
            raise ValueError('oracle winding fit: invalid ' + key)
    result["minimum_margin"] = min(result["margin_x"], result["margin_y"])
    return result


def _conductor_current(p, field, tape_length, conductor_length):
    """Independent absolute-current estimate; continuous inventory counts, amperes.

    The material reference is fixed at 4 mm, 20 K, 20 T and 56 micrometres.
    The field exponent is source-derived independently of the sizing envelope.
    """
    facts = {key: p['magnet_' + key] for key in (
        'reference_tape_current', 'material_factor', 'orientation_factor',
        'cabling_factor', 'degradation_factor', 'sharing_factor',
        'allowable_fraction', 'allow_field_extrapolation', 'tape_width',
        'tape_thickness', 'f_set', 'f_wp_vol', 'turn_current')}
    facts.update(field=field, temperature=p['T_cold_cryo'],
                 tape_length=tape_length, conductor_length=conductor_length)
    for key, value in facts.items():
        if not math.isfinite(value) or (value <= 0 and key != 'allow_field_extrapolation'):
            raise ValueError('oracle conductor current: invalid ' + key)
    if facts['temperature'] != 20 or facts['tape_thickness'] != 0.000056:
        raise ValueError('oracle conductor current: unsupported temperature/construction')
    if not 0.004 <= facts['tape_width'] <= 0.006:
        raise ValueError('oracle conductor current: unsupported width')
    if facts['allow_field_extrapolation'] not in (0, 1):
        raise ValueError('oracle conductor current: invalid extrapolation switch')
    if not 20 <= field <= 32 or (field > 24 and facts['allow_field_extrapolation'] != 1):
        raise ValueError('oracle conductor current: unsupported field')
    for key in ('cabling_factor', 'degradation_factor', 'sharing_factor', 'allowable_fraction'):
        if facts[key] > 1:
            raise ValueError('oracle conductor current: invalid ' + key)

    def positive(value):
        if not math.isfinite(value) or value <= 0:
            raise ValueError('oracle conductor current: arithmetic overflow/underflow')
        return value

    # Validate each multiplication to prevent compensating extreme factors hiding underflow.
    tape_current = positive(facts['reference_tape_current'] * (facts['tape_width'] / 0.004))
    for factor in ((field / 20) ** -0.6, facts['material_factor'], facts['orientation_factor']):
        tape_current = positive(tape_current * factor)
    n_set = positive(tape_length / conductor_length)
    n_ref = positive(positive(n_set * facts['f_set']) / facts['f_wp_vol'])
    critical = {}
    for label, count in (('reference', n_ref), ('set', n_set)):
        capacity = positive(count * tape_current)
        for key in ('cabling_factor', 'degradation_factor', 'sharing_factor'):
            capacity = positive(capacity * facts[key])
        critical[label] = capacity
    fraction_ref = positive(facts['turn_current'] / critical['reference'])
    fraction_set = positive(facts['turn_current'] / critical['set'])
    allowed = positive(facts['allowable_fraction'] * critical['reference'])
    result = dict(parallel_tapes_set=n_set, parallel_tapes_reference=n_ref,
                  tape_critical_current=tape_current,
                  critical_current_reference=critical['reference'], critical_current_set=critical['set'],
                  operating_fraction_reference=fraction_ref, operating_fraction_set=fraction_set,
                  allowable_current=allowed, margin_fraction=facts['allowable_fraction'] - fraction_ref,
                  margin_current=allowed - facts['turn_current'], field_extrapolated=float(field > 24))
    if not all(math.isfinite(value) for value in result.values()):
        raise ValueError('oracle conductor current: nonfinite output')
    return result


# WI-067 explicit current equipment scenario; legacy comparisons override both selectors.
IN.update({
    'cooling_enabled': True,
    'cooling_layout_multiplier': 1,
    'cooling_tube_wall': 0.0015,
    'cooling_shell_wall': 0.2,
    'cooling_accessory_mass': 10000,
    'cooling_secondary_head': 40,
    'cooling_eta_p': 0.75,
    'cooling_eta_motor': 0.95,
    'cooling_machine_life': 10,
    'cooling_bundle_life': 15,
    'cooling_makeup_fraction': 0.001,
    'cooling_inventory_reserve': 0.1,
    'cooling_removal_multiplier': 1,
    'cooling_saltprice_source_choice': 0,
    'cooling_costscale': 1,
    'cooling_fabrication_rate_2017': 310,
    'cooling_cost_mode': 1.0,
    'cooling_energy_mode': 1.0,
})


IN.update({'facility_'+key:value for key,value in facilities_oracle.DEFAULTS.items()})
IN.update({'inventory_'+key:value for key,value in inventory_oracle.DEFAULTS.items()})
PROCESSING_DEFAULTS = {'enabled': True, 'source_conditions': True, 'capacity_margin': 1.0, 'price_multiplier': 1.0, 'reference_flow': 2.08e-05, 'exponent': 0.3, 'target_cpi': 321.9, 'transfer_capital': 111000.0, 'transfer_installation': 112000.0, 'transfer_cpi': 60.6, 'cleanup_capital': 1000000.0, 'cleanup_installation': 70000.0, 'cleanup_cpi': 82.4, 'distiller_capital': 1237000.0, 'distiller_installation': 63000.0, 'distiller_cpi': 65.2, 'containment_capital': 182000.0, 'containment_installation': 30000.0, 'containment_cpi': 82.4}
IN.update({'processing_'+key:value for key,value in PROCESSING_DEFAULTS.items()})

# WI-073 selected physical facts; current design defaults, not hidden solver constants.
IN.update({
    'matched_cycle_enabled': 1.0, 'cooling_water_enabled': 1.0,
    'matched_main_pressure_MPa': 6.2, 'matched_extraction_pressure_MPa': .8,
    'matched_steam_temperature_C': 445., 'matched_reheat_temperature_C': 445.,
    'matched_condenser_temperature_C': 42., 'matched_eta_hp': .9, 'matched_eta_lp': .9,
    'matched_eta_condensate_pump': .8, 'matched_eta_feedwater_pump': .8,
    'matched_eta_pump_motor': .95, 'matched_eta_mechanical': .99, 'matched_eta_generator': .98,
    'matched_salt_hot_C': 465., 'matched_salt_cp_kJ_kgK': 1.560,
    'cw_water_inlet_C': 25., 'cw_water_outlet_C': 35., 'cw_head_m': 20.,
    'cw_eta_pump': .8, 'cw_eta_motor': .95,
})

def compute():
    if "magnet_R0" in IN:
        raise ValueError("retired oracle input magnet_R0; use plant R")
    if "tbr" in IN:
        raise ValueError("retired oracle input tbr; achieved breeding is computed")
    if "I_total" in IN:
        raise ValueError("retired oracle input I_total; inventory is computed")
    p = IN
    for mode in ('cooling_cost_mode', 'cooling_energy_mode'):
        if not math.isfinite(p[mode]) or p[mode] not in (0., 1.):
            raise ValueError('oracle cooling modes must be finite binary selectors')
    if (p['cooling_cost_mode'] or p['cooling_energy_mode']) and not p['cooling_enabled']:
        raise ValueError('oracle selected cooling effects require enabled equipment')
    # WI-072: active facility layout requires positive cooling inventories,
    # as its existing native domain does; disabled equipment supplies zeros.
    if p['facility_facilities_enabled'] and not p['cooling_enabled']:
        raise ValueError('oracle active facilities require enabled cooling equipment')
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
    # WI-044: the coil-centre minor radius -- eq. 39's / eq. 2.82's a_coil (design D1) --
    # and the reported aspect ratio.
    r_coil_centre = vessel_or + p["coil_t"] / 2.0
    A = p["R"] / p["a"]
    # CAS27 PbLi inventory keyed to the computed blanket volume (WI-021)
    special_materials_capital = blanket_vol * 0.50 * 9400.0 * 5.0
    # --- Coil-set field, peak field, winding-pack stress (WI-035; moved ahead
    # of the plasma chain at WI-037 because sustainment reads B_axis) ---
    B_axis = (p["mu0"] * p["magnet_k_link"] * p["magnet_n_coils"] * p["magnet_I_coil"]
              / (p["magnet_two_pi"] * p["R"]))
    # WI-044: the peak field sees the coil bore. Lion 2021 eq. 39 has the field on the
    # coil rising as R / (R - a_coil); with B_axis ~ N I / R the peak/axis ratio carries
    # that factor. The printed ratio is the anchor at the reference geometry, the factor
    # is applied normalised there (exactly 1.0 at the design point), and the winding-pack
    # term of eq. 39 is not carried (a1(C) unprinted, design D2).
    if not p["R"] - r_coil_centre > 0.0:
        raise ValueError("oracle: live magnet clearance R - r_coil_centre must be > 0")
    if not p["magnet_R_ref"] - p["magnet_a_coil_ref"] > 0.0:
        raise ValueError("oracle: reference magnet clearance R_ref - a_coil_ref must be > 0")
    bore_factor = p["R"] / (p["R"] - r_coil_centre)
    bore_factor_ref = p["magnet_R_ref"] / (p["magnet_R_ref"] - p["magnet_a_coil_ref"])
    bore_norm = bore_factor / bore_factor_ref
    B_peak = B_axis * p["magnet_peak_ratio"] * bore_norm
    # WI-044: stored magnetic energy from the coil-set inductance shape, thesis eq. 2.82
    # L = L(C) (a_coil/a_ref)^2 (R_ref/R) with W = 1/2 L I^2, anchored at the printed 111 GJ.
    W_mag = (p["magnet_W_mag_ref"] * (p["magnet_I_coil"] / p["magnet_I_ref"]) ** 2
             * (r_coil_centre / p["magnet_a_coil_ref"]) ** 2 * (p["magnet_R_ref"] / p["R"]))
    # WI-044: casing mass from stored energy, Lion 2021 eq. 56 M = 1.348 W^0.78 with the
    # constant absorbed by the anchor (no units printed); the 63 t floor keeps its seam.
    m_casing = p["magnet_m_casing_ref"] * (W_mag / p["magnet_W_mag_ref"]) ** 0.78
    for key in ('magnet_support_coefficient', 'cryo_q_nuc_structure'):
        if not math.isfinite(p[key]) or p[key] < 0:
            raise ValueError('oracle coil support: nonnegative finite coefficient/heating required')
    if not math.isfinite(p['cryo_rho_structure']) or p['cryo_rho_structure'] <= 0:
        raise ValueError('oracle coil support: positive finite structure density required')
    if p['magnet_support_coefficient'] > 0 and (not math.isfinite(p['magnet_support_exponent']) or p['magnet_support_exponent'] <= 0):
        raise ValueError('oracle coil support: positive finite active exponent required')
    for key in ('magnet_legacy_casing_fraction', 'structure_residual_fraction', 'cryo_joint_drive_fraction'):
        if not math.isfinite(p[key]) or not 0 <= p[key] <= 1:
            raise ValueError('oracle coil support: accounting fractions must lie in [0,1]')
    support_mass = (1000*p["magnet_support_coefficient"]*(W_mag/1e6)**p["magnet_support_exponent"]) if p["magnet_support_coefficient"] else 0.0
    if not math.isfinite(support_mass) or support_mass < 0:
        raise ValueError('oracle coil support: nonnegative finite support mass required')
    # WI-036: the pack sizes itself from the current; WI-058: the winding length follows
    # the coil bore (WI-036 had it follow the major radius); both were held inputs before.
    # Preserve existing public current/density diagnostic precedence. The reference
    # density changes inventory conditionally; no absolute current margin is established.
    _validate_winding_pack_magnitudes(p["magnet_I_coil"], p["magnet_j_wp"])
    grade = _conductor_field_capability(p['magnet_B_max'], p['magnet_B_grade_ref'],
                                       p['magnet_field_exponent'], p['magnet_j_wp'])
    current_sizing = _current_driven_sizing(p, B_peak, grade['j_wp_effective'])
    effective_density = current_sizing['selected_effective_density']
    wp_side = _winding_pack_side(p["magnet_I_coil"], effective_density)
    # WI-058 (design D2/D3): the printed circumference at the reference bore times the bore ratio;
    # exactly 25.0 at the design point (the same float over itself); R does not enter.
    c_coil = p["magnet_c_coil_ref"] * (r_coil_centre / p["magnet_a_coil_ref"])
    if wp_side == 0.0:
        raise ValueError("oracle Winding Pack Stress: wp_side must be nonzero")
    sigma_wp = p["magnet_k_sigma"] * p["magnet_I_coil"] * B_peak / wp_side
    # WI-036: the conductor's own operand, checked separately from the structure's.
    eps_cond = p["magnet_f_cond"] * sigma_wp / p["magnet_E_wp"]
    # WI-036: a wider pack now costs cold mass, which reaches the cryoplant.
    vol_cold_total = (p["magnet_f_wp_vol"] * p["magnet_n_coils"] * wp_side * wp_side
                      * c_coil + p["vol_cold_cryo"])
    vol_winding_pack = p["magnet_f_wp_vol"] * p["magnet_n_coils"] * wp_side * wp_side * c_coil
    # WI-040 shares this state with inventory. Preserve the pre-existing public
    # cryoplant diagnostic before invoking the new inventory consumer.
    if not 0.0 < p["T_cold_cryo"] < p["T_amb_cryo"]:
        raise ValueError("oracle cryoplant: require 0 < T_cold < T_amb")
    inventory = _winding_material_inventory(p, vol_winding_pack)
    # Independent expanded quantity path, avoiding the native square-root/volume chain.
    tape_volume_direct = (p['magnet_I_coil'] * grade['quantity_factor']
        * p['magnet_n_coils'] * p['magnet_f_wp_vol'] * c_coil
        * (1 - sum(p['magnet_f_' + m] for m in ('copper', 'solder', 'steel', 'helium')))
        / (1e6 * p['magnet_j_wp']))
    if p['magnet_sizing_mode'] == 1:
        tape_volume_direct = (current_sizing['required_pack_area'] * p['magnet_inventory_multiplier']
            * p['magnet_n_coils'] * p['magnet_f_wp_vol'] * c_coil
            * (1 - sum(p['magnet_f_' + m] for m in ('copper', 'solder', 'steel', 'helium'))))
    # Retain the independently expanded quantity as a cross-check. Exact
    # predicates use the authored sqrt/volume sequence, never a snapped margin.
    if not math.isclose(tape_volume_direct, inventory['tape_volume'], rel_tol=1e-12):
        raise ValueError('oracle expanded tape volume disagrees with inventory')
    procurement = _winding_procurement(p, c_coil, inventory['material_cost'], inventory['tape_volume'])

    insulation = _insulation_inventory(p, c_coil, wp_side, vol_winding_pack)
    conductor = _conductor_current(p, B_peak, procurement['tape_length'], procurement['conductor_length'])

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
    thermal = _coil_thermal_inventory(p, c_coil, wp_side)
    p_tf_total = p["p_tf"] + thermal['p_drive']
    p_coils = p_tf_total + p["p_pf"]
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
    # Signed sustained operation, with installed capacity retained above.
    operating_heat_coupled = sust["p_aux_required"]
    operating_heat_delivered = operating_heat_coupled / p["eta_couple_heat"]
    operating_heat_wallplug = operating_heat_delivered / p["eta_source_heat"]
    # --- WI-045 (goal plant-closure): the reactor source heat, the representative
    # primary loop and the temperature-compatible cycle, written from the WI-045
    # design's stated equations (D1-D5, D9), not from the generated modules.
    #   q_source   = mn*p_neutron + p_alpha + p_coupled           (no pump credit)
    #   mdot       = q_source*1e6/(cp*dT);  mdot_loop = mdot/n_loops
    #   dp_loop    = f_loss*dp_ref*(mdot_loop/mdot_loop_ref)^2;  r = p/(p - dp)
    #   T_comp_in  = T_in/(1 + (r^k - 1)/eta_is);  w_fluid = mdot*cp*(T_in - T_comp_in)/1e6
    #   p_elec     = w_fluid/eta_drive;  q_ihx = q_source + w_fluid
    #   p_pump_total      = loop_live*p_elec + p_pump_direct
    #   q_recovered_total = loop_live*w_fluid + eta_p_direct*p_pump_direct
    #   eta_fit    = a*ln(T2_C + 273) - b - delta_eta;  eta_th = cycle_live*eta_fit + eta_th_direct
    # In the dormant mode the two totals are the old held scalars to the bit
    # (0.0*x + held), so the sums below are the pre-WI-045 sums exactly.
    q_source = p["mn"] * p_neutron + p_alpha + operating_heat_coupled
    loop_mdot = _primary_loop_mass_flow(q_source, p["loop_cp"], p["loop_dT_blanket"])
    loop_T_out = p["loop_T_in"] + p["loop_dT_blanket"]
    loop_mdot_loop = loop_mdot / p["n_loops"]
    loop_dp_loop = p["f_loss"] * p["dp_loop_ref"] * (loop_mdot_loop / p["mdot_loop_ref"]) ** 2
    loop_p_loop_margin = p["loop_p"] - loop_dp_loop
    # WI-047 (T-006's named shared-line edit on WI-045's block): outside the loss
    # law's domain the compressor ratio's fractional power takes a complex root and
    # the seam surfaced it as a raw TypeError (goal plant-closure T-005 return). The
    # package records execution_failed there; the oracle now DECLARES it, in the
    # sustainment chain's own pattern (RuntimeError "oracle ...", recorded by the
    # study pre-screen as a reason), so a screen classifies the region instead of
    # crashing. WI-045's expected text stands on either side of these three lines.
    if loop_p_loop_margin <= 0.0:
        raise RuntimeError("oracle loop: pressure domain -- the per-path loss exceeds the loop pressure (p_loop_margin <= 0)")
    loop_r_comp = p["loop_p"] / (p["loop_p"] - loop_dp_loop)
    loop_k_isen = (p["loop_gamma"] - 1.0) / p["loop_gamma"]
    loop_T_comp_in = p["loop_T_in"] / (1.0 + (loop_r_comp ** loop_k_isen - 1.0) / p["eta_is"])
    loop_w_fluid = loop_mdot * p["loop_cp"] * (p["loop_T_in"] - loop_T_comp_in) / 1.0e6
    loop_p_elec = loop_w_fluid / p["eta_drive"]
    loop_q_ihx = q_source + loop_w_fluid
    loop_capacity_margin = p["mdot_loop_ref"] - loop_mdot_loop
    loop_p_pump_total = p["loop_live"] * loop_p_elec + p["p_pump_direct"]
    loop_q_recovered_total = (p["loop_live"] * loop_w_fluid
                              + p["eta_p_direct"] * p["p_pump_direct"])
    cycle_T2_C = loop_T_out - p["dT_approach"] - 273.15
    cycle_eta_fit = (p["a_fit"] * math.log(cycle_T2_C + p["T_offset_fit"])
                     - p["b_fit"] - p["delta_eta"])
    cycle_eta_th = p["cycle_live"] * cycle_eta_fit + p["eta_th_direct"]
    # Independent WI-067 equipment oracle, upstream of all cost/performance consumers.
    cooling = cooling_oracle.calculate({
        'enabled': p['cooling_enabled'],
        'layout_multiplier': p['cooling_layout_multiplier'],
        'tube_wall': p['cooling_tube_wall'],
        'shell_wall': p['cooling_shell_wall'],
        'accessory_mass': p['cooling_accessory_mass'],
        'secondary_head': p['cooling_secondary_head'],
        'eta_p': p['cooling_eta_p'],
        'eta_motor': p['cooling_eta_motor'],
        'machine_life': p['cooling_machine_life'],
        'bundle_life': p['cooling_bundle_life'],
        'makeup_fraction': p['cooling_makeup_fraction'],
        'inventory_reserve': p['cooling_inventory_reserve'],
        'removal_multiplier': p['cooling_removal_multiplier'],
        'saltprice_source_choice': p['cooling_saltprice_source_choice'],
        'costscale': p['cooling_costscale'],
        'fabrication_rate_2017': p['cooling_fabrication_rate_2017'],
        'n_mod': p['n_mod'], 'n_loops': p['n_loops'],
        'mdot_loop': loop_mdot_loop, 'dp_loop': loop_dp_loop,
        'helium_suction_K': loop_T_comp_in, 'helium_discharge_Pa': p['loop_p'],
        'helium_hot_K': loop_T_out, 'helium_cp': p['loop_cp'], 'helium_gamma': p['loop_gamma'],
        'primary_shaft_MW': loop_w_fluid, 'primary_electric_MW': loop_p_elec,
        'q_ihx_MW': loop_q_ihx, 'years': p['operational_years'],
        'discount': p['discount_rate'], 'sourcefitargument_C': cycle_T2_C,
    })
    cooling.update(hx_shell_bore=3.2 if p['cooling_enabled'] else 0.,
                   hx_shell_wall=p['cooling_shell_wall'] if p['cooling_enabled'] else 0.,
                   hx_shell_length=13. if p['cooling_enabled'] else 0.,
                   hx_tube_length=11.6 if p['cooling_enabled'] else 0.)
    cooling_electric_total = loop_p_pump_total + p['cooling_energy_mode'] * cooling['salt_electric_MW']
    cooling_recovered_total = loop_q_recovered_total + p['cooling_energy_mode'] * cooling['salt_shaft_MW']

    cycle_margin_low = cycle_T2_C - p["T2_min"]
    cycle_margin_high = p["T2_max"] - cycle_T2_C
    cycle_domain_product = cycle_margin_low * cycle_margin_high
    # Original-table independent state calculation follows the salt producer.
    matched_cycle = matched_cycle_oracle.matched_interface({
        'enabled': p['matched_cycle_enabled'],
        'heat_available_MW': cooling['conversion_heat_MW'],
        'source_heat_MW': q_source,
        'selected_recovered_MW': cooling_recovered_total,
        'salt_flow_per_circuit': cooling['salt_flow'],
        'salt_circuit_count': cooling['ihx_count'],
        'salt_return_C': cooling['salt_return_C'],
        **{name: p['matched_'+name] for name in (
            'salt_hot_C', 'salt_cp_kJ_kgK', 'main_pressure_MPa', 'extraction_pressure_MPa',
            'steam_temperature_C', 'reheat_temperature_C', 'condenser_temperature_C',
            'eta_hp', 'eta_lp', 'eta_condensate_pump', 'eta_feedwater_pump',
            'eta_pump_motor', 'eta_mechanical', 'eta_generator')},
    })
    cooling_water = matched_cycle_oracle.cooling_interface({
        'enabled': p['cooling_water_enabled'], 'cycle_active': p['matched_cycle_enabled'],
        'q_rejection_before_cooling_MW': matched_cycle['q_rejection_before_cooling_MW'],
        'condenser_temperature_C': p['matched_condenser_temperature_C'],
        **{name:p['cw_'+name] for name in ('water_inlet_C','water_outlet_C','head_m','eta_pump','eta_motor')},
    })
    cycle_selection = matched_cycle_oracle.selection_interface({
        'matched_enabled': p['matched_cycle_enabled'], 'legacy_eta': cycle_eta_th,
        'matched_eta': matched_cycle['eta_gross'], 'legacy_domain_product': cycle_domain_product,
    })
    p_th = (p["mn"] * p_neutron + p_alpha + operating_heat_coupled
            + cooling_recovered_total)
    p_the = cycle_selection['eta_selected'] * p_th
    p_et = p_the
    p_sub = p["f_sub"] * p_et
    # Cryoplant electrical chain (WI-024) — mirrors the generated
    # cryoplant_electrical_power_impl.py statement forms verbatim (bit-exact):
    cop_carnot = (p["T_cold_cryo"] / (p["T_amb_cryo"] - p["T_cold_cryo"]))
    cop = (p["f_carnot_cryo"] * cop_carnot)
    structure_nuclear = p['cryo_q_nuc_structure']*support_mass/p['cryo_rho_structure']*1e-6
    p_cold = ((p["q_nuc_cryo"]*vol_cold_total*1e-6+p["p_fixed_cryo"]+structure_nuclear)
              *p["f_uplift_cryo"]+thermal['q_cold']*1e-6)
    p_cryo_cold = p_cold/cop+p["p_cryo_direct"]
    p_cryo_shield = (thermal['q_shield']*1e-6*(p['T_amb_cryo']-p['T_shield_cryo'])
                     /(p['f_carnot_shield']*p['T_shield_cryo'])) if p['cryo_inventory_enabled'] else 0.0
    p_cryo = p_cryo_cold+p_cryo_shield
    recirculating = (p_coils + cooling_electric_total + p_sub + p_aux + p_cool + p_cryo
                     + operating_heat_wallplug)
    # Zero-demand branch preserves the historical floating-point expression.
    if matched_cycle['p_cycle_pumps_MW'] != 0 or cooling_water['p_cooling_pump_electric_MW'] != 0:
        recirculating += matched_cycle['p_cycle_pumps_MW'] + cooling_water['p_cooling_pump_electric_MW']
    q_eng = p_et / recirculating
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et

    # --- Account costs ($) ---
    total_kAm = (p["magnet_G"] * B_axis * p["R"] * r_coil
                 / (p["mu0"] * 1000.0))
    magnet = total_kAm * p["magnet_cost_per_kAm"] * p["magnet_coil_markup"]
    # WI-035 decomposed magnet accounts (design D4/D5/D6); `magnet` above stays
    # the 1cfe-form comparison channel, the rollup enters the powercore sum.
    kAm_wind = p["magnet_n_coils"] * p["magnet_I_coil"] * p["magnet_f_set"] * c_coil / 1000.0
    winding_pack_legacy = kAm_wind * p["magnet_cost_per_kAm"] * p["magnet_f_wp_fab"]
    winding_pack = procurement["cost"]
    magnet_structure = (p["magnet_legacy_casing_fraction"]*p["magnet_n_coils"]*m_casing+support_mass)*p["magnet_steel_price"]*p["magnet_f_steel_fab"]
    support_effective_all_in_rate = p["magnet_steel_price"] * p["magnet_f_steel_fab"]
    for name in ("magnet_steel_price", "magnet_f_steel_fab"):
        if not math.isfinite(p[name]) or p[name] < 0:
            raise ValueError("oracle support rate: invalid " + name)
    if not math.isfinite(support_effective_all_in_rate):
        raise ValueError("oracle support rate: nonfinite product")
    magnet_capital_rollup = winding_pack + magnet_structure + insulation["stock_cost"]
    blanket = (p["blanket_unit_cost"] * p["blanket_structure_factor"] * blanket_vol
               * (p_th / p["p_th_ref"]) ** p["alpha_06"])
    shield = (p["shield_unit_cost"] * shield_vol * p["shield_scale"]
              * (p_th / p["p_th_ref"]) ** p["alpha_06"])
    structure_legacy_cost = (p["structure_unit_cost"] * structure_vol
                 * (p_et / p["p_et_ref"]) ** p["alpha_05"])
    structure = p["structure_residual_fraction"] * structure_legacy_cost
    vessel = (p["vessel_unit_cost"] * vessel_vol
              * (p_et / p["p_et_ref"]) ** p["alpha_06"])
    power_supplies = p["power_supplies_base"] * (p_et / p["p_et_ref"]) ** p["alpha_07"]
    divertor = p["divertor_base"] * (p_th / p["divertor_p_th_ref"]) ** p["divertor_alpha"]
    heating = p["heating_ecrh_per_mw"] * heat_delivered  # ECRH-only; others zero
    turbine = p["n_mod"] * p_the * p["turbine_per_mw"]
    electric = p["n_mod"] * p_et * p["electric_per_mw"]
    heat_rejection = p["n_mod"] * p_th * p["heat_rej_per_mw"]
    misc = p["n_mod"] * p_et * p["misc_per_mw"]

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

    replacement_cost_per_event = (blanket + divertor) * p["n_mod"]
    # WI-046: one lifecycle calendar produces availability and CAS72 (the closed form
    # above); the periodic chain survives as its held mode.
    cal = _oracle_lifecycle_calendar(
        cost_per_event=replacement_cost_per_event, q_n=wall_load_peak,
        fluence_limit=p["fluence_limit"], interest_rate=p["discount_rate"], operational_years=p["operational_years"],
        outage_years=p["outage_years"], unplanned_fraction=p["unplanned_fraction"],
        coil_life_fpy=p["coil_life_fpy"], availability_direct=p["availability_direct"],
    )

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
    # WI-068: independent facilities geometry and interval inventories.
    facilities = facilities_oracle.layout(
        {key:p['facility_'+key] for key in facilities_oracle.DEFAULTS},
        dict(n_mod=p['n_mod'], major_radius=p['R'], minor_outer_radius=lt_shield_or,
             blanket_volume=blanket_vol, calendar_mode=p['availability_direct'],
             calendar_years=p['operational_years'], calendar_outage=p['outage_years'],
             cooling_helium_count=cooling['circulator_count'], cooling_salt_count=cooling['salt_pump_count'],
             cooling_bundle_count=cooling['ihx_count'], cooling_circuits=cooling['ihx_count'],
             cooling_machine_life=p['cooling_machine_life'], cooling_bundle_life=p['cooling_bundle_life'],
             hx_tube_length=11.6, hx_shell_bore=3.2, hx_shell_wall=p['cooling_shell_wall'], hx_shell_length=13.),
        cal['events'])
    buildings_legacy, precon_legacy = buildings, precon
    facility_mode = p['facility_facilities_cost_mode']
    buildings = (1-facility_mode)*buildings_legacy + facility_mode*facilities['layout_buildings_capital']
    precon = (1-facility_mode)*precon_legacy + facility_mode*(p['precon_fixed_base']+facilities['layout_land_cost'])
    facility_exclusion = facility_mode*(1+p['contingency_rate'])*facilities['installed_facility_capital']
    # Unlevelized annual O&M (WI-025). WI-029 levelizes it into CAS71 below;
    # it is no longer the DCF numerator itself.
    annual_om_unlevelized = ((p["om_annual_ref"] * (((p_net * p["n_mod"]) / p["ref_net_power"]) ** p["om_alpha"]))
                 + p["om_direct"])

    powercore_capital = (magnet_capital_rollup + heating + divertor + blanket + shield
                         + structure + vessel + power_supplies)
    bop_capital = turbine + electric + heat_rejection + misc

    breeding = breeding_oracle.response(p)
    inventory_parameters = {key: p['inventory_'+key] for key in inventory_oracle.DEFAULTS}
    inventory_parameters['enabled'] = inventory_parameters.pop('inventory_enabled')
    inventory_parameters.update(
        p_fus=p_fus, q_eff=p['fuel_q_eff'], mev_to_joules=p['mev_to_joules'],
        burn_fraction=p['burn_fraction'], t_recycle=p['t_recycle'],
        tbr_available=breeding['tbr_mean'], breeding_defined=breeding['defined_flag'],
        eta_extract=p['eta_extract'], lambda_T=p['lambda_T'], G_stock=p['G_stock'],
        m_T_kg=p['m_T_kg'], plasma_volume=V, n_T0=sust['n_T0'],
        alpha_n=p['alpha_n'], availability=cal["availability"])
    fuel_inventory = inventory_oracle.evaluate(**inventory_parameters)

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
    coolant_legacy = coolant
    coolant = (1 - p['cooling_cost_mode']) * coolant_legacy + p['cooling_cost_mode'] * cooling['installed_total']
    aux_cooling = aux_cost + cryo_cost
    waste = p["waste_base"] * (n * p_th / p["waste_ref"]) ** p["waste_alpha"]
    fuel_handling_legacy = p["fuel_handling_base"] * (n * p_net / p["fuel_ref"]) ** p["fuel_alpha"]
    processing = processing_oracle.calculate({key:p['processing_'+key] for key in PROCESSING_DEFAULTS} | dict(
        flow=fuel_inventory['dt_processor_kg_s'], inventory_enabled=p['inventory_inventory_enabled'],
        n_mod=n, legacy_cost=fuel_handling_legacy))
    fuel_handling = processing['cost']
    processing_exclusion = (1 + p['contingency_rate']) * processing['installation_total']
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
    supplementary = ((p["supp_shipping_frac"] * (cas20_capital - p["cooling_cost_mode"] * cooling["delivered_total"] - facility_exclusion - processing_exclusion)
                      + p["supp_spares_frac"] * cas23_to_28_capital
                      + p["supp_tax_frac"] * cas20_capital
                      + p["supp_insurance_frac"] * (cas20_capital + cas30_capital)
                      + p["supp_startup_base"] * (n * p_net / p["ref_net_power"])
                      + p["supp_decom_base"] * (n * p_net / p["ref_net_power"]))
                     * (1.0 + p["supp_contingency_rate"]))
    # CAS10 (precon) enters at overnight (no CAS29/CAS30)
    overnight_capital = (precon + cas20_capital + cas30_capital + owner + supplementary)
    # CAS60 IDC reported line (Option C: NOT summed into total_capital)
    f_idc = finance.idc_factor(p["discount_rate"], p["construction_years"])
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
        return finance.annuity(annual_cost, i_rate, g_infl, n_life, t_c)

    cooling_om_total = annual_om_unlevelized + p["cooling_cost_mode"] * cooling["consumables_annual"]
    cas71_annual = _levelized_annual_cost(cooling_om_total)


    availability = cal["availability"]
    cas72_annual = cal["cas72_annual"] + p["cooling_cost_mode"] * cooling["replacement_annual"]
    # (WI-046: the fuel block moved below the calendar -- it reads the calendar's availability)
    # CAS80 raw annual DT fuel (costs.py:476-544, DT branch), then levelized.
    annual_fuel_raw = (n * p_fus * (3600.0 * 8760.0) * 1.0e6 * availability
                       * p["fuel_cost_per_rxn"]
                       / (p["fuel_q_eff"] * p["mev_to_joules"]))
    burn_correction = (1.0 + (1.0 - p["burn_fraction"]) / p["burn_fraction"]
                       * (1.0 - p["fuel_recovery"]))
    annual_fuel = annual_fuel_raw * burn_correction
    cas80_annual = _levelized_annual_cost(annual_fuel)
    cas70_annual = cas71_annual + cas72_annual
    annual_om = cas70_annual + cas80_annual   # the DCF numerator (WI-029)

    # --- WI-047 (goal plant-closure): the fuel-cycle flows, the divertor heat ledger
    # and the exhaust gas load, written from the WI-047 design's stated equations
    # (D1-D7), not from the generated modules.
    #   E_fus_J      = q_eff*mev_to_joules;  burn = p_fus*1e6/E_fus_J;  inject = burn/f_burn
    #   exhaust      = inject - burn;  loss = (1 - t_recycle)*exhaust
    #   tbr_required = (burn + loss + lambda_T*I_total + G_stock)/(eta_extract*burn)
    #   p_heat_abs   = p_alpha_heat + p_coupled (sustained operating basis);  p_sep = p_heat_abs - p_rad_core
    #   f_rad_edge   = (f_total*p_heat_abs - p_rad_core)/p_sep;  p_target = p_heat_abs - f_total*p_heat_abs
    #   q_peak       = q_ref*p_target/p_nonrad_ref;  shadow = q_peak*R_ref/R
    #   n_molecules  = (D + T)/2 + He;  Q = n*k_B*T_gas;  S_eff = Q/p_exhaust
    fuel_E_fus_J = p["fuel_q_eff"] * p["mev_to_joules"]
    fuel_burn_rate = p_fus * 1.0e6 / fuel_E_fus_J
    fuel_inject_rate = fuel_burn_rate / p["burn_fraction"]
    fuel_exhaust_rate = fuel_inject_rate - fuel_burn_rate
    fuel_loss_rate = (1.0 - p["t_recycle"]) * fuel_exhaust_rate
    fuel_tbr_required = ((fuel_burn_rate + fuel_loss_rate + p['lambda_T']*fuel_inventory['total_atoms'] + p['G_stock'])
                         / (p['eta_extract']*fuel_burn_rate))
    # Raw margin is undefined whenever the coupled adequacy flag is zero.
    fuel_tbr_margin = breeding['tbr_mean'] - fuel_tbr_required
    breeding_adequacy = breeding_oracle.adequacy(
        mean=breeding['tbr_mean'], lower=breeding['tbr_lower'], defined=breeding['defined_flag'],
        floor=p['tbr_floor'], required=fuel_tbr_required, burn=fuel_burn_rate,
        loss=fuel_loss_rate, extraction=p['eta_extract'], decay_constant=p['lambda_T'],
        inventory=fuel_inventory['total_atoms'], growth=p['G_stock'], burn_fraction=p['burn_fraction'],
        recycle=p['t_recycle'])
    fuel_burn_kg_per_fpy = fuel_burn_rate * p["m_T_kg"] * p["s_per_fpy"]
    divheat = divertor_account(
        alpha=sust["p_alpha_heat"], auxiliary=operating_heat_coupled,
        core_radiation=sust["p_rad"], radiation_fraction=p["f_rad_total"],
        capture_fraction=p["target_capture_fraction"], reference_peak=p["q_target_ref"],
        reference_power=p["p_nonrad_ref"], limit=p["q_target_limit"],
        radius=p["R"], reference_radius=p["R_ref_divertor"],
        auxiliary_required=sust["p_aux_required"], installed=heat_coupled)
    vacuum_n_molecules = (fuel_exhaust_rate + fuel_exhaust_rate) / 2.0 + fuel_burn_rate
    vacuum_Q_total = vacuum_n_molecules * p["k_B"] * p["T_gas"]
    vacuum_S_eff_required = vacuum_Q_total / p["p_exhaust"]

    # --- LCOE DCF ($/MWh) ---
    d = p["discount_rate"]
    N = p["operational_years"]
    crf = finance.crf(d, N)
    idc_factor = finance.growth(d, p["construction_years"] / 2.0)
    annual_capital = total_capital * idc_factor * crf
    annual_energy_mwh = 8760.0 * p_net * availability
    lcoe = (annual_capital + annual_om) / annual_energy_mwh

    # --- WI-029 Option (ii): 1cfe-form comparison channels ------------------
    # crf_71 is the CRF the CAS71 levelization computes; the pipeline reuses
    # that same channel, so the mirror reads it the same way.
    crf_71 = finance.crf(i_rate, n_life)
    cas90_1cfe = crf_71 * (overnight_capital + idc_capital)
    lcoe_1cfe = ((cas90_1cfe + cas70_annual + cas80_annual)
                 / (8760.0 * p_net * n * availability))

    # --- Volume-averaged thermal beta and conductor peak field (WI-030) ---
    # WI-042: beta reads the sustainment chain's one volume-averaged pressure
    # ('Volume-Averaged Beta' on p_avg_in) -- W and beta share <p> by construction.
    # WI-035: beta reads the computed axis field (B_peak computed above).
    beta = 2.0 * p["beta_mu0"] * sust["p_avg"] / (B_axis ** 2)

    return dict(
        # WI-072: expose independently computed intermediates for complete
        # native-channel verification. No generated result supplies these values.
        coverage_annual_total=annual_om,
        coverage_cas70=cas70_annual,
        coverage_cas71_crf=crf_71,
        coverage_cas71_levelized=cas71_annual,
        coverage_cas80_crf=crf_71,
        coverage_cas80_levelized=cas80_annual,
        coverage_cooling_cost_mode=p['cooling_cost_mode'],
        coverage_cooling_energy_mode=p['cooling_energy_mode'],
        coverage_cooling_consumables=p['cooling_cost_mode'] * cooling['consumables_annual'],
        coverage_cooling_replacements=p['cooling_cost_mode'] * cooling['replacement_annual'],
        coverage_cooling_shipping=p['cooling_cost_mode'] * cooling['delivered_total'],
        coverage_coil_length=c_coil,
        coverage_wp_side=wp_side,
        coverage_cold_volume=vol_cold_total,
        coverage_blanket_volume=blanket_vol,
        coverage_outer_radius=lt_shield_or,
        coverage_coil_inner_radius=r_coil,
        coverage_shield_volume=shield_vol,
        coverage_structure_volume=structure_vol,
        coverage_vessel_volume=vessel_vol,
        coverage_wall_area=wall_area,
        coverage_replacement_event=replacement_cost_per_event,
        **{"conductor_" + key: value for key, value in conductor.items()},
        **{"fit_" + key: value for key, value in _winding_fit(p, None if p["magnet_sizing_mode"] == 0 else current_sizing["required_pack_area"] * p["magnet_inventory_multiplier"]).items()},
        **{"sizing_" + key: value for key, value in current_sizing.items()},
        V=V, p_fus=p_fus, p_th=p_th, p_the=p_the, p_et=p_et,
        p_cryo=p_cryo, p_cryo_cold=p_cryo_cold, p_cryo_shield=p_cryo_shield,
        support_mass=support_mass, p_tf_total=p_tf_total, p_cold=p_cold,
        structure_nuclear=structure_nuclear*1e6, structure_legacy_cost=structure_legacy_cost,
        **{'thermal_'+name: value for name, value in thermal.items()},
        q_eng=q_eng, rec_frac=rec_frac, p_net=p_net, wall_load=wall_load,
        wall_peak_calibration=wall_peak_calibration, wall_load_peak=wall_load_peak,  # WI-041
        beta=beta, B_peak=B_peak,  # WI-030 physics channels
        B_axis=B_axis, sigma_wp=sigma_wp,  # WI-035 field + stress channels
        eps_cond=eps_cond,  # WI-036 conductor strain operand
        # WI-044 coil-bore channels: the stored energy, the computed casing mass, the
        # coil-centre radius the shapes take, and the reported aspect ratio
        W_mag=W_mag, m_casing=m_casing, r_coil_centre=r_coil_centre, A=A,
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
        operating_heat_coupled=operating_heat_coupled,
        operating_heat_delivered=operating_heat_delivered,
        operating_heat_wallplug=operating_heat_wallplug,
        heat_eta_pin_eff=heat_eta_pin_eff, heat_delivered=heat_delivered,
        heat_coupled=heat_coupled, heat_wallplug_total=heat_wallplug_total,
        # WI-045 source-heat, loop and cycle channels
        q_source=q_source,
        loop_mdot=loop_mdot, loop_T_out=loop_T_out, loop_mdot_loop=loop_mdot_loop,
        loop_dp_loop=loop_dp_loop, loop_p_loop_margin=loop_p_loop_margin,
        loop_r_comp=loop_r_comp, loop_T_comp_in=loop_T_comp_in,
        loop_w_fluid=loop_w_fluid, loop_p_elec=loop_p_elec, loop_q_ihx=loop_q_ihx,
        loop_capacity_margin=loop_capacity_margin,
        loop_p_pump_total=loop_p_pump_total, loop_q_recovered_total=loop_q_recovered_total,
        cycle_T2_C=cycle_T2_C, cycle_eta_fit=cycle_eta_fit, cycle_eta_th=cycle_eta_th,
        cycle_margin_low=cycle_margin_low, cycle_margin_high=cycle_margin_high,
        cycle_domain_product=cycle_domain_product,
        **{'matched_'+name:value for name,value in matched_cycle.items()},
        **{'cw_'+name:value for name,value in cooling_water.items()},
        **{'cycle_selection_'+name:value for name,value in cycle_selection.items()},
        winding_pack=winding_pack, magnet_structure=magnet_structure,
        support_effective_all_in_rate=support_effective_all_in_rate,
        **{"insulation_" + name: value for name, value in insulation.items()},
        winding_pack_legacy=winding_pack_legacy, vol_winding_pack=vol_winding_pack,
        **{'conductor_' + name: value for name, value in grade.items()},
        **{"winding_" + name: value for name, value in inventory.items()},
        tape_length=procurement["tape_length"],
        tape_procurement_cost=procurement["tape_cost"],
        conductor_length=procurement["conductor_length"],
        winding_fabrication_cost=procurement["winding_fabrication_cost"],
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
        coolant=coolant, coolant_legacy=coolant_legacy, aux_cooling=aux_cooling, waste=waste,
        cooling_electric_total=cooling_electric_total, cooling_recovered_total=cooling_recovered_total,
        cooling_om_total=cooling_om_total,
        **{'cooling_' + name: value for name, value in cooling.items()},
        **{'facility_' + name: value for name, value in facilities.items()},
        buildings_legacy=buildings_legacy, precon_legacy=precon_legacy, facility_exclusion=facility_exclusion,
        facility_site_allowance=facilities['active']*p['facility_retained_site_improvements'],
        facility_initial_sector_start_days=p['facility_initial_sector_start_days'],
        facility_cooling_initial_handoff_days=p['facility_cooling_initial_handoff_days'],
        shipping_cooling_exclusion=p['cooling_cost_mode']*cooling['delivered_total'],
        shipping_facility_exclusion=facility_exclusion,
        shipping_remaining_base=cas20_capital-p['cooling_cost_mode']*cooling['delivered_total']-facility_exclusion-processing_exclusion,
        fuel_handling_legacy=fuel_handling_legacy,
        shipping_fuel_installation_exclusion=processing_exclusion,
        **{'processing_'+key:value for key,value in processing.items()},
        fuel_handling=fuel_handling, other_rpe=other_rpe, inc=inc,
        owner=owner, supplementary=supplementary, idc_capital=idc_capital,
        reactor_equipment_subtotal=reactor_equipment_subtotal,
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
        # WI-046 lifecycle calendar channels (the closed-form derivation)
        calendar_availability=cal["availability"],
        calendar_coil_life_margin_fpy=cal["coil_life_margin_fpy"],
        calendar_replacement_pv=cal["replacement_pv"],
        calendar_planned_downtime_yr=cal["planned_downtime_yr"],
        calendar_terminal_downtime_yr=cal["terminal_downtime_yr"],
        calendar_unplanned_downtime_yr=cal["unplanned_downtime_yr"],
        calendar_productive_fpy=cal["productive_fpy"],
        calendar_dated_energy_ratio=cal["dated_energy_ratio"],
        calendar_cas72_annual=cal["cas72_annual"],
        calendar_n_replacements=cal["n_replacements"],
        calendar_physical_life_fpy=cal["physical_life_fpy"],
        cas70_annual=cas70_annual, cas80_annual=cas80_annual,
        cas90_1cfe=cas90_1cfe, lcoe_1cfe=lcoe_1cfe,
        # WI-047 fuel / divertor-heat / vacuum channels
        fuel_burn_rate=fuel_burn_rate, fuel_inject_rate=fuel_inject_rate,
        fuel_exhaust_rate=fuel_exhaust_rate, fuel_loss_rate=fuel_loss_rate,
        fuel_tbr_required=fuel_tbr_required, fuel_tbr_margin=fuel_tbr_margin,
        fuel_burn_kg_per_fpy=fuel_burn_kg_per_fpy,
        **{'inventory_' + name: value for name, value in fuel_inventory.items()},
        **{'breeding_' + name: value for name, value in breeding.items()},
        **{'breeding_adequacy_' + name: value for name, value in breeding_adequacy.items()},
        **{"divheat_" + name: value for name, value in divheat.items()},
        vacuum_n_molecules=vacuum_n_molecules, vacuum_Q_total=vacuum_Q_total,
        vacuum_S_eff_required=vacuum_S_eff_required,
    )


def reconstruct_divertor_source_case(f_rad_total=0.9, q_target_ref=9.5, p_nonrad_ref=50.0):
    """WI-047 (spec MR-WI047-9): the source's own divertor case reconstructed in the
    oracle's ledger arithmetic -- a reconstruction at the source's point, not a
    validation of the fixed-geometry scaling off it. Stellaris section 2.6 (text
    lines 1219-1246; render stellaris_p15_divertor.png): 90 % of the net core
    heating radiated, 500 MW -> 50 MW to the divertor; peaks 9.5 (200 eV, 1 m^2/s)
    and 5.0 (100 eV, 3 m^2/s) MW/m^2 at that 50 MW; both below the adopted 10.
    With p_rad_core = 0 the whole radiated share is the edge's (f_rad_edge = 0.9).
    Written p - f*p so 500 - 450 = 50 exactly and 9.5*50/50 = 9.5 exactly (design D4).
    """
    p_heat_abs = 500.0
    p_rad_core = 0.0
    p_sep = p_heat_abs - p_rad_core
    f_rad_edge = (f_rad_total * p_heat_abs - p_rad_core) / p_sep
    p_target_nonrad = p_heat_abs - f_rad_total * p_heat_abs
    q_peak = q_target_ref * p_target_nonrad / p_nonrad_ref
    q_peak_low = 5.0 * p_target_nonrad / p_nonrad_ref
    p_target_doubled = 2.0 * p_heat_abs - f_rad_total * (2.0 * p_heat_abs)
    q_peak_doubled = q_target_ref * p_target_doubled / p_nonrad_ref
    return dict(p_heat_abs=p_heat_abs, p_sep=p_sep, f_rad_edge=f_rad_edge,
                p_target_nonrad=p_target_nonrad, q_peak=q_peak, q_peak_low=q_peak_low,
                q_peak_doubled=q_peak_doubled)


def reconstruct_reference_circuit(eta_is=None):
    """WI-045 MR-WI045-13: the Moscato 2017 reference circuit reconstructed in the
    oracle's own arithmetic -- a reconstruction of the source's numbers at the
    source's point, NOT a validation of the loop law off design.

    Printed (output.md:79-81, :89-91, Table 2 :128, Table 3 :151-154; raw p. 6):
    2101.7 MW blanket heat at 2025.7 kg/s over 300->500 C in 9 loops; per-path
    losses IB 214+62+87.9 = 363.9 kPa, OB 174+56.6+85.1 = 315.7 kPa; IHX duties
    3x208.1 + 6x267.8 = 2231.1 MW; circulators 3x2x6.8 + 6x2x7.5 = 130.8 MW.
    """
    cp = IN["loop_cp"]
    Q_ref, mdot_ref, n_ref = 2101.7, 2025.7, 9.0
    dT = 200.0
    cp_implied = Q_ref * 1.0e6 / (mdot_ref * dT)
    dp_ib = (214.0 + 62.0 + 87.9) * 1e3
    dp_ob = (174.0 + 56.6 + 85.1) * 1e3
    w_ib, w_ob = 3.0 * 208.1, 6.0 * 267.8
    dp_weighted = (w_ib * dp_ib + w_ob * dp_ob) / (w_ib + w_ob)
    Q_ihx = 3.0 * 208.1 + 6.0 * 267.8
    W_check = Q_ihx - Q_ref
    P_circ_printed = 3.0 * 2.0 * 6.8 + 6.0 * 2.0 * 7.5
    p_loop, gamma = IN["loop_p"], IN["loop_gamma"]
    k = (gamma - 1.0) / gamma
    r = p_loop / (p_loop - dp_weighted)
    T_in = IN["loop_T_in"]
    dT_actual = W_check * 1.0e6 / (mdot_ref * cp)
    T1 = T_in - dT_actual
    eta_is_closed = (r ** k - 1.0) * T1 / dT_actual
    eta = IN["eta_is"] if eta_is is None else eta_is
    # the loop law at the reference per-loop flow (ratio 1): the same statements as compute()
    mdot_loop = mdot_ref / n_ref
    dp_loop = 1.0 * dp_weighted * (mdot_loop / IN["mdot_loop_ref"]) ** 2
    r_comp = p_loop / (p_loop - dp_loop)
    T_comp_in = T_in / (1.0 + (r_comp ** k - 1.0) / eta)
    w_fluid = mdot_ref * cp * (T_in - T_comp_in) / 1.0e6
    return dict(
        cp_bound=cp, cp_implied=cp_implied, cp_discrepancy=(cp_implied - cp) / cp,
        dp_ib_kPa=dp_ib / 1e3, dp_ob_kPa=dp_ob / 1e3, dp_weighted_kPa=dp_weighted / 1e3,
        Q_ihx_MW=Q_ihx, W_check_MW=W_check, P_circ_printed_MW=P_circ_printed,
        residual_printed_minus_fluid_MW=P_circ_printed - W_check,
        r=r, dT_actual_K=dT_actual, T1_K=T1, eta_is_closed_form=eta_is_closed,
        eta_is_bound=eta, w_fluid_reproduced_MW=w_fluid, w_residual_MW=w_fluid - W_check,
    )


if __name__ == "__main__":
    r = compute()
    for k, v in r.items():
        print(f"{k:22s} {v:,.4f}")
