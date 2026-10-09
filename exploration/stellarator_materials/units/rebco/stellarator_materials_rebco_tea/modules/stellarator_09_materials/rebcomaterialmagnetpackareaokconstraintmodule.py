"""Constraint module for stellarator_09_materials__rebco_material__magnet__pack_area_ok__4d2ccf27ef95a21a (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Round1 REBCO Magnet System'::pack_area_ok in owner instance stellarator_09_materials__rebco_material__magnet.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__winding_fit


class RebcoMaterialMagnetPackAreaOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    fit_margin_in: float


class RebcoMaterialMagnetPackAreaOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialMagnetPackAreaOkConstraintModule(ModuleBase[RebcoMaterialMagnetPackAreaOkConstraintInput, RebcoMaterialMagnetPackAreaOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__magnet__pack_area_ok__4d2ccf27ef95a21a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__magnet__pack_area_ok__4d2ccf27ef95a21a"

    def run(self, fit_margin_in: float) -> ModuleResult[RebcoMaterialMagnetPackAreaOkConstraintOutput]:
        RebcoMaterialMagnetPackAreaOkConstraintInput(fit_margin_in=fit_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__winding_fit(fit_margin_in=fit_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialMagnetPackAreaOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"fit_margin_in": float(fit_margin_in)},
                )
            )
        )
