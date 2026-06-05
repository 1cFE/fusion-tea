# Implementation Plan: Explorer Adapter + Pilot Regeneration (Item 10)

**Status:** In Progress (Phases 1–2 complete)
**Created:** 2026-05-31
**Last Updated:** 2026-05-31

## Source Documents

- **Spec:** [`spec.md`](spec.md)
- **Design:** [`design.md`](design.md) ← component details, key bets, invariants, gotchas
- **Epic:** [`epic_concept_analysis_rework.md`](../../backlog/epic_concept_analysis_rework.md), Item 10

## Implementation Strategy

**Phasing Rationale.** Adapter code (P1) and view change (P2) are concept-independent; they validate against synthetic fixtures and can land before any pilot row is touched. P3 runs row 01 (ARC) alone — already validated under Item 8 — to localize bugs to the adapter when something fails. Only then does P4 fan out across the fit × grounding grid (14 / 08 / 26). P5 closes out with the report and fold-back dispatch.

**Critical Path.** P1 → P3 → P4 → P5. P2 can run parallel with P1.

**First Proof Point.** A Phase 1 unit-test fixture where `result_1gw` is removed from a `model_setup.py` whose frontmatter says `Comparison-Status: costingfe` → `ExtractionError` raised. Proves the strict-consumer contract (design Bet 1, Invariant 1) before any concept is regenerated.

**Overall Validation Approach.**
- Every phase starts with tests where applicable (P1, P2 stencils below).
- P3–P4 validation is execution-based: archive procedure runs clean, regen exits 0, critic exits 0, ingest exits 0.
- Fold-backs surfacing during P3/P4 dispatch back to Items 7/8/9 *during* the phase, not deferred to P5.

---

## Phase 1: Explorer Adapter + Unit Tests

### Goal

All code changes to the explorer's extraction pipeline land + unit tests for the new contract pass. No concepts regenerated.

### Assumption Under Test

The strict-consumer contract (Bet 1), routing cross-check (Bet 7), and `pending-design-point` skip (Bet 8) behave as specified against synthetic fixtures.

### Test Stencil (Write This First)

```python
# exploration/concept_explorer/tests/test_extract_adapter.py
def test_costingfe_missing_result_1gw_raises(tmp_path):
    # frontmatter: Comparison-Status: costingfe, P-Native: 233
    # model_setup.py: model, result defined; result_1gw missing
    write_concept_fixture(tmp_path, status="costingfe", p_native=233, include_result_1gw=False)
    with pytest.raises(ExtractionError, match="result_1gw missing"):
        run_extraction(tmp_path.parent, data_dir, concept_filter=["99"])

def test_verify_two_knob_mismatch_raises(tmp_path):
    write_concept_fixture(tmp_path, status="costingfe", p_native=233, n_mod_override=5.0)  # wrong
    with pytest.raises(ExtractionError, match="n_mod"):
        run_extraction(...)

def test_routing_crosscheck_disagreement_raises(tmp_path):
    # Comparison-Status: costingfe but model_setup.py is non-costingfe-shaped
    write_concept_fixture(tmp_path, status="costingfe", model_setup_kind="standalone")
    with pytest.raises(ExtractionError, match="routing"):
        run_extraction(...)

def test_pending_design_point_skipped(tmp_path, capsys):
    write_concept_fixture(tmp_path, status="pending-design-point")
    run_extraction(...)
    assert not (data_dir / "99.json").exists()
    assert "99" in capsys.readouterr().out  # skip message
```

### Changes Required

