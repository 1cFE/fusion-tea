# Batch Pipeline Run — All Concepts Through Approval

**Status**: Not Started
**Created**: 2026-04-05
**Branch**: `design-space-explore`

---

## Current State Inventory

### Already Complete (skip entirely)
| Concept | State | Notes |
|---------|-------|-------|
| `21-spherical-tokamak-hts` | **Approved** | Done |

### Legacy Synthesized (need review → address-review → re-synthesize → approve)
| Concept | State | Notes |
|---------|-------|-------|
| `02-acoustic-icf-sonofusion` | S* (stale) | Legacy iter-1/INTERRUPTED, has synthesis |
| `03-laser-icf-liquid-jet-target` | S | Legacy iter-1/INTERRUPTED, has synthesis |
| `04-laser-icf` | S | Legacy iter-1/INTERRUPTED, has synthesis |
| `05-planar-coil-stellarator` | S | Legacy iter-1/INTERRUPTED, has synthesis |
| `06-magnetic-mirror` | S | Legacy iter-1/INTERRUPTED, has synthesis |
| `08-frc-w-direct-conversion` | S* (stale) | Legacy, iter-3/FAIL but has synthesis |
| `11-magnetic-mirror` | S | Legacy iter-1/INTERRUPTED, has synthesis |
| `12-levitated-dipole` | S* (stale) | Legacy, iter-3/FAIL but has synthesis |

### Need --resume with --research (stuck at FAIL after 3 iterations)
| Concept | State | Iters | Notes |
|---------|-------|-------|-------|
| `01-hts-compact-tokamak` | M* (stale) | 4, all FAIL | Already tried research on iter-4 |
| `07-maglif` | D | 3, all FAIL | No model-setup yet |
| `09-qi-stellarator-hts` | D | 3, PASS→FAIL→FAIL | Regressed from iter-1 PASS |
| `17a-laser-icf-hybrid-drive` | M | 3, all FAIL | Has model-setup + review |
| `22-projectile-icf` | D | 3, all FAIL | Only has analysis |

### PASS but needs pipeline continuation
| Concept | State | Notes |
|---------|-------|-------|
| `14-magnetized-target-fusion-pneumatic-compression` | D | iter-3/PASS, needs model-setup → review |

### Interrupted (needs --resume)
| Concept | State | Notes |
|---------|-------|-------|
| `15-sheared-flow-stabilized-z-pinch` | G | iter-1/INTERRUPTED, gap-check exists |

### Not Yet Run (22 concepts — gap-check only)
| Concept | Family |
|---------|--------|
| `10-large-scale-stellarator` | MFE |
| `13-electrostatic-hybrid` | Non-Standard |
| `16-muon-catalyzed-fusion` | Non-Standard |
| `17b-laser-icf-fast-ignition` | IFE |
| `18-p-b11-frc` | MFE |
| `19-orbital-levitated-dipole` | MFE |
| `20a-type-one-stellarator` | MFE |
| `20b-renaissance-stellarator` | MFE |
| `23-laser-icf-nanostructured-target` | IFE |
| `24-dense-plasma-focus` | Non-Standard |
| `25-heavy-ion-beam-icf` | IFE |
| `26-laser-icf-indirect-drive` | IFE |
| `27-polywell` | Non-Standard |
| `28-hts-tokamak-full-hts` | MFE |
| `29-negative-triangularity-tokamak` | MFE |
| `30-laser-icf-nif-commercialization` | IFE |
| `31-laser-icf-oec-architecture` | IFE |
| `32-laser-icf-french-national` | IFE |
| `33-state-backed-tokamak-best` | MFE |
| `34-compact-spherical-tokamak-india` | MFE |
| `35-polomac-magnetic-confinement` | MFE |
| `36-helical-coil-stellarator` | MFE |

---

## Phase 1: Stage 1 Analysis (analyze → model-setup → review)

Run `stage1-all` with `--research --max-passes 3` for all concepts that need it.
Gap-check is skipped by default (no `--include-gap-analysis` flag).

