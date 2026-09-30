"""Constraint module for magnet_subsystem__subsystem__rebco__capacity_ok__ea481269af095f7f (Item 7 / D2/D3/D9).

Effective predicate: magnet_subsystem::subsystem::rebco::capacity_ok in owner instance magnet_subsystem__subsystem__rebco.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from magnet_materials_tea.schemas.constraint_types import ConstraintEvaluation
from magnet_materials_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__refrigerator_capacity


class SubsystemRebcoCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    capacity_margin_in: float


class SubsystemRebcoCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class SubsystemRebcoCapacityOkConstraintModule(ModuleBase[SubsystemRebcoCapacityOkConstraintInput, SubsystemRebcoCapacityOkConstraintOutput]):
    name: str = "magnet_subsystem__subsystem__rebco__capacity_ok__ea481269af095f7f"
    version: str = "v0.1"

    CONSTRAINT_ID = "magnet_subsystem__subsystem__rebco__capacity_ok__ea481269af095f7f"

    def run(self, capacity_margin_in: float) -> ModuleResult[SubsystemRebcoCapacityOkConstraintOutput]:
        SubsystemRebcoCapacityOkConstraintInput(capacity_margin_in=capacity_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__refrigerator_capacity(capacity_margin_in=capacity_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=SubsystemRebcoCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"capacity_margin_in": float(capacity_margin_in)},
                )
            )
        )
