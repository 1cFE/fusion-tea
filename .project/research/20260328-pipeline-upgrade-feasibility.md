---
date: 2026-03-28T10:00:00-05:00
researcher: Claude
topic: "Concept analysis pipeline upgrade feasibility — multi-pass, interactive agent, update handoff, visuals, manual sources"
tags: [research, pipeline, concept-analysis, upgrades]
status: complete
last_updated: 2026-03-28
---

# Research: Concept Analysis Pipeline Upgrades

**Date**: 2026-03-28
**Researcher**: Claude
**Research Type**: Architecture / Feasibility

## Research Questions

Five proposed upgrades to `exploration/concept_analysis/`:

1. Multi-pass analyze stage (current single-call → first pass + checklist review pass)
2. Interactive "manage" agent for per-concept Q&A and vetting
3. Reliable update handoff pattern (interactive session → artifact updates)
4. "build-visuals" stage after model-setup
5. Manual data source addition and incremental analysis updates

## Summary

- **Q1 (multi-pass)**: Straightforward. The analyze stage is a single `claude -p` call producing the full analysis. Adding a second pass requires only a new prompt template and a two-call sequence in `cmd_analyze`. No architectural barriers.
- **Q2 (interactive agent)**: Best implemented as a Claude Code custom command (`.claude/commands/`) that takes a concept number, loads all artifacts for that concept, and opens an interactive `claude` session (not `claude -p`). The command knows the pipeline state and can guide the conversation.
- **Q3 (update handoff)**: The key insight is to separate *identifying changes* from *applying changes*. The interactive session should produce a structured "change request" file (like review.md's PA-N format), and a separate headless pass applies the changes. This matches the existing review → address-review pattern.
- **Q4 (build-visuals)**: A new stage between model-setup and review that generates an interactive HTML sensitivity explorer from `model_setup.py` + `model_output.txt`. Pattern: headless Claude writes the HTML, pipeline validates it opens.
- **Q5 (manual sources)**: Download PDF → `uv run agentic-mbse extract` → place output in a new `iter-N/sources/` directory → run an `update-analysis` command that makes a targeted second pass on the existing analysis.

---

## Detailed Findings

### Q1: How Does "analyze" Work? How to Make It Multi-Pass?

#### Current Mechanism

The analyze stage (`cmd_analyze`, `run_analysis.py:820-921`) works as follows:

1. **Template fill**: Reads `prompt_templates/analysis.md`, substitutes concept-specific paths (dossier, sources, exemplars, approved pool)
2. **Frontmatter pre-write**: Creates `analysis.md` with YAML frontmatter before invoking Claude
3. **Single `claude -p` call**: Passes the filled template as stdin to `claude -p --dangerously-skip-permissions --verbose` (`invoke_claude()`, line 469-497)
4. **Claude writes body**: The prompt instructs Claude to use the Write tool to create `analysis_body.md` — a separate file from the frontmatter
5. **Assembly**: Script reads back the frontmatter (which Claude may have edited for `Reuses`) and concatenates with the body
6. **Cleanup**: Removes `analysis_body.md` temp file

The entire analysis (Sections 1-8, often 15-30K chars) is produced in a single Claude call. There is no intermediate checkpoint or second pass.

#### Multi-Pass Design

**Approach: Add a `--passes N` flag (default 1, max 2-3) to `cmd_analyze`**

Pass 1 (existing): Generate full analysis as-is. Output: `analysis_body.md` → assembled into `analysis.md`.

Pass 2 (new): A "quality review" pass. Reads the just-written `analysis.md` and a checklist prompt, then edits the file in place using Edit tool calls.

Implementation:

```python
# In cmd_analyze, after assembly:
if args.passes >= 2:
    # Pass 2: quality checklist review
    checklist_template = (TEMPLATES_DIR / "analysis_checklist.md").read_text()
    checklist_prompt = fill_template(checklist_template, {
        "analysis_path": str(analysis_path),
        "source_paths": format_source_list(sources),
        "dossier_path": str(dossier_path),
    })
    prompt_path_p2 = out_dir / "analysis_checklist_prompt.md"
    prompt_path_p2.write_text(checklist_prompt)

    stdout2, stderr2, rc2 = invoke_claude(
        checklist_prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )
    # Claude edits analysis.md in place via Edit tool
```

The checklist prompt (`prompt_templates/analysis_checklist.md`) would:
- Read the completed `analysis.md`
- Check against a specific checklist (citation completeness, parameter table coverage, derivation chains, anti-hallucination flags, section completeness)
- Use the Edit tool to fix issues directly in `analysis.md`
- Write a brief log of changes to `analysis_checklist_log.md`

**Key decisions**:
- Pass 2 should use Edit tool (targeted fixes), not Write (full rewrite) — avoids the "rewrite drift" problem where a second pass silently drops content
- The checklist should be concrete and checkable (not "improve quality"), e.g.: "Every row in Section 5 parameter table has a non-empty Source column with §Section reference"
- Consider using a different/stronger model for pass 2 (e.g., opus for review if pass 1 is sonnet)
- The `--passes` flag should be per-stage, not global, since other stages may not benefit

**Alternative: Separate `quality-check` stage** instead of multi-pass analyze. This would be a new stage between analyze and model-setup. Pro: cleaner separation of concerns, can be re-run independently. Con: adds another stage to an already 6-stage pipeline.

**Recommendation**: Start with the separate `quality-check` stage approach. It's more composable, can be added to `stage1-all`, and avoids complicating `cmd_analyze`. The implementation is identical (same prompt, same Edit-based approach) — it's just invoked as its own subcommand.

---

### Q2: Interactive "Manage" Agent

#### Design

A Claude Code custom command that opens an interactive session focused on a single concept. The agent knows the full pipeline context and can guide the user through vetting the analysis.

**Implementation: `.claude/commands/manage-concept.md`**

```markdown
# Manage Concept: $ARGUMENTS

You are an interactive analysis manager for the fusion concept analysis pipeline.

## Your Role
Help the user understand, vet, and improve the analysis for concept $ARGUMENTS.

## Context Loading
Read these files to understand the current state:
1. Pipeline README: `exploration/concept_analysis/README.md`
2. Concept status: run `uv run python exploration/concept_analysis/scripts/run_analysis.py status $ARGUMENTS`
3. Load all artifacts that exist for this concept from `exploration/concept_analysis/analyses/{concept-id}/`
4. Load the Phase 1a dossier and source documents

## Behavior by Pipeline Stage

### If stage is `drafted` or `model-setup` (early vetting):
Focus on these "key components" checks:
- **Key Bets**: What are the specific technical/economic bets this concept makes?
  For each bet: what happens if it's true? What happens if it's false?
- **Critical Assumptions**: What are the biggest assumptions, especially ones
  unique to this concept? Are they well-founded or speculative?
- **Asterisks**: Any red flags, unusual claims, or things that "feel wrong"
  based on the source material?

### If stage is `reviewed` (post-review):
- Help the user fill in Decision fields in `review.md`
- Explain each proposed action and its implications
- If the user wants to mark decisions, write them to a change request file

### General capabilities:
- Answer questions about the analysis, sources, and model
- Compare parameters against other approved analyses
- Trace claims back to source documents
- Identify where the analysis is on thin ice

## Important Rules
- Do NOT directly edit analysis.md, model_setup.py, or review.md
- Instead, if changes are identified, write them to:
  `exploration/concept_analysis/analyses/{concept-id}/change_requests.md`
- Use the structured format described in the change request section below
```

The user invokes this as:
```bash
claude /manage-concept 11
```

This opens a normal interactive Claude session with the concept context pre-loaded.

#### Stage-Aware Behavior

The command reads pipeline state via `get_concept_state()` logic (filesystem checks) and adjusts its focus:

| State | Agent Focus |
|-------|------------|
| `drafted` / `model-setup` | Key bets, critical assumptions, asterisks |
| `reviewed` (has-actions) | Help fill review decisions, explain PA items |
| `reviewed` (addressed) | Deep vetting, cross-concept comparison |
| `synthesized` | Challenge synthesis verdicts, probe risk ratings |

#### Key Bets Framework

For early-stage vetting, the agent should structure its analysis around:

1. **Bets** — "This concept bets that [X] is achievable at scale"
   - Impact if true: [quantified where possible]
   - Impact if false: [what breaks in the economics]
   - Current evidence: [what sources say]

2. **Assumptions** — "The analysis assumes [Y]"
   - Is this unique to this concept or shared?
   - What is the assumption based on?
   - What would change if the assumption is wrong?

3. **Asterisks** — "Flag: [Z]"
   - Why this is noteworthy
   - Whether it's addressed in the analysis

---

### Q3: Reliable Update Handoff Pattern

#### The Problem

Interactive Claude sessions are unreliable for making artifact changes because:
- Context can drift during long conversations
- Edit tool calls in interactive mode may target wrong locations
- No audit trail of what changed and why
- User may discuss many potential changes but only want some applied

#### Proposed Pattern: Change Request Files

Separate the *identification* of changes from the *application* of changes, matching the existing review → address-review pattern.

**Step 1: Interactive session produces `change_requests.md`**

The interactive "manage" agent (Q2) writes structured change requests:

```markdown
# Change Requests: 11-magnetic-mirror
## Generated: 2026-03-28 via /manage-concept

### CR-1: Update plasma beta value
- **Target:** analysis.md §Section 5, Parameter Table
- **Current:** β = 0.15 (no source)
- **Proposed:** β = 0.08-0.12 (range)
- **Source:** arxiv-2411-06644-confinement-predictions.md §Results Table 3
- **Rationale:** Original value appears to be from an older mirror design; WHAM predictions are lower
- **Decision:** _[accept / reject / modify]_

### CR-2: Add new source document findings
- **Target:** analysis.md §Section 1, §Section 5
- **Current:** No mention of Realta 2026 funding round implications
- **Proposed:** Add paragraph noting $25M funding and revised timeline
- **Source:** NEW: realta-series-b-announcement-2026.md
- **Rationale:** Material update to data availability assessment
- **Decision:** _[accept / reject / modify]_
```

**Step 2: User reviews and fills in Decision fields** (same as review.md workflow)

**Step 3: A headless `apply-changes` command processes the file**

```bash
uv run python scripts/run_analysis.py apply-changes 11
```

This is essentially `address-review` but reading from `change_requests.md` instead of `review.md`. The implementation can share the same `parse_proposed_actions` pattern and address-review prompt template.

**Key design decision**: Change requests should be cumulative — multiple interactive sessions can append to the same `change_requests.md`, and the user applies them as a batch. This avoids the "apply one change, re-enter session, find another change" loop.

#### Flowing Updates Downstream

When `apply-changes` modifies `analysis.md`:
- If `model_setup.py` exists and a change affected Section 5 parameters → re-run model-setup (or flag for re-run)
- If `review.md` exists → mark `Review-Status: stale` so the user knows to re-review
- If `synthesis.md` exists → delete or mark stale

This is a "dirty flag" propagation. The simplest implementation:

```python
def propagate_staleness(concept_id, changed_files):
    """After apply-changes, mark downstream artifacts as stale."""
    out_dir = ANALYSES_DIR / concept_id
    if "analysis.md" in changed_files:
        # Model may need regeneration
        model_path = out_dir / "model_setup.py"
        if model_path.exists():
            print(f"  warn: analysis.md changed — consider re-running model-setup")
        # Review is now stale
        review_path = out_dir / "review.md"
        if review_path.exists():
            review_path.rename(out_dir / "review.md.stale")
        # Synthesis is now stale
        synthesis_path = out_dir / "synthesis.md"
        if synthesis_path.exists():
            synthesis_path.rename(out_dir / "synthesis.md.stale")
```

**Alternative**: Instead of renaming to `.stale`, add a `Stale: true` frontmatter field. This preserves the file for reference while marking it as out-of-date. The `status` command can then show a "stale" indicator.

---

### Q4: "build-visuals" Stage

#### Placement and Purpose

New stage between model-setup (3) and review (4):

```
gap-check → analyze → model-setup → build-visuals → review → ...
   (1)        (2)        (3)           (3b)           (4)
```

Purpose: Generate an interactive HTML page with sensitivity sliders so the user can manually explore how parameter changes affect LCOE before the review stage. This is both a sanity check ("does moving thermal efficiency actually change LCOE by the expected amount?") and a discovery tool ("which parameters matter most?").

#### Implementation Pattern

**Input**: `model_setup.py` + `model_output.txt` + `analysis.md` (for parameter names/ranges)

**Output**: `sensitivity_explorer.html` — a single-file HTML page with:
- Sliders for each key parameter (drawn from model_setup.py's forward() arguments)
- Real-time LCOE recalculation (JavaScript reimplementation of the cost model)
- Tornado chart showing sensitivity rankings
- Baseline values and ranges from the analysis

**Prompt approach**: A headless Claude call that:
1. Reads `model_setup.py` to understand the cost model structure
2. Reads `analysis.md` Section 5 for parameter ranges and confidence levels
3. Generates a self-contained HTML file with embedded JS that reimplements the cost calculation
4. Includes reasonable ±20-50% ranges for each parameter (wider for low-confidence values)

**Why single-file HTML**: No build step, no dependencies, opens in any browser, easy to review. Matches the pattern used in `docs/demo/index.html`.

**Validation**: After generation, the script can:
1. Check the file is valid HTML (basic syntax check)
2. Optionally open it in a browser (`xdg-open` or `open`)
3. Compare the baseline LCOE in the HTML against `model_output.txt` — they should match

**Template** (`prompt_templates/build_visuals.md`):

```markdown
# Build Sensitivity Explorer: {{concept_name}}

Read the cost model and analysis, then generate an interactive HTML sensitivity explorer.

## Files to Read
- Model: `{{model_setup_path}}`
- Model output: `{{model_output_path}}`
- Analysis: `{{analysis_path}}` (Section 5 for parameter ranges)

## Output
Write a single self-contained HTML file to: `{{output_path}}`

## Requirements
- Slider for each model.forward() parameter
- Real-time LCOE update as sliders move
- Tornado chart ranking parameters by sensitivity
- Baseline values must match model_output.txt
- Parameter ranges: use analysis.md confidence levels
  (high → ±20%, medium → ±35%, low → ±50%)
- Clean, readable layout
- No external dependencies
```

**stage1-all integration**: Add to the chain after model-setup. If model_setup.py doesn't exist (concept skipped model-setup), skip build-visuals too.

---

### Q5: Manual Data Source Addition and Incremental Updates

#### Current Source Organization

Sources live in `exploration/phase_1a/research/{concept-id}/iter-NN/sources/`:
```
11-magnetic-mirror/
├── dossier.md           # Structured summary
├── iter-01/sources/     # First research pass
│   ├── aps-dpp-2025-sutherland.md
│   ├── arxiv-2411-06644-confinement-predictions.md
│   └── ...
└── iter-02/sources/     # Second research pass
    ├── fusion-report-interview-realta.md
    └── realta-svb-funding-feb2026.md
```

The `find_sources()` function (`run_analysis.py:543-558`) globs `iter-*/sources/*.md` and returns all of them. The analyze prompt includes all source paths.

#### Manual Source Addition Process

**Step 1: Download and extract**

```bash
# Download PDF to a working location
cp ~/Downloads/new-paper.pdf /tmp/

# Extract using agentic-mbse
uv run agentic-mbse extract /tmp/new-paper.pdf --output exploration/phase_1a/research/11-magnetic-mirror/iter-03/sources/

# The extraction creates: iter-03/sources/new-paper/output.md
# Flatten to match expected structure:
mv exploration/phase_1a/research/11-magnetic-mirror/iter-03/sources/new-paper/output.md \
   exploration/phase_1a/research/11-magnetic-mirror/iter-03/sources/new-paper.md
```

**Step 2: Automate this as a pipeline command**

Add an `add-source` subcommand:

```bash
uv run python scripts/run_analysis.py add-source 11 ~/Downloads/new-paper.pdf
```

Implementation:
1. Determine the next `iter-NN` number for the concept
2. Create `iter-NN/sources/` directory
3. Run `uv run agentic-mbse extract <pdf> --output <dir>`
4. Flatten the output (handle the subdirectory nesting)
5. Print confirmation with the new source path
6. Optionally update `dossier.md` with a note about the new source

#### Incremental Analysis Updates

**The problem**: After adding a new source, you don't want to re-run the entire `analyze` stage from scratch — you want a targeted pass that reads the new source and updates the existing analysis.

**Proposed: `update-analysis` subcommand**

```bash
uv run python scripts/run_analysis.py update-analysis 11 --sources iter-03/sources/new-paper.md
```

This runs a new prompt template (`prompt_templates/update_analysis.md`) that:
1. Reads the existing `analysis.md`
2. Reads only the NEW source documents (specified via `--sources` flag)
3. Uses Edit tool to update relevant sections of `analysis.md`
4. Writes an update log to `update_log.md`

The prompt template:

```markdown
# Update Analysis: {{concept_name}}

The analysis has been completed. New source documents have been added.
Review the new sources and update the analysis where the new information
is material.

## Existing Analysis
`{{analysis_path}}`

## New Source Documents
{{new_source_paths}}

## Instructions
1. Read the existing analysis completely
2. Read each new source document
3. For each section of the analysis, determine if the new sources contain
   material information that should be incorporated
4. Use the Edit tool to make targeted updates to `{{analysis_path}}`
5. Do NOT rewrite sections that don't need changes
6. For each edit, add a citation to the new source
7. Write a summary of changes to `{{log_path}}`
```

**Staleness propagation** (same as Q3): After update-analysis modifies `analysis.md`, mark downstream artifacts (review, synthesis) as stale.

**Connection to Q3 (change requests)**: The `update-analysis` command could also produce change requests instead of applying edits directly. This gives the user a review step:

```bash
# Option A: Direct update (for trusted additions)
uv run python scripts/run_analysis.py update-analysis 11 --sources new-paper.md

# Option B: Propose updates (for careful review)
uv run python scripts/run_analysis.py update-analysis 11 --sources new-paper.md --propose-only
# This writes to change_requests.md instead of editing analysis.md
# Then: uv run python scripts/run_analysis.py apply-changes 11
```

Option B is safer and more consistent with the overall pipeline philosophy (human gates before artifact mutation).

---

## Architecture Insights

### Patterns to Preserve

1. **Prompt saved before invocation**: Every stage saves `{stage}_prompt.md` for audit trail. New stages should do the same.
2. **Filesystem-based state**: No database. State derived from file existence and frontmatter. New stages should follow this (e.g., `sensitivity_explorer.html` exists → `visuals-built` state).
3. **Sequential concept processing in analyze**: The reuse pool is re-scanned before each concept. This matters for ordering.
4. **Idempotent re-runs**: Every stage skips if output exists unless `--force`. New stages should follow.
5. **`claude -p` with `--dangerously-skip-permissions`**: Headless calls use Write/Edit tools freely. Interactive sessions (Q2) should NOT use this flag.

### Patterns to Introduce

1. **Change request files**: A general mechanism for proposing artifact mutations. Reusable across interactive agent (Q2), update-analysis (Q5), and potentially review (Q4 could migrate to this).
2. **Staleness propagation**: When upstream artifacts change, downstream artifacts should be marked. Currently this doesn't exist — once review.md exists, nothing invalidates it.
3. **Incremental updates**: The current pipeline is write-once-per-stage. Update-analysis (Q5) and apply-changes (Q3) introduce targeted edits to existing artifacts.

---

## Feasibility Assessment

| Upgrade | Complexity | Dependencies | Risk |
|---------|-----------|-------------|------|
| Q1: Multi-pass analyze | Low | New prompt template only | Low — additive, no changes to existing flow |
| Q2: Interactive agent | Medium | `.claude/commands/` file + state-aware prompt | Low — no pipeline changes needed |
| Q3: Change request handoff | Medium | New file format + `apply-changes` command | Medium — need to handle merge conflicts with existing content |
| Q4: Build-visuals | Medium | New prompt template + HTML validation | Low — isolated new stage |
| Q5: Manual sources | Medium | `add-source` + `update-analysis` commands | Medium — agentic-mbse extraction has known quirks (flatten, output nesting) |

All five are feasible. Q1 and Q2 can be built independently. Q3 and Q5 share the change-request pattern and should be designed together. Q4 is independent.

**Suggested implementation order**: Q1 → Q4 → Q3 → Q5 → Q2

- Q1 is simplest and immediately improves analysis quality
- Q4 is isolated and provides immediate user value
- Q3 establishes the change-request pattern needed by Q5 and Q2
- Q5 builds on Q3's pattern for incremental updates
- Q2 ties everything together as the interactive frontend

---

## Recommendations

1. **Start with Q1 as a separate `quality-check` stage** (not multi-pass within analyze). This is the cleanest addition — one new prompt template, one new `cmd_quality_check`, added to `stage1-all`.

2. **Design the change-request format early** (Q3) since Q2 and Q5 both depend on it. The existing `review.md` PA-N format is a good starting point — extend it slightly for non-review contexts (add a `Source` field for provenance).

3. **For Q2, use `.claude/commands/manage-concept.md`** — this is the standard Claude Code mechanism for custom interactive commands. The command file is a prompt template that gets the concept ID as `$ARGUMENTS`.

4. **For Q4, generate single-file HTML** with embedded JS. The cost models are simple enough (mostly multiplication chains) that a JS reimplementation is tractable. Use the same `invoke_claude` pattern as other stages.

5. **For Q5, implement `add-source` as the first step** — it's useful immediately even without `update-analysis`. Then add `update-analysis --propose-only` which produces change requests (linking to Q3).

---

## Open Questions

1. **Quality-check prompt specifics**: What should the checklist contain? Need to review the handwritten exemplars vs. automated analyses to identify the most common quality gaps.

2. **Change request granularity**: Should a CR be section-level ("rewrite Section 3 with new TRL data") or edit-level ("change β from 0.15 to 0.08-0.12 in the parameter table")? Section-level is easier to write but harder to apply reliably.

3. **Staleness strategy**: Rename to `.stale`? Frontmatter flag? Delete and regenerate? Each has tradeoffs for UX and pipeline complexity.

4. **Build-visuals model constraints**: The HTML needs to reimplement the cost model in JS. For 1costingfe models this is complex (many CAS accounts). May need to simplify to "top-N sensitivity parameters" rather than full model reimplementation.

5. **Interactive agent scope**: Should `/manage-concept` be able to trigger pipeline stages (e.g., "re-run review")? Or should it only produce change requests and leave pipeline execution to the CLI?

## Code References

- `exploration/concept_analysis/scripts/run_analysis.py:469-497` — `invoke_claude()` function (headless Claude call)
- `exploration/concept_analysis/scripts/run_analysis.py:820-921` — `cmd_analyze()` (current single-pass implementation)
- `exploration/concept_analysis/scripts/run_analysis.py:582-632` — `parse_proposed_actions()` (PA-N parsing, reusable for CR-N)
- `exploration/concept_analysis/scripts/run_analysis.py:1125-1225` — `cmd_address_review()` (pattern for applying structured changes)
- `exploration/concept_analysis/scripts/run_analysis.py:543-558` — `find_sources()` (source discovery, relevant for Q5)
- `exploration/concept_analysis/prompt_templates/analysis.md` — current analyze prompt template
- `exploration/concept_analysis/prompt_templates/review.md` — review prompt (PA-N format reference)
- `exploration/concept_analysis/prompt_templates/address_review.md` — address-review prompt (change application pattern)
