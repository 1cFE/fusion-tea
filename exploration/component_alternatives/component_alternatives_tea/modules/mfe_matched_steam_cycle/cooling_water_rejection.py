"""Cooling_Water_RejectionModule Module Wrapper

TEAx module for Cooling_Water_Rejection calculation.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

Inputs:
    - head_m_in: head_m_in parameter
    - water_outlet_C_in: water_outlet_C_in parameter
    - water_inlet_C_in: water_inlet_C_in parameter
    - eta_pump_in: eta_pump_in parameter
    - cycle_active_in: cycle_active_in parameter
    - condenser_temperature_C_in: condenser_temperature_C_in parameter
    - enabled_in: enabled_in parameter
    - eta_motor_in: eta_motor_in parameter
    - q_rejection_before_cooling_MW_in: q_rejection_before_cooling_MW_in parameter

Outputs:
    - site_qualified: site_qualified result
    - cooling_approach_ok: cooling_approach_ok result
    - q_cooling_motor_loss_MW: q_cooling_motor_loss_MW result
    - water_flow_kg_s: water_flow_kg_s result
    - water_energy_residual_MW: water_energy_residual_MW result
    - reference_scenario: reference_scenario result
    - condenser_water_gap_K: condenser_water_gap_K result
    - q_total_rejection_MW: q_total_rejection_MW result
    - p_cooling_pump_electric_MW: p_cooling_pump_electric_MW result
    - p_cooling_pump_shaft_MW: p_cooling_pump_shaft_MW result
    - water_pump_rise_K: water_pump_rise_K result
    - active: active result
    - denominator_kJ_kg: denominator_kJ_kg result

SysML Source: root-0/mfe_matched_steam_cycle.sysml:105

SysML Source: root-0/mfe_matched_steam_cycle.sysml:105

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_matched_steam_cycle/cooling_water_rejection_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.cooling_water_rejection_output import Cooling_Water_RejectionOutput


class Cooling_Water_RejectionInput(BaseModel):
    """Input model for Cooling_Water_RejectionModule.

    Attributes:
        head_m_in: head_m_in input
        water_outlet_C_in: water_outlet_C_in input
        water_inlet_C_in: water_inlet_C_in input
        eta_pump_in: eta_pump_in input
        cycle_active_in: cycle_active_in input
        condenser_temperature_C_in: condenser_temperature_C_in input
        enabled_in: enabled_in input
        eta_motor_in: eta_motor_in input
        q_rejection_before_cooling_MW_in: q_rejection_before_cooling_MW_in input
    """
    head_m_in: float = Field(..., description="head_m_in input")
    water_outlet_C_in: float = Field(..., description="water_outlet_C_in input")
    water_inlet_C_in: float = Field(..., description="water_inlet_C_in input")
    eta_pump_in: float = Field(..., description="eta_pump_in input")
    cycle_active_in: float = Field(..., description="cycle_active_in input")
    condenser_temperature_C_in: float = Field(..., description="condenser_temperature_C_in input")
    enabled_in: float = Field(..., description="enabled_in input")
    eta_motor_in: float = Field(..., description="eta_motor_in input")
    q_rejection_before_cooling_MW_in: float = Field(..., description="q_rejection_before_cooling_MW_in input")


class Cooling_Water_RejectionModule(ModuleBase[Cooling_Water_RejectionInput, Cooling_Water_RejectionOutput]):
    """TEAx module for Cooling_Water_Rejection calculation.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

Inputs:
    - head_m_in: head_m_in parameter
    - water_outlet_C_in: water_outlet_C_in parameter
    - water_inlet_C_in: water_inlet_C_in parameter
    - eta_pump_in: eta_pump_in parameter
    - cycle_active_in: cycle_active_in parameter
    - condenser_temperature_C_in: condenser_temperature_C_in parameter
    - enabled_in: enabled_in parameter
    - eta_motor_in: eta_motor_in parameter
    - q_rejection_before_cooling_MW_in: q_rejection_before_cooling_MW_in parameter

Outputs:
    - site_qualified: site_qualified result
    - cooling_approach_ok: cooling_approach_ok result
    - q_cooling_motor_loss_MW: q_cooling_motor_loss_MW result
    - water_flow_kg_s: water_flow_kg_s result
    - water_energy_residual_MW: water_energy_residual_MW result
    - reference_scenario: reference_scenario result
    - condenser_water_gap_K: condenser_water_gap_K result
    - q_total_rejection_MW: q_total_rejection_MW result
    - p_cooling_pump_electric_MW: p_cooling_pump_electric_MW result
    - p_cooling_pump_shaft_MW: p_cooling_pump_shaft_MW result
    - water_pump_rise_K: water_pump_rise_K result
    - active: active result
    - denominator_kJ_kg: denominator_kJ_kg result

