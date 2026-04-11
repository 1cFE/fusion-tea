# Design: Re-source NO-Verdict .orig.md Files

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05
**Last Updated:** 2026-04-05
**Branch:** design-space-explore
**Commit:** ae8544b

## Overview

Standalone script that processes 21 `.orig.md` files — multi-source Haiku compilations with broken provenance — by extracting their listed URLs and searching for additional sources, producing properly-traced individual source files via `add-source`.

## Related Artifacts

- **Spec:** `.project/active/orig-md-research/spec.md`
- **Provenance investigation:** `.project/concepts/source-acquisition-investigation.md`
- **Triage report:** `.project/active/source-replacement/triage-report.md`
- **Research module (pattern source):** `exploration/concept_analysis/scripts/lib/research.py`
- **Research prompt (methodology source):** `exploration/concept_analysis/prompt_templates/research.md`

## Research Findings

### .orig.md Header Format Patterns

All 21 files follow one of four header patterns for listing source URLs:

| Pattern | Example | Count |
|---------|---------|-------|
| `**Sources**: url1, url2` | `hb11-company-overview.orig.md` | 8 |
| `**Source**: url1, url2` | `xcimer-energy-website-and-science.orig.md` | 5 |
| `Source: url (text)` (no bold) | `general-fusion-technology-overview.orig.md` | 3 |
| Bullet list under `## Source` | `type-one-energy-infinity-two-design.orig.md` | 3 |
| No explicit URLs | `general-fusion-lm26-milestones-2025.orig.md`, `tokamak-energy-roadmap.orig.md` | 2 |

**Key insight:** The agent prompt should handle all patterns — it reads the whole file and extracts URLs from any format. A rigid parser is unnecessary.

### Existing Infrastructure (Direct Reuse)

| Component | Location | How it's called |
|-----------|----------|-----------------|
| `invoke_claude()` | `scripts/lib/claude.py:7` | `invoke_claude(prompt, cwd, timeout, model)` → `(stdout, stderr, rc)` |
| `find_sources()` | `scripts/lib/sources.py:10` | `find_sources(concept_id)` → `list[Path]`. Globs `iter-*/sources/*.md`. **Note: matches `.orig.md` too** since glob `*.md` matches it. |
| `cmd_add_source` / CLI | `scripts/run_analysis.py:864` | `uv run python scripts/run_analysis.py add-source <concept_num> <url>`. Handles extraction, companion dir, symlink, duplicate check. |
| `fill_template()` | `scripts/lib/templating.py:11` | `fill_template(text, {"var": "val"})`. Supports `{{var}}`, `{{#if var}}...{{/if}}`, `{{@path}}`. |
| `find_latest_sources_dir()` | `scripts/lib/sources.py:91` | `find_latest_sources_dir(concept_id)` → latest `iter-NN/sources/` dir. |
| `RESEARCH_DIR` | `scripts/lib/paths.py:19` | `REPO_ROOT / "knowledge" / "concept_research"` |
| `CONCEPT_ANALYSIS_DIR` | `scripts/lib/paths.py:10` | CWD for `invoke_claude()` |

### find_sources() .orig.md Interaction

