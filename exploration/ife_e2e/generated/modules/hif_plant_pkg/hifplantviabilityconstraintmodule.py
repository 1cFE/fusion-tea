"""Constraint module for hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b (Item 7 / D2/D3/D9).

Effective predicate: ife_plant::'IFE Power Plant'::viability in owner instance hif_plant_pkg__hif_plant.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from ife_tea.schemas.constraint_types import ConstraintEvaluation
from ife_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_fusion_cycle__viability_threshold


class HifPlantViabilityConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    eta: float
    gain: float
    threshold: float


class HifPlantViabilityConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class HifPlantViabilityConstraintModule(ModuleBase[HifPlantViabilityConstraintInput, HifPlantViabilityConstraintOutput]):
    name: str = "hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b"
    version: str = "v0.1"

    CONSTRAINT_ID = "hif_plant_pkg__hif_plant__viability__81ddf10fb1d1749b"

    def run(self, eta: float, gain: float, threshold: float) -> ModuleResult[HifPlantViabilityConstraintOutput]:
        HifPlantViabilityConstraintInput(eta=eta, gain=gain, threshold=threshold)  # validate every resolved formal
        body = constraint_pred_definition_fusion_cycle__viability_threshold(eta=eta, gain=gain, threshold=threshold)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=HifPlantViabilityConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"eta": float(eta), "gain": float(gain), "threshold": float(threshold)},
                )
            )
        )
