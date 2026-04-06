# Concept Analysis Pipeline

Automated pipeline for producing D1+ techno-economic analyses of ~38 fusion
concepts. Uses headless Claude (`claude -p`) with template-driven prompts,
an approval-based cross-concept reuse pool, and filesystem-based state tracking.

## Quick Start

```bash
cd exploration/concept_analysis

# See all 38 concepts
uv run python scripts/run_analysis.py list

# Check progress
uv run python scripts/run_analysis.py status

# Run everything through review for one or more concepts
uv run python scripts/run_analysis.py stage1-all 02 03 04

# Dry-run to preview prompts without calling Claude
uv run python scripts/run_analysis.py stage1-all 02 --dry-run
```

## Pipeline Stages

The pipeline has 6 core stages plus utility commands. Each is a subcommand
of `run_analysis.py`.

```
[gap-check] → analyze ⟲ assess → model-setup → review → synthesize → approve
   (opt)        (2)                   (3)          (4)       (5)         (6)
                  ↑                                 ↑
          iterative loop                   human inspection gate
        (--max-passes, default 3)

Side channels:
  add-source → update-analysis     (incremental source addition)
```

| Stage | Command | What it does | Output |
|-------|---------|-------------|--------|
| 1 (opt) | `gap-check` | Assess source coverage gaps | `gap_report.md` |
| 2 | `analyze` | Iterative D1+ analysis (analyze → assess loop) | `analysis.md` + `feedback_iter_N.md` |
| 3 | `model-setup` | Generate Python cost model (1costingfe or free-form) | `model_setup.py` + `model_output.txt` |
| 4 | `review` | Structured review with proposed actions | `review.md` |
| 4b | `address-review` | Apply user decisions from review | Updates `analysis.md` / `model_setup.py` |
| 5 | `synthesize` | Editorial synthesis with cross-concept context | `synthesis.md` |
| 6 | `approve` | Mark as approved (enters reuse pool) | Sets `Status: approved` in frontmatter |
| — | `add-source` | Add a PDF or URL source to a concept | Extracted source in `iter-NN/sources/` |
| — | `update-analysis` | Incorporate new sources into existing analysis | Updates `analysis.md` (marks downstream stale) |

### Composite Command

**`stage1-all`** chains analyze → model-setup → review in one invocation.
Gap-check is **opt-in** via `--include-gap-analysis`.

```bash
# Single concept
uv run python scripts/run_analysis.py stage1-all 11

# Multiple concepts
uv run python scripts/run_analysis.py stage1-all 02 03 04 05

# All remaining, filtered by family
uv run python scripts/run_analysis.py stage1-all --all --family MFE

# Include gap-check (skipped by default)
uv run python scripts/run_analysis.py stage1-all 11 --include-gap-analysis
```

After `stage1-all`, you read the generated `review.md` files, fill in
Decision fields for each proposed action, then continue:

```bash
uv run python scripts/run_analysis.py address-review 02
uv run python scripts/run_analysis.py synthesize 02
uv run python scripts/run_analysis.py approve 02
```

## Subcommand Reference

### Concept Selection

Every stage subcommand accepts concepts by:

- **Numeric prefix**: `01`, `17a`
- **Full ID**: `01-hts-compact-tokamak`
- **Partial name/company** (case-insensitive): `Commonwealth`, `tokamak`
- **`--all`**: All remaining concepts (skips those already at the target state)
- **`--family`**: Filter by confinement family (`MFE`, `IFE`, `MIF`, `Non-Standard`)

### Common Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--model` | `sonnet` | Claude model (`sonnet`, `opus`, `haiku`) |
| `--dry-run` | off | Generate and save prompts without calling Claude |
| `--force` | off | Re-run even if output files already exist |
| `--timeout` | 900 | Per-invocation timeout in seconds |

**Stage-specific flags:**

| Flag | Stages | Default | Description |
|------|--------|---------|-------------|
| `--max-passes` | `analyze`, `stage1-all` | 3 | Max analyze→assess iterations (1 = no assessment) |
| `--feedback PATH` | `analyze` | — | Apply a feedback file to existing analysis (skips cold-start) |
| `--include-gap-analysis` | `stage1-all` | off | Include gap-check stage (skipped by default) |

### Individual Stages

