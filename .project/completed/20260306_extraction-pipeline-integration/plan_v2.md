# Implementation Plan v2: Re-extraction with Claude Fix

**Status:** Complete
**Created:** 2026-02-27
**Context:** The v1 re-extraction ran without Claude enhancement due to a JSON parsing bug in `invoke_claude()` (see `~/1cfe/agentic-mbse/.project/active/v4-claude-invocation-and-logging/design.md`). That bug is now fixed. This plan re-runs extraction with Claude actually working.

## Source Documents
- **v4 Fix Design:** `~/1cfe/agentic-mbse/.project/active/v4-claude-invocation-and-logging/design.md`
- **Integration Design:** `.project/active/extraction-pipeline-integration/design.md`
- **Original Plan:** `.project/active/extraction-pipeline-integration/plan.md`

## Key Constraint

**Do NOT remove old files.** Keep `full_document.md` and other legacy files in place for before/after quality comparison. The `_cleanup_legacy_files()` call in `re_extract_sources()` must be skipped or disabled for this run.

---

## Phase 1: Validate the Fix

### Goal
Confirm that the agentic-mbse Claude invocation fix is installed and working in the fusion-tea environment before spending budget on full re-extraction.

### Steps

#### 1. Verify agentic-mbse is up to date
- [x] Check that the installed agentic-mbse has the `invoke_claude()` JSON array parsing fix and `--check` flag
- [x] `uv run agentic-mbse extract --help` should show `--check` and `--check-json`

#### 2. Run `--check` on one PDF
- [x] `uv run agentic-mbse extract --check-json "knowledge/raw/Hawker - 2020 - A simplified economic model for inertial fusion.pdf"`
- [x] Verify output shows `claude.status == "pass"` (not `"fail"` or `"not_available"`)
- [x] Verify output shows `capabilities.math_reextraction == true`
- [x] Verify output shows `capabilities.table_enhancement == true`
- [x] Note the Claude cost for the probe (should be ~$0.07) — actual: $0.076

#### 3. Run `--check` on all 6 source PDFs
- [x] Run `--check-json` against each PDF in `knowledge/raw/` to confirm no per-document issues
- [x] All should show `overall: "pass"` and `claude.status: "pass"` — all 6 pass

### Validation
All `--check` probes pass with Claude available. Ready to spend real budget.

---

## Phase 2: Integration Changes

### Goal
Adjust `re_extract_sources()` to support a `--keep-legacy` mode so old files are preserved for comparison. Also surface stderr from extraction (new pipeline warnings from the v4 fix).

### Changes Required

#### 1. Add `--keep-legacy` flag to CLI
**File:** `scripts/zotero_ingest.py` (`parse_args()`)
- [x] Add `--keep-legacy` argument (store_true): "Keep old extraction files (full_document.md, etc.) for comparison"

#### 2. Conditionally skip legacy cleanup
**File:** `scripts/zotero_ingest.py` (`re_extract_sources()`)
- [x] Wrap the `_cleanup_legacy_files(output_dir)` call with `if not args.keep_legacy:`

#### 3. Surface stderr on success
**File:** `scripts/zotero_ingest.py` (`run_extraction()`)

The v4 fix added `logger.warning` for Claude failures, output rejection, and a post-loop summary. These go to stderr. Currently `run_extraction()` uses `capture_output=True` and only prints stderr on failure. On success, all pipeline warnings are silently discarded.

- [x] After successful extraction, print any stderr lines containing "WARNING" so pipeline issues are visible

### Validation
- [x] `uv run python scripts/zotero_ingest.py --help` shows `--keep-legacy`
- [x] Syntax check passes

---

## Phase 3: Re-extract All 6 Sources

### Goal
Re-run extraction with Claude actually working. Keep old files for comparison.

### Steps

#### 1. Smoke test: re-extract 1 source
- [x] `uv run python scripts/zotero_ingest.py --re-extract --keep-legacy --limit 1`
- [x] Verify `cost.json` exists in the output dir (proves Claude was called) — TEA DT MFE: $0.38 for 4 pages
- [x] Verify `output.md` was updated (check mtime or SHA256 change) — SHA256 changed
- [x] Verify `full_document.md` still exists (legacy preserved)
- [ ] ~~Check stderr output for Claude enhancement summary~~ — no WARNINGs emitted (all pages succeeded)

#### 2. Re-extract remaining 5 sources
- [x] `uv run python scripts/zotero_ingest.py --re-extract --keep-legacy` — 6/6 extracted, 0 failed
- [x] 4/6 show `cost.json` (Claude invoked where quality gate requested it). 2/6 correctly skipped Claude: Helios used arXiv HTML shortcut, Hsu was handled entirely by GMFT table detection.
- [x] All 6 still have `full_document.md` alongside `output.md` (legacy preserved)

