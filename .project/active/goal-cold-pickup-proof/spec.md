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

- `[OWNER]` None of the five hardening mechanisms — envelope YAML, event ledger, digests, idempotency keys, reconciliation — enters the first build unless a recorded proof run demonstrates that the prose/native-facts route failed. Source: `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions, P2/M4; carried as the epic's Hardening rule.

Concurrent goal runs and unattended dispatch are **not** on that list and are not proof-gated. ADR-003 treats them as premises of the ruling — facts about the system today that make the threat model small enough for git plus a fresh reviewer to cover (`003-lean-first-persistence.md:34`). They are barred outright, and no evidence this item produces can promote them.

That ruling makes the cold run the *only* admissible evidence in either direction. Without it there is nothing to promote a hardening mechanism on, and equally nothing that justifies leaving the prose route alone. The proof is what turns "we decided to stay lean" into "we stayed lean and here is what happened when it was used."

This item is a proof, not a build. Its output is a real goal in `work/orchestration/goals/`, kept evidence of what each cold session was given and what it produced, and an honest report — including any place the prose failed.

## Success Criteria

Nine criteria below against the epic's six. Six map one-to-one; three are refinements that split a compound epic criterion so an auditor can check it: "The judgment replays from the trail alone" and "Discovery-row accounting" are pulled out of the epic's closure criterion, and "Failures are recorded" carries the epic's hardening criterion on its own.

**How orderings are checked.** Three criteria assert that one thing happened before another, and an auditor who did not run the proof has files, not a clock. Mtimes prove nothing after a checkout and content order proves nothing across two files, so the ordering predicate is **git commit ancestry on `feat/goal-integration-seam`**: the seed record, the write-ahead trail state, and each cold session's input brief are committed *before* the session that depends on them runs. Where a criterion below says "before," it means an auditor can show the earlier commit is an ancestor of the later one.

- [x] **Cold grounding.** A fresh non-builder session, given the operator question and the repository but no prewritten `goal.md`, produces a `goal.md` at `work/orchestration/goals/<slug>/` that reaches `Status: grounded` with every template heading filled: question, consumer, answered-when, invariants, grounding evidence cited as `<path>@<sha>` (or explicitly unpinned), the four limits restated with numbers, reserved gates, and close rule.
- [x] **The grounding gate's reach is measured, per field class.** The gate Item 1 shipped defends one of the epic's five field classes (§ A predicted prose failure), so this criterion does not assert that the gate holds — it requires the proof to establish, for each of the five, whether the shipped contract refused task start and on what basis. The one thing an auditor checks: a per-field-class record, backed by the enforcer session's own output.

  The enforcer is **a separate fresh session** following the runbook, handed the deliberately ungrounded draft and asked to proceed to a task `[AGENT]`. The contract holds for a field class only if that session refuses task start and names the missing class *unprompted*. The orchestrator-as-operator never plays the refusing role — it built the brief and knows which five classes are supposed to be checked, so its refusal would be the harness grading its own homework. A refusal the grounding session raises against its own draft is recorded but does not satisfy the criterion, for the reason the runbook gives about reviewing your own work (`GOAL_RUNBOOK.md:43`).

  The refusal is committed before any `### T-001 scope` entry is, so the ordering is auditable by ancestry.
- [x] **The goal directory stands alone.** From `work/orchestration/goals/<slug>/` plus the repository — with no access to this spec, this item's directory, or any operator transcript — a reader identifies the active strategy, the one task, the open gate/limit state, and the native evidence the round rests on.
- [x] **Interrupted resume, with a landed effect to not repeat.** Three things are present on disk, in a commit that is an ancestor of the resumer's first commit, *before* the second fresh session starts: the write-ahead `### T-00N start` entry, the completed observable native artifact that task produced, and no `### T-00N return` and no stop. **An interruption that landed no native effect fails this criterion** — that is the clean-boundary case the epic excludes (`epic:329`), and it would otherwise pass vacuously.

  The resume session, given only the goal directory and the repository, appends either the correct return or a `### Stop` of kind `interruption`. It does not re-produce the native effect: the completed native artifact's hash is unchanged across the session, and the evidence shows no second invocation of whatever produced it. "Byte-identical" scopes to that artifact alone — the discovery log legitimately gains joined disposition rows during a correct resume (Criterion 7), so the file as a whole is not the unit. The resumer also walks the round's cited refs for external mutation (`GOAL_RUNBOOK.md` § When a cited artifact moves) and leaves the open gate and limit state intact — the owner's resume criterion is three-part: no re-running completed stages, no duplicated side effects, and no lost open gates (`.project/concepts/goal-driven-model-development-harness.md` SC 3).
