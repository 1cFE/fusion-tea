# Implementation Plan: Merge Concept Explorer and Write Operator Guide

**Status:** Draft
**Created:** 2026-04-06
**Last Updated:** 2026-04-06

## Source Documents
- **Spec:** `.project/active/explorer-merge/spec.md`
- **Design:** `.project/active/explorer-merge/design.md` ← See here for component details, merged file contents, path corrections

## Implementation Strategy

**Phasing Rationale:**
Pre-merge fixes (Phase 1) go on the explorer branch in the worktree to keep them atomic and avoid tangling with merge conflicts. The merge itself (Phase 2) is then a cleaner operation. Post-merge cleanup (Phase 3) is cosmetic and low-risk. The operator guide (Phase 4) comes last because it documents the merged system and every command must be verified against reality.

**Overall Validation Approach:**
- Phase 1: Explorer test suite in worktree after each fix commit
- Phase 2: Pipeline smoke test + explorer tests + extraction + server startup
- Phase 3: Re-run tests to confirm no path breakage
- Phase 4: Manual execution of every command in the guide

**Working directories:**
- Phase 1: `~/1cfe/fusion-tea_concept-explorer` (worktree)
- Phases 2-4: `~/1cfe/fusion-tea` (main repo)

---

## Phase 1: Pre-Merge Fixes on Explorer Branch

### Goal
Fix three issues on `ralph/concept-explorer` before merging: corrupted CAS22 labels, mandatory playwright dependency, and stale `.project/active/` items. Each is a separate commit in the worktree.

### 1.1: Fix CAS22_NAMES Dict

**File:** `exploration/concept_explorer/models.py` (EDIT)
- [x] Replace `CAS22_NAMES` dict with authoritative 18-entry version from `design.md#step-12-fix-cas22_names-on-explorer-branch`
- [x] Verify `from_forward_result()` iterates all `CAS22_NAMES` keys (not a hardcoded subset)

**Test files** (EDIT — update assertions):
- [x] Search explorer tests for any assertions on CAS22 label strings (e.g., "Maintenance Equipment") and update to match corrected labels
- [x] Search for assertions on CAS22 key counts and update to expect 18 keys

**Validation:**
- [x] `cd ~/1cfe/fusion-tea_concept-explorer && uv run pytest exploration/concept_explorer/tests/ -x -v`
- [x] Commit: `fix: correct CAS22 sub-account labels and add missing keys (C220109-C220112)`

### 1.2: Make Playwright Optional

**File:** `pyproject.toml` (EDIT)
- [x] Remove `playwright` from `[dependency-groups] dev`
- [x] Add `[project.optional-dependencies] e2e = ["playwright>=1.58.0"]`

**File:** `exploration/concept_explorer/tests/test_views_manual.py` (EDIT)
- [x] Add after docstring, before other imports:
  ```python
  import pytest
  pytest.importorskip("playwright", reason="playwright not installed — install with: uv sync --extra e2e && playwright install chromium")
  ```

**File:** `exploration/concept_explorer/tests/test_integration_manual.py` (EDIT)
- [x] Same `importorskip` guard as above

**File:** `exploration/concept_explorer/tests/PLAYWRIGHT_GUIDE.md` (EDIT)
- [x] Update install instructions to note `uv sync --extra e2e && playwright install chromium`

**Validation:**
- [x] `cd ~/1cfe/fusion-tea_concept-explorer && uv lock && uv sync` (should NOT install playwright)
- [x] `uv run pytest exploration/concept_explorer/tests/ -x -v` (playwright tests skip with message, all others pass)
- [x] Commit: `fix: make playwright an optional e2e dependency`

### 1.3: Archive Completed Explorer Work Items

- [x] `git mv .project/active/compare-shell/ .project/completed/20260404_compare-shell/`
- [x] `git mv .project/active/selection-tray/ .project/completed/20260404_selection-tray/`
- [x] `git mv .project/active/views-capex-sensitivity/ .project/completed/20260404_views-capex-sensitivity/`
- [x] `git mv .project/active/views-categorical-summary/ .project/completed/20260404_views-categorical-summary/`
- [x] `git mv .project/active/explorer-integration/ .project/completed/20260404_explorer-integration/`
- [x] `git mv .project/active/explorer-ux-v2/ .project/completed/20260404_explorer-ux-v2/`
- [x] `git mv .project/active/concept-id-unification/ .project/completed/20260404_concept-id-unification/`
- [x] Also archive any other completed items from explorer that overlap with pipeline (e.g., `automated-concept-analysis`, `iterative-analysis-loop`, `constraint-atms-spike`, `source-replacement` if they exist)

