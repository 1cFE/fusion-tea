# Pre-execution protocol — 20260914-magnet-coil-realism

Study under goal `magnet-coil-realism` round 1 (`work/orchestration/goals/magnet-coil-realism/trail.md` § T-003 scope). Executor: the round agent's forked session, 2026-09-14. Written before any point ran; the record (`record.md`) is filled after the fresh pre-execution critique returns and is committed with the results.

## Intake

`[OWNER-VERBATIM 2026-09-14]` "ok agreed, draft the goal file and /run-goal" — the ruling on the proposal whose question was "does the magnet's winding length, cold load and structure follow the coil the model builds, and does correcting them change which machine the model favours?" (`work/orchestration/goals/magnet-coil-realism/evidence/grounding_proposal.md`).

`[AGENT]` Everything below is the executor's. This study reads round 1's increment alone — the winding length computed from the coil bore (WI-058, pin below) — and asks: at the new pin, how do the magnet capital and its parts (winding procurement: tape, winding fabrication, material inventory; casing structure), the cryoplant electrical and the recirculating fraction respond to the minor radius on the design column and through the cheapest committed 18-verdict-feasible machine; how do they respond to the major radius at fixed bore; which committed cases flip and why; did the cheapest committed feasible machine or the `a`-minimum of LCOE move.

## Pin

Package `exploration/stellarator_e2e/generated`, manifest `exploration/stellarator_e2e/studies/manifest.json`; pin `2a89b16387270ac29ee9bd406987c8561c46353a7865f9054cb741998dd912e1`, semantic `8eb332b9c73e1b80a5d7629e4de3532c739c280bbc889f45cb7bf3672269959d`, executable `e11e4c17b11681ac98b754e1ecbd60452fc11c758ef2d9ce72cfc57d4e740cad`, teax `8d877460ac4f6f264561d916e40c1708adb13397` (`work/orchestration/goals/magnet-coil-realism/evidence/T-002_integration/integration_return.json`, ten gates passed, commit `1d08fb85`). Baseline LCOE 142.50725862880648 $/MWh, 17 of 18 verdicts satisfied, `divertor_heat_ok` violated as at the entering pin.

## What changed in the model, and what this study is not

WI-058 (`work/active/WI-058_coil-winding-length-from-bore/`, audit PASS at `a6286a55`): `c_coil = c_coil_ref × (a_coil / a_coil_ref)` on the coil-centre bore (`rb.r_coil_centre = a + 1.85 m`), `c_coil_ref = 25.0` m at 3.15 m, `k_coil` retired; the major radius no longer enters the winding length. Consumers of the length: the winding-pack cold volume, the ampere-metres, the winding procurement (tape, winding fabrication, material inventory) and through the cold volume the cryoplant load. Not touched: the peak field, stress, strain, stored energy, casing mass, tape price, reference density, selected envelope, coil count. At the entering pin the grounding probe (`work/orchestration/goals/magnet-coil-realism/evidence/grounding_probe/transects.csv`) read the winding procurement and the cryoplant load bit-constant in `a` on the design column and exactly proportional to `R`.

This is a sensitivity study of an engineered window. It claims no boundary, no optimum, no qualified design range. The committed 3,751-point plant-closure window is not re-run; any "cheapest feasible machine" statement is about the transect through the committed cheapest machine, not the window.

## Arms (candidate; fixed after the oracle scan, baseline and preflight)

Every point carries `availability_direct = 0` (the live lifecycle calendar, as every committed record since WI-046) and every other input at the package default. Entry keys are the package's own (`oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT`); the validity mask `R > a + 2.25` holds at every point (checked in `preparation/proposals.json`).

