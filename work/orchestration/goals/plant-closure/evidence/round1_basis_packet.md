# Round 1 basis packet — the shared interface every item builds on — 2026-09-08

`[AGENT]` under `goal.md` § Reserved gates 1–7. This is the one page the three item specs (WI-045, WI-046, WI-047) cite for what they share, so that three items touching the same four files land without contradicting each other. It fixes interfaces and names; the items' designs fix mechanisms inside them. A design that finds a line here wrong amends this packet by a dated note and says so in its own text; nothing here is silently overridden.

## 1. The four verifications the strategy's assumptions needed (done 2026-09-08)

| Assumption | Checked | Result |
|---|---|---|
| The study store persists multi-output channels at the entering pin | `exploration/stellarator_e2e/studies/20260907-minor-radius/results/points.csv` | `W_th_MJ_store` is populated from the store (258.89442055162493 on the first row) — a `sustain__*` multi-output field read back from evidence, the schema-v3 repair live; the same record also carries `_oracle` columns for `p_net`, `p_aux_required`, `tau_E`. A new multi-output module publishes to the store; the exporter declares its map. |
| The codegen arithmetic envelope | `~/1cfe/sysml-codegen/src/sysml_codegen/extraction/calc_compat_renderer.py` `_ARITHMETIC_OPERATOR_MAP` | `+ - * / ** ^` only. **The cycle fit (a logarithm) and the calendar (a loop over dated events) go to the handwritten stage**; the loop, the fuel flows, the divertor ledger and the gas load are flat arithmetic. |
| The constraint-def pattern | `models/library/analyses/mfe_viability.sysml` (`'Burn Hold'` 249–314) | `constraint def 'Name' { doc; in attribute x_in : Real; <expression> }`, asserted at the plant as `assert constraint name_ok : 'Name' { in x_in = <channel>; }`. A two-sided bound is one constraint on a product of margins. |
| The shared route's publication contract | `exploration/stellarator_e2e/studies/study_route.py` 194–227; `ANNEX.md` § Numeric publication | `run_points(..., required_channels=)` refuses evidence lacking a declared column before persisting; a nonfinite value is kept and the exporter refuses it. A new study passes its own map. The route asserts `EXPECTED_CONSTRAINT_COUNT` at 49. |

## 2. The quantity ledger — one producer per quantity

Channel keys are `stellarator_09__stellaris__<usage>__<output>`; the usage names below are the ones the plant wiring uses, so the study's column map can be written from this table.

