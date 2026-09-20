"""Constraint module for stellarator_09__stellaris__condensate_flow_capacity_ok__252eeccf9b929ade (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::condensate_flow_capacity_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class StellarisCondensateFlowCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class StellarisCondensateFlowCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisCondensateFlowCapacityOkConstraintModule(ModuleBase[StellarisCondensateFlowCapacityOkConstraintInput, StellarisCondensateFlowCapacityOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__condensate_flow_capacity_ok__252eeccf9b929ade"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__condensate_flow_capacity_ok__252eeccf9b929ade"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[StellarisCondensateFlowCapacityOkConstraintOutput]:
        StellarisCondensateFlowCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisCondensateFlowCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
