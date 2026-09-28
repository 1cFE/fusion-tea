"""Matched entering oracle controls; native execution is separately tested/studied."""
import json, math, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from exploration.stellarator_e2e.studies import oracle_entry as oe, study_route as route
from scripts.study.verify import derive_verdict, package_input_values
from tests.models.current_mfe_regressions import WI040_CHANGED_ECONOMICS
HERE=Path(__file__).resolve().parent
old=json.loads((ROOT/'work/orchestration/goals/tape-procurement-consistency/evidence/entering/comparison.json').read_text())
changed={oe.ORACLE_OUTPUT_TO_CHANNEL[k] for k in WI040_CHANGED_ECONOMICS}
changed|={oe.ORACLE_OUTPUT_TO_CHANNEL[k] for k in ('winding_pack','tape_procurement_cost')}
retired=oe.P+'magnet__conductor_grade__cost_per_kAm_effective'
catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR)
params=package_input_values(route.PACKAGE_DIR);bindings=oe.operand_bindings()
rows=[];count=0
for row in old['rows']:
    current=oe.evaluate(row['point'])
    for key,value in row['channels'].items():
        if key not in changed and key != retired:
            assert math.isclose(current[key],value,rel_tol=1e-12,abs_tol=1e-12),(row['id'],key,current[key],value)
            count+=1
    verdicts={e['source_local_identity']:('satisfied' if derive_verdict(cid,e,bindings,row['point'],params,current)[0] else 'violated') for cid,e in catalog.items()}
    assert verdicts==row['verdicts'],row['id']
    rows.append({'id':row['id'],'tape_length':current[oe.ORACLE_OUTPUT_TO_CHANNEL['tape_length']],
        'tape_cost_before':row['channels'][oe.ORACLE_OUTPUT_TO_CHANNEL['tape_procurement_cost']],
        'tape_cost_after':current[oe.ORACLE_OUTPUT_TO_CHANNEL['tape_procurement_cost']],
        'lcoe_before':row['channels'][oe.ORACLE_OUTPUT_TO_CHANNEL['lcoe']],
        'lcoe_after':current[oe.ORACLE_OUTPUT_TO_CHANNEL['lcoe']]})
report={'scope':'60 matched oracle cases, not native study execution','unchanged_scalar_comparisons':count,
        'unchanged_predicate_comparisons':60*18,'mismatches':0,'rows':rows}
(HERE/'matched-entering.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',count,'unchanged scalar comparisons and',60*18,'predicate comparisons')
