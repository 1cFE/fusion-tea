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

- [ ] Write the four library files and the two design files from design § Proposed design verbatim; re-read each against the design (formals, expressions, the dormancy defaults, every `Source`/`Ref`/`Basis`)
- [ ] `uv run agentic-mbse validate models` — Level 1 0 errors; Level 2 the 12 pre-existing warnings only; Level 3 pass. **If Level 3 rejects `r_comp ** k_isen` or the chained outputs, stop:** that is the design's risk 4, a form question, not a number
- [ ] `uv run agentic-mbse validate models --complete` → `prototype/validate_complete.txt`; Level 6 residue: expect the WI-044 residue plus 23 design attrs (207 → 230); record the actual
- [ ] Copy each of the six files to its twin (`cp`); `cmp` clean on all six; `diff -rq` between the two trees shows no other difference
- [ ] `uv run python -m pytest tests/models -q` — expect 47 / 1 / 13 with the one failure the census fingerprint test (re-derived in phase 4), as at WI-044 phase 1; any other delta explained here

**Gate.** Levels 1–3; twins identical; `tests/models` as expected with every delta explained.

## Phase 2 — The restatement and the predictions, written before regeneration; `evidence/baseline_before/`; commit A

- [ ] Write `## MR-WI045-16 restatement` at the end of this plan (the section below, filled): (a) the committed columns keep their meaning; (b) live differs everywhere, held equals bit-for-bit; (c) three verdicts, the count sites; (d) the entry-point delta; (e) DI-007 scoped
- [ ] Copy design § Expected baseline behaviour (both modes) and § Off-design predictions into `## Predictions` below with the exact `proto_results.json` values (the prediction of record precedes execution in git order)
- [ ] `evidence/baseline_before/`: `study_route.execute_baseline(...)` on the unchanged package → `baseline_result.json`, `package_identity.json` (remove `_work/`); the single runner's output → `run_stellaris_single_output.txt`; confirm `package_identity.json` carries the WI-044 pin (indicator `30abb21be6d7…`, executable `7d295fec2c78…`) and 106 channels, ten verdicts, LCOE 322.31843948570247
- [ ] **Commit A** with an explicit pathspec: the four library files, the two design files, the six twins, `work/active/WI-045_primary-loop-and-cycle/` (spec, design, plan, `prototype/`, `evidence/baseline_before/`); message names the restatement as preceding regeneration

**Gate.** The restatement and the predictions are in git before any regenerated byte.

