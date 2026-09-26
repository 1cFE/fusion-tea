"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('costed_loop_brayton_plant_generator_capacity_capacity_ok_866bb648afde20fc', 'costed_loop_brayton_plant_checks_net_positive_987a4d032b5440a8', 'costed_loop_brayton_plant_checks_loop_capacity_ok_9c561de0cd1f50b3', 'costed_loop_brayton_plant_checks_heat_removal_ok_177997e14a28cae1', 'costed_loop_brayton_plant_turbine_capacity_capacity_ok_583bf29eadcd21ed', 'costed_loop_brayton_plant_rejection_capacity_capacity_ok_839b61a7b3fe128c', 'costed_loop_brayton_plant_he_capacity_capacity_ok_5bc3ff690032908b', 'costed_loop_brayton_plant_compressor_capacity_capacity_ok_6e46ae5b5c0061be', 'costed_loop_brayton_plant_fuel_inventory_capacity_ok_9d250853407ea035')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 9, 'applicable_gate_total': 9, 'assessed_gate_count': 9, 'unassessed_gate_count': 0, 'inapplicable_gate_count': 0, 'unassessed_reasons': {}, 'coverage_state': 'complete'}


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    costed_loop_brayton_plant_generator_capacity_capacity_ok_866bb648afde20fc: ConstraintEvaluation
    costed_loop_brayton_plant_checks_net_positive_987a4d032b5440a8: ConstraintEvaluation
    costed_loop_brayton_plant_checks_loop_capacity_ok_9c561de0cd1f50b3: ConstraintEvaluation
    costed_loop_brayton_plant_checks_heat_removal_ok_177997e14a28cae1: ConstraintEvaluation
    costed_loop_brayton_plant_turbine_capacity_capacity_ok_583bf29eadcd21ed: ConstraintEvaluation
    costed_loop_brayton_plant_rejection_capacity_capacity_ok_839b61a7b3fe128c: ConstraintEvaluation
    costed_loop_brayton_plant_he_capacity_capacity_ok_5bc3ff690032908b: ConstraintEvaluation
    costed_loop_brayton_plant_compressor_capacity_capacity_ok_6e46ae5b5c0061be: ConstraintEvaluation
    costed_loop_brayton_plant_fuel_inventory_capacity_ok_9d250853407ea035: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "c909808a62e399a8bba73a66712e2e314f8673023f26632729a6478313488d4d"

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
