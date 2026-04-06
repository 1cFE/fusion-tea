# Design: Automated Concept Analysis

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-20
**Updated:** 2026-03-20
**Branch:** design-space-explore
**Commit:** 8c8db45

## Overview

A headless Claude pipeline that produces D1+ concept analyses for ~29 remaining fusion concepts, using Phase 1a dossiers and extracted sources as input. Borrows the orchestration pattern from `exploration/phase_1a/scripts/run_concept.py` (template-driven, `claude -p`, immutable prompt artifacts).

## Related Artifacts

- **Concept:** `.project/concepts/automated-concept-analysis.md`
- **Brief:** `exploration/concept_analysis/concept_analysis_brief.md`
- **Canonical table:** `exploration/concept_analysis/table.csv` (38 concepts × 21 columns, with ID)
- **Exemplars:** `exploration/concept_analysis/handwritten/{01,07,26}-*.md`
- **Phase 1a orchestrator:** `exploration/phase_1a/scripts/run_concept.py` (pattern source)
- **Phase 1a templates:** `exploration/phase_1a/prompt_templates/{research,synthesis}.md`

---

## Research Findings

### Existing Infrastructure Patterns

**Phase 1a orchestrator** (`run_concept.py`, 596 lines):
- Template-driven: Handlebars-style `{{variable}}` substitution with `{{#if}}/{{#unless}}` conditionals
- `claude -p --dangerously-skip-permissions --verbose` via subprocess stdin
- Concept lookup: by dir name, numeric index, slug, or partial company name (`find_concept()`)
- Gap detection: regex-parses dossier for TBD/Unknown/low-confidence columns
- Immutable artifacts: prompt saved before invocation, output saved after
- `--dry-run`: generates prompts without invoking Claude
- `--list`: prints all concepts

**Phase 2a expander** (`expand.py`, 475 lines):
- Streaming: `--output-format stream-json` for real-time progress
- JSON repair: handles LLM quirks like `{"bare_value"}` set literals
- Popen-based (non-blocking) vs. Phase 1a's subprocess.run (blocking)

**Phase 1a prompt templates**:
- Research template: instructs agent to search web, save sources, report per-column
- Synthesis template: instructs agent to read files by absolute path, apply merge rules
- Both reference schema for vocabulary grounding

### Handwritten Exemplar Structure

The three exemplars have different structures but share a core:

| Exemplar | Sections | Length | Notes |
|----------|----------|--------|-------|
| `01-hts-compact-tokamak.md` | D1 only (4 sections + sources) | 133 lines | Family-level analysis, tokamak-wide |
| `26-laser-icf-indirect-drive.md` | D1 partial + comparison table | ~78 lines | Inertia vs Xcimer side-by-side |
| `07-maglif.md` | D1 + D2 + deep dives + material analysis | ~450 lines | Most complete, includes code model |

Common D1 sections across all three:
1. Availability of Data (with rating: Rich/Moderate/Limited/Opaque)
2. Challenges in Capturing System Function
3. Maturity of Key Subsystems and Components (TRL assessments)
4. Key Materials and Supply Chain Considerations

### Phase 1a Data Available Per Concept

Each concept directory in `exploration/phase_1a/research/NN-slug/` contains:
- `dossier.md`: 80-120 lines, 12 structured columns with value/confidence/citation/notes
- `changelog.md`: iteration history with what changed
- `iter-NN/output.md`: raw research output per cycle
- `iter-NN/sources/`: 1-3 extracted markdown documents (varying length, typically 5-50 pages)
- `iter-NN/prompt.md`: saved research prompt (immutable)

Source documents are the richest input — they contain the actual technical content the dossier was derived from.

---

## Proposed Design

### Workflow Stages

