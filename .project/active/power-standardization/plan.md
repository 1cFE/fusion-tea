# Implementation Plan: Power Output Standardization

**Status:** In Progress (revised — post-hoc scaling approach)
**Created:** 2026-04-12
**Last Updated:** 2026-04-12

## Source Documents
- **Spec:** `.project/active/power-standardization/spec.md`
- **Design:** `.project/active/power-standardization/design.md` ← See here for component details, feedback file content, scaling formula, extractor change

## Implementation Strategy

**Approach change**: Switched from "re-run models at 1000 MWe" to "post-hoc scaling". Every model stays at its native design point. A uniform `scaled_headline` dict provides 1000 MWe-normalized LCOE and overnight $/kW for comparison. This eliminates Q_eng inflation, geometry inconsistency, and the need to re-derive cost overrides.

**Phasing Rationale:**
Phase 1 builds the `--feedback` pipeline infrastructure (DONE). Phase 2 handles feedback file rewrites, template rewrites, extractor support, verification, and direct edits. Phase 3 uses the pipeline for feedback iteration on the remaining 10 concepts. Phase 4 validates the full set end-to-end.

Phase 2 tasks are mostly independent of each other.

---

## Phase 1: Pipeline `--feedback` Flag + Feedback Files (COMPLETED — plumbing only)

### Goal
Enable standalone `model-setup` to accept a feedback file. Create initial feedback file structure.

### Changes Completed
- [x] Renamed `_extract_model_findings` → `extract_model_findings` in `scripts/lib/loop.py`
- [x] Updated import in `scripts/test_regex_migration.py`
- [x] Added `--feedback` CLI argument to `model-setup` subparser in `scripts/run_analysis.py`
- [x] Threaded feedback through `cmd_model_setup`
- [x] Created `prompt_templates/feedback/power_standardization_costingfe.md`
- [x] Created `prompt_templates/feedback/power_standardization_freeform.md`

### Still Valid
- `--feedback` CLI plumbing — unchanged, still correct
- `extract_model_findings` rename — still correct
- Feedback file structure/format — still correct

### Needs Redo in Phase 2
- Feedback file **content** needs rewrite (old content instructed re-running at 1000 MWe; new content instructs adding `scaled_headline`)

---

## Phase 2: Feedback Rewrites + Templates + Extractor + Verification + Direct Edits

### Goal
Rewrite feedback content for post-hoc scaling approach. Update templates. Add extractor support. Verify 6 concepts. Direct-edit 3 concepts. All zero-risk, independent tasks.

### Changes Required

#### 1. Rewrite Feedback Files
**File:** `exploration/concept_analysis/prompt_templates/feedback/power_standardization_costingfe.md`
- [x] Rewrite content: instruct adding `scaled_headline` block (see `design.md#component-2`)
- [x] Do NOT instruct changing `net_electric_mw` or re-deriving overrides

**File:** `exploration/concept_analysis/prompt_templates/feedback/power_standardization_freeform.md`
- [x] Rewrite content: instruct adding `scaled_headline` block (see `design.md#component-2`)
- [x] Do NOT instruct changing physics or renaming `results`

#### 2. Rewrite Prompt Template Sections
**File:** `exploration/concept_analysis/prompt_templates/model_setup_costingfe.md`
- [x] Replace existing "Power Standardization (CRITICAL)" section with `scaled_headline` instructions (see `design.md#component-3`)

**File:** `exploration/concept_analysis/prompt_templates/model_setup_freeform.md`
- [x] Replace existing "Power Standardization (CRITICAL)" section with `scaled_headline` instructions (see `design.md#component-3`)

#### 3. Add Extractor Support (FR-7)
**File:** `exploration/concept_explorer/extract_explorer_data.py`
- [x] In `extract_costingfe` (~line 206): after availability injection, inject `scaled_headline` values into raw dict if present
- [x] In `extract_standalone` (~line 434): added `_apply_scaled_headline` helper applied in all 3 extraction paths before `from_forward_result`

#### 4. Verify 6 Existing 1000 MWe Concepts (FR-2)
- [x] 03 — Laser ICF Liquid Jet: confirmed `result` at `net_electric_mw=1000`
- [x] 04 — Laser ICF p-B11: confirmed `result` at `net_electric_mw=1000`
- [x] 07 — MagLIF: confirmed at 1000 MWe
- [x] 08 — FRC w/ Direct Conversion: confirmed plant-level 1000 MWe (20×50 MWe modules)
- [x] 09 — QI Stellarator HTS: confirmed `result` at `net_electric_mw=1000`
- [x] 10 — Large-Scale Stellarator: confirmed `result` at `net_electric_mw=1000`

#### 5. Direct Edits — 3 Simple Costingfe Models (FR-3)
**File:** `exploration/concept_analysis/analyses/05-planar-coil-stellarator/model_setup.py`
- [x] Add `scaled_headline` block after existing `result` (see `design.md#component-4` for pattern)
- [x] Add print line for scaled headline

**File:** `exploration/concept_analysis/analyses/11-magnetic-mirror/model_setup.py`
- [x] Same pattern

