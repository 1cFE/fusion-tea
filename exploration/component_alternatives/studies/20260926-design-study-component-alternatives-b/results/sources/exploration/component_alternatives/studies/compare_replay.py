"""Compare preserved and repaired native evidence without calculating plant physics."""
import argparse
import hashlib
import json
from pathlib import Path


def compare(old, new):
    read=lambda p:json.loads(p.read_text())
    original={r['case']:r for r in read(old/'results/cases.json')['cases']}
    repaired={r['case']:r for r in read(new/'results/cases.json')['cases']}
    assert original.keys()==repaired.keys(), 'changed case catalog'
    assert read(new/'results/verification_summary.json')['outcome']=='pass'
    output=new/'results/replay-comparison.json'
    if output.exists():raise ValueError('comparison already exists')
    old_catalog=read(old/'results/constraint_catalog.json');new_catalog=read(new/'results/constraint_catalog.json')
    assert old_catalog==new_catalog,'predicate identity/meaning changed'
    old_manifest=read(old/'manifest.json');new_manifest=read(new/'manifest.json')
    assert old_manifest['absolute_tolerances']==new_manifest['absolute_tolerances']
    differences=[];changes=[];worst={}
    for name,before in original.items():
        after=repaired[name]
        assert before['inputs']==after['inputs'], f'chosen inputs changed: {name}'
        assert before['outputs'].keys()==after['outputs'].keys(), f'channels changed: {name}'
        changed=[key for key in before['outputs'] if before['outputs'][key]!=after['outputs'][key]]
        for key in changed:
            error=abs(before['outputs'][key]-after['outputs'][key])
            if error>worst.get(key,{}).get('absolute_change',-1):
                worst[key]={'case':name,'before':before['outputs'][key],'after':after['outputs'][key],'absolute_change':error}
        differences.append({'case':name,'old_candidate_id':before['candidate_id'],'new_candidate_id':after['candidate_id'],'changed_numeric_channels':len(changed)})
        if before['verdicts']!=after['verdicts']:
            changes.append({'case':name,'changes':{key:{'before':value,'after':after['verdicts'][key]} for key,value in before['verdicts'].items() if value!=after['verdicts'][key]}})
    doc={'cases':len(original),'all_inputs_identical':True,'all_output_identities_identical':True,'constraint_catalog_identical':True,'absolute_tolerances_identical':True,'relative_tolerance':1e-9,
         'old_snapshot_sha256':hashlib.sha256((old/'snapshot.json').read_bytes()).hexdigest(),
         'old_executable':sorted({r['executable_fingerprint'] for r in original.values()}),
         'new_executable':sorted({r['executable_fingerprint'] for r in repaired.values()}),
         'case_correspondence':differences,'predicate_changes':changes,'maximum_absolute_changes_by_channel':worst}
    output.write_text(json.dumps(doc,indent=2)+'\n')
    print(json.dumps({'cases':len(original),'predicate_changed_cases':len(changes),'changed_channels':len(worst),'all_inputs_identical':True}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--old',type=Path,required=True);parser.add_argument('--new',type=Path,required=True)
    args=parser.parse_args();compare(args.old,args.new)
