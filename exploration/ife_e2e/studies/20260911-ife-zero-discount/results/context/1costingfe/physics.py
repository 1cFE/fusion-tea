"""Layer 2: Physics — fuel physics, power balance (forward + inverse)."""

import jax.numpy as jnp

from costingfe.layers.radiation import (
    compute_impurity_fraction,
    compute_p_rad,
)
from costingfe.types import Fuel, ImpurityMix, PowerTable, WallMaterial

# ---------------------------------------------------------------------------
# Fundamental constants (CODATA 2018 values)
# ---------------------------------------------------------------------------
_EV = 1.602176634e-19  # J per eV (exact by 2019 SI redefinition)
_ATOMIC_MASS = 1.66053906892e-27  # kg
MEV_TO_JOULES = _EV * 1e6  # 1 MeV in J
M_DEUTERIUM_KG = 3.3435837768e-27  # deuteron mass, kg
M_PROTON_KG = 1.67262192595e-27  # proton mass, kg
M_HE3_KG = 5.0064127862e-27  # helion mass, kg (He-3 nucleus)
M_LI6_KG = 6.015122795 * _ATOMIC_MASS  # kg
M_B11_KG = 11.0093054 * _ATOMIC_MASS  # kg

# DD burn fraction defaults (T=50 keV, tau_p=5 s)
DD_F_T_DEFAULT = 0.969  # DD tritium burn fraction
DD_F_HE3_DEFAULT = 0.689  # DD He-3 burn fraction

# ---------------------------------------------------------------------------
# Fusion Q-values and product energies (MeV) — nuclear reaction data
# Source: pyFECONs fuel_physics.py
# ---------------------------------------------------------------------------
# DT: D + T -> He4(3.52 MeV) + n(14.06 MeV), Q = 17.58 MeV
E_ALPHA_DT = 3.52
Q_DT = 17.58
E_N_DT = 14.06

# DD branch 1: D + D -> T(1.01 MeV) + p(3.02 MeV), Q = 4.03 MeV
E_T_DD = 1.01
E_P_DD = 3.02
Q_DD_PT = 4.03

# DD branch 2: D + D -> He3(0.82 MeV) + n(2.45 MeV), Q = 3.27 MeV
E_HE3_DD = 0.82
E_N_DD = 2.45
Q_DD_NHE3 = 3.27

# DHe3: D + He3 -> He4(3.6 MeV) + p(14.7 MeV), Q = 18.35 MeV
Q_DHE3 = 18.35

# PB11: p + B11 -> 3 He4, Q = 8.68 MeV
Q_PB11 = 8.68

# PB11 side reactions (neutron-producing)
# 11B(alpha,n)14N: Q = +0.158 MeV, dominant (~1e-3 per alpha)
Q_ALPHA_N_PB11 = 0.158
# 11B(p,n)11C: Q = -2.765 MeV, threshold 3.02 MeV (~1e-5 per proton)
Q_P_N_PB11 = -2.765

# DD primary per-event averages (50/50 branches)
_E_CHARGED_PRIMARY_DD = 0.5 * (E_T_DD + E_P_DD) + 0.5 * E_HE3_DD  # ~2.425
_E_NEUTRON_PRIMARY_DD = 0.5 * E_N_DD  # ~1.225
_E_TOTAL_PRIMARY_DD = 0.5 * Q_DD_PT + 0.5 * Q_DD_NHE3  # ~3.65


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class OperatingPointInfeasible(Exception):
    """Raised when the operating point implied by a stated net power at a
    stated geometry violates an error-severity plasma limit (inverse mode)."""


class SizingInfeasible(Exception):
    """Raised when no machine geometry in the search range [x_min, x_max]
    can deliver the requested net electric power target (sizing mode)."""


