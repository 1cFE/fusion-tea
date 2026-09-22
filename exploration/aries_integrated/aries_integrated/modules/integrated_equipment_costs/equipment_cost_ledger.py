"""Equipment_Cost_LedgerModule Module Wrapper

TEAx module for Equipment_Cost_Ledger calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - replacement_reserve_in: replacement_reserve_in parameter
    - direct_in: direct_in parameter
    - consumables_in: consumables_in parameter
    - om_in: om_in parameter
    - source_reactor_gap_in: source_reactor_gap_in parameter
    - replacement_total_in: replacement_total_in parameter
    - indirect_in: indirect_in parameter
    - source_coil_excess_in: source_coil_excess_in parameter
    - availability_in: availability_in parameter
    - tritium_in: tritium_in parameter
    - owner_in: owner_in parameter
    - source_core_excess_in: source_core_excess_in parameter
    - net_power_in: net_power_in parameter
    - contingency_in: contingency_in parameter
    - source_direct_in: source_direct_in parameter
    - currency_year_in: currency_year_in parameter
    - source_inclusive_in: source_inclusive_in parameter
    - import_price_in: import_price_in parameter
    - deuterium_in: deuterium_in parameter

Outputs:
    - annual_operating: annual_operating result
    - source_inclusive: source_inclusive result
    - direct: direct result
    - source_reactor_gap: source_reactor_gap result
    - direct_difference: direct_difference result
    - annual_export_mwh: annual_export_mwh result
    - source_direct: source_direct result
    - source_coil_excess: source_coil_excess result
    - annual_import_cost: annual_import_cost result
    - annual_replacement_reserve: annual_replacement_reserve result
    - source_core_excess: source_core_excess result
    - overnight: overnight result
    - annual_import_mwh: annual_import_mwh result
    - lifetime_replacement: lifetime_replacement result
    - currency_year: currency_year result

SysML Source: root-0/integrated_equipment_costs.sysml:98

SysML Source: root-0/integrated_equipment_costs.sysml:98

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_equipment_costs/equipment_cost_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from aries_integrated.primitives import Float
from aries_integrated.schemas.equipment_cost_ledger_output import Equipment_Cost_LedgerOutput


class Equipment_Cost_LedgerInput(BaseModel):
    """Input model for Equipment_Cost_LedgerModule.

    Attributes:
        replacement_reserve_in: replacement_reserve_in input
        direct_in: direct_in input
        consumables_in: consumables_in input
        om_in: om_in input
        source_reactor_gap_in: source_reactor_gap_in input
        replacement_total_in: replacement_total_in input
        indirect_in: indirect_in input
        source_coil_excess_in: source_coil_excess_in input
        availability_in: availability_in input
        tritium_in: tritium_in input
        owner_in: owner_in input
        source_core_excess_in: source_core_excess_in input
        net_power_in: net_power_in input
        contingency_in: contingency_in input
        source_direct_in: source_direct_in input
        currency_year_in: currency_year_in input
        source_inclusive_in: source_inclusive_in input
        import_price_in: import_price_in input
        deuterium_in: deuterium_in input
    """
    replacement_reserve_in: float = Field(..., description="replacement_reserve_in input")
    direct_in: float = Field(..., description="direct_in input")
    consumables_in: float = Field(..., description="consumables_in input")
    om_in: float = Field(..., description="om_in input")
    source_reactor_gap_in: float = Field(..., description="source_reactor_gap_in input")
    replacement_total_in: float = Field(..., description="replacement_total_in input")
    indirect_in: float = Field(..., description="indirect_in input")
    source_coil_excess_in: float = Field(..., description="source_coil_excess_in input")
    availability_in: float = Field(..., description="availability_in input")
    tritium_in: float = Field(..., description="tritium_in input")
    owner_in: float = Field(..., description="owner_in input")
    source_core_excess_in: float = Field(..., description="source_core_excess_in input")
    net_power_in: float = Field(..., description="net_power_in input")
    contingency_in: float = Field(..., description="contingency_in input")
    source_direct_in: float = Field(..., description="source_direct_in input")
    currency_year_in: float = Field(..., description="currency_year_in input")
    source_inclusive_in: float = Field(..., description="source_inclusive_in input")
    import_price_in: float = Field(..., description="import_price_in input")
    deuterium_in: float = Field(..., description="deuterium_in input")


class Equipment_Cost_LedgerModule(ModuleBase[Equipment_Cost_LedgerInput, Equipment_Cost_LedgerOutput]):
    """TEAx module for Equipment_Cost_Ledger calculation.

