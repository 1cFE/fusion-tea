---
date: 2026-02-03T12:00:00-06:00
researcher: Claude
topic: "Knowledge Database Architecture"
tags: [research, infrastructure, knowledge-management, data-architecture]
status: complete
last_updated: 2026-02-03
---

# Research: Knowledge Database Architecture

**Date**: 2026-02-03
**Researcher**: Claude
**Research Type**: Architecture / Infrastructure

## Research Question

How should fusion-tea organize and store its three tiers of knowledge data (raw documents, extracted markdown, curated knowledge) within a git-based MBSE workflow? Should raw/extracted data live in git, external storage, or a hybrid? How does Zotero fit? What are the cross-platform (Linux + Windows) implications?

## Summary

- **Extracted markdown in git is fine**: The current corpus is ~420KB; even hundreds of 20-100KB extracted documents will stay well under GitHub's 1GB soft limit. Plain git handles text merges well.
- **Raw PDFs are the real source of truth** and must be stored durably. Many technical PDFs are not re-fetchable from URLs or DOIs (internal reports, paywalled journals, conference proceedings, emailed documents). Losing a raw PDF means losing the source.
- **Zotero + pyzotero Web API is viable for headless workflows, but requires Zotero Storage (paid)**: The Web API (api.zotero.org) works fully headless via pyzotero for metadata and tags. However, **`zot.dump()` only works with Zotero Storage, NOT with WebDAV**. The API has no access to third-party WebDAV servers. This means the headless PDF download pipeline requires a paid Zotero Storage plan ($20/yr for 2GB).
- **Zotero serves as both durable PDF store and ingestion state machine**: Items added on desktop sync to Zotero cloud. Headless VM queries API for new items, downloads PDFs (Zotero Storage only), extracts, and tags items as processed.
- **SOURCE_INDEX.md merge conflicts are manageable**: Append-only registries with clear per-entry formatting merge cleanly.
- **Symlinks are fragile cross-platform; avoid them for core data paths**: Windows symlinks require elevated privileges and behave differently. Use conventions + scripts instead.

## The Core Problem: Raw Data Durability

Not all PDFs are retrievable. Sources come from:
- Paywalled journals (access may expire or change institutions)
- Internal reports and memos (no public URL exists)
- Conference USB drives or personal communications
- Government reports on ephemeral web servers
- Scanned legacy documents

A system that assumes "we can always re-download from the DOI/URL" is fragile. **The raw PDFs themselves are irreplaceable artifacts.** The `.bib` file is metadata *about* sources -- it's useful for bibliography management, but it is not the source of truth for the data.

This means raw PDF storage must be:
1. **Durable** -- files cannot be casually lost
2. **Shared** -- all team members need access
3. **Append-only** -- new PDFs are added, existing ones are never modified
4. **Decoupled from git** -- binary files don't belong in git history

## Detailed Findings

### 1. Current State Assessment

**Repo size**: ~8MB actual content (454MB is `.venv`, 8MB is `.git`). The knowledge directory is 420KB total across 19 files. This is tiny.

**Current knowledge tiers**:

| Tier | Location | Count | Size | Format |
|------|----------|-------|------|--------|
| Raw sources | External (PyFECONS at `/home/reid/PyFECONS`) | 1 registered | N/A | Codebase |
| Extracted sources | `knowledge/sources/` | 1 file | ~20KB | Markdown |
| Research (pending) | `knowledge/research/pending/` | 0 | 0 | Markdown |
| Research (approved) | `knowledge/research/approved/` | 14 files | ~350KB | Markdown |
| Knowledge registry | `knowledge/KNOWLEDGE.md` | 14 DI-entries | ~12KB | Markdown |
| Source index | `knowledge/SOURCE_INDEX.md` | 1 source | ~2KB | Markdown |

**Observation**: The project currently has almost no extracted source documents. The approved research files are the bulk of the knowledge directory. As the project grows to ingest ARIES reports, ITER documentation, material databases, and academic papers, this will change significantly.

### 2. Git Storage: What Fits, What Doesn't

**GitHub limits**:
- Soft warning at 1GB repo size
- Hard limit: 100MB per file, 2GB per push
- PR diff limit: 20,000 lines per file, 500KB raw diff per file

**Markdown in git** (extracted documents):
- A 500-page PDF typically extracts to 50-150KB of markdown
- 100 such documents = 5-15MB -- trivially small for git
- 500 documents = 25-75MB -- still fine
- Git compresses text extremely well; delta compression works across versions
- Merges work well for line-based text (markdown is ideal)

