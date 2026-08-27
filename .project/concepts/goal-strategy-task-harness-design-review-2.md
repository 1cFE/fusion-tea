# Design Review 2: Goal Strategy and Task Harness (revised)

**Design:** `.project/concepts/goal-strategy-task-harness-design.md` (rev. 2026-08-23 18:49, "revised after independent review")
**Spec-equivalents:** `.project/concepts/goal-driven-model-development-harness.md` (input concept) + the owner rulings recorded in `.project/concepts/goal-strategy-task-harness-design-review.md` § Resolutions
**Review File:** `.project/concepts/goal-strategy-task-harness-design-review-2.md`
**Product-lens ledger:** `.project/concepts/goal-strategy-task-harness-design-product-lens.md`
**Date:** 2026-08-23

This is the second review round. Review 1 (verdict Revise) and its owner resolutions are the baseline; this round checks the revision fresh, with a new product-lens run and a new ponytail challenge. Review 1's file is untouched — it remains the authority for the 2026-08-23 rulings.

---

## The Point

The goal layer must let a non-builder operator ground a question against the model base and run the study → reading → disposition → model-change loop with criticism, disk-resume, and replayable judgment — while three owner-grade constraints of 2026-08-23 hold: (1) criterion 4 of `study-driven-model-development.md` stands — every round dispositions the open `DISCOVERY_LOG.md` rows its evidence touches, joined `<study-id>#<n>`, with the goal agent appending disposition rows and the runbook's sole-writer rule amended; (2) lean first, harden on evidence — first build is goal file + brief-pattern prose trail + fresh-round discipline + the log join, with envelopes/ledger/digests/idempotency/reconciliation as a hardening path promoted only on observed failure; (3) the goal evidence seam — goal inputs may cite `.project/` by path and digest, each PM mutated only natively, CLAUDE.md's contrary wording named as the surface an ADR amends.

## Fundamental Assessment

**Sound.** The revision faithfully incorporates every recorded ruling, and both independent checks confirm it:

- **Product-lens: gate DISPOSED.** All three owner-grade constraints hold in the text; the previously blocking silent drop is gone; neither design smell (consumer-compensation; unstated ownership change) fires — the prior version's goal-side effects ledger, which did fire smell 2, is gone from the first build, and every ownership move (log writer split, evidence seam, brief-pattern succession) is declared with its authority. Three lower-authority findings, all dispositioned (carried below as MA3, mi1, mi3).
- **Ponytail (ultra): CHALLENGE — narrow.** Verbatim: "The skeleton is right, honors every recorded ruling, and should proceed after trims; nothing here needs an owner ruling reopened." Its one most important reason: the trail's *record grain* quietly rebuilds, as bookkeeping, the per-stage ceremony the granularity ruling deleted as authorization — a 5+5-line Invoke/Return block at every native stop point plus an 11-field task section is "an envelope in prose clothing" (~30 structured blocks for the design's own example round, where the WI-029 brief carried an equivalent run in six dated entries and native registries already record stage position).

This is the right piece of work: it is exactly the revision the rulings directed, and the remaining issues are trims and honesty sentences, not shape errors. No owner decision needs reopening.

## Ponytail Challenge (round 2)

*Fresh subagent, ponytail role per `~/.claude/commands/_my_ponytail.md`, ultra intensity. Returned verbatim:*

---

**Posture:** ULTRA, adapted to design review. Evidence base read before the mechanism: the Item 6 research doc, the 22-row discovery log, the WI-029 brief, the run-study skill/runbook, both parent concepts, the prior review's Resolutions. Owner-settled rulings (lean-first; criterion-4 join; evidence seam) are respected — nothing below asks to relitigate them, and I found no new evidence that would.

