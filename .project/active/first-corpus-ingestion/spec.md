# Spec: First Corpus Ingestion (KNOW-DB Item 4)

**Status:** Draft
**Owner:** Reid Westwood
**Created:** 2026-02-09 03:01 UTC
**Complexity:** LOW
**Branch:** proj-modeling-0
**Epic:** `.project/backlog/epic-knowledge-database-integration.md` — Item 4

---

## Business Goals

### Why This Matters

The fusion-tea knowledge base currently has a single extracted source (TEA D-T MFE cost analysis). The automation pipeline is proven end-to-end (Items 1-3 complete, write access confirmed), but the corpus is too thin to support downstream modeling work. Key references — ARIES design studies, fusion costing methodology, systems code documentation — are not yet available for `/research` workflows or cost model validation. Ingesting a first batch of 5 real documents validates the pipeline at modest scale and immediately provides source material for work items WI-006 through WI-018.

### Success Criteria

- [ ] 5+ real fusion sources ingested into `knowledge/sources/`
- [ ] All ingested sources registered in SOURCE_INDEX.md with full metadata
- [ ] All ingested Zotero items tagged `extracted` (via `--sync-tags` after commit)
- [ ] Extraction quality audited per source (headings, tables, images spot-checked via `/pdf-analysis`)
- [ ] At least 1 source fully researched (DI-XXX entries in KNOWLEDGE.md)
- [ ] Git repo size still manageable (`git count-objects -vH` < 100MB)
- [ ] All sources committed

### Priority

P1 — final item in the KNOW-DB epic. Unblocks research workflows and downstream modeling work.

---

## Problem Statement

### Current State

- 1 extracted source in `knowledge/sources/` (TEA D-T MFE cost analysis)
- 1 additional source (COST_MODELING.md) manually authored, not from the pipeline
- Automation pipeline complete and proven (`scripts/zotero_ingest.py`), refactored to git-authoritative manifest workflow (ingestion-workflow-v2)
- Zotero write access confirmed (API key updated 2026-02-09)
- Zotero group library (5428393) has items; pipeline auto-discovers unprocessed items by diffing against `knowledge/MANIFEST.jsonl`

### Desired Outcome

5+ real fusion reference documents ingested through the full pipeline (Zotero -> download -> extract -> register -> tag -> commit), quality-audited, and at least one fully researched to validate the complete knowledge pipeline end-to-end.

---

## Scope

### In Scope

1. **Source selection and Zotero curation** — Add 5 specific fusion documents to Zotero, attach PDFs (no manual tagging needed; manifest-based queue auto-discovers new items)
2. **Batch ingestion** — Run `scripts/zotero_ingest.py --limit 5` to process unmanifested items
3. **Quality audit** — Use `/pdf-analysis` to inspect a handful of headings, tables, and images per paper
4. **Re-extraction** — Re-run with `--enhance` on any documents with quality issues
5. **Research one source** — Run `/research` against one ingested source to produce DI-XXX entries
6. **Zotero tag sync** — After commit, run `--sync-tags` to mark processed items as `extracted` in Zotero; researched items tagged `researched`
7. **Commit** — Stage and commit all new extracted sources

### Out of Scope

- Researching all 5 sources (ongoing project work, not epic scope)
- Extraction quality fixes in `agentic-mbse` itself (file issues upstream if needed)
- SOURCE_INDEX.md splitting into per-type files
- CI/CD integration
- Ingesting more than 5-7 sources (scale-up is future work)

### Edge Cases & Considerations

- **Large PDFs (500+ pages)**: Some fusion reports are very long. The extraction pipeline has a 900s timeout. If a document exceeds this, process it in sections or use `--no-enhance` for a faster pass.
- **Paywalled sources**: All selected documents MUST be publicly available or already in the user's possession. Do not attempt to download from paywalled journals.
- **Duplicate detection**: If a selected document is already in Zotero (e.g., the Helios paper at key `7E42ICWG`), it will be auto-discovered by manifest diffing — no manual action needed. If it's already in `MANIFEST.jsonl`, it will be skipped.
- **Extraction quality variance**: Complex fusion PDFs with multi-column layouts, equation-heavy sections, or scanned tables may produce lower-quality extraction. The quality audit step catches these.
- **Repo size**: Extracted markdown + images should remain well under 100MB for 5 sources. Monitor with `git count-objects -vH`.

---

## Requirements

### Functional Requirements

> Requirements are from the epic definition and user direction unless marked [INFERRED] or [FROM INVESTIGATION].

**FR-1: Source Selection**

The following 5 fusion reference documents MUST be sourced and added to Zotero:

| # | Document | Relevance | Approximate Size |
|---|----------|-----------|-----------------|
| 1 | Najmabadi et al., "The ARIES-AT Advanced Tokamak, Advanced Technology Fusion Power Plant" (Fusion Engineering and Design, 2006) | Canonical tokamak design/cost reference; ARIES costing methodology baseline | ~30 pages |
| 2 | Najmabadi et al., "The ARIES-CS Compact Stellarator Fusion Power Plant" (Fusion Engineering and Design, 2008) | Stellarator comparison point; alternative confinement concept costing | ~25 pages |
| 3 | Sheffield et al., "A Cost Assessment of Future Electric Power Stations" (Fusion Technology, 2016) | Foundational fusion costing algorithms and methodology | ~20 pages |
| 4 | Kovari et al., "PROCESS: A Systems Code for Fusion Power Plants" (Fusion Engineering and Design, 2014-2016) | Systems-level design code documentation; parametric cost model reference | ~15 pages |
| 5 | Entler et al., "Approximation of the Economy of Fusion Energy" (Energy, 2018) | Fusion LCOE methodology; economic comparison framework | ~12 pages |

