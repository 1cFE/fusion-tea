---
Status: active
Created: 2026-09-04
Updated: 2026-09-04
Related Artifacts:
  Spec: ./spec.md
  Design: ./design.md
---

# WI-041 Plan — building the source-anchored wall-load fence

## Source documents

Design (primary): `./design.md`. Spec: `./spec.md`. Epic: `work/backlog/epic-mfe-cost-modeling.md` § Item WI-041. Governing goal task: `work/orchestration/goals/wall-and-heating/trail.md` § T-002 scope (round 2). Evidence of record: `work/orchestration/goals/wall-and-heating/evidence/round2_T-001_source_basis.md`.

## Design summary

Two library calcs — a calibration computed from six printed source facts, and the peak as the average times it — move the wall chain up to the generic plant (D1) so the fence and the lifetime calc both read one peak; the lifetime calc takes the wall load as an explicit input bound to the peak (D2); the calibration's decomposition lives in doc text (D3); the constancy assumption is stated (D4); the three stale doc comments ride the regeneration (D5). Rationale and the rejected alternatives are in the design; they are not repeated here.

## Prototype baseline

`models/library/analyses/mfe_plasma_scaling.sysml:257-339` holds both calc defs and passes Level 1 with 0 errors and 0 warnings across 25 files; Level 2 shows the two expected `Unused calc def` warnings and the 12 pre-existing placeholder bindings (design § Prototype and validation report). The prototype is not yet copied to its twin. It needs no syntax refinement; it needs consumers.

## Phasing approach

Library before instances; the restatement **before** the regeneration commit; the expensive, irreversible regeneration last. Six phases in two commits:

- **Commit A (phases 1–4):** the model edits in both trees, the doc corrections, and the restatement — the tree is model-complete and the restatement is on the record **before** any regeneration is committed (MR-WI041-11; the round-1 ordering deviation is not repeated).
- **Commit B (phases 5–6):** regeneration, the handwritten impl, the oracle, the re-pin, the fixtures, the batteries, the SV rows.

Why the restatement sits in phase 4 and not phase 6: it is a statement about *meaning*, derivable from the design's expected-behaviour table before any number is generated, and writing it after regeneration invites fitting it to what came out.

## Validation strategy

Levels 1–3 after every model phase; full Levels 1–6 and both batteries in phase 6. Environment, confirmed in this session:

```bash
set -a; source ~/1cfe/agentic-mbse/.env; set +a
uv run agentic-mbse validate models
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env \
  sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated \
  --package-name stellarator_tea --overwrite --smart-regen --preserve-handwritten
uv run python -m pytest tests/models -q
rm -rf .integration_workspace
uv run --env-file ~/1cfe/agentic-mbse/.env --env-file .venv/integration.env python -m pytest tests/study -q   # ~7.5 min
```

Every canonical file under `models/` edited here is copied byte-for-byte to its twin under `exploration/stellarator_e2e/models/` in the same phase (`tests/models/test_model_family_spines.py` fails on any drift).

---

## Phase 1 — Library: the two new calcs, the lifetime calc's operand, two doc texts

**Overview.** Finish the library side. The two new calc defs exist; the lifetime calc's interface changes to take the wall load; the constraint def and the heating chain get their doc corrections.

**Design reference.** § Proposed design → "New: `calc def 'Neutron Wall Load Peak Calibration'`", "New: `calc def 'Neutron Wall Load Peak'`", "Changed: `calc def 'Levelized Replacement Cost'`", "Changed: `constraint def 'Neutron Wall Load Limit'`", "Changed: `mfe_heating_chain.sysml:30-35`"; decisions D2 and D5.

**Files.**
- `models/library/analyses/mfe_plasma_scaling.sysml` — REFINE (review the prototype against the design table)
- `models/library/analyses/mfe_account_costs.sysml` — REFINE
- `models/library/analyses/mfe_viability.sysml` — REFINE (doc only)
- `models/library/analyses/mfe_heating_chain.sysml` — REFINE (doc only)

**Checklist.**
- [x] Re-read the two prototype calc defs against the design's table; confirm names, the two defaulted formals last, the three expressions
- [x] `mfe_account_costs.sysml` 'Levelized Replacement Cost': replace `in p_fus`, `in ash_frac_in`, `in firstwall_area` with `in attribute q_n_in : Real;`; drop the chain's first two lines from the doc and the WI-029 "neutron power INSIDE this calc" comment; say the operand arrives computed and that the plant binds the peak, with the source's reason
- [x] `mfe_viability.sysml` 'Neutron Wall Load Limit': doc says the operand is the computed peak and the limit the printed peak, same basis; Ref adds Table 6's lifetime rows
- [x] `mfe_heating_chain.sysml:30-35`: the EI-5 sentence
- [x] Copy all four files to their twins
- [x] `uv run agentic-mbse validate models` — Level 1 clean; Level 2 no new warnings beyond the two unused defs

**Validation checkpoint.** Level 1: 0 errors. **Gate.** The calc defs' formal names are exactly the design's binding table; a rename here costs three files later.

---