- [x] **Bounded closure.** The round closes with no promoted pin and no committed study, on **an unresolved owner gate or a declared limit** — the two of the runbook's six close triggers that are reachable for this proof (see § A close trigger the epic names does not exist). The round's last semantic outcome may be a task-level `BOUNDED_NEGATIVE`; that outcome does not itself close the round. A `### Round N result` is written with intent, task sequence, last semantic outcome, a *derived* stop reason, evidence refs, proposed learning delta, and finding dispositions. No task ends silently and no stop is unrecorded.

- [x] **The judgment replays from the trail alone.** Every goal-level decision the round made carries all five fields — the finding or trigger, the decision and its reason, the tier (`execution detail | reserved gate | premise surprise`), who decided, and what changed, resolving to a path, an id, a commit, or `none`. A reader replays the round's judgment from `trail.md` with no second ledger existing anywhere. This is the surface that carries the lean route's central claim (`[OWNER]`, concept SC 6), so a decision recorded with four fields is a recorded prose failure, not a formatting nit.
- [x] **Discovery-row accounting.** Every discovery row the round's evidence touched carries a joined disposition row appended under its existing `<study-id>#<n>` id — at minimum `20260823-magnet-technology-ab#2`, which is `unrouted` today. No first-sighting row is edited, no id is minted, and no touched row returns as `unrouted`.
- [ ] **Fresh review catches the seed.** A third fresh session, running the review mode, catches the one seeded scope or comparison-meaning drift, accounts for every touched discovery row, and accepts or corrects the proposed learning delta before it lands in `learnings.md`. The seed record — the drift's identity and the detection expected of the reviewer — is committed before the review session runs, so ancestry carries the ordering. That the reviewer was not told is established by its input record being complete and closed (§ Cold sessions and evidence), since absence of information is not observable from an artifact.

  After the review completes, a dated `### Amendment` is appended to the kept `trail.md` disclosing that one drift was seeded for this proof and citing the verification record `[AGENT]`. Disclosure is post-review only, so it cannot spoil the test, and the goal directory does not survive into the repository silently carrying a planted drift.

  **Left unchecked deliberately at audit, 2026-08-26.** Not exercised as designed: the seed did not propagate — the round agent narrowed the widened frame back to `goal.md`'s question at the writer, so no drift existed for the reviewer to catch. The branch covering this outcome was declared before the run (`design.md:269`, `plan.md:400`, in commits that are ancestors of `a6caab37`). The review demonstrated the same faculty on a real organic drift and settled the learning delta, and the post-review disclosure amendment is present (`trail.md:251`). Checking this box would soften a recorded non-exercise into a pass. See `audit.md` § Spec conformance, criterion 8.
- [x] **Failures are recorded, and nothing is promoted without them.** The proof report states every point where the prose route was ambiguous, was misread, or failed, with the session output that shows it. If the report proposes no hardening mechanism, it says so. If it proposes one, it cites the recorded failure that promotes it under the owner's rule.

## A close trigger the epic names does not exist

The epic writes the closure criterion as "a legitimate bounded-negative, owner gate, or declared limit" (`epic:321`). Item 1's shipped contract does not offer the first of those. The runbook's six close triggers are a valid study reading, a strategy blocker, changed comparison meaning, an unresolved owner gate, a declared limit, and the goal answered (`GOAL_RUNBOOK.md:84-91`). `BOUNDED_NEGATIVE` is a *task return outcome*, and its stated effect is the opposite of closing: "A first-class result; choose the next task" (`GOAL_RUNBOOK.md:120`).

The epic's wording predates Item 1's shipped contract. **The runbook is authoritative** `[AGENT]`, and the epic's intent maps onto it cleanly: the round's last semantic outcome may well be a task-level `BOUNDED_NEGATIVE`, and the round then closes on one of the six. Since this proof also closes with no committed study, trigger 1 is out too, leaving an unresolved owner gate or a declared limit as the reachable routes. Every criterion in this spec uses the runbook's trigger vocabulary. This resolution is flagged to the owner in the orchestrator's run summary rather than settled here.

## A predicted prose failure

One conflict is visible before the run starts, and parking it silently would make the proof dishonest.

The epic's criterion is that a goal cannot start without repository evidence, an answer contract, limits, invariants, and reserved gates — five field classes. The gate Item 1 shipped defends one of them: "A goal whose § Grounding evidence is empty stays `Status: draft`, and a draft goal authorizes no task" (`GOAL_RUNBOOK.md:72`). Nothing in the runbook refuses a goal for missing invariants, missing limits, or missing reserved gates, and nothing says where a refusal is *written* — a draft goal has no open round, so `trail.md` has no heading for it.

