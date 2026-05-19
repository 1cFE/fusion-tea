# Spec: concept-downselect Merge (Option B.3.a — drop renumber)

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-19 11:59
**Complexity:** HIGH
**Branch:** TBD (working branch off `main`, e.g. `concept-downselect-rebase`)

---

## Work Item Summary

Integrate the durable work from the `concept-downselect` branch into `main` *without* reintroducing Mallory's 38→39 renumber. The renumber was deliberately stripped from `main` in PR #16 (`6d32f4d`); merging `concept-downselect` as-is would silently reverse that decision. "Done" means: every piece of research, methodology, scoring infrastructure, new-concept analysis, and split-17 reanalysis on `concept-downselect` lives on `main` under main's existing concept-ID scheme, with no data, code, or functionality lost — and the pipeline still validates green.

## Why This Matters Now

The two branches have diverged by ~2,000 files. The longer we wait, the harder reconciliation gets, and the V2 scoring framework + new concept analyses (37/38/39) + downselect methodology are blocked from being usable on `main` until this lands. A bad merge would either lose research artifacts, corrupt the ID space, or quietly re-renumber the corpus. We need a deliberate, auditable port.

## Key Bets / Constraints

- **Bet:** Mallory's 38→39 renumber is *not* worth carrying forward. PR #16 already made this call; this spec ratifies it.
- **Bet:** Cherry-pick-by-chunk produces a cleaner, more reviewable result than `git merge` across this divergence.
- **Constraint:** Main's existing concept-ID scheme (with 17a, 17b, 20a, 20b, 21–33 unchanged; Pranos dropped; 37/38/39 added via Mallory's CSV translate) is the canonical ID space after this merge.
- **Constraint:** No file or commit on `concept-downselect` representing original research, analysis, or new code may be silently dropped. Anything intentionally not ported MUST be explicitly listed and justified in the implementation notes.
- **Constraint:** `main`'s v3 CSV schema (Heating Type / Driver Type / Blanket Config added; Plasma State / Tritium Breeding / Neutron Management dropped) is preserved as-is. Downselect artifacts ported in must conform.
- **Non-goal:** This work item does NOT re-decide the renumber. If we ever want it, that is a separate work item using `scripts/renumber/renumber.py` against post-merge `main`.
- **Non-goal:** R2 binary reconciliation for renumber orphans. The renumber is dropped, so the orphan problem evaporates; no R2 op required.
- **Non-goal:** New domain work. This is a port-and-reconcile; no new analyses, no new sources beyond what's already on `concept-downselect`.

---

## Business Goals

### Why This Matters

Real durable value sits on `concept-downselect`:
- A complete downselect methodology + worked examples + HTML explainer.
- The full Wurzel & Hsu paper and several meta-analysis dossiers (megaprojects, FOAK, experience-rate-overestimates).
- A new `exploration/scoring_v2/` module (features → embeddings → weights pipeline, 12 features, 4+7 embeddings, 26 passing tests).
- Three deeply-researched net-new concepts (NearStar MTIF, SHINE accelerator-driven, ENN p-B11 ST) with source-grounded LCOE runs.
- A split of the shared 17 dossier into separate Focused Energy and Xcimer analyses.

None of it is usable from `main` until this merge lands.

### Success Criteria

- [ ] All non-renumber work on `concept-downselect` exists on `main` after merge.
- [ ] Concept ID scheme on `main` is unchanged by this merge (zero directory renames in `exploration/concept_analysis/analyses/` or `knowledge/concept_research/`).
- [ ] Pipeline validation passes post-merge (see Acceptance Criteria).
- [ ] Every artifact on `concept-downselect` that we chose not to port is explicitly enumerated and justified in implementation notes.
- [ ] An auditable trail exists: each ported chunk is a separate commit (or small commit series) with a clear message naming what it ported and from which source commit(s).

### Priority

P0 — blocks downstream use of scoring_v2 and the new concepts on `main`.

---

## Problem Statement

### Current State

