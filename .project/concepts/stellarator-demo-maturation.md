# Concept: Stellarator Demo Maturation — Depth Rubric and Goal-Driven Refinement

**Created:** 2026-08-30
**Status:** Draft

---

## Problem Statement

The stellarator demo's next milestone is criterion 4, the ARIES-CS hold-out comparison (Anchor B). The comparison machinery is ready: the reference is sealed (`knowledge/holdout/aries-cs/PROTOCOL.md`), the per-axis pass/fail bands were ratified pre-reveal on 2026-07-19 (`.project/completed/20260821_demo-anchor-acceptance-spec/spec.md`), and epic Item 7 defines the reveal-and-compare procedure. But the owner is not convinced the model is worth comparing yet, and the repo supports the doubt: the plant model is a parametric calc network on a one-deep part tree (14 leaf subsystems, none decomposing further), cost accounts stop at CAS 2-digit granularity, confinement/τ_E is explicitly out of scope so nothing pushes back on the operating point, and TBR is a cited constant rather than a computed quantity. Load-bearing values were demonstrably wrong weeks before this concept (`p_pump` ~100× low until WI-033, 2026-08-28).

Running the blind comparison now would spend the demo's one irreversible piece of evidence on a model state nobody believes in. But the alternative — "improve the model first" — has no defined target: the concept's stage 3 (agentic research and model development) is least-specified by design and has never run as its stage-3⇄4 interleave intended. "Get closer to ARIES-level quality" is not an actionable goal while ARIES-CS itself is sealed and must stay sealed.

This concept defines the maturation phase: make "ARIES-level quality" operational without unsealing anything, direct model development at the measured gaps, and turn "ready for Item 7" into a defined condition instead of a feeling.

## Owner's Words

From the 2026-08-29 session (carried via handoff):

- **[OWNER-VERBATIM]** "I am not convinced the model quality is high enough to actually compare to ARIES. so I want to work with an agent to really think through what the comparison / evaluation will really be looking at. — Is it really just the raw LCOE number? — How are we going to compare if some of the input assumptions are different? — And if ARIES has a ton of engineering work and ours is surface-level, how much did we really demonstrate?"

From this session (2026-08-30):

- **[OWNER-VERBATIM]** "it isn't all about a single number -- LCOE will be thrown off for every changed assumption. What I also want to explore is whether we can actually compare something about the structural and behavioral modeling."
- **[OWNER-VERBATIM]** "I don't feel like our models are all that sophisticated, so the idea would be to choose an area to further develop, via a `goal` -- e.g. decompose some modeling area or bolster the physics modeling."
- **[OWNER-VERBATIM]** "we really haven't done anything interesting with the models, so doing the baseline now and breaking the 'holdout' label feels premature."
- **[OWNER-VERBATIM]** "both feel necessary" — the two quality dimensions (physics self-consistency; structural/costing depth), asked which one "ARIES-level" means.
- **[OWNER-VERBATIM]** "I'm done caring about the 1costingFE reproduction. we showed we could do it. pin it, or archive those models. but let's move on -- I do not want to be anchored to 1costingFE."
- **[OWNER-VERBATIM]** "for rubrics I don't care about it. but for the research, yes I still want to try and maintain the clean room" — the clean-room split: rubric-writing is exempt; model-facing research keeps the clean room.
- **[OWNER]** The seal stays. No reveal, no baseline comparison now; the earlier-considered scoped reveal is set aside (see Non-Goals).

## Success Criteria

When this work is complete:

1. **A depth rubric exists, written blind.** A per-subsystem rubric states what a systems-level fusion conceptual design study models and at what depth, on both dimensions — physics self-consistency (quantities computed vs fixed, constraints that push back) and structural/costing depth (part decomposition, cost sub-account granularity). Every rubric line cites its sources; the four sealed ARIES-CS papers are never among them (rubric sessions are otherwise exempt from the clean room — see the split ruling below). The finished rubric is committed and its `path@sha` recorded.
2. **The model is graded against the rubric.** A grading report scores the current model per subsystem per dimension, with each score traceable to model elements by path, and produces a gap ranking crossed with study evidence of what is load-bearing (cost share, binding constraints, error history).
3. **At least one maturation goal is grounded and run.** A goal targeting the top-ranked gap is grounded per `work/orchestration/GOAL_RUNBOOK.md`, executes at least one round, and its model changes hold up: the canonical validation battery passes and affected studies re-run without crashes or unexplained constraint-verdict flips (the full "clean" definition is a spec item). Reproducing 1costingFE is not a gate — Anchor A is closed evidence (see Non-Goals).
4. **Progress is measured by re-grading.** After goal round(s), the model is re-graded against the rubric version in force; the delta is the measured answer to "did we advance toward ARIES-level quality," available without unsealing anything. (Rubric revision policy: spec item, open question 6.)
5. **Reveal-readiness is a defined condition.** A written, owner-ratified condition states what rubric state (or other evidence) triggers Item 7. The reveal itself stays owner-held per PROTOCOL §6 — the condition informs the call, it does not automate it.
6. **The seal and the clean room hold where they apply.** The four sealed papers stay unread; model-facing sessions (goal research, model development) keep the clean-room rule — including treating rubric-ingested sources as barred until screened clean; the PROTOCOL log shows no reveal and no violations.
7. **The 1costingFE closure is recorded.** The handshake's achieved state is preserved per the owner's ruling — pinned (the exact model/package state where it holds, recorded and citable) or archived — and the standing handshake guardrail is updated to match, so no future session re-inherits the reproduction duty by accident.