**Binary files in git** (raw PDFs, images):
- Every version stored as a full copy (no delta compression for binaries)
- A single 10MB PDF across 3 revisions = 30MB of git history forever
- Cannot be meaningfully diffed or merged
- Images from extraction are typically small (10-500KB) and rarely change -- acceptable in git

**Recommendation**: Extracted markdown and small images belong in git. Raw PDFs do not.

### 3. Raw Document Storage Options

#### Option A: Git LFS for Raw PDFs (Recommended starting point)

**How it works**:
- Raw PDFs stored in `knowledge/raw/` directory
- Git LFS tracks `*.pdf` files, storing them on the LFS server (GitHub, GitLab, or self-hosted)
- Git repo only contains lightweight pointer files
- `git clone` fetches pointers; `git lfs pull` fetches actual PDFs on demand

**Advantages**:
- PDFs live alongside the project -- no separate system to manage
- Append-only use pattern is ideal for LFS (no re-uploading modified versions)
- Durability tied to your git hosting (GitHub, GitLab, etc.)
- Team members automatically get access via normal git permissions
- Works on Linux and Windows identically
- No additional tool beyond `git lfs install` (one-time per machine)

**Disadvantages**:
- GitHub free tier: 1GB LFS storage, 1GB/month bandwidth (paid tiers scale)
- Every team member must run `git lfs install` once
- Without LFS client installed, you get pointer files instead of actual PDFs (fails gracefully but confusingly)
- No bibliography metadata (must be tracked separately in `.bib` or SOURCE_INDEX.md)

**Why LFS works here despite earlier reservations**: The earlier assessment dismissed LFS because "PDFs are append-only, so LFS versioning provides no real benefit." But versioning isn't the point -- **the point is keeping binary files out of git's object store while still having them travel with the repo.** For append-only PDFs, LFS is low-overhead: each PDF is uploaded once and never changes.

**Sizing estimate**: 50 PDFs at average 5MB = 250MB LFS storage. Well within paid tier limits, and free tier covers the first ~200MB.

#### Option B: Cloud Bucket (S3/GCS/Azure Blob) + Manifest

**How it works**:
- Raw PDFs uploaded to a cloud bucket with stable keys
- A manifest file (`RAW_MANIFEST.yaml`) in git tracks: filename, SHA256, bucket URL, upload date
- Extraction script downloads from bucket → extracts → commits markdown

**Advantages**:
- No desktop tool dependency
- Scales to arbitrary size
- Immutable storage (append-only, versioned buckets)
- Works in CI/CD pipelines
- Cheapest per-GB of any option

**Disadvantages**:
- Requires cloud account setup and credentials management
- No bibliography metadata (must be tracked separately)
- More infrastructure to maintain
- Another system to lose access to (account expiry, credential rotation)

**When this makes sense**: If the corpus grows past 1-2GB of raw PDFs, or if you need CI/CD access to raw files.

#### Option C: Zotero + pyzotero Web API (Recommended)

**How it works**:
- Zotero desktop (on any machine with a display) manages bibliography metadata + PDF files
- PDFs sync to **Zotero Storage** (paid plans; required for API file access)
- On the headless VM, pyzotero queries the Zotero Web API (api.zotero.org) to list items and download PDF attachments -- no GUI needed
- Zotero tags and collections track processing state (new → extracted → indexed → researched)
- Better BibTeX optionally auto-exports `.bib` file on the desktop machine

```python
from pyzotero import zotero
zot = zotero.Zotero(library_id, 'user', api_key)

# List items in a collection
items = zot.collection_items('COLLECTION-KEY')

# Download a PDF attachment (ONLY works with Zotero Storage, NOT WebDAV)
for item in items:
    children = zot.children(item['key'])
    for child in children:
        if child['data'].get('contentType') == 'application/pdf':
            zot.dump(child['key'], child['data']['filename'], '/output/dir/')

# Tag as processed (works regardless of storage backend)
zot.add_tags(item, 'extracted')
```

**Advantages**:
- Durable PDF storage (Zotero Storage cloud)
- Headless PDF retrieval via Web API (pyzotero) -- no GUI on VM
- Rich metadata, annotations, browser integration (on desktop)
- Tags/collections as processing state machine
- Cross-platform (desktop: Linux/Windows/Mac; headless: any OS with Python)
- `.bib` auto-export via Better BibTeX (optional)
- Team collaboration via Zotero groups

