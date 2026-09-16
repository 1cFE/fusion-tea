"""Package-owned oracle seam for the stellarator package.

`verify.py` is generic: it knows a manifest names a module and a callable, and
nothing else. Everything that is *this package's* knowledge lives here —

* which qualified entry key becomes which oracle input (`ENTRY_KEY_TO_ORACLE_INPUT`),
* which oracle output is which qualified channel (`ORACLE_OUTPUT_TO_CHANNEL`),
* which qualified key or channel each constraint's predicate operand means
  (`operand_bindings`, design D12).

Two published surfaces and nothing else: `evaluate` and `operand_bindings`. The
independent oracle `verify_stellaris.py` recomputes the current model equations.
Its live radius operands use plant R; fixed reference anchors stay unchanged.

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

import verify_stellaris as vs  # noqa: E402  (the independent oracle)

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
#: authored attribute). Plant R also owns the live magnet radius.
ENTRY_KEY_TO_ORACLE_INPUT: dict[str, str] = {
    f"{P}magnet__winding_pack__sizing_mode": "magnet_sizing_mode",
    f"{P}magnet__winding_pack__inventory_multiplier": "magnet_inventory_multiplier",
    **{f"{P}magnet__winding_pack__{name}": "magnet_" + name for name in (
        "reference_tape_current", "material_factor", "orientation_factor", "cabling_factor",
        "degradation_factor", "sharing_factor", "allowable_fraction", "allow_field_extrapolation",
    )},
    f"{P}magnet__winding_pack__fit_aspect_ratio": "fit_aspect_ratio",
    f"{P}magnet__winding_pack__internal_build_x": "fit_internal_x",
    f"{P}magnet__winding_pack__internal_build_y": "fit_internal_y",
    f"{P}magnet__winding_pack__ground_insulation": "fit_ground",
    f"{P}magnet__casing__interior_y": "fit_interior_y",
    f"{P}magnet__casing__wall_thickness": "fit_wall",
    f"{P}magnet__casing__assembly_clearance": "fit_clearance",
    f"{P}magnet__coil__coil_t": "coil_t",

    # WI-059 reviewed explicit coil inventory and total-support accounting controls.
    **{f"{P}cryoplant__{leaf}": key for leaf, key in {
        'inventory_enabled': 'cryo_inventory_enabled', 'n_leads': 'cryo_n_leads',
        'L0': 'cryo_L0', 'f_lead': 'cryo_f_lead', 'T_shield': 'T_shield_cryo',
        'f_carnot_shield': 'f_carnot_shield', 't_case': 'cryo_t_case',
        'shield_area_ratio': 'cryo_shield_area_ratio', 'eps_eff': 'cryo_emittance',
        'sigma_SB': 'cryo_sigma_SB', 'q_MLI': 'cryo_q_mli', 'g_per_coil': 'cryo_g_per_coil',
        'k_c': 'cryo_k_cold', 'k_s': 'cryo_k_shield',
        'q_nuc_structure': 'cryo_q_nuc_structure', 'rho_structure': 'cryo_rho_structure',
        'joint_drive_fraction': 'cryo_joint_drive_fraction',
    }.items()},
    f"{P}magnet__c_support": "magnet_support_coefficient",
    f"{P}magnet__e_support": "magnet_support_exponent",
    f"{P}magnet__legacy_casing_fraction": "magnet_legacy_casing_fraction",
    f"{P}structure__residual_fraction": "structure_residual_fraction",
    f"{P}plasma__R": "R",
    f"{P}plasma__a": "a",
    # WI-046 (goal plant-closure round 1, 2026-09-08): availability retired as an entry
    # key -- the lifecycle calendar produces it. The four calendar levers replace it;
    # availability_direct > 0 selects the held mode (the compatibility bridge).
    f"{P}availability_direct": "availability_direct",
    f"{P}outage_years": "outage_years",
    f"{P}unplanned_fraction": "unplanned_fraction",
    f"{P}magnet__coil__coil_life_fpy": "coil_life_fpy",
    # WI-030/WI-035: the magnet levers and the beta referents. magnet__B retired
    # (WI-035 inversion — the field is a channel now); the coil-set current and
    # its facts are the entry keys.
    f"{P}magnet__coil__n_coils": "magnet_n_coils",
    f"{P}magnet__coil__I_coil": "magnet_I_coil",
    f"{P}magnet__coil__k_link": "magnet_k_link",
    f"{P}magnet__coil__f_set": "magnet_f_set",
    f"{P}magnet__winding_pack__j_wp": "magnet_j_wp",
    # WI-058 (2026-09-14): the winding length follows the coil bore; the printed circumference
    # at the reference bore replaces the WI-036 shape factor over the major radius.
    f"{P}magnet__coil__c_coil_ref": "magnet_c_coil_ref",
    f"{P}magnet__winding_pack__f_wp_vol": "magnet_f_wp_vol",
    f"{P}magnet__winding_pack__E_wp": "magnet_E_wp",
    f"{P}magnet__winding_pack__f_cond": "magnet_f_cond",
    f"{P}magnet__winding_pack__eps_cond_allow": "magnet_eps_cond_allow",
    f"{P}magnet__winding_pack__k_sigma": "magnet_k_sigma",
    f"{P}magnet__casing__sigma_allow": "magnet_sigma_allow",
    f"{P}magnet__winding_pack__f_wp_fab": "magnet_f_wp_fab",
    # WI-040 explicit material procurement and winding-operation facts.
    f"{P}magnet__coil__turn_current": "magnet_turn_current",
    **{f"{P}magnet__winding_pack__{name}": "magnet_" + name for name in (
        "f_copper", "f_solder", "f_steel", "f_helium", "rho_copper", "rho_solder",
        "rho_steel", "price_copper", "price_solder", "price_steel", "price_helium",
        "helium_pressure", "helium_gas_constant", "winding_rate_1990",
        "tape_width", "tape_thickness", "tape_price_per_m",
        "cost_escalation", "nonplanar_factor",
        "f_wp_perimeter", "insulation_sheet_thickness", "insulation_sheet_price",
    )},
    # WI-044: magnet__m_casing retired (the casing mass is computed from the stored
    # energy); the five coil-bore anchors are the entry keys that replaced it.
    f"{P}magnet__casing__m_casing_ref": "magnet_m_casing_ref",
    f"{P}magnet__casing__W_mag_ref": "magnet_W_mag_ref",
    f"{P}magnet__coil__I_ref": "magnet_I_ref",
    f"{P}magnet__coil__R_ref": "magnet_R_ref",
    f"{P}magnet__coil__a_coil_ref": "magnet_a_coil_ref",
    f"{P}magnet__casing__steel_price": "magnet_steel_price",
    f"{P}magnet__casing__f_steel_fab": "magnet_f_steel_fab",
    f"{P}magnet__winding_pack__B_max": "magnet_B_max",
    f"{P}magnet__winding_pack__B_grade_ref": "magnet_B_grade_ref",
    f"{P}magnet__winding_pack__field_exponent": "magnet_field_exponent",
    f"{P}magnet__coil__peak_ratio": "magnet_peak_ratio",
    f"{P}plasma__n_e0": "n_e0",
    # WI-042: alpha_n_e retired as an entry key -- the electron profile is derived
    # inside the sustainment chain by quasi-neutrality from the fuel and the ash.
    f"{P}plasma__T_i0": "T_i0",
    # WI-037: n_D0/n_T0/T_e0/n_He0 retired as entry keys (computed by the
    # sustainment chain); the sustainment held facts and the coupled-heating
    # lever are entry keys instead. Oracle input names per `verify_stellaris.IN`.
    f"{P}plasma__iota_23": "iota_23",
    f"{P}plasma__f_ren": "f_ren",
    f"{P}plasma__f_alpha_fast": "f_alpha_fast",
    f"{P}plasma__tau_ratio_ash": "tau_ratio_ash",
    f"{P}plasma__f_suppr_ash": "f_suppr_ash",
    f"{P}plasma__Z_eff_core": "Z_eff_core",
    f"{P}plasma__f_W_core": "f_W_core",
    f"{P}plasma__Ti_over_Te": "Ti_over_Te",
    # WI-039: p_input, p_ecrh and eta_pin retired as entry points -- installed
    # wall-plug power is now the lever and the chain derives both. The declared
    # p_input/p_ecrh tie went with them: the invariant it maintained is structural.
    f"{P}heating__p_wallplug_heat": "p_wallplug_heat",
    f"{P}heating__eta_source_heat": "eta_source_heat",
    f"{P}heating__eta_couple_heat": "eta_couple_heat",
    f"{P}heating__p_delivered_direct_heat": "p_delivered_direct_heat",
    f"{P}heating__p_coupled_direct_heat": "p_coupled_direct_heat",
    # WI-041: the six source-anchored peak-calibration facts and the dormant
    # direct term are entry keys (the retired exact ash_frac never was one here).
    f"{P}blanket__first_wall__wall_peak_q_ref": "wall_peak_q_ref",
    f"{P}blanket__first_wall__wall_peak_p_fus_ref": "wall_peak_p_fus_ref",
    f"{P}blanket__first_wall__wall_peak_R_ref": "wall_peak_R_ref",
    f"{P}blanket__first_wall__wall_peak_a_ref": "wall_peak_a_ref",
    f"{P}blanket__first_wall__wall_peak_kappa_ref": "wall_peak_kappa_ref",
    f"{P}blanket__first_wall__wall_peak_standoff_ref": "wall_peak_standoff_ref",
    f"{P}blanket__first_wall__wall_peak_calibration_direct": "wall_peak_calibration_direct",
    f"{P}plasma__sustain__ash_frac_in": "sustain_ash_frac",
    f"{P}plasma__sustain__R_w_sync_in": "R_w_sync",
    f"{P}plasma__sustain__kappa_sync_in": "kappa_sync",
    # Item 6 study 2 (20260821-power-cycle-ab): the power-conversion block that
    # defines the arms, and the discount-rate lever. Oracle input names per
    # `verify_stellaris.IN` (eta_th, turbine_per_mw, heat_rej_per_mw, discount_rate).
    # WI-045 (goal plant-closure): eta_th retired as an entry key (it is the cycle
    # calc's channel now); eta_p and p_pump were never mapped. The five flags and
    # directs plus the circuit and fit facts are the entry keys. Study levers per
    # design D7: loop_live, cycle_live, p_pump_direct, eta_p_direct, eta_th_direct,
    # n_loops, loop_dT_blanket, loop_T_in, f_loss, dT_approach; the fit coefficients
    # and domain are swapped together through a declared arm binding, never alone.
    f"{P}heat_transport__loop_live": "loop_live",
    f"{P}turbine__cycle_live": "cycle_live",
    f"{P}heat_transport__p_pump_direct": "p_pump_direct",
    f"{P}heat_transport__eta_p_direct": "eta_p_direct",
    f"{P}turbine__eta_th_direct": "eta_th_direct",
    f"{P}heat_transport__loop_T_in": "loop_T_in",
    f"{P}heat_transport__loop_dT_blanket": "loop_dT_blanket",
    f"{P}heat_transport__loop_cp": "loop_cp",
    f"{P}heat_transport__loop_gamma": "loop_gamma",
    f"{P}heat_transport__loop_p": "loop_p",
    f"{P}heat_transport__n_loops": "n_loops",
    f"{P}heat_transport__mdot_loop_ref": "mdot_loop_ref",
    f"{P}heat_transport__dp_loop_ref": "dp_loop_ref",
    f"{P}heat_transport__f_loss": "f_loss",
    f"{P}heat_transport__eta_is": "eta_is",
    f"{P}heat_transport__eta_drive": "eta_drive",
    f"{P}turbine__dT_approach": "dT_approach",
    f"{P}turbine__a_fit": "a_fit",
    f"{P}turbine__b_fit": "b_fit",
    f"{P}turbine__T_offset_fit": "T_offset_fit",
    f"{P}turbine__T2_min": "T2_min",
    f"{P}turbine__T2_max": "T2_max",
    f"{P}turbine__delta_eta": "delta_eta",
    f"{P}turbine__cost_per_mw": "turbine_per_mw",
    f"{P}heat_rejection__cost_per_mw": "heat_rej_per_mw",
    f"{P}discount_rate": "discount_rate",
    # Item 6 study 1 (20260823-magnet-technology-ab): the conductor block that
    # defines the arms. Oracle input names per `verify_stellaris.IN`.
    f"{P}magnet__coil__cost_per_kAm": "magnet_cost_per_kAm",
    f"{P}cryoplant__T_cold_cryo": "T_cold_cryo",
    # WI-059: publish existing equipment/allowance levers used by the reviewed sensitivities.
    f"{P}cryoplant__f_carnot_cryo": "f_carnot_cryo",
    f"{P}cryoplant__p_tfcool": "p_tfcool",
    f"{P}magnet__vol_cold_cryo": "vol_cold_cryo",
    # WI-047 (goal plant-closure, 2026-09-08): the fuel-cycle, divertor-heat and
    # vacuum facts (design D11). Levers for the round's study: t_recycle (the
    # recovery semantics), burn_fraction,
    # f_rad_total, q_target_ref / p_nonrad_ref (the low case 5.0 at 50), p_exhaust,
    # T_gas, R_ref_divertor; the achieved tbr becomes a key too (the adequacy arm).
    # The two library defaults are LIBRARY_DEFAULT entry points of the package.
    f"{P}blanket__tbr": "tbr",
    f"{P}fuel_cycle__burn_fraction": "burn_fraction",
    f"{P}fuel_cycle__t_recycle": "t_recycle",
    f"{P}fuel_cycle__eta_extract": "eta_extract",
    f"{P}fuel_cycle__lambda_T": "lambda_T",
    f"{P}fuel_cycle__I_total": "I_total",
    f"{P}fuel_cycle__G_stock": "G_stock",
    f"{P}fuel_cycle__m_T_kg": "m_T_kg",
    f"{P}divertor__f_rad_total": "f_rad_total",
    f"{P}divertor__q_target_ref": "q_target_ref",
    f"{P}divertor__p_nonrad_ref": "p_nonrad_ref",
    f"{P}divertor__q_target_limit": "q_target_limit",
    f"{P}divertor__R_ref_divertor": "R_ref_divertor",
    f"{P}vacuum_pumping__T_gas": "T_gas",
    f"{P}vacuum_pumping__p_exhaust": "p_exhaust",
    f"{P}fuel_cycle__fuel__s_per_fpy_in": "s_per_fpy",
    f"{P}vacuum_pumping__vacuum__k_B_in": "k_B",
}

#: Oracle output name -> qualified channel name. Only channels the package records
#: as single-field floats appear; the oracle returns more than the package does.
ORACLE_OUTPUT_TO_CHANNEL: dict[str, str] = {
    **{"sizing_" + name: f"{P}magnet__current_sizing__{name}" for name in (
        "required_tapes", "required_conductor_area", "required_pack_area",
        "required_effective_density", "selected_effective_density", "tape_available_current")},
    **{"conductor_" + name: f"{P}magnet__conductor_current__{name}" for name in (
        "parallel_tapes_set", "parallel_tapes_reference", "tape_critical_current",
        "critical_current_reference", "critical_current_set", "operating_fraction_reference",
        "operating_fraction_set", "allowable_current", "margin_fraction", "margin_current", "field_extrapolated",
    )},
    "fit_minimum_margin": f"{P}magnet__wp_fit__minimum_margin",
    "fit_nominal_x": f"{P}magnet__wp_fit__nominal_x",
    "fit_nominal_y": f"{P}magnet__wp_fit__nominal_y",
    "fit_internal_x": f"{P}magnet__wp_fit__internal_x",
    "fit_internal_y": f"{P}magnet__wp_fit__internal_y",
    "fit_pack_x": f"{P}magnet__wp_fit__pack_x",
    "fit_pack_y": f"{P}magnet__wp_fit__pack_y",
    "fit_insulated_x": f"{P}magnet__wp_fit__insulated_x",
    "fit_insulated_y": f"{P}magnet__wp_fit__insulated_y",
    "fit_required_x": f"{P}magnet__wp_fit__required_x",
    "fit_required_y": f"{P}magnet__wp_fit__required_y",
    "fit_cavity_x": f"{P}magnet__wp_fit__cavity_x",
    "fit_cavity_y": f"{P}magnet__wp_fit__cavity_y",
    "fit_exterior_x": f"{P}magnet__wp_fit__exterior_x",
    "fit_exterior_y": f"{P}magnet__wp_fit__exterior_y",
    "fit_margin_x": f"{P}magnet__wp_fit__margin_x",
    "fit_margin_y": f"{P}magnet__wp_fit__margin_y",

    "operating_heat_coupled": f"{P}operating_heat__p_coupled",
    "operating_heat_delivered": f"{P}operating_heat__p_delivered",
    "operating_heat_wallplug": f"{P}operating_heat__p_wallplug",
    "V": f"{P}plasma__geom__V",
    "p_fus": f"{P}plasma__fusion__p_fus",
    "p_th": f"{P}pb__p_th",
    "p_the": f"{P}pb__p_the",
    "p_et": f"{P}pb__p_et",
    "p_cryo": f"{P}cryoplant__refrigeration_sum__total",
    "p_cryo_cold": f"{P}cryoplant__cryo_elec__p_elec",
    "p_cryo_shield": f"{P}cryoplant__shield_elec__p_elec",
    "p_tf_total": f"{P}power_supplies__tf_power__total",
    "p_cold": f"{P}cryoplant__cold_load__p_cold",
    "support_mass": f"{P}magnet__support_mass__m_support",
    "structure_nuclear": f"{P}cryoplant__cold_load__q_structure_nuclear",
    "structure_legacy_cost": f"{P}structure__structure_cost__legacy_cost",
    **{f'thermal_{name}': f'{P}cryoplant__inventory__{channel}' for name, channel in {
        'area_cold': 'area_cold', 'area_shield': 'area_shield',
        'q_lead_cold': 'q_lead_cold', 'q_lead_shield': 'q_lead_shield',
        'q_radiation_cold': 'q_rad_cold', 'q_radiation_shield': 'q_rad_shield',
        'q_support_cold': 'q_support_cold', 'q_support_shield': 'q_support_shield',
        'q_cold': 'q_inventory_cold', 'q_shield': 'q_inventory_shield', 'p_drive': 'p_drive',
    }.items()},
    "q_eng": f"{P}pb__q_eng",
    "rec_frac": f"{P}pb__rec_frac",
    "p_net": f"{P}pb__p_net",
    "wall_load": f"{P}blanket__first_wall__wall_load_calc__wall_load",
    "wall_peak_calibration": f"{P}blanket__first_wall__wall_peak_cal__calibration",  # WI-041
    "wall_load_peak": f"{P}blanket__first_wall__wall_peak_calc__wall_load_peak",  # WI-041 the fence and lifetime operand
    "beta": f"{P}plasma__beta_calc__beta",  # WI-030 computed volume-averaged beta
    "B_peak": f"{P}magnet__peak_field_calc__B_peak",  # WI-030 peak field on the conductor
    "B_axis": f"{P}magnet__field_calc__B_axis",  # WI-035 computed axis field
    "sigma_wp": f"{P}magnet__wp_stress__sigma_wp",  # WI-035 winding-pack stress operand
    "eps_cond": f"{P}magnet__cond_strain__eps_cond",  # WI-036 conductor strain operand
    # WI-044: the coil-bore channels
    "W_mag": f"{P}magnet__stored_energy__W_mag",  # stored magnetic energy (eq. 2.82 shape, anchored)
    "m_casing": f"{P}magnet__casing_mass__m_casing",  # computed casing mass (eq. 56 shape, anchored)
    "r_coil_centre": f"{P}rb__r_coil_centre",  # the coil bore the shapes take
    "A": f"{P}plasma__geom__A",  # reported aspect ratio
    "winding_pack_legacy": f"{P}magnet__winding_pack_cost__cost",  # retained WI-035 comparison
    "winding_pack": f"{P}magnet__winding_procurement__cost",  # WI-040 selected account
    "vol_winding_pack": f"{P}magnet__wp_volume__vol_winding_pack",
    **{'conductor_' + name: f'{P}magnet__conductor_grade__{name}' for name in (
        'quantity_factor', 'j_wp_effective')},
    **{"winding_" + name: f"{P}magnet__material_inventory__{name}" for name in (
        "mass_copper", "mass_solder", "mass_steel", "mass_helium", "cost_copper",
        "cost_solder", "cost_steel", "cost_helium", "material_cost", "helium_density",
        "tape_volume",
    )},
    "tape_length": f"{P}magnet__winding_procurement__tape_length",
    "tape_procurement_cost": f"{P}magnet__winding_procurement__tape_cost",
    "conductor_length": f"{P}magnet__winding_procurement__conductor_length",
    "winding_fabrication_cost": f"{P}magnet__winding_procurement__winding_fabrication_cost",
    **{"insulation_" + name: f"{P}magnet__insulation_inventory__{name}" for name in (
        "internal_volume", "ground_volume", "sheet_area", "stock_cost")},
    "support_effective_all_in_rate": f"{P}magnet__magnet_structure_cost__effective_all_in_rate",
    "magnet_structure": f"{P}magnet__magnet_structure_cost__cost",  # WI-035 sub-account
    "magnet_capital_rollup": f"{P}magnet__magnet_capital_rollup__capital_cost",  # WI-035 rollup
    "aux_cost": f"{P}cryoplant__aux_cooling__aux_cost",  # WI-035 aux split
    "cryo_cost": f"{P}cryoplant__aux_cooling__cryo_cost",  # WI-035 cryoplant sub-account
    "magnet": f"{P}magnet__magnet_cost__capital_cost",  # WI-035: the 1cfe-form comparison channel
    "heating": f"{P}heating__heating_cost__cost",
    "divertor": f"{P}divertor__divertor_cost__cost",
    "blanket": f"{P}blanket__blanket_cost__cost",
    "shield": f"{P}shield__shield_cost__cost",
    "structure": f"{P}structure__structure_cost__cost",
    "vessel": f"{P}vessel__vessel_cost__cost",
    "power_supplies": f"{P}power_supplies__power_supplies_cost__cost",
    "turbine": f"{P}turbine__turbine_cost__cost",
    "electric": f"{P}electric_plant__electric_cost__cost",
    "heat_rejection": f"{P}heat_rejection__heat_rejection_cost__cost",
    "misc": f"{P}misc_plant__misc_cost__cost",
    "buildings": f"{P}buildings__buildings_cost__cost",
    "precon": f"{P}precon_cost__cost",
    # The package's om_cost channel is the *unlevelized* annual O&M; the oracle's
    # `annual_om` is the levelized one. Checked against the committed store, not
    # matched by name — the names agree and the numbers do not.
    "annual_om_unlevelized": f"{P}om_cost__annual_om",
    "powercore_capital": f"{P}powercore_capital__powercore_capital",
    "bop_capital": f"{P}bop_capital__bop_capital",
    "remote_handling": f"{P}remote_handling__cost",
    "installation": f"{P}installation__cost",
    "coolant": f"{P}heat_transport__coolant__cost",
    "aux_cooling": f"{P}cryoplant__aux_cooling__cost",
    "waste": f"{P}waste__cost",
    "fuel_handling": f"{P}fuel_cycle__fuel_handling__cost",
    "other_rpe": f"{P}other_rpe__cost",
    "inc": f"{P}inc_cost__cost",
    "owner": f"{P}owner__cost",
    "supplementary": f"{P}supplementary__cost",
    "idc_capital": f"{P}idc__cost",
    "reactor_equipment_subtotal": f"{P}reactor_equipment_subtotal__reactor_equipment_subtotal",
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
    "annual_fuel": f"{P}fuel_cycle__fuel_calc__annual_fuel",
    # WI-037 sustainment channels
    "n_bar19": f"{P}plasma__sustain__n_bar19",
    "n_He0": f"{P}plasma__sustain__n_He0",
    "n_D0": f"{P}plasma__sustain__n_D0",
    "n_T0": f"{P}plasma__sustain__n_T0",
    "T_e0": f"{P}plasma__sustain__T_e0",
    "W_th": f"{P}plasma__sustain__W_th",
    "tau_E": f"{P}plasma__sustain__tau_E",
    "p_brems": f"{P}plasma__sustain__p_brems",
    "p_line": f"{P}plasma__sustain__p_line",
    "p_sync": f"{P}plasma__sustain__p_sync",
    "p_rad": f"{P}plasma__sustain__p_rad",
    "p_alpha_heat": f"{P}plasma__sustain__p_alpha_heat",
    "p_aux_required": f"{P}plasma__sustain__p_aux_required",
    # WI-042 derived-profile channels: the one volume-averaged pressure (beta's
    # input), the derived electron profile's volume average and effective
    # exponent, and the ash shape's effective exponent (a diagnostic).
    "p_avg": f"{P}plasma__sustain__p_avg",
    "n_e_volav": f"{P}plasma__sustain__n_e_volav",
    "alpha_n_e_eff": f"{P}plasma__sustain__alpha_n_e_eff",
    "alpha_He_eff": f"{P}plasma__sustain__alpha_He_eff",
    # WI-039 heating-chain channels
    "heat_coupled": f"{P}heating__heat__p_coupled",
    "heat_delivered": f"{P}heating__heat__p_delivered",
    "heat_wallplug_total": f"{P}heating__heat__p_wallplug_total",
    "heat_eta_pin_eff": f"{P}heating__heat__eta_pin_eff",
    # WI-045 (goal plant-closure): the source heat, the loop and the cycle. The
    # usage is named primary_loop because `loop` is a SysML keyword.
    "q_source": f"{P}blanket__source_heat__q_source",
    "loop_mdot": f"{P}heat_transport__primary_loop__mdot",
    "loop_T_out": f"{P}heat_transport__primary_loop__T_out",
    "loop_mdot_loop": f"{P}heat_transport__primary_loop__mdot_loop",
    "loop_dp_loop": f"{P}heat_transport__primary_loop__dp_loop",
    "loop_p_loop_margin": f"{P}heat_transport__primary_loop__p_loop_margin",
    "loop_r_comp": f"{P}heat_transport__primary_loop__r_comp",
    "loop_T_comp_in": f"{P}heat_transport__primary_loop__T_comp_in",
    "loop_w_fluid": f"{P}heat_transport__primary_loop__w_fluid",
    "loop_p_elec": f"{P}heat_transport__primary_loop__p_elec",
    "loop_q_ihx": f"{P}heat_transport__primary_loop__q_ihx",
    "loop_capacity_margin": f"{P}heat_transport__primary_loop__capacity_margin",
    "loop_p_pump_total": f"{P}heat_transport__primary_loop__p_pump_total",
    "loop_q_recovered_total": f"{P}heat_transport__primary_loop__q_recovered_total",
    "cycle_T2_C": f"{P}turbine__cycle__T2_C",
    "cycle_eta_fit": f"{P}turbine__cycle__eta_fit",
    "cycle_eta_th": f"{P}turbine__cycle__eta_th",
    "cycle_margin_low": f"{P}turbine__cycle__margin_low",
    "cycle_margin_high": f"{P}turbine__cycle__margin_high",
    "cycle_domain_product": f"{P}turbine__cycle__domain_product",
    # WI-046: CAS72 is the lifecycle calendar's output (the retired cas72_calc__cost
    # channel is gone); the other ten calendar channels beside it.
    "cas72_annual": f"{P}calendar__cas72_annual",
    "calendar_availability": f"{P}calendar__availability",
    "calendar_coil_life_margin_fpy": f"{P}calendar__coil_life_margin_fpy",
    "calendar_replacement_pv": f"{P}calendar__replacement_pv",
    "calendar_planned_downtime_yr": f"{P}calendar__planned_downtime_yr",
    "calendar_terminal_downtime_yr": f"{P}calendar__terminal_downtime_yr",
    "calendar_unplanned_downtime_yr": f"{P}calendar__unplanned_downtime_yr",
    "calendar_productive_fpy": f"{P}calendar__productive_fpy",
    "calendar_dated_energy_ratio": f"{P}calendar__dated_energy_ratio",
    "calendar_n_replacements": f"{P}calendar__n_replacements",
    "calendar_physical_life_fpy": f"{P}calendar__physical_life_fpy",
    # WI-047 fuel / divertor-heat / vacuum channels (nineteen)
    "fuel_burn_rate": f"{P}fuel_cycle__fuel__burn_rate",
    "fuel_inject_rate": f"{P}fuel_cycle__fuel__inject_rate",
    "fuel_exhaust_rate": f"{P}fuel_cycle__fuel__exhaust_rate",
    "fuel_loss_rate": f"{P}fuel_cycle__fuel__loss_rate",
    "fuel_tbr_required": f"{P}fuel_cycle__fuel__tbr_required",
    "fuel_tbr_margin": f"{P}fuel_cycle__fuel__tbr_margin",
    "fuel_burn_kg_per_fpy": f"{P}fuel_cycle__fuel__burn_kg_per_fpy",
    "divheat_p_heat_abs": f"{P}divertor__divheat__p_heat_abs",
    "divheat_p_sep": f"{P}divertor__divheat__p_sep",
    "divheat_f_rad_edge": f"{P}divertor__divheat__f_rad_edge",
    "divheat_f_rad_edge_in_range": f"{P}divertor__divheat__f_rad_edge_in_range",
    "divheat_p_target_nonrad": f"{P}divertor__divheat__p_target_nonrad",
    "divheat_q_target_peak": f"{P}divertor__divheat__q_target_peak",
    "divheat_q_target_peak_area_scaled": f"{P}divertor__divheat__q_target_peak_area_scaled",
    "divheat_q_target_margin": f"{P}divertor__divheat__q_target_margin",
    "divheat_p_heat_operating_minus_installed": f"{P}divertor__divheat__p_heat_operating_minus_installed",
    "vacuum_n_molecules": f"{P}vacuum_pumping__vacuum__n_molecules",
    "vacuum_Q_total": f"{P}vacuum_pumping__vacuum__Q_total",
    "vacuum_S_eff_required": f"{P}vacuum_pumping__vacuum__S_eff_required",
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
    # WI-050 scalar domains, IDs and formal names read from the current contract.
    "stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7": {
        "efficiency": {"kind": "input", "key": f"{P}heating__eta_couple_heat"},
    },
    "stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f": {
        "efficiency": {"kind": "input", "key": f"{P}heating__eta_source_heat"},
    },
    "stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650": {
        "efficiency": {"kind": "input", "key": f"{P}heating__eta_couple_heat"},
    },
    "stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5": {
        "efficiency": {"kind": "input", "key": f"{P}heating__eta_source_heat"},
    },
    f"{P}reference_conductor_current_ok__3cf239a7cdc0f2f0": {
        "margin_fraction_in": {"kind": "channel", "key": f"{P}magnet__conductor_current__margin_fraction"},
    },
    f"{P}wp_fit_ok__a25ca6a0161f6339": {
        "minimum_margin_in": {"kind": "channel", "key": f"{P}magnet__wp_fit__minimum_margin"},
    },
    # Operand names are the constraint definitions' formal names as the catalog's
    # predicate IR spells them: `_in`-suffixed where the D-5 rename touched the formal
    # (beta, beta_limit, tbr, tbr_floor, wall_load_limit), bare where it did not
    # (net_electric, rec_frac, threshold, wall_load).
    f"{P}beta_ok__82b78aad420730d5": {
        # WI-030: beta is computed ('Volume-Averaged Beta'), no longer a bound input.
        "beta_in": {"kind": "channel", "key": f"{P}plasma__beta_calc__beta"},
        "beta_limit_in": {"kind": "input", "key": f"{P}beta_limit"},
    },
    f"{P}peak_field_ok__49c6b8228a73cac5": {
        # WI-030: B_peak is the 'Conductor Peak Field' output; the ceiling is a
        # magnet-part attribute (entry point magnet__B_max).
        "B_peak": {"kind": "channel", "key": f"{P}magnet__peak_field_calc__B_peak"},
        "B_max_in": {"kind": "input", "key": f"{P}magnet__winding_pack__B_max"},
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
        "tbr_in": {"kind": "input", "key": f"{P}blanket__tbr"},
        "tbr_floor_in": {"kind": "input", "key": f"{P}tbr_floor"},
    },
    f"{P}wall_load_ok__ab2c790419af93bb": {
        # WI-041: the fence's operand is the source-anchored PEAK, not the
        # circular-torus average (the constraint id did not move: it hashes
        # the definition and the local identity, not the binding).
        "wall_load": {"kind": "channel", "key": f"{P}blanket__first_wall__wall_peak_calc__wall_load_peak"},
        "wall_load_limit_in": {"kind": "input", "key": f"{P}wall_load_limit"},
    },
    f"{P}wp_stress_ok__f38a102195da1dd0": {
        # WI-035: computed winding-pack stress vs the held sourced allowable.
        "sigma_in": {"kind": "channel", "key": f"{P}magnet__wp_stress__sigma_wp"},
        "sigma_allow_in": {"kind": "input", "key": f"{P}magnet__casing__sigma_allow"},
    },
    f"{P}cond_strain_ok__251d4c803804ab60": {
        # WI-036: the conductor's own check, separate from the structure's.
        # The operand is computed ('Conductor Strain'); the limit is a magnet-part
        # attribute and stays settable, because the band practitioners enforce
        # spans 0.2% to 0.4% and the tape this design specifies is the weakest
        # of the five measured.
        "eps_cond": {"kind": "channel", "key": f"{P}magnet__cond_strain__eps_cond"},
        "eps_cond_allow_in": {"kind": "input", "key": f"{P}magnet__winding_pack__eps_cond_allow"},
    },
    f"{P}sustainment_ok__77add152ed8eafce": {
        # WI-037: computed required sustained coupled heating vs the installed
        # plasma-coupled heating, coupled-to-coupled. WI-039: the installed side
        # is no longer the held p_input entry key -- it is the heating chain's
        # computed coupled power, so both operands are now computed.
        "p_aux_required_in": {"kind": "channel", "key": f"{P}plasma__sustain__p_aux_required"},
        "p_aux_installed_in": {"kind": "channel", "key": f"{P}heating__heat__p_coupled"},
    },
    f"{P}burn_hold_ok__03c3f94b878e5b58": {
        # WI-043 (goal burn-control): the lower half of the operating-point
        # condition, p_aux_required >= 0, on the same computed operand the
        # sustainment limit reads. One operand, a literal zero on the other
        # side (the balance's own closing value; not an entry point). The id's
        # hash is codegen's, read from generated/contracts/model_contract.json.
        "p_aux_required_in": {"kind": "channel", "key": f"{P}plasma__sustain__p_aux_required"},
    },
    # WI-045 (goal plant-closure): the loop's two fences and the cycle's domain
    # fence, all on computed operands ('Primary Coolant Loop', 'Power Cycle
    # Efficiency' outputs); the rated per-loop flow is the instance's reference
    # figure (entry point mdot_loop_ref). Ids read from model_contract.json at the
    # 2026-09-08 regeneration.
    f"{P}loop_pressure_ok__5905ab54f5e8a945": {
        "p_loop_margin_in": {"kind": "channel", "key": f"{P}heat_transport__primary_loop__p_loop_margin"},
    },
    f"{P}loop_capacity_ok__d77f6027ceb27852": {
        "mdot_loop_in": {"kind": "channel", "key": f"{P}heat_transport__primary_loop__mdot_loop"},
        "mdot_loop_rated_in": {"kind": "input", "key": f"{P}heat_transport__mdot_loop_ref"},
    },
    f"{P}cycle_domain_ok__ba3fa9c3653b3fd3": {
        "domain_product_in": {"kind": "channel", "key": f"{P}turbine__cycle__domain_product"},
    },
    # WI-047: the divertor target peak (computed, the fixed-geometry pessimistic
    # case scaled in load) against the adopted threshold (an instance input).
    # The id is read from generated/contracts/model_contract.json, never guessed.
    f"{P}divertor_heat_ok__26b4658f9fdfd7b7": {
        "q_target_peak_in": {"kind": "channel", "key": f"{P}divertor__divheat__q_target_peak"},
        "q_target_limit_in": {"kind": "input", "key": f"{P}divertor__q_target_limit"},
    },
}


class OracleSeamError(Exception):
    """A point, key, or output this seam cannot map. Always a mechanical failure."""


def _oracle_overrides(point: Mapping[str, float]) -> dict[str, float]:
    """Translate qualified current entry keys, refusing undeclared inputs."""
    if f"{P}magnet__R0" in point:
        raise OracleSeamError(f"retired entry key {P}magnet__R0; use plant R")
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
    if "magnet_R0" in overrides:
        raise OracleSeamError("retired oracle input magnet_R0; use plant R")
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
