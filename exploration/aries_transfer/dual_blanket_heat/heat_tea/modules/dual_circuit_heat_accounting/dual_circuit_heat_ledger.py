"""Dual_Circuit_Heat_LedgerModule Module Wrapper

TEAx module for Dual_Circuit_Heat_Ledger calculation.

delivered_total = duty_1_in + duty_2_in; deposited_total = deposition_1_in + deposition_2_in; friction_total = friction_1_in + friction_2_in; energy_residual = delivered_total - deposited_total - friction_total. All quantities MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: two-branch control boundary with internal exchange canceling once. Basis: generic energy accounting; native completion rejects nonfinite/negative supplied heat and nonfinite outputs, but preserves signed residuals without clamping or forcing closure. A nonzero residual is a diagnostic, not an equipment adequacy claim. Independent source comparison belongs in the analysis record, not this physical producer. Last Updated: 2026-09-21.

Inputs:
    - deposition_1_in: deposition_1_in parameter
    - friction_1_in: friction_1_in parameter
    - duty_2_in: duty_2_in parameter
    - duty_1_in: duty_1_in parameter
    - friction_2_in: friction_2_in parameter
    - deposition_2_in: deposition_2_in parameter

Outputs:
    - friction_total: friction_total result
    - deposited_total: deposited_total result
    - delivered_total: delivered_total result
    - energy_residual: energy_residual result

SysML Source: root-0/dual_circuit_heat_accounting.sysml:13

SysML Source: root-0/dual_circuit_heat_accounting.sysml:13

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/dual_circuit_heat_accounting/dual_circuit_heat_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from heat_tea.primitives import Float
from heat_tea.schemas.dual_circuit_heat_ledger_output import Dual_Circuit_Heat_LedgerOutput


class Dual_Circuit_Heat_LedgerInput(BaseModel):
    """Input model for Dual_Circuit_Heat_LedgerModule.

    Attributes:
        deposition_1_in: deposition_1_in input
        friction_1_in: friction_1_in input
        duty_2_in: duty_2_in input
        duty_1_in: duty_1_in input
        friction_2_in: friction_2_in input
        deposition_2_in: deposition_2_in input
    """
    deposition_1_in: float = Field(..., description="deposition_1_in input")
    friction_1_in: float = Field(..., description="friction_1_in input")
    duty_2_in: float = Field(..., description="duty_2_in input")
    duty_1_in: float = Field(..., description="duty_1_in input")
    friction_2_in: float = Field(..., description="friction_2_in input")
    deposition_2_in: float = Field(..., description="deposition_2_in input")


class Dual_Circuit_Heat_LedgerModule(ModuleBase[Dual_Circuit_Heat_LedgerInput, Dual_Circuit_Heat_LedgerOutput]):
    """TEAx module for Dual_Circuit_Heat_Ledger calculation.

delivered_total = duty_1_in + duty_2_in; deposited_total = deposition_1_in + deposition_2_in; friction_total = friction_1_in + friction_2_in; energy_residual = delivered_total - deposited_total - friction_total. All quantities MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: two-branch control boundary with internal exchange canceling once. Basis: generic energy accounting; native completion rejects nonfinite/negative supplied heat and nonfinite outputs, but preserves signed residuals without clamping or forcing closure. A nonzero residual is a diagnostic, not an equipment adequacy claim. Independent source comparison belongs in the analysis record, not this physical producer. Last Updated: 2026-09-21.

Inputs:
    - deposition_1_in: deposition_1_in parameter
    - friction_1_in: friction_1_in parameter
    - duty_2_in: duty_2_in parameter
    - duty_1_in: duty_1_in parameter
    - friction_2_in: friction_2_in parameter
    - deposition_2_in: deposition_2_in parameter

Outputs:
    - friction_total: friction_total result
    - deposited_total: deposited_total result
    - delivered_total: delivered_total result
    - energy_residual: energy_residual result

SysML Source: root-0/dual_circuit_heat_accounting.sysml:13

    SysML Source: root-0/dual_circuit_heat_accounting.sysml:13

    Calculation Specification:
        See documentation:
delivered_total = duty_1_in + duty_2_in; deposited_total = deposition_1_in + deposition_2_in; friction_total = friction_1_in + friction_2_in; energy_residual = delivered_total - deposited_total - friction_total. All quantities MW. Source: work/active/WI-086_aries-dual-blanket-heat-accounting/spec.md. Ref: two-branch control boundary with internal exchange canceling once. Basis: generic energy accounting; native completion rejects nonfinite/negative supplied heat and nonfinite outputs, but preserves signed residuals without clamping or forcing closure. A nonzero residual is a diagnostic, not an equipment adequacy claim. Independent source comparison belongs in the analysis record, not this physical producer. Last Updated: 2026-09-21.

    IMPLEMENTATION: See heat_tea.handwritten.dual_circuit_heat_accounting.dual_circuit_heat_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts friction_total, deposited_total, delivered_total, energy_residual fields to separate channels.
    """

    name: str = "Dual_Circuit_Heat_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, deposition_1_in: float, friction_1_in: float, duty_2_in: float, duty_1_in: float, friction_2_in: float, deposition_2_in: float    ) -> Dual_Circuit_Heat_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            deposition_1_in: deposition_1_in input
            friction_1_in: friction_1_in input
            duty_2_in: duty_2_in input
            duty_1_in: duty_1_in input
            friction_2_in: friction_2_in input
            deposition_2_in: deposition_2_in input

        Returns:
            Validated input model
        """
        return Dual_Circuit_Heat_LedgerInput(deposition_1_in=deposition_1_in, friction_1_in=friction_1_in, duty_2_in=duty_2_in, duty_1_in=duty_1_in, friction_2_in=friction_2_in, deposition_2_in=deposition_2_in)

    def run(
        self, deposition_1_in: float, friction_1_in: float, duty_2_in: float, duty_1_in: float, friction_2_in: float, deposition_2_in: float    ) -> ModuleResult[Dual_Circuit_Heat_LedgerOutput]:
        """Execute calculation.

        Args:
            deposition_1_in: deposition_1_in input
            friction_1_in: friction_1_in input
            duty_2_in: duty_2_in input
            duty_1_in: duty_1_in input
            friction_2_in: friction_2_in input
            deposition_2_in: deposition_2_in input

        Returns:
            Module result with Dual_Circuit_Heat_LedgerOutput (friction_total, deposited_total, delivered_total, energy_residual)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(deposition_1_in, friction_1_in, duty_2_in, duty_1_in, friction_2_in, deposition_2_in)

        # Import handwritten implementation
        from heat_tea.handwritten.dual_circuit_heat_accounting.dual_circuit_heat_ledger_impl import (
            run_dual_circuit_heat_ledger,
        )

        # Execute implementation - returns tuple of values
        friction_total, deposited_total, delivered_total, energy_residual = run_dual_circuit_heat_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Dual_Circuit_Heat_LedgerOutput(
                friction_total=friction_total,
                deposited_total=deposited_total,
                delivered_total=delivered_total,
                energy_residual=energy_residual,
            )
        )
