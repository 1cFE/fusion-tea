# Audit: MFE operating-heating study package

**Verdict:** Certify
**Audited:** 2026-09-11
**Branch:** test/codex-native-skills
**Commit:** 676c7308

## The Point

The model repair separates installed heating capacity and procurement from the signed heating needed during operation. Current study consumers must execute that repaired plant, publish its operating power and individual feasibility checks, and compare it with the independent oracle. A baseline that violates the divertor limit must remain visibly infeasible. The owner requested audit remediation and authorized proceeding; this package migration's detailed requirements are agent-inferred under T-017, not new owner requirements.

## Summary

The current package meets SC-1–4. Fresh native execution verifies baseline, installed reserve and physical demand controls, including all 18 predicates and the three operating channels. Current metadata reproduces through native APIs and all 642 preserved file hashes match; inherited historical-export defects and model limitations remain explicit.

## Product Judgment

**This is the right bounded piece of work.** It makes the audited plant usable through the current study route without changing the model or concealing baseline infeasibility. The fresh product-lens ledger is **DISPOSED (audit-F1)**, with no unresolved BLOCK. Its only finding is agent-grade: six generated JSON graph fixtures repeat expectations in the Python regression contract (`tests/study/test_known_answers.py:33`). The fired smell is “Two representations must be manually kept synchronized.”

The qualitative test contract is deliberately reviewed separately from generated output. Automatically refreshing it would allow a changed producer to redefine its own expected behavior. The repeated mechanical counts do add maintenance work; this audit does not claim that duplication is ideal. Here, all six fixtures reproduce byte-for-byte, the Python expectations match the actual graph, and the product's manifest identities derive from native producers. No user-facing output or producer invariant depends on unchecked synchronization. I therefore dispose this lower-authority finding as optional test cleanup while retaining the independent qualitative assertions. It does not justify expanding this migration into shared tooling changes.

Fresh lens provenance is in `audit-evidence/product-lens-provenance.md`; its full output is retained. The lens independently rechecked retained arithmetic, but used the sealed interpreter directly rather than the required launcher. That computation receives no native-runtime credit. This auditor's launcher-based TEAx execution supplies the runtime evidence below. Narrow, named source tracing was used; no broad code exploration was needed.

## Findings

### Plan completion

All six Phase 1 steps are verified. The package metadata caller uses existing manifest fingerprint APIs, the route's baseline producer and the indicator CLI (`implementation/refresh_metadata.py:23`). It introduces no arithmetic or shared producer implementation. The audit gate is now satisfied. The plan and upstream contract at `6cf3649e`, T-017 at `392219a8`, WI-050 audit at `55456198`, and its package-consumer handoff were read.

### Spec conformance

- **SC-1 — met.** The route publishes all three operating channels (`exploration/stellarator_e2e/studies/study_route.py:77`), resolves the full catalog and refuses missing/unexpected verdict IDs (`:257`, `:272`). The oracle maps operating outputs and four exact efficiency assertion IDs (`oracle_entry.py:192`, `:360`). Installed sustainment and signed burn-hold bindings remain unchanged. Fresh stored controls rederive all 18 predicates with worst channel relative deviation `1.3031089676201858e-16`, below `1e-9`. Missing bindings, altered channels and planted verdict mismatches all reject.
- **SC-2 — met.** Native fingerprint APIs reproduce current identities; six graph fixtures reproduce byte-for-byte. Exact catalog/binding equality, 247 public inputs and 28 resolved feature references pass (`tests/study/test_operand_bindings.py:92`). The three independent heating graph groups exactly match retained evidence. Installed wallplug reaches capital and both LCOEs, with no operating-heating objective reach. Its structural divertor path is module-level propagation through the installed-capacity diagnostic; actual reserve execution leaves operating heat unchanged. Availability and discount rate leave all 18 assertions unreachable. All 12 historical exporter/test identities in the inherited-failure inventory match `6cf3649e`.
- **SC-3 — met.** The four handoff-named modules and current verifier, route, graph, operand, numeric publication and preflight regressions pass. Fresh battery: **164 passed, one optional historical-store skip**. A separate current publication selection passes **eight tests**. No required current TEAx execution was skipped. Scalar domain tests cover both efficiencies, and native zero-efficiency execution is recorded as `execution_failed` and refused by export (`tests/study/test_verify.py:370`).
- **SC-4 — met.** All 642 preserved hashes match, including model/generated/shared-tool/history and WI-050 evidence. The production diff from `6cf3649e` is exactly the four authorized current study files. Frozen production/test bytes still match `676c7308`. The annex states operating/capacity semantics, invalid-domain behavior and limits (`exploration/stellarator_e2e/studies/ANNEX.md:23`). This fresh non-author audit certifies the package scope before integration.

The owner-stated remediation need is served by this migration. All inferred implementation requirements are met. Non-goals are respected: no model arithmetic, finance, supported scope, thresholds, historical study, generated code or shared producer changed. No candidate or committed study was created.

### Design conformance

The implementation uses the existing package-owned oracle seam, route, manifest and generic verifier. It preserves the audited independent arithmetic and capacity/burn-hold semantics. It adds required objective comparisons for all three operating outputs, so publication cannot pass by omitting their independent checks. No undocumented architectural change was found. The item-local metadata script is a reproducible caller, as allowed by the specification.

### Code integrity

No new silent fallback, broad swallowed exception, placeholder, clipping or new mode-switch abstraction was found. Publication validates declared channels and exact catalog verdicts before CSV writes (`study_route.py:294–338`). The retained duplicated test expectations are disposed in Product Judgment rather than hidden as a green rubric result.

The implementation's broad run remains **150 passed, 86 historical failures, one historical-store skip**; this is not a green suite. The 86 are credible inherited defects: 20 unguarded-value cases and 66 older export-signature mismatches. Historical source/test hashes match the entering revision, the recorded isolated reproductions fail independently, and source inspection confirms `.get()` publication and the incompatible signatures (`20260830-stress-fence/study.py:171`, `20260901-sustainment-fence/study.py:208`, `20260903-priced-levers/study.py:235`, `20260907-minor-radius/study.py:604`). These defects do not exempt new current-route outputs from the contract. Their repair requires separate historical-export scope. Existing failed logs are preserved without relabeling.

## Certification

Evidence and exact commands are in `audit-evidence/commands.md`. `check.py`/`checks.json` establish preservation, native metadata, baseline metadata and graph reproduction. `controls.json`, `verification_summary.json` and `package_identity.json` retain fresh stored-execution results; the temporary store path is in `controls.log`. `current-tests.log` and `current-publication-tests.log` retain fresh tests. Counts overlap implementation runs and must not be summed across reports.

All spec criteria and the plan audit gate are marked complete. Parent owns the CURRENT_WORK status update and certificate freeze. No commit was made by this auditor.

**Not checked:** Integration, pin promotion, a new study, historical exporter repair or full historical re-execution; independent recertification of underlying source physics, finance/calendar choices, held efficiencies or design-point equipment scaling; rerunning the separately audited model's full validation battery. WI-050's baseline divertor violation, ten inherited Level 2 findings, and Level 6's 227 inherited plus two accepted introduced checker findings remain. This certificate establishes current package consumer readiness, not plant feasibility, all-suite success or acceptance of residual goal findings.
