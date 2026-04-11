# Design: Shared Memory System

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29 16:15 PDT
**Updated:** 2026-03-29 16:15 PDT
**Branch:** design-space-explore

## Overview

A file-based cross-concept memory system with two interfaces: a Python function in `run_analysis.py` that loads relevant memories into pipeline prompts, and a `.claude/agents/` agent definition for interactive read/write from human sessions.

## Related Artifacts

- **Spec:** `.project/active/shared-memory-system/spec.md`
- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 4)
- **Research:** `.project/research/20260328-pipeline-upgrade-feasibility.md`
- **Agent pattern reference:** `.claude/agents/sysmlv2-validator.md`
- **Pipeline subagent reference:** `exploration/concept_analysis/prompt_templates/agents/source_reader.md`
- **Analysis template:** `exploration/concept_analysis/prompt_templates/analysis_v2.md`
- **Pipeline script:** `exploration/concept_analysis/scripts/run_analysis.py`

## Research Findings

### Pipeline Prompt Architecture

The analysis template (`analysis_v2.md`) uses three mechanisms from `fill_template()` (`run_analysis.py:502`):
1. **File inclusions** `{{@config/analysis_goals.md}}` — inlines external markdown
2. **Conditionals** `{{#if cold_start}}...{{/if}}` — mode-based sections
3. **Variable substitution** `{{variable}}` — string replacement

The analysis prompt already has a "Cross-Concept Reuse" section at the bottom (line 166) that provides approved prior analyses as reading material. Memory context fits naturally as a sibling section.

### cmd_analyze() Integration Points

`cmd_analyze()` (`run_analysis.py:1019-1216`) builds common template variables at lines 1062-1075, then builds mode-specific prompts. The relevant hookpoint is **before prompt construction** — load memories, add to common_vars, let the template's conditional section handle display.

The assessment loop (lines 1136-1215) iterates: assess → check verdict → feedback pass. Memory is read once at the start (before cold-start), not re-read between iterations.

### Existing Agent Pattern

`.claude/agents/*.md` files use YAML frontmatter:
```yaml
---
name: agent-name
description: One-line description for triggering.
tools: Tool1, Tool2, Tool3
---
```

