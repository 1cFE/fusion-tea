---
Status: draft
Created: 2026-09-08
Updated: 2026-09-08
Related Artifacts:
  Spec: ./spec.md
---

# WI-046 Design — the lifecycle calendar: one clock for component life, dated replacement, availability and CAS72

One handwritten calc replaces the periodic CAS72 chain: in its live mode it walks a deterministic finite-horizon calendar from the physical first-wall life, produces the replacement dates, the productive full-power years, the downtimes, the availability and the dated-event CAS72; in its held mode it reproduces the retired chain to the bit. Written under goal `plant-closure` round 1, task T-003 (`work/orchestration/goals/plant-closure/trail.md` § T-003 scope); the form is `[AGENT] — proposed under the owner's direction of 2026-09-08` (`goal.md` § Reserved gates 4, 6; the basis packet `evidence/round1_basis_packet.md` §§ 2, 3, 6, 8 with its Amendment). Prototyped in `prototype/proto.py` → `prototype/proto_results.json` (pure Python on the oracle's inputs; no model file touched — the T-003 exclusions). This design decides the spec's six open decisions (D1–D6) and four it found (D7–D10).

## Overview

Today `availability = 0.85` is an instance constant read by fuel, CAS72, both LCOE forms and the study seam, and CAS72 is the periodic chain `L_cal = L / A`, `n_rep = ceil(N / L_cal) − 1` in a handwritten impl (spec § Current state). After this item:

- `calc def 'Lifecycle Calendar'` (`models/library/analyses/mfe_lifecycle.sysml`, manual interface on the exact route) takes the peak wall load, the fluence limit, the horizon, the outage duration, the residual unplanned fraction, the cost per event, the discount rate, the coil life and `availability_direct`, and publishes eleven channels;
- the generic plant wires it as `calendar`, binds `availability` by reference to `calendar.availability` (the WI-044 D5 pattern) so every existing consumer reads one producer without a text change, and reads `cas72_annual` from it; `'Levelized Replacement Cost'` and its impl retire;
- the Stellaris instance binds `outage_years = 0.5833333333333334` (seven months, the source's estimate), `unplanned_fraction = 0.0` with the packet's label, `coil_life_fpy = 10.0`, `availability_direct = 0.0` (live); `availability = 0.85` retires as an entry point;
- with `availability_direct = 0.85` the package reproduces the entering pin bit-for-bit (the compatibility bridge); live, at the entering pin's other values, availability reads `0.9027777777777779`, five replacements at 4.52 / 9.63 / 14.74 / 19.85 / 24.95 yr, CAS72 136,289,876.08 $/yr, LCOE 305.184 (§ Expected baseline behaviour).

No verdict is added by this item (WI-045 takes the set 10 → 13 and WI-047 to 14; packet Amendment item 3). Census: 209 at entry → predicted 212 (`availability` out; `availability_direct`, `outage_years`, `unplanned_fraction`, `coil_life_fpy` in).

## Research findings

- **The held chain's numbers at the design point** (`proto_results.json` § `held`): physical life `4.5239260339489915` FPY (18 / 3.9788448937763854), `L_cal = 5.322265922292932` yr, `n_rep = 5.0`, events at `k · L_cal` (5.32, 10.64, 15.97, 21.29, 26.61), `replacement_pv = 1571600794.5219266`, CAS72 `126649655.78572692` — **equal with `==` to `verify_stellaris._oracle_levelized_replacement_cost` and to the pinned channel `cas72_calc__cost`** (`held_equals_mirror: true`). The chain carried verbatim inside the new impl is a copy, not a re-derivation, so the held mode is bit-identical by construction (spec risk 1 discharged at the prototype).
- **The live calendar at the design point** (§ `live.7mo_u0`): the interval walk and the closed form `t_k = k L / b + (k − 1) d` agree at every event to 1e-12 yr; the fifth restart at 25.536 yr is before the horizon and the sixth limit would fall at 30.06, so five replacements; `productive_fpy 27.083333333333336`, `planned_downtime_yr 2.916666666666667`, `availability 0.9027777777777779`, `replacement_pv 1691226685.2130158`, CAS72 `136289876.0833351`, `dated_energy_ratio 1.0051616112988944`, `coil_life_margin_fpy −17.083333333333336`; the time identity residual 3.6e-15 yr.
- **The probe's "calendar-only 133.03 M$/yr" was not the calendar's CAS72.** The grounding probe overrode the oracle's `availability` scalar, which fed the live availability back into the *periodic* chain (`L_cal = L / 0.9028`); the dated-event CAS72 is 136.29 M$/yr because the first event comes at 4.52 yr instead of 5.32 and each later one earlier still — the research's "outage of timing error" in dollars: +3.26 M$/yr, +0.575 $/MWh. The design's numbers are the calendar's; the probe's are cross-checks of the availability half only (packet Amendment item 2 stands; this is the correction to its parenthetical).
- **Five months buys a sixth replacement** (§ `live.5mo_u0`): events at 4.52, 9.46, 14.41, 19.35, 24.29, 29.23 with the sixth restart at 29.64 < 30; availability `0.9166666666666666`; CAS72 147.49 M$/yr — availability up 1.4 points and CAS72 up 8 % at once, so LCOE moves only 302.51 against 305.18. The integer step `minor-radius` L-002 found along `a` is live in the outage duration; a study reads the count beside every availability.
- **The unplanned fraction brackets the held value**: `u` 0.05 → 0.8576, `u` 0.10 → 0.8125 at seven months; at ten months and `u` 0 → 0.8611. The held 0.85 has no privileged position on this surface.
- **A committed high-wall-load point where the count steps** (§ `stepping_points`): `c3343` (peak 9.039 MW/m², committed LCOE 152.91, infeasible) reads 12 replacements on the held chain (`L_cal` 2.343) and **11** on the calendar with availability 0.7861 — the calendar buys fewer because each outage delays the next limit, and charges the lost production the held chain never did (`wall-and-heating` L-011's gap closed in the direction the research predicted). The feasible `c7752` (peak 4.040) reads 5 on both, availability 0.8912.
- **The synthetic cases reproduce the research's numbers** (§ `synthetic`): `L 4, d 7/12, N 10` → events 4 and 8.5833, two replacements, planned 7/6 yr, 53/6 FPY, `A 0.8833333`; `N 8.7` → one replacement, terminal 0.1167 yr; `N 9 + 2/12` → one (restart exactly at retirement is not strictly before); `N 9 + 2/12 + 1e-6` → two; `q_n = 0` → no replacement, `A = 1 − u`; no outage and `u` 0 → `A = 1.0` with CAS72 still 154.38 M$/yr (five events at zero duration); `N` 3000 → `A` 0.88586 against the asymptote `L / (L + d)` 0.88578; `productive_fpy` non-increasing in `u`; the held mode equals the mirror on the single runner's three guard cases.
- **The codegen envelope and the manual stage.** A loop over dated events and `math.ceil` are outside `+ - * / **` (packet § 1), so the calc is a manual interface exactly as `'Levelized Replacement Cost'` is (`mfe_account_costs.sysml:796-888`: every output `out attribute x : Real;` with no expression, the doc carrying the normative chain). The generated caller unpacks the impl's return tuple in an order it fixes (`generated/modules/mfe_plasma_sustainment/plasma_sustainment.py:685` for a 17-output manual calc; the impl's docstring records the order "verified at the regeneration"); the pydantic input class is `<CalcName>Input` with the formals as fields (`levelized_replacement_cost.py:100-116`).
- **The existing single-runner gate imports the old impl by name** (`run_stellaris_single.py:259-263`: `from stellarator_tea.handwritten.mfe_account_costs.levelized_replacement_cost_impl import levelized_replacement_cost`), so retiring the file breaks the gate unless the gate is restated onto the new impl's held mode (D9).
- **The oracle already has the held-mode mirror** (`verify_stellaris.py:358-382`); `compute()` reads `p["availability"]` at four sites (`:616`, `:639-643`, `:655`, `:665`). The seam maps `availability` at `oracle_entry.py:55` and the route declares it as an axis (`study_route.py:55`, `BASELINE` at `:62`, `proposal_for` at `:89-98`, the availability sweep at `:365-397`); the known-answer fixture `tests/study/data/availability.expected.json` and `test_known_answers.py:49` (`"availability": (True, [], ['cas72', 'fuel', 'lcoe', 'lcoe_1cfe'], 6, 8)`) and `:105-108` (`test_availability_reaches_no_constraint`) name it.
- **The IFE plants carry their own `availability`** (`models/designs/generic_ife/ife_plant.sysml`, `hif_ife/hif_plant.sysml`) and do not import the MFE plant; the tokamak instance of epic Item 3 does not exist. The generic MFE plant's `availability` has no default today (`mfe_plant.sysml:1000`) — every instance binds it.

## Design decisions

### D1 — The impl walks intervals; the oracle derives the closed form. `[AGENT]`
The handwritten impl is the general form (an interval walk that a later component split can extend: the earliest remaining life triggers, only the replaced clock resets) and the oracle computes the event dates from `t_k = k · L / b + (k − 1) · d` with the strict-restart rule, then the productive time, downtimes, PV and CAS72 from those dates. The two are algebraically the same for one bundled event and computationally independent, which is what the oracle gate is for (spec MR-WI046-10; the prototype's assertion that both give the same five dates to 1e-12 is the first instance). Rejected: both closed-form (one derivation checked against itself); both walks (the same).

### D2 — What the held mode reports for the seven non-cost outputs. `[AGENT]`
The retired chain implies, and the held mode publishes: `physical_life_fpy` = the clipped `core_lifetime_fpy` (the chain's own life quantity, floor and cap included — the held mode carries the guards, the live mode has none); `n_replacements = n_rep`; `productive_fpy = N · A_direct`; `planned_downtime_yr = 0.0`; `unplanned_downtime_yr = N − N · A_direct` (the held multiplier is an undifferentiated downtime — it belongs to no schedule, so it is reported as the residual under the "unplanned" name with the docstring saying so); `terminal_downtime_yr = 0.0`; `coil_life_margin_fpy = coil_life − N · A_direct`; `dated_energy_ratio = 1.0` (uniform production is what the annual-equivalent form assumes). The identity `F + T_p + T_u + T_term = N` holds in this mode too. The event dates in held mode are `k · L_cal`, deposited with the diagnostic (D6) and labelled the periodic chain's. Rejected: reporting NaN for the non-cost outputs in held mode (a blank channel is what the route refuses).

### D3 — `dated_energy_ratio` bins by calendar year from commissioning. `[AGENT]`
Year `y` covers `(y − 1, y]` with a fractional last year when `N` is not an integer; `E_y ∝ b ×` the online calendar time inside year `y` (an outage that straddles a year boundary splits); `ratio = Σ_y E_y (1 + i)^{−y} / [E_avg Σ_y Δ_y (1 + i)^{−y}]` with `E_avg = F / N` and `Δ_y` the year's length. `P_net` cancels. The ratio is exactly 1.0 when production is uniform (`q_n = 0` and `u = 0`, or the held mode) and 1.0 at `i = 0` for any schedule (the discount factors are all 1) — both are its tests. At the design point 1.00516: the calendar's energy is front-loaded relative to uniform (the first 4.52 yr run before any outage), so the exact-DCF denominator would be 0.5 % larger and the headline 0.5 % lower than the annual-equivalent form reports. Rejected: event-aligned intervals (not a year-by-year cash-flow convention; harder to state).

### D4 — `availability` stays a plant attribute bound by reference to `calendar.availability`; the consumers' text is unchanged. `[AGENT]`
`attribute availability : Real = calendar.availability;` replaces the bare declaration at `mfe_plant.sysml:1000`; `fuel_calc`, `lcoe_calc`, `lcoe_1cfe_calc` keep `in availability_in = availability;`. This is the WI-044 D5 `m_casing` pattern (an attribute bound by reference to a calc output ceases to be an entry point and keeps its consumers). If the codegen classifies the reference as a bare alias that mints no channel (the WI-028 class), the fallback is stated now: the three consumers read `calendar.availability` directly and the attribute is removed; either way one producer. The plan's regeneration step checks which happened and records it.

### D5 — The `availability` study axis is renamed to `availability_direct`, and the known-answer fixture is re-derived. `[AGENT]`
`study_route.py`: `AXES["availability"]` → `AXES["availability_direct"] = [f"{P}availability_direct"]`; `BASELINE["availability"]` → `BASELINE["availability_direct"] = 0.0` (the instance's live value); `proposal_for`'s third argument and the availability sweep (`availability_sweep_proposals`, `run_availability_sweep`) restated onto the new key, the sweep's grid becoming the held-mode values it always was (0.7–0.95 select the held mode, so its response is the retired chain's — the sweep keeps its meaning as a historical comparison and says so). `tests/study/data/axes.known_answers.json`: the axis renamed; `availability.expected.json` → `availability_direct.expected.json` re-derived by `scripts/study/indicators.py`; `test_known_answers.py` `CASES` and the `FIXTURE_CONTRACT` row restated from the report with a dated comment; `test_availability_reaches_no_constraint` keeps its claim — a sweep over `availability_direct` reaches `cas72`, `fuel`, `lcoe`, `lcoe_1cfe` and no constraint, because every nonzero value selects the held mode whose response is the old one — with the docstring saying the lever is now the held-mode switch and the live chain's response to design lives on the wall-load axes (`a`, `R`, `I_coil`, which now reach the eleven calendar channels). Rejected: dropping the axis (loses the known answer that made the original finding mechanical). The manifest's `axes` block and any tie data naming `availability` are restated by the re-pin.

### D6 — Event dates are a diagnostic JSON under the item's evidence and a printed line in the single runner, never a channel. `[AGENT]`
The impl exposes a helper `calendar_events(...)` returning the dates (used by the single runner's gate and the prototype); `run_stellaris_single.py` prints them at the baseline in both modes; the implementation deposits `evidence/baseline_live/events.json` and, for the off-design points, `evidence/offdesign_points/events.json`. A variable-length list is not a scalar channel and the packet § 2 says so.

### D7 — No defaults on the four new plant attributes; every MFE instance binds them; the held mode is a binding away. `[AGENT]`
`outage_years`, `unplanned_fraction`, `coil_life_fpy`, `availability_direct` are declared without defaults, as `availability` is today and as the WI-044 anchors are (its D6): the abstract generic plant compiles unbound, the IFE plants are separate part defs with their own `availability`, and a second MFE instance binds its own facts. A concept that wants the old behaviour binds `availability_direct` to its old constant and any values for the other three — the held mode ignores them — which reproduces its old chain exactly. Rejected: `availability_direct default 0.0` with the others defaulted (a concept binding nothing would silently get a live calendar on zero outage — `A = 1.0` — a behaviour change by default, the thing dormant-safety exists to prevent).

### D8 — The mode is selected by `availability_direct_in > 0`; a negative value is invalid. `[AGENT]`
The packet § 3 fixes the rule; the impl raises on `availability_direct_in < 0`, on `availability_direct_in > 1`, and on any non-finite input (MR-WI046-2's fail-loudly posture); in held mode the other inputs are validated only for finiteness (the retired chain never validated them). The oracle applies the same rule.

### D9 — Placement, retirement and the gate. `[AGENT]`
The calc lives in a new `models/library/analyses/mfe_lifecycle.sysml` (package `mfe_lifecycle`); the plant usage is `calendar`, so the channels are `calendar__<output>` as the packet names them. `'Levelized Replacement Cost'` is removed from `mfe_account_costs.sysml` (lines 796–888) and its impl file `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` is deleted at the regeneration; its docstring's history (WI-029 MF-1's three guards; WI-041's peak operand; the exact-route form and the migration ledger row) moves into the new impl's docstring, and the ledger row in `models/stellarator_migration_ledger.md` gets one dated line saying the calc was retired by WI-046 with its chain carried as the calendar's held mode (a history note, not an edit of the row). `run_stellaris_single.py`'s `_cas72_guard_gate` is restated: it imports the new impl's held-mode function (`lifecycle_calendar_held`) and the oracle's `_oracle_levelized_replacement_cost`, keeps the three synthetic guard cases verbatim, and adds the live-mode boundary cases (D1's closed form against the impl's walk on the research's synthetic cases) as a fourth family. Rejected: keeping the old calc def dormant in the library (a second producer of CAS72's meaning with no usage; the packet's one-producer rule).

### D10 — The restatement precedes regeneration; predictions precede execution; this item integrates second. `[AGENT]`
The WI-044 shape: commit A carries the model edits, the twins, spec, design, plan (with the MR-WI046-15 restatement and the predictions) and `evidence/baseline_before/` from the package as WI-045 left it; commit B the regenerated package, the new impl, the oracle, the seam, the route and fixture rename, the single runner, the re-pin, SV and trace rows, `evidence/baseline_held/`, `evidence/baseline_live/`, `evidence/offdesign_points/`; commit C the `tests/study` run of record. Because WI-045 lands first (packet § 9), the live-mode prediction this design states is at the entering pin's other values; the plan re-states it at WI-045's package state in `evidence/baseline_before/` before commit A (the divertor account in `cost_per_event` moves with WI-045's live gross power). WI-045's prototype results (`work/active/WI-045_primary-loop-and-cycle/prototype/proto_results.json`) did not exist when this design was written; the plan reads them when they do.

## Proposed design

### New: `calc def 'Lifecycle Calendar'` — `models/library/analyses/mfe_lifecycle.sysml` (prototyped in Python; the SysML text below is the implementation's copy-in)

```sysml
package mfe_lifecycle {
    private import ScalarValues::*;

    calc def 'Lifecycle Calendar' {
        doc /*
        One clock for the neutron-damage-limited in-vessel set (first wall /
        blanket + divertor, bundled): physical life -> a dated replacement
        calendar over the plant horizon -> productive full-power years,
        downtimes, availability, the replacement present value and CAS72.
        Replaces 'Levelized Replacement Cost' (WI-029 / WI-041), whose periodic
        chain is carried verbatim as this calc's HELD MODE (WI-046; goal
        plant-closure round 1; basis packet sections 2, 3, 8).

        LIVE MODE (availability_direct_in = 0), the deterministic finite-horizon
        calendar (research Option B):

          L      = fluence_limit / q_n                         [FPY] (q_n = 0: infinite)
          b      = 1 - u                                       productive fraction online
          walk from t = 0 with new components in capital: an online interval
          accrues productive time b*dt and unplanned downtime u*dt; when the
          accumulated life reaches L an outage of length d starts at that date
          t_k, the event is charged at t_k, nothing ages during the outage, and
          the bundled clock resets; a replacement is bought only if restart
          t_k + d falls STRICTLY before N; otherwise production ceases at t_k
          and N - t_k is terminal downtime; the horizon ending mid-run closes the
          last interval.
          Closed form for one bundled event: t_k = k*L/b + (k-1)*d.
          F + T_planned + T_unplanned + T_terminal = N          (identity)
          availability     = F / N
          replacement_pv   = sum_k C / (1+i)^t_k                (payment at outage start)
          cas72_annual     = CRF(i, N) * replacement_pv         (CRF = 1/N at i = 0)
          coil_life_margin = coil_life - F                      (reported, never a fence)
          dated_energy_ratio = PV of the calendar's yearly energy over the PV of the
                               uniform annual-equivalent energy (P_net cancels);
                               1.0 for uniform production; the exact-DCF headline
                               would divide by this ratio -- the annual-equivalent
                               convention stays the headline (WI-029 Option ii).

        HELD MODE (availability_direct_in > 0), the retired chain VERBATIM
        (levelized_replacement_cost_impl.py:70-101 at the WI-044 pin, the 1cfe
        guards carried as WI-029 MF-1 carried them; economics.py:53-75,
        model.py:102-111 at pin 0254385):

          core_lifetime_FPY = clip(fluence_limit / max(q_n, 1e-6), 0.5, N*A)
          core_lifetime_cal = core_lifetime_FPY / A
          s                 = (1 + i)^(-core_lifetime_cal)
          n_rep             = max(0, ceil(N / core_lifetime_cal) - 1)
          pv                = C * s * (1 - s^n_rep) / (1 - s)
          cas72_annual      = CRF(i, N) * pv
          availability      = A;  F = N*A;  T_unplanned = N - N*A (undifferentiated)

        The held mode is the compatibility bridge: with availability_direct at a
        concept's former constant every consumer reads what it read before, to
        the bit (goal plant-closure, Invariants). It is not a calendar and its
        guards are not material evidence (the 0.5 FPY floor is a gradient guard,
        the N*A cap a horizon cap); the live mode has neither and fails loudly
        on an invalid input.

        WHAT THIS IS NOT: whole-plant lifetime closure. One bundled event; the
        divertor's separate life, other scheduled maintenance (cryoplant,
        turbine, vacuum, fuel systems), decay-heat cooling and imported
        electricity during outages, replacement labour and waste are outside it;
        the coil's finite dose life is a reported margin because no admissible
        source gives its response to shielding or geometry. Availability
        integrates TIME: the loop, the exhaust and the conversion are sized at
        the online operating point and are not derated by it. Fixed staffing
        (CAS71) stays per calendar year; no lost-sales cost is added while the
        energy is removed from the denominator.

        EXECUTABLE SEMANTIC: the walk and ceil are outside the codegen envelope
        (+ - * / ** only), so this calc routes to the handwritten stage
        (manual_required); the generated handwritten impl is normative and is
        guarded by the oracle's independent closed-form derivation
        (verify_stellaris.py) at rel 1e-9 on every output.

        Concept-agnostic: every quantity is an input (MR-3). Event dates are a
        diagnostic artifact of the impl, not outputs.

        **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf (Stellaris, sec. 2.11, pp. 28-29; Table 6, p. 21 -- read as the renders under work/orchestration/goals/plant-closure/evidence/grounding_sources/); knowledge/sources/process_a_systems_code_for_fusion_power_plants_part_2/output.md (Kovari et al. 2016, sec. 8); /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
        **Ref**: Stellaris p. 29 (seven months estimated; five months and 90 % targets; four years between major maintenance); p. 28 (cooldown and recommissioning ~30 days each, inside the estimate); Table 6 (first-wall structure lifetime ~4-6 FPY; coil lifetime ~10 FPY); Kovari 2016 sec. 8 eq. 54 (planned / unplanned overlap), eqs. 55-59 (blanket / divertor lifetimes and outages -- the precedent for distinct lives, not adopted); economics.py:53-75, model.py:102-111 (the held chain); knowledge/research/pending/20260907-163520_lifetime-availability-closure-prework.md sec. Option B
        **Basis**: deterministic finite-horizon replacement calendar on the peak wall load; annual-equivalent economics with the exact-dated shadow
        */

        // peak neutron wall load [MW/m^2] (the plant binds 'Neutron Wall Load Peak')
        in attribute q_n_in : Real;
        // fluence allowance of the bundled in-vessel set [MW yr/m^2]
        in attribute fluence_limit_in : Real;
        // plant horizon N [yr]
        in attribute operational_years_in : Real;
        // scheduled outage per bundled replacement d [yr]
        in attribute outage_years_in : Real;
        // residual unplanned fraction of scheduled-online time u [1]
        in attribute unplanned_fraction_in : Real;
        // plant-total replaceable-account cost per event C [$]
        in attribute cost_per_event : Real;
        // discount rate i [1/yr]
        in attribute interest_rate : Real;
        // coil dose life [FPY] -- a reported margin's reference
        in attribute coil_life_fpy_in : Real;
        // HELD-MODE switch and value: 0 selects the live calendar; a value in
        // (0, 1] selects the retired periodic chain at that availability
        in attribute availability_direct_in : Real;

        // Manual interface on the exact route: every output declared without
        // an expression; the handwritten impl is the executable meaning.
        // physical first-wall life [FPY] (held mode: the clipped chain value)
        out attribute physical_life_fpy : Real;
        // replacements bought inside the horizon [count, as a float]
        out attribute n_replacements : Real;
        // productive full-power years F
        out attribute productive_fpy : Real;
        // scheduled outage time [calendar yr]
        out attribute planned_downtime_yr : Real;
        // residual unplanned downtime [calendar yr] (held mode: N - N*A)
        out attribute unplanned_downtime_yr : Real;
        // production ceased before the horizon [calendar yr]
        out attribute terminal_downtime_yr : Real;
        // equivalent availability F / N [1]
        out attribute availability : Real;
        // present value of the dated replacement events [$]
        out attribute replacement_pv : Real;
        // CAS72 levelized scheduled replacement [$/yr]
        out attribute cas72_annual : Real;
        // coil dose life minus productive FPY [FPY]; negative = exceeded
        out attribute coil_life_margin_fpy : Real;
        // exact-dated energy PV over the annual-equivalent PV [1]
        out attribute dated_energy_ratio : Real;
    }
}
```

### Retired: `calc def 'Levelized Replacement Cost'` — `models/library/analyses/mfe_account_costs.sysml` lines 796–888
Removed. The `// ---- CAS72 levelized scheduled replacement (WI-029, Rung B) ----` banner is replaced by one comment line: `// CAS72 moved to mfe_lifecycle 'Lifecycle Calendar' (WI-046); its periodic chain is that calc's held mode.` The three producer-shaping defs that follow (`'Annual Cost Rollup'` …) are untouched. The migration ledger (`models/stellarator_migration_ledger.md`) gains one dated line under the calc's row (D9).

### Changed: `models/designs/generic_mfe/mfe_plant.sysml` (lines 952–973 and 1000 as of `d981670f`)

```sysml
        // ---- CAS72 and availability from one lifecycle calendar (WI-046) -----
        // Replaceable set = the fluence-limited in-vessel accounts C220101
        // (blanket/first wall) + C220108 (divertor), plant-total (x n_mod), one
        // bundled event. Source: defaults.py:299 (replaceable_accounts), pin 0254385.
        attribute replacement_cost_per_event : Real =
            (blanket.capital_cost + divertor.capital_cost) * n_mod;

        // Core fluence limit [MW-yr/m^2] (instance binds; DT 18.0, defaults.py:291).
        attribute fluence_limit : Real;
        // scheduled outage per bundled replacement [yr] (instance binds)
        attribute outage_years : Real;
        // residual unplanned fraction of scheduled-online time [1] (instance binds)
        attribute unplanned_fraction : Real;
        // coil dose life [FPY] (instance binds) -- a reported margin's reference
        attribute coil_life_fpy : Real;
        // held-mode switch: 0 = the live calendar; (0, 1] = the retired periodic
        // chain at that availability (the compatibility bridge; instance binds)
        attribute availability_direct : Real;

        // The lifetime operand is the PEAK wall load (WI-041); the calendar is
        // the one producer of availability and CAS72 (WI-046).
        calc calendar : 'Lifecycle Calendar' {
            in q_n_in = wall_peak_calc.wall_load_peak;
            in fluence_limit_in = fluence_limit;
            in operational_years_in = operational_years;
            in outage_years_in = outage_years;
            in unplanned_fraction_in = unplanned_fraction;
            in cost_per_event = replacement_cost_per_event;
            in interest_rate = discount_rate;
            in coil_life_fpy_in = coil_life_fpy;
            in availability_direct_in = availability_direct;
        }
        // expose_pure channel for A-2
        attribute cas72_annual : Real = calendar.cas72_annual;

        calc cas70_calc : 'Annual Cost Rollup' {
            in cas71 = cas71_calc.levelized;
            in cas72 = calendar.cas72_annual;
            in cas80 = cas80_calc.levelized;
        }
```

and at the LCOE block:

```sysml
        // capacity factor [0..1] -- the calendar's output, bound by reference
        // (WI-046; the WI-044 m_casing pattern): one producer, every consumer
        // (fuel_calc, lcoe_calc, lcoe_1cfe_calc) reads it unchanged.
        attribute availability : Real = calendar.availability;
```

The `fuel_calc` usage precedes the calendar in file order and reads `availability`; the exact route resolves calc-output references regardless of source order (the WI-044 `magnet.m_casing = casing_mass.m_casing` binding sits above `casing_mass`'s declaration) — the plan's Level 1–3 validation checks it before the twins are synced (risk 2). `fuel_calc`, `lcoe_calc`, `lcoe_1cfe_calc` text unchanged (D4).

### Changed: `models/designs/stellarator_09/stellarator_plant.sysml` (line 1117 as of `d981670f`; the four bindings replace it)

```sysml
        :>> availability_direct = 0.0 {  // LIVE: the calendar produces availability (WI-046).
            doc /*
            The held-mode switch of 'Lifecycle Calendar'. 0.0 selects the live
            calendar; binding the former constant 0.85 here reproduces the
            pre-WI-046 package to the bit (the compatibility bridge -- goal
            plant-closure, Invariants; the study's compatibility arm sets it).
            History: availability = 0.85 was held here from WI-009 to WI-044,
            cited to backcasting_bridge.py:48 (1costingFE reference), and read as
            no_constraint_response by two committed studies.
            **Source**: work/orchestration/goals/plant-closure/evidence/round1_basis_packet.md **Ref**: sections 3 and 8 (the mode rule) **Basis**: the live calendar is the producer; the held value survives as the bridge
            */
        }
        :>> outage_years = 0.5833333333333334 {  // seven months, the source's ESTIMATE [yr].
            doc /*
            Stellaris sec. 2.11: "A provisional, early estimate of the possible
            overall maintenance duration to replace the in-vessel assemblies,
            including full replacement of the breeder blankets, has been
            performed, and a completion time of seven months is estimated."
            The five-month window and the 90 % overall availability on the same
            page are TARGETS ("a target overall plant availability of 90% has
            been set, based on an approximate 4.5 year operating cycle"; "a
            target on the remote maintenance systems to achieve replacement of
            the in-vessel components within a five-month window"), and the four
            years between major maintenance periods is the source's operating
            assumption -- none is an achieved value and none is bound here. The
            ~30 days of cooldown and ~30 days of recommissioning (p. 28) are
            inside the estimate and are not added. 7/12 as the IEEE-754 double.
            **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf **Ref**: p. 29 (render work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p29_maintenance.png), p. 28 (stellaris_p28_maintenance.png) **Basis**: the source's whole-outage estimate for one bundled in-vessel replacement
            */
        }
        :>> unplanned_fraction = 0.0 {  // NO ADMISSIBLE SOURCE; surfaced, not defaulted.
            doc /*
            equivalent availability conditional on the in-vessel maintenance
            calendar; unplanned failures not modelled. No admissible source gives
            a reliability basis for this machine; the round's study runs 0.05 and
            0.10 as declared stress scenarios, never a probability (basis packet
            section 6). Raising this fraction is not a substitute for reporting
            the coil-life margin.
            **Source**: work/orchestration/goals/plant-closure/evidence/round1_basis_packet.md **Ref**: section 6 (the surfaced input and its label) **Basis**: a missing input surfaced with options, never defaulted [OWNER 2026-09-02]
            */
        }
        :>> coil_life_fpy = 10.0 {  // coil lifetime (99th quantile) [FPY], Table 6.
            doc /*
            Reported as a margin channel (calendar.coil_life_margin_fpy), NEVER a
            fence: no admissible source gives the coil dose's response to
            shielding or geometry, and a direct constraint is not the rubric's
            "pushes back" [OWNER 2026-09-04]. Replacing in-vessel components does
            not reset coil dose; at 27 productive FPY the margin reads about
            -17 FPY -- a disclosed limitation of the 30-year horizon.
            **Source**: knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf **Ref**: Table 6, p. 21 (render work/orchestration/goals/plant-closure/evidence/grounding_sources/stellaris_p21_table6.png: "Coil lifetime (99th quantile) [FPY] ~10") **Basis**: the source's 3D OpenMC estimate at its own shielding
            */
        }
```

The `fluence_limit = 18.0` binding's doc gains one sentence: "Cross-check, not identity: 18 / 3.979 = 4.52 FPY sits inside the source's ~4–6 FPY first-wall band (Table 6); the ARIES-FS 200 dpa convention and the paper's ARC-DPA allowance are not shown to be the same damage measure (research line 78)." The disclosure block of MR-WI046-14 (a)–(f) is carried by the calc doc above and the four bindings.

### Twins: `exploration/stellarator_e2e/models/analyses/mfe_lifecycle.sysml` (new), `analyses/mfe_account_costs.sysml`, `designs/generic_mfe/mfe_plant.sysml`, `designs/stellarator_09/stellarator_plant.sysml` — copied byte-for-byte (plan phase 1).

### New: `exploration/stellarator_e2e/generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py` — the normative body (the stencil's `inputs.<field>` names read at regeneration; the return-tuple order fixed by the regenerated caller and recorded in the docstring at implementation)

```python
"""Handwritten implementation for Lifecycle_Calendar (WI-046; goal plant-closure round 1).

AUTO_IMPLEMENTED = False  (hand-written, normative -- do not regenerate over
this file; the bridge sets preserve_handwritten=True. When the calc's
interface changes the generator re-stencils it and this body is restored by
hand, as WI-041 did on 2026-09-04.)

SysML Source: models/analyses/mfe_lifecycle.sysml ('Lifecycle Calendar')

Executable semantic (normative, per the calc doc). Two modes, selected by
availability_direct_in:

LIVE (availability_direct_in == 0.0): the deterministic finite-horizon calendar
(research Option B; design D1 the interval walk). Physical life L = fluence /
q_n (q_n == 0 -> infinite). b = 1 - u. From t = 0: an online interval accrues
F += b*dt, T_u += u*dt; when the accumulated life reaches L an outage of length
d starts at t_k; the event is charged at t_k; the clock resets; a replacement is
bought only if t_k + d < N strictly, else production ceases and N - t_k is
terminal downtime. F + T_p + T_u + T_term == N to 1e-12. availability = F/N.
replacement_pv = sum C/(1+i)**t_k; cas72 = CRF(i,N)*pv with CRF = 1/N at i = 0.
coil_life_margin = coil_life - F. dated_energy_ratio: calendar-year bins from
commissioning (design D3). Invalid or non-finite inputs RAISE; no floors.

HELD (0 < availability_direct_in <= 1): the retired 'Levelized Replacement
Cost' chain VERBATIM -- levelized_replacement_cost_impl.py:70-101 at the WI-044
pin (WI-029 MF-1 carried 1cfe's three guards verbatim: the inner max(q_n,1e-6),
the clip floor 0.5 / cap N*A in jnp order, the outer max(0, ...); the float
n_rep so s**n_rep takes 1cfe's pow path; WI-041 made the wall load the PEAK
handed in). availability = A_direct; F = N*A; T_p = 0; T_u = N - N*A
(undifferentiated held downtime, design D2); T_term = 0; physical_life = the
clipped value; coil margin on N*A; dated_energy_ratio = 1.0.

Source: /home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py (pin 0254385)
Ref:    economics.py:53-75 (levelized_replacement_cost); model.py:102-111
        (_core_lifetime_fpy -- the clip and the inner max); economics.py:6-10 (CRF);
        Stellaris sec. 2.11 pp. 28-29 and Table 6 p. 21 (the renders under
        work/orchestration/goals/plant-closure/evidence/grounding_sources/);
        research 20260907-163520_lifetime-availability-closure-prework.md Option B
Basis:  one clock for damage, dated replacement, availability and CAS72
"""

import math

from stellarator_tea.modules.mfe_lifecycle.lifecycle_calendar import (
    Lifecycle_CalendarInput,
)

AUTO_IMPLEMENTED = False
_EPS = 1e-12


def _crf(i: float, N: float) -> float:
    if i == 0.0:
        return 1.0 / N
    p = (1.0 + i) ** N
    return i * p / (p - 1.0)


def _clip(value: float, lo: float, hi: float) -> float:
    """jnp.clip semantics verbatim: floor first, THEN cap (model.py:102-111)."""
    return min(max(value, lo), hi)


def lifecycle_calendar_held(cost_per_event, q_n, fluence_limit, availability,
                            interest_rate, operational_years, coil_life_fpy):
    """The retired periodic chain, verbatim (the held mode)."""
    core_lifetime_fpy = _clip(fluence_limit / max(q_n, 1e-6), 0.5,
                              operational_years * availability)
    core_lifetime_cal = core_lifetime_fpy / availability
    s = (1.0 + interest_rate) ** (-core_lifetime_cal)
    n_rep = max(0.0, float(math.ceil(operational_years / core_lifetime_cal)) - 1.0)
    pv = cost_per_event * s * (1.0 - s ** n_rep) / (1.0 - s)
    disc_pow_n = (1.0 + interest_rate) ** operational_years
    crf = interest_rate * disc_pow_n / (disc_pow_n - 1.0)
    cost = crf * pv
    F = operational_years * availability
    return dict(
        physical_life_fpy=core_lifetime_fpy, n_replacements=n_rep, productive_fpy=F,
        planned_downtime_yr=0.0, unplanned_downtime_yr=operational_years - F,
        terminal_downtime_yr=0.0, availability=availability, replacement_pv=pv,
        cas72_annual=cost, coil_life_margin_fpy=coil_life_fpy - F,
        dated_energy_ratio=1.0,
        events=[k * core_lifetime_cal for k in range(1, int(n_rep) + 1)],
    )


def _validate_live(q_n, fluence_limit, N, d, u, C, i, coil_life):
    vals = dict(q_n=q_n, fluence_limit=fluence_limit, N=N, d=d, u=u, C=C, i=i,
                coil_life=coil_life)
    for k, v in vals.items():
        if not math.isfinite(v):
            raise ValueError(f"Lifecycle Calendar: non-finite input {k}={v!r}")
    if (N <= 0.0 or fluence_limit <= 0.0 or q_n < 0.0 or d < 0.0 or C < 0.0
            or not (0.0 <= u < 1.0) or i <= -1.0):
        raise ValueError(f"Lifecycle Calendar: input outside domain {vals!r}")


def lifecycle_calendar_live(cost_per_event, q_n, fluence_limit, interest_rate,
                            operational_years, outage_years, unplanned_fraction,
                            coil_life_fpy):
    """The deterministic finite-horizon calendar (the live mode), as an interval walk."""
    N, d, u, C, i = (operational_years, outage_years, unplanned_fraction,
                     cost_per_event, interest_rate)
    _validate_live(q_n, fluence_limit, N, d, u, C, i, coil_life_fpy)
    b = 1.0 - u
    L = math.inf if q_n == 0.0 else fluence_limit / q_n
    t = F = T_p = T_u = T_term = 0.0
    events, segments = [], []
    while t < N:
        run = L / b
        if t + run >= N:
            dt = N - t
            F += b * dt
            T_u += u * dt
            segments.append((t, N))
            t = N
            break
        F += L
        T_u += u * run
        segments.append((t, t + run))
        t += run
        if t + d < N:
            events.append(t)
            T_p += d
            t += d
        else:
            T_term = N - t
            t = N
    pv = sum(C / (1.0 + i) ** t_k for t_k in events)
    A = F / N
    return dict(
        physical_life_fpy=L, n_replacements=float(len(events)), productive_fpy=F,
        planned_downtime_yr=T_p, unplanned_downtime_yr=T_u, terminal_downtime_yr=T_term,
        availability=A, replacement_pv=pv, cas72_annual=_crf(i, N) * pv,
        coil_life_margin_fpy=coil_life_fpy - F,
        dated_energy_ratio=_dated_energy_ratio(segments, b, N, i, F),
        events=events,
    )


def _dated_energy_ratio(segments, b, N, i, F):
    """Design D3: calendar-year bins (y-1, y] from commissioning; E_y = b x online
    time inside year y; PV(E_y) / (E_avg x sum of discounted year lengths)."""
    if F == 0.0:
        raise ValueError("Lifecycle Calendar: zero productive time -- energy undefined")
    n_years = int(math.ceil(N - _EPS))
    E_avg = F / N
    num = den = 0.0
    for y in range(1, n_years + 1):
        y0, y1 = float(y - 1), min(float(y), N)
        online = sum(max(0.0, min(s1, y1) - max(s0, y0)) for s0, s1 in segments)
        disc = (1.0 + i) ** (-y)
        num += b * online * disc
        den += E_avg * (y1 - y0) * disc
    return num / den


def lifecycle_calendar(inputs) -> dict:
    """Mode select (design D8): availability_direct_in == 0 -> live; (0, 1] -> held."""
    A_direct = inputs.availability_direct_in
    if not math.isfinite(A_direct) or A_direct < 0.0 or A_direct > 1.0:
        raise ValueError(f"Lifecycle Calendar: availability_direct_in {A_direct!r} outside [0, 1]")
    if A_direct > 0.0:
        return lifecycle_calendar_held(
            cost_per_event=inputs.cost_per_event, q_n=inputs.q_n_in,
            fluence_limit=inputs.fluence_limit_in, availability=A_direct,
            interest_rate=inputs.interest_rate, operational_years=inputs.operational_years_in,
            coil_life_fpy=inputs.coil_life_fpy_in)
    return lifecycle_calendar_live(
        cost_per_event=inputs.cost_per_event, q_n=inputs.q_n_in,
        fluence_limit=inputs.fluence_limit_in, interest_rate=inputs.interest_rate,
        operational_years=inputs.operational_years_in, outage_years=inputs.outage_years_in,
        unplanned_fraction=inputs.unplanned_fraction_in, coil_life_fpy=inputs.coil_life_fpy_in)


def calendar_events(inputs) -> list[float]:
    """Diagnostic (design D6): the event dates; not a channel."""
    return lifecycle_calendar(inputs)["events"]


def run_lifecycle_calendar(inputs: Lifecycle_CalendarInput) -> tuple[
    float, float, float, float, float, float, float, float, float, float, float
]:
    """Execute Lifecycle_Calendar -- returns the eleven outputs in the generated
    caller's unpack order (READ FROM modules/mfe_lifecycle/lifecycle_calendar.py
    AT THE REGENERATION AND RECORDED HERE; the placeholder order below is the
    SysML declaration order and is corrected if the caller differs)."""
    r = lifecycle_calendar(inputs)
    return (r["physical_life_fpy"], r["n_replacements"], r["productive_fpy"],
            r["planned_downtime_yr"], r["unplanned_downtime_yr"], r["terminal_downtime_yr"],
            r["availability"], r["replacement_pv"], r["cas72_annual"],
            r["coil_life_margin_fpy"], r["dated_energy_ratio"])
```

The old `generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` is deleted at regeneration; the generator moves nothing (it is not re-stencilled, it disappears with its calc), but if a `handwritten/backup/` directory appears the plan removes it and regenerates again to `New: 0, Preserved: N, Regenerated: 0` (memory `gotcha_codegen_manual_stage_regen`).

### Changed: `exploration/stellarator_e2e/verify_stellaris.py` (D1, MR-WI046-10; plan phase 3)
`IN`: drop `availability`; add `availability_direct = 0.0`, `outage_years = 0.5833333333333334`, `unplanned_fraction = 0.0`, `coil_life_fpy = 10.0`. New `_oracle_lifecycle_calendar(...)`: the closed form — `L = fluence / q_n`, `b = 1 − u`, `t_k = k L / b + (k − 1) d` for every `k` with `t_k + d < N`; then `F`, `T_p`, `T_u`, `T_term` from the dates (`T_term = N − t_last_limit` when the next limit `t_{K+1}` falls at or before `N − d` fails the strict rule … derived from the dates, not walked), the PV, CAS72, the margin and the year-binned ratio written from D3's statement; the held mode through the existing `_oracle_levelized_replacement_cost` plus D2's readings; the mode select as D8. `compute()`: `cal = _oracle_lifecycle_calendar(...)` after the wall peak; `availability = cal["availability"]` replaces `p["availability"]` at the fuel (`:616`), CAS72 (`:639-643` — now `cas72_annual = cal["cas72_annual"]`), DCF energy (`:655`) and 1cfe (`:665`) lines; the return dict gains the eleven outputs under `calendar__*`-mapped names.

### Changed: `exploration/stellarator_e2e/studies/oracle_entry.py` (plan phase 3)
`ENTRY_KEY_TO_ORACLE_INPUT`: `availability` → `availability_direct`, plus `outage_years`, `unplanned_fraction`, `coil_life_fpy`; `ORACLE_OUTPUT_TO_CHANNEL`: the eleven `calendar__*` channels; `cas72` objective channel `cas72_calc__cost` → `calendar__cas72_annual` in the manifest's objective catalog and the seam's map (the objective's name `cas72` unchanged); `OPERAND_BINDINGS` unchanged (no verdict).

### Changed: `exploration/stellarator_e2e/studies/study_route.py`, `tests/study/data/axes.known_answers.json`, `tests/study/data/availability_direct.expected.json` (renamed), `tests/study/test_known_answers.py` (D5; plan phase 4)

### Changed: `exploration/stellarator_e2e/run_stellaris_single.py` (D6, D9; plan phase 3)
`_cas72_guard_gate` restated: imports `lifecycle_calendar_held` and the oracle mirror; the three synthetic cases verbatim; a fourth family — the live boundary cases (spec MR-WI046-12) against the oracle's closed form and the research's expected values; prints the baseline's event dates in both modes. `EXPECTED_VERDICT_COUNT` unchanged by this item (WI-045 will have moved it to 13 before this item lands).

### Re-derived (D5, D10): `stellarator.snapshot.json`, `studies/manifest.json` (fingerprints; the `cas72` objective channel; the axis data; the headline re-pinned from the executed live LCOE), `tests/models/data/mfe_census.json` (expect +3 net), the six fixtures, `test_known_answers.py`, `generated/**`.

## Cross-file bindings

| Input | Bound to | Source file |
|---|---|---|
| `calendar.q_n_in` | `wall_peak_calc.wall_load_peak` | `mfe_plant.sysml` ← `'Neutron Wall Load Peak'` (WI-041) |
| `calendar.fluence_limit_in`, `operational_years_in`, `interest_rate` | `fluence_limit`, `operational_years`, `discount_rate` | instance bindings (unchanged) |
| `calendar.cost_per_event` | `replacement_cost_per_event` = `(blanket.capital_cost + divertor.capital_cost) · n_mod` | `mfe_plant.sysml` (unchanged; moves with WI-045's divertor account) |
| `calendar.outage_years_in`, `unplanned_fraction_in`, `coil_life_fpy_in`, `availability_direct_in` | the four new plant attributes | instance bindings (new) |
| `availability` (plant attribute) | `calendar.availability` (reference redefinition) | `mfe_plant.sysml` |
| `fuel_calc.availability_in`, `lcoe_calc.availability_in`, `lcoe_1cfe_calc.availability_in` | `availability` (unchanged text) | `mfe_plant.sysml` |
| `cas70_calc.cas72`, `cas72_annual` | `calendar.cas72_annual` | `mfe_plant.sysml` |

Dataflow stays unidirectional: wall chain → `calendar` → `availability` → fuel / LCOE; costs (`blanket`, `divertor`) → `calendar` → CAS72 → CAS70 → LCOE. No cycle: the calendar reads capital costs that depend on `p_th`, never on availability or CAS72. New import in the generic plant: `private import mfe_lifecycle::*;` beside the existing analysis imports.

## Expected baseline behaviour (MR-WI046-11; stated before regeneration)

**At the entering pin's other values** (the prototype's package state: `p_th` 3224.35, `cost_per_event` 816,069,911.57 $, `q_peak` 3.9788448937763854, `N` 30, `i` 0.07):

| Mode | `availability` | `n_replacements` | events [yr] | `productive_fpy` | `cas72_annual` [$/yr] | LCOE [$/MWh] | `dated_energy_ratio` | `coil_life_margin_fpy` |
|---|---|---|---|---|---|---|---|---|
| held (`availability_direct` 0.85) | `0.85` | `5.0` | 5.32, 10.64, 15.97, 21.29, 26.61 (the periodic chain's) | `25.5` | **`126649655.78572692`** (bit-identical; `==` the mirror and the pinned channel) | **`322.31843948570247`** (bit-identical) | `1.0` | `-15.5` |
| live (`availability_direct` 0.0; 7 months; `u` 0) | `0.9027777777777779` | `5.0` | `4.5239260339489915`, `9.631185401231317`, `14.738444768513641`, `19.845704135795966`, `24.95296350307829` | `27.083333333333336` | `136289876.0833351` | `305.18438420593134` | `1.0051616112988944` | `-17.083333333333336` |

In held mode every channel of the entering pin's set is bit-identical (`availability` enters every consumer as the double `0.85` it was; CAS72 as the same double) and the ten verdicts are unchanged — the identity the implementation proves by diffing `evidence/baseline_held/baseline_result.json` against `exploration/stellarator_e2e/studies/20260907-minor-radius/results/baseline_result.json`. If any channel differs, the work stops and derives why.

**At WI-045's package state** (this item integrates second): `cost_per_event` moves with the divertor account (`'Divertor Cost'` scales with `p_th`, which WI-045's live loop raises 3224.35 → ≈ 3301.45 MW), so the live CAS72 and LCOE differ from the table; the availability, the count, the dates, the margin and the ratio do not (they depend on `q_peak`, `d`, `u`, `N` only, none of which WI-045 touches). The plan re-states the live prediction in `evidence/baseline_before/` from WI-045's landed package before commit A. `work/active/WI-045_primary-loop-and-cycle/prototype/proto_results.json` did not exist when this design was written.

## Off-design predictions (`prototype/proto_results.json`; the implementation executes them)

| Point | `d` [yr] | `u` | `n` | `availability` | `cas72_annual` [M$/yr] | LCOE (entering-pin values) | note |
|---|---|---|---|---|---|---|---|
| A — five months | 5/12 | 0 | **6** | `0.9166666666666666` | 147.487 | 302.508 | the sixth restart at 29.64 < 30 |
| B — seven months, `u` 0.05 | 7/12 | 0.05 | 5 | `0.8576388888888889` | 131.272 | 320.307 | events 4.76 … 26.14 |
| C — seven months, `u` 0.10 | 7/12 | 0.10 | 5 | `0.8125` | 125.979 | 337.057 | |
| D — ten months | 10/12 | 0 | 5 | `0.8611111111111112` | 133.263 | 319.385 | |
| E — `c3343` (peak 9.039, R 11.2-class infeasible point) | 7/12 | 0 | **11** (held chain: 12) | `0.7861111111111112` | — (its own `cost_per_event`) | — | the calendar buys fewer and loses more |
| F — `c7752` (peak 4.040, feasible) | 7/12 | 0 | 5 (held 5) | `0.8911741898870316` | — | — | first event 4.456 vs held 5.242 |

A–D are executed at the baseline's levers with the calendar inputs moved; E and F through `study_route.run_points` in the committed record's `point()` shape (their `cost_per_event` is their own, so CAS72 is read from the execution and compared with the prototype re-run on the executed capital). Every non-calendar channel at E and F is predicted equal to the entering pin's value at the same coordinates except the availability-consuming ones (fuel, both LCOE forms, CAS70) — the item touches nothing else.

## Validation plan

1. Levels 1–3 pass on `models/` with the new package and the retired def; no new Level 2 warning; Levels 4–6 residue equal to the pre-change run except the retired calc's own rows.
2. `tests/models` after the twin sync: 48 / 13 or better, every delta explained (a test that counts calc defs or reads the CAS72 def by name is restated from the live tree with a dated comment).
3. Regeneration: `New: 1` (the calendar module), the old module and impl gone, `Regenerated` only on the changed non-manual modules (the plant), no `backup/` after the second pass, seal clean; the caller's unpack order read and recorded in the impl's docstring.
4. The held-mode diff (MR-WI046-11): every channel bit-identical; the eleven new channels at D2's held values; the verdicts unchanged; single-runner parity; the oracle gate passes in both modes.
5. The live-mode execution: the eleven channels equal the prediction (re-stated at WI-045's package state) to 1e-9 relative; oracle parity 0.0 on all eleven; the closed form and the walk agree at every event.
6. The boundary cases (MR-WI046-12) pass in the single runner's gate and in a `tests/models` test that imports the impl and the oracle functions directly.
7. Re-pin by producers; census +3 net with the predicted key delta; the axis renamed and its fixture re-derived; `tests/study` green apart from the branch's known fail-closed set.
8. SV-063 (held identity), SV-064 (live at the design point with oracle parity), SV-065 (boundary cases) `passing`; trace rows for the calc and the four bindings.

## Validation report (prototype, 2026-09-08)

`prototype/proto.py` → `proto_results.json`, run with `uv run python`: `held_equals_mirror: true` (CAS72 `126649655.78572692` by `==` against the oracle mirror and the pinned channel); the live design point as tabled; the seven arms; the closed form agreeing with the walk at every event of every arm; the time identity ≤ 3.6e-15 yr in every case; the synthetic cases at the research's expected values (§ Research findings); the three single-runner guard cases equal on the held mode; the long-horizon limit within 0.1 % of `L / (L + d)`; `productive_fpy` non-increasing in `u`. No model file was touched (T-003's exclusions); Levels 1–6 run in the plan's phase 1.

## Implementation checklist (phased; the plan carries the checkboxes)

1. Wait for WI-045's commit B; re-read the shared sites at that state; write the model edits (the new file, the retirement, the plant, the instance); Levels 1–3; twins; `tests/models`.
2. The MR-WI046-15 restatement and the predictions re-stated at WI-045's package state; `evidence/baseline_before/`; commit A.
3. Regeneration (twice if a backup appears); the impl restored on the stencil's names with the caller's unpack order; the oracle and the seam; the route and the single runner; the held-mode diff; the live execution; A–F.
4. Re-pin; the axis rename and fixture; batteries; SV and trace rows; commit B.
5. `tests/study` run of record; commit C.

## Risks

1. **The reference redefinition `availability = calendar.availability` mints no producer channel** (the WI-028 bare-alias class). *Likelihood: low* (the `magnet.m_casing = casing_mass.m_casing` precedent minted one). *Mitigation:* D4's fallback — the three consumers read `calendar.availability` directly; recorded in the phase-3 record.
2. **The plant's `fuel_calc` usage precedes `calendar` in file order.** *Likelihood: low* that the exact route cares. *Mitigation:* Levels 1–3 before the twins; if it does, the calendar block moves above the fuel block (a text move, no meaning change).
3. **The regeneration leaves a `handwritten/backup/`** from the deleted impl. *Mitigation:* the two-pass recipe.
4. **A literal count of channels or modules hides in a test.** *Mitigation:* the batteries; each restated from the live package with a dated comment.
5. **WI-045's package state changes `cost_per_event` so the design's live CAS72 is stale.** *By design:* the plan re-states it before commit A (D10); the availability, count, dates and ratio are invariant to WI-045.
6. **The held mode differs at one ulp because the impl's `_crf` is not the retired chain's inline CRF.** *Mitigation:* `lifecycle_calendar_held` carries the inline `disc_pow_n` / `crf` lines verbatim (above), not `_crf`; the prototype's `==` is on that form.
7. **A reader takes 0.9028 as an achieved availability.** *Mitigation:* the label on `unplanned_fraction`, the calc doc's "conditional on the in-vessel maintenance calendar", the study's stress arms beside every availability.

## Approval

The owner delegated the modelling judgement at grounding (`goal.md` § Reserved gates); this design proceeds to the plan under that delegation, as WI-044 did. The fresh round review is the independent check; `/review-model` is available if the owner wants one before the round closes.
