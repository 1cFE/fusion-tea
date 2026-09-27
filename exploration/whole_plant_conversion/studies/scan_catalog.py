"""Independent preflight scan and complete-point builder; never native execution.

Requires the released integration identity. Every oracle result is planning evidence;
final comparisons and ranking must be re-derived from stored native results.
"""
from __future__ import annotations
import argparse,hashlib,json,math
from collections import Counter
from functools import lru_cache
from pathlib import Path
from exploration.whole_plant_conversion import verify
from exploration.whole_plant_conversion.studies import proposals as offers,scenarios,study_route
from scripts.study import common,manifest
P=offers.P
SHARED_OWNERS={'source_checks','source_basis','supplied_core','cryogenic_demand','primary_offer','fuel_accounts'}
GAS_OWNERS={'water_ic1','water_ic2','water_pre','turbine_capacity','generator_capacity','he_capacity','recuperator_duty_capacity','rejection_capacity','compressor_capacity'}
GAS_HARDWARE={'cycle__selected_flow','recuperator_hardware__ua','conversion_services__price_factor',
              *(f'compressor_{i}__selected_ratio' for i in (1,2,3)),
              *(f'{owner}__ua' for owner in ('water_ic1','water_ic2','water_pre'))}
STEAM_HARDWARE={'steam_transport__n_loops','steam_transport__salt_pumps_per_circuit','steam_transport__selected_salt_design_flow_kg_s'}

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def dump(path,value):path.write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')

def predicate_catalog():
    result={}
    for cid,bindings in verify.operand_bindings().items():
        owner=cid.removeprefix(P).split('__')[0]
        if owner in SHARED_OWNERS:branch='shared'
        elif owner.startswith(('steam_','salt_')):branch='steam'
        elif owner.startswith('gas_') or owner in GAS_OWNERS:branch='gas'
        else:raise ValueError('unassigned predicate owner '+owner)
        result[cid]=dict(owner=owner,branch=branch,operands=bindings,
          authored_definition=verify.authored_constraint_types().get(cid.rsplit('__',1)[0]))
    if len(result)!=125:raise ValueError('review changed predicate census before scanning')
    return result

def predicate_input_dependencies(catalog,base):
    """Conservative input reachability through native wiring, without body math.

    Every output inherits all inputs of its producing calculation. This can force
    extra oracle evaluations; it cannot incorrectly prove an affected output fixed.
    """
    pipeline=verify.yaml.safe_load((verify.PACKAGE/'pipelines/pipeline.yaml').read_text())
    producers={}
    for module in pipeline['modules'].values():
        for source in module.get('outputs',{}).values():
            producers[source.split(' ',1)[1].removesuffix('.root')]=module
    @lru_cache(None)
    def dependencies(name):
        name=name.removesuffix('.root')
        if name in base:return frozenset([name])
        if '.' in name:
            prefix,tail=name.split('.',1)
            if prefix.endswith('_params') and tail in base:return frozenset([tail])
        if name not in producers:raise ValueError('unresolved dependency channel '+name)
        module=producers[name]
        if module['module_type']=='EntryPoint':raise ValueError('unresolved entry leaf '+name)
        refs=[source.split(' ',1)[1] for source in module.get('inputs',{}).values()]
        return frozenset().union(*(dependencies(ref) for ref in refs))
    return {cid:sorted(set().union(*(set([binding['key']]) if binding['kind']=='input' else dependencies(binding['key']) for binding in item['operands'].values()))) for cid,item in catalog.items()}

