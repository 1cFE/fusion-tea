---
Status: draft
Created: 2026-09-08
Updated: 2026-09-08
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-046 Plan — the lifecycle calendar

Five phases, the WI-044 shape, run **after WI-045's commit B and before WI-047** (basis packet § 9): model edits and twins; the restatement and the predictions re-stated at WI-045's package state, `evidence/baseline_before/`, commit A; regeneration with the new manual stencil, the retired impl deleted, the oracle, the seam, the route and the single runner, the held-mode identity and the live execution, the off-design points; re-pin by producers, the axis rename and fixture, batteries, SV and trace rows, commit B; the `tests/study` run of record, commit C.

## Source documents

- `spec.md` MR-WI046-1..16; `design.md` D1–D10, § Proposed design (the SysML text and the impl body to copy in), § Expected baseline behaviour, § Off-design predictions, § Validation plan; `prototype/proto_results.json`.
- The basis packet `work/orchestration/goals/plant-closure/evidence/round1_basis_packet.md` §§ 2, 3, 6, 8, 9 and its Amendment (items 2, 4).
- Recipes: memory `gotcha_repin_after_regeneration` (snapshot → manifest → census → fixtures → single runner; the two traps; the adding-a-verdict note does not apply — this item adds none), `gotcha_codegen_manual_stage_regen` (a deleted manual impl; the backup-dir two-pass rule), `gotcha_syside_env_not_exported`.
- Precedent: `work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/plan.md` phases 3–5 and its phase records (the stale-stencil check over every AUTO_IMPLEMENTED impl after regeneration — `evidence/stencil_check.py` there — is re-run here).

## Design summary

One handwritten calc, `'Lifecycle Calendar'`, with two modes: live (the finite-horizon calendar) and held (the retired periodic chain verbatim, selected by `availability_direct > 0`); `availability` bound by reference to its output; `cas72_annual` from it; `'Levelized Replacement Cost'` and its impl retired; the oracle derives the closed form independently; the `availability` axis becomes `availability_direct`; no verdict added; the held mode reproduces the entering pin bit-for-bit.

## Prototype baseline

