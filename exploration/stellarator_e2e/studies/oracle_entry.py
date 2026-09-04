"""Package-owned oracle seam for the stellarator package.

`verify.py` is generic: it knows a manifest names a module and a callable, and
nothing else. Everything that is *this package's* knowledge lives here —

* which qualified entry key becomes which oracle input (`ENTRY_KEY_TO_ORACLE_INPUT`),
* which oracle output is which qualified channel (`ORACLE_OUTPUT_TO_CHANNEL`),
* which qualified key or channel each constraint's predicate operand means
  (`operand_bindings`, design D12).

Two published surfaces and nothing else: `evaluate` and `operand_bindings`. The
independent oracle `verify_stellaris.py` is imported and never modified — it stays
independent evidence, and a study-seam edit to it would compromise that.

Everything here fails closed. An entry key with no declared mapping, two keys
that map to one oracle input but disagree, or an oracle output with no channel
is a mechanical failure, not a silently skipped comparison.

Nothing here feeds a number *into* a run. Since the stellarator model migration
(2026-08-21) the package runs sealed on stock teax and the oracle only recomputes;
CAS27 (`special_materials_capital`) is now a package channel the oracle recomputes
from its own blanket volume, so oracle parity verifies it for the first time.
"""

from __future__ import annotations

import functools
import sys
from collections.abc import Mapping
from pathlib import Path

E2E = Path(__file__).resolve().parent.parent
if str(E2E) not in sys.path:
    sys.path.insert(0, str(E2E))

import verify_stellaris as vs  # noqa: E402  (the independent oracle, unmodified)

# The profile integral depends only on (alpha_n, alpha_T, T_i0), none of which any
# study sweeps, so memoizing it is exact rather than an approximation. Applied once
# at import (`run_design_search.py:79`).
if not hasattr(vs._profile_integral, "cache_info"):
    vs._profile_integral = functools.lru_cache(maxsize=None)(vs._profile_integral)

P = "stellarator_09__stellaris__"