## Phase 2 — Generic plant: the wall chain moves up, the lifetime calc reads the peak

**Overview.** The generic plant grows the three-calc wall chain with seven dormant-safe attributes, rebinds `cas72_calc`, and retires `ash_frac`.

**Design reference.** § Proposed design → "Changed: `models/designs/generic_mfe/mfe_plant.sysml`" (the stencil); § Cross-file bindings; decisions D1, D2.

**Files.** `models/designs/generic_mfe/mfe_plant.sysml` — REFINE.

**Checklist.**
- [x] After the `fusion` calc (`:330-340`): the seven `wall_peak_*` attributes with the dormancy comment, then `wall_load_calc`, `wall_peak_cal`, `wall_peak_calc` exactly as the design stencil — **attribute references and calc outputs only, no expressions in bindings**
- [x] `cas72_calc` (`:898-907`): `in q_n_in = wall_peak_calc.wall_load_peak;` replaces `in p_fus`, `in ash_frac_in`, `in firstwall_area`
- [x] Remove `attribute ash_frac : Real default 0.2002;` (`:889-893`) and its comment; grep the plant for any other reader
- [x] Copy to the twin
- [x] `uv run agentic-mbse validate models` — Levels 1–3

**Validation checkpoint.** The two `Unused calc def` warnings are gone; no unbound inputs. **Gate.** No reader of `ash_frac` remains under `models/` except the sustainment calc's own `sustain__ash_frac_in`, which is not this item's.

---

## Phase 3 — Stellaris instance: the six source facts, the fence, the exposed quantities, the doc corrections

**Overview.** Bind the source, rebind the fence to the peak, expose the peak and the calibration, and correct every stale comment this item owns.

**Design reference.** § Proposed design → "Changed: `models/designs/stellarator_09/stellarator_plant.sysml`" (each bullet is one checklist item below); decisions D3, D4, D5; § Expected baseline behaviour.

**Files.** `models/designs/stellarator_09/stellarator_plant.sysml` — REFINE.

**Checklist.**
- [x] Delete the instance's `calc wall_load_calc` block (`:1149-1152`) — the generic one is inherited under the same name
- [x] Delete `:>> ash_frac = 0.2002275312855518` (`:1100-1110`) with its doc (D2)
- [x] Bind the six reference facts and zero the direct term, each with its page-image citation (`wall_peak_q_ref` 4.05; `wall_peak_p_fus_ref` 2700.0; `wall_peak_R_ref` 12.7; `wall_peak_a_ref` 1.3; `wall_peak_kappa_ref` 1.0; `wall_peak_standoff_ref` 0.10 with the minimum-vs-averaged standoff note; `wall_peak_calibration_direct` 0.0)
- [x] `wall_peak_q_ref`'s doc carries D3's decomposition cross-check (1.77 → ~945 m²; the external band → 800–1120 m²; 4.05 / 2.87 is not a peaking factor) and D4's meaning for this machine
- [x] Rewrite the cross-check comment block (`:1126-1143`) to what T-001 established; the disclosed baseline: peak 4.088 against 4.05, **violated**
- [x] `wall_load_limit`'s doc: drop the 4.95 hedge; cite the Table 2 image and the Table 5 image's absence of a peak row
- [x] `wall_load_ok`: `in wall_load = wall_peak_calc.wall_load_peak;` with a comment stating the disclosed verdict and that it is never tuned
- [x] Expose `neutron_wall_load_peak` and `wall_peak_calibration` beside `neutron_wall_load` (`:1192`)
- [x] `:700,703`: the archived WI-039 design path
- [x] Copy to the twin
- [x] `uv run agentic-mbse validate models` — Levels 1–3; `uv run python -m pytest tests/models -q` (expect the spine test green on the synced twins; the census test will fail until phase 6 and says so)

**Validation checkpoint.** Levels 1–3 pass. **Gate.** Every one of the six bindings cites a page image, not a text line (spec MR-WI041-10).

---

## Phase 4 — The restatement, written before regeneration

**Overview.** State what changes meaning, for every committed study, from the design's expected-behaviour table — before any generated number exists. This phase produces text only and is committed with phases 1–3 as **commit A**.

**Design reference.** § Expected baseline behaviour; decisions D1 (the census), D2 (the retired entry point and the convention change); spec MR-WI041-5, MR-WI041-6, MR-WI041-11.

**Known surface, mapped before starting** (grep of `wall_load_calc__wall_load|wall_load_ok|cas72|ash_frac`, 2026-09-04):

