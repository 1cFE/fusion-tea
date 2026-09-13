"""Constraint module for stellarator_09__stellaris__net_positive__484521d56c02667a (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::net_positive in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__net_power_positive


class StellarisNetPositiveConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    net_electric: float


class StellarisNetPositiveConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisNetPositiveConstraintModule(ModuleBase[StellarisNetPositiveConstraintInput, StellarisNetPositiveConstraintOutput]):
    name: str = "stellarator_09__stellaris__net_positive__484521d56c02667a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__net_positive__484521d56c02667a"

    def run(self, net_electric: float) -> ModuleResult[StellarisNetPositiveConstraintOutput]:
        StellarisNetPositiveConstraintInput(net_electric=net_electric)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__net_power_positive(net_electric=net_electric)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisNetPositiveConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"net_electric": float(net_electric)},
                )
            )
        )
