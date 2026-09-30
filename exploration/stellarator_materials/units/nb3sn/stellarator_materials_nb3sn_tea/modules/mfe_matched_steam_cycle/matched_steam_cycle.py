"""Matched_Steam_CycleModule Module Wrapper

TEAx module for Matched_Steam_Cycle calculation.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

Inputs:
    - enabled_in: enabled_in parameter
    - eta_hp_in: eta_hp_in parameter
    - steam_temperature_C_in: steam_temperature_C_in parameter
    - salt_return_C_in: salt_return_C_in parameter
    - eta_condensate_pump_in: eta_condensate_pump_in parameter
    - salt_circuit_count_in: salt_circuit_count_in parameter
    - eta_lp_in: eta_lp_in parameter
    - eta_mechanical_in: eta_mechanical_in parameter
    - extraction_pressure_MPa_in: extraction_pressure_MPa_in parameter
    - heat_available_MW_in: heat_available_MW_in parameter
    - eta_pump_motor_in: eta_pump_motor_in parameter
    - eta_feedwater_pump_in: eta_feedwater_pump_in parameter
    - salt_flow_per_circuit_in: salt_flow_per_circuit_in parameter
    - salt_hot_C_in: salt_hot_C_in parameter
    - source_heat_MW_in: source_heat_MW_in parameter
    - condenser_temperature_C_in: condenser_temperature_C_in parameter
    - main_pressure_MPa_in: main_pressure_MPa_in parameter
    - eta_generator_in: eta_generator_in parameter
    - salt_cp_kJ_kgK_in: salt_cp_kJ_kgK_in parameter
    - selected_recovered_MW_in: selected_recovered_MW_in parameter
    - reheat_temperature_C_in: reheat_temperature_C_in parameter

Outputs:
    - s_main_kJ_kgK: s_main_kJ_kgK result
    - reheat_min_gap_K: reheat_min_gap_K result
    - mdot_heater_kg_s: mdot_heater_kg_s result
    - h_hp_kJ_kg: h_hp_kJ_kg result
    - s_lp_kJ_kgK: s_lp_kJ_kgK result
    - p_condensate_pumped_MPa: p_condensate_pumped_MPa result
    - mdot_main_kg_s: mdot_main_kg_s result
    - mdot_reheat_kg_s: mdot_reheat_kg_s result
    - q_generator_loss_MW: q_generator_loss_MW result
    - t_feed_C: t_feed_C result
    - p_cycle_net_before_cooling_MW: p_cycle_net_before_cooling_MW result
    - main_UA_available: main_UA_available result
    - p_feedwater_electric_MW: p_feedwater_electric_MW result
    - q_rejection_before_cooling_MW: q_rejection_before_cooling_MW result
    - p_lp_MPa: p_lp_MPa result
    - lp_quality: lp_quality result
    - h_condensate_pumped_kJ_kg: h_condensate_pumped_kJ_kg result
    - t_heater_C: t_heater_C result
    - p_cycle_pumps_MW: p_cycle_pumps_MW result
    - t_condensate_C: t_condensate_C result
    - salt_reheat_flow_kg_s: salt_reheat_flow_kg_s result
    - s_reheat_kJ_kgK: s_reheat_kJ_kgK result
    - salt_main_flow_kg_s: salt_main_flow_kg_s result
    - p_gross_MW: p_gross_MW result
    - p_feedwater_shaft_MW: p_feedwater_shaft_MW result
    - h_main_kJ_kg: h_main_kJ_kg result
    - t_reheat_C: t_reheat_C result
    - installed_sg_capacity_qualified: installed_sg_capacity_qualified result
    - p_hp_shaft_MW: p_hp_shaft_MW result
    - p_main_MPa: p_main_MPa result
    - t_hp_C: t_hp_C result
    - mdot_feed_kg_s: mdot_feed_kg_s result
    - mdot_bleed_kg_s: mdot_bleed_kg_s result
    - p_condensate_MPa: p_condensate_MPa result
    - salt_heat_residual_MW: salt_heat_residual_MW result
    - p_hp_MPa: p_hp_MPa result
    - active: active result
    - eta_gross: eta_gross result
    - h_lp_kJ_kg: h_lp_kJ_kg result
    - mdot_condensate_kg_s: mdot_condensate_kg_s result
    - h_feed_kJ_kg: h_feed_kJ_kg result
    - heater_energy_residual_MW: heater_energy_residual_MW result
    - lp_moisture_fraction: lp_moisture_fraction result
    - t_main_C: t_main_C result
    - cycle_electric_residual_MW: cycle_electric_residual_MW result
    - p_feed_MPa: p_feed_MPa result
    - main_UA_MW_K: main_UA_MW_K result
    - bleed_fraction: bleed_fraction result
    - p_reheat_MPa: p_reheat_MPa result
    - mdot_lp_kg_s: mdot_lp_kg_s result
    - reheat_UA_MW_K: reheat_UA_MW_K result
    - p_lp_shaft_MW: p_lp_shaft_MW result
    - p_heater_MPa: p_heater_MPa result
    - q_main_MW: q_main_MW result
    - q_pump_motor_loss_MW: q_pump_motor_loss_MW result
    - q_mechanical_loss_MW: q_mechanical_loss_MW result
    - p_condensate_electric_MW: p_condensate_electric_MW result
    - main_min_gap_K: main_min_gap_K result
    - heater_mass_residual_kg_s: heater_mass_residual_kg_s result
    - s_hp_kJ_kgK: s_hp_kJ_kgK result
    - h_heater_kJ_kg: h_heater_kJ_kg result
    - main_admission_ok: main_admission_ok result
    - q_condenser_MW: q_condenser_MW result
    - mdot_hp_kg_s: mdot_hp_kg_s result
    - h_condensate_kJ_kg: h_condensate_kJ_kg result
    - p_condensate_shaft_MW: p_condensate_shaft_MW result
    - turbine_equipment_qualified: turbine_equipment_qualified result
    - h_reheat_kJ_kg: h_reheat_kJ_kg result
    - cycle_shaft_residual_MW: cycle_shaft_residual_MW result
    - reheat_admission_ok: reheat_admission_ok result
    - s_heater_kJ_kgK: s_heater_kJ_kgK result
    - q_reheat_MW: q_reheat_MW result
    - s_feed_kJ_kgK: s_feed_kJ_kgK result
    - salt_flow_total_kg_s: salt_flow_total_kg_s result
    - reheat_UA_available: reheat_UA_available result
    - s_condensate_kJ_kgK: s_condensate_kJ_kgK result
    - mdot_condensate_pumped_kg_s: mdot_condensate_pumped_kg_s result
    - t_lp_C: t_lp_C result

SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:3

SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/mfe_matched_steam_cycle/matched_steam_cycle_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from stellarator_materials_nb3sn_tea.primitives import Float
from stellarator_materials_nb3sn_tea.schemas.matched_steam_cycle_output import Matched_Steam_CycleOutput


class Matched_Steam_CycleInput(BaseModel):
    """Input model for Matched_Steam_CycleModule.

    Attributes:
        enabled_in: enabled_in input
        eta_hp_in: eta_hp_in input
        steam_temperature_C_in: steam_temperature_C_in input
        salt_return_C_in: salt_return_C_in input
        eta_condensate_pump_in: eta_condensate_pump_in input
        salt_circuit_count_in: salt_circuit_count_in input
        eta_lp_in: eta_lp_in input
        eta_mechanical_in: eta_mechanical_in input
        extraction_pressure_MPa_in: extraction_pressure_MPa_in input
        heat_available_MW_in: heat_available_MW_in input
        eta_pump_motor_in: eta_pump_motor_in input
        eta_feedwater_pump_in: eta_feedwater_pump_in input
        salt_flow_per_circuit_in: salt_flow_per_circuit_in input
        salt_hot_C_in: salt_hot_C_in input
        source_heat_MW_in: source_heat_MW_in input
        condenser_temperature_C_in: condenser_temperature_C_in input
        main_pressure_MPa_in: main_pressure_MPa_in input
        eta_generator_in: eta_generator_in input
        salt_cp_kJ_kgK_in: salt_cp_kJ_kgK_in input
        selected_recovered_MW_in: selected_recovered_MW_in input
        reheat_temperature_C_in: reheat_temperature_C_in input
    """
    enabled_in: float = Field(..., description="enabled_in input")
    eta_hp_in: float = Field(..., description="eta_hp_in input")
    steam_temperature_C_in: float = Field(..., description="steam_temperature_C_in input")
    salt_return_C_in: float = Field(..., description="salt_return_C_in input")
    eta_condensate_pump_in: float = Field(..., description="eta_condensate_pump_in input")
    salt_circuit_count_in: float = Field(..., description="salt_circuit_count_in input")
    eta_lp_in: float = Field(..., description="eta_lp_in input")
    eta_mechanical_in: float = Field(..., description="eta_mechanical_in input")
    extraction_pressure_MPa_in: float = Field(..., description="extraction_pressure_MPa_in input")
    heat_available_MW_in: float = Field(..., description="heat_available_MW_in input")
    eta_pump_motor_in: float = Field(..., description="eta_pump_motor_in input")
    eta_feedwater_pump_in: float = Field(..., description="eta_feedwater_pump_in input")
    salt_flow_per_circuit_in: float = Field(..., description="salt_flow_per_circuit_in input")
    salt_hot_C_in: float = Field(..., description="salt_hot_C_in input")
    source_heat_MW_in: float = Field(..., description="source_heat_MW_in input")
    condenser_temperature_C_in: float = Field(..., description="condenser_temperature_C_in input")
    main_pressure_MPa_in: float = Field(..., description="main_pressure_MPa_in input")
    eta_generator_in: float = Field(..., description="eta_generator_in input")
    salt_cp_kJ_kgK_in: float = Field(..., description="salt_cp_kJ_kgK_in input")
    selected_recovered_MW_in: float = Field(..., description="selected_recovered_MW_in input")
    reheat_temperature_C_in: float = Field(..., description="reheat_temperature_C_in input")


class Matched_Steam_CycleModule(ModuleBase[Matched_Steam_CycleInput, Matched_Steam_CycleOutput]):
    """TEAx module for Matched_Steam_Cycle calculation.

