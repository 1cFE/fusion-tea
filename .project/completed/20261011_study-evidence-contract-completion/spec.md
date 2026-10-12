# Spec: Study Evidence Contract Completion

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-09-07T16:50:29-07:00
**Complexity:** MEDIUM
**Branch:** `feat/demo-maturation`

---

## Problem

The three-repository numeric-evidence repair is merged, and fusion-tea has a shared route that can reject incomplete evidence. Seven current stellarator study exporters bypass that contract: they retrieve declared outputs with permissive lookups and do not give their channel maps to the execution route. Missing evidence can therefore become blank CSV fields, while the automatically discovered publication suite reports 75 failures. The package annex describes the repaired contract, but the reusable run-study instructions do not require it and the live backlog still describes the upstream defect as open. Fixing only the exporters would leave the next study author able to repeat the same failure.

This is a coding-PM contract-completion item alongside the grounded `minor-radius` goal. It must make publication trustworthy without changing, delaying, or consuming the state of that goal.

## Success Criteria

- [ ] Every stellarator study exporter present at the implementation cutoff refuses publication when any declared result is absent, null, or non-finite; valid zero values remain publishable, and a refusal leaves any existing output file byte-for-byte unchanged.
- [ ] Successful and resumed study cases are checked for present, non-null declared outputs before they can be persisted; publication then applies the stricter non-finite check.
- [ ] The automatically discovered exporter regression covers every current study, including exporters that require arm or oracle context, and `tests/study/test_study_publication_fail_closed.py` completes with zero failures without weakening its invalid-value matrix.
- [ ] A real generated-package round trip proves that representative multi-output numeric channels survive TEAx evidence storage, reopening, and CSV publication without blank fields.
- [ ] The live operator surface is audited as one change: `.claude/skills/run-study/{SKILL.md,runbook.md,record-template.md}`, `modeling_project/STUDY_POLICY.md`, `exploration/stellarator_e2e/studies/ANNEX.md`, `.project/backlog/BACKLOG.md`, and applicable product-promise documentation are each updated or carry a recorded no-change disposition explaining why they are not part of the contract.
- [ ] A repository-wide search finds no other live command, skill, template, runbook, policy, or package-level instruction that teaches study creation or publication while omitting or contradicting the completed evidence contract.
- [ ] A fresh operator following the native runbook can identify the study, case, and channel that caused a refusal and can retry or resume safely from the recorded lineage without builder memory, hidden repair state, or manual store surgery; automated coverage exercises the resumed-case path.
- [ ] The live backlog defect receives a terminal disposition that cites the implementation and validation evidence, while immutable first-sighting study records and the active goal trail remain unchanged.
- [ ] The `minor-radius` goal can continue from its existing grounded state with its files, active branch state, package pin, stores, study records, and native workflow untouched by this item's implementation and validation.

## Known Requirements

