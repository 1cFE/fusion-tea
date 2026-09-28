"""Author prototype; fixed-pressure NIST tables, no fitted cycle efficiency."""
from pathlib import Path
import json, hashlib
import numpy as np
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).parent
SOURCES={
 'main':ROOT/'knowledge/sources/nist_webbook_water6_2mpa171to455c_halfk_state_table/raw.html',
 'bleed':ROOT/'knowledge/sources/nist_water0_8mpa42to455c_matched_cycle_table/raw.html',
 'condenser':ROOT/'knowledge/sources/nist_water_temperature_grid_saturation_20to60c_corrected/raw.html'}
def rows(path):
 result=[]
 for tr in BeautifulSoup(path.read_text(),'html.parser').select('tr'):
  c=[x.get_text(' ',strip=True) for x in tr.select('td')]
  if len(c)>=14 and c[-1] in ('liquid','vapor'):
   result.append(dict(zip(('T','P','rho','v','u','h','s'),map(float,c[:7])),phase=c[-1]))
 return result
def interp(data,xkey,x,ykey):
 data=sorted(data,key=lambda r:r[xkey]); xs=[r[xkey] for r in data]
 if not xs[0]<=x<=xs[-1]: raise ValueError(f'Property domain: {xkey}={x} outside {xs[0],xs[-1]}')
 return float(np.interp(x,xs,[r[ykey] for r in data]))
M=rows(SOURCES['main']); B=rows(SOURCES['bleed']); C=rows(SOURCES['condenser'])
BL=[r for r in B if r['phase']=='liquid']; BV=[r for r in B if r['phase']=='vapor']; bf=BL[-1]; bg=BV[0]
def stateT(data,T,phase):
 d=[r for r in data if r['phase']==phase];return {k:interp(d,'T',T,k) for k in ('T','P','h','s','v')}
def bh_s(s):
 if bf['s']<=s<=bg['s']:return bf['h']+(s-bf['s'])/(bg['s']-bf['s'])*(bg['h']-bf['h'])
 return interp(BV,'s',s,'h')
def bh_T(h):return interp(B,'h',h,'T')
def profile(data,h0,h1,hot,cold,Q):
 # Dense enthalpy grid plus every original phase boundary/knot; finite stream pairing.
 hs=np.unique(np.r_[np.linspace(h0,h1,10001),[r['h'] for r in data if h0<r['h']<h1]])
 ordered=sorted(data,key=lambda r:r['h']);tw=np.interp(hs,[r['h'] for r in ordered],[r['T'] for r in ordered]);ts=cold+(hot-cold)*(hs-h0)/(h1-h0);gap=ts-tw
 if min(gap)<=0:return {'min_gap_K':float(min(gap)),'UA_MW_K':None}
 return {'min_gap_K':float(min(gap)),'UA_MW_K':float(np.trapezoid(1/gap,hs)*Q/(h1-h0))}
