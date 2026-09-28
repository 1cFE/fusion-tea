"""Whole-plant electricity and separately supplied common rejection boundary."""
import math
AUTO_IMPLEMENTED=False
INPUTS=dict(conversion_net_MW=0.,primary_electric_MW=0.,primary_fluid_MW=0.,heating_wall_MW=100.,deposited_heating_MW=50.,coil_drive_MW=0.,refrigeration_MW=0.,cold_W=0.,intercept_W=0.,tf_cooling_MW=15.,pf_cooling_MW=0.,fuel_vacuum_MW=10.,house_MW=4.,reactor_controls_MW=36.5999451053,residual_MW=5.,auxiliary_electric_MW=2.,auxiliary_rating_MW=200.,auxiliary_water_C=25.,availability=.8,import_price=50.)
OUTPUTS='upstream_electric_MW net_export_MW standby_MW annual_export_MWh annual_import_MWh annual_net_grid_MWh annual_import_cost auxiliary_heat_MW auxiliary_margin_MW primary_motor_loss_MW power_residual domain_supported'.split()
def calculate(x):
    keys='primary_electric_MW heating_wall_MW coil_drive_MW refrigeration_MW tf_cooling_MW pf_cooling_MW fuel_vacuum_MW house_MW reactor_controls_MW residual_MW auxiliary_electric_MW'.split()
    up=math.fsum(x[k] for k in keys);net=x['conversion_net_MW']-up
    motor=x['primary_electric_MW']-x['primary_fluid_MW']
    q=up-x['primary_fluid_MW']-x['deposited_heating_MW']-x['coil_drive_MW']+(x['cold_W']+x['intercept_W'])/1e6
    standby=x['refrigeration_MW']+x['house_MW']+x['auxiliary_electric_MW']
    e=8760*x['availability']*net;i=8760*(1-x['availability'])*standby
    return dict(upstream_electric_MW=up,net_export_MW=net,standby_MW=standby,annual_export_MWh=e,annual_import_MWh=i,annual_net_grid_MWh=e-i,annual_import_cost=i*x['import_price'],auxiliary_heat_MW=q,auxiliary_margin_MW=x['auxiliary_rating_MW']-q,primary_motor_loss_MW=motor,power_residual=x['conversion_net_MW']-net-up,domain_supported=float(0<x['availability']<=1 and x['auxiliary_water_C']==25. and min(x[k] for k in keys)>=0 and motor>=-1e-10))

from whole_plant_conversion_tea.modules.whole_plant_conversion_accounts.whole_plant_operating_ledger import Whole_Plant_Operating_LedgerInput

def _native_result(inputs):
    result=calculate({k.removesuffix('_in'):v for k,v in inputs.model_dump().items()})
    return tuple(result[k] for k in ['auxiliary_margin_MW', 'annual_net_grid_MWh', 'domain_supported', 'annual_import_MWh', 'power_residual', 'annual_export_MWh', 'annual_import_cost', 'net_export_MW', 'standby_MW', 'primary_motor_loss_MW', 'upstream_electric_MW', 'auxiliary_heat_MW'])

def run_whole_plant_operating_ledger(inputs: Whole_Plant_Operating_LedgerInput) -> tuple[float, float, float, float, float, float, float, float, float, float, float, float]:
    return _native_result(inputs)
