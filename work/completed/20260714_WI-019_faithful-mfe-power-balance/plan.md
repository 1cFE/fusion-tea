---
Status: complete
Created: 2026-07-14
Updated: '2026-07-14'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-019 Plan: Faithful MFE Power Balance

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** (demo model-development item; §3 barred paths must not be read).

## Source Documents

- Design: `./design.md` (primary — decisions D1–D5, consumer map, regen procedure, validation report)
- Spec: `./spec.md` (MR-WI019-1..7, success criteria 1–4, SV-025/026)
- Epic: `work/backlog/epic-mfe-cost-modeling.md`

## Design Summary

Replace the lossy thermal-power formula with the collapsed faithful form `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump` (design "Research Findings"), swap the `fpcppf` input for absolute `p_pump` (D2), full-precision alpha ratio (D3), `p_sub = f_sub·p_et` (D4), output contract unchanged (D5). Then propagate through the e2e chain and re-run the Anchor A handshake as the success measure.

## Prototype Baseline

The design phase already applied and validated the **canonical** edits (design "Validation Report", PASS):

- `models/library/analyses/mfe_power_balance.sysml` — new formula, `p_pump` input, doc-comment derivation + regime conditions. DONE.
- `models/designs/generic_mfe/mfe_plant.sysml` — attribute + binding rename. DONE.
- `models/designs/stellarator_09/stellarator_plant.sysml` — `:>> p_pump = 1.0` with `steady_state_stellarator.yaml:21` citation. DONE.
- Validation: L1 = 0 errors; L2/L6 issue sets byte-identical to pristine HEAD (baseline extracted and re-validated); numeric check vs 1costingFE power table ≤6.2e-8 on all six channels.

Remaining: staged e2e copies, oracle, pipeline regen, runner headline update, handshake, matrix/status/doc refresh — Phases 2–4 below.