def cycle(name,Tsteam=445.,Tc=42.,eta_t=.90,reheat=False):
 cf=stateT(C,Tc,'liquid');cg=stateT(C,Tc,'vapor'); inlet=stateT(M,Tsteam,'vapor')
 eta_p=.80; eta_motor=.95;eta_gen=.98;eta_mech=.99;Q=3306.889098848892
 wp1=cf['v']*(.8-cf['P'])*1000/eta_p;hc=cf['h']+wp1
 hp=inlet['h']-eta_t*(inlet['h']-bh_s(inlet['s']));sp=interp(B,'h',hp,'s')
 y=(bf['h']-hc)/(hp-hc)
 wp2=bf['v']*(6.2-.8)*1000/eta_p;feed=bf['h']+wp2
 lp=stateT(B,Tsteam,'vapor') if reheat else {'h':hp,'s':sp}
 xs=(lp['s']-cf['s'])/(cg['s']-cf['s'])
 if not 0<=xs<=1:raise ValueError('LP ideal endpoint outside saturation domain')
 hls=cf['h']+xs*(cg['h']-cf['h']);hl=lp['h']-eta_t*(lp['h']-hls)
 x=(hl-cf['h'])/(cg['h']-cf['h'])
 if not 0<=x<=1:raise ValueError('LP actual endpoint outside saturation domain')
 qb=inlet['h']-feed;qr=(1-y)*(lp['h']-hp);qin=qb+qr;m=Q*1000/qin
 wt=inlet['h']-hp+(1-y)*(lp['h']-hl);wp=(1-y)*wp1+wp2
 shaft=m*wt/1000;gross=shaft*eta_mech*eta_gen;pump=m*wp/1000/eta_motor
 qc=m*(1-y)*(hl-cf['h'])/1000;loss=shaft-gross+pump-m*wp/1000
 # Declared cooling-water scenario, not site-qualified:25->35 C,20 m head.
 cw0=stateT(C,25,'liquid');cw1=stateT(C,35,'liquid');rej=qc+loss
 cw_specific_electric=9.80665*20/.8/.95/1000
 # All cooling pump/motor input ultimately enters this water loop; solve it in the rise.
 mcw=rej*1000/(cw1['h']-cw0['h']-cw_specific_electric);pcw=mcw*cw_specific_electric/1000
 cold=269.664729914530
 main=profile(M,feed,inlet['h'],465,cold,Q*qb/qin)
 rh=profile(B,hp,lp['h'],465,cold,Q*qr/qin) if reheat else None
 return dict(name=name,steam_C=Tsteam,condenser_C=Tc,eta_turbine=eta_t,reheat=reheat,bleed_fraction=y,feedwater_C=interp(M,'h',feed,'T'),bleed_C=bh_T(hp),steam_kg_s=m,LP_quality=x,LP_ideal_quality=xs,main=main,reheater=rh,gross_MW=gross,gross_efficiency=gross/Q,feed_and_condensate_pump_MW=pump,cooling_water_pump_MW=pcw,cycle_net_MW=gross-pump-pcw,condenser_MW=qc,mechanical_generator_motor_loss_MW=loss,rejection_before_cw_pump_MW=rej,cooling_water_kg_s=mcw,cooling_water_pump_temperature_rise_K=cw_specific_electric/((cw1['h']-cw0['h'])/10),cooling_water_heat_closure_MW=mcw*(cw1['h']-cw0['h'])/1000-rej-pcw,cooling_water_min_gap_K=Tc-35,main_duty_MW=Q*qb/qin,reheater_duty_MW=Q*qr/qin,salt_reheater_flow_fraction=qr/qin,open_heater_residual_kJ_kg=(1-y)*hc+y*hp-bf['h'],first_law_residual_MW=Q+pump-gross-qc-loss,shaft_first_law_residual_MW=Q+m*wp/1000-shaft-qc,states={'main_inlet':inlet,'bleed_h':hp,'bleed_s':sp,'feed_h':feed,'LP_inlet':lp,'LP_outlet_h':hl,'condensate':cf},assumptions={'pump_isentropic':eta_p,'motor':eta_motor,'generator':eta_gen,'mechanical':eta_mech,'cooling_water_head_m':20})
if __name__=='__main__':
 cases=[cycle('no_reheat_baseline'),cycle('reheat_baseline',reheat=True),cycle('no_reheat_eta85',eta_t=.85),cycle('reheat_cold40',Tc=40,reheat=True),cycle('reheat_warm50',Tc=50,reheat=True),cycle('reheat_steam435',Tsteam=435,reheat=True)]
 result={'authority':'AGENT research prototype; not adopted or independently validated','source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCES.values()},'cases':cases}
 (OUT/'cycle-results.json').write_text(json.dumps(result,indent=2)+'\n')
 for c in cases:print(c['name'],{k:c[k] for k in ('feedwater_C','bleed_fraction','LP_quality','gross_MW','feed_and_condensate_pump_MW','cooling_water_pump_MW','cycle_net_MW','main','reheater','first_law_residual_MW')})
