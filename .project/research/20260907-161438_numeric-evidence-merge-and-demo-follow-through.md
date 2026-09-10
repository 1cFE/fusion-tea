---
date: 2026-09-07T16:14:38-07:00
researcher: Codex
topic: Numeric evidence merge status and remaining demo follow-through
tags: [stellarator, evidence, teax, sysml-codegen, studies]
status: complete
last_updated: 2026-09-07
---

# Numeric Evidence Merge and Demo Follow-Through

## Research Question

The owner recalled merging the blank numeric-evidence fix across fusion-tea, TEAx, and sysml-codegen. Determine whether those fixes landed, whether the current stellarator studies consume them, and why the evidence-surface test still reports failures.

## Summary

The owner is correct: the three-repository repair merged on 2026-09-06. TEAx PR #5 fixed numeric exit projection, fusion-tea PR #111 added fail-closed study publication, and sysml-codegen PR #14 added cross-repository acceptance coverage for the generator's already-correct multi-output shape.

The current burn-control study demonstrably uses the repaired TEAx revision and evidence schema v3. Its stored results contain the heating and sustainment outputs that were blank under schema v2.

The remaining 75 test failures do not reopen the upstream defect. They come from an unmerged, now-stale demo adaptation branch. Seven study exporters added after or outside fusion-tea PR #111 have not adopted the shared `required_channels` contract, and five of those exporters also expose signatures that the merged generic test helper cannot invoke.

## Detailed Findings

### The three core changes merged

- TEAx PR #5 merged as `8d877460ac4f6f264561d916e40c1708adb13397` with the title “Preserve numeric exit outputs in study evidence.” The implementation accepts bare or one-level-wrapped real numbers, converts them to floats, preserves existing exit keys, and advances evidence from schema v2 to v3. Relevant code: `T:packages/teax-simkit/simkit/evaluation/projection.py:26`, `T:packages/teax-simkit/simkit/evaluation/projection.py:78`, `T:packages/teax-simkit/simkit/evaluation/evaluator.py:109`, and `T:packages/teax-simkit/simkit/evaluation/evidence.py:110`.
- fusion-tea PR #111 merged as `6f7ff023a4079c34c86619470ab63db785cb691b`. Current `feat/demo-maturation` contains it through merge `2de2b167`. The shared route now requires callers to name required output channels, validates both resumed and newly evaluated cases before persistence, and refuses missing or null comparison coverage. Relevant code: `F:exploration/stellarator_e2e/studies/study_route.py:181`, `F:exploration/stellarator_e2e/studies/study_route.py:288`, and `F:exploration/stellarator_e2e/studies/study_route.py:304`.
- sysml-codegen PR #14 merged as `40a724c4a1f6561325defb4aa92556734de3743a`. It added acceptance tests and documentation rather than changing production generation. The generator already emitted separate bare primitive exit channels for multi-output calculations. Relevant code: `C:src/sysml_codegen/generation/pipeline.py:155`, `C:src/sysml_codegen/generation/pipeline.py:204`, `C:src/sysml_codegen/generation/pipeline.py:284`, `C:tests/execution/test_numeric_evidence_teax.py:19`, and `C:.project/numeric-evidence-acceptance.md:5`.

Repository prefixes in this document are `F:` for `/home/reid/1cfe/fusion-tea/`, `T:` for `/home/reid/1cfe/teax/`, and `C:` for `/home/reid/1cfe/sysml-codegen/`.

### The current study path consumes the repaired runtime

- `F:.venv/integration.env:1` selects the sibling TEAx checkout at `/home/reid/1cfe/teax`.
- The burn-control integration return expects and records TEAx merge `8d877460`, and its checks pass. Relevant evidence: `F:work/orchestration/goals/burn-control/evidence/T-002_integration_return.json:46`, `F:work/orchestration/goals/burn-control/evidence/T-002_integration_return.json:77`, and `F:work/orchestration/goals/burn-control/evidence/T-002_integration_return.json:109`.
- The burn-control snapshot records evidence schema v3 and TEAx revision `8d877460`. Relevant evidence: `F:exploration/stellarator_e2e/studies/20260907-burn-control/snapshot.json:219` and `F:exploration/stellarator_e2e/studies/20260907-burn-control/snapshot.json:841`.
- The burn-control baseline result contains the four previously blank heating outputs and the sustainment outputs. Relevant evidence: `F:exploration/stellarator_e2e/studies/20260907-burn-control/results/baseline_result.json:46` and `F:exploration/stellarator_e2e/studies/20260907-burn-control/results/baseline_result.json:89`.
- The burn-control validation compared a v2 record produced with the old executor against the v3 fixed executor and found all 7,712 committed store channels and verdicts bit-identical. The repair changed evidence capture, not model results.

### Why 75 evidence-surface tests fail

The focused command `UV_CACHE_DIR=/tmp/fusion-tea-uv-cache uv run python -m pytest tests/study/test_study_publication_fail_closed.py -q --tb=short` reports 75 failed, 41 passed, and 2 skipped.

Seven current exporters still read `case.outputs.get(channel)` and call `run_points` without `required_channels`:

- Stress fence: `F:exploration/stellarator_e2e/studies/20260830-stress-fence/study.py:151` and `F:exploration/stellarator_e2e/studies/20260830-stress-fence/study.py:227`.
- Sustainment fence: `F:exploration/stellarator_e2e/studies/20260901-sustainment-fence/study.py:185` and `F:exploration/stellarator_e2e/studies/20260901-sustainment-fence/study.py:274`.
- Priced levers: `F:exploration/stellarator_e2e/studies/20260903-priced-levers/study.py:235` and `F:exploration/stellarator_e2e/studies/20260903-priced-levers/study.py:335`.
- September 3 wall and heating: `F:exploration/stellarator_e2e/studies/20260903-wall-and-heating/study.py:380` and `F:exploration/stellarator_e2e/studies/20260903-wall-and-heating/study.py:521`.
- September 4 wall and heating: `F:exploration/stellarator_e2e/studies/20260904-wall-and-heating/study.py:389` and `F:exploration/stellarator_e2e/studies/20260904-wall-and-heating/study.py:538`.
- Stored-energy basis: `F:exploration/stellarator_e2e/studies/20260905-stored-energy-basis/study.py:510` and `F:exploration/stellarator_e2e/studies/20260905-stored-energy-basis/study.py:784`.
- Burn control: `F:exploration/stellarator_e2e/studies/20260907-burn-control/study.py:535` and `F:exploration/stellarator_e2e/studies/20260907-burn-control/study.py:928`.

The failure count is deterministic. The generic suite tests two case positions against five invalid forms across seven uncovered exporters, which produces 70 failures. Five exporters require extra `arms` or `oracle` export arguments, while the merged helper calls each exporter with only cases and a path; their valid-value cases add five `TypeError` failures. Total: 75.

### The missing work exists on a stale local branch

The local branch `fix/numeric-study-evidence-demo` ends at `c089d8fb`. Commit `1afe3bf0` adapted the five demo exporters that existed at that point. Commit `eecf2f45` added a signature-aware export helper and a real heating round trip. Later commits recorded validation and provenance.

That branch was deliberately not merged or pushed because it was based on a local demo-maturation history carrying unrelated owner work. It also predates the stored-energy and burn-control studies, so merging it now would still leave two exporters uncovered and risks deleting or disturbing newer study work.

### Executor revision bookkeeping is a separate gap

The integration environment and burn-control snapshot prove which TEAx revision ran, but the general verification manifest still reports the TEAx executor revision as unrecorded. This weakens reproducibility bookkeeping, but it is not the cause of blank numeric outputs or the 75 publication-test failures.

## Architecture Insights

The repair has three distinct responsibilities. sysml-codegen emits primitive output channels, TEAx projects those numeric channels into evidence, and fusion-tea refuses to publish a study when its claimed evidence channels are absent or unusable. Treating all three as one “evidence surface” hid the fact that the upstream runtime is repaired while some downstream study adapters remain outside the publication contract.

The dynamic exporter test is useful because it discovers new study modules automatically. Its current invocation logic is too narrow for exporters with study-specific context arguments. A shared exporter protocol or a single adapter layer would prevent each new study from inventing a subtly different publication seam.

Schema v2 stores are historical evidence. The missing values were never stored, so they cannot be recovered by reading them with the fixed runtime. They should remain unchanged rather than being silently reinterpreted as v3 evidence.

## Feasibility Assessment

Finishing the evidence surface is a bounded fusion-tea change. It does not require reopening TEAx or sysml-codegen. The local commits show the intended caller and test patterns, but the changes should be reimplemented against the current studies rather than cherry-picked or merged. The current tree has two newer studies and other intervening edits.

The main implementation risk is inconsistent exporter signatures. Porting only the seven `required_channels` changes will enforce runtime publication, but the generic regression suite also needs a reliable way to supply each exporter's required context. A shared adapter is preferable to a growing collection of name-based exceptions if the studies will continue to multiply.

## Recommendations

1. Do not reopen the TEAx or sysml-codegen fixes. Preserve their current tests as the upstream contract.
2. Reimplement the two useful patterns shown by `1afe3bf0` and `eecf2f45` against current `feat/demo-maturation`: required-channel enforcement in each exporter and signature-aware invocation in the generic test. Do not cherry-pick or merge `fix/numeric-study-evidence-demo` wholesale.
3. Adapt all seven current exporters to declare required channels and use indexed output access after validation. Include stored-energy basis and burn control, which did not exist when the local repair branch was created.
4. Make the dynamic publication test invoke exporters through a shared adapter or explicit per-study fixture that supplies required `arms` and `oracle` context. Keep automatic discovery so new exporters enter the contract by default.
5. Re-run the focused publication suite, then the broader study suite. The immediate acceptance target is zero failures in `tests/study/test_study_publication_fail_closed.py` without weakening its invalid-value matrix.
6. Leave schema v2 evidence artifacts unchanged and label them historical where they are compared with v3 results.
7. Track TEAx executor-revision recording as a separate seam-hardening item. It should not block recognition that the numeric-evidence defect itself is fixed.

## Open Questions

- Should every study exporter adopt one common callable signature, or should the regression suite own adapters for study-specific context? The common signature has a higher migration cost but reduces future drift.
- Should the executor revision live in the general verification manifest, the study package manifest, or both? The current burn-control evidence proves the revision locally, but the broader package contract does not.
