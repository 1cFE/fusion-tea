# Implementation Plan: Shared Memory System

**Status:** Complete
**Created:** 2026-03-29
**Last Updated:** 2026-03-29

## Source Documents
- **Spec:** `.project/active/shared-memory-system/spec.md`
- **Design:** `.project/active/shared-memory-system/design.md` ← See here for component details, matching rules, entry format, agent structure

## Implementation Strategy

**Phasing Rationale:**
Phase 1 builds the storage format and loading function (the foundation). Phase 2 wires it into the pipeline (the integration). Phase 3 adds the interactive agent (the human interface). Each phase is independently verifiable and builds on the previous one.

---

## Phase 1: Storage + Loading Function

### Goal
Create the memory directory and implement `load_relevant_memories()` with the canonical parsing/matching logic from `design.md#component-3`.

### Test Stencil (Write This First)
```python
# exploration/concept_analysis/scripts/test_memory.py
# Run: uv run python exploration/concept_analysis/scripts/test_memory.py

from pathlib import Path
import tempfile

# Import after adding to run_analysis.py
from run_analysis import load_relevant_memories

def test_empty_dir():
    """NF-1: empty dir returns empty string."""
    with tempfile.TemporaryDirectory() as d:
        assert load_relevant_memories("09-laser-ife", Path(d)) == ""

def test_nonexistent_dir():
    assert load_relevant_memories("09-laser-ife", Path("/nonexistent")) == ""

def test_concept_match():
    """Concept-specific entry matches by short ID."""
    # Create temp dir with a memory file containing test entries
    # Entry tagged "09" should match concept "09-laser-ife"
    # Entry tagged "01" should NOT match

def test_family_match():
    """Family-tagged entry matches by confinement family."""
    # Entry tagged "IFE" should match when family="IFE"
    # Entry tagged "MFE" should NOT match

def test_all_match():
    """Universal entry matches every concept."""
    # Entry tagged "all" should always match

def test_mixed_tags():
    """Entry with multiple tags: '09, IFE, all'."""
    # Should match concept 09, any IFE concept, and any concept
```

### Changes Required

**See `design.md` for:**
- Entry format → `design.md#component-1`
- Matching rules and regex → `design.md#component-3`
- Function signature and implementation steps → `design.md#component-4`

**Specific file changes:**

#### 1. Memory directory
- [x] Create `exploration/concept_analysis/memory/`
- [x] Add `.gitkeep`
- [x] Add `learnings.md` with H1 header per `design.md#component-2`

#### 2. Test file
**File:** `exploration/concept_analysis/scripts/test_memory.py` (NEW)
- [x] Implement test stencil above with concrete test entries
- [x] Run tests, verify all pass

#### 3. Loading function
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Add `MEMORY_DIR` constant near existing path constants (~line 30)
- [x] Add `_MEMORY_META_RE` compiled regex (from `design.md#component-4`)
- [x] Add `load_relevant_memories()` function (signature and steps in `design.md#component-4`)

### Validation

**Automated:**
- [x] `uv run python exploration/concept_analysis/scripts/test_memory.py` → 11/11 tests pass

**Manual:**
- [x] Write 3 test entries to `memory/learnings.md` covering: concept-specific (`09`), family (`IFE`), universal (`all`)
- [x] Call `load_relevant_memories("09-laser-ife", MEMORY_DIR, family="IFE")` → returns 2 (FLiBe + O&M; ARIES is MFE-only, correctly excluded)
- [x] Call `load_relevant_memories("01-hts-compact-tokamak", MEMORY_DIR, family="MFE")` → returns ARIES + O&M (correct)

**What We Know Works After This Phase:**
Memory files can be parsed, split into entries, and matched against concept context. Empty directory returns empty string with no overhead.

---

## Phase 2: Pipeline Integration

### Goal
Wire `load_relevant_memories()` into the analysis prompt via template variable so the analyze agent receives relevant memories on every run.

### Test Stencil (Write This First)
```bash
# Dry-run validation: run analyze on a concept, then inspect the saved prompt
# 1. With empty memory dir — prompt should NOT contain "Cross-Concept Memory"
uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 17a --max-passes 1
grep -c "Cross-Concept Memory" exploration/concept_analysis/analyses/17a-*/analysis_prompt_iter_1.md
# Expected: 0

# 2. Add a test entry, re-run with --force
# grep should find the section
# Expected: 1
```

### Changes Required

**See `design.md` for:**
- Template variable wiring → `design.md#component-4` (Template variable section)
- Template section text → `design.md#component-5`
- Placement rationale → `design.md#component-5`

**Specific file changes:**

#### 1. Pipeline script
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] In `cmd_analyze()`, add `memory_context` to `common_vars` dict (~line 1119-1138), calling `load_relevant_memories(cid, MEMORY_DIR, family=c.get("Confinement Family", ""))`

#### 2. Analysis template
**File:** `exploration/concept_analysis/prompt_templates/analysis_v2.md`
- [x] Add `{{#if memory_context}}` conditional section between Per-Source Reading Pattern (line 27) and `{{#if cold_start}}` (line 29), per `design.md#component-5`

### Validation

**Automated:**
- [x] Run analyze on one concept with empty memory dir → prompt file does NOT contain "Cross-Concept Memory" (NF-1) ✓
- [x] Add a test memory entry tagged for that concept → re-run with `--force` → prompt file DOES contain the entry text ✓

