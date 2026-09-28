"""Constraint module for costed_loop_brayton__plant__checks__heat_removal_ok__177997e14a28cae1 (Item 7 / D2/D3/D9).

Effective predicate: costed_loop_brayton::plant::checks::heat_removal_ok in owner instance costed_loop_brayton__plant__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.schemas.constraint_types import ConstraintEvaluation
from costed_loop_brayton_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate


class PlantChecksHeatRemovalOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    unmet_in: float


class PlantChecksHeatRemovalOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantChecksHeatRemovalOkConstraintModule(ModuleBase[PlantChecksHeatRemovalOkConstraintInput, PlantChecksHeatRemovalOkConstraintOutput]):
    name: str = "costed_loop_brayton__plant__checks__heat_removal_ok__177997e14a28cae1"
    version: str = "v0.1"

    CONSTRAINT_ID = "costed_loop_brayton__plant__checks__heat_removal_ok__177997e14a28cae1"

    def run(self, tolerance_in: float, unmet_in: float) -> ModuleResult[PlantChecksHeatRemovalOkConstraintOutput]:
        PlantChecksHeatRemovalOkConstraintInput(tolerance_in=tolerance_in, unmet_in=unmet_in)  # validate every resolved formal
        body = constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate(unmet_in=unmet_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantChecksHeatRemovalOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"unmet_in": float(unmet_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
