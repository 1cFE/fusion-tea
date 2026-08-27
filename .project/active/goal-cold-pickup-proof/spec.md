# Spec: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-26
**Complexity:** MEDIUM
**Branch:** `feat/goal-integration-seam` (`[OWNER 2026-08-26]` — no child branch)

---

## Problem

Item 1 shipped the lean goal contract — `work/orchestration/GOAL_RUNBOOK.md`, the three templates at `work/orchestration/goal-templates/`, the `run-goal` skill, and ADRs 001–007. Every one of those files was written by the person who designed the layer, and no session that was not that person's has ever used them. `work/orchestration/goals/` does not exist. No goal has been grounded, no round opened, no round reviewed.

That leaves three bets carrying the epic's critical path, all of them untested:

- **A stranger can ground a goal, and an ungrounded one cannot start.** The runbook says a draft goal authorizes no task. Nothing has ever tried to start one.
- **A fresh session can resume an interruption from disk.** The write-ahead start line exists precisely so an interruption leaves a trace. No interruption has ever happened, so nothing has ever read one.
- **A fresh reviewer catches drift and settles the learning delta.** The review section describes eight checks. None has run against a real round.

There is a second reason the run has to happen, and it is the owner's:

- `[OWNER]` No task envelope, machine event ledger, digest comparison, idempotency layer, reconciliation operation, concurrent goal run, or unattended dispatcher enters the first build unless a recorded proof run demonstrates that the prose/native-facts route failed. Source: `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions, P2/M4; carried as the epic's Hardening rule.

That ruling makes the cold run the *only* admissible evidence in either direction. Without it there is nothing to promote a hardening mechanism on, and equally nothing that justifies leaving the prose route alone. The proof is what turns "we decided to stay lean" into "we stayed lean and here is what happened when it was used."

This item is a proof, not a build. Its output is a real goal in `work/orchestration/goals/`, kept evidence of what each cold session was given and what it produced, and an honest report — including any place the prose failed.

## Success Criteria

The six criteria below are the epic's, made concrete against the chosen question and the artifacts on disk.

- [ ] **Cold grounding.** A fresh non-builder session, given the operator question and the repository but no prewritten `goal.md`, produces a `goal.md` at `work/orchestration/goals/<slug>/` that reaches `Status: grounded` with every template heading filled: question, consumer, answered-when, invariants, grounding evidence cited as `<path>@<sha>` (or explicitly unpinned), the four limits restated with numbers, reserved gates, and close rule.
- [ ] **The grounding gate holds, and its real reach is measured.** A draft that is missing repository evidence, the answer contract, invariants, limits, or reserved gates is refused before any task scope is written, and the refusal names which fields are missing. The evidence shows the refusal came before the first `### T-001 scope` entry, not after. **The five field classes are not equally defended today** — see § A predicted prose failure — so the criterion is met either by the refusal happening or by the proof recording, per field class, that it did not and why.
- [ ] **The goal directory stands alone.** From `work/orchestration/goals/<slug>/` plus the repository — with no access to this spec, this item's directory, or any operator transcript — a reader identifies the active strategy, the one task, the open gate/limit state, and the native evidence the round rests on.
- [ ] **Interrupted resume.** A second fresh session, given only the goal directory and the repository, resolves a `### T-00N start` that has no matching return and no stop. It appends either the correct return or a `### Stop` of kind `interruption`, and it does not repeat the native effect the interrupted task already completed. The completed native artifact is byte-identical before and after the resume session, or its only change is one the resumer's own recorded reasoning accounts for. The resumer also walks the round's cited refs for external mutation (`GOAL_RUNBOOK.md` § When a cited artifact moves) and leaves the open gate and limit state intact — the owner's resume criterion is three-part: no re-running completed stages, no duplicated side effects, and no lost open gates (`.project/concepts/goal-driven-model-development-harness.md` SC 3).
- [ ] **Bounded closure.** The round closes with no promoted pin and no committed study, on one of the six close triggers — legitimate bounded-negative, unresolved owner gate, or declared limit. A `### Round N result` is written with intent, task sequence, last semantic outcome, a *derived* stop reason, evidence refs, proposed learning delta, and finding dispositions. No task ends silently and no stop is unrecorded.

- [ ] **The judgment replays from the trail alone.** Every goal-level decision the round made carries all five fields — the finding or trigger, the decision and its reason, the tier (`execution detail | reserved gate | premise surprise`), who decided, and what changed, resolving to a path, an id, a commit, or `none`. A reader replays the round's judgment from `trail.md` with no second ledger existing anywhere. This is the surface that carries the lean route's central claim (`[OWNER]`, concept SC 6), so a decision recorded with four fields is a recorded prose failure, not a formatting nit.
- [ ] **Discovery-row accounting.** Every discovery row the round's evidence touched carries a joined disposition row appended under its existing `<study-id>#<n>` id — at minimum `20260823-magnet-technology-ab#2`, which is `unrouted` today. No first-sighting row is edited, no id is minted, and no touched row returns as `unrouted`.
- [ ] **Fresh review catches the seed.** A third fresh session, running the review mode, catches the one seeded scope or comparison-meaning drift, accounts for every touched discovery row, and accepts or corrects the proposed learning delta before it lands in `learnings.md`. The evidence shows the seed was planted and its expected detection recorded *before* the review session ran, and that the reviewer was not told about it.
- [ ] **Failures are recorded, and nothing is promoted without them.** The proof report states every point where the prose route was ambiguous, was misread, or failed, with the session output that shows it. If the report proposes no hardening mechanism, it says so. If it proposes one, it cites the recorded failure that promotes it under the owner's rule.

