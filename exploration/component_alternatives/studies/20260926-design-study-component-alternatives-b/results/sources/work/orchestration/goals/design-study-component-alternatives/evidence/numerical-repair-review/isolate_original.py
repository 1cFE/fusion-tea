"""Independent high-precision diagnosis; reads retained results, changes no model.

Decimal counterflow integration and analytical one-active-stage closure check the
six original discrepancies. Native versus oracle gas tuples isolate propagation.
Only the actually used series/one-heater scenario is supported by this probe.
"""
import json
import sys
from decimal import Decimal as D, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / 'exploration/component_alternatives'))
import verify
import oracle_thermal

P = verify.P
RECORD = ROOT / 'exploration/component_alternatives/studies/20260926-design-study-component-alternatives'
dec = lambda x: D(str(x))


def bisect(fn, low, high):
    for _ in range(190):
        mid = (low + high) / 2
        if fn(mid) > 0:
            high = mid
        else:
            low = mid
    return (low + high) / 2


def cooler(inputs, outputs):
    get = lambda owner, key: dec(outputs[P + owner + '__evaluate__' + key])
    inp = lambda key: dec(inputs[P + 'water_pre__' + key])
    rows = [(dec(r['t']), dec(r['h'])) for r in oracle_thermal._liquid_rows()]

    def interp(value, reverse=False):
        seq = [(b, a) for a, b in rows] if reverse else rows
        for (a, b), (c, d) in zip(seq, seq[1:]):
            if a <= value <= c:
                return b + (d - b) * (value - a) / (c - a)
        raise ValueError('probe property range')

    q = -get('precooler', 'heat_into_fluid')
    hot = get('recuperator', 'hot_out') - D('273.15')
    cold = get('precooler', 'temperature_out') - D('273.15')
    electric = D('9.80665') * inp('head') / (1000 * inp('eta_p') * inp('eta_motor'))
    ha = interp(inp('water_inlet_C')) + electric
    ta = interp(ha, True)

    def evaluate(tout):
        hout = interp(tout)
        flow = 1000 * q / (hout - ha)
        nodes = [(ta, ha)] + [(t, h) for t, h in rows if ta < t < tout] + [(tout, hout)]
        gaps = [cold + (hot - cold) * (h - ha) / (hout - ha) - t for t, h in nodes]
        ua = D(0)
        for i in range(len(nodes) - 1):
            dq = flow * (nodes[i + 1][1] - nodes[i][1]) / 1000
            a, b = gaps[i:i + 2]
            ua += dq / a if a == b else dq * (b / a).ln() / (b - a)
        return ua, flow

    t = bisect(lambda x: evaluate(x)[0] - inp('ua'), ta + D('1e-7'), min(hot, D(60)) - D('1e-7'))
    ua, flow = evaluate(t)
    return {'outlet': t, 'flow': flow, 'power': flow * electric / 1000,
            'evaluated_outlet_residual': evaluate(get('water_pre', 'water_outlet_C'))[0] - inp('ua')}


def gas_closure(inputs, outputs):
    get = lambda owner, key: dec(outputs[P + owner + '__evaluate__' + key])
    inp = lambda owner, key: dec(inputs[P + owner + '__' + key])
    c = inp('cycle', 'selected_flow') * inp('cycle', 'cp') / D('1e6')
    ch = get('primary_loop', 'mdot') * inp('primary_loop', 'loop_cp') / D('1e6')
    ua = inp('he_hx', 'selected_area') * inp('he_hx', 'assumed_u') / D('1e6')
    q, hot = get('primary_loop', 'q_ihx'), get('primary_loop', 'T_out')
    cold = get('compressor_3', 'temperature_out')
    eps = inp('recuperator_hardware', 'ua') / (inp('recuperator_hardware', 'ua') + c)
    k = 1 - inp('cycle', 'turbine_efficiency') * (1 - (inp('cycle', 'return_pressure') / get('pressure_loss', 'pressure_out')) ** ((inp('cycle', 'gamma') - 1) / inp('cycle', 'gamma')))

    def coeff(f):
        low, high = min((1-f)*ch, c), max((1-f)*ch, c)
        ratio, ntu = low/high, ua/low
        eff = ntu/(1+ntu) if abs(1-ratio) < D('1e-10') else (1-(-ntu*(1-ratio)).exp())/(1-ratio*(-ntu*(1-ratio)).exp())
        return eff*low

    t_full = (cold*(1-eps)+q/c)/(1-eps*k)
    inlet = cold*(1-eps)+eps*k*t_full
    if coeff(D(0))*(hot-inlet) < q:
        a = coeff(D(0))
        t_full = ((c-a)*cold*(1-eps)+a*hot)/(c-(c-a)*eps*k)
        inlet = cold*(1-eps)+eps*k*t_full
    accepted = min(q, coeff(D(0))*(hot-inlet))
    margin = hot-inlet-accepted/coeff(D(0))

    def bypass(heater):
        if coeff(D(0))*(hot-heater) < q:
            return D(0)
        f = bisect(lambda x: q-coeff(x)*(hot-heater), D(0), 1-D('1e-9'))
        return f*get('primary_loop', 'mdot')

    return {'turbine_temperature': t_full, 'heater_inlet': inlet, 'hot_bound_margin': margin,
            'bypass_native_heater': bypass(get('heat_exchangers', 'heater_inlet')),
            'bypass_accurate_heater': bypass(inlet)}


def main():
    rows = {r['case']: r for r in json.loads((RECORD/'results/cases.json').read_text())['cases']}
    failed = [r['case'] for r in json.loads((RECORD/'results/verification-diagnostics.json').read_text())['cases'] if r['numeric_mismatches']]
    result = {}
    with localcontext() as context:
        context.prec = 65
        for name in failed:
            row = rows[name]
            native, oracle = row['outputs'], verify.evaluate(row['inputs'])
            if name.startswith('gas-'):
                result[name] = {'native_flow': native[P+'water_pre__evaluate__water_flow'],
                                'oracle_flow': oracle[P+'water_pre__evaluate__water_flow'],
                                'native_tuple_decimal': cooler(row['inputs'], native),
                                'oracle_tuple_decimal': cooler(row['inputs'], oracle)}
            else:
                result[name] = {'native': {k: native[P+owner+'__evaluate__'+k] for owner,k in [('heat_exchangers','turbine_temperature'),('heat_exchangers','heater_inlet'),('heat_exchangers','he_hot_bound_margin'),('gas_boundary','bypass_flow')]},
                                'oracle': {k: oracle[P+owner+'__evaluate__'+k] for owner,k in [('heat_exchangers','turbine_temperature'),('heat_exchangers','heater_inlet'),('heat_exchangers','he_hot_bound_margin'),('gas_boundary','bypass_flow')]},
                                'native_tuple_decimal': gas_closure(row['inputs'], native),
                                'oracle_tuple_decimal': gas_closure(row['inputs'], oracle)}
    target = Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(result, indent=2, default=str)+'\n')
    print(target)


if __name__ == '__main__':
    main()
