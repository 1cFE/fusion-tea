"""Integrated_Plant_LedgerModule Module Wrapper

TEAx module for Integrated_Plant_Ledger calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic integrated plant ledger. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - divertor_friction_in: divertor_friction_in parameter
    - electric_motor_loss_in: electric_motor_loss_in parameter
    - producer_mode_in: producer_mode_in parameter
    - reference_heater_temperature_in: reference_heater_temperature_in parameter
    - compressor_1_in: compressor_1_in parameter
    - auxiliary_heat_in: auxiliary_heat_in parameter
    - turbine_exhaust_in: turbine_exhaust_in parameter
    - pump_electric_in: pump_electric_in parameter
    - electric_cryo_electric_in: electric_cryo_electric_in parameter
    - electric_shaft_import_in: electric_shaft_import_in parameter
    - electric_auxiliary_electric_in: electric_auxiliary_electric_in parameter
    - pump_recovered_in: pump_recovered_in parameter
    - unmet_heat_in: unmet_heat_in parameter
    - intercooler_1_in: intercooler_1_in parameter
    - electric_control_electric_in: electric_control_electric_in parameter
    - divertor_available_in: divertor_available_in parameter
    - electric_fuel_electric_in: electric_fuel_electric_in parameter
    - electric_fuel_base_electric_in: electric_fuel_base_electric_in parameter
    - electric_primary_pump_electric_in: electric_primary_pump_electric_in parameter
    - reference_turbine_temperature_in: reference_turbine_temperature_in parameter
    - he_available_in: he_available_in parameter
    - electric_other_electric_demand_in: electric_other_electric_demand_in parameter
    - compressor_2_in: compressor_2_in parameter
    - expansion_factor_in: expansion_factor_in parameter
    - reference_fusion_in: reference_fusion_in parameter
    - electric_fuel_variable_electric_in: electric_fuel_variable_electric_in parameter
    - electric_heating_electric_in: electric_heating_electric_in parameter
    - reference_gross_in: reference_gross_in parameter
    - divertor_deposition_in: divertor_deposition_in parameter
    - turbine_work_in: turbine_work_in parameter
    - electric_generator_loss_in: electric_generator_loss_in parameter
    - pbli_available_in: pbli_available_in parameter
    - reference_net_in: reference_net_in parameter
    - accepted_heat_in: accepted_heat_in parameter
    - electric_compressor_demand_in: electric_compressor_demand_in parameter
    - electric_net_shaft_in: electric_net_shaft_in parameter
    - reference_blanket_deposition_in: reference_blanket_deposition_in parameter
    - closure_residual_in: closure_residual_in parameter
    - he_friction_in: he_friction_in parameter
    - recuperator_cold_out_in: recuperator_cold_out_in parameter
    - pbli_deposition_in: pbli_deposition_in parameter
    - heater_inlet_in: heater_inlet_in parameter
    - electric_heating_loss_in: electric_heating_loss_in parameter
    - electric_dissipated_auxiliary_in: electric_dissipated_auxiliary_in parameter
    - other_heat_in: other_heat_in parameter
    - he_deposition_in: he_deposition_in parameter
    - source_residual_in: source_residual_in parameter
    - compressor_3_in: compressor_3_in parameter
    - electric_pump_loss_in: electric_pump_loss_in parameter
    - nuclear_gain_in: nuclear_gain_in parameter
    - intercooler_2_in: intercooler_2_in parameter
    - fusion_power_in: fusion_power_in parameter
    - pbli_friction_in: pbli_friction_in parameter
    - electric_gross_electric_in: electric_gross_electric_in parameter
    - precooler_in: precooler_in parameter
    - electric_net_electric_in: electric_net_electric_in parameter
    - turbine_temperature_in: turbine_temperature_in parameter

Outputs:
    - supported_hydraulics: supported_hydraulics result
    - fuel_base_electric: fuel_base_electric result
    - comparison_fusion_difference: comparison_fusion_difference result
    - heating_loss: heating_loss result
    - assumed_auxiliary_demands: assumed_auxiliary_demands result
    - control_electric: control_electric result
    - net_shaft: net_shaft result
    - fuel_variable_electric: fuel_variable_electric result
    - plant_residual: plant_residual result
    - fuel_electric: fuel_electric result
    - recuperator_state_residual: recuperator_state_residual result
    - auxiliary_electric: auxiliary_electric result
    - comparison_blanket_deposition_difference: comparison_blanket_deposition_difference result
    - net_electric: net_electric result
    - efficiency_defined: efficiency_defined result
    - conditional_net_result: conditional_net_result result
    - energy_tolerance: energy_tolerance result
    - heating_electric: heating_electric result
    - primary_pump_electric: primary_pump_electric result
    - comparison_turbine_temperature_difference: comparison_turbine_temperature_difference result
    - thermal_efficiency: thermal_efficiency result
    - cycle_residual: cycle_residual result
    - cryo_electric: cryo_electric result
    - unmatched_source_heat: unmatched_source_heat result
    - generator_loss: generator_loss result
    - residual_magnitude: residual_magnitude result
    - comparison_gross_difference: comparison_gross_difference result
    - supported_deposition: supported_deposition result
    - source_energy_residual: source_energy_residual result
    - motor_loss: motor_loss result
    - other_electric_demand: other_electric_demand result
    - supported_materials: supported_materials result
    - dissipated_auxiliary: dissipated_auxiliary result
    - gross_electric: gross_electric result
    - branch_residual: branch_residual result
    - supported_magnet: supported_magnet result
    - supported_machine_map: supported_machine_map result
    - pump_loss: pump_loss result
    - electrical_residual: electrical_residual result
    - cycle_rejection: cycle_rejection result
    - shaft_import: shaft_import result
    - comparison_heater_temperature_difference: comparison_heater_temperature_difference result
    - supported_breeding: supported_breeding result
    - turbine_state_residual: turbine_state_residual result
    - compressor_demand: compressor_demand result
    - total_available_heat: total_available_heat result
    - comparison_net_difference: comparison_net_difference result
    - net_result_producer_mode: net_result_producer_mode result

SysML Source: root-0/integrated_heat_electricity.sysml:235

SysML Source: root-0/integrated_heat_electricity.sysml:235

GAP: Code generator does NOT implement calc logic - only wrapper structure.
Handwritten implementation required in handwritten/integrated_heat_electricity/integrated_plant_ledger_impl.py
"""

