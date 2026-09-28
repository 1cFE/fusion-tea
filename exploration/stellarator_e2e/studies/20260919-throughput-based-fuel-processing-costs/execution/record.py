"""Write the completed record and joined findings from retained study evidence."""
import json
from pathlib import Path

H = Path(__file__).resolve().parents[1]
R = H / 'results'
read = lambda path: json.loads(path.read_text())
rows = read(R / 'interpreted-cases.json')
summary = read(R / 'summary.json')
catalog = read(R / 'predicate-catalog.json')
groups = read(H / 'axes.json')['groups']
ind = read(H / 'indicators.json')
props = read(H / 'preparation/proposals.json')
verification = read(R / 'oracle-all-points.json')
b = summary['reference']; old = summary['legacy_reference']; n = len(rows)
prior = (H / 'record.md').read_text()
intake = prior.split('## 2. Intake\n\n')[1].split('## 3. Objective and result')[0].strip()
home = 'work/orchestration/goals/throughput-based-fuel-processing-costs/learnings.md'
findings = [
    ('1', 'model', 'Capacity margin has no constraint response; process duty, pressure, reliability and adequacy are not qualified.', 'Authorized sensitivity only; no redundancy or design-margin recommendation.', home),
    ('2', 'model', 'Source-price multiplier has no constraint response or procurement/economic calibration.', 'Retain engineered stress range, not market-price confidence or physical improvement.', home),
    ('3', 'model', 'Containment expenditure CPI has no constraint response; the historical chronology and modern price remain unresolved.', 'Retain named 1978/1980/1982 scenarios; date-only spread is not full uncertainty.', home),
    ('4', 'model', 'Account selection has no constraint response; no physical qualification predicate discriminates the cost methods.', 'Matched controls preserve physical failures; conditional source declaration is not qualification.', home),
    ('5', 'model', 'Burn changes both throughput capital and existing recurring fuel; physical recovery and recurring-price recovery remain separate inputs.', 'Use matched account deltas for attribution; hold recurring recovery at its authored value.', home),
    ('6', 'model', 'All 20 finite cases retain failed plant screens despite lower conditional processing cost.', 'No feasible optimum, breeding self-sufficiency or complete installed fuel plant claim.', home),
    ('7', 'process', 'Stock proposal validation rejected five Boolean legacy switches before execution while accepting numeric representations.', 'Preserved attempt 1; coordinator-authorized equivalent 0.0 controls re-scanned and executed in a fresh store. Shared-route allowlist remains unchanged.', 'exploration/stellarator_e2e/studies/study_route.py'),
]
S = {}
S['1. Study header'] = f'- **Study id:** {H.name}\n- **Package:** stellarator_tea\n- **Date executed:** 2026-09-19\n- **Executor:** Codex interface_review; entering-interface reviewer, independent arithmetic author and study author. No final independent certification claimed.\n- **Mode:** execute\n- **Arms:** arm-native; one generated candidate with active/legacy account controls.'
S['2. Intake'] = intake.replace('Prepare a finite sensitivity study', 'Execute a finite sensitivity study').replace('Final keys, indicators and case window will be resolved from the audited package before execution.', 'Keys, indicators and the case window were resolved from the audited package before execution.')
S['3. Objective and result'] = f'Objective channels are `stellarator_09__stellaris__lcoe_calc__lcoe` and `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe`. The active reference gives ${b["LCOE"]:.6f}/MWh and ${b["LCOE_1cfe"]:.6f}/MWh, against ${old["LCOE"]:.6f}/MWh and ${old["LCOE_1cfe"]:.6f}/MWh at the identical legacy physical point. Conditional processing capital is ${b["processing_selected"]:.2f}; all charge effects flow through the native model. [Report](report.md) explains scope and attribution; [points](results/points.csv) contain results. The selected finite list is not optimized.'
table = ['| `constraint_id` | `source_local_identity` | Status | Note |', '|---|---|---|---|']
for cid, item in catalog.items():
    failures = [row['id'] for row in rows if row[cid] != 'satisfied']
    counts = summary['predicate_counts'][cid]
    status = 'satisfied' if not failures else ('violated' if len(failures) == n else 'satisfied / violated by case')
    where = 'all cases' if len(failures) == n else ', '.join(failures)
    note = f'{counts["satisfied"]} satisfied; {counts["violated"]} violated; {counts["indeterminate"]} indeterminate.'
    if failures: note += ' Violations: ' + where + '.'
    table.append(f'| `{cid}` | `{item["source_local_identity"]}` | {status} | {note} |')
