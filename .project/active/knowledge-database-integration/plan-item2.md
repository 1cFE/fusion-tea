# Implementation Plan: Single-Source End-to-End Pipeline (KNOW-DB Item 2)

**Status:** In Progress
**Created:** 2026-02-08
**Last Updated:** 2026-02-08
**Epic:** `.project/backlog/epic-knowledge-database-integration.md` — Item 2

---

## Source Documents
- **Spec:** `.project/active/knowledge-database-integration/spec.md`
- **Design:** `.project/active/knowledge-database-integration/design.md` — See here for component details, dependencies, architecture

## Implementation Strategy

**Phasing Rationale:**
This is a manual pipeline execution, not application code. Phases follow the data flow: download → extract → register → commit. The riskiest step (group library connectivity) comes first to fail fast. No unit tests — validation is via shell checks and manual inspection at each phase boundary.

**Overall Validation Approach:**
- Each phase has explicit verification checks (shell commands + manual inspection)
- Each phase produces artifacts consumed by the next phase
- Phase boundaries are natural stopping points if issues arise

---

## Phase 1: Download Script + Group Library Connectivity

### Goal
Write `scripts/zotero_group_download.py` and prove the 1cfe group library API works. This is the primary de-risk: Item 1 only proved the user library, and group library access is a different API call with potentially different permissions.

### Validation Stencil (Verify Before Proceeding)
```bash
# 1. Script runs without import errors
uv run python scripts/zotero_group_download.py --help

# 2. Download succeeds — PDF exists with non-zero size
uv run python scripts/zotero_group_download.py PMXLGPKG
ls -la knowledge/raw/*.pdf

# 3. SHA256 is printed in output (capture for Phase 3)

# 4. Skip-if-exists works on re-run
uv run python scripts/zotero_group_download.py PMXLGPKG
# Should print "already exists" and skip download
```

### Changes Required

**See `design.md#component-1` for:** Script interface, arguments, behavior, patterns reused from `zotero_test.py`.

**Specific file changes:**

#### 1. Download Script
**File:** `scripts/zotero_group_download.py` (NEW)
- [x] Create script with argparse: `item_key` (positional), `--tag-extracted`, `--tag-only`, `--output-dir`
- [x] Connect to group library: `zotero.Zotero(5428393, 'group', api_key)`
- [x] Fetch item metadata + find PDF child attachment
- [x] Download via `zot.dump()` to `--output-dir` (default `knowledge/raw/`)
- [x] Skip-if-exists: check output dir for matching filename before downloading
- [x] Compute and print SHA256
- [x] `--tag-only` mode: skip download, just tag via `zot.add_tags()`
- [x] `--tag-extracted` mode: download then tag
- [x] Print summary: title, Zotero key, filename, size, SHA256, save path

### Validation (How to Verify This Phase)

**Automated:**
- [x] `uv run python scripts/zotero_group_download.py PMXLGPKG` exits 0
- [x] PDF file exists in `knowledge/raw/` with size > 0
- [x] Re-running skips download (skip-if-exists)

**Manual:**
- [x] Script output shows title, Zotero key `5428393:PMXLGPKG`, SHA256
- [x] Capture SHA256 from output — needed for SOURCE_INDEX.md in Phase 3

**What We Know Works After This Phase:**
- Group library API connectivity (the key Item 1 → Item 2 gap)
- PDF download to `knowledge/raw/`
- Script is reusable for `--tag-only` in Phase 3

---

## Phase 2: PDF Extraction

### Goal
Run `agentic-mbse extract` with full enhancement pipeline on the downloaded fusion PDF. This validates that the extraction toolchain handles real fusion documents (complex tables, equations, multi-section structure).