`prototype/proto.py` (pure Python; no model file touched): the held mode `==` the oracle mirror and the pinned CAS72; the live design point (0.9027777777777779; five events; CAS72 136,289,876.08; LCOE 305.184 at the entering pin's other values); the arms A–D; the synthetic boundary cases; the stepping points E and F. Nothing regenerated; Levels 1–6 run in phase 1.

## Environment

`set -a; source ~/1cfe/agentic-mbse/.env; source .venv/integration.env; set +a` for validation, `tests/models` and the seam; `PYTHONPATH=$HOME/1cfe/teax/packages/teax-simkit:$PWD/exploration/stellarator_e2e/pkg` for the single runner and the route; `PYTHONPATH` unset for `tests/study`. Always `uv run python`. Commit with an explicit pathspec; never `git add -A` (the owner's staged files). Long runs detached (`setsid nohup`) with a monitor.

## Validation strategy

Levels 1–3 after every model edit; the held-mode diff before anything else after regeneration; the live execution with oracle parity; the boundary cases in the single runner's gate; the batteries after the re-pin; `tests/study` after the commit (its git-clean gate).

---

## Phase 1 — Model edits at WI-045's package state; Levels 1–3; twins; `tests/models`

**Precondition.** WI-045's commit B is in `git log` (the loop and cycle landed, the package regenerated, the verdict count at 13). Re-read `mfe_plant.sysml` and `stellarator_plant.sysml` at that state: the line numbers in `design.md` are as of `d981670f` and will have moved; the sites are the CAS72 block (`replacement_cost_per_event` … `cas72_annual`), the `cas70_calc` usage, the `availability` declaration, and the instance's `availability = 0.85` binding.

**Files.** `models/library/analyses/mfe_lifecycle.sysml` — NEW (design § Proposed design, verbatim); `models/library/analyses/mfe_account_costs.sysml` — the `'Levelized Replacement Cost'` def REMOVED (design § Retired); `models/designs/generic_mfe/mfe_plant.sysml` — the calendar block, the `cas70_calc` input, the `availability` reference binding, the `mfe_lifecycle` import; `models/designs/stellarator_09/stellarator_plant.sysml` — the four bindings replacing `availability = 0.85`, the `fluence_limit` doc sentence; `models/stellarator_migration_ledger.md` — one dated line under the retired calc's row (D9); the twins under `exploration/stellarator_e2e/models/` — COPY byte-for-byte.

- [x] Write the four model edits from the design's text; keep `fuel_calc` reading `availability` (D4)
- [x] `uv run agentic-mbse validate models` — Level 1 0 errors; Level 2 the pre-existing warnings only (12 at the WI-044 pin; WI-045 may have moved the count — take WI-045's phase record as the baseline); if the exact route rejects the forward reference `availability = calendar.availability` (risk 2), move the calendar block above the fuel block and record it
- [x] `uv run agentic-mbse validate models --complete` → `prototype/validate_complete.txt`; compare Levels 4–6 with WI-045's run; the only expected delta is the retired def's own rows and the new def's
- [x] Copy the changed files and the new file to their twins (`cp`); `cmp` clean; `diff -rq` between the trees shows no other difference
- [x] `uv run python -m pytest tests/models -q` — expect WI-045's count or better; a test that names `'Levelized Replacement Cost'` or counts calc defs / modules by literal is restated from the live tree with a dated comment and recorded here

**Gate.** Levels 1–3 clean; twins identical; `tests/models` as expected with every delta explained.

## Phase 2 — The restatement and the predictions at WI-045's package state; `evidence/baseline_before/`; commit A

- [x] `evidence/baseline_before/`: `study_route.execute_baseline(...)` on WI-045's package (unchanged by this item) → `baseline_result.json`, `package_identity.json` (remove `_work/`); the single runner's output → `run_stellaris_single_output.txt`; confirm `package_identity.json` carries WI-045's executable fingerprint
- [x] Re-run `prototype/proto.py` against that baseline (its `cost_per_event` = the landed `blanket + divertor` capital) and write `## Predictions` below with the exact live values at WI-045's package state — the availability, count, dates, margin and ratio must equal the design's (they do not depend on WI-045); CAS72 and LCOE will differ and are stated here as the prediction of record
- [x] Write `## MR-WI046-15 restatement` below: (a) the committed `cas72` and `availability` columns are the periodic chain's at held availability, never edited; (b) the held mode reproduces them at every point, the live mode differs at every point whose wall peak differs from the design point's and at the design point by the first-event timing; (c) no verdict is added by this item; the count sites stay at WI-045's 13; (d) the entry-point delta (`availability` out; `availability_direct`, `outage_years`, `unplanned_fraction`, `coil_life_fpy` in; census +3 net predicted) and the `cas72` objective's channel key change; (e) the round's study re-reads the inherited window in both modes and joins by case id to the committed `20260907-minor-radius` record
- [x] **Commit A** with an explicit pathspec: the four model files, the ledger line, the twins, `work/active/WI-046_lifecycle-calendar/` (spec, design, plan, `prototype/`, `evidence/baseline_before/`); message names the restatement as preceding regeneration

**Gate.** The restatement and the predictions are in git before any regenerated byte.

## Phase 3 — Regeneration; the impl; the oracle, the seam, the route, the single runner; the held-mode identity; the live execution; A–F

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py` — NEW (the design's body on the stencil's names); `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` — DELETED; `verify_stellaris.py` — the calendar's closed-form derivation and the four `availability` sites (D1, § Changed); `studies/oracle_entry.py` — the levers and the eleven channels; `studies/study_route.py` — the axis rename (D5); `run_stellaris_single.py` — the guard gate restated (D9), the event-date print (D6); `evidence/baseline_held/`, `evidence/baseline_live/`, `evidence/offdesign_points/` — NEW.

- [x] Regenerate:
  ```bash
  /home/reid/1cfe/fusion-tea/.venv/bin/sysml-codegen generate --models exploration/stellarator_e2e/models \
    --output exploration/stellarator_e2e/generated --package-name stellarator_tea \
    --overwrite --smart-regen --preserve-handwritten
  ```
  Expect `New: 1` (the calendar module and its stencil), the old CAS72 module gone, `Regenerated` on the plant module (its wiring changed) and nothing manual. Read the stencil's `inputs.<field>` names and the caller's unpack order from `generated/modules/mfe_lifecycle/lifecycle_calendar.py`; write the impl body from the design onto them; record the unpack order in the impl's docstring
- [x] Delete `levelized_replacement_cost_impl.py` if the generator left it; `rm -rf generated/handwritten/backup/` if present; regenerate again — expect `New: 0, Preserved: N, Regenerated: 0`, the impl byte-identical, no backup dir, seal clean (`gotcha_codegen_manual_stage_regen`). **Any `Regenerated` on another manual-stage calc is a stop**
- [x] Re-run WI-044's stale-stencil checker (`work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/evidence/stencil_check.py`) over every AUTO_IMPLEMENTED impl: expect 0 stale (the plant module's wiring changed; its stencil must show the calendar's inputs)
- [x] Read the eleven channel keys and the four new entry keys from `generated/contracts/model_contract.json`; confirm whether `availability` minted a producer channel or became a bare alias (D4); record which and, if the alias, apply the fallback and regenerate again
- [x] `verify_stellaris.py` per design § Changed: `IN` −`availability` +the four; `_oracle_lifecycle_calendar` from the closed form (D1) with the held mode through the existing mirror and D2's readings; `compute()` reads `cal["availability"]` at the four sites and `cal["cas72_annual"]`; the return dict +11. Written from the design's statement, not from the impl
- [x] `oracle_entry.py`: the levers, the eleven channels, the `cas72` objective channel; `OPERAND_BINDINGS` unchanged
- [x] `study_route.py`: `AXES`, `BASELINE`, `proposal_for`, the availability sweep restated onto `availability_direct` (D5) with a dated comment; `manifest.json`'s `axes` / tie data restated in phase 4
- [x] `run_stellaris_single.py`: `_cas72_guard_gate` restated — the three synthetic guard cases against `lifecycle_calendar_held` and the mirror; a fourth family of live boundary cases (`L 4, d 7/12, N 10 / 8.7 / 9.1667 / 9.1667+1e-6`; `q_n 0`; no outage; `i 0`; `u` monotone) against the oracle's closed form and the research's expected values; the baseline's event dates printed in both modes; `EXPECTED_VERDICT_COUNT` unchanged by this item (13 after WI-045)
- [x] **Held-mode identity:** with the instance's `availability_direct` temporarily overridden to `0.85` through the route's proposal (never by editing the instance), execute the baseline → `evidence/baseline_held/baseline_result.json`; diff against `exploration/stellarator_e2e/studies/20260907-minor-radius/results/baseline_result.json` restricted to the channels WI-045 did not move (and against WI-045's `evidence/baseline_after/` for the ones it did): **every channel bit-identical; the eleven new channels at D2's held values; the verdicts unchanged** — record the diff here. **If any channel moves, stop and derive why before continuing** (`goal.md` § Invariants)
- [x] **Live execution:** the instance as bound → `evidence/baseline_live/baseline_result.json` and `events.json`; compare the eleven channels with `## Predictions` (1e-9 relative); the single runner's output → `evidence/baseline_live/run_stellaris_single_output.txt` with verdict parity and the oracle gate passing (0.0 on all eleven)
- [x] Execute A–D (the calendar levers moved at the baseline) and E–F (`c3343`, `c7752` in the committed record's `point()` shape) through `study_route.run_points`; deposit `evidence/offdesign_points/results.json` and `events.json`; compare with `proto_results.json` (E and F re-run in the prototype on the executed `cost_per_event`); every non-calendar, non-availability-consuming channel at E and F equal to the entering pin's value at the same coordinates (or WI-045's, for the channels it moved)

**Gate.** The held-mode identity holds; the live prediction holds with oracle parity; the boundary cases pass; A–F agree.

## Phase 4 — Re-pin, the axis and fixture, batteries, SV and trace rows; commit B

**Files.** `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, `tests/study/data/axes.known_answers.json`, `tests/study/data/availability.expected.json` → `availability_direct.expected.json`, the other five fixtures, `tests/study/test_known_answers.py` — RE-DERIVE / RESTATE; `modeling_project/VALIDATION_MATRIX.md`, `data/traceability_matrix.csv` — via `pm` ops.

- [x] Snapshot recaptured from the twin tree
- [x] `manifest.json`: the three fingerprints from the package's contracts (`files` as path strings); `baseline.verdicts` unchanged by this item (13); the `cas72` objective's channel `calendar__cas72_annual`; the axis block renamed; `baseline.headline.value` re-pinned from the executed **live** LCOE (the pin is the package as bound: live); `m.load(manifest)` validates
- [x] `mfe_census.json` re-derived (`integ.rederived_census(pkg)` + the new semantic fingerprint); expect +3 net (`availability` out; four in) — record the actual count and delta
- [x] `axes.known_answers.json`: `availability` → `availability_direct`; the six fixtures re-derived via `scripts/study/indicators.py`; `EXPECTED_SEMANTIC_FINGERPRINT`, `FIXTURE_CONTRACT` and `CASES` restated **from the report** with a dated comment (predicted: `availability_direct` reaches `cas72`, `fuel`, `lcoe`, `lcoe_1cfe` and no constraint — the held-mode response; `a`, `R`, `R+tie`, `I_coil` newly reach the eleven calendar channels through the wall peak; `interest_rate` reaches `calendar__replacement_pv` and `cas72_annual`); `test_availability_reaches_no_constraint` docstring restated (D5)
- [x] Any literal count the batteries find restated from the live package with a WI-046 comment; the verdict-count sites must not move
- [x] `uv run agentic-mbse validate models --complete` — compare with `prototype/validate_complete.txt`; record any new residue
- [x] `tests/models` — WI-045's count or better; every delta explained; add `tests/models/test_lifecycle_calendar.py` importing the impl's two mode functions and the oracle's closed form on the research's boundary cases (MR-WI046-12)
- [x] `rm -rf .integration_workspace`; `tests/study` — expect green apart from the branch's known fail-closed cases (75 at entry plus the per-record cases the newest records add); every other delta explained
- [x] `pm add-validation` ×3 then `pm update-validation … --status passing` with the evidence paths: SV-063 the held-mode identity (every channel bit-identical at `availability_direct` 0.85; CAS72 126,649,655.78572692; the eleven held readings); SV-064 the live calendar at the design point (availability 0.9027777777777779, five events at the stated dates, CAS72 and LCOE at the prediction of record, oracle parity 0.0, the closed form and the walk agreeing); SV-065 the boundary cases (the research's synthetic values reproduced by the impl and the oracle; the time identity; `u` monotone; the six-at-five-months step)
- [x] `pm trace-element` for `'Lifecycle Calendar'` (`mfe_lifecycle.sysml`, type calc) and the four instance bindings
- [x] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified — below)
- [x] **Commit B** with an explicit pathspec: the regenerated package (including the deleted impl), the new impl, the oracle, the seam, the route, the single runner, the pin files, the fixtures and the two test files, the SV/trace rows, `evidence/baseline_held/`, `evidence/baseline_live/`, `evidence/offdesign_points/`, this plan; never `git add -A`
- [x] Note for the modelling PM: the BACKLOG row moves at close through `pm close-item`; the epic file's item note is owner-facing

**Gate.** Both batteries as expected with every delta explained; no expectation patched to match; SV-063..065 `passing`.

## Phase 5 — The `tests/study` run of record; commit C

- [x] After commit B, `tests/study` on the clean tree (detached; ~11 min last time); record the count and the failing set; confirm the failing set equals the pre-existing fail-closed set or explain every difference
- [x] **Commit C**: any test-file restatement the run forced, and this plan's phase-5 record

---

## Feasibility concerns

1. **The reference redefinition mints no channel** (risk 1). *Mitigation:* D4's fallback, recorded in phase 3.
2. **The forward reference in the plant** (risk 2). *Mitigation:* Levels 1–3 in phase 1 before the twins; a text move if needed.
3. **The deleted impl leaves a backup or a stale plant stencil.** *Mitigation:* the two-pass recipe and the stale-stencil checker.
4. **The single-runner gate's import of the old impl** breaks at regeneration until restated. *Mitigation:* restated in the same phase before the runner executes.
5. **WI-045 has not landed when this plan starts.** *Mitigation:* phase 1's precondition; this item waits (packet § 9).

---

## MR-WI046-15 restatement — the comparison meaning at the new pin (2026-09-08, written before regeneration)

(a) **The committed columns.** Every committed record's `cas72` (`cas72_calc__cost`) and `availability` columns are the periodic chain's at the held availability 0.85 (`L_cal = L / 0.85`, `n_rep = ceil(30 / L_cal) − 1`, events at `k · L_cal`); their meaning is unchanged and no record is edited.
(b) **What the new package reproduces and what it moves.** With `availability_direct = 0.85` (the held mode) the package reproduces those columns and every other channel bit-for-bit at every point — the compatibility bridge the round's study proves by case id. With `availability_direct = 0.0` (the instance as bound, the live calendar) `availability` and CAS72 differ at every point: at the design point by the first event's timing alone (4.524 yr instead of 5.322; five events either way; 0.85 → 0.9027777777777779; CAS72 128,437,178.45 → 138,213,460.01 at WI-045's package state), and elsewhere by the count too (`c3343`: 12 → 11).
(c) **No verdict is added by this item.** The verdict set stays at WI-045's thirteen and every count site keeps its value; the fourteenth is WI-047's.
(d) **Entry points and channels.** `availability` retires as an entry point; `availability_direct`, `outage_years`, `unplanned_fraction`, `coil_life_fpy` appear (census 229 → 232 predicted, +3 net); the `cas72` objective's channel key moves from `cas72_calc__cost` to `calendar__cas72_annual` (the objective's name unchanged); eleven `calendar__*` channels appear; the `availability` study axis becomes `availability_direct` (design D5) and its known-answer fixture is re-derived, its no-response claim kept — a sweep over the held-mode switch reaches `cas72`, `fuel`, `lcoe`, `lcoe_1cfe` and no constraint.
(e) **The round's study** re-reads the inherited window in both modes and joins by case id to the committed `20260907-minor-radius` record; the design-point attribution arm assigns the calendar's share of the move; every availability is reported beside its outage, its unplanned fraction and its replacement count.

## Predictions — the calendar channels at the baseline and at A–F (2026-09-08, `prototype/proto_results_at_wi045.json`, written before regeneration)

`prototype/restate_at_wi045.py` is `proto.py` re-run at WI-045's package state (the oracle at `693a4dff`: live loop and cycle, `p_th` 3302.29, `cost_per_event` = blanket 718,554,642.71 + divertor 109,033,211.40 = 827,587,854.11 $, `q_peak` 3.9788448937763854, `N` 30, `i` 0.07). The design's table at the entering pin is the cross-check: the availability, count, dates, margin and ratio are identical (they do not depend on WI-045); CAS72 and LCOE are the prediction of record below.

| Mode / arm | `availability` | `n_replacements` | events [yr] | `productive_fpy` | `cas72_annual` [$/yr] | LCOE [$/MWh] | `dated_energy_ratio` | `coil_life_margin_fpy` |
|---|---|---|---|---|---|---|---|---|
| held (`availability_direct` 0.85) — the identity | `0.85` | `5.0` | 5.32, 10.64, 15.97, 21.29, 26.61 | `25.5` | **`128437178.4450173`** (`==` the oracle mirror and WI-045's `cas72_calc__cost`) | **`237.2528002420958`** (bit-identical to `evidence/baseline_before/`) | `1.0` | `-15.5` |
| live, 7 months, `u` 0 — the baseline as bound | `0.9027777777777779` | `5.0` | 4.5239260339489915, 9.631185401231317, 14.738444768513641, 19.845704135795966, 24.95296350307829 | `27.083333333333336` | `138213460.00639772` | `224.6095247280447` | `1.0051616112988944` | `-17.083333333333336` |
| A — 5 months, `u` 0 | `0.9166666666666666` | **`6.0`** | 4.524, 9.465, 14.405, 19.346, 24.286, 29.227 | `27.5` | `149568478.48653913` | `222.60465316226882` | `1.0118678661630118` | `-17.5` |
| B — 7 months, `u` 0.05 | `0.8576388888888891` | `5.0` | 4.762 … 26.144 | `25.72916666666667` | `133124991.0331273` | `235.756845106268` | `1.0092808735586443` | `-15.729166666666671` |
| C — 7 months, `u` 0.10 | `0.8125000000000002` | `5.0` | 5.027 … 27.466 | `24.375000000000007` | `127756586.47991884` | `248.10390641078916` | `1.0134202110184956` | `-14.375000000000007` |
| D — 10 months, `u` 0 | `0.8611111111111112` | `5.0` | 4.524 … 25.953 | `25.833333333333336` | `135143912.0723116` | `235.0709859473848` | `1.012757014874591` | `-15.833333333333336` |

The LCOE column is the exact form (`lcoe_exact`: the numerator with the calendar's CAS72, the denominator on the live availability). E (`c3343`) and F (`c7752`) are executed through the route at their own coordinates and compared with the prototype re-run on the executed `cost_per_event` (design § Off-design predictions: E 11 replacements at 0.7861, F 5 at 0.8912).

## Spec success criteria, verified (2026-09-08)

- **Functional.** `'Lifecycle Calendar'` exists as a manual-interface calc with eleven exposed channels (`calendar__*` in `generated/contracts/model_contract.json`); `availability` is bound by reference and every consumer (`fuel_calc`, `lcoe_calc`, `lcoe_1cfe_calc`) reads `calendar__availability` directly in `generated/pipelines/pipeline.yaml` (lines 815–1007) — one producer, no separate `availability` channel; `cas70_calc` reads `calendar__cas72_annual`; `'Levelized Replacement Cost'` and its impl are gone from the library, the plant, the package and the seal; the package regenerates twice to `Regenerated: 0` and executes in both modes.
- **Quality.** Levels 1–3 pass; Level 2 the 12 pre-existing placeholders; Level 6 248 → 252 (the four new design-attribute references, the pre-existing class) — `evidence/validate_complete_after.txt` unchanged from phase 1; `tests/models` 63 passed / 13 skipped (48 + the 15 boundary tests); the stale-stencil check 0 stale over 50 AUTO stencils; the affected `tests/study` files are the run of record's (phase 5 — the git-clean gate refuses an uncommitted package tree).
- **Verification.** SV-066 (the held-mode identity: 126 / 126 channels, thirteen verdicts, the three guard cases), SV-067 (the live design point and A–F with oracle parity), SV-068 (the boundary cases) — all `passing`; two trace rows.

## Phase records

### Phase 1 record — 2026-09-08

- The four model edits written from design § Proposed design verbatim (`scratchpad/wi046_phase1_edits.py`, string replacement with single-occurrence asserts): `models/library/analyses/mfe_lifecycle.sysml` new (the calc def, 8,364 bytes); `'Levelized Replacement Cost'` removed from `mfe_account_costs.sysml` (94 lines) and replaced by the one-line pointer; the plant's CAS72 block replaced by the calendar block, `availability` bound by reference `= calendar.availability`, `private import mfe_lifecycle::*;` added; the instance's `availability = 0.85` replaced by the four bindings and the `fluence_limit` doc sentence added; the migration ledger's dated note under the retired impl's row.
- Levels 1–3: Level 1 0 errors — the forward reference `availability = calendar.availability` above the `calendar` usage compiles (risk 2 did not bite); Level 2 the 12 pre-existing placeholder warnings (`prototype/validate_complete.txt` lines 23–37, the same `waste` / `fuel_handling` / `other_rpe` literals as WI-045's record); Level 3 pass; Levels 4–5 pass; Level 6 248 → **252** (the four new design-attribute references `outage_years`, `unplanned_fraction`, `coil_life_fpy`, `availability_direct` in the calendar wiring; the same pre-existing class). No new residue class.
- Twins: the four files copied byte-for-byte, `cmp` clean; `diff -rq` shows only the IFE-only files the twin tree never carried.
- `tests/models`: first run 3 failed / 6 errors, one root cause — `analyses/mfe_lifecycle.sysml` absent from the MFE family's owned list (`tests/model_families.py`), so the materialized subset could not resolve the namespace (the WI-045 phase-1 case). Restated: owned +1 with a dated comment. Final: **47 passed / 1 failed / 13 skipped**, the one failure the census fingerprint test, re-derived in phase 4 — as at WI-045 and WI-044 phase 1.

### Phase 2 record — 2026-09-08

- `evidence/baseline_before/`: the three files are WI-045's `evidence/baseline_after/` copied — the package on disk is byte-identical to the one that executed them (commits B and C of WI-045 changed no package byte; `package_contract.json` reads `executable_fingerprint f5373d2d25f196cd…`), so a re-execution would reproduce them exactly; live: 126 channels, thirteen verdicts, LCOE 237.2528002420958, `cas72_calc__cost` 128437178.4450173.
- The predictions of record re-stated at that package state (§ Predictions above, `prototype/restate_at_wi045.py` → `proto_results_at_wi045.json`): the held mode `==` the oracle mirror and the landed channel (`held_equals_mirror: true` on 128,437,178.45); the live calendar's availability, count, dates, margin and ratio equal the design's entering-pin values to the double; CAS72 138,213,460.01 and LCOE 224.6095 are the prediction of record.
- The MR-WI046-15 restatement written above; commit A carries it, the model edits, the twins, the family restatement and this item's directory.

### Phase 3 record — 2026-09-08

- **Regeneration pass 1** (`evidence/regen_output.txt`): `Stencils - New: 1, Preserved: 72, Regenerated: 0` — the new manual stub `handwritten/mfe_lifecycle/lifecycle_calendar_impl.py`; no backup directory; the retired calc's module `modules/mfe_account_costs/levelized_replacement_cost.py` gone; the orphaned old impl left on disk by the generator and deleted by hand (the seal had been computed with it present — pass 2 re-sealed without it). **The caller's unpack order** (`modules/mfe_lifecycle/lifecycle_calendar.py:390`): `(availability, coil_life_margin_fpy, replacement_pv, planned_downtime_yr, terminal_downtime_yr, unplanned_downtime_yr, productive_fpy, dated_energy_ratio, cas72_annual, n_replacements, physical_life_fpy)` — not the declaration order (the WI-045 case again); the design's body restored on the stencil's `inputs.<field>` names (`q_n_in`, `fluence_limit_in`, `operational_years_in`, `outage_years_in`, `unplanned_fraction_in`, `cost_per_event`, `interest_rate`, `coil_life_fpy_in`, `availability_direct_in`) returning in the caller's order, recorded in the docstring.
- **Regeneration pass 2** (`regen_output_2.txt`): `New: 0, Preserved: 73, Regenerated: 0`, no backup, seal clean, the three manual impls (calendar, sustainment, cycle) byte-identical across the pass; **stale-stencil check** 50 AUTO checked / 4 manual skipped / **0 stale** (`evidence/stencil_check_output.txt`).
- **The contract:** eleven `calendar__*` channels; the four new entry keys; `availability` no longer an entry key and **not a separate channel** — the reference binding resolved to the producer, so `fuel_calc`, `lcoe_calc` and `lcoe_1cfe_calc` read `calendar__availability` directly (`pipeline.yaml` 815–1007; design D4's primary path, no fallback needed); semantic fingerprint `e6a7baa5a822b47b…`, sealed executable `e0d9b1ac19a440ff…`.
- **The oracle** (`verify_stellaris.py`): `IN` −`availability` +`availability_direct 0.0`, `outage_years 7/12`, `unplanned_fraction 0.0`, `coil_life_fpy 10.0`; `_oracle_lifecycle_calendar` written from the closed form `t_k = k·L/b + (k−1)·d` with the strict-restart rule and the year-binned energy ratio from D3's statement (the held mode through the existing mirror plus D2's readings); `compute()` calls it after the wall peak and reads its availability at the fuel, the two energy denominators and CAS72 — **the fuel block moved below the calendar** (it read `availability` before the calendar existed in the function's order; a text move, the value unchanged); the return dict +11 `calendar_*`. **The seam** (`oracle_entry.py`): the entry-key map −1 +4, the channel map +10 with `cas72_annual` → `calendar__cas72_annual`; `OPERAND_BINDINGS` untouched. **The route** (`study_route.py`): `AXES` / `BASELINE` / `proposal_for` / the sweep restated onto `availability_direct` (design D5) with the sweep's held-mode meaning stated. **The runner:** `run_stellaris.py` `CH["cas72"]` → the calendar channel; `_cas72_guard_gate` restated onto the held impl and the mirror (the three WI-029 cases verbatim, `coil_life_fpy` supplied) plus the fourth family — nine live boundary cases against the oracle's closed form on all eleven outputs, the time identity, `u` monotone — and the baseline's event dates printed in both modes; the oracle gate +11 channels; the anchors restated to the executed live values only after the gate read bit-exact (first run: anchors DEVIATION on LCOE / CAS70 / CAS80 / lcoe_1cfe as expected, parity 13 / `full_satisfaction`, oracle PASS on every channel, guards PASS; second run all green — `evidence/baseline_live/run_stellaris_single_output.txt`).
- **The held-mode identity** (`evidence/compat_mode/diff_vs_before.json`, `run_phase3_points.py`, the compatibility proposal `availability_direct 0.85` through `study_route.run_points` with the route's channels plus WI-045's twenty and the calendar's eleven): **126 of 126 channels of WI-045's live baseline bit-identical, 0 moved; the thirteen verdicts unchanged; LCOE 237.2528002420958**; the only channel gone `cas72_calc__cost`, whose 128437178.4450173 is `calendar__cas72_annual` exactly; the held readings `availability 0.85, n_replacements 5, productive 25.5, unplanned 4.5, ratio 1.0, coil margin −15.5, physical life 4.5239260339489915`.
- **The live baseline** (`evidence/baseline_live/`): 136 channels, thirteen satisfied, LCOE **224.60952472804465** — every calendar channel within 2.6e-16 of the prediction of record and of the oracle's closed form (`result.json` through the route; `baseline_result.json` + `package_identity.json` through `execute_baseline` after the re-pin; `events.json` live 4.5239 / 9.6312 / 14.7384 / 19.8457 / 24.9530 and held 5.3223 / 10.6445 / 15.9668 / 21.2891 / 26.6113).
- **A–D and E–F** (`evidence/offdesign_points/summary.json`, `events.json`; `evidence/stepping_points/`): A five months → six events, 0.9166666666666666, CAS72 149,568,478.49, LCOE 222.6047; B `u` 0.05 → 0.8576388888888891, 235.7568; C `u` 0.10 → 0.8125, 248.1039; D ten months → 0.8611111111111112, 235.0710 — all at 6.6e-16 or better against the predictions and the oracle. **E (`c3343`, R 17.2, a 1.8, peak 9.04) at the instance's fourteen loops `execution_failed`** — the loop's per-loop flow drives its pressure loss past the 8 MPa loop pressure and the compressor ratio's fractional power takes a complex root (WI-045's domain; `stepping_points/c3343_at_14_loops_execution_failed.json`), and the oracle seam raises a raw `TypeError` there instead of a declared invalid (a seam finding for the trail, not this item's); E re-run with the loop re-sized to 60 loops (every chain in domain; the calendar's count and availability do not depend on the loop count): **eleven replacements, availability 0.7861111111111112** as predicted, LCOE 143.80; F (`c7752`) five replacements, 0.8911741898870316 as predicted, LCOE 261.17 with `loop_capacity_ok` and `recirc_ok` violated at fourteen loops (WI-045's finding); the wall peak at E and F identical to the committed `20260907-minor-radius` record (relative deviation 0.0); oracle parity 2.0e-14 or better; worst deviation overall 2.04e-14.

### Phase 4 record — 2026-09-08

- **Re-pin by the producers** (`scratchpad/wi046_repin.py`; memory `gotcha_repin_after_regeneration`): the snapshot recaptured from the twin tree; `manifest.json` — indicator `19a97a940e68d3ec…`, executable `e0d9b1ac19a440ff…`, semantic `e6a7baa5a822b47b…`, the baseline point's `availability 0.85` → `availability_direct 0.0`, `baseline.headline.value` **224.60952472804465** from the executed live baseline, the `cas72` objective's channel `calendar__cas72_annual`, thirteen verdicts unchanged, `m.load()` validated; `mfe_census.json` re-derived: **232** entry points (229 − `availability` + `availability_direct`, `outage_years`, `unplanned_fraction`, `coil_life_fpy`), exactly the prediction; library defaults 51, usage literals 10, design attributes 171.
- **The axis and the fixtures** (design D5): `axes.known_answers.json` `availability` → `availability_direct` with its note restated; `availability.expected.json` moved to `availability_direct.expected.json`; the six fixtures re-derived by `scripts/study/indicators.py`; `test_known_answers.py` `CASES`, `EXPECTED_SEMANTIC_FINGERPRINT` and `FIXTURE_CONTRACT` restated **from the report** with a dated comment — the calendar's eleven outputs add ten tainted channels on every axis that reaches it (R, a 127 → 137; R+tie 132 → 142; I_coil 122 → 132; `availability_direct` 8 → 18; `interest_rate` 11 → 22 with 8 → 9 modules), the constraints unchanged, and `interest_rate` now reaches `fuel` (the trace is module-level: the calendar module takes the discount rate and produces the availability the fuel calc reads, though the executed live availability does not depend on the rate — the report's own not_derivable statement, recorded); `test_availability_reaches_no_constraint` → `test_availability_direct_reaches_no_constraint`, its claim kept (thirteen unreachable); `test_subset_flag.ALL_AXES`, `test_output_contract` (`by_axis`), `test_study_publication_fail_closed` (`_case`'s keys) and `test_operand_bindings` (`BASELINE_POINT`, `PINNED_LCOE` 237.2528002420958 → 224.60952472804465 with the history comment) restated. No verdict-count site moves (thirteen).
- **New test** `tests/models/test_lifecycle_calendar.py` (spec MR-WI046-12): the nine boundary cases against the closed form and the research's values, the held-mode `==`, and six invalid-input cases that must raise; needs `STOP_PARSER_TEAX_ROOT` (skips otherwise, as the runner's sealed-package import does).
- **Validation** (`evidence/validate_complete_after.txt`): unchanged from phase 1 (Level 2 the 12 placeholders; Level 6 252). **`tests/models`: 63 passed / 13 skipped.** The affected `tests/study` files cannot run before commit B (the git-clean gate refuses the uncommitted package tree — the WI-045 phase-4 note); they are phase 5's.
- **SV-066, SV-067, SV-068** added and `passing`; two trace rows (`'Lifecycle Calendar'`; the four instance bindings).
- Commit B: the regenerated package (the retired module and impl deleted), the new impl, the oracle, the seam, the route, the two runner files, the pin files (snapshot, manifest, census), the axes file and the six fixtures (one moved), the five restated study tests, the new models test, the two PM matrices, this item's `evidence/` and plan.

### Phase 5 record — 2026-09-08

- **The run of record** (`evidence/tests_study_run_of_record.txt`, one battery, detached with `setsid nohup` on the tree at commit B `9f6058f6`, polled with short foreground loops): **86 failed / 424 passed / 1 skipped in 11:36** — the entry count exactly; every failure in `test_study_publication_fail_closed.py` (the 75 pre-existing fail-closed cases + 11 for `20260907-minor-radius`), no other failing test, no errors. The eight restated and neighbouring files had already passed in isolation on the committed tree (107 passed / 1 skipped: `test_known_answers`, `test_operand_bindings`, `test_valid_empty`, `test_subset_flag`, `test_output_contract`, `test_verify`, `test_numeric_evidence`, `test_committed_store`); no test-file restatement was forced by the battery — WI-045's two late sites (`test_verify`, `test_numeric_evidence`) did not move for this item (no verdict added; the cycle channel unchanged).
- **A launch that did not fire, recorded:** the first detached launch was guarded by `pgrep -f 'pytest tests/study'`, whose pattern matched the tool shell's own command line (the recorded gotcha), so the guard refused and six minutes of polling read an absent file; relaunched with a bracket pattern (`[p]ython3 -m pytest tests/study`) — the one run above is the run of record. No second battery ran.
- **Commit C:** this plan and the run of record.
- The tree is handed to WI-047's plan (packet § 9); its `evidence/baseline_before/` is this item's `evidence/baseline_live/` (live: 136 channels, thirteen verdicts, LCOE 224.60952472804465, availability 0.9027777777777779; held: WI-045's 237.2528002420958 through the compatibility proposal `availability_direct 0.85`).

