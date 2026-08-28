# Design Review: GSTH Item 5 — Research-to-Model Round Proof

**Design:** `.project/active/goal-research-model-proof/design.md` (Draft 2026-08-27)
**Spec:** `.project/active/goal-research-model-proof/spec.md` (revised 2026-08-27)
**Review File:** `.project/active/goal-research-model-proof/design-review.md`
**Date:** 2026-08-27
**Reviewer:** fresh non-author session, non-interactive stage subagent

---

## The Point

The goal layer was built to decide two things: what to work on next, and what the evidence means. Its hardest moment is the one it has never been through — a modeling attempt runs out of evidence mid-task, has to go get some, and then has to decide whether what came back still lets the old comparisons stand.

Three pieces exist and none of them have been joined. Item 4 proved a round can be grounded, killed, resumed, and reviewed — but only on manual seams, and it never had to acquire anything. Item 2 built the research seam and proved it against fixtures, offline. Item 1 wrote the pre-execution critic checkpoint into the runbook, and no live round has ever passed through it. A gate that has never bound is not evidence of anything.

So the obligation is not to build. It is to run the sequence once, on a need the repository is genuinely waiting on — the stellarator's `p_pump` = 1.0 MW, roughly 100× below admissible helium-primary circulator figures, understating `rec_frac` in every arm of both committed A/B studies (`DISCOVERY_LOG.md` row `20260821-power-cycle-ab#3`; DI-008) — and come out with a record an auditor can check against disk rather than against anybody's account.

Two things make this worth more than a demo, and both are the owner's. First, criticism sits *before* work compounds on a misread (`[OWNER-VERBATIM]`, `.project/concepts/goal-driven-model-development-harness.md:33`). Second, honest outcomes are first-class: a queued source, a bounded negative, a strategy blocker, or a park at a reserved gate are all valid results, and the item is deliberately not built so that only the positive path can succeed.

The whole proof turns on one claim being checkable from `git log` alone: **the prerequisite emerged from the work rather than from the prompt.** Everything else is machinery in service of that.

---

## Fundamental Assessment

**Sound, with must-fix gaps.** This is the right piece of work and the approach is right.

The design's central move — *nothing is built; the goal layer's own five surfaces carry the run, and the item directory holds only briefs, transcripts, and records about the run* — is the correct reading of a proof item under ADR-003's hardening bar. The complexity that is here is almost all ordering discipline (commit ancestry predicates, a pre-declared covering branch, a brief fence), and ordering discipline is exactly what a proof-of-emergence needs. I looked for a simpler design that still makes "the prerequisite was not staged" checkable by an auditor who does not trust the operator, and I could not find one. The abstractions are all prose files with a single job each; none earns a "why does this exist?"

I am not recommending Rework. The findings below are gaps and contradictions inside a sound frame, not a wrong frame.

**Product lens.** I did not spawn the lens subagent (this session is non-interactive and the orchestrator brief scopes the review to eight priorities; `product-lens.md` is marked in the spec as "to be created at close; not yet run"). I ran the lens reasoning inline against the durable product statements — `GOAL_RUNBOOK.md`, ADR-001 through ADR-008, `docs/research_seam_operator_guide.md`, the epic, and the owner-verbatim in the concept. Deriving the point independently, I land on the same point the design states, which is itself worth recording: the design has not drifted from the problem. No owner/`[HARD]` contradiction found. **This is not a substitute for the lens run — if the pipeline expects a `product-lens.md` ledger entry for this item, it still owes one.**

**Both design-level smells fire, and both must be visible in the judgment rather than buried in a rubric row.**

