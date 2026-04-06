# Concept: Autonomous Source Acquisition

**Created:** 2026-04-04
**Status:** Draft

---

## Problem Statement

The analysis loop (assess → analyze, repeating up to `--max-passes`) converges well on structural/framing problems — consolidating differentiators, stating testable hypotheses, recommending modeling approaches. But it hits a hard wall on data problems.

The analysis agent writes Section 6 (Data Gap Inventory) as a structured table classifying each gap by type (`truly-unknown`, `proprietary`, `not-yet-sourced`, `derivable`) with criticality ratings and source recommendations. Many gaps are marked `not-yet-sourced` with specific search strategies like "REBCO manufacturers' public roadmaps; Rocky Mountain Institute superconductor market analysis" or "ITER TBM results; ARC detailed design update." But nothing acts on these. The analyze step re-reads the same source documents and cannot produce data that isn't there.

Real example: concept 01 (ARC) reaches pass 3 with unresolved findings like "parameter table missing rows for demountable joint fabrication premium" — not because the analyst failed to look, but because no source in the concept's research directory contains that data.

The tools to acquire and incorporate new sources already exist:
- **`add-source <concept> <pdf-or-url>`** fetches a source, runs `agentic-mbse extract`, and places the output in the concept's `iter-NN/sources/` directory
- **The analyze step** can use any source listed in `source_paths` — it spawns subagents to read each one
- **WebSearch and WebFetch** are available in headless `claude -p` mode (configured in `.claude/settings.local.json`)

The missing piece is an autonomous research agent that bridges the gap between "the analysis says data exists somewhere" and "a source with that data is in the concept's directory."

## Success Criteria

1. **Data gaps trigger web research** — when the analysis contains `not-yet-sourced` gaps and the assessment flags data insufficiency, a research agent autonomously searches for sources to fill those gaps.
2. **Accessible sources get fetched and extracted** into the concept's source directory via the existing `add-source` pathway, producing proper source files with YAML frontmatter, companion dirs, and verbatim text.
3. **Inaccessible sources get queued for human action** — each entry includes the URL, what gap it would address, why it couldn't be fetched (403, paywall, requires login), and what the operator should do.
4. **The analysis improves** — the analyze step sees new sources in its refreshed `source_paths` and uses them to close or narrow the gaps that triggered research.
5. **Guardrails prevent runaway costs** — configurable limits on number of searches per concept, number of extractions per run, and total extraction budget (since `agentic-mbse extract` can cost $5-50/PDF).
6. **An audit trail exists** — a per-concept research log recording what was searched, what was found, what was fetched/rejected/queued, and why.
7. **Source provenance is clean** — every acquired source is a single-URL extraction via `agentic-mbse extract`, never a WebFetch summary or multi-source compilation.

---

## User Stories

**US-1:** As a pipeline operator, when I run the analysis loop, concepts with `not-yet-sourced` data gaps automatically get web research and source acquisition attempted, so analyses improve beyond what the initial source set supports.

**US-2:** As a pipeline operator, when the pipeline identifies a promising source it can't access, I find a structured queue file telling me what was found, why it failed, and what gap it would address, so I can manually download it and run `add-source` myself.

**US-3:** As a pipeline operator, I can control research behavior via CLI flags — disable it entirely, cap the number of searches or extractions, or set a budget limit — so I control cost and runtime.

---

## Key Behavior

### Current loop structure (lines 1270-1349 of `run_analysis.py`)

```
for pass_num in range(1, max_passes + 1):
    ASSESS  — assessment agent reads analysis.md, writes feedback_iter_N.md
             if VERDICT: PASS → break
             if max passes reached → break
    ANALYZE — analysis agent reads feedback, edits analysis.md via Edit tool
```

Sources are gathered once before the loop (`find_sources(rid)` at line 1135), formatted into `source_paths` in `common_vars` (line 1152), and reused unchanged for every pass. Even if new files appear in `iter-*/sources/` mid-loop, the analyze step's prompt doesn't list them.

### Proposed loop structure

```
for pass_num in range(1, max_passes + 1):
    ASSESS   — same as today
               if VERDICT: PASS → break
               if max passes reached → break
    RESEARCH — new step (details below)
               if sources acquired → refresh source_paths in common_vars
    ANALYZE  — same as today, but with potentially enriched source list
```

### The research step: search → triage → extract

