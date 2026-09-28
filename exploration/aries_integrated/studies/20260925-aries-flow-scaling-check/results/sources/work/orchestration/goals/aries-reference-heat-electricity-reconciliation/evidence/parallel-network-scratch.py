"""Scratch: first-principles check of the Fig. 12 parallel PbLi/divertor network with the model's own stage equations.
Not model code; informs the round-2 strategy only."""
import math
def eff(ua, cmin, cmax):
    cr, ntu = cmin/cmax, ua/cmin
    if abs(1-cr) < 1e-10: return ntu/(1+ntu)
    d = math.exp(-ntu*(1-cr)); return -math.expm1(-ntu*(1-cr))/(1-cr*d)
def stage(t_in, c_cycle, q_avail, ch, ua, limit):
    if c_cycle <= 0: return 0., t_in
    cmin, cmax = min(ch, c_cycle), max(ch, c_cycle)
    k = eff(ua, cmin, cmax)*cmin
    cap = k*max(limit-t_in, 0.)
    q = min(q_avail, cap)
    return q, t_in + q/c_cycle
def run(flow=1600., eps=.95, split=.8, q_he=1248.57, q_pbli=1485.78, q_div=191.41, div_flow=283., ua=50., cp=5193., gamma=5/3, eta_t=.93, p_t=15*(1-.045), p_r=15/3.5, t_cold=371.0942, parallel=True):
    c = flow*cp/1e6
    k = 1-eta_t*(1-(p_r/p_t)**((gamma-1)/gamma))
    ch_he, ch_pb, ch_dv = 3261*cp/1e6, 26860*190/1e6, div_flow*cp/1e6
    def evaluate(tt):
        inlet = t_cold + eps*max(k*tt-t_cold, 0.)
        q1, t1 = stage(inlet, c, q_he, ch_he, ua, 729.15)
        if parallel:
            qp, tp = stage(t1, split*c, q_pbli, ch_pb, ua, 1011.15)
            qd, td = stage(t1, (1-split)*c, q_div, ch_dv, ua, 973.15)
            t_out = split*tp + (1-split)*td
        else:
            qd, t2 = stage(t1, c, q_div, ch_dv, ua, 973.15)
            qp, t_out = stage(t2, c, q_pbli, ch_pb, ua, 1011.15)
        total = q1+qp+qd
        return c*(tt-inlet)-total, dict(inlet=inlet, t_he_out=t1, q_he=q1, q_pbli=qp, q_div=qd, unmet=q_he+q_pbli+q_div-total, t_out=t_out)
    lo, hi = t_cold, 1011.15
    for _ in range(200):
        mid = (lo+hi)/2; r, out = evaluate(mid)
        if abs(r) < 1e-8 or hi-lo < 1e-10: break
        lo, hi = (lo, mid) if r > 0 else (mid, hi)
    tt = mid
    # cycle work with the model's compressor demand scaling with flow (1372.85 MW at 1400 kg/s)
    w_t = c*tt*(1-k); w_c = 1372.8509*flow/1400.; net_shaft = w_t-w_c
    gross = .98*max(net_shaft, 0.)
    return dict(turbine_K=tt, gross=gross, eta=gross/(c*(tt-out['inlet'])) if tt > out['inlet'] else 0., **out)
print('%-38s %8s %8s %8s %8s %8s' % ('case', 'Tt(K)', 'gross', 'unmet', 'q_pbli', 'eta'))
for label, kw in [
    ('series C3 (check vs native 907.89/1094.74/151.0)', dict(parallel=False)),
    ('parallel C3 split 0.70', dict(split=.70)), ('parallel C3 split 0.75', dict(split=.75)), ('parallel C3 split 0.80', dict(split=.80)), ('parallel C3 split 0.85', dict(split=.85)), ('parallel C3 split 0.90', dict(split=.90)),
    ('parallel C3 1500 kg/s split 0.80', dict(flow=1500., split=.80)), ('parallel C3 1400 kg/s split 0.80', dict(flow=1400., split=.80)),
    ('parallel, original inputs 1400/0.8/500 s0.8', dict(flow=1400., eps=.8, split=.8, q_he=1143.755, q_pbli=1379.653, q_div=394.4, div_flow=500.)),
    ('parallel, orig inputs but eps .95', dict(flow=1400., eps=.95, split=.8, q_he=1143.755, q_pbli=1379.653, q_div=394.4, div_flow=500.)),
    ('parallel C3 UAx10 split 0.8', dict(ua=500.)),
]:
    r = run(**kw); print('%-38s %8.2f %8.2f %8.2f %8.2f %8.4f' % (label, r['turbine_K'], r['gross'], r['unmet'], r['q_pbli'], r['eta']))
