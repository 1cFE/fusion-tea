# Concept Analysis Operator Guide

This guide walks you through analyzing a fusion concept end-to-end: from raw research through cost modeling, visual review, and approval. The whole process for one concept typically takes 1-3 sessions depending on source availability and how many issues surface during review.

## What This System Does

The pipeline takes a fusion concept (e.g., "MagLIF" or "HTS Compact Tokamak") and iteratively builds a techno-economic analysis: identifying data gaps, pulling from research sources, constructing a cost model, and assessing the result. An LLM does the heavy lifting at each step; your job is to steer it — adding sources when data is thin, flagging issues when the model looks wrong, and deciding when the analysis is good enough.

The explorer is a local web app that visualizes the cost models so you can actually see what the pipeline produced — LCOE breakdowns, sensitivity charts, CAS cost structures — and compare concepts side by side.

**The two systems form a loop:** pipeline produces artifacts → explorer lets you review them → you file feedback → pipeline iterates.

## Shorthand Used Below

All commands assume you're in the project root (`fusion-tea/`).

```bash
PIPELINE="exploration/concept_analysis/scripts/run_analysis.py"
EXTRACT="exploration/concept_explorer/extract_explorer_data.py"
SERVER="exploration/concept_explorer/server.py"
```

---

## The Short Version

If you just want to get a concept analyzed and visible:

```bash
# 1. Run the pipeline (iterates automatically, ~20 min per pass)
uv run python $PIPELINE analyze 07 --max-passes 5

# 2. Extract data for the explorer
uv run python $EXTRACT --concept 07

# 3. Launch the explorer and open http://127.0.0.1:8421
uv run python $SERVER
```

That's it. The rest of this guide explains what's happening, how to steer it, and what to do when things need fixing.

---

## Step 1: Run the Analysis Pipeline

### Starting a concept

```bash
uv run python $PIPELINE analyze 07
```