| Quantity | Producer (usage · output) | Consumers | Held-mode value |
|---|---|---|---|
| Reactor source heat `q_source` [MW] = `mn·p_n + p_α + p_coupled`, no pump credit | the power balance (`pb__q_source`, a new output) | the loop; the heat ledger's reporting | unchanged |
| Loop mass flow, outlet temperature, per-loop flow, per-path pressure loss, compressor pressure ratio, compressor inlet temperature | `loop__mdot`, `loop__T_out`, `loop__mdot_loop`, `loop__dp_loop`, `loop__r_comp`, `loop__T_comp_in` (WI-045, `'Primary Coolant Loop'`) | the cycle (`T_out`); the two loop verdicts; the study | computed regardless of mode (the chain always evaluates) |
| Circulator fluid work, loop electrical draw, IHX duty | `loop__w_fluid`, `loop__p_elec`, `loop__q_ihx` | reported | computed regardless |
| Pump electrical to the recirculating sum | `loop__p_elec_live` = `loop_live · p_elec`; the plant sums `p_pump_total = loop.p_elec_live + p_pump_direct` | the power balance (`p_pump_total_in`, replacing `p_pump_in`) | `0.0 + 195.0` = 195.0 exactly |
| Recovered pump heat to the thermal sum | `loop__q_recovered_live` = `loop_live · w_fluid`; the plant sums `q_recovered = loop.q_recovered_live + eta_p_direct · p_pump_direct` | the power balance (`q_recovered_in`, replacing `eta_p_in · p_pump_in`) | `0.0 + 0.5 · 195.0` = 97.5 exactly |
| Cycle turbine-inlet temperature, fitted efficiency, domain margins | `cycle__T2_C`, `cycle__eta_fit`, `cycle__margin_low`, `cycle__margin_high` (WI-045, `'Power Cycle Efficiency'`, handwritten) | the domain verdict; the study | computed regardless |
| Thermal efficiency to the power balance | `cycle__eta_th` = `cycle_live · eta_fit + eta_th_direct` | the power balance (`eta_th_in`) | `0.0 · eta_fit + 0.333` = 0.333 exactly |
| Physical first-wall life, replacement count and dates, productive FPY, planned / unplanned / terminal downtime, availability, replacement PV, CAS72, coil-life margin, dated-energy ratio | `calendar__physical_life_fpy`, `__n_replacements`, `__productive_fpy`, `__planned_downtime_yr`, `__unplanned_downtime_yr`, `__terminal_downtime_yr`, `__availability`, `__replacement_pv`, `__cas72_annual`, `__coil_life_margin_fpy`, `__dated_energy_ratio` (WI-046, `'Lifecycle Calendar'`, handwritten; event dates as a diagnostic artifact, not channels) | `availability` (the plant attribute, bound by reference to `calendar.availability` — the WI-044 `m_casing` pattern), read by fuel, both LCOE forms and the study; `cas72_annual` into the CAS70 rollup | `availability_direct` 0.85 selects the held mode: availability = 0.85 and CAS72 by the periodic chain verbatim (the retired `'Levelized Replacement Cost'` arithmetic carried inside the new impl) |
| Tritium burn, injection, exhaust, permanent loss rates, required breeding ratio, adequacy margin, annual burn mass | `fuel__burn_rate`, `__inject_rate`, `__exhaust_rate`, `__loss_rate`, `__tbr_required`, `__tbr_margin`, `__burn_kg_per_fpy` (WI-047, `'Fuel Cycle Flows'`) | the gas load; the study; **no fence** (§ 6) | computed regardless |
| Absorbed heating, separatrix power, edge radiated fraction, non-radiated target load, peak target flux (fixed geometry), the R-scaled shadow, margin | `divheat__p_heat_abs`, `__p_sep`, `__f_rad_edge`, `__p_target_nonrad`, `__q_target_peak`, `__q_target_peak_area_scaled`, `__q_target_margin` (WI-047, `'Divertor Heat Ledger'`) | `divertor_heat_ok`; the study | computed regardless |
| Gas throughput after recombination, required effective speed at the declared exhaust pressure | `vacuum__Q_total`, `__S_eff_required` (WI-047, `'Vacuum Gas Load'`) | reported | computed regardless |
| Operating-versus-installed heating difference | `divheat__p_heat_operating_minus_installed` = `sustain.p_aux_required − heat.p_coupled` | reported (§ 5) | — |

Retired entry points: `p_pump`, `eta_p`, `eta_th`, `availability` as direct instance scalars (they become `p_pump_direct`, `eta_p_direct`, `eta_th_direct`, `availability_direct` with the live flags `loop_live`, `cycle_live`). New entry points: the circuit facts, the fit coefficients and domain, the outage and unplanned fraction, the coil life, the fuel and divertor facts, the exhaust pressure. Each spec lists its own census delta.

## 3. Dormancy and the held-reproduction rule

Every new chain carries either a `0/1` live flag on the quantity it feeds into an existing sum, or an additive direct term, or both, in flat arithmetic. The rule that makes the compatibility arm bit-exact: **the dormant contribution is formed as `0.0 · x + held` and enters the existing sum at the same position the held scalar used to occupy.** IEEE-754 gives `0.0 · x = 0.0` for finite `x` and `0.0 + held = held` exactly, so the old left-to-right operation sequence is preserved to the bit. Each item's design states this for its own sum and proves it by executing the dormant package against the entering pin's `baseline_result.json` (every channel of the old set bit-identical; the old ten verdicts unchanged). A chain that cannot be made dormant this way is a `PREREQUISITE` return, not a scope change.