#: Qualified entry key -> oracle input name. Every key that can appear in a proposal
#: or in a recorded case's inputs is declared here; an undeclared key is a failure.
#: One key per swept plant attribute since the model migration (the library formals
#: are bound by the `_in` convention, so codegen projects one entry point per
#: authored attribute); `magnet__R0` is the separately authored tie.
ENTRY_KEY_TO_ORACLE_INPUT: dict[str, str] = {
    f"{P}R": "R",
    f"{P}magnet__R0": "magnet_R0",
    f"{P}a": "a",
    f"{P}availability": "availability",
    # WI-030/WI-035: the magnet levers and the beta referents. magnet__B retired
    # (WI-035 inversion — the field is a channel now); the coil-set current and
    # its facts are the entry keys.
    f"{P}magnet__n_coils": "magnet_n_coils",
    f"{P}magnet__I_coil": "magnet_I_coil",
    f"{P}magnet__k_link": "magnet_k_link",
    f"{P}magnet__f_set": "magnet_f_set",
    f"{P}magnet__j_wp": "magnet_j_wp",
    f"{P}magnet__k_coil": "magnet_k_coil",
    f"{P}magnet__f_wp_vol": "magnet_f_wp_vol",
    f"{P}magnet__E_wp": "magnet_E_wp",
    f"{P}magnet__f_cond": "magnet_f_cond",
    f"{P}magnet__eps_cond_allow": "magnet_eps_cond_allow",
    f"{P}magnet__k_sigma": "magnet_k_sigma",
    f"{P}magnet__sigma_allow": "magnet_sigma_allow",
    f"{P}magnet__f_wp_fab": "magnet_f_wp_fab",
    f"{P}magnet__m_casing": "magnet_m_casing",
    f"{P}magnet__steel_price": "magnet_steel_price",
    f"{P}magnet__f_steel_fab": "magnet_f_steel_fab",
    f"{P}magnet__B_max": "magnet_B_max",
    f"{P}magnet__peak_ratio": "magnet_peak_ratio",
    f"{P}n_e0": "n_e0",
    f"{P}alpha_n_e": "alpha_n_e",
    f"{P}T_i0": "T_i0",
    # WI-037: n_D0/n_T0/T_e0/n_He0 retired as entry keys (computed by the
    # sustainment chain); the sustainment held facts and the coupled-heating
    # lever are entry keys instead. Oracle input names per `verify_stellaris.IN`.
    f"{P}iota_23": "iota_23",
    f"{P}f_ren": "f_ren",
    f"{P}f_alpha_fast": "f_alpha_fast",
    f"{P}tau_ratio_ash": "tau_ratio_ash",
    f"{P}f_suppr_ash": "f_suppr_ash",
    f"{P}Z_eff_core": "Z_eff_core",
    f"{P}f_W_core": "f_W_core",
    f"{P}Ti_over_Te": "Ti_over_Te",
    # WI-039: p_input, p_ecrh and eta_pin retired as entry points -- installed
    # wall-plug power is now the lever and the chain derives both. The declared
    # p_input/p_ecrh tie went with them: the invariant it maintained is structural.
    f"{P}p_wallplug_heat": "p_wallplug_heat",
    f"{P}eta_source_heat": "eta_source_heat",
    f"{P}eta_couple_heat": "eta_couple_heat",
    f"{P}p_delivered_direct_heat": "p_delivered_direct_heat",
    f"{P}p_coupled_direct_heat": "p_coupled_direct_heat",
    # WI-041: the six source-anchored peak-calibration facts and the dormant
    # direct term are entry keys (the retired exact ash_frac never was one here).
    f"{P}wall_peak_q_ref": "wall_peak_q_ref",
    f"{P}wall_peak_p_fus_ref": "wall_peak_p_fus_ref",
    f"{P}wall_peak_R_ref": "wall_peak_R_ref",
    f"{P}wall_peak_a_ref": "wall_peak_a_ref",
    f"{P}wall_peak_kappa_ref": "wall_peak_kappa_ref",
    f"{P}wall_peak_standoff_ref": "wall_peak_standoff_ref",
    f"{P}wall_peak_calibration_direct": "wall_peak_calibration_direct",
    f"{P}sustain__ash_frac_in": "sustain_ash_frac",
    f"{P}sustain__R_w_sync_in": "R_w_sync",
    f"{P}sustain__kappa_sync_in": "kappa_sync",
    # Item 6 study 2 (20260821-power-cycle-ab): the power-conversion block that
    # defines the arms, and the discount-rate lever. Oracle input names per
    # `verify_stellaris.IN` (eta_th, turbine_per_mw, heat_rej_per_mw, discount_rate).
    f"{P}eta_th": "eta_th",
    f"{P}turbine__cost_per_mw": "turbine_per_mw",
    f"{P}heat_rejection__cost_per_mw": "heat_rej_per_mw",
    f"{P}discount_rate": "discount_rate",
    # Item 6 study 1 (20260823-magnet-technology-ab): the conductor block that
    # defines the arms. Oracle input names per `verify_stellaris.IN`.
    f"{P}magnet__cost_per_kAm": "magnet_cost_per_kAm",
    f"{P}T_cold_cryo": "T_cold_cryo",
    f"{P}vol_cold_cryo": "vol_cold_cryo",
}

