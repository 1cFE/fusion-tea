# Spec: GSTH Item 5 — Research-to-Model Round Proof

**Status:** Draft — revised 2026-08-27 against `spec-review.md` (verdict Revise)
**Owner:** Reid W
**Created:** 2026-08-27
**Complexity:** HIGH
**Branch:** `feat/goal-research-model-proof`
**Epic:** `.project/backlog/epic_goal_strategy_task_harness.md@83d6fc6c` § Item 5

---

## Problem

The goal layer has never run the sequence it exists for. Item 4 proved a goal can be grounded, interrupted, resumed, and reviewed — but it ran on manual seams and it never had to go get evidence it did not have. Item 2 built the native research seam and proved it against fixtures, offline. Nothing has yet put the two together: **no goal round has discovered a prerequisite inside a bounded model task, acquired evidence through the native seam, and re-authorized modeling from the recorded result.** `[INHERITED: epic_goal_strategy_task_harness.md § Item 5 Current State]`

The second gap is about judgment, not machinery. The owner's requirement is that criticism sits *before* work compounds on a misread — `[OWNER-VERBATIM]` "Study > Analysis > Dispositions Plan / Critic looks at the analysis and plan and can push back on either/both / Those docs get updated and re-reviewed, looping as necessary" (`.project/concepts/goal-driven-model-development-harness.md:33`). Item 1 wrote that checkpoint into `GOAL_RUNBOOK.md` § The pre-execution disposition checkpoint. No live round has ever passed through it. A gate that has never bound is not yet evidence of anything.

**There is a real need waiting: the modeling work is real, the source gap under it is real, and the row is still open.** The evidence for each of those three, in order.

