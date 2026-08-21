"""Constraint report aggregator (Item 7 / D5/D11) — exact schema, one required field per
eligible assertion.

Exists even for zero eligible assertions (D11): a missing result is a schema failure, never a
silent gap.
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation, ConstraintReport

EXPECTED_IDS = ('stellarator_09_stellaris_beta_ok_82b78aad420730d5', 'stellarator_09_stellaris_net_positive_484521d56c02667a', 'stellarator_09_stellaris_recirc_ok_afc3be66f0a3421b', 'stellarator_09_stellaris_tbr_ok_2cd198f674d413e4', 'stellarator_09_stellaris_wall_load_ok_ab2c790419af93bb')


class ConstraintReportAggregatorInput(BaseModel):
    model_config = {"extra": "forbid"}

    stellarator_09_stellaris_beta_ok_82b78aad420730d5: ConstraintEvaluation
    stellarator_09_stellaris_net_positive_484521d56c02667a: ConstraintEvaluation
    stellarator_09_stellaris_recirc_ok_afc3be66f0a3421b: ConstraintEvaluation
    stellarator_09_stellaris_tbr_ok_2cd198f674d413e4: ConstraintEvaluation
    stellarator_09_stellaris_wall_load_ok_ab2c790419af93bb: ConstraintEvaluation


class ConstraintReportAggregatorOutput(MultiOutput):
    constraint_report: ConstraintReport


class ConstraintReportAggregatorModule(
    ModuleBase[ConstraintReportAggregatorInput, ConstraintReportAggregatorOutput]
):
    name: str = "constraint_report_aggregator"
    version: str = "v0.1"

    CATALOG_FINGERPRINT = "c565283a88599da6a2186b4092dc3eed9574a9870458cc45a76eabaeac4cdf2f"

    def run(self, **evaluations) -> ModuleResult[ConstraintReportAggregatorOutput]:
        validated = ConstraintReportAggregatorInput(**evaluations)
        results = [getattr(validated, cid) for cid in EXPECTED_IDS]
        statuses = [r.status for r in results]
        if "violated" in statuses:
            headline = "violation"
        elif "indeterminate" in statuses:
            headline = "indeterminate"
        elif results:
            headline = "all_satisfied"
        else:
            headline = "not_assessed"
        return ModuleResult(
            data=ConstraintReportAggregatorOutput(
                constraint_report=ConstraintReport(
                    catalog_fingerprint=self.CATALOG_FINGERPRINT,
                    assessed_count=len(results),
                    headline=headline,
                    results=results,
                )
            )
        )
