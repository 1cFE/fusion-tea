"""Controlled_Network_Heat_Driven_ClosureModule Module Wrapper

TEAx module for Controlled_Network_Heat_Driven_Closure calculation.

Native selectable legacy or constant-U primary-bypass closure. Full delivered duty fixes required hot temperature from the supplied aggregate return; actual accepted duty closes the cycle and exposes unmet heat. Active HX outlet and mixed loop return are distinct. Mode 0 preserves reviewed legacy arithmetic. **Source**: work/active/WI-097_exchanger-thermal-requirements/design.md. **Reference**: controlled branch equations, coupled cycle closure, domains and exact-return/30 K conditional requirements; original source interpretation in work/orchestration/goals/design-study-exchanger-architecture/evidence/r2-thermal-requirements.md. Units: MW, K, MPa, kg/s, J/(kg K), MW/K; fractions and modes dimensionless. **Last Updated**: 2026-09-27.

Inputs:
    - pbli_cp_in: pbli_cp_in parameter
    - divertor_available_in: divertor_available_in parameter
    - pbli_ua_in: pbli_ua_in parameter
    - cp_in: cp_in parameter
    - pbli_limit_in: pbli_limit_in parameter
    - he_required_return_in: he_required_return_in parameter
    - control_mode_in: control_mode_in parameter
    - pbli_cold_approach_in: pbli_cold_approach_in parameter
    - pbli_hot_approach_in: pbli_hot_approach_in parameter
    - divertor_flow_in: divertor_flow_in parameter
    - divertor_cold_approach_in: divertor_cold_approach_in parameter
    - gamma_in: gamma_in parameter
    - he_hot_approach_in: he_hot_approach_in parameter
    - turbine_pressure_in: turbine_pressure_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - divertor_required_return_in: divertor_required_return_in parameter
    - divertor_cp_in: divertor_cp_in parameter
    - divertor_hot_approach_in: divertor_hot_approach_in parameter
    - return_pressure_in: return_pressure_in parameter
    - he_limit_in: he_limit_in parameter
    - pbli_flow_in: pbli_flow_in parameter
    - divertor_max_bypass_in: divertor_max_bypass_in parameter
    - he_max_bypass_in: he_max_bypass_in parameter
    - turbine_efficiency_in: turbine_efficiency_in parameter
    - pbli_available_in: pbli_available_in parameter
    - he_available_in: he_available_in parameter
    - divertor_limit_in: divertor_limit_in parameter
    - pbli_max_bypass_in: pbli_max_bypass_in parameter
    - recuperator_effectiveness_in: recuperator_effectiveness_in parameter
    - flow_in: flow_in parameter
    - he_ua_in: he_ua_in parameter
    - he_cp_in: he_cp_in parameter
    - pbli_required_return_in: pbli_required_return_in parameter
    - he_cold_approach_in: he_cold_approach_in parameter
    - divertor_ua_in: divertor_ua_in parameter
    - pbli_split_in: pbli_split_in parameter
    - he_flow_in: he_flow_in parameter
    - network_mode_in: network_mode_in parameter
    - return_tolerance_in: return_tolerance_in parameter

Outputs:
    - pbli_secondary_in: pbli_secondary_in result
    - he_hx_return: he_hx_return result
    - pbli_hot: pbli_hot result
    - he_secondary_in: he_secondary_in result
    - pbli_cold_approach_margin: pbli_cold_approach_margin result
    - mixed_outlet: mixed_outlet result
    - pbli_split_used: pbli_split_used result
    - he_return_residual_magnitude: he_return_residual_magnitude result
    - heater_inlet: heater_inlet result
    - pbli_capability_at_solution: pbli_capability_at_solution result
    - pbli_cold_terminal_difference: pbli_cold_terminal_difference result
    - pbli_capability: pbli_capability result
    - divertor_secondary_out: divertor_secondary_out result
    - divertor_cold_approach_margin: divertor_cold_approach_margin result
    - divertor_hot: divertor_hot result
    - divertor_required_hot: divertor_required_hot result
    - he_cold_approach_margin: he_cold_approach_margin result
    - divertor_transferred: divertor_transferred result
    - pbli_return_residual: pbli_return_residual result
    - pbli_return_residual_magnitude: pbli_return_residual_magnitude result
    - divertor_stream_out: divertor_stream_out result
    - divertor_return_residual: divertor_return_residual result
    - divertor_state_defined: divertor_state_defined result
    - pbli_active_flow: pbli_active_flow result
    - network_mode_used: network_mode_used result
    - divertor_hx_return: divertor_hx_return result
    - pbli_return: pbli_return result
    - divertor_cold_terminal_difference: divertor_cold_terminal_difference result
    - unmet_heat: unmet_heat result
    - iterations: iterations result
    - he_state_defined: he_state_defined result
    - divertor_mixed_return: divertor_mixed_return result
    - divertor_unmet: divertor_unmet result
    - pbli_hot_terminal_difference: pbli_hot_terminal_difference result
    - pbli_secondary_out: pbli_secondary_out result
    - accepted_heat: accepted_heat result
    - divertor_hot_approach_margin: divertor_hot_approach_margin result
    - turbine_temperature: turbine_temperature result
    - pbli_mixed_return: pbli_mixed_return result
    - divertor_active_flow: divertor_active_flow result
    - he_active_flow: he_active_flow result
    - divertor_return: divertor_return result
    - pbli_state_defined: pbli_state_defined result
    - pbli_required_hot_margin: pbli_required_hot_margin result
    - he_transferred: he_transferred result
    - he_hot_terminal_difference: he_hot_terminal_difference result
    - divertor_hot_bound_margin: divertor_hot_bound_margin result
    - he_capability: he_capability result
    - he_hot_bound_margin: he_hot_bound_margin result
    - he_capability_at_solution: he_capability_at_solution result
    - he_cold_terminal_difference: he_cold_terminal_difference result
    - pbli_transferred: pbli_transferred result
    - divertor_secondary_in: divertor_secondary_in result
    - he_mixed_return: he_mixed_return result
    - he_required_hot_margin: he_required_hot_margin result
    - divertor_capability_at_solution: divertor_capability_at_solution result
    - pbli_stream_out: pbli_stream_out result
    - pbli_hx_return: pbli_hx_return result
    - he_secondary_out: he_secondary_out result
    - he_hot: he_hot result
    - he_hot_approach_margin: he_hot_approach_margin result
    - pbli_hot_approach_margin: pbli_hot_approach_margin result
    - divertor_return_residual_magnitude: divertor_return_residual_magnitude result
    - he_return: he_return result
    - divertor_required_hot_margin: divertor_required_hot_margin result
    - he_return_residual: he_return_residual result
    - pbli_control_margin: pbli_control_margin result
    - he_bypass_fraction: he_bypass_fraction result
    - he_control_margin: he_control_margin result
    - pbli_unmet: pbli_unmet result
    - divertor_bypass_fraction: divertor_bypass_fraction result
    - he_unmet: he_unmet result
    - divertor_control_margin: divertor_control_margin result
    - divertor_capability: divertor_capability result
    - divertor_hot_terminal_difference: divertor_hot_terminal_difference result
    - expansion_factor: expansion_factor result
    - closure_residual: closure_residual result
    - he_required_hot: he_required_hot result
    - control_mode_used: control_mode_used result
    - pbli_bypass_fraction: pbli_bypass_fraction result
    - pbli_required_hot: pbli_required_hot result
    - pbli_hot_bound_margin: pbli_hot_bound_margin result

SysML Source: root-0/controlled_exchanger_closure.sysml:3

SysML Source: root-0/controlled_exchanger_closure.sysml:3

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/controlled_exchanger_closure/controlled_network_heat_driven_closure_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.primitives import Float
from exchanger_architecture_thermal_tea.schemas.controlled_network_heat_driven_closure_output import Controlled_Network_Heat_Driven_ClosureOutput


class Controlled_Network_Heat_Driven_ClosureInput(BaseModel):
    """Input model for Controlled_Network_Heat_Driven_ClosureModule.

    Attributes:
        pbli_cp_in: pbli_cp_in input
        divertor_available_in: divertor_available_in input
        pbli_ua_in: pbli_ua_in input
        cp_in: cp_in input
        pbli_limit_in: pbli_limit_in input
        he_required_return_in: he_required_return_in input
        control_mode_in: control_mode_in input
        pbli_cold_approach_in: pbli_cold_approach_in input
        pbli_hot_approach_in: pbli_hot_approach_in input
        divertor_flow_in: divertor_flow_in input
        divertor_cold_approach_in: divertor_cold_approach_in input
        gamma_in: gamma_in input
        he_hot_approach_in: he_hot_approach_in input
        turbine_pressure_in: turbine_pressure_in input
        cold_temperature_in: cold_temperature_in input
        divertor_required_return_in: divertor_required_return_in input
        divertor_cp_in: divertor_cp_in input
        divertor_hot_approach_in: divertor_hot_approach_in input
        return_pressure_in: return_pressure_in input
        he_limit_in: he_limit_in input
        pbli_flow_in: pbli_flow_in input
        divertor_max_bypass_in: divertor_max_bypass_in input
        he_max_bypass_in: he_max_bypass_in input
        turbine_efficiency_in: turbine_efficiency_in input
        pbli_available_in: pbli_available_in input
        he_available_in: he_available_in input
        divertor_limit_in: divertor_limit_in input
        pbli_max_bypass_in: pbli_max_bypass_in input
        recuperator_effectiveness_in: recuperator_effectiveness_in input
        flow_in: flow_in input
        he_ua_in: he_ua_in input
        he_cp_in: he_cp_in input
        pbli_required_return_in: pbli_required_return_in input
        he_cold_approach_in: he_cold_approach_in input
        divertor_ua_in: divertor_ua_in input
        pbli_split_in: pbli_split_in input
        he_flow_in: he_flow_in input
        network_mode_in: network_mode_in input
        return_tolerance_in: return_tolerance_in input
    """
    pbli_cp_in: float = Field(..., description="pbli_cp_in input")
    divertor_available_in: float = Field(..., description="divertor_available_in input")
    pbli_ua_in: float = Field(..., description="pbli_ua_in input")
    cp_in: float = Field(..., description="cp_in input")
    pbli_limit_in: float = Field(..., description="pbli_limit_in input")
    he_required_return_in: float = Field(..., description="he_required_return_in input")
    control_mode_in: float = Field(..., description="control_mode_in input")
    pbli_cold_approach_in: float = Field(..., description="pbli_cold_approach_in input")
    pbli_hot_approach_in: float = Field(..., description="pbli_hot_approach_in input")
    divertor_flow_in: float = Field(..., description="divertor_flow_in input")
    divertor_cold_approach_in: float = Field(..., description="divertor_cold_approach_in input")
    gamma_in: float = Field(..., description="gamma_in input")
    he_hot_approach_in: float = Field(..., description="he_hot_approach_in input")
    turbine_pressure_in: float = Field(..., description="turbine_pressure_in input")
    cold_temperature_in: float = Field(..., description="cold_temperature_in input")
    divertor_required_return_in: float = Field(..., description="divertor_required_return_in input")
    divertor_cp_in: float = Field(..., description="divertor_cp_in input")
    divertor_hot_approach_in: float = Field(..., description="divertor_hot_approach_in input")
    return_pressure_in: float = Field(..., description="return_pressure_in input")
    he_limit_in: float = Field(..., description="he_limit_in input")
    pbli_flow_in: float = Field(..., description="pbli_flow_in input")
    divertor_max_bypass_in: float = Field(..., description="divertor_max_bypass_in input")
    he_max_bypass_in: float = Field(..., description="he_max_bypass_in input")
    turbine_efficiency_in: float = Field(..., description="turbine_efficiency_in input")
    pbli_available_in: float = Field(..., description="pbli_available_in input")
    he_available_in: float = Field(..., description="he_available_in input")
    divertor_limit_in: float = Field(..., description="divertor_limit_in input")
    pbli_max_bypass_in: float = Field(..., description="pbli_max_bypass_in input")
    recuperator_effectiveness_in: float = Field(..., description="recuperator_effectiveness_in input")
    flow_in: float = Field(..., description="flow_in input")
    he_ua_in: float = Field(..., description="he_ua_in input")
    he_cp_in: float = Field(..., description="he_cp_in input")
    pbli_required_return_in: float = Field(..., description="pbli_required_return_in input")
    he_cold_approach_in: float = Field(..., description="he_cold_approach_in input")
    divertor_ua_in: float = Field(..., description="divertor_ua_in input")
    pbli_split_in: float = Field(..., description="pbli_split_in input")
    he_flow_in: float = Field(..., description="he_flow_in input")
    network_mode_in: float = Field(..., description="network_mode_in input")
    return_tolerance_in: float = Field(..., description="return_tolerance_in input")


class Controlled_Network_Heat_Driven_ClosureModule(ModuleBase[Controlled_Network_Heat_Driven_ClosureInput, Controlled_Network_Heat_Driven_ClosureOutput]):
    """TEAx module for Controlled_Network_Heat_Driven_Closure calculation.

