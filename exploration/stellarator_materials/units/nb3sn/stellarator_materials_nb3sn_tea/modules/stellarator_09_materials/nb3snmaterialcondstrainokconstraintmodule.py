"""Constraint module for stellarator_09_materials__nb3sn_material__cond_strain_ok__404dca1f50a13e3a (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::cond_strain_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__conductor_strain_limit


class Nb3snMaterialCondStrainOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    eps_cond_allow_in: float
    eps_cond: float


class Nb3snMaterialCondStrainOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialCondStrainOkConstraintModule(ModuleBase[Nb3snMaterialCondStrainOkConstraintInput, Nb3snMaterialCondStrainOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__cond_strain_ok__404dca1f50a13e3a"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__cond_strain_ok__404dca1f50a13e3a"

    def run(self, eps_cond_allow_in: float, eps_cond: float) -> ModuleResult[Nb3snMaterialCondStrainOkConstraintOutput]:
        Nb3snMaterialCondStrainOkConstraintInput(eps_cond_allow_in=eps_cond_allow_in, eps_cond=eps_cond)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__conductor_strain_limit(eps_cond=eps_cond, eps_cond_allow_in=eps_cond_allow_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialCondStrainOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"eps_cond": float(eps_cond), "eps_cond_allow_in": float(eps_cond_allow_in)},
                )
            )
        )
