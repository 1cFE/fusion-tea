"""Independently check every numeric channel and strict native engineering predicate."""
import argparse
import json
import math
import sys
from pathlib import Path
from candidate_common import digest, exclusive_document


def check(root, result_path):
    root=Path(root).resolve()
    sys.path.insert(0,str(root/'exploration/stellarator_e2e/studies'))
    sys.path.insert(0,str(root))
    from exploration.stellarator_e2e.studies import oracle_entry
    from scripts.study.verify import derive_verdict, package_input_values
    result=json.loads(Path(result_path).read_text())
    if result['state']!='completed': raise ValueError('incomplete native execution')
    package=root/'exploration/stellarator_e2e/generated'
    contract=json.loads((package/'contracts/model_contract.json').read_text())
    expected=oracle_entry.evaluate(result['requested_overrides'])
    channel_types={row['channel_name']:row['python_type'] for row in contract['outputs'] if row['python_type'] in ('float','int','bool')}
    channels=set(channel_types)
    if channels!=set(expected) or channels!=set(result['outputs']):
        raise ValueError('native/independent/contract numeric inventories differ')
    discrepancies=[]
    for key,value in expected.items():
        absolute=1e-18 if '__inventory__' in key else 1e-6
        actual=result['outputs'][key]
        if isinstance(value,bool) or channel_types[key]=='bool':
            # Native transport may encode a Boolean as exactly 0/1; arithmetic tolerance
            # must never turn an invalid fractional status into independent agreement.
            agrees=(type(actual) in (bool,int,float) and actual in (0,1)
                    and type(value) in (bool,int,float) and value in (0,1) and actual==value)
        else:
            agrees=math.isclose(actual,value,rel_tol=1e-9,abs_tol=absolute)
        if not agrees:
            discrepancies.append({'channel':key,'native':result['outputs'][key],'independent':value})
    defaults=package_input_values(package);bindings=oracle_entry.operand_bindings()
    entries=contract['constraint_catalog']['concrete_entries']
    if set(result['verdicts'])!={entry['constraint_id'] for entry in entries}: raise ValueError('predicate inventory differs')
    predicate_checks=[]
    for entry in entries:
        cid=entry['constraint_id'];record={'constraint_id':cid,'native_verdict':result['verdicts'][cid]}
        for label,values in [('native_operands',result['outputs']),('independent_operands',expected)]:
            satisfied,_=derive_verdict(cid,entry,bindings,result['requested_overrides'],defaults,values)
            record[label]='satisfied' if satisfied else 'violated'
        record['passed']=record['native_verdict']==record['native_operands']==record['independent_operands']
        predicate_checks.append(record)
    return {'status':'pass' if not discrepancies and all(row['passed'] for row in predicate_checks) else 'fail',
            'result_sha256':digest(result_path),'numeric_channels':len(channels),'numeric_discrepancies':discrepancies,
            'predicate_checks':predicate_checks,'violated_constraints':[key for key,value in result['verdicts'].items() if value=='violated'],
            'meaning':'Scalar comparison tolerance is separate from exact physical predicate evaluation. Input identity and aliases receive no independent physics credit.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path.cwd())
    parser.add_argument('--native-result',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    result,ok=exclusive_document(args.out,lambda:check(args.root,args.native_result),inputs=[args.native_result])
    raise SystemExit(0 if ok and result['status']=='pass' else 1)
