---
date: 2026-02-27T07:41:39-06:00
researcher: Claude
topic: "Integration of Redesigned agentic-mbse PDF Extraction Pipeline into fusion-tea"
tags: [research, extraction, integration, pipeline, agentic-mbse]
status: complete
last_updated: 2026-02-27
---

# Research: Integration of Redesigned agentic-mbse PDF Extraction Pipeline

**Date**: 2026-02-27T07:41:39-06:00
**Researcher**: Claude
**Research Type**: Integration / Architecture

## Research Question

The agentic-mbse project just completed a redesign of its PDF extraction pipeline (documented in `~/1cfe/agentic-mbse/docs/extraction.md`). How does this affect fusion-tea's knowledge ingestion pipeline, what are the breaking changes, and what needs to be updated?

## Summary

- **The old 4-layer pipeline (`--enhance`) has been replaced by an 8-step quality-gated pipeline** with budget-controlled Claude usage. The `--enhance` flag is deprecated and emits a warning. The new pipeline is fundamentally different in architecture: instead of a monolithic AI pass, it uses per-page quality assessment and targeted surgical fixes.
- **The primary output filename changed**: `full_document.md` → `output.md`. This is a **hard breaking change** for fusion-tea's ingestion script, which checks for `full_document.md` in three places.
- **The metadata format changed**: Old `summary.json` (DOCX-oriented) is replaced by `metrics.json` + `decisions.json` + `cost.json` for PDFs. The PDF pipeline no longer writes `summary.json` at all.
- **The nesting behavior that `_flatten_extraction_output()` was designed to handle may no longer occur**, since the PDF pipeline now writes directly to the output directory rather than creating a subdirectory named after the file.
- **The quality issues identified in the corpus audit (LLM dialogue contamination, broken tables) are directly addressed by the new pipeline design** — the quality gate and budget system replace the all-or-nothing `--enhance` approach.

## Detailed Findings

### 1. CLI Flag Changes (Breaking)

**Old flags (used by fusion-tea)**:
```python
# scripts/zotero_ingest.py:95-101
cmd = [
    "uv", "run", "agentic-mbse", "extract", str(pdf_path),
    "--output", str(output_dir),
    "--index", "--summarize",
]
if enhance:
    cmd.append("--enhance")
```

**New flags** (from `extract_cli.py:363-457`):
| Old Flag | Status | New Equivalent | Notes |
|----------|--------|----------------|-------|
| `--enhance` | **Deprecated** (hidden, emits warning) | `--budget 2.0` (default) | Budget controls Claude usage automatically |
| `--no-enhance` | Superseded | `--budget 0` | Zero budget = no Claude calls |
| `--structure-only` | **Deprecated** (hidden, emits warning) | `--dry-run` | Preview quality gate without Claude |
| `--fix-tables` | **Deprecated** (hidden, emits warning) | `--no-tables` / default | Table detection is now automatic |
| `--output` | **Unchanged** | `--output` | Still works the same |
| `--index` | **Unchanged** | `--index` | Still works the same |
| `--summarize` | **Unchanged** | `--summarize` | Still works the same |
| *(new)* | — | `--budget USD` | Default $2.00, controls Claude spend |
| *(new)* | — | `--model {opus,sonnet,haiku}` | Default sonnet |
| *(new)* | — | `--no-img2table` | Disable second-pass table detection |
| *(new)* | — | `--docling` | Enable third-pass table detection |
| *(new)* | — | `--dry-run` | Quality gate preview, no Claude spend |
| *(new)* | — | `--html-path PATH` | arXiv HTML shortcut override |

**Impact**: The `--enhance` flag still works (hidden, backward-compatible) but emits a `DeprecationWarning`. It is effectively ignored since the new pipeline **always** runs the quality-gated approach — `--enhance` doesn't change behavior. The `--no-enhance` flag in `zotero_ingest.py` maps to the concept of `--budget 0`.

### 2. Output File Changes (Breaking)

**Old output** (DOCX-style, also used for enhanced PDFs):
```
knowledge/sources/<slug>/
├── full_document.md       ← main markdown
├── INDEX.md               ← section index
├── summary.json           ← {source_file, backend_used, statistics, ...}
├── images/                ← extracted figures
└── style.json             ← (sometimes present)
```

**New output** (PDF pipeline, from `extract_cli.py:252-264`):
```
knowledge/sources/<slug>/
├── output.md              ← main markdown (RENAMED)
├── INDEX.md               ← section index (unchanged)
├── metrics.json           ← {char_count, heading_count, heading_by_level, table_row_count, ...} (NEW)
├── decisions.json         ← [{page_num, action, reasons, details}, ...] (NEW)
└── cost.json              ← [{page_num, cost_usd, tokens, model}, ...] (NEW, only if Claude used)
```

