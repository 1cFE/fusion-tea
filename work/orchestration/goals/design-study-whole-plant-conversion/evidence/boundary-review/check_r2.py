"""Independent r2 design-equation probe, using labelled synthetic purchases.

This is not native acceptance of the unexecuted magnet or whole-plant package.
"""
from decimal import Decimal as D
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
common_names = '''land facilities magnet heating divertor blanket shield structure vessel power_supplies remote_handling installation primary_circulators primary_pipes primary_spares primary_helium cryoplant auxiliary_rejection waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous pbl_initial owner digital_twin source_installation_allowance tritium_initial'''.split()
H = set('''magnet heating divertor blanket shield structure vessel power_supplies remote_handling primary_circulators primary_pipes cryoplant auxiliary_rejection waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous'''.split())
F = set('''magnet heating divertor blanket shield structure vessel power_supplies remote_handling cryoplant waste fuel_processing other_reactor reactor_controls shared_electrical miscellaneous'''.split())
assert H <= set(common_names) and F <= H
q = {n: D(i+1)*1000000 for i,n in enumerate(common_names)}
branch = {f'slot{i}':D(i)*1000000 for i in range(3,11)} | {'controller':D(1000000)}

def gas_overheads(q,b,c=D('.1'),i=D('.2')):
    direct=sum(v for n,v in q.items() if n not in {'land','owner','tritium_initial'})+sum(b.values())
    equipment=sum(q[n] for n in H)+sum(b.values())
    freight=sum(q[n] for n in F)+sum(v for n,v in b.items() if n!='slot9')
    spares=equipment-q['primary_circulators']
    tax=equipment+sum(q[n] for n in ('primary_spares','primary_helium','pbl_initial','tritium_initial'))
    contingency=c*direct
    indirect=i*(direct+contingency)*D(8)/6
    costs={'contingency':contingency,'indirect':indirect,'freight':D('.015')*freight,'spares':D('.02')*spares,'tax':D('.01')*tax,'insurance':D('.015')*(direct+contingency+indirect),'commissioning':D('.005')*direct}
    subtotal=direct+sum(q[n] for n in ('land','owner','tritium_initial'))
    assert subtotal==sum(q.values())+sum(b.values())
    return {'initial':subtotal+sum(costs.values()),'bases':{'direct':direct,'equipment':equipment,'freight':freight,'spares':spares,'tax':tax},'overheads':costs}

base=gas_overheads(q,branch)
changed=gas_overheads(q,branch|{'slot3':branch['slot3']+D(1000000)})
slot9=gas_overheads(q,branch|{'slot9':branch['slot9']+D(1000000)})
assert changed['bases']['direct']-base['bases']['direct']==1000000
assert changed['bases']['freight']-base['bases']['freight']==1000000
assert slot9['bases']['freight']==base['bases']['freight']
assert gas_overheads(q,branch)==base  # Other branch's held purchases cannot mutate.
mid=gas_overheads(q,branch,c=D('.1'))['initial']
assert 2*mid==gas_overheads(q,branch,c=D(0))['initial']+gas_overheads(q,branch,c=D('.2'))['initial']

fuel=[]
for source,tbr,extraction,recovery in product((2500,2800),('1.1980739195540366','1.1861455810023918'),('1','.9'),('.99','.98')):
    a=D('3.52')/D('17.58'); fusion=(D(source)-50)/(D('1.2')*(1-a)+a)
    reactions=D('.8')*31536000*fusion*1000000/(D('17.58')*D('1.602176634e-13'))
    loss=reactions*(1-D('.05'))/D('.05')*(1-D(recovery))
    decay=D(5)/D('5.008267663228036e-27')*D('1.782785958230312e-9')*31536000
    need=reactions+loss+decay; bred=reactions*D(tbr); usable=bred*D(extraction)
    external=max(need-usable,D(0)); surplus=max(usable-need,D(0))
    d_purchase=reactions+loss; li_purchase=bred
    residuals=[d_purchase-reactions-loss,external+usable-need-surplus,li_purchase-bred]
    assert all(abs(r)<D('1e-25')*reactions for r in residuals)
    fuel.append({'source':source,'tbr':tbr,'extraction':extraction,'recovery':recovery,'external_T_kg':float(external*D('5.008267663228036e-27')),'D_kg':float(d_purchase*D('3.3435837768e-27')),'Li6_kg':float(li_purchase*D('6.015122795')*D('1.66053906892e-27'))})

paths=['work/active/WI-098_whole-plant-conversion-comparison/'+n for n in ('design.md','configuration.md')]
result={'status':'design arithmetic checks passed','synthetic_purchase_note':'Distinct synthetic amounts test membership and response; these are not predicted plant costs. Exact gas aggregate slots include inseparable transport stock.','reviewed_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'synthetic_gas_base':base,'slot3_increment_initial':changed['initial']-base['initial'],'delivered_slot9_increment_initial':slot9['initial']-base['initial'],'fuel_scenarios':fuel}
(HERE/'r2-checks.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps({'status':result['status'],'fuel_scenarios':len(fuel),'slot3_increment_initial':str(result['slot3_increment_initial']),'delivered_slot9_increment_initial':str(result['delivered_slot9_increment_initial'])}))
