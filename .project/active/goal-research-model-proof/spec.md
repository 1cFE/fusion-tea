# Spec: GSTH Item 5 — Research-to-Model Round Proof

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-27
**Complexity:** HIGH
**Branch:** `feat/goal-research-model-proof`
**Epic:** `.project/backlog/epic_goal_strategy_task_harness.md@83d6fc6c` § Item 5

---

## Problem

The goal layer has never run the sequence it exists for. Item 4 proved a goal can be grounded, interrupted, resumed, and reviewed — but it ran on manual seams and it never had to go get evidence it did not have. Item 2 built the native research seam and proved it against fixtures, offline. Nothing has yet put the two together: **no goal round has discovered a prerequisite inside a bounded model task, acquired evidence through the native seam, and re-authorized modeling from the recorded result.** `[INHERITED: epic_goal_strategy_task_harness.md § Item 5 Current State]`

The second gap is about judgment, not machinery. The owner's requirement is that criticism sits *before* work compounds on a misread — `[OWNER-VERBATIM]` "Study > Analysis > Dispositions Plan / Critic looks at the analysis and plan and can push back on either/both / Those docs get updated and re-reviewed, looping as necessary" (`.project/concepts/goal-driven-model-development-harness.md:33`). Item 1 wrote that checkpoint into `GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint. No live round has ever passed through it. A gate that has never bound is not yet evidence of anything.