```
                    ┌─────────────────────────────────────────────┐
                    │          CONCEPT ANALYSIS PIPELINE          │
                    └─────────────────────────────────────────────┘

  Per-concept state: (not started) → gap-checked → drafted → approved

  ╔═══════════════╗     ╔═══════════════╗     ╔═══════════════╗     ╔═══════════════╗
  ║   STAGE 1     ║     ║   STAGE 2     ║     ║   STAGE 3     ║     ║   STAGE 4     ║
  ║   GAP CHECK   ║────▶║   ANALYZE     ║────▶║   REVIEW      ║────▶║   APPROVE     ║
  ║               ║     ║               ║     ║               ║     ║               ║
  ║ Can run in    ║     ║ Sequential —  ║     ║ Human reads   ║     ║ Human marks   ║
  ║ parallel for  ║     ║ reads prior   ║     ║ draft, edits  ║     ║ approved via  ║
  ║ all concepts  ║     ║ approved work ║     ║ if needed     ║     ║ CLI command   ║
  ╚═══════════════╝     ╚═══════════════╝     ╚═══════════════╝     ╚═══════════════╝
        │                      │                     │                      │
        ▼                      ▼                     ▼                      ▼
  ┌───────────┐         ┌───────────┐         ┌───────────┐         ┌───────────┐
  │gap_report │         │analysis.md│         │ (human    │         │analysis.md│
  │    .md    │         │Status:    │         │  edits    │         │Status:    │
  │           │         │  draft    │         │  in-place)│         │  approved │
  └───────────┘         └───────────┘         └───────────┘         └───────────┘
                                                                         │
                                                                         ▼
                                                                  ┌─────────────┐
                                                                  │ REUSE POOL  │
                                                                  │ visible to  │
                                                                  │ subsequent  │
                                                                  │ analyses    │
                                                                  └─────────────┘
```

**Stage 1 — GAP CHECK** (parallelizable):
- **Input**: Phase 1a dossier + list of source files + schema + brief
- **Agent**: Headless Claude reads dossier, scans available sources, assesses coverage against the 4 D1 sections + D2 parameter needs
- **Output**: `gap_report.md` — structured assessment of what data exists vs. what's missing
- **Human action**: Review gap reports, optionally download/extract additional sources
- **Can skip**: If you're confident the Phase 1a data is sufficient, go straight to Stage 2

**Stage 2 — ANALYZE** (sequential, order matters):
- **Input**: Phase 1a dossier + all extracted sources + approved prior analyses + exemplars + schema + brief
- **Agent**: Headless Claude synthesizes a D1+ analysis from all available data
- **Output**: `analysis.md` with `Status: draft` in YAML frontmatter
- **Key**: Agent reads all approved analyses from the reuse pool. Concepts analyzed later benefit from earlier approved work.

**Stage 3 — REVIEW** (human):
- Not automated. Human reads the draft, edits in-place if needed. No tooling required.

**Stage 4 — APPROVE** (CLI command):
- **Input**: Concept ID
- **Action**: Updates YAML frontmatter in `analysis.md` to `Status: approved`, adds `Approved-Date`
- **Effect**: Analysis becomes visible to subsequent Stage 2 runs

### Typical Usage Flow

```bash
# See what's been done
uv run python exploration/concept_analysis/scripts/run_analysis.py status

# ── STAGE 1: Gap check (batch, parallel) ──────────────────────

# Gap check all remaining concepts
uv run python ... gap-check --all

# Gap check specific concepts by number
uv run python ... gap-check 01 07 17a 21

# Gap check a confinement family
uv run python ... gap-check --family MFE

# Dry run (see the prompt, don't call Claude)
uv run python ... gap-check 01 --dry-run

# ── Human reviews gap reports, downloads sources if needed ────

# ── STAGE 2: Analyze (sequential, one at a time) ─────────────

# Analyze a single concept
uv run python ... analyze 01

# Analyze a batch (runs sequentially, each sees prior approved)
uv run python ... analyze 01 21 28

# ── STAGE 3: Human reviews draft ─────────────────────────────
# (no CLI — just read and edit the file)

# ── STAGE 4: Approve ─────────────────────────────────────────

# Approve after review
uv run python ... approve 01

# Check status again
uv run python ... status
```

### CLI Design

**Single entry point**: `exploration/concept_analysis/scripts/run_analysis.py`

**Subcommands**:

```
run_analysis.py <command> [concepts...] [options]

Commands:
  status                Show per-concept state table
  gap-check [IDs...]    Run Stage 1 gap assessment
  analyze [IDs...]      Run Stage 2 D1+ analysis
  approve [IDs...]      Run Stage 4 approval
  list                  List all 38 concepts with IDs

Concept selection (applies to gap-check, analyze, approve):
  01                    Numeric ID (zero-padded or not)
  17a                   Variant ID
  01 07 17a 21          Multiple concepts (space-separated)
  --all                 All remaining concepts (not yet at target stage)
  --family MFE          All concepts in a confinement family
  --family IFE
  --family MIF
  --family "Non-Standard"

Options:
  --model MODEL         Claude model (sonnet, opus, haiku). Default: sonnet
  --dry-run             Generate prompts without calling Claude
  --timeout SECS        Per-invocation timeout. Default: 900
  --force               Re-run even if stage output already exists
```

**Concept ID resolution** (borrowed from `run_concept.py:find_concept()`):

The script loads `exploration/concept_analysis/table.csv` and resolves concept references:
- `01` → matches ID prefix `01-hts-compact-tokamak`
- `17a` → matches ID prefix `17a-laser-icf-hybrid-drive`
- `hts-compact-tokamak` → matches slug portion
- `CFS` → matches Company column (partial, case-insensitive)

Multiple matches → error with disambiguation list.

### Data Model

**Concept registry**: `table.csv` — read-only, 38 rows. Provides ID, name, company, confinement family. The script loads this on every invocation to resolve concept references and for `--family` filtering.

**Progress tracking**: Filesystem-derived. The script scans `analyses/*/` on each invocation:

| Files present | Frontmatter | State |
|---------------|-------------|-------|
| nothing | — | `not-started` |
| `gap_report.md` | — | `gap-checked` |
| `analysis.md` | `Status: draft` | `drafted` |
| `analysis.md` | `Status: approved` | `approved` |

**Default behavior**: `gap-check` and `analyze` skip concepts that already have the target output. `--force` re-runs regardless.

**Reuse pool**: All `analyses/*/analysis.md` files where frontmatter `Status == approved`. Scanned fresh before each Stage 2 invocation so mid-batch approvals are picked up immediately.

### Output Structure

```
exploration/concept_analysis/
├── table.csv                         # Concept registry — read-only (exists)
├── handwritten/                      # Hand-done exemplars (exists)
│   ├── 01-hts-compact-tokamak.md
│   ├── 07-maglif.md
│   └── 26-laser-icf-indirect-drive.md
├── analyses/                         # Per-concept output directories
│   ├── 01-hts-compact-tokamak/
│   │   ├── gap_check_prompt.md      # Saved prompt (immutable, audit trail)
│   │   ├── gap_report.md            # Stage 1 output
│   │   ├── analysis_prompt.md       # Saved prompt (immutable, audit trail)
│   │   └── analysis.md              # Stage 2 output (draft or approved)
│   └── 21-spherical-tokamak-hts/
│       └── ...
├── prompt_templates/                 # Handlebars-style templates
│   ├── gap_check.md                 # Stage 1 prompt template
│   ├── analysis.md                  # Stage 2 prompt template
│   └── output_template.md          # D1+ section structure (read by agent at runtime)
└── scripts/
    └── run_analysis.py              # Orchestrator
```

All artifacts per concept are flat in `analyses/{id}/`. No nesting — one gap check, one analysis per concept.

**Prompt lifecycle**: For each stage, the script fills the template → saves the prompt → invokes Claude → saves the output. The saved prompt is the immutable audit trail (same pattern as Phase 1a `iter-NN/prompt.md`).

### YAML Frontmatter (analysis.md)

```yaml
---
ID: 01-hts-compact-tokamak
Concept: HTS Compact Tokamak
Company: Commonwealth Fusion Systems
Status: draft                    # draft | approved
Created: 2026-03-20
Approved-Date:                   # set by approve command
Reuses: []                       # agent updates via Edit tool during analysis
---
```

**Frontmatter is script-generated, then agent-editable.** The structural fields (ID, Concept, Company, Status, dates) are deterministic from table.csv + today's date. `Reuses` is initialized as `[]` and the agent updates it via the Edit tool if it references approved prior analyses. The script pre-writes frontmatter to `analysis.md` before Claude runs (see Output Assembly below).

The `approve` command updates `Status` to `approved` and sets `Approved-Date`. The `analyze` command scans all `analyses/*/analysis.md` files for `Status: approved` to build the reuse pool.

### Output Assembly (analysis.md)

The `cmd_analyze` pipeline for each concept:

1. **Script pre-writes `analysis.md`** with frontmatter from table.csv metadata (`make_frontmatter()`), including `Reuses: []`
2. **Script invokes Claude** with `{{output_path}}` (body file) and `{{analysis_path}}` (frontmatter file)
3. **Claude writes sections 1-8 to `{{output_path}}`** using the Write tool — narration goes to stdout (ignored)
4. **Claude edits `Reuses` in `{{analysis_path}}`** via Edit tool if it referenced approved prior analyses
5. **Script reads back frontmatter** from `analysis.md` (which may now have populated `Reuses`)
6. **Script assembles** `analysis.md` = frontmatter + body file contents
7. **Script deletes the temp body file**
8. **Script verifies** `analysis.md` starts with `---`

This cleanly separates concerns:
- **Structured metadata** (frontmatter) — script-generated, agent-editable for `Reuses` only
- **Analytical content** (body) — LLM-generated, written to file (not captured from stdout)
- **Narration** (stdout) — discarded

On failure (Claude error or missing body file), the script cleans up the pre-written `analysis.md` to avoid stale state. If Claude fails to write the body file, the script detects it immediately rather than silently saving narration as the analysis.

### D1+ Output Template

The output structure is defined in a dedicated artifact: `prompt_templates/output_template.md`. This file is:
- **Referenced by the analysis prompt template** (via `{{output_template_path}}`) — the agent reads it at runtime
- **The source of truth** for what sections the analysis should contain
- **Evolvable** — can be refined through testing without changing the orchestrator or prompt template

The output template will be calibrated against the handwritten exemplars during implementation. It must cover:
- The 4 brief D1 sections (data availability, modeling challenges, subsystem maturity, materials/supply chain)
- Structured LCOE parameter extraction for D2 scoping (capital costs, operating costs, energy conversion, capacity factor, scaling assumptions) — with mandatory citation per value
- Data gap inventory (structured, with gap type classification)
- Cross-concept reuse notes (what was adopted from approved priors, what diverges)

The exact format is determined by studying the exemplars and iterating through test runs, not prescribed here.

### Prompt Template Design

**Template 1: `gap_check.md`**

The gap check prompt is lightweight — it reads the dossier and source file listing, then assesses coverage against the D1+ sections.

```
Input context (via {{variables}}):
  {{concept_id}}           — e.g., "01-hts-compact-tokamak"
  {{concept_name}}         — e.g., "HTS Compact Tokamak"
  {{company}}              — e.g., "Commonwealth Fusion Systems"
  {{dossier_path}}         — absolute path to dossier.md
  {{source_file_list}}     — list of all source files with sizes
  {{schema_path}}          — absolute path to schema.md
  {{brief_path}}           — absolute path to concept_analysis_brief.md

Output: structured gap report covering:
  - Per D1 section: what's covered, what's missing
  - Per D2 parameter category: what data exists, what's absent
  - Source recommendations (only from known databases or flagged as unverified)
  - Overall assessment: ready for full analysis? or needs more sources?
```

The agent reads files by path (using `claude -p --dangerously-skip-permissions`), so it can access the actual dossier and source content.

**Template 2: `analysis.md`**

The analysis prompt is heavier — it provides the full context for producing a D1+ write-up.