### 1A. Resume stuck/interrupted concepts (6 concepts)

These already have iterations — resume them first to clear the backlog.

- [x] **Batch 1A-1**: Resume PASS + interrupted
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 3 \
    14-magnetized-target-fusion-pneumatic-compression \
    15-sheared-flow-stabilized-z-pinch
  ```
  - 14: Already PASS at iter-3, should go straight to model-setup → review
  - 15: INTERRUPTED at iter-1, will restart analysis

  **UPDATE (2026-04-06):**
  - ✅ **14**: PASS at iter-3. Pipeline advanced through model-setup and review. Review verdict: **PROCEED**. Complete.
  - ⚠️ **15**: FAIL at iter-3 (3 findings). Model works, review says PROCEED, but 3 analysis-text findings remain (driver cost framing, nearest-neighbor positioning, modeling approach statement). Root cause: research acquired sources on iter-3, so iter-2's assess findings were **silently dropped** by the research→source-integration feedback path (Bug B in feedback-routing-fix spec). The findings were re-flagged by iter-3 assessment but no iteration budget remained.
  After feedback-routing fix, re-run:
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 4 \
    15-sheared-flow-stabilized-z-pinch
  ```

- [x] **Batch 1A-2**: Resume FAIL concepts (group 1)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 6 \
    07-maglif \
    09-qi-stellarator-hts
  ```
  - Both at iter-3/FAIL. --max-passes 6 allows 3 more iterations with research.

  **UPDATE (2026-04-06):**
  - ⚠️ **07**: FAIL at iter-6 (2 findings). Model works (R* state). Sources grew 8→16. Remaining findings are analysis-text only: nearest-neighbor designations (never delivered to analysis agent — dropped by research on every iteration, Bug B) and rep-rate scenario table (data exists in analysis but not assembled into answer). Forward progress on other axes but these two stuck.
  After feedback-routing fix, re-run:
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 7 \
    07-maglif
  ```
  - ⚠️ **09**: FAIL at iter-6 (2 findings). Model works (R* state). Sources grew 5→11. Remaining findings are analysis-text only: CAS25 power conversion framing and sensitivity axis ranking. These findings ARE evolving (not stuck) — concept made progress because research found nothing on iter-6, so assess feedback was delivered. Likely to converge with 1-2 more iterations.
  After feedback-routing fix, re-run:
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 8 \
    09-qi-stellarator-hts
  ```

- [x] **Batch 1A-3**: Resume FAIL concepts (group 2)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 6 \
    22-projectile-icf \
    17a-laser-icf-hybrid-drive
  ```

  **UPDATE (2026-04-06):**
  - ✅ **22**: PASS at iter-5. Pipeline advanced through model-setup and review. Sources grew 4→11. Complete.
  - ⚠️ **17a**: FAIL at iter-6 (1 finding). Very close — down from 3 findings to 1. The remaining finding is **model-targeted** (Bug A): analysis correctly recommends an H-3 rep-rate/capacity-factor scenario table, but `model_setup.py` doesn't generate it. The analysis agent cannot fix this — it requires the model agent to act on the finding directly.
  After feedback-routing fix (Problem A — model category routing), re-run:
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 7 \
    17a-laser-icf-hybrid-drive
  ```

- [x] **Batch 1A-4**: Resume concept 01 (special case)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 7 \
    01-hts-compact-tokamak
  ```
  - Already at iter-4/FAIL with research. --max-passes 7 allows 3 more tries.

  **UPDATE (2026-04-06):**
  - ⚠️ **01**: FAIL at iter-7 (3 findings). Sources grew 4→14 (research working). Finding Thread C (differentiator gaps) shows genuine forward progress — rotates to new findings each iteration. But Threads A+B are stuck: "no viability bridging scenario" (blocking, model-targeted) and "REBCO absent from sensitivity table" (blocking, escalated, model-targeted) have repeated for 3+ iterations. Both require model code changes (Bug A). Third finding (FLiBe blanket cost) is analysis-text and progressing.
  After feedback-routing fix (Problem A), re-run:
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --resume --research --max-passes 10 \
    01-hts-compact-tokamak
  ```

- [ ] **Checkpoint 1A**: Run `status` and verify all 6 concepts advanced past D state
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py status
  ```

  **UPDATE (2026-04-06):** Partial. 2 of 6 concepts fully complete (14, 22). 4 remaining need feedback-routing fix before re-running. Checkpoint deferred until after fix is implemented and remaining concepts re-run.

  Current state:
  | Concept | State | Verdict | Blocker |
  |---------|-------|---------|---------|
  | 14 | R (reviewed, PROCEED) | PASS | — |
  | 15 | M* (model-setup, stale) | FAIL (3) | Bug B (assess findings dropped by research) |
  | 07 | R* (reviewed, stale) | FAIL (2) | Bug B (assess findings dropped by research) |
  | 09 | R* (reviewed, stale) | FAIL (2) | Close to converging, 1-2 more iters |
  | 22 | R* (reviewed) | PASS | — |
  | 17a | M* (model-setup, stale) | FAIL (1) | Bug A (model-targeted finding) |
  | 01 | M* (model-setup, stale) | FAIL (3) | Bug A (2 model-targeted findings) |

