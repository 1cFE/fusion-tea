# Design: Interactive Manage-Concept Agent

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29 17:22 PDT
**Branch:** design-space-explore
**Commit:** 4528866

## Overview

A `.claude/commands/manage-concept.md` custom command that opens an interactive Claude session for vetting, questioning, and improving a specific concept's analysis. The agent loads concept context, adapts to pipeline state, and produces structured outputs (change requests, review decisions, memory entries) that integrate with the existing pipeline.

## Related Artifacts

- **Spec:** `.project/active/manage-concept-agent/spec.md`
- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 5)
- **Research:** `.project/research/20260328-pipeline-upgrade-feasibility.md` (Q2, Q3)
- **Dependencies:**
  - Item 1: `prompt_templates/config/feedback_format.md`, `prompt_templates/analysis_v2.md` (feedback-pass mode)
  - Item 4: `.claude/agents/memory-handler.md`, `exploration/concept_analysis/memory/learnings.md`

---

## Research Findings

### Existing Command Pattern

All 14 commands in `.claude/commands/` follow this frontmatter pattern:

```yaml
---
name: command-name
description: Brief purpose
skills: [skill1, skill2]
allowed-tools: [Read, Grep, Glob, Bash, Task, Write, Edit, AskUserQuestion]
user-invocable: true
---
```

Commands are prompt templates — they instruct the agent on what to read and how to behave. The agent does actual file reading via tool calls during the interactive session. Commands reference skills for domain knowledge but are self-contained in their behavioral specification.

### Pipeline Script Architecture (`run_analysis.py`)

Key functions the command's behavior must align with:

| Function | Lines | Signature | Purpose |
|----------|-------|-----------|---------|
| `get_concept_state()` | 384-431 | `(concept_id, analyses_dir) -> str` | Returns state: not-started/gap-checked/drafted/model-setup/reviewed/synthesized/approved, with `*` suffix for stale |
| `find_sources()` | 617-632 | `(concept_id, research_dir) -> list[Path]` | Globs `iter-*/sources/*.md` for all extracted sources |
| `parse_proposed_actions()` | 776-824 | `(review_path) -> list[dict]` | Parses PA-N entries from review.md (id, description, category, severity, location, finding, proposed_fix, decision, user_notes) |
| `load_relevant_memories()` | 888-932 | `(concept_id, memory_dir, family) -> str` | Matches memory entries by short ID + family tag + "all" |
| `propagate_staleness()` | 434-468 | `(concept_id, reason, analyses_dir) -> list[str]` | Marks model_setup.py/review.md/synthesis.md stale |
| `cmd_update_analysis()` | 1927-2074 | `(concepts, args) -> None` | 2-pass: source-integration pre-pass → feedback-pass |

### Concept Directory Structure

Each concept in `exploration/concept_analysis/analyses/<concept-id>/` contains:

```
analysis.md              # 30-40KB, Sections 1-8 with YAML frontmatter
gap_report.md            # Stage 1 output
model_setup.py           # Cost model (forward() call with commented parameters)
model_output.txt         # LCOE results, CAS breakdown, sensitivity analysis
review.md                # Citation/calculation audit, PA-1..PA-N with Decision fields
synthesis.md             # Editorial synthesis
*_prompt.md              # Saved prompts (audit trail)
address_log.md           # Log of review decisions applied
feedback_iter_N.md       # Assessment feedback from iterative loop
```

### Analysis.md Frontmatter

```yaml
---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (D-T)
Company: Realta Fusion
Status: draft
Created: 2026-03-28
Approved-Date:
Reuses: [01-hts-compact-tokamak, 08-frc-w-direct-conversion]
Review-Status: addressed
---
```

The `Reuses` field lists concepts referenced during analysis — these are natural comparison targets.

### PA-N Entry Format (review.md)

```markdown
### PA-N: [Short description]
- **Category:** citation-error | calculation-error | model-bug | inconsistency | factual-concern | improvement
- **Severity:** blocking | important | minor
- **Location:** [file §section or line]
- **Finding:** [what the review found]
- **Proposed Fix:** [what should change]
- **Decision:** _[USER FILLS IN: agree | reject | alternative]_
- **User Notes:** _[USER FILLS IN]_
```