*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

Inputs:
    - enabled_in: enabled_in parameter
    - eta_hp_in: eta_hp_in parameter
    - steam_temperature_C_in: steam_temperature_C_in parameter
    - salt_return_C_in: salt_return_C_in parameter
    - eta_condensate_pump_in: eta_condensate_pump_in parameter
    - salt_circuit_count_in: salt_circuit_count_in parameter
    - eta_lp_in: eta_lp_in parameter
    - eta_mechanical_in: eta_mechanical_in parameter
    - extraction_pressure_MPa_in: extraction_pressure_MPa_in parameter
    - heat_available_MW_in: heat_available_MW_in parameter
    - eta_pump_motor_in: eta_pump_motor_in parameter
    - eta_feedwater_pump_in: eta_feedwater_pump_in parameter
    - salt_flow_per_circuit_in: salt_flow_per_circuit_in parameter
    - salt_hot_C_in: salt_hot_C_in parameter
    - source_heat_MW_in: source_heat_MW_in parameter
    - condenser_temperature_C_in: condenser_temperature_C_in parameter
    - main_pressure_MPa_in: main_pressure_MPa_in parameter
    - eta_generator_in: eta_generator_in parameter
    - salt_cp_kJ_kgK_in: salt_cp_kJ_kgK_in parameter
    - selected_recovered_MW_in: selected_recovered_MW_in parameter
    - reheat_temperature_C_in: reheat_temperature_C_in parameter

