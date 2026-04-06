# Implementation Plan: Research Artifact Sync

**Status:** In Progress
**Created:** 2026-04-03
**Last Updated:** 2026-04-03

## Source Documents
- **Spec:** `.project/active/research-artifact-sync/spec.md`
- **Design:** `.project/active/research-artifact-sync/design.md` — see here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
Phase 1 establishes the new directory structure — everything else depends on it. Phase 2 validates the pipeline still works. Phase 3 adds R2 tooling and docs, which are independent additions.

---

## Phase 1: Migration Script + Gitignore

### Goal
Move research to `knowledge/concept_research/`, create symlink, generate inner SOURCE_INDEX.md, update gitignore. This is the foundation — all other phases depend on files being in the right place.

### Changes Required

**See `design.md#component-1` for migration script logic and `design.md#component-2` for gitignore details.**

#### 1. Migration Script
**File:** `scripts/migrate_research.py` (NEW)
- [x] Create script with `--dry-run` and `--reindex` flags
- [x] Implement: verify source exists, verify destination doesn't exist
- [x] Implement: `shutil.copytree()` from `exploration/phase_1a/research/` → `knowledge/concept_research/`
- [x] Implement: file count comparison by category (`.md`, `.json`, `.png`, `.html`, `.pdf`)
- [x] Implement: remove original directory, create symlink
- [x] Implement: verify symlink resolves correctly
- [x] Implement: idempotency check (already migrated → exit 0)
- [x] Implement: generate `knowledge/concept_research/SOURCE_INDEX.md` (see `design.md#component-5b` for format)
  - Scan all concept dirs for iterations, sources, source types (HTML/PDF detection via companion dirs)
- [x] Implement: create `knowledge/concept_research/.gitignore` (see `design.md#component-2` for content)

#### 2. Root Gitignore Cleanup
**File:** `.gitignore` (MODIFY)
- [x] Remove the 3 old `exploration/phase_1a/research/` binary exclusion patterns

#### 3. Run Migration
- [x] Execute: `uv run python scripts/migrate_research.py`
- [x] Verify output: file counts match, symlink created

### Validation

**Automated:**
- [x] Migration script reports matching file counts for all categories
- [x] `python -c "from pathlib import Path; print(Path('exploration/phase_1a/research').resolve())"` prints path containing `knowledge/concept_research`

**Manual:**
- [x] `ls knowledge/concept_research/` shows 38 concept dirs + SOURCE_INDEX.md + .gitignore
- [x] `ls -la exploration/phase_1a/research` shows symlink
- [x] `cat knowledge/concept_research/SOURCE_INDEX.md` shows all 38 concepts with sources
- [x] `git status` shows no binary files staged (only .md/.json files and new scripts)

**What We Know Works After This Phase:**
Files are in canonical location, symlink provides backward compatibility, binaries are gitignored, inner source index exists.

---

## Phase 2: Pipeline Path Update + Verification

### Goal
Update `run_analysis.py` to use the canonical path and verify the pipeline produces identical output.

### Changes Required

**See `design.md#component-4` for the exact 3-line change.**

#### 1. Capture Baseline
- [x] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py status` and save output
- [x] Run `uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check 01 --dry-run` and save prompt output

#### 2. Pipeline Path Update
**File:** `exploration/concept_analysis/scripts/run_analysis.py:40-42` (MODIFY)
- [x] Add `REPO_ROOT = Path(__file__).resolve().parents[3]`
- [x] Change `RESEARCH_DIR` to `REPO_ROOT / "knowledge" / "concept_research"`
- [x] Keep `PHASE_1A_DIR` and `SCHEMA_PATH` for `schema.md` reference

#### 3. Verify Equivalence
- [x] Run `status` again, diff against baseline
- [x] Run `gap-check 01 --dry-run` again, diff prompt content against baseline

### Validation

**Automated:**
- [x] `run_analysis.py status` output matches baseline exactly
- [x] `run_analysis.py gap-check 01 --dry-run` prompt content matches baseline

**Manual:**
- [x] `run_analysis.py list` shows all 38 concepts

**What We Know Works After This Phase:**
The concept analysis pipeline works identically from the new location. The migration is functionally complete.

---

## Phase 3: Sync Script + Onboarding Docs

### Goal
Add R2 sync tooling, README, top-level SOURCE_INDEX entry, and .env.example update. These are pure additions — independent of migration correctness.

### Changes Required

**See `design.md#component-3` for sync script, `design.md#component-5a` for SOURCE_INDEX entry, `design.md#component-6` for README, `design.md#component-7` for .env.example.**