def event_energies(
    fuel: Fuel,
    dd_f_T: float,
    dd_f_He3: float,
    dhe3_dd_frac: float,
    dhe3_f_T: float,
    dhe3_f_He3: float,
    pb11_f_alpha_n: float,
    pb11_f_p_n: float,
) -> tuple[float, float]:
    """Per-fusion-event total and neutron energies [MeV] for each fuel,
    including the secondary-burn channels. Single source of truth shared by
    ash_neutron_split (partition) and fusion_power (rate -> power).
    """
    if fuel == Fuel.DT:
        E_total = Q_DT
        E_neutron = E_N_DT
        return E_total, E_neutron
    elif fuel == Fuel.DD:
        E_charged = (
            _E_CHARGED_PRIMARY_DD + 0.5 * dd_f_T * E_ALPHA_DT + 0.5 * dd_f_He3 * Q_DHE3
        )
        E_total = _E_TOTAL_PRIMARY_DD + 0.5 * dd_f_T * Q_DT + 0.5 * dd_f_He3 * Q_DHE3
        E_neutron = E_total - E_charged
        return E_total, E_neutron
    elif fuel == Fuel.DHE3:
        # Energy-weighted ash fraction: total charged energy / total fusion energy.
        # D-He3 events release Q_DHE3 = 18.35 MeV (all charged); D-D events release
        # primary energy plus T-burnup (in D-T) and He-3-burnup (in D-He-3) chains.
        # See examples/dhe3_mix_optimization.py for a Bosch-Hale verification.
        E_n_dd = (
            _E_NEUTRON_PRIMARY_DD
            + 0.5 * dhe3_f_T * E_N_DT  # T burns in D-T -> 14.1 MeV neutron
        )
        E_c_dd = (
            _E_CHARGED_PRIMARY_DD
            + 0.5 * dhe3_f_T * E_ALPHA_DT  # T burns in D-T -> 3.5 MeV alpha
            + 0.5 * dhe3_f_He3 * Q_DHE3  # He-3 burns in D-He-3 -> 18.35 MeV charged
        )
        E_DD_event = E_n_dd + E_c_dd
        E_charged = (1 - dhe3_dd_frac) * Q_DHE3 + dhe3_dd_frac * E_c_dd
        E_total = (1 - dhe3_dd_frac) * Q_DHE3 + dhe3_dd_frac * E_DD_event
        E_neutron = E_total - E_charged
        return E_total, E_neutron
    elif fuel == Fuel.PB11:
        # Side reaction 1: 11B(alpha,n)14N
        # Each p+11B produces 3 alphas (~2.89 MeV each). Each alpha has
        # probability pb11_f_alpha_n of undergoing 11B(alpha,n)14N.
        n_alpha_n = 3.0 * pb11_f_alpha_n  # alpha-n reactions per primary event
        E_alpha = Q_PB11 / 3.0  # average alpha energy (~2.89 MeV)
        # CM kinematics: neutron energy in lab frame
        # E_CM = E_alpha * m_B11/(m_alpha + m_B11) = E_alpha * 11/15
        # Products share E_CM + Q among n(1/15) and 14N(14/15)
        E_CM_products = E_alpha * 11.0 / 15.0 + Q_ALPHA_N_PB11
        E_n_alpha = E_CM_products * 14.0 / 15.0 + E_alpha * 4.0 / 225.0  # ~2.18 MeV

        # Side reaction 2: 11B(p,n)11C
        # Endothermic (Q = -2.765 MeV, threshold 3.02 MeV). The primary
        # proton has ~zero kinetic energy in the CM, so this reaction competes
        # with p+11B only at the high-energy tail. pb11_f_p_n is the fraction
        # of primary p+11B events that instead undergo (p,n).
        # CM kinematics: E_CM = E_p * 11/12; products share E_CM + Q
        # At threshold (~3.02 MeV), E_n ~ (E_CM + Q) * 11/12 ~ 0.17 MeV
        E_n_pn = 0.17  # MeV, neutron energy near threshold

        # Total energy and neutron energy per primary event
        E_total = Q_PB11 + n_alpha_n * Q_ALPHA_N_PB11 + pb11_f_p_n * Q_P_N_PB11
        E_neutron = n_alpha_n * E_n_alpha + pb11_f_p_n * E_n_pn
        return E_total, E_neutron
    else:
        raise ValueError(f"Unknown fuel type: {fuel}")


def ash_neutron_split(
    p_fus: float,
    fuel: Fuel,
    dd_f_T: float,
    dd_f_He3: float,
    dhe3_dd_frac: float,
    dhe3_f_T: float,
    dhe3_f_He3: float,
    pb11_f_alpha_n: float,
    pb11_f_p_n: float,
) -> tuple[float, float]:
    """Compute charged-particle (ash) and neutron power from fusion power.

    Returns (p_ash, p_neutron) in MW. All paths are JAX-differentiable.

    Source: pyFECONs fuel_physics.py:compute_ash_neutron_split
    """
    E_total, E_neutron = event_energies(
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )
    ash_frac = (E_total - E_neutron) / E_total
    p_ash = p_fus * ash_frac
    p_neutron = p_fus * (1.0 - ash_frac)
    return p_ash, p_neutron


