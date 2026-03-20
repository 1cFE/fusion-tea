# Implementation Plan: Automated Concept Analysis

**Status:** Draft
**Created:** 2026-03-20
**Last Updated:** 2026-03-20

## Source Documents
- **Concept:** `.project/concepts/automated-concept-analysis.md`
- **Design:** `.project/active/automated-concept-analysis/design.md` ← See here for component details, CLI design, data model, prompt templates

## Implementation Strategy

**Phasing Rationale:** Action-first and iterative. Each phase ends with a real test — running the pipeline on actual concepts. Pieces not needed yet get `#TODO` + `NotImplementedError` stubs. The design is ~80% solid; the remaining 20% will be discovered through testing. Design doc gets updated as we learn.

**Overall Validation Approach:**
- No formal test suite — process execution IS the test
- Each phase has a concrete CLI invocation that validates the work
- Iterate on prompts and templates based on real output quality

---

## Phase 1: Skeleton + `status` + `list`

### Goal
Working CLI with argparse, table loading, concept ID resolution, filesystem state scanning, and the two read-only commands. No Claude calls. This validates the data model foundation.

### Changes Required

**See `design.md` for:**
- CLI subcommand design → `design.md#cli-design`
- Concept ID resolution logic → `design.md#cli-design` (resolve_concepts)
- Data model / state detection → `design.md#data-model`
- Output directory structure → `design.md#output-structure`

**Specific file changes:**

#### 1. Script
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (NEW)
- [x] Create with argparse entry point, subcommand dispatch
- [x] `load_table()` — read `table.csv`, return list of concept dicts with ID, name, company, family
- [x] `resolve_concepts()` — map CLI args (01, 17a, --all, --family) to concept IDs
- [x] `get_concept_state()` — check `analyses/{id}/` for gap_report.md, analysis.md, frontmatter Status
- [x] `parse_frontmatter()` — extract YAML frontmatter from markdown files
- [x] `cmd_list()` — print all 38 concepts with IDs
- [x] `cmd_status()` — print status table (ID, name, state)
- [x] Stub remaining subcommands with `#TODO` / `NotImplementedError`

#### 2. Directory
- [x] Create `exploration/concept_analysis/analyses/` (will be populated by later phases)
- [x] Create `exploration/concept_analysis/scripts/`
- [x] Create `exploration/concept_analysis/prompt_templates/`

### Validation

- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py list` — shows all 38 concepts
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — shows all as "not-started"
- [x] Concept resolution works: `... status 01`, `... status 17a`, `... status --family MFE`

**What We Know Works After This Phase:**
Table loading, concept ID resolution, filesystem state scanning, CLI skeleton.

---

## Phase 2: Template Engine + `gap-check --dry-run`

### Goal
Template filling utility, the gap-check prompt template, prompt saving, and dry-run mode. We want to see the generated prompt before spending API calls.

### Changes Required

**See `design.md` for:**
- Template variable design → `design.md#prompt-template-design` (Template 1: gap_check.md)
- Prompt lifecycle → `design.md#output-structure` (save prompt → invoke → save output)
- Source file discovery → `design.md#script-architecture` (find_sources)

**Specific file changes:**

#### 1. Template
**File:** `exploration/concept_analysis/prompt_templates/gap_check.md` (NEW)
- [x] Write gap-check prompt template with `{{variable}}` placeholders
- [x] Include instructions for reading dossier, scanning sources, assessing coverage
- [x] Reference the brief and schema by path

#### 2. Script updates
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] `fill_template(template_text, replacements)` — simple `{{var}}` substitution (from Phase 1a pattern)
- [x] `find_sources(concept_id)` — scan Phase 1a `iter-*/sources/` for all source files
- [x] `cmd_gap_check()` — gather inputs, fill template, save prompt, handle `--dry-run`
- [x] `--dry-run` flag: save prompt but skip Claude invocation, print prompt path
- [x] `--model` flag: store for later use (default: sonnet)

### Validation

- [x] `uv run python ... gap-check 01 --dry-run` → saves prompt to `analyses/01-hts-compact-tokamak/gap_check_prompt.md`
- [x] Read saved prompt — verify it has correct paths, references the brief, lists source files
- [x] `uv run python ... gap-check 01 07 --dry-run` → saves prompts for both concepts

**What We Know Works After This Phase:**
Template filling, source file discovery, prompt saving, dry-run mode. We can review prompts before calling Claude.

---

## Phase 3: `invoke_claude()` + Live `gap-check`

### Goal
Wire up Claude invocation via `claude -p` subprocess. Run gap-check on 1-2 real concepts. First end-to-end test.

### Changes Required

