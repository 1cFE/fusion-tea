# Spec: Concept Research 17-Split Reconciliation

**Status:** Implementation Complete
**Owner:** Reid W
**Created:** 2026-05-19 15:28 PDT
**Complexity:** MEDIUM
**Branch:** concept-downselect-rebase

---

## Work Item Summary

Reconcile `knowledge/concept_research/` with the canonical concept ID list in `exploration/concept_analysis/table.csv`. The split-17 work (Xcimer vs. Focused Energy) landed in `concept_analysis/analyses/` and as supplemental dossier files inside the legacy `17-laser-icf-direct-drive/` folder, but the research tree itself was never partitioned. Also archive two retired pre-split parent folders (`20-modular-hts-stellarator`, `34-compact-spherical-tokamak-india`) and regenerate the stale `SOURCE_INDEX.md`. Done state: every directory under `concept_research/` corresponds to a current canonical ID, and `SOURCE_INDEX.md` reflects that.

## Why This Matters Now

The downselect-rebase work introduced the split (17a/17b) and retired three folders, but the research tree on disk still uses pre-split IDs. Any pipeline that globs `concept_research/*/` (analysis, scoring, the explorer) currently sees a mix of canonical and stale IDs, which silently biases anything that joins on directory name. Fixing it now — before the next analysis rerun — avoids a wave of downstream corrections.

## Key Bets / Constraints

- **Bet:** The existing per-iter source filenames (`xcimer-*`, `focused-energy-*`, plus shared HYLIFE/LLNL/ARPA-E background) are clean enough to partition by inspection. No fresh research-pipeline run is required to do the structural split.
- **Bet:** The two `dossier_17{a,b}_*_concept_downselect.md` files (already present inside the legacy dir) plus the deeper per-side `analysis.md` in `concept_analysis/analyses/` carry enough per-side content to seed canonical `dossier.md` files.
- **Constraint:** No data loss. Every source artifact, dossier, changelog, and iter file in the legacy folders must be preserved (moved or archived, not deleted).
- **Constraint:** The R2 binary tree (`r2:1cfe-research/concept_research/`) must stay in sync — renames need a `rclone` push after local restructuring.
- **Constraint:** A targeted research rerun on 17a and 17b to fill known gaps (Focused Energy paywalled J. Fusion Energy paper, Xcimer ASPEN parameters, classification lock-in) is **out of scope** for this work item; it is a recommended follow-up.
- **Non-goal:** Re-running or re-validating the analysis pipeline (`concept_analysis/analyses/`); that tree is already canonically named and is the upstream reference.
- **Non-goal:** Touching the archived downselect renumber crosswalk (`archive/concept-downselect-renumber-crosswalk.csv`); it was already rejected and archived.

---

## Business Goals

### Why This Matters

Concept IDs are the join key across every layer of the project (scoring features, explorer routes, analysis runs, traceability citations). When the research tree and the canonical table disagree, every downstream consumer must either special-case the legacy IDs or silently mis-join. The cost of leaving this drift in place compounds with every new pipeline run and every new contributor who has to mentally maintain "what current IDs are, and what `concept_research/` *actually* has."

### Success Criteria

- [ ] Every directory under `knowledge/concept_research/` matches an ID in `exploration/concept_analysis/table.csv` (or is in `archive/`).
- [ ] `17a-laser-icf-hybrid-drive/` and `17b-laser-icf-fast-ignition/` exist with per-side `dossier.md`, `changelog.md`, and properly partitioned `iter-NN/sources/`.
- [ ] The retired folders (`20-modular-hts-stellarator/`, `34-compact-spherical-tokamak-india/`) are archived with breadcrumb pointers.
- [ ] `SOURCE_INDEX.md` lists all 40 canonical concepts and none of the retired IDs.
- [ ] R2 binary tree reflects the new structure (or a documented sync command is queued for the user to run).

### Priority

P1 — blocking clean execution of the next analysis/scoring run, but not gating any in-flight modeling work. Should be completed before any further pipeline reruns that consume `concept_research/`.

---

## Problem Statement

### Current State

`knowledge/concept_research/` contains 40 ID-prefixed directories. Compared to canonical (`concept_analysis/table.csv`):

| Drift | Detail |
|---|---|
| Missing canonical IDs | `17a-laser-icf-hybrid-drive/`, `17b-laser-icf-fast-ignition/` |
| Legacy pre-split parents | `17-laser-icf-direct-drive/`, `20-modular-hts-stellarator/` |
| Dropped concept on disk | `34-compact-spherical-tokamak-india/` (marked `drop` in archive crosswalk) |
| Stale index | `SOURCE_INDEX.md` ends at concept 36 (missing 37/38/39), still references retired IDs |

