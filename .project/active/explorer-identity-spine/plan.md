# Implementation Plan: Explorer Identity & Shared Spine (Theme A)

**Status:** All phases complete (A1 + A2 + A3 done) — ready for audit
**Created:** 2026-06-06 15:05 PDT
**Last Updated:** 2026-06-06

## Source Documents
- **Spec:** `.project/active/explorer-identity-spine/spec.md`
- **Design:** `.project/active/explorer-identity-spine/design.md` ← component details, decisions, invariants, gotchas

## Implementation Strategy

**Phasing Rationale:** A1 (identity) is foundational *and* riskiest — Option B's correctness rests on every served concept's CSV/registry name already being clean `Name (Fuel)`. So Phase 1 leads with that audit, then builds the server-side resolution; Phase 2 wires the surfaces. A3 (caveat) is the next visible win. A2 (palette/facets) is groundwork with no on-screen payoff until B1's matrix, so it lands last. See `design.md#key-bets--decisions` (D1/D2/D4 settled).

**Critical Path:** name-cleanliness audit → `resolve_identity()` + payload stamping → `conceptLabel()` + surface wiring → caveat consolidation → palette/facet exports.

**First Proof Point:** Phase 1's audit + `resolve_identity` unit tests. If the audit shows the CSV names aren't uniformly `Name (Fuel)`, Option B needs an honest fallback before any surface is touched.

**Overall Validation Approach:** Each phase starts with tests; backend phases use pytest, frontend phases use browser-inspect (per `.claude/skills/browser-inspect/SKILL.md`) plus grep-guards for the single-authority invariants in `design.md#required-invariants`. Test command: `uv run python -m pytest exploration/concept_explorer/tests/`.

---

## Phase 1: Identity Resolution (Backend)

### Goal
Establish one server-side identity authority (`resolve_identity`) sourced from the CSV/registry, stamped onto both served payloads. First, prove the CSV names are clean `Name (Fuel)`.

### Assumption Under Test
Every *served* concept's registry name is already `Name (Fuel)` (so the overlay needs no name-recomposition), and `concept_id` is a usable `#code` including suffix variants.

### Test Stencil (Write This First)
```python
# tests/test_identity.py
def test_resolve_identity_normal():
    ident = resolve_identity("01")          # registry-backed
    assert ident.code == "01"
    assert ident.name == "HTS Compact Tokamak (D-T)"   # Name (Fuel), not the company form
    assert ident.fuel == FuelType.DT

def test_resolve_identity_suffix_variant():
    assert resolve_identity("17a").code == "17a"

def test_resolve_identity_fuel_missing():        # honest: base name, no "(None)"
    ident = resolve_identity("<fuel-na-id>")
    assert "(None)" not in ident.name

def test_resolve_identity_not_in_registry():     # degrade, never throw/blank
    ident = resolve_identity("<served-but-unregistered>")
    assert ident.name and ident.code
```

### Changes Required

**See `design.md` for:** `#architecture` (identity data flow), `#component-overview` (`resolve_identity`), `#required-invariants`, `#implementation-notes` (fuel-missing, suffix variants, family-color key).

