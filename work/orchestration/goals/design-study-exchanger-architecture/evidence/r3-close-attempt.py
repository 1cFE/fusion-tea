"""Preserve the failed Round3 study honestly; never emit a successful study seal."""
import collections,gzip,hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
record=ROOT/'exploration/exchanger_architecture/thermal_requirements/studies/20260927-exchanger-thermal-comparison'
goal=ROOT/'work/orchestration/goals/design-study-exchanger-architecture'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (record/'attempt-snapshot.json').exists()
rows=read(record/'results/cases.json')['cases'];complete=[r for r in rows if r['state']=='completed'];failed=[r for r in rows if r['state']!='completed']
assert len(rows)==1277 and len(complete)==1275 and len(failed)==2
verification=read(record/'results/verification-attempt.json')
assert verification['outcome']=='pass'
axes=read(record/'axis-plan.json')['axes'];catalog=read(record/'results/constraint_catalog.json')
heads=[line for line in (record/'record.md').read_text().splitlines() if line.startswith('## ')]
assert len(heads)==17
fields=[]
fields.append('**Blocked attempt, 2026-09-27.** Executor: goal coordinator. Package exchanger_architecture_thermal_tea, Round3 executable cd16e8deb2f579e4cb1afcaf0fedbfc53498ba125783fbf8e17af14ffb4cbcc7. One architecture arm. The native execution prerequisite failed; this is not a completed or accepted comparison.')
fields.append('Owner intake is retained verbatim in owner-brief.md, owner-supplement-r2.md and owner-supplement-r3.md. Latest direction: “you are very intelligent. I trust your judgement. please make your best calls, document it, and proceed until you have strong study results.”\n\n[AGENT] The conditional N-R returns, six local30K minima, explicit A/B offers and search/sensitivity choices are documented in r3-study-contract.md and r3-cost-boundary.md. Their agent provenance is preserved.')
fields.append('The intended objective is net electricity and conditional LCOE, with complete thermal/equipment acceptance. Qualified channels are `aries_integrated_plant__plant_ledger__evaluate__net_electric` and `aries_integrated_plant__lifecycle_price__evaluate__lcoe`. **No accepted ranking or LCOE result is delivered by this failed attempt.** 1275 maps completed; two finite cases raised a numerical bypass-solver exception. Full stored outputs remain under results/.')
lines=['Constraint counts apply only to completed cases; the two execution failures have no native verdict. These counts are evidence, not a preferred-case certification.','| constraint_id | source_local_identity | satisfied | violated |','|---|---|---:|---:|']
for cid,e in sorted(catalog.items()):
 c=collections.Counter(r['verdicts'].get(cid,'missing') for r in complete)
 lines.append(f"| `{cid}` | `{e['source_local_identity']}` | {c['satisfied']} | {c['violated']} |")
fields.append('\n\n'.join(lines[:1])+'\n\n'+'\n'.join(lines[1:]))
fields.append('| Axis | Proposed | Judged | Reason |\n|---|---|---|---|\n'+'\n'.join(f"| {a['axis']} | {a['framing']} | unchanged, provisional | Native completeness prerequisite failed; no reframing justified. |" for a in axes))
parts=[]
for a in axes:
 parts.append(f"#### {a['axis']} — feasible structure (search framing)\n\n**Applies:** "+('yes; independent sampled structure remains in oracle-selection.json and oracle-scan-summary.json, but no accepted native boundary result follows from this attempt.' if a['framing']=='search' else 'not applicable — sensitivity-framed.'))
 parts.append(f"#### {a['axis']} — observed response (sensitivity framing)\n\n**Applies:** "+('yes; native cases and failure locations remain in results/cases.json. No uncertainty boundary or robustness claim is accepted.' if a['framing']=='sensitivity' else 'not applicable — search-framed.'))
