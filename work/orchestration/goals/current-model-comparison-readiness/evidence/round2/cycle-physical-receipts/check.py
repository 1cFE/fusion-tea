"""Independent review arithmetic. No author modules imported; common NIST originals disclosed."""
from pathlib import Path
from html import unescape
import re,json,hashlib,math,bisect
ROOT=Path.cwd(); OUT=Path(__file__).parent
base=ROOT/'knowledge/sources'
paths=[base/x/'raw.html' for x in ('nist_webbook_water6_2mpa171to455c_halfk_state_table','nist_water0_8mpa42to455c_matched_cycle_table','nist_water_temperature_grid_saturation_20to60c_corrected')]
meta=[]
def read(p):
 t=p.read_text(); rows=[]
 for tr in re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S):
  cols=[unescape(re.sub('<[^>]+>','',v)).strip() for v in re.findall(r'<td[^>]*>(.*?)</td>',tr,re.S)]
  if len(cols)>=14 and cols[-1] in ['liquid','vapor']:
   rows.append(dict(zip(['T','P','rho','v','u','h','s'],map(float,cols[:7])),phase=cols[-1]))
 assert rows
 meta.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),rows=len(rows),query=unescape(re.search(r'/cgi/fluid.cgi\?Action=Data[^\"]+',t)[0]),anchors=[rows[0],rows[-1]]))
 for r in rows: assert abs(r['h']-r['u']-1000*r['P']*r['v'])<.0002
 return rows
M,B,C=map(read,paths)
def val(rows,x,key='T',out='h'):
 r=sorted(rows,key=lambda r:r[key]); xs=[r[key] for r in r]
 assert xs[0]<=x<=xs[-1],(key,x,xs[0],xs[-1])
 i=max(1,min(len(r)-1,bisect.bisect_right(xs,x)));a,b=r[i-1],r[i]
 return a[out]+(b[out]-a[out])*(x-a[key])/(b[key]-a[key])
def phase(rows,p):return [r for r in rows if r['phase']==p]
bl=phase(B,'liquid')[-1];bv=phase(B,'vapor')[0]
# Exact analytical integration of each linear temperature-gap segment, including latent interval.
def profile(rows,a,b,Q):
 knots=sorted(set([a,b]+[r['h'] for r in rows if a<r['h']<b]))
 gaps=[269.664729914530+(465-269.664729914530)*(h-a)/(b-a)-val(rows,h,'h','T') for h in knots]
 assert min(gaps)>0
 ua=0
 for ha,hb,ga,gb in zip(knots,knots[1:],gaps,gaps[1:]):
  ua+=(hb-ha)*(1/ga if abs(gb-ga)<1e-10 else math.log(gb/ga)/(gb-ga))
 return {'min_gap_K':min(gaps),'UA_MW_K':ua*Q/(b-a),'checked_knots':len(knots)}
