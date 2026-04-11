# Design: Merge Concept Explorer and Write Operator Guide

**Status**: Draft
**Owner**: Reid W
**Created**: 2026-04-06
**Updated**: 2026-04-06
**Branch**: `design-space-explore`
**Commit**: `7b34e8b`

## Overview

Merge the `ralph/concept-explorer` branch (40 commits, 103 files — FastAPI explorer UX) into `design-space-explore` (24 commits — analysis pipeline improvements), resolve all conflicts, fix interface gaps between pipeline output and explorer input, and write an operator guide for the end-to-end concept approval workflow.

## Related Artifacts

- **Spec**: `.project/active/explorer-merge/spec.md`
- **Explorer README**: `exploration/concept_explorer/README.md` (on explorer branch)
- **Explorer design docs**: `DESIGN.md`, `DESIGN_v1.md` (on explorer branch)
- **Pipeline manage-concept**: `.claude/commands/manage-concept.md`
- **Batch pipeline plan**: `.project/active/batch-pipeline-run/plan.md`

## Research Findings

### Merge Landscape

- **Common ancestor**: `5049c71`
- **40 commits** on `ralph/concept-explorer` not on `design-space-explore`
- **24 commits** on `design-space-explore` not on `ralph/concept-explorer`
- **103 files changed** between branches (by diff stat)

### Conflict Zone Analysis

Seven files have changes on both sides. Research revealed the exact contents of each:

**1. `pyproject.toml`** — HIGH conflict. Branches have divergent project names (`fusion-tea` vs `ralph-project`), different Python version floors (`>=3.12` vs `>=3.11`), non-overlapping dependency lists, and different tool configs. Explorer adds ruff/mypy configs and a `[dependency-groups]` section with playwright.

