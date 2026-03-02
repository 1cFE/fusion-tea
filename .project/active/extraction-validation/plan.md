# Implementation Plan: Extraction Pipeline Validation

**Status:** Complete
**Created:** 2026-03-01
**Last Updated:** 2026-03-01

## Source Documents

- **Spec:** `.project/active/extraction-validation/spec.md`
- **Design:** N/A (execution/validation task, no design doc)

## Implementation Strategy

**Phasing Rationale:**
Capture baselines before overwriting anything → low-cost preview before expensive extraction → full extraction → compare and decide. Each phase gates the next: if `--check` fails we stop, if `--dry-run` reveals show-stoppers we reassess before spending ~$300 on full extraction.

**Overall Validation Approach:**
- Quantitative baselines captured BEFORE re-extraction (can't go back)
- Each phase updates `results.md` incrementally
- Learnings, issues, and surprises documented as they happen

---

## Phase 1: Baseline Capture & Installation Check

### Goal

Record quantitative metrics for all 6 existing extractions (so we have numbers to compare against after re-extraction), then verify v4 pipeline components are functional. This must happen first because re-extraction overwrites `output.md`.

### Steps

#### 1. Capture baseline metrics for all 6 sources

For each source in `knowledge/sources/`:
- [ ] Line count, word count, file size of `output.md`
- [ ] Header count (`## ` lines)
- [ ] Table count (markdown table delimiters)
- [ ] Strikethrough marker count (`~~`)
- [ ] Capture key fields from existing `metrics.json` and `decisions.json` if present

#### 2. Run `--check`

- [ ] Run `uv run agentic-mbse extract --check`
- [ ] Capture full output (component status, dependency availability)
- [ ] Note any missing optional dependencies (GMFT, Img2Table, Docling, Pandoc)

#### 3. Start `results.md`

- [ ] Create `.project/active/extraction-validation/results.md`
- [ ] Write baseline metrics table
- [ ] Write `--check` output section

### Validation

- [ ] `--check` exits without error
- [ ] Baseline metrics recorded for all 6 sources
- [ ] `results.md` exists with baseline and check sections

**What We Know After This Phase:**
Pipeline is functional. We have quantitative baselines to compare against later.

---

## Phase 2: Quality Gate Preview (`--dry-run`)

### Goal

Run `--dry-run` on 2-3 sources to see what v4's quality gate would decide — which pages need enhancement, what issues it detects — before committing to full (expensive) extraction.

### Steps

#### 1. Select sources for dry-run

Pick 2-3 sources that cover different characteristics:
- [ ] One with known table issues (e.g., Hawker)
- [ ] One with good prior extraction quality (e.g., Delene or Hsu)
- [ ] Optionally a third with different characteristics

#### 2. Run `--dry-run` on each

- [ ] `uv run agentic-mbse extract --dry-run <pdf_path>` for each selected source
- [ ] Capture full output for each

#### 3. Assess dry-run results

- [ ] Do quality gate decisions seem reasonable?
- [ ] Any unexpected findings (pages flagged that shouldn't be, or not flagged that should be)?
- [ ] Compare quality gate assessment against known issues (Hawker strikethrough, etc.)
- [ ] Go/no-go decision: proceed to full extraction, or stop and investigate?

#### 4. Update `results.md`

- [ ] Add dry-run output and assessment to results document

### Validation

- [ ] `--dry-run` output captured for at least 2 sources
- [ ] Assessment written with go/no-go for Phase 3

**What We Know After This Phase:**
Quality gate is making reasonable decisions. We're confident enough to invest in full extraction.

---

## Phase 3: Full Re-extraction

### Goal

Re-extract all 6 existing PDFs with the v4 pipeline using consistent settings.

### Steps

#### 1. Pre-extraction cleanup (if needed)

- [ ] Check if `--force` is sufficient or if old artifacts need manual removal
- [ ] Document any cleanup steps taken

#### 2. Re-extract all 6 sources

For each PDF in the corpus:
- [ ] `uv run agentic-mbse extract --force --budget 50 --model opus --index --summarize <pdf_path>`
- [ ] Verify `output.md` was produced
- [ ] Verify `metrics.json` and `decisions.json` were produced
- [ ] Note any errors, warnings, or unexpected behavior

Sources:
- [ ] `an_assessment_of_the_economics_of_future_electric_power`
- [ ] `aries_cost_account_documentation`
- [ ] `a_simplified_economic_model_for_inertial_fusion`
- [ ] `overview_of_the_helios_design_a_practical_planar_coil`
- [ ] `revisit_of_the_2017_costing_for_four_arpa_e_alpha_concepts`
- [ ] `tea_dt_mfe_cost_analysis`

#### 3. Post-extraction verification

- [ ] All 6 sources have new `output.md`
- [ ] All 6 sources have `metrics.json` and `decisions.json`
- [ ] `full_document.md` files are preserved (old baseline)

### Validation

- [ ] All 6 extractions completed without pipeline errors
- [ ] All expected output files present
- [ ] `full_document.md` not overwritten

**What We Know After This Phase:**
v4 pipeline runs to completion on all 6 fusion sources.

---

## Phase 4: Comparison & Verdict

### Goal

Compare v4 output against Phase 1 baselines using both qualitative assessment and quantitative metrics. Record acceptability verdict.

### Steps

#### 1. Capture new metrics

- [ ] Same metrics as Phase 1 baseline: line count, word count, file size, header count, table count, strikethrough count
- [ ] Capture `metrics.json` and `decisions.json` key fields

#### 2. Quantitative comparison

- [ ] Build comparison table: old metrics vs. new metrics for each source
- [ ] Flag significant changes (>20% difference in any metric)

#### 3. Qualitative comparison

For each source, spot-check:
- [ ] Equation rendering — improved, same, or regressed?
- [ ] Table extraction — structured tables vs. garbled text?
- [ ] Prose readability — clean markdown vs. artifacts?
- [ ] Any LLM hallucination text present?
- [ ] Cost data accuracy — spot-check key numbers against known values

Focus deeper review on:
- [ ] Hawker (known problem case — strikethrough, tables, equations)
- [ ] At least one other source in depth

#### 4. Write verdict

- [ ] **Verdict**: proceed / proceed with caveats / block
- [ ] **Rationale**: What improved, what regressed, what's acceptable
- [ ] **Known issues**: Pre-existing vs. new, with upstream issue references if needed
- [ ] **Recommendations**: Any follow-up actions for later items

#### 5. Finalize `results.md`

- [ ] Comparison tables complete
- [ ] Qualitative notes for each source
- [ ] Verdict section written
- [ ] Document is self-contained and readable

### Validation

- [ ] Quality comparison includes both qualitative and quantitative for each source
- [ ] Verdict recorded with clear rationale
- [ ] `results.md` is complete and ready to commit

**What We Know After This Phase:**
Whether the v4 extraction pipeline is acceptable for the investigation ahead. All spec acceptance criteria met.

---

## Risk Management

| Risk | Mitigation |
|------|------------|
| Re-extraction overwrites `output.md` before baselines captured | Phase 1 captures all baselines first |
| `--force` doesn't clean up old artifacts properly | Phase 3 Step 1 checks and handles cleanup |
| Full extraction costs ~$300 in API calls | Phase 2 dry-run provides low-cost preview before committing |
| Pipeline fails mid-corpus | Extract one-at-a-time, document partial results |
| Hawker strikethrough attributed to v4 | Spec and plan explicitly call this out as pre-existing |

---

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-03-01
**Issues:** `--check` with Claude probe produces no stdout from non-TTY (Claude CLI requires TTY). Workaround: pipe to file.
**Surprises:** Docling shows `not_installed` — it's in agentic-mbse's `extract-full` extras but not in fusion-tea's venv.

### Phase 2 Completion
**Completed:** 2026-03-01
**Issues:** None
**Surprises:** Quality gate flagged 0 pages for Claude enhancement on both sources. Dry-run output is minimal but sufficient for go/no-go.

### Phase 3 Completion
**Completed:** 2026-03-01
**Issues:** Img2Table `niBlackThreshold` broken on all sources (OpenCV contrib issue). Claude summarize fails from Claude Code (nested session). Ran from user terminal via `scripts/extract_all.sh`.
**Surprises:** Swanson used `pandoc_arxiv` backend (1.5s, $0) — identical output to baseline. Total cost only ~$5.58, far under $300 estimate.

### Phase 4 Completion
**Completed:** 2026-03-01
**Issues:** One numeric accuracy concern — Delene Claude-enhanced page changed "3% inflation" to "5%". Quality gate catches gross errors but not subtle numeric changes.
**Surprises:** Table deduplication is the biggest quality win — old pipeline rendered every table twice (plaintext + garbled markdown). v4 renders once, cleanly. Line counts dropped 25-55% with no content loss.

---

**Deliverable:** `.project/active/extraction-validation/results.md`
**Status**: Complete (2026-03-01)
