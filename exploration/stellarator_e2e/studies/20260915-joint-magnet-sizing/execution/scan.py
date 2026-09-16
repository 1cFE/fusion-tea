"""Independent oracle scan; retain refusals, never perform an outer sizing solve."""
import json
from pathlib import Path
from collections import Counter
from exploration.stellarator_e2e.studies import oracle_entry as oe, study_route as route
from scripts.study.verify import derive_verdict, package_input_values
H=Path(__file__).resolve().parents[1]; R=H/'results'
read=lambda p:json.loads(p.read_text())
def write(name,x):(R/name).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
assert read(R/'preflight_results.json')['outcome']=='pass'
params=package_input_values(route.PACKAGE_DIR)
catalog=route._catalog_by_constraint_id(route.PACKAGE_DIR); bindings=oe.operand_bindings()
def evaluate(row):
    point=row['point']
    try:
        channels=oe.evaluate(point)
        verdicts={cid:'satisfied' if derive_verdict(cid,e,bindings,point,params,channels)[0] else 'violated' for cid,e in catalog.items()}
        return row|{'outcome':'evaluated','channels':channels,'verdicts':verdicts,
                   'violated':[catalog[c]['source_local_identity'] for c,v in verdicts.items() if v!='satisfied'],
                   'full_satisfied':all(v=='satisfied' for v in verdicts.values())}
    except ValueError as error:
        trace=error.__traceback__; fields=[]
        while trace is not None:
            if 'B_peak' in trace.tb_frame.f_locals: fields.append(trace.tb_frame.f_locals['B_peak'])
            trace=trace.tb_next
        return row|{'outcome':'refused','error':str(error),'actual_peak_field_T':fields[0] if fields else None,
                   'full_satisfied':False,'verdicts':None,'interpretation':'Unsupported evaluation, not physical infeasibility or nonconvergence.'}
if __name__=='__main__':
    rows=[evaluate(r) for r in read(H/'preparation/scan-proposals.json')]
    write('initial-oracle-scan.json',{'rows':rows,'states':dict(Counter(r['outcome'] for r in rows))})
    valid=[r for r in rows if r['outcome']=='evaluated']
    print('states',Counter(r['outcome'] for r in rows),'passes',sum(r['full_satisfied'] for r in valid))
    print('default passes',[(r['id'],r['channels'][oe.P+'lcoe_calc__lcoe']) for r in valid if r['family']=='default-grid' and r['full_satisfied']][:20])
    print('violations',Counter(v for r in valid if r['family']=='default-grid' for v in r['violated']))
