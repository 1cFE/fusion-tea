"""Bounded full-duty feasibility probe; not native study or qualified economics.

Solve full-duty cycle algebra, then explicit primary bypass at fixed installed UA.
Failed rows retain attempted full-duty temperatures, not an actual partial-duty cycle.
"""
import json
import math
from pathlib import Path
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/cases.json'
B = ('he', 'pbli', 'divertor')
RET = dict(zip(B, (659.15, 724.15, 846.15)))
CH = dict(zip(B, (3261*5193/1e6, 26860*190/1e6, 500*5193/1e6)))
CAP = dict(zip(B, (729.15, 1011.15, 973.15)))
OFFERS = {'original': (50.,50.,50.), 'small': (12.,12.,3.), 'medium': (18.,18.,6.), 'large': (24.,24.,9.)}

def effectiveness_conductance(ua, ch, cs):
    if ch <= 0: return 0.
    low, high = min(ch,cs), max(ch,cs)
    ratio, ntu = low/high, ua/low
    if abs(1-ratio) < 1e-10: eps = ntu/(1+ntu)
    else:
        z = math.exp(-ntu*(1-ratio))
        eps = -math.expm1(-ntu*(1-ratio))/(1-ratio*z)
    return eps*low

def assess(load, flow, mode, split, offer, cold, k, eff):
    q = {'he': .41164*load+141., 'pbli': .56636*load, 'divertor': .15*load+29.}
    c = flow*5193/1e6
    turbine = (cold*(1-eff)+sum(q.values())/c)/(1-eff*k)
    if k*turbine <= cold: turbine = cold+sum(q.values())/c
    t0 = cold+eff*max(k*turbine-cold,0)
    assert abs(c*(turbine-t0)-sum(q.values())) < 1e-8
    tins = {'he': t0, 'divertor': t0+q['he']/c, 'pbli': t0+(q['he']+(q['divertor'] if mode == 0 else 0))/c}
    cs = {b: c for b in B} if mode == 0 else {'he':c,'pbli':split*c,'divertor':(1-split)*c}
    states={}
    reasons=[]
    for b,ua in zip(B,OFFERS[offer]):
        h=RET[b]+q[b]/CH[b]
        cap0=effectiveness_conductance(ua,CH[b],cs[b])*max(h-tins[b],0)
        state={'duty_mw':q[b], 'required_hot_k':h,'hot_cap_margin_k':CAP[b]-h,
               'secondary_in_k':tins[b], 'secondary_out_k':tins[b]+q[b]/cs[b],
               'full_flow_capability_mw':cap0, 'installed_ua_mw_k':ua}
        if h > CAP[b]+1e-9: reasons.append(b+':hot_cap')
        if cap0 < q[b]-1e-8:
            reasons.append(b+':insufficient_conductance')
        else:
            f=brentq(lambda f: effectiveness_conductance(ua,(1-f)*CH[b],cs[b])*max(h-tins[b],0)-q[b],0.,1.,xtol=1e-14)
            tx=h-q[b]/((1-f)*CH[b])
            d_hot=h-state['secondary_out_k']; d_cold=tx-tins[b]
            mixed=f*h+(1-f)*tx
            lm=None
            if min(d_hot,d_cold)>1e-8:
                lm=(d_hot-d_cold)/math.log(d_hot/d_cold) if abs(d_hot-d_cold)>1e-8 else (d_hot+d_cold)/2
                if min(d_hot,d_cold)>=30-1e-8:
                    assert abs(q[b]-ua*lm)<1e-6
            assert abs(mixed-RET[b])<1e-8
            state.update(bypass_fraction=f,active_hx_return_k=tx,mixed_return_k=mixed,
                         hot_terminal_k=d_hot,cold_terminal_k=d_cold,lmtd_k=lm)
            if min(d_hot,d_cold)<30-1e-8: reasons.append(b+':approach')
        states[b]=state
    return {'load_mw':load,'cycle_flow_kg_s':flow,'mode':mode,'split':split,'offer':offer,
            'area_m2':dict(zip(B,[x*1000 for x in OFFERS[offer]])),
            'hx_purchase_usd2004':sum(OFFERS[offer])*1000/50000*58325700,
            'attempted_full_duty_turbine_k':turbine,'attempted_full_duty_inlet_k':t0,
            'thermal_pass':not reasons,'failure_reasons':reasons,'branches':states}

def main():
    original=json.loads(SOURCE.read_text())['cases'][0]
    p='aries_integrated_plant__'; inp=original['inputs']; out=original['outputs']
    cold=out[p+'compressor_3__evaluate__temperature_out']
    k=1-inp[p+'cycle__turbine_efficiency']*(1-(inp[p+'cycle__return_pressure']/out[p+'pressure_loss__evaluate__pressure_out'])**((inp[p+'cycle__gamma']-1)/inp[p+'cycle__gamma']))
    eff=inp[p+'cycle__recuperator_effectiveness']
    rows=[]
    for load in (1650.,1835.4512830147435,1950.,2000.,2200.):
        for offer in OFFERS:
            for flow in range(1100,1651,50):
                for mode,splits in ((0,(.85,)),(1,tuple(i/100 for i in range(40,91,5)))):
                    for split in splits: rows.append(assess(load,flow,mode,split,offer,cold,k,eff))
    groups=[]
    for load in sorted({r['load_mw'] for r in rows}):
        for offer in OFFERS:
            for mode in (0,1):
                rr=[r for r in rows if (r['load_mw'],r['offer'],r['mode'])==(load,offer,mode)]
                passed=[r for r in rr if r['thermal_pass']]
                groups.append({'load_mw':load,'offer':offer,'mode':mode,'points':len(rr),'thermal_passes':len(passed),
                               'minimum_passing_flow':min((r['cycle_flow_kg_s'] for r in passed),default=None)})
    result={'kind':'development full-duty feasibility; not native study; no equipment/net/cost-account verification',
            'source':str(SOURCE.relative_to(ROOT)), 'cold_k':cold,'expansion_factor':k,'recuperator_effectiveness':eff,
            'offers_ua_mw_k':OFFERS,'returns_k':RET,'primary_capacity_rate_mw_k':CH,'hot_caps_k':CAP,
            'terminal_minimum_k':30.,'rows':rows,'summary':groups}
    dest=Path(__file__).with_name('development-probe.json');dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'points':len(rows),'thermal_passes':sum(r['thermal_pass'] for r in rows),'groups':groups},indent=2))

if __name__=='__main__': main()