- [ ] **Sync 1A**: Push new research artifacts to R2
  ```bash
  ./scripts/sync_research.sh push
  ```

### 1B. Fresh concepts — batch runs (22 concepts, ~8 batches of 2-3)

Grouped by family for thematic coherence within batches.

- [ ] **Batch 1B-1**: MFE — Stellarators
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    10-large-scale-stellarator \
    20a-type-one-stellarator \
    20b-renaissance-stellarator
  ```

- [ ] **Batch 1B-2**: MFE — Tokamaks
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    28-hts-tokamak-full-hts \
    29-negative-triangularity-tokamak \
    33-state-backed-tokamak-best
  ```

- [ ] **Batch 1B-3**: MFE — Compact/Spherical Tokamaks
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    34-compact-spherical-tokamak-india
  ```

- [ ] **Batch 1B-4**: MFE — Other magnetic confinement
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    18-p-b11-frc \
    19-orbital-levitated-dipole \
    35-polomac-magnetic-confinement
  ```

- [ ] **Batch 1B-5**: MFE — Helical + Mirror
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    36-helical-coil-stellarator
  ```

- [ ] **Batch 1B-6**: IFE — Laser concepts (group 1)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    17b-laser-icf-fast-ignition \
    23-laser-icf-nanostructured-target \
    25-heavy-ion-beam-icf
  ```

- [ ] **Batch 1B-7**: IFE — Laser concepts (group 2)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    26-laser-icf-indirect-drive \
    30-laser-icf-nif-commercialization \
    31-laser-icf-oec-architecture
  ```

- [ ] **Batch 1B-8**: IFE + Non-Standard (remaining)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    32-laser-icf-french-national \
    13-electrostatic-hybrid \
    16-muon-catalyzed-fusion
  ```

- [ ] **Batch 1B-9**: Non-Standard (remaining)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --research --max-passes 3 \
    24-dense-plasma-focus \
    27-polywell
  ```

- [ ] **Checkpoint 1B**: Run `status` and confirm all 22 fresh concepts reached at least M (model-setup) state
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py status
  ```
  Note: Some may still be at D (drafted) if all 3 iterations FAILed. Record which ones need attention.

- [ ] **Sync 1B**: Push new research artifacts to R2
  ```bash
  ./scripts/sync_research.sh push
  ```

### 1C. Legacy synthesized concepts (8 concepts)

These have old analyses. Decision needed: re-run from scratch with `--force`, or accept existing analysis and just ensure review is current.

- [ ] **Decision**: For each legacy synthesized concept, determine whether to:
  - (a) Accept existing analysis, skip to Phase 2 (review → address-review)
  - (b) Re-run with `--force --research --max-passes 3` for fresh analysis

  Concepts: 02, 03, 04, 05, 06, 08, 11, 12