class Scanner:
    def __init__(self,base):
        self.base=dict(base);self.predicates=predicate_catalog();self.dependencies=predicate_input_dependencies(self.predicates,base);self.cache={};self.candidates={};self.roles=[];self.admission_audit=[]
    def evaluate(self,point):
        if set(point)!=set(self.base) or any(not math.isfinite(x) for x in point.values()):raise ValueError('invalid complete scan point')
        key=digest(point)
        if key in self.cache:return self.cache[key]
        row=dict(point_id=key,input_delta={k:v for k,v in point.items() if self.base[k]!=v})
        try:outputs=verify.evaluate(point)
        except (ValueError,ZeroDivisionError) as error:
            if str(error).startswith('unknown oracle inputs'):raise RuntimeError('scan input surface changed or disappeared during evaluation') from error
            row.update(status='oracle_refusal',error=str(error),eligible=dict(steam=False,gas=False),failed=dict(steam=[],gas=[]),outputs={})
        else:
            verdicts={}
            for cid,item in self.predicates.items():
                operands={k:(point if x['kind']=='input' else outputs)[x['key']] for k,x in item['operands'].items()}
                verdicts[cid]='satisfied' if verify.predicate(operands,item['authored_definition']) else 'violated'
            failed={b:[cid for cid,state in verdicts.items() if state=='violated' and self.predicates[cid]['branch'] in ('shared',b)] for b in ('steam','gas')}
            selected={k:v for k,v in outputs.items() if any(k.startswith(P+owner+'__') for owner in ('steam_whole','gas_whole','steam_operating','gas_operating','source_basis','fuel_accounts','cryogenic_demand','primary_offer'))}
            row.update(status='evaluated',outputs=selected,verdicts=verdicts,failed=failed,eligible={b:not failed[b] and math.isfinite(outputs[P+b+'_whole__evaluate__lcoe_USD2025_MWh']) and outputs[P+b+'_whole__evaluate__lcoe_USD2025_MWh']>0 for b in failed},independent_scalar_count=len(outputs))
        self.cache[key]=row
        if len(self.cache)%100==0:print('independent oracle points',len(self.cache),flush=True)
        return row
    def value(self,row,branch,field='lcoe_USD2025_MWh'):
        return row['outputs'][P+branch+'_whole__evaluate__'+field]
    def add(self,description):
        point=description['point'];key=digest(point);alias={k:v for k,v in description.items() if k!='point'}
        if key not in self.candidates:self.candidates[key]=dict(case=description['case'],point_id=key,point=dict(point),aliases=[])
        self.candidates[key]['aliases'].append(alias)
        self.roles.append(dict(alias,point_id=key))
        return self.evaluate(point)
    def choose(self,rows,branch,source,scenario):
        candidates=[r for r in rows if r['point'][P+'source_basis__q_source_MW']==source]
        eligible=[r for r in candidates if self.evaluate(r['point'])['eligible'][branch]]
        if eligible:
            selected=min(eligible,key=lambda r:(self.value(self.evaluate(r['point']),branch),r['case']))
            return dict(selected,anchor_supported=True,selection='minimum independent whole-plant LCOE among admitted finite offers')
        finite=[r for r in candidates if self.evaluate(r['point'])['status']=='evaluated']
        if not finite:raise ValueError(f'no finite {branch} anchor at source{source} scenario{scenario}')
        selected=min(finite,key=lambda r:(len(self.evaluate(r['point'])['failed'][branch]),r['case']))
        return dict(selected,anchor_supported=False,selection='diagnostic fallback with fewest failed applicable predicates; no rankable anchor')
    def catalog(self,base,scenario,source_values=(2500.,2800.,3000.)):
        gas=[r for r in offers.gas_catalog(base) if r['point'][P+'source_basis__q_source_MW'] in source_values]
        # First locate a gas anchor using only shared and gas predicates.
        ga={q:self.choose(gas,'gas',q,scenario) for q in source_values}
        steam=[r for q in source_values for r in offers.steam_catalog(ga[q]['point'])]
        sa={q:self.choose(steam,'steam',q,scenario) for q in source_values}
        # Pair every gas offer with the selected steam hardware at the same source.
        paired=[]
        for r in gas:
            q=r['point'][P+'source_basis__q_source_MW'];choice={k:sa[q]['point'][P+k] for k in STEAM_HARDWARE}
            paired.append(dict(r,point=offers.change(r['point'],choice),paired_steam_anchor=sa[q]['case']))
        rows=[]
        for branch,group in [('gas',paired),('steam',steam)]:
            for r in group:
                row=dict(r,case=scenario+'::'+r['case'],scenario=scenario,branch=branch,
                         source_MW=r['point'][P+'source_basis__q_source_MW'],family='nominal_catalog' if scenario=='nominal' else 'joint_efficiency',range_authority='engineered finite catalog')
                self.add(row);rows.append(row)
        anchors={}
        for q in source_values:
            selected_gas=self.choose([r for r in rows if r['branch']=='gas'],'gas',q,scenario)
            selected_steam=self.choose([r for r in rows if r['branch']=='steam'],'steam',q,scenario)
            complete=offers.change(selected_gas['point'],{k:selected_steam['point'][P+k] for k in STEAM_HARDWARE})
            result=self.evaluate(complete)
            anchors[str(int(q))]=dict(point=complete,point_id=digest(complete),gas_case=selected_gas['case'],steam_case=selected_steam['case'],gas_supported=result['eligible']['gas'],steam_supported=result['eligible']['steam'],gas_selection=selected_gas['selection'],steam_selection=selected_steam['selection'])
            # Each combined anchor is already the intersection of two catalog rows.
            if digest(complete) not in self.candidates:raise ValueError('paired anchor escaped the declared catalog')
        return rows,anchors
    def scenario_rows(self,nominal,base,common_cases):
        for scenario in common_cases:
            for offer in nominal:
                if offer['source_MW'] not in (2500.,2800.) or not self.evaluate(offer['point'])['eligible'][offer['branch']]:continue
                point=offers.change(offer['point'],scenario['choices'])
                self.add(dict(case=scenario['scenario']+'::'+offer['case'],scenario=scenario['scenario'],family=scenario['family'],branch=offer['branch'],source_MW=offer['source_MW'],role='rerank_nominal_supported_catalog',nominal_offer=offer['case'],chosen=scenario['choices'],range_authority=scenario['range_authority'],point=point))
        # Audit excluded offers conservatively. One unchanged violated predicate
        # is sufficient to prove exclusion remains. Otherwise evaluate the point.
        for scenario in common_cases:
            for offer in nominal:
                branch=offer['branch'];initial=self.evaluate(offer['point'])
                if offer['source_MW'] not in (2500.,2800.) or initial['eligible'][branch]:continue
                changed={P+k for k,value in scenario['choices'].items() if offer['point'][P+k]!=value}
                fixed=[cid for cid in initial['failed'][branch] if not changed.intersection(self.dependencies[cid])]
                audit=dict(scenario=scenario['scenario'],nominal_offer=offer['case'],branch=branch,source_MW=offer['source_MW'],changed_inputs=sorted(changed),nominal_failed_predicates=initial['failed'][branch])
                if fixed:
                    audit.update(disposition='excluded_by_invariant_failed_predicate',invariant_failed_predicates=fixed)
                else:
                    point=offers.change(offer['point'],scenario['choices']);result=self.evaluate(point)
                    audit.update(disposition='newly_admitted' if result['eligible'][branch] else 'still_excluded_after_oracle_evaluation',point_id=result['point_id'],oracle_status=result['status'],failed_predicates=result['failed'][branch])
                    if result['eligible'][branch]:
                        self.add(dict(case=scenario['scenario']+'::'+offer['case'],scenario=scenario['scenario'],family=scenario['family'],branch=branch,source_MW=offer['source_MW'],role='newly_admitted_scenario_offer',nominal_offer=offer['case'],chosen=scenario['choices'],range_authority=scenario['range_authority'],point=point))
                self.admission_audit.append(audit)
        # All eight quote/service scenarios are applied relative to each offer's
        # own quote; using one anchor's prices would erase selected offer factors.
        for offer in nominal:
            if offer['source_MW'] not in (2500.,2800.) or not self.evaluate(offer['point'])['eligible'][offer['branch']]:continue
            rows=[r for r in offers.sensitivity_catalog(offer['point']) if '-quote-' in r['case'] or '-recurring-' in r['case']]
            if len(rows)!=8:raise ValueError('expected eight price/service scenarios')
            for row in rows:
                name=row['case'].split(f"sensitivity-q{offer['source_MW']:g}-",1)[1]
                self.add(dict(row,case=name+'::'+offer['case'],scenario=name,family='conversion_price_service',branch=offer['branch'],source_MW=offer['source_MW'],role='rerank_nominal_supported_catalog',nominal_offer=offer['case'],range_authority='engineered multipliers, not confidence intervals'))
    def held_diagnostics(self,anchors):
        for q in ('2500','2800'):
            anchor=anchors[q]
            if not (anchor['gas_supported'] and anchor['steam_supported']):raise ValueError('held diagnostics require a supported paired anchor')
            for row in offers.sensitivity_catalog(anchor['point']):
                if '-eta' not in row['case'] or '-both-' in row['case']:continue
                branch='gas' if '-gas-' in row['case'] else 'steam'
                self.add(dict(row,case='held::'+row['case'],scenario='held_efficiency',family='held_efficiency',branch=branch,source_MW=float(q),role='held_offer_response_no_optimized_claim',anchor=anchor['point_id']))
            for row in offers.adverse_controller_catalog(anchor['point']):
                branch='gas' if '-gas-' in row['case'] else 'steam'
                self.add(dict(row,case='adverse::'+row['case'],scenario='adverse_controller',family='adverse_controller',branch=branch,source_MW=float(q),role='adverse_selected_offer',anchor=anchor['point_id']))
    def edge_scan(self,anchors):
        edges=[]
        for q in ('2500','2800'):
            anchor=anchors[q]
            for branch in ('gas','steam'):
                if not anchor[branch+'_supported']:raise ValueError('window edge reread requires a new passing branch anchor')
                if branch=='gas':
                    axes=[('flow',{'cycle__selected_flow':offers.GAS_FLOWS[0]},{'cycle__selected_flow':offers.GAS_FLOWS[-1]}),
                          ('stage_ratio',{f'compressor_{i}__selected_ratio':offers.STAGE_RATIOS[0] for i in (1,2,3)},{f'compressor_{i}__selected_ratio':offers.STAGE_RATIOS[-1] for i in (1,2,3)})]
                    def service(index):
                        offer=offers.SERVICE_OFFERS[index]
                        return {'recuperator_hardware__ua':offer['recuperator_ua'],'conversion_services__price_factor':offer['quote_factor'],**{owner+'__ua':ua for owner,ua in zip(('water_ic1','water_ic2','water_pre'),offer['ua'])}}
                    axes.append(('service_offer',service(0),service(-1)))
                else:
                    axes=[('circuits',{'steam_transport__n_loops':10.},{'steam_transport__n_loops':14.}),('pumps_per_circuit',{'steam_transport__salt_pumps_per_circuit':2.},{'steam_transport__salt_pumps_per_circuit':4.}),('pump_design_flow',{'steam_transport__selected_salt_design_flow_kg_s':225.},{'steam_transport__selected_salt_design_flow_kg_s':250.})]
                axes.append(('source',{'source_basis__q_source_MW':2500.},{'source_basis__q_source_MW':3000.}))
                for axis,lower,upper in axes:
                    for end,chosen in [('lower',lower),('upper',upper)]:
                        point=offers.change(anchor['point'],chosen);name=f'edge-q{q}-{branch}-{axis}-{end}'
                        result=self.add(dict(case=name,scenario='window_edges',family='window_edges',branch=branch,source_MW=point[P+'source_basis__q_source_MW'],role='held_anchor_edge_reread',chosen=chosen,anchor=anchor['point_id'],point=point))
                        edges.append(dict(case=name,branch=branch,axis=axis,end=end,chosen=chosen,anchor_source_MW=float(q),anchor=anchor['point_id'],anchor_supported=True,point_id=result['point_id'],status='caught' if not result['eligible'][branch] else 'not_caught',failed_predicates=result['failed'][branch],oracle_status=result['status']))
        return edges