**First, credit where it is earned.** This revision is a real shrink, not a cosmetic one. The control plane is gone to a hardening table with promote-conditions, the task is a bounded objective per the granularity ruling, the discovery-log join is restored exactly as ruled (goal agent appends disposition rows, joined by `<study-id>#<n>`, one runbook sentence), the goal directory explicitly *succeeds* the flat brief (review m3, fixed), the cite-don't-restate invariant is now stated (M2, fixed), and the rulings are carried with provenance citing the review's Resolutions (M3, fixed). The skeleton satisfies the rulings.

**1. Does the remaining machinery need to exist?**

Most of it, at the grain of one entry per goal-relevant event. Not all of it at the grain written.

- **The invocation/return block "at every native stop point" — the biggest remaining fat.** The design (§ Invocation and return) requires a 5-line `Invoke` + 5-line `Return` block per native boundary. A task that advances one work item `open → audit` (which § Strategy and task explicitly allows) writes ~6–7 pairs; a realistic round (`model → research → model → integrate → study.execute → study.read`, the design's own example) writes ~30 structured blocks. The proven referent carried an entire seven-stage item — two owner gates, a mid-run pin drift, a hard halt, resume across sessions — in about six dated stage-log entries (`work/orchestration/handshake-lcoe-construction.md` § Stage log). And the native side already records stage position: the modeling dashboard infers stage from which artifact files exist (CLAUDE.md, stage detection), the study record is its own ledger, `pm` ops write the registries. A per-stage return block restates what native artifacts carry — brushing against the design's own "never mirror or restate" invariant. What validation slice 2 (fresh pickup from an unreturned invocation) actually needs is only the **write-ahead rule**: append intent before invoking, then trust filesystem facts. Keep write-ahead and the return **vocabulary**; log at task grain plus genuine stop events; let observed friction promote denser logging — the design's own hardening philosophy, applied to its own trail.
- **The 11-field task template** (Objective … Scope check). The prior review's P2 row put the target at ~6 lines of prose; the WI-031 request table did the same authority work in 4 columns. Cut: `Allowed native stages` (double-encodes `Scope`, and degenerates once "a task may traverse several seams" — see §5), `Prerequisite` as a field (predicting prerequisites is forward-planning residue; the `PREREQUISITE` return suffices), `Comparison invariants` (already in `goal.md`'s contract — cite, don't repeat), and collapse `Positive result` / `Bounded negative` / `Stops` into done-when / stop-when.
- **RetryCheck** — keep. It is exactly the ruled shape (P4: mechanical check plus one logged judgment), one entry, no review type.
- **Seam-vocabulary table** — keep as documentation; five seams matching the native surfaces is right (study split execute/read mirrors the skill's two modes). One honesty fix: two of five rows (`research`, `integrate`) name native returns that **do not exist yet** — the design says so two paragraphs later. Mark those rows as pending their native repairs, and say which validation slices they block (3 and 5).
- **RoundIntent** — one line of the strategy revision, not a node. The semantic model says roles-not-files, so this costs nothing to collapse; naming it as a tree node invites someone to build it a section.

**2. What can be deleted instead of accommodated?**

- **The two-patterns question is resolved, correctly:** "For goal-driven runs this directory succeeds the flat `work/orchestration/*.md` brief pattern; it does not coexist" (§ First-Build Persistence). Clean.
- **The runbook is amended, not accommodated — but the amendment has two homes and the design names one.** The sole-writer rule lives in runbook step 14 *and* in `DISCOVERY_LOG.md`'s own header ("Only a study's executor appends rows"). The one-sentence amendment must land in both, or the header must cite the runbook as authority. Concrete, five-minute miss.
- **A quiet good deletion worth naming:** the input concept's planned runbook change ("review lenses written by a critic session, not the executor," `goal-driven-model-development-harness.md` § Existing artifacts to modify) is dropped — native reviews stay native. Right call under lean-first, but the design should say it dropped it, one line, so the divergence from the input concept isn't silent.
- **`learnings.md` as a third file** is defensible (cross-round memory read without scanning the trail) but was an `[AGENT]` choice — the P2 ruling named "goal file + trail"; the C1 ruling named the LearningLog *mechanism*, not a file. Fine to keep; know it's yours.

**3. Invariants at their real owners?**

Yes, with one gap. Research acquisition/registration and integrate (regenerate → verify → pin) are correctly named "prerequisite repairs at their native owners, not harness logic" — the research doc's own verdict (`20260822-120756`, Feasibility 1–3). The one-sentence runbook amendment is the minimal repair at the right owner. Cite-don't-restate is now an invariant. **The gap:** the design never says where the two native repairs are *tracked*. They gate validation slices 3 and 5; untracked, they become the harness's hidden first tasks and the first round silently absorbs them. Name their tracking home (backlog items) or state that the first slices run with the WI-031 hand pattern at those seams.

**4. Which abstraction or field can still be removed, and what breaks?**

| Cut | What breaks |
|---|---|
| Per-stop-point Invoke/Return blocks → task-grain + stop events, write-ahead kept | Nothing — validation slice 2 survives on write-ahead + native facts; WI-029 is the existence proof |
| `Allowed native stages` field | Nothing — scope + seam vocabulary already bound it |
| `Prerequisite` field (keep the return) | Nothing — the return classifies the event when it happens |
| `Comparison invariants` per task → cite `goal.md` | Nothing — one source of truth instead of a drift pair |
| `RoundIntent` node → one strategy line | Nothing |
| Scope-check enum's `REVISE` (self-issued) | Nothing — see below; only `OWNER_GATE` has teeth |

What survives because it earns its place: write-ahead invocation, the six-value return vocabulary, the round caps, the disposition join, `learnings.md` acceptance flow, the fresh round review, the hardening table.

**5. Is this the smallest design satisfying the rulings? New problems?**

Close. The shape is the ruled shape. Two introduced problems to fix in prose:

- **Multi-seam tasks soften the scope check to a narrative.** "A task may traverse several seams when they serve one bounded objective" plus a self-issued `ACCEPTED` means nothing *prevents* a mega-task ("answer the round intent") that swallows the round. The real preventive bounds are elsewhere and are good: at most one pin, one committed study, a valid study reading closes the round, owner gates. The design should say plainly that in the first build task-level authority is **retrospective** — enforced by the fresh round review checking recorded scopes — and only `OWNER_GATE` in the scope check is preventive. As written, the Essence's "the goal layer decides why work is justified" over-claims what a self-checked prose section enforces.
- **`PREREQUISITE` is semantically clean as a return** — "blocked on an identified missing input, strategy and meaning intact" is a real, distinct outcome, and forcing re-authorization of the resumed objective is the design's point, not a wart. It is *not* clean as a template field: the field predicts, the return records; delete the field.

**6. Verdict**

**CHALLENGE — narrow.** The skeleton is right, honors every recorded ruling, and should proceed after trims; nothing here needs an owner ruling reopened.

**The one most important reason:** the trail's record grain quietly rebuilds, as bookkeeping, the per-stage ceremony the owner's granularity ruling deleted as authorization — a 5+5-line Invoke/Return block at every native stop point plus an 11-field task section is an envelope in prose clothing, ~30 structured blocks for the design's own example round, where the proven referent (`handshake-lcoe-construction.md`) carried an equivalent run in six dated entries and the native registries already record stage position. Keep the write-ahead rule and the return vocabulary; log at task grain and stop events; shrink the task section to ~6 lines; and let the design's own hardening rule — promote structure only when a run shows prose failing — govern its logging the way it already governs its ledger.

---

### Ponytail Disposition

- **Trail grain (per-stop Invoke/Return + 11-field template = envelope in prose clothing): ACCEPTED** → MA1. The evidence (WI-029's six entries; native registries already recording stage position; the design's own cite-don't-restate invariant) is decisive. Keep write-ahead + the return vocabulary; log at task grain plus genuine stop events; task section ~6 lines. One nuance kept for the author: a task may still *narrow* the goal's comparison invariants for its scope — cite `goal.md` and state only the narrowing, rather than deleting the concept.
- **Scope check is retrospective; Essence over-claims: ACCEPTED** → MA2. Matches this review's own Stage-0 candidate finding.
- **Native repairs untracked: ACCEPTED** → MA4.
- **Seam rows pending-repair labels; RoundIntent collapse; PREREQUISITE field deletion; REVISE enum; runbook amendment second home; dropped-lens-change divergence note: ACCEPTED** → mi2, mi5, mi4, mi8, mi1, mi6.
- **`learnings.md` as a third file: no change required** — recorded as an `[AGENT]`-owned choice the author keeps knowingly; consistent with the C1 mechanism ruling.
- **RetryCheck, seam table, hardening table, fresh round review: CLEAR** — no findings.

---

## Dimensional Review

### 1. Spec Compliance — **Pass with concerns**
Every recorded ruling is incorporated faithfully (verified independently and by the product-lens oracle; see Fundamental Assessment). Provenance is carried well — the rulings table grades each row honestly, quotes the owner where given, and cites Review 1's Resolutions as authority. Two inherited obligations are handled incompletely: the input concept's criterion 6 replay-entry discipline (five fields: finding, decision + reason, tier, who decided, what changed) is neither present in the trail's entries nor explicitly deferred (MA3, lens F1); the "one end-to-end operator document" scope item has no named deliverable, though the invoke/return pattern likely *is* it in substance (mi3, lens F2).

### 2. Pattern Consistency — **Concerns**
The design claims the proven brief pattern ("following the proven orchestration-brief pattern") but specifies a record grain far denser than that pattern's referent — per-stop-point structured blocks vs WI-029's ~six dated stage-log entries (MA1). Everything else aligns: run home, Align-ruling style, native command surfaces, discovery-log conventions.

### 3. Abstraction Quality — **Pass** (with trims)
Goal / strategy / task / round / review earn their places; the Mental Model section states them plainly and the tasks-vs-findings axis distinction ("a task controls authority; a finding controls traceability") is exactly the clarification round 1 demanded. Trims: `RoundIntent` as a tree node (mi5), the `Prerequisite` template field (mi4), `Allowed native stages` (folded in MA1).

### 4. Duplication Avoidance — **Concerns**
The cite-don't-restate invariant is stated, but two specified structures work against it: per-stop return blocks restating what native artifacts already record (MA1), and `Comparison invariants` repeated per task when `goal.md` owns them (fold into MA1's trim; cite-and-narrow instead). The goal directory superseding the flat brief resolves round 1's coexistence concern cleanly.

### 5. Data Structure Clarity — **Pass**
The return vocabulary (`COMPLETE | BOUNDED_NEGATIVE | PREREQUISITE | STRATEGY_BLOCKER | OWNER_GATE | MECHANICAL_FAILURE`) is well-defined, and deriving the round stop reason from the last result plus limits removes round 1's double-enum concern. One sentence distinguishing `PREREQUISITE` as an invocation return that becomes the task's ending outcome would spare a cold reader (mi4).

### 6. Route Safety (seams and returns) — **Pass with concerns**
Crash semantics are clean: write-ahead invoke entries, native facts as truth for an unreturned invocation, no unattended-dispatch parity claim. Concerns: two of five seam rows (`research`, `integrate`) name native returns that do not exist yet and should be labeled pending with the validation slices they block (mi2); nothing forbids a native work item a round holds from advancing outside any goal task (mi7); the self-issued `REVISE` scope-check value has no teeth (mi8).

### 7. Bets & Decisions Integrity — **Pass with concerns**
The rulings table is the strongest provenance record in this line — each row graded, owner quotes carried, `[AGENT]` inferences marked overridable. One hidden bet surfaced: *prose at per-stage grain stays maintainable across a real round* — contradicted by the design's own hardening philosophy and by the WI-029 referent (MA1). One decision made silently: dropping the input concept's planned runbook change (critic-written review lenses) — right call under lean-first, but say it (mi6). `learnings.md` as a third file is an `[AGENT]` choice kept knowingly (noted, no change).

### 8. Reader Comprehension — **Pass**
Essence → Problems → Mental Model → mechanism is the right order, and the worked example in Round Semantics does what round 1 asked. One over-claim to soften: "the goal layer decides why work is justified" — in the first build that authority is retrospective (fresh round review over recorded scopes), and only `OWNER_GATE` is preventive; one honest sentence (MA2).

---

## Issues by Severity

### Critical
- None.

### Major
- **MA1 — Trail record grain rebuilds per-stage ceremony as bookkeeping** (Pattern Consistency / Duplication / ponytail). Per-stop-point 5+5-line Invoke/Return blocks plus an 11-field task section ≈ an envelope in prose clothing (~30 structured blocks for the design's own example round vs WI-029's six entries). Fix: keep the write-ahead rule and the six-value return vocabulary; log at task grain plus genuine stop events; shrink the task section to ~6 lines (done-when / stop-when collapse; cite-and-narrow `goal.md`'s comparison invariants; drop `Allowed native stages`); let the hardening rule govern logging density.
- **MA2 — First-build task authority is retrospective; the design implies it is preventive** (Comprehension / ponytail / this review's Stage 0). State plainly: the scope check is a self-recorded authorization test; enforcement is the fresh round review over recorded scopes plus the round's hard bounds (one pin, one study, reading closes the round, owner gates); only `OWNER_GATE` is preventive.
- **MA3 — Replay-entry discipline dropped without saying so** (Spec Compliance / lens F1). Input-concept criterion 6's five fields (finding, decision + reason, tier, who decided, what changed) are absent from the trail's entries and not explicitly deferred. Fix: add tier and who-decided to the trail's decision/return entries (cheap prose), or record criterion 6 as explicitly deferred to hardening, owner-visible.
- **MA4 — The two native repairs have no named tracking home** (ponytail §3). Research acquisition/registration and integrate gate validation slices 3 and 5; untracked, the first round silently absorbs them. Fix: name backlog items, or state that the first slices run the WI-031 hand pattern at those seams.

### Minor
- **mi1 — The sole-writer amendment has three textual homes**, and the design names one: runbook step 14 (`runbook.md:221`), the administer section's "An administrator does not append" (`runbook.md:270` — the goal agent's disposition append must be distinguished from the administrator role), and `DISCOVERY_LOG.md`'s own header ("Only a study's executor appends rows"). (lens F3 + ponytail)
- **mi2 — Label the `research` and `integrate` seam rows pending their native repairs**, naming the validation slices they block (3 and 5).
- **mi3 — Name the operator-document deliverable** — the design + trail pattern may *be* it; say so. (lens F2)
- **mi4 — `PREREQUISITE`: delete the predictive template field, keep the return**; one sentence distinguishing return from task-ending outcome.
- **mi5 — Collapse `RoundIntent` to one line of the strategy revision**, not a tree node.
- **mi6 — Note the dropped input-concept runbook change** (critic-written review lenses) as a one-line decision record.
- **mi7 — Name the dangerous combination**: a native work item a round holds (via task inputs) advanced outside any goal task — one invariant line or an accepted-risk note.
- **mi8 — The self-issued `REVISE` scope-check value has no teeth** — cut it or say what it obliges.

---

## Recommendations

1. Apply the MA1 trail-grain trim — it is the design's own hardening philosophy applied to its own logging, and every other finding shrinks with it.
2. Add the MA2 honesty sentence on retrospective authority.
3. Resolve MA3 (five fields or explicit deferral) and MA4 (name the repair tracking home).
4. Sweep the minors — all are one-line or one-label fixes; mi1's three-site list matters most for the C1 ruling's implementation.

---

## Resolutions

All findings incorporated by the author in the 2026-08-23 revision (245 lines); each verified against the revised text by the reviewing session:

- **MA1 (trail grain) — incorporated.** Logging is task-grain: one `WriteAheadStart` before the first native side effect, `StopEvent`s only for genuine stops, one task return; new design principle "Log judgment, not routine stage motion"; the task section is six lines (Objective / Why now / Scope / Inputs / Done when / Stop when); `Allowed native stages`, the `Prerequisite` field, and per-task `Comparison invariants` are gone (Inputs "cite `goal.md` and state only any narrower constraint" — the cite-and-narrow nuance kept); denser per-stage trail events moved into the hardening table with a promote-condition.
- **MA2 (retrospective authority) — incorporated.** Stated in the Overview ("task scope is auditable rather than mechanically enforced; owner gates stop work preventively; all other bounds checked retrospectively"), in § Task ("a reviewable record, not a technical sandbox"), and in § Failure Modes and System Confidence.
- **MA3 (five replay fields) — incorporated.** The task return's Decision line carries finding/trigger, decision + reason, tier (`execution detail | reserved gate | premise surprise`), decided by, and what changed (resolving to paths/ids/commits or `none`); backed by a new Required Invariant.
- **MA4 (repair tracking) — incorporated.** The design states no backlog items track the two seam repairs, requires the epic to create named prerequisite items for both, and pins the interim: slice 3 uses the WI-031 hand pattern, slice 5 the current manual integration pattern; "a goal round may not silently absorb either repair."
- **mi1 — incorporated.** All three writer-amendment homes named: runbook step 14, the administrator prohibition, the discovery-log header; administrator still never writes.
- **mi2 — incorporated.** `research` and `integrate` seam rows marked "(pending native repair; blocks slice 3/5)".
- **mi3 — incorporated.** Operator deliverable named: `work/orchestration/GOAL_RUNBOOK.md`, shared, not per-goal.
- **mi4 — incorporated.** `PREREQUISITE` is "discovered as a return, not predicted in task scope"; the predictive field is deleted.
- **mi5 — incorporated.** `RoundIntent` collapsed into `StrategyRevision` (intended model increment + intended study question).
- **mi6 — incorporated.** The dropped input-concept runbook change (critic-authored review lenses) is recorded as an `[AGENT]` lean-first divergence in § Review Pattern.
- **mi7 — incorporated.** New invariant: a referenced native work item changed outside an active goal task voids the task's authority; re-ground or close the round.
- **mi8 — incorporated.** The self-issued scope-check enum is gone; an unresolved owner gate prevents execution, and scope is a recorded section audited by the fresh round review.
- **Provenance note — incorporated.** The Lean-first ADR row now splits the `[OWNER]` ruling from the `[AGENT]`-owned separate `learnings.md` mechanism; the ADR table rows also gained affected seams and rejected alternatives (meeting the density bar).

Review 1, this review, and the product-lens ledger were left untouched by the author, as required.

---

**Overall:** **Approve** *(updated 2026-08-23 after verified incorporation of all Review 2 findings; originally Revise — narrow)*. No critical findings ever; no owner ruling reopened; no smell fired; the accepted ponytail challenge is incorporated. Ready for final owner acceptance.
**Next Steps:** Owner acceptance of the design, then ADR filing per Review 1's candidate assessment (Strategy and task; Round boundary; Lean-first persistence; Finding disposition; Review topology; Goal evidence seam — naming CLAUDE.md as an amended surface; Supersession as split). Then `/_my_epic_plan` for the build slices — the design already names what the epic must own (two native seam repairs, `GOAL_RUNBOOK.md`, non-builder resume proof, manual/native seam equivalence, fresh-review comparison proof).