## A predicted prose failure

One conflict is visible before the run starts, and parking it silently would make the proof dishonest.

The epic's criterion is that a goal cannot start without repository evidence, an answer contract, limits, invariants, and reserved gates — five field classes. The gate Item 1 shipped defends one of them: "A goal whose § Grounding evidence is empty stays `Status: draft`, and a draft goal authorizes no task" (`GOAL_RUNBOOK.md:72`). Nothing in the runbook refuses a goal for missing invariants, missing limits, or missing reserved gates, and nothing says where a refusal is *written* — a draft goal has no open round, so `trail.md` has no heading for it.

So the grounding gate is not one test. It is one test and four predictions. The proof runs the draft against the gate as shipped and records, per field class, whether the cold session refused and on what basis. A field class that sails through is a recorded prose failure under the owner's hardening rule — evidence for the owner to act on, not a defect this item repairs. Fixing the runbook belongs to whoever owns Item 1, after the evidence is in.

## Known Requirements

### The proof goal

- **[NEED]** `[OWNER 2026-08-26]` The operator question is the orchestrator's pick, delegated by the owner: should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`, instead of held? It grounds on discovery row `20260823-magnet-technology-ab#2` (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`). The grounding chain available to the cold session is the committed study record, DI-010 (`knowledge/KNOWLEDGE.md:76`), and WI-031's approved research (`work/completed/20260822_WI-031_research-round-item6-values/`).
- **[NEED]** `[OWNER 2026-08-26]` The orchestrator plays the operator in the co-development. Operator-side content in `goal.md` is marked `[AGENT]` — orchestrator-operationalized — and never as owner intent.
- **[NEED]** `[OWNER 2026-08-26]` The reserved gates for this goal are merge, push, item close, and archive per the runbook, plus: any model or knowledge mutation beyond the goal directory needs owner sign-off. (`[AGENT]` default, ratified by the owner.)
- **[NEED]** `[OWNER 2026-08-26]` The work stays on `feat/goal-integration-seam`. No child branch.
- **[HARD]** The goal directory is `work/orchestration/goals/<slug>/`, holding `goal.md`, `trail.md`, and `learnings.md` copied from `work/orchestration/goal-templates/`; the template headings are the contract (`GOAL_RUNBOOK.md` § The five surfaces). Whether anything else may sit alongside them is open — see Open Questions.
- **[HARD]** The goal layer cites and never restates native state. No work item status, study number, or spec requirement is copied into `trail.md` (`GOAL_RUNBOOK.md` § What this is).
- **[INFERRED]** The proof goal is a real goal, kept in the repository after the item closes — not a scratch fixture. It is the first entry under `work/orchestration/goals/`.

### Cold sessions and evidence

- **[HARD]** "Fresh" is a *session* boundary, not a work boundary: the critic is never the author's session (`GOAL_RUNBOOK.md` § What "fresh" means, quoting `[OWNER]` at `.project/concepts/goal-driven-model-development-harness.md:47`). Grounding, resume, and review are three sessions, none of which authored what it is handed.
- **[NEED]** The kept evidence shows, for each cold session, exactly what it was given and exactly what it returned, so a later reader can audit the freshness claim rather than take it on trust. A session whose inputs are not recorded does not count as proof.
- **[HARD]** No cold session is handed this spec, this item's directory, or the seeded-drift record. Its inputs are the goal directory, the repository, and the operator prompt.
- **[NEED]** `[OWNER 2026-08-26]` The orchestrator's notes on how the operator exchange actually works are a named artifact in this item's directory, not prose folded into the report — what the grounding dialogue asked, where it stalled, what the operator had to supply that the runbook did not prompt for.
- **[INFERRED]** The proof report is the epic's `verification_record.md` under one name, not two documents. It is concise and reads as a verdict; the transcripts are referenced evidence, not its content.
- **[INHERITED: `goal-driven-model-development-harness.md` SC 1]** Grounding evidence is checked for substance, not only citation form: which package, which entry keys and constraints can respond to the question, and what the discovery log and knowledge base already say. The chosen `vol_cold_cryo` question has exactly that chain available, so a `goal.md` that cites well-formed paths carrying none of it does not pass grounding.

### The interruption