*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

Inputs:
    - replacement_reserve_in: replacement_reserve_in parameter
    - direct_in: direct_in parameter
    - consumables_in: consumables_in parameter
    - om_in: om_in parameter
    - source_reactor_gap_in: source_reactor_gap_in parameter
    - replacement_total_in: replacement_total_in parameter
    - indirect_in: indirect_in parameter
    - source_coil_excess_in: source_coil_excess_in parameter
    - availability_in: availability_in parameter
    - tritium_in: tritium_in parameter
    - owner_in: owner_in parameter
    - source_core_excess_in: source_core_excess_in parameter
    - net_power_in: net_power_in parameter
    - contingency_in: contingency_in parameter
    - source_direct_in: source_direct_in parameter
    - currency_year_in: currency_year_in parameter
    - source_inclusive_in: source_inclusive_in parameter
    - import_price_in: import_price_in parameter
    - deuterium_in: deuterium_in parameter

Outputs:
    - annual_operating: annual_operating result
    - source_inclusive: source_inclusive result
    - direct: direct result
    - source_reactor_gap: source_reactor_gap result
    - direct_difference: direct_difference result
    - annual_export_mwh: annual_export_mwh result
    - source_direct: source_direct result
    - source_coil_excess: source_coil_excess result
    - annual_import_cost: annual_import_cost result
    - annual_replacement_reserve: annual_replacement_reserve result
    - source_core_excess: source_core_excess result
    - overnight: overnight result
    - annual_import_mwh: annual_import_mwh result
    - lifetime_replacement: lifetime_replacement result
    - currency_year: currency_year result