Outputs:
    - s_main_kJ_kgK: s_main_kJ_kgK result
    - reheat_min_gap_K: reheat_min_gap_K result
    - mdot_heater_kg_s: mdot_heater_kg_s result
    - h_hp_kJ_kg: h_hp_kJ_kg result
    - s_lp_kJ_kgK: s_lp_kJ_kgK result
    - p_condensate_pumped_MPa: p_condensate_pumped_MPa result
    - mdot_main_kg_s: mdot_main_kg_s result
    - mdot_reheat_kg_s: mdot_reheat_kg_s result
    - q_generator_loss_MW: q_generator_loss_MW result
    - t_feed_C: t_feed_C result
    - p_cycle_net_before_cooling_MW: p_cycle_net_before_cooling_MW result
    - main_UA_available: main_UA_available result
    - p_feedwater_electric_MW: p_feedwater_electric_MW result
    - q_rejection_before_cooling_MW: q_rejection_before_cooling_MW result
    - p_lp_MPa: p_lp_MPa result
    - lp_quality: lp_quality result
    - h_condensate_pumped_kJ_kg: h_condensate_pumped_kJ_kg result
    - t_heater_C: t_heater_C result
    - p_cycle_pumps_MW: p_cycle_pumps_MW result
    - t_condensate_C: t_condensate_C result
    - salt_reheat_flow_kg_s: salt_reheat_flow_kg_s result
    - s_reheat_kJ_kgK: s_reheat_kJ_kgK result
    - salt_main_flow_kg_s: salt_main_flow_kg_s result
    - p_gross_MW: p_gross_MW result
    - p_feedwater_shaft_MW: p_feedwater_shaft_MW result
    - h_main_kJ_kg: h_main_kJ_kg result
    - t_reheat_C: t_reheat_C result
    - installed_sg_capacity_qualified: installed_sg_capacity_qualified result
    - p_hp_shaft_MW: p_hp_shaft_MW result
    - p_main_MPa: p_main_MPa result
    - t_hp_C: t_hp_C result
    - mdot_feed_kg_s: mdot_feed_kg_s result
    - mdot_bleed_kg_s: mdot_bleed_kg_s result
    - p_condensate_MPa: p_condensate_MPa result
    - salt_heat_residual_MW: salt_heat_residual_MW result
    - p_hp_MPa: p_hp_MPa result
    - active: active result
    - eta_gross: eta_gross result
    - h_lp_kJ_kg: h_lp_kJ_kg result
    - mdot_condensate_kg_s: mdot_condensate_kg_s result
    - h_feed_kJ_kg: h_feed_kJ_kg result
    - heater_energy_residual_MW: heater_energy_residual_MW result
    - lp_moisture_fraction: lp_moisture_fraction result
    - t_main_C: t_main_C result
    - cycle_electric_residual_MW: cycle_electric_residual_MW result
    - p_feed_MPa: p_feed_MPa result
    - main_UA_MW_K: main_UA_MW_K result
    - bleed_fraction: bleed_fraction result
    - p_reheat_MPa: p_reheat_MPa result
    - mdot_lp_kg_s: mdot_lp_kg_s result
    - reheat_UA_MW_K: reheat_UA_MW_K result
    - p_lp_shaft_MW: p_lp_shaft_MW result
    - p_heater_MPa: p_heater_MPa result
    - q_main_MW: q_main_MW result
    - q_pump_motor_loss_MW: q_pump_motor_loss_MW result
    - q_mechanical_loss_MW: q_mechanical_loss_MW result
    - p_condensate_electric_MW: p_condensate_electric_MW result
    - main_min_gap_K: main_min_gap_K result
    - heater_mass_residual_kg_s: heater_mass_residual_kg_s result
    - s_hp_kJ_kgK: s_hp_kJ_kgK result
    - h_heater_kJ_kg: h_heater_kJ_kg result
    - main_admission_ok: main_admission_ok result
    - q_condenser_MW: q_condenser_MW result
    - mdot_hp_kg_s: mdot_hp_kg_s result
    - h_condensate_kJ_kg: h_condensate_kJ_kg result
    - p_condensate_shaft_MW: p_condensate_shaft_MW result
    - turbine_equipment_qualified: turbine_equipment_qualified result
    - h_reheat_kJ_kg: h_reheat_kJ_kg result
    - cycle_shaft_residual_MW: cycle_shaft_residual_MW result
    - reheat_admission_ok: reheat_admission_ok result
    - s_heater_kJ_kgK: s_heater_kJ_kgK result
    - q_reheat_MW: q_reheat_MW result
    - s_feed_kJ_kgK: s_feed_kJ_kgK result
    - salt_flow_total_kg_s: salt_flow_total_kg_s result
    - reheat_UA_available: reheat_UA_available result
    - s_condensate_kJ_kgK: s_condensate_kJ_kgK result
    - mdot_condensate_pumped_kg_s: mdot_condensate_pumped_kg_s result
    - t_lp_C: t_lp_C result

SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:3

    SysML Source: root-0/analyses/mfe_matched_steam_cycle.sysml:3

    Calculation Specification:
        See documentation:
*Source**: work/orchestration/goals/current-model-comparison-readiness/evidence/round2/cycle-proposal-v2.md **Reference**: WI-073 design.md and interface-inventory.md; original NIST tables and independent physical review. **Basis**: [AGENT] reviewed reduced extraction/reheat cycle and conditional cooling-water scenario; equipment and installed cost unqualified. **Last Updated**: 2026-09-19 Numerical semantic: the normative handwritten implementation executes the exact state/work equations in the cited design. Disabled modes branch before property access; no extrapolation. Units are given by the scalar names and interface inventory.

    IMPLEMENTATION: See stellarator_materials_nb3sn_tea.handwritten.mfe_matched_steam_cycle.matched_steam_cycle_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts s_main_kJ_kgK, reheat_min_gap_K, mdot_heater_kg_s, h_hp_kJ_kg, s_lp_kJ_kgK, p_condensate_pumped_MPa, mdot_main_kg_s, mdot_reheat_kg_s, q_generator_loss_MW, t_feed_C, p_cycle_net_before_cooling_MW, main_UA_available, p_feedwater_electric_MW, q_rejection_before_cooling_MW, p_lp_MPa, lp_quality, h_condensate_pumped_kJ_kg, t_heater_C, p_cycle_pumps_MW, t_condensate_C, salt_reheat_flow_kg_s, s_reheat_kJ_kgK, salt_main_flow_kg_s, p_gross_MW, p_feedwater_shaft_MW, h_main_kJ_kg, t_reheat_C, installed_sg_capacity_qualified, p_hp_shaft_MW, p_main_MPa, t_hp_C, mdot_feed_kg_s, mdot_bleed_kg_s, p_condensate_MPa, salt_heat_residual_MW, p_hp_MPa, active, eta_gross, h_lp_kJ_kg, mdot_condensate_kg_s, h_feed_kJ_kg, heater_energy_residual_MW, lp_moisture_fraction, t_main_C, cycle_electric_residual_MW, p_feed_MPa, main_UA_MW_K, bleed_fraction, p_reheat_MPa, mdot_lp_kg_s, reheat_UA_MW_K, p_lp_shaft_MW, p_heater_MPa, q_main_MW, q_pump_motor_loss_MW, q_mechanical_loss_MW, p_condensate_electric_MW, main_min_gap_K, heater_mass_residual_kg_s, s_hp_kJ_kgK, h_heater_kJ_kg, main_admission_ok, q_condenser_MW, mdot_hp_kg_s, h_condensate_kJ_kg, p_condensate_shaft_MW, turbine_equipment_qualified, h_reheat_kJ_kg, cycle_shaft_residual_MW, reheat_admission_ok, s_heater_kJ_kgK, q_reheat_MW, s_feed_kJ_kgK, salt_flow_total_kg_s, reheat_UA_available, s_condensate_kJ_kgK, mdot_condensate_pumped_kg_s, t_lp_C fields to separate channels.
    """

    name: str = "Matched_Steam_CycleModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, enabled_in: float, eta_hp_in: float, steam_temperature_C_in: float, salt_return_C_in: float, eta_condensate_pump_in: float, salt_circuit_count_in: float, eta_lp_in: float, eta_mechanical_in: float, extraction_pressure_MPa_in: float, heat_available_MW_in: float, eta_pump_motor_in: float, eta_feedwater_pump_in: float, salt_flow_per_circuit_in: float, salt_hot_C_in: float, source_heat_MW_in: float, condenser_temperature_C_in: float, main_pressure_MPa_in: float, eta_generator_in: float, salt_cp_kJ_kgK_in: float, selected_recovered_MW_in: float, reheat_temperature_C_in: float    ) -> Matched_Steam_CycleInput:
        """Validate inputs and fill defaults.

        Args:
            enabled_in: enabled_in input
            eta_hp_in: eta_hp_in input
            steam_temperature_C_in: steam_temperature_C_in input
            salt_return_C_in: salt_return_C_in input
            eta_condensate_pump_in: eta_condensate_pump_in input
            salt_circuit_count_in: salt_circuit_count_in input
            eta_lp_in: eta_lp_in input
            eta_mechanical_in: eta_mechanical_in input
            extraction_pressure_MPa_in: extraction_pressure_MPa_in input
            heat_available_MW_in: heat_available_MW_in input
            eta_pump_motor_in: eta_pump_motor_in input
            eta_feedwater_pump_in: eta_feedwater_pump_in input
            salt_flow_per_circuit_in: salt_flow_per_circuit_in input
            salt_hot_C_in: salt_hot_C_in input
            source_heat_MW_in: source_heat_MW_in input
            condenser_temperature_C_in: condenser_temperature_C_in input
            main_pressure_MPa_in: main_pressure_MPa_in input
            eta_generator_in: eta_generator_in input
            salt_cp_kJ_kgK_in: salt_cp_kJ_kgK_in input
            selected_recovered_MW_in: selected_recovered_MW_in input
            reheat_temperature_C_in: reheat_temperature_C_in input

        Returns:
            Validated input model
        """
        return Matched_Steam_CycleInput(enabled_in=enabled_in, eta_hp_in=eta_hp_in, steam_temperature_C_in=steam_temperature_C_in, salt_return_C_in=salt_return_C_in, eta_condensate_pump_in=eta_condensate_pump_in, salt_circuit_count_in=salt_circuit_count_in, eta_lp_in=eta_lp_in, eta_mechanical_in=eta_mechanical_in, extraction_pressure_MPa_in=extraction_pressure_MPa_in, heat_available_MW_in=heat_available_MW_in, eta_pump_motor_in=eta_pump_motor_in, eta_feedwater_pump_in=eta_feedwater_pump_in, salt_flow_per_circuit_in=salt_flow_per_circuit_in, salt_hot_C_in=salt_hot_C_in, source_heat_MW_in=source_heat_MW_in, condenser_temperature_C_in=condenser_temperature_C_in, main_pressure_MPa_in=main_pressure_MPa_in, eta_generator_in=eta_generator_in, salt_cp_kJ_kgK_in=salt_cp_kJ_kgK_in, selected_recovered_MW_in=selected_recovered_MW_in, reheat_temperature_C_in=reheat_temperature_C_in)

    def run(
        self, enabled_in: float, eta_hp_in: float, steam_temperature_C_in: float, salt_return_C_in: float, eta_condensate_pump_in: float, salt_circuit_count_in: float, eta_lp_in: float, eta_mechanical_in: float, extraction_pressure_MPa_in: float, heat_available_MW_in: float, eta_pump_motor_in: float, eta_feedwater_pump_in: float, salt_flow_per_circuit_in: float, salt_hot_C_in: float, source_heat_MW_in: float, condenser_temperature_C_in: float, main_pressure_MPa_in: float, eta_generator_in: float, salt_cp_kJ_kgK_in: float, selected_recovered_MW_in: float, reheat_temperature_C_in: float    ) -> ModuleResult[Matched_Steam_CycleOutput]:
        """Execute calculation.

        Args:
            enabled_in: enabled_in input
            eta_hp_in: eta_hp_in input
            steam_temperature_C_in: steam_temperature_C_in input
            salt_return_C_in: salt_return_C_in input
            eta_condensate_pump_in: eta_condensate_pump_in input
            salt_circuit_count_in: salt_circuit_count_in input
            eta_lp_in: eta_lp_in input
            eta_mechanical_in: eta_mechanical_in input
            extraction_pressure_MPa_in: extraction_pressure_MPa_in input
            heat_available_MW_in: heat_available_MW_in input
            eta_pump_motor_in: eta_pump_motor_in input
            eta_feedwater_pump_in: eta_feedwater_pump_in input
            salt_flow_per_circuit_in: salt_flow_per_circuit_in input
            salt_hot_C_in: salt_hot_C_in input
            source_heat_MW_in: source_heat_MW_in input
            condenser_temperature_C_in: condenser_temperature_C_in input
            main_pressure_MPa_in: main_pressure_MPa_in input
            eta_generator_in: eta_generator_in input
            salt_cp_kJ_kgK_in: salt_cp_kJ_kgK_in input
            selected_recovered_MW_in: selected_recovered_MW_in input
            reheat_temperature_C_in: reheat_temperature_C_in input

        Returns:
            Module result with Matched_Steam_CycleOutput (s_main_kJ_kgK, reheat_min_gap_K, mdot_heater_kg_s, h_hp_kJ_kg, s_lp_kJ_kgK, p_condensate_pumped_MPa, mdot_main_kg_s, mdot_reheat_kg_s, q_generator_loss_MW, t_feed_C, p_cycle_net_before_cooling_MW, main_UA_available, p_feedwater_electric_MW, q_rejection_before_cooling_MW, p_lp_MPa, lp_quality, h_condensate_pumped_kJ_kg, t_heater_C, p_cycle_pumps_MW, t_condensate_C, salt_reheat_flow_kg_s, s_reheat_kJ_kgK, salt_main_flow_kg_s, p_gross_MW, p_feedwater_shaft_MW, h_main_kJ_kg, t_reheat_C, installed_sg_capacity_qualified, p_hp_shaft_MW, p_main_MPa, t_hp_C, mdot_feed_kg_s, mdot_bleed_kg_s, p_condensate_MPa, salt_heat_residual_MW, p_hp_MPa, active, eta_gross, h_lp_kJ_kg, mdot_condensate_kg_s, h_feed_kJ_kg, heater_energy_residual_MW, lp_moisture_fraction, t_main_C, cycle_electric_residual_MW, p_feed_MPa, main_UA_MW_K, bleed_fraction, p_reheat_MPa, mdot_lp_kg_s, reheat_UA_MW_K, p_lp_shaft_MW, p_heater_MPa, q_main_MW, q_pump_motor_loss_MW, q_mechanical_loss_MW, p_condensate_electric_MW, main_min_gap_K, heater_mass_residual_kg_s, s_hp_kJ_kgK, h_heater_kJ_kg, main_admission_ok, q_condenser_MW, mdot_hp_kg_s, h_condensate_kJ_kg, p_condensate_shaft_MW, turbine_equipment_qualified, h_reheat_kJ_kg, cycle_shaft_residual_MW, reheat_admission_ok, s_heater_kJ_kgK, q_reheat_MW, s_feed_kJ_kgK, salt_flow_total_kg_s, reheat_UA_available, s_condensate_kJ_kgK, mdot_condensate_pumped_kg_s, t_lp_C)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(enabled_in, eta_hp_in, steam_temperature_C_in, salt_return_C_in, eta_condensate_pump_in, salt_circuit_count_in, eta_lp_in, eta_mechanical_in, extraction_pressure_MPa_in, heat_available_MW_in, eta_pump_motor_in, eta_feedwater_pump_in, salt_flow_per_circuit_in, salt_hot_C_in, source_heat_MW_in, condenser_temperature_C_in, main_pressure_MPa_in, eta_generator_in, salt_cp_kJ_kgK_in, selected_recovered_MW_in, reheat_temperature_C_in)

        # Import handwritten implementation
        from stellarator_materials_nb3sn_tea.handwritten.mfe_matched_steam_cycle.matched_steam_cycle_impl import (
            run_matched_steam_cycle,
        )

        # Execute implementation - returns tuple of values
        s_main_kJ_kgK, reheat_min_gap_K, mdot_heater_kg_s, h_hp_kJ_kg, s_lp_kJ_kgK, p_condensate_pumped_MPa, mdot_main_kg_s, mdot_reheat_kg_s, q_generator_loss_MW, t_feed_C, p_cycle_net_before_cooling_MW, main_UA_available, p_feedwater_electric_MW, q_rejection_before_cooling_MW, p_lp_MPa, lp_quality, h_condensate_pumped_kJ_kg, t_heater_C, p_cycle_pumps_MW, t_condensate_C, salt_reheat_flow_kg_s, s_reheat_kJ_kgK, salt_main_flow_kg_s, p_gross_MW, p_feedwater_shaft_MW, h_main_kJ_kg, t_reheat_C, installed_sg_capacity_qualified, p_hp_shaft_MW, p_main_MPa, t_hp_C, mdot_feed_kg_s, mdot_bleed_kg_s, p_condensate_MPa, salt_heat_residual_MW, p_hp_MPa, active, eta_gross, h_lp_kJ_kg, mdot_condensate_kg_s, h_feed_kJ_kg, heater_energy_residual_MW, lp_moisture_fraction, t_main_C, cycle_electric_residual_MW, p_feed_MPa, main_UA_MW_K, bleed_fraction, p_reheat_MPa, mdot_lp_kg_s, reheat_UA_MW_K, p_lp_shaft_MW, p_heater_MPa, q_main_MW, q_pump_motor_loss_MW, q_mechanical_loss_MW, p_condensate_electric_MW, main_min_gap_K, heater_mass_residual_kg_s, s_hp_kJ_kgK, h_heater_kJ_kg, main_admission_ok, q_condenser_MW, mdot_hp_kg_s, h_condensate_kJ_kg, p_condensate_shaft_MW, turbine_equipment_qualified, h_reheat_kJ_kg, cycle_shaft_residual_MW, reheat_admission_ok, s_heater_kJ_kgK, q_reheat_MW, s_feed_kJ_kgK, salt_flow_total_kg_s, reheat_UA_available, s_condensate_kJ_kgK, mdot_condensate_pumped_kg_s, t_lp_C = run_matched_steam_cycle(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Matched_Steam_CycleOutput(
                s_main_kJ_kgK=s_main_kJ_kgK,
                reheat_min_gap_K=reheat_min_gap_K,
                mdot_heater_kg_s=mdot_heater_kg_s,
                h_hp_kJ_kg=h_hp_kJ_kg,
                s_lp_kJ_kgK=s_lp_kJ_kgK,
                p_condensate_pumped_MPa=p_condensate_pumped_MPa,
                mdot_main_kg_s=mdot_main_kg_s,
                mdot_reheat_kg_s=mdot_reheat_kg_s,
                q_generator_loss_MW=q_generator_loss_MW,
                t_feed_C=t_feed_C,
                p_cycle_net_before_cooling_MW=p_cycle_net_before_cooling_MW,
                main_UA_available=main_UA_available,
                p_feedwater_electric_MW=p_feedwater_electric_MW,
                q_rejection_before_cooling_MW=q_rejection_before_cooling_MW,
                p_lp_MPa=p_lp_MPa,
                lp_quality=lp_quality,
                h_condensate_pumped_kJ_kg=h_condensate_pumped_kJ_kg,
                t_heater_C=t_heater_C,
                p_cycle_pumps_MW=p_cycle_pumps_MW,
                t_condensate_C=t_condensate_C,
                salt_reheat_flow_kg_s=salt_reheat_flow_kg_s,
                s_reheat_kJ_kgK=s_reheat_kJ_kgK,
                salt_main_flow_kg_s=salt_main_flow_kg_s,
                p_gross_MW=p_gross_MW,
                p_feedwater_shaft_MW=p_feedwater_shaft_MW,
                h_main_kJ_kg=h_main_kJ_kg,
                t_reheat_C=t_reheat_C,
                installed_sg_capacity_qualified=installed_sg_capacity_qualified,
                p_hp_shaft_MW=p_hp_shaft_MW,
                p_main_MPa=p_main_MPa,
                t_hp_C=t_hp_C,
                mdot_feed_kg_s=mdot_feed_kg_s,
                mdot_bleed_kg_s=mdot_bleed_kg_s,
                p_condensate_MPa=p_condensate_MPa,
                salt_heat_residual_MW=salt_heat_residual_MW,
                p_hp_MPa=p_hp_MPa,
                active=active,
                eta_gross=eta_gross,
                h_lp_kJ_kg=h_lp_kJ_kg,
                mdot_condensate_kg_s=mdot_condensate_kg_s,
                h_feed_kJ_kg=h_feed_kJ_kg,
                heater_energy_residual_MW=heater_energy_residual_MW,
                lp_moisture_fraction=lp_moisture_fraction,
                t_main_C=t_main_C,
                cycle_electric_residual_MW=cycle_electric_residual_MW,
                p_feed_MPa=p_feed_MPa,
                main_UA_MW_K=main_UA_MW_K,
                bleed_fraction=bleed_fraction,
                p_reheat_MPa=p_reheat_MPa,
                mdot_lp_kg_s=mdot_lp_kg_s,
                reheat_UA_MW_K=reheat_UA_MW_K,
                p_lp_shaft_MW=p_lp_shaft_MW,
                p_heater_MPa=p_heater_MPa,
                q_main_MW=q_main_MW,
                q_pump_motor_loss_MW=q_pump_motor_loss_MW,
                q_mechanical_loss_MW=q_mechanical_loss_MW,
                p_condensate_electric_MW=p_condensate_electric_MW,
                main_min_gap_K=main_min_gap_K,
                heater_mass_residual_kg_s=heater_mass_residual_kg_s,
                s_hp_kJ_kgK=s_hp_kJ_kgK,
                h_heater_kJ_kg=h_heater_kJ_kg,
                main_admission_ok=main_admission_ok,
                q_condenser_MW=q_condenser_MW,
                mdot_hp_kg_s=mdot_hp_kg_s,
                h_condensate_kJ_kg=h_condensate_kJ_kg,
                p_condensate_shaft_MW=p_condensate_shaft_MW,
                turbine_equipment_qualified=turbine_equipment_qualified,
                h_reheat_kJ_kg=h_reheat_kJ_kg,
                cycle_shaft_residual_MW=cycle_shaft_residual_MW,
                reheat_admission_ok=reheat_admission_ok,
                s_heater_kJ_kgK=s_heater_kJ_kgK,
                q_reheat_MW=q_reheat_MW,
                s_feed_kJ_kgK=s_feed_kJ_kgK,
                salt_flow_total_kg_s=salt_flow_total_kg_s,
                reheat_UA_available=reheat_UA_available,
                s_condensate_kJ_kgK=s_condensate_kJ_kgK,
                mdot_condensate_pumped_kg_s=mdot_condensate_pumped_kg_s,
                t_lp_C=t_lp_C,
            )
        )
