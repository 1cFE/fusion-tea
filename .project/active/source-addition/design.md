# Design: Source Addition and Incremental Updates

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-29T12:45:55-07:00
**Updated:** 2026-03-29
**Branch:** source-addition

## Overview

Two new `run_analysis.py` subcommands: `add-source` (extract and place a PDF/URL source following companion-dir + symlink conventions) and `update-analysis` (two-step process using a source-integration pre-pass + feedback-pass mode to incrementally update an existing analysis).

## Related Artifacts

- **Spec:** `.project/active/source-addition/spec.md`
- **Epic:** `.project/backlog/epic_concept_analysis_v2.md` (Item 3)
- **Dependency:** `.project/active/iterative-analysis-loop/` (Item 1 — feedback format, modal prompt, staleness)
- **Conventions:** `.project/active/source-replacement/` (companion-dir + symlink layout)
- **Research:** `.project/research/20260328-pipeline-upgrade-feasibility.md` (Q5)
- **Pipeline:** `exploration/concept_analysis/scripts/run_analysis.py`

## Research Findings

### Existing Pipeline Architecture

`run_analysis.py` (`exploration/concept_analysis/scripts/run_analysis.py`) is a ~1750-line argparse-based CLI. Key patterns:

- **Concept resolution**: `resolve_concepts()` (:251) maps CLI args (numeric IDs, slugs, partial names) to concept dicts loaded from `table.csv` via `load_table()` (:189). Each concept has `_id` (e.g., `01-hts-compact-tokamak`) and `_research_id` (maps to Phase 1a directory).
- **Source discovery**: `find_sources(concept_id)` (:612) globs `iter-*/sources/*.md` under `RESEARCH_DIR / concept_id`. Returns sorted list of absolute Paths. Symlinks are followed transparently. Companion directories (no `.md` extension) are invisible.
- **Template engine**: `fill_template()` (:498) supports `{{variable}}` substitution, `{{#if var}}...{{/if}}` conditionals, and `{{@config/file.md}}` file inclusion.
- **Claude invocation**: `invoke_claude()` (:538) runs `claude -p --dangerously-skip-permissions --verbose` via subprocess, passing prompt on stdin. Returns (stdout, stderr, returncode).
- **Staleness propagation**: `propagate_staleness(concept_id, reason)` (:429) marks `model_setup.py`, `review.md`, and `synthesis.md` as stale via frontmatter flags or `# STALE:` comments.
- **CLI convention**: Every subcommand supports `--model`, `--timeout`, `--dry-run`, `--force` where applicable. All handlers take `(concepts, args)` signature. Parser built in `build_parser()` (:1634), dispatch table in `main()` (:1733).

### Modal Analysis Prompt (Item 1)

`analysis_v2.md` has three mutually exclusive modes controlled by template variables:
- **Cold start** (`cold_start="true"`): Writes full analysis from scratch to `{{output_path}}`
- **Feedback pass** (`feedback_pass="true"`): Reads existing `{{analysis_path}}` + `{{feedback_path}}`, makes targeted edits
- **Self-advance** (`self_advance="true"`): Reads existing analysis, self-evaluates, makes improvements

The feedback-pass mode (:101-135) expects `{{feedback_path}}` to point to a file with F-N findings in the standard feedback format. It uses the Edit tool to make targeted improvements. Source paths are still passed via `{{source_paths}}` for subagent evidence gathering.

### Assessment Loop Pattern (Item 1)

`cmd_analyze` (:895-1091) implements the loop:
1. Cold start → `analysis_body.md` → assemble with frontmatter
2. For each assessment pass: invoke assessment prompt → parse `VERDICT:` line → if FINDINGS, invoke analysis in feedback-pass mode
3. Each feedback saved as `feedback_iter_N.md`
4. Staleness propagated after feedback passes

The key integration point for `update-analysis` is that it can reuse the **exact same feedback-pass invocation** (lines 1061-1086) — just with different feedback content and a different feedback filename.

### Source Layout Conventions

Established by source-replacement (`.project/active/source-replacement/plan.md`):