def mfe_forward_power_balance(
    p_fus: float,
    fuel: Fuel,
    p_input: float,
    mn: float,
    eta_th: float,
    eta_p: float,
    eta_pin: float,
    eta_de: float,
    f_sub: float,
    f_dec: float,
    p_coils: float,
    p_cool: float,
    p_pump: float,
    p_trit: float,
    p_house: float,
    p_cryo: float,
    n_e: float,
    T_e: float,
    Z_eff: float,
    plasma_volume: float,
    B: float,
    dd_f_T: float,
    dd_f_He3: float,
    dhe3_dd_frac: float,
    dhe3_f_T: float,
    dhe3_f_He3: float,
    pb11_f_alpha_n: float,
    pb11_f_p_n: float,
    wall_material: WallMaterial | None,
    T_edge: float,
    tau_ratio: float,
    fw_area: float,
    R_major: float,
    a_minor: float,
    kappa: float,
    R_w: float,
    # Genuine optional overrides (keep defaults)
    p_rad_override: float | None = None,
    f_rad_fus: float | None = None,
    seeded_impurities: dict[str, float] | None = None,
    radiation_peaking_factor: float = 1.0,
) -> PowerTable:
    """MFE forward power balance: fusion power -> net electric.

    Plasma energy balance: P_ash + P_input = P_rad + P_transport.
    If P_rad > P_ash + P_input at the given T_e, heating power is increased
    to sustain the plasma (P_input_eff = P_rad - P_ash).

    Radiation model: bremsstrahlung + synchrotron + impurity line radiation,
    or f_rad_fus * P_fus when the radiation fraction is specified directly.
    """
    # Step 1: Ash/neutron split
    p_ash, p_neutron = ash_neutron_split(
        p_fus,
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )

    # Step 2: Build impurity mix (if wall_material provided)
    impurities = None
    if wall_material is not None and p_rad_override is None and f_rad_fus is None:
        wall_derived = {}
        symbol, f_z = compute_impurity_fraction(
            wall_material,
            T_edge,
            fw_area,
            plasma_volume,
            tau_ratio,
        )
        wall_derived[symbol] = f_z
        impurities = ImpurityMix(
            wall_derived=wall_derived,
            seeded=seeded_impurities or {},
        )
    elif seeded_impurities and p_rad_override is None and f_rad_fus is None:
        # Seeded impurities without wall material (wall_material=None explicitly)
        impurities = ImpurityMix(wall_derived={}, seeded=seeded_impurities)

    # Step 3: Radiation power
    if f_rad_fus is not None:
        p_rad = f_rad_fus * p_fus
    elif p_rad_override is not None:
        p_rad = p_rad_override
    else:
        p_rad = compute_p_rad(
            n_e,
            T_e,
            Z_eff,
            plasma_volume,
            B,
            impurities,
            R=R_major,
            a=a_minor,
            kappa=kappa,
            R_w=R_w,
            radiation_peaking_factor=radiation_peaking_factor,
        )

    # Step 4: Plasma energy balance — P_ash + P_input = P_rad + P_transport
    # If P_rad > P_ash + P_input, increase heating to sustain T_e
    p_input_eff = jnp.maximum(p_input, p_rad - p_ash)
    p_transport = p_ash + p_input_eff - p_rad

    # Step 5: Auxiliary power
    p_aux = p_trit + p_house

    # Step 6: DEC routing (operates on transport channel only)
    p_dee = f_dec * eta_de * p_transport
    p_dec_waste = f_dec * (1.0 - eta_de) * p_transport
    p_wall = (1.0 - f_dec) * p_transport

    # Step 7: Thermal power (neutrons + radiation + wall transport + pumping)
    # P_input enters via transport (Step 4), not here
    p_th = mn * p_neutron + p_rad + p_wall + eta_p * p_pump

    # Step 8: Thermal electric
    p_the = eta_th * p_th

    # Step 9: Gross electric
    p_et = p_dee + p_the

    # Step 10: Lost power
    p_loss = (p_th - p_the) + p_dec_waste

    # Step 11: Subsystem power
    p_sub = f_sub * p_et

    # Step 12: Scientific Q
    q_sci = p_fus / p_input_eff

    # Step 13: Engineering Q (uses effective heating power)
    recirculating = (
        p_coils + p_pump + p_sub + p_aux + p_cool + p_cryo + p_input_eff / eta_pin
    )
    q_eng = p_et / recirculating

    # Step 14: Net electric
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et

    return PowerTable(
        p_fus=p_fus,
        p_ash=p_ash,
        p_neutron=p_neutron,
        p_rad=p_rad,
        p_wall=p_wall,
        p_dee=p_dee,
        p_dec_waste=p_dec_waste,
        p_th=p_th,
        p_the=p_the,
        p_et=p_et,
        p_loss=p_loss,
        p_net=p_net,
        p_input=p_input_eff,
        p_pump=p_pump,
        p_sub=p_sub,
        p_aux=p_aux,
        p_coils=p_coils,
        p_cool=p_cool,
        p_cryo=p_cryo,
        p_target=0.0,
        q_sci=q_sci,
        q_eng=q_eng,
        rec_frac=rec_frac,
    )