#: Oracle output name -> qualified channel name. Only channels the package records
#: as single-field floats appear; the oracle returns more than the package does.
ORACLE_OUTPUT_TO_CHANNEL: dict[str, str] = {
    "V": f"{P}geom__V",
    "p_fus": f"{P}fusion__p_fus",
    "p_th": f"{P}pb__p_th",
    "p_the": f"{P}pb__p_the",
    "p_et": f"{P}pb__p_et",
    "p_cryo": f"{P}cryo_elec__p_elec",
    "q_eng": f"{P}pb__q_eng",
    "rec_frac": f"{P}pb__rec_frac",
    "p_net": f"{P}pb__p_net",
    "wall_load": f"{P}wall_load_calc__wall_load",
    "wall_peak_calibration": f"{P}wall_peak_cal__calibration",  # WI-041
    "wall_load_peak": f"{P}wall_peak_calc__wall_load_peak",  # WI-041 the fence and lifetime operand
    "beta": f"{P}beta_calc__beta",  # WI-030 computed volume-averaged beta
    "B_peak": f"{P}peak_field_calc__B_peak",  # WI-030 peak field on the conductor
    "B_axis": f"{P}field_calc__B_axis",  # WI-035 computed axis field
    "sigma_wp": f"{P}wp_stress__sigma_wp",  # WI-035 winding-pack stress operand
    "eps_cond": f"{P}cond_strain__eps_cond",  # WI-036 conductor strain operand
    "winding_pack": f"{P}winding_pack_cost__cost",  # WI-035 sub-account
    "magnet_structure": f"{P}magnet_structure_cost__cost",  # WI-035 sub-account
    "magnet_capital_rollup": f"{P}magnet_capital_rollup__capital_cost",  # WI-035 rollup
    "aux_cost": f"{P}aux_cooling__aux_cost",  # WI-035 aux split
    "cryo_cost": f"{P}aux_cooling__cryo_cost",  # WI-035 cryoplant sub-account
    "magnet": f"{P}magnet_cost__capital_cost",  # WI-035: the 1cfe-form comparison channel
    "heating": f"{P}heating_cost__cost",
    "divertor": f"{P}divertor_cost__cost",
    "blanket": f"{P}blanket_cost__cost",
    "shield": f"{P}shield_cost__cost",
    "structure": f"{P}structure_cost__cost",
    "vessel": f"{P}vessel_cost__cost",
    "power_supplies": f"{P}power_supplies_cost__cost",
    "turbine": f"{P}turbine_cost__cost",
    "electric": f"{P}electric_cost__cost",
    "heat_rejection": f"{P}heat_rejection_cost__cost",
    "misc": f"{P}misc_cost__cost",
    "buildings": f"{P}buildings_cost__cost",
    "precon": f"{P}precon_cost__cost",
    # The package's om_cost channel is the *unlevelized* annual O&M; the oracle's
    # `annual_om` is the levelized one. Checked against the committed store, not
    # matched by name — the names agree and the numbers do not.
    "annual_om_unlevelized": f"{P}om_cost__annual_om",
    "powercore_capital": f"{P}powercore_capital__powercore_capital",
    "bop_capital": f"{P}bop_capital__bop_capital",
    "remote_handling": f"{P}remote_handling__cost",
    "installation": f"{P}installation__cost",
    "coolant": f"{P}coolant__cost",
    "aux_cooling": f"{P}aux_cooling__cost",
    "waste": f"{P}waste__cost",
    "fuel_handling": f"{P}fuel_handling__cost",
    "other_rpe": f"{P}other_rpe__cost",
    "inc": f"{P}inc_cost__cost",
    "owner": f"{P}owner__cost",
    "supplementary": f"{P}supplementary__cost",
    "idc_capital": f"{P}idc__cost",
    "cas22_capital": f"{P}cas22_capital__cas22_capital",
    "cas2x_pre_contingency": f"{P}cas2x_pre_contingency__cas2x_pre_contingency",
    "cas20_capital": f"{P}cas20_capital__cas20_capital",
    "cas23_to_28_capital": f"{P}cas23_to_28_capital__cas23_to_28_capital",
    "overnight_capital": f"{P}overnight_capital__overnight_capital",
    "contingency_capital": f"{P}contingency__cost",
    "indirect_capital": f"{P}indirect__cost",
    "total_capital": f"{P}total_capital__total_capital",
    "lcoe": f"{P}lcoe_calc__lcoe",
    # CAS27, recomputed by the oracle from its own blanket volume and compared against
    # the package's in-package producer — the ingredient the era route could not verify.
    "special_materials": f"{P}special_materials_capital__special_materials_capital",
    "annual_fuel": f"{P}fuel_calc__annual_fuel",
    # WI-037 sustainment channels
    "n_bar19": f"{P}sustain__n_bar19",
    "n_He0": f"{P}sustain__n_He0",
    "n_D0": f"{P}sustain__n_D0",
    "n_T0": f"{P}sustain__n_T0",
    "T_e0": f"{P}sustain__T_e0",
    "W_th": f"{P}sustain__W_th",
    "tau_E": f"{P}sustain__tau_E",
    "p_brems": f"{P}sustain__p_brems",
    "p_line": f"{P}sustain__p_line",
    "p_sync": f"{P}sustain__p_sync",
    "p_rad": f"{P}sustain__p_rad",
    "p_alpha_heat": f"{P}sustain__p_alpha_heat",
    "p_aux_required": f"{P}sustain__p_aux_required",
    # WI-039 heating-chain channels
    "heat_coupled": f"{P}heat__p_coupled",
    "heat_delivered": f"{P}heat__p_delivered",
    "heat_wallplug_total": f"{P}heat__p_wallplug_total",
    "heat_eta_pin_eff": f"{P}heat__eta_pin_eff",
    "cas72_annual": f"{P}cas72_calc__cost",
    "cas90_1cfe": f"{P}cas90_1cfe_calc__cas90",
    "lcoe_1cfe": f"{P}lcoe_1cfe_calc__lcoe",
}

