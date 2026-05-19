# concept-downselect Rebase: Post-Implementation Audit & Loss Inventory

**Date:** 2026-05-19
**Auditor:** Claude (post-implementation review)
**Subject:** `.project/active/concept-downselect-merge/` (branch `concept-downselect-rebase`)
**Source of truth:** `/home/reid/1cfe/fusion-tea-concept-downselect` worktree @ `concept-downselect`
**Target:** `/home/reid/1cfe/fusion-tea` @ `concept-downselect-rebase`

## TL;DR

The Option B.3.a "drop the renumber" merge landed clean against every functional acceptance criterion in `spec.md`. No code, no test suite, no research dossier, and no source citation was silently lost. The audit did surface one minor documentation gap (the renumber crosswalk was not archived per FR-7) and one analytical content delta worth recording (downselect's `analyses/17/analysis.md` proton-coupling exposition is not present verbatim in main's `17b`, but its narrative is preserved through the Option C overlay). Everything else marked "skipped" was intentional and justified at the time of the skip.

---

## 1. Scope of the audit

This audit verifies the rebase against three independent benchmarks:

1. **Spec invariants** (`.project/active/concept-downselect-merge/spec.md` FR-1 → FR-11).
2. **Worktree-to-rebase file ledger** (`_downselect_filelist.txt`, 2348 entries) against `implementation_notes.md`.
3. **Functional probes** — `agentic-mbse status`, `pytest tests/scoring_v2/`, `seed_registry.py`, `run_analysis.py status`, all green.

Where this audit differs from the Phase 6 self-audit recorded in `plan.md` lines 446-467: I re-derived the comparison from the source worktree, did not consult the existing ledger first, and flagged any delta a future maintainer might mistake for a loss — even if the team made it deliberately.

---

## 2. Potential information losses

### 2.1 Crosswalk archive — **MINOR DOC GAP, NOT A DATA LOSS**

**Spec invariant:** FR-7 / AC-8 require `scripts/renumber/renumber.py` to be absent, and explicitly **allow** `scripts/renumber/crosswalk.csv` to survive *if and only if* moved under an archival path so it cannot be mistaken for live tooling.

**Observed state:**
- `/home/reid/1cfe/fusion-tea/scripts/renumber/` — does not exist ✓
- `/home/reid/1cfe/fusion-tea/archive/` — does not contain a crosswalk ✗
- Source worktree retains `scripts/renumber/crosswalk.csv` at the source branch tip ✓

**Implication:** The rebase neither carried the crosswalk forward nor archived it. The spec wording was permissive ("MAY exist if and only if"), so this is **not a hard violation**, but the spec's Scope section ("In Scope") committed to "Capturing the renumber crosswalk … on `main` as a historical record". That commitment was not honored.

**Loss severity:** Low. The crosswalk is preserved on the source branch and reproducible from the renumber tool. Future readers of `main` cannot, however, see Mallory's intended ID mapping without checking out the source branch. **Recommendation:** copy the file as `archive/concept-downselect-renumber-crosswalk.csv` with a one-line README marking it historical-only, before the PR lands.

### 2.2 Downselect `analyses/17/analysis.md` proton-coupling exposition — **MITIGATED BY OVERLAY**

The downselect-side `analyses/17-laser-icf-direct-drive-fast-ignition/analysis.md` contains ~200 lines on Target Normal Sheath Acceleration (TNSA), proton-beam propagation through the cone structure, and hot-spot energy-deposition geometry that are not present in main's `analyses/17b-laser-icf-fast-ignition/analysis.md`. Main's 17b is shorter (~200 lines) and was last edited 2026-04-19; the downselect file is ~400 lines and was last edited 2026-05-18.

**Why this is not flagged as a hard loss:** the downselect version was captured under Option C as `analyses/17b-laser-icf-fast-ignition/synthesis_concept_downselect.md` and as the corresponding `dossier_17b_focused_concept_downselect.md` under the shared 17 research dir. The *narrative* is preserved; what differs is which document carries it.

**Risk:** A future reader looking only at `17b/analysis.md` will not see the TNSA physics discussion. Cross-referencing requires opening the `*_concept_downselect.md` siblings. The `implementation_notes.md` ledger records this but the analysis.md itself does not link to its legacy sibling.

**Recommendation (non-blocking):** add a one-line "See also: synthesis_concept_downselect.md for additional TNSA/cone physics context" pointer in `17b/analysis.md` so the overlay is discoverable.

### 2.3 Pre-Wave-B analysis artifacts on concepts 01-16, 18, 19, 35, 36 — **INTENTIONAL, JUSTIFIED**

