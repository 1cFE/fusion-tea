# Implementation Plan: Cost Landscape Page (Theme F)

**Status:** Complete (all 5 phases; re-extract held per user)
**Created:** 2026-06-07
**Last Updated:** 2026-06-07

## Source Documents
- **Spec:** `.project/active/explorer-cost-landscape/spec.md`
- **Design:** `.project/active/explorer-cost-landscape/design.md` ← component details, decisions D1–D7, invariants I1–I6, architecture

## Implementation Strategy

**Phasing Rationale:** Build outward from the data. Phase 1 proves the decomposition is real and exact (the bet everything rests on), Phase 2 packages it server-side, Phase 3 proves the matrix-grouping reuse on a non-matrix surface *before* the Plotly work, Phase 4 is the visual core, Phase 5 is interaction + edges. Each phase is independently testable and leaves the tree green.

**Critical Path:** P1 (cas71/72 + sum-to-LCOE) → P2 (`/api/cost-landscape`) → P3 (page + nav + grouping reuse) → P4 (stacked bars + axis + color) → P5 (hover/click/caveat/degradation).

**First Proof Point:** Phase 1's sum-to-LCOE test passing on re-extracted data — confirms the four components decompose the headline exactly (I1, Bet B1).

**Overall Validation Approach:** Test-first each phase; `uv run python -m pytest` for automated, `browser-inspect` skill for UI; full suite each phase for no regressions.

---

## Phase 1: Extractor split + re-extract + sum-to-LCOE test

### Goal
Surface `cas71`/`cas72` in the extracted JSON and prove the four annualized components sum to the stored headline LCOE. De-risks the entire feature.

### Assumption Under Test
The four components (CAS90/CAS71/CAS72/CAS80) decompose LCOE exactly (I1) — and `cas71`/`cas72` are already in the costingFE `CostResult` (`types.py:268-270`), so surfacing them is a pure `models.py` change (no costingFE wrapper needed).

### Test Stencil (Write This First)
```python
# tests/test_cost_landscape_decomposition.py (NEW)
@pytest.mark.parametrize("cid", ["01", "24", "23"])
def test_components_sum_to_headline_lcoe(cid):
    cm = load_concept(cid).cost_model
    ann = cm.cas70.cost_m_usd + cm.cas80.cost_m_usd + cm.cas90.cost_m_usd
    lcoe = cm.headline.lcoe_per_mwh
    parts = [cm.cas90, cm.cas71, cm.cas72, cm.cas80]
    got = sum(p.cost_m_usd / ann * lcoe for p in parts)
    assert got == pytest.approx(lcoe, rel=1e-6)
    assert cm.cas71.cost_m_usd + cm.cas72.cost_m_usd == pytest.approx(cm.cas70.cost_m_usd, rel=1e-6)
```

### Changes Required
**See `design.md#component-overview` and `#appendix` for field locations.**

- [x] `tests/test_cost_landscape_decomposition.py` (NEW) — served-data B1/I1 reconstruction (01/24/23) + split wiring (cas71+cas72==cas70) + honest-degradation (absent→None). 9 tests, all pass.
- [x] `models.py` `CostModelData` — added `cas71: CASAccount | None = None`, `cas72: CASAccount | None = None` (**optional**, not required — see Phase 1 notes) + `CAS_NAMES` entries ("Fixed O&M (annualised)", "Scheduled Replacement (annualised)"; cas70 label unchanged).
- [x] `models.py` `from_forward_result` — builds `cas71`/`cas72` from `costs` when the key is present, else `None` (absent→None policy at the call site).
- [x] `extract_explorer_data.py` `_freeform_to_explorer_dict` — already emits cas71/72 (`:511-512`); costingfe path emits them via `dataclasses.asdict(CostResult)` (`types.py:268-270`). Confirmed: no extractor change needed.
- [ ] **HELD (per user, 2026-06-07):** Re-extract served concepts: `uv run python exploration/concept_explorer/extract_explorer_data.py --skip-narrative` — deferred until the active 1 GWe override-policy churn settles, to avoid stacking stale outputs.

