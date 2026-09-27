"""Independent scouting and explicit proposal selection; no native physics execution.

All thermal/economic values and predicates are supplied by the package-owned
independent oracle. The actual study uses stock StudyRunner, separately.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from exploration.exchanger_architecture.thermal_requirements.studies import study_route as route, oracle_entry
from scripts.study import common, manifest, verify

GOAL = ROOT/'work/orchestration/goals/design-study-exchanger-architecture'
RECORD = ROOT/'exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison'
P = 'aries_integrated_plant__'
BRANCHES = ('he', 'pbli', 'divertor')
LOADS = (1650., 1835.4512830147435, 1950., 2000.)
OFFERS = {'original': (50000.,50000.,50000.), 'A':(12000.,12000.,2000.), 'B':(18000.,18000.,2000.)}
SCENARIOS = ('main','approach15','approach45','U0.8','U1.2','loss0.02','loss0.08','pump0.8','pump1.2','bypass0.25','bypass0.5','post-pump-return')

def key(owner, field): return P+owner+'__'+field

def out(owner, field): return key(owner, 'evaluate__'+field)

def read(path): return json.loads(path.read_text())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f: json.dump(value, f, separators=(',',':'), allow_nan=False); f.write('\n')


def definitions():
    rows = [
        ('source_mode',['source__producer_mode'],'sensitivity','Legacy baseline and supplied source boundary; no plasma sustainment claim.'),
        ('source_load',['source__reference_fusion_mw'],'search','Matched loads 1650,1835.4512830147435,1950,2000 MW; old leaders and source-cap boundary controls.'),
        ('architecture',['heat_exchangers__network_mode'],'search','Series and series-then-parallel secondary connections.'),
        ('flow',['cycle__selected_flow'],'search','Common broad flow scan; independently refine every sampled feasible component.'),
        ('split',['heat_exchangers__pbli_split_fraction'],'search','Network split .1–.9 initially, local refinement to .0005; series inert placeholder .85.'),
        ('control_mode',['heat_exchangers__control_mode'],'sensitivity','Legacy0 control and main1 explicit primary bypass.'),
        ('offer',[b+'_hx__'+f for b in BRANCHES for f in ('selected_area','price_factor')],'sensitivity','Explicit original,A,B areas/prices, common price multiplier and inherited linear price sensitivity; coordinated offers, no physical identity asserted.'),
        ('approach',['heat_exchangers__'+b+'_'+f+'_approach' for b in BRANCHES for f in ('hot','cold')],'sensitivity','Main30K, labelled15/45K engineering requirements.'),
        ('conductance',[b+'_hx__assumed_u' for b in BRANCHES],'sensitivity','Correlated U multipliers .8/1.2 at fixed area; not a resizing law.'),
        ('pressure_loss',['pressure_loss__loss_fraction'],'sensitivity','Common .02/.08 and differential network-loss comparison against baseline .045.'),
        ('pump_mode',[b+'_pump__pump_mode' for b in BRANCHES],'sensitivity','Coordinated explicit fixed-power scenarios.'),
        ('pump_power',[b+'_pump__fixed_power' for b in BRANCHES],'sensitivity','Each pump own reference power multiplied by .8/1.2; recovered heat recomputed.'),
        ('bypass_limit',['heat_exchangers__'+b+'_max_bypass' for b in BRANCHES],'sensitivity','Main mathematical range1; assumed limits.25/.5, no actuator rating claim.'),
        ('return_convention',['heat_exchangers__'+b+'_required_return' for b in BRANCHES],'sensitivity','Main aggregate targets; alternate post-pump-source reading subtracts booked recovered heat/Ch from aggregate return.'),
        ('tritium_price',['fuel_inventory__tritium_price'],'sensitivity','Zero-price accounting endpoint reprices initial stock and annual purchases.'),
    ]
    axes=[]; ties=[]
    for axis,names,framing,basis in rows:
        keys=[P+n for n in names]
        axes.append(dict(axis=axis,keys=[dict(key=k,provenance='fan_out' if i==0 else 'tie') for i,k in enumerate(keys)],framing=framing,basis='[AGENT] '+basis,window_provenance='engineered'))
        ties += [dict(key=k,rides_with=[keys[0]],note='[AGENT] Coordinated scenario; distinct quantities remain distinct. '+basis) for k in keys[1:]]
    declared=[k['key'] for a in axes for k in a['keys']]
    assert len(declared)==len(set(declared)) and set(declared)<=set(route.interface()['entry_keys']), set(declared)-set(route.interface()['entry_keys'])
    return axes,ties


def prepare():
    common.assert_tree_clean(route.PACKAGE_DIR)
    loaded=manifest.load(route.MANIFEST_PATH)
    manifest.assert_pin_matches(loaded,manifest.indicator_input_fingerprint(route.PACKAGE_DIR))
    axes,ties=definitions()
    if RECORD.exists(): raise ValueError('record exists; preserve prior evidence')
    RECORD.mkdir(parents=True)
    write(RECORD/'manifest.json',loaded.data|{'ties':ties})
    write(RECORD/'axes.json',{'schema_version':'study-axis-declaration/v1','groups':[{'axis':a['axis'],'keys':a['keys'],'note':a['basis']} for a in axes]})
    write(RECORD/'axis-plan.json',{'axes':axes,'loads':LOADS,'offers_m2':OFFERS,'price_per_hx_usd2004':58325700.,'scenarios':SCENARIOS,'flow_scan':[500,2400,50],'split_scan':[.1,.9,.05],'flow_bracket_kg_s':.025,'split_final_spacing':.0005,'native_execution_authorized':False})
    for name in ('owner-brief.md','owner-supplement-r2.md','owner-supplement-r3.md','r2-thermal-requirements.md','r2-source-review.md','r3-study-contract.md','r3-cost-boundary.md','r3-protocol-review.md'):
        shutil.copyfile(GOAL/'evidence'/name,RECORD/name)
    write(RECORD/'baseline-inputs.json',loaded.data['baseline']['point'])
    template=(ROOT/'.agents/skills/run-study/record-template.md').read_text()
    (RECORD/'record-template-source.md').write_text(template)
    import re
    heads=re.findall(r'^## (?:[1-9]|1[0-7])\. .+$',template,re.M)[:17]
    (RECORD/'record.md').write_text('# Study record — thermally consistent exchanger comparison\n\n'+'\n\n'.join(h+'\n\nPreparation pending; execution not released.' for h in heads)+'\n')
    print(json.dumps({'record':str(RECORD),'axes':len(axes)}))


class Scout:
    def __init__(self):
        self.base=read(RECORD/'baseline-inputs.json')
        self.catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
        self.bindings=oracle_entry.operand_bindings()
        self.cache={}; self.rows=[]; self.proposals={}; self.aliases=[]; self.selected=[]
        self.declared={k['key'] for a in read(RECORD/'axis-plan.json')['axes'] for k in a['keys']}
        self.development=read(ROOT/'work/active/WI-097_exchanger-thermal-requirements/evidence/development-followup.json')['rows']
        self.checkpoint_start=0

    def point(self,load,offer,mode,flow,split,scenario):
        p=dict(self.base)
        p.update({key('source','producer_mode'):0.,key('source','reference_fusion_mw'):load,key('heat_exchangers','control_mode'):1.,key('heat_exchangers','network_mode'):float(mode),key('cycle','selected_flow'):float(flow),key('heat_exchangers','pbli_split_fraction'):float(split)})
        for b,area in zip(BRANCHES,OFFERS[offer]):
            p[key(b+'_hx','selected_area')]=area
            p[key(b+'_hx','price_factor')]=50000./area
        if scenario.startswith('approach'):
            for b in BRANCHES:
                for end in ('hot','cold'): p[key('heat_exchangers',b+'_'+end+'_approach')]=float(scenario[8:])
        elif scenario.startswith('U'):
            for b in BRANCHES: p[key(b+'_hx','assumed_u')]*=float(scenario[1:])
        elif scenario.startswith('loss'): p[key('pressure_loss','loss_fraction')]=float(scenario[4:])
        elif scenario.startswith('pump'):
            for b in BRANCHES:
                p[key(b+'_pump','pump_mode')]=1.
                p[key(b+'_pump','fixed_power')]=p[key(b+'_pump','reference_power')]*float(scenario[4:])
        elif scenario.startswith('bypass'):
            for b in BRANCHES:p[key('heat_exchangers',b+'_max_bypass')]=float(scenario[6:])
        elif scenario=='post-pump-return':
            for b in BRANCHES:
                # Source temperature interpreted after pump: upstream aggregate
                # target is lower by the already counted recovered pump heat.
                recovered=p[key(b+'_pump','reference_power')]*p[key('deposition',b+'_recovery')]
                capacity=p[key('heat_exchangers',b+'_flow')]*p[key('heat_exchangers',b+'_cp')]/1e6
                p[key('heat_exchangers',b+'_required_return')]-=recovered/capacity
        elif scenario!='main':raise ValueError(scenario)
        return p

    def evaluate(self,p,meta):
        ident=tuple(sorted(p.items()))
        if ident in self.cache:return self.cache[ident]
        if len(self.rows)>=200000:raise RuntimeError('Declared 200,000-point oracle budget reached; retained checkpoints require a scope review.')
        changed={k:v for k,v in p.items() if v!=self.base[k]}
        assert set(changed)<=self.declared,set(changed)-self.declared
        row={'scan_id':len(self.rows),'metadata':meta,'changes':changed}
        try:
            vals=oracle_entry.evaluate(p)
            verdicts={cid:'satisfied' if verify.derive_verdict(cid,e,self.bindings,p,{},vals)[0] else 'violated' for cid,e in self.catalog.items()}
            row.update(status='evaluated',failed=[cid for cid,v in verdicts.items() if v!='satisfied'],net=vals[out('plant_ledger','net_electric')],lcoe=vals[out('lifecycle_price','lcoe')])
            row['pass']=not row['failed'] and row['net']>0
            row['thermal']={k.rsplit('__',1)[-1]:v for k,v in vals.items() if k.startswith(P+'heat_exchangers__evaluate__')}
        except Exception as e:row.update(status='refused',error=type(e).__name__+': '+str(e),**{'pass':False})
        self.rows.append(row); self.cache[ident]=row
        return row

    def get(self,load,offer,mode,flow,split,scenario):
        meta=dict(load=load,offer=offer,mode=mode,flow=round(float(flow),10),split=round(float(split),10),scenario=scenario)
        p=self.point(load,offer,mode,meta['flow'],meta['split'],scenario)
        return self.evaluate(p,meta)

    def propose(self,row,label):
        m=row['metadata']; p=self.base|row['changes']; ident=tuple(sorted(p.items()))
        if row['status']!='evaluated' or row.get('net',0)<=0:return
        if ident in self.proposals:
            self.aliases.append({'label':label,'case':self.proposals[ident]['case']});return
        name=f'case-{len(self.proposals):05d}'
        self.proposals[ident]=dict(case=name,classification=label,metadata=m,scan_id=row['scan_id'],point=p)

    def boundary(self,load,offer,mode,split,scenario,left,right):
        a=self.get(load,offer,mode,left,split,scenario); b=self.get(load,offer,mode,right,split,scenario)
        assert a['pass']!=b['pass']
        while right-left>.025:
            middle=(left+right)/2
            c=self.get(load,offer,mode,middle,split,scenario)
            if c['pass']==a['pass']:left=middle;a=c
            else:right=middle;b=c
        return a,b

    def line(self,load,offer,mode,split,scenario,retain=False):
        flows=set(range(500,2401,50))
        # Known development passes remain seeds, not accepted results. Include
        # them for perturbed scenarios too; the oracle recomputes everything.
        old_offer={'A':'matched_small','B':'matched_medium'}.get(offer)
        flows.update(r['cycle_flow_kg_s'] for r in self.development if r['thermal_pass'] and r['load_mw']==load and r['offer']==old_offer and r['mode']==mode and (mode==0 or abs(r['split']-split)<1e-8))
        rows=[self.get(load,offer,mode,f,split,scenario) for f in sorted(flows)]
        # A same-status failed pair can hide a narrow passing interval. Sample
        # its interior in the development-supported operating neighborhood.
        extra=[]
        for a,b in zip(rows,rows[1:]):
            left,right=a['metadata']['flow'],b['metadata']['flow']
            if not a['pass'] and not b['pass'] and 900<=left<right<=1800 and right-left>12.5:
                extra.extend(self.get(load,offer,mode,left+(right-left)*t,split,scenario) for t in (.25,.5,.75))
        rows=sorted(rows+extra,key=lambda r:r['metadata']['flow'])
        passing=[r for r in rows if r['pass']]
        edges=[]
        for a,b in zip(rows,rows[1:]):
            if a['pass']!=b['pass']:
                pair=self.boundary(load,offer,mode,split,scenario,a['metadata']['flow'],b['metadata']['flow'])
                edges.extend(pair);passing.extend(r for r in pair if r['pass'])
        if retain:
            for r in edges:self.propose(r,'component-boundary')
            for r in (rows[0],rows[-1]):self.propose(r,'scan-edge-control')
        return max(passing,key=lambda r:r['net'],default=None)

    def search(self,load,offer,mode,scenario):
        splits=[.85] if mode==0 else [round(.1+i*.05,10) for i in range(17)]
        minima=[self.line(load,offer,mode,s,scenario,retain=True) for s in splits]
        candidates=[r for r in minima if r]
        levels=[]
        if candidates and mode:
            # Refine every coarse local maximum and isolated feasible component.
            anchors=[]
            for i,r in enumerate(minima):
                if r and all(other is None or r['net']>=other['net'] for other in minima[max(0,i-1):i]+minima[i+1:i+2]):anchors.append(r)
            for spacing,halfwidth in ((.005,.05),(.001,.006),(.0005,.0015)):
                new=[]
                for anchor in anchors:
                    center=anchor['metadata']['split']
                    ss=[round(center+j*spacing,10) for j in range(-round(halfwidth/spacing),round(halfwidth/spacing)+1) if .001<=center+j*spacing<=.999]
                    local=[self.line(load,offer,mode,s,scenario) for s in ss]
                    local=[r for r in local if r]
                    if local:new.append(max(local,key=lambda r:r['net']))
                if not new:break
                anchors=new;candidates+=new
                best=max(new,key=lambda r:r['net']);levels.append({'spacing':spacing,'scan_id':best['scan_id'],'net':best['net'],'lcoe':best['lcoe']})
        best=max(candidates,key=lambda r:r['net'],default=None)
        result=dict(load=load,offer=offer,mode=mode,scenario=scenario,best_scan_id=best['scan_id'] if best else None,refinement=levels,edge_passes=[r['metadata'] for r in self.rows if r['metadata'].get('load')==load and r['metadata'].get('offer')==offer and r['metadata'].get('mode')==mode and r['metadata'].get('scenario')==scenario and r['pass'] and (r['metadata'].get('flow') in (500,2400) or r['metadata'].get('split') in (.1,.9))])
        if best:
            self.propose(best,'selected-best-tested')
            f=best['metadata']['flow'];s=best['metadata']['split']
            before=dict(scan_id=best['scan_id'],net=best['net'],lcoe=best['lcoe'])
            # Final local half-step and neighboring failures, all executed.
            for df in (-.05,-.025,-.0125,0,.0125,.025,.05):
                r=self.get(load,offer,mode,f+df,s,scenario);self.propose(r,'final-flow-neighbor')
                if r['pass'] and r['net']>best['net']:best=r
            result['best_scan_id']=best['scan_id']
            if mode:
                for ds in (-.001,-.0005,.0005,.001):
                    r=self.get(load,offer,mode,best['metadata']['flow'],s+ds,scenario)
                    self.propose(r,'final-split-neighbor')
                    if r['pass'] and r['net']>best['net']:best=r
                    adjusted=self.line(load,offer,mode,s+ds,scenario)
                    if adjusted:
                        self.propose(adjusted,'final-split-flow-refinement')
                        if adjusted['net']>best['net']:best=adjusted
            result['best_scan_id']=best['scan_id']
            result['final_neighborhood_change']={'before':before,'after':{'scan_id':best['scan_id'],'net':best['net'],'lcoe':best['lcoe']},'delta_net':best['net']-before['net'],'delta_lcoe':best['lcoe']-before['lcoe']}
            fixed_split=best['metadata']['split'];fixed_flow=best['metadata']['flow'];flow_before=best
            for df in (-.0125,-.00625,.00625,.0125):
                r=self.get(load,offer,mode,fixed_flow+df,fixed_split,scenario)
                self.propose(r,'final-selected-split-flow-halving')
                if r['pass'] and r['net']>best['net']:best=r
            result['best_scan_id']=best['scan_id']
            result['flow_halving']={'before_scan_id':flow_before['scan_id'],'after_scan_id':best['scan_id'],'fixed_split':fixed_split,'delta_net':best['net']-flow_before['net'],'delta_lcoe':best['lcoe']-flow_before['lcoe']}
            if len(levels)>=2:
                result['split_halving']={'delta_net':levels[-1]['net']-levels[-2]['net'],'delta_lcoe':levels[-1]['lcoe']-levels[-2]['lcoe']}
            result['stability_pass']=abs(result['flow_halving']['delta_net'])<=.2 and abs(result['flow_halving']['delta_lcoe'])<=.1 and all(abs(result.get('split_halving',{}).get(k,0))<=limit for k,limit in (('delta_net',.2),('delta_lcoe',.1)))
        self.selected.append(result)
        write(RECORD/'scan-checkpoints'/f'component-{len(self.selected):03d}.json',{'rows':self.rows[self.checkpoint_start:],'selection':result})
        self.checkpoint_start=len(self.rows)
        print(json.dumps(result|{'edge_passes':len(result['edge_passes'])}),flush=True)

    def run(self):
        for load in LOADS:
            for offer in ('A','B'):
                for mode in (0,1):self.search(load,offer,mode,'main')
        for scenario in SCENARIOS[1:]:
            for mode in (0,1):self.search(LOADS[1],'B',mode,scenario)
        # Matched passing flow isolates the connection change from operating
        # freedom. Keep any failure visible instead of declaring equivalence.
        for load in LOADS:
            for offer in ('A','B'):
                pair=[s for s in self.selected if s['load']==load and s['offer']==offer and s['scenario']=='main']
                if len(pair)!=2 or any(s['best_scan_id'] is None for s in pair):continue
                best=[self.rows[s['best_scan_id']] for s in pair]
                flow=max(r['metadata']['flow'] for r in best)+.1
                for r in best:
                    m=r['metadata']
                    self.propose(self.get(load,offer,m['mode'],flow,m['split'],'main'),'equal-flow-control')
        for load in (LOADS[1],2000.,2005.,2005.04,2200.,2300.):
            for offer in ('original','A','B'):
                for mode in (0,1):self.propose(self.get(load,offer,mode,1400.,.7 if mode else .85,'main'),'fixed-equipment-and-hot-cap-control')
        # Financial endpoints at every selected passing main case.
        for selection in self.selected:
            if selection['scenario']!='main' or selection['best_scan_id'] is None:continue
            parent=self.rows[selection['best_scan_id']]
            for scenario,factor in (('zero-tritium',0.),('price-half',.5),('price-double',2.),('linear-area-price',1.)):
                p=self.base|parent['changes']; meta=parent['metadata']|{'scenario':scenario,'parent_scan_id':parent['scan_id']}
                if scenario=='zero-tritium':p[key('fuel_inventory','tritium_price')]=0.
                else:
                    for b in BRANCHES:p[key(b+'_hx','price_factor')]=1. if scenario=='linear-area-price' else p[key(b+'_hx','price_factor')]*factor
                self.propose(self.evaluate(p,meta),'financial-sensitivity')
        write(RECORD/'oracle-scan.json',{'kind':'independent oracle scan; not native execution','base_inputs':'baseline-inputs.json','cases':self.rows})
        write(RECORD/'oracle-selection.json',{'selected':self.selected,'scope':'Best tested passing operations; sampled components, no global optimum proof.'})
        write(RECORD/'proposed-points.json',{'cases':list(self.proposals.values()),'aliases':self.aliases})
        print(json.dumps({'scanned':len(self.rows),'native_proposals':len(self.proposals)}))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=('prepare','scan'));args=parser.parse_args()
    if args.action=='prepare':prepare()
    else:Scout().run()