- [x] **Audit script/test** — assert every served concept's `concept_registry.json` name matches `Name (Fuel)` (or is a documented honest exception). This is the de-risk gate; run before anything else. *(Result: 35/36 clean; concept 35 `PoloMac Magnetic Confinement` omits the suffix despite a known D-D fuel → **Option 1 (compose from structured fuel)** confirmed by user. Audit now asserts the post-resolution invariant.)*
- [x] **`resolve_identity(concept_id)`** in `server.py` — reads from the loaded registry, returns `Identity{code, name, fuel}`; honest fallback when not in registry. Signature is `resolve_identity(concept_id, registry, *, served_name=None)` (registry passed explicitly, not via global, for testability — adapts the stencil's single-arg form).
- [x] **Stamp both payloads at load** — overlay `name`/`fuel` onto served `ConceptData` (code == `concept_id`); registry names composed in `_load_taxonomy` before similarity/constellation derive from them; retain the frontmatter name as `analyst_name`. Doc-comment added on `ConceptData.name`.
- [x] **`tests/test_identity.py`** (NEW) — the stencil + audit assertion + end-to-end both-layers + manifest checks (14 tests).

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_identity.py` → 14 passed
- [x] Full suite → no regressions (241 passed excluding the manual Playwright suites; the 6 `test_extract_adapter` failures and 39 `test_views_manual`/`test_integration_manual` setup errors are pre-existing — verified identical against committed code via `git stash`).
**Manual:**
- [x] Hit `/api/concepts/01` and `/api/taxonomy/concepts/01` → both return `name = "HTS Compact Tokamak (D-T)"`, `code = "01"`. *(Promoted to an automated parametrized test: `test_both_layers_serve_canonical_identity` covers 01 / 24 / 35.)*

**What We Know Works After This Phase:** identity is resolved once, server-side, consistent across both layers; the clean-name assumption is proven (35/36) and its single exception (35) documented and composed.

---

## Phase 2: Identity (Frontend Surfaces)

### Goal
Every surface renders `#NN Name (Fuel)` through one helper; the code becomes a visible handle.

### Assumption Under Test
One `conceptLabel()` can serve all naming surfaces without per-page special-casing.

### Test Stencil (Write This First)
```javascript
// conceptLabel returns the canonical parts; surfaces compose from it
test("conceptLabel renders code + Name (Fuel)", () => {
  const { code, name } = conceptLabel({ concept_id: "17a", name: "Laser ICF ... (D-T)" });
  expect(code).toBe("17a");
  expect(name).toMatch(/\(.+\)$/);            // fuel suffix present
});
```

### Changes Required

**See `design.md` for:** `#architecture` (conceptLabel), `#required-invariants` (no direct `.name` reads).

- [x] **`conceptLabel()`** new small JS module (`static/js/concept_label.js`, `window.conceptLabel`) returning `{code, name, codeText, text, codeChip()}`. DOM sites use `.codeChip()` + `.name`; Plotly/Cytoscape/`textContent` sites use `.text` (`"#NN Name (Fuel)"`).
- [x] **Wire surfaces** through it, each showing the `#code`: cards (`index_page.js`), hero + breadcrumb + title (`concept_page.js`), sticky headline (`sticky_headline.js`), compare chips/picker/placeholder/landscape (`comparison.js`), constellation hover (`constellation.js`), taxonomy card + neighbor-table headers + neighbor list (`taxonomy_card.js`), parameter-card links (`parameter_card.js`). New `.concept-code` CSS token (muted monospace chip). `concept_label.js` added to all four templates before the surface scripts.
- [x] **Grep-guard test** (`tests/test_identity_frontend.py`, 19 tests) — each surface calls `conceptLabel(`; no raw payload `.name` label renders; templates load the helper first.

### Validation
**Automated:** [x] full suite passes (260, excl. pre-existing manual/adapter); [x] grep-guard passes (19).
**Manual (browser-inspect):**
- [x] Verified live (session `identity*`): cards `#33 …`, `#20b Renaissance Stellarator (D-T)`, `#06 Magnetic Mirror (p-B11)`; **PoloMac card `#35 PoloMac Magnetic Confinement (D-D)`** (composed suffix live); concept 17a hero/breadcrumb/title all `#17a Laser ICF - Hybrid Direct Drive (D-T)`; compare chips `#01 …` / `#24 Dense Plasma Focus (p-B11)`; constellation hover `#01 HTS Compact Tokamak (D-T)`; taxonomy card `#12 Levitated Dipole (D-T)` + neighbor list with codes. **Zero page errors** (only pre-existing cytoscape `cursor:pointer`/wheel warnings).

**What We Know Works After This Phase:** A1 complete — one label, one code, everywhere.

**Scope note (spec-honoring, not a skip):** the spec's surface enumeration (spec.md:67) covers landing cards / hero+breadcrumb+sticky / compare columns+picker+placeholders / constellation / taxonomy card / neighbor tables / parameter links — all wired. It deliberately does **not** include the compare *integrated chart views* (`view_capex/summary/sensitivity/categorical`) or the neighborhood **cytoscape graph** node labels; those still render the canonical name (server-stamped) but no `#code` chip, by design (keeping codes on the identity chrome, not every chart axis).

---

## Phase 3: Honest-Caveat Consolidation (A3)

### Goal
One `caveatMarker()` replaces the six duplicated low-grounding sites; `fit_grade` arrives via the server-load overlay; absent fields announce themselves.

### Assumption Under Test
`fit_grade` is available from `tables/archetype_fit.csv` at server load (no per-concept re-extraction), and one component covers all four caveat dimensions across all sites.

### Test Stencil (Write This First)
```python
def test_fit_grade_in_overlay():
    payload = served_concept("01")
    assert payload.fit_grade in {"High","Med","Low","None", None}
```
```javascript
test("caveatMarker covers asterisk, fit None, not-recorded", () => {
  expect(caveatMarker({ asterisk: true }).title).toMatch(/single-source/);
  expect(caveatMarker({ fitGrade: "None" })).toBeTruthy();
  expect(caveatMarker({ missing: "fit_grade" }).title).toMatch(/not recorded/i);
});
```

### Changes Required

**See `design.md` for:** `#research-findings` (asterisk folds in single-source; the 6 sites), `#component-overview` (`caveatMarker`), `#non-goals` (one marker, not the D3 maturity panel).

- [x] **`fit_grade` via overlay** — `_load_fit_grades(archetype_fit.csv)` at startup (codes via `id.split("-",1)[0]`, so `17a`/`20b` carry through); `_stamp_identity` stamps `fit_grade` onto `ConceptData` and `ConceptManifestEntry` (so cards/picker get it without a fetch). Recorded `"None"` preserved as distinct from absent (Python `None`).
- [x] **`caveatMarker()`** new JS module (`static/js/caveat_marker.js`, `window.caveatMarker`) — inputs `{asterisk, fitGrade, missing}`; returns `{any, title, glyph, element(), html()}`. DOM sites use `.element()`; the cytoscape/innerHTML tooltip uses `.html()`.
- [x] **Replace the marker sites** — 5 real sites (the design's "6th, graph node styling" doesn't exist as code): `index_page.js`, `concept_page.js` (hero), `taxonomy_card.js`, `comparison.js` (`lowGroundingMarker` delegates; 2 call sites), `neighborhood_graph.js` (`lowGroundingMarkup` delegates; 3 tooltips). `taxonomy.js` patches `fit_grade` onto registry entries (like asterisk). New `.caveat-marker` CSS (aliases the old `.low-grounding-marker`).
- [x] **Honest-absence variant** — concept-page hero passes `missing:"Archetype fit"` when `fit_grade == null`, so an unrecorded grade renders "not recorded" instead of vanishing (FR-A3.3). (Never fires in current data — all 36 served concepts have a fit row — but wired + tested.)
- [x] Tests (`tests/test_caveat.py`, 18): fit-grade load/overlay/manifest + single-authorship grep-guard + delegation + template load-order. Behavioral stencil verified live in-browser.

### Validation
**Automated:** [x] new tests pass (18); [x] full suite (278, excl. pre-existing manual/adapter); [x] grep-guard (single authorship — ⚠/marker markup only in `caveat_marker.js`).
**Manual (browser-inspect):**
- [x] Verified live (session `caveat*`): `caveatMarker({asterisk:true}).title` → /single-source/; `{fitGrade:'None'}` → truthy + archetype title; `{missing:'fit_grade'}` → "fit_grade not recorded."; `{fitGrade:'High'}` → no marker (`element()===null`). Markers render on the **PoloMac card**, **concept-35 hero** (`#35 … (D-D) ⚠`, fit-None title), **compare chip 02** (01 High → none), and **taxonomy card 02**. Zero page errors (only pre-existing cytoscape + concept-35 `[tornado] Missing parameterMetadata` warnings — a data-coverage issue independent of A3).

**What We Know Works After This Phase:** A3 complete — one caveat device, honest degradation, no silent vanish on covered fields.

---

## Phase 4: Palette + Facet/Filter Model (A2)

### Goal
One ontology color authority traceable to `concept_ontology_v3.png`; JS color duplication deleted; facet + filter-state models exported for B1/C1. No widget.

### Assumption Under Test
The PNG colors can be sampled into a token set, and existing family colors can be re-sourced from it with zero visual change.

### Test Stencil (Write This First)
```javascript
test("one family-color authority; constellation imports it", () => {
  expect(ontologyPalette.family.MFE).toBe("#3b82f6");   // from token authority
  // grep-guard (separate): no hard-coded family hexes remain in constellation.js
});
test("facet model is importable and lists the ontology dimensions", () => {
  expect(facetModel.map(f => f.key)).toEqual(
    expect.arrayContaining(["family","fuel","magnet","driver"]));
});
```

### Changes Required

**See `design.md` for:** `#architecture` (palette/facet flow), `#key-bets--decisions` (Bet 3: small visible footprint), `#implementation-notes` (don't let A2.3 drift; family color keys off the enum).

- [x] **PNG palette → `:root` dimension tokens** (`explorer.css`) — `--onto-{dim}-{value}` for fuel/magnet/driver/capture/blanket/opmode/reprate + fit-grade/has-cost-model, hexes copied verbatim from the PNG **generator** `exploration/phase_1a/generate_ontology_chart.py` (PALETTES dict) and cited — the traceable source that *produced* `concept_ontology_v3.png`.
- [x] **Shared JS color map** (`ontology_palette.js`) — reads every color from CSS `:root` via `getComputedStyle` (CSS is the single authority; **zero hex literals in JS**). Deleted **5** `FAMILY_COLORS` dicts (not just constellation: also `neighborhood_graph.js`, `view_capex/summary/sensitivity.js`) and re-sourced from `ontologyPalette.family`. Family badges already keyed off `--color-badge-*` CSS tokens (unchanged).
- [x] **Facet model + filter-state model** — `window.facetModel` (10 facets: family/fuel/magnet/driver/capture/blanket/opMode/repRate/fitGrade/hasCostModel, each value→{label,color}, + payload `field`); `window.filterState` (`create/toggle/isEmpty/matches`, AND-across/OR-within). No widget.
- [x] Tests (`tests/test_palette.py`, 14): no-JS-hex authority guard, family-dedup + re-source, family tokens unchanged, dimension tokens trace to generator, template load-order. Stencil (`ontologyPalette.family.MFE`, `facetModel` keys, `filterState`) verified live in-browser.

### Validation
**Automated:** [x] tests pass (14); [x] grep-guard (no family hexes / no FAMILY_COLORS dicts; ontology_palette.js hex-free); [x] full suite (292, excl. pre-existing manual/adapter).
**Manual (browser-inspect):**
- [x] **Visually unchanged** verified: constellation marker colors `{MFE #3b82f6, IFE #a855f7, MIF #f59e0b, NONSTANDARD #6b7280}` — identical to before; family badge backgrounds `rgb(59,130,246)` = `#3b82f6`; index/compare render identical. `ontologyPalette.family` resolves from CSS; `facetModel` lists all 10 facets; `filterState.matches` works. **Zero console / page errors** (every CSS token resolved — no missing-token warnings). palette↔PNG mapping documented in `:root` + `ontology_palette.js`.

**What We Know Works After This Phase:** A2 groundwork complete — one palette authority + importable facet/filter models ready for B1, duplication gone.

---

## Environment Setup

**See CLAUDE.md** — `uv run python ...` only. Tests: `uv run python -m pytest exploration/concept_explorer/tests/`. Browser checks: `browser-inspect` skill.

## Risk Management

**See `design.md#potential-risks`.** Phase-specific:
- **Phase 1:** the clean-`Name (Fuel)` assumption — *the audit is the first action*; any exception gets a documented honest fallback before surfaces are touched.
- **Phase 3:** `fit_grade` source moved to overlay — verify `archetype_fit.csv` covers all served concepts; honest "not recorded" where it doesn't.
- **Phases 2–3:** consolidating shared call sites can regress one surface — browser-inspect each of the four surface types.
- **Phase 4:** invisible groundwork reads as "did nothing" — the verifiable output is the token authority + deleted duplication, not a pixel change.

## Audit Resolution (2026-06-07)

Post-implementation audit (`/_my_audit_implementation`) findings, all addressed:

- **M1 (major) — identity grep-guard false confidence.** `test_no_raw_name_label_render` scanned a fixed 7-file allowlist (couldn't catch a new/unwired surface), inconsistent with the Phase 3/4 glob guards. **Fixed:** rewritten to glob *every* `*.js` with a documented `_RAW_NAME_EXCLUDED` set (the helper, the out-of-scope chart views + cytoscape graph, and `cas_breakdown.js`'s non-concept tile names). It now actively protects all in-scope surfaces.
- **m1 (minor) — two surfaces rendered the name without the `#code`.** `selection_tray.js` (comparison popover + tray chips) and `taxonomy.js:275` ("Neighborhood of …"). These were oversights, not the deliberate spec-line-67 exclusions. **Fixed:** wired through `conceptLabel()`; both added to `_TOUCHED`. Browser-confirmed: heading now "Neighborhood of #12 Levitated Dipole (D-T)".
- **m2 (minor) — `_compose_name` double-suffix on contradictory data.** A registry name ending in a *different* fuel suffix than the structured fuel would get two suffixes. Zero occurrences (Phase-1 audit confirms). **Decision: not a logic change** — stripping would mask the data bug and could mangle legitimate non-fuel parentheticals; the Phase-1 audit is the real guard. Added a clarifying doc-comment in `server.py`.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-06-06

**Audit / de-risk gate result:** 35 of 36 served (non-omitted) concepts have a clean `Name (Fuel)` registry name. All 40 registry concepts carry a real structured fuel (28 DT, 6 PB11, 4 DD, 2 DHe3) — `FUEL_MAP` only maps the four real fuels, so the design's feared *fuel-missing / `(None)`* case **does not occur in current data** (still coded + tested defensively per FR-A1.5). One exception: **concept 35** (`PoloMac Magnetic Confinement`, fuel D-D) omits the suffix in the authored CSV name. **Decision (user, 2026-06-06): Option 1 — compose `(D-D)` from the structured fuel** (real data, not a fabricated fallback), satisfying FR-A1.1 universally rather than shipping the one spec-violating exception Option 2 (the design's literal "as-authored" risk-table wording) would have left.

**Changes Made:**
- `models.py`: added `FUEL_DISPLAY` (the single fuel→display authority, OTHER→"" so no `(OTHER)`/`(None)`); added `analyst_name: str|None` and `fuel: FuelType|None` overlay fields to `ConceptData` with doc-comments clarifying the on-disk `name` is analyst frontmatter phrasing, overwritten in memory at load.
- `server.py`: added `Identity` dataclass, `_compose_name()` (idempotent suffix composition), `resolve_identity(concept_id, registry, *, served_name=None)` (the single identity authority, honest degradation when absent), and `_stamp_identity()` (overlays ConceptData + rebuilds manifest/parameter index from stamped concepts). `_load_taxonomy` now composes registry names *before* similarity/constellation derive from them. Lifespan calls `_stamp_identity` after both loaders.
- `tests/test_identity.py` (NEW, 14 tests): audit gate, `resolve_identity` normal/suffix-variant/not-in-registry/none-registry, the documented 35 exception, `_compose_name` idempotence + honest fuel-missing, and end-to-end both-layers/manifest/analyst-name retention.

**Issues Encountered:**
- Pre-existing test noise: 6 `test_extract_adapter` failures + 39 manual-Playwright setup errors. Verified pre-existing (identical against committed code via `git stash`); not caused by this work.

**Deviations from Plan:**
- `resolve_identity` takes the registry explicitly (not from a global) — cleaner and matches the existing test-fixture pattern; the stencil's single-arg form was illustrative. `code` is not a new stored field (it equals `concept_id`, already present); only `name`/`fuel`/`analyst_name` are stamped onto `ConceptData`.
- Registry-name composition for the taxonomy layer happens inside `_load_taxonomy` (so similarity reports + constellation see canonical names), not only in `_stamp_identity`; `_compose_name`'s idempotence makes the double pass safe.

### Phase 2 Completion
**Completed:** 2026-06-06

**Changes Made:**
- `static/js/concept_label.js` (NEW): `window.conceptLabel(c)` → `{code, name, codeText, text, codeChip()}`. The one front-end naming authority; pairs the server-stamped canonical `name` with the visible `#code` handle.
- `static/css/explorer.css`: new `.concept-code` token (muted monospace) for the code chip.
- Wired surfaces: `index_page.js` (cards), `concept_page.js` (hero, breadcrumb, title, override-panel name), `sticky_headline.js` (crumb), `comparison.js` (concept-bar chips, picker items, placeholder rows, landscape cells), `constellation.js` (Plotly hover text), `taxonomy_card.js` (card header, comparison table headers, neighbor list), `parameter_card.js` (cross-concept links).
- Templates: `concept_label.js` added to index/concept/compare/taxonomy before the surface scripts.
- `tests/test_identity_frontend.py` (NEW, 19 tests): helper-adoption + no-raw-`.name`-render grep-guard + template load-order.

**Issues Encountered:**
- *Misplaced new files (resolved):* the Write tool resolves relative paths against the shell cwd, so `concept_label.js` and `test_identity_frontend.py` first landed under `static/js/exploration/...`. Moved to the correct paths and removed the stray nested dirs. Use absolute paths for Write.
- *Stale server:* a previously-running server held `dist/` with old templates; restarted to pick up the new `concept_label.js` script tag.

**Deviations from Plan:**
- The helper returns string forms (`text`/`codeText`) in addition to `codeChip()`, because Plotly trace text and Cytoscape/`textContent` sites can't take a DOM node — the design's "(+ optional element)" is realised as both a chip element and string forms.
- Wired the compare **landscape cells** too (same file, same identity concern) beyond the literal "columns/picker/placeholder" wording — they're a compare naming surface. Integrated chart views + cytoscape graph left name-only per the spec enumeration (see scope note above).

### Phase 3 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `models.py`: `fit_grade: str | None` on `ConceptData` and `ConceptManifestEntry`; `build_manifest` copies it. Doc-comment flags the recorded-`"None"` vs absent (`None`) distinction.
- `server.py`: `_load_fit_grades(csv_path)` (non-fatal; `{}` if file absent); `_stamp_identity` extended to stamp `fit_grade`; lifespan computes `fit_csv_path = base_dir.parent / "concept_analysis" / "tables" / "archetype_fit.csv"` and passes the grades. `import csv` added.
- `static/js/caveat_marker.js` (NEW): `window.caveatMarker(inputs)` — the one honest-caveat device (`element()` + `html()` forms).
- `static/css/explorer.css`: `.caveat-marker` (aliases `.low-grounding-marker`).
- Delegated the 5 marker sites: `index_page.js`, `concept_page.js` (hero, + honest-absence `missing`), `taxonomy_card.js`, `comparison.js` (`lowGroundingMarker`), `neighborhood_graph.js` (`lowGroundingMarkup`). `taxonomy.js` patches `fit_grade` onto registry entries. `caveat_marker.js` added to all four templates.
- `tests/test_caveat.py` (NEW, 18 tests).

**Issues Encountered:**
- Pre-existing concept-35 `[tornado] Missing parameterMetadata` console warnings (incomplete `parameter_metadata` coverage — same keys behind the long-standing pydantic UserWarning). Data-coverage issue, independent of A3; not introduced here.

**Deviations from Plan:**
- The design's "6 sites incl. graph node styling" — only **5** real marker sites exist; there is no low-grounding node-styling code in `neighborhood_graph.js` (node classes are center/neighbor/bridge). Consolidated the 5.
- `fit_grade` also added to `ConceptManifestEntry` (+ `taxonomy.js` patch) — the design said "add to `ConceptData`," but cards / compare picker / taxonomy surfaces read the manifest/registry, so the grade had to ride the same rails as the asterisk to render there.
- Marker now flags **archetype-fit `"None"`** in addition to the asterisk on every delegated surface (the consolidation win); `Med`/`Low` are not flagged (spec lists only "None").

### Phase 4 Completion
**Completed:** 2026-06-07

**Source for the palette:** the PNG `concept_ontology_v3.png` is a rendered heatmap; its **generator** `exploration/phase_1a/generate_ontology_chart.py` holds the exact `PALETTES` hex dict that produced it — the authoritative, traceable source (better than pixel-sampling). Family band colors there (MFE `#3b50a0`) differ from the explorer's family colors (MFE `#3b82f6`); per design Bet 3 + the test stencil, the explorer keeps its existing family colors (zero visual change) and the PNG supplies the *dimension* vocabulary.

**Changes Made:**
- `static/css/explorer.css`: ontology dimension tokens added to `:root` (`--onto-*`, copied from the generator, cited); family-token comment marks `:root` as the single family-color authority.
- `static/js/ontology_palette.js` (NEW): reads every color from `:root` via `getComputedStyle` (no JS hex). Exports `window.ontologyPalette` (family + 9 dimension maps), `window.facetModel` (10 facets), `window.filterState` (create/toggle/isEmpty/matches).
- Deleted 5 `FAMILY_COLORS` literal dicts (`constellation.js`, `neighborhood_graph.js`, `view_capex.js`, `view_summary.js`, `view_sensitivity.js`) → `const/var FAMILY_COLORS = ontologyPalette.family`. Fixed `constellation.js` family fallback hex → `FAMILY_COLORS.NONSTANDARD`. `ontology_palette.js` added to all four templates before consumers.
- `tests/test_palette.py` (NEW, 14 tests).

**Issues Encountered:**
- The generic grey `#6b7280` is shared by the family NONSTANDARD color *and* the CAS-account/fallback grey, so it can't be guarded per-file by hex; the grep-guard checks the 3 distinctive family hexes (`#3b82f6/#a855f7/#f59e0b`) plus the literal-dict + re-source checks.

**Deviations from Plan:**
- **5** `FAMILY_COLORS` duplications, not 1 — the design named only `constellation.js`, but the same dict was copy-pasted into 4 more JS files; the single-authority principle (and the "no family hexes in JS" grep-guard) required all 5.
- Palette source is the PNG **generator script** (exact hexes), not pixel-sampling the PNG image — more accurate and genuinely traceable.
- CSS `:root` is the single authority and JS derives from it (`getComputedStyle`), per the design's architecture diagram — so the JS map holds zero hex literals.
- The compare integrated views (`view_*.js`) were updated here (they held `FAMILY_COLORS` copies) even though Phase 2 left their *naming* alone — A2 is a color concern, and their family-color duplication was in scope for the dedup.

### (template) Phase 1 Completion
### (template) Phase 2 Completion
### (template) Phase 3 Completion
### (template) Phase 4 Completion
### Phase 3 Completion
### Phase 4 Completion

---

**Status**: Draft → In Progress → **Implementation Complete** (all 4 phases; awaiting audit)
