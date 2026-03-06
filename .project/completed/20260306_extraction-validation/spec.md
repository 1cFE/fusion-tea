# Spec: Extraction Pipeline Validation

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-03-01 14:22 PST
**Complexity:** LOW
**Branch:** processing-work
**Epic:** `.project/backlog/epic-full-workflow-demo.md` — Item 1

---

## Business Goals

### Why This Matters

The v4 extraction pipeline (`doc-ingest-clean` branch of agentic-mbse) is a prerequisite for all downstream workflow demo work — source ingestion, research, and modeling all depend on extraction quality. Additional changes have landed in agentic-mbse since the last re-extraction (Feb 27), so we need to re-validate before proceeding.

This is infrastructure validation, not research — the goal is a quick go/no-go decision on whether the current extraction pipeline is acceptable for the investigation ahead.

### Success Criteria

- [ ] `--check` runs without errors (all pipeline components functional)
- [ ] `--dry-run` output reviewed for at least 2 sources
- [ ] All 6 sources re-extracted with v4 pipeline
- [ ] Quality comparison documented (vs. previous extraction)
- [ ] Acceptability verdict recorded

### Priority

P0 prerequisite — gates all other items in the Full Workflow Demo epic.

---

## Problem Statement

### Current State

- agentic-mbse `doc-ingest-clean` branch has both the validation stack restructure (8→6 levels) and extraction pipeline v4 (8-step orchestration, quality gates, ensemble table detection)
- fusion-tea has 6 existing extracted sources in `knowledge/sources/`, each with:
  - `full_document.md` — old extraction (pre-v4)
  - `output.md` — Feb 27 re-extraction (previous agentic-mbse code, prior to latest `doc-ingest-clean` changes)
  - `metrics.json`, `decisions.json`, `INDEX.md` — from Feb 27 run
- Known quality issues in old extraction (visible in Hawker `full_document.md`):
  - Garbled equations (e.g., `_Cp_ = _[α][P][e]_` with bracket artifacts)
  - Table structure destroyed (dot-leader walls instead of structured tables)
  - Page numbers misinterpreted as strikethrough (`~~**3**~~`)
  - LLM hallucination text embedded in extraction ("Wait, let me reconsider...", "Could you share the PDF page image so I can give you the exact LaTeX?")
- Additional changes have been made to agentic-mbse since the Feb 27 re-extraction — v4 pipeline not yet validated against current code
- `--check` (built-in corpus validation) and `--dry-run` (quality gate preview) are new v4 features, never exercised in fusion-tea

### Desired Outcome

Confidence that the current v4 extraction pipeline produces acceptable output for our fusion corpus, with any regressions or issues documented. A clear verdict on whether to proceed or file upstream issues first.

---

## Scope

### In Scope

1. Installation verification via `--check`
2. Quality gate preview via `--dry-run` on 2-3 sources
3. Full re-extraction of all 6 existing PDFs with v4 pipeline
4. Quality comparison: v4 output vs. previous `output.md` (qualitative + metrics)
5. Verdict document with findings and acceptability decision

### Out of Scope

- Fixing extraction bugs in agentic-mbse (file issues if found)
- Re-validating `zotero_ingest.py` integration (separate concern for new source ingestion)
- New source ingestion
- Any modeling, research, or taxonomy work

### Edge Cases & Considerations

- Hawker PDF has known upstream OCR/table limitations (17 strikethrough markers) — this is a known baseline, not a regression
- Some sources may have `images/` directories that affect re-extraction behavior (flatten gotcha documented in MEMORY.md)
- `--force` only bypasses `output.md` existence check; may need explicit cleanup of old files before re-extraction

---

## Requirements

### Functional Requirements

> Requirements below are from the epic item description and user's clarifications.

1. **FR-1**: Run `uv run agentic-mbse extract --check` and document the results — which pipeline components are available, any missing optional dependencies (GMFT, Img2Table, Docling, Pandoc)
2. **FR-2**: Run `--dry-run` on at least 2 existing source PDFs to preview quality gate decisions — which pages need enhancement, what issues are detected. Capture the `--dry-run` output as part of deliverables.
3. **FR-3**: Re-extract all 6 existing PDFs using the v4 pipeline with settings: `--force --budget 50 --model opus --index --summarize`
4. **FR-4**: Compare v4 output quality against previous `output.md` files using:
   - **Qualitative assessment**: Read both versions, note improvements and regressions in prose, equations, and overall readability
   - **Quantitative metrics where possible**: Table counts, header counts, strikethrough marker counts, file sizes, any metrics from `metrics.json` / `decisions.json`
5. **FR-5**: Document an acceptability verdict: proceed with v4, proceed with caveats, or block pending upstream fixes
6. **FR-6**: Capture `--check` output in the results document (not just pass/fail — include the component status details)

### Non-Functional Requirements

- Re-extraction MUST use `uv run` (project Python environment convention)
- Results document MUST be committed to git as a durable artifact
- Known issues (e.g., Hawker strikethrough) SHOULD be called out as pre-existing, not attributed to v4

---

## Acceptance Criteria

### Core Functionality

- [ ] `--check` runs without errors and output is captured in results
- [ ] `--dry-run` output captured for at least 2 sources
- [ ] All 6 sources have new `output.md` from v4 pipeline
- [ ] Quality comparison includes both qualitative notes and quantitative metrics for each source
- [ ] Verdict is recorded with clear rationale

### Quality & Integration

- [ ] Existing `full_document.md` files are preserved (not overwritten — they serve as the old-extraction baseline)
- [ ] Results document is self-contained and readable without needing to re-run anything

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-full-workflow-demo.md` — Item 1
- **Prior work:** `.project/completed/20260209_knowledge-database-integration/` (KNOW-DB Item 5 — previous re-extraction)
- **Script:** `scripts/zotero_ingest.py` (NOT used in this item — direct CLI only)
- **Sources:** `knowledge/sources/` (6 directories)
- **agentic-mbse:** `~/1cfe/agentic-mbse` on `doc-ingest-clean` branch

---

**Next Steps:** After approval, proceed directly to execution (no design doc needed — this is execution/validation work, not software construction).
**Deliverable:** `.project/active/extraction-validation/results.md`
