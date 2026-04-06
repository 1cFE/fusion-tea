# Implementation Plan: Concept ID Unification

**Status:** Complete
**Created:** 2026-04-05
**Last Updated:** 2026-04-05

## Source Documents
- **Spec:** `.project/active/concept-id-unification/spec.md`
- **Design:** `.project/active/concept-id-unification/design.md` -- See here for component details, data flow analysis, DD-1 resolution

## Implementation Strategy

**Phasing Rationale:**
Model-first, consumers second. Phase 1 changes the Python model + seed script + regenerates data files + updates Python tests. This establishes the new data shape that everything downstream depends on. Phase 2 updates the 3 JS files that reference `analysis_id`. Phase 3 is a validation sweep to confirm zero remaining references and all pages work.

**Overall Validation Approach:**
- Each phase starts with tests (update existing test expectations, then change code)
- `uv run python -m pytest exploration/concept_explorer/tests/` after each phase
- `grep -rn "analysis_id" exploration/` as final sweep

---

## Phase 1: Python Model + Data Layer

### Goal
Change the data model, update seed script, regenerate data files, update all Python tests. After this phase, the Python layer is fully migrated and all Python tests pass.

### Test Stencil (Write This First)
```python
# Update test_taxonomy_models.py — change BEFORE touching the model

# 1. All ConceptTaxonomy constructions need slug= added:
concept = ConceptTaxonomy(
    concept_id="01",          # was "hts-compact-tokamak"
    slug="hts-compact-tokamak",  # NEW required field
    name="HTS Compact Tokamak",
    ...
)

# 2. by_id() calls switch from slug to analysis ID:
concept = registry.by_id("01")  # was "hts-compact-tokamak"

# 3. New test for by_slug():
def test_by_slug(self, registry):
    concept = registry.by_slug("hts-compact-tokamak")
    assert concept is not None
    assert concept.concept_id == "01"

# 4. Replace analysis_id tests with concept_id spot checks:
def test_concept_id_is_analysis_id(self, registry):
    cfs = registry.by_id("01")
    assert cfs.slug == "hts-compact-tokamak"
    hb11 = registry.by_id("04")
    assert hb11.slug == "laser-icf-p-b11-fast-ignition"
```

### Changes Required

**See `design.md#1-python-models` and `design.md#2-data-regeneration` for full details.**

#### 1. Update Tests First
**File:** `exploration/concept_explorer/tests/test_taxonomy_models.py`

Slug→analysis_id mapping for concepts referenced in tests:
- `hts-compact-tokamak` → `01`
- `frc-w-direct-conversion` → `08`
- `p-b11-frc` → `18`
- `laser-icf-p-b11-fast-ignition` → `04`
- `magnetic-mirror-p-b11` → `06`
- `magnetic-mirror-d-t` → `11`
- `laser-icf-fast-ignition-d-t` → `17b`
- `qi-stellarator-hts` → `09`

Changes:
- [ ] `test_round_trip` (line 50): Add `slug="hts-compact-tokamak"`, change `concept_id` to `"01"`
- [ ] Validation rejection tests (lines 76, 90, 104, 117, 161, 175): Add `slug="bad"` to all `ConceptTaxonomy(concept_id="bad", ...)` constructions
- [ ] `test_tbd_values_serialize_as_strings` (line 129): Add `slug="test"`
- [ ] `test_na_fields_serialize_as_null` (line 144): Add `slug="test"`
- [ ] `test_by_id` (line 218): Change `"hts-compact-tokamak"` → `"01"`
- [ ] `test_known_concept_helion` (line 241): Change `"frc-w-direct-conversion"` → `"08"`
- [ ] `test_known_concept_tae` (line 249): Change `"p-b11-frc"` → `"18"`
- [ ] `test_analysis_id_populated_for_all_concepts` (line 255): Delete entirely
- [ ] `test_analysis_id_spot_checks` (line 260): Replace with `test_concept_id_is_analysis_id` that verifies `by_id("04").slug == "laser-icf-p-b11-fast-ignition"`, etc.
- [ ] Add `test_by_slug` — verify `by_slug("hts-compact-tokamak")` returns concept with `concept_id == "01"`

