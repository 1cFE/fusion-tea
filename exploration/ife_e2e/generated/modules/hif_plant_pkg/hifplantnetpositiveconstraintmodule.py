"""Constraint module for hif_plant_pkg__hif_plant__net_positive__1d299cceab19c61c (Item 7 / D2/D3/D9).

Effective predicate: ife_plant::'IFE Power Plant'::net_positive in owner instance hif_plant_pkg__hif_plant.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.schemas.constraint_types import ConstraintEvaluation
from ife_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_fusion_cycle__positive_net_generation


class HifPlantNetPositiveConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    net_power: float


class HifPlantNetPositiveConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HifPlantNetPositiveConstraintModule(ModuleBase[HifPlantNetPositiveConstraintInput, HifPlantNetPositiveConstraintOutput]):
    name: str = "hif_plant_pkg__hif_plant__net_positive__1d299cceab19c61c"
    version: str = "v0.1"

    CONSTRAINT_ID = "hif_plant_pkg__hif_plant__net_positive__1d299cceab19c61c"

    def run(self, net_power: float) -> ModuleResult[HifPlantNetPositiveConstraintOutput]:
        HifPlantNetPositiveConstraintInput(net_power=net_power)  # validate every resolved formal
        body = constraint_pred_definition_fusion_cycle__positive_net_generation(net_power=net_power)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HifPlantNetPositiveConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"net_power": float(net_power)},
                )
            )
        )
