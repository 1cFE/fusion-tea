# Implementation Plan: Concept Research 17-Split Reconciliation

**Status:** Draft
**Created:** 2026-05-19
**Last Updated:** 2026-05-19

## Source Documents

- **Spec:** `.project/active/concept-research-17-split/spec.md` ← see for FRs, scope, partition inventory (Appendix), acceptance criteria
- **Design:** (skipped — open design questions resolved inline below)

---

## Inline Design Decisions

Decisions deferred from spec, locked in here so the plan is executable.

| Decision | Choice | Rationale |
|---|---|---|
| **Shared-source partition rule** | **Duplicate** shared sources into BOTH `17a-…/iter-NN/sources/` and `17b-…/iter-NN/sources/`. | Each dossier should be self-contained; cross-references into archive are fragile. Sources are markdown + R2-tracked binaries — duplication on disk is cheap. Avoids unresolvable "which side does HYLIFE-II belong to" debates. |
| **Iteration numbering on new sides** | Preserve `iter-01`, `iter-02`, `iter-03` numbering. Each iter-NN on the new sides contains only the sources that originally lived in that iter-NN of the legacy dir, partitioned by side (or duplicated for shared). Add an `iter-04` with a single changelog entry recording the split. | Maintains provenance: any source's iter history matches its original collection iter. Renumbering would orphan that history. |
| **Citation paths in `concept_analysis/analyses/17{a,b}/iter-*/analyze_prompt.md`** | Leave as-is; do not rewrite. | These are frozen historical prompts already consumed by past analysis runs. The archive README documents that those paths now resolve under `archive/concept_research_legacy/`. Live scripts do not consume these paths (verified). |
| **Archive layout** | Single umbrella `archive/concept_research_legacy/` containing `17-laser-icf-direct-drive/`, `20-modular-hts-stellarator/`, `34-compact-spherical-tokamak-india/`, plus one top-level `README.md`. | Minimal layout, easy to discover, parallels existing `archive/` flat structure. |
| **`SOURCE_INDEX.md` regeneration** | Hand-author from a directory walk in Phase 4. The existing `migrate_research.py` `--reindex` flag is for the initial migration; it may not produce the precise current format. | Cheap to inspect what's there; verifies the listing matches reality. |
| **R2 sync strategy** | Push new dirs via `./scripts/sync_research.sh push`; explicitly `rclone delete` the three retired remote dirs as a separate documented step. User-confirmed step (destructive on R2) before execution. | R2 push is additive only; without an explicit delete, the remote tree drifts from local. |

---

## Implementation Strategy

**Phasing Rationale:** De-risk by building the partition manifest first (Phase 1) so every later phase has a single source of truth for "what goes where." Construct the new canonical dirs (Phase 2) before retiring the legacy ones (Phase 3) so we never have a window with neither side intact. Reindex (Phase 4) after structure is settled. R2 sync (Phase 5) is last because it's destructive on the remote and the local tree must be final.

**Critical Path:** partition manifest → build 17a/17b → archive legacy → reindex → R2.

**First Proof Point:** Phase 1 partition manifest CSV passes a roundtrip check — every legacy source file appears in the manifest exactly once, and the manifest's side assignments cover all 22 sources.

**Overall Validation Approach:**
- Each phase has a verifiable disk-state assertion (file existence, diff against canonical table, byte-count parity).
- The acceptance diff (`comm` of `ls concept_research/` against `table.csv`) runs at every phase boundary as a regression gate.
- No commit until Phase 5 passes the full acceptance set.

---

## Phase 1: Partition Manifest + Verification Harness

### Goal

Codify the legacy-source partition as a single CSV manifest that every later phase reads. Write the diff-check that enforces FR-6 (filesystem ⊆ canonical IDs). Snapshot pre-state.

### Assumption Under Test

That the 22 legacy sources cleanly partition into {17a-only, 17b-only, shared} with no ambiguous cases requiring fresh research. (Spec Appendix asserts this; this phase proves it by enumeration.)

### Test Stencil (Write First)

```bash
# tests/test_17_split_manifest.sh — sanity checks on the manifest
set -euo pipefail
MANIFEST=.project/active/concept-research-17-split/source_partition.csv

# 1. every legacy source appears exactly once
find knowledge/concept_research/17-laser-icf-direct-drive -path "*/sources/*" -maxdepth 4 -mindepth 4 \
  -not -name "*.md" -printf "%f\n" | sort -u > /tmp/legacy_sources.txt
awk -F',' 'NR>1 {print $2}' "$MANIFEST" | sort -u > /tmp/manifest_sources.txt
diff /tmp/legacy_sources.txt /tmp/manifest_sources.txt  # must be empty

# 2. every row has a valid side
awk -F',' 'NR>1 && $3 !~ /^(17a|17b|shared)$/ {exit 1}' "$MANIFEST"

# 3. spot-check known assignments
grep -q "^iter-01,xcimer-energy-approach,17a," "$MANIFEST"
grep -q "^iter-01,focused-energy-technology,17b," "$MANIFEST"
```

### Changes Required

#### 1. Source partition manifest
**File:** `.project/active/concept-research-17-split/source_partition.csv` (NEW)
Columns: `iter,source_basename,side,notes`
- [ ] Populate from spec Appendix table.
- [ ] OSTI items (`osti-biblio-7021072`, `osti-servlets-purl-*` ×5): open each `output.md` to confirm "shared" vs side-specific; update manifest with definitive side.
- [ ] `sciencedirect-…-s0920379624001868`: confirm whether HYLIFE-III nuclear analysis → if Xcimer-specific, mark `17a`; else `shared`.

#### 2. Verification script
**File:** `.project/active/concept-research-17-split/verify.sh` (NEW)
- [ ] Implement test stencil above.
- [ ] Add canonical-diff check: `comm -23 <(ls knowledge/concept_research/ | grep -E '^[0-9]' | sort) <(awk -F, 'NR>1 {print $1}' exploration/concept_analysis/table.csv | sort)` — current expected state: prints `17-laser-icf-direct-drive`, `20-modular-hts-stellarator`, `34-compact-spherical-tokamak-india`. Target state (after Phase 3): empty.
- [ ] Add reverse-diff check: canonical IDs missing from disk. Current expected: `17a-…`, `17b-…`. Target state: empty.
- [ ] Make `verify.sh` print a pass/fail header per check.

#### 3. Pre-state snapshot
**File:** `.project/active/concept-research-17-split/pre_state.txt` (NEW)
- [ ] `ls -laR knowledge/concept_research/17-laser-icf-direct-drive knowledge/concept_research/20-modular-hts-stellarator knowledge/concept_research/34-compact-spherical-tokamak-india > pre_state.txt`
- [ ] `sha256sum` of each `dossier.md`, `changelog.md`, `dossier_17a_*.md`, `dossier_17b_*.md` appended to the same file.

### Validation

**Automated:**
- [ ] `bash .project/active/concept-research-17-split/verify.sh` runs without error.
- [ ] Manifest test stencil passes.

**Manual:**
- [ ] Eyeball the manifest CSV: every row has a defensible side + notes.

**What We Know Works After This Phase:** The partition rule is fully specified before any file moves. A roundtrip check guarantees no source can be forgotten.

---

## Phase 2: Build `17a-` and `17b-` Directories

### Goal

Create the two canonical per-side directories with dossier, changelog, and partitioned `iter-NN/sources/`. Legacy dir untouched in this phase (still present alongside).

### Assumption Under Test

That the existing seed dossiers (`dossier_17{a,b}_*_concept_downselect.md`) + shared `dossier.md` content can be merged into per-side `dossier.md` files without regression (FR-7).

### Test Stencil (Write First)

```bash
# tests/test_17ab_dirs.sh
set -euo pipefail
for side in 17a-laser-icf-hybrid-drive 17b-laser-icf-fast-ignition; do
  d=knowledge/concept_research/$side
  test -f "$d/dossier.md"
  test -f "$d/changelog.md"
  test -d "$d/iter-01/sources" && test -d "$d/iter-02/sources" && test -d "$d/iter-03/sources"
  # dossier must have differentiation table section
  grep -q "^## Differentiation Table Values" "$d/dossier.md"
  # changelog must reference the split
  grep -q "split" "$d/changelog.md"
done

# Source-completeness check: union(17a, 17b sources) ⊇ legacy sources
find knowledge/concept_research/17a-laser-icf-hybrid-drive knowledge/concept_research/17b-laser-icf-fast-ignition \
  -path "*/sources/*" -maxdepth 4 -mindepth 4 -printf "%f\n" | sort -u > /tmp/new_sources.txt
find knowledge/concept_research/17-laser-icf-direct-drive \
  -path "*/sources/*" -maxdepth 4 -mindepth 4 -printf "%f\n" | sort -u > /tmp/legacy_again.txt
comm -23 /tmp/legacy_again.txt /tmp/new_sources.txt  # must be empty
```

### Changes Required

#### 1. Create skeleton dirs
- [ ] `mkdir -p knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-{01,02,03}/sources`
- [ ] `mkdir -p knowledge/concept_research/17b-laser-icf-fast-ignition/iter-{01,02,03}/sources`

#### 2. Partition sources per manifest
Driven by `source_partition.csv` from Phase 1. For each row:
- side=`17a` → copy source dir + companion `.md` files into `17a-…/iter-NN/sources/`
- side=`17b` → copy into `17b-…/iter-NN/sources/`
- side=`shared` → copy into BOTH

- [ ] Write a one-off script `apply_partition.sh` that reads the manifest and does the copies. Use `cp -a` (preserve all metadata, follow no symlinks).
- [ ] Run it. Verify by re-running the source-completeness check from the test stencil.

#### 3. Promote per-side dossiers
- [ ] **17a dossier**: start from `dossier_17a_xcimer_concept_downselect.md`. Strip the "treat as low-confidence" header. Merge in Xcimer-specific commentary from the shared `dossier.md` (per-column citations where shared dossier explicitly attributes to Xcimer). Update header: confidence per-column, iterations completed=2 (inherited iter-01/02 plus this split = iter-03+04? — count iterations as 3, since iter-03 was the third source-gathering pass), last updated 2026-05-19. Write to `17a-laser-icf-hybrid-drive/dossier.md`.
- [ ] **17b dossier**: same process from `dossier_17b_focused_concept_downselect.md`, merging Focused-Energy-specific content from the shared dossier. Write to `17b-laser-icf-fast-ignition/dossier.md`.
- [ ] **Quality check**: for each Differentiation Table column on each side, confirm at least one citation is present and is company-specific (not a shared-background-source-only citation).

#### 4. Per-side changelogs
- [ ] Copy the shared `changelog.md` to both new dirs as the base.
- [ ] Append iter-04 entry to each: date 2026-05-19, action "split from `17-laser-icf-direct-drive/`", side-specific notes (which sources moved, which were duplicated as shared), reference to spec.

### Validation

**Automated:**
- [ ] `bash tests/test_17ab_dirs.sh` (or inline equivalent) passes.
- [ ] Source-completeness check empty.
- [ ] Dossier grep checks pass.

**Manual:**
- [ ] Open each new `dossier.md` and verify: header reflects single company, "Differentiation Table Values" section reads as side-specific (no Xcimer claims in 17b dossier, no Focused claims in 17a dossier).
- [ ] Spot-check one shared source (e.g., `hylife-energy-conversion-notes`) appears in both `17a-…/iter-02/sources/` and `17b-…/iter-02/sources/`.

**What We Know Works After This Phase:** Both canonical dirs exist, fully populated, dossiers are per-side. Legacy dir still on disk (untouched).

---

## Phase 3: Archive Retired Legacy Folders

### Goal

Move the three legacy dirs to `archive/concept_research_legacy/` with a top-level README explaining each disposition. After this phase, `knowledge/concept_research/` matches canonical IDs exactly.

### Assumption Under Test

That no live consumer breaks when the legacy dirs leave their original paths. (Pre-check confirmed: only the `_concept_downselect.md` historical artifacts and frozen `analyze_prompt.md` files reference these paths; no live scripts do.)

### Test Stencil (Write First)

```bash
# tests/test_archive.sh
set -euo pipefail
test -d archive/concept_research_legacy
test -f archive/concept_research_legacy/README.md
test -d archive/concept_research_legacy/17-laser-icf-direct-drive
test -d archive/concept_research_legacy/20-modular-hts-stellarator
test -d archive/concept_research_legacy/34-compact-spherical-tokamak-india
test ! -d knowledge/concept_research/17-laser-icf-direct-drive
test ! -d knowledge/concept_research/20-modular-hts-stellarator
test ! -d knowledge/concept_research/34-compact-spherical-tokamak-india
# canonical-diff is empty
comm -23 \
  <(ls knowledge/concept_research/ | grep -E '^[0-9]' | sort) \
  <(awk -F, 'NR>1 {print $1}' exploration/concept_analysis/table.csv | sort) \
  | wc -l | grep -q "^0$"
```

### Changes Required

#### 1. Archive dir + README
- [ ] `mkdir -p archive/concept_research_legacy`
- [ ] Write `archive/concept_research_legacy/README.md` with:
  - One section per archived concept: original path → archive path, disposition (`split` / `superseded by 20a+20b` / `dropped per crosswalk`), reference to spec, list of any consumers that still path-reference these dirs (historical `analyze_prompt.md` files + `resurface_reports/*.json`).
  - Note that absolute-path references in those historical artifacts now resolve under `archive/concept_research_legacy/`.

#### 2. Move legacy dirs
- [ ] `git mv knowledge/concept_research/17-laser-icf-direct-drive archive/concept_research_legacy/`
- [ ] `git mv knowledge/concept_research/20-modular-hts-stellarator archive/concept_research_legacy/`
- [ ] `git mv knowledge/concept_research/34-compact-spherical-tokamak-india archive/concept_research_legacy/`

### Validation

**Automated:**
- [ ] `bash tests/test_archive.sh` passes (canonical-diff returns 0 lines).
- [ ] `bash .project/active/concept-research-17-split/verify.sh` shows both diff directions empty.

**Manual:**
- [ ] Read README.md end-to-end; confirm each archived dir's disposition is documented.
- [ ] `git status` shows the moves as renames (no content diffs).

**What We Know Works After This Phase:** `knowledge/concept_research/` is canonically aligned. Every dir matches a current table.csv ID. No source data lost.

---

## Phase 4: Regenerate `SOURCE_INDEX.md` + Cross-Reference Check

### Goal

Bring `SOURCE_INDEX.md` in line with the new directory structure: all 40 canonical concepts listed (including 17a, 17b, 37, 38, 39), no retired IDs.

### Assumption Under Test

That hand-authoring `SOURCE_INDEX.md` from a directory walk produces output structurally consistent with the existing format. (Validated by diffing structure of unchanged sections.)

### Test Stencil (Write First)

```bash
# tests/test_source_index.sh
set -euo pipefail
INDEX=knowledge/concept_research/SOURCE_INDEX.md

# 1. exactly 40 concept sections
test "$(grep -cE '^### [0-9]' "$INDEX")" = "40"

# 2. contains canonical IDs
grep -q "^### 17a-laser-icf-hybrid-drive" "$INDEX"
grep -q "^### 17b-laser-icf-fast-ignition" "$INDEX"
grep -q "^### 37-magnetized-target-inertial-fusion-mtif" "$INDEX"
grep -q "^### 38-particle-accelerator-driven-fusion" "$INDEX"
grep -q "^### 39-spherical-tokamak-cs-free-p-b11" "$INDEX"

# 3. does NOT contain retired IDs
! grep -q "^### 17-laser-icf-direct-drive" "$INDEX"
! grep -q "^### 20-modular-hts-stellarator" "$INDEX"
! grep -q "^### 34-compact-spherical-tokamak-india" "$INDEX"

# 4. every listed concept matches a real directory
for id in $(grep -oE '^### [^[:space:]]+' "$INDEX" | sed 's/^### //'); do
  test -d "knowledge/concept_research/$id" || { echo "MISSING: $id"; exit 1; }
done
```

### Changes Required

#### 1. Regenerate index
**File:** `knowledge/concept_research/SOURCE_INDEX.md` (MODIFY)
- [ ] Keep the existing header (title + sync command + intro).
- [ ] For each canonical concept dir (sorted by ID), emit a `### {id}` section with Dossier, Iterations, Sources subsections matching existing format.
- [ ] Sources listed by walking each `iter-NN/sources/` directory; format each entry as in current index (`{name}` for dir + `{name}.md` for processed extraction).

#### 2. Live-script reference scan
- [ ] `grep -rln "concept_research/17-laser-icf-direct-drive\|concept_research/20-modular-hts-stellarator\|concept_research/34-compact-spherical-tokamak-india" scripts/ exploration/concept_analysis/scripts/` — confirmed empty during planning, re-confirm.
- [ ] If any live script reference appears, EITHER update it to the new canonical path OR document the deferral in the archive README.

### Validation

**Automated:**
- [ ] `bash tests/test_source_index.sh` passes.
- [ ] `bash verify.sh` still shows canonical diff empty.

**Manual:**
- [ ] Open `SOURCE_INDEX.md`, spot-check 5 sections (including 17a, 17b, 38, 20a, 39) for completeness and format consistency.

**What We Know Works After This Phase:** Index is current; all canonical IDs discoverable from the index; no retired IDs present.

---

## Phase 5: R2 Sync + Final Acceptance

### Goal

Bring the R2 binary tree in line with local. Run the full acceptance check from `spec.md`.

### Assumption Under Test

That `sync_research.sh push` correctly uploads the new 17a/17b dirs, and that `rclone delete` (or equivalent) cleanly removes the three retired remote dirs.

### Test Stencil (Write First — manual acceptance is the test here)

```bash
# Manual acceptance gate from spec.md
set -euo pipefail
# Spec acceptance criteria — all must pass
ls knowledge/concept_research/ | grep -E '^17' | sort -u | diff - <(printf "17a-laser-icf-hybrid-drive\n17b-laser-icf-fast-ignition\n")
test ! -d knowledge/concept_research/20-modular-hts-stellarator
test ! -d knowledge/concept_research/34-compact-spherical-tokamak-india
test -f knowledge/concept_research/17a-laser-icf-hybrid-drive/dossier.md
test -f knowledge/concept_research/17b-laser-icf-fast-ignition/dossier.md
grep -q "Differentiation Table Values" knowledge/concept_research/17a-laser-icf-hybrid-drive/dossier.md
grep -q "Differentiation Table Values" knowledge/concept_research/17b-laser-icf-fast-ignition/dossier.md
bash .project/active/concept-research-17-split/verify.sh
```

### Changes Required

#### 1. R2 push (new dirs only — additive, non-destructive)
- [ ] `./scripts/sync_research.sh push` from repo root.
- [ ] Confirm via `rclone ls r2:1cfe-research/concept_research/17a-laser-icf-hybrid-drive/ | head` that new content is up.

#### 2. R2 retire (destructive — confirm with user before running)
- [ ] **PAUSE — request user confirmation before destructive R2 ops.**
- [ ] On confirmation:
  - `rclone purge r2:1cfe-research/concept_research/17-laser-icf-direct-drive`
  - `rclone purge r2:1cfe-research/concept_research/20-modular-hts-stellarator`
  - `rclone purge r2:1cfe-research/concept_research/34-compact-spherical-tokamak-india`
- [ ] Verify each: `rclone ls r2:1cfe-research/concept_research/17-laser-icf-direct-drive/ 2>&1` returns "directory not found".

#### 3. Final acceptance
- [ ] Run the full acceptance block (test stencil above).
- [ ] Update spec's acceptance-criteria checkboxes.

### Validation

**Automated:**
- [ ] Acceptance block exits 0.
- [ ] All `verify.sh` checks pass.

**Manual:**
- [ ] Spot-check: pull a fresh copy via `./scripts/sync_research.sh pull 17a-laser-icf-hybrid-drive` (in a temp location) and verify binary artifacts arrive.

**What We Know Works After This Phase:** Local + R2 + index are all aligned. All spec acceptance criteria pass.

---

## Environment Setup

**See CLAUDE.md.** Notes specific to this work:
- All Python via `uv run python` (none required for this plan — pure shell/file ops).
- `rclone` needed for Phase 5 R2 ops; setup in `knowledge/concept_research/README.md`.

---

## Risk Management

| Risk | Mitigation |
|---|---|
| Shared-source partition rule produces dossier regressions on one side | Phase 2's per-column citation check catches this; spot-check is part of validation. |
| Renaming on R2 leaves orphans | Explicit `rclone purge` step in Phase 5, gated on user confirmation. |
| Historical `analyze_prompt.md` files break absolute paths | Archive README documents the new resolution path. No live consumer breaks (pre-checked). |
| OSTI sources mis-classified as shared when actually side-specific | Phase 1 explicitly opens each `output.md` to firm up assignment before partitioning. |
| Iteration numbering confusion | Decision codified in inline design table: iter-NN inherited from legacy; iter-04 is the split event. |
| User has uncommitted work in legacy dirs at execution time | Phase 1 pre_state.txt captures pre-state; `git status` check before Phase 2 starts. |

---

## Implementation Notes

[TO BE FILLED DURING IMPLEMENTATION]

### Phase 1 Completion
**Completed:** 2026-05-19
**Actual Changes:**
- Created `.project/active/concept-research-17-split/source_partition.csv` — 22 rows covering all legacy iter-01..03 source dirs. OSTI items classified by opening each `output.md`: `osti-servlets-purl-1438678` (Meier fast-ignition economics) → 17b; rest stayed shared per inspection.
- Created `.project/active/concept-research-17-split/verify.sh` (executable). Manifest roundtrip + canonical-diff + per-side + archive + SOURCE_INDEX checks all in one harness.
- Created `.project/active/concept-research-17-split/pre_state.txt` (1153 lines) — full `ls -laR` of the three legacy dirs plus sha256s of all dossier*.md/changelog.md files.
- `sciencedirect-…s0920379624001868` confirmed as Xcimer-specific (HYLIFE-III nuclear analysis of XEC = Xcimer Energy Corp) → 17a, not shared as initially noted in spec appendix.

**Issues Encountered:**
- Initial find depth in verify.sh was off by one (caught `images/` subdirs at depth 4). Fixed to depth 3 with explicit `grep -v ^images$` filter.

**Deviations:** None.

### Phase 2 Completion
**Completed:** 2026-05-19
**Actual Changes:**
- `knowledge/concept_research/17a-laser-icf-hybrid-drive/` and `17b-laser-icf-fast-ignition/` created.
- Sources partitioned via `apply_partition.sh` (committed under work-item dir). Counts: 17a = 18 source dirs (5 own + 13 shared), 17b = 18 (5 own + 13 shared); union covers all 22 legacy sources.
- Per-side `dossier.md` written from scratch (not promoted directly from seed) — seeds had near-identical bodies + cross-company commentary, so each canonical dossier was rewritten as side-only. Differentiation Table Values section locks in side-specific values; e.g., 17a `Repetition Rate` = Sub-Hz (high); 17b `Primary Heating` = Laser (fast ignition) (high, upgraded from medium).
- Per-side `changelog.md` written: inherited iter-01..03 entries (shared origin marked verbatim), plus a new iter-04 split entry on each side documenting classification resolution and source partitioning.

**Issues Encountered:**
- Classification of `osti-servlets-purl-1438678` (Meier fast-ignition economics) reassigned to 17b only (originally "shared" in manifest draft); Meier 2006 is fast-ignition-specific economics, much more relevant to Focused Energy than to Xcimer's HDD.

**Deviations:**
- Plan called for "promote seed dossier with shared-content merge"; reality was that seed dossiers were essentially the shared dossier with a one-paragraph header, so rewriting per-side from scratch (using both seed + shared as evidence) produced a cleaner result. No content lost — citations and reasoning carried over.

### Phase 3 Completion
**Completed:** 2026-05-19
**Actual Changes:**
- `git mv` of 3 legacy dirs → `archive/concept_research_legacy/`.
- `archive/concept_research_legacy/README.md` written — per-concept dispositions (split / superseded / dropped), known stale-path references documented, reversibility instructions included.
- Canonical alignment now passes both directions: `comm` diff is empty.

**Issues Encountered:** None.

**Deviations:** None.

### Phase 4 Completion
**Completed:** 2026-05-19
**Actual Changes:**
- `SOURCE_INDEX.md` regenerated by `regen_source_index.sh` (script committed under work-item dir). 40 concept sections, listing 17a/17b/37/38/39, no retired IDs.
- Source-type inference: primary heuristic is `raw.pdf`/`raw.html` presence; fallback reads `source_type` (and `source` extension) from `output.md` frontmatter when binaries aren't synced locally. 3 sources land as `[unknown]` (no output.md frontmatter; not on R2 yet) — acceptable for current state.
- Live-script reference scan re-confirmed: no script under `scripts/` or `exploration/concept_analysis/scripts/` references legacy paths (one comment in `oneoff_3d_clustering.py` noted as historical, no live behavior).

**Issues Encountered:**
- Pre-existing `SOURCE_INDEX.md` was significantly stale beyond just the 17/20/34 entries — source counts were way under-reported (e.g., concept 01 listed 8 sources, actual is 32). Regeneration fixes this incidentally.

**Deviations:** None.

### Phase 5 Completion
**Completed:** 2026-05-19
**Actual Changes:**
- Pre-push belt-and-suspenders archive to `~/archive/1cfe/`:
  - `concept_research_legacy/` — R2 snapshot pulled via `rclone copy` for all three retired prefixes (633 + 59 + 3 = 695 objects, ~47 MiB).
  - `concept_research_legacy_git_tracked/` — local copy of the git-tracked archive subtree.
  - `work-item_concept-research-17-split/` — copy of spec/plan/manifests/scripts.
  - `README.md` documenting contents + restore procedure.
- `./scripts/sync_research.sh push` ran. **Discovery**: the script uses `rclone sync` (mirror), not `rclone copy`, so the retired R2 prefixes were deleted as a side effect of the push (local mirror no longer contained them after Phase 3). Net effect = push-and-purge in one step. The separate `rclone purge` step planned for Phase 5 was therefore unnecessary; verified empty afterwards.
- R2 final state confirmed: retired prefixes empty; 17a/17b prefixes populated.

**Issues Encountered:**
- `sync_research.sh push` mirror semantics weren't surfaced in the plan — destructive R2 ops happened during push, not as a separate gated step. Mitigated by archiving first per user direction. Updating CLAUDE.md / sync_research.sh docstring should be considered a follow-up so future contributors don't get surprised.

**Deviations:** No separate `rclone purge` step needed (mirror push already deleted retired remote dirs). All acceptance criteria green: verify.sh PASS 26 / FAIL 0.

---

**Status:** Draft → In Progress → Complete