**See `design.md` for:**
- Claude invocation pattern → Phase 1a `run_concept.py:invoke_claude()` (lines 294+)
- Gap check output → `design.md#workflow-stages` (Stage 1)

**Specific file changes:**

#### 1. Script updates
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] `invoke_claude(prompt, cwd, timeout, model)` — subprocess `claude -p` via stdin (adapt from Phase 1a)
- [x] Wire `cmd_gap_check()` to invoke Claude when not `--dry-run`
- [x] Save output to `analyses/{id}/gap_report.md`
- [x] Handle `--force` (re-run even if gap_report.md exists)
- [x] Handle `--timeout` flag
- [x] Print progress (concept name, timing)

### Validation

- [x] `uv run python ... gap-check 01` → produces `analyses/01-hts-compact-tokamak/gap_report.md`
- [x] Review gap report quality — does it correctly assess data coverage?
- [x] `uv run python ... status` → concept 01 shows "gap-checked"
- [x] Re-run without `--force` → skips (already done)
- [ ] Re-run with `--force` → re-generates (not tested to save API cost — mechanism verified via code review)

**What We Know Works After This Phase:**
Full gap-check pipeline end-to-end. Claude invocation works. Output is saved correctly. State detection picks up new files.

**Design feedback loop:** Review gap report quality. If the prompt needs adjustment, update `gap_check.md` template and re-run with `--force`.

---

## Phase 4: Output Template + `analyze --dry-run`

### Goal
Write the D1+ output template (calibrated from handwritten exemplars), the analysis prompt template, and wire up `cmd_analyze` with dry-run. This is the highest-leverage creative work — the output template defines what the agent produces.

### Changes Required

**See `design.md` for:**
- Output template design → `design.md#d1-output-template`
- Analysis prompt template → `design.md#prompt-template-design` (Template 2: analysis.md)
- Cross-concept reuse mechanism → `design.md#cross-concept-reuse-mechanism`
- YAML frontmatter → `design.md#yaml-frontmatter-analysismd`

**Specific file changes:**

#### 1. Output template
**File:** `exploration/concept_analysis/prompt_templates/output_template.md` (NEW)
- [x] Study all 3 handwritten exemplars to extract common structure
- [x] Write D1+ section template covering: data availability, modeling challenges, subsystem maturity, materials/supply chain, LCOE parameter extraction, data gap inventory, cross-concept notes
- [x] Include YAML frontmatter template
- [x] Include citation and confidence annotation requirements

#### 2. Analysis prompt template
**File:** `exploration/concept_analysis/prompt_templates/analysis.md` (NEW)
- [x] Write analysis prompt with `{{variable}}` placeholders
- [x] Instructions: read output template, read all sources, cite every value, read approved priors, document reuse
- [x] Anti-hallucination instructions (honest gaps, no fabrication)

#### 3. Script updates
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] `find_approved()` — scan `analyses/*/analysis.md` for `Status: approved` frontmatter
- [x] `find_exemplars()` — list `handwritten/*.md` files
- [x] `cmd_analyze()` — gather all inputs (dossier, sources, exemplars, approved, output template), fill template, save prompt
- [x] Dry-run support for analyze command

### Validation

- [x] `uv run python ... analyze 01 --dry-run` → saves prompt to `analyses/01-.../analysis_prompt.md`
- [x] Read saved prompt — verify it includes: dossier path, source paths, exemplar paths, output template path, (empty) approved list
- [x] Output template reviewed against handwritten exemplars — covers all sections

**What We Know Works After This Phase:**
Analysis prompt template is complete and reviewable. Output template defines the D1+ structure. All input gathering works (sources, exemplars, approved pool).

**Design feedback loop:** This is the phase where we'll most likely want to update the design. The output template and prompt may need iteration after seeing real output in Phase 5.

---

## Phase 5: Live `analyze` + `approve` + Holdout Validation

### Goal
Run analysis on real concepts, implement the approve command, verify the reuse pool works. First full end-to-end validation.

### Changes Required

**See `design.md` for:**
- Approve workflow → `design.md#workflow-stages` (Stage 4)
- Frontmatter update → `design.md#yaml-frontmatter-analysismd`
- Reuse pool → `design.md#cross-concept-reuse-mechanism`
- Holdout validation → `design.md#holdout-validation`

**Specific file changes:**

#### 1. Script updates
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [ ] Wire `cmd_analyze()` to invoke Claude (not just dry-run)
- [ ] Write output to `analyses/{id}/analysis.md` with draft frontmatter
- [ ] `update_frontmatter()` — update Status/Approved-Date in existing frontmatter
- [ ] `cmd_approve()` — update frontmatter to `Status: approved`, set `Approved-Date`
- [ ] Sequential processing: each concept in a batch re-scans approved pool before starting