**2. `.gitignore`** — MEDIUM conflict. Explorer rewrote it to a minimal form (lost all `.claude/`, `modeling_project/`, `work/` gitignore entries that the pipeline needs). Explorer adds useful entries: `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `exploration/concept_explorer/data/`, `exploration/concept_explorer/dist/`.

**3. `tests/conftest.py`** — LOW conflict. Explorer's version is a 2-line stub (`import pytest`). Pipeline's version has real fixtures (`models_dir`, `load_sysml`). Keep pipeline's version entirely.

**4. `.project/CURRENT_WORK.md`** — LOW conflict. Both branches updated independently. Take pipeline's current version, add explorer status note.

**5. `.project/completed/CHANGELOG.md`** — LOW conflict. Both branches added entries. Concatenate chronologically.

**6. `uv.lock`** — AUTO-RESOLVE. Delete both, regenerate after `pyproject.toml` merge.

**7. `src/concept_explorer/__init__.py`** — NO real conflict. Inert scaffold file, exists only on explorer branch.

### CAS22 Label Corruption (Critical Finding)

The explorer's `CAS22_NAMES` dict in `models.py` has **wrong labels** for accounts C220200–C220700, not just missing keys. The explorer maps:
- `C220200` → "Maintenance Equipment" (actually: **Main & Secondary Coolant**)
- `C220300` → "Remote Handling & Hot Cell" (actually: **Auxiliary Cooling & Cryoplant**)
- `C220400` → "Instrumentation & Control" (actually: **Radioactive Waste Management**)
- `C220500` → "Plasma / Feedback Control" (actually: **Fuel Handling & Storage**)
- `C220600` → "Cryogenic Cooling System" (actually: **Other Reactor Plant Equipment**)
- `C220700` → "Neutron Source & Moderator" (actually: **Instrumentation & Control**)

Plus 4 missing keys: `C220109` (Direct Energy Converter), `C220110` (Remote Handling & Maintenance Equipment), `C220111` (Installation Labor), `C220112` (Isotope Separation Plant).

Source of truth: `costingfe/layers/cas22.py:316-336` at `~/1cfe/1costingfe`.

### Path Resolution

All explorer paths are computed relative to `__file__` — no hardcoded absolute paths:
- `extract_explorer_data.py:30-33`: `_ANALYSES_DIR = Path(__file__).parent.parent / "concept_analysis" / "analyses"` — resolves to `exploration/concept_analysis/analyses/`, which is correct post-merge.
- `server.py:68,498-507`: `BASE_DIR = Path(__file__).parent` — all data/templates/static paths relative to this. Correct post-merge.
- Server default port: **8421** (not 8000 as spec stated).

### Script Path Correction

The spec uses `scripts/run_analysis.py` but the actual path is **`exploration/concept_analysis/scripts/run_analysis.py`**. All operator guide commands must use the correct path.

### Playwright Usage

Playwright is used in exactly 2 files:
- `exploration/concept_explorer/tests/test_views_manual.py` (640 lines, 16 tests)
- `exploration/concept_explorer/tests/test_integration_manual.py` (561 lines, 12 tests)

Both import `from playwright.sync_api import sync_playwright, Page` at module level. Neither is collected by pytest automatically (no `test_` prefix pattern match issue — they ARE named `test_*` so pytest WILL collect them). They need skip guards.

### Explorer `.project/active/` Items

The explorer branch has 7 items in `.project/active/` that represent completed explorer work:
- `compare-shell/` — completed (comparison page shell)
- `concept-id-unification/` — completed (unified concept IDs)
- `explorer-integration/` — completed (wiring selection tray to comparison)
- `explorer-ux-v2/` — completed (epic concept doc)
- `selection-tray/` — completed (taxonomy selection tray)
- `views-capex-sensitivity/` — completed (CapEx + Sensitivity views)
- `views-categorical-summary/` — completed (Categorical + Summary views)

These overlap with pipeline's active items: `batch-pipeline-run`, `feedback-routing-fix`, `orig-md-research`, `source-replacement`, `traceability-system`.

---

## Proposed Design

### Phase 1: Pre-Merge Preparation

Before running `git merge`, prepare the target branch to minimize conflict surface.

#### Step 1.1: Stage Explorer Work Item Archives

On the `ralph/concept-explorer` branch (in the worktree), move completed work items:

```
.project/active/compare-shell/        → .project/completed/20260404_compare-shell/
.project/active/selection-tray/        → .project/completed/20260404_selection-tray/
.project/active/views-capex-sensitivity/ → .project/completed/20260404_views-capex-sensitivity/
.project/active/views-categorical-summary/ → .project/completed/20260404_views-categorical-summary/
.project/active/explorer-integration/  → .project/completed/20260404_explorer-integration/
.project/active/explorer-ux-v2/        → .project/completed/20260404_explorer-ux-v2/
.project/active/concept-id-unification/ → .project/completed/20260404_concept-id-unification/
```

Commit this on the explorer branch. This eliminates `.project/active/` collision with pipeline items.

**Rationale**: Doing this pre-merge (on the source branch) produces a clean merge where `.project/active/` contains only pipeline items. Doing it post-merge would require manual cleanup of a merged directory.

#### Step 1.2: Fix CAS22_NAMES on Explorer Branch

Replace the corrupted `CAS22_NAMES` dict in `exploration/concept_explorer/models.py` with the authoritative mapping from costingfe before merging. This keeps the fix atomic and reviewable.

New dict (18 entries, matching `costingfe/layers/cas22.py:316-336`):

```python
CAS22_NAMES: ClassVar[dict[str, str]] = {
    "C220101": "First Wall & Blanket",
    "C220102": "Radiation Shield",
    "C220103": "Magnets / Coils",
    "C220104": "Heating & Driver Systems",
    "C220105": "Primary Structure & Support",
    "C220106": "Vacuum System",
    "C220107": "Power Conditioning & Energy Storage",
    "C220108": "Divertor / Target Factory",
    "C220109": "Direct Energy Converter",
    "C220110": "Remote Handling & Maintenance Equipment",
    "C220111": "Installation Labor",
    "C220112": "Isotope Separation Plant",
    "C220200": "Main & Secondary Coolant",
    "C220300": "Auxiliary Cooling & Cryoplant",
    "C220400": "Radioactive Waste Management",
    "C220500": "Fuel Handling & Storage",
    "C220600": "Other Reactor Plant Equipment",
    "C220700": "Instrumentation & Control",
}
```

Also update `from_forward_result()` in `CostModelData` to iterate all keys in `CAS22_NAMES` (it already does — confirm no hardcoded subset).

Update any tests that assert on CAS22 label values.

#### Step 1.3: Make Playwright Optional on Explorer Branch

In the explorer's `pyproject.toml`:
- Remove `playwright` from `[dependency-groups] dev`
- Add `[project.optional-dependencies] e2e = ["playwright>=1.58.0"]`

In both test files, add a module-level skip guard at the top (after docstring, before other imports):

```python
import pytest
pytest.importorskip("playwright", reason="playwright not installed — install with: uv sync --extra e2e && playwright install chromium")

