# Project-Level Tables

Single source of truth for the upstream judgments the concept-analysis pipeline reads at runtime. Schemas are pinned in `.project/completed/20260821_concept-rework-tables/spec.md` (CONCEPT-REWORK Item 5).

All four tables are CSV, UTF-8, one row per concept. `concept_id` is the directory slug under `knowledge/concept_research/` and is the join key across all four.

| File | Method | Verification gate |
|---|---|---|
| `ontology.csv` | Hand-write from enum-map + dossier knowledge | Spot-check each row against `knowledge/concept_research/<id>/` |
| `archetype_fit.csv` | Reshape `.project/research/20260509-1costingfe-enum-map.md` → re-grade Rank 1/2/3 into High/Med/Low/None | Per-row Rank-2 split decision is in `fit_rationale` |
| `comparables.csv` | **Generated** by `scripts/derive_comparables.py` from ontology | Spot-check derivation rule on a handful of rows; do not hand-edit |
| `design_point.csv` | Batch agent proposal from dossier → per-row hand-verification | Sign-off per row in `verified_by` / `verified_date` |

---

## Comparables derivation rule (v1)

Implemented in `scripts/derive_comparables.py`. Reads `ontology.csv` and `archetype_fit.csv`; writes `comparables.csv`. Idempotent — re-running produces an identical file.

**Match tiers** for each target concept:
- **Tier 1**: same subfamily-cluster + same `fuel` + same `driver_class` + same `conversion_path`.
- **Tier 2**: same subfamily-cluster + same `fuel`, allowing `driver_class` and `conversion_path` to differ.

Up to 5 comparables, Tier 1 fills first; within each tier sort ascending by `concept_id` for determinism.

**Subfamily clusters** are mostly singletons (each `confinement_subfamily` is its own cluster). The exception:
- `{tokamak, spherical-tokamak}` — spherical aspect ratio is a geometry-parameter variant within the TOKAMAK enum, not a different cost structure. ARC and a spherical-tokamak both run through the same TOKAMAK enum scaffolding, so they're treated as one cluster for comparability.

**`fit_grade=None` concepts** (02, 16, 35, 38) are excluded from both sides of matching — they don't reach the costingfe pipeline and don't get comparables of their own.

**Concepts with empty comparables** are honest "no comparable concept in corpus" — most are single-of-kind (only maglif, only heavy-ion-ife, only orbitron, ...) or fuel-isolated within their subfamily (DT-mirror 11 has no PB11-mirror neighbor; PB11-spherical-tokamak 39 has no PB11 cluster-mate). Downstream sanity-check flags these with `no_data` per account; not a script error.

**Phase 0 ground-truth row**: `01-hts-compact-tokamak → [21, 28, 29, 33]` — the v1 rule reproduces this exactly. The script self-checks this on every run.

---

## Vocabulary extensions

Two values added to `ontology.csv` vocabularies during population, beyond the spec's initial list:

- **`driver_class = electrostatic-steady-state`** — used for Orbitron (#13) and Polywell (#27). The rotating-electrode / inertial-electrostatic-confinement family is steady-state non-pulsed but the drive is electrostatic, not magnetic. Distinct from `magnetic-steady-state` because comparables matching should not pull magnetic and electrostatic together.
- **`driver_class = mechanical-pulsed`** — used for General Fusion (#14) and MIF Tech (#37). Pneumatic-piston / mechanical liner compression is pulsed but the energy delivery is mechanical (gas pressure), not electrical pulsed-power. Distinct from `pulsed-power` because the cost driver is the compressor system, not the capacitor bank.

---

## Verification gate logs

Recorded as work progresses. See `.project/completed/20260821_concept-rework-tables/gate_log.md`.

| Table | Verified by | Date | Notes |
|---|---|---|---|
| ontology.csv | _pending_ | _pending_ | |
| archetype_fit.csv | _pending_ | _pending_ | Rank-2 splits decided per row; see `fit_rationale` |
| comparables.csv | _pending_ | _pending_ | v1 rule matches Phase 0 ground-truth on concept 01 |
| design_point.csv | _pending_ | _pending_ | Per-row sign-off recorded in `verified_by` / `verified_date` columns |
