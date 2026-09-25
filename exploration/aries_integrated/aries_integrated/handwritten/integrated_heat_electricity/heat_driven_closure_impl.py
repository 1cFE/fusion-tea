"""Fixed-hardware counterflow exchangers and bounded recuperated thermal closure.

Normative equations and domain: WI-089 design, Heat-driven recuperated cycle.
The root solves operating temperatures only; no equipment quantity is selected.
"""
import math
from aries_integrated.handwritten.integrated_heat_electricity.common import values, require, finish
AUTO_IMPLEMENTED = False
BRANCHES = ('he', 'divertor', 'pbli')


def run_heat_driven_closure(inputs):
    v = values(inputs)
    for key in ('cold_temperature', 'flow', 'cp', 'turbine_pressure', 'return_pressure'):
        require(v[key] > 0, key + ' must be positive')
    require(v['gamma'] > 1, 'gamma must exceed one')
    require(0 < v['turbine_efficiency'] <= 1, 'turbine efficiency must be in (0,1]')
    require(0 <= v['recuperator_effectiveness'] <= 1, 'recuperator effectiveness must be in [0,1]')
    require(v['turbine_pressure'] > v['return_pressure'], 'expansion pressure ordering invalid')
    c = v['flow']*v['cp']/1e6
    k = 1-v['turbine_efficiency']*(1-(v['return_pressure']/v['turbine_pressure'])**((v['gamma']-1)/v['gamma']))
    require(0 < k < 1, 'expansion factor outside closure domain')
    coeff = {}
    for b in BRANCHES:
        for suffix in ('flow', 'cp', 'limit'):
            require(v[b+'_'+suffix] > 0, b+' '+suffix+' must be positive')
        require(v[b+'_ua'] >= 0 and v[b+'_available'] >= 0, 'UA and available heat must be nonnegative')
        ch = v[b+'_flow']*v[b+'_cp']/1e6
        cmin, cmax = min(ch,c), max(ch,c)
        cr, ntu = cmin/cmax, v[b+'_ua']/cmin
        if abs(1-cr) < 1e-10:
            effectiveness = ntu/(1+ntu)
        else:
            decay = math.exp(-ntu*(1-cr))
            effectiveness = -math.expm1(-ntu*(1-cr))/(1-cr*decay)
        coefficient = effectiveness*cmin
        require(0 <= coefficient <= c*(1+1e-14), 'exchanger coefficient violates passive bound')
        coeff[b] = (coefficient, ch)

    def evaluate(turbine):
        cold = v['cold_temperature']
        inlet = cold+v['recuperator_effectiveness']*max(k*turbine-cold,0.)
        secondary = inlet
        outputs = {}
        total = 0.
        for b in BRANCHES:
            coefficient, ch = coeff[b]
            cap = coefficient*max(v[b+'_limit']-secondary,0.)
            q = min(v[b+'_available'],cap)
            defined = coefficient > 0 and q > 0 and v[b+'_limit'] > secondary
            hot = secondary+q/coefficient if defined else 0.
            primary_return = hot-q/ch if defined else 0.
            outputs.update({b+'_transferred':q,b+'_unmet':v[b+'_available']-q,
                            b+'_capability':cap,b+'_hot':hot,b+'_return':primary_return,
                            b+'_hot_bound_margin':v[b+'_limit']-hot if defined else 0.,
                            b+'_hot_terminal_difference':hot-(secondary+q/c) if defined else 0.,
                            b+'_cold_terminal_difference':primary_return-secondary if defined else 0.,
                            b+'_state_defined':float(defined),b+'_secondary_in':secondary,
                            b+'_secondary_out':secondary+q/c})
            secondary += q/c
            total += q
        return c*(turbine-inlet)-total, inlet, total, outputs

    lo = v['cold_temperature']
    hi = max([lo]+[v[b+'_limit'] for b in BRANCHES])
    require(evaluate(lo)[0] <= 1e-8 and evaluate(hi)[0] >= -1e-8, 'thermal closure bracket invalid')
    for iteration in range(1,101):
        temperature = (lo+hi)/2
        residual, inlet, accepted, out = evaluate(temperature)
        if abs(residual) <= 1e-8 or hi-lo <= 1e-10:
            break
        if residual > 0:
            hi = temperature
        else:
            lo = temperature
    else:
        raise ValueError('thermal closure did not converge in 100 iterations')
    require(abs(residual) <= 1e-6, 'thermal closure residual exceeds numerical contract')
    out.update(turbine_temperature=temperature,heater_inlet=inlet,expansion_factor=k,
               accepted_heat=accepted,unmet_heat=sum(out[b+'_unmet'] for b in BRANCHES),
               closure_residual=residual,iterations=float(iteration))
    return finish('heat_driven_closure',out)