from pydantic import BaseModel, Field, RootModel
from simkit.core.base import ModuleBase, ModuleResult

from exchanger_architecture_thermal_tea.primitives import Float
from exchanger_architecture_thermal_tea.schemas.integrated_plant_ledger_output import Integrated_Plant_LedgerOutput


class Integrated_Plant_LedgerInput(BaseModel):
    """Input model for Integrated_Plant_LedgerModule.

    Attributes:
        divertor_friction_in: divertor_friction_in input
        electric_motor_loss_in: electric_motor_loss_in input
        producer_mode_in: producer_mode_in input
        reference_heater_temperature_in: reference_heater_temperature_in input
        compressor_1_in: compressor_1_in input
        auxiliary_heat_in: auxiliary_heat_in input
        turbine_exhaust_in: turbine_exhaust_in input
        pump_electric_in: pump_electric_in input
        electric_cryo_electric_in: electric_cryo_electric_in input
        electric_shaft_import_in: electric_shaft_import_in input
        electric_auxiliary_electric_in: electric_auxiliary_electric_in input
        pump_recovered_in: pump_recovered_in input
        unmet_heat_in: unmet_heat_in input
        intercooler_1_in: intercooler_1_in input
        electric_control_electric_in: electric_control_electric_in input
        divertor_available_in: divertor_available_in input
        electric_fuel_electric_in: electric_fuel_electric_in input
        electric_fuel_base_electric_in: electric_fuel_base_electric_in input
        electric_primary_pump_electric_in: electric_primary_pump_electric_in input
        reference_turbine_temperature_in: reference_turbine_temperature_in input
        he_available_in: he_available_in input
        electric_other_electric_demand_in: electric_other_electric_demand_in input
        compressor_2_in: compressor_2_in input
        expansion_factor_in: expansion_factor_in input
        reference_fusion_in: reference_fusion_in input
        electric_fuel_variable_electric_in: electric_fuel_variable_electric_in input
        electric_heating_electric_in: electric_heating_electric_in input
        reference_gross_in: reference_gross_in input
        divertor_deposition_in: divertor_deposition_in input
        turbine_work_in: turbine_work_in input
        electric_generator_loss_in: electric_generator_loss_in input
        pbli_available_in: pbli_available_in input
        reference_net_in: reference_net_in input
        accepted_heat_in: accepted_heat_in input
        electric_compressor_demand_in: electric_compressor_demand_in input
        electric_net_shaft_in: electric_net_shaft_in input
        reference_blanket_deposition_in: reference_blanket_deposition_in input
        closure_residual_in: closure_residual_in input
        he_friction_in: he_friction_in input
        recuperator_cold_out_in: recuperator_cold_out_in input
        pbli_deposition_in: pbli_deposition_in input
        heater_inlet_in: heater_inlet_in input
        electric_heating_loss_in: electric_heating_loss_in input
        electric_dissipated_auxiliary_in: electric_dissipated_auxiliary_in input
        other_heat_in: other_heat_in input
        he_deposition_in: he_deposition_in input
        source_residual_in: source_residual_in input
        compressor_3_in: compressor_3_in input
        electric_pump_loss_in: electric_pump_loss_in input
        nuclear_gain_in: nuclear_gain_in input
        intercooler_2_in: intercooler_2_in input
        fusion_power_in: fusion_power_in input
        pbli_friction_in: pbli_friction_in input
        electric_gross_electric_in: electric_gross_electric_in input
        precooler_in: precooler_in input
        electric_net_electric_in: electric_net_electric_in input
        turbine_temperature_in: turbine_temperature_in input
    """
    divertor_friction_in: float = Field(..., description="divertor_friction_in input")
    electric_motor_loss_in: float = Field(..., description="electric_motor_loss_in input")
    producer_mode_in: float = Field(..., description="producer_mode_in input")
    reference_heater_temperature_in: float = Field(..., description="reference_heater_temperature_in input")
    compressor_1_in: float = Field(..., description="compressor_1_in input")
    auxiliary_heat_in: float = Field(..., description="auxiliary_heat_in input")
    turbine_exhaust_in: float = Field(..., description="turbine_exhaust_in input")
    pump_electric_in: float = Field(..., description="pump_electric_in input")
    electric_cryo_electric_in: float = Field(..., description="electric_cryo_electric_in input")
    electric_shaft_import_in: float = Field(..., description="electric_shaft_import_in input")
    electric_auxiliary_electric_in: float = Field(..., description="electric_auxiliary_electric_in input")
    pump_recovered_in: float = Field(..., description="pump_recovered_in input")
    unmet_heat_in: float = Field(..., description="unmet_heat_in input")
    intercooler_1_in: float = Field(..., description="intercooler_1_in input")
    electric_control_electric_in: float = Field(..., description="electric_control_electric_in input")
    divertor_available_in: float = Field(..., description="divertor_available_in input")
    electric_fuel_electric_in: float = Field(..., description="electric_fuel_electric_in input")
    electric_fuel_base_electric_in: float = Field(..., description="electric_fuel_base_electric_in input")
    electric_primary_pump_electric_in: float = Field(..., description="electric_primary_pump_electric_in input")
    reference_turbine_temperature_in: float = Field(..., description="reference_turbine_temperature_in input")
    he_available_in: float = Field(..., description="he_available_in input")
    electric_other_electric_demand_in: float = Field(..., description="electric_other_electric_demand_in input")
    compressor_2_in: float = Field(..., description="compressor_2_in input")
    expansion_factor_in: float = Field(..., description="expansion_factor_in input")
    reference_fusion_in: float = Field(..., description="reference_fusion_in input")
    electric_fuel_variable_electric_in: float = Field(..., description="electric_fuel_variable_electric_in input")
    electric_heating_electric_in: float = Field(..., description="electric_heating_electric_in input")
    reference_gross_in: float = Field(..., description="reference_gross_in input")
    divertor_deposition_in: float = Field(..., description="divertor_deposition_in input")
    turbine_work_in: float = Field(..., description="turbine_work_in input")
    electric_generator_loss_in: float = Field(..., description="electric_generator_loss_in input")
    pbli_available_in: float = Field(..., description="pbli_available_in input")
    reference_net_in: float = Field(..., description="reference_net_in input")
    accepted_heat_in: float = Field(..., description="accepted_heat_in input")
    electric_compressor_demand_in: float = Field(..., description="electric_compressor_demand_in input")
    electric_net_shaft_in: float = Field(..., description="electric_net_shaft_in input")
    reference_blanket_deposition_in: float = Field(..., description="reference_blanket_deposition_in input")
    closure_residual_in: float = Field(..., description="closure_residual_in input")
    he_friction_in: float = Field(..., description="he_friction_in input")
    recuperator_cold_out_in: float = Field(..., description="recuperator_cold_out_in input")
    pbli_deposition_in: float = Field(..., description="pbli_deposition_in input")
    heater_inlet_in: float = Field(..., description="heater_inlet_in input")
    electric_heating_loss_in: float = Field(..., description="electric_heating_loss_in input")
    electric_dissipated_auxiliary_in: float = Field(..., description="electric_dissipated_auxiliary_in input")
    other_heat_in: float = Field(..., description="other_heat_in input")
    he_deposition_in: float = Field(..., description="he_deposition_in input")
    source_residual_in: float = Field(..., description="source_residual_in input")
    compressor_3_in: float = Field(..., description="compressor_3_in input")
    electric_pump_loss_in: float = Field(..., description="electric_pump_loss_in input")
    nuclear_gain_in: float = Field(..., description="nuclear_gain_in input")
    intercooler_2_in: float = Field(..., description="intercooler_2_in input")
    fusion_power_in: float = Field(..., description="fusion_power_in input")
    pbli_friction_in: float = Field(..., description="pbli_friction_in input")
    electric_gross_electric_in: float = Field(..., description="electric_gross_electric_in input")
    precooler_in: float = Field(..., description="precooler_in input")
    electric_net_electric_in: float = Field(..., description="electric_net_electric_in input")
    turbine_temperature_in: float = Field(..., description="turbine_temperature_in input")