#: constraint_id -> source_name -> {"kind", "key"} (design D12).
#:
#: Hand-authored because it cannot be inferred: of the eleven `feature_ref` operands
#: across the six constraints, `net_positive.net_electric` resolves to no parameter
#: and no key by name at all (it is the `pb__p_net` channel), and the three that
#: could be name-matched use three different composition rules. A tool that guessed
#: would compare the wrong number and read as a pass.
OPERAND_BINDINGS: dict[str, dict[str, dict[str, str]]] = {
    # Operand names are the constraint definitions' formal names as the catalog's
    # predicate IR spells them: `_in`-suffixed where the D-5 rename touched the formal
    # (beta, beta_limit, tbr, tbr_floor, wall_load_limit), bare where it did not
    # (net_electric, rec_frac, threshold, wall_load).
    f"{P}beta_ok__82b78aad420730d5": {
        # WI-030: beta is computed ('Volume-Averaged Beta'), no longer a bound input.
        "beta_in": {"kind": "channel", "key": f"{P}beta_calc__beta"},
        "beta_limit_in": {"kind": "input", "key": f"{P}beta_limit"},
    },
    f"{P}peak_field_ok__49c6b8228a73cac5": {
        # WI-030: B_peak is the 'Conductor Peak Field' output; the ceiling is a
        # magnet-part attribute (entry point magnet__B_max).
        "B_peak": {"kind": "channel", "key": f"{P}peak_field_calc__B_peak"},
        "B_max_in": {"kind": "input", "key": f"{P}magnet__B_max"},
    },
    f"{P}net_positive__484521d56c02667a": {
        # No parameter and no key contains "net_electric": it is the power-balance
        # net electric channel, which the store does not record (multi-field model)
        # but the oracle returns. This operand is why bindings are published rather
        # than inferred.
        "net_electric": {"kind": "channel", "key": f"{P}pb__p_net"},
    },
    f"{P}recirc_ok__afc3be66f0a3421b": {
        "rec_frac": {"kind": "channel", "key": f"{P}pb__rec_frac"},
        # Usage-prefixed (the constraint usage's own default), not a plant attribute:
        # one of the three composition rules in play.
        "threshold": {"kind": "input", "key": f"{P}recirc_ok__threshold"},
    },
    f"{P}tbr_ok__2cd198f674d413e4": {
        "tbr_in": {"kind": "input", "key": f"{P}tbr"},
        "tbr_floor_in": {"kind": "input", "key": f"{P}tbr_floor"},
    },
    f"{P}wall_load_ok__ab2c790419af93bb": {
        # WI-041: the fence's operand is the source-anchored PEAK, not the
        # circular-torus average (the constraint id did not move: it hashes
        # the definition and the local identity, not the binding).
        "wall_load": {"kind": "channel", "key": f"{P}wall_peak_calc__wall_load_peak"},
        "wall_load_limit_in": {"kind": "input", "key": f"{P}wall_load_limit"},
    },
    f"{P}wp_stress_ok__f38a102195da1dd0": {
        # WI-035: computed winding-pack stress vs the held sourced allowable.
        "sigma_in": {"kind": "channel", "key": f"{P}wp_stress__sigma_wp"},
        "sigma_allow_in": {"kind": "input", "key": f"{P}magnet__sigma_allow"},
    },
    f"{P}cond_strain_ok__251d4c803804ab60": {
        # WI-036: the conductor's own check, separate from the structure's.
        # The operand is computed ('Conductor Strain'); the limit is a magnet-part
        # attribute and stays settable, because the band practitioners enforce
        # spans 0.2% to 0.4% and the tape this design specifies is the weakest
        # of the five measured.
        "eps_cond": {"kind": "channel", "key": f"{P}cond_strain__eps_cond"},
        "eps_cond_allow_in": {"kind": "input", "key": f"{P}magnet__eps_cond_allow"},
    },
    f"{P}sustainment_ok__77add152ed8eafce": {
        # WI-037: computed required sustained coupled heating vs the installed
        # plasma-coupled heating, coupled-to-coupled. WI-039: the installed side
        # is no longer the held p_input entry key -- it is the heating chain's
        # computed coupled power, so both operands are now computed.
        "p_aux_required_in": {"kind": "channel", "key": f"{P}sustain__p_aux_required"},
        "p_aux_installed_in": {"kind": "channel", "key": f"{P}heat__p_coupled"},
    },
}


