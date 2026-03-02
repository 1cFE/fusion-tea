# Implementation Plan: First Corpus Ingestion (KNOW-DB Item 4)

**Status:** Draft
**Created:** 2026-02-09
**Last Updated:** 2026-02-09

## Source Documents
- **Spec:** `.project/active/first-corpus-ingestion/spec.md`
- **Pipeline V2 Design:** `.project/active/ingestion-workflow-v2/design.md` ← See here for pipeline mechanics, CLI flags, manifest format

## Implementation Strategy

**Phasing Rationale:**
This is an execution task (running existing tooling), not a code development task. No design doc needed. Phases follow the natural pipeline order: curate sources → ingest → audit quality → fix issues → research → commit → tag sync. Each phase has a clear gate before proceeding.

**Key Constraint:** Source selection and Zotero curation (Phase 1) is a manual/human step — the user must add PDFs to Zotero. Phases 2+ are automatable.

---

## Phase 1: Source Selection & Zotero Curation

### Goal
Get 5 fusion reference documents into the Zotero group library with PDFs attached. This is the prerequisite for everything else.

### Steps

- [ ] Identify 5 target documents per FR-1 (spec table):
  1. Najmabadi et al., "The ARIES-AT..." (Fusion Eng. & Design, 2006)
  2. Najmabadi et al., "The ARIES-CS..." (Fusion Eng. & Design, 2008)
  3. Sheffield et al., "A Cost Assessment of Future Electric Power Stations" (Fusion Technology, 2016)
  4. Kovari et al., "PROCESS: A Systems Code..." (Fusion Eng. & Design, 2014-2016)
  5. Entler et al., "Approximation of the Economy of Fusion Energy" (Energy, 2018)
- [ ] For each: verify PDF is obtainable (publicly available or already in possession). If paywalled, identify substitute per spec FR-1.
- [ ] Add each to Zotero group library (ID 5428393) with correct bibliographic metadata
- [ ] Attach PDF to each item (child attachment or standalone) and sync to Zotero Storage
- [ ] Record substitutions (if any) and Zotero keys for all 5 items

### Validation

- [ ] `uv run python scripts/zotero_ingest.py --dry-run` shows 5+ pending items (the new items appear because they are not in MANIFEST.jsonl)
- [ ] Each item has a PDF attachment visible in the dry-run output

**Gate:** Do not proceed to Phase 2 until dry-run confirms all 5 items are in the pending queue.

---

## Phase 2: Batch Ingestion

### Goal
Run the ingestion pipeline to download, extract, and register all 5 sources.

### Steps

- [ ] Run ingestion with batch limit:
  ```
  uv run python scripts/zotero_ingest.py --limit 5
  ```
- [ ] Monitor output for errors (download failures, extraction timeouts, PDF resolution failures)
- [ ] If any item fails:
  - Check if PDF is accessible in Zotero Storage
  - Check for timeout (900s limit) — use `--no-enhance` for very large PDFs
  - Re-run; already-processed items will be skipped (idempotency via manifest)

### Validation

- [ ] 5 new directories exist under `knowledge/sources/`
- [ ] Each new directory contains at minimum `full_document.md` and `INDEX.md`
- [ ] `knowledge/MANIFEST.jsonl` exists and has 6 entries (1 seed + 5 new)
- [ ] `knowledge/SOURCE_INDEX.md` has 6+ entries total
- [ ] Idempotency check: re-run `uv run python scripts/zotero_ingest.py --dry-run` → 0 pending items

**Gate:** All 5 sources extracted and manifest updated before proceeding.

---

## Phase 3: Quality Audit

### Goal
Audit extraction quality for each source. Identify and remediate significant issues.

### Steps

For each of the 5 extracted sources:
- [ ] **Source 1** (ARIES-AT): Spot-check 3-5 headings, 2-3 tables, 2-3 images. Record pass/fail.
- [ ] **Source 2** (ARIES-CS): Same audit.
- [ ] **Source 3** (Sheffield cost assessment): Same audit.
- [ ] **Source 4** (PROCESS systems code): Same audit.
- [ ] **Source 5** (Entler fusion economy): Same audit.

