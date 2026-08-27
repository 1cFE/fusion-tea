# Spec Review: Goal Grounding, Cold-Pickup Resume, and Round-Review Proof

**Spec:** `.project/active/goal-cold-pickup-proof/spec.md`
**Contract:** `claude-pack/commands/_my_spec.md`
**Review File:** `.project/active/goal-cold-pickup-proof/spec-review.md`
**Date:** 2026-08-26

Severities: **must-fix** (blocks the spec becoming the contract) / **should-fix** (fix before design starts) / **consider** (design or owner may absorb it).

---

## Reality Check

**Sound.** The spec is about the right work item, the Problem section is accurate, and the criteria map onto the epic's six without silent narrowing. Every artifact-facing claim I spot-checked is true: `work/orchestration/goals/` does not exist; discovery row `20260823-magnet-technology-ab#2` is `unrouted` today (`exploration/stellarator_e2e/studies/DISCOVERY_LOG.md:20`); DI-010 is at `knowledge/KNOWLEDGE.md:76`; `work/completed/20260822_WI-031_research-round-item6-values/` exists; the `[OWNER]` hardening ruling is at `goal-strategy-task-harness-design-review.md:209`; the freshness quote is genuinely `[OWNER]` at `goal-driven-model-development-harness.md:47`.

The § "A predicted prose failure" premise is **correct** — I verified it independently (see L1-4). Design would not be badly misled by this spec, but four defects would let a technically-passing proof prove less than the epic asked for. Verdict is Revise, not Approve.

---

## Audit

### Lens 1 — Faithfulness

**L1-1 · Direct claim (must-fix):** Success Criterion "Bounded closure" (spec:37) says the round closes "on one of the six close triggers — legitimate bounded-negative, unresolved owner gate, or declared limit." **Bounded-negative is not one of the six close triggers.** The runbook's six are: a valid study reading, a strategy blocker, changed comparison meaning, an unresolved owner gate, a declared limit, and the goal answered (`GOAL_RUNBOOK.md:84-91`). `BOUNDED_NEGATIVE` is a *task return outcome*, and the runbook is explicit that its effect is "A first-class result; choose the next task" (`GOAL_RUNBOOK.md:120`) — it leaves the round open. Requirement (spec:82) repeats the error and cites § Opening and closing a round as its authority, which is the section that contradicts it.

This matters because the round is required to close with no pin and no study, which also rules out trigger 1. A cold round agent following this spec would look for a closure route Item 1's contract does not offer, and the admissible set is actually narrower than the spec advertises: strategy blocker, changed comparison meaning, owner gate, declared limit, or goal answered.

The epic seeded this wording (`epic_goal_strategy_task_harness.md:321`), so the honest move is not to quietly copy it or quietly fix it. This is a Law-4 premise conflict between the epic and Item 1's shipped contract, and it should be surfaced in the spec as one, with the criterion restated against the runbook's actual trigger list.

**L1-2 · Direct claim (must-fix):** Two requirements are tagged owner-grade for content the owner did not originate.

- spec:56 — `**[NEED]** [OWNER 2026-08-26]` for the `vol_cold_cryo` question. `align.md:29-35` records this correctly: the *delegation* is `[OWNER 2026-08-26]` ("you pick"), and the pick itself is the "Orchestrator's recorded call `[AGENT]`". The requirement's prose says so honestly ("is the orchestrator's pick, delegated by the owner") but the tag contradicts the prose. Under `capture-fidelity.md` § 1, `[NEED]` is settled-eligible and owner-originated; an orchestrator pick is `[INFERRED]`, or `[AGENT]` carried down. As tagged, the question becomes do-not-relitigate when it is a judgment call design or the owner may still overturn.
- spec:58 — reserved gates, tagged `**[NEED]** [OWNER 2026-08-26]` with a trailing parenthetical "(`[AGENT]` default, ratified by the owner.)". The settled rule is exact on this case: "An approved agent recommendation stays `[AGENT] (ratified by owner, date)`" and is *not* settled. The parenthetical is the correct grade; the primary tag overrides it.

Fix the tags, not the prose. Note the asymmetry in how each is challenged: an `[OWNER]` item is challenged by asking the owner, an agent-grade one by re-deriving against its recorded reasoning — which is exactly the reasoning `align.md:33-35` preserves for the question pick.

