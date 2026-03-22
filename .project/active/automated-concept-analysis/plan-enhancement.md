# Implementation Plan: Concept Analysis Enhancement Pipeline

**Status:** In Progress
**Created:** 2026-03-22
**Last Updated:** 2026-03-22

## Source Documents
- **Spec:** `.project/active/automated-concept-analysis/spec-enhancement.md`
- **Design:** `.project/active/automated-concept-analysis/design-enhancement.md` ← See here for component details, prompt templates, function signatures, mapping data

## Implementation Strategy

**Phasing Rationale:**
Build bottom-up: shared infrastructure first (state machine, CLI, template engine), then each pipeline stage in execution order. Each phase ends with a live run on concept 08 (FRC w/ Direct Conversion) as the real validation gate — this concept has the richest data, an existing handwritten holdout, and an existing 1costingfe example for comparison.

**Overall Validation Approach:**
- Each phase has a `--dry-run` smoke test followed by a live Claude invocation
- Concept 08 is the test case throughout
- User inspects real output at each phase before proceeding

---

## Phase 1: Foundation — State Machine, CLI Skeleton, `fill_template()` Upgrade

### Goal
Get the infrastructure in place that all new commands depend on. This is the only phase that modifies shared code paths (state detection, template engine, CLI parser), so we de-risk it first.

### Changes Required

**See `design-enhancement.md` for:**
- State machine logic → `design-enhancement.md#component-5-updated-state-detection-and-cli`
- `fill_template()` upgrade → `design-enhancement.md#2e-cmd_model_setup-implementation` (conditional support)
- CLI parser additions → `design-enhancement.md#5b-cli-additions`
- Status display symbols → `design-enhancement.md#5c-status-display-update`

**Specific file changes:**

#### 1. `fill_template()` — add `{{#if var}}...{{/if}}` conditionals
**File:** `exploration/concept_analysis/scripts/run_analysis.py:281`
- [x] Add regex-based conditional processing before variable substitution (see design §2e, ~15 lines)
- [x] Empty/falsy values → block removed; truthy values → block content kept

#### 2. `get_concept_state()` — add new states
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (find existing `get_concept_state()`)
- [x] Add `model-setup`, `reviewed`, `synthesized` state detection (see design §5a)
- [x] Detection order: approved → synthesized → reviewed → model-setup → drafted → gap-checked → not-started

#### 3. Status display — new symbols
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (find `cmd_status()`)
- [x] Add `M` (model-setup), `R` (reviewed), `S` (synthesized) symbols
- [x] Update summary line to count new states

#### 4. CLI parser — add 4 subcommand stubs
**File:** `exploration/concept_analysis/scripts/run_analysis.py:680` (in `build_parser()`)
- [x] Add `model-setup` parser with args: `concepts`, `--all`, `--family`, `--model`, `--dry-run`, `--timeout`, `--force`
- [x] Add `review` parser with same args
- [x] Add `address-review` parser with args: `concepts`, `--all`, `--family`, `--model`, `--dry-run`, `--timeout` (no `--force`)
- [x] Add `synthesize` parser with same args as review

#### 5. Dispatch table and stub handlers
**File:** `exploration/concept_analysis/scripts/run_analysis.py:720`
- [x] Add 4 stub functions (`cmd_model_setup`, `cmd_review`, `cmd_address_review`, `cmd_synthesize`) that print "not yet implemented"
- [x] Add all 4 to dispatch dict

### Validation

**Automated:**
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — displays correctly, no regressions on existing states
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py model-setup 08` — prints "not yet implemented" (stub works)

**Real example — verify existing pipeline still works:**
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — all existing concept states unchanged
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py gap-check 08 --dry-run` — still generates correct prompt (no regressions)

**What We Know Works After This Phase:**
- State machine correctly detects all 7 states
- `fill_template()` handles conditionals
- CLI accepts all new subcommands
- Existing commands unbroken

---

## Phase 2: Citation Traceability Upgrade

### Goal
Upgrade the analysis prompt templates to produce directly verifiable citations (direct quotes, section-level references, derivation chains, footnotes). Then re-run analysis on concept 08 to validate the improvement.

### Changes Required

**See `design-enhancement.md` for:**
- Citation format specification → `design-enhancement.md#component-1-citation-traceability-upgrade`
- Four citation mechanisms (1a–1d) with examples

