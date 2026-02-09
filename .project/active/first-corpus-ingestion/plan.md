# Implementation Plan: First Corpus Ingestion (KNOW-DB Item 4)

**Status:** Draft
**Created:** 2026-02-09
**Last Updated:** 2026-02-09

## Source Documents
- **Spec:** `.project/active/first-corpus-ingestion/spec.md`
- **Epic:** `.project/backlog/epic-knowledge-database-integration.md` — Item 4

## Implementation Strategy

**Phasing Rationale:**
This is an operational/execution task — no new code is written. The phases follow the natural pipeline flow: load the queue (Zotero curation) → drain the queue (batch ingestion) → verify output (quality audit) → validate end-to-end (research one source) → persist (commit). Each phase produces verifiable output before the next begins.

**Overall Validation Approach:**
- Each phase has concrete pass/fail checks
- Quality audit (Phase 3) gates committing (Phase 5)
- Re-extraction is the remediation path for quality failures
- Repo size budget (< 100MB) checked before final commit

---

## Phase 1: Zotero Source Curation

### Goal
Get 5 fusion reference documents into the Zotero group library with PDFs attached and tagged `new`. This is the human-driven input step — everything downstream depends on having sources in the queue.

### Source Selection

Per spec FR-1, these 5 documents are targeted:

| # | Document | Relevance |
|---|----------|-----------|
| 1 | Najmabadi et al., "The ARIES-AT Advanced Tokamak" (FED, 2006) | Canonical tokamak design/cost reference |
| 2 | Najmabadi et al., "The ARIES-CS Compact Stellarator" (FED, 2008) | Stellarator comparison point |
| 3 | Sheffield et al., "A Cost Assessment of Future Electric Power Stations" (Fusion Technology, 2016) | Foundational fusion costing algorithms |
| 4 | Kovari et al., "PROCESS: A Systems Code for Fusion Power Plants" (FED, 2014-2016) | Systems code documentation |
| 5 | Entler et al., "Approximation of the Economy of Fusion Energy" (Energy, 2018) | Fusion LCOE methodology |

Substitutions allowed per spec if any document is paywalled or unavailable in PDF form. Replacement must be a publicly available fusion energy reference relevant to cost modeling or plant design.

### Steps

For each of the 5 documents:
- [ ] Locate PDF (publicly available or already in possession)
- [ ] Add to Zotero group library (ID 5428393) with correct bibliographic metadata
- [ ] Attach PDF as child item, sync to Zotero Storage
- [ ] Tag `new`

### Validation

**Verify queue is loaded:**
```bash
uv run python scripts/zotero_ingest.py --dry-run
```
- [ ] Output shows 5 items pending
- [ ] Each item shows a PDF filename (none say "no PDF — will skip")

**What We Know Works After This Phase:**
Zotero library has 5+ `new`-tagged items with PDF attachments, ready for the ingestion pipeline.

---

## Phase 2: Batch Ingestion

### Goal
Run `scripts/zotero_ingest.py` to process all `new`-tagged items through the full pipeline: download → extract → register → tag.

### Steps

- [ ] Run dry-run to confirm queue state:
  ```bash
  uv run python scripts/zotero_ingest.py --dry-run
  ```
- [ ] Run the batch ingestion (with `--enhance` default):
  ```bash
  uv run python scripts/zotero_ingest.py
  ```
- [ ] Review script output summary: N found, N extracted, N skipped, N failed

### Failure Handling

If any document **fails extraction** (timeout or error):
1. Re-run with `--no-enhance` for a faster pass:
   ```bash
   uv run python scripts/zotero_ingest.py
   ```
   (Script automatically skips already-extracted items via `-extracted` tag filter)
2. If still failing, use `--local-pdf` with the already-downloaded PDF from `knowledge/raw/`:
   ```bash
   uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/<filename>.pdf --no-enhance
   ```
3. For very large PDFs (500+ pages) hitting the 900s timeout, consider `--no-enhance` as the primary path

### Validation

- [ ] 5+ new directories exist under `knowledge/sources/`
- [ ] Each directory contains at minimum `full_document.md` and `INDEX.md`
  ```bash
  for d in knowledge/sources/*/; do echo "$d: $(ls "$d" | tr '\n' ' ')"; done
  ```
- [ ] SOURCE_INDEX.md has 6+ entries (1 existing + 5 new)
- [ ] Script summary shows 5 extracted, 0 failed
- [ ] Verify Zotero tags updated:
  ```bash
  uv run python -c "
  import sys; sys.path.insert(0, 'scripts')
  from zotero_lib import connect, load_api_key
  zot = connect(load_api_key())
  items = zot.everything(zot.top(tag=['extracted']))
  print(f'{len(items)} items tagged extracted')
  for i in items:
      print(f'  [{i[\"key\"]}] {i[\"data\"].get(\"title\", \"?\")}')
  "
  ```

**What We Know Works After This Phase:**
The full pipeline ran at batch scale. All 5 sources are extracted, registered, and tagged.

---

## Phase 3: Quality Audit

### Goal
Inspect extraction quality for each of the 5 new sources. Catch garbled text, broken tables, missing images, or incorrect heading hierarchy before committing.

### Audit Checklist Per Source

For each new source directory in `knowledge/sources/`:

**Headings (3-5 per document):**
- [ ] Open `full_document.md` and check that H1/H2/H3 hierarchy is correct
- [ ] No garbled/truncated heading text
- [ ] Section structure matches the original paper's table of contents

**Tables (2-3 per document, if present):**
- [ ] Markdown pipe tables have correct column alignment
- [ ] No merged-cell corruption (data in wrong columns)
- [ ] Numeric values preserved correctly (not garbled by OCR)

