"""Cold_Load_SumModule Module Wrapper

TEAx module for Cold_Load_Sum calculation.

Assemble cold MW once; uplift only the legacy nuclear/fixed and
explicit structure-nuclear terms, never the enumerated inventory.
Native completion requires finite positive rho_structure and finite
nonnegative q_nuc_structure, m_support and q_inventory_cold.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D5. **Basis**: heat balance, W to MW conversion.
*Last Updated**: 2026-09-15

Inputs:
    - p_fixed: p_fixed parameter
    - f_uplift: f_uplift parameter
    - rho_structure: rho_structure parameter
    - q_inventory_cold: q_inventory_cold parameter
    - q_nuc: q_nuc parameter
    - q_nuc_structure: q_nuc_structure parameter
    - m_support: m_support parameter
    - vol_cold: vol_cold parameter

Outputs:
    - q_structure_nuclear: q_structure_nuclear result
    - p_cold: p_cold result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:62

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:62

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_cryo_inventory/cold_load_sum_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.cold_load_sum_output import Cold_Load_SumOutput


class Cold_Load_SumInput(BaseModel):
    """Input model for Cold_Load_SumModule.

    Attributes:
        p_fixed: p_fixed input
        f_uplift: f_uplift input
        rho_structure: rho_structure input
        q_inventory_cold: q_inventory_cold input
        q_nuc: q_nuc input
        q_nuc_structure: q_nuc_structure input
        m_support: m_support input
        vol_cold: vol_cold input
    """
    p_fixed: float = Field(..., description="p_fixed input")
    f_uplift: float = Field(..., description="f_uplift input")
    rho_structure: float = Field(..., description="rho_structure input")
    q_inventory_cold: float = Field(..., description="q_inventory_cold input")
    q_nuc: float = Field(..., description="q_nuc input")
    q_nuc_structure: float = Field(..., description="q_nuc_structure input")
    m_support: float = Field(..., description="m_support input")
    vol_cold: float = Field(..., description="vol_cold input")


class Cold_Load_SumModule(ModuleBase[Cold_Load_SumInput, Cold_Load_SumOutput]):
    """TEAx module for Cold_Load_Sum calculation.

Assemble cold MW once; uplift only the legacy nuclear/fixed and
explicit structure-nuclear terms, never the enumerated inventory.
Native completion requires finite positive rho_structure and finite
nonnegative q_nuc_structure, m_support and q_inventory_cold.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D5. **Basis**: heat balance, W to MW conversion.
*Last Updated**: 2026-09-15

Inputs:
    - p_fixed: p_fixed parameter
    - f_uplift: f_uplift parameter
    - rho_structure: rho_structure parameter
    - q_inventory_cold: q_inventory_cold parameter
    - q_nuc: q_nuc parameter
    - q_nuc_structure: q_nuc_structure parameter
    - m_support: m_support parameter
    - vol_cold: vol_cold parameter

Outputs:
    - q_structure_nuclear: q_structure_nuclear result
    - p_cold: p_cold result

SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:62

    SysML Source: root-0/analyses/mfe_cryo_inventory.sysml:62

    Calculation Specification:
        q_nuc = 0.0
        vol_cold = 0.0
        p_fixed = 0.0
        f_uplift = 1.0
        q_nuc_structure = 0.0
        m_support = 0.0
        rho_structure = 1.0
        q_inventory_cold = 0.0
        q_structure_nuclear = q_nuc_structure * m_support / rho_structure
        p_cold = f_uplift * (q_nuc * vol_cold * 1e-06 + p_fixed + q_structure_nuclear * 1e-06) + q_inventory_cold * 1e-06
        
Documentation:
Assemble cold MW once; uplift only the legacy nuclear/fixed and
explicit structure-nuclear terms, never the enumerated inventory.
Native completion requires finite positive rho_structure and finite
nonnegative q_nuc_structure, m_support and q_inventory_cold.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D5. **Basis**: heat balance, W to MW conversion.
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_cryo_inventory.cold_load_sum_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts q_structure_nuclear, p_cold fields to separate channels.
    """

    name: str = "Cold_Load_SumModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, p_fixed: float, f_uplift: float, rho_structure: float, q_inventory_cold: float, q_nuc: float, q_nuc_structure: float, m_support: float, vol_cold: float    ) -> Cold_Load_SumInput:
        """Validate inputs and fill defaults.

        Args:
            p_fixed: p_fixed input
            f_uplift: f_uplift input
            rho_structure: rho_structure input
            q_inventory_cold: q_inventory_cold input
            q_nuc: q_nuc input
            q_nuc_structure: q_nuc_structure input
            m_support: m_support input
            vol_cold: vol_cold input

        Returns:
            Validated input model
        """
        return Cold_Load_SumInput(p_fixed=p_fixed, f_uplift=f_uplift, rho_structure=rho_structure, q_inventory_cold=q_inventory_cold, q_nuc=q_nuc, q_nuc_structure=q_nuc_structure, m_support=m_support, vol_cold=vol_cold)

    def run(
        self, p_fixed: float, f_uplift: float, rho_structure: float, q_inventory_cold: float, q_nuc: float, q_nuc_structure: float, m_support: float, vol_cold: float    ) -> ModuleResult[Cold_Load_SumOutput]:
        """Execute calculation.

        Args:
            p_fixed: p_fixed input
            f_uplift: f_uplift input
            rho_structure: rho_structure input
            q_inventory_cold: q_inventory_cold input
            q_nuc: q_nuc input
            q_nuc_structure: q_nuc_structure input
            m_support: m_support input
            vol_cold: vol_cold input

        Returns:
            Module result with Cold_Load_SumOutput (q_structure_nuclear, p_cold)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(p_fixed, f_uplift, rho_structure, q_inventory_cold, q_nuc, q_nuc_structure, m_support, vol_cold)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_cryo_inventory.cold_load_sum_impl import (
            run_cold_load_sum,
        )

        # Execute implementation - returns tuple of values
        q_structure_nuclear, p_cold = run_cold_load_sum(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cold_Load_SumOutput(
                q_structure_nuclear=q_structure_nuclear,
                p_cold=p_cold,
            )
        )