def run(c):
 T,Tc,eta,rh=c['steam_C'],c['condenser_C'],c['eta_turbine'],c['reheat'];Q=3306.889098848892
 lf,vf=phase(C,'liquid'),phase(C,'vapor');hf=val(lf,Tc);hg=val(vf,Tc);sf=val(lf,Tc,out='s');sg=val(vf,Tc,out='s');pc=val(lf,Tc,out='P')
 h1=val(phase(M,'vapor'),T);s1=val(phase(M,'vapor'),T,out='s')
 his=val(B,s1,'s','h');h2=h1-eta*(h1-his)
 h3=val(phase(B,'vapor'),T) if rh else h2
 s3=val(phase(B,'vapor'),T,out='s') if rh else val(B,h2,'h','s')
 xideal=(s3-sf)/(sg-sf); assert 0<xideal<1
 h4=h3-eta*(h3-(hf+xideal*(hg-hf)))
 wcp=val(lf,Tc,out='v')*(.8-pc)*1000/.8; wfp=bl['v']*5400/.8
 hc=hf+wcp; feed=bl['h']+wfp;y=(bl['h']-hc)/(h2-hc)
 assert 0<y<1 and h2>bv['h']
 qmain=h1-feed;qre=(1-y)*(h3-h2);m=1000*Q/(qmain+qre)
 hp=m*(h1-h2)/1000;lp=m*(1-y)*(h3-h4)/1000;shaft=hp+lp;gross=shaft*.99*.98
 pump_shaft=m*(wfp+(1-y)*wcp)/1000;pe=pump_shaft/.95
 cond=m*(1-y)*(h4-hf)/1000;loss=shaft-gross+pe-pump_shaft;rej=cond+loss
 dh=val(lf,35)-val(lf,25);we=9.80665*20/760
 mcw=1000*rej/(dh-we);cw=mcw*we/1000
 actual={'gross_MW':gross,'gross_efficiency':gross/Q,'bleed_fraction':y,'feedwater_C':val(M,feed,'h','T'),'steam_kg_s':m,'LP_quality':(h4-hf)/(hg-hf),'feed_and_condensate_pump_MW':pe,'cooling_water_pump_MW':cw,'condenser_MW':cond,'cycle_net_MW':gross-pe-cw}
 for k,v in actual.items():assert abs(v-c[k])<1e-8,(k,v,c[k])
 assert abs(Q+pe-gross-rej)<1e-9
 assert abs(mcw*dh/1000-rej-cw)<1e-9
 assert abs((1-y)*hc+y*h2-bl['h'])<1e-10
 main=profile(M,feed,h1,Q*qmain/(qmain+qre));reheat=profile(B,h2,h3,Q*qre/(qmain+qre)) if rh else None
 for key,own in [('main',main),('reheater',reheat)]:
  if own:assert abs(own['UA_MW_K']/c[key]['UA_MW_K']-1)<1e-6
 return dict(name=c['name'],outputs=actual,main=main,reheater=reheat,HP_entropy_gain=val(B,h2,'h','s')-s1,LP_entropy_gain=sf+(h4-hf)/(hg-hf)*(sg-sf)-s3,three_percent_allowance_MW=.03*gross,new_pumps_MW=pe+cw)
author=json.loads((OUT.parent/'cycle-results.json').read_text())
result={'independent_from':'author code; common original NIST property source','properties':meta,'cases':[run(c) for c in author['cases']]}
# Withhold alternate original knots, reconstruct them within each separate phase.
errors={}
for label,rows in [('main',M),('bleed',B),('condenser',C)]:
 errors[label]={}
 for ph in ['liquid','vapor']:
  r=phase(rows,ph);coarse=r[::2]+([r[-1]] if r[-1] not in r[::2] else [])
  errors[label][ph]={k:max(abs(val(coarse,v['T'],out=k)-v[k]) for v in r) for k in ['h','s']}
result['independent_coarse_refinement_errors']=errors
result['reviewed_artifact_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [OUT.parent/'cycle-proposal.md',OUT.parent/'cycle-prototype.py',OUT.parent/'cycle-results.json',OUT.parent/'cycle-author-checks.json']}
(OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'cases':len(result['cases']),'baseline':result['cases'][1],'refinement':errors},indent=2))
# Independently check incompressible pump work against isentropic h(s) in captured tables.
checks=[]
for name,down,sin,hin,w in [('feedwater',phase(M,'liquid'),bl['s'],bl['h'],bl['v']*5400)]+[(f'condensate_{T}',phase(B,'liquid'),val(phase(C,'liquid'),T,out='s'),val(phase(C,'liquid'),T),val(phase(C,'liquid'),T,out='v')*(.8-val(phase(C,'liquid'),T,out='P'))*1000) for T in (40,42,50)]:
 if not min(r['s'] for r in down)<=sin<=max(r['s'] for r in down):
  checks.append(dict(name=name,status='outside captured entropy domain; no extrapolation'));continue
 exact=val(down,sin,'s','h')-hin
 checks.append(dict(name=name,table_isentropic_kJ_kg=exact,incompressible_kJ_kg=w,relative_difference=w/exact-1))
result['pump_approximation_checks']=checks
(OUT/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