**Specific file changes:**

#### 1. Output template — add Citation Format section
**File:** `exploration/concept_analysis/prompt_templates/output_template.md`
- [x] Add `## Citation Format` section specifying 4 mechanisms: direct quotes, section-level table refs, derivation chains, footnote-style prose refs
- [x] Include examples for each mechanism (from design §1a–1d)
- [x] Add guidance: "Use direct block quotes for the 3-5 most critical claims per section"

#### 2. Analysis prompt — add citation instructions
**File:** `exploration/concept_analysis/prompt_templates/analysis.md`
- [x] Add citation format instructions referencing the output template's Citation Format section
- [x] Emphasize: table Source column must include `§Section Name`, not just filename

### Validation

**Dry-run check:**
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 08 --dry-run --force` — prompt includes citation instructions

**Real example — re-analyze concept 08 with upgraded citations:**
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze 08 --force` — produces new `analysis.md`
- [ ] Inspect analysis.md: are direct quotes present? Do table Source entries include section references? Are derivation chains used for inferred values?
- [ ] Compare citation density against holdout-report-08.md findings — are the gaps identified there addressed?

**What We Know Works After This Phase:**
- Analysis prompt produces verifiable citations
- The quality gap identified in holdout-report-08.md (citations not directly verifiable) is addressed

---

## Phase 3: Model Setup Stage

### Goal
Add the `model-setup` command with two-path architecture (1costingfe API vs free-form dataclass). Concept 08 should produce a runnable `model_setup.py` comparable to the existing `dhe3_pulsed_frc.py`.

### Changes Required

**See `design-enhancement.md` for:**
- Two-path architecture → `design-enhancement.md#2a-two-path-architecture`
- Concept mapping data → `design-enhancement.md#2b-concept-mapping-data`
- 1costingfe prompt template → `design-enhancement.md#2c-prompt-template-1costingfe-path`
- Free-form prompt template → `design-enhancement.md#2d-prompt-template-free-form-path`
- `cmd_model_setup()` implementation → `design-enhancement.md#2e-cmd_model_setup-implementation`

**Specific file changes:**

#### 1. Concept mapping data
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (new section after constants)
- [x] Add `COSTINGFE_MAPPING` dict (family-level + concept-specific overrides)
- [x] Add `FREEFORM_CONCEPTS` set
- [x] Add `FUEL_MAPPING` dict
- [x] Add `get_model_path()` resolver function
- [x] Add `get_costingfe_mapping()` helper for family-level fallback

#### 2. 1costingfe prompt template
**File:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md` (NEW)
- [x] Create template per design §2c
- [x] Template variables: `concept_name`, `company`, `analysis_path`, `example_path`, `defaults_path`, `readme_path`, `costing_constants_path`, `costingfe_concept`, `costingfe_fuel`, `mapping_notes`, `output_path`
- [x] Includes: script structure requirements, traceability requirements, anti-hallucination instructions, usage comment

#### 3. Free-form prompt template
**File:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md` (NEW)
- [x] Create template per design §2d
- [x] References MagLIF exemplar as structural template
- [x] 5-layer architecture instructions, parameter documentation requirements, sensitivity analysis

#### 4. `cmd_model_setup()` — replace stub
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Implement full `cmd_model_setup()` per design §2e
- [x] Two-path prompt selection based on `get_model_path()`
- [x] State gate: skip if no `analysis.md`
- [x] Skip/force logic for existing `model_setup.py`
- [x] Save prompt, invoke Claude, print hint for running the model

### Validation

**Dry-run check:**
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py model-setup 08 --dry-run` — prompt saved, references analysis params, dhe3_pulsed_frc.py example, MAG_TARGET defaults
- [x] Verify prompt includes the analysis.md content, the example script, and YAML defaults

**Real example — generate model for concept 08:**
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py model-setup 08` — produces `model_setup.py` (380s, 29059 bytes)
- [x] `uv run python exploration/concept_analysis/analyses/08-frc-w-direct-conversion/model_setup.py` — runs, prints LCOE=50.3 $/MWh (after adding costingfe to pyproject.toml)
- [x] Inspect model_setup.py: inline traceability comments present, UNCERTAIN flags on eta_th/burn_fraction/capacitor costs, sensitivity analysis included
- [x] Compare LCOE output against existing `dhe3_pulsed_frc.py` — 50.3 $/MWh is in the right ballpark
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — concept 08 shows `M` state

