"""Write the complete reviewable study argument from retained result artifacts."""
import hashlib
import json
from pathlib import Path

H=Path(__file__).resolve().parents[1]
R=H/'results'
P='stellarator_09__stellaris__'
read=lambda p:json.loads(p.read_text())
a=read(R/'analysis.json')
rows=a['cases'];byid={r['proposal_id']:r for r in rows}
props=read(H/'preparation/proposals.json')
axes=read(H/'axes.json')['groups']
ind={g['axis']:g for g in read(H/'indicators.json')['groups']}
catalog=read(R/'predicate-catalog.json')
verification=read(R/'verification_summary.json')
pre=read(R/'preflight_results.json')
snapshot=H/'snapshot.json'
sid=H.name
findings=[
    ('model','The low source profile lowers the target peak but increases uncaptured non-radiated load, while target capital and plant/loop response are unchanged at fixed plasma coordinates.','Conditional transport sensitivity; wall interception and geometry-specific engineering/cost consequences remain unrepresented.'),
    ('model','Changing major radius at held transport changes heating and conditional peak response; neither equivalent area nor the radius shadow identifies physical wetted area or independent peaking.','Geometry transfer remains unresolved; area/peaking gains are conditional requirements, not design levers.'),
    ('model','Greater total radiation can make the non-radiated target predicate pass without changing plant heat, primary-loop demand or target capital at a held plasma state.','Radiation-control capability, total target radiative deposition and wall accommodation are not qualified.'),
    ('model','Two evaluated points have negative auxiliary demand and power_account_valid=0; they remain numerical failed controls.','Both retained after coordinator release and excluded from physical heat-load-gain interpretation.'),
    ('model','No selected point satisfies all20 predicates, and every entering scalar/predicate comparison remains unchanged.','Preserve the joint study bounded negative; these diagnostic source/radiation sensitivities do not regrade it or establish global infeasibility.'),
]
home='work/orchestration/goals/divertor-peak-heat-load'
finding_rows=[{'id':f'{sid}#{n}','kind':kind,'finding':finding,'disposition':disposition,'home':home} for n,(kind,finding,disposition) in enumerate(findings,1)]
(H/'preparation/findings.json').write_text(json.dumps(finding_rows,indent=2)+'\n')
# Only create first sightings. Never rewrite any existing discovery row.
log=H.parent/'DISCOVERY_LOG.md'
existing=log.read_text()
new=[]
for f in finding_rows:
    line=f"| 2026-09-16 | {f['kind']} | {f['id']} | {f['finding']} | {f['disposition']} | {f['home']} |"
    if f['id'] not in existing: new.append(line)
if new:
    with log.open('a') as stream:stream.write('\n'+'\n'.join(new)+'\n')

out=[]
def para(s=''):out.append(s+'\n')
def heading(n,title):para(f'## {n}. {title}')
def table(headers,values):
    para('| '+' | '.join(headers)+' |')
    para('| '+' | '.join(['---']*len(headers))+' |')
    for values_row in values:para('| '+' | '.join(str(x).replace('|','/') for x in values_row)+' |')
    para()

heading(1,'Study header')
para(f'- **Study id:** {sid}\n- **Package:** stellarator_tea\n- **Date executed:** 2026-09-16 UTC\n- **Executor:** Codex delegated study executor /root/divertor_research\n- **Mode:** execute\n- **Arms:** arm-native; one prepared-list study with diagnostic families')
para('The date-prefixed study ID was assigned by the coordinator on the owner’s local date. This is the WI-065 capture-account package at the candidate recorded in snapshot.json; it adds accounting diagnostics while preserving the existing peak and predicates.')
heading(2,'Intake')
for quote in ['A bounded study revisits the reference and selected joint-sizing rejection cases, separating geometry changes from deposition/peaking assumptions.','Attribute changes against the entering package. Report divertor feasibility separately from all-predicate feasibility. Retain failed cases and preserve the joint study’s bounded negative conclusion unless a documented model correction or physical design change alters it.','If those consequences cannot be represented, label the change as a conditional requirement or sensitivity rather than a free design improvement.']:
    para('[OWNER-VERBATIM] “'+quote+'”')