### Validation
**Automated:**
- [x] `uv run python -m pytest tests/test_cost_landscape_decomposition.py` → 9 passed
- [x] Full suite → no regressions (309 passed; the only failures are the pre-existing manual/adapter exclusions, confirmed identical with my change stashed)
**Manual:**
- [ ] **DEFERRED with the re-extract:** Inspect a re-extracted `data/01.json` → `cost_model.cas71`/`cas72` present and sum to `cas70`. (Today the served JSON carries only combined `cas70`; the split-present-in-served-JSON proof rides the held re-extract.)

**What We Know Works After This Phase:** The schema carries the split, the wiring builds it, and the annualised components reconstruct the stored headline LCOE exactly on the *current* served data (B1/I1) — without the re-extract. The remaining proof (split present in the re-extracted JSON) is held with the re-extract.

---

## Phase 2: Server aggregate `/api/cost-landscape`

### Goal
A purpose-built endpoint serving per-costed-concept `{lcoe, components{capital,fixed_om,replacement,fuel}, overrides[compact]}`, built from in-memory `ConceptData` with server-side account→component roll-up.

### Assumption Under Test
The roll-up is total (I6) — every override account maps to exactly one component — and the aggregate is cheap to build from `state.concepts`.

### Test Stencil (Write This First)
```python
# tests/test_cost_landscape_api.py (NEW)
def test_rollup_is_total_and_components_present():
    landscape = build_cost_landscape(load_all_concepts())
    for row in landscape.concepts:
        assert set(row.components) == {"capital", "fixed_om", "replacement", "fuel"}
        for ov in row.overrides:
            assert ov.component in {"capital", "fixed_om", "replacement", "fuel"}
```

### Changes Required
**See `design.md#component-overview` (build_cost_landscape) and `#implementation-notes` (override→component map).**

- [x] `tests/test_cost_landscape_api.py` (NEW) — roll-up totality (I6), concept 01 capital override (C220103), LCOE==headline, only-costed-concepts, endpoint shape, roll-up-map unit (incl. CAS70→fixed_om + fail-loud on unknown), rationale-short (first sentence / abbreviation-safe / structured-basis fallback / None). 22 tests.
- [x] `models.py` — `CostComponent` (enum), `CostComponents`, `CompactOverride`, `CostLandscapeEntry`, `CostLandscape`, `build_cost_landscape()` + `_override_component()` + `_override_rationale_short()`/`_first_sentence()` helpers. (Builder lives in models.py beside `build_manifest`/`build_parameter_index` — see notes.)
- [x] `server.py` — imports + `cost_landscape` on `_State`; built in `lifespan` from stamped concepts; `api_cost_landscape` route mirroring `api_get_manifest`; registered `/api/cost-landscape`.

### Validation
**Automated:**
- [x] `pytest tests/test_cost_landscape_api.py` → 22 passed; full suite 331 passed (only pre-existing manual/adapter exclusions fail).
**Manual:**
- [x] TestClient `GET /api/cost-landscape` → 36 costed concepts; concept 01 shaped `{lcoe 155.17, components{capital 1006.5, fixed_om null, replacement null, fuel 0.93, om_combined 147.99}, overrides[C220103→capital, CAS27→capital]}`.

**What We Know Works After This Phase:** The page has a single, correct data source.

---

## Phase 3: Page scaffold + nav + data join + grouping (no chart)

### Goal
New page/route/template; nav reordered to **All Concepts · Design Space Viz · Compare · Cost landscape**; page JS fetches the 4 sources, joins via `matrix_data.joinConcepts`, and renders a placeholder (group bands + concept codes) with a live group-by control.

### Assumption Under Test
B2 — `matrix_data.js` rows/grouping/sort/filter reuse cleanly on a non-matrix surface, with no refetch on re-group (I3).

### Test Stencil (Write This First)
```
# browser-inspect (manual-driven), asserted via JSON sidecar / console
# 1. goto /cost-landscape → page renders, nav shows 4 links, "Cost landscape" active
# 2. group-by = Fuel → bands relabel; capture network → ZERO new requests (I3)
# 3. within a band, concept codes ascend by LCOE (cheapest first)
```