---

## Why This Shape

- **Key bet:** "ARIES-level quality" can be characterized from the *class* of study ARIES-CS belongs to — systems-level conceptual design studies — without reading the sealed instance. The rubric operationalizes the owner's "peek at what good looks like" instinct against the class instead of the hold-out. **[OWNER 2026-08-30, "reason it out"]** The rubric is written by engineering reasoning against the model, existing repo sources, and Waganer — not by ingesting exemplar design studies. Exemplar reading stays available on demand if a rubric line is contested or a calibrated bar is later needed.
- **Why this shape is promising:** it converts an unactionable aspiration into a measurement loop (grade → goal → re-grade) using machinery that already exists (goal runbook, study layer, validation battery), and it *strengthens* the demo instead of spending it: the rubric doubles as a pre-committed prediction checkable at reveal time.
- **Why not reveal now:** the blind is the demo's one irreversible asset, and today's model state is not one anyone wants graded as the final exam. **[OWNER]** ruling above.
- **The 1costingFE anchor is closed, not carried.** **[OWNER 2026-08-30]** ruling above ("pin it, or archive those models"). Plainly: the handshake proved the machinery reproduces another tool's arithmetic, that proof stands at a recorded model state, and future development is free to make the model smarter even where that changes what the old handshake would print. Without this ruling, deepening the model would collide with the standing rule that the handshake must keep matching; with it, the collision disappears. The spec picks the mechanism (pin vs archive, open question 5) and records the ruling at the guardrail's home (`work/orchestration/stale-basis-recompute.md`).
- **The clean-room split.** **[OWNER 2026-08-30]** The clean room exists so the *model* is never built from ARIES-CS data — it binds the agents building the model, not the ones writing the yardstick. So: rubric sessions read design literature freely (fusion studies routinely cite ARIES-CS; tolerated there), with only the four sealed papers off-limits. Model-facing sessions keep the clean room as it stands today. The firewall between the layers is the rubric's output rule — depth prescriptions only ("decompose the blanket further", "make confinement push back"), never ARIES-CS-specific values or design facts — plus one bookkeeping rule: a source ingested for the rubric is barred for model-facing sessions until screened clean, so the exemption cannot leak the clean room away through the repo.
- **Constraint to preserve downstream:** the sealed papers stay sealed until Item 7, and the rubric and gradings are committed before any reveal so the yardstick cannot be shaped by it. PROTOCOL §4 (derived-artifact containment) still binds any future reveal-stage session.

---

## User Stories

### Measurement

**US-1: See quality as a trajectory.**
As the methodology owner, I can read the grading report and its re-grade deltas, so that "is the model getting closer to ARIES-level" is a measured claim rather than a feeling, and I can decide when Item 7 is worth triggering.

**US-2: A comparison richer than one number.**
As the methodology owner, I get depth-rubric reporting alongside the ratified B-2/B-3/B-4 comparison, so that the eventual Anchor B report reflects structure and behavior, not just LCOE — with the ratified verdict untouched unless I amend the bands.

### Direction

**US-3: Goals aimed at measured gaps.**
As the modeler, I pick the next development area from a ranked gap list crossed with study evidence, so that depth grows where it matters most instead of where it is most interesting.

**US-4: Refinement that doesn't regress.**
As the modeler, each goal round ends with the validation battery and affected studies re-run, so that added depth never silently breaks the model's own checks or its study results.

### The eventual reveal

**US-5: An honest claim that survives scrutiny.**
As the write-up author, I can state exactly what was blind and what was not — bands pre-committed (2026-07-19), sealed papers unread until comparison, model values never sourced from ARIES-CS, development directed by a class-based rubric written outside the clean room — so the public claim is accurate without overreach.