para('[INHERITED: coordinator] Five exact entering controls, uncrossed paired-source/radiation variants, six radius samples and a signed-negative control make the27-point sample. The coordinator’s scoped instructions and owner authority are captured in preparation/study-brief.md and preparation/goal-at-authority.md. protocol.md records the executor’s framing. No acceptance limit, physical-area input or independent peaking parameter was varied.')
heading(3,'Objective and result')
para(f'**LCOE channel:** `{P}lcoe_calc__lcoe`. All27 cases completed. The legacy reference gives {byid["reference"]["quantities"]["LCOE_dollars_MWh"]:.12g} dollars/MWh. The evaluated diagnostic range is {min(r["quantities"]["LCOE_dollars_MWh"] for r in rows):.12g}–{max(r["quantities"]["LCOE_dollars_MWh"] for r in rows):.12g} dollars/MWh, including invalid-account cases. No feasible minimum is claimed because none passes all20 predicates. Sources: results/native-cases.json and results/analysis.json.')
para('Paired source transport and total-radiation sensitivities leave LCOE unchanged at each held plasma/magnet point. They change the target heat account without representing added engineering or control costs. The existing target predicate alone is not physical divertor qualification: the account must also be valid with an active source case, and neither peak includes total radiative surface deposition.')
table(['Named control','q peak MW/m²','q shadow MW/m²','account valid','LCOE $/MWh','Failed predicates'],[(r['proposal_id'],f"{r['account']['q_target_peak']:.9g}",f"{r['account']['q_target_peak_area_scaled']:.9g}",int(r['account']['power_account_valid']),f"{r['quantities']['LCOE_dollars_MWh']:.9g}",', '.join(r['violated'])) for r in rows if r['family'] in ['base-control','invalid-account-control']])
para('Every case’s H, core/edge/total radiation, S,N,D,U,Aeq, active/valid flags, both peaks, signed margin, target capital, plant heat, loop demand/capacity, field/current/fit and LCOE are in results/case-summary.csv. Conditional above-limit power/area/radiation requirements are in the same file and results/analysis.json. qshadow is a conditional peak, never average heat flux.')
heading(4,'Constraint outcomes')
para(f"The exact native predicate reports {a['overall']['divertor_predicate_passes']} divertor passes; the same {a['overall']['divertor_account_supported_passes']} also have valid active accounts. There are {a['overall']['invalid_accounts']} invalid accounts and {a['overall']['all20_passes']} all-predicate passes. These are non-radiated transport checks, not total surface thermal qualification. Every qualified constraint identity is retained below and per point in results/native-cases.json; failure locations are joined in results/case-summary.csv.")
table(['constraint_id','source_local_identity','Statuses over27','Location evidence'],[(cid,e['source_local_identity'],', '.join(f'{k}: {v}' for k,v in a['predicate_outcomes'][cid]['counts'].items()),'results/native-cases.json; case-summary.csv') for cid,e in catalog.items()])
heading(5,'Framing')
para('**As proposed at intake and judged after the run:** every declared group remains sensitivity-framed. No framing changed. This finite diagnostic selection does not owe a 5–95% all-predicate feasible fraction and does not establish a feasible boundary. Context choices that co-vary are controls, not independently identified causal effects.')
table(['Axis','Proposed','Judged','Changed?','Reason'],[(g['axis'],'sensitivity','sensitivity','no','Matched diagnostic contrasts or held context; no optimum/boundary claim.') for g in axes])
heading(6,'Per-axis account')
for g in axes:
    axis=g['axis'];keys=[k['key'] for k in g['keys']];values={k:sorted({r['point'][k] for r in props}) for k in keys}
    para(f'#### {axis} — feasible structure (search framing)')
    para('**Applies:** not applicable; this group is sensitivity-framed.')
    para(f'#### {axis} — observed response (sensitivity framing)')
    if axis=='paired-source-profile':text='At each of five held base controls, the low profile lowers peak flux to5/9.5 of its high-profile value and increases uncaptured heat. Deposited power and equivalent area change together. Cost, plant heat, loop demand and other predicates remain unchanged. Source-profile family cases in results/analysis.json locate all violations.'
    elif axis=='divertor__f_rad_total':text='Changing total radiation from.90 to.88/.92 raises/lowers the peak by20% at each held base state. Radiation moves heat between account destinations without changing plant heat, loop demand or cost. The reduction is a conditional radiation-control requirement; radiation-sensitivity family cases retain every other failure.'
    elif axis=='plasma__R':text='The six radius variants change heating and multiple plant/magnet predicates. Larger radius raises the fixed-target peak in all three sampled pairs. The R12.9 variant of the field-passing rejection has negative auxiliary demand and an invalid account; it remains a numerical diagnostic only. Radius-sensitivity family cases locate all failures. The radius shadow gives no demonstrated physical-area response.'
    elif all(len(v)==1 for v in values.values()):text='Held context only; this record measures no independent response for this group. Complete values and provenance remain in axes.json and snapshot.json. Its presence makes proposals explicit, not a tested sensitivity direction.'
    else:text='Varies only between declared context controls and is not isolated from other changed choices. Results/analysis.json and preparation/proposals.json preserve each combination and every failure. No separate causal response is inferred from co-variation.'
    para('**Applies:** yes. '+text+' No boundary claim is made.')