### Validation Stencil (Verify Before Proceeding)
```bash
# 1. Extraction completes successfully
uv run agentic-mbse extract knowledge/raw/<filename>.pdf \
    --output knowledge/sources/tea_dt_mfe_cost_analysis/ \
    --index --summarize --enhance

# 2. All expected outputs exist
ls knowledge/sources/tea_dt_mfe_cost_analysis/
# Should show: full_document.md, INDEX.md, summary.json, images/

# 3. full_document.md has substantial content
wc -c knowledge/sources/tea_dt_mfe_cost_analysis/full_document.md
# Should be >1000 chars

# 4. summary.json shows success
python3 -c "import json; d=json.load(open('knowledge/sources/tea_dt_mfe_cost_analysis/summary.json')); print(d['processing_completed'])"
# Should print: True

# 5. Compute extract SHA256 (capture for Phase 3)
sha256sum knowledge/sources/tea_dt_mfe_cost_analysis/full_document.md
```

### Changes Required

**See `design.md#component-2` for:** Exact CLI invocation, slug choice rationale, expected outputs.

**No new files.** Execute the extraction CLI interactively.

- [x] Run `uv run agentic-mbse extract` with flags from `design.md#component-2`
- [x] If extraction fails with `--enhance`: retry with `--structure-only` (Layer 3 only)
- [x] If Layer 2 (GMFT) crashes: retry with `--no-tables`
- [x] Note any extraction quality issues for documentation (non-blocking per spec)

### Validation (How to Verify This Phase)

**Automated:**
- [x] `full_document.md` exists, >1000 chars
- [x] `INDEX.md` exists with section entries
- [x] `summary.json` exists with `processing_completed: true`

**Manual:**
- [x] Open `full_document.md` — document is readable, section structure is sensible
- [x] Spot-check: tables are formatted, equations are recognizable
- [x] Capture `full_document.md` SHA256 — needed for SOURCE_INDEX.md in Phase 3
- [x] Note any quality issues (garbled tables, missing images) — document but don't block

**What We Know Works After This Phase:**
- `agentic-mbse extract --enhance` handles real fusion PDFs
- Extraction output is in the expected directory structure
- Both SHA256 values (raw PDF + extracted markdown) are available for registration

---

## Phase 3: Registration + Config + Tagging

### Goal
Update SOURCE_INDEX.md with the new entry (canonical + extended metadata), create LOCAL_SOURCES.yaml template, add gitignore entry, and tag the Zotero item as `extracted`.

### Validation Stencil (Verify Before Proceeding)
```bash
# 1. SOURCE_INDEX.md has new entry with all fields
grep -c "### TEA D-T MFE Cost Analysis" knowledge/SOURCE_INDEX.md
# Should print: 1

grep -c "Zotero Key" knowledge/SOURCE_INDEX.md
# Should print: 1

# 2. PyFECONS entry unchanged
grep "### PyFECONS" knowledge/SOURCE_INDEX.md
# Should still exist

# 3. LOCAL_SOURCES.yaml exists
test -f knowledge/LOCAL_SOURCES.yaml && echo "EXISTS" || echo "MISSING"

# 4. LOCAL_SOURCES.yaml is gitignored
git check-ignore knowledge/LOCAL_SOURCES.yaml
# Should print the path (meaning it's ignored)

# 5. Zotero tag applied
uv run python scripts/zotero_group_download.py PMXLGPKG --tag-only
# Should succeed
```

### Changes Required

**See `design.md#component-3` for:** New entry structure, placement, backward compatibility.
**See `design.md#component-4` for:** LOCAL_SOURCES.yaml content, gitignore update.

**Specific file changes:**

#### 1. SOURCE_INDEX.md
**File:** `knowledge/SOURCE_INDEX.md` (EDIT)
- [x] Add new `### TEA D-T MFE Cost Analysis` entry after PyFECONS
- [x] Include 4 canonical fields (Type, Location, Use for, Validation)
- [x] Add `#### Extended Metadata` sub-heading with 5 extended fields
- [x] Fill in SHA256 values captured from Phases 1 and 2
- [x] Verify PyFECONS entry is unchanged