This runs the concept through an iterative **analyze → model-setup → assess** loop automatically. Each pass takes roughly 15-25 minutes (it's calling Claude under the hood). By default it does 3 passes — each pass assesses the previous output and tries to fix issues.

You can control how many passes it takes:

```bash
# More passes for complex concepts (MagLIF needed 9)
uv run python $PIPELINE analyze 07 --max-passes 5

# Single pass, no self-assessment (useful for a quick first look)
uv run python $PIPELINE analyze 07 --max-passes 1

# Run 2 more passes from wherever each concept currently is
# (works across multiple concepts at different iterations)
uv run python $PIPELINE analyze 07 11 15 --add-passes 2

# Enable web research (lets the LLM search for papers between iterations)
uv run python $PIPELINE analyze 07 --research
```

`--add-passes N` is the easiest way to extend a run. It implies `--resume` and calculates the right `--max-passes` per concept, so you don't need to know where each one is.

### Convergence is not guaranteed

The pipeline's self-assessor can be picky. A concept might sit at FAIL with 2-3 minor findings for many iterations. **That's fine.** The PASS/FAIL verdict is a quality signal, not a gate. If the cost model runs and the analysis covers the key questions, the concept is ready for human review in the explorer — that's what matters.

### Resuming after interruption

If a run gets interrupted or you want to pick up where you left off:

```bash
uv run python $PIPELINE analyze 07 --resume
```

This skips stages that already have output and continues from the last incomplete step.

### Checking status

```bash
# See all concepts at a glance
uv run python $PIPELINE status

# One concept
uv run python $PIPELINE status 07
```

State codes: `A`=approved, `S`=synthesized, `R`=reviewed, `M`=model-setup, `D`=drafted, `G`=gap-checked, `-`=not started. An asterisk (`*`) means downstream artifacts are stale (something changed upstream).

---

## Step 2: Get It Into the Explorer

The explorer only shows concepts that have been **extracted** — the pipeline and explorer don't share data automatically. After running the pipeline, you need to extract:

```bash
# Extract one concept (fast)
uv run python $EXTRACT --concept 07

# Extract everything that has a model_setup.py or analysis.md
uv run python $EXTRACT

# Skip the slow narrative extraction if you just want numbers
uv run python $EXTRACT --concept 07 --skip-narrative
```

This reads from `exploration/concept_analysis/analyses/` and writes JSON to `exploration/concept_explorer/data/`. The server loads from that `data/` directory.

Then start the server if it's not already running:

```bash
uv run python $SERVER
# Open http://127.0.0.1:8421
```

If the server is already running, just reload the browser after re-extracting.

---

## Step 3: Start With the Landscape

Before diving into any single concept's numbers, start with the taxonomy page to get your bearings. The taxonomy shows **all 38 concepts** — no extraction needed — so you can see the full design space even before running a single pipeline pass.

### Taxonomy page (`/taxonomy`)

Go to **http://127.0.0.1:8421/taxonomy**. Three views, each showing the full concept landscape:

- **Decision tree** (left panel) — The classification hierarchy. Expand branches to see how concepts are grouped: MFE vs IFE vs MIF, then by sub-type (tokamak, stellarator, mirror, z-pinch, etc.). Click any concept to focus it.
- **Constellation** (center) — A 2D scatter plot where similar concepts cluster together. This is the quickest way to get a feel for the design space. Are the clusters sensible? Is anything obviously misclassified? Double-click a concept to focus it and see its neighborhood.
- **Neighborhood graph** — After focusing a concept, this shows its nearest neighbors with similarity scores. Click a neighbor to see a field-by-field comparison of their taxonomy attributes. This is pure qualitative comparison — no cost model needed.

**What to look for:**
- Is each concept in the right branch of the decision tree?
- Do the constellation clusters make physical sense? (e.g., all stellarators near each other, all IFE concepts grouped)
- When you compare neighbors, do the taxonomy attributes (confinement, fuel cycle, magnet type, etc.) line up with your expectations?

### Qualitative comparison from the taxonomy

You can compare any two concepts purely on their taxonomy attributes without needing extracted cost data:

1. **Focus a concept** — click it in the tree or double-click it in the constellation
2. **Click a neighbor** in the neighborhood list — this shows a side-by-side attribute comparison (shared vs. divergent fields, bridge concepts that connect them)
3. **Build a selection** — Ctrl+click (Cmd+click on Mac) concepts in any view to add them to the **selection tray** at the bottom of the page. The tray collects concepts as you browse.
4. **Launch comparison** — Once you have 2-3 concepts in the tray, click "Compare" to jump to the comparison page

The **Categorical** view on the comparison page works for all concepts (it reads from the taxonomy registry). The **Summary**, **CapEx**, and **Sensitivity** views require extracted cost model data — those will only populate for concepts you've run through the pipeline and extraction step.

This is a good workflow for deciding which concepts to analyze next: browse the landscape, find interesting clusters or outliers, then go run the pipeline on the ones that matter.

---

## Step 4: Review Extracted Concepts

Once you've run the pipeline and extracted data (Steps 1-2), the explorer shows the quantitative results.

### Index page (`/`)

The grid shows all **extracted** concepts, split into **Approved** (green) and **In Progress** (amber). Each card has the concept name, confinement family, company, LCOE, and confidence level.

**Things that should make you squint:**
- LCOE below $10/MWh or above $500/MWh (probably a modeling error)
- Wrong confinement family (tokamak labeled as IFE, etc.)
- "Low" confidence on a well-studied concept with good sources

### Concept profile (`/concept/{id}`)

This is the main review page for a single concept. Top to bottom:

- **Headline economics** — LCOE, overnight capital cost, net power, Q_eng, capacity factor. Quick sanity check: Q_eng should be > 1 (otherwise it's a net energy sink), capacity factor between 0.30-0.95.
- **Narrative** — The economic thesis: what costs are eliminated, what's novel, what are the key bets. Does the story make sense for this concept type?
- **Tornado chart** — Sensitivity bars ranked by how much each parameter moves LCOE. The dominant parameters should match your intuition (e.g., availability and rep-rate for pulsed concepts, magnet cost for stellarators).
- **CAS breakdown** — Cost structure with expandable CAS22 sub-accounts. Check that the right accounts are present: a tokamak should have magnet costs, a MagLIF should have a target factory, a steady-state concept shouldn't have per-shot consumables.
- **Sliders** — Drag parameters to see LCOE respond in real-time. Great for testing "what if" scenarios.

### Side-by-side comparison (`/compare`)

If you collected concepts in the taxonomy selection tray, you're already here. Otherwise, select 2-3 concepts from the index page. Four views:

| View | What it shows | Good for | Needs extraction? |
|------|--------------|----------|-------------------|
| Categorical | Taxonomy attributes | Classification consistency | No |
| Summary | LCOE drivers | Comparing economic structure | Yes |
| CapEx | CAS stacked bars | Spotting cost structure outliers | Yes |
| Sensitivity | Tornado overlays | Comparing which parameters matter | Yes |

---

## Step 5: Fix Issues

When the explorer reveals problems — wrong cost accounts, missing data, implausible sensitivities — you have two tools:

### `/manage-concept` for interactive triage

```
/manage-concept 07
```

This loads the concept's full context in Claude Code and lets you explore it interactively. You can ask questions about the model, identify issues, and write change requests. The command adapts to the concept's current state (drafted, reviewed, synthesized, etc.).

**Important:** Don't edit `analysis.md` by hand. Changes should flow through `change_requests.md` so the pipeline can incorporate them properly.

### Adding sources when data is thin

If a cost account looks wrong because there simply isn't good source data:

```bash
# Add a PDF or URL
uv run python $PIPELINE add-source 07 /path/to/paper.pdf
uv run python $PIPELINE add-source 07 https://example.com/report.pdf

# Preview what it'll do without actually extracting
uv run python $PIPELINE add-source 07 /path/to/paper.pdf --dry-run
```

### Re-running after changes

After filing change requests or adding sources, re-run the pipeline to incorporate them:

```bash
uv run python $PIPELINE analyze 07 --resume
```

Then re-extract and check the explorer:

```bash
uv run python $EXTRACT --concept 07 --skip-narrative
```

Reload the browser. Repeat until it looks right.

---

## Step 6: Approval (When You're Ready)

Once a concept's analysis holds up under review, the formal path is:

```bash
# 1. Structured review — produces review.md with PROCEED/REVISE verdict
uv run python $PIPELINE review 07

# 2. If REVISE: re-run pipeline, then review again
uv run python $PIPELINE analyze 07 --resume

# 3. If PROCEED with proposed actions: address them, then...
uv run python $PIPELINE address-review 07

# 4. Generate editorial synthesis
uv run python $PIPELINE synthesize 07

# 5. Approve
uv run python $PIPELINE approve 07
```

After approval, re-extract one more time — the concept moves from "In Progress" to "Approved" on the explorer index page.

**Shortcut:** If you're confident and want to skip synthesis:

```bash
uv run python $PIPELINE approve 07 --force
```

---

## Reference: All Pipeline Commands

| Command | What it does |
|---------|-------------|
| `status [ID]` | Show state table (all concepts or one) |
| `list` | List all concepts with IDs |
| `gap-check ID` | Run gap assessment only |
| `analyze ID [--max-passes N] [--add-passes N] [--resume] [--research]` | Iterative analysis loop (analyze → model-setup → assess) |
| `model-setup ID` | Generate cost model only |
| `review ID` | Structured review with verdict |
| `address-review ID` | Apply decisions from review |
| `synthesize ID` | Generate editorial synthesis |
| `approve ID [--force]` | Mark concept as approved |
| `add-source ID PATH [--name NAME] [--dry-run]` | Add a PDF or URL source |

Common flags on most commands: `--model MODEL` (default: sonnet), `--dry-run`, `--timeout SECONDS`, `--force`.