def validate_release(integration_path):
    loaded=manifest.load(study_route.MANIFEST_PATH);interface=study_route.interface()
    expected={k:interface[k] for k in ('executable_fingerprint','semantic_fingerprint')}
    expected['pin']=loaded.pinned_digest
    if integration_path.suffix=='.md':
        review=integration_path.read_text()
        if 'Verdict: pass' not in review or any(interface[k] not in review for k in ('executable_fingerprint','semantic_fingerprint')):raise ValueError('exact independent integration review PASS required')
        integration=dict(kind='oracle preparation release only; native CANDIDATE still required for execution',review=str(integration_path),review_sha256=hashlib.sha256(integration_path.read_bytes()).hexdigest(),candidate=expected)
    else:
        integration=common.read_json(integration_path,'native integration return')
        if integration.get('class')!='CANDIDATE' or integration.get('exit_code')!=0:raise ValueError('released native integration CANDIDATE required')
        for key,wanted in expected.items():
            if integration['candidate'].get(key)!=wanted:raise ValueError('integration identity mismatch '+key)
    common.assert_tree_clean(study_route.PACKAGE_DIR)
    manifest.assert_pin_matches(loaded,manifest.indicator_input_fingerprint(study_route.PACKAGE_DIR))
    return integration,loaded

def run(integration_path,out,base_receipt):
    integration,loaded=validate_release(integration_path)
    if out.exists():raise ValueError('scan evidence exists; choose a new output directory')
    doc=common.read_json(base_receipt,'final native development baseline')
    matches=[r for r in doc['cases'] if r['case']=='whole-baseline2500']
    if len(matches)!=1 or matches[0]['state']!='completed':raise ValueError('supported complete baseline missing')
    receipt=matches[0];base={k:float(v) for k,v in receipt['inputs'].items()}
    if len(base)!=637 or set(base)!=set(verify.defaults()):raise ValueError('review changed complete input surface')
    if receipt['executable_fingerprint']!=integration['candidate']['executable_fingerprint']:raise ValueError('baseline identity mismatch')
    out.mkdir(parents=True);scan=Scanner(base)
    if not all(scan.evaluate(base)['eligible'].values()):raise ValueError('native baseline is not supported by independent predicates')
    nominal,anchors=scan.catalog(base,'nominal')
    if Counter(r['branch'] for r in nominal)!=dict(gas=375,steam=72):raise ValueError('nominal catalog count changed')
    common_cases=list(scenarios.common_scenarios(base))
    if len(common_cases)!=44:raise ValueError('review changed common scenario count')
    scan.scenario_rows(nominal,base,common_cases)
    performance={}
    for scenario in scenarios.joint_efficiency_scenarios(base):
        rows,a=scan.catalog(offers.change(base,scenario['choices']),scenario['scenario'],(2500.,2800.));performance[scenario['scenario']]=a
    scan.held_diagnostics(anchors);edges=scan.edge_scan(anchors)
    candidates=list(scan.candidates.values());refusals=[r for r in scan.cache.values() if r['status']=='oracle_refusal']
    scenario_summary={}
    for role in scan.roles:
        branch=role['branch'];group=(role['scenario'],role['source_MW'],branch)
        key='::'.join(map(str,group));result=scan.cache[role['point_id']]
        summary=scenario_summary.setdefault(key,dict(scenario=group[0],source_MW=group[1],branch=branch,attempted_aliases=0,eligible_aliases=0,best=None))
        summary['attempted_aliases']+=1
        if result['eligible'][branch]:
            summary['eligible_aliases']+=1;value=scan.value(result,branch)
            if summary['best'] is None or value<summary['best']['oracle_lcoe_USD2025_MWh']:summary['best']=dict(case=role['case'],point_id=role['point_id'],oracle_lcoe_USD2025_MWh=value,interpretation='planning selection; native ranking required')
    unique=len(candidates);summary=dict(kind='independent oracle planning scan; no native ranking',status='requires_refusal_review' if refusals else 'budget_exceeded' if unique>3000 else 'threshold_reserve_shortfall' if unique>2900 else 'ready_for_review',unique_complete_points=unique,alias_count=len(scan.roles),duplicate_aliases=len(scan.roles)-unique,reserved_threshold_points=min(100,max(3000-unique,0)),remaining_total_budget=max(3000-unique,0),nominal_catalog=dict(gas=375,steam=72),common_scenarios=44,price_service_scenarios=8,joint_efficiency_scenarios=2,oracle_evaluations=len(scan.cache),oracle_refusals=len(refusals),admission_audit=dict(Counter(r['disposition'] for r in scan.admission_audit)),predicate_membership=dict(Counter(r['branch'] for r in scan.predicates.values())),native_required=True)
    dump(out/'baseline.json',dict(source_receipt=str(base_receipt),sha256=hashlib.sha256(base_receipt.read_bytes()).hexdigest(),point=base,integration_candidate=integration['candidate']))
    dump(out/'predicate-catalog.json',scan.predicates)
    dump(out/'predicate-input-dependencies.json',dict(method='each calculation output conservatively inherits every input dependency',predicates=scan.dependencies))
    dump(out/'admission-audit.json',dict(method='one unchanged failed applicable predicate proves exclusion; otherwise evaluate changed point and add every newly admitted offer',summary=dict(Counter(r['disposition'] for r in scan.admission_audit)),cases=scan.admission_audit))
    dump(out/'proposed-points.json',dict(cases=candidates,summary=summary))
    dump(out/'case-membership.json',dict(cases=scan.roles))
    dump(out/'oracle-scan.json',dict(baseline='baseline.json',point_reconstruction='baseline.point updated by input_delta; SHA256 of canonical complete point is point_id',cases=list(scan.cache.values())))
    dump(out/'anchors.json',dict(nominal=anchors,joint_efficiency=performance))
    dump(out/'scenario-scan.json',dict(scenarios=common_cases,results=list(scenario_summary.values())))
    dump(out/'window.json',dict(provenance='engineered',selection='retained finite hardware catalog re-read from newly passing whole-plant anchors',edges=edges,source3000='shared source failures retained; no passing anchor at3000 claimed',bound_claim='A not_caught endpoint is an open edge of this finite catalog, not a continuous feasible bound or global optimum. No automatic extension or equipment sizing.'))
    dump(out/'summary.json',summary)
    common.assert_tree_clean(study_route.PACKAGE_DIR)
    print(json.dumps(summary,indent=2))
    if summary['status']!='ready_for_review':raise ValueError('scan requires coordinator disposition; no range reduction performed')
    return summary