- `main` carries 27 commits (sensitivity-sliders PR completion, Wave B data hygiene, the ontology-v3 PR #16, and follow-up Heating/Driver wiring) that `concept-downselect` has not absorbed since its last `main` merge (`e9d5de2`).
- `concept-downselect` carries 13 commits in four logical chunks (research/methodology, Wurzel paper, scoring V2, renumber+net-new), authored by Reid and Mallory.
- The two branches' restructurings of the concept corpus are incompatible: Mallory renumbered 16 concepts on `concept-downselect`; PR #16 on `main` deliberately kept the old IDs.
- A direct `git merge` would produce hundreds of modify/rename conflicts on `analyses/`, full-file conflicts on `table.csv`, `scoring.py`, `concepts.py`, and the registry JSON files, with an internally inconsistent result tree.

### Desired Outcome

`main` carries the union of:
- Everything currently on `main`, unchanged.
- All `concept-downselect` artifacts in chunks 1, 2, and 4 (research, Wurzel, scoring V2 framework, net-new 37/38/39 analyses, split-17 reanalysis), translated onto `main`'s ID scheme and v3 CSV schema where they touch those structures.

The renumber tooling (`scripts/renumber/renumber.py` and its companion files) stays on `concept-downselect` history only; it is not ported to `main`.

---

## Scope

### In Scope

- Identifying every file and concept change on `concept-downselect` that is not the renumber itself.
- Porting research artifacts (Chunk 1): `knowledge/concept_research/` meta-analysis dossiers, `.project/concepts/down_select/`, `.project/concepts/scoring-framework-v2.md`, `.project/concepts/concept-trace.md`, `docs/demo/down-select.html`, and worked-example scripts/markdown.
- Porting the Wurzel & Hsu paper (Chunk 2).
- Porting the entire `exploration/scoring_v2/` module + `tests/scoring_v2/` (Chunk 3).
- Porting the three net-new concept analyses (Chunk 4 carve-out): NearStar MTIF, SHINE, ENN — under main's IDs 37/38/39 (which already exist as Mallory-CSV stubs).
- Porting the split-17 reanalysis content: Focused Energy under main's `17b-laser-icf-fast-ignition` (or whatever main currently labels Focused Energy), Xcimer under main's `17a-laser-icf-hybrid-drive` (or its main equivalent). Final mapping decided during implementation by reading main's current state.
- Reconciling `scoring_v2/features/*.yaml` keys to main's IDs.
- Reconciling `SOURCE_INDEX.md` regeneration.
- Capturing the renumber crosswalk (`scripts/renumber/crosswalk.csv`) on `main` as a historical record only (no executable tooling), so we have an audit of what Mallory intended.

### Out of Scope

- `scripts/renumber/renumber.py` and its run-time companions (`manifest.json`, `manifest.diff.txt`, `inventory.md`, `r2_ops.log`, `reanalyze.txt`).
- Re-applying main's Wave B data-hygiene fixes onto any "renumbered" IDs — no renumber happens, so no remapping needed.
- The R2 binary orphan cleanup mentioned in `a2004fa`'s commit message.
- Any new analysis, new source, or new feature not already present on `concept-downselect`.
- Deleting the `concept-downselect` branch (decide separately after merge lands).

### Edge Cases & Considerations

- **17a/17b identity on main.** Main keeps both `17a-laser-icf-hybrid-drive` (Xcimer) and `17b-laser-icf-fast-ignition` (Focused Energy). Downselect's split-17 reanalysis renamed these as 17 (Focused) and 27 (Xcimer). When porting the *content* (re-analyzed LCOE, source-grounded prompts, iter dirs), it must land on main's 17a/17b directories, not on new 17/27 directories.
- **Net-new 37/38/39 already exist on main as Mallory-CSV stubs.** Downselect's 37/38/39 are the *full analyses*. Porting must overlay/replace stubs with full content, preserving any per-row CSV metadata main already set (Concept Name, Company, Driver Technology, Research ID, plus the new v3 columns).
- **scoring_v2 feature YAMLs are keyed by ID.** Downselect generated 39 YAMLs against the renumbered scheme. On main, the 16 renumbered IDs are different (e.g., main has 21-spherical-tokamak-hts, downselect has 22-spherical-tokamak-hts). Each YAML must be either renamed to main's ID OR regenerated via `exploration/scoring_v2/extract.py --bulk-taxonomy` against main's `table.csv`. Both approaches are acceptable; regeneration is preferred because the taxonomy values main holds may differ from downselect's (v3 schema introduced new columns).
- **`scoring.py` `_C2`/`_HERITAGE` tables.** Downselect remapped these to its 39-ID scheme. Main has Mallory's *architecture-driven* C2 classification. Take main's version; do not port downselect's table remap (the remap exists only to compensate for the renumber that we are dropping).
- **`docs/demo/down-select.html`.** Downselect heavily edited it across 4 commits. Main may also have touched neighboring `docs/demo/` files. Port downselect's final version; spot-check no main edits collide.
- **Pranos (old-34).** Both branches drop it. Confirm main's drop is already in place; no action needed beyond verification.
- **`uv.lock`.** Both branches touch it heavily. Resolve by running `uv sync` post-merge against the union of dependencies, not by manual conflict resolution.
- **WS-1B work item.** `work/active/WI-1B_concept-reanalysis-and-net-new/` exists on `concept-downselect` to track the split + net-new reanalysis. It is still valid as a tracking artifact (the *work* of analyzing 37/38/39 + split-17 happened); port it. Close it once the analyses are ported.

---

## Requirement Selection Notes

The requirements below are deliberately limited to invariants that must hold at the *end state* — i.e., what we will check to verify "no loss" and "renumber not reintroduced." Procedural details (commit order, branch names, whether to squash) belong in the design / plan. The acceptance criteria carry the verification commands.

---

## Requirements

### Functional Requirements

> All FR below are from the user's request to "verify expected final state, including ensuring no data, code, or functionality was lost." FRs not marked are settled in this spec.

1. **FR-1 (ID space preservation):** Main's concept ID space MUST be byte-identical before and after merge with respect to directory names under `exploration/concept_analysis/analyses/` and `knowledge/concept_research/`. No directory MAY be renamed.
2. **FR-2 (CSV schema preservation):** `exploration/concept_analysis/table.csv` MUST remain on the v3 schema introduced by PR #16 (Heating Type, Driver Type, Blanket Config present; Plasma State, Tritium Breeding, Neutron Management absent). Row count and row identities MUST match main's pre-merge state, with the sole exception that rows 37/38/39 MAY be enriched with cell values from `concept-downselect` provided the row identity columns (ID, Concept Name, Company, Driver Technology, Research ID) are unchanged.
3. **FR-3 (research artifact completeness):** Every file added under `knowledge/concept_research/`, `.project/research/`, `.project/concepts/down_select/`, `.project/concepts/`, and `docs/demo/` by the commits `6eb2291`, `539a1b5`, `57ece9e`, `1d9937a`, `ab19c2a`, `f7f5da8`, `e7964c8`, and `8585ddd` MUST exist on `main` post-merge with byte-identical content, unless explicitly listed and justified as intentionally dropped in the implementation notes.
4. **FR-4 (scoring_v2 completeness):** The entire `exploration/scoring_v2/` module (extract.py, score.py, lib/, embeddings/) and `tests/scoring_v2/` MUST exist on `main` post-merge. `uv run pytest tests/scoring_v2/` MUST pass with the same pass/skip/xfail counts as on `concept-downselect` (26 passed / 3 skipped / 1 xfailed), or any deviation MUST be documented in implementation notes.
5. **FR-5 (net-new concept content):** The full analysis content for concepts 37, 38, 39 from `concept-downselect` (analyses/*/analysis.md, iter-01/sources/, model_output.txt where present, metrics) MUST exist under main's IDs 37/38/39 post-merge.
6. **FR-6 (split-17 reanalysis content):** The split-17 reanalysis content from `concept-downselect` (Focused Energy and Xcimer separate analyses) MUST exist on `main` under main's 17a (Xcimer / hybrid-drive) and 17b (Focused Energy / fast-ignition) directories. Mapping confirmation is a design-stage task.
7. **FR-7 (renumber tool exclusion):** `scripts/renumber/renumber.py` MUST NOT exist on `main` post-merge. The historical record `scripts/renumber/crosswalk.csv` MAY exist if and only if it is moved under a clearly archival path (e.g., `archive/` or `.project/research/`) so it is not mistaken for live tooling.
8. **FR-8 (no regression of main's Wave B fixes):** All data-hygiene fixes from main (commits `2ab95bf`, `ebcf1c3`, `45c9db5`, `50081cc`, `6ba8f02`, `9851b7e`) MUST remain applied post-merge, byte-identical to their pre-merge state on main.
9. **FR-9 (pipeline green):** `uv run agentic-mbse status` MUST exit 0 and produce no parser errors. `exploration/concept_analysis/seed_registry.py` and `exploration/concept_analysis/run_analysis.py status` MUST both exit 0.
10. **FR-10 (audit trail):** Implementation notes at `.project/active/concept-downselect-merge/implementation_notes.md` MUST list, for every commit on `concept-downselect`, exactly which files were ported, which were skipped, and the reason for any skip.
11. **FR-11 (no silent drops):** [INFERRED] If during implementation any file from `concept-downselect` is intentionally not ported, the decision MUST be recorded in implementation notes *before* the corresponding port commit lands. No "we forgot" outcomes.

### Non-Functional Requirements

- **Reviewability:** Each chunk (research, Wurzel, scoring V2, net-new analyses, split-17 reanalysis) SHOULD be a separate commit or tight commit series so a reviewer can read the merge as four logical PRs.
- **Determinism:** Where feasible, ported artifacts SHOULD be regenerated by the existing tooling on main (e.g., `extract.py --bulk-taxonomy`, `seed_registry.py`) rather than copied verbatim, so the result is reproducible from `table.csv` + source files.

---

## Acceptance Criteria

### Core Functionality

- [ ] **AC-1 (ID space):** `diff <(git ls-tree -r --name-only main:exploration/concept_analysis/analyses) <(git ls-tree -r --name-only <merge-branch>:exploration/concept_analysis/analyses)` shows only additions (no renames, no deletions) under `analyses/`.
- [ ] **AC-2 (CSV schema):** `head -1 exploration/concept_analysis/table.csv` shows the v3 columns (includes `Heating Type`, `Driver Type`, `Blanket Config`; excludes `Plasma State`, `Tritium Breeding`, `Neutron Management`).
- [ ] **AC-3 (CSV row identity):** For each row in `table.csv` that exists on pre-merge `main`, the `ID`, `Concept Name`, `Company`, `Driver Technology`, and `Research ID` columns are unchanged after merge.
- [ ] **AC-4 (research present):** For each of `knowledge/concept_research/{wurzel,megaprojects,what_is_foak,experience_rate_overestimates,…}/`, `output.md` exists and matches the byte content from `concept-downselect`.
- [ ] **AC-5 (scoring_v2 tests):** `uv run pytest tests/scoring_v2/ -v` → 26 passed / 3 skipped / 1 xfailed (or deviation documented).
- [ ] **AC-6 (net-new analyses):** `exploration/concept_analysis/analyses/37-*/analysis.md`, `…/38-*/analysis.md`, `…/39-*/analysis.md` are populated with the full downselect content (not stubs).
- [ ] **AC-7 (split-17 content):** `exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/iter-*/` contains Xcimer reanalysis content; `…/17b-laser-icf-fast-ignition/iter-*/` contains Focused Energy reanalysis content.
- [ ] **AC-8 (renumber tool absent):** `git ls-tree -r main scripts/renumber/renumber.py` returns nothing.
- [ ] **AC-9 (pipeline green):** `uv run agentic-mbse status && uv run python exploration/concept_analysis/seed_registry.py && uv run python exploration/concept_analysis/run_analysis.py status` all exit 0.
- [ ] **AC-10 (Wave B fixes intact):** For commits `2ab95bf`, `ebcf1c3`, `45c9db5`, `50081cc`, `6ba8f02`, `9851b7e` — `git diff <commit>^..<commit> -- <touched files>` applied to post-merge state yields zero new differences.

### No-Loss Verification

- [ ] **AC-11 (commit-by-commit file ledger):** Implementation notes contain a table: for each commit on `concept-downselect`, list (files-added, files-modified, files-deleted), and for each entry mark `[ported]`, `[ported-with-transform]`, `[skipped: <reason>]`.
- [ ] **AC-12 (no orphan downselect files):** `git diff --name-only main..<concept-downselect-snapshot>` cross-referenced against the implementation-notes ledger — every file accounted for, zero unaccounted-for paths.
- [ ] **AC-13 (functionality probe):** Spot-check by running `exploration/scoring_v2/score.py` (or its CLI entry) post-merge and confirm it produces the same headline scores documented in `30ecdd8`'s commit message (CFS 2.90, Helion 4.80, Stellarator 1.50 under slice1 weights).

### Quality & Integration

- [ ] Pre-existing tests continue to pass: `uv run pytest` (full suite) returns same pass count as pre-merge main, plus the new scoring_v2 tests.
- [ ] `uv run agentic-mbse status` reports no orphan items, no status mismatches.
- [ ] `concept-downselect` branch is preserved (not deleted) until the merge has lived on main for at least one week.

---

## Next-Stage Handoff

**Settled in this spec:**
- Renumber is dropped. Final.
- Four logical chunks (research, Wurzel, scoring V2, net-new + split-17) to port.
- Main's ID space and v3 schema are canonical.
- Audit trail requirement (implementation notes ledger) is mandatory.

**Design must figure out:**
- The exact target main-side directory paths for Focused Energy / Xcimer split-17 content (read main's current state to confirm 17a = Xcimer and 17b = Focused, or vice versa, by inspecting current CSV rows and analysis.md headers).
- Whether to cherry-pick downselect commits directly (`git cherry-pick`) or to copy the artifact trees and stage them fresh per-chunk. Cherry-pick is auditable; tree-copy is cleaner when paths must be remapped. Likely hybrid: cherry-pick Chunks 1 + 2 + 3, tree-copy Chunk 4 due to path remapping.
- How to handle `scoring_v2/features/*.yaml` reconciliation: rename-vs-regenerate. Recommend regenerate via `extract.py --bulk-taxonomy` on main's table.
- Conflict resolution strategy for `docs/demo/down-select.html` (last-wins from downselect with spot-check).
- Whether to land all four chunks as one PR or as four sequential PRs (recommend four — better review).

**Watch-outs for design:**
- `uv.lock` will conflict heavily. Plan for `uv sync` regeneration, not manual merge.
- `SOURCE_INDEX.md` regenerates from `knowledge/concept_research/`. Re-run generator post-port rather than merging text.
- `scoring.py` on main has architecture-driven C2 classification (from Mallory's content pull). Do not port downselect's `_C2`/`_HERITAGE` remap — it exists only to support the renumber we are dropping.
- The phase_1a / phase_2a Heating Type + Driver Type wiring on main (commits `db24808`, `fff5c18`, `6558cf6`) is unchanged by this merge; downselect did not touch those files. Verify post-merge.

---

## Related Artifacts

- **Prior analysis:** `.project/reports/2026-05-19-concept-downselect-merge-analysis.md`
- **Source branch:** `concept-downselect` (worktree at `/home/reid/1cfe/fusion-tea-concept-downselect`)
- **Target branch:** `main` (current head `8d59784`)
- **Design:** `.project/active/concept-downselect-merge/design.md` (to be created)
- **Plan:** `.project/active/concept-downselect-merge/plan.md` (to be created)
- **Implementation notes:** `.project/active/concept-downselect-merge/implementation_notes.md` (to be created during execution)

---

**Next Steps:** After approval, proceed to `/_my_design` to settle the open mapping questions and choose cherry-pick-vs-tree-copy per chunk.
