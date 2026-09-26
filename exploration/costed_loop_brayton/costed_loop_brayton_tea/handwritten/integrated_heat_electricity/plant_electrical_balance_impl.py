"""Generator/auxiliary occurrence owns conversion and disjoint plant demands."""
from costed_loop_brayton_tea.handwritten.integrated_heat_electricity.common import values, require, finish
AUTO_IMPLEMENTED = False


def _reviewed_run_plant_electrical_balance(inputs):
    v = values(inputs)
    require(all(x >= 0 for x in v.values()), 'electrical inputs must be nonnegative')
    for key in ('heating_efficiency','generator_efficiency','motor_efficiency'):
        require(0 < v[key] <= 1, key+' must be in (0,1]')
    require(v['pump_recovered'] <= v['pump_electric'], 'recovered pump heat exceeds electricity')
    compressors = sum(v['compressor_'+str(i)] for i in (1,2,3))
    shaft = v['turbine_work']-compressors
    gross = v['generator_efficiency']*max(shaft,0.)
    imported = max(-shaft,0.)/v['motor_efficiency']
    heating = v['auxiliary_heat']/v['heating_efficiency']
    fuel_variable = v['fuel_coefficient']*v['fuel_exhaust']
    fuel = v['fuel_base']+fuel_variable
    dissipated = v['cryo']+fuel+v['control']+v['other_electric']
    auxiliary = v['pump_electric']+heating+dissipated
    return finish('plant_electrical_balance',dict(compressor_demand=compressors,net_shaft=shaft,
        gross_electric=gross,shaft_import=imported,generator_loss=(1-v['generator_efficiency'])*max(shaft,0.),
        motor_loss=(1/v['motor_efficiency']-1)*max(-shaft,0.),heating_electric=heating,
        heating_loss=heating-v['auxiliary_heat'],fuel_electric=fuel,fuel_base_electric=v['fuel_base'],
        fuel_variable_electric=fuel_variable,auxiliary_electric=auxiliary,net_electric=gross-imported-auxiliary,
        pump_loss=v['pump_electric']-v['pump_recovered'],dissipated_auxiliary=dissipated,
        cryo_electric=v['cryo'],control_electric=v['control'],other_electric_demand=v['other_electric'],
        primary_pump_electric=v['pump_electric']))


from costed_loop_brayton_tea.modules.integrated_heat_electricity.plant_electrical_balance import Plant_Electrical_BalanceInput


def run_plant_electrical_balance(inputs: Plant_Electrical_BalanceInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float, float]:
    """Typed native adapter; delegates unchanged reviewed calculation."""
    return _reviewed_run_plant_electrical_balance(inputs)