- `arm-a-transect` (30 points): `plasma__a` ∈ {1.3, 1.4, …, 2.2} on three columns — the design column (R 12.7, I_coil 15.4 MA); the cheap column at 100 MW (R 12.7, `magnet__coil__I_coil` 13e6, `plasma__n_e0` 4.048e20 — the committed `20260912-plant-closure:c0113` coordinates, LCOE 191.7581690876428, all 18 satisfied at that record's pin); the cheap column at 220 MW (the same with `heating__p_wallplug_heat` 220 — `c0130`, 198.00258969214127).
- `arm-R-transect` (14 points): `plasma__R` ∈ {11.43, 12.0, 12.7, 13.5, 14.2, 15.0, 15.7} at `a` 1.3 on the design column and at `a` 1.7 on the cheap column at 100 MW.
- `arm-matched-window` (108 points): the coordinates of every committed `20260913-magnet-design-transfer` case — R {11.43, 12.7, 13.97} × a {1.17, 1.3, 1.43} × I_coil {14, 15.4, 17} MA × `magnet__winding_pack__B_max` {20, 24.9, 27.5, 30} T — read from that record's `results/cases.json` and submitted as the four axis coordinates only (`preparation/matched-window-cases.json`, `preparation/proposals.json`). **Disclosure:** the committed cases carry their full fixed-input set, which includes the retired key `magnet__coil__k_coil` = 1.9685…; that key does not exist at this pin (`c_coil_ref` replaces it), so the committed input dicts cannot be replayed verbatim. Every other committed fixed input equals the current package default (checked: zero differences over the 108 cases). The comparison by case id is therefore a comparison of the same coordinates under the old and the new winding-length form, and nothing else.

## Framing (proposed)

| Axis | Framing | Why |
|---|---|---|
| `a` | sensitivity | The increment made the winding chain respond to the bore; the question is the size and shape of that response and its consequence for the price minimum on each column. No boundary claim. |
| `R` | sensitivity | The increment made the winding chain invariant in `R` at fixed bore; the question is what the rest of the plant does and how the price moves. No boundary claim. |
| `I_coil`, `B_max` | sensitivity (matched-window coordinates, not swept transects) | Present only so every committed magnet-design-transfer case is re-read at its own coordinates. |
| `n_e0`, `p_wallplug_heat` | declined as swept axes (column coordinates) | Fixed at the committed cheap-machine values; declared so their indicators are traced. |

Indicators (`indicators.json`, all six groups, `subset=false`): `a` 13/18 constraints reachable, 14/14 objectives; `R` 13/18, 14/14; `I_coil` 13/18, 13/14; `B_max` 5/18, 6/14; `n_e0` 10/18, 11/14; `p_wallplug_heat` 2/18, 3/14. No axis reports `no_constraint_response`; no owner ruling under policy § 9 is required; no axis is labelled `unresisted`. Reachability is a possible path, never a response.

## Expected responses (predeclared; the run decides)

From the WI-058 off-design predictions (`work/active/WI-058_coil-winding-length-from-bore/prototype/proto_results.json`, executed and matched by the oracle within 5.5e-16) and the entering-pin probe:

- Along `a` at fixed `R`, `I_coil`, `B_max`: `c_coil`, the winding-pack volume, tape, winding fabrication, material inventory and winding procurement scale by `(a + 1.85) / 3.15`; the cryoplant electrical rises with the cold volume; casing structure follows the stored energy as before (WI-044); peak field, stress, strain, stored energy, casing mass and `p_th` are unmoved by the length. At `a` 2.2 on the design column: ratio 1.2857, procurement about $2,019.05M, magnet capital about $2,099.6M, LCOE 129.35 against the entering pin's 122.51.
- Along `R` at fixed `a`: the winding chain is invariant to the double; every other channel moves as before.
- Verdict flips relative to the committed records can come only through channels the length reaches: `recirc_ok` (through the cryoplant electrical, expected to be small) and `net_positive` (same path); `peak_field_ok`, `wp_stress_ok`, `cond_strain_ok`, `beta_ok`, `wall_load_ok`, `sustainment_ok`, `burn_hold_ok`, `divertor_heat_ok`, `loop_*`, `tbr_ok`, `cycle_domain_ok`, the four heating checks do not read the length. The run reports every flip by case id with the operand that moved.
- The `a`-minimum of LCOE on the design column sat at `a` 2.0 (119.75) at the entering pin; with the magnet now priced against the bore it is expected to move to a smaller `a` or flatten — the run decides.

## Comparisons the record carries

1. Before/after per point against the entering-pin probe transects (design column, `a` 1.3–2.2 and `R` 11.43–15.7) and against the committed plant-closure `c0113` and `c0130` and every magnet-design-transfer case (`results/comparison-*.json|csv`).
2. Every verdict flip by case id, with the operand that moved.
3. The `a`-minimum of LCOE on each column, before and after.
4. The cryoplant's share of the recirculating power at the design point and at `c0113`.

Every count names its sense of "feasible" (the 18-verdict claim).

## Route, verification, record

Route: the study-local direct-API route (`studies/study_route.run_points`, a `PreparedListStrategy` over the prepared list — transects and matched points are not a Cartesian grid), one store per arm under `results/<arm>/_work/`, required channels in `preparation/required-channels.json` (every declared column must be published or the route refuses). Baseline and preflight per runbook steps 5–6 before any point; the oracle scan of every candidate point (step 7) fixes the window as `engineered`. Verification (step 10): `scripts/study/verify.py` over a stratified sample per arm at 1e-9 relative, every verdict re-derived from oracle operands; the 16 native channels outside the oracle map (ANNEX § Current oracle comparison coverage — `magnet__coil_length__c_coil` is one of them) are disclosed as not independently verified by the generic tool, and `c_coil` is checked instead by the identity `c_coil = 25 × (a + 1.85) / 3.15` at every point in the report. Findings register and first-sighting discovery rows at step 14; `tests/study/test_records.py` before the commit; snapshot with one `arms[]` entry per arm, each carrying `effective_executable_fingerprint`.

## Reviews owed

Pre-execution framing critique by a fresh non-author session (this protocol, `axes.json`, `indicators.json`, `preparation/`), verdict recorded in `reviews/preexecution-review.md` and § 14 before any point runs. Post-execution: correctness, honesty and readability lenses; a fresh administrator synthesis after the commit (dispatched by the round agent); the goal's disposition checkpoint before any follow-up.
