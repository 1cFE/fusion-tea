# Concept-Design Review: Goal Strategy and Task Harness

**Concept:** `.project/concepts/goal-strategy-task-harness-design.md`
**Review File:** `.project/concepts/goal-strategy-task-harness-design-review.md`
**Date:** 2026-08-23
**Status:** Owner resolutions recorded 2026-08-23 — verdict **Revise**; awaiting author incorporation and final owner acceptance

> **Custody note (2026-08-23):** this review file was deleted from disk while the owner-resolution
> dialogue was in progress — apparently by the session that revised the concept — repeating the
> pattern finding M3 flags for the prior design's review. Restored by the reviewing session with
> resolutions intact. The review file is owned by the reviewer until resolutions close; the concept
> author must not delete it.

## Sources Read (Stage 1)

One line each, read before the concept's own rationale was adopted:

- `.project/concepts/goal-driven-model-development-harness.md` — the input concept: owner-graded quotes; goal → rounds → findings walked to research / model / seam; hybrid orchestrator; critics; replay ledger.
- `.project/concepts/goal-harness-design.md` — the superseded design: persistent orchestrator, the *finding lifecycle* as the orchestration unit, run directory + ledger + per-round decisions document.
- `.project/concepts/study-driven-model-development.md` — the governing prior concept: record contract, detectors, and the discovery log; criterion 4 is **owner-settled**: the log carries finding → disposition → what changed, across rounds, with no dangling dispositions.
- `.project/research/20260822-120756_research-extraction-harness.md` — the evidence base: the loop ran once by hand (Item 6); the acquisition/registration gaps; patterns P1–P10.
- `.project/active/run-study-first-consumer/plan.md` — the actual manual trace: Phases 1–3 complete and certified; two studies, one model item, one research round, one regeneration.
- `.claude/skills/run-study/SKILL.md`, `runbook.md` — the native study contract: executor/administrator split; step 14 makes the executor the sole writer of the discovery log; records immutable after step 15.
- `exploration/stellarator_e2e/studies/DISCOVERY_LOG.md` — 22 rows today; roughly 7 `unrouted` or "item not yet minted."
- `modeling_project/STUDY_POLICY.md` — the ratified rulebook (axis rule, constraint triage, no fallbacks, verification).
- `work/orchestration/handshake-lcoe-construction.md` — the existing hand-run orchestration-brief pattern: Align rulings, graded inputs, reserved gates, stage log.
- `.project/mental-alignment/runs/20260823-113407_goal-harness-status.md` — the state of play before the pivot; records that a review of the prior design existed (`goal-harness-design-review.md`) with three parked owner decisions. **That review file has since been deleted from disk.**
- ADR state: `.project/adr/` does not exist; the modeling AD registry (`modeling_project/ARCHITECTURE.md`, AD-001–AD-007) has no orchestration decision. CLAUDE.md's two-PM rule ("do not cross-reference between them") is the live guidance the cross-PM ADR candidate would amend.

**The semantic problem, stated before reading the proposal:** the stages exist and work; what is missing is an owner for the judgment *between* them — deciding what work is justified next, keeping that decision from going stale as evidence arrives, and surviving session death — so that someone other than the builder (human or agent) can run the loop and every decision can be replayed afterward.

## Fundamental Assessment

**Judgment: Concerns** — the skeleton (a control boundary above native workflows, native ownership preserved, fresh-agent round reviews) is right; one owner-settled obligation was dropped silently, and the mechanism scale is not supported by the evidence. Both the review and the independent ponytail challenge converge on the same two points.

### Are we actually solving the right problem?

Mostly yes, and the reframe is the concept's real strength. The superseded design treated the problem as *work tracking*: a queue of findings, each walked through states by a persistent orchestrator. This concept treats it as *authorization control*: a grounded goal, one revisable strategy, exactly one reviewed task, and the rule that no result authorizes its own follow-up. That targets the actual failure mode of agentic loops — stale forward authority and self-repair drift — rather than its bookkeeping symptom. The round boundary (one agent owns a round; a fresh agent reviews it) is a well-motivated control on the observed tendency of an agent to defend its own strategy.

The concept also gets invariant ownership right at the edges: `research` and `integrate` need callable native boundaries, and the concept names those as **prerequisite repairs at the native owner**, not logic inside the harness. That is exactly the posture this review exists to check for.