from playwright.sync_api import sync_playwright, Page  # noqa: E402
```

Update `PLAYWRIGHT_GUIDE.md` first section to note:
```
Playwright is an optional dependency. Install with:
  uv sync --extra e2e
  playwright install chromium
```

Commit on explorer branch.

### Phase 2: Git Merge

#### Step 2.1: Merge with Manual Resolution

```bash
git merge ralph/concept-explorer --no-commit
```

Resolve each conflict file:

| File | Action |
|------|--------|
| `pyproject.toml` | See Phase 2.2 below |
| `.gitignore` | See Phase 2.3 below |
| `tests/conftest.py` | `git checkout design-space-explore -- tests/conftest.py` (keep ours) |
| `.project/CURRENT_WORK.md` | `git checkout design-space-explore -- .project/CURRENT_WORK.md` then manually append explorer section |
| `.project/completed/CHANGELOG.md` | Concatenate chronologically from both |
| `uv.lock` | `git rm uv.lock` (regenerate later) |

#### Step 2.2: pyproject.toml Merged Content

Keep `fusion-tea` identity and pipeline's full dependency list. Add explorer-only dependencies. Add explorer tool configs. Keep `requires-python = ">=3.12"` (pipeline's minimum; explorer works fine at 3.12+).

Structure of merged file:

```toml
[project]
name = "fusion-tea"
version = "0.1.0"
description = "Fusion Techno-Economic Analysis"
requires-python = ">=3.12"
dependencies = [
    # Pipeline dependencies (existing)
    "agentic-mbse[extract-full,web]",
    "costingfe",
    "sysml-codegen",
    "teax-simkit",
    "pytest>=8.0",
    "fastapi>=0.128.0",
    "uvicorn[standard]>=0.42.0",
    "httpx>=0.28.1",
    "matplotlib>=3.10.8",
    "numpy>=2.4.0",
    "pyzotero>=1.10.0",
    "python-dotenv>=1.2.1",
    "graphviz>=0.21",
    # Explorer additions
    "jinja2>=3.1.6",
    "pydantic>=2",
    "pyyaml>=6.0.3",
]

[project.optional-dependencies]
e2e = ["playwright>=1.58.0"]

[dependency-groups]
dev = ["mypy>=1.10", "ruff>=0.4", "types-pyyaml"]

[tool.uv.sources]
costingfe = { path = "../1costingfe", editable = true }
teax-simkit = { path = "../teax-simkit", editable = true }
agentic-mbse = { path = "../agentic-mbse", editable = true }
sysml-codegen = { path = "../sysml-codegen", editable = true }

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.mypy]
python_version = "3.12"
warn_return_any = true
warn_unused_configs = true
```

**Notes**:
- `fastapi` version: pipeline has `>=0.128.0`, explorer has `>=0.135.2`. Keep pipeline's lower bound (uv resolves to latest anyway).
- `uvicorn`: pipeline has `>=0.40.0`, explorer has `[standard]>=0.42.0`. Use `[standard]` extra (adds watchfiles, etc.) with pipeline's lower bound.
- `pytest`: already in pipeline deps, no need to duplicate.
- `httpx`: already in pipeline deps.
- Python target in ruff/mypy: bump to 3.12 to match `requires-python`.

#### Step 2.3: .gitignore Merged Content

```gitignore
# Python
__pycache__/
*.py[cod]
build/
dist/
wheels/
*.egg-info/
.venv/
.env
.mypy_cache/
.pytest_cache/
.ruff_cache/
.DS_Store

# Tool-owned files (managed by agentic-mbse init --dev)
.claude/commands/
.claude/agents/
.claude/skills/
.claude/hooks/
modeling_project/MODELING_GUIDE.md
modeling_project/MODELING_PROCESS.md
work/EPIC_GUIDE.md
work/backlog/epic_template.md
.claude/.tool-hashes.json

# Project-specific
knowledge/LOCAL_SOURCES.yaml

