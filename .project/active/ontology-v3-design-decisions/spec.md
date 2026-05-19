# Spec: Ontology v3 — Resolve Design Open Questions

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-17 21:30 PDT
**Complexity:** LOW
**Branch:** `ontology-update` (PR target: `main`)
**Epic:** [ONTOLOGY-V3](../../backlog/epic_ontology_v3_migration.md) — Item 4
**Depends on:** Item 3 (`.project/active/ontology-v3-close-gaps/`)

---

## Work Item Summary

Resolve the two design open questions blocking the v3 ontology merge to `main`: HB11's `Fast ignition` (CSV) vs `Ultrashort` (ontology MD) disagreement, and the missing typed `Heating Type` / `Driver Type` columns in `table.csv` that the v3 MD already populates. Both have the same root cause — Mallory partially executed her own P8/P9 proposals. Investigation during research showed both fixes are mechanical: Q1 is a broken MD generator (`ImportError` on `TREE_PATH`), not a classification decision; Q2 is two columns to thread through existing typed-enum machinery that the generators already expect.

## Why This Matters Now

The v3 migration's whole point is eliminating dual-source-of-truth drift. Shipping it with two known contradictions defeats that goal and forces them to be chased through downstream consumers later. This work item is the gate that lets the migration land on `main` and unblocks Item 5 (synthesis refresh).

## Key Bets / Constraints

- **Bet (Q1):** CSV is correct. HB11's `Laser Approach = Fast ignition` matches company self-branding, two-pulse architecture, and Mallory's own `RECLASSIFIED_CONCEPTS.md`. The chart generator already maps `Fast ignition → Fast-ig.`; the MD just needs to be regenerated.
- **Bet (Q2):** Extend the CSV with typed `Heating Type` and `Driver Type` columns (option (a) from research). This is what `SCHEMA_REVISION_PROPOSALS.md` P8/P9 prescribe and what the generators already read.
- **Constraint:** Per-concept analysis artifacts (`analyses/*/synthesis.md`, `model_setup.py`) are untouched — Item 5 territory.
- **Constraint:** Legacy `Primary Heating` / `Driver Technology` free-text columns stay; they carry richer per-concept detail than the typed enums.
- **Non-goal:** Rerunning scoring (Item 3), refreshing synthesis (Item 5), reconciling `column_map.py`'s wrong-CSV-path bug (Item 3), Pacific Fusion row split (already resolved via P4 magnet vocab collapse).

---

## Business Goals

### Why This Matters

The v3 migration eliminates dual-source-of-truth drift. Shipping with known contradictions defeats the purpose and creates technical debt that downstream consumers will inherit silently.

### Success Criteria

- [ ] HB11's `Laser Approach` value is consistent across `table.csv`, `CONCEPT_ONTOLOGY.md`, the chart PNG, `RECLASSIFIED_CONCEPTS.md`, and the dossier.
- [ ] `table.csv` carries typed `Heating Type` and `Driver Type` columns; downstream enums and parsers consume them.
- [ ] An ADR records both decisions and their rationale.
- [ ] `ontology-update` merged to `main`.

### Priority

P0 — gates the entire v3 migration's arrival on `main`. Blocks Item 5.

---

## Problem Statement

### Current State

Two artifacts on `ontology-update` disagree with the CSV:

1. **`CONCEPT_ONTOLOGY.md:56`** places HB1 under `Ultrashort` sub-type. **`table.csv` row 04** has `Laser Approach = Fast ignition`, which the chart generator's `_LASER_SUBTYPE` mapping (`generate_ontology_chart.py:211-214`) routes to `Fast-ig.`. The MD is stale because `generate_ontology_md.py:18` fails with `ImportError: cannot import name 'TREE_PATH'` and nobody has regenerated it.
2. **`CONCEPT_ONTOLOGY.md:14-15, 30-69`** defines typed vocabularies for `Heating Type` (P8) and `Driver Type` (P9) and populates per-concept values. **`table.csv`** has only legacy free-text `Primary Heating` and `Driver Technology` columns — Mallory's P8/P9 prescribed CSV additions were never executed. Downstream typed consumers (`taxonomy_models.py`, `seed_registry.py`, `column_map.py`, the §W5 cost-wiring opportunity) cannot read what does not exist.

### Desired Outcome

