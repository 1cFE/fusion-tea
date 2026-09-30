"""Constraint module for stellarator_09_materials__rebco_material__magnet__ampere_floor_ok__527f82db402c44d5 (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Round1 REBCO Magnet System'::ampere_floor_ok in owner instance stellarator_09_materials__rebco_material__magnet.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_material_variants__ampere_floor


class RebcoMaterialMagnetAmpereFloorOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float


class RebcoMaterialMagnetAmpereFloorOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialMagnetAmpereFloorOkConstraintModule(ModuleBase[RebcoMaterialMagnetAmpereFloorOkConstraintInput, RebcoMaterialMagnetAmpereFloorOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__magnet__ampere_floor_ok__527f82db402c44d5"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__magnet__ampere_floor_ok__527f82db402c44d5"

    def run(self, margin_in: float) -> ModuleResult[RebcoMaterialMagnetAmpereFloorOkConstraintOutput]:
        RebcoMaterialMagnetAmpereFloorOkConstraintInput(margin_in=margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_material_variants__ampere_floor(margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialMagnetAmpereFloorOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_in": float(margin_in)},
                )
            )
        )
