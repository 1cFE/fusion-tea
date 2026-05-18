# Design: Ontology v3 Adoption (No Renumbering)

**Status:** Complete (implemented 2026-05-17, commit `8db3ed2` on `ontology-update`)
**Owner:** Reid W
**Created:** 2026-05-17
**Branch:** `ontology-update` @ `244ca24`
**Spec:** [.project/active/ontology-v3-merge/spec.md](spec.md)
**Source branch:** `origin/fix/concept-renumbering-robustness` @ `1b960a9` (cherry-pick by file)
**Baseline:** `main` @ `a8a779e`

---

## Overview

Adopt v3 ontology *content* from Mallory's branch — schema swap, new concepts, code refactor, docs — while keeping our existing concept IDs. Mechanical execution is a CSV rewrite plus targeted file copies. The non-obvious work is reconciling two files (`scoring.py`, `standardize_eta_th.py`) where `main` has refactored since Mallory's branch point.

## Related Artifacts

- **Spec:** [spec.md](spec.md)
- **Epic:** [.project/backlog/epic_ontology_v3_migration.md](../../backlog/epic_ontology_v3_migration.md) (Item 2)
- **Research:** [.project/research/20260517_ontology_v3_delta.md](../../research/20260517_ontology_v3_delta.md) (esp. Addendum)
- **Plan (to be created):** [plan.md](plan.md)

---

## Research Findings

### Branch divergence since merge-base

- **Merge-base:** `704a3a5` (`Fusion tea scoring (#13)`).
- **Main has moved ahead** with 20+ commits including a scoring/canonical-params refactor that lands in files the spec marks as "verbatim pull from Mallory":
  - `45c9db5` (2026-05-17): adds `canonical_availability()` helper into `lib/scoring.py` (+59 LOC).
  - `6ba8f02` (2026-05-17): extracts canonical params into **new file** `lib/scoring/../canonical_params.py`; removes 110 LOC from `scoring.py`; updates `standardize_eta_th.py` to import from `canonical_params`.
- **Mallory's branch predates both refactors**, so her `scoring.py` keeps `_CANONICAL_ETA_TH` inline (lines 23–44), no `canonical_availability`, no `canonical_mn`, and a fresh `canonical_eta_th()` function (line 45).

### Spec'd files: drift map vs. main since merge-base

| File | Touched on main? | Status |
|---|---|---|
| `lib/scoring.py` | **Yes (2 commits)** | Conflict — needs synthesized merge (see below) |
| `lib/concepts.py` | No | Pull verbatim |
| `lib/claude.py` | No | Pull verbatim |
| `standardize_eta_th.py` | **Yes (1 commit)** | Conflict — needs synthesized merge |
| `rerun_all_models.py` | No (new file) | Pull verbatim |
| `C2_SCORING.md` | No (new file) | Pull verbatim |
| `taxonomy_models.py` | No | Pull verbatim |
| `seed_registry.py` | No | Pull verbatim |
| `similarity.py` | No | Pull verbatim |
| `static/js/taxonomy_card.js`, `view_categorical.js` | No | Pull verbatim |
| `phase_1a/schema.md` | No | Pull verbatim |
| `phase_1a/*.md` (4 new docs) | No (new files) | Pull verbatim |
| `phase_1a/generate_ontology_{chart,md}.py` | No (new files) | Pull verbatim |
| `phase_1a/concept_ontology_v3.png` | No (new file) | Pull verbatim |

### CSV inventory

- Main: 38 data rows (38-line header+rows; `wc -l` = 39 due to header).
- Mallory: 39 data rows under her renumbered scheme.
- Our target: **40 rows** = (38 main − 1 Pranos) + (3 new: NearStar, SHINE, ENN) + (0 net for 22 split: row 22 stays, NearStar becomes row 37 = one of the "3 new" above).

  Math sanity: 38 − 1 (Pranos drop) − 0 (22 stays, NearStar peeled out) + 1 (NearStar = 37) + 1 (SHINE = 38) + 1 (ENN = 39) = **40** ✓.

- Schema diff: drop `Plasma State, Tritium Breeding, Neutron Management`; add `Blanket Config`. Other column names unchanged.

### Orphan: `knowledge/concept_research/20-modular-hts-stellarator/`

