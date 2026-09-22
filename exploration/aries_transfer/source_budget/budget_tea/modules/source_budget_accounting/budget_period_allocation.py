"""Budget_Period_AllocationModule Module Wrapper

TEAx module for Budget_Period_Allocation calculation.

Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. period=selected_period for mode0; period=selected_period/availability for mode1. annual_capital=capital/period; annual_replacement=replacement/period; partial_annual_cost=annual_capital+annual_replacement; annual_energy=8760*net_power*availability; lifetime_energy=annual_energy*period. Guarded pass-through net_power/availability; constant module_count1 and excluded_annual_channel0 are nonpublic outputs. Dollars, MW, years, MWh; mode selects explicit comparison convention, not inferred reliability. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

Inputs:
    - period_mode_in: period_mode_in parameter
    - availability_in: availability_in parameter
    - capital_budget_in: capital_budget_in parameter
    - replacement_budget_in: replacement_budget_in parameter
    - net_power_in: net_power_in parameter
    - selected_period_in: selected_period_in parameter

Outputs:
    - annual_replacement: annual_replacement result
    - module_count: module_count result
    - validated_availability: validated_availability result
    - annual_energy: annual_energy result
    - lifetime_energy: lifetime_energy result
    - excluded_annual_channel: excluded_annual_channel result
    - comparison_period: comparison_period result
    - partial_annual_cost: partial_annual_cost result
    - annual_capital: annual_capital result
    - validated_net_power: validated_net_power result

SysML Source: root-0/source_budget_accounting.sysml:18

SysML Source: root-0/source_budget_accounting.sysml:18

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/source_budget_accounting/budget_period_allocation_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from budget_tea.primitives import Float
from budget_tea.schemas.budget_period_allocation_output import Budget_Period_AllocationOutput


class Budget_Period_AllocationInput(BaseModel):
    """Input model for Budget_Period_AllocationModule.

    Attributes:
        period_mode_in: period_mode_in input
        availability_in: availability_in input
        capital_budget_in: capital_budget_in input
        replacement_budget_in: replacement_budget_in input
        net_power_in: net_power_in input
        selected_period_in: selected_period_in input
    """
    period_mode_in: float = Field(..., description="period_mode_in input")
    availability_in: float = Field(..., description="availability_in input")
    capital_budget_in: float = Field(..., description="capital_budget_in input")
    replacement_budget_in: float = Field(..., description="replacement_budget_in input")
    net_power_in: float = Field(..., description="net_power_in input")
    selected_period_in: float = Field(..., description="selected_period_in input")


class Budget_Period_AllocationModule(ModuleBase[Budget_Period_AllocationInput, Budget_Period_AllocationOutput]):
    """TEAx module for Budget_Period_Allocation calculation.

Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. period=selected_period for mode0; period=selected_period/availability for mode1. annual_capital=capital/period; annual_replacement=replacement/period; partial_annual_cost=annual_capital+annual_replacement; annual_energy=8760*net_power*availability; lifetime_energy=annual_energy*period. Guarded pass-through net_power/availability; constant module_count1 and excluded_annual_channel0 are nonpublic outputs. Dollars, MW, years, MWh; mode selects explicit comparison convention, not inferred reliability. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

Inputs:
    - period_mode_in: period_mode_in parameter
    - availability_in: availability_in parameter
    - capital_budget_in: capital_budget_in parameter
    - replacement_budget_in: replacement_budget_in parameter
    - net_power_in: net_power_in parameter
    - selected_period_in: selected_period_in parameter

Outputs:
    - annual_replacement: annual_replacement result
    - module_count: module_count result
    - validated_availability: validated_availability result
    - annual_energy: annual_energy result
    - lifetime_energy: lifetime_energy result
    - excluded_annual_channel: excluded_annual_channel result
    - comparison_period: comparison_period result
    - partial_annual_cost: partial_annual_cost result
    - annual_capital: annual_capital result
    - validated_net_power: validated_net_power result

