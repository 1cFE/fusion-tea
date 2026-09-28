"""Constraint module for whole_plant_conversion__plant__cryogenic_demand__cold_margin_w_ok__7dcadae371ddbe6d (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::cryogenic_demand::cold_margin_w_ok in owner instance whole_plant_conversion__plant__cryogenic_demand.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_whole_plant_conversion_accounts__whole_plant_nonnegative


class PlantCryogenicDemandColdMarginWOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    metric_in: float


class PlantCryogenicDemandColdMarginWOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantCryogenicDemandColdMarginWOkConstraintModule(ModuleBase[PlantCryogenicDemandColdMarginWOkConstraintInput, PlantCryogenicDemandColdMarginWOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__cryogenic_demand__cold_margin_w_ok__7dcadae371ddbe6d"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__cryogenic_demand__cold_margin_w_ok__7dcadae371ddbe6d"

    def run(self, metric_in: float) -> ModuleResult[PlantCryogenicDemandColdMarginWOkConstraintOutput]:
        PlantCryogenicDemandColdMarginWOkConstraintInput(metric_in=metric_in)  # validate every resolved formal
        body = constraint_pred_definition_whole_plant_conversion_accounts__whole_plant_nonnegative(metric_in=metric_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantCryogenicDemandColdMarginWOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"metric_in": float(metric_in)},
                )
            )
        )
