"""Constraint module for stellarator_09_materials__rebco_material__magnet__acceptance_ok__998be97e16fad569 (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Round1 REBCO Magnet System'::acceptance_ok in owner instance stellarator_09_materials__rebco_material__magnet.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance


class RebcoMaterialMagnetAcceptanceOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    supported_in: float


class RebcoMaterialMagnetAcceptanceOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialMagnetAcceptanceOkConstraintModule(ModuleBase[RebcoMaterialMagnetAcceptanceOkConstraintInput, RebcoMaterialMagnetAcceptanceOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__magnet__acceptance_ok__998be97e16fad569"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__magnet__acceptance_ok__998be97e16fad569"

    def run(self, margin_in: float, supported_in: float) -> ModuleResult[RebcoMaterialMagnetAcceptanceOkConstraintOutput]:
        RebcoMaterialMagnetAcceptanceOkConstraintInput(margin_in=margin_in, supported_in=supported_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance(supported_in=supported_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialMagnetAcceptanceOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"supported_in": float(supported_in), "margin_in": float(margin_in)},
                )
            )
        )