| file | what it is | what happens |
|---|---|---|
| `studies/20260829-p-pump-fence`, `20260830-stress-fence`, `20260901-sustainment-fence`, `20260903-priced-levers`, `20260903-wall-and-heating`, `20260821-power-cycle-ab`, `20260823-magnet-technology-ab` (`study.py`, records) | read the wall-load channel and/or `cas72`; their `wall_load_ok` verdicts were average-vs-peak | **restated, not re-run**: a wall-load column re-reads through the calibration (peak = average × 1.316441 at the reference geometry); `wall_load_ok` re-reads as peak ≤ 4.05; `cas72` does not re-read and stands at its pin; the `20260903-wall-and-heating` shadow columns are superseded by the fence |
| `exploration/stellarator_e2e/studies/manifest.json` | baseline verdict `wall_load_ok: satisfied`; the recorded fingerprints; no `ash_frac` key | the verdict flips to `violated` **with its derivation beside it**; fingerprints re-pinned in phase 6 |
| `studies/oracle_entry.py` | entry keys and channels | `ash_frac` key retired; seven `wall_peak_*` keys and two channels added |
| `tests/models/data/mfe_census.json` | 199 entry points | re-derived from a live generation: −1 (`ash_frac`) + 7 = 205 expected |
| `tests/study/data/{R,a,I_coil,R+tie,availability,interest_rate}.expected.json`, `test_known_answers.py` | bound to the semantic fingerprint | re-derived by running the tool; the fixture-binding fingerprint updated; `FIXTURE_CONTRACT` re-read (the `cas72` reach now passes through the two new modules) |
| `exploration/stellarator_e2e/onecfe_point.json`, `emit_1cfe_point.py`, `handshake_1costingfe.py` | the broken 1costingFE handshake | untouched; the keys it would need are noted |

**Checklist.**
- [x] Write `## MR-WI041-11 restatement` at the end of this plan: (a) the fence's meaning change and the one multiplier that re-reads a committed wall-load column; (b) the lifetime operand's change, why CAS72 does not re-read, and the D2 convention change (0.79977 → 0.7998, 3.4 × 10⁻⁵); (c) the disclosed baseline verdict and its derivation (4.05 × 2725.363 / 2700 = 4.088 > 4.05); (d) the declared CAS72 and LCOE moves; (e) per-study statements for the seven studies above, including that the `20260903-wall-and-heating` shadow columns are superseded; (f) the census and entry-key changes
- [x] ~~Write a dated restatement note into the two record dirs~~ **Not done as written, by decision before execution:** committed study records are append-only under the study runbook and WI-039's precedent kept its restatement in the plan (§ MR-WI039-9) with no file added to any record dir; the restatement below names both studies and the round trail cites it
- [x] **Commit A**: the four library files, the two plants, the twins, this plan through phase 4, the spec, the design; message names the restatement as preceding regeneration — `df6dc964`

**Gate.** `git log` shows commit A before any regeneration commit.

---

## Phase 5 — Regeneration, the handwritten impl, baseline parity, the oracle

**Overview.** Generate, edit the preserved impl to the new signature, execute at the baseline, prove the expected-behaviour table, then write the oracle's own chain and the perturbation test.

**Design reference.** § Proposed design → "Changed: `calc def 'Levelized Replacement Cost'`" (the impl signature), "Changed: `verify_stellaris.py` and `oracle_entry.py`"; § Expected baseline behaviour; § Validation plan items 2–7.

**Files.** `exploration/stellarator_e2e/generated/**` — REGENERATE; `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` — REFINE (by hand); `exploration/stellarator_e2e/verify_stellaris.py` — REFINE; `exploration/stellarator_e2e/studies/oracle_entry.py` — REFINE.