There is a real need waiting. Discovery row `20260821-power-cycle-ab#3` records that the stellarator's `p_pump` = 1.0 MW is roughly 100× below admissible helium-primary circulator figures, understating `rec_frac` in every arm of both committed A/B studies; the row's own disposition says "re-sourcing is a separate modeling item; item not yet minted" (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a:9`; `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 15`). DI-008 states the band (2–6 % of blanket thermal power, ~60–190 MW for Stellaris) and names its authority, but its strongest primary — Moscato et al. SOFT 2018, WPBOP-CPR(18) 20276 — is marked "open PDF, **not ingested**" (`knowledge/KNOWLEDGE.md@ffa5c54c` DI-008). The WI-031 research round said the same thing and routed it to a modeling item that was never minted (`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c` § R4). So the modeling work is real, the source gap under it is real, and the row is still open.

`[OWNER 2026-08-27]` **This is the live need for the proof.** A new goal is grounded on it under `work/orchestration/goals/`; the only existing goal, `cryo-volume-basis`, is closed and is not reopened. The ruling was made with the conflict surfaced: it takes the `p_pump` re-source **off** Run-Study Item 6 Phase 4's close list.

`[OWNER]` The obligation this work runs under is that the proof stays lean: no envelopes, ledgers, digests, idempotency, reconciliation, or dispatcher machinery unless a recorded run failure promotes it (epic § Epic Strategy, Hardening rule; sourced to `goal-strategy-task-harness-design-review.md` § Resolutions P2/M4). Prose artifacts and native facts only.

**This is a proof item, and honest outcomes are first-class.** A `STRATEGY_BLOCKER` close, an `OPERATOR_QUEUE` return, or a `BOUNDED_NEGATIVE` from the research seam are all valid results. The item is not built so that only the positive path can succeed.

## Success Criteria

The six epic criteria, plus two this item adds. Each is verified against disk in `verification_record.md`, not asserted.

- [ ] A bounded model task returns a real `PREREQUISITE` with native evidence and no predicted future task list. `[INHERITED: epic § Item 5]`
- [ ] A fresh critic reviews the reading and the proposed dispositions before any research or model follow-up begins; the revisions and the final verdict are recorded as `C-00N.rK` entries. `[INHERITED: epic § Item 5]`
- [ ] The Item 2 seam returns registered MR-4-citable evidence or an honest strategy blocker, with no hand-written registry step anywhere in the path. `[INHERITED: epic § Item 5]`
- [ ] Under the positive path, a newly authorized modeling task advances the native work item under the same strategy and preserves comparison meaning. `[INHERITED: epic § Item 5]`
- [ ] Every touched finding receives a joined disposition update, and accepted learning cites the research/model evidence. `[INHERITED: epic § Item 5]`
- [ ] The round closes through `RoundResult` and a fresh `RoundReview` without mirroring modeling-PM state. `[INHERITED: epic § Item 5]`
- [ ] `GOAL_RUNBOOK.md` § The native seams marks `research` as native rather than "pending native repair", and the change is made after the live round exercised the seam, not before. `[NEED — OWNER 2026-08-27, in-scope ruling at Align]`
- [ ] Every prose failure the run hits is recorded, and no hardening-path mechanism appears without the recorded failure that promotes it. `[INHERITED: epic § Success Criteria, last item]`

**Not a criterion, deliberately:** that the round reaches the positive path. If the seam queues or returns a bounded negative, or the evidence moves the premise, the round closes on that and the item is still complete. What must not happen is a manufactured positive.

## Known Requirements

### A. The goal and its grounding

- **[NEED]** `[OWNER 2026-08-27]` **R-A1** — A new goal directory under `work/orchestration/goals/` is grounded on the `p_pump` re-source need, citing discovery row `20260821-power-cycle-ab#3`, DI-008, and the study record's § 15 as its evidence. `cryo-volume-basis` is not reopened.
- **[NEED]** `[OWNER 2026-08-27, reserved gate (a)]` **R-A2** — The goal's question and its "answered when" terms are the owner's, settled at grounding. The run parks and asks; no task starts before the owner has ruled on both.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Grounding a goal]** **R-A3** — The goal is grounded only when all five field classes are non-hollow: grounding evidence, answer contract, invariants, limits, reserved gates. A goal hollow in any of them authorizes no task.
- **[NEED]** `[OWNER 2026-08-27, reserved gates (b) and (c)]` **R-A4** — `goal.md` § Reserved gates names, at minimum: any model or knowledge mutation beyond the goal directory (the work item lands through the modeling PM; the go/no-go is the owner's), and the close ruling if the round ends on a judgment call.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Limits]** **R-A5** — `goal.md` restates every limit explicitly, including the checkpoint revision cap (R-C3). Nothing is inherited silently.
- **[INFERRED]** **R-A6** — `goal.md` § Invariants names the channel a `p_pump` change travels — `p_pump` → thermal balance and the recirculating sum → `rec_frac` and `p_net` → the `recirc_ok` and `net_positive` verdicts and LCOE (`models/library/analyses/mfe_power_balance.sysml:119,135`) — and states that the change moves every arm of both committed A/B studies equally. This is the invariant most likely to produce an honest close, so a round must be able to see it before it runs, not after.
- **[NEED]** `[OWNER 2026-08-27, conflict surfaced at Align]` **R-A7** — The removal of the `p_pump` re-source from Run-Study Item 6 Phase 4's close list is recorded where a Phase 4 operator will read it (`.project/CURRENT_WORK.md` names it in the Phase 4 next-up entry today).

### B. The bounded model task and its `PREREQUISITE`

- **[INHERITED: epic § Item 5 scope 2]** **R-B1** — The round's first task is a bounded *modeling* objective on the `p_pump` value. Its `### T-00N scope` names no research task and carries no future task list.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Running one task]** **R-B2** — `PREREQUISITE` is discovered as a return, never predicted in a scope. A scope that lists its own prerequisites is a plan.
- **[INFERRED]** **R-B3** — This spec's expectation that the task will hit a source prerequisite is a proof obligation on the item, not an instruction to the task. If the bounded modeling objective can be met without one, that is recorded as what happened; the first success criterion then goes unmet and is owner-visible. A prerequisite is not manufactured to satisfy this document.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Running one task]** **R-B4** — Every return carries its outcome, evidence refs, the goal-level reading of them, and the five decision fields for each goal-level decision: the finding or trigger; the decision and its reason; the tier; who decided; what changed.

### C. The one critic checkpoint

- **[NEED]** `[OWNER 2026-08-25, epic § Success Criteria]` **R-C1** — A fresh non-author critic reviews the reading and the proposed dispositions **before any semantic follow-up task executes**. The author revises until the checkpoint passes or its declared cap produces an owner-visible stop.
- **[INFERRED]** **R-C2** — The reading under review is of the *already committed* study record `20260821-power-cycle-ab@881d4448` § 15 finding `#3` and its supporting knowledge (DI-008), together with the model task's `PREREQUISITE` return. This round executes no study — study execution is Item 6's — so the runbook's trigger phrase ("after a study reading produces proposed dispositions", § The pre-execution disposition checkpoint) is satisfied by a reading of committed study evidence rather than of a freshly executed run. *Surfaced rather than resolved silently: a strict reading of that phrase would mean the checkpoint never fires in this item, which contradicts the epic criterion it exists to prove. If the owner reads the trigger more narrowly, the runbook sentence is what needs amending, not this item's checkpoint.*
- **[NEED]** `[OWNER 2026-08-25; cap value inherited from `GOAL_RUNBOOK.md@1d43dc5b` § Limits]` **R-C3** — **The cap is 2 revisions (3 submissions)**, restated in `goal.md`. At the cap the round writes `### Stop — YYYY-MM-DD` of kind `cap`, naming the unresolved dispositions and what the owner must decide. **The cap stops the work; it never releases it.** Execution is not permitted past an unpassed checkpoint.
- **[INHERITED: epic § Item 5 Out of Scope]** **R-C4** — Exactly one checkpoint, placed as above. Routine native stages get no separate goal critics; their own reviews are native.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § What "fresh" means]** **R-C5** — "Fresh" is a session boundary, not a work boundary: the critic is never the author's session. An agent that cannot obtain one writes the handoff stop and stops; it does not review its own dispositions and does not wave the gate through.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § The pre-execution disposition checkpoint]** **R-C6** — Each submission is a new `### Checkpoint C-00N.rK` entry naming the reviewer, the reading, the dispositions, the verdict, and what the author changed. A previous entry is never amended; the sequence of submissions is the record of the disagreement.

