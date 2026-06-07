# Implementation Plan: Concept Explorer Omit List

**Status:** Complete
**Created:** 2026-06-05 13:25
**Last Updated:** 2026-06-05 (implementation complete — all 4 phases)

## Source Documents
- **Spec:** `.project/active/concept-explorer-omit-list/spec.md`
- **Design:** `.project/active/concept-explorer-omit-list/design.md` ← component details, invariants, architecture, gotchas

## Implementation Strategy

**Phasing Rationale:**
One shared loader, two independent consumers. Phase 1 builds the loader and kills the one real correctness risk (int-vs-string key) before any call site exists. Phases 2–4 are the three enforcement points; they are mutually independent (FR-6), so order is by risk, not dependency — extraction (2), then server concept-load (3), then server taxonomy/tree prune (4, the only non-trivial transform).

**Critical Path:**
Phase 1 (loader) → unblocks 2, 3, 4 (any order). Each later phase calls `load_omit_list()` and is otherwise self-contained.

**First Proof Point:**
Phase 1 test — an *unquoted* `26:` YAML key resolves to `{"26"}` matching `parse_concept_id` output. If that passes, every other site is a one-line membership check.

**Overall Validation Approach:**
- Each phase starts with tests (pytest + `tmp_path`, matching existing `tests/`).
- Each phase proves its consumer works *in isolation* (the independence requirement).
- Full suite (`exploration/concept_explorer/tests/`) green after each phase — no regressions.

---

## Phase 1: Shared Loader + Omit File

### Goal
Create `omit_list.yaml` and `load_omit_list() -> set[str]` in `models.py`. Foundation for all enforcement; contains the only real correctness risk.

### Assumption Under Test
A numeric YAML key matches the string ID from `parse_concept_id`; missing/empty file and unknown IDs are no-ops (FR-8, I-1).

### Test Stencil (Write This First)
```python
# tests/test_models.py
def test_load_omit_list_unquoted_numeric_key_matches_string_id(tmp_path):
    (tmp_path / "omit_list.yaml").write_text("26: bad data\n34: dup\n")
    assert load_omit_list(tmp_path / "omit_list.yaml") == {"26", "34"}

def test_load_omit_list_missing_file_is_empty_set(tmp_path):
    assert load_omit_list(tmp_path / "nope.yaml") == set()

def test_load_omit_list_empty_file_is_empty_set(tmp_path):
    (tmp_path / "omit_list.yaml").write_text("")
    assert load_omit_list(tmp_path / "omit_list.yaml") == set()
```

### Changes Required

**See `design.md` for:** loader behavior → `design.md#component-overview`; key gotcha → `design.md#implementation-notes`; invariant I-1 → `design.md#required-invariants`.

#### 1. Test File
**File:** `exploration/concept_explorer/tests/test_models.py` (extend)
- [x] Add the three stencil tests above
- [x] Add: reasons-ignored (values discarded), and an int-key coerced to str

#### 2. Omit File
**File:** `exploration/concept_explorer/omit_list.yaml` (NEW)
- [x] Create with quoted keys `"26"`/`"27"`/`"34"`/`"38"` + one-line reason each

#### 3. Loader
**File:** `exploration/concept_explorer/models.py` (add `import yaml`, near `build_manifest`)
- [x] `load_omit_list(path: Path | None = None) -> set[str]`; default `Path(__file__).parent / "omit_list.yaml"`
- [x] Missing/empty file → `set()`; coerce keys `str(k)`; discard values
- [x] Let malformed YAML raise (author bug — fail loud, per design)

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_models.py` → pass (23 passed)
- [x] Full suite → no regressions (run after Phase 4)

**Manual:**
- [x] `uv run python -c "from exploration.concept_explorer.models import load_omit_list; print(load_omit_list())"` → `{'26','27','34','38'}`

**What We Know Works After This Phase:**
The shared loader and the int-vs-string match. Everything downstream is membership checks.

---

## Phase 2: Extraction Enforcement (Consumer #1)

### Goal
`discover_concepts()` skips omitted IDs so no `data/{id}.json` is written/refreshed; omitted concepts join the existing `skipped` report.

### Assumption Under Test
Omitted concepts produce no data file; non-omitted still extract — with no server involvement (independence).

### Test Stencil (Write This First)
```python
# tests/test_extraction.py
def test_discover_concepts_excludes_omitted(tmp_path, monkeypatch):
    # analyses/ with 05 + 27; omit {"27"}
    ids = [parse_concept_id(d.name) for d in discover_concepts(analyses, {"27"})]
    assert "05" in ids and "27" not in ids