**File:** `exploration/concept_explorer/tests/test_taxonomy_server.py`

Changes:
- [ ] `test_taxonomy_concept_endpoint` (line 174): Change URL from `/hts-compact-tokamak` → `/01`
- [ ] `test_taxonomy_similarity_endpoint` (line 192): Change URL from `/hts-compact-tokamak` → `/01`, assert `query_concept_id == "01"`
- [ ] `test_taxonomy_compare_endpoint` (line 210): Change URL from `/hts-compact-tokamak/qi-stellarator-hts` → `/01/09`, assert `concept_id == "09"`

#### 2. Python Model
**File:** `exploration/concept_explorer/taxonomy_models.py`

- [ ] `ConceptTaxonomy` (line 185-217): Add `slug: str` after `concept_id`, remove `analysis_id: str | None = None`
- [ ] `ConceptRegistry` (line 293-309): Add `by_slug()` method per `design.md#1-python-models`

#### 3. Seed Script
**File:** `exploration/concept_explorer/seed_registry.py`

- [ ] `_parse_row()` (line 108): Change `concept_id=slugify(name)` → `concept_id=row["ID"].split("-", 1)[0]`
- [ ] `_parse_row()`: Add `slug=slugify(name)` after `concept_id=`
- [ ] `_parse_row()` (line 134): Remove `analysis_id=row["ID"].split("-", 1)[0] or None`

#### 4. Regenerate Data
- [ ] Run: `uv run python exploration/concept_explorer/seed_registry.py`
- [ ] Verify `concept_registry.json` has `"concept_id": "01"` and `"slug": "hts-compact-tokamak"` for first entry
- [ ] Verify `decision_tree.json` has analysis IDs in leaf arrays (e.g. `"01"` not `"hts-compact-tokamak"`)

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/test_taxonomy_models.py -v` -- all pass
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/test_taxonomy_server.py -v` -- all pass
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/ -v` -- full suite, no regressions

**What We Know Works After This Phase:**
- Python model has correct fields (`concept_id` = analysis ID, `slug`, no `analysis_id`)
- `by_id()` and `by_slug()` work correctly
- Data files regenerated with correct shape
- Decision tree contains analysis IDs
- All Python tests pass

---

## Phase 2: JS Consumers

### Goal
Update the 3 JS files that reference `analysis_id`. Add `_modeledIds` to selection tray. After this phase, zero `analysis_id` references remain in the codebase.

### Changes Required

**See `design.md#5-frontend-javascript` for before/after code.**

#### 1. taxonomy_card.js
**File:** `exploration/concept_explorer/static/js/taxonomy_card.js`

- [ ] Line 120: `concept.analysis_id && _modeledIds && _modeledIds.has(concept.analysis_id)` → `_modeledIds && _modeledIds.has(concept.concept_id)`
- [ ] Line 123: `concept.analysis_id` → `concept.concept_id`

#### 2. selection_tray.js
**File:** `exploration/concept_explorer/static/js/selection_tray.js`

- [ ] Add module-level `var _modeledIds = null;` near other state vars (line ~33)
- [ ] Add public `setModeledIds(ids)` function: `_modeledIds = ids;`
- [ ] Line 128-132 (`add()` function): Remove `analysis_id: concept.analysis_id` from stored object
- [ ] Line 197 (popover): `!concept.analysis_id` → `!_modeledIds || !_modeledIds.has(concept.concept_id)`
- [ ] Line 287 (chip rendering): `!concept.analysis_id` → `!_modeledIds || !_modeledIds.has(concept.concept_id)`
- [ ] Expose `setModeledIds` in the module's return/public API

#### 3. taxonomy.js (wire setModeledIds)
**File:** `exploration/concept_explorer/static/js/taxonomy.js`

- [ ] After line 109 (`TaxonomyCards.setModeledIds(modeledIds)`): Add `SelectionTray.setModeledIds(modeledIds);`

#### 4. view_categorical.js
**File:** `exploration/concept_explorer/static/js/view_categorical.js`

- [ ] Lines 89-92: Remove the `analysis_id || concept_id` workaround comment block, change to `const key = c.concept_id;`

### Validation

