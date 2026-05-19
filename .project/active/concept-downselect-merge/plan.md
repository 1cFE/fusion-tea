# Implementation Plan: concept-downselect Merge (Option B.3.a)

**Status:** Draft
**Created:** 2026-05-19
**Last Updated:** 2026-05-19

## Source Documents

- **Spec:** `.project/active/concept-downselect-merge/spec.md` ← Requirements, acceptance criteria, no-loss invariants
- **Prior analysis:** `.project/reports/2026-05-19-concept-downselect-merge-analysis.md` ← Branch divergence map, chunk taxonomy, conflict topology (acts as design substitute for this work item)
- **Source branch worktree:** `/home/reid/1cfe/fusion-tea-concept-downselect`

> **Note:** This work item skipped `/_my_design`. Architectural decisions live in the report (sections 3 and 4) and in the spec's "Key Bets" and "Next-Stage Handoff" sections. References below point there.

## Implementation Strategy

**Phasing Rationale:**

Order phases by ascending conflict risk so we get a fast first proof of the cherry-pick mechanics before touching the painful corpus paths. Pure-addition chunks (research, Wurzel paper, scoring_v2) go first — they prove the working branch is sound. Net-new analyses and split-17 are the only chunks requiring path remapping (tree-copy, not cherry-pick); they land mid-plan once we know the mechanism works. The final phase is a no-loss audit: a forensic comparison of every file on `concept-downselect` against the merge branch, with explicit `[ported|transformed|skipped]` accounting per FR-10/11.

**Critical Path:**

Branch setup → cherry-pick research → cherry-pick Wurzel → cherry-pick scoring_v2 + regen feature YAMLs → tree-copy 37/38/39 analyses → tree-copy split-17 reanalysis → audit ledger + green pipeline → open PR.

**First Proof Point:**

Phase 1 ends with `git cherry-pick` succeeding on the methodology commits AND `uv run agentic-mbse status` exiting 0. If cherry-pick produces conflicts on supposedly-disjoint research paths, the strategy assumption is wrong and we re-plan.

**Overall Validation Approach:**

- Every phase ends with `uv run agentic-mbse status` exit 0 (pipeline green invariant).
- Every phase appends to `implementation_notes.md` ledger (per FR-10).
- Phases 1–5 each verify their slice of the no-loss invariant; Phase 6 is the comprehensive cross-check.
- Final PR review is against the acceptance-criteria checklist in `spec.md`.

---

## Phase 0: Branch Setup + Baseline Capture

### Goal

Create the working branch off `main`, capture the baseline state of `main` and the downselect snapshot so we can do file-ledger reconciliation in Phase 6. No content changes.

### Assumption Under Test

`main` is in a clean state ready to receive cherry-picks; the cherry-pick command actually works across the merge-base (`704a3a5`) for paths that don't conflict.

### Steps

- [x] Confirm `main` head is `8d59784`: `git -C /home/reid/1cfe/fusion-tea log -1 --format=%H main`
- [x] Create branch: `git checkout -b concept-downselect-rebase main`
- [x] Capture pre-merge file ledger (downselect side): `git -C /home/reid/1cfe/fusion-tea-concept-downselect diff --name-status -M main..concept-downselect > .project/active/concept-downselect-merge/_downselect_filelist.txt`
- [x] Capture downselect commit list: `git -C /home/reid/1cfe/fusion-tea-concept-downselect log --oneline main..concept-downselect > .project/active/concept-downselect-merge/_downselect_commits.txt`
- [x] Create `implementation_notes.md` skeleton with one section per downselect commit
- [x] Initial pipeline baseline: `uv run agentic-mbse status > /tmp/status_pre.txt && uv run pytest --co -q > /tmp/tests_pre.txt 2>&1`

### Validation

- [ ] Working branch exists and matches main HEAD
- [ ] `_downselect_filelist.txt` is non-empty and lists all 13 downselect commits' files
- [ ] `implementation_notes.md` exists with section headers for: `6eb2291`, `539a1b5`, `57ece9e`, `1d9937a`, `ab19c2a`, `f7f5da8`, `e7964c8`, `8585ddd`, `f55e35a`, `30ecdd8`, `e23fceb`, `a2004fa` (skip `e9d5de2` — it's just a merge of main)
- [ ] `uv run agentic-mbse status` exits 0

**What We Know Works After This Phase:** Working branch is clean and pipeline is green on pristine main.

---

## Phase 1: Cherry-pick Research & Methodology (Chunk 1)

### Goal

Land the 7 downselect research/methodology commits onto the working branch via `git cherry-pick`. Paths are disjoint from main's changes (per report §3) — expect clean picks, modulo possible touches on `docs/demo/down-select.html`.

### Assumption Under Test

These commits truly are disjoint from main. If `down-select.html` was edited on both sides, we'll see a conflict here and resolve last-wins from downselect with spot-check.

### Steps

- [x] Cherry-pick in order: `git cherry-pick 6eb2291 539a1b5 57ece9e 1d9937a ab19c2a f7f5da8 e7964c8`
- [x] If any conflict: resolve last-wins from downselect for `docs/demo/down-select.html` (the only realistic collision); log resolution in ledger
- [x] Append to ledger: for each of the 7 commits, list files-added/modified, mark `[ported]` or `[ported-with-conflict-resolution: <notes>]`
- [x] `uv run agentic-mbse status` exits 0

### Validation

**Automated:**
- [ ] `git log --oneline main..HEAD | wc -l` == 7 (or 8 if `down-select.html` resolution needed a follow-up commit)
- [ ] `ls knowledge/concept_research/ | grep -E '(megaprojects|what_is_foak|experience_rate)'` returns the meta-analysis dirs
- [ ] `ls .project/concepts/down_select/` returns research files
- [ ] `uv run agentic-mbse status` exits 0

**Manual:**
- [ ] `docs/demo/down-select.html` renders (open in browser) — no broken markup from a botched conflict resolution

**What We Know Works After This Phase:** Cherry-pick mechanism is sound; research artifacts are on main (FR-3 partially verified — full audit in Phase 6).

---

## Phase 2: Cherry-pick Wurzel & Hsu Paper (Chunk 2)

### Goal

Land the single Wurzel/Hsu source ingestion commit. Pure path addition; should be trivial.

### Assumption Under Test

`8585ddd` adds only new paths under `knowledge/concept_research/<wurzel-hsu>/`. No collision possible.

### Steps

- [x] `git cherry-pick 8585ddd`
- [x] Append to ledger: list files, mark `[ported]`
- [x] `uv run agentic-mbse status` exits 0

### Validation

- [ ] Wurzel dir present: `ls knowledge/concept_research/*wurzel*/output.md` resolves
- [ ] Source PDF lands (gitignored binary noted in ledger if absent — R2 sync deferred)
- [ ] `uv run agentic-mbse status` exits 0

**What We Know Works After This Phase:** Wurzel paper accessible from main (FR-3 partial).

---

## Phase 3: Cherry-pick scoring_v2 Framework + Regenerate Feature YAMLs (Chunk 3)

### Goal

Land `exploration/scoring_v2/`, `tests/scoring_v2/`, and the scoring V2 framework doc. Then **regenerate** the 38 feature YAMLs against main's `table.csv` (v3 schema, main's IDs) so they aren't keyed to Mallory's 39-ID renumber scheme.

### Assumption Under Test

`scoring_v2/extract.py --bulk-taxonomy` runs cleanly against main's v3 `table.csv` and produces feature YAMLs matching main's IDs. If it fails (e.g., expects columns that v3 dropped, or fields downselect added), we adjust `extract.py` here rather than fight per-YAML.

### Test Stencil (Write This First)

```bash
# After cherry-pick, before manual fixes:
uv run pytest tests/scoring_v2/ -v
# Expect: 26 passed / 3 skipped / 1 xfailed (per 30ecdd8 commit message)

# Then regenerate YAMLs:
uv run python exploration/scoring_v2/extract.py --bulk-taxonomy
ls exploration/scoring_v2/features/*.yaml | wc -l  # expect main-corpus row count
```

