"""Constraint module for stellarator_09_materials__nb3sn_material__cryoplant__capacity_ok__8830dacf5e39e904 (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Staged Cryoplant'::capacity_ok in owner instance stellarator_09_materials__nb3sn_material__cryoplant.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__refrigerator_capacity


class Nb3snMaterialCryoplantCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    capacity_margin_in: float


class Nb3snMaterialCryoplantCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialCryoplantCapacityOkConstraintModule(ModuleBase[Nb3snMaterialCryoplantCapacityOkConstraintInput, Nb3snMaterialCryoplantCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__cryoplant__capacity_ok__8830dacf5e39e904"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__cryoplant__capacity_ok__8830dacf5e39e904"

    def run(self, capacity_margin_in: float) -> ModuleResult[Nb3snMaterialCryoplantCapacityOkConstraintOutput]:
        Nb3snMaterialCryoplantCapacityOkConstraintInput(capacity_margin_in=capacity_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__refrigerator_capacity(capacity_margin_in=capacity_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialCryoplantCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"capacity_margin_in": float(capacity_margin_in)},
                )
            )
        )
