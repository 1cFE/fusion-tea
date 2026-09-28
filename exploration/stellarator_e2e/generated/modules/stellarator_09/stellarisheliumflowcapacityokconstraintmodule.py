"""Constraint module for stellarator_09__stellaris__helium_flow_capacity_ok__de4eed99bc4bea72 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09::stellaris::helium_flow_capacity_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class StellarisHeliumFlowCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class StellarisHeliumFlowCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisHeliumFlowCapacityOkConstraintModule(ModuleBase[StellarisHeliumFlowCapacityOkConstraintInput, StellarisHeliumFlowCapacityOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__helium_flow_capacity_ok__de4eed99bc4bea72"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__helium_flow_capacity_ok__de4eed99bc4bea72"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[StellarisHeliumFlowCapacityOkConstraintOutput]:
        StellarisHeliumFlowCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisHeliumFlowCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