def mfe_inverse_power_balance(
    p_net_target: float,
    fuel: Fuel,
    p_input: float,
    mn: float,
    eta_th: float,
    eta_p: float,
    eta_pin: float,
    eta_de: float,
    f_sub: float,
    f_dec: float,
    p_coils: float,
    p_cool: float,
    p_pump: float,
    p_trit: float,
    p_house: float,
    p_cryo: float,
    n_e: float,
    T_e: float,
    Z_eff: float,
    plasma_volume: float,
    B: float,
    dd_f_T: float,
    dd_f_He3: float,
    dhe3_dd_frac: float,
    dhe3_f_T: float,
    dhe3_f_He3: float,
    pb11_f_alpha_n: float,
    pb11_f_p_n: float,
    wall_material: WallMaterial | None,
    T_edge: float,
    tau_ratio: float,
    fw_area: float,
    R_major: float,
    a_minor: float,
    kappa: float,
    R_w: float,
    # Genuine optional overrides (keep defaults)
    p_rad_override: float | None = None,
    f_rad_fus: float | None = None,
    seeded_impurities: dict[str, float] | None = None,
    radiation_peaking_factor: float = 1.0,
) -> float:
    """Inverse MFE power balance: target net electric -> required fusion power.

    Uses Newton iteration to invert the forward power balance.  The forward
    balance is piecewise linear in P_fus due to the plasma energy balance:

        P_ash + P_input_eff = P_rad + P_transport

    where P_input_eff = max(P_input, P_rad - P_ash).  When P_rad exceeds
    P_ash + P_input, the effective heating increases to sustain T_e, which
    raises recirculating power and penalises LCOE.

    When f_rad_fus is provided, P_rad = f_rad_fus * P_fus (proportional to
    P_fus rather than constant).  P_net remains piecewise linear in P_fus,
    so Newton still converges in ≤2 iterations.
    """
    # Step 1: Build impurity mix (if wall_material provided)
    impurities = None
    if wall_material is not None and p_rad_override is None and f_rad_fus is None:
        wall_derived = {}
        symbol, f_z = compute_impurity_fraction(
            wall_material,
            T_edge,
            fw_area,
            plasma_volume,
            tau_ratio,
        )
        wall_derived[symbol] = f_z
        impurities = ImpurityMix(
            wall_derived=wall_derived,
            seeded=seeded_impurities or {},
        )
    elif seeded_impurities and p_rad_override is None and f_rad_fus is None:
        # Seeded impurities without wall material (wall_material=None explicitly)
        impurities = ImpurityMix(wall_derived={}, seeded=seeded_impurities)

    # Step 2: Radiation power
    # When f_rad_fus is set, p_rad = f_rad_fus * p_fus (handled inside _p_net).
    # Otherwise, p_rad is constant w.r.t. p_fus.
    if f_rad_fus is None:
        if p_rad_override is not None:
            p_rad_raw = p_rad_override
        else:
            p_rad_raw = compute_p_rad(
                n_e,
                T_e,
                Z_eff,
                plasma_volume,
                B,
                impurities,
                R=R_major,
                a=a_minor,
                kappa=kappa,
                R_w=R_w,
                radiation_peaking_factor=radiation_peaking_factor,
            )
    else:
        p_rad_raw = 0.0  # placeholder; _p_net uses f_rad_fus * pf

    # Step 3: Ash fraction from fuel type (use p_fus=1.0 to get the fraction)
    p_ash_unit, _ = ash_neutron_split(
        1.0,
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )
    ash_frac = p_ash_unit
    neutron_frac = 1.0 - ash_frac
    fr = f_rad_fus if f_rad_fus is not None else 0.0
    use_frf = f_rad_fus is not None

    # Constant recirculating loads (independent of p_fus and p_input_eff)
    p_aux = p_trit + p_house
    p_recirc_base = p_coils + p_pump + p_aux + p_cool + p_cryo

    # Step 4: Forward P_net as a function of P_fus (matches forward balance)
    def _p_net(pf):
        pa = ash_frac * pf
        pn = neutron_frac * pf
        pr = fr * pf if use_frf else p_rad_raw
        pi_eff = jnp.maximum(p_input, pr - pa)
        p_transport = pa + pi_eff - pr
        p_dee = f_dec * eta_de * p_transport
        p_wall = (1.0 - f_dec) * p_transport
        p_th = mn * pn + pr + p_wall + eta_p * p_pump
        p_et = eta_th * p_th + p_dee
        p_sub = f_sub * p_et
        return p_et - p_sub - p_recirc_base - pi_eff / eta_pin

    # Analytical dP_net/dP_fus (piecewise linear in P_fus)
    def _dp_net(pf):
        pa = ash_frac * pf
        pr = fr * pf if use_frf else p_rad_raw
        capped = pr >= pa + p_input
        if use_frf:
            # Uncapped: pi_eff = p_input, transport = (af - fr)*pf + p_input
            # p_th = (mn*nf + f_dec*fr + (1-f_dec)*af)*pf + const
            dp_uncapped = (1.0 - f_sub) * (
                eta_th * (mn * neutron_frac + f_dec * fr + (1.0 - f_dec) * ash_frac)
                + f_dec * eta_de * (ash_frac - fr)
            )
            # Capped: pi_eff = (fr - af)*pf, transport = 0
            # p_th = (mn*nf + fr)*pf + const
            dp_capped = (1.0 - f_sub) * eta_th * (mn * neutron_frac + fr) - (
                fr - ash_frac
            ) / eta_pin
        else:
            # Original: p_rad constant
            dp_uncapped = (1.0 - f_sub) * (
                eta_th * (mn * neutron_frac + (1.0 - f_dec) * ash_frac)
                + f_dec * eta_de * ash_frac
            )
            dp_capped = (1.0 - f_sub) * eta_th * mn * neutron_frac + ash_frac / eta_pin
        return jnp.where(capped, dp_capped, dp_uncapped)

    # Step 5: Linear initial guess (uncapped assumption)
    if use_frf:
        c_et = eta_th * (
            mn * neutron_frac + f_dec * fr + (1.0 - f_dec) * ash_frac
        ) + f_dec * eta_de * (ash_frac - fr)
        c_et0 = (
            eta_th * ((1.0 - f_dec) * p_input + eta_p * p_pump)
            + f_dec * eta_de * p_input
        )
    else:
        c_et = (
            eta_th * (mn * neutron_frac + (1.0 - f_dec) * ash_frac)
            + f_dec * eta_de * ash_frac
        )
        c_et0 = eta_th * (
            f_dec * p_rad_raw + (1.0 - f_dec) * p_input + eta_p * p_pump
        ) + f_dec * eta_de * (p_input - p_rad_raw)
    p_recirc_init = p_recirc_base + p_input / eta_pin
    p_fus = (p_net_target + p_recirc_init - (1.0 - f_sub) * c_et0) / (
        (1.0 - f_sub) * c_et
    )

    # Step 6: Newton refinement (converges in ≤2 for piecewise-linear)
    for _ in range(4):
        residual = _p_net(p_fus) - p_net_target
        dp = _dp_net(p_fus)
        p_fus = p_fus - residual / dp

    return p_fus


