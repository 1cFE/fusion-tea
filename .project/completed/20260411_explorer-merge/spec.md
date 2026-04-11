# Spec: Merge Concept Explorer and Write Operator Guide

**Status**: Draft
**Owner**: Reid
**Created**: 2026-04-06
**Complexity**: Standard
**Branch**: `design-space-explore` (target), `ralph/concept-explorer` (source)

---

## Context

Two parallel development streams have been running on separate branches of the same repo:

- **`design-space-explore`** (24 commits ahead): Analysis pipeline — iterative analysis loop with convergence tracking, autonomous source acquisition, PROCEED/REVISE review, `/manage-concept` interactive command, cross-concept memory, feedback routing fixes, batch pipeline orchestration.
- **`ralph/concept-explorer`** (40 commits ahead): Concept Explorer UX — FastAPI server, Pydantic data models, data extraction pipeline, 4-page interactive frontend (Index, Concept Profile, Comparison, Taxonomy), sensitivity tornado charts, CAS breakdown, similarity engine, selection tray, live recompute via costingfe.

They share a common ancestor (`5049c71`) and diverge across 103 changed files. The explorer worktree lives at `~/1cfe/fusion-tea_concept-explorer`.

These two systems form a closed loop: the pipeline produces analysis artifacts, the explorer extracts and visualizes them, and operator review via the explorer feeds back into the pipeline via `/manage-concept`. This work item merges them and documents the end-to-end operator workflow.

---

## Scope

### In Scope

1. **Git merge** of `ralph/concept-explorer` into `design-space-explore`
2. **Conflict resolution** across known conflict zones
3. **Interface gap remediation** — ensure pipeline outputs match explorer inputs
4. **Operator guide** — write-up for taking a concept from partially-run through approval

### Out of Scope

- Running the batch pipeline on remaining concepts (separate work item)
- Implementing `model_metadata.yaml` generation (enhancement, not blocker)
- Narrative extraction via `claude -p` (optional feature, already works)
- E2E Playwright test automation
- Explorer feature development (taxonomy enhancements, new views, etc.)

---

## Deliverables

### D1: Clean Merge

Merge `ralph/concept-explorer` into `design-space-explore` with all conflicts resolved.

**Known Conflict Zones** (7 files with both-sides changes):

| File | Resolution Strategy |
|------|-------------------|
| `pyproject.toml` | Manual merge — keep `fusion-tea` as project name, merge dependency lists (pipeline needs `agentic-mbse`, `pyzotero`, `matplotlib`, etc.; explorer needs `fastapi`, `jinja2`, `pydantic`, `uvicorn`, `pyyaml`, `costingfe`). Retain `requires-python = ">=3.12"`. |
| `.gitignore` | Manual merge — keep pipeline's tool-owned gitignore entries (`.claude/commands/`, `modeling_project/MODELING_GUIDE.md`, etc.) AND add explorer's data/dist gitignore entries (`exploration/concept_explorer/data/`, `exploration/concept_explorer/dist/`). |
| `.project/CURRENT_WORK.md` | Take `design-space-explore` version (current), then append explorer status section. |
| `.project/completed/CHANGELOG.md` | Concatenate entries from both branches chronologically. |
| `tests/conftest.py` | Both branches modified — merge fixtures from both. |
| `uv.lock` | Regenerate after `pyproject.toml` merge via `uv lock`. |
| `src/concept_explorer/__init__.py` | Keep (inert scaffold from explorer, no conflict). |

**Non-conflicting additions** (explorer-only, clean merge):
- `exploration/concept_explorer/` — entire explorer package (models, server, extraction, similarity, templates, static assets, tests)
- `specs/` — 12 explorer spec documents
- `DESIGN.md`, `DESIGN_v1.md`, `DESIGN_REVIEW.md`, `IMPLEMENTATION_PLAN_v1.md` — explorer design artifacts
- `.project/active/` and `.project/completed/` — explorer work items (6 active, 5 completed)

**Acceptance Criteria**:
- [ ] `git merge` completes without unresolved conflicts
- [ ] `uv lock` succeeds with merged dependencies
- [ ] `uv run pytest exploration/concept_explorer/tests/` passes (explorer tests)
- [ ] `uv run python scripts/run_analysis.py list` works (pipeline still functional)
- [ ] Explorer server starts: `uv run python -m exploration.concept_explorer.server` or equivalent

### D2: Interface Gap Remediation

Ensure the pipeline's output artifacts satisfy the explorer's extraction requirements. Gaps identified:

#### Gap 1: CAS22 Sub-Account Key Mismatch

**Problem**: Pipeline's `model_setup.py` files produce CAS22 keys `C220109` (DEC), `C220111` (Installation), `C220112` (Isotope Separation) that are missing from the explorer's `CAS22_NAMES` mapping in `models.py`. The explorer silently drops these sub-accounts.

**Fix**: Add the missing keys to `CAS22_NAMES` in `exploration/concept_explorer/models.py`.

