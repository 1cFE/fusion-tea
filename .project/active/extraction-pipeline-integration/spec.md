# Spec: Extraction Pipeline Integration (agentic-mbse Redesign)

**Status:** Implementation Complete (New Ingestion blocked on user action)
**Owner:** Reid W
**Created:** 2026-02-27 07:58:53 PST
**Complexity:** MEDIUM
**Branch:** processing-work
**Epic:** KNOW-DB (Item 5)

---

## Business Goals

### Why This Matters

The agentic-mbse extraction pipeline was redesigned from a 4-layer monolithic `--enhance` approach to an 8-step quality-gated pipeline with per-page assessment, budget-controlled Claude usage, and output validation. This redesign directly addresses the quality failures found in the corpus audit (all 5 sources failed on tables, 4/5 failed on headings, Source 3 had critical LLM dialogue contamination).

However, the redesign introduces breaking changes to fusion-tea's ingestion script: the primary output filename changed (`full_document.md` → `output.md`), CLI flags are deprecated (`--enhance` → `--budget`), and metadata files changed (`summary.json` → `metrics.json` + `decisions.json` + `cost.json`). The ingestion script currently references the old filenames and flags in 5+ locations and will produce broken results without updating.

### Success Criteria

- [x] `uv run python scripts/zotero_ingest.py` runs end-to-end with zero deprecation warnings from agentic-mbse
- [~] All extracted sources use uniform `output.md` format — all 6 have `output.md`; `full_document.md` intentionally retained via `--keep-legacy` for quality comparison (plan_v2). Run `--re-extract` without `--keep-legacy` to clean up.
- [ ] At least 12 documents successfully extracted — **blocked**: only 6 sources; requires user to add ~6 PDFs to Zotero (FR-9)
- [x] The 5 corpus-audit failures re-extracted with measurably improved quality: Delene LLM contamination 6→0 (fixed), Hsu ColN 3→0 (fixed), Waganer ColN 31→0 (fixed), Swanson strikethrough 2→0 (fixed via arXiv), Hawker strikethrough 17→12 (improved; remainder is upstream OCR limitation)
- [x] Extraction uses opus model and $50 budget by default (maximum quality, cost-insensitive)
- [~] Both paths updated in code and Zotero path verified via `--re-extract`; `--local-pdf` not end-to-end tested this session

### Priority

Continuation of KNOW-DB epic. Unblocks Item 4 completion (first corpus ingestion at scale) and all downstream knowledge research work.

---

## Problem Statement

### Current State

- `scripts/zotero_ingest.py` uses deprecated `--enhance` flag (line 101) — still accepted but emits `DeprecationWarning` and is effectively a no-op in the new pipeline
- `_flatten_extraction_output()` checks for `full_document.md` (lines 118, 121) — **hard break**, the PDF pipeline now writes `output.md`
- SHA256 computation targets `full_document.md` (lines 286, 377) — **hard break**, file doesn't exist
- `--no-enhance` CLI flag (line 62-64) maps to a deprecated concept — should be `--budget 0`
- Default extraction uses `sonnet` model with $2.00 budget — suboptimal for this project where cost is not a concern
- All 6 existing source directories contain old-format files (`full_document.md`, `summary.json`, `style.json`)
- Corpus audit showed 5/5 sources failed on tables, 4/5 failed on headings — the new pipeline's quality gate addresses these issues but hasn't been applied

### Desired Outcome

- Ingestion script fully aligned with the new 8-step extraction pipeline
- Smart defaults that maximize extraction quality (opus model, $50 budget)
- All sources re-extracted to uniform format with quality-gated output
- 12+ documents extracted demonstrating the pipeline works across diverse document styles

---

## Scope

### In Scope

1. **Update `scripts/zotero_ingest.py`** — all references to deprecated flags and old filenames
2. **Update CLI interface** — replace `--no-enhance` with `--budget` parameter, add `--model` parameter
3. **Set smart defaults** — $50 budget, opus model
4. **Re-extract all 6 existing sources** with the new pipeline
5. **Clean up old files** from re-extracted source directories (`full_document.md`, `summary.json`, `style.json`)
6. **Ingest ~6 additional documents** from Zotero (whatever is pending) to reach 12+ total
7. **Verify end-to-end pipeline** — both Zotero-sourced and `--local-pdf` paths

### Out of Scope

