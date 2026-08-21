# Implementation Plan: Normalize Concept-Directory Resolution (Stop Storing Paths)

**Status:** Complete
**Created:** 2026-06-15
**Last Updated:** 2026-06-15

## Source Documents
- **Spec:** `.project/active/explorer-model-setup-path-normalization/spec.md`
- **Design:** `.project/active/explorer-model-setup-path-normalization/design.md` ← component details, decisions (D1–D4), invariants (INV-1–4), bets (B1–B3), gotchas

## Implementation Strategy

**Phasing Rationale:**
De-risk the one load-bearing assumption (B2/INV-2: `model_type` ⟺ resolvable `model_setup.py`) before touching any code, because a violation there is a *data* fix that must precede deleting the schema field. Then make the core code change (resolver + server rewiring + delete `SourcePaths`) test-first. Then propagate the "no paths" rule outward — extractor (so future regens stay clean), then the 40 committed files. Verify end-to-end last.

**Critical Path:**
Audit passes → server derives + `SourcePaths` deleted (suite green) → extractor stops emitting → data migrated → live e2e returns the parity LCOE.

**First Proof Point:**
Phase 1's audit passing across all real concept files — confirms the design's central equivalence holds in the actual data.

**Overall Validation Approach:**
- Each phase starts with a test.
- `uv run python -m pytest exploration/concept_explorer/tests/ -q` is the regression gate after each code phase.
- No flag-day: pydantic ignores leftover keys (`design.md` Research Findings), so Phases 2–4 are order-independent for correctness; landed together for a coherent diff.

---

## Phase 1: Audit the `model_type` ↔ `model_setup.py` Equivalence (De-Risk)

### Goal
Prove INV-2 across all real concept data before deleting anything: every `model_type == COSTINGFE` concept has a resolvable `{id}-*/model_setup.py`, and every `STANDALONE` concept does not require one. Land it as a permanent test so future drift is caught.

### Assumption Under Test
B2 / INV-2 — `model_type == COSTINGFE` is exactly "has a runnable `model_setup.py`". If false, the gate (D3) and resolution mis-fire for some concept.

### Test Stencil (Write This First)
```python
# tests/test_model_setup_resolution.py (NEW)
def test_costingfe_concepts_resolve_to_a_model_setup():
    analyses_root = REPO_ROOT / "exploration/concept_analysis/analyses"
    for path in sorted(DATA_DIR.glob("[0-9]*.json")):
        concept = ConceptData.model_validate_json(path.read_text())
        d = find_concept_dir(concept.concept_id, analyses_root)  # Phase 2 promotes this
        if concept.model_type == ModelType.COSTINGFE:
            assert d is not None and (d / "model_setup.py").exists(), concept.concept_id
        # STANDALONE concepts: no model_setup.py requirement asserted
```

### Changes Required
**See `design.md`:** "Required Invariants" (INV-2), "Key Bets" (B2), "Potential Risks".

- [x] Create `exploration/concept_explorer/tests/test_model_setup_resolution.py` with the equivalence assertion across all `data/[0-9]*.json`.
- [x] If Phase 2's `find_concept_dir` doesn't exist yet, inline the prefix-scan in the test temporarily, then switch to the import in Phase 2.

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_model_setup_resolution.py -q` → passes for all concepts.

**Manual:**
- [x] If any concept fails: stop, treat as a data discrepancy, reconcile `model_type` vs. the actual `analyses/` tree before proceeding. → No failures; all COSTINGFE concepts resolved.

**What We Know Works After This Phase:**
The design's central equivalence holds in real data — safe to delete the path field.

---

## Phase 2: Server Resolution + Delete `SourcePaths` (Core Change)

### Goal
Compute resolves `model_setup.py` from `concept_id`; the 422 gate reads `model_type`; `SourcePaths`/`sources` is deleted. All tests updated and green.

### Assumption Under Test
B1 — a concept's directory is fully determined by `concept_id` via the shared `analyses_root` + prefix scan, in the test harness and at runtime.

### Test Stencil (Write This First)
```python
# test_state_and_compute.py — fixture mirrors the REAL layout so derivation works
def costingfe_base_dir(tmp_path):
    base = tmp_path / "exploration" / "concept_explorer"
    (base / "data").mkdir(parents=True)
    setup = tmp_path / "exploration/concept_analysis/analyses/04-fake/model_setup.py"
    setup.parent.mkdir(parents=True); setup.write_text(_FAKE_MODULE_PY)
    # ConceptData(..., model_type=ModelType.COSTINGFE)  # no path field
    return base

def test_compute_is_host_independent(client):  # NEW
    assert client.post("/api/compute", json={"concept_id": "04", "overrides": {}}).status_code == 200
def test_compute_freeform_returns_422(client):
    assert client.post("/api/compute", json={"concept_id": "01", "overrides": {}}).status_code == 422
```

### Changes Required
**See `design.md`:** "Architecture" (data flow), "Component Overview", "Key Decisions" (D1–D3), "Implementation Notes" (fixture restructuring, no-fallback rule, lru_cache stability).

**Production code:**
- [ ] `findings.py:83` — rename `_find_concept_dir` → public `find_concept_dir`; update its internal call sites (`build_findings`).
- [ ] `server.py` — add `analyses_root_for(base_dir)` (single home for the `base_dir.parent/concept_analysis/analyses` literal); use it at the findings endpoint (`:756`).
- [ ] `server.py:1042` — compute 422 gate → `concept.model_type != ModelType.COSTINGFE`.
- [ ] `server.py:990–994` — replace `Path(concept.sources.model_setup)` with `find_concept_dir(concept_id, analyses_root_for(state.base_dir))`; raise explicit **500** when dir is `None` or `model_setup.py` missing (no fallback, message names concept_id + resolved root — D3, FR-5).
- [ ] `models.py:400,492` — delete `SourcePaths` class and the `sources` field on `ConceptData`.

**Tests (drop `SourcePaths`; set `model_type` where capability matters):**
- [ ] `test_state_and_compute.py:133–173` — fixture mirrors real layout (stencil above); add `test_compute_is_host_independent`.
- [ ] `test_slider_override_semantics.py:254,269` — same fixture-layout fix.
- [ ] `test_models.py:30,116,378` · `test_server.py:35,53,103` · `test_taxonomy_server.py:27,61` · `test_extraction.py:51,1423,1572` — remove `SourcePaths` import/usage; where a costingfe concept is implied, set `model_type=ModelType.COSTINGFE`.
- [ ] `test_model_setup_resolution.py` — switch to importing the now-public `find_concept_dir`.

### Validation
**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/ -q` → all pass (no `SourcePaths` import errors anywhere).

**Manual:**
- [ ] Start server, `POST /api/compute {concept_id:"01", overrides:{}}` → 200 (against un-migrated data — proves derivation ignores the stale `sources` block).
- [ ] `POST /api/compute` for a freeform concept (02/03/16/27/35) → 422.

**What We Know Works After This Phase:**
Compute works by derivation on the dev box even before data migration; the schema no longer has a path field; findings unaffected.

---

## Phase 3: Extractor Stops Emitting Paths

### Goal
Future regenerations never bake a path again (FR-4).

### Assumption Under Test
Removing the `sources=SourcePaths(...)` argument from both `ConceptData` constructions leaves the extractor otherwise correct (the value was write-only).

### Test Stencil (Write This First)
```python
# test_extract_adapter.py (extend existing) — fresh extraction carries no path
data = json.loads(extracted_concept.model_dump_json())
assert "sources" not in data
assert "model_setup.py" not in extracted_concept.model_dump_json()
```

### Changes Required
**See `design.md`:** "Component Overview" (extractor), "Key Decisions" (D4 — parity is structural).
- [ ] `extract_explorer_data.py:489` and `:805` — remove the `sources=SourcePaths(...)` argument; remove the now-unused `SourcePaths` import.

