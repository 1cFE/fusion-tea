# Research: manage-concept Command vs Actual Pipeline

**Date**: 2026-04-19
**Topic**: Audit of `.claude/commands/manage-concept.md` against the actual concept analysis pipeline implementation
**Sources**: `exploration/concept_analysis/README.md`, `scripts/run_analysis.py`, `scripts/lib/state.py`, actual `status` output, filesystem inspection

## Summary

The `manage-concept.md` command has significant drift from the actual pipeline implementation. It was likely written for an earlier version and not updated after the loop refactor, state.py changes, and command removals.

## Findings

### 1. CRITICAL: State Detection is Wrong

**Command says** (line 38-46): States are `approved`, `synthesized`, `reviewed`, `model-setup`, `drafted`, `gap-checked`, `not-started`.

**Reality** (`state.py:11-15`): States are `approved`, `synthesized`, `reviewed`, **`iterating`**, `gap-checked`, `not-started`.

- There is NO `model-setup` or `drafted` state — both map to `iterating`
- The status display uses `I{N}` with iteration count (e.g., `I7`), not `M` or `D`
- The status output also includes `Extr` (extraction state) and `Iterations` columns

**Impact**: Phase 1 content loading, Phase 2 state presentation, and all Mode selection (A/B/C/D) key off these wrong state names.

### 2. CRITICAL: Pipeline Stage Reference Lists Non-Existent Commands

**Command says** (line 330-346): `build-visuals` and `update-analysis --sources <name>` are valid commands.

**Reality**: The dispatch table has exactly 10 commands: `list`, `status`, `gap-check`, `analyze`, `model-setup`, `review`, `address-review`, `synthesize`, `approve`, `add-source`. Neither `build-visuals` nor `update-analysis` exists.

### 3. IMPORTANT: Status Display Format is Wrong

**Command says** (line 318-322):
```
Legend: A=approved  S=synthesized  R=reviewed  M=model-setup  D=drafted  G=gap-checked  -=not-started  *=stale
```

**Reality**:
```
Legend: A=approved  S=synthesized  R=reviewed  I{N}=iterating(N iterations)  G=gap-checked  -=not-started  *=stale downstream  E=extracted  E*=extraction stale
```

### 4. IMPORTANT: Change Request / Change Log Protocols Are Aspirational

**Command describes** (lines 197-268): Detailed protocols for `change_requests.md` with F-N entries and `change_log.md` as audit trail.

**Reality**: Zero concepts have `change_requests.md` or `change_log.md` files. The actual feedback mechanism is:
- In-loop: `iter-N/feedback.md` from the assess step
- Cross-loop: `--feedback PATH` flag on `analyze` (exists but rarely used manually)
- Audit trail: `iter-N/verdict.json` with structured iteration records

The change_requests workflow isn't wrong per se (--feedback works), but it describes a manual workflow that nobody uses. The actual workflow is the autonomous quality loop.

### 5. IMPORTANT: Missing Key Flags

The Pipeline Stage Reference table doesn't mention:
- `--resume` — continue from last iteration
- `--add-passes N` — run N additional passes per concept
- `--research` — enable autonomous source acquisition
- `--max-passes` — control iteration count
- `--max-research-searches` / `--max-research-extractions` — research cost control

These are central to daily usage.

### 6. MINOR: Mode A ("Early Vetting") references wrong states

**Command says**: Mode A activates for `drafted` or `model-setup` states.

**Reality**: Both of these are `iterating`. Mode A should activate for `iterating` state (concept has analysis.md but no review/synthesis).

### 7. MINOR: Explorer/extraction state not surfaced

The actual status output includes extraction state (`E`, `E*`), but manage-concept doesn't know about the concept explorer or extraction pipeline at all.

### 8. MINOR: Stale detection is incomplete

Command checks `model_setup.py` line 1 and frontmatter `Stale: true`. Reality also tracks explorer JSON staleness via `.json.stale` marker files (`state.py:93-101`).

## What's Correct

- Phase 3 memory loading (file exists, tag format matches)
- review.md PA-N decision editing workflow
- Source path pattern (`knowledge/concept_research/<id>/iter-*/sources/*.md`)
- Cross-concept comparison approach (reading other concepts' artifacts)
- "What NOT to Edit Directly" rules (analysis.md, model_setup.py, synthesis.md)
- General confirmation requirements

## Recommendation

The command needs a significant rewrite to:
1. Replace all state names with actual ones (`iterating` instead of `drafted`/`model-setup`)
2. Remove `build-visuals` and `update-analysis` from the pipeline reference
3. Update status display format
4. Either remove change_requests/change_log protocols or mark them as optional manual workflow
5. Add `--resume`, `--add-passes`, `--research` to pipeline reference
6. Update Mode A trigger to `iterating` state
7. Add extraction state awareness