```
iter-NN/sources/
  source-name.md              ← symlink to source-name/output.md
  source-name.orig.md         ← preserved original (replacement only)
  source-name/                ← companion extraction dir
    output.md                 ← extracted markdown with YAML frontmatter
    raw.html (or raw.pdf)     ← original fetched source
    metrics.json              ← extraction metrics
    decisions.json            ← pipeline decisions (PDF only)
    images/                   ← extracted figures (PDF only)
```

Key rules:
- **Always symlink, never copy**: `ln -s source-name/output.md source-name.md` — preserves relative image paths
- **Hyphens in names**: Existing sources use hyphenated-lowercase (e.g., `wham-experiment-details`), NOT underscores
- **PDF flattening required**: PDF extraction creates a nested subdir that must be flattened up one level

### Existing Flattening Logic

`_flatten_extraction_output()` in `scripts/zotero_ingest.py` (:158-180) finds subdirs containing `output.md` and moves their contents up. This logic is specific to zotero_ingest's context (operates on `knowledge/sources/` dirs). We need equivalent logic for Phase 1a sources.

### Slugification

`scripts/zotero_lib.py:slugify()` (:214) uses underscores. Phase 1a source names use hyphens. Need a new `slugify_source()` function using hyphens and matching the existing naming convention.

### Feedback Format

`config/feedback_format.md` defines the F-N structure:
```
VERDICT: FINDINGS

### F-N: [Short title]
- **Target:** [Section or aspect]
- **Finding:** [What's insufficient/missing]
- **Recommendation:** [Specific action]
- **Priority:** blocking | important | minor
```

The source-integration pre-pass must produce output in this exact format so the feedback-pass mode handles it identically to assessment feedback.

## Design Decisions

### DD-1: Source-Integration Pre-Pass Prompt

**Decision**: New prompt template `prompt_templates/source_integration.md`.

**Context**: `update-analysis` needs a pre-pass that reads new sources + existing analysis and generates F-N feedback. This cannot reuse the assessment prompt (different focus — assessment checks shape quality; source-integration identifies new information to incorporate).

**Design**:
- Reads: existing `analysis.md`, new source document(s) via subagent pattern
- Produces: F-N feedback targeting specific analysis sections with specific new information to incorporate
- Focus: "What material information does this source add that the analysis doesn't cover?" — NOT quality assessment
- Uses the standard feedback format so the downstream feedback-pass is identical
- Findings should reference analysis goals where the new information is relevant

### DD-2: Companion-Dir Placement (add-source)

**Decision**: Add to latest existing `iter-NN/sources/`. Create `iter-01/sources/` if none exist.

**Rationale**: New sources added during concept vetting are supplementary material to the existing research, not a new research iteration. Creating a new iteration for each added source would inflate the directory structure unnecessarily.

### DD-3: Flattening Logic Location

**Decision**: Implement flattening as a standalone helper function in `run_analysis.py` rather than importing from `zotero_ingest.py`.

**Rationale**: The `zotero_ingest.py` flatten function uses module-level constants (`EXTRACT_OUTPUT`) and is coupled to the zotero workflow. The logic is ~15 lines; duplicating it with appropriate constants is cleaner than creating a cross-dependency. The constant `output.md` is the filename to look for.

## Proposed Design

### Component 1: `slugify_source(input_path_or_url: str) -> str`

**Location**: `run_analysis.py`, new helper function near `find_sources()`.

Derives a descriptive hyphenated source name:
- **PDF path**: Strip extension, lowercase, replace non-alphanumeric with hyphens, collapse runs, strip edges. E.g., `/tmp/SPARC_ICRF_Heating_Paper.pdf` → `sparc-icrf-heating-paper`.
- **URL**: Extract the path component, strip common prefixes (`/abs/`, `/pdf/`, `/html/`, `/article/`), strip file extensions, slugify the meaningful portion. E.g., `https://arxiv.org/abs/2411.06644` → `arxiv-2411-06644`. For HTML pages: use the last meaningful path segment(s). E.g., `https://realta.com/fusion-hub-spotlight` → `realta-fusion-hub-spotlight`.
- **Truncation**: Max 60 chars, truncate at hyphen boundary.