```bash
# Stage 1: Gap check
uv run python scripts/run_analysis.py gap-check 02 03

# Stage 2: Full analysis (sequential — each sees the reuse pool)
uv run python scripts/run_analysis.py analyze 02 03

# Stage 3: Generate cost model
uv run python scripts/run_analysis.py model-setup 02 03

# Stage 4: Automated review
uv run python scripts/run_analysis.py review 02

# Stage 4b: Apply review decisions (after human fills in Decision fields)
uv run python scripts/run_analysis.py address-review 02

# Stage 5: Synthesis (requires Review-Status = addressed or clean)
uv run python scripts/run_analysis.py synthesize 02

# Stage 6: Approve (requires synthesis unless --force)
uv run python scripts/run_analysis.py approve 02

# Add a new source (PDF or URL) to a concept
uv run python scripts/run_analysis.py add-source 17a /path/to/paper.pdf
uv run python scripts/run_analysis.py add-source 11 https://example.com/article

# Update analysis to incorporate newly added sources
uv run python scripts/run_analysis.py update-analysis 17a --sources sparc-icrf-heating-paper
```

### Info Commands

```bash
# List all 38 concepts with ID, name, company, family
uv run python scripts/run_analysis.py list

# Status table (all or filtered)
uv run python scripts/run_analysis.py status
uv run python scripts/run_analysis.py status --family MFE
uv run python scripts/run_analysis.py status 01 07 11
```

## State Detection

State is determined by filesystem inspection — no database. Detection order
(highest to lowest):

| State | Condition |
|-------|-----------|
| `approved` | `analysis.md` exists with `Status: approved` |
| `synthesized` | `synthesis.md` exists |
| `reviewed` | `analysis.md` has `Review-Status: addressed` or `clean` |
| `model-setup` | `model_setup.py` exists |
| `drafted` | `analysis.md` exists |
| `gap-checked` | `gap_report.md` exists |
| `not-started` | None of the above |

A `*` suffix (e.g., `model-setup*`) indicates **stale downstream artifacts** —
`analysis.md` was updated (via feedback pass, `update-analysis`, or
`/manage-concept`) after those artifacts were generated. Re-run the stale
stage(s) to reconcile.

Every stage checks prerequisites and skips concepts that already have output,
making re-runs safe and idempotent.

## Cross-Concept Reuse Pool

The `analyze` stage scans for all approved prior analyses and injects their
paths into the prompt. Claude reads them and reuses consistent assumptions
(materials costs, discount rates, shared subsystems) with attribution.

This means **ordering matters for `analyze`**: earlier concepts provide inputs
to later ones. The stage processes concepts sequentially, re-scanning the
approved pool before each concept.

Approved analyses are tracked via the `Status: approved` field in
`analysis.md` YAML frontmatter. The `Reuses: []` field records which prior
concepts were referenced.

## Shared Memory

The `memory/` directory accumulates cross-concept learnings (common pitfalls,
parameter sanity ranges, recurring feedback patterns). The `analyze` stage
loads relevant memories before each run via a memory-handler subagent. Memories
are saved explicitly — via the interactive `/manage-concept` agent or after
review sessions.

## Directory Layout

```
concept_analysis/
├── README.md                    # This file
├── table.csv                    # 38-concept registry (read-only reference)
├── concept_analysis_brief.md    # D1+ deliverable specification
├── add_ids.py                   # Helper: map concept names → canonical IDs
├── scripts/
│   └── run_analysis.py          # Pipeline orchestrator (single entry point)
├── prompt_templates/            # Stage-specific prompt templates
│   ├── gap_check.md             #   Stage 1 prompt
│   ├── analysis_v2.md           #   Stage 2 prompt (modal: cold-start / feedback / self-advance)
│   ├── assessment.md            #   Stage 2 assessment prompt (analyze→assess loop)
│   ├── source_integration.md    #   update-analysis pre-pass prompt
│   ├── output_template.md       #   D1+ output section structure
│   ├── model_setup_costingfe.md #   Stage 3 prompt (1costingfe path)
│   ├── model_setup_freeform.md  #   Stage 3 prompt (free-form path)
│   ├── review.md                #   Stage 4 prompt
│   ├── address_review.md        #   Stage 4b prompt
│   ├── synthesis.md             #   Stage 5 prompt
│   ├── config/                  #   Extracted goals and checklists
│   │   ├── analysis_goals.md    #     What the analysis should cover
│   │   ├── assessment_checklist.md #  What the assessor checks
│   │   ├── review_checklist.md  #     Numerical accuracy checks (for review stage)
│   │   ├── quality_standards.md #     Citation format, anti-hallucination, depth
│   │   └── feedback_format.md   #     Structured feedback entry format
│   └── agents/
│       └── source_reader.md     #   Subagent prompt for source reading
├── memory/                      # Cross-concept shared learnings
│   └── learnings.md             #   Accumulated insights from analysis sessions
├── handwritten/                 # Human-written exemplar analyses
│   ├── 01-hts-compact-tokamak.md
│   ├── 07-maglif.md
│   ├── 07-maglif.py
│   ├── 08-frc-w-direct-conversion.md
│   ├── 11-magnetic-mirror.md
│   ├── 11-magnetic-mirror.py
│   ├── 11-magnetic-mirror-comparison.md
│   └── 26-laser-icf-indirect-drive.md
└── analyses/                    # Generated outputs (one dir per concept)
    ├── 01-hts-compact-tokamak/
    ├── 02-acoustic-icf-sonofusion/
    ├── ...                      # 38 concept directories
    └── 36-helical-coil-stellarator/
```

