"""Constraint module for stellarator_09_materials__rebco_material__cryoplant__capacity_ok__a7ae0d27f2e7a69e (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Staged Cryoplant'::capacity_ok in owner instance stellarator_09_materials__rebco_material__cryoplant.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__refrigerator_capacity


class RebcoMaterialCryoplantCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    capacity_margin_in: float


class RebcoMaterialCryoplantCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialCryoplantCapacityOkConstraintModule(ModuleBase[RebcoMaterialCryoplantCapacityOkConstraintInput, RebcoMaterialCryoplantCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__cryoplant__capacity_ok__a7ae0d27f2e7a69e"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__cryoplant__capacity_ok__a7ae0d27f2e7a69e"

    def run(self, capacity_margin_in: float) -> ModuleResult[RebcoMaterialCryoplantCapacityOkConstraintOutput]:
        RebcoMaterialCryoplantCapacityOkConstraintInput(capacity_margin_in=capacity_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__refrigerator_capacity(capacity_margin_in=capacity_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialCryoplantCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"capacity_margin_in": float(capacity_margin_in)},
                )
            )
        )
