"""Controlled_Conversion_BoundaryModule Module Wrapper

TEAx module for Controlled_Conversion_Boundary calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/controlled_conversion_boundary_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - salt_shaft_in: salt_shaft_in parameter
    - imported_electric_in: imported_electric_in parameter
    - return_residual_in: return_residual_in parameter
    - dp_in: dp_in parameter
    - salt_cp_in: salt_cp_in parameter
    - total_flow_rating_in: total_flow_rating_in parameter
    - exchanger_flow_rating_in: exchanger_flow_rating_in parameter
    - max_bypass_in: max_bypass_in parameter
    - available_in: available_in parameter
    - hot_temperature_in: hot_temperature_in parameter
    - temperature_rating_in: temperature_rating_in parameter
    - bypass_flow_rating_in: bypass_flow_rating_in parameter
    - raw_heat_in: raw_heat_in parameter
    - bypass_fraction_in: bypass_fraction_in parameter
    - pressure_in: pressure_in parameter
    - gross_electric_in: gross_electric_in parameter
    - exchanger_flow_in: exchanger_flow_in parameter
    - net_shaft_in: net_shaft_in parameter
    - actuation_in: actuation_in parameter
    - salt_flow_in: salt_flow_in parameter
    - cycle_rejection_in: cycle_rejection_in parameter
    - capability_open_in: capability_open_in parameter
    - pressure_rating_in: pressure_rating_in parameter
    - primary_flow_in: primary_flow_in parameter
    - salt_electric_in: salt_electric_in parameter
    - added_dp_rating_in: added_dp_rating_in parameter
    - feasible_in: feasible_in parameter
    - loss_factor_in: loss_factor_in parameter

Outputs:
    - salt_hot: salt_hot result
    - salt_return: salt_return result
    - bypass_fraction_margin: bypass_fraction_margin result
    - steam_heat: steam_heat result
    - source_adequate: source_adequate result
    - temperature_margin: temperature_margin result
    - added_dp: added_dp result
    - added_dp_margin: added_dp_margin result
    - bypass_flow: bypass_flow result
    - salt_motor_loss: salt_motor_loss result
    - converged: converged result
    - duty_correction: duty_correction result
    - pressure_margin: pressure_margin result
    - actual_heat: actual_heat result
    - raw_return_residual: raw_return_residual result
    - controller_capacity_ok: controller_capacity_ok result
    - motor_import_loss: motor_import_loss result
    - exchanger_flow_margin: exchanger_flow_margin result
    - bypass_flow_margin: bypass_flow_margin result
    - total_flow_margin: total_flow_margin result
    - rejection_load: rejection_load result
    - raw_heat_residual: raw_heat_residual result
    - unremoved_heat: unremoved_heat result
    - generator_loss: generator_loss result

SysML Source: root-0/component_alternatives_thermal.sysml:123

SysML Source: root-0/component_alternatives_thermal.sysml:123

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/component_alternatives_thermal/controlled_conversion_boundary_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from component_alternatives_tea.primitives import Float
from component_alternatives_tea.schemas.controlled_conversion_boundary_output import Controlled_Conversion_BoundaryOutput


class Controlled_Conversion_BoundaryInput(BaseModel):
    """Input model for Controlled_Conversion_BoundaryModule.

    Attributes:
        salt_shaft_in: salt_shaft_in input
        imported_electric_in: imported_electric_in input
        return_residual_in: return_residual_in input
        dp_in: dp_in input
        salt_cp_in: salt_cp_in input
        total_flow_rating_in: total_flow_rating_in input
        exchanger_flow_rating_in: exchanger_flow_rating_in input
        max_bypass_in: max_bypass_in input
        available_in: available_in input
        hot_temperature_in: hot_temperature_in input
        temperature_rating_in: temperature_rating_in input
        bypass_flow_rating_in: bypass_flow_rating_in input
        raw_heat_in: raw_heat_in input
        bypass_fraction_in: bypass_fraction_in input
        pressure_in: pressure_in input
        gross_electric_in: gross_electric_in input
        exchanger_flow_in: exchanger_flow_in input
        net_shaft_in: net_shaft_in input
        actuation_in: actuation_in input
        salt_flow_in: salt_flow_in input
        cycle_rejection_in: cycle_rejection_in input
        capability_open_in: capability_open_in input
        pressure_rating_in: pressure_rating_in input
        primary_flow_in: primary_flow_in input
        salt_electric_in: salt_electric_in input
        added_dp_rating_in: added_dp_rating_in input
        feasible_in: feasible_in input
        loss_factor_in: loss_factor_in input
    """
    salt_shaft_in: float = Field(..., description="salt_shaft_in input")
    imported_electric_in: float = Field(..., description="imported_electric_in input")
    return_residual_in: float = Field(..., description="return_residual_in input")
    dp_in: float = Field(..., description="dp_in input")
    salt_cp_in: float = Field(..., description="salt_cp_in input")
    total_flow_rating_in: float = Field(..., description="total_flow_rating_in input")
    exchanger_flow_rating_in: float = Field(..., description="exchanger_flow_rating_in input")
    max_bypass_in: float = Field(..., description="max_bypass_in input")
    available_in: float = Field(..., description="available_in input")
    hot_temperature_in: float = Field(..., description="hot_temperature_in input")
    temperature_rating_in: float = Field(..., description="temperature_rating_in input")
    bypass_flow_rating_in: float = Field(..., description="bypass_flow_rating_in input")
    raw_heat_in: float = Field(..., description="raw_heat_in input")
    bypass_fraction_in: float = Field(..., description="bypass_fraction_in input")
    pressure_in: float = Field(..., description="pressure_in input")
    gross_electric_in: float = Field(..., description="gross_electric_in input")
    exchanger_flow_in: float = Field(..., description="exchanger_flow_in input")
    net_shaft_in: float = Field(..., description="net_shaft_in input")
    actuation_in: float = Field(..., description="actuation_in input")
    salt_flow_in: float = Field(..., description="salt_flow_in input")
    cycle_rejection_in: float = Field(..., description="cycle_rejection_in input")
    capability_open_in: float = Field(..., description="capability_open_in input")
    pressure_rating_in: float = Field(..., description="pressure_rating_in input")
    primary_flow_in: float = Field(..., description="primary_flow_in input")
    salt_electric_in: float = Field(..., description="salt_electric_in input")
    added_dp_rating_in: float = Field(..., description="added_dp_rating_in input")
    feasible_in: float = Field(..., description="feasible_in input")
    loss_factor_in: float = Field(..., description="loss_factor_in input")


class Controlled_Conversion_BoundaryModule(ModuleBase[Controlled_Conversion_BoundaryInput, Controlled_Conversion_BoundaryOutput]):
    """TEAx module for Controlled_Conversion_Boundary calculation.

