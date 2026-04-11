# Spec: Phase 1a Source Replacement

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-28 14:13 PDT
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

The Phase 1a research pipeline used Claude Code's WebFetch tool to capture source material. WebFetch doesn't return actual page content — it passes pages through Haiku 3.5 and returns only Haiku's summary. The result is that all 166 source files across 36 concepts are Haiku paraphrases: 20-100 line summaries that discard tables, detailed engineering parameters, cost breakdowns, and quantitative data that were present in the original pages.

The concept analysis pipeline reads these files as primary input. Every analysis built on top of them inherits this lossy foundation. The `agentic-mbse[web]` feature (now complete) can extract actual page content via `agentic-mbse extract <url>`. Replacing the Haiku paraphrases with real extractions gives the analysis stage substantively richer material — particularly for the iterative analysis loop (ANALYSIS-V2 Item 1) which will re-analyze concepts against these sources.

### Success Criteria

- [ ] Every source file with a recoverable URL has been re-extracted with actual content
- [ ] Source files without URLs have had their original URL located via web search where possible
- [ ] Original files preserved as `.orig.md` for comparison and rollback
- [ ] A quality report exists documenting each replacement with a comparison between old (WebFetch) and new (extraction) content
- [ ] The replacement source files are drop-in compatible with `find_sources()` in `run_analysis.py` (same directory structure, same `.md` extension)

### Priority

Should complete before running the iterative analysis loop at scale (ANALYSIS-V2 Phase 4 integration testing), but is fully independent work. No dependency on ANALYSIS-V2 implementation; no changes to pipeline code.

---

## Problem Statement

### Current State

166 source files in `exploration/phase_1a/research/*/iter-*/sources/*.md` across 36 concepts. These were created by Phase 1a research agents that used WebFetch to "save" web content. Due to WebFetch's architecture (content goes through Haiku, only Haiku's paraphrase is returned), the files contain:

- 20-100 line summaries instead of the actual page content
- Paraphrased claims instead of direct quotes
- Omitted tables, parameter lists, and structured data
- No verbatim cost figures or engineering specifications that appeared in the original

**Source file inventory by URL availability:**

| Category | Count | Description |
|----------|-------|-------------|
| URL in header | 119 | Clear `**Source**: https://...` or similar in first 15 lines |
| URL in body only | 10 | URL appears in text but not in header metadata |
| Paper citation only | 8 | ArXiv ID, DOI, or journal reference — URL constructable |
| No URL anywhere | 29 | Synthesized notes, compiled summaries — URL must be found via web search |
| **Total** | **166** | |

Additionally, 2 concepts (20a-type-one-stellarator, 20b-renaissance-stellarator) have no source files at all (only dossiers). These are out of scope.

### Desired Outcome

Each source file that has a recoverable URL is replaced with the full extraction output from `agentic-mbse extract <url>`. The original file is preserved as `filename.orig.md`. A quality report documents each replacement with a side-by-side assessment.

For the ~29 files with no URL, the executing agent searches the web to find the likely original source, then extracts it. If the original cannot be found, the file is flagged in the report and kept as-is.

---

## Scope

### In Scope

- Re-extracting all ~166 source files using `agentic-mbse extract <url>`
- Locating original URLs for the ~29 files that have no URL (via web search using titles, key phrases, and concept context)
- Constructing URLs from paper citations (arXiv IDs → `https://arxiv.org/abs/...`, DOIs → `https://doi.org/...`)
- Renaming originals to `.orig.md` before replacement
- Producing a quality report with per-file comparison between old and new content
- The quality comparison MUST include what WebFetch returns for the same URL, so we can see the full chain: original page → WebFetch paraphrase → full extraction

### Out of Scope

- Changes to the analysis pipeline, prompts, or `run_analysis.py`
- Adding new sources not already in the source directories
- Modifying dossier files
- Concepts 20a and 20b (no source files exist)
- Re-running any concept analyses — that happens later under ANALYSIS-V2

### Edge Cases & Considerations

- **URLs that are now dead/moved**: Some source URLs may have changed since March 2026 capture. The executing agent should try the Wayback Machine or find the new URL. If unrecoverable, flag in report and keep original.
- **PDF URLs**: `agentic-mbse extract` handles PDFs natively. ArXiv PDFs, OSTI reports, and journal papers that are PDFs will route through the PDF pipeline automatically.
- **Paywalled content**: Some journal articles (ScienceDirect, Wiley, AIP) may be behind paywalls. The extraction will get whatever is publicly accessible (abstract, open-access version). Flag in report if content is limited.
- **Duplicate URLs across concepts**: Some URLs appear in multiple concepts (e.g., arXiv papers cited by related concepts). Extract once, copy to each location — but each file should be independently complete.
- **Very large extractions**: Some pages (Wikipedia, long reports) may produce very large markdown files. This is fine — the analysis agent uses subagents to read sources, so context budget is managed at that level.
- **Company websites with JavaScript**: `agentic-mbse[web]` uses `trafilatura` which doesn't render JS. Some company pages (e.g., `helionenergy.com/technology/`) may have thin content via static extraction. Flag in report; the original Haiku summary may actually contain more content for these cases (since WebFetch did render JS via the Turndown step).

