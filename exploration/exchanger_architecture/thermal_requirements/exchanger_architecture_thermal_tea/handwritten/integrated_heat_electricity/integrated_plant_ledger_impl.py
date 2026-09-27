"""Single-count shaft/electric/heat ledger with explicit conditional support.

Whole-boundary unmet source heat is an unremoved requirement, not physical rejection.
Source mismatch remains signed and causes the balance gate to fail in literal mode.
"""
from exchanger_architecture_thermal_tea.handwritten.integrated_heat_electricity.common import values, require, finish
AUTO_IMPLEMENTED = False


def _reviewed_run_integrated_plant_ledger(inputs):
    v = values(inputs)
    signed = {'source_residual','intercooler_1','intercooler_2','precooler','closure_residual','electric_net_shaft','electric_net_electric'}
    for key,value in v.items():
        if key not in signed:
            require(value >= 0, key+' must be nonnegative')
    for key in ('intercooler_1','intercooler_2','precooler'):
        require(v[key] <= 0, key+' must reject heat')
    e = {k.removeprefix('electric_'): value for k, value in v.items() if k.startswith('electric_')}
    compressors = e['compressor_demand']
    net_shaft = e['net_shaft']
    gross = e['gross_electric']
    imported = e['shaft_import']
    gen_loss = e['generator_loss']
    motor_loss = e['motor_loss']
    heating = e['heating_electric']
    heating_loss = e['heating_loss']
    fuel = e['fuel_electric']
    dissipated = e['dissipated_auxiliary']
    auxiliary = e['auxiliary_electric']
    net = e['net_electric']
    rejection = -sum(v[k] for k in ('intercooler_1','intercooler_2','precooler'))
    available = sum(v[b+'_available'] for b in ('he','pbli','divertor'))
    deposited = sum(v[b+'_deposition'] for b in ('he','pbli','divertor'))
    friction = sum(v[b+'_friction'] for b in ('he','pbli','divertor'))
    branch_residual = available-deposited-friction
    cycle_residual = v['accepted_heat']-rejection-net_shaft
    electric_residual = gross-imported-auxiliary-net
    pump_loss = e['pump_loss']
    sinks = v['other_heat']+v['unmet_heat']+rejection+gen_loss+motor_loss+pump_loss+heating_loss+dissipated
    plant_residual = v['fusion_power']+v['nuclear_gain']-net-sinks
    turbine_residual = v['turbine_exhaust']-v['expansion_factor']*v['turbine_temperature']
    recuperator_residual = v['recuperator_cold_out']-v['heater_inlet']
    tol = max(1e-6,1e-9*(v['fusion_power']+v['nuclear_gain']+v['auxiliary_heat']+v['pump_recovered']))
    magnitude = max(abs(x) for x in (branch_residual,cycle_residual,electric_residual,plant_residual,v['source_residual'],v['closure_residual']))
    out = dict(compressor_demand=compressors,net_shaft=net_shaft,cycle_rejection=rejection,gross_electric=gross,
               shaft_import=imported,generator_loss=gen_loss,motor_loss=motor_loss,heating_electric=heating,
               heating_loss=heating_loss,fuel_electric=fuel,fuel_base_electric=e['fuel_base_electric'],fuel_variable_electric=e['fuel_variable_electric'],auxiliary_electric=auxiliary,net_electric=net,
               pump_loss=pump_loss,dissipated_auxiliary=dissipated,branch_residual=branch_residual,
               cycle_residual=cycle_residual,electrical_residual=electric_residual,plant_residual=plant_residual,
               source_energy_residual=v['source_residual'],unmatched_source_heat=v['unmet_heat'],
               energy_tolerance=tol,residual_magnitude=magnitude,
               thermal_efficiency=gross/v['accepted_heat'] if v['accepted_heat']>0 else 0.,
               efficiency_defined=float(v['accepted_heat']>0),total_available_heat=available,
               comparison_fusion_difference=v['fusion_power']-v['reference_fusion'],
               comparison_gross_difference=gross-v['reference_gross'],comparison_net_difference=net-v['reference_net'],
               comparison_turbine_temperature_difference=v['turbine_temperature']-v['reference_turbine_temperature'],
               comparison_heater_temperature_difference=v['heater_inlet']-v['reference_heater_temperature'],
               comparison_blanket_deposition_difference=v['he_deposition']+v['pbli_deposition']-v['reference_blanket_deposition'],
               turbine_state_residual=turbine_residual,recuperator_state_residual=recuperator_residual,
               supported_magnet=0.,supported_breeding=0.,supported_deposition=0.,supported_hydraulics=0.,
               supported_materials=0.,supported_machine_map=0.,assumed_auxiliary_demands=1.,conditional_net_result=1.,net_result_producer_mode=v['producer_mode'],
               cryo_electric=e['cryo_electric'],control_electric=e['control_electric'],other_electric_demand=e['other_electric_demand'],primary_pump_electric=e['primary_pump_electric'])
    return finish('integrated_plant_ledger',out)


from exchanger_architecture_thermal_tea.modules.integrated_heat_electricity.integrated_plant_ledger import Integrated_Plant_LedgerInput


def run_integrated_plant_ledger(inputs: Integrated_Plant_LedgerInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_integrated_plant_ledger(inputs)