Discovery row `20260821-power-cycle-ab#3` records that the stellarator's `p_pump` = 1.0 MW is roughly 100× below admissible helium-primary circulator figures, understating `rec_frac` in every arm of both committed A/B studies; the row's own disposition says "re-sourcing is a separate modeling item; item not yet minted" (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md@e891b23a:9`; `exploration/stellarator_e2e/studies/20260821-power-cycle-ab/record.md@881d4448 § 15`).

DI-008 states the band (2–6 % of blanket thermal power, ~60–190 MW for Stellaris) and names its authority, but its strongest primary — Moscato et al. SOFT 2018, WPBOP-CPR(18) 20276 — is marked "open PDF, **not ingested**" (`knowledge/KNOWLEDGE.md@ffa5c54c` DI-008).

The WI-031 research round said the same thing and routed it to a modeling item that was never minted (`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md@ffa5c54c` § R4).

`[OWNER 2026-08-27]` **This is the live need for the proof.** A new goal is grounded on it under `work/orchestration/goals/`; the only existing goal, `cryo-volume-basis`, is closed and is not reopened. The ruling was made with the conflict surfaced: it takes the `p_pump` re-source **off** Run-Study Item 6 Phase 4's close list.

`[OWNER]` The obligation this work runs under is that the proof stays lean: no envelopes, ledgers, digests, idempotency, reconciliation, or dispatcher machinery unless a recorded run failure promotes it (epic § Epic Strategy, Hardening rule; sourced to `goal-strategy-task-harness-design-review.md` § Resolutions P2/M4). Prose artifacts and native facts only.

**This is a proof item, and honest outcomes are first-class.** A `STRATEGY_BLOCKER` close, an `OPERATOR_QUEUE` return, a `BOUNDED_NEGATIVE` from the research seam, or a park at a reserved gate are all valid results. The item is not built so that only the positive path can succeed.

## Success Criteria

The six epic criteria, plus three this item adds. Each is verified against disk in `verification_record.md`, not asserted — every criterion below names the path, commit, or return file that settles it.

**Audit marking, 2026-08-28 (`audit.md`).** A box is `[x]` only where the audit re-ran the evidence against disk and the criterion is met. Retired and non-exercised criteria stay `[ ]` with their disposition named — a non-exercised criterion under a pre-declared covering branch is a declared stop, not a met criterion, and marking it would erase that distinction.

- [ ] **Retired `[OWNER 2026-08-28]`** — ruling verified by audit at `briefs/implement_resume_gate_a.md@c8362239` Ruling 1. A bounded model task returns a real `PREREQUISITE` with native evidence and no predicted future task list. Checked against the task's `### T-00N` scope and return in `trail.md`. `[INHERITED: epic § Item 5]`
- [x] A fresh critic reviews the reading and the proposed dispositions before any research or model follow-up begins; the revisions and the final verdict are recorded as `C-00N.rK` entries. `[INHERITED: epic § Item 5]`
- [ ] **Non-exercised** under the covering branch declared at `covering-branches.md:36@e02ce403` — audit confirmed the branch predates the round. The Item 2 seam is invoked natively and its return is routed as it stands, as one of the seam's four native classes: `REGISTERED` (MR-4-citable evidence), `OPERATOR_QUEUE` (a named candidate handed to the owner with its reason), `BOUNDED_NEGATIVE`, or `BLOCKER`. No hand-written `SOURCE_INDEX.md` entry, manifest row, or source directory appears anywhere in the path. Checked against the seam's run directory and return file. `[INHERITED: epic § Item 5, widened to the seam's four native return classes per `docs/research_seam_operator_guide.md@9637f1b7` § The four return classes]`

  **`OPERATOR_QUEUE` is the likeliest honest return here**, because DI-008's strongest primary — Moscato et al., SOFT 2018, WPBOP-CPR(18) 20276 — is recorded as "open PDF, **not ingested**" (`knowledge/KNOWLEDGE.md@ffa5c54c` DI-008), which is exactly the guide's queue shape: a named candidate blocked on something only a person can resolve (`research_seam_operator_guide.md@9637f1b7:165`). If that is the return, the item does not retry it into a positive and does not re-grade it as a blocker: the queue return is committed as evidence, the round parks it at the owner gate (R-A4/R-E2) with its reason, and the round closes on it honestly. Criterion 3 is met by the honest routing, not by the class of the return.

- [ ] **Non-exercised**, same branch — audit confirmed `work/` untouched vs base `e44498d4` and no WI minted. Under the positive path, a newly authorized modeling task advances the native work item under the same strategy and preserves comparison meaning. `[INHERITED: epic § Item 5]`
- [x] Every touched finding receives a joined disposition update, and accepted learning cites the research/model evidence. `[INHERITED: epic § Item 5]`
- [x] The round closes through `RoundResult` and a fresh `RoundReview` without mirroring modeling-PM state. `[INHERITED: epic § Item 5]`
- [ ] **Non-exercised** — no seam run, so R-G3 has nothing to rest on; audit confirmed the runbook diff vs base is 0 lines and the stale row stands. `GOAL_RUNBOOK.md` § The native seams marks `research` as native rather than "pending native repair", and the surrounding prose agrees with the flipped table (R-G). The ordering is checked by commit: the commit carrying the runbook change is later in `git log` than the commit carrying the seam's run record. `[NEED — OWNER 2026-08-27, in-scope ruling at Align]`
- [ ] **Met on its stated terms, with a ninth entry owed** (`audit.md` Finding 3 and its two companions: the `covering-branches.md:32@e02ce403` citation, the "twelve entries" miscount, the "spec review A9" label). All eight existing entries resolve to real artifacts. `verification_record.md` records every point where the prose route was ambiguous, misread, or failed during the run, whether or not it promoted anything. Checked as a positive obligation — the record exists and its entries resolve to real run artifacts — not as a claim that nothing went unrecorded. `[INFERRED: Item 4's pattern, `.project/completed/20260827_goal-cold-pickup-proof/verification_record.md`]`
- [x] No hardening-path mechanism appears in the shipped item without the recorded run failure that promotes it. Checked against the item's own diff and `verification_record.md`. Audit re-read the whole diff and swept wider than the item directory (`work/`, `exploration/`, `CURRENT_WORK.md`): no mechanism anywhere. `[INHERITED: epic § Success Criteria, last item]`

**Not a criterion, deliberately:** that the round reaches the positive path. Four honest non-positive closes are valid results, and the round is still complete on any of them: the seam returns `OPERATOR_QUEUE`; the seam returns `BOUNDED_NEGATIVE`; the evidence moves the premise and the round closes `STRATEGY_BLOCKER`; or the round parks at a reserved gate and the owner has not ruled by close. The last is near-certain rather than hypothetical — R-A4 and R-E2 make minting or advancing the follow-up work item the owner's go/no-go, so this round parks at least once by construction. A park at a declared gate is a declared stop, not an unmet criterion. What must not happen is a manufactured positive.

Which criteria each of these four outcomes covers is declared before the run, not argued after it (R-H4).

## Known Requirements

### A. The goal and its grounding

- **[NEED]** `[OWNER 2026-08-27]` **R-A1** — A new goal directory under `work/orchestration/goals/` is grounded on the `p_pump` re-source need, citing discovery row `20260821-power-cycle-ab#3`, DI-008, and the study record's § 15 as its evidence. `cryo-volume-basis` is not reopened.
- **[NEED]** `[OWNER 2026-08-27, reserved gate (a)]` **R-A2** — The goal's question and its "answered when" terms are the owner's, settled at grounding. The run parks and asks; no task starts before the owner has ruled on both.
- **[INFERRED]** **R-A2a — staged discovery is the failure mode this item has to avoid.** The question settled at gate (a) is about the **model value**: is `p_pump` = 1.0 MW defensible, and what sourced value should the model carry? It is never phrased as "acquire the Moscato PDF" or as any other research errand. The distinction is the whole proof: a round grounded on the prerequisite and then asked to discover it is restating its inputs, and criterion 1's word "real" would be met by machinery that proves nothing.

  Two consequences bind downstream. First, the bounded task's `### T-00N scope` names a modeling objective only (R-B1) — attempt to re-base `p_pump` from repository-native sources under the goal's invariants — and the research prerequisite must **emerge as its return** when the only citable authority turns out to be un-ingested. Second, `verification_record.md` shows the distinction: what the task was asked for, what it returned, and why the return was a finding rather than a restatement.

  **Spec-level hazard for design to guard:** the grounding exchange itself can destroy this. If the owner-facing grounding conversation writes the research prerequisite into the goal question or into the task scope, the discovery is staged before the run starts and no later care recovers it. Design must say how the grounding exchange and the task brief are kept to the modeling objective.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Grounding a goal]** **R-A3** — The goal is grounded only when all five field classes are non-hollow: grounding evidence, answer contract, invariants, limits, reserved gates. A goal hollow in any of them authorizes no task.
