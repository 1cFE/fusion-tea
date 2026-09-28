"""Write the narrative for the blocked attempt, retaining the owner's intake verbatim."""
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'exploration/component_alternatives/studies/20260926-design-study-component-alternatives'
read=lambda path:json.loads(path.read_text())
s=(P/'record.md').read_text()
intake=s.split('## 2. Intake\n',1)[1].split('## 3. Objective',1)[0]
cases=read(P/'results/cases.json')['cases'];constraints=read(P/'results/constraint-summary.json');axes=read(P/'results/axis-assessment.json');groups=read(P/'axes.json')['groups'];pre=read(P/'preparation/preflight_results.json');window=read(P/'window.json')
findings=[
 ('model','Native cooler stopping accuracy exceeds the numerical verification tolerance in six cases, including two predicate-passing sensitivities.','Blocked; independent review confirms native accuracy dependency. No repair or waiver in this run.','work/orchestration/goals/design-study-component-alternatives/evidence/verification-failure-review.md'),
 ('model','Equipment prices, installed scope, service allowances and replacement costs remain conditional; hypothetical quote changes can alter the comparison.','Declared seam; withheld procurement recommendation and retained cost-correction frontier.','work/orchestration/goals/design-study-component-alternatives/comparison-contract.md'),
 ('model','The fixed steam turbine offer and tested gas choices have unequal supported operating freedom.','Declared seam; comparison is selected steam versus tested Brayton offers only.','work/active/WI-096_matched-conversion-subsystems/design.md'),
 ('model','Controller pressure service, machine efficiencies and detailed site hydraulics lack qualification.','Declared seam; modeled checks do not establish operating or procurement qualification.','work/active/WI-096_matched-conversion-subsystems/design.md'),
 ('model','Only 14 of 375 gas catalog combinations pass all checks (3.73%); finite-water property/root limits reject many combinations.','Declared seam; H1 search feasible-fraction hypothesis is falsified for this catalog. No continuous boundary inferred.','exploration/component_alternatives/studies/20260926-design-study-component-alternatives/results/constraint-summary.json'),
 ('process','Direct study launch initially lacked the documented TEAx import path and stopped before evaluation.','Resolved operationally; same points and package run with the documented environment.','exploration/component_alternatives/studies/20260926-design-study-component-alternatives/preparation/execution-attempt1/failure.txt'),
 ('process','Reachable-constraint indicators on financial axes do not prove physical resistance to price assumptions.','Declared seam; all financial changes remain sensitivity-framed, with no optimization claim.','exploration/component_alternatives/studies/20260926-design-study-component-alternatives/results/axis-assessment.json'),
]
parts=['# Selected steam offer versus tested Brayton offers\n\n**Blocked at numerical verification.** This sealed attempt preserves executed evidence; it is not a released economic comparison. Formal goal and work-item closure remain owner-held.\n',
'## 1. Study header\n\n- **Study id:** `'+P.name+'`\n- **Package:** `component_alternatives_tea`\n- **Date executed:** 2026-09-26\n- **Executor:** Goal coordinator `/root`\n- **Mode:** execute; stopped at verification\n- **Arm:** `arm-matched-offers`\n',
'## 2. Intake\n'+intake,
'''## 3. Objective and result

The native objectives are `component_alternatives__plant__steam_ledger__evaluate__cost_per_net_MWh` and `component_alternatives__plant__gas_ledger__evaluate__cost_per_net_MWh`, in USD2025 per net MWh. These include the conversion subsystem and its connecting equipment, with common finance and source conditions.

All 498 distinct points completed; 83 pass every implemented predicate. Full numerical verification failed. Six cases disagree beyond predeclared tolerances, including two otherwise-passing efficiency sensitivities. Native output and cost plots are diagnostic, unreleased results. They cannot establish a completed economic ranking.

`results/cases.json` and `results/cases.csv` retain every input, output and predicate. `results/verification-diagnostics.json` identifies the numerical qualifications by case. No failed point was deleted.
''',
'## 4. Constraint outcomes\n\nAll 84 executing checks are listed below. Counts refer to the 498 native cases. Zero indeterminate verdicts occurred. Independent diagnostic re-derivation agrees with every predicate, but that does not override six numerical failures. Case attribution is in `results/constraint-summary.json`.\n\n| `constraint_id` | `source_local_identity` | Satisfied | Violated |\n|---|---|---:|---:|\n'+''.join(f"| `{r['constraint_id']}` | `{r['source_local_identity']}` | {r['counts'].get('satisfied',0)} | {r['counts'].get('violated',0)} |\n" for r in constraints),
'## 5. Framing\n\n[AGENT] Proposed framings are retained as judged; none changed after execution. Search means selection from the finite explicit catalog, not continuous optimization. Sensitivities remain hypothetical scenarios. Thirty-nine attributes varied; four traced directions remained declined.\n\n| Axis | Proposed | Judged | Executed variation |\n|---|---|---|---|\n'+''.join(f"| `{a['axis']}` | {a['framing_proposed']} | {a['framing_judged']} | {'yes' if a['executed'] else 'declined'} |\n" for a in axes),
'## 6. Per-axis account\n\n`results/axis-assessment.json` records every tested value, its case identities and the number satisfying all implemented checks. The following compact account uses the same order as those values. Coordinated offers vary several attributes together; grouped counts do not identify an isolated causal effect. The comparison and sensitivity figures use matched cases and carry the verification block.\n\n| Axis | Tested values | Predicate-passing / evaluated at each value | Account |\n|---|---|---|---|\n'+''.join(f"| `{a['axis']}` | {', '.join('/'.join(f'{v:g}' for v in level) for level in a['tested_values'])} | {', '.join(str(x['satisfying_all_checks'])+'/'+str(x['cases']) for x in a['level_outcomes'])} | {a['account']} |\n" for a in axes)+ '\nThe gas catalog has 14 passing cases of 375, below the policy H1 search band of 5–95%. This is a negative result for that hypothesis, not evidence of an equality over chosen source/ratio inputs. Cooler property/root validity and source/capacity requirements account for the failures. Steam connector offers pass in 21 of 72 scans. The 54 sensitivity/controller proposals yield 51 passing cases; three undersized gas bypass offers fail. All scan cases evaluated, and only three exact duplicates were removed from native execution with aliases retained.\n',
'## 7. Axis groups\n\nEvery axis is a single SysML attribute with its complete emitted entry-key group. `axes.json` retains all 43 groups and provenance. Equal compressor ratios and common financial choices are coordinated scenario selections, not inferred physical identities.\n\n| Axis | Complete key | Provenance |\n|---|---|---|\n'+''.join(f"| `{a['axis']}` | `{a['keys'][0]['key']}` | {a['keys'][0]['provenance']} |\n" for a in groups),
'''## 8. Indicators and rulings

All 43 proposed axes, including the four declined directions, were traced. Every result is `constraints_reachable`; no `no_constraint_response` axis exists, no subset was used, and no new owner ruling is required. `indicators.json` preserves exact paths and evidence.

Not derivable: monotonicity, identity of the same physical quantity across differing names, and intra-module operand dependency. A reachable constraint is a possible graph path, not evidence that it responds. Financial assumptions remain sensitivity-framed under the owner's requested price/fuel sensitivity. Their missing procurement qualification is a finding, even though the graph reports reachability.
''',
'## 9. Preflight results\n\nAll gates ran on the promoted package. `preparation/package_identity.json` and `preparation/baseline_result.json` are local copies of the exact gate inputs; their digests are in `preparation/preflight_results.json`. `preparation/integration_return.json` preserves all ten integration gates.\n\n| Gate | Outcome | Detail |\n|---|---|---|\n'+''.join(f"| {g['gate']} | {g['status']} | {str(g.get('detail','')).replace('|','/')} |\n" for g in pre['gates'])+'\nThe suffix scan has 12 advisory warnings. They are different attributes (inactive branch UA, primary loop count and controller-loss ratings), not missing fan-out copies. The declared groups map the actual authored attributes; no sweep key was silently tied to those siblings.\n',
'''## 10. Execution route and why

The study-local direct API uses stock `StudyRunner` and `PreparedListStrategy` because the list combines explicit coordinated equipment offers with selected-anchor sensitivities. The strict package loader, evaluator, store and query retain the native lifecycle. The matching physical calculations live in the model. Glue ledger: none; no runtime adapter.

The first launch lacked the documented TEAx import root and stopped before creating a native store. `preparation/execution-attempt1/` preserves that attempt. Retry 1 used the documented environment with the same 498 points and package. `results/execution-context.json` records exact commands and revision. No physical or metadata change was needed for the retry.
''',
'''## 11. Study definition and window provenance

The window is engineered, not a qualified equipment envelope. `proposals.py` in the archived sources composes independently chosen inputs without a physical root or equipment sizing calculation. Core, steam and sensitivity oracle scans all completed before native execution. Every evaluated offer, including engineering failures, entered the native list; three exact duplicate points have explicit aliases in `window.json`. No body refusal occurred in these scans. Earlier development property refusals remain in the WI-096 evidence.

The best tested passing gas offer at each source anchored the steam connector scan. The least-cost passing connector then anchored the sensitivities. This is discrete offer selection; it does not establish equal optimization of the technologies. The common 14-circuit steam curve remains visible separately. The scan fixes a finite list, not a continuous feasible boundary or global optimum. Every tested value and generating choice is retained in the proposal files and snapshot window.
''',
'''## 12. Cross-fingerprint correlation and what it means

Single fingerprint: no cross-arm correlation needed. Every native case uses the same executable identity and model contract. Earlier development diagnostics and prior goal studies are historical evidence; none is merged into this store or treated as a matched main-study observation.
''',
'''## 13. Verification

**Failed; dependent completion stopped.** The stock verifier requested all 498 cases and stopped at its first numerical disagreement. `results/verification-attempt1-failure.json` retains the exact case and outputs. `results/verification-blocker.json` records the disposition. There is no successful `verification_summary.json` for this study.

Post-failure diagnostics compared 872 channels and independently re-derived all 84 predicates in each case. Six cases exceed unchanged predeclared tolerances; zero predicates disagree. These diagnostics inventory the failure and do not replace the stock verifier's release gate. Four solver iteration counts are diagnostic-only and excluded. Chosen inputs, assumed prices, imposed pressure service and supplied property data are common premises, not independently validated scientific facts.

The independent reviewer used a 60-digit cooler calculation at the exact native gas tuple. It agrees with the oracle; the native cooler's residual stopping rule permits amplified flow and pump error at a small water temperature rise. No oracle error was demonstrated. Required native numerical repair/new executable revalidation or new tolerance authority is outside this continuation. No model, tolerance or case selection was changed after the failure.
''',
'''## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Fourth design, continuing independent reviewer | PASS | Reviewed physical roles, MR-7, five substantive bodies and one newly written iterative cooler family; scope authorized. |
| Implemented integration, same non-author reviewer | PASS at WI-096 `29dcb5d8` | Reused exact implementation, 17-case numerical and predicate evidence; this does not cover all main-study points. |
| Stock integration seam | CANDIDATE, ten gates pass | Exact promoted identity retained. |
| Full study verification | FAIL | Six numerical mismatch cases identified; none removed. |
| Independent failure assessment | FINDINGS / stop | Accurate independent cooler root identifies native numerical accuracy dependency. |

Review artifacts and the original design/spec are copied under `results/sources/` at sealing. Final assurance of the blocked answer is recorded in the goal trail; it cannot convert this failure into a verification pass.
''',
'## 15. Findings\n\nFirst sightings are joined to `DISCOVERY_LOG.md` by the following IDs. Every finding has a retained home; future model work remains owner-held.\n\n| Id | Kind | Finding | Disposition | Home |\n|---|---|---|---|---|\n'+''.join(f"| `{P.name}#{i}` | {kind} | {finding} | {disp} | `{home}` |\n" for i,(kind,finding,disp,home) in enumerate(findings,1)),
'''## 16. Snapshot

- **File:** `snapshot.json`
- **Status:** blocked-at-verification evidence seal; `released: false`
- **Schema version:** 1 with explicit failed-verification fields
- **SHA256:** recorded after sealing in the final assurance and goal replay

The snapshot preserves the actual failure. Its verification summary digest is null because no passing summary exists; the failure and full diagnostic artifacts have their own digests. This is an explicit blocked-record exception in shape, not a policy exception permitting execution or release.
''',
'''## 17. What this record does not contain

There is no passing full-study verification summary, released economic recommendation, qualified procurement quotation, validated machinery map, detailed controller/site hydraulic design, reactor/fuel price model, or equally optimized technology comparison. The sealed runtime and independent oracle are included; their external licensed toolchain and Python environment must still be provided for replay.

Historical source audits, rejected designs and earlier failed native attempts remain in the goal and WI-096 history. This record copies the specific reviewed design, implementation, failure evidence and executed package needed to identify this attempt; it does not duplicate the entire project history. Formal closure is absent because the owner retains it.
''']
(P/'record.md').write_text('\n'.join(parts))
log=P.parent/'DISCOVERY_LOG.md'
assert not log.exists(), 'preserve existing discovery log'
log.write_text('# Component alternatives study discoveries\n\n| Date | Kind | Record | Finding | Disposition | Home |\n|---|---|---|---|---|---|\n'+''.join(f'| 2026-09-26 | `{kind}` | `{P.name}#{i}` | {finding} | {disp} | `{home}` |\n' for i,(kind,finding,disp,home) in enumerate(findings,1)))
print('Blocked record and seven discovery rows written.')