`find_sources()` (`sources.py:10`) globs `*.md` which **does match `.orig.md`**. This means:
- The before/after filesystem diff used to detect acquired sources will include `.orig.md` in the "before" set
- Newly acquired sources will be detected correctly (they're `.md` files, not `.orig.md`)
- No issue — the diff produces `post - pre`, so `.orig.md` files cancel out

### Concept Resolution from File Path

The `.orig.md` path contains the concept ID: `knowledge/concept_research/<concept_id>/iter-NN/sources/<name>.orig.md`. The concept ID (e.g., `15-sheared-flow-stabilized-z-pinch`) can be parsed from the path. The concept's numeric prefix (e.g., `15`) is what `add-source` needs.

The concept table (`table.csv`) maps numeric prefix → full concept metadata. But for this script, we only need the numeric prefix for the `add-source` CLI call, which can be extracted from the path without loading the CSV.

### research.md Prompt — What to Reuse Verbatim

The following sections from `prompt_templates/research.md` apply unchanged:
- **Source Quality Hierarchy** (lines 76-86) — priority ordering for source types
- **News-Site Heuristic** (lines 88-99) — when company sites fail, search news coverage
- **Rules** (lines 100-110) — WebFetch for triage only, add-source only, one URL per call
- **Output JSON format** (lines 112-175) — same schema works, adapted field names

### What Doesn't Transfer

- **Section 6 gap table parsing** — the research.md prompt reads structured gap IDs and types. The .orig.md prompt reads free-text content with embedded URLs.
- **Prior-attempts memory** — research.md accumulates cross-iteration log. This script is single-pass per file; no need for cross-invocation memory.
- **Budget/gap prioritization** — research.md prioritizes blocking > important > nice-to-have gaps. This script prioritizes header URLs first, then web search for uncovered claims.

## Proposed Design

### Architecture

```
resurface_orig.py          — CLI entry point + batch orchestrator
prompt_templates/
  resurface.md             — agent prompt template
```

Two files. The orchestrator discovers `.orig.md` files, invokes a `claude -p` agent per file, detects acquired sources, and writes reports. The prompt template tells the agent how to read the `.orig.md`, try header URLs, search for remaining claims, and extract via `add-source`.

No new library modules — the script imports from `lib/` directly.

### New Research Iteration Strategy

Each affected concept gets a **new `iter-NN+1/sources/` directory** for re-sourced files. This treats the work as new research rather than patching existing iterations.

**Why a new iter:** The `.orig.md` files are goals — we use their claims as search targets, but we don't know what we'll actually find. The extracted sources may cover different ground than the originals. Mixing them into existing iters would conflate Phase 1a research with this re-sourcing pass.

**Mechanics:** The orchestrator groups `.orig.md` files by concept, creates the new iter directory **once per concept** before processing any of that concept's files. Since `add-source` calls `find_latest_sources_dir()`, and the new iter is now the latest, all extractions for that concept naturally land there.

```
# Before:
22-projectile-icf/
  iter-01/sources/   ← original research
  iter-02/sources/   ← Phase 1a iteration 2

# After:
22-projectile-icf/
  iter-01/sources/   ← original research
  iter-02/sources/   ← Phase 1a iteration 2
  iter-03/sources/   ← re-sourced from .orig.md files (this script)
```

**Concepts with multiple `.orig.md` files** (04 has 3, 23 has 3, 14 has 2, 21 has 2): all `.orig.md` files for a concept share the same new iter. The agent is invoked once per `.orig.md` file, but all extractions land in the same directory.

**Current state:**
| Concepts | Current latest | New iter |
|----------|---------------|----------|
| 12 concepts | iter-02 | iter-03 |
| 21, 29 | iter-03 | iter-04 |
| 24, 31 | iter-01 | iter-02 |

### Component 1: Orchestrator (`scripts/resurface_orig.py`)

**Location:** `exploration/concept_analysis/scripts/resurface_orig.py`

**Responsibilities:**
1. Discover `.orig.md` files (glob or explicit paths)
2. Parse concept ID and numeric prefix from each file path
3. Group by concept; create new iter directory once per concept
4. For each file: build prompt, invoke agent, detect acquired sources, write report
5. Produce summary report at the end

**CLI interface:**

```
uv run python scripts/resurface_orig.py --all [--dry-run] [--max-extractions N] [--model MODEL] [--timeout SECS]
uv run python scripts/resurface_orig.py FILE [FILE ...] [--dry-run] [--max-extractions N]
```

- `--all`: glob `RESEARCH_DIR/**/iter-*/sources/*.orig.md`
- `FILE ...`: explicit `.orig.md` paths
- `--dry-run`: save prompts, don't invoke Claude
- `--max-extractions N`: cap per file (default 5)
- `--model MODEL`: Claude model (default: sonnet — these are short, focused tasks)
- `--timeout SECS`: per-file timeout (default 600)

**Batch grouping:**

```python
def ensure_new_iter(concept_id: str) -> Path:
    """Create a new iter-NN+1/sources/ dir for this concept. Idempotent.

    Returns the new sources dir path. If already created (concept has
    multiple .orig.md files), returns the existing one.
    """
    concept_dir = RESEARCH_DIR / concept_id
    existing = sorted(concept_dir.glob("iter-*"))
    if existing:
        latest_num = int(existing[-1].name.split("-")[1])
        new_num = latest_num + 1
    else:
        new_num = 1
    new_dir = concept_dir / f"iter-{new_num:02d}" / "sources"
    new_dir.mkdir(parents=True, exist_ok=True)
    return new_dir


def main():
    # ... arg parsing ...

    # Group .orig.md files by concept
    by_concept: dict[str, list[Path]] = {}
    for p in orig_paths:
        cid, _ = parse_concept_from_path(p)
        by_concept.setdefault(cid, []).append(p)

    results = []
    for concept_id, files in by_concept.items():
        # Create new iter ONCE per concept
        new_sources_dir = ensure_new_iter(concept_id)
        print(f"\n{concept_id}: new iter at {new_sources_dir.parent.name}/")

        for orig_path in files:
            result = process_one(orig_path, new_sources_dir, args)
            results.append(result)
    # ... summary ...
```

**Core function:**

```python
def process_one(orig_path: Path, new_sources_dir: Path,
                args: argparse.Namespace) -> dict:
    """Process a single .orig.md file. Returns result dict."""
    # 1. Parse concept info from path
    concept_id, concept_num = parse_concept_from_path(orig_path)

    # 2. Read .orig.md content
    content = orig_path.read_text(encoding="utf-8")

    # 3. Snapshot current sources (new iter dir already exists, so
    #    find_sources() will include it — but it's empty, so no effect)
    pre_sources = set(str(s) for s in find_sources(concept_id))

    # 4. Build prompt from template
    prompt = fill_template(template_text, {
        "orig_filename": orig_path.name,
        "orig_content": content,
        "concept_num": concept_num,
        "concept_id": concept_id,
        "max_extractions": str(args.max_extractions),
        "output_path": str(output_path),
    })

    # 5. Save prompt (audit trail)
    prompt_path = report_dir / f"{orig_path.stem}.prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    if args.dry_run:
        return {"status": "dry-run", "prompt_saved": str(prompt_path)}

    # 6. Invoke agent — add-source will use find_latest_sources_dir(),
    #    which now returns new_sources_dir (it's the latest iter)
    stdout, stderr, rc = invoke_claude(
        prompt, cwd=CONCEPT_ANALYSIS_DIR,
        timeout=args.timeout, model=args.model,
    )

    # 7. Detect acquired sources via filesystem diff
    post_sources = find_sources(concept_id)
    acquired = [s for s in post_sources if str(s) not in pre_sources]

    # 8. Parse agent output JSON
    agent_report = parse_agent_output(output_path)

    # 9. Build result
    return {
        "orig_path": str(orig_path),
        "concept_id": concept_id,
        "acquired": [str(p) for p in acquired],
        "agent_report": agent_report,
        "recommendation": agent_report.get("recommendation", "unknown"),
    }
```

**Path parsing:**

```python
def parse_concept_from_path(orig_path: Path) -> tuple[str, str]:
    """Extract concept_id and concept_num from .orig.md path.

    Path pattern: .../knowledge/concept_research/<concept_id>/iter-NN/sources/<name>.orig.md
    """
    # Walk up: sources/ → iter-NN/ → concept_id/
    concept_dir = orig_path.parent.parent.parent
    concept_id = concept_dir.name  # e.g., "15-sheared-flow-stabilized-z-pinch"
    concept_num = re.match(r"^(\d+[a-z]?)-", concept_id).group(1)  # e.g., "15"
    return concept_id, concept_num
```

**Report output:**

Per-file JSON written to `exploration/concept_analysis/resurface_reports/<name>.json`. Summary table printed to stdout.

The report directory is ephemeral (gitignored or in the script's output area) — the durable artifacts are the source files created by `add-source`.

### Component 2: Agent Prompt Template (`prompt_templates/resurface.md`)

**Location:** `exploration/concept_analysis/prompt_templates/resurface.md`

**Strategy:** The agent gets the full `.orig.md` content and follows a three-phase approach:

1. **Extract URLs from the file** — scan the header and body for any URLs. These are the original sources the research agent visited. Try each one first.
2. **Try header URLs via `add-source`** — for each URL found, attempt extraction. Many will succeed (standard HTML news sites). Some will fail (JS-heavy company sites, 404s). Log outcomes.
3. **Search for uncovered claims** — for claims/data in the `.orig.md` that aren't covered by successfully-extracted header URLs, use WebSearch to find alternative sources. Apply the news-site heuristic: if company site fails, search for news coverage.

**Template variables:**

| Variable | Source | Example |
|----------|--------|---------|
| `{{orig_filename}}` | `orig_path.name` | `first-light-fusion-technology.orig.md` |
| `{{orig_content}}` | File content | Full markdown text |
| `{{concept_num}}` | Path parse | `22` |
| `{{concept_id}}` | Path parse | `22-projectile-icf` |
| `{{max_extractions}}` | CLI flag | `5` |
| `{{output_path}}` | Computed | `/tmp/resurface/22-first-light-fusion-technology.json` |

**Prompt structure:**

```markdown
# Source Acquisition: Re-source {{orig_filename}}

You are a research agent. Below is a legacy source file (Haiku paraphrase compiled
from multiple URLs). Your job: find the actual URLs where this data comes from,
and extract each one as a proper source file using `add-source`.

## The Legacy File

```
{{orig_content}}
```

## Instructions

### Phase 1: Extract URLs from the file

Scan the file above for URLs. They appear in headers like:
- `**Sources**: url1, url2, ...`
- `**Source**: url`
- `Source: url (text)`
- Bullet lists under `## Source` or `## Sources`
- Inline URLs in the text body

List every URL you find.

### Phase 2: Try header URLs first

For each URL found in Phase 1, attempt extraction:

```
uv run python scripts/run_analysis.py add-source {{concept_num}} "<url>"
```

Run from the working directory. Log the outcome for each URL:
- **Success**: source extracted, note the source name
- **Fail (JS/empty)**: URL returned thin or no content — note this, search for
  news coverage in Phase 3
- **Fail (404/timeout)**: URL is dead — note this
- **Fail (paywall/403)**: URL requires access — log for human action
- **Duplicate**: source name already exists — skip (already extracted)

### Phase 3: Search for uncovered claims

After Phase 2, review the original file content. Are there significant claims,
technical parameters, or data points NOT covered by any successfully-extracted source?

For each uncovered claim cluster:
1. Use WebSearch to find alternative URLs (news articles, press releases,
   institutional pages) that contain the same data
2. Use WebFetch to triage candidates (accessibility, relevance)
3. Extract confirmed sources via `add-source`

[Source Quality Hierarchy — copied verbatim from research.md lines 76-86]

[News-Site Heuristic — copied verbatim from research.md lines 88-99]

### Phase 4: Coverage Assessment

After all extraction attempts, assess coverage:
- Which claims from the original file are now backed by at least one extracted source?
- Which claims remain uncovered?
- Recommendation: `delete` (>80% covered), `partial` (50-80%), `keep` (<50%)

Also note whether the thin replacement `.md` file (same path without `.orig`)
adds any unique content not in the newly-extracted sources.

## Rules

1. NEVER use WebFetch output as source content. WebFetch is for triage only.
2. NEVER write source files manually. Every source MUST come from `add-source`.
3. One URL per `add-source` call.
4. At most {{max_extractions}} extractions per invocation.
5. Log everything in the output file.

## Output

Write a JSON file to: `{{output_path}}`

[Schema — adapted from research.md with claim-oriented fields instead of gap-oriented]
```

**Output JSON schema:**

```json
{
  "orig_file": "first-light-fusion-technology.orig.md",
  "urls_found": ["https://firstlightfusion.com/...", "https://newatlas.com/..."],
  "extractions": [
    {
      "url": "https://newatlas.com/energy/first-light-fusion-flare/",
      "source_name": "newatlas-energy-first-light-fusion-flare",
      "outcome": "success",
      "covers": ["FLARE pivot details", "funding history"]
    },
    {
      "url": "https://firstlightfusion.com/",
      "outcome": "fail_js",
      "notes": "JS-heavy, only navigation text extracted"
    }
  ],
  "uncovered_claims": [
    "Machine 4 specs (60 km/s, 100 MJ) — no accessible source found"
  ],
  "recommendation": "delete",
  "replacement_md_note": "Thin replacement (31 lines) is a subset of newatlas extraction"
}
```

### Batch Flow

```
main()
├── Discover .orig.md files (glob or args)
├── Load prompt template (once)
├── Group files by concept
├── For each concept:
│   ├── ensure_new_iter() — create iter-NN+1/sources/ once
│   └── For each .orig.md in this concept:
│       ├── parse_concept_from_path()
│       ├── Read content
│       ├── fill_template()
│       ├── Save prompt (audit trail)
│       ├── invoke_claude() [or skip if --dry-run]
│       ├── Filesystem-diff find_sources() to detect acquired
│       ├── Parse agent output JSON
│       └── Write per-file report JSON
├── Print summary table
└── Write summary JSON (all results)
```

### Report Directory

```
exploration/concept_analysis/resurface_reports/
├── 04-hb11-company-overview.json         # per-file agent output
├── 04-hb11-company-overview.prompt.md    # saved prompt (audit)
├── 22-first-light-fusion-technology.json
├── 22-first-light-fusion-technology.prompt.md
├── ...
└── summary.json                          # all results + recommendations
```

This directory should be gitignored (ephemeral output). The durable artifacts are the source files in `knowledge/concept_research/`.

### Resumability

If the script is interrupted, re-running `--all` should:
1. Re-discover all `.orig.md` files
2. Skip files that already have a report JSON with `"status": "complete"` in `resurface_reports/`
3. Process remaining files

This is achieved by checking for an existing report before invoking the agent. The `--force` flag can override this to reprocess everything.

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Header URLs are all JS-heavy company sites → all fail | High for ~15 of 21 | Medium | Phase 3 (web search for news coverage) is the main value-add. The news-site heuristic specifically addresses this. |
| Agent extracts too many sources per file | Low | Low | `--max-extractions` cap. Default 5 is generous for 15-90 line files. |
| Agent output JSON is malformed | Medium | Low | Parse gracefully — still detect acquired sources via filesystem diff (source of truth pattern from research.py). |
| `add-source` fails silently | Low | Medium | The orchestrator diffs `find_sources()` before and after — it doesn't trust the agent's self-reporting. |
| Cost accumulation across 21 files | Low | Medium | Sonnet is cheap (~$0.10-0.30/invocation). `add-source` extractions cost $0-2 each depending on PDF vs HTML. Total expected: $5-15 for all 21 files. |

## Integration Strategy

This script is **standalone and ephemeral**. It:
- Lives alongside `run_analysis.py` in `scripts/` but is not part of the analysis pipeline
- Imports from `lib/` (paths, claude, sources, templating) but adds no new library code
- Produces source files via the same `add-source` pathway used by the analysis loop's research step
- Will be run once (or a few times with resume), then its job is done

After completion:
1. User reviews `summary.json` recommendations
2. `.orig.md` files marked `delete` are removed
3. `.orig.md` files marked `partial` are inspected — uncovered claims noted for manual action
4. Thin replacement `.md` files superseded by richer individual sources are removed
5. `plan-completion.md` Phase 6 Step 3 is updated with results

## Validation Approach

### Test run (1-2 files)

Pick two files with different characteristics:
- **`first-light-fusion-technology.orig.md`** (92 lines, 6 header URLs including newatlas.com and neimagazine.com) — tests the header-URL-first strategy with extractable news sites
- **`general-fusion-lm26-milestones-2025.orig.md`** (30 lines, no explicit URLs) — tests the web-search fallback when no header URLs exist

Verify:
- Prompt is well-formed (`--dry-run`)
- Agent finds and extracts at least one source per file
- Per-file report JSON is valid and contains coverage assessment
- Source files have YAML frontmatter, companion dir, symlink

### Full run

Process all 21 files. Review `summary.json`:
- How many recommend `delete` vs `partial` vs `keep`?
- Total sources acquired?
- Total cost?
- Any unexpected failures?

---

**Next Step:** After approval → `/_my_plan` or `/_my_implement` (small enough to implement directly)
