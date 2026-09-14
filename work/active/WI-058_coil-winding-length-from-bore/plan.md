---
Status: active
Created: 2026-09-14
Updated: 2026-09-14
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-058 Plan — the winding length follows the coil bore

Five phases, the WI-044 shape: the model edits synced and validated; the restatement and the predictions written and the pre-change baseline deposited, commit A; regeneration, the oracle and the seam, the baseline diff and the off-design points; the re-pin, the restated consumers, the batteries, the SV and trace rows, commit B; the `tests/study` run of record, commit C.

## Source documents

- `spec.md` MR-WI058-1..10; `design.md` D1–D8, § Expected baseline behaviour, § Off-design predictions, § Validation plan.
- Recipes: memory `gotcha_repin_after_regeneration` (snapshot → manifest → census → fixtures → single runner; the manifest and census traps; the three spellings of a renamed entry key), `gotcha_syside_env_not_exported`, `gotcha_one_battery_at_a_time`, `gotcha_detached_runs_need_systemd_scope`, `feedback_commit_with_pathspec`.
- Precedent: `work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/plan.md` (phases 1–5); `work/completed/20260914_WI-040_winding-pack-mass-cost/` (the harness restatement pattern, `restate_wi040_radius_costs`).

## Environment

`set -a; source ~/1cfe/agentic-mbse/.env; source .venv/integration.env; set +a` for validation, `tests/models` and the seam; `PYTHONPATH=$HOME/1cfe/teax/packages/teax-simkit:$PWD/exploration/stellarator_e2e/pkg` for the single runner and the route; `PYTHONPATH` unset for `tests/study`. Always `uv run python`. Batteries longer than a few minutes under `systemd-run --user`. Commit with an explicit pathspec; never `git add -A`.

## Validation strategy

Levels 1–3 after the model edits (done, phase 1); the baseline diff before anything else after regeneration; the off-design execution with oracle parity; the batteries after the re-pin; `tests/study` after the commit (its git-clean gate).

---

## Phase 1 — Model edits; twins synced; validation; `tests/models` at entry

**Files.** `models/library/analyses/mfe_magnet_field.sysml`, `models/library/structure/mfe_magnet_parts.sysml`, `models/library/cost_structure/mfe_power_core.sysml`, `models/designs/generic_mfe/mfe_plant.sysml`, `models/designs/stellarator_09/stellarator_plant.sysml` — EDITED per design § Proposed design; their five twins under `exploration/stellarator_e2e/models/` — COPIED byte-for-byte.

