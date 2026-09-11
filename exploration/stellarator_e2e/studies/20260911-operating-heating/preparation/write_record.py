"""Write the proposed native record. No evaluation."""
import json
from pathlib import Path
R=Path('exploration/stellarator_e2e/studies/20260911-operating-heating')
p=json.loads((R/'preparation/proposal.json').read_text())
c=json.loads((R/'preparation/model-contract.json').read_text())['constraint_catalog']['concrete_entries']
m=json.loads((R/'context/manifest.json').read_text())
expected={x['source_local_identity']:x['expected'] for x in m['baseline']['verdicts']}
rows='\n'.join('| '+x['constraint_id']+' | '+x['source_local_identity']+' | Not executed | Pinned baseline expects '+expected[x['source_local_identity']]+'. |' for x in c)
axes='\n'.join('| '+a+' | stellarator_09__stellaris__'+a+' | fan_out | Complete single-attribute entry group. |' for a in ['p_wallplug_heat','f_alpha_fast','n_e0','T_i0'])
text='''## 1. Study header

- **Study id:** 20260911-operating-heating
- **Package:** stellarator_tea
- **Date executed:** Not executed; prepared 2026-09-11.
- **Executor:** Native T-019 preparation agent; parent owns execution authorization.
- **Mode:** execute, preparation only.
- **Arms:** arm-reserve, arm-retained-alpha, arm-density, arm-coordinated-zero.

## 2. Intake

[OWNER-VERBATIM]

> I have this audit report of modeling issues: .project/reports/20260907-fusion-model-audit.md

> I'd like you to $run-goal to address these.

> yes ground and proceed

[AGENT] Under T-019 scope at 167785f0 and Round 4, test whether reserve changes at fixed plasma and efficiencies leave operation unchanged while procurement responds, and whether supported demand changes at fixed heating installation propagate coherently without repricing installed heating. The specific study question, engineered cases and expectations are agent-originated. Preserve historical evidence, held finance/efficiencies and design-point sizing conventions.

The record uses the single T-018 candidate copied in `context/integration_return.json`; no new pin is created. Model audit at 55456198 and package certificate at 07c33fee are copied in `context/`. Their conclusions are inherited bounded evidence, not new study execution.

## 3. Objective and result

- **LCOE objective channels:** stellarator_09__stellaris__lcoe_calc__lcoe and stellarator_09__stellaris__lcoe_1cfe_calc__lcoe.
- **LCOE result:** Not executed. The copied manifest pins headline 224.26923288439 $/MWh; this is an expectation, not a T-019 result.

The report will separately identify current-case response and inherited pre-repair attribution. All proposed signed-invalid cases remain in the result account. No optimum or feasible plant is claimed.

## 4. Constraint outcomes

No constraint has executed in this record. Every catalog identity below must be reported for every completed case; the notes are inherited baseline expectations.

| constraint_id | source_local_identity | Status | Note |
|---|---|---|---|
'''+rows+'''

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| p_wallplug_heat | sensitivity | Reserve/procurement intervention with fixed operation; includes capacity-limited diagnostic. |
| f_alpha_fast | sensitivity | Bounded physical-assumption control of retained alpha and operating demand; coordinated near-zero case explicitly separate. |
| n_e0 | sensitivity | Public plasma-state control provides positive and negative signed demand without a demand override. |
| T_i0 | sensitivity, declined | Candidate temperature-only probe did not produce negative demand; density gives the needed diagnostic without a temperature intervention. |

**As judged after the run.** Not yet judged; no TEAx point ran.

## 6. Per-axis account

'''
for a in ['p_wallplug_heat','f_alpha_fast','n_e0','T_i0']:
    text+=f'#### {a} — feasible structure (search framing)\n\n**Applies:** not applicable — this axis is sensitivity-framed.\n\n#### {a} — observed response (sensitivity framing)\n\n**Applies:** '+('not applicable — candidate declined; preliminary probe remains in preparation evidence.' if a=='T_i0' else 'yes. No executed response yet. The final account must identify every violation at its studied coordinates; no physical boundary claim is made.')+'\n\n'