The ledger documents ~64 `model_output.txt`, `model_setup.py`, `synthesis.md`, and `iter-N/analyze_prompt.md` files under unchanged concepts as `[skipped: superseded by main's Wave B data-hygiene fixes]`. Spot-check confirms downselect's numbers are pre-correction (e.g., concept 01 LCOE 641.6 $/MWh vs. main's post-Wave-B 571.1 $/MWh). Porting them would have regressed main's data hygiene.

**Loss severity:** None — main's values are demonstrably the corrected ones.

### 2.4 Renumber-driven file moves on `analyses/` — **INTENTIONAL, FR-1 INVARIANT**

124 R100 renames (e.g., `21-spherical-tokamak-hts/` → `22-spherical-tokamak-hts/`) and the corresponding `_C2/_HERITAGE` table remap in `scoring.py` were skipped en bloc. FR-1 (ID-space byte-identity) and FR-7 (no renumber tool) make this a non-negotiable design decision, ratified by PR #16's `6d32f4d`.

**Loss severity:** None — the renumber's cosmetic value is exactly what the spec scoped out.

### 2.5 `scripts/renumber/{manifest.json,manifest.diff.txt,inventory.md,r2_ops.log,reanalyze.txt}` — **INTENTIONAL**

Companion files of the dropped renumber tool. All ledger-skipped as `[renumber tooling artifacts]`. No analytical content; pure runtime traces of an operation we deliberately did not run.

### 2.6 `features/34-compact-spherical-tokamak-india.yaml` — **INTENTIONAL (Pranos drop)**

Pranos (old-34) was dropped on main by PR #16. Carrying its scoring_v2 feature YAML would create a ghost concept. Skipped consistent with FR-1.

### 2.7 `.project/active/concept-renumber-migration/*` planning artifacts — **INTENTIONAL**

Spec, design, and plan docs for the dropped renumber. Not ported. No loss because the work item itself was retired.

**Net assessment:** Exactly one item (§2.1, crosswalk archive) is a real gap relative to the spec's stated intent. One item (§2.2) is a discoverability concern, not a content loss. Everything else is intentional and documented.

---

## 3. Key deltas — worktree vs. rebase analysis.md

| Concept | Worktree dir (DS ID) | Rebase dir (main ID) | DS lines | Rebase lines | Substantive delta |
|---|---|---|---|---|---|
| MTIF / NearStar | `37-magnetized-target-inertial-fusion/` | `37-magnetized-target-inertial-fusion-mtif/` | ~350 | ~450 | Rebase has **firmer engineering critique** (rail-shot lifetime quantified to 8 orders of magnitude gap; explicit 190 $/MWh nominal LCOE + availability elasticity). DS has softer framing, including a coal-retrofit strategic angle the rebase downplays. |
| SHINE / ADF | `38-accelerator-driven-fusion/` | `38-particle-accelerator-driven-fusion/` | ~250 | ~350 | Rebase carries deeper subsystem cost breakdown (accelerator capex, target fab cost anchors). DS narrative is preserved verbatim in `dossier_concept_downselect.md`. |
| ENN / p-B11 ST | `39-cs-free-spherical-tokamak-pb11/` | `39-spherical-tokamak-cs-free-p-b11/` | ~300 | ~400 | Rebase has additional iter passes (iter-1 + iter-2). DS unique content (roadmap timeline emphasis) lives in `dossier_concept_downselect.md`. |
| Xcimer / hybrid drive | `27-laser-icf-hybrid-direct-drive/` | `17a-laser-icf-hybrid-drive/` | ~400 | ~300 (canonical) + DS overlay | Different document instances. Rebase 17a has deeper subsystem cost breakdowns ($0.40/J capacitor target vs. $10/J market). DS 27 emphasizes TRUMPF Feb-2026 whitepaper; same citation appears in rebase. Both authored ~April–May 2026. |
| Focused Energy / fast ignition | `17-laser-icf-direct-drive-fast-ignition/` | `17b-laser-icf-fast-ignition/` | ~400 | ~200 (canonical) + DS overlay | **DS contains ~200 lines on TNSA proton physics not in rebase 17b.** Preserved through `17b/synthesis_concept_downselect.md` and the shared `dossier_17b_focused_concept_downselect.md`. See §2.2. |

**Slug differences (informational, not losses):**

| Concept | Worktree slug | Rebase slug |
|---|---|---|
| 37 | `magnetized-target-inertial-fusion` | `magnetized-target-inertial-fusion-mtif` |
| 38 | `accelerator-driven-fusion` | `particle-accelerator-driven-fusion` |
| 39 | `cs-free-spherical-tokamak-pb11` | `spherical-tokamak-cs-free-p-b11` |

These slug differences trace back to PR #16's CSV translate (`phase_1a/translate_csv_to_ours.py`) and main's later normalization; the rebase preserves main's slugs per FR-1.

---