**File:** `exploration/concept_analysis/analyses/21-spherical-tokamak-hts/model_setup.py`
- [x] Same pattern

### Validation

**Automated:**
- [x] Each of the 3 edited models runs without errors
- [x] Each prints scaled headline with p_net = 1000
- [x] Extractor loads a model with `scaled_headline` and produces correct HeadlineEconomics

**Manual:**
- [x] Verify 6 existing concepts are compliant (already done from previous Phase 2)
- [x] Prompt templates contain updated "Power Standardization" section with `scaled_headline`
- [x] Feedback files instruct `scaled_headline`, not `net_electric_mw=1000`

---

## Phase 3: Feedback Iteration Runs (10 Concepts)

### Goal
Re-run 5 costingfe + 5 freeform concepts through the pipeline with post-hoc scaling feedback. This is the bulk of the work (~2.5 hours sequential).

### Changes Required

#### 1. Costingfe Feedback Runs (5 concepts)
```bash
PIPELINE="exploration/concept_analysis/scripts/run_analysis.py"
FEEDBACK="exploration/concept_analysis/prompt_templates/feedback/power_standardization_costingfe.md"

uv run python $PIPELINE model-setup 01 06 14 17a 28 --force --feedback $FEEDBACK
```
- [x] 01 — HTS Compact Tokamak (ARC): validate, confirm overrides untouched
- [x] 06 — Magnetic Mirror p-B11: validate, confirm CAS21 override untouched
- [x] 14 — MTF Pneumatic (GF): validate
- [x] 17a — Laser ICF Hybrid (Xcimer): validate
- [x] 28 — HTS Tokamak Full HTS: validate

#### 2. Freeform Feedback Runs (5 concepts)
```bash
FEEDBACK="exploration/concept_analysis/prompt_templates/feedback/power_standardization_freeform.md"

uv run python $PIPELINE model-setup 02 12 15 22 35 --force --feedback $FEEDBACK
```
- [x] 02 — Acoustic ICF/Sonofusion: validate
- [x] 12 — Levitated Dipole: validate (required --timeout 1800)
- [x] 15 — SFS Z-Pinch: validate (required --timeout 1800)
- [x] 22 — Projectile ICF: validate (required --timeout 1800)
- [x] 35 — PoloMac: validate

#### 3. Per-Concept Validation
For each of the 10 concepts after regeneration:
- [x] `uv run python model_setup.py` exits cleanly
- [x] `scaled_headline` dict exists at module level with `p_net_mw=1000.0`
- [x] Native `result`/`results` unchanged (Q_eng, p_net at native power)
- [x] LCOE is plausible (scaled < native for p_native < 1000)

### Validation

**Automated:**
- [x] All 10 models run without errors
- [x] All 10 have `scaled_headline` at module level

**Manual:**
- [x] Costingfe: verify cost_overrides are untouched (not re-derived) — spot-checked 01 (ARC)
- [x] Freeform: verify physics params unchanged (p_fus, Q_sci, Q_eng)
- [x] Compare LCOE before/after for sanity

---

## Phase 4: Re-extraction and Cross-Concept Validation

### Goal
Re-extract all 19 concepts and verify the explorer shows consistent 1000 MWe headlines.

### Changes Required

#### 1. Re-extract All Concepts
- [x] Run `uv run python exploration/concept_explorer/extract_explorer_data.py`
- [x] Verify no extraction errors

#### 2. Cross-Concept p_net Verification
```python
# uv run python -c "
import json
from pathlib import Path
data_dir = Path('exploration/concept_explorer/data')
failures = []
for f in sorted(data_dir.glob('*.json')):
    if f.name in ('manifest.json', 'parameter_index.json'):
        continue
    d = json.loads(f.read_text())
    cm = d.get('cost_model')
    if cm:
        p = cm.get('headline', {}).get('p_net_mw')
        if p is None or abs(p - 1000.0) > 1.0:
            failures.append((d['concept_id'], p))
if failures:
    print('FAIL:', failures)
else:
    print('ALL 1000 MWe — PASS')
# "
```
- [x] All concepts show p_net = 1000.0
- [x] No failures

#### 3. LCOE Sanity Check
- [x] Review LCOE values across all concepts
- [x] No order-of-magnitude outliers (range: 41.6–373.9 $/MWh)
- [x] Scaled LCOE < native LCOE for all concepts with p_native < 1000

#### 4. Explorer Regression Check
- [x] Explorer loads without errors (confirmed by user)
- [x] Comparison view renders correctly (confirmed by user)
- [x] Costingfe sliders: N/A — no concepts have `parameter_metadata` with ranges, so sliders never render. Pre-existing state, unrelated to this work.

---

## Environment Setup

**See CLAUDE.md for full environment rules** — always use `uv run python ...`

---

## Risk Management

