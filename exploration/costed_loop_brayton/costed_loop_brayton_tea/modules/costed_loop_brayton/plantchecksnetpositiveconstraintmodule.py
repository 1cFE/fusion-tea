"""Constraint module for costed_loop_brayton__plant__checks__net_positive__987a4d032b5440a8 (Item 7 / D2/D3/D9).

Effective predicate: costed_loop_brayton::plant::checks::net_positive in owner instance costed_loop_brayton__plant__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.schemas.constraint_types import ConstraintEvaluation
from costed_loop_brayton_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__net_power_positive


class PlantChecksNetPositiveConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    net_electric: float


class PlantChecksNetPositiveConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlantChecksNetPositiveConstraintModule(ModuleBase[PlantChecksNetPositiveConstraintInput, PlantChecksNetPositiveConstraintOutput]):
    name: str = "costed_loop_brayton__plant__checks__net_positive__987a4d032b5440a8"
    version: str = "v0.1"

    CONSTRAINT_ID = "costed_loop_brayton__plant__checks__net_positive__987a4d032b5440a8"

    def run(self, net_electric: float) -> ModuleResult[PlantChecksNetPositiveConstraintOutput]:
        PlantChecksNetPositiveConstraintInput(net_electric=net_electric)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__net_power_positive(net_electric=net_electric)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlantChecksNetPositiveConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"net_electric": float(net_electric)},
                )
            )
        )