fields.append('\n\n'.join(parts))
fields.append('| Axis | Entry key | Provenance |\n|---|---|---|\n'+'\n'.join(f"| {a['axis']} | `{k['key']}` | {k['provenance']} |" for a in axes for k in a['keys'])+'\n\nDeclared ties coordinate scenarios, not physical equality. Exact interpretations remain in axes.json and manifest.json.')
fields.append('All fifteen groups have `constraints_reachable`; no group reports `no_constraint_response`. This is only graph reachability. Monotonicity, cross-key physical identity and intra-module dependencies are not derivable. The agent still treats price assumptions as unresisted procurement/fuel sensitivities, authorized by delegated owner judgment. Missing procurement, source sustainment and control/hydraulic qualification remain explicit in the contract.')
fields.append('All study preflight gates pass in preparation/preflight.json. The model integration passed all ten gates, copied in results/integration_return_used.json. Those prerequisites did not guarantee complete execution over the refined candidate set.')
fields.append('Stock strict loader, PreparedEvaluator, StudyDefinition, PreparedListStrategy, StudyRunner and StudyStore. Coordinated full input maps require the direct-API definition. Glue ledger: none. results/export-proof.json preserves exact full-map matching and unchanged native export evidence. The exporter correctly rejects the incomplete execution.')
fields.append('The engineered window was selected from an independent scan of91,234 maps, retaining all697 known development passing seeds and refining every observed component. Two matched catalogues share flow freedom; the network adds a supplied split. Final selected resolutions meet0.2MW/0.1USD2004-per-MWh stability targets, with final split spacing as fine as0.00025 and final flow probes0.00625kg/s. No sampled passing outer edge remains. The1kg/s negative series check still found no offer-B pass at1650MW. These are retained scouting results, not global proofs or accepted native architecture outcomes. The exact scan/selection/proposals and exclusions are retained, with lossless compression described below.')
fields.append('Single executable fingerprint; cross-fingerprint correlation is not applicable inside this attempt. The next round must explicitly correlate the same1277 complete input maps against a corrected executable; it cannot overwrite this store or silently retry this pin.')
fields.append('results/verification-attempt.json reports numeric PASS for every completed row:1275 of1277 total,435 independent channels and35 predicates each, unchanged1e-9 relative and declared absolute classes. The two failed rows are not sampled by the stock verifier; this is not an all-point verification pass. Independently recomputed failed states are finite and satisfy the unchanged engineering predicates. Failure checks and later repair review belong to WI-097; the next study must verify all1277 executions.')
fields.append('Source, design, preparation and implementation reviews passed within their declared scopes. r3-failure-review.md approves retaining this attempt and using Round4 for unchanged-meaning repair. A numerical remedy requires its own independent review. No ranking is approved by the partial verification receipt.')
fields.append(f"| Finding id | Kind | Finding | Disposition | Home |\n|---|---|---|---|---|\n| {record.name}#1 | model | Two finite supplied maps fail native bypass convergence; complete study execution is unmet. | model fix: Round4 T-007 reviewed stable evaluation and exact-map replay, pending | work/active/WI-097_exchanger-thermal-requirements |")
fields.append('`attempt-snapshot.json` hashes the blocked attempt, archived original executable, original source bytes, retained native store and completed-case verification. A successful-study snapshot is deliberately absent because execution failed. It is a failure-preservation record, not a completed-study seal. lossless-compression.json maps compressed files to exact original byte hashes; decompressing restores every original scan/proposal/checkpoint byte.')
fields.append('No accepted preferred architecture, complete native execution/verification, completed-study snapshot, vendor price qualification, actuator rating, piping design, source sustainment, breeding/fuel-supply model or plant recommendation. Those omissions are explicit; the preserved two numerical failures cannot be treated as engineering rejections.')
(record/'record.md').write_text('# Blocked study attempt — thermally consistent exchanger comparison\n\n'+'\n\n'.join(h+'\n\n'+f for h,f in zip(heads,fields))+'\n')
for name in ('r3-study-contract.md','r3-cost-boundary.md','r3-protocol-review.md','r3-failure-review.md'):
 shutil.copyfile(goal/'evidence'/name,record/name)
for name in ('r3-prepare-study.py','r3-refine-study.py','r3-finalize-proposals.py','r3-close-attempt.py'):
 target=record/'results/preparation-sources'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(goal/'evidence'/name,target)
compressed=[]
paths=[record/name for name in ('oracle-scan.json','candidate-ledger.json','proposed-points-initial.json','proposed-points-refined.json')]+sorted((record/'scan-checkpoints').glob('*.json'))
for path in paths:
 raw=path.read_bytes();target=path.with_suffix(path.suffix+'.gz')
 with target.open('wb') as stream:
  with gzip.GzipFile(filename='',mode='wb',fileobj=stream,mtime=0,compresslevel=6) as zipped:zipped.write(raw)
 assert gzip.decompress(target.read_bytes())==raw
 compressed.append({'original':path.relative_to(record).as_posix(),'original_sha256':hashlib.sha256(raw).hexdigest(),'compressed':target.relative_to(record).as_posix(),'compressed_sha256':sha(target),'original_bytes':len(raw)})
 path.unlink()
(record/'lossless-compression.json').write_text(json.dumps({'files':compressed},indent=2)+'\n')
artifacts=[{'path':p.relative_to(record).as_posix(),'sha256':sha(p)} for p in sorted(record.rglob('*')) if p.is_file() and p.name not in ('record.md','attempt-snapshot.json') and '__pycache__' not in p.parts and 'pkg_link' not in p.parts and p.suffix!='.pyc' and not p.name.endswith(('-wal','-shm'))]
(record/'attempt-snapshot.json').write_text(json.dumps({'schema':'blocked-study-attempt/v1','study_id':record.name,'status':'blocked_execution','cases_total':1277,'cases_completed':1275,'failed_case_ids':[r['candidate_id'] for r in failed],'verification_scope':'all1275 completed rows only,435channels/35predicates; full1277execution gate failed','executable_fingerprint':'cd16e8deb2f579e4cb1afcaf0fedbfc53498ba125783fbf8e17af14ffb4cbcc7','artifacts':artifacts},indent=2)+'\n')
log=record.parent/'DISCOVERY_LOG.md'
if not log.exists():log.write_text('# Discovery log — exchanger thermal comparison\n\n| Date | Kind | Record | Finding | Disposition | Home |\n|---|---|---|---|---|---|\n')
with log.open('a') as f:f.write(f'| 2026-09-27 | model | {record.name}#1 | Two finite maps fail native bypass convergence. | model fix: Round4 T-007; unchanged maps, requirements and verification contract | work/active/WI-097_exchanger-thermal-requirements |\n')
print(json.dumps({'artifacts':len(artifacts),'attempt_snapshot_sha256':sha(record/'attempt-snapshot.json'),'compressed_files':len(compressed)}))