- Switching from CLI to Python API (`extract_pdf()`) — CLI is the stable interface
- Fixing agentic-mbse internal inconsistencies (DOCX backends still write `full_document.md`, `index.py` expects it) — upstream issues
- Splitting SOURCE_INDEX.md into per-type files
- CI/CD integration or scheduled batch runs
- Researching the extracted sources (separate work)
- Changes to `zotero_lib.py` (no filename references, no changes needed)

### Edge Cases & Considerations

- **`get_output_dir()` nesting**: agentic-mbse still creates a subdirectory named after the sanitized input filename when `--output` is passed. `_flatten_extraction_output()` is still needed but must check for `output.md` instead of `full_document.md`.
- **Existing source directories**: Since they contain `full_document.md` (not `output.md`), the new pipeline's skip-if-exists check (`output.md` presence) won't trigger. Re-extraction should work without `--force`. Use `--force` as a safety measure anyway.
- **INDEX.md generation**: The `--index` flag should work with the new pipeline since `extract_cli.py` passes the correct `output.md` path to the indexer. Verify during testing.
- **`--summarize` flag**: Still supported and unchanged. Continue using it.
- **Budget consumption at scale**: With $50 budget and ~12 documents, budget is ample. The per-document cost at opus is roughly $2-8 depending on page count and quality gate decisions. 12 documents at $50 each would be $600 max, but budget is per-invocation so each document gets up to $50.

---

## Requirements

### Functional Requirements

> Requirements below are from user's request unless marked [INFERRED].

1. **FR-1**: ✅ Replace `--enhance` flag usage with `--budget` flag in `run_extraction()`. The `--enhance` flag MUST NOT appear in any CLI invocation. — No `--enhance` in code; `--budget` and `--model` always passed.

2. **FR-2**: ✅ Replace `--no-enhance` CLI argument with `--budget` parameter. Default value MUST be `50.0` (USD). Passing `--budget 0` disables Claude enhancement (equivalent to old `--no-enhance`). — Verified in `--help` output.

3. **FR-3**: ✅ Add `--model` CLI argument to `zotero_ingest.py`. Default value MUST be `opus`. Valid choices: `opus`, `sonnet`, `haiku`. Passed through to agentic-mbse's `--model` flag. — Verified in `--help` output.

4. **FR-4**: ✅ Update `_flatten_extraction_output()` to check for `output.md` instead of `full_document.md`. — Uses `EXTRACT_OUTPUT` constant. Also fixed re-extraction flatten bug (early return when old output.md existed).

5. **FR-5**: ✅ Update SHA256 computation in both `process_zotero_item()` and `process_local_pdf()` to target `output.md` instead of `full_document.md`. — Both use `EXTRACT_OUTPUT` constant.

6. **FR-6**: ✅ Update warning messages referencing `full_document.md` to reference `output.md`. — Warnings use f-string with `EXTRACT_OUTPUT`.

7. **FR-7**: ✅ [INFERRED] Pass `--budget` and `--model` values through to the agentic-mbse CLI invocation in `run_extraction()`. — Always passed in CLI command construction.

8. **FR-8**: ✅ Re-extract all 6 existing sources using the updated pipeline. — All 6 re-extracted twice (v1 without Claude, v2 with Claude). Legacy files intentionally retained via `--keep-legacy` for quality comparison; cleanup capability exists and is tested.

9. **FR-9**: ❌ **BLOCKED** — Ingest additional documents from Zotero to reach at least 12 total extracted sources. Requires user to add ~6 PDFs to Zotero and tag them.

10. **FR-10**: ✅ [INFERRED] The `run_extraction()` function signature MUST be updated to accept `budget` and `model` parameters instead of the `enhance` boolean. — Signature: `(pdf_path, output_dir, *, budget, model, force)`.

### Non-Functional Requirements

1. **NFR-1**: ✅ Zero deprecation warnings from agentic-mbse during extraction. — No `--enhance` or `--no-enhance` in code. Only 2 occurrences of "enhance" are in help text describing `--budget 0` and `--model`.

2. **NFR-2**: ✅ Extraction quality visibly improved for all 5 corpus-audit sources:
   - ✅ No LLM dialogue contamination — Delene: 6→0 (critical fix)
   - ✅ No ColN placeholder headers — Hsu: 3→0, Waganer: 31→0
   - ✅ Swanson strikethrough: 2→0 (fixed via arXiv HTML shortcut)
   - ⚠️ Hawker strikethrough: 17→12 (improved 29%, remainder is upstream OCR limitation in agentic-mbse, not fixable from fusion-tea side)