*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/controlled_conversion_boundary_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

Inputs:
    - salt_shaft_in: salt_shaft_in parameter
    - imported_electric_in: imported_electric_in parameter
    - return_residual_in: return_residual_in parameter
    - dp_in: dp_in parameter
    - salt_cp_in: salt_cp_in parameter
    - total_flow_rating_in: total_flow_rating_in parameter
    - exchanger_flow_rating_in: exchanger_flow_rating_in parameter
    - max_bypass_in: max_bypass_in parameter
    - available_in: available_in parameter
    - hot_temperature_in: hot_temperature_in parameter
    - temperature_rating_in: temperature_rating_in parameter
    - bypass_flow_rating_in: bypass_flow_rating_in parameter
    - raw_heat_in: raw_heat_in parameter
    - bypass_fraction_in: bypass_fraction_in parameter
    - pressure_in: pressure_in parameter
    - gross_electric_in: gross_electric_in parameter
    - exchanger_flow_in: exchanger_flow_in parameter
    - net_shaft_in: net_shaft_in parameter
    - actuation_in: actuation_in parameter
    - salt_flow_in: salt_flow_in parameter
    - cycle_rejection_in: cycle_rejection_in parameter
    - capability_open_in: capability_open_in parameter
    - pressure_rating_in: pressure_rating_in parameter
    - primary_flow_in: primary_flow_in parameter
    - salt_electric_in: salt_electric_in parameter
    - added_dp_rating_in: added_dp_rating_in parameter
    - feasible_in: feasible_in parameter
    - loss_factor_in: loss_factor_in parameter