## Phase 3 — Regeneration (twice); the stale-stencil check; the oracle and the seam; the held-mode identity; the live baseline; P1 / P3 / P4; the synthetic cases

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `generated/handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py` — NEW (the design's body restored over the stencil); `verify_stellaris.py` — REWRITE per D12; `studies/oracle_entry.py` — the keys, channels and three bindings per D12; `run_stellaris_single.py` — `EXPECTED_VERDICTS` +3, `EXPECTED_VERDICT_COUNT` 13, the `p_th` / `recirc` comments; `evidence/baseline_after/`, `evidence/compat_mode/`, `evidence/offdesign_points/`, `evidence/synthetic_cases/` — NEW.

- [ ] Regenerate, pass 1:
  ```bash
  /home/reid/1cfe/fusion-tea/.venv/bin/sysml-codegen generate --models exploration/stellarator_e2e/models \
    --output exploration/stellarator_e2e/generated --package-name stellarator_tea \
    --overwrite --smart-regen --preserve-handwritten
  ```
  Expect `New: 4` (the source-heat, loop and cycle modules and the cycle's handwritten STENCIL, a `NotImplementedError` body), `Regenerated` on the power balance and the plant modules (their interfaces changed), every existing handwritten impl preserved byte-identical; record the counts → `evidence/regen_output.txt`. **Any `Regenerated` on an existing manual-stage calc is a stop** (`gotcha_codegen_manual_stage_regen`); a `backup/` dir created for an AUTO module whose output set grew is the WI-044 phase-3 case — remove it before pass 2
- [ ] Read the stencil `generated/handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py`: the `inputs.<field>` names and the generated caller's unpack order in `generated/modules/mfe_power_cycle/power_cycle_efficiency.py`; restore the design's normative body over the stencil with the return tuple in the caller's order (D13); record the order here
- [ ] `rm -rf exploration/stellarator_e2e/generated/handwritten/backup/` if present; regenerate, pass 2 → `evidence/regen_output_2.txt`: expect `New: 0, Regenerated: 0`, the cycle impl preserved byte-identical (`cmp` against the restored body), no `backup/`, seal clean
- [ ] Run the WI-044 stale-stencil checker (`work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/evidence/stencil_check.py`, copied to `evidence/`) over every AUTO stencil → `evidence/stencil_check_output.txt`: expect 0 stale; the power balance's regenerated body carries `q_recovered_in` and `p_pump_total_in` at the old positions (read it: `p_th = ((mn_in * p_neutron) + p_alpha) + p_input_in) + q_recovered_in` in the emitted order, `recirculating` with `p_pump_total_in` second) — **if a stale stencil survives, delete it and regenerate a third time, as WI-044 did; never patch a stencil by hand**
- [ ] Read `generated/contracts/model_contract.json`: the three new constraint ids (`stellarator_09__stellaris__loop_pressure_ok__<hash>`, `…loop_capacity_ok__<hash>`, `…cycle_domain_ok__<hash>`), their operand names as the predicate IR spells them, the twenty new channel keys and the 23 new entry keys; record them here
- [ ] `verify_stellaris.py` per D12: `IN` −3 +23; `compute()` the source heat, the loop chain, the cycle chain, the two sums with the new operands; the return dict +20; a `reconstruct_reference_circuit()` function beside `compute()` for MR-WI045-13. Written from the design's equations, not from the generated modules
- [ ] `oracle_entry.py`: `ENTRY_KEY_TO_ORACLE_INPUT` −`eta_th` +23 (comment marks the D7 levers); `ORACLE_OUTPUT_TO_CHANNEL` +20; `OPERAND_BINDINGS` +3 with the ids from the contract (`mdot_loop_rated_in` as `{"kind": "input", "key": f"{P}mdot_loop_ref"}`)
- [ ] `run_stellaris_single.py`: `EXPECTED_VERDICTS` gains `loop_pressure_ok`, `loop_capacity_ok`, `cycle_domain_ok` = `satisfied` with dated comments (the sizing rule; the domain); `EXPECTED_VERDICT_COUNT = 13`; the nine-anchor block's expected LCOE re-stated to the live prediction 237.25280024209582 **after** the oracle gate reads bit-exact (never before); the parity message "thirteen satisfied (WI-045: three fences added; the design point moved as predicted)"
- [ ] **The held-mode identity first** (MR-WI045-10): through `study_route.run_points` one proposal at the baseline levers with `loop_live 0.0, cycle_live 0.0, p_pump_direct 195.0, eta_p_direct 0.5, eta_th_direct 0.333` (the compatibility proposal; `required_channels` the route's `CHANNELS` plus the twenty new keys); deposit `evidence/compat_mode/result.json`; diff every channel of the entering pin's `baseline_result.json` (106) against it: **every one bit-identical, the old ten verdicts unchanged, LCOE 322.31843948570247**; the three new verdicts satisfied; record the diff here (`evidence/compat_mode/diff_vs_pin.json`)
- [ ] **If any existing channel moves in held mode, stop and derive why before continuing** (`goal.md` § Invariants; the packet § 3 rule)
- [ ] The live baseline: the single runner → `evidence/baseline_after/run_stellaris_single_output.txt` (13 / `full_satisfaction`; the oracle gate bit-exact on every channel including the twenty new ones); `study_route.execute_baseline(evidence/baseline_after)`; diff against `## Predictions` (live): every listed channel to 1e-9 relative; `p_fus`, `wall_load_peak`, `B_peak`, `beta`, `p_aux_required` bit-identical to the pin → `evidence/baseline_after/diff_vs_predictions.json`
- [ ] Execute P1, P3, P4 through `run_points` (proposals in the committed record's `point()` shape; P3 and P4 differ only in `n_loops`); deposit `evidence/offdesign_points/results.json`; compare the loop and cycle channels to `## Predictions` (1e-9 relative); the oracle seam's `evaluate()` at the three points → 0.0 relative deviation on every new channel and on `lcoe`; the three new verdicts and `recirc_ok` re-derived through `OPERAND_BINDINGS` agree with the package (P1 capacity violated; P3 capacity and recirc violated; P4 all satisfied)
- [ ] The synthetic cases through `run_points` and the oracle → `evidence/synthetic_cases/results.json`: `loop_T_in` 623.15 − 200 (so `T_hot` 623.15 K, the Stellaris local 350 °C) reads `cycle_domain_ok` violated with `cycle__eta_fit` 0.3713254788502389 published; `n_loops` 7 reads `loop_capacity_ok` violated with `loop__p_elec` 717.7666412961582; no clamp anywhere

**Gate.** The held-mode identity holds; the live predictions hold; the oracle agrees; the fences re-derive.

## Phase 4 — Re-pin, fixtures, the count sites, batteries, SV and trace rows; commit B

**Files.** `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, `tests/study/data/*.expected.json`, `tests/study/test_known_answers.py`, `tests/study/test_operand_bindings.py`, `tests/study/test_valid_empty.py`, `studies/study_route.py:49` — RE-DERIVE / RESTATE; `modeling_project/VALIDATION_MATRIX.md`, `data/traceability_matrix.csv` — via `pm` ops.

- [ ] Snapshot recaptured from the twin tree (`capture_instance_graph_snapshot([Path("exploration/stellarator_e2e/models")], …)`)
- [ ] `manifest.json`: the three fingerprints from the package's contracts (`files` as path strings); `baseline.verdicts` gains the three (`{"source_local_identity": "loop_pressure_ok", "expected": "satisfied"}`, …) = thirteen; `baseline.headline.value` re-pinned from the executed live LCOE (expected 237.25280024209582 — **a moved headline by design, the first since the pin discipline began; the restatement below says so**); `m.load(manifest)` validates; the `availability` axis untouched (WI-046's)
- [ ] `mfe_census.json` re-derived (`integ.rederived_census(pkg)` + the new semantic fingerprint); expect **229** (−`eta_th`, `eta_p`, `p_pump`; +23) — record the actual count and delta
- [ ] The six fixtures re-derived via `scripts/study/indicators.py --package … --manifest … --groups tests/study/data/axes.known_answers.json`; `EXPECTED_SEMANTIC_FINGERPRINT` and `FIXTURE_CONTRACT` restated **from the report** (predicted: the three new modules fired on every axis that reaches `fusion` or `heat` — R, R+tie, a, I_coil — and the three new constraints reachable there; `availability` and `interest_rate` gain the cycle and loop modules only if the trace reaches them, which it should not) with a dated comment saying what moved and why
- [ ] The count sites restated from the live package, each with a WI-045 comment: `study_route.py:49` `EXPECTED_CONSTRAINT_COUNT = 13`; `run_stellaris_single.py` (done in phase 3); `tests/study/test_operand_bindings.py` (ten → thirteen); `tests/study/test_valid_empty.py` (bounds / `constraints_unreachable`); `tests/study/test_known_answers.py` (`constraints_unreachable` on the no-response axes). These are counts of the constraint set, read from the report and the contract, never fitted
- [ ] `uv run agentic-mbse validate models --complete` → `evidence/validate_complete_after.txt`; compare with `prototype/validate_complete.txt`; record any new residue
- [ ] `tests/models` — expect 48 / 13 or better; every delta explained
- [ ] `rm -rf .integration_workspace`; `tests/study` — expect green apart from the branch's known fail-closed cases (86 at entry: the 75 + 11 for `20260907-minor-radius`); every other delta explained. **Expected known movers** (the WI-044 phase-5 precedent): the `pipeline.yaml` line number in `test_mechanical_failures.py` (module order changes with three new modules); the reach test in `test_known_answers.py` if a geometry axis's reach changed; each verified against the live pipeline before restating
- [ ] `pm add-validation` ×3 then `pm update-validation … --status passing` with the evidence paths: **SV-063** the held-mode identity (every channel of the entering pin bit-identical under the compatibility proposal; the old ten verdicts; LCOE 322.31843948570247; `evidence/compat_mode/`); **SV-064** the reference-circuit reconstruction (2101.7 MW at 2025.7 kg/s over 200 K, `cp` 5187.6 implied against 5193 bound; 363.9 / 315.7 / 329.187 kPa; 2231.1 MW; 129.4 against 130.8 printed; `w_fluid` 129.4 at `eta_is` 0.772796639536644 to 1e-12 — a reconstruction, not validation); **SV-065** the live baseline and P1 / P3 / P4 at the predictions with oracle parity 0.0, the three new verdicts and `recirc_ok` re-derived, the synthetic fail-closed cases
- [ ] `pm trace-element` for `'Reactor Source Heat'`, `'Primary Coolant Loop'`, `'Power Cycle Efficiency'`, the three constraint defs, and the eighteen instance-bound facts (one row each, or grouped as the tool allows)
- [ ] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified — below)
- [ ] **Commit B** with an explicit pathspec: the regenerated package, the handwritten impl, the oracle, the seam, the single runner, the pin files, the fixtures and the four test files, `study_route.py`, the SV/trace rows, `evidence/baseline_after/`, `evidence/compat_mode/`, `evidence/offdesign_points/`, `evidence/synthetic_cases/`, `evidence/regen_output*.txt`, `evidence/stencil_check*`, `evidence/validate_complete_after.txt`, this plan; never `git add -A`
- [ ] Note for the modelling PM: the BACKLOG row moves at close through `pm close-item`; the round's trail records the landing

**Gate.** Both batteries as expected with every delta explained; no expectation patched to match; SV-063..065 `passing`.

## Phase 5 — The `tests/study` run of record; commit C

- [ ] After commit B, `tests/study` on the clean tree (detached, `setsid nohup`, ~11 min); record the count and the failing set; confirm the failing set equals the pre-existing fail-closed set (86) or explain every difference
- [ ] **Commit C**: any test-file restatement the run forced, and this plan's phase-5 record
- [ ] Hand the tree to WI-046's plan (packet § 9); its `evidence/baseline_before/` is this item's `evidence/baseline_after/`

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

## Spec success criteria, verified (filled at phase 4)

- **Functional.** —
- **Quality.** —
- **Verification.** —
- **Requirements not covered by an SV, checked by reading.** —

## Phase records

*(appended as each phase completes)*
