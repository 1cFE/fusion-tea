# Spec: Ontology v3 Adoption (No Renumbering)

**Status:** Complete (implemented 2026-05-17, commit `8db3ed2` on `ontology-update`)
**Owner:** Reid W
**Created:** 2026-05-17
**Revised:** 2026-05-17 (strategy: adopt schema + code + new concepts only; keep existing IDs)
**Complexity:** MEDIUM-LOW
**Branch:** `ontology-update` (already exists off `main` @ `a8a779e`; planning commit `244ca24` already on branch)
**Epic:** ONTOLOGY-V3, Item 2

---

## Work Item Summary

Adopt the v0.3.0 ontology *content* (column schema + new concepts + code refactor + docs) from `origin/fix/concept-renumbering-robustness` (single commit `1b960a9` by Mallory, 2026-05-17), but **keep our existing concept IDs unchanged**. Mallory's branch renumbers 16 concepts; her renumbering was aesthetic (de-suffix `17a/b` / `20a/b`, compact after Pranos drop and Inertia dedup), not load-bearing. Her code refactor derives classification from CSV columns, not IDs — so IDs are free labels. Net effect: schema swap on `table.csv`, drop Pranos row, split combined-22 (First Light + NearStar) into our existing `22` (First Light) plus new `37` (NearStar), add `38` (SHINE) and `39` (ENN), pull her 12 authored code/doc files, no directory renames.

## Why This Matters Now

Mallory's branch has the v0.3.0 schema and the architecture-driven code refactor we want. Adopting her ID scheme would force ~30 directory renames in `analyses/` and `knowledge/concept_research/`, risk breaking external references (R2 paths, prior research, explorer JSON paths), and create unnecessary conflict with Item 1's standardization. By keeping our IDs and only pulling the *content* changes, we get the same v0.3.0 schema with a fraction of the mechanical work and a cleaner diff.

## Key Bets / Constraints

- **Bet:** Mallory's `lib/scoring.py` and `lib/concepts.py` refactors derive from CSV columns (`Confinement Family / MFE Topology / IFE Driver / MIF Method / Magnet Type`) plus slug overrides for z-pinch and levitated dipole — not from numeric ID prefix. Therefore our IDs work with her code as long as the CSV's classification columns are correct.
- **Bet:** Mallory's new ontology docs (`CONCEPT_ONTOLOGY.md`, `RECLASSIFIED_CONCEPTS.md`, etc.) reference her IDs. We accept that divergence in this item and add a one-page ID-mapping table; full doc-ID translation is deferred (probably Item 4 design work).
- **Bet:** The schema swap (`Plasma State` / `Tritium Breeding` / `Neutron Management` → `Blanket Config`) is value-mappable from Mallory's CSV row-by-row, even after relabeling IDs.
- **Constraint:** Our existing concept directories in `analyses/` and `knowledge/concept_research/` are not renamed. Item 1's standardization survives unchanged.
- **Constraint:** We keep concepts `26-laser-icf-indirect-drive` and `30-laser-icf-nif-commercialization` as **two separate rows** (Mallory deduplicated them into her `31`; we don't follow her here).
- **Non-goal:** Adopting Mallory's renumbering scheme.
- **Non-goal:** Pulling Mallory's regenerated `analyses/{ID}/synthesis.md` / `analysis.md` / `model_output.txt` / `iter-N/` artifacts. Item 5 refreshes synthesis for affected concepts.
- **Non-goal:** Pulling Mallory's `concept_explorer/data/{ID}.json` files. `extract_explorer_data.py` rebuilds them.
- **Non-goal:** Pulling Mallory's `scores/*.{json,md}` files (she flagged stale). Item 3 reruns scoring.
- **Non-goal:** Fixing the 9 code gaps from `.project/research/20260517_ontology_v3_delta.md` §Addendum. Item 3.

---

## Business Goals

### Why This Matters

Item 2 gates Items 3–5. The fastest path is to adopt only the content changes from Mallory's branch. Keeping our IDs avoids the bulk of the mechanical work, keeps Item 1's standardization in place naturally, and produces a small reviewable PR.

### Success Criteria

- [ ] `exploration/concept_analysis/table.csv` is at v3 schema (drops `Plasma State` / `Tritium Breeding` / `Neutron Management`, adds `Blanket Config`), uses **our existing IDs**, has 40 rows: 37 existing-minus-Pranos rows + 3 new rows (37 NearStar, 38 SHINE, 39 ENN).
- [ ] All 12 authored code files from Mallory's branch (lib refactor, explorer code, standardize_eta_th, rerun_all_models, taxonomy_models, seed_registry, similarity, JS) are on `ontology-update` at her content.
- [ ] All 9 new doc + generator files from `exploration/phase_1a/` are on `ontology-update`, with an added `ID_MAPPING.md` documenting where Mallory's IDs differ from ours.
- [ ] Combined-22 row (First Light + NearStar) is split: `22-projectile-icf` keeps First Light only; new row `37-magnetized-target-inertial-fusion-mtif` for NearStar.
- [ ] Pranos row dropped from CSV; Pranos directories left in place (flagged for Item 6 cleanup).
- [ ] `concept_research/20-modular-hts-stellarator/` orphan disposition decided and documented.
- [ ] No concept directories renamed in `analyses/` or `knowledge/concept_research/`.
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` runs to completion, producing a 40-concept `concept_registry.json`.
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` runs.
- [ ] One single commit on `ontology-update` (after planning commit `244ca24`), with attribution trailer.

### Priority

P0. Gates Items 3–5 of ONTOLOGY-V3.

---

## Problem Statement

### Current State

- `ontology-update` is at planning commit `244ca24` (off `main` @ `a8a779e`). Working tree is clean.
- `main` has 38 concept rows in `table.csv` (01–36 with subitems 17a, 17b, 20a, 20b; row 22 is combined "First Light Fusion, NearStar Fusion"; Pranos is at 34).
- `origin/fix/concept-renumbering-robustness` (commit `1b960a9`) has 39 rows under a different ID scheme.
- Mallory's renumbering (informational; we're not adopting):