Substitutions MAY be made if a document is unavailable (paywalled without access, not in PDF form, etc.), but the replacement MUST be a publicly available fusion energy reference relevant to cost modeling or plant design.

**FR-2: Zotero Curation**

Each selected document MUST be:
1. Added to the 1cfe Zotero group library (ID 5428393) with correct bibliographic metadata
2. PDF attached as a child item (or added as a standalone attachment) and synced to Zotero Storage

Note: No manual tagging is needed. The git-authoritative pipeline auto-discovers items not yet in `knowledge/MANIFEST.jsonl`.

**FR-3: Batch Ingestion**

Run `uv run python scripts/zotero_ingest.py --limit 5` to process unmanifested items. The script MUST:
- Determine pending items by diffing the Zotero library against `knowledge/MANIFEST.jsonl`
- Download PDFs to `knowledge/raw/`
- Extract each to `knowledge/sources/<slug>/` with `--enhance` (default)
- Append entries to `knowledge/SOURCE_INDEX.md` with full extended metadata
- Append entries to `knowledge/MANIFEST.jsonl` upon successful extraction

Note: Zotero `extracted` tagging is deferred — run `--sync-tags` after committing (see FR-6).

**FR-4: Quality Audit**

After extraction, each source MUST be audited for extraction quality using the `/pdf-analysis` skill. The audit MUST inspect:
- **Headings**: A sample of 3-5 section headings per document — verify correct hierarchy (H1/H2/H3) and no garbled text
- **Tables**: A sample of 2-3 tables per document (if present) — verify structure preserved (rows/columns intact, no merged-cell corruption)
- **Images**: A sample of 2-3 images per document (if present) — verify image files exist in `images/` and references in markdown are correct

Quality issues MUST be documented. Documents with significant quality problems SHOULD be re-extracted with `--enhance --force` or with alternative flags (e.g., `--backend docling`, `--no-tables`).

**FR-5: Research One Source**

At least one ingested source MUST be fully researched using the `/research` workflow:
- Source selection is implementer's choice
- Research MUST produce DI-XXX entries in `knowledge/KNOWLEDGE.md`
- The Zotero item SHOULD be tagged `researched` after completion

**FR-6: Commit, Tag Sync, and Size Check**

All extracted sources, SOURCE_INDEX.md updates, MANIFEST.jsonl updates, and KNOWLEDGE.md updates MUST be committed to git. After committing:
1. Run `uv run python scripts/zotero_ingest.py --sync-tags` to tag all manifested items as `extracted` in Zotero
2. Run `git count-objects -vH` and verify total repo size remains under 100MB

---

## Acceptance Criteria

### Core Functionality

- [ ] 5+ source directories exist under `knowledge/sources/` (in addition to existing sources)
- [ ] Each new source directory contains at minimum `full_document.md` and `INDEX.md`
- [ ] SOURCE_INDEX.md has 6+ entries total (1 existing + 5 new), each with Zotero key, checksums, extraction path
- [ ] MANIFEST.jsonl has 6+ entries total (1 seed + 5 new)
- [ ] All 5 new Zotero items are tagged `extracted` (via `--sync-tags` after commit)
- [ ] Quality audit notes recorded for each source (pass/fail per heading/table/image check)
- [ ] At least 1 source has been `/research`-ed with DI-XXX entries in KNOWLEDGE.md
- [ ] `git count-objects -vH` shows repo size < 100MB

### Quality & Integration

- [ ] No PDF files committed to git (`knowledge/raw/.gitignore` intact)
- [ ] No secrets committed to git
- [ ] Extraction used `--enhance` by default
- [ ] Quality issues (if any) documented with recommended remediation
- [ ] `--sync-tags` run after commit to sync Zotero tags to manifest state

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-knowledge-database-integration.md`
- **Pipeline V2 Spec:** `.project/active/ingestion-workflow-v2/spec.md`
- **Pipeline V2 Design:** `.project/active/ingestion-workflow-v2/design.md`
- **Item 3 Spec:** `.project/active/zotero-ingestion-script/spec.md`
- **Automation Script:** `scripts/zotero_ingest.py` (refactored to git-authoritative manifest workflow)
- **Shared Library:** `scripts/zotero_lib.py`
- **Manifest:** `knowledge/MANIFEST.jsonl`
- **Write Access Test:** `scripts/test_zotero_write_access.py` (confirmed 2026-02-09)
- **SOURCE_INDEX.md:** `knowledge/SOURCE_INDEX.md`
- **KNOWLEDGE.md:** `knowledge/KNOWLEDGE.md`
- **Design:** `.project/active/first-corpus-ingestion/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`
