---
status: accepted
date: 2026-05-17
deciders: [Reid W]
---

# ADR-001: CSV is the source of truth for concept ontology; MD/PNG are generated

## Context

During the v3 ontology migration (`ontology-update` branch, epic `ONTOLOGY-V3`,
Item 4) two contradictions surfaced between `exploration/concept_analysis/table.csv`
and `exploration/phase_1a/CONCEPT_ONTOLOGY.md`:

- **Q1.** HB11 Energy's `Laser Approach` is `Fast ignition` in CSV, but the
  committed `CONCEPT_ONTOLOGY.md` placed HB1 under the `Ultrashort` sub-type.
  Origin: `generate_ontology_md.py` failed with
  `ImportError: cannot import name 'TREE_PATH'` on every run since the
  v3 merge, so the committed MD was never regenerated against current CSV.
  The committed copy was authored on `origin/fix/concept-renumbering-robustness`
  (Mallory Snowden's branch) and uses her numeric IDs.
- **Q2.** `CONCEPT_ONTOLOGY.md` defines typed `Heating Type` (P8) and
  `Driver Type` (P9) vocabularies and per-concept values for all 39 concepts.
  `table.csv` had only the legacy free-text `Primary Heating` and
  `Driver Technology` columns — Mallory's P8/P9 CSV additions were never
  applied.

## Decision Q1: CSV is authoritative; `Fast ignition → Fast-ig.`

HB11's `Laser Approach = Fast ignition` in `table.csv` remains unchanged.
The chart generator's `_LASER_SUBTYPE` map
(`generate_ontology_chart.py:211-214`) routes `Fast ignition → Fast-ig.`
sub-type. The MD generator now produces the same routing once its broken
import is fixed.

### Rationale Q1

- HB11 Energy's own technical communications self-brand the approach as
  "fast ignition" with a two-pulse architecture.
- `RECLASSIFIED_CONCEPTS.md` (Mallory's own proposal record) labels HB11
  as `Fast ignition`.
- The dossier (`knowledge/concept_research/04-laser-icf/dossier.md`)
  supports the same.
- Changing CSV to `Ultrashort pulse` would also require editing the dossier,
  `RECLASSIFIED_CONCEPTS.md`, and contradict company self-branding.
- The contradiction is fully explained by the MD being stale, not by a
  classification dispute.

## Decision Q2: Add typed columns to CSV; retain legacy free-text columns

Both `exploration/concept_analysis/table.csv` and `exploration/phase_1a/table.csv`
gain `Heating Type` and `Driver Type` columns inserted after their legacy
free-text counterparts (`Primary Heating` and `Driver Technology`).

The enum vocabularies live in
`exploration/concept_explorer/taxonomy_models.py` (`HeatingType`, `DriverType`).
`Heating Type` is parsed as a raw string + computed atom list to accommodate
combinations like `ICRH + NBI`; `Driver Type` is a single enum value.

Consumers updated: `seed_registry.py` (`_parse_row`),
`similarity.py` (`SIMILARITY_DIMENSIONS`),
`phase_2a/column_map.py` (`DESIGN_COLUMNS`, `VOCABULARY`, `KEY_TO_COLUMN`,
`VALUE_ALIASES`).

### Rationale Q2

- The chart and MD generators *already* expect these columns (the MD
  generator references `r['Heating Type']` / `r['Driver Type']`).
- `SCHEMA_REVISION_PROPOSALS.md` P8/P9 prescribe the additions; the
  generator code was written to match. Only the CSV was missing.
- Legacy `Primary Heating` and `Driver Technology` columns carry richer
  per-concept detail (e.g. `Petawatt ps CPA laser + laser-driven kT field`
  vs typed `DPSSL Laser`); they remain for downstream consumers that
  need that richness.
- Two CSV columns is the smallest delta that wires every downstream
  typed consumer without renaming or deleting anything else.

## Consequences

- The committed `CONCEPT_ONTOLOGY.md` and `concept_ontology_v3.png` are
  now treated as generated artifacts. Any future edit to the ontology
  goes through `table.csv` plus a regeneration pass; the generators must
  remain runnable.
- Many class-(c) divergences surfaced during Phase 1 regen
  (ID format slug-vs-numeric, family reclassifications for TAE/SHINE,
  energy-capture and magnet-type overrides) were all explained as
  "regenerated MD reflects current CSV; committed copy was generated
  against Mallory's pre-merge state with her numeric IDs". Accepted
  as-is; no CSV edits needed.
- The INE×2 code collision in the MD summary tables
  (`26-laser-icf-indirect-drive` and `30-laser-icf-nif-commercialization`
  both render as `INE`) is cosmetic and deferred to ONTOLOGY-V3 Item 5/6.
- `phase_2a/column_map.py::TABLE_PATH` still points at
  `phase_1b_v2/table_v2.csv`. Reconciling that is Item 3's scope, not this
  ADR's.

## Open

- Mallory has not been notified of the Q1 resolution. Courtesy ping is
  optional, not blocking. If a response materializes, append it as an
  appendix to this ADR.
