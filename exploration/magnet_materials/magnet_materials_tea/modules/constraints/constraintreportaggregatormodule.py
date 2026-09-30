"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('magnet_subsystem_subsystem_rebco_capacity_ok_ea481269af095f7f', 'magnet_subsystem_subsystem_rebco_fit_ok_977ffb782260e056', 'magnet_subsystem_subsystem_rebco_copper_ok_b9db08c2aa4dd8f9', 'magnet_subsystem_subsystem_rebco_steel_ok_4f587fec2c667312', 'magnet_subsystem_subsystem_rebco_acceptance_ok_904ca5528ef92aa4', 'magnet_subsystem_subsystem_nb3sn_capacity_ok_c900a95e873755be', 'magnet_subsystem_subsystem_nb3sn_copper_ok_a4ff5a6abedecdd2', 'magnet_subsystem_subsystem_nb3sn_fit_ok_768d741c21386f93', 'magnet_subsystem_subsystem_nb3sn_acceptance_ok_6ecc44a52542ba77', 'magnet_subsystem_subsystem_nb3sn_steel_ok_5d849655e24deaf4')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 10, 'applicable_gate_total': 10, 'assessed_gate_count': 10, 'unassessed_gate_count': 0, 'inapplicable_gate_count': 0, 'unassessed_reasons': {}, 'coverage_state': 'complete'}


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    magnet_subsystem_subsystem_rebco_capacity_ok_ea481269af095f7f: ConstraintEvaluation
    magnet_subsystem_subsystem_rebco_fit_ok_977ffb782260e056: ConstraintEvaluation
    magnet_subsystem_subsystem_rebco_copper_ok_b9db08c2aa4dd8f9: ConstraintEvaluation
    magnet_subsystem_subsystem_rebco_steel_ok_4f587fec2c667312: ConstraintEvaluation
    magnet_subsystem_subsystem_rebco_acceptance_ok_904ca5528ef92aa4: ConstraintEvaluation
    magnet_subsystem_subsystem_nb3sn_capacity_ok_c900a95e873755be: ConstraintEvaluation
    magnet_subsystem_subsystem_nb3sn_copper_ok_a4ff5a6abedecdd2: ConstraintEvaluation
    magnet_subsystem_subsystem_nb3sn_fit_ok_768d741c21386f93: ConstraintEvaluation
    magnet_subsystem_subsystem_nb3sn_acceptance_ok_6ecc44a52542ba77: ConstraintEvaluation
    magnet_subsystem_subsystem_nb3sn_steel_ok_5d849655e24deaf4: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "5590514b5020a3b645b72bf80aeb4ac7df80dc8b7a91613576853d60d85972f1"

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