#### 1. Sync Script
**File:** `scripts/sync_research.sh` (NEW)
- [x] Create script with pull/push/dry-run/concept-specific interface
- [x] Implement preflight checks (rclone installed, R2 remote configured)
- [x] Implement rclone sync with `--include` filters for binary types
- [x] `chmod +x scripts/sync_research.sh`

#### 2. README
**File:** `knowledge/concept_research/README.md` (NEW)
- [x] Document: what the directory contains, directory structure
- [x] Document: git vs R2 (what's tracked vs synced)
- [x] Document: how to sync (`./scripts/sync_research.sh pull`)
- [x] Document: rclone setup for R2 (config steps, Cloudflare dashboard)
- [x] Document: relationship to concept analysis pipeline

#### 3. Top-level SOURCE_INDEX Entry
**File:** `knowledge/SOURCE_INDEX.md` (MODIFY)
- [x] Append umbrella entry for Concept Research Dossiers (see `design.md#component-5a`)

#### 4. .env.example Update
**File:** `.env.example` (MODIFY)
- [x] Add comment block for R2 setup instructions (see `design.md#component-7`)

### Validation

**Manual:**
- [x] `./scripts/sync_research.sh pull --dry-run` either shows transfer plan (if rclone configured) or gives clear error message
- [x] `cat knowledge/concept_research/README.md` has complete setup instructions
- [x] `grep -A5 "Concept Research" knowledge/SOURCE_INDEX.md` shows umbrella entry
- [x] `cat .env.example` includes R2 setup comment block

**What We Know Works After This Phase:**
Full tooling is in place. A new team member can clone, read the README, set up rclone, and `sync_research.sh pull` to get all binary artifacts.

---

## Post-Implementation: R2 Upload (Manual)

Not part of the automated plan — requires rclone to be installed and configured.

- [ ] Install rclone: `sudo apt install rclone` or `brew install rclone`
- [ ] Configure R2 remote: `rclone config` (type: s3, provider: Cloudflare)
- [ ] Initial push: `./scripts/sync_research.sh push`
- [ ] Round-trip test: delete local binaries → `./scripts/sync_research.sh pull` → verify files match

---

## Risk Management

**See `design.md#potential-risks` for full risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: Migration script validates file counts before removing original — no data loss possible. `--dry-run` available for preview.
- **Phase 2**: Baseline capture before any code change — diff-based validation catches any regression.
- **Phase 3**: Sync script fails gracefully if rclone isn't installed — no hard dependency.

## Implementation Notes

*To be filled during implementation.*

### Phase 1 Completion
**Completed:** 2026-04-03
**Actual Changes:**
- Created `scripts/migrate_research.py` with `--dry-run` and `--reindex` flags
- Updated `.gitignore`: replaced 3 old exploration patterns with comment pointing to new local `.gitignore`
- Ran migration: 1834 files copied (1019 binary, 815 text), counts verified
- Created `knowledge/concept_research/.gitignore` (filters 7 binary extensions)
- Generated `knowledge/concept_research/SOURCE_INDEX.md` (38 concepts, all sources indexed)
- Symlink `exploration/phase_1a/research` → `../../knowledge/concept_research` verified
- `git add --dry-run` confirms 0 binaries, 817 text files would be staged
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-04-03
**Actual Changes:**
- Modified `exploration/concept_analysis/scripts/run_analysis.py:40-43` — added `REPO_ROOT`, changed `RESEARCH_DIR` to canonical path, kept `PHASE_1A_DIR` for `schema.md`
- All three pipeline commands (`status`, `gap-check 01 --dry-run`, `list`) produce identical output before and after
**Issues:** None
**Deviations:** None

### Phase 3 Completion
**Completed:** 2026-04-03
**Actual Changes:**
- Created `scripts/sync_research.sh` — rclone wrapper with pull/push/dry-run/concept-specific sync, preflight checks, binary-only `--include` filters
- Created `knowledge/concept_research/README.md` — directory structure, git vs R2 table, rclone setup, sync instructions, pipeline relationship
- Appended umbrella entry to `knowledge/SOURCE_INDEX.md` (before "How Sources Are Used" section)
- Added R2 comment block to `.env.example` (rclone config steps, not env vars)
**Issues:** None
**Deviations:** None

---

**Status**: Complete
