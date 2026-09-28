"""Fixed-hardware counterflow exchangers with a selectable network and bounded recuperated thermal closure.

Normative equations and domain: WI-092 design (network mode 1) and WI-089 design, Heat-driven
recuperated cycle. Mode 0 copies the reviewed heat_driven_closure_impl.py equations line for line;
that reviewed definition and completion are retained unchanged and are no longer bound by the live
assembly. Mode 1 evaluates the published series-then-parallel network (Raffray Fig. 12). The root
solves operating temperatures only; no equipment quantity is selected, and the supplied split
fraction is an operating choice (a stand-in for the unmodelled branch hydraulic balance) that never
resizes a stage. 0 < split < 1 is required in both modes.
"""
import math
from exchanger_architecture_thermal_tea.handwritten.controlled_exchanger_closure.legacy_support import values, require, finish
AUTO_IMPLEMENTED = False
BRANCHES = ('he', 'divertor', 'pbli')


def run_network_heat_driven_closure(inputs):
    v = values(inputs)
    for key in ('cold_temperature', 'flow', 'cp', 'turbine_pressure', 'return_pressure'):
        require(v[key] > 0, key + ' must be positive')
    require(v['gamma'] > 1, 'gamma must exceed one')
    require(0 < v['turbine_efficiency'] <= 1, 'turbine efficiency must be in (0,1]')
    require(0 <= v['recuperator_effectiveness'] <= 1, 'recuperator effectiveness must be in [0,1]')
    require(v['turbine_pressure'] > v['return_pressure'], 'expansion pressure ordering invalid')
    require(v['network_mode'] in (0, 1), 'network mode must be 0 (series) or 1 (published network)')
    require(0 < v['pbli_split'] < 1, 'PbLi split fraction must be strictly inside (0,1)')
    mode, split = int(v['network_mode']), v['pbli_split']
    c = v['flow']*v['cp']/1e6
    k = 1-v['turbine_efficiency']*(1-(v['return_pressure']/v['turbine_pressure'])**((v['gamma']-1)/v['gamma']))
    require(0 < k < 1, 'expansion factor outside closure domain')
    stream = {'he': c, 'divertor': c, 'pbli': c} if mode == 0 else {'he': c, 'divertor': (1-split)*c, 'pbli': split*c}
    coeff = {}
    for b in BRANCHES:
        for suffix in ('flow', 'cp', 'limit'):
            require(v[b+'_'+suffix] > 0, b+' '+suffix+' must be positive')
        require(v[b+'_ua'] >= 0 and v[b+'_available'] >= 0, 'UA and available heat must be nonnegative')
        ch = v[b+'_flow']*v[b+'_cp']/1e6
        cs = stream[b]
        cmin, cmax = min(ch,cs), max(ch,cs)
        cr, ntu = cmin/cmax, v[b+'_ua']/cmin
        if abs(1-cr) < 1e-10:
            effectiveness = ntu/(1+ntu)
        else:
            decay = math.exp(-ntu*(1-cr))
            effectiveness = -math.expm1(-ntu*(1-cr))/(1-cr*decay)
        coefficient = effectiveness*cmin
        require(0 <= coefficient <= cs*(1+1e-14), 'exchanger coefficient violates passive bound')
        coeff[b] = (coefficient, ch, cs)

    def stage(b, secondary, outputs):
        coefficient, ch, cs = coeff[b]
        cap = coefficient*max(v[b+'_limit']-secondary,0.)
        q = min(v[b+'_available'],cap)
        defined = coefficient > 0 and q > 0 and v[b+'_limit'] > secondary
        hot = secondary+q/coefficient if defined else 0.
        primary_return = hot-q/ch if defined else 0.
        outputs.update({b+'_transferred':q,b+'_unmet':v[b+'_available']-q,
                        b+'_capability':cap,b+'_hot':hot,b+'_return':primary_return,
                        b+'_hot_bound_margin':v[b+'_limit']-hot if defined else 0.,
                        b+'_hot_terminal_difference':hot-(secondary+q/cs) if defined else 0.,
                        b+'_cold_terminal_difference':primary_return-secondary if defined else 0.,
                        b+'_state_defined':float(defined),b+'_secondary_in':secondary,
                        b+'_secondary_out':secondary+q/cs})
        return q, secondary+q/cs

    def evaluate(turbine):
        cold = v['cold_temperature']
        inlet = cold+v['recuperator_effectiveness']*max(k*turbine-cold,0.)
        outputs = {}
        if mode == 0:
            secondary, total = inlet, 0.
            for b in BRANCHES:
                q, secondary = stage(b, secondary, outputs)
                total += q
            outputs.update(pbli_stream_out=outputs['pbli_secondary_out'], divertor_stream_out=outputs['divertor_secondary_out'],
                           mixed_outlet=secondary)
        else:
            q_he, t1 = stage('he', inlet, outputs)
            q_p, tp = stage('pbli', t1, outputs)
            q_d, td = stage('divertor', t1, outputs)
            total = q_he+q_p+q_d
            outputs.update(pbli_stream_out=tp, divertor_stream_out=td, mixed_outlet=split*tp+(1-split)*td)
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
               closure_residual=residual,iterations=float(iteration),network_mode_used=float(mode),pbli_split_used=split)
    return finish('network_heat_driven_closure',out)
