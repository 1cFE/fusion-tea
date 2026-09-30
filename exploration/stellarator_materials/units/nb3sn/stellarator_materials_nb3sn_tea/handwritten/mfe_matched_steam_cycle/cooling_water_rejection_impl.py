"""WI-073 conditional cooling-water circulation, including its own heat input."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from stellarator_materials_nb3sn_tea.modules.mfe_matched_steam_cycle.cooling_water_rejection import Cooling_Water_RejectionInput

if __package__:
    from .matched_steam_cycle_impl import mode, finite, efficiency, positive, property_tables, state_temperature, balance
else:
    from matched_steam_cycle_impl import mode, finite, efficiency, positive, property_tables, state_temperature, balance

AUTO_IMPLEMENTED = False
INPUT_NAMES = ('enabled','cycle_active','q_rejection_before_cooling_MW','condenser_temperature_C',
    'water_inlet_C','water_outlet_C','head_m','eta_pump','eta_motor')
REAL_OUTPUTS = ('water_flow_kg_s','p_cooling_pump_shaft_MW','p_cooling_pump_electric_MW',
    'q_cooling_motor_loss_MW','q_total_rejection_MW','water_pump_rise_K',
    'condenser_water_gap_K','water_energy_residual_MW','denominator_kJ_kg')
BOOL_OUTPUTS = ('active','reference_scenario','site_qualified','cooling_approach_ok')
# Synchronize with actual generated stencil before native package integration.
GENERATED_OUTPUT_ORDER = ('site_qualified', 'cooling_approach_ok', 'q_cooling_motor_loss_MW', 'water_flow_kg_s', 'water_energy_residual_MW', 'reference_scenario', 'condenser_water_gap_K', 'q_total_rejection_MW', 'p_cooling_pump_electric_MW', 'p_cooling_pump_shaft_MW', 'water_pump_rise_K', 'active', 'denominator_kJ_kg')


def calculate(parameters):
    result = dict.fromkeys(REAL_OUTPUTS,0.) | dict.fromkeys(BOOL_OUTPUTS,False)
    if not mode(parameters['enabled'],'cooling-water enabled'):
        return result
    if not mode(parameters['cycle_active'],'cooling-water cycle active'):
        raise ValueError('WI-073 cooling water: enabled cooling requires matched cycle enabled')
    p = {name:finite(parameters[name],name) for name in INPUT_NAMES}
    for name in ('eta_pump','eta_motor'):
        efficiency(p[name],name)
    positive(p['q_rejection_before_cooling_MW'],'cycle rejection heat')
    if p['head_m'] < 0:
        raise ValueError('WI-073 cooling water: nonnegative pump head required')
    if not 20 <= p['water_inlet_C'] < p['water_outlet_C'] <= 60:
        raise ValueError('WI-073 cooling water: require 20 <= inlet < outlet <= 60 C')
    if not 20 <= p['condenser_temperature_C'] <= 60:
        raise ValueError('WI-073 cooling water: condenser outside 20..60 C')
    rows = property_tables()['saturation']
    inlet = state_temperature(rows,p['water_inlet_C'],'liquid')
    outlet = state_temperature(rows,p['water_outlet_C'],'liquid')
    dh = outlet['h']-inlet['h']
    specific_shaft = 9.80665*p['head_m']/p['eta_pump']/1000
    specific_electric = specific_shaft/p['eta_motor']
    denominator = dh-specific_electric
    positive(denominator,'cooling-water energy denominator')
    flow = p['q_rejection_before_cooling_MW']*1000/denominator
    positive(flow,'cooling-water mass flow')
    shaft,electric = flow*specific_shaft/1000,flow*specific_electric/1000
    rejection = p['q_rejection_before_cooling_MW']+electric
    residual = flow*dh/1000-rejection
    balance(residual,rejection,'cooling-water heat')
    gap = p['condenser_temperature_C']-p['water_outlet_C']
    result.update(water_flow_kg_s=flow,p_cooling_pump_shaft_MW=shaft,
        p_cooling_pump_electric_MW=electric,q_cooling_motor_loss_MW=electric-shaft,
        q_total_rejection_MW=rejection,water_pump_rise_K=specific_electric/(dh/(p['water_outlet_C']-p['water_inlet_C'])),
        condenser_water_gap_K=gap,water_energy_residual_MW=residual,
        denominator_kJ_kg=denominator,active=True,reference_scenario=True,cooling_approach_ok=gap>0)
    for name in REAL_OUTPUTS:
        finite(result[name],name)
    return result


def run_cooling_water_rejection(inputs: Cooling_Water_RejectionInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float, float]:
    result=calculate({name:getattr(inputs,name+'_in') for name in INPUT_NAMES})
    return tuple(result[name] for name in GENERATED_OUTPUT_ORDER)