def extend(integration_path,out):
    """Add declared interactions and native-confirmable engineering brackets."""
    validate_release(integration_path)
    if (out/'extension-plan.json').exists():raise ValueError('extension evidence already exists')
    base=json.loads((out/'baseline.json').read_text())['point'];scan=Scanner(base)
    scan.cache={r['point_id']:r for r in json.loads((out/'oracle-scan.json').read_text())['cases']}
    scan.candidates={r['point_id']:r for r in json.loads((out/'proposed-points.json').read_text())['cases']}
    scan.roles=json.loads((out/'case-membership.json').read_text())['cases']
    previous=json.loads((out/'summary.json').read_text());initial_roles=list(scan.roles)
    anchors=json.loads((out/'anchors.json').read_text())['nominal']
    extensions=[];crossings=[]
    for performance,gf,sf in [('gas-favourable',.5,1.5),('steam-favourable',1.5,.5)]:
        name=performance+'-gas-quote-x'+str(gf)+'-steam-x'+str(sf)
        admitted=[r for r in initial_roles if r['scenario']==performance and scan.cache[r['point_id']]['eligible'][r['branch']]]
        # Positive quote multipliers cannot repair a physical predicate failure.
        # Both performance catalogs were evaluated in full before this filter.
        for role in admitted:
            point=scan.candidates[role['point_id']]['point']
            chosen={k:point[P+k]*gf for k in offers.GAS_QUOTE_KEYS}
            chosen.update({k:point[P+k]*sf for k in offers.STEAM_QUOTE_KEYS})
            scan.add(dict(case=name+'::'+role['case'],scenario=name,family='joint_performance_price',branch=role['branch'],source_MW=role['source_MW'],role='rerank_performance_supported_catalog',performance_offer=role['case'],chosen=chosen,range_authority='engineered positive quote multipliers and efficiency assumptions',point=offers.change(point,chosen)))
        extensions.append(dict(scenario=name,performance=performance,gas_quote_factor=gf,steam_quote_factor=sf,admitted_aliases=len(admitted),eligibility_basis='full performance catalog; positive price changes preserve physical eligibility'))
        for q in (2500.,2800.):
            group=[r for r in admitted if r['source_MW']==q]
            def prices(t):
                rows=[]
                for role in group:
                    point=scan.candidates[role['point_id']]['point']
                    chosen={k:point[P+k]*(1+t*(gf-1)) for k in offers.GAS_QUOTE_KEYS}
                    chosen.update({k:point[P+k]*(1+t*(sf-1)) for k in offers.STEAM_QUOTE_KEYS})
                    rows.append((role,chosen,offers.change(point,chosen)))
                return rows
            def gap(t):
                best={b:math.inf for b in ('gas','steam')}
                for role,_,point in prices(t):
                    row=scan.evaluate(point);branch=role['branch']
                    if row['eligible'][branch]:best[branch]=min(best[branch],scan.value(row,branch))
                return best['gas']-best['steam'],best
            low,lowbest=gap(0.);high,highbest=gap(1.)
            record=dict(performance=performance,source_MW=q,path='gas quote factor 1+t*(gas_endpoint-1); steam quote factor 1+t*(steam_endpoint-1)',gas_endpoint=gf,steam_endpoint=sf,t_domain=[0.,1.],endpoint_gaps=[low,high],endpoint_best=[lowbest,highbest],interpretation='finite catalog reranking at fixed performance; native confirmation required')
            if low*high<0:
                left,right=0.,1.
                for _ in range(20):
                    mid=(left+right)/2;middle,_=gap(mid)
                    if low*middle>0:left=mid
                    else:right=mid
                center=(left+right)/2;bracket=[max(0.,center-1e-5),min(1.,center+1e-5)]
                record.update(disposition='crossing bracket proposed',oracle_bracket_t=bracket,bracket_results=[])
                for end,t in zip(('lower','upper'),bracket):
                    scenario=f'economic-bracket-{performance}-q{q:g}-{end}'
                    delta,best=gap(t);record['bracket_results'].append(dict(t=t,gap=delta,best=best,scenario=scenario))
                    for role,chosen,point in prices(t):
                        scan.add(dict(case=scenario+'::'+role['case'],scenario=scenario,family='economic_boundary',branch=role['branch'],source_MW=q,role='rerank_performance_supported_catalog_at_price_bracket',performance_offer=role['case'],chosen=chosen,path_t=t,range_authority='bracket within declared positive quote endpoints',point=point))
            else:record['disposition']='no crossing in declared positive quote path'
            crossings.append(record)
    cryo=[]
    for q in ('2500','2800'):
        anchor=anchors[q];capacity=scan.cache[anchor['point_id']]['outputs'][P+'cryogenic_demand__evaluate__q_nuc_capacity_W_m3']
        for end,offset in [('below',-.01),('above',.01)]:
            chosen={'cryogenic_demand__q_nuc_W_m3':capacity+offset,'cryogenic_demand__extra_cold_W':0.}
            point=offers.change(anchor['point'],chosen);result=scan.evaluate(point)
            for branch in ('gas','steam'):
                scan.add(dict(case=f'cryo-capacity-q{q}-{end}-{branch}',scenario='cryogenic_capacity_'+end,family='cryogenic_boundary',branch=branch,source_MW=float(q),role='engineering_boundary_diagnostic',chosen=chosen,anchor=anchor['point_id'],range_authority='independent capacity threshold bracket; not a nuclear heat uncertainty interval',point=point))
            cryo.append(dict(source_MW=float(q),end=end,threshold_W_m3=capacity,chosen=chosen,point_id=result['point_id'],failed=result['failed']))
    summary=dict(previous);unique=len(scan.candidates);refusals=[r for r in scan.cache.values() if r['status']=='oracle_refusal']
    summary.update(status='requires_refusal_review' if refusals else 'budget_exceeded' if unique>3000 else 'ready_for_review',unique_complete_points=unique,alias_count=len(scan.roles),duplicate_aliases=len(scan.roles)-unique,remaining_total_budget=max(3000-unique,0),reserved_threshold_points=min(100,max(3000-unique,0)),oracle_evaluations=len(scan.cache),oracle_refusals=len(refusals),joint_performance_price_scenarios=2,cryogenic_bracket_points=4,economic_crossing_brackets=sum(r['disposition']=='crossing bracket proposed' for r in crossings))
    results={}
    for role in scan.roles:
        key=(role['scenario'],role['source_MW'],role['branch']);row=scan.cache[role['point_id']];branch=role['branch']
        entry=results.setdefault(key,dict(scenario=key[0],source_MW=key[1],branch=branch,attempted_aliases=0,eligible_aliases=0,best=None));entry['attempted_aliases']+=1
        if row['eligible'][branch]:
            entry['eligible_aliases']+=1;value=scan.value(row,branch)
            if entry['best'] is None or value<entry['best']['oracle_lcoe_USD2025_MWh']:entry['best']=dict(case=role['case'],point_id=role['point_id'],oracle_lcoe_USD2025_MWh=value,interpretation='planning selection; native ranking required')
    scenario_doc=json.loads((out/'scenario-scan.json').read_text());scenario_doc['results']=list(results.values());scenario_doc['extensions']=extensions
    dump(out/'summary-before-extension.json',previous)
    dump(out/'extension-plan.json',dict(interactions=extensions,economic_crossings=crossings,cryogenic_brackets=cryo,added_unique_points=unique-previous['unique_complete_points']))
    dump(out/'proposed-points.json',dict(cases=list(scan.candidates.values()),summary=summary));dump(out/'case-membership.json',dict(cases=scan.roles))
    dump(out/'oracle-scan.json',dict(baseline='baseline.json',point_reconstruction='baseline.point updated by input_delta; SHA256 of canonical complete point is point_id',cases=list(scan.cache.values())))
    dump(out/'scenario-scan.json',scenario_doc);dump(out/'summary.json',summary)
    common.assert_tree_clean(study_route.PACKAGE_DIR);print(json.dumps(summary,indent=2))
    if summary['status']!='ready_for_review':raise ValueError('extension requires coordinator disposition; no range reduction performed')
    return summary

