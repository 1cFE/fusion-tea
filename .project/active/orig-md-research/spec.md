# Spec: Re-source NO-Verdict .orig.md Files

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05
**Complexity:** MEDIUM
**Branch:** design-space-explore

---

## Business Goals

### Why This Matters

21 `.orig.md` files remain in `knowledge/concept_research/`. These are Haiku-paraphrased multi-source compilations from the Phase 1a research pipeline — verified-real data (10/10 spot-check confirmed in the provenance investigation) but with broken provenance: no single URL per claim, no YAML frontmatter, no companion dirs. They exist alongside thin replacement `.md` files that captured less content because the original URLs are JS-heavy company sites.

The data in these files is valuable for the analysis pipeline. But "Haiku said so" is not a citable source. The actual data lives on standard HTML news sites, press releases, and institutional pages (confirmed by the provenance investigation in `triage-report.md`) — sites that `agentic-mbse extract` handles perfectly.

### Success Criteria

- [ ] Each `.orig.md` file is processed: claims are matched to individually-extracted source files with proper provenance (YAML frontmatter, companion dir, single URL)
- [ ] Source files are placed in the concept's sources directory via `add-source`
- [ ] A per-file report records: what claims were in the `.orig.md`, which source(s) now cover them, which remain uncovered
- [ ] Fully-covered `.orig.md` files are deleted; partially-covered ones are flagged for human review
- [ ] The thin replacement `.md` files are also cleaned up (deleted if superseded by richer individual sources, or kept if they add unique content)

### Priority

Completes Phase 6 Step 3 of `plan-completion.md`. The last operational step before Phase 7 (SOURCE_INDEX reconciliation). Unblocks final cleanup of the source replacement project.

---

## Problem Statement

### Current State

Each of the 21 `.orig.md` files:
1. Contains real data (company specs, funding amounts, technical parameters, timelines)
2. Was compiled from 3-8 URLs by a research agent that visited multiple pages and summarized via Haiku
3. Has a header listing the original URLs (e.g., `**Sources**: firstlightfusion.com, newatlas.com, neimagazine.com`)
4. Sits alongside a thin `.md` replacement that only extracted the primary company URL (which is JS-heavy)

The autonomous source acquisition module (`lib/research.py`) was built for the analysis loop — it reads Section 6 gap tables, not `.orig.md` files. Different entry point, different prompt, different success metric.

### Desired Outcome

A standalone script that:
1. Reads each `.orig.md` to extract domain hints, company names, and source URLs from headers
2. Uses a `claude -p` agent to search for and extract the actual URLs where claims originate
3. Produces properly-traced individual source files via `add-source`
4. Reports coverage: which `.orig.md` claims are now backed by proper sources

---

## Scope

### In Scope

1. **Standalone script** — `scripts/resurface_orig.py` (or similar) in `exploration/concept_analysis/scripts/`
2. **Per-file processing** — reads `.orig.md` content, constructs research prompt, invokes `claude -p` agent
3. **Source extraction via `add-source`** — reuses the existing CLI command for proper provenance
4. **Coverage reporting** — per-file JSON/markdown report of what was sourced vs. gaps
5. **Cleanup decisions** — report recommendations for each `.orig.md` (delete, keep, partial)

### Out of Scope

- Modifying `lib/research.py` or the analysis loop — this is a separate operational script
- Headless browser extraction — if the primary URL is JS-heavy, the script finds news coverage instead
- Cross-concept source sharing — if concept 04 and concept 23 both need HB11 data, they get separate extractions
- Automated `.orig.md` deletion — script reports recommendations, human confirms

---

## What Can Be Reused

### Direct reuse (import or call as-is)

| Component | Location | What it provides |
|-----------|----------|-----------------|
| `invoke_claude()` | `lib/claude.py` | Headless `claude -p` invocation with timeout, model selection, stderr capture |
| `find_sources()` | `lib/sources.py` | Source discovery (before/after diff to detect acquired sources) |
| `cmd_add_source` / CLI `add-source` | `run_analysis.py:864` | Full extraction pipeline: `agentic-mbse extract` → companion dir → symlink → duplicate check |
| `fill_template()` | `lib/templating.py` | `{{variable}}` substitution in prompt templates |
| `_slugify_url()` / `_slugify_text()` | `lib/sources.py` | Source name generation from URLs |
| `find_latest_sources_dir()` | `lib/sources.py` | Finds the correct `iter-NN/sources/` directory for placement |

### Pattern reuse (adapt the approach, don't import directly)

| Pattern | Source | Adaptation needed |
|---------|--------|-------------------|
| Search → triage → extract pipeline | `prompt_templates/research.md` | Different input: `.orig.md` content + header URLs instead of Section 6 gap table. Same three-tool separation (WebSearch for discovery, WebFetch for triage, `add-source` for capture). |
| Research log schema | `lib/research.py` (research_log.json) | Adapt to per-file tracking instead of per-gap tracking. Same JSON structure works. |
| Filesystem-diff source detection | `lib/research.py:43-44,98-100` | Identical pattern: snapshot `find_sources()` before, diff after. |
| Prior-attempts memory | `format_prior_attempts()` in `lib/research.py` | May not be needed (single-pass per file), but useful if the script supports resume/retry. |

### Needs to be built new