### Validation
- [x] `ls knowledge/sources/*/cost.json` — 4/6 present (2 correctly skipped Claude)
- [x] `ls knowledge/sources/*/output.md` — all 6 present
- [x] `ls knowledge/sources/*/full_document.md` — all 6 still present (legacy kept)
- [x] `ls knowledge/sources/*/decisions.json` — all 6 present

---

## Phase 4: Quality Comparison

### Goal
Compare Claude-enhanced output against the old extraction to quantify improvement.

### Steps

#### 1. Hawker (Source 1) — strikethrough
- [x] NEW: 12 `~~` markers | OLD: 17 `~~` markers — **improved** (29% reduction)

#### 2. Delene (Source 3) — LLM dialogue contamination
- [x] NEW: 0 real contamination (2 false positives: "whereas" matching `here.s`)
- [x] OLD: 6 LLM dialogue lines ("Let me look at this", "Based on the text you provided", etc.) + 2 legitimate
- [x] **Critical fix confirmed** — zero LLM dialogue contamination in new extraction

#### 3. Hsu (Source 4) — ColN placeholders
- [x] NEW: 0 ColN placeholders | OLD: 3 ColN placeholders — **fixed**

#### 4. All sources — decisions.json truthfulness
- [x] Claude actions per source:
  - Delene: 7 claude / 39 total (18% of pages enhanced)
  - Waganer: 2 claude / 100 total (2%)
  - Hawker: 3 claude / 14 total (21%)
  - Araiinejad: 3 claude / 12 total (25%)
  - Helios: 0/0 (arXiv shortcut — no quality gate)
  - Hsu: 0/9 (GMFT handled all tables)
- [x] All claude_replace actions correspond to real Claude invocations (confirmed by cost.json)

#### 5. Cost summary
- [x] Total Claude spend: **$3.06**
  - Delene: $1.11 (39 pages, 7 enhanced)
  - Waganer: $1.09 (100 pages, 2 enhanced)
  - Araiinejad: $0.45 (12 pages, 3 enhanced)
  - Hawker: $0.41 (14 pages, 3 enhanced)

### Validation
Quality comparison table with old vs new metrics for each source. Decisions reflect reality.

---

## Risk Management

- **Phase 1 low risk**: `--check` is read-only, costs ~$0.07 per probe
- **Phase 2 low risk**: Adding a flag and an `if` guard
- **Phase 3 medium risk**: Real extraction with $50 budget per doc, ~$300 max total. Smoke test first with `--limit 1`
- **Phase 4 no risk**: Read-only comparison

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-02-27
**Results:**
All 6 PDFs pass `--check-json` with `claude.status: "pass"` and `overall: "pass"`.
| Source | Pages | Claude Cost | Key Capabilities |
|--------|-------|-------------|------------------|
| Hawker | 14 | $0.076 | math_reextraction, table_enhancement |
| Swanson | 30 | $0.092 | math_reextraction, table_enhancement, arxiv_shortcut |
| Delene | 39 | $0.068 | math_reextraction, table_enhancement |
| Hsu | 9 | $0.071 | math_reextraction, table_enhancement |
| Waganer | 100 | $0.062 | math_reextraction, table_enhancement |
| Araiinejad | 12 | $0.089 | math_reextraction, table_enhancement |
Total probe cost: ~$0.46
**Issues:** None

### Phase 2 Completion
**Completed:** 2026-02-27
**Changes:**
- Added `--keep-legacy` flag to `parse_args()` (store_true)
- Wrapped `_cleanup_legacy_files()` call with `if not args.keep_legacy:`
- Added stderr WARNING line surfacing after successful extraction in `run_extraction()`
- Also fixed agentic-mbse `--check-json` stdout contamination: added `PYMUPDF_SUGGEST_LAYOUT_ANALYZER=0` env var in `check.py:run_check()` as defense-in-depth against first-run pymupdf layout warning leaking through `redirect_stdout`
**Issues:** None

### Phase 3 Completion
**Completed:** 2026-02-27
**Results:** 6/6 extracted, 0 failed. 4/6 had Claude invoked (cost.json present). 2/6 correctly skipped Claude (Helios: arXiv shortcut, Hsu: GMFT handled all tables).
**Issues:**
- Flatten bug: `_flatten_extraction_output()` returned early when old `output.md` existed, leaving new extraction in nested subdir. Fixed by removing the early-return check and always looking for candidate nested subdirs.
- No stderr WARNINGs surfaced because all pages succeeded — the WARNING surfacing code is correct but had nothing to surface.

### Phase 4 Completion
**Completed:** 2026-02-27
**Quality Comparison:**

| Source | Metric | OLD | NEW | Verdict |
|--------|--------|-----|-----|---------|
| Hawker | `~~` strikethrough | 17 | 12 | Improved (29% reduction) |
| Delene | LLM dialogue lines | 6 | 0 | **Fixed** (critical) |
| Hsu | ColN placeholders | 3 | 0 | **Fixed** |

Total Claude spend: $3.06 across 4 sources (2 sources didn't need Claude).
Quality gate correctly routed: Helios used arXiv shortcut, Hsu handled by GMFT.
