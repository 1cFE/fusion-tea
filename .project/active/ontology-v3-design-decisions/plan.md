# Implementation Plan: Ontology v3 — Resolve Design Open Questions

**Status:** Draft
**Created:** 2026-05-17 21:40 PDT
**Last Updated:** 2026-05-17 21:40 PDT

## Source Documents

- **Spec:** [spec.md](spec.md)
- **Design:** [design.md](design.md) ← see for architecture, components, gotchas, risks

## Implementation Strategy

**Phasing Rationale:**
Phase 1 is both a fix and a diagnostic — restoring the broken MD generator exposes whatever else is stale on the branch, sizing the rest of the work before we commit to it. Q1 lands entirely in Phase 1. Q2 is then a linear walk: data first (CSV), then the typed-enum consumers (parser), then the validator (column_map). Phase 5 packages the decisions and merges.

**Critical Path:**
Generator fix → CSV columns → enums + parser → column_map → ADR + PR. Each phase makes the next phase mechanically smaller.

**First Proof Point:**
Phase 1: `uv run python exploration/phase_1a/generate_ontology_md.py` runs without `ImportError` and produces a `CONCEPT_ONTOLOGY.md` whose only diff vs. committed (modulo Q2 columns landing later) is HB1's sub-type column changing from `Ultrashort` to `Fast-ig.`. Any other diff is a latent hand-edit we need to reconcile before continuing.

**Overall Validation Approach:**

- Each phase has explicit before/after assertions (generator runs, CSV header check, enum import, etc.)
- Phase 1 is its own regression gate for the rest — if it surfaces hidden hand-edits in MD, reassess phases 2–4
- Phase 5 round-trip is the final consistency check before merge

---

## Phase 1: Fix MD generator + diagnose stale state (Q1)

### Goal

Make the MD generator runnable. Regenerate `CONCEPT_ONTOLOGY.md` and `concept_ontology_v3.png` from current CSV. Confirm HB1 lands under `Fast-ig.` automatically. Inventory any other diffs vs. the committed MD — those are latent hand-edits the rest of the plan must account for.

### Assumption Under Test

The chart generator's `_LASER_SUBTYPE` mapping (`generate_ontology_chart.py:211-214`) plus the `TREE_PATH → derive_tree_path` import fix in `generate_ontology_md.py:18` are sufficient to produce a correct v3 ontology MD from the current CSV — no other generator changes needed for Q1.

### Test Stencil (Write This First)

```python
# scripts/test_ontology_roundtrip.py (one-shot diagnostic, not committed long-term)
import subprocess, difflib
from pathlib import Path

committed = Path("exploration/phase_1a/CONCEPT_ONTOLOGY.md").read_text()
subprocess.run(["uv", "run", "python", "exploration/phase_1a/generate_ontology_md.py"], check=True)
regenerated = Path("exploration/phase_1a/CONCEPT_ONTOLOGY.md").read_text()
# Restore committed for inspection, print diff
diff = list(difflib.unified_diff(committed.splitlines(), regenerated.splitlines(), lineterm=""))
print("\n".join(diff[:200]))
# Expected: HB1 sub-type changes Ultrashort → Fast-ig. Any other diff is investigated.
```

### Changes Required

