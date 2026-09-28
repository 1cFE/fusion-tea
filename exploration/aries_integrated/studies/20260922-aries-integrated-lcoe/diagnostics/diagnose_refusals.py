"""Retain partial native results for actual financial refusals, outside study protocol."""
import hashlib,json,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
DIAGNOSTIC=ROOT/'.project/active/aries-comparison-preparation/post-reveal-investigation/failure-propagation/native-teax'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(DIAGNOSTIC))
from simkit.evaluation.evaluator import PreparedEvaluator
from simkit.evaluation.package_load import ProvisionalPackageLoader
from simkit.study.bridge import CandidateBridge
from simkit.evaluation.diagnostics import plain

package=ROOT/'exploration/aries_integrated/aries_integrated'
work=Path(tempfile.mkdtemp(prefix='wi091-native-diagnostic-'))
prepared=PreparedEvaluator(ProvisionalPackageLoader(package_dir=package,package_name='aries_integrated',link_root=work/'links',strict=True),package/'pipelines/pipeline.yaml',expects_constraint_report=True)
rows=json.loads((HERE/'development-cases.json').read_text());bridge=CandidateBridge(prepared.entry_models)
selected=['no-breeding-credit','nonpositive_energy','negative_discount','double_source_financing']
records=[]
for row in rows:
    if row['case'] not in selected:continue
    assert prepared.fingerprint==row['fingerprint']
    typed=bridge.build(row['effective_inputs'])
    evidence=prepared.diagnose(typed);doc=evidence.to_document()
    if row['status']=='evaluated':
        for key,value in evidence.numeric_outputs.items():assert value==row['outputs'][key],(key,value,row['outputs'][key])
        assert evidence.state=='complete_diagnostic'
    else:assert evidence.state=='partial'
    P='aries_integrated_plant__'
    power=evidence.numeric_outputs.get(P+'plant_ledger__evaluate__net_electric')
    if row['case']=='nonpositive_energy':
        assert power is not None and power<0
        assert P+'lifecycle_price__evaluate__lcoe' not in evidence.numeric_outputs
        assert evidence.publications[P+'lifecycle_price__evaluate__lcoe']['status']=='blocked_dependency'
    if row['case']=='negative_discount':assert P+'lifecycle_price__evaluate__lcoe' not in evidence.numeric_outputs
    if row['case']=='double_source_financing':assert P+'source_lifecycle_price__evaluate__lcoe' not in evidence.numeric_outputs
    path=HERE/('diagnostic-'+row['case']+'.json')
    path.write_text(json.dumps(doc,indent=2,sort_keys=True,allow_nan=False)+'\n')
    predicates={key:plain(value) for key,value in plain(evidence.publications).items() if value['status']=='available_structured' and isinstance(value.get('structured_value'),dict) and value['structured_value'].get('status') in ('satisfied','violated','indeterminate')}
    records.append(dict(case=row['case'],state=evidence.state,net_electric_mw=power,numeric_count=len(evidence.numeric_outputs),predicate_count=len(predicates),predicates=predicates,provenance=plain(evidence.provenance),integrated_lcoe_publication=plain(evidence.publications[P+'lifecycle_price__evaluate__lcoe']),source_lcoe_publication=plain(evidence.publications[P+'source_lifecycle_price__evaluate__lcoe']),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
    print(row['case'],evidence.state,power,len(evidence.numeric_outputs),flush=True)
(HERE/'diagnostic-verification.json').write_text(json.dumps({'passed':True,'runtime':str(DIAGNOSTIC.relative_to(ROOT)),'baseline_numeric_parity':True,'cases':records},indent=2,allow_nan=False)+'\n')