**Acceptance Criteria**:
- [ ] All CAS22 sub-account keys produced by costingfe are represented in `CAS22_NAMES`
- [ ] Existing tests updated to cover new keys

#### Gap 2: Extraction Path Configuration

**Problem**: The extraction script hardcodes `../../concept_analysis/analyses/` as the relative path to pipeline artifacts. After merge, both live in the same repo and the path should resolve correctly, but this needs verification.

**Fix**: Verify the path resolves correctly post-merge. If not, make the analyses directory configurable via CLI argument or environment variable.

**Acceptance Criteria**:
- [ ] `uv run python -m exploration.concept_explorer.extract_explorer_data` successfully discovers and extracts at least one concept with a `model_setup.py`

#### Gap 3: Playwright Dependency Must Be Optional

**Problem**: The explorer branch lists `playwright>=1.58.0` in dev dependencies. Playwright downloads full browser binaries (~40MB+), is heavyweight, and poses a security surface we don't want as a default dependency.

**Fix**:
- Move `playwright` to a separate optional extra (e.g., `[e2e]`) in `pyproject.toml`, not in `[dev]`
- Add `pytest.importorskip("playwright")` (or equivalent top-of-module skip) in `test_views_manual.py` and `test_integration_manual.py` so they skip cleanly when playwright is absent
- Update `PLAYWRIGHT_GUIDE.md` to note the install command: `uv add --optional e2e playwright && playwright install chromium`

**Acceptance Criteria**:
- [ ] `uv sync` (without `--extra e2e`) does NOT install playwright
- [ ] `uv run pytest exploration/concept_explorer/tests/` skips playwright tests with a clear skip message (not import errors)
- [ ] `uv sync --extra e2e` installs playwright for developers who want E2E tests

#### Gap 4: Explorer .project Cleanup

**Problem**: The explorer branch has its own `.project/active/` work items (e.g., `explorer-integration`, `selection-tray`, `views-capex-sensitivity`, `compare-shell`, `concept-id-unification`, `explorer-ux-v2`, `views-categorical-summary`) that reflect completed explorer work. These will collide with or clutter the pipeline's `.project/` state.

**Fix**: Archive completed explorer work items to `.project/completed/` with appropriate date prefixes. Keep `concept-id-unification` if still relevant to both systems.

**Acceptance Criteria**:
- [ ] No stale explorer work items in `.project/active/` post-merge
- [ ] `concept-id-unification` status assessed and handled appropriately

### D3: Operator Guide

A write-up in `exploration/concept_analysis/OPERATOR_GUIDE.md` documenting the end-to-end workflow for taking a concept from partial analysis through explorer-based review to approval.

**Target audience**: Human operators who will run the pipeline and review results.

**Required sections**:

#### Section 1: Pipeline Quick Reference

- How to check concept status: `uv run python scripts/run_analysis.py status <concept-id>`
- How to run additional analysis iterations: `uv run python scripts/run_analysis.py stage1-all <concept-id> [--research] [--max-passes N]`
- How to resume after failure: `uv run python scripts/run_analysis.py stage1-all <concept-id> --resume`
- How to add a source: `uv run python scripts/run_analysis.py add-source <concept-id> <path-or-url>`
- How to trigger review: `uv run python scripts/run_analysis.py review <concept-id>`

#### Section 2: Launching the Explorer

- Prerequisites: at least one concept must have `model_setup.py` (state >= `model-setup`)
- Data extraction: `uv run python -m exploration.concept_explorer.extract_explorer_data [--concepts ID1 ID2 ...]`
- Starting the server: `uv run python -m exploration.concept_explorer.server` (or `uvicorn` command)
- URL: `http://localhost:8000`

#### Section 3: Explorer Tour — Sanity-Checking a Concept

Walk through each page with guidance on what to look for:

**Index Page** (`/`):
- Two sections: "Approved" (green) and "In Progress" (amber)
- Each card shows: concept name, confinement family badge, company, LCOE, confidence
- New concepts appear under "In Progress" until explicitly approved
- Quick scan: does the LCOE look plausible? Is the confinement family correct?

**Concept Profile** (`/concept/{id}`):
- Hero section: name, family, company — verify basic metadata
- Headline Economics: LCOE, overnight cost, P_net, Q_eng, capacity factor — are these physically reasonable?
- Narrative: key bets, eliminated costs, novel costs — does the thesis make sense?
- Risk table: are risks well-characterized with retirement paths?
- Tornado chart: sensitivity bars ranked by elasticity — which parameters dominate? Are the ranges reasonable?
- CAS breakdown: stacked bar with expandable CAS22 — does the cost structure match expectations for this concept type?
- Sliders (costingfe concepts): adjust parameters to see LCOE response in real-time

**Comparison Page** (`/compare`):
- Select 2-3 concepts from the same confinement family
- Integrated mode: side-by-side with independent view selectors
- Landscape mode: grid layout with unified view
- Four views: Categorical (taxonomy attributes), Summary (LCOE drivers), CapEx (CAS stacked bars), Sensitivity (tornado overlays)
- Use this to cross-check: does a tokamak's cost structure look similar to other tokamaks? Are outliers justified?

