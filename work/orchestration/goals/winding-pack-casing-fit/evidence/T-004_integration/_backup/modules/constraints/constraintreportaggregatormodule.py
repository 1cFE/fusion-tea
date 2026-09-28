"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import (
    ConstraintEvaluation,
    ConstraintReport,
    CoverageAccount,
)

EXPECTED_IDS = ('stellarator_09_stellaris_wp_stress_ok_f38a102195da1dd0', 'stellarator_09_stellaris_cond_strain_ok_251d4c803804ab60', 'stellarator_09_stellaris_recirc_ok_afc3be66f0a3421b', 'stellarator_09_stellaris_cycle_domain_ok_ba3fa9c3653b3fd3', 'stellarator_09_stellaris_beta_ok_82b78aad420730d5', 'stellarator_09_stellaris_heating_couple_positive_ok_697e87be76f504b7', 'stellarator_09_stellaris_divertor_heat_ok_26b4658f9fdfd7b7', 'stellarator_09_stellaris_heating_source_upper_ok_14ddae450a8eda6f', 'stellarator_09_stellaris_net_positive_484521d56c02667a', 'stellarator_09_stellaris_burn_hold_ok_03c3f94b878e5b58', 'stellarator_09_stellaris_wall_load_ok_ab2c790419af93bb', 'stellarator_09_stellaris_tbr_ok_2cd198f674d413e4', 'stellarator_09_stellaris_heating_couple_upper_ok_6cc9307cc149d650', 'stellarator_09_stellaris_peak_field_ok_49c6b8228a73cac5', 'stellarator_09_stellaris_sustainment_ok_77add152ed8eafce', 'stellarator_09_stellaris_loop_capacity_ok_d77f6027ceb27852', 'stellarator_09_stellaris_wp_fit_ok_a25ca6a0161f6339', 'stellarator_09_stellaris_heating_source_positive_ok_1e184791591370e5', 'stellarator_09_stellaris_loop_pressure_ok_5905ab54f5e8a945')

#: The coverage account, derived at generation from the sealed catalog by
#: `generation/coverage.py::coverage_account` and baked here exactly the way
#: CATALOG_FINGERPRINT and EXPECTED_IDS are. Which gates are applicable and which were
#: assessed depends on the model, never on this candidate's input values, so recomputing it
#: per evaluation would recompute a constant.
COVERAGE = {'authored_usage_total': 19, 'applicable_gate_total': 19, 'assessed_gate_count': 19, 'unassessed_gate_count': 0, 'inapplicable_gate_count': 0, 'unassessed_reasons': {}, 'coverage_state': 'complete'}


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    stellarator_09_stellaris_wp_stress_ok_f38a102195da1dd0: ConstraintEvaluation
    stellarator_09_stellaris_cond_strain_ok_251d4c803804ab60: ConstraintEvaluation
    stellarator_09_stellaris_recirc_ok_afc3be66f0a3421b: ConstraintEvaluation
    stellarator_09_stellaris_cycle_domain_ok_ba3fa9c3653b3fd3: ConstraintEvaluation
    stellarator_09_stellaris_beta_ok_82b78aad420730d5: ConstraintEvaluation
    stellarator_09_stellaris_heating_couple_positive_ok_697e87be76f504b7: ConstraintEvaluation
    stellarator_09_stellaris_divertor_heat_ok_26b4658f9fdfd7b7: ConstraintEvaluation
    stellarator_09_stellaris_heating_source_upper_ok_14ddae450a8eda6f: ConstraintEvaluation
    stellarator_09_stellaris_net_positive_484521d56c02667a: ConstraintEvaluation
    stellarator_09_stellaris_burn_hold_ok_03c3f94b878e5b58: ConstraintEvaluation
    stellarator_09_stellaris_wall_load_ok_ab2c790419af93bb: ConstraintEvaluation
    stellarator_09_stellaris_tbr_ok_2cd198f674d413e4: ConstraintEvaluation
    stellarator_09_stellaris_heating_couple_upper_ok_6cc9307cc149d650: ConstraintEvaluation
    stellarator_09_stellaris_peak_field_ok_49c6b8228a73cac5: ConstraintEvaluation
    stellarator_09_stellaris_sustainment_ok_77add152ed8eafce: ConstraintEvaluation
    stellarator_09_stellaris_loop_capacity_ok_d77f6027ceb27852: ConstraintEvaluation
    stellarator_09_stellaris_wp_fit_ok_a25ca6a0161f6339: ConstraintEvaluation
    stellarator_09_stellaris_heating_source_positive_ok_1e184791591370e5: ConstraintEvaluation
    stellarator_09_stellaris_loop_pressure_ok_5905ab54f5e8a945: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "6b9183c0f94be2a260cca71c00dded5f447e749f4d97a9df4cffd14a566d303b"

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
