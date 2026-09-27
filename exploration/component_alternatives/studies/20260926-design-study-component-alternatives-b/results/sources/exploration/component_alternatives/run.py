"""Execute the WI-096 development cases through the generated component_alternatives_tea graph.

A case overrides entry inputs by key. Each case stores its effective inputs, every output, the constraint report or the
refusal with the body's message and the module that raised it. Writes only under the evidence directory (or --root).

Run: .codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" python exploration/component_alternatives/run.py'
"""
import argparse
import json
import re
import shutil
import traceback
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'component_alternatives_tea'
EVIDENCE = ROOT / 'work/active/WI-096_matched-conversion-subsystems/evidence'
P = 'component_alternatives__plant__'
RATIO = lambda r: {P+f'compressor_{i}__selected_ratio':r for i in (1,2,3)}
SCENARIOS = {
 'baseline':{},
 'source2800-ihx10':{P+'blanket_source__q_source':2800.,P+'steam_transport__n_loops':10.},
 'source3000-ihx12':{P+'blanket_source__q_source':3000.,P+'steam_transport__n_loops':12.},
 'source3000-ihx14':{P+'blanket_source__q_source':3000.},
 'gas-low-ratio-flow':{P+'blanket_source__q_source':3000.,P+'cycle__selected_flow':1500.,**RATIO(1.2)},
 'bypass-small-offer':{P+'gas_boundary__bypass_flow_rating':500.,P+'gas_ledger__controller_capital':8e6},
 'salt-two-pumps':{P+'steam_transport__salt_pumps_per_circuit':2.},
 'salt-three-pumps':{P+'steam_transport__salt_pumps_per_circuit':3.,P+'steam_transport__selected_salt_design_flow_kg_s':300.},
 'salt225-offer':{P+'steam_transport__selected_salt_design_flow_kg_s':225.,P+'steam_transport__n_loops':10.,P+'blanket_source__q_source':2800.},
 'pre-UA40-no-root':{P+'water_pre__ua':40.},
 'pre-UA20-no-root':{P+'water_pre__ua':20.},
 'water-flow-insufficient':{P+'water_ic1__flow_rating':1000.},
 'water-power-insufficient':{P+'water_ic1__power_rating':1.},
 'water-duty-insufficient':{P+'water_ic1__duty_rating':100.},
 'recuperator-UA80':{P+'recuperator_hardware__ua':80.,P+'conversion_services__price_factor':1.5},
 'flow2250-fixed-UA':{P+'cycle__selected_flow':2250.},
 'zero-discount':{P+'steam_ledger__rate':0.,P+'gas_ledger__rate':0.},
 'water-property-refusal':{P+'water_ic1__water_inlet_C':61.},
}


def load_runtime():
    from simkit.evaluation.package_load import ProvisionalPackageLoader
    module, fingerprint = ProvisionalPackageLoader(package_dir=PACKAGE, package_name='component_alternatives_tea', link_root=HERE / 'links').load()
    return module, module.create_component_alternatives_tea_registry(), str(fingerprint)


def entry_module(pipeline):
    return next(m for m in pipeline['modules'].values() if m.get('module_type') == 'EntryPoint')


def refusing_module(text):
    found = re.findall(r'(component_alternatives__[A-Za-z0-9_]+)', text)
    return found[0] if found else None


def execute_case(name, changes, runtime, root=None):
    from simkit.core.pipeline import execute_pipeline
    module, registry, fingerprint = runtime
    folder = (root or EVIDENCE / 'native_runs') / name
    if (folder/'result.json').exists():
        number=1
        while folder.with_name(folder.name+f'.attempt{number}').exists():number+=1
        folder.rename(folder.with_name(folder.name+f'.attempt{number}'))
    folder.mkdir(parents=True, exist_ok=True)
    pipeline = yaml.safe_load((PACKAGE / 'pipelines/pipeline.yaml').read_text())
    entry = entry_module(pipeline)
    effective = {}
    for key, spec in entry['inputs'].items():
        schema, relative = spec.split(' ', 1)
        values = json.loads((PACKAGE / 'pipelines' / relative).read_text())
        for parameter in values:
            if parameter in changes:
                values[parameter] = changes[parameter]
        path = folder / (key + '.json')
        path.write_text(json.dumps(values, indent=2) + '\n')
        entry['inputs'][key] = schema + ' ' + str(path.resolve())
        effective.update(values)
    unknown = set(changes) - set(effective)
    if unknown:
        raise ValueError('unknown scenario keys: ' + repr(sorted(unknown)))
    path = folder / 'pipeline.yaml'
    path.write_text(yaml.safe_dump(pipeline, sort_keys=False))
    row = dict(case=name, changes=changes, effective_inputs=effective, fingerprint=fingerprint)
    try:
        result = execute_pipeline(path, folder / 'outputs', registry=registry, custom_schema_types=module.CUSTOM_SCHEMA_TYPES)
        row.update(status='evaluated', outputs={k: v.model_dump(mode='json') if hasattr(v, 'model_dump') else v for k, v in result.outputs.items()})
    except Exception as error:
        text = traceback.format_exc()
        row.update(status='refused', error=str(error), exception_type=type(error).__name__, refusing_module=refusing_module(text), traceback=text)
    (folder / 'result.json').write_text(json.dumps(row, indent=2) + '\n')
    shutil.rmtree(folder / 'outputs', ignore_errors=True)
    return row


if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path);parser.add_argument('--cases',nargs='*');args=parser.parse_args()
 runtime=load_runtime();summary=[]
 for name,changes in SCENARIOS.items():
  if args.cases and name not in args.cases:continue
  row=execute_case(name,changes,runtime,args.root)
  item={'case':name,'status':row['status']}
  if row['status']=='evaluated':
   results=row['outputs']['constraint_report']['results']
   item['violated']=[r['constraint_id'] for r in results if r['status']=='violated']
   item['steam_net']=row['outputs'][P+'steam_ledger__evaluate__net_electric'];item['gas_net']=row['outputs'][P+'gas_ledger__evaluate__net_electric']
  else:item['error']=row['error']
  print(json.dumps(item));summary.append(item)
 (args.root or EVIDENCE/'native_runs').joinpath('summary.json').write_text(json.dumps(summary,indent=2)+'\n')
