"""WI-097 reviewed constant-U primary bypass and coupled cycle closure.

Normative equations, domain, failure meanings and conditional requirements:
work/active/WI-097_exchanger-thermal-requirements/design.md.
Control changes active primary heat-capacity rate, never supplied installed UA.
"""
from __future__ import annotations

import math

AUTO_IMPLEMENTED = False
BRANCHES = ('he', 'divertor', 'pbli')


def require(condition, message):
    if not condition:
        raise ValueError('controlled exchanger closure: ' + message)


def conductance(ua, ch, cs):
    """Counterflow epsilon*Cmin in MW/K, including equal-capacity limit."""
    if ua <= 0.0 or ch <= 0.0:
        return 0.0
    low, high = min(ch, cs), max(ch, cs)
    ratio, ntu = low / high, ua / low
    if ratio == 1.0:
        epsilon = ntu / (1.0 + ntu)
    else:
        loss = -math.expm1(-ntu * (1.0 - ratio))
        epsilon = loss / ((1.0 - ratio) + ratio * loss)
    return epsilon * low


def bypass_stage(q_available, ua, ch, cs, hot, secondary):
    """Return actual finite-transfer states, including engineering failures."""
    drive = max(hot - secondary, 0.0)
    capability = conductance(ua, ch, cs) * drive
    q = min(q_available, capability)
    fraction = 0.0
    if q_available > 0.0 and capability > q_available:
        lo, hi = 0.0, 1.0
        for _ in range(100):
            fraction = (lo + hi) / 2.0
            actual = conductance(ua, (1.0 - fraction) * ch, cs) * drive
            error = actual - q_available
            if abs(error) <= 1e-10:
                break
            if error > 0.0:
                lo = fraction
            else:
                hi = fraction
        else:
            require(False, 'bypass solve did not converge')
    active = (1.0 - fraction) * ch
    require(active > 0.0, 'positive active primary capacity required')
    defined = q > 0.0 and ua > 0.0 and drive > 0.0
    hx_return = hot - q / active
    mixed_return = hot - q / ch
    secondary_out = secondary + q / cs
    return dict(transferred=q, unmet=q_available-q, capability=capability,
                hot=hot, return_value=mixed_return, state_defined=float(defined),
                hot_terminal_difference=hot-secondary_out if defined else 0.0,
                cold_terminal_difference=hx_return-secondary if defined else 0.0,
                secondary_in=secondary, secondary_out=secondary_out,
                hx_return=hx_return, mixed_return=mixed_return, bypass_fraction=fraction,
                capability_at_solution=conductance(ua, active, cs)*drive)