The research step uses three different tools for three different jobs. This separation is critical — it was learned from investigating the Phase 1a research pipeline, where conflating search/triage/capture produced source files with no provenance (see `source-acquisition-investigation.md`).

**WebSearch** — discovery. Find candidate URLs. Returns result titles, URLs, and short excerpts. Good at: discovering which pages exist for a topic.

**WebFetch** — triage only. Fetches a URL and passes it through Haiku 3.5 with a prompt. The research agent never sees the raw page content — it sees Haiku's summary. This means:
- "Exact quotes" from WebFetch are Haiku's paraphrases, not verbatim text
- Numbers pass through Haiku's interpretation before the agent sees them
- WebFetch does NOT use a headless browser — JS-heavy pages return empty shells

WebFetch is useful for quick relevance checks ("does this page contain REBCO cost data?") and triage before expensive extraction ("is this a full paper or a paywall landing page?"). It must **never** be used to create source file content.

**`add-source` / `agentic-mbse extract`** — capture. The only acceptable way to create source files. Produces verbatim text extraction with YAML frontmatter (URL, timestamp, content hash), companion directory (raw HTML/PDF, images, metrics), and proper symlinks. One URL per source file — no multi-source compilations.

### Research agent flow

A new agent invocation between assess and analyze. The research agent:

1. **Reads the current analysis** — particularly Section 6's gap table to identify `not-yet-sourced` gaps with source recommendations
2. **Reads the assessment feedback** — to understand what the assessment flagged as insufficient, which may point to specific data needs
3. **Searches the web** — using WebSearch with queries derived from the gap descriptions and source recommendations. The prompt instructs the agent to get exact URLs, a description of what each source contains, and an assessment of whether it would address the gap.
4. **Triages candidates with WebFetch** — for each promising URL, uses WebFetch to quickly check: Is this page relevant to the gap? Is the content accessible (not paywalled, not JS-empty)? Does it contain the specific data needed? This is a cheap relevance check before committing to extraction.
5. **Extracts confirmed sources via `add-source`** — for URLs that pass triage, calls `add-source` (which runs `agentic-mbse extract`). This places properly-formatted, single-URL source files in the concept's `iter-NN/sources/` directory. One URL per source file — never compilations.
6. **Queues inaccessible sources** — for sources behind paywalls, 403s, or requiring institutional access, writes an entry to a human intervention queue file
7. **Logs everything** — writes a research log recording: queries run, URLs found, WebFetch triage results, extraction outcomes, queue entries, and which gap each action targeted

After the research step, if any new sources were acquired, the pipeline re-calls `find_sources(rid)` and updates `common_vars["source_paths"]` so the analyze step's prompt includes the new sources.

### Where the data actually lives

Phase 1a investigation revealed that for many fusion concepts, the useful technical data lives on **standard HTML news sites** (The Engineer, NEI Magazine, World Nuclear News, GlobeNewsWire), not on the JS-heavy company sites (which often return empty shells to non-browser clients). The research agent should know this: when a company site returns nothing useful, search for news coverage of the company's announcements — that's where the data is, in standard HTML that `agentic-mbse extract` handles perfectly.

### Source quality hierarchy