**L1-3 · Direct claim (should-fix):** The `[OWNER]` hardening list at spec:23 and spec:90 is wider than the owner's ruling. The owner's words at `goal-strategy-task-harness-design-review.md:209` name "the envelope YAML, event ledger, digests, idempotency keys, and reconciliation" as the hardening path. The spec's list adds **"concurrent goal run"** and **"unattended dispatcher."** ADR-003 treats those two differently: at `003-lean-first-persistence.md:34` they are stated as *facts about the system today* ("no concurrent goal runs and no unattended dispatch") that make the threat model small — they are premises of the ruling, not items the ruling gates.

The consequence is not cosmetic. As written, spec:90 implies that a recorded run failure could promote unattended dispatch into the build, which directly contradicts this spec's own Non-Goal at spec:97 ("No goal agent starts another session") and the runbook's flat bar at `GOAL_RUNBOOK.md:48`. Either trim the list to the owner's five, or state separately that dispatch and concurrency are barred outright rather than proof-gated.

**L1-4 · Direct claim (no defect — premise confirmed):** I checked the § "A predicted prose failure" premise against Item 1's artifacts rather than taking it on trust, and **it holds**.

- The only refusal condition anywhere in Item 1 is grounding evidence: "A goal whose § Grounding evidence is empty stays `Status: draft`, and **a draft goal authorizes no task**" (`GOAL_RUNBOOK.md:72`). The template repeats exactly that one condition and nothing else (`goal-templates/goal.md` § Status: "a goal is `draft` until § Grounding evidence is non-empty").
- Nothing in the runbook or the template refuses a goal for a missing answer contract, missing invariants, missing limits, or missing reserved gates. § Grounding a goal's "**Write:**" paragraph (`GOAL_RUNBOOK.md:68`) enumerates all of them as things to write, but writing instructions are not a gate.
- `.claude/skills/run-goal/SKILL.md:37` adds nothing — it routes `ground` straight to the runbook section.
- The spec's secondary observation is also true: there is no stated home for a refusal, because a draft goal has no open round and therefore no `## Round N` heading in `trail.md` to append under.

The handling is right. Measuring per field class rather than narrowing the criterion is what the owner's hardening rule asks for, and spec:50 is explicit that repairing the runbook belongs to Item 1's owner. The spec does not assume the gate works and does not assign itself Item 1 repair work. See L2-2 for the one question this leaves open.

### Lens 2 — Problem & Approach

**L2-1 · Question to the user (must-fix):** **Who enforces the grounding gate in this proof?** The spec never says, and the answer decides whether the gate test proves anything.

The runbook assigns it: "**Who checks it:** the operator" (`GOAL_RUNBOOK.md:72`). In this proof the owner has settled that the orchestrator plays the operator (spec:57, `align.md:36`). That gives three possibilities, and they are not equally good evidence:

1. **The orchestrator-as-operator refuses the draft.** This tests nothing cold. The orchestrator built the epic brief and knows exactly which five field classes are supposed to be checked; a refusal from it is the harness grading its own homework.
2. **The cold grounding session refuses its own draft on its first pass.** Weak for the same reason the runbook's own § What "fresh" means gives: reading your own draft with your own reasoning in front of you is not a review (`GOAL_RUNBOOK.md:43`). It is still worth recording, but it is not the epic's "a deliberately ungrounded draft is rejected before task start."
3. **A separate fresh session is handed a bad draft and asked to start a task under it.** This is the only variant that tests what the epic's criterion says, and it is the one that would surface the four undefended field classes honestly.

The spec parks the choice in Open Questions (spec:105) as a mechanism question. It is not — it determines the validity of Criterion 2 and, together with L1-4, determines whether the per-field-class measurement means anything. Decide it at spec stage.

**L2-2 · Question to the user (should-fix):** `align.md:49` records that **Item 1 is audited and gate-CLEAR but not owner-closed.** The spec's chosen handling of the grounding-gate finding — record it, let the owner act after the evidence is in (spec:50) — is correct under the hardening rule, but it has a cost the spec does not name: Item 1 can be owner-closed *before* this proof runs, with a gate that defends one field class out of five and a known finding sitting in a spec nobody has read at close time. Do you want the L1-4 finding surfaced to you now as an Item 1 open question, or is parking it in this spec's § A predicted prose failure enough? The spec should say which, so a later reader knows the choice was made rather than missed.

**L2-3 · Question to the user (consider):** The spec commits to keeping this as **a real goal in the repository after the item closes** (spec:62, `[INFERRED]`), and to planting a deliberate drift inside it (spec:84). The seed's identity and expected detection are recorded in *this item's* directory — which is coding-PM state that gets archived at close. After archival, `work/orchestration/goals/<slug>/` reads as the repository's first and canonical real goal, containing a round that drifted and a review that caught it, with nothing on the goal side saying the drift was planted.