Unfilled fields use italic placeholder: `_[USER FILLS IN: ...]_` or `_[USER FILLS IN]_`.

### F-N Feedback Format (`config/feedback_format.md`)

```markdown
VERDICT: PASS | FINDINGS

### F-N: [Short title]
- **Target:** [Section number or aspect]
- **Finding:** [Shape/framing issue — NOT numerical accuracy]
- **Recommendation:** [Specific enough for analysis agent to act on]
- **Priority:** blocking | important | minor
```

Max 3 findings per assessment pass. Findings address analysis shape/framing only.

### Memory Entry Format (`memory/learnings.md`)

```markdown
## [Descriptive Title]
Date: YYYY-MM-DD | Concepts: TAG[, TAG]*

Body text — 3-7 lines, specific and actionable.
```

Tags: short numeric IDs (`09`), family tags (`MFE`, `IFE`, `MIF`), or `all`. Total entry ≤ 10 lines.

### Analysis Goals (5 core objectives from `config/analysis_goals.md`)

1. **Concept Positioning** — Family, nearest neighbors, relationship to other approaches
2. **Key Differentiators** — Differences from mainstream tokamak (novel/borrowed/shared)
3. **TEA Implications** — Cost advantages/penalties per differentiator
4. **Modeling Approach** — How to model differences, key hypotheses, high-leverage parameters
5. **Risks and Assumptions** — Key bets with failure consequences, unique vs. shared assumptions

### Feedback-Pass Mode (analysis_v2.md)

The analysis template supports three modes via template variables:
- **Cold start**: `cold_start: "true"` — full first-pass analysis
- **Feedback pass**: `feedback_pass: "true"`, `feedback_path: <path>` — reads existing analysis + feedback file, uses Edit tool for targeted improvements
- **Self-advance**: neither set — agent reviews and improves own work

The feedback-pass mode is the mechanism for applying change requests from manage-concept.

### Integration Gap: `--feedback` Flag

Currently `cmd_update_analysis()` takes `--sources` and generates its own feedback via a source-integration pre-pass. There is no direct way to invoke feedback-pass mode with an arbitrary feedback file.

**Required addition**: A `--feedback <path>` flag on `cmd_analyze` (or a lightweight `cmd_apply_feedback` subcommand) that skips cold-start and goes straight to feedback-pass mode with the specified file. This is ~30 lines of code in `run_analysis.py`.

---

## Proposed Design

### Architecture Overview

The deliverable is a single file: `.claude/commands/manage-concept.md`. This is a prompt template that instructs an interactive Claude session. It does not modify the pipeline script — the only pipeline-side change is the `--feedback` flag addition.

```
User invokes: claude /manage-concept 11
                     │
                     ▼
        ┌─ manage-concept.md ──┐
        │                      │
        │  1. Resolve concept  │    Reads analyses dir, determines state
        │  2. Load context     │    analysis.md, review.md, model_output.txt, memories
        │  3. Present state    │    Pipeline state, available artifacts, stale markers
        │  4. Stage-aware mode │    Key bets / PA decisions / deep vetting
        │                      │
        │  Interactive session │    User asks questions, requests changes
        │                      │
        │  Outputs:            │
        │  ├─ change_requests.md  (F-N feedback → analysis agent)
        │  ├─ change_log.md       (session audit trail)
        │  ├─ review.md edits     (Decision fields)
        │  └─ memory/learnings.md (cross-concept insights)
        └──────────────────────┘
```

### Component 1: Command File (`.claude/commands/manage-concept.md`)

**Frontmatter:**

```yaml
---
name: manage-concept
description: Interactive concept analysis vetting, comparison, and improvement
skills: []
allowed-tools: [Read, Grep, Glob, Bash, Write, Edit, Agent, AskUserQuestion]
user-invocable: true
---
```

**No skills referenced** — the command is domain-specific to the concept analysis pipeline and carries all its own instructions. `Agent` tool is included for invoking the memory-handler subagent.

**Prompt structure** (sections within the command file):