SysML Source: root-0/source_budget_accounting.sysml:18

    SysML Source: root-0/source_budget_accounting.sysml:18

    Calculation Specification:
        See documentation:
Source: work/active/WI-088_aries-source-budget-cost-contribution/spec.md. Ref: accepted financial scope and Lyon Eq7/account mapping. Basis: AGENT generic disjoint-budget accounting and explicit period convention. period=selected_period for mode0; period=selected_period/availability for mode1. annual_capital=capital/period; annual_replacement=replacement/period; partial_annual_cost=annual_capital+annual_replacement; annual_energy=8760*net_power*availability; lifetime_energy=annual_energy*period. Guarded pass-through net_power/availability; constant module_count1 and excluded_annual_channel0 are nonpublic outputs. Dollars, MW, years, MWh; mode selects explicit comparison convention, not inferred reliability. Native guard rejects nonfinite/negative budgets, nonpositive multiplier/period/power, mode outside0/1, availability outside(0,1], overflow and zero energy. Last Updated: 2026-09-21.

    IMPLEMENTATION: See budget_tea.handwritten.source_budget_accounting.budget_period_allocation_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts annual_replacement, module_count, validated_availability, annual_energy, lifetime_energy, excluded_annual_channel, comparison_period, partial_annual_cost, annual_capital, validated_net_power fields to separate channels.
    """

    name: str = "Budget_Period_AllocationModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, period_mode_in: float, availability_in: float, capital_budget_in: float, replacement_budget_in: float, net_power_in: float, selected_period_in: float    ) -> Budget_Period_AllocationInput:
        """Validate inputs and fill defaults.

        Args:
            period_mode_in: period_mode_in input
            availability_in: availability_in input
            capital_budget_in: capital_budget_in input
            replacement_budget_in: replacement_budget_in input
            net_power_in: net_power_in input
            selected_period_in: selected_period_in input

        Returns:
            Validated input model
        """
        return Budget_Period_AllocationInput(period_mode_in=period_mode_in, availability_in=availability_in, capital_budget_in=capital_budget_in, replacement_budget_in=replacement_budget_in, net_power_in=net_power_in, selected_period_in=selected_period_in)

    def run(
        self, period_mode_in: float, availability_in: float, capital_budget_in: float, replacement_budget_in: float, net_power_in: float, selected_period_in: float    ) -> ModuleResult[Budget_Period_AllocationOutput]:
        """Execute calculation.

        Args:
            period_mode_in: period_mode_in input
            availability_in: availability_in input
            capital_budget_in: capital_budget_in input
            replacement_budget_in: replacement_budget_in input
            net_power_in: net_power_in input
            selected_period_in: selected_period_in input

        Returns:
            Module result with Budget_Period_AllocationOutput (annual_replacement, module_count, validated_availability, annual_energy, lifetime_energy, excluded_annual_channel, comparison_period, partial_annual_cost, annual_capital, validated_net_power)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(period_mode_in, availability_in, capital_budget_in, replacement_budget_in, net_power_in, selected_period_in)

        # Import handwritten implementation
        from budget_tea.handwritten.source_budget_accounting.budget_period_allocation_impl import (
            run_budget_period_allocation,
        )

        # Execute implementation - returns tuple of values
        annual_replacement, module_count, validated_availability, annual_energy, lifetime_energy, excluded_annual_channel, comparison_period, partial_annual_cost, annual_capital, validated_net_power = run_budget_period_allocation(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Budget_Period_AllocationOutput(
                annual_replacement=annual_replacement,
                module_count=module_count,
                validated_availability=validated_availability,
                annual_energy=annual_energy,
                lifetime_energy=lifetime_energy,
                excluded_annual_channel=excluded_annual_channel,
                comparison_period=comparison_period,
                partial_annual_cost=partial_annual_cost,
                annual_capital=annual_capital,
                validated_net_power=validated_net_power,
            )
        )
