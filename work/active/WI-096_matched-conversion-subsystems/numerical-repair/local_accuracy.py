"""Retained local-root regressions against pre-repair independent Decimal receipts."""
import argparse, importlib.util, json, math, sys
from pathlib import Path
R=Path(__file__).resolve().parents[4];H=R/'exploration/component_alternatives';E=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
D=load('diagnosis',E/'gas-root-diagnosis.py')
from component_alternatives_tea.handwritten.component_alternatives_thermal.finite_water_cooler_impl import calculate

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 if args.out.exists():raise FileExistsError(args.out)
 rows=json.loads((H/'studies/20260926-design-study-component-alternatives/results/cases.json').read_text())['cases']
 dec=json.loads((R/'work/orchestration/goals/design-study-component-alternatives/evidence/numerical-repair-review/isolate_original.json').read_text())
 p=D.P;report=[]
 for row in rows:
  cid=row['candidate_id'].rsplit(':',1)[-1]
  if cid not in ('c0035','c0040','c0160','c0206'):continue
  y=row['outputs'];v=row['inputs'];x={k:v[p+'water_pre__'+k] for k in ('ua','water_inlet_C','head','eta_p','eta_motor','flow_rating','power_rating','duty_rating')}
  x.update(gas_inlet_K=y[p+'recuperator__evaluate__hot_out'],gas_outlet_K=y[p+'precooler__evaluate__temperature_out'],gas_heat_into_fluid=y[p+'precooler__evaluate__heat_into_fluid'])
  out=calculate(x);accurate=dec[row['case']]['native_tuple_decimal'];checks={}
  for nk,dk in [('water_outlet_C','outlet'),('water_flow','flow'),('pump_electric','power')]:
   exact=float(accurate[dk]);error=abs(out[nk]-exact);relative=error/max(abs(out[nk]),abs(exact));checks[nk]=dict(native=out[nk],decimal=accurate[dk],absolute_error=error,relative_error=relative);assert relative<1e-9
  exact_margin=x['flow_rating']-float(accurate['flow']);relative=abs(out['flow_margin']-exact_margin)/max(abs(out['flow_margin']),abs(exact_margin));assert relative<1e-9
  report.append(dict(case=cid,exact_inputs=x,checks=checks,flow_margin_relative_error=relative,iterations=out['iterations'],ua_residual=out['ua_residual']))
 net=D.sealed_code((H/'component_alternatives_tea/handwritten/integrated_heat_electricity/network_heat_driven_closure_impl.py').read_text(),'repaired_network')
 control=D.sealed_code((H/'component_alternatives_tea/handwritten/loop_return_control/primary_bypass_control_impl.py').read_text(),'repaired_controller')
 for row in json.loads((E/'gas-root-diagnosis.json').read_text())['cases']:
  if row['candidate_id'].rsplit(':',1)[-1] not in ('c0480','c0484','c0481','c0482','c0485'):continue
  nx=row['exact_native_network_inputs'];cx=row['exact_native_controller_inputs'];native,trace=D.invoke(net,'_reviewed_run_network_heat_driven_closure',nx);c,ct=D.invoke(control,'calculate',cx)
  target=float(row['decimal_network_same_inputs']['he_hot_bound_margin']);relative=abs(native['he_hot_bound_margin']-target)/max(abs(target),abs(native['he_hot_bound_margin']));assert relative<1e-9
  bypass=cx['primary_flow']-c['exchanger_primary_flow'];target_bypass=float(row['decimal_controller_same_inputs']['bypass_flow']);bre=abs(bypass-target_bypass)/max(abs(bypass),abs(target_bypass));assert bre<1e-9
  assert math.nextafter(trace['lo'],math.inf)==trace['hi']
  assert math.nextafter(ct['lo'],math.inf)==ct['hi']
  report.append(dict(case=row['candidate_id'].rsplit(':',1)[-1],network_same_tuple_margin_relative_error=relative,bypass_same_tuple_relative_error=bre,network_trace=trace,controller_trace=ct))
 args.out.write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(report),'local root tuples')
if __name__=='__main__':main()