1. **Header & Role** — "You are an interactive analysis manager for concept `$ARGUMENTS`"
2. **Context Loading Protocol** — Ordered list of files to read, with path patterns
3. **State Presentation** — How to report pipeline state to user
4. **Stage-Aware Behavior** — Mode selection based on state
5. **Key Bets Framework** — How to identify and present bets/assumptions/flags
6. **Change Request Protocol** — F-N format, appending rules, numbering
7. **Review Decision Protocol** — PA editing rules, confirmation flow
8. **Cross-Concept Comparison** — How to find and compare other concepts
9. **Memory Protocol** — Read at start, write by request or suggestion
10. **Pipeline Stage Reference** — CLI commands for all stages
11. **Rules & Constraints** — What NOT to edit, confirmation requirements

### Component 2: Context Loading Protocol

The agent reads context in a specific order at session start. This is instruction in the command prompt, not code.

**Phase 1 — State Discovery (lightweight, always):**

```
1. List files in exploration/concept_analysis/analyses/$ARGUMENTS*/
   (glob to resolve partial IDs like "11" → "11-magnetic-mirror")
2. Read analysis.md frontmatter only (first 15 lines) for Status, Reuses, Review-Status
3. Check existence of: model_setup.py, review.md, synthesis.md, change_requests.md
4. Check for stale markers: "# STALE:" in model_setup.py line 1, "Stale: true" in review.md/synthesis.md frontmatter
5. Determine state: approved > synthesized > reviewed > model-setup > drafted > gap-checked > not-started

**Note on duplication:** This logic mirrors `get_concept_state()` in `run_analysis.py` (lines 384-431). This is a conscious duplication — the command runs in an interactive Claude session without importing the Python function. If pipeline states or stale markers change in `run_analysis.py`, the command prompt must be updated to match. The `status` CLI command can be used as a cross-check.
```

**Phase 2 — Content Loading (state-dependent):**

| State | Read immediately | Read on demand |
|-------|-----------------|----------------|
| not-started / gap-checked | gap_report.md (if exists) | — |
| drafted | analysis.md (full) | sources via find_sources() pattern |
| model-setup | analysis.md, model_output.txt | model_setup.py, sources |
| reviewed | analysis.md, review.md, model_output.txt | model_setup.py, sources |
| synthesized / approved | analysis.md, synthesis.md, model_output.txt | review.md, model_setup.py, sources |

**Phase 3 — Memory Loading:**

Invoke the memory-handler subagent (`.claude/agents/memory-handler.md`) via Agent tool in read mode, passing:
- Concept ID (full, e.g., "11-magnetic-mirror")
- Family tag (extracted from analysis.md or inferred from concept name)

Alternatively, the agent can read `exploration/concept_analysis/memory/learnings.md` directly and filter entries matching the concept's tags. This is simpler and avoids a subagent invocation for a straightforward file read.

**Design decision: Direct memory read.** FR-2 allows either direct file read or memory-handler subagent. The memory-handler is more useful for write validation (format enforcement, duplicate checking). For reading, the matching logic is simple enough to describe in the command prompt: extract short ID from concept name, match entries tagged with that ID, the confinement family, or "all".

### Component 3: State Presentation

After loading context, the agent presents a status block to the user:

```
## Concept: Magnetic Mirror (D-T) — Realta Fusion
**Pipeline State:** model-setup (M)
**Stale Downstream:** model_setup.py (stale: analysis updated by source addition)

**Available Artifacts:**
- analysis.md (38.7 KB, created 2026-03-28, Reuses: [01, 08])
- model_setup.py (16.2 KB) ⚠ STALE
- model_output.txt (5.8 KB, LCOE: 135.2 $/MWh)
- review.md — not yet created
- synthesis.md — not yet created

**Sources:** 8 documents across iter-0, iter-1, iter-2

**Relevant Memories:** 2 entries loaded (ARIES parameter source, O&M breakdown pattern)

**Focus for this stage:** Key bets analysis — identifying what this concept is betting on,
critical assumptions, and flags.
```

The exact wording adapts per state. For `not-started`/`gap-checked`, the focus section becomes pipeline guidance instead.

### Component 4: Stage-Aware Behavior Modes

#### Mode A: Early Vetting (`drafted`, `model-setup`)