## 4. Numbering differences — full crosswalk

The renumber that was dropped is documented here for future reference (since `crosswalk.csv` was not archived — see §2.1):

| Worktree (DS) ID | Main ID (canonical) | Company / Concept | Disposition |
|---|---|---|---|
| 01–16 | 01–16 | unchanged | identical |
| 17 | 17b | Focused Energy (fast ignition) | DS relabel reversed |
| 27 | 17a | Xcimer (hybrid direct drive) | DS relabel reversed |
| 18, 19 | 18, 19 | unchanged | identical |
| 20 | 20a | (various) | DS suffix-strip reversed |
| 21 | 20b | (various) | DS suffix-strip reversed |
| 22 | 21 | spherical-tokamak-hts | DS +1 shift reversed |
| 23 | 22 | (next concept) | DS +1 shift reversed |
| … | … | shift continues through 34→33 | all DS shifts reversed |
| (dropped) | — | NIF commercialization (old-30) | both branches drop |
| (dropped) | — | Pranos India (old-34) | both branches drop |
| 35, 36 | 35, 36 | unchanged | identical |
| 37 | 37 | NearStar MTIF | net-new, both branches |
| 38 | 38 | SHINE accelerator-driven | net-new, both branches |
| 39 | 39 | ENN p-B11 ST | net-new, both branches |

**Key invariants honored by the rebase:**
- Main's 17a (Xcimer) and 17b (Focused) remain distinct directories; downselect's collapse of 17a→27 and 17b→17 was not propagated.
- Net-new 37/38/39 IDs are identical across branches by coincidence of arrival; the concept *identities* match (NearStar=37, SHINE=38, ENN=39).
- `Research ID` pinning that Mallory used to preserve dossier paths under renumber is moot here because no rename happens.

---

## 5. How downselect pipeline changes were resolved

The downselect branch carried three pipeline-touching changes. Each was reconciled differently against main's v3 schema:

### 5.1 `exploration/scoring_v2/` — port + regenerate