**Automated:**
- [ ] `grep -rn "analysis_id" exploration/` -- zero hits
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/ -v` -- still passing (no Python regressions)

**What We Know Works After This Phase:**
- All `analysis_id` references eliminated from codebase
- JS files consistent with new data shape
- Selection tray has `_modeledIds` for cost-model gating

---

## Phase 3: Full Validation Sweep

### Goal
Verify everything works end-to-end. All automated tests pass, grep confirms zero `analysis_id` hits, manual smoke test passes.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/ -v` -- all pass
- [ ] `grep -rn "analysis_id" exploration/` -- zero hits
- [ ] `grep -rn "analysis_id" exploration/concept_explorer/static/js/` -- zero hits (belt + suspenders)

**Manual Smoke Test (start server: `uv run python -m exploration.concept_explorer.server`):**
- [ ] Taxonomy page loads, 38 concepts in tree
- [ ] Click tree leaf → neighborhood graph renders with neighbors
- [ ] Similarity panel shows nearest neighbors with scores
- [ ] Constellation scatter plot renders, click dot → focus works
- [ ] Ctrl+click concepts → chips appear in selection tray
- [ ] "No cost model" indicator correct (concepts without cost data get dimmed chip)
- [ ] "Landscape" button → navigates to `/compare?concepts=...` with analysis IDs → comparison page loads correctly
- [ ] Concept profile `/concept/04` loads
- [ ] Index page concept links work
- [ ] No JS console errors on any page

**What We Know Works After This Phase:**
- Complete end-to-end validation
- All acceptance criteria from spec confirmed

---

## Environment Setup

**See CLAUDE.md for full environment rules. Key commands:**
- Tests: `uv run python -m pytest exploration/concept_explorer/tests/ -v`
- Seed: `uv run python exploration/concept_explorer/seed_registry.py`
- Server: `uv run python -m exploration.concept_explorer.server`

---

## Risk Management

**See `design.md#potential-risks` for detailed risk analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: Run seed script AFTER model changes, BEFORE tests. Tests depend on regenerated data files matching the new model.
- **Phase 2**: Selection tray `_modeledIds` is the only net-new code. Follow existing `TaxonomyCards.setModeledIds()` pattern exactly.

## Implementation Notes

*TO BE FILLED DURING IMPLEMENTATION*

### Phase 1 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- `taxonomy_models.py`: Added `slug: str` field, removed `analysis_id`, added `by_slug()` method
- `seed_registry.py`: `concept_id` now from `row["ID"].split("-", 1)[0]`, `slug` from `slugify(name)`, removed `analysis_id` assignment
- Regenerated `concept_registry.json` and `decision_tree.json`
- `test_taxonomy_models.py`: Added `slug=` to all constructions, updated `by_id()` calls to use analysis IDs, replaced `test_analysis_id_*` with `test_concept_id_is_analysis_id` and `test_by_slug`
- `test_taxonomy_server.py`: Updated route URLs from slugs to analysis IDs, updated assertions
**Issues:** None
**Deviations:** None

### Phase 2 Completion
**Completed:** 2026-04-05
**Actual Changes:**
- `taxonomy_card.js`: `concept.analysis_id` → `concept.concept_id` (2 lines)
- `selection_tray.js`: Added `_modeledIds` state var, `setModeledIds()` in public API, removed `analysis_id` from stored object, replaced `!concept.analysis_id` checks with `!_modeledIds || !_modeledIds.has(concept.concept_id)` (popover + chip rendering)
- `taxonomy.js`: Added `SelectionTray.setModeledIds(modeledIds)` call
- `view_categorical.js`: Removed `analysis_id || concept_id` workaround + comment block → `c.concept_id`
**Issues:** None
**Deviations:** None

### Phase 3 Completion
**Completed:** 2026-04-05
**Actual Changes:** Validation only — no code changes
- 32/32 taxonomy tests pass
- `grep analysis_id` in JS: zero hits
- `grep analysis_id` in data files: zero hits
- Only remaining `analysis_id` string in exploration/ is the test method name `test_concept_id_is_analysis_id` (descriptive, not a field reference)
**Issues:** None
**Deviations:** None

---

**Status**: Complete
