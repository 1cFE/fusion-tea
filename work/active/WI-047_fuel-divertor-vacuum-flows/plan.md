---
Status: active
Created: 2026-09-08
Updated: 2026-09-08
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-047 Plan — the fuel, divertor-heat and vacuum reduced flows

Five phases, the WI-044 shape, landing THIRD on the shared files after WI-045 (the loop and the cycle) and WI-046 (the calendar) — basis packet § 9. The "before" package of every diff here is the one WI-046's commit B leaves; the plan records its pin at phase 2.

## Source documents

- `spec.md` MR-WI047-1..13; `design.md` D1–D12, § Proposed design (the exact SysML text), § Expected baseline behaviour, § Off-design predictions, § Validation plan; `prototype/proto_results.json` (the prediction of record).
- `work/orchestration/goals/plant-closure/evidence/round1_basis_packet.md` §§ 2, 4, 5, 6, 9 and its Amendment (item 3: this item takes the verdict count 13 → 14).
- Recipes: memory `gotcha_repin_after_regeneration` (snapshot → manifest → census → fixtures → single runner; the two traps; "adding a verdict" — the five literal count sites); `gotcha_codegen_manual_stage_regen` (not expected: no manual stage here); `gotcha_syside_env_not_exported`; `feedback_commit_with_pathspec`.
- Precedents: `work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/plan.md` (the phases); `work/completed/20260907_WI-043_two-sided-sustainment-condition/plan.md` phases 4–5 (adding a verdict; the eight count sites).

## Design summary

Three flat calcs reading existing channels (`fusion.p_fus`, `sustain.p_alpha_heat` / `p_rad` / `p_aux_required`, `heat.p_coupled`) and thirteen instance facts; eighteen new channels; one constraint def and one assert; no existing channel moves; `divertor_heat_ok` VIOLATED at the baseline on the pessimistic case (10.535 against 10); the breeding margin −0.116 reported, never asserted; every missing input surfaced at its binding.

## Prototype baseline

`prototype/proto.py` → `proto_results.json` (2026-09-08): the P0 doubles; the source case exact (50.0; 9.5 / 5.0; 19.0 doubled); the 1.19 identity and the 0.99611 threshold; the lossless check; the molecule count; P3 `c2823` and P4 `c3598`. No model file touched yet.

## Environment

`set -a; source ~/1cfe/agentic-mbse/.env; source .venv/integration.env; set +a` for validation, `tests/models` and the seam; `PYTHONPATH=$HOME/1cfe/teax/packages/teax-simkit:$PWD/exploration/stellarator_e2e/pkg` for the single runner and the route; `PYTHONPATH` unset for `tests/study`. Always `uv run python`. Commit with an explicit pathspec; never `git add -A`.

## Validation strategy

Levels 1–3 after every model edit; the baseline diff before anything else after regeneration (every existing channel identical; one verdict added, violated); the off-design execution with oracle parity; the batteries after the re-pin; `tests/study` after the commit.

---

## Phase 1 — The model text in; validation; twins; `tests/models`

**Files.** `models/library/analyses/mfe_fuel_cycle.sysml`, `mfe_divertor_heat.sysml`, `mfe_vacuum.sysml` — NEW from design § Proposed design; `mfe_viability.sysml` — one constraint def after `'Neutron Wall Load Limit'`; `models/designs/generic_mfe/mfe_plant.sysml` — three imports, the fuel / divheat / vacuum blocks after `cas80_annual`, the assert after `cond_strain_ok`; `models/designs/stellarator_09/stellarator_plant.sysml` — the thirteen bindings and the `tbr` comment sentence; the six twins — COPY byte-for-byte.

- [x] Confirm the shared files are at WI-046's commit B (the packet § 9 order); record that commit here
- [x] Write the three library files and the constraint def verbatim from the design; add the plant blocks and the assert; add the instance bindings with their docs
- [x] `uv run agentic-mbse validate models` — Level 1 0 errors; Level 2 no new warning beyond the recorded set. **If the exact route refuses `in E_fus_J = fuel_q_eff * mev_to_joules;`** (the WI-028 bare-alias class), bind a plant attribute `fuel_E_fus_J : Real = fuel_q_eff * mev_to_joules;` and read it; record which form landed (design risk 2)
- [x] Copy the six files to their twins (`cp`); `cmp` clean; `diff -rq` between the trees shows no other difference
- [x] `uv run python -m pytest tests/models -q` — the count as WI-046 left it or better; any test counting attributes, formals, channels or constraints by literal recorded here and restated in phase 4 from the live package

**Gate.** Levels 1–3; twins identical; `tests/models` as expected with every delta explained.

## Phase 2 — The restatement and the predictions, written before regeneration; `evidence/baseline_before/`; commit A

