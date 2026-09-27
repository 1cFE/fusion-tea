"""Constraint module for component_alternatives__plant__source_checks__flow_ok__d77445a069dcb805 (Item 7 / D2/D3/D9).

Effective predicate: component_alternatives::plant::source_checks::flow_ok in owner instance component_alternatives__plant__source_checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.schemas.constraint_types import ConstraintEvaluation
from component_alternatives_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__loop_capacity


class PlantSourceChecksFlowOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    mdot_loop_rated_in: float
    mdot_loop_in: float


class PlantSourceChecksFlowOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantSourceChecksFlowOkConstraintModule(ModuleBase[PlantSourceChecksFlowOkConstraintInput, PlantSourceChecksFlowOkConstraintOutput]):
    name: str = "component_alternatives__plant__source_checks__flow_ok__d77445a069dcb805"
    version: str = "v0.1"

    CONSTRAINT_ID = "component_alternatives__plant__source_checks__flow_ok__d77445a069dcb805"

    def run(self, mdot_loop_rated_in: float, mdot_loop_in: float) -> ModuleResult[PlantSourceChecksFlowOkConstraintOutput]:
        PlantSourceChecksFlowOkConstraintInput(mdot_loop_rated_in=mdot_loop_rated_in, mdot_loop_in=mdot_loop_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__loop_capacity(mdot_loop_in=mdot_loop_in, mdot_loop_rated_in=mdot_loop_rated_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantSourceChecksFlowOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"mdot_loop_in": float(mdot_loop_in), "mdot_loop_rated_in": float(mdot_loop_rated_in)},
                )
            )
        )