def calculate(inputs):
    v = {name.removesuffix('_in'): float(value) for name, value in inputs.model_dump().items()}
    require(all(math.isfinite(x) for x in v.values()), 'all inputs must be finite')
    require(v['control_mode'] in (0.0, 1.0), 'control mode must be 0 or 1')
    require(v['return_tolerance'] > 0.0, 'return tolerance must be positive')
    for b in BRANCHES:
        require(v[b+'_required_return'] > 0.0, b+' required return must be positive')
        require(v[b+'_hot_approach'] >= 0.0 and v[b+'_cold_approach'] >= 0.0,
                b+' approach requirements must be nonnegative')
        require(0.0 <= v[b+'_max_bypass'] <= 1.0, b+' maximum bypass must be in [0,1]')

    if v['control_mode'] == 0.0:
        # The reviewed function's arithmetic is unchanged. Its output adapter
        # returns named values because the unbound old schema is not generated.
        from exchanger_architecture_thermal_tea.handwritten.controlled_exchanger_closure.legacy_network import run_network_heat_driven_closure
        out = run_network_heat_driven_closure(inputs)
        for b in BRANCHES:
            out.update({b+'_hx_return': out[b+'_return'], b+'_mixed_return':out[b+'_return'],
                        b+'_bypass_fraction':0.0, b+'_capability_at_solution':out[b+'_transferred']})
    else:
        for key in ('cold_temperature', 'flow', 'cp', 'turbine_pressure', 'return_pressure'):
            require(v[key] > 0.0, key+' must be positive')
        require(v['gamma'] > 1.0, 'gamma must exceed one')
        require(0.0 < v['turbine_efficiency'] <= 1.0, 'turbine efficiency must lie in (0,1]')
        require(0.0 <= v['recuperator_effectiveness'] <= 1.0, 'recuperator effectiveness must lie in [0,1]')
        require(v['turbine_pressure'] > v['return_pressure'], 'expansion pressure ordering invalid')
        require(v['network_mode'] in (0.0, 1.0), 'network mode must be 0 or 1')
        require(0.0 < v['pbli_split'] < 1.0, 'PbLi split must be strictly inside (0,1)')
        for b in BRANCHES:
            for suffix in ('flow', 'cp', 'limit'):
                require(v[b+'_'+suffix] > 0.0, b+' '+suffix+' must be positive')
            require(v[b+'_ua'] >= 0.0 and v[b+'_available'] >= 0.0, b+' UA and duty must be nonnegative')
        capacity = v['flow'] * v['cp'] / 1e6
        expansion = 1.0-v['turbine_efficiency']*(1.0-(v['return_pressure']/v['turbine_pressure'])**((v['gamma']-1.0)/v['gamma']))
        require(0.0 < expansion < 1.0, 'expansion factor outside closure domain')
        split = v['pbli_split']
        secondary_capacity = {b:capacity for b in BRANCHES} if v['network_mode'] == 0.0 else {
            'he':capacity, 'pbli':split*capacity, 'divertor':(1.0-split)*capacity}
        primary_capacity = {b:v[b+'_flow']*v[b+'_cp']/1e6 for b in BRANCHES}
        hot = {b:v[b+'_required_return']+v[b+'_available']/primary_capacity[b] for b in BRANCHES}

        def evaluate(turbine):
            inlet = v['cold_temperature']+v['recuperator_effectiveness']*max(expansion*turbine-v['cold_temperature'],0.0)
            states = {}

            def stage(b, secondary):
                state = bypass_stage(v[b+'_available'],v[b+'_ua'],primary_capacity[b],secondary_capacity[b],hot[b],secondary)
                state['return'] = state.pop('return_value')
                state['hot_bound_margin'] = v[b+'_limit']-hot[b]
                states.update({b+'_'+key:value for key,value in state.items()})
                return state['secondary_out']

            if v['network_mode'] == 0.0:
                secondary = inlet
                for b in BRANCHES:
                    secondary = stage(b, secondary)
                mixed = secondary
            else:
                t1 = stage('he',inlet)
                tp, td = stage('pbli',t1), stage('divertor',t1)
                mixed = split*tp+(1.0-split)*td
            total = sum(states[b+'_transferred'] for b in BRANCHES)
            states.update(pbli_stream_out=states['pbli_secondary_out'],
                          divertor_stream_out=states['divertor_secondary_out'],mixed_outlet=mixed)
            return capacity*(turbine-inlet)-total, inlet, total, states

        lo, hi = v['cold_temperature'], max([v['cold_temperature']]+list(hot.values()))
        require(evaluate(lo)[0] <= 1e-8 and evaluate(hi)[0] >= -1e-8, 'cycle bracket invalid')
        for iteration in range(1,101):
            turbine = (lo+hi)/2.0
            residual, inlet, accepted, out = evaluate(turbine)
            if abs(residual) <= 1e-8 or hi-lo <= 1e-10:
                break
            if residual > 0.0:
                hi = turbine
            else:
                lo = turbine
        else:
            require(False, 'cycle closure did not converge')
        require(abs(residual) <= 1e-6, 'cycle heat residual exceeds contract')
        out.update(turbine_temperature=turbine,heater_inlet=inlet,expansion_factor=expansion,
                   accepted_heat=accepted,unmet_heat=sum(out[b+'_unmet'] for b in BRANCHES),
                   closure_residual=residual,iterations=float(iteration),network_mode_used=v['network_mode'],pbli_split_used=split)

    out['control_mode_used'] = v['control_mode']
    for b in BRANCHES:
        ch = v[b+'_flow']*v[b+'_cp']/1e6
        required_hot = v[b+'_required_return']+v[b+'_available']/ch
        residual = out[b+'_mixed_return']-v[b+'_required_return']
        out.update({b+'_required_hot':required_hot,b+'_required_hot_margin':v[b+'_limit']-required_hot,
                    b+'_active_flow':(1.0-out[b+'_bypass_fraction'])*v[b+'_flow'],
                    b+'_return_residual':residual,b+'_return_residual_magnitude':abs(residual),
                    b+'_hot_approach_margin':out[b+'_hot_terminal_difference']-v[b+'_hot_approach'],
                    b+'_cold_approach_margin':out[b+'_cold_terminal_difference']-v[b+'_cold_approach'],
                    b+'_control_margin':v[b+'_max_bypass']-out[b+'_bypass_fraction']})
    require(all(math.isfinite(value) for value in out.values()), 'nonfinite output')
    return out


def run_controlled_network_heat_driven_closure(inputs):
    from exchanger_architecture_thermal_tea.schemas.controlled_network_heat_driven_closure_output import Controlled_Network_Heat_Driven_ClosureOutput
    result = calculate(inputs)
    require(set(result) == set(Controlled_Network_Heat_Driven_ClosureOutput.model_fields), 'output contract mismatch')
    return tuple(result[name] for name in Controlled_Network_Heat_Driven_ClosureOutput.model_fields)