The handwritten calendar selects its mode by `availability_direct > 0` (held: the periodic chain; live: the calendar); the handwritten cycle by `cycle_live` inside flat arithmetic on its output. Both impls carry both semantics in their docstrings and the oracle mirrors both.

The instance binds the live values: `loop_live 1.0`, `cycle_live 1.0`, `p_pump_direct 0.0`, `eta_p_direct 0.0`, `eta_th_direct 0.0`, `availability_direct 0.0`. The compatibility arm binds `0.0, 0.0, 195.0, 0.5, 0.333, 0.85`. The generic plant's defaults are the dormant ones, so a concept that binds no circuit still executes (MR-3; the WI-024 / WI-039 pattern).

## 4. The verdicts added and where the count moves

Four new asserts, all with computed operands against instance-bound limits: `loop_pressure_ok` (`p_loop − dp_loop > 0`), `loop_capacity_ok` (`mdot_loop ≤ mdot_loop_rated`, the reference per-loop flow), `cycle_domain_ok` (`(T2_C − T2_min)·(T2_max − T2_C) ≥ 0`), `divertor_heat_ok` (`q_target_peak ≤ q_target_limit`). Ten → fourteen. The literal count sites, each restated with a dated comment by the item that adds its verdict: `study_route.py:49` (`EXPECTED_CONSTRAINT_COUNT`), `run_stellaris_single.py:74` (`EXPECTED_VERDICT_COUNT`, and `EXPECTED_VERDICTS`), `tests/study/test_operand_bindings.py`, `tests/study/test_valid_empty.py`, `tests/study/test_known_answers.py` (bounds / `constraints_unreachable` / the fixture contract), `studies/manifest.json` `baseline.verdicts`, `oracle_entry.OPERAND_BINDINGS` (one entry per new constraint id read from `generated/contracts/model_contract.json`).

"Feasible" in every study count names its set: the old ten, or the fourteen.

## 5. The heat ledger and the heating basis in round 1

- `q_source = mn·p_n + p_α + p_coupled` is the reactor's heat with no pump credit; the loop's fluid work is recovered into the IHX duty once (`q_ihx = q_source + w_fluid`), and `p_th` to the cycle is `q_source + q_recovered` — the same joules, one destination each.
- **The thermal sum keeps the installed coupled heating (`heat.p_coupled`, 50 MW) in round 1** — the compatibility rule. The divertor ledger's absorbed heating is `sustain.p_alpha_heat + heat.p_coupled` on the same basis, and the operating-versus-installed difference (`sustain.p_aux_required − heat.p_coupled`, −0.92 MW at the design point, much larger elsewhere) is a reported channel, not blended into any attribution. Moving the plant to operating heating is a named follow-on.
- Radiation is a destination of the absorbed heating, never added to it: `p_sep = p_heat_abs − p_rad_core` with `p_rad_core = sustain.p_rad`; the source's 90 % is a **total** radiated fraction, so `f_rad_edge = (0.9·p_heat_abs − p_rad_core) / p_sep` is derived and reported (a value outside `[0, 1]` is an inconsistent assumption, reported, not clamped); the non-radiated target load is `0.1·p_heat_abs`.
- The source's divertor case (90 % radiated, 500 → 50 MW) and its first-wall case (100 % radiated) are different load cases and are never summed.

## 6. What is surfaced as missing, and how each calc executes without it

