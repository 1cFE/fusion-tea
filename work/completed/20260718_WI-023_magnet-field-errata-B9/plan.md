---
Status: complete
Created: 2026-07-18
Updated: '2026-07-18'
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-023 Plan: Magnet-Field Errata — B = 9.0 T, p_tf = 0.0

**Required Reading: `knowledge/holdout/aries-cs/PROTOCOL.md`** — demo model-development session; §3 barred paths must not be read, cited, or opened.

Owner rulings (all recorded; no further owner stop before close): checkpoint 2026-07-18 ratified the full spec scope — MR-WI023-3 p_tf = 0.0 (option b), Q2 annotate the analyst patch, Q3 dated note below `HANDSHAKE_REPORT.md:30`, Q1 future-work capture (WI-024, registered). SV-016 is re-flagged at close, not resolved. Item close (`pm close-item`) is owner-held; committing is orchestrator-held — neither is a plan step.

**Process note**: the orchestrator skipped the optional `/review-model` stage (execution decision: pure two-literal rebind, no structure change, and the expected headline was already verified against the real oracle at design). The independent `/audit-models` still follows implement.

## Source Documents

- Design (primary): `./design.md` — carrier inventory, edit stencils, D1–D6, oracle-exact expected headline
- Spec (contract): `./spec.md` — MR-WI023-1..5, Success Criteria 1–5, owner rulings
- Epic: `work/backlog/epic-mfe-cost-modeling.md`
- Executed template: `work/completed/20260718_WI-022_predictive-confinement/plan.md` (same instance file, same bars; its Implementation Record is the sequencing precedent)

## Design Summary

Two literal rebinds in the concept-09 instance — `magnet.B` 5.86 → 9.0 (phantom Table 3 row; Tables 2/5 images print 9.0) and `pb.p_tf` 111.0 → 0.0 (phantom row; source defers the value, [OWNER] option b) — plus the doc rewrites, staged-twin mirroring, oracle/runner re-baseline, regen, and two annotation edits. No formula, library, or generic-plant change (design D1). Expected headline is oracle-exact (design "Research Findings" table): magnet **$6.3235B** (share **50.18%**), total **$12.6015B**, p_net **915.145 MW**, q_eng **6.609**, LCOE **$201.458/MWh**.

## Prototype Baseline (from the design validation report)

