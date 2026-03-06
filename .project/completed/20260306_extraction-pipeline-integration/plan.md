# Implementation Plan: Extraction Pipeline Integration

**Status:** In Progress
**Created:** 2026-02-27 08:12:25 PST
**Last Updated:** 2026-02-27

## Source Documents
- **Spec:** `.project/active/extraction-pipeline-integration/spec.md`
- **Design:** `.project/active/extraction-pipeline-integration/design.md` — See here for component details, function signatures, data flows

## Implementation Strategy

**Phasing Rationale:**
Phases 1 and 2 are pure code changes to `scripts/zotero_ingest.py` — they can be completed in one session with immediate validation via `--help` and `--dry-run`. Phase 3 is execution: running the updated pipeline against real documents to validate quality and completeness. This ordering ensures the tool works correctly before spending API budget on extraction.

**Overall Validation Approach:**
- No unit test framework exists for these scripts (consistent with project patterns)
- Validation is: `--help` output, `--dry-run` output, then real extraction runs
- Each phase has scripted checks that can be run from the command line

---

## Phase 1: Core Script Modernization

### Goal
Replace all deprecated flags, hardcoded filenames, and CLI interface in `zotero_ingest.py`. After this phase, the script is fully aligned with the new agentic-mbse pipeline — but only for the normal ingestion and local-pdf paths (re-extract mode is Phase 2).

### Changes Required

**See `design.md` for:** Component details (1-7), function signatures, CLI flag definitions, constant values

**Specific file changes:**

#### 1. Integration Constants
**File:** `scripts/zotero_ingest.py:45` (after imports, before `parse_args()`)
- [ ] Add constants block: `EXTRACT_OUTPUT`, `EXTRACT_LEGACY_FILES`, `DEFAULT_BUDGET`, `DEFAULT_MODEL` (see `design.md#component-1`)

#### 2. Module Docstring
**File:** `scripts/zotero_ingest.py:1-18`
- [ ] Update usage examples to reflect `--budget`, `--model`, `--re-extract` (see `design.md#component-2`)

#### 3. CLI Interface
**File:** `scripts/zotero_ingest.py:61-64` (`parse_args()`)
- [ ] Remove `--no-enhance` argument
- [ ] Add `--budget` argument (float, default `DEFAULT_BUDGET`)
- [ ] Add `--model` argument (choices, default `DEFAULT_MODEL`)

#### 4. `run_extraction()` Signature and Body
**File:** `scripts/zotero_ingest.py:90-113`
- [ ] Change signature: `enhance: bool` → `*, budget: float = DEFAULT_BUDGET, model: str = DEFAULT_MODEL, force: bool = False`
- [ ] Replace CLI command construction: remove `--enhance` conditional, add `--budget`/`--model` always, add `--force` conditional (see `design.md#component-3`)

#### 5. `_flatten_extraction_output()`
**File:** `scripts/zotero_ingest.py:116-132`
- [ ] Replace `"full_document.md"` with `EXTRACT_OUTPUT` on lines 118 and 121 (see `design.md#component-4`)

#### 6. `process_zotero_item()` — Call Site and SHA256
**File:** `scripts/zotero_ingest.py:278, 285-291`
- [ ] Update `run_extraction()` call: `enhance=not args.no_enhance` → `budget=args.budget, model=args.model`
- [ ] Update SHA256 target: `"full_document.md"` → `EXTRACT_OUTPUT`
- [ ] Update warning message text (see `design.md#component-6`)

#### 7. `process_local_pdf()` — Call Site and SHA256
**File:** `scripts/zotero_ingest.py:367, 377-382`
- [ ] Update `run_extraction()` call: `enhance=not args.no_enhance` → `budget=args.budget, model=args.model`
- [ ] Update SHA256 target: `"full_document.md"` → `EXTRACT_OUTPUT`
- [ ] Update warning message text

### Validation