The research agent needs guidance on what to prioritize:
1. **Peer-reviewed papers** (arXiv, journal articles) — most authoritative for physics/engineering claims
2. **Government reports** (OSTI, DOE, IAEA) — authoritative for program data
3. **Institutional pages** (university, national lab) — authoritative for facility specs
4. **Press releases** (company's own) — authoritative for company announcements, funding, milestones
5. **News articles with direct quotes** (The Engineer, WNN, ANS) — good for sourcing company claims with attribution
6. **News summaries without quotes** — weakest acceptable source
7. **Blog posts, forums** — not acceptable as sole source for quantitative claims

### How the analyze step uses new sources

The analyze step already spawns subagents per source (via the `source_reader.md` pattern in `analysis_v2.md`). If `source_paths` now includes a newly-acquired source, the agent will read it like any other source. The feedback from the assessment step tells it what to improve, and the new source gives it data to improve with.

The analysis prompt may need a small addition telling the agent to check whether new sources contain data relevant to Section 6 gaps, and to update the gap table accordingly (close resolved gaps, narrow partially-resolved ones).

---

## What Changes

### `run_analysis.py`

- **Assessment loop (lines 1270-1349)**: Insert research step between assess and analyze. After research, if sources were acquired, re-call `find_sources(rid)` and rebuild `source_paths` in `common_vars`.
- **New function**: Orchestrates the research agent invocation — constructs the research prompt, invokes via `claude -p`, checks for acquired sources, writes human queue entries.
- **`add-source` reuse**: The research agent calls `add-source` for each source it wants to acquire. This is the existing function that handles PDF/URL extraction and directory placement.
- **CLI flags on `analyze` command**: `--research` (enable/disable, default off initially), `--max-research-sources N` (cap extractions per concept per pass), `--research-budget N` (cap total extraction cost).

### New prompt template: `prompt_templates/research.md`

The research agent prompt. Takes:
- Path to current `analysis.md` (for Section 6 gap table)
- Path to current `feedback_iter_N.md` (for assessment findings)
- The concept name and ID
- Budget/limit constraints

Must enforce:
- **Never write source file content from WebFetch output.** WebFetch is for triage, not capture.
- **Every source file created via `add-source` only.** This ensures YAML frontmatter, companion dir, verbatim text.
- **One URL per source file.** No multi-source compilations. The analysis agent synthesizes across sources at read time.
- **Log the full search → triage → extract chain** for each source: what query found it, what WebFetch preview showed, why it was deemed relevant to which gap, extraction outcome.

### Analysis prompt (`analysis_v2.md`, feedback pass mode)

Small addition: when new sources are present in `source_paths` that weren't there in prior passes, tell the agent to check whether they contain data relevant to Section 6 gaps and update the gap table (close resolved gaps, narrow partially-resolved ones).

### Assessment checklist (consider, not required)

Currently the assessment checks structural quality. It could be augmented to note when Section 6 contains `not-yet-sourced` gaps that seem researchable — but this may not be necessary if the research step reads Section 6 directly.

### Human intervention queue

A markdown file per concept (e.g., `research_queue.md` in the concept's analysis directory) listing sources the research agent found but couldn't access. Each entry includes:
- URL or reference
- What gap it would address (gap # from Section 6)
- Why it couldn't be fetched (HTTP status, paywall indicator, JS-only site, etc.)
- Suggested action for the operator

---

## Validation: Test Cases

The 21 NO-verdict `.orig.md` files from source replacement are ideal for validating this module:
- Contain verified-real data (10/10 spot-check confirmed)
- Domain hints in headers (even if not exact URLs)
- The actual source URLs are on standard HTML news sites that `agentic-mbse extract` handles
- 21 varied cases across startup profiles, news articles, press releases
- Measurable success: do the extracted sources cover the claims in the `.orig.md`?

---

## Out of Scope

- Researching `proprietary` or `truly-unknown` gaps — only gaps where published data likely exists
- Zotero integration for discovered sources — sources go directly to concept's iter directory
- Cross-concept source sharing — if concept 01 finds a useful report, it doesn't auto-propagate to others
- Automated paywall bypass
- Changing the assessment agent's role — it stays a framing/structural evaluator
- Using WebFetch output as source content — this recreates the Phase 1a provenance problems

## Open Questions

1. **Does `claude -p` have access to WebSearch/WebFetch?** Settings show them configured, and `--dangerously-skip-permissions` is used, but this needs verification. If not available in headless mode, the research agent needs a different invocation pattern.
2. **Should research run every iteration or only when the loop stalls?** Running every pass is more aggressive but costlier. Running only when findings persist across passes is more targeted. Could be controlled by a flag.
3. **What search providers work best for technical papers?** WebSearch hits general web. OSTI, Google Scholar, Semantic Scholar have better academic coverage. The research prompt could instruct the agent to target specific databases via site-scoped queries.

---

## Decomposition Guidance

1. **Research agent prompt** — build and test the prompt template that reads analysis + feedback, searches web via WebSearch, triages via WebFetch, and extracts via `add-source`. Enforce the search/triage/capture separation. This is the core new artifact.
2. **Pipeline integration** — wire the research step into the assessment loop, handle `source_paths` refresh, add CLI flags, write research logs and human queue.
3. **Analysis prompt update** — small change to feedback-pass mode telling the agent to use new sources for gap closure and update Section 6.

## Related Investigation

See `.project/concepts/source-acquisition-investigation.md` for the full analysis of how Phase 1a research agents created source files, why WebFetch output is lossy, and verification that the data in `.orig.md` files is real despite broken provenance.
