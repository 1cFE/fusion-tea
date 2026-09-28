"""Network_Heat_Driven_ClosureModule Module Wrapper

TEAx module for Network_Heat_Driven_Closure calculation.

*Source**: work/active/WI-092_aries-parallel-exchanger-network/design.md. **Reference**: generic network heat-driven closure; network mode 0 copies the reviewed 'Heat Driven Closure' equations line for line (that definition is retained in this file, unbound by the live assembly), mode 1 evaluates the published series-then-parallel exchanger network (Raffray Fig. 12) with a supplied cycle-flow split that is an operating choice, never a sizing rule. MW/K/MPa/kg/s/J per kg K as documented; mode and split are dimensionless; 0 < split < 1 in both modes. **Last Updated**: 2026-09-25.

Inputs:
    - pbli_split_in: pbli_split_in parameter
    - divertor_cp_in: divertor_cp_in parameter
    - pbli_cp_in: pbli_cp_in parameter
    - he_flow_in: he_flow_in parameter
    - divertor_available_in: divertor_available_in parameter
    - divertor_flow_in: divertor_flow_in parameter
    - he_limit_in: he_limit_in parameter
    - pbli_flow_in: pbli_flow_in parameter
    - he_cp_in: he_cp_in parameter
    - flow_in: flow_in parameter
    - gamma_in: gamma_in parameter
    - turbine_pressure_in: turbine_pressure_in parameter
    - pbli_available_in: pbli_available_in parameter
    - he_available_in: he_available_in parameter
    - network_mode_in: network_mode_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - he_ua_in: he_ua_in parameter
    - divertor_limit_in: divertor_limit_in parameter
    - divertor_ua_in: divertor_ua_in parameter
    - turbine_efficiency_in: turbine_efficiency_in parameter
    - pbli_ua_in: pbli_ua_in parameter
    - cp_in: cp_in parameter
    - return_pressure_in: return_pressure_in parameter
    - pbli_limit_in: pbli_limit_in parameter
    - recuperator_effectiveness_in: recuperator_effectiveness_in parameter

Outputs:
    - pbli_state_defined: pbli_state_defined result
    - he_hot: he_hot result
    - network_mode_used: network_mode_used result
    - pbli_cold_terminal_difference: pbli_cold_terminal_difference result
    - divertor_hot: divertor_hot result
    - divertor_hot_bound_margin: divertor_hot_bound_margin result
    - pbli_stream_out: pbli_stream_out result
    - he_hot_bound_margin: he_hot_bound_margin result
    - he_cold_terminal_difference: he_cold_terminal_difference result
    - divertor_unmet: divertor_unmet result
    - pbli_secondary_out: pbli_secondary_out result
    - accepted_heat: accepted_heat result
    - divertor_transferred: divertor_transferred result
    - divertor_state_defined: divertor_state_defined result
    - he_state_defined: he_state_defined result
    - expansion_factor: expansion_factor result
    - pbli_hot: pbli_hot result
    - pbli_transferred: pbli_transferred result
    - pbli_split_used: pbli_split_used result
    - divertor_hot_terminal_difference: divertor_hot_terminal_difference result
    - he_transferred: he_transferred result
    - divertor_stream_out: divertor_stream_out result
    - pbli_return: pbli_return result
    - he_secondary_in: he_secondary_in result
    - pbli_secondary_in: pbli_secondary_in result
    - divertor_secondary_in: divertor_secondary_in result
    - closure_residual: closure_residual result
    - unmet_heat: unmet_heat result
    - heater_inlet: heater_inlet result
    - he_return: he_return result
    - he_capability: he_capability result
    - pbli_hot_bound_margin: pbli_hot_bound_margin result
    - turbine_temperature: turbine_temperature result
    - pbli_capability: pbli_capability result
    - he_secondary_out: he_secondary_out result
    - he_unmet: he_unmet result
    - divertor_cold_terminal_difference: divertor_cold_terminal_difference result
    - pbli_hot_terminal_difference: pbli_hot_terminal_difference result
    - divertor_capability: divertor_capability result
    - mixed_outlet: mixed_outlet result
    - divertor_return: divertor_return result
    - he_hot_terminal_difference: he_hot_terminal_difference result
    - divertor_secondary_out: divertor_secondary_out result
    - iterations: iterations result
    - pbli_unmet: pbli_unmet result

SysML Source: root-0/integrated_heat_electricity.sysml:112

SysML Source: root-0/integrated_heat_electricity.sysml:112

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_heat_electricity/network_heat_driven_closure_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from costed_loop_brayton_tea.primitives import Float
from costed_loop_brayton_tea.schemas.network_heat_driven_closure_output import Network_Heat_Driven_ClosureOutput


class Network_Heat_Driven_ClosureInput(BaseModel):
    """Input model for Network_Heat_Driven_ClosureModule.

    Attributes:
        pbli_split_in: pbli_split_in input
        divertor_cp_in: divertor_cp_in input
        pbli_cp_in: pbli_cp_in input
        he_flow_in: he_flow_in input
        divertor_available_in: divertor_available_in input
        divertor_flow_in: divertor_flow_in input
        he_limit_in: he_limit_in input
        pbli_flow_in: pbli_flow_in input
        he_cp_in: he_cp_in input
        flow_in: flow_in input
        gamma_in: gamma_in input
        turbine_pressure_in: turbine_pressure_in input
        pbli_available_in: pbli_available_in input
        he_available_in: he_available_in input
        network_mode_in: network_mode_in input
        cold_temperature_in: cold_temperature_in input
        he_ua_in: he_ua_in input
        divertor_limit_in: divertor_limit_in input
        divertor_ua_in: divertor_ua_in input
        turbine_efficiency_in: turbine_efficiency_in input
        pbli_ua_in: pbli_ua_in input
        cp_in: cp_in input
        return_pressure_in: return_pressure_in input
        pbli_limit_in: pbli_limit_in input
        recuperator_effectiveness_in: recuperator_effectiveness_in input
    """
    pbli_split_in: float = Field(..., description="pbli_split_in input")
    divertor_cp_in: float = Field(..., description="divertor_cp_in input")
    pbli_cp_in: float = Field(..., description="pbli_cp_in input")
    he_flow_in: float = Field(..., description="he_flow_in input")
    divertor_available_in: float = Field(..., description="divertor_available_in input")
    divertor_flow_in: float = Field(..., description="divertor_flow_in input")
    he_limit_in: float = Field(..., description="he_limit_in input")
    pbli_flow_in: float = Field(..., description="pbli_flow_in input")
    he_cp_in: float = Field(..., description="he_cp_in input")
    flow_in: float = Field(..., description="flow_in input")
    gamma_in: float = Field(..., description="gamma_in input")
    turbine_pressure_in: float = Field(..., description="turbine_pressure_in input")
    pbli_available_in: float = Field(..., description="pbli_available_in input")
    he_available_in: float = Field(..., description="he_available_in input")
    network_mode_in: float = Field(..., description="network_mode_in input")
    cold_temperature_in: float = Field(..., description="cold_temperature_in input")
    he_ua_in: float = Field(..., description="he_ua_in input")
    divertor_limit_in: float = Field(..., description="divertor_limit_in input")
    divertor_ua_in: float = Field(..., description="divertor_ua_in input")
    turbine_efficiency_in: float = Field(..., description="turbine_efficiency_in input")
    pbli_ua_in: float = Field(..., description="pbli_ua_in input")
    cp_in: float = Field(..., description="cp_in input")
    return_pressure_in: float = Field(..., description="return_pressure_in input")
    pbli_limit_in: float = Field(..., description="pbli_limit_in input")
    recuperator_effectiveness_in: float = Field(..., description="recuperator_effectiveness_in input")


class Network_Heat_Driven_ClosureModule(ModuleBase[Network_Heat_Driven_ClosureInput, Network_Heat_Driven_ClosureOutput]):
    """TEAx module for Network_Heat_Driven_Closure calculation.