**Disadvantages**:
- **Requires Zotero Storage (paid) for headless PDF downloads** -- the Web API cannot access files on WebDAV
- Requires at least one team member with Zotero desktop to add/curate sources
- Zotero Storage free tier is only 300MB; paid plans: 2GB/$20yr, 6GB/$60yr, unlimited/$120yr
- API key management needed
- Network dependency for PDF downloads on headless VM

**Critical: WebDAV does NOT work with the Web API**:

The Zotero Web API (api.zotero.org) **cannot serve files stored on WebDAV**. The API has no knowledge of or credentials for your third-party WebDAV server. This means:

| Capability | Zotero Storage | WebDAV |
|---|---|---|
| pyzotero `zot.dump()` (headless PDF download) | **Works** | **Does NOT work** |
| Metadata, tags, collections via API | Works | Works |
| zotero.org web library file access | Works | Does NOT work |
| Zotero desktop sync | Works | Works |
| Price | 300MB free, $20/yr 2GB, $120/yr unlimited | Free (self-hosted or services) |
| Reliability | Guaranteed compatible | Provider-dependent |

WebDAV is not "unsafe" in a security sense, but it has practical problems:
- Many free WebDAV providers have degraded or shut down (4shared ransomware, pCloud service changes)
- Zotero provides "only minimal support" for WebDAV issues
- Files stored as encoded zip archives -- direct access requires custom decoding
- Several providers recommend against extensive use of their own WebDAV

**If you want the automated headless pipeline, you must use Zotero Storage.** WebDAV only works for syncing between Zotero desktop clients.

**Verdict**: This is the strongest option for the headless pipeline, but requires a Zotero Storage plan. The 2GB/$20yr plan covers ~400 PDFs and is the recommended starting point. Metadata and tag operations (the state machine) work regardless of storage backend.

#### Option D: Convention-Based Local Storage (Simplest)

**How it works**:
- Raw PDFs stored at a conventional path (e.g., `knowledge/raw/` with `.gitignore`)
- Each user is responsible for having the PDFs locally
- SOURCE_INDEX.md entries include SHA256 checksums for verification

**Advantages**:
- Zero additional tooling
- Works immediately
- Git stays clean

**Disadvantages**:
- No automated distribution -- new team members must obtain PDFs manually
- No single durable store -- if everyone's laptop dies, PDFs are gone
- No bibliography integration

**Verdict**: Viable for solo work but doesn't scale to a team. The PDFs need to be *somewhere* durable and shared.

#### Option E: Papis (CLI-native bibliography manager)

**How it works**:
- Papis is a fully CLI-based bibliography manager (no GUI required)
- Stores each document as a folder: `info.yaml` (metadata) + PDF files
- Can import `.bib` files: `papis import --from bibtex references.bib`
- Library lives at `~/Documents/papers/` by default (configurable)

**Advantages**:
- Works fully headless (SSH-only)
- Stores PDFs in a structured, predictable directory layout
- Can import from BibTeX, DOI, arXiv
- Python-based, installable via uv
- Human-readable `info.yaml` metadata per document

**Disadvantages**:
- Smaller ecosystem than Zotero (fewer plugins, no browser integration)
- Doesn't auto-fetch PDFs as reliably as Zotero
- Library sync between machines would need rsync/scp/shared filesystem
- Less mature than Zotero

**Verdict**: Strong candidate for the headless VM side of the workflow. Could complement Zotero (desktop) or replace it entirely for CLI-oriented users.

### 4. Headless Environment Constraints

**The primary development environment is a headless Linux VM accessed via SSH.** This eliminates any tool that requires a running GUI.

**What works headless**:
- git, git-lfs -- fully CLI
- **pyzotero Web API** -- metadata, tags, collections: always work. **File downloads: only with Zotero Storage** (not WebDAV)
- Papis -- fully CLI-native
- `agentic-mbse extract` -- CLI tool
- pybtex -- BibTeX processing

**What requires GUI (unusable on headless VM)**:
- Zotero desktop application
- Zotero 7 local API (requires desktop running)
- Better BibTeX JSON-RPC (runs inside Zotero desktop)
- Zotero's "Find Available PDF" feature

**Implication**: The pipeline splits naturally: **desktop** handles source acquisition and curation (Zotero GUI), **headless VM** handles extraction and downstream processing (pyzotero + agentic-mbse). The Web API is the bridge. For cases where a PDF can't come through Zotero (e.g., scp'd directly), the pipeline also supports: raw PDF on disk → `agentic-mbse extract` → markdown in git.

### 5. Extracted Data in Git: Merge and Maintenance