| Component | Why it can't be reused |
|-----------|----------------------|
| **`.orig.md` parser** | Extracts: (a) the `Sources:` header URLs, (b) company/organization names, (c) quantitative claims worth sourcing, (d) domain context. No existing parser reads this format. |
| **Research prompt template** | `research.md` reads analysis gap tables with structured `gap_id`/`gap_type` fields. The `.orig.md` prompt needs to read free-text content with embedded URLs and produce search queries from claims, not gap entries. Core methodology (search→triage→extract, source quality hierarchy, news-site heuristic) is the same but the input parsing is different. |
| **Coverage reporter** | Compares `.orig.md` claims against acquired source content. Determines: fully covered → recommend delete, partially covered → flag gaps, uncovered → recommend keep. Nothing like this exists. |
| **Batch orchestrator** | Iterates over all 21 `.orig.md` files, manages per-file state, produces summary report. Simpler than the analysis loop — no iteration, no feedback, just process each file. |

---

## Requirements

### Functional Requirements

1. **FR-1**: The script MUST accept a list of `.orig.md` file paths (or `--all` to discover them via glob `knowledge/concept_research/**/iter-*/sources/*.orig.md`).

2. **FR-2**: For each `.orig.md`, the script MUST invoke a `claude -p` research agent that:
   - Reads the `.orig.md` content
   - Extracts the `Sources:` header URLs and tries them first (many are the actual original URLs)
   - Searches the web for claims that aren't covered by the header URLs
   - Triages candidates with WebFetch (accessibility, relevance)
   - Extracts confirmed sources via `add-source` (one URL per source file)

3. **FR-3**: The script MUST NOT use WebFetch output as source content. WebFetch is for triage only. All source files must be created via `add-source` (which calls `agentic-mbse extract`).

4. **FR-4**: The script MUST produce a per-file report (JSON) recording:
   - Original `.orig.md` path and content summary
   - URLs attempted (from header + web search)
   - Extraction outcomes (success, failure + reason)
   - Coverage assessment: which claims from `.orig.md` are now covered by extracted sources
   - Recommendation: `delete` (fully covered), `keep` (uncovered), `partial` (flag for review)

5. **FR-5**: The script MUST support `--dry-run` (save prompts without invoking Claude) and `--max-extractions N` (cap per file).

6. **FR-6**: The script MUST detect the correct concept from the `.orig.md` path (parse the concept ID from the directory structure) for `add-source` calls.

7. **FR-7**: The script SHOULD handle the common case where the `.orig.md` header lists 3-8 URLs. The "try header URLs first" strategy is expected to cover 60-80% of claims without web search.

8. **FR-8**: The thin replacement `.md` file (same name without `.orig`) SHOULD be noted in the report. If all its content is a subset of what the new individual sources cover, recommend deleting it too.

### Non-Functional Requirements

9. **NF-1**: Script should be under 300 lines (orchestrator only — prompt template is separate).

10. **NF-2**: Each `.orig.md` should be processable independently (no cross-file dependencies). This allows partial runs and resume.

11. **NF-3**: The prompt template should reuse the source quality hierarchy and news-site heuristic from `research.md` verbatim — don't reinvent methodology that's already validated.

---

## Edge Cases & Considerations

- **Header URL format varies**: Some have `**Sources**: url1, url2`, others have `Source: url`, others have URLs inline in text. The agent prompt should handle all three patterns rather than requiring a rigid parser.
- **Same company across multiple .orig.md files**: HB11 appears in concepts 04 and 23. Each gets its own extractions — no cross-concept sharing. Some URLs may be extracted twice. This is acceptable (disk is cheap, provenance is per-concept).
- **Header URLs may be dead**: Some company sites have changed since March 2026. The agent should note 404s/timeouts and search for cached/archived versions or news coverage.
- **The thin .md replacement may have unique content**: The replacement extracted the primary URL which may have some content not in the `.orig.md`. The report should note this.
- **Some .orig.md files are very short** (15-22 lines): These may need only 1-2 source extractions. The agent should not over-search.

---

## Acceptance Criteria

### Core Functionality

- [ ] Script processes at least 1 `.orig.md` file end-to-end in a test run
- [ ] At least one source file is created via `add-source` with YAML frontmatter + companion dir
- [ ] Per-file report is produced with coverage assessment
- [ ] `--dry-run` produces a reviewable prompt without invoking Claude
- [ ] `--all` discovers all 21 `.orig.md` files

### Quality

- [ ] Source files created via `add-source` only (no WebFetch content as source)
- [ ] Report correctly identifies which `.orig.md` claims are covered vs. uncovered
- [ ] Script is resumable (can be re-run on files that failed without re-processing successes)

---

## Related Artifacts

- **Provenance investigation:** `.project/concepts/source-acquisition-investigation.md`
- **Triage report:** `.project/active/source-replacement/triage-report.md` (lists all 21 files with context)
- **Concept doc:** `.project/concepts/autonomous-source-acquisition.md`
- **Research module (pattern source):** `exploration/concept_analysis/scripts/lib/research.py`
- **Research prompt (methodology source):** `exploration/concept_analysis/prompt_templates/research.md`
- **Plan-completion context:** `.project/active/source-replacement/plan-completion.md` (Phase 6 Step 3)
