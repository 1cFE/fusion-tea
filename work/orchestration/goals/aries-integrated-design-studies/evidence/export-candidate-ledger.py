"""Export readable per-candidate accounting from frozen native-derived study records."""
import csv,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
STUDIES=ROOT/'exploration/aries_integrated/studies'
IDS=['20260922-aries-integrated-local-response','20260922-aries-integrated-coupled-design','20260922-aries-integrated-design-robustness']
rows=[];sources=[]
for sid in IDS:
 r=STUDIES/sid;p=r/'results/accounting.json';data=json.loads(p.read_text())
 sources.append({'study':sid,'accounting_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'snapshot_sha256':hashlib.sha256((r/'snapshot.json').read_bytes()).hexdigest()})
 for x in data['cases']:
  row={'study':sid,'case':x['case'],'scenario':x['scenario'],'classification':x['classification'],'net_MW':x['net_mw'],'annual_MWh':x['annual_mwh'],'gross_T_kg_per_calendar_year':x['gross_makeup_kg_year'],'assumed_new_feed_kg_per_calendar_year':x['new_feed_kg_year'],'external_T_purchase_kg_per_calendar_year':x['external_purchases_kg_year'],'curtailed_feed_kg_per_calendar_year':x['curtailed_feed_kg_year'],'supply_service_USD2004_per_year':x['service_annual_usd2004'],'overnight_USD2004':x['overnight_usd2004'],'unmet_heat_MW':x['unmet_heat_mw'],'passes_evaluated_checks':x['passes_evaluated_checks'],'scientific_qualification':x['scientific_qualification']}
  for branch,vals in x['equipment'].items():
   for k,v in vals.items():row[branch+'_'+k]=v
  row.update({k+'_USD2004_per_MWh':v for k,v in x['contributions'].items()})
  row['failed_predicates']='; '.join(k+'='+v for k,v in x['verdicts'].items() if v!='satisfied')
  rows.append(row)
with (HERE/'candidate-ledger.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
(HERE/'candidate-ledger-provenance.json').write_text(json.dumps({'rows':len(rows),'sources':sources,'quantity_origin':'All engineering values selected unchanged from native-derived accounting.json; reporting does not evaluate a model.'},indent=2)+'\n')
print(json.dumps({'rows':len(rows),'output':str(HERE/'candidate-ledger.csv')}))
