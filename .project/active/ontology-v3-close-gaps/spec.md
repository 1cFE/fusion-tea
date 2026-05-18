# Spec: Close v3 Code Gaps and Pass Tests

**Status:** ✅ Implemented 2026-05-17 (2 carry-forwards — see end-of-doc note). Revised 2026-05-17 (FR-4, FR-6, FR-8 narrowed to match verified codebase state — see Requirement Selection Notes).
**Owner:** Reid W
**Created:** 2026-05-17
**Complexity:** MEDIUM
**Branch:** ontology-update
**Epic:** ONTOLOGY-V3 (Item 3)

---

## Work Item Summary

The v3 ontology schema, new concept slate, and architecture-driven classification have already landed on `ontology-update` (commit `6d32f4d`). However, several downstream consumers were not touched by the merge and will silently break (or are already broken) against v3: Phase 2a's `column_map.py`, the explorer's decision-tree builder, Jinja templates, one JS module, parameter display registry, taxonomy tests, two ID-prefix-keyed analysis scripts, and the committed `scores/*.json` artifacts that encode the old buggy C2 values. This work item closes those nine gaps, regenerates scores against the architecture-derived classifier, and gets the test suite green so the explorer and Phase 2a pipeline operate cleanly against v3.

## Why This Matters Now

Item 2 of the ontology v3 epic landed the schema change but explicitly deferred per-concept regeneration and downstream adapter updates. Until Item 3 closes, Phase 2a constraint validation emits `UNMAPPABLE` for every dropped column, the explorer's taxonomy view renders the old 4-family tree instead of the v3 sibling groups (Estatic / Other / Cmpt-Tor), templates reference fields that no longer exist on the data, scoring outputs are stale, and the test suite is broken. None of the v3 work is reviewable end-to-end until this gap-close ships.

## Key Bets / Constraints

- **Bet:** Keeping the 4-bucket `ConfinementFamily` enum and encoding the v3 sibling groups as a display-only `tree_group` / `_HIERARCHY` layer minimizes blast radius vs. extending the enum. (Recommendation from epic Risk row 2.)
- **Bet:** The architecture-driven classification pattern (`Confinement Family / MFE Topology / Magnet Type / IFE Driver / MIF Method` + slug overrides) already established in `lib/scoring.py` is the canonical pattern; `oneoff_3d_clustering.py` and `generate_ontology_chart.py` get refactored to match it rather than maintaining parallel ID-prefix maps.
- **Constraint:** No changes to `table.csv` schema, no resolution of the HB11 Fast-ignition-vs-Ultrashort inconsistency, no new `Heating Type` / `Driver Type` columns — those are Item 4's job. This item works against the CSV as committed in `6d32f4d`.
- **Constraint:** No `synthesis.md` refresh and no re-extraction of per-concept JSON beyond what scoring rerun naturally touches — that's Item 5.
- **Non-goal:** Refactoring any code path that already works against v3. Touch only what is broken or stale.

---

## Business Goals

### Why This Matters

The v3 migration is mid-flight: the schema is in but the consumers aren't. Without closing these gaps, no one (including future Claude sessions) can use the explorer, run Phase 2a, or trust the scores. The work blocks merging the migration to `main` (Item 4) and blocks the synthesis refresh (Item 5).

### Success Criteria

- [x] `uv run python -m pytest exploration/concept_explorer/tests/` passes from a clean checkout (176 passed, 2 skipped)
- [~] Explorer tree shape verified at the data/contract layer (`decision_tree.json` root field is `tree_group`; six top-level groups present; server endpoint test passes). Visual `browser-inspect` smoke deferred to Item 5.
- [x] Phase 2a `validate.py --summary` smoke shows zero `UNMAPPABLE` from dropped column names
- [~] `scores/verified_scores.json` regenerated against architecture-derived C2 (35/40 concepts; 5 lack synthesis YAML). `calibrated_scores.json` deferred — `calibrate` Claude call hit time cap.
- [x] `seed_registry.py` → `decision_tree.json` regen → explorer test suite runs without manual fixups