#### 2. LOCAL_SOURCES.yaml
**File:** `knowledge/LOCAL_SOURCES.yaml` (NEW)
- [x] Create with template content from `design.md#component-4`
- [x] Placeholder path for PyFECONS (`/path/to/PyFECONS`)
- [x] Zotero group config (id, name)
- [x] Comments explaining STATUS: convention only, no code reads it

#### 3. Gitignore Update
**File:** `.gitignore` (EDIT)
- [x] Add `knowledge/LOCAL_SOURCES.yaml` entry

#### 4. Zotero Tag
- [ ] Run `uv run python scripts/zotero_group_download.py PMXLGPKG --tag-only`
- [ ] Verify tag was applied (check script output)

### Validation (How to Verify This Phase)

**Automated:**
- [x] `grep "### TEA D-T MFE Cost Analysis" knowledge/SOURCE_INDEX.md` finds entry
- [x] `grep "### PyFECONS" knowledge/SOURCE_INDEX.md` still finds original entry
- [x] `git check-ignore knowledge/LOCAL_SOURCES.yaml` confirms gitignored
- [ ] Zotero tag script exits 0 — **BLOCKED: 403 Write access denied (see Issues)**

**Manual:**
- [x] Read SOURCE_INDEX.md — new entry has all 9 fields, old entry untouched
- [x] Read LOCAL_SOURCES.yaml — comments are clear, placeholder paths used

**What We Know Works After This Phase:**
- SOURCE_INDEX.md extended metadata format is established
- LOCAL_SOURCES.yaml convention is in place
- Zotero item reflects pipeline state (`extracted` tag)

---

## Phase 4: Verification + Commit

### Goal
Final verification against all spec acceptance criteria, then git commit. This is the gate before declaring Item 2 complete.

### Validation Stencil (Verify Before Committing)
```bash
# Acceptance criteria checklist
# AC-1: PDF downloaded
test -f knowledge/raw/*.pdf && echo "PASS" || echo "FAIL"

# AC-2: Extraction outputs exist
test -f knowledge/sources/tea_dt_mfe_cost_analysis/full_document.md && echo "PASS" || echo "FAIL"
test -f knowledge/sources/tea_dt_mfe_cost_analysis/INDEX.md && echo "PASS" || echo "FAIL"
test -f knowledge/sources/tea_dt_mfe_cost_analysis/summary.json && echo "PASS" || echo "FAIL"

# AC-3: SOURCE_INDEX.md updated
grep -q "5428393:PMXLGPKG" knowledge/SOURCE_INDEX.md && echo "PASS" || echo "FAIL"

# AC-4: LOCAL_SOURCES.yaml exists and gitignored
test -f knowledge/LOCAL_SOURCES.yaml && echo "PASS" || echo "FAIL"
git check-ignore -q knowledge/LOCAL_SOURCES.yaml && echo "PASS" || echo "FAIL"

# AC-5: No secrets staged
git diff --cached --name-only | grep -q ".env" && echo "FAIL: .env staged" || echo "PASS"

# AC-6: No PDFs staged
git diff --cached --name-only | grep -q ".pdf" && echo "FAIL: PDF staged" || echo "PASS"
```

### Changes Required

**See `design.md#component-5` for:** Staged files list, NOT-staged list.

**No new files.** Git operations only.

- [x] Run full acceptance criteria checklist (stencil above)
- [x] Stage files: `scripts/zotero_group_download.py`, `knowledge/sources/tea_dt_mfe_cost_analysis/`, `knowledge/SOURCE_INDEX.md`, `.gitignore`
- [x] Verify nothing sensitive is staged (`git diff --cached --name-only`)
- [x] Commit with descriptive message referencing KNOW-DB Item 2

### Validation (How to Verify This Phase)

**Automated:**
- [x] All acceptance criteria checks pass
- [x] `git status` shows clean working tree (except gitignored files and unrelated changes)

