# Design: Close v3 Code Gaps and Pass Tests

**Status:** ✅ Implemented 2026-05-17 (commits `ac320a4`, `f3f40c9`, `42d04b2`, `029b3ab` on `ontology-update`). Two carry-forwards into Item 5: `calibrate` Claude call timed out; `browser-inspect` smoke deferred. Revised 2026-05-17 (post-review: scoring cost analysis corrected, shared-helper question resolved, enum typing verified, JSON snippet added, spec FR-4/6/8 amendments reflected).
**Owner:** Reid W
**Created:** 2026-05-17
**Branch:** ontology-update
**Spec:** `.project/active/ontology-v3-close-gaps/spec.md`

---

## Overview

Close the nine v3-migration follow-up gaps with surgical edits: rename/drop stale field references where the data model already changed, encode v3 sibling groups in the explorer's decision tree as a display-only layer, refactor two ID-prefix-keyed analysis scripts to the architecture-driven classification pattern that `lib/scoring.py` already exemplifies, fix the test suite, regenerate scores, and smoke-test the explorer.

## Related Artifacts

- **Spec:** `.project/active/ontology-v3-close-gaps/spec.md`
- **Epic:** `.project/backlog/epic_ontology_v3_migration.md` (Item 3)
- **Research:** `.project/research/20260517_ontology_v3_delta.md` (§Addendum is the gap source)
- **Prior:** `.project/active/ontology-v3-merge/` (Item 2, complete)

## Research Findings

Inventory of the current state vs. spec assumptions (full evidence in Appendix A):

| Spec gap | Current state | Real work |
|---|---|---|
| 1. `phase_2a/column_map.py` | `DESIGN_COLUMNS` (lines 26–44), `KEY_TO_COLUMN` (363–389), `VOCABULARY` (94–188) still reference dropped columns | Drop three columns + their `VOCABULARY` and `KEY_TO_COLUMN` entries; add `Blanket Config` mirror entries |
| 2. `seed_registry.py::_HIERARCHY` | Lines 134–149 still encode old `MFE/IFE/MIF/NONSTANDARD` tree only (verified) | Add `tree_group` display layer + v3 sibling groups; keep `ConfinementFamily` enum unchanged |
| 3. Jinja templates | **Already clean** — grep for `tritium_breeding`/`neutron_management`/`plasma_state`/`blanket_config` in all `.j2` files returns zero hits. Field display routes through Python/JS, not template field names | No-op; verify-clean grep gates FR-4 (revised) |
| 4. `neighborhood_graph.js` | Lines 46–50 still hardcode dropped fields as display labels; `taxonomy_card.js:27,146` and `view_categorical.js:65` already use a `{field, label}` dict pattern | Align to the refactored pattern; add `blanket_config`, drop the three retired |
| 5. `parameter_display_registry.yaml` | Only numeric-parameter entries (e.g. `blanket_t`). `blanket_config` is categorical, doesn't belong; the dropped columns were never numeric parameters | **No change needed** — verify-clean grep gates FR-6 (revised) |
| 6. `test_taxonomy_models.py` | Lines 29, 33 import `PlasmaState`, `TritiumBreeding` which no longer exist → import-time crash. `test_round_trip` (lines 61–63) assigns the dropped fields. Other test modules also touch `plasma_state` | Real fix: rewrite to use `BlanketConfig`; sweep sibling test files |
| 7. `oneoff_3d_clustering.py` | `CADENCE_BY_PREFIX` (88–119) keyed by 2-digit ID prefix → silently miscategorizes after renumber; `FUNDING_M_USD` (43–82) keyed by full slug, **safe but missing new-concept entries (37/38/39)** | Refactor `CADENCE_BY_PREFIX` to architecture-derived keys (FR-8 revised); audit `FUNDING_M_USD` and add 37/38/39 entries |
| 8. `generate_ontology_chart.py::TREE_PATH` | Lines 201–244: hardcoded `{prefix: (family, topology, subtype)}` dict | Derive from `table.csv` via the same architecture-column logic the explorer uses; ~50 lines replaced |
| 9. Scores | `scores/verified_scores.{json,md}`, `scores/calibrated_scores.{json,md}` committed pre-refactor; entry is `run_scoring_pipeline.py` (verified) | Rerun deterministically; commit new artifacts |