**Default opening action:** Present initial key bets analysis.

The agent reads the full analysis.md and identifies:

**Bets** — Technical or economic claims the concept's viability depends on:
- Template: "This concept bets that **[X]** is achievable at scale"
- For each: impact if true, impact if false, current evidence quality
- Sources: Drawn from Sections 2 (challenges), 3 (differentiators), 5 (parameters), 6 (gaps)

**Assumptions** — Values or approaches taken as given:
- Template: "The analysis assumes **[Y]**"
- For each: unique to this concept or shared with others? Basis? What changes if wrong?
- Sources: Section 5 parameter table (especially values marked `[estimated]`, `[inferred]`, `[analogue]`)

**Flags** — Noteworthy items that may need attention:
- Template: "Flag: **[Z]**"
- Examples: missing source data for a key parameter, unusually optimistic/pessimistic values, contradictions between sources
- Sources: Section 1 (data availability), Section 6 (gaps), model_output.txt (sensitivity rankings)

**Identification heuristic** (instructions to the agent):
1. Scan Section 5 parameter table for rows with `[estimated]`/`[inferred]`/`[analogue]` or empty Source columns — these are assumption-backed
2. Scan Section 2 for phrases like "requires", "depends on", "assumes", "if achievable" — these indicate bets
3. Check model_output.txt sensitivity analysis — parameters with highest elasticity are highest-leverage bets
4. Cross-reference Reuses field — if this concept reuses parameters from a very different concept type, that's a flag
5. Check Section 6 gap table for blocking gaps — each is a bet that the gap can be filled

If `model_setup` state, also:
- Compare model_output.txt LCOE against the "typical" range for this confinement family (available from approved analyses or shared memory)
- Note if recirculating power fraction is unusually high/low
- Flag any parameters where model_setup.py uses framework defaults (no override) — these may be inappropriate for this concept

#### Mode B: Review Decision Support (`reviewed`)

**Default opening action:** Present PA items grouped by severity.

The agent reads review.md and presents PA items in priority order:

```
## Proposed Actions Requiring Decisions

### Blocking (0 items)
(none)

### Important (2 items)
**PA-3:** Blanket energy multiplication — model uses M=1.10 but derivation from
TBR=1.1 gives M≈1.37. Proposed fix: use 1costingfe standard value with corrected comment.
→ What's your decision? (agree / reject / alternative)

**PA-5:** Direct energy conversion efficiency 54% — no source cited, appears optimistic
compared to ARIES-CS 45%. Proposed fix: range 35-54% with sensitivity note.
→ What's your decision?

### Minor (6 items)
[listed more briefly]

### Already Decided (N items)
[PA items where Decision field is already filled]
```

When the user decides on a PA item, the agent:
1. Confirms: "I'll set PA-3 Decision to 'agree'. Confirm?"
2. On confirmation, uses Edit tool to replace `_[USER FILLS IN: agree | reject | alternative]_` with the decision value in review.md
3. Optionally captures User Notes if the user provides rationale

**Edit target patterns:**
- Decision: `- **Decision:** _[USER FILLS IN: agree | reject | alternative]_` → `- **Decision:** agree`
- User Notes: `- **User Notes:** _[USER FILLS IN]_` → `- **User Notes:** Use 1costingfe standard M=1.10 per AD-003`

After all decisions are filled, the agent suggests: "All PA decisions filled. Run address-review to apply: `uv run python exploration/concept_analysis/scripts/run_analysis.py address-review <concept-id>`"

#### Mode C: Deep Vetting (`synthesized`, `approved`)

**Default opening action:** Summarize synthesis verdicts and offer to challenge them.

The agent reads synthesis.md and presents:
- Overall verdict and LCOE estimate
- Risk ratings and their basis
- TRL assessment
- Cross-concept ranking position (if available)

Then offers: "Want me to challenge any of these verdicts, compare against a specific concept, or probe a particular assumption?"

#### Mode D: Pre-Analysis Guidance (`not-started`, `gap-checked`)

**Default opening action:** Inform user and suggest next pipeline step.

```
Concept 37 has no analysis yet (state: gap-checked).

To start analysis:
  uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 37

I can help you explore the sources or gap report if you want to understand
what's available before running the pipeline.
```