def audit_interactions(integration_path,out):
    validate_release(integration_path)
    base=json.loads((out/'baseline.json').read_text())['point'];scan=Scanner(base)
    scan.cache={r['point_id']:r for r in json.loads((out/'oracle-scan.json').read_text())['cases']}
    candidates={r['point_id']:r for r in json.loads((out/'proposed-points.json').read_text())['cases']}
    roles=json.loads((out/'case-membership.json').read_text())['cases'];audit=[]
    for role in roles:
        performance=role['scenario']
        if performance not in ('gas-favourable','steam-favourable'):continue
        initial=scan.cache[role['point_id']];branch=role['branch']
        if initial['eligible'][branch]:continue
        point=candidates[role['point_id']]['point'];gf,sf=(.5,1.5) if performance=='gas-favourable' else (1.5,.5)
        chosen={k:point[P+k]*gf for k in offers.GAS_QUOTE_KEYS};chosen.update({k:point[P+k]*sf for k in offers.STEAM_QUOTE_KEYS})
        changed={P+k for k,v in chosen.items() if point[P+k]!=v};fixed=[cid for cid in initial['failed'][branch] if not changed.intersection(scan.dependencies[cid])]
        entry=dict(performance=performance,case=role['case'],branch=branch,source_MW=role['source_MW'],changed_inputs=sorted(changed),nominal_failed_predicates=initial['failed'][branch])
        if fixed:entry.update(disposition='excluded_by_invariant_failed_predicate',invariant_failed_predicates=fixed)
        else:
            result=scan.evaluate(offers.change(point,chosen));entry.update(disposition='newly_admitted' if result['eligible'][branch] else 'still_excluded_after_oracle_evaluation',point_id=result['point_id'],oracle_status=result['status'],failed_predicates=result['failed'][branch])
        audit.append(entry)
    census=dict(Counter(r['disposition'] for r in audit))
    dump(out/'interaction-admission-audit.json',dict(method='conservative input dependency proof or explicit oracle evaluation at opposing quote endpoints; the only varied inputs inside crossing paths are positive equipment quote scalars, whose account arithmetic does not alter physical outputs',summary=census,cases=audit))
    dump(out/'oracle-scan.json',dict(baseline='baseline.json',point_reconstruction='baseline.point updated by input_delta; SHA256 of canonical complete point is point_id',cases=list(scan.cache.values())))
    summary=json.loads((out/'summary.json').read_text());summary.update(oracle_evaluations=len(scan.cache),interaction_admission_audit=census,oracle_refusals=sum(r['status']=='oracle_refusal' for r in scan.cache.values()))
    if census.get('newly_admitted') or summary['oracle_refusals']:summary['status']='requires_interaction_admission_review'
    dump(out/'summary.json',summary);proposed=json.loads((out/'proposed-points.json').read_text());proposed['summary']=summary;dump(out/'proposed-points.json',proposed)
    common.assert_tree_clean(study_route.PACKAGE_DIR);print(json.dumps(summary,indent=2))
    if summary['status']!='ready_for_review':raise ValueError('interaction admission requires coordinator review')
    return summary

