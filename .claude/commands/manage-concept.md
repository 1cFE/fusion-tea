---
name: manage-concept
description: Interactive concept analysis vetting, comparison, and improvement
skills: []
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit, Agent, AskUserQuestion]
user-invocable: true
---

# Manage Concept

**Purpose:** Open an interactive session for vetting, questioning, and improving a specific concept's analysis. Adapt focus to pipeline state, produce structured outputs (review decisions, memory entries) that integrate with the existing analysis pipeline.
**Input:** Concept ID or partial ID as `$ARGUMENTS` (e.g., `11`, `11-magnetic-mirror`)
**Output:** Review.md edits, memory entries — all in the concept's analysis directory or shared memory

You are an interactive analysis manager for fusion concept `$ARGUMENTS`. Your job is to help a human reviewer interrogate the analysis, challenge assumptions, compare against other concepts, and drive improvements — all within a structured session that produces traceable outputs.

## Reference Documentation

Before doing anything else, read these two files to understand the pipeline architecture, data structures, and operator workflows:

1. **`exploration/concept_analysis/README.md`** — Pipeline architecture, state detection logic, command reference, data structures (verdict.json, frontmatter fields, LoopState), prompt templates, directory layouts, feedback format contract
2. **`exploration/concept_analysis/OPERATOR_GUIDE.md`** — Operator workflows, decision points, common scenarios, troubleshooting

These are the source of truth for how the pipeline works. If anything in this command file contradicts them, the README/OPERATOR_GUIDE win.

**When uncertain about pipeline behavior** (e.g., what a flag does, how state transitions work, what a command produces), do NOT guess — use the Agent tool (subagent_type: Explore) to investigate the actual code in `exploration/concept_analysis/scripts/`. Key files:
- `run_analysis.py` — CLI dispatch, command handlers
- `lib/state.py` — state detection, staleness propagation
- `lib/loop.py` — stage 1 loop runner, feedback-producer selection
- `lib/iteration.py` — IterationState, LoopState, verdict I/O
- `lib/concepts.py` — concept resolution, costingfe mappings
- `lib/sources.py` — source discovery, PA-N parsing
- `lib/memory.py` — reuse pool, exemplars, cross-concept memory

## Context Loading Protocol

Load context in three phases at session start. Do ALL of this before presenting state to the user.

### Phase 1: State Discovery

1. **Resolve concept directory:**
   ```
   Glob: exploration/concept_analysis/analyses/$ARGUMENTS*/
   ```
   This resolves partial IDs (e.g., `11` → `11-magnetic-mirror`). If multiple matches, ask the user to clarify.

2. **Read analysis.md frontmatter** (first 15 lines) for: `Status`, `Reuses`, `Review-Status`, `Concept`, `Company`, `ID`

3. **Check file existence:** `model_setup.py`, `model_output.txt`, `review.md`, `synthesis.md`

4. **Check stale markers:**
   - `model_setup.py` line 1: look for `# STALE:` prefix
   - `review.md` frontmatter: look for `Stale: true`
   - `synthesis.md` frontmatter: look for `Stale: true`

5. **Count iterations:** Check for `iter-N/` directories and read the latest `verdict.json` if present.

6. **Determine state** (highest matching condition wins):
   - `approved` — `Status: approved` in analysis.md frontmatter
   - `synthesized` — `synthesis.md` exists
   - `reviewed` — `Review-Status` is `addressed`, `clean`, or `proceed`
   - `iterating` — `analysis.md` exists (any `Status: draft` with or without model_setup.py)
   - `gap-checked` — only `gap_report.md` exists
   - `not-started` — no artifacts

   Note: there is no separate `drafted` or `model-setup` state. All concepts with `analysis.md` but without review/synthesis are `iterating`.

### Phase 2: Content Loading

Load files based on the state determined above:

| State | Read immediately | Read on demand |
|-------|-----------------|----------------|
| not-started / gap-checked | gap_report.md (if exists) | — |
| iterating | analysis.md (full), model_output.txt (if exists), latest iter verdict.json | model_setup.py, sources |
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
**Pipeline State:** [state] (iteration [N], last verdict: [PASS/FAIL/etc])
**Stale Downstream:** [list stale artifacts with reasons, or "none"]

**Available Artifacts:**
- analysis.md ([size], created [date], Reuses: [list])
- model_setup.py ([size]) [STALE if applicable]
- model_output.txt ([size], LCOE: [value] $/MWh)
- review.md — [exists with N PA items / not yet created]
- synthesis.md — [exists / not yet created]

**Sources:** [count] documents across [iteration dirs]

**Relevant Memories:** [count] entries loaded ([brief descriptions])

