"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_selected_flow_pump(inputs):
    v = values(inputs)
    require(v['flow']>=0 and v['reference_flow']>0 and v['reference_power']>=0 and v['fixed_power']>=0, 'invalid pump flow/power')
    require(0<v['efficiency']<=1 and 0<v['reference_efficiency']<=1, 'pump efficiency must be in (0,1]')
    require(v['mode'] in (0,1), 'pump mode must be 0 proxy or 1 fixed-source')
    p=v['fixed_power'] if v['mode']==1 else v['reference_power']*(v['flow']/v['reference_flow'])**3*v['reference_efficiency']/v['efficiency']
    result=dict(electric=p,hydraulic_supported=0.,operating_flow=v['flow'],mode=v['mode'])
    return finish('selected_flow_pump', result)
