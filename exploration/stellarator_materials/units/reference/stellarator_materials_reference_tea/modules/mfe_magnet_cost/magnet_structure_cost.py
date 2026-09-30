"""Magnet_Structure_CostModule Module Wrapper

TEAx module for Magnet_Structure_Cost calculation.

Electromagnetic support cost, exclusive total or legacy casing basis.
cost=(legacy_casing_fraction*n_coils*m_casing+m_support)*steel_price*f_steel_fab.
The casing output remains an inherited floor diagnostic in total-support mode.
Native domain: every input finite and nonnegative; legacy_casing_fraction in [0,1]; finite nonnegative outputs with no positive product underflow. Historical multiplication order is preserved. effective_all_in_rate=steel_price*f_steel_fab exposes one assumed all-in rate; the factors do not establish measured material/fabrication subtotals.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D1-D2; T-005_structure_basis.md.
*Basis**: inherited 6 dollars/kg times 3 = 18 dollars/kg all-in assumption; unknown price year and manufacturing qualification, no demonstrated duplicate removed or sourced casing/intercoil split.
*Last Updated**: 2026-09-15

Inputs:
    - n_coils: n_coils parameter
    - legacy_casing_fraction: legacy_casing_fraction parameter
    - m_casing: m_casing parameter
    - steel_price: steel_price parameter
    - f_steel_fab: f_steel_fab parameter
    - m_support: m_support parameter

Outputs:
    - cost: cost result
    - effective_all_in_rate: effective_all_in_rate result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:157

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:157

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_magnet_cost/magnet_structure_cost_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_reference_tea.primitives import Float
from stellarator_materials_reference_tea.schemas.magnet_structure_cost_output import Magnet_Structure_CostOutput


class Magnet_Structure_CostInput(BaseModel):
    """Input model for Magnet_Structure_CostModule.

    Attributes:
        n_coils: n_coils input
        legacy_casing_fraction: legacy_casing_fraction input
        m_casing: m_casing input
        steel_price: steel_price input
        f_steel_fab: f_steel_fab input
        m_support: m_support input
    """
    n_coils: float = Field(..., description="n_coils input")
    legacy_casing_fraction: float = Field(..., description="legacy_casing_fraction input")
    m_casing: float = Field(..., description="m_casing input")
    steel_price: float = Field(..., description="steel_price input")
    f_steel_fab: float = Field(..., description="f_steel_fab input")
    m_support: float = Field(..., description="m_support input")


class Magnet_Structure_CostModule(ModuleBase[Magnet_Structure_CostInput, Magnet_Structure_CostOutput]):
    """TEAx module for Magnet_Structure_Cost calculation.

Electromagnetic support cost, exclusive total or legacy casing basis.
cost=(legacy_casing_fraction*n_coils*m_casing+m_support)*steel_price*f_steel_fab.
The casing output remains an inherited floor diagnostic in total-support mode.
Native domain: every input finite and nonnegative; legacy_casing_fraction in [0,1]; finite nonnegative outputs with no positive product underflow. Historical multiplication order is preserved. effective_all_in_rate=steel_price*f_steel_fab exposes one assumed all-in rate; the factors do not establish measured material/fabrication subtotals.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D1-D2; T-005_structure_basis.md.
*Basis**: inherited 6 dollars/kg times 3 = 18 dollars/kg all-in assumption; unknown price year and manufacturing qualification, no demonstrated duplicate removed or sourced casing/intercoil split.
*Last Updated**: 2026-09-15

Inputs:
    - n_coils: n_coils parameter
    - legacy_casing_fraction: legacy_casing_fraction parameter
    - m_casing: m_casing parameter
    - steel_price: steel_price parameter
    - f_steel_fab: f_steel_fab parameter
    - m_support: m_support parameter

Outputs:
    - cost: cost result
    - effective_all_in_rate: effective_all_in_rate result

SysML Source: root-0/analyses/mfe_magnet_cost.sysml:157

    SysML Source: root-0/analyses/mfe_magnet_cost.sysml:157

    Calculation Specification:
        m_support = 0.0
        legacy_casing_fraction = 1.0
        effective_all_in_rate = steel_price * f_steel_fab
        cost = (legacy_casing_fraction * n_coils * m_casing + m_support) * steel_price * f_steel_fab
        
Documentation:
Electromagnetic support cost, exclusive total or legacy casing basis.
cost=(legacy_casing_fraction*n_coils*m_casing+m_support)*steel_price*f_steel_fab.
The casing output remains an inherited floor diagnostic in total-support mode.
Native domain: every input finite and nonnegative; legacy_casing_fraction in [0,1]; finite nonnegative outputs with no positive product underflow. Historical multiplication order is preserved. effective_all_in_rate=steel_price*f_steel_fab exposes one assumed all-in rate; the factors do not establish measured material/fabrication subtotals.
*Source**: work/active/WI-059_coil-thermal-and-total-support-inventory/design.md
*Reference**: D1-D2; T-005_structure_basis.md.
*Basis**: inherited 6 dollars/kg times 3 = 18 dollars/kg all-in assumption; unknown price year and manufacturing qualification, no demonstrated duplicate removed or sourced casing/intercoil split.
*Last Updated**: 2026-09-15

    IMPLEMENTATION: See stellarator_materials_reference_tea.handwritten.mfe_magnet_cost.magnet_structure_cost_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts cost, effective_all_in_rate fields to separate channels.
    """

    name: str = "Magnet_Structure_CostModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, n_coils: float, legacy_casing_fraction: float, m_casing: float, steel_price: float, f_steel_fab: float, m_support: float    ) -> Magnet_Structure_CostInput:
        """Validate inputs and fill defaults.

        Args:
            n_coils: n_coils input
            legacy_casing_fraction: legacy_casing_fraction input
            m_casing: m_casing input
            steel_price: steel_price input
            f_steel_fab: f_steel_fab input
            m_support: m_support input

        Returns:
            Validated input model
        """
        return Magnet_Structure_CostInput(n_coils=n_coils, legacy_casing_fraction=legacy_casing_fraction, m_casing=m_casing, steel_price=steel_price, f_steel_fab=f_steel_fab, m_support=m_support)

    def run(
        self, n_coils: float, legacy_casing_fraction: float, m_casing: float, steel_price: float, f_steel_fab: float, m_support: float    ) -> ModuleResult[Magnet_Structure_CostOutput]:
        """Execute calculation.

        Args:
            n_coils: n_coils input
            legacy_casing_fraction: legacy_casing_fraction input
            m_casing: m_casing input
            steel_price: steel_price input
            f_steel_fab: f_steel_fab input
            m_support: m_support input

        Returns:
            Module result with Magnet_Structure_CostOutput (cost, effective_all_in_rate)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(n_coils, legacy_casing_fraction, m_casing, steel_price, f_steel_fab, m_support)

        # Import handwritten implementation
        from stellarator_materials_reference_tea.handwritten.mfe_magnet_cost.magnet_structure_cost_impl import (
            run_magnet_structure_cost,
        )

        # Execute implementation - returns tuple of values
        cost, effective_all_in_rate = run_magnet_structure_cost(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Magnet_Structure_CostOutput(
                cost=cost,
                effective_all_in_rate=effective_all_in_rate,
            )
        )