### D. The native research seam

- **[INHERITED: epic § Item 5 scope 3; `docs/research_seam_operator_guide.md@9637f1b7`]** **R-D1** — The research is run through the Item 2 seam natively: `scripts/research_seam.py` for the request and the run record, `scripts/source_registry.py` for the one write into `knowledge/`, driven by `/research-acquire`. No hand-written `SOURCE_INDEX.md` entry, manifest row, or source directory appears anywhere in the path.
- **[INFERRED]** **R-D2** — The request's `consumer` field names the live need by native id — the discovery row `20260821-power-cycle-ab#3`, or the modeling work item once it exists — so the request, its run, and any bounded negative key to the thing that is waiting.
- **[INHERITED: `docs/research_seam_operator_guide.md@9637f1b7` § The four return classes]** **R-D3** — The seam's native return class (`REGISTERED` / `OPERATOR_QUEUE` / `BOUNDED_NEGATIVE` / `BLOCKER`) is preserved verbatim in the trail and routed as it stands. The goal layer reads it; it does not re-grade it.
- **[INHERITED: `docs/research_seam_operator_guide.md@9637f1b7` § Commit the run directory with the work]** **R-D4** — The request, the run record, the receipts, the return, and any bounded negative are committed as evidence alongside the round.
- **[INHERITED: Item 2 spec R-C3, `[OWNER 2026-08-25]`]** **R-D5** — Acquisition may register sources; it must not mint a DI. Minting a DI or amending DI-008 is a knowledge mutation beyond the goal directory and therefore a reserved gate (R-A4).
- **[INFERRED]** **R-D6** — `OPERATOR_QUEUE` and `BOUNDED_NEGATIVE` are routed as real results. A queued source hands to the owner with its reason; a bounded negative is cited by whatever was waiting on it. Neither is retried into a positive by hand.