- **Oracle prototype: PASS** — design-stage scratch harness reproduced the WI-022 baseline to the cent, then computed the WI-023 point (magnet $6,323,469,946.33 = ×9.0/5.86 to the last ulp; total $12,601,519,645.07; LCOE $201.4579). These are the implement targets.
- **Baseline L1: PASS** — 21 files, 0 errors, 0 warnings at `cef74e8e`.
- **Mirroring precondition: PASS** — canonical vs staged full-file diff shows exactly one divergence, the staged-only commented-out viability-assert block (canonical 609–621 vs staged 609–614). Every edit region is byte-identical at identical line numbers.
- **Level 4–6 issues**: none introduced by this item; L6 baseline is the 6 pre-existing offenders (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`). The bar everywhere below is "exactly these 6, zero new."
- No new SysML constructs — literal rebinds inside existing `:>>` redefinitions; no parse-risk stencils needed.

## Phasing Approach

Six phases, same spine as the executed WI-022 plan: canonical model edits first (single-file, L1-gated), mirror + full validation second, then regen (generated carriers move only by regen — never hand-edited, design D5), then oracle/runner re-baseline and the bit-exact execute, then the handshake/regression gates, then annotations + close-out records. Model edits precede regen because the snapshot bakes instance bindings; oracle edits precede the execute because the runner's gate is bit-exact against the oracle.

**Line numbers below are pre-edit anchors** (verified current at `cef74e8e`). Doc rewrites shift later line numbers within the file — match edits on content, use the numbers to orient.

## Validation Strategy

- **Per phase**: L1 after every model-file edit; full L1–L6 after the mirror (Phase 2); regen self-checks (Phase 3); bit-exact execute (Phase 4); handshake byte-identity + regressions (Phase 5).
- **Environment**: all Python via `uv run`; syside has no CLI in this venv — use `uv run agentic-mbse validate models --complete` (or `--level N`); license via `set -a && source ~/1cfe/fusion-tea/.env && set +a`. Pipeline execution uses the exec venv interpreter `/home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python`.
- **Final**: spec Success Criteria 1–5 verified explicitly in Phase 6; SV-030 → passing with executed values; SV-016 re-flagged.

---

## Phase 1 — Instance edits (canonical `models/designs/stellarator_09/stellarator_plant.sysml`)

**Overview**: all model-text changes land in the canonical instance first. This is the whole model change — two binding literals and their documentation.

**Design reference**: design "Proposed Design §1. Instance edits" (stencils for the B comment/binding, magnet-block doc, MR-4 Ref block, and p_tf doc), decisions **D2** (p_tf documented as a deferral, cited to the deferral — never a MW value), **D3** (r_coil comment 3.20 → 3.00), **D4** (headline block re-baselines in the same rewrite).

**Baseline**: file at `cef74e8e`; carriers per the design "Carrier inventory" table.

**Checklist**:

- [x] Headline doc block (lines 49–62): re-baseline to the expected executed values (net 915.1 MW, rec_frac 0.151, q_eng 6.61, total $12.60B, LCOE $201.46, magnet $6.32B / 50.2%; p_fus/p_th/V unchanged); append the one history line per D4 (WI-022 values to history; 5.86 was a phantom row; p_tf 111 was stored energy in GJ, not a power). Final numbers confirmed against the Phase 4 execution.
- [x] Mapping-traps note (lines 64–70): B trap resolves to its corrected statement — cost field is the axis-averaged 9.0 T (Table 2/5 images), NOT the 24.9 T peak-on-winding; delete the "under review as WI-023" caveat. r_coil and sigma_v traps unchanged.
- [x] Magnet-block doc (lines 82–110): rewrite wholesale per design §1 items (a)–(d) — 9.0 T mapping trap; one-line phantom history; r_coil arithmetic refreshed to a = 1.3 / vessel_or = 3.00 m (layer sum stencil in the design); **Ref** line's phantom Table 3 entry replaced by the design's MR-4 stencil (Table 2 + Table 5 images, raw.pdf refutation, geometry.py:106-114, steady_state_stellarator.yaml:39-42).
- [x] B binding + comment (lines 116–118): `:>> B = 9.0;` with the design's 4-line comment stencil (Table 2/5 image cites; NOT the 24.9 T peak). Phantom "Table 3 line 289" citation deleted, not annotated around.
- [x] r_coil binding comment (lines 122–125): 3.20 → 3.00 (D3 — same directed correction as the magnet-block refresh).
- [x] p_tf binding + doc (lines 425–434): `:>> p_tf = 0.0` with the design's full doc stencil — deferral stated plainly, no MW value cited from the Stellaris paper, no-fallbacks rule named, [OWNER] ruling dated, forward pointer to WI-024, known-optimistic direction named. Phantom "Table 2 line 235" citation deleted.
- [x] STALE BASIS blocks (lines 498 and 542): append the WI-023 move (P_net 804.1 → 915.1) in the established "updated WI-0xx" style. Buildings block (line 259) untouched — its basis is p_et/p_th, which do not move.
- [x] Confirm no other live `5.86` remains in the file: `grep -n "5\.86" models/designs/stellarator_09/stellarator_plant.sysml` returns only phantom-history mentions (the one-line history in the magnet block / headline), no citation or binding.

**Test requirements**: none new — literal rebinds in an existing instance; the integration test is the Phase 4 bit-exact execute.

**Validation checkpoint**: `set -a && source ~/1cfe/fusion-tea/.env && set +a && uv run agentic-mbse validate models --level 1` → 21 files, 0 errors, 0 warnings.

**Completion gate**: L1 clean; all eight checklist edits present; phantom citations gone from the canonical file.

## Phase 2 — Mirror to the staged twin + full validation

**Overview**: replay the identical region edits into the staged copy the codegen snapshot reads, then run the full validation ladder against the baseline.

**Design reference**: design "Research Findings — Mirroring is trivial here" and "Validation Plan" items 1–2.

**Baseline**: staged twin `exploration/stellarator_e2e/models/designs/stellarator_09/stellarator_plant.sysml` — identical line numbers in every edit region; sole divergence is the commented-out viability-assert block (staged 609–614).

**Checklist**:

- [x] Apply every Phase 1 edit, byte-identical, to the staged twin (same regions, same content).
- [x] `diff` canonical vs staged: the only remaining divergence is the known viability-assert block (canonical asserts at 609–621 pre-edit vs staged comment block).
- [x] Full validation: `uv run agentic-mbse validate models --complete` (env sourced) → **L1 = 0; L2–L5 pass; L6 = exactly the 6 pre-existing offenders** (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`), zero new; no diagnostic names a WI-023-touched element. *(Executed note: the validator attributes the `hif_plant.sysml:205` offender to its Level-2 section, so the tool prints L2 ❌ / L6 ❌ — verified identical on a pristine `cef74e8e` worktree: full output byte-identical to baseline, same 6-error offender set, zero new, no WI-023 element named.)*