*Source**: work/active/WI-092_aries-parallel-exchanger-network/design.md. **Reference**: generic network heat-driven closure; network mode 0 copies the reviewed 'Heat Driven Closure' equations line for line (that definition is retained in this file, unbound by the live assembly), mode 1 evaluates the published series-then-parallel exchanger network (Raffray Fig. 12) with a supplied cycle-flow split that is an operating choice, never a sizing rule. MW/K/MPa/kg/s/J per kg K as documented; mode and split are dimensionless; 0 < split < 1 in both modes. **Last Updated**: 2026-09-25.

Inputs:
    - pbli_split_in: pbli_split_in parameter
    - divertor_cp_in: divertor_cp_in parameter
    - pbli_cp_in: pbli_cp_in parameter
    - he_flow_in: he_flow_in parameter
    - divertor_available_in: divertor_available_in parameter
    - divertor_flow_in: divertor_flow_in parameter
    - he_limit_in: he_limit_in parameter
    - pbli_flow_in: pbli_flow_in parameter
    - he_cp_in: he_cp_in parameter
    - flow_in: flow_in parameter
    - gamma_in: gamma_in parameter
    - turbine_pressure_in: turbine_pressure_in parameter
    - pbli_available_in: pbli_available_in parameter
    - he_available_in: he_available_in parameter
    - network_mode_in: network_mode_in parameter
    - cold_temperature_in: cold_temperature_in parameter
    - he_ua_in: he_ua_in parameter
    - divertor_limit_in: divertor_limit_in parameter
    - divertor_ua_in: divertor_ua_in parameter
    - turbine_efficiency_in: turbine_efficiency_in parameter
    - pbli_ua_in: pbli_ua_in parameter
    - cp_in: cp_in parameter
    - return_pressure_in: return_pressure_in parameter
    - pbli_limit_in: pbli_limit_in parameter
    - recuperator_effectiveness_in: recuperator_effectiveness_in parameter

