"""Constraint module for stellarator_09_materials__rebco_material__reheat_UA_capacity_ok__a8194f424b087b57 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::reheat_UA_capacity_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class RebcoMaterialReheatUaCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class RebcoMaterialReheatUaCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialReheatUaCapacityOkConstraintModule(ModuleBase[RebcoMaterialReheatUaCapacityOkConstraintInput, RebcoMaterialReheatUaCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__reheat_ua_capacity_ok__a8194f424b087b57"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__reheat_UA_capacity_ok__a8194f424b087b57"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[RebcoMaterialReheatUaCapacityOkConstraintOutput]:
        RebcoMaterialReheatUaCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialReheatUaCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
