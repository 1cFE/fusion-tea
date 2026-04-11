# Design: Research Artifact Sync (R2 + rclone)

**Status**: Approved
**Owner**: Reid W
**Created**: 2026-04-03
**Branch**: design-space-explore
**Commit**: ea65924

## Overview

Migrate 38 concept research directories from `exploration/phase_1a/research/` to `knowledge/concept_research/`, sync ~1019 binary artifacts via Cloudflare R2 (`1cfe-research` bucket), and index the collection for agent discoverability. A symlink preserves backward compatibility.

## Related Artifacts

- **Spec**: `.project/active/research-artifact-sync/spec.md`
- **Research**: `.project/research/20260403-research-artifact-storage-options.md`

## Research Findings

### Current State

- **38 concept directories** + 1 report file (`source_replacement_report.md`) in `exploration/phase_1a/research/`
- **1019 binary files** (PNG, HTML, PDF) totaling ~60 MB
- **815 text files** (MD, JSON) totaling ~89 MB
- **149 MB total**
- 2 concepts (20a, 20b) have 0 iterations/sources — empty placeholder directories
- Iteration counts range from 1 to 3 per concept; source counts from 2 to 22

### Code Consumers

Only one code consumer of `RESEARCH_DIR`:

- **`exploration/concept_analysis/scripts/run_analysis.py`** (lines 40-42):
  ```python
  PHASE_1A_DIR = CONCEPT_ANALYSIS_DIR.parent / "phase_1a"
  SCHEMA_PATH = PHASE_1A_DIR / "schema.md"
  RESEARCH_DIR = PHASE_1A_DIR / "research"
  ```
  `RESEARCH_DIR` is used by 5 functions (lines 617-758), all via default parameter `research_dir: Path = RESEARCH_DIR`. No other `.py` or `.sh` files reference the path.

### Existing Patterns

- **`scripts/extract_all.sh`**: Existing shell script pattern — `set -euo pipefail`, parallel execution, log capture, exit status reporting. Good structural reference for `sync_research.sh`.
- **`.env.example`**: Currently has `SYSIDE_LICENSE_KEY`, `ZOTERO_KEY`, `ZOTERO_ID`. R2 credentials follow same pattern.
- **`.gitignore`**: Already has binary exclusion patterns for the old path (lines at bottom of file). These will be replaced by a local `.gitignore` in `knowledge/concept_research/`.
- **rclone**: Not currently installed. Must be added as a prerequisite.

### Symlink Considerations

The symlink `exploration/phase_1a/research/` → `../../knowledge/concept_research/` will:
- Make `run_analysis.py` work unchanged during transition (resolves via symlink)
- Keep the 177 embedded paths in saved prompt files functional
- Resolve correctly via `Path.resolve()` (Python follows symlinks by default)

The relative symlink `../../knowledge/concept_research/` is correct because `exploration/phase_1a/research/` is 2 levels deep from repo root (`exploration/phase_1a/`), and the target is `knowledge/concept_research/` from root.

## Proposed Design

### Component 1: Migration Script

**File**: `scripts/migrate_research.py`

Python (not shell) because we need file counting, validation, and reporting that's awkward in bash.

**Interface**:
```bash
uv run python scripts/migrate_research.py              # full migration
uv run python scripts/migrate_research.py --dry-run    # report only
```

**Logic**:
1. Verify source exists (`exploration/phase_1a/research/`)
2. Verify destination doesn't exist yet (`knowledge/concept_research/`)
3. `shutil.copytree()` the entire directory
4. Count files in source and destination, compare (by category: `.md`, `.json`, `.png`, `.html`, `.pdf`)
5. Report: files copied, binary vs text breakdown
6. Remove original directory
7. Create symlink: `exploration/phase_1a/research/` → `../../knowledge/concept_research/`
8. Verify symlink resolves correctly

**Idempotency**: If destination already exists, check if symlink already exists. If both are in place, report "already migrated" and exit 0.

### Component 2: Gitignore Update

**File**: `knowledge/concept_research/.gitignore`

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

**Old patterns to remove** from root `.gitignore`:
```gitignore
# These three lines are replaced by knowledge/concept_research/.gitignore
exploration/phase_1a/research/**/sources/*/images/
exploration/phase_1a/research/**/sources/*/raw.html
exploration/phase_1a/research/**/sources/*/raw.pdf
```

The migration script creates the local `.gitignore` as part of migration. The root `.gitignore` cleanup is a separate manual edit (part of the implementation, not the script).

### Component 3: R2 Sync Script

**File**: `scripts/sync_research.sh`

