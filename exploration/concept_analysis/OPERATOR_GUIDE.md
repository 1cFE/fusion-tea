# Concept Analysis Operator Guide

How to take a fusion concept from initial analysis through explorer-based review to final approval.

## Typical Workflow

```
Pipeline                          Explorer                         Pipeline
────────                          ────────                         ────────
status → stage1-all ──────────→ extract → server ──────────────→ /manage-concept
  (gap → analyze → model-setup     (review in browser)             (triage issues)
   → review)                                                            │
       ▲                                                                │
       │                                                                ▼
       └──── stage1-all --resume ◄──── change_requests.md ◄──── file change requests
                    │
                    ▼
              address-review → synthesize → approve
                                               │
                                               ▼
                                    re-extract → concept shows
                                                 as "Approved"
```

All commands below use this base path:

```bash
PIPELINE="exploration/concept_analysis/scripts/run_analysis.py"
EXTRACT="exploration/concept_explorer/extract_explorer_data.py"
SERVER="exploration/concept_explorer/server.py"
```

---

## 1. Pipeline Quick Reference

### Check concept status

```bash
# All concepts
uv run python $PIPELINE status

# Single concept
uv run python $PIPELINE status 01

# Filter by confinement family
uv run python $PIPELINE status --family MFE
```

The status table shows state codes: `A`=approved, `S`=synthesized, `R`=reviewed, `M`=model-setup, `D`=drafted, `G`=gap-checked, `-`=not-started. An asterisk (`*`) means downstream artifacts are stale.

### Run the full pipeline

```bash
# Run one concept through gap-check → analyze → model-setup → review
uv run python $PIPELINE stage1-all 01

# Multiple concepts
uv run python $PIPELINE stage1-all 01 07 09

# All remaining concepts
uv run python $PIPELINE stage1-all --all

# Resume after interruption or failure
uv run python $PIPELINE stage1-all 01 --resume

# Enable autonomous web research between iterations
uv run python $PIPELINE stage1-all 01 --research

# Control iteration depth (default: 3; 1 = single pass, no assessment)
uv run python $PIPELINE stage1-all 01 --max-passes 5

# Re-run even if output exists
uv run python $PIPELINE stage1-all 01 --force
```

### Add a source

```bash
# Add a PDF
uv run python $PIPELINE add-source 01 /path/to/paper.pdf

# Add a URL (will be extracted)
uv run python $PIPELINE add-source 01 https://example.com/report.pdf

# Override automatic source name
uv run python $PIPELINE add-source 01 /path/to/paper.pdf --name "smith-2024-compact-tokamak"

# Preview without extracting
uv run python $PIPELINE add-source 01 /path/to/paper.pdf --dry-run
```

### Other pipeline commands

```bash
# Structured review with proposed actions
uv run python $PIPELINE review 01

# Apply user decisions from review
uv run python $PIPELINE address-review 01

# Generate editorial synthesis
uv run python $PIPELINE synthesize 01

# Approve a concept (requires review + synthesis)
uv run python $PIPELINE approve 01

# Approve without synthesis (use sparingly)
uv run python $PIPELINE approve 01 --force
```

Common flags available on most commands: `--model MODEL` (default: sonnet), `--dry-run`, `--timeout SECONDS`, `--force`.

---

## 2. Launching the Explorer

### Prerequisites

At least one concept must have reached the `model-setup` state (has a `model_setup.py` file in its analysis directory). Concepts without `model_setup.py` won't appear in the explorer.

### Step 1: Extract data

The extraction script reads pipeline artifacts from `exploration/concept_analysis/analyses/` and writes JSON to `exploration/concept_explorer/data/`.

```bash
# Extract all concepts that have model_setup.py
uv run python $EXTRACT

# Extract specific concepts
uv run python $EXTRACT --concept 01 07 09

# Skip LLM-based narrative extraction (faster, sets narrative=null)
uv run python $EXTRACT --concept 01 --skip-narrative
```

### Step 2: Start the server

```bash
uv run python $SERVER
```

The server starts at **http://127.0.0.1:8421**. It loads all JSON files from `exploration/concept_explorer/data/` on startup.

To use a different port:

```bash
uv run python $SERVER --port 9000
```

---

## 3. Explorer Tour — Sanity-Checking a Concept

### Index Page (`/`)

Two sections: **Approved** (green) and **In Progress** (amber). Each card shows: concept name, confinement family badge, company, LCOE, and confidence level.

**Red flags to check:**
- LCOE wildly outside expected range for the concept type (e.g., < $10/MWh or > $500/MWh)
- Wrong confinement family badge
- Missing company/organization
- Confidence showing "low" for a well-studied concept

### Concept Profile (`/concept/{id}`)

The main review page for a single concept. Sections from top to bottom:

- **Hero**: Name, confinement family, company — verify basic metadata is correct
- **Headline Economics**: LCOE, overnight cost, P_net, Q_eng, capacity factor — check physical reasonableness
- **Narrative**: Key bets, eliminated costs, novel costs — does the economic thesis make sense?
- **Risk Table**: Are risks well-characterized? Do they have retirement paths?
- **Tornado Chart**: Sensitivity bars ranked by elasticity — which parameters dominate LCOE? Are the ±ranges physically plausible?
- **CAS Breakdown**: Stacked bar with expandable CAS22 sub-accounts — does the cost structure match expectations for this concept type?
- **Sliders** (costingfe concepts only): Adjust parameters to see LCOE response in real-time