**Key differences**:
- `full_document.md` → `output.md` — **Hard break**. Three locations in `zotero_ingest.py` reference `full_document.md`
- `summary.json` → No equivalent for PDFs. Only DOCX extraction still writes `summary.json`
- `images/` directory — Not produced by the new PDF pipeline (images stay inline via pymupdf4llm references)
- New `metrics.json`, `decisions.json`, `cost.json` provide much richer quality data

### 3. Affected Code in fusion-tea

**`scripts/zotero_ingest.py`** — 5 locations need updates:

| Line | Code | Issue |
|------|------|-------|
| 96-101 | `cmd.append("--enhance")` | `--enhance` is deprecated. Replace with `--budget` flag or remove entirely (default $2.00 budget is reasonable) |
| 118 | `if (output_dir / "full_document.md").exists():` | **Hard break**: File is now `output.md` |
| 121 | `if ... (subdirs[0] / "full_document.md").exists():` | **Hard break**: Same filename issue |
| 286-288 | `full_doc = output_dir / "full_document.md"` | **Hard break**: SHA256 computation targets wrong file |

**`scripts/zotero_ingest.py` parse_args()** — 1 location:

| Line | Code | Issue |
|------|------|-------|
| 62-64 | `--no-enhance` argument | Should be updated to `--budget 0` semantics |

**`work/analysis/corpus-ingestion-quality-audit.md`** — References `full_document.md` throughout but this is a historical document, no code impact.

### 4. The `_flatten_extraction_output()` Question

The old pipeline sometimes created a nested subdirectory: `output_dir/<sanitized_name>/full_document.md`. The `_flatten_extraction_output()` function moved contents up one level.

**In the new pipeline**: When `--output` is passed, `get_output_dir()` (`base.py:56-65`) uses the output_base path, but the PDF pipeline in `cmd_extract()` (`extract_cli.py:253`) writes directly to the `output_dir` returned by `get_output_dir()`. However, `get_output_dir()` **still creates a subdirectory** named after the sanitized filename:

```python
def get_output_dir(input_path, output_base=None):
    dir_name = sanitize_filename(input_path.name)  # e.g., "Hawker_2020_..."
    if output_base is not None:
        return output_base / dir_name              # output_base/Hawker_2020_...
    return input_path.parent / dir_name
```

So if fusion-tea calls:
```
agentic-mbse extract /path/to/paper.pdf --output knowledge/sources/my_slug/
```

The actual output lands at:
```
knowledge/sources/my_slug/<sanitized_pdf_name>/output.md
```

This means **`_flatten_extraction_output()` is still needed**, but must check for `output.md` instead of `full_document.md`.

### 5. Pipeline Architecture Comparison

**Old (4-layer, `--enhance`)**:
1. Base extraction (pymupdf4llm)
2. GMFT table extraction (optional)
3. Structural repair (AI heading detection)
4. Quality repair (AI equation/table cross-validation)

Layers 3-4 were all-or-nothing with `--enhance`. The LLM enhancement was monolithic — when it failed (as with Delene source 3), it injected conversational dialogue directly into the output.

**New (8-step, quality-gated)**:
1. arXiv shortcut (Pandoc HTML, skip remaining on success)
2. Base extraction (pymupdf4llm per-page)
3. Ensemble table detection (GMFT primary, Img2Table second-pass, Docling optional third-pass)
4. Table filtering & enhancement (budget-aware, per-table Claude)
5. Quality gate (per-page assessment: math garbling, table anomalies, text density)
6. Budget allocation (rank pages by severity, select top N within budget)
7. Claude page enhancement (vision-based, with validation against original)
8. Route & merge (KEEP / CLAUDE_REPLACE / GMFT_REPLACE / GMFT_APPEND / STRIP_FALSE / STRIP_BROKEN)

**Critical improvement**: Step 7 includes `validate_claude_output()` — each Claude result is validated against the original before acceptance. This directly addresses the LLM dialogue contamination found in Source 3 (Delene). Bad Claude output is rejected and the original pymupdf output is kept.

### 6. Quality Improvements for Known Issues

The corpus audit identified these issues. Here's how the new pipeline addresses each:

| Issue | Affected Sources | Old Pipeline | New Pipeline |
|-------|-----------------|--------------|--------------|
| LLM dialogue contamination | Source 3 (Delene) | `--enhance` injected LLM conversation | Quality gate validates Claude output; bad responses rejected |
| Strikethrough table headers | Sources 1, 2 | Not detected | `quality_gate.py` detects math garbling (strikethroughs) and routes to CLAUDE_REPLACE |
| `ColN` placeholder headers | Sources 4, 5 | Not detected | `quality_gate.py` detects ColN auto-headers, routes to STRIP_FALSE or GMFT_REPLACE |
| `<br>` HTML in tables | Sources 4, 5 | Not detected | `quality_gate.py` detects `<br>` artifacts, routes to STRIP_BROKEN or GMFT_REPLACE |
| Flat heading hierarchy | Sources 1, 4 | Fixed by `--enhance` Layer 3 | `postprocess.py` performs deterministic header promotion (bold patterns, split bold, appendix, plain-text) without LLM |
| DOI fragmentation | Source 2 | Not addressed | Not directly addressed (references are low priority) |

### 7. Existing Sources: Forward Compatibility

The 6 sources already extracted in `knowledge/sources/` use the old format (`full_document.md`, `summary.json`). After updating the ingestion script:

**Option A: Leave existing, new format going forward**
- Existing sources keep `full_document.md`, new ones get `output.md`
- Requires any code reading sources to check for both filenames
- Simplest, no re-extraction needed

**Option B: Re-extract all sources with new pipeline**
- Use `--force` to re-extract all 6 sources
- Produces uniform `output.md` format with quality metrics
- Addresses audit-identified quality issues (especially Source 3)
- More work upfront, cleaner long-term

**Option C: Rename existing files + re-extract problem sources**
- Rename `full_document.md` → `output.md` in existing directories
- Re-extract Source 3 (Delene) which has critical LLM contamination
- Middle ground: fast, mostly consistent

### 8. Programmatic API Alternative

The new pipeline exposes a clean Python API (`extraction/__init__.py`):

```python
from agentic_mbse.extraction import extract_pdf, PipelineConfig, PipelineResult

config = PipelineConfig(
    claude_budget_usd=2.0,
    claude_model="sonnet",
    enable_tables=True,
)
result: PipelineResult = extract_pdf(pdf_path, config=config)

# Access everything directly
result.markdown          # Final markdown string
result.metrics           # ExtractionMetrics dataclass
result.decisions         # List[PageDecision]
result.cost              # List[CostRecord]
result.total_cost_usd    # Float
result.elapsed_seconds   # Float
result.error             # Optional[str]
```

This would eliminate the subprocess call, flatten logic, and output file parsing. However, it couples fusion-tea more tightly to agentic-mbse internals. The CLI interface is the documented stable boundary.

## Code References

- `scripts/zotero_ingest.py:90-113` — `run_extraction()` and `_flatten_extraction_output()` — the primary integration point
- `scripts/zotero_ingest.py:62-64` — `--no-enhance` CLI flag definition
- `scripts/zotero_ingest.py:116-132` — `_flatten_extraction_output()` checks for `full_document.md`
- `scripts/zotero_ingest.py:286-291` — SHA256 computation on `full_document.md`
- `scripts/zotero_lib.py:15-18` — Constants (SOURCES_DIR, MANIFEST_PATH, etc.) — no changes needed
- `~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py:183-206` — Deprecation warnings for `--enhance`, `--fix-tables`, `--structure-only`
- `~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py:236-264` — New PDF output generation (`output.md`, `metrics.json`, `decisions.json`, `cost.json`)
- `~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py:363-457` — New CLI flag definitions
- `~/1cfe/agentic-mbse/src/agentic_mbse/extraction/pipeline.py:94-106` — `PipelineConfig` dataclass
- `~/1cfe/agentic-mbse/src/agentic_mbse/extraction/types.py:73-81` — `PipelineResult` dataclass
- `~/1cfe/agentic-mbse/src/agentic_mbse/extraction/base.py:56-65` — `get_output_dir()` nesting behavior
- `~/1cfe/agentic-mbse/src/agentic_mbse/extraction/postprocess.py:1-50` — Deterministic header promotion (replaces Layer 3 `--enhance`)
- `work/analysis/corpus-ingestion-quality-audit.md` — Quality issues with current extractions

## Architecture Insights

1. **The redesign shifts from "monolithic AI pass" to "surgical targeted fixes"**. The old `--enhance` sent the entire document through LLM layers. The new pipeline assesses each page individually and only sends problematic pages to Claude, with validation on the response. This is architecturally superior for cost control and quality.