### Component 5: Change Request Protocol

When the user identifies an issue that requires changes to analysis.md:

**Step 1:** Agent drafts an F-N entry in conversation:
```
I'll draft this as a change request:

### F-4: Recirculating power fraction uses optimistic pump estimate
- **Target:** Section 5, Parameter Table (p_pump row)
- **Finding:** Pump power of 2 MW appears optimistic for a 70m chamber...
- **Recommendation:** Update to 8-12 MW range based on ARIES-CS scaling...
- **Priority:** important

Write this to change_requests.md?
```

**Step 2:** On confirmation, the agent writes/appends to `exploration/concept_analysis/analyses/<concept-id>/change_requests.md`.

**Append logic:**
1. If `change_requests.md` exists, read it to find the last F-N number
2. Increment from there (e.g., if last is F-3, new entry starts at F-4)
3. Append the new entry with a blank line separator
4. If file doesn't exist, create with header:

```markdown
# Change Requests: <concept-id>

Generated via /manage-concept interactive sessions.
Apply with: uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> --feedback change_requests.md

VERDICT: FINDINGS

### F-1: [title]
...
```

**Max-3 rule clarification:** The `feedback_format.md` max-3-findings rule constrains the *assessment agent's* per-pass output — it prevents the automated loop from churning. The manage-concept agent is not bound by this limit. A single interactive session may produce any number of F-N entries in `change_requests.md`. The analysis agent's feedback-pass mode processes all F-N entries in the file regardless of count — it iterates over each finding and applies edits sequentially.

**After writing change requests**, the agent notes:
```
Change request F-4 written. To apply all pending changes:
  uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <concept-id> --feedback exploration/concept_analysis/analyses/<concept-id>/change_requests.md

Want me to run this? (It invokes headless Claude — typically takes 2-5 minutes.)
```

**Pipeline invocation expectations:** Running `cmd_analyze --feedback` from within the interactive session via Bash is a long-running operation (2-5 minutes for a feedback pass). The agent SHOULD warn the user about duration before offering to run it. If the user prefers, they can run it after the session ends instead.

### Component 6: Change Log Protocol

The agent maintains `exploration/concept_analysis/analyses/<concept-id>/change_log.md` as a cumulative session audit trail.

**Entry format:**

```markdown
## Session: 2026-03-29 17:30 PDT

### Findings Discussed
- Recirculating power fraction appears optimistic (p_pump = 2 MW for 70m chamber)
- Direct energy conversion efficiency of 54% lacks source citation
- Model uses tokamak-derived blanket costs but concept has significantly different geometry

### Decisions Made
- PA-3: agree (blanket energy multiplication)
- PA-5: alternative — use 35-54% range instead of single point

### Change Requests Written
- F-4: Recirculating power fraction pump estimate (important)
- F-5: DEC efficiency source needed (minor)

### Learnings Saved
- "Mirror concepts consistently lack pump power data" → memory/learnings.md
```

**Write timing:** The agent should write/update the change log at natural breakpoints during the conversation (after a batch of decisions, before session end), not after every single interaction.

At session end, the agent should proactively offer: "Want me to update the change log with this session's findings before we wrap up?"

### Component 7: Cross-Concept Comparison

The agent performs on-demand comparison by reading other concepts' artifacts.

**Finding comparison targets:**

1. **From Reuses field:** Read current concept's frontmatter → `Reuses: [01, 08, 11, 21]` → these are direct comparison targets
2. **By family:** Grep `exploration/concept_analysis/analyses/*/analysis.md` frontmatter for concepts in the same confinement family
3. **By user request:** User names a specific concept ID or concept name
4. **From status:** Run `uv run python exploration/concept_analysis/scripts/run_analysis.py status` to see all concepts and their states

**Comparison operations:**

| Comparison Type | Source Files | What to Extract |
|----------------|-------------|-----------------|
| Parameter comparison | analysis.md Section 5 | Parameter table rows — value, source, confidence |
| LCOE comparison | model_output.txt | Total LCOE, CAS breakdown, recirculating fraction |
| Model structure | model_setup.py | `forward()` arguments, overrides, commented rationale |
| Risk comparison | analysis.md Section 6 | Gap table, blocking vs. non-blocking |
| Differentiators | analysis.md Section 3 | Novel/borrowed/shared subsystem classification |

