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

- [ ] Write the four model edits from the design's text; keep `fuel_calc` reading `availability` (D4)
- [ ] `uv run agentic-mbse validate models` — Level 1 0 errors; Level 2 the pre-existing warnings only (12 at the WI-044 pin; WI-045 may have moved the count — take WI-045's phase record as the baseline); if the exact route rejects the forward reference `availability = calendar.availability` (risk 2), move the calendar block above the fuel block and record it
- [ ] `uv run agentic-mbse validate models --complete` → `prototype/validate_complete.txt`; compare Levels 4–6 with WI-045's run; the only expected delta is the retired def's own rows and the new def's
- [ ] Copy the changed files and the new file to their twins (`cp`); `cmp` clean; `diff -rq` between the trees shows no other difference
- [ ] `uv run python -m pytest tests/models -q` — expect WI-045's count or better; a test that names `'Levelized Replacement Cost'` or counts calc defs / modules by literal is restated from the live tree with a dated comment and recorded here

**Gate.** Levels 1–3 clean; twins identical; `tests/models` as expected with every delta explained.

## Phase 2 — The restatement and the predictions at WI-045's package state; `evidence/baseline_before/`; commit A

- [ ] `evidence/baseline_before/`: `study_route.execute_baseline(...)` on WI-045's package (unchanged by this item) → `baseline_result.json`, `package_identity.json` (remove `_work/`); the single runner's output → `run_stellaris_single_output.txt`; confirm `package_identity.json` carries WI-045's executable fingerprint
- [ ] Re-run `prototype/proto.py` against that baseline (its `cost_per_event` = the landed `blanket + divertor` capital) and write `## Predictions` below with the exact live values at WI-045's package state — the availability, count, dates, margin and ratio must equal the design's (they do not depend on WI-045); CAS72 and LCOE will differ and are stated here as the prediction of record
- [ ] Write `## MR-WI046-15 restatement` below: (a) the committed `cas72` and `availability` columns are the periodic chain's at held availability, never edited; (b) the held mode reproduces them at every point, the live mode differs at every point whose wall peak differs from the design point's and at the design point by the first-event timing; (c) no verdict is added by this item; the count sites stay at WI-045's 13; (d) the entry-point delta (`availability` out; `availability_direct`, `outage_years`, `unplanned_fraction`, `coil_life_fpy` in; census +3 net predicted) and the `cas72` objective's channel key change; (e) the round's study re-reads the inherited window in both modes and joins by case id to the committed `20260907-minor-radius` record
- [ ] **Commit A** with an explicit pathspec: the four model files, the ledger line, the twins, `work/active/WI-046_lifecycle-calendar/` (spec, design, plan, `prototype/`, `evidence/baseline_before/`); message names the restatement as preceding regeneration

**Gate.** The restatement and the predictions are in git before any regenerated byte.

## Phase 3 — Regeneration; the impl; the oracle, the seam, the route, the single runner; the held-mode identity; the live execution; A–F

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py` — NEW (the design's body on the stencil's names); `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` — DELETED; `verify_stellaris.py` — the calendar's closed-form derivation and the four `availability` sites (D1, § Changed); `studies/oracle_entry.py` — the levers and the eleven channels; `studies/study_route.py` — the axis rename (D5); `run_stellaris_single.py` — the guard gate restated (D9), the event-date print (D6); `evidence/baseline_held/`, `evidence/baseline_live/`, `evidence/offdesign_points/` — NEW.

- [ ] Regenerate:
  ```bash
  /home/reid/1cfe/fusion-tea/.venv/bin/sysml-codegen generate --models exploration/stellarator_e2e/models \
    --output exploration/stellarator_e2e/generated --package-name stellarator_tea \
    --overwrite --smart-regen --preserve-handwritten
  ```
  Expect `New: 1` (the calendar module and its stencil), the old CAS72 module gone, `Regenerated` on the plant module (its wiring changed) and nothing manual. Read the stencil's `inputs.<field>` names and the caller's unpack order from `generated/modules/mfe_lifecycle/lifecycle_calendar.py`; write the impl body from the design onto them; record the unpack order in the impl's docstring
- [ ] Delete `levelized_replacement_cost_impl.py` if the generator left it; `rm -rf generated/handwritten/backup/` if present; regenerate again — expect `New: 0, Preserved: N, Regenerated: 0`, the impl byte-identical, no backup dir, seal clean (`gotcha_codegen_manual_stage_regen`). **Any `Regenerated` on another manual-stage calc is a stop**
- [ ] Re-run WI-044's stale-stencil checker (`work/completed/20260908_WI-044_magnet-chain-sees-coil-bore/evidence/stencil_check.py`) over every AUTO_IMPLEMENTED impl: expect 0 stale (the plant module's wiring changed; its stencil must show the calendar's inputs)
- [ ] Read the eleven channel keys and the four new entry keys from `generated/contracts/model_contract.json`; confirm whether `availability` minted a producer channel or became a bare alias (D4); record which and, if the alias, apply the fallback and regenerate again
- [ ] `verify_stellaris.py` per design § Changed: `IN` −`availability` +the four; `_oracle_lifecycle_calendar` from the closed form (D1) with the held mode through the existing mirror and D2's readings; `compute()` reads `cal["availability"]` at the four sites and `cal["cas72_annual"]`; the return dict +11. Written from the design's statement, not from the impl
- [ ] `oracle_entry.py`: the levers, the eleven channels, the `cas72` objective channel; `OPERAND_BINDINGS` unchanged
- [ ] `study_route.py`: `AXES`, `BASELINE`, `proposal_for`, the availability sweep restated onto `availability_direct` (D5) with a dated comment; `manifest.json`'s `axes` / tie data restated in phase 4
- [ ] `run_stellaris_single.py`: `_cas72_guard_gate` restated — the three synthetic guard cases against `lifecycle_calendar_held` and the mirror; a fourth family of live boundary cases (`L 4, d 7/12, N 10 / 8.7 / 9.1667 / 9.1667+1e-6`; `q_n 0`; no outage; `i 0`; `u` monotone) against the oracle's closed form and the research's expected values; the baseline's event dates printed in both modes; `EXPECTED_VERDICT_COUNT` unchanged by this item (13 after WI-045)
- [ ] **Held-mode identity:** with the instance's `availability_direct` temporarily overridden to `0.85` through the route's proposal (never by editing the instance), execute the baseline → `evidence/baseline_held/baseline_result.json`; diff against `exploration/stellarator_e2e/studies/20260907-minor-radius/results/baseline_result.json` restricted to the channels WI-045 did not move (and against WI-045's `evidence/baseline_after/` for the ones it did): **every channel bit-identical; the eleven new channels at D2's held values; the verdicts unchanged** — record the diff here. **If any channel moves, stop and derive why before continuing** (`goal.md` § Invariants)
- [ ] **Live execution:** the instance as bound → `evidence/baseline_live/baseline_result.json` and `events.json`; compare the eleven channels with `## Predictions` (1e-9 relative); the single runner's output → `evidence/baseline_live/run_stellaris_single_output.txt` with verdict parity and the oracle gate passing (0.0 on all eleven)
- [ ] Execute A–D (the calendar levers moved at the baseline) and E–F (`c3343`, `c7752` in the committed record's `point()` shape) through `study_route.run_points`; deposit `evidence/offdesign_points/results.json` and `events.json`; compare with `proto_results.json` (E and F re-run in the prototype on the executed `cost_per_event`); every non-calendar, non-availability-consuming channel at E and F equal to the entering pin's value at the same coordinates (or WI-045's, for the channels it moved)

**Gate.** The held-mode identity holds; the live prediction holds with oracle parity; the boundary cases pass; A–F agree.

## Phase 4 — Re-pin, the axis and fixture, batteries, SV and trace rows; commit B

**Files.** `stellarator.snapshot.json`, `studies/manifest.json`, `tests/models/data/mfe_census.json`, `tests/study/data/axes.known_answers.json`, `tests/study/data/availability.expected.json` → `availability_direct.expected.json`, the other five fixtures, `tests/study/test_known_answers.py` — RE-DERIVE / RESTATE; `modeling_project/VALIDATION_MATRIX.md`, `data/traceability_matrix.csv` — via `pm` ops.

- [ ] Snapshot recaptured from the twin tree
- [ ] `manifest.json`: the three fingerprints from the package's contracts (`files` as path strings); `baseline.verdicts` unchanged by this item (13); the `cas72` objective's channel `calendar__cas72_annual`; the axis block renamed; `baseline.headline.value` re-pinned from the executed **live** LCOE (the pin is the package as bound: live); `m.load(manifest)` validates
- [ ] `mfe_census.json` re-derived (`integ.rederived_census(pkg)` + the new semantic fingerprint); expect +3 net (`availability` out; four in) — record the actual count and delta
- [ ] `axes.known_answers.json`: `availability` → `availability_direct`; the six fixtures re-derived via `scripts/study/indicators.py`; `EXPECTED_SEMANTIC_FINGERPRINT`, `FIXTURE_CONTRACT` and `CASES` restated **from the report** with a dated comment (predicted: `availability_direct` reaches `cas72`, `fuel`, `lcoe`, `lcoe_1cfe` and no constraint — the held-mode response; `a`, `R`, `R+tie`, `I_coil` newly reach the eleven calendar channels through the wall peak; `interest_rate` reaches `calendar__replacement_pv` and `cas72_annual`); `test_availability_reaches_no_constraint` docstring restated (D5)
- [ ] Any literal count the batteries find restated from the live package with a WI-046 comment; the verdict-count sites must not move
- [ ] `uv run agentic-mbse validate models --complete` — compare with `prototype/validate_complete.txt`; record any new residue
- [ ] `tests/models` — WI-045's count or better; every delta explained; add `tests/models/test_lifecycle_calendar.py` importing the impl's two mode functions and the oracle's closed form on the research's boundary cases (MR-WI046-12)
- [ ] `rm -rf .integration_workspace`; `tests/study` — expect green apart from the branch's known fail-closed cases (75 at entry plus the per-record cases the newest records add); every other delta explained
- [ ] `pm add-validation` ×3 then `pm update-validation … --status passing` with the evidence paths: SV-063 the held-mode identity (every channel bit-identical at `availability_direct` 0.85; CAS72 126,649,655.78572692; the eleven held readings); SV-064 the live calendar at the design point (availability 0.9027777777777779, five events at the stated dates, CAS72 and LCOE at the prediction of record, oracle parity 0.0, the closed form and the walk agreeing); SV-065 the boundary cases (the research's synthetic values reproduced by the impl and the oracle; the time identity; `u` monotone; the six-at-five-months step)
- [ ] `pm trace-element` for `'Lifecycle Calendar'` (`mfe_lifecycle.sysml`, type calc) and the four instance bindings
- [ ] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified — below)
- [ ] **Commit B** with an explicit pathspec: the regenerated package (including the deleted impl), the new impl, the oracle, the seam, the route, the single runner, the pin files, the fixtures and the two test files, the SV/trace rows, `evidence/baseline_held/`, `evidence/baseline_live/`, `evidence/offdesign_points/`, this plan; never `git add -A`
- [ ] Note for the modelling PM: the BACKLOG row moves at close through `pm close-item`; the epic file's item note is owner-facing

**Gate.** Both batteries as expected with every delta explained; no expectation patched to match; SV-063..065 `passing`.

## Phase 5 — The `tests/study` run of record; commit C

- [ ] After commit B, `tests/study` on the clean tree (detached; ~11 min last time); record the count and the failing set; confirm the failing set equals the pre-existing fail-closed set or explain every difference
- [ ] **Commit C**: any test-file restatement the run forced, and this plan's phase-5 record

---

## Feasibility concerns

1. **The reference redefinition mints no channel** (risk 1). *Mitigation:* D4's fallback, recorded in phase 3.
2. **The forward reference in the plant** (risk 2). *Mitigation:* Levels 1–3 in phase 1 before the twins; a text move if needed.
3. **The deleted impl leaves a backup or a stale plant stencil.** *Mitigation:* the two-pass recipe and the stale-stencil checker.
4. **The single-runner gate's import of the old impl** breaks at regeneration until restated. *Mitigation:* restated in the same phase before the runner executes.
5. **WI-045 has not landed when this plan starts.** *Mitigation:* phase 1's precondition; this item waits (packet § 9).

---

## MR-WI046-15 restatement — the comparison meaning at the new pin

*(Written in phase 2, before commit A.)*

## Predictions — the calendar channels at the baseline and at A–F

*(Written in phase 2 from `prototype/proto_results.json` re-run at WI-045's package state, before commit A; the design's table at the entering pin's values is the cross-check.)*

## Spec success criteria, verified

*(Written in phase 4.)*

## Phase records

*(Appended as each phase closes.)*
