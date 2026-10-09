"""Constraint module for stellarator_09__stellaris__feedwater_flow_capacity_ok__3065124bba3fb314 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::feedwater_flow_capacity_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_reference_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class StellarisFeedwaterFlowCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class StellarisFeedwaterFlowCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisFeedwaterFlowCapacityOkConstraintModule(ModuleBase[StellarisFeedwaterFlowCapacityOkConstraintInput, StellarisFeedwaterFlowCapacityOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__feedwater_flow_capacity_ok__3065124bba3fb314"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__feedwater_flow_capacity_ok__3065124bba3fb314"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[StellarisFeedwaterFlowCapacityOkConstraintOutput]:
        StellarisFeedwaterFlowCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisFeedwaterFlowCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
