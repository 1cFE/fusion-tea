# Design: Autonomous Source Acquisition (Research Step)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-05
**Updated:** 2026-04-05
**Branch:** design-space-explore
**Commit:** cfbff65

---

## Overview

Implement the research step that fills the `_run_research_step` stub in `lib/loop.py:570-581`. A research agent (via `claude -p`) reads data gaps from the analysis, searches the web, extracts sources via `add-source`, then chains to the existing source-integration prompt for rich feedback.

## Related Artifacts

- **Spec:** `.project/active/autonomous-source-acquisition/spec_v2.md`
- **Concept:** `.project/concepts/autonomous-source-acquisition.md`
- **Loop refactor spec:** `.project/active/refactor-stage1-loop/spec.md`
- **Extension point stub:** `exploration/concept_analysis/scripts/lib/loop.py:570-581`
- **Source integration:** `exploration/concept_analysis/scripts/lib/loop.py:512-567`

---

## Research Findings

### Existing Code to Reuse

**`_run_source_integration()` (loop.py:512-567)**
Takes `(concept, iter_dir, new_sources: list[Path], analysis_path, args)`. Invokes `source_integration.md` template via `claude -p`, which spawns subagents to read each new source and produces structured findings in `feedback_format.md` schema. Returns `Path` to output file or `None` if verdict is PASS.

**`invoke_claude()` (claude.py:7-35)**
Runs `claude -p --dangerously-skip-permissions --verbose [--model M]` with prompt via stdin. Working directory set via `cwd` parameter. Returns `(stdout, stderr, rc)`. No mechanism to restrict tools — the agent gets whatever tools `claude -p` provides, which includes WebSearch, WebFetch, and Bash (confirmed in `.claude/settings.local.json`).

**`cmd_add_source()` (run_analysis.py:834-932)**
Self-contained: resolves concept from ID/prefix, slugifies URL, checks duplicates, runs `uv run agentic-mbse extract <source> --save-source --output <dir>`, flattens output, creates symlink. Places sources in `knowledge/concept_research/{rid}/iter-NN/sources/`. The research agent can invoke this via Bash as:
```
uv run python scripts/run_analysis.py add-source <concept_num> <url>
```
from `cwd=CONCEPT_ANALYSIS_DIR`.

**`find_sources()` (sources.py:10-25)**
Scans `knowledge/concept_research/{rid}/iter-*/sources/*.md`. Returns sorted list of absolute paths. Called per-iteration in the loop (loop.py:101) and after research (loop.py:130-131). Fast filesystem scan.

**`fill_template()` (templating.py)**
Supports `{{variable}}` substitution and `{{@path}}` file inclusion (relative to `TEMPLATES_DIR`). `{{#if var}}...{{/if}}` conditionals.

**Argparse locations:**
- `p_analyze` at run_analysis.py:965, `--research` at line 979
- `p_s1` (stage1-all) at run_analysis.py:1027, `--research` at line 1044

### Key Constraint: Circular Import Avoidance

`loop.py` imports from most `lib/` modules. If `research.py` imports `_run_source_integration` from `loop.py`, that creates a circular dependency (`loop.py` → `research.py` → `loop.py`). The design avoids this by having `run_research_step()` return the list of acquired sources, and letting `loop.py` handle the source-integration chaining. This also matches the existing pattern: loop.py already knows how to call `_run_source_integration()`.

---

## Proposed Design

### Component Overview

```
                    loop.py (existing, modified)
                    ├── feedback-producer branch (lines 122-132)
                    │   calls run_research_step() from research.py
                    │   then chains to _run_source_integration() if sources acquired
                    │
lib/research.py     │   prompt_templates/research.md
(new, ~200 lines)   │   (new)
├── run_research_step()    ← main entry point
│   ├── load_research_log()
│   ├── build prompt from template
│   ├── invoke_claude()
│   ├── parse research_output.json
│   └── update_research_log()
│       returns list[Path] of acquired sources
```

### 1. Loop Integration (loop.py — branch rewrite + stub deletion)

**Two changes are required in loop.py.** This is a branch rewrite, not just filling a stub.

