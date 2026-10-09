"""Constraint module for stellarator_09_materials__rebco_material__magnet__steel_ok__3833f52286c5bd91 (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Round1 REBCO Magnet System'::steel_ok in owner instance stellarator_09_materials__rebco_material__magnet.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__structural_steel_allowance


class RebcoMaterialMagnetSteelOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    steel_margin_in: float


class RebcoMaterialMagnetSteelOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialMagnetSteelOkConstraintModule(ModuleBase[RebcoMaterialMagnetSteelOkConstraintInput, RebcoMaterialMagnetSteelOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__magnet__steel_ok__3833f52286c5bd91"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__magnet__steel_ok__3833f52286c5bd91"

    def run(self, steel_margin_in: float) -> ModuleResult[RebcoMaterialMagnetSteelOkConstraintOutput]:
        RebcoMaterialMagnetSteelOkConstraintInput(steel_margin_in=steel_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__structural_steel_allowance(steel_margin_in=steel_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialMagnetSteelOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"steel_margin_in": float(steel_margin_in)},
                )
            )
        )
