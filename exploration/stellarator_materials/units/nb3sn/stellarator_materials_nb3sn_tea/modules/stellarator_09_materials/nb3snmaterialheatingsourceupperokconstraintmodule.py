"""Constraint module for stellarator_09_materials__nb3sn_material__heating_source_upper_ok__91d002eb84ef7479 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::heating_source_upper_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_heating_chain__heating_efficiency_upper


class Nb3snMaterialHeatingSourceUpperOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    efficiency: float


class Nb3snMaterialHeatingSourceUpperOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialHeatingSourceUpperOkConstraintModule(ModuleBase[Nb3snMaterialHeatingSourceUpperOkConstraintInput, Nb3snMaterialHeatingSourceUpperOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__heating_source_upper_ok__91d002eb84ef7479"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__heating_source_upper_ok__91d002eb84ef7479"

    def run(self, efficiency: float) -> ModuleResult[Nb3snMaterialHeatingSourceUpperOkConstraintOutput]:
        Nb3snMaterialHeatingSourceUpperOkConstraintInput(efficiency=efficiency)  # validate every resolved formal
        body = constraint_pred_definition_mfe_heating_chain__heating_efficiency_upper(efficiency=efficiency)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialHeatingSourceUpperOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"efficiency": float(efficiency)},
                )
            )
        )
