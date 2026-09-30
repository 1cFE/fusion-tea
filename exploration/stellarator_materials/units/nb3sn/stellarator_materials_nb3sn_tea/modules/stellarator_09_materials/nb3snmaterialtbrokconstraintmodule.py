"""Constraint module for stellarator_09_materials__nb3sn_material__tbr_ok__d57174176b5d2862 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::nb3sn_material::tbr_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_tritium_breeding__computed_tbr_adequacy


class Nb3snMaterialTbrOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    defined_in: float
    numerical_margin_in: float


class Nb3snMaterialTbrOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialTbrOkConstraintModule(ModuleBase[Nb3snMaterialTbrOkConstraintInput, Nb3snMaterialTbrOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__tbr_ok__d57174176b5d2862"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__tbr_ok__d57174176b5d2862"

    def run(self, defined_in: float, numerical_margin_in: float) -> ModuleResult[Nb3snMaterialTbrOkConstraintOutput]:
        Nb3snMaterialTbrOkConstraintInput(defined_in=defined_in, numerical_margin_in=numerical_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_tritium_breeding__computed_tbr_adequacy(defined_in=defined_in, numerical_margin_in=numerical_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialTbrOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "numerical_margin_in": float(numerical_margin_in)},
                )
            )
        )
