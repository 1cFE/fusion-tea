"""Combine reviewed dispositions, preserving every original comparison row."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
BASE = HERE.parent.parent

def build():
    original = json.loads((BASE/'partial-assessment/attempts/diagnostic-1/report.json').read_text())
    quantities = json.loads((HERE/'quantity-rows.json').read_text())
    costs = json.loads((HERE/'cost-rows.json').read_text())
    q = {r['id']:r for r in quantities['rows']}
    c = {r['id']:r for r in costs['rows']}
    assert len(q) == len(c) == 35 and not (q.keys() & c.keys())
    structural = {'subsystems':('fail','Missing separate PbLi heat-removal branch; see structure.md for B-2 interpretation.'), 'radial_order':('pass','Pass only for the prescribed qualitative sequence; no dimension or clearance qualification.'), 'cas_coverage':('unresolved','Broad account machinery present; full scope mapping remains unresolved.')}
    rows=[]
    for prior in original['rows']:
        key = prior['id']
        row={'id':key,'axis':prior['axis'],'original_row':prior,'assessment_verdict':'not_established','nominal_ratio':None,'independent_prediction_credit':False}
        if key in structural:
            verdict,reason=structural[key]
            row.update(disposition='structural_review',assessment_verdict=verdict,reason=reason,evidence='structure.md')
        elif key in q:
            item=q[key]
            row.update(disposition=item['disposition'],reason=item['reason'],nominal_ratio=item['nominal_ratio'],evidence='quantities.md',detailed_assessment=item)
        elif key in c:
            item=c[key]
            row.update(disposition='cost_review',assessment_verdict=item['scientific_verdict'],reason=item['specific_blocker'],nominal_ratio=item['nominal_model_reference_ratio'],evidence='costs.md',detailed_assessment=item)
        elif prior['role'] in ('held','supplied'):
            row.update(disposition='selected_or_supplied_information',reason='Selected or supplied value; no independent prediction credit.',evidence='../partial-assessment/report.md')
        elif prior['numerical_availability']=='structural_evidence_required':
            row.update(disposition='missing_corresponding_model_or_scope',reason=prior['historical_correspondence_evidence'],evidence='../partial-assessment/report.md')
        elif prior['model_definedness']=='undefined':
            row.update(disposition='blocked_model_domain',reason='Model-definedness guards or downstream dependencies suppress this value.',evidence='../partial-assessment/attempts/diagnostic-1/model-definedness.json')
        elif prior['numerical_availability']=='unavailable_dependency':
            row.update(disposition='unavailable_calculation',reason='Conductor calculation refused its domain; no predicted value exists.',evidence='../partial-assessment/report.md')
        elif prior['field_qualification']['field_applicability']!='unaffected_by_field_finding':
            row.update(disposition='blocked_field_qualification',reason='Field model applicability is unqualified; numerical arithmetic is not a supported prediction.',evidence='../partial-assessment/attempts/diagnostic-1/field-qualification.json')
        else:
            row.update(disposition='retained_diagnostic',reason='Field-independent diagnostic retained; no source-comparison or engineering-acceptance claim.',evidence='../partial-assessment/report.md')
        rows.append(row)
    assert len(rows)==276 and len({r['id'] for r in rows})==276
    assert [r['original_row'] for r in rows]==original['rows']
    assert all(r['nominal_ratio'] is None or r['id'] in (q.keys()|c.keys()) for r in rows)
    assert all(not r['independent_prediction_credit'] for r in rows)
    return {'schema_version':1,'comparison_kind':'post_reveal_partial_assessment','source_report_sha256':hashlib.sha256((BASE/'partial-assessment/attempts/diagnostic-1/report.json').read_bytes()).hexdigest(),'row_count':len(rows),'disposition_counts':dict(Counter(r['disposition'] for r in rows)),'axis_verdicts':{'structural':'fail','derived':'not_established','cost':'not_established','overall':'does_not_pass'},'supported_lcoe':None,'rows':rows}

if __name__=='__main__':
    result=build()
    (HERE/'comparison-rows.json').write_text(json.dumps(result,indent=2)+'\n')
    with (HERE/'comparison-rows.csv').open('w',newline='') as f:
        names=['id','axis','disposition','assessment_verdict','nominal_ratio','independent_prediction_credit','reason','evidence']
        writer=csv.DictWriter(f,fieldnames=names,extrasaction='ignore');writer.writeheader();writer.writerows(result['rows'])
    print(json.dumps({'rows':result['row_count'],'counts':result['disposition_counts']},indent=2))