**See `design.md` for:**
- Strict-consumer contract → [`design.md#bet-1`](design.md#bet-1-strict-consumer-no-fallback-over-compatibility-tolerant)
- Routing cross-check truth table → [`design.md#bet-7`](design.md#bet-7-routing-cross-check-not-routing-replacement)
- `pending-design-point` semantics → [`design.md#bet-8`](design.md#bet-8-pending-design-point-is-skip-with-message-not-ingest)
- `_to_confinement_family` helper + error shapes → [`design.md#implementation-notes`](design.md#implementation-notes)
- Invariants 1–5 → [`design.md#required-invariants`](design.md#required-invariants)

**Specific file changes:**

#### 1. Test file
**File:** `exploration/concept_explorer/tests/test_extract_adapter.py` (NEW)
- [x] Implement test stencil above
- [x] Add fixture helper `write_concept_fixture` (frontmatter + `model_setup.py` + optional `result_1gw`)
- [x] Add fixtures for: `Confinement-Family: MFE` → enum maps; missing → NONSTANDARD fallback; `costingfe-asterisked` → `asterisk_in_comparison: True`; `freeform-deferred` → standalone path, no asterisk

#### 2. Explorer adapter
**File:** `exploration/concept_explorer/extract_explorer_data.py`
- [x] Remove `parse_confinement_family` (L89–102)
- [x] Add `_to_confinement_family(raw) -> ConfinementFamily` helper per [`design.md#implementation-notes`](design.md#implementation-notes)
- [x] Add `verify_two_knob(result_1gw, p_native, *, tolerance_rel=1e-9)` helper
- [x] At L835 (post `is_costingfe` heuristic): add Bet 7 cross-check; raise `ExtractionError` on the three disagreement cases
- [x] At dispatch (L841): branch on `Comparison-Status` — `pending-design-point` → skip + log; `freeform-deferred` → `extract_standalone`; `costingfe` / `costingfe-asterisked` → `extract_costingfe`
- [x] `extract_costingfe`: remove L260–262 fallback; require `result_1gw`; call `verify_two_knob`; pass `asterisk_in_comparison = (status == "costingfe-asterisked")` to `ConceptData`
- [x] `extract_standalone` (L287, L579): replace `parse_confinement_family` calls with `_to_confinement_family(frontmatter.get("Confinement-Family"))`
- [x] End-of-run skip summary: print skipped concept IDs and reason

#### 3. Models
**File:** `exploration/concept_explorer/models.py`
- [x] Add `asterisk_in_comparison: bool = False` to `ConceptData`

### Validation

**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_extract_adapter.py` → all pass (13/13)
- [x] `uv run python -m pytest exploration/concept_explorer/tests/` → no regressions (74/74 explorer tests pass; existing fixtures updated for Item 6 frontmatter + result_1gw)
- [x] `uv run python -m pytest exploration/concept_analysis/scripts/` → no regressions (4 pre-existing `test_concepts_v2.py` `StopIteration` failures on `pending` records are unrelated to Item 10; verified by running against the pre-change tree)

**Manual:**
- [x] `grep -n "parse_confinement_family\|result_1gw is not None else result" exploration/concept_explorer/extract_explorer_data.py` → no matches (FR-1, FR-3)
- [x] End-of-run skip summary verified by `TestPendingDesignPoint::test_end_of_run_skip_summary_present` (asserts `"Skipped 1 concept"` in stdout)

**What We Know Works After This Phase:**
- Strict-consumer contract holds against synthetic fixtures (Invariants 1, 3).
- Routing cross-check raises on disagreement (Invariant 2).
- Asterisk flag flows from frontmatter to `ConceptData` (Invariant 4).
- `pending-design-point` skip path works (Invariant 5).

---

## Phase 2: Comparison-View Asterisk Render

### Goal

The comparison view renders an asterisk badge next to concepts where `asterisk_in_comparison: true`, with a tooltip explaining the low-grounding case.

### Assumption Under Test

The visual idiom is the right size — a small marker plus a tooltip — without colliding with existing badges (Risk row 3 in design).

### Test Stencil (Write This First)

```javascript
// exploration/concept_explorer/tests/test_comparison_asterisk.spec.js  (or equivalent)
test("asterisk badge renders when asterisk_in_comparison is true", () => {
  const concept = {concept_id: "26", name: "Inertia", asterisk_in_comparison: true};
  render(<ComparisonRow concept={concept} />);
  expect(screen.getByTitle(/grounding is low/i)).toBeInTheDocument();
});

test("no asterisk when asterisk_in_comparison is false", () => {
  const concept = {concept_id: "01", name: "ARC", asterisk_in_comparison: false};
  render(<ComparisonRow concept={concept} />);
  expect(screen.queryByTitle(/grounding is low/i)).toBeNull();
});
```

If the explorer's test setup doesn't have a JS test harness today, fall back to a runtime check: ingest the `02-test` fixture from Phase 1, open the comparison view in `browser-inspect`, screenshot, eyeball.

### Changes Required

**See `design.md` for:**
- Asterisk surface scope → [`design.md#bet-2`](design.md#bet-2-asterisk-is-render-time-driven-by-comparison-status-costingfe-asterisked-only--and-that-status-means-low-grounding-nothing-else)
- Tooltip text → [`design.md#bet-2`](design.md#bet-2-asterisk-is-render-time-driven-by-comparison-status-costingfe-asterisked-only--and-that-status-means-low-grounding-nothing-else)

**Specific file changes:**

- [x] ~~`exploration/concept_explorer/templates/compare.html.j2`~~ — N/A: compare.html.j2 is a JS-driven skeleton; per-concept rows are built dynamically from JSON. Render lives entirely in comparison.js.
- [x] `exploration/concept_explorer/static/js/comparison.js` — `asteriskBadge(concept)` helper renders `<span class="comparison-asterisk" title="…">*</span>` when `concept.asterisk_in_comparison` is true; called from the concept-bar chip and landscape-cell header (the picker reads from manifest, which doesn't currently carry the field — out of scope, noted in code)
- [x] `exploration/concept_explorer/static/css/explorer.css` — `.comparison-asterisk` style (small grey marker; non-clickable; `cursor: help` for the tooltip)

### Validation

**Automated:**
- [x] ~~JS test from stencil~~ — N/A: no JS test harness present in `concept_explorer/`. Structural verification done via curl: API returns `asterisk_in_comparison: true` for synthesized 99 and `false` for 01; comparison.js + explorer.css are served with the new helper and class.

**Manual:**
- [x] Synthesized `data/99.json` (copy of 01 with `asterisk_in_comparison: true`)
- [x] Started explorer on :8430; operator opened `/compare?mode=landscape&concepts=01,99`
- [x] Operator confirmed: asterisk marker renders next to concept 99 name; tooltip ("Asterisked: design-point grounding is low …") appears on hover; concept 01 shows no asterisk
- [x] Cleanup: 99.json removed, server killed

**What We Know Works After This Phase:**
- Render-side asterisk path works independent of any pilot concept being regenerated.

---

## Phase 3: Pilot Row 01 (ARC) — Adapter Smoke Test

### Goal

Run the full archive → regen → critic → restore → ingest procedure for concept 01 (already known-good under Item 8). Confirm the adapter does not fail on a known-conforming row.

### Assumption Under Test

The explorer adapter (P1) and the upstream pipeline (Items 4 / 6 / 7 / 8 / 9) compose cleanly against a real concept. If P3 fails, the bug is localized: either the adapter, or P3-specific procedure issues — not the new pipeline (Item 8 already validated ARC).

### Procedure (no test stencil — execution-only)

Per [`design.md#bet-4`](design.md#bet-4-archive-the-pre-regen-concept-dir-restore-reviewmd-from-it):

1. **Archive:** `git mv exploration/concept_analysis/analyses/01-hts-compact-tokamak archive/concept-rework-explorer-pilot/01-hts-compact-tokamak-pre-regen/`
2. **Log:** append a line to `archive/concept-rework-explorer-pilot/README.md`: date, commit, concept ID, "pre-regen archive for Item 10 pilot"
3. **Commit** the archive move
4. **Re-create** the concept dir from upstream tables — orchestrator's `init-concept` / equivalent path, regen runs from clean state
5. **Regenerate** via `uv run python -m exploration.concept_analysis.scripts.run_analysis regenerate-concept 01-hts-compact-tokamak`
6. **Critic:** run `model_critic` against the regenerated artifacts → review document next to artifacts
7. **Restore `review.md`** from archive if and only if the archived version had operator-filled Decision fields (eyeball check); commit
8. **Ingest:** `uv run python exploration/concept_explorer/extract_explorer_data.py --concept 01`

### Changes Required

- [ ] `archive/concept-rework-explorer-pilot/README.md` (NEW, may not exist yet)
- [ ] Two git commits: archive move + (if needed) review.md restore

### Validation

**Automated:**
- [ ] regen exits 0
- [ ] `model_critic` exits 0
- [ ] explorer ingest exits 0; `data/01.json` written; no `ExtractionError`
- [ ] `data/01.json` shows `asterisk_in_comparison: false` (ARC is high-grounding)

**Manual:**
- [ ] Inspect regenerated `analysis.md` frontmatter: `Confinement-Family`, `Comparison-Status: costingfe`, `P-Native: 233`, `Grounding-Confidence: high`
- [ ] Inspect regenerated `model_setup.py`: four-step helper-form shape per Item 7. If the analyst used relative overrides, the file imports `generic_reference` alongside `run_native_and_1gw` and calls it before the overrides list — explorer is indifferent either way (it reads `result_1gw` only); flag in `pilot_report.md` if the form is unfamiliar so Item 11 picks it up
- [ ] Inspect `result_1gw.params`: `net_electric_mw == 1000`, `n_mod ≈ 4.292`
- [ ] Render comparison view containing concept 01 + a stubbed asterisked row → both render correctly side-by-side

**What We Know Works After This Phase:**
- Adapter + upstream pipeline compose on a known-good concept.
- Archive / restore procedure is sound at single-row scale.

---

## Phase 4: Pilot Rows 14, 08, 26 — Grid Coverage

### Goal

Exercise the fit × grounding grid: Med-fit (14 GF MTF), Low-fit (08 Helion Orion), High-fit / low-grounding with `n_mod < 1` (26 Inertia). Surface fold-backs as they appear and dispatch them during the phase.

### Assumption Under Test

The whole new pipeline holds across concept variety — including DHE3 fuel (08), the MAG_TARGET catch-all enum (14), and the asterisk-path + super-1GWe inverted framing (26). If any row fails, the failure mode is real and the fold-back item is identified.

### Procedure (per row)

Same as P3, executed in order: **14 → 08 → 26**. Between rows, if a fold-back is required:
- Item 7 fold-back (helper/validator) → land in `concept-rework-helpers-validators`, retry the row.
- Item 8 fold-back (prompt) → land in `concept-rework-prompt-templates`, retry the row.
- Item 9 fold-back (critic) → land in `concept-rework-model-critic`, retry the critic pass.

Order rationale: 14 first (Med-fit, "least exotic" of the three) → 08 (DHE3 + Low fit) → 26 (asterisk + `n_mod < 1`, the hairiest mechanical case). If 14 fails on something fundamental, the same failure likely hits 08/26 too and we save running cost.

### Changes Required

- [ ] Three more entries in `archive/concept-rework-explorer-pilot/README.md`
- [ ] Up to six commits (archive + restore per row)
- [ ] Fold-back PRs in Items 7 / 8 / 9 as needed (separate work-item dirs)

### Validation (per row)

**Automated:**
- [ ] regen + critic + ingest all exit 0
- [ ] `verify_two_knob` passes for each row's `result_1gw`
- [ ] Row 26 ingest: `data/26.json` shows `asterisk_in_comparison: true`

**Manual:**
- [ ] Frontmatter sanity-check per row (Confinement-Family, P-Native, Grounding-Confidence)
- [ ] `result_1gw.params["n_mod"]` matches design's expected value (14: 6.667, 08: 20, 26: 0.667)
- [ ] Comparison view with all four pilot rows side-by-side — row 26 asterisked, others not
- [ ] LCOE spread across the four rows passes eyeball sanity check (none wildly outside NOAK plausibility; if 26 inverts the framing as expected, note in P5)

**What We Know Works After This Phase:**
- The pipeline holds across fit × grounding variety.
- `n_mod < 1` regime is mechanically sound (or its fold-back is identified).
- Asterisk path is end-to-end validated (Bet 2 / Invariant 4).

---

## Phase 5: Pilot Report + Fold-Back Dispatch Close-Out

### Goal

Write `pilot_report.md` per [`design.md#component-overview`](design.md#component-overview) (issue-list-first shape, per Invariant 8 + FR-9). Confirm every fold-back surfaced in P3/P4 either landed back into its owning item or is explicitly recorded as deferred / accepted residual.

### Procedure

- [ ] Write `pilot_report.md` with structure per [`pilot_report.md`](../concept-rework-prompt-templates/pilot_report.md) precedent (executive summary → per-concept observations → cross-cutting findings → fold-back table → weak-signal note if applicable)
- [ ] Cross-link to fold-back PRs / commits in Items 7 / 8 / 9
- [ ] Update epic Item 10's success-criteria checkboxes
- [ ] If pilot surfaced zero issues, flag the "weak signal" note in the executive summary per Invariant 8
- [ ] Record disposition of row 26's inverted-framing observation (asterisk meaning under `n_mod < 1`) — note for Item 11

### Validation

**Manual:**
- [ ] Report cross-references each pilot row, each fold-back, each disposition
- [ ] Epic Item 10 checkboxes match plan-side completion state
- [ ] No fold-back is left "open without disposition" — every one is `landed before bulk` / `deferred to Item 11` / `accepted residual`

**What We Know Works After This Phase:**
- Item 10 is complete; Item 11 is unblocked.

---

## Environment Setup

**See [`CLAUDE.md`](../../../CLAUDE.md) for full environment rules.** Key reminders: `uv run python …` (never bare `python`); explorer ingest is `uv run python exploration/concept_explorer/extract_explorer_data.py`; browser inspection uses `scripts/browser_inspect.py` (see `browser-inspect` skill).

---

## Risk Management

**See [`design.md#potential-risks`](design.md#potential-risks) for the full table.**

**Phase-Specific Mitigations:**
- **P1** — synthetic fixtures are the cheapest place to discover contract bugs; if a test passes against an unrealistic fixture but fails on a real concept in P3, the fixture is wrong, fix it then.
- **P3** — known-good concept means a P3 failure localizes to the adapter; debug there, not in the pipeline.
- **P4 row 14 first** — Med-fit smoke test before the more exotic Low-fit rows; common-mode failures caught cheaper.
- **P4 row 26 last** — the `n_mod < 1` mechanical edge is the most likely place for a real new finding; running it last means the other rows have already absorbed any P1/P2 regressions.

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION — Leave empty now]

### Phase 1 Completion

**Completed:** 2026-05-31

**Changes Made:**
- `exploration/concept_explorer/models.py`: added `asterisk_in_comparison: bool = False` to `ConceptData`.
- `exploration/concept_explorer/extract_explorer_data.py`:
  - Removed `parse_confinement_family` (body-prose regex) and replaced with `_to_confinement_family(raw) -> ConfinementFamily` (frontmatter-driven, case/whitespace-tolerant, unknown → NONSTANDARD).
  - Added `verify_two_knob(result_1gw, p_native, concept_id, *, tolerance_rel=1e-9)` raising `ExtractionError` on `net_electric_mw != 1000`, `n_mod != 1000/P_native`, or non-positive `P_native`.
  - `run_extraction` now reads `Comparison-Status` from frontmatter and: (a) skips `pending-design-point` with a per-row message + end-of-run summary, (b) cross-checks `costingfe`/`costingfe-asterisked` and `freeform-deferred` against the import-source heuristic and raises on disagreement.
  - `extract_costingfe`: unconditional `result_1gw` requirement (legacy `result_1gw is not None else result` fallback removed); `verify_two_knob` called when `P-Native` is present; `asterisk_in_comparison` populated from `comparison_status == "costingfe-asterisked"`.
  - Both `extract_costingfe` and `extract_standalone` now read `Confinement-Family` via `_to_confinement_family(frontmatter.get("Confinement-Family"))`.
- `exploration/concept_explorer/tests/test_extraction.py`: updated `_make_concept_dir` to emit `Confinement-Family` frontmatter (replaces body-prose marker), updated all 9 `SimpleNamespace(model=..., result=...)` mock-modules to include `result_1gw=result`, replaced `TestParseConfinementFamily` with `TestToConfinementFamily`.
- `exploration/concept_explorer/tests/test_extract_adapter.py` (new, 13 tests): strict-consumer contract, two-knob verify, routing cross-check, pending-design-point skip, asterisk flag — all green.

**Issues Encountered:**
- None. The plan's "specific file changes" matched the codebase 1:1 except for the legacy `result_1gw → result` fallback, which I removed unconditionally (rather than gating it on `comparison_status` being set). See Deviations.

**Deviations from Plan:**
- **Strict `result_1gw` requirement is unconditional** in `extract_costingfe`, not gated on `comparison_status ∈ {costingfe, costingfe-asterisked}`. Plan's manual grep validation (`result_1gw is not None else result` → no matches) requires the fallback to be gone entirely. Design Bet 6 (dropped) anticipates un-migrated concepts will fail naturally until Item 11; this matches that posture. `verify_two_knob` is still gated on `P-Native` being present, so un-migrated costingfe concepts that happen to expose `result_1gw` but have no `P-Native` frontmatter still ingest. Net effect: stricter than spec FR-3 ("MUST raise when routing is costingfe and no result_1gw"), aligned with plan's grep check.

### Phase 2 Completion

**Completed:** 2026-05-31

**Scope expansion mid-phase.** The plan's Phase 2 wired the asterisk only into the `/compare` view. During eyeball verification the operator pushed back: a small grey `*` on one page is weak signal. Phase 2 ended up covering five surfaces with a larger amber warning glyph (⚠) sharing one `.low-grounding-marker` class.

**Changes Made:**
- `exploration/concept_explorer/models.py`: added `asterisk_in_comparison: bool = False` to `ConceptManifestEntry`; `build_manifest` populates it from `ConceptData`. This propagates the field to every consumer of `/api/manifest`.
- `exploration/concept_explorer/static/css/explorer.css`: `.low-grounding-marker` rule (amber `#d97706`, `font-size-md`, bold, `cursor: help`, `user-select: none`).
- `exploration/concept_explorer/static/js/comparison.js`: `lowGroundingMarker(concept)` helper emits `<span class="low-grounding-marker">⚠</span>` with tooltip. Wired into concept-bar chip + landscape-cell header.
- `exploration/concept_explorer/static/js/index_page.js`: marker added to the All Concepts card meta row (between family badge and company).
- `exploration/concept_explorer/static/js/concept_page.js`: marker appended to the hero name on `/concept/{id}`.
- `exploration/concept_explorer/static/js/taxonomy.js`: cross-references manifest into the registry by concept_id so downstream views read `asterisk_in_comparison` without a second fetch.
- `exploration/concept_explorer/static/js/taxonomy_card.js`: marker appended to the taxonomy card name (right-side panel on `/taxonomy`).
- `exploration/concept_explorer/static/js/neighborhood_graph.js`: marker appended inline with concept name in the three graph tooltip variants (center / neighbor / bridge).

**Final surface set:**
- All Concepts cards (`/`)
- Compare chips + landscape-cell headers (`/compare`)
- Taxonomy card panel (`/taxonomy`)
- Concept hero (`/concept/{id}`)
- Neighborhood graph tooltip on hover (`/taxonomy` → focused concept)

**Surfaces explicitly NOT marked (user-confirmed during verification):**
- Constellation scatter dots — operator rejected an amber ring around the dot. No marker.
- Cytoscape graph node visual (border) — operator rejected an amber border on the node. Tooltip-only.
- Concept picker dropdown on `/compare` — manifest now carries the field, but operator did not ask for the picker to show it; left as-is.

**Issues Encountered:**
- Playwright not installed in this venv → drove the eyeball verification by synthesizing a `data/99.json` (copy of 01 with the flag flipped) and temporarily toggling `asterisk_in_comparison: true` on `data/26.json` so the marker would appear in surfaces driven by the taxonomy registry (which doesn't include synthetic IDs).
- The amber marker uses `⚠` (U+26A0). Inline placement next to the concept name in flex-row meta layouts works without collision; on the cytoscape node the user did not want any indicator (border was rejected — tooltip-only is the call).

**Deviations from Plan:**
- **Scope expanded beyond `/compare`.** Plan's Phase 2 was compare-only; after operator review the marker now shows on five surfaces. See "Final surface set" above.
- **Visual idiom changed.** Plan / design specified a small grey `*` asterisk (`comparison-asterisk` class). The shipped treatment is an amber `⚠` (`low-grounding-marker` class) — better signal-to-noise. Tooltip text and semantic meaning unchanged.
- **No `compare.html.j2` edit.** The Jinja template is a JS-driven skeleton.
- **No JS unit test.** The explorer has no JS test harness; eyeball verification across the five surfaces is the gate.

### Phase 3 Completion

### Phase 4 Completion

### Phase 5 Completion

---

**Status**: Draft → In Progress → Complete
