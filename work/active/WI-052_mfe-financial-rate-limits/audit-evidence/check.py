import csv, importlib.util, json, math, re, xml.etree.ElementTree as ET
from collections import Counter
from decimal import Decimal as D, localcontext
from pathlib import Path
ROOT=Path.cwd(); ITEM=ROOT/'work/active/WI-052_mfe-financial-rate-limits'; I=ITEM/'implementation'; A=ITEM/'audit-evidence'
def load(path):return json.loads(path.read_text())
def junit(path):
    result={}
    for x in ET.parse(path).getroot().iter('testcase'):
        key=(x.get('classname'),x.get('name')); status=next((t for t in ('failure','error','skipped') if x.find(t) is not None),'passed')
        assert key not in result
        result[key]=(status,x.find(status).get('message','') if status!='passed' else '')
    return result
report={}
for suite in ('models','study'):
    old=junit(I/f'entering/pytest-{suite}.xml');new=junit(I/f'pytest-{suite}.xml')
    inherited={k:v for k,v in old.items() if v[0]!='passed'}
    assert all(new.get(k)==v for k,v in inherited.items())
    fresh={str(k):v for k,v in new.items() if v[0] in ('failure','error') and old.get(k,('absent',))[0] not in ('failure','error')}
    report[suite]={'entering':dict(Counter(v[0] for v in old.values())),'candidate':dict(Counter(v[0] for v in new.values())),'inherited_identical':len(inherited),'new_failures':fresh,'removed':[str(k) for k in old.keys()-new.keys()]}
assert len(report['study']['new_failures'])==22
spec=importlib.util.spec_from_file_location('factors',ROOT/'exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/financial_factors.py');f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
checks=[]
with localcontext() as ctx:
    ctx.prec=110
    for n in (.3,.75,1.01,7.25,30.5,199.75):
        for rate in (0.,-.02,.02,.08,-1e-18,1e-18,-1e-10,1e-10):
            i=D(rate);N=D(n)
            values={'crf':(f.crf(rate,n),1/N if not i else i*(1+i)**N/((1+i)**N-1)), 'idc':(f.idc(rate,n),D(0) if not i else ((1+i)**N-1)/(N*i)-1)}
            for g in ((rate,math.nextafter(rate,math.inf),math.nextafter(rate,-math.inf),0.) if rate else (0.,1e-18,-1e-18)):
                G=D(g);first=D(1234567)*(1+G)**D(8.25)
                expected=first*N/(1+i) if i==G else first*(1-((1+G)/(1+i))**N)/(i-G)
                values['annuity_'+repr(g)]=(f.annuity_pv(1234567.,rate,g,n,8.25),expected)
            for name,(actual,expected) in values.items():
                error=abs(D(actual)-expected)/(abs(expected) if expected else D(1));assert error<=D('1e-9'),(name,n,rate,error)
                checks.append({'quantity':name,'duration':n,'rate':rate,'actual':actual,'expected':str(expected),'error':str(error)})
report['additional_numerical_checks']=checks
new=load(A/'native-absolute/native.json');author=load(I/'native-results.json');assert new==author
old=load(I/'entering/native.json');ledger=load(I/'scalar-ledger.json');assert old['inputs']==new['inputs'];assert len(new['inputs'])==246
for case,row in new['cases'].items():
    assert len(row['outputs'])==158
    baseline=old['cases'][case.split('_')[0]+'_ordinary'];assert list(row['outputs'])==list(baseline['outputs']);assert row['responses']==baseline['responses'] and row['report']==baseline['report']
    assert {r['name'] for r in ledger[case]}==set(row['outputs'])
    for r in ledger[case]:
        assert r['candidate']==row['outputs'][r['name']]
        if r['coverage']=='exact entering physical/other':assert r['candidate']==baseline['outputs'][r['name']]
report['native']='Fresh ten-case output exactly equals retained candidate; 158 scalars each, input defaults, physical/report/verdict checks pass'
for name in ('mfe_account_costs.sysml','mfe_lcoe_dcf.sysml','mfe_lifecycle.sysml'):
    assert (ROOT/'models/library/analyses'/name).read_bytes()==(ROOT/'exploration/stellarator_e2e/models/analyses'/name).read_bytes()
report['mirror']='three changed pairs byte equal'
rows=list(csv.DictReader((ROOT/'data/traceability_matrix.csv').open()))
report['traceability']=[r for r in rows if r['Element'].strip("'") in ('IDC Closed-Form Cost','Levelized Annual Cost','LCOE DCF','Lifecycle Calendar')]
(A/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(checks),'fresh independent Decimal checks; exact fresh native reproduction; raw JUnit comparison confirms 22 new nodes')
