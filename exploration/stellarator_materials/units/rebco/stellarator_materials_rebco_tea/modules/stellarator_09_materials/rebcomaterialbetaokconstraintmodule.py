"""Constraint module for stellarator_09_materials__rebco_material__beta_ok__35a0c2df4310d104 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::beta_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__beta_limit


class RebcoMaterialBetaOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    beta_in: float
    beta_limit_in: float


class RebcoMaterialBetaOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialBetaOkConstraintModule(ModuleBase[RebcoMaterialBetaOkConstraintInput, RebcoMaterialBetaOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__beta_ok__35a0c2df4310d104"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__beta_ok__35a0c2df4310d104"

    def run(self, beta_in: float, beta_limit_in: float) -> ModuleResult[RebcoMaterialBetaOkConstraintOutput]:
        RebcoMaterialBetaOkConstraintInput(beta_in=beta_in, beta_limit_in=beta_limit_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__beta_limit(beta_in=beta_in, beta_limit_in=beta_limit_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialBetaOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"beta_in": float(beta_in), "beta_limit_in": float(beta_limit_in)},
                )
            )
        )
