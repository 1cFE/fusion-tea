"""Constraint module for stellarator_09_materials__rebco_material__loop_pressure_ok__aef108bdfd08fc32 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::loop_pressure_ok in owner instance stellarator_09_materials__rebco_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_rebco_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_rebco_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__loop_pressure_margin


class RebcoMaterialLoopPressureOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    p_loop_margin_in: float


class RebcoMaterialLoopPressureOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class RebcoMaterialLoopPressureOkConstraintModule(ModuleBase[RebcoMaterialLoopPressureOkConstraintInput, RebcoMaterialLoopPressureOkConstraintOutput]):
    name: str = "stellarator_09_materials__rebco_material__loop_pressure_ok__aef108bdfd08fc32"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__rebco_material__loop_pressure_ok__aef108bdfd08fc32"

    def run(self, p_loop_margin_in: float) -> ModuleResult[RebcoMaterialLoopPressureOkConstraintOutput]:
        RebcoMaterialLoopPressureOkConstraintInput(p_loop_margin_in=p_loop_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__loop_pressure_margin(p_loop_margin_in=p_loop_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=RebcoMaterialLoopPressureOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"p_loop_margin_in": float(p_loop_margin_in)},
                )
            )
        )