| Mallory's ID | Our ID | Concept |
|---|---|---|
| 17 | 17b | Focused Energy |
| 20 | 20a | Type One |
| 21 | 20b | Renaissance |
| 22 | 21 | Tokamak Energy ST |
| 23 | 22 | First Light (NearStar split out) |
| 24 | 23 | Marvel |
| 25 | 24 | LPPFusion |
| 26 | 25 | Intensity Energy |
| 27 | 17a | Xcimer |
| 28 | 27 | EMC2 Polywell |
| 29 | 28 | Energy Singularity |
| 30 | 29 | Firefly NT |
| 31 | 26 + 30 | Inertia (Mallory deduped; we keep both) |
| 32 | 31 | Blue Laser OEC |
| 33 | 32 | GenF |
| 34 | 33 | Neo Fusion BEST |
| 37 | 37 | NearStar (new) |
| 38 | 38 | SHINE (new) |
| 39 | 39 | ENN (new) |

- Rows that don't change ID: 01–16, 18, 19, 35, 36.
- Pranos (Mallory: dropped; ours: 34): drop from CSV.

### Desired Outcome

A single commit on `ontology-update` containing:
1. v3-schema `table.csv` with our 40 rows.
2. 12 authored code files at Mallory's content.
3. 9 ontology docs + generators at Mallory's content, plus a new `ID_MAPPING.md`.
4. Regenerated `concept_registry.json` and `decision_tree.json`.

No directory renames. Pranos directories left in place. Mallory's regenerated artifacts not pulled.

---

## Scope

### In Scope

**Bucket A — Code, generators, and ontology docs (pull wholesale, no translation needed):**

Code (12 files):
- `exploration/concept_analysis/scripts/lib/scoring.py`
- `exploration/concept_analysis/scripts/lib/concepts.py`
- `exploration/concept_analysis/scripts/lib/claude.py`
- `exploration/concept_analysis/scripts/standardize_eta_th.py`
- `exploration/concept_analysis/scripts/rerun_all_models.py` (new)
- `exploration/concept_analysis/C2_SCORING.md` (new)
- `exploration/concept_explorer/taxonomy_models.py`
- `exploration/concept_explorer/seed_registry.py`
- `exploration/concept_explorer/similarity.py`
- `exploration/concept_explorer/static/js/taxonomy_card.js`
- `exploration/concept_explorer/static/js/view_categorical.js`
- `exploration/phase_1a/schema.md`