### Priority

P0 — blocks Items 4–6 of the ontology v3 epic. Sequenced strictly after Item 2 (already complete) and before Item 4 (HB11 + CSV-vs-MD decision + PR to `main`).

---

## Problem Statement

### Current State

After `6d32f4d`, the following are known broken or stale against v3:

1. `exploration/phase_2a/column_map.py` — `DESIGN_COLUMNS`, `KEY_TO_COLUMN`, `VOCABULARY`, `VALUE_ALIASES` still reference `Plasma State`, `Tritium Breeding`, `Neutron Management`; no entries for `Blanket Config`.
2. `exploration/concept_explorer/seed_registry.py` — `_HIERARCHY` / `_SUBTYPES` still encode the old MFE/IFE/MIF/Non-Standard tree; v3 sibling groups (Estatic / Other / Cmpt-Tor; Dipole/Supported; MIF/Pulsed power) are absent.
3. `exploration/concept_explorer/templates/{taxonomy,index,concept,compare}.html.j2` — verified clean (grep for the three dropped column names returns zero hits). Templates route field display through Python/JS, not template field names. Action: verify-only.
4. `exploration/concept_explorer/static/js/neighborhood_graph.js` — same field-name rename that `taxonomy_card.js` and `view_categorical.js` already received was not applied here.
5. `exploration/concept_explorer/data/parameter_display_registry.yaml` — verified to contain only numeric sensitivity parameters; `blanket_config` is categorical and out of scope for this registry. No stale entries for the dropped columns. Action: verify-only.
6. `exploration/concept_explorer/tests/test_taxonomy_models.py` — fixtures and assertions reference the old enums/fields; suite likely fails.
7. `exploration/concept_analysis/scripts/oneoff_3d_clustering.py` — `CADENCE_BY_PREFIX` and `FUNDING_M_USD` are keyed off ID prefixes; not refactored to the architecture-driven pattern. Missing entries for ENN, NST, SHI, Xcimer-27.
8. `exploration/phase_1a/generate_ontology_chart.py` — `TREE_PATH` is a hardcoded ID-prefix structure; should derive from the CSV.
9. `scores/verified_scores.{json,md}` and `scores/calibrated_scores.{json,md}` — committed before the classification refactor, encode the old buggy C2 values for the 8 silently miscategorized concepts.

### Desired Outcome

Every gap above is closed; tests pass; a smoke run of the explorer and Phase 2a against one representative concept shows no errors; scores are regenerated and reflect the architecture-derived classifier.

---

## Scope

### In Scope