2. **The quality gate is the key new component**. `quality_gate.py` (439 lines) implements per-page scoring for math garbling, table anomalies, heading anomalies, and text density. This information is persisted in `decisions.json`, providing full auditability of extraction decisions — something the old pipeline completely lacked.

3. **The old `--enhance` flag is a no-op in the new pipeline**. It's accepted silently (with a deprecation warning) but doesn't change behavior. The new pipeline **always** applies the quality gate; the `--budget` flag controls how much Claude intervention occurs. `--budget 0` is the true equivalent of `--no-enhance`.

4. **Output file naming is a genuine breaking change**, not just a flag rename. The PDF pipeline writes `output.md` at `extract_cli.py:254`; this is not configurable. Any consumer that expects `full_document.md` will break.

5. **The `get_output_dir()` nesting still applies**. When `--output` is passed, the pipeline still creates a subdirectory named after the sanitized input filename. The `_flatten_extraction_output()` workaround in fusion-tea is still necessary but needs its filename check updated.

## Feasibility Assessment

**Integration effort: Small (1-2 hours)**. The changes are well-scoped:

1. Update `run_extraction()` to use `--budget` instead of `--enhance` — straightforward flag swap
2. Update `_flatten_extraction_output()` to check for `output.md` — one-line change
3. Update SHA256 computation to target `output.md` — one-line change
4. Update `--no-enhance` CLI flag to `--budget 0` semantics — minor refactor
5. Decide on existing source handling (Option A, B, or C above)

**Risks**:
- **Low risk**: The deprecated flags still work, so even without updating, the pipeline won't crash — it just emits warnings and uses the new behavior anyway
- **Medium risk**: Existing sources use `full_document.md`; any code that reads sources needs to handle both filenames during the transition
- **No risk**: The `--index` and `--summarize` flags are unchanged

## Recommendations

### Immediate (Update Ingestion Script)

1. **Replace `--enhance` with `--budget`** in `run_extraction()`:
   ```python
   cmd = [
       "uv", "run", "agentic-mbse", "extract", str(pdf_path),
       "--output", str(output_dir),
       "--index", "--summarize",
       "--budget", str(budget),
   ]
   ```
   Add `--budget` as a configurable parameter (default `2.0`, `0` for no-Claude).

2. **Update `_flatten_extraction_output()`** to check for `output.md`:
   ```python
   def _flatten_extraction_output(output_dir: Path) -> None:
       if (output_dir / "output.md").exists():
           return
       subdirs = [d for d in output_dir.iterdir() if d.is_dir()]
       if len(subdirs) == 1 and (subdirs[0] / "output.md").exists():
           ...
   ```

3. **Update SHA256 target** in `process_zotero_item()` and `process_local_pdf()`:
   ```python
   full_doc = output_dir / "output.md"
   ```

4. **Replace `--no-enhance` flag** with `--budget`:
   ```python
   parser.add_argument("--budget", type=float, default=2.0,
       help="Claude budget in USD (default: 2.0, 0 = no Claude)")
   ```

### Short-term (Re-extract Problem Sources)

5. **Re-extract Source 3 (Delene)** with the new pipeline — the quality gate will prevent the LLM dialogue contamination that was the critical issue.

6. **Consider re-extracting all 6 sources** to get uniform `output.md` format and benefit from the new quality gate, header promotion, and table handling improvements.

### Optional (Programmatic API)

7. **Consider switching to the Python API** (`extract_pdf()` directly) instead of subprocess. This would eliminate:
   - The flatten workaround
   - Subprocess timeout management
   - Output file parsing

   But it increases coupling to agentic-mbse internals. The CLI is the more stable interface. **Recommend staying with CLI for now.**

## Open Questions

1. **Should we maintain backward compatibility with `full_document.md`?** If other code or workflows read from `knowledge/sources/<slug>/full_document.md`, we need a transition strategy. Need to check if any agentic-mbse commands (e.g., `/research`, section reading) expect `full_document.md`.

2. **What budget should be the default for batch ingestion?** The new pipeline defaults to $2.00 per document. For a batch of 20+ documents, this could be $40+. May want a lower default (e.g., $0.50) for batch runs with an option to increase for priority sources.

3. **Should `metrics.json` and `decisions.json` be committed to git?** They provide valuable quality auditability but add ~10-50KB per source. The corpus audit was done manually; these files would make it automatic.

4. **Index generation**: The new pipeline generates INDEX.md from `output.md` (not `full_document.md`). Need to verify the `--index` flag still works correctly with the new output path when called via `--output`.