**Individual source documents** (`knowledge/sources/{name}/full_document.md`):
- Append-only lifecycle (added once, rarely modified)
- No merge conflicts expected -- different sources are different files
- If re-extraction needed: replace the file entirely (git handles this cleanly)

**SOURCE_INDEX.md**:
- Currently a flat markdown file with one entry
- As sources grow, merge risk increases if multiple people add sources simultaneously
- **Mitigation strategies**:
  1. **Append-only convention**: New sources always added at the end
  2. **One entry per PR**: Each source addition is its own PR
  3. **Machine-readable format**: Consider YAML or TOML frontmatter + markdown body for easier automated merging
  4. **Split file**: If >50 sources, consider `SOURCE_INDEX/` directory with one file per source type

**KNOWLEDGE.md**:
- Same append-only pattern (DI-XXX entries added, rarely modified)
- Status field changes (`captured` → `addressed`) are the only edits
- Sequential DI-XXX numbering could conflict; use timestamps or UUIDs if parallel work is common

**Recommended SOURCE_INDEX.md evolution**:
```markdown
# Source Index
<!-- Entries sorted alphabetically by name. Add new entries in order. -->

### ARIES-AT Study
- **ID**: SRC-001
- **Type**: documentation
- **Raw**: knowledge/raw/aries_at_2000.pdf (LFS-tracked)
- **Raw SHA256**: abc123...
- **Extracted**: knowledge/sources/aries_at/
- **Extract SHA256**: def456... (of full_document.md)
- **Added**: 2026-02-03
- **BibTeX Key**: aries_at_2000 (if in bibliography.bib)
- **Use for**: ...
- **Validation**: ...
```

Both the raw file reference and the extraction output are tracked, with checksums for verification.

### 6. Symlinks, Rsync, and Cross-Platform Concerns

**Symlinks**:
- Linux: Work seamlessly
- Windows: Require Developer Mode or administrator privileges; git's `core.symlinks` setting varies
- **Verdict**: Avoid symlinks for anything in the critical path. Use them only for developer convenience with a documented fallback.

**Rsync**:
- Linux: Built-in
- Windows: Requires WSL, Cygwin, or a port
- **Verdict**: If needed, use a Python script (`shutil.copytree` or similar) for portability

**Cross-platform path conventions**:
- Use relative paths within the repo
- For external references (PyFECONS), document the expected structure and let each user configure via `.env` or local config
- agentic-mbse already uses absolute paths in SOURCE_INDEX.md (e.g., `/home/reid/PyFECONS`) -- this is inherently non-portable and should evolve to support environment variables or user-local overrides

**Recommendation**: Add a `knowledge/LOCAL_SOURCES.yaml` (gitignored) for machine-specific paths, with `SOURCE_INDEX.md` containing portable references (relative paths within repo, DOIs as supplementary info).

### 7. Proposed Directory Structure

```
knowledge/
├── SOURCE_INDEX.md              # Source registry (git-tracked)
├── KNOWLEDGE.md                 # Curated insights DI-XXX (git-tracked)
├── bibliography.bib             # BibTeX metadata, optional (git-tracked)
├── LOCAL_SOURCES.yaml           # Machine-specific paths (gitignored)
├── raw/                         # Local PDF cache (gitignored)
│   ├── .gitignore               # *.pdf -- never commit raw PDFs
│   ├── aries_at_2000.pdf        # Downloaded from Zotero API or scp'd
│   ├── iter_design_desc_2018.pdf
│   └── ...
├── sources/                     # Extracted documents (git-tracked)
│   ├── aries_at/               # One dir per source
│   │   ├── full_document.md
│   │   ├── INDEX.md
│   │   ├── summary.json
│   │   └── images/
│   ├── iter_design_desc/
│   │   ├── full_document.md
│   │   ├── INDEX.md
│   │   └── images/
│   └── ...
├── research/                    # Research pipeline (git-tracked)
│   ├── pending/
│   ├── approved/
│   └── impacts/
└── .gitkeep files as needed
```

**Key design decisions**:
- `raw/` is a **local cache** (gitignored). PDFs are downloaded from Zotero API (requires Zotero Storage) or scp'd manually. The durable copy lives in Zotero Storage.
- `sources/` is plain git (small text files, fully versioned)
- `bibliography.bib` is optional -- useful if someone maintains it via Better BibTeX, but not required for the pipeline
- `LOCAL_SOURCES.yaml` handles machine-specific paths for external sources (codebases, databases)