S['4. Constraint outcomes'] = f'All {len(catalog)} authored predicates are retained at every case; {summary["wholeplant_satisfied"]} cases satisfy all. Complete qualified point verdicts are in [native cases](results/native-cases.json).\n\n' + '\n'.join(table)
S['5. Framing'] = '**As proposed at intake.** Every axis was sensitivity-framed to separate actual demand from monetary and capacity assumptions.\n\n**As judged after the run.** All eight remain sensitivities. Burn/recovery change breeding verdicts at some finite points; that does not turn this finite list into a boundary search. Density changes multiple systems and plant screens. Cost/date/margin controls preserve physical outputs. No framing changed and no optimum is claimed.'
families = {'fuel_cycle__burn_fraction': 'burn', 'fuel_cycle__t_recycle': 'recovery', 'plasma__n_e0': 'density', 'unplanned_fraction': 'downtime', 'fuel_cycle__processing_price_multiplier': 'price', 'fuel_cycle__processing_capacity_margin': 'margin', 'fuel_cycle__processing_containment_cpi': 'containment-date', 'fuel_cycle__processing_enabled': 'legacy-control'}
meaning = {
    'burn': 'Both running processing demand and recurring fuel change; matched controls isolate the capital-method contribution.',
    'recovery': 'Pre-loss inlet and processing price stay fixed while losses and required breeding change. Recurring-price recovery stays held.',
    'density': 'Native operating power, equipment demand and electricity output change together; matched controls isolate account selection.',
    'downtime': 'Running capacity and processing price stay fixed while availability, annual amounts and LCOE change.',
    'price': 'Price scales equipment and installation; upstream outputs and predicates remain fixed.',
    'margin': 'Actual inlet remains fixed; installed capacity and source power-law costs rise. No spare-train or reliability claim.',
    'containment-date': 'Only containment conversion and downstream totals change; other source rows are unchanged.',
    'legacy-control': 'Same physical inputs and predicate verdicts; only selected cost and downstream economics change.',
}
axis_text = []
for group in groups:
    axis = group['axis']; family = families[axis]
    selected = [row for row in rows if row['family'] == family or row['id'] == 'reference']
    if family == 'legacy-control':
        ids = {row['id'].removeprefix('legacy-') for row in selected}
        selected += [row for row in rows if row['id'] in ids and row not in selected]
    failure_locations = '; '.join(row['id'] + ': ' + row['failed'].replace(';', ', ') for row in selected)
    axis_text += [f'#### {axis} — feasible structure (search framing)', '', '**Applies:** Not applicable; sensitivity-framed.', '', f'#### {axis} — observed response (sensitivity framing)', '', '**Applies:** Yes.', '', meaning[family] + f' Selected cases: {", ".join(row["id"] for row in selected)}. No boundary claim is made. Violations: {failure_locations}. See results/points.csv for exact responses.', '']
S['6. Per-axis account'] = '\n'.join(axis_text).strip()
S['7. Axis groups'] = '| Axis | Entry key | Provenance | Note |\n|---|---|---|---|\n' + '\n'.join(f'| {group["axis"]} | `{entry["key"]}` | {entry["provenance"]} | One public attribute; every direct consumer binds it. |' for group in groups for entry in group['keys']) + '\n\nNo ties or undeclared suffix siblings. [Pipeline fan-out evidence](preparation/fan-out-evidence.json) names all direct consumers. Computed throughput and power were not swept.'
indicator_rows = ['| Axis | Indicator | Ruling | Note |', '|---|---|---|---|']
finding_by_axis = {'fuel_cycle__processing_capacity_margin': '1', 'fuel_cycle__processing_price_multiplier': '2', 'fuel_cycle__processing_containment_cpi': '3', 'fuel_cycle__processing_enabled': '4'}
for group in ind['groups']:
    result = 'no_constraint_response' if group['no_constraint_response'] else 'constraints_reachable'
    note = f'Model finding {H.name}#{finding_by_axis[group["axis"]]} remains.' if group['no_constraint_response'] else 'Reachability is conservative; response judged from native cases.'
    indicator_rows.append(f'| {group["axis"]} | {result} | Coordinator sensitivity release under owner result 7 and adoption | {note} |')
