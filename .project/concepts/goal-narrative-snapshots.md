# Concept: Goal Narrative Snapshots

**Created:** 2026-09-04
**Status:** Draft

---

## Problem Statement

The goal layer is an authoritative operating record. Its three files answer what the goal is, what happened, and what the run learned. They deliberately cite native evidence instead of retelling it, and their stable or append-only behavior lets a fresh operator reconstruct the run.

Humans also need a readable engineering story that brings the question, model changes, study results, limits, and possible visuals together. Putting that story in a goal directory makes it look like part of the goal contract even though it has different authority and mutability. It also forces exceptions into the goal layer's three-file, cite-don't-restate pattern.

A single living summary creates a second problem: it becomes stale as the goal advances. During concept shaping, the wall-and-heating draft said that T-004 had not returned and no checkpoint existed, while the trail had already recorded two checkpoint submissions, a passing verdict, T-004 complete, and T-005 started; the trail advanced again while this concept was being reviewed. The useful artifact is therefore not a current-state file. It is a dated account of what the evidence supported at one milestone (`work/narratives/20260904-184254Z-wall-and-heating.md`; `work/orchestration/goals/wall-and-heating/trail.md`).

## Owner's Words

- **[OWNER-VERBATIM]** "I would like to codify the `narrative.md` pattern as OPTIONAL but also not hidden."
- **[OWNER-VERBATIM]** "what if this was kept separate? e.g. a folder outside of orchestration -- `work/narratives/{slug}.md` or something? Then the concept could be: separate skill for summarizing results for humans, invoked asynchronously." **Force:** `work/narratives/` is the proposed home; separation from orchestration and a separate skill are the requirement.
- **[OWNER-VERBATIM]** "have it be {datetime-stamp}-{slug}.md so it is easy to see the chronology"
- **[OWNER-VERBATIM]** "this also means we can rerun the narrative multiple times, e.g. after round 1 and then again after round 2" **[EXAMPLE]** Round 1 and round 2 illustrate milestone snapshots; they do not limit when a narrative may be created.

## Success Criteria

When this work is complete:

1. **[INHERITED: `.project/adr/0003-lean-first-persistence.md`; `.claude/skills/run-goal/SKILL.md`] The goal contract stays unchanged** — `work/orchestration/goals/<slug>/` retains its three authoritative contract files, and neither `/run-goal` nor `GOAL_RUNBOOK.md` gains a narrative lifecycle or presentation role.
2. **[OWNER] A narrative is optional and discoverable** — a user can explicitly invoke a separate, user-invocable goal-narrative skill with narrative-specific triggers, while no goal stage, gate, review, close, or resume requires a narrative to exist.
3. **[OWNER] Each normal invocation creates one chronological snapshot** — the output filename contains a sortable datetime stamp and the canonical goal slug, and a later normal invocation for the same goal creates a second file rather than replacing the first.
4. **[AGENT] Every snapshot declares its source condition** — the header retains the worked examples' `Goal status`, `Narrative cutoff`, and `Review status`; relevant dirty inputs make the cutoff visibly provisional, and mixed source-review states remain visible rather than being flattened.
5. **[AGENT] Every snapshot declares a coherent basis** — the narrator starts from the three goal files at one repository cutoff and follows only their cited native records at that cutoff. Earlier narratives and orientation summaries are never evidence inputs.
6. **[AGENT] Authority remains one-way** — consistent with `.project/adr/0006-goal-evidence-seam.md`, a narrative may summarize and cite goal and native records, but it is never evidence, state, authorization, a review verdict, or an authoritative input cited by those records.
7. **[AGENT] The narrator has one write boundary** — each invocation creates one new snapshot and does not mutate the goal directory, native evidence, work-item state, study records, discovery log, or an earlier narrative.
8. **[OWNER] Repeated narratives remain intelligible as history** — a reader can compare, for example, the post-round-1 and post-round-2 accounts without mistaking the older account for an incomplete current-state document.
9. **[AGENT] Unsupported claims remain visible** — every narrative distinguishes recorded facts from narrator interpretation and states what the cited sources do not support.