# Explorer generated data (re-extracted on demand)
exploration/concept_explorer/data/
exploration/concept_explorer/dist/
```

#### Step 2.4: CURRENT_WORK.md Update

Keep pipeline's current version. Append a section:

```markdown
### Concept Explorer (merged from ralph/concept-explorer)

**Status**: Merged, functional
**Location**: `exploration/concept_explorer/`
**Branch**: Merged into `design-space-explore` from `ralph/concept-explorer`

4-page interactive explorer (Index, Concept Profile, Comparison, Taxonomy) with FastAPI backend. 
Extracts data from pipeline artifacts. 140+ tests. See `exploration/concept_explorer/README.md`.
```

#### Step 2.5: Regenerate Lock File

After all conflict resolution:

```bash
git checkout --theirs uv.lock 2>/dev/null; rm -f uv.lock
uv lock
uv sync
```

#### Step 2.6: Commit

```bash
git add -A
git commit -m "Merge concept explorer into analysis pipeline branch"
```

### Phase 3: Post-Merge Verification

Run these checks in order:

1. **Pipeline smoke test**:
   ```bash
   uv run python exploration/concept_analysis/scripts/run_analysis.py list
   ```
   Expected: 38 concepts listed.

2. **Explorer test suite**:
   ```bash
   uv run pytest exploration/concept_explorer/tests/ -x -v
   ```
   Expected: All non-playwright tests pass. Playwright tests skip with clear message.

3. **Extraction test**:
   ```bash
   uv run python exploration/concept_explorer/extract_explorer_data.py --concepts 01
   ```
   Expected: Produces `exploration/concept_explorer/data/01.json`, `manifest.json`, `parameter_index.json`.

4. **Server test**:
   ```bash
   uv run python exploration/concept_explorer/server.py
   ```
   Expected: Starts on `http://127.0.0.1:8421`. Index page loads with at least concept 01.

### Phase 4: Explorer Design Artifact Relocation

The explorer branch has several top-level design documents that are explorer-specific and clutter the repo root:

| File | Action |
|------|--------|
| `DESIGN.md` | Move to `exploration/concept_explorer/docs/DESIGN.md` |
| `DESIGN_v1.md` | Move to `exploration/concept_explorer/docs/DESIGN_v1.md` |
| `DESIGN_REVIEW.md` | Move to `exploration/concept_explorer/docs/DESIGN_REVIEW.md` |
| `IMPLEMENTATION_PLAN_v1.md` | Move to `exploration/concept_explorer/docs/IMPLEMENTATION_PLAN_v1.md` |
| `AGENTS.md` | Move to `exploration/concept_explorer/docs/AGENTS.md` |
| `PROMPT_build.md` | Move to `exploration/concept_explorer/docs/PROMPT_build.md` |
| `PROMPT_plan.md` | Move to `exploration/concept_explorer/docs/PROMPT_plan.md` |
| `specs/` (12 files) | Move to `exploration/concept_explorer/docs/specs/` |
| `loop.sh` | Move to `exploration/concept_explorer/` or delete if no longer needed |
| `src/concept_explorer/__init__.py` | Delete (inert scaffold, real code is in `exploration/concept_explorer/`) |
| `tests/__init__.py` | Keep if needed for test discovery, otherwise delete |

Commit as a separate cleanup commit after verification passes.

### Phase 5: Operator Guide

Write `exploration/concept_analysis/OPERATOR_GUIDE.md` following the 7-section structure from the spec, with these corrections and details from research:

**Key corrections from spec**:
- Script path: `exploration/concept_analysis/scripts/run_analysis.py` (not `scripts/run_analysis.py`)
- Server port: `8421` (not `8000`)
- Extraction command: `uv run python exploration/concept_explorer/extract_explorer_data.py` (direct script invocation, not `-m` module)
- `--concepts` flag on extraction (not `--concept`)

**Section-by-section implementation notes**:

**Section 1 (Pipeline Quick Reference)**: Use the exact CLI from the argparse research. All commands share: `uv run python exploration/concept_analysis/scripts/run_analysis.py <command> <concept-id> [flags]`. Include the key commands: `status`, `stage1-all`, `add-source`, `review`, `address-review`, `synthesize`, `approve`. Note common flags: `--model`, `--dry-run`, `--timeout`, `--force`, `--research`, `--max-passes`, `--resume`.