```
Input context (via {{variables}}):
  {{concept_id}}           — concept ID
  {{concept_name}}         — human-readable name
  {{company}}              — company name
  {{dossier_path}}         — absolute path to Phase 1a dossier
  {{source_paths}}         — list of absolute paths to all source documents
  {{schema_path}}          — path to schema.md
  {{brief_path}}           — path to concept_analysis_brief.md
  {{exemplar_paths}}       — paths to ALL handwritten exemplars
  {{approved_analyses}}    — paths to all approved analysis.md files
  {{output_path}}          — where to write the analysis
  {{output_template_path}} — path to output_template.md (the D1+ section structure)

Key instructions in the template:
  - Read the output template for the required section structure
  - Read all source documents (not just the dossier summary)
  - Every quantitative value must cite a specific source
  - If data doesn't exist, say so — do not fabricate
  - Read approved prior analyses and reuse shared assumptions
  - Document what was reused in the cross-concept notes section
  - Write sections 1-8 to {{output_path}} using the Write tool
  - Edit Reuses field in {{analysis_path}} if prior analyses were referenced
  - Do NOT include YAML frontmatter (script handles that)
  - Do NOT output the analysis to stdout — write it to the file
```

### Cross-Concept Reuse Mechanism

When the `analyze` command runs:

1. **Scan reuse pool**: Find all `analyses/*/analysis.md` with `Status: approved` in frontmatter
2. **Build context**: For each approved analysis, extract the file path
3. **Inject into prompt**: The analysis template includes `{{approved_analyses}}` listing all approved analysis paths. The agent reads them via file access.
4. **Agent instructions**: The template tells the agent:
   - Read all approved analyses
   - Identify shared subsystems, materials, cost structures
   - Reuse consistent assumptions (cite the source concept)
   - Note divergences in Section 7
   - Do NOT copy text verbatim — synthesize and adapt

**Context size management**: As the reuse pool grows (potentially 20+ approved analyses at 200-400 lines each), the prompt itself doesn't contain their text — it lists file paths. The agent reads them selectively via `claude -p --dangerously-skip-permissions`. Claude's context window handles the file reading.

### Holdout Validation

Holdout validation is a human activity, not a script feature. The agent always sees all available exemplars and data — there is no automated holdout hiding mechanism.

To run a holdout test: analyze a concept that has a handwritten version, then compare the agent output to the handwritten version side-by-side. The user manages which concepts to use as holdouts.

### Script Architecture (`run_analysis.py`)

Modeled on `run_concept.py` but organized around subcommands:

```python
# Core modules (all in scripts/):
#
# run_analysis.py          — CLI entry point, subcommand dispatch
#   load_table()           — reads table.csv, returns list of concept dicts
#   resolve_concepts()     — maps CLI args (01, 17a, --all, --family) to concept IDs
#   get_concept_state()    — checks filesystem for gap_report.md, analysis.md, frontmatter
#
# Subcommand handlers:
#   cmd_status()           — print status table
#   cmd_gap_check()        — Stage 1 for one or more concepts
#   cmd_analyze()          — Stage 2 for one or more concepts (sequential)
#   cmd_approve()          — Stage 4 for one or more concepts
#   cmd_list()             — print all concepts
#
# Shared utilities:
#   fill_template()        — Handlebars-style {{variable}} substitution
#   invoke_claude()        — subprocess claude -p via stdin (from run_concept.py)
#   find_sources()         — scan Phase 1a iter-*/sources/ for all source files
#   find_approved()        — scan analyses/ for Status: approved files
#   find_exemplars()       — list all handwritten/*.md files
#   parse_frontmatter()    — extract YAML frontmatter from markdown
#   update_frontmatter()   — update Status/Approved-Date in frontmatter
```

**Key functions**:

`resolve_concepts(args, table)` — maps CLI concept references to full IDs:
```python
def resolve_concepts(args: list[str], flags: Namespace, table: list[dict]) -> list[str]:
    """Resolve concept references to canonical IDs.

    Handles: numeric (01), variant (17a), slug, partial company name,
    --all (remaining), --family (confinement family filter).
    """
```