So the grounding gate is not one test. It is one test and four predictions. The proof runs the draft against the gate as shipped and records, per field class, whether the enforcer session refused and on what basis. A field class that sails through is a recorded prose failure under the owner's hardening rule — evidence for the owner to act on, not a defect this item repairs. Fixing the runbook belongs to whoever owns Item 1, after the evidence is in.

**This does not halt on Item 1's close** `[AGENT]`. Item 1 is gate-CLEAR but not owner-closed (`align.md:49`), so it could close before this proof runs, with a gate defending one field class out of five. The shortfall is not raised now as an Item 1 blocker; it reaches the owner in the orchestrator's run summary, carrying this item's measured evidence, which is worth more than the prediction alone. A later reader should read that as a choice, not an oversight.

## Known Requirements

### The proof goal

- **[AGENT] (ratified by owner 2026-08-26)** The operator question is the orchestrator's pick; only the *delegation* was the owner's ("you pick", `align.md:29-35`). Not settled — challenge it by re-deriving against the reasoning `align.md:33-35` records, not by asking the owner. The question: should `vol_cold_cryo` be computed from the ampere-turns the model already carries plus DI-010's `J_eng`, instead of held? It grounds on discovery row `20260823-magnet-technology-ab#2` (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md`). The grounding chain available to the cold session is the committed study record, DI-010 (`knowledge/KNOWLEDGE.md:76`), and WI-031's approved research (`work/completed/20260822_WI-031_research-round-item6-values/`).
- **[NEED]** `[OWNER 2026-08-26]` The orchestrator plays the operator in the co-development. Operator-side content in `goal.md` is marked `[AGENT]` — orchestrator-operationalized — and never as owner intent.
- **[AGENT] (ratified by owner 2026-08-26)** The reserved gates for this goal are merge, push, item close, and archive per the runbook, plus: any model or knowledge mutation beyond the goal directory needs owner sign-off. An agent default the owner approved, so not settled.
- **[NEED]** `[OWNER 2026-08-26]` The work stays on `feat/goal-integration-seam`. No child branch.
- **[HARD]** The goal directory is `work/orchestration/goals/<slug>/`, holding `goal.md`, `trail.md`, and `learnings.md` copied from `work/orchestration/goal-templates/`; the template headings are the contract (`GOAL_RUNBOOK.md` § The five surfaces). Whether anything else may sit alongside them is open — see Open Questions.
- **[HARD]** The goal layer cites and never restates native state. No work item status, study number, or spec requirement is copied into `trail.md` (`GOAL_RUNBOOK.md` § What this is).
- **[INFERRED]** The proof goal is a real goal, kept in the repository after the item closes — not a scratch fixture. It is the first entry under `work/orchestration/goals/`.

### Cold sessions and evidence

- **[HARD]** "Fresh" is a *session* boundary, not a work boundary: the critic is never the author's session (`GOAL_RUNBOOK.md` § What "fresh" means, quoting `[OWNER]` at `.project/concepts/goal-driven-model-development-harness.md:47`). Grounding, resume, and review are three sessions, none of which authored what it is handed.
- **[NEED]** The freshness record is **complete and closed**, not merely accurate about what it lists: every cold session is enumerated, each with its full kept input and its full return, and the record states plainly that no other input existed — no context injection, no prior turn, no verbal hint from the operator. A record that is exact about everything it contains while silent about what it omits does not establish freshness, and freshness is what Criteria 2, 4, and 8 rest on. A session whose inputs are not recorded this way does not count as proof.
- **[HARD]** No cold session is handed this spec, this item's directory, or the seeded-drift record. Its inputs are the goal directory, the repository, and the operator prompt.
- **[NEED]** `[OWNER 2026-08-26]` The orchestrator's notes on how the operator exchange actually works are a named artifact in this item's directory, not prose folded into the report — what the grounding dialogue asked, where it stalled, what the operator had to supply that the runbook did not prompt for.
- **[INFERRED]** The proof report is the epic's `verification_record.md` under one name, not two documents. It is concise and reads as a verdict; the transcripts are referenced evidence, not its content.
- **[INHERITED: `goal-driven-model-development-harness.md` SC 1]** Grounding evidence is checked for substance, not only citation form: which package, which entry keys and constraints can respond to the question, and what the discovery log and knowledge base already say. The chosen `vol_cold_cryo` question has exactly that chain available, so a `goal.md` that cites well-formed paths carrying none of it does not pass grounding.

