"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('combinations_lumped_fit_lumped_fit_he_fit_domain_ok_b88eae8078e8995f', 'combinations_lumped_fit_lumped_fit_pbli_fit_domain_ok_f30925cbe487ee4d', 'combinations_lumped_fit_lumped_fit_divertor_fit_domain_ok_72e8945d8d697cd1', 'combinations_circulator_purchase_circulator_purchase_circulator_capacity_capacity_ok_4ffbb5ea99182b98', 'combinations_plasma_chain_plasma_chain_he_capacity_capacity_ok_d2b59d407f4559fd', 'combinations_plasma_chain_plasma_chain_divertor_pump_capacity_ok_b0d2ef5eececd260', 'combinations_plasma_chain_plasma_chain_pbli_pump_capacity_ok_2740088b7321b64f', 'combinations_plasma_chain_plasma_chain_rejection_capacity_capacity_ok_77de6a398fb88ba8', 'combinations_plasma_chain_plasma_chain_generator_capacity_capacity_ok_c425e327953b0497', 'combinations_plasma_chain_plasma_chain_checks_heat_removal_ok_e3aa56b0160f3e08', 'combinations_plasma_chain_plasma_chain_checks_net_positive_1ca673e570772897', 'combinations_plasma_chain_plasma_chain_turbine_capacity_capacity_ok_a7b56c68f9f9a298', 'combinations_plasma_chain_plasma_chain_divertor_capacity_capacity_ok_f4df61f2684e5d3c', 'combinations_plasma_chain_plasma_chain_he_pump_capacity_ok_933c88ced63feb63', 'combinations_plasma_chain_plasma_chain_compressor_capacity_capacity_ok_0bc93f698ed19a5d', 'combinations_plasma_chain_plasma_chain_pbli_capacity_capacity_ok_16d446380d5ebc09', 'combinations_plasma_chain_plasma_chain_fuel_capacity_capacity_ok_5c625963d8a8bf70', 'combinations_loop_brayton_loop_brayton_turbine_capacity_capacity_ok_a4f0ad4edcd0de39', 'combinations_loop_brayton_loop_brayton_checks_heat_removal_ok_c7a2f9638fd1e56b', 'combinations_loop_brayton_loop_brayton_checks_net_positive_d22e3a3d83be3d66', 'combinations_loop_brayton_loop_brayton_checks_loop_capacity_ok_42cc45f771fa6628', 'combinations_loop_brayton_loop_brayton_rejection_capacity_capacity_ok_f641e3674fbef65a', 'combinations_loop_brayton_loop_brayton_he_capacity_capacity_ok_5a310602c6faa347', 'combinations_loop_brayton_loop_brayton_compressor_capacity_capacity_ok_cb22fc3ae07b48e1', 'combinations_loop_brayton_loop_brayton_generator_capacity_capacity_ok_d2956d9503aa885e')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 25, 'applicable_gate_total': 25, 'assessed_gate_count': 25, 'unassessed_gate_count': 0, 'inapplicable_gate_count': 0, 'unassessed_reasons': {}, 'coverage_state': 'complete'}


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    combinations_lumped_fit_lumped_fit_he_fit_domain_ok_b88eae8078e8995f: ConstraintEvaluation
    combinations_lumped_fit_lumped_fit_pbli_fit_domain_ok_f30925cbe487ee4d: ConstraintEvaluation
    combinations_lumped_fit_lumped_fit_divertor_fit_domain_ok_72e8945d8d697cd1: ConstraintEvaluation
    combinations_circulator_purchase_circulator_purchase_circulator_capacity_capacity_ok_4ffbb5ea99182b98: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_he_capacity_capacity_ok_d2b59d407f4559fd: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_divertor_pump_capacity_ok_b0d2ef5eececd260: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_pbli_pump_capacity_ok_2740088b7321b64f: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_rejection_capacity_capacity_ok_77de6a398fb88ba8: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_generator_capacity_capacity_ok_c425e327953b0497: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_checks_heat_removal_ok_e3aa56b0160f3e08: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_checks_net_positive_1ca673e570772897: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_turbine_capacity_capacity_ok_a7b56c68f9f9a298: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_divertor_capacity_capacity_ok_f4df61f2684e5d3c: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_he_pump_capacity_ok_933c88ced63feb63: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_compressor_capacity_capacity_ok_0bc93f698ed19a5d: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_pbli_capacity_capacity_ok_16d446380d5ebc09: ConstraintEvaluation
    combinations_plasma_chain_plasma_chain_fuel_capacity_capacity_ok_5c625963d8a8bf70: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_turbine_capacity_capacity_ok_a4f0ad4edcd0de39: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_checks_heat_removal_ok_c7a2f9638fd1e56b: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_checks_net_positive_d22e3a3d83be3d66: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_checks_loop_capacity_ok_42cc45f771fa6628: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_rejection_capacity_capacity_ok_f641e3674fbef65a: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_he_capacity_capacity_ok_5a310602c6faa347: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_compressor_capacity_capacity_ok_cb22fc3ae07b48e1: ConstraintEvaluation
    combinations_loop_brayton_loop_brayton_generator_capacity_capacity_ok_d2956d9503aa885e: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "e4485b61f27aada4a8b666ffcc7745205feabe09a8c0ed4ec60ebc8e3a60f2f7"

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