def _charged_particle_fraction(
    fuel: Fuel,
    dd_f_T: float = DD_F_T_DEFAULT,
    dd_f_He3: float = DD_F_HE3_DEFAULT,
    dhe3_dd_frac: float = 0.131,
    dhe3_f_T: float = 0.5,
    dhe3_f_He3: float = 0.1,
    pb11_f_alpha_n: float = 0.0,
    pb11_f_p_n: float = 0.0,
) -> float:
    """Return charged-particle (ash) fraction for a given fuel."""
    ash_frac, _ = ash_neutron_split(
        1.0,
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )
    return ash_frac


# ---------------------------------------------------------------------------
# Pulsed Thermal Power Balance
# ---------------------------------------------------------------------------


def pulsed_thermal_forward(
    p_fus: float,
    fuel: Fuel,
    e_driver_mj: float,
    f_rep: float,
    mn: float,
    eta_th: float,
    eta_pin: float,
    f_rad: float,
    f_sub: float,
    p_pump: float,
    p_trit: float,
    p_house: float,
    p_cryo: float,
    p_target: float,
    p_coils: float = 0.0,
    f_dec: float = 0.0,
    eta_de: float = 0.6,
    dd_f_T: float = DD_F_T_DEFAULT,
    dd_f_He3: float = DD_F_HE3_DEFAULT,
    dhe3_dd_frac: float = 0.131,
    dhe3_f_T: float = 0.5,
    dhe3_f_He3: float = 0.1,
    pb11_f_alpha_n: float = 0.0,
    pb11_f_p_n: float = 0.0,
) -> PowerTable:
    """Pulsed thermal forward power balance: fusion power -> net electric.

    Unified pulsed-confinement balance using per-pulse energy parameters
    (e_driver_mj, f_rep) and a radiation loss fraction (f_rad).  Supports
    partial charged-particle direct capture via f_dec (default 0 = all ash
    thermalises) and eta_de (DEC efficiency).  Mirrors the steady-state
    hybrid formula: fraction f_dec of non-radiated ash is collected at
    eta_de, remaining ash and all radiation thermalise into the blanket.

    CRITICAL: All conditionals on float parameters use jnp.where because
    these parameters may be JAX tracers during sensitivity analysis.
    """
    # Average driver power
    p_driver = e_driver_mj * f_rep

    # Step 1: Ash/neutron split
    p_ash, p_neutron = ash_neutron_split(
        p_fus,
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )

    # Step 2: Radiation and charged-particle split
    p_rad = f_rad * p_ash
    p_charged_net = p_ash - p_rad

    # Step 3: Direct charged-particle capture (hybrid mode; f_dec=0 means pure thermal)
    p_direct = f_dec * p_charged_net
    p_dee = eta_de * p_direct
    p_dec_waste = (1.0 - eta_de) * p_direct  # lost; not added to thermal

    # Step 4: Thermal power — (1-f_dec) of non-radiated ash + all radiation +
    # driver + pump thermalise. Pump only when thermal conversion is active.
    p_thermal_ash = (1.0 - f_dec) * p_charged_net + p_rad
    pump_term = jnp.where(eta_th > 0, p_pump, 0.0)
    p_th = mn * p_neutron + p_thermal_ash + p_driver + pump_term

    # Step 5: Thermal electric and gross
    p_the = eta_th * p_th
    p_et = p_the + p_dee

    # Step 6: Wall load from charged particles
    p_wall = p_charged_net

    # Step 7: Lost power
    p_loss = p_th - p_the

    # Step 8: Subsystem power
    p_sub = f_sub * p_et

    # Step 9: Scientific Q
    q_sci = p_fus / p_driver

    # Step 10: Recirculating and engineering Q
    p_aux = p_trit + p_house
    recirculating = (
        p_driver / eta_pin
        + jnp.where(eta_th > 0, p_pump, 0.0)
        + p_sub
        + p_aux
        + p_cryo
        + p_target
        + p_coils
    )
    q_eng = p_et / recirculating

    # Step 11: Net electric
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et

    # Pulsed-specific fields
    e_stored_mj = e_driver_mj / eta_pin
    f_ch = _charged_particle_fraction(
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )

    return PowerTable(
        p_fus=p_fus,
        p_ash=p_ash,
        p_neutron=p_neutron,
        p_rad=p_rad,
        p_wall=p_wall,
        p_dee=p_dee,
        p_dec_waste=p_dec_waste,
        p_th=p_th,
        p_the=p_the,
        p_et=p_et,
        p_loss=p_loss,
        p_net=p_net,
        p_input=0.0,
        p_pump=p_pump,
        p_sub=p_sub,
        p_aux=p_aux,
        p_coils=p_coils,
        p_cool=0.0,
        p_cryo=p_cryo,
        p_target=p_target,
        q_sci=q_sci,
        q_eng=q_eng,
        rec_frac=rec_frac,
        e_driver_mj=e_driver_mj,
        e_stored_mj=e_stored_mj,
        f_rep=f_rep,
        f_ch=f_ch,
    )


