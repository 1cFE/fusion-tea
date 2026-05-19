# Merge Analysis: `concept-downselect` → `main`

**Date:** 2026-05-19
**Worktree:** `/home/reid/1cfe/fusion-tea-concept-downselect`
**Branch:** `concept-downselect` (clean, up to date with `origin/concept-downselect`)
**Merge base:** `704a3a5` (multiple bases — concept-downselect already absorbed `main` once via `e9d5de2` up to `833c863`)

The branches have diverged substantially. The symmetric diff touches **2,086 files / +109,843 / −44,681 lines**. A direct merge will produce hundreds of conflicts, dominated by one structural collision: **both branches restructured the concept corpus, but in incompatible ways**.

---

## 1. What landed on `main` since `concept-downselect` last synced

`concept-downselect` already merged `main` at `e9d5de2` (carrying main up to `833c863`). Since then, **27 commits** landed on `main`, in three coherent waves:

### Wave A — Sensitivity-sliders PR completion (`8e28088`, `240613e`)
Merge of `sensitivity-sliders` PR #14. Already-known UI work; not relevant to corpus.

### Wave B — Data hygiene on existing concepts (`2055cdb` → `9851b7e`)
Eight small fixes against the **then-current 38-concept old-ID scheme**:
- `2ab95bf` — concept 28 `structure_t/vessel_t` mislabel
- `ebcf1c3` — `eta_th` category-mapping fix on concepts **06, 07, 34**
- `45c9db5` — plant availability standardization on 13 D-T concepts
- `50081cc` — stale availability strings in concept **28**
- `6ba8f02` — `mn` standardization on D-T concepts
- `9851b7e` — `lifetime_yr` standardization
- `2055cdb` — `--feedback` flag refactor (pipeline tooling)

All keyed on **old concept IDs** (e.g., 28, 34) — many of which `concept-downselect` has relabeled or dropped.

### Wave C — Ontology v3 epic, PR #16 (`97828dc` → `8d59784`)
The big one. 16 commits planning + implementing a v3 ontology migration. Key commit `6d32f4d`: "adopt ontology v3 schema, new concepts, and architecture-driven classification (**no renumbering**)".

What main's v3 PR did:
- Adopted v0.3.0 ontology *content* from `origin/fix/concept-renumbering-robustness` (Mallory Snowden, `1b960a9`) — **without** her renumbering.
- New CSV column schema: **added** Heating Type, Driver Type, Blanket Config; **dropped** Plasma State, Tritium Breeding, Neutron Management.
- `phase_1a/translate_csv_to_ours.py` rewrites Mallory's CSV onto the *existing* (pre-downselect) ID scheme.
- Drops Pranos (old-34); emits Mallory's First Light row as our 22; fans Inertia onto our 26 + 30; emits 37/38/39 verbatim. Final: **40-row table.csv** (header + 40 data rows, but Pranos dropped → 39 concepts).
- 13 verbatim file pulls from Mallory: `lib/concepts.py`, `lib/claude.py`, `rerun_all_models.py`, `taxonomy_models.py`, `seed_registry.py`, `similarity.py`, two `static/js/*.js` views, and 6 `phase_1a/` docs incl. `CONCEPT_ONTOLOGY.md`, `RECLASSIFIED_CONCEPTS.md`, `SCHEMA_REVISION_PROPOSALS.md`, `concept_ontology_v3.png`.
- Architecture-driven `_C2`/`_HERITAGE` classification in `scoring.py`.
- Regenerated `concept_registry.json`, `decision_tree.json`.
- Subsequent commits (`db24808`, `fff5c18`, `6558cf6`, `f8740cd`) wire the new Heating Type / Driver Type columns through `phase_2a/column_map.py` and parsers; `42d04b2` refactors analysis CADENCE/TREE_PATH; `029b3ab` regenerates `verified_scores`; `2ed0be7` runs new concepts.

---

## 2. What `concept-downselect` did

**13 commits**, four coherent chunks of work:

### Chunk 1 — Downselect research & methodology (`6eb2291`, `539a1b5`, `57ece9e`, `1d9937a`, `ab19c2a`, `f7f5da8`, `e7964c8`)
Pure research + an HTML explainer (`docs/demo/down-select.html`). Adds:
- `knowledge/concept_research/{megaprojects, what_is_foak, experience_rate_overestimates, ...}/` — 4 new meta-analysis sources.
- `.project/concepts/down_select/` — methodology research, worked examples, traces.
- `.project/concepts/scoring-framework-v2.md` — proposes the V2 scoring rubric.

