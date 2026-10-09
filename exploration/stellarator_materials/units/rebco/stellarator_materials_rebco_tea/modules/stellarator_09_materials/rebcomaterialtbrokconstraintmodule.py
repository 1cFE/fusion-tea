"""Constraint module for stellarator_09_materials__rebco_material__tbr_ok__8ce4a3c0d3818607 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::tbr_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_tritium_breeding__computed_tbr_adequacy


class RebcoMaterialTbrOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    defined_in: float
    numerical_margin_in: float


class RebcoMaterialTbrOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialTbrOkConstraintModule(ModuleBase[RebcoMaterialTbrOkConstraintInput, RebcoMaterialTbrOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__tbr_ok__8ce4a3c0d3818607"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__tbr_ok__8ce4a3c0d3818607"

    def run(self, defined_in: float, numerical_margin_in: float) -> ModuleResult[RebcoMaterialTbrOkConstraintOutput]:
        RebcoMaterialTbrOkConstraintInput(defined_in=defined_in, numerical_margin_in=numerical_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_tritium_breeding__computed_tbr_adequacy(defined_in=defined_in, numerical_margin_in=numerical_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialTbrOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "numerical_margin_in": float(numerical_margin_in)},
                )
            )
        )