That is probably fine — a caught drift in an honest round is realistic, and the trail is append-only so it self-documents. But it is a decision, and the spec makes it by inference. Should the goal directory itself carry a disclosure that one drift was seeded for the proof, or does the archived item directory suffice as the record?

**L2-4 · Rewrite request (consider):** The spec names three cold sessions (grounding, resume, review) but never maps them to the round's roles. Somebody has to open the round with a strategy revision, write the `T-001` scope and start line, and — after the resumer appends the return — write the `### Round N result`. ADR-002's one-agent-per-round rule and § What "fresh" means constrain the legal mappings; not every assignment is valid. The spec should either state the session-to-role map or add it to Open Questions as a validity-bearing item, not leave it implicit in spec:66.

### Lens 3 — Pipeline Risk

**L3-1 · Direct claim (must-fix):** **The epic's clean-boundary exclusion has no teeth in the criteria.** The epic bars "treating a clean-boundary handoff as proof of interruption recovery" (`epic:329`). The spec carries it as a `[HARD]` requirement (spec:75) — the interruption must land after the write-ahead start, *after the native side effect has landed*, and before the return. But Criterion 4 (spec:36), which is what an auditor actually checks, is satisfiable without any native side effect having landed:

- "resolves a `### T-00N start` that has no matching return and no stop" — true of an interruption that did nothing.
- "does not repeat the native effect the interrupted task already completed" — vacuously true when there is no completed effect.
- "The completed native artifact is byte-identical before and after the resume session" — vacuously true when no artifact exists.

So a proof that started a task, wrote the start line, and stopped before touching anything native would pass Criterion 4 while being exactly the toothless case the epic excludes. The criterion needs to require positively that a native side effect landed before the stop, and that the kept evidence shows it. The `[HARD]` requirement is a statement of intent; only the criterion is audited.

**L3-2 · Direct claim (must-fix):** **Three criteria assert an ordering with no stated way to check it on disk.** An auditor who did not run the proof has files, not a clock.

- Criterion 2 (spec:34): "the refusal came before the first `### T-001 scope` entry."
- Criterion 4 / requirement (spec:75, and per L3-1): the side effect landed before the interruption.
- Criterion 8 (spec:41): "the seed was planted and its expected detection recorded *before* the review session ran, and the reviewer was not told about it."

Criterion 2's is partly self-evident from append-only trail order, since `trail.md` is never edited in place. The other two are not: a file's mtime proves nothing after a checkout, and content order proves nothing across two files. Commit ordering on `feat/goal-integration-seam` would settle all three, and the branch decision is already owner-settled (spec:59) — but the spec never says commits carry the ordering, and Open Questions does not list it. Either state the auditable ordering predicate in the criteria, or add it to Open Questions as a load-bearing item. Criterion 8's "the reviewer was not told" is the harder half: absence of information is not observable from an artifact, so it can only be established by the kept input record being complete (see L3-5).

**L3-3 · If-then tradeoff (should-fix):** Criterion 4 requires the completed native artifact to be "byte-identical before and after the resume session." Requirement spec:77 nominates the discovery-log disposition row as a legitimate native target. Those two collide **if** the artifact is the file: the round's own obligation is to append joined disposition rows so that no touched row returns as `unrouted` (Criterion 7, `GOAL_RUNBOOK.md:236`), and the resumer is the session most likely to owe one. `DISCOVERY_LOG.md` will not be byte-identical after a correct resume.

If the intended unit is the *row* the interrupted task appended, say row. If the intended unit is the file, then the discovery log is disqualified as the interruption target and spec:77 should say so. As written a design agent can pick either reading and produce a proof that fails audit on the other.

**L3-4 · Rewrite request (should-fix):** Criterion 2 is titled "**The grounding gate holds**, and its real reach is measured," but after the third sentence the criterion no longer requires the gate to hold — it requires the reach to be recorded. The three sentences also read as a requirement, an evidence rule, and a retraction of the requirement, in that order. Rewrite so the title states what is actually being asserted and the criterion states the one thing an auditor checks: that the proof recorded, per field class, whether the shipped gate refused and on what basis. The measurement framing is the right call (L1-4); the wording undercuts it.