**Conflict risk: LOW.** Disjoint paths from main.

### Chunk 2 — Wurzel & Hsu paper (`8585ddd`)
Ingests `knowledge/concept_research/<wurzel-hsu>/`. New paths only. **Conflict risk: NONE.**

### Chunk 3 — Scoring V2 framework (`f55e35a`, `30ecdd8`)
New top-level module `exploration/scoring_v2/` (features/embeddings/lib/extract.py/score.py) plus `tests/scoring_v2/`. **Main has no `exploration/scoring_v2/` directory** — pure addition.
**Conflict risk: NONE on the new module itself.** *But* the feature YAMLs are keyed on the new 39-ID scheme, which collides with main's old IDs (see Chunk 4).

### Chunk 4 — 38→39 corpus renumber + 3 net-new concepts (`e23fceb` tooling, `a2004fa` corpus)
**This is the conflict epicenter.** Both commits authored by **Mallory Snowden** on this branch — the same renumber work whose *content* (without the renumber) was selectively pulled onto `main` via PR #16.
- New tool `scripts/renumber/renumber.py` (826 LOC) plus crosswalk, manifest, inventory, r2_ops log.
- WS-1B work item docs.
- Renumber rules (from `scripts/renumber/crosswalk.csv`):
  - **Unchanged (20 concepts):** 01–16, 18, 19, 35, 36.
  - **Dropped (2):** old-30 (Inertia NIF-commercialization, redundant), old-34 (Pranos India).
  - **Relabeled (16):** 17a→17 (Focused Energy, fast-ignition), 17b→27 (Xcimer hybrid-direct), 20a→20, 20b→21, 21→22, 22→23, … 33→34. Each relabeled row gets `Research ID` pinned to old slug so the existing research dirs stay in place.
  - **Net-new (3):** 37 NearStar MTIF, 38 SHINE accelerator-driven, 39 ENN CS-free p-B11 ST.
- Re-analyzes Focused Energy (17) and Xcimer (27) on the *split* 17 dossier.
- Regenerates `table.csv`, `scoring.py` (`_C2`/`_HERITAGE` remapped), feature YAMLs (39 taxonomy / 28 cost-model), scoring_v2 scores, explorer registry, decision tree, SOURCE_INDEX.
- Rename impact (per `git diff --name-status -M`): **124 R100 (renames) + 284 A + 66 M** under `exploration/concept_analysis/analyses/`.

---

## 3. Structural conflicts & inconsistencies

| Area | `main` | `concept-downselect` | Resolution required |
|---|---|---|---|
| **Concept ID space** | 40-row table, keeps old IDs (17a, 17b, 20a, 20b, 21–33 unchanged), drops Pranos, adds 37/38/39 verbatim from Mallory's source branch | 39 concepts, renumbered by Mallory (17a→17, 17b→27, 20a→20, 20b→21, 21→22 … 33→34), drops old-30 + old-34, adds own 37/38/39 | **Pick one ID scheme.** Same author (Mallory) produced the renumber; `main`'s PR #16 chose to pull her content *without* the renumber. Decision is whether to reverse that. |
| **`table.csv`** | v3 schema (Heating Type / Driver Type / Blanket Config added; Plasma State / Tritium Breeding / Neutron Management dropped). 40 rows. | Old schema. 39 rows. Different row identities. | Cell-by-cell merge impossible — must regenerate downselect's CSV under v3 schema *after* renumber decision. |
| **`exploration/concept_analysis/analyses/`** | In-place edits to `eta_th`, `availability`, `mn`, `lifetime_yr`, `structure_t/vessel_t`, plus regenerated `analysis.md` for several concepts | Many directories renamed (e.g., `17a-laser-icf-hybrid-drive/` → `27-laser-icf-hybrid-direct-drive/`; `21-spherical-tokamak-hts/` → `22-…/`; etc.) and content edited | Renames vs in-place edits → git rename detection (R100) helps for unmodified, but for concepts where main *also* edited content (06, 07, 28, 34, …) we get **rename-with-conflict**. Concepts main fixed (28 `structure_t`; 34 `eta_th`) sit on rows downselect renumbered or dropped. |
| **`knowledge/concept_research/`** | New meta-analysis dirs only | Pure additions (4 meta + Wurzel paper) — no concept-dir renames; downselect's renumber kept research dirs stable via Research ID pinning | LOW direct conflict; but the `SOURCE_INDEX.md` was regenerated on both sides → text conflict. |
| **`scoring.py`** | Main: architecture-driven `_C2`/`_HERITAGE` classification (from Mallory) | Downselect: `_C2`/`_HERITAGE` table remapped to 39-ID scheme | Must apply main's architecture-driven logic *and* downselect's ID remap. Mechanical text merge will collide; semantic merge required. |
| **`exploration/concept_analysis/lib/`** | Main pulls in Mallory's `concepts.py`, `claude.py`, `taxonomy_models.py`, `seed_registry.py`, `similarity.py` | Downselect uses pre-v3 versions | Take main's; verify downselect made no edits to these files. |
| **`phase_1a/` artifacts** | New: `CONCEPT_ONTOLOGY.md`, `RECLASSIFIED_CONCEPTS.md`, `SCHEMA_REVISION_PROPOSALS.md`, `ID_MAPPING.md`, `translate_csv_to_ours.py`, `_mallory_table.csv`, `concept_ontology_v3.png`, `generate_ontology_*.py` | Untouched | Take main's wholesale. |
| **`phase_2a/column_map.py`** | Added Heating Type + Driver Type | Untouched | Take main's. |
| **`exploration/scoring_v2/`** | Does not exist | New module + features + tests | Take downselect's, **then re-key feature YAMLs to whichever ID scheme wins**. |
| **`verified_scores` regen (`029b3ab`)** | Against v3 classifier on main's IDs | Against downselect's 39-ID classifier | Re-regenerate post-merge. |
| **Net-new 37/38/39** | Main: from Mallory (verbatim CSV rows; minimal analysis content) | Downselect: deeply analyzed with sources, LCOE runs, `concept_research/{37,38,39}/iter-01/` populated | **Downselect's are richer** — prefer downselect content; reconcile CSV row identity with main's schema. |
| **R2 binaries** | Untouched | Renumber left orphans (per `r2_ops.log`); not yet reconciled | Out of scope for this merge but pending. |

