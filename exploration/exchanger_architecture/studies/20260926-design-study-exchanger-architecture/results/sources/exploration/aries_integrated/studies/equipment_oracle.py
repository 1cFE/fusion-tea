"""Independent WI-090 arithmetic from accepted design; no generated imports.

Bindings to actual public inputs/outputs belong in oracle_entry.py. Helpers express
reviewed equations rather than calling the implementation under verification.
"""
from decimal import Decimal
from math import isfinite


def purchase(quantity, reference_quantity, reference_cost, factor=1., fixed=False):
    if not all(isfinite(x) for x in (quantity,reference_quantity,reference_cost,factor)):
        raise ValueError('nonfinite purchase input')
    if quantity<0 or reference_quantity<=0 or reference_cost<0 or factor<=0:
        raise ValueError('invalid purchase domain')
    return reference_cost*factor*(1. if fixed else quantity/reference_quantity)


def pump(flow, reference_flow, reference_power, efficiency, reference_efficiency=.8, fixed=False):
    if flow<0 or reference_flow<=0 or reference_power<0 or not 0<efficiency<=1:
        raise ValueError('invalid pump domain')
    return reference_power if fixed else reference_power*(flow/reference_flow)**3*reference_efficiency/efficiency


def exchanger(area, coefficient):
    if area<0 or coefficient<0:
        raise ValueError('negative heat exchanger input')
    return area*coefficient/1e6


def fuel(burn_rate, loss_rate, exhaust_rate, atom_mass, seconds_per_year, availability,
         selected_kg, residence_s, decay_constant, recovered_kg, price_musd_kg):
    if not 0<=availability<=1 or min(selected_kg,residence_s,recovered_kg,price_musd_kg)<0:
        raise ValueError('invalid selected fuel scenario')
    burn=burn_rate*atom_mass*seconds_per_year*availability
    loss=loss_rate*atom_mass*seconds_per_year*availability
    decay=selected_kg*decay_constant*seconds_per_year
    requirement=exhaust_rate*atom_mass*residence_s
    deficit=max(burn+loss+decay-recovered_kg,0.)
    return {'selected_atoms':selected_kg/atom_mass,'required_kg':requirement,
            'margin_kg':selected_kg-requirement,'annual_burn_kg':burn,
            'annual_loss_kg':loss,'annual_decay_kg':decay,
            'annual_external_kg':deficit,'annual_external_cost':deficit*price_musd_kg,
            'initial_stock_cost':selected_kg*price_musd_kg}


def schedule(life_fpy, availability, plant_years, event_amount):
    if life_fpy<=0 or not 0<availability<=1 or plant_years<=0 or event_amount<0:
        raise ValueError('invalid schedule domain')
    # Enumerate exact decimal event times: independent of an implementation using ceil.
    interval=Decimal(str(life_fpy))/Decimal(str(availability))
    end=Decimal(str(plant_years))
    dates=[]
    k=1
    while k*interval<end:
        dates.append(float(k*interval))
        k+=1
        if k>100000:
            raise ValueError('oracle schedule exceeds bounded diagnostic domain')
    return {'interval':float(interval),'count':len(dates),'event_times':dates,
            'lifetime_total':len(dates)*event_amount,'reserve':event_amount*availability/life_fpy}