- **Framework code** (`extract.py`, `score.py`, `lib/`, `embeddings/`, weights): ported verbatim via cherry-picks `f55e35a` and `30ecdd8`.
- **Schema reconciliation:** `tritium_breeding` and `neutron_management` switched from `extractor: taxonomy` to `extractor: manual` because their source columns were dropped from `table.csv` by ontology v3 (PR #16). Pre-v3 values for concepts 01–36 retained as authoritative; 37/38/39 hand-filled. Confirmed in `exploration/scoring_v2/schema.yaml`.
- **Feature YAMLs:** regenerated via `extract.py --bulk-taxonomy` against main's v3 `table.csv`, not ported as-is from downselect (which had pre-v3 IDs). Output: 40 yamls; Pranos yaml deleted. The downselect-only `34-compact-spherical-tokamak-india.yaml` is correctly absent.
- **`table.csv` fill-in:** 17 enum cells on rows 37/38/39 filled with `"N/A"` (Mallory's CSV translate had left them empty; scoring_v2 enum schema requires N/A for non-applicable).
- **Test result delta:** rebase shows **23 passed / 3 skipped / 4 xfailed**, vs. downselect's `30ecdd8` commit-message claim of 26/3/1. The three newly-xfailed tests (`test_xlsx_collapse[01-…-5.0]`, `test_xlsx_collapse[08-frc-…-4.65]`, `test_slice1_preservation_under_slice1_weights`, plus `test_plant_level_modularity_ordering` in test_embeddings.py) are **strict xfails** caused by ontology-v3 reclassification of Helion's Magnet Type (`Pulsed EM` → `Resistive`), which lowers `coils_rating` and shifts the slice-1 baselines. Re-baselining was explicitly deferred to a future slice-3 work item. Documented as an FR-4 allowed deviation.
- **Headline AC-13 probe:** ordering is preserved (Helion > CFS > Stellarator) but absolute Helion score shifted from 4.80 → 4.20. Spec-acceptance check passed because AC-13 measures ordering intent, not exact float match.

### 5.2 `exploration/concept_analysis/scoring.py` `_C2`/`_HERITAGE` — keep main's

Downselect's `scoring.py` remapped `_C2`/`_HERITAGE` tables onto the 39-ID scheme. Main's `scoring.py` has Mallory's architecture-driven classification keyed to main's IDs. The rebase takes main's version untouched. Downselect's remap was an artifact of the dropped renumber and would have been internally inconsistent with main's ID space.

### 5.3 `concept_registry.json`, `decision_tree.json`, `SOURCE_INDEX.md` — regenerated, not merged

These three were modified on both branches with mutually exclusive ID schemes. Resolution strategy: do not text-merge; let `seed_registry.py` and the source-index generator emit fresh outputs against the post-rebase `table.csv`. Phase 6 confirmed `seed_registry.py` exits 0 and emits 40 concepts.

### 5.4 `uv.lock` — `uv sync`, not manual merge

The plan anticipated heavy `uv.lock` conflict. Actuality: only one conflict (during `f7f5da8`), resolved take-ours since `pyproject.toml` was unchanged. Phase 3's expected `uv sync` after scoring_v2 cherry-picks was not needed because the cherry-picks landed clean.

### 5.5 `phase_1a/translate_csv_to_ours.py` and `phase_2a/column_map.py` — untouched

Both branches' Heating Type / Driver Type wiring lives on main; downselect did not touch these files, so the merge is a no-op for them. Verified.

---

## 6. Outstanding items

1. **Archive the crosswalk** (§2.1). One file move + one-line README. Should land before the PR opens.
2. **Add a back-reference from `17b/analysis.md` to its `*_concept_downselect.md` siblings** (§2.2) so the TNSA proton physics narrative is discoverable from the canonical analysis. Non-blocking but useful.
3. **Slice-3 follow-up work item** to re-baseline scoring_v2 tests against v3 Helion Magnet Type. Already noted in Phase 3 implementation notes; should be opened as a fresh WI before the four xfails rot.

## 7. Acceptance-criteria reconciliation

| AC | Verified by | Status |
|---|---|---|
| AC-1 ID space byte-identity | `git ls-tree` diff on `analyses/` shows 3 additions, 0 deletions, 0 renames | ✓ |
| AC-2 v3 CSV schema | header check on `table.csv` | ✓ |
| AC-3 row identity | identity-column diff on pre-existing rows = 0 | ✓ |
| AC-4 meta-analysis dossiers present | spot-checked 5 dossiers | ✓ |
| AC-5 scoring_v2 tests | 23/3/4 (vs. 26/3/1 baseline) — deviation documented per FR-4 | ✓ with documented deviation |
| AC-6 net-new 37/38/39 non-stub | all >200 lines analysis.md | ✓ |
| AC-7 split-17 content | overlays present under 17a and 17b | ✓ |
| AC-8 renumber tool absent | `scripts/renumber/` does not exist | ✓ |
| AC-9 pipeline green | three commands all exit 0 | ✓ |
| AC-10 Wave B fixes intact | all 6 commits present in HEAD ancestry | ✓ |
| AC-11/12 ledger reconciliation | 2411 files classified, 0 unaccounted | ✓ |
| AC-13 scoring ordering | Helion > CFS > Stellarator preserved | ✓ (ordering, not absolute) |
| Quality: full pytest | not re-run in audit | not verified by this audit |
| Quality: agentic-mbse status, no orphans | exit 0 in Phase 6 | ✓ |
| Quality: branch preserved | source worktree intact at branch tip | ✓ |

---

## UPDATE — 2026-05-19 (post-audit cleanup)

The two recommendations from §6/§8 were actioned before the PR opened:

1. **Crosswalk archived.** `archive/concept-downselect-renumber-crosswalk.csv` now holds Mallory's 38→39 ID mapping verbatim from the source branch's `scripts/renumber/crosswalk.csv` (42 lines). A short `archive/README.md` marks the file as historical-only and points back to this report for context. FR-7's "MAY exist if and only if" archival clause is now satisfied; the spec's "In Scope" commitment to capture the crosswalk on `main` is honored.

2. **17b back-reference added.** `exploration/concept_analysis/analyses/17b-laser-icf-fast-ignition/analysis.md` now opens with a `> See also:` pointer to `synthesis_concept_downselect.md` and the legacy dossier, so the TNSA proton-coupling narrative captured under Option C is discoverable from the canonical analysis file. Discoverability concern (§2.2) closed.

No other items remain from §6 except the slice-3 re-baseline follow-up, which is a future WI rather than a pre-PR fix. The PR can open with full spec-AC coverage including the previously-permissive FR-7 archival clause now met.

## 8. Verdict

The rebase is **lossless within the spec's definition of loss**. The single FR-7 deviation (crosswalk archival) is permissive in the spec text and recoverable in five minutes. The downselect proton-coupling exposition is preserved through the Option C overlay but is not maximally discoverable. The three new scoring_v2 xfails are intentional v3-data deviations, not regressions. Nothing else flagged.

**Recommended pre-PR fix list:**
1. `cp /home/reid/1cfe/fusion-tea-concept-downselect/scripts/renumber/crosswalk.csv archive/concept-downselect-renumber-crosswalk.csv` + a one-line README.
2. Optional: add a `> See also: synthesis_concept_downselect.md` line at the top of `analyses/17b-laser-icf-fast-ignition/analysis.md`.

After those, the PR can be opened with full spec-AC coverage.
