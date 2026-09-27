"""Write the seventeen-section record from verified stored evidence and review."""
from pathlib import Path
import argparse, hashlib, json


def load(path): return json.loads(path.read_text())

def write(record):
    results=record/'results'; presentation=results/'presentation'
    verification=load(results/'verification_summary.json')
    assert verification['outcome']=='pass'
    assert len(verification['channels_checked'])==1192 and len(verification['constraints_rederived'])==125
    data=load(presentation/'native-ranking.json')
    counts=load(results/'constraint-summary.json')
    axes=load(results/'axis-assessment.json')['groups']
    groups=load(record/'axes.json')['groups']
    scan=load(record/'preparation/summary.json')
    window=load(record/'window.json')
    integration=load(record/'integration/integration_return.json')
    assert integration['class']=='CANDIDATE'
    assert scan['unique_complete_points']==data['native_cases']==counts['cases']
    assert sum(store['sampling']['sampled_rows'] for store in verification['stores'])==counts['cases']
    reviews=record/'supporting/final-results-review.md'
    assert reviews.exists() and 'Verdict: pass' in reviews.read_text()
    lines=['# Whole-plant steam versus helium Brayton conversion study','',
      '## 1. Study header','',f'- **Study id:** `{record.name}`',
      '- **Package:** whole_plant_conversion','- **Date executed:** 2026-09-27',
      '- **Executor:** Codex coordinator /root','- **Mode:** execute','- **Arms:** arm-whole-plant-offers','',
      '## 2. Intake','',
      'The complete owner-provided goal and scope are retained verbatim in [owner-brief.md](owner-brief.md), including its explicitly agent-proposed starting strategy.','',
      '> For one consistently specified reactor concept, how does selecting the modeled steam or helium Brayton conversion system change net electricity exported, whole-plant LCOE and the assumptions under which each choice is preferable?','',
      '[AGENT] This execution uses the reviewed supplied-source inventory, a finite equipment catalog and engineered sensitivity scenarios. The owner authorized conditional modeling assumptions and required complete plant power/cost scope. The chosen ranges are not empirical uncertainty bounds. [Configuration](supporting/configuration.md), [comparison contract](supporting/comparison-contract.md) and [pre-execution framing](pre-execution-framing.md) retain that authority and the applicable reporting bands.','',
      '## 3. Objective and result','',
      'The objective channels are `whole_plant_conversion__plant__steam_whole__evaluate__lcoe_USD2025_MWh` and the corresponding `gas_whole` channel. They are native whole-plant lifecycle costs per exported MWh in real 2025 USD. The native ledger includes startup fuel, operating imports, source and conversion service, replacements and terminal events. Annual net grid delivery after standby imports is also reported and must remain positive.','',
      '| Source MW | Branch | Net export MW | Initial capital billion USD2025 | Financed capital billion USD2025 | LCOE USD2025/MWh | Native case |',
      '|---:|---|---:|---:|---:|---:|---|']
    for row in data['rankings']:
        if row['scenario']!='nominal':continue
        if not row['selected']:
            lines.append(f"| {row['source_MW']:g} | {row['branch']} | — | — | — | unsupported | No passing offer |")
        else:
            m=row['metrics'];lines.append(f"| {row['source_MW']:g} | {row['branch']} | {m['power.net_export_MW']:.6f} | {m['initial.initial_capital']/1e9:.6f} | {m['whole.initial_financed_capital']/1e9:.6f} | {m['whole.lcoe_USD2025_MWh']:.6f} | `{row['selected']['native_case']}` |")
    lines += ['', 'These are fresh minima over admitted native catalog members. The full paired scenario results, exact signed differences, strict ordering and ±5 USD2025/MWh reporting classifications are in [matched-pairs.csv](results/presentation/matched-pairs.csv). The power reporting band is ±5 MW. Neither band is a physical constraint or statistical interval. [Study conclusion](study-conclusion.md) explains the preference, combined-assumption reversal and native threshold confirmations.','',
      '## 4. Constraint outcomes','',
      'Every executing identity is listed below. Counts cover all stored points, including the alternative branch in a paired computational assembly. Ranking requires its own branch and all shared predicates; it does not require an unused alternative to pass. The [complete constraint summary](results/constraint-summary.json) links every failed identity to its exact native case. Source, nuclear-transport and global-construction qualification flags are separate, deliberately zero conditions on the scientific interpretation; passing equipment checks does not qualify them.','',
      '| constraint_id | source_local_identity | Branch | Satisfied | Violated | Other |','|---|---|---|---:|---:|---:|']
    for row in counts['constraints']:
        c=row['counts'];lines.append(f"| `{row['constraint_id']}` | `{row['source_local_identity']}` | {row['branch']} | {c.get('satisfied',0)} | {c.get('violated',0)} | {sum(v for k,v in c.items() if k not in ('satisfied','violated'))} |")
    lines += ['', '## 5. Framing','',
      'The proposed and judged framing coincide. Search means selecting among the finite declared equipment/operating offers, not locating a continuous or global optimum. Sensitivity means observing conditional scenario responses. Coordinated scenario changes do not establish a separate marginal effect of each participating attribute.','',
      '| Axis | Proposed | Judged | Changed? | Execution |','|---|---|---|---|---|']
    for row in axes:lines.append(f"| `{row['axis']}` | {row['framing_proposed']} | {row['framing_judged']} | no | {'executed' if row['declared_executed'] else 'declined with reason in axes.json'} |")
    lines += ['', '## 6. Per-axis account','',
      'The [axis assessment](results/axis-assessment.json) retains exact observed values for every declared key. The [native scenario rankings](results/presentation/scenario-summary.json), [case ledger](results/presentation/attempted-case-ledger.csv) and [window edge rereading](window.json) carry the response, failed locations and finite feasible structure. An edge marked not_caught remains open; no continuous feasible limit is inferred. The separately declared cryogenic brackets are held-equipment boundary diagnostics, not a neutronics uncertainty interval.','']
    for row in axes:
        axis=row['axis'];search=row['framing_judged']=='search';executed=row['declared_executed']
        lines += [f'#### `{axis}` — feasible structure (search framing)','',
          '**Applies:** '+('yes' if search else 'not applicable — sensitivity-framed'),'',
          ('The finite admitted offers and failed native cases are retained in the linked case ledger. Observed choices are in the axis assessment; relevant edge checks are in window.json. No global optimum is claimed.' if search else 'The study does not make a search claim for this attribute.'),'',
          f'#### `{axis}` — observed response (sensitivity framing)','',
          '**Applies:** '+('not applicable — search-framed' if search else 'yes'),'',
          ('No separate sensitivity claim is made for this search-framed attribute; its coordinated scenario context remains recorded.' if search else
           'This declared attribute was held fixed. Its decline reason is retained in axes.json; no observed response or boundary is claimed.' if not executed else
           'The native scenario table and case ledger record this attribute’s coordinated changes, response and any violated checks. The axis assessment lists its actual values. No independent marginal response or general feasible-region boundary is claimed.'),'']
    lines += ['## 7. Axis groups','',
      'All groups are actual qualified source attributes expanded to their emitted input keys. Each group has one emitted key with fan_out provenance. There are no cross-attribute ties. Equal ratios, prices and efficiency changes are coordinated choices, not asserted physical identities.','',
      '| Axis | Entry key | Provenance |','|---|---|---|']
    for group in groups:
        for key in group['keys']:lines.append(f"| `{group['axis']}` | `{key['key']}` | {key['provenance']} |")
    lines += ['', '## 8. Indicators and rulings','',
      'All 90 declared groups, including five declined groups, report constraints_reachable in [indicators.json](indicators.json); subset is false. None reports no_constraint_response, so no additional owner ruling is required. The owner explicitly requested price, performance, common cost/load, fuel and availability sensitivities. A reachable path is a possible dependency, not proof of physical or economic resistance.','',
      '**Not derivable:** monotonicity of a channel in an axis; identity of the same physical quantity across differing key names; intra-module operand dependency. No indicator output or report claims these. Engineered price and efficiency scenarios remain sensitivities even where a domain/economic predicate is reachable.','',
      'There are no no_constraint_response model-development findings. Other material limitations and discoveries are registered in §15.','',
      '## 9. Preflight results','',
      'The [native integration return](integration/integration_return.json) records all ten gates passing. The same frozen package, full axis declaration, manifest, baseline and environment are used by this study; that valid evidence is reused. [Preflight results](preparation/preflight_results.json), [package identity](preparation/package_identity.json), [baseline result](preparation/baseline_result.json) and [Python read coverage](preparation/read_coverage.json) retain the actual receipts.','',
      '| Gate | Outcome | Evidence |','|---|---|---|',
      '| Declared-group key validation | pass | Full 90-group declaration and native preflight |',
      '| Suffix-sibling scan | pass; warnings remain interpretive | Exact tool output in preparation/preflight_results.json |',
      '| Baseline headline reproduction | pass | Complete 637-input baseline and native result |',
      '| Manifest/package fingerprints | pass | Integration manifest and lineage gates |',
      '| Package cleanliness | pass | Integration and stock main route before/after checks |',
      '| Python read coverage | pass | Fresh baseline observer receipt; limits retained in integration documentation |','',
      'The first round is sealed separately as 20260927-design-study-whole-plant-conversion at commit 275ba13c, with released=false. It retains the invalid concurrent preparation scan and all 2496 native cases that failed numerical verification. This replacement record preserves the equipment catalog and acceptance tolerances. Independent high-precision evidence justified tightening the independent cooler root solve; four cryogenic diagnostic points now straddle the same capacity threshold at ±0.01 W/m³. The numerical repair proposal, review and regression evidence are retained under supporting. No native main-study attempt was discarded.','',
      '## 10. Execution route and why','',
      '**Route:** study-local direct API using the stock strict loader, PreparedEvaluator, StudyRunner, PreparedListStrategy, StudyStore and StudyQuery. Coordinated equipment tuples and scenario blocks require a prepared point list. The route was exercised by integration before execution. Every main point carries complete inputs, scalar outputs and all native verdicts in the store.','',
      '**Glue ledger: none.** No runtime adapter or external physics solver supplies a missing model relationship. Oracle scans choose candidate inputs before execution; report code only joins, selects, decomposes and plots native outputs. The cost plot normalizes published cost PV components by published energy PV; the headline remains the native LCOE channel.','',
      '## 11. Study definition and window provenance','',
      f"The stable-package independent scan evaluated {scan['oracle_evaluations']} complete points, with zero refusals, before fixing {scan['unique_complete_points']} unique native proposals and {scan['alias_count']} catalog/scenario aliases. The final definitions, values, brackets and input-source hashes are frozen in [window.json](window.json), [proposed-points.json](proposed-points.json) and [candidate-freeze.json](preparation/candidate-freeze.json).",'',
      'The window is engineered. It retains the predecessor catalog but rereads its edges from currently passing whole-plant anchors. Failure pruning in common/quote scenarios is justified by an invariant failed predicate or an explicit changed-point oracle evaluation. Both admission audits retain every decision; no newly admitted offer was omitted. Changed performance rescans the full affected catalog. The 3000 MW source has no passing shared equipment basis and is retained as unsupported. Hypothetical performance/price interactions and native strict-zero/reporting-band brackets are part of the predeclared list.','',
      '## 12. Cross-fingerprint correlation and what it means','',
      'Single fingerprint for all main-study points; no cross-arm correlation is needed. The predecessor is historical context with a narrower cost/power boundary and 0.85 availability, compared with 0.80 here. Its 498 controls exactly reproduce 872 inherited channels and 84 predicates under legacy finance; new whole-plant conditions and outputs are additional scope. Six selected predecessor native receipts and the historical verification/summary are retained under supporting/predecessor. The report does not reuse those winners as the new whole-plant answer or interpret the boundary/finance/reranking difference as a pure cost addition.','',
      '## 13. Verification','',
      'The stock verifier passed every main case across all 1192 named scalar outputs and all 125 re-derived predicates. Four inherited solver-iteration diagnostics are excluded. It uses the existing relative and predeclared absolute numerical tolerances; physical inequalities are not relaxed. [Verification summary](results/verification_summary.json) gives exact case selection and comparisons; snapshot.json retains the executed command, source revision, tolerance declarations and receipt digest.','',
      'Numerical agreement checks implementation of the declared equations. The independent cooler solver uses the separately reviewed tighter stopping precision; it retains its own equations and does not copy native outputs. Numerical verification does not establish vendor performance, source heating transport, plasma sustainment or global manufactured reactor fit. Fixed captured constants and qualification flags that agree by construction are not independent empirical validations. Earlier independent source/accounting and native behavior reviews are retained with their actual scope.','',
      '## 14. Review outcomes','',
      '| Lens | Verdict | Disposition |','|---|---|---|',
      '| Source, full account/power boundary and MR-7 | independent PASS | Exact frozen implementation identity; supporting/implementation-integration-review.md |',
      '| Pre-execution framing, range and admission | coordinator checked | Existing source/math review applies; complete stable-package scan, explicit materiality and admission audit retained |',
      '| Final whole-plant reranking, claims and presentation | independent PASS | supporting/final-results-review.md; exact native evidence, assumptions and findings assessed |','',
      'No duplicate source review is claimed. The same independent reviewer reused valid implementation coverage and inspected the new execution, ranking and claim paths.','',
      '## 15. Findings','',
      '| Id | Kind | Finding | Disposition | Home |','|---|---|---|---|']
    findings=load(record/'findings.json')['findings']
    for f in findings:lines.append(f"| {f['id']} | {f['kind']} | {f['finding']} | {f['disposition']} | {f['home']} |")
    snapshot=record/'snapshot.json'
    lines += ['', '## 16. Snapshot','', '- **File:** snapshot.json',
      '- **sha256:** '+(hashlib.sha256(snapshot.read_bytes()).hexdigest() if snapshot.exists() else 'Resolved at the final seal; this is the reviewed pre-seal record.'),
      '- **Schema version:** 1','',
      'The snapshot resolves values and artifact digests. The sealed package and frozen source bundle make the result independent of later live model, manifest or report changes.','',
      '## 17. What this record does not contain','',
      'The record retains six selected predecessor native cases and its verification/summary, not the full predecessor 498-case store. It retains the reviewed development report and verification receipts rather than every raw development run. Original background PDFs are not bundled; their stated authority, assumptions and calculations are retained in the copied configuration, design and source audit. The whole-plant main store, complete inputs, all native outputs/verdicts, report data, renderer, replay instructions, scan history and required identities are included.','',
      '**END OF RECORD**','']
    (record/'record.md').write_text('\n'.join(lines))
    print(json.dumps({'sections':17,'axes':len(axes),'constraints':len(counts['constraints']),'cases':counts['cases']}))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--record',type=Path,required=True);write(p.parse_args().record)