- **A consumer compensating for a platform guarantee.** D5 hands the round agent an operator ruling because the shipped runbook actively points it at the wrong route. The round (consumer) is compensating for the runbook (platform) being stale. *Disposition: acceptable, because the design does not hide it* — it names it as a measured prose failure destined for `verification_record.md` § Failures, and the runbook flip at C-FLIP repairs the platform permanently within this same item. This is the smell firing in its benign form: a disclosed, time-boxed compensation with the platform fix in the same diff. It does become a real problem via M1 below (the compensation arrives after the critic already passed on the wrong route), which is a sequencing bug, not a framing one.
- **Ownership of an invariant moving without saying so.** D8 lifts the seam-class → task-outcome reading out of the round agent's hands and fixes it in `goal.md` before the round opens. That is a defensible call — the design's stated reason ("four classes × six outcomes is exactly where an honest queue gets quietly re-graded into a blocker") is a good one — but the design presents it as a recording decision rather than as a transfer of judgment from the round to the item. See M3; it needs to be stated as what it is, and it needs a different home than § Invariants.

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

Coverage is high. Walking the spec's requirement blocks: R-A1 (§ The goal), R-A2 (gate (a) row), R-A2a (§ The grounding guard — this is the strongest section in the document), R-A3, R-A4, R-A5, R-A6, R-B1/B2/B3 (task table + B1's "if false"), R-C1/C3/C3a/C4/C5/C6 (§ The round + § Sessions), R-D1/D2/D3/D4/D5/D6 (D5, D7, D8, § The seam invocation), R-E1/E2/E3/E4, R-F1/F2/F3/F4/F5, R-G1–G4 (the four-spot edit list, which I verified line by line against `GOAL_RUNBOOK.md:256,262,264,267` — all four line references are correct), R-H1/H2/H3/H4 (D6, C-COVER, Invariant 10). All four Open Questions are answered and the design says which answers are the owner's rather than closing them.

Four compliance defects:

- **C1 — R-A7 is weakened from a removal to a note.** The spec grades R-A7 `[NEED]` `[OWNER 2026-08-27]`: the `p_pump` re-source *is removed* from Run-Study Item 6 Phase 4's close list. The design (§ Findings, closure, and the flip, R-A7a paragraph) implements only R-A7a — *one sentence appended* to the Phase 4 next-up entry. `.project/CURRENT_WORK.md:22` still reads "Next: Phase 4 (close) — owner sequences merge to `main`, the oracle-retirement BACKLOG row, the runbook sentences …, **the `p_pump` re-source item**, WI-030's DI note". Appending a sentence to a very long dense line while leaving the list member standing is precisely capture-fidelity Rule 3's accretion failure: a correction must delete or amend the corrected content, not add compensating prose beside it. The owner-graded removal must actually strike the list member; the R-A7a sentence then records where it went.
- **C2 — R-C2's surfacing obligation is dropped.** The spec's R-C2 carries an explicit surfacing note: `GOAL_RUNBOOK.md:140` phrases the checkpoint trigger as "after a study reading produces proposed dispositions", this round executes no study, and the spec directs that the reading be "recorded as an orchestrator execution-detail decision, **loudly**, and surfaced to the owner in the run log." The design never mentions runbook `:140` or this conflict anywhere. It handles the *other* runbook staleness (the seam row, § The stale runbook row) thoroughly and by contrast. Under capture-fidelity Rule 4, a premise conflict the spec explicitly parked for loud surfacing cannot silently vanish at the next hop. The design needs to name where this lands — `verification_record.md` § Failures and the run summary are the natural homes, alongside the seam-row failure.
- **C3 — the limits list in § The goal is wrong.** It says the goal restates "all four limits … (retry 2, checkpoint 2 revisions / 3 submissions, rounds 6, **no time limit**)". The runbook's fourth limit (`GOAL_RUNBOOK.md:230`) is **tasks per round: none**, not a time limit; the runbook has no time limit row at all. R-A5 requires every limit restated explicitly and nothing inherited silently, so a `goal.md` written from this sentence would carry a fabricated fourth limit and omit a real one. The design knows the right value — B5 cites `:230` correctly — so this is a slip in one sentence, but it is the sentence the plan will copy.
- **C4 — R-B4's five decision fields are never mentioned.** The design's "cited, never restated" posture is right in general, but R-B4 is a spec requirement with no landing site in the design at all, and the returns it governs (T-001's especially) are the item's primary evidence. One clause in the task table or § The round would close it.

Provenance carried faithfully otherwise. `[OWNER-VERBATIM]` from the concept survives with its quote in § The Point; the owner's `[OWNER 2026-08-27]` need is graded; `[INHERITED: epic …]` is carried on the Current State framing. No `[INFERRED]` spec item is silently hardened into a fixed constraint — the design correctly keeps the goal's § Question wording open as the owner's at gate (a), and correctly declines to pre-judge the R-E1-vs-R-E3 comparison-meaning question.

### 2. Pattern Consistency
**Assessment:** Pass

This is Item 4's pattern applied faithfully and with the right adaptations: cold sessions as direct `claude -p --output-format stream-json --verbose` teed outside the tree (never `orchestrate-stage.sh`), one committed brief per run, transcript and output committed after, a freshness record enumerating kept and discarded runs and closing with a completeness statement, `verification_record.md` per-criterion against disk, `operator-notes.md` written after the runs from kept transcripts with every operator call graded `[AGENT]` and never as a contract repair. The commit-sequence table with `git merge-base --is-ancestor` predicates is Item 4's shape.

The two known harness failure modes are carried into Implementation Notes correctly (date-anchored predicates for error 08a; fence sweeps against tool-call inputs rather than raw text). Naming files `covering-branches.md` / `freshness-record.md` / `meta.md` follows the precedent. Nothing invents a new pattern where one exists.

### 3. Abstraction Quality
**Assessment:** Concerns

Every artifact earns its place. I tested each by deletion: without `covering-branches.md` an `OPERATOR_QUEUE` return gets re-read after the fact as a failed criterion (this is R-H4's own rationale and it holds); without the pre-declared D8 mapping the round agent improvises four-to-six routing in the moment; without the grounding guard's may/may-not lists the whole proof is unfalsifiable. None of these is a wrapper around something that did not need wrapping.

The one abstraction I would push back on is **D8's placement, not its existence** — see M3.

The genuine gap here is not over-abstraction but under-specification: **the brief allowlist is never written down.** Item 4's design states it explicitly (`design.md:72`: an allowlist of what each session *may* read, then the named denials). The Item 5 design specifies the may/may-not lists for the *grounding* brief only, and then twice refers in passing to "every brief embeds its own denial list" (Research Findings; Implementation Notes) as though the lists were already defined. For sessions 03 through 08 — the round agent, the critic, the reviewer — no allowlist or denial list appears anywhere. Invariant 2 is the check; the design never states the mechanism the check is checking. See M2.

### 4. Duplication Avoidance
**Assessment:** Pass

The design is disciplined about the thing this layer is most prone to: it cites `GOAL_RUNBOOK.md` and the seam guide rather than restating them ("Nothing here restates that procedure" in § The seam invocation is exactly right), it keeps modeling-PM and goal state uncrossed per ADR-006, and § Owner pause points explicitly states "Nothing about a gate is mirrored into the item directory." No parallel structure is created that will drift.

### 5. Data Structure Clarity
**Assessment:** Pass

The request JSON is given concretely with every seam-required field, and I checked it against `docs/research_seam_operator_guide.md:95-105` — `question`, `consumer`, `gap_type`, `priority`, `where_to_look`, `limits` are all present and `open` will not refuse it. The `consumer` value `20260821-power-cycle-ab#3` matches the guide's documented `<study-id>#<n>` form (`:106`) and D7's reasoning for it (the row exists at request time; the work item does not) is correct and correctly sequenced. The request-key note (hash over `question`/`consumer`/`gap_type`/sorted `where_to_look`, with `priority` and `limits` deliberately outside it) is accurately read from `:108`.

### 6. Route Safety
**Assessment:** Concerns

Reading "routes" as this item's actual control flow — the seam class → task outcome mapping, and the fences that gate each transition.

**D8's mapping, checked against the runbook's real return vocabulary** (`GOAL_RUNBOOK.md:119-127`, the six outcomes `COMPLETE` / `BOUNDED_NEGATIVE` / `PREREQUISITE` / `STRATEGY_BLOCKER` / `OWNER_GATE` / `MECHANICAL_FAILURE`):

- `REGISTERED` → `COMPLETE`. Legal and obvious.
- `BOUNDED_NEGATIVE` → `BOUNDED_NEGATIVE`. Legal; the runbook grades it "a real, useful 'no' … a first-class result", which matches the guide's "this is an answer, not a failure" (`:161`).
- `OPERATOR_QUEUE` → `PREREQUISITE`. **Legal, and not a re-grade.** `PREREQUISITE` means "something needed is missing … preserves strategy and comparison meaning; another scoped task may follow", which is exactly a named candidate a person still has to fetch. One wrinkle worth noting rather than fixing: the design then parks the queued candidate at owner gate (b), and `OWNER_GATE` ("a reserved decision is needed") is arguably the closer fit for the *task's* outcome. `PREREQUISITE`-then-park is defensible and I would not force a change, but the trail should make the two-step visible so the fresh reviewer does not read it as a missing gate.
- `BLOCKER` → `MECHANICAL_FAILURE`. **The mapping is right; the retry authorization attached to it is not.** See M4.

**The fences.** Invariant 3 fences briefs committed before T-001's return, which is the correct fence line for *staged discovery* — the discovery is staged only if the answer reaches the round before the round returns it. The T-002 brief naming the seam scripts lands after that line and therefore stages nothing about the discovery. On priority 3's specific question: yes, "before T-001's return" is the right fence for the T-002 brief. What the fence does *not* protect is the checkpoint (M1).

**One fence hole.** Invariant 2 denies the item directory, `.orchestrate-logs/`, and `~/goal-proof-logs-item5/`. It does not deny `.project/backlog/epic_goal_strategy_task_harness.md`, whose § Item 5 states the intended `model → research → model` sequence and the native-research-seam criterion (`epic:51`). A cold round agent browsing `.project/backlog/` reads the shape of the errand. I confirmed the epic does not name `p_pump`, Moscato, or WPBOP, so this is a lesser leak than the item directory would be — but it is a leak the invariant does not cover and the design does not acknowledge. Advisory A2.

### 7. Bets & Decisions Integrity
**Assessment:** Concerns

The five stated bets are genuine claims about reality, not mechanism choices in disguise, and each carries a real "if false → what fails" that is not a mitigation in costume. B1's "if false" is especially honest — *no mitigation, by design; R-B3 forbids manufacturing one, the item ships a smaller proof and criterion 1 goes unmet, owner-visible*. That is the sentence that tells me this design is not built to succeed at all costs. B2 is the load-bearing one for the whole proof and it is correctly identified as such. The eight decisions each name a rejected alternative with a reason, and the reasons are real (D1's rejection of any slug containing "source" or "research" because every session reads the directory name first is a genuinely sharp catch).

**The hidden bet.** The design rests on an unstated belief: *if a source registers, the positive path (R-E1 advance) is available.* D3 builds the entire `spec-model` ceiling on it, § The seam invocation's "likely path" narrates `REGISTERED` → gate (b) → mint and spec, and the budget assumes it. But the design's own R-A6 evidence points the other way. DI-008's band is ~60–190 MW for Stellaris against the held 1.0 MW. The arms already sit at `rec_frac` 0.94 / 0.79 / 0.68 at the same grid corner (`record.md@881d4448:208`), and `recirc_ok` already fails at R ≤ 8.0 / 6.5 / 5.5 m by arm. An equal addition of tens of megawatts to every arm's recirculating sum, against arms already that close to and past the fence, very plausibly moves the premise rather than the numbers — which is R-E3 `STRATEGY_BLOCKER` territory, not R-E1.

I am not saying the design should predict the answer; it is right not to, and R-A6 correctly stops short of the conclusion. I am saying the design treats `STRATEGY_BLOCKER` as a covered branch while planning, budgeting, and narrating as if `REGISTERED` → advance. On the design's own evidence, `REGISTERED` → `STRATEGY_BLOCKER` may be the *most* likely positive-seam outcome, and it is the one path where the round has to do real analytic work (the comparison-meaning judgment, over the critic checkpoint and the fresh reviewer) that nothing in the session table or the 8h budget accounts for. Surface it as a bet and budget for it. See M5.

### 8. Reader Comprehension
**Assessment:** Pass

This is a hard document that reads well. § The Point gives the mental model before any mechanism, § Core Concept states the thesis in one bolded sentence ("the proof lives in what the run was never told") that actually predicts the rest of the document, and the tables do real work rather than decorating. A reader unfamiliar with the item can skim it once and come away with the system, the bets, and the decisions.

Two comprehension nits, neither blocking: § The round's task table and § Sessions describe the same sequence in two different framings (by task, by run), and a reader has to hold both to see that T-002 happens in session 05 which is session 03 resumed. And § The commit sequence's row 4 is where three separate obligations (D5's ruling, the seam run, C-SEAM) collapse into one line. Both are fine for the plan author; a first-time reader would benefit from one sentence joining the two tables.

---

## Issues by Severity

Classified must-fix / advisory per the brief. "Must-fix" = the design as written will produce a wrong or contradictory run and the plan cannot resolve it by choosing well.

### Must-fix

- **M1 — The checkpoint can pass on the WI-031 hand pattern, and D5 then overrides a passed checkpoint.** *(Route Safety / Spec Compliance, R-C1)* Session 03 reads `GOAL_RUNBOOK.md` § The native seams before it writes the reading and proposed dispositions — and today that section tells it the `research` seam is unrepaired and routes it to the WI-031 hand pattern (`:264`). So the proposed *research disposition* handed to the fresh critic at C-001.r1 will plausibly name the hand pattern, and the critic — reading the same stale runbook — will plausibly pass it. D5's ruling then arrives at T-002 and changes the route to the native seam. R-C1's guarantee is that a fresh critic approved the dispositions *before* the follow-up executed; what executes here is not what the critic approved. The design's own § Failures framing anticipates the staleness but not this sequencing consequence. **Resolution:** the design must say what happens when the T-002 ruling changes an already-passed disposition. The clean answer is that a route change to a passed disposition requires a new `C-001.r2` submission (which R-C6 already provides the shape for, and which costs one session inside the conditional 04b budget). The alternative — delivering the ruling *before* the checkpoint rather than after — is worse: it moves the ruling inside the window where it colors the critic's judgment, though notably not inside Invariant 3's staging fence.
- **M2 — Invariant 2 contradicts the brief-delivery mechanism, because the mechanism is never stated.** *(Abstraction Quality / Auditability)* Invariant 2 forbids any cold session's tool-call inputs from reading `.project/active/goal-research-model-proof/`. Every brief lives at `sessions/NN-<role>/brief.md` inside that directory (§ Component Overview). As written, a session cannot receive its own brief without breaching the invariant. Item 4's mechanism resolves this — the brief text is passed to `claude -p` on stdin, and the file in the item directory is the committed *record* of what was passed, never the session's read (`.project/completed/20260827_goal-cold-pickup-proof/plan.md:100` records confirming "how the brief is passed on stdin"). The Item 5 design never states this. **Resolution:** state the delivery mechanism explicitly, and state the per-session allowlist and denial list for sessions 03–08 the way Item 4's design does at `design.md:72` — the design currently refers twice to "every brief embeds its own denial list" without ever defining one outside the grounding brief.
- **M3 — The D8 mapping does not belong in `goal.md` § Invariants.** *(Abstraction Quality / Spec Compliance, R-A3)* § Invariants has a defined contract in the runbook: "the invariants a comparison must preserve, so a later round cannot drift the meaning of 'better'" (`:68`), and it is one of the five field classes whose non-hollowness R-A3 checks before any task is authorized. A seam-class → task-outcome routing table is an operational reading, not a comparison invariant. Putting it there pollutes a field class an auditor reads for a different purpose, and it is doubly awkward because § Invariants already carries R-A6's real content (the `p_pump` channel and the equal-input/unequal-effect distinction). **Resolution:** give the mapping its own home. It must predate the round to do its job (D8's stated reason is sound), so an item-side committed file — `covering-branches.md` is already the pre-declared-readings artifact and already commits at C-COVER ahead of C-T001 — is the natural place, with the trail citing it. Whatever the home, the design should also state plainly what M3 is: the item taking a judgment the runbook leaves to the round agent, and why.
- **M4 — The `BLOCKER` → `MECHANICAL_FAILURE` retry authorization exceeds what the runbook permits.** *(Route Safety, R-D3 / runbook `:132`)* The class mapping itself is right — the guide's `BLOCKER` is "the invocation could not get far enough to say anything about any candidate … fix what `reason` names — a malformed request, an unwritable registry — and re-run" (`:159`, `:166-168`), which is machinery broken and meaning intact. But D8 and § Potential Risks both authorize the retry as "retried within the cap **after fixing the request**", and `GOAL_RUNBOOK.md:132` permits a retry **only** when "the task, its inputs, its scope, and its meaning are all identical." A malformed request fixed by editing `question`, `consumer`, `gap_type`, or `where_to_look` changes the seam's own request key (`research_seam_operator_guide.md:108`) — by the seam's own definition it is a different request, so by the runbook's definition it is a different task, not a retry. **Resolution:** split the case. A blocker whose fix leaves the request key unchanged (unwritable registry, environment, `limits`) is a legal `MECHANICAL_FAILURE` retry under the same T-00N id. A blocker whose fix changes any key field is a new task with a new scope, and the trail must show it as one. Getting this wrong is precisely what the fresh reviewer checks ("retry classification — was each retry genuinely mechanical, with task, inputs, scope, and meaning identical?", `:169`), so it will surface as a review finding if left.
- **M5 — `REGISTERED` → `STRATEGY_BLOCKER` is an unstated bet and an unbudgeted path.** *(Bets & Decisions)* See Dimension 7. The design's own R-A6 evidence (band ~60–190 MW against a held 1.0 MW; arms at `rec_frac` 0.94/0.79/0.68; `recirc_ok` already failing at three different radii) makes it likely that a successfully registered source moves the premise rather than the value. The design plans, narrates, and budgets the `REGISTERED` branch as though advance were the natural sequel, and treats `STRATEGY_BLOCKER` only as a covered non-exercise. **Resolution:** state it as a bet with its "if false" (B6: *a registered value preserves the strategy's premise* → if false, T-002 or T-003 returns `STRATEGY_BLOCKER` via gate (c), criterion 4 goes non-exercised under the declared branch, and criterion 3 is still met). Confirm `covering-branches.md` lists it explicitly — R-H4's own list does name the `STRATEGY_BLOCKER` close, so this may be only a design-narrative fix — and budget the comparison-meaning judgment, which is the one honest outcome that costs analytic work rather than a park.
- **C1 — R-A7's owner-graded removal is implemented as an appended note.** *(Spec Compliance)* Detailed in Dimension 1. The list member at `.project/CURRENT_WORK.md:22` must be struck, not annotated beside.
- **C2 — R-C2's `:140` surfacing obligation is dropped.** *(Spec Compliance / capture-fidelity Rule 4)* Detailed in Dimension 1. Needs a named landing site.