Inside the legacy `17-laser-icf-direct-drive/`:
- iter-01..03/sources/ contain ~22 source artifacts mixing Xcimer-only, Focused-only, and shared-background sources.
- `dossier.md` (iter-2) is the old shared write-up.
- `dossier_17a_xcimer_concept_downselect.md` and `dossier_17b_focused_concept_downselect.md` were overlaid in commit `a704c38` as per-side seeds (iter-0, low confidence).

### Desired Outcome

The research tree on disk is the authoritative listing of concepts the project tracks, matches the canonical ID list, and any consumer that globs `concept_research/*/` sees exactly the current concept set.

---

## Scope

### In Scope

- Create `knowledge/concept_research/17a-laser-icf-hybrid-drive/` and `17b-laser-icf-fast-ignition/` with:
  - `dossier.md` promoted/reconciled from the `dossier_17{a,b}_*_concept_downselect.md` seed plus relevant content from the shared `dossier.md`.
  - `changelog.md` carrying forward the relevant iter-01/iter-02 entries from the shared changelog, plus an iter-03 entry recording the split.
  - `iter-NN/sources/` populated by partitioning the legacy sources by company (see partition table in Appendix).
- Retire `17-laser-icf-direct-drive/` to `archive/concept_research_legacy/` with a README pointer to 17a/17b.
- Archive `20-modular-hts-stellarator/` and `34-compact-spherical-tokamak-india/` to `archive/concept_research_legacy/` with breadcrumb READMEs.
- Regenerate `SOURCE_INDEX.md` to list all 40 canonical concepts and only canonical concepts.
- Update R2 to match (push restructured tree).

### Out of Scope

- A fresh research-pipeline iteration on 17a or 17b to fill substantive gaps (paywalled Focused Energy papers, Xcimer ASPEN parameters, classification lock-in). Recommended follow-up.
- Any change to `exploration/concept_analysis/analyses/` (already canonically named).
- Any change to scoring, the explorer, or analysis code that joins on concept ID — they will benefit automatically, but their own state is not in scope.
- Touching concepts outside the three named legacy IDs.

### Edge Cases & Considerations

- Some sources are genuinely shared background (HYLIFE-II/III, LLNL economics model, ARPA-E IFE workshop, general laser-physics surveys). The partition strategy needs an explicit rule: copy to both sides, or place in a `shared/` subdir, or assign to whichever side actually cites it. Design must choose one.
- The shared `dossier.md` has richer classification commentary (esp. on whether Focused Energy is "direct drive" vs. "fast ignition") than the per-side seed dossiers. Merging — not just promoting — is required so per-side dossiers don't regress in detail.
- Iteration numbering: the legacy dir has iter-01..03; the per-side seed dossiers are iter-0. The split itself should be recorded as an iter event (likely iter-03 on the new per-side changelogs, with iter-01/02 entries inherited).
- R2 sync after rename: `sync_research.sh push` will upload the new dirs but does not delete the old ones; an explicit `rclone delete` or `sync` is needed to retire R2 copies.
- Companion analyses dirs in `concept_analysis/analyses/17a-…/17b-…/` reference sources by path. If any of them path-reference `concept_research/17-laser-icf-direct-drive/…`, those references will break. Design must check and decide whether to rewrite citations or leave them as legacy pointers into `archive/`.

---

## Requirement Selection Notes

Requirements below cover the *structural* contract: what must exist, what must not, and what must not be lost. They deliberately do not prescribe (a) the partition strategy for shared sources, (b) the dossier merge mechanics, or (c) the exact archive layout — those are design decisions.

---

## Requirements

### Functional Requirements

1. **FR-1** [from user]: The directory `knowledge/concept_research/17a-laser-icf-hybrid-drive/` MUST exist after this work, containing a `dossier.md` whose primary subject is Xcimer Energy's KrF-excimer Hybrid Direct Drive approach.
2. **FR-2** [from user]: The directory `knowledge/concept_research/17b-laser-icf-fast-ignition/` MUST exist after this work, containing a `dossier.md` whose primary subject is Focused Energy's DPSSL + proton-fast-ignition approach.
3. **FR-3** [from user]: Every source artifact (file or subdirectory) currently under `knowledge/concept_research/17-laser-icf-direct-drive/iter-*/sources/` MUST end up reachable from at least one of: (a) the new `17a-…` dir, (b) the new `17b-…` dir, (c) an archived copy of the legacy dir. No source MUST be deleted outright.
4. **FR-4** [from user]: The legacy directories `17-laser-icf-direct-drive/`, `20-modular-hts-stellarator/`, and `34-compact-spherical-tokamak-india/` MUST be removed from `knowledge/concept_research/` after this work and MUST be archived under a single location (e.g., `archive/concept_research_legacy/`) with a top-level README explaining the disposition of each.
5. **FR-5** [from user]: `knowledge/concept_research/SOURCE_INDEX.md` MUST list exactly the 40 canonical concepts from `exploration/concept_analysis/table.csv` (no legacy IDs, no missing IDs).
6. **FR-6** [INFERRED]: After the split, the set of directory names under `knowledge/concept_research/` matching `^[0-9]+[a-z]?-` MUST be a strict subset of the ID column of `exploration/concept_analysis/table.csv`. (A verification check enforcing this should run as part of acceptance.)
7. **FR-7** [INFERRED]: Each new per-side dossier MUST carry forward the substantive classification, citation, and confidence content from both the corresponding `dossier_17{a,b}_*_concept_downselect.md` seed AND the shared `dossier.md` — i.e., no regression in evidence/citation density relative to the shared dossier.
8. **FR-8** [INFERRED]: Each new per-side `changelog.md` MUST include the original iter-01 and iter-02 changelog entries (or an explicit reference to them in the archived legacy `changelog.md`) plus a new iter-03 entry recording the split itself with date and rationale.
9. **FR-9** [INFERRED]: An R2 sync operation MUST be performed (or queued as an explicit follow-up command for the user to run) so the remote binary tree matches the local restructuring; the work item is not "done" while local and R2 are divergent.

### Non-Functional Requirements

- **Traceability**: The split commit message and the archived legacy README MUST together let a future reader reconstruct which sources went to which side and why.
- **Reversibility**: The change MUST be reversible from the archive contents alone (no information about the legacy state lives only in git history or in this spec).

---

## Acceptance Criteria

### Core Functionality

- [ ] `ls knowledge/concept_research/ | grep -E '^17'` returns exactly `17a-laser-icf-hybrid-drive` and `17b-laser-icf-fast-ignition` — no `17-laser-icf-direct-drive`.
- [ ] `ls knowledge/concept_research/` contains no `20-modular-hts-stellarator` or `34-compact-spherical-tokamak-india`.
- [ ] `archive/concept_research_legacy/` (or equivalent) exists with `17-laser-icf-direct-drive/`, `20-modular-hts-stellarator/`, `34-compact-spherical-tokamak-india/`, and a README explaining each disposition.
- [ ] `17a-laser-icf-hybrid-drive/dossier.md` and `17b-laser-icf-fast-ignition/dossier.md` exist; each has a `## Differentiation Table Values` section with per-column citations.
- [ ] Each new dir has a `changelog.md` including at least one entry that explicitly references the legacy-tree partition (date, source files moved/copied, rationale).
- [ ] Per-side `iter-NN/sources/` directories exist and the set of source basenames across 17a + 17b ⊇ the set of source basenames previously under the legacy dir.
- [ ] `SOURCE_INDEX.md` lists 17a, 17b, 37, 38, 39 and does not list 17, 20-modular-hts-stellarator, or 34-compact-spherical-tokamak-india.
- [ ] Diff check: `comm -23 <(ls knowledge/concept_research/ | grep -E '^[0-9]') <(awk -F, 'NR>1 {print $1}' exploration/concept_analysis/table.csv | sort)` is empty.

### Quality & Integration

- [ ] R2 push (`./scripts/sync_research.sh push`) completes successfully, or a follow-up sync command is documented in the work-item handoff.
- [ ] No source markdown file referenced by `concept_analysis/analyses/17a-…/` or `17b-…/` is broken (spot-check by grepping those analyses for path references into the legacy tree).
- [ ] Existing concept-explorer/scoring runs continue to load all 40 concepts.

---

## Next-Stage Handoff

**Settled in this spec:**
- The three legacy folders to retire (17, 20-modular, 34-india).
- That 17a is Xcimer and 17b is Focused Energy.
- That no fresh research-pipeline run is required for this work item.
- That all legacy material must end up in `archive/` rather than being deleted.

**Design must figure out:**
- Partition rule for shared-background sources (duplicate into both sides? `shared/` subdir? assign to first-citing side?).
- Iteration numbering on the new per-side trees (inherit iter-01/02 by copy? or restart at iter-01 with a single split-event entry?).
- Whether to rewrite citation paths in `concept_analysis/analyses/17a/17b/` files that point at the legacy tree, or leave them as legacy-archive pointers.
- Archive layout: one `archive/concept_research_legacy/` umbrella, or per-concept archive folders?
- Whether to regenerate `SOURCE_INDEX.md` by hand or via `scripts/migrate_research.py --reindex`.
- Whether the R2 sync includes deleting retired remote dirs explicitly, or only adds the new ones.

**Watch-outs for design:**
- The shared `dossier.md` has classification content (esp. Focused Energy's direct-drive-vs-fast-ignition ambiguity) richer than the seed dossiers. Merge carefully so that nuance isn't lost.
- The downselect seed dossiers were written as "treat as low confidence until re-sourced" — their confidence flags should not be propagated unchanged into the canonical per-side dossiers.
- `dossier_17a_xcimer_concept_downselect.md`'s body still contains shared/Focused-Energy claims (per its own header note). Filtering that content before promotion is required.
- Renaming on R2 is not atomic — local push followed by remote delete of stale paths is two operations; if the user runs only the push, the R2 tree will have *both* old and new dirs.

---

## Related Artifacts

- **Audit context:** Conversation history (2026-05-19) audit of `knowledge/concept_research/` vs `exploration/concept_analysis/table.csv`.
- **Canonical ID list:** `exploration/concept_analysis/table.csv`
- **Archived crosswalk (rejected renumbering):** `archive/concept-downselect-renumber-crosswalk.csv`
- **Split-17 overlay commit:** `a704c38` (created the seed `dossier_17{a,b}_*_concept_downselect.md` files)
- **Per-side deep analyses:** `exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/`, `…/17b-laser-icf-fast-ignition/`
- **Design:** `.project/active/concept-research-17-split/design.md` (to be created)
- **Plan:** `.project/active/concept-research-17-split/plan.md` (to be created)

---

## Appendix — Source Partition Inventory

Inventory of the 22 sources under `knowledge/concept_research/17-laser-icf-direct-drive/iter-*/sources/`, with proposed partition. **Design decides the final rule for the shared bucket.**

### Iter-01 (2 sources)
| Source | Side |
|---|---|
| `xcimer-energy-approach` | 17a |
| `focused-energy-technology` | 17b |

### Iter-02 (4 sources)
| Source | Side |
|---|---|
| `xcimer-science-page` | 17a |
| `xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb` | 17a (Xcimer whitepaper) |
| `focused-energy-callahan-interview` | 17b |
| `hylife-energy-conversion-notes` | shared (Xcimer chamber heritage; cited by 17a primarily) |

### Iter-03 (16 sources)
| Source | Side (proposed) |
|---|---|
| `prnewswire-news-releases-focused-energy-and-amplitude-enter` | 17b |
| `arpa-e-sites-default-files-migrated-a05-zuegel` | shared (ARPA-E IFE workshop) |
| `digital-ark-67531-metadc626683` | shared (HYLIFE / LLNL ref) |
| `laserfocusworld-lasers-sources-article-14274951-can-high` | shared (laser tech survey) |
| `lasers-sites-lasers-files-2023-11-haefner-ilt-ife-workshop` | shared (IFE workshop) |
| `llnl-53961-llnl-releases-generalized-economics-model-fusion` | shared (LLNL economics) |
| `opg-oe-abstract-cfm` | shared (Optica abstract) |
| `optica-opn-home-articles-volume-34-june-2023-features` | shared (laser physics feature) |
| `osti-biblio-7021072` | shared (OSTI; needs content check) |
| `osti-servlets-purl-1438678` | shared (OSTI; needs content check) |
| `osti-servlets-purl-15013230` | shared (OSTI; needs content check) |
| `osti-servlets-purl-2561299` | shared (OSTI; needs content check) |
| `osti-servlets-purl-6137961` | shared (OSTI; needs content check) |
| `osti-servlets-purl-622702` | shared (OSTI; needs content check) |
| `pmc-articles-pmc7658748` | shared (PMC review) |
| `sciencedirect-science-article-pii-s0920379624001868` | shared (likely HYLIFE-III nuclear analysis → 17a leaning) |

**Summary**: 5 clearly 17a, 4 clearly 17b, 13 shared (most being IFE-physics or LLNL/HYLIFE background that both sides legitimately draw on). The OSTI items need a quick title/content check during implementation to firm up the side or confirm "shared."

---

**Next Steps:** After approval, proceed to `/_my_design` (or directly to `/_my_plan` if the partition rule is the only open design question and is decided inline).