S['8. Indicators and rulings'] = '\n'.join(indicator_rows) + '\n\n[Framing proposal](reviews/framing-proposal.md), [axis ruling](reviews/axis-rulings.json) and [window release](reviews/window-release.json) precede dependent execution. All groups were traced; none declined. Each no-response axis carries a separate finding in §15.\n\nNot derivable from indicators: monotonicity, physical identity across differently named keys and intra-module operand dependence. constraints_reachable means a possible path, not observed response. unresisted is an executor judgment, never a tool output.'
S['9. Preflight results'] = '| Gate | Outcome | Detail |\n|---|---|---|\n' + '\n'.join(f'| {gate["gate"]} | {gate["status"]} | {gate["detail"]} |' for gate in read(R / 'preflight_results.json')['gates']) + '\n\nThe identity and baseline checks read results/package_identity.json and results/baseline_result.json. No study preflight gate was skipped. Before/after native execution cleanliness passes are retained. Integration’s omitted read-set coverage remains a separate disclosed limitation; the indicator tool’s own coverage check does not retroactively certify it.'
S['10. Execution route and why'] = 'Study-local direct API using stock StudyRunner and PreparedListStrategy through the retained study_route.py. It supports the finite one-factor list and matched account controls without a Cartesian grid or handwritten plant evaluator. The route loaded and reproduced the pinned baseline before native cases.\n\nGlue ledger: none. The caller declares inputs and requested outputs; the sealed model supplies all physics and cost equations. Runtime import paths and teax revision are captured in results/execution-environment.json and the integration receipt.\n\nAttempt 1 admitted 15 active cases and rejected five Boolean legacy proposals before evaluation. The original store/raw artifacts remain, with the complete backup and rejection receipt in results/attempt-1/. Under recorded coordinator authority, false changed only to numeric 0.0; the equivalent list was re-scanned and run in a fresh results/study/retry-1/ store. No scientific window or model change occurred. The relocated backup is not claimed cold-reproducible; the completed retry has the frozen-package reproduction route.'
S['11. Study definition and window provenance'] = 'The window is engineered: compact finite physical sensitivities, source-price stress, capacity allowance and actual containment expenditure-date scenarios. The independent oracle evaluated the complete 20 candidates after baseline/preflight, and the coordinator retained them all. The mechanical representation retry was re-scanned before execution. No candidate was dropped for plant failure and no feasible anchor was manufactured. results/oracle-scan.json retains all mapped channels and derived verdicts. This is not a continuous design window, uncertainty distribution or feasible-boundary claim.'
S['12. Cross-fingerprint correlation and what it means'] = 'Single generated fingerprint; no cross-fingerprint correlation needed. Account selection changes within the same package at matched physical inputs. The rejected-proposal attempt and completed retry use that same executable but distinct proposal-definition identities because their Boolean representation differs. Historical studies remain unchanged.'
S['13. Verification'] = f'All {verification["scalar_comparisons"]} mapped scalar comparisons and {verification["predicate_comparisons"]} independently derived predicate comparisons pass across {n} cases. The generic verifier samples every case across four observed verdict combinations and passes. There are {verification["mapped_channels"]} unique mapped scalar channels (920 numeric and 14 Boolean); 935 semantic map labels include one duplicate target. Of 942 numeric outputs, 22 are outside the oracle map and named in preparation/coverage.json. All new processing outputs and the shipping exclusion are mapped. Exact native invariance checks also pass.\n\nIndependent software arithmetic does not independently verify shared source assumptions or neutron-transport data. The cost-oracle author is this study executor; final certification belongs to the non-author reviewer. The integration read-set omission, static L2 residue and three added L6 dot diagnostics remain disclosed. No full static-validation pass is asserted.'
S['14. Review outcomes'] = '| Lens | Verdict | Disposition |\n|---|---|---|\n| Original source/price and design | Conditional PASS; owner adopted premise | Retained reference copies and source digests; no new source premise in this study. |\n| Independent implementation audit | PASS for audited candidate | preparation/references/audit.md and implementation-review.md; audited commit matches release. |\n| Native integration | All ten gates pass | preparation/integration-return.json; omitted read-set coverage still disclosed. |\n| Framing and window | Coordinator releases under owner authority | reviews/axis-rulings.json and window-release.json; equivalent representation retry explicitly authorized. |\n| Native verification and explanation | Author checks complete | Scalar/predicate/invariance receipts and report; not independent final approval. |\n| Final independent study and grade | Pending | Coordinator obtains final non-author assessment after record commit. |'
S['15. Findings'] = '| Id | Kind | Finding | Disposition | Home |\n|---|---|---|---|---|\n' + '\n'.join(f'| `{H.name}#{i}` | {kind} | {finding} | {disposition} | `{target}` |' for i, kind, finding, disposition, target in findings)
S['16. Snapshot'] = 'Pending final evidence freeze; written once after the record and tool copies are complete.'
S['17. What this record does not contain'] = 'The producer package and required tool/helper sources are included at freeze. The later coordinator commit and independent grade are recorded outside this immutable study record. The record does not include an installed Python environment, syside license, entire external toolchain checkouts or large upstream transport binaries; reproduction needs the recorded compatible runtime. It contains retained source/review texts and their provenance, not every complete historical source paper. It has no commercial quotation, measured process-feed qualification, reliability design or complete fuel-plant estimate.'
(H / 'record.md').write_text('\n\n'.join('## ' + title + '\n\n' + text for title, text in S.items()) + '\n')
write_findings = [{'id': H.name + '#' + i, 'kind': kind, 'finding': finding, 'disposition': disposition, 'home': target} for i, kind, finding, disposition, target in findings]
(R / 'findings.json').write_text(json.dumps(write_findings, indent=2) + '\n')
log = H.parent / 'DISCOVERY_LOG.md'; existing = log.read_text()
with log.open('a') as stream:
    for finding in write_findings:
        if finding['id'] not in existing:
            stream.write(f'| 2026-09-19 | {finding["kind"]} | `{finding["id"]}` | {finding["finding"]} | {finding["disposition"]} | `{finding["home"]}` |\n')
