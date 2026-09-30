"""Constraint module for stellarator_09_materials__rebco_material__ihx_capacity_ok__e64acdb414b82e94 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::rebco_material::ihx_capacity_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__intermediate_exchanger_capacity


class RebcoMaterialIhxCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    defined_in: float
    margin_m2_in: float


class RebcoMaterialIhxCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialIhxCapacityOkConstraintModule(ModuleBase[RebcoMaterialIhxCapacityOkConstraintInput, RebcoMaterialIhxCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__ihx_capacity_ok__e64acdb414b82e94"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__ihx_capacity_ok__e64acdb414b82e94"

    def run(self, defined_in: float, margin_m2_in: float) -> ModuleResult[RebcoMaterialIhxCapacityOkConstraintOutput]:
        RebcoMaterialIhxCapacityOkConstraintInput(defined_in=defined_in, margin_m2_in=margin_m2_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__intermediate_exchanger_capacity(defined_in=defined_in, margin_m2_in=margin_m2_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialIhxCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_m2_in": float(margin_m2_in)},
                )
            )
        )