### Changes Required
**See `design.md#architecture` (data flow) and `#research-findings` (matrix reuse).**

- [x] `templates/cost_landscape.html.j2` (NEW) — extends `base.html.j2`; controls bar (`#cost-controls`) + excluded note + chart-mount `<div>` (`#cost-chart`); loads Theme-A scripts + `matrix_data.js` + the page script (Plotly already vendored in base head).
- [x] `static/js/cost_landscape_page.js` (NEW) — fetches manifest+registry+tree+cost-landscape ONCE; joins via `matrixData.joinConcepts` + attaches the cost record by `concept_id`; keeps only concepts present in the aggregate (= costed + finite LCOE); `matrixData.project()` for grouping; **own `byLcoeAsc` comparator** (makeComparator can't sort numeric LCOE); curated 6-option group-by dropdown; placeholder band render + honest excluded note.
- [x] `base.html.j2` — reordered links (All Concepts · Design Space Viz · Pipeline · Compare · Cost landscape), added Cost landscape, relabelled Taxonomy → "Design Space Viz". **Pipeline kept** (user decision (b), 2026-06-07).
- [x] `server.py` — render call in `_render_templates` (`active_nav="cost_landscape"`); `cost_landscape_page` `FileResponse` handler; registered `GET /cost-landscape`.

### Validation
**Automated:** [x] Full suite 331 passed (only pre-existing manual/adapter exclusions fail); nav active-state spot-check correct on all 5 pages.
**Manual (browser-inspect, session `cost-landscape-p3`):**
- [x] `/cost-landscape` renders (placeholder bands, cheapest-first); nav order + active state correct; other pages' nav intact.
- [x] Re-group through all 6 options → `/api/` request count stays **4** (zero refetch, I3); `firstBandAsc:true` every grouping; console clean (0 errors / 0 page_errors); grouping deterministic (25 tree bands initial == after regroup).

**What We Know Works After This Phase:** The data spine + grouping reuse are proven; only the cell render remains.

---

## Phase 4: Stacked-bar chart + axis (D5) + colors (D3)

### Goal
Replace the placeholder with Plotly 4-trace stacked bars (Capital/Fixed-O&M/Replacement/Fuel), colored from 4 new `:root` tokens, on a focused linear axis with annotated overflow for outliers.

### Assumption Under Test
A focused-range linear axis keeps the ~90% readable while honestly flagging outliers (D5); the stack visibly sums to LCOE.

### Test Stencil (Write This First)
```
# browser-inspect
# 1. each bar = 4 stacked segments; total height tracks LCOE
# 2. concept 03 (pathological) absent; "N excluded" note present (I5)
# 3. concept 16 (2068) drawn to cap with "↑ 2068" annotation (D5)
# 4. concept 17a/17b show Replacement + Fuel segments; 01 shows ~none
```

### Changes Required
**See `design.md#key-decisions` (D3 color, D5 axis), `#implementation-notes` (stack order).**

- [x] `explorer.css` — 4 `--cost-*` tokens **+ a 5th `--cost-om-combined`** in `:root` (see notes); `.cost-landscape__excluded`/`__chart` layout block.
- [x] `cost_landscape_page.js` — Plotly `barmode:"stack"`, one trace/component (color via local `tok()` → :root, no hex); **own `byLcoeAsc`** within-band x-order (not `makeComparator`); `customdata=concept_id`; decompose `$/MWh = casX/(cas90+cas70+cas80)×lcoe` (D2); focused linear y-range [0,400] with **draw-to-cap + "↑ true LCOE" annotation** (incl. 03 per decision (a)); vertical band-leaf labels + colored separators; honest cap/excluded note.

### Validation
**Automated:** [x] Full suite 331 passed (zero regressions); I2 hex-guard — no hex literals in `cost_landscape_page.js`.
**Manual (browser-inspect, sessions `cost-p4`/`cost-p4b`):**
- [x] Every bar's segments sum to its LCOE (I1 verified by eval: #01=155.17, #16=2068.2, #03=37452.46, #24=16.05 — all == headline). Stacks colored from tokens; console clean (no missing-token errors, I2). 6 over-cap bars drawn to cap with true-value annotations (↑496/904/2,068/1,297/37,452/793). Fuel segments visibly carry the p-B11/IFE fuel story (#04/#06/#08/#18/#23). Re-group (tree↔fuel) updates traces + band labels live.

**What We Know Works After This Phase:** The chart tells the LCOE-decomposition story honestly across the field.

---

## Phase 5: Hover, click-through, caveat markers, honest degradation

### Goal
Summary hover (D6); bar click → concept page (FR-F9); caveat marker on x-ticks; honest degradation for cas71/72-missing concepts (37/39) and not-recorded override fields.

### Assumption Under Test
The "why" is reachable (hover summary + deep-link, D6/B3) and missing data says so rather than vanishing (FR-F10/I5).

### Test Stencil (Write This First)
```
# browser-inspect
# 1. hover segment → component, $/MWh, %, "★N adjustments · <source>"
# 2. click bar → /concept/{id} for that concept
# 3. concept 37 (no 71/72 split) → single "O&M" segment + caveat, not a fake split
# 4. x-tick shows #code + ⚠ where caveat applies
```

### Changes Required
**See `design.md#key-decisions` (D6), `#implementation-notes` (rationale_short, cas71/72 absent, caveat tick).**

- [x] `cost_landscape_page.js` — enriched `hovertext[]` per segment (★N adjustments + per-override notes + "blocked (not applied)" + caveat reason + click cue); `plotly_click` → `window.location = /concept/{customdata}` (wired once); caveat glyph via `caveatMarker().glyph` on x-tick text where `cav.any`; combined-O&M segment + "not recorded"/"blocked" honest wording. cas71/72-missing combined-O&M segment already shipped in Phase 4 (forced by held re-extract).
- [x] `explorer.css` — no extra styling needed (Plotly tooltip + tick chrome suffice).

### Validation
**Automated:** [x] Full suite 331 passed (only pre-existing manual/adapter exclusions fail); A3 glyph-authority guard `test_caveat.py::test_marker_markup_authored_only_in_caveat_marker` passes (glyph sourced from `caveatMarker().glyph`, not a literal).
**Manual (browser-inspect, sessions `cost-p5`/`cost-p5-nav`/`cost-p5-final`):**
- [x] Hover shows segment $/MWh + % + override summary (#04 Capital: "★ 7 adjustments · C220101: … · …5 more — click for detail"; combined-O&M correctly surfaces the CAS70 override; "blocked (not applied)" honest). Click → emits navigate to `/concept/17a` (FR-F9). ⚠ on all 10 caveat ticks (FR-F5/F10). Console clean across load + regroup.

**What We Know Works After This Phase:** Feature-complete against spec FR-F1…F11 and acceptance criteria.

---

## Environment Setup

**See CLAUDE.md** — always `uv run python ...`; explorer server + `browser-inspect` skill for UI; never bare `python`/`pip`.

## Risk Management

**See `design.md#potential-risks`.**

**Phase-Specific Mitigations:**
- **P1**: re-extract may hit the FU2 jax-batch staleness — isolate per-concept; verify each headline vs module `result_1gw`. Coordinate timing with 1 GWe override-policy churn.
- **P3**: matrix-grouping reuse — if `buildControls` can't be shared cleanly, duplicate the small dropdown rather than risk B1 (matrix).
- **P4**: outlier axis — D5 focused-range + annotation; never log (breaks additive stacking).
- **P5**: Plotly tick labels are plain text — use an annotation layer for #code+⚠.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-06-07 (code + tests; re-extract held per user)

**Changes Made:**
- Added `exploration/concept_explorer/tests/test_cost_landscape_decomposition.py` (9 tests): served-data reconstruction of headline LCOE for 01/24/23 (B1/I1, runs on current JSON via combined cas70); `from_forward_result` builds cas71/cas72 and they reconstitute cas70 (I6); four-way share decomposition sums to LCOE; absent split → None (honest degradation, FR-F10).
- `models.py` `CostModelData`: added `cas71`/`cas72` as `CASAccount | None = None`; added `CAS_NAMES` entries "Fixed O&M (annualised)" / "Scheduled Replacement (annualised)"; `from_forward_result` builds each from `costs` when the key is present, else `None`; docstring example updated.

**Deviations from Plan (and why):**
- **cas71/cas72 are OPTIONAL, not required** (plan §"Changes Required" said `cas71: CASAccount`). Two independent reasons forced this, and they agree:
  1. *Held re-extract:* all 39 served `data/NN.json` carry only combined `cas70` today. Required fields would make every concept fail Pydantic load, breaking the server and suite — incompatible with holding the re-extract.
  2. *Correct long-term design:* the design itself (§Implementation Notes, "cas71/72 absent — 37, 39") says some concepts legitimately lack the split and must render combined O&M. So `None` = honest "no split recorded" is the right contract regardless of the re-extract — not a transitional fallback. This reconciles the plan's "add cas71: CASAccount" with the design's degradation requirement.
- **Test exercises the split through `from_forward_result` (synthetic), not served JSON.** The plan's stencil loaded served concepts and read `cm.cas71`; that can only pass on re-extracted data (plan's own "first proof point" names it "passing on re-extracted data"). To make Phase 1 land meaningfully *without* the re-extract, the served-data tests prove the B1/I1 reconstruction on the combined cas70 (non-tautological: the components rebuild the stored headline exactly via the energy formula, ratio 1.0000 for 01/24/23), and the split-specific wiring is proven via the constructor. No `skip`/`xfail` used.

**Held / Deferred (explicit):**
- The re-extract (FR-F11) and its served-JSON proof (cas71/cas72 present + sum to cas70 in `data/NN.json`) are **held at the user's instruction** pending the 1 GWe override-policy rerun. When that lands, re-run the extract and add a served-data split assertion to `test_cost_landscape_decomposition.py`.

**Verification:** new file 9 passed; full suite 309 passed with only the pre-existing manual/adapter exclusions failing (verified identical with my `models.py` change stashed → same 6 adapter failures, so zero regressions).

### Phase 2 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `models.py`: new cost-landscape section — `CostComponent` enum (segment vocabulary authority), `CostComponents` (capital/fixed_om/replacement/fuel + `om_combined`), `CompactOverride`, `CostLandscapeEntry`, `CostLandscape`; `build_cost_landscape(concepts)` (pure); `_override_component()` (account→segment roll-up, total + fail-loud); `_override_rationale_short()`/`_first_sentence()` (abbreviation-aware).
- `server.py`: import `CostLandscape`/`build_cost_landscape`; `cost_landscape: CostLandscape` on `_State`; built in `lifespan` from the stamped concepts (precomputed once, like the manifest); `api_cost_landscape` handler; registered `app.get("/api/cost-landscape")`.
- `tests/test_cost_landscape_api.py`: 22 tests (see checklist above).

**Decisions / Deviations (and why):**
- **`CAS70 → fixed_om`** (user-confirmed 2026-06-07). The design's I6 map only enumerated cas71/cas72, but real registry overrides are authored at the *combined* `CAS70` level (6 of them). They roll up to the O&M segment; the override's `account` string stays `"CAS70"` so nothing is misrepresented. An account outside the known vocabulary **raises** (no silent bucket) — keeps I6 totality honest.
- **`build_cost_landscape()` lives in `models.py`, not `server.py`** (design Component Overview said server.py). Chosen for consistency with the sibling pure builders `build_manifest`/`build_parameter_index` (both in models.py) and clean test imports (no server spin-up). The route handler stays in server.py. Same "one tested place" the design wanted.
- **Added `om_combined` (CAS70) to `CostComponents`** beyond the design's 4-key `{capital,fixed_om,replacement,fuel}`. Load-bearing for honest degradation: the 71/72 split is absent for *all* concepts pre-re-extract (and permanently for 37/39), so without the combined value the chart couldn't draw any O&M segment. `fixed_om`/`replacement` stay `None` when the split isn't recorded; `om_combined` is always present and equals their sum when it is.
- **`rationale_short` is abbreviation-aware.** Naive first-sentence splitting truncated a real rationale to "Sorbom et al." on concept 01; added a small abbreviation set so the boundary skips `et al.`/`e.g.`/etc. Falls back to structured `cost_basis · provenance` when no prose rationale, `None` when nothing is recorded (front-end renders "not recorded", FR-F10).

**Verification:** 22 new tests pass; full suite 331 passed (309 prior + 22), only the pre-existing manual/adapter exclusions failing — zero regressions. Endpoint manually exercised via TestClient (36 costed concepts, concept-01 shape confirmed).

### Phase 3 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `templates/cost_landscape.html.j2` (NEW); `static/js/cost_landscape_page.js` (NEW); `base.html.j2` nav reorder/rename/add; `server.py` render call + `cost_landscape_page` handler + `GET /cost-landscape` route.

**Decisions / Deviations (and why):**
- **Pipeline kept in the nav** (user decision (b)). FR-F2 listed exactly 4 items and omitted the existing Pipeline link; rather than silently drop a page's only nav entry, confirmed and kept it. Final order: All Concepts · Design Space Viz · Pipeline · Compare · Cost landscape (the spec's relative order of its four preserved, Pipeline in its slot).
- **Own `byLcoeAsc` comparator, not `makeComparator("lcoe")`.** The plan referenced `makeComparator(lcoe, asc)`, but matrixData's comparator only knows code/name/ontology-facet keys — `"lcoe"` would silently fall back to code order. The cost page sorts each band by the attached `cost.lcoe` (code tiebreak) after `project()` groups.
- **Membership = the aggregate, not a re-derived filter.** A row appears iff it's in `/api/cost-landscape` (costed + finite LCOE), which the aggregate already guarantees — so the page filters by aggregate membership and attaches the cost record, rather than re-implementing the has_cost_model/finite check (single source of "what's costed").
- **Curated 6 group options** (no-grouping + tree + fuel/driver/capture/opMode) reusing matrixData.GROUP_OPTIONS labels; "No grouping" → matrixData's single ungrouped band, relabelled "All costed concepts".
- **No CSS this phase.** Plan put the `:root` cost tokens + `.cost-landscape` block in Phase 4; the placeholder reuses `matrix-control*` classes and renders readably unstyled. Phase 4 brings the real styling.
- **Excluded note shows 0 today** — all 36 served concepts are costed (omit list drops non-costed). The note path activates in Phase 4 when D5 outlier exclusions begin.