**Change A: Replace the entire `elif` branch at lines 122-132.** The existing code:

```python
# EXISTING (loop.py:122-132) — TO BE REPLACED IN FULL
elif getattr(args, "research", False) and iter_num > 1:
    # Research extension point (FR-13, FR-14)
    feedback_source = "research"
    feedback_path = _run_research_step(concept, iter_dir, args)
    if feedback_path is None:
        # Research not yet implemented — fall through to normal
        feedback_source = "assess"
        feedback_path = _get_prior_feedback(concept_dir, iter_num)
    # FR-15: re-find sources after research
    current_sources = find_sources(rid)
    common_vars["source_paths"] = format_source_list(current_sources)
```

is replaced by:

```python
# NEW (replaces lines 122-132)
elif getattr(args, "research", False) and iter_num > 1:
    feedback_source = "research"
    from lib.research import run_research_step
    acquired = run_research_step(concept, iter_dir, args)

    # Refresh sources after research (FR-15) — must happen before
    # source-integration so it can see the new files
    current_sources = find_sources(rid)
    common_vars["source_paths"] = format_source_list(current_sources)

    if acquired:
        # Chain to source-integration for rich feedback (FR-10)
        feedback_path = _run_source_integration(
            concept, iter_dir, acquired, analysis_path, args)
        if feedback_path is None:
            # Source integration found no material additions
            feedback_source = "assess"
            feedback_path = _get_prior_feedback(concept_dir, iter_num)
    else:
        # Nothing acquired — fall through to assess
        feedback_source = "assess"
        feedback_path = _get_prior_feedback(concept_dir, iter_num)
```

Key difference from the existing branch: the source refresh moves *before* the source-integration call (was at the end of the block). Source-integration needs `find_sources()` to have already picked up the new files. The local import avoids circular dependencies (`loop.py` → `research.py` would be one-way).

**Change B: Delete the `_run_research_step` stub (lines 570-581).** It is fully replaced by the branch above calling into `lib/research.py`.

### 2. Research Module (lib/research.py)

**Purpose:** Orchestrate the research agent and manage the research log.

**Signature:**
```python
def run_research_step(
    concept: dict,
    iter_dir: Path,
    args: argparse.Namespace,
) -> list[Path]:
    """Run autonomous source acquisition. Returns list of newly-acquired source paths."""
```

**Flow:**

```
1. Derive paths:
   - analysis_path = ANALYSES_DIR / cid / "analysis.md"
   - log_path = ANALYSES_DIR / cid / "research_log.json"
   - output_path = iter_dir / "research_output.json"

2. Snapshot current sources:
   pre_sources = set(str(s) for s in find_sources(rid))

3. Load research log → format prior attempts summary for prompt

4. Build prompt from research.md template:
   - concept_name, concept_id (for add-source calls)
   - analysis_path (to read Section 6)
   - prior_attempts (formatted summary of already-attempted gaps)
   - output_path (where agent writes results)
   - max_searches, max_extractions (from args)

5. Save prompt to iter_dir / "research_prompt.md"

6. If dry_run: return []

7. invoke_claude(prompt, cwd=CONCEPT_ANALYSIS_DIR, timeout=args.timeout, model=args.model)

8. If rc != 0: print error, return []

9. Detect new sources (source of truth — filesystem diff):
    post_sources = find_sources(rid)
    acquired = [s for s in post_sources if str(s) not in pre_sources]

10. Update research log:
    - If output_path exists and parses as valid JSON:
      append agent's per-gap entries + record acquired paths by iteration
    - If output_path missing or malformed:
      log warning, still record acquired paths (from diff) with a
      note that agent output was unavailable

11. Return acquired
```

**Supporting functions:**

```python
def load_research_log(concept_dir: Path) -> dict:
    """Load research_log.json or return empty structure."""

def update_research_log(concept_dir: Path, new_entries: list[dict]) -> None:
    """Append entries to research_log.json."""

def format_prior_attempts(log: dict) -> str:
    """Format prior log entries as readable text for the research prompt.
    Groups by gap_id, shows status and what was tried."""
```

