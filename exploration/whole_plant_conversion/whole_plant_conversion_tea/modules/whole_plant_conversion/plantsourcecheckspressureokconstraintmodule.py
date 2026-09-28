"""Constraint module for whole_plant_conversion__plant__source_checks__pressure_ok__e9cb76bbd569aa90 (Item 7 / D2/D3/D9).

Effective predicate: whole_plant_conversion::plant::source_checks::pressure_ok in owner instance whole_plant_conversion__plant__source_checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from whole_plant_conversion_tea.schemas.constraint_types import ConstraintEvaluation
from whole_plant_conversion_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__loop_pressure_margin


class PlantSourceChecksPressureOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    p_loop_margin_in: float


class PlantSourceChecksPressureOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSourceChecksPressureOkConstraintModule(ModuleBase[PlantSourceChecksPressureOkConstraintInput, PlantSourceChecksPressureOkConstraintOutput]):
    name: str = "whole_plant_conversion__plant__source_checks__pressure_ok__e9cb76bbd569aa90"
    version: str = "v0.1"

    CONSTRAINT_ID = "whole_plant_conversion__plant__source_checks__pressure_ok__e9cb76bbd569aa90"

    def run(self, p_loop_margin_in: float) -> ModuleResult[PlantSourceChecksPressureOkConstraintOutput]:
        PlantSourceChecksPressureOkConstraintInput(p_loop_margin_in=p_loop_margin_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__loop_pressure_margin(p_loop_margin_in=p_loop_margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSourceChecksPressureOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"p_loop_margin_in": float(p_loop_margin_in)},
                )
            )
        )
