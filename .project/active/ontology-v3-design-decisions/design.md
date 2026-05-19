# Design: Ontology v3 — Resolve Design Open Questions

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-17 21:35 PDT
**Branch:** `ontology-update`
**Commit at design time:** `42d04b2`

## Overview

Resolve the two ontology-v3 contradictions blocking the merge to `main`: HB11's `Fast ignition` vs `Ultrashort` placement, and the missing typed `Heating Type` / `Driver Type` CSV columns. Both have the same root cause and admit small, mechanical fixes; the design centers on what the *minimum* fix is, not on inventing new mechanism.

## Related Artifacts

- **Spec:** [spec.md](spec.md)
- **Research:** `.project/research/20260517-212537_ontology-v3-item4-open-questions.md`
- **Epic:** `.project/backlog/epic_ontology_v3_migration.md` Item 4
- **Prior items:** `.project/active/ontology-v3-merge/`, `.project/active/ontology-v3-close-gaps/`

## Research Findings

Investigation found that the spec overstates the work because **the chart generator already encodes the correct rule** and the MD generator is broken:

- `exploration/phase_1a/generate_ontology_chart.py:211-214` already maps `Laser Approach` values to chart sub-types:
  ```python
  _LASER_SUBTYPE = {
      'Fast ignition': 'Fast-ig.',
      'Direct drive fast ignition': 'Fast-ig.',
      'Ultrashort pulse': 'Ultrashort',
      'Liquid jet': 'Ultrashort',
  }
  ```
  CSV row 04 has `Laser Approach = Fast ignition`. Running the chart generator now produces a PNG with HB1 under `Fast-ig.` — Q1 is **already correct on the chart side**.
- `exploration/phase_1a/generate_ontology_md.py:15-21` imports `TREE_PATH` from the chart module, but the chart module exports a function `derive_tree_path` (line 236) — there is no `TREE_PATH` constant. The MD generator fails with `ImportError` on every run. That is why `CONCEPT_ONTOLOGY.md` is stale and disagrees with CSV: nobody has regenerated it on this branch.
- `exploration/phase_1a/generate_ontology_md.py:71-95` already references `r['Heat']`, `r['Driver']`, `r['Heating Type']`, `r['Driver Type']` — the MD generator *expects* the typed columns. The generators are the consumers Q2 needs to feed.
- `exploration/concept_explorer/taxonomy_models.py:78` still exports `PrimaryHeating` (19-value legacy enum); there is no `HeatingType` or `DriverType`. v3 already removed `PlasmaState` / `NeutronManagement` / `TritiumBreeding`.
- `exploration/concept_explorer/seed_registry.py:119-127` parses `Laser Approach`, `Primary Heating`, `Driver Technology` directly from CSV row by column name. Adding new columns to CSV requires adding two new lines here.
- `exploration/concept_explorer/seed_registry.py:131-178` defines `tree_group(c)` — an architecture-driven (no ID-prefix) display-grouping function with a built-in ADR comment. Established pattern for derived groupings; we should not duplicate it.
- `exploration/phase_2a/column_map.py:20` points at `phase_1b_v2/table_v2.csv`, NOT the v3 `exploration/concept_analysis/table.csv`. This is Item 3's scope to reconcile, but Q2's additions to `DESIGN_COLUMNS` must land against whichever path Item 3 settles on.
- The committed `CONCEPT_ONTOLOGY.md` MUST therefore be either hand-edited or generated from an earlier CSV state; the only way to know which is to fix the MD generator and diff its output against the committed file.

## Core Concept

**Both questions reduce to "regenerate or extend, do not redesign."** The chart's `Laser Approach → sub-type` map and the MD generator's column expectations encode the correct v3 schema already. Q1 fix is one missing import in `generate_ontology_md.py` plus a regenerate-and-commit; Q2 fix is two new CSV columns whose values flow through generators that are already coded to read them. The ADR records the decisions so future readers do not re-litigate them, and so the next person who edits the MD knows it is a generated artifact, not a source.

This is the right approach because: (a) the alternatives all add net surface area without solving a real problem (no new grouping rule is required — the chart already has it; no new file format is needed — the CSV already absorbs new columns cleanly); (b) the failure modes are all caught by re-running existing tooling; (c) it preserves Mallory's intent as expressed in `SCHEMA_REVISION_PROPOSALS.md` P8/P9 with no deviation.

## Key Bets & Decisions