**Pre-existing finding (out of scope, surfaced for the owner):** `tests/models/test_power_balance.py` targets the pre-archive layout (`models/library/calculations/power_balance/`, `'Alpha Power Calc'`, `fuel_type`/`fpcppf` interface, dated 2026-01-26) and **fails at HEAD before this work item** (`test_power_balance_sysml_exists` asserts a path that hasn't existed since the WI-009 restructure). Not caused or worsened by WI-019; rewriting it is a separate small work item. Recorded here so the final-phase pytest result is read correctly.

## Phasing Approach

Four phases, bottom-up along the execution chain: canonical models (done — verify only) → staged copies + oracle (the pure-Python truth the executor is checked against) → regenerate + execute (teax bit-exactness gate) → handshake + close-out (the SV-025/026 measurements and bookkeeping). Each phase gates the next; no parallelization needed (single-file edits, strictly sequential dependencies).

## Validation Strategy

- Per phase: L1 (0 errors) on any touched `.sysml`; phase-specific numeric gates below.
- Final: `uv run agentic-mbse validate models --complete` parity with the design-phase baseline (no new L2/L6 issues); SV-025/026 measured by the handshake; SV-023 IFE anchor regression re-run; spec success criteria 1–4 checked explicitly.

---

## Phase 1 — Canonical models (verification only; edits landed at design)

**Overview**: The design prototype IS the production canonical change (small, fully cited). This phase just pins its status.

**Design Reference**: design "Proposed Design" (calc stencil, instance binding) and "Validation Report".

**Checklist**
- [x] `models/library/analyses/mfe_power_balance.sysml` — REFINE: header doc (derivation + regime), `p_pump` input replaces `fpcppf`, `p_alpha = (3.52/17.58)·p_nrl`, collapsed `p_th`, `p_sub = f_sub·p_et`, derived `p_pump` deleted *(applied 2026-07-14)*
- [x] `models/designs/generic_mfe/mfe_plant.sysml` — REFINE: attribute `p_pump` (line 129), binding `in p_pump = p_pump` (line 146) *(applied)*
- [x] `models/designs/stellarator_09/stellarator_plant.sysml` — REFINE: `:>> p_pump = 1.0` + citation *(applied)*
- [x] `uv run agentic-mbse validate models --complete` — L1 0 errors; L2/L6 identical to HEAD baseline *(done at design)*
- [x] Re-run `uv run agentic-mbse validate models` (L1–L3) at implement start to confirm worktree state unchanged

**Completion gate**: L1–L3 pass, 0 errors.

## Phase 2 — Staged e2e copies + pure-Python oracle

**Overview**: Mirror the canonical edits into the codegen-adapted staged models and the oracle, so the generated pipeline and its reference implementation agree on the new formula. Keep the canonical-vs-staged split (do NOT port staged adaptations back).

**Design Reference**: design "Consumer map" rows 4–6 and "Oracle mirror".

**Files to Modify**
- `exploration/stellarator_e2e/models/analyses/mfe_power_balance.sysml` — REFINE (byte-identical edit to canonical; file verified identical pre-edit)
- `exploration/stellarator_e2e/models/designs/generic_mfe/mfe_plant.sysml` — REFINE (lines 129/146, same rename)
- `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` — REFINE (lines 310-312, same binding+citation)
- `exploration/stellarator_e2e/verify_stellaris.py` — REFINE (oracle mirror)

**Checklist**
- [x] Staged `mfe_power_balance.sysml`: apply the identical canonical diff (confirm with `diff` against canonical afterward — files should again be identical)
- [x] Staged `mfe_plant.sysml`: attribute + binding rename
- [x] Staged `stellarator_plant.sysml`: `:>> p_pump = 1.0` + citation
- [x] `verify_stellaris.py:20`: params `fpcppf=0.06` → `p_pump=1.0` (comment: 1costingFE `steady_state_stellarator.yaml:21`)
- [x] `verify_stellaris.py:65-70`: `p_th = mn·p_neutron + p_alpha + p_input + eta_p·p_pump`; delete derived `p_pump`; `p_sub = f_sub·p_et`; `recirculating` uses `p["p_pump"]`
- [x] `uv run agentic-mbse validate exploration/stellarator_e2e/models --level 1` — 0 errors
- [x] Oracle spot-run: `compute()` at Stellaris defaults returns p_th 3182.4 / p_the 1059.7 / p_net 786.1 / q_eng 3.873 (design "Validation Report" hand-check values)

**Test requirements**: the oracle spot-run above is the phase's numeric test (mirrors design-phase check).

**Completion gate**: staged L1 = 0 errors; staged power-balance file identical to canonical; oracle reproduces the design-phase numbers to 0.1 MW.

## Phase 3 — Regenerate pipeline + teax execution

**Overview**: Re-emit the generated package from the staged models and prove the executor still matches the oracle bit-exactly at the new formula, with the runner's headline table updated from WI-018 to WI-019 values.

**Design Reference**: design "Pipeline regeneration procedure"; CODEGEN_FINDINGS.md findings 8/9 (glue re-applies; constraints stay commented in staged copies).

**Files to Modify**
- `exploration/stellarator_e2e/stellarator.snapshot.json`, `generated/` — REGENERATE (snapshot → `bridge_v11_generate.py`)
- `exploration/stellarator_e2e/run_stellaris.py` — REFINE (headline table only, lines ~227-235)

**Checklist**
- [x] `source /home/reid/1cfe/fusion-tea/.env` (SYSIDE_LICENSE_KEY) and regenerate: `sysml-codegen snapshot` over staged models → `bridge_v11_generate.py` (exact invocations per CODEGEN_FINDINGS.md; sys_design JSON now carries `pb__p_pump`)
- [x] Confirm the regenerated pb module signature: `p_pump` in, no `fpcppf`
- [x] `run_stellaris.py` headline table: p_net 575→786.1 (tol 3), rec_frac 0.36→0.258 (tol 0.01), q_eng 2.8→3.873 (tol 0.05); update total-capital / LCOE / magnet entries to oracle-computed WI-019 values (compute via oracle before the run; V and p_fus unchanged at 564 / 2700)
- [x] Run `exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py` — every executed channel bit-exact vs oracle (rel 1e-9, the standing gate), headline check green
- [x] Record the executed WI-019 Stellaris headline (p_th, p_net, LCOE, total capital, magnet share) in this plan's notes

**Completion gate**: `run_stellaris.py` exits green — exec≡oracle on all channels, headline table passes.

## Phase 4 — Handshake re-run, SV measurements, close-out

**Overview**: The success measure: feed 1costingFE's Anchor A point through the regenerated pipeline, measure SV-025/026, refresh the report and project bookkeeping.

**Design Reference**: design "Consumer map" row 7 (handshake mapping) and "Validation Plan" step 4; spec "Success Criteria".

**Files to Modify**
- `exploration/stellarator_e2e/handshake_1costingfe.py` — REFINE (mapping block, lines 191-194)
- `exploration/stellarator_e2e/HANDSHAKE_REPORT.md` — REFINE (numbers + discrepancy list)
- `modeling_project/VALIDATION_MATRIX.md` — SV-025/026 status
- `models/designs/stellarator_09/stellarator_plant.sysml` — REFINE (stale BOP doc comment quoting p_et=896.8/p_th=2693.1 at line ~231; refresh to executed WI-019 values)
- `.project/CURRENT_WORK.md` — headline + status
- `data/traceability_matrix.csv` — trace row (follow existing WI-009/018 row convention; use `uv run agentic-mbse pm trace-element` if that is how prior rows were made)

**Checklist**
- [x] `handshake_1costingfe.py:191-194`: replace the fpcppf trap block with `f"{P}pb__p_pump": pb["p_pump"]`
- [x] Re-run handshake (two-venv procedure per HANDSHAKE_REPORT "What was run"; re-emit `onecfe_point.json` only if commit pin moved — it hasn't)
- [x] **SV-025**: power channels (p_th/p_the/p_et/p_net/q_eng/rec_frac) vs 1costingFE ≤1e-5 rel → flip to `passing` (`uv run agentic-mbse pm update-validation SV-025 --status passing`)
- [x] **SV-026**: all 12 power-scaled accounts end-to-end ≤0.1% rel → flip to `passing`
- [x] `HANDSHAKE_REPORT.md`: refresh power-balance table (gaps → ~0), per-account end-to-end column, rollup/LCOE section (remaining gap now purely structural: CAS22 tail, CAS40/50/60, LCOE construction); mark discrepancies 1 and 9 RESOLVED (WI-019); keep 2–8 with updated numbers
- [x] Refresh stale headline numbers in `stellarator_plant.sysml` doc comment(s) (grep for 896.8/2693/575/250.95 in canonical + staged instance files)
- [x] Final validation: `uv run agentic-mbse validate models --complete` — parity with baseline (L1 0 errors, no new L2/L6)
- [x] IFE regression (SV-023): re-run `exploration/ife_e2e/run_anchors.py` in the exec venv — unchanged anchors
- [x] `uv run python -m pytest tests/models/ -q` — expect: `test_power_balance.py` fails pre-existing (documented above), no NEW failures
- [x] Spec success criteria 1–4: verify each explicitly and record results in this plan
- [x] Update `.project/CURRENT_WORK.md` (WI-019 done, new headline, SV-016 band question noted for review)
- [ ] `uv run agentic-mbse pm close-item WI-019` (after owner sees the summary; keep as final step)
- [x] Raise at close: SV-016 "Q_eng ~10–40" band vs measured q_eng 3.87 (Stellaris) / 8.8 (1cfe 1 GWe) — owner adjusts or annotates, not silently edited

**Completion gate**: SV-025 and SV-026 measured passing; report + matrix + CURRENT_WORK consistent; no new validation or test regressions.

---

## Feasibility Concerns

| concern | mitigation |
|---|---|
| Regen path drift (snapshot/bridge invocations from memory) | exact commands recorded in CODEGEN_FINDINGS.md; if the bridge chokes, that is a codegen finding to file, not a model workaround |
| Runner/handshake harness glue breaks on regenerated YAML | glue keys off pb *output* names (unchanged); run_stellaris oracle gate catches it before the handshake |
| `pm update-validation` may not target manually-added rows | fall back to editing the matrix row directly (matrix is markdown; BACKLOG.md is the scripts-only file) |
| Stale test file misread as WI-019 regression | pre-existing failure documented in Prototype Baseline; final-phase pytest expectation states it explicitly |


---

## Implementation Record (2026-07-14)

All phases executed same-session; every gate green.

**Phase 2** — staged copies byte-identical to canonical (power balance) / same targeted edits (plant, instance); staged L1 = 0 errors; oracle spot-run matched design predictions to 0.1 MW.

**Phase 3** — snapshot + V11 bridge regenerated (same 3 known offenders bridged, 0 after); generated pb module carries the new formula verbatim, `p_pump` in / no `fpcppf` anywhere in `generated/`; `run_stellaris.py` green: every executed channel bit-exact vs oracle (rel tol 1e-9), WI-019 headline check green.

**Phase 4** — handshake re-run:
- **SV-025 PASSING**: all six power channels ≤6.3e-8 rel (tolerance 1e-5; worst = p_th/p_the/p_et at +6.23e-8, the reference float32 floor).
- **SV-026 PASSING**: all 12 power-scaled accounts ≤1.0e-7 end-to-end (tolerance 0.1%; worst = heat_rejection +1.0e-7). Was −8.6…−16.4%.
- Rollup after fix: net electric 0.00% (was −23.5%); total capital −41.9% (was −44.4%); LCOE −30.9% (was −13.2% — the offsetting-errors cancellation removed; gap now purely structural scope). Explained in HANDSHAKE_REPORT.md.
- HANDSHAKE_REPORT.md refreshed; discrepancies 1, 2, 3, 9 marked RESOLVED (WI-019).
- IFE regression (SV-023): run_anchors.py ALL PASSED (rel 1e-6).
- Final `validate models --complete`: L1 0 errors; L2 (3) / L6 (105) byte-identical to pristine-HEAD baseline (verified via git-archive extract and detached worktree).
- pytest tests/models: 2 failed / 10 passed / 13 skipped / 18 errors — **identical tally at pristine HEAD** (stale pre-WI-009 test file, documented in Prototype Baseline). Zero new regressions.

**New Stellaris headline (executed)**: V 564 m³, p_fus 2700 MW, p_th 3182.4 MW, gross 1059.7 MW, net 786.1 MW, rec_frac 0.258, q_eng 3.87, total overnight $10.086B, LCOE $189.13/MWh, magnet $4.392B (43.5%).

**Spec success criteria**: 1 ✓ (SV-025, 6.3e-8 ≪ 1e-5) · 2 ✓ (SV-026, 1.0e-7 ≪ 0.1%) · 3 ✓ (L1–L6 parity, SV-023 pass, runner bit-exact) · 4 ✓ (headline recorded here + CURRENT_WORK.md + instance doc).

**SV verification tests**: SV-025/026 verify through `handshake_1costingfe.py`, recorded in the matrix Test column — same convention as SV-023/024 (harness-verified, not pytest; the two-venv + license-gated chain doesn't fit the pytest runner).

**Deviations from plan**: none of substance. Additions beyond the checklist: `run_stellaris.py` headline label strings WI-018→WI-019; handshake re-emitted `onecfe_point.json` (same pinned commit).

**Surfaced to owner at close (out of WI-019 scope, discovered during headline refresh):**
1. Three pass-through constants were derived at the pre-WI-019 power point and are now internally inconsistent with the model's own p_net: `buildings_capital` (at p_et=896.8/p_th=2693.1), `preconstruction_capital` (at P_net=575.3), `annual_om` (at P_net=575.3). Annotated STALE BASIS in both canonical and staged instance files; recomputing them belongs to the Stage-3 pass-through/account-scope item. If recomputed, total capital and LCOE move again (all three scale up with p_net).
2. SV-016 reasonableness band says "Q_eng in ~10-40"; measured q_eng is 3.87 (Stellaris point) / 8.84 (1cfe 1 GWe point). The band was a pre-fix order-of-magnitude guess; owner should adjust or annotate SV-016 (still `pending`).
3. Pre-existing: `tests/models/test_power_balance.py` targets the pre-WI-009 layout and fails at HEAD; candidate for a small backlog item.
