---
Status: draft
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

- [ ] Confirm the shared files are at WI-046's commit B (the packet § 9 order); record that commit here
- [ ] Write the three library files and the constraint def verbatim from the design; add the plant blocks and the assert; add the instance bindings with their docs
- [ ] `uv run agentic-mbse validate models` — Level 1 0 errors; Level 2 no new warning beyond the recorded set. **If the exact route refuses `in E_fus_J = fuel_q_eff * mev_to_joules;`** (the WI-028 bare-alias class), bind a plant attribute `fuel_E_fus_J : Real = fuel_q_eff * mev_to_joules;` and read it; record which form landed (design risk 2)
- [ ] Copy the six files to their twins (`cp`); `cmp` clean; `diff -rq` between the trees shows no other difference
- [ ] `uv run python -m pytest tests/models -q` — the count as WI-046 left it or better; any test counting attributes, formals, channels or constraints by literal recorded here and restated in phase 4 from the live package

**Gate.** Levels 1–3; twins identical; `tests/models` as expected with every delta explained.

## Phase 2 — The restatement and the predictions, written before regeneration; `evidence/baseline_before/`; commit A

- [ ] Write `## MR-WI047 restatement` at the end of this plan: (a) no committed study record changes in meaning — the new channels did not exist in any committed record and none of the existing columns' semantics move; (b) one verdict is added and the fourteen-verdict "feasible" is a new set the study reports beside the ten (and beside WI-045's thirteen); (c) the count sites this item moves: `study_route.py` `EXPECTED_CONSTRAINT_COUNT` 13 → 14, `run_stellaris_single.py` `EXPECTED_VERDICT_COUNT` 13 → 14 and `EXPECTED_VERDICTS["divertor_heat_ok"] = "violated"`, `tests/study/test_operand_bindings.py`, `test_valid_empty.py`, `test_known_answers.py`, `studies/manifest.json` `baseline.verdicts`, `oracle_entry.OPERAND_BINDINGS`; (d) the entry points appearing (the thirteen instance facts; `s_per_fpy` and `k_B` if the census counts calc-formal defaults) and none retiring; (e) the expected baseline: every existing channel bit-identical, eighteen new channels at the design's doubles, `divertor_heat_ok` violated
- [ ] Copy design § Expected baseline behaviour and § Off-design predictions into `## Predictions` below with the exact `proto_results.json` doubles (the prediction of record precedes execution in git order)
- [ ] `evidence/baseline_before/`: `study_route.execute_baseline(...)` on WI-046's package → `baseline_result.json`, `package_identity.json` (remove `_work/`); the single runner's output → `run_stellaris_single_output.txt`; record the pin's indicator digest here
- [ ] **Commit A** with an explicit pathspec: the four library files, the plant, the instance, the six twins, `work/active/WI-047_fuel-divertor-vacuum-flows/` (spec, design, plan, `prototype/`, `evidence/baseline_before/`); the message names the restatement as preceding regeneration

**Gate.** The restatement and the predictions are in git before any regenerated byte.

## Phase 3 — Regeneration; the oracle and the seam; the baseline diff; P3 and P4

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `verify_stellaris.py` — ADD the three derivations (D11); `studies/oracle_entry.py` — the thirteen levers, the eighteen channels, one binding; `run_stellaris_single.py` — the verdict and the count; `studies/study_route.py` — the count; `evidence/baseline_after/`, `evidence/offdesign_points/` — NEW.

- [ ] Regenerate:
  ```bash
  /home/reid/1cfe/fusion-tea/.venv/bin/sysml-codegen generate --models exploration/stellarator_e2e/models \
    --output exploration/stellarator_e2e/generated --package-name stellarator_tea \
    --overwrite --smart-regen --preserve-handwritten
  ```
  Expect `New: 4` (three calc modules + the constraint module), `Regenerated` on the plant module only, every handwritten impl preserved byte-identical (WI-045's cycle impl and WI-046's calendar impl included), no `generated/handwritten/backup/`, seal clean. **Any `Regenerated` on a manual-stage calc is a stop** (`gotcha_codegen_manual_stage_regen`)