**Manual:**
- [x] Inspect `analysis_prompt_iter_1.md` — memory section at line 93, after Quality Standards (33) and Per-Source Reading (63), before Mode: Cold Start (119) ✓
- [x] Verify the `{{#if}}` / `{{/if}}` brackets don't leak into the prompt when memory is empty ✓

**What We Know Works After This Phase:**
The full pipeline path: memory files → loading function → template variable → analysis prompt. Empty memory = invisible. Present memory = correctly positioned in prompt.

---

## Phase 3: Memory-Handler Agent

### Goal
Write the `.claude/agents/memory-handler.md` agent definition with read and write modes for interactive use.

### Test Stencil (Write This First)
```
# Interactive validation — invoke agent from Claude Code session

# Read mode test (with entries from Phase 2 still in memory/):
> Use the memory-handler agent to find memories relevant to concept 09 (IFE family)
# Expected: returns matching entries

# Read mode empty test:
> Use the memory-handler agent to find memories relevant to concept 35 (no entries)
# Expected: "No relevant memories found."

# Write mode test:
> Use the memory-handler agent to save this learning:
>   Title: "Laser Driver Cost Dominates IFE LCOE"
>   Concepts: 09, 22
>   Body: "For laser-driven IFE concepts, the laser driver system typically
>   accounts for 40-60% of total capital cost..."
# Expected: entry appended to learnings.md with correct format

# Write mode rejection test:
> Use the memory-handler agent to save a 15-line entry
# Expected: rejected with "exceeds 10 line limit"
```

### Changes Required

**See `design.md` for:**
- Agent structure and modes → `design.md#component-6`
- Validation rules → `design.md#component-6` (Write Mode section)
- Response formats → `design.md#component-6`
- Matching rules (shared with pipeline) → `design.md#component-3`

**Specific file changes:**

#### 1. Agent definition
**File:** `.claude/agents/memory-handler.md` (NEW)
- [x] YAML frontmatter: name, description, tools (Read, Write, Grep, Glob)
- [x] Role description and memory directory path
- [x] Read mode instructions referencing canonical matching rules
- [x] Write mode instructions with format validation (≤10 lines, required fields)
- [x] Response formats for both modes
- [x] DO/DON'T guidelines

### Validation

**Manual:** (agent definition is for interactive use — validation requires invoking from a Claude Code session)
- [ ] Invoke agent in read mode with matching context → correct entries returned
- [ ] Invoke agent in read mode with no matches → "No relevant memories found."
- [ ] Invoke agent in write mode with valid entry → appended correctly, format verified
- [ ] Invoke agent in write mode with oversized entry → rejected
- [ ] Inspect written entry — has H2 header, Date, Concepts, body ≤7 lines

**What We Know Works After This Phase:**
Complete system: pipeline reads memories automatically, humans read/write interactively via agent. Format constraints enforced on write. All acceptance criteria from spec met.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Regex edge cases — test stencil covers malformed entries, entries without metadata, empty files
- **Phase 2**: Template conditional leakage — manual prompt inspection verifies `{{#if}}` works correctly with empty string
- **Phase 3**: Agent scope — agent is for interactive sessions only, pipeline has no dependency on it

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Created `exploration/concept_analysis/memory/` with `.gitkeep` and `learnings.md` (3 sample entries)
- Added `MEMORY_DIR` constant at `run_analysis.py:38`
- Added `_MEMORY_META_RE` regex and `load_relevant_memories()` at `run_analysis.py:878-930`
- Created `test_memory.py` with 11 tests covering: empty dir, nonexistent dir, empty file, concept match, no match, family match (MFE + IFE), universal match, case-insensitive family, multiple files, entries without metadata
**Issues:** None
**Deviations:**
- Plan expected `load_relevant_memories("09-laser-ife", ..., family="IFE")` to return all 3 entries, but ARIES is tagged `MFE` not `IFE`, so correctly returns 2. Plan's expected output was wrong; implementation is correct.
- Plan expected `("01-hts-compact-tokamak", ..., family="MFE")` to return "only the `all` entry" but it correctly returns ARIES (MFE match) + O&M (all match) = 2 entries. Plan's expected output was wrong; implementation is correct.
- Test stencil expanded from 6 outlined tests to 11 concrete tests for better coverage.

### Phase 2 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Added `memory_context` loading + variable to `common_vars` in `cmd_analyze()` at `run_analysis.py:1119-1138`
- Added `{{#if memory_context}}` conditional section to `analysis_v2.md` between Per-Source Reading Pattern and `{{#if cold_start}}`
**Issues:** None
**Deviations:** None — implementation matched design exactly.

### Phase 3 Completion
**Completed:** 2026-03-29
**Actual Changes:**
- Created `.claude/agents/memory-handler.md` with YAML frontmatter (name, description, tools: Read/Write/Grep/Glob), read mode with canonical matching rules, write mode with validation (≤10 lines, required fields, duplicate check), response formats, DO/DON'T guidelines
**Issues:** None
**Deviations:** None — agent manual validation deferred to interactive session (cannot be automated).

---

**Status**: Complete (all 3 phases implemented, agent manual validation pending interactive session)