```python
def slugify_source(input_str: str, max_len: int = 60) -> str:
    """Derive a hyphenated source name from a file path or URL."""
    if input_str.startswith(("http://", "https://")):
        return _slugify_url(input_str, max_len)
    # Local file: use stem
    name = Path(input_str).stem
    return _slugify_text(name, max_len)

def _slugify_text(text: str, max_len: int = 60) -> str:
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if len(slug) <= max_len:
        return slug
    truncated = slug[:max_len]
    last_sep = truncated.rfind("-")
    return truncated[:last_sep] if last_sep > max_len // 2 else truncated

def _slugify_url(url: str, max_len: int = 60) -> str:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    # Use domain + path for descriptive names
    domain = parsed.netloc.replace("www.", "").split(".")[0]  # e.g., "arxiv", "realta"
    path = parsed.path.rstrip("/")
    # Strip common prefixes
    for prefix in ("/abs/", "/pdf/", "/html/", "/article/", "/papers/"):
        if path.startswith(prefix):
            path = path[len(prefix):]
            break
    # Strip file extensions
    path = re.sub(r"\.(pdf|html|htm)$", "", path)
    # Combine domain + meaningful path
    combined = f"{domain}-{path}" if path else domain
    return _slugify_text(combined, max_len)
```

### Component 2: `flatten_companion_dir(companion_dir: Path) -> None`

**Location**: `run_analysis.py`, new helper function.

Replicates the zotero_ingest flattening logic: finds subdirs containing `output.md`, moves their contents up one level, removes the empty nested dir. Identical logic to `_flatten_extraction_output()` in `zotero_ingest.py:158-180` but self-contained.

```python
EXTRACT_OUTPUT = "output.md"

def flatten_companion_dir(companion_dir: Path) -> None:
    """Flatten nested extraction subdirectory if present."""
    subdirs = [d for d in companion_dir.iterdir() if d.is_dir()]
    candidates = [d for d in subdirs if (d / EXTRACT_OUTPUT).exists()]
    if len(candidates) != 1:
        return  # already flat or ambiguous
    nested = candidates[0]
    for item in nested.iterdir():
        dest = companion_dir / item.name
        if item.is_file():
            item.rename(dest)
        elif not dest.exists():
            item.rename(dest)
    if not any(nested.iterdir()):
        nested.rmdir()
```

### Component 3: `find_latest_sources_dir(concept_id: str) -> Path`

**Location**: `run_analysis.py`, new helper function.

Returns the latest `iter-NN/sources/` directory for the concept, or creates `iter-01/sources/` if none exist. Used by `cmd_add_source` to determine where to place new sources.

```python
def find_latest_sources_dir(concept_id: str,
                            research_dir: Path = RESEARCH_DIR) -> Path:
    """Find the latest iter-NN/sources/ dir, or create iter-01/sources/."""
    concept_dir = research_dir / concept_id
    iter_dirs = sorted(concept_dir.glob("iter-*"))
    if iter_dirs:
        sources_dir = iter_dirs[-1] / "sources"
        sources_dir.mkdir(exist_ok=True)
        return sources_dir
    # No iterations exist — create iter-01
    sources_dir = concept_dir / "iter-01" / "sources"
    sources_dir.mkdir(parents=True, exist_ok=True)
    return sources_dir
```

### Component 4: `check_duplicate_source(concept_id: str, name: str) -> Path | None`

**Location**: `run_analysis.py`, new helper function.

Scans all `iter-*/sources/` directories for `<name>.md`. Returns the path if found (duplicate), None if clear.

```python
def check_duplicate_source(concept_id: str, name: str,
                           research_dir: Path = RESEARCH_DIR) -> Path | None:
    """Check if a source with this name already exists in any iteration."""
    concept_dir = research_dir / concept_id
    for iter_dir in concept_dir.glob("iter-*"):
        candidate = iter_dir / "sources" / f"{name}.md"
        if candidate.exists():
            return candidate
    return None
```

### Component 5: `resolve_source_names(concept_id: str, names: list[str]) -> list[Path]`

**Location**: `run_analysis.py`, new helper function.