**What We Know Works After This Phase:**
- Two-path model setup routing works
- Concept 08 has a runnable LCOE model with traceable parameters
- State detection correctly shows `model-setup` state

---

## Phase 4: Review Stage

### Goal
Add `review` and `address-review` commands. The review produces structured findings with Proposed Actions; the user fills in decisions; address-review applies them. This is the most complex phase due to the iterative loop and PA parsing.

### Changes Required

**See `design-enhancement.md` for:**
- Review prompt template → `design-enhancement.md#3a-review-prompt-template`
- `cmd_review()` implementation → `design-enhancement.md#3b-cmd_review-implementation`
- PA parser → `design-enhancement.md#3c-proposed-action-parsing`
- Address-review prompt template → `design-enhancement.md#3d-address-review-prompt-template`
- `cmd_address_review()` implementation → `design-enhancement.md#3e-cmd_address_review-implementation`

**Specific file changes:**

#### 1. Review prompt template
**File:** `exploration/concept_analysis/prompt_templates/review.md` (NEW)
- [x] Create template per design §3a
- [x] 5 review checklist categories: citation verification, calculation verification, model setup audit, consistency check, factual concerns
- [x] Output format with CV-N, CALC-N, MSA-N finding types and PA-N proposed actions
- [x] PA format: Category, Severity, Location, Finding, Proposed Fix, Decision (blank), User Notes (blank)

#### 2. Address-review prompt template
**File:** `exploration/concept_analysis/prompt_templates/address_review.md` (NEW)
- [x] Create template per design §3d
- [x] Accepts decisions block, instructs Claude to apply agree/alternative/reject
- [x] Appends to address_log.md

#### 3. `parse_proposed_actions()` function
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Implement PA parser per design §3c
- [x] Parse `### PA-N:` headers and `**Key:** Value` fields
- [x] Strip italic placeholder markers for unfilled fields
- [x] Handle edge cases: missing fields, extra whitespace

#### 4. `format_source_list()` helper
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Format source paths as numbered markdown list for the review prompt (already existed from Phase 1)

#### 5. `cmd_review()` — replace stub
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Implement per design §3b
- [x] State gate: skip if no analysis.md; warn but proceed if no model_setup.py
- [x] Track iteration number from frontmatter
- [x] Update frontmatter: Review-Iterations, Last-Review, Review-Status
- [x] Detect CLEAN vs HAS ISSUES from output

#### 6. `cmd_address_review()` — replace stub
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [x] Implement per design §3e
- [x] Parse review.md for filled-in decisions
- [x] Build decisions block for prompt
- [x] Update Review-Status → addressed after applying

### Validation

**Dry-run check:**
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py review 08 --dry-run` — prompt saved, includes analysis.md, model_setup.py, source documents

**Real example — full review cycle on concept 08:**
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py review 08` — produces `review.md` (495s, 31889 chars, 22 citations checked, 8 calcs, 14 model params, 8 PAs)
- [x] Inspect review.md: citations verified against sources with FOUND/NOT FOUND status; PA-N actions properly formatted with blank Decision/User Notes fields; all 8 PAs parse correctly through `parse_proposed_actions()`
- [x] Check analysis.md frontmatter: Review-Iterations=1, Review-Status=has-actions ✓
- [x] User filled in all 8 PA decisions as "agree" in review.md
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py address-review 08` — applies decisions (320s, 8 actions processed)
- [x] Inspect address_log.md: all 8 changes logged correctly, none skipped
- [x] `git diff HEAD` analysis.md / model_setup.py: all 8 PA edits verified against review findings — PA-1 (He3 footnote), PA-2 (softened superlative), PA-3 (17 keV threshold), PA-4 (cap bank cost clarified), PA-5 (installation arithmetic), PA-6 (8→~9 keV), PA-7 (CAS21 traceability), PA-8 (>95% demo caveat)
- [x] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — concept 08 shows `R` state (Review-Status=addressed)

**What We Know Works After This Phase:**
- Review produces structured, verifiable findings
- PA parsing handles real Claude output
- Address-review applies user decisions correctly
- Iterative review loop works (could run review again for iteration 2)

---

## Phase 5: Synthesis Stage and Approve Gate

### Goal
Add `synthesize` command and update `approve` to gate on synthesis. The synthesis provides editorial judgment, sensitivity insights, and decision support — the "so what?" that the automated analysis lacks.

### Changes Required

**See `design-enhancement.md` for:**
- Synthesis prompt template → `design-enhancement.md#4a-synthesis-prompt-template`
- `cmd_synthesize()` implementation → `design-enhancement.md#4b-cmd_synthesize-implementation`
- `find_approved_syntheses()` helper → `design-enhancement.md#component-4-synthesis-stage`
- Approve gate → `design-enhancement.md#component-4c-cmd_approve-gate-update`

