"""Reviewed C1 correction: assumed mean nuclear heat, fixed native inventory/capacity.
Cold Load Sum and fraction-of-Carnot equations; no transport scaling claim.
"""
import math
AUTO_IMPLEMENTED=False
INPUTS=dict(q_nuc_W_m3=35.5,extra_cold_W=0.,cold_volume_m3=307.2600000000001,inventory_cold_W=9322.57888517031,fixed_cold_MW=.0075,intercept_inventory_W=41189.504334608944,cold_temperature_K=20.,intercept_temperature_K=77.,ambient_temperature_K=300.,cold_carnot_fraction=.2,intercept_carnot_fraction=.2,cold_rating_W=40000.,intercept_rating_W=60000.)
OUTPUTS='cold_W intercept_W cold_electric_MW intercept_electric_MW refrigeration_MW cold_margin_W intercept_margin_W q_nuc_capacity_W_m3 extra_cold_capacity_W nuclear_transport_qualified domain_supported'.split()
def calculate(x):
    if any(not math.isfinite(v) for v in x.values()) or min(x['q_nuc_W_m3'],x['extra_cold_W'])<0:raise ValueError('finite nonnegative cryogenic heating demands required')
    if not(0<x['cold_temperature_K']<x['ambient_temperature_K'] and 0<x['intercept_temperature_K']<x['ambient_temperature_K'] and min(x['cold_volume_m3'],x['cold_carnot_fraction'],x['intercept_carnot_fraction'])>0):raise ValueError('cryogenic temperature/COP domain')
    cold=(x['q_nuc_W_m3']*x['cold_volume_m3']+x['extra_cold_W'])*1e-6+x['fixed_cold_MW']+x['inventory_cold_W']*1e-6
    intercept=x['intercept_inventory_W'];ce=cold*(x['ambient_temperature_K']-x['cold_temperature_K'])/(x['cold_carnot_fraction']*x['cold_temperature_K']);ie=intercept*1e-6*(x['ambient_temperature_K']-x['intercept_temperature_K'])/(x['intercept_carnot_fraction']*x['intercept_temperature_K'])
    return dict(cold_W=cold*1e6,intercept_W=intercept,cold_electric_MW=ce,intercept_electric_MW=ie,refrigeration_MW=ce+ie,cold_margin_W=x['cold_rating_W']-cold*1e6,intercept_margin_W=x['intercept_rating_W']-intercept,q_nuc_capacity_W_m3=(x['cold_rating_W']-x['inventory_cold_W']-x['fixed_cold_MW']*1e6-x['extra_cold_W'])/x['cold_volume_m3'],extra_cold_capacity_W=x['cold_rating_W']-x['inventory_cold_W']-x['fixed_cold_MW']*1e6-x['q_nuc_W_m3']*x['cold_volume_m3'],nuclear_transport_qualified=0.,domain_supported=float(min(x.values())>=0 and max(x['cold_carnot_fraction'],x['intercept_carnot_fraction'])<=1))
