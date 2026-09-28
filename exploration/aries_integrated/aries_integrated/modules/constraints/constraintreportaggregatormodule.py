"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('aries_integrated_plant_divertor_pump_capacity_ok_d6730c7060447f4c', 'aries_integrated_plant_rejection_capacity_capacity_ok_295420bc9fb25608', 'aries_integrated_plant_turbine_capacity_capacity_ok_089f9e8e61919ec1', 'aries_integrated_plant_compressor_capacity_capacity_ok_a45f9cf05e8aa7ab', 'aries_integrated_plant_fuel_inventory_capacity_ok_37f4667fbfb616d0', 'aries_integrated_plant_pbli_capacity_capacity_ok_55a012a287da9395', 'aries_integrated_plant_divertor_capacity_capacity_ok_be7081920ad8e8ed', 'aries_integrated_plant_he_pump_capacity_ok_fcee5ee009fe5180', 'aries_integrated_plant_fuel_capacity_capacity_ok_8eb5888bfe62cd64', 'aries_integrated_plant_he_capacity_capacity_ok_db2733d1d5baf3cf', 'aries_integrated_plant_pbli_pump_capacity_ok_79d116aa320dd4fb', 'aries_integrated_plant_generator_capacity_capacity_ok_60b43f15d48ff161', 'aries_integrated_plant_plant_ledger_heat_removal_ok_695378663bcd8d07', 'aries_integrated_plant_plant_ledger_balances_ok_9af2e85b5e4e5535')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 14, 'applicable_gate_total': 14, 'assessed_gate_count': 14, 'unassessed_gate_count': 0, 'inapplicable_gate_count': 0, 'unassessed_reasons': {}, 'coverage_state': 'complete'}


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

    CATALOG_FINGERPRINT = "b2fdfd4e0b31a376f963243a06c935cdb4295e916d307d31cfaddc9ade75ce5f"

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
