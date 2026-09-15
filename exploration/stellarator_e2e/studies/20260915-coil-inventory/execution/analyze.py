"""Record-local comparison of every required mapped scalar and all historical case identities."""
import csv,json,math
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parents[1];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
def write(name,data):(R/name).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def key(p):return json.dumps({k:float(v) for k,v in p.items()},sort_keys=True)
rows=list(csv.DictReader((R/'points.csv').open()))
scan=read(R/'oracle-scan.json'); byscan={(arm,key(r['point'])):r for arm,rs in scan['arms'].items() for r in rs}
inputs={(r['arm_id'],r['candidate_id']):r['inputs'] for r in read(R/'case-inputs.json')}
verdicts=list(next(iter(scan['arms'].values()))[0]['verdicts'])
required=read(H/'preparation/required-channels.json');fail=[];worst=0;comparisons=0
for r in rows:
    pt=inputs[(r['arm_id'],r['candidate_id'])];s=byscan[(r['arm_id'],key(pt))]
    for full in required:
        c=full[len(P):]
        if full not in s['channels']:continue
        got=float(r[c]);want=s['channels'][full];dev=abs(got-want)/max(abs(got),abs(want),1e-100)
        worst=max(worst,dev);comparisons+=1
        if not math.isclose(got,want,rel_tol=1e-9,abs_tol=1e-12):fail.append({'id':r['candidate_id'],'channel':full,'native':got,'oracle':want})
    for v in verdicts:
        if r[v]!=s['verdicts'][v]:fail.append({'id':r['candidate_id'],'predicate':v})
# Supplement existing unmapped circumference/cold-volume channels using declared identities.
params={}
for p in (H.parent.parent/'generated/inputs').glob('*.json'):params.update(read(p))
for r in rows:
    cc=float(r['magnet__coil_length__c_coil']);rc=float(r['rb__r_coil_centre'])
    assert math.isclose(cc,params[P+'magnet__coil__c_coil_ref']*rc/params[P+'magnet__coil__a_coil_ref'],rel_tol=1e-12)
    assert math.isclose(float(r['magnet__wp_volume__vol_cold_total']),float(r['magnet__wp_volume__vol_winding_pack'])+params[P+'magnet__vol_cold_cryo'],rel_tol=1e-12)
write('oracle-all-points.json',{'outcome':'pass' if not fail else 'fail','rows':len(rows),'scalar_comparisons':comparisons,'predicate_comparisons':len(rows)*len(verdicts),'max_relative_deviation':worst,'failures':fail,'identity_checks':['bore circumference','cold volume'],'unmapped_required_channels':[k for k in required if k not in next(iter(byscan.values()))['channels']]})
assert not fail,fail[:3]
L='lcoe_calc__lcoe';CR='cryoplant__refrigeration_sum__total';OLDCR='cryoplant__cryo_elec__p_elec'
def feasible(r):return all(r[v]=='satisfied' for v in verdicts)
def values(r):
    return {'candidate_id':r['candidate_id'],'arm':r['arm_id'],'column':r['column'],'source_case':r['source_case'],'inputs':inputs[(r['arm_id'],r['candidate_id'])],
            'lcoe':float(r[L]),'feasible_18':feasible(r),'violated':[v for v in verdicts if r[v]!='satisfied'],
            'cryo_MW':float(r[CR]),'cryo_share':float(r[CR])/(float(r['pb__p_et'])-float(r['pb__p_net'])),
            'magnet_capital':float(r['magnet__magnet_capital_rollup__capital_cost']),
            'support_cost':float(r['magnet__magnet_structure_cost__cost']),'support_mass':float(r['magnet__support_mass__m_support'])}