### E. Resuming modeling, or closing honestly

- **[INHERITED: epic § Item 5 scope 3]** **R-E1** — If the registered evidence preserves the strategy and comparison meaning, the round records a new bounded modeling task and advances the native work item through the modeling PM's own operations.
- **[NEED]** `[OWNER 2026-08-27, reserved gate (b)]` **R-E2** — Minting or advancing that work item is a reserved gate. The run parks and asks; the go/no-go is the owner's.
- **[INHERITED: epic § Item 5 scope 3]** **R-E3** — If the evidence changes the premise the strategy rests on, the round closes as `STRATEGY_BLOCKER` rather than forcing the positive path.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § The native seams]** **R-E4** — Any regeneration, verification, or pinning the modeling work implies is out of this round: that is the `integrate` seam and Item 6's step. A round that reaches it returns `PREREQUISITE` naming the seam.

### F. Findings, closure, and review

- **[INHERITED: epic § Success Criteria; ADR-004]** **R-F1** — Every open `DISCOVERY_LOG.md` row the round's evidence touches receives a joined `<study-id>#<n>` disposition row, appended under the same id, with status and changed-or-next reference. No touched row returns `unrouted`. A first-sighting row is never edited — the study executor remains the first-sighting writer.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § The discovery log]** **R-F2** — No id is minted. A finding the round discovers itself is not a log row: it goes to `learnings.md`, a native work item, the research seam, or an ADR, and the trail cites it.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Opening and closing a round]** **R-F3** — The round closes on exactly one of the six triggers, with a `### Round N result` carrying intent met/unmet, the task sequence, the last semantic outcome, the **derived** stop reason, the evidence refs, the proposed learning delta, and the finding dispositions.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § The fresh review]** **R-F4** — A fresh `RoundReview` reads the round end to end after the result is written, returns `PASS` / `FINDINGS` / `OWNER_GATE`, and accepts, corrects, or rejects the learning delta before it is appended to `learnings.md`. The round agent does not review its own round.
- **[INHERITED: ADR-006; `CLAUDE.md` two-PM rule]** **R-F5** — No modeling-PM or coding-PM state is mirrored into the goal directory. Evidence is cited `<path>@<commit-sha>`; a citation that pins nothing says "unpinned; no native digest" in the citation itself.

### G. The runbook flip

- **[NEED]** `[OWNER 2026-08-27]` **R-G1** — `GOAL_RUNBOOK.md` § The native seams: the `research` row changes from "**pending native repair**" to native. The `integrate` row is Item 6's and is not touched here.
- **[INFERRED]** **R-G2** — The prose bullet under that table that directs a round to the WI-031 hand pattern is part of the same row and retires with it, replaced by a pointer to `docs/research_seam_operator_guide.md`. Leaving it would tell the next round to hand-write what the seam now does.
- **[INFERRED]** **R-G3** — The flip lands after the live round has actually invoked the seam, so the runbook change rests on the run rather than on the shipment.

### H. Evidence and the hardening bar

- **[NEED]** `[OWNER — epic § Epic Strategy, Hardening rule]` **R-H1** — No task envelope, event ledger, digest comparison, idempotency layer, reconciliation pass, or dispatcher enters this item unless a recorded run failure promotes it, and the failure is owner-visible when it does.
- **[INFERRED]** **R-H2** — `verification_record.md` maps each success criterion above to disk evidence — a path, a commit, a return file — and records every point where the prose route was ambiguous, misread, or failed, whether or not it promoted anything. Item 4's record (`.project/completed/20260827_goal-cold-pickup-proof/verification_record.md`) is the shape to match.
- **[INHERITED: epic § Item 5 Deliverables]** **R-H3** — The item ships `spec.md`, `design.md`, `plan.md`, `verification_record.md`, the goal's `goal.md` / `trail.md` / `learnings.md`, the joined discovery-log rows, the independent disposition-critic artifact, the final `RoundReview`, and the native research and modeling artifacts referenced by id and path.