### 3. Research Prompt Template (prompt_templates/research.md)

The research agent runs as a single `claude -p` invocation with WebSearch, WebFetch, and Bash tools.

**Template variables:**
| Variable | Source |
|----------|--------|
| `concept_name` | `concept["Concept Name"]` |
| `concept_id` | `concept["_id"]` |
| `concept_num` | `concept["_num"]` (for `add-source` CLI calls) |
| `analysis_path` | Path to `analysis.md` |
| `output_path` | Path to write `research_output.json` |
| `max_searches` | `args.max_research_searches` |
| `max_extractions` | `args.max_research_extractions` |
| `prior_attempts` | Formatted summary from research log |

**Prompt structure (sections):**

1. **Role:** You are a research agent acquiring sources to fill data gaps in a fusion concept analysis.

2. **Files to read:** `{{analysis_path}}` — specifically Section 6 (Data Gap Inventory).

3. **Prior research attempts:** `{{prior_attempts}}` — skip gaps already marked `closed` or `failed`. Gaps marked `partial` may be re-attempted with different queries.

4. **Instructions — the search→triage→extract pipeline:**
   - For each `not-yet-sourced` gap (skip `proprietary`, `truly-unknown`, `derivable`):
     - **Search** (WebSearch, up to `{{max_searches}}` total): Construct queries from the gap's description and source recommendations. Try site-scoped queries for known databases (arxiv.org, osti.gov, scholar.google.com).
     - **Triage** (WebFetch): For each candidate URL, fetch and check: Is the content accessible? Is it relevant to the gap? Is it a full document (not a landing page, paywall, or JS-empty shell)? WebFetch passes content through a summarizer — use it ONLY for relevance/accessibility checks, never as source content.
     - **Extract** (Bash): For URLs that pass triage, run:
       ```
       uv run python scripts/run_analysis.py add-source {{concept_num}} "<url>"
       ```
       Up to `{{max_extractions}}` total extractions per invocation. If extraction fails, log the failure and continue.

5. **Source quality hierarchy:** (from spec FR-3) Peer-reviewed > government > institutional > press releases > news with quotes > news summaries.

6. **News-site heuristic:** (from spec FR-4) When company sites return nothing useful (JS-heavy, empty content), search for news coverage on The Engineer, NEI Magazine, WNN, GlobeNewsWire, ANS Nuclear Newswire.

7. **Rules:**
   - NEVER use WebFetch output as source content. WebFetch is for triage only.
   - NEVER write source files manually. Every source must come from `add-source`.
   - One URL per `add-source` call. No multi-source compilations.
   - Check that a URL is not already in the concept's sources before extracting.

8. **Output:** Write results to `{{output_path}}` using the Write tool. Format:

```json
{
  "gaps_attempted": [
    {
      "gap_id": "G-3",
      "gap_description": "Demountable joint fabrication premium",
      "queries": ["REBCO demountable joint cost manufacturing"],
      "candidates": [
        {
          "url": "https://example.com/rebco-costs",
          "title": "REBCO Manufacturing Cost Analysis",
          "triage": "relevant",
          "notes": "Contains 2024 cost projections"
        }
      ],
      "extracted": [
        {
          "url": "https://example.com/rebco-costs",
          "source_name": "example-rebco-costs"
        }
      ],
      "failed": [
        {
          "url": "https://paywalled.com/paper",
          "reason": "403 Forbidden — institutional access required"
        }
      ],
      "status": "closed"
    }
  ],
  "summary": {
    "gaps_attempted": 2,
    "sources_extracted": 1,
    "sources_failed": 1,
    "searches_used": 3,
    "extractions_used": 1
  }
}
```

**Note on gap identification:** Section 6 uses a table format. The research agent reads the table rows and identifies gaps by their position/description. The `gap_id` in the output is whatever identifier the agent derives (e.g., row number like "G-3" or a short slug from the gap description). This doesn't need to be machine-parseable by the orchestrator — it's for the research log's audit trail.

### 4. Research Log Schema

File: `analyses/{concept_id}/research_log.json`