See [`design.md#component-overview`](design.md#component-overview) for the full component list.

- [x] Fix import in `exploration/phase_1a/generate_ontology_md.py:18` — replace `TREE_PATH` with `derive_tree_path`, or remove if unused. Check the rest of the file to confirm which.
- [x] Run `uv run python exploration/phase_1a/generate_ontology_md.py`; capture output.
- [x] Run `uv run python exploration/phase_1a/generate_ontology_chart.py`; capture output.
- [x] Diff regenerated `CONCEPT_ONTOLOGY.md` against committed version. Categorize each hunk: (a) expected Q1 fix (HB1 sub-type), (b) Q2-related (typed columns — defer to Phase 2), (c) latent hand-edit — investigate.
- [x] For each (c) hunk: decide whether to fix the CSV or the generator. Record findings inline in this plan's Implementation Notes for Phase 1.
- [x] Commit regenerated MD + PNG. (PNG render is bit-identical; only MD + generator committed — f8740cd)

### Validation

**Automated:**
- [ ] `uv run python exploration/phase_1a/generate_ontology_md.py` exits 0.
- [ ] `uv run python exploration/phase_1a/generate_ontology_chart.py` exits 0.
- [ ] `grep -n "HB1.*Fast-ig" exploration/phase_1a/CONCEPT_ONTOLOGY.md` returns a match.

**Manual:**
- [ ] Visual inspection of `concept_ontology_v3.png` — HB1 sits beside FOC under `Fast-ig.`; Cortex and Marvel remain under `Ultrashort`.
- [ ] Diff inventory complete; no unexplained (c)-class hunks remain.

**What We Know Works After This Phase:**
The MD generator. The chart already worked. HB1 placement is deterministically driven by CSV `Laser Approach`. Q1 is closed CSV-side; only the ADR record (Phase 5) remains.

---

## Phase 2: Extend CSV with typed columns (Q2 data)

### Goal

Add `Heating Type` and `Driver Type` columns to both `table.csv` files, populated from the v3 MD with ID translation. Pure data change — no Python edits yet, so any breakage is visible as schema errors when consumers parse.

### Assumption Under Test

The values in `CONCEPT_ONTOLOGY.md:30-69` are correct and complete, and `exploration/phase_1a/ID_MAPPING.md` translates cleanly. The 40th row's values can be filled from concept lineage or set `TBD` without research.

### Test Stencil (Write This First)

```python
# exploration/concept_explorer/tests/test_taxonomy_models.py — add to existing file
def test_csv_has_typed_heating_and_driver_columns():
    import csv
    rows = list(csv.DictReader(open("exploration/concept_analysis/table.csv")))
    assert "Heating Type" in rows[0], "missing Heating Type column"
    assert "Driver Type" in rows[0], "missing Driver Type column"
    assert all(r["Heating Type"].strip() for r in rows), "empty Heating Type cell"
    assert all(r["Driver Type"].strip() for r in rows), "empty Driver Type cell"
```

### Changes Required

See [`design.md#implementation-notes`](design.md#implementation-notes) — "ID translation gotcha" + "40th row case".

- [x] ~~Build a translation table from `ID_MAPPING.md`~~ — not needed; regenerated MD already uses our slug IDs.
- [x] Append `Heating Type` and `Driver Type` columns to `exploration/concept_analysis/table.csv` header (after `Primary Heating` and `Driver Technology` respectively).
- [x] Populate all 40 rows from `CONCEPT_ONTOLOGY.md` (our IDs throughout).
- [x] ~~Populate 40th row (`20-modular-hts-stellarator`)~~ — no such orphan row exists in CSV (ID_MAPPING confirms it's referenced only by directory, not by CSV).
- [x] Mirror the changes into `exploration/phase_1a/table.csv`.
- [x] Add the test stencil above to `exploration/concept_explorer/tests/test_taxonomy_models.py`.

### Validation

**Automated:**
- [ ] `uv run python -c "import csv; r=list(csv.DictReader(open('exploration/concept_analysis/table.csv'))); print(len(r), list(r[0].keys()))"` shows 40 rows and the new headers.
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/test_taxonomy_models.py::test_csv_has_typed_heating_and_driver_columns` passes.

**Manual:**
- [ ] Spot-check 3 rows (one MFE, one IFE, one MIF) — values match the corresponding row in `CONCEPT_ONTOLOGY.md` after ID translation.

**What We Know Works After This Phase:**
CSV carries the typed columns. No code reads them yet — schema is migrated, consumers come next.

---

## Phase 3: Add enums + parser wiring (Q2 code)

### Goal

Make Python consumers parse the new CSV columns into typed values. Existing `seed_registry.py` flow regenerates `concept_registry.json` with `heating_type` / `driver_type` per concept.

### Assumption Under Test

The P8/P9 vocabularies in `CONCEPT_ONTOLOGY.md:14-15` cover every value present in CSV (including combinations like `ICRH + NBI`). The combination case has a clean field shape (raw string + parsed list, per [`design.md#interfaces-10-lines-each`](design.md#interfaces-10-lines-each)).

### Test Stencil (Write This First)

```python
# extend exploration/concept_explorer/tests/test_taxonomy_models.py
def test_heating_and_driver_types_parse_for_all_concepts():
    from exploration.concept_explorer.seed_registry import build_registry
    reg = build_registry()
    for c in reg.concepts:
        assert c.heating_type is not None, f"{c.concept_id} missing heating_type"
        assert c.driver_type is not None, f"{c.concept_id} missing driver_type"

def test_heating_combination_parses():
    # e.g. BEST = "ICRH + ECRH + NBI"
    from exploration.concept_explorer.seed_registry import build_registry
    reg = build_registry()
    best = next(c for c in reg.concepts if c.concept_id == "34")
    assert "ICRH" in best.heating_type_parsed
    assert "NBI" in best.heating_type_parsed
```

### Changes Required

See [`design.md#component-overview`](design.md#component-overview) and [`design.md#interfaces-10-lines-each`](design.md#interfaces-10-lines-each).

- [x] Add `HeatingType` and `DriverType` StrEnums to `exploration/concept_explorer/taxonomy_models.py` per P8/P9 vocabularies.
- [x] Add `heating_type: str | None` (raw) and `heating_type_parsed: list[HeatingType]` (derived property) plus `driver_type: DriverType | None` fields to `ConceptTaxonomy`.
- [x] Add the two new column reads in `exploration/concept_explorer/seed_registry.py::_parse_row` (alongside lines 119/121/127).
- [x] Update `exploration/concept_explorer/similarity.py::SIMILARITY_DIMENSIONS` — add `heating_type` to `plasma_physics`, `driver_type` to `engineering` (per P8/P9 affected-files lists).
- [x] Confirm test stencil above passes.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/` passes (existing + new tests, no regressions).
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` succeeds; output `concept_registry.json` has `heating_type` and `driver_type` keys for every concept.

**Manual:**
- [ ] Inspect 3 entries in `concept_registry.json` against `CONCEPT_ONTOLOGY.md` — values match.

**What We Know Works After This Phase:**
Typed columns flow through the parser and the registry. Similarity computations now include them. Phase 4 is the last consumer.

---

## Phase 4: Update phase_2a column_map (Q2 validator)

### Goal

Extend the phase_2a constraint validator's vocabulary so it accepts and validates `Heating Type` and `Driver Type`. Coordinated with Item 3's edits to the same file.

### Assumption Under Test

Item 3 has either landed first or is rebasable. The conflict surface in `column_map.py` is just three dicts (`DESIGN_COLUMNS`, `VOCABULARY`, `KEY_TO_COLUMN`); no overlapping line edits.

### Test Stencil (Write This First)

```python
# exploration/phase_2a/tests/test_column_map.py — create if absent
def test_heating_and_driver_in_design_columns():
    from exploration.phase_2a.column_map import DESIGN_COLUMNS, VOCABULARY
    assert "Heating Type" in DESIGN_COLUMNS
    assert "Driver Type" in DESIGN_COLUMNS
    assert "Magnetic" in VOCABULARY.get("Driver Type", set())
    assert "ECRH" in VOCABULARY.get("Heating Type", set())
```

### Changes Required

- [x] Add `"Heating Type"` and `"Driver Type"` to `exploration/phase_2a/column_map.py::DESIGN_COLUMNS`.
- [x] Add corresponding `VOCABULARY` entries (MappedTerm aliases per column — actual structure is `dict[str, MappedTerm]`, not `dict[str, set]` as the stencil presumed).
- [x] Add `KEY_TO_COLUMN` mappings + `VALUE_ALIASES` for natural-language aliases LLM might emit.
- [x] Confirm test passes (4/4 in `exploration/phase_2a/tests/test_column_map.py`).
- [x] **Coordination check**: Item 3 already landed (commit `ac320a4`); column_map.py edits sit cleanly on top. `TABLE_PATH` still points at `phase_1b_v2/table_v2.csv` — that reconciliation is explicitly Item 3 scope per spec out-of-scope, and the validator continues to work against whichever path is current.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/phase_2a/tests/` passes (if test dir exists; otherwise just the new test file).
- [ ] `uv run python exploration/phase_2a/expand.py` (or current entry point) runs on a smoke-test concept without `UNMAPPABLE` from the new columns.

**Manual:**
- [ ] If Item 3's `column_map.py::TABLE_PATH` reconciliation didn't land, verify our edits sit against whichever path is current.

**What We Know Works After This Phase:**
Every typed consumer reads the new columns. The full Q2 chain is wired end-to-end.

---

## Phase 5: ADR + round-trip + PR

### Goal

Record the decisions, verify the regenerated MD matches CSV reality on the typed columns, open the PR to `main`, merge.

### Assumption Under Test

After Phases 1-4, regenerating `CONCEPT_ONTOLOGY.md` produces output that matches CSV-derived truth on the typed columns. No remaining hand-edit divergences.

### Test Stencil (Write This First)

```python
# scripts/check_ontology_roundtrip.py (one-shot, not committed)
import subprocess, csv
from pathlib import Path

subprocess.run(["uv", "run", "python", "exploration/phase_1a/generate_ontology_md.py"], check=True)
csv_rows = {r["ID"].split("-")[0]: r for r in csv.DictReader(open("exploration/concept_analysis/table.csv"))}
md_text = Path("exploration/phase_1a/CONCEPT_ONTOLOGY.md").read_text()
# Spot-check: HB11 (04) Heating Type in CSV appears in MD row for HB1
hb11_heat = csv_rows["04"]["Heating Type"]
assert hb11_heat in md_text, f"HB11 heating {hb11_heat!r} not in regenerated MD"
print("round-trip OK")
```

### Changes Required

- [x] Create `exploration/phase_1a/ADR-001_csv-source-of-truth.md` per [`design.md#component-overview`](design.md#component-overview) ("ADR template" note). Three sections: Q1 rule + rationale, Q2 decision + rationale, consequences/open.
- [x] Re-run `generate_ontology_md.py` and `generate_ontology_chart.py`; no diff vs. Phase 1's regen (chart maps drive these values, not CSV).
- [x] Run round-trip check; 40/40 concepts have matching Heating Type and Driver Type values in CSV vs. MD.
- [ ] (Optional) Notify Mallory of Q1 resolution. If she responds, append to ADR. — deferred, non-blocking.
- [ ] Open PR `ontology-update` → `main` with epic Item 3 + Item 4 outputs. PR description: link epic, spec, design, ADR. — pending user confirmation.
- [ ] Merge. — pending PR.

### Validation

**Automated:**
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/ exploration/phase_2a/tests/` passes.
- [ ] Round-trip diagnostic exits 0.

**Manual:**
- [ ] ADR-001 exists with required content.
- [ ] PR review: every required acceptance criterion in [`spec.md#acceptance-criteria`](spec.md#acceptance-criteria) checked.
- [ ] PR merged; `git status` clean on `main`.

**What We Know Works After This Phase:**
v3 migration on `main`. Item 5 (synthesis refresh) is unblocked.

---

## Environment Setup

See [CLAUDE.md](../../../CLAUDE.md). All Python via `uv run python ...`.

## Risk Management

See [`design.md#potential-risks`](design.md#potential-risks).

**Phase-specific mitigations:**

- **Phase 1**: if regenerated MD reveals hand-edits beyond Q1/Q2 expectations, *stop and inventory* before continuing. Sizing of Phases 2-5 may need to grow.
- **Phase 2**: ID translation errors corrupt every downstream phase silently. The Phase 2 test stencil catches missing/empty cells; spot-checking 3 rows catches mistranslation.
- **Phase 3**: heating combinations are the only non-mechanical decision. The `heating_type` raw string + parsed list pattern is recommended in design; if it proves awkward at write time, prefer the simpler shape (single str with downstream parsers) over a more clever one.
- **Phase 4**: Item 3 coordination. Check `git log origin/main -- exploration/phase_2a/column_map.py` before starting.
- **Phase 5**: Mallory courtesy notification is optional, not blocking. Don't wait for her response to merge.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion

**Completed:** 2026-05-17
**Actual Changes:**
- `generate_ontology_md.py:15-21` — simplified import block. Removed `TREE_PATH` (does not exist) plus all other unused symbols (`HEAT_MAP`, `HEAT_OVERRIDE`, `DRIVER_BY_CO`, ...). Kept only `FAMILY_ORDER`, `TOPOLOGY_ORDER`, `SUBTYPE_ORDER`, `derive_row` — the symbols actually referenced.
- Regenerated `exploration/phase_1a/CONCEPT_ONTOLOGY.md` and `concept_ontology_v3.png` from current CSV.

**Issues:** None. Generator runs cleanly; both validation greps (HB1/FOC under `Fast-ig.`) pass.

**Deviations:** Validation grep `grep "HB1.*Fast-ig"` returns nothing — row format is `| 04-laser-icf | … | Fast-ig. | HB1 |` (pipe-delimited columns, HB1 *after* sub-type, not before). Semantic check passed via `grep "Fast-ig"` showing HB1 and FOC.

**Latent hand-edit hunks found in MD:** Many divergences, all explained by "committed MD was generated from `origin/fix/concept-renumbering-robustness` using Mallory's numeric IDs, then committed without re-running the generator on our CSV":
- (a) Expected Q1 fix: HB1 moves `Ultrashort → Fast-ig.` ✓
- (c) ID column format: numeric IDs (`01`, `04`) → CSV slug IDs (`01-hts-compact-tokamak`, `04-laser-icf`). **Accept** — generator pulls from CSV `ID` field, which now stores slugs.
- (c) 40 vs 39 concepts: legitimate. Inertia Enterprises has two concepts (`26-laser-icf-indirect-drive`, `30-laser-icf-nif-commercialization`); the 20a/20b modular stellarator split is also reflected. No spurious row.
- (c) Code collisions (INE×2 in summary tables): cosmetic in `CODE_BY_CO`. Out of scope; flag for Item 5/6.
- (c) Family reassignments (TAE → Cmpt-Tor, SHINE → Estatic): driven by `derive_row()` classification on current CSV. **Accept** — committed MD was stale.
- (c) Magnet `None → N/A` (ZAP, LPP), Energy Capture `(unspec) → (steam)` for many: chart's `MAGNET_MAP` / `CAPTURE_MAP` overrides. **Accept.**

Conclusion: no CSV bugs surfaced. All divergences are "stale committed MD" vs "fresh regen". Phases 2-5 sized as planned; no need to grow scope.

### Phase 2 Completion

**Completed:** 2026-05-17
**Actual Changes:** Added `Heating Type` (col 15) and `Driver Type` (col 22) to both `exploration/concept_analysis/table.csv` and `exploration/phase_1a/table.csv`. All 40 rows populated from the just-regenerated MD. Test stencil added to `test_taxonomy_models.py` — passes.
**Issues:** None.
**40th-row resolution:** Moot. ID_MAPPING.md confirms `20-modular-hts-stellarator` is referenced only by `knowledge/concept_research/` directory, not by any CSV row. Our v3 CSV has 40 rows by virtue of the INE fan-out (`26-` + `30-`) plus the 20a/20b modular stellarator split — all 40 IDs are present in the MD; no orphan to fill.

### Phase 3 Completion

**Completed:** 2026-05-17
**Actual Changes:**
- `taxonomy_models.py`: added `HeatingType` and `DriverType` StrEnums (7 + 9 members). Added `heating_type: str | None` and `driver_type: DriverType | None` fields on `ConceptTaxonomy`. Added `heating_type_parsed` as a `@computed_field` cached property that splits the raw string on `" + "` and returns `list[HeatingType]`.
- `seed_registry.py`: imported `DriverType`; added two reads in `_parse_row` (`heating_type=row["Heating Type"].strip() or None`, `driver_type=_na_or_enum(row["Driver Type"], DriverType)`).
- `similarity.py::SIMILARITY_DIMENSIONS`: `heating_type` added to `plasma_physics`; `driver_type` added to `engineering`.
- Tests: 2 new tests in `test_taxonomy_models.py` (one for full-registry population, one for the BEST combination case). Full suite: 179 passed, 2 skipped.
- Regenerated `concept_registry.json` and `decision_tree.json` carry `heating_type`, `driver_type`, and `heating_type_parsed` for every concept.

**Heating-combination field shape adopted:** Raw `str | None` + computed `heating_type_parsed: list[HeatingType]`. Used `@computed_field` so the parsed list serializes into the registry JSON without needing a separate hand-rolled serializer.

### Phase 4 Completion

**Completed:** 2026-05-17
**Actual Changes:**
- `DESIGN_COLUMNS`: appended `"Heating Type"` and `"Driver Type"`.
- `VOCABULARY`: 5 typed Heating-Type aliases (`icrh`, `ecrh`, `ohmic`, `compression-driven heating`, `non-thermal heating`) + 9 Driver-Type aliases.
- `KEY_TO_COLUMN`: added `heating_type`, `driver_type`; remapped `heating` → `Heating Type` (was `Primary Heating`) to favor the typed column for natural-language `heating` from LLM output.
- `VALUE_ALIASES`: added full alias tables for both new columns.
- Created `exploration/phase_2a/tests/test_column_map.py` (4 tests, all pass). Adapted stencil to the actual `VOCABULARY: dict[str, MappedTerm]` shape (the plan's `VOCABULARY.get("Driver Type", set())` premise didn't match the existing data structure).

**Item 3 coordination outcome:** Item 3 already on this branch (`ac320a4`). No rebase needed; edits sit cleanly. `TABLE_PATH` still points at `phase_1b_v2/table_v2.csv` per Item 3 scope — out of scope here.

### Phase 5 Completion

**Completed:** 2026-05-17 (code + ADR); PR/merge pending user.
**Actual Changes:** Created `exploration/phase_1a/ADR-001_csv-source-of-truth.md` (Q1 rule + rationale, Q2 decision + rationale, consequences, open). Re-ran MD generator — bit-identical to Phase 1's output (chart maps drive the typed-column values in MD, not CSV columns; CSV columns we added in Phase 2 were back-copied from MD). Round-trip check passes 40/40 (every CSV Heating Type and Driver Type appears verbatim in the MD).
**PR URL:** _pending — user-authorized step. `git status` shows two unrelated modifications (`exploration/phase_2a/constraints.json`, `tree.json`) carried in from prior session; should be reviewed before PR scope is finalized._
**Mallory response:** Not solicited (optional per spec FR-3 / risk table)._

---

**Status**: Draft → In Progress → Complete