synthesis = ['# Executor synthesis', '', 'Authorship: Codex interface_review, study and independent cost-oracle author. This is an executor reading of this record, not an independent review. Reading scope: completed native artifacts and this record before snapshot freeze; no snapshot had been read.', '',
f'The study asks how computed exhaust demand reaches conditional process capital and electricity cost. The reference prices {b["flow_kg_day"]:.6f} kg D+T/day at ${b["processing_selected"]/1e6:.6f} million of limited historical subsystem scope in 2025 purchasing power. Matched account controls reduce total capital by ${(old["total_capital"]-b["total_capital"])/1e6:.6f} million and lifecycle LCOE by ${old["LCOE"]-b["LCOE"]:.6f}/MWh at the unchanged physical reference. [Native results](results/points.csv) and [matched deltas](results/matched-account-deltas.json) support those figures.', '',
'Burn fraction changes inlet and both processing capital and existing recurring fuel. Physical recovery changes losses but not pre-loss capacity; its recurring-price counterpart remains held. Density changes multiple operating quantities; matched controls isolate the method effect. Downtime changes annual amounts and electricity output, not running capacity. Price, margin and containment-date controls preserve upstream physical predictions. All eight axes retain sensitivity framing; no boundary or optimum is inferred.', '',
'All 20 retry cases retain failed whole-plant predicates. Qualified verdicts and exact failure locations are in record.md §4 and results/native-cases.json. Four no-response assumption axes retain their missing-pushback findings. Seven joined findings are in results/findings.json. The record also preserves the first attempt’s five proposal rejections and the authorized numeric-representation retry.', '',
f'All {verification["scalar_comparisons"]} independent scalar comparisons and {verification["predicate_comparisons"]} predicate comparisons pass. The generic sample and native invariance checks pass. The mapped arithmetic shares source assumptions and transport data with production; 22 numeric channels remain outside the oracle map. [Verification](results/oracle-all-points.json) and [coverage](preparation/coverage.json) distinguish those limits.', '',
'## What the record does not support', '', 'It does not establish feasible operation, breeding self-sufficiency, qualified impurities or recovery, present-day equipment prices, spare-train reliability or a complete fuel plant. The price/date/margin ranges are declared sensitivities, not confidence intervals. Integration read-set coverage was omitted, static diagnostics remain, and final independent grading is pending. The record names external runtime prerequisites; it is not a complete installed runtime image.']
(H / 'synthesis.md').write_text('\n'.join(synthesis) + '\n')
print(f'Wrote 17 sections, executor synthesis and {len(findings)} joined first-sighting findings')