```

### Changes Required

**See `design.md` for:** insertion point → `design.md#component-overview`; reporting → `design.md#implementation-notes`; I-2 → `design.md#required-invariants`.

**Specific file changes:**
- [x] `extract_explorer_data.py:836` — `discover_concepts()` takes/loads the omit set; skip when `concept_id` is in it. Pass the set from `run_extraction` (load once at top) so it is testable.
- [x] `extract_explorer_data.py:971` — add omitted concepts to the `skipped` list with reason `"omit_list"`
- [x] `tests/test_extraction.py` — stencil + assert no `data/27.json` written by a `run_extraction` over a tmp analyses dir

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_extraction.py` → pass (71 passed, 4 new)

**Manual:**
- [x] Scoped run `--concept 05 26 --skip-narrative` → stdout reports `26: omit_list`, 05 extracted; `data/26.json` mtime unchanged (used a kept+omitted pair to avoid rewriting all of `data/`; full-run early-returns only if *every* discovered dir is omitted)

**What We Know Works After This Phase:**
Extraction-side skip + report, independent of the server.

---

## Phase 3: Server Concept-Load Filter (Consumer #2, Part A)

### Goal
`_load_data()` drops omitted IDs from the globbed concept set; manifest + parameter index follow automatically (built from the filtered list).

### Assumption Under Test
Filtering only the loaded list removes omitted concepts from manifest and parameter index too (I-4) — no double-filter needed; stale on-disk `26/27/34.json` are hidden with no extraction run (independence).

### Test Stencil (Write This First)
```python
# tests/test_server.py
def test_load_data_excludes_omitted(tmp_path, monkeypatch):
    # data/ with 05.json + 27.json on disk; omit {"27"}
    concepts, manifest, pindex = _load_data(data_dir)  # omit patched to {"27"}
    assert "27" not in concepts
    assert all(c.concept_id != "27" for c in manifest.concepts)
    assert (data_dir / "27.json").exists()  # I-6: file untouched
```

### Changes Required

**See `design.md` for:** filter point → `design.md#component-overview`; "don't double-filter" → `design.md#implementation-notes`; I-3/I-4/I-6 → `design.md#required-invariants`.

**Specific file changes:**
- [x] `server.py:200` — in `_load_data()`, after the `_NON_CONCEPT_FILES` glob, exclude paths whose `parse_concept_id`/stem is in `load_omit_list()`. Filter the concept set only; leave `build_manifest`/`build_parameter_index` as-is.
- [x] `tests/test_server.py` — stencil + assert manifest and parameter index both exclude the omitted ID, and the on-disk file remains

### Validation
**Automated:**
- [x] `uv run python -m pytest exploration/concept_explorer/tests/test_server.py` → pass (26 passed, 3 new)

**Manual:**
- [x] `_load_data(real data/)` with default omit → 26/27/34/38 absent from concepts + manifest; `data/26.json` still on disk; 35 concepts loaded

**What We Know Works After This Phase:**
Profiles, comparison, manifest, parameter index all exclude omitted concepts; existing files untouched.

---

## Phase 4: Server Taxonomy Filter + Tree Prune (Part B)

### Goal
`_load_taxonomy()` filters `registry.concepts` (→ similarity, constellation) and prunes omitted IDs from the decision tree, dropping emptied branches.

### Assumption Under Test
Registry filter covers similarity/constellation (no positional assumptions); `prune_decision_tree` removes IDs from leaf `concepts` and drops empty branches while leaving siblings intact (I-3, I-5).