Native selectable legacy or constant-U primary-bypass closure. Full delivered duty fixes required hot temperature from the supplied aggregate return; actual accepted duty closes the cycle and exposes unmet heat. Active HX outlet and mixed loop return are distinct. Mode 0 preserves reviewed legacy arithmetic. **Source**: work/active/WI-097_exchanger-thermal-requirements/design.md. **Reference**: controlled branch equations, coupled cycle closure, domains and exact-return/30 K conditional requirements; original source interpretation in work/orchestration/goals/design-study-exchanger-architecture/evidence/r2-thermal-requirements.md. Units: MW, K, MPa, kg/s, J/(kg K), MW/K; fractions and modes dimensionless. **Last Updated**: 2026-09-27.

Inputs:
    - pbli_cp_in: pbli_cp_in parameter
    - divertor_available_in: divertor_available_in parameter
    - pbli_ua_in: pbli_ua_in parameter
    - cp_in: cp_in parameter
    - pbli_limit_in: pbli_limit_in parameter
    - he_required_return_in: he_required_return_in parameter
    - control_mode_in: control_mode_in parameter
    - pbli_cold_approach_in: pbli_cold_approach_in parameter
    - pbli_hot_approach_in: pbli_hot_approach_in parameter
    - divertor_flow_in: divertor_flow_in parameter
    - divertor_cold_approach_in: divertor_cold_approach_in parameter
    - gamma_in: gamma_in parameter
    - he_hot_approach_in: he_hot_approach_in parameter
    - turbine_pressure_in: turbine_pressure_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - divertor_required_return_in: divertor_required_return_in parameter
    - divertor_cp_in: divertor_cp_in parameter
    - divertor_hot_approach_in: divertor_hot_approach_in parameter
    - return_pressure_in: return_pressure_in parameter
    - he_limit_in: he_limit_in parameter
    - pbli_flow_in: pbli_flow_in parameter
    - divertor_max_bypass_in: divertor_max_bypass_in parameter
    - he_max_bypass_in: he_max_bypass_in parameter
    - turbine_efficiency_in: turbine_efficiency_in parameter
    - pbli_available_in: pbli_available_in parameter
    - he_available_in: he_available_in parameter
    - divertor_limit_in: divertor_limit_in parameter
    - pbli_max_bypass_in: pbli_max_bypass_in parameter
    - recuperator_effectiveness_in: recuperator_effectiveness_in parameter
    - flow_in: flow_in parameter
    - he_ua_in: he_ua_in parameter
    - he_cp_in: he_cp_in parameter
    - pbli_required_return_in: pbli_required_return_in parameter
    - he_cold_approach_in: he_cold_approach_in parameter
    - divertor_ua_in: divertor_ua_in parameter
    - pbli_split_in: pbli_split_in parameter
    - he_flow_in: he_flow_in parameter
    - network_mode_in: network_mode_in parameter
    - return_tolerance_in: return_tolerance_in parameter

