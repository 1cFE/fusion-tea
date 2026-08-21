# Epic: Ontology v3 Migration

> **Archived 2026-08-21** — Complete (Items 1–4; Item 5 superseded by the rework regeneration, Item 6 discharged by this cleanup). Status audit: `.project/reports/2026-08-21-1339-status-report.md`.

**Epic ID**: ONTOLOGY-V3
**Status**: In Progress (Items 1–3 complete 2026-05-17; Item 3 has two carry-forwards — see Item 3 notes)
**Priority**: P0
**Created**: 2026-05-17
**Estimated Effort**: 5–8 days across three branches

---

## Executive Summary

Migrate the project from the v0.2.x concept ontology to v0.3.0: drop `Plasma State` / `Tritium Breeding` / `Neutron Management`, add consolidated `Blanket Config`, renumber the concept slate (4 new concepts, 1 dropped, several IDs shifted/deduplicated), and adopt the architecture-driven (not ID-keyed) classification pattern. Most of the implementation already exists on `origin/fix/concept-renumbering-robustness`; this epic merges it in, closes the known gaps, and reruns dependent artifacts.

**Critical Success Factor**: All downstream consumers (concept explorer, phase_2a validator, scoring pipeline, synthesis prose) operate against the v3 schema with no stale references to the dropped columns or pre-renumbering IDs, and the test suite passes.

---

## Why This Epic?

**Current State**:
- `consistency-checks` branch contains in-flight availability/η_th standardization edits across ~20 concept files (uncommitted), pinning the codebase to the v0.2.x schema.
- `origin/fix/concept-renumbering-robustness` (single commit `1b960a9`, Mallory) implements the v3 schema migration + renumbering + pipeline rerun for all 38→39 concepts, but is divergent from `main` and has known gaps (column_map, decision-tree hierarchy, Jinja templates, tests, stale scores, CSV-vs-doc inconsistency on HB11).
- `phase_2a/column_map.py` still references the dropped columns — Phase 2a will break the moment v3 lands.
- `_C2_CONCEPT_MAP` and `FREEFORM_CONCEPTS` were keyed by numeric ID prefix; the renumbering silently miscategorized 8 concepts. Already fixed on the branch but the refactor pattern needs preserving going forward.
- `scores/verified_scores.{json,md}` and `scores/calibrated_scores.{json,md}` were generated before the classification refactor and encode the old buggy C2 values.
- Several `synthesis.md` files (P2 BACKLOG item) cite pre-standardization availability/LCOE numbers and will fall further out of date once the v3 reclassifications propagate.

**Future State**:
- Single v3 schema in `table.csv` with `Blanket Config` and the new concept slate.
- `ConfinementFamily` enum and `_HIERARCHY`/`_SUBTYPES` in `seed_registry.py` reflect the v3 tree (Estatic, Other, Cmpt-Tor as siblings; Dipole/Supported; MIF/Pulsed power).
- All classification lookups derive from architecture columns, not ID prefixes — codified as a project convention.
- Phase 2a validator, explorer UI, parameter display registry, and tests all pass.
- Scores regenerated against the new classification; synthesis prose refreshed for affected concepts.
- Detailed delta report and codebase trace preserved at `.project/research/20260517_ontology_v3_delta.md`.

---

## Success Criteria