The log has two sections: **per-gap entries** (from the agent's `research_output.json`, if parseable) and **per-iteration acquired paths** (from the filesystem diff — the source of truth for what was actually acquired).

```json
{
  "entries": [
    {
      "iteration": 2,
      "timestamp": "2026-04-05T18:30:00Z",
      "gap_id": "G-3",
      "gap_description": "Demountable joint fabrication premium",
      "queries": ["REBCO demountable joint cost"],
      "candidates": [
        {
          "url": "https://...",
          "title": "...",
          "triage": "relevant",
          "notes": "..."
        }
      ],
      "extracted": [
        {
          "url": "https://...",
          "source_name": "..."
        }
      ],
      "failed": [
        {
          "url": "https://...",
          "reason": "..."
        }
      ],
      "status": "closed"
    }
  ],
  "acquired_by_iteration": {
    "2": [
      "/abs/path/to/knowledge/concept_research/.../iter-3/sources/example-rebco-costs.md"
    ]
  }
}
```

**No `source_path` enrichment in entries.** The agent's `extracted[].source_name` is a self-reported slug that may not match the filesystem. The orchestrator does not attempt to correlate agent-reported names with actual paths. Instead:
- `acquired_by_iteration` records the actual paths from the pre/post `find_sources()` diff, keyed by iteration number. This is the authoritative record of what was acquired.
- `entries[].extracted` records what the agent *claims* it extracted (for audit trail / debugging).

When the agent output is missing or malformed, the orchestrator still records the diff-detected paths in `acquired_by_iteration` with a note:

```json
"acquired_by_iteration": {
  "3": {
    "paths": ["..."],
    "note": "agent output missing or malformed — paths detected by filesystem diff"
  }
}
```

The `format_prior_attempts()` function reads the log and produces a human-readable summary for the research prompt:

```
## Prior Research Attempts (do not re-attempt these)

### G-3: Demountable joint fabrication premium [CLOSED]
- Iteration 2: searched "REBCO demountable joint cost"
- Extracted: example-rebco-costs (https://example.com/rebco-costs)

### G-5: Tritium breeding ratio [FAILED]
- Iteration 2: searched "ARC tritium breeding blanket ratio"
- All candidates paywalled (IEEE, Elsevier)
```

### 5. CLI Flags (run_analysis.py)

Add to both `p_analyze` (after line 980) and `p_s1` (after line 1045):

```python
p.add_argument("--max-research-searches", type=int, default=5,
               help="Max WebSearch calls per research step (default: 5)")
p.add_argument("--max-research-extractions", type=int, default=3,
               help="Max source extractions per research step (default: 3)")
```

Access via `getattr(args, "max_research_searches", 5)` and `getattr(args, "max_research_extractions", 3)` for safety (in case called from a code path that doesn't have these args).

Also update the `--research` help text from "not yet implemented" to describe actual behavior.

### 6. Data Flow (End-to-End)

```
Iteration N (N > 1, --research enabled):

1. loop.py calls run_research_step(concept, iter_dir, args)

2. research.py:
   a. Snapshots find_sources(rid)
   b. Loads research_log.json → formats prior attempts
   c. Builds prompt from research.md template
   d. Saves research_prompt.md to iter-N/
   e. invoke_claude(prompt) → research agent runs:
      - Reads analysis.md Section 6
      - WebSearch for gap queries
      - WebFetch for triage
      - Bash: add-source for extraction (→ knowledge/concept_research/{rid}/iter-NN/sources/)
      - Writes research_output.json to iter-N/
   f. Parses research_output.json → updates research_log.json
   g. Diffs find_sources(rid) → returns list[Path] of new sources

3. loop.py receives acquired sources:
   - If non-empty → _run_source_integration(concept, iter_dir, acquired, analysis_path, args)
     - source_integration.md prompt reads each new source via subagents
     - Produces structured findings (feedback_format.md)
     - Returns Path to feedback file
   - If empty → falls through to assess feedback

4. loop.py continues iteration:
   - Analyze step (feedback_pass mode, consuming source-integration findings)
   - Model-setup
   - Assess
   - Write verdict.json (research_ran=true)
```

### 7. File Changes Summary

| File | Change |
|------|--------|
| `scripts/lib/research.py` | **New.** ~200 lines. `run_research_step()`, log I/O, prior-attempts formatter. |
| `scripts/lib/loop.py` | **Modified.** Replace stub (lines 570-581) delete. Replace branch (lines 122-132) with research call + source-integration chain. |
| `prompt_templates/research.md` | **New.** Research agent prompt template. |
| `scripts/run_analysis.py` | **Modified.** Add `--max-research-searches` and `--max-research-extractions` to `p_analyze` and `p_s1`. Update `--research` help text. |
| `scripts/lib/__init__.py` | No change (empty, already exists). |

---

## Potential Risks

1. **`claude -p` tool availability.** The design assumes WebSearch, WebFetch, and Bash are all available. Settings confirm WebSearch and WebFetch are configured. Bash is always available with `--dangerously-skip-permissions`. **Mitigation:** FR-0 requires verification before implementation. Test with a simple research prompt on one concept first.

2. **`add-source` extraction cost.** Each extraction runs `agentic-mbse extract` which can cost $5-50. With default cap of 3 extractions per pass, worst case is ~$150/concept/pass. **Mitigation:** `--max-research-extractions` provides hard cap. Default of 3 is conservative.

3. **Research agent output format.** The agent must write valid JSON to `research_output.json`. LLMs occasionally produce malformed JSON. **Mitigation:** The orchestrator should handle parse failures gracefully — log a warning and fall through (return empty list). The research log update is skipped but sources acquired via `add-source` are still detected by the `find_sources()` diff.

4. **Research agent ignoring instructions.** The agent might use WebFetch content as source material, or write files directly instead of using `add-source`. **Mitigation:** Prompt enforcement (explicit rules section). The orchestrator detects new sources via `find_sources()` diff, not by trusting the agent's output — so manually-written files in the wrong location are simply ignored.

5. **Source-integration timeout.** Chaining research → source-integration means two Claude invocations per iteration. With default 900s timeout each, one iteration could take up to 30 minutes. **Mitigation:** Research step uses the same `--timeout` flag. Users can lower it if needed.

---

## Integration Strategy

The research step plugs into an explicitly designed extension point. No existing code paths are altered when `--research` is not passed. The only structural change to loop.py is replacing 10 lines of stub code with ~15 lines of real orchestration that reuses `_run_source_integration()`.

The prompt template is self-contained — it doesn't depend on any other prompt's output format. The source-integration chaining is handled by the loop, not the research agent, so the research agent has no knowledge of the feedback format.

---

## Validation Approach

### FR-0 Verification (prerequisite)
Run a minimal `claude -p` invocation that uses WebSearch and Bash:
```bash
echo "Use WebSearch to find 'REBCO superconductor cost'. Then use Bash to run: echo 'tools work'" | claude -p --dangerously-skip-permissions --verbose
```
Confirm both tools produce results.

### Dry-Run Validation
```bash
uv run python scripts/run_analysis.py stage1-all 02 --resume --research --dry-run
```
Verify: `research_prompt.md` saved to `iter-N/`, no Claude calls made, no sources modified.

### Single-Concept Test
Pick a concept with known `not-yet-sourced` gaps (e.g., 01-hts-compact-tokamak which had "demountable joint fabrication premium" gap):
```bash
uv run python scripts/run_analysis.py stage1-all 01 --resume --research --max-research-extractions 1 --max-research-searches 2
```
Verify:
- Research prompt saved to `iter-N/research_prompt.md`
- Research output saved to `iter-N/research_output.json`
- `research_log.json` created/updated
- If source acquired: source-integration ran, feedback file produced, analyze step consumed it
- If nothing acquired: loop fell through to assess feedback normally
- `verdict.json` has `research_ran: true`

### Backward Compatibility
```bash
# Without --research: unchanged behavior
uv run python scripts/run_analysis.py stage1-all 02 --resume --dry-run
# Verify: no research prompt, no research log activity
```

---

**Next Steps:** After approval → `/_my_plan` to break into implementation phases, or `/_my_implement` directly given the contained scope.