def reporting_band(integration_path,out):
    validate_release(integration_path)
    if (out/'reporting-band-plan.json').exists():raise ValueError('reporting band evidence already exists')
    base=json.loads((out/'baseline.json').read_text())['point'];scan=Scanner(base)
    scan.cache={r['point_id']:r for r in json.loads((out/'oracle-scan.json').read_text())['cases']}
    scan.candidates={r['point_id']:r for r in json.loads((out/'proposed-points.json').read_text())['cases']}
    scan.roles=json.loads((out/'case-membership.json').read_text())['cases']
    group=[r for r in scan.roles if r['scenario']=='gas-favourable' and r['source_MW']==2800. and scan.cache[r['point_id']]['eligible'][r['branch']]]
    def rows(t):
        for role in group:
            point=scan.candidates[role['point_id']]['point'];chosen={k:point[P+k]*(1-.5*t) for k in offers.GAS_QUOTE_KEYS};chosen.update({k:point[P+k]*(1+.5*t) for k in offers.STEAM_QUOTE_KEYS})
            yield role,chosen,offers.change(point,chosen)
    def gap(t):
        best={b:math.inf for b in ('gas','steam')}
        for role,_,point in rows(t):
            result=scan.evaluate(point);branch=role['branch']
            if result['eligible'][branch]:best[branch]=min(best[branch],scan.value(result,branch))
        return best['gas']-best['steam'],best
    low,_=gap(0.);high,_=gap(1.);brackets=[]
    for target in (5.,-5.):
        if not high<target<low:raise ValueError('materiality threshold is outside declared path')
        # Try the endpoint secant, then verify it with full oracle reranking.
        center=(low-target)/(low-high);ends=[center-1e-5,center+1e-5]
        if not gap(ends[0])[0]>target>gap(ends[1])[0]:
            left,right=0.,1.
            for _ in range(20):
                mid=(left+right)/2
                if gap(mid)[0]>target:left=mid
                else:right=mid
            center=(left+right)/2;ends=[center-1e-5,center+1e-5]
        record=dict(target_gap_USD2025_MWh=target,source_MW=2800.,performance='gas-favourable',path='gas factor=1-0.5t; steam factor=1+0.5t',bracket=[])
        for end,t in zip(('lower','upper'),ends):
            if not 0<t<1:raise ValueError('bracket escaped positive quote endpoint window')
            scenario=f'reporting-band-gap{target:+g}-q2800-{end}';delta,best=gap(t)
            record['bracket'].append(dict(scenario=scenario,t=t,gap_USD2025_MWh=delta,best=best))
            for role,chosen,point in rows(t):
                scan.add(dict(case=scenario+'::'+role['case'],scenario=scenario,family='reporting_boundary',branch=role['branch'],source_MW=2800.,role='rerank_performance_supported_catalog_at_reporting_band',performance_offer=role['case'],chosen=chosen,path_t=t,target_gap_USD2025_MWh=target,range_authority='five USD2025/MWh comparison materiality band; not a physical constraint',point=point))
        if not record['bracket'][0]['gap_USD2025_MWh']>target>record['bracket'][1]['gap_USD2025_MWh']:raise ValueError('reporting threshold bracket did not straddle target')
        brackets.append(record)
    summary=json.loads((out/'summary.json').read_text());unique=len(scan.candidates)
    summary.update(unique_complete_points=unique,alias_count=len(scan.roles),duplicate_aliases=len(scan.roles)-unique,remaining_total_budget=3000-unique,oracle_evaluations=len(scan.cache),oracle_refusals=sum(r['status']=='oracle_refusal' for r in scan.cache.values()),reporting_materiality_USD2025_MWh=5.,reporting_threshold_brackets=2)
    if unique>3000 or summary['oracle_refusals']:summary['status']='requires_reporting_band_review'
    doc=json.loads((out/'scenario-scan.json').read_text());newroles=[r for r in scan.roles if r['family']=='reporting_boundary'];results={}
    for role in newroles:
        key=(role['scenario'],role['branch']);row=scan.cache[role['point_id']];branch=role['branch'];entry=results.setdefault(key,dict(scenario=key[0],source_MW=2800.,branch=branch,attempted_aliases=0,eligible_aliases=0,best=None));entry['attempted_aliases']+=1
        if row['eligible'][branch]:
            entry['eligible_aliases']+=1;value=scan.value(row,branch)
            if entry['best'] is None or value<entry['best']['oracle_lcoe_USD2025_MWh']:entry['best']=dict(case=role['case'],point_id=role['point_id'],oracle_lcoe_USD2025_MWh=value,interpretation='planning selection; native ranking required')
    doc['results'].extend(results.values());dump(out/'scenario-scan.json',doc)
    dump(out/'reporting-band-plan.json',dict(materiality_band_USD2025_MWh=5.,interpretation='strict zero crossing is algebraic; absolute gas-minus-steam gap at most five is reporting-indeterminate',brackets=brackets))
    dump(out/'oracle-scan.json',dict(baseline='baseline.json',point_reconstruction='baseline.point updated by input_delta; SHA256 of canonical complete point is point_id',cases=list(scan.cache.values())))
    dump(out/'proposed-points.json',dict(cases=list(scan.candidates.values()),summary=summary));dump(out/'case-membership.json',dict(cases=scan.roles));dump(out/'summary.json',summary)
    common.assert_tree_clean(study_route.PACKAGE_DIR);print(json.dumps(summary,indent=2))
    if summary['status']!='ready_for_review':raise ValueError('reporting band requires coordinator review')