Both contradictions resolved with recorded rationale. CSV-as-source-of-truth invariant restored. Migration mergeable to `main`.

---

## Scope

### In Scope

- **Q1**: fix `generate_ontology_md.py` import; regenerate `CONCEPT_ONTOLOGY.md` and `concept_ontology_v3.png`; commit both. CSV unchanged.
- **Q2**: add `Heating Type` and `Driver Type` columns to `exploration/concept_analysis/table.csv` and `exploration/phase_1a/table.csv`, populated from `CONCEPT_ONTOLOGY.md:30-69` with ID translation per `ID_MAPPING.md`. Add `HeatingType` and `DriverType` enums to `taxonomy_models.py`. Update `seed_registry.py::_parse_row` and `similarity.py::SIMILARITY_DIMENSIONS`. Add new entries to `phase_2a/column_map.py` `DESIGN_COLUMNS` / `VOCABULARY` / `KEY_TO_COLUMN`.
- **ADR-001** in `exploration/phase_1a/` recording both decisions.
- **Round-trip check**: regenerated MD matches the committed version on typed columns (after Q2 lands); divergences reconciled.
- **PR + merge** to `main`.

### Out of Scope

- Rerunning scoring (Item 3).
- Refreshing per-concept synthesis prose (Item 5).
- Removing legacy `Primary Heating` / `Driver Technology` columns.
- Reconciling `column_map.py::TABLE_PATH` pointing at `phase_1b_v2/table_v2.csv` (Item 3).
- Refactoring `generate_ontology_chart.py` beyond the typo-class import fix in the MD generator.
- BACKLOG cleanup (Item 6).

### Edge Cases & Considerations

- **Generator round-trip mismatch.** If regenerated MD diverges from the committed one beyond the expected Q1 (`Ultrashort → Fast-ig.` for HB1) and Q2 (typed columns), each divergence is information — either a hidden hand-edit in the committed MD or a latent generator bug. Reconcile before merge.
- **Heating-type combinations** (`ICRH + NBI`, etc.) don't fit a single `StrEnum` value cleanly. Design stage picks the field shape (raw string + parsed list vs other).
- **ID translation gotcha.** `CONCEPT_ONTOLOGY.md` uses Mallory's IDs; our CSV uses ours. The 27/28/29/30/37/38/39 region is where the renumbering bites. Apply `ID_MAPPING.md` when copying values across.
- **40th-row case.** Our CSV has 40 rows; v3 MD has 39 (Pranos dropped). The orphan `20-modular-hts-stellarator` needs `Heating Type` / `Driver Type` values from its lineage (Type One / Renaissance) or `TBD` with an ADR note.
- **Item 3 overlap on `column_map.py`.** If Item 3 has not landed when this work starts, rebase. Predictable conflict, small surface.

---

## Requirement Selection Notes

Each settled question gets one normative requirement plus a third for the decision record and a fourth for the merge gate. Implementation choices (commit decomposition, exactly how to encode combinations, generator-internal cleanups) are deferred to design and plan.

---

## Requirements

### Functional Requirements

> All requirements derived from the research at `.project/research/20260517-212537_ontology-v3-item4-open-questions.md`, reviewed by the user before this spec.

1. **FR-1 (Q1)**: HB11's `Laser Approach` MUST remain `Fast ignition` in `table.csv`. `CONCEPT_ONTOLOGY.md` and `concept_ontology_v3.png` MUST place HB1 under `Fast-ig.` sub-type alongside FOC. This MUST result from running `generate_ontology_md.py` and `generate_ontology_chart.py` against the current CSV — no hand edits to generated artifacts.
2. **FR-2 (Q2)**: Both `table.csv` files MUST include typed `Heating Type` and `Driver Type` columns with values matching `CONCEPT_ONTOLOGY.md:30-69` (after ID translation). `taxonomy_models.py`, `seed_registry.py`, `similarity.py`, and `phase_2a/column_map.py` MUST be updated to parse and validate the new typed columns.
3. **FR-3 (decision record)**: `exploration/phase_1a/ADR-001_csv-source-of-truth.md` MUST exist recording (a) the `Fast-ig.` vs `Ultrashort` rule with rationale, (b) the CSV-as-source-of-truth decision with rationale, (c) Mallory's response on Q1 if she provides one.
4. **FR-4 (merge)**: A PR from `ontology-update` to `main` MUST land containing FR-1/2/3 changes plus Item 3's outputs. The PR MUST NOT merge while `table.csv` and `CONCEPT_ONTOLOGY.md` disagree on any typed column.