- Directory exists with `dossier.md`, `iter-01..03/`, and last touched in commit `066a37d` (pre-split).
- `diff` confirms its `dossier.md` differs from both `20a-type-one-stellarator/` and `20b-renaissance-stellarator/`.
- **Decision:** has unique pre-split content; do not delete in this item. Document in `ID_MAPPING.md` and flag for Item 6.

---

## Core Concept

The v3 adoption is **a cherry-pick disguised as a merge**: we take Mallory's commit `1b960a9` and apply 18 files of her content to our tree, plus a programmatic CSV rewrite that translates her ID column to ours while preserving all other v3 column values verbatim. Two of those 18 files conflict with intervening `main` work and require a small synthesized version that keeps `main`'s `canonical_params` extraction *and* Mallory's architecture-driven classification refactor.

The key insight is that **Mallory's renumbering is decoupled from her real contribution**. Her code already derives classification from architecture columns (`Confinement Family`, `MFE Topology`, `IFE Driver`, `MIF Method`, `Magnet Type`) plus two slug overrides — never from numeric ID prefix. So our IDs flow through her code unchanged as long as the CSV's architecture columns are correctly populated. That makes "keep our IDs" cheap.

Why this approach is right:
- A merge would force ~30 directory renames; a cherry-pick-by-file produces a ~25-file PR.
- The CSV rewrite is the only non-trivial generation step, and it's small enough to be a single ~80-LOC script that lives next to Mallory's other phase_1a generators (and can be rerun if her branch evolves).
- The two `scoring.py`/`standardize_eta_th.py` conflicts have clean boundaries — Mallory adds new C2 logic in the lower half; main refactored canonical params in the upper half — so they merge cleanly when treated as orthogonal patches.

---

## Key Bets & Decisions

### Bet 1: A small Python generator owns the CSV translation

We commit `exploration/phase_1a/translate_csv_to_ours.py` (~80 LOC) that reads Mallory's CSV from disk (a checked-in snapshot at `exploration/phase_1a/_mallory_table.csv`), translates her IDs → ours, splits row 23, duplicates row 31 → our 26+30, drops Pranos, and writes `exploration/concept_analysis/table.csv` + `exploration/phase_1a/table.csv`.

**Why a script vs. hand-edit:**
- Idempotent and reviewable: the diff against Mallory's CSV is a few lines of mapping logic, not 40 hand-typed rows.
- Re-runnable if Mallory's branch evolves before we land this.
- Naturally explains the 26+30 duplication and 22-split as code, not commit-message prose.

**Why not a one-off script that gets deleted:** keeping it under `phase_1a/` mirrors Mallory's pattern (`generate_ontology_chart.py`, `generate_ontology_md.py`) — generators live with the data they generate.

**Alternative considered:** patch Mallory's CSV in-place with `sed`/`awk` in a Bash one-liner. Rejected — the 26/30 fan-out and the row-22 split are not regex-friendly.

### Bet 2: `scoring.py` and `standardize_eta_th.py` are two clean cherry-pick patches (no value reconciliation)

**Decision: relax FR-2 for these two files.** Substitute "byte-identical to Mallory" with "main + a targeted patch from Mallory." Verified findings that simplify this:

- **Mallory's `_CANONICAL_ETA_TH` table is byte-identical to main's `canonical_params.py` table** (same 16 entries, same values, same comments). Mallory's "thermal-cycle η_th update" in her commit message refers to the *regex* in `standardize_eta_th.py`, not the η_th values. So `canonical_params.py` is untouched.
- `lib/scoring.py` final content = main's slim version (no inline `_CANONICAL_ETA_TH`, no `canonical_eta_th()` function — those live in `canonical_params.py`) **+ the bottom half of Mallory's `scoring.py`**: her `detect_c2_category`, `_derive_peer_group`, `apply_heritage_credit`, peer-group logic. Mechanical patch, no value conflicts.
- `standardize_eta_th.py` final content = main's version (which imports from `canonical_params`) **+ Mallory's regex enhancement**: the extended pattern `_?(?:eta_th|...)(?:_[A-Za-z0-9]+)*` that also catches variant names like `_ETA_TH_CENTRAL`, `eta_dec`, `ETA_DEC`. This is real value-add — main's regex misses 4+ concepts (19, 25, 27, 36). Plan must call this out so it doesn't get lost during the merge.

**Why this is the right call:** main's `canonical_params` refactor is good engineering; Mallory's classification refactor + regex extension are the actual value-add. The two changes are orthogonal.