`get_concept_state(concept_id, analyses_dir)` — determines per-concept status:
```python
def get_concept_state(concept_id: str, analyses_dir: Path) -> str:
    """Check filesystem to determine concept state.

    Returns: 'not-started' | 'gap-checked' | 'drafted' | 'approved'
    """
    analysis_path = analyses_dir / concept_id / "analysis.md"
    gap_path = analyses_dir / concept_id / "gap_report.md"

    if analysis_path.exists():
        fm = parse_frontmatter(analysis_path)
        if fm.get("Status") == "approved":
            return "approved"
        return "drafted"
    if gap_path.exists():
        return "gap-checked"
    return "not-started"
```

`cmd_analyze(concepts, table, opts)` — Stage 2 handler:
```python
def cmd_analyze(concepts: list[str], table: list[dict], opts: Namespace):
    """Run Stage 2 analysis for each concept sequentially.

    For each concept:
    1. Gather Phase 1a dossier path + all source file paths
    2. Gather all approved analysis paths (reuse pool)
    3. Gather all exemplar paths
    4. Fill analysis.md template
    5. Save prompt to analyses/{id}/prompts/analysis_prompt.md
    6. Invoke claude -p
    7. Write output to analyses/{id}/analysis.md with draft frontmatter

    Concepts are processed sequentially so that if concept A is approved
    mid-batch (by the user in another terminal), concept B will see it.
    """
```

---

## Potential Risks

1. **Context window limits**: Source documents can be very large (50+ pages each). If a concept has 3 iterations × 3 sources = 9 documents, plus 10+ approved prior analyses, the total context may exceed limits. **Mitigation**: The agent reads files selectively — the prompt instructs it to scan source documents rather than memorize them all. The `claude -p` headless mode handles context management internally.

2. **Prompt size for analysis template**: The template itself includes the D1+ output structure, exemplar paths, approved analysis paths, and instructions. With 20+ approved analyses, the path listing alone is manageable (~1KB). The content is read by the agent, not included inline.

3. **Sequential bottleneck**: Stage 2 must run sequentially for reuse to work. For 29 concepts at ~5-10 min each, that's 2.5-5 hours. **Mitigation**: The user can approve in parallel (in another terminal), and the next `analyze` invocation will pick up new approvals. The ordering is a guideline, not a hard constraint — user can analyze in any order.

4. **Hallucination in quantitative parameters**: The highest-risk failure mode. **Mitigation**: The prompt template explicitly instructs citation-per-value, "inferred" flagging, and honest gaps. The D1+ template structures this as a table with mandatory Source/Confidence columns.

5. **Source file paths change**: If Phase 1a directories are reorganized, source paths in prompts break. **Mitigation**: Paths are resolved at runtime by scanning the filesystem, not hardcoded.

---

## Integration Strategy

- **Fits alongside Phase 1a**: Uses the same dossier data as input. Does not modify Phase 1a artifacts.
- **Fits alongside Phase 2a**: Independent track. The concept analyses don't reference the reasoning tree, and vice versa.
- **Table.csv is the shared ID registry**: Both the analyses and Phase 1a/1b reference the same concept IDs from `exploration/concept_analysis/table.csv`.
- **No config file**: All state is derived from the filesystem. `table.csv` provides the concept registry. `analyses/*/analysis.md` frontmatter provides per-concept state. `handwritten/` provides exemplars. Analysis ordering is a planning decision managed by the user via CLI arguments.

---

## Validation Approach

1. **Holdout test** (primary): Run `analyze` on 1-2 holdout concepts. Compare agent output to handwritten version on four dimensions (factual accuracy, gap identification, LCOE parameter capture, analytical depth). Must pass ≥3/4 dimensions with no major factual errors.

2. **Dry-run review**: Before running the full pipeline, use `--dry-run` on 2-3 concepts to review the generated prompts. Verify the prompt includes the right sources, exemplars, and approved analyses.

3. **Incremental rollout**: Analyze 2-3 data-rich concepts first (e.g., concept 01, 21). Review and approve. Then analyze the next batch, verifying that cross-concept reuse works correctly.

4. **Status dashboard**: `status` command gives a quick view of progress across all 38 concepts, making it easy to spot concepts stuck in draft or missing gap checks.

---

**Next Step:** After approval → `/_my_plan` for phased implementation
