"""Constraint module for combinations_plasma_chain__plasma_chain__checks__heat_removal_ok__e3aa56b0160f3e08 (Item 7 / D2/D3/D9).

Effective predicate: combinations_plasma_chain::plasma_chain::checks::heat_removal_ok in owner instance combinations_plasma_chain__plasma_chain__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate


class PlasmaChainChecksHeatRemovalOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    tolerance_in: float
    unmet_in: float


class PlasmaChainChecksHeatRemovalOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlasmaChainChecksHeatRemovalOkConstraintModule(ModuleBase[PlasmaChainChecksHeatRemovalOkConstraintInput, PlasmaChainChecksHeatRemovalOkConstraintOutput]):
    name: str = "combinations_plasma_chain__plasma_chain__checks__heat_removal_ok__e3aa56b0160f3e08"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_plasma_chain__plasma_chain__checks__heat_removal_ok__e3aa56b0160f3e08"

    def run(self, tolerance_in: float, unmet_in: float) -> ModuleResult[PlasmaChainChecksHeatRemovalOkConstraintOutput]:
        PlasmaChainChecksHeatRemovalOkConstraintInput(tolerance_in=tolerance_in, unmet_in=unmet_in)  # validate every resolved formal
        body = constraint_pred_definition_integrated_heat_electricity__heat_removal_adequate(unmet_in=unmet_in, tolerance_in=tolerance_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlasmaChainChecksHeatRemovalOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"unmet_in": float(unmet_in), "tolerance_in": float(tolerance_in)},
                )
            )
        )