Outputs:
    - salt_hot: salt_hot result
    - salt_return: salt_return result
    - bypass_fraction_margin: bypass_fraction_margin result
    - steam_heat: steam_heat result
    - source_adequate: source_adequate result
    - temperature_margin: temperature_margin result
    - added_dp: added_dp result
    - added_dp_margin: added_dp_margin result
    - bypass_flow: bypass_flow result
    - salt_motor_loss: salt_motor_loss result
    - converged: converged result
    - duty_correction: duty_correction result
    - pressure_margin: pressure_margin result
    - actual_heat: actual_heat result
    - raw_return_residual: raw_return_residual result
    - controller_capacity_ok: controller_capacity_ok result
    - motor_import_loss: motor_import_loss result
    - exchanger_flow_margin: exchanger_flow_margin result
    - bypass_flow_margin: bypass_flow_margin result
    - total_flow_margin: total_flow_margin result
    - rejection_load: rejection_load result
    - raw_heat_residual: raw_heat_residual result
    - unremoved_heat: unremoved_heat result
    - generator_loss: generator_loss result

SysML Source: root-0/component_alternatives_thermal.sysml:123

    SysML Source: root-0/component_alternatives_thermal.sysml:123

    Calculation Specification:
        available_in = 0.0
        capability_open_in = 0.0
        raw_heat_in = 0.0
        feasible_in = 0.0
        return_residual_in = 0.0
        primary_flow_in = 0.0
        exchanger_flow_in = 0.0
        bypass_fraction_in = 0.0
        pressure_in = 0.0
        hot_temperature_in = 0.0
        dp_in = 0.0
        loss_factor_in = 1.1
        total_flow_rating_in = 4000.0
        exchanger_flow_rating_in = 4000.0
        bypass_flow_rating_in = 2000.0
        max_bypass_in = 0.5
        pressure_rating_in = 8000000.0
        temperature_rating_in = 800.0
        added_dp_rating_in = 100000.0
        salt_flow_in = 0.0
        salt_cp_in = 1560.0
        salt_shaft_in = 0.0
        salt_electric_in = 0.0
        actuation_in = 0.1
        gross_electric_in = 0.0
        net_shaft_in = 0.0
        imported_electric_in = 0.0
        cycle_rejection_in = 0.0
        