### Test Stencil (Write This First)
```python
# tests/test_taxonomy_server.py / test_taxonomy_models.py
def test_prune_drops_emptied_branch_keeps_siblings():
    tree = {"field":"f","children":[
        {"value":"A","concepts":["27"]},          # becomes empty -> dropped
        {"value":"B","concepts":["05","27"]}]}     # keeps "05"
    out = prune_decision_tree(tree, {"27"})
    vals = [c["value"] for c in out["children"]]
    assert vals == ["B"] and out["children"][0]["concepts"] == ["05"]
```

### Changes Required

**See `design.md` for:** prune sketch + "filter registry once" → `design.md#implementation-notes`; tree shape → `design.md#research-findings`; I-3/I-5 → `design.md#required-invariants`.

**Specific file changes:**
- [x] `taxonomy_models.py` — add `prune_decision_tree(tree: dict, omitted: set[str]) -> dict` (recursive: strip `concepts`, recurse `children`, drop subtrees with zero concepts). Pure function, no I/O. (Plus `_subtree_has_concepts` helper.)
- [x] `server.py:248` — in `_load_taxonomy()`, after `model_validate_json`/`json.loads`: filter `registry.concepts` to drop omitted (rebuild via `registry.model_copy(update=...)`); apply `prune_decision_tree` to the loaded tree's `root` before computing similarity/constellation.
- [x] Spot-check `compute_similarity_matrix`/`compute_constellation` take the concept list as input (no fixed-count/positional assumption) — confirmed (see Implementation Notes).
- [x] `tests/test_taxonomy_models.py` — prune unit tests (5); `tests/test_taxonomy_server.py` — assert omitted IDs absent from `/api/taxonomy/tree`, registry, similarity, and constellation responses

### Validation
**Automated:**
- [x] `uv run python -m pytest .../test_taxonomy_server.py .../test_taxonomy_models.py` → pass (54 passed)
- [x] Full suite → no NEW regressions (215 passed / 2 skipped excluding pre-existing adapter failures; see Implementation Notes)

**Manual:**
- [x] `_load_taxonomy(real data/)` default omit → registry=37, no 26/27/34/38 in registry/tree/constellation/neighbors; **no dead-end tree branches**

**What We Know Works After This Phase:**
Full "omit from EVERYTHING" — registry, similarity, constellation, and decision tree all clean.

---

## Environment Setup

**See CLAUDE.md** — all Python via `uv run`. Tests: `uv run python -m pytest exploration/concept_explorer/tests/`.

---

## Risk Management

**See `design.md#potential-risks` for detail.**

**Phase-Specific Mitigations:**
- **Phase 1**: explicit unquoted-numeric-key test before any call site exists — the riskiest bug dies first.
- **Phase 4**: prune is the only non-trivial transform — unit-tested in isolation with a fixture mirroring the real `{children, concepts}` shape before wiring into `_load_taxonomy`. Spot-check similarity/constellation for positional assumptions.

## Implementation Notes

### Phase 1 Completion
**Completed:** 2026-06-05

**Changes made:**
- Created `exploration/concept_explorer/omit_list.yaml` — quoted keys `"26"/"27"/"34"/"38"` with one-line reasons + header documenting format and the quoted-key rule.
- `models.py` — added `from pathlib import Path` + `import yaml`; added `_OMIT_LIST_PATH` and `load_omit_list(path=None) -> set[str]` (coerces keys to `str`, discards reasons, missing/empty → `set()`, malformed YAML raises).
- `tests/test_models.py` — `TestLoadOmitList` (8 tests): unquoted-numeric-key match, quoted keys, suffixed ID, reasons discarded, missing/empty/comments-only → `set()`, default-path initial set.

**Result:** 23 passed; manual `load_omit_list()` → `{'26','27','34','38'}`.

### Phase 2 Completion
**Completed:** 2026-06-05

**Changes made:**
- `extract_explorer_data.py` — imported `load_omit_list`; `discover_concepts()` gained `omitted: set[str] | None = None` and skips omitted IDs; `run_extraction()` loads the omit list once and passes it in.
- Reporting: rather than threading omitted dirs out of `discover_concepts` (which returns only kept dirs), `run_extraction` re-calls `discover_concepts(..., omitted=None)` to get the unfiltered eligible set and appends those in the omit set to `skipped` with reason `"omit_list"`. Cheap second dir-scan, no logic duplication.
- `tests/test_extraction.py` — `TestOmitListExtraction` (4 tests): discover excludes/keeps, no data file written for omitted while non-omitted extracts (+ report), and a pre-existing omitted file is **not refreshed**.