Resolves short source names to full paths. For `update-analysis --sources sparc-icrf-heating-paper`, scans `iter-*/sources/sparc-icrf-heating-paper.md` and returns the match. Errors if any name is not found.

```python
def resolve_source_names(concept_id: str, names: list[str],
                         research_dir: Path = RESEARCH_DIR) -> list[Path]:
    """Resolve short source names to full paths under the concept."""
    concept_dir = research_dir / concept_id
    resolved = []
    for name in names:
        # Append .md if not present
        fname = name if name.endswith(".md") else f"{name}.md"
        matches = list(concept_dir.glob(f"iter-*/sources/{fname}"))
        if not matches:
            print(f"  error: source '{name}' not found under {concept_dir}/iter-*/sources/")
            sys.exit(1)
        if len(matches) > 1:
            print(f"  error: source '{name}' found in multiple iterations: {matches}")
            sys.exit(1)
        resolved.append(matches[0])
    return resolved
```

### Component 6: `cmd_add_source` Subcommand

**Location**: `run_analysis.py`, new command function + argparse registration.

**Handler signature**: `cmd_add_source(concepts: list[dict], args: argparse.Namespace)` — receives the full table like all other handlers. Internally resolves to a single concept via `resolve_one(concepts, args.concept)` and errors if zero or multiple matches.

**Flow**:

```
1. Resolve concept: resolve_one(concepts, args.concept) → single concept dict
2. Determine source name: args.name (if --name provided) or slugify_source(args.source)
3. Get research_id from concept dict (c["_research_id"])
4. Check for duplicate: check_duplicate_source(research_id, name)
   - If duplicate found and --force: remove existing symlink + companion dir (shutil.rmtree)
   - If duplicate found and no --force: error and exit
5. Find placement: find_latest_sources_dir(research_id) → sources_dir
6. If --dry-run: print what would be created and exit
7. Create companion dir: sources_dir / name / (mkdir)
8. Run extraction:
     uv run agentic-mbse extract <source> --save-source --output <companion_dir>/
9. Flatten if needed: flatten_companion_dir(companion_dir)
10. Verify output.md exists in companion dir
11. Create symlink: sources_dir / f"{name}.md" → f"{name}/output.md"
12. Print confirmation
13. On failure: remove companion dir, report error
```

**Argparse registration**:
```python
p_add = sub.add_parser("add-source", help="Add a PDF or URL source to a concept")
p_add.add_argument("concept", help="Concept ID (single concept)")
p_add.add_argument("source", help="PDF path or URL to extract")
p_add.add_argument("--name", help="Override automatic source name")
p_add.add_argument("--force", action="store_true",
    help="Re-extract even if source name already exists")
p_add.add_argument("--dry-run", action="store_true", help="Show what would be created")
```

Note: `add-source` takes a single `concept` positional (not `concepts` nargs="*") because it always operates on exactly one concept. No `--model`/`--timeout` needed — extraction is handled by `agentic-mbse` with its own defaults.

**`--force` behavior**: If `--force` is passed and a source with the same name already exists, remove the existing symlink and companion dir before re-extracting. Without `--force`, duplicate detection rejects the operation.

**Extraction subprocess**:
```python
cmd = ["uv", "run", "agentic-mbse", "extract", source,
       "--save-source", "--output", str(companion_dir)]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
```

Timeout of 600s (10 minutes) matches agentic-mbse's default PDF extraction timeout.

**Error handling**: If extraction fails (nonzero returncode) or `output.md` doesn't exist after extraction:
- Remove companion dir (`shutil.rmtree`)
- Print stderr snippet
- Exit with error

### Component 7: `cmd_update_analysis` Subcommand

**Location**: `run_analysis.py`, new command function + argparse registration.

**Handler signature**: `cmd_update_analysis(concepts: list[dict], args: argparse.Namespace)` — same pattern as `cmd_add_source`. Resolves to single concept via `resolve_one()`.

**Flow**:

```
1. Resolve concept: resolve_one(concepts, args.concept) → single concept dict
2. Resolve source names → full paths via resolve_source_names(c["_research_id"], args.sources)
3. Verify analysis.md exists for concept
4. Load source_integration.md template
5. Step 1 — Source-Integration Pre-Pass:
   a. Fill template with: analysis_path, new_source_paths, concept_name, feedback_path
   b. Save prompt as source_integration_prompt_<timestamp>.md (audit trail)
   c. Invoke Claude (fresh thread) with the filled template
   d. Verify feedback file was created
   e. If --dry-run: print feedback content and exit
6. Step 2 — Feedback Pass:
   a. Fill analysis_v2.md template in feedback-pass mode:
      - feedback_pass="true", feedback_path=<from step 1>
      - All other common_vars (source_paths=ALL sources, dossier, etc.)
   b. Save prompt as update_analysis_prompt_<timestamp>.md (audit trail)
   c. Invoke Claude (fresh thread) with the filled template
   d. Claude edits analysis.md via Edit tool
7. Propagate staleness on downstream artifacts
8. Print summary
```

**Argparse registration**:
```python
p_upd = sub.add_parser("update-analysis",
    help="Update analysis to incorporate new sources")
p_upd.add_argument("concept", help="Concept ID (single concept)")
p_upd.add_argument("--sources", nargs="+", required=True,
    help="Source names to incorporate (e.g., sparc-icrf-heating-paper)")
p_upd.add_argument("--model", default="sonnet", help="Claude model (default: sonnet)")
p_upd.add_argument("--timeout", type=int, default=900, help="Per-invocation timeout")
p_upd.add_argument("--dry-run", action="store_true",
    help="Run pre-pass and show feedback, but don't invoke analysis agent")
```

**Timestamp format**: ISO 8601 compact, e.g., `feedback_update_20260329T124500.md`. Avoids collisions while being human-readable and sortable.

**Naming convention note**: The assessment loop uses iteration-numbered files (`feedback_iter_1.md`, `analysis_prompt_iter_2.md`). Source updates use timestamp-based names instead because they're ad-hoc events outside the numbered iteration sequence. Both live in the same `analyses/<concept>/` directory.

**Re-using feedback-pass infrastructure**: Step 2 builds `common_vars` the same way `cmd_analyze` does (lines 938-951), then fills `analysis_v2.md` with `feedback_pass="true"`. The only difference from the assessment loop is:
- Feedback file is `feedback_update_<ts>.md` instead of `feedback_iter_N.md`
- The prompt file is `update_analysis_prompt_<ts>.md` instead of `analysis_prompt_iter_N.md`

### Component 8: `source_integration.md` Prompt Template

**Location**: `exploration/concept_analysis/prompt_templates/source_integration.md`

**Purpose**: Read new source(s) + existing analysis → produce F-N feedback identifying what material information should be incorporated and where.

**Structure**:

```markdown
# Source Integration Assessment: {{concept_name}}

You are evaluating new source documents that have been added to a concept
that already has a completed analysis. Your job is to identify what material
information from the new sources should be incorporated into the existing
analysis, and produce structured feedback for the analysis agent.

## Existing Analysis
Read this file completely:
`{{analysis_path}}`

## New Source Documents (use subagents)

Spawn one subagent per new source document. Ask each subagent:
- What new technical, economic, or performance data does this source contain?
- Does it contain information that contradicts or updates claims in the analysis?
- What LCOE-relevant parameters or cost data are present?
- What risk, timeline, or TRL information is relevant?

New sources:
{{new_source_paths}}

## Analysis Goals (for reference)

{{@config/analysis_goals.md}}

## Instructions

1. Read the existing analysis completely
2. Spawn subagents to read each new source
3. Compare the new information against what the analysis already covers
4. Identify material gaps — information that would change the analysis's
   conclusions, parameter values, risk assessment, or modeling recommendations
5. Do NOT flag information the analysis already covers adequately
6. Do NOT flag minor/cosmetic additions — focus on material impact

## Output

Write structured feedback to this file using the Write tool:
`{{feedback_path}}`

Use this exact format:

{{@config/feedback_format.md}}

**Adaptation for source integration**: The "Finding" field should describe
what new information the source provides. The "Recommendation" field should
specify exactly where and how to incorporate it into the analysis (which
section, what to add/update). The "Target" field should reference the analysis
section that needs updating.

If the new sources contain no material information beyond what the analysis
already covers, return `VERDICT: PASS`.
```