**Example interaction:**
```
User: How does the thermal efficiency compare to other mirror concepts?

Agent: [Reads 06-magnetic-mirror/analysis.md and 11-magnetic-mirror/analysis.md Section 5]
       [Reads model_output.txt for both]

       Concept 06 (Classical Mirror) uses η_th = 0.35 (analogue from MFTF-B scaling)
       Concept 11 (Realta Mirror) uses η_th = 0.40 (estimated, high uncertainty)

       For comparison, tokamak concepts 01 and 21 use η_th = 0.33 (ARIES-AT baseline).

       The 0.40 for concept 11 is optimistic — it assumes a high-temperature FLiBe
       outlet that hasn't been demonstrated at this scale. Flag as a key bet?
```

### Component 8: Memory Integration

**Read (session start):**

The agent reads `exploration/concept_analysis/memory/learnings.md` directly. Matching logic described in the command prompt:

1. Extract short ID from concept (e.g., `11` from `11-magnetic-mirror`)
2. Determine family tag (from analysis.md frontmatter or concept name — MFE for mirrors, IFE for laser concepts, etc.)
3. Match entries tagged with: short ID, family tag, or `all`
4. Surface relevant entries to the user in the state presentation

**Write (during session):**

Two triggers:
1. **User request:** "Save this to memory" → agent writes immediately
2. **Agent suggestion:** Agent identifies a cross-concept pattern → suggests saving → writes only after user confirmation

**Write process:**
1. Draft the entry in conversation (showing the formatted entry)
2. Get user confirmation
3. Invoke memory-handler subagent via Agent tool in write mode — this handles format validation, duplicate checking, and appending to the correct file
4. Confirm to user: "Saved to memory/learnings.md"

**Design decision: Use memory-handler for writes.** Unlike reads (where the agent can match entries itself), writes benefit from the memory-handler's validation (≤10 lines, no duplicates, proper tagging). The agent drafts the content; the handler validates and appends.

### Component 9: Pipeline Stage Reference

Embedded in the command prompt as a reference table:

```
## Pipeline Commands Reference

All commands: uv run python exploration/concept_analysis/scripts/run_analysis.py <command> <concept-id>

| Command          | Purpose                              | Typical Next Step        |
|-----------------|--------------------------------------|--------------------------|
| gap-check       | Assess source coverage               | analyze                  |
| analyze         | Generate D1+ analysis (iterative)    | model-setup              |
| analyze --feedback <path> | Apply feedback file       | review                   |
| model-setup     | Generate cost model + LCOE           | build-visuals or review  |
| build-visuals   | Generate sensitivity explorer HTML   | review                   |
| review          | Citation/calculation audit           | (fill PA decisions)      |
| address-review  | Apply PA decisions to artifacts      | synthesize               |
| synthesize      | Generate editorial synthesis         | approve                  |
| approve         | Mark concept as approved             | —                        |
| add-source <path-or-url> | Extract and add new source  | update-analysis          |
| update-analysis --sources <name> | Integrate new source | review                   |
| status          | Show all concepts' pipeline state    | —                        |
```

The agent uses this to:
- Suggest the next stage based on current state
- Provide exact commands when the user asks "what should I run next?"
- Offer to run stages via Bash (with user approval)

### Component 10: Required Pipeline Integration

**Addition to `run_analysis.py`:** A `--feedback <path>` flag on `cmd_analyze`.

When `--feedback` is provided:
1. Skip cold-start mode
2. Set template variables: `feedback_pass: "true"`, `feedback_path: str(args.feedback)`
3. Invoke `analysis_v2.md` in feedback-pass mode
4. After successful run, call `propagate_staleness()` on the concept
5. Archive the consumed feedback file: rename to `change_requests_YYYYMMDD_HHMMSS.md` in the same directory (same convention as `feedback_iter_N.md` audit trail files). This ensures future `/manage-concept` sessions start with a fresh `change_requests.md` while preserving history.