def pulsed_thermal_inverse(
    p_net_target: float,
    fuel: Fuel,
    q_eng: float,
    f_rep: float,
    mn: float,
    eta_th: float,
    eta_pin: float,
    f_rad: float,
    f_sub: float,
    p_pump: float,
    p_trit: float,
    p_house: float,
    p_cryo: float,
    p_target: float,
    p_coils: float = 0.0,
    f_dec: float = 0.0,
    eta_de: float = 0.6,
    dd_f_T: float = DD_F_T_DEFAULT,
    dd_f_He3: float = DD_F_HE3_DEFAULT,
    dhe3_dd_frac: float = 0.131,
    dhe3_f_T: float = 0.5,
    dhe3_f_He3: float = 0.1,
    pb11_f_alpha_n: float = 0.0,
    pb11_f_p_n: float = 0.0,
) -> tuple[float, float]:
    """Inverse pulsed thermal (possibly hybrid) power balance.

    Target net electric -> required P_fus and E_driver.  Derives driver
    energy from q_eng, then solves for P_fus accounting for the hybrid
    DEC contribution (f_dec, eta_de).  f_dec=0 reduces to pure thermal.
    """
    # Derive gross electric and recirculating from q_eng
    p_et = p_net_target * q_eng / (q_eng - 1.0)
    p_recirc = p_et / q_eng

    # Solve for p_driver from recirculating budget
    # p_recirc = p_driver/eta_pin + pump_term + f_sub*p_et
    #          + p_aux + p_cryo + p_target + p_coils
    pump_term = jnp.where(eta_th > 0, p_pump, 0.0)
    p_aux = p_trit + p_house
    fixed_loads = pump_term + f_sub * p_et + p_aux + p_cryo + p_target + p_coils
    p_driver = (p_recirc - fixed_loads) * eta_pin
    e_driver_mj = p_driver / f_rep

    # Ash fraction
    ash_frac, _ = ash_neutron_split(
        1.0,
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )
    neutron_frac = 1.0 - ash_frac

    # p_et = eta_th * p_th + p_dee
    # p_th = mn*nfrac*p_fus + thermal_ash_coeff*p_fus + p_driver + pump
    # p_dee = eta_de * f_dec * (1-f_rad) * ash_frac * p_fus
    # Solve for p_fus
    thermal_ash_coeff = ash_frac * ((1.0 - f_dec) * (1.0 - f_rad) + f_rad)
    dee_coeff = eta_de * f_dec * (1.0 - f_rad) * ash_frac
    c_et = eta_th * (mn * neutron_frac + thermal_ash_coeff) + dee_coeff
    p_fus = (p_et - eta_th * (p_driver + pump_term)) / c_et
    return p_fus, e_driver_mj


