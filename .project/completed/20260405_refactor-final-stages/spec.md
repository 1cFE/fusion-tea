# Spec: Final Stages Rescope (Work Item #3)

**Status:** Draft
**Owner:** reid
**Created:** 2026-04-05
**Complexity:** MEDIUM
**Branch:** design-space-explore
**Depends on:** `.project/active/refactor-stage1-loop/` (Work Item #2 — stage1 loop refactor)

---

## Business Goals

### Why This Matters

With Work Item #2, the stage1 loop now runs assess *with* model output inside the loop. The assess step evaluates framing, completeness, and model consistency on every iteration. This means the current `review` prompt — which spends most of its time on citation verification, calculation re-derivation, and model parameter auditing — is now largely redundant with what assess does autonomously.

Meanwhile, the things a human review is actually good at — strategic judgment about modeling approach, whether the right things are being emphasized, whether a concept's positioning makes sense in the broader investigation — have no dedicated step. The current review buries these under 100+ lines of numerical QA checklist.

The result: review becomes a human judgment gate with two clear outcomes (proceed or kick back), and a lightweight final check at synthesis guards the approve step.

### Success Criteria

- [ ] The human review focuses on strategic/qualitative assessment, not numerical QA.
- [ ] Review produces a clear verdict: PROCEED (with optional minor fixes) or REVISE (with corrective actions that feed back into stage1).
- [ ] The kick-back path to stage1 is explicit: corrective actions from review are formatted as feedback that `stage1-all --resume` can consume.
- [ ] A final check exists between synthesis and approval.

### Priority

Last of the three refactor work items. Can be done incrementally — the review rescope is the core change; the synthesis gate is lighter.

---

## Problem Statement

### Current State

The `review` prompt template (`review.md`, 144 lines) is a detailed numerical QA checklist:

| Section | What it checks | Lines |
|---|---|---|
| Citation Verification | Search sources for quoted text | 27–36 |
| Calculation Verification | Re-derive inferred values independently | 37–42 |
| Model Setup Audit | Trace every `model.forward()` parameter to analysis | 43–53 |
| Internal Consistency | Cross-section value agreement | 54–56 |
| Factual Concerns | Unsupported claims, implausible numbers | 57–60 |

The assess prompt (`assessment.md`) explicitly says: *"You are NOT checking numerical accuracy — that is the review stage's responsibility."* With WI#2 moving model-setup inside the loop and feeding model output to assess, the boundary between "what assess checks" and "what review checks" has shifted. Assess now evaluates model consistency on every iteration. Citation verification and calculation re-derivation remain un-automated, but they are also the least valuable part of the review — the stage1 loop's multiple iterations tend to self-correct numerical issues.

The review output (`review.md`) uses a `PA-N: Proposed Action` format with `Decision: _[USER FILLS IN]_` fields. `address-review` then applies those decisions. This works for targeted fixes but doesn't support the "kick back to stage1 with strategic feedback" path — that would need feedback in `config/feedback_format.md` format, not PA-N format.

### Desired Outcome

Two-phase post-loop flow:

```
Stage 1 loop converges
    ↓
Human Review (strategic/qualitative)
    ├── PROCEED (with optional minor fixes) → address minor → synthesize
    └── REVISE (with corrective actions) → stage1-all --resume (review as feedback-producer)
         ↑                                         │
         └─────────────────────────────────────────┘

Synthesize → Final Check → Approve
```

---

## Scope

### In Scope

1. **New review prompt** — refocused on strategic/qualitative assessment.
2. **Review verdict** — structured PROCEED/REVISE outcome in review output.
3. **Kick-back path** — REVISE corrective actions formatted as feedback for stage1 (another substitutable feedback-producer per WI#2 FR-16).
4. **address-review update** — only runs on PROCEED path for minor fixes; unchanged mechanically.
5. **Assess prompt update** — remove the "you are NOT checking numerical accuracy" exclusion, since review is no longer doing that job. Allow assess to check what it can.
6. **Final synthesis check** — a lightweight step between synthesize and approve.
7. **Update `Review-Status` values** — current values (`has-actions`, `clean`, `addressed`) replaced or extended to reflect the new PROCEED/REVISE model.

### Out of Scope

- **Stage1 loop changes.** That's WI#2. This spec only adds a new feedback-producer (review corrective actions) to the already-defined substitutable-prompt interface.
- **Automated citation verification.** If review stops doing it, nothing replaces it. If we want it back later, it's a separate optional "audit" step.
- **Changes to synthesize mechanics.** The synthesis prompt and its behavior stay the same. Only the gate before approve changes.

### Edge Cases & Considerations

- **Gradual migration.** The old review prompt and its PA-N format have been used on all 36 concepts. Some may have reviews in progress. The new prompt can coexist — new reviews use the new format; existing `review.md` files with PA-N format continue to work with `address-review`.
- **REVISE loop depth.** A human could review → REVISE → stage1 resume → re-review → REVISE again. There's no limit. This is fine — the human is in control. Each review's corrective actions go into the next iteration's `iter-N/feedback.md` with `feedback_source: "review"`.
- **Numerical QA gap.** Dropping citation verification and calculation re-derivation from review means nobody does them systematically. The mitigation: assess catches structural/model inconsistencies inside the loop, and the human eyeballs numbers during review. If a systematic numerical audit is wanted later, it becomes an optional `audit` step (out of scope here).
- **Review is still agent-generated.** The agent produces the review document (strategic assessment, questions, recommendations). The human reads it, fills in the verdict field, and optionally adds notes. This is the same human-in-the-loop pattern as today, just with different content.

---

## Requirements

### Review Rescope

1. **FR-1:** A new review prompt template SHALL replace the current `review.md` template. The new prompt SHALL focus on:
   - **Modeling approach:** Is the concept being modeled the right way? Are the key cost drivers and differentiators captured?
   - **Strategic positioning:** Does the analysis correctly characterize where this concept sits relative to others? Are the comparison axes meaningful?
   - **Risk and uncertainty framing:** Are the right risks highlighted? Is the confidence assessment realistic?
   - **Data sufficiency:** Are there critical gaps that should trigger more research before proceeding?
   - **Cross-concept consistency:** Are assumptions consistent with approved analyses of related concepts?

   The new prompt SHALL NOT include: citation verification, calculation re-derivation, or model parameter auditing checklists.

2. **FR-2:** The review output SHALL include a structured verdict section with exactly one of:
   - `VERDICT: PROCEED` — the analysis is strategically sound. Optional minor notes may follow.
   - `VERDICT: REVISE` — significant strategic issues require another pass through stage1. Corrective actions follow.

   The verdict line SHALL be human-editable (agent proposes, human confirms or overrides).

3. **FR-3:** When the verdict is `REVISE`, the review output SHALL include corrective actions in `config/feedback_format.md` format (`### F-N:` findings with targets and recommendations). This enables the review to act as a feedback-producer for `stage1-all --resume` per WI#2 FR-16.

4. **FR-4:** When the verdict is `PROCEED`, the review output MAY include minor notes in the existing `PA-N` format (for `address-review` to consume). These are small fixes that don't warrant a full stage1 re-run.

5. **FR-5:** `Review-Status` frontmatter values SHALL be updated. Current frontmatter values (`run_analysis.py:471-478`):

   | Current value | Set by | Meaning |
   |---|---|---|
   | `has-actions` | `review` (issues found) | Review found issues with PA-N actions |
   | `clean` | `review` (no issues) | Review found no issues |
   | `addressed` | `address-review` | User decisions applied |

   Note: `get_concept_state()` (`state.py:33`) maps `addressed` or `clean` → state `"reviewed"`. `"reviewed"` is a state detection output, not a stored frontmatter value.

   Proposed replacement:

   | New value | Replaces | Meaning |
   |---|---|---|
   | `proceed` | `clean`, and `has-actions` when issues are minor | Review passed strategic assessment; optional PA-N minor fixes |
   | `revise` | `has-actions` when issues are strategic | Significant issues require stage1 re-run |
   | `addressed` | _(unchanged)_ | Minor fixes from PROCEED review applied |

   `cmd_synthesize()` currently gates on `Review-Status in ("addressed", "clean")` (line 631-632) — this SHALL be updated to `in ("addressed", "proceed")`. Legacy values (`clean`, `has-actions`) SHALL continue to be recognized by `get_concept_state` for backward compatibility with existing analyses.

### Kick-Back Path

6. **FR-6:** The review's corrective actions (from a REVISE verdict) SHALL be consumable as a feedback-producer by the stage1 loop. The workflow is:
   1. `review` generates `review.md` with `VERDICT: REVISE` + `### F-N:` findings.
   2. Human confirms or edits the verdict and findings.
   3. `stage1-all <concept> --resume` detects `Review-Status: revise` and selects `review.md` as the feedback source for the next iteration.

   This adds `"review"` to the `feedback_source` enum in `verdict.json` (alongside `"assess"`, `"source_integration"`, `"research"`, `"cold_start"` from WI#2 FR-19).

   **Feedback-producer priority order** (highest to lowest, evaluated on each iteration):
   1. **Cold start** — iteration 1, no resume
   2. **Review corrective actions** — resume + `Review-Status: revise` (NEW). One-shot: fires once via `used_review_feedback` flag, then falls through to assess on subsequent iterations. Analogous to `source_integration`'s one-shot behavior.
   3. **Source-integration** — resume + new sources detected
   4. **Research** — `--research` flag, iteration > 1
   5. **Assess** — default, iteration > 1

7. **FR-7:** After a REVISE kick-back, when stage1 converges again, the review step runs again. The iteration count on the review itself increments (`Review-Iterations` in frontmatter).

### Assess Prompt Update

8. **FR-8:** The assess prompt template SHALL be updated to:
   - **Remove** the "You are NOT checking numerical accuracy" exclusion and the explicit list of deferred checks (citation correctness, calculation verification, etc.).
   - **Add** a "numerical plausibility" check dimension. This is NOT full calculation re-derivation (expensive, formerly review's job). It IS: orders-of-magnitude reasonableness, model output LCOE alignment with analysis narrative, physical plausibility of parameter values. The assess step already receives `model_output_path` inside the loop (`loop.py:476`), so it has the data — it needs prompt guidance to use it.
   - The exact checklist wording is a prompt-tuning decision; the requirement is that numerical plausibility is an explicit assessment dimension, not just an unlocked possibility.

### Address-Review Update

9. **FR-9:** `address-review` SHALL only be invoked after a PROCEED verdict. If `Review-Status` is `revise`, `address-review` SHALL print a message directing the user to run `stage1-all --resume` instead.

10. **FR-10:** `address-review` mechanics are otherwise unchanged — it reads PA-N actions with filled Decision fields and applies them via the agent.

### Final Synthesis Check

11. **FR-11:** The `approve` command SHALL add a new gate requiring that a review with verdict PROCEED exists (i.e., `Review-Status` is `proceed` or `addressed`). Currently, `approve` only checks that `synthesis.md` exists (`run_analysis.py:760-762`); it does not check `Review-Status`. The new gate adds a direct review check so that manually creating `synthesis.md` cannot bypass the review step. If `Review-Status` is `revise` or missing, `approve` SHALL refuse with a message. `--force` overrides both the synthesis and review gates.

12. **FR-12:** [RESOLVED — DEFERRED] No agent-driven "synthesis review" step between synthesize and approve. The human reads `synthesis.md` before approving; the review gate (FR-11) and synthesize gate (`Review-Status` check) provide sufficient quality control. If quality issues emerge in practice, a synthesis-review prompt can be added as a separate work item.

---

## Acceptance Criteria

### Review Rescope

- [ ] New review prompt produces strategic/qualitative assessment, not numerical QA checklist.
- [ ] Review output contains `VERDICT: PROCEED` or `VERDICT: REVISE` as a structured line.
- [ ] REVISE reviews include corrective actions in `config/feedback_format.md` format.
- [ ] PROCEED reviews may include minor `PA-N` actions for address-review.
- [ ] `Review-Status` frontmatter uses new values (`proceed`, `revise`). Legacy values still recognized.

### Kick-Back Path

- [ ] After a REVISE review: `stage1-all <concept> --resume` uses the review's corrective actions as feedback for the next iteration.
- [ ] `verdict.json` for the resumed iteration records `feedback_source: "review"`.
- [ ] After stage1 re-converges, running `review` again works (iteration increments).
- [ ] Full round-trip: stage1 → review(REVISE) → stage1 --resume → review(PROCEED) → address-review → synthesize → approve.

### Assess Update

- [ ] Assess prompt no longer contains the "NOT checking numerical accuracy" exclusion.
- [ ] Assess still produces output in `config/feedback_format.md` format (no structural change).

### Address-Review

- [ ] `address-review` on a concept with `Review-Status: revise` prints a redirect message and exits without modifying files.
- [ ] `address-review` on a concept with `Review-Status: proceed` works as before.

### Approve Gate

- [ ] `approve` on a concept without a PROCEED review refuses with a message.
- [ ] `approve --force` overrides the gate.
- [ ] `approve` on a concept with `Review-Status: proceed` or `addressed` works as before.

### Backward Compatibility

- [ ] Existing concepts with old-format `review.md` (PA-N format, `Review-Status: has-actions` or `clean`) continue to work with `address-review` and `approve`.
- [ ] `get_concept_state` correctly handles both old and new `Review-Status` values.
- [ ] `status` command displays correctly for concepts in any state (old or new review format).

---

## Related Artifacts

- **Prereq:** `.project/active/refactor-stage1-loop/spec.md` (Work Item #2 — stage1 loop with substitutable feedback-producers).
- **Design concept:** `.project/active/refactor-run-analysis/design-concept.md` — the broader vision. This spec implements the "human intervention gate" and "review becomes editorial/judgment" aspects.
- **Current prompts:** `prompt_templates/review.md`, `prompt_templates/address_review.md`, `prompt_templates/assessment.md` — to be updated.
- **Feedback format:** `prompt_templates/config/feedback_format.md` — the shared schema that review REVISE actions must use.

---

**Next Steps:** After approval, proceed to `/_my_design`. The review prompt rewrite is the core deliverable; the plumbing changes (verdict parsing, kick-back, gates) are straightforward once the prompt shape is defined.