text+='''## 7. Axis groups

All four considered axes are declared in `axes.json` and traced, including the declined temperature candidate. The existing R/magnet-radius tie remains in the complete pinned baseline point; it is not swept.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
'''+axes+'''

## 8. Indicators and rulings

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| p_wallplug_heat | constraints_reachable | No no-response ruling needed | 2/18 constraints reachable; module-level divertor reach includes the installed diagnostic, not proof of operational coupling. |
| f_alpha_fast | constraints_reachable | No no-response ruling needed | 10/18; proposed sensitivity and coordinated diagnostic. |
| n_e0 | constraints_reachable | No no-response ruling needed | 10/18; proposed sensitivity and coordinated diagnostic. |
| T_i0 | constraints_reachable | No no-response ruling needed | 10/18; declined, retained in indicators. |

**Not derivable, disclosed in every record.** Indicators cannot determine monotonicity, physical identity across different key names, or intra-module operand dependency. constraints_reachable means a possible graph path, not actual response. unresisted would be an agent judgment, not a tool result.

**Model-development findings.** No no_constraint_response axis was reported, so its special finding/ruling obligation does not apply. Broader engineering omissions remain in copied audits and the eventual findings register.

## 9. Preflight results

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | Indicator validation passed; formal preflight pending | All four complete groups validated in indicators.json. |
| Suffix-sibling scan (warnings only) | Did not run | Formal preflight follows fresh critique and pinned baseline execution. |
| Baseline gate against the pinned headline | Did not run | No results/baseline_result.json exists yet. |
| Manifest / package fingerprint match | Indicator fingerprint matched; formal identity gate pending | Current indicator-input pin matches the sole promoted candidate. |
| Package cleanliness | Did not run | Formal preflight must establish package cleanliness. |

## 10. Execution route and why

**Proposed route:** study-local direct-API using the current package-owned route's stock StudyRunner and PreparedListStrategy. Four prepared arms contain coordinated cases and explicit labels; `study.py` calls the route with all 141 declared numeric columns. This is a proposed rationale pending the required baseline/preflight exercise. Importing the definition performs no evaluation.

**Glue disclosure:** glue ledger: none. Stock strict loading, no adapter and no harness-supplied model results. The algebraic fraction selects public inputs; it does not override computed demand.

## 11. Study definition and window provenance

The candidate windows are engineered for bounded sensitivity and signed diagnostics. The exact 16 proposals live in `preparation/proposal.json`. No source is claimed for their bounds. Preliminary oracle-only exploration is preserved under `preparation/preliminary-*.json` with its scripts. This early exploration made critique concrete; it does not complete runbook Step 7. After critique, execute the exact pinned baseline, run all preflight gates, then repeat/confirm the candidate scans before fixing the final windows.

The density-only scan reaches negative demand. The coordinated near-zero candidate uses a separately declared density and retained-alpha pair, selected by an affine interpolation within the fraction domain. Its preliminary residual is nonzero; native zero remains unproved. Temperature exploration remains visible as a declined candidate. Geometry is unchanged and meets the existing held radial-stack mask. Negative demand is retained for diagnosis rather than masked away.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. Copied historical baseline attribution is a separately labeled audit comparator, not another executed study arm. Historical plant-closure windows and regrade credit are not inherited.

## 13. Verification

Not executed. Use generic verify.py with sample-size 16 across the arm stores, covering all cases and therefore every verdict combination. Check all catalog objectives and predicate operands, plus the deposited independent identities in `preparation/expectations.md`. The additional 141-column publication map ensures relevant conservation and cost values are present before persistence/export.

Oracle parity verifies translation given shared assumptions; it does not recertify those assumptions. Independent identities/finance attribution, inherited native exact-zero fixtures, source authority and engineering limitations must be reported separately. Failed evaluation is retained as failed evidence and stops publication; no failing case is silently omitted.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing critique | Pending fresh critic | No TEAx baseline or point may execute before parent authorizes the next stage. |
| Correctness | Not reviewed | Required after execution. |
| Honesty | Not reviewed | Required after execution. |
| Readability | Not reviewed | Required after execution. |

## 15. Findings

No study findings have been finalized at preparation. Final execution must assign every finding an id and a home and join its first-sighting row to the discovery log before commit. The original model/package limitations are copied as inherited context and are not accepted residuals by this record.

## 16. Snapshot

Final snapshot.json is not created. It must resolve the manifest values, all three fingerprints, complete entry models and compatibility tuples, stock no-adapter identities, exact windows, tool/runtime/source digests, all result digests and all copied content used. `context/index.json` currently inventories copied evidence with hashes; it is not a substitute for the final snapshot.

## 17. What this record does not contain

This preparation record contains no TEAx baseline, study point/store, formal preflight, formal post-preflight oracle scan, numerical verification, final framing judgment, finalized findings register, final snapshot, committed study or administrator synthesis. All preliminary predictions are labeled. It contains no fresh historical-package rerun or full-plant exact-zero result. Those limitations must be amended honestly as authorized execution completes.
'''
(R/'record.md').write_text(text)
