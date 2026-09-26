"""Constraint module for combinations_plasma_chain__plasma_chain__checks__net_positive__1ca673e570772897 (Item 7 / D2/D3/D9).

Effective predicate: combinations_plasma_chain::plasma_chain::checks::net_positive in owner instance combinations_plasma_chain__plasma_chain__checks.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.schemas.constraint_types import ConstraintEvaluation
from combinations_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__net_power_positive


class PlasmaChainChecksNetPositiveConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    net_electric: float


class PlasmaChainChecksNetPositiveConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class PlasmaChainChecksNetPositiveConstraintModule(ModuleBase[PlasmaChainChecksNetPositiveConstraintInput, PlasmaChainChecksNetPositiveConstraintOutput]):
    name: str = "combinations_plasma_chain__plasma_chain__checks__net_positive__1ca673e570772897"
    version: str = "v0.1"

    CONSTRAINT_ID = "combinations_plasma_chain__plasma_chain__checks__net_positive__1ca673e570772897"

    def run(self, net_electric: float) -> ModuleResult[PlasmaChainChecksNetPositiveConstraintOutput]:
        PlasmaChainChecksNetPositiveConstraintInput(net_electric=net_electric)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__net_power_positive(net_electric=net_electric)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=PlasmaChainChecksNetPositiveConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"net_electric": float(net_electric)},
                )
            )
        )
