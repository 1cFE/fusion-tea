"""Independent C1 correction arithmetic from exact captured native terms."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).resolve().parent
CAP=ROOT/'work/active/WI-098_whole-plant-conversion-comparison/evidence/magnet-capture'
P='stellarator_09__stellaris__'
x=json.loads((CAP/'offer-inputs.json').read_text())
case=json.loads((CAP/'native-cases.json').read_text())[1]
o=case['outputs']
V=o[P+'magnet__wp_volume__vol_cold_total']
inventory=o[P+'cryoplant__inventory__q_inventory_cold']
intercept=o[P+'cryoplant__inventory__q_inventory_shield']
fixed=x[P+'cryoplant__p_fixed_cryo']*1e6
Tc=x[P+'cryoplant__T_cold_cryo'];Ts=x[P+'cryoplant__T_shield'];Ta=x[P+'cryoplant__T_amb_cryo']
COPc=x[P+'cryoplant__f_carnot_cryo']*Tc/(Ta-Tc)
COPs=x[P+'cryoplant__f_carnot_shield']*Ts/(Ta-Ts)
cold_rating=x[P+'cryoplant__rated_cold_W']
intercept_rating=x[P+'cryoplant__rated_intercept_W']

def evaluate(q,extra):
    assert math.isfinite(q) and math.isfinite(extra) and q>=0 and extra>=0
    cold=q*V+extra+fixed+inventory
    electric=(cold/COPc+intercept/COPs)*1e-6
    return {'q_W_m3':q,'extra_W':extra,'cold_W':cold,'intercept_W':intercept,'refrigeration_MW':electric,'cold_margin_W':cold_rating-cold,'intercept_margin_W':intercept_rating-intercept,'refrigerator_heat_to_sink_MW':electric+(cold+intercept)*1e-6,'q_limit_W_m3':(cold_rating-fixed-inventory-extra)/V}

rows=[evaluate(q,e) for q,e in ((35.5,0),(50,0),(80,0),(35.5,10000),(35.5,13000))]
assert abs(rows[0]['cold_W']-o[P+'cryoplant__cold_load__p_cold']*1e6)<1e-10
assert abs(rows[0]['refrigeration_MW']-o[P+'cryoplant__refrigeration_sum__total'])<1e-12
assert [r['cold_margin_W']>=0 for r in rows]==[True,True,False,True,False]
drive=o[P+'cryoplant__inventory__p_drive']
drive_heat=(o[P+'cryoplant__inventory__q_lead_cold']+o[P+'cryoplant__inventory__q_lead_shield']+fixed)*1e-6
assert x[P+'cryoplant__joint_drive_fraction']==1
assert abs(drive-drive_heat)<1e-15
result={'scope':'Equation probe, no new native scenario execution or scientific qualification.','capture_candidate':case['candidate_id'],'capture_input_sha256':hashlib.sha256((CAP/'offer-inputs.json').read_bytes()).hexdigest(),'scenarios':rows,'coil_drive_already_in_extracted_heat_MW':drive,'fixed_quote_USD2025':x[P+'cryoplant__purchase_cost_per_module']}
(HERE/'capture-r2-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