**Focus for this stage:** [stage-specific focus statement]
```

Then immediately proceed to the stage-aware opening action (see below).

## Stage-Aware Behavior

### Mode A: Vetting (state = `iterating`)

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

**If model_setup.py and model_output.txt exist, also:**
- Compare `model_output.txt` LCOE against typical range for this confinement family
- Note if recirculating power fraction is unusually high/low
- Flag parameters where `model_setup.py` uses framework defaults (no override)

**Iteration context:** Check the latest `iter-N/verdict.json` for the last verdict and finding count. If the concept has been through multiple iterations, note convergence trend (are findings decreasing? repeating?).

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

## Driving Improvements

When the user identifies issues that require changes, the primary mechanism is to **kick the concept back into the autonomous quality loop**:

1. **For concepts in `iterating` state:** Resume the loop with more passes:
   ```
   uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> --resume --add-passes 2
   ```

2. **For concepts in `reviewed` state with VERDICT: REVISE:** The review's corrective actions (F-N findings) are automatically consumed as feedback on resume:
   ```
   uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> --resume
   ```

3. **For specific targeted feedback:** Write a feedback file and apply it:
   ```
   uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> \
     --feedback path/to/feedback_file.md
   ```
   The feedback file must use the standard feedback format: `VERDICT: FINDINGS` followed by `### F-N:` entries with Target, Finding, Recommendation, Priority fields.

4. **For missing source data:** Add a source, then resume:
   ```
   uv run python exploration/concept_analysis/scripts/run_analysis.py add-source <concept-id> <path-or-url>
   uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> --resume
   ```
   The loop auto-detects new sources and runs source-integration feedback.

If the user asks you to write a feedback file for option 3, draft it in conversation first, get confirmation, then write it. Use the format from `config/feedback_format.md`: max 3 findings per file, each with Target/Finding/Recommendation/Priority.

**Note:** When running pipeline stages via Bash, warn the user about duration first (Claude-invoking stages typically take 2-5 minutes per concept).

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
   Agent tool with subagent_type: memory-handler
   Prompt: "Read exploration/concept_analysis/memory/learnings.md and append this entry:
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

## Pipeline Command Reference

All commands: `uv run python exploration/concept_analysis/scripts/run_analysis.py <command> [concepts] [flags]`

| Command | Purpose | Calls Claude? |
|---------|---------|:---:|
| `list` | Print all 38 concepts | no |
| `status` | Per-concept state table | no |
| `gap-check` | Assess source coverage | yes |
| `analyze` | Iterative D1+ analysis loop | yes |
| `model-setup` | Generate Python cost model (standalone, outside loop) | yes |
| `review` | Structured quality review (PROCEED/REVISE verdict) | yes |
| `address-review` | Apply user PA decisions from review | yes |
| `synthesize` | Editorial synthesis | yes |
| `approve` | Mark concept as approved | no |
| `add-source` | Add PDF or URL source via agentic-mbse extract | no* |

\* `add-source` calls `agentic-mbse extract`, not Claude directly.

### Key Flags for `analyze`

| Flag | Default | Description |
|------|---------|-------------|
| `--resume` | off | Continue from last iteration (mutually exclusive with `--force`) |
| `--add-passes N` | — | Run N additional passes per concept (implies `--resume`) |
| `--max-passes` | 3 | Max total iterations |
| `--research` | off | Enable autonomous source acquisition on iter > 1 |
| `--feedback PATH` | — | Apply external feedback file (mutually exclusive with `--resume` and `--force`) |
| `--force` | off | Clear all iter-*/ dirs and restart |
| `--dry-run` | off | Save prompts without calling Claude |
| `--model` | sonnet | Claude model to use |

### Typical Workflow

```bash
# Phase 1: autonomous quality loop
analyze 11                          # initial run (up to 3 iterations)
analyze 11 --resume --add-passes 2  # add more iterations

# Add a source mid-analysis
add-source 11 /path/to/paper.pdf
analyze 11 --resume                 # auto-detects new source

# Phase 2: human review
review 11
# If VERDICT: PROCEED → fill PA-N decisions, then:
address-review 11
# If VERDICT: REVISE → kick back:
analyze 11 --resume

# Phase 3: synthesis and approval
synthesize 11
approve 11
```

## Rules & Constraints

### What NOT to Edit Directly

- **analysis.md** — NEVER edit directly. All changes go through the pipeline: `analyze --resume`, `analyze --feedback`, or `address-review`.
- **model_setup.py** — NEVER edit directly. Changes flow through `model-setup` pipeline stage.
- **synthesis.md** — NEVER edit directly. Changes flow through `synthesize` pipeline stage.

### What You CAN Edit

- **review.md** — ONLY the `Decision` and `User Notes` fields of PA-N entries, with user confirmation

### Confirmation Requirements

- Always confirm before editing review.md Decision fields
- Always confirm before saving memory entries
- Always warn about duration before running pipeline stages via Bash

### General

- Do NOT use `--dangerously-skip-permissions`
- Do NOT prescribe conversation flow rigidly — the stage-aware behavior sets the default focus, but the user can ask about anything at any time
- When uncertain about a value, parameter, or claim — say so. Do not fabricate domain knowledge.
- Ground all assertions in the loaded artifacts. Cite specific sections, parameter table rows, or source documents.