- **Bet:** The CSV's `Laser Approach = Fast ignition` for HB11 is correct and authoritative. We do not change it. The chart's existing rule (`'Fast ignition' → 'Fast-ig.'` sub-type) is the rule we adopt; we just need to make sure all generated artifacts reflect it. *Alternative not taken:* changing CSV to `Ultrashort pulse` so the MD's current state "wins." Rejected because it would also force changing the dossier, `RECLASSIFIED_CONCEPTS.md`, and HB11's company-confirmed self-branding.
- **Bet:** `Heating Type` and `Driver Type` go into both `table.csv` files as new columns; legacy `Primary Heating` and `Driver Technology` stay as supplementary free-text. *Alternative not taken:* rename `Primary Heating → Heating Type` and drop `Driver Technology`. Rejected because the free-text columns carry per-concept richness the enums discard (e.g., `Petawatt ps CPA laser + laser-driven kT field` vs `DPSSL Laser`), and we already cited preserving this in the spec.
- **Bet:** The MD generator's `ImportError` is a typo-class bug, not a missing feature. Fix is to import `derive_tree_path` (or remove the unused `TREE_PATH` import) and let the rest of the file work as written. *Alternative not taken:* rewriting `generate_ontology_md.py` to be standalone from the chart module. Rejected as out-of-proportion to the bug.
- **Bet:** The ADR lives in `exploration/phase_1a/ADR-001_csv-source-of-truth.md`, alongside the rest of the v3 design docs. *Alternative not taken:* `.project/research/` or `modeling_project/ARCHITECTURE.md`. Rejected because the decisions are local to the phase_1a ontology infrastructure; centralized architecture records would over-elevate a tactical fix.

## Architecture

The data flow this design preserves:

```
table.csv (source of truth)
   │
   ├──► generate_ontology_chart.py ──► concept_ontology_v3.png
   │       (uses _LASER_SUBTYPE, derive_tree_path)
   │
   ├──► generate_ontology_md.py ──────► CONCEPT_ONTOLOGY.md
   │       (imports derive_tree_path from chart; reads r['Heating Type'], r['Driver Type'])
   │
   ├──► seed_registry.py ────────────► concept_registry.json, decision_tree.json
   │       (parses every CSV column into ConceptTaxonomy + enums)
   │
   ├──► phase_2a/column_map.py ─────► constraint validator
   │       (DESIGN_COLUMNS, KEY_TO_COLUMN, VOCABULARY)
   │
   ├──► concept_explorer/similarity.py ─► similarity scores
   │
   └──► lib/scoring.py ──────────────► verified_scores.json (Item 3 territory)
```

Q1 fixes the second arrow only. Q2 adds two columns to the source and threads them through arrows 3, 4, 5. The chart generator (arrow 1) already reads what it needs; Q2 may produce minor cleanups in chart-internal mappings (`HEAT_MAP`, `DRIVER_BY_CO`) but those are optional consolidations, not requirements.

## Required Invariants

- After this work, **every value in `CONCEPT_ONTOLOGY.md`'s `Heating Type` and `Driver Type` columns must equal the value in the corresponding `table.csv` row**, for all 40 concepts on our IDs. This is testable by diffing the generated MD against the committed one (after the ID-mapping translation).
- The chart generator's `_LASER_SUBTYPE` mapping and the MD generator's `derive_tree_path`-derived sub-type must produce identical sub-type values for every concept. This is structurally guaranteed once both call the same function — but worth asserting in a one-liner test.
- The legacy `Primary Heating` and `Driver Technology` free-text columns must still parse via the existing seed_registry path (we do not delete them); downstream code that reads them must not break.
- `seed_registry.py::tree_group` continues to be the canonical derived-grouping function — no parallel grouping logic introduced.

## Component Overview