- **[NEED]** The in-progress goal must not be disrupted. `[OWNER-VERBATIM 2026-09-07]` “a goal is in progress, so I don't want to disrupt it”.
- **[NEED]** Every relevant command, skill, and documentation surface must be brought current in the same work item as the code and tests. `[OWNER-VERBATIM 2026-09-07]` “I want to make sure we update any/all relevant commands/skills/documentation at the same time”.
- **[HARD]** Numeric-publication validation has two different timing rules: absent or null required outputs are refused before persistence, while non-finite numeric results may remain stored as model results but are refused before any CSV bytes are written. This is the existing shared-route contract at `exploration/stellarator_e2e/studies/study_route.py:194-311` and `exploration/stellarator_e2e/studies/ANNEX.md:88-90`.
- **[HARD]** Evidence-schema-v2 stores cannot recover outputs that were never recorded and are lineage-incompatible with v3 execution. Historical v2 stores, CSVs, records, and their stated limitations remain historical rather than being rewritten or resumed under v3. This is forced by the TEAx evidence contract and recorded at `exploration/stellarator_e2e/studies/ANNEX.md:90`.
- **[HARD]** The implementation may not use the primary checkout's mutable goal state as a work surface. `work/orchestration/goals/minor-radius/` is grounded under the goal-native workflow, and the primary checkout already contains owner changes. Isolation must preserve both sets of work.
- **[INHERITED]** The ARIES-CS hold-out remains sealed, this item reads no barred material, and the item carries `knowledge/holdout/aries-cs/PROTOCOL.md` as Required Reading. Source: `.project/backlog/epic_stellarator_mbse_demo.md:17` and `knowledge/holdout/aries-cs/PROTOCOL.md` §§ 1–4, 8.
- **[INHERITED]** A non-builder must be able to run and resume the study seam from the runbook and native records alone. Evidence refusal and recovery therefore cannot depend on builder memory or an unrecorded repair step. Source: `.project/product/0001-goal-round-native-operability.md`, backed by `.project/concepts/goal-driven-model-development-harness.md` § Success Criteria.
- **[INFERRED]** The completed regression continues discovering new study exporters automatically, so future exporters enter the publication contract by default rather than through a manually maintained list.
- **[INFERRED]** The work is confined to fusion-tea. The merged TEAx and sysml-codegen contracts remain inputs and are not reopened unless implementation produces new evidence that contradicts the completed research.
- **[INFERRED]** Historical records may receive a new addendum only if the implementation uncovers a factual error in a record's existing account; they are not edited to make old evidence look as though it ran under the new contract.

## Non-Goals

- Changing the stellarator model, regenerating its package, moving the `minor-radius` goal's pin, executing that goal's study, or editing anything under `work/orchestration/goals/minor-radius/`.
- Changing TEAx numeric projection or sysml-codegen output emission; their merged fixes and acceptance tests are upstream dependencies of this item.
- Re-executing all historical studies or manufacturing values for schema-v2 evidence that omitted them.
- Standardizing every study's domain-specific CSV columns, arm model, or oracle calculations beyond what evidence-safe invocation requires.
- Repairing the separate TEAx executor-revision reporting gap in `scripts/study/verify.py`.
- Addressing unrelated run-study backlog findings, changing goal-layer semantics, altering the clean-room protocol, or revealing ARIES-CS.

## Open Questions / Deferred to design

- Whether exporters should converge on one callable protocol or the regression suite should use explicit adapters for existing `arms` and `oracle` arguments. A common protocol reduces future drift; adapters avoid changing domain-specific exporter APIs.
- Whether the earlier backlog request for a declaration-time scalar-channel gate still adds useful protection beyond the merged TEAx v3 projection and the shared route's pre-persistence check. If retained, design must give the preflight or indicator layer an authoritative exporter-channel declaration rather than imply it already has one.
- Whether evidence schema version and the required-channel map belong in `snapshot.json` and `record-template.md`, or whether the recorded TEAx revision plus result artifacts already provide the right provenance boundary.
- Which instruction is the single rule home for numeric publication. The runbook must make the operator obligation unavoidable; design decides whether `STUDY_POLICY.md` also needs an owner-ratified general rule or should only point to the operational contract.
- Whether the focused real heating-chain round-trip from local commit `eecf2f45` should be reconstructed directly or replaced by an equivalent current-study fixture with less setup coupling.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_stellarator_mbse_demo.md` Item 10; related capability owner: `.project/backlog/epic_run_study_capability.md`
- **Required Reading:** `.project/concepts/stellarator-demo-maturation.md`; `.project/active/demo-depth-rubric/spec.md`; `knowledge/holdout/aries-cs/PROTOCOL.md`
- **Research:** `.project/research/20260907-161438_numeric-evidence-merge-and-demo-follow-through.md`
- **Defect record:** `.project/backlog/BACKLOG.md:37`; `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` sightings `20260821-power-cycle-ab#5`, `20260901-sustainment-fence#3`, `20260903-priced-levers#4`, and `20260903-wall-and-heating#4`
- **Product promise:** `.project/product/0001-goal-round-native-operability.md`
- **Product lens:** `.project/active/study-evidence-contract-completion/product-lens.md` (latest verdict)
- **Design:** `.project/active/study-evidence-contract-completion/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `$my-design` in an isolated worktree that does not share the `minor-radius` goal's mutable state.