**L3-5 · Direct claim (should-fix):** Requirement spec:67 requires the evidence to show "exactly what it was given and exactly what it returned." A record can be exact about everything it contains and still be silent about a context injection, a prior turn, or a hint the operator gave verbally — and that is precisely what freshness claims turn on. The requirement needs to demand that the input record is **complete and closed** — the session's inputs were these and nothing else — not merely accurate about what it lists. This is the requirement Criterion 8's "the reviewer was not told about it" rests on, and it is currently weaker than the claim it has to support.

**L3-6 · Direct claim (consider):** Open Question spec:105 ("whether the refusal comes from the same grounding session on its first pass or from a separate session handed the bad draft") is a spec-stage question, not design's — see L2-1. Everything else in the deferred list is genuinely mechanism, and spec:111's flag that the last three are load-bearing is the right instinct; this one belongs above it.

### Lens 4 — Hygiene

**L4-1 · Direct claim (should-fix):** spec:31 says "**The six criteria below** are the epic's, made concrete." There are **nine**. The epic has six; the spec split discovery-row accounting and five-field judgment replay into their own criteria and expanded the closure criterion. That is a defensible sharpening, but the count sentence makes it invisible — a reader mapping epic-to-spec will silently assume a 1:1 correspondence that does not exist. Fix the count and say plainly that three of the nine are refinements of the epic's four, five, and six.

### Lens 5 — Reader Comprehension

**L5-1 · Rewrite request (consider):** Criterion 2 (spec:34) is the only place the spec is hard to read on one pass, and it is the criterion carrying the most consequential judgment in the item. The reader has to hold three clauses that partly cancel, then jump to a later section to learn why. Lead with the plain point — the shipped gate defends one field class, so this criterion measures reach rather than asserting the gate — and put the forward reference first, not last. Covered mechanically by L3-4; noting it here because comprehension is the sharper cost.

---

## Engagement Summary

**Overall take:** This is a strong spec on the thing it was most likely to get wrong — the grounding-gate premise checks out against Item 1's actual files, and the measure-don't-narrow handling is right. What it gets wrong is smaller and concrete: one closure route it offers does not exist in Item 1's contract, two owner tags are on agent-originated content, and the criteria as written let a weaker proof pass than the epic asked for. Revise, not Rework.

**Here's what I need you to weigh in on:**

1. **[L1-1]** Bounded-negative is not one of the runbook's six close triggers — the epic's wording says it is, the runbook says it closes nothing. Confirm the spec should surface this as an epic/Item-1 conflict and restate the criterion against the runbook's real trigger list, rather than inheriting the epic's slip.
2. **[L2-1]** Decide who refuses the ungrounded draft: the orchestrator-as-operator, the cold grounding session on its own draft, or a separate fresh session handed a bad draft. Only the third tests what the epic's criterion claims. This is a spec-stage call, not design's.
3. **[L3-1, L3-2]** Two criteria are satisfiable by a proof that did less than the epic requires: Criterion 4 passes with no native side effect at all, and three "X happened before Y" claims have no disk-checkable ordering. Confirm the criteria should carry a positive landed-effect requirement and a stated ordering predicate (commits are the obvious candidate, and the branch is already settled).
4. **[L1-2]** Two requirements are tagged `[NEED] [OWNER 2026-08-26]` for your *delegation*, not your decision — the `vol_cold_cryo` question pick and the extra reserved gate are both orchestrator calls you ratified. As tagged they become do-not-relitigate. Confirm they should be regraded agent-side with the ratification noted.
5. **[L1-3]** The `[OWNER]` hardening list adds "concurrent goal run" and "unattended dispatcher" to your five. ADR-003 treats those as barred premises, not proof-gated mechanisms, and this spec's own Non-Goals bars dispatch outright. Trim the list, or split the two out as flat bars.
6. **[L2-2]** Item 1 is gate-CLEAR but not owner-closed. Do you want the grounding-gate finding raised to you now as an Item 1 open question, or is parking it in this spec enough? Either way the spec should record which you chose.
7. **[L2-3]** The proof goal stays in the repository as the first real goal, with a planted drift inside it and the seed record archived in the coding-PM item directory. Should the goal directory itself disclose that the drift was seeded?

---

## Resolutions

All five must-fix and five should-fix incorporated 2026-08-26. Orchestrator dispositions on the seven weigh-in points are recorded inline below.

