"""Reviewed finite accounting diagnostics; never mutates model/source output terms."""
import hashlib,json,math,sys
from pathlib import Path
D=Path(__file__).resolve().parent; ROOT=D.parents[4];sys.path.insert(0,str(ROOT))
from exploration.stellarator_e2e.studies import oracle_entry as oe,study_route as route
from scripts.study.verify import derive_verdict,package_input_values
read=lambda p:json.loads(p.read_text()); sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert read(D/'reuse-check.json')['outcome']=='pass'
assert '**PASS for the finite diagnostics' in (D/'source-math-review.md').read_text()
H=ROOT/'exploration/stellarator_e2e/studies/20260916-stellaris-reference-reconciliation'
selected=['legacy-control','exact-profiles-legacy','table5-conditioned-legacy','offref-R-plus2pct','offref-a-plus2pct']
rows={r['proposal_id']:r for r in read(H/'results/native-cases.json')}
params=package_input_values(route.PACKAGE_DIR);cat=route._catalog_by_constraint_id(route.PACKAGE_DIR); bindings=oe.operand_bindings()
checks=[]; errors=[]; n=0;m=0;worst=0
for name in selected:
 row=rows[name];ch=oe.evaluate(row['inputs']);n+=len(ch)
 for k,v in ch.items():
  native=row['outputs'][k];worst=max(worst,abs(v-native)/max(abs(v),abs(native),1e-300))
  if not math.isclose(native,v,rel_tol=1e-9,abs_tol=0):errors.append([name,k,native,v])
 verdict={cid:'satisfied' if derive_verdict(cid,e,bindings,row['inputs'],params,ch)[0] else 'violated' for cid,e in cat.items()};m+=len(verdict)
 for k,v in verdict.items():
  if row['verdicts'][k]!=v:errors.append([name,k,row['verdicts'][k],v])
 checks.append({'case':name,'outputs':ch,'verdicts':verdict,'source_native_candidate':row['candidate_id']})
assert not errors,errors
inv=read(D/'model-accounting/inventory.json'); by={r['case']:r for r in inv['cases']}; t=by['table5-conditioned-legacy']['terms']
W=t['W_th'];tau=t['tau_E'];R=t['p_rad'];Halpha=t['p_alpha_heat'];F=t['p_fus'];A=t['p_aux_required'];Ws=504.65;ts=1.46;Fs=2700.;Hs=.95*.2*Fs
C=W/tau;Cs=Ws/ts
combos=[{'W_tau':'model' if not c else 'published_pair_conditional','alpha':'model' if not h else 'source_fusion_with_approx_0.2','radiation':'model','aux_MW':R+(Cs if c else C)-(Hs if h else Halpha)} for c in (0,1) for h in (0,1)]
dW=Ws/tau-C;dt=W/ts-C;interaction=Cs-Ws/tau-W/ts+C
fusion_effect=-.95*.2002*(Fs-F);convention_effect=-.95*(.2-.2002)*Fs
fuelF=F*(1.96e20/t['n_D0'])**2;fuelDelta=-.95*.2002*(fuelF-F)
required_rad=Hs-Cs;unresolved=R-required_rad
attrib={'entering_aux_MW':A,'paired_confinement_delta_MW':Cs-C,'fusion_power_delta_MW_at_model_fraction':fusion_effect,'alpha_fraction_delta_MW_at_source_fusion':convention_effect,'partial_source_conditioned_aux_MW':R+Cs-Hs,'explicit_unresolved_model_minus_ignition_inferred_radiation_MW':unresolved,'required_radiation_MW_inferred_not_independent':required_rad,'additive_identity_error_MW':(A+Cs-C+fusion_effect+convention_effect)-(R+Cs-Hs),'rounding_policy':'No physical uncertainty inferred; 2700 rounding interval unspecified.'}
assert abs(attrib['additive_identity_error_MW'])<1e-10
order={'W_only_delta_MW':dW,'tau_only_delta_MW':dt,'interaction_MW':interaction,'W_then_tau_deltas_MW':[dW,Cs-Ws/tau],'tau_then_W_deltas_MW':[dt,Cs-W/ts],'paired_delta_MW':Cs-C,'physical_scope':'Frozen accounting only, not independently realizable plasma interventions.'}
rounding={'assumption':'Extra nearest-rounding assumption at displayed decimal digits; no source uncertainty claim. Fusion2700 held exactly only for these illustrations.','W_over_tau_MW':[(Ws-.005)/(ts+.005),(Ws+.005)/(ts-.005)],'LCFS_flux_times_plasma_area_MW':[(1.18-.005)*(327-.5),(1.18+.005)*(327+.5)],'photon_flux_times_plasma_area_MW':[(.70-.005)*(327-.5),(.70+.005)*(327+.5)]}
rounding['forced_photon_balance_MW']=[rounding['W_over_tau_MW'][0]+rounding['photon_flux_times_plasma_area_MW'][0]-Hs,rounding['W_over_tau_MW'][1]+rounding['photon_flux_times_plasma_area_MW'][1]-Hs]
flux={'plasma_area_m2':327.,'LCFS_flux_product_MW':1.18*327,'photon_flux_product_MW':.70*327,'LCFS_minus_source_confinement_MW':1.18*327-Cs,'forced_photon_balance_MW':Cs+.70*327-Hs,'scope':'Incompatibility tests; plasma area is not established photon averaging area and flux products are not valid core loss substitutions.'}
result={'scope':'Reviewed finite arithmetic plus five fresh oracle controls against unchanged prior native study. No source-conditioned plant or ignition reproduction.','inputs':{'review_sha256':sha(D/'source-math-review.md'),'plan_sha256':sha(D/'diagnostic-plan.md'),'native_cases_sha256':sha(H/'results/native-cases.json'),'source_report_sha256':sha(D/'source-balance.md')},'verification':{'scalar_comparisons':n,'predicate_comparisons':m,'max_relative_error':worst,'relative_tolerance':1e-9,'absolute_tolerance':0,'errors':errors},'controls':checks,'balance_terms_MW':{'radiation':R,'brems':t['p_brems'],'tungsten':t['p_line'],'synchrotron':t['p_sync'],'confinement':C,'retained_alpha':Halpha,'auxiliary':A},'four_combinations':combos,'attribution':attrib,'W_tau_interactions':order,'fuel_only':{'source_peak_fuel_m3':1.96e20,'model_peak_fuel_m3':t['n_D0'],'conditioned_fusion_MW':fuelF,'alpha_only_aux_delta_MW':fuelDelta,'alpha_only_aux_MW':A+fuelDelta,'scope':'Printed fuel rescaling of fixed integral only; ash/energy/radiation not reclosed.'},'source_flux_compatibility':flux,'conditional_precision':rounding,'downstream_native_controls':[{'case':k,'downstream':by[k]['downstream'],'verdicts':rows[k]['verdicts']} for k in selected]}
(D/'diagnostics.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({'verification':result['verification'],'terms':result['balance_terms_MW'],'attribution':attrib,'W_tau_interactions':order,'fuel_only':result['fuel_only'],'precision':rounding},indent=2))
