"""Constraint module for stellarator_09_materials__nb3sn_material__magnet__acceptance_ok__0f682bc3436c0794 (Item 7 / D2/D3/D9).

Effective predicate: magnet_material_variants::'Nb3Sn Magnet System'::acceptance_ok in owner instance stellarator_09_materials__nb3sn_material__magnet.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance


class Nb3snMaterialMagnetAcceptanceOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    supported_in: float


class Nb3snMaterialMagnetAcceptanceOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialMagnetAcceptanceOkConstraintModule(ModuleBase[Nb3snMaterialMagnetAcceptanceOkConstraintInput, Nb3snMaterialMagnetAcceptanceOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__magnet__acceptance_ok__0f682bc3436c0794"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__magnet__acceptance_ok__0f682bc3436c0794"

    def run(self, margin_in: float, supported_in: float) -> ModuleResult[Nb3snMaterialMagnetAcceptanceOkConstraintOutput]:
        Nb3snMaterialMagnetAcceptanceOkConstraintInput(margin_in=margin_in, supported_in=supported_in)  # validate every resolved formal
        body = constraint_pred_definition_magnet_conductor_alternatives__conductor_acceptance(supported_in=supported_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialMagnetAcceptanceOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"supported_in": float(supported_in), "margin_in": float(margin_in)},
                )
            )
        )