heading(7,'Axis groups')
para('axes.json declares every complete entry-key group and provenance. The paired source case is an explicit coordinator tie between metadata values, not a claim that the two keys name one physical scalar. All other groups are public-attribute fan-outs. The one physical radius already fans through model composition; there is no retired magnet-radius injection. Held field/current/fit/loop/heat limits remain model defaults. Source-profile and geometry application limits are preserved in preparation/source-review.md and source-evidence/.')
table(['Axis','Entry key','Provenance','Note'],[(g['axis'],k['key'],k['provenance'],g['note']) for g in axes for k in g['keys']])
heading(8,'Indicators and rulings')
table(['Axis','Indicator','Ruling','Note'],[(g['axis'],'constraints_reachable','Coordinator released sensitivity protocol','possible paths: '+str(len(ind[g['axis']]['constraints_reachable']))) for g in axes])
para('No group reported no_constraint_response, so the owner-reserved ruling and mandatory missing-pushback finding for that indicator were not triggered. Physical wetted area and independent peaking were declined at scope formation because no supported native inputs exist; no fictitious key or failed indicator run was substituted. Their missing independent representation is finding#2.')
para('**Not derivable:** monotonicity of channels in an axis, physical identity across different entry keys and intra-module operand dependency. constraints_reachable means a possible graph path, not observed response. unresisted is an agent judgment and is not reported here as a tool result. Full non-subset indicators are in indicators.json; release is in preparation/execution-release.json.')
heading(9,'Preflight results')
para('The exact manifest baseline was executed before preflight. Every mechanical gate passed. results/package_identity.json and results/baseline_result.json are the identity/headline evidence; results/preflight_results.json records each gate. The suffix-sibling scan is warning-only, and its exact results are retained.')
gates=pre.get('gates',{})
if isinstance(gates,dict):table(['Gate','Outcome','Evidence'],[(name,str(result.get('outcome',result.get('status','recorded'))),'results/preflight_results.json') for name,result in gates.items()])
elif isinstance(gates,list):table(['Gate','Outcome','Evidence'],[(g.get('gate',g.get('name','gate')),g.get('outcome',g.get('status','recorded')),'results/preflight_results.json') for g in gates])
para('The two initial command attempts failed on imports before evaluation and were corrected by using the documented repository+TEAx import paths. preparation/runtime-command.md records them. The successful run retained the inherited boolean-serialization warning; no runtime or model repair was made.')
heading(10,'Execution route and why')
para('**Route:** study-local direct API, stock PreparedListStrategy through study_route.run_points. A prepared list preserves coordinated source pairs and uncrossed radiation/radius scenarios. The loader, baseline and preflight exercised this route before the27 study points. **Glue ledger: none.** No adapter or supplied physical quantity exists on this route. study.py is the definition; results/entry-models.json captures the complete actual entry-model map.')
para('The native SQLite study store and its content-addressed evidence are retained under results/study/_work/. The manifest baseline has its own store under results/_work/. Store compatibility, coverage, inputs, outputs and per-constraint reports were checked by execution/check_artifacts.py; results/native-store-check.json contains the pre-freeze custody result. No hand-rolled native sweep was used.')
heading(11,'Study definition and window provenance')
para('The independent current oracle scanned all proposed diagnostic points after baseline/preflight. Every candidate evaluated, so no refinement, masking or replacement was needed. The window was adopted after reading results/oracle-scan.json and the coordinator’s explicit release to retain the second invalid account. reviews/window-selection.md records that decision. Bounds and provenance are snapshot values; the window is engineered for attribution, not sourced machine admissibility. With no all-predicate-feasible anchor, no edge or constrained region is claimed caught.')
para('The held radial stack supplies the geometric mask R>a+2.25m; every selected point satisfies it, so it removes no point. All rejected predicates and both invalid accounts remain in the record. The sample cap was40, with27 unique study points plus one separately required manifest-baseline execution. No additional native refinement point ran.')
heading(12,'Cross-fingerprint correlation and what it means')
para('One current native arm uses one package fingerprint and compatibility tuple, so no cross-arm native-store correlation is needed. Entering attribution separately uses the frozen f76 oracle and original contracts/inputs in preparation/entering/. The two oracle dependencies are explicitly loaded in a separate process. Only target_capture_fraction is removed from old-oracle inputs. All20 qualified predicate IDs and predicate_ir expressions are unchanged; the isolated comparison verifies this before evaluation.')
para('Every one of the218 entering mapped outputs and all20 predicates agrees at each of27 matched coordinates. results/comparison-entering.json records zero changed channels and zero predicate flips. Eight new accounting outputs are current-only. This establishes arithmetic preservation on these points, not equivalent engineering authority across geometries. The original native controls are captured separately; this study does not claim old-native execution for its all-point attribution. Finance-helper bytes match the entering commit.')
heading(13,'Verification')
para('All-point comparison passed:6102 mapped scalar comparisons and540 exact predicate comparisons. Generic verification separately passed with stratification over observed verdict combinations; its sampled-case IDs, coverage and command are in results/verification_summary.json. Tolerances, source digests and sample strategy are snapshot values. No exact-sign discrepancy occurred in the selected sample. The known exact-current-boundary case is not in it.')
para('Verification covers the current oracle’s226 mapped scalars, with all242 native numeric outputs retained. The16 unmapped native channels are explicitly listed in results/oracle-all-points.json and are not independent-oracle claims. The oracle independently recomputes equations but shares audited assumptions; it does not validate those assumptions against operating hardware. Held values identical by construction, a derived Aeq identity, and conservation residuals are internal consistency evidence, not measured physical area, geometry or material qualification.')
heading(14,'Review outcomes')
table(['Lens','Verdict','Disposition'],[('Original source/math','Prior independent source-review.md applicable','Copied in preparation/; source pairs, equivalent-area identity and geometry/radiation limits unchanged.'),('WI-065 implementation','Independent PASS within its recorded validation limits','preparation/implementation-review.md; reused for unchanged implementation, not study certification.'),('Protocol/indicators','Coordinator released','reviews/preexecution-check.md; no no_constraint_response group.'),('Post-scan invalid account','Coordinator released retention','reviews/window-selection.md; exclude both invalid cases from physical gain interpretation.'),('Study arithmetic and custody','Executor checks passed','All-point/generic/store artifacts; not an independent review.'),('Final study/goal meaning','Pending coordinator-arranged independent review','This ready-to-freeze record does not self-certify closure.')])
heading(15,'Findings')
table(['Id','Kind','Finding','Disposition','Home'],[(f['id'],f['kind'],f['finding'],f['disposition'],f['home']) for f in finding_rows])
para('These five first sightings join the append-only discovery log by the exact IDs above. The coordinator owns later joined disposition rows and all existing findings. No earlier row was edited.')
heading(16,'Snapshot')
para('- **File:** snapshot.json\n- **Schema version:** 1\n- **sha256:** '+(hashlib.sha256(snapshot.read_bytes()).hexdigest() if snapshot.exists() else 'Pending final artifact snapshot; executor will resolve before freeze.'))
para('The snapshot resolves manifest content, all three required fingerprints, candidate pin, complete entry-model map, stock store compatibility tuple, verification/tool identities and artifact digests. Content needed to read this study is captured inside this directory; external paths in provenance identify origin only. The raw native stores and evidence are included in the commit inventory; symlinked live package trees and runtime caches are excluded.')
heading(17,'What this record does not contain')
para('No physical wetted-area measurement, separate peaking factor, per-target sharing map, qualified radius transfer, total radiative target/first-wall deposition map, neutral exhaust solution, breeding accommodation, target cooling/support/manufacturing assessment or target/control cost response. No global optimum, universal infeasibility claim, relaxed heat-flux threshold, broad replay of the joint study or old-native27-point rerun. No thermal qualification at either invalid account. The preserved high/low source cases refer to a resonant island divertor, not a non-resonant topology. No new insight approval or goal closure is implied.')
para('An executor synthesis is intentionally absent until the coordinator commits the evidence. The final independent review and any coordinator dispositions are later records. All mathematical and custody facts needed for that review are present in the retained results and preparation artifacts.')
(H/'record.md').write_text('\n'.join(out))
print('Wrote17-section record and',len(new),'new discovery rows.')