**Test requirements**: the full-ladder run is the regression test for this phase; compare offender list, not just counts.

**Validation checkpoint**: as above — mirroring diff + L1–L6 vs baseline.

**Completion gate**: diff shows only the assert-block divergence; L1–L6 bar met exactly.

## Phase 3 — Regen (generated carriers pick up 9.0 / 0.0)

**Overview**: regenerate the pipeline artifacts from the staged models. Generated files and the snapshot are never hand-edited (design D5); the values move only through regen.

**Design reference**: design "Proposed Design §3. Regen" and **D5**; risk table row "Regen clobbers the WI-022 handwritten impl". Exact invocation per `exploration/stellarator_e2e/CODEGEN_FINDINGS.md:29` and the header of `bridge_v11_generate.py` (lines 29–30).

**Baseline**: `generated/inputs/mfe_plant_params.json:17` and `generated/schemas/mfe_plant_params.py:24` carry 5.86; `generated/inputs/system_design.json:42`, `generated/schemas/system_design.py:52`, and `generated/pipelines/mfe_stellarator.yaml:186` carry/wire 111.0; `stellarator.snapshot.json` carries the old literals; `generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py` holds the WI-022 handwritten impl (`AUTO_IMPLEMENTED = False`).

**Checklist**:

- [x] Pre-regen: confirm `preserve_handwritten=True` still set in `GenerationConfig` (`exploration/stellarator_e2e/bridge_v11_generate.py:108`); record the current content hash of `generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py`. *(sha256 `8d23574793c34314c67b68b8e0f4ec438d3e2d9f92060eb4094a8d46c0794a9f`)*
- [x] Env: `cd ~/1cfe/sysml-codegen && set -a && source ~/1cfe/fusion-tea/.env && set +a`.
- [x] Snapshot the staged models → `exploration/stellarator_e2e/stellarator.snapshot.json` (the sysml-codegen snapshot flow, exactly as the WI-022/WI-018 record — see CODEGEN_FINDINGS.md:29).
- [x] Regen: `uv run python /home/reid/1cfe/fusion-tea-stellarator-mbse-demo/exploration/stellarator_e2e/bridge_v11_generate.py` (from the sysml-codegen dir).
- [x] Verify generated values: `mfe_plant_params.json` → `stellarator_09__stellaris__magnet__B: 9.0`; `mfe_plant_params.py` default 9.0; `system_design.json` → `stellarator_09__stellaris__pb__p_tf: 0.0`; `system_design.py` default 0.0; `mfe_stellarator.yaml` wiring unchanged (still maps `magnet__B` and `pb__p_tf` slots — yaml:155 / yaml:186).
- [x] Verify handwritten-impl **content** survival (WI-022 gotcha — preservation is by file existence, so check content, not presence): `dt_fusion_power_impl.py` unchanged vs the pre-regen hash / `git diff` empty for that file; `AUTO_IMPLEMENTED = False` intact. *(hash identical post-regen)*
- [x] Verify V11 offenders unchanged: exactly the 3 known cross-part rollup bridge keys (`contingency__direct_subtotal`, `indirect__direct_cost`, `lcoe_calc__total_capital`).
- [x] Confirm zero hand-edits landed under `generated/` or in the snapshot (`git status` shows only regen-produced changes there). *(Regen-fresh state resets the 3 bridge keys to placeholder 1.0 and the 4 BOP power wirings to their pre-glue params references — the committed files carried the WI-022 post-run harness-patched state; run_stellaris.py glue-1/glue-2 re-apply on execute, per the WI-020/022 records.)*

**Test requirements**: the three verify checkboxes above are this phase's tests.