### Per-Concept Output Files

A fully completed concept directory contains:

```
analyses/{concept-id}/
├── gap_check_prompt.md      # Saved Stage 1 prompt (audit trail)
├── gap_report.md            # Stage 1 output: source coverage assessment
├── analysis_prompt.md       # Saved Stage 2 prompt (each iteration)
├── analysis.md              # Stage 2 output: D1+ analysis (YAML frontmatter + body)
├── feedback_iter_1.md       # Assessment feedback from iteration 1
├── feedback_iter_2.md       # Assessment feedback from iteration 2 (if needed)
├── assessment_prompt.md     # Saved assessment prompt
├── model_setup_prompt.md    # Saved Stage 3 prompt
├── model_setup.py           # Stage 3 output: runnable Python cost model
├── model_output.txt         # Model execution output (LCOE values)
├── review_prompt.md         # Saved Stage 4 prompt
├── review.md                # Stage 4 output: findings + proposed actions
├── address_review_prompt.md # Saved Stage 4b prompt (if review had actions)
├── address_log.md           # Log of applied review actions
├── synthesis_prompt.md      # Saved Stage 5 prompt
└── synthesis.md             # Stage 5 output: editorial synthesis (YAML frontmatter + body)
```

Every prompt is saved before invocation for full reproducibility.

## YAML Frontmatter

### analysis.md

```yaml
---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (D-T)
Company: Realta Fusion
Status: draft              # draft → approved
Created: 2026-03-20
Approved-Date:             # set on approval
Reuses: []                 # prior concept IDs referenced
Review-Iterations: 1       # incremented each review cycle
Last-Review: 2026-03-20
Review-Status: addressed   # has-actions → addressed → clean
---
```

### synthesis.md

```yaml
---
ID: 11-magnetic-mirror
Concept: Magnetic Mirror (D-T)
Company: Realta Fusion
Type: synthesis
Status: draft              # draft → approved
Created: 2026-03-20
---
```

## Model Setup Paths

Each concept maps to one of two model generation paths:

**1costingfe path** (29 concepts) — generates a script using the
[1costingfe](../../1costingfe/) library with family-level defaults
(e.g., `mfe_tokamak.yaml`) and concept-specific overrides.

**Free-form path** (9 concepts: 12, 13, 15, 16, 18, 19, 24, 27, 35) —
concepts without a clean 1costingfe mapping get a standalone Python LCOE
model using `maglif_lcoe_model.py` as a structural reference.

After generating `model_setup.py`, the pipeline automatically executes it
and saves output to `model_output.txt`, checking that LCOE appears in the
results.

## Review Workflow

The review stage produces structured findings with proposed actions:

```markdown
### PA-1: Missing citation for plasma beta assumption
- **Category:** Citation gap
- **Severity:** medium
- **Location:** analysis.md, §Plasma Parameters
- **Finding:** Beta value of 0.15 has no source citation
- **Proposed Fix:** Add citation from [source] §section
- **Decision:** _[fill in: accept / reject / modify]_
- **User Notes:** _[optional context]_
```

After reading `review.md`, fill in the **Decision** and **User Notes** fields,
then run `address-review` to apply the changes. The cycle can repeat
(`review` → `address-review` → `review` → ...) until the review comes back
clean.

## Data Sources

Each concept's analysis draws from:

1. **Phase 1a research dossier** — `knowledge/concept_research/{concept-id}/dossier.md`
2. **Extracted source documents** — `knowledge/concept_research/{concept-id}/iter-*/sources/*.md`
3. **Handwritten exemplars** — `handwritten/*.md` (injected as quality references)
4. **Approved prior analyses** — the reuse pool (discovered automatically)
5. **Shared memory** — `memory/learnings.md` (cross-concept accumulated insights)
