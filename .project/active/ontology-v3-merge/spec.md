# Spec: Ontology v3 Mechanical Merge

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-05-17
**Complexity:** MEDIUM-HIGH
**Branch:** `ontology-v3-migration` (to be created off `main` @ `a8a779e`)
**Epic:** ONTOLOGY-V3, Item 2

---

## Work Item Summary

Bring `origin/fix/concept-renumbering-robustness` (single commit `1b960a9` by Mallory, 2026-05-17 — 1,657 files, +36k/-58k LOC) onto a new branch off the freshly-updated `main`. The branch implements the v0.3.0 schema swap (drops `Plasma State` / `Tritium Breeding` / `Neutron Management`; adds `Blanket Config`), renumbers the concept slate (4 new concepts, Pranos dropped, IDs shifted/deduplicated), reruns the analysis pipeline for all 38→39 concepts, and refactors `lib/scoring.py` + `lib/concepts.py` to derive C2/freeform classification from architecture columns instead of hardcoded ID prefixes. This work item is the **mechanical merge only** — resolve conflicts (concentrated in the analyses/ artifacts that Item 1's availability/η_th standardization also touched), verify the codebase still builds end-to-end, and regenerate the explorer registry. Fixing the 9 known code gaps (column_map, decision-tree hierarchy, Jinja templates, tests, stale scores, etc.) is Item 3. Design questions (HB11 inconsistency, CSV-vs-MD source of truth) are Item 4.

## Why This Matters Now

`main` is now at `a8a779e` (the PR #15 merge of `consistency-checks`) and carries availability/η_th standardization across ~20 analyses. The ontology branch, written before that standardization landed, will conflict with every analyzed concept's `model_setup.py` / `analysis.md` / `synthesis.md` / `model_output.txt`. Every additional commit on `main` between now and the merge widens that conflict surface — getting the mechanical merge done first, on a dedicated branch, freezes the conflict resolution work and unblocks Items 3–5. Without it, the v3 schema can't propagate to `phase_2a/column_map.py`, the explorer, the test suite, or the synthesis refresh.

## Key Bets / Constraints

- **Bet:** Re-applying Item 1's standardization on top of the renumbered/reclassified `analyses/` files is mostly mechanical — the standardization edits are localized to availability/η_th kwargs and YAML frontmatter, and the renumbering doesn't touch those values. Conflicts will be path/filename-level (renamed directories, new IDs) more than line-level.
- **Bet:** A merge (preserving Mallory's authored commit) is preferable to a cherry-pick. The 1,657-file diff is too large to manually re-author cleanly, and keeping the commit intact preserves attribution and the detailed commit message.
- **Constraint:** The merged tree MUST still build and run end-to-end against the v3 schema before this item is considered done — `seed_registry.py`, `extract_explorer_data.py`, and `run_analysis.py status` all run to completion. Test suite fixes are explicitly Item 3's job; broken tests do NOT block this item, but broken entry-point scripts DO.
- **Constraint:** No new code authored in this item. Conflict resolution and re-applied standardization edits only. Anything that requires designing a fix (e.g. `column_map.py` references the dropped columns) is deferred to Item 3.
- **Non-goal:** Fixing the 9 known gaps from `.project/research/20260517_ontology_v3_delta.md` §Addendum.
- **Non-goal:** Resolving the HB11 Fast-ignition-vs-Ultrashort inconsistency on the branch — that's Item 4.
- **Non-goal:** Refreshing synthesis prose — that's Item 5.

---

## Business Goals

### Why This Matters

The v0.3.0 ontology is the canonical taxonomy going forward. Until the schema and renumbering land on `main`, every downstream effort (Phase 2a constraint validation, scoring, explorer UI, synthesis prose, comparative analysis) operates against a stale schema. The mechanical merge is the gate that unblocks everything in the rest of the ONTOLOGY-V3 epic. Doing it as a discrete, low-judgment item — separated from the higher-risk code-gap work — lets us land the merge fast and review the conflicts in isolation.

### Success Criteria

- [ ] `ontology-v3-migration` branch exists, rooted at `main` @ `a8a779e`, with `1b960a9` merged in.
- [ ] All Item 1 availability/η_th changes are preserved on the renumbered/reclassified analyses.
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` runs to completion against the merged tree.
- [ ] `uv run python exploration/concept_explorer/extract_explorer_data.py` runs to completion (warnings allowed; hard failures not).
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` runs and prints a sensible table.
- [ ] No working-tree references to pre-renumbering IDs in tracked source/data files (audited via grep).
- [ ] Regenerated `concept_registry.json` and `decision_tree.json` reflect the 39-concept slate.

### Priority

P0. Gates Items 3–5 of the ONTOLOGY-V3 epic. Conflict surface widens with every additional `main` commit.

---

## Problem Statement

### Current State

- `main` is at `a8a779e`. Working tree has three modifications: `.project/backlog/BACKLOG.md`, `.project/backlog/epic_ontology_v3_migration.md`, `uv.lock`. (BACKLOG and epic are part of this epic's planning; `uv.lock` was the unresolved tail from Item 1.)
- `origin/fix/concept-renumbering-robustness` (`1b960a9`) is a divergent single commit authored 2026-05-17 14:14. It branched from a point in `main`'s history before Item 1's availability standardization landed.
- The branch's diff intersects `main` at:
  - **Every analyzed concept** (`analyses/{ID}/{analysis,synthesis,model_output,model_setup}.{md,py,txt}`): the branch's pipeline rerun produced new content for these; Item 1 modified availability/η_th values in many of them.
  - **`scripts/standardize_eta_th.py`**: both branches edit it.
  - **`scripts/lib/scoring.py`**: branch refactors C2 derivation; Item 1 likely didn't touch this file but verify.
  - **`scripts/lib/concepts.py`**: branch refactors freeform classification; Item 1 likely didn't touch.
- `knowledge/concept_research/` directories are renamed on the branch (e.g. `17a-laser-icf-hybrid-drive` → `27-laser-icf-hybrid-direct-drive`); Item 1 didn't touch this tree, so conflicts there should be additions/renames only.
- `concept_explorer/data/{ID}.json` files are renumbered on the branch.

### Desired Outcome

- A single merge commit on `ontology-v3-migration` integrates `1b960a9` with `main`.
- All availability/η_th standardization values from Item 1 are present in the corresponding (renumbered) analysis files on the merged branch.
- `concept_registry.json` and `decision_tree.json` are regenerated and committed.
- The branch is ready to receive Item 3 (code gap fixes) without re-doing any conflict work.

---

## Scope

### In Scope

- Branch creation: `git checkout -b ontology-v3-migration` from `main` @ `a8a779e`.
- Pre-merge inventory: enumerate every conflicting file by category (analyses artifacts vs scripts vs data vs research) before starting resolution. Save inventory to `.project/active/ontology-v3-merge/conflict-inventory.md` for reference during execution.
- Merge execution: `git merge origin/fix/concept-renumbering-robustness` (preserve the commit; do not squash).
- Conflict resolution, in this order:
  1. **`scripts/lib/scoring.py`** and **`scripts/lib/concepts.py`** — take the branch version verbatim (architecture-driven refactor); confirm Item 1 didn't touch these (sanity check via `git log main -- <file>`).
  2. **`scripts/standardize_eta_th.py`** — both-edits conflict; combine: keep the branch's thermal-cycle update structure, keep Item 1's any-canonical-value additions if any.
  3. **`analyses/{ID}/`** — for each renumbered concept, re-apply Item 1's availability/η_th values onto the branch's reclassified file. Mechanical: identify the old-ID directory the file came from, copy the relevant kwargs/frontmatter values across, verify the rest matches the branch.
  4. **`knowledge/concept_research/`** — accept the branch's renames; no Item 1 conflicts expected here.
  5. **`concept_explorer/data/{ID}.json`** — accept the branch's renumbered files.
- Post-merge verification (in order):
  1. `git status` clean.
  2. `uv run python exploration/concept_explorer/seed_registry.py` — must succeed; regenerates `concept_registry.json` and `decision_tree.json`.
  3. `uv run python exploration/concept_explorer/extract_explorer_data.py` — must succeed for all 39 concepts (warnings OK; hard exit non-zero is a fail).
  4. `uv run python exploration/concept_analysis/scripts/run_analysis.py status` — must run; output sanity-checked against the 39-concept slate.
  5. Old-ID grep audit: `grep -rE '(17a-|17b-|20a-|20b-|34-compact-spherical-tokamak)' exploration knowledge --include='*.py' --include='*.md' --include='*.csv' --include='*.json'` — expected matches limited to migration notes in `RECLASSIFIED_CONCEPTS.md` and `add_ids.py` (legacy migration script). Anything else is a fail.
  6. Spot-check 3 reclassified concepts (e.g. 04 HB11, 22 → 23+37 split, 27 Xcimer-moved-from-17a): confirm availability/η_th values from Item 1 are present in the merged file.
- Commit the merge with the default merge message preserved.
- Push `ontology-v3-migration` to `origin`.

### Out of Scope

- Fixing `phase_2a/column_map.py` (references dropped columns) — Item 3.
- Fixing `_HIERARCHY`/`_SUBTYPES` in `seed_registry.py` to encode the v3 tree groups — Item 3.
- Fixing `ConfinementFamily` enum — Item 3.
- Fixing Jinja templates and `neighborhood_graph.js` — Item 3.
- Fixing `parameter_display_registry.yaml` — Item 3.
- Updating `tests/test_taxonomy_models.py` — Item 3.
- Rerunning scoring (`scores/verified_scores.json` is known-stale) — Item 3.
- Refactoring `oneoff_3d_clustering.py` `CADENCE_BY_PREFIX` and `generate_ontology_chart.py` `TREE_PATH` — Item 3.
- Resolving the HB11 Fast-ignition-vs-Ultrashort inconsistency — Item 4.
- Deciding CSV-vs-MD source of truth for `Heating Type` / `Driver Type` columns — Item 4.
- Refreshing synthesis prose for affected concepts — Item 5.
- Opening the PR to `main` — Items 3 and 4 must complete first.

### Edge Cases & Considerations

- **Item 1's `uv.lock` modification** is currently uncommitted on `main`'s working tree. Decide before merging: either commit it on `main` first (clean baseline) or stash and reapply post-merge. Recommend the former — a clean working tree before the merge avoids confusion.
- **Old-ID references in `add_ids.py`**: the file is a legacy migration script (`exploration/concept_analysis/add_ids.py`); its hardcoded `CONCEPT_ID_MAP` references old IDs. The branch did not touch it. Decision: leave it as-is for this item (it's not in the live pipeline) and flag for Item 3 / Item 6 cleanup. Do NOT fail the old-ID grep audit on this file alone.
- **Pranos dropping**: concept `34-compact-spherical-tokamak-india` is removed from the slate. Its `analyses/34-compact-spherical-tokamak-india/` directory and `knowledge/concept_research/34-compact-spherical-tokamak-india/` should be deleted by the merge. Verify they are absent post-merge. (If Item 1 modified Pranos files, those edits are discarded — confirm with the user before discarding; if it was in Item 1's batch, escalate.)
- **22 → 23 + 37 split**: the old combined "First Light, NearStar" concept becomes 23 (First Light) and 37 (NearStar). Item 1's edits to old-22 should go to new-23 (First Light is the primary concept; NearStar's MTIF analysis is a separate new artifact on the branch). Verify by reading old-22's availability value and confirming it lands in new-23, not new-37.
- **26+30 merge**: both Inertia Enterprises rows consolidated into new-31. Item 1's edits to old-26 and old-30 should both go to new-31. If they disagree, take the most recent (likely old-30, the NIF commercialization variant) and flag in the merge commit body.
- **Conflicts in `analyses/{ID}/synthesis.md` Stale frontmatter**: the branch's pipeline rerun reset `Stale: false` on every synthesis file. Item 1's standardization marked some as `Stale: true`. Resolution: take the branch's `Stale: false` (Item 5 will do a deliberate synthesis refresh; carrying forward `Stale: true` from Item 1 is misleading because the underlying values are now the branch's regenerated values).
- **Conflicts in `model_output.txt`**: these are generated artifacts. If both branches changed them, take the branch's version (it was regenerated after the reclassification). Item 1's `model_output.txt` updates were downstream effects of the standardization, which will be re-derived once Item 5 reruns the pipeline.
- **`.stale` sidecars in `concept_explorer/data/`**: the branch dropped these (regenerated extraction). Accept the branch's state.
- **Test files (`exploration/concept_explorer/tests/`)**: the branch did not update them, so no conflicts expected. They will be broken against the new enums — that's Item 3.
- **Working-tree edits from this epic** (`BACKLOG.md`, `epic_ontology_v3_migration.md`, `uv.lock`): commit these on `main` BEFORE the merge, so the merge starts from a clean state. Use a single "epic planning" commit.

---

## Requirement Selection Notes

Requirements below cover the contract of "what 'merged correctly' means" for this item — specifically the invariants that must hold post-merge for Item 3 to start cleanly. The exact mechanics of conflict resolution (3-way merge tooling, ours-vs-theirs choices for individual files, whether to use `git rerere`) are intentionally left to design. The shape of the post-merge audit script (one-liner vs Python helper) is also design's call.

---

## Requirements

### Functional Requirements

> Requirements derive from the ONTOLOGY-V3 epic Item 2 definition and the user's spec invocation.

1. **FR-1**: A new branch `ontology-v3-migration` MUST be created off `main` at exactly commit `a8a779e` (PR #15 merge) and MUST contain a single merge commit integrating `origin/fix/concept-renumbering-robustness` (`1b960a9`) as a second parent. The merge MUST preserve `1b960a9` as a reachable commit (no squash, no cherry-pick).
2. **FR-2**: Working-tree changes from epic planning (`.project/backlog/BACKLOG.md`, `.project/backlog/epic_ontology_v3_migration.md`, `uv.lock`) MUST be committed to `main` before the merge starts, so the merge proceeds from a clean working tree.
3. **FR-3**: After the merge, every analyzed concept whose availability or η_th values were edited by Item 1 MUST contain those edited values in its post-merge file location (which may be under a new ID after renumbering). For concepts split (22 → 23+37), the values go to the primary successor (23). For concepts merged (26+30 → 31), the most-recent variant's values are taken and the choice is documented in the merge commit body.
4. **FR-4**: After the merge, the following commands MUST run to completion (exit code 0; warnings tolerable):
   - `uv run python exploration/concept_explorer/seed_registry.py`
   - `uv run python exploration/concept_explorer/extract_explorer_data.py`
   - `uv run python exploration/concept_analysis/scripts/run_analysis.py status`
5. **FR-5**: After the merge, `concept_explorer/data/concept_registry.json` MUST contain exactly 39 concepts whose IDs match the v3 slate (no pre-renumbering IDs).
6. **FR-6**: After the merge, an old-ID grep audit (`grep -rE '(17a-|17b-|20a-|20b-|34-compact-spherical-tokamak)'` across `exploration/` and `knowledge/`, restricted to `*.py *.md *.csv *.json *.txt`) MUST produce no matches except in the explicit allow-list: `exploration/phase_1a/RECLASSIFIED_CONCEPTS.md` (the migration log) and `exploration/concept_analysis/add_ids.py` (legacy migration script — flagged for Item 3/6 cleanup).
7. **FR-7**: The branch MUST be pushed to `origin/ontology-v3-migration` after the merge is verified locally. No PR is opened in this item — that gate belongs to Item 4.
8. **FR-8**: [INFERRED] The merge commit body MUST list any decisions made during conflict resolution that are not mechanical (e.g. 26+30 variant selection, any Pranos files discarded), so Item 3 has a record to consult.
9. **FR-9**: A pre-merge conflict inventory MUST be produced at `.project/active/ontology-v3-merge/conflict-inventory.md` listing every conflicting path grouped by category (lib/scripts, analyses, research, data, other), to scope the resolution work and serve as a checklist during execution.

### Non-Functional Requirements

- **NFR-1**: The merge MUST complete in a single working session (≤1.5 days elapsed). Conflict resolution is mechanical; if it stretches past a day, something is structurally wrong and we should escalate rather than push through.
- **NFR-2**: No new code is authored in this item. Every change in the merge commit is either (a) from `main`, (b) from `1b960a9`, or (c) a hand-resolved combination of those two for a specific file. Resist the temptation to "just fix" anything from Item 3's list.

---

## Acceptance Criteria

### Core Functionality

- [ ] `git rev-parse ontology-v3-migration` resolves; `git merge-base ontology-v3-migration main` returns `a8a779e`.
- [ ] `git log --merges -1 ontology-v3-migration` shows a merge commit with `1b960a9` as one of two parents.
- [ ] `.project/active/ontology-v3-merge/conflict-inventory.md` exists and lists conflicts by category.
- [ ] `uv run python exploration/concept_explorer/seed_registry.py` exits 0.
- [ ] `uv run python exploration/concept_explorer/extract_explorer_data.py` exits 0.
- [ ] `uv run python exploration/concept_analysis/scripts/run_analysis.py status` exits 0 and prints a row for each of the 39 concepts.
- [ ] `python -c "import json; d=json.load(open('exploration/concept_explorer/data/concept_registry.json')); print(len(d['concepts']))"` prints `39`.
- [ ] Spot-check verification commands for 3 reclassified concepts produce expected availability/η_th values (commands listed in design).

### Quality & Integration

- [ ] Old-ID grep audit (FR-6) returns only the allow-listed files.
- [ ] The merge commit body documents any non-mechanical resolution decisions (26+30 variant pick, Pranos disposition).
- [ ] `git push origin ontology-v3-migration` succeeds.
- [ ] No edits to files listed in "Out of Scope" — verified by `git diff main...ontology-v3-migration -- <those-paths>` showing only what's attributable to `1b960a9` or to standardization-value carry-overs.
- [ ] Tests are NOT run in this item (they will fail against new enums; Item 3 fixes them).

---

## Next-Stage Handoff

**Settled in this spec:**
- The branch shape (single merge commit, no squash, no cherry-pick).
- Conflict resolution order (libs → scripts → analyses → research → data).
- Out-of-scope list (everything from Items 3, 4, 5).
- The post-merge verification chain (3 entry-point scripts + grep audit + spot-checks).
- The pre-merge planning commit on `main` (BACKLOG, epic, uv.lock).
- Handling for renumbered/split/merged concepts (22 → 23+37, 26+30 → 31, Pranos dropped).
- The branch is NOT PR'd in this item.

**Design must figure out:**
- The exact 3-way merge approach for `analyses/{ID}/` files where Item 1 and the branch both edited — whether to favor `git mergetool` interactively, scripted patch-rebase, or per-file `git checkout --ours/--theirs` followed by re-applying Item 1's deltas via a generated patch.
- Whether to commit the epic-planning changes (BACKLOG, epic, uv.lock) as one commit on `main` or split them. Recommend one commit; design can confirm.
- Whether the pre-merge conflict inventory is produced by a hand-script (`git merge --no-commit --no-ff` then `git diff --name-only --diff-filter=U`) or by reading the branch's file list against `main`'s. Either works.
- The exact form of the spot-check verification commands for the 3 reclassified concepts.
- The exact grep audit invocation — directory scope, file globs, allow-list mechanism (in-script grep -v vs documented exception list).
- How to handle a Pranos file Item 1 modified, if any — discard with note vs. preserve as orphan file vs. escalate.
- Whether to use `git rerere` for repeated identical conflict patterns across the ~30+ analyses files.

**Watch-outs for design:**
- The number-of-files conflict surface is large (potentially every analyzed concept), but the per-file conflict is small (availability + η_th kwargs only). A scripted approach that re-applies Item 1's standardization values to the branch's reclassified files may be faster than interactive resolution. Design should evaluate.
- `git merge` may report rename-with-modification conflicts (e.g. `17a-laser-icf-hybrid-drive/` → `27-laser-icf-hybrid-direct-drive/`). These need explicit attention — Git's default rename detection may or may not catch the rename depending on similarity threshold.
- The Pranos concept (`34-compact-spherical-tokamak-india`) was dropped on the branch. If Item 1 modified its files, those edits will appear as "deleted by them, modified by us" conflicts. Resolve by deleting (accept branch's removal) and noting in the merge commit body.
- Generated artifacts (`model_output.txt`, `decision_tree.json`, `concept_registry.json`) should be taken from the branch and then regenerated post-merge as the final step — do not hand-resolve generated files.
- `concept_explorer/data/{ID}.json` are renumbered on the branch. If Item 1 didn't touch these (it shouldn't have — it edited model setups, not extracted data), there should be no conflicts here; accept the branch's renames.
- `uv.lock` is currently modified on `main`'s working tree from Item 1's tail. Commit it before starting the merge — otherwise Git will demand stash/commit when the merge produces additional lock churn.

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_ontology_v3_migration.md` (Item 2)
- **Research:** `.project/research/20260517_ontology_v3_delta.md` (full delta + branch addendum)
- **Branch to merge:** `origin/fix/concept-renumbering-robustness` @ `1b960a9` (Mallory, 2026-05-17)
- **Baseline:** `main` @ `a8a779e` (PR #15 merge)
- **Item 1 history:** PR #15, merged `consistency-checks` → `main`
- **Conflict inventory (to be created):** `.project/active/ontology-v3-merge/conflict-inventory.md`
- **Design (to be created):** `.project/active/ontology-v3-merge/design.md`
- **Plan (to be created):** `.project/active/ontology-v3-merge/plan.md`

---

**Next Steps:** After approval, proceed to `/_my_design`. Design must specifically resolve the per-file conflict-resolution approach (scripted vs interactive) and produce the exact spot-check commands for the 3 reclassified-concept verifications.