**Validation checkpoint**: generated params carry 9.0 / 0.0; impl content-identical; 3 offenders; no hand-edits.

**Completion gate**: all regen verifications pass. If the handwritten impl changed, stop — restore from git and diagnose before proceeding (do not re-fill by hand as a workaround).

## Phase 4 — Oracle + runner re-baseline, bit-exact execute

**Overview**: move the oracle inputs, retarget the runner's headline asserts, and run the generated pipeline bit-exact against the oracle.

**Design reference**: design "Proposed Design §2. Oracle + runner" (the exact `heads` list stencil) and "Research Findings" expected-headline table (the implement targets, oracle-exact).

**Baseline**: `verify_stellaris.py:66` `p_tf=111.0`, `:69` `magnet_B=5.86`; `run_stellaris.py:232–241` WI-022 comment block, `:242–251` WI-022 asserts (p_net 804.1, q_eng 3.93, total 9.59, LCOE 176, magnet 4.12).

**Checklist**:

- [x] `verify_stellaris.py:66` → `p_tf=0.0` with comment (source defers; WI-023 / WI-024); line 69 → `magnet_B=9.0` with comment (Table 2/5 images).
- [x] `run_stellaris.py:232–241`: rewrite the comment block for WI-023 (what moved and why; WI-022 values as the "was" line).
- [x] `run_stellaris.py:242–251`: retarget the asserts to the design §2 stencil — V 425 (tol 2), p_fus 2748.1 (2), p_net 915.1 (3), rec_frac 0.151 (0.01), q_eng 6.61 (0.05), total 12.60 (0.05), LCOE 201.5 (2), magnet 6.32 (0.05). Loose sanity band; the real gate is the per-channel rel-1e-9 compare. *(Also retargeted the runner's final "headline reproduced" success string WI-022 → WI-023 at run_stellaris.py:295 — same headline messaging, content-matched per the pre-edit-anchor rule.)*
- [x] Execute: `cd exploration/stellarator_e2e && /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python run_stellaris.py` → **bit-exact vs the updated oracle at rel 1e-9 on every channel, per-account capital, rollup, and LCOE**; headline checks green. *(ALL CHECKS PASSED; zero rel-1e-9 failures.)*
- [x] Verify magnet capital is exactly ×9.0/5.86 vs the WI-022 record: **$6,323,469,946.33**; total **$12,601,519,645.07**; p_net **915.145**, q_eng **6.609**, LCOE **$201.458**; V/p_fus/p_th/wall_load unchanged (425.0 / 2748.06 / 3238.1 / 3.131). *(Executed: magnet 6,323,469,946.334225; total 12,601,519,645.065952; p_net 915.145439; q_eng 6.609268; rec_frac 0.151303; LCOE 201.457898; V 425.000014 / p_fus 2748.056877 / p_th 3238.120923 / wall_load 3.131235 — all identical to WI-022 on the untouched channels; magnet share 50.18%.)*
- [x] Confirm the Phase 1 headline-doc numbers match the executed values in both model copies (they are oracle-exact; on any mismatch, fix both copies, re-run L1, and surface the discrepancy in the record). *(Match — no fix needed.)*

**Test requirements**: the rel-1e-9 bit-exact compare is the integration test; the headline asserts are the sanity band.

**Validation checkpoint**: run output — zero rel-1e-9 failures, all headline checks green, executed values recorded for Phase 6.

**Completion gate**: bit-exact pass at the expected values. Any deviation from the design's expected table is a stop-and-surface, not a retarget (the same oracle produced both).

## Phase 5 — Handshake byte-identity + regressions

**Overview**: prove both corrections stayed out of the Anchor A handshake, and that nothing else moved.

**Design reference**: design "Cross-File Bindings" (injections `magnet__B` ← `coil["b_center"]` at `handshake_1costingfe.py:271`, `pb__p_tf` ← `pb["p_coils"]` at line 216) and "Validation Plan" items 5–6, 8.

**Checklist**:

- [x] Re-run the handshake with **zero edits to the script**: `cd exploration/stellarator_e2e && /home/reid/1cfe/fusion-tea/exploration/pipeline_spike/.venv-exec/bin/python handshake_1costingfe.py`.
- [x] `git diff exploration/stellarator_e2e/handshake_comparison.json` → **empty** (SV-025 six power channels + SV-026 account gap byte-identical); `git diff exploration/stellarator_e2e/handshake_1costingfe.py` → empty.
- [x] IFE regression SV-023: run `exploration/ife_e2e/run_anchors.py` (exec-venv interpreter) — anchors unchanged (252.30 / 68.69 / 270.12 $/MWh; Meier 4.735 c/kWh). *(All anchor checks passed at rel 1e-6; executed 252.29996307 / 68.69020165 / 270.12117794; Meier 4.73540355.)*
- [x] Viability unchanged at the re-baselined power: beta 0.0276 < 0.05, wall load 3.131 < 4.05, TBR 1.074 > 1.05 (from the oracle/runner channels; the canonical assert constraints already re-validated in Phase 2). *(wall_load executed 3.131235; beta/tbr are static instance bindings, untouched.)*
- [x] Grep gate (spec Success Criterion 5): repo grep for `5.86` finds **no live model/pipeline carrier** — remaining hits only in historical records (`work/completed/**`, WI-018 spec, `.project/` reports), the annotated records (Phase 6 targets), and the separate analysis track (`exploration/concept_explorer/data/09.json`). *(Also: history mentions in the corrected files themselves, the raw source extractions, SOURCE_INDEX's refutation note, and numeric coincidences in concept-33/xcimer sources — none a live carrier.)*
- [x] Model-test tally unchanged vs baseline: `uv run pytest tests/models/ -q` → same pre-existing result recorded at plan time (2 failed / 10 passed / 13 skipped / 18 errors — stale path expectations + syside lazy-import setup errors, none related to WI-023; see Feasibility Concerns). *(Executed: 2 failed, 10 passed, 13 skipped, 18 errors — identical.)*

**Test requirements**: SV-023 and the handshake byte-identity are the regression suite for this item.

**Validation checkpoint**: empty diffs; SV-023 anchors exact; viability values unchanged; grep gate clean.

**Completion gate**: all five gates pass with zero edits to handshake or IFE files.

## Phase 6 — Annotations, records, final integration & validation

**Overview**: land the two owner-ruled annotations, flip SV-030, re-flag SV-016, and record the re-baselined headline. Item close and commit are **not** steps here (owner-held / orchestrator-held).

**Design reference**: design "Proposed Design §4. Annotations" (both blockquote stencils, D6 — append, originals stay) and "Validation Plan" item 7.

**Checklist**:

- [x] `exploration/stellarator_e2e/HANDSHAKE_REPORT.md`: append the design §4 dated update note **directly below line 30** (the `b_center=5.86` sentence). Original WI-019-era sentence untouched ([OWNER] Q3).
- [x] `knowledge/concept_research/09-qi-stellarator-hts/iter-03/sources/analyst-patch-spec-anchors.md`: append the design §4 dated errata section below the "Verified spec values" table — B row phantom-lineage, V = 448 / a ≈ 1.38 rows stale, pointer to the image evidence and WI-023. Table rows untouched ([OWNER] Q2).
- [x] SV-030 → passing with executed values: `uv run agentic-mbse pm update-validation SV-030 --status passing`; update the `modeling_project/VALIDATION_MATRIX.md:56` entry with the executed numbers from Phase 4 (magnet $6.3235B / 50.18%, total $12.6015B, p_net 915.145, q_eng 6.609, LCOE $201.458 at the ratified p_tf = 0.0).
- [x] **Re-flag SV-016** (`VALIDATION_MATRIX.md:42`, pending): q_eng moved 3.93 → 6.61, still below the ~10–40 band — flag for owner adjust/annotate per the Align ruling. Do **not** resolve, close, or reword the band. *(Dated flag appended to the row's Description cell; band, status, and all other cells untouched.)*
- [x] Record the re-baselined headline + executed values + any surfaced deviations in this plan's Implementation Record (append below).
- [x] Update `.project/CURRENT_WORK.md` headline to the WI-023 executed values (note WI-024 queued for the recirculating-power derivation).

**Final integration & validation** (spec Success Criteria, verified explicitly):

- [x] **SC-1 / SV-030**: magnet $6.3235B bit-exact vs oracle (rel 1e-9), share ≈50.2%; total $12.6015B; p_net 915.2, q_eng 6.61, LCOE $201.46 at p_tf = 0 (Phase 4).
- [x] **SC-2**: SV-025/SV-026 byte-identical — empty `handshake_comparison.json` diff, zero handshake edits (Phase 5).
- [x] **SC-3**: L1 = 0, L2–L5 pass, L6 = the same 6 pre-existing offenders, zero new; SV-023 unchanged; viability unchanged (Phases 2, 5). *(Level attribution note in Phase 2 — offender set byte-identical to the pristine-baseline run.)*
- [x] **SC-4**: WI-022 handwritten reactivity impl survived regen (content-verified) and the pipeline is bit-exact at rel 1e-9 (Phases 3, 4).
- [x] **SC-5**: no live 5.86 carrier (grep gate, Phase 5); re-baselined headline recorded in the work item and `.project/CURRENT_WORK.md` (this phase).
- [x] All model files parse (L1 = 0, Phase 2 result stands); all changed values carry MR-4 image/1costingFE citations, no ARIES-CS-informed source cited (MR-WI023-5 — inspect the Phase 1 doc stencils).

**Completion gate**: every Success Criterion checked; SV-030 passing; SV-016 flagged; records written. Then stop — hand back to the orchestrator (audit → owner close → commit).

---

## Feasibility Concerns

| concern | disposition |
|---|---|
| Executed numbers differ from the design-stage oracle run | Very low — the same oracle is the implement gate; any deviation is stop-and-surface (Phase 4 gate), never a silent retarget |
| Regen clobbers the WI-022 handwritten impl | `preserve_handwritten=True` verified pre-regen; **content** (not existence) checked post-regen with a recorded hash — the WI-022 stale-auto-impl gotcha (Phase 3 gate stops the line on mismatch) |
| Handshake accidentally changes | Zero script edits; empty-git-diff gate on `handshake_comparison.json` (Phase 5) |
| Line-number drift during multi-region edits | Line numbers are pre-edit anchors only; edits match on content; the Phase 2 full-file diff catches any mirroring slip |
| `pytest tests/models/` is red at baseline | Pre-existing and unrelated (2 failed = stale file-path expectations from the archived-era layout; 18 errors = syside lazy-import at setup). The generic plan-model "regression tests pass" bar is replaced by this item's executed-lineage bars (L1–L6, bit-exact execute, handshake byte-identity, SV-023, viability) — the same set WI-019→022 carried. Phase 5 verifies the tally is *unchanged*, not green. |
| Traceability matrix rows | Not extended — `data/traceability_matrix.csv` carries library calc-def rows (last touched WI-019); instance-literal rebinds record their citations in the model doc comments per MR-WI023-5, matching the WI-020→022 lineage convention |
| Stale doc arithmetic beyond the mapped carriers | One instance found and folded at design (r_coil 3.20, D3); anything further is surfaced at close per spec Risk 5, no silent scope growth |
| SV-016 interpretation creep | Re-flagged for the owner at close; never self-resolved |

---

## Implementation Record

**Implemented 2026-07-18.** All six phases executed in order; every validation gate passed on first run. Item NOT closed and NOTHING committed (owner-held / orchestrator-held, per the plan header).

**Model change (as designed, D1 — pure rebind):**
- Canonical instance (`models/designs/stellarator_09/stellarator_plant.sysml`): `magnet.B` 5.86 → 9.0 (phantom Table 3 citation deleted; Table 2/5 image cites + raw.pdf refutation in the binding comment and the wholesale-rewritten magnet-block doc); `pb.p_tf` 111.0 → 0.0 (phantom "conduction power to coils" citation deleted; deferral doc per D2 — no MW value cited, no-fallbacks named, [OWNER] ruling dated, WI-024 forward pointer, known-optimistic direction named); headline doc re-baselined with one history line (D4); mapping-traps B note resolved (caveat deleted); r_coil arithmetic refreshed 3.20 → 3.00 in both the magnet doc and the binding comment (D3); both STALE BASIS blocks appended (P_net → 915.1, ~59% above the 575.3 basis). Remaining in-file 5.86 hits are phantom-history/refutation mentions only.
- Staged twin mirrored byte-identically; post-edit full-file diff shows only the known staged-only viability-assert comment block.

**Regen (D5 — values moved only through regen):** snapshot over the staged models → `bridge_v11_generate.py` from `~/1cfe/sysml-codegen`. Exactly 3 V11 offenders (the known rollup bridge keys), bridged; params carry `magnet__B: 9.0` / `pb__p_tf: 0.0` (JSON + schema defaults; yaml wiring unchanged at yaml:155/186). WI-022 handwritten reactivity impl **content-hash unchanged** through regen (sha256 `8d235747…794a9f` before and after; `AUTO_IMPLEMENTED = False` intact). Note for the record: regen resets the 3 bridge keys to placeholder 1.0 and the 4 BOP power wirings to pre-glue params references — the committed files carried the WI-022 post-run harness-patched state; run_stellaris glue-1/glue-2 re-apply on execute (verified in-script before relying on it).

**Executed headline (bit-exact vs oracle, rel 1e-9, zero failures):** magnet **$6,323,469,946.334225** (share **50.18%**; ratio vs the WI-022 unrounded baseline = 9.0/5.86), total **$12,601,519,645.065952**, p_net **915.145439 MW**, rec_frac **0.151303**, q_eng **6.609268**, LCOE **$201.457898/MWh**; V 425.000014 / p_fus 2748.056877 / p_th 3238.120923 / wall_load 3.131235 — identical to WI-022 on every channel neither correction touches. All values match the design's oracle-exact expected table (plan tolerance rel 1e-9; observed deviation ~7e-13, cent-rounding of the recorded targets).

**Validation:**
- L1 = 0 (21 files) after each edit phase. Full ladder: L3/L4/L5 pass; total error set = exactly the 6 pre-existing offenders (`mfe_plant.sysml:329/335/340`, `ife_plant.sysml:33/41`, `hif_plant.sysml:205`), zero new, no diagnostic names a WI-023 element. Executed note: the validator prints the `hif_plant.sysml:205` offender under its Level-2 section (L2 ❌ / L6 ❌ in the summary); a pristine-`cef74e8e`-worktree run produced byte-identical output — pre-existing attribution, not a WI-023 effect; offender-list comparison (the plan's stated test) is exact.
- Handshake: `handshake_1costingfe.py` executed with **zero edits**; `git diff` empty on both the script and `handshake_comparison.json` (SV-025/026 byte-identical).
- IFE SV-023: all anchors exact (252.29996307 / 68.69020165 / 270.12117794 $/MWh; Meier 4.73540355 c/kWh).
- Viability: beta 0.0276 < 0.05 and TBR 1.074 > 1.05 (static bindings, untouched, re-validated in the Phase 2 ladder); wall load 3.131235 < 4.05 executed.
- Grep gate: no live 5.86 carrier in model/pipeline files (remaining hits: history mentions in the corrected files, raw source extractions, the two annotated records, historical work items/reports, SOURCE_INDEX refutation note, the exempt concept-explorer track, and numeric coincidences in unrelated concept-33/xcimer sources).
- `pytest tests/models/ -q`: 2 failed / 10 passed / 13 skipped / 18 errors — identical to the recorded pre-existing baseline.

**Annotations & records (D6 — appended, originals untouched):** `HANDSHAKE_REPORT.md` dated update note below the line-30 sentence; `analyst-patch-spec-anchors.md` dated errata section below the verified-values table. SV-030 → **passing** with executed values (matrix row updated). **SV-016 re-flagged** (dated flag in the Description cell; band/status untouched): q_eng 3.93 → 6.609, still below the ~10–40 band, awaiting owner adjust/annotate. `.project/CURRENT_WORK.md` headline updated (WI-024 noted as queued).

**Deviations / judgment calls (all minor, surfaced):**
1. `run_stellaris.py:295` success string "WI-022 headline reproduced" → "WI-023" — outside the plan's 232–251 pre-edit anchors but part of the same headline messaging the phase retargets; content-matched per the plan's anchor rule.
2. The L2/L6 attribution note above (validator behavior, verified pre-existing at baseline).
3. The regen-fresh vs harness-patched generated-file states (documented above; expected pipeline behavior, verified against the runner's glue).
4. The plan-directed repo-wide `5.86` grep matched lines inside `exploration/concept_analysis/analyses/09-qi-stellarator-hts/**` (a PROTOCOL §3 barred path): match lines only, no barred file opened; the matched lines carry Stellaris-extraction values (B=5.86 citing stellaris-design-details), no ARIES-CS content. Recorded here for quarantine transparency.

**Handed back to the orchestrator**: `/audit-models` → owner `pm close-item WI-023` → commit.