SysML Source: root-0/integrated_equipment_costs.sysml:98

    SysML Source: root-0/integrated_equipment_costs.sysml:98

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-090_aries-integrated-equipment-and-costs/design.md. **Ref**: accepted equations, variable-role table and assumptions E1-E10; source-basis.md linked there. **Basis**: [ASSUMED] conditional engineering estimate, USD2004. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See aries_integrated.handwritten.integrated_equipment_costs.equipment_cost_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts annual_operating, source_inclusive, direct, source_reactor_gap, direct_difference, annual_export_mwh, source_direct, source_coil_excess, annual_import_cost, annual_replacement_reserve, source_core_excess, overnight, annual_import_mwh, lifetime_replacement, currency_year fields to separate channels.
    """

    name: str = "Equipment_Cost_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, replacement_reserve_in: float, direct_in: float, consumables_in: float, om_in: float, source_reactor_gap_in: float, replacement_total_in: float, indirect_in: float, source_coil_excess_in: float, availability_in: float, tritium_in: float, owner_in: float, source_core_excess_in: float, net_power_in: float, contingency_in: float, source_direct_in: float, currency_year_in: float, source_inclusive_in: float, import_price_in: float, deuterium_in: float    ) -> Equipment_Cost_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            replacement_reserve_in: replacement_reserve_in input
            direct_in: direct_in input
            consumables_in: consumables_in input
            om_in: om_in input
            source_reactor_gap_in: source_reactor_gap_in input
            replacement_total_in: replacement_total_in input
            indirect_in: indirect_in input
            source_coil_excess_in: source_coil_excess_in input
            availability_in: availability_in input
            tritium_in: tritium_in input
            owner_in: owner_in input
            source_core_excess_in: source_core_excess_in input
            net_power_in: net_power_in input
            contingency_in: contingency_in input
            source_direct_in: source_direct_in input
            currency_year_in: currency_year_in input
            source_inclusive_in: source_inclusive_in input
            import_price_in: import_price_in input
            deuterium_in: deuterium_in input

        Returns:
            Validated input model
        """
        return Equipment_Cost_LedgerInput(replacement_reserve_in=replacement_reserve_in, direct_in=direct_in, consumables_in=consumables_in, om_in=om_in, source_reactor_gap_in=source_reactor_gap_in, replacement_total_in=replacement_total_in, indirect_in=indirect_in, source_coil_excess_in=source_coil_excess_in, availability_in=availability_in, tritium_in=tritium_in, owner_in=owner_in, source_core_excess_in=source_core_excess_in, net_power_in=net_power_in, contingency_in=contingency_in, source_direct_in=source_direct_in, currency_year_in=currency_year_in, source_inclusive_in=source_inclusive_in, import_price_in=import_price_in, deuterium_in=deuterium_in)

    def run(
        self, replacement_reserve_in: float, direct_in: float, consumables_in: float, om_in: float, source_reactor_gap_in: float, replacement_total_in: float, indirect_in: float, source_coil_excess_in: float, availability_in: float, tritium_in: float, owner_in: float, source_core_excess_in: float, net_power_in: float, contingency_in: float, source_direct_in: float, currency_year_in: float, source_inclusive_in: float, import_price_in: float, deuterium_in: float    ) -> ModuleResult[Equipment_Cost_LedgerOutput]:
        """Execute calculation.

        Args:
            replacement_reserve_in: replacement_reserve_in input
            direct_in: direct_in input
            consumables_in: consumables_in input
            om_in: om_in input
            source_reactor_gap_in: source_reactor_gap_in input
            replacement_total_in: replacement_total_in input
            indirect_in: indirect_in input
            source_coil_excess_in: source_coil_excess_in input
            availability_in: availability_in input
            tritium_in: tritium_in input
            owner_in: owner_in input
            source_core_excess_in: source_core_excess_in input
            net_power_in: net_power_in input
            contingency_in: contingency_in input
            source_direct_in: source_direct_in input
            currency_year_in: currency_year_in input
            source_inclusive_in: source_inclusive_in input
            import_price_in: import_price_in input
            deuterium_in: deuterium_in input

        Returns:
            Module result with Equipment_Cost_LedgerOutput (annual_operating, source_inclusive, direct, source_reactor_gap, direct_difference, annual_export_mwh, source_direct, source_coil_excess, annual_import_cost, annual_replacement_reserve, source_core_excess, overnight, annual_import_mwh, lifetime_replacement, currency_year)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(replacement_reserve_in, direct_in, consumables_in, om_in, source_reactor_gap_in, replacement_total_in, indirect_in, source_coil_excess_in, availability_in, tritium_in, owner_in, source_core_excess_in, net_power_in, contingency_in, source_direct_in, currency_year_in, source_inclusive_in, import_price_in, deuterium_in)

        # Import handwritten implementation
        from aries_integrated.handwritten.integrated_equipment_costs.equipment_cost_ledger_impl import (
            run_equipment_cost_ledger,
        )

        # Execute implementation - returns tuple of values
        annual_operating, source_inclusive, direct, source_reactor_gap, direct_difference, annual_export_mwh, source_direct, source_coil_excess, annual_import_cost, annual_replacement_reserve, source_core_excess, overnight, annual_import_mwh, lifetime_replacement, currency_year = run_equipment_cost_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Equipment_Cost_LedgerOutput(
                annual_operating=annual_operating,
                source_inclusive=source_inclusive,
                direct=direct,
                source_reactor_gap=source_reactor_gap,
                direct_difference=direct_difference,
                annual_export_mwh=annual_export_mwh,
                source_direct=source_direct,
                source_coil_excess=source_coil_excess,
                annual_import_cost=annual_import_cost,
                annual_replacement_reserve=annual_replacement_reserve,
                source_core_excess=source_core_excess,
                overnight=overnight,
                annual_import_mwh=annual_import_mwh,
                lifetime_replacement=lifetime_replacement,
                currency_year=currency_year,
            )
        )