SysML Source: root-0/mfe_matched_steam_cycle.sysml:105

    SysML Source: root-0/mfe_matched_steam_cycle.sysml:105

    Calculation Specification:
        See documentation:
*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

    IMPLEMENTATION: See component_alternatives_tea.handwritten.mfe_matched_steam_cycle.cooling_water_rejection_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts site_qualified, cooling_approach_ok, q_cooling_motor_loss_MW, water_flow_kg_s, water_energy_residual_MW, reference_scenario, condenser_water_gap_K, q_total_rejection_MW, p_cooling_pump_electric_MW, p_cooling_pump_shaft_MW, water_pump_rise_K, active, denominator_kJ_kg fields to separate channels.
    """

    name: str = "Cooling_Water_RejectionModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, head_m_in: float, water_outlet_C_in: float, water_inlet_C_in: float, eta_pump_in: float, cycle_active_in: float, condenser_temperature_C_in: float, enabled_in: float, eta_motor_in: float, q_rejection_before_cooling_MW_in: float    ) -> Cooling_Water_RejectionInput:
        """Validate inputs and fill defaults.

        Args:
            head_m_in: head_m_in input
            water_outlet_C_in: water_outlet_C_in input
            water_inlet_C_in: water_inlet_C_in input
            eta_pump_in: eta_pump_in input
            cycle_active_in: cycle_active_in input
            condenser_temperature_C_in: condenser_temperature_C_in input
            enabled_in: enabled_in input
            eta_motor_in: eta_motor_in input
            q_rejection_before_cooling_MW_in: q_rejection_before_cooling_MW_in input

        Returns:
            Validated input model
        """
        return Cooling_Water_RejectionInput(head_m_in=head_m_in, water_outlet_C_in=water_outlet_C_in, water_inlet_C_in=water_inlet_C_in, eta_pump_in=eta_pump_in, cycle_active_in=cycle_active_in, condenser_temperature_C_in=condenser_temperature_C_in, enabled_in=enabled_in, eta_motor_in=eta_motor_in, q_rejection_before_cooling_MW_in=q_rejection_before_cooling_MW_in)

    def run(
        self, head_m_in: float, water_outlet_C_in: float, water_inlet_C_in: float, eta_pump_in: float, cycle_active_in: float, condenser_temperature_C_in: float, enabled_in: float, eta_motor_in: float, q_rejection_before_cooling_MW_in: float    ) -> ModuleResult[Cooling_Water_RejectionOutput]:
        """Execute calculation.

        Args:
            head_m_in: head_m_in input
            water_outlet_C_in: water_outlet_C_in input
            water_inlet_C_in: water_inlet_C_in input
            eta_pump_in: eta_pump_in input
            cycle_active_in: cycle_active_in input
            condenser_temperature_C_in: condenser_temperature_C_in input
            enabled_in: enabled_in input
            eta_motor_in: eta_motor_in input
            q_rejection_before_cooling_MW_in: q_rejection_before_cooling_MW_in input

        Returns:
            Module result with Cooling_Water_RejectionOutput (site_qualified, cooling_approach_ok, q_cooling_motor_loss_MW, water_flow_kg_s, water_energy_residual_MW, reference_scenario, condenser_water_gap_K, q_total_rejection_MW, p_cooling_pump_electric_MW, p_cooling_pump_shaft_MW, water_pump_rise_K, active, denominator_kJ_kg)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(head_m_in, water_outlet_C_in, water_inlet_C_in, eta_pump_in, cycle_active_in, condenser_temperature_C_in, enabled_in, eta_motor_in, q_rejection_before_cooling_MW_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.mfe_matched_steam_cycle.cooling_water_rejection_impl import (
            run_cooling_water_rejection,
        )

        # Execute implementation - returns tuple of values
        site_qualified, cooling_approach_ok, q_cooling_motor_loss_MW, water_flow_kg_s, water_energy_residual_MW, reference_scenario, condenser_water_gap_K, q_total_rejection_MW, p_cooling_pump_electric_MW, p_cooling_pump_shaft_MW, water_pump_rise_K, active, denominator_kJ_kg = run_cooling_water_rejection(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Cooling_Water_RejectionOutput(
                site_qualified=site_qualified,
                cooling_approach_ok=cooling_approach_ok,
                q_cooling_motor_loss_MW=q_cooling_motor_loss_MW,
                water_flow_kg_s=water_flow_kg_s,
                water_energy_residual_MW=water_energy_residual_MW,
                reference_scenario=reference_scenario,
                condenser_water_gap_K=condenser_water_gap_K,
                q_total_rejection_MW=q_total_rejection_MW,
                p_cooling_pump_electric_MW=p_cooling_pump_electric_MW,
                p_cooling_pump_shaft_MW=p_cooling_pump_shaft_MW,
                water_pump_rise_K=water_pump_rise_K,
                active=active,
                denominator_kJ_kg=denominator_kJ_kg,
            )
        )
