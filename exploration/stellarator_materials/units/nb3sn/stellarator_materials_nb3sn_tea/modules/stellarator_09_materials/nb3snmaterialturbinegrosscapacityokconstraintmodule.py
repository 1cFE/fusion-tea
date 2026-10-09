"""Constraint module for stellarator_09_materials__nb3sn_material__turbine_gross_capacity_ok__946403aa70c1c824 (Item 7 / D2/D3/D9).

Effective predicate: stellarator_09_materials::nb3sn_material::turbine_gross_capacity_ok in owner instance stellarator_09_materials__nb3sn_material.
Three-valued (Kleene) semantics. A verdict against the assertion does not itself raise (INV-3).
"""

from pydantic import BaseModel
from simkit.config.schema import MultiOutput
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.schemas.constraint_types import ConstraintEvaluation
from stellarator_materials_nb3sn_tea.modules.constraints.predicates import _finalize_assertion, constraint_pred_definition_mfe_viability__offered_equipment_capacity


class Nb3snMaterialTurbineGrossCapacityOkConstraintInput(BaseModel):
    """Exact input schema: one field per resolved formal."""
    margin_in: float
    defined_in: float


class Nb3snMaterialTurbineGrossCapacityOkConstraintOutput(MultiOutput):
    evaluation: ConstraintEvaluation


class Nb3snMaterialTurbineGrossCapacityOkConstraintModule(ModuleBase[Nb3snMaterialTurbineGrossCapacityOkConstraintInput, Nb3snMaterialTurbineGrossCapacityOkConstraintOutput]):
    name: str = "stellarator_09_materials__nb3sn_material__turbine_gross_capacity_ok__946403aa70c1c824"
    version: str = "v0.1"

    CONSTRAINT_ID = "stellarator_09_materials__nb3sn_material__turbine_gross_capacity_ok__946403aa70c1c824"

    def run(self, margin_in: float, defined_in: float) -> ModuleResult[Nb3snMaterialTurbineGrossCapacityOkConstraintOutput]:
        Nb3snMaterialTurbineGrossCapacityOkConstraintInput(margin_in=margin_in, defined_in=defined_in)  # validate every resolved formal
        body = constraint_pred_definition_mfe_viability__offered_equipment_capacity(defined_in=defined_in, margin_in=margin_in)
        verdict = _finalize_assertion(
            body,
            is_negated=False,
            expected_value=True,
        )
        return ModuleResult(
            data=Nb3snMaterialTurbineGrossCapacityOkConstraintOutput(
                evaluation=ConstraintEvaluation(
                    constraint_id=self.CONSTRAINT_ID,
                    actual_value=verdict.actual_value,
                    status=verdict.status,
                    margin=verdict.margin,
                    observed={"defined_in": float(defined_in), "margin_in": float(margin_in)},
                )
            )
        )