The problem is what fell off the truck during the pivot. The input concept and the prior governing concept both treat "what happens to a finding after a study logs it" as the thing that needs an owner; the prior concept settled at **owner grade** that the discovery log carries finding → disposition → what changed, across rounds, with no dangling dispositions (criterion 4), and criterion 5's "loop closes" is *demonstrated through* a finding moving. The concept under review (as reviewed) never mentioned the discovery log, record §15, or dispositions. Its only trace was the "Supersession" ADR candidate — graded `[AGENT]`, "pending acceptance" — which retires "the earlier finding-lifecycle control model" as historical. An agent-graded row cannot retire an owner-settled criterion, and the conflict was not surfaced anywhere. The ~7 `unrouted` discovery-log rows had no consumer in the new design. *(Owner engagement on this is recorded under Resolutions.)*

This does not make the strategy/task shape wrong. Task-as-authorization-unit and finding-as-evidence-unit can coexist: a round review could be obliged to disposition every open finding the round's evidence touches, or the owner could amend criterion 4. But that is the owner's call, and the concept resolved it silently. Until it is surfaced and ruled, the design has an ownership hole exactly where both parent documents said the loop was broken.

### Architecture verdict

The system shape — control boundary above native workflows, natives keep their state and technical proofs, evidence flows by reference with digests, hand-run and dispatched routes converge on one reconciliation — is right, and clearly better-shaped than the predecessor. The concerns are about weight and about what was dropped, not about the skeleton: the finding-disposition ownership hole (above), per-native-stage task granularity that partially re-encodes the native pipelines at the goal layer, and integrity machinery (sealed digests, idempotency keys, effect queries) sized for adversarial conditions the non-goals exclude. Each is fixable inside this shape.

## Ponytail Challenge

*Fresh subagent, ponytail role per `~/.claude/commands/_my_ponytail.md`, ultra intensity, architecture-adapted. Returned verbatim:*

---

**Posture:** ULTRA. Deletion before addition. The evidence base is two hand runs, both driven by the builder, both successful. Everything below is graded against what those runs actually needed.

**1. Does this machinery need to exist at all?**

Mostly no. Separate what the evidence shows from what the design builds.