class OracleSeamError(Exception):
    """A point, key, or output this seam cannot map. Always a mechanical failure."""


def _oracle_overrides(point: Mapping[str, float]) -> dict[str, float]:
    """Translate qualified entry keys into oracle inputs, refusing anything undeclared.

    Several keys carry one physical quantity (``geom__R`` and ``rb__R`` are both the
    major radius). They must agree: a proposal that set them apart would be two
    different geometries, and the oracle can only be given one.
    """
    overrides: dict[str, float] = {}
    for key, value in point.items():
        name = ENTRY_KEY_TO_ORACLE_INPUT.get(key)
        if name is None:
            raise OracleSeamError(
                f"entry key has no declared oracle mapping: {key!r} "
                f"(declare it in ENTRY_KEY_TO_ORACLE_INPUT)"
            )
        if name in overrides and overrides[name] != float(value):
            raise OracleSeamError(
                f"entry keys disagree on oracle input {name!r}: already {overrides[name]}, "
                f"then {key!r} = {float(value)}"
            )
        overrides[name] = float(value)
    return overrides


def _compute(overrides: Mapping[str, float]) -> dict[str, float]:
    """Run the independent oracle at a point, restoring its module globals after."""
    saved = dict(vs.IN)
    vs.IN.update(overrides)
    try:
        return vs.compute()
    finally:
        vs.IN.clear()
        vs.IN.update(saved)


def evaluate(point: Mapping[str, float]) -> dict[str, float]:
    """Recompute a point through the independent oracle. Qualified keys in, channels out.

    The returned map is keyed by the package's qualified channel names, so a generic
    tool can compare it to a recorded case's outputs without knowing anything about
    this package.
    """
    result = _compute(_oracle_overrides(point))
    channels = {}
    for name, channel in ORACLE_OUTPUT_TO_CHANNEL.items():
        if name not in result:
            raise OracleSeamError(
                f"oracle returned no output {name!r} declared for channel {channel!r}"
            )
        channels[channel] = float(result[name])
    return channels


def operand_bindings() -> dict[str, dict[str, dict[str, str]]]:
    """Publish which qualified key or channel each predicate operand means (D12)."""
    return {
        cid: {name: dict(binding) for name, binding in ops.items()}
        for cid, ops in OPERAND_BINDINGS.items()
    }