**Sizing estimate** (at scale):

| Content | Count | Avg Size | Total | Storage |
|---------|-------|----------|-------|---------|
| Raw PDFs | 50 | 5MB | 250MB | Zotero Storage (paid) |
| Extracted sources | 50 | 100KB | 5MB | Git |
| Source images | 500 | 50KB | 25MB | Git |
| Research reports | 50 | 30KB | 1.5MB | Git |
| bibliography.bib | 1 | 50KB | 50KB | Git |
| **Git total** | | | **~32MB** | |
| **Zotero total** | | | **~250MB** | |

Git stays small (~32MB). Zotero Storage handles binary storage. At 50 sources (~250MB), the 2GB/$20yr plan is sufficient. The 6GB/$60yr plan covers ~1,200 PDFs. Unlimited is $120/yr.

### 8. The Extraction Pipeline (Headless-Compatible)

The pipeline works entirely from a headless SSH session. Two entry points: Zotero API (primary) or direct PDF (fallback).

#### Path A: Zotero-Managed Sources (Primary)

```
Step 1: Acquire PDF (on desktop, one-time)
  - Add source to Zotero via browser plugin, DOI, or manual import
  - Attach PDF (Zotero "Find Available PDF", drag-and-drop, or manual)
  - PDF syncs to Zotero Storage (required for API file access)
  - Optionally tag with collection "Inbox" or tag "new"

Step 2: Discover new sources (on headless VM)
  # pyzotero queries Zotero Web API -- no GUI needed
  from pyzotero import zotero
  zot = zotero.Zotero(library_id, 'user', api_key)

  # Find items tagged "new" (not yet extracted)
  new_items = zot.items(tag='new')
  # Or list a specific collection
  new_items = zot.collection_items('INBOX-COLLECTION-KEY')

Step 3: Download PDF (on headless VM)
  for item in new_items:
      children = zot.children(item['key'])
      for child in children:
          if child['data'].get('contentType') == 'application/pdf':
              zot.dump(child['key'], child['data']['filename'], 'knowledge/raw/')

Step 4: Extract
  agentic-mbse extract knowledge/raw/aries_at_2000.pdf \
      --output knowledge/sources/aries_at/ \
      --index --summarize

Step 5: Update state
  # Tag item as extracted in Zotero (via API)
  zot.add_tags(item, 'extracted')
  # Register in SOURCE_INDEX.md (manual or automated)

Step 6: Commit
  git add knowledge/sources/aries_at/ knowledge/SOURCE_INDEX.md
  git commit -m "Add ARIES-AT study as source SRC-002"

Step 7: Research (later)
  /research  # Analyze the new source
  # Produces pending/ research report
  # After review, moves to approved/
  # Key findings become DI-XXX entries in KNOWLEDGE.md
  # Tag item as "researched" in Zotero
```

#### Path B: Direct PDF (Fallback)

For PDFs that aren't in Zotero (scp'd files, local-only documents):

```
Step 1: Get PDF onto VM
  scp user@desktop:~/paper.pdf knowledge/raw/

Step 2-6: Same as Path A steps 4-7
```

**Zotero as ingestion state machine**: Tags track each source through the pipeline:
- `new` → source added, not yet processed
- `extracted` → markdown exists in `knowledge/sources/`
- `indexed` → registered in SOURCE_INDEX.md
- `researched` → has approved research in `knowledge/research/approved/`

This state is queryable via pyzotero, enabling automation: a script can find all `new` items, download and extract them, then update tags -- all headless.

#### Near-Term Workflow Details

##### Adding New PDFs

**Who**: Anyone with Zotero desktop, or anyone with SSH access to the VM.

**Via Zotero (preferred)**:
1. Add the source to Zotero (browser plugin click, drag PDF in, or add by DOI/ISBN)
2. Attach the PDF if not already attached (right-click → "Find Available PDF", or drag file onto item)
3. Tag it `new` (signals: ready for extraction, not yet processed)
4. Zotero syncs metadata + PDF to Zotero Storage automatically → done

**Direct to VM (fallback, no Zotero)**:
1. `scp paper.pdf vm:fusion-tea/knowledge/raw/`
2. Extraction happens directly, skipping the Zotero pull step
3. Source won't have Zotero metadata or durable cloud backup -- consider adding to Zotero later

##### Pulling and Processing on the Headless VM

**Who**: Whoever is on the headless VM, or an automated script. Steps 1-5 below could be a single command.

**Smart pull (only new items)**:

pyzotero supports tag filtering with negation. This is the key query:

```python
from pyzotero import zotero
zot = zotero.Zotero(LIBRARY_ID, 'user', API_KEY)

# Find items tagged "new" but NOT tagged "extracted"
items = zot.everything(zot.top(tag=['new', '-extracted']))
```

This returns only items that need processing. No re-downloading of already-processed sources.

**Specific pull (named items)**:

```python
# By text search across titles/metadata
items = zot.top(q='ARIES-AT')

# By collection
items = zot.collection_items_top('FUSION-REPORTS-COLLECTION-KEY')

# By Zotero item key (if you know it)
item = zot.item('ABC12345')
```

**Version-based incremental sync** (alternative to tag-based):

```python
# Save the library version after each sync
last_version = zot.last_modified_version()

# Next time, only get items modified since then
zot.add_parameters(since=last_version)
changed_items = zot.everything(zot.top())
```

##### Full Processing Script (Reference Implementation)

```python
#!/usr/bin/env python3
"""Pull new sources from Zotero, extract, tag, and prepare for commit."""

from pyzotero import zotero
from pathlib import Path
import subprocess

# Config (could come from LOCAL_SOURCES.yaml or .env)
LIBRARY_ID = '12345'
API_KEY = 'xxxxxxxx'
RAW_DIR = Path('knowledge/raw')
SOURCES_DIR = Path('knowledge/sources')

zot = zotero.Zotero(LIBRARY_ID, 'user', API_KEY)

# Step 1: Discover new items (tagged "new", not yet "extracted")
new_items = zot.everything(zot.top(tag=['new', '-extracted']))
print(f"Found {len(new_items)} new sources to process")

for item in new_items:
    title = item['data'].get('title', 'untitled')
    item_key = item['key']

    # Step 2: Find PDF attachment
    children = zot.children(item_key)
    pdf_children = [c for c in children
                    if c['data'].get('contentType') == 'application/pdf']

    if not pdf_children:
        print(f"  SKIP {title} -- no PDF attached")
        continue

    child = pdf_children[0]
    filename = child['data']['filename']

    # Step 3: Download PDF to local cache
    RAW_DIR.mkdir(exist_ok=True)
    local_pdf = Path(zot.dump(child['key'], filename, str(RAW_DIR)))
    print(f"  Downloaded: {local_pdf}")

    # Step 4: Generate a slug for the source directory
    slug = title.lower().replace(' ', '_')[:40]  # or use item_key
    output_dir = SOURCES_DIR / slug

    # Step 5: Extract
    subprocess.run([
        'uv', 'run', 'agentic-mbse', 'extract',
        str(local_pdf),
        '--output', str(output_dir),
        '--index', '--summarize'
    ], check=True)
    print(f"  Extracted to: {output_dir}")

    # Step 6: Tag as extracted in Zotero
    zot.add_tags(item, 'extracted')
    print(f"  Tagged as extracted: {title}")

print("Done. Run 'git status' to review, then commit.")
```

##### After the Script Runs

```bash
# Review what was extracted
git status

# Stage and commit
git add knowledge/sources/ knowledge/SOURCE_INDEX.md
git commit -m "Extract 3 new sources from Zotero"
```

##### Workflow Diagram: Who Does What

