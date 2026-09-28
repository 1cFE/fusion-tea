"""Offline bounded SG admission research, not a canonical plant implementation.
Original NIST6.2MPa tables; exact integration over phase-aware piecewise-linear T(h).
"""
from pathlib import Path
from html.parser import HTMLParser
import math,json,hashlib,csv,io,bisect
ROOT=Path(__file__).resolve().parents[7]
OUT=Path(__file__).parent
class Rows(HTMLParser):
 def __init__(self): super().__init__();self.rows=[];self.row=[];self.cell=None
 def handle_starttag(self,tag,attrs):
  if tag=='tr':self.row=[]
  if tag in ('td','th'):self.cell=''
 def handle_data(self,data):
  if self.cell is not None:self.cell+=data
 def handle_endtag(self,tag):
  if tag in ('td','th') and self.cell is not None:self.row.append(self.cell.strip());self.cell=None
  if tag=='tr' and len(self.row)==14 and self.row[-1] in ('liquid','vapor'): self.rows.append(self.row)
def load(slug):
 path=ROOT/'knowledge/sources'/slug/'raw.html'; p=Rows();p.feed(path.read_text())
 assert p.rows
 rows=[dict(T=float(r[0]),p=float(r[1]),h=float(r[5]),s=float(r[6]),cp=float(r[8]),phase=r[-1]) for r in p.rows]
 assert all(r['p']==6.2 for r in rows)
 return path,rows
sources={}
for name,slug in [('1K','nist_webbook_water6_2mpa171to455c_state_table'),('0.5K','nist_webbook_water6_2mpa171to455c_halfk_state_table')]:
 path,rows=load(slug);sources[name]=(path,rows)
# Fixed adopted-for-screening assumptions. No pressure drop or external heat loss.
T_HOT=465.;CP_SALT=1560.;HEAD=40.;ETA_P=.75;G=9.80665;T_IHX_COLD=270.;T_SINK=42.+273.15
DT_PUMP=G*HEAD/(ETA_P*CP_SALT);T_COLD=T_IHX_COLD-DT_PUMP;SPAN=T_HOT-T_COLD
BASELINE_PATH=ROOT/'work/orchestration/goals/current-model-comparison-readiness/evidence/entering-validation/baseline/baseline_result.json'
DEFAULTS_PATH=ROOT/'exploration/stellarator_e2e/generated/inputs/stellarator_plant_params.json'
BASELINE=json.loads(BASELINE_PATH.read_text());DEFAULTS=json.loads(DEFAULTS_PATH.read_text())
PREFIX='stellarator_09__stellaris__heat_transport__'
assert DEFAULTS[PREFIX+'n_loops']==14
assert DEFAULTS[PREFIX+'equipment_secondary_head']==HEAD
assert DEFAULTS[PREFIX+'equipment_eta_p']==ETA_P
assert DEFAULTS[PREFIX+'equipment_eta_motor']==.95
assert DEFAULTS[PREFIX+'loop_T_in']==573.15 and DEFAULTS[PREFIX+'loop_dT_blanket']==200
Q_IHX=BASELINE['channels'][PREFIX+'primary_loop__q_ihx'] # Current fourteen-circuit baseline.

MSALT=Q_IHX*1e6/(CP_SALT*195.);WSALT=MSALT*G*HEAD/ETA_P/1e6;QSG=Q_IHX+WSALT
assert abs(QSG-BASELINE['channels'][PREFIX+'equipment__conversion_heat_MW'])<1e-9
assert abs(WSALT-BASELINE['channels'][PREFIX+'equipment__salt_shaft_MW'])<1e-9
assert abs(T_COLD-BASELINE['channels'][PREFIX+'equipment__salt_return_C'])<1e-12
U_KW=[1.13,1.28,.993] # NASA effective-U transfer, F absorbed, NOT a validated target U.
def section(points,h0,h3,ms):
 gaps=[T_COLD+SPAN*(r['h']-h0)/(h3-h0)-r['T'] for r in points]
 ua=0.
 for a,b,g1,g2 in zip(points,points[1:],gaps,gaps[1:]):
  if min(g1,g2)<=0:raise ValueError('nonpositive temperature difference')
  dh=b['h']-a['h'];ua+=ms/1000*dh*(1/g1 if abs(g2-g1)<1e-12 else math.log(g2/g1)/(g2-g1))
 imin=min(range(len(gaps)),key=gaps.__getitem__)
 return dict(duty_MW=ms*(points[-1]['h']-points[0]['h'])/1000,min_gap_K=gaps[imin],min_at_water_C=points[imin]['T'],min_at_h_kJkg=points[imin]['h'],UA_MW_K=ua,points=len(points),gap_start_K=gaps[0],gap_end_K=gaps[-1],max_cp_kJ_kg_K=max(r['cp'] for r in points) if points[0]['phase']==points[-1]['phase'] else None,min_cp_kJ_kg_K=min(r['cp'] for r in points) if points[0]['phase']==points[-1]['phase'] else None)