3. **NFR-3**: ✅ Default configuration maximizes quality. `DEFAULT_BUDGET = 50.0`, `DEFAULT_MODEL = "opus"`.

---

## Acceptance Criteria

### Core Functionality

- [x] `run_extraction()` builds a CLI command using `--budget` and `--model` flags (no `--enhance`)
- [x] `_flatten_extraction_output()` checks for `output.md` (not `full_document.md`)
- [x] SHA256 computed from `output.md` in both Zotero and local-PDF paths
- [x] `--budget` CLI arg with default `50.0` replaces `--no-enhance`
- [x] `--model` CLI arg with default `opus` is available
- [x] `run_extraction()` accepts `budget: float` and `model: str` parameters

### Re-extraction

- [x] All 6 existing sources re-extracted with new pipeline (twice: v1 without Claude, v2 with Claude)
- [x] Each re-extracted directory contains `output.md`
- [~] Old files intentionally retained via `--keep-legacy` for before/after quality comparison (plan_v2). Cleanup capability exists — run `--re-extract` without `--keep-legacy` to remove.
- [x] Re-extracted sources have `metrics.json` and `decisions.json` (all 6 confirmed)

### New Ingestion

- [ ] At least 6 additional documents ingested from Zotero — **BLOCKED: requires user to add PDFs**
- [ ] Total extracted sources >= 12 — **BLOCKED: currently 6**
- [ ] Documents represent varied styles — **BLOCKED**
- [ ] All new sources registered in SOURCE_INDEX.md with full metadata — **BLOCKED**
- [ ] All new sources recorded in MANIFEST.jsonl — **BLOCKED**

### Quality & Integration

- [x] Zero deprecation warnings from agentic-mbse in script output
- [~] Both paths: Zotero path verified via `--re-extract` (6/6 success); `--local-pdf` code updated but not end-to-end tested this session
- [x] Existing `zotero_lib.py` functions work without modification (zero diff)
- [x] Delene (Source 3) re-extraction shows no LLM dialogue contamination (6→0)

---

## Related Artifacts

- **Research:** `.project/research/20260227-074139_extraction-pipeline-redesign-integration.md`
- **Corpus Audit:** `work/analysis/corpus-ingestion-quality-audit.md`
- **Epic:** `.project/backlog/epic-knowledge-database-integration.md` (KNOW-DB)
- **Existing Script:** `scripts/zotero_ingest.py` (primary file to update)
- **Existing Lib:** `scripts/zotero_lib.py` (no changes needed)
- **agentic-mbse Extraction Docs:** `~/1cfe/agentic-mbse/docs/extraction.md`
- **Design:** `.project/active/extraction-pipeline-integration/design.md` (to be created)

---

## Code Change Summary

For design/implementation reference — the specific locations that need updating:

| File | Location | Change |
|------|----------|--------|
| `scripts/zotero_ingest.py` | Line 62-64 | Replace `--no-enhance` arg with `--budget` (float, default 50.0) |
| `scripts/zotero_ingest.py` | After line 64 | Add `--model` arg (choices: opus/sonnet/haiku, default opus) |
| `scripts/zotero_ingest.py` | Line 90 | Update `run_extraction()` signature: `enhance: bool` → `budget: float, model: str` |
| `scripts/zotero_ingest.py` | Lines 95-101 | Build CLI command with `--budget` and `--model` instead of `--enhance` |
| `scripts/zotero_ingest.py` | Line 118 | `full_document.md` → `output.md` |
| `scripts/zotero_ingest.py` | Line 121 | `full_document.md` → `output.md` |
| `scripts/zotero_ingest.py` | Line 278 | Update `run_extraction()` call site: pass `budget`/`model` |
| `scripts/zotero_ingest.py` | Lines 286-288 | `full_document.md` → `output.md` |
| `scripts/zotero_ingest.py` | Line 367 | Update `run_extraction()` call site: pass `budget`/`model` |
| `scripts/zotero_ingest.py` | Lines 377-379 | `full_document.md` → `output.md` |

---

**Next Steps:** After approval, proceed to `/_my_design`