- **L1-1 — RESOLVED, surfaced not copied.** New § "A close trigger the epic names does not exist": the epic's "legitimate bounded-negative" wording predates Item 1's shipped contract; `GOAL_RUNBOOK.md:84-91` is authoritative `[AGENT]`. The epic's intent maps on — the round's last semantic outcome may be a task-level `BOUNDED_NEGATIVE`, and the round then closes on one of the six; with no committed study, the reachable routes are an unresolved owner gate or a declared limit. Criterion "Bounded closure" and requirement (Closure § first bullet) both restated in the runbook's vocabulary. Flagged to the owner in the orchestrator's run summary rather than settled in the spec.
- **L1-2 — RESOLVED.** Both requirements regraded `[AGENT] (ratified by owner 2026-08-26)` per `align.md`. The question-pick bullet now says only the delegation was the owner's and names the re-derivation route (`align.md:33-35`) as how it is challenged; the reserved-gates bullet says plainly it is an agent default the owner approved and is not settled.
- **L1-3 — RESOLVED.** The `[OWNER]` list trimmed to the owner's five (envelope YAML, event ledger, digests, idempotency keys, reconciliation), cited to `goal-strategy-task-harness-design-review.md:209`. Concurrency and dispatch split out as a separate `[INHERITED: ADR-003:34]` requirement stating they are barred outright, not proof-gated — matching the spec's own Non-Goal and `GOAL_RUNBOOK.md:48`. Same split made in the Problem section.
- **L1-4 — Noted, no action.** Premise independently confirmed by the reviewer; § A predicted prose failure stands, with the enforcer now named (L2-1) so the per-field-class measurement has a subject.
- **L2-1 — RESOLVED, decided in the spec `[AGENT]`.** Variant 3: a separate fresh runbook-following session is handed the ungrounded draft and asked to proceed to a task. The contract holds for a field class only if that session refuses task start and names the missing class unprompted. The orchestrator-as-operator never plays the refusing role; a self-raised refusal from the grounding session is recorded but does not satisfy the criterion.
- **L2-2 — DISPOSED.** The grounding-gate shortfall does not halt on Item 1's close. It reaches the owner in the orchestrator's run summary carrying this item's measured evidence `[AGENT]`. Recorded in § A predicted prose failure so a later reader sees a choice, not an oversight.
- **L2-3 — DISPOSED, yes.** After the fresh review completes, a dated `### Amendment` is appended to the kept `trail.md` disclosing the seeded drift and citing the verification record. Disclosure is post-review only, so it cannot spoil the test. Recorded in Criterion 8 and the seeding requirement.
- **L2-4 — RESOLVED.** The session-to-role map added to Open Questions as a validity-bearing item, naming ADR-002's one-agent-per-round rule and § What "fresh" means as the constraints that make some mappings illegal.
- **L3-1 — RESOLVED.** Criterion 4 now requires positively, on disk and before the resumer starts: the write-ahead entry, the completed observable native artifact, and no return and no stop. States explicitly that an interruption landing no native effect fails the criterion, and that the resumer must not re-produce the effect (artifact hash unchanged, no second-invocation evidence).
- **L3-2 — RESOLVED.** New paragraph under Success Criteria states the ordering predicate for the whole spec: git commit ancestry on `feat/goal-integration-seam`, with the seed record, the write-ahead state, and each cold session's input brief committed before the dependent session runs. Criteria 2, 4, and 8 each carry it. Criterion 8's harder half — that the reviewer was not told — is routed to the complete-and-closed input record (L3-5).
- **L3-3 — RESOLVED.** "Byte-identical" scoped to the artifact the interrupted task produced, never a whole file; the criterion says the discovery log legitimately gains joined rows during a correct resume, and the requirement names the row as the unit where the row is the target.
- **L3-4 / L5-1 — RESOLVED.** Criterion 2 retitled "The grounding gate's reach is measured, per field class" and rewritten to lead with the plain point and the forward reference, then state the one thing an auditor checks. The requirement-then-retraction sequence is gone.
- **L3-5 — RESOLVED.** The freshness requirement now demands a complete and closed record: every session enumerated with its full kept input and return, plus a statement that no other input existed — no context injection, no prior turn, no verbal hint.
- **L3-6 — RESOLVED.** The refusal-enforcer question removed from Open Questions (settled in Criterion 2); what the bad draft contains and who authors it stays as genuine design work.
- **L4-1 — RESOLVED.** Count corrected to nine, with the three refinements named and mapped back to the epic's criteria.

---

**Verdict:** Revise
**Next Steps:** Record resolutions above, then return to the spec-agent session and point it at this review to incorporate. The reviewer does not edit the spec. Must-fix before design: L1-1, L1-2, L2-1, L3-1, L3-2.
