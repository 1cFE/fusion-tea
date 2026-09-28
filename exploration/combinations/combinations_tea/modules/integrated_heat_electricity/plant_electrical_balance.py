"""Plant_Electrical_BalanceModule Module Wrapper

TEAx module for Plant_Electrical_Balance calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator/auxiliary owner and electrical energy ledger equations; efficiencies dimensionless, rates atoms/s, all powers MW. **Last Updated**: 2026-09-22.

Inputs:
    - motor_efficiency_in: motor_efficiency_in parameter
    - compressor_1_in: compressor_1_in parameter
    - pump_electric_in: pump_electric_in parameter
    - generator_efficiency_in: generator_efficiency_in parameter
    - cryo_in: cryo_in parameter
    - other_electric_in: other_electric_in parameter
    - control_in: control_in parameter
    - turbine_work_in: turbine_work_in parameter
    - pump_recovered_in: pump_recovered_in parameter
    - fuel_exhaust_in: fuel_exhaust_in parameter
    - compressor_2_in: compressor_2_in parameter
    - fuel_coefficient_in: fuel_coefficient_in parameter
    - heating_efficiency_in: heating_efficiency_in parameter
    - auxiliary_heat_in: auxiliary_heat_in parameter
    - compressor_3_in: compressor_3_in parameter
    - fuel_base_in: fuel_base_in parameter

Outputs:
    - fuel_base_electric: fuel_base_electric result
    - other_electric_demand: other_electric_demand result
    - dissipated_auxiliary: dissipated_auxiliary result
    - net_electric: net_electric result
    - generator_loss: generator_loss result
    - net_shaft: net_shaft result
    - heating_electric: heating_electric result
    - cryo_electric: cryo_electric result
    - fuel_variable_electric: fuel_variable_electric result
    - compressor_demand: compressor_demand result
    - auxiliary_electric: auxiliary_electric result
    - gross_electric: gross_electric result
    - fuel_electric: fuel_electric result
    - primary_pump_electric: primary_pump_electric result
    - motor_loss: motor_loss result
    - shaft_import: shaft_import result
    - heating_loss: heating_loss result
    - pump_loss: pump_loss result
    - control_electric: control_electric result

SysML Source: root-0/integrated_heat_electricity.sysml:197

SysML Source: root-0/integrated_heat_electricity.sysml:197

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_heat_electricity/plant_electrical_balance_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from combinations_tea.primitives import Float
from combinations_tea.schemas.plant_electrical_balance_output import Plant_Electrical_BalanceOutput


class Plant_Electrical_BalanceInput(BaseModel):
    """Input model for Plant_Electrical_BalanceModule.

    Attributes:
        motor_efficiency_in: motor_efficiency_in input
        compressor_1_in: compressor_1_in input
        pump_electric_in: pump_electric_in input
        generator_efficiency_in: generator_efficiency_in input
        cryo_in: cryo_in input
        other_electric_in: other_electric_in input
        control_in: control_in input
        turbine_work_in: turbine_work_in input
        pump_recovered_in: pump_recovered_in input
        fuel_exhaust_in: fuel_exhaust_in input
        compressor_2_in: compressor_2_in input
        fuel_coefficient_in: fuel_coefficient_in input
        heating_efficiency_in: heating_efficiency_in input
        auxiliary_heat_in: auxiliary_heat_in input
        compressor_3_in: compressor_3_in input
        fuel_base_in: fuel_base_in input
    """
    motor_efficiency_in: float = Field(..., description="motor_efficiency_in input")
    compressor_1_in: float = Field(..., description="compressor_1_in input")
    pump_electric_in: float = Field(..., description="pump_electric_in input")
    generator_efficiency_in: float = Field(..., description="generator_efficiency_in input")
    cryo_in: float = Field(..., description="cryo_in input")
    other_electric_in: float = Field(..., description="other_electric_in input")
    control_in: float = Field(..., description="control_in input")
    turbine_work_in: float = Field(..., description="turbine_work_in input")
    pump_recovered_in: float = Field(..., description="pump_recovered_in input")
    fuel_exhaust_in: float = Field(..., description="fuel_exhaust_in input")
    compressor_2_in: float = Field(..., description="compressor_2_in input")
    fuel_coefficient_in: float = Field(..., description="fuel_coefficient_in input")
    heating_efficiency_in: float = Field(..., description="heating_efficiency_in input")
    auxiliary_heat_in: float = Field(..., description="auxiliary_heat_in input")
    compressor_3_in: float = Field(..., description="compressor_3_in input")
    fuel_base_in: float = Field(..., description="fuel_base_in input")


class Plant_Electrical_BalanceModule(ModuleBase[Plant_Electrical_BalanceInput, Plant_Electrical_BalanceOutput]):
    """TEAx module for Plant_Electrical_Balance calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator/auxiliary owner and electrical energy ledger equations; efficiencies dimensionless, rates atoms/s, all powers MW. **Last Updated**: 2026-09-22.