**Acceptance criteria update needed in plan:** the FR-2 verification "`git diff` returns empty for `scoring.py` / `standardize_eta_th.py`" cannot hold. Plan should restate as: "diff is non-empty but limited to the canonical-params relocation; PR review confirms Mallory's logic is fully carried over."

### Bet 3: Mallory's ontology docs and chart go in untranslated

`CONCEPT_ONTOLOGY.md`, `RECLASSIFIED_CONCEPTS.md`, `CONCEPT_CATEGORIES_PROPOSAL.md`, `SCHEMA_REVISION_PROPOSALS.md`, and `concept_ontology_v3.png` all reference Mallory's IDs. We pull them verbatim and add **one** new file `exploration/phase_1a/ID_MAPPING.md` plus **one** 2-line prepended note on `CONCEPT_ONTOLOGY.md` pointing at the mapping.

**Why not translate the docs:** translation is high-cost, low-value for this item — the docs are reference reading, not pipeline inputs. Item 4 can do the translation if/when those docs need to be canonical.

**Alternative:** rename Mallory's IDs throughout the prose with `sed`. Rejected — collisions (e.g., "17" appears as section headers, footnote refs, and ID literals; not all are safe to rewrite) and the renumbering is genuinely informative for someone tracing v3-design history.

### Bet 4: Orphan `20-modular-hts-stellarator/` stays put

Has unique pre-split dossier content (verified by `diff`). Document in `ID_MAPPING.md`, flag for Item 6 cleanup. Not worth a delete in this commit.

---

## Architecture

### Execution flow

```
1. Snapshot Mallory's CSV → exploration/phase_1a/_mallory_table.csv (checked in)
2. Copy 16 spec'd files verbatim from origin/fix/concept-renumbering-robustness
   (everything except scoring.py + standardize_eta_th.py)
3. Synthesize scoring.py and standardize_eta_th.py:
   - scoring.py: keep main's canonical-params imports, take Mallory's detect_c2 +
     heritage + peer-group logic
   - canonical_params.py: edit the canonical η_th table per Mallory's value changes
4. Run translate_csv_to_ours.py:
   - input:  exploration/phase_1a/_mallory_table.csv
   - output: exploration/concept_analysis/table.csv
   - output: exploration/phase_1a/table.csv (byte-identical copy)
5. Hand-author ID_MAPPING.md
6. Prepend 2-line note to phase_1a/CONCEPT_ONTOLOGY.md
7. Run: uv run python exploration/concept_explorer/seed_registry.py
   → regenerates concept_registry.json (40 entries) + decision_tree.json
8. Verify: uv run python exploration/concept_analysis/scripts/run_analysis.py status
9. Commit (single commit, attribution trailer)
```

### CSV translation logic

The generator reads Mallory's CSV as a list of dicts (csv.DictReader), then:

| Mallory's row | Action |
|---|---|
| Pranos | Skip (drop) |
| Row 31 (Inertia, deduped) | Emit **twice**: once as our `26-laser-icf-indirect-drive` (use Mallory's row 31 content but overwrite Concept Name/Company/Driver Technology/Research ID from our main `table.csv` row 26); once as our `30-laser-icf-nif-commercialization` (same pattern, overwrite from our row 30) |
| Row 23 (First Light only) | Emit as our `22-projectile-icf` (overwrite Research ID; keep `Company = "First Light Fusion"` only — Mallory already has this) |
| Row 37 (NearStar, new) | Emit as `37-magnetized-target-inertial-fusion-mtif` (Research ID = same slug) |
| Row 38 (SHINE, new) | Emit as `38-particle-accelerator-driven-fusion` |
| Row 39 (ENN, new) | Emit as `39-spherical-tokamak-cs-free-p-b11` |
| All other rows | Look up `mallory_id → our_id` via the renumbering table; rewrite `ID` and `Research ID` columns; pass through all other column values verbatim |

The renumbering table is the 16-row map in spec.md (lines 70–90), expressed as a Python dict literal at the top of the script. The output column order is Mallory's v3 header.

### File touch surface (for plan sizing)

- **Pulled verbatim** (16 files): `lib/concepts.py`, `lib/claude.py`, `rerun_all_models.py`, `C2_SCORING.md`, `taxonomy_models.py`, `seed_registry.py`, `similarity.py`, `static/js/taxonomy_card.js`, `static/js/view_categorical.js`, `schema.md`, `CONCEPT_ONTOLOGY.md` (then patched with 2-line note), `CONCEPT_CATEGORIES_PROPOSAL.md`, `RECLASSIFIED_CONCEPTS.md`, `SCHEMA_REVISION_PROPOSALS.md`, `concept_ontology_v3.png`, `generate_ontology_chart.py`, `generate_ontology_md.py`.
- **Synthesized merge** (2 files): `lib/scoring.py`, `standardize_eta_th.py` (or alternatively, just `canonical_params.py`).
- **Generated** (3 files): `table.csv`, `phase_1a/table.csv`, `concept_registry.json`, `decision_tree.json`.
- **New, hand-authored** (2 files): `phase_1a/ID_MAPPING.md`, `phase_1a/translate_csv_to_ours.py`, `phase_1a/_mallory_table.csv` (snapshot).
- **Net commit size:** ~27 files. Within NFR-2 budget.

---

## Required Invariants

- The CSV's architecture columns (`Confinement Family`, `MFE Topology`, `IFE Driver`, `MIF Method`, `Magnet Type`) **must be Mallory's values, not ours** for every row. `seed_registry.py` and the new `detect_c2_category` derive behavior from these — they are the load-bearing inputs.
- Our IDs in the `ID` and `Research ID` columns must match existing directory slugs under `analyses/` and `knowledge/concept_research/` for the 37 retained rows. For the 3 new rows, the slug Mallory chose is what we use (since new directories will be created in Item 5).
- `exploration/concept_analysis/table.csv` and `exploration/phase_1a/table.csv` are byte-identical (FR-5).
- `seed_registry.py` runs to completion against the new CSV and produces exactly 40 concept entries (FR-10, FR-12).
- No file under `analyses/` or `knowledge/concept_research/` is renamed in this commit (FR-13).
- No regenerated synthesis/analysis/model_output artifacts are committed (FR-14).

---

## Component Overview

- **`exploration/phase_1a/translate_csv_to_ours.py`** — new generator script. Reads `_mallory_table.csv`, applies the renumbering map + split + dedup-fanout, writes both CSV outputs. ~80 LOC.
- **`exploration/phase_1a/_mallory_table.csv`** — checked-in snapshot of Mallory's `exploration/concept_analysis/table.csv` at commit `1b960a9`. Treated as input data, not source code. Underscore prefix marks it as derived/snapshot.
- **`exploration/phase_1a/ID_MAPPING.md`** — new prose doc. Three sections: (1) renumbering map (the 16-row table from spec), (2) orphan-directory note for `20-modular-hts-stellarator/`, (3) pointer back to `CONCEPT_ONTOLOGY.md` for the v3 design rationale.
- **`exploration/concept_analysis/scripts/lib/scoring.py`** — cherry-pick patch. Take main's slim version + Mallory's bottom-half classification functions. See "Bet 2."
- **`exploration/concept_analysis/scripts/lib/canonical_params.py`** — **untouched** (Mallory's η_th table is byte-identical to main's; no edit needed).
- **`exploration/concept_analysis/scripts/standardize_eta_th.py`** — cherry-pick patch. Take main's version + Mallory's regex enhancement (extended pattern catching `_ETA_TH_CENTRAL`, `eta_dec`, `ETA_DEC`).
- **`exploration/concept_analysis/scripts/run_analysis.py`** — **NOT pulled.** Main's version is schema-agnostic for the dropped/added columns (grep confirms zero references to `Plasma State`/`Tritium Breeding`/`Neutron Management`/`Blanket Config`). Mallory's +127 LOC are out of scope for this item; Item 3 or 5 can pull if needed. Plan must explicitly state this so it isn't pulled on a whim.
- **`exploration/concept_explorer/data/{ID}.json`** (per-concept files) — **left untouched.** They exist on main with old-schema data and will be stale until Item 5 reruns `extract_explorer_data.py`. This commit must not stage them.
- All other spec-listed files — straight `git checkout origin/fix/concept-renumbering-robustness -- <path>`.

**Note on `CONCEPT_ONTOLOGY.md`:** the 2-line note prepended to its top is a hand-edit, not Mallory's content — it technically violates the verbatim guarantee. This is intentional and must be documented in the commit body. The note points readers to `ID_MAPPING.md`.

---

## Non-Goals

- Renaming any concept directory under `analyses/` or `knowledge/concept_research/`.
- Pulling Mallory's regenerated `analyses/{ID}/*.md` or `concept_explorer/data/{ID}.json`.
- Translating Mallory's ontology docs to our IDs (deferred to Item 4).
- Fixing `phase_2a/column_map.py`, `_HIERARCHY` in `seed_registry.py`, `ConfinementFamily` enum splits, Jinja templates, `neighborhood_graph.js`, `parameter_display_registry.yaml`, taxonomy tests (deferred to Item 3).
- HB11 Fast-ignition-vs-Ultrashort decision (deferred to Item 4).
- Pranos directory deletion (deferred to Item 6).
- Deleting `concept_research/20-modular-hts-stellarator/` (deferred to Item 6).

---

## Implementation Notes

**Mallory's CSV has the v3 header but **keeps the old hierarchy columns** (Confinement Family, MFE Topology, IFE Driver, MIF Method, Non-Standard Mechanism, Tokamak Shape, Stellarator Type, Laser Approach). They are not removed — they coexist with the new `Blanket Config` column. The dropped columns are `Plasma State`, `Tritium Breeding`, `Neutron Management`. Don't be tempted to "clean up" the hierarchy columns — Mallory's code reads them.

**The 26/30 fan-out edge case:** Mallory's row 31 has `Concept Name = "Laser ICF – Indirect Drive (Inertia)"` (or similar) which matches our 26 more than our 30. The translation script must read our existing `main` CSV to pull authoritative `Concept Name`, `Company`, `Driver Technology` values for both rows, and only pull from Mallory the v3-specific values (`Blanket Config`, classification columns, etc.). **Concretely:** define a small set of "identity columns" that come from our main CSV (Concept Name, Company, Driver Technology, Research ID) and "v3 columns" that come from Mallory's row 31 (Blanket Config, Fuel, Primary Heating, Energy Capture, Magnet Type, Operation Mode, Repetition Rate, Confinement Family, MFE Topology, IFE Driver, MIF Method, Non-Standard Mechanism, Tokamak Shape, Stellarator Type, Laser Approach, Overall Confidence).

**Research ID convention:** Set Research ID = our ID slug for every row. For the 3 new rows, Mallory's Research ID already matches our chosen slugs (37/38/39 are the same on her side).

**Snapshot freshness:** if Mallory pushes a new commit to her branch before we land this, refresh `_mallory_table.csv` (single `git show` redirect) and rerun the script.

**Pseudo-code for the generator (interface only, ~10 lines):**

```python
RENUMBER_MAP = {"17": "17b", "20": "20a", "21": "20b", ...}  # 16 entries
SPLIT_22 = "23"  # Mallory's 23 → our 22 (First Light only)
DUP_26_30 = "31" # Mallory's 31 → our 26 AND our 30
DROP = {"Pranos"}  # matched by company name
NEW_VERBATIM = {"37", "38", "39"}
# read _mallory_table.csv, read our main table.csv (for identity columns of 26/30),
# emit rows per the dispatch above, write both output CSVs.
```

---

## Potential Risks

- **`seed_registry.py` enum-validation errors.** Mallory's `taxonomy_models.py` drops `PlasmaState`/`TritiumBreeding`/`NeutronManagement` and adds `BlanketConfig` with a fixed enum. If the CSV has a `Blanket Config` value Mallory's enum doesn't cover (e.g. a typo like "Motten salt"), `seed_registry.py` raises. **Mitigation:** verify after step 4 by running with `--strict`/equivalent; if it warns, proceed; if it errors, capture the offending row+value, escalate. (Spec watch-out already flags this.)
- **Mallory's `Research ID` for renumbered rows is wrong for us.** The translation script must overwrite `Research ID` with our slug; if missed, downstream code that joins on Research ID breaks silently.
- **Drift in `standardize_eta_th.py` regex during merge.** Mallory's regex extension is small but easy to drop on the floor. Plan must call it out as an explicit verification step (run `standardize_eta_th.py` after the merge and confirm it touches concepts 19/25/27/36 — the ones main's regex misses).

