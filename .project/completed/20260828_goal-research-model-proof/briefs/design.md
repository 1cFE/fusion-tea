# Brief to /_my_design — GSTH Item 5: Research-to-Model Round Proof

Write `.project/active/goal-research-model-proof/design.md`. Do NOT run git commits.
Finish with `ARTIFACT: <path>`, or ask if genuinely blocked.

## Contract

The spec is the contract: `.project/active/goal-research-model-proof/spec.md`
(revised 2026-08-27 against `spec-review.md`, all must-fix findings applied). Owner
rulings in `align.md` are settled. Requirements source behind the spec:
`.project/backlog/epic_goal_strategy_task_harness.md` § Item 5.

This is a PROOF/EXECUTION item, not a feature build. "Design" here means: how the live
run is structured, sessioned, evidenced, and kept honest — not new code architecture.
The only repo-content changes are: the new goal directory, trail/learnings writes, the
GOAL_RUNBOOK research-row flip (R-G1–G4), discovery-log disposition rows (R-F1), the
CURRENT_WORK Phase 4 list note (R-A7a), and whatever the native seams themselves write.
No new scripts or mechanisms (R-H1 hardening rule).

## The spec's four open questions are yours to settle (record each as D-N with rationale)

1. **Goal slug/directory** — propose one (the question is about the model value, per
   R-A2a; e.g. `p-pump-basis`-like). Final wording of the question is the owner's at
   gate (a); the slug proposal must not smuggle the research errand in.
2. **Rounds and the floor** — one round; ship on the floor if the second half is blocked
   (spec § Open Questions states the floor). Decide and record.
3. **Bound on the follow-up WI** — the epic budget is 8h execute; decide how far the
   authorized modeling task is carried (recommend: through the modeling PM's spec/design
   at most, implementation only if trivially small — you decide and bound it).
4. **Session choreography** — how the critic (R-C5) and RoundReview (R-F4) sessions are
   obtained and their evidence kept. Item 4's working pattern is the reference:
   `.project/completed/20260827_goal-cold-pickup-proof/operator-notes.md` § Mechanism
   notes. Two hard-won operational facts you MUST design around (auto-memory, verified):
   - Fresh headless sessions run as direct `claude -p --output-format stream-json
     --verbose` teed OUTSIDE the repo — never via orchestrate-stage.sh.
   - Goal/trail templates contain literal placeholder headings (`### T-001 return —
     YYYY-MM-DD`); any disk predicate against goal files must be date-anchored or it
     false-positives.

## Design must also cover

- **The grounding exchange guard (R-A2a hazard)** — how the owner-facing grounding
  conversation and the task brief are kept to the modeling objective so the research
  prerequisite can only EMERGE. Concretely: what the grounding prompt may and may not
  contain.
- **Owner pause points** — gate (a) at grounding, gate (b) at WI mint/advance, gate (c)
  at a judgment-call close. The run parks and asks; design where and how each park is
  written so the owner can rule asynchronously.
- **The covering-branch declaration (R-H4)** — its file, location, content shape, and
  the commit-before-round ordering that makes it ancestry-checkable.
- **Seam invocation plan (R-D1/R-D2)** — the concrete `research_seam.py` request shape
  for this need (consumer = discovery row id), per `docs/research_seam_operator_guide.md`.
  The likely `OPERATOR_QUEUE` path end-to-end, including what parks and what closes.
- **Evidence layout** — where run transcripts/records live in the item dir vs the goal
  dir vs native homes; verification_record.md structure (match Item 4's shape).
- **Runbook flip mechanics (R-G1–G4)** — exact edits, ordered after the seam run commit.

## Boundaries

Non-goals per spec. Don't restate the runbook — cite it. Provenance discipline per
capture-fidelity: your decisions are agent-grade (D-N with rationale); owner rulings
stay marked as they are in the spec.