This is ~30 lines of additional code in `cmd_analyze`, reusing the existing feedback-pass invocation pattern from `cmd_update_analysis()` (lines 2016-2066).

**Alternative considered:** A new `cmd_apply_feedback` subcommand. Rejected — the functionality is a mode of `cmd_analyze`, not a separate stage. Adding it as a flag keeps the command surface smaller.

---

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Context window pressure from large analysis.md (~40KB) + review.md (~20KB) + model_output.txt (~6KB) | Agent may lose detail late in conversation | Load review.md and sources on-demand rather than upfront; use Agent tool for cross-concept reads |
| Key bets analysis quality depends on prompt engineering | Bets may be generic or miss concept-specific nuances | Concrete heuristics in prompt (scan for `[estimated]`, check sensitivity rankings, compare Reuses); iterate on prompt after first 3-5 sessions |
| Change requests may not cleanly apply via feedback-pass | Analysis agent may misinterpret recommendations | Same risk as assessment feedback — mitigated by the same F-N format and specific Target/Recommendation fields |
| Multiple sessions creating conflicting change requests | Later change requests may contradict earlier ones | Append-only with incrementing F-N numbers; user reviews full file before applying; analysis agent sees all requests together |
| PA Decision edits could target wrong line if review.md has unusual formatting | Edit tool fails or edits wrong field | Use specific enough old_string patterns (full PA-N header + Decision line) to ensure unique match |

---

## Integration Strategy

**What this complements:**
- The iterative analysis loop (Item 1) provides the feedback format and feedback-pass mechanism that change requests flow through
- The shared memory system (Item 4) provides the cross-concept learning infrastructure
- The build-visuals stage (Item 2) provides sensitivity data that informs key bets analysis
- The `address-review` command provides the pattern for PA decision application

**What this does NOT change:**
- No modifications to existing prompt templates
- No modifications to existing pipeline stages
- No changes to the memory-handler subagent
- No changes to artifact formats (analysis.md, review.md, synthesis.md)

**New artifacts introduced:**
- `.claude/commands/manage-concept.md` — the command file
- `analyses/<concept-id>/change_requests.md` — per-concept, created on demand
- `analyses/<concept-id>/change_log.md` — per-concept, created on demand
- `--feedback` flag on `cmd_analyze` in `run_analysis.py`

---

## Validation Approach

### Manual Testing Protocol

**Test 1: Early-stage concept (drafted/model-setup)**
1. Run `claude /manage-concept 11` (magnetic mirror — state: model-setup with stale marker)
2. Verify: state presentation shows correct state, stale indicator, artifact list
3. Verify: key bets analysis identifies ≥3 substantive bets grounded in sources
4. Create a change request → verify `change_requests.md` written with correct F-N format
5. Verify: change log captures session findings

**Test 2: Reviewed concept**
1. Run `claude /manage-concept 12` (levitated dipole — state: synthesized, has review.md with PA items)
2. Verify: PA items presented grouped by severity
3. Fill in 2-3 PA decisions → verify `review.md` Decision fields updated correctly
4. Verify: agent suggests address-review after decisions filled

**Test 3: Cross-concept comparison**
1. During a session, ask "Compare thermal efficiency with concept 06"
2. Verify: agent reads both concepts' analysis.md and/or model_output.txt
3. Verify: comparison is specific (names values, sources, confidence levels)

**Test 4: Memory integration**
1. Verify: agent surfaces relevant memories at session start
2. Ask agent to save a learning → verify entry appended to memory/learnings.md in correct format
3. Have agent suggest a learning → verify it asks for confirmation before writing

**Test 5: Pipeline guidance**
1. Ask "what should I run next?" → verify correct CLI command suggested
2. Ask agent to run a stage → verify it offers the command or runs via Bash with approval

**Test 6: Append behavior**
1. Run two sessions on the same concept with change requests
2. Verify: second session's F-N numbers continue from first session's last number
3. Verify: change_log.md has two timestamped session entries

### Acceptance Gate

All 6 test scenarios pass. The command file is self-contained and works without modifications to existing pipeline stages (except the `--feedback` flag addition).

---

**Next Step:** After approval → `/_my_plan` to create implementation plan with phased execution