class Integrated_Plant_LedgerModule(ModuleBase[Integrated_Plant_LedgerInput, Integrated_Plant_LedgerOutput]):
    """TEAx module for Integrated_Plant_Ledger calculation.

*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic integrated plant ledger. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

Inputs:
    - divertor_friction_in: divertor_friction_in parameter
    - electric_motor_loss_in: electric_motor_loss_in parameter
    - producer_mode_in: producer_mode_in parameter
    - reference_heater_temperature_in: reference_heater_temperature_in parameter
    - compressor_1_in: compressor_1_in parameter
    - auxiliary_heat_in: auxiliary_heat_in parameter
    - turbine_exhaust_in: turbine_exhaust_in parameter
    - pump_electric_in: pump_electric_in parameter
    - electric_cryo_electric_in: electric_cryo_electric_in parameter
    - electric_shaft_import_in: electric_shaft_import_in parameter
    - electric_auxiliary_electric_in: electric_auxiliary_electric_in parameter
    - pump_recovered_in: pump_recovered_in parameter
    - unmet_heat_in: unmet_heat_in parameter
    - intercooler_1_in: intercooler_1_in parameter
    - electric_control_electric_in: electric_control_electric_in parameter
    - divertor_available_in: divertor_available_in parameter
    - electric_fuel_electric_in: electric_fuel_electric_in parameter
    - electric_fuel_base_electric_in: electric_fuel_base_electric_in parameter
    - electric_primary_pump_electric_in: electric_primary_pump_electric_in parameter
    - reference_turbine_temperature_in: reference_turbine_temperature_in parameter
    - he_available_in: he_available_in parameter
    - electric_other_electric_demand_in: electric_other_electric_demand_in parameter
    - compressor_2_in: compressor_2_in parameter
    - expansion_factor_in: expansion_factor_in parameter
    - reference_fusion_in: reference_fusion_in parameter
    - electric_fuel_variable_electric_in: electric_fuel_variable_electric_in parameter
    - electric_heating_electric_in: electric_heating_electric_in parameter
    - reference_gross_in: reference_gross_in parameter
    - divertor_deposition_in: divertor_deposition_in parameter
    - turbine_work_in: turbine_work_in parameter
    - electric_generator_loss_in: electric_generator_loss_in parameter
    - pbli_available_in: pbli_available_in parameter
    - reference_net_in: reference_net_in parameter
    - accepted_heat_in: accepted_heat_in parameter
    - electric_compressor_demand_in: electric_compressor_demand_in parameter
    - electric_net_shaft_in: electric_net_shaft_in parameter
    - reference_blanket_deposition_in: reference_blanket_deposition_in parameter
    - closure_residual_in: closure_residual_in parameter
    - he_friction_in: he_friction_in parameter
    - recuperator_cold_out_in: recuperator_cold_out_in parameter
    - pbli_deposition_in: pbli_deposition_in parameter
    - heater_inlet_in: heater_inlet_in parameter
    - electric_heating_loss_in: electric_heating_loss_in parameter
    - electric_dissipated_auxiliary_in: electric_dissipated_auxiliary_in parameter
    - other_heat_in: other_heat_in parameter
    - he_deposition_in: he_deposition_in parameter
    - source_residual_in: source_residual_in parameter
    - compressor_3_in: compressor_3_in parameter
    - electric_pump_loss_in: electric_pump_loss_in parameter
    - nuclear_gain_in: nuclear_gain_in parameter
    - intercooler_2_in: intercooler_2_in parameter
    - fusion_power_in: fusion_power_in parameter
    - pbli_friction_in: pbli_friction_in parameter
    - electric_gross_electric_in: electric_gross_electric_in parameter
    - precooler_in: precooler_in parameter
    - electric_net_electric_in: electric_net_electric_in parameter
    - turbine_temperature_in: turbine_temperature_in parameter

Outputs:
    - supported_hydraulics: supported_hydraulics result
    - fuel_base_electric: fuel_base_electric result
    - comparison_fusion_difference: comparison_fusion_difference result
    - heating_loss: heating_loss result
    - assumed_auxiliary_demands: assumed_auxiliary_demands result
    - control_electric: control_electric result
    - net_shaft: net_shaft result
    - fuel_variable_electric: fuel_variable_electric result
    - plant_residual: plant_residual result
    - fuel_electric: fuel_electric result
    - recuperator_state_residual: recuperator_state_residual result
    - auxiliary_electric: auxiliary_electric result
    - comparison_blanket_deposition_difference: comparison_blanket_deposition_difference result
    - net_electric: net_electric result
    - efficiency_defined: efficiency_defined result
    - conditional_net_result: conditional_net_result result
    - energy_tolerance: energy_tolerance result
    - heating_electric: heating_electric result
    - primary_pump_electric: primary_pump_electric result
    - comparison_turbine_temperature_difference: comparison_turbine_temperature_difference result
    - thermal_efficiency: thermal_efficiency result
    - cycle_residual: cycle_residual result
    - cryo_electric: cryo_electric result
    - unmatched_source_heat: unmatched_source_heat result
    - generator_loss: generator_loss result
    - residual_magnitude: residual_magnitude result
    - comparison_gross_difference: comparison_gross_difference result
    - supported_deposition: supported_deposition result
    - source_energy_residual: source_energy_residual result
    - motor_loss: motor_loss result
    - other_electric_demand: other_electric_demand result
    - supported_materials: supported_materials result
    - dissipated_auxiliary: dissipated_auxiliary result
    - gross_electric: gross_electric result
    - branch_residual: branch_residual result
    - supported_magnet: supported_magnet result
    - supported_machine_map: supported_machine_map result
    - pump_loss: pump_loss result
    - electrical_residual: electrical_residual result
    - cycle_rejection: cycle_rejection result
    - shaft_import: shaft_import result
    - comparison_heater_temperature_difference: comparison_heater_temperature_difference result
    - supported_breeding: supported_breeding result
    - turbine_state_residual: turbine_state_residual result
    - compressor_demand: compressor_demand result
    - total_available_heat: total_available_heat result
    - comparison_net_difference: comparison_net_difference result
    - net_result_producer_mode: net_result_producer_mode result

SysML Source: root-0/integrated_heat_electricity.sysml:235

    SysML Source: root-0/integrated_heat_electricity.sysml:235

    Calculation Specification:
        See documentation:
*Source**: work/completed/20260922_WI-089_aries-integrated-heat-and-electricity/design.md. **Reference**: accepted WI-089 design and source/assumption register; generic integrated plant ledger. Normative equations, units and operating domains are in the named design sections; typed native completion enforces them. MW/K/MPa/kg/s/J per kg K/atoms per s as documented; dimensionless flags use 0/1. **Last Updated**: 2026-09-22.

    IMPLEMENTATION: See exchanger_architecture_thermal_tea.handwritten.integrated_heat_electricity.integrated_plant_ledger_impl
    for manual implementation.

    NOTE: Uses MultiOutput pattern for type-safe multi-output support.
    TEAx automatically extracts supported_hydraulics, fuel_base_electric, comparison_fusion_difference, heating_loss, assumed_auxiliary_demands, control_electric, net_shaft, fuel_variable_electric, plant_residual, fuel_electric, recuperator_state_residual, auxiliary_electric, comparison_blanket_deposition_difference, net_electric, efficiency_defined, conditional_net_result, energy_tolerance, heating_electric, primary_pump_electric, comparison_turbine_temperature_difference, thermal_efficiency, cycle_residual, cryo_electric, unmatched_source_heat, generator_loss, residual_magnitude, comparison_gross_difference, supported_deposition, source_energy_residual, motor_loss, other_electric_demand, supported_materials, dissipated_auxiliary, gross_electric, branch_residual, supported_magnet, supported_machine_map, pump_loss, electrical_residual, cycle_rejection, shaft_import, comparison_heater_temperature_difference, supported_breeding, turbine_state_residual, compressor_demand, total_available_heat, comparison_net_difference, net_result_producer_mode fields to separate channels.
    """

    name: str = "Integrated_Plant_LedgerModule"
    version: str = "v0.1"

    def validate_and_fill_default(
        self, divertor_friction_in: float, electric_motor_loss_in: float, producer_mode_in: float, reference_heater_temperature_in: float, compressor_1_in: float, auxiliary_heat_in: float, turbine_exhaust_in: float, pump_electric_in: float, electric_cryo_electric_in: float, electric_shaft_import_in: float, electric_auxiliary_electric_in: float, pump_recovered_in: float, unmet_heat_in: float, intercooler_1_in: float, electric_control_electric_in: float, divertor_available_in: float, electric_fuel_electric_in: float, electric_fuel_base_electric_in: float, electric_primary_pump_electric_in: float, reference_turbine_temperature_in: float, he_available_in: float, electric_other_electric_demand_in: float, compressor_2_in: float, expansion_factor_in: float, reference_fusion_in: float, electric_fuel_variable_electric_in: float, electric_heating_electric_in: float, reference_gross_in: float, divertor_deposition_in: float, turbine_work_in: float, electric_generator_loss_in: float, pbli_available_in: float, reference_net_in: float, accepted_heat_in: float, electric_compressor_demand_in: float, electric_net_shaft_in: float, reference_blanket_deposition_in: float, closure_residual_in: float, he_friction_in: float, recuperator_cold_out_in: float, pbli_deposition_in: float, heater_inlet_in: float, electric_heating_loss_in: float, electric_dissipated_auxiliary_in: float, other_heat_in: float, he_deposition_in: float, source_residual_in: float, compressor_3_in: float, electric_pump_loss_in: float, nuclear_gain_in: float, intercooler_2_in: float, fusion_power_in: float, pbli_friction_in: float, electric_gross_electric_in: float, precooler_in: float, electric_net_electric_in: float, turbine_temperature_in: float    ) -> Integrated_Plant_LedgerInput:
        """Validate inputs and fill defaults.

        Args:
            divertor_friction_in: divertor_friction_in input
            electric_motor_loss_in: electric_motor_loss_in input
            producer_mode_in: producer_mode_in input
            reference_heater_temperature_in: reference_heater_temperature_in input
            compressor_1_in: compressor_1_in input
            auxiliary_heat_in: auxiliary_heat_in input
            turbine_exhaust_in: turbine_exhaust_in input
            pump_electric_in: pump_electric_in input
            electric_cryo_electric_in: electric_cryo_electric_in input
            electric_shaft_import_in: electric_shaft_import_in input
            electric_auxiliary_electric_in: electric_auxiliary_electric_in input
            pump_recovered_in: pump_recovered_in input
            unmet_heat_in: unmet_heat_in input
            intercooler_1_in: intercooler_1_in input
            electric_control_electric_in: electric_control_electric_in input
            divertor_available_in: divertor_available_in input
            electric_fuel_electric_in: electric_fuel_electric_in input
            electric_fuel_base_electric_in: electric_fuel_base_electric_in input
            electric_primary_pump_electric_in: electric_primary_pump_electric_in input
            reference_turbine_temperature_in: reference_turbine_temperature_in input
            he_available_in: he_available_in input
            electric_other_electric_demand_in: electric_other_electric_demand_in input
            compressor_2_in: compressor_2_in input
            expansion_factor_in: expansion_factor_in input
            reference_fusion_in: reference_fusion_in input
            electric_fuel_variable_electric_in: electric_fuel_variable_electric_in input
            electric_heating_electric_in: electric_heating_electric_in input
            reference_gross_in: reference_gross_in input
            divertor_deposition_in: divertor_deposition_in input
            turbine_work_in: turbine_work_in input
            electric_generator_loss_in: electric_generator_loss_in input
            pbli_available_in: pbli_available_in input
            reference_net_in: reference_net_in input
            accepted_heat_in: accepted_heat_in input
            electric_compressor_demand_in: electric_compressor_demand_in input
            electric_net_shaft_in: electric_net_shaft_in input
            reference_blanket_deposition_in: reference_blanket_deposition_in input
            closure_residual_in: closure_residual_in input
            he_friction_in: he_friction_in input
            recuperator_cold_out_in: recuperator_cold_out_in input
            pbli_deposition_in: pbli_deposition_in input
            heater_inlet_in: heater_inlet_in input
            electric_heating_loss_in: electric_heating_loss_in input
            electric_dissipated_auxiliary_in: electric_dissipated_auxiliary_in input
            other_heat_in: other_heat_in input
            he_deposition_in: he_deposition_in input
            source_residual_in: source_residual_in input
            compressor_3_in: compressor_3_in input
            electric_pump_loss_in: electric_pump_loss_in input
            nuclear_gain_in: nuclear_gain_in input
            intercooler_2_in: intercooler_2_in input
            fusion_power_in: fusion_power_in input
            pbli_friction_in: pbli_friction_in input
            electric_gross_electric_in: electric_gross_electric_in input
            precooler_in: precooler_in input
            electric_net_electric_in: electric_net_electric_in input
            turbine_temperature_in: turbine_temperature_in input

        Returns:
            Validated input model
        """
        return Integrated_Plant_LedgerInput(divertor_friction_in=divertor_friction_in, electric_motor_loss_in=electric_motor_loss_in, producer_mode_in=producer_mode_in, reference_heater_temperature_in=reference_heater_temperature_in, compressor_1_in=compressor_1_in, auxiliary_heat_in=auxiliary_heat_in, turbine_exhaust_in=turbine_exhaust_in, pump_electric_in=pump_electric_in, electric_cryo_electric_in=electric_cryo_electric_in, electric_shaft_import_in=electric_shaft_import_in, electric_auxiliary_electric_in=electric_auxiliary_electric_in, pump_recovered_in=pump_recovered_in, unmet_heat_in=unmet_heat_in, intercooler_1_in=intercooler_1_in, electric_control_electric_in=electric_control_electric_in, divertor_available_in=divertor_available_in, electric_fuel_electric_in=electric_fuel_electric_in, electric_fuel_base_electric_in=electric_fuel_base_electric_in, electric_primary_pump_electric_in=electric_primary_pump_electric_in, reference_turbine_temperature_in=reference_turbine_temperature_in, he_available_in=he_available_in, electric_other_electric_demand_in=electric_other_electric_demand_in, compressor_2_in=compressor_2_in, expansion_factor_in=expansion_factor_in, reference_fusion_in=reference_fusion_in, electric_fuel_variable_electric_in=electric_fuel_variable_electric_in, electric_heating_electric_in=electric_heating_electric_in, reference_gross_in=reference_gross_in, divertor_deposition_in=divertor_deposition_in, turbine_work_in=turbine_work_in, electric_generator_loss_in=electric_generator_loss_in, pbli_available_in=pbli_available_in, reference_net_in=reference_net_in, accepted_heat_in=accepted_heat_in, electric_compressor_demand_in=electric_compressor_demand_in, electric_net_shaft_in=electric_net_shaft_in, reference_blanket_deposition_in=reference_blanket_deposition_in, closure_residual_in=closure_residual_in, he_friction_in=he_friction_in, recuperator_cold_out_in=recuperator_cold_out_in, pbli_deposition_in=pbli_deposition_in, heater_inlet_in=heater_inlet_in, electric_heating_loss_in=electric_heating_loss_in, electric_dissipated_auxiliary_in=electric_dissipated_auxiliary_in, other_heat_in=other_heat_in, he_deposition_in=he_deposition_in, source_residual_in=source_residual_in, compressor_3_in=compressor_3_in, electric_pump_loss_in=electric_pump_loss_in, nuclear_gain_in=nuclear_gain_in, intercooler_2_in=intercooler_2_in, fusion_power_in=fusion_power_in, pbli_friction_in=pbli_friction_in, electric_gross_electric_in=electric_gross_electric_in, precooler_in=precooler_in, electric_net_electric_in=electric_net_electric_in, turbine_temperature_in=turbine_temperature_in)

    def run(
        self, divertor_friction_in: float, electric_motor_loss_in: float, producer_mode_in: float, reference_heater_temperature_in: float, compressor_1_in: float, auxiliary_heat_in: float, turbine_exhaust_in: float, pump_electric_in: float, electric_cryo_electric_in: float, electric_shaft_import_in: float, electric_auxiliary_electric_in: float, pump_recovered_in: float, unmet_heat_in: float, intercooler_1_in: float, electric_control_electric_in: float, divertor_available_in: float, electric_fuel_electric_in: float, electric_fuel_base_electric_in: float, electric_primary_pump_electric_in: float, reference_turbine_temperature_in: float, he_available_in: float, electric_other_electric_demand_in: float, compressor_2_in: float, expansion_factor_in: float, reference_fusion_in: float, electric_fuel_variable_electric_in: float, electric_heating_electric_in: float, reference_gross_in: float, divertor_deposition_in: float, turbine_work_in: float, electric_generator_loss_in: float, pbli_available_in: float, reference_net_in: float, accepted_heat_in: float, electric_compressor_demand_in: float, electric_net_shaft_in: float, reference_blanket_deposition_in: float, closure_residual_in: float, he_friction_in: float, recuperator_cold_out_in: float, pbli_deposition_in: float, heater_inlet_in: float, electric_heating_loss_in: float, electric_dissipated_auxiliary_in: float, other_heat_in: float, he_deposition_in: float, source_residual_in: float, compressor_3_in: float, electric_pump_loss_in: float, nuclear_gain_in: float, intercooler_2_in: float, fusion_power_in: float, pbli_friction_in: float, electric_gross_electric_in: float, precooler_in: float, electric_net_electric_in: float, turbine_temperature_in: float    ) -> ModuleResult[Integrated_Plant_LedgerOutput]:
        """Execute calculation.

        Args:
            divertor_friction_in: divertor_friction_in input
            electric_motor_loss_in: electric_motor_loss_in input
            producer_mode_in: producer_mode_in input
            reference_heater_temperature_in: reference_heater_temperature_in input
            compressor_1_in: compressor_1_in input
            auxiliary_heat_in: auxiliary_heat_in input
            turbine_exhaust_in: turbine_exhaust_in input
            pump_electric_in: pump_electric_in input
            electric_cryo_electric_in: electric_cryo_electric_in input
            electric_shaft_import_in: electric_shaft_import_in input
            electric_auxiliary_electric_in: electric_auxiliary_electric_in input
            pump_recovered_in: pump_recovered_in input
            unmet_heat_in: unmet_heat_in input
            intercooler_1_in: intercooler_1_in input
            electric_control_electric_in: electric_control_electric_in input
            divertor_available_in: divertor_available_in input
            electric_fuel_electric_in: electric_fuel_electric_in input
            electric_fuel_base_electric_in: electric_fuel_base_electric_in input
            electric_primary_pump_electric_in: electric_primary_pump_electric_in input
            reference_turbine_temperature_in: reference_turbine_temperature_in input
            he_available_in: he_available_in input
            electric_other_electric_demand_in: electric_other_electric_demand_in input
            compressor_2_in: compressor_2_in input
            expansion_factor_in: expansion_factor_in input
            reference_fusion_in: reference_fusion_in input
            electric_fuel_variable_electric_in: electric_fuel_variable_electric_in input
            electric_heating_electric_in: electric_heating_electric_in input
            reference_gross_in: reference_gross_in input
            divertor_deposition_in: divertor_deposition_in input
            turbine_work_in: turbine_work_in input
            electric_generator_loss_in: electric_generator_loss_in input
            pbli_available_in: pbli_available_in input
            reference_net_in: reference_net_in input
            accepted_heat_in: accepted_heat_in input
            electric_compressor_demand_in: electric_compressor_demand_in input
            electric_net_shaft_in: electric_net_shaft_in input
            reference_blanket_deposition_in: reference_blanket_deposition_in input
            closure_residual_in: closure_residual_in input
            he_friction_in: he_friction_in input
            recuperator_cold_out_in: recuperator_cold_out_in input
            pbli_deposition_in: pbli_deposition_in input
            heater_inlet_in: heater_inlet_in input
            electric_heating_loss_in: electric_heating_loss_in input
            electric_dissipated_auxiliary_in: electric_dissipated_auxiliary_in input
            other_heat_in: other_heat_in input
            he_deposition_in: he_deposition_in input
            source_residual_in: source_residual_in input
            compressor_3_in: compressor_3_in input
            electric_pump_loss_in: electric_pump_loss_in input
            nuclear_gain_in: nuclear_gain_in input
            intercooler_2_in: intercooler_2_in input
            fusion_power_in: fusion_power_in input
            pbli_friction_in: pbli_friction_in input
            electric_gross_electric_in: electric_gross_electric_in input
            precooler_in: precooler_in input
            electric_net_electric_in: electric_net_electric_in input
            turbine_temperature_in: turbine_temperature_in input

        Returns:
            Module result with Integrated_Plant_LedgerOutput (supported_hydraulics, fuel_base_electric, comparison_fusion_difference, heating_loss, assumed_auxiliary_demands, control_electric, net_shaft, fuel_variable_electric, plant_residual, fuel_electric, recuperator_state_residual, auxiliary_electric, comparison_blanket_deposition_difference, net_electric, efficiency_defined, conditional_net_result, energy_tolerance, heating_electric, primary_pump_electric, comparison_turbine_temperature_difference, thermal_efficiency, cycle_residual, cryo_electric, unmatched_source_heat, generator_loss, residual_magnitude, comparison_gross_difference, supported_deposition, source_energy_residual, motor_loss, other_electric_demand, supported_materials, dissipated_auxiliary, gross_electric, branch_residual, supported_magnet, supported_machine_map, pump_loss, electrical_residual, cycle_rejection, shaft_import, comparison_heater_temperature_difference, supported_breeding, turbine_state_residual, compressor_demand, total_available_heat, comparison_net_difference, net_result_producer_mode)
        """
        # Validate inputs
        validated_inputs = self.validate_and_fill_default(divertor_friction_in, electric_motor_loss_in, producer_mode_in, reference_heater_temperature_in, compressor_1_in, auxiliary_heat_in, turbine_exhaust_in, pump_electric_in, electric_cryo_electric_in, electric_shaft_import_in, electric_auxiliary_electric_in, pump_recovered_in, unmet_heat_in, intercooler_1_in, electric_control_electric_in, divertor_available_in, electric_fuel_electric_in, electric_fuel_base_electric_in, electric_primary_pump_electric_in, reference_turbine_temperature_in, he_available_in, electric_other_electric_demand_in, compressor_2_in, expansion_factor_in, reference_fusion_in, electric_fuel_variable_electric_in, electric_heating_electric_in, reference_gross_in, divertor_deposition_in, turbine_work_in, electric_generator_loss_in, pbli_available_in, reference_net_in, accepted_heat_in, electric_compressor_demand_in, electric_net_shaft_in, reference_blanket_deposition_in, closure_residual_in, he_friction_in, recuperator_cold_out_in, pbli_deposition_in, heater_inlet_in, electric_heating_loss_in, electric_dissipated_auxiliary_in, other_heat_in, he_deposition_in, source_residual_in, compressor_3_in, electric_pump_loss_in, nuclear_gain_in, intercooler_2_in, fusion_power_in, pbli_friction_in, electric_gross_electric_in, precooler_in, electric_net_electric_in, turbine_temperature_in)

        # Import handwritten implementation
        from exchanger_architecture_thermal_tea.handwritten.integrated_heat_electricity.integrated_plant_ledger_impl import (
            run_integrated_plant_ledger,
        )

        # Execute implementation - returns tuple of values
        supported_hydraulics, fuel_base_electric, comparison_fusion_difference, heating_loss, assumed_auxiliary_demands, control_electric, net_shaft, fuel_variable_electric, plant_residual, fuel_electric, recuperator_state_residual, auxiliary_electric, comparison_blanket_deposition_difference, net_electric, efficiency_defined, conditional_net_result, energy_tolerance, heating_electric, primary_pump_electric, comparison_turbine_temperature_difference, thermal_efficiency, cycle_residual, cryo_electric, unmatched_source_heat, generator_loss, residual_magnitude, comparison_gross_difference, supported_deposition, source_energy_residual, motor_loss, other_electric_demand, supported_materials, dissipated_auxiliary, gross_electric, branch_residual, supported_magnet, supported_machine_map, pump_loss, electrical_residual, cycle_rejection, shaft_import, comparison_heater_temperature_difference, supported_breeding, turbine_state_residual, compressor_demand, total_available_heat, comparison_net_difference, net_result_producer_mode = run_integrated_plant_ledger(validated_inputs)


        # Return MultiOutput container (TEAx auto-extracts to channels)
        # MultiOutput fields use plain float (not RootModel[float])
        return ModuleResult(
            data=Integrated_Plant_LedgerOutput(
                supported_hydraulics=supported_hydraulics,
                fuel_base_electric=fuel_base_electric,
                comparison_fusion_difference=comparison_fusion_difference,
                heating_loss=heating_loss,
                assumed_auxiliary_demands=assumed_auxiliary_demands,
                control_electric=control_electric,
                net_shaft=net_shaft,
                fuel_variable_electric=fuel_variable_electric,
                plant_residual=plant_residual,
                fuel_electric=fuel_electric,
                recuperator_state_residual=recuperator_state_residual,
                auxiliary_electric=auxiliary_electric,
                comparison_blanket_deposition_difference=comparison_blanket_deposition_difference,
                net_electric=net_electric,
                efficiency_defined=efficiency_defined,
                conditional_net_result=conditional_net_result,
                energy_tolerance=energy_tolerance,
                heating_electric=heating_electric,
                primary_pump_electric=primary_pump_electric,
                comparison_turbine_temperature_difference=comparison_turbine_temperature_difference,
                thermal_efficiency=thermal_efficiency,
                cycle_residual=cycle_residual,
                cryo_electric=cryo_electric,
                unmatched_source_heat=unmatched_source_heat,
                generator_loss=generator_loss,
                residual_magnitude=residual_magnitude,
                comparison_gross_difference=comparison_gross_difference,
                supported_deposition=supported_deposition,
                source_energy_residual=source_energy_residual,
                motor_loss=motor_loss,
                other_electric_demand=other_electric_demand,
                supported_materials=supported_materials,
                dissipated_auxiliary=dissipated_auxiliary,
                gross_electric=gross_electric,
                branch_residual=branch_residual,
                supported_magnet=supported_magnet,
                supported_machine_map=supported_machine_map,
                pump_loss=pump_loss,
                electrical_residual=electrical_residual,
                cycle_rejection=cycle_rejection,
                shaft_import=shaft_import,
                comparison_heater_temperature_difference=comparison_heater_temperature_difference,
                supported_breeding=supported_breeding,
                turbine_state_residual=turbine_state_residual,
                compressor_demand=compressor_demand,
                total_available_heat=total_available_heat,
                comparison_net_difference=comparison_net_difference,
                net_result_producer_mode=net_result_producer_mode,
            )
        )
