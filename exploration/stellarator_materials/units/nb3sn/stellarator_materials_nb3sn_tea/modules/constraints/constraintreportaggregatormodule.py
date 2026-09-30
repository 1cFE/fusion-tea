"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('stellarator_09_materials_nb3sn_material_cryoplant_capacity_ok_8830dacf5e39e904', 'stellarator_09_materials_nb3sn_material_magnet_pack_area_ok_51632f8f2a7b1d5f', 'stellarator_09_materials_nb3sn_material_magnet_acceptance_ok_0f682bc3436c0794', 'stellarator_09_materials_nb3sn_material_magnet_steel_ok_3f894fc95501d96d', 'stellarator_09_materials_nb3sn_material_magnet_ampere_floor_ok_bbe387e1eb85f9b9', 'stellarator_09_materials_nb3sn_material_magnet_copper_ok_be9121bc3fcdea7a', 'stellarator_09_materials_nb3sn_material_wp_stress_ok_c61cade8f669c8f2', 'stellarator_09_materials_nb3sn_material_cond_strain_ok_404dca1f50a13e3a', 'stellarator_09_materials_nb3sn_material_recirc_ok_097dfc7574999504', 'stellarator_09_materials_nb3sn_material_helium_pressure_rise_capacity_ok_4bbd03d1c0fdffdc', 'stellarator_09_materials_nb3sn_material_tbr_ok_d57174176b5d2862', 'stellarator_09_materials_nb3sn_material_cycle_domain_ok_76acde2a26a78109', 'stellarator_09_materials_nb3sn_material_facility_occupancy_ok_e81ea8f8cf26823a', 'stellarator_09_materials_nb3sn_material_feedwater_electric_capacity_ok_c45a8ca67324291d', 'stellarator_09_materials_nb3sn_material_beta_ok_a6d1355f00db8834', 'stellarator_09_materials_nb3sn_material_facility_material_capacity_ok_c7de34bf2e881cc4', 'stellarator_09_materials_nb3sn_material_facility_parcel_ok_99f0ef2cd6538d03', 'stellarator_09_materials_nb3sn_material_fuel_processing_capacity_ok_d36667b777c42fe9', 'stellarator_09_materials_nb3sn_material_heating_couple_positive_ok_31dbd874e3b68e88', 'stellarator_09_materials_nb3sn_material_helium_flow_capacity_ok_631fba08153122f2', 'stellarator_09_materials_nb3sn_material_divertor_heat_ok_84770e9a36dc1b57', 'stellarator_09_materials_nb3sn_material_facility_capacity_ok_6d4fb7d42a36d0a7', 'stellarator_09_materials_nb3sn_material_facility_geometry_ok_14b78dfe909c8501', 'stellarator_09_materials_nb3sn_material_salt_flow_capacity_ok_090e097c99199295', 'stellarator_09_materials_nb3sn_material_water_flow_capacity_ok_71de9e2671863dbc', 'stellarator_09_materials_nb3sn_material_hp_shaft_capacity_ok_06729372362a4c6b', 'stellarator_09_materials_nb3sn_material_reheat_UA_capacity_ok_3832be39603086f5', 'stellarator_09_materials_nb3sn_material_facility_outage_ok_93bfd834822ee642', 'stellarator_09_materials_nb3sn_material_heating_source_upper_ok_91d002eb84ef7479', 'stellarator_09_materials_nb3sn_material_net_positive_2ff2061dd70a24f7', 'stellarator_09_materials_nb3sn_material_hp_flow_capacity_ok_cc7e78dbd3c706de', 'stellarator_09_materials_nb3sn_material_feedwater_flow_capacity_ok_3bcdd6d04c7a0abb', 'stellarator_09_materials_nb3sn_material_cold_stage_capacity_ok_53d0507e047820a1', 'stellarator_09_materials_nb3sn_material_lp_shaft_capacity_ok_ef6a20387b2fc647', 'stellarator_09_materials_nb3sn_material_cooling_water_heat_direction_96754d6cc5733ef5', 'stellarator_09_materials_nb3sn_material_condensate_pressure_rise_capacity_ok_4758ab1d486197ab', 'stellarator_09_materials_nb3sn_material_direct_electric_capacity_ok_a285e66b19ed2cb4', 'stellarator_09_materials_nb3sn_material_ihx_capacity_ok_e4869509b6443c3b', 'stellarator_09_materials_nb3sn_material_magnet_pf_electric_capacity_ok_ca95b633e7cc10d5', 'stellarator_09_materials_nb3sn_material_magnet_tf_electric_capacity_ok_e99855ae6bf1b46e', 'stellarator_09_materials_nb3sn_material_sustainment_ok_1a778604648c352e', 'stellarator_09_materials_nb3sn_material_wall_load_ok_41289e190845d753', 'stellarator_09_materials_nb3sn_material_salt_head_capacity_ok_a3f15f8c47fee4d0', 'stellarator_09_materials_nb3sn_material_heating_couple_upper_ok_0e4c29c53a56780e', 'stellarator_09_materials_nb3sn_material_peak_field_ok_1fcd44510d5ceb9a', 'stellarator_09_materials_nb3sn_material_reference_conductor_current_ok_ed9bbbfb7399171f', 'stellarator_09_materials_nb3sn_material_intercept_stage_capacity_ok_94f24b6c7d86d868', 'stellarator_09_materials_nb3sn_material_feedwater_pressure_rise_capacity_ok_92e4f80e79613b88', 'stellarator_09_materials_nb3sn_material_salt_shaft_capacity_ok_316c1c5c7f51a07c', 'stellarator_09_materials_nb3sn_material_condenser_rejection_capacity_ok_27ac304fc5982908', 'stellarator_09_materials_nb3sn_material_water_rejection_capacity_ok_f150ed41745d4a0f', 'stellarator_09_materials_nb3sn_material_water_head_capacity_ok_148d2392c7e3b09e', 'stellarator_09_materials_nb3sn_material_lp_flow_capacity_ok_b9357da3012ec632', 'stellarator_09_materials_nb3sn_material_facility_routes_ok_50ce1d1c00491ff5', 'stellarator_09_materials_nb3sn_material_helium_electric_capacity_ok_b6ae0d7d280eacb4', 'stellarator_09_materials_nb3sn_material_loop_capacity_ok_a12ef69878182648', 'stellarator_09_materials_nb3sn_material_electric_gross_capacity_ok_488a485d1eb1e88b', 'stellarator_09_materials_nb3sn_material_wp_fit_ok_11c66596aad579df', 'stellarator_09_materials_nb3sn_material_facility_replacement_ready_7aa76b338808935e', 'stellarator_09_materials_nb3sn_material_heating_source_positive_ok_d489a4b936f894ba', 'stellarator_09_materials_nb3sn_material_water_electric_capacity_ok_d2e2ee4a515ad778', 'stellarator_09_materials_nb3sn_material_condensate_flow_capacity_ok_ced096a46a13bff0', 'stellarator_09_materials_nb3sn_material_loop_pressure_ok_f97fa1dc432c78ba', 'stellarator_09_materials_nb3sn_material_matched_main_heat_direction_67f41575de96bd94', 'stellarator_09_materials_nb3sn_material_burn_hold_ok_8a46a7e0aeda985a', 'stellarator_09_materials_nb3sn_material_salt_electric_capacity_ok_320f302447d67a70', 'stellarator_09_materials_nb3sn_material_helium_pumping_capacity_ok_e41cbf588edbe7d8', 'stellarator_09_materials_nb3sn_material_facility_initial_ready_bd8b5a0e4ec512f7', 'stellarator_09_materials_nb3sn_material_matched_reheat_heat_direction_9cff90d247be59e3', 'stellarator_09_materials_nb3sn_material_condensate_electric_capacity_ok_886bd4436560bb81', 'stellarator_09_materials_nb3sn_material_main_UA_capacity_ok_5ee8c284f5da46ad', 'stellarator_09_materials_nb3sn_material_turbine_gross_capacity_ok_946403aa70c1c824', 'stellarator_09_materials_nb3sn_material_represented_coolant_fill_ok_81ed94010b513177')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 78, 'applicable_gate_total': 78, 'assessed_gate_count': 73, 'unassessed_gate_count': 5, 'inapplicable_gate_count': 0, 'unassessed_reasons': {'owner_has_no_occurrences': 5}, 'coverage_state': 'partial'}


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    stellarator_09_materials_nb3sn_material_cryoplant_capacity_ok_8830dacf5e39e904: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_magnet_pack_area_ok_51632f8f2a7b1d5f: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_magnet_acceptance_ok_0f682bc3436c0794: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_magnet_steel_ok_3f894fc95501d96d: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_magnet_ampere_floor_ok_bbe387e1eb85f9b9: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_magnet_copper_ok_be9121bc3fcdea7a: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_wp_stress_ok_c61cade8f669c8f2: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_cond_strain_ok_404dca1f50a13e3a: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_recirc_ok_097dfc7574999504: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_helium_pressure_rise_capacity_ok_4bbd03d1c0fdffdc: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_tbr_ok_d57174176b5d2862: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_cycle_domain_ok_76acde2a26a78109: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_occupancy_ok_e81ea8f8cf26823a: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_feedwater_electric_capacity_ok_c45a8ca67324291d: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_beta_ok_a6d1355f00db8834: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_material_capacity_ok_c7de34bf2e881cc4: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_parcel_ok_99f0ef2cd6538d03: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_fuel_processing_capacity_ok_d36667b777c42fe9: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_heating_couple_positive_ok_31dbd874e3b68e88: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_helium_flow_capacity_ok_631fba08153122f2: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_divertor_heat_ok_84770e9a36dc1b57: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_capacity_ok_6d4fb7d42a36d0a7: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_geometry_ok_14b78dfe909c8501: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_salt_flow_capacity_ok_090e097c99199295: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_water_flow_capacity_ok_71de9e2671863dbc: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_hp_shaft_capacity_ok_06729372362a4c6b: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_reheat_UA_capacity_ok_3832be39603086f5: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_outage_ok_93bfd834822ee642: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_heating_source_upper_ok_91d002eb84ef7479: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_net_positive_2ff2061dd70a24f7: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_hp_flow_capacity_ok_cc7e78dbd3c706de: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_feedwater_flow_capacity_ok_3bcdd6d04c7a0abb: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_cold_stage_capacity_ok_53d0507e047820a1: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_lp_shaft_capacity_ok_ef6a20387b2fc647: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_cooling_water_heat_direction_96754d6cc5733ef5: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_condensate_pressure_rise_capacity_ok_4758ab1d486197ab: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_direct_electric_capacity_ok_a285e66b19ed2cb4: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_ihx_capacity_ok_e4869509b6443c3b: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_magnet_pf_electric_capacity_ok_ca95b633e7cc10d5: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_magnet_tf_electric_capacity_ok_e99855ae6bf1b46e: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_sustainment_ok_1a778604648c352e: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_wall_load_ok_41289e190845d753: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_salt_head_capacity_ok_a3f15f8c47fee4d0: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_heating_couple_upper_ok_0e4c29c53a56780e: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_peak_field_ok_1fcd44510d5ceb9a: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_reference_conductor_current_ok_ed9bbbfb7399171f: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_intercept_stage_capacity_ok_94f24b6c7d86d868: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_feedwater_pressure_rise_capacity_ok_92e4f80e79613b88: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_salt_shaft_capacity_ok_316c1c5c7f51a07c: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_condenser_rejection_capacity_ok_27ac304fc5982908: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_water_rejection_capacity_ok_f150ed41745d4a0f: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_water_head_capacity_ok_148d2392c7e3b09e: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_lp_flow_capacity_ok_b9357da3012ec632: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_routes_ok_50ce1d1c00491ff5: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_helium_electric_capacity_ok_b6ae0d7d280eacb4: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_loop_capacity_ok_a12ef69878182648: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_electric_gross_capacity_ok_488a485d1eb1e88b: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_wp_fit_ok_11c66596aad579df: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_replacement_ready_7aa76b338808935e: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_heating_source_positive_ok_d489a4b936f894ba: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_water_electric_capacity_ok_d2e2ee4a515ad778: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_condensate_flow_capacity_ok_ced096a46a13bff0: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_loop_pressure_ok_f97fa1dc432c78ba: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_matched_main_heat_direction_67f41575de96bd94: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_burn_hold_ok_8a46a7e0aeda985a: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_salt_electric_capacity_ok_320f302447d67a70: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_helium_pumping_capacity_ok_e41cbf588edbe7d8: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_facility_initial_ready_bd8b5a0e4ec512f7: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_matched_reheat_heat_direction_9cff90d247be59e3: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_condensate_electric_capacity_ok_886bd4436560bb81: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_main_UA_capacity_ok_5ee8c284f5da46ad: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_turbine_gross_capacity_ok_946403aa70c1c824: ConstraintEvaluation
    stellarator_09_materials_nb3sn_material_represented_coolant_fill_ok_81ed94010b513177: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "fa2fb0901d79ed7eeaaf15ea09784a499a26a5567da2de9799eaed5ec5d381ed"

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
