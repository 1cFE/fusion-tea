"""Constraint module for stellarator_09_materials__nb3sn_material__reference_conductor_current_ok__ed9bbbfb7399171f (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::nb3sn_material::reference_conductor_current_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_conductor_current__reference_conductor_current_margin


class Nb3snMaterialReferenceConductorCurrentOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_fraction_in: float


class Nb3snMaterialReferenceConductorCurrentOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialReferenceConductorCurrentOkConstraintModule(ModuleBase[Nb3snMaterialReferenceConductorCurrentOkConstraintInput, Nb3snMaterialReferenceConductorCurrentOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__reference_conductor_current_ok__ed9bbbfb7399171f"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__reference_conductor_current_ok__ed9bbbfb7399171f"

    def run(self, margin_fraction_in: float) -> ModuleResult[Nb3snMaterialReferenceConductorCurrentOkConstraintOutput]:
        Nb3snMaterialReferenceConductorCurrentOkConstraintInput(margin_fraction_in=margin_fraction_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_conductor_current__reference_conductor_current_margin(margin_fraction_in=margin_fraction_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialReferenceConductorCurrentOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"margin_fraction_in": float(margin_fraction_in)},
                )
            )
        )