### Validation
**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/test_extract_adapter.py -q` → passes.

**Manual:**
- [ ] Re-extract one costingfe concept (per the extractor's normal invocation) → emitted JSON has no `sources` key and no path string.

**What We Know Works After This Phase:**
The source of new data emits the new schema; migration (Phase 4) and fresh extraction now produce structurally identical output (FR-6).

---

## Phase 4: Migrate the 40 Committed Data Files

### Goal
Remove the `sources` block from every `data/*.json` (FR-1, FR-6).

### Assumption Under Test
All machine-path strings are confined to the `sources` block (verified in design — 2 per file, both in `sources`), so stripping that key fully satisfies FR-1.

### Test Stencil (Write This First)
```bash
# Post-migration assertion (also the acceptance grep)
grep -rl 'C:\\Users\\mallo' exploration/concept_explorer/data/*.json   # → empty
grep -rlE '/home/|C:\\|model_setup\.py|analysis\.md' exploration/concept_explorer/data/*.json  # → empty
```

### Changes Required
**See `design.md`:** "Component Overview" (migration script), "Key Decisions" (D4).
- [ ] Add a one-shot migration script (work-item dir or `scripts/`) that loads each `data/*.json`, removes the top-level `sources` key, and writes back with the file's existing indent/encoding (minimal diff).
- [ ] Run it; commit the 40 updated files.

### Validation
**Automated:**
- [ ] Both greps above return empty (INV-1).
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/ -q` → still green (server loads migrated data fine).

**Manual:**
- [ ] `git diff --stat` shows only `sources` blocks removed, nothing else changed.

**What We Know Works After This Phase:**
No machine-specific strings remain in committed data; loaded data and fresh-extracted data match.

---

## Phase 5: End-to-End Verification

### Goal
Confirm the acceptance criteria on a live server and prove host independence (INV-3, INV-4).

### Assumption Under Test
B3 — the `analyses/` tree resolves correctly regardless of where the repo/data sits on disk.

### Test Stencil (Write This First)
```bash
# Live server, real data
curl -s -X POST localhost:8421/api/compute -H 'Content-Type: application/json' \
  -d '{"concept_id":"01","overrides":{}}' | jq '.headline.lcoe_per_mwh'   # ≈ 161.69
```

### Changes Required
- [ ] No code changes; verification only.

### Validation
**Automated:**
- [ ] Full suite green: `uv run python -m pytest exploration/concept_explorer/tests/ -q`.

**Manual:**
- [ ] Start server (`uv run python exploration/concept_explorer/server.py` or uvicorn per CLAUDE.md); `POST /api/compute {concept_id:"01"}` → 200, `headline.lcoe_per_mwh ≈ 161.69` (INV-3).
- [ ] Freeform concept → 422.
- [ ] Copy `data/` (and run from) a path matching no contributor's machine → compute still 200 (INV-4).

**What We Know Works After This Phase:**
Slider recompute works on any host with the parity LCOE — acceptance criteria met.

---

## Environment Setup

**See CLAUDE.md** — uv-only (`uv run python …`), never bare `python`. Server: `uv run python exploration/concept_explorer/server.py` (port 8421) or `uv run python -m uvicorn exploration.concept_explorer.server:app --port 8421`. Browser/UI checks via the `browser-inspect` skill if needed.

---

## Risk Management

**See `design.md#potential-risks` for detailed analysis.**

**Phase-Specific Mitigations:**
- **Phase 1**: The audit *is* the mitigation for the biggest risk (B2 desync) — it runs before any deletion and becomes a permanent regression test.
- **Phase 2**: Compute-fixture rewrite is where incidental breakage hides; the full suite is the gate, and the un-migrated-data manual check proves derivation independent of the stale field.
- **Phase 4**: `git diff --stat` guards against the migration touching anything beyond `sources`.
- **Phase 5**: Host-independence check (relocated data) directly exercises B3/INV-4 — the failure mode that the absolute paths hid for so long.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-06-15
**Changes Made:**
- Created `exploration/concept_explorer/tests/test_model_setup_resolution.py` — asserts `model_type == COSTINGFE` ⟺ resolvable `{id}-*/model_setup.py` across the server-loaded concept set (digit-stem files, omit-list applied). Inlines the prefix-scan for now; switches to `findings.find_concept_dir` in Phase 2.

**Result:** `1 passed`. All COSTINGFE concepts resolve to a real `model_setup.py` under `exploration/concept_analysis/analyses`. B2/INV-2 confirmed in real data — safe to delete the `SourcePaths` field.

**Issues Encountered:** None. (5 pre-existing pydantic `parameter_metadata` warnings on freeform concepts 02/03/16/27/35 — unrelated to this change.)

**Deviations from Plan:** None.

### Phase 2 Completion
**Completed:** 2026-06-15
**Changes Made:**
- `findings.py`: promoted `_find_concept_dir` → public `find_concept_dir` (3 occurrences).
- `server.py`: added `ModelType` import; added `_analyses_root(base_dir)` helper (single home for `base_dir.parent/concept_analysis/analyses`), used it at the findings endpoint and in compute; compute 422 gate now `concept.model_type != ModelType.COSTINGFE`; the module-load path derives `model_setup.py` via `find_concept_dir` and raises an explicit `RuntimeError` (→500) when the dir or file is unresolvable (no fallback, FR-5/D3).
- `models.py`: deleted `SourcePaths` class and the `sources` field on `ConceptData`.
- Tests: removed `SourcePaths` from 6 files; restructured the two compute fixtures (`test_state_and_compute.py`, `test_slider_override_semantics.py`) to mirror the real layout (`base_dir/.. /concept_analysis/analyses/{id}-*/model_setup.py`) and set `model_type`; added `test_compute_resolves_without_any_stored_path` (asserts the served JSON has no path and compute still returns 200). Switched the Phase-1 audit test to import `find_concept_dir`.

**Result:** Full suite failure set byte-identical to clean-`main` baseline (34 failed / 39 errored — all pre-existing frontend-JS / Playwright / identity tests), +2 new passes from this work. Compute-specific tests: 14 passed. Zero new lint errors (all 12 ruff findings pre-existing).

**Issues/Deviations:**
- Initially removed the now-dead `analysis_path` parameter from `extract_costingfe`/`extract_standalone` (no-slop cleanup), but it rippled into ~15 test call sites and was scope creep beyond the plan; **reverted** — ruff doesn't select ARG rules, so an unused param isn't flagged, and the extractor change is kept to exactly "drop the `sources=` argument."

### Phase 3 Completion
**Completed:** 2026-06-15
**Changes Made:** `extract_explorer_data.py`: dropped the `sources=SourcePaths(...)` argument from both `ConceptData` constructions (costingfe + standalone branches); removed the `SourcePaths` import. No path is emitted.
**Result:** `test_extract_adapter.py` / `test_extraction.py` extraction tests at baseline (the only failures there are pre-existing). Fresh extraction now emits no `sources` key.

### Phase 4 Completion
**Completed:** 2026-06-15
**Changes Made:** Added `migrate_strip_sources.py` (work-item dir); ran it over all 40 `data/[0-9]*.json`. It round-trips each file through `ConceptData` (drops the unknown `sources` key) and re-emits `model_dump_json(indent=2)` — byte-parity with fresh extractor output (FR-6). Verified `sources` was the ONLY on-disk key absent from the model, so nothing else is lost.
**Result:** FR-1 clean — no `C:\Users\mallo`, `/home/`, `model_setup.py`, or `analysis.md`-as-path strings remain in `data/*.json` (one `analysis.md` remains in 08.json as a human-authored override *citation* string, not a path — correctly left). Diff is the 4-line `sources` block removed per file; two files (27 served, 34 omitted) additionally gained schema-default fields they were missing (stale older-schema files normalized to current — also FR-6-correct).
**Issues/Deviations:**
- Migration script needed a `sys.path` bootstrap (running a script by deep path doesn't put repo root on the path).
- **Ignore-list correction (user-flagged):** a draft regression scan globbed all files and flagged concept 34 (had a real `model_setup` path but `model_type=null` → would 422). Re-running the scan **with the omit list applied** showed 34/26/38 are omitted (server returns 404, never gate-checked). Among the **38 served** concepts, OLD `(model_setup present)` ⟺ NEW `(model_type==costingfe)` holds exactly → compute 200/422 preserved. **No edit made to 34.** Concepts 03/27 have costingfe-shaped `model_setup.py` but were extracted as standalone (model_setup null) — correctly remain 422, unchanged.

### Phase 5 Completion
**Completed:** 2026-06-15
**Changes Made:** None (verification only). Also updated `README.md` §7.5 + the data-model diagram to reflect the `SourcePaths` removal (documented removed code).
**Result (live server, real data):**
- `POST /api/compute {concept_id:"01"}` → **200, `headline.lcoe_per_mwh = 161.6857 ≈ 161.69`** (INV-3 parity).
- freeform concept `03` → **422** (INV-2/D3).
- omitted concept `34` → **404** (ignore list respected).
- Host independence (INV-4): proven by `test_compute_resolves_without_any_stored_path`, which runs the full resolve→load→forward path under an arbitrary `tmp_path` matching no machine.
- Server log clean (no tracebacks/500s).

---

**Status**: Draft → In Progress → Complete
```