**Section 2 (Launching the Explorer)**: Document the two-step process:
1. Extract: `uv run python exploration/concept_explorer/extract_explorer_data.py [--concepts ID ...]`
   - Options: `--skip-narrative` (skip Claude-based narrative extraction), `--concepts` (specific IDs)
   - Produces JSON in `exploration/concept_explorer/data/`
2. Serve: `uv run python exploration/concept_explorer/server.py [--port PORT]`
   - Default: `http://127.0.0.1:8421`
   - Prerequisite: at least one concept must have `model_setup.py`

**Section 3 (Explorer Tour)**: Per spec, walk through each page. Add specific "red flag" checklist items for each page that operators should verify. Note that concepts without `model_setup.py` will show limited data (no tornado, no CAS breakdown, no sliders).

**Section 4 (Issue Triage)**: Document `/manage-concept` invocation and the 4 modes (A-D). Emphasize: never edit `analysis.md` directly. Change requests go through `change_requests.md` → `analyze --feedback`.

**Section 5 (Adding Sources)**: `add-source` command, then `stage1-all --resume` to re-analyze with the new source. Note that source extraction uses agentic-mbse and may cost $5-50 depending on document size.

**Section 6 (Review → Synthesis)**: The full PROCEED/REVISE flow. Emphasize the gate: synthesis requires `Review-Status` in {addressed, clean, proceed}.

**Section 7 (Approval)**: `approve` command. Note the `--force` flag for approving without synthesis. After approval, re-extract to see the concept move to "Approved" in the explorer.

**Tone**: Direct, task-oriented. Commands are copy-pasteable. No assumed knowledge of pipeline internals. Include a "Typical Workflow" diagram at the top showing the happy path.

---

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| `uv lock` fails with conflicting version constraints | Medium | Blocks merge | Regenerate from scratch; if constraints conflict, relax version bounds |
| Explorer tests fail post-merge due to import path changes | Low | Blocks verification | Explorer paths are `__file__`-relative, unlikely to break |
| CAS22 fix breaks existing explorer test assertions | Medium | Requires test updates | Update test assertions alongside the fix (Phase 1.2) |
| costingfe path `../1costingfe` doesn't resolve from merged repo | Low | Server won't start | Both branches use same UV source; path is relative to repo root |
| Explorer's `_manual.py` tests collected by pytest without playwright | High | Test suite crashes on import | Phase 1.3 adds `importorskip` guards — must be done before merge |
| Top-level files from explorer (`DESIGN.md`, `specs/`, etc.) confuse contributors | Medium | Navigability | Phase 4 relocates them under `exploration/concept_explorer/docs/` |

## Integration Strategy

The merge creates a single-repo, two-system architecture:

```
exploration/
├── concept_analysis/          # PIPELINE: produces artifacts
│   ├── scripts/run_analysis.py
│   ├── analyses/{id}/         # Per-concept artifacts
│   └── ...
└── concept_explorer/          # EXPLORER: visualizes artifacts
    ├── extract_explorer_data.py  # Bridge: reads analyses/, writes data/
    ├── server.py                 # Serves UX
    ├── models.py                 # Pydantic data models
    └── ...
```

The **extraction script** is the bridge: it reads from `../concept_analysis/analyses/` (relative to its own location) and writes to `./data/`. This path resolves correctly because both directories are siblings under `exploration/`.

The **operator guide** documents the human loop: pipeline → extract → explore → identify issues → `/manage-concept` → re-run pipeline → re-extract → verify.

## Validation Approach

**Phase 1 (pre-merge fixes)**: Each fix committed separately on the explorer branch. Run `uv run pytest exploration/concept_explorer/tests/ -x` after each commit in the worktree.

**Phase 2 (merge)**: `git merge --no-commit` to preview conflicts. Resolve per design. `uv lock && uv sync` to verify dependency resolution.

**Phase 3 (post-merge)**: Four-step verification (pipeline smoke test, explorer tests, extraction test, server test) as detailed above.

**Phase 4 (relocation)**: `git mv` for each file. Re-run tests to confirm no path breakage.

**Phase 5 (operator guide)**: Manual walkthrough — execute each command in the guide against a real concept (e.g., concept 01 which has `model_setup.py`).

---

Next Step: After approval → `/_my_plan` for phased execution with checkboxes.