**Verification:** browser-inspect session `cost-landscape-p3` — zero refetch across all 6 regroups (`/api/` count constant at 4), cheapest-first within every band, console clean, deterministic grouping. Full suite 331 passed (zero regressions); nav active states correct on all 5 pages.

### Phase 4 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `explorer.css`: 5 `--cost-*` :root tokens + `.cost-landscape__excluded`/`__chart` block.
- `cost_landscape_page.js`: replaced the placeholder DOM render with a Plotly stacked-bar chart — per-concept decomposition (D2), token-sourced colors (D3), focused linear axis with draw-to-cap + annotation (D5), band separators + vertical leaf labels, adaptive trace set.

**Decisions / Deviations (and why):**
- **Outlier policy (user-confirmed):** cap = **400 $/MWh**; over-cap bars (incl. 03=37,452) **drawn to the cap with a "↑ true LCOE" annotation** (decision (a)) — uniform, nothing hidden, no arbitrary exclusion threshold. So **nothing is hard-excluded** from the chart for magnitude; the "N excluded" note now covers only non-costed/non-finite (0 today) plus a separate honest "N exceed the cap" line. This **supersedes** the plan stencil's "03 absent / N excluded" wording.
- **5th token `--cost-om-combined`** beyond the design's 4. Load-bearing: pre-re-extract *every* concept lacks the 71/72 split, so the bar's O&M portion is the combined CAS70 — without a combined trace the stack wouldn't sum to LCOE (I1) for any concept today. The page shows an adaptive trace set: Capital + Fuel always; Fixed-O&M/Replacement only if some concept has the split; O&M-(combined) only if some concept lacks it. Today → Capital · O&M (combined) · Fuel; after re-extract → Capital · Fixed-O&M · Replacement · Fuel (+ combined only for 37/39). **This also pulls the Phase-5 "combined-O&M segment" degradation forward into Phase 4** — it's required now for I1 to hold on the held-re-extract data.
- **Own `byLcoeAsc`, not `makeComparator("lcoe")`** (carried from Phase 3 — makeComparator can't sort numeric LCOE).
- **No hex in JS (I2):** chart-chrome colors also read from :root tokens (`--color-surface-2`/`--color-border`/`--color-text-*`) via `tok()`, so the whole module is hex-free (stricter than view_capex, which hardcodes chrome hex).
- **Vertical band-leaf labels.** 25 tree bands across 36 concepts collide horizontally; vertical labels fit each narrow band, colored by family/value. Tree labels show the leaf only (last path segment).

**Verification:** browser-inspect (`cost-p4`, `cost-p4b`) — I1 holds for every bar (segment sums == headline LCOE), colors resolve from tokens, console clean, 6 over-cap annotations correct, tree + fuel groupings both readable and live. Full suite 331 passed; I2 hex-guard clean.

**Post-completion refinement (2026-06-07, user feedback "better differentiate the groups"):** the original thin dotted separators + vertical labels left it hard to (a) read dense tree labels and (b) tell which bars sit in which group. Replaced with **translucent colored background zones** per band (family color for tree, value color for dims, via `hexToRgba()` from the token hex — no authored hex, I2 intact) + a boundary separator + **staggered two-row labels**. Tree now reads as clear MFE/IFE/MIF/Non-Standard color zones; dimension groupings show one labeled zone per value. browser-inspect `cost-zones` (tree + driver) — zones render, console clean; suite still 331.

### Phase 5 Completion
**Completed:** 2026-06-07

**Changes Made:**
- `cost_landscape_page.js`: enriched per-segment hover (override summary + caveat reason + click cue), `plotly_click` → concept page (wired once, survives re-react), ⚠ on x-tick text via `caveatMarker().glyph`, honest "blocked (not applied)"/"not recorded" wording. Added `overrideSummary`/`coveredComponents`/`truncate` helpers.

**Decisions / Deviations (and why):**
- **Combined-O&M honest degradation shipped in Phase 4, not here** — forced by the held re-extract (the combined segment is load-bearing for I1 today). Phase 5 therefore covered hover + click + caveat ticks only.
- **Hover surfaces per-override notes (FR-F8), not just D6's count+source.** FR-F8 asks for "source/override notes"; the hover shows "★N adjustments" + up to 2 `account: rationale_short` lines + "…N more — click for detail", reconciling FR-F8 (notes visible) with D6 (summary + deep-link for full).
- **Combined-O&M segment aggregates the fixed_om+replacement override families.** Analyst O&M overrides are authored at CAS70 (→ `fixed_om`), but today's rendered O&M segment is `om_combined`; `coveredComponents()` maps the combined segment to both O&M families so those overrides surface on its hover.
- **Caveat glyph sourced from `caveatMarker().glyph`, never a literal** — required by the A3 single-authority grep-guard (`test_caveat.py`). Tripped it first with a literal ⚠ (incl. one in a code comment); fixed both. Did not add the page to the test's curated `_CAVEAT_SITES`/`_TEMPLATES` lists, matching the post-Theme-A precedent (matrix_page.js is also a caveatMarker consumer not in those lists).
- **Over-cap bars keep the "↑ true LCOE" annotation as their caveat** (from Phase 4); not double-marked with ⚠ (which is reserved for grounding caveats — asterisk/archetype-fit). The ↑ value is more specific than a generic glyph.

**Verification:** browser-inspect (`cost-p5`/`cost-p5-nav`/`cost-p5-final`) — hover summaries correct (incl. combined-O&M override surfacing and blocked wording), click navigates to `/concept/{id}`, 10 caveat ⚠ ticks, console clean. Full suite 331 passed; A3 glyph-authority guard green; I2 hex-guard green.

---

**Status**: Draft → In Progress → **Complete (2026-06-07)** — all 5 phases done; the served-JSON cas71/72 split proof remains held with the re-extract (per user).