Additional findings:
- **`ConfinementFamily` enum is unchanged in v3** — `taxonomy_models.py:111–113` already removed `PlasmaState`/`NeutronManagement` enums; `BlanketConfig` enum (lines 131–139) and `ConceptTaxonomy.blanket_config` field (line 194) are present. The data-model layer is done.
- **Architecture-driven classification reference** lives in `exploration/concept_analysis/scripts/lib/scoring.py` and `concepts.py` — uses `Confinement Family / MFE Topology / Magnet Type / IFE Driver / MIF Method` + slug overrides. This is the pattern to mirror in gaps 7 and 8.
- **No stale `FREEFORM_CONCEPTS` / `_C2_CONCEPT_MAP` references** remain in `exploration/` (verified via grep). The carry-forward audit from Item 2 is mostly already done.
- **Scoring rerun cost** — verified by reading `run_analysis.py` and `lib/scoring.py`:
  - `cmd_extract_scores` (`run_analysis.py:1222`) calls `build_verified_scores()` (`lib/scoring.py:380`), which reads each concept's existing `synthesis.md` Section 8 YAML (F1–F7, C1/C3/C4/C5/C8 = Claude-scored, preserved) and applies the **new** architecture-driven `detect_c2_category()` to recompute C2. **Pure Python, no Claude call.** Writes `scores/verified_scores.{json,md}`.
  - `cmd_calibrate` (`run_analysis.py:1260`) makes **one** cross-concept `invoke_claude_validated()` call (not per-concept). Reads `verified_scores.md`, emits `scores/calibrated_scores.{json,md}`. Cost ≈ $0.50.
  - `cmd_synthesize` and the legacy `cmd_score` *are* per-concept Claude calls but **are not on the rerun path** for FR-10; synthesis prose refresh is Item 5's job.
  - Net Item-3 scoring cost ≈ $0.50, well inside spec NFR-2's $50 ceiling. This addresses the epic's Risk row at line 289 ("if interactive, batch via `claude -p`") — `calibrate` is already single-call, no batching needed.

**Net effect on scope:** spec gaps 3 and 5 collapse to no-ops with documentation. The real work is concentrated in gaps 1, 2, 4, 6, 7, 8, plus the scoring rerun.

## Core Concept

The v3 data model is already in place. What remains is a perimeter cleanup: every place the codebase still *names* the dropped columns, every place that still *infers classification from numeric ID prefixes*, and every artifact (tests, scores) generated before those names and inferences were corrected. The design organizes these as four concentric rings — **schema names** (column_map), **display layer** (seed_registry tree, JS, templates), **classification logic** (clustering, chart generation), and **derived artifacts** (tests, scores) — and closes each ring with the same principle: data-model-first. Where the data model already encodes the answer (a CSV column, a `ConfinementFamily` value, a slug), the consumer reads it; where it doesn't (display-only sibling groups like Estatic/Cmpt-Tor), we add a thin display layer rather than mutating the model.

The key insight that justifies this approach: **`ConfinementFamily` and `tree_group` are different concerns.** The enum is a stable classification used by scoring, similarity, and Phase 2a; the v3 sibling groups are a display reorganization for the decision tree. Conflating them by extending the enum would force a cascade through `taxonomy_models.py` validators, every concept JSON, every scoring path, and every test fixture. Keeping them separate lets the visible UI change come from a `_HIERARCHY` rewrite alone.

## Key Bets & Decisions