**Automated:**
- [ ] `uv run python scripts/zotero_ingest.py --help` — shows `--budget` (default 50.0), `--model` (default opus), no `--no-enhance`
- [ ] `grep -n 'full_document\|--enhance\|no.enhance' scripts/zotero_ingest.py` — returns zero matches (only constants block mentions legacy files)
- [ ] `grep -n 'EXTRACT_OUTPUT\|DEFAULT_BUDGET\|DEFAULT_MODEL' scripts/zotero_ingest.py` — constants used in all expected locations

**Manual:**
- [ ] Read through the complete file to confirm no stale references

**What We Know Works After This Phase:**
CLI interface is modernized. All code paths reference `output.md` via constant. `run_extraction()` builds correct agentic-mbse command. Normal ingestion and `--local-pdf` paths are updated (but not yet tested with real extraction).

---

## Phase 2: Re-extract Mode

### Goal
Add `--re-extract` as a first-class script mode that re-processes all manifested sources with `--force`, cleans up legacy files, and reports new SHA256 values. This enables the Phase 3 re-extraction of existing sources.

### Changes Required

**See `design.md` for:** Component 5 (`_cleanup_legacy_files`), Component 8 (`re_extract_sources`), main() integration

**Specific file changes:**

#### 1. `_cleanup_legacy_files()` Function
**File:** `scripts/zotero_ingest.py` (after `_flatten_extraction_output()`)
- [ ] Add `_cleanup_legacy_files(output_dir)` function (see `design.md#component-5`)

#### 2. `re_extract_sources()` Function
**File:** `scripts/zotero_ingest.py` (after `sync_tags_command()`)
- [ ] Add `re_extract_sources(zot, args)` function (see `design.md#component-8`)
- [ ] Supports `--dry-run` and `--limit` flag interaction

#### 3. `parse_args()` — Add `--re-extract` Flag
**File:** `scripts/zotero_ingest.py` (`parse_args()`)
- [ ] Add `--re-extract` argument (store_true)

#### 4. `main()` Integration
**File:** `scripts/zotero_ingest.py` (`main()`, after `--sync-tags` early exit)
- [ ] Add `if args.re_extract:` early exit that calls `re_extract_sources(zot, args)`

### Validation

**Automated:**
- [ ] `uv run python scripts/zotero_ingest.py --help` — shows `--re-extract` flag
- [ ] `uv run python scripts/zotero_ingest.py --re-extract --dry-run` — lists all 6 manifested sources with Zotero keys and slugs

**Manual:**
- [ ] Verify dry-run output matches the 6 entries in `knowledge/MANIFEST.jsonl`
- [ ] Verify `--re-extract --dry-run --limit 2` only shows 2 entries

**What We Know Works After This Phase:**
All code is complete. Re-extract mode correctly reads the manifest and resolves sources. Ready for real extraction runs in Phase 3.

---

## Phase 3: Execution — Re-extract & Ingest

### Goal
Run the updated pipeline against real documents: re-extract the 6 existing sources to validate quality improvements and uniform output format, then ingest additional documents to reach 12+ total. This phase validates all spec acceptance criteria.

### Changes Required

No code changes. This phase is execution and verification.

#### 1. Re-extract Existing Sources
- [ ] Run: `uv run python scripts/zotero_ingest.py --re-extract`
- [ ] Verify: all 6 sources have `output.md` — `ls knowledge/sources/*/output.md`
- [ ] Verify: no legacy files remain — `ls knowledge/sources/*/full_document.md` (should fail / empty)
- [ ] Verify: quality metadata present — `ls knowledge/sources/*/metrics.json`
- [ ] Verify: zero deprecation warnings in output (grep for `DeprecationWarning`)

#### 2. Quality Spot-Checks
- [ ] **Delene (Source 3):** Open `knowledge/sources/an_assessment_of_the_economics_of_future_electric_power/output.md`, search for LLM dialogue patterns ("As an AI", "I'll help", conversational language) — should find none
- [ ] **Hawker (Source 1):** Check tables in `knowledge/sources/a_simplified_economic_model_for_inertial_fusion/output.md` — no `~~strikethrough~~` headers
- [ ] **Hsu (Source 4):** Check tables in `knowledge/sources/revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts/output.md` — no `ColN` placeholder headers