---

## Integration Strategy

This item is gating for Items 3–5 of the ONTOLOGY-V3 epic. After this commit lands:

- **Item 3** (code-gap closure) operates against the v3 schema in our CSV with Mallory's `taxonomy_models.py` enums. It fixes the 9 holes the addendum already enumerated (`phase_2a/column_map.py`, `_HIERARCHY`, `ConfinementFamily` enum, Jinja templates, `neighborhood_graph.js`, `parameter_display_registry.yaml`, tests, `oneoff_3d_clustering.py::FUNDING_M_USD`/`CADENCE_BY_PREFIX`, scoring rerun).
- **Item 4** (resolve ontology decisions) resolves HB11 Ultrashort-vs-Fast-ignition and CSV-vs-MD authority for `Heating Type`/`Driver Type`. Translates the ontology docs to our IDs if needed.
- **Item 5** (new-concept analyses) runs `extract_explorer_data.py` and the analysis pipeline for 37/38/39 — and refreshes any existing concept whose classification flipped (04, 07, 13, 18, 22, 26+30, 27, 35).
- **Item 6** (cleanup) deletes Pranos directories and the `20-modular-hts-stellarator/` orphan.

No coordination is required with active modeling work — this commit is contained to `exploration/`.

---

## Validation Approach

Per spec acceptance criteria, plus design-specific:

1. **Verbatim checks (spec FR-2/FR-3)** — `git diff origin/fix/concept-renumbering-robustness -- <path>` returns empty for all files in the "verbatim pulled" list. **Adjusted: scoring.py and standardize_eta_th.py are expected to diff** — verify instead by reviewing their PR diff against `main` and confirming the canonical-params relocation is the only delta from Mallory's intent.
2. **CSV shape (FR-4 through FR-8)** — header check, row count = 40, ID set matches spec, no Pranos, two Inertia rows, row 22 First-Light-only.
3. **Mirror (FR-5)** — `cmp` returns success.
4. **Regen (FR-10/FR-11)** — `seed_registry.py` exits 0; `concept_registry.json` has 40 entries.
5. **`status` smoke (FR-12)** — exits 0.
6. **Non-renames (FR-13)** — `git diff --name-only --diff-filter=R main` empty for the two trees.
7. **No regenerated artifacts (FR-14, FR-15)** — `git diff --name-only main` shows no `synthesis.md`/`analysis.md`/`model_output.txt` paths, and only `concept_registry.json`+`decision_tree.json` under `concept_explorer/data/`.
8. **Translator idempotence (design-specific)** — enforced *inside* the script: after writing, re-read its own output and assert it is byte-identical to a second-pass result. No manual verification step needed.

Manual sanity check: spot-check these 3 rows in the output CSV:
- **`17a-laser-icf-hybrid-drive`** (Xcimer, renumbered from Mallory's 27 → our 17a — tests the renumber map).
- **`26-laser-icf-indirect-drive`** (Inertia — tests the 26/30 fan-out: v3 columns from Mallory's row 31, identity columns from our main row 26).
- **`37-magnetized-target-inertial-fusion-mtif`** (NearStar — tests new-row verbatim path).

---

## Next-Stage Handoff

**Plan must treat as fixed:**
- Single-commit, ~27-file scope.
- The 18-file verbatim list and the 2 synthesized-merge files (with the relaxed FR-2 wording for those 2).
- The generator script lives at `exploration/phase_1a/translate_csv_to_ours.py`.
- Mallory's CSV snapshot lives at `exploration/phase_1a/_mallory_table.csv` (checked in).
- `ID_MAPPING.md` is a standalone file at `exploration/phase_1a/ID_MAPPING.md` with a 2-line prepended note on `CONCEPT_ONTOLOGY.md`.

**Plan must figure out:**
- Phase ordering of the synthesized merges relative to the verbatim pulls (likely: verbatim pulls first, then synthesized, so the synthesized merge can be reviewed against a clean baseline).
- Exact commit message wording. Recommended subject: `feat: adopt ontology v3 schema, new concepts, and architecture-driven classification (no renumbering)`. Body summarizes the 4 buckets. Trailer: `Co-developed-with: Mallory Snowden <mallory.snowden@astera.org>`.
- Whether to refresh `_mallory_table.csv` snapshot just before commit (probably yes, single command).

**De-risk first:** run `seed_registry.py` on a draft CSV before committing anything else. If it errors on `Blanket Config` enum values, the design assumption that the schema swap is value-mappable row-by-row needs review.

---

**Next Step:** After approval → `/_my_plan`.