```
┌─────────────────────────────────────────────────────────────────────┐
│ DESKTOP (human, Zotero GUI)                                        │
│                                                                     │
│  1. Find source (browser, colleague, conference, etc.)              │
│  2. Add to Zotero (metadata + PDF)                                  │
│  3. Tag "new"                                                       │
│  4. Zotero syncs to cloud → done                                    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                    Zotero Storage (paid, required for API)
                              │
┌─────────────────────────────────────────────────────────────────────┐
│ HEADLESS VM (human or script, pyzotero + agentic-mbse)              │
│                                                                     │
│  5. Query: zot.top(tag=['new', '-extracted'])   ← smart, only new  │
│  6. Download PDF: zot.dump(...)                 ← specific or batch │
│  7. Extract: agentic-mbse extract ...                               │
│  8. Tag "extracted": zot.add_tags(...)          ← updates state     │
│  9. Register in SOURCE_INDEX.md                                     │
│ 10. git add + commit                                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                         git push
                              │
┌─────────────────────────────────────────────────────────────────────┐
│ LATER (human + Claude, in-repo)                                     │
│                                                                     │
│ 11. /research against new source                                    │
│ 12. pending/ → approved/ → KNOWLEDGE.md (DI-XXX)                   │
│ 13. Tag "researched" in Zotero                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 9. Zotero's Role: Desktop Curator + Cloud Store + Headless API

Zotero plays three distinct roles in this architecture:

**Role 1: Desktop curator (GUI, on desktop/laptop)**
- Browser plugin captures papers with one click
- "Find Available PDF" automatically downloads from publishers
- Rich metadata editing (authors, dates, tags, notes, collections)
- Annotation and highlighting in the built-in PDF reader
- Better BibTeX auto-exports `.bib` file (optional, for git)

**Role 2: Durable PDF storage (Zotero Storage, paid)**
- PDFs sync to Zotero Storage (300MB free, paid plans from $20/yr)
- Files are durable -- survive laptop loss, disk failure, OS reinstall
- Team members share access via Zotero groups (group storage draws from owner's plan)
- **Must use Zotero Storage (not WebDAV) for API file access**

**Role 3: Headless API for the extraction pipeline (on VM)**
- pyzotero queries api.zotero.org -- no GUI needed, no Zotero install needed
- `zot.dump()` downloads PDF attachments (**Zotero Storage only** -- does not work with WebDAV)
- Tags and collections are read/writable via API, enabling state tracking (works regardless of storage backend)
- Item metadata (title, authors, DOI, date) available for SOURCE_INDEX.md generation

**What Zotero does NOT do on the headless VM**:
- Cannot run the GUI (no display)
- Cannot use "Find Available PDF" (desktop-only feature)
- Cannot use Better BibTeX JSON-RPC or local API (requires desktop running)
- **Cannot download files stored on WebDAV** (API has no access to third-party WebDAV servers)

**Why not WebDAV?** WebDAV is a valid Zotero storage backend for syncing between desktop clients, but it is invisible to the Web API. Files on WebDAV are stored as zip archives with base64-encoded filenames, cannot be accessed through the zotero.org web library, and cannot be downloaded via pyzotero. Additionally, the WebDAV provider ecosystem is declining: several free services have degraded or shut down, and Zotero provides "only minimal support" for third-party WebDAV issues. WebDAV is not "unsafe" in a security sense, but it does not support the headless pipeline this project needs.

**Papis as alternative**: For users who prefer a fully CLI-native tool and don't want Zotero at all, Papis provides local bibliography management with a structured directory layout. It can import `.bib` files and stores PDFs alongside `info.yaml` metadata. However, it lacks Zotero's cloud sync, browser integration, and team collaboration features.

### 10. Alternative: DVC for Data Versioning

**Data Version Control (DVC)** is worth mentioning as an alternative to Git LFS:
- Tracks large files via `.dvc` pointer files in git
- Supports any remote storage backend (S3, GCS, local, SSH)
- Pipeline support could automate: PDF → extract → index → commit
- More flexible than LFS for complex data workflows

**When DVC makes sense over LFS**:
- If raw PDFs need to live in cheaper cloud storage (S3 at ~$0.023/GB/month vs GitHub LFS pricing)
- If the extraction pipeline should be reproducible and tracked as a DVC pipeline
- If the project grows beyond ~100 sources with large image sets

**Current assessment**: Start with Git LFS for simplicity. Consider DVC if storage costs or pipeline reproducibility become concerns.

## Architecture Insights

The current agentic-mbse architecture has a clear philosophy:
- `full_document.md` + `INDEX.md` over physical chunking (leverages Claude's large context)
- Checksum-based freshness detection (only re-index when source changes)
- Line-range-based section retrieval (grep + offset, no embedding DB needed)
- SOURCE_INDEX.md as a human-readable registry with machine-parseable structure

This philosophy extends naturally to the knowledge database question: keep the *working data* (extracted markdown) in git where it's versioned, diffable, and directly accessible to Claude agents. Keep the *raw data* (PDFs) in Zotero Storage (durable cloud storage with headless API access). Treat bibliography metadata (`.bib`) as optional enrichment, not as the source of truth.

**The source of truth hierarchy**:
1. **Raw PDFs** (in Zotero Storage) -- the irreplaceable artifacts
2. **Extracted markdown** (in `knowledge/sources/`, git-tracked) -- the working data
3. **SOURCE_INDEX.md** -- the registry that connects raw → extracted → knowledge
4. **Zotero metadata + tags** -- processing state and bibliography info (accessible via API)
5. **bibliography.bib** -- optional export of Zotero metadata for git
6. **KNOWLEDGE.md** -- curated insights derived from research against extracted sources

## Feasibility Assessment

**Feasibility: HIGH** for the recommended approach.

- Zotero + pyzotero Web API: Mature, well-documented, works headless (with Zotero Storage)
- Extracted markdown in git: Already working, scales to hundreds of documents
- Headless extraction pipeline: `agentic-mbse extract` is CLI-native by design
- Cross-platform: Zotero desktop on Linux/Windows/Mac; pyzotero on any OS with Python
- Cost: 2GB Zotero Storage at $20/yr covers ~400 PDFs

**Risks**:
- Zotero Storage dependency for PDF retrieval on headless VM (mitigated by keeping `knowledge/raw/` as local cache)
- Recurring cost ($20-120/yr depending on plan)
- Team members must have Zotero accounts for group library access
- API rate limits on api.zotero.org (unlikely to be an issue at this scale)
- SOURCE_INDEX.md becoming stale if sources are added without registering

## Recommendations

### Immediate (No new tooling needed)

1. **Establish the `knowledge/sources/` convention**: One subdirectory per source, containing `full_document.md`, `INDEX.md`, `summary.json`, and `images/`. This is already the agentic-mbse pattern.

2. **Create `knowledge/raw/` directory** (gitignored) as a local cache for downloaded PDFs. This ensures extraction can be re-run without re-downloading.

3. **Evolve SOURCE_INDEX.md** to include Zotero item key, checksums, and extraction path per entry.

### Short-term (When document-extraction lands in agentic-mbse)

4. **Set up Zotero infrastructure**:
   - Create a Zotero account and group library for the project
   - Install Zotero desktop + Better BibTeX on at least one machine
   - Purchase Zotero Storage plan (2GB/$20yr recommended starting point; required for headless API file access)
   - Generate API key for headless access

5. **Install pyzotero on the VM**: `uv add pyzotero` and configure with API key.

6. **Define the extraction workflow** as documented in Section 8:
   - Path A (primary): Zotero API → download PDF → extract → tag → commit
   - Path B (fallback): scp PDF → extract → commit

7. **Create `knowledge/LOCAL_SOURCES.yaml`** (gitignored) for machine-specific paths to external sources (codebases, databases not in the repo).

### Medium-term (As corpus grows)

8. **Build an ingestion script** that automates Path A: query Zotero for `new` items → download → extract → tag as `extracted` → register in SOURCE_INDEX.md → commit.

9. **Consider splitting SOURCE_INDEX.md** into per-type files if it exceeds ~50 entries.

10. **Optionally export `bibliography.bib`** via Better BibTeX and commit to git. Useful for citation in documents, but not required for the pipeline.

11. **Monitor git repo size** with `git count-objects -vH`. If extracted images push past 500MB, consider Git LFS for images only.

### Things to Avoid

- **Don't treat `.bib` or URLs as the source of truth for raw data** -- many PDFs are not re-fetchable
- **Don't use WebDAV as the Zotero storage backend** if you need headless API file downloads -- the Web API cannot access WebDAV files
- **Don't access WebDAV storage directly** -- files are encoded zips with base64 filenames; no practical way to extract PDFs without Zotero client
- **Don't use symlinks** for cross-platform data paths
- **Don't store raw PDFs in git** (even with LFS -- Zotero handles durable storage better)
- **Don't use rsync** for cross-platform workflows; use Python scripts if file copying is needed

## Open Questions

1. **Zotero Storage plan sizing**: The 300MB free tier covers ~60 PDFs. The 2GB/$20yr plan covers ~400 PDFs and is the recommended starting point. If the corpus grows past 400 sources, the 6GB/$60yr or unlimited/$120yr plans are available. Group library storage draws from the group owner's plan.

2. **Extraction automation**: Should `agentic-mbse extract` automatically register the source in SOURCE_INDEX.md, or should that remain a manual step? Auto-registration reduces friction but may produce entries that need editing.

3. **Image storage threshold**: At what point do extracted images warrant Git LFS or external storage? Current images are tiny, but some technical PDFs contain many large figures.

4. **Non-PDF codebases as sources**: PyFECONS is a codebase source referenced by absolute path. As more codebase sources are added, should they be git submodules, or continue as external path references in LOCAL_SOURCES.yaml?

5. **Zotero group vs individual libraries**: A shared group library enables team-wide access and collaborative tagging. Individual libraries with API keys are simpler but don't share state. Group library is recommended for teams >1 person.

6. **Offline/air-gapped scenarios**: If the headless VM occasionally lacks network access, the `knowledge/raw/` local cache becomes important. Should we formalize a "sync all new PDFs" step that pre-downloads everything?