Inputs:
    - motor_efficiency_in: motor_efficiency_in parameter
    - compressor_1_in: compressor_1_in parameter
    - pump_electric_in: pump_electric_in parameter
    - generator_efficiency_in: generator_efficiency_in parameter
    - cryo_in: cryo_in parameter
    - other_electric_in: other_electric_in parameter
    - control_in: control_in parameter
    - turbine_work_in: turbine_work_in parameter
    - pump_recovered_in: pump_recovered_in parameter
    - fuel_exhaust_in: fuel_exhaust_in parameter
    - compressor_2_in: compressor_2_in parameter
    - fuel_coefficient_in: fuel_coefficient_in parameter
    - heating_efficiency_in: heating_efficiency_in parameter
    - auxiliary_heat_in: auxiliary_heat_in parameter
    - compressor_3_in: compressor_3_in parameter
    - fuel_base_in: fuel_base_in parameter

Outputs:
    - fuel_base_electric: fuel_base_electric result
    - other_electric_demand: other_electric_demand result
    - dissipated_auxiliary: dissipated_auxiliary result
    - net_electric: net_electric result
    - generator_loss: generator_loss result
    - net_shaft: net_shaft result
    - heating_electric: heating_electric result
    - cryo_electric: cryo_electric result
    - fuel_variable_electric: fuel_variable_electric result
    - compressor_demand: compressor_demand result
    - auxiliary_electric: auxiliary_electric result
    - gross_electric: gross_electric result
    - fuel_electric: fuel_electric result
    - primary_pump_electric: primary_pump_electric result
    - motor_loss: motor_loss result
    - shaft_import: shaft_import result
    - heating_loss: heating_loss result
    - pump_loss: pump_loss result
    - control_electric: control_electric result

SysML Source: root-0/integrated_heat_electricity.sysml:197

    SysML Source: root-0/integrated_heat_electricity.sysml:197

    Calculation Specification:
        See documentation:
*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: generator/auxiliary owner and electrical energy ledger equations; efficiencies dimensionless, rates atoms/s, all powers MW. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See combinations_tea.handwritten.integrated_heat_electricity.plant_electrical_balance_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts fuel_base_electric, other_electric_demand, dissipated_auxiliary, net_electric, generator_loss, net_shaft, heating_electric, cryo_electric, fuel_variable_electric, compressor_demand, auxiliary_electric, gross_electric, fuel_electric, primary_pump_electric, motor_loss, shaft_import, heating_loss, pump_loss, control_electric fields to separate channels.
    """

    name: str = "Plant_Electrical_BalanceModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, motor_efficiency_in: float, compressor_1_in: float, pump_electric_in: float, generator_efficiency_in: float, cryo_in: float, other_electric_in: float, control_in: float, turbine_work_in: float, pump_recovered_in: float, fuel_exhaust_in: float, compressor_2_in: float, fuel_coefficient_in: float, heating_efficiency_in: float, auxiliary_heat_in: float, compressor_3_in: float, fuel_base_in: float    ) -> Plant_Electrical_BalanceInput:
        """Validate inputs and fill defaults.

        Args:
            motor_efficiency_in: motor_efficiency_in input
            compressor_1_in: compressor_1_in input
            pump_electric_in: pump_electric_in input
            generator_efficiency_in: generator_efficiency_in input
            cryo_in: cryo_in input
            other_electric_in: other_electric_in input
            control_in: control_in input
            turbine_work_in: turbine_work_in input
            pump_recovered_in: pump_recovered_in input
            fuel_exhaust_in: fuel_exhaust_in input
            compressor_2_in: compressor_2_in input
            fuel_coefficient_in: fuel_coefficient_in input
            heating_efficiency_in: heating_efficiency_in input
            auxiliary_heat_in: auxiliary_heat_in input
            compressor_3_in: compressor_3_in input
            fuel_base_in: fuel_base_in input

        Returns:
            Validated input model
        """
        return Plant_Electrical_BalanceInput(motor_efficiency_in=motor_efficiency_in, compressor_1_in=compressor_1_in, pump_electric_in=pump_electric_in, generator_efficiency_in=generator_efficiency_in, cryo_in=cryo_in, other_electric_in=other_electric_in, control_in=control_in, turbine_work_in=turbine_work_in, pump_recovered_in=pump_recovered_in, fuel_exhaust_in=fuel_exhaust_in, compressor_2_in=compressor_2_in, fuel_coefficient_in=fuel_coefficient_in, heating_efficiency_in=heating_efficiency_in, auxiliary_heat_in=auxiliary_heat_in, compressor_3_in=compressor_3_in, fuel_base_in=fuel_base_in)

    def run(
        self, motor_efficiency_in: float, compressor_1_in: float, pump_electric_in: float, generator_efficiency_in: float, cryo_in: float, other_electric_in: float, control_in: float, turbine_work_in: float, pump_recovered_in: float, fuel_exhaust_in: float, compressor_2_in: float, fuel_coefficient_in: float, heating_efficiency_in: float, auxiliary_heat_in: float, compressor_3_in: float, fuel_base_in: float    ) -> ModuleResult[Plant_Electrical_BalanceOutput]:
        """Execute calculation.

        Args:
            motor_efficiency_in: motor_efficiency_in input
            compressor_1_in: compressor_1_in input
            pump_electric_in: pump_electric_in input
            generator_efficiency_in: generator_efficiency_in input
            cryo_in: cryo_in input
            other_electric_in: other_electric_in input
            control_in: control_in input
            turbine_work_in: turbine_work_in input
            pump_recovered_in: pump_recovered_in input
            fuel_exhaust_in: fuel_exhaust_in input
            compressor_2_in: compressor_2_in input
            fuel_coefficient_in: fuel_coefficient_in input
            heating_efficiency_in: heating_efficiency_in input
            auxiliary_heat_in: auxiliary_heat_in input
            compressor_3_in: compressor_3_in input
            fuel_base_in: fuel_base_in input

        Returns:
            Module result with Plant_Electrical_BalanceOutput (fuel_base_electric, other_electric_demand, dissipated_auxiliary, net_electric, generator_loss, net_shaft, heating_electric, cryo_electric, fuel_variable_electric, compressor_demand, auxiliary_electric, gross_electric, fuel_electric, primary_pump_electric, motor_loss, shaft_import, heating_loss, pump_loss, control_electric)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(motor_efficiency_in, compressor_1_in, pump_electric_in, generator_efficiency_in, cryo_in, other_electric_in, control_in, turbine_work_in, pump_recovered_in, fuel_exhaust_in, compressor_2_in, fuel_coefficient_in, heating_efficiency_in, auxiliary_heat_in, compressor_3_in, fuel_base_in)

        # Import handwritten implementation
        from combinations_tea.handwritten.integrated_heat_electricity.plant_electrical_balance_impl import (
            run_plant_electrical_balance,
        )

        # Execute implementation - returns tuple of values
        fuel_base_electric, other_electric_demand, dissipated_auxiliary, net_electric, generator_loss, net_shaft, heating_electric, cryo_electric, fuel_variable_electric, compressor_demand, auxiliary_electric, gross_electric, fuel_electric, primary_pump_electric, motor_loss, shaft_import, heating_loss, pump_loss, control_electric = run_plant_electrical_balance(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Plant_Electrical_BalanceOutput(
                fuel_base_electric=fuel_base_electric,
                other_electric_demand=other_electric_demand,
                dissipated_auxiliary=dissipated_auxiliary,
                net_electric=net_electric,
                generator_loss=generator_loss,
                net_shaft=net_shaft,
                heating_electric=heating_electric,
                cryo_electric=cryo_electric,
                fuel_variable_electric=fuel_variable_electric,
                compressor_demand=compressor_demand,
                auxiliary_electric=auxiliary_electric,
                gross_electric=gross_electric,
                fuel_electric=fuel_electric,
                primary_pump_electric=primary_pump_electric,
                motor_loss=motor_loss,
                shaft_import=shaft_import,
                heating_loss=heating_loss,
                pump_loss=pump_loss,
                control_electric=control_electric,
            )
        )