Outputs:
    - pbli_secondary_in: pbli_secondary_in result
    - he_hx_return: he_hx_return result
    - pbli_hot: pbli_hot result
    - he_secondary_in: he_secondary_in result
    - pbli_cold_approach_margin: pbli_cold_approach_margin result
    - mixed_outlet: mixed_outlet result
    - pbli_split_used: pbli_split_used result
    - he_return_residual_magnitude: he_return_residual_magnitude result
    - heater_inlet: heater_inlet result
    - pbli_capability_at_solution: pbli_capability_at_solution result
    - pbli_cold_terminal_difference: pbli_cold_terminal_difference result
    - pbli_capability: pbli_capability result
    - divertor_secondary_out: divertor_secondary_out result
    - divertor_cold_approach_margin: divertor_cold_approach_margin result
    - divertor_hot: divertor_hot result
    - divertor_required_hot: divertor_required_hot result
    - he_cold_approach_margin: he_cold_approach_margin result
    - divertor_transferred: divertor_transferred result
    - pbli_return_residual: pbli_return_residual result
    - pbli_return_residual_magnitude: pbli_return_residual_magnitude result
    - divertor_stream_out: divertor_stream_out result
    - divertor_return_residual: divertor_return_residual result
    - divertor_state_defined: divertor_state_defined result
    - pbli_active_flow: pbli_active_flow result
    - network_mode_used: network_mode_used result
    - divertor_hx_return: divertor_hx_return result
    - pbli_return: pbli_return result
    - divertor_cold_terminal_difference: divertor_cold_terminal_difference result
    - unmet_heat: unmet_heat result
    - iterations: iterations result
    - he_state_defined: he_state_defined result
    - divertor_mixed_return: divertor_mixed_return result
    - divertor_unmet: divertor_unmet result
    - pbli_hot_terminal_difference: pbli_hot_terminal_difference result
    - pbli_secondary_out: pbli_secondary_out result
    - accepted_heat: accepted_heat result
    - divertor_hot_approach_margin: divertor_hot_approach_margin result
    - turbine_temperature: turbine_temperature result
    - pbli_mixed_return: pbli_mixed_return result
    - divertor_active_flow: divertor_active_flow result
    - he_active_flow: he_active_flow result
    - divertor_return: divertor_return result
    - pbli_state_defined: pbli_state_defined result
    - pbli_required_hot_margin: pbli_required_hot_margin result
    - he_transferred: he_transferred result
    - he_hot_terminal_difference: he_hot_terminal_difference result
    - divertor_hot_bound_margin: divertor_hot_bound_margin result
    - he_capability: he_capability result
    - he_hot_bound_margin: he_hot_bound_margin result
    - he_capability_at_solution: he_capability_at_solution result
    - he_cold_terminal_difference: he_cold_terminal_difference result
    - pbli_transferred: pbli_transferred result
    - divertor_secondary_in: divertor_secondary_in result
    - he_mixed_return: he_mixed_return result
    - he_required_hot_margin: he_required_hot_margin result
    - divertor_capability_at_solution: divertor_capability_at_solution result
    - pbli_stream_out: pbli_stream_out result
    - pbli_hx_return: pbli_hx_return result
    - he_secondary_out: he_secondary_out result
    - he_hot: he_hot result
    - he_hot_approach_margin: he_hot_approach_margin result
    - pbli_hot_approach_margin: pbli_hot_approach_margin result
    - divertor_return_residual_magnitude: divertor_return_residual_magnitude result
    - he_return: he_return result
    - divertor_required_hot_margin: divertor_required_hot_margin result
    - he_return_residual: he_return_residual result
    - pbli_control_margin: pbli_control_margin result
    - he_bypass_fraction: he_bypass_fraction result
    - he_control_margin: he_control_margin result
    - pbli_unmet: pbli_unmet result
    - divertor_bypass_fraction: divertor_bypass_fraction result
    - he_unmet: he_unmet result
    - divertor_control_margin: divertor_control_margin result
    - divertor_capability: divertor_capability result
    - divertor_hot_terminal_difference: divertor_hot_terminal_difference result
    - expansion_factor: expansion_factor result
    - closure_residual: closure_residual result
    - he_required_hot: he_required_hot result
    - control_mode_used: control_mode_used result
    - pbli_bypass_fraction: pbli_bypass_fraction result
    - pbli_required_hot: pbli_required_hot result
    - pbli_hot_bound_margin: pbli_hot_bound_margin result