**What the two hand runs actually lacked** (research doc `20260822-120756`, Summary and §4): a source-registration operation (WI-031's index entries were hand-written bash), a research-acquisition mode for `/research`, one shared research-request shape, and the upstream supersession stubs. The research doc's own verdict: "Feasible, and mostly assembly … four small pieces," with dispatch automation explicitly deferred ("Prove the loop interactively on the next Item 6 gap"). The design under challenge agrees — its Procedure Contracts section ends by conceding that research acquisition and the integrate boundary "are prerequisite capabilities, not logic inside the goal harness."

So the two real repairs live outside the harness. What the harness itself adds is a control plane: sealed goal digests, 16-field immutable task envelopes, a 6-event JSONL ledger, idempotency keys and effect queries, a reconciliation operation, three fresh-critic review types, and 11 procedure contracts. **No failure in either hand run is evidence for any of it.** The failures the runs produced are all in `DISCOVERY_LOG.md` — 22 rows — and every one is a model gap or a study-tooling defect with a native home. Zero rows say "authority drifted," "a stale task retained authority," or "we couldn't tell what ran."

**The smallest thing that lets a non-builder or an agent run the loop** already has a proven referent in the repo: `work/orchestration/handshake-lcoe-construction.md`. That one file — Align rulings, graded inputs, reserved gates, stage log — carried WI-029 through register → spec → design+review → two owner gates → plan → implement → audit → owner close, across sessions, with resume-from-prose working in practice. The input concept's own success criterion 8 asks for "one document [that] describes the loop end-to-end … usable without the orchestrator." That document has never been written. Write it, hand the six `unrouted` discovery-log rows to a non-builder session running the brief pattern, and observe the friction. That observed friction — not this design — is the requirements list for any machinery.

**2. What existing machinery can be deleted instead of accommodated?**

The design accommodates everything and deletes nothing. Three deletions it should be proposing instead:

- **The superseded finding-state ambiguity, resolved by deletion, not by silence.** The prior design (`goal-harness-design.md`) parked a real owner conflict: prior-concept criterion 4 says the log carries dispositions across rounds; the runbook makes the executor its sole writer. The new design's answer is to delete the *question* (see §5). The honest deletion is one of the two rules, by owner ruling.
- **The cross-PM citation prohibition, shrunk rather than parked.** The design parks "may goal artifacts cite `.project/` evidence" as an owner decision. But the existing, accepted `work/orchestration/handshake-lcoe-construction.md` already cites `.project/concepts/`, `.project/active/`, and `.project/backlog/` throughout. The prohibition as read is already dead practice; the research doc named the durable rule ("the join lives in `knowledge/` artifacts and `pm` operations; mutate each PM only natively"). Propose a one-line CLAUDE.md amendment; don't build a design around a parked reading of a rule the repo doesn't follow.
- **Nothing else needs accommodating.** The oracle is already retiring (policy §10). The record contract, discovery log, and administer mode need no changes for the brief pattern — which is exactly the "minimize changes to start" the owner asked for verbatim.

**3. Invariants at their real owners?**

Half yes, half no.

- **Yes:** pushing research-acquisition and integrate repairs to native owners is the design's best move. Keep it.
- **No — the ledger/reconciliation/idempotency layer compensates downstream for invariants the natives already own.** "Filesystem artifacts and native registries override claimed effects" is already the universal native invariant (research doc, Architecture Insights: the research step diffs `find_sources()`, the study store is crash-safe, spines tests byte-compare, `verify.py` re-derives). A goal-level `invoke_returned` event with "observed effects," an effect query per procedure, and a reconciliation operation re-state that invariant in a second place. If a native procedure can't tell you what it did from disk, that's a defect at the native owner (the design's own Principle 4!) — not a reason for a goal-side effects ledger.
- **No — per-stage task authorization compensates at the wrong altitude.** `model.open` through `model.audit` as seven separately enveloped, separately scope-reviewed goal tasks re-sequences what the modeling PM already sequences. The goal's legitimate checkpoints are two: "is this work item justified" (at open) and "did it land" (at audit/integrate). WI-029 ran all seven stages under one brief with two owner gates. The design would have minted ~9 envelopes, ~9 scope reviews, and ~50 ledger events for the same run.

**4. Which abstractions can be removed?**

In deletion order, with what breaks:

| Abstraction | Delete? | What breaks if gone |
|---|---|---|
| sha256-sealed goal digest + owner-set `grounded` seal | **Yes** | Nothing. The goal file is in git; a commit hash already seals content. No tool verifies the digest; "only the owner may set status" is convention either way. |
| 16-field immutable task-envelope YAML | **Yes — shrink to prose** | Nothing. No parser or consumer is named. The WI-031 spec table (4 columns) and the handshake brief's Align section carried identical authority. Keep the *discipline* (one task, scope, out-of-scope, success/exhaustion) as a brief section, ~6 lines of prose. |
| 6-event append-only JSONL ledger | **Yes** | Nothing today. No reader exists; "status derivation" is listed as still-needed design. The stage log satisfied the owner's verbatim "running on-disk log" requirement in WI-029. Revisit only if a dispatched (headless) route ever exists — which has never been attempted (the prior design named it the first risk; still untried). |
| Idempotency keys + effect queries per procedure | **Yes** | Nothing. Resume = read the directory — the invariant every native already enforces, and the administer role already proves cold-read works. |
| Reconciliation operation for hand-run parity | **Yes** | Nothing. Hand-run parity in the brief pattern is "the human writes the same stage-log line," demonstrated across the whole WI-029 run. |
| Three fresh-critic review types | **Cut to one** | Keep the round review — the fresh-pickup bet is genuinely good and matches the administer precedent. Task-scope review is the same fresh agent's job when it writes the next strategy; the "retry critic" is a hash comparison plus one logged judgment, not a review type. |
| 11 procedure contracts | **Cut to 4 seams** | study (exists: execute/read), research (native repair), modeling item as *one* contract open→audit, integrate (native repair). This is exactly the five-kinds-of-work table the mental-alignment run already derived. |

What survives, because it earns its place: no forward plan; one bounded strategy per round; bounded negatives and strategy blockers as first-class outcomes; fresh agent reviews the round and writes the next strategy; owner keeps close/archive. That is roughly 20 lines of the current 220.

**5. Smallest architecture — and the silent drop**

**The silent drop first, because it is disqualifying.** The governing concept (`study-driven-model-development.md`) has owner-settled criteria: the discovery log carries **finding → disposition → what changed, with no dangling dispositions, across rounds** (criterion 4), and the loop demonstrably closes on findings (criterion 5). The owner's verbatim: "we should make the log of discoveries an explicit deliverable." The superseded design at least made the finding the orchestration unit and honestly *parked* the writer conflict as an ADR for the owner. The new design replaces the finding with the task as the unit — and the words "finding," "discovery log," "§15," and "unrouted" appear **nowhere in it**. `DISCOVERY_LOG.md` today holds six `unrouted` model findings (`20260821-power-cycle-ab#1,#2,#5`; `20260823-magnet-technology-ab#2,#3,#4`) — including the confinement-closure gap that is the actual headline of study 2 — and in the proposed system nothing consumes them. The review file that recorded the parked conflict has been deleted from disk. That is a premise conflict between two owner-graded artifacts resolved silently, in the deleting direction — precisely what capture-fidelity §4 forbids. The design's Prior Art section says "the design succeeds only if a fresh agent can reconstruct why each task ran" — but tasks are not the semantic problem; *findings walking to dispositions* is the semantic problem, the one the owner named as a deliverable and possibly a contribution.

**The smallest architecture that solves the semantic problem:**

1. `work/orchestration/goals/{goal}/goal.md` — grounded with the operator, prose, sealed by git. (Keep from this design.)
2. `trail.md` in the handshake-brief pattern — Align rulings, graded inputs, per-round strategy + result + fresh review as dated stage-log entries. One file, proven referent.
3. **The findings walk as the round's spine:** each round's decisions take the open `unrouted` rows plus new §15 rows and assign next steps; one owner ruling resolves who appends disposition updates to the log (the parked ADR, un-deleted).
4. The two native repairs (register-source + `/research` acquisition; the integrate boundary) — already correctly located by this design.
5. Fresh agent per round for pickup and review — the one control idea here that earns its cost.

No envelopes, no ledger, no digests, no reconciliation, no dispatch — until a non-builder run of rounds on the six unrouted rows produces a failure that prose demonstrably cannot carry.

**6. Verdict**

**CHALLENGE.**

**The one most important reason:** the design silently abandons the owner-settled obligation that findings are walked to dispositions across rounds — the discovery log and its six `unrouted` rows have no consumer anywhere in the goal/strategy/task model — and spends the whole complexity budget instead on an authority-control plane (sealed digests, immutable envelopes, event ledger, idempotency, 11 per-stage contracts, three critic types) for which two successful hand runs provide zero demand evidence. It deletes the problem and builds the non-problem. Before any acceptance: restore the finding walk as the unit the harness serves (or get an explicit owner ruling superseding criterion 4 of `study-driven-model-development.md`), extract the two native repairs as their own items, and reduce the harness itself to the proven brief pattern plus the fresh-round discipline — then let a non-builder run actually fail before any envelope or ledger is written.

---

### Disposition

Strand by strand — nothing averaged away:

- **P1 — Silent drop of the finding walk (criterion 4; the deleted parked ADR): ACCEPTED.** Identical to this review's C1, independently derived. The concept must change: restore an owner for the cross-round finding-disposition obligation, or put the amendment of criterion 4 to the owner as an explicit decision. Verdict cannot be Approve until incorporated.
- **P2 — Control plane has no demand evidence (digests, envelope YAML, event ledger, idempotency keys, effect queries, reconciliation): ACCEPTED IN PART; OWNER DECISION REQUIRED on scale and sequencing.** Accepted: no failure in either hand run motivates any element of it; the WI-029 brief pattern is a proven referent for resume, rulings, gates, and hand-run parity; each element must be justified against a demonstrated need or staged behind one. The sealed-digest and effect-query rows are accepted for deletion-or-defense (this review's M4, now sharpened). Owner decision: whether the first build is the lean brief-pattern loop (prove on the `unrouted` rows, harden on observed friction) or the full control plane built once. The owner ratified the strategy/task *shape* in the 2026-08-23 discussion; the ponytail's re-derivation contradicts the *mechanism scale*, and the recorded reasoning behind the ratification is too thin (M3) to settle it — so the prove-first vs build-once tradeoff goes to the owner.
- **P3 — Per-stage authorization at the wrong altitude (11 contracts → ~4 seams; 2 checkpoints per work item): ACCEPTED in substance.** Identical to M1, with stronger evidence than this review had: WI-029 ran seven native stages under one brief with two owner gates. Per-stage *stop points* (research interrupts; bounded negatives) do not require per-stage authorization envelopes. The concept must argue the granularity against its review cost or coarsen it.
- **P4 — Three critic types → one fresh round review (+ retry as a hash check): ACCEPTED IN PART.** The review-topology ADR candidate is already `pending acceptance`; the concept must defend the task-scope critic's marginal value over "the fresh round agent authored the strategy the task serves," and the retry review's status as a review type rather than a mechanical check plus one logged judgment.
- **P5 — Cross-PM prohibition is dead practice; propose the CLAUDE.md amendment instead of parking: ACCEPTED as a sharpening; the decision remains the owner's.** Verified: `work/orchestration/handshake-lcoe-construction.md` cites `.project/concepts/`, `.project/active/`, and `.project/backlog/` throughout and was accepted practice. The parked decision should be presented to the owner as "ratify existing practice with a one-line CLAUDE.md amendment," not as a novel exception. *(Since resolved by the owner — see Resolutions.)*
- **P6 — "Don't build the harness; write the operator document and observe friction": REJECTED IN PART, with evidence.** The owner's verbatim asks make a goal-layer control boundary the mandate, not merely documentation: "I would like to offer a higher level of abstraction: user sets a goal, and the system can execute the different stages and loop autonomously," and "we MUST design for 'resumes'." A concept for that layer is in-scope work, not speculative machinery. The legitimate kernel of this strand — prove a lean loop before hardening it — is carried in P2's owner decision, not by discarding the concept.

## Dimensional Review

### 1. Semantic Model — **Concerns**

The strategy/task/round model represents the domain's real semantics directly: authority, staleness, and the difference between an operational accident (retryable) and a discovery (round-closing). The outcome vocabulary (`achieved | bounded_negative | strategy_blocker | owner_gate | operational_blocker`) encodes the owner's "bounded negatives are useful outcomes" requirement faithfully.

The gap: the *finding* — the domain object both parent concepts treat as what the loop exists to move — had no representation as reviewed. `result_recorded` carries a free-text "goal implication," but nothing joins a study's §15 rows to any later task, so "no dangling dispositions" is unprovable in this model. See Critical C1 and its resolution-in-progress.

Also note: preservation of the current pipeline is honest here — natives are treated as evidence and their defects (research/`integrate` boundaries) named for repair, not wrapped. No mechanism category exempts a user-visible behavior.

### 2. Responsibility and Invariant Ownership — **Pass** (one hole)

Clear single owners: natives own their state and technical proofs; the goal layer owns authorization and goal-fit; the owner holds grounding, reserved gates, and close/archive; the seam owns no domain question. Repairs pushed to producers (research, integrate) rather than compensated downstream — the right direction. The one guarantee with no owner is the cross-round finding-disposition obligation (C1). The cross-PM seam ownership change is surfaced as an explicit owner decision rather than smuggled — correct handling (and since ruled by the owner).

### 3. Simplification and Deletion — **Concerns**

- What this concept supersedes (the prior design's finding states, per-round decisions document, per-finding queue) was never built, so nothing real is deleted; the comparison is paper-to-paper.
- Nothing existing is retired or unified: the harness adds a fourth artifact family (goal home) beside the study record, the modeling work item, and the orchestration brief. That may be inherent to a new control layer, but the concept claims compact persistence while the envelope + six-event ledger + three review artifacts *is* a second workflow object model at task granularity. The bet is only honest if the ledger cites native evidence and never restates it; that rule is implied (refs, digests) but not stated as an invariant. See Major M2 (partially addressed in the post-review revision).
- The orchestration-brief pattern (`work/orchestration/*.md`: Align rulings, graded inputs, stage log) is the closest existing machinery to the goal home. The concept cites it as prior art but does not say whether the goal home replaces that pattern for goal-driven work or coexists with it. A cheap deletion opportunity: state that a goal directory *is* the orchestration brief's successor for these runs.

### 4. Abstraction Quality — **Concerns**

- **Earn their place:** goal / strategy / task / round / seam. Strategy-with-abandonment-conditions in particular is a genuinely better abstraction than a forward plan.
- **Heavier than the demonstrated problem:** sha256-sealed goal digests, strategy digests, per-procedure idempotency keys and effect queries, immutable envelope-by-digest. Crash recovery justifies idempotency thinking at the seam; cryptographic sealing of a single-operator, git-tracked file tree is process armor with no demonstrated adversary. Git already provides content addressing and history. The concept should either name the failure these digests catch that git + review does not, or thin them to "immutable by convention, enforced at review" for the first build. (Detailed design may still conclude digests are cheap enough to keep — but then that is a design decision, not a concept-level requirement.)
- **11 procedure contracts:** making every native modeling stage (`model.spec` … `model.audit`) a separately authorized, separately scope-reviewed goal task re-encodes the native pipeline's sequencing at the goal layer and buys a heavy review cadence (a routine one-item round ≈ 8–11 scope reviews plus a round review). The stated justification — research may interrupt between stages; a stage result changes what is justified — requires per-stage *stop points*, not necessarily per-stage *authorization*. See Major M1.

### 5. System Confidence — **Pass**

Strongest section of the concept. Seam obligations are explicit per procedure (invoke with / native return / goal decision). Route agreement (dispatched vs hand-run) has an equivalence claim and a named mechanism (same envelope, same reconciliation, `actor: human`). Unowned proofs are named honestly — fresh-round pickup, crash recovery without duplicate effects, hand-run parity, clean closure without a study — and the validation strategy exercises each (replay Item 6, kill/resume around first effect, dispatch-vs-hand comparison, blocked-round closure). Dangerous combination not named: a native `work/` item advanced *outside* any goal task while a round holds it via `work_item_refs` — worth one line in detailed design.

### 6. Decisions and ADR Candidates — **Concerns**

The candidate table exists, carries provenance grades, and correctly parks the cross-PM decision for the owner (since ruled). Two problems:

- The **Supersession** candidate is under-honest: it retires an owner-settled criterion (prior concept criterion 4) under an `[AGENT]` grade without naming the conflict (C1).
- Every "ratified by owner, 2026-08-23" grade rests on an unrecorded design discussion, and the prior design's review file — which carried three explicitly parked owner decisions — was deleted from disk. Two of the three parked decisions receive implicit answers in this concept (sequencing; research critic → review topology); the third (who writes finding state) receives none. The evidence chain for the pivot's owner rulings is thinner than for any other shaping document in this line. See Major M3.

Per-candidate disposition is in the ADR Candidate Assessment section below.

### 7. Comprehension — **Concerns**

A cold reader who has the two parent concepts can reconstruct the shape, but only with effort. The input concept's five-line frame ("a goal is a question… every finding goes to one of three places…") has no successor here; the document opens in mechanism vocabulary (envelope, ledger, digest, round) without a plain-language walk of one round first. Two overlapping stop/outcome enums (task outcomes; round stop reasons) must be held simultaneously. The vocabulary is precise and consistent — the issue is layering, not sloppiness. One "how a round actually goes" narrative paragraph before the data model would fix most of it.

## Issues by Severity

### Critical

- **C1 — Silent retirement of an owner-settled obligation.** Prior concept criterion 4 (`[OWNER]`: discovery log carries finding → disposition → what changed, across rounds, no dangling dispositions) and the prior design's parked owner decision (who writes a finding's state after the study logs it) have no owner, no mechanism, and no mention in this concept; the `[AGENT]`-graded Supersession candidate is the only trace. The ~7 `unrouted` log rows have no consumer. Surface it: either (a) give the round result/review an explicit obligation to disposition every open finding the round's evidence touches, joined by `<study-id>#<n>`, or (b) put the amendment of criterion 4 to the owner as its own decision. Verdict cannot be Approve until the owner rules. *(Owner engagement recorded under Resolutions; residual confirm pending.)*

### Major

- **M1 — Per-native-stage task granularity is asserted, not argued.** The procedure table makes each native modeling stage a separately authorized and scope-reviewed goal task, re-encoding native sequencing at the goal layer and imposing ~8–11 fresh-critic reviews per routine round. The interruption/re-justification rationale needs per-stage stop points, not necessarily per-stage authorization envelopes. Either argue the granularity against its review cost, or name granularity an open detailed-design question with a coarser envelope (e.g. "advance WI-XXX until bounded result or blocker") as the live alternative.
- **M2 — The ledger's restatement boundary is unstated.** `invoke_returned` (observed effects, raw-output ref, proposed outcome) and `result_recorded` (native evidence refs, accepted outcome) sit on territory native records already own. Without an invariant like "the ledger cites native evidence by ref and never restates it," the event schema will grow into a mirror of native state — the very thing the concept's own bet forbids. *(Partially addressed in the post-review revision — see Resolutions.)*
- **M3 — The pivot's provenance is unrecorded.** Owner ratifications of 2026-08-23 exist only in chat; the prior design's review (three parked owner decisions) was deleted rather than resolved-on-record. Record the ratifications (quotes or a dated ruling note in the concept), and disposition the deleted review's three parked decisions explicitly — one line each — so the shaping chain has no invisible hops.
- **M4 — Digest/sealing machinery exceeds the demonstrated threat.** Sealed goal digest, strategy digests, envelope immutability by digest, idempotency keys, effect queries — for a single-operator, serialized (non-goal: no concurrency), git-tracked system. Name the failure each catches that git + review does not, or downgrade to convention-plus-review for the first build and let a real drift incident promote them. *Sharpened by ponytail P2, which extends the same demand-evidence bar to the event ledger and the reconciliation operation, with the WI-029 brief as the proven prose referent; the scale/sequencing tradeoff is parked as an owner decision (see Disposition P2).*

### Minor

- **m1 — Two overlapping outcome enums.** Task outcomes and round stop reasons could be one derivation (round stop reason = f(last task outcome, caps)); as written both must be maintained in agreement.
- **m2 — `model.open` as a full task.** Minting a native work-item container is a cheap deterministic operation carrying a full envelope + scope review; consider folding it into the first substantive stage task.
- **m3 — Goal-home vs orchestration-brief coexistence unstated** (see Dimension 3): say whether `work/orchestration/goals/{goal}/` supersedes the flat `work/orchestration/*.md` brief for goal-driven runs.
- **m4 — Research-doc guidance conflict, cosmetic.** The research basis recommended the cross-PM join live in `knowledge/` artifacts and pm operations; the concept puts the goal home in `work/orchestration/` (owner-set) and parks the citation question. Fine — but the concept should not cite the research doc as unqualified support without noting the divergence.

## ADR Candidate Assessment

- **Strategy and task** — **keep.** Load-bearing, dense, honestly graded `[AGENT]` (ratified by owner). Before filing: record the ratification evidence (M3) — a filed ADR resting on an unrecorded chat is challengeable at its root.
- **Round boundary** — **keep.** Owner purpose + agent mechanism is the honest split; affected seams (round result, review, strategy authorship) are named.
- **Review topology** — **reshape.** Its content is sound, but it cannot be filed until M1 (task granularity) is resolved — the number and placement of scope critics is exactly what granularity decides.
- **Goal evidence seam** (formerly "Cross-PM seam") — **keep; now `[OWNER]`-ruled** (see Resolutions). The filed ADR must name CLAUDE.md's live "do not cross-reference" rule as an affected surface to amend.
- **Supersession** — **reshape (do not file as written).** It silently retires prior-concept criterion 4, which is owner-settled and cannot be superseded by an `[AGENT]` row. Split it: (i) task replaces finding as the *orchestration* unit — agent-grade, fileable after C1 is ruled; (ii) the fate of the cross-round finding-disposition obligation — owner decision, to be recorded with the ruling.

## Resolutions

- **C1 / P1 (finding walk) — RESOLVED `[OWNER]` 2026-08-23, in two parts.** (1) Mechanism: "it should now be addressed in the design — `LearningLog` ├── `RoundResult` (mandatory, even when intent failed) └── `RoundReview` (fresh next goal agent)"; the concept was revised on disk accordingly (`learnings.md` append-only run memory; entries proposed by `RoundResult`, accepted or corrected by the fresh `RoundReview`; invariant "Every learning cites an accepted result; mechanical failures produce no learning entry"). (2) The `DISCOVERY_LOG.md` join, ruled **option (a)**: criterion 4 of `study-driven-model-development.md` **holds as settled** — `RoundResult`/`RoundReview` must disposition every open log row the round's evidence touches, and the goal agent appends the disposition update to `DISCOVERY_LOG.md`, joined by `<study-id>#<n>`. One runbook sentence amends the sole-writer rule: the study executor writes first-sighting rows; a goal round may append disposition rows. This also retro-resolves the prior design's parked ADR ("who writes a finding's state after the study logs it") in the direction its deleted review recommended. The Supersession ADR candidate may now be filed split per the assessment, carrying this ruling.
- **Goal evidence seam (P5 / former cross-PM parked decision) — RESOLVED `[OWNER]` 2026-08-23:** the revised concept carries the "Goal evidence seam" ADR candidate at owner grade: goal input references may cite `.project/` artifacts by path and digest; each PM remains mutable only through native operations. This ratifies existing practice (the WI-029 brief already cited `.project/` paths). Filing note stands: the ADR must name CLAUDE.md's "do not cross-reference" rule as an affected surface.
- **M2 (ledger restatement boundary) — partially addressed in the revision:** the ledger is now framed as "persistence plumbing, not the semantic model," and the LearningLog "indexes accepted results; it does not replace their evidence." The explicit cite-don't-restate invariant for `invoke_returned` / `result_recorded` payloads remains for the author to state.
- **P2 / M4 (control-plane scale and sequencing) — RESOLVED `[OWNER]` 2026-08-23, option (a): lean first, harden on evidence.** First build = goal file + the brief-pattern trail carrying strategy / task / result / review as dated prose sections, plus the fresh-round discipline and the C1 discovery-log join, run on the open `unrouted` rows. The envelope YAML, event ledger, digests, idempotency keys, and reconciliation remain in the concept as the *hardening path*, each promoted only when a run demonstrates prose failing — the first headless dispatch being the natural trigger. Owner's words: "yeah I agree with (a)."
- **M1/P3 (task granularity) and P4 (critic count) — direction settled by implication of the scale ruling; graded `[AGENT]` inference, owner may override.** A lean brief-pattern loop cannot carry ~9 scope reviews per round, so the consistent reading is the coarse grain: one task = one bounded objective that may span native stages until a bounded result or blocker, with per-stage *stop points* preserved (research interrupts, bounded negatives); the fresh round review is the one standing critic, task-scope review lightweight within it, retry as a mechanical check plus one logged judgment. The author implements this in the revision; the 11-procedure table may survive as seam *vocabulary* but not as 11 separately enveloped authorization units in the first build.
- **M3 (ratification recording) — partially discharged by this dialogue.** The rulings above are now on the record in this file, in the owner's words where given. Remaining for the author: cite this review's Resolutions from the concept (or restate the rulings inline with dates), and add the one-line dispositions of the deleted prior review's three parked decisions (finding-state → resolved here under C1 option (a); sequencing → resolved here under P2 option (a); research critic → absorbed into the review topology per P4).

## Verdict

**Revise.**

The system shape — a goal-layer control boundary, native workflows keeping their state and technical proofs, prerequisite repairs at native owners, fresh-agent round reviews — is right, and better than its predecessor. It is not filed-and-forgotten wrong (Rework): even the ultra-intensity ponytail's "what survives" list keeps the concept's principles (no forward plan, one bounded strategy per round, bounded negatives as first-class outcomes, fresh round review, owner-held close). What must change before acceptance:

1. **C1 / ponytail P1 (accepted, material — blocks Approve):** restore an owner for the cross-round finding-disposition obligation, or put the amendment of prior-concept criterion 4 to the owner as an explicit decision. The concept may not retire an owner-settled criterion under an `[AGENT]` grade. *(Owner engagement in progress — see Resolutions.)*
2. **Owner decisions — all obtained (2026-08-23, recorded under Resolutions):** (a) C1's discovery-log join — criterion 4 holds; rounds disposition open log rows; goal agent appends disposition rows; one runbook sentence amends the sole-writer rule. (b) Control-plane scale — **lean first, harden on evidence**; envelope/ledger/digests/idempotency/reconciliation become the hardening path, promoted only on demonstrated need. (c) Goal evidence seam — `[OWNER]`-ruled in the revised concept.
3. **Concept revisions (directions now fixed by the rulings):** coarsen task granularity to bounded objectives with per-stage stop points, keeping the procedure table as seam vocabulary (M1/P3); state the ledger's cite-don't-restate invariant (M2, partially done); cite this review's recorded rulings and disposition the deleted review's three parked decisions inline (M3); restructure the persistence mechanisms as the staged hardening path per the P2 ruling (M4); collapse the critic types to the fresh round review with lightweight scope/retry checks (P4); add the C1 `DISCOVERY_LOG.md` join and the runbook sentence; minors m1–m4 at the author's judgment.

Per review rules, the accepted material ponytail challenge prevents Approve until incorporated. The concept-design author incorporates this review; ADR candidates are filed only at final owner acceptance.
