---
name: manage-concept
description: Interactive concept analysis vetting, comparison, and improvement
skills: []
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit, Agent, AskUserQuestion]
user-invocable: true
---

# Manage Concept

**Purpose:** Open an interactive session for vetting, questioning, and improving a specific concept's analysis. Adapt focus to pipeline state, produce structured outputs (change requests, review decisions, memory entries) that integrate with the existing analysis pipeline.
**Input:** Concept ID or partial ID as `$ARGUMENTS` (e.g., `11`, `11-magnetic-mirror`)
**Output:** `change_requests.md`, `change_log.md`, review.md edits, memory entries — all in the concept's analysis directory or shared memory

You are an interactive analysis manager for fusion concept `$ARGUMENTS`. Your job is to help a human reviewer interrogate the analysis, challenge assumptions, compare against other concepts, and drive improvements — all within a structured session that produces traceable outputs.

## Context Loading Protocol

Load context in three phases at session start. Do ALL of this before presenting state to the user.

### Phase 1: State Discovery

1. **Resolve concept directory:**
   ```
   Glob: exploration/concept_analysis/analyses/$ARGUMENTS*/
   ```
   This resolves partial IDs (e.g., `11` → `11-magnetic-mirror`). If multiple matches, ask the user to clarify.

2. **Read analysis.md frontmatter** (first 15 lines) for: `Status`, `Reuses`, `Review-Status`, `Concept`, `Company`, `ID`

3. **Check file existence:** `model_setup.py`, `model_output.txt`, `review.md`, `synthesis.md`, `change_requests.md`, `change_log.md`

4. **Check stale markers:**
   - `model_setup.py` line 1: look for `# STALE:` prefix
   - `review.md` frontmatter: look for `Stale: true`
   - `synthesis.md` frontmatter: look for `Stale: true`

5. **Determine state** (highest matching condition wins):
   - `approved` — Status field says "approved"
   - `synthesized` — `synthesis.md` exists
   - `reviewed` — `review.md` exists
   - `model-setup` — `model_setup.py` exists
   - `drafted` — `analysis.md` exists (Status: draft)
   - `gap-checked` — only `gap_report.md` exists
   - `not-started` — no artifacts

### Phase 2: Content Loading

Load files based on the state determined above:

| State | Read immediately | Read on demand |
|-------|-----------------|----------------|
| not-started / gap-checked | gap_report.md (if exists) | — |
| drafted | analysis.md (full) | sources |
| model-setup | analysis.md, model_output.txt | model_setup.py, sources |
| reviewed | analysis.md, review.md, model_output.txt | model_setup.py, sources |
| synthesized / approved | analysis.md, synthesis.md, model_output.txt | review.md, model_setup.py, sources |

All paths relative to `exploration/concept_analysis/analyses/<concept-id>/`.

For sources, use the glob pattern: `knowledge/concept_research/<concept-id>/iter-*/sources/*.md` (e.g., `knowledge/concept_research/11-magnetic-mirror/iter-*/sources/*.md`). Sources live in the concept research directory, not in the concept analysis directory.

### Phase 3: Memory Loading

Read `exploration/concept_analysis/memory/learnings.md` directly. Match entries relevant to this concept:

1. Extract short numeric ID from the concept (e.g., `11` from `11-magnetic-mirror`)
2. Determine confinement family from the concept name or analysis frontmatter (MFE for tokamaks/stellarators/mirrors, IFE for laser/heavy-ion concepts, MIF for magnetized target)
3. Match entries tagged with: the short ID, the family tag, or `all`
4. Surface matched entries in the state presentation

## State Presentation

After loading context, present a status block:

```
## Concept: [Concept Name] — [Company]
**Pipeline State:** [state] ([letter code])
**Stale Downstream:** [list stale artifacts with reasons, or "none"]

**Available Artifacts:**
- analysis.md ([size], created [date], Reuses: [list])
- model_setup.py ([size]) [⚠ STALE if applicable]
- model_output.txt ([size], LCOE: [value] $/MWh)
- review.md — [exists with N PA items / not yet created]
- synthesis.md — [exists / not yet created]
- change_requests.md — [exists with N pending findings / not present]

**Sources:** [count] documents across [iteration dirs]

**Relevant Memories:** [count] entries loaded ([brief descriptions])

**Focus for this stage:** [stage-specific focus statement]
```

Then immediately proceed to the stage-aware opening action (see below).

## Stage-Aware Behavior

### Mode A: Early Vetting (state = `drafted` or `model-setup`)

**Default opening action:** Present key bets analysis.

Read the full analysis.md and identify:

**Bets** — Technical or economic claims the concept's viability depends on:
- Template: "This concept bets that **[X]** is achievable at scale"
- For each: impact if true, impact if false, current evidence quality
- Sources: Sections 2 (challenges), 3 (differentiators), 5 (parameters), 6 (gaps)

**Assumptions** — Values or approaches taken as given:
- Template: "The analysis assumes **[Y]**"
- For each: unique to this concept or shared? Basis? What changes if wrong?
- Sources: Section 5 parameter table (especially values marked `[estimated]`, `[inferred]`, `[analogue]`)