- **[HARD]** The interruption is a genuine mid-task stop: after the write-ahead `### T-00N start` line, after the native side effect has landed, and before the `### T-00N return`. A clean-boundary handoff does not count as proof (epic § Out of Scope).
- **[HARD]** The native artifact the interrupted task leaves is observable on disk and outside the goal directory, so that the resumer reads native state as truth rather than reading the trail's expectation (`GOAL_RUNBOOK.md` § Resuming an interruption).
- **[INFERRED]** The native target is chosen so that leaving it half-finished trips no reserved gate — so not a model file, not a knowledge file, and not anything requiring merge, push, close, or archive. The discovery-log disposition row is inside the round's authority (`GOAL_RUNBOOK.md` § The discovery log: a round's one write outside its own directory) and is a legitimate candidate; so is minting a native work item through its owning PM.
- **[NEED]** "Without duplicating the completed native effect" is checked against the artifact, not asserted. The evidence carries the artifact's state before and after the resume session.

### Closure, drift, and review

- **[HARD]** The round closes with no promoted pin and no committed study. The close trigger is a legitimate bounded-negative, an unresolved owner gate, or a declared limit — an honest empty round is a result (`GOAL_RUNBOOK.md` § Opening and closing a round).
- **[HARD]** The stop reason is derived from the last semantic outcome plus the goal's limits, written as a derivation, not maintained as a second status enum.
- **[NEED]** Exactly one drift is seeded — a scope drift or a comparison-meaning drift — and it is a plausible one a real round could commit, not a flagrant marker. Its identity and the detection expected of the reviewer are recorded in this item's directory before the review session runs.
- **[HARD]** The study executor remains the sole writer of first-sighting rows; the goal round appends joined disposition rows under existing ids only, read newest-row-wins (`GOAL_RUNBOOK.md` § The discovery log, ADR-004).
- **[HARD]** A learning entry lands in `learnings.md` only after the round review has accepted or corrected the delta the round result proposed (`learnings.md` template, `GOAL_RUNBOOK.md` § The fresh review).

### The hardening bar

- **[NEED]** `[OWNER]` No hardening mechanism — envelope, event ledger, digest comparison, idempotency key, reconciliation operation, concurrent run, or unattended dispatcher — is promoted by this item unless the proof report records the run failure that demonstrates the prose route failing. Source: `goal-strategy-task-harness-design-review.md` § Resolutions P2/M4, via the epic's Hardening rule.
- **[INFERRED]** Recording a failure is not the same as fixing it. This item records; whether a recorded failure promotes a mechanism, amends the runbook, or is left alone is the owner's call at close.

## Non-Goals

- **Solving the chosen finding.** Whether `vol_cold_cryo` should be computed is the goal's question; answering it is not this item's deliverable. The round may legitimately close without it.
- **Using Item 2's research seam or Item 3's integration seam.** The documented manual patterns stay in force for this proof, so the lean contract is tested before the native repairs are available (epic § Parallel work).
- **Unattended dispatch.** No goal agent starts another session. Where a gate needs a fresh reviewer, the agent stops and hands back, as the runbook says.
- **Changing the runbook, the templates, or the ADRs.** This item reads them and reports on them. Any amendment is a separate decision after the evidence is in.
- **Route-equivalence comparison between hand-operated and agent-operated paths.** That is epic Item 6's.

## Open Questions / Deferred to design

- How a cold session is actually obtained and driven, and how its inputs and outputs are captured as evidence. The freshness requirement is stated above; the mechanism is design's.
- Which native target the interrupted task uses, and what the "observable artifact" is concretely.
- What the deliberately ungrounded draft contains, who authors it, and whether the refusal comes from the same grounding session on its first pass or from a separate session handed the bad draft.
- Which of the two drift kinds is seeded, and how it is planted so it reads as ordinary round work.
- The goal slug, and whether this goal's limits differ from the runbook defaults (a declared value wins; the numbers must appear in `goal.md` either way).
- Where the cold-session evidence physically lives — inside the item directory, or under the goal directory — given that the goal directory must stay readable as a real goal and not as a test fixture.
- How much of the round is a single task versus two, and whether the interruption and the closure ride the same task.

The last three are load-bearing on whether the proof is valid, not just tidy. Design settles them before anything runs.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 4
- **Align record:** `.project/active/goal-cold-pickup-proof/align.md`
- **Required Reading:**
  - `.project/active/goal-harness-contract/` — Item 1's spec, design, plan
  - `work/orchestration/GOAL_RUNBOOK.md`, `work/orchestration/goal-templates/`, `.claude/skills/run-goal/SKILL.md`
  - `.project/adr/001-strategy-and-task.md` through `007-supersession.md`
  - `.project/concepts/goal-driven-model-development-harness.md` § Owner's Words, Success Criteria 1, 3, 6–8
  - `.project/concepts/goal-strategy-task-harness-design.md` § Goal and strategy, Task-grain invocation, Review Pattern, Validation and Handoff
  - `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions C1, P2
  - `work/orchestration/handshake-lcoe-construction.md` — cold prose referent
  - `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`
- **Product lens:** `.project/active/goal-cold-pickup-proof/product-lens.md`
- **Design:** `.project/active/goal-cold-pickup-proof/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