- **`exploration/concept_analysis/table.csv`** + **`exploration/phase_1a/table.csv`** — two new columns (`Heating Type`, `Driver Type`) appended after their legacy counterparts; values copied from `CONCEPT_ONTOLOGY.md:30-69` with ID translation via `exploration/phase_1a/ID_MAPPING.md`.
- **`exploration/concept_explorer/taxonomy_models.py`** — two new `StrEnum` classes (`HeatingType`, `DriverType`) per P8/P9 vocabulary tables; two new optional fields on `ConceptTaxonomy`. `PrimaryHeating` enum stays for legacy free-text passthrough.
- **`exploration/concept_explorer/seed_registry.py`** — two new lines in `_parse_row` reading the new columns into the new fields.
- **`exploration/phase_2a/column_map.py`** — two new entries in `DESIGN_COLUMNS`; corresponding `VOCABULARY` / `KEY_TO_COLUMN` additions. Coordinated with Item 3's edit to this file.
- **`exploration/concept_explorer/similarity.py::SIMILARITY_DIMENSIONS`** — add `heating_type` to the existing `plasma_physics` group; add `driver_type` to `engineering` group. Per P8/P9 affected-files lists.
- **`exploration/phase_1a/generate_ontology_md.py`** — fix line 18 import: `TREE_PATH` → `derive_tree_path` (or remove the unused import — investigate which the rest of the file actually uses).
- **`exploration/phase_1a/CONCEPT_ONTOLOGY.md`** — regenerated; committed alongside the CSV changes so the diff is reviewable as one change-set.
- **`exploration/phase_1a/concept_ontology_v3.png`** — regenerated (the generator already produces the correct output; we just commit the current render).
- **`exploration/phase_1a/ADR-001_csv-source-of-truth.md`** — new file (~50 lines): records (a) the `Fast-ig.` vs `Ultrashort` rule with one-paragraph rationale, (b) the CSV-as-source decision with one-paragraph rationale, (c) optional Mallory response if she provides one.

## Non-Goals

- Refactoring `generate_ontology_chart.py` (638 lines) for any reason other than Q1's `TREE_PATH` issue.
- Deleting or deprecating `Primary Heating` / `Driver Technology` columns.
- Reconciling `column_map.py`'s wrong-CSV-path bug — that belongs to Item 3.
- Re-running scoring or synthesis (Item 3 and Item 5).
- Per-concept analysis artifact changes.
- Pacific Fusion row split (P5 — already resolved via P4 magnet vocab collapse).

## Implementation Notes

- **MD generator import fix**: read both `generate_ontology_md.py:15-21` and `generate_ontology_chart.py`'s `derive_tree_path` (line 236) before editing. The chart module currently exports a function, not a constant. Pick the smallest patch that makes the import resolve — likely either replace `TREE_PATH` with `derive_tree_path` in the import (if it is genuinely used downstream) or remove `TREE_PATH` from the import entirely (if `derive_row` already encapsulates the tree path).
- **ID translation gotcha**: `CONCEPT_ONTOLOGY.md` rows use Mallory's IDs; our CSV uses our IDs. Apply `exploration/phase_1a/ID_MAPPING.md` when copying `Heating Type` / `Driver Type` values across. The 27/28/29/30/37/38/39 region is where the renumbering bites; the early IDs (01-25) mostly coincide.
- **40th row case**: our CSV has 40 rows; v3 MD has 39 (Pranos dropped). The orphan (`20-modular-hts-stellarator` per `ID_MAPPING.md`) needs reasonable `Heating Type` / `Driver Type` values — almost certainly inherits from concepts in its lineage (Type One / Renaissance). If unclear, set both to `TBD` and flag in the ADR.
- **column_map.py coordination**: this file is in Item 3's scope. If Item 3 has not landed when this work starts, rebase or apply the addition as a small patch on top of Item 3's branch. The risk is a merge conflict — predictable and recoverable.
- **Round-trip check**: after the CSV edit and the MD generator fix, regenerated `CONCEPT_ONTOLOGY.md` must match the committed (hand-curated?) version on typed columns. Any divergence is information: either CSV is wrong (fix CSV), or the committed MD has hand-edits the generator can't reproduce (back-port the edits to CSV or to the generator). Treat unexplained divergences as bugs and reconcile before merge.
- **ADR template**: short. Use a YAML frontmatter (`status: accepted, date: 2026-05-17, deciders: [Reid W, optionally Mallory]`) + body (Decision Q1, Rationale Q1, Decision Q2, Rationale Q2, Consequences, Open). Keep under ~80 lines.

### Interfaces (~10 lines each)

`taxonomy_models.py` additions:

```python
class HeatingType(StrEnum):
    ICRH = "ICRH"; ECRH = "ECRH"; NBI = "NBI"; OHMIC = "Ohmic"
    # ... combinations like "ECRH + NBI" handled at parse time
    NA_COMPRESSION = "N/A (compression-driven)"
    NA_NONTHERMAL = "N/A (non-thermal)"
    TBD = "TBD"

class DriverType(StrEnum):
    MAGNETIC = "Magnetic"; MAGNETIC_PINCH = "Magnetic pinch"
    DPSSL_LASER = "DPSSL Laser"; GAS_LASER = "Gas Laser"
    ION_BEAM = "Ion/particle beam"; MECHANICAL = "Mechanical/kinetic"
    ELECTROSTATIC = "Electrostatic"; OTHER = "Other"; TBD = "TBD"
```

Combinations (e.g. `ICRH + NBI`) cannot be enum values cleanly — design choice: store as `str` field with validator that splits on `" + "` and checks each part against `HeatingType`. Recommend a `heating_type_raw: str` field plus a `parsed_heating: list[HeatingType]` derived property. Final mechanics to plan.

## Potential Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Regenerated `CONCEPT_ONTOLOGY.md` diverges from committed MD in unexpected ways | Medium | Medium | Round-trip check before merge; reconcile each divergence in the ADR or fix |
| Combinations like `ICRH + NBI` don't fit a single `StrEnum` value cleanly | High | Low | Store raw + parsed; pattern already used elsewhere if you grep for it |
| Item 3 hasn't landed when this work begins; `column_map.py` edits collide | Medium | Low | Rebase; predictable conflict |
| 40th-row (`20-modular-hts-stellarator` orphan) values for new columns are genuinely unknown | Low | Low | Set `TBD`; document in ADR |
| Mallory disagrees with Q1 resolution after PR opens | Low | Medium | Resolution path documented in spec FR-3; ADR captures her response |
| Re-running `generate_ontology_md.py` exposes more hand-edits beyond Q2 columns | Low | Medium | Reconcile each — these are latent bugs, finding them now is value |

## Integration Strategy

This work item is the final gate before `ontology-update` merges to `main`. Item 2 brought in v3 schema + new concepts. Item 3 closes code-side gaps and gets tests passing. Item 4 resolves the remaining design contradictions and merges. Item 5 (synthesis refresh) and Item 6 (BACKLOG cleanup) operate on `main` post-merge.

PR strategy: single PR from `ontology-update` to `main` containing Item 3 outputs + Item 4 outputs. Reviewable as one v3 migration story. Decompose into commits by concern: (1) Q1 generator fix + regenerated MD/PNG, (2) Q2 CSV columns, (3) Q2 enums + parser updates, (4) Q2 column_map + similarity, (5) ADR. Order matters for `git bisect` if anything breaks downstream.

## Validation Approach

- **Existing tests**: `uv run python -m pytest exploration/concept_explorer/tests/` passes. Already required by Item 3; here it's a regression check.
- **Generator round-trip**: `uv run python exploration/phase_1a/generate_ontology_md.py` succeeds and writes a file. Diff against committed MD; every divergence on the typed columns is reconciled.
- **Chart regen**: `uv run python exploration/phase_1a/generate_ontology_chart.py` succeeds and renders 40 concepts with HB1 under `Fast-ig.` and Cortex+Marvel under `Ultrashort`. Visual inspection of `concept_ontology_v3.png`.
- **Registry build**: `uv run python exploration/concept_explorer/seed_registry.py` succeeds; `concept_registry.json` has populated `heating_type` and `driver_type` for every concept; spot-check 3–5 entries against `CONCEPT_ONTOLOGY.md`.
- **Constraint validator**: `uv run python exploration/phase_2a/expand.py` (or current entry point) runs without `UNMAPPABLE` errors for either new column. Smoke-test one concept.
- **Explorer**: optional browser-inspect of taxonomy and compare views; not strictly required for this item since UI changes are Item 3 scope.

## Next-Stage Handoff

**Treat as fixed:**
- CSV stays the source of truth; MD is generated.
- HB11's `Laser Approach = Fast ignition` is correct; generators encode the rule that places HB1 under `Fast-ig.`.
- Two new typed columns + enums; legacy free-text columns retained.
- ADR-001 records both decisions.
- Single PR to `main` with Item 3 + Item 4 outputs.

**Remains open:**
- Whether to keep the import as `derive_tree_path` or refactor differently — implementation detail.
- How exactly to handle heating-type combinations (single string + parser vs. list field) — small design choice for the plan stage.
- Whether `column_map.py::VOCABULARY` for the new types should be auto-derived from enum classes or hand-listed — pick at plan time.
- Optional consolidation of chart-internal `HEAT_MAP` / `DRIVER_BY_CO` to read from the new CSV columns directly. Nice-to-have, not required.

**De-risk first:** Run `generate_ontology_md.py` with the import fix on a scratch CSV with the new columns added for 2-3 representative concepts. Confirm the output matches expectations before committing the full CSV change-set. This is the cheapest way to expose any latent generator bugs.

## Next Steps

After approval → `/_my_plan` to produce a phased execution plan with the commit decomposition listed under Integration Strategy.