def calc(rows,approach):
 t=T_HOT-approach;liq=[r for r in rows if r['phase']=='liquid'];vap=[r for r in rows if r['phase']=='vapor' and r['T']<=t]
 assert vap[-1]['T']==t;hf=liq[-1];hg=vap[0];h0=liq[0]['h'];h3=vap[-1]['h'];ms=QSG*1000/(h3-h0)
 sections=[section(liq,h0,h3,ms),section([hf,hg],h0,h3,ms),section(vap,h0,h3,ms)]
 for sec,u in zip(sections,U_KW):sec['illustrative_area_m2']=sec['UA_MW_K']*1000/u;sec['UA_per_MW_SG_per_K']=sec['UA_MW_K']/QSG
 eta=.1802*math.log(t+273)-.7823
 salt_exergy_fraction=1-T_SINK*math.log((T_HOT+273.15)/(T_COLD+273.15))/SPAN
 water_exergy_per_kg=(h3-h0)-T_SINK*(vap[-1]['s']-liq[0]['s'])
 qcheck=sum(s['duty_MW'] for s in sections)-QSG
 return dict(hot_approach_K=approach,minimum_section_approach_assumption_K=20,steam_C=t,steam_pressure_MPa=6.2,feedwater_C=171,saturation_C=hf['T'],h_feed_kJkg=h0,h_sat_liquid_kJkg=hf['h'],h_sat_vapor_kJkg=hg['h'],h_steam_kJkg=h3,s_feed_kJkgK=liq[0]['s'],s_steam_kJkgK=vap[-1]['s'],steam_flow_kg_s=ms,steam_flow_per_MW_SG=ms/QSG,section_names=['economizer','evaporator','superheater'],sections=sections,min_gap_K=min(s['min_gap_K'] for s in sections),thermal_20K_screen_satisfied=all(s['min_gap_K']>=20 for s in sections),energy_residual_MW=qcheck,UA_total_MW_K=sum(s['UA_MW_K'] for s in sections),illustrative_area_total_m2=sum(s['illustrative_area_m2'] for s in sections),salt_junctions_C=[T_COLD,T_COLD+SPAN*(hf['h']-h0)/(h3-h0),T_COLD+SPAN*(hg['h']-h0)/(h3-h0),T_HOT],conditional_Kovari_efficiency=eta,salt_heat_exergy_ceiling_fraction=salt_exergy_fraction,salt_heat_exergy_MW=QSG*salt_exergy_fraction,water_exergy_gain_MW=ms*water_exergy_per_kg/1000,heat_transfer_exergy_destruction_MW=QSG*salt_exergy_fraction-ms*water_exergy_per_kg/1000,conditional_cycle_MW=QSG*eta,SG_hardware_capacity_status='not established',cycle_efficiency_status='conditional surrogate, not proved by admission')
results={name:[calc(rows,a) for a in [10,20,30]] for name,(path,rows) in sources.items()}
coarse=sources['1K'][1];fine=sources['0.5K'][1];errors=[]
for phase in ['liquid','vapor']:
 c=[r for r in coarse if r['phase']==phase];ts=[r['T'] for r in c]
 for r in (r for r in fine if r['phase']==phase):
  j=bisect.bisect_left(ts,r['T'])
  if j<len(c) and ts[j]==r['T']:assert c[j]==r;continue
  a,b=c[j-1],c[j];f=(r['T']-a['T'])/(b['T']-a['T']);he=a['h']+f*(b['h']-a['h']);te=a['T']+(r['h']-a['h'])/(b['h']-a['h'])*(b['T']-a['T'])
  errors.append(dict(T=r['T'],phase=phase,enthalpy_error_kJkg=he-r['h'],inverse_temperature_error_K=te-r['T']))
refinements=[]
for c,f in zip(results['1K'],results['0.5K']):refinements.append(dict(hot_approach_K=c['hot_approach_K'],total_UA_relative_change=(f['UA_total_MW_K']-c['UA_total_MW_K'])/c['UA_total_MW_K'],max_section_UA_relative_change=max(abs(y['UA_MW_K']-x['UA_MW_K'])/x['UA_MW_K'] for x,y in zip(c['sections'],f['sections'])),minimum_gap_change_K=f['min_gap_K']-c['min_gap_K']))
meta=dict(baseline_kind='current integrated14circuit baseline',baseline_identity=BASELINE['executed_under'],baseline_sha256=hashlib.sha256(BASELINE_PATH.read_bytes()).hexdigest(),effective_defaults_sha256=hashlib.sha256(DEFAULTS_PATH.read_bytes()).hexdigest(),Q_IHX_reference_MW=Q_IHX,Q_SG_reference_MW=QSG,salt_flow_kg_s=MSALT,salt_shaft_MW=WSALT,salt_return_to_pump_C=T_COLD,salt_return_to_IHX_C=T_IHX_COLD,salt_supply_C=T_HOT,salt_cp_JkgK=CP_SALT,sink_C=42,source_rows={n:len(r) for n,(p,r) in sources.items()},source_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p,r in sources.values()},max_midpoint_enthalpy_error_kJkg=max(abs(r['enthalpy_error_kJkg']) for r in errors),max_midpoint_inverse_temperature_error_K=max(abs(r['inverse_temperature_error_K']) for r in errors),refinement=refinements,claim='Steady countercurrent adiabatic admission screening at fixed pressure, not physical hardware qualification or validated cycle efficiency.')
(OUT/'results.json').write_text(json.dumps(dict(metadata=meta,cases=results),indent=2)+'\n')
(OUT/'interpolation-errors.json').write_text(json.dumps(errors,indent=2)+'\n')
with (OUT/'water-properties-halfK.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['T','p','h','s','cp','phase']);w.writeheader();w.writerows(fine)
print(json.dumps(meta,indent=2))
for c in results['0.5K']:print(json.dumps({k:c[k] for k in ['hot_approach_K','steam_flow_kg_s','min_gap_K','thermal_20K_screen_satisfied','UA_total_MW_K','salt_junctions_C','water_exergy_gain_MW','heat_transfer_exergy_destruction_MW']}))
