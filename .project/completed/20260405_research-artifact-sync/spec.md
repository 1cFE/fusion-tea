# Spec: Research Artifact Sync (R2 + rclone)

**Status**: draft
**Owner**: reid
**Created**: 2026-04-03
**Complexity**: medium
**Branch**: design-space-explore

## Problem Statement

Phase 1a concept research produced ~149 MB of artifacts across 38+ fusion concepts in `exploration/phase_1a/research/`. These include:

- **918 extracted images** (PNGs, ~15 MB) — equations, tables, figures from PDFs
- **90 raw HTML snapshots** (~24 MB) — web source captures
- **11 raw PDFs** (~21 MB) — downloaded source documents
- **Markdown outputs** (~89 MB) — processed text, dossiers, prompts (fine in git)

The binary artifacts (HTML, PDF, PNG) are currently committed to git, causing GitHub pushes to fail at ~56 MB pack size. The concept analysis pipeline (`run_analysis.py`) reads these sources via hardcoded paths into `exploration/phase_1a/research/`. We need to:

1. Promote this research to a more accessible, canonical location at `knowledge/concept_research/`
2. Sync binary artifacts via Cloudflare R2 so they're `.gitignored` but team-accessible
3. Keep markdown content in git (it's the primary research output)
4. Update the concept analysis pipeline to find sources at the new location
5. Index the research collection for discoverability by other agents and workflows

## Scope

### In Scope

1. **New directory structure**: `knowledge/concept_research/{concept-id}/` mirroring the per-concept research layout
2. **R2 sync configuration**: rclone remote setup using existing `1cfe-research` bucket, sync scripts, credential management
3. **Selective gitignore**: Binary artifacts (*.pdf, *.html, *.png) ignored; markdown (*.md) and JSON (*.json) tracked
4. **Pipeline path update**: Modify `run_analysis.py` to resolve sources from the new location
5. **Migration script**: Move existing Phase 1a research to the new structure
6. **Symlink for transition**: `exploration/phase_1a/research/` → `knowledge/concept_research/`
7. **Source indexing**: Umbrella entry in top-level `SOURCE_INDEX.md` + detailed inner `SOURCE_INDEX.md` inside `concept_research/`
8. **Developer onboarding**: Setup instructions for new team members

### Out of Scope

- Migrating `knowledge/sources/` (the existing Zotero-ingested sources) — those stay as-is
- Changing the Phase 1a research pipeline (`run_concept.py`) — that workflow is complete
- R2 bucket versioning configuration (can be added later)
- Automated CI/CD sync (manual sync is sufficient for 2-5 researchers)
- Bulk-updating embedded paths in 177 saved prompt/analysis files under `exploration/concept_analysis/analyses/` — these are historical audit trail artifacts, not live inputs

## Requirements

### R1: Directory Structure

Migrate `exploration/phase_1a/research/` to `knowledge/concept_research/` as the canonical home for per-concept research:

```
knowledge/concept_research/
├── SOURCE_INDEX.md                    # Detailed per-concept source index (R7)
├── README.md                          # Documents the structure and sync process
├── {concept-id}/                      # e.g., 01-hts-compact-tokamak/
│   ├── dossier.md                     # Consolidated research findings (git-tracked)
│   ├── changelog.md                   # Iteration history (git-tracked)
│   ├── iter-01/
│   │   ├── prompt.md                  # Research prompt (git-tracked)
│   │   ├── output.md                  # Claude output (git-tracked)
│   │   ├── synthesis_prompt.md        # Synthesis prompt (git-tracked)
│   │   └── sources/
│   │       ├── {source-name}.md       # Processed extraction (git-tracked)
│   │       ├── {source-name}.orig.md  # Original extraction (git-tracked)
│   │       ├── {source-name}/         # Source artifact directory
│   │       │   ├── output.md          # Extracted text (git-tracked)
│   │       │   ├── metrics.json       # Extraction metrics (git-tracked)
│   │       │   ├── raw.html           # Original HTML snapshot (R2-synced, gitignored)
│   │       │   ├── raw.pdf            # Original PDF (R2-synced, gitignored)
│   │       │   └── images/            # Extracted figures (R2-synced, gitignored)
│   │       │       ├── page_001_fig_0.png
│   │       │       └── ...
│   │       └── ...
│   ├── iter-02/
│   │   └── ...
│   └── iter-N/
└── ...
```

**Key principle**: The directory structure is identical to the existing Phase 1a layout. This is a relocation, not a restructuring.

**Acceptance criteria**:
- All 38+ concept directories exist under `knowledge/concept_research/`
- Directory tree mirrors `exploration/phase_1a/research/` exactly
- README.md documents the structure and sync process

### R2: Selective Gitignore

Binary artifacts within `concept_research/` must be gitignored while markdown and JSON remain tracked.

**Gitignore rules** (in `knowledge/concept_research/.gitignore`):
```gitignore
# Binary artifacts — synced via R2, not git
*.pdf
*.html
*.png
*.jpg
*.jpeg
*.gif
*.svg
```

**Acceptance criteria**:
- `git status` shows no binary artifacts after migration
- All `.md` and `.json` files are tracked
- Old gitignore patterns for `exploration/phase_1a/research/` are removed (the symlink + new `.gitignore` handles it)

### R3: R2 Sync Configuration

Provide tooling for syncing binary artifacts between local and the existing `1cfe-research` R2 bucket.

**Components**:
- `scripts/sync_research.sh` — wrapper around rclone for push/pull operations
- `.env.example` updated with R2 credential placeholders (or rclone config instructions)
- rclone config template or setup instructions in README

**Sync script interface**:
```bash
# Pull all binary artifacts from R2 to local
./scripts/sync_research.sh pull

# Push local binary artifacts to R2
./scripts/sync_research.sh push

# Dry-run (show what would be transferred)
./scripts/sync_research.sh pull --dry-run

# Sync specific concept only
./scripts/sync_research.sh pull 01-hts-compact-tokamak
```

**R2 bucket layout** (mirrors local structure):
```
1cfe-research/
└── concept_research/
    └── {concept-id}/
        └── iter-NN/
            └── sources/
                └── {source-name}/
                    ├── raw.html
                    ├── raw.pdf
                    └── images/
                        └── *.png
```

**Acceptance criteria**:
- `sync_research.sh pull` populates all binary artifacts at correct relative paths
- `sync_research.sh push` uploads local binary artifacts to R2
- Dry-run mode shows transfers without executing
- Concept-specific sync works for incremental updates
- Script validates rclone is installed and R2 remote is configured before running
- Script reports transfer summary (files synced, total size)

### R4: Pipeline Path Update

Update `exploration/concept_analysis/scripts/run_analysis.py` to resolve research sources from the new location.

**Current paths** (in `run_analysis.py`):
```python
PHASE_1A_DIR = CONCEPT_ANALYSIS_DIR.parent / "phase_1a"
SCHEMA_PATH = PHASE_1A_DIR / "schema.md"
RESEARCH_DIR = PHASE_1A_DIR / "research"
```

**New paths**:
```python
# Research directory: canonical location
REPO_ROOT = Path(__file__).resolve().parents[3]
RESEARCH_DIR = REPO_ROOT / "knowledge" / "concept_research"

# schema.md stays in phase_1a (not part of the research migration)
PHASE_1A_DIR = CONCEPT_ANALYSIS_DIR.parent / "phase_1a"
SCHEMA_PATH = PHASE_1A_DIR / "schema.md"
```

**Note**: `schema.md` remains at `exploration/phase_1a/schema.md` — it is not part of the research data and is not migrated. `PHASE_1A_DIR` is retained solely for this reference.

**Functions affected**:
- `find_sources()` (line 617) — scans `iter-*/sources/*.md`
- `find_latest_sources_dir()` (line 703) — finds/creates latest iteration
- `get_dossier_path()` (line 755) — resolves `dossier.md`
- Any function using `RESEARCH_DIR`

**Acceptance criteria**:
- `run_analysis.py list` works identically before and after
- `run_analysis.py status` shows the same state for all 38 concepts
- `run_analysis.py gap-check 01 --dry-run` generates the same prompt content
- The symlink at `exploration/phase_1a/research/` means the old path also resolves correctly during transition
- No changes to the concept analysis output directory (`analyses/`)

### R5: Migration Script

One-time script to move existing Phase 1a research to the new location.

**Script**: `scripts/migrate_research.sh` (or Python)

**Behavior**:
1. Copy (not move) all content from `exploration/phase_1a/research/` to `knowledge/concept_research/`
2. Verify file counts match between source and destination
3. Report which binary files will be gitignored vs tracked
4. Replace `exploration/phase_1a/research/` with a symlink to `knowledge/concept_research/`
5. Do NOT delete the original data until copy + symlink are verified

**Acceptance criteria**:
- All 38+ concept directories are copied with full structure preserved
- File counts match between source and destination
- Symlink `exploration/phase_1a/research/` → `../../knowledge/concept_research/` is created and resolves correctly
- Script is idempotent (safe to re-run)

### R6: Initial R2 Upload

After migration, push all binary artifacts to R2 as the initial seed.

**Acceptance criteria**:
- All binary artifacts are uploaded to `1cfe-research` bucket
- `sync_research.sh pull` into an empty `concept_research/` directory reproduces all binary files
- Round-trip verified: push → delete local → pull → diff shows no differences

### R7: Source Indexing

Create two levels of source indexing for discoverability:

**A. Top-level `knowledge/SOURCE_INDEX.md`** — one umbrella entry:

```markdown
### Concept Research Dossiers
- **Type**: research collection
- **Location**: knowledge/concept_research/
- **Use for**: Per-concept techno-economic research across 38+ fusion concepts.
  Contains dossiers, source extractions, iteration history, and per-concept
  source materials. See `knowledge/concept_research/SOURCE_INDEX.md` for the
  detailed per-concept source listing. Serves all RQs.
```

**B. Inner `knowledge/concept_research/SOURCE_INDEX.md`** — detailed per-concept index:

Lists each concept with its available sources, iteration count, and source types, so agents can find "where's the stellarator research?" without traversing nested directories. Format TBD during implementation, but should include at minimum:
- Concept ID and name
- Number of research iterations
- List of source names per iteration (with type: HTML, PDF, etc.)
- Path to dossier

**Acceptance criteria**:
- Top-level SOURCE_INDEX.md has the umbrella entry
- Inner SOURCE_INDEX.md lists all 38+ concepts with their sources
- An agent reading the inner index can locate any concept's dossier or specific source extraction without directory traversal

### R8: Developer Onboarding

Update `.env.example` and add setup instructions so new team members can get started.

**Acceptance criteria**:
- `.env.example` includes R2 credential placeholders
- `knowledge/concept_research/README.md` documents:
  - What this directory contains
  - How to install rclone
  - How to configure the R2 remote
  - How to sync artifacts
  - What's in git vs what needs syncing

## Design Constraints

### DC1: No Restructuring
The per-concept directory layout (`{concept-id}/iter-NN/sources/{source-name}/`) must be preserved exactly. This is a relocation, not a redesign. The analysis pipeline depends on this structure.

### DC2: Markdown Stays in Git
All `.md` and `.json` files must remain git-tracked. Only binary artifacts (PDF, HTML, PNG/image files) go to R2. This ensures dossiers, prompts, and analysis outputs are always available without syncing.

### DC3: Relative Paths Must Work
Processed markdown files reference images by relative path (e.g., `images/page_001_fig_0.png`). After R2 sync, these paths must resolve correctly. This is guaranteed by preserving directory structure in both git and R2.

### DC4: No Mandatory Sync
The analysis pipeline must work without binary artifacts present. The pipeline only reads `.md` files from `iter-*/sources/` — it never reads raw PDFs, HTML, or images directly. Missing binary artifacts should not block `run_analysis.py`.

### DC5: Single Source of Truth
After migration, `knowledge/concept_research/` is the canonical location. `exploration/phase_1a/research/` becomes a symlink to the canonical location, preserving backward compatibility for existing scripts and embedded paths.

## Success Criteria

- [ ] `knowledge/concept_research/` contains all 38+ concept research directories
- [ ] Binary artifacts are gitignored and sync via `./scripts/sync_research.sh pull/push`
- [ ] `run_analysis.py status` shows identical state before and after migration
- [ ] `run_analysis.py gap-check 01 --dry-run` generates correct prompts from new location
- [ ] `exploration/phase_1a/research/` symlink resolves to `knowledge/concept_research/`
- [ ] A fresh clone + `sync_research.sh pull` gives a fully functional research environment
- [ ] Top-level SOURCE_INDEX.md has umbrella entry for concept research
- [ ] Inner SOURCE_INDEX.md maps all 38+ concepts and their sources
- [ ] `.env.example` and README document the setup process