**Validation:**
- [x] `ls .project/active/` shows only items not yet completed
- [x] Commit: `chore: archive completed explorer work items`

### What We Know Works After Phase 1
- CAS22 labels match costingfe source of truth (18 accounts, correct names)
- Playwright won't be pulled by default `uv sync`
- Playwright tests skip cleanly without crashing the test suite
- `.project/active/` on explorer branch has no stale completed items

---

## Phase 2: Git Merge + Conflict Resolution

### Goal
Merge `ralph/concept-explorer` into `design-space-explore` and resolve all conflicts. Regenerate lock file.

### 2.1: Execute Merge

- [ ] `cd ~/1cfe/fusion-tea`
- [ ] `git merge ralph/concept-explorer --no-commit`
- [ ] Note which files have conflicts (expected: `pyproject.toml`, `.gitignore`, `tests/conftest.py`, `.project/CURRENT_WORK.md`, `.project/completed/CHANGELOG.md`, `uv.lock`)

### 2.2: Resolve pyproject.toml

- [ ] Write merged content per `design.md#step-22-pyprojecttoml-merged-content`
- [ ] Key points: keep `fusion-tea` name, `>=3.12` Python, superset deps, add `[project.optional-dependencies] e2e`, add `[dependency-groups] dev` with mypy/ruff, add `[tool.ruff]` and `[tool.mypy]` sections, keep all 4 UV sources

### 2.3: Resolve .gitignore

- [ ] Write merged content per `design.md#step-23-gitignore-merged-content`
- [ ] Key points: combine Python ignores, keep tool-owned entries, add explorer data/dist entries, add cache dirs

### 2.4: Resolve Other Conflicts