# ---------------------------------------------------------------------------
# Pulsed DEC (Inductive) Power Balance
# ---------------------------------------------------------------------------


def pulsed_dec_forward(
    p_fus: float,
    fuel: Fuel,
    e_driver_mj: float,
    f_rep: float,
    mn: float,
    eta_th: float,
    eta_pin: float,
    eta_dec: float,
    f_pdv: float,
    f_rad: float,
    f_sub: float,
    p_pump: float,
    p_trit: float,
    p_house: float,
    p_cryo: float,
    p_target: float,
    p_coils: float = 0.0,
    dd_f_T: float = DD_F_T_DEFAULT,
    dd_f_He3: float = DD_F_HE3_DEFAULT,
    dhe3_dd_frac: float = 0.131,
    dhe3_f_T: float = 0.5,
    dhe3_f_He3: float = 0.1,
    pb11_f_alpha_n: float = 0.0,
    pb11_f_p_n: float = 0.0,
) -> PowerTable:
    """Pulsed inductive DEC forward power balance: fusion power -> net electric.

    Models inductive DEC where driver energy circulates in an electromagnetic
    loop (cap bank -> coils -> plasma -> coils -> cap bank).  Charged-particle
    PdV work is recovered inductively.

    CRITICAL: The recirculating power for the driver is only the charging
    losses p_driver * (1/eta_pin - 1), NOT the full p_driver/eta_pin, because
    the cap bank energy goes out and comes back each cycle.

    All conditionals on float parameters use jnp.where for JAX traceability.
    """
    # Average driver power
    p_driver = e_driver_mj * f_rep

    # Step 1: Ash/neutron split
    p_ash, p_neutron = ash_neutron_split(
        p_fus,
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )

    # Step 2: Radiation and charged-particle split
    p_rad = f_rad * p_ash
    p_charged_net = p_ash - p_rad

    # Step 3: DEC recovery
    p_pdv = f_pdv * p_charged_net
    p_recovered = eta_dec * (p_driver + p_pdv)
    p_dee = p_recovered - p_driver  # net DEC electric output

    # Step 4: Waste heat
    p_dec_waste = (1.0 - eta_dec) * (p_driver + p_pdv)
    p_undirected = p_charged_net - p_pdv

    # Step 5: Thermal pool (neutrons + rad + undirected + DEC waste)
    p_pump_heat = jnp.where(eta_th > 0, p_pump, 0.0)
    p_th = mn * p_neutron + p_rad + p_undirected + p_dec_waste + p_pump_heat

    # Step 6: Thermal electric
    p_the = eta_th * p_th

    # Step 7: Gross electric: DEC net + thermal
    p_et = p_dee + p_the

    # Step 8: Wall load from undirected charged particles + DEC waste + radiation
    p_wall = p_undirected + p_dec_waste + p_rad

    # Step 9: Lost power
    p_loss = p_th - p_the

    # Step 10: Subsystem power
    p_sub = f_sub * p_et

    # Step 11: Scientific Q
    q_sci = p_fus / p_driver

    # Step 12: Recirculating — driver CHARGING LOSSES ONLY
    p_pump_recirc = jnp.where(eta_th > 0, p_pump, 0.0)
    p_aux = p_trit + p_house
    recirculating = (
        p_driver * (1.0 / eta_pin - 1.0)
        + p_pump_recirc
        + p_sub
        + p_aux
        + p_cryo
        + p_target
        + p_coils
    )
    q_eng = p_et / recirculating

    # Step 13: Net electric
    rec_frac = 1.0 / q_eng
    p_net = (1.0 - rec_frac) * p_et

    # Pulsed-specific fields
    e_stored_mj = e_driver_mj / eta_pin
    f_ch = _charged_particle_fraction(
        fuel,
        dd_f_T,
        dd_f_He3,
        dhe3_dd_frac,
        dhe3_f_T,
        dhe3_f_He3,
        pb11_f_alpha_n,
        pb11_f_p_n,
    )

    return PowerTable(
        p_fus=p_fus,
        p_ash=p_ash,
        p_neutron=p_neutron,
        p_rad=p_rad,
        p_wall=p_wall,
        p_dee=p_dee,
        p_dec_waste=p_dec_waste,
        p_th=p_th,
        p_the=p_the,
        p_et=p_et,
        p_loss=p_loss,
        p_net=p_net,
        p_input=0.0,
        p_pump=p_pump,
        p_sub=p_sub,
        p_aux=p_aux,
        p_coils=p_coils,
        p_cool=0.0,
        p_cryo=p_cryo,
        p_target=p_target,
        q_sci=q_sci,
        q_eng=q_eng,
        rec_frac=rec_frac,
        e_driver_mj=e_driver_mj,
        e_stored_mj=e_stored_mj,
        f_rep=f_rep,
        f_ch=f_ch,
    )