### The interruption

- **[HARD]** The interruption is a genuine mid-task stop: after the write-ahead `### T-00N start` line, after the native side effect has landed, and before the `### T-00N return`. A clean-boundary handoff does not count as proof (epic § Out of Scope). Criterion 4 audits this positively — a start line with nothing landed behind it fails.
- **[HARD]** The native artifact the interrupted task leaves is observable on disk and outside the goal directory, so that the resumer reads native state as truth rather than reading the trail's expectation (`GOAL_RUNBOOK.md` § Resuming an interruption).
- **[INFERRED]** The native target is chosen so that leaving it half-finished trips no reserved gate — so not a model file, not a knowledge file, and not anything requiring merge, push, close, or archive. The discovery-log disposition row is inside the round's authority (`GOAL_RUNBOOK.md` § The discovery log: a round's one write outside its own directory) and is a legitimate candidate; so is minting a native work item through its owning PM.
- **[NEED]** "Without duplicating the completed native effect" is checked against the artifact, not asserted. The evidence carries the artifact's hash before and after the resume session, and the unit is the artifact the interrupted task produced — a single appended row, if that is the target — never a whole file the round has other legitimate reasons to append to.

### Closure, drift, and review

- **[HARD]** The round closes with no promoted pin and no committed study, on an unresolved owner gate or a declared limit — an honest empty round is a result (`GOAL_RUNBOOK.md` § Opening and closing a round, six triggers at `:84-91`). A task-level `BOUNDED_NEGATIVE` return does not close a round; see § A close trigger the epic names does not exist.
- **[HARD]** The stop reason is derived from the last semantic outcome plus the goal's limits, written as a derivation, not maintained as a second status enum.
- **[NEED]** Exactly one drift is seeded — a scope drift or a comparison-meaning drift — and it is a plausible one a real round could commit, not a flagrant marker. Its identity and the detection expected of the reviewer are recorded in this item's directory and committed before the review session runs, so ancestry proves the order. After the review completes, a dated `### Amendment` in the kept `trail.md` discloses the seeding and cites the verification record — post-review only, so the test is not spoiled and the goal directory does not enter the repository as the first canonical goal while silently carrying a planted drift `[AGENT]`.
- **[HARD]** The study executor remains the sole writer of first-sighting rows; the goal round appends joined disposition rows under existing ids only, read newest-row-wins (`GOAL_RUNBOOK.md` § The discovery log, ADR-004).
- **[HARD]** A learning entry lands in `learnings.md` only after the round review has accepted or corrected the delta the round result proposed (`learnings.md` template, `GOAL_RUNBOOK.md` § The fresh review).

### The hardening bar

- **[NEED]** `[OWNER]` None of the five hardening mechanisms — envelope YAML, event ledger, digests, idempotency keys, reconciliation — is promoted by this item unless the proof report records the run failure that demonstrates the prose route failing. Source: `goal-strategy-task-harness-design-review.md:209` (owner's words), via the epic's Hardening rule.
- **[INHERITED: `.project/adr/003-lean-first-persistence.md:34`]** Concurrent goal runs and unattended dispatch are barred outright, not proof-gated. ADR-003 treats them as premises that keep the threat model small, so no evidence this item produces can promote them, and this spec's § Non-Goals bars dispatch independently.
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
- What the deliberately ungrounded draft contains and who authors it. *Who refuses it* is settled in Criterion 2 — a separate fresh session — and is not design's to revisit.
- Which of the two drift kinds is seeded, and how it is planted so it reads as ordinary round work.
- The session-to-role map: which session opens the round with the strategy revision, writes the `T-001` scope and start line, and writes the `### Round N result` after the resumer appends the return. ADR-002's one-agent-per-round rule and § What "fresh" means rule out some assignments, so not every mapping of the three cold sessions onto the round's roles is legal.
- The goal slug, and whether this goal's limits differ from the runbook defaults (a declared value wins; the numbers must appear in `goal.md` either way).
- Where the cold-session evidence physically lives — inside the item directory, or under the goal directory — given that the goal directory must stay readable as a real goal and not as a test fixture.
- How much of the round is a single task versus two, and whether the interruption and the closure ride the same task.

The last four — evidence location, task shape, the session-to-role map, and how a cold session is obtained and captured — are load-bearing on whether the proof is valid, not just tidy. Design settles them before anything runs.

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
- **Spec review:** `.project/active/goal-cold-pickup-proof/spec-review.md` — verdict Revise, 2026-08-26; all five must-fix and five should-fix incorporated in this revision
- **Design:** `.project/active/goal-cold-pickup-proof/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