---

## Why This Shape

- **[OWNER] Key bet:** A goal narrative is a derived presentation snapshot, not a fourth goal artifact.
- **[AGENT] Why this shape is promising:** Physical separation preserves the goal layer's authority and mutability rules. Timestamped outputs turn expected staleness into visible chronology and allow the engineering story to improve after each milestone without overwriting prior context.
- **[INHERITED: `.project/product/0001-goal-round-native-operability.md`] Constraint to preserve downstream:** Goal operation must remain possible from `goal.md`, `trail.md`, `learnings.md`, the shared runbook, and native records alone. No authoritative workflow may depend on a narrative.

---

## User Stories

### Goal operator

**US-1: Capture the story at a useful milestone**
**[AGENT]** As a goal operator, I can ask for a human-readable narrative after a reviewed round or during an open one, so that I have a coherent account without editing the goal's operating record.

**US-2: Capture later understanding separately**
**[OWNER]** As a goal operator, I can run the narrator again after another round, so that the new account sits beside the old one and their order is obvious from their names.

### Human reader

**US-3: Know what an account represents**
**[AGENT]** As a reader, I can see the goal status, evidence cutoff, and review state of the summarized records at the top, including whether dirty source content made the cutoff provisional, so that I do not mistake the account for current authoritative state.

**US-4: Follow claims back to evidence**
**[AGENT]** As a reader, I can follow quantitative and decision-bearing claims to authoritative goal or native records, so that the plain-language account remains auditable.

### Explainer author

**US-5: Find the visual story**
**[AGENT]** As an explainer author, I can use the narrative's story arc and visual index to plan a human-facing artifact, while tracing published claims to the underlying authoritative sources.

---

## Key Concepts

### 1. Narrative snapshot

**[OWNER]** A narrative is a human-facing account of one goal at one evidence cutoff. Goal progress never updates an old snapshot. A later milestone produces another timestamped file.

**[AGENT]** Every narrator invocation creates a new snapshot. A later milestone never updates an earlier one; an ordinary targeted edit may still correct a Markdown error without becoming a narrator mode or lifecycle.

### 2. Separate narrator role

**[AGENT]** The narrator is a presentation role, not an operator, round agent, administrator, or fresh reviewer. It does not satisfy a goal gate and does not certify the evidence. Its only product is the narrative snapshot.

### 3. Out-of-band invocation

**[AGENT] (ratified by owner, 2026-09-04)** The narrative skill is invoked independently of `/run-goal`; the goal workflow never dispatches it automatically. “Asynchronously” means optional and out of the goal's critical path. A genuinely concurrent run needs a fixed evidence cutoff so it cannot combine two changing states.

### 4. Chronology and evidence cutoff

**[OWNER]** The filename timestamp says when the account was generated; the header separately says which repository state it read.

**[AGENT] (ratified by owner, 2026-09-04)** Start from the lexically sortable `YYYYMMDD-HHMMSS-<goal-slug>.md` shape. The spec must settle one timezone and same-second collision behavior without permitting overwrite.

### 5. One-way provenance

**[AGENT]** Narratives may restate cited evidence because they live outside the authority layer. A downstream explainer may use the narrative as a story map, but not as the evidence for its claims.

**[INHERITED: capture-fidelity laws]** Narratives preserve the source's force: owner decisions remain owner decisions, each source's actual review stage is named, provisional readings remain provisional, and narrator synthesis is labeled as synthesis. The worked-example `Review status` describes the authoritative records summarized; mixed review states are enumerated there or named beside affected claims, and the narrator does not imply a separate certification of its own prose.

### 6. One authoring contract

**[AGENT]** The narrative skill is the complete authoring contract and the sole procedural home. If the output directory has a README for human discovery, it states only what the directory contains and points to the skill; it does not copy the procedure.

---

## Scope of Behavior Changes

### New artifacts to create

