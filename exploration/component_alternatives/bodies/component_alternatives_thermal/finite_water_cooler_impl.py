"""WI-096 piecewise-property counterflow cooler with model-owned water solve.

Q is minus the gas conditioning component's heat_into_fluid [MW]. Exact segment
integration uses the retained steam property table; pump electric work precedes HX.
No root returns a defined failed receipt; property and sign domain errors refuse.
"""
import math
AUTO_IMPLEMENTED=False
INPUTS=dict(gas_inlet_K=369.,gas_outlet_K=308.15,gas_heat_into_fluid=-600.,ua=25.,water_inlet_C=25.,head=20.,eta_p=.8,eta_motor=.95,flow_rating=100000.,power_rating=30.,duty_rating=2000.)
OUTPUTS='evaluation_defined failure_code duty water_inlet_after_C water_outlet_C water_flow pump_electric total_rejection min_gap required_ua ua_residual energy_residual flow_margin power_margin duty_margin bracket_low_ua bracket_high_ua iterations'.split()
def calculate(x):
    from component_alternatives_tea.handwritten.mfe_matched_steam_cycle.matched_steam_cycle_impl import property_tables,interpolate
    if any(not math.isfinite(v) for v in x.values()): raise ValueError('nonfinite cooler input')
    q=-x['gas_heat_into_fluid'];hot=x['gas_inlet_K']-273.15;cold=x['gas_outlet_K']-273.15
    if q<=0 or hot<=cold or x['ua']<=0: raise ValueError('cooler requires positive cooling and UA')
    if not (20<=x['water_inlet_C']<60 and x['head']>=0 and 0<x['eta_p']<=1 and 0<x['eta_motor']<=1):
        raise ValueError('cooler water/property/pump domain')
    rows=sorted([r for r in property_tables()['saturation'] if r['phase']=='liquid'],key=lambda r:r['T'])
    h=lambda t:interpolate(rows,'T',t,'h');t=lambda ent:interpolate(rows,'h',ent,'T')
    e=9.80665*x['head']/(x['eta_p']*x['eta_motor'])/1000
    hr=h(x['water_inlet_C']);ha=hr+e;ta=t(ha)
    out=dict.fromkeys(OUTPUTS,0.)
    out.update(duty=q,water_inlet_after_C=ta,duty_margin=x['duty_rating']-q)
    upper=min(hot,60.)
    if ta>=upper or cold<=ta:
        out.update(failure_code=1.,min_gap=cold-ta)
        return out
    def at(tout):
        mdot=1000*q/(h(tout)-ha)
        knots=sorted([0.,q]+[(r['h']-ha)*mdot/1000 for r in rows if ha<r['h']<h(tout)])
        gaps=[cold+(hot-cold)*z/q-t(ha+1000*z/mdot) for z in knots]
        if min(gaps)<=0: raise ValueError('cooler profile pinch')
        ua=math.fsum((b-a)*(math.log1p((gb-ga)/ga)/(gb-ga) if gb!=ga else 1/ga)
          for a,b,ga,gb in zip(knots,knots[1:],gaps,gaps[1:]))
        return ua,mdot,min(gaps)
    lo=ta+1e-7;hi=upper-1e-7
    if lo>=hi:
        out.update(failure_code=1.)
        return out
    al=at(lo)[0];ah=at(hi)[0]
    out.update(bracket_low_ua=al,bracket_high_ua=ah)
    if not al<=x['ua']<=ah:
        out.update(failure_code=2.)
        return out
    for iteration in range(1,201):
        mid=lo+(hi-lo)/2
        # Resolve the temperature bracket to adjacent floats. A UA-only stop
        # does not bound flow or pumping power when the water rise is small.
        if mid==lo or mid==hi:
            mid=min((lo,hi),key=lambda value:abs(at(value)[0]-x['ua']))
            ua,mdot,gap=at(mid)
            break
        ua,mdot,gap=at(mid)
        if ua<x['ua']:lo=mid
        else:hi=mid
    else:raise ValueError('cooler bisection failed to converge')
    power=mdot*e/1000
    out.update(evaluation_defined=1.,water_outlet_C=mid,water_flow=mdot,pump_electric=power,total_rejection=q+power,
      min_gap=gap,required_ua=ua,ua_residual=ua-x['ua'],energy_residual=mdot*(h(mid)-hr)/1000-q-power,
      flow_margin=x['flow_rating']-mdot,power_margin=x['power_rating']-power,iterations=float(iteration))
    return out
