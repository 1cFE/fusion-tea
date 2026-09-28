"""Execute canonical or development scenarios through the generated native graph."""
import traceback
import argparse
import json
from pathlib import Path
import yaml

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
PACKAGE=HERE/'aries_integrated'
EVIDENCE=ROOT/'work/active/WI-090_aries-integrated-equipment-and-costs/evidence'
PREFIX='aries_integrated_plant__'
SCENARIOS={
    'nominal-source-assumed':{},
    'nominal-calculated':{PREFIX+'source__producer_mode':1.},
    'literal-Lyon-source-input':{**{PREFIX+b+'_pump__pump_mode':1. for b in ('he','pbli','divertor')},PREFIX+'cycle__recuperator_effectiveness':.95},
    'literal-Raffray-accounting':{**{PREFIX+b+'_pump__pump_mode':1. for b in ('he','pbli','divertor')},PREFIX+'source__reference_fusion_mw':2365.,PREFIX+'deposition__heat_mode':1.,PREFIX+'cycle__recuperator_effectiveness':.95},
}


def load_runtime():
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    module,fingerprint=ProvisionalPackageLoader(package_dir=PACKAGE,package_name='aries_integrated',link_root=HERE/'links').load()
    return module,module.create_aries_integrated_registry(),str(fingerprint)


def execute_case(name, changes, runtime, root=None):
    from simkit.core.pipeline import execute_pipeline
    module,registry,fingerprint=runtime
    folder=(root or EVIDENCE/'native_runs')/name
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
    parser=argparse.ArgumentParser();parser.add_argument('--case',choices=SCENARIOS);args=parser.parse_args()
    runtime=load_runtime()
    rows=[]
    for name,changes in SCENARIOS.items():
        if args.case and args.case!=name:continue
        row=execute_case(name,changes,runtime);rows.append(row)
        summary={'case':name,'status':row['status']}
        if row['status']=='evaluated':
            for owner,key in [('source','selected_power'),('heat_exchangers','accepted_heat'),('heat_exchangers','unmet_heat'),('plant_ledger','gross_electric'),('plant_ledger','net_electric'),('plant_ledger','plant_residual')]:
                summary[key]=row['outputs'][PREFIX+owner+'__evaluate__'+key]
        else:summary['error']=row['error']
        print(json.dumps(summary))
    (EVIDENCE/'baseline-execution.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()