- The nine gaps enumerated above.
- A short (≤1 paragraph) ADR-style comment in `seed_registry.py` recording the "keep enum, add `tree_group`" decision.
- A `browser-inspect` smoke session capturing the explorer rendering v3 correctly (session JSON saved under `/tmp/browser_inspect/<session>/`).
- Whatever minor follow-ups surface in code review of the nine changes (e.g. orphaned imports analogous to the `FREEFORM_CONCEPTS` cleanup noted in Item 2's carry-forward).

### Out of Scope

- HB11 Fast-ignition-vs-Ultrashort inconsistency (Item 4).
- CSV-vs-MD source-of-truth decision for `Heating Type` / `Driver Type` (Item 4).
- Adding `Heating Type` / `Driver Type` columns to `table.csv` (Item 4).
- Refreshing any `synthesis.md` (Item 5).
- Re-extracting per-concept `concept_explorer/data/{ID}.json` files beyond what scoring rerun naturally produces (Item 5).
- Modifying `taxonomy_models.py` enums (explicitly avoided — `tree_group` is display-only).
- Touching `analyses/` files except where scoring regeneration writes them (FR-14 carryover from Item 2).
- Merging to `main` (Item 4).

### Edge Cases & Considerations

- **Stale-import audit:** Item 2 turned up a dead `FREEFORM_CONCEPTS` import in `run_analysis.py` and a missing `canonical_eta_th` import in `scoring.py`. The gap-close should grep for similar orphans introduced by the renumbering / refactor before declaring done.
- **Decision-tree shape change:** The `_HIERARCHY` rewrite changes the structure of `decision_tree.json`. Any consumer that reads that file with rigid key expectations (explorer JS, possibly tests) may need a matching update.
- **Template defensive rendering:** Some concepts may not have `blanket_config` populated yet. Templates should hide-or-blank, not crash, on missing fields.
- **Scoring rerun cost / non-interactivity:** The scoring driver may assume interactive Claude calls. If non-TTY fails, batch via `claude -p` with the existing `lib/claude.py` harness. Cap at ~$50 budget.
- **ID-prefix references elsewhere:** `oneoff_3d_clustering.py` and `generate_ontology_chart.py` are the named offenders, but there may be others. A grep for `CADENCE_BY_PREFIX`-shaped patterns is part of the design step.

---

## Requirement Selection Notes

Most decisions here are mechanical (rename a field, update a dict). The genuinely normative choices are: (a) keep the enum and add `tree_group` rather than extend `ConfinementFamily`; (b) regenerate scores rather than hand-patching the committed JSON; (c) refactor the *unstable* ID-keyed scripts to the architecture-driven pattern (`CADENCE_BY_PREFIX` is keyed by 2-digit numeric prefix — broken by renumbering — and must be refactored; `FUNDING_M_USD` is keyed by full concept slug, which is stable across renumbering, and is a per-company fact rather than an architecture-derived value, so it may stay slug-keyed). Everything else is implementation detail and belongs in design/plan.

**Revision note (2026-05-17, prior to design):** During design Stage 0 the codebase was audited against the original FR set. Three FRs are amended to match verified reality:
- **FR-4 (Jinja templates):** verified zero stale field-name references; action narrowed to *verify clean*.
- **FR-6 (`parameter_display_registry.yaml`):** verified registry holds only numeric sensitivity parameters; categorical `blanket_config` is out of scope for this file; no stale entries present. Action narrowed to *verify clean*.
- **FR-8 (`oneoff_3d_clustering.py`):** mandate applies to `CADENCE_BY_PREFIX` only (numeric-prefix-keyed, broken by renumbering). `FUNDING_M_USD` is slug-keyed and may stay; its keys are checked for currency vs `table.csv` instead.

---

## Requirements

### Functional Requirements

1. **FR-1**: `phase_2a/column_map.py` MUST be updated so `DESIGN_COLUMNS`, `KEY_TO_COLUMN`, `VOCABULARY`, and `VALUE_ALIASES` reflect the v3 CSV header — entries for `Plasma State`, `Tritium Breeding`, and `Neutron Management` removed; `Blanket Config` mappings added.
2. **FR-2**: `seed_registry.py::_HIERARCHY` and `_SUBTYPES` MUST encode the v3 tree (Estatic, Other, Cmpt-Tor as top-level siblings; Dipole/Supported and MIF/Pulsed power as new leaves). The generated `decision_tree.json` MUST reflect this.
3. **FR-3**: A short ADR-style comment in `seed_registry.py` MUST record the decision to keep the existing `ConfinementFamily` enum and introduce a display-only `tree_group` rather than extend the enum.
4. **FR-4 (revised)**: The four Jinja templates (`taxonomy.html.j2`, `index.html.j2`, `concept.html.j2`, `compare.html.j2`) MUST be verified clean of references to `tritium_breeding` / `neutron_management` / `plasma_state` via grep. (Verified zero hits at design time; this FR is a no-regression check, not an edit.)
5. **FR-5**: `neighborhood_graph.js` MUST receive the same field-name rename already applied to `taxonomy_card.js` and `view_categorical.js`.
6. **FR-6 (revised)**: `parameter_display_registry.yaml` MUST be verified to contain no stale entries for `plasma_state` / `tritium_breeding` / `neutron_management`. (Verified zero hits at design time; `blanket_config` is categorical and out of registry scope — the registry holds only numeric sensitivity parameters.)
7. **FR-7**: `tests/test_taxonomy_models.py` MUST be updated so fixtures and assertions match v3; `BlanketConfig` MUST gain coverage equivalent to what the dropped columns had.
8. **FR-8 (revised)**: `oneoff_3d_clustering.py::CADENCE_BY_PREFIX` MUST be refactored to derive from architecture columns (`Confinement Family`, `MFE Topology`, `Magnet Type`, `IFE Driver`, `MIF Method`) plus slug overrides — mirroring the `lib/scoring.py::detect_c2_category` pattern. `FUNDING_M_USD` MAY remain slug-keyed (slugs are stable across renumbering; funding is per-company, not architecture-derived), but its keys MUST be audited against `table.csv` — entries for ENN (39), NearStar (37), SHINE (38), and Xcimer renumber (now `17a-laser-icf-hybrid-drive`) MUST be added; the entry for Pranos (`34-compact-spherical-tokamak-india`) MAY be left in place (drop deferred to Item 6) or removed.
9. **FR-9**: `generate_ontology_chart.py::TREE_PATH` MUST derive from `table.csv` rather than hardcoded ID prefixes.
10. **FR-10**: The scoring pipeline MUST be rerun and `scores/verified_scores.{json,md}` and `scores/calibrated_scores.{json,md}` MUST be regenerated against the architecture-derived classifier.
11. **FR-11**: `uv run python -m pytest exploration/concept_explorer/tests/` MUST pass.
12. **FR-12**: A `browser-inspect` smoke session MUST verify the explorer renders the v3 tree, the compare view works, and no console errors appear on a concept whose old field is absent. Session JSON MUST be saved under `/tmp/browser_inspect/<session>/`.
13. **FR-13**: Before declaring done, a grep MUST be performed for orphaned references to the dropped columns and to the old ID-prefix maps; any hits MUST be resolved or explicitly logged as out-of-scope follow-ups.
14. **FR-14**: `oneoff_3d_clustering.py` and `generate_ontology_chart.py` MUST produce identical output for unchanged concepts after the architecture-driven refactor (regression check).

### Non-Functional Requirements

- **NFR-1**: All work commits SHOULD be small, reviewable, and grouped by gap (one logical commit per FR where practical) so the review can track against the 9-item gap list.
- **NFR-2**: Scoring rerun SHOULD stay under ~$50 LLM budget. (Expected actual cost ≈ $0.50 — see design Bet 3: `extract-scores` is deterministic Python; `calibrate` is a single cross-concept Claude call, not per-concept. The $50 cap is a safety margin for the unlikely case that `calibrate` retries or `extract-scores` surfaces synthesis-YAML gaps that force a `synthesize` rerun for a few concepts.)

---

## Acceptance Criteria

### Core Functionality

- [x] `phase_2a/column_map.py` aligns with the v3 CSV header (FR-1) — `ac320a4`
- [x] `seed_registry.py` generates a v3-shaped `decision_tree.json` reflecting the new top-level groups (FR-2) — `f3f40c9`
- [x] ADR comment present in `seed_registry.py` documenting the enum-vs-`tree_group` decision (FR-3) — `f3f40c9`
- [x] Jinja templates verified clean of stale field-name references (FR-4 — verify-only)
- [x] `neighborhood_graph.js` field-rename matches `taxonomy_card.js` / `view_categorical.js` (FR-5) — `f3f40c9`
- [x] `parameter_display_registry.yaml` verified clean of stale entries (FR-6 — verify-only)
- [x] `test_taxonomy_models.py` updated; includes `BlanketConfig` coverage (FR-7) — `f3f40c9`
- [x] `oneoff_3d_clustering.py::CADENCE_BY_PREFIX` refactored to architecture-driven keys; `FUNDING_M_USD` keys audited and missing-concept entries added (FR-8 revised) — `42d04b2`
- [x] `generate_ontology_chart.py` derives `TREE_PATH` from the CSV (FR-9) — `42d04b2`
- [~] Scores regenerated and committed (FR-10) — `verified_scores.{json,md}` regenerated (`029b3ab`); `calibrated_scores.*` deferred — see carry-forward note in epic Item 3.

### Quality & Integration

- [x] `uv run python -m pytest exploration/concept_explorer/tests/` passes (FR-11) — 176 passed, 2 skipped
- [x] Phase 2a smoke (`validate.py --summary`): zero `UNMAPPABLE` from dropped column names
- [ ] `browser-inspect` smoke session saved; explorer renders v3 tree; zero console errors (FR-12) — **deferred to Item 5 / pre-PR for Item 4**
- [x] Stale-reference grep complete; no surprises (FR-13) — remaining hits are intentional v3-transition comments or out-of-scope historical `phase_1b/1d` files
- [x] `oneoff_3d_clustering.py` byte-identical for unchanged concepts; `generate_ontology_chart.py` regenerated with new family-color for `Cmpt-Tor` (FR-14)
- [x] No edits to `table.csv` schema, `taxonomy_models.py` enums, `synthesis.md`, or `analyses/` files outside scoring outputs

---

## Next-Stage Handoff

**Settled in this spec:**
- Scope is the nine gaps in `.project/research/20260517_ontology_v3_delta.md` §Addendum, plus stale-import audit and explorer smoke test.
- `ConfinementFamily` enum stays as-is; v3 sibling groups become a display-only `tree_group` layer.
- `oneoff_3d_clustering.py` and `generate_ontology_chart.py` get the full architecture-driven refactor, not a patch.
- Scoring artifacts get regenerated, not hand-patched.
- HB11, CSV-vs-MD, synthesis refresh, and merge-to-`main` are not in scope.

**Design must figure out:**
- The exact shape of the `_HIERARCHY` / `_SUBTYPES` structures that produce the v3 `decision_tree.json` — specifically how to represent sibling groups without enum changes, and whether the explorer JS consumers need any contract updates to consume the new shape.
- Whether to introduce a small shared helper for the "architecture columns → classification key" mapping used by `scoring.py`, `concepts.py`, `oneoff_3d_clustering.py`, and `generate_ontology_chart.py`, or to inline the logic per script.
- Whether the scoring rerun is driven by `rerun_all_models.py` (pulled-in from Mallory's branch) or a new entry point, and how to make it run non-interactively.
- Commit grouping strategy (one PR with 9 commits vs. multiple smaller PRs).

**Watch-outs for design:**
- Templates and JS must defend against missing `blanket_config` on older concept JSON until Item 5 refreshes them.
- The `decision_tree.json` shape change may break tests that hard-assert key paths — update tests in lockstep, not after the fact.
- Scoring rerun touches `analyses/{ID}/scoring/*` style files for many concepts; confirm this is what we want before committing the regeneration (FR-14 from Item 2 forbade `analyses/` edits; scores are an explicit allowance here, but the design should articulate the boundary).
- The stale-import audit (FR-13) is easy to defer and easy to forget — design should bake it in as an explicit plan phase, not a wrap-up step.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_ontology_v3_migration.md` (Item 3)
- **Research:** `.project/research/20260517_ontology_v3_delta.md` (§Addendum lists the nine gaps verbatim)
- **Prior work item:** `.project/active/ontology-v3-merge/` (Item 2, complete)
- **Design:** `.project/active/ontology-v3-close-gaps/design.md` (to be created)
- **Plan:** `.project/active/ontology-v3-close-gaps/plan.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_design`.