---

## Key Concepts

### 1. The depth rubric

A per-subsystem table with two columns of depth levels: physics self-consistency (what is computed, what pushes back, what closes the loop) and structural/costing depth (part decomposition below level 1, cost sub-account granularity, per-component costing). Illustrative shape only — e.g., subsystem rows spanning plasma/physics through buildings, levels running from "fixed cited input" to "computed with constraints binding"; the actual rows, level anchors, format, and home are spec decisions, including whether the rows must align with B-2's ratified correspondence list (which the reveal comparison will use). Sourced from class-referent studies; never from the sealed instance.

### 2. The grade → goal → re-grade loop

Stage 3⇄4 of the demo arc, run as designed for the first time: grade the model, cross with study evidence, ground a goal at the intersection ("biggest rubric gap" × "load-bearing in studies"), run rounds under the goal runbook's discipline, re-run affected studies, re-grade. The re-grade delta is the loop's output. The loop repeats until the reveal-readiness condition is met or the owner redirects; a goal that passes its gates but moves the rubric grade not at all is a named failure mode the spec's stopping rule must handle (surface to owner, don't loop silently).

### 3. Reveal-readiness condition

A short written statement, ratified by the owner, of what evidence makes triggering Item 7 worthwhile — e.g. a rubric threshold, named gaps closed, or study-stability criteria. Its exact form is a spec decision. It converts "when is the model good enough" from a recurring conversation into a checkable state, while leaving the trigger itself owner-held.

### 4. The rubric sits outside the clean room; its output is the firewall

Rubric authors read the literature freely (sealed papers excepted) and emit only depth prescriptions — what a real study models and how deeply, never ARIES-CS-specific values. Model-facing sessions consume the rubric and the goals, not the rubric's sources. At reveal time the rubric can be laid against ARIES-CS's actual depth as reported context in the Item 7 annex; no blind-prediction claim is made for it, and nothing about it touches the ratified pass/fail verdict.

---

## Scope of Behavior Changes

### New artifacts to create

- The depth rubric document (home and format per spec), committed with recorded `path@sha`
- The grading report (initial grade + gap ranking) and re-grade deltas
- One or more maturation goals under `work/orchestration/goals/` per the runbook contract
- The reveal-readiness condition statement (owner-ratified)
- The 1costingFE closure record (pin or archive, per open question 5)
- Model changes produced by goal rounds (library and/or `stellarator_09` instance), each with sourced citations per MR-4

### Existing artifacts to modify

- `.project/backlog/epic_stellarator_mbse_demo.md` — track this phase (item shape per EPIC_GUIDE; likely a stage-3 maturation item ahead of Item 7)
- `work/orchestration/stale-basis-recompute.md` — the standing handshake guardrail records the owner's closure ruling
- Study records — affected studies re-run against the matured model state
- `knowledge/holdout/aries-cs/PROTOCOL.md` — one owner-approved amendment recording the clean-room split (spec drafts it; owner approves; logged in §6). The seal itself is unchanged.
- No change to the governing concept's criteria or the ratified bands

### Behavior changes by workflow stage

- Stage 3 (research/refinement): moves from ad-hoc defect-driven fixes to rubric-directed goals with measured outcomes
- Stage 4 (studies): studies double as regression evidence for maturation rounds
- Item 7 (later, unchanged procedure): gains the rubric-check annex as reported material; formalization beyond that is owner-gated

---

## Non-Goals / Out of Scope

- **[OWNER]** No reveal and no baseline comparison now. A scoped agent-only reveal ("agent reads ARIES, models untouched, gap analysis defines goals") was considered this session and set aside: the model has not yet done enough for a comparison — blind or informed — to be worth the irreversible unseal. Item 7 runs later, as designed.
- **[OWNER]** Maintaining the 1costingFE reproduction is not a maturation duty. Anchor A is finished evidence ("we showed we could do it"); goals neither re-run nor preserve the handshake, and the write-up cites the pinned or archived state where it holds.
- **[OWNER]** The Waganer ARIES cost-account doc falls under the rubric exemption (ruled 2026-08-30, superseding the same-day "leave it" deferral): rubric sessions may read it freely; the §3 exception path remains in force for model-facing sessions.
- **[AGENT]** No amendment to criterion 4, the B-2/B-3/B-4 bands, or the governing concept — this phase slots inside the existing arc as stage 3, so the concept-level contract stands as ratified. (Any future fourth-axis formalization is a separate owner-ratified act, per Key Concept 4.)
- **[AGENT]** Reopening a deliberately scoped-out physics domain (e.g., confinement/τ_E, ruled out of scope as "Rung C") is an owner call made at goal grounding via the runbook's reserved gates — a goal may propose it, never assume it.
- **[AGENT]** No breadth-first deepening of all 14 subsystems — the rubric ranks; goals execute one gap at a time.
- **[AGENT]** Demo criterion 5's assessment (studies-through-study-layer) is separate work — its evidence exists and it can close independently of this phase.