- [ ] **If re-running**: Batch as needed
  ```bash
  # Example if re-running all:
  uv run python exploration/concept_analysis/scripts/run_analysis.py stage1-all --force --research --max-passes 3 \
    02-acoustic-icf-sonofusion 03-laser-icf-liquid-jet-target 04-laser-icf
  # ... etc in batches of 3
  ```

---

## Phase 2: Review → Address-Review

For every concept that reaches M (model-setup) or beyond after Phase 1.

### 2A. Run review for all concepts that need it

- [ ] **Review batch**: Run review for all concepts at M state or that need re-review
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py review --all
  ```
  This skips concepts that already have a current review.

- [ ] **Checkpoint 2A**: Verify all concepts now have review.md
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py status
  ```

### 2B. Address-review for each concept

Each review produces a PROCEED or REVISE verdict. For REVISE verdicts, `address-review` applies corrective actions and kicks back to the stage1 loop.

- [ ] `address-review` concept `01-hts-compact-tokamak`
- [ ] `address-review` concept `02-acoustic-icf-sonofusion`
- [ ] `address-review` concept `03-laser-icf-liquid-jet-target`
- [ ] `address-review` concept `04-laser-icf`
- [ ] `address-review` concept `05-planar-coil-stellarator`
- [ ] `address-review` concept `06-magnetic-mirror`
- [ ] `address-review` concept `07-maglif`
- [ ] `address-review` concept `08-frc-w-direct-conversion`
- [ ] `address-review` concept `09-qi-stellarator-hts`
- [ ] `address-review` concept `10-large-scale-stellarator`
- [ ] `address-review` concept `11-magnetic-mirror`
- [ ] `address-review` concept `12-levitated-dipole`
- [ ] `address-review` concept `13-electrostatic-hybrid`
- [ ] `address-review` concept `14-magnetized-target-fusion-pneumatic-compression`
- [ ] `address-review` concept `15-sheared-flow-stabilized-z-pinch`
- [ ] `address-review` concept `16-muon-catalyzed-fusion`
- [ ] `address-review` concept `17a-laser-icf-hybrid-drive`
- [ ] `address-review` concept `17b-laser-icf-fast-ignition`
- [ ] `address-review` concept `18-p-b11-frc`
- [ ] `address-review` concept `19-orbital-levitated-dipole`
- [ ] `address-review` concept `20a-type-one-stellarator`
- [ ] `address-review` concept `20b-renaissance-stellarator`
- [ ] `address-review` concept `22-projectile-icf`
- [ ] `address-review` concept `23-laser-icf-nanostructured-target`
- [ ] `address-review` concept `24-dense-plasma-focus`
- [ ] `address-review` concept `25-heavy-ion-beam-icf`
- [ ] `address-review` concept `26-laser-icf-indirect-drive`
- [ ] `address-review` concept `27-polywell`
- [ ] `address-review` concept `28-hts-tokamak-full-hts`
- [ ] `address-review` concept `29-negative-triangularity-tokamak`
- [ ] `address-review` concept `30-laser-icf-nif-commercialization`
- [ ] `address-review` concept `31-laser-icf-oec-architecture`
- [ ] `address-review` concept `32-laser-icf-french-national`
- [ ] `address-review` concept `33-state-backed-tokamak-best`
- [ ] `address-review` concept `34-compact-spherical-tokamak-india`
- [ ] `address-review` concept `35-polomac-magnetic-confinement`
- [ ] `address-review` concept `36-helical-coil-stellarator`

Or batch:
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py address-review --all
```

- [ ] **Checkpoint 2B**: Any REVISE verdicts? If so, re-run `stage1-all --resume --research` for those concepts, then repeat review → address-review.

- [ ] **Sync 2**: Push any new research artifacts from address-review cycles to R2
  ```bash
  ./scripts/sync_research.sh push
  ```

---

## Phase 3: Synthesis

For every concept that has passed review (PROCEED verdict).

- [ ] **Synthesize all PROCEED concepts**:
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py synthesize --all
  ```