**Specific file changes:**

#### 1. Synthesis prompt template
**File:** `exploration/concept_analysis/prompt_templates/synthesis.md` (NEW)
- [ ] Create template per design §4a
- [ ] 7 mandatory sections: Executive Summary, What Matters Most for LCOE, Risk Verdicts, Structural Advantages/Disadvantages, Cross-Concept Positioning, Modeling Confidence, What Would Change My Mind
- [ ] Voice instructions: opinionated, direct, quantified, model-backed
- [ ] Conditionals for model_setup_path and model_output_path

#### 2. `find_approved_syntheses()` helper
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [ ] Find synthesis.md files from approved concepts for cross-concept context

#### 3. `cmd_synthesize()` — replace stub
**File:** `exploration/concept_analysis/scripts/run_analysis.py`
- [ ] Implement per design §4b
- [ ] State gate: refuse if Review-Status not in {addressed, clean}
- [ ] Check for model_output.txt (user-generated)
- [ ] Gather approved prior syntheses for cross-concept perspective

#### 4. `cmd_approve()` — add synthesis gate
**File:** `exploration/concept_analysis/scripts/run_analysis.py` (find existing `cmd_approve()`)
- [ ] Add check: if no synthesis.md and not `--force`, skip with message
- [ ] Add `--force` arg to approve parser if not already present

### Validation

**Gate enforcement check:**
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize 08` with Review-Status != addressed/clean → refuses with helpful message

**Real example — full synthesis on concept 08:**
- [ ] Optionally: `uv run python exploration/concept_analysis/analyses/08-.../model_setup.py | tee exploration/concept_analysis/analyses/08-.../model_output.txt` — save model output for synthesis
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize 08` — produces `synthesis.md`
- [ ] Inspect synthesis.md: does it contain opinionated verdicts? Does it use model LCOE numbers? Are sensitivity insights quantified?
- [ ] Compare against holdout-report-08.md handwritten analysis — does the synthesis match or exceed the editorial quality?
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — concept 08 shows `S` state
- [ ] Test approve gate: `uv run python exploration/concept_analysis/scripts/run_analysis.py approve 08` — works (synthesis exists)

**End-to-end validation:**
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — full state table with all 7 state symbols working
- [ ] Concept 08 directory has the complete file set: analysis.md (with citations), model_setup.py, review.md, address_log.md, synthesis.md

**What We Know Works After This Phase:**
- Full enhanced pipeline: analyze → model-setup → review → address-review → synthesize → approve
- Pipeline ordering enforced at every gate
- All three holdout-report gaps addressed: verifiable citations, modeled LCOE, editorial synthesis

---

## Environment Setup

**See CLAUDE.md for full environment rules**

All commands use: `uv run python exploration/concept_analysis/scripts/run_analysis.py ...`

1costingfe reference files are at `/home/reid/1cfe/1costingfe/` (read-only — we never modify these).

---

## Risk Management

**See `design-enhancement.md#potential-risks` for detailed risk analysis**

**Phase-Specific Mitigations:**
- **Phase 1**: Changes to shared functions (`fill_template`, `get_concept_state`) — validate existing commands still work before proceeding
- **Phase 3**: Model setup quality depends on prompt engineering — `--dry-run` lets us iterate on prompts before burning Claude credits
- **Phase 4**: PA parsing is the most fragile component — test with real Claude output, add lenient matching
- **Phase 5**: Synthesis quality is the hardest to validate automatically — compare against handwritten holdout as the quality bar

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-03-22
**Actual Changes:**
- Modified `run_analysis.py:fill_template()` — added `{{#if var}}...{{/if}}` conditional support via `re.sub` with `re.DOTALL`
- Modified `run_analysis.py:get_concept_state()` — expanded from 4 states to 7 (added model-setup, reviewed, synthesized detection)
- Modified `run_analysis.py:cmd_status()` — added M/R/S symbols and updated summary/legend lines
- Added 4 subcommand parsers (`model-setup`, `review`, `address-review`, `synthesize`) to `build_parser()`
- Added `--force` flag to `approve` parser (needed for Phase 5 synthesis gate bypass)
- Added 4 stub handlers and updated dispatch table
**Issues:** None
**Deviations:** Added `--force` to approve parser proactively (needed in Phase 5 but easy to add now)