**Interface**:
```bash
./scripts/sync_research.sh pull                          # pull all
./scripts/sync_research.sh push                          # push all
./scripts/sync_research.sh pull --dry-run                # preview
./scripts/sync_research.sh pull 01-hts-compact-tokamak   # single concept
```

**Design**:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Configuration
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOCAL_DIR="$REPO_ROOT/knowledge/concept_research"
REMOTE="r2:1cfe-research/concept_research"
INCLUDE_ARGS=(--include "*.pdf" --include "*.html" --include "*.png"
              --include "*.jpg" --include "*.jpeg" --include "*.gif"
              --include "*.svg")

# Parse arguments
ACTION="${1:?Usage: sync_research.sh <pull|push> [--dry-run] [concept-id]}"
shift
DRY_RUN=""
CONCEPT=""
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN="--dry-run" ;;
    *) CONCEPT="$arg" ;;
  esac
done

# Preflight checks
command -v rclone >/dev/null 2>&1 || { echo "error: rclone not installed"; exit 1; }
rclone lsd r2: >/dev/null 2>&1 || { echo "error: R2 remote 'r2' not configured in rclone"; exit 1; }

# Build paths
if [[ -n "$CONCEPT" ]]; then
  LOCAL_DIR="$LOCAL_DIR/$CONCEPT"
  REMOTE="$REMOTE/$CONCEPT"
fi

# Execute
case "$ACTION" in
  pull) rclone sync "$REMOTE" "$LOCAL_DIR" "${INCLUDE_ARGS[@]}" $DRY_RUN --progress ;;
  push) rclone sync "$LOCAL_DIR" "$REMOTE" "${INCLUDE_ARGS[@]}" $DRY_RUN --progress ;;
  *) echo "error: unknown action '$ACTION' (use pull or push)"; exit 1 ;;
esac
```

**Key decisions**:
- Uses `rclone sync` (mirror semantics) — destination matches source exactly. This is appropriate because we want the R2 bucket to be an exact mirror of local binary artifacts.
- `--include` filters ensure only binary types are transferred (rclone excludes everything not included).
- `--progress` gives transfer feedback.
- Remote name `r2` is conventional — the user configures this via `rclone config`.
- No `.env` loading needed — rclone uses its own config file (`~/.config/rclone/rclone.conf`). The `.env.example` documents what's needed but rclone doesn't read `.env`.

**On `.env.example` vs rclone config**: rclone has its own credential store. Adding `R2_ACCESS_KEY_ID` and `R2_SECRET_ACCESS_KEY` to `.env.example` is misleading if nothing reads them. Instead, the README documents how to run `rclone config` to set up the `r2` remote. The `.env.example` gets a comment pointing to the rclone setup docs, not actual credential variables.

### Component 4: Pipeline Path Update

**File**: `exploration/concept_analysis/scripts/run_analysis.py`

**Change** (lines 40-42):
```python
# Before:
PHASE_1A_DIR = CONCEPT_ANALYSIS_DIR.parent / "phase_1a"
SCHEMA_PATH = PHASE_1A_DIR / "schema.md"
RESEARCH_DIR = PHASE_1A_DIR / "research"

# After:
REPO_ROOT = Path(__file__).resolve().parents[3]
RESEARCH_DIR = REPO_ROOT / "knowledge" / "concept_research"

PHASE_1A_DIR = CONCEPT_ANALYSIS_DIR.parent / "phase_1a"
SCHEMA_PATH = PHASE_1A_DIR / "schema.md"
```

This is the only code change. All downstream functions already accept `research_dir` as a parameter — no signature changes needed.

**Note**: Because the symlink exists, the old relative path would also work. But updating the constant is correct — the canonical path should be the real one, not the symlink. This also means the code works even if the symlink is eventually removed.

### Component 5: Source Indexing

#### 5a: Top-level SOURCE_INDEX.md entry

Append to `knowledge/SOURCE_INDEX.md`:

```markdown
### Concept Research Dossiers
- **Type**: research collection
- **Location**: knowledge/concept_research/
- **Use for**: Per-concept techno-economic research across 38 fusion concepts.
  Contains dossiers, source extractions (HTML/PDF with agentic-mbse), iteration
  history, and synthesis outputs. See `knowledge/concept_research/SOURCE_INDEX.md`
  for detailed per-concept source listing. Serves all RQs.
```

No Zotero metadata or SHA256 — this is a collection, not a single extracted document.

#### 5b: Inner SOURCE_INDEX.md

**File**: `knowledge/concept_research/SOURCE_INDEX.md`

**Generated by the migration script** (not hand-written). The script scans the migrated directory tree and produces a structured index.

**Format**:

```markdown
# Concept Research — Source Index

