"""Preserve actual oracle frame values for a refused endpoint, without replacing physics."""
import json
from pathlib import Path
from exploration.stellarator_e2e.studies import oracle_entry
H=Path(__file__).resolve().parents[1];p=H/'results/edge-scan.json';x=json.loads(p.read_text())
for row in x['edges']:
 if row.get('outcome')!='unsupported_field_domain' or 'actual_peak_field_T' in row:continue
 try:oracle_entry.evaluate(row['point'])
 except ValueError as error:
  assert str(error)=='oracle conductor current: unsupported field'
  trace=error.__traceback__;fields=[]
  while trace is not None:
   if 'B_peak' in trace.tb_frame.f_locals:fields.append(trace.tb_frame.f_locals['B_peak'])
   trace=trace.tb_next
  assert fields and all(v==fields[0] for v in fields)
  row['actual_peak_field_T']=fields[0];row['supported_field_domain_T']=[20,32]
  print(row['axis'],row['edge'],row['value'],'B_peak',fields[0])
 else:raise AssertionError('Expected domain refusal did not recur')
p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