**Checklist.**
- [x] Regenerate with `--smart-regen --preserve-handwritten`; confirm exit 0, the two new modules, the lifetime wrapper's `q_n_in`, and the impl preserved byte-identical (then edited)
- [x] Edit the handwritten impl: `levelized_replacement_cost(cost_per_event, q_n, fluence_limit, availability, interest_rate, operational_years)`; drop the two neutron-power lines; `run_…` reads `inputs.q_n_in`; docstring says the operand is the peak and why
- [x] `exploration/stellarator_e2e/run_stellaris_single.py` (found while mapping callers): its three synthetic CAS72 guard cases call the old signature — restate each with `q_n = p_fus × (1 − ash_frac) / firstwall_area` at the same values so every guard stays live; `EXPECTED_VERDICTS["wall_load_ok"]` → `violated` with the derivation; the nine anchors (LCOE, CAS70) re-pinned from the executed baseline **after** oracle parity, never before
- [x] Execute at the baseline (`study_route.execute_baseline` through the seam's route, or `run_stellaris_single.py`); record every row of the expected-behaviour table with before/after — **the average bit-identical, the calibration 1.316440857, the peak 4.088044684, `wall_load_ok` violated, CAS72 131,494,480, LCOE moved by ΔCAS72 / annual MWh, everything else identical**
- [x] **If any other value moves, stop and derive why before continuing** (`goal.md` § Invariants)
- [x] Oracle: add the six facts and the direct term to `IN`, drop `ash_frac`; compute `A_ref`, `p_n_ref`, `calibration`, `wall_load_peak` **from the design's table with the generated module closed**; `_oracle_levelized_replacement_cost` takes `q_n`; return `wall_peak_calibration` and `wall_load_peak`
- [x] `oracle_entry.py`: seven entry keys added, `ash_frac` removed, two channels mapped
- [x] Parity at the baseline: average, calibration, peak, CAS72, LCOE
- [x] **Perturbation:** `wall_peak_q_ref` 4.05 → 4.50 alone; confirm the calibration, the peak, the fence margin, CAS72 and LCOE move in both model and oracle and the average does not; restore 4.05; record the numbers
- [x] **Identity from channels:** `neutron_wall_load_peak × 2700 / p_fus = 4.05` to float precision at the baseline; record it

**Gate.** Model and oracle agree on every row; the identity holds; the perturbation moves both together. If the oracle disagrees, find out which is wrong before touching either.

---

## Phase 6 — Re-pin, fixtures, batteries, SV and traceability rows

**Overview.** Bring every pinned artifact to the new package by running the producers, never by editing numbers.

**Design reference.** Phase 4's surface table; spec MR-WI041-5, MR-WI041-10; § Validation plan item 8.

**Checklist.**
- [x] Recapture `exploration/stellarator_e2e/stellarator.snapshot.json` (`sysml_codegen.snapshot.capture.capture_instance_graph_snapshot`, the producer the seam's gate 4 uses)
- [x] `manifest.json`: the three fingerprints re-pinned from the package's contracts; `baseline.verdicts` `wall_load_ok` → `violated` **with the derivation in a `note`**; `baseline.headline.value` re-pinned to the executed LCOE
- [x] `tests/models/data/mfe_census.json` re-derived from a live generation (expect 205; record the retired and minted keys)
- [x] Six `tests/study/data/*.expected.json` re-derived by running the reachability tool; `test_known_answers.py`'s fingerprint and `FIXTURE_CONTRACT` re-read from the live report, with the comment saying what moved and why
- [x] `uv run agentic-mbse pm add-validation` ×3: the design-point identity; the disclosed verdict change; lifetime-by-peak inside the source's ~4–6 FPY band. Then `pm update-validation SV-0xx --status passing` for each with the evidence
- [x] `uv run agentic-mbse pm trace-element` for the two new calc defs
- [x] Full `uv run agentic-mbse validate models` — Levels 1–6; 4–6 reviewed; any new residue recorded
- [x] `tests/models` — expect 48 passed / 13 skipped or better, every delta explained
- [x] `rm -rf .integration_workspace`; `tests/study` — expect 359 passed / 1 skipped or better, every delta explained (first run on the uncommitted tree: 16 failed / 24 errors, all but two the git-clean gate and one my shell's `PYTHONPATH` leaking into a negative test; the two genuine sites below fixed; the run of record is after commit B — see the phase-6 record)
- [x] Verify each spec success criterion and record where its evidence is (§ Spec success criteria, verified)
- [ ] **Commit B**: the regenerated package, the impl, the oracle, the pin files, the fixtures, this plan

**Gate.** Both batteries green with every delta explained; no expectation patched to match.

---

## Feasibility concerns

1. **Codegen refuses the moved usage or the dormant arithmetic.** *Mitigation:* the form matches WI-039's accepted chain; a refusal is a `MECHANICAL_FAILURE` with a retry, and the form is not changed to dodge the tool.
2. **The lifetime wrapper's regenerated schema and the hand-edited impl disagree on a field name.** *Mitigation:* read the regenerated `Levelized_Replacement_CostInput` before editing the impl; `generated/tests/test_implementations_runnable.py` catches a mismatch.
3. **`tests/study` costs ~7.5 minutes per run.** *Mitigation:* run it once at the end of phase 6.
4. **The census count differs from 205.** *Mitigation:* it is re-derived, not asserted; the number here is a prediction and the phase record says what it actually is and why.


---

## Phase records

### Phases 1–3 — 2026-09-04

Library, generic plant and Stellaris instance edited as designed; every canonical file copied byte-for-byte to its twin (`diff -rq` clean on both trees). `uv run agentic-mbse validate models --complete`: Level 1 0 errors / 0 warnings over 25 files; Level 2 exactly the 12 pre-existing placeholder bindings (no unused definition, no unbound input); Levels 3, 4, 5 pass; Level 6 237 issues against 230 at HEAD (measured on a `git archive HEAD models` copy in the scratchpad): design attributes checked 200 → 208 (seven `wall_peak_*` attributes and two exposed peak attributes minted, `ash_frac` retired), `L6_DESIGN_ATTR_UNEXTRACTABLE` 58 → 60, `L6_DESIGN_ATTR_INCOMPLETE` unchanged at 105, every other printed counter unchanged at 0; the validator itemizes only five issues even with `--verbose`, so the remaining five of the seven are not attributable line by line from its output — no new error kind appears in the printed counters. Recorded as residue, not resolved: the same classes carry the cryo-chain and heating-chain siblings. No test battery run yet: the census and known-answer fixtures are bound to the old fingerprint by design and are re-derived in phase 6.

One deviation from the design's stencil, recorded: none. One item retired beyond the design's list: none — `ash_frac` (generic and instance) retired as D2 says; grep confirms no reader remains except `sustain__ash_frac_in`.

---

## MR-WI041-11 restatement — the fence's meaning change and the committed studies (2026-09-04, written before regeneration)

**Ordering.** This section is committed with the model edits (commit A) and before any regenerated byte (commit B). The round-1 T-002 wrote its restatement after regenerating and recorded that as a deviation; this item does not repeat it.

### (a) What the fence now means, and the one multiplier that re-reads a committed wall-load column

Before WI-041, `wall_load_ok` compared the circular-torus **average** (`neutron_wall_load`, neutron power over `kappa·4π²·R·(a + 0.10)`) with the source's printed **peak** limit 4.05. After WI-041 it compares the computed **peak**: the same average times a calibration computed at the source's design point,

    calibration = 4.05 × [1.0 · 4π² · 12.7 · (1.3 + 0.10)] / [2700 × (1 − 0.2002)] = 4.05 × 701.926265 / 2159.46 = 1.316440857.

The average itself is untouched (bit-identical at the baseline: 3.105376639). Because the calibration is constant over every lever (design D4), **any committed wall-load column re-reads exactly**: peak = 1.316440857 × average, and the fence re-reads as peak ≤ 4.05, i.e. **average ≤ 3.076481 MW/m²**. No committed study needs re-execution to re-read its wall verdicts; a reader applies the multiplier to the `wall_load` column. This is the sharpening of the shadow columns the `20260903-wall-and-heating` study carried (net 1.15× and 1.83× bounds on the same average): the fence's multiplier, 1.3164, sits inside that band, and the shadow columns are **superseded** by it.

### (b) The lifetime operand, why CAS72 does not re-read, and the convention change

`'Levelized Replacement Cost'` no longer computes its own `q_n = p_fus × (1 − ash_frac) / wall_area`; it takes `q_n_in`, and the plant binds the **peak**. A committed `cas72` column does **not** re-read by a multiplier: the core life is `clip(18 / q_n, 0.5, 25.5)` full-power years and the replacement count `ceil(30 / (life / 0.85)) − 1` is a step function, so a 1.316× move in the operand changes both the interval and the count discontinuously. Committed `cas72` values stand at their own pins; only re-execution at the new pin gives the new values.

The retired exact `ash_frac` (0.2002275312855518) fed only this calc. Its retirement moves the lifetime chain's neutron fraction to the average's 0.7998, a 3.4 × 10⁻⁵ relative change on the operand, folded into the move in (d). Recomputed from the recorded baseline, CAS72 at the average with 0.2002 would read 95,901,232 against the recorded 95,898,253 — that is the whole convention effect.

### (c) The disclosed baseline verdict and its derivation

At the baseline geometry (R 12.7, a 1.3, kappa 1.0, standoff 0.10) the model's reference area equals the source's, so the peak reduces to the source's peak scaled by fusion power:

    peak = 4.05 × p_fus / 2700 = 4.05 × 2725.3631229 / 2700 = 4.088044684 MW/m² > 4.05.

**`wall_load_ok` at the baseline flips `satisfied` → `violated`**, by the model's 0.94 % fusion-power excess over the source's ~2700 MW — the result the round-2 strategy expected, and a first-class result on the `sustainment_ok` precedent. The manifest's `baseline.verdicts` entry carries this derivation as a note when it is flipped in phase 6; nothing is adjusted to keep the baseline feasible (spec MR-WI041-5).

### (d) The declared CAS72 and LCOE moves

From the calc's own equations at the pinned constants (fluence limit 18, i 0.07, N 30, availability 0.85, cost per event 828,544,559.61):

| | before | after |
|---|---|---|
| lifetime operand [MW/m²] | 3.105271 (average, exact ash) | 4.088045 (peak) |
| core life [FPY] / [cal-yr] | 5.7964 / 6.8193 | 4.4031 / 5.1801 |
| scheduled replacements | 4 | 5 |
| `cas72_calc__cost` [$/yr] | 95,898,253 | 131,494,480 (+35,596,226; +37.1 %) |
| `lcoe_calc__lcoe` [$/MWh] | 307.08712043 | + ΔCAS72 / annual MWh — derived at phase 5 from the executed baseline and recorded there |

Everything upstream of CAS72 — fusion power, every capital account, the heating chain, the other eight verdicts — is predicted bit-identical; phase 5 checks the prediction and derives any surprise rather than fitting it.

### (e) The committed studies, one by one

Every committed study's `wall_load_ok` column was average-vs-peak and re-reads through (a); every `cas72` column stands at its pin per (b).

- **`20260903-wall-and-heating`** (record § 4, § 15 #1, #3; the shadow columns `wall_load_shadow_lo/hi`, `wall_load_ok_shadow_lo/hi`, `feasible_shadow_lo` in `results/points.csv`): the fence's multiplier 1.3164 supersedes the 1.15× / 1.83× shadow bounds. The reviewer's count under 1.316 (26 of 91 feasible 220 MW points survive; cheapest 371.005, `c0584`) is the re-read of this study under the fence, subject to the (b) caveat that the survivors' `cas72` and LCOE columns are at the old lifetime operand. Round 2's study re-executes at the new pin. Its `cas72` column (1 mention) stands.
- **`20260903-priced-levers`** (§ 15 #1: `wall_load_ok` violated 264/439; 27 of 240 blocked by the wall alone at 50 MW): re-reads through (a) — points at average ≤ 3.0765 pass the fence; the deadlock reading it grounded is strengthened, not weakened, because the fence tightens.
- **`20260901-sustainment-fence`**, **`20260830-stress-fence`**: `wall_load_ok` columns re-read through (a); no `cas72` reading.
- **`20260829-p-pump-fence`** (`synthesis.md:49-50,69`: `wall_load_ok` violated at every a ≥ 1.70, 4.16469 at a = 1.70 against 4.05): re-reads through (a) — under the peak the boundary moves to average ≤ 3.0765, so the a-threshold moves inward; the constancy-in-R observation was at a pre-WI-037 pin and does not transfer regardless. Its two `cas72` readings stand.
- **`20260821-power-cycle-ab`**, **`20260823-magnet-technology-ab`**: `wall_load_ok` and `cas72` readings stand at their pins (pre-migration and pre-WI-030 packages; not reproducible as written already, per the MR-WI036-11 / MR-WI037-7 restatements); the (a) re-read applies to their wall columns if anyone re-reads them.

No committed record, snapshot, `results/` file or `DISCOVERY_LOG.md` row is edited by this item; a disposition row for the two routed findings (`20260903-priced-levers#1`, `20260903-wall-and-heating#1`, `#3`) is the round result's, after the round's study reading.

### (f) The census and the entry keys

One entry point retires (`stellarator_09__stellaris__ash_frac`; not swept by any committed study — grep of every `axes.json`, `study.py` and fixture is empty) and seven are minted (`stellarator_09__stellaris__wall_peak_q_ref`, `…p_fus_ref`, `…R_ref`, `…a_ref`, `…kappa_ref`, `…standoff_ref`, `…calibration_direct`): 199 → 205 predicted; `tests/models/data/mfe_census.json` is re-derived from the live generation in phase 6, and the phase record states the actual count. `oracle_entry.py` maps the seven keys and drops the one; two channels (`wall_peak_calc__wall_load_peak`, `wall_peak_cal__calibration`) are added. The six known-answer fixtures are re-derived by running the reachability tool; the `cas72` reach now passes through the two new modules, so `FIXTURE_CONTRACT`'s trace sizes for `R`, `R+tie`, `a` and `I_coil` are expected to grow by two modules — read off the live report, never typed.


### Phase 5 — 2026-09-04

**Regeneration, twice — a gotcha worth recording.** The first `sysml-codegen generate --smart-regen --preserve-handwritten` reported `New: 2, Preserved: 65, Regenerated: 1`: the two new modules were stencilled and auto-implemented (their arithmetic matches the design table line for line), and the lifetime calc's handwritten impl was **re-stencilled to a `NotImplementedError` stub** because its interface changed, the old body moved to `handwritten/backup/levelized_replacement_cost_impl_20260904_120019.py`. The package is sealed at generation, so a hand edit afterwards reads as a seal violation (`TAMPER` on the impl, `MISSING` on the backup once removed) and the package will not load. The working sequence: restore the guarded chain by hand on the new signature, delete the codegen's backup directory (the old body is in git at `df6dc964` and every earlier commit), then regenerate **again** — `New: 0, Preserved: 68, Regenerated: 0`, the impl byte-identical through the second run, no backup directory recreated, seal clean. The seam's `handwritten-lost` condition is exactly this stub; a manual-stage interface change always needs the second regeneration.

**Baseline parity, every row of the design's table** (`study_route.execute_baseline` at the regenerated package, executable identity `d4be3951…`, against the pinned `evidence/T-003_baseline_result.json`): 58 → 60 channels; **exactly five differ** —

| channel | before | after |
|---|---|---|
| `wall_load_calc__wall_load` (average) | 3.105376639122585 | 3.105376639122585 (unchanged) |
| `wall_peak_cal__calibration` | — | 1.3164408570995383 |
| `wall_peak_calc__wall_load_peak` | — | 4.088044684423419 |
| `cas72_calc__cost` | 95,898,253.47855279 | 131,494,479.60591842 |
| `lcoe_calc__lcoe` | 307.08712042841586 | 313.5134115016116 |
| `lcoe_1cfe_calc__lcoe` | 301.0951146207506 | 307.52140569394635 |

Every other channel bit-identical; verdicts: `wall_load_ok` `satisfied` → `violated`, the other eight unchanged. The calibration, the peak and CAS72 land on the design's predictions to the last digit. The LCOE move, derived now that the annual energy is known (`p_net` 743.910232 MW × 8760 h × 0.85): +35,596,226 / 5,539,086 MWh = **+6.426 $/MWh**.

**Independence.** `verify_stellaris.py` computes the average, the calibration (through its own torus-area convention at the six reference facts), the peak and the peak-driven CAS72 from the design's table, with `ash_frac` dropped from `IN` and the seven reference keys added; `oracle_entry.py` maps the seven entry keys and the two new channels. Parity at the baseline: zero relative deviation on the average, the calibration, the peak, CAS72, LCOE and `p_fus`. **Perturbation** (`wall_peak_q_ref` 4.05 → 4.50 alone, model through `study_route.run_points`, oracle through `IN`): the average stays 3.105376639; the calibration 1.316441 → 1.462712; the peak 4.088045 → 4.542272; CAS72 131,494,480 → 152,915,091; LCOE 313.513412 → 317.380537 — model and oracle agree to zero relative deviation on every one. **Identity from channels:** `neutron_wall_load_peak × 2700 / p_fus` = 4.049999999999999 (float-exact 4.05).

**`run_stellaris_single.py`.** The three synthetic CAS72 guard cases restated as `q_n = p_fus × (1 − ash) / area` at the same values (every guard still binds: cap, floor, outer max); `EXPECTED_VERDICTS["wall_load_ok"]` → `violated` with the derivation; the three moved anchors (LCOE 313.513412, CAS70 199,635,292.948643, `lcoe_1cfe` 307.521406) re-pinned **after** the script's own oracle gate read bit-exact on each, never before; the parity message corrected ("seven satisfied + sustainment_ok violated + wall_load_ok violated"). Full run: anchors green, verdict parity PASS, bit-exact vs oracle PASS on every channel, guard spot-check PASS.

### Phase 6 — 2026-09-04

- **Snapshot** recaptured through `capture_instance_graph_snapshot` (changed, one line).
- **Manifest** re-pinned from the package's own contracts: indicator-input `c1b0f0d1…` (was `2649e0ea…`), executable `d4be3951…` (was `b0c5f3ed…`), semantic `d468f3b6…` (was `48731d15…`); headline 313.5134115016116; `wall_load_ok` expected `violated`. **Deviation from MR-WI041-5's letter, recorded:** the manifest's verdict schema admits only `source_local_identity` and `expected` (`scripts/study/manifest.py:337`), so no derivation note can sit beside the flip there; the derivation is § MR-WI041-11 restatement (c) of this plan, the SV-051 row, and commit B's message, all of which the manifest's git history reaches.
- **Census** re-derived through the seam's own helper (`scripts/integrate.py::rederived_census`): **199 → 207**, not the 205 predicted — one design attribute retired (`stellarator_09__stellaris__ash_frac`), seven minted (`wall_peak_q_ref`, `…p_fus_ref`, `…R_ref`, `…a_ref`, `…kappa_ref`, `…standoff_ref`, `…calibration_direct`), and **two library defaults minted that the prediction missed**: the calibration calc's defaulted formals `wall_peak_cal__ash_frac_in` and `wall_peak_cal__pi` are entry points of the library-default class, exactly as `sustain__ash_frac_in` and every other defaulted formal are. Nothing else moved.
- **Six known-answer fixtures** re-derived by running `scripts/study/indicators.py` on the live package: the same reachable constraints and the same objectives on every axis; `R`, `R+tie`, `a` and `I_coil` fire **one** more module and taint one more channel (59→60/86→87, 71→72/98→99, 59→60/86→87, 68→69/90→91) — the new peak module — and `availability` and `interest_rate` are unchanged. The calibration module is reached by no axis, because its inputs are the six held facts: the constancy assumption, visible in the trace. `wall_load_ok`'s operand classes are unchanged (computed vs bound). `test_known_answers.py`'s fingerprint and `FIXTURE_CONTRACT` read off that report, with the comment saying what moved. (The plan's phase-4 prediction "two modules" was wrong by one for the reason just given; the fixture, not the prediction, is the record.)
- **SV rows** SV-050 (design-point identity), SV-051 (disclosed verdict change, with the perturbation), SV-052 (lifetime by the peak inside the source's ~4–6 FPY band; the declared CAS72 and LCOE moves), all `passing` on the evidence above. **Traceability rows** for both new calc defs.
- **Validation** Levels 1–6 as in the phases 1–3 record (nothing under `models/` changed since). **`tests/models`: 48 passed / 13 skipped** — the recorded baseline exactly, the census and spine tests green on the re-derived fixture and the synced twins.

### Spec success criteria, verified — 2026-09-04

| criterion (spec § Success criteria / MR) | where the evidence is |
|---|---|
| **Functional.** `wall_load_ok` reads a computed peak; peak, calibration and average exist as named, exposed quantities; the lifetime calc reads the peak; the model regenerates and executes at the baseline | `stellarator_plant.sysml` (`wall_load_ok` bound to `wall_peak_calc.wall_load_peak`; `neutron_wall_load`, `neutron_wall_load_peak`, `wall_peak_calibration` exposed); `mfe_plant.sysml` (`cas72_calc.q_n_in = wall_peak_calc.wall_load_peak`); the regenerated package at `d4be3951…`; § Phase 5 record |
| **MR-WI041-1** like with like | the constraint's operand is `wall_peak_calc.wall_load_peak` against the printed peak; `mfe_viability.sysml` doc names both bases |
| **MR-WI041-2** calibration computed from printed factors, never typed in | `'Neutron Wall Load Peak Calibration'` computes it from six bound facts; no literal near 1.316 under `models/` (`grep -rn '1\.316' models/` finds only doc text naming the result) |
| **MR-WI041-3** design-point identity | SV-050 passing: `peak × 2700 / p_fus` = 4.049999999999999 |
| **MR-WI041-4** average retained; 2.87 a comparand of unstated basis | `neutron_wall_load` bit-identical (3.105376639); the rewritten cross-check block at `stellarator_plant.sysml` (the "WHAT THE SOURCE PRINTS" comment) says what T-001 § 2 established and calls 4.05 / 2.87 "NOT a peaking factor" |
| **MR-WI041-5** verdict change disclosed and derived, never tuned | manifest `wall_load_ok` expected `violated`; SV-051; § MR-WI041-11 restatement (c); no limit, calibration, power or geometry adjusted (the model diff touches none of them) — the schema deviation on the manifest note recorded in § Phase 6 |
| **MR-WI041-6** lifetime operand is the peak, decided explicitly, move declared | `mfe_plant.sysml` comment above `cas72_calc` and the calc def's doc; § MR-WI041-11 restatement (b), (d); SV-052; CAS72 131,494,479.61 and LCOE 313.5134115 bit-exact against the oracle |
| **MR-WI041-7** constancy assumption stated | the library calc's doc ("CONSTANCY ASSUMPTION") and the instance's `wall_peak_q_ref` doc ("CONSTANCY (design D4)"); visible in the trace (the calibration module is reached by no sweep) |
| **MR-WI041-8** independent verification | `verify_stellaris.py` computes the chain from the design's table; zero relative deviation at the baseline and under the `q_ref` perturbation; `run_stellaris_single.py` bit-exact gate PASS on every channel |
| **MR-WI041-9** library concept-agnostic and dormant-safe | both calc defs in `models/library/analyses/`; the seven `wall_peak_*` attributes default to the dormant values in the generic plant (calibration 1.0 → peak = average); the Stellaris facts only in `stellarator_plant.sysml` |
| **MR-WI041-10** every value sourced, page images cited | each of the six bindings cites its page image (`page_002_table_0.png`, `page_001_table_0.png`, `pdf-17-1.png`, `pdf-17-2.png`) or the line for the standoff; traceability rows for both calc defs; nothing defaulted in |
| **MR-WI041-11** restatement before regeneration | § MR-WI041-11 restatement is in commit `df6dc964` (commit A); the regenerated package is in commit B, after it |
| **MR-WI041-12** nothing outside the wall chain and the lifetime operand changes; doc comments corrected | the baseline diff: exactly five channels differ (the two new ones, CAS72, LCOE, `lcoe_1cfe`) and one verdict; `p_fus`, geometry, `wall_area`, `wall_load_limit`, every heating number unchanged; `stellarator_plant.sysml` cross-check block rewritten, the two archived WI-039 paths corrected, `mfe_heating_chain.sysml` EI-5 sentence added |
| **Quality.** Levels 1–3 pass; no new Level 4–6 residue class; batteries green | § Phases 1–3 record (Level 6 230 → 237 attributed); `tests/models` 48 / 13; `tests/study` — see the phase-6 line |
| **Verification.** identity; baseline 4.0869 → executed 4.088045 (the design's 4.0869 used 0.8 for the neutron share in one line; the calc's 0.2002 gives 4.088045, and the design's own table says 4.088044684) violated; CAS72 and LCOE moved by the declared amounts, oracle agreeing; everything else bit-identical | § Phase 5 record |

**The study battery's first run (on the uncommitted tree, before commit B): 319 passed, 16 failed, 24 errors, 1 skipped.** Read, not waved through:
- **Git-clean class (13 failures, 24 errors):** `test_common`, `test_integration_workspace`, every `test_integrate_*`, `test_preflight_gates` and the `test_verify` tests behind the `promoted_run` fixture gate on a git-clean `generated/` and refuse an uncommitted package by design (`package tree is not git-clean: exploration/stellarator_e2e/generated`). The WI-039 precedent ran this battery after its re-pin commit for the same reason; the run of record is after commit B.
- **`test_integrate_preconditions::test_simkit_probe_refuses_without_the_teax_root` (1):** my shell had `PYTHONPATH` pointing at `teax-simkit` for the baseline scripts, so the negative test found simkit with the root unset. An invocation artifact; the plan's invocation (no `PYTHONPATH` export) is used for the run of record.
- **Two genuine restatement sites the surface table missed, fixed:** (i) `oracle_entry.OPERAND_BINDINGS` still bound `wall_load_ok`'s operand to `wall_load_calc__wall_load` — the verifier re-derived the fence from the average and read `satisfied` where the store says `violated` (`test_verify`: three failures and the nine errors behind `summary`); rebound to `wall_peak_calc__wall_load_peak`, which is precisely the operand change this item makes, and which the constraint id (`…__ab2c790419af93bb`, unchanged: it hashes the definition and the local identity, not the binding) did not flag. (ii) `test_mechanical_failures::test_the_corrupt_line_carries_file_line_and_key_path` pins the pipeline line of `rb.inputs.R_in` — :87 → :103 now that the wall modules sit above it; re-pinned with the history in its comment.
- **`test_operand_bindings::test_the_shim_reproduces_the_pinned_headline` (1):** `PINNED_LCOE` 307.08712042841586 → 313.5134115016116 with the derivation, as § MR-WI041-11 (d) says.