- [ ] Read `generated/contracts/model_contract.json`: the constraint id `stellarator_09__stellaris__divertor_heat_ok__<hash>` and its evaluation channel; the eighteen channel keys (`fuel__*` 7, `divheat__*` 9, `vacuum__*` 3 — `n_molecules` included); the new entry keys; record all here
- [ ] Read the generated `divertor_heat_ledger.py`: `p_target_nonrad = p_heat_abs - f_rad_total * p_heat_abs` verbatim (D4 — the exact source reproduction depends on the form)
- [ ] `verify_stellaris.py` per D11: `IN` + the thirteen instance doubles; `compute()` + the fuel block, the ledger, the gas load, written from the design's equations; the return dict + eighteen
- [ ] `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` + thirteen; `ORACLE_OUTPUT_TO_CHANNEL` + eighteen; `OPERAND_BINDINGS` + one entry for the read constraint id (`q_target_peak_in` ← the `divheat__q_target_peak` channel key; `q_target_limit_in` ← the `q_target_limit` input key)
- [ ] `run_stellaris_single.py`: `EXPECTED_VERDICTS["divertor_heat_ok"] = "violated"` with the comment (10.535 against 10 on the pessimistic case by the model's 10.9 % absorbed-heating excess; disclosed, never tuned; the low case reads 5.545); `EXPECTED_VERDICT_COUNT = 14`; the parity message restated (thirteen satisfied, one violated — not `full_satisfaction`); the oracle gate's channel list + the eighteen
- [ ] `study_route.py`: `EXPECTED_CONSTRAINT_COUNT = 14` with a dated comment
- [ ] Execute the single runner → `evidence/baseline_after/run_stellaris_single_output.txt`; verdict parity 14; the oracle gate passes on every new channel (rel 1e-9)
- [ ] `study_route.execute_baseline(evidence/baseline_after)`; diff `baseline_result.json` before/after: **every existing channel bit-identical; eighteen new channels at the predicted doubles; the verdict list gains exactly `divertor_heat_ok: violated`; nothing else** — record the diff here
- [ ] **If any existing channel moves, stop and derive why before continuing** (`goal.md` § Invariants)
- [ ] Execute P3 (`c2823`: R 15.7, a 2.2, 13 MA, 13 keV, n 5.06e20, 100 MW) and P4 (`c3598`: R 17.2, a 2.2, 14 MA, 13 keV, 100 MW) through `study_route.run_points` with proposals in the `20260907-minor-radius/study.py` `point()` shape and `required_channels` covering the eighteen; deposit `evidence/offdesign_points/results.json`; compare `divheat__q_target_peak` (20.331362085603267 / 22.535740772495682), `q_target_peak_area_scaled` (16.446388438672706 / 16.639…), `fuel__*` and `vacuum__*` to `## Predictions` at 1e-9 relative; read `p_sep` and `f_rad_edge` (unpredicted — no `p_rad` in the committed CSV) and check `p_sep > 0`; the oracle seam's `evaluate()` at both points → 0.0 relative deviation on all eighteen; `divertor_heat_ok` re-derived through the binding agrees (violated at both)
- [ ] The oracle's source-case check: with `p_heat_abs` 500 and `p_rad_core` 0 the oracle's ledger reads `p_target_nonrad` 50.0 and peaks 9.5 / 5.0 exactly; doubled 19.0 — deposit under `evidence/source_case/`

**Gate.** The baseline identity holds; the one verdict change is the predicted one; the predictions hold; the oracle agrees.

## Phase 4 — Re-pin, fixtures, batteries, SV and trace rows; commit B

**Files.** `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, `tests/study/data/*.expected.json`, `tests/study/test_known_answers.py`, `test_operand_bindings.py`, `test_valid_empty.py` — RE-DERIVE / RESTATE; `modeling_project/VALIDATION_MATRIX.md`, `data/traceability_matrix.csv` — via `pm` ops.

- [ ] Snapshot recaptured from the twin tree
- [ ] `manifest.json`: the three fingerprints from the package's contracts (`files` as path strings); `baseline.verdicts` gains `{"source_local_identity": "divertor_heat_ok", "expected": "violated"}` (fourteen entries); `baseline.headline.value` re-pinned from the executed LCOE (expected unchanged from WI-046's pin — this item moves no number); `m.load(manifest)` validates
- [ ] `mfe_census.json` re-derived (`integ.rederived_census(pkg)` + the new semantic fingerprint); expect WI-046's count + 13 (or + 15 with the two calc-formal defaults) — record the actual count and delta
- [ ] The six fixtures re-derived via `scripts/study/indicators.py --package … --manifest … --groups tests/study/data/axes.known_answers.json`; `EXPECTED_SEMANTIC_FINGERPRINT` and `FIXTURE_CONTRACT` restated **from the report** (predicted: every axis reaching `p_fus` — R, R+tie, a, I_coil — gains the three modules and their channels, and `divertor_heat_ok` becomes reachable on them; `availability` / `availability_direct` and `interest_rate` unchanged) with a dated comment
- [ ] The literal count sites restated from the live package with a WI-047 comment: `tests/study/test_operand_bindings.py` (fourteen), `test_valid_empty.py` (bounds / `constraints_unreachable`), `test_known_answers.py` (`constraints_unreachable` on the axes that reach none)
- [ ] `uv run agentic-mbse validate models --complete` — compare with WI-046's run; record any new residue
- [ ] `tests/models` — every delta explained
- [ ] `rm -rf .integration_workspace`; `tests/study` — expect green apart from the branch's known fail-closed cases; every other delta explained
- [ ] `pm add-validation` ×4 then `pm update-validation … --status passing` with the evidence paths: (1) the source case reproduced exactly (500 → 50; 9.5 / 5.0; 19.0 doubled; oracle and package); (2) the fuel identities (1.19 at 0.99; loss 0 and `tbr_required` 1.0 at `t_recycle` 1 for three burn fractions; the 0.9961052631578947 threshold); (3) the molecule count (atoms / molecules 1.95 at the design point; doubling every rate doubles `S_eff_required`); (4) the baseline's disclosed verdict (every existing channel bit-identical; eighteen new channels at the predictions; `divertor_heat_ok` violated at 10.535329131066188; oracle parity 0.0; P3 / P4 as predicted)
- [ ] `pm trace-element` for `'Fuel Cycle Flows'`, `'Divertor Heat Ledger'`, `'Vacuum Gas Load'`, `'Divertor Target Heat Limit'` and the thirteen instance facts
- [ ] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified — below)
- [ ] **Commit B** with an explicit pathspec: the regenerated package, the oracle, the seam, the single runner, the route, the pin files, the fixtures and the three test files, the SV/trace rows, `evidence/baseline_after/`, `evidence/offdesign_points/`, `evidence/source_case/`, this plan; never `git add -A`
- [ ] Note for the modelling PM: the BACKLOG row moves at close through `pm close-item`

**Gate.** Both batteries as expected with every delta explained; no expectation patched to match; the four SV rows `passing`.

## Phase 5 — The `tests/study` run of record; commit C

- [ ] After commit B, `tests/study` on the clean tree (detached if longer than ten minutes); record the count and the failing set; confirm it equals the pre-existing fail-closed set or explain every difference
- [ ] **Commit C**: any test-file restatement the run forced, and this plan's phase-5 record

---

## Feasibility concerns

1. **The codegen refuses the product on a calc input** (`E_fus_J = fuel_q_eff * mev_to_joules`). *Mitigation:* the plant-attribute fallback (phase 1); either form is value-identical.
2. **`p_sep ≤ 0` somewhere in the sweep** makes `f_rad_edge` nonfinite. *Mitigation:* the exporter's nonfinite refusal and the in-range channel; the study declares such points; no clamp (design risk 3).
3. **The census counts the two calc-formal defaults.** *Mitigation:* the actual delta is recorded, whichever it is.
4. **A count site beyond the seven named** (the WI-043 evidence found eight literal verdict-count sites). *Mitigation:* the batteries find it; each restated from the live package with a comment.

## Predictions — (to be copied from `prototype/proto_results.json` at phase 2, before regeneration)

## MR-WI047 restatement — (to be written at phase 2, before regeneration)

## Spec success criteria, verified — (to be written at phase 4)

## Phase records — (appended per phase)
