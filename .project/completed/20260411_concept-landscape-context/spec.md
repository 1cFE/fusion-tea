# Spec: Concept Landscape Context for Analysis Pipeline

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-06T10:00:00-07:00
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

The analysis pipeline asks agents to "name 2-3 nearest-neighbor concepts for comparison" (assessment checklist, analysis goal #1), but provides no cross-concept catalog. The agent can only discover neighbors from its own sources, the dossier, approved prior analyses, or training data. This works when a concept's sources naturally reference neighbors (concept 09's stellarator papers discuss ARIES-CS and W7-X), but fails when they don't (concept 07's MagLIF/Sandia papers don't discuss General Fusion's pneumatic MTF). The result is shallow or unsourced nearest-neighbor comparisons that the assessor can't verify.

Separately, the pipeline status codes `D` (drafted) and `M` (model-setup) are vestigial — the iterative loop now runs analysis + model-setup together each iteration, making them indistinguishable in practice. The actual progression signal is iteration count.

Additionally, the concept explorer extraction (`extract_explorer_data.py`) is not tracked as a pipeline stage. It only requires `analysis.md` and/or `model_setup.py` — NOT review, synthesis, or approval. This means any concept with at least one completed iteration is extractable, but there's no visibility into which concepts have been extracted, and no staleness propagation when the analysis is updated post-extraction.

### Success Criteria

- [ ] Every analysis agent invocation receives a complete concept catalog with taxonomy properties and pipeline status
- [ ] Every assessment agent invocation receives the same catalog, enabling neighbor correctness verification (not just presence)
- [ ] Status codes reflect the actual pipeline lifecycle: `I{N}` replaces `D` and `M`
- [ ] All status consumers (CLI `cmd_status`, landscape function, any other callers of `get_concept_state`) use the new codes consistently
- [ ] Extraction is tracked as an orthogonal status flag — visible in `cmd_status` and the landscape, with staleness propagation when analysis updates post-extraction

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
- Explorer extraction (`extract_explorer_data.py`) is invisible to the pipeline — no status tracking, no staleness propagation. Only requires `analysis.md` + `model_setup.py` (confirmed: does NOT read review, synthesis, or approval artifacts). Currently 3 concepts extracted (01, 07, 08) out of 18 that are extractable

### Desired Outcome

- Both agents receive an inline markdown landscape showing all 38 concepts with their taxonomy properties, grouped and prioritized by pipeline maturity
- Approved concepts are highlighted as the primary cross-reference pool; in-progress concepts with multiple iterations are still valuable for positioning
- Status codes accurately reflect the loop-based lifecycle

---

## Scope

### In Scope

1. **New function**: `build_concept_landscape()` in `lib/memory.py` (or new `lib/landscape.py`) — produces inline markdown from taxonomy + status
2. **Status code simplification**: Modify `get_concept_state()` to return `iterating` (with iteration count available separately) instead of `drafted` / `model-setup`
3. **Extraction as orthogonal status flag**: Track whether explorer JSON exists for a concept and whether it's stale relative to `analysis.md` / `model_setup.py`
4. **Staleness propagation for extraction**: `propagate_staleness()` marks explorer JSON as stale when analysis updates
5. **CLI update**: `cmd_status` adopts new codes — `I{N}` replaces `D` and `M`, shows extraction flag
6. **Prompt injection**: Add `concept_landscape` to `_build_common_vars()`, reference in `analysis_v2.md` and `assessment.md`
7. **All status consumers**: Any code that calls `get_concept_state()` or uses the old state strings MUST be updated

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
- Extraction staleness: explorer JSON at `concept_explorer/data/{id}.json` is cross-pipeline — `propagate_staleness()` in the analysis pipeline needs to know about the explorer data path. This creates a coupling between the two pipelines that should be minimal (path knowledge only).
- Extraction can happen at any stage from `I1` onward — it's not gated on review/synthesis/approval

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
10. **FR-10**: Extraction MUST be tracked as an orthogonal flag on concept status — a concept at any stage from `I1` onward MAY have extraction done or not done
11. **FR-11**: `propagate_staleness()` MUST mark the explorer JSON (`concept_explorer/data/{id}.json`) as stale when analysis or model artifacts change. The staleness mechanism for JSON files SHOULD use a sidecar file or similar approach (JSON files don't have frontmatter).
12. **FR-12**: `cmd_status` MUST show extraction status (e.g., `E` flag or column) alongside the pipeline stage
13. **FR-13**: The landscape summary MUST include extraction status per concept so the user can see what needs extraction for the explorer UX

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

### Extraction Tracking

- [ ] `cmd_status` shows extraction status per concept (extracted, stale, or not extracted)
- [ ] `propagate_staleness()` marks explorer JSON as stale when analysis/model changes
- [ ] Landscape includes extraction status per concept
- [ ] Extraction is gatable from `I1` onward (not gated on review/synthesis/approval)

### Quality & Integration

- [ ] Existing tests continue to pass
- [ ] `--dry-run` prompts include the landscape (verifiable without running Claude)
- [ ] Landscape generation adds negligible time (<100ms for 38 concepts)

---

## Related Artifacts

- **Research:** `.project/research/20260406-nearest-neighbor-cross-concept-bug.md`
- **Design:** `.project/active/concept-landscape-context/design.md` (to be created)
- **Key files:**
  - `exploration/concept_analysis/scripts/lib/state.py` — `get_concept_state()`, `get_iteration_summary()`, `propagate_staleness()`
  - `exploration/concept_analysis/scripts/lib/memory.py` — approved/exemplar discovery
  - `exploration/concept_analysis/scripts/lib/concepts.py` — `resolve_concepts()` uses `get_concept_state()` with `target_state` filtering
  - `exploration/concept_analysis/scripts/run_analysis.py` — `_build_common_vars()`, `cmd_status()`, `cmd_model_setup()` (uses `target_state="model-setup"`)
  - `exploration/concept_analysis/prompt_templates/analysis_v2.md` — analysis prompt
  - `exploration/concept_analysis/prompt_templates/assessment.md` — assessment prompt
  - `exploration/concept_analysis/scripts/lib/paths.py` — `TABLE_PATH`
  - `exploration/concept_explorer/extract_explorer_data.py` — extraction script (reads `analysis.md` + `model_setup.py`, writes JSON to `data/`)
  - `exploration/concept_explorer/data/` — extracted JSON files, staleness target

---

**Next Steps:** After approval, proceed to `/_my_design`