def pulsed_dec_inverse(
    p_net_target: float,
    fuel: Fuel,
    q_eng: float,
    f_rep: float,
    mn: float,
    eta_th: float,
    eta_pin: float,
    eta_dec: float,
    f_pdv: float,
    f_rad: float,
    f_sub: float,
    p_pump: float,
    p_trit: float,
    p_house: float,
    p_cryo: float,
    p_target: float,
    p_coils: float = 0.0,
    dd_f_T: float = DD_F_T_DEFAULT,
    dd_f_He3: float = DD_F_HE3_DEFAULT,
    dhe3_dd_frac: float = 0.131,
    dhe3_f_T: float = 0.5,
    dhe3_f_He3: float = 0.1,
    pb11_f_alpha_n: float = 0.0,
    pb11_f_p_n: float = 0.0,
) -> tuple[float, float]:
    """Inverse pulsed DEC: target P_net + Q_eng -> required P_fus and e_driver_mj.

    Derives driver energy from q_eng (DEC recirculating = charging losses only),
    then solves linearly for P_fus from the gross electric balance.

    Returns (p_fus, e_driver_mj).
    """
    # Step 1: Derive gross electric and recirculating from q_eng
    p_et = p_net_target * q_eng / (q_eng - 1.0)
    p_recirc = p_et / q_eng

    # Step 2: Solve for p_driver from recirculating budget
    # p_recirc = p_driver*(1/eta_pin - 1) + pump_term + f_sub*p_et
    #          + p_aux + p_cryo + p_target + p_coils
    pump_term = jnp.where(eta_th > 0, p_pump, 0.0)
    p_aux = p_trit + p_house
    fixed_loads = pump_term + f_sub * p_et + p_aux + p_cryo + p_target + p_coils
    p_driver = (p_recirc - fixed_loads) / (1.0 / eta_pin - 1.0)
    e_driver_mj = p_driver / f_rep

    # Step 3: Solve for p_fus from the gross electric balance
    # p_et = p_dee + p_the
    # p_dee = eta_dec*(p_driver + p_pdv) - p_driver
    #       where p_pdv = f_pdv * f_ch * (1-f_rad) * p_fus
    # p_the = eta_th * p_th
    #       where p_th = mn*neutron_frac*p_fus + f_ch*f_rad*p_fus
    #                   + f_ch*(1-f_rad)*(1-f_pdv)*p_fus  (undirected)
    #                   + (1-eta_dec)*(p_driver + p_pdv)   (DEC waste)
    #                   + pump_term
    f_ch = _charged_particle_fraction(
        fuel,
        dd_f_T=dd_f_T,
        dd_f_He3=dd_f_He3,
        dhe3_dd_frac=dhe3_dd_frac,
        dhe3_f_T=dhe3_f_T,
        dhe3_f_He3=dhe3_f_He3,
        pb11_f_alpha_n=pb11_f_alpha_n,
        pb11_f_p_n=pb11_f_p_n,
    )
    neutron_frac = 1.0 - f_ch

    # Coefficients of p_fus in p_dee
    cn = f_ch * (1.0 - f_rad)  # charged_net fraction
    pdv_coeff = f_pdv * cn  # p_pdv per p_fus
    # p_dee = eta_dec*(p_driver + pdv_coeff*p_fus) - p_driver
    # p_dee contribution from p_fus: eta_dec * pdv_coeff * p_fus
    # p_dee constant: eta_dec*p_driver - p_driver = (eta_dec - 1)*p_driver
    dee_fus_coeff = eta_dec * pdv_coeff
    dee_const = (eta_dec - 1.0) * p_driver

    # Coefficients of p_fus in p_the
    # p_th = mn*neutron_frac*p_fus + f_ch*f_rad*p_fus + cn*(1-f_pdv)*p_fus
    #      + (1-eta_dec)*(p_driver + pdv_coeff*p_fus) + pump_term
    undirected_coeff = cn * (1.0 - f_pdv)
    dec_waste_fus = (1.0 - eta_dec) * pdv_coeff
    th_fus_coeff = mn * neutron_frac + f_ch * f_rad + undirected_coeff + dec_waste_fus
    th_const = (1.0 - eta_dec) * p_driver + pump_term
    the_fus_coeff = eta_th * th_fus_coeff
    the_const = eta_th * th_const

    # p_et = dee_const + dee_fus_coeff*p_fus + the_const + the_fus_coeff*p_fus
    # Solve: p_fus = (p_et - dee_const - the_const) / (dee_fus_coeff + the_fus_coeff)
    p_fus = (p_et - dee_const - the_const) / (dee_fus_coeff + the_fus_coeff)
    return p_fus, e_driver_mj