- [x] Write `## MR-WI047 restatement` at the end of this plan: (a) no committed study record changes in meaning — the new channels did not exist in any committed record and none of the existing columns' semantics move; (b) one verdict is added and the fourteen-verdict "feasible" is a new set the study reports beside the ten (and beside WI-045's thirteen); (c) the count sites this item moves: `study_route.py` `EXPECTED_CONSTRAINT_COUNT` 13 → 14, `run_stellaris_single.py` `EXPECTED_VERDICT_COUNT` 13 → 14 and `EXPECTED_VERDICTS["divertor_heat_ok"] = "violated"`, `tests/study/test_operand_bindings.py`, `test_valid_empty.py`, `test_known_answers.py`, `studies/manifest.json` `baseline.verdicts`, `oracle_entry.OPERAND_BINDINGS`; (d) the entry points appearing (the thirteen instance facts; `s_per_fpy` and `k_B` if the census counts calc-formal defaults) and none retiring; (e) the expected baseline: every existing channel bit-identical, eighteen new channels at the design's doubles, `divertor_heat_ok` violated
- [x] Copy design § Expected baseline behaviour and § Off-design predictions into `## Predictions` below with the exact `proto_results.json` doubles (the prediction of record precedes execution in git order)
- [x] `evidence/baseline_before/`: `study_route.execute_baseline(...)` on WI-046's package → `baseline_result.json`, `package_identity.json` (remove `_work/`); the single runner's output → `run_stellaris_single_output.txt`; record the pin's indicator digest here
- [x] **Commit A** with an explicit pathspec: the four library files, the plant, the instance, the six twins, `work/active/WI-047_fuel-divertor-vacuum-flows/` (spec, design, plan, `prototype/`, `evidence/baseline_before/`); the message names the restatement as preceding regeneration

**Gate.** The restatement and the predictions are in git before any regenerated byte.

## Phase 3 — Regeneration; the oracle and the seam; the baseline diff; P3 and P4

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `verify_stellaris.py` — ADD the three derivations (D11); `studies/oracle_entry.py` — the thirteen levers, the eighteen channels, one binding; `run_stellaris_single.py` — the verdict and the count; `studies/study_route.py` — the count; `evidence/baseline_after/`, `evidence/offdesign_points/` — NEW.

- [x] Regenerate:
  ```bash
  /home/reid/1cfe/fusion-tea/.venv/bin/sysml-codegen generate --models exploration/stellarator_e2e/models \
    --output exploration/stellarator_e2e/generated --package-name stellarator_tea \
    --overwrite --smart-regen --preserve-handwritten
  ```
  Expect `New: 4` (three calc modules + the constraint module), `Regenerated` on the plant module only, every handwritten impl preserved byte-identical (WI-045's cycle impl and WI-046's calendar impl included), no `generated/handwritten/backup/`, seal clean. **Any `Regenerated` on a manual-stage calc is a stop** (`gotcha_codegen_manual_stage_regen`)
