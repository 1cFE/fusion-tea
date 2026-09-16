"""Constraint module for stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::recirc_ok in owner instance stellarator_09__stellaris.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__economic_recirculating_threshold


class StellarisRecircOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    rec_frac: float
    threshold: float


class StellarisRecircOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class StellarisRecircOkConstraintModule(ModuleBase[StellarisRecircOkConstraintInput, StellarisRecircOkConstraintOutput]):
    name: str = "stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b"

    def run(self, rec_frac: float, threshold: float) -> ModuleResult[StellarisRecircOkConstraintOutput]:
        StellarisRecircOkConstraintInput(rec_frac=rec_frac, threshold=threshold)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__economic_recirculating_threshold(rec_frac=rec_frac, threshold=threshold)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=StellarisRecircOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"rec_frac": float(rec_frac), "threshold": float(threshold)},
                )
            )
        )