**Manual:**
- [x] Review `git diff --cached` — only expected files
- [x] No `.env`, no PDFs, no `LOCAL_SOURCES.yaml` in staged changes

**What We Know Works After This Phase:**
- Full end-to-end pipeline: Zotero group download → extract → register → tag → commit
- All spec acceptance criteria met
- Item 2 is complete, unblocking Item 3

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: If group API fails, check API key permissions at zotero.org/settings/keys. May need to regenerate with group access enabled.
- **Phase 2**: If `--enhance` fails or is extremely slow, fall back to `--structure-only` or plain extraction. Document quality delta. If `--no-tables` needed, note for upstream issue.
- **Phase 3**: If `zot.add_tags()` API is different than expected, check pyzotero docs. Non-blocking — can tag manually via Zotero desktop as last resort.

---

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-02-08
**Actual Changes:**
- Created `scripts/zotero_group_download.py` with argparse, group library connection, PDF download, skip-if-exists, SHA256, tagging support
- Downloaded PDF (2,435,839 bytes) to `knowledge/raw/`
- Raw PDF SHA256: `58d6e64c6e822645ed30f81c570396b6a4f20a66c969f65cb599d6084644e68b`
- Filename: `Araiinejad and Shirvan - 2025 - Techno-economic analysis of deuterium-tritium magnetic confinement fusion power plants.pdf`
**Issues:** None
**Deviations:** None — implementation matches design exactly

### Phase 2 Completion
**Completed:** 2026-02-08
**Actual Changes:**
- Ran `uv run agentic-mbse extract` with `--output knowledge/sources/ --index --summarize --enhance --force`
- Renamed auto-generated slug (`Araiinejad_and_Shirvan___2025___...`) to `tea_dt_mfe_cost_analysis/` per design
- Outputs: `full_document.md` (74,494 bytes, 74,200 chars), `INDEX.md` (5,404 bytes, 10 sections), `summary.json`, `images/` (8 images)
- Extract SHA256: `9d8a160c4dfe6cbe39c2e804979799d7f3b41d39bde983bd6d61c4830147ce63`
- Backend: pymupdf; structure enhancement skipped (document already well-structured)
- Quality: Good — readable text, section structure preserved, images extracted
**Issues:** None
**Deviations:**
- `--output` flag is a base directory, not final path — tool auto-creates sanitized subdirectory. Used `--output knowledge/sources/` then renamed to `tea_dt_mfe_cost_analysis/`
- Enhancement Layer 3 (structural repair) skipped automatically — document was already well-structured. This is expected behavior, not a failure.

### Phase 3 Completion
**Completed:** 2026-02-08
**Actual Changes:**
- Added `### TEA D-T MFE Cost Analysis` entry to `knowledge/SOURCE_INDEX.md` with 4 canonical + 5 extended metadata fields
- Created `knowledge/LOCAL_SOURCES.yaml` with template content per design
- Added `knowledge/LOCAL_SOURCES.yaml` to `.gitignore`
**Issues:**
- Zotero tagging failed with 403 Write access denied. API key has read-only group access. Per plan risk mitigation, this is non-blocking — tag manually via Zotero desktop or regenerate API key with group write permissions at zotero.org/settings/keys.
**Deviations:**
- Zotero tag not applied via API (FR-4 partially unmet). All other Phase 3 items complete.

### Phase 4 Completion
**Completed:** 2026-02-08
**Actual Changes:**
- All 6 acceptance criteria passed
- Staged 14 files: `scripts/zotero_group_download.py`, `knowledge/sources/tea_dt_mfe_cost_analysis/` (full_document.md, INDEX.md, summary.json, 8 images), `knowledge/SOURCE_INDEX.md`, `.gitignore`
- Committed as `54f126b` on branch `proj-modeling-0`
**Issues:** None
**Deviations:** None

---

**Status**: ~~Draft~~ → ~~In Progress~~ → **Complete**