Per-concept research dossiers and source extractions for the Fusion TEA
concept landscape. Binary artifacts (PDF, HTML, PNG) synced via R2;
markdown and JSON tracked in git.

Sync: `./scripts/sync_research.sh pull`

## Concepts

### 01-hts-compact-tokamak
- **Dossier**: `01-hts-compact-tokamak/dossier.md`
- **Iterations**: 2 (iter-03, iter-04)
- **Sources** (8):
  - `iter-03/sources/arc-reactor-specifications` — [HTML]
  - `iter-03/sources/sparc-icrf-heating-paper` — [HTML]
  - `iter-04/sources/arc-power-conversion-studies` — [PDF]
  - `iter-04/sources/cfs-2025-2026-updates` — [HTML]
  - *(+ 4 processed .md extractions)*

### 02-acoustic-icf-sonofusion
...
```

**Source type detection**: The script checks each `sources/{name}/` companion directory for `raw.html`, `raw.pdf`, or `images/` to determine the source type label. Sources with only `.md` files (no companion directory) are listed as "processed extraction."

**Why generate rather than hand-write**: 38 concepts, 280+ sources — manual authoring is error-prone and immediately stale. The migration script has all the data it needs to generate this. It can be regenerated with a `--reindex` flag if the collection changes.

### Component 6: README

**File**: `knowledge/concept_research/README.md`

Documents:
- What this directory contains (concept research for 38 fusion concepts)
- Directory structure (concept → iterations → sources)
- What's in git vs R2 (markdown/JSON in git, PDF/HTML/PNG via R2)
- How to sync (`./scripts/sync_research.sh pull`)
- How to set up rclone for R2 (link to Cloudflare R2 docs, `rclone config` steps)
- Relationship to the concept analysis pipeline

### Component 7: .env.example Update

Add a comment block (not variables) since rclone manages its own credentials:

```bash
# --- R2 artifact sync ---
# Binary research artifacts are synced via rclone to Cloudflare R2.
# Run: rclone config
#   - Remote name: r2
#   - Type: s3
#   - Provider: Cloudflare
#   - Access key / secret: from Cloudflare dashboard → R2 → API tokens
#   - Endpoint: <account-id>.r2.cloudflarestorage.com
# Then: ./scripts/sync_research.sh pull
```

## Potential Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Binary files already in git history bloat clone size | Certain | Out of scope for this work. Can be addressed later with `git filter-repo`. The immediate goal is preventing further growth. |
| Symlink breaks on Windows | Low (team uses Linux/Mac) | Document in README. Windows users can use `mklink /D` or just update their `RESEARCH_DIR`. |
| `rclone sync` deletes files on destination that don't exist on source | Possible if used carelessly | Dry-run mode documented prominently. `push` and `pull` are explicit — no accidental direction. |
| Large initial upload takes time | Low risk | ~60 MB of binaries — minutes, not hours. |

## Integration Strategy

**Execution order** (some steps can be parallelized):

1. **Migration script** creates destination, copies files, creates symlink, generates inner SOURCE_INDEX.md
2. **Gitignore updates** — add local `.gitignore` in `concept_research/`, remove old patterns from root
3. **Pipeline path update** — 3-line change in `run_analysis.py`
4. **Top-level SOURCE_INDEX.md** — append umbrella entry
5. **Sync script + README + .env.example** — new files
6. **Verify**: `run_analysis.py status` shows identical output
7. **R2 upload**: `./scripts/sync_research.sh push` to seed the bucket
8. **Round-trip test**: delete local binaries → `pull` → verify files match

Steps 1-5 are a single commit. Steps 6-8 are verification (not committed).

## Validation Approach

1. **File count parity**: Migration script reports source vs destination counts by type
2. **Symlink resolution**: `python -c "from pathlib import Path; print(Path('exploration/phase_1a/research').resolve())"` → should print canonical path
3. **Pipeline equivalence**: `uv run python exploration/concept_analysis/scripts/run_analysis.py status` output matches pre-migration baseline
4. **Dry-run prompt check**: `run_analysis.py gap-check 01 --dry-run` generates same prompt content
5. **R2 round-trip**: push → delete local binaries → pull → `diff -r` shows no differences
6. **Git status clean**: after migration, `git status` shows no binary files (only new/moved `.md`/`.json` files and new scripts)

---

**Next Step**: After approval → `/_my_plan` for phased implementation, or `/_my_implement` if the scope is clear enough to proceed directly.