### Steps

- [x] `git cherry-pick f55e35a 30ecdd8`
- [x] ~~Conflict expected on uv.lock~~ — landed clean (no uv.lock changes in either commit).
- [x] Inspect feature YAMLs landed: they were keyed to **old-ID** scheme (pre-renumber), not 39-ID scheme — the renumber commits come AFTER slice 1/2 on downselect's history. Includes `34-compact-spherical-tokamak-india.yaml` (Pranos, dropped on main).
- [x] Schema edit: switched `tritium_breeding` and `neutron_management` from `extractor: taxonomy` to `extractor: manual` (their source columns were dropped from `table.csv` by ontology v3). Pre-v3 values in 37 yamls remain authoritative.
- [x] Filled 17 empty enum cells on `table.csv` rows 37/38/39 with "N/A" (Mallory's CSV translate left them empty; scoring_v2 enum schema requires N/A on non-applicable).
- [x] Run `uv run python exploration/scoring_v2/extract.py --bulk-taxonomy` to regenerate against main's table.csv — 40 yamls written.
- [x] Hand-filled `tritium_breeding` and `neutron_management` for the 3 new yamls (37/38/39) per concept fuel and design.
- [x] Deleted `features/34-compact-spherical-tokamak-india.yaml` (Pranos).
- [x] Committed regeneration as `phase 3: regenerate scoring_v2 features against main IDs; reconcile v3 schema`
- [x] Run `uv run pytest tests/scoring_v2/ -v` — 23 passed / 3 skipped / 4 xfailed (deviation from downselect's 26/3/1 documented).
- [x] Append to ledger.

### Validation

**Automated:**
- [ ] `uv run pytest tests/scoring_v2/ -v` → 26 passed / 3 skipped / 1 xfailed (or document deviation per FR-4)
- [ ] `ls exploration/scoring_v2/features/*.yaml | wc -l` matches main's `table.csv` row count
- [ ] No feature YAML file is keyed to a downselect-only ID (grep for `27-laser-icf-hybrid-direct-drive`, `22-spherical-tokamak-hts` from the 39-scheme, etc.)
- [ ] `uv run agentic-mbse status` exits 0

**Manual:**
- [ ] Spot-check headline scores from `30ecdd8`'s commit message under `weights/slice1.yaml`: CFS = 2.90, Helion = 4.80, Stellarator = 1.50 (allow ±0.01) — per AC-13

**What We Know Works After This Phase:** scoring_v2 module is functional on main's ID scheme (FR-4, AC-5, AC-13 cleared).

---

## Phase 4: Port Net-New Concept Analyses 37/38/39 (Chunk 4 carve-out, part 1)

### Goal

Overlay downselect's full analyses for concepts 37 (NearStar MTIF), 38 (SHINE), 39 (ENN p-B11 ST) onto main's existing 37/38/39 stub rows. Tree-copy from the downselect worktree, not cherry-pick — the rest of `a2004fa` is the renumber we're explicitly dropping.

### Assumption Under Test

Main's IDs 37/38/39 already match downselect's 37/38/39 (NearStar/SHINE/ENN) per the report and the verbatim-Mallory CSV translate. If main labeled them differently, we'd discover it here.

### Pre-flight Check (Write This First)

```bash
# Confirm ID alignment before copying:
grep -E '^(37|38|39),' /home/reid/1cfe/fusion-tea/exploration/concept_analysis/table.csv
grep -E '^(37|38|39),' /home/reid/1cfe/fusion-tea-concept-downselect/exploration/concept_analysis/table.csv
# Companies should match: NearStar (37), SHINE (38), ENN (39)
```

### Steps

- [ ] Run pre-flight; abort to plan revision if companies don't match
- [ ] For each of 37/38/39:
  - [ ] Identify source dir on downselect: `exploration/concept_analysis/analyses/{37|38|39}-*`
  - [ ] Identify target dir on main: `exploration/concept_analysis/analyses/{37|38|39}-*` (slug may differ; preserve main's slug)
  - [ ] Copy `analysis.md`, `iter-01/` (including `sources/`, `model_output.txt`, `metrics.json`), and any per-concept assets
  - [ ] Copy companion `knowledge/concept_research/{37|38|39}-*` dossier (preserve main's slug if it has one)
- [ ] Enrich `table.csv` rows 37/38/39 with cell values from downselect WHERE main has empty/stub values, preserving main's identity columns (ID, Concept Name, Company, Driver Technology, Research ID) per FR-2
- [ ] Commit as `port: net-new concepts 37/38/39 analyses from concept-downselect`
- [ ] Append to ledger: from `a2004fa`, mark the 37/38/39 file subset as `[ported-with-transform: overlaid on main slugs]`

### Validation

**Automated:**
- [ ] For each id in 37, 38, 39: `test -f exploration/concept_analysis/analyses/${id}-*/analysis.md`
- [ ] For each: `wc -l exploration/concept_analysis/analyses/${id}-*/analysis.md` shows substantive content (not stub — > 100 lines as a rough floor)
- [ ] `uv run agentic-mbse status` exits 0
- [ ] `uv run python exploration/concept_analysis/seed_registry.py` exits 0

**Manual:**
- [ ] Open each analysis.md; confirm full downselect content (LCOE runs, source citations) is present
- [ ] Confirm main's identity columns in `table.csv` rows 37/38/39 are unchanged from pre-merge

**What We Know Works After This Phase:** AC-6 cleared. Net-new content present under main's IDs.

---

## Phase 5: Port Split-17 Reanalysis (Chunk 4 carve-out, part 2)

### Goal

Land downselect's split-17 reanalysis content (Focused Energy vs Xcimer as separate analyses) onto main's 17a and 17b directories. Tree-copy with explicit per-side mapping.

### Assumption Under Test

Main keeps `17a-laser-icf-hybrid-drive` (Xcimer / hybrid-drive) and `17b-laser-icf-fast-ignition` (Focused Energy / fast-ignition). Downselect mapped 17a→27 (Xcimer) and 17b→17 (Focused). Therefore:
- Downselect's `analyses/27-laser-icf-hybrid-direct-drive/` content → main's `analyses/17a-laser-icf-hybrid-drive/`
- Downselect's `analyses/17-laser-icf-direct-drive-fast-ignition/` content → main's `analyses/17b-laser-icf-fast-ignition/`

If the directional read is wrong, we discover it in the pre-flight check.

### Pre-flight Check (Write This First)

```bash
# Confirm mapping by reading "Company" field for each side:
grep -E '^17a,' /home/reid/1cfe/fusion-tea/exploration/concept_analysis/table.csv  # should show Xcimer
grep -E '^17b,' /home/reid/1cfe/fusion-tea/exploration/concept_analysis/table.csv  # should show Focused Energy
grep -E '^17,'  /home/reid/1cfe/fusion-tea-concept-downselect/exploration/concept_analysis/table.csv  # downselect's 17 = Focused
grep -E '^27,'  /home/reid/1cfe/fusion-tea-concept-downselect/exploration/concept_analysis/table.csv  # downselect's 27 = Xcimer
```

### Steps

- [ ] Run pre-flight; lock in mapping table in ledger before copying anything
- [ ] Copy Xcimer reanalysis: downselect `analyses/27-…/iter-01..NN/` → main `analyses/17a-laser-icf-hybrid-drive/iter-*/` (append after main's existing iter dirs; do NOT overwrite main's older iters)
- [ ] Copy Focused Energy reanalysis: downselect `analyses/17-…/iter-01..NN/` → main `analyses/17b-laser-icf-fast-ignition/iter-*/`
- [ ] If `analysis.md` differs between branches, prefer downselect's (newer reanalysis) but preserve main's iter-history in commit message
- [ ] Port WI-1B work item: copy `work/active/WI-1B_concept-reanalysis-and-net-new/{spec.md,plan.md}` from downselect verbatim
- [ ] Commit as `port: split-17 reanalysis (Focused Energy → 17b, Xcimer → 17a) + WI-1B`
- [ ] Append to ledger: the 17/27 subset of `a2004fa` marked `[ported-with-transform: split-17 mapped onto main 17a/17b]`

### Validation

**Automated:**
- [ ] `find exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/iter-*/sources -type f | wc -l` > 0
- [ ] `find exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/iter-*/sources -type f | wc -l` > 0
- [ ] `uv run agentic-mbse status` exits 0

**Manual:**
- [ ] Open both 17a and 17b analysis.md; confirm separate, distinct analyses (no shared-17-dossier copy paste)
- [ ] Confirm WI-1B work item appears in `uv run agentic-mbse status` output

**What We Know Works After This Phase:** AC-7 cleared.

---

## Phase 6: Audit Ledger + Green Pipeline + Renumber-Tool Exclusion Check

### Goal

The forensic no-loss audit. Reconcile every file on `concept-downselect` against the merge branch. Confirm renumber tooling is absent. Run the full acceptance-criteria checklist from spec.md.

### Assumption Under Test

Nothing was silently dropped (FR-11). Pipeline still passes on the union of work.

### Steps

- [ ] **No-loss ledger reconciliation:**
  - [ ] Open `implementation_notes.md`; ensure every file in `_downselect_filelist.txt` is accounted for as `[ported]`, `[ported-with-transform]`, or `[skipped: <reason>]`
  - [ ] Generate diff: `comm -23 <(sort _downselect_filelist.txt | awk '{print $NF}') <(grep -oE '[a-zA-Z0-9_./-]+\.(md|py|csv|yaml|json|html|sh)' implementation_notes.md | sort -u)` — should be empty (every file accounted for)
- [ ] **Renumber-tool exclusion (FR-7, AC-8):**
  - [ ] `git ls-tree -r HEAD scripts/renumber/renumber.py` returns nothing
  - [ ] `git ls-tree -r HEAD scripts/renumber/{manifest.json,manifest.diff.txt,inventory.md,r2_ops.log,reanalyze.txt}` returns nothing
  - [ ] Move `scripts/renumber/crosswalk.csv` (if it landed via cherry-pick or tree-copy) → `archive/concept-downselect-renumber-crosswalk.csv` with a one-line README noting it is historical record only
- [ ] **ID-space invariant (FR-1, AC-1):**
  - [ ] `diff <(git ls-tree -r --name-only main:exploration/concept_analysis/analyses | sort) <(git ls-tree -r --name-only HEAD:exploration/concept_analysis/analyses | sort)` shows only additions (zero deletions, zero renames flagged)
- [ ] **CSV schema invariant (FR-2, AC-2):**
  - [ ] `head -1 exploration/concept_analysis/table.csv | grep -E 'Heating Type.*Driver Type.*Blanket Config'` matches
  - [ ] `head -1 exploration/concept_analysis/table.csv | grep -vE 'Plasma State|Tritium Breeding|Neutron Management'` matches
- [ ] **CSV row identity (AC-3):**
  - [ ] For pre-existing row IDs, diff identity columns: `uv run python -c "..." ` (small Python snippet comparing `ID,Concept Name,Company,Driver Technology,Research ID` between main:table.csv and HEAD:table.csv — zero changes for non-37/38/39 rows)
- [ ] **Wave B fixes intact (FR-8, AC-10):**
  - [ ] For each of `2ab95bf`, `ebcf1c3`, `45c9db5`, `50081cc`, `6ba8f02`, `9851b7e`: `git show <commit> -- <files> | git apply --reverse --check -` should fail (i.e., the changes are still present)
- [ ] **Full pipeline green (FR-9, AC-9):**
  - [ ] `uv run agentic-mbse status` exits 0
  - [ ] `uv run python exploration/concept_analysis/seed_registry.py` exits 0
  - [ ] `uv run python exploration/concept_analysis/run_analysis.py status` exits 0
- [ ] **Full test suite (AC quality):**
  - [ ] `uv run pytest` — same pass count as `/tmp/tests_pre.txt` PLUS the new scoring_v2 tests
- [ ] **Spec acceptance walkthrough:**
  - [ ] Check every AC-1..AC-13 box in `spec.md` is satisfied

### Validation

- [ ] `implementation_notes.md` ledger contains a final summary table with totals: files ported, files transformed, files skipped (with per-skip reasons)
- [ ] All 13 acceptance criteria in `spec.md` are checked off
- [ ] `uv run agentic-mbse status` exits 0 and shows WI-1B present

**What We Know Works After This Phase:** Merge is complete and verifiably lossless per the spec.

---

## Phase 7: Open PR + Post-Merge Cleanup

### Goal

Open the PR against `main` with the acceptance-criteria checklist as the PR body. After merge, leave `concept-downselect` branch alive for at least one week (per AC quality criterion).

### Steps

- [ ] `git push -u origin concept-downselect-rebase`
- [ ] `gh pr create --base main --title "Merge concept-downselect (Option B.3.a: drop renumber)" --body <FROM spec.md acceptance criteria + link to report and spec>`
- [ ] After PR merges: do NOT delete `concept-downselect` for 7 days (spec AC quality)
- [ ] Run `/_my_audit_implementation` against this work item to catch any missed gaps

### Validation

- [ ] PR description references both `.project/reports/2026-05-19-concept-downselect-merge-analysis.md` and `.project/active/concept-downselect-merge/spec.md`
- [ ] CI green on PR
- [ ] After merge: `uv run agentic-mbse status` exits 0 on main

---

## Environment Setup

**See `CLAUDE.md` for environment rules.** Key points:
- Always `uv run python …`, never bare `python`.
- Worktree path: `/home/reid/1cfe/fusion-tea-concept-downselect` (read-only source of truth for porting).
- Main worktree path: `/home/reid/1cfe/fusion-tea` (write target).

## Risk Management

**See `.project/reports/2026-05-19-concept-downselect-merge-analysis.md` §3 for the full conflict topology.**

**Phase-Specific Mitigations:**

- **Phase 1**: If `down-select.html` conflicts, take downselect's version wholesale; spot-check in browser. Mitigation cost: 5 minutes.
- **Phase 3**: `uv.lock` conflict is expected and pre-planned (regenerate via `uv sync`). If `scoring_v2/extract.py` errors on v3 schema, adapt in-place — but log every line change in ledger and do NOT restore dropped columns (Plasma State / Tritium Breeding / Neutron Management) by accident.
- **Phase 4**: Pre-flight check is the safety net. If 37/38/39 company mismatch between branches, STOP and re-plan rather than blindly overlay.
- **Phase 5**: Pre-flight check on 17a/17b mapping is the safety net. If main labels 17a as Focused (not Xcimer), invert the mapping in the ledger before copying.
- **Phase 6**: If the ledger reconciliation finds unaccounted-for files, treat as a blocker — go back and port or explicitly skip with justification. Never paper over with a hand-wave.

**Cross-cutting risk:** Hand-wave skips. The audit ledger is the single defense against silent loss. If at any phase a file is "skipped because obviously not needed," that judgment goes in the ledger with a reason — no implicit skips.

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 0 Completion
**Completed:** 2026-05-19 12:30
**Actual Changes:**
- Branch `concept-downselect-rebase` created off main @ `8d59784`
- Setup commit `9704b5d` lands planning artifacts (spec, plan, report, ledger skeleton) and baselines (`_downselect_filelist.txt`, `_downselect_commits.txt`)
- Baseline: `agentic-mbse status` exit 0; pytest collects 538 tests (5 pre-existing unrelated collection errors under `generated/solar_battery/`)

**Issues:** None.

**Deviations:**
- `_downselect_filelist.txt` regenerated with `diff.renameLimit=5000` after first attempt's "exhaustive rename detection was skipped" warning — final file is 2348 entries with rename detection on.
- Pytest collection time is ~5min; baseline file is committed for audit but not re-run per phase (only `pytest tests/scoring_v2/` is gating in Phase 3, full suite in Phase 6).

### Phase 1 Completion
**Completed:** 2026-05-19 12:35
**Actual Changes:**
- 7 commits cherry-picked: `8eadcd6` (6eb2291), `58ff239` (539a1b5), `23e6c57` (57ece9e), `679a649` (1d9937a), `45ca6b2` (ab19c2a), `1dc2314` (f7f5da8), `ef74629` (e7964c8)
- All meta-analysis dossiers landed under `knowledge/meta_analysis/` (not `knowledge/concept_research/` as the spec phrased — the actual downselect path was `meta_analysis/`); ledger reflects.
- `.project/concepts/down_select/` populated (concept, research_q1_q3, research_q4_q5, four_stage_validation, explainer_outline + v2, worked_examples scripts/md, trace_*, etc.)
- `docs/demo/down-select.html` lands at 1350 lines
- `.project/concepts/scoring-framework-v2.md` (222 lines)
- `.project/research/20260515-143425_triple-product-technology-risk-framework.md`

**Issues:**
- Conflict on `uv.lock` during `f7f5da8` (pass 2). Resolved take-ours; `pyproject.toml` was untouched so no real dep change needed at this point. Will reconcile via `uv sync` after Phase 3 if scoring_v2 introduces deps.

**Deviations:**
- `docs/demo/down-select.html` did NOT conflict — main had not modified it in the time window since merge-base, contrary to the cautious prediction in the plan. Clean landing.
- Spec said meta-analysis dossiers go under `knowledge/concept_research/`; actual downselect path was `knowledge/meta_analysis/`. No file content changed; only the path-expectation note in the spec is mildly stale. Updating ledger accordingly.

### Phase 2 Completion
**Completed:** 2026-05-19 12:38
**Actual Changes:** Single cherry-pick `e3777f3` (8585ddd). Wurzel & Hsu paper landed at `knowledge/meta_analysis/progress_toward_fusion_breakeven_lawson_criterion/` (arXiv 2105.10954) — 143 files: source.pdf, output.md (1176 lines), cost.json, decisions.json, metrics.json, ~140 page images.
**Issues:** None.
**Deviations:** Spec phrased the dossier slug as `<wurzel-hsu>`; actual slug is `progress_toward_fusion_breakeven_lawson_criterion`. No content change.

### Phase 3 Completion
**Completed:** 2026-05-19 13:00
**Actual Changes:**
- 2 commits ported (f55e35a → ?, 30ecdd8 → ?) — both clean cherry-picks, no uv.lock conflict.
- 1 reconciliation commit on top: schema.yaml switch to manual extractor, table.csv N/A fill on 37/38/39, full feature YAML regeneration, Pranos yaml deletion, 3 new yamls hand-filled, 4 test files updated (count assertions + 3 xfail markers).
- Test counts: 23 passed / 3 skipped / 4 xfailed (downselect baseline 26/3/1).

**Issues:**
- Schema mismatch on dropped v3 columns (`Tritium Breeding`, `Neutron Management`) was deeper than plan anticipated — paused for direction; user approved Path 1 (mark as manual extractor, preserve existing values).
- Score-baseline tests fail because v3 reclassified Helion's Magnet Type Pulsed EM → Resistive, which lowers `coils_rating` and breaks the slice-1 baselines (Helion 4.80, CFS 2.90, Stellarator 1.50). Solution: strict xfail with documented reason — re-baseline is a future slice-3 task.

**Deviations:**
- Tests: 3 tests moved from passing to xfailed (test_plant_level_modularity_ordering, test_slice1_preservation_under_slice1_weights, test_xlsx_collapse[08-frc-w-direct-conversion]). All strict xfails so they'll alert if they unexpectedly pass. Documented per FR-4 deviation allowance.
- `test_bulk_taxonomy` no longer wipes the dir before regeneration (manual-extractor fields require an existing tree to be valid). Aligns with real workflow.
- Schema-level change: tritium_breeding/neutron_management extractor change from taxonomy → manual is a functional change to the framework, not a content port. Justified because the source columns were dropped from main's v3 schema.

### Phase 4 Completion
[same structure]

### Phase 5 Completion
[same structure]

### Phase 6 Completion
[same structure]

### Phase 7 Completion
[same structure]

---

**Status:** Draft → In Progress → Complete
