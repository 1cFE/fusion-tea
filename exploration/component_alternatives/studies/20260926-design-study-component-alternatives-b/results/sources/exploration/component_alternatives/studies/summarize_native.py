"""Summarize stored native identities, predicate outcomes and declared-axis levels."""
import argparse
import collections
import json
from pathlib import Path


def summarize(record):
    read=lambda name:json.loads((record/name).read_text())
    verification=read('results/verification_summary.json')
    if verification['outcome']!='pass':raise ValueError('verified native evidence required')
    cases=read('results/cases.json')['cases']; catalog=read('results/constraint_catalog.json')
    target=record/'results/constraint-summary.json'
    if target.exists():raise ValueError('preserve prior summary')
    constraints=[{'constraint_id':cid,'source_local_identity':entry['source_local_identity'],
                  'counts':dict(collections.Counter(r['verdicts'][cid] for r in cases)),
                  'violated_cases':[r['case'] for r in cases if r['verdicts'][cid]!='satisfied']}
                 for cid,entry in catalog.items()]
    target.write_text(json.dumps(constraints,indent=2)+'\n')
    groups={a['axis']:a for a in read('axes.json')['groups']}; judged=[]
    for frame in read('axis-framing.json'):
        keys=[row['key'] for row in groups[frame['axis']]['keys']]
        levels=sorted({tuple(r['inputs'][k] for k in keys) for r in cases})
        row=dict(frame,executed=len(levels)>1,framing_judged=frame['framing_proposed'],changed=False,tested_values=levels)
        row['level_outcomes']=[]
        for level in levels:
            selected=[r for r in cases if tuple(r['inputs'][k] for k in keys)==level]
            passed=[r for r in selected if all(v=='satisfied' for v in r['verdicts'].values())]
            row['level_outcomes'].append({'values':level,'cases':len(selected),'satisfying_all_checks':len(passed),'case_ids':[r['candidate_id'] for r in selected]})
        row['account']=('Declined under held steam offer; no varied native point or boundary claim.' if frame['declined'] else 'Finite catalog only; coordinated choices prevent isolated causal attribution from grouped counts.' if frame['framing_proposed']=='search' else 'Hypothetical scenario response at selected anchors; no boundary claim.')
        judged.append(row)
    (record/'results/axis-assessment.json').write_text(json.dumps(judged,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'constraints':len(constraints),'axes':len(judged),'predicate_passing':sum(all(v=='satisfied' for v in r['verdicts'].values()) for r in cases)}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--record',type=Path,required=True)
    summarize(parser.parse_args().record)