**Taxonomy Page** (`/taxonomy`):
- Decision tree (left): collapsible classification hierarchy
- Constellation (center): 2D scatter of all 38 concepts by similarity — are clusters sensible?
- Neighborhood graph: double-click a concept to see its nearest neighbors
- Selection tray (bottom): collect concepts for comparison, then click "Compare"
- Use this to verify: is the concept classified correctly? Who are its neighbors?

#### Section 4: Issue Triage via `/manage-concept`

- When the explorer reveals issues (wrong LCOE, missing risks, misclassified taxonomy), use `/manage-concept <concept-id>` in Claude Code
- The command loads context and presents stage-appropriate options
- **For reviewed concepts (Mode B)**: Walk through PA-N proposed actions, fill Decision fields
- **For drafted concepts (Mode A)**: Identify bets and flags, write change requests
- Change requests are written to `change_requests.md` — never edit `analysis.md` directly
- Apply changes: `uv run python scripts/run_analysis.py stage1-all <concept-id> --resume --feedback change_requests.md`

#### Section 5: Adding Sources Mid-Review

- If the explorer reveals a data gap (e.g., missing CAS account detail, uncertain parameter):
  1. Find the source (paper, report, vendor data)
  2. `uv run python scripts/run_analysis.py add-source <concept-id> <path-or-url>`
  3. Re-run analysis: `uv run python scripts/run_analysis.py stage1-all <concept-id> --resume`
  4. Re-extract explorer data and refresh

#### Section 6: Final Review, Feedback, and Synthesis

- Once satisfied with the analysis via explorer review:
  1. **Review**: `uv run python scripts/run_analysis.py review <concept-id>` — produces PROCEED or REVISE verdict
  2. **If REVISE**: `uv run python scripts/run_analysis.py stage1-all <concept-id> --resume` (review findings become feedback, one-shot)
  3. **If PROCEED with actions**: Fill PA-N Decisions in `review.md` (via `/manage-concept` or editor), then `uv run python scripts/run_analysis.py address-review <concept-id>`
  4. **If PROCEED clean**: Skip to synthesis
  5. **Synthesize**: `uv run python scripts/run_analysis.py synthesize <concept-id>` — generates editorial synthesis
  6. **Re-extract** explorer data to verify final state in the UX

#### Section 7: Final Approval

- Prerequisites: PROCEED review + synthesis complete
- Command: `uv run python scripts/run_analysis.py approve <concept-id>`
- This sets `Status: approved` in `analysis.md` and `synthesis.md` frontmatter
- Re-extract explorer data — concept moves from "In Progress" to "Approved" on the index page
- The approved analysis joins the reuse pool for future concepts

**Acceptance Criteria**:
- [ ] Guide covers all 7 sections above
- [ ] Commands are copy-pasteable (correct paths, flags, argument order)
- [ ] Guide references actual file paths and command names from the codebase
- [ ] No assumptions about reader's prior knowledge of the pipeline internals
- [ ] Reviewed for accuracy against current pipeline commands (run_analysis.py --help)

---

## Known Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| `uv.lock` conflicts are notoriously messy | Merge blocker | Regenerate from scratch after pyproject.toml merge |
| Explorer's `pyproject.toml` uses `name = "ralph-project"` and `requires-python = ">=3.11"` | Dependency resolution issues | Take pipeline's project name and Python version, merge dep lists |
| costingfe local path dependency (`../1costingfe`) may differ | Server startup failure | Verify path, adjust if needed |
| Explorer `.project/` state may conflict with pipeline `.project/` state | Confusing project management | Archive explorer work items before merge |
| CAS22 key mismatch causes silent data loss in tornado charts | Incorrect visualizations | Fix `CAS22_NAMES` mapping (Gap 1) |
| 34 of 38 concepts lack `model_setup.py` — explorer will show mostly "In Progress" cards with limited data | Poor first impression | Expected; guide should set expectations about progressive population |

---

## Dependencies

- `costingfe` library must be accessible at the expected path (`../1costingfe` or equivalent)
- Pipeline must be functional on `design-space-explore` (verified: `run_analysis.py list` works)
- Explorer tests depend on `pytest`, `httpx`, `ruff` (added via merged pyproject.toml)

---

## Verification Plan

1. **Pre-merge**: Dry-run merge to identify all conflicts (`git merge --no-commit ralph/concept-explorer`)
2. **Merge**: Resolve conflicts per D1 strategy, commit
3. **Lock**: `uv lock` and `uv sync` with merged dependencies
4. **Pipeline smoke test**: `uv run python scripts/run_analysis.py list` (38 concepts listed)
5. **Explorer test suite**: `uv run pytest exploration/concept_explorer/tests/ -x`
6. **Extraction test**: `uv run python -m exploration.concept_explorer.extract_explorer_data --concepts 01` (at least one concept with model_setup.py)
7. **Server test**: Start server, load index page, navigate to a concept profile
8. **Guide review**: Verify all commands in the operator guide execute successfully
