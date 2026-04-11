# Design: Concept ID Unification

**Status:** Complete
**Owner:** Reid W
**Created:** 2026-04-05
**Updated:** 2026-04-06
**Branch:** ralph/concept-explorer
**Commit:** 7374772

## Overview

Unify the meaning of `concept_id` across taxonomy and cost model systems so the analysis directory ID (e.g., `"04"`) is the single canonical identifier. The slug (`"hts-compact-tokamak"`) gets its own `slug` field, and `analysis_id` is eliminated.

## Related Artifacts

- **Spec:** `.project/active/concept-id-unification/spec.md`
- **Prior rename:** commit d4ceb34 (`cost_model_id` → `analysis_id`)
- **Memory:** `.claude/projects/-home-reid-1cfe-fusion-tea/memory/project_concept_id_mismatch.md`

## Research Findings

### Data Flow: Taxonomy Page

The taxonomy page has an interconnected ID chain:

1. **Server startup** (`server.py:276-278`): Precomputes similarity reports dict, keyed by `concept.concept_id` (currently slug)
2. **Registry API** → `taxonomy.js:95`: Builds `_registry` keyed by `concept.concept_id` (slug)
3. **Decision tree** (`seed_registry.py:200`): Stores `c.concept_id` (slug) in leaf `concepts` arrays
4. **Tree click** → passes slug from decision tree → `handleFocus(slug)` → `_registry[slug]` → lookup succeeds
5. **Similarity fetch**: `fetchSimilarity(slug)` → `GET /api/taxonomy/similarity/{slug}` → server lookup by slug key
6. **Constellation data** (`similarity.py:391`): Points carry `concept_id` (slug) as identifier
7. **Selection tray** (`selection_tray.js:128-132`): Stores both `concept_id` (slug) and `analysis_id`; navigation to compare uses `getIds()` which returns **slug** keys
8. **Compare navigation** (`selection_tray.js:328`): `/compare?concepts=slug1,slug2` — but `comparison.js:202` validates against manifest (which uses analysis IDs) → **currently broken** for taxonomy-originating selections

### Data Flow: Cost Model / Comparison Page

- `manifest.json`, `ConceptData`, and `comparison.js` all use analysis ID as `concept_id`
- URLs: `/concept/04`, `/compare?concepts=04,05`
- No slugs in this system

### Key Files Requiring Changes

| File | What uses `concept_id` | Current meaning |
|------|----------------------|-----------------|
| `taxonomy_models.py:189` | `ConceptTaxonomy.concept_id` | Slug |
| `taxonomy_models.py:217` | `ConceptTaxonomy.analysis_id` | Analysis ID |
| `taxonomy_models.py:300-305` | `ConceptRegistry.by_id()` | Searches by slug |
| `seed_registry.py:108,134` | `_parse_row()` | Assigns slug to `concept_id`, analysis ID to `analysis_id` |
| `seed_registry.py:200` | `_build_decision_tree()` | Puts slugs in tree leaf arrays |
| `similarity.py:189-196,278-279` | `compare_pair()`, `find_nearest()` | Uses slug in PairComparison IDs |
| `server.py:276-278` | `_load_taxonomy()` | Keys similarity dict by slug |
| `server.py:409-417` | `api_taxonomy_concept()` | Route param = slug |
| `server.py:422-433` | `api_taxonomy_similarity()` | Route param = slug |
| `server.py:443-459` | `api_taxonomy_compare()` | Route params = slug |
| `taxonomy.js:95-96` | `_registry` index | Keyed by slug |
| `taxonomy_card.js:120-123` | Cost model link | Uses `analysis_id` to link |
| `selection_tray.js:128-132` | `add()` | Stores slug as key, `analysis_id` separately |
| `view_categorical.js:89-92` | Cache key workaround | `analysis_id \|\| concept_id` |
| `constellation.js:64,176,224` | Point IDs | Uses `concept_id` (slug from API) |
| `neighborhood_graph.js:163-164,176-177` | Node IDs | Uses `concept_id` (slug from API) |

### Existing Patterns

- `ConceptData.concept_id` already uses analysis ID — this is the target state
- `ConceptManifest` entries use analysis ID
- All cost-model URLs use analysis ID
- `seed_registry.py` already has the `slugify()` function and reads `row["ID"]` for analysis ID