## Non-Goals

- **Study execution, package regeneration, and pin promotion.** Item 6 owns those. A round that reaches them returns `PREREQUISITE`. `[INHERITED: epic § Item 5 Out of Scope]`
- **More than the one bounded live need.** The other open rows in `DISCOVERY_LOG.md` (`#1`, `#2`, `#5`) are not this item's, except where this round's own evidence touches them, in which case R-F1 applies. `[INHERITED: epic § Item 5 Out of Scope]`
- **Research or model writes outside their native workflows.** `[INHERITED: epic § Item 5 Out of Scope]`
- **A critic per native stage.** One checkpoint, placed as R-C1 says. `[INHERITED: epic § Item 5 Out of Scope]`
- **Repairing the `integrate` seam or flipping its runbook row.** Item 6's. `[NEED — OWNER 2026-08-27]`
- **Reopening the `cryo-volume-basis` goal.** Closed 2026-08-27 by owner ruling; it is read here as a worked example of artifact shape only. `[NEED — OWNER 2026-08-27]`

## Open Questions / Deferred to design

- **The goal slug and directory name.** Follows from the question the owner settles at grounding (R-A2), so it cannot be fixed here.
- **How many rounds this item covers.** The epic's sequence is one round (`model → research → model`), but a `STRATEGY_BLOCKER` or an unresolved gate could close round 1 before the modeling resumes. Whether the item then opens round 2 or stops is a design call, bounded by the goal's round limit.
- **Whether the follow-up modeling work item lands inside this item or is handed to the owner at the gate.** R-E2 makes the go/no-go the owner's; how far the round carries the item once authorized — spec only, or through implement — is design's to scope against the item's effort budget.
- **Whether a covering branch is declared before the run.** Item 4 declared, ahead of its run, which outcomes would count as honest non-exercise of a criterion, and the audit relied on that ancestry. Doing the same here would pre-commit the honest-outcome branches (R-B3, R-D6, R-E3) so they cannot be re-read as failure after the fact. Recommended, but it is a design and plan decision.
- **How the checkpoint critic and the round reviewer are obtained.** The runbook says an agent stops and hands back (R-C5). Whether this item's execution uses fresh operator-started sessions throughout, and how their inputs and outputs are kept as evidence, is design's.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md@83d6fc6c` § Item 5
- **Required Reading:**
  - `work/orchestration/GOAL_RUNBOOK.md@1d43dc5b` — the operating contract; cited throughout, restated nowhere
  - `.project/completed/20260827_goal-harness-contract/` — Item 1 (the contract, ADR-001–007)
  - `.project/completed/20260827_goal-research-seam/` — Item 2; `scripts/research_seam.py`, `scripts/source_registry.py`, `docs/research_seam_operator_guide.md@9637f1b7`
  - `.project/completed/20260827_goal-cold-pickup-proof/` — Item 4, the manual-seam proof this item extends
  - `.project/concepts/goal-strategy-task-harness-design.md` § Task-grain invocation, Native seams, Round Semantics, Findings and Learning, Review Pattern
  - `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words (critic placement, `:33`) and Success Criteria 2, 4–6
  - `.project/research/20260822-120756_research-extraction-harness.md` § the one manual trace, patterns P1–P10
  - `work/orchestration/goals/cryo-volume-basis/` — worked example of `goal.md`/`trail.md` shape; closed, not reopened
  - `knowledge/KNOWLEDGE.md@ffa5c54c` DI-008 and `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448` § 15 finding `#3` — the native evidence behind the live need
  - `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c` § R4 — the prior routing of this same need
- **Product-lens:** `.project/active/goal-research-model-proof/product-lens.md`
- **Design:** `.project/active/goal-research-model-proof/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