Outputs:
    - pbli_state_defined: pbli_state_defined result
    - he_hot: he_hot result
    - network_mode_used: network_mode_used result
    - pbli_cold_terminal_difference: pbli_cold_terminal_difference result
    - divertor_hot: divertor_hot result
    - divertor_hot_bound_margin: divertor_hot_bound_margin result
    - pbli_stream_out: pbli_stream_out result
    - he_hot_bound_margin: he_hot_bound_margin result
    - he_cold_terminal_difference: he_cold_terminal_difference result
    - divertor_unmet: divertor_unmet result
    - pbli_secondary_out: pbli_secondary_out result
    - accepted_heat: accepted_heat result
    - divertor_transferred: divertor_transferred result
    - divertor_state_defined: divertor_state_defined result
    - he_state_defined: he_state_defined result
    - expansion_factor: expansion_factor result
    - pbli_hot: pbli_hot result
    - pbli_transferred: pbli_transferred result
    - pbli_split_used: pbli_split_used result
    - divertor_hot_terminal_difference: divertor_hot_terminal_difference result
    - he_transferred: he_transferred result
    - divertor_stream_out: divertor_stream_out result
    - pbli_return: pbli_return result
    - he_secondary_in: he_secondary_in result
    - pbli_secondary_in: pbli_secondary_in result
    - divertor_secondary_in: divertor_secondary_in result
    - closure_residual: closure_residual result
    - unmet_heat: unmet_heat result
    - heater_inlet: heater_inlet result
    - he_return: he_return result
    - he_capability: he_capability result
    - pbli_hot_bound_margin: pbli_hot_bound_margin result
    - turbine_temperature: turbine_temperature result
    - pbli_capability: pbli_capability result
    - he_secondary_out: he_secondary_out result
    - he_unmet: he_unmet result
    - divertor_cold_terminal_difference: divertor_cold_terminal_difference result
    - pbli_hot_terminal_difference: pbli_hot_terminal_difference result
    - divertor_capability: divertor_capability result
    - mixed_outlet: mixed_outlet result
    - divertor_return: divertor_return result
    - he_hot_terminal_difference: he_hot_terminal_difference result
    - divertor_secondary_out: divertor_secondary_out result
    - iterations: iterations result
    - pbli_unmet: pbli_unmet result