- **[NEED]** `[OWNER 2026-08-27, reserved gates (b) and (c)]` **R-A4** — `goal.md` § Reserved gates names, at minimum: any model or knowledge mutation beyond the goal directory (the work item lands through the modeling PM; the go/no-go is the owner's), and the close ruling if the round ends on a judgment call.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Limits]** **R-A5** — `goal.md` restates every limit explicitly, including the checkpoint revision cap and its number (R-C3, R-C3a). Nothing is inherited silently.
- **[INFERRED]** **R-A6** — `goal.md` § Invariants names the channel a `p_pump` change travels — `p_pump` → thermal balance and the recirculating sum → `rec_frac` and `p_net` → the `recirc_ok` and `net_positive` verdicts and LCOE (`models/library/analyses/mfe_power_balance.sysml:119,135`) — and states the equal-input / unequal-effect distinction explicitly:

  - **The input shift is equal across arms.** `p_pump` is cycle-independent (DI-007), held at 1.0 MW in all four arms, so a re-sourced value adds the same megawatts to every arm's recirculating sum. This is what the study record means when finding `#3` says the understatement "does not bias the A/B" (`record.md@881d4448:245`).
  - **The effect is not equal.** `rec_frac` is the recirculating sum over `p_et`, and `p_et` differs by arm by construction (η 0.333 → 0.47). The arms already sit at different recirculating fractions at the same grid corner — **0.94 / 0.79 / 0.68 by arm** (`record.md@881d4448:208`) — and the `recirc_ok` fence already sits at different radii: violated at **R ≤ 8.0 m** (paper), **≤ 6.5 m** (upstream), **≤ 5.5 m** (both η 0.47 arms), at a = 0.8 m against threshold 0.5 (`record.md@881d4448:56`). An equal addition therefore moves each arm's fence by a different amount and can change the feasible regions unevenly.

  The invariant states this distinction and stops there. It does **not** say whether comparison meaning survives — that is exactly the R-E1 (advance) versus R-E3 (`STRATEGY_BLOCKER`) judgment, and it belongs to the round, decided on the registered evidence with the critic checkpoint and the fresh reviewer over it. A round must be able to see the channel and the distinction before it runs; it must not be handed the conclusion.

- **[NEED]** `[OWNER 2026-08-27, conflict surfaced at Align]` **R-A7** — The `p_pump` re-source is removed from Run-Study Item 6 Phase 4's owner-sequenced close list (`align.md:10-12`).
- **[INFERRED]** **R-A7a** — That removal is recorded where a Phase 4 operator will read it (`.project/CURRENT_WORK.md` names the item in the Phase 4 next-up entry today). The owner ruled the removal; where it gets written down is this spec's inference about not leaving a stale close list behind.

### B. The bounded model task and its `PREREQUISITE`

- **[INHERITED: epic § Item 5 scope 2]** **R-B1** — The round's first task is a bounded *modeling* objective on the `p_pump` value. Its `### T-00N scope` names no research task and carries no future task list.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Running one task]** **R-B2** — `PREREQUISITE` is discovered as a return, never predicted in a scope. A scope that lists its own prerequisites is a plan.
- **[INFERRED]** **R-B3** — This spec's expectation that the task will hit a source prerequisite is a proof obligation on the item, not an instruction to the task. If the bounded modeling objective can be met without one, that is recorded as what happened; the first success criterion then goes unmet and is owner-visible. A prerequisite is not manufactured to satisfy this document.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § Running one task]** **R-B4** — Every return carries its outcome, evidence refs, the goal-level reading of them, and the five decision fields for each goal-level decision: the finding or trigger; the decision and its reason; the tier; who decided; what changed.

### C. The one critic checkpoint

- **[NEED]** `[OWNER 2026-08-25, epic § Success Criteria]` **R-C1** — A fresh non-author critic reviews the reading and the proposed dispositions **before any semantic follow-up task executes**. The author revises until the checkpoint passes or its declared cap produces an owner-visible stop.
- **[INHERITED: epic § Item 5 scope 2, decomposition ratified by owner 2026-08-25]** **R-C2** — The checkpoint fires on **the reading**, and a reading of already-committed study evidence is a reading. Its basis is the epic's own Item 5 scope step 2: *"Write the reading and proposed research/model dispositions, then send them to a fresh non-author critic before either semantic follow-up executes"* (epic:389) — a sentence that names no freshly executed study, and one the owner ratified with the decomposition (epic Priority and Estimated Effort headers record that ratification, 2026-08-25).

  So the reading under review here is of the committed study record `20260821-power-cycle-ab@881d4448` § 15 finding `#3` and its supporting knowledge (DI-008), together with the model task's `PREREQUISITE` return. This round executes no study — study execution is Item 6's.

  *Surfacing note, not a resolution: `GOAL_RUNBOOK.md@1d43dc5b:140` phrases the trigger as "after a study reading produces proposed dispositions". If the owner ever reads that phrase narrowly — a study this round executed — then it is the runbook sentence that gets amended, not this item's checkpoint. Recorded as an orchestrator execution-detail decision, loudly, and surfaced to the owner in the run log.*

- **[NEED]** `[OWNER 2026-08-25]` **R-C3** — The checkpoint runs under a declared revision cap, restated explicitly in `goal.md`. At the cap the round writes `### Stop — YYYY-MM-DD` of kind `cap`, naming the unresolved dispositions and what the owner must decide. **The cap stops the work; it never releases it.** Execution is not permitted past an unpassed checkpoint.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b:232` § Limits]** **R-C3a** — The cap *number* is the runbook default, **2 revisions (3 submissions)**. The runbook says a goal may declare tighter or looser values and the declared value wins, so this number is the default this goal carries unless the owner overrides it at grounding. The existence of a cap and the cap-stops-work rule (R-C3) are owner-graded and are not overridable here.
- **[INHERITED: epic § Item 5 Out of Scope]** **R-C4** — Exactly one checkpoint, placed as above. Routine native stages get no separate goal critics; their own reviews are native.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § What "fresh" means]** **R-C5** — "Fresh" is a session boundary, not a work boundary: the critic is never the author's session. An agent that cannot obtain one writes the handoff stop and stops; it does not review its own dispositions and does not wave the gate through.
- **[INHERITED: `GOAL_RUNBOOK.md@1d43dc5b` § The pre-execution disposition checkpoint]** **R-C6** — Each submission is a new `### Checkpoint C-00N.rK` entry naming the reviewer, the reading, the dispositions, the verdict, and what the author changed. A previous entry is never amended; the sequence of submissions is the record of the disagreement.

### D. The native research seam

- **[INHERITED: epic § Item 5 scope 3; `docs/research_seam_operator_guide.md@9637f1b7`]** **R-D1** — The research is run through the Item 2 seam natively: `scripts/research_seam.py` for the request and the run record, `scripts/source_registry.py` for the one write into `knowledge/`, driven by `/research-acquire`. No hand-written `SOURCE_INDEX.md` entry, manifest row, or source directory appears anywhere in the path.
- **[INFERRED]** **R-D2** — The request's `consumer` field names the live need by native id — the discovery row `20260821-power-cycle-ab#3`, or the modeling work item once it exists — so the request, its run, and any bounded negative key to the thing that is waiting.
- **[INHERITED: `docs/research_seam_operator_guide.md@9637f1b7` § The four return classes]** **R-D3** — The seam's native return class (`REGISTERED` / `OPERATOR_QUEUE` / `BOUNDED_NEGATIVE` / `BLOCKER`) is preserved verbatim in the trail and routed as it stands. The goal layer reads it; it does not re-grade it.
- **[INHERITED: `docs/research_seam_operator_guide.md@9637f1b7` § Commit the run directory with the work]** **R-D4** — The request, the run record, the receipts, the return, and any bounded negative are committed as evidence alongside the round.
- **[INHERITED: Item 2 spec R-C3, `[OWNER 2026-08-25]`]** **R-D5** — Acquisition may register sources; it must not mint a DI. Minting a DI or amending DI-008 is a knowledge mutation beyond the goal directory and therefore a reserved gate (R-A4). For this round a registered source is a sufficient MR-4 basis on its own — the follow-up modeling task cites the registered source directly, so the positive path does not require a DI amendment to reach criterion 4.
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
- **[INFERRED]** **R-G4** — The prose around the table is amended with it, so the section does not contradict its own row. `GOAL_RUNBOOK.md:262` currently reads "**Two seams are not repaired yet**, and a goal round may not silently absorb either repair"; after the flip that sentence says one seam (`integrate`) remains pending, and the closing sentence at `:267` ("The repairs have their own owners and their own failure contracts") is made consistent with a single remaining repair. The `integrate` table row and its own bullet are Item 6's and are still not touched (R-G1).

### H. Evidence and the hardening bar

- **[NEED]** `[OWNER — epic § Epic Strategy, Hardening rule]` **R-H1** — No task envelope, event ledger, digest comparison, idempotency layer, reconciliation pass, or dispatcher enters this item unless a recorded run failure promotes it, and the failure is owner-visible when it does.
- **[INFERRED]** **R-H2** — `verification_record.md` maps each success criterion above to disk evidence — a path, a commit, a return file — and records every point where the prose route was ambiguous, misread, or failed, whether or not it promoted anything. Item 4's record (`.project/completed/20260827_goal-cold-pickup-proof/verification_record.md`) is the shape to match.
- **[INFERRED]** **R-H4 — the covering branch is declared before the run.** Before the round opens, the item commits a written list of which honest non-exercise outcomes count for which success criteria: the `OPERATOR_QUEUE` return and the owner-gate park, which leave criterion 4's positive path non-exercised while criterion 3 is still met by honest routing; a bounded negative (R-D6); a `STRATEGY_BLOCKER` close (R-E3); and the no-prerequisite case (R-B3). The declaration is committed **ahead of** the round so its ancestry is checkable — an auditor can confirm from `git log` that the branch list predates the outcome it covers. Rationale: this is Item 4's pattern, and the epic's own disposition of criterion 5 leans on "the covering branch was declared before the run" (epic:338). Without it, an `OPERATOR_QUEUE` return or a gate park gets re-read after the fact as a failed criterion.
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
- **How many rounds this item covers, and what the item is worth if the second half never runs.** The epic's sequence is one round (`model → research → model`), but a queue, a `STRATEGY_BLOCKER`, or an unresolved gate could close round 1 before the modeling resumes. **The item's floor:** even if the second half never executes, the item still proves the first half — a real `PREREQUISITE` discovered by a bounded task, a fresh critic binding before follow-up, and the native seam invoked with its return routed honestly (criteria 1, 2, 3, 5, 6). That is a shippable result. Whether the item then opens round 2 to reach criterion 4 or ships on the floor is design's call, bounded by the goal's round limit.
- **Whether the follow-up modeling work item lands inside this item or is handed to the owner at the gate.** R-E2 makes the go/no-go the owner's; how far the round carries the item once authorized — spec only, or through implement — is design's to **bound**, not merely scope. The epic's budget is 8h execute, and carrying a modeling work item through implement does not fit it. Design records the bound it chooses.
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
- **Review:** `.project/active/goal-research-model-proof/spec-review.md` — verdict Revise, 2026-08-27; this revision applies it
- **Align:** `.project/active/goal-research-model-proof/align.md` — owner rulings, settled
- **Product-lens:** `.project/active/goal-research-model-proof/product-lens.md` (to be created at close; not yet run)
- **Design:** `.project/active/goal-research-model-proof/design.md` (to be created)

**Requirement numbering note (revision 2026-08-27):** no requirement the review cited was renumbered. Two were split so each half carries its true grade — R-A7 (owner-ruled removal) / R-A7a (inferred recording obligation), and R-C3 (owner-graded cap existence and cap-stops-work) / R-C3a (inherited cap number). Added: R-A2a (staged-discovery discipline), R-G4 (runbook prose around the flipped row), R-H4 (pre-declared covering branch, promoted from Open Question 4).

---

**Next Steps:** After approval, proceed to `/_my_design`.
