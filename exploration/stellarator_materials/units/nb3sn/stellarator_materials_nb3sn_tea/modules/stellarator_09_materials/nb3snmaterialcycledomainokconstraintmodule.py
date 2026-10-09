"""Constraint module for stellarator_09_materials__nb3sn_material__cycle_domain_ok__76acde2a26a78109 (Item 7 / D2/D3/D9).

Effective predicate: mfe_plant::'MFE Power Plant'::cycle_domain_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__cycle_fit_domain


class Nb3snMaterialCycleDomainOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    domain_product_in: float


class Nb3snMaterialCycleDomainOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialCycleDomainOkConstraintModule(ModuleBase[Nb3snMaterialCycleDomainOkConstraintInput, Nb3snMaterialCycleDomainOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__cycle_domain_ok__76acde2a26a78109"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__cycle_domain_ok__76acde2a26a78109"

    def run(self, domain_product_in: float) -> ModuleResult[Nb3snMaterialCycleDomainOkConstraintOutput]:
        Nb3snMaterialCycleDomainOkConstraintInput(domain_product_in=domain_product_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__cycle_fit_domain(domain_product_in=domain_product_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialCycleDomainOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"domain_product_in": float(domain_product_in)},
                )
            )
        )