| Missing input | Home | Handling in round 1 | Retrieval target |
|---|---|---|---|
| Residual unplanned outage fraction | WI-046 `unplanned_fraction` | instance 0.0 with the label "equivalent availability conditional on the in-vessel maintenance calendar; unplanned failures not modelled"; 0.05 / 0.10 declared stress arms in the study | none admissible (a reliability basis) |
| Compressor drive / motor boundary | WI-045 `eta_drive` | 1.0 — the source's printed circulator figure is the boundary (130.8 printed ≈ 129.4 fluid work); electrical draw is a disclosed lower bound (the WI-033 pattern) | Moscato's preliminary circulator design |
| Physical tritium recovery of the unburned stream | WI-047 `t_recycle` | **open decision for the owner** (§ 8): the existing `fuel_recovery` 0.99 read as the physical recovery makes `tbr_required` 1.19 against 1.074 — reported as `fuel__tbr_margin`, **not a fence**; the study's transect over 0.99–1.0 locates the 0.9961 threshold | UKAEA STEP fuel-cycle paper (Lord et al.) |
| Isotope residence times, breeder extraction efficiency, startup reserve | WI-047 `I_total`, `eta_extract`, `G_stock` | dormant 0 / 1.0 / 0 with the label; inventory and startup stock **not computed** in round 1 (a bounded negative unless sourced) | the same STEP paper |
| Exhaust boundary pressure, gas temperature, duct conductance | WI-047 `p_exhaust`, `T_gas` | `T_gas` 300 K stated as a convention; `p_exhaust` 1.0 Pa declared so `S_eff_required` is the throughput's own value per pascal, labelled "declared, not sourced" | W7-X pumping / ITER torus cryopump specifications |
| Target-area scaling with machine size | WI-047 `q_target_peak_area_scaled` | fixed geometry is the verdict's operand (the sourced case); the `R_ref / R` scaling is a reported shadow only | new transport / geometry cases |
| Primary equipment, processing-plant, building costs | — | not modelled; dispositions in § Answered when (c) | cost sources with scope |

## 7. Expected behaviour at the design point (the probe, `grounding_probe/summary.md`; each design's prototype corrects)

| | Held mode (compatibility) | Live |
|---|---|---|
| Every channel of the entering pin's set; the old ten verdicts | **bit-identical** (LCOE 322.31843948570247) | move as below |
| `loop__p_elec` / `q_recovered` / `p_th` | 195.0 / 97.5 / 3224.352676 | 174.60 / 174.60 / 3301.450 (14 loops, per-loop 215.0 vs rated 225.1, dp 300.5 kPa, `r` 1.0390, η_is 0.777 by source-point calibration) |
| `cycle__T2_C` / `eta_th` | 480 / 0.333 | 480 / 0.41136 (Rankine, He primary; sCO2 0.37518 as an arm) |
| `calendar__availability` / `n_replacements` / CAS72 | 0.85 / 5 / 126.65 M$/yr | 0.9028 / 5 (4.52, 9.63, 14.74, 19.85, 24.95 yr) / ≈ 134.9 M$/yr at `u` 0 |
| `divheat__q_target_peak` (pessimistic case 9.5 at 50 MW) | 10.52 MW/m² (`p_heat_abs` 553.6, `p_sep` 333.9, `f_rad_edge` 0.834) | same |
| `fuel__tbr_required` / `tbr_margin` at `t_recycle` 0.99, no decay, no stock | 1.19 / −0.116 | same |
| LCOE | 322.318439 | ≈ 224.08 (`u` 0) / 235.14 (`u` 0.05) |
| Verdicts | ten satisfied; the four new ones read on the live chains | thirteen satisfied; **`divertor_heat_ok` violated** (10.52 against 10 on the pessimistic case; 5.54 on the low case) — disclosed, never tuned (the WI-041 precedent) |

## 8. Open decisions each spec must close, with the packet's recommendation