## Design Decisions

### DD-1: Universal Analysis ID vs Slug-Keyed Taxonomy

The spec (FR-8) assumed the taxonomy page would continue using slugs internally and the API routes would rename parameters to `slug`. During research, I found this creates a split-identity problem.

**Option A: Slug-keyed taxonomy (spec's assumption)**
- `_registry` in taxonomy.js keyed by slug
- Decision tree stores slugs
- API routes renamed: `/api/taxonomy/similarity/{slug}`
- Selection tray translates slug → analysis_id for compare navigation
- **Pro:** Minimal taxonomy JS changes
- **Con:** Still two ID systems — taxonomy uses slug, cost model uses analysis ID. Selection tray must maintain dual mapping. Existing bug in compare navigation persists (need explicit translation). `_restoreFromUrl` needs reverse lookup.

**Option B: Universal analysis ID (recommended)**
- `_registry` in taxonomy.js keyed by `concept_id` (analysis ID)
- Decision tree stores analysis IDs
- API routes keep `concept_id` parameter name (now means analysis ID)
- Selection tray keyed by analysis ID — compare navigation works directly
- `slug` field exists on objects for display but is never used as a lookup key in JS
- **Pro:** True unification — one ID system. Fixes existing compare navigation bug. Simpler code. Shorter URLs (`?selected=01,04` vs `?selected=hts-compact-tokamak,...`).
- **Con:** More files change (decision tree regenerated, constellation/neighborhood use analysis ID). FR-8 becomes unnecessary.

**Recommendation:** Option B. The whole point is to have one canonical ID. Keeping slug as a lookup key in the taxonomy page perpetuates the split.

**Impact on spec:** FR-8 (rename route parameters to `slug`) becomes **not applicable** — routes keep `concept_id` which now means analysis ID everywhere. FR-5 (`by_slug()`) is still implemented but unused by the current UI.

**Decision:** Option B — universal analysis ID. Spec updated to match.

## Proposed Design

*Contingent on DD-1 resolution. Written assuming Option B (universal analysis ID).*

### 1. Python Models (`taxonomy_models.py`)

**`ConceptTaxonomy`** (line 185-217):
```python
class ConceptTaxonomy(BaseModel):
    # Identity
    concept_id: str          # Analysis directory ID, e.g. "01" (was slug)
    slug: str                # URL-safe slug, e.g. "hts-compact-tokamak" (NEW field)
    name: str
    company: str | None = None
    # ... (all other fields unchanged)
    confidence: TaxonomyConfidence
    # analysis_id: REMOVED
```

**`ConceptRegistry`** (line 293-309):
```python
class ConceptRegistry(BaseModel):
    version: str
    generated_from: str | None = None
    concepts: list[ConceptTaxonomy]

    def by_id(self, concept_id: str) -> ConceptTaxonomy | None:
        """Look up by analysis ID (e.g. '04')."""
        for c in self.concepts:
            if c.concept_id == concept_id:
                return c
        return None

    def by_slug(self, slug: str) -> ConceptTaxonomy | None:
        """Look up by slug (e.g. 'hts-compact-tokamak')."""
        for c in self.concepts:
            if c.slug == slug:
                return c
        return None

    def by_family(self, family: ConfinementFamily) -> list[ConceptTaxonomy]:
        return [c for c in self.concepts if c.confinement_family == family]
```

### 2. Data Regeneration (`seed_registry.py`)

**`_parse_row()`** (line 107-135):
```python
return ConceptTaxonomy(
    concept_id=row["ID"].split("-", 1)[0] or None,  # "01", "04", etc.
    slug=slugify(name),                               # "hts-compact-tokamak"
    name=name,
    # ... all other fields unchanged ...
    confidence=TaxonomyConfidence(row["Overall Confidence"].strip()),
    # analysis_id= REMOVED
)
```

`concept_id` becomes non-optional (`str`, not `str | None`) — all 38 concepts already have analysis IDs per commit d4ceb34.

**`_build_decision_tree()`** (line 200): No change needed — it already uses `c.concept_id`, which will now be the analysis ID. The tree leaf arrays will contain `["01", "04", ...]` instead of `["hts-compact-tokamak", ...]`.

**Duplicate ID check** (line 321): Still works — checks `c.concept_id` for duplicates.

**After code changes, regenerate data:**
```bash
uv run python exploration/concept_explorer/seed_registry.py
```
This rewrites both `concept_registry.json` and `decision_tree.json`.

### 3. Similarity Engine (`similarity.py`)

No code changes needed. All `concept_id` references on `ConceptTaxonomy` objects will automatically use the analysis ID since the field is renamed. The similarity models (`PairComparison`, `SimilarityResult`, `ConstellationPoint`, etc.) use `concept_id` as a passthrough — they'll carry analysis IDs.

### 4. Server (`server.py`)

**`_load_taxonomy()`** (line 276-278): No code change needed — `concept.concept_id` will be the analysis ID, and the dict will be keyed by analysis ID.

**`api_taxonomy_concept()`** (line 409): No change — `concept_id` parameter now means analysis ID, `reg.by_id()` searches by analysis ID.

**`api_taxonomy_similarity()`** (line 422-433): No change — lookup key is now analysis ID.

**`api_taxonomy_compare()`** (line 443-459): No change — `reg.by_id()` works with analysis IDs.

**Route registrations** (line 601-602): No change — parameter name `concept_id` remains, now means analysis ID.

### 5. Frontend JavaScript

#### `taxonomy.js` (lines 94-96)
```javascript
// Before:
_registry[concepts[c].concept_id] = concepts[c];
nameMap[concepts[c].concept_id] = concepts[c].name;

// After:
_registry[concepts[c].concept_id] = concepts[c];  // Now keyed by analysis ID
nameMap[concepts[c].concept_id] = concepts[c].name;  // nameMap also by analysis ID
```
The code is identical — the field name didn't change. The *value* changes from slug to analysis ID because the server now sends analysis IDs. `nameMap` is passed to `TreeView.updateLeafLabels()` which replaces raw IDs with human names — essential now that IDs are "01" not "hts-compact-tokamak".

#### `taxonomy_card.js` (lines 120-123)
```javascript
// Before:
if (concept.analysis_id && _modeledIds && _modeledIds.has(concept.analysis_id)) {
  link.href = "/concept/" + concept.analysis_id;

// After:
if (_modeledIds && _modeledIds.has(concept.concept_id)) {
  link.href = "/concept/" + concept.concept_id;
```

#### `selection_tray.js` (lines 128-132)
```javascript
// Before:
_selected.set(concept.concept_id, {
  concept_id: concept.concept_id,
  name: concept.name,
  confinement_family: concept.confinement_family,
  analysis_id: concept.analysis_id
});

// After:
_selected.set(concept.concept_id, {
  concept_id: concept.concept_id,  // Now analysis ID
  name: concept.name,
  confinement_family: concept.confinement_family
  // analysis_id: REMOVED — concept_id IS the analysis ID
});
```

**Chip rendering** (line 287):
```javascript
// Before:
if (!concept.analysis_id) {
  chip.classList.add("selection-tray__chip--no-model");
}

// After: Need a way to check if concept has a cost model.
// _modeledIds (from manifest) contains analysis IDs. concept.concept_id is now analysis ID.
if (!_modeledIds || !_modeledIds.has(concept.concept_id)) {
  chip.classList.add("selection-tray__chip--no-model");
}
```

This requires `_modeledIds` to be accessible in the selection tray. Currently `TaxonomyCards` has it but `SelectionTray` doesn't. Need to add a `setModeledIds()` function to `SelectionTray`, called from `taxonomy.js` alongside the existing `TaxonomyCards.setModeledIds(modeledIds)` call.

**Popover** (line 197):
```javascript
// Before:
if (!concept.analysis_id) {

// After:
if (!_modeledIds || !_modeledIds.has(concept.concept_id)) {
```

**`_navigateToCompare()`** (line 325-328): No change — `getIds()` returns analysis IDs, which is what the compare page expects.

**`_restoreFromUrl()`** (line 348-359): No change — URL has `?selected=01,04`, `_registry["01"]` returns the concept since registry is now keyed by analysis ID.

#### `view_categorical.js` (lines 89-92)
```javascript
// Before (workaround):
const key = c.analysis_id || c.concept_id;

// After (clean):
const key = c.concept_id;
```

Also lines 110, 146, 198, 222 — all `taxonomyData[c.concept_id]` lookups. These work because `taxonomyData` is built from the registry API response keyed by `concept_id` (analysis ID), and `c.concept_id` from `ConceptData` is already the analysis ID.

#### `constellation.js`, `neighborhood_graph.js`

No code changes. These use `concept_id` from API responses, which will now be analysis IDs. All lookups go through `_registry[conceptId]` which is keyed by analysis ID.

#### `tree_view.js` (line 103)

Tree leaf labels initially show the raw concept ID. Currently this is a readable slug like "hts-compact-tokamak". After the change, it'll briefly show "01" until `updateLeafLabels(nameMap)` replaces it with the concept name. This is a visual flash during load — acceptable since it's <100ms.

### 6. Tests (`test_taxonomy_models.py`)

**Lines 255-283** — `test_analysis_id_populated_for_all_concepts` and `test_analysis_id_spot_checks`:
- Delete both tests (they test `analysis_id` which no longer exists)
- Replace with: `test_concept_id_is_analysis_id` — verify `concept_id` is the analysis directory ID for spot-checked concepts

**Lines 249**: `registry.by_id("p-b11-frc")` → `registry.by_id("09")` (or whatever the analysis ID is)
- All `by_id()` calls in tests that currently pass slugs must be updated to analysis IDs

**Lines 51, 76, 90, etc.**: Test `ConceptTaxonomy` construction — change `concept_id="hts-compact-tokamak"` to `concept_id="01"`, add `slug="hts-compact-tokamak"`

**Add new tests:**
- `test_by_slug()` — verify `by_slug("hts-compact-tokamak")` returns the correct concept

**`test_taxonomy_server.py`** (lines 195, 214):
- Update route calls to use analysis ID instead of slug
- Update assertions

### 7. Change Summary

| File | Type of change |
|------|---------------|
| `taxonomy_models.py` | Rename fields, add `slug`, add `by_slug()` |
| `seed_registry.py` | Swap field assignments in `_parse_row()` |
| `similarity.py` | **No changes** |
| `server.py` | **No changes** |
| `concept_registry.json` | **Regenerated** by seed script |
| `decision_tree.json` | **Regenerated** by seed script |
| `taxonomy.js` | **No changes** (values change, code doesn't) |
| `taxonomy_card.js` | `analysis_id` → `concept_id` (2 lines) |
| `selection_tray.js` | Remove `analysis_id`, add `_modeledIds` check (~6 lines) |
| `view_categorical.js` | Remove workaround (1 line + 2 comment lines) |
| `constellation.js` | **No changes** |
| `neighborhood_graph.js` | **No changes** |
| `tree_view.js` | **No changes** |
| `comparison.js` | **No changes** |
| `test_taxonomy_models.py` | Update all slug→analysis_id in test data, update assertions |
| `test_taxonomy_server.py` | Update route calls and assertions |

## Potential Risks

1. **Tree leaf label flash**: Leaves briefly show "01" instead of "hts-compact-tokamak" before `updateLeafLabels` runs. Mitigation: Acceptable (<100ms), and the current slugs weren't great labels either (hyphens, no caps).

2. **Broken bookmarks**: Anyone with `?selected=hts-compact-tokamak` bookmarks will lose their selection. Mitigation: This is a dev-only tool, no external users.

3. **Similarity test regressions**: Tests that assert specific concept IDs in similarity results will need updating. Mitigation: Run full test suite after changes.

## Integration Strategy

This is a pure refactor — no new features, no new files. The change propagates from the data model outward:

1. Change Python models + seed script
2. Regenerate data files
3. Update JS consumers
4. Update tests
5. Run full test suite + manual smoke test

All existing pages continue to work because the analysis ID values are already present in the data — they're just accessed through a different field name.

## Validation Approach

### Automated
- `uv run python -m pytest exploration/concept_explorer/tests/` — all tests pass
- `grep -rn "analysis_id" exploration/` — zero hits

### Manual Smoke Test
- Taxonomy page: tree view loads, click concept → neighborhood graph, similarity panel works
- Constellation: dots render, click → focus works
- Selection tray: Ctrl+click adds concepts, chips show, "No cost model" indicator correct
- Compare navigation: select concepts on taxonomy → "Landscape" button → compare page loads with correct concepts
- Concept profile: `/concept/04` loads correctly
- Index page: concept list links work

---

**Next Step:** Awaiting DD-1 decision, then → `/_my_plan` or `/_my_implement`