SysML Source: root-0/integrated_heat_electricity.sysml:112

    SysML Source: root-0/integrated_heat_electricity.sysml:112

    Calculation Specification:
        See documentation:
*Source**: work/active/WI-092_aries-parallel-exchanger-network/design.md. **Reference**: generic network heat-driven closure; network mode 0 copies the reviewed 'Heat Driven Closure' equations line for line (that definition is retained in this file, unbound by the live assembly), mode 1 evaluates the published series-then-parallel exchanger network (Raffray Fig. 12) with a supplied cycle-flow split that is an operating choice, never a sizing rule. MW/K/MPa/kg/s/J per kg K as documented; mode and split are dimensionless; 0 < split < 1 in both modes. **Last Updated**: 2026-09-25.

    IMPLEMENTATION: See costed_loop_brayton_tea.handwritten.integrated_heat_electricity.network_heat_driven_closure_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts pbli_state_defined, he_hot, network_mode_used, pbli_cold_terminal_difference, divertor_hot, divertor_hot_bound_margin, pbli_stream_out, he_hot_bound_margin, he_cold_terminal_difference, divertor_unmet, pbli_secondary_out, accepted_heat, divertor_transferred, divertor_state_defined, he_state_defined, expansion_factor, pbli_hot, pbli_transferred, pbli_split_used, divertor_hot_terminal_difference, he_transferred, divertor_stream_out, pbli_return, he_secondary_in, pbli_secondary_in, divertor_secondary_in, closure_residual, unmet_heat, heater_inlet, he_return, he_capability, pbli_hot_bound_margin, turbine_temperature, pbli_capability, he_secondary_out, he_unmet, divertor_cold_terminal_difference, pbli_hot_terminal_difference, divertor_capability, mixed_outlet, divertor_return, he_hot_terminal_difference, divertor_secondary_out, iterations, pbli_unmet fields to separate channels.
    """

    name: str = "Network_Heat_Driven_ClosureModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, pbli_split_in: float, divertor_cp_in: float, pbli_cp_in: float, he_flow_in: float, divertor_available_in: float, divertor_flow_in: float, he_limit_in: float, pbli_flow_in: float, he_cp_in: float, flow_in: float, gamma_in: float, turbine_pressure_in: float, pbli_available_in: float, he_available_in: float, network_mode_in: float, cold_temperature_in: float, he_ua_in: float, divertor_limit_in: float, divertor_ua_in: float, turbine_efficiency_in: float, pbli_ua_in: float, cp_in: float, return_pressure_in: float, pbli_limit_in: float, recuperator_effectiveness_in: float    ) -> Network_Heat_Driven_ClosureInput:
        """Validate inputs and fill defaults.

        Args:
            pbli_split_in: pbli_split_in input
            divertor_cp_in: divertor_cp_in input
            pbli_cp_in: pbli_cp_in input
            he_flow_in: he_flow_in input
            divertor_available_in: divertor_available_in input
            divertor_flow_in: divertor_flow_in input
            he_limit_in: he_limit_in input
            pbli_flow_in: pbli_flow_in input
            he_cp_in: he_cp_in input
            flow_in: flow_in input
            gamma_in: gamma_in input
            turbine_pressure_in: turbine_pressure_in input
            pbli_available_in: pbli_available_in input
            he_available_in: he_available_in input
            network_mode_in: network_mode_in input
            cold_temperature_in: cold_temperature_in input
            he_ua_in: he_ua_in input
            divertor_limit_in: divertor_limit_in input
            divertor_ua_in: divertor_ua_in input
            turbine_efficiency_in: turbine_efficiency_in input
            pbli_ua_in: pbli_ua_in input
            cp_in: cp_in input
            return_pressure_in: return_pressure_in input
            pbli_limit_in: pbli_limit_in input
            recuperator_effectiveness_in: recuperator_effectiveness_in input

        Returns:
            Validated input model
        """
        return Network_Heat_Driven_ClosureInput(pbli_split_in=pbli_split_in, divertor_cp_in=divertor_cp_in, pbli_cp_in=pbli_cp_in, he_flow_in=he_flow_in, divertor_available_in=divertor_available_in, divertor_flow_in=divertor_flow_in, he_limit_in=he_limit_in, pbli_flow_in=pbli_flow_in, he_cp_in=he_cp_in, flow_in=flow_in, gamma_in=gamma_in, turbine_pressure_in=turbine_pressure_in, pbli_available_in=pbli_available_in, he_available_in=he_available_in, network_mode_in=network_mode_in, cold_temperature_in=cold_temperature_in, he_ua_in=he_ua_in, divertor_limit_in=divertor_limit_in, divertor_ua_in=divertor_ua_in, turbine_efficiency_in=turbine_efficiency_in, pbli_ua_in=pbli_ua_in, cp_in=cp_in, return_pressure_in=return_pressure_in, pbli_limit_in=pbli_limit_in, recuperator_effectiveness_in=recuperator_effectiveness_in)

    def run(
        self, pbli_split_in: float, divertor_cp_in: float, pbli_cp_in: float, he_flow_in: float, divertor_available_in: float, divertor_flow_in: float, he_limit_in: float, pbli_flow_in: float, he_cp_in: float, flow_in: float, gamma_in: float, turbine_pressure_in: float, pbli_available_in: float, he_available_in: float, network_mode_in: float, cold_temperature_in: float, he_ua_in: float, divertor_limit_in: float, divertor_ua_in: float, turbine_efficiency_in: float, pbli_ua_in: float, cp_in: float, return_pressure_in: float, pbli_limit_in: float, recuperator_effectiveness_in: float    ) -> ModuleResult[Network_Heat_Driven_ClosureOutput]:
        """Execute calculation.

        Args:
            pbli_split_in: pbli_split_in input
            divertor_cp_in: divertor_cp_in input
            pbli_cp_in: pbli_cp_in input
            he_flow_in: he_flow_in input
            divertor_available_in: divertor_available_in input
            divertor_flow_in: divertor_flow_in input
            he_limit_in: he_limit_in input
            pbli_flow_in: pbli_flow_in input
            he_cp_in: he_cp_in input
            flow_in: flow_in input
            gamma_in: gamma_in input
            turbine_pressure_in: turbine_pressure_in input
            pbli_available_in: pbli_available_in input
            he_available_in: he_available_in input
            network_mode_in: network_mode_in input
            cold_temperature_in: cold_temperature_in input
            he_ua_in: he_ua_in input
            divertor_limit_in: divertor_limit_in input
            divertor_ua_in: divertor_ua_in input
            turbine_efficiency_in: turbine_efficiency_in input
            pbli_ua_in: pbli_ua_in input
            cp_in: cp_in input
            return_pressure_in: return_pressure_in input
            pbli_limit_in: pbli_limit_in input
            recuperator_effectiveness_in: recuperator_effectiveness_in input

        Returns:
            Module result with Network_Heat_Driven_ClosureOutput (pbli_state_defined, he_hot, network_mode_used, pbli_cold_terminal_difference, divertor_hot, divertor_hot_bound_margin, pbli_stream_out, he_hot_bound_margin, he_cold_terminal_difference, divertor_unmet, pbli_secondary_out, accepted_heat, divertor_transferred, divertor_state_defined, he_state_defined, expansion_factor, pbli_hot, pbli_transferred, pbli_split_used, divertor_hot_terminal_difference, he_transferred, divertor_stream_out, pbli_return, he_secondary_in, pbli_secondary_in, divertor_secondary_in, closure_residual, unmet_heat, heater_inlet, he_return, he_capability, pbli_hot_bound_margin, turbine_temperature, pbli_capability, he_secondary_out, he_unmet, divertor_cold_terminal_difference, pbli_hot_terminal_difference, divertor_capability, mixed_outlet, divertor_return, he_hot_terminal_difference, divertor_secondary_out, iterations, pbli_unmet)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(pbli_split_in, divertor_cp_in, pbli_cp_in, he_flow_in, divertor_available_in, divertor_flow_in, he_limit_in, pbli_flow_in, he_cp_in, flow_in, gamma_in, turbine_pressure_in, pbli_available_in, he_available_in, network_mode_in, cold_temperature_in, he_ua_in, divertor_limit_in, divertor_ua_in, turbine_efficiency_in, pbli_ua_in, cp_in, return_pressure_in, pbli_limit_in, recuperator_effectiveness_in)

        # Import handwritten implementation
        from costed_loop_brayton_tea.handwritten.integrated_heat_electricity.network_heat_driven_closure_impl import (
            run_network_heat_driven_closure,
        )

        # Execute implementation - returns tuple of values
        pbli_state_defined, he_hot, network_mode_used, pbli_cold_terminal_difference, divertor_hot, divertor_hot_bound_margin, pbli_stream_out, he_hot_bound_margin, he_cold_terminal_difference, divertor_unmet, pbli_secondary_out, accepted_heat, divertor_transferred, divertor_state_defined, he_state_defined, expansion_factor, pbli_hot, pbli_transferred, pbli_split_used, divertor_hot_terminal_difference, he_transferred, divertor_stream_out, pbli_return, he_secondary_in, pbli_secondary_in, divertor_secondary_in, closure_residual, unmet_heat, heater_inlet, he_return, he_capability, pbli_hot_bound_margin, turbine_temperature, pbli_capability, he_secondary_out, he_unmet, divertor_cold_terminal_difference, pbli_hot_terminal_difference, divertor_capability, mixed_outlet, divertor_return, he_hot_terminal_difference, divertor_secondary_out, iterations, pbli_unmet = run_network_heat_driven_closure(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Network_Heat_Driven_ClosureOutput(
                pbli_state_defined=pbli_state_defined,
                he_hot=he_hot,
                network_mode_used=network_mode_used,
                pbli_cold_terminal_difference=pbli_cold_terminal_difference,
                divertor_hot=divertor_hot,
                divertor_hot_bound_margin=divertor_hot_bound_margin,
                pbli_stream_out=pbli_stream_out,
                he_hot_bound_margin=he_hot_bound_margin,
                he_cold_terminal_difference=he_cold_terminal_difference,
                divertor_unmet=divertor_unmet,
                pbli_secondary_out=pbli_secondary_out,
                accepted_heat=accepted_heat,
                divertor_transferred=divertor_transferred,
                divertor_state_defined=divertor_state_defined,
                he_state_defined=he_state_defined,
                expansion_factor=expansion_factor,
                pbli_hot=pbli_hot,
                pbli_transferred=pbli_transferred,
                pbli_split_used=pbli_split_used,
                divertor_hot_terminal_difference=divertor_hot_terminal_difference,
                he_transferred=he_transferred,
                divertor_stream_out=divertor_stream_out,
                pbli_return=pbli_return,
                he_secondary_in=he_secondary_in,
                pbli_secondary_in=pbli_secondary_in,
                divertor_secondary_in=divertor_secondary_in,
                closure_residual=closure_residual,
                unmet_heat=unmet_heat,
                heater_inlet=heater_inlet,
                he_return=he_return,
                he_capability=he_capability,
                pbli_hot_bound_margin=pbli_hot_bound_margin,
                turbine_temperature=turbine_temperature,
                pbli_capability=pbli_capability,
                he_secondary_out=he_secondary_out,
                he_unmet=he_unmet,
                divertor_cold_terminal_difference=divertor_cold_terminal_difference,
                pbli_hot_terminal_difference=pbli_hot_terminal_difference,
                divertor_capability=divertor_capability,
                mixed_outlet=mixed_outlet,
                divertor_return=divertor_return,
                he_hot_terminal_difference=he_hot_terminal_difference,
                divertor_secondary_out=divertor_secondary_out,
                iterations=iterations,
                pbli_unmet=pbli_unmet,
            )
        )
