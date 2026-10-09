"""Constraint module for stellarator_09_materials__rebco_material__represented_coolant_fill_ok__bc6a51fed9b48ceb (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::represented_coolant_fill_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__represented_coolant_fill


class RebcoMaterialRepresentedCoolantFillOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    defined_in: float
    helium_margin_in: float
    salt_margin_in: float


class RebcoMaterialRepresentedCoolantFillOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialRepresentedCoolantFillOkConstraintModule(ModuleBase[RebcoMaterialRepresentedCoolantFillOkConstraintInput, RebcoMaterialRepresentedCoolantFillOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__represented_coolant_fill_ok__bc6a51fed9b48ceb"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__represented_coolant_fill_ok__bc6a51fed9b48ceb"

    def run(self, defined_in: float, helium_margin_in: float, salt_margin_in: float) -> ModuleResult[RebcoMaterialRepresentedCoolantFillOkConstraintOutput]:
        RebcoMaterialRepresentedCoolantFillOkConstraintInput(defined_in=defined_in, helium_margin_in=helium_margin_in, salt_margin_in=salt_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__represented_coolant_fill(defined_in=defined_in, helium_margin_in=helium_margin_in, salt_margin_in=salt_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialRepresentedCoolantFillOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "helium_margin_in": float(helium_margin_in), "salt_margin_in": float(salt_margin_in)},
                )
            )
        )