Documentation:
*Source**: work/active/WI-096_matched-conversion-subsystems/design.md. **Reference**: reviewed fourth submission, sections 2-8. **Basis**: [AGENT] conditional component offer and explicitly reviewed equations; hydraulic, price and loss-sink qualification remain unverified. **Last Updated**: 2026-09-26. Numerical semantics are the complete calculate function in exploration/component_alternatives/bodies/component_alternatives_thermal/controlled_conversion_boundary_impl.py; units MW, K/degC, kg/s, Pa, MW/K, USD2025 and years as named.

    IMPLEMENTATION: See component_alternatives_tea.handwritten.component_alternatives_thermal.controlled_conversion_boundary_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts salt_hot, salt_return, bypass_fraction_margin, steam_heat, source_adequate, temperature_margin, added_dp, added_dp_margin, bypass_flow, salt_motor_loss, converged, duty_correction, pressure_margin, actual_heat, raw_return_residual, controller_capacity_ok, motor_import_loss, exchanger_flow_margin, bypass_flow_margin, total_flow_margin, rejection_load, raw_heat_residual, unremoved_heat, generator_loss fields to separate channels.
    """

    name: str = "Controlled_Conversion_BoundaryModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, salt_shaft_in: float, imported_electric_in: float, return_residual_in: float, dp_in: float, salt_cp_in: float, total_flow_rating_in: float, exchanger_flow_rating_in: float, max_bypass_in: float, available_in: float, hot_temperature_in: float, temperature_rating_in: float, bypass_flow_rating_in: float, raw_heat_in: float, bypass_fraction_in: float, pressure_in: float, gross_electric_in: float, exchanger_flow_in: float, net_shaft_in: float, actuation_in: float, salt_flow_in: float, cycle_rejection_in: float, capability_open_in: float, pressure_rating_in: float, primary_flow_in: float, salt_electric_in: float, added_dp_rating_in: float, feasible_in: float, loss_factor_in: float    ) -> Controlled_Conversion_BoundaryInput:
        """Validate inputs and fill defaults.

        Args:
            salt_shaft_in: salt_shaft_in input
            imported_electric_in: imported_electric_in input
            return_residual_in: return_residual_in input
            dp_in: dp_in input
            salt_cp_in: salt_cp_in input
            total_flow_rating_in: total_flow_rating_in input
            exchanger_flow_rating_in: exchanger_flow_rating_in input
            max_bypass_in: max_bypass_in input
            available_in: available_in input
            hot_temperature_in: hot_temperature_in input
            temperature_rating_in: temperature_rating_in input
            bypass_flow_rating_in: bypass_flow_rating_in input
            raw_heat_in: raw_heat_in input
            bypass_fraction_in: bypass_fraction_in input
            pressure_in: pressure_in input
            gross_electric_in: gross_electric_in input
            exchanger_flow_in: exchanger_flow_in input
            net_shaft_in: net_shaft_in input
            actuation_in: actuation_in input
            salt_flow_in: salt_flow_in input
            cycle_rejection_in: cycle_rejection_in input
            capability_open_in: capability_open_in input
            pressure_rating_in: pressure_rating_in input
            primary_flow_in: primary_flow_in input
            salt_electric_in: salt_electric_in input
            added_dp_rating_in: added_dp_rating_in input
            feasible_in: feasible_in input
            loss_factor_in: loss_factor_in input

        Returns:
            Validated input model
        """
        return Controlled_Conversion_BoundaryInput(salt_shaft_in=salt_shaft_in, imported_electric_in=imported_electric_in, return_residual_in=return_residual_in, dp_in=dp_in, salt_cp_in=salt_cp_in, total_flow_rating_in=total_flow_rating_in, exchanger_flow_rating_in=exchanger_flow_rating_in, max_bypass_in=max_bypass_in, available_in=available_in, hot_temperature_in=hot_temperature_in, temperature_rating_in=temperature_rating_in, bypass_flow_rating_in=bypass_flow_rating_in, raw_heat_in=raw_heat_in, bypass_fraction_in=bypass_fraction_in, pressure_in=pressure_in, gross_electric_in=gross_electric_in, exchanger_flow_in=exchanger_flow_in, net_shaft_in=net_shaft_in, actuation_in=actuation_in, salt_flow_in=salt_flow_in, cycle_rejection_in=cycle_rejection_in, capability_open_in=capability_open_in, pressure_rating_in=pressure_rating_in, primary_flow_in=primary_flow_in, salt_electric_in=salt_electric_in, added_dp_rating_in=added_dp_rating_in, feasible_in=feasible_in, loss_factor_in=loss_factor_in)

    def run(
        self, salt_shaft_in: float, imported_electric_in: float, return_residual_in: float, dp_in: float, salt_cp_in: float, total_flow_rating_in: float, exchanger_flow_rating_in: float, max_bypass_in: float, available_in: float, hot_temperature_in: float, temperature_rating_in: float, bypass_flow_rating_in: float, raw_heat_in: float, bypass_fraction_in: float, pressure_in: float, gross_electric_in: float, exchanger_flow_in: float, net_shaft_in: float, actuation_in: float, salt_flow_in: float, cycle_rejection_in: float, capability_open_in: float, pressure_rating_in: float, primary_flow_in: float, salt_electric_in: float, added_dp_rating_in: float, feasible_in: float, loss_factor_in: float    ) -> ModuleResult[Controlled_Conversion_BoundaryOutput]:
        """Execute calculation.

        Args:
            salt_shaft_in: salt_shaft_in input
            imported_electric_in: imported_electric_in input
            return_residual_in: return_residual_in input
            dp_in: dp_in input
            salt_cp_in: salt_cp_in input
            total_flow_rating_in: total_flow_rating_in input
            exchanger_flow_rating_in: exchanger_flow_rating_in input
            max_bypass_in: max_bypass_in input
            available_in: available_in input
            hot_temperature_in: hot_temperature_in input
            temperature_rating_in: temperature_rating_in input
            bypass_flow_rating_in: bypass_flow_rating_in input
            raw_heat_in: raw_heat_in input
            bypass_fraction_in: bypass_fraction_in input
            pressure_in: pressure_in input
            gross_electric_in: gross_electric_in input
            exchanger_flow_in: exchanger_flow_in input
            net_shaft_in: net_shaft_in input
            actuation_in: actuation_in input
            salt_flow_in: salt_flow_in input
            cycle_rejection_in: cycle_rejection_in input
            capability_open_in: capability_open_in input
            pressure_rating_in: pressure_rating_in input
            primary_flow_in: primary_flow_in input
            salt_electric_in: salt_electric_in input
            added_dp_rating_in: added_dp_rating_in input
            feasible_in: feasible_in input
            loss_factor_in: loss_factor_in input

        Returns:
            Module result with Controlled_Conversion_BoundaryOutput (salt_hot, salt_return, bypass_fraction_margin, steam_heat, source_adequate, temperature_margin, added_dp, added_dp_margin, bypass_flow, salt_motor_loss, converged, duty_correction, pressure_margin, actual_heat, raw_return_residual, controller_capacity_ok, motor_import_loss, exchanger_flow_margin, bypass_flow_margin, total_flow_margin, rejection_load, raw_heat_residual, unremoved_heat, generator_loss)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(salt_shaft_in, imported_electric_in, return_residual_in, dp_in, salt_cp_in, total_flow_rating_in, exchanger_flow_rating_in, max_bypass_in, available_in, hot_temperature_in, temperature_rating_in, bypass_flow_rating_in, raw_heat_in, bypass_fraction_in, pressure_in, gross_electric_in, exchanger_flow_in, net_shaft_in, actuation_in, salt_flow_in, cycle_rejection_in, capability_open_in, pressure_rating_in, primary_flow_in, salt_electric_in, added_dp_rating_in, feasible_in, loss_factor_in)

        # Import handwritten implementation
        from component_alternatives_tea.handwritten.component_alternatives_thermal.controlled_conversion_boundary_impl import (
            run_controlled_conversion_boundary,
        )

        # Execute implementation - returns tuple of values
        salt_hot, salt_return, bypass_fraction_margin, steam_heat, source_adequate, temperature_margin, added_dp, added_dp_margin, bypass_flow, salt_motor_loss, converged, duty_correction, pressure_margin, actual_heat, raw_return_residual, controller_capacity_ok, motor_import_loss, exchanger_flow_margin, bypass_flow_margin, total_flow_margin, rejection_load, raw_heat_residual, unremoved_heat, generator_loss = run_controlled_conversion_boundary(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Controlled_Conversion_BoundaryOutput(
                salt_hot=salt_hot,
                salt_return=salt_return,
                bypass_fraction_margin=bypass_fraction_margin,
                steam_heat=steam_heat,
                source_adequate=source_adequate,
                temperature_margin=temperature_margin,
                added_dp=added_dp,
                added_dp_margin=added_dp_margin,
                bypass_flow=bypass_flow,
                salt_motor_loss=salt_motor_loss,
                converged=converged,
                duty_correction=duty_correction,
                pressure_margin=pressure_margin,
                actual_heat=actual_heat,
                raw_return_residual=raw_return_residual,
                controller_capacity_ok=controller_capacity_ok,
                motor_import_loss=motor_import_loss,
                exchanger_flow_margin=exchanger_flow_margin,
                bypass_flow_margin=bypass_flow_margin,
                total_flow_margin=total_flow_margin,
                rejection_load=rejection_load,
                raw_heat_residual=raw_heat_residual,
                unremoved_heat=unremoved_heat,
                generator_loss=generator_loss,
            )
        )