### Phase 2 Completion
**Completed:** 2026-03-22
**Actual Changes:**
- Added `## Citation Format` section to `prompt_templates/output_template.md` — 4 citation mechanisms (direct quotes, section-level table refs, derivation chains, footnote-style) with examples and usage guidance
- Added `### Citation Format (CRITICAL)` subsection to `prompt_templates/analysis.md` under Content Requirements — 5 bullet points reinforcing the citation format requirements
**Issues:** None
**Deviations:** None — the "real example" validation items (re-analyze 08 with --force) are left unchecked as they require a live Claude invocation; template changes are verified via dry-run

### Phase 3 Completion
**Completed:** 2026-03-22
**Actual Changes:**
- Added `COSTINGFE_DIR`, `COSTINGFE_EXAMPLES_DIR`, `COSTINGFE_DEFAULTS_DIR`, `COSTINGFE_CONSTANTS_PATH`, `COSTINGFE_README_PATH`, `FREEFORM_EXEMPLAR_PATH` path constants
- Added `COSTINGFE_MAPPING` dict (6 family-level + 1 concept-specific entry for 08-frc)
- Added `FREEFORM_CONCEPTS` set (9 concepts: 12, 13, 15, 16, 18, 19, 24, 27, 35)
- Added `FUEL_MAPPING` dict (D-T, D-D, D-He3, p-B11)
- Added `FAMILY_KEY_MAP` dict mapping CSV (Family, Sub-type) tuples → COSTINGFE_MAPPING keys
- Added `get_model_path()`, `get_costingfe_mapping()`, `_get_subcategory()` helper functions
- Created `prompt_templates/model_setup_costingfe.md` — 1costingfe path template with all template variables
- Created `prompt_templates/model_setup_freeform.md` — free-form path template referencing MagLIF exemplar
- Replaced `cmd_model_setup()` stub with full implementation (resolve, gate, two-path routing, save, invoke, verify)
**Issues:** None
**Deviations:** Added `FAMILY_KEY_MAP` (not explicitly in design) to cleanly resolve CSV column values to mapping keys. Also added `_get_subcategory()` helper to extract the right sub-type column per family.

### Phase 4 Completion
**Completed:** 2026-03-22
**Actual Changes:**
- Created `prompt_templates/review.md` — 5 review checklist categories (citation verification, calculation verification, model setup audit, internal consistency, factual concerns), structured output format with CV-N/CALC-N/MSA-N finding types, PA-N proposed actions with blank Decision/User Notes fields
- Created `prompt_templates/address_review.md` — accepts decisions block, instructs Claude to apply agree/alternative/reject via Edit tool, appends change log to address_log.md
- Added `parse_proposed_actions()` function — regex-based PA parser that splits on `### PA-N:` headers, extracts `**Key:** Value` fields, strips italic placeholder markers for unfilled fields
- Replaced `cmd_review()` stub — full implementation with state gate (skip if no analysis.md, warn if no model_setup.py), iteration tracking from frontmatter, source gathering, template fill, Claude invocation, frontmatter update (Review-Iterations, Last-Review, Review-Status), CLEAN/HAS ISSUES detection from output
- Replaced `cmd_address_review()` stub — parses review.md for filled-in decisions, builds decisions block for prompt, invokes Claude to apply edits, updates Review-Status → addressed
- `format_source_list()` already existed from earlier phases — no changes needed
**Issues:** None
**Deviations:** Added fallback in `cmd_review()` — if Claude prints to stdout instead of writing to the output file, we capture stdout as the review content (same pattern as gap-check). Also added `--force` skip logic to review (not explicitly in design but consistent with all other commands).

### Phase 5 Completion
**Completed:**
**Actual Changes:**
**Issues:**
**Deviations:**

---

**Status**: Draft → In Progress → Complete