### Non-Functional Requirements

- **Traceability**: every value added to `Heating Type` / `Driver Type` MUST trace to its source row in `CONCEPT_ONTOLOGY.md`. No new research; no values invented during migration.

---

## Acceptance Criteria

### Core Functionality

- [ ] `table.csv` row 04 unchanged: `Laser Approach = Fast ignition`.
- [ ] `uv run python exploration/phase_1a/generate_ontology_md.py` succeeds; regenerated `CONCEPT_ONTOLOGY.md` shows HB1 under `Fast-ig.`.
- [ ] `uv run python exploration/phase_1a/generate_ontology_chart.py` succeeds; PNG shows HB1 under `Fast-ig.` alongside FOC.
- [ ] Both `table.csv` files have `Heating Type` and `Driver Type` columns populated for all 40 rows.
- [ ] `taxonomy_models.py` defines `HeatingType` and `DriverType` enums per P8/P9 vocabularies.
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` succeeds; `concept_registry.json` carries the new typed values for every concept.
- [ ] `phase_2a/column_map.py` `DESIGN_COLUMNS` / `VOCABULARY` / `KEY_TO_COLUMN` include the new columns.
- [ ] `similarity.py::SIMILARITY_DIMENSIONS` includes `heating_type` in `plasma_physics` and `driver_type` in `engineering` (per P8/P9 affected-files).
- [ ] `exploration/phase_1a/ADR-001_csv-source-of-truth.md` exists with the three required content elements.
- [ ] Round-trip: regenerated MD matches committed MD on typed columns; divergences reconciled.

### Quality & Integration

- [ ] `uv run python -m pytest exploration/concept_explorer/tests/` passes (regression check; overlaps Item 3).
- [ ] No new `UNMAPPABLE` warnings from `phase_2a/column_map.py` against `table.csv`.
- [ ] PR from `ontology-update` to `main` merged; `git status` clean on `main`.

---

## Next-Stage Handoff

**Settled:**

- HB11 CSV value stays `Fast ignition`; Q1 fix is regenerating MD/PNG, not changing CSV or grouping logic.
- CSV is the source of truth; MD is a generated artifact. `Heating Type` / `Driver Type` added as typed CSV columns (option (a)).
- Legacy `Primary Heating` / `Driver Technology` retained as free-text supplements.
- ADR-001 captures both decisions.
- PR `ontology-update` → `main`.

**Design must figure out:**

- Field shape for heating combinations (`ICRH + NBI`) — raw string + parser vs list field vs other.
- Exact patch to `generate_ontology_md.py:18` — replace `TREE_PATH` with `derive_tree_path` (if used downstream) vs remove the unused import.
- Commit decomposition for the PR.

**Watch-outs:**

- ID translation when copying values from `CONCEPT_ONTOLOGY.md` to our CSV (use `ID_MAPPING.md`); 27/28/29/30/37/38/39 region.
- 40th-row case (`20-modular-hts-stellarator` orphan) — values from lineage or `TBD` with ADR note.
- `column_map.py` also touched by Item 3 — rebase if needed.
- Regenerating MD may expose hand-edits beyond Q1/Q2 — reconcile each, don't paper over.

---

## Related Artifacts

- **Research:** `.project/research/20260517-212537_ontology-v3-item4-open-questions.md`
- **Design:** `design.md` (drafted)
- **Epic:** `.project/backlog/epic_ontology_v3_migration.md` Item 4
- **Prior work items:** `.project/active/ontology-v3-merge/`, `.project/active/ontology-v3-close-gaps/`
- **Source-of-truth references:**
  - `exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md` — P8, P9 proposals
  - `exploration/phase_1a/CONCEPT_ONTOLOGY.md` — v3 vocabulary + per-concept values
  - `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md` — Mallory's proposal record
  - `exploration/phase_1a/ID_MAPPING.md` — Mallory IDs ↔ ours
  - `knowledge/concept_research/04-laser-icf/dossier.md` — HB11 evidence chain

---

**Next Steps:** `/_my_plan` (design already drafted).