def freeze(integration_path,out):
    integration,_=validate_release(integration_path)
    if (out/'candidate-freeze.json').exists():raise ValueError('candidate evidence is already frozen')
    summary=json.loads((out/'summary.json').read_text());base=json.loads((out/'baseline.json').read_text())['point'];proposed=json.loads((out/'proposed-points.json').read_text());members=json.loads((out/'case-membership.json').read_text())['cases']
    if summary['status']!='ready_for_review' or summary['oracle_refusals'] or summary['unique_complete_points']>3000:raise ValueError('candidate set is not ready for freeze')
    ids=set();labels=set()
    for row in proposed['cases']:
        if digest(row['point'])!=row['point_id'] or set(row['point'])!=set(base):raise ValueError('complete point identity failed')
        if row['point_id'] in ids:raise ValueError('duplicate complete point');
        ids.add(row['point_id'])
        for alias in row['aliases']:
            if alias['case'] in labels:raise ValueError('duplicate alias label')
            labels.add(alias['case'])
    if len(ids)!=summary['unique_complete_points'] or len(labels)!=summary['alias_count'] or len(members)!=len(labels):raise ValueError('candidate census mismatch')
    window=json.loads((out/'window.json').read_text());extension=json.loads((out/'extension-plan.json').read_text());band=json.loads((out/'reporting-band-plan.json').read_text())
    price_rows=[r for r in offers.sensitivity_catalog(base) if '-quote-' in r['case'] or '-recurring-' in r['case']]
    window['declared_finite_window']=dict(source_MW=list(offers.SOURCE_MW),supported_scenario_sources_MW=[2500.,2800.],gas=dict(flow_kg_s=list(offers.GAS_FLOWS),coordinated_stage_pressure_ratios=list(offers.STAGE_RATIOS),service_offers=list(offers.SERVICE_OFFERS)),steam=dict(circuits=[10,11,12,14],pumps_per_circuit=[2,3,4],pump_design_flow_kg_s=[225,250]),common_scenarios=list(scenarios.common_scenarios(base)),price_service_scenarios=[dict(case=r['case'],baseline_choices=r['chosen']) for r in price_rows],price_application='each multiplier applies to that offer own selected quote; baseline choices above identify inputs, all exact per-offer values are in proposed-points aliases and complete points',joint_efficiency_scenarios=list(scenarios.joint_efficiency_scenarios(base)),performance_price_interactions=extension['interactions'],economic_brackets=extension['economic_crossings'],cryogenic_brackets=extension['cryogenic_brackets'],reporting_materiality=band,held_efficiency_diagnostics=[dict(case=r['case'],baseline_choices=r['chosen']) for r in offers.sensitivity_catalog(base) if '-eta' in r['case'] and '-both-' not in r['case']],adverse_controllers=[dict(case=r['case'],baseline_choices=r['chosen']) for r in offers.adverse_controller_catalog(base)])
    window.update(candidate_count=len(ids),alias_count=len(labels),native_evaluation_budget=3000,remaining_budget=3000-len(ids),admission_evidence=['admission-audit.json','interaction-admission-audit.json'],comparison_band_USD2025_MWh=5.,comparison_band_kind='reporting materiality, not a physical constraint',exact_points='proposed-points.json',scope='conditional supplied-source and supplied-demand economics within finite hardware offers; source/plasma and nuclear transport qualification remain zero')
    dump(out/'window.json',window)
    (out/'README.md').write_text('# Independent study preparation\n\n[AGENT] This frozen preparation proposes '+str(len(ids))+' unique complete native evaluations with '+str(len(labels))+' descriptive aliases. Every point has all 637 public inputs. The independent oracle selected candidates and tested admission; final rankings require the retained native responses.\n\nThe finite catalog contains 375 gas offers and 72 steam connector offers across 2,500, 2,800, and 3,000 MW. Scenario reranking uses the supported 2,500 and 2,800 MW sources. Branch eligibility requires the 23 shared predicates plus the branch predicates (43 gas or 59 steam), and finite positive whole-plant LCOE. An unrelated alternative failure does not exclude the tested branch.\n\nThe common-scenario admission audit proves unchanged failure for 11,735 excluded pairs and evaluates another 189, with no newly admitted offers. The interaction audit proves unchanged failure for 467 pairs and evaluates another 67, with no newly admitted offers. Both opposing efficiency cases rescan the full catalogs.\n\nThe new-anchor edge reread has 18 caught and 14 uncaught endpoints. Uncaught endpoints remain explicit edges of an engineered finite catalog; they establish no continuous feasibility boundary or global optimum. Exact inputs, sources, scenario choices, edge predicates, and brackets are in window.json.\n\nThe economic threshold path at 2,800 MW holds the gas-favourable efficiency assumptions fixed while moving gas quote multipliers from 1 to 0.5 and steam quote multipliers from 1 to 1.5. Every algebraic-zero and reporting-band bracket reranks every admitted offer from that performance catalog. A gap within 5 USD2025/MWh is reporting-indeterminate. Cryogenic brackets test the selected cold-capacity boundary with unchanged hardware and zero extra structural heat; they do not define a nuclear heat uncertainty interval.\n\nThe sibling preparation-attempt-01-invalid directory retains the mechanically invalid first attempt, which overlapped package regeneration. It has no physical or ranking authority. This preparation used the stable integration CANDIDATE.\n\nThe native executor joins proposed-points.cases.case to point_id, then joins every case-membership alias by point_id. Predicate ownership is in predicate-catalog.json. Source, plasma, and nuclear transport qualification remain outside these conditional accounting claims.\n')
    artifact_hashes={str(path.relative_to(out)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(out.iterdir()) if path.is_file()}
    code=[Path(__file__),Path(offers.__file__),Path(scenarios.__file__),Path(verify.__file__),*sorted(Path(verify.__file__).parent.glob('oracle_*.py'))]
    code_hashes={str(path.relative_to(Path.cwd()) if path.is_absolute() else path):hashlib.sha256(path.read_bytes()).hexdigest() for path in code}
    result=dict(status='frozen independent preparation; native confirmation required',integration_candidate=integration['candidate'],unique_complete_points=len(ids),alias_count=len(labels),native_evaluation_budget=3000,artifact_sha256=artifact_hashes,code_sha256=code_hashes)
    dump(out/'candidate-freeze.json',result);common.assert_tree_clean(study_route.PACKAGE_DIR);print(json.dumps({k:v for k,v in result.items() if k not in ('artifact_sha256','code_sha256')},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--release',type=Path,required=True,help='exact integration review PASS or native integration CANDIDATE return');p.add_argument('--out',type=Path,required=True);p.add_argument('--extend',action='store_true');p.add_argument('--audit-interactions',action='store_true');p.add_argument('--reporting-band',action='store_true');p.add_argument('--freeze',action='store_true');p.add_argument('--baseline-receipt',type=Path,default=Path('work/active/WI-098_whole-plant-conversion-comparison/evidence/development-final/native/cases.json'));a=p.parse_args();freeze(a.release,a.out) if a.freeze else reporting_band(a.release,a.out) if a.reporting_band else audit_interactions(a.release,a.out) if a.audit_interactions else extend(a.release,a.out) if a.extend else run(a.release,a.out,a.baseline_receipt)
