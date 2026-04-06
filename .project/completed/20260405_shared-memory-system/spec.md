# Spec: Shared Memory System

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29 15:59 PDT
**Complexity:** MEDIUM
**Branch:** design-space-explore
**Epic:** ANALYSIS-V2, Item 4

---

## Business Goals

### Why This Matters

Each concept analysis currently starts from zero cross-concept context. After 20+ analyses, the pipeline has accumulated implicit knowledge — parameter sanity ranges, common data gaps, recurring assessment findings, source quality notes — but none of it persists. The same mistakes get repeated and the same discoveries get rediscovered.

A shared memory system lets later analyses benefit from earlier ones, compounding quality over time rather than treating each concept as an island.

### Success Criteria

- [ ] After 3-5 concept analyses using memory, the pipeline avoids previously-encountered pitfalls without human prompting *(deferred — requires organic accumulation over multiple runs)*
- [x] A human can read the accumulated memory files and understand what the pipeline has learned
- [ ] Memory is useful enough that turning it off produces noticeably worse first drafts *(deferred — requires organic accumulation over multiple runs)*

### Priority

Prerequisite for Item 5 (interactive manage-concept agent). Should be built before Item 5 starts.

---

## Problem Statement

### Current State

Pipeline agents (analyze, assess, review) run with concept-specific context only: dossier, sources, exemplars, and the approved pool. There is no mechanism to carry forward cross-concept learnings like:
- "FLiBe coolant cost data is consistently sparse across IFE concepts"
- "Superconducting magnet costs vary 3x across sources — always flag confidence"
- "Assessment agent repeatedly flags missing O&M breakdown — add to cold-start checklist weight"
- "ARIES studies are the most reliable parameter source for MFE concepts"

### Desired Outcome

A lightweight, file-based memory system that pipeline agents consult before running and can write to after discovering something worth remembering. The system is designed for organic growth — no predefined taxonomy, just constrained entry format and a handler agent that manages categorization.

---

## Scope

### In Scope

1. Memory storage directory and entry format
2. Memory-handler agent definition (`.claude/agents/`)
3. Integration into the analyze agent (first consumer)
4. Read and write modes for the handler

### Out of Scope

- Semantic search / embeddings (keyword + concept tag matching only)
- Automated memory extraction from pipeline outputs (explicit save only)
- Memory pruning, expiration, or deduplication (manual curation)
- Integration into assess/review/manage-concept agents (future work, after Item 4 proves value)
- Seeding from existing analyses (accumulate organically from re-runs)

### Edge Cases & Considerations

- **Cold start**: First few analyses produce no memories and consume none. The system must add zero overhead when memory is empty.
- **Memory bloat**: Without constraints, agents will write verbose entries. Hard cap of 10 lines per entry prevents this.
- **Stale memories**: A memory about "concept X lacks data on Y" becomes false after a source addition. No automated staleness detection — human curates. Entries should be specific enough to verify.
- **Category discovery**: Categories emerge from use, not upfront taxonomy. The handler decides file placement. Early on, a single file is fine; the handler splits when a file gets unwieldy.

---

## Requirements

### Functional Requirements

> Requirements below are from user's epic description unless marked [INFERRED].

1. **FR-1**: Memory storage lives at `exploration/concept_analysis/memory/` as simple markdown files with structured entries. No database.

2. **FR-2**: Each memory entry MUST be ≤10 lines of text, timestamped (ISO 8601 date), and tagged with originating concept ID(s). This is a hard format constraint, not a guideline.

3. **FR-3**: A memory-handler agent definition at `.claude/agents/memory-handler.md` following the project's agent pattern (YAML frontmatter with name/description/tools, structured instruction body with modes, guidelines, and response format).

4. **FR-4**: The handler MUST support two modes:
   - **Read mode**: Given current context (concept ID, pipeline stage, topic keywords), return relevant memory entries. Return nothing if no relevant memories exist.
   - **Write mode**: Given a learning/insight, validate it against the entry format constraints (≤10 lines, has timestamp, has concept tag), categorize it, and append to the appropriate memory file.

5. **FR-5**: The analyze stage MUST include relevant cross-concept memories in the analysis prompt for every run (cold-start and feedback-pass modes). The pipeline script loads memories and injects them as a template variable — the memory-handler agent is NOT invoked during headless pipeline runs. The agent is for interactive sessions only.

6. **FR-6**: Categories are NOT predefined. The handler decides file placement based on content. Starting with a single file is acceptable; the handler splits files when they grow large. [INFERRED — from epic's "discover the right structure through use" and user's "design for general discovery"]

7. **FR-7**: Memory entries MUST be grep-friendly — no nested structure, no YAML within entries, no cross-references between entries. Each entry is self-contained.

### Non-Functional Requirements

- **NF-1**: Zero overhead when memory directory is empty — the analyze agent should not slow down or produce different behavior when no memories exist.
- **NF-2**: Memory files MUST be human-readable. A person should be able to open any memory file and understand every entry without tooling.

---

## Acceptance Criteria

### Core Functionality

- [x] `exploration/concept_analysis/memory/` directory exists and is writable by pipeline agents
- [x] `.claude/agents/memory-handler.md` agent definition exists with read and write modes
- [ ] Memory-handler in read mode returns relevant entries given concept + stage context *(pending interactive validation)*
- [ ] Memory-handler in read mode returns empty/nothing when no relevant memories exist *(pending interactive validation)*
- [ ] Memory-handler in write mode validates ≤10 line constraint and rejects oversized entries *(pending interactive validation)*
- [ ] Memory-handler in write mode appends entries with timestamp and concept tag *(pending interactive validation)*
- [x] Analyze agent (`analysis_v2.md`) includes relevant memories in prompt via `load_relevant_memories()`

### Format Constraints

- [x] Every memory entry is ≤10 lines
- [x] Every memory entry has an ISO 8601 date
- [x] Every memory entry has at least one concept tag
- [x] Memory files are plain markdown, grep-friendly, no nested structure

### Quality & Integration

- [x] Existing tests/pipeline behavior unchanged when memory directory is empty
- [x] Memory-handler agent follows `.claude/agents/` pattern (YAML frontmatter, tools declaration, structured body)
- [ ] After a manual test run on 1 concept, at least one meaningful memory is written *(deferred — requires interactive use)*

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 4)
- **Research:** `.project/research/20260328-pipeline-upgrade-feasibility.md`
- **Agent pattern reference:** `.claude/agents/sysmlv2-validator.md`, `.claude/agents/syside-expert.md`
- **Pipeline subagent reference:** `exploration/concept_analysis/prompt_templates/agents/source_reader.md`
- **Analysis prompt (integration target):** `exploration/concept_analysis/prompt_templates/analysis_v2.md`
- **Design:** `.project/active/shared-memory-system/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
