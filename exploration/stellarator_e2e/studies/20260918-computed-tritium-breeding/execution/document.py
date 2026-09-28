"""Render executor findings from retained native outputs; never evaluates the model."""
import hashlib,json,math,shutil,subprocess
from pathlib import Path
H=Path(__file__).resolve().parents[1];ROOT=H.parents[3];R=H/'results';P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
write=lambda p,x:p.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')
rows=read(R/'interpreted-cases.json');catalog=read(R/'predicate-catalog.json');defaults=read(H/'preparation/resolved-defaults.json')
base=next(x for x in rows if x['proposal_id']=='thickness-0.8');supported=[x for x in rows if x['breeding_defined']]
source=ROOT/'work/orchestration/goals/computed-tritium-breeding/evidence/round2'
for name in ['table-release-review.md','benchmark-and-interface-review.md','method-precheck.md']:
 shutil.copy2(source/name,H/'reviews'/name)
for src in ['models/library/analyses/mfe_plasma_scaling.sysml','models/designs/stellarator_09/breeding_response.json','exploration/stellarator_e2e/studies/study_route.py']:
 dst=H/'preparation/source-copies'/src;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/src,dst)
write(R/'execution-environment.json',{'repo_revision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'launcher':'.codex-test/run','runtime_import_fix':'workflow.py adds STOP_PARSER_TEAX_ROOT/packages/teax-simkit to sys.path and PYTHONPATH and sets STUDY_REQUIRE_TEAX=1','phases_completed':['prepare','baseline','scan','execute','verify','export'],'failed_phase_attempts':[],'warnings':[{'phases':['baseline','execute'],'source':'pydantic serializer','message':'PydanticSerializationUnexpectedValue(Expected bool; field cryoplant inventory_enabled; input_value=1.0, input_type=float)','disposition':'Existing authored numeric carrier; all native execution and verification passed; no model edit.'}],'export_correction':'Keep required_tbr, recycle_loss_rate, decay_rate and stock_growth_rate defined when breeding is undefined; null only breeding-derived diagnostics. Raw results unchanged.'})
vols=[]
for row in rows:
 t=row['thickness_m'];Rmajor=row['R_m'];C=2*math.pi**2*Rmajor
 gross=C*((1.45+t)**2-1.45**2);fw=C*(1.45**2-1.4**2);reflector=C*((1.65+t)**2-(1.45+t)**2)
 assert math.isclose(row['blanket_volume_m3'],fw+gross+reflector,rel_tol=1e-12)
 vols.append({'proposal_id':row['proposal_id'],'costing_aggregate_volume_m3':row['blanket_volume_m3'],'gross_breeder_shell_volume_m3':gross,'removed_breeder_volume_m3':.03*gross,'retained_breeder_volume_m3':.97*gross,'firstwall_fullshell_volume_m3':fw,'reflector_fullshell_volume_m3':reflector,'defined_transport_scenario':row['breeding_defined']})
write(R/'volume-accounting.json',{'basis':'Accounting geometry only for unsupported cases; no transport prediction implied. C=2*pi^2*R, kappa=1; firstwall r=1.4 to1.45m; breeder1.45 to1.45+t; reflector1.45+t to1.65+t. Native CAS22 blanket volume sums all three full shells; transport retains whole FW but removes3% breeder and reflector.', 'source_copy':'preparation/source-copies/models/library/analyses/mfe_plasma_scaling.sysml','rows':vols})
table=['| Thickness m | Mean TBR | Numerical lower | TBR screen | Peak-field screen | Blanket cost $M | LCOE $/MWh |','|---|---|---|---|---|---|---|']
tbr=next(k for k,v in catalog.items() if v['source_local_identity']=='tbr_ok');peak=next(k for k,v in catalog.items() if v['source_local_identity']=='peak_field_ok')
for x in supported:table.append(f"| {x['thickness_m']:g} | {x['tbr_mean']:.6f} | {x['tbr_lower']:.6f} | {x[tbr]} | {x[peak]} | {x['blanket_cost_dollars']/1e6:.3f} | {x['LCOE_dollars_MWh']:.3f} |")
v=next(x for x in vols if x['proposal_id']=='thickness-0.8')
report='''# Computed breeding thickness study

Executor synthesis, 2026-09-18. This is a conditional conceptual-design sensitivity, with all native outcomes retained. It is not an independent study reading or an actual-plant self-sufficiency claim.

The 0.80 m reference build has mean TBR 1.198074, but its numerical lower estimate is 1.186146 against the conditional requirement 1.190000. The mean alone would hide the failed numerical screen. The sampled 0.825 m case clears that screen and newly fails the peak-field screen. Every case also retains failed divertor heat, reference conductor current and winding-pack fit screens. No whole-plant feasible case was found in this fixed-default study.

'''+ '\n'.join(table)+'''

These are generated-package interpolation results, not new transport histories. The lower estimate subtracts the fixed 0.01 interpolation allowance and twice the propagated Monte Carlo standard error. Independent withheld transport points tested the interpolation upstream. Those numerical checks do not bound alloy, source-profile, nuclear-data, actual openings or shaped-geometry uncertainty. The exact crossing between sampled values was not searched and no continuous feasible boundary or optimum is claimed.

## Consequences elsewhere in the plant

At supported endpoints 0.60 and 1.00 m, native coil-bore radius rises from 2.8 to 3.2 m, blanket cost from $551.362M to $899.684M, total capital from $8.364B to $9.471B and LCOE from $134.126 to $156.000/MWh. Thermal power remains 3301.213 MW and availability 0.902778 because their relevant assumptions are held. Net power decreases slightly from 1012.6337 to 1012.5828 MW. These outcomes come from the existing plant graph; increasing computed TBR does not supply extra energy. The neutron-energy multiplier remains the held input 1.2.

Moving from 0.80 to 0.90 m increases blanket cost from $718.414M to $807.272M and LCOE from $144.747 to $150.295/MWh. At the 0.90 m point breeding passes conditionally and peak field fails. Improving one screen therefore incurs a represented magnet/build tradeoff rather than recovering a previously passing whole plant.

## Undefined-domain diagnostics

The 0.55 m and 1.05 m thickness cases and the R=12.71 m case retain undefined breeding and a failed TBR predicate. Their raw zero carriers remain in native-cases.json, while interpreted-cases.json and points.csv display breeding-derived quantities as null. They retain defined account requirements and independent loss streams, plus unrelated plant costs/power/verdicts. None is evidence of a physical TBR deficit or an extrapolated response.

## Volume and cost accounting

'''+f"At 0.80 m, the native blanket cost volume is {v['costing_aggregate_volume_m3']:.6f} m³. It aggregates full-shell first wall ({v['firstwall_fullshell_volume_m3']:.6f} m³), gross breeder ({v['gross_breeder_shell_volume_m3']:.6f} m³) and reflector ({v['reflector_fullshell_volume_m3']:.6f} m³). The transport scenario removes {v['removed_breeder_volume_m3']:.6f} m³ of breeder in its 10.8-degree window, leaving {v['retained_breeder_volume_m3']:.6f} m³. It also removes the same angular fraction of reflector and high-temperature shield, while retaining the first wall.\n\n"+'''The source formula is C=2π²Rκ and each shell has volume C(r_outer²−r_inner²), with R=12.7 m and κ=1. The inner radii are 1.40 m for the first wall, 1.45 m for the breeder and 1.45+t for the reflector; thicknesses are 0.05 m, t and 0.20 m. The copied model source and complete per-case reconstruction are retained in preparation/source-copies/ and results/volume-accounting.json. The CAS22 aggregate is not a pure breeder volume. Full-shell charging, generic unit costs and an opening with no installed port cost form a declared cost convention; they do not establish identical material inventories or qualified installed costs.

## Verification and custody

All 13 native cases completed. Independent software arithmetic agreed for all 3,185 mapped scalar comparisons and all 260 predicate comparisons. The generic verifier also passed with no exceptions; its worst relative scalar deviation was 1.512e-15. All 261 numeric native outputs are retained at every case; 16 are outside the 245-channel oracle map. The oracle and implementation share transport response data, so their agreement is not independent physical validation. Physical table review, transport validation and benchmark limitations are copied into this record.

Evidence: results/points.csv; results/native-cases.json; results/oracle-all-points.json; results/verification_summary.json; results/volume-accounting.json; preparation/transport-evidence/; reviews/table-release-review.md. The 13 prepared points and all failed screens remain unchanged. No model, limit, allowance, operating input or studied window was tuned after results.
'''
(H/'report.md').write_text(report)
print('Rendered report and custody/accounting evidence')
