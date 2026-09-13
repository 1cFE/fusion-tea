---
Status: active
Created: 2026-09-08
Updated: 2026-09-08
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-045 Plan — the primary coolant loop and the temperature-compatible cycle

Five phases, the WI-044 shape: the model edits, twins and validation; the restatement, the predictions and the pre-change baseline, commit A; regeneration (twice, the new stencil restored between), the oracle and the seam, the held-mode identity, the live baseline, the off-design points; the re-pin by producers, the count sites, batteries, SV and trace rows, commit B; the `tests/study` run of record, commit C. This item integrates **first** of the round's three (packet § 9); WI-046's plan starts from commit C's tree.

## Source documents

- `spec.md` MR-WI045-1..18; `design.md` D1–D15, § Proposed design (the exact text), § Expected baseline behaviour, § Off-design predictions, § Validation plan.
- `work/orchestration/goals/plant-closure/evidence/round1_basis_packet.md` §§ 3, 4, 9 and its Amendment.
- Recipes: memory `gotcha_codegen_manual_stage_regen` (this item ADDS a manual stage: the stencil appears, is restored, and the package is regenerated again), `gotcha_repin_after_regeneration` (snapshot → manifest → census → fixtures → single runner; the verdict-addition note: five count sites, +1 module and +1 tainted channel on every axis that reaches each operand), `gotcha_syside_env_not_exported`, `gotcha_commit_with_pathspec`.
- Precedents: `work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/plan.md` (phases 3–5, the stale-stencil finding and its checker `evidence/stencil_check.py`), `work/completed/20260907_WI-043_two-sided-sustainment-condition/plan.md` phases 4–5 (a verdict addition: the regeneration command, the contract read, the seam binding, the count sites).

## Design summary

Three new calcs (`'Reactor Source Heat'`, `'Primary Coolant Loop'`, `'Power Cycle Efficiency'` — the last handwritten), the power balance's two formals replaced at the same positions, three verdicts, five flags/directs with dormant defaults and eighteen instance-bound facts; the dormant mode reproduces the entering pin bit-for-bit; the live design point reads 175.44 MW of loop draw, 0.41136 efficiency and LCOE 237.2528 at held availability.

## Prototype baseline

`prototype/proto.py` → `proto_results.json` (design § Validation report): the reference reconstruction closes at `eta_is` 0.772796639536644; the held-mode identity checks all `True`; the live design point and P1 / P3 / P4 predicted. No model file touched; nothing regenerated.

## Environment

`uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python …` for validation, `tests/models`, the seam and the route; `PYTHONPATH=$HOME/1cfe/teax/packages/teax-simkit:$PWD/exploration/stellarator_e2e/pkg` for the single runner and the route; `PYTHONPATH` unset for `tests/study`. Always `uv run`. Commit with an explicit pathspec; never `git add -A` (the owner's staged files).

## Validation strategy

Levels 1–3 after every model edit; the held-mode identity before anything else after regeneration; the live baseline against the predictions; the off-design points with oracle parity and verdict re-derivation; the batteries after the re-pin; `tests/study` after the commit (its git-clean gate).

---

## Phase 1 — The model edits; Levels 1–3; twins synced; `tests/models`

**Files.** `models/library/analyses/mfe_power_balance.sysml` (the source-heat calc; the two formals; the two sums), `mfe_primary_loop.sysml` (NEW), `mfe_power_cycle.sysml` (NEW), `mfe_viability.sysml` (three constraint defs), `models/designs/generic_mfe/mfe_plant.sysml` (imports; the attribute block replacing 413–421; the three usages; the `pb` lines; the three asserts), `models/designs/stellarator_09/stellarator_plant.sysml` (the block replacing 779–808; the turbine comment; the disclosure block); their six twins under `exploration/stellarator_e2e/models/` — COPY byte-for-byte.

- [x] Write the four library files and the two design files from design § Proposed design verbatim; re-read each against the design (formals, expressions, the dormancy defaults, every `Source`/`Ref`/`Basis`)
- [x] `uv run agentic-mbse validate models` — Level 1 0 errors; Level 2 the 12 pre-existing warnings only; Level 3 pass. **If Level 3 rejects `r_comp ** k_isen` or the chained outputs, stop:** that is the design's risk 4, a form question, not a number
- [x] `uv run agentic-mbse validate models --complete` → `prototype/validate_complete.txt`; Level 6 residue: expect the WI-044 residue plus 23 design attrs (207 → 230); record the actual
- [x] Copy each of the six files to its twin (`cp`); `cmp` clean on all six; `diff -rq` between the two trees shows no other difference
- [x] `uv run python -m pytest tests/models -q` — expect 47 / 1 / 13 with the one failure the census fingerprint test (re-derived in phase 4), as at WI-044 phase 1; any other delta explained here

**Gate.** Levels 1–3; twins identical; `tests/models` as expected with every delta explained.

## Phase 2 — The restatement and the predictions, written before regeneration; `evidence/baseline_before/`; commit A

- [x] Write `## MR-WI045-16 restatement` at the end of this plan (the section below, filled): (a) the committed columns keep their meaning; (b) live differs everywhere, held equals bit-for-bit; (c) three verdicts, the count sites; (d) the entry-point delta; (e) DI-007 scoped
- [x] Copy design § Expected baseline behaviour (both modes) and § Off-design predictions into `## Predictions` below with the exact `proto_results.json` values (the prediction of record precedes execution in git order)
- [x] `evidence/baseline_before/`: `study_route.execute_baseline(...)` on the unchanged package → `baseline_result.json`, `package_identity.json` (remove `_work/`); the single runner's output → `run_stellaris_single_output.txt`; confirm `package_identity.json` carries the WI-044 pin (indicator `30abb21be6d7…`, executable `7d295fec2c78…`) and 106 channels, ten verdicts, LCOE 322.31843948570247
- [x] **Commit A** with an explicit pathspec: the four library files, the two design files, the six twins, `work/active/WI-045_primary-loop-and-cycle/` (spec, design, plan, `prototype/`, `evidence/baseline_before/`); message names the restatement as preceding regeneration

**Gate.** The restatement and the predictions are in git before any regenerated byte.

## Phase 3 — Regeneration (twice); the stale-stencil check; the oracle and the seam; the held-mode identity; the live baseline; P1 / P3 / P4; the synthetic cases

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `generated/handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py` — NEW (the design's body restored over the stencil); `verify_stellaris.py` — REWRITE per D12; `studies/oracle_entry.py` — the keys, channels and three bindings per D12; `run_stellaris_single.py` — `EXPECTED_VERDICTS` +3, `EXPECTED_VERDICT_COUNT` 13, the `p_th` / `recirc` comments; `evidence/baseline_after/`, `evidence/compat_mode/`, `evidence/offdesign_points/`, `evidence/synthetic_cases/` — NEW.

- [x] Regenerate, pass 1:
  ```bash
  /home/reid/1cfe/fusion-tea/.venv/bin/sysml-codegen generate --models exploration/stellarator_e2e/models \
    --output exploration/stellarator_e2e/generated --package-name stellarator_tea \
    --overwrite --smart-regen --preserve-handwritten
  ```
  Expect `New: 4` (the source-heat, loop and cycle modules and the cycle's handwritten STENCIL, a `NotImplementedError` body), `Regenerated` on the power balance and the plant modules (their interfaces changed), every existing handwritten impl preserved byte-identical; record the counts → `evidence/regen_output.txt`. **Any `Regenerated` on an existing manual-stage calc is a stop** (`gotcha_codegen_manual_stage_regen`); a `backup/` dir created for an AUTO module whose output set grew is the WI-044 phase-3 case — remove it before pass 2
- [x] Read the stencil `generated/handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py`: the `inputs.<field>` names and the generated caller's unpack order in `generated/modules/mfe_power_cycle/power_cycle_efficiency.py`; restore the design's normative body over the stencil with the return tuple in the caller's order (D13); record the order here
- [x] `rm -rf exploration/stellarator_e2e/generated/handwritten/backup/` if present; regenerate, pass 2 → `evidence/regen_output_2.txt`: expect `New: 0, Regenerated: 0`, the cycle impl preserved byte-identical (`cmp` against the restored body), no `backup/`, seal clean
- [x] Run the WI-044 stale-stencil checker (`work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/evidence/stencil_check.py`, copied to `evidence/`) over every AUTO stencil → `evidence/stencil_check_output.txt`: expect 0 stale; the power balance's regenerated body carries `q_recovered_in` and `p_pump_total_in` at the old positions (read it: `p_th = ((mn_in * p_neutron) + p_alpha) + p_input_in) + q_recovered_in` in the emitted order, `recirculating` with `p_pump_total_in` second) — **if a stale stencil survives, delete it and regenerate a third time, as WI-044 did; never patch a stencil by hand**
- [x] Read `generated/contracts/model_contract.json`: the three new constraint ids (`stellarator_09__stellaris__loop_pressure_ok__<hash>`, `…loop_capacity_ok__<hash>`, `…cycle_domain_ok__<hash>`), their operand names as the predicate IR spells them, the twenty new channel keys and the 23 new entry keys; record them here
- [x] `verify_stellaris.py` per D12: `IN` −3 +23; `compute()` the source heat, the loop chain, the cycle chain, the two sums with the new operands; the return dict +20; a `reconstruct_reference_circuit()` function beside `compute()` for MR-WI045-13. Written from the design's equations, not from the generated modules
- [x] `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` −`eta_th` +23 (comment marks the D7 levers); `ORACLE_OUTPUT_TO_CHANNEL` +20; `OPERAND_BINDINGS` +3 with the ids from the contract (`mdot_loop_rated_in` as `{"kind": "input", "key": f"{P}mdot_loop_ref"}`)
- [x] `run_stellaris_single.py`: `EXPECTED_VERDICTS` gains `loop_pressure_ok`, `loop_capacity_ok`, `cycle_domain_ok` = `satisfied` with dated comments (the sizing rule; the domain); `EXPECTED_VERDICT_COUNT = 13`; the nine-anchor block's expected LCOE re-stated to the live prediction 237.25280024209582 **after** the oracle gate reads bit-exact (never before); the parity message "thirteen satisfied (WI-045: three fences added; the design point moved as predicted)"
- [x] **The held-mode identity first** (MR-WI045-10): through `study_route.run_points` one proposal at the baseline levers with `loop_live 0.0, cycle_live 0.0, p_pump_direct 195.0, eta_p_direct 0.5, eta_th_direct 0.333` (the compatibility proposal; `required_channels` the route's `CHANNELS` plus the twenty new keys); deposit `evidence/compat_mode/result.json`; diff every channel of the entering pin's `baseline_result.json` (106) against it: **every one bit-identical, the old ten verdicts unchanged, LCOE 322.31843948570247**; the three new verdicts satisfied; record the diff here (`evidence/compat_mode/diff_vs_pin.json`)
- [x] **If any existing channel moves in held mode, stop and derive why before continuing** (`goal.md` § Invariants; the packet § 3 rule)
- [x] The live baseline: the single runner → `evidence/baseline_after/run_stellaris_single_output.txt` (13 / `full_satisfaction`; the oracle gate bit-exact on every channel including the twenty new ones); `study_route.execute_baseline(evidence/baseline_after)`; diff against `## Predictions` (live): every listed channel to 1e-9 relative; `p_fus`, `wall_load_peak`, `B_peak`, `beta`, `p_aux_required` bit-identical to the pin → `evidence/baseline_after/diff_vs_predictions.json`
- [x] Execute P1, P3, P4 through `run_points` (proposals in the committed record's `point()` shape; P3 and P4 differ only in `n_loops`); deposit `evidence/offdesign_points/results.json`; compare the loop and cycle channels to `## Predictions` (1e-9 relative); the oracle seam's `evaluate()` at the three points → 0.0 relative deviation on every new channel and on `lcoe`; the three new verdicts and `recirc_ok` re-derived through `OPERAND_BINDINGS` agree with the package (P1 capacity violated; P3 capacity and recirc violated; P4 all satisfied)
- [x] The synthetic cases through `run_points` and the oracle → `evidence/synthetic_cases/results.json`: `loop_T_in` 623.15 − 200 (so `T_hot` 623.15 K, the Stellaris local 350 °C) reads `cycle_domain_ok` violated with `cycle__eta_fit` 0.3713254788502389 published; `n_loops` 7 reads `loop_capacity_ok` violated with `loop__p_elec` 717.7666412961582; no clamp anywhere

**Gate.** The held-mode identity holds; the live predictions hold; the oracle agrees; the fences re-derive.

## Phase 4 — Re-pin, fixtures, the count sites, batteries, SV and trace rows; commit B

**Files.** `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, `tests/study/data/*.expected.json`, `tests/study/test_known_answers.py`, `tests/study/test_operand_bindings.py`, `tests/study/test_valid_empty.py`, `studies/study_route.py:49` — RE-DERIVE / RESTATE; `modeling_project/VALIDATION_MATRIX.md`, `data/traceability_matrix.csv` — via `pm` ops.

- [x] Snapshot recaptured from the twin tree (`capture_instance_graph_snapshot([Path("exploration/stellarator_e2e/models")], …)`)
- [x] `manifest.json`: the three fingerprints from the package's contracts (`files` as path strings); `baseline.verdicts` gains the three (`{"source_local_identity": "loop_pressure_ok", "expected": "satisfied"}`, …) = thirteen; `baseline.headline.value` re-pinned from the executed live LCOE (expected 237.25280024209582 — **a moved headline by design, the first since the pin discipline began; the restatement below says so**); `m.load(manifest)` validates; the `availability` axis untouched (WI-046's)
- [x] `mfe_census.json` re-derived (`integ.rederived_census(pkg)` + the new semantic fingerprint); expect **229** (−`eta_th`, `eta_p`, `p_pump`; +23) — record the actual count and delta
- [x] The six fixtures re-derived via `scripts/study/indicators.py --package … --manifest … --groups tests/study/data/axes.known_answers.json`; `EXPECTED_SEMANTIC_FINGERPRINT` and `FIXTURE_CONTRACT` restated **from the report** (predicted: the three new modules fired on every axis that reaches `fusion` or `heat` — R, R+tie, a, I_coil — and the three new constraints reachable there; `availability` and `interest_rate` gain the cycle and loop modules only if the trace reaches them, which it should not) with a dated comment saying what moved and why
- [x] The count sites restated from the live package, each with a WI-045 comment: `study_route.py:49` `EXPECTED_CONSTRAINT_COUNT = 13`; `run_stellaris_single.py` (done in phase 3); `tests/study/test_operand_bindings.py` (ten → thirteen); `tests/study/test_valid_empty.py` (bounds / `constraints_unreachable`); `tests/study/test_known_answers.py` (`constraints_unreachable` on the no-response axes). These are counts of the constraint set, read from the report and the contract, never fitted
- [x] `uv run agentic-mbse validate models --complete` → `evidence/validate_complete_after.txt`; compare with `prototype/validate_complete.txt`; record any new residue
- [x] `tests/models` — expect 48 / 13 or better; every delta explained
- [x] `rm -rf .integration_workspace`; `tests/study` — expect green apart from the branch's known fail-closed cases (86 at entry: the 75 + 11 for `20260907-minor-radius`); every other delta explained. **Expected known movers** (the WI-044 phase-5 precedent): the `pipeline.yaml` line number in `test_mechanical_failures.py` (module order changes with three new modules); the reach test in `test_known_answers.py` if a geometry axis's reach changed; each verified against the live pipeline before restating
- [x] `pm add-validation` ×3 then `pm update-validation … --status passing` with the evidence paths: **SV-063** the held-mode identity (every channel of the entering pin bit-identical under the compatibility proposal; the old ten verdicts; LCOE 322.31843948570247; `evidence/compat_mode/`); **SV-064** the reference-circuit reconstruction (2101.7 MW at 2025.7 kg/s over 200 K, `cp` 5187.6 implied against 5193 bound; 363.9 / 315.7 / 329.187 kPa; 2231.1 MW; 129.4 against 130.8 printed; `w_fluid` 129.4 at `eta_is` 0.772796639536644 to 1e-12 — a reconstruction, not validation); **SV-065** the live baseline and P1 / P3 / P4 at the predictions with oracle parity 0.0, the three new verdicts and `recirc_ok` re-derived, the synthetic fail-closed cases
- [x] `pm trace-element` for `'Reactor Source Heat'`, `'Primary Coolant Loop'`, `'Power Cycle Efficiency'`, the three constraint defs, and the eighteen instance-bound facts (one row each, or grouped as the tool allows)
- [x] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified — below)
- [x] **Commit B** with an explicit pathspec: the regenerated package, the handwritten impl, the oracle, the seam, the single runner, the pin files, the fixtures and the four test files, `study_route.py`, the SV/trace rows, `evidence/baseline_after/`, `evidence/compat_mode/`, `evidence/offdesign_points/`, `evidence/synthetic_cases/`, `evidence/regen_output*.txt`, `evidence/stencil_check*`, `evidence/validate_complete_after.txt`, this plan; never `git add -A`
- [x] Note for the modelling PM: the BACKLOG row moves at close through `pm close-item`; the round's trail records the landing

**Gate.** Both batteries as expected with every delta explained; no expectation patched to match; SV-063..065 `passing`.

## Phase 5 — The `tests/study` run of record; commit C

- [x] After commit B, `tests/study` on the clean tree (detached, `setsid nohup`, ~11 min); record the count and the failing set; confirm the failing set equals the pre-existing fail-closed set (86) or explain every difference
- [x] **Commit C**: any test-file restatement the run forced, and this plan's phase-5 record
- [x] Hand the tree to WI-046's plan (packet § 9); its `evidence/baseline_before/` is this item's `evidence/baseline_after/`

---

## Feasibility concerns

1. **Codegen reports a dependency cycle despite D3.** *Mitigation:* the module graph is read from `pipeline.yaml` after pass 1; a cycle is a `PREREQUISITE` return naming codegen, not a re-wiring.
2. **The cycle stencil's caller unpacks in an order other than the declaration's.** *Mitigation:* the order is read from the caller and the return reordered (D13); the second regeneration proves preservation.
3. **The power balance's AUTO stencil is preserved stale on the changed expression.** *Mitigation:* the WI-044 checker after every pass; a stale stencil is deleted and the package regenerated, never edited.
4. **The `required_channels` map for the compatibility proposal.** The route's `CHANNELS` may not include the twenty new keys; the proposal passes its own map (the route accepts one). A refusal is recorded and fixed in the map, never by dropping a channel.
5. **`tests/study` carries 86 red fail-closed cases at entry.** *Mitigation:* the run of record lists the set and shows it equals the entry set or explains each difference.
6. **The manifest headline moves.** By design (the live baseline is the pin's baseline after this item); preflight's `baseline_headline` gate reads the re-pinned value; the compatibility arm, not the manifest, is the bridge to the entering pin.

---

## MR-WI045-16 restatement — the comparison meaning at the new pin (2026-09-08, written before regeneration)

**Ordering.** Committed with the model edits (commit A) and before any regenerated byte (commit B).

### (a) The committed columns keep their meaning, and are never edited

Every committed record carries `p_th`, `p_et`, `p_net`, `rec_frac`, `q_eng`, `lcoe`, `lcoe_1cfe`, `cas72`, `total_capital` computed by the held chain: `p_th = mn·p_n + p_α + p_coupled + 0.5 × 195`, `p_the = 0.333 × p_th`, `recirculating = … + 195 + …` at every point. Those columns mean exactly that and stand at their own pins; no file under `exploration/stellarator_e2e/studies/2026*/` changes.

### (b) Live differs everywhere; held equals bit-for-bit

At the new pin in live mode the same channel names carry the loop and the cycle: `p_th` gains the loop's fluid work (175.44 MW at the design point) in place of the 97.5 MW credit; `p_the` is 0.41136 × `p_th` in place of 0.333 ×; `recirculating` carries the loop's draw (cubic in the per-loop flow at a held count) in place of 195. They differ from the committed values at every point. In held mode — the compatibility proposal `loop_live 0, cycle_live 0, p_pump_direct 195.0, eta_p_direct 0.5, eta_th_direct 0.333` — the same package reproduces the committed values bit-for-bit, because the dormant contributions are formed as `0.0·x + held` at the same operation positions (design D9; `prototype/proto_results.json` `held_mode_identity`). The round's study proves the second by case id on a sample of the committed window; a committed column cannot be re-read at the live chain by a multiplier (the loop's draw depends on `q_source` cubically through the per-loop flow and on `n_loops` quadratically), so the study re-executes.

### (c) Three verdicts are added; the count sites move 10 → 13

`loop_pressure_ok`, `loop_capacity_ok`, `cycle_domain_ok` join the ten. `manifest.json` `baseline.verdicts` = 13; `EXPECTED_VERDICT_COUNT`, `EXPECTED_CONSTRAINT_COUNT` and the three test literals move to 13, each with a dated comment. WI-047 moves them to 14; WI-046 adds none. "Feasible" in the round's study names its set (the old ten or the fourteen) at every count. At the design point in live mode the ten existing verdicts are unchanged (`net_positive` and `recirc_ok` gain margin) and the three new ones are satisfied; off the design point `loop_capacity_ok` catches almost every committed point at the instance's 14 loops (design D6), and at `c2823` the loop's draw breaks `recirc_ok` — the committed verdict columns are not wrong, they are the held chain's.

### (d) The entry-point delta

`eta_th`, `eta_p`, `p_pump` retire as direct instance scalars; `loop_live`, `cycle_live`, `p_pump_direct`, `eta_p_direct`, `eta_th_direct`, `loop_T_in`, `loop_dT_blanket`, `loop_cp`, `loop_gamma`, `loop_p`, `n_loops`, `mdot_loop_ref`, `dp_loop_ref`, `f_loss`, `eta_is`, `eta_drive`, `dT_approach`, `a_fit`, `b_fit`, `T_offset_fit`, `T2_min`, `T2_max`, `delta_eta` appear (23). Census 209 → 229 predicted (phase 4 records the actual). Twenty channels appear (`source_heat__q_source`; thirteen `loop__*`; six `cycle__*`). No committed study holds a retired key as an axis key except `eta_th` through the seam's lever in `20260821-power-cycle-ab` (a preset comparison at its own pin; its record stands, and the seam's map retires the key — a proposal naming `eta_th` is refused, which is the intended fail-closed behaviour for a retired entry point).

### (e) DI-007 is scoped, not amended

DI-007's "power-cycle choice does not reach primary-coolant pumping power" describes the three-field preset model correctly at its own pin. After this item the cycle reads the loop's outlet, so a cycle arm and a loop arm share the primary circuit only when their boundary conditions (`T_out`, the approach) are equal; the sCO2 arm on the same heat satisfies that by construction. No DI is edited by this item; the research's DI candidate 2 is the round's to file.

## Predictions — the design point in both modes and P1 / P3 / P4 (2026-09-08, `prototype/proto_results.json`, written before regeneration)

Copied from design § Expected baseline behaviour and § Off-design predictions; the exact doubles are the JSON's.

| Point | Mode / levers | `loop__p_elec` | `loop__q_recovered_total` | `loop__p_pump_total` | `cycle__eta_th` | `pb__p_th` | `pb__p_net` | `pb__rec_frac` | `lcoe_calc__lcoe` | New verdicts |
|---|---|---|---|---|---|---|---|---|---|---|
| P0 held | compatibility proposal | 175.4365426878376 | `97.5` | `195.0` | `0.333` | `3224.352676294579` | `716.633806369912` | `0.3325626292668907` | `322.31843948570247` | all satisfied |
| P0 live | the instance | 175.4365426878376 | 175.4365426878376 | 175.4365426878376 | 0.41135655404954075 | 3302.2892189824165 | 1012.3648698998519 | 0.2547473338899163 | 237.25280024209582 | all satisfied |
| P1 | R 12.7, a 1.4, 15.4 MA, 100 MW; 14 loops | 209.66570510819685 | 209.66570510819685 | 209.66570510819685 | 0.41135655404954075 | 3526.933258907216 | 1067.7722416861886 | 0.26402516671983356 | 231.32525675570017 | capacity VIOLATED |
| P3 | `c2823`; 14 loops | 1447.9729180478694 | 1447.9729180478694 | 1447.9729180478694 | 0.41135655404954075 | 7719.313363213116 | 1502.2763876461277 | 0.5269002172397199 | 250.52954946775412 | capacity VIOLATED; `recirc_ok` VIOLATED |
| P4 | `c2823`; 27 loops | 380.7670505420672 | 380.7670505420672 | 380.7670505420672 | 0.41135655404954075 | 6652.107495707313 | 2143.6501908768514 | 0.21661322229463523 | 171.23178310298275 | all satisfied |

Every existing channel at P0 held is the entering pin's exactly; at P1 / P3 / P4 the plasma, wall and magnet channels are the pin's at the same coordinates.

## Spec success criteria, verified (2026-09-08, phase 4)

- **Functional.** The three calcs and the twenty channels exist in the generated package (`generated/contracts/model_contract.json`: `source_heat__q_source`, thirteen `primary_loop__*`, six `cycle__*`; 23 new entry keys); the power balance reads `q_recovered_in` and `p_pump_total_in` at the old positions (the regenerated stencil, phase 3); `eta_th_in` arrives from the cycle; the three asserts exist with ids `loop_pressure_ok__5905ab54f5e8a945`, `loop_capacity_ok__d77f6027ceb27852`, `cycle_domain_ok__ba3fa9c3653b3fd3`; the package regenerates through the pinned codegen twice (`evidence/regen_output.txt`, `regen_output_2.txt`) and executes at the baseline, at P1 / P3 / P4 and at the two synthetic cases.
- **Quality.** Levels 1, 3, 4, 5 pass; Level 2 the 12 pre-existing placeholder warnings; Level 6 248 issues (236 before the item; the same five printed sites shifted; `evidence/validate_complete_after.txt`); `tests/models` 48 / 13 after the re-pin (phase 4); the affected `tests/study` files green (the run of record is phase 5).
- **Verification.** SV-063 (held-mode identity), SV-064 (the reference reconstruction), SV-065 (the live baseline, P1 / P3 / P4, the synthetic cases, oracle parity and verdict re-derivation) `passing`; trace rows for the three calcs, the three constraint defs and the three groups of instance facts (`data/traceability_matrix.csv`).
- **Requirements not covered by an SV, checked by reading.** MR-WI045-14 (the disclosures a–g) in the instance's WI-045 block and the two calc docs; MR-WI045-15 (Kovari 2016 registered at T-002, cited by the registered path and the render); MR-WI045-16 (the restatement above, in commit A before any regenerated byte); MR-WI045-17 (`git diff` of commit A confined to the six model files, their twins and two test restatements; commit B to the regenerated package, the oracle, the seam, the runner, the pin files, the fixtures and the PM matrices — the CAS72 chain, `availability` and the fuel / divertor / vacuum quantities untouched); MR-WI045-12 (census 209 → 229: −`eta_th`, `eta_p`, `p_pump`; +23).

## Phase records

*(appended as each phase completes)*

### Phase 1 record — 2026-09-08

- The six model files written from design § Proposed design verbatim (`scratchpad/wi045_phase1_edits.py`, string-replacement with single-occurrence asserts). **One deviation forced by the parser:** `loop` is a SysML keyword (the `loop` action), so Level 1 refused `calc loop : 'Primary Coolant Loop'` and every `loop.<output>` reference; the usage is named **`primary_loop`** and the channels the study will see are `primary_loop__*` (not the packet's / design's `loop__*`). The plant attributes `loop_live`, `loop_T_in`, … are ordinary identifiers and unaffected. Recorded for the packet's next amendment and the oracle seam's channel map (phase 3).
- Levels 1–3: Level 1 0 errors (27 files); Level 2 the 12 pre-existing placeholder warnings (`prototype/validate_complete.txt` line 31, the same as before the change); Level 3 pass; Levels 4–5 pass; Level 6 236 → **248** issues (the five printed sites are the same expressions shifted by line numbers; the delta is the new design-attribute references — the design predicted 23 design attrs, the tool counts 12 more issues). No new residue class.
- Twins: the six files copied byte-for-byte, `cmp` clean; `diff -rq` between the trees shows only the IFE-only files the twin tree never carried.
- `tests/models`: first run 4 failed / 6 errors — `test_owned_paths_cover_every_canonical_file` (the two new library files were not in the MFE family's owned list) and the interface test `test_has_all_required_inputs` (it lists the calc's formals by name). Restated: `tests/model_families.py` MFE `owned` +2 (the WI-039 precedent, dated comment); `tests/models/test_power_balance.py` `required_inputs` `eta_p_in` → `q_recovered_in`, `p_pump_in` → `p_pump_total_in` (dated comment). Final: **47 passed / 1 failed / 13 skipped**, the one failure the census fingerprint test, re-derived in phase 4 — as at WI-044 phase 1.

### Phase 2 record — 2026-09-08

- The MR-WI045-16 restatement and the § Predictions table were written by the design task (T-003) and stand above; this record confirms they precede commit A in git order.
- `evidence/baseline_before/`: `study_route.execute_baseline` on the unchanged package → `baseline_result.json` (106 channels, 10 verdicts, LCOE 322.31843948570247) and `package_identity.json` (sealed executable `7d295fec2c78…`, the WI-044 pin); `_work/` removed; the single runner's output → `run_stellaris_single_output.txt` (anchors green, verdict parity 10 / `full_satisfaction`, bit-exact vs oracle PASS).
- Commit A: the four library files, the two design files, the six twins, the two test restatements, and this item's directory.

### Phase 3 record — 2026-09-08

- **Regeneration pass 1** (`evidence/regen_output.txt`): `Stencils - New: 3, Preserved: 69, Regenerated: 1`. The three new stencils are `mfe_power_balance/reactor_source_heat_impl.py` and `mfe_primary_loop/primary_coolant_loop_impl.py` (AUTO, bodies as the design's expressions) and `mfe_power_cycle/power_cycle_efficiency_impl.py` (the manual stub). The one `Regenerated` is the power balance's AUTO stencil, whose interface changed (`backup/mfe_power_balance_calc_impl_20260908_072820.py` created — the WI-044 phase-3 case); its body carries `q_recovered_in` and `p_pump_total_in` at the old positions (`p_th = mn_in * p_neutron + p_alpha + p_input_in + q_recovered_in`; `recirculating = p_coils + p_pump_total_in + …`). `levelized_replacement_cost_impl.py` and `plasma_sustainment_impl.py` byte-identical (`git diff --quiet`).
- **The caller's unpack order** (`generated/modules/mfe_power_cycle/power_cycle_efficiency.py`): `(margin_low, T2_C, margin_high, eta_th, eta_fit, domain_product)` — NOT the declaration order (design D13 anticipated this). The normative body was restored on the stencil's `inputs.<field>_in` names returning in the caller's order; the caller was not edited.
- **Regeneration pass 2** (`regen_output_2.txt`, after `rm -rf handwritten/backup/`): `New: 0, Preserved: 73, Regenerated: 0`, no backup dir, the cycle impl byte-identical to the restored body, the existing manual impls untouched, seal clean.
- **Stale-stencil check** (`evidence/stencil_check.py`, WI-044's, → `stencil_check_output.txt`): 50 AUTO stencils checked, 4 manual skipped, **0 stale**.
- **The contract**: the three constraint ids above; 20 new channels under `source_heat__`, `primary_loop__` (the usage rename of phase 1) and `cycle__`; 23 new entry keys; semantic fingerprint `a331cd82e48f19d5…`.
- **The oracle** (`verify_stellaris.py`): `IN` −`eta_th`, `eta_p`, `p_pump` +23; `compute()` forms `q_source`, the loop chain, the cycle chain, then `p_th` and `recirculating` on the two totals (written from the design's equations); the return dict +20; `reconstruct_reference_circuit()` beside `compute()` (SV-064). **The seam** (`oracle_entry.py`): the entry-key map −1 +23 (D7's levers marked), the channel map +20, `OPERAND_BINDINGS` +3 with the contract's ids. **The single runner**: `EXPECTED_VERDICTS` +3, `EXPECTED_VERDICT_COUNT` 13, the parity message, the oracle gate +18 channels; the nine anchors restated to the live values only after the gate read bit-exact (first run: anchors DEVIATION as expected, parity 13 PASS, oracle PASS; second run: all green — `evidence/baseline_after/run_stellaris_single_output.txt`).
- **The held-mode identity** (`evidence/compat_mode/`, the compatibility proposal through `study_route.run_points` with the route's `CHANNELS` plus the twenty new keys): **106 of 106 entering-pin channels bit-identical, 0 moved; the old ten verdicts unchanged; LCOE 322.31843948570247**; the three new verdicts satisfied on the live-computed loop and cycle (`diff_vs_pin.json`).
- **The live baseline** (`evidence/baseline_after/`): 126 channels, 13 verdicts satisfied, LCOE **237.2528002420958**; every predicted channel within 1.3e-16 relative of the design's prediction; `p_fus`, the wall peak, `B_peak`, `beta`, `p_aux_required` bit-identical to the pin (`diff_vs_predictions.json`); the sealed executable fingerprint `f5373d2d25f196cd…`.
- **P1 / P3 / P4 and the synthetic cases** (`evidence/offdesign_points/`, `evidence/synthetic_cases/`; `evidence/run_phase3_points.py`): every loop and cycle channel and LCOE at relative deviation 0.0 from the predictions; the oracle seam at 0.0 (max 3.2e-16); verdicts — P1 `loop_capacity_ok` violated (with `peak_field_ok` violated as at the pin), P3 `loop_capacity_ok` and `recirc_ok` violated (rec_frac 0.527, LCOE 250.53), P4 all thirteen satisfied (LCOE 171.23), T_hot 350 °C `cycle_domain_ok` violated with `eta_fit` 0.3713 published, n_loops 7 `loop_capacity_ok` and `recirc_ok` violated with `p_elec` 717.77; the four verdicts re-derived through `OPERAND_BINDINGS` agree with the package at all six points (`verdict_rederivation.json`; the `recirc_ok` threshold is the constraint usage's own default 0.5, not an entry key).
- **Deviation from the plan's text:** the design's `loop__*` channel names are `primary_loop__*` (phase 1's keyword rename); the plan's `evidence/compat_mode/result.json` and `offdesign_points/result.json` carry the route's cases with inputs, outputs and verdicts, and a `summary.json` beside them.

### Phase 4 record — 2026-09-08

- **Re-pin by the producers** (memory `gotcha_repin_after_regeneration`): the snapshot recaptured from the twin tree; `manifest.json` re-pinned — indicator `1b6e6b313d93f5f0…`, executable `f5373d2d25f196cd…`, semantic `a331cd82e48f19d5…`, `baseline.verdicts` thirteen (alphabetical, the three new ones `satisfied`), `baseline.headline.value` **237.2528002420958** from the executed live baseline — **the first moved headline since the pin discipline began, by design** (MR-WI045-16 (b)); `m.load()` validated; the `availability` axis untouched (WI-046's). `mfe_census.json` re-derived: **229** entry points (209 − `eta_th`, `eta_p`, `p_pump` + 23), exactly the prediction; library defaults 51, usage literals 10, design attributes 168.
- **The six fixtures** re-derived from `scripts/study/indicators.py` and `EXPECTED_SEMANTIC_FINGERPRINT` / `FIXTURE_CONTRACT` restated from the report: the geometry axes fire the three new modules and reach the three new constraints (R, a: 71 → 77 fired, 104 → 127 tainted; R+tie 76 → 82, 109 → 132; I_coil 73 → 79, 99 → 122; twelve of thirteen constraints reachable, `tbr_ok` the one unreachable); `availability` 6 / 8 and `interest_rate` 8 / 11 unchanged with all thirteen unreachable. `test_I_coil_reaches_the_field_constraints_through_calcs` gains the three fences (the loop sizes from the fusion power); `test_operand_bindings` `PINNED_LCOE` 322.31843948570247 → 237.2528002420958 with the history comment.
- **The count sites**, each with a dated comment: `study_route.py` `EXPECTED_CONSTRAINT_COUNT = 13`; `run_stellaris_single.py` (phase 3); `test_operand_bindings.py` 10 → 13 entries and 18 → 22 feature-ref operands; `test_valid_empty.py` bounds / `constraints_unreachable` 13; `test_known_answers.py` `constraints_unreachable` 13.
- **Validation** (`evidence/validate_complete_after.txt`): unchanged from phase 1 (Level 2 the 12 placeholders; Level 6 248). **`tests/models`: 48 passed / 13 skipped.** The affected `tests/study` files (`test_known_answers`, `test_operand_bindings`, `test_valid_empty`) green; the full battery is phase 5's run of record on the committed tree (its git-clean gate fails on an uncommitted one — memory `gotcha_repin_after_regeneration`).
- **SV-063, SV-064, SV-065** added and `passing`; nine trace rows (`data/traceability_matrix.csv`).
- Commit B: the regenerated package, the four handwritten impls (three new, one regenerated AUTO), the oracle, the seam, the runner, `study_route.py`, the pin files (snapshot, manifest, census), the six fixtures and the three test files, the two PM matrices, and this item's `evidence/` and plan.

### Phase 5 record — 2026-09-08

- **The run of record** (`evidence/tests_study_run_of_record.txt`, one battery, detached with `setsid nohup`, the tree at commit B plus the two restatements below): **86 failed / 424 passed / 1 skipped in 11:32** — the entry count exactly; every failure in `test_study_publication_fail_closed.py` (the 75 pre-existing fail-closed cases + 11 for `20260907-minor-radius`), no other failing test, no errors.
- **Two count sites the plan's list missed, found by the battery and restated with dated comments (commit C):** `tests/study/test_verify.py` `test_every_catalog_constraint_is_rederived_with_its_operand_count` carries the constraint set by name (+3); `tests/study/test_numeric_evidence.py` `test_real_multi_output_values_survive_reopened_store_and_export` asserted `p_et == 0.333 · p_th` with the held efficiency as a literal — it now declares the cycle's `eta_th` channel in its required map and asserts `p_et == eta_th · p_th` (the identity, on the calc's own channel). Both green in isolation (33 passed / 1 skipped) before the run of record.
- **A contaminated first run, superseded and recorded:** the first battery after commit B was launched as a harness background command and killed by the harness's memory accounting mid-run; the re-launch overlapped with a second detached launch of the same command (the round agent's), and the two shared `.integration_workspace` — 89 failed / 380 passed / 41 errors, the errors all "a previous run left .integration_workspace behind". Not a regression; the strays were stopped, the workspace removed, and the single detached run above is the run of record (the goal's harness note: detached runs with short polls).
- **Commit C:** the two test restatements, this plan, and the run of record.
- The tree is handed to WI-046's plan (packet § 9); its `evidence/baseline_before/` is this item's `evidence/baseline_after/` (live: 126 channels, thirteen verdicts, LCOE 237.2528002420958; held: the WI-044 pin bit-for-bit through the compatibility proposal).