**Images (2-3 per document, if present):**
- [ ] Image files exist in `images/` subdirectory
- [ ] Markdown image references (`![...](images/...)`) point to existing files
- [ ] Images are reasonable quality (not blank or corrupted)

### Steps

For each source:
- [ ] **Source 1** (ARIES-AT): headings ☐ tables ☐ images ☐
- [ ] **Source 2** (ARIES-CS): headings ☐ tables ☐ images ☐
- [ ] **Source 3** (Sheffield costing): headings ☐ tables ☐ images ☐
- [ ] **Source 4** (PROCESS): headings ☐ tables ☐ images ☐
- [ ] **Source 5** (Entler LCOE): headings ☐ tables ☐ images ☐

### Re-Extraction for Quality Failures

If a source has significant quality issues:
1. Remove the extracted directory
2. Re-extract with enhanced flags:
   ```bash
   uv run agentic-mbse extract knowledge/raw/<filename>.pdf \
     --output knowledge/sources/<slug>/ \
     --index --summarize --enhance
   ```
3. If tables are the problem specifically, try with `--backend docling` or `--no-tables`
4. Re-audit after re-extraction

### Validation

- [ ] All 5 sources pass the heading/table/image checks (or issues documented with remediation notes)
- [ ] No PDFs accidentally committed (check `knowledge/raw/.gitignore` is intact)

**What We Know Works After This Phase:**
Extraction quality is verified across 5 diverse fusion documents. Any quality issues are documented or remediated.

---

## Phase 4: Research One Source

### Goal
Run the full `/research` workflow against one ingested source to produce DI-XXX entries in `knowledge/KNOWLEDGE.md`. This validates the complete knowledge pipeline end-to-end: extraction → research → domain insights.

### Source Selection

Recommended: **Sheffield et al., "A Cost Assessment of Future Electric Power Stations"** — most directly relevant to the fusion costing model and likely to produce immediately actionable DI-XXX entries for WI-006 through WI-018.

Alternative: Implementer's choice per spec FR-5.

### Steps

- [ ] Run `/research` against the selected source
- [ ] Review pending research entries in `knowledge/research/pending/`
- [ ] Approve relevant entries → moves to `knowledge/research/approved/`
- [ ] Verify new DI-XXX entries appear in `knowledge/KNOWLEDGE.md`
- [ ] Tag the Zotero item as `researched`:
  ```bash
  uv run python -c "
  import sys; sys.path.insert(0, 'scripts')
  from zotero_lib import connect, load_api_key
  zot = connect(load_api_key())
  item = zot.item('<ITEM_KEY>')
  zot.add_tags(item, 'researched')
  print('Tagged as researched')
  "
  ```

### Validation

- [ ] At least 1 new DI-XXX entry exists in `knowledge/KNOWLEDGE.md` (currently DI-001 through DI-014)
- [ ] DI-XXX entries have proper structure: Source, Context, Model implications, Analysis implications, Status
- [ ] Zotero item has `researched` tag

**What We Know Works After This Phase:**
The complete knowledge pipeline works end-to-end: Zotero → download → extract → research → domain insights. The project has actionable new domain knowledge.

---

## Phase 5: Commit and Size Check

### Goal
Stage and commit all new artifacts. Verify repo size stays under the 100MB budget.

### Steps

- [ ] Verify no secrets or PDFs are staged:
  ```bash
  git status
  ```
  - No `.pdf` files should appear
  - No `.env` or credential files should appear
- [ ] Stage new source directories and updated index files:
  ```bash
  git add knowledge/sources/*/
  git add knowledge/SOURCE_INDEX.md
  git add knowledge/KNOWLEDGE.md
  ```
- [ ] Commit with descriptive message
- [ ] Verify repo size:
  ```bash
  git count-objects -vH
  ```
  - [ ] Total size < 100MB

### Validation

- [ ] `git status` is clean (all new sources committed)
- [ ] `git count-objects -vH` shows size-pack < 100MB
- [ ] `git log --oneline -1` shows the commit
- [ ] No PDF files in the commit (`git diff --name-only HEAD~1` shows only markdown, images, json)

**What We Know Works After This Phase:**
All 5+ sources are committed, repo size is manageable, and the KNOW-DB epic is complete.

---

## Environment Setup

**See CLAUDE.md for full environment rules.** Key commands:
- All Python via `uv run python ...`
- Ingestion: `uv run python scripts/zotero_ingest.py`
- Extraction: `uv run agentic-mbse extract ...`
- Zotero API key in `.env` (gitignored)

---

## Risk Management

| Risk | Phase | Mitigation |
|------|-------|------------|
| Document paywalled/unavailable | Phase 1 | Substitute with another publicly available fusion reference per spec |
| Large PDF timeout (900s) | Phase 2 | Use `--no-enhance` for faster extraction; process in sections if needed |
| Poor extraction quality (garbled tables) | Phase 3 | Re-extract with `--enhance --force`, `--backend docling`, or `--no-tables` |
| Repo size exceeds 100MB | Phase 5 | Unlikely for 5 sources; if it happens, check for oversized images and remove or compress |

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:**
**Sources Selected:**
**Substitutions:**
**Issues:**

### Phase 2 Completion
**Completed:**
**Script Output:**
**Failures:**

### Phase 3 Completion
**Completed:**
**Audit Results:**
**Re-Extractions:**

### Phase 4 Completion
**Completed:**
**Source Researched:**
**DI-XXX Entries Created:**

### Phase 5 Completion
**Completed:**
**Repo Size:**
**Commit SHA:**

---

**Status**: Draft → In Progress → Complete