- [ ] `tests/conftest.py`: `git checkout design-space-explore -- tests/conftest.py` (keep pipeline's version with real fixtures)
- [ ] `.project/CURRENT_WORK.md`: Keep pipeline's version, append explorer status section per `design.md#step-24`
- [ ] `.project/completed/CHANGELOG.md`: Concatenate entries from both branches chronologically
- [ ] `uv.lock`: Delete and regenerate

### 2.5: Regenerate Lock File and Sync

- [ ] `rm -f uv.lock`
- [ ] `uv lock`
- [ ] `uv sync`

### 2.6: Commit Merge

- [ ] `git add -A`
- [ ] `git commit -m "Merge concept explorer (ralph/concept-explorer) into analysis pipeline branch"`

### Validation

**Automated:**
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py list` → 38 concepts
- [ ] `uv run pytest exploration/concept_explorer/tests/ -x -v` → All non-playwright tests pass, playwright tests skip
- [ ] `uv run pytest tests/ -x` → Existing pipeline/model tests still pass (if any)

**Manual:**
- [ ] `uv run python exploration/concept_explorer/extract_explorer_data.py --concepts 01 --skip-narrative` → Produces `exploration/concept_explorer/data/01.json`
- [ ] `uv run python exploration/concept_explorer/server.py &` → Starts on `http://127.0.0.1:8421`
- [ ] Open `http://127.0.0.1:8421` → Index page loads, concept 01 visible
- [ ] Open `http://127.0.0.1:8421/concept/01` → Profile page renders with CAS breakdown showing correct labels
- [ ] Kill server

**What We Know Works After Phase 2:**
- Both systems coexist in one repo with shared dependencies
- Pipeline CLI functional
- Explorer extraction, server, and test suite functional
- CAS22 labels correct in the running UX

---

## Phase 3: Post-Merge Cleanup

### Goal
Relocate explorer design artifacts from repo root to `exploration/concept_explorer/docs/`. Delete inert scaffolds.

### Changes

- [ ] `mkdir -p exploration/concept_explorer/docs/specs`
- [ ] `git mv DESIGN.md exploration/concept_explorer/docs/`
- [ ] `git mv DESIGN_v1.md exploration/concept_explorer/docs/`
- [ ] `git mv DESIGN_REVIEW.md exploration/concept_explorer/docs/`
- [ ] `git mv IMPLEMENTATION_PLAN_v1.md exploration/concept_explorer/docs/`
- [ ] `git mv AGENTS.md exploration/concept_explorer/docs/`
- [ ] `git mv PROMPT_build.md exploration/concept_explorer/docs/`
- [ ] `git mv PROMPT_plan.md exploration/concept_explorer/docs/`
- [ ] `git mv specs/* exploration/concept_explorer/docs/specs/ && rmdir specs`
- [ ] `git mv loop.sh exploration/concept_explorer/` (or `git rm` if no longer needed — check if referenced)
- [ ] `git rm -r src/concept_explorer/` (inert scaffold — real code is in `exploration/concept_explorer/`)
- [ ] Check if `tests/__init__.py` from explorer is empty/stub — if so, `git rm` it (pipeline's tests/ doesn't need it)

### Validation

- [ ] `uv run pytest exploration/concept_explorer/tests/ -x` → Still passes (no import path changes)
- [ ] `ls` at repo root → No explorer-specific design docs cluttering root
- [ ] Commit: `chore: relocate explorer design artifacts to exploration/concept_explorer/docs/`

**What We Know Works After Phase 3:**
- Repo root is clean
- All code still functional

---

## Phase 4: Operator Guide

### Goal
Write `exploration/concept_analysis/OPERATOR_GUIDE.md` — the 7-section human operator guide for the concept analysis → explorer review → approval workflow.

### Changes

**File:** `exploration/concept_analysis/OPERATOR_GUIDE.md` (NEW)
- [ ] Write preamble with "Typical Workflow" diagram (happy path overview)
- [ ] Section 1: Pipeline Quick Reference — status, stage1-all, add-source, review commands (correct path: `exploration/concept_analysis/scripts/run_analysis.py`)
- [ ] Section 2: Launching the Explorer — extract command, server command (port 8421), prerequisites
- [ ] Section 3: Explorer Tour — page-by-page walkthrough (Index, Profile, Comparison, Taxonomy) with red-flag checklists
- [ ] Section 4: Issue Triage via `/manage-concept` — modes A-D, change request protocol
- [ ] Section 5: Adding Sources Mid-Review — `add-source` → `stage1-all --resume` flow
- [ ] Section 6: Final Review, Feedback, and Synthesis — PROCEED/REVISE paths, address-review, synthesize
- [ ] Section 7: Final Approval — `approve` command, re-extract to see status change

See `design.md#phase-5-operator-guide` for section-by-section implementation notes and corrected commands.

### Validation

**Manual — execute each key command from the guide against concept 01:**
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status 01` → Shows concept state
- [ ] `uv run python exploration/concept_explorer/extract_explorer_data.py --concepts 01 --skip-narrative` → Extracts successfully
- [ ] `uv run python exploration/concept_explorer/server.py` → Starts, concept 01 visible
- [ ] Verify all other commands in the guide have correct syntax (flags, argument order) by checking `--help` output
- [ ] Commit: `docs: add operator guide for concept analysis → explorer → approval workflow`

**What We Know Works After Phase 4:**
- Complete, copy-pasteable documentation for human operators
- Every command verified against the live system

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Run explorer tests after each commit in the worktree. If CAS22 test updates are extensive, grep for all `CAS22` references before committing.
- **Phase 2**: If `uv lock` fails, check for version constraint conflicts between pipeline and explorer deps. Relax bounds if needed (e.g., fastapi, uvicorn).
- **Phase 3**: If any explorer test imports from the relocated files, grep for import paths before committing. (Unlikely — design docs aren't imported.)
- **Phase 4**: If a command's behavior has changed since the research phase, re-run with `--help` to verify current flags.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-04-06
**Actual Changes:**
- 1.1: Fixed CAS22_NAMES in both `models.py` (14→18 entries, 6 corrected labels, 4 new keys) AND `static/js/cas_breakdown.js` (same fix — design didn't mention this duplicate, caught by grep)
- 1.2: Moved playwright to `[project.optional-dependencies] e2e`, added `importorskip` guards, updated PLAYWRIGHT_GUIDE.md. `uv sync` confirmed playwright uninstalled.
- 1.3: Archived 10 explorer work items (7 from plan + 3 additional: automated-concept-analysis, iterative-analysis-loop, constraint-atms-spike)
- Validation: 148 tests passed, 2 playwright files skipped cleanly

**Issues:**
- Explorer tests require `PYTHONPATH=.` — no pytest path config in explorer's pyproject.toml. Pre-existing issue, will need fixing in merged pyproject.toml (add `[tool.pytest.ini_options] pythonpath = ["."]`).

**Deviations:**
- Also fixed `cas_breakdown.js` (not in plan/design) — had identical corrupted CAS22 labels
- Archived 10 items instead of 7 (plan missed automated-concept-analysis, iterative-analysis-loop, constraint-atms-spike)
- `C220108` label changed from "Fuel Handling & Target Factory" to "Divertor / Target Factory" (matching costingfe)

### Phase 2 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 3 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

### Phase 4 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete
