"""Contract r5 section 7 statuses, flags and near-threshold descriptors, from one evaluation's published values.

Used identically on the oracle's values (the scan, step 7) and on the package's recorded values (verification,
step 10), so a status is always re-derived from recorded verdicts and flags, never copied from the case file.

Statuses, mutually exclusive, in the contract's order:
  unsupported       a domain refusal (design K25, recorded with its text), conductor status_code 0, or REBCO
                    B_peak > 25 T
  ignited           the policy's operating-point class is 'ignited' (matched power only with p_aux_required < 0 at
                    every ladder value; a search fact, read from the case's own policy trace or its base design's);
                    checked against the recorded p_aux_required < 0
  capacity-limited  a re-supplied rating at its list or rule bound whose screen still fails: cold or intercept rating
                    at the 75 kW top of Round 1's list, or 4 sector service teams (the policy's bound), with the
                    screen violated (read from the recorded inputs)
  failed            any other verdict not satisfied, except peak_field_ok (carried as envelope_flag) and the two open
                    plant gaps tbr_ok and divertor_heat_ok (carried with their margins, r5 (P) Q5)
  supported         otherwise
"""
from __future__ import annotations

import math

NOT_FAILING = ("peak_field_ok", "tbr_ok", "divertor_heat_ok")
CAPACITY_SCREENS = {"cold": ("cold_stage_capacity_ok", "capacity_ok"), "intercept": ("intercept_stage_capacity_ok",),
                    "teams": ("facility_outage_ok", "facility_initial_ready")}
LIST_TOP_W = 75_000.0
TEAMS_BOUND = 4.0
NEAR = 0.02  # [AGENT] a margin within 2 % of its scale (Round 1 contract r3 section 8 convention)


def operating_point_class(case: dict, by_id: dict) -> str | None:
    trace = (case.get("policy") or {}).get("trace") or {}
    if "operating_point" in trace:
        return trace["operating_point"]
    base = (case.get("policy") or {}).get("base_case")
    if base:
        return operating_point_class(by_id[base], by_id)
    return None


def status(unit: str, refusal: str | None, ch: dict | None, verdicts: dict | None, inputs: dict,
           op_class: str | None) -> tuple[str, list[str]]:
    """ch: channel suffix -> value; verdicts: package local identity -> status; inputs: suffix -> value."""
    if refusal is not None:
        return "unsupported", ["domain refusal: " + refusal]
    B = ch["magnet__peak_field_calc__B_peak"]
    if ch["magnet__conductor__status_code"] == 0.0:
        return "unsupported", ["conductor status 0"]
    if unit == "rebco" and B > 25.0:
        return "unsupported", ["REBCO above 25 T"]
    if op_class == "ignited":
        return "ignited", ["p_aux_required < 0 at every ladder value reaching matched power"]
    violated = sorted(k for k, s in verdicts.items() if s != "satisfied" and k not in NOT_FAILING)
    exhausted = []
    if float(inputs["cryoplant__rated_cold_W"]) >= LIST_TOP_W:
        exhausted.append("cold")
    if float(inputs["cryoplant__rated_intercept_W"]) >= LIST_TOP_W:
        exhausted.append("intercept")
    if float(inputs["buildings__sector_service_teams"]) >= TEAMS_BOUND:
        exhausted.append("teams")
    bound = [s for which in exhausted for s in CAPACITY_SCREENS[which] if s in violated]
    if bound:
        return "capacity-limited", bound
    if violated:
        return "failed", violated
    return "supported", []


def _near(gap: float, scale: float) -> bool:
    return math.isfinite(gap) and math.isfinite(scale) and abs(gap) <= NEAR * abs(scale)


def near_threshold(unit: str, ch: dict, inputs: dict) -> list[str]:
    """Status-deciding checks whose operand sits within 2 % of its threshold (scales stated per check)."""
    acc_scale = (float(inputs["cryoplant__T_cold_cryo"]) + float(inputs["magnet__nuclear_rise"])
                 + float(inputs["magnet__margin_rise"])) if unit == "nb3sn" else float(inputs["magnet__fraction_rule"])
    rows = {
        "recirc_ok": (ch["pb__rec_frac"] - float(inputs["recirc_ok__threshold"]), float(inputs["recirc_ok__threshold"])),
        "net_positive": (ch["pb__p_net"], ch["pb__p_et"]),
        "wall_load_ok": (ch["blanket__first_wall__wall_peak_calc__wall_load_peak"] - float(inputs["wall_load_limit"]),
                         float(inputs["wall_load_limit"])),
        "wp_stress_ok": (ch["magnet__wp_stress__sigma_wp"] - float(inputs["magnet__casing__sigma_allow"]),
                         float(inputs["magnet__casing__sigma_allow"])),
        "beta_ok": (ch["plasma__beta_calc__beta"] - float(inputs["beta_limit"]), float(inputs["beta_limit"])),
        "cond_strain_ok": (ch["magnet__cond_strain__eps_cond"] - float(inputs["magnet__winding_pack__eps_cond_allow"]),
                           float(inputs["magnet__winding_pack__eps_cond_allow"])),
        "ampere_floor_ok": (ch["magnet__pack_field__ampere_floor_margin"], ch["magnet__pack_field__ampere_floor"]),
        "acceptance_ok": (ch["magnet__conductor__acceptance_margin"], acc_scale),
        "pack_area_ok": (ch["magnet__area__fit_margin"], ch["magnet__area__gross_area"]),
        "divertor_heat_ok": (ch["divertor__divheat__q_target_peak"] - float(inputs["divertor__q_target_limit"]),
                             float(inputs["divertor__q_target_limit"])),
    }
    return sorted(name for name, (gap, scale) in rows.items() if _near(gap, scale))


def flags(unit: str, ch: dict, verdicts: dict, inputs: dict, case: dict) -> dict:
    """Contract section 7 flags from one evaluation (power_short and free_capacity are policy facts of the case)."""
    B = ch["magnet__peak_field_calc__B_peak"]
    code = ch["magnet__conductor__status_code"]
    x = ch["magnet__pack_field__R_over_sqrt_A_wp"]
    beta = ch["plasma__beta_calc__beta"]
    out = dict(
        envelope_flag=verdicts["peak_field_ok"] == "violated",
        green_extrapolated=ch["cryoplant__refrigeration__green_extrapolated"] == 1.0,
        power_short=int((case.get("flags") or {}).get("power_short", 0) or 0),
        arm_extrapolated=bool(float(inputs["magnet__coil__arm_slope"]) != 0.0 and not 25.0 <= x <= 40.0),
        R_over_sqrt_A_wp=x,
        ampere_floor_margin=ch["magnet__pack_field__ampere_floor_margin"],
        beta_verdict_0_05=verdicts["beta_ok"],
        beta_verdict_0_04="indeterminate" if math.isnan(beta) else ("satisfied" if beta <= 0.04 else "violated"),
        divertor_pass=verdicts["divertor_heat_ok"] == "satisfied",
        divertor_q_target_margin=ch["divertor__divheat__q_target_margin"],
        tbr_pass=verdicts["tbr_ok"] == "satisfied",
    )
    if unit == "rebco":
        out.update(extrapolated=20.0 < B <= 24.0, beyond_law_extents=24.0 < B <= 25.0,
                   above_stellaris_envelope=B > 24.9)
    else:
        out.update(extrapolated=code in (2.0, 3.0), beyond_law_extents=False, above_stellaris_envelope=False)
    return out