SysML Source: root-0/controlled_exchanger_closure.sysml:3

    SysML Source: root-0/controlled_exchanger_closure.sysml:3

    Calculation Specification:
        See documentation:
Native selectable legacy or constant-U primary-bypass closure. Full delivered duty fixes required hot temperature from the supplied aggregate return; actual accepted duty closes the cycle and exposes unmet heat. Active HX outlet and mixed loop return are distinct. Mode 0 preserves reviewed legacy arithmetic. **Source**: work/active/WI-097_exchanger-thermal-requirements/design.md. **Reference**: controlled branch equations, coupled cycle closure, domains and exact-return/30 K conditional requirements; original source interpretation in work/orchestration/goals/design-study-exchanger-architecture/evidence/r2-thermal-requirements.md. Units: MW, K, MPa, kg/s, J/(kg K), MW/K; fractions and modes dimensionless. **Last Updated**: 2026-09-27.

    IMPLEMENTATION: See exchanger_architecture_thermal_tea.handwritten.controlled_exchanger_closure.controlled_network_heat_driven_closure_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts pbli_secondary_in, he_hx_return, pbli_hot, he_secondary_in, pbli_cold_approach_margin, mixed_outlet, pbli_split_used, he_return_residual_magnitude, heater_inlet, pbli_capability_at_solution, pbli_cold_terminal_difference, pbli_capability, divertor_secondary_out, divertor_cold_approach_margin, divertor_hot, divertor_required_hot, he_cold_approach_margin, divertor_transferred, pbli_return_residual, pbli_return_residual_magnitude, divertor_stream_out, divertor_return_residual, divertor_state_defined, pbli_active_flow, network_mode_used, divertor_hx_return, pbli_return, divertor_cold_terminal_difference, unmet_heat, iterations, he_state_defined, divertor_mixed_return, divertor_unmet, pbli_hot_terminal_difference, pbli_secondary_out, accepted_heat, divertor_hot_approach_margin, turbine_temperature, pbli_mixed_return, divertor_active_flow, he_active_flow, divertor_return, pbli_state_defined, pbli_required_hot_margin, he_transferred, he_hot_terminal_difference, divertor_hot_bound_margin, he_capability, he_hot_bound_margin, he_capability_at_solution, he_cold_terminal_difference, pbli_transferred, divertor_secondary_in, he_mixed_return, he_required_hot_margin, divertor_capability_at_solution, pbli_stream_out, pbli_hx_return, he_secondary_out, he_hot, he_hot_approach_margin, pbli_hot_approach_margin, divertor_return_residual_magnitude, he_return, divertor_required_hot_margin, he_return_residual, pbli_control_margin, he_bypass_fraction, he_control_margin, pbli_unmet, divertor_bypass_fraction, he_unmet, divertor_control_margin, divertor_capability, divertor_hot_terminal_difference, expansion_factor, closure_residual, he_required_hot, control_mode_used, pbli_bypass_fraction, pbli_required_hot, pbli_hot_bound_margin fields to separate channels.
    """

    name: str = "Controlled_Network_Heat_Driven_ClosureModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pbli_cp_in: float, divertor_available_in: float, pbli_ua_in: float, cp_in: float, pbli_limit_in: float, he_required_return_in: float, control_mode_in: float, pbli_cold_approach_in: float, pbli_hot_approach_in: float, divertor_flow_in: float, divertor_cold_approach_in: float, gamma_in: float, he_hot_approach_in: float, turbine_pressure_in: float, cold_temperature_in: float, divertor_required_return_in: float, divertor_cp_in: float, divertor_hot_approach_in: float, return_pressure_in: float, he_limit_in: float, pbli_flow_in: float, divertor_max_bypass_in: float, he_max_bypass_in: float, turbine_efficiency_in: float, pbli_available_in: float, he_available_in: float, divertor_limit_in: float, pbli_max_bypass_in: float, recuperator_effectiveness_in: float, flow_in: float, he_ua_in: float, he_cp_in: float, pbli_required_return_in: float, he_cold_approach_in: float, divertor_ua_in: float, pbli_split_in: float, he_flow_in: float, network_mode_in: float, return_tolerance_in: float    ) -> Controlled_Network_Heat_Driven_ClosureInput:
        """Validate inputs and fill defaults.

        Args:
            pbli_cp_in: pbli_cp_in input
            divertor_available_in: divertor_available_in input
            pbli_ua_in: pbli_ua_in input
            cp_in: cp_in input
            pbli_limit_in: pbli_limit_in input
            he_required_return_in: he_required_return_in input
            control_mode_in: control_mode_in input
            pbli_cold_approach_in: pbli_cold_approach_in input
            pbli_hot_approach_in: pbli_hot_approach_in input
            divertor_flow_in: divertor_flow_in input
            divertor_cold_approach_in: divertor_cold_approach_in input
            gamma_in: gamma_in input
            he_hot_approach_in: he_hot_approach_in input
            turbine_pressure_in: turbine_pressure_in input
            cold_temperature_in: cold_temperature_in input
            divertor_required_return_in: divertor_required_return_in input
            divertor_cp_in: divertor_cp_in input
            divertor_hot_approach_in: divertor_hot_approach_in input
            return_pressure_in: return_pressure_in input
            he_limit_in: he_limit_in input
            pbli_flow_in: pbli_flow_in input
            divertor_max_bypass_in: divertor_max_bypass_in input
            he_max_bypass_in: he_max_bypass_in input
            turbine_efficiency_in: turbine_efficiency_in input
            pbli_available_in: pbli_available_in input
            he_available_in: he_available_in input
            divertor_limit_in: divertor_limit_in input
            pbli_max_bypass_in: pbli_max_bypass_in input
            recuperator_effectiveness_in: recuperator_effectiveness_in input
            flow_in: flow_in input
            he_ua_in: he_ua_in input
            he_cp_in: he_cp_in input
            pbli_required_return_in: pbli_required_return_in input
            he_cold_approach_in: he_cold_approach_in input
            divertor_ua_in: divertor_ua_in input
            pbli_split_in: pbli_split_in input
            he_flow_in: he_flow_in input
            network_mode_in: network_mode_in input
            return_tolerance_in: return_tolerance_in input

        Returns:
            Validated input model
        """
        return Controlled_Network_Heat_Driven_ClosureInput(pbli_cp_in=pbli_cp_in, divertor_available_in=divertor_available_in, pbli_ua_in=pbli_ua_in, cp_in=cp_in, pbli_limit_in=pbli_limit_in, he_required_return_in=he_required_return_in, control_mode_in=control_mode_in, pbli_cold_approach_in=pbli_cold_approach_in, pbli_hot_approach_in=pbli_hot_approach_in, divertor_flow_in=divertor_flow_in, divertor_cold_approach_in=divertor_cold_approach_in, gamma_in=gamma_in, he_hot_approach_in=he_hot_approach_in, turbine_pressure_in=turbine_pressure_in, cold_temperature_in=cold_temperature_in, divertor_required_return_in=divertor_required_return_in, divertor_cp_in=divertor_cp_in, divertor_hot_approach_in=divertor_hot_approach_in, return_pressure_in=return_pressure_in, he_limit_in=he_limit_in, pbli_flow_in=pbli_flow_in, divertor_max_bypass_in=divertor_max_bypass_in, he_max_bypass_in=he_max_bypass_in, turbine_efficiency_in=turbine_efficiency_in, pbli_available_in=pbli_available_in, he_available_in=he_available_in, divertor_limit_in=divertor_limit_in, pbli_max_bypass_in=pbli_max_bypass_in, recuperator_effectiveness_in=recuperator_effectiveness_in, flow_in=flow_in, he_ua_in=he_ua_in, he_cp_in=he_cp_in, pbli_required_return_in=pbli_required_return_in, he_cold_approach_in=he_cold_approach_in, divertor_ua_in=divertor_ua_in, pbli_split_in=pbli_split_in, he_flow_in=he_flow_in, network_mode_in=network_mode_in, return_tolerance_in=return_tolerance_in)

    def run(
        self, pbli_cp_in: float, divertor_available_in: float, pbli_ua_in: float, cp_in: float, pbli_limit_in: float, he_required_return_in: float, control_mode_in: float, pbli_cold_approach_in: float, pbli_hot_approach_in: float, divertor_flow_in: float, divertor_cold_approach_in: float, gamma_in: float, he_hot_approach_in: float, turbine_pressure_in: float, cold_temperature_in: float, divertor_required_return_in: float, divertor_cp_in: float, divertor_hot_approach_in: float, return_pressure_in: float, he_limit_in: float, pbli_flow_in: float, divertor_max_bypass_in: float, he_max_bypass_in: float, turbine_efficiency_in: float, pbli_available_in: float, he_available_in: float, divertor_limit_in: float, pbli_max_bypass_in: float, recuperator_effectiveness_in: float, flow_in: float, he_ua_in: float, he_cp_in: float, pbli_required_return_in: float, he_cold_approach_in: float, divertor_ua_in: float, pbli_split_in: float, he_flow_in: float, network_mode_in: float, return_tolerance_in: float    ) -> ModuleResult[Controlled_Network_Heat_Driven_ClosureOutput]:
        """Execute calculation.

        Args:
            pbli_cp_in: pbli_cp_in input
            divertor_available_in: divertor_available_in input
            pbli_ua_in: pbli_ua_in input
            cp_in: cp_in input
            pbli_limit_in: pbli_limit_in input
            he_required_return_in: he_required_return_in input
            control_mode_in: control_mode_in input
            pbli_cold_approach_in: pbli_cold_approach_in input
            pbli_hot_approach_in: pbli_hot_approach_in input
            divertor_flow_in: divertor_flow_in input
            divertor_cold_approach_in: divertor_cold_approach_in input
            gamma_in: gamma_in input
            he_hot_approach_in: he_hot_approach_in input
            turbine_pressure_in: turbine_pressure_in input
            cold_temperature_in: cold_temperature_in input
            divertor_required_return_in: divertor_required_return_in input
            divertor_cp_in: divertor_cp_in input
            divertor_hot_approach_in: divertor_hot_approach_in input
            return_pressure_in: return_pressure_in input
            he_limit_in: he_limit_in input
            pbli_flow_in: pbli_flow_in input
            divertor_max_bypass_in: divertor_max_bypass_in input
            he_max_bypass_in: he_max_bypass_in input
            turbine_efficiency_in: turbine_efficiency_in input
            pbli_available_in: pbli_available_in input
            he_available_in: he_available_in input
            divertor_limit_in: divertor_limit_in input
            pbli_max_bypass_in: pbli_max_bypass_in input
            recuperator_effectiveness_in: recuperator_effectiveness_in input
            flow_in: flow_in input
            he_ua_in: he_ua_in input
            he_cp_in: he_cp_in input
            pbli_required_return_in: pbli_required_return_in input
            he_cold_approach_in: he_cold_approach_in input
            divertor_ua_in: divertor_ua_in input
            pbli_split_in: pbli_split_in input
            he_flow_in: he_flow_in input
            network_mode_in: network_mode_in input
            return_tolerance_in: return_tolerance_in input

        Returns:
            Module result with Controlled_Network_Heat_Driven_ClosureOutput (pbli_secondary_in, he_hx_return, pbli_hot, he_secondary_in, pbli_cold_approach_margin, mixed_outlet, pbli_split_used, he_return_residual_magnitude, heater_inlet, pbli_capability_at_solution, pbli_cold_terminal_difference, pbli_capability, divertor_secondary_out, divertor_cold_approach_margin, divertor_hot, divertor_required_hot, he_cold_approach_margin, divertor_transferred, pbli_return_residual, pbli_return_residual_magnitude, divertor_stream_out, divertor_return_residual, divertor_state_defined, pbli_active_flow, network_mode_used, divertor_hx_return, pbli_return, divertor_cold_terminal_difference, unmet_heat, iterations, he_state_defined, divertor_mixed_return, divertor_unmet, pbli_hot_terminal_difference, pbli_secondary_out, accepted_heat, divertor_hot_approach_margin, turbine_temperature, pbli_mixed_return, divertor_active_flow, he_active_flow, divertor_return, pbli_state_defined, pbli_required_hot_margin, he_transferred, he_hot_terminal_difference, divertor_hot_bound_margin, he_capability, he_hot_bound_margin, he_capability_at_solution, he_cold_terminal_difference, pbli_transferred, divertor_secondary_in, he_mixed_return, he_required_hot_margin, divertor_capability_at_solution, pbli_stream_out, pbli_hx_return, he_secondary_out, he_hot, he_hot_approach_margin, pbli_hot_approach_margin, divertor_return_residual_magnitude, he_return, divertor_required_hot_margin, he_return_residual, pbli_control_margin, he_bypass_fraction, he_control_margin, pbli_unmet, divertor_bypass_fraction, he_unmet, divertor_control_margin, divertor_capability, divertor_hot_terminal_difference, expansion_factor, closure_residual, he_required_hot, control_mode_used, pbli_bypass_fraction, pbli_required_hot, pbli_hot_bound_margin)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pbli_cp_in, divertor_available_in, pbli_ua_in, cp_in, pbli_limit_in, he_required_return_in, control_mode_in, pbli_cold_approach_in, pbli_hot_approach_in, divertor_flow_in, divertor_cold_approach_in, gamma_in, he_hot_approach_in, turbine_pressure_in, cold_temperature_in, divertor_required_return_in, divertor_cp_in, divertor_hot_approach_in, return_pressure_in, he_limit_in, pbli_flow_in, divertor_max_bypass_in, he_max_bypass_in, turbine_efficiency_in, pbli_available_in, he_available_in, divertor_limit_in, pbli_max_bypass_in, recuperator_effectiveness_in, flow_in, he_ua_in, he_cp_in, pbli_required_return_in, he_cold_approach_in, divertor_ua_in, pbli_split_in, he_flow_in, network_mode_in, return_tolerance_in)

        # Import handwritten implementation
        from exchanger_architecture_thermal_tea.handwritten.controlled_exchanger_closure.controlled_network_heat_driven_closure_impl import (
            run_controlled_network_heat_driven_closure,
        )

        # Execute implementation - returns tuple of values
        pbli_secondary_in, he_hx_return, pbli_hot, he_secondary_in, pbli_cold_approach_margin, mixed_outlet, pbli_split_used, he_return_residual_magnitude, heater_inlet, pbli_capability_at_solution, pbli_cold_terminal_difference, pbli_capability, divertor_secondary_out, divertor_cold_approach_margin, divertor_hot, divertor_required_hot, he_cold_approach_margin, divertor_transferred, pbli_return_residual, pbli_return_residual_magnitude, divertor_stream_out, divertor_return_residual, divertor_state_defined, pbli_active_flow, network_mode_used, divertor_hx_return, pbli_return, divertor_cold_terminal_difference, unmet_heat, iterations, he_state_defined, divertor_mixed_return, divertor_unmet, pbli_hot_terminal_difference, pbli_secondary_out, accepted_heat, divertor_hot_approach_margin, turbine_temperature, pbli_mixed_return, divertor_active_flow, he_active_flow, divertor_return, pbli_state_defined, pbli_required_hot_margin, he_transferred, he_hot_terminal_difference, divertor_hot_bound_margin, he_capability, he_hot_bound_margin, he_capability_at_solution, he_cold_terminal_difference, pbli_transferred, divertor_secondary_in, he_mixed_return, he_required_hot_margin, divertor_capability_at_solution, pbli_stream_out, pbli_hx_return, he_secondary_out, he_hot, he_hot_approach_margin, pbli_hot_approach_margin, divertor_return_residual_magnitude, he_return, divertor_required_hot_margin, he_return_residual, pbli_control_margin, he_bypass_fraction, he_control_margin, pbli_unmet, divertor_bypass_fraction, he_unmet, divertor_control_margin, divertor_capability, divertor_hot_terminal_difference, expansion_factor, closure_residual, he_required_hot, control_mode_used, pbli_bypass_fraction, pbli_required_hot, pbli_hot_bound_margin = run_controlled_network_heat_driven_closure(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Controlled_Network_Heat_Driven_ClosureOutput(
                pbli_secondary_in=pbli_secondary_in,
                he_hx_return=he_hx_return,
                pbli_hot=pbli_hot,
                he_secondary_in=he_secondary_in,
                pbli_cold_approach_margin=pbli_cold_approach_margin,
                mixed_outlet=mixed_outlet,
                pbli_split_used=pbli_split_used,
                he_return_residual_magnitude=he_return_residual_magnitude,
                heater_inlet=heater_inlet,
                pbli_capability_at_solution=pbli_capability_at_solution,
                pbli_cold_terminal_difference=pbli_cold_terminal_difference,
                pbli_capability=pbli_capability,
                divertor_secondary_out=divertor_secondary_out,
                divertor_cold_approach_margin=divertor_cold_approach_margin,
                divertor_hot=divertor_hot,
                divertor_required_hot=divertor_required_hot,
                he_cold_approach_margin=he_cold_approach_margin,
                divertor_transferred=divertor_transferred,
                pbli_return_residual=pbli_return_residual,
                pbli_return_residual_magnitude=pbli_return_residual_magnitude,
                divertor_stream_out=divertor_stream_out,
                divertor_return_residual=divertor_return_residual,
                divertor_state_defined=divertor_state_defined,
                pbli_active_flow=pbli_active_flow,
                network_mode_used=network_mode_used,
                divertor_hx_return=divertor_hx_return,
                pbli_return=pbli_return,
                divertor_cold_terminal_difference=divertor_cold_terminal_difference,
                unmet_heat=unmet_heat,
                iterations=iterations,
                he_state_defined=he_state_defined,
                divertor_mixed_return=divertor_mixed_return,
                divertor_unmet=divertor_unmet,
                pbli_hot_terminal_difference=pbli_hot_terminal_difference,
                pbli_secondary_out=pbli_secondary_out,
                accepted_heat=accepted_heat,
                divertor_hot_approach_margin=divertor_hot_approach_margin,
                turbine_temperature=turbine_temperature,
                pbli_mixed_return=pbli_mixed_return,
                divertor_active_flow=divertor_active_flow,
                he_active_flow=he_active_flow,
                divertor_return=divertor_return,
                pbli_state_defined=pbli_state_defined,
                pbli_required_hot_margin=pbli_required_hot_margin,
                he_transferred=he_transferred,
                he_hot_terminal_difference=he_hot_terminal_difference,
                divertor_hot_bound_margin=divertor_hot_bound_margin,
                he_capability=he_capability,
                he_hot_bound_margin=he_hot_bound_margin,
                he_capability_at_solution=he_capability_at_solution,
                he_cold_terminal_difference=he_cold_terminal_difference,
                pbli_transferred=pbli_transferred,
                divertor_secondary_in=divertor_secondary_in,
                he_mixed_return=he_mixed_return,
                he_required_hot_margin=he_required_hot_margin,
                divertor_capability_at_solution=divertor_capability_at_solution,
                pbli_stream_out=pbli_stream_out,
                pbli_hx_return=pbli_hx_return,
                he_secondary_out=he_secondary_out,
                he_hot=he_hot,
                he_hot_approach_margin=he_hot_approach_margin,
                pbli_hot_approach_margin=pbli_hot_approach_margin,
                divertor_return_residual_magnitude=divertor_return_residual_magnitude,
                he_return=he_return,
                divertor_required_hot_margin=divertor_required_hot_margin,
                he_return_residual=he_return_residual,
                pbli_control_margin=pbli_control_margin,
                he_bypass_fraction=he_bypass_fraction,
                he_control_margin=he_control_margin,
                pbli_unmet=pbli_unmet,
                divertor_bypass_fraction=divertor_bypass_fraction,
                he_unmet=he_unmet,
                divertor_control_margin=divertor_control_margin,
                divertor_capability=divertor_capability,
                divertor_hot_terminal_difference=divertor_hot_terminal_difference,
                expansion_factor=expansion_factor,
                closure_residual=closure_residual,
                he_required_hot=he_required_hot,
                control_mode_used=control_mode_used,
                pbli_bypass_fraction=pbli_bypass_fraction,
                pbli_required_hot=pbli_required_hot,
                pbli_hot_bound_margin=pbli_hot_bound_margin,
            )
        )