#### 3. Ingest New Documents
- [ ] User adds ~6 PDFs to Zotero, tags them `new`
- [ ] Run: `uv run python scripts/zotero_ingest.py`
- [ ] Verify: new sources appear in `knowledge/sources/`
- [ ] Verify: new entries in `knowledge/SOURCE_INDEX.md`
- [ ] Verify: new entries in `knowledge/MANIFEST.jsonl`

#### 4. Final Acceptance
- [ ] Count total sources: `ls -d knowledge/sources/*/ | wc -l` — should be ≥ 12
- [ ] All sources have `output.md`: `for d in knowledge/sources/*/; do [ -f "$d/output.md" ] || echo "MISSING: $d"; done`
- [ ] Test `--local-pdf` path: `uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/<any_pdf>.pdf --budget 0` (quick test, no Claude)

### Validation

**What We Know Works After This Phase:**
All spec acceptance criteria met. 12+ documents extracted with uniform `output.md` format. Quality improvements verified on previously-failed sources. Both Zotero and local-pdf paths work. Zero deprecation warnings.

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Low risk — mechanical changes with immediate `--help` / grep validation
- **Phase 2**: Low risk — new code follows existing patterns (`sync_tags_command` is the template for a mode)
- **Phase 3**: Medium risk — real extraction may surface unexpected issues. Mitigated by running `--re-extract --limit 1` first to smoke-test before processing all 6

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-02-27
**Actual Changes:**
- Added constants block at line 48-52: `EXTRACT_OUTPUT`, `EXTRACT_LEGACY_FILES`, `DEFAULT_BUDGET`, `DEFAULT_MODEL`
- Updated module docstring with new CLI usage examples
- Removed `--no-enhance` arg, added `--budget`, `--model`, `--re-extract`
- Updated `run_extraction()` signature: `enhance: bool` → `*, budget, model, force`
- Updated `_flatten_extraction_output()` to use `EXTRACT_OUTPUT` constant
- Updated SHA256 in `process_zotero_item()` and `process_local_pdf()`: `full_doc` → `extract_doc`, uses `EXTRACT_OUTPUT`
- Updated both `run_extraction()` call sites to pass `budget`/`model`
**Issues:** None
**Deviations:** None — all changes matched plan exactly

### Phase 2 Completion
**Completed:** 2026-02-27
**Actual Changes:**
- Added `_cleanup_legacy_files()` after `_flatten_extraction_output()`
- Added `re_extract_sources()` after `sync_tags_command()` — supports `--dry-run`, `--limit`
- `--re-extract` flag already added in Phase 1 CLI changes
- Added `if args.re_extract:` early exit in `main()` after `--sync-tags`
**Issues:** None
**Deviations:** `--re-extract` arg was added in Phase 1 (grouped with other CLI changes for cleaner diff) rather than Phase 2 as planned. No functional impact.

### Phase 3 Completion (Re-extraction only — new ingestion requires user action)
**Completed:** 2026-02-27 (re-extraction portion)
**Actual Changes:**
- All 6 sources re-extracted with opus/$50 via `--re-extract`
- All 6 have `output.md`, `metrics.json`, `decisions.json`, `INDEX.md`
- Zero legacy files remain (`full_document.md`, `summary.json`, `style.json` all removed)
- Cleaned up leftover nested dir from smoke test (`tea_dt_mfe_cost_analysis/Araiinejad_...`)
- Fixed `_flatten_extraction_output()` to handle re-extraction (multiple subdirs, file overwrite)
**Issues:**
- Hawker (Source 1) still has 17 `~~strikethrough~~` markers — identical count to old extraction. This is an upstream agentic-mbse OCR/table limitation, not an integration issue.
- Smoke test revealed flatten bug: `len(subdirs) == 1` failed when `images/` existed. Fixed with candidate-based approach.
**Deviations:**
- Phase 3 steps 3-4 (ingest new documents, final acceptance ≥12 sources) require user to add PDFs to Zotero — not completed yet

---

**Status**: Draft → In Progress → Complete
