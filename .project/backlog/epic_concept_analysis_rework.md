# Epic: Concept-Analysis Pipeline Rework

**Epic ID**: CONCEPT-REWORK
**Status**: Draft
**Priority**: P0
**Created**: 2026-05-30
**Estimated Effort**: ~9–13 days

**Design**: [`.project/concepts/concept-analysis-rework-design.md`](../concepts/concept-analysis-rework-design.md)
**Touchpoints research**: [`.project/research/20260530-concept-rework-code-touchpoints.md`](../research/20260530-concept-rework-code-touchpoints.md)
**Companion docs**: [`.project/concepts/concept-analysis-rework.md`](../concepts/concept-analysis-rework.md), [`.project/research/20260509-1costingfe-enum-map.md`](../research/20260509-1costingfe-enum-map.md), [`.project/research/20260530-072832_1costingfe-and-pipeline-redesign-context.md`](../research/20260530-072832_1costingfe-and-pipeline-redesign-context.md)

---

## Executive Summary

The concept-analysis pipeline produces per-concept LCOE numbers that look comparable but aren't: each concept's `analysis.md` describes a different (often composite) plant, each `model_setup.py` re-derives library work and buries analyst judgment in code, and "1 GWe NOAK" is reached by a different mechanism for every concept. This epic splits the work into two crisp layers — **specify one named plant** per concept, **project its cost at one standardized scale** via a single two-knob mechanism — and reorganizes the per-concept setup files so the costing library carries the default story and every analyst departure is one accountable, toggleable, evidence-backed override.

**Critical Success Factor**: After rollout, every costingfe concept's `result_1gw` is reached by `forward(net_electric_mw=1000, n_mod=1000/P_native, override_reference_mw=P_native)`, and every cost departure from the library is a single registry entry with `account / value / enabled / provenance / source / rationale`.

---

## Why This Epic?

**Current State**:
- Within a single concept, geometry, performance, and cost anchors often describe three different plants stitched together; the unit the LCOE number describes does not exist as a coherent design anywhere.
- `model_setup.py` files re-pass dozens of library defaults as if deliberate, drifting from library updates and hiding which numbers are actually the analyst's judgment.
- "1 GWe NOAK" is reached differently per concept (native scale, single-knob output-power scaling, no scaling at all) under one label — comparison view is not apples-to-apples.
- Archetype mapping, comparables, and family classification are agent-judgment at runtime; every concept's review is subtly different.
- The critic only runs in-loop (`assess`, `review`), entangled with loop state — can't be applied to archived concepts.

**Future State**:
- Each `analysis.md` has one **Design Point block**: one named plant, its native scale, its source citations; every LCOE parameter on the page describes that unit.
- Each `model_setup.py` is a short, ordered four-step script: spec → native forward → override registry → 1 GWe NOAK forward. No re-passed library defaults.
- Every override is a six-field record (`account / value / enabled / provenance / source / rationale`); flipping `enabled: False` reverts that account to the library's answer.
- Archetype, archetype-fit grade, and comparables are pre-computed project-level tables read by the orchestrator, not invented at runtime.
- `model_critic` is a standalone tool invokable against any concept directory at any time.
- `concept_explorer` reads each concept's `result_1gw` at exactly 1000 MWe, reached by the same two-knob mechanism — comparison is apples-to-apples by construction.

---

## Success Criteria

- [ ] 1costingFE accepts non-integer `n_mod > 0`; override scaling under the two-knob call is verified by test.
- [ ] Ontology, archetype-fit, and comparables tables exist as the single source of truth; consumed by orchestrator and prompts.
- [ ] Every non-`None` fit-grade concept has a regenerated `analysis.md` with a Design Point block and a regenerated `model_setup.py` matching the four-step shape.
- [ ] Every regenerated `model_setup.py` exposes `model`, `result`, `result_1gw` at module level; `result_1gw` is reached by the two-knob call at `net_electric_mw=1000`.
- [ ] Override registry validator enforces six-field entries; AST validator enforces the module-level contract and the `net_electric_mw=1000` call shape.
- [ ] `model_critic` runs cleanly against an archived concept (no loop-state dependency).
- [ ] `concept_explorer` reads `result_1gw` from every costingfe concept with no fallback path; `Confinement-Family:` is read from frontmatter, not body prose.
- [ ] Toggling all overrides off in any `model_setup.py` produces the library's bare answer for that concept's specified plant (manual spot-check on the pilot set).

