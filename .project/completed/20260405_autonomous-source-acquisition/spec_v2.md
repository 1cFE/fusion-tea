# Spec v2: Autonomous Source Acquisition (Research Step)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-04-05
**Complexity:** MEDIUM
**Branch:** design-space-explore
**Depends on:** `.project/active/refactor-stage1-loop/` (Work Item #2 — loop refactor, complete)

---

## Business Goals

### Why This Matters

The analysis loop (assess → analyze, up to `--max-passes`) converges well on structural problems but hits a hard wall on data problems. The analysis agent writes Section 6 (Data Gap Inventory) classifying each gap by type (`truly-unknown`, `proprietary`, `not-yet-sourced`, `derivable`). Many gaps are marked `not-yet-sourced` with specific search strategies — but nothing acts on them. The analyze step re-reads the same source documents and cannot produce data that isn't there.

The tools already exist: `add-source` fetches and extracts sources, the analyze step reads any source in `source_paths`, and WebSearch/WebFetch are available in headless `claude -p` mode. The missing piece: a research agent that fills the `_run_research_step` stub in `lib/loop.py:570-581`.

### Success Criteria

- [ ] When `--research` is enabled, `not-yet-sourced` gaps trigger autonomous web search and source extraction between ASSESS and ANALYZE.
- [ ] Acquired sources have clean provenance: single URL, extracted via `add-source`, YAML frontmatter, companion dir.
- [ ] Sources the agent can't access are logged with URL, gap reference, and failure reason.
- [ ] The analyze step sees new sources on the next pass (existing `source_paths` refresh in loop.py handles this).
- [ ] Configurable limits prevent runaway costs (search cap, extraction cap).
- [ ] Existing loop behavior is unchanged when `--research` is not enabled.

### Priority

Fills the stub created by the stage1 loop refactor (FR-13/FR-14). The extension point, `--research` flag, and post-research source refresh are already wired — this spec defines what runs inside the stub.

---

## Problem Statement

### Current State

The `_run_research_step` stub in `lib/loop.py:570-581` prints "research step not yet implemented — skipping" and returns `None`. The loop already handles:

- **Flag parsing**: `--research` accepted by `stage1-all` and `analyze`
- **Feedback-producer selection** (loop.py:122-132): research is selected on iter > 1 when `--research` is set
- **Source refresh** (loop.py:130-132): `find_sources()` re-called after research returns
- **Fallback** (loop.py:126-129): if research returns `None`, falls through to normal assess feedback

The loop's feedback-producer contract is simple: return a `Path` to a feedback file in `config/feedback_format.md` schema, or `None` to skip. The research step just needs to fill this contract.

### Desired Outcome

`_run_research_step` calls a research agent (via `claude -p`) that reads the analysis's data gaps, searches the web, extracts promising sources via `add-source`, and produces a feedback file telling the analyze step what new data is available.

---

## Scope

### In Scope

1. **Research prompt template** (`prompt_templates/research.md`) — the prompt for the research agent
2. **Research orchestration** (`lib/research.py`) — replaces the stub, handles invocation, log writing, CLI flag wiring
3. **Research log** — per-concept append-only record of what was searched/found/extracted
4. **CLI flags** — extraction cap, search cap (on `analyze` and `stage1-all`)

### Out of Scope

- **Standalone re-sourcing of `.orig.md` files** — spec v1's "Mode B" is dropped. That's a separate tool if needed later.
- **Gap table schema extension** — the research step does not modify Section 6's format. It produces feedback findings that the analyze step uses to update gaps naturally.
- **Assessment agent changes** — unchanged, stays a framing/structural evaluator.
- **Researching `proprietary`, `truly-unknown`, or `derivable` gaps** — only `not-yet-sourced`.
- **Zotero integration** — sources go directly to concept's iter directory.
- **Cross-concept source sharing**.
- **Prompt template changes to `analysis_v2.md` or `assessment.md`** — the analyze step already reads whatever sources are in `source_paths`; no prompt change needed.

### Edge Cases

- **WebSearch/WebFetch availability in `claude -p`**: Must be verified. If unavailable, the research agent needs MCP or direct API calls instead.
- **JS-heavy company sites**: Useful data often lives on news sites (The Engineer, NEI Magazine, WNN, GlobeNewsWire), not JS-heavy company pages. The research prompt must encode this.
- **Duplicate sources**: The research agent may find a URL already in the concept's sources. Must check before extracting.
- **`add-source` failure**: Extraction can fail (paywall, JS-empty page, timeout). Failures are logged, not fatal.
- **Cost**: Each `agentic-mbse extract` call costs $5-50. The extraction cap is the primary cost control.
- **Pass 1 gaps are immature**: The earliest-pass threshold (currently implicit — `--research` only fires on iter > 1) prevents wasting research on gaps that would be refined by the first assess pass.

---

## Architecture

### How It Fits

```
lib/loop.py (existing):
  for iter_num in range(start_iter, max_passes + 1):
      ...
      elif args.research and iter_num > 1:         ← existing branch (line 122)
          feedback_path = _run_research_step(...)   ← STUB TO FILL
          if feedback_path is None:
              fall through to assess feedback       ← existing fallback
          find_sources() refresh                    ← existing (line 130-132)
      ...

lib/research.py (new):
  run_research_step(concept, iter_dir, args) → Path | None
    1. Read analysis.md Section 6 for not-yet-sourced gaps
    2. Read prior research log (skip already-attempted gaps)
    3. Build + invoke research prompt via claude -p
    4. Parse agent output → log entries
    5. Write research log (append)
    6. If sources acquired → run source-integration prompt → return feedback path
    7. If nothing acquired → return None
```

### The Research Agent (claude -p invocation)

A single Claude invocation that has access to WebSearch, WebFetch, and Bash (for `add-source`). The agent:

1. **Reads the analysis** — specifically Section 6's gap table to find `not-yet-sourced` gaps
2. **Reads the research log** (if exists) — skips gaps already attempted
3. **For each unattempted gap** (up to search cap):
   - Runs WebSearch with queries derived from the gap's source recommendations
   - Triages top results with WebFetch (relevance check, paywall detection, JS-empty detection)
   - For promising URLs (up to extraction cap): runs `add-source <concept> <url>` via Bash
   - For inaccessible URLs: logs the failure
4. **Writes a structured output file** containing:
   - Per-gap results (what was searched, what was found, what was extracted/failed)
   - A summary of acquired sources

The orchestrator (`lib/research.py`) then reads this output, appends entries to the research log, and returns the list of newly-acquired source paths (detected via `find_sources()` diff, not from the agent's self-reported output).

The **loop** (`loop.py`) — not `research.py` — handles the source-integration chaining. This avoids a circular import (`loop.py` → `research.py` → `loop.py`). The return type is `list[Path]` (acquired sources), not `Path | None` (feedback file). When the list is non-empty, the loop calls the existing `_run_source_integration()` to produce rich feedback.

### Feedback via Source-Integration

When the research step acquires sources, the loop chains into `_run_source_integration()` (loop.py:512-567). This gives the analyze step the same quality of feedback regardless of whether sources were added manually or autonomously:

```
research.py:run_research_step() returns list[Path]
    → loop.py refreshes find_sources()
    → loop.py calls _run_source_integration() with acquired paths
    → source-integration reads new sources, produces detailed findings
    → analyze step consumes findings in feedback-pass mode
```

This reuses `source_integration.md` — a prompt that already knows how to spawn subagents per source, assess what material information they contain, and produce structured findings in `config/feedback_format.md` format. The cost is one additional Claude call per research iteration that acquires sources, but the feedback quality matches the manual `source add` + `--resume` path (WI#2 FR-17).

The research agent itself stays focused on search/triage/extract — it does not need to understand the feedback format or produce analysis-quality findings about source content.

### The Research Log

A JSON file per concept at `analyses/{concept_id}/research_log.json`. Append-only across passes and runs. Schema:

```json
{
  "entries": [
    {
      "iteration": 2,
      "timestamp": "2026-04-05T...",
      "gap_id": "G-3",
      "gap_description": "Demountable joint fabrication premium",
      "queries": ["REBCO demountable joint cost", "HTS joint fabrication premium"],
      "candidates": [
        {
          "url": "https://example.com/article",
          "title": "...",
          "triage_result": "relevant|irrelevant|paywall|js-empty|error",
          "triage_notes": "Contains REBCO cost data from 2024"
        }
      ],
      "extracted": [
        {
          "url": "https://example.com/article",
          "source_name": "example-rebco-cost-data"
        }
      ],
      "failed": [
        {
          "url": "https://paywalled.com/paper",
          "reason": "403 Forbidden",
          "suggested_action": "Download from institutional access and run add-source manually"
        }
      ],
      "status": "closed|partial|failed|skipped"
    }
  ]
}
```

The orchestrator reads prior entries to skip already-attempted gaps (status `closed` or `failed`). Gaps with status `partial` may be re-attempted.

---

## Requirements

### Prerequisite

**FR-0**: `claude -p` MUST have access to WebSearch, WebFetch, and Bash tools. Verify before implementation by running a test invocation.

### Research Agent

1. **FR-1** (discovery/triage/capture separation): WebSearch for discovery, WebFetch for triage only, `add-source` (via Bash) for capture. WebFetch output MUST NOT become source content.

2. **FR-2** (single-URL sources): Every extraction targets exactly one URL via `add-source`.

3. **FR-3** (source quality priority): The research prompt MUST instruct the agent to prioritize: peer-reviewed papers > government reports (OSTI, DOE, IAEA) > institutional pages > press releases > news articles with direct quotes > news summaries. Blog posts and forums not acceptable as sole source for quantitative claims.

4. **FR-4** (news-site heuristic): The research prompt MUST encode: when company sites return nothing useful, search for news coverage of the company's announcements on standard HTML sites (The Engineer, NEI Magazine, WNN, GlobeNewsWire, ANS Nuclear Newswire).

5. **FR-5** (gap targeting): The research agent MUST read Section 6 of `analysis.md` and target only `not-yet-sourced` gaps. It MUST skip `proprietary`, `truly-unknown`, and `derivable` gaps.

6. **FR-6** (skip prior attempts): The research agent MUST read the research log and skip gaps already marked `closed` or `failed`. Gaps marked `partial` MAY be re-attempted.

7. **FR-7** (structured output): The research agent MUST write a structured output file (JSON or markdown with parseable sections) containing per-gap results: queries run, candidate URLs with triage outcomes, extraction results, and failures with reasons.

8. **FR-8** (duplicate check): Before calling `add-source`, the research agent MUST check that the URL is not already present in the concept's existing sources. (The `add-source` command also checks for duplicate names, but the URL check prevents wasted invocations.)

### Orchestration

9. **FR-9** (stub replacement): The `_run_research_step` stub in `lib/loop.py` and the `elif` branch that calls it (lines 122-132) MUST both be replaced. `lib/research.py:run_research_step()` takes `(concept, iter_dir, args)` and returns `list[Path]` — the list of newly-acquired source file paths (detected via `find_sources()` diff). The loop handles source-integration chaining (FR-10), not `research.py`.

10. **FR-10** (feedback via source-integration): When `run_research_step()` returns a non-empty list, the **loop** (not `research.py`) MUST call `_run_source_integration()` with the acquired paths to produce the feedback file. This is the same source-integration prompt used when the user manually runs `source add` + `--resume` (WI#2 FR-17). The source-integration step reads each new source via subagents and produces structured findings in `config/feedback_format.md` format.

11. **FR-11** (no-op when nothing found): If `run_research_step()` returns an empty list, the loop falls through to normal assess feedback. Source-integration is NOT invoked when nothing was acquired.

12. **FR-12** (log persistence): After the research agent completes, the orchestrator MUST append results to `research_log.json` in the concept directory. The log MUST be readable by subsequent iterations to support FR-6.

13. **FR-13** (research prompt saved): The rendered research prompt MUST be saved to `iter-N/research_prompt.md` for audit trail (consistent with how all other prompts are saved).

### CLI Flags

14. **FR-14** (extraction cap): `--max-research-extractions N` — maximum `add-source` calls per concept per pass. Default: 3. Applies to `analyze` and `stage1-all`.

15. **FR-15** (search cap): `--max-research-searches N` — maximum WebSearch calls per concept per pass. Default: 5. Applies to `analyze` and `stage1-all`.

16. **FR-16** (existing flags unchanged): The existing `--research` toggle, `--resume`, `--max-passes`, `--model`, `--dry-run`, `--force`, and `--timeout` flags continue to work as documented.

### Non-Functional

17. **FR-NF-1**: `lib/research.py` MUST be under 300 lines (consistent with lib/ module size convention).
18. **FR-NF-2**: The research prompt template MUST be a standalone file in `prompt_templates/research.md`.
19. **FR-NF-3**: No changes to existing prompt templates (`analysis_v2.md`, `assessment.md`, etc.).

---

## Acceptance Criteria

### Core Functionality

- [ ] `stage1-all 02 --resume --research` on a concept with `not-yet-sourced` gaps in Section 6: the research step fires, searches the web, and attempts extraction for at least one gap.
- [ ] Acquired sources appear in `knowledge/concept_research/{rid}/iter-*/sources/` with YAML frontmatter and companion directories (standard `add-source` output).
- [ ] The subsequent analyze pass sees the new sources in its prompt (verify via `--dry-run` after a research pass that acquired sources).
- [ ] `research_log.json` contains structured entries for each attempted gap.
- [ ] When sources acquired, source-integration prompt runs on the new sources and produces feedback in `config/feedback_format.md` format — same quality as manual `source add` + `--resume`.

### Skip / No-Op Behavior

- [ ] Research step returns `None` (no-op) when Section 6 has no `not-yet-sourced` gaps.
- [ ] Research step skips gaps already in the log as `closed` or `failed`.
- [ ] Extraction cap respected: at most `--max-research-extractions` calls to `add-source` per pass.
- [ ] Search cap respected: at most `--max-research-searches` WebSearch calls per pass.
- [ ] When no sources acquired, loop falls through to normal assess feedback (existing behavior).

### Backward Compatibility

- [ ] `stage1-all 02` (without `--research`) behaves identically to before — research step does not fire.
- [ ] `analyze 02 --resume` (without `--research`) behaves identically — no research.
- [ ] All non-stage1 commands (review, synthesize, etc.) unaffected.

### Dry Run

- [ ] `stage1-all 02 --resume --research --dry-run` saves the research prompt to `iter-N/research_prompt.md` without calling Claude or running any web searches/extractions.

### Quality

- [ ] No WebFetch output used as source file content (enforced in prompt).
- [ ] Every acquired source created via `add-source` only (enforced in prompt — no manual file writes).
- [ ] `lib/research.py` under 300 lines.
- [ ] No changes to existing prompt templates.

---

## Comparison: What Changed from Spec v1

| Aspect | Spec v1 | This spec (v2) |
|--------|---------|-----------------|
| Modes | Two (A: in-loop, B: standalone `.orig.md`) | One (in-loop only) |
| Gap table schema | Extended with research-state fields (FR-A5) | Unchanged — feedback findings handle it |
| Analysis prompt changes | Required (FR-A6) | None — existing source reading is sufficient |
| Assessment agent changes | None (same in both) | None |
| Research log | Complex schema with `gap_id`/`claim_id` bindings | Simpler: gap-indexed JSON entries |
| Human queue | Separate file with dedup across passes | Part of research log (`failed` entries) |
| Feedback generation | Research agent wrote feedback directly | Chains into existing `source_integration.md` prompt |
| Code integration | Would have wired into pre-refactor 2306-line file | Fills a clean stub in `lib/loop.py` |
| Complexity | HIGH | MEDIUM |

Key insight: the stage1 loop refactor created a clean extension point with a simple contract (return `Path | None`). Most of spec v1's complexity came from fitting into the old monolithic structure and trying to serve two different use cases.

---

## Decomposition Guidance

1. **Verify FR-0** — confirm `claude -p` can call WebSearch, WebFetch, and Bash. If not, document the workaround before proceeding.
2. **Research prompt template** — build `prompt_templates/research.md`. Test standalone with `claude -p` on one concept to verify it can search, triage, and call `add-source`.
3. **Orchestration module** — build `lib/research.py` with `run_research_step()`, log reading/writing, and feedback generation. Wire into the loop.py stub.
4. **CLI flags** — add `--max-research-extractions` and `--max-research-searches` to argparse.

---

## Related Artifacts

- **Concept:** `.project/concepts/autonomous-source-acquisition.md`
- **Investigation:** `.project/concepts/source-acquisition-investigation.md`
- **Spec v1 (superseded):** `.project/active/autonomous-source-acquisition/spec.md`
- **Loop refactor (prereq, complete):** `.project/active/refactor-stage1-loop/spec.md`
- **Code cleanup (prereq, complete):** `.project/active/refactor-run-analysis/spec.md`
- **Extension point stub:** `exploration/concept_analysis/scripts/lib/loop.py:570-581`
- **Feedback format:** `exploration/concept_analysis/prompt_templates/config/feedback_format.md`

---

**Next Steps:** After approval, proceed to `/_my_design` to decide research prompt structure and orchestrator implementation details.
