"""Create an unfilled observation worksheet; reference fields remain unavailable."""
import argparse
import adapter as a
from pathlib import Path


def template(attempt):
    path=Path(attempt)
    native=a.strict((path/'result.json').read_bytes()) if a.terminal_custody(path) else {'state':'interrupted','verdicts':{},'outputs':{},'effective_inputs':{},'input_roles':{}}
    manifest=a.strict((a.HERE/'historical-manifest.json').read_bytes())
    contract=a.strict((a.PACKAGE/'contracts/model_contract.json').read_bytes())
    exported={r['id']:r for r in a.export(native,manifest,contract)['rows']}
    quantities={}
    for q in manifest['quantities']:
        value=exported[q['id']]['value']
        if type(value) is bool: value=int(value)
        model={'value':value,'unit':q['unit'],'basis':q['conversion']['basis'], 'scope':q['included_scope'],'technology':q['technology']}
        quantities[q['id']]={'model':model,'reference':{'value':None,'unit':q['unit'],'basis':'unresolved','scope':[],'technology':'unresolved'},'model_valid':exported[q['id']]['status']=='mapped','applicability_evidence':''}
    state='completed' if native['state']=='completed' else 'refused' if native['state']=='execution_refused' else 'failed'
    return {'schema_version':1,'run_kind':'conditioned','execution_status':state,'constraints':{k:v=='satisfied' for k,v in native.get('verdicts',{}).items()},'extrapolations':[],'quantities':quantities,'notes':'Unfilled post-reveal worksheet. Add source page/table, definition and correspondence evidence; do not overwrite model values.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--attempt-dir',required=True);p.add_argument('--output',required=True)
    args=p.parse_args();a.verify_identity();a.document(args.output,template(args.attempt_dir))
