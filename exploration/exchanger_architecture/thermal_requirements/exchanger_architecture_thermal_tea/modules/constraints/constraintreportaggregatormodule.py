"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('aries_integrated_plant_divertor_pump_capacity_ok_d6730c7060447f4c', 'aries_integrated_plant_rejection_capacity_capacity_ok_295420bc9fb25608', 'aries_integrated_plant_turbine_capacity_capacity_ok_089f9e8e61919ec1', 'aries_integrated_plant_compressor_capacity_capacity_ok_a45f9cf05e8aa7ab', 'aries_integrated_plant_fuel_inventory_capacity_ok_37f4667fbfb616d0', 'aries_integrated_plant_pbli_capacity_capacity_ok_55a012a287da9395', 'aries_integrated_plant_divertor_capacity_capacity_ok_be7081920ad8e8ed', 'aries_integrated_plant_he_pump_capacity_ok_fcee5ee009fe5180', 'aries_integrated_plant_fuel_capacity_capacity_ok_8eb5888bfe62cd64', 'aries_integrated_plant_heat_exchangers_divertor_return_ok_f69c5310bdcc41d7', 'aries_integrated_plant_heat_exchangers_pbli_control_ok_0c3b021e2e8589fb', 'aries_integrated_plant_heat_exchangers_pbli_return_ok_100f6bf9ad61a22c', 'aries_integrated_plant_heat_exchangers_divertor_control_ok_14c1c0f314a994fd', 'aries_integrated_plant_heat_exchangers_he_return_ok_ae5f4d6db630fc8e', 'aries_integrated_plant_heat_exchangers_divertor_cold_approach_ok_e70598993d392f74', 'aries_integrated_plant_heat_exchangers_pbli_state_ok_4664e5e1ddbb7ac5', 'aries_integrated_plant_heat_exchangers_he_required_hot_ok_3371b55ff752c6e4', 'aries_integrated_plant_heat_exchangers_he_state_ok_d5b9d58030392fe5', 'aries_integrated_plant_heat_exchangers_divertor_state_ok_416e01681b16be81', 'aries_integrated_plant_heat_exchangers_he_hot_cap_ok_05ebd6dad2e4adc1', 'aries_integrated_plant_heat_exchangers_pbli_cold_approach_ok_667d6ca45c6e61de', 'aries_integrated_plant_heat_exchangers_he_control_ok_f48454bb1d6f0e91', 'aries_integrated_plant_heat_exchangers_divertor_required_hot_ok_712add8be60bd1ae', 'aries_integrated_plant_heat_exchangers_he_hot_approach_ok_7a2967e855192aeb', 'aries_integrated_plant_heat_exchangers_pbli_hot_approach_ok_85855c74bdb13305', 'aries_integrated_plant_heat_exchangers_divertor_hot_cap_ok_cd5f29bd8533c481', 'aries_integrated_plant_heat_exchangers_pbli_hot_cap_ok_73a44108fcb5be1c', 'aries_integrated_plant_heat_exchangers_divertor_hot_approach_ok_5e95ef937d10cc33', 'aries_integrated_plant_heat_exchangers_he_cold_approach_ok_eab4f3486f0aa140', 'aries_integrated_plant_heat_exchangers_pbli_required_hot_ok_aa9057b8ce236e6b', 'aries_integrated_plant_he_capacity_capacity_ok_db2733d1d5baf3cf', 'aries_integrated_plant_pbli_pump_capacity_ok_79d116aa320dd4fb', 'aries_integrated_plant_generator_capacity_capacity_ok_60b43f15d48ff161', 'aries_integrated_plant_plant_ledger_heat_removal_ok_695378663bcd8d07', 'aries_integrated_plant_plant_ledger_balances_ok_9af2e85b5e4e5535')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 35, 'applicable_gate_total': 35, 'assessed_gate_count': 35, 'unassessed_gate_count': 0, 'inapplicable_gate_count': 0, 'unassessed_reasons': {}, 'coverage_state': 'complete'}


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    aries_integrated_plant_divertor_pump_capacity_ok_d6730c7060447f4c: ConstraintEvaluation
    aries_integrated_plant_rejection_capacity_capacity_ok_295420bc9fb25608: ConstraintEvaluation
    aries_integrated_plant_turbine_capacity_capacity_ok_089f9e8e61919ec1: ConstraintEvaluation
    aries_integrated_plant_compressor_capacity_capacity_ok_a45f9cf05e8aa7ab: ConstraintEvaluation
    aries_integrated_plant_fuel_inventory_capacity_ok_37f4667fbfb616d0: ConstraintEvaluation
    aries_integrated_plant_pbli_capacity_capacity_ok_55a012a287da9395: ConstraintEvaluation
    aries_integrated_plant_divertor_capacity_capacity_ok_be7081920ad8e8ed: ConstraintEvaluation
    aries_integrated_plant_he_pump_capacity_ok_fcee5ee009fe5180: ConstraintEvaluation
    aries_integrated_plant_fuel_capacity_capacity_ok_8eb5888bfe62cd64: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_divertor_return_ok_f69c5310bdcc41d7: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_pbli_control_ok_0c3b021e2e8589fb: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_pbli_return_ok_100f6bf9ad61a22c: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_divertor_control_ok_14c1c0f314a994fd: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_he_return_ok_ae5f4d6db630fc8e: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_divertor_cold_approach_ok_e70598993d392f74: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_pbli_state_ok_4664e5e1ddbb7ac5: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_he_required_hot_ok_3371b55ff752c6e4: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_he_state_ok_d5b9d58030392fe5: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_divertor_state_ok_416e01681b16be81: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_he_hot_cap_ok_05ebd6dad2e4adc1: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_pbli_cold_approach_ok_667d6ca45c6e61de: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_he_control_ok_f48454bb1d6f0e91: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_divertor_required_hot_ok_712add8be60bd1ae: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_he_hot_approach_ok_7a2967e855192aeb: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_pbli_hot_approach_ok_85855c74bdb13305: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_divertor_hot_cap_ok_cd5f29bd8533c481: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_pbli_hot_cap_ok_73a44108fcb5be1c: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_divertor_hot_approach_ok_5e95ef937d10cc33: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_he_cold_approach_ok_eab4f3486f0aa140: ConstraintEvaluation
    aries_integrated_plant_heat_exchangers_pbli_required_hot_ok_aa9057b8ce236e6b: ConstraintEvaluation
    aries_integrated_plant_he_capacity_capacity_ok_db2733d1d5baf3cf: ConstraintEvaluation
    aries_integrated_plant_pbli_pump_capacity_ok_79d116aa320dd4fb: ConstraintEvaluation
    aries_integrated_plant_generator_capacity_capacity_ok_60b43f15d48ff161: ConstraintEvaluation
    aries_integrated_plant_plant_ledger_heat_removal_ok_695378663bcd8d07: ConstraintEvaluation
    aries_integrated_plant_plant_ledger_balances_ok_9af2e85b5e4e5535: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "252ea329ab805a5521706f777b411e46c39c519a057176a4682350c993b80f57"

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
