# Audit: Cold-Pickup Administrator Exercise

**Verdict:** Needs Work
**Audited:** 2026-08-20
**Branch:** feat/stellarator-mbse-demo
**Commit:** a27e882c

---

## The Point

The committed study record is the only handoff between the agent that ran a study and the administrator that writes its synthesis. A fresh administrator must recover framing per axis, the LCOE result, named constraint outcomes, and evidence-backed findings from that record alone. Missing facts stay missing. This legacy exercise exists to find holes in the record contract before Item 6 spends a new study run.

## Summary

This is the right exercise, and much of its evidence is solid: the cold-reader prompt is preserved, the scratch inputs match the pre-read commit, the committed synthesis is byte-identical to the reader output, old evidence did not change, and all 273 study tests pass. The product-lens ledger is clear, and SC4 now reflects the owner's approved G1 exception. The remaining blocker is the runbook committing the record before it registers findings. Three findings also lack a direct source beside the claim, but that remains a low-risk, non-blocking traceability issue: the supporting evidence exists elsewhere in the same synthesis and record, so the cost is reader lookup rather than evidence loss or a likely wrong conclusion.

## Product Judgment

**This is the right piece of work, and the ledger gate is CLEAR.** The owner-authorized structured block at `product-lens.md` resolves `spec-F1` and `spec-F2`; the prior owner block resolves `audit-F1` and its associated smell for Item 5. G1 is non-load-bearing here, and the oracle's place in a general study remains a future Align question.

Certification still waits on the runbook commit sequence found by the required fresh final check. The owner chose to leave that issue recorded and unresolved. SC4 now represents the approved G1 exception.

## Findings

### Plan completion

- **Phase 1 verified.** The seven pre-read scratch files hash-match commit `316fc3a0`; the brief was the fresh agent's only prompt; the committed synthesis is byte-identical to the scratch output.
- **Phase 2 evidence boundary verified.** The saved reader trace shows one tool spill file containing output from the allowed scratch `make_report.py`. **[OWNER] 2026-08-20:** this is transport for already-approved evidence, not an outside evidence source. The trace shows no package, work-item, prior-session, or other outside study evidence entering the synthesis.
- **Phase 2 citation validation resolved during the owner walkthrough.** The stencil now treats path and absent-file matches as review prompts rather than automatic failures. The two `_work/` mentions report an exclusion, and the three absent filenames report missing evidence; none supports a claim. The reviewed semantic condition is checked, with no cold-read rerun required.
- **Phase 3 verified after the owner-directed audit correction.** `gaps.md § Cross-check` now preserves all seventeen rows, including mixed inside/outside evidence, the three reader misses, and the disposition of every absence. It was completed from existing artifacts; the cold reader and its synthesis were not rerun or edited.
- **Phase 4 verified after the owner-directed audit correction.** G1 and G2 have dispositions. Absence 8 now separates the two executor bounds recorded in report prose from the missing resolved evidence and the absent beta/TBR values. The synthesis overstatement is preserved as a reader miss rather than silently edited.
- **Phase 5 is partial.** Commits, legacy-evidence immutability, heading count, and the 273-test suite are verified. Certification remains open on the runbook ordering issue. G1 is documented as a future oracle-concept question and no longer blocks Item 5.

### Spec conformance

- **SC1 — minor non-blocking deviation; risk low.** The availability finding at `synthesis.md:97` and process findings at `synthesis.md:114,116` do not directly name their in-directory evidence, contrary to `spec.md:26` and the `[NEED]` at `spec.md:41`. Their support exists elsewhere in the same synthesis and record. This creates lookup friction, not missing evidence or a material correctness risk, and does not block certification.
- **SC2 — met under the owner-confirmed interpretation rule.** `synthesis.md:63-73` keeps the executor's missing historical framing missing, labels `search` and `sensitivity` as the administrator's reading, and cites the in-directory language and data behind that judgment. The brief's no-inference rule bars filling a missing fact or attributing it to the executor; it does not bar a clearly labeled synthesis judgment.
- **SC3 — verified.** The 17-section recovery comparison is complete, and every absence has one honest bucket. Absence 8 distinguishes recorded prose claims from missing resolved evidence.
- **SC4 — verified after owner correction.** A non-load-bearing gap does not need to be applied, but an explicitly authorized optional application is allowed when its edit, reason, and authority are recorded. G1 follows that rule.
- **SC5 — verified as not applicable.** `gaps.md:69-71` states why this was not a zero-gap result.
- **Directory-only `[NEED]` — met under the owner-confirmed provenance rule.** The reader used no study evidence outside the record; a tool-generated copy of an allowed file does not change its provenance.
- **Other tagged requirements — met.** The work uses the tracked evidence surface, follows the synthesis section shape, reports missing facts explicitly, covers both legacy studies, leaves old evidence untouched, runs no new study points, and creates no discovery-log entry.
- **Non-goals respected.** No legacy record retrofit, new study execution, policy amendment, linter, or discovery-log routing was added.

### Design conformance

No `design.md` exists. The owner-approved skip is recorded in `plan.md:8-10`; no silent design deviation was found. The stale design pointer and next step in `spec.md` were corrected as tracking metadata during this audit.

### Code integrity

- **Runbook commit ordering blocks a compliant record.** `runbook.md:215-227` resolves and commits the record, freezes it, and fails closed on any remaining placeholder. Step 15 at `runbook.md:230-240` then fills `record.md § 15 Findings`, whose template still contains placeholders at `record-template.md:206-212`. The record must register findings before the commit/freeze gate.
- **Deferred oracle-contract question.** `.claude/skills/run-study/record-template.md:302-309` uses a smaller digest shape than the canonical tool contract. The owner decided this should not be refined until the workflow decides whether an oracle is mandatory, package-conditional, or outside the study contract. It is not an Item 5 certification condition.
- No unresolved product-drift smell controls this item after that disposition. No god function, implicit mode, parameter sprawl, policy utility, broad exception, silent fallback, or compatibility shim was added.

---

## Certification

Verified: the upstream artifacts and parent epic; all product-lens ledger blocks; preserved cold-reader prompt and tool trace; scratch/pre-read file set and hashes; synthesis byte identity; relevant commits; template heading/token invariants; legacy study immutability; non-goals; and `uv run python -m pytest tests/study -q` (**273 passed in 200.12s**).

Marked: spec SC2 through SC5, the Phase 2 citation validation, the Phase 3 cross-check, the Phase 4 classification, and the Item 5 tracking update are checked. The Item 5 heading remains open. The product-lens ledger is clear; only the runbook sequence remains as a certification blocker. `CURRENT_WORK.md` records Needs Work and removes superseded RUN-STUDY status blocks.

**Not checked:** A browser rendering of `report.html`; the full repository test suite outside `tests/study`; behavior of a capability-compliant Item 6 record; or a corrected end-to-end record writer/administrator seam, because no correction exists yet.

---

## Post-audit disposition — 2026-08-20

**Runbook commit ordering — FIXED by owner instruction ("fix it please").** `runbook.md` steps 14 and 15 swapped: step 14 now registers the findings and appends the discovery-log rows; step 15 resolves the snapshot and commits, with its placeholder check now naming § 15 explicitly. Cross-references renumbered in `run-study-contract/coverage.md` and `run-study-cold-pickup/gaps.md`. Checks: fifteen execute steps in order; record template 17 headings; `git diff --check` clean. The verdict above is left as written; a fresh re-audit owns flipping it.