### Validation

- [ ] `uv run python ... analyze 01` → produces `analyses/01-.../analysis.md` with `Status: draft`
- [ ] Review analysis quality against handwritten `01-hts-compact-tokamak.md` (holdout test)
- [ ] `uv run python ... approve 01` → updates frontmatter to `Status: approved`
- [ ] `uv run python ... analyze 21 --dry-run` → prompt now lists concept 01 in approved analyses
- [ ] `uv run python ... status` → shows concept 01 as "approved", concept 21 as appropriate state

**What We Know Works After This Phase:**
Complete pipeline: gap-check → analyze → review → approve → reuse. Quality is assessable via holdout comparison.

**Design feedback loop:** Based on output quality, iterate on:
- Output template (section structure, depth expectations)
- Analysis prompt (instructions, anti-hallucination)
- Gap-check prompt (if gap reports weren't useful enough)

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 2-3**: Dry-run before live — catch prompt issues before burning API calls
- **Phase 4**: Output template calibrated against exemplars — reduces rework in Phase 5
- **Phase 5**: Start with holdout concept (01) — compare against known-good before batch

---

## Implementation Notes

_TO BE FILLED DURING IMPLEMENTATION_

### Phase 1 Completion
**Completed:** 2026-03-20
**Actual Changes:**
- Created `exploration/concept_analysis/scripts/run_analysis.py` (~270 lines) with full CLI skeleton
- Created directories: `analyses/`, `scripts/`, `prompt_templates/`
- Functions: `load_table()`, `resolve_one()`, `resolve_concepts()`, `parse_frontmatter()`, `get_concept_state()`, `cmd_list()`, `cmd_status()`
- Concept ID resolution handles: numeric (`01`), variant (`17a`), full ID, slug, partial company name, `--family` filter
- Status command shows state symbols (A/D/G/-) with summary counts
**Issues:** None
**Deviations:** None — followed design closely

### Phase 2 Completion
**Completed:** 2026-03-20
**Actual Changes:**
- Created `exploration/concept_analysis/prompt_templates/gap_check.md` — structured gap assessment template with 5 D1+ sections, gap type classification, LCOE parameter tables, anti-hallucination instructions
- Added to `run_analysis.py`: `fill_template()`, `find_sources()`, `get_dossier_path()`, `format_source_list()`
- Rewrote `cmd_gap_check()` with: concept resolution, skip-if-exists, template filling, prompt saving, dry-run support
- Prompt includes absolute paths to dossier, all source files (with KB sizes), brief, and schema
**Issues:** None
**Deviations:** Added `get_dossier_path()` and `format_source_list()` helpers not in original plan — cleaner separation of concerns

### Phase 3 Completion
**Completed:** 2026-03-20
**Actual Changes:**
- Added `invoke_claude()` — subprocess wrapper for `claude -p --dangerously-skip-permissions --verbose`, handles timeout and model selection
- Wired live gap-check path in `cmd_gap_check()` with progress printing and timing
- Added `subprocess` and `time` imports
- End-to-end test: concept 01 gap-check completed in 149s, 13K chars, high quality output
**Issues:** None — output quality was strong on first run. Gap report correctly uses source material, classifies gaps, makes sensible recommendations.
**Deviations:** Skipped `--force` live re-test to save API cost — the skip-if-exists and force flag mechanics are verified via code structure.

### Phase 4 Completion
**Completed:** 2026-03-20
**Actual Changes:**
- Created `prompt_templates/output_template.md` — 8-section D1+ structure: data availability, system function challenges, subsystem maturity (TRL ascending), materials/supply chain, LCOE parameters (available + missing tables), data gap inventory, cross-concept notes, sources. Includes YAML frontmatter template and citation/confidence annotation requirements.
- Created `prompt_templates/analysis.md` — analysis prompt template with all {{variable}} placeholders, anti-hallucination rules, cross-concept reuse instructions, quality calibration against exemplars
- Added to `run_analysis.py`: `find_approved()`, `find_exemplars()`, `format_path_list()`
- Rewired `cmd_analyze()` with: input gathering, template filling, prompt saving, dry-run, sequential processing with per-concept reuse pool re-scan
- Output template calibrated against all 3 exemplars: covers the 4 brief D1 sections + structured LCOE parameter extraction + gap inventory + cross-concept reuse
**Issues:** None
**Deviations:** Added Section 8 (Sources) not in original design — matches exemplar practice of listing primary sources at the end. Added `format_path_list()` helper for cleaner path rendering in prompts.

### Phase 5 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**