**Bet 1 — Display-only `tree_group` layer over enum extension.** Add v3 sibling groups (Estatic, Other, Cmpt-Tor; Dipole/Supported; MIF/Pulsed power) by extending `_HIERARCHY` / `_SUBTYPES` and introducing a `tree_group` derivation function that maps `(ConfinementFamily, MFE Topology, Magnet Type, …)` → display group. The `ConfinementFamily` enum stays 4-bucket. Documented as a one-paragraph ADR comment at the top of `_HIERARCHY`.
**Alternative rejected:** Extending the enum. Forces cascading changes through validators, every per-concept JSON, scoring code, and test fixtures, in exchange for a UI-only benefit.

**Bet 2 — Architecture-driven keys, mirroring `lib/scoring.py`.** Refactor `oneoff_3d_clustering.py::CADENCE_BY_PREFIX` and `generate_ontology_chart.py::TREE_PATH` to derive keys from architecture columns + slug overrides (same shape as `scoring.py::_classify_concept`). `FUNDING_M_USD` stays slug-keyed because slugs are stable (the footgun was prefix keying, not slug keying — only refactor what's actually unsafe).
**Alternative rejected:** Patching the ID-keyed dicts with the four new concepts. Leaves the renumbering footgun unfixed.

**Bet 3 — Regenerate scores via the deterministic stages only; do not re-synthesize.** Run `uv run python exploration/concept_analysis/scripts/run_analysis.py extract-scores` (free, deterministic Python — re-derives C2 from `detect_c2_category` reading existing synthesis YAML) followed by `... calibrate` (one cross-concept Claude call, ≈ $0.50). Commit the regenerated `scores/verified_scores.{json,md}` and `scores/calibrated_scores.{json,md}`.
**Why not `run_scoring_pipeline.py` end-to-end:** that script also runs `synthesize` (per-concept Claude call) and `heatmap`. `synthesize` would rewrite prose under the new classifier — that's Item 5's job, not Item 3's, and the per-concept cost would push past NFR-2. `heatmap` regenerates rendered artifacts not required by FR-10.
**Alternative rejected:** Hand-editing the JSON. Encodes the new classifier values without traceability and risks drift the next time scoring is rerun.
**Cost calibration:** ≈ $0.50 actual; $50 spec ceiling absorbs the edge case where a synthesis YAML block is malformed (warns out of `build_verified_scores`) and a small `synthesize` rerun for 1–2 concepts is needed to recover. If more than ~5 concepts need re-synthesis, stop and reassess scope.

**Bet 4 — Stale-import audit becomes Phase 1, not a cleanup step.** Run the grep sweep (`Plasma State`, `Tritium Breeding`, `Neutron Management`, `_C2_CONCEPT_MAP`, `FREEFORM_CONCEPTS`, ID-prefix dict literals) up front. Either every hit becomes a phase or is explicitly logged as out-of-scope. Prevents the "we missed one" failure mode that Item 2's review caught twice.

**Bet 5 — Phase 2a smoke and `browser-inspect` smoke are part of done, not optional.** Each is a discrete plan phase with a saved artifact (zero `UNMAPPABLE` count, `/tmp/browser_inspect/<session>/` JSON).

**Bet 6 — Spec gaps 3 and 5 close as documented no-ops, not skipped.** Spec FR-4 and FR-6 were amended at design time to "verify clean" (codebase already in target state). Commits 3a and 3b in the FR-to-commit map (see Implementation Notes) execute the verification grep and record the result.

**Bet 7 — No new shared "classifier helper" module; pattern-by-reference instead.** Each consumer (`seed_registry.tree_group`, `oneoff_3d_clustering.cadence_by_architecture`, `generate_ontology_chart.derive_tree_path`) reads the same architecture columns but produces a *different* output shape (group string, float, 3-tuple). Factoring a shared function would not reduce code, and `concept_explorer/` and `concept_analysis/scripts/lib/` are separate Python packages with awkward cross-import (`lib/` modules use flat `from lib.x import y` assuming cwd, no `__init__.py` above `lib/`). Each consumer ships with a `# Mirrors lib/scoring.py:detect_c2_category — keep column reads and slug overrides in sync` comment at the top of its derivation function. The stale-import grep in Bet 4 includes the architecture-column names to catch drift.
**Alternative considered:** extract a shared `exploration/architecture_classifier.py` module. Rejected — would force `concept_analysis/scripts/lib/scoring.py` and `concept_explorer/seed_registry.py` to coordinate on a third-party module with cross-package sys.path semantics; net code change is larger than the duplication it would eliminate.

## Architecture

```
                    ┌──────────────────────────────────────┐
                    │  table.csv  (v3 schema — fixed)      │
                    │  taxonomy_models.py  (v3 — fixed)    │
                    └─────────────┬────────────────────────┘
                                  │ reads
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
  column_map.py            seed_registry.py          lib/scoring.py
  (Phase 2a names)         (decision tree +          (architecture-
   FR-1                     tree_group display)      driven classifier
                            FR-2, FR-3                — reference impl)
        │                         │                         │
        │                         ▼                         │
        │                  decision_tree.json               │
        │                         │                         │
        │                         ▼                         │
        │                  JS field/label dicts             │
        │                  (neighborhood_graph.js           │
        │                   aligns to taxonomy_card.js)     │
        │                   FR-5                            │
        │                                                   ▼
        │                                          oneoff_3d_clustering.py
        │                                          generate_ontology_chart.py
        │                                          (mirror lib/scoring.py
        │                                           pattern)
        │                                           FR-8, FR-9, FR-14
        │
        └────────────────► test_taxonomy_models.py
                           parameter_display_registry.yaml (no-op)
                           Jinja templates (no-op)
                           FR-6 (no-op), FR-7

                    ┌──────────────────────────────────┐
                    │  run_scoring_pipeline.py         │
                    │  → scores/{verified,calibrated}  │
                    │  FR-10                           │
                    └──────────────────────────────────┘

Smoke gates:  Phase 2a expand (0 UNMAPPABLE)  +  browser-inspect (0 console errs)
              FR-11, FR-12
```

The four rings (schema names → display layer → classification logic → derived artifacts) are independent enough to be implemented as separate phases. The only cross-ring dependency is that gap 2 (decision tree) and gap 4 (JS) share a field-name contract; both must use `blanket_config`.

## Required Invariants

- **I-1** No file in `exploration/` references `Plasma State`, `Tritium Breeding`, or `Neutron Management` as a column name or field key after this work.
- **I-2** No file in `exploration/` keys classification on a numeric ID prefix (string slices like `concept_id[:2]`, dict literals like `{"01": …}` used to infer classification). Slug-keyed dicts where the slug is the stable identifier (`FUNDING_M_USD`) are allowed.
- **I-3** `ConfinementFamily` enum and `ConceptTaxonomy` model are unchanged by this work.
- **I-4** `table.csv` schema and content are unchanged by this work.
- **I-5** No `analyses/{ID}/` files outside `scores/` are touched. (Item 2's FR-14 boundary; scoring rerun is the documented exception.)
- **I-6** `decision_tree.json` after `seed_registry.py` regeneration contains the v3 sibling groups (Estatic, Other, Cmpt-Tor visible as top-level entries alongside MFE/IFE/MIF).
- **I-7** `oneoff_3d_clustering.py` and `generate_ontology_chart.py` produce byte-identical output for concepts whose architecture columns are unchanged (regression check; FR-14).

## Component Overview

- **`exploration/phase_2a/column_map.py`** — Phase 2a column vocabulary. Drop the three retired columns from `DESIGN_COLUMNS`/`KEY_TO_COLUMN`/`VOCABULARY`/`VALUE_ALIASES`; add `Blanket Config` mirrors using the existing `MappedTerm` shape.
- **`exploration/concept_explorer/seed_registry.py`** — Decision tree builder. Extend `_HIERARCHY` and `_SUBTYPES` with v3 sibling groups; add a `tree_group(concept) → str` helper used as the top-level grouping key; add ADR comment.
- **`exploration/concept_explorer/static/js/neighborhood_graph.js`** — Neighborhood graph view. Replace hardcoded `[{label: "Plasma State", …}]`-style references with the `{field, label}` dict pattern used by `taxonomy_card.js:27,146` and `view_categorical.js:65`; include `blanket_config`.
- **`exploration/concept_explorer/tests/test_taxonomy_models.py`** (+ sibling test files that import dropped enums) — Test suite. Remove `PlasmaState`/`TritiumBreeding` imports; rewrite `test_round_trip` to round-trip `BlanketConfig`; add a `BlanketConfig` enum coverage test.
- **`exploration/concept_analysis/scripts/oneoff_3d_clustering.py`** — One-off 3D clustering driver. Replace `CADENCE_BY_PREFIX` with `cadence_by_architecture(concept) → float` derived from `Confinement Family / MFE Topology / Magnet Type` plus a small slug-override dict for edge cases (FR-8 revised). Keep `FUNDING_M_USD` slug-keyed but audit against `table.csv`: add entries for 37 NearStar, 38 SHINE, 39 ENN (currently missing); the Pranos entry may stay (Item 6 cleanup) or be removed.
- **`exploration/phase_1a/generate_ontology_chart.py`** — Static ontology chart generator. Replace `TREE_PATH` constant with a function that reads `table.csv` and derives `(family, topology, subtype)` per row via the same logic as `seed_registry.py`'s decision-tree path.
- **`exploration/concept_analysis/scripts/run_analysis.py`** (subcommands `extract-scores` and `calibrate`) — Score regeneration entry points. `extract-scores` is deterministic Python; `calibrate` is a single Claude call. **Do not** invoke `run_scoring_pipeline.py` end-to-end (it would also run per-concept `synthesize`). Outputs: `scores/verified_scores.{json,md}` and `scores/calibrated_scores.{json,md}`.
- **Smoke harnesses** — Phase 2a expand on one representative concept (zero `UNMAPPABLE` from dropped columns); `browser-inspect` session against the local explorer (zero console errors; v3 tree visible).

## Non-Goals

- `table.csv` schema changes (Item 4).
- HB11 Fast-ignition-vs-Ultrashort decision (Item 4).
- New `Heating Type` / `Driver Type` columns (Item 4).
- `synthesis.md` refresh (Item 5).
- Per-concept `concept_explorer/data/{ID}.json` re-extraction beyond what scoring rerun writes (Item 5).
- Extending `ConfinementFamily` enum.
- Refactoring `FUNDING_M_USD` keying (slug-stable, not a footgun).
- Touching templates or `parameter_display_registry.yaml` (verified no-op).

## Implementation Notes

**Decision tree shape contract.** The current `decision_tree.json` shape is `{family: {topology: [concepts]}}`. The v3 shape adds sibling top-level keys at the family level (Estatic, Other, Cmpt-Tor become peers of MFE/IFE/MIF in the tree even though they're not `ConfinementFamily` enum values). Implementation can either (a) keep `family` as the dict key and let the top-level set include the new strings, or (b) introduce `tree_group` as a new outer dict key. **Pick (a)** — it minimizes JS consumer churn. Document the convention in the ADR comment.

**`tree_group` derivation** — enum values verified against `taxonomy_models.py`:
- `MFETopology.COMPACT_TOROID = "Compact Toroid"` (capital T)
- `NonStandardMechanism` members: `ELECTROSTATIC`, `MUON_CATALYZED`, `PLASMA_FOCUS`. "IEC" and "Polywell" are *not* enum members — Polywell-style devices use `mechanism = Electrostatic`.

```python
def tree_group(c: ConceptTaxonomy) -> str:
    """v3 display-only sibling grouping. Mirrors lib/scoring.py:detect_c2_category
    pattern (architecture columns, no ID prefix); keep slug overrides in sync."""
    if c.confinement_family == ConfinementFamily.NONSTANDARD:
        if c.non_standard_mechanism == NonStandardMechanism.ELECTROSTATIC:
            return "Estatic"
        return "Other"
    if c.mfe_topology == MFETopology.COMPACT_TOROID:
        return "Cmpt-Tor"
    return c.confinement_family.value  # "MFE" | "IFE" | "MIF"
```

The function returns one of: `"MFE"`, `"IFE"`, `"MIF"`, `"Cmpt-Tor"`, `"Estatic"`, `"Other"`. Test by iterating every row in `table.csv` and printing the resulting group; cross-check against the table in `CONCEPT_ONTOLOGY.md`.

**`decision_tree.json` shape — before/after.** Choosing option (a) (`tree_group` becomes top-level key, replacing `confinement_family`):

```jsonc
// Before (today's main, post-Item-2):
{
  "MFE":  { "Tokamak":      ["01-...", "21-...", ...],
            "Stellarator":  ["05-...", ...] },
  "IFE":  { "Laser":        ["04-...", ...] },
  "MIF":  { "Magnetized target": ["07-..."] },
  "NONSTANDARD": { "Electrostatic": ["13-...", "27-..."],
                   "Plasma focus":  ["24-..."] }
}

// After:
{
  "MFE":      { "Tokamak":     ["01-...", "21-...", ...],
                "Stellarator": ["05-...", ...] },
  "IFE":      { "Laser":       ["04-...", ...] },
  "MIF":      { "Magnetized target": ["07-..."] },
  "Cmpt-Tor": { "FRC":              ["08-...", "18-..."],
                "Pulsed":           ["15-..."] },
  "Estatic":  { "Polywell":         ["27-..."],
                "IEC":              ["13-..."] },
  "Other":    { "Plasma focus":     ["24-..."],
                "Muon-catalyzed":   ["16-..."] }
}
```

JS consumers iterate top-level keys (`Object.keys(tree)`) — they get the six v3 groups instead of four, no schema change. Levels-of-nesting unchanged.

**Phase 2a `VOCABULARY` entries for `Blanket Config`.** Follow the existing `MappedTerm("<column>", "<predicate>", "<value>")` shape. Enum values from `taxonomy_models.BlanketConfig` (LIQUID_METAL, MOLTEN_SALT, SOLID_BREEDER, OTHER_HYBRID, NA_NO_TRITIUM, NA_NON_POWER, TBD) are the authority for `VALUE_ALIASES`.

**Score rerun cost (corrected).** See Bet 3. `cmd_extract_scores` is deterministic Python (`build_verified_scores` in `lib/scoring.py:380` reads existing synthesis YAML + new `detect_c2_category`). `cmd_calibrate` makes one cross-concept Claude call (≈ $0.50). `cmd_synthesize` is **not** on the FR-10 path. Run order: `extract-scores` → `calibrate` (depends on `verified_scores.md` from the first). Treat `synthesize` as forbidden in Item 3 — fail loudly if a plan phase tries to invoke it.

**`generate_ontology_chart.py` I-7 regression check — baseline pinned.** Run the generator at commit `8db3ed2` (Item 2's post-merge tip) and save the PNG + any CSV output to `/tmp/i7_baseline/`. After the refactor, regenerate and diff. Any change for a concept whose architecture columns are unchanged fails I-7. (Pinning the baseline to `8db3ed2` rather than `main` is important: pre-Item-2 `main` has the v0.2.x schema and would diff on schema grounds, not refactor grounds.)

**Stale-import sweep query** (run before declaring done): `rg -n 'Plasma State|Tritium Breeding|Neutron Management|_C2_CONCEPT_MAP|FREEFORM_CONCEPTS|CADENCE_BY_PREFIX|TREE_PATH' exploration/` plus a focused search for `concept_id\[:2\]` and `id\[:2\]` slicing patterns.

**FR → commit map** (NFR-1 reconciliation — 14 FRs collapse into 6 reviewable commits aligned to the 6 phases):

| Phase | Commits | FRs satisfied |
|---|---|---|
| 0 — Audit | (none; baseline artifacts saved to `/tmp/i7_baseline/`, no commit) | FR-13 setup, FR-14 baseline |
| 1 — Schema names | C1: `column_map.py` edits | FR-1 |
| 2 — Display layer | C2: `seed_registry.py` + ADR + regenerated `decision_tree.json`; C3: `neighborhood_graph.js` rename | FR-2, FR-3, FR-5 |
| 3 — Classification logic | C4: `oneoff_3d_clustering.py` refactor + `FUNDING_M_USD` audit; C5: `generate_ontology_chart.py` refactor + I-7 diff | FR-8, FR-9, FR-14 |
| 4 — Derived artifacts | C6: test suite updates + `BlanketConfig` coverage; C7: scoring rerun (`extract-scores` + `calibrate`) commits `scores/*` | FR-7, FR-10, FR-11 |
| 5 — Final sweep | (no new commit; verifies FR-4, FR-6 no-ops via grep; runs Phase 2a smoke + `browser-inspect`; appends verification artifacts to Phase 4's commit notes) | FR-4, FR-6, FR-12, FR-13 |

Phases 0 and 5 produce no fresh commits; FR-4 and FR-6 are verify-only per the spec revision. Total: 7 commits in 6 phases. Plan stage can collapse C2+C3 or C4+C5 if review pressure demands fewer commits, but each pair has a clean review boundary.

## Potential Risks

| Risk | Mitigation |
|---|---|
| `decision_tree.json` shape change breaks an explorer JS consumer that hard-asserts keys | Phase the JS update with the seed_registry change; `browser-inspect` smoke catches it before commit |
| `tree_group` mapping is wrong for an edge concept (e.g. Levitated Dipole, which is both MFE-topology and a v3 "Dipole" leaf) | Test the mapping against every row in `table.csv` as part of the seed_registry change; print the resulting grouping; compare against `CONCEPT_ONTOLOGY.md` |
| Score rerun produces unexpected diffs because the v3 classifier reads architecture columns we didn't audit | Diff `scores/calibrated_scores.json` before/after; if any concept's C2 changes, confirm it matches the v3 reclassification expected behavior |
| Refactoring `oneoff_3d_clustering.py` introduces a subtle behavior change | I-7 regression check: rerun on the v0.2.x committed table.csv (from `main`) and confirm output is unchanged for shared concepts |
| Test fixtures touch more files than `test_taxonomy_models.py` | Inventory found `test_state_and_compute.py:82`, `test_extraction.py:115` also reference `plasma_state` — sweep all `exploration/concept_explorer/tests/` in one phase |

## Integration Strategy

This is a perimeter cleanup on the `ontology-update` branch. No new branch needed. Sequencing:

1. **Audit (Phase 0)** — stale-reference grep, save baseline outputs from `oneoff_3d_clustering.py` and `generate_ontology_chart.py` for I-7.
2. **Schema names ring (Phase 1)** — `column_map.py` + tests for it. Phase 2a smoke gate here.
3. **Display layer ring (Phase 2)** — `seed_registry.py` (+ ADR), `neighborhood_graph.js`. Regenerate `decision_tree.json`. `browser-inspect` smoke gate here.
4. **Classification logic ring (Phase 3)** — `oneoff_3d_clustering.py`, `generate_ontology_chart.py`. I-7 regression check here.
5. **Derived artifacts ring (Phase 4)** — `test_taxonomy_models.py` and siblings; `run_scoring_pipeline.py` rerun; commit `scores/*`.
6. **Final sweep (Phase 5)** — re-run the stale-reference grep; confirm I-1, I-2; update epic checkboxes.

Each phase commits independently (NFR-1). PR remains on `ontology-update`; merge-to-`main` is Item 4.

## Validation Approach

- **Per-phase gates** (called out above): Phase 2a `UNMAPPABLE` count, `browser-inspect` console-error count, I-7 byte-diff.
- **Test suite:** `uv run python -m pytest exploration/concept_explorer/tests/` green (FR-11).
- **Manual smoke:** `uv run python exploration/concept_explorer/seed_registry.py` → inspect `decision_tree.json` for Estatic/Other/Cmpt-Tor presence; spin up the explorer; click through taxonomy → concept → compare → neighborhood views for two concepts (one MFE, one Non-Standard); confirm no console errors.
- **Score sanity:** diff `scores/calibrated_scores.json` before/after; spot-check the 8 historically-miscategorized concepts have C2 values matching their v3 classification.
- **Done-criteria for the epic checkbox:** all spec acceptance checkboxes flipped; commits grouped per NFR-1; saved `browser-inspect` session JSON path recorded in the wrap-up.

## Next-Stage Handoff

**Plan must treat as fixed:**
- Six phases above (Audit → Schema names → Display → Classification → Derived → Sweep).
- Bets 1–6 (display-only `tree_group`, architecture-driven keys, regenerate scores, audit-first, smoke-as-done, no-ops documented).
- Invariants I-1 through I-7.

**Plan must figure out:**
- Concrete file:line edit list per phase.
- Exact representative concept for the Phase 2a smoke (suggest 19-tokamak-energy or another concept with a non-trivial blanket entry).
- Exact representative concepts for the explorer click-through (suggest one of each: MFE, IFE, MIF, NONSTANDARD/Estatic to cover the v3 sibling groups).
- Commit grouping (recommend one commit per phase = 6 commits, with the Phase 4 scoring rerun as its own commit so the JSON diff is reviewable in isolation).

**De-risk first:** Phase 2 (`tree_group` derivation + `decision_tree.json` shape) — this is the only piece with non-trivial logic and the only piece that can break the explorer UI invisibly. Build it first; smoke-test it before moving on.

---

## Appendix A — Detailed Inventory Evidence

(Captured during Stage 2 research; preserved for the plan stage.)

- **`column_map.py:26–44`** — `DESIGN_COLUMNS` includes the three retired columns.
- **`column_map.py:94–188`** — `VOCABULARY` entries keyed `plasma_state`, `tritium_breeding`, `neutron_management`.
- **`column_map.py:363–389`** — `KEY_TO_COLUMN` maps stale keys.
- **`seed_registry.py:134–149`** — `_HIERARCHY` lists only MFE/IFE/MIF/NONSTANDARD; no v3 groups.
- **`seed_registry.py:124`** — `blanket_config=_na_or_enum(...)` already wired (confirms data-model layer done).
- **`taxonomy_models.py:111–113`** — comment confirms PlasmaState/NeutronManagement removal.
- **`taxonomy_models.py:131–139`** — `BlanketConfig` enum present.
- **`taxonomy_models.py:194`** — `ConceptTaxonomy.blanket_config` field present.
- **Jinja templates** — `rg 'tritium_breeding|neutron_management|plasma_state|blanket_config' exploration/concept_explorer/templates/` → 0 hits.
- **`neighborhood_graph.js:46–50`** — hardcoded references to retired display labels.
- **`taxonomy_card.js:27,146`**, **`view_categorical.js:65`** — refactored `{field, label}` dict pattern (reference for the rename).
- **`parameter_display_registry.yaml`** — only numeric parameter entries; categorical fields not registered here.
- **`test_taxonomy_models.py:29,33,61,63`** — failing imports / usages of dropped enums.
- **`test_state_and_compute.py:82`, `test_extraction.py:115`** — additional `plasma_state` references.
- **`oneoff_3d_clustering.py:88–119`** — `CADENCE_BY_PREFIX` (prefix-keyed, footgun).
- **`oneoff_3d_clustering.py:43–82`** — `FUNDING_M_USD` (slug-keyed, safe).
- **`generate_ontology_chart.py:201–244`** — `TREE_PATH` hardcoded prefix-to-tuple dict.
- **`run_scoring_pipeline.py:267–270`** — emits the four score files.
- **`run_analysis.py:1239,1334,1353`** — score file paths and the calibrate entry point.
- **Stale-reference negatives** — no remaining hits for `FREEFORM_CONCEPTS` or `_C2_CONCEPT_MAP` in `exploration/`.

---

**Next Step:** After approval → `/_my_plan`.