Quality dimensions per source:
- **Headings**: Correct hierarchy (H1/H2/H3)? No garbled text?
- **Tables**: Structure preserved (rows/columns intact)? No merged-cell corruption?
- **Images**: Files exist in `images/`? Markdown references correct?

### Remediation (if needed)

- [ ] For sources with significant issues, re-extract:
  ```
  uv run python scripts/zotero_ingest.py --local-pdf knowledge/raw/<filename>.pdf --enhance --force
  ```
  Or try alternative flags: `--backend docling`, `--no-tables`
- [ ] Document quality issues and remediation in this section (Implementation Notes below)

### Validation

- [ ] Quality audit notes recorded for each source (pass/fail per dimension)
- [ ] Any re-extractions completed and re-audited

**Gate:** All 5 sources at acceptable quality before committing.

---

## Phase 4: Commit & Size Check

### Goal
Commit all extracted sources to git and verify repo size.

### Steps

- [ ] Verify `knowledge/raw/.gitignore` is intact (no PDFs staged)
- [ ] Stage extracted sources, MANIFEST.jsonl, and SOURCE_INDEX.md updates
- [ ] Commit with descriptive message referencing KNOW-DB Item 4
- [ ] Run `git count-objects -vH` and verify total size < 100MB

### Validation

- [ ] `git status` is clean
- [ ] No PDF files in the commit (`git diff --name-only HEAD~1` shows only markdown, images, jsonl, md)
- [ ] Repo size < 100MB

---

## Phase 5: Zotero Tag Sync

### Goal
Sync Zotero tags to reflect manifest state (deferred tagging per pipeline v2).

### Steps

- [ ] Run tag sync:
  ```
  uv run python scripts/zotero_ingest.py --sync-tags
  ```
- [ ] Verify output shows all 5 new items tagged `extracted`

### Validation

- [ ] All 5 new Zotero items have `extracted` tag
- [ ] Pre-existing `PMXLGPKG` item tag unchanged or also tagged

---

## Phase 6: Research One Source

### Goal
Fully research at least one ingested source to produce DI-XXX entries in KNOWLEDGE.md, validating the complete knowledge pipeline.

### Steps

- [ ] Select one source (recommendation: Sheffield "Cost Assessment" or Entler "Approximation of the Economy" — most directly relevant to LCOE modeling)
- [ ] Run `/research` workflow against the selected source
- [ ] Ensure DI-XXX entries are created in `knowledge/KNOWLEDGE.md`
- [ ] Tag the Zotero item `researched` (manual or via API)
- [ ] Commit KNOWLEDGE.md updates

### Validation

- [ ] At least 1 source fully researched with DI-XXX entries in KNOWLEDGE.md
- [ ] Research insights are actionable for downstream modeling work (WI-006 through WI-018)

---

## Risk Management

| Risk | Impact | Mitigation |
|------|--------|------------|
| Paywalled PDFs (can't obtain all 5 targets) | Medium — delays Phase 1 | Substitution allowed per spec FR-1. Many fusion reports are publicly available from university/lab repositories. |
| Extraction timeout on large PDFs (500+ pages) | Low — ARIES reports are ~25-30 pages | Use `--no-enhance` for faster pass; process in sections if needed |
| Poor extraction quality (multi-column layouts, equations) | Medium — fusion papers have complex formatting | Phase 3 catches this; re-extract with alternative backends |
| MANIFEST.jsonl not seeded with existing source | Low — first run may re-process `PMXLGPKG` | Pipeline is idempotent; if it re-processes, just accept the manifest entry |

---

## Implementation Notes

_TO BE FILLED DURING IMPLEMENTATION_

### Phase 1 Completion
**Completed:**
**Actual sources selected:**
**Substitutions:**
**Zotero keys:**

### Phase 2 Completion
**Completed:**
**Items processed:**
**Errors:**
**MANIFEST.jsonl entries:**

### Phase 3 Completion
**Completed:**
**Quality audit results:**
| Source | Headings | Tables | Images | Overall | Notes |
|--------|----------|--------|--------|---------|-------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### Phase 4 Completion
**Completed:**
**Commit hash:**
**Repo size:**

### Phase 5 Completion
**Completed:**
**Tags synced:**

### Phase 6 Completion
**Completed:**
**Source researched:**
**DI entries created:**

---

**Status**: Draft → In Progress → Complete