- [ ] **Checkpoint 3**: Verify all concepts now at S (synthesized) state
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py status
  ```
  Record any that didn't reach S and why.

---

## Phase 4: Approval

For every synthesized concept. This is a human-in-the-loop step — each approval should be reviewed before confirming.

- [ ] `approve` concept `01-hts-compact-tokamak`
- [ ] `approve` concept `02-acoustic-icf-sonofusion`
- [ ] `approve` concept `03-laser-icf-liquid-jet-target`
- [ ] `approve` concept `04-laser-icf`
- [ ] `approve` concept `05-planar-coil-stellarator`
- [ ] `approve` concept `06-magnetic-mirror`
- [ ] `approve` concept `07-maglif`
- [ ] `approve` concept `08-frc-w-direct-conversion`
- [ ] `approve` concept `09-qi-stellarator-hts`
- [ ] `approve` concept `10-large-scale-stellarator`
- [ ] `approve` concept `11-magnetic-mirror`
- [ ] `approve` concept `12-levitated-dipole`
- [ ] `approve` concept `13-electrostatic-hybrid`
- [ ] `approve` concept `14-magnetized-target-fusion-pneumatic-compression`
- [ ] `approve` concept `15-sheared-flow-stabilized-z-pinch`
- [ ] `approve` concept `16-muon-catalyzed-fusion`
- [ ] `approve` concept `17a-laser-icf-hybrid-drive`
- [ ] `approve` concept `17b-laser-icf-fast-ignition`
- [ ] `approve` concept `18-p-b11-frc`
- [ ] `approve` concept `19-orbital-levitated-dipole`
- [ ] `approve` concept `20a-type-one-stellarator`
- [ ] `approve` concept `20b-renaissance-stellarator`
- [ ] `approve` concept `22-projectile-icf`
- [ ] `approve` concept `23-laser-icf-nanostructured-target`
- [ ] `approve` concept `24-dense-plasma-focus`
- [ ] `approve` concept `25-heavy-ion-beam-icf`
- [ ] `approve` concept `26-laser-icf-indirect-drive`
- [ ] `approve` concept `27-polywell`
- [ ] `approve` concept `28-hts-tokamak-full-hts`
- [ ] `approve` concept `29-negative-triangularity-tokamak`
- [ ] `approve` concept `30-laser-icf-nif-commercialization`
- [ ] `approve` concept `31-laser-icf-oec-architecture`
- [ ] `approve` concept `32-laser-icf-french-national`
- [ ] `approve` concept `33-state-backed-tokamak-best`
- [ ] `approve` concept `34-compact-spherical-tokamak-india`
- [ ] `approve` concept `35-polomac-magnetic-confinement`
- [ ] `approve` concept `36-helical-coil-stellarator`

Or batch (if comfortable approving without individual review):
```bash
uv run python exploration/concept_analysis/scripts/run_analysis.py approve 01-hts-compact-tokamak 02-acoustic-icf-sonofusion ...
```

- [ ] **Checkpoint 4**: Final status — all 37 remaining concepts at A (approved)
  ```bash
  uv run python exploration/concept_analysis/scripts/run_analysis.py status
  ```

- [ ] **Final Sync**: Push all artifacts to R2
  ```bash
  ./scripts/sync_research.sh push
  ./scripts/sync_research.sh push --dry-run  # verify nothing missed
  ```

---

## Notes

- **Cost**: Each `stage1-all` iteration with `--research` may trigger source extractions ($5-50 each via agentic-mbse). Budget ~$5-15 per concept for research extractions.
- **Time**: Each concept takes ~5-15 min per iteration. With 22 fresh concepts × 3 iterations = ~66 iterations. At ~10 min each ≈ 11 hours of runtime.
- **Parallelism**: Batches within a phase can run sequentially in a single terminal session. The script handles one concept at a time within a batch.
- **Failure handling**: If a concept exhausts max-passes and still FAILs, it stays at D state. Decide case-by-case whether to increase max-passes, add sources manually, or accept the FAIL and proceed with `--force` on downstream stages.