---

## Requirements

### Functional Requirements

> Requirements are from user's request unless marked [INFERRED].

**Enumeration**

1. **FR-1**: The plan MUST include a complete enumeration of all source files to be replaced, organized by concept, with: filename, current URL (or "NONE — search needed"), and file category (header URL / body URL / citation only / no URL).

2. **FR-2**: For files with paper citations only (arXiv IDs, DOIs), the plan MUST construct the full URL before extraction (e.g., `arXiv:2508.06761` → `https://arxiv.org/abs/2508.06761`).

3. **FR-3**: For files with no URL anywhere, the executing agent MUST search the web to find the likely original source URL using the file's title, key content, and concept context. This is necessary to avoid building on hallucinated content.

**Extraction**

4. **FR-4**: Each source file with a recovered URL MUST be re-extracted using `uv run agentic-mbse extract <url>`.

5. **FR-5**: Before extraction, the original file MUST be renamed from `source.md` to `source.orig.md`. The new extraction MUST be saved as `source.md` (same filename as original).

6. **FR-6**: [INFERRED] The new source file MUST preserve or improve upon the metadata header from the original (source URL, retrieval date, title). The `agentic-mbse extract` output includes YAML frontmatter with this metadata.

7. **FR-7**: [INFERRED] If extraction fails (URL dead, paywall, timeout), the original file MUST be restored from `.orig.md` back to `.md`, and the failure MUST be logged in the quality report.

**Quality Review**

8. **FR-8**: The executing agent MUST manually review each extraction output. "Manually review" means: read the new extraction, compare it to the `.orig.md` file, and assess whether the new version is substantively richer.

9. **FR-9**: For each replacement, the executing agent MUST also check what WebFetch returns for the same URL (using the WebFetch tool with a prompt like "Extract all technical content from this page"). This creates a three-way comparison: original `.orig.md` (what the Phase 1a agent saved) vs. WebFetch live result (what the tool actually returns) vs. new extraction (what `agentic-mbse extract` produces).

10. **FR-10**: The executing agent MUST write a quality comment for each file in a report log. The comment MUST include:
    - Whether the new extraction is richer than the original (YES/NO/MIXED)
    - A 1-2 sentence comparison noting what was gained or lost
    - Any flags (paywall, JS-rendered content, dead URL, etc.)

11. **FR-11**: The quality report MUST be saved as a single file at `exploration/phase_1a/research/source_replacement_report.md`, organized by concept.

**Cleanup**

12. **FR-12**: The `.orig.md` files MUST be retained until the user explicitly approves deletion. The spec does NOT include deletion — that is a separate manual step after review.

### Non-Functional Requirements

13. **NFR-1**: The replacement MUST NOT change the directory structure. Files stay in their existing `iter-*/sources/` locations. `find_sources()` in `run_analysis.py` must continue to find them without code changes.

14. **NFR-2**: [INFERRED] The work SHOULD be done concept-by-concept (not file-by-file across all concepts) so that partial completion leaves whole concepts in a clean state.

15. **NFR-3**: [INFERRED] The executing agent SHOULD batch work to avoid excessive API calls — e.g., extract all files for one concept, then review and write report entries for that concept, before moving to the next.

---

## Acceptance Criteria

### Core Functionality

- [ ] All ~137 files with recoverable URLs (header + body + citation) have been re-extracted
- [ ] All ~29 files with no URL have been searched; those where the original was found have been re-extracted
- [ ] Original files preserved as `.orig.md` alongside new `.md` files
- [ ] `find_sources()` returns the new files without any code changes

### Quality Report

- [ ] `source_replacement_report.md` exists with an entry for every source file (166 total)
- [ ] Each entry includes the three-way comparison comment (orig vs WebFetch vs extraction)
- [ ] Each entry has a YES/NO/MIXED quality verdict
- [ ] Files that could not be replaced are flagged with reason

### Integrity

- [ ] No source files were deleted — only renamed to `.orig.md`
- [ ] No new source files were added (only replacements of existing)
- [ ] No changes to `run_analysis.py` or any pipeline code

---

## Related Artifacts

- **Research:** `.project/research/20260328-source-capture-pipeline-feasibility.md`
- **Research:** `.project/research/20260328-web-content-sanitization-for-llm-pipelines.md`
- **Tool:** `agentic-mbse[web]` (complete, on `webfetch-tools` branch → merged)
- **Downstream:** ANALYSIS-V2 epic (`.project/backlog/epic_concept_analysis_v2.md`) — benefits from richer sources but has no dependency on this work item
- **Design:** `.project/active/source-replacement/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