- [x] Read `generated/contracts/model_contract.json`: the constraint id `stellarator_09__stellaris__divertor_heat_ok__<hash>` and its evaluation channel; the eighteen channel keys (`fuel__*` 7, `divheat__*` 9, `vacuum__*` 3 — `n_molecules` included); the new entry keys; record all here
- [x] Read the generated `divertor_heat_ledger.py`: `p_target_nonrad = p_heat_abs - f_rad_total * p_heat_abs` verbatim (D4 — the exact source reproduction depends on the form)
- [x] `verify_stellaris.py` per D11: `IN` + the thirteen instance doubles; `compute()` + the fuel block, the ledger, the gas load, written from the design's equations; the return dict + eighteen
- [x] `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` + thirteen; `ORACLE_OUTPUT_TO_CHANNEL` + eighteen; `OPERAND_BINDINGS` + one entry for the read constraint id (`q_target_peak_in` ← the `divheat__q_target_peak` channel key; `q_target_limit_in` ← the `q_target_limit` input key)
- [x] `run_stellaris_single.py`: `EXPECTED_VERDICTS["divertor_heat_ok"] = "violated"` with the comment (10.535 against 10 on the pessimistic case by the model's 10.9 % absorbed-heating excess; disclosed, never tuned; the low case reads 5.545); `EXPECTED_VERDICT_COUNT = 14`; the parity message restated (thirteen satisfied, one violated — not `full_satisfaction`); the oracle gate's channel list + the eighteen
- [x] `study_route.py`: `EXPECTED_CONSTRAINT_COUNT = 14` with a dated comment
- [x] Execute the single runner → `evidence/baseline_after/run_stellaris_single_output.txt`; verdict parity 14; the oracle gate passes on every new channel (rel 1e-9)
- [x] `study_route.execute_baseline(evidence/baseline_after)`; diff `baseline_result.json` before/after: **every existing channel bit-identical; eighteen new channels at the predicted doubles; the verdict list gains exactly `divertor_heat_ok: violated`; nothing else** — record the diff here
- [x] **If any existing channel moves, stop and derive why before continuing** (`goal.md` § Invariants)
- [x] Execute P3 (`c2823`: R 15.7, a 2.2, 13 MA, 13 keV, n 5.06e20, 100 MW) and P4 (`c3598`: R 17.2, a 2.2, 14 MA, 13 keV, 100 MW) through `study_route.run_points` with proposals in the `20260907-minor-radius/study.py` `point()` shape and `required_channels` covering the eighteen; deposit `evidence/offdesign_points/results.json`; compare `divheat__q_target_peak` (20.331362085603267 / 22.535740772495682), `q_target_peak_area_scaled` (16.446388438672706 / 16.639…), `fuel__*` and `vacuum__*` to `## Predictions` at 1e-9 relative; read `p_sep` and `f_rad_edge` (unpredicted — no `p_rad` in the committed CSV) and check `p_sep > 0`; the oracle seam's `evaluate()` at both points → 0.0 relative deviation on all eighteen; `divertor_heat_ok` re-derived through the binding agrees (violated at both)
- [x] The oracle's source-case check: with `p_heat_abs` 500 and `p_rad_core` 0 the oracle's ledger reads `p_target_nonrad` 50.0 and peaks 9.5 / 5.0 exactly; doubled 19.0 — deposit under `evidence/source_case/`

**Gate.** The baseline identity holds; the one verdict change is the predicted one; the predictions hold; the oracle agrees.

## Phase 4 — Re-pin, fixtures, batteries, SV and trace rows; commit B

**Files.** `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, `tests/study/data/*.expected.json`, `tests/study/test_known_answers.py`, `test_operand_bindings.py`, `test_valid_empty.py` — RE-DERIVE / RESTATE; `modeling_project/VALIDATION_MATRIX.md`, `data/traceability_matrix.csv` — via `pm` ops.

- [x] Snapshot recaptured from the twin tree
- [x] `manifest.json`: the three fingerprints from the package's contracts (`files` as path strings); `baseline.verdicts` gains `{"source_local_identity": "divertor_heat_ok", "expected": "violated"}` (fourteen entries); `baseline.headline.value` re-pinned from the executed LCOE (expected unchanged from WI-046's pin — this item moves no number); `m.load(manifest)` validates
- [x] `mfe_census.json` re-derived (`integ.rederived_census(pkg)` + the new semantic fingerprint); expect WI-046's count + 13 (or + 15 with the two calc-formal defaults) — record the actual count and delta
- [x] The six fixtures re-derived via `scripts/study/indicators.py --package … --manifest … --groups tests/study/data/axes.known_answers.json`; `EXPECTED_SEMANTIC_FINGERPRINT` and `FIXTURE_CONTRACT` restated **from the report** (predicted: every axis reaching `p_fus` — R, R+tie, a, I_coil — gains the three modules and their channels, and `divertor_heat_ok` becomes reachable on them; `availability` / `availability_direct` and `interest_rate` unchanged) with a dated comment
- [x] The literal count sites restated from the live package with a WI-047 comment: `tests/study/test_operand_bindings.py` (fourteen), `test_valid_empty.py` (bounds / `constraints_unreachable`), `test_known_answers.py` (`constraints_unreachable` on the axes that reach none)
- [x] `uv run agentic-mbse validate models --complete` — compare with WI-046's run; record any new residue
- [x] `tests/models` — every delta explained
- [x] `rm -rf .integration_workspace`; `tests/study` — expect green apart from the branch's known fail-closed cases; every other delta explained
- [x] `pm add-validation` ×4 then `pm update-validation … --status passing` with the evidence paths: (1) the source case reproduced exactly (500 → 50; 9.5 / 5.0; 19.0 doubled; oracle and package); (2) the fuel identities (1.19 at 0.99; loss 0 and `tbr_required` 1.0 at `t_recycle` 1 for three burn fractions; the 0.9961052631578947 threshold); (3) the molecule count (atoms / molecules 1.95 at the design point; doubling every rate doubles `S_eff_required`); (4) the baseline's disclosed verdict (every existing channel bit-identical; eighteen new channels at the predictions; `divertor_heat_ok` violated at 10.535329131066188; oracle parity 0.0; P3 / P4 as predicted)
- [x] `pm trace-element` for `'Fuel Cycle Flows'`, `'Divertor Heat Ledger'`, `'Vacuum Gas Load'`, `'Divertor Target Heat Limit'` and the thirteen instance facts
- [x] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified — below)
- [x] **Commit B** with an explicit pathspec: the regenerated package, the oracle, the seam, the single runner, the route, the pin files, the fixtures and the three test files, the SV/trace rows, `evidence/baseline_after/`, `evidence/offdesign_points/`, `evidence/source_case/`, this plan; never `git add -A`
- [x] Note for the modelling PM: the BACKLOG row moves at close through `pm close-item`

**Gate.** Both batteries as expected with every delta explained; no expectation patched to match; the four SV rows `passing`.

## Phase 5 — The `tests/study` run of record; commit C

- [x] After commit B, `tests/study` on the clean tree (detached if longer than ten minutes); record the count and the failing set; confirm it equals the pre-existing fail-closed set or explain every difference
- [x] **Commit C**: any test-file restatement the run forced, and this plan's phase-5 record

---

## Feasibility concerns

1. **The codegen refuses the product on a calc input** (`E_fus_J = fuel_q_eff * mev_to_joules`). *Mitigation:* the plant-attribute fallback (phase 1); either form is value-identical.
2. **`p_sep ≤ 0` somewhere in the sweep** makes `f_rad_edge` nonfinite. *Mitigation:* the exporter's nonfinite refusal and the in-range channel; the study declares such points; no clamp (design risk 3).
3. **The census counts the two calc-formal defaults.** *Mitigation:* the actual delta is recorded, whichever it is.
4. **A count site beyond the seven named** (the WI-043 evidence found eight literal verdict-count sites). *Mitigation:* the batteries find it; each restated from the live package with a comment.

## Predictions — the nineteen new channels at the design point and the two off-design points (2026-09-08, `prototype/proto_results.json`, written before regeneration)

At WI-046's package state (`evidence/baseline_before/baseline_result.json`, sealed executable `e0d9b1ac19a440ff…`, 136 channels, thirteen verdicts, LCOE 224.60952472804465) the ledger's inputs are the pin's own — `fusion__p_fus` 2652.5632625175904, `sustain__p_alpha_heat` 504.49100689822046, `sustain__p_rad` 219.7216452237653, `sustain__p_aux_required` 49.07960078792678, `heat__p_coupled` 50.0 (read from that file) — so the design's predictions stand unchanged here. **Every one of the 136 existing channels is bit-identical after this item; the thirteen existing verdicts are unchanged; one verdict is added, violated.**

| Channel | P0 design point | P3 `c2823` (R 15.7, a 2.2, 13 MA, 13 keV, n 5.06e20, 100 MW) | P4 `c3598` (R 17.2, a 2.2, 14 MA, 13 keV, 100 MW) |
|---|---|---|---|
| `fuel__burn_rate` [atoms/s] | 9.417518585656878e+20 | 1.9042052198807694e+21 | 2.120783878472184e+21 |
| `fuel__inject_rate` | 1.8835037171313755e+22 | 3.8084104397615385e+22 | 4.241567756944368e+22 |
| `fuel__exhaust_rate` | 1.7893285312748067e+22 | 3.6179899177734618e+22 | 4.02948936909715e+22 |
| `fuel__loss_rate` | 1.7893285312748084e+20 | 3.617989917773465e+20 | 4.0294893690971534e+20 |
| `fuel__tbr_required` | 1.1900000000000002 | 1.1900000000000002 | 1.1900000000000002 |
| `fuel__tbr_margin` | -0.1160000000000001 | -0.1160000000000001 | -0.1160000000000001 |
| `fuel__burn_kg_per_fpy` [kg/FPY] | 148.74097510492368 | 300.75156064605267 | 334.95815187579154 |
| `divheat__p_heat_abs` [MW] | 554.4910068982205 | 1070.0716887159617 | 1186.0916196050364 |
| `divheat__p_sep` | 334.7693616744551 | read at execution (no `p_rad` in the committed CSV); expected > 0 | read at execution; expected > 0 |
| `divheat__f_rad_edge` | 0.8343662621559043 | read at execution | read at execution |
| `divheat__f_rad_edge_in_range` | 0.1381992027318891 | read at execution | read at execution |
| `divheat__p_target_nonrad` [MW] | 55.449100689822046 | 107.00716887159615 | 118.60916196050357 |
| `divheat__q_target_peak` [MW/m²] (pessimistic 9.5 at 50) | **10.53532913106619** | 20.331362085603267 | 22.53574077249568 |
| — the same on the low case (5.0 at 50, a study lever) | 5.544910068982205 | 10.700716887159615 | 11.860916196050358 |
| `divheat__q_target_peak_area_scaled` | 10.53532913106619 | 16.446388438672706 | 16.639762082017157 |
| `divheat__q_target_margin` | -0.5353291310661898 | -10.331362085603267 | -12.535740772495679 |
| `divheat__p_heat_operating_minus_installed` [MW] | -0.920399212073221 | -16.65946471163329 (oracle column) | -8.753791607409084 (oracle column) |
| `vacuum__n_molecules` [/s] | 1.8835037171313755e+22 | 3.8084104397615385e+22 | 4.241567756944368e+22 |
| `vacuum__Q_total` [Pa·m³/s] | 78.0137257066115 | 157.74234195738987 | 175.68348846172455 |
| `vacuum__S_eff_required` [m³/s at 1 Pa] | 78.0137257066115 | 157.74234195738987 | 175.68348846172455 |
| `divertor_heat_ok` | **violated** (low case: satisfied) | violated (low: violated; shadow 16.45: violated) | violated on every reading |

The source case in the oracle's reconstruction: `p_heat_abs` 500, `p_rad_core` 0 → `p_target_nonrad` 50.0, peaks 9.5 / 5.0, doubled 19.0 — exact. The recovery threshold for zero margin: `t_recycle` 0.9961052631578947; `tbr_required` 1.0 and `loss_rate` 0.0 at `t_recycle` 1 for burn fractions 0.01 / 0.05 / 0.2. Absorbed heating at exact satisfaction: 526.3157894736844 MW (pessimistic), 1000.0000000000002 (low).

## MR-WI047 restatement — the comparison meaning at the new pin (2026-09-08, written before regeneration)

(a) **No committed study record changes in meaning.** The nineteen channels this item adds (`fuel__*` 7, `divheat__*` 9, `vacuum__*` 3 — the scratch contract of the final phase-1 text, `scratchpad/gen_probe`, read 2026-09-08) existed in no committed record; no existing column's semantics moves; the ledger reads `sustain__*`, `heat__p_coupled`, `fusion__p_fus` and writes nothing back; the power balance, the calendar, every cost account and every existing verdict operand are untouched. No record is edited.
(b) **One verdict is added, and it reads VIOLATED at the baseline by design.** `divertor_heat_ok` (`'Divertor Target Heat Limit'`, the fixed-geometry pessimistic case scaled in the non-radiated load: 10.535 against 10.0 at the design point, the model's absorbed heating 554.49 MW being 10.9 % above the source's 500) — the disclosed, explained change on the WI-041 precedent, never tuned. "Feasible" gains a third set the study reports beside the ten and beside WI-045's thirteen; every count names its set.
(c) **The count sites this item moves, 13 → 14:** `studies/study_route.py` `EXPECTED_CONSTRAINT_COUNT`; `run_stellaris_single.py` `EXPECTED_VERDICT_COUNT` and `EXPECTED_VERDICTS["divertor_heat_ok"] = "violated"` with the headline no longer `full_satisfaction`; `tests/study/test_operand_bindings.py` (fourteen entries; the feature-ref operand count +1); `test_valid_empty.py` (bounds / `constraints_unreachable` 14); `test_known_answers.py` (`constraints_unreachable` on the no-response axes 14; the fixture contract restated from the report); `test_verify.py` (the constraint set by name +1); `studies/manifest.json` `baseline.verdicts` (fourteen, `divertor_heat_ok` `violated`); `oracle_entry.OPERAND_BINDINGS` (+1, the id read from the regenerated contract). `test_numeric_evidence.py`, `test_subset_flag.py`, `test_output_contract.py`, `test_study_publication_fail_closed.py` and `run_stellaris.py` are checked and restated only if the battery finds them moved (no channel this item adds enters their maps).
(d) **Entry points appearing, none retiring:** the thirteen instance facts (`t_recycle`, `eta_extract`, `lambda_T`, `I_total`, `G_stock`, `m_T_kg`, `f_rad_total`, `q_target_ref`, `p_nonrad_ref`, `q_target_limit`, `R_ref_divertor`, `T_gas`, `p_exhaust`) plus the two library defaults the census counts as entry points (`fuel__s_per_fpy_in`, `vacuum__k_B_in` — design risk 5, confirmed on the scratch contract): +15, so the census is expected 232 → 247; `tbr` keeps its key `stellarator_09__stellaris__tbr` (now declared on the generic plant with a dormant default and redefined by the instance — phase 1 deviation 2).
(e) **The expected baseline:** every one of the 136 existing channels bit-identical; nineteen new channels at the § Predictions doubles; the thirteen existing verdicts unchanged; `divertor_heat_ok` violated. The held mode of the earlier items is unaffected (this item has no dormant term of its own beyond the generic plant's defaults; with the compatibility proposal of WI-045 / WI-046 the nineteen channels read the same values, since they depend on the plasma chain only).

## Spec success criteria, verified (2026-09-08)

- **Functional**: the nineteen channels and the fourteenth verdict exist in the generated package (`generated/contracts/model_contract.json`); `divertor_heat_ok` reads the computed peak; the package regenerates through the pinned codegen and executes at the baseline, P3, P4 and the low case (phase 3).
- **Quality**: Levels 1–3 pass with no new Level 2 warning (the 12 placeholders; Level 6 253, one new design-attribute reference of the pre-existing class); `tests/models` 63 / 13; the restated study tests green in isolation; the full `tests/study` battery is phase 5's run of record on the committed tree.
- **Verification**: the baseline identity and the disclosed verdict (SV-072); the source case reproduced exactly (SV-069); the fuel identities (SV-070); the molecule count (SV-071); every SV `passing`.

## Phase records

### Phase 1 record — 2026-09-08

- The shared files were at WI-046's commit C `1c87c343` (the package on disk sealed `e0d9b1ac19a440ff…`, WI-046's live baseline). The three library files, the constraint def, the plant blocks, the assert and the thirteen instance bindings written from design § Proposed design verbatim (`scratchpad/wi047_phase1_edits.py`, single-occurrence asserts), then four deviations the validator and the exact route forced, each recorded here and none changing a value:
  1. **The `_in` formal convention.** The design's calc formals carried bare names (`in attribute p_fus`, `burn_fraction`, …) and the plant bound `in burn_fraction = burn_fraction;` — Level 2 flagged fourteen self-named bindings, and the codegen projects entry points on the `_in` convention every landed calc uses. Every formal of the three calcs is now `<name>_in` (the bodies renamed with it), and the plant binds `in x_in = x`. The channel names (`fuel__burn_rate`, …) are unchanged.
  2. **`tbr` on the generic plant.** `fuel.tbr_available_in = tbr` could not resolve: `tbr` was declared by the Stellaris instance alone (with its `tbr_ok` fence). The generic plant now declares `attribute tbr : Real default 1.0;` (dormant: no breeding claim) beside the fuel-flow attributes, and the instance redefines it `:>> tbr = 1.074` with its doc; the entry key `stellarator_09__stellaris__tbr` is unchanged (design D3 kept: one number, one entry point).
  3. **The per-reaction energy.** `in E_fus_J_in = fuel_q_eff * mev_to_joules;` read as two undefined bindings on the exact route (design risk 2, the WI-028 class). Rather than the plant-attribute fallback, the calc takes the two factors as formals (`q_eff_in`, `mev_to_joules_in` — exactly `'DT Fuel Cost'`'s formals) and forms `E_fus_J` inside; value-identical.
  4. **A defaulted formal declared between bound ones.** The scratch generation refused with `SI_RENDERING_COLLISION: distinct inputs on 'stellarator_09__stellaris__vacuum' render to one parameter name`; a monkeypatched projection showed the unbound defaulted formal `k_B_in` (declared 4th of 6) taking the name `p_exhaust_in` — the exact route matches an unbound defaulted formal by slot. `k_B_in` is now the last formal, as every landed calc keeps its defaulted formals last; generation then succeeds (`scratchpad/gen_probe`, 91 module wrappers, 76 stencils). A first attempt at this diagnosis — publishing the deuterium exhaust stream as its own fuel output so the vacuum calc's two formals bind two channels — was reverted once the true cause was found: design D1 (two formals on one channel) lands as written. **A codegen finding for the trail:** an unbound defaulted formal declared before a bound one is mis-slotted (candidate for `CODEGEN_FINDINGS.md`).
- Levels 1–3 (`prototype/validate_complete.txt`): Level 1 0 errors (31 files); Level 2 the 12 pre-existing placeholder literals only (undefined 0, self-named 0); Level 3 pass; Levels 4–5 pass; Level 6 252 → **253** (one new design-attribute reference, the same pre-existing class).
- Twins: the six files copied byte-for-byte, `cmp` clean on all six; `diff -rq` shows only the IFE-only files the twin tree never carried.
- `tests/models`: the MFE family's owned list +3 with a dated comment (`tests/model_families.py`, the WI-045 / WI-046 precedent); then **62 passed / 1 failed / 13 skipped**, the one failure the census fingerprint test, re-derived in phase 4 — as at every predecessor's phase 1.

### Phase 2 record — 2026-09-08

- `evidence/baseline_before/`: WI-046's `evidence/baseline_live/` copied (`baseline_result.json` 136 channels / thirteen verdicts / LCOE 224.60952472804465; `package_identity.json` sealed `e0d9b1ac19a440ff…`; the single runner's output) — the package on disk is byte-identical to the one that executed them (WI-046's commit C changed no package byte; `package_contract.json` reads the same fingerprint), the WI-046 phase-2 precedent.
- The restatement and the predictions written above from `proto_results.json` and the scratch contract; commit A carries them, the model edits, the twins, the family restatement and this item's directory.

### Phase 3 record — 2026-09-08

- **Regeneration** (`evidence/regen_output.txt`): `Stencils - New: 3, Preserved: 73, Regenerated: 0` — the three AUTO stencils `mfe_fuel_cycle/fuel_cycle_flows_impl.py`, `mfe_divertor_heat/divertor_heat_ledger_impl.py`, `mfe_vacuum/vacuum_gas_load_impl.py` (bodies as the design's expressions; the ledger's `p_target_nonrad = p_heat_abs - f_rad_total_in * p_heat_abs` verbatim); the constraint module has no stencil; no backup directory; the three manual impls (sustainment, cycle, calendar) byte-identical (`git diff --quiet`); seal clean. **Stale-stencil check** (`evidence/stencil_check.py`, WI-044's): 53 AUTO checked / 4 manual skipped / **0 stale**. A single pass sufficed (no manual stage in this item).
- **The contract**: `divertor_heat_ok` is `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` with its `__evaluation` channel, operands `q_target_peak_in` and `q_target_limit_in`; nineteen channels under `fuel__` (7), `divheat__` (9), `vacuum__` (3); fifteen new entry keys (the thirteen instance facts plus `fuel__s_per_fpy_in` and `vacuum__k_B_in`); semantic fingerprint `42237b2b07673bfd…`, sealed executable `234d0b27d2b5327e…`.
- **The oracle** (`verify_stellaris.py`): `IN` +`tbr` (never needed before; `tbr_ok` binds package inputs) +13 facts +2 library defaults; `compute()` adds the fuel block, the ledger and the gas load after the annual-cost block, written from the design's equations (`p["R"]` for the shadow); the return dict +19; `reconstruct_divertor_source_case()` beside the reference-circuit reconstruction (500 → 50.0, 9.5 / 5.0, 19.0 doubled — exact). **The named shared-line edit (T-006 scope):** in WI-045's loop block, `if loop_p_loop_margin <= 0.0: raise RuntimeError("oracle loop: pressure domain -- ...")` between the margin and the compressor ratio — the sustainment chain's own declared-invalid pattern (a `RuntimeError` the study pre-screen records as a reason); WI-045's expected text stands on either side. **The seam** (`oracle_entry.py`): the entry-key map +17 (`tbr`, `burn_fraction` — neither was a key — the thirteen facts, the two library defaults), the channel map +19, `OPERAND_BINDINGS` +1 with the contract's id. **The single runner**: `EXPECTED_VERDICTS["divertor_heat_ok"] = "violated"` with its comment, `EXPECTED_HEADLINE = "violation"` (WI-041's precedent), `EXPECTED_VERDICT_COUNT` 14, the parity message, the oracle gate +19; **the route**: `EXPECTED_CONSTRAINT_COUNT` 14. First run: verdict parity 14 / `violation`, anchors GREEN (no headline value moved), bit-exact vs oracle PASS on every channel (`evidence/baseline_after/run_stellaris_single_output.txt`).
- **The baseline identity** (`evidence/baseline_after/diff_vs_before.json`): **136 of 136 existing channels bit-identical, 0 moved, 0 gone**; the thirteen existing verdicts unchanged; nineteen channels new at the § Predictions doubles (worst relative deviation **0.0**); the verdict list gains exactly `divertor_heat_ok: violated`; LCOE 224.60952472804465 before and after; sealed executable `e0d9b1ac…` → `234d0b27…`.
- **P3 / P4 / the low case / E / E7** (`evidence/run_phase3_points.py` → `evidence/offdesign_points/result.json`, `summary.json`): P3 `c2823` at fourteen loops — `q_target_peak` 20.331362085603267, shadow 16.446388438672706, `p_sep` 424.68, `f_rad_edge` 0.748, every predicted channel at 0.0 relative, oracle parity 0.0, `divertor_heat_ok` violated (with `loop_capacity_ok` and `recirc_ok`, WI-045's finding); P4 `c3598` — 22.53574077249568, shadow 16.639762082017157, `p_sep` 472.83, likewise violated; the low case at the design point — 5.544910068982205, satisfied; the verdict re-derived through `OPERAND_BINDINGS` (an input-kind binding falling back to the package's own parameter default when the proposal does not set it — `q_target_limit` 10.0) agrees with the package at every completed point. **E (`c3343` at fourteen loops)** `execution_failed` in the package and a raw `TypeError` (complex) in the seam — but the loop margin there is **+2.89 MPa by hand** (`hand_loop_margin_at_E` in `summary.json`: per-loop 887 kg/s, loss 5.11 MPa against 8), so T-005's reading "a complex compressor root" was wrong about the site: the complex value is the CAS10 land term's `sqrt(p_net)` on a negative net power — the pre-existing WI-034 class (`20260829-p-pump-fence#1`), which the study pre-screen already records as "oracle p_net <= 0". **E7 (`c3343` at seven loops, loss 20.45 MPa against 8)** trips the loop's own domain: the package `execution_failed`, the oracle raises the declared `RuntimeError: oracle loop: pressure domain -- …` — the named shared-line edit exercised.
- **The source case** (`evidence/source_case/results.json`): `p_target_nonrad` 50.0, peaks 9.5 / 5.0, doubled 19.0, all `==` exact; the 1.19 identity and the 0.9961052631578947 threshold carried from the prototype.

### Phase 4 record — 2026-09-08

- **Re-pin by the producers** (`scratchpad/wi047_repin.py`; memory `gotcha_repin_after_regeneration`): the snapshot recaptured from the twin tree; `manifest.json` — indicator `e2b0fe3979af1c75…`, executable `234d0b27d2b5327e…`, semantic `42237b2b07673bfd…`, `baseline.verdicts` **fourteen** with `divertor_heat_ok` `violated` (the WI-041 precedent for a pinned violated verdict), `baseline.headline.value` 224.60952472804465 from the executed baseline (unchanged, as predicted — this item moves no number), `m.load()` validated; `mfe_census.json` re-derived: **247** entry points (232 + 13 design attributes + 2 library defaults: library_default 51 → 53, usage_literal 10, design_attribute 171 → 184), exactly the restatement's prediction.
- **The six fixtures** re-derived by `scripts/study/indicators.py`; `EXPECTED_SEMANTIC_FINGERPRINT` and `FIXTURE_CONTRACT` restated **from the report** with a dated comment: every axis reaching `fusion` fires four more modules and taints twenty more channels and reaches `divertor_heat_ok` (R, a: 77 → 81 / 137 → 157; R+tie 82 → 86 / 142 → 162; I_coil 79 → 83 / 132 → 152); `availability_direct` 6 / 18 and `interest_rate` 9 / 22 unchanged with all fourteen unreachable; the objectives lists unchanged.
- **The count sites**, each with a dated comment: `study_route.py` 14; `run_stellaris_single.py` (phase 3); `test_operand_bindings.py` 13 → 14 entries and 22 → 24 feature-ref operands; `test_valid_empty.py` 14 / 14; `test_known_answers.py` 14 and the I_coil reach set +`divertor_heat_ok`; `test_verify.py` +`divertor_heat_ok`; **and one site the plan's list missed:** `test_output_contract.py` counts the manifest's `inputs/` files (7 → 9: `mfe_fuel_cycle_params.json` and `mfe_vacuum_params.json`, the two calc-formal library defaults). `test_known_answers`, `test_operand_bindings`, `test_valid_empty`, `test_output_contract` green in isolation (68 passed); `test_verify` and the rest wait for the committed tree (its git-clean gate refuses the uncommitted package — the WI-046 phase-4 note).
- **Validation**: unchanged from phase 1 (Level 2 the 12 placeholders; Level 6 253). **`tests/models`: 63 passed / 13 skipped** (the census fingerprint test green on the re-derived file).
- **SV-069** (the source case reproduced exactly; oracle parity), **SV-070** (the fuel identities and the threshold), **SV-071** (the molecule count), **SV-072** (the baseline's disclosed verdict; every existing channel identical; P3 / P4 / the low case; the re-derivation) added and `passing`; five trace rows (the three calc defs, the constraint def, the thirteen instance bindings).
- Commit B: the regenerated package, the three new AUTO impls, the oracle (with the named shared-line edit), the seam, the runner, the route, the pin files (snapshot, manifest, census), the six fixtures and the five restated study tests, the two PM matrices, this item's `evidence/` and plan.

### Phase 5 record — 2026-09-08

- **The first run of record** (detached on the committed tree at commit B `d235dde4`) read **87 failed / 423 passed / 1 skipped** in 12:05 — one failure more than the entry count. The failing set differed from WI-046's run of record (`1c87c343`) by exactly one test, and in one direction only: `tests/study/test_mechanical_failures.py::test_the_corrupt_line_carries_file_line_and_key_path` newly failing, nothing newly passing.
- **The delta explained, and restated rather than patched.** That test corrupts the radial-build module's `R_in` line in the generated `pipelines/pipeline.yaml` and asserts the parser's error names the file, the line and the key path. The line number is a literal that moves whenever the regenerated pipeline orders modules differently, and the test's own comment records its history (`:84 -> :87` WI-036; `:87 -> :103` WI-041; `:103 -> :83` WI-044). WI-047's three new modules shift it again. The live package was read before the literal was touched: `grep -n` puts the radial-build `R_in` line at **85** (the first of four such lines; its neighbours are the radial-build thicknesses, and the key path the test asserts is `modules.stellarator_09__stellaris__rb.inputs.R_in`), so the restatement is `:83 -> :85` with the history extended in the comment. `tests/study/test_mechanical_failures.py` then reads 19 passed in isolation.
- **The run of record** (re-run detached on the same package, the test-file restatement in the working tree — the git-clean gate is over the *package* tree, which commit B already carries): **86 failed / 424 passed / 1 skipped** in 12:04, and the failing set is now **identical, test for test, to WI-046's run of record** — the 75 pre-existing fail-closed cases plus the 11 for `20260907-minor-radius`, every one in `test_study_publication_fail_closed.py`, none touching this item's work. Both runs are kept in the evidence file's history through git; the second is the run of record.
- **One battery at a time**, launched with `setsid nohup` and polled with an `until` loop over the evidence file (memory `gotcha_one_battery_at_a_time`, recorded after T-004's contaminated run); `pgrep` used a bracket pattern so it never matched its own shell.
- Commit C: the one test-file restatement, this record, and the run of record.