**Red flags to check:**
- Q_eng < 1 (net energy loss)
- Capacity factor > 0.95 or < 0.30 without justification
- Dominant sensitivity parameter with implausibly wide range
- CAS22 account missing that should be present (e.g., no magnet cost for a magnetic confinement concept)
- CAS22 account present that shouldn't be (e.g., target factory cost for a steady-state tokamak)

### Comparison Page (`/compare`)

Select 2–3 concepts for side-by-side analysis. Two layout modes:

- **Integrated**: Side-by-side with independent view selectors per concept
- **Landscape**: Grid layout with unified view across all selected concepts

Four views available:

| View | Shows | Use for |
|------|-------|---------|
| Categorical | Taxonomy attributes | Verifying classification consistency |
| Summary | LCOE drivers | Comparing economic structure |
| CapEx | CAS stacked bars | Spotting cost structure outliers |
| Sensitivity | Tornado overlays | Comparing parameter sensitivity |

**Red flags to check:**
- Two concepts of the same type with dramatically different cost structures
- A concept's sensitivity profile that doesn't match its peers
- Taxonomy attributes that should be the same across a family but differ

### Taxonomy Page (`/taxonomy`)

- **Decision Tree** (left): Collapsible classification hierarchy
- **Constellation** (center): 2D scatter of all concepts by similarity — are clusters sensible?
- **Neighborhood Graph**: Double-click a concept to see its nearest neighbors
- **Selection Tray** (bottom): Collect concepts, then click "Compare" to jump to comparison

**Red flags to check:**
- A concept classified in the wrong branch of the decision tree
- A concept clustered far from its expected peers in the constellation
- Unexpected neighbors in the neighborhood graph

---

## 4. Issue Triage via `/manage-concept`

When the explorer reveals issues, use the `/manage-concept` command in Claude Code:

```
/manage-concept <concept-id>
```

The command loads the concept's full context and presents stage-appropriate options:

| Mode | When (state) | What you can do |
|------|-------------|-----------------|
| A | `drafted` or `model-setup` | Identify key bets and flags, write change requests |
| B | `reviewed` | Walk through PA-N proposed actions, fill Decision fields |
| C | `synthesized` or `approved` | Challenge synthesis verdicts, deep-vet assumptions |
| D | `not-started` or `gap-checked` | Get guidance on next pipeline step to run |

**Important:** Never edit `analysis.md` directly. All changes flow through `change_requests.md`:

1. Use `/manage-concept` to identify issues and write change requests
2. Re-run the pipeline with feedback:
   ```bash
   uv run python $PIPELINE stage1-all <concept-id> --resume
   ```
3. Re-extract and verify in the explorer

---

## 5. Adding Sources Mid-Review

If the explorer reveals a data gap (missing CAS account detail, uncertain parameter, thin sourcing):

1. **Find the source** — paper, technical report, vendor datasheet
2. **Add it to the concept:**
   ```bash
   uv run python $PIPELINE add-source <concept-id> /path/to/source.pdf
   ```
   Source extraction uses agentic-mbse and may take a few minutes depending on document size.
3. **Re-run analysis** to incorporate the new source:
   ```bash
   uv run python $PIPELINE stage1-all <concept-id> --resume
   ```
4. **Re-extract and refresh** the explorer to verify the improvement:
   ```bash
   uv run python $EXTRACT --concept <concept-id> --skip-narrative
   ```
   Then reload the browser.

---

## 6. Final Review, Feedback, and Synthesis

Once you're satisfied with a concept's analysis after explorer review:

### Step 1: Run structured review

```bash
uv run python $PIPELINE review <concept-id>
```

This produces a `review.md` file with a **PROCEED** or **REVISE** verdict, plus proposed actions (PA-1, PA-2, ...) with Decision fields.

### Step 2: Handle the verdict

**If REVISE:** The review findings become feedback for the next iteration.
```bash
uv run python $PIPELINE stage1-all <concept-id> --resume
```
Then repeat from Step 1.

**If PROCEED with proposed actions:** Fill in the Decision fields in `review.md` (via `/manage-concept` Mode B or an editor), then apply:
```bash
uv run python $PIPELINE address-review <concept-id>
```

**If PROCEED clean** (no proposed actions): Skip to Step 3.

### Step 3: Synthesize

```bash
uv run python $PIPELINE synthesize <concept-id>
```

Generates an editorial synthesis summarizing the concept's economics, key bets, risks, and comparison context.

### Step 4: Verify in explorer

Re-extract and check the final state in the browser:
```bash
uv run python $EXTRACT --concept <concept-id>
```

---

## 7. Final Approval

### Prerequisites

- Review verdict is PROCEED (with actions addressed, or clean)
- Synthesis is complete

### Approve

```bash
uv run python $PIPELINE approve <concept-id>
```

This sets `Status: approved` in the concept's `analysis.md` and `synthesis.md` frontmatter.

To approve without synthesis (use sparingly):
```bash
uv run python $PIPELINE approve <concept-id> --force
```

### Verify

Re-extract explorer data:
```bash
uv run python $EXTRACT --concept <concept-id> --skip-narrative
```

Reload the browser — the concept moves from "In Progress" to "Approved" on the index page. The approved analysis joins the reuse pool for future concepts.
