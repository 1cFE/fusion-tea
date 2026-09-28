"""Inventory all disagreements after a stock verifier failure; never supplies a pass."""
import argparse
import json
from pathlib import Path
from scripts.study import common, verify
from exploration.component_alternatives.studies import oracle_entry


def diagnose(record):
    result_path = record / 'results/verification-diagnostics.json'
    if result_path.exists():
        raise ValueError('diagnostic evidence exists')
    cases = json.loads((record / 'results/cases.json').read_text())['cases']
    manifest = json.loads((record / 'manifest.json').read_text())
    catalog = json.loads((record / 'results/constraint_catalog.json').read_text())
    absolute = {r['channel']:r['value'] for r in manifest['absolute_tolerances']}
    bindings = oracle_entry.operand_bindings()
    wanted = set(verify.objective_channels(verify.manifest_mod.load(record / 'manifest.json')).values())
    wanted.update(b['key'] for table in bindings.values() for b in table.values() if b.get('kind')=='channel')
    rows=[]
    for case in cases:
        calculated=oracle_entry.evaluate(case['inputs'])
        errors=[]
        for channel in sorted(wanted):
            native=case['outputs'][channel]; independent=calculated[channel]
            relative=common.relative_deviation(native,independent); error=abs(native-independent)
            if relative>=verify.TOLERANCE and error>=absolute.get(channel,0.):
                errors.append({'channel':channel,'native':native,'oracle':independent,'relative_deviation':relative,'absolute_error':error,'absolute_limit':absolute.get(channel,0.)})
        mismatches=[]
        for cid,entry in catalog.items():
            ok,_=verify.derive_verdict(cid,entry,bindings,case['inputs'],manifest['baseline']['point'],calculated)
            expected='satisfied' if ok else 'violated'
            if case['verdicts'][cid]!=expected:mismatches.append({'constraint_id':cid,'native':case['verdicts'][cid],'oracle':expected})
        rows.append({'case':case['case'],'candidate_id':case['candidate_id'],'satisfies_all_implemented_checks':all(v=='satisfied' for v in case['verdicts'].values()),'numeric_mismatches':errors,'predicate_mismatches':mismatches})
    document={'kind':'post-failure-diagnostic-not-a-verification-release','cases':rows,'channels_per_case':len(wanted),'constraints_per_case':len(catalog),'cases_with_numeric_mismatches':sum(bool(r['numeric_mismatches']) for r in rows),'cases_with_predicate_mismatches':sum(bool(r['predicate_mismatches']) for r in rows)}
    result_path.write_text(json.dumps(document,indent=2)+'\n')
    print(json.dumps({k:v for k,v in document.items() if k!='cases'}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--record',type=Path,required=True)
    diagnose(parser.parse_args().record)
