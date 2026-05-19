# Ontology v3 — ID Mapping (Mallory ↔ Ours)

This document reconciles the concept-ID scheme used in the v3 ontology docs
(authored on `origin/fix/concept-renumbering-robustness` by Mallory Snowden)
with the IDs in this repository. We adopted the v3 schema, concepts, and
classification code **without** adopting Mallory's renumbering — our existing
IDs survive unchanged so the directory tree under `analyses/` and
`knowledge/concept_research/` does not have to move.

The other v3 docs in this directory (`CONCEPT_ONTOLOGY.md`,
`RECLASSIFIED_CONCEPTS.md`, `CONCEPT_CATEGORIES_PROPOSAL.md`,
`SCHEMA_REVISION_PROPOSALS.md`, `concept_ontology_v3.png`) reference Mallory's
IDs verbatim. Use the table below to map them onto ours when reading.

## 1. ID Translation Table

The 16 concepts whose IDs differ between Mallory's branch and ours:

| Mallory's ID | Our ID                                   | Concept (Company)                          |
| ------------ | ---------------------------------------- | ------------------------------------------ |
| 17           | 17b-laser-icf-fast-ignition              | Laser ICF — Fast Ignition (Focused Energy) |
| 20           | 20a-type-one-stellarator                 | QI Modular HTS Stellarator (Type One)      |
| 21           | 20b-renaissance-stellarator              | Compact Liquid-Wall Stellarator (Renaissance) |
| 22           | 21-spherical-tokamak-hts                 | Spherical Tokamak — HTS (Tokamak Energy)   |
| 23           | 22-projectile-icf                        | Projectile ICF (First Light Fusion)        |
| 24           | 23-laser-icf-nanostructured-target       | Nanostructured Target (Marvel Fusion)      |
| 25           | 24-dense-plasma-focus                    | Dense Plasma Focus (LPPFusion)             |
| 26           | 25-heavy-ion-beam-icf                    | Heavy Ion Beam ICF (Intensity Energy)      |
| 27           | 17a-laser-icf-hybrid-drive               | Laser ICF — Hybrid Direct Drive (Xcimer)   |
| 28           | 27-polywell                              | Polywell (EMC2)                            |
| 29           | 28-hts-tokamak-full-hts                  | Full-HTS Tokamak (Energy Singularity)      |
| 30           | 29-negative-triangularity-tokamak        | NT Tokamak (Firefly Fusion)                |
| 31           | **26 + 30** (fan-out)                    | Laser ICF — Indirect Drive (Inertia) — Mallory deduplicated; we kept both |
| 32           | 31-laser-icf-oec-architecture            | OEC Architecture (Blue Laser Fusion)       |
| 33           | 32-laser-icf-french-national             | French National Direct Drive (GenF)        |
| 34           | 33-state-backed-tokamak-best             | BEST (Neo Fusion)                          |

IDs that are unchanged between Mallory and us:
01–16, 18, 19, 35, 36, 37 (NearStar), 38 (SHINE), 39 (ENN).

Concepts dropped from the CSV in v3 adoption:
- **Pranos Fusion** (our `34-compact-spherical-tokamak-india`). Already absent
  from Mallory's CSV. Directory under `knowledge/concept_research/` is left in
  place; physical cleanup is deferred to ONTOLOGY-V3 Item 6.

## 2. The 26 + 30 Fan-Out

Mallory's row 31 (Inertia Enterprises) collapses what we represent as two
distinct concepts:
- `26-laser-icf-indirect-drive` — the Thunderwall DPSSL architecture.
- `30-laser-icf-nif-commercialization` — NIF-style commercialization with a
  different driver configuration.

The translator (`translate_csv_to_ours.py`) emits both rows from Mallory's
single row 31. The v3 columns (`Blanket Config`, `Magnet Type`, classification
columns, etc.) are identical on both rows because they come from Mallory's
row 31. The four **identity columns** — `Concept Name`, `Company`, `Driver
Technology`, `Research ID` — come from our existing `table.csv`, so the two
concepts remain distinguishable.

## 3. Orphan Directory

`knowledge/concept_research/20-modular-hts-stellarator/` predates the split
into `20a-type-one-stellarator/` and `20b-renaissance-stellarator/` and
contains unique pre-split research content (verified by `diff` against the
two successor directories). It is **not** referenced by any row of the v3
`table.csv`. Disposition (archive vs. delete) is deferred to ONTOLOGY-V3
Item 6.

## 4. Provenance and Further Reading

- The v3 schema design and column rationale: see `CONCEPT_ONTOLOGY.md` and
  `SCHEMA_REVISION_PROPOSALS.md` in this directory.
- Per-concept reclassification rationale (referencing Mallory's IDs): see
  `RECLASSIFIED_CONCEPTS.md`.
- The translator that produced `table.csv`: `translate_csv_to_ours.py` (in
  this directory). Snapshot input: `_mallory_table.csv`.
- Source branch: `origin/fix/concept-renumbering-robustness` @ `1b960a9`
  (Mallory Snowden, 2026-05-17).
