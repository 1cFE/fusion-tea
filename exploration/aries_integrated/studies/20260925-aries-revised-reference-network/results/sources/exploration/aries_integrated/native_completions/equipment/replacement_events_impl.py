"""Reviewed native calculation; emitted from WI-090 authoring record."""
import math
from aries_integrated.handwritten.integrated_equipment_costs.common import values, require, finish
AUTO_IMPLEMENTED = False

def run_replacement_events(inputs):
    v = values(inputs)
    require(v['event_cost']>=0 and v['life_fpy']>0 and v['plant_years']>0 and 0<v['availability']<=1, 'invalid replacement schedule')
    interval=v['life_fpy']/v['availability']
    n=max(0,math.ceil(v['plant_years']/interval)-1)
    require(n<1000000, 'replacement event count outside supported bound')
    result=dict(event_cost=v['event_cost'],interval_years=interval,event_count=float(n),lifetime_total=n*v['event_cost'],annual_reserve=v['event_cost']/interval,first_event_year=interval if n else 0.,last_event_year=n*interval)
    return finish('replacement_events', result)
