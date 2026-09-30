"""Constraint module for stellarator_09_materials__rebco_material__heating_couple_upper_ok__d388de0d1f5a62b5 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::heating_couple_upper_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_heating_chain__heating_efficiency_upper


class RebcoMaterialHeatingCoupleUpperOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    efficiency: float


class RebcoMaterialHeatingCoupleUpperOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialHeatingCoupleUpperOkConstraintModule(ModuleBase[RebcoMaterialHeatingCoupleUpperOkConstraintInput, RebcoMaterialHeatingCoupleUpperOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__heating_couple_upper_ok__d388de0d1f5a62b5"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__heating_couple_upper_ok__d388de0d1f5a62b5"

    def run(self, efficiency: float) -> ModuleResult[RebcoMaterialHeatingCoupleUpperOkConstraintOutput]:
        RebcoMaterialHeatingCoupleUpperOkConstraintInput(efficiency=efficiency)  # validate every resolved formal
        body = constraint_pred_definition_mfe_heating_chain__heating_efficiency_upper(efficiency=efficiency)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialHeatingCoupleUpperOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"efficiency": float(efficiency)},
                )
            )
        )