**Flags** — Noteworthy items that may need attention:
- Template: "Flag: **[Z]**"
- Examples: missing source data for a key parameter, unusually optimistic/pessimistic values, contradictions
- Sources: Section 1 (data availability), Section 6 (gaps), model_output.txt (sensitivity rankings)

**How to identify these — scan systematically:**
1. Section 5 parameter table: rows with `[estimated]`, `[inferred]`, `[analogue]`, or empty Source columns → these are assumption-backed
2. Section 2: phrases like "requires", "depends on", "assumes", "if achievable" → these indicate bets
3. `model_output.txt` sensitivity analysis: parameters with highest elasticity are highest-leverage bets
4. `Reuses` frontmatter field: if this concept reuses parameters from a very different concept type, that's a flag
5. Section 6 gap table: blocking gaps are bets that the gap can be filled

**If `model-setup` state, also:**
- Compare `model_output.txt` LCOE against typical range for this confinement family
- Note if recirculating power fraction is unusually high/low
- Flag parameters where `model_setup.py` uses framework defaults (no override)

### Mode B: Review Decision Support (state = `reviewed`)

**Default opening action:** Present PA items grouped by severity.

Read review.md and present PA items in priority order:

```
## Proposed Actions Requiring Decisions

### Blocking (N items)
**PA-1:** [description] — [finding summary]
→ What's your decision? (agree / reject / alternative)

### Important (N items)
[...]

### Minor (N items)
[listed more briefly]

### Already Decided (N items)
[PA items where Decision field is already filled]
```

When the user decides on a PA item:
1. Confirm: "I'll set PA-N Decision to '[value]'. Confirm?"
2. On confirmation, use Edit tool to replace the placeholder in review.md:
   - Decision: `_[USER FILLS IN: agree | reject | alternative]_` → the decided value
   - User Notes (if provided): `_[USER FILLS IN]_` → the user's rationale
3. Use a specific enough `old_string` pattern that includes the PA-N header context to ensure a unique match

After all decisions are filled, suggest:
```
All PA decisions filled. Run address-review to apply:
  uv run python exploration/concept_analysis/scripts/run_analysis.py address-review <concept-id>
```

### Mode C: Deep Vetting (state = `synthesized` or `approved`)

**Default opening action:** Summarize synthesis verdicts and offer to challenge them.

Read synthesis.md and present:
- Overall verdict and LCOE estimate
- Risk ratings and their basis
- TRL assessment
- Cross-concept ranking position (if available)

Then offer: "Want me to challenge any of these verdicts, compare against a specific concept, or probe a particular assumption?"

### Mode D: Pre-Analysis Guidance (state = `not-started` or `gap-checked`)

**Default opening action:** Inform user and suggest next pipeline step.

```
Concept [id] has no analysis yet (state: [state]).

To start analysis:
  uv run python exploration/concept_analysis/scripts/run_analysis.py analyze [concept-id]

I can help you explore the sources or gap report if you want to understand
what's available before running the pipeline.
```

## Change Request Protocol

When the user identifies an issue that requires changes to analysis.md, write structured feedback using the F-N format.

**Step 1:** Draft the entry in conversation and show the user:
```
I'll draft this as a change request:

### F-N: [Short title]
- **Target:** [Section number or aspect]
- **Finding:** [What needs to change — shape/framing, NOT numerical accuracy]
- **Recommendation:** [Specific enough for the analysis agent to act on]
- **Priority:** blocking | important | minor

Write this to change_requests.md?
```

**Step 2:** On confirmation, write or append to `exploration/concept_analysis/analyses/<concept-id>/change_requests.md`.

**Append logic:**
1. If `change_requests.md` exists, read it to find the last F-N number
2. Increment from there (e.g., last is F-3 → new entry starts at F-4)
3. Append the new entry with a blank line separator
4. If the file doesn't exist, create with this header:

```markdown
# Change Requests: <concept-id>

Generated via /manage-concept interactive sessions.
Apply with: uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> --feedback change_requests.md

VERDICT: FINDINGS

### F-1: [title]
...
```

**After writing change requests**, note:
```
Change request F-N written. To apply all pending changes:
  uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> \
    --feedback exploration/concept_analysis/analyses/<concept-id>/change_requests.md

Want me to run this? (It invokes headless Claude — typically takes 2-5 minutes.)
```

If the user asks you to run it, use Bash. Warn about duration first.

**Note:** The feedback_format.md max-3-findings rule constrains the *automated assessment agent's* per-pass output. You are NOT bound by that limit. A single interactive session may produce any number of F-N entries.

## Change Log Protocol

Maintain `exploration/concept_analysis/analyses/<concept-id>/change_log.md` as a cumulative audit trail.

**Entry format:**

```markdown
## Session: YYYY-MM-DD HH:MM

### Findings Discussed
- [bullet list of key topics/findings from this session]

### Decisions Made
- [PA-N: decision (brief description)]

### Change Requests Written
- [F-N: title (priority)]

### Learnings Saved
- [title → memory/learnings.md]
```

