# Spec: Concept Landscape Context for Analysis Pipeline

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-06T10:00:00-07:00
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

The analysis pipeline asks agents to "name 2-3 nearest-neighbor concepts for comparison" (assessment checklist, analysis goal #1), but provides no cross-concept catalog. The agent can only discover neighbors from its own sources, the dossier, approved prior analyses, or training data. This works when a concept's sources naturally reference neighbors (concept 09's stellarator papers discuss ARIES-CS and W7-X), but fails when they don't (concept 07's MagLIF/Sandia papers don't discuss General Fusion's pneumatic MTF). The result is shallow or unsourced nearest-neighbor comparisons that the assessor can't verify.

Separately, the pipeline status codes `D` (drafted) and `M` (model-setup) are vestigial — the iterative loop now runs analysis + model-setup together each iteration, making them indistinguishable in practice. The actual progression signal is iteration count.

### Success Criteria

- [ ] Every analysis agent invocation receives a complete concept catalog with taxonomy properties and pipeline status
- [ ] Every assessment agent invocation receives the same catalog, enabling neighbor correctness verification (not just presence)
- [ ] Status codes reflect the actual pipeline lifecycle: `I{N}` replaces `D` and `M`
- [ ] All status consumers (CLI `cmd_status`, landscape function, any other callers of `get_concept_state`) use the new codes consistently

### Priority

High — this is a quality bottleneck for batch analysis runs. Directly blocks accurate nearest-neighbor positioning for concepts whose sources are domain-narrow.

---

## Problem Statement

### Current State

- `table.csv` (38 concepts × 22 design columns) exists and is loaded by `lib/concepts.py` for orchestration, but is **never injected into any prompt**
- The analysis agent sees: concept-specific sources, dossier, approved analysis file paths, cross-concept memories, exemplars — no concept list or taxonomy
- The assessment agent sees: only the analysis text and model output — cannot verify neighbor selection at all
- Status codes include `D` (drafted) and `M` (model-setup) which are no longer distinct stages in the loop-based pipeline
- `get_concept_state()` distinguishes D vs M by checking `model_setup.py` existence, which is meaningless when model-setup runs every iteration

### Desired Outcome

- Both agents receive an inline markdown landscape showing all 38 concepts with their taxonomy properties, grouped and prioritized by pipeline maturity
- Approved concepts are highlighted as the primary cross-reference pool; in-progress concepts with multiple iterations are still valuable for positioning
- Status codes accurately reflect the loop-based lifecycle

---

## Scope

### In Scope

1. **New function**: `build_concept_landscape()` in `lib/memory.py` (or new `lib/landscape.py`) — produces inline markdown from taxonomy + status
2. **Status code simplification**: Modify `get_concept_state()` to return `iterating` (with iteration count available separately) instead of `drafted` / `model-setup`
3. **CLI update**: `cmd_status` adopts new codes — `I{N}` replaces `D` and `M`
4. **Prompt injection**: Add `concept_landscape` to `_build_common_vars()`, reference in `analysis_v2.md` and `assessment.md`
5. **All status consumers**: Any code that calls `get_concept_state()` or uses the old state strings MUST be updated

### Out of Scope

- Pre-computing nearest-neighbor similarity scores (the agent does the matching)
- Changing the dossier pipeline or Phase 1a artifacts
- Changing the `approved_analyses` file-path mechanism (stays as-is for deep reading)
- Filtering taxonomy columns (all 22 columns included)

### Edge Cases & Considerations

- Concepts with 0 iterations but an `analysis.md` (e.g., from pre-loop era migration) — should map to `I0` or `I1` depending on whether content exists
- Concepts whose model-setup failed on first iteration — still `I1` (iteration completed, model failed is a detail)
- Stale marker (`*` suffix) — SHOULD be preserved in the new scheme
- Landscape size: 38 rows × 22 columns + status info inline in every prompt — estimate ~8-10KB. Acceptable for prompt budget.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

1. **FR-1**: A `build_concept_landscape()` function MUST produce an inline markdown summary of all concepts combining taxonomy table columns (all 22) with pipeline status
2. **FR-2**: The landscape MUST group concepts by status tier — approved first (highest priority for cross-referencing), then in-progress (ordered by iteration count descending), then not-yet-analyzed
3. **FR-3**: In-progress concepts MUST show iteration count (e.g., `I7`, `I3`) so the agent can gauge analysis maturity
4. **FR-4**: The landscape MUST be injected inline (not as a file path) into both the analysis prompt (`analysis_v2.md`) and the assessment prompt (`assessment.md`)
5. **FR-5**: `get_concept_state()` MUST collapse `drafted` and `model-setup` into a single `iterating` state. The iteration count is available from `get_iteration_summary()`.
6. **FR-6**: `cmd_status` CLI output MUST use `I{N}` in place of `D` and `M`, where N is the iteration count
7. **FR-7**: ALL consumers of `get_concept_state()` that reference `drafted` or `model-setup` MUST be updated to use the new `iterating` state
8. **FR-8**: [INFERRED] The `approved_analyses` file-path list in the analysis prompt MUST remain unchanged — the landscape complements it (catalog for positioning) rather than replacing it (file paths for deep reading)
9. **FR-9**: [INFERRED] The landscape for a given concept SHOULD exclude that concept's own row (the agent already knows its own identity)

---

## Acceptance Criteria

### Core Functionality

- [ ] `build_concept_landscape()` returns a markdown string containing all 38 concepts (minus the current one) with taxonomy columns and status
- [ ] Concepts are grouped: approved → in-progress → gap-checked → not-started
- [ ] In-progress concepts show `I{N}` with iteration count
- [ ] The landscape appears inline in cold-start analysis prompts
- [ ] The landscape appears inline in feedback-pass analysis prompts
- [ ] The landscape appears inline in assessment prompts
- [ ] `cmd_status` output shows `I{N}` instead of `D` or `M`
- [ ] No code references the old `drafted` or `model-setup` state strings

### Quality & Integration

- [ ] Existing tests continue to pass
- [ ] `--dry-run` prompts include the landscape (verifiable without running Claude)
- [ ] Landscape generation adds negligible time (<100ms for 38 concepts)

---

## Related Artifacts

- **Research:** `.project/research/20260406-nearest-neighbor-cross-concept-bug.md`
- **Design:** `.project/active/concept-landscape-context/design.md` (to be created)
- **Key files:**
  - `exploration/concept_analysis/scripts/lib/state.py` — `get_concept_state()`, `get_iteration_summary()`
  - `exploration/concept_analysis/scripts/lib/memory.py` — approved/exemplar discovery
  - `exploration/concept_analysis/scripts/run_analysis.py` — `_build_common_vars()`, `cmd_status()`
  - `exploration/concept_analysis/prompt_templates/analysis_v2.md` — analysis prompt
  - `exploration/concept_analysis/prompt_templates/assessment.md` — assessment prompt
  - `exploration/concept_analysis/scripts/lib/paths.py` — `TABLE_PATH`

---

**Next Steps:** After approval, proceed to `/_my_design`