---

## Backlog Items

> Each item below names the files touched and the general success criteria only. Mechanism, data shapes, and any cross-cutting design decisions are deferred to that item's own `spec.md` / `design.md`.
>
> **Sequencing principle**: the high-risk bets in this rework are agent-driven (Design Point extraction, override honesty, critic acuity), not coding. Phase 0 front-loads cheap, throwaway probes that exercise those bets *before* any plumbing is built, so the plumbing in Phase 1 is designed against what the prompts actually need — and so bet failure is caught on day 2, not day 7.

---

## Phase 0 — De-risk the agent-driven bets (~2 days, mostly throwaway)

### Item 1: End-to-End Manual Prototype (one concept)

**Type**: Research / Throwaway
**Effort**: ~1 day
**Dependencies**: None.

**What this is**: a hand-driven walkthrough of the rework on a single concept, with everything stubbed or hand-written. No helpers, no validators, no template files, no CLI subcommands. Goal is signal, not artifacts.

**Activities**:
- Pick one concept with a clean dossier and a likely-High archetype fit.
- Hand-write the archetype-fit row and a tiny comparables stub (just the rows needed for this concept).
- Hand-draft the new analyze prompt and run it one-shot (`claude -p`) against the dossier. Read the Design Point block and override candidates by eye.
- Hand-write the four-step `model_setup.py` using current 1costingFE; run it. Inspect `result` and `result_1gw` per-account values. Empirically check whether overrides scale sensibly under the two-knob call (i.e. de-risk Item 4's library precondition before formal test work).
- Hand-draft the `model_critic` prompt and run it against the artifacts. Read its output.
- Write a short findings doc.

**Success Criteria**:
- [ ] Findings doc enumerates: which of the six key bets held, which wobbled, which broke.
- [ ] If the 1costingFE override-scaling invariant holds empirically, Item 4 scope shrinks to "formalize as test"; if not, Item 4 scope grows and the fix is informed by what we saw.
- [ ] Hand-drafted prompts (analyze, model_setup discipline note, critic) are saved as the starting point for Item 7's productionized versions.

**Kill switch**: if Design Point extraction is incoherent, or overrides come back as dressed-up library defaults with no real provenance, **stop and rethink** before committing to Phase 1.

**Deliverables**:
- `.project/active/concept-rework-prototype/findings.md`
- Throwaway artifacts under `/tmp/` or a scratch dir; do not pollute `analyses/`.

---

### Item 2: Prompt-Stability Probe

**Type**: Research / Throwaway
**Effort**: ~0.5 day
**Dependencies**: Item 1 (reuses the analyze prompt draft).

**What this is**: re-run the Item 1 analyze prompt twice on 2–3 *additional* concepts (spanning likely-Med and likely-Low archetype fit), and diff the outputs run-to-run.

**Success Criteria**:
- [ ] For each concept, Design Point name and `P_native` are stable across repeated runs (or instability is characterized — which fields drift, by how much).
- [ ] Override candidate sets overlap meaningfully across runs (or non-overlap is characterized).
- [ ] Findings folded into the Item 1 doc as a stability addendum.

**Kill switch**: if stability is poor and the cause isn't an easy prompt fix, the "specify one named plant" framing needs re-design before Phase 1.

**Deliverables**:
- Updates to `.project/active/concept-rework-prototype/findings.md`.

---

### Item 3: Critic Acuity Probe (against existing artifacts)

**Type**: Research / Throwaway
**Effort**: ~0.5 day
**Dependencies**: Item 1 (reuses the critic prompt draft). Can run parallel to Item 2.

**What this is**: point the hand-drafted `model_critic` prompt at 2–3 *existing* (un-regenerated) concept directories — ones where we already know inconsistencies live. Mock-feed fit grade and comparables by hand.

**Success Criteria**:
- [ ] For each concept, the critic surfaces at least one of the known inconsistencies (and we record which it misses).
- [ ] Findings folded into the Item 1 doc as a critic-acuity addendum.

**Kill switch**: if the critic produces only generic boilerplate, the standalone-critic bet is weaker than the design assumes — Phase 1's Item 8 needs a rethink (e.g. fold critique back into `assess` rather than standalone).

**Deliverables**:
- Updates to `.project/active/concept-rework-prototype/findings.md`.

---

## Phase 1 — Build the plumbing (informed by Phase 0)

### Item 4: 1costingFE Library Preconditions

**Type**: Code/Integration
**Effort**: 0.5–1 day (may shrink to ~0.25 day if Phase 0 empirically confirmed the override-scaling invariant already holds).
**Dependencies**: Item 1 (Phase 0 findings determine scope).

**Files touched** (in `~/1cfe/1costingfe/`):
- `src/costingfe/validation.py` — `n_mod` field constraint.
- `src/costingfe/model.py` — `_scale_overrides` and `forward()` override paths (verify; modify only if Phase 0 or formal test finds a gap).
- Library tests.

**Success Criteria**:
- [ ] The two 1costingFE invariants the design depends on (non-integer `n_mod`; correct override scaling under the two-knob call) hold and are covered by tests.
- [ ] Library version pinned for downstream consumption.

---

### Item 5: Deterministic Project Tables + Comparables Sanity-Check

**Type**: Implementation
**Effort**: 1–1.5 days
**Dependencies**: Item 1 (Phase 0 findings sanity-check the table schemas before all 38 rows are populated). Parallel with Item 4.

**Files touched** (new, location TBD in spec):
- Ontology table.
- Archetype-fit table (seedable from [`enum-map`](../research/20260509-1costingfe-enum-map.md)).
- Comparables table (or derivation script reading ontology).
- Comparables sanity-check script.

**Success Criteria**:
- [ ] All three tables exist and cover every concept.
- [ ] Sanity-check script produces structured output for an LLM reviewer (not a verdict) on a hand-fed pair of concepts.

---

### Item 6: Pipeline Glue — Frontmatter, `concepts.py`, CLI Subcommands

**Type**: Code/Integration
**Effort**: 1–1.5 days
**Dependencies**: Item 5.

**Files touched** (in `exploration/concept_analysis/scripts/`):
- `lib/concepts.py` (replace hard-coded archetype mapping with table read).
- `lib/frontmatter.py` (new fields + `Reuses` → `Comparables` rename).
- `lib/loop.py` (minimal — drop dependence on dropped validators).
- `run_analysis.py` (new subcommands: regenerate-concept, init-tables).
- Knock-on `Reuses` renames across `lib/`.

**Success Criteria**:
- [ ] Archetype routing reads the table; freeform vs costingfe is determined by `fit_grade`.
- [ ] New frontmatter fields emitted and pre-populated from the upstream tables.
- [ ] Regenerate-concept and init-tables subcommands run end-to-end on a dry-run target.

---

### Item 7: Shared `model_setup` Helpers + Validator Rework

**Type**: Implementation
**Effort**: 1–1.5 days
**Dependencies**: Items 1 (prototype informs the helper API shape), 4, 5.

**Files touched** (in `exploration/concept_analysis/scripts/`):
- `lib/model_setup_helpers.py` (new shared utility module).
- `lib/validators.py` (drop the regex-on-LLM-markdown validators; add new contract checks for `model_setup.py` and the override registry).

**Success Criteria**:
- [ ] A regenerated `model_setup.py` can be written as a short, ordered script against the shared helpers, with no per-concept duplication of the two-knob forward pattern or the override-registry → `cost_overrides` translation.
- [ ] Validators enforce the design's module-level contract (`model`, `result`, `result_1gw` at module level; `result_1gw` reached at `net_electric_mw=1000`) and the override-registry shape; fragile regex validators are removed.
- [ ] Loop runs cleanly on a dry-run without the dropped validators.

---

### Item 8: Prompt Template Rework

**Type**: Implementation
**Effort**: 1–1.5 days (down from 1.5–2: Phase 0's hand-drafts are the starting point).
**Dependencies**: Items 1 (productionizes the Phase 0 hand-drafts), 5, 6, 7.

**Files touched** (in `exploration/concept_analysis/prompt_templates/`):
- `analysis_v2.md` + `output_template.md`.
- `model_setup_costingfe.md` + `model_setup_costingfe_edit.md`.
- `assessment.md` + `review.md` + `config/feedback_format.md` + `config/assessment_checklist.md`.
- `config/analysis_goals.md`, `config/quality_standards.md`, `config/scoring_framework.md`.
- `synthesis.md`, `score.md` (rename leak-through only).

**Out of Scope**: `model_setup_freeform*.md` (deferred per design non-goal).

**Success Criteria**:
- [ ] Dry-run on one concept produces an `analysis.md` containing the Design Point block and a `model_setup.py` matching the four-step shape.
- [ ] Assess/review output is parse-robust under the new validators (no reliance on the dropped regex paths).
- [ ] Quality-standards doc reflects the new discipline (no re-passing of library defaults; every parameter describes the design point).

---

### Item 9: `model_critic` Standalone Tool

**Type**: Code/Integration
**Effort**: 0.5–1 day (down from 1: Phase 0's hand-drafted critic prompt is the starting point).
**Dependencies**: Items 1 (productionizes the Phase 0 critic prompt), 5.

**Files touched** (in `exploration/concept_analysis/`):
- `scripts/agents/model_critic.py` (new).
- `prompt_templates/model_critic.md` (new).
- `scripts/run_analysis.py` (new subcommand).

**Success Criteria**:
- [ ] `model_critic` runs against active **and** archived concept directories with no loop-state dependency and writes one review document next to the artifacts.

---

---

## Phase 2 — Pilot + bulk rollout

### Item 10: Explorer Adapter + Pilot Regeneration

**Type**: Code/Integration + Execution
**Effort**: 1.5–2 days
**Dependencies**: Items 4, 6, 7, 8, 9.

**Files touched**:
- `exploration/concept_explorer/extract_explorer_data.py` (frontmatter read; drop `result_1gw` fallback; fractional `n_mod` verification; narrative-extraction prompt).
- New artifacts under `exploration/concept_analysis/analyses/` for 3–5 pilot concepts spanning High / Med / Low archetype-fit.
- `pilot_report.md` in the work-item directory.

**Success Criteria**:
- [ ] Explorer reads every pilot concept without a fallback path; family field resolves from frontmatter.
- [ ] Every pilot `result_1gw` is at exactly `net_electric_mw=1000` via the two-knob mechanism.
- [ ] Pilot report enumerates issues found and any fixes folded back into templates/helpers/validators before bulk rollout.

---

### Item 11: Bulk Regeneration

**Type**: Execution
**Effort**: 1–1.5 days
**Dependencies**: Item 10.

**Files touched**:
- Regenerated artifacts under `exploration/concept_analysis/analyses/` for every non-`None` fit-grade concept.
- Snapshots of any User-Decisions worth preserving (to `.project/`) before deletion.
- Per-batch logs in the work-item directory.

**Out of Scope**: freeform / `None` fit-grade concepts (untouched, asterisked in explorer).

**Success Criteria**:
- [ ] Every non-`None` concept has fresh artifacts conforming to the new contract; validators pass.
- [ ] Cross-concept comparison view shows uniform `result_1gw @ 1000 MWe` semantics across all non-freeform concepts.

---

### Item 8: Bulk Regeneration

**Type**: Execution
**Effort**: 1–1.5 days (spec 0.5h, design 0.5h, plan 1h, execute 6–10h)
**Dependencies**: Item 7 (pilot signs off the pipeline).

**Objective**: Regenerate every non-`None` fit-grade concept under the new pipeline; leave `None` concepts asterisked and untouched.

**Scope**:
1. For each non-`None` concept: snapshot any User-Decisions worth preserving; `cmd_regenerate_concept`.
2. Spot-check via `model_critic` on a sample; run override-toggle invariant check on a few.
3. Update `concept_explorer` snapshot/views; confirm comparison view is apples-to-apples.
4. Asterisk freeform concepts in the explorer per design.

**Out of Scope**:
- Touching freeform concepts' `analyses/{id}/`.
- Editing `knowledge/concept_research/{id}/`.

**Success Criteria**:
- [ ] Every non-`None` concept has fresh artifacts conforming to the new contract.
- [ ] Cross-concept comparison view shows uniform `result_1gw @ 1000 MWe` semantics.
- [ ] Validator suite passes on every regenerated `model_setup.py`.

**Deliverables**:
- `.project/active/concept-rework-bulk/plan.md` and per-batch logs.
- Regenerated artifacts under `exploration/concept_analysis/analyses/`.

---

## Dependencies

**External**:
- 1costingFE library (Item 1 modifies it; downstream items pin the updated version).
- Claude CLI / agentic-mbse for pipeline execution.

**Internal**:
- None — this epic owns the rework end-to-end.

**Item Dependency Graph**:
```
Phase 0 — De-risk
  Item 1 (E2E manual prototype)
     │
     ├──> Item 2 (prompt-stability probe)
     └──> Item 3 (critic acuity probe)
     │
     │   [KILL SWITCH: review findings before Phase 1]
     ▼
Phase 1 — Plumbing
  Item 4 (library prereqs)   Item 5 (tables + sanity check)
                                          │
                              ┌───────────┼───────────┐
                              ▼           ▼           ▼
                          Item 6      Item 7       Item 9
                          (glue)      (helpers      (critic
                                       + valid.)    productionized)
                              ▲           ▲
                              └─────┬─────┘
                                    ▼
                              Item 8 (prompts productionized)

Phase 2 — Rollout
  Item 10 (explorer adapter + pilot 3–5 concepts)
        │
        ▼
  Item 11 (bulk regenerate)
```

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Agent can't reliably extract a coherent Design Point from a dossier | **High** — specification layer never settles; whole rework rests on this | Item 1 probes this on day 1 with a throwaway prompt; Item 2 tests stability across re-runs. Kill switch if it breaks. |
| Agent populates overrides as dressed-up library defaults rather than honest provenance | **High** — accountability story is theater | Item 1 inspects override provenance by hand on the prototype concept. Kill switch if provenance is fabricated. |
| `model_critic` rubber-stamps rather than finds issues | High — independent-review story collapses | Item 3 points the critic at known-bad existing artifacts before any productionization. Phase 1's Item 9 reshapes if the standalone framing doesn't hold. |
| 1costingFE override-scaling under the two-knob call doesn't behave as design assumes | High — invalidates the cost-projection invariant | Item 1 exercises it empirically on a real concept; Item 4 formalizes the test (and fixes if needed). |
| New prompt structure produces lower-quality `analysis.md` than current free-form template | Med — pilot exposes; bulk regen amplifies | Phase 0 prototype + stability probe surface this on day 2, not day 7. Item 10 (pilot) spans High/Med/Low fit before bulk. |
| Snapshot of preserved User-Decisions misses content | Med — analyst rework lost | Item 10 documents the snapshot procedure; Item 11 follows it mechanically. |
| Dropped regex validators leave silent contract gaps | Med — bad shapes ship | New `model_setup.py` and override-registry checks in Item 7 cover the structural invariants; structured assess/review output in Item 8 covers the rest. |
| Bulk regeneration cost (LLM tokens) blows past expectations | Low — budget known | Pilot establishes per-concept cost; user is not cost-sensitive per project memory. |

---

## Timeline

**Total Effort**: ~10–14 days (Phase 0 ~2 d, Phase 1 ~6–9 d, Phase 2 ~2.5–3.5 d)

| Item | Effort | Phase | Dependencies |
|------|--------|-------|--------------|
| Item 1: E2E manual prototype | ~1 d | 0 | — |
| Item 2: Prompt-stability probe | ~0.5 d | 0 | Item 1 |
| Item 3: Critic acuity probe | ~0.5 d | 0 | Item 1 (parallel with Item 2) |
| Item 4: Library preconditions | 0.5–1 d | 1 | Item 1 |
| Item 5: Tables + sanity check | 1–1.5 d | 1 | Item 1 (parallel with Item 4) |
| Item 6: Pipeline glue | 1–1.5 d | 1 | Item 5 |
| Item 7: Helpers + validators | 1–1.5 d | 1 | Items 1, 4, 5 |
| Item 8: Prompt rework | 1–1.5 d | 1 | Items 1, 5, 6, 7 |
| Item 9: model_critic | 0.5–1 d | 1 | Items 1, 5 |
| Item 10: Explorer + pilot | 1.5–2 d | 2 | Items 4, 6, 7, 8, 9 |
| Item 11: Bulk regeneration | 1–1.5 d | 2 | Item 10 |

**Phase 0 gate**: review Item 1's findings doc before committing to Phase 1. If a key bet broke, redirect — don't just plow into the plumbing.

Items 4 and 5 can run in parallel; Items 7 and 9 can run in parallel after their deps; Item 8 is the pacing gate before pilot.

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete*

**What Went Well**: TBD
**What Could Improve**: TBD
**Surprises**: TBD

---

**Last Updated**: 2026-05-30
**Next Action**: Spec Item 1 (E2E manual prototype) — get signal on the agent-driven bets before committing to any plumbing.