**Write timing:** Update at natural breakpoints (after a batch of decisions, before wrapping up) — not after every single interaction.

At session end, proactively offer: "Want me to update the change log with this session's findings before we wrap up?"

## Cross-Concept Comparison

Perform on-demand comparison by reading other concepts' artifacts.

**Finding comparison targets:**

1. **From Reuses field:** Current concept's frontmatter `Reuses: [01, 08, 21]` → direct comparison targets
2. **By family:** Grep `exploration/concept_analysis/analyses/*/analysis.md` frontmatter for same confinement family
3. **By user request:** User names a specific concept ID or name
4. **From status:** `uv run python exploration/concept_analysis/scripts/run_analysis.py status` shows all concepts

**Comparison operations:**

| Type | Source Files | What to Extract |
|------|-------------|-----------------|
| Parameter comparison | analysis.md Section 5 | Parameter table rows — value, source, confidence |
| LCOE comparison | model_output.txt | Total LCOE, CAS breakdown, recirculating fraction |
| Model structure | model_setup.py | `forward()` arguments, overrides, rationale |
| Risk comparison | analysis.md Section 6 | Gap table, blocking vs. non-blocking |
| Differentiators | analysis.md Section 3 | Novel/borrowed/shared classification |

When comparing, always name specific values, sources, and confidence levels. Generic comparison is not useful.

## Memory Protocol

### Reading (session start)

Already handled in Phase 3 of Context Loading. Surface matched entries in the state presentation.

### Writing (during session)

Two triggers:
1. **User request:** "Save this to memory" → draft and write immediately after confirmation
2. **Agent suggestion:** You identify a cross-concept pattern → suggest saving → write ONLY after user confirmation

**Write process:**
1. Draft the entry in conversation showing the formatted entry
2. Get user confirmation
3. Invoke memory-handler subagent via Agent tool:
   ```
   Agent tool with subagent_type not specified (general-purpose)
   Prompt: "You are the memory-handler agent. Read .claude/agents/memory-handler.md for your
   instructions. Write this entry to exploration/concept_analysis/memory/learnings.md:
   [formatted entry]"
   ```
4. Confirm to user: "Saved to memory/learnings.md"

**Entry format:**
```markdown
## [Descriptive Title]
Date: YYYY-MM-DD | Concepts: TAG[, TAG]*

Body text — specific and actionable. 3-7 lines.
```

Tags: short numeric IDs (`09`), family tags (`MFE`, `IFE`, `MIF`), or `all`. Total entry ≤ 10 lines.

## Pipeline Stage Reference

All commands: `uv run python exploration/concept_analysis/scripts/run_analysis.py <command> <concept-id>`

| Command | Purpose | Typical Next Step |
|---------|---------|-------------------|
| gap-check | Assess source coverage | analyze |
| analyze | Generate D1+ analysis (iterative) | model-setup |
| analyze --feedback \<path\> | Apply feedback file to existing analysis | review |
| model-setup | Generate cost model + LCOE | build-visuals or review |
| build-visuals | Generate sensitivity explorer HTML | review |
| review | Citation/calculation audit | (fill PA decisions) |
| address-review | Apply PA decisions to artifacts | synthesize |
| synthesize | Generate editorial synthesis | approve |
| approve | Mark concept as approved | — |
| add-source \<path-or-url\> | Extract and add new source | update-analysis |
| update-analysis --sources \<name\> | Integrate new source | review |
| status | Show all concepts' pipeline state | — |

Use this table to:
- Suggest the next stage based on current state
- Provide exact commands when the user asks "what should I run next?"
- Run stages via Bash if the user approves (warn about duration for Claude-invoking stages)

## Rules & Constraints

### What NOT to Edit Directly

- **analysis.md** — NEVER edit directly. All changes go through `change_requests.md` → `analyze --feedback` pipeline. The analysis agent is the authority on analysis.md content.
- **model_setup.py** — NEVER edit directly. Changes flow through `model-setup` pipeline stage.
- **synthesis.md** — NEVER edit directly. Changes flow through `synthesize` pipeline stage.

### What You CAN Edit

- **review.md** — ONLY the `Decision` and `User Notes` fields of PA-N entries, with user confirmation
- **change_requests.md** — Create or append F-N entries, with user confirmation
- **change_log.md** — Create or append session entries

### Confirmation Requirements

- Always confirm before writing change requests
- Always confirm before editing review.md Decision fields
- Always confirm before saving memory entries
- Always warn about duration before running pipeline stages via Bash

### General

- Do NOT use `--dangerously-skip-permissions`
- Do NOT prescribe conversation flow rigidly — the stage-aware behavior sets the default focus, but the user can ask about anything at any time
- When uncertain about a value, parameter, or claim — say so. Do not fabricate domain knowledge.
- Ground all assertions in the loaded artifacts. Cite specific sections, parameter table rows, or source documents.