---

## Assumptions & Prerequisites

- The goal runbook and its round discipline (`work/orchestration/GOAL_RUNBOOK.md`) are operational — evidenced by three completed goals.
- The study layer and canonical validation battery are available as regression gates (574/14/0 at tip).
- Anchor A is closed evidence at a recorded model state, not a live gate (owner ruling 2026-08-30; mechanism per open question 5).
- New-source ingestion for the rubric is in scope and necessary (see Key bet); the clean-room split makes it cheap for the rubric task, and the barred-until-screened bookkeeping keeps it safe for model-facing sessions.
- The demo branch shipped: PR #110 (`feat/wi033-p-pump-rebase`) merged to `main` 2026-08-30 — no pending-work sequencing question remains.

## Open Questions

1. Rubric format and home: rows, level anchors, directory, index registration — and whether rows must align with B-2's ratified correspondence list.
2. Grading protocol: who authors and who grades (fresh agent, authoring agent, or both for agreement), and how re-grading avoids drift.
3. The reveal-readiness condition's form: rubric threshold vs named-gap list vs study-stability criteria — and what evidence the owner wants in front of them when ruling.
4. Goal cadence and stopping rule: one goal at a time vs a small portfolio; when re-grade triggers the next goal vs a readiness check; the zero-delta failure mode's handling.
5. ~~The 1costingFE closure mechanism~~ — settled [OWNER 2026-08-30]: **pin.** Record the exact commit where the handshake holds; no file moves. Remaining detail: the wording recorded at the guardrail's home.
6. Rubric revision policy: frozen at v1, or revisable pre-reveal with each version committed at its own `path@sha`, deltas restated, and the prediction claim attaching to the last pre-reveal version.

---

## Next-Stage Handoff

**Settled here:**

- **[OWNER]** The seal stays; no reveal, no baseline comparison now (2026-08-30).
- **[OWNER]** Both quality dimensions — physics self-consistency and structural/costing depth — are in scope ("both feel necessary").
- **[OWNER]** Development direction is set via goals (the goal layer), targeting measured gaps.
- **[OWNER]** The 1costingFE anchor is closed: pin or archive, no ongoing reproduction duty (2026-08-30).
- **[OWNER]** The clean-room split (2026-08-30): rubric-writing exempt (Waganer included); model-facing research keeps the clean room; the four sealed papers unread until Item 7.
- **[OWNER]** The rubric is written by reasoning, no exemplar ingestion now ("reason it out", 2026-08-30); 1costingFE closure = **pin** (2026-08-30).
- **[OWNER]** The Waganer exception is deferred to request-time with concrete scope.
- **[AGENT] (ratified by owner, 2026-08-30)** The composition: rubric first (the yardstick), then grade, then goal(s) at the gap×load-bearing intersection, then re-grade — rather than goals picked directly from study evidence or agent judgment.

**Needs spec next:**

- Rubric format, level anchors, home, and B-2 alignment (open question 1)
- Grading protocol with authoring- and grading-bias controls (open question 2)
- The clean-room mechanics for model-facing research rounds: how goal research vets new sources, and how rubric-ingested sources get screened before model sessions may read them
- The PROTOCOL amendment text recording the clean-room split, for owner approval
- The 1costingFE closure mechanism and guardrail wording (open question 5)
- Reveal-readiness condition form and ratification path (open question 3)
- Goal cadence, stopping rule, zero-delta handling (open question 4); rubric revision policy (open question 6)
- The exact "clean" definition for study re-runs in success criterion 3

**Decomposition guidance:**

- Natural seams: (a) 1costingFE pin + PROTOCOL amendment (small admin, unblocking), (b) rubric authoring + initial grading (one item — the grade exercises the rubric and both are cheap together), (c) each maturation goal (goal-native tracking per the runbook, or its own item — spec picks one home to avoid double-tracking), (d) reveal-readiness condition (trivial-scale, owner-gated).
- Tracking home is the demo epic (`.project/backlog/epic_stellarator_mbse_demo.md`) since this is stage 3 of the demo arc; goal execution records live goal-native under `work/orchestration/goals/`. Read `.project/EPIC_GUIDE.md` before registering items.