# Attributed WI-059 delta uses immediately entering Round1, with exact row coordinates.
old=list(csv.DictReader((H/'preparation/entering-points.csv').open()));nom=[r for r in rows if r['arm_id']!='arm-assumptions'];assert len(old)==len(nom)==159
inputcols=['plasma__R','plasma__a','magnet__coil__I_coil','magnet__winding_pack__B_max','plasma__n_e0','heating__p_wallplug_heat','availability_direct']
deltas=[]
for before,after in zip(old,nom,strict=True):
    for k in ['arm_id','column','source_case',*inputcols]:assert before[k]==after[k],(k,before[k],after[k])
    deltas.append({'entering_case':before['candidate_id'],'current_case':after['candidate_id'],'arm':after['arm_id'],'column':after['column'],'source_case':after['source_case'],
                   'lcoe_before':float(before[L]),'lcoe_after':float(after[L]),'lcoe_delta':float(after[L])-float(before[L]),
                   'cryo_before':float(before[OLDCR]),'cryo_after':float(after[CR]),
                   'verdict_flips':{v:[before[v],after[v]] for v in verdicts if before[v]!=after[v]}})
write('comparison-entering-round1.json',{'basis':'Attributed WI-059 increment; committed entering Round1 package','cases':deltas})
# Older-package reference comparisons retain original case IDs and make no increment attribution.
older=read(H/'preparation/before-matched-window.json');oldby={r['source_case']:r for r in older['cases']};refs=[]
for r in rows:
    if r['arm_id']!='arm-matched-window':continue
    b=oldby[r['source_case']];bv=b['committed_verdicts']
    # Preparation records short names; refuse a missing authored predicate.
    assert set(verdicts)<=set(bv)
    refs.append({'source_case':r['source_case'],'current_case':r['candidate_id'],'lcoe_before':b['committed_lcoe'],'lcoe_after':float(r[L]),'verdict_flips':{v:[bv[v],r[v]] for v in verdicts if bv[v]!=r[v]}})
write('comparison-older-matched.json',{'basis':'Historical reference only; multiple model increments separate packages','source_pin':older['source_pin'],'cases':refs})
oldpc=read(H/'preparation/before-plant-closure-anchors.json');anchors=[]
for source,b in oldpc['cases'].items():
    col='cheap-100' if source.endswith('c0113') else 'cheap-220'
    r=next(r for r in nom if r['arm_id']=='arm-a-transect' and r['column']==col and float(r['plasma__a'])==1.7)
    br=b['row'];anchors.append({'source_case':source,'current':values(r),'historical_lcoe':float(br.get('lcoe',br.get(L))),'verdict_flips':{v:[br[v],r[v]] for v in verdicts if br[v]!=r[v]}})
write('comparison-plant-closure.json',{'basis':'Historical reference only; multiple model increments separate packages','source_pin':oldpc['source_pin_extra'],'cases':anchors})
columns=[]
for arm in ('arm-a-transect','arm-R-transect'):
    for col in sorted({r['column'] for r in rows if r['arm_id']==arm}):
        subset=[r for r in rows if r['arm_id']==arm and r['column']==col];fs=[r for r in subset if feasible(r)]
        columns.append({'arm':arm,'column':col,'rows':len(subset),'feasible_18_rows':len(fs),'unrestricted_price_minimum':values(min(subset,key=lambda r:float(r[L]))),'sampled_feasible_minimum':values(min(fs,key=lambda r:float(r[L]))) if fs else None})
counts={arm:{'rows':len(rs),'feasible_18_rows':sum(feasible(r) for r in rs),'violations_by_predicate':{v:sum(r[v]!='satisfied' for r in rs) for v in verdicts}} for arm in scan['arms'] for rs in [[r for r in rows if r['arm_id']==arm]]}
design=next(r for r in nom if r['arm_id']=='arm-a-transect' and r['column']=='design' and float(r['plasma__a'])==1.3)
write('analysis.json',{'design':values(design),'columns':columns,'counts':counts,'assumptions':[values(r) for r in rows if r['arm_id']=='arm-assumptions'],'attributed_verdict_flips':sum(bool(r['verdict_flips']) for r in deltas),'historical_matched_verdict_flips':sum(bool(r['verdict_flips']) for r in refs),'note':'Nominal geometric minima exclude assumption-altered cases. Every feasible count requires all18predicates.'})
print('ANALYSIS PASS',len(rows),'rows',comparisons,'scalar comparisons',worst,'max relative error')