- [ ] `consistency-checks` branch merged to `main` (Item 1)
- [x] `fix/concept-renumbering-robustness` content adopted via cherry-pick-by-file onto `ontology-update` (Item 2 ✅ 2026-05-17; code-side gaps from Item 3 still pending)
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` generates a v3-shaped `decision_tree.json` reflecting the new top-level groups
- [ ] `uv run python exploration/concept_explorer/extract_explorer_data.py` runs clean against the renumbered slate
- [ ] `uv run python -m pytest exploration/concept_explorer/tests/` passes
- [ ] `phase_2a/column_map.py::DESIGN_COLUMNS` aligns with the v3 CSV header; constraint validation runs without `UNMAPPABLE` errors from removed columns
- [ ] Scores regenerated; `verified_scores.json` and `calibrated_scores.json` reflect architecture-derived C2 values
- [ ] HB11 classification inconsistency (CSV `Fast ignition` vs ontology MD `Ultrashort`) resolved one way or the other, with a written rationale
- [ ] Decision recorded on CSV-vs-MD source-of-truth for the new `Heating Type` / `Driver Type` columns (Item 4)
- [ ] Stale `synthesis.md` files refreshed for the 13 availability-affected concepts and any concept whose v3 classification changed (Item 5)
- [ ] BACKLOG.md cleanup items (Items 5–6 below) closed or explicitly carried forward
- [ ] Feedback memory added: "ID-prefix lookups are a known footgun — derive classification from architecture columns + slug overrides"

---

## Backlog Items

### Item 1: Land `consistency-checks` on `main` ✅ Complete (2026-05-17)

**Type**: Code/Integration
**Effort**: 0.5 day (review 1h, fixups 1h, PR 1h, merge 1h)
**Dependencies**: None
**Merged**: PR #15 → `main` as `a8a779e`

**Objective**: Get the current in-flight availability/η_th standardization work merged to `main` so the v3 migration starts from a stable baseline.

**Scope**:
1. Review the ~20 modified files on `consistency-checks` (mostly `model_setup.py` / `analysis.md` / `synthesis.md` / `model_output.txt` updates from the standardization scripts).
2. Stage, commit, and push.
3. Open PR; resolve any review comments.
4. Squash-merge to `main`.
5. Verify `main` builds and that `uv run python exploration/concept_explorer/extract_explorer_data.py` still works against the v0.2.x schema (one last time).

**Out of Scope**:
- Any v3 schema changes.
- Touching `table.csv`.

**Success Criteria**:
- [x] `consistency-checks` branch merged to `main` (PR #15, `a8a779e`)
- [x] CI / smoke commands green on `main`
- [ ] No uncommitted edits remain in the working tree — `uv.lock` diff still pending review

**Deliverables**:
- Merged PR
- Clean `git status` on `main`

---

### Item 2: Merge ontology v3 branch (mechanical merge + immediate breakage fix) ✅ Complete (2026-05-17)

**Outcome**: Adopted v3 schema, new concepts (37/38/39), and architecture-driven classification from `origin/fix/concept-renumbering-robustness` (1b960a9) by cherry-pick-by-file onto `ontology-update`. Kept our existing concept IDs — no directory renames. Single commit `8db3ed2` after planning commit `244ca24`. See `.project/active/ontology-v3-merge/{spec,design,plan}.md` and `exploration/phase_1a/ID_MAPPING.md` for the renumber map and 26/30 fan-out rationale.

**Strategy revision vs. original spec**: We did NOT merge or adopt Mallory's renumbering. Instead we adopted only her schema + code + new concepts, translating her CSV onto our IDs via `exploration/phase_1a/translate_csv_to_ours.py`. Pranos dropped from CSV (directory left in place — Item 6). `20-modular-hts-stellarator/` orphan documented in ID_MAPPING.md, deferred to Item 6.

**Success criteria verification**:
- [x] Single commit landed on `ontology-update` (`8db3ed2` after `244ca24`). Note: not `ontology-v3-migration` per original plan — branch was renamed during planning.
- [x] `table.csv` has 40 rows (37 retained + 3 new), v3 columns, `Research ID` = our slug for every row.
- [x] `seed_registry.py` succeeds; `concept_registry.json` has 40 entries.
- [x] η_th values from Item 1 preserved (no `analyses/` files touched in this commit — FR-14).
- [x] No references to old IDs in tracked files (we kept our IDs; Mallory's IDs only appear in pulled-verbatim v3 docs, intentionally — ID_MAPPING.md compensates).
- [ ] `extract_explorer_data.py` clean run: **deferred to Item 5** (per-concept `{ID}.json` regeneration was explicitly out of scope).

**Carry-forward items uncovered during execution** (folded into the right downstream items):
- `run_analysis.py` had a dead `FREEFORM_CONCEPTS` import — fixed in this commit (1 line). Mentioned because Item 3 should audit for similar orphaned references.
- `scoring.py` initially shipped without the `canonical_eta_th` import after stripping the inline definition. Caught in review; amended into `8db3ed2`. Lesson logged: Phase gates need behavioral smoke that reaches the function, not just module-load.

---

### Item 3: Close v3 code gaps and pass tests

**Status**: ✅ Complete 2026-05-17 (with 2 carry-forwards to Item 5 — see below)
**Type**: Implementation
**Effort**: 1.5 days (spec 1h, design 2h, plan 1h, execute 8h)
**Dependencies**: Item 2
**Artifacts**: `.project/active/ontology-v3-close-gaps/{spec,design,plan}.md`
**Commits on `ontology-update`**:
- `ac320a4` Phase 1: `column_map.py` v3 schema (FR-1)
- `f3f40c9` Phase 2: `tree_group` display layer + v3 test sweep (FR-2/3/5/7/11)
- `42d04b2` Phase 3: architecture-driven `cadence_by_architecture` + `derive_tree_path` (FR-8/9/14)
- `029b3ab` Phase 4: `verified_scores` regen against v3 classifier (FR-10 partial)

**Objective**: Close the 9 gaps identified in `.project/research/20260517_ontology_v3_delta.md` §Addendum that the branch did not address, then get the test suite green.

**Scope**:
1. **`exploration/phase_2a/column_map.py`** — update `DESIGN_COLUMNS`, `KEY_TO_COLUMN`, `VOCABULARY`, `VALUE_ALIASES`: drop entries for `Plasma State` / `Tritium Breeding` / `Neutron Management`; add `Blanket Config` mappings.
2. **`exploration/concept_explorer/seed_registry.py`** — extend `_HIERARCHY` and `_SUBTYPES` to encode the v3 tree (Estatic, Other, Cmpt-Tor as top-level siblings; Dipole/Supported, MIF/Pulsed power as new leaves). Decide whether to extend `ConfinementFamily` enum or stay with the 4-bucket enum + a separate `tree_group` field — record the choice in a short ADR comment.
3. **`exploration/concept_explorer/templates/{taxonomy,index,concept,compare}.html.j2`** — rename `tritium_breeding`/`neutron_management`/`plasma_state` references to `blanket_config`; hide dropped fields gracefully.
4. **`exploration/concept_explorer/static/js/neighborhood_graph.js`** — same field-name rename as `taxonomy_card.js` / `view_categorical.js` already received.
5. **`exploration/concept_explorer/data/parameter_display_registry.yaml`** — add `blanket_config` entry; remove the three dropped entries.
6. **`exploration/concept_explorer/tests/test_taxonomy_models.py`** — update fixtures and assertions for the new enums; add tests for `BlanketConfig`.
7. **`exploration/concept_analysis/scripts/oneoff_3d_clustering.py`** — refactor `CADENCE_BY_PREFIX` and `FUNDING_M_USD` to key off `Confinement Family / MFE Topology / Magnet Type` (mirroring the `scoring.py` / `concepts.py` pattern); add ENN, NST, SHI, Xcimer-27 entries to whatever residual ID-keyed maps remain.
8. **`exploration/phase_1a/generate_ontology_chart.py`** — refactor `TREE_PATH` to derive from the CSV instead of hardcoded ID prefixes (called out by Mallory as known follow-up).
9. **Rerun scoring** — execute the scoring pipeline so `scores/verified_scores.{json,md}` and `scores/calibrated_scores.{json,md}` reflect architecture-derived C2 (the branch's committed scores are known-stale).
10. **Smoke-test the explorer** via the `browser-inspect` skill: taxonomy view renders v3 tree, compare view works, no console errors when a concept's old field is absent.

**Out of Scope**:
- Source-of-truth decision for new `Heating Type` / `Driver Type` columns (Item 4).
- HB11 classification fix (Item 4).
- Refreshing synthesis prose (Item 5).

**Success Criteria**:
- [x] `uv run python -m pytest exploration/concept_explorer/tests/` passes (176 passed, 2 skipped)
- [x] `phase_2a/validate.py --summary` runs without `UNMAPPABLE` from dropped column names
- [x] Explorer renders v3 tree groupings (`decision_tree.json` root field `tree_group`; six top-level keys MFE/IFE/MIF/Cmpt-Tor/Estatic/Other)
- [x] `decision_tree.json` reflects the new sibling structure
- [x] `oneoff_3d_clustering.py`: feature values byte-identical to baseline for retained concepts; KMeans cluster labels shift only because new concepts (37/38/39) join the dataset
- [x] `generate_ontology_chart.py`: renders 40 concepts; pre-existing crash on missing family color also fixed
- [ ] `browser-inspect` smoke test (deferred — see carry-forwards)

**Deliverables**:
- 8 of 9 code changes committed (FR-4 and FR-6 verified no-op per spec revision); see commits above
- Updated test suite passing (176 tests)
- Regenerated `verified_scores.{json,md}` (`calibrated_scores.*` deferred)
- `browser-inspect` smoke session — **deferred**

**Carry-forwards into Item 5**:
1. **`calibrated_scores.{json,md}` not regenerated** — `extract-scores` ran (deterministic), but the single cross-concept `calibrate` Claude call hit the session time cap and was killed. Five concepts (`04-laser-icf`, `11-magnetic-mirror`, `37-magnetized-target-inertial-fusion-mtif`, `38-particle-accelerator-driven-fusion`, `39-spherical-tokamak-cs-free-p-b11`) also lack Section-8 synthesis YAML and so are missing from `verified_scores.json`. Item 5's synthesis refresh should resynthesize those five and then run `calibrate` once afterward.
2. **`browser-inspect` smoke not run** — taxonomy/compare/neighborhood views were not click-tested. The underlying contract (decision_tree.json shape, JS field labels) is exercised by the test suite (`test_taxonomy_server.py` confirms the new `tree_group` root field; `test_taxonomy_models.py` confirms the six top-level groups) but the visual gate is unverified. Run before Item 4's PR-to-`main`.

---

### Item 4: Resolve v3 design open questions and merge to `main`

**Type**: Research → Decision → Implementation
**Effort**: 0.5–1 day (depending on how much CSV reshaping the decisions force)
**Dependencies**: Item 3

**Objective**: Decide and apply the two outstanding design calls before merging the migration to `main`, so we don't ship internal inconsistencies.

**Scope**:
1. **HB11 Fast-ignition vs Ultrashort**: confirm with the source dossier and Mallory whether HB11's `Laser Approach` is `Fast ignition` (per `table.csv` row 04 on the branch) or `Ultrashort` (per `CONCEPT_ONTOLOGY.md` table on the branch). Apply whichever is correct in both places.
2. **CSV vs MD source of truth for `Heating Type` / `Driver Type`**: the v3 ontology markdown introduces these typed vocabularies but `table.csv` still carries the old `Primary Heating` and free-text `Driver Technology`. Decide:
   - (a) extend `table.csv` with explicit `Heating Type` and `Driver Type` columns derived from the new vocab, and update `taxonomy_models.py` accordingly; OR
   - (b) make `CONCEPT_ONTOLOGY.md` the source and have `table.csv` derived from it via a generator.
   Recommend (a) — it keeps a single CSV source and avoids markdown round-tripping — but (b) is viable if we want the markdown to be the human-editable surface. Capture the decision in a short ADR-style note in `exploration/phase_1a/`.
3. Apply the decision: either extend the CSV (and `seed_registry.py`, `taxonomy_models.py`) or implement the MD→CSV generator.
4. Open the PR from `ontology-v3-migration` → `main`.
5. Merge.

**Out of Scope**:
- Rerunning synthesis (Item 5).
- Backlog cleanup (Item 6).

**Success Criteria**:
- [ ] HB11 row in `table.csv` and `CONCEPT_ONTOLOGY.md` agree
- [ ] Decision recorded for `Heating Type` / `Driver Type` source of truth
- [ ] PR merged to `main`
- [ ] Auto-memory entry added: "ID-prefix lookups are a known footgun — derive classification from architecture columns + slug overrides"

**Deliverables**:
- ADR note in `exploration/phase_1a/`
- Updated `table.csv` / generator
- Merged PR

---

### Item 5: Bring every concept to ≥3 analysis iterations

**Type**: Execution
**Effort**: 2–4 days (3 new concepts from scratch + 6 under-iterated concepts)
**Dependencies**: Item 4

**Objective**: Every concept in the slate has at least 3 iterations of analysis + model_setup so the cross-concept comparison floor is consistent. New v3 concepts that have CSV rows but no upstream artifacts get bootstrapped to the same bar.

**Scope**:

Audited 2026-05-17 — 9 concepts below the bar:

| Concept | Iters today | Action |
|---|---|---|
| `03-laser-icf-liquid-jet-target` | 1 | Run 2 more iters |
| `04-laser-icf` (HB11) | 1 | Run 2 more iters |
| `05-planar-coil-stellarator` | 1 | Run 2 more iters |
| `11-magnetic-mirror` | 1 | Run 2 more iters |
| `06-magnetic-mirror` | 2 | Run 1 more iter |
| `21-spherical-tokamak-hts` | 2 | Run 1 more iter |
| `37-magnetized-target-inertial-fusion-mtif` (NearStar) | 0 (no analyses dir) | Bootstrap research dossier + 3 iters |
| `38-particle-accelerator-driven-fusion` (SHINE) | 0 (no analyses dir) | Bootstrap research dossier + 3 iters |
| `39-spherical-tokamak-cs-free-p-b11` (ENN) | 0 (no analyses dir) | Bootstrap research dossier + 3 iters |

Execution:
1. For the 6 existing under-iterated concepts: `uv run python exploration/concept_analysis/scripts/run_analysis.py analyze <ID>` for the deficit iterations.
2. For the 3 new concepts (37/38/39): create `knowledge/concept_research/{ID}/` dossiers first (pull primary sources for NearStar, SHINE, ENN), then run analysis pipeline to ≥3 iters.
3. Re-extract for the explorer: `uv run python exploration/concept_explorer/extract_explorer_data.py --concept <ID>` for each touched concept.

**Out of Scope**:
- Synthesis refresh — not in scope here.
- Raising the bar above 3 iters for concepts already at ≥3.
- Adding new concepts beyond 37/38/39.

**Success Criteria**:
- [ ] `for d in exploration/concept_analysis/analyses/*/; do ls -d "$d"iter-* | wc -l; done` shows every count ≥ 3
- [ ] `37/`, `38/`, `39/` directories exist under both `knowledge/concept_research/` and `exploration/concept_analysis/analyses/`
- [ ] `extract_explorer_data.py` runs clean for every touched concept

**Deliverables**:
- Iterations added per the table above
- Research dossiers for NearStar, SHINE, ENN under `knowledge/concept_research/`
- Refreshed `concept_explorer/data/{ID}.json` for touched concepts
- Refreshed `concept_explorer/data/{ID}.json` for the same set
- Brief summary table at `.project/research/<date>_ontology-v3-synthesis-refresh.md` listing what changed per concept

---

### Item 6: BACKLOG.md cleanup pass

**Type**: Code/Integration
**Effort**: 0.5 day
**Dependencies**: Item 5

**Objective**: Close out the BACKLOG entries that this epic resolved or superseded, and explicitly reroll the ones it didn't.

**Scope**:
1. Mark closed in BACKLOG.md:
   - "Refresh synthesis.md for 13 standardized concepts" (absorbed into Item 5)
2. Carry forward (still P2/P3, unchanged):
   - "Investigate 20a capital-side availability coupling"
   - "Non-D-T availability policy + standardize"
   - "Concept 09 dual-site availability refactor"
   - "Audit script for DEFAULT labels vs actual values"
3. Add new BACKLOG entries for any v3 follow-ups discovered during Items 2–4 that didn't fit in the epic scope (e.g. if the CSV-vs-MD decision triggers an MD→CSV generator, log it as a future P3 maintenance item).
4. Update `Last Updated` date and add a "v3 migration completed" row to the Completed table.

**Out of Scope**:
- Anything not in BACKLOG.md.
- Spec/design/plan files for the carry-forward items.

**Success Criteria**:
- [ ] BACKLOG.md `Last Updated` date is current
- [ ] No stale references to dropped/renumbered concepts in BACKLOG.md
- [ ] Epic moved to Completed table with duration filled in
- [ ] Auto-memory updated with the v3 schema reference

**Deliverables**:
- Updated `.project/backlog/BACKLOG.md`
- Updated `.project/CURRENT_WORK.md`
- This epic file moved to `.project/completed/` (per project convention if applicable)

---

## Dependencies

**External**:
- `origin/fix/concept-renumbering-robustness` (single commit `1b960a9`, Mallory) — must remain accessible for cherry-pick / merge
- `uv` Python environment with current dependencies
- Concept research artifacts on R2 (already pulled or pullable via `scripts/sync_research.sh`)

**Internal**:
- Existing `.project/active/` items unaffected
- Availability standardization work on `consistency-checks` (Item 1 ships it)

**Item Dependency Graph**:
```
Item 1: Land consistency-checks  (0.5d)
  └─> Item 2: Merge v3 branch    (1.5d)
        └─> Item 3: Close gaps + tests  (1.5d)
              └─> Item 4: Design Qs + PR  (0.5–1d)
                    └─> Item 5: Synthesis refresh  (1–2d)
                          └─> Item 6: BACKLOG cleanup  (0.5d)
```

Items 1–4 are strictly sequential because each writes to the same files the next reads. Item 5 *could* start in parallel with Item 4 for the availability-only concepts (their refresh isn't ontology-dependent), but the simpler scheduling is strictly serial.

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Merge conflicts between Item 1's standardization edits and the branch's reclassified analyses are extensive (every analyzed concept overlaps) | High | Treat Item 2 as a careful merge, not a fast cherry-pick. Plan to re-apply Item 1's standardization on top of the renumbered IDs file-by-file. Budget half a day for this alone. |
| `ConfinementFamily` enum change cascades through `taxonomy_models.py` validators and breaks per-concept data files | Medium | Item 3 names this as an explicit decision. Recommend keeping the 4-bucket enum and adding a `tree_group` display-only field — minimizes blast radius. |
| Phase 2a `column_map.py` is wider than expected; LLM-derived constraint vocabularies need re-validation against new columns | Medium | Run Phase 2a end-to-end on a single representative concept (Item 3 success criteria) before declaring done. |
| Synthesis refresh (Item 5) is more expensive than budgeted because re-synthesis requires re-running parts of the pipeline | Medium | Synthesis-only refresh (not full re-analyze) is cheap (~$0.20/concept). Cap at $50 budget; if budget hits, halt and reassess. |
| HB11 classification (Fast ignition vs Ultrashort) isn't resolvable from sources and needs a Mallory call | Low | Item 4 explicitly calls this out. If unresolvable, ship the CSV value and add a `# DEVIATION:` note in the ontology MD. |
| Renumbering breaks external references (Linear tickets, R2 paths, other tools) | Low–Medium | Audit done in Item 2 success criteria. R2 path migration is part of the branch's pipeline rerun; verify R2 directory names match the new slugs before considering Item 2 done. |
| `scores/verified_scores.json` rerun (Item 3) blocked because the scoring pipeline assumes interactive Claude calls | Medium | Identify the scoring driver script during Item 3 design step; if interactive, batch via `claude -p` with a non-TTY fallback. The existing `lib/claude.py` harness should already handle this. |

---

## Timeline

**Total Effort**: 5.5–8 days (one engineer, sequential)

| Item | Effort | Dependencies | Branch |
|------|--------|--------------|--------|
| Item 1: Land `consistency-checks` | 0.5d | None | `consistency-checks` → `main` |
| Item 2: Merge ontology v3 branch | 1.5d | Item 1 | `ontology-v3-migration` |
| Item 3: Close v3 code gaps + tests | 1.5d | Item 2 | `ontology-v3-migration` |
| Item 4: Design Qs + merge PR | 0.5–1d | Item 3 | `ontology-v3-migration` → `main` |
| Item 5: Refresh synthesis | 1–2d | Item 4 | `synthesis-refresh-v3` → `main` |
| Item 6: BACKLOG cleanup | 0.5d | Item 5 | `synthesis-refresh-v3` (same PR) or trivial commit on `main` |

---

## Lessons Learned (Post-Completion)

*Fill in after epic is complete*

**What Went Well**:
- TBD

**What Could Improve**:
- TBD

**Surprises**:
- TBD

---

## References

- `.project/research/20260517_ontology_v3_delta.md` — full delta analysis + branch addendum
- `origin/fix/concept-renumbering-robustness` — commit `1b960a9` (Mallory, 2026-05-17)
- `.project/research/20260517-availability-policy-affected-concepts.md` — input to Item 5
- `exploration/phase_1a/CONCEPT_ONTOLOGY.md` (on the branch) — v3 canonical table
- `exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md` (on the branch) — P1–P10 schema rationale
- `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md` (on the branch) — per-concept move log

---

**Last Updated**: 2026-05-17
**Next Action**: Item 2 — branch `ontology-v3-migration` off updated `main`, merge/cherry-pick `1b960a9` from `origin/fix/concept-renumbering-robustness`, resolve conflicts