- **[AGENT] (ratified by owner, 2026-09-04)** `work/narratives/` as the sibling home for timestamped goal narratives outside `work/orchestration/`.
- **[OWNER]** A user-invocable Claude skill dedicated to producing goal narratives; the skill owns the full authoring contract.
- **[AGENT]** An optional pointer-only directory README if discovery outside Claude's skill routing needs it.
- **[AGENT]** Timestamped replacements for the three current narrative drafts.

### Existing artifacts to modify

- **[INHERITED: goal-layer three-file contract]** Remove the uncommitted narrative surface from `GOAL_RUNBOOK.md`; the goal operating contract does not own this feature.
- **[AGENT]** Remove narrative files from goal directories and repair their links when placing them in the separate home.
- **[AGENT]** Update live orientation text that points to the deleted `wall-and-heating/SUMMARY.md` or says that no prose home exists.
- **[AGENT]** Add lightweight checks that preserve the separation, keep `/run-goal`'s modes and directory contract unchanged, give the narrator specific discovery triggers, and validate the narrative contract without requiring any goal to have a narrative.

### Behavior changes by workflow stage

- **[INHERITED: goal-layer contract] Goal work:** No change. Goal rounds neither create nor refresh narratives.
- **[OWNER] Narrative invocation:** The user invokes the separate skill with a goal slug or goal path at a useful milestone.
- **[AGENT] Narrative production:** The narrator reads the three goal files at one declared repository cutoff, follows their cited native records at that cutoff, and creates one new timestamped snapshot. It does not use prior narratives or orientation summaries as evidence.
- **[OWNER] Later milestone:** Another invocation creates another file. Earlier snapshots remain as dated accounts.
- **[AGENT] Downstream presentation:** Visual or HTML work may use the narrative to find the story and source material, while retaining direct evidence citations.

---

## Non-Goals / Out of Scope

- **[OWNER]** The narrative is not part of the goal orchestration contract; separation exists to preserve that boundary.
- **[OWNER]** A narrative is not required for every goal or every round; it is produced when a human summary is useful.
- **[AGENT]** Automatic post-round dispatch is out of scope because optional invocation is the simpler boundary and unattended dispatch remains outside the current goal architecture.
- **[AGENT]** A mutable `latest.md`, current pointer, or narrative index is not required; sortable filenames provide chronology without another state surface.
- **[AGENT]** The narrator does not perform a fresh review, accept learnings, change dispositions, or close a goal.
- **[AGENT]** HTML generation and publication are separate presentation work; this concept produces Markdown source material only.
- **[AGENT]** Historical completed concepts, designs, audits, and product promises are not rewritten to mention an optional presentation feature.

---

## Assumptions & Prerequisites

- **[AGENT]** Goal slugs are stable and unique enough to identify the source goal from each filename.
- **[AGENT]** The initial narratives are internal working artifacts. Material intended for publication moves through the existing explainer workflow.
- **[AGENT]** A goal and its cited evidence can be read at a coherent repository cutoff when a snapshot is produced.

## Resolved Questions

Resolved during specification on 2026-09-04. The decisions and their provenance are recorded in `.project/active/goal-narrative-snapshots/spec.md` § Resolved Decisions; no technical design question remains.

---

## Next-Stage Handoff

**Settled here:**

- **[OWNER]** Human-facing goal narratives live outside the goal orchestration directory and are produced through a separate skill.
- **[OWNER]** Narratives are optional but discoverable.
- **[OWNER]** Each narrative filename carries a datetime stamp and goal slug so chronology is visible.
- **[OWNER]** The narrator may run multiple times for one goal, producing separate milestone accounts rather than replacing the earlier narrative.

**Resolved in spec:**

- **[OWNER]** Dirty source content is allowed and makes the narrative cutoff visibly provisional.
- **[INFERRED]** The remaining naming, citation, metadata, migration, and enforcement choices are specified in `.project/active/goal-narrative-snapshots/spec.md`; no design artifact is required before implementation.

**Decomposition guidance:**

- **[AGENT]** One small coding/documentation work item should be sufficient: the canonical narrator skill, draft migration, live-reference cleanup, and focused consistency tests.
