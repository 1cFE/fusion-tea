"""Constraint module for stellarator_09_materials__nb3sn_material__peak_field_ok__1fcd44510d5ceb9a (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::peak_field_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__conductor_peak_field_limit


class Nb3snMaterialPeakFieldOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    B_max_in: float
    B_peak: float


class Nb3snMaterialPeakFieldOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialPeakFieldOkConstraintModule(ModuleBase[Nb3snMaterialPeakFieldOkConstraintInput, Nb3snMaterialPeakFieldOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__peak_field_ok__1fcd44510d5ceb9a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__peak_field_ok__1fcd44510d5ceb9a"

    def run(self, B_max_in: float, B_peak: float) -> ModuleResult[Nb3snMaterialPeakFieldOkConstraintOutput]:
        Nb3snMaterialPeakFieldOkConstraintInput(B_max_in=B_max_in, B_peak=B_peak)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__conductor_peak_field_limit(B_peak=B_peak, B_max_in=B_max_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialPeakFieldOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"B_peak": float(B_peak), "B_max_in": float(B_max_in)},
                )
            )
        )
