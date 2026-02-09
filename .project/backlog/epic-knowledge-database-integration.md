# Epic: Knowledge Database Integration (Zotero + Extraction Pipeline)

**Epic ID**: KNOW-DB
**Status**: In Progress
**Priority**: P1
**Created**: 2026-02-06
**Estimated Effort**: 4-5 days

---

## Executive Summary

Establish a durable, repeatable pipeline for ingesting domain reference documents (PDFs, technical reports, standards) into the fusion-tea knowledge base. Uses Zotero as the durable PDF store and metadata manager, pyzotero for headless API access, and `agentic-mbse extract` for conversion to structured markdown. This epic de-risks the architecture first with a single end-to-end proof, then builds automation for batch ingestion.

**Critical Success Factor**: A single CLI command can pull new sources from Zotero, extract them to structured markdown, register them in SOURCE_INDEX.md, and prepare a git commit — all headless.

---

## Why This Epic?

**Current State**:
- Knowledge directory has 1 extracted source (COST_MODELING.md, manually written)
- No raw PDF storage strategy — PDFs exist ad-hoc on local machines
- SOURCE_INDEX.md has 1 entry (PyFECONS codebase) with no checksums or extraction metadata
- No pipeline to go from "found a paper" to "indexed and searchable in the project"
- `agentic-mbse extract` merged (PR #3, commit b9f8dbe) with 4-layer pipeline, not yet used in fusion-tea
- Zotero account exists but is not yet configured for the project

**Future State**:
- Zotero Storage holds all raw PDFs durably (survives laptop loss, shareable)
- Headless VM can pull new PDFs via pyzotero API and extract them automatically
- `knowledge/sources/` contains structured markdown for all ingested documents
- SOURCE_INDEX.md tracks every source with Zotero key, checksums, and extraction path
- Zotero tags track processing state (new → extracted → indexed → researched)
- Adding a new source is: "add to Zotero, tag `new`, run the pull script"

---

## Background

### Research

| Document | Key Findings |
|----------|--------------|
| [20260203-knowledge-database-architecture.md](../research/20260203-knowledge-database-architecture.md) | Zotero Storage + pyzotero Web API is the recommended architecture. WebDAV does NOT work for headless PDF downloads. Extracted markdown in git scales to hundreds of documents. Raw PDFs must NOT go in git. |

### Key Technical Decisions (from research)

1. **Raw PDFs**: Stored in Zotero Storage (paid, $20/yr for 2GB). Local cache in `knowledge/raw/` (gitignored).
2. **Extracted markdown**: In `knowledge/sources/` (git-tracked). One subdirectory per source.
3. **Extraction tool**: `agentic-mbse extract` (PDF/DOCX → full_document.md + INDEX.md + images/).
4. **Headless API**: pyzotero queries api.zotero.org. `zot.dump()` downloads PDFs. Tags track state.
5. **No symlinks, no rsync**: Cross-platform safety. Python scripts for portability.

### External Dependency

The `agentic-mbse extract` command was merged in PR #3 (commit `b9f8dbed`, 2026-02-08). It provides a **4-layer extraction pipeline**:

- **Layer 1 — Base extraction**: PyMuPDF4LLM (default), Docling, or Pandoc backends with automatic fallback
- **Layer 2 — GMFT table extraction**: Detects broken pipe tables and re-extracts from PDF using GMFT (optional dep: `gmft>=0.3`)
- **Layer 3 — Claude structural repair**: AI-powered heading detection and document structure repair (`--enhance` or `--structure-only`)
- **Layer 4 — AI quality repair**: Cross-validated repair of equations, tables, and structure issues (`--enhance` only)

Key CLI flags:
- `--index` — Generate INDEX.md after extraction
- `--summarize` — Include AI summaries in INDEX.md (requires `--index`)
- `--enhance` — Enable Layers 3+4 (structural repair + quality repair)
- `--structure-only` — Enable Layer 3 only (structural repair, skip quality repair)
- `--no-tables` — Skip Layer 2 GMFT table extraction
- `--model {opus,sonnet,haiku}` — Override Claude model for structural repair
- `--max-repair-pages N` — Limit Layer 4 repair scope
- `--backend {docling,pymupdf,pandoc}` — Force a specific backend

Output structure: `full_document.md`, `INDEX.md`, `summary.json`, `images/`

Optional dependencies for best quality:
- `gmft>=0.3` — Layer 2 table extraction (`uv add gmft` or `uv add agentic-mbse[extract-tables]`)
- `docling>=2.0` — Alternative extraction backend (`uv add agentic-mbse[extract-full]`)

---

## Success Criteria

- [x] pyzotero can connect to Zotero Web API and download a PDF attachment on the headless VM
- [x] At least one real fusion document fully ingested: Zotero → download → extract → SOURCE_INDEX.md → git
- [x] SOURCE_INDEX.md format evolved to include Zotero item key, checksums, and extraction paths
- [x] `knowledge/raw/` directory exists and is properly gitignored
- [x] Automation script can batch-process all `new`-tagged Zotero items in one command
- [ ] 5+ real fusion sources ingested and committed to `knowledge/sources/`
- [ ] At least one ingested source has been researched via `/research` and produced DI-XXX entries

---

## Backlog Items

### Item 1: Zotero API De-Risk [0.5 day]

**Type**: Integration

**Objective**: Prove that pyzotero can connect to the Zotero Web API, query items, and download a PDF from Zotero Storage on the headless VM.

**Current State**:
- ✅ Zotero account exists
- ❓ Zotero Storage plan status (300MB free tier vs paid — need to verify)
- ❌ No pyzotero installed in fusion-tea
- ❌ No API key generated
- ❌ No proof that headless PDF download works

**Scope**:
1. **Zotero Storage verification**: Confirm Zotero Storage is active (not WebDAV). Purchase 2GB plan if needed ($20/yr).
2. **API key generation**: Generate a Zotero API key with read/write access.
3. **pyzotero installation**: `uv add pyzotero` in fusion-tea.
4. **Connectivity test**: Write a small script that connects, lists library items, and verifies metadata access.
5. **PDF download test**: Add a test PDF to Zotero (any document), sync to Storage, then download via `zot.dump()` on the VM.
6. **Credential storage**: Store library ID and API key in a gitignored config file (`.env` or `knowledge/LOCAL_SOURCES.yaml`).

**Out of Scope**:
- Full directory structure setup (Item 2)
- Real fusion document extraction (Item 2)
- Automation scripting (Item 3)
- Collections/tagging conventions beyond a basic test

**Success Criteria**:
- [x] `uv add pyzotero` succeeds and pyzotero is in `pyproject.toml`
- [x] A Python script on the headless VM connects to Zotero API and lists items
- [x] `zot.dump()` successfully downloads a PDF attachment to a local directory
- [x] API key is stored in a gitignored location
- [x] De-risk verdict documented: **PASSED** — Zotero Storage + pyzotero works for headless pipeline

**Deliverables**:
- `scripts/zotero_test.py` — proof-of-concept connectivity + download script
- `.env` or `knowledge/LOCAL_SOURCES.yaml` — credential template (gitignored)
- Brief de-risk report (can be inline in this epic or a short note)

**Dependencies**: None (first item)

---

### Item 2: Single-Source End-to-End Pipeline [1 day]

**Type**: Integration

**Objective**: Ingest one real fusion reference document through the complete pipeline: Zotero → pyzotero download → `agentic-mbse extract` → register in SOURCE_INDEX.md → git commit. Proves the full architecture works.

**Current State**:
- ✅ `agentic-mbse extract` available (PR #3 merged, commit b9f8dbe — 4-layer pipeline)
- ✅ Zotero API connectivity proven (Item 1)
- ✅ `knowledge/raw/` directory exists with `.gitignore` excluding `*.pdf`
- ✅ `knowledge/sources/tea_dt_mfe_cost_analysis/` extracted (full_document.md, INDEX.md, summary.json, images/)
- ✅ SOURCE_INDEX.md has extended metadata format (Zotero key, checksums, extraction path)

**Scope**:
1. **Directory setup**:
   - Create `knowledge/raw/` with `.gitignore` (exclude `*.pdf`)
   - Create `knowledge/LOCAL_SOURCES.yaml` template (gitignored) for machine-specific paths
2. **Source acquisition**: Add one real fusion document to Zotero desktop (e.g., an ARIES study, publicly available). Tag it `new`.
3. **Headless download**: Use pyzotero to find the `new`-tagged item and download the PDF to `knowledge/raw/`.
4. **Extraction**: Run `uv run agentic-mbse extract knowledge/raw/<document>.pdf --output knowledge/sources/<slug>/ --index --summarize --enhance`.
   - `--enhance` enables Layer 3 (structural repair) + Layer 4 (AI quality repair) for best results on complex fusion PDFs.
   - If `gmft` is installed, Layer 2 table extraction runs automatically. Skip with `--no-tables` if not needed.
5. **SOURCE_INDEX.md evolution**: Update the format to include:
   - Zotero item key
   - Raw file SHA256
   - Extracted path
   - Extract SHA256 (of full_document.md)
   - Date added
   - Use-for and validation notes
   - *(SRC-XXX source ID system deferred — no toolchain support exists)*
6. **Zotero state update**: Tag the item as `extracted` via API.
7. **Commit**: Stage extracted output + SOURCE_INDEX.md update.

**Out of Scope**:
- Batch processing (Item 3)
- Multiple sources (Item 4)
- Splitting SOURCE_INDEX.md into per-type files (medium-term concern)

**Success Criteria**:
- [x] `knowledge/raw/` exists with `.gitignore` excluding PDFs
- [x] `knowledge/LOCAL_SOURCES.yaml` template exists (gitignored)
- [x] One real fusion PDF downloaded from Zotero Storage to `knowledge/raw/`
- [x] `agentic-mbse extract` produces `full_document.md`, `INDEX.md`, `summary.json`, and `images/` in `knowledge/sources/<slug>/`
- [x] SOURCE_INDEX.md has a new entry with Zotero key, checksums, and extraction path
- [x] Zotero item is tagged `extracted` *(resolved: API key updated with write access, verified 2026-02-09)*
- [x] All extracted content committed to git

**Deliverables**:
- `knowledge/raw/.gitignore`
- `knowledge/LOCAL_SOURCES.yaml` (template, gitignored)
- `knowledge/sources/<first-source>/` (full_document.md, INDEX.md, images/)
- Updated `knowledge/SOURCE_INDEX.md` with evolved format
- Git commit with the first extracted source

**Dependencies**: Item 1

---

### Item 3: Ingestion Automation Script [1-1.5 days]

**Type**: Implementation

**Objective**: Build an automation script that batch-processes all `new`-tagged Zotero items: download PDFs, extract to markdown, tag as processed, and register in SOURCE_INDEX.md.

**Current State**:
- ✅ Single-source pipeline proven end-to-end (Item 2)
- ✅ SOURCE_INDEX.md format established (Item 2)
- ✅ Reference implementation exists in research report (Section 8)
- ✅ Automation script implemented (`scripts/zotero_ingest.py`)

**Scope**:
1. **Smart pull**: Query Zotero for items tagged `new` but not `extracted` (`zot.top(tag=['new', '-extracted'])`)
2. **PDF download**: Download each item's PDF attachment to `knowledge/raw/`
3. **Slug generation**: Generate a clean directory name from the item title
4. **Extraction**: Run `agentic-mbse extract --index --summarize --enhance` for each downloaded PDF
5. **SOURCE_INDEX.md registration**: Auto-append new entries with Zotero metadata, checksums, extraction paths
6. **Zotero state update**: Tag each processed item as `extracted`
7. **Error handling**:
   - Skip items with no PDF attachment (log warning)
   - Handle extraction failures gracefully (log, don't tag as extracted)
   - Handle duplicate slugs (append Zotero key suffix)
8. **Direct-PDF fallback path**: Support `--local-pdf <path>` for PDFs not in Zotero (scp'd files)
9. **Dry-run mode**: `--dry-run` to list what would be processed without doing it

**Out of Scope**:
- CI/CD integration
- Automatic `/research` invocation
- Version-based incremental sync (tag-based is sufficient for now)
- SOURCE_INDEX.md splitting (future concern)

**Success Criteria**:
- [x] `uv run python scripts/zotero_ingest.py` processes all `new`-tagged items
- [x] Each processed item gets: PDF downloaded, markdown extracted, SOURCE_INDEX.md entry, Zotero tag updated
- [x] `--dry-run` lists items without modifying anything
- [x] `--local-pdf <path>` extracts a PDF not managed by Zotero
- [x] Items with no PDF attachment are skipped with a warning
- [x] Extraction failures are logged and the item is NOT tagged as extracted
- [x] Script output summarizes: N items found, N extracted, N skipped, N failed

**Deliverables**:
- `scripts/zotero_ingest.py` — the automation script
- Updated `scripts/zotero_test.py` or removal if superseded
- Brief usage documentation in script docstring

**Dependencies**: Item 2

---

### Item 4: First Corpus Ingestion [1 day]

**Type**: Execution

**Objective**: Use the automation pipeline to ingest 5-10 real fusion reference documents, validating the system at modest scale and producing immediately useful knowledge for the project.

**Current State**:
- ✅ Automation script works (Item 3)
- ✅ One source already ingested (Item 2)
- ❌ Only 1 extracted source in the project
- ❌ Many key references (ARIES studies, ITER docs, material databases) not yet available

**Scope**:
1. **Source selection**: Identify 5-10 high-value fusion documents for initial corpus. Candidates:
   - ARIES-AT study (tokamak cost/design reference)
   - ARIES-CS study (stellarator comparison)
   - ITER Plant Description Document sections
   - Fusion power plant costing studies
   - Material property references for fusion-relevant materials
2. **Zotero curation**: Add selected documents to Zotero desktop, attach PDFs, tag `new`
3. **Batch ingestion**: Run `scripts/zotero_ingest.py` to process all new items
4. **Quality review**: Spot-check extracted markdown for quality (tables, images, section structure). Re-run with `--enhance --force` on any documents with quality issues.
5. **Research one source**: Run `/research` against at least one ingested source to validate the full knowledge pipeline (extraction → research → KNOWLEDGE.md DI-XXX entries)
6. **Tag researched items**: Update Zotero tags for any sources that complete the research step
7. **Commit**: Stage and commit all new extracted sources

**Out of Scope**:
- Researching all 5-10 sources (that's ongoing project work, not epic scope)
- Extraction quality fixes (file issues against agentic-mbse if needed)
- SOURCE_INDEX.md splitting

**Success Criteria**:
- [ ] 5+ real fusion sources ingested into `knowledge/sources/`
- [ ] All ingested sources registered in SOURCE_INDEX.md with full metadata
- [ ] All ingested Zotero items tagged `extracted`
- [ ] Extraction quality spot-checked (no garbled tables, images referenced correctly)
- [ ] At least 1 source fully researched (pending → approved, DI-XXX entries in KNOWLEDGE.md)
- [ ] Git repo size still manageable (`git count-objects -vH` < 100MB)
- [ ] All sources committed

**Deliverables**:
- `knowledge/sources/<5+ source directories>/` — extracted documents
- Updated `knowledge/SOURCE_INDEX.md` — 6+ entries (including the Item 2 source)
- Updated `knowledge/KNOWLEDGE.md` — new DI-XXX entries from researched source(s)
- Quality notes on any extraction issues encountered

**Dependencies**: Item 3

---

## Dependencies

**External**:
- Zotero Storage plan (paid, $20/yr for 2GB) — required for headless PDF download
- `agentic-mbse` with document extraction (PR #3 merged, commit b9f8dbe) — installed as editable dep, auto-updates
- Optional: `gmft>=0.3` for Layer 2 table extraction quality; `docling>=2.0` for alternative backend
- Network access from headless VM to api.zotero.org

**Internal**:
- No blocking dependencies on other epics (this is infrastructure, not modeling)
- Once complete, this enables richer source data for modeling work items (WI-006 through WI-018)

**Item Dependency Graph**:
```
Item 1: Zotero API De-Risk (no dependencies)
  └─> Item 2: Single-Source End-to-End Pipeline (depends on Item 1)
        └─> Item 3: Ingestion Automation Script (depends on Item 2)
              └─> Item 4: First Corpus Ingestion (depends on Item 3)
```

Note: Items are strictly sequential. Each validates assumptions needed by the next.

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Zotero Storage not activated or using WebDAV | High — blocks entire headless pipeline | Item 1 explicitly verifies this before proceeding. WebDAV does NOT work for API downloads. |
| `agentic-mbse extract` quality issues on real fusion PDFs | Medium — garbled tables, missing images | Item 2 validates with a real document. File issues upstream if needed. 4-layer pipeline with `--enhance` provides structural repair + AI quality repair. GMFT table extraction available if `gmft` is installed. |
| Zotero API rate limits | Low — unlikely at this scale | pyzotero handles rate limiting. Batch sizes will be <20 items. |
| Large PDFs exhaust extraction memory | Medium — some fusion reports are 500+ pages | `agentic-mbse extract` has configurable timeout + fallback. Can process in sections if needed. |
| Recurring cost sensitivity ($20-120/yr) | Low — small relative to project value | Start with 2GB/$20yr. Monitor usage. Can downgrade to local-only fallback (Path B) if needed. |

---

## Timeline

**Total Effort**: ~4 days (sequential, each item gates the next)

| Item | Effort | Dependencies |
|------|--------|--------------|
| Item 1: Zotero API De-Risk | 0.5 day | None |
| Item 2: Single-Source E2E Pipeline | 1 day | Item 1 |
| Item 3: Ingestion Automation Script | 1-1.5 days | Item 2 |
| Item 4: First Corpus Ingestion | 1 day | Item 3 |

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete*

**What Went Well**:
- TBD

**What Could Improve**:
- TBD

**Surprises**:
- TBD

---

**Last Updated**: 2026-02-09
**Next Action**: Begin Item 4 (First Corpus Ingestion) — Items 1, 2, and 3 are complete