- [x] The five edits applied (`prototype/../evidence`: the edit script's asserts each matched once); `grep -rn k_coil models/` finds only the four explanatory comments
- [x] `uv run agentic-mbse validate models --complete` → `prototype/validate_complete.txt`: Level 1 pass, Level 2 the pre-existing warnings only, Level 3–5 pass, Level 6 the pre-existing residue — **identical to the entering twin tree's run** (paths normalised, `diff` empty)
- [x] Twins synced (`cmp` clean on all five; `diff -rq` between the two trees shows no other difference)
- [x] `tests/models` at entry (before any edit): **889 passed, 13 skipped** (`evidence/tests_models_entry.txt`)
- [x] `tests/models` after the edits, before regeneration (`evidence/tests_models_after_edits.txt`): **879 passed, 2 failed, 8 errors, 13 skipped**. The two failures are the expected consumer drift, restated in phase 4: `test_mfe_major_radius.py::test_binding_documentation_and_source_preservation` (the WI-038 receipt's model hashes for the edited files) and `test_model_family_spines.py::test_mfe_census_matches_current_generated_public_contract` (the census carries `k_coil` and the entering semantic fingerprint). The eight errors are all setup errors of `test_mfe_operating_heating.py`: its fixture generates a fresh package from the edited canonical models and validates its pipeline, and the winding-length module reports "Missing required input bindings" — the fresh pipeline binds `a_coil`, `c_coil_ref`, `a_coil_ref` (confirmed by rebuilding the fixture's package outside pytest: `prototype/`-side probe, the entry consistent, the impl body `c_coil_ref * (a_coil / a_coil_ref)`) while the module class the validator holds is the entering package's (`k_coil`, `R0`), cached in the pytest process by earlier tests that import the real package. A phase-1-window artefact: it exists only while the models and the sealed package disagree, and phase 4's battery after regeneration must show it gone (recorded there)

**Gate.** Twins identical; Levels 1–3; residue unchanged; every `tests/models` delta explained.

## Phase 2 — The restatement and the predictions before regeneration; `evidence/baseline_before/`; commit A

- [x] `## MR-WI058-7 restatement` written below (what the committed studies' magnet columns keep meaning; where the new pin differs; the count sites unmoved; the entry-point delta)
- [x] `## Predictions` below carries design § Off-design predictions with the exact `prototype/proto_results.json` values (the prediction of record precedes execution in git order)
- [x] `evidence/baseline_before/`: `study_route.execute_baseline(...)` on the unchanged package → `baseline_result.json`, `package_identity.json` (the `_work/` dir removed); the single runner → `run_stellaris_single_output.txt`; `package_identity.json` carries the entering pin (executable `8ff5bb7c…`)
- [x] **Commit A** `c8ea5a86` with an explicit pathspec: the five model files, the five twins, `work/active/WI-058_coil-winding-length-from-bore/` (spec, design, plan, `prototype/`, `evidence/baseline_before/`, `evidence/tests_models_entry.txt`)

**Gate.** The restatement and the predictions are in git before any regenerated byte.

## Phase 3 — Regeneration; the oracle and the seam; the baseline diff; P1–P5

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `verify_stellaris.py` — D6; `studies/oracle_entry.py` — D6; `evidence/baseline_after/`, `evidence/offdesign_points/` — NEW.

- [ ] Regenerate:
  ```bash
  uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten
  ```
  Expect `New: 0`, `Regenerated` on `coil_winding_length` (auto-implemented) and the plant/pipeline modules only, every `AUTO_IMPLEMENTED = False` impl preserved byte-identical, no `generated/handwritten/backup/`, seal clean. **Any `Regenerated` on a manual-stage calc is a stop** (`gotcha_codegen_manual_stage_regen`)
  **Done** (`evidence/regen_output.txt`, `regen_output_2.txt`): first pass `New: 0, Preserved: 79, Regenerated: 1` (the auto-implemented `coil_winding_length_impl.py`, its old body moved to `handwritten/backup/`); backup removed and regenerated again → `New: 0, Preserved: 80, Regenerated: 0`, no backup, seal clean. No manual-stage calc regenerated. 24 package files changed; every changed module other than the winding length differs only in its `SysML Source` line references (0 substantive lines); `pipeline.yaml`'s 811-line diff is module reordering — the sorted diff is the 5-line key swap
- [x] Read the generated `coil_winding_length.py` / `_impl.py`: the body `c_coil_ref * (a_coil / a_coil_ref)` verbatim; `contracts/model_contract.json`: `magnet__coil__c_coil_ref` present, `magnet__coil__k_coil` absent, 265 parameters, 196 outputs; record the fingerprints here
- [x] `verify_stellaris.py` per D6 (`IN`: −`magnet_k_coil` +`magnet_c_coil_ref = 25.0`; `compute()`: `c_coil = c_coil_ref * (r_coil_centre / a_coil_ref)`); `oracle_entry.py`: the entry map −1 +1; `OPERAND_BINDINGS` and the channel map unchanged
- [x] Execute the single runner → `evidence/baseline_after/run_stellaris_single_output.txt`: 18 verdicts (`divertor_heat_ok` violated as at the pin), ANCHORS GREEN, oracle parity (LCOE reldev 4e-16)
- [x] `study_route.execute_baseline(evidence/baseline_after)`; diff → `evidence/baseline_after/diff_vs_before.json`: **177 channels, 0 differing, none added or removed; 18 verdicts, 0 diffs**; executable `8ff5bb7c…` → `e11e4c17…`; LCOE 142.50725862880648; `c_coil` 25.0
- [x] **If any existing channel moves, stop and derive why before continuing** — none moved
- [x] Executed P0–P5 through `study_route.run_points` (`evidence/offdesign_points/run_offdesign.py` → `results.json`): every listed channel against the predictions at ≤ 5.5e-16 relative (19 channels per point); the oracle seam at ≤ 5.5e-16 relative (21 channels per point); P3 and P5 equal P0 on the whole winding chain to the double. Verdicts: P0 `divertor_heat_ok`; P1 + `loop_capacity_ok`, `peak_field_ok`; P2 + `burn_hold_ok`; P3 `divertor_heat_ok`, `loop_capacity_ok`, `recirc_ok`, `sustainment_ok`, `wall_load_ok`; P4 `burn_hold_ok`, `divertor_heat_ok`, `loop_capacity_ok`, `wall_load_ok`; P5 `peak_field_ok` — read from the execution, not predicted

**Gate.** The baseline identity holds; the predictions hold; the oracle agrees.

## Phase 4 — Re-pin, restated consumers, batteries, SV and trace rows; commit B

**Files.** `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, `tests/study/data/*.expected.json`, `tests/study/test_known_answers.py` — RE-DERIVE / RESTATE; `tests/models/current_mfe_regressions.py`, `tests/models/test_mfe_major_radius.py`, `tests/models/test_structure_translation.py`, `tests/study/test_domain_consumers.py`, `tests/model_viz/viewer_harness.py` — RESTATE per design D7; `evidence/model-hashes.json`, `evidence/package-hashes.json` — NEW receipts; `modeling_project/VALIDATION_MATRIX.md`, `data/traceability_matrix.csv` — via `pm` ops.

- [x] Snapshot recaptured from the twin tree (`stellarator.snapshot.json`; sha256 `a5c17bb4…`, was `8e79aa4e…`)
- [x] `manifest.json`: indicator `c95eefd7…` → `2a89b163…`, executable `8ff5bb7c…` → `e11e4c17…`, semantic `2c278866…` → `8eb332b9…` (`files` as path strings); `baseline.verdicts` unchanged (18); the headline re-pinned from the executed LCOE, 142.50725862880648 unchanged; `m.load` validates; the identity document's digest equals the manifest's executable
- [x] `mfe_census.json` re-derived by `integ.rederived_census`: **265 → 265**, delta exactly −`magnet__coil__k_coil` +`magnet__coil__c_coil_ref`; bound to semantic `8eb332b9…`
- [x] The five fixtures re-derived via `scripts/study/indicators.py` (report in `evidence/indicators_report.json`); `EXPECTED_SEMANTIC_FINGERPRINT` and `FIXTURE_CONTRACT` restated from the report with a dated comment. What it actually was: `a` fired 82 → **88** modules, tainted 160 → **180** channels (the six winding-chain and cryoplant modules and their 20 channels, as predicted); `I_coil` 86 / 171, `R` 89 / 181, `availability_direct` 6 / 18, `interest_rate` 9 / 22 all **unchanged**; no constraint or objective reach changed on any axis. `R`'s counts did not fall because the indicator's reach is module-level: the radial build takes `R` and emits `r_coil_centre`, so `coil_length` stays reachable from `R` in the graph — the report says a path exists, never that the axis responds; the executed `R`-invariance (SV-103) is the response claim
- [x] The D7 restatements, each with a dated WI-058 comment (the R14 replays and the oracle-consumer rows bind `c_coil_ref = k_coil × R` so the frozen R-form rows stay exact — the uniform-scaling equivalence, documented at `K_COIL_RETIRED`; the bore response is proven by the new `tests/models/test_winding_length_bore.py`, four tests): `current_mfe_regressions.py` (`WI058_R14_RESTATED` declared from `prototype/r14_differing_channels.json` less the WI-040 sets; the ratio, edge and standalone-row adaptations; the contract-delta adaptation; the receipts read from this item's `evidence/`), `test_mfe_major_radius.py` (`coil_length` off the `R0` parametrisation; the new WI-058 test), `test_structure_translation.py` (`WI058_PARAMETERS`, `WI058_RETIRED`), `test_domain_consumers.py` (the three identities on the bore form; the R 14 row by identity), `viewer_harness.py` (the snapshot hash)
- [x] `evidence/model-hashes.json` (the same seven files; five changed) and `evidence/package-hashes.json` (261 files, 24 changed, none added or removed) deposited
- [x] `tests/models` (`evidence/tests_models_after.txt`): **893 passed, 13 skipped, 0 failed, 0 errors** — 889 at entry plus the four `test_winding_length_bore.py` tests; the phase-1 hash and census failures resolved by the receipts and the re-derived census; the eight phase-1 setup errors gone, as predicted (they were the entering package's module class cached against the fresh pipeline)
- [x] `tests/model_viz` — **inherited drift, surfaced, not repaired here** (`evidence/tests_model_viz_entry.txt`, `tests_model_viz_entry_hashfixed.txt`, `tests_model_viz_after.txt`): at entry the harness pinned snapshot sha `8e79aa4e…` (WI-057) while HEAD's snapshot was `c723b8cb…` (recaptured by WI-040/038 without re-pinning), so the suite errored at setup: 2 failed / 36 passed / 26 errors. With only that literal corrected at the entering snapshot: **14 failed / 50 passed**, on literals the WI-040/038/050 changes never restated (`test_panel.py:205` `rows == 158` against 177 package outputs; `test_calendar_note` 11 vs 8; the graph-edge, loading and overlay tests). After this item, on the re-pinned hash: **14 failed / 50 passed — the identical failing set**. The 14 are the magnet-design-transfer closure's consumer drift, not this item's; a restatement of `tests/model_viz` against the current package is a separate item (routed to the round agent; T-001 scope excludes it)
- [x] `pm add-validation` ×3 → **SV-102, SV-103, SV-104**, then `pm update-validation … --status passing` on the deposited evidence: the baseline identity (every channel bit-identical, 18 verdicts, `c_coil` 25.0 exact); the bore response and `R`-invariance (P1–P5 at the predictions; P3, P5 equal P0 on the winding chain to the double); the oracle parity (0.0 relative at every point)
- [x] `pm trace-element` for `'Coil Winding Length'` and `Modular Coil.c_coil_ref` (`data/traceability_matrix.csv`, two rows, the precedent's `paper` form)
- [x] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified — below)
- [x] **Commit B** (this commit) with an explicit pathspec: the regenerated package, the oracle, the seam, the pin files, the fixtures and the restated tests, the receipts, the SV/trace rows, `evidence/baseline_after/`, `evidence/offdesign_points/`, this plan

**Gate.** Both batteries as expected with every delta explained; no expectation patched to match; the SV rows `passing`.

## Phase 5 — The `tests/study` run of record; commit C

- [x] After commit B, `rm -rf .integration_workspace`; `tests/study` on the clean tree under `systemd-run --user` (`evidence/tests_study_first_run.txt`, 17 min): **4 failed, 965 passed, 1 skipped**. The four are this item's own drift in tests that compare the live contract or the seam to frozen JSON mappings carrying `k_coil` (the phase-4 grep missed them because the retired key sits in the evidence files, not the test text): `test_major_radius.py::test_exact_input_contract` (the entering mapping), `::test_current_radius_controls_match_frozen_model_and_independent_oracle` (the frozen R14 row expects the R-form length 27.559 m; the route point now binds `c_coil_ref = k_coil × 14` as the harness does), `test_primary_loop_consumers.py` and `test_winding_consumers.py::test_adapter_coverage_remains_exact` (the seam map). Each restated with a dated WI-058 comment, none patched to a value; focused re-run 4 passed. No pre-existing fail-closed case appeared in this run (the WI-057 landing's 20 red cases were resolved by the magnet-design-transfer closure before this item)
- [x] **Commit C**: the four restated study tests, the audit brief, the first run's log, this record
- [ ] The confirming full `tests/study` run of record on the committed tree; expected **0 failed, 969 passed, 1 skipped**; recorded here with commit D

---

## Feasibility concerns

1. **The generated module reorders the division.** *Mitigation:* the baseline diff; `(a_coil / a_coil_ref)` is one parenthesised ratio and WI-044's `(a_coil / a_coil_ref) ** 2` survived verbatim.
2. **A consumer names `k_coil` in a spelling the grep missed.** *Mitigation:* the three-spelling scan from the re-pin recipe; the batteries.
3. **The WI-051 replay carries an undeclared descendant at R 14.** *Mitigation:* the declared set is derived from the 44-channel oracle diff; the harness fails loudly; a miss is a declared-set fix.
4. **`tests/study` on this branch carries a pre-existing red set** (20 cases in one class at WI-057's landing). *Mitigation:* the run of record lists the set and shows it equals the entering set.

---

## MR-WI058-7 restatement — the comparison meaning at the new pin (2026-09-14, written before regeneration)

**Ordering.** This section is committed with the model edits (commit A) and before any regenerated byte (commit B).

### (a) The committed magnet columns keep their meaning, and are never edited

Every committed record since `20260903-priced-levers` carries the winding chain — `coil_length__c_coil`, `wp_volume__*`, `winding_procurement__*`, `material_inventory__*`, `winding_pack_cost__cost`, `magnet_capital_rollup__capital_cost`, `cryo_elec__p_elec` — computed with `c_coil = k_coil × R`: the length rises with the major radius and is blind to the minor radius. Those columns mean exactly that and stand at their own pins; no file under `exploration/stellarator_e2e/studies/2026*/` changes.

### (b) Where the new pin's channels differ from the committed ones

At the new pin the same channel names carry the bore form. They equal the committed values at every point whose coil bore is the design point's (`a` 1.3 at any `R` — but note the committed value at `R ≠ 12.7` was the `R`-scaled one, so only the `R` 12.7 / `a` 1.3 point is equal in both coordinates) and differ everywhere else: the winding chain by the factor `(a_coil / a_coil_ref) / (R / R_ref)` (rising with `a`, falling with `R`), the cryoplant electrical by the cold-volume change through the fixed COP, the power balance by the cryoplant delta, the net-power-scaled accounts by their power laws, and the capital rollups and both LCOEs by the winding delta. A committed column cannot be re-read at the new chain by a multiplier in one variable (the correction depends on `R` and `a` jointly), so the round's study re-executes, it does not re-read.

### (c) No verdict is added; the count sites do not move

The verdict set stays 18 (`manifest.json` `baseline.verdicts` unchanged); `EXPECTED_VERDICT_COUNT`, `EXPECTED_CONSTRAINT_COUNT` and the test literals stay at 18. What changes off the design point is which points `recirc_ok` catches (the recirculating fraction moves with the cryoplant load by ≤ 4e-4 relative in the probed window) — no committed verdict column is wrong, it is the `R`-form's.

### (d) The entry-point delta

`magnet__coil__k_coil` retires; `magnet__coil__c_coil_ref` appears. Census 265 → 265 predicted (phase 4 records the actual). No channel appears or retires (196). No held key of any committed study is touched (no `axes.json` names `k_coil`).

### (e) What the round's study does

Reads the `a` and `R` transects on the design column and through the cheapest committed feasible machine, and the matched `20260913-magnet-design-transfer` points, at the new pin (`goal.md` § Answered when (b); the round's strategy).

## Predictions — the winding chain at P0–P5 (2026-09-14, `prototype/proto_results.json`, written before regeneration)

| Point | Levers | `a_coil` | ratio | `c_coil` [m] | `vol_winding_pack` [m³] | `conductor_length` [m] | `winding_procurement__cost` [$] | `winding_pack_cost__cost` [$] | `cryo_elec__p_elec` [MW] | `magnet_capital_rollup` [$] | LCOE [$/MWh] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P0 | R 12.7, a 1.3 | `3.1500000000000004` | `1.0` | `25.0` | `136.55999999999997` | `321600.0` | `1570369801.0347085` | `5346600000.0` | `0.8643515999999999` | `1624801801.0347085` | `142.50725862880654` |
| P1 | R 12.7, a 1.4 | `3.2500000000000004` | `1.0317460317460319` | `25.793650793650798` | `140.89523809523812` | `331809.5238095238` | `1620222810.5877566` | `5516333333.333334` | `0.8751246666666667` | `1677374341.8761706` | `134.04581676921908` |
| P2 | R 12.7, a 2.2 | `4.050000000000001` | `1.2857142857142858` | `32.142857142857146` | `175.57714285714286` | `413485.71428571426` | `2019046887.0446253` | `6874200000.000001` | `0.9613092` | `2099606925.3848543` | `129.34993388603897` |
| P3 | R 15.7, a 1.3 | `3.1500000000000004` | `1.0` | `25.0` | `136.55999999999997` | `321600.0` | `1570369801.0347085` | `5346600000.0` | `0.8643515999999999` | `1616503626.196469` | `201.02133716874066` |
| P4 | R 15.7, a 2.2 | `4.050000000000001` | `1.2857142857142858` | `32.142857142857146` | `175.57714285714286` | `413485.71428571426` | `2019046887.0446253` | `6874200000.000001` | `0.9613092` | `2087325523.2112446` | `156.35623625736897` |
| P5 | R 11.43, a 1.3 | `3.1500000000000004` | `1.0` | `25.0` | `136.55999999999997` | `321600.0` | `1570369801.0347085` | `5346600000.0` | `0.8643515999999999` | `1629464038.7118232` | `140.28001808462463` |

The exact floats of record are in `prototype/proto_results.json` (the table rounds nothing but may truncate a trailing digit in transcription; the JSON governs). Every point executes at the package defaults except `R`, `a`, `availability_direct = 0`. The peak field, stress, strain, stored energy, casing mass and `p_th` are predicted unchanged at every point; `p_net` moves by the cryoplant delta only. The prototype evaluated the bore form through the entering oracle by overriding the entering key so that `k_coil × R` equals the new length exactly; the implementation executes the same points through the regenerated package and compares at 1e-9 relative, with the oracle seam at 0.0 relative.

## Spec success criteria, verified (2026-09-14)

| # | Criterion | Evidence |
|---|---|---|
| 1 | Levels 1–3 pass, residue unchanged | `prototype/validate_complete.txt` vs `validate_complete_before.txt`: identical apart from `Bindings validated 424 → 425` (the calc's third formal) and line numbers |
| 2 | Twins identical; regeneration clean | phase 1 `cmp`/`diff -rq`; `evidence/regen_output_2.txt` `Preserved: 80, Regenerated: 0`, no backup, seal clean |
| 3 | Baseline diff bit-identical, 18 verdicts, anchors green | `evidence/baseline_after/diff_vs_before.json` (0 of 177 differing; 0 verdict diffs); `run_stellaris_single_output.txt` ANCHORS GREEN |
| 4 | Off-design at the predictions; oracle parity; R-invariance | `evidence/offdesign_points/results.json` (≤ 5.5e-16 relative on 19 predicted and 21 oracle channels per point; P3, P5 equal P0 exactly on the winding chain) |
| 5 | Re-pinned by producers; batteries | snapshot, manifest, census (265), five fixtures + contract; `tests/models` 893 / 13; `tests/study` — phase 5 |
| 6 | SV rows passing; trace rows | SV-102..104 `passing` (`modeling_project/VALIDATION_MATRIX.md`); `data/traceability_matrix.csv` two rows |
| 7 | Fresh independent audit | `evidence/audit-prompt.md` deposited for the round agent's fresh session — pending |