### Specific double-touches on the same data

Main's data-hygiene wave (Wave B) edited concepts that downselect renumbered/dropped:
- `ebcf1c3` (eta_th) → concept **34** is *dropped* on downselect (Pranos); 06/07 are unchanged on downselect → those fixes apply cleanly to 06/07, lost for 34.
- `2ab95bf`, `50081cc` (concept 28) → on downselect, **old-28 (Energy Singularity HTS-tokamak)** became **new-29**. Fix must be re-targeted.
- `45c9db5`, `6ba8f02`, `9851b7e` (13 D-T concepts) → some are renumbered (21→22, 22→23, …, 33→34, 17a→17, 17b→27, 20a→20, 20b→21, 28→29, 29→30); the fixes need ID remapping.

---

## 4. Merge strategy options

### Option A — Direct merge of `concept-downselect` into `main`

**Feasibility: LOW. Not recommended.**

Expected mechanics:
- Git will detect ~124 renames (R100) cleanly, but for the ~16 relabeled concepts where main *also* changed content, you get **modify/rename conflicts** that git resolves badly (often leaves both old and new paths populated).
- `table.csv` will conflict end-to-end (different schemas, different rows, different identities).
- `scoring.py`, `concepts.py`, `seed_registry.py` will conflict heavily.
- `SOURCE_INDEX.md` will conflict (both regenerated).
- `concept_registry.json` and `decision_tree.json` will conflict (both regenerated, mutually exclusive ID schemes).
- Final tree will be internally inconsistent (CSV says 40 rows under v3 schema; analyses/ dirs partly renamed; scoring.py partly remapped) — practically un-fixable in a single conflict resolution pass.

**Verdict:** A "resolve as you go" merge here means re-deriving downselect's renumber on top of main's v3 schema by hand, file by file. That's not a merge — it's a re-implementation disguised as one, with poor reviewability.

### Option B — Cherry-pick by chunk, with deterministic re-derivation of the renumber

**Feasibility: HIGH. Recommended.**

Treat downselect's 13 commits as four logical PRs against current `main`:

1. **PR-1: Research + downselect methodology** *(low risk, low conflict)*
   Cherry-pick: `6eb2291`, `539a1b5`, `57ece9e`, `1d9937a`, `ab19c2a`, `f7f5da8`, `e7964c8`, `8585ddd`.
   Squash into one commit: "Concept-downselect methodology, research, and explainer". Paths are mostly disjoint from main's changes — expect clean cherry-picks; only `docs/demo/down-select.html` may conflict with main's docs work; spot-check.

