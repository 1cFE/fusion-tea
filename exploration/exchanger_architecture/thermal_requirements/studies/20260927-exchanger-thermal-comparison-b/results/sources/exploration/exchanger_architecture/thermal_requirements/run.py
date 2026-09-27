"""Execute canonical or development scenarios through the generated native graph."""
import traceback
import argparse
import json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
PACKAGE=HERE/'exchanger_architecture_thermal_tea'
EVIDENCE=ROOT/'work/active/WI-097_exchanger-thermal-requirements/evidence'
PREFIX='aries_integrated_plant__'
def scenarios():
    """Declared assembled controls, with complete saved inputs for replays."""
    saved=json.loads((ROOT/'exploration/exchanger_architecture/studies/20260926-design-study-exchanger-architecture/results/cases.json').read_text())['cases']
    nominal=json.loads((ROOT/'exploration/aries_integrated/studies/manifest.json').read_text())['baseline']['point']
    cases={'replay-nominal-calculated':nominal}
    selections=[('supplied-n',1835.4512830147435,1400.,0.,.85),
                ('series-leader-2300',2300.,1500.,0.,.85),('network-leader-2300',2300.,1400.,1.,.65),
                ('series-unmet-pbli',2300.,1400.,0.,.85),('network-fixed-split-failure',2300.,1400.,1.,.85),
                ('network-2600',2600.,1600.,1.,.65)]
    for label,load,flow,mode,split in selections:
        match=next(r for r in saved if all(abs(r['inputs'][key]-value)<1e-9 for key,value in {
            PREFIX+'source__reference_fusion_mw':load,PREFIX+'cycle__selected_flow':flow,
            PREFIX+'heat_exchangers__network_mode':mode,PREFIX+'heat_exchangers__pbli_split_fraction':split}.items()))
        cases['replay-'+label]=match['inputs']
    source=dict(cases['replay-supplied-n'])
    hx=PREFIX+'heat_exchangers__'
    source[hx+'control_mode']=1.
    for mode in (0.,1.):
        cases['original-controlled-'+str(int(mode))]=source|{hx+'network_mode':mode}
    for offer,areas,flow_pair in [('a',(12000.,12000.,2000.),(1360.,1310.)),('b',(18000.,18000.,2000.),(1300.,1260.))]:
        for mode,flow in enumerate(flow_pair):
            changes=source|{hx+'network_mode':float(mode),hx+'pbli_split_fraction':.75,PREFIX+'cycle__selected_flow':flow}
            for b,area in zip(('he','pbli','divertor'),areas):
                changes[PREFIX+b+'_hx__selected_area']=area
                changes[PREFIX+b+'_hx__price_factor']=50000./area
            cases['offer-'+offer+'-'+str(mode)]=changes
    base=cases['offer-b-0']
    cases['partial-transfer']=base|{PREFIX+'pbli_hx__assumed_u':500.}
    cases['source-hot-cap-failure']=base|{PREFIX+'source__reference_fusion_mw':2200.}
    cases['control-authority-failure']=base|{hx+'he_max_bypass':.01}
    cases['zero-conductance']=base|{PREFIX+'divertor_hx__selected_area':0.}
    cases['offer-b-linear-price']=base|{PREFIX+b+'_hx__price_factor':1. for b in ('he','pbli','divertor')}
    return cases


def load_runtime():
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    module,fingerprint=ProvisionalPackageLoader(package_dir=PACKAGE,package_name='exchanger_architecture_thermal_tea',link_root=Path('/tmp/wi097-native-links')).load()
    return module,module.create_exchanger_architecture_thermal_tea_registry(),str(fingerprint)


def execute_case(name, changes, runtime, root=None):
    from simkit.core.pipeline import execute_pipeline
    module,registry,fingerprint=runtime
    folder=(root or EVIDENCE/'native-runs')/name
    folder.mkdir(parents=True,exist_ok=True)
    pipeline=yaml.safe_load((PACKAGE/'pipelines/pipeline.yaml').read_text())
    effective={}
    groups={}
    for key,entry in pipeline['modules']['entry_fusion']['inputs'].items():
        schema,relative=entry.split(' ',1)
        values=json.loads((PACKAGE/'pipelines'/relative).read_text())
        for parameter in values:
            if parameter in changes:
                values[parameter]=changes[parameter]
        path=folder/(key+'.json')
        path.write_text(json.dumps(values,indent=2)+'\n')
        pipeline['modules']['entry_fusion']['inputs'][key]=schema+' '+str(path.resolve())
        effective.update(values)
        groups[key]=values
    unknown=set(changes)-set(effective)
    if unknown:
        raise ValueError('unknown scenario keys: '+repr(unknown))
    path=folder/'pipeline.yaml'
    path.write_text(yaml.safe_dump(pipeline,sort_keys=False))
    row=dict(case=name,changes=changes,effective_inputs=effective,groups=groups,fingerprint=fingerprint)
    try:
        result=execute_pipeline(path,folder/'outputs',registry=registry,custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
        row.update(status='evaluated',outputs={k:v.model_dump(mode='json') if hasattr(v,'model_dump') else v for k,v in result.outputs.items()})
    except Exception as error:
        row.update(status='refused',error=str(error),exception_type=type(error).__name__,traceback=traceback.format_exc())
    (folder/'result.json').write_text(json.dumps(row,indent=2)+'\n')
    return row


def main():
    cases=scenarios()
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=cases);args=parser.parse_args()
    runtime=load_runtime()
    rows=[]
    for name,changes in cases.items():
        if args.case and args.case!=name:continue
        row=execute_case(name,changes,runtime);rows.append(row)
        summary={'case':name,'status':row['status']}
        if row['status']=='evaluated':
            for owner,key in [('source','selected_power'),('heat_exchangers','accepted_heat'),('heat_exchangers','unmet_heat'),('plant_ledger','gross_electric'),('plant_ledger','net_electric'),('plant_ledger','plant_residual')]:
                summary[key]=row['outputs'][PREFIX+owner+'__evaluate__'+key]
        else:summary['error']=row['error']
        print(json.dumps(summary))
    (EVIDENCE/'native-controls.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
