"""Constraint module for stellarator_09_materials__nb3sn_material__heating_couple_positive_ok__31dbd874e3b68e88 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::heating_couple_positive_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_heating_chain__heating_efficiency_positive


class Nb3snMaterialHeatingCouplePositiveOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    efficiency: float


class Nb3snMaterialHeatingCouplePositiveOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialHeatingCouplePositiveOkConstraintModule(ModuleBase[Nb3snMaterialHeatingCouplePositiveOkConstraintInput, Nb3snMaterialHeatingCouplePositiveOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__heating_couple_positive_ok__31dbd874e3b68e88"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__heating_couple_positive_ok__31dbd874e3b68e88"

    def run(self, efficiency: float) -> ModuleResult[Nb3snMaterialHeatingCouplePositiveOkConstraintOutput]:
        Nb3snMaterialHeatingCouplePositiveOkConstraintInput(efficiency=efficiency)  # validate every resolved formal
        body = constraint_pred_definition_mfe_heating_chain__heating_efficiency_positive(efficiency=efficiency)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialHeatingCouplePositiveOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"efficiency": float(efficiency)},
                )
            )
        )