### Advisory

- **A1 — Invariant 9 is not auditable as written.** *(Auditability, priority 5)* Invariants 1–8 and 10 all resolve to a command over disk: brief-ancestry walk, tool-input fence sweep over transcripts, pre-T-001 brief grep, two `git merge-base --is-ancestor` calls, `uv run python scripts/source_registry.py verify` (I confirmed the `verify` subcommand exists), `tests/study/test_records.py` (confirmed present), a scoped `GOAL_RUNBOOK.md` diff, and a keyword grep over the item diff. Invariant 9 — "every disk predicate against a goal file is date-anchored" — is a rule about commands the operator ran, and once a run is over there is no artifact to check it against. It is a real and valuable operating discipline (it is Item 4's harness error 08a, and it belongs in Implementation Notes where it already is), but listing it among invariants an auditor verifies overstates it. Either drop it to a note, or make it checkable by requiring `verification_record.md` to paste every predicate command it used.
- **A2 — the fence does not cover `.project/backlog/`.** *(Route Safety)* `epic_goal_strategy_task_harness.md` § Item 5 states the intended `model → research → model` sequence and the native-research-seam criterion. It names no `p_pump`, Moscato, or WPBOP (I checked), so the leak is about the *shape* of the errand rather than its content — but Invariant 2 does not cover it and the design does not acknowledge it. Either add it to the denial list or record it in `verification_record.md` as a second ambient hint, the way § The grounding guard already handles row `#3`'s Home column. That existing paragraph — surface the hint you cannot remove, and judge the criterion on the work actually done — is the right model and should just be extended.
- **A3 — Invariant 10's grep is weaker than its claim.** *(Auditability)* "No task envelope, event ledger, digest comparison, idempotency layer, reconciliation pass, or dispatcher appears in the item's diff" is checkable by keyword only for the named nouns. A dispatcher does not have to call itself one. Given this item ships almost no code, the practical risk is near zero — but the verification record should say the check is a keyword sweep plus a read of the diff, not claim mechanical completeness.
- **A4 — session 08's authority to open round 2 is unbounded.** *(Session choreography, priority 6)* The choreography is otherwise legal: session 03 authors the whole round and reviews nothing; 04 and 08 authored no part of what they review; the grounding session authored `goal.md` but not the round and is reused as neither reviewer — all consistent with ADR-002 and § What "fresh" means. Resuming session 03 across turns 05/06/07 is correct, not a violation, since one agent per round is the rule and the operator turns are exactly Item 4's committed-resume-brief mechanism. But `GOAL_RUNBOOK.md:181` says that after a pass the fresh reviewer "either recommends the owner-held close or writes the next strategy revision — which opens round N+1", and D2 says no round 2 is opened. Session 08's brief should say which of the two the item wants, without scripting the verdict.
- **A5 — budget floor is inside 8h but has little slack.** *(Budget realism, priority 7)* The floor path is 01, 02, 03, 04, 05, 07, 08 — seven sessions with 06 conditional, against the stated 8–10. That is inside the 8h execute estimate on Item 4's measured shape. Two things eat the margin and neither is in the count: M1's likely `C-001.r2` re-submission (one session), and M5's comparison-meaning judgment if a source registers (real analytic work, not a park). Worth stating in § Potential Risks rather than discovering at the plan.
- **A6 — R-B4's five decision fields have no landing site.** *(Spec Compliance)* One clause in the task table or § The round closes it.
- **A7 — C3's limits slip.** *(Spec Compliance)* "no time limit" should read "tasks per round: none" per `GOAL_RUNBOOK.md:230`. Listed separately here because it is a one-word fix the plan will otherwise propagate into `goal.md`.
- **A8 — the two tables want one joining sentence.** *(Reader Comprehension)* § The round (by task) and § Sessions (by run) describe the same sequence twice; a reader has to derive that T-002 runs in session 05, which is session 03 resumed.
- **A9 — the product-lens ledger entry is still owed.** The spec marks `product-lens.md` "to be created at close; not yet run". I ran the lens reasoning inline and found no owner/`[HARD]` contradiction, but that is not the ledger entry the pipeline expects.

### On the priorities that came back clean

Recording these explicitly so the design agent does not re-litigate them:

- **Hardening rule (priority 8): clean.** `covering-branches.md`, `freshness-record.md`, `meta.md`, `operator-notes.md`, and `verification_record.md` are all prose artifacts on Item 4's precedent. Nothing crosses into R-H1's banned list — no envelope, ledger, digest comparison, idempotency layer, reconciliation, or dispatcher. `meta.md` records session id, command, cwd, log dir, times, exit status and kept/discarded, which is Item 4's exact shape and is a record of a run rather than a control structure. Invariant 6's `source_registry.py verify` is Item 2's shipped tool, not new machinery. The Non-Goals list bars new scripts explicitly.
- **Invariant 3's fence line (priority 3): correct.** Fencing briefs committed before T-001's return is the right line for staged discovery, and the T-002 brief naming the seam scripts falls legitimately outside it. D5 is phrased as an operator ruling with provenance (`docs/research_seam_operator_guide.md@9637f1b7`, the runbook row named as stale pending this item's own flip), not as an instruction that stages the errand, and the design commits to recording whether the round agent spotted the staleness unprompted — which is the honest way to keep the compensation from contaminating the measurement. The gap is M1's timing consequence, not the ruling's framing. One small addition: the ruling should carry its `[AGENT]` grade in the brief itself, not only in `operator-notes.md`.
- **Requirement coverage (priority 1): R-A2a, R-C3a, R-G4, and R-H4 all land solidly.** R-A2a gets the strongest section in the document; R-C3a's number is carried correctly; R-G4's `:262` and `:267` edits are both present and their line references check out; R-H4 gets D6, the `covering-branches.md` artifact, C-COVER, and Invariant 4.

---

## Recommendations

1. **Fix M1 first — it is the only finding that breaks a spec guarantee at runtime.** Decide and write down what a post-checkpoint route change costs. A new `C-001.r2` submission is the answer that keeps R-C1 intact.
2. **State the brief-delivery mechanism and the per-session allowlists (M2).** This is a paragraph, it is already solved in Item 4, and without it Invariant 2 reads as self-contradictory to anyone auditing the run.
3. **Move D8's mapping out of `goal.md` § Invariants (M3)**, and say plainly that the item is taking a reading the runbook leaves to the round.
4. **Split the `BLOCKER` retry rule by whether the request key changes (M4).**
5. **Promote the registered-source-preserves-the-premise assumption to a stated bet, and budget the comparison-meaning judgment (M5).**
6. **Close C1 and C2** — strike the Phase 4 list member rather than annotating it, and give R-C2's `:140` conflict a named landing site next to the seam-row failure.
7. Sweep the advisories at plan time; A1 and A7 are one-line fixes and A2 extends a paragraph that already exists.

---

## Resolutions

*To be filled during Stage 4, when the owner engages with this review. One entry per resolved issue — this is what the design agent reads to incorporate the review.*

---

**Overall:** Revise

The frame is right, the pattern is Item 4's and correctly adapted, and the proof's central discipline — make "the prerequisite emerged from the work" checkable from `git log` alone — is well served by everything in the document. Five must-fixes and two dropped spec obligations stand between this and a design the plan can execute without improvising. None of them requires rethinking the approach.

**Next Steps:** Once resolutions are recorded, re-run `/_my_design` (or return to the design-agent session) and point it at this review to incorporate. The reviewer does not edit the design. The product-lens ledger entry (A9) is still owed before close.