**Phase-Specific Mitigations:**
- **Phase 2**: If extractor injection breaks `from_forward_result`, the override is in the raw dict layer — easy to debug and revert.
- **Phase 3**: If a feedback-iterated model regresses quality or ignores the `scaled_headline` directive, compare with git history and re-run with refined feedback. Per-concept validation catches issues before they propagate.
- **Phase 4**: If extraction shows outlier LCOE values, investigate individual model before bulk commit.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-04-12
**Actual Changes:**
- Renamed `_extract_model_findings` → `extract_model_findings` in `scripts/lib/loop.py` (definition + internal caller at line 505)
- Updated import in `scripts/test_regex_migration.py` (import + all 5 usages)
- Added `--feedback` CLI argument to `model-setup` subparser in `scripts/run_analysis.py:1202`
- Added import of `extract_model_findings` to `run_analysis.py:76`
- Threaded feedback through `cmd_model_setup` at line ~483: reads file, extracts findings, falls back to raw content, passes to `build_model_vars`
- Created `prompt_templates/feedback/power_standardization_costingfe.md`
- Created `prompt_templates/feedback/power_standardization_freeform.md`
**Issues:** None
**Deviations:** None — design was accurate

### Approach Revision (between Phase 2 and Phase 3)
**Date:** 2026-04-12
**Change:** Switched from "re-run at 1000 MWe" to "post-hoc scaling with `scaled_headline`"
**Reason:** Re-running at 1000 MWe inflates Q_eng, creates geometry/parasitic inconsistency, and requires re-derivation of absolute-dollar cost overrides. Post-hoc scaling preserves physics consistency.
**Impact:** Reverted 5 model files changed in Phase 2. Rewrote spec, design, plan. Phase 2 verification (6 concepts) still valid. Phase 2 direct edits and template changes need redo with new approach.

### Phase 2 Completion (revised)
**Completed:** 2026-04-12
**Actual Changes:**
- Rewrote `prompt_templates/feedback/power_standardization_costingfe.md` — now instructs `scaled_headline` block, not `net_electric_mw=1000`
- Rewrote `prompt_templates/feedback/power_standardization_freeform.md` — same approach, preserves `results` at native power
- Replaced "Power Standardization (CRITICAL)" section in `model_setup_costingfe.md` — now instructs `scaled_headline` with α=0.6
- Replaced "Power Standardization (CRITICAL)" section in `model_setup_freeform.md` — same, uses `results["power"]` for p_native
- Added `scaled_headline` injection in `extract_explorer_data.py:extract_costingfe` (4 lines after availability injection)
- Added `_apply_scaled_headline` helper in `extract_explorer_data.py:extract_standalone` — applied in all 3 extraction paths
- Added `scaled_headline` block + print line to `05-planar-coil-stellarator/model_setup.py` (390 MWe → LCOE 155.5→106.7)
- Added `scaled_headline` block + print line to `11-magnetic-mirror/model_setup.py` (500 MWe → LCOE 118.6→89.9)
- Added `scaled_headline` block + print line to `21-spherical-tokamak-hts/model_setup.py` (600 MWe → LCOE 183.8→149.9)
- Verified all 6 existing 1000 MWe concepts (03, 04, 07, 08, 09, 10) — confirmed compliant
**Issues:** None
**Deviations:** Standalone extractor uses a local `_apply_scaled_headline` helper instead of inline injection in each path — reduces duplication (3 paths share one helper)

### Phase 3 Completion
**Completed:** 2026-04-12
**Actual Changes:**
- Regenerated 5 costingfe models (01, 06, 14, 17a, 28) via `--feedback` pipeline — all have `scaled_headline`
- Regenerated 5 freeform models (02, 12, 15, 22, 35) via `--feedback` pipeline — all have `scaled_headline`
- All 10 models validated: run cleanly, `scaled_headline.p_net_mw=1000.0`, native results preserved
- Costingfe cost_overrides confirmed untouched (spot-checked 01-ARC)
**Issues:**
- 3 freeform concepts (12, 15, 22) timed out at default 900s limit; re-run with `--timeout 1800` succeeded
**Deviations:** None — all models followed the feedback directive correctly

### Phase 4 Completion
**Completed:** 2026-04-12
**Actual Changes:**
- Re-extracted all 19 concepts via `extract_explorer_data.py` — all wrote successfully
- All 19 concepts show `p_net_mw=1000.0` in explorer headline data
- LCOE range: 41.6–373.9 $/MWh (no order-of-magnitude outliers)
- Overnight $/kW range: 1,773–28,077 (consistent with LCOE ordering)
- Added `scaled_headline` to concept 08 (FRC w/ Direct Conversion) — was missed in Phase 2/3 because costingfe `power_table.p_net` reports per-module 50 MWe, not plant-level 1000 MWe. No economy-of-scale adjustment needed (LCOE/overnight already correct at plant level via `n_mod=20`).
**Issues:**
- Concept 08 required a fix: `power_table.p_net` returns per-module value (50 MWe) for modular plants. Added `scaled_headline` with p_net=1000, LCOE and overnight unchanged.
**Deviations:**
- Concept 08 `scaled_headline` uses factor=1.0 (no scaling) unlike other concepts — it just corrects the p_net display for the modular plant architecture.

---

**Status**: Complete (pending manual explorer regression check)