**Key design choices**:
- Uses the subagent pattern (consistent with `analysis_v2.md`) for reading new sources
- References the existing analysis goals so findings are framed in terms of the analysis's objectives
- Includes the standard feedback format via `{{@config/feedback_format.md}}`
- Explicit instruction to only flag **material** additions — avoids churning on minor details

### CLI Dispatch Integration

Both new commands are registered in `build_parser()` and added to the dispatch table:

```python
dispatch = {
    "list": cmd_list,
    "status": cmd_status,
    "gap-check": cmd_gap_check,
    "analyze": cmd_analyze,
    "model-setup": cmd_model_setup,
    "review": cmd_review,
    "address-review": cmd_address_review,
    "synthesize": cmd_synthesize,
    "approve": cmd_approve,
    "stage1-all": cmd_stage1_all,
    "add-source": cmd_add_source,         # NEW
    "update-analysis": cmd_update_analysis,  # NEW
}
```

Note: These commands take a single `concept` positional rather than `concepts` nargs="*", which means they won't use `resolve_concepts()` directly. Instead, they'll use `resolve_one()` (:216) and verify exactly one match.

### Data Flow Diagram

```
add-source:
  PDF/URL → agentic-mbse extract → companion_dir/output.md
                                  → companion_dir/raw.{pdf,html}
                                  → companion_dir/metrics.json
         → flatten if nested
         → symlink: name.md → name/output.md
         → find_sources() picks up automatically

update-analysis:
  source names → resolve to paths
               → source_integration.md prompt
               → Claude pre-pass (reads new sources + analysis)
               → feedback_update_<ts>.md (F-N format)
               → analysis_v2.md feedback-pass mode
               → Claude edits analysis.md
               → propagate_staleness()
```

## Potential Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| URL slugification produces poor names | Low | `--name` override flag; user sees the name in confirmation output and can re-run |
| PDF extraction timeout (large papers) | Medium | 600s timeout matches agentic-mbse default; user can re-run |
| Pre-pass generates no findings when source has material info | Medium | Prompt explicitly instructs to flag material additions; assessment quality will improve with use |
| Pre-pass generates too many findings (>3 limit) | Low | Feedback format specifies max 3; prompt inherits this from `feedback_format.md` |
| Symlink breaks if companion dir is moved | Low | Symlinks are relative (`name/output.md`), not absolute — move the entire sources dir and they survive |
| Flattening fails on unusual extraction output | Low | Flattening is a no-op if no nested subdir with `output.md` found; companion dir is still usable |

## Integration Strategy

- **No changes to existing code**: `find_sources()`, `propagate_staleness()`, `fill_template()`, `invoke_claude()`, and the feedback-pass mode of `analysis_v2.md` are all reused as-is.
- **One new prompt template**: `source_integration.md` — the pre-pass prompt. Everything else is existing infrastructure.
- **Pipeline state**: `add-source` doesn't change pipeline state (concept stays at whatever stage it's at). `update-analysis` modifies `analysis.md` and triggers staleness, which `status` already reports via the `*` suffix.

## Validation Approach

**Manual testing** (these are headless Claude pipelines, not unit-testable):

1. **add-source PDF**: Run on a concept with existing iterations. Verify companion dir layout, symlink, `find_sources()` discovery.
2. **add-source URL**: Run with an HTML URL. Verify same layout with `raw.html`.
3. **add-source duplicate**: Try to add a source with a name that already exists. Verify rejection.
4. **add-source no iterations**: Run on a concept with no `iter-*` dirs. Verify `iter-01/sources/` creation.
5. **add-source --dry-run**: Verify output shows intended placement without creating files.
6. **update-analysis**: Add a source, then update analysis. Verify pre-pass generates F-N feedback, feedback-pass modifies `analysis.md`, staleness propagates.
7. **update-analysis --dry-run**: Verify pre-pass runs and feedback is shown but analysis agent is not invoked.

---

**Next Step:** After approval → `/_my_plan` for implementation phasing