**Deviation from plan:** plan said add to `skipped` "at :971 in the loop"; since `discover_concepts` filters omitted out *before* the loop, they can't be added from inside it. Reporting is done right after discovery instead (same `skipped` list, same `"omit_list"` reason, same output block) — satisfies FR-3.

**Edge case noted:** if `--concept` is scoped to *only* omitted IDs, `concept_dirs` is empty and `run_extraction` early-returns ("no concept directories found") before the skipped report prints. Pre-existing early-return behavior; harmless (a normal full run never hits it). Manual check therefore used a kept+omitted pair (`--concept 05 26`).

**Result:** 71 passed (4 new). Manual: `05` extracted, `26: omit_list` reported, `data/26.json` mtime unchanged.

### Phase 3 Completion
**Completed:** 2026-06-05

**Changes made:**
- `server.py` — imported `load_omit_list`; `_load_data()` gained `omitted: set[str] | None = None` (default `None` → `load_omit_list()`); concept files filtered by `f.stem not in omit_set` *before* validation (so omitted files aren't even parsed). Manifest/parameter index unchanged — they derive from the filtered list (I-4).
- `tests/test_server.py` (3 tests): omitted absent from concepts/manifest/parameter-index; on-disk file remains (I-6); empty omit keeps all.

**Result:** 26 passed (3 new). Manual: real `data/` → 35 loaded, 26/27/34/38 absent from concepts + manifest, `data/26.json` on disk.

### Phase 4 Completion
**Completed:** 2026-06-05

**Changes made:**
- `taxonomy_models.py` — added pure `prune_decision_tree(node, omitted)` + `_subtree_has_concepts(node)` helper (non-mutating; strips omitted from leaf `concepts`, drops subtrees with zero concepts).
- `server.py` — imported `prune_decision_tree`; `_load_taxonomy()` gained `omitted` param (default `None` → `load_omit_list()`); filters `registry.concepts` via `model_copy(update=...)` before similarity/constellation (I-5), and prunes `decision_tree["root"]`.
- `tests/test_taxonomy_models.py` — `TestPruneDecisionTree` (5 tests: drop emptied branch + keep siblings, no-mutation, nested collapse, nested survival, empty-omit no-op).
- `tests/test_taxonomy_server.py` — derived `_EXPECTED_REGISTRY_COUNT` from source files; **updated two existing count assertions** (`registry`, `constellation`) from `40` to the computed post-omit count; added endpoint tests (tree/constellation/similarity exclude omitted, omitted→404) and two direct `_load_taxonomy` tests.

**Spot-check (plan-required):** `compute_similarity_matrix(registry)` derives `n=len(registry.concepts)` and `concept_ids` dynamically (similarity.py:310–311); `compute_constellation(matrix, registry)` builds `id_to_concept` from the list (similarity.py:388). **No positional/fixed-count assumptions** — filtering the registry to 37 is safe.

**Important finding (registry membership):** of the omit set, only **26/27/38** are in the registry/tree; **34 is in `data/` but not in the taxonomy** (matches spec Current State). So the post-omit registry/constellation count is **37** (40 − 3), not 36. The two updated count assertions compute this from the source files + omit list rather than hard-coding, so they track `omit_list.yaml`.

### Cross-cutting notes

**Pre-existing test failures (NOT caused by this work):** `tests/test_extract_adapter.py` has **6 failing tests** (TestStrictConsumer, TestVerifyTwoKnob, TestRoutingCrossCheck) that expect `run_extraction` to *raise* on per-concept errors. They fail identically with my source changes stashed — they were broken by the keep-going batch refactor (commit `effed3de`), which records per-concept errors and continues instead of raising. Out of scope for the omit-list work; flagged for the user.

**Full-suite result:** excluding that pre-existing-failing file, **215 passed / 2 skipped** (the 2 skips are the manual server-integration tests). Omit-list additions: 8 + 4 + 3 + 5 + endpoint/loader tests, all green.

---

**Status**: Draft → In Progress → **Complete**