Docs + generators (8 files):
- `exploration/phase_1a/CONCEPT_ONTOLOGY.md`
- `exploration/phase_1a/CONCEPT_CATEGORIES_PROPOSAL.md`
- `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md`
- `exploration/phase_1a/SCHEMA_REVISION_PROPOSALS.md`
- `exploration/phase_1a/concept_ontology_v3.png`
- `exploration/phase_1a/generate_ontology_chart.py`
- `exploration/phase_1a/generate_ontology_md.py`

These reference Mallory's IDs. We pull them verbatim and accept the divergence (see Bucket C ID-mapping doc).

**Bucket B — CSV translation:**

Produce `exploration/concept_analysis/table.csv` (and its `exploration/phase_1a/table.csv` mirror) with:
- v3 column structure (Mallory's header): `ID, Research ID, Concept Name, Company, Confinement Family, MFE Topology, IFE Driver, MIF Method, Non-Standard Mechanism, Tokamak Shape, Stellarator Type, Laser Approach, Fuel, Primary Heating, Energy Capture, Magnet Type, Blanket Config, Operation Mode, Repetition Rate, Driver Technology, Overall Confidence`
- For each of the 37 existing-minus-Pranos concepts:
  - ID = our existing ID (per the table above)
  - Column values = Mallory's row for the equivalent concept (which has the v3 `Blanket Config` value plus revised vocabulary, e.g. Focused Energy moving to Direct Drive Fast Ignition; HB11 stays whatever Mallory has, etc.)
  - For our 26 (Inertia Indirect) and our 30 (Inertia NIF Commercialization): take Mallory's row 31 (deduplicated) for our 26; manually populate our 30 with the same Blanket Config and other v3 column values that Mallory's 31 carries (they're the same company concept), but keep the `Concept Name` and `Driver Technology` distinct as they are on `main`.
- For the 3 new concepts:
  - 37 NearStar, 38 SHINE, 39 ENN — copy Mallory's rows verbatim (her IDs already match what we want).
- For Pranos: drop entirely.

**Bucket C — Split row 22 and add ID-mapping doc:**

- Edit our row `22-projectile-icf`: change `Concept Name` from "Projectile ICF (D-T)" with company "First Light Fusion, NearStar Fusion" to just First Light Fusion (matching Mallory's row 23 content modulo the ID).
- Add a new row 37 for NearStar with Mallory's row 37 content.
- Add `exploration/phase_1a/ID_MAPPING.md` documenting the Mallory-to-ours ID translation (the table above), so future readers can reconcile.

**Bucket D — Regeneration:**

- After CSV is in place, run `uv run python exploration/concept_explorer/seed_registry.py` to regenerate `concept_registry.json` and `decision_tree.json`. Commit both.

### Out of Scope

- Pulling Mallory's regenerated `analyses/{ID}/synthesis.md`, `analysis.md`, `model_output.txt`, `iter-N/` content for the 35 renumbered concepts. None of these are pulled.
- Pulling Mallory's regenerated `concept_explorer/data/{ID}.json`. Not pulled.
- Pulling Mallory's `scores/*.{json,md}`. Not pulled.
- Renaming concept directories in `analyses/` or `knowledge/concept_research/`.
- Pranos directory cleanup. Left in place; Item 6 task.
- `concept_research/20-modular-hts-stellarator/` orphan cleanup. Verify and document; physical deletion deferred to Item 6 if uncertain.
- Populating `analyses/37/`, `analyses/38/`, `analyses/39/` for the new concepts. Item 5 runs the pipeline.
- Translating Mallory's ontology docs to our IDs (CONCEPT_ONTOLOGY.md, RECLASSIFIED_CONCEPTS.md). Deferred; ID-mapping doc suffices for now.
- Fixing `phase_2a/column_map.py`, `_HIERARCHY` in `seed_registry.py`, `ConfinementFamily` enum, Jinja templates, `neighborhood_graph.js`, `parameter_display_registry.yaml`, tests. Item 3.
- HB11 Fast-ignition vs Ultrashort decision. Item 4.
- `Heating Type` / `Driver Type` CSV-vs-MD decision. Item 4.

### Edge Cases & Considerations

- **Mallory's row 31 (Inertia, deduped) maps to two of our rows (26 + 30)**: take her column values (especially `Blanket Config`, `Primary Heating`, etc.) and apply to both. Keep our existing `Concept Name` / `Company` / `Driver Technology` text on each. If her row 31's `Concept Name` is e.g. "Laser ICF - Indirect Drive (D-T)" matching our 26 better than 30, just take that one and leave our 30's name as it is.
- **Mallory's row 23 (First Light only) maps to our row 22**: take her content but use our `22-projectile-icf` ID. Remove NearStar from the `Company` field.
- **Our row 22's `Driver Technology` says "Electromagnetic gun"**: Mallory's row 23 also says this. Keep.
- **Mallory's row 37 (NearStar) is wholly new**: take verbatim (her ID = 37 = our ID).
- **`concept_research/20-modular-hts-stellarator/` orphan**: Verify it has no unique content vs `20a/` and `20b/`. If empty/stale, delete in this item; otherwise leave and flag for Item 6.
- **The `Research ID` column**: Mallory populated it with the concept slug. Apply the same convention to our rows. For renumbered concepts, the Research ID Mallory used may correspond to a directory name that doesn't exist on our tree (e.g. her `27-laser-icf-hybrid-direct-drive` Research ID doesn't match our `17a-laser-icf-hybrid-drive` directory). Set our Research ID to match our actual directory slug.
- **`exploration/phase_1a/table.csv` is a mirror of the main `table.csv`**: keep them in sync (same content).
- **Mallory's regenerated files for renumbered concepts are simply not pulled**: this is the cleanest approach; do not attempt to merge anything.
- **Pranos in CSV vs directory**: dropping the row from CSV is mandatory; deleting the directory is optional (and deferred to Item 6). The seed_registry will still work because it iterates CSV rows, not directories.

---

## Requirement Selection Notes

Requirements below cover the post-execution invariants. The mechanics of CSV row-by-row translation (manual edit vs scripted vs hand-CSV-in-vim) and the exact format of the ID-mapping doc are intentionally left to design. Whether to run `extract_explorer_data.py` and whether to commit its rebuilt JSON files in this item is also design's call.

---

## Requirements

### Functional Requirements

> Requirements derive from the ONTOLOGY-V3 epic Item 2 (revised twice), and the strategy approved by the user on 2026-05-17.

1. **FR-1**: `ontology-update` MUST receive **exactly one commit** containing buckets A + B + C + D. The commit message MUST include a `Co-developed-with: Mallory Snowden <mallory.snowden@astera.org>` trailer or equivalent attribution prose.
2. **FR-2**: All 12 authored code files in Bucket A MUST be present at exactly the content of `origin/fix/concept-renumbering-robustness:1b960a9` for each path. Verifiable by `git diff origin/fix/concept-renumbering-robustness -- <path>` returning empty for each.
3. **FR-3**: All 7 doc/generator files in Bucket A (`CONCEPT_ONTOLOGY.md`, `RECLASSIFIED_CONCEPTS.md`, `CONCEPT_CATEGORIES_PROPOSAL.md`, `SCHEMA_REVISION_PROPOSALS.md`, `concept_ontology_v3.png`, `generate_ontology_chart.py`, `generate_ontology_md.py`) MUST be present at Mallory's content.
4. **FR-4**: `exploration/concept_analysis/table.csv` MUST:
   - Use the v3 column header from Mallory's CSV.
   - Have 40 data rows.
   - Have IDs from our existing scheme (01–36 incl. 17a, 17b, 20a, 20b) for the 37 existing-minus-Pranos rows, plus 37, 38, 39 for the new concepts.
   - Have no row for Pranos (`34-compact-spherical-tokamak-india`).
   - Have two distinct Inertia rows (our `26-laser-icf-indirect-drive` and our `30-laser-icf-nif-commercialization`).
5. **FR-5**: `exploration/phase_1a/table.csv` MUST be byte-identical to `exploration/concept_analysis/table.csv`.
6. **FR-6**: Our row 22 (`22-projectile-icf`) MUST have `Company` = First Light Fusion only (NearStar removed).
7. **FR-7**: A new row with ID `37-magnetized-target-inertial-fusion-mtif` MUST exist with NearStar's content per Mallory's row 37.
8. **FR-8**: New rows 38 (SHINE) and 39 (ENN) MUST exist with Mallory's content for those rows.
9. **FR-9**: `exploration/phase_1a/ID_MAPPING.md` MUST be created, documenting the Mallory-to-ours ID translation for the 16 concepts where IDs differ.
10. **FR-10**: `exploration/concept_explorer/data/concept_registry.json` MUST be regenerated and committed, MUST contain exactly 40 entries (matching the CSV).
11. **FR-11**: `exploration/concept_explorer/data/decision_tree.json` MUST be regenerated and committed.
12. **FR-12**: `uv run python exploration/concept_analysis/scripts/run_analysis.py status` MUST exit 0.
13. **FR-13**: No directory under `exploration/concept_analysis/analyses/` or `knowledge/concept_research/` is renamed in this commit. Verifiable by `git diff --name-only --diff-filter=R main` returning empty for those trees.
14. **FR-14**: No regenerated `analyses/{ID}/synthesis.md`, `analysis.md`, `model_output.txt`, or `iter-N/` files are committed. Verifiable by `git diff --stat` showing zero file changes under `analyses/{any}/synthesis.md` etc.
15. **FR-15**: [INFERRED] No `scores/*.{json,md}` or `concept_explorer/data/{ID}.json` files are touched in this commit. Verifiable by `git diff --name-only` showing none of those paths.

### Non-Functional Requirements

- **NFR-1**: The execution MUST complete in a single working session (≤2 hours).
- **NFR-2**: The commit diff MUST be reviewable in a small PR. Expected size: ~25 files (12 code + 8 docs + 1 mapping + 2 CSV + 2 generated JSON).

---

## Acceptance Criteria

### Code, docs, generators (Bucket A)

- [ ] `git diff origin/fix/concept-renumbering-robustness -- exploration/concept_analysis/scripts/lib/scoring.py` returns empty.
- [ ] Same for `lib/concepts.py`, `lib/claude.py`, `standardize_eta_th.py`, `rerun_all_models.py`, `C2_SCORING.md`.
- [ ] `git diff origin/fix/concept-renumbering-robustness -- exploration/concept_explorer/taxonomy_models.py` returns empty.
- [ ] Same for `seed_registry.py`, `similarity.py`, `static/js/taxonomy_card.js`, `static/js/view_categorical.js`.
- [ ] Same for the 7 doc/generator files in `exploration/phase_1a/`.

### CSV (Bucket B + C)

- [ ] `head -1 exploration/concept_analysis/table.csv` matches Mallory's v3 header (contains `Blanket Config`, no `Plasma State` / `Tritium Breeding` / `Neutron Management`).
- [ ] `wc -l exploration/concept_analysis/table.csv` prints 41 (header + 40 rows).
- [ ] `awk -F, 'NR>1 {print $1}' exploration/concept_analysis/table.csv | sort` contains all our IDs (01 through 36 incl. 17a/b, 20a/b, except 34) plus 37, 38, 39.
- [ ] No row with ID `34-compact-spherical-tokamak-india`.
- [ ] Two distinct Inertia rows (`26-laser-icf-indirect-drive` and `30-laser-icf-nif-commercialization`).
- [ ] Row `22-projectile-icf` has `Company` containing First Light only (no "NearStar").
- [ ] Row `37-magnetized-target-inertial-fusion-mtif` exists.
- [ ] `cmp exploration/concept_analysis/table.csv exploration/phase_1a/table.csv` returns success (byte-identical).
- [ ] `exploration/phase_1a/ID_MAPPING.md` exists and documents all 16 ID differences.

### Regeneration (Bucket D)

- [ ] `uv run python exploration/concept_explorer/seed_registry.py` exits 0.
- [ ] `python -c "import json; d=json.load(open('exploration/concept_explorer/data/concept_registry.json')); print(len(d['concepts']))"` prints `40`.
- [ ] `concept_registry.json` and `decision_tree.json` are staged and committed.

### Out-of-scope verifications

- [ ] `git diff --name-only --diff-filter=R main -- exploration/concept_analysis/analyses/ knowledge/concept_research/` returns empty (no renames).
- [ ] `git diff --name-only main -- 'exploration/concept_analysis/analyses/**/synthesis.md' 'exploration/concept_analysis/analyses/**/analysis.md' 'exploration/concept_analysis/analyses/**/model_output.txt'` returns empty.
- [ ] `git diff --name-only main -- 'exploration/concept_analysis/scores/' 'exploration/concept_explorer/data/*.json'` shows only `concept_registry.json` and `decision_tree.json`, not per-concept `{ID}.json`.
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` exits 0.

### Commit hygiene

- [ ] One single commit on `ontology-update` after `244ca24`.
- [ ] Commit message includes `Co-developed-with: Mallory Snowden` trailer.

---

## Next-Stage Handoff

**Settled in this spec:**
- Adopt schema, code, docs, new concepts; keep our existing IDs.
- Pranos row dropped; Pranos directories left in place.
- 26 + 30 stay as two distinct Inertia rows.
- Split 22 into First Light (our 22) + NearStar (new 37).
- New IDs for SHINE = 38, ENN = 39.
- Mallory's renumbered ontology docs pulled verbatim; ID-mapping doc compensates.
- No directory renames. Mallory's regenerated artifacts not pulled.
- Single commit with attribution trailer.

**Design must figure out:**
- Mechanics of CSV translation: hand-edit, generate via a one-off script that reads Mallory's CSV and rewrites IDs, or use a tabular tool. Recommend a small Python script that's checked in under `exploration/phase_1a/` next to the other generators — it's the kind of thing we'll want to rerun if Mallory's branch evolves.
- The exact column-by-column mapping for the 26/30 split case (Mallory's 31 → our 26 + 30): which columns get copied to both vs which stay distinct.
- Disposition of `concept_research/20-modular-hts-stellarator/`: verify content overlap with 20a/20b, decide delete-now vs defer-to-Item-6.
- Whether the new `ID_MAPPING.md` lives at `exploration/phase_1a/ID_MAPPING.md` or alongside Mallory's `RECLASSIFIED_CONCEPTS.md` or as a section appended to that file. Recommend standalone file for clarity.
- Whether to also append a note at the top of Mallory's `CONCEPT_ONTOLOGY.md` pointing readers to the ID mapping. Recommend yes — a single 2-line note.
- Exact commit message form (subject + body + trailer).

**Watch-outs for design:**
- Mallory's CSV rows for the renumbered existing concepts may have updated value vocabulary (e.g. revised `Primary Heating` strings) that we want to adopt verbatim — translation is ONLY the ID column, not the other columns. Don't accidentally rewrite values.
- Some of Mallory's classification revisions for existing concepts (e.g. HB11 might land as Ultrashort in her CSV vs. Fast ignition on `main`) are intentional and part of the v3 adoption. Item 4 will resolve any inconsistencies between her CSV and her docs; this item just propagates her CSV values as authored.
- The `Research ID` column needs special care: Mallory populated it with her slug naming. We need to set it to our slug naming. For renumbered concepts whose slugs differ, this means the Research ID won't match Mallory's value — use our existing directory slug.
- The CSV translation script (if used) needs to handle that Mallory's row 23 (First Light) maps to our 22, AND that NearStar from her 37 needs to be its own row in ours (also at 37). Inertia 31 maps to our 26 *and* our 30. So the script isn't a pure one-to-one row rewrite — it has branching logic for those two cases.
- After regeneration, `concept_registry.json` may surface validation errors against enum updates (e.g. `Blanket Config` values, dropped Plasma State). That's expected; if it blocks `seed_registry.py` from completing, log the errors and escalate. If it just warns, proceed.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_ontology_v3_migration.md` (Item 2)
- **Research:** `.project/research/20260517_ontology_v3_delta.md`
- **Source branch:** `origin/fix/concept-renumbering-robustness` @ `1b960a9` (Mallory, 2026-05-17) — cherry-picked file-by-file, not merged
- **Baseline:** `main` @ `a8a779e`
- **Planning commit:** `244ca24` (already on `ontology-update`)
- **Design (to be created):** `.project/active/ontology-v3-merge/design.md`
- **Plan (to be created):** `.project/active/ontology-v3-merge/plan.md`

---

**Next Steps:** After approval, proceed to `/_my_design`. Design must resolve the CSV translation mechanics, the 26/30 column-mapping detail, the orphan-directory disposition, and the exact commit message.