1. WI-045: sized-flow mode (flow from `q_source` and a held blanket rise) versus held-flow mode — **sized flow**; the loop count an instance integer sized at the design point (14) and held; the pressure-loss law at nominal density with the constant-property error bounded in the design.
2. WI-045: the loop file split (`mfe_primary_loop.sysml` + `mfe_power_cycle.sysml`) and the power balance's formals (`q_recovered_in`, `p_pump_total_in` replacing `eta_p_in`, `p_pump_in`) — **as named here**.
3. WI-045: the fit's version contract — **the printed Table 4 form with the literal 273** (`ln(T2_C + 273)`), Δη 0 and said so; Kovari 2016 registered through `scripts/source_registry.py register` before the coefficients are bound.
4. WI-046: `'Levelized Replacement Cost'` — **retired from the plant and the library**, its guarded chain carried verbatim as the calendar impl's held mode with the history in the docstring; the handwritten backup mechanics per `gotcha_codegen_manual_stage_regen`.
5. WI-046: payment at outage start; restart-strictly-before-horizon; the annual-equivalent convention with `dated_energy_ratio` as the shadow — **as the research's Option B**.
6. WI-047: the recovery semantics — **surfaced to the owner** (§ 6); the calc reads the existing 0.99 and publishes the margin; no fence.
7. WI-047: the divertor case bound in the instance — **the pessimistic case (9.5 at 50 MW)**, the low case a study arm; the verdict on fixed geometry; the R-scaled shadow reported.
8. WI-047: the gas load counts molecules (D₂/T₂/DT as atoms/2, helium atomic) at `T_gas` 300 K.

## 9. File ownership and the integration order

| Item | Owns (new) | Edits (shared, in this order) | Must not touch |
|---|---|---|---|
| WI-045 | `models/library/analyses/mfe_primary_loop.sysml`, `mfe_power_cycle.sysml`; `generated/handwritten/mfe_power_cycle/` | `mfe_power_balance.sysml` (formals; `q_source` output); `mfe_plant.sysml` lines 415–419 (attributes) and 484–500 (`pb` wiring), the `loop` / `cycle` usages, two asserts; `stellarator_plant.sysml` 779–785 and the circuit / fit bindings; `verify_stellaris.py` power balance; `oracle_entry.py` levers and two bindings; the twins | the CAS72 chain, `availability`, the fuel / divertor / vacuum quantities |
| WI-046 | `mfe_lifecycle.sysml`; `generated/handwritten/mfe_lifecycle/` | `mfe_account_costs.sysml` (retire 795–890); `mfe_plant.sysml` 952–970 and 1000; `stellarator_plant.sysml` 1117 and the outage / fraction / coil-life bindings; `verify_stellaris.py` CAS72 / availability; `oracle_entry.py`; the twins | the power balance, the loop, the cycle |
| WI-047 | `mfe_fuel_cycle.sysml`, `mfe_divertor_heat.sysml`, `mfe_vacuum.sysml` | `mfe_plant.sysml` (three usages, one assert); `stellarator_plant.sysml` (the facts and the labels); `verify_stellaris.py`; `oracle_entry.py` (levers, one binding); the twins | `'DT Fuel Cost'` (its cost semantics stay), the calendar, the loop |

Integration is **sequential: WI-045, then WI-046, then WI-047**, each on one coordinated pass (twins → regeneration → oracle → baseline diffs in both modes → re-pin by the producers → batteries → SV rows → commit with a pathspec). Designs and prototypes run in parallel before that. One `integrate` pin after the third. The compatibility proof is re-executed on the final package: every direct term held → the entering pin bit-for-bit.

## 10. What the study exporter will declare

Its `required_channels` map is every `<usage>__<output>` in § 2 plus the existing objective catalog; the fourteen verdicts by `source_local_identity`; the arms' lever values (`loop_live`, `cycle_live`, the four direct terms, `outage_years`, `unplanned_fraction`, `dT_blanket` / `T_in`, `n_loops`, the divertor case pair, `t_recycle`, `burn_fraction`); the join columns to the committed `20260907-minor-radius` record by case id. Written when the study is scoped, from this table.

## Amendment 2026-09-08 — what the three spec writers found (recorded, the sections above unedited)