Followed by structured markdown: role description, capability tiers/modes, workflow patterns, response format, guidelines (DO/DON'T).

The pipeline's own subagent (`prompt_templates/agents/source_reader.md`) is simpler — just inline instructions that get pasted into the main prompt via `{{@agents/source_reader.md}}`. No YAML frontmatter, no tool declarations.

### Key Insight: Two Interfaces, Not One

The pipeline (headless `claude -p`) and interactive sessions have different needs:

| Need | Pipeline | Interactive |
|------|----------|-------------|
| Read memories | Deterministic, zero-cost when empty | Smart retrieval, conversational |
| Write memories | Not needed (pipeline doesn't learn) | Essential (human captures insights) |
| Reliability | Must not fail or add latency | Best-effort is fine |

This means: **script-side loading** for pipeline reads, **agent invocation** for interactive read/write. One storage format serves both.

## Proposed Design

### Component 1: Memory Entry Format

Each memory entry is a self-contained markdown block:

```markdown
## [Descriptive Title]
Date: 2026-03-29 | Concepts: 09, 14, 22

Body text — the actual insight, learning, or pattern.
Specific enough to be verifiable. Actionable enough to
change behavior. 3-7 lines typical.
```

**Format rules:**
- H2 header with descriptive title (enables `grep "^## "` to list all entries)
- Metadata line: ISO 8601 date + concept IDs (short numeric form, or `all` for universal)
- Blank line, then body text
- Total entry: ≤10 lines (header + metadata + blank + body)
- Entries separated by a blank line between closing body and next H2
- No YAML, no nested headers, no cross-references between entries

**Concept tagging convention:**
- Use short numeric IDs: `01`, `09`, `22` (not full slug)
- Use `all` for insights that apply to every concept
- Use family tags for confinement-class insights: `MFE`, `IFE`, `MIF`

Example entries:

```markdown
## ARIES Studies Are Best Parameter Source for MFE Concepts
Date: 2026-03-29 | Concepts: MFE

ARIES-AT and ARIES-CS studies provide the most complete parameter sets
for magnetic confinement cost modeling — plant-level CAS breakdowns,
thermal efficiency targets, and magnet cost estimates. Prefer these over
individual paper estimates when available. Cross-check against PROCESS
code outputs where overlap exists.

## FLiBe Coolant Cost Data Is Consistently Sparse
Date: 2026-03-29 | Concepts: 09, 14, 22, IFE

IFE concepts using FLiBe as primary coolant/breeder consistently lack
cost data for coolant inventory and processing. Flag as [estimated] with
high uncertainty. The HYLIFE-II report (Moir 1994) is the only source
with FLiBe cost estimates but uses 1994 dollars.

## Assessment Repeatedly Flags Missing O&M Breakdown
Date: 2026-03-29 | Concepts: all

The assessment agent flags missing O&M cost breakdown (fixed vs variable,
scheduled maintenance, unplanned outage costs) in >80% of first-pass
analyses. Cold-start analyses should include a placeholder O&M subsection
in Section 3 even when source data is sparse, to avoid a guaranteed
feedback finding.
```

### Component 2: Memory File Organization

**Starting state:** A single file `exploration/concept_analysis/memory/learnings.md` with an H1 header:

```markdown
# Cross-Concept Learnings

[entries accumulate here]
```

**Growth rule:** When a file exceeds ~30 entries, the memory-handler agent splits it by theme. Possible split targets (discovered, not predetermined):
- `source_quality.md` — notes about which sources are reliable/sparse
- `parameter_patterns.md` — sanity ranges, common estimation approaches
- `assessment_patterns.md` — recurring findings, checklist gaps
- `modeling_patterns.md` — what works/doesn't in cost models

The handler decides when and how to split. The pipeline's `load_relevant_memories()` function scans all `*.md` files in the directory, so splits are transparent.

**Directory:** `exploration/concept_analysis/memory/`

### Component 3: Matching Rules (Canonical, Shared by Both Interfaces)

Both the pipeline function and the memory-handler agent use the same matching rules. These are the authoritative definition — if the implementations drift, this section is the tiebreaker.

**Metadata line format:** `Date: YYYY-MM-DD | Concepts: TAG[, TAG]*`

**Parsing the metadata line:**
- Match with regex: `^Date:\s*(\d{4}-\d{2}-\d{2})\s*\|\s*Concepts:\s*(.+)$`
- The `Concepts` capture group is a comma-separated list of tags, whitespace-trimmed
- Each tag is one of: a short numeric concept ID (`09`), a family tag (`MFE`, `IFE`, `MIF`), or the literal `all`

**An entry matches a concept if any of these are true:**
1. The entry's tags contain the concept's short numeric ID (e.g., `09` from `09-laser-ife`)
2. The entry's tags contain the concept's confinement family (e.g., `IFE`)
3. The entry's tags contain `all`

**Entry splitting:** Files are split into entries on the `^## ` pattern (H2 at start of line). Everything from one `## ` to the next (or EOF) is one entry.

### Component 4: Pipeline Integration (Script-Side Loading)

New function in `run_analysis.py`:

```python
MEMORY_DIR = CONCEPT_ANALYSIS_DIR / "memory"

# Regex for metadata line: "Date: 2026-03-29 | Concepts: 09, IFE, all"
_MEMORY_META_RE = re.compile(
    r"^Date:\s*\d{4}-\d{2}-\d{2}\s*\|\s*Concepts:\s*(.+)$", re.MULTILINE
)

def load_relevant_memories(
    concept_id: str, memory_dir: Path, family: str = "",
) -> str:
    """Load memory entries relevant to a concept.

    Args:
        concept_id: Full concept ID, e.g. "09-laser-ife". Short ID
            extracted as the leading numeric segment.
        memory_dir: Path to the memory directory.
        family: Confinement family tag, e.g. "IFE". Empty string if unknown.

    Returns:
        Matched entries as a markdown string, or "" if none found
        or memory dir doesn't exist.
    """
```

**Implementation steps:**
1. If `memory_dir` doesn't exist or contains no `*.md` files → return `""` (NF-1)
2. Extract short ID: `concept_id.split("-")[0]` (e.g., `"09"` from `"09-laser-ife"`)
3. Build match set: `{short_id, family.upper(), "all"} - {""}` (drop empty strings)
4. For each `*.md` file, split content into entries on `^## ` boundaries
5. For each entry, extract tags via `_MEMORY_META_RE`; split on `,` and strip whitespace
6. Entry matches if `entry_tags & match_set` is non-empty
7. Return matched entries joined with `\n\n`

**Confinement family lookup:** `cmd_analyze()` has access to the concept row (`c` dict) at line 1040. Extract `c.get("Confinement Family", "")`.

**Template variable:** Add `"memory_context"` to common_vars (line 1062-1075):

```python
memory_context = load_relevant_memories(
    cid, MEMORY_DIR, family=c.get("Confinement Family", ""),
)
common_vars = {
    # ... existing vars ...
    "memory_context": memory_context,
}
```

### Component 5: Analysis Template Update

Add a new conditional section to `analysis_v2.md`, placed **before** the mode-specific sections (between the Per-Source Reading Pattern and `{{#if cold_start}}`). This makes memory available in all modes.

```markdown
{{#if memory_context}}
## Cross-Concept Memory

The following insights were captured from prior concept analyses. Use them
to avoid known pitfalls and apply established patterns. Do not cite these
memories as sources — they are guidance, not evidence. Verify any specific
claims against the actual source documents.

{{memory_context}}
{{/if}}
```

**Placement rationale:** Before mode-specific instructions so the agent has memory context when reading sources and writing the analysis. After quality standards so it knows citation rules apply to sources, not memories.

### Component 6: Memory-Handler Agent Definition

**File:** `.claude/agents/memory-handler.md`
**Tools:** Read, Write, Grep, Glob

The agent operates in two modes, determined by the prompt it receives:

#### Read Mode

Invoked when a caller needs relevant memories for a given context. The agent follows the canonical matching rules from Component 3:
1. Globs `exploration/concept_analysis/memory/*.md`
2. Splits files into entries on `^## ` boundaries
3. Parses each entry's `Date: ... | Concepts: ...` metadata line
4. Matches entries where tags intersect with {concept short ID, family, "all"}
5. Returns matched entries as formatted text

**Response format (read mode):**
```
## Relevant Memories

[entries, or "No relevant memories found."]
```

#### Write Mode

Invoked when a caller wants to save a new learning. The agent:
1. Receives the insight text, concept ID(s), and date
2. Validates: ≤10 lines, has required fields
3. Reads existing memory files to check for duplicates or related entries
4. Appends to the most appropriate file (or creates a new one if splitting)
5. Confirms what was written and where

**Validation rules (enforced by agent):**
- Entry must have H2 header with descriptive title
- Entry must have `Date:` and `Concepts:` metadata line
- Body must be ≤7 lines (header + metadata + blank = 3, so 7 body lines = 10 total)
- Body must be specific and actionable, not vague
- Reject entries that duplicate existing memories (suggest updating instead)

**Response format (write mode):**
```
## Memory Saved

**File:** memory/learnings.md
**Entry:** [title]
**Concepts:** [tags]
```

### Component 7: Write Path

Memories enter the system through three paths:

1. **Interactive sessions** (primary path): A human using `/manage-concept` or a regular Claude session invokes the memory-handler agent to save an insight discovered during analysis review. This is the expected main path.

2. **Manual curation**: A human directly edits memory files, following the entry format. The format is simple enough that no tooling is required.

3. **Assessment findings** (future, not in this item): The assessment agent could flag recurring patterns as memory candidates. Not implemented now — mentioned for design awareness.

The pipeline itself (headless `claude -p` runs) does NOT write memories. Writing requires human judgment about what's worth remembering.

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Memory entries are too vague to be actionable | Low value, wasted context budget | Agent validates "specific and actionable" on write; ≤10 line cap forces precision |
| Stale memories mislead analysis | Wrong parameter ranges, false confidence | Entries are specific enough to verify; human curates; agent instruction says "verify against sources" |
| Too many memories match, bloating the prompt | Context budget pressure | Start with one file, organic growth; concept-specific matching limits results; can add a cap (e.g., top 10 entries) if needed |
| Agent splits files poorly | Awkward organization | Low stakes — files can be manually reorganized; grep still finds everything |
| `claude -p` can't find `.claude/agents/` from `exploration/concept_analysis/` CWD | Agent not available in pipeline context | Agent is for interactive use only; pipeline uses script-side loading, no agent dependency |

## Integration Strategy

### What Changes

| File | Change |
|------|--------|
| `exploration/concept_analysis/scripts/run_analysis.py` | Add `MEMORY_DIR` constant, `load_relevant_memories()` function, add `memory_context` to common_vars |
| `exploration/concept_analysis/prompt_templates/analysis_v2.md` | Add `{{#if memory_context}}` section between Per-Source Reading Pattern and mode sections |
| `.claude/agents/memory-handler.md` | New file — agent definition |
| `exploration/concept_analysis/memory/` | New directory — created empty, with `.gitkeep` |

### What Doesn't Change

- Assessment prompt (`assessment.md`) — does not read memories
- Review prompt — does not read memories
- `fill_template()` — already supports `{{#if}}` conditionals, no changes needed
- `invoke_claude()` — no changes
- Config files in `prompt_templates/config/` — no changes

### Ordering

1. Create memory directory + `.gitkeep`
2. Write memory-handler agent definition
3. Add `load_relevant_memories()` to `run_analysis.py`
4. Add `{{#if memory_context}}` section to `analysis_v2.md`
5. Test: run `cmd_analyze` on a concept with empty memory dir → no change in behavior
6. Test: manually add a memory entry → verify it appears in the analysis prompt

## Validation Approach

### Automated

- Run `cmd_analyze` on one concept with empty memory directory — verify identical behavior to current (NF-1)
- Run `cmd_analyze` on one concept after manually adding a relevant memory entry — verify it appears in the saved prompt file (`analysis_prompt_iter_1.md`)

### Manual

- Add 2-3 test memory entries covering different matching patterns (concept-specific, family-level, universal)
- Run analysis for a concept that should match some but not all entries
- Inspect the saved prompt to verify correct entries were included and non-matching entries excluded
- Invoke memory-handler agent interactively to verify read and write modes work
- Verify written entries conform to format constraints

### Success Criteria (from spec)

- [ ] Empty memory dir → zero overhead, identical behavior
- [ ] Memory entries appear in analysis prompts when relevant
- [ ] Memory-handler agent reads and writes correctly
- [ ] All entries conform to ≤10 line, timestamped, concept-tagged format
- [ ] After 1 manual test run, at least one meaningful memory could be written

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement`