2. **PR-2: Scoring V2 framework + slice 1 + slice 2** *(structural addition; deferred ID re-key)*
   Cherry-pick: `f55e35a`, `30ecdd8`.
   Conflict locus: `exploration/scoring_v2/features/*.yaml` are keyed to the 39-ID scheme. Either (a) cherry-pick the feature YAMLs in their old-ID form first (since we have not yet renumbered, this is the consistent state) and re-key after PR-3, or (b) cherry-pick with the 39-ID YAMLs and accept temporary mismatch with `table.csv` until PR-3. Recommend (a): re-derive scoring_v2 features against current main's IDs in a single deterministic pass, since the underlying taxonomy values are unchanged for the 20 unchanged concepts.

3. **PR-3: Renumber decision** — *this is the negotiation point.*
   Two sub-options:
   - **B.3.a Adopt main's "no-renumber" position.** Drop the renumber commits (`e23fceb`, `a2004fa`). Keep downselect's 3 net-new concept analyses (37/38/39) and the split-17 reanalysis (Focused vs Xcimer) by porting them onto main's existing ID scheme: under main, 17a stays 17a, 17b stays 17b, 27 is still empty for downselect's Xcimer. This means dossier-split + re-analyses port cleanly but the *renumber itself* is abandoned.
   - **B.3.b Honor the renumber on top of main.** Re-run `scripts/renumber/renumber.py` (cherry-pick tooling first via `e23fceb`) against post-main state. The tool is deterministic (per `inventory.md`), reads `crosswalk.csv`, and writes table.csv + relabels analyses/ dirs + remaps scoring.py. This re-derivation produces a single clean commit instead of the half-merged mess from option A. Then re-apply main's Wave-B fixes (eta_th/availability/mn/lifetime) via remap-on-IDs.

   **Recommend B.3.a** unless there is a strong external reason for renumbering: main already pulled Mallory's content *without* renumbering as an explicit decision (`6d32f4d`), Mallory's ID_MAPPING.md formalizes the mapping, and abandoning the renumber removes the largest source of downstream churn for the analyses/ tree and R2.

4. **PR-4: Net-new concept analyses + split-17 reanalysis** *(content port)*
   The valuable artifacts from `a2004fa` that we want regardless of renumber: the three new concept dossiers + analyses for NearStar (MTIF), SHINE, ENN; and the re-analyzed Focused Energy + Xcimer on the split-17 dossier. Port these onto whichever ID scheme PR-3 picked, with fresh commits.

### Option C — Hybrid: reset-and-replay

**Feasibility: MEDIUM, only if Option B's PR-3 lands on B.3.b.**

`git reset --hard main` on the worktree, then re-run `renumber.py` and re-stage downselect's net-new content as fresh commits. Cleanest history if we *are* keeping the renumber, but throws away the existing review trail on the 13 commits.

---

## 5. Recommendation

**Option B with PR-3 = B.3.a (drop the renumber).**

Rationale:
- `main`'s PR #16 (`6d32f4d`, authored by you) deliberately took Mallory's ontology-v3 *content* but left her renumber behind ("no directory renames in analyses/ or knowledge/concept_research/"). Merging `concept-downselect` as-is would silently reverse that decision and reintroduce the renumber via the back door.
- B.3.a confines the conflict surface to ~4 small PRs of disjoint or near-disjoint paths.
- The downselect work that has real durable value — downselect *methodology*, the *V2 scoring framework*, the *3 new concept analyses*, the *split-17 reanalysis*, the *meta-analysis research dossiers* — all survives the renumber being dropped. Only the ID-relabel cosmetics are sacrificed.
- R2 reconciliation pending on downselect (per `a2004fa` commit message) goes away entirely if the renumber is dropped.

If we *do* want to renumber, B.3.b is the right way to do it: re-run the deterministic tool on post-main state and produce a single clean commit, rather than fighting git's three-way merge through 200+ rename conflicts.

---

## 6. Suggested sequencing

1. Cut a temporary integration branch off `main`: `git checkout -b concept-downselect-rebase main`.
2. Cherry-pick PR-1 (research/methodology, 8 commits) → squash → commit.
3. Cherry-pick PR-2 (scoring_v2 framework, 2 commits) → spot-fix feature YAML IDs → commit.
4. **Decision gate (user):** B.3.a or B.3.b on the renumber. Document choice in `.project/research/`.
5. Port PR-4 content (new 37/38/39 + split-17 reanalysis) onto the chosen ID scheme.
6. Open PR vs `main`; run validation (`uv run agentic-mbse status`, scoring_v2 tests, run_analysis.py status).
7. Update `MEMORY.md` with the renumber decision; drop or close `WI-1B` per outcome.