1. **§ 7's divertor numbers were computed on the operating basis** (`p_aux_required` 49.08) while § 5 fixes the installed basis (`heat.p_coupled` 50) for round 1. On the installed basis: `p_heat_abs` 554.49, `p_sep` 334.77, `f_rad_edge` 0.8344, `q_target_peak` 10.535 (pessimistic) / 5.545 (low). 0.17 % apart; no verdict changes; the WI-047 spec carries the installed-basis values. The operating-minus-installed channel is a `'Divertor Heat Ledger'` output (`divheat__p_heat_operating_minus_installed`), as § 2's last row says.
2. **§ 7's CAS72 and LCOE are the all-three figures.** Each item states its own prediction at its own package state in the § 9 order: WI-045 alone at held availability 0.85 (the prototype supplies it; the WI-045 spec's ≈ 259 is a placeholder marked as such), WI-046 after WI-045 (the calendar-only oracle arm reads 133.03 M$/yr and 304.61 $/MWh at the entering pin), WI-047 last.
3. **§ 4's count is staged:** WI-045 takes the verdict set 10 → 13, WI-047 adds the fourteenth; WI-046 adds none. Each restates the count sites it moves.
4. **The `availability` study axis** (`study_route.py` `AXES`, the known-answer fixture `availability.expected.json`) is not addressed above: WI-046's design decides whether the axis retires or renames to `availability_direct` (its open decision 5), and the fixture contract restates accordingly.

## Amendment 2026-09-08 (2) — what the three designs corrected (recorded; the designs are authoritative for their items)

1. **Names (WI-045 D3, D9).** `q_source` is produced by its own calc `'Reactor Source Heat'` as `source_heat__q_source` (a `pb → loop → pb` edge would be a module-graph cycle); the loop's two dormant aggregations are its own outputs, `loop__p_pump_total` (= `loop_live·p_elec + p_pump_direct`) and `loop__q_recovered_total` (= `loop_live·w_fluid + eta_p_direct·p_pump_direct`), replacing § 2's `pb__q_source`, `loop__p_elec_live`, `loop__q_recovered_live` and the plant-level sums.
2. **Numbers (WI-045 D2; WI-046 D3, item 10).** The compressor calibration is `eta_is` 0.772796639536644 (the probe solved the isentropic rise on the wrong end of the compression); the design-point loop draw is 175.4365 MW, not 174.60; loop-only LCOE 305.81, loop + cycle at held availability 237.25. The calendar's live CAS72 at the entering pin is 136,289,876.08 $/yr (dated events, the first at 4.52 yr), not the probe's 133.03 (which fed the live availability into the periodic chain); calendar-only LCOE 305.18; `dated_energy_ratio` 1.00516; the coil-life margin −17.08 FPY. § 7 stands as the probe's record; these are the item predictions.
3. **The loop-capacity finding (WI-045 D6).** At 14 loops sized 4.5 % under the rating at the design point, nearly every committed point off the design column violates `loop_capacity_ok` (`c2823` at 431 kg/s per loop against 225), and `c2823` re-sized to 27 loops reads every verdict satisfied at 171.23 $/MWh against 250.53 at 14. The loop count is an unpriced instance integer: the study carries a per-point re-sized arm (`n_loops = ceil(mdot / mdot_loop_ref)`) beside the fixed-count arm, and no LCOE along `n_loops` is read as an optimum (R7.S is a disposition, § 6).
4. **The divertor finding (WI-047 D8).** On the pessimistic case at fixed geometry `c2823` reads 20.33 MW/m² and the highest-fusion feasible point 22.54: the fence closes every committed cheap machine; exact satisfaction sits at 526.3 MW absorbed heating. The strategy's abandonment condition names this as a valid adverse reading the study measures (with the low case and the R-scaled shadow beside it), never a limit to move.
5. **Two mechanics decided at regeneration, fallbacks named:** whether the exact route accepts a product on a calc input binding (WI-047: a plant attribute otherwise) and whether a reference binding mints a channel (WI-046 D4: bare-alias fallback); the census's treatment of calc-formal defaults (`s_per_fpy`, `k_B`).
