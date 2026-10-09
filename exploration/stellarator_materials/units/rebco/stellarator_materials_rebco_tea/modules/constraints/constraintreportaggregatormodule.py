"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('stellarator_09_materials_rebco_material_cryoplant_capacity_ok_a7ae0d27f2e7a69e', 'stellarator_09_materials_rebco_material_magnet_steel_ok_3833f52286c5bd91', 'stellarator_09_materials_rebco_material_magnet_ampere_floor_ok_527f82db402c44d5', 'stellarator_09_materials_rebco_material_magnet_copper_ok_4c832191ef5eb0d7', 'stellarator_09_materials_rebco_material_magnet_pack_area_ok_4d2ccf27ef95a21a', 'stellarator_09_materials_rebco_material_magnet_acceptance_ok_998be97e16fad569', 'stellarator_09_materials_rebco_material_wp_stress_ok_fdb21f48452667e8', 'stellarator_09_materials_rebco_material_beta_ok_35a0c2df4310d104', 'stellarator_09_materials_rebco_material_cond_strain_ok_347e1ae0d46e036c', 'stellarator_09_materials_rebco_material_recirc_ok_5d4235cfd9f4768c', 'stellarator_09_materials_rebco_material_helium_electric_capacity_ok_cb84e81c1d9f4ff2', 'stellarator_09_materials_rebco_material_hp_shaft_capacity_ok_b373b1d4ff3823c8', 'stellarator_09_materials_rebco_material_cycle_domain_ok_bca3373bdd5bb090', 'stellarator_09_materials_rebco_material_facility_occupancy_ok_23c7d3c0c97b254a', 'stellarator_09_materials_rebco_material_condensate_flow_capacity_ok_2853033437fa7007', 'stellarator_09_materials_rebco_material_water_head_capacity_ok_ab846ad3af228cf2', 'stellarator_09_materials_rebco_material_cold_stage_capacity_ok_3bc0a73db9d3e213', 'stellarator_09_materials_rebco_material_lp_flow_capacity_ok_fbaebe15b4b2669f', 'stellarator_09_materials_rebco_material_facility_material_capacity_ok_b001b53a93bea9e7', 'stellarator_09_materials_rebco_material_facility_parcel_ok_09e54f5187da2c9f', 'stellarator_09_materials_rebco_material_heating_couple_positive_ok_3969a43f5fda8071', 'stellarator_09_materials_rebco_material_salt_electric_capacity_ok_99532fdbf4beb4d1', 'stellarator_09_materials_rebco_material_feedwater_electric_capacity_ok_ec4b1f09526dad32', 'stellarator_09_materials_rebco_material_divertor_heat_ok_4848b02ea1557c2d', 'stellarator_09_materials_rebco_material_facility_capacity_ok_c0747ad3c5d93311', 'stellarator_09_materials_rebco_material_reheat_UA_capacity_ok_a8194f424b087b57', 'stellarator_09_materials_rebco_material_salt_shaft_capacity_ok_569c89a5b855b295', 'stellarator_09_materials_rebco_material_wp_fit_ok_63e3c00c99928ca9', 'stellarator_09_materials_rebco_material_facility_geometry_ok_0258a993c78f2ff1', 'stellarator_09_materials_rebco_material_fuel_processing_capacity_ok_4ccc57f69813cb74', 'stellarator_09_materials_rebco_material_salt_head_capacity_ok_88b673b363c69f34', 'stellarator_09_materials_rebco_material_facility_outage_ok_12cedaf5124fff79', 'stellarator_09_materials_rebco_material_water_electric_capacity_ok_c74614e39b597493', 'stellarator_09_materials_rebco_material_heating_source_upper_ok_6811904a62eebc34', 'stellarator_09_materials_rebco_material_net_positive_f137773a88435534', 'stellarator_09_materials_rebco_material_cooling_water_heat_direction_77d713899c16e2ab', 'stellarator_09_materials_rebco_material_wall_load_ok_bb886accb1fe4358', 'stellarator_09_materials_rebco_material_water_rejection_capacity_ok_b282501b0da7ba05', 'stellarator_09_materials_rebco_material_tbr_ok_8ce4a3c0d3818607', 'stellarator_09_materials_rebco_material_turbine_gross_capacity_ok_887d77cd5a478001', 'stellarator_09_materials_rebco_material_hp_flow_capacity_ok_ae582a956a8ee301', 'stellarator_09_materials_rebco_material_direct_electric_capacity_ok_2ca22857e50ae9a8', 'stellarator_09_materials_rebco_material_salt_flow_capacity_ok_891f3985476a4a75', 'stellarator_09_materials_rebco_material_intercept_stage_capacity_ok_d3b9b3c84a8d0f8c', 'stellarator_09_materials_rebco_material_represented_coolant_fill_ok_bc6a51fed9b48ceb', 'stellarator_09_materials_rebco_material_magnet_pf_electric_capacity_ok_b38a37482abd8213', 'stellarator_09_materials_rebco_material_feedwater_flow_capacity_ok_9871a398794bd034', 'stellarator_09_materials_rebco_material_electric_gross_capacity_ok_6d466b03bfce1ad5', 'stellarator_09_materials_rebco_material_burn_hold_ok_b5da7626bab05382', 'stellarator_09_materials_rebco_material_magnet_tf_electric_capacity_ok_f8a1bf91be445766', 'stellarator_09_materials_rebco_material_helium_flow_capacity_ok_bf55136c825f0dde', 'stellarator_09_materials_rebco_material_heating_couple_upper_ok_d388de0d1f5a62b5', 'stellarator_09_materials_rebco_material_helium_pumping_capacity_ok_b3df6c4ada78f0e8', 'stellarator_09_materials_rebco_material_main_UA_capacity_ok_c2196a4dedc17d72', 'stellarator_09_materials_rebco_material_ihx_capacity_ok_e64acdb414b82e94', 'stellarator_09_materials_rebco_material_peak_field_ok_d2be7a2c6d0ebc66', 'stellarator_09_materials_rebco_material_sustainment_ok_60ca4f2cb2aaa5bd', 'stellarator_09_materials_rebco_material_helium_pressure_rise_capacity_ok_800684f4fbfd04ab', 'stellarator_09_materials_rebco_material_condenser_rejection_capacity_ok_1cdb674fdf5b2141', 'stellarator_09_materials_rebco_material_facility_routes_ok_31d1e5a5efc9b026', 'stellarator_09_materials_rebco_material_lp_shaft_capacity_ok_734f3bc0941a792d', 'stellarator_09_materials_rebco_material_loop_capacity_ok_d6532a89816fb7e2', 'stellarator_09_materials_rebco_material_condensate_pressure_rise_capacity_ok_79f16d6e8bc1b15b', 'stellarator_09_materials_rebco_material_facility_replacement_ready_b4650f2585ff4e4a', 'stellarator_09_materials_rebco_material_heating_source_positive_ok_622599bd0a938078', 'stellarator_09_materials_rebco_material_water_flow_capacity_ok_2a464637ca64c033', 'stellarator_09_materials_rebco_material_loop_pressure_ok_aef108bdfd08fc32', 'stellarator_09_materials_rebco_material_matched_main_heat_direction_d54ab1b7234536a0', 'stellarator_09_materials_rebco_material_condensate_electric_capacity_ok_d94728038066f7cb', 'stellarator_09_materials_rebco_material_facility_initial_ready_d38e32e55e61fdc5', 'stellarator_09_materials_rebco_material_matched_reheat_heat_direction_8bc64e6763926d8f', 'stellarator_09_materials_rebco_material_feedwater_pressure_rise_capacity_ok_2c733f473a68f18e', 'stellarator_09_materials_rebco_material_reference_conductor_current_ok_0dd0d2cb1e851094')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 78, 'applicable_gate_total': 78, 'assessed_gate_count': 73, 'unassessed_gate_count': 5, 'inapplicable_gate_count': 0, 'unassessed_reasons': {'owner_has_no_occurrences': 5}, 'coverage_state': 'partial'}


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    stellarator_09_materials_rebco_material_cryoplant_capacity_ok_a7ae0d27f2e7a69e: ConstraintEvaluation
    stellarator_09_materials_rebco_material_magnet_steel_ok_3833f52286c5bd91: ConstraintEvaluation
    stellarator_09_materials_rebco_material_magnet_ampere_floor_ok_527f82db402c44d5: ConstraintEvaluation
    stellarator_09_materials_rebco_material_magnet_copper_ok_4c832191ef5eb0d7: ConstraintEvaluation
    stellarator_09_materials_rebco_material_magnet_pack_area_ok_4d2ccf27ef95a21a: ConstraintEvaluation
    stellarator_09_materials_rebco_material_magnet_acceptance_ok_998be97e16fad569: ConstraintEvaluation
    stellarator_09_materials_rebco_material_wp_stress_ok_fdb21f48452667e8: ConstraintEvaluation
    stellarator_09_materials_rebco_material_beta_ok_35a0c2df4310d104: ConstraintEvaluation
    stellarator_09_materials_rebco_material_cond_strain_ok_347e1ae0d46e036c: ConstraintEvaluation
    stellarator_09_materials_rebco_material_recirc_ok_5d4235cfd9f4768c: ConstraintEvaluation
    stellarator_09_materials_rebco_material_helium_electric_capacity_ok_cb84e81c1d9f4ff2: ConstraintEvaluation
    stellarator_09_materials_rebco_material_hp_shaft_capacity_ok_b373b1d4ff3823c8: ConstraintEvaluation
    stellarator_09_materials_rebco_material_cycle_domain_ok_bca3373bdd5bb090: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_occupancy_ok_23c7d3c0c97b254a: ConstraintEvaluation
    stellarator_09_materials_rebco_material_condensate_flow_capacity_ok_2853033437fa7007: ConstraintEvaluation
    stellarator_09_materials_rebco_material_water_head_capacity_ok_ab846ad3af228cf2: ConstraintEvaluation
    stellarator_09_materials_rebco_material_cold_stage_capacity_ok_3bc0a73db9d3e213: ConstraintEvaluation
    stellarator_09_materials_rebco_material_lp_flow_capacity_ok_fbaebe15b4b2669f: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_material_capacity_ok_b001b53a93bea9e7: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_parcel_ok_09e54f5187da2c9f: ConstraintEvaluation
    stellarator_09_materials_rebco_material_heating_couple_positive_ok_3969a43f5fda8071: ConstraintEvaluation
    stellarator_09_materials_rebco_material_salt_electric_capacity_ok_99532fdbf4beb4d1: ConstraintEvaluation
    stellarator_09_materials_rebco_material_feedwater_electric_capacity_ok_ec4b1f09526dad32: ConstraintEvaluation
    stellarator_09_materials_rebco_material_divertor_heat_ok_4848b02ea1557c2d: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_capacity_ok_c0747ad3c5d93311: ConstraintEvaluation
    stellarator_09_materials_rebco_material_reheat_UA_capacity_ok_a8194f424b087b57: ConstraintEvaluation
    stellarator_09_materials_rebco_material_salt_shaft_capacity_ok_569c89a5b855b295: ConstraintEvaluation
    stellarator_09_materials_rebco_material_wp_fit_ok_63e3c00c99928ca9: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_geometry_ok_0258a993c78f2ff1: ConstraintEvaluation
    stellarator_09_materials_rebco_material_fuel_processing_capacity_ok_4ccc57f69813cb74: ConstraintEvaluation
    stellarator_09_materials_rebco_material_salt_head_capacity_ok_88b673b363c69f34: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_outage_ok_12cedaf5124fff79: ConstraintEvaluation
    stellarator_09_materials_rebco_material_water_electric_capacity_ok_c74614e39b597493: ConstraintEvaluation
    stellarator_09_materials_rebco_material_heating_source_upper_ok_6811904a62eebc34: ConstraintEvaluation
    stellarator_09_materials_rebco_material_net_positive_f137773a88435534: ConstraintEvaluation
    stellarator_09_materials_rebco_material_cooling_water_heat_direction_77d713899c16e2ab: ConstraintEvaluation
    stellarator_09_materials_rebco_material_wall_load_ok_bb886accb1fe4358: ConstraintEvaluation
    stellarator_09_materials_rebco_material_water_rejection_capacity_ok_b282501b0da7ba05: ConstraintEvaluation
    stellarator_09_materials_rebco_material_tbr_ok_8ce4a3c0d3818607: ConstraintEvaluation
    stellarator_09_materials_rebco_material_turbine_gross_capacity_ok_887d77cd5a478001: ConstraintEvaluation
    stellarator_09_materials_rebco_material_hp_flow_capacity_ok_ae582a956a8ee301: ConstraintEvaluation
    stellarator_09_materials_rebco_material_direct_electric_capacity_ok_2ca22857e50ae9a8: ConstraintEvaluation
    stellarator_09_materials_rebco_material_salt_flow_capacity_ok_891f3985476a4a75: ConstraintEvaluation
    stellarator_09_materials_rebco_material_intercept_stage_capacity_ok_d3b9b3c84a8d0f8c: ConstraintEvaluation
    stellarator_09_materials_rebco_material_represented_coolant_fill_ok_bc6a51fed9b48ceb: ConstraintEvaluation
    stellarator_09_materials_rebco_material_magnet_pf_electric_capacity_ok_b38a37482abd8213: ConstraintEvaluation
    stellarator_09_materials_rebco_material_feedwater_flow_capacity_ok_9871a398794bd034: ConstraintEvaluation
    stellarator_09_materials_rebco_material_electric_gross_capacity_ok_6d466b03bfce1ad5: ConstraintEvaluation
    stellarator_09_materials_rebco_material_burn_hold_ok_b5da7626bab05382: ConstraintEvaluation
    stellarator_09_materials_rebco_material_magnet_tf_electric_capacity_ok_f8a1bf91be445766: ConstraintEvaluation
    stellarator_09_materials_rebco_material_helium_flow_capacity_ok_bf55136c825f0dde: ConstraintEvaluation
    stellarator_09_materials_rebco_material_heating_couple_upper_ok_d388de0d1f5a62b5: ConstraintEvaluation
    stellarator_09_materials_rebco_material_helium_pumping_capacity_ok_b3df6c4ada78f0e8: ConstraintEvaluation
    stellarator_09_materials_rebco_material_main_UA_capacity_ok_c2196a4dedc17d72: ConstraintEvaluation
    stellarator_09_materials_rebco_material_ihx_capacity_ok_e64acdb414b82e94: ConstraintEvaluation
    stellarator_09_materials_rebco_material_peak_field_ok_d2be7a2c6d0ebc66: ConstraintEvaluation
    stellarator_09_materials_rebco_material_sustainment_ok_60ca4f2cb2aaa5bd: ConstraintEvaluation
    stellarator_09_materials_rebco_material_helium_pressure_rise_capacity_ok_800684f4fbfd04ab: ConstraintEvaluation
    stellarator_09_materials_rebco_material_condenser_rejection_capacity_ok_1cdb674fdf5b2141: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_routes_ok_31d1e5a5efc9b026: ConstraintEvaluation
    stellarator_09_materials_rebco_material_lp_shaft_capacity_ok_734f3bc0941a792d: ConstraintEvaluation
    stellarator_09_materials_rebco_material_loop_capacity_ok_d6532a89816fb7e2: ConstraintEvaluation
    stellarator_09_materials_rebco_material_condensate_pressure_rise_capacity_ok_79f16d6e8bc1b15b: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_replacement_ready_b4650f2585ff4e4a: ConstraintEvaluation
    stellarator_09_materials_rebco_material_heating_source_positive_ok_622599bd0a938078: ConstraintEvaluation
    stellarator_09_materials_rebco_material_water_flow_capacity_ok_2a464637ca64c033: ConstraintEvaluation
    stellarator_09_materials_rebco_material_loop_pressure_ok_aef108bdfd08fc32: ConstraintEvaluation
    stellarator_09_materials_rebco_material_matched_main_heat_direction_d54ab1b7234536a0: ConstraintEvaluation
    stellarator_09_materials_rebco_material_condensate_electric_capacity_ok_d94728038066f7cb: ConstraintEvaluation
    stellarator_09_materials_rebco_material_facility_initial_ready_d38e32e55e61fdc5: ConstraintEvaluation
    stellarator_09_materials_rebco_material_matched_reheat_heat_direction_8bc64e6763926d8f: ConstraintEvaluation
    stellarator_09_materials_rebco_material_feedwater_pressure_rise_capacity_ok_2c733f473a68f18e: ConstraintEvaluation
    stellarator_09_materials_rebco_material_reference_conductor_current_ok_0dd0d2cb1e851094: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "58e131b29b58ccf2af6ea6cbc354b4ee3febee32c084162da70febaf541f1e2c"

    def run(self, **evaluations) -> ModuleResult[ConstraintReportAggregatorOutput]:
        validated = ConstraintReportAggregatorInput(**evaluations)
        results = [getattr(validated, cid) for cid in EXPECTED_IDS]
        statuses = [r.status for r in results]
        coverage = CoverageAccount(**COVERAGE)

        # Statuses decide the top two arms; the account decides the rest. The status set
        # contains only occurrences of applicable assessed gates by construction, so the
        # `violation` arm cannot fire from a gate outside the denominator: an inapplicable
        # gate is either unassessed (no entries, no results) or refused at generation.
        #
        # Result-list non-emptiness stops deciding anything. That was the whole defect —
        # `all_satisfied` meant "nothing that arrived failed", whatever fraction arrived.
        if "violated" in statuses:
            headline = "violation"
        elif "indeterminate" in statuses:
            headline = "indeterminate"
        elif coverage.unassessed_gate_count == 0 and coverage.assessed_gate_count > 0:
            headline = "full_satisfaction"
        elif coverage.applicable_gate_total > 0:
            headline = "partial_coverage"
        else:
            headline = "not_assessed"
        return ModuleResult(
            data=ConstraintReportAggregatorOutput(
                constraint_report=ConstraintReport(
                    catalog_fingerprint=self.CATALOG_FINGERPRINT,
                    assessed_entry_count=len(results),
                    headline=headline,
                    coverage=coverage,
                    results=results,
                )
            )
        )
