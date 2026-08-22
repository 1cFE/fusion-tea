# Study record — 20260821-power-cycle-ab

## 1. Study header

- **Study id:** `20260821-power-cycle-ab`
- **Package:** `stellarator_e2e` (`exploration/stellarator_e2e/generated`, `stellarator_tea`, runtime contract 2.0.0, sealed after WI-030)
- **Date executed:** 2026-08-22 (record opened 2026-08-21; the study id keeps its minted date)
- **Executor:** Claude (RUN-STUDY Item 6 Phase 2 session, branch `feat/run-study-first-consumer`)
- **Mode:** execute
- **Arms:** `arm-rankine-paper`, `arm-rankine-upstream`, `arm-sco2`, `arm-sco2-eta-only`

Arms are variants of the same question, run to be compared. Two studies asking different
questions of the same package are two records, not two arms of one.

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> Compare steam Rankine against sCO2 on the stellarator
> Run sensitivity analysis on other axes for each type
> Try to find a non-intuitive result on the interactions

*(Owner, 2026-08-21, verbatim; three bullets as given.)*

**Executor's additions (mine, not the owner's):**

- "Steam Rankine" and "sCO2" are represented as the power-conversion block the package exposes: `eta_th`, the turbine rate (`turbine__cost_per_mw`, CAS23) and the heat-rejection rate (`heat_rejection__cost_per_mw`, CAS26). That is exactly what 1costingFE's cycle presets carry (`defaults.py:578-593`); CAS24/CAS25 and the primary pumping power are cycle-independent (DI-007). The cycle is the secondary side; the Stellaris primary coolant is helium regardless.
- Four arms, not two. The Stellaris paper assumes "a simple electrical conversion efficiency of 1/3" and names no cycle (`raw.pdf` p. 3). Its cost rates in the model are the upstream *Rankine* preset, but its efficiency is not (upstream Rankine is 0.40). So `arm-rankine-paper` (η 0.333, the model as built) and `arm-rankine-upstream` (η 0.40) separate "paper vs upstream" from "Rankine vs sCO2"; `arm-sco2` is the upstream sCO2 preset (η 0.47, lower rates). The fourth, `arm-sco2-eta-only` (η 0.47 with the Rankine rates), was recommended by the pre-execution critique and added on the owner's yes (2026-08-22) so an sCO2 difference splits into an efficiency part and a cost-rate part. "Rankine" in the arm labels is this study's label, not the paper's.
- "Other axes for each type" was taken at intake as: the two geometry levers the proof-of-life searched (`R`, `a`, same window) and the two economic levers it and the known-answer set already declare (`availability`, `discount_rate`), each swept identically in every arm. The two economic axes were then traced, came back `no_constraint_response`, and were declined by the owner (§ 8, 2026-08-22); they are held at baseline in every point. What ran is the same (R, a) grid under each of the four cycle blocks. No new axis is invented; the interaction question is answered by running the same geometry axes under each cycle.
- "Interactions" is read as: does the cycle change *where* the constraints bind and *which* one binds (the feasible region over R, a), and does it change the *shape* of the economic-lever responses, not only their level. The "non-intuitive result" is something to look for in the data, not a hypothesis fixed in advance; whatever is found is reported with its evidence, and "nothing non-intuitive found" is an acceptable answer.
- Every point runs on the one sealed package (post-WI-030, six constraints); the arms differ only in the three block values, so one fingerprint, one store.

## 3. Objective and result

- **LCOE objective channel(s):** `stellarator_09__stellaris__lcoe_calc__lcoe` ($/MWh; `stellarator_09__stellaris__lcoe_1cfe_calc__lcoe` is also exported as `lcoe_1cfe`)
- **LCOE result:** per arm, at the baseline geometry (R 12.7 m, a 1.3 m) and at the best feasible point of the (R, a) grid (`results/points.csv`, columns `arm_id`, `R`, `a`, `lcoe`, `feasible`):

| Arm | η | LCOE at baseline geometry | Best feasible LCOE | at (R, a) |
|---|---|---|---|---|
| `arm-rankine-paper` | 0.333 | 275.264 | 209.000 | (14.0, 1.65) |
| `arm-rankine-upstream` | 0.40 | 229.191 | 176.477 | (13.5, 1.65) |
| `arm-sco2-eta-only` | 0.47 | 196.299 | 152.787 | (13.0, 1.65) |
| `arm-sco2` | 0.47 | 194.638 | 151.187 | (13.0, 1.65) |

Over the studied space the objective behaves the same way in every arm: it falls with `a` until the wall-load fence at a = 1.65 m, and along that fence it has a shallow interior minimum in R (within 0.1 $/MWh over R 13–15 m). The arm ordering — `arm-sco2` cheapest, then `arm-sco2-eta-only`, then `arm-rankine-upstream`, then `arm-rankine-paper` — holds at all 948 grid points; no geometry reverses it. Splitting the sCO2 difference: at the baseline geometry, η 0.40 → 0.47 is worth −32.9 $/MWh (−14.4 %) and the cheaper sCO2 turbine and heat-rejection rates a further −1.7 $/MWh (−0.8 %); over the points feasible in both arms the rate effect is between −0.5 % and −1.1 % of LCOE and the efficiency effect between −13.3 % and −23.4 %. The unconstrained minimum of every arm lies past the wall-load fence (a = 2.2, R 8.5–9.0 m, `wall_load_ok` violated), so `wall_load_ok` is the active constraint at every arm's optimum.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status. Status is per arm over the 948-point grid (`results/points.csv` verdict columns, named by `source_local_identity`); the qualified ids are the catalog's (`results/baseline_result.json` `verdicts[]`).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | `beta_ok` | satisfied | at every point of every arm; β is computed from profiles and `magnet__B` (WI-030), which no axis of this study touches — inert by construction, identical across arms |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | `net_positive` | satisfied | at every point of every arm, including the (4.0, 0.8) corner where the oracle scan shows p_net of 8.3 / 36.2 / 65.5 MW by η (`results/oracle_scan.json`); the cycle block reaches it, but the window never drives net power negative |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | `peak_field_ok` | satisfied | at every point; B_peak = 24.9 T = B_max in every arm, untouched by any axis here — inert, identical across arms |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | `recirc_ok` | violated at 32 / 17 / 10 / 10 points (paper, upstream, sco2-eta-only, sco2), satisfied elsewhere | the small-machine corner: violated at R ≤ 8.0 m for a = 0.8 in the paper arm, R ≤ 6.5 in the upstream arm, R ≤ 5.5 in both η 0.47 arms (threshold 0.5); the fence moves inward as η rises; the two η 0.47 arms are identical here (the rates do not enter rec_frac) |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | `tbr_ok` | satisfied | at every point; TBR is a bound input (1.074 vs floor 1.05) — inert, identical across arms |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | `wall_load_ok` | violated at 353 points per arm, satisfied elsewhere | violated at a ≥ 1.70 m for every R (wall load 4.165 MW/m² at a = 1.70 against the 4.05 limit; 4.035 at a = 1.65); in this model wall load at fixed profiles depends on `a` alone, so the fence is a horizontal line in (R, a) and is identical in all four arms |

No verdict is `indeterminate` anywhere. Three verdict combinations occur in the whole study (all satisfied; only `wall_load_ok` violated; only `recirc_ok` violated), each in every arm; no point violates both. The three inert verdicts are the structural limit the critique named (§ 14): no cycle value reaches β, B_peak, or TBR, so nothing in this study could have moved them.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `R` | search | Reaches `net_positive`, `recirc_ok`, `wall_load_ok` through computed operands (`indicators.json`); the proof-of-life found both fences and a constrained optimum on this axis, and the oracle scan shows both fences inside the window in every arm. |
| `a` | search | Same reach as `R`; the wall-load fence is set by `a` first (wall area ∝ a at fixed R, fusion power ∝ a²). |
| `availability` | sensitivity | `no_constraint_response` (sound negative): no constraint operand is reachable. The oracle scan moves LCOE 455 → 248 $/MWh at baseline geometry with no verdict change. Proposed as sensitivity; declined by the owner's ruling (§ 8) before any point ran. |
| `discount_rate` | sensitivity | `no_constraint_response`: reaches only CAS72, the two LCOE forms (levelization and IDC). Scan: 163 → 485 $/MWh, no verdict change. Proposed as sensitivity; declined by the owner's ruling (§ 8) before any point ran. |
| cycle block (the arms) | search | The arms are the levels of one categorical axis: each holds a fixed (η, turbine rate, heat-rejection rate) triple. It reaches `net_positive` and `recirc_ok` through `p_et` and the recirculating sum, so the question is whether the feasible region and the active constraint move with it — search framing. Not a numeric sweep. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `R` | search | no | Verdict structure found: `recirc_ok` fences the small-R corner (the fence position depends on the arm), and the constrained LCOE minimum is interior in R (13–14 m along the a = 1.65 fence) in every arm. Feasible fraction 59–62 % per arm, inside the policy § 7 H1 band. |
| `a` | search | no | `wall_load_ok` fences a ≥ 1.70 m at every R in every arm; the LCOE optimum sits on that fence. The fence is a function of `a` alone. |
| `availability` | not run | — | Declined by the owner's ruling before execution; held at 0.85 in every point. The proposed sensitivity framing was never tested and no account is owed (§ 6). |
| `discount_rate` | not run | — | Declined; held at 0.07 in every point. As above. |
| cycle block (the arms) | search | no | The block does move verdict structure: 22 grid points flip `recirc_ok` between the extreme arms and the feasible count rises 563 → 585. It does not move the wall-load fence or the LCOE ordering, and it moves the optimum by 1 m in R. Search framing stands, with the finding that the structure it moves is confined to the small-machine corner. |

## 6. Per-axis account

One pair of subsections per axis. Both ship present; the `**Applies:**` line
discharges the one the axis's framing does not owe. Every number is from `results/points.csv`; fence positions are at grid resolution (ΔR 0.5 m, Δa 0.05 m) and no claim is made about where a boundary sits between grid nodes.

#### `R` — feasible structure (search framing)
**Applies:** yes

Active constraint at small R: `recirc_ok`. For a = 0.80 m the largest violating R is 8.0 m (`arm-rankine-paper`), 6.5 m (`arm-rankine-upstream`), 5.5 m (both η 0.47 arms); the violated set shrinks with `a` and vanishes above a = 1.10 / 1.00 / 0.95 m respectively. `wall_load_ok` is independent of R (below). Constrained optimum: found, interior in R, on the wall-load fence — (14.0, 1.65) paper, (13.5, 1.65) upstream, (13.0, 1.65) both η 0.47 arms; the minimum is shallow (the four best points of each arm lie within 0.07 $/MWh). The optimum moves to smaller R as η rises.

#### `R` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `a` — feasible structure (search framing)
**Applies:** yes

Active constraint at large a: `wall_load_ok`, violated at every a ≥ 1.70 m for every R from 4.0 to 20.0 m, in every arm (wall load 4.165 MW/m² against the 4.05 limit; 4.035 at a = 1.65). The fence is a horizontal line because, with profiles held fixed, fusion power scales as R·a² and wall area as R·a, so the load depends on `a` alone. The objective falls monotonically toward the fence at every R in every arm (the unconstrained minimum is at a = 2.2), so a = 1.65 m is the optimal `a` in all four arms. At small a, `recirc_ok` is active (above).

#### `a` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `availability` — feasible structure (search framing)
**Applies:** not applicable — this axis was declined by the owner's ruling (§ 8) and not swept; it is held at 0.85 in every point

#### `availability` — observed response (sensitivity framing)
**Applies:** not applicable — declined and not swept; the only response on record is the oracle scan at baseline geometry in § 8 (LCOE only, no verdict moves), which is a scan, not a run

#### `discount_rate` — feasible structure (search framing)
**Applies:** not applicable — declined by the owner's ruling (§ 8) and not swept; held at 0.07 in every point

#### `discount_rate` — observed response (sensitivity framing)
**Applies:** not applicable — declined and not swept; the oracle scan in § 8 is the only response on record

#### cycle block (the arms) — feasible structure (search framing)
**Applies:** yes

What the block moves: the `recirc_ok` fence and only that fence. Feasible points 563 / 578 / 585 / 585 of 948 (paper, upstream, sco2-eta-only, sco2); the 22 points feasible in `arm-sco2` but not in `arm-rankine-paper` all lie in R 4.0–8.0, a 0.80–1.10. The two η 0.47 arms have identical verdicts at every point: the turbine and heat-rejection rates reach no constraint operand. What the block does not move: `wall_load_ok` (353 violations at the same points in every arm), the three inert verdicts, `net_positive` (never violated), and the LCOE ordering of the arms (fixed at all 948 points). Constrained optimum per arm: on the wall-load fence in every arm, R 14.0 → 13.5 → 13.0 m as η rises 0.333 → 0.40 → 0.47; the rates do not move it.

Two results from the data that bear on the owner's third bullet ("a non-intuitive result on the interactions"), stated as facts of the run:

- Total capital rises with η at every point (paper, then upstream, then sco2-eta-only, in increasing order at 948/948 points), because CAS23 turbine cost is priced per MW electric and a higher η means more MWe from the same thermal power. LCOE still falls, because MWh rises faster. `arm-sco2` has higher total capital than `arm-rankine-upstream` at every point despite its cheaper rates.
- The η gain is largest where recirculation is heaviest: −43 % at (4.0, 0.8), −20 % at (6.0, 1.0), −14 % at baseline geometry, −13.5 % at (20.0, 1.5). The sCO2 rate advantage is worth at most 1.1 % of LCOE anywhere in the window, so in this model the case for sCO2 is the efficiency, not the equipment price.

No interaction with magnet cost, wall load, β, or peak field was possible (§ 17). Nothing reverses the ordering of the arms.

#### cycle block (the arms) — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

## 7. Axis groups

Every declared qualified entry key, with its per-key provenance.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `R` | `stellarator_09__stellaris__R` | fan_out | plasma major radius, one plant-level entry point since the model migration |
| `R` | `stellarator_09__stellaris__magnet__R0` | tie | the magnet-cost Ampere's-law current runs on the same major radius under a separately authored attribute; declared in `manifest.json` `ties` (Item 3, 2026-08-19) and carried in ANNEX § Declared ties |
| `a` | `stellarator_09__stellaris__a` | fan_out | plasma minor radius |
| `availability` | `stellarator_09__stellaris__availability` | fan_out | capacity factor; one entry point (consuming calcs bind it by the `_in` convention) |
| `discount_rate` | `stellarator_09__stellaris__discount_rate` | fan_out | discount / interest rate; reaches CAS71, CAS72, CAS80 levelization and IDC |
| cycle block (held per arm) | `stellarator_09__stellaris__eta_th` | fan_out | thermal-to-electric efficiency |
| cycle block (held per arm) | `stellarator_09__stellaris__turbine__cost_per_mw` | fan_out | CAS23 turbine rate |
| cycle block (held per arm) | `stellarator_09__stellaris__heat_rejection__cost_per_mw` | fan_out | CAS26 heat-rejection rate; the two suffix siblings the scan found (`electric_plant__cost_per_mw`, `misc_plant__cost_per_mw`) are CAS24/CAS25, cycle-independent upstream (DI-007), and deliberately not in the block |

## 8. Indicators and rulings

Per proposed axis, including axes proposed and declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `R` | constraints_reachable (`net_positive`, `recirc_ok`, `wall_load_ok`; 7/8 objectives) | — | swept, search-framed |
| `a` | constraints_reachable (same three; 7/8 objectives) | — | swept, search-framed |
| `availability` | `no_constraint_response` (0/6; objectives `cas72`, `fuel`, `lcoe`, `lcoe_1cfe`) | **[OWNER-VERBATIM 2026-08-22]** "no sensitivity" | **declined** on the owner's ruling: not swept; held at 0.85 in every proposal. Oracle scan (`results/oracle_scan.json`): LCOE 455 → 248 $/MWh over 0.50–0.95 with no verdict change in any arm. |
| `discount_rate` | `no_constraint_response` (0/6; objectives `cas72`, `lcoe`, `lcoe_1cfe`) | **[OWNER-VERBATIM 2026-08-22]** "no sensitivity" | **declined** on the owner's ruling: not swept; held at 0.07 in every proposal. Oracle scan: LCOE 163 → 485 $/MWh over 0.03–0.12 with no verdict change. |
| cycle block (the arms) | constraints_reachable (`net_positive`, `recirc_ok`; `cas72`, `lcoe`, `lcoe_1cfe`, `total_capital`) | — | not a numeric sweep; four arm levels (owner added the fourth, 2026-08-22). Two suffix siblings (`electric_plant__cost_per_mw`, `misc_plant__cost_per_mw`) are CAS24/CAS25, cycle-independent upstream (DI-007), excluded. |

**Not derivable, disclosed in every record.** These are not decidable from the
indicator run and no indicator output claims them: monotonicity of any channel in any
axis; identity of the same physical quantity across differing key names; intra-module
operand dependency. `constraints_reachable` is a *possible* path and never a statement
that a constraint responds. `unresisted` is the agent's recorded judgment, never a
tool output.

**Model-development findings.** Every `no_constraint_response` axis carries one, in
addition to the user's ruling. The ruling does not discharge it.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `availability` | Nothing ties the achievable capacity factor to what sets it. CAS72 prices the fluence-limited core replacements but no coupling makes availability a *consequence* of the core lifetime and the outage time each replacement implies, or of any maintenance model; the model accepts any capacity factor at any wall load. The constraint that should push back is an availability ceiling derived from core lifetime and replacement duration. | `20260821-power-cycle-ab#1` |
| `discount_rate` | The cost of capital is a free multiplier. Nothing couples it to construction duration, to the capital mix, or to a financing structure; no bound or trade-off resists it. Whether anything *should* push back inside a techno-economic model is itself a modeling question (a finance-risk coupling would be a new input class); the gap is stated, not its fix. | `20260821-power-cycle-ab#2` |

## 9. Preflight results

Every mechanical gate that ran, with its outcome. The identity and baseline gates
read the documents the route-preparation step deposited in `results/`; name those
files in the detail column so a cold reader can open what the gate read. A gate that did not run is stated as
such with its condition.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 8 declared keys across 5 groups, all package inputs (`results/preflight_results.json`) |
| Suffix-sibling scan (warnings only) | warnings: 2 | `cycle_block`: `stellarator_09__stellaris__electric_plant__cost_per_mw`, `…misc_plant__cost_per_mw` — CAS24/CAS25 rates, cycle-independent (DI-007), excluded on purpose |
| Identity | pass | kind sealed, digest `7447efea9f20…` recomputed from 0 allowed-modified files; every sealed artifact matches (`results/package_identity.json`) |
| Baseline gate against the pinned headline | pass | `lcoe_calc__lcoe` expected 275.2642200420774, observed at relative deviation 0.000e+00; 6/6 pinned verdicts match (`results/baseline_result.json`) |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk (`manifest_currency`) |
| Package cleanliness | pass | package tree byte-untouched (git clean) before execution; re-checked after (§ 13) |

## 10. Execution route and why

- **Route:** study-local direct-API (`study.py` in this directory, over `studies/study_route.py`'s `run_points`: stock `ProvisionalPackageLoader(strict=True)` → `PreparedEvaluator` → `StudyDefinition` with `PreparedListStrategy` → `StudyRunner` → `StudyStore`)
- **Why this route:** three arms that each hold a three-key block constant while four axes sweep is a coordinated proposal list, not a Cartesian product; stock teax `744745f`'s CLI builds only a `GridStrategy` (`simkit/study/config.py:126`), which would cross-multiply the block keys. The route loaded and gated at steps 5–6 before this was written.

The rationale is recorded after the route was first exercised and gated, so it accounts
for a route already known to load rather than predicting one.

**Glue disclosure.** What the harness supplies that the model does not, and what that
means for the claims. The ledger's entries are values and live in `snapshot.json`
under `glue_ledger`; this is the argument about them.

glue ledger: none. No adapter on this route, so nothing is harness-supplied. Every value in every proposal is either a swept axis, the declared tie, or an arm's block; every other input is the sealed package's own.

## 11. Study definition and window provenance

The candidate windows were scanned with the package-owned oracle (`oracle_entry.evaluate`, `results/oracle_scan.json`) at the corners and the baseline of each arm before any package point ran. What the scan showed and what it fixed:

- **(R, a):** the proof-of-life window (R 4–20 m, a 0.8–2.2 m, validity mask R > a + 2.25 m) contains both fences in every arm: the small-machine corner fails `recirc_ok` (rec_frac 0.94 / 0.79 / 0.68 by arm) and the fat-plasma corner fails `wall_load_ok` (5.46 MW/m², cycle-independent). Reused unchanged so the arms join the proof-of-life record by coordinate.
- **availability 0.50–0.95** and **discount_rate 0.03–0.12:** scanned (LCOE only; no verdict moves in any arm) before the owner declined both axes (§ 8). Neither was swept; `arms[].window` carries them as held values (0.85, 0.07).

The geometry window is **engineered**: it is the proof-of-life's choice, kept so the arms join that record by coordinate, with the sourced validity mask. What that costs: no claim that the swept range is the physically or commercially attainable range; a result at a window edge is a result about the window, not about the plant. In this study no optimum sits on a window edge (R 13–14 m of 4–20; a 1.65 of 0.80–2.20, set by a constraint, not the window), but the `recirc_ok` fence at a = 0.8 reaches R = 8.0 m in the paper arm, well inside the window's lower edge of 4.0 m only because the window was chosen to contain it. The arm blocks are sourced values (§ 2, `study.py` docstring), not windows.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. All four arms ran in one store under the one sealed executable fingerprint `7447efea9f20…` and the one semantic fingerprint `1ca93d0c988c…` (`snapshot.json` `stores[0].compatibility_tuple`); the arms differ only in three input values, so every constraint is the same definition with the same `predicate_ir` in every arm, and no boundary was crossed.

## 13. Verification

**Outcome: pass.** `verify.py` sampled 12 completed cases of 3792 from the one store, stratified by verdict combination: 3 strata observed (the three combinations § 4 names), one case from each, then a seeded random fill. Every compared channel agreed with the independent oracle at relative deviation below 1e-9; the worst deviation was 4.00e-16 (`lcoe_1cfe_calc__lcoe` on `20260821-power-cycle-ab:c2127`). All six constraint verdicts were re-derived from the predicate IR through the package's published operand bindings and matched the store at every sampled case (`results/verification_summary.json` `constraints_rederived`, `verdict_mismatches: []`). The package tree was git-clean after the run (`results/postrun_clean.json`) and verify's own cleanliness check passed. What this licenses: the generated package computes the model's equations as the hand-written oracle does, at the sampled points, for the 10 compared channels (`beta_calc__beta`, `cas72_calc__cost`, `fuel_calc__annual_fuel`, `lcoe_1cfe_calc__lcoe`, `lcoe_calc__lcoe`, `magnet_cost__capital_cost`, `peak_field_calc__B_peak`, `special_materials_capital__special_materials_capital`, `total_capital__total_capital`, `wall_load_calc__wall_load`) and for the six verdicts.

**Sampling is arm-blind**, as inherited from the proof-of-life (`verify.py` `stratified_sample`; the design reads this as sufficient because the obligation is coverage of every verdict combination, which it gives). By case position the sample fell 3 / 1 / 6 / 2 on `arm-rankine-paper` / `arm-rankine-upstream` / `arm-sco2` / `arm-sco2-eta-only`, so every arm was sampled at least once, and every verdict combination occurs in every arm, so no stratum is arm-specific. The sample did not, by design, check each combination in each arm.

**Not covered.** (1) `fusion__p_fus` is not in the manifest's objective catalog and is not a predicate operand, so it is not compared — a known coverage delta carried from the Item 4 audit (`ANNEX.md § Oracle`); `magnet_capital` joined the catalog for this study and is compared. (2) The two power-balance operands, `net_electric` (`pb__p_net`) and `rec_frac`, are not recorded in the store, so their verdicts are re-derived from the oracle's own values of those operands and compared to the store's verdicts — the verdict is verified, the operand value is not recorded on the package side. (3) Values fed identically to both sides are not independently verified: the swept `R`, `a`, the tie `magnet__R0`, and each arm's three block values (by construction), and the package inputs both sides read, `p_pump` (1.0), `eta_p` (0.5), the held `availability` and `discount_rate`. Oracle parity verifies the package's arithmetic given those values, not the values. (4) The CAS23 and CAS26 component costs (`turbine_cost__cost`, `heat_rejection_cost__cost`) are compared only through `total_capital`, not as named channels. (5) The glue ledger is empty, so the `not_independently_verified` block of the summary is empty for that reason, not because everything is verified.

## 14. Review outcomes

Each named lens, its verdict, and its disposition. The pre-execution framing critique
is one of them.

| Lens | Verdict | Disposition |
|---|---|---|
| Pre-execution framing critique (fresh `general-purpose` subagent, 2026-08-21, read § 1–2, `axes.json`, `indicators.json`, policy §§ 2/5/7/9, runbook step 4) | PROCEED WITH CHANGES. Framings honest; axes legal under policy §§ 2/5. Required: rulings + findings for the two `no_constraint_response` axes; a framing row for the cycle block; the objective channel and baseline geometry named; the aspect mask sourced; per-arm window scan; three verdicts (`beta_ok`, `peak_field_ok`, `tbr_ok`) inert over the whole study and must be declared so. Recommended: a fourth arm (sCO2 η with Rankine rates) to split efficiency from cost rates; econ sweeps at more than one geometry. Structural limits named: the cycle reaches none of the wall-load, beta, peak-field fences nor magnet cost, so no interaction with those can appear. | Rulings taken and recorded (§ 8); cycle-block row added (§ 5); objective channel `lcoe_calc__lcoe`, baseline geometry (R 12.7, a 1.3), and the inert verdicts stated (§ 3, § 4, § 17); the mask is sourced — a derived geometric bound from the held-fixed radial-build stack, `ANNEX.md § Validity masks`, cited in § 11; the window scan was run in all three arms before the critique (`results/oracle_scan.json`). Fourth arm **added** (`arm-sco2-eta-only`, owner 2026-08-22). Multi-geometry econ sweeps: not taken — the owner declined the econ axes and clarified (2026-08-22) that what they want is the *A/B* at different geometries, which the per-arm (R, a) grid already gives at every point of the window. |
| Correctness (executor, post-run, 2026-08-22) | Every number in §§ 3–6 was recomputed from `results/points.csv` by a throwaway script and the per-arm feasible counts, fence positions, optima, and the cross-arm identity of the four cycle-independent verdicts and channels (`wall_load`, `p_fus`, `magnet_capital`, `beta` identical at every point across arms) checked there. `verify.py` pass; post-run clean pass. One defect found: the export declared five power-balance channels the store does not record (`p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et`); their columns are empty. | The empty columns are kept as exported (the CSV is evidence, and the export script is committed beside it) and disclosed in § 17; filed as finding `#5`. No number in the record depends on them — the recirculation account uses the `recirc_ok` verdict column, and the corner `rec_frac` values quoted come from the oracle scan, labelled as such. |
| Honesty (executor, 2026-08-22) | Checked that every claim in §§ 3–6 is a fact of the run, not a boundary claim beyond grid resolution; that the two "non-intuitive" results are stated as mechanisms the model contains (turbine cost per MWe; recirculation share), not as physics claims about real plants; that the declined axes carry no account; that the three inert verdicts and the impossible interactions are stated (§ 4, § 17); that the window is engineered and says what that costs (§ 11). | No change; § 17 lists the gaps. |
| Readability (executor, 2026-08-22) | Self-applied against the working-voice rule: lead with the point, numbers with their file, plain terms. The external readability check is the fresh administrator's synthesis, which is written after this record is committed and cannot be cited here. | Its "does not support" entries are classified in the Item 6 plan's Phase 2 notes, not in this record (immutable once committed; an addendum would carry any correction). |

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md` as `20260821-power-cycle-ab#n`.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260821-power-cycle-ab#1` | model | Nothing couples the capacity factor to what sets it (core lifetime, replacement outage, maintenance); the model accepts any availability at any wall load (§ 8, `no_constraint_response`). | Owner ruled "no sensitivity"; axis declined. The gap stands: an availability ceiling derived from core lifetime and replacement duration is the constraint that should push back. | unrouted — candidate modeling item under the MFE Cost Modeling epic (`work/backlog/epic-mfe-cost-modeling.md`) |
| `20260821-power-cycle-ab#2` | model | The discount rate is a free multiplier: nothing couples it to construction duration, capital mix, or financing structure (§ 8, `no_constraint_response`). | Owner ruled "no sensitivity"; axis declined. Whether anything *should* push back inside a techno-economic model is itself a modeling question; the gap is stated, not its fix. | unrouted — stated for the modeling PM; no item minted |
| `20260821-power-cycle-ab#3` | model | `p_pump` = 1.0 MW (held, cycle-independent in every arm) is roughly 100× below helium-primary circulator figures (2–6 % of blanket thermal power), per DI-008. It suppresses the recirculating fraction in every arm equally, so it does not bias the A/B, but it understates `rec_frac` everywhere. | Not changed in this study (DI-007: not part of the cycle choice). Re-sourcing is a separate modeling item. | research round WI-031 follow-up R4 (`knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md`); modeling item not yet minted |
| `20260821-power-cycle-ab#4` | process | The oracle seam's key map grows per study: `oracle_entry.ENTRY_KEY_TO_ORACLE_INPUT` needed four new entries (`eta_th`, the two rates, `discount_rate`) before the scan or `verify.py` could run, and the annex sentence "four keys today" was already stale (eighteen after WI-030 and this study). Any study that moves a new entry key edits the seam first; `verify.py` fails closed on an undeclared key, which is the right behaviour, but the cost lands on the study. | Seam edited and committed with the scaffold (`ffa5c54c`); the annex's stale count corrected in this commit. The oracle leaves the study contract after Item 6 (policy § 10), which retires the seam with it. | documented seam — `exploration/stellarator_e2e/studies/ANNEX.md § Oracle` |
| `20260821-power-cycle-ab#5` | process | The quantities the two cycle-sensitive constraints read — `pb__p_net` (`net_positive`) and `pb__rec_frac` (`recirc_ok`) — are fields of one multi-field power-balance model and are not recorded in the store (the evidence layer records single-field float channels only; `ANNEX.md § Oracle` says so). A study can report the verdict but not the operand's value on the package side; this record's export declared those channels and shipped empty columns. | Columns left as exported and disclosed (§ 13, § 17); the verdicts are verified by re-deriving from the oracle's operand values. The gap is in the package's evidence projection, not in this study. | unrouted — a sysml-codegen / teax evidence-layer question (record per-field outputs of multi-field models), outside this repository's tools |
| `20260821-power-cycle-ab#6` | process | `record-template.md` contains the marker `**END OF RECORD**` twice (once in the preamble explaining it, once as the marker), so slicing the template at the first occurrence yields nothing. Cost the executor three attempts when opening this record. | Worked around (slice at the occurrence after `## 1.`); the template is not edited in this item (design I1). | skill — `.claude/skills/run-study/record-template.md` |

**Homes a finding may route to:** tool, runbook step, policy rule, skill, modeling
item, research round, documented seam. `unrouted` is a stated state, not a blank.

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `3df983550962be1963b460ea4f64a7b24969dad4bfdfd5fd57166b7d0fc2d34c`
- **Schema version:** `1`

No snapshot content is restated here.

## 17. What this record does not contain

- **Power-balance values per point.** `p_net`, `rec_frac`, `q_eng`, `p_th`, `p_et` are declared in `study.py` and exported, but the store does not record them (finding `#5`), so those five columns of `results/points.csv` are empty at every row. The only per-point record of net power and recirculating fraction is the `net_positive` and `recirc_ok` verdict columns. The corner and baseline values quoted in § 4 and § 11 are from the oracle scan (`results/oracle_scan.json`), not from the package.
- **Any run on the economic axes.** `availability` and `discount_rate` were declined; nothing in `results/` moves them. The § 8 oracle-scan numbers are the only response on record and are three-arm (the scan predates the fourth arm).
- **Which cycle the Stellaris paper assumes.** It names none ("a simple electrical conversion efficiency of 1/3"); "Rankine" in `arm-rankine-paper` is this study's label because the model's cost rates are the upstream Rankine preset.
- **Any interaction between the cycle and magnet cost, wall load, β, peak field, or TBR.** The cycle block reaches none of their operands (`indicators.json`), and the run confirms the four are identical across arms at every point. The study could not have found one.
- **Any cycle × geometry reversal.** The LCOE ordering of the arms is the same at every grid point; no geometry favours a lower-η arm.
- **Boundary positions finer than the grid.** Fences are located at ΔR 0.5 m, Δa 0.05 m; the wall-load fence lies between a = 1.65 and 1.70 at every R, the `recirc_ok` fence between the listed R values.
- **A sourced `p_pump`.** Held at 1.0 MW in every arm (finding `#3`); the A/B is unbiased by it but every `rec_frac` is understated.
- **The store.** `_work/20260821-power-cycle-ab.db` is gitignored; its compatibility tuple is in `snapshot.json` `stores[]` and the verification summary digests it. The 3,792 cases are in `results/points.csv`.
- **The 1costingFE handshake.** Outside the study contract (policy § 10); not run.
- **Per-arm stratified verification.** The sample is arm-blind (§ 13); no claim that each verdict combination was checked in each arm.
- **Wall-clock.** 3,792 points ran in 9 min 2 s on the stock route (0.14 s/point); recorded here only, not in a result artifact.
- **Plots.** None; the CSV is the result.

## Addendum 2026-08-22

Written by the executor after the administrator's `synthesis.md` (committed `e41150e8`), which was read against this record. Nothing above this line, and nothing in `snapshot.json`, `indicators.json`, or `results/`, is changed. Three statements above are corrected and three findings are added.

**Corrections of statements (numbers recomputed from `results/points.csv`):**

- § 3: "within 0.1 $/MWh over R 13–15 m" along the a = 1.65 fence overstates the flatness. The LCOE at R 13.0–15.0 on that fence lies within 0.26 $/MWh of the arm's feasible minimum (0.15 / 0.17 / 0.24 / 0.26 $/MWh for paper / upstream / sco2-eta-only / sco2). The optimum is shallow; the number was too tight.
- § 6 (`R`): "the four best points of each arm lie within 0.07 $/MWh" — the spread is 0.055 / 0.076 / 0.062 / 0.068 $/MWh; read "within 0.08".
- § 6 (cycle block): "the sCO2 rate advantage is worth at most 1.1 % of LCOE anywhere in the window" holds over the points feasible in both arms (−0.5 % to −1.1 %, § 3). Over the whole window, including `wall_load_ok`-violated points, it reaches 1.33 % (at R 5.5, a 2.2). The conclusion — the efficiency, not the rates, carries the sCO2 case — stands.
- § 10 "three arms that each hold a three-key block constant while four axes sweep" is stale text from before the fourth arm and the two declines: four arms, two swept axes. The same stale sentence is in the docstring of `study.py` (lines 3–4 and 33 as committed); `study.py` is digested into `snapshot.json` `arms[].artifacts` and is therefore not edited. The code ran four arms over (R, a) only, as `results/points.csv` shows.

**Findings added (rows appended to `DISCOVERY_LOG.md`):**

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260821-power-cycle-ab#7` | process | The record carries every verdict but not, as data, the bound values the verdicts were judged against (`wall_load_limit` 4.05, `recirc_ok__threshold` 0.5, `tbr` 1.074 / `tbr_floor` 1.05, `beta_limit` 0.05, `magnet__B_max` 24.9): they appear only as prose in § 4. `indicators.json` names the bound keys (`bounds[].operands[].ref`) and carries a `value` only for literal operands, not for bound design attributes; no `results/` artifact carries them either. A reader cannot check a fence against its limit from the directory alone (synthesis § 6 entry 5, *(contract)*). | Stated here; no artifact added (results are frozen). The contract should require the bound values as snapshot data, or the indicator tool should emit them for bound operands as it does for literals. | skill — `.claude/skills/run-study/record-template.md` (contract); alternatively tool `scripts/study/indicators.py`; not edited in Item 6 (design I1) |
| `20260821-power-cycle-ab#8` | process | `results/verification_summary.json` `teax.revision` is the string `"unrecorded"`: `verify.py` reads `simkit.__version__`, which stock teax does not define, so the verification artifact does not say which teax it ran under. The snapshot's `teax.revision` (`744745f`, from `git rev-parse` in the teax checkout) has no verification-side artifact behind it (synthesis § 5, § 6 entry 10). | Disclosed; the snapshot value stands on the executor's resolution. The tool should record the checkout's git revision (the module path it already records resolves to it). | tool — `scripts/study/verify.py`; not edited in Item 6 (design I1) |
| `20260821-power-cycle-ab#9` | process | Stale pre-execution text survived into the committed record and its definition file (§ 10 "three arms … four axes"; `study.py` docstring), because the arm count and the axis set changed after those sentences were written and the step-15 placeholder check catches only unreplaced placeholder tokens, not stale prose. | Corrected above for the record; `study.py` left as digested. A pre-commit read of § 1 against § 10 and the definition's docstring would have caught it. | runbook step 15 (a stale-prose check beside the placeholder check); not edited in Item 6 (design I1) |

**Classification of the synthesis's "What the record does not support" entries**, for the Item 6 plan: entries 5 and 10 are contract gaps (findings #7, #8); every other entry is either a gap this record states itself in § 17 (1, 2, 3, 4, 6, 7, 8, 9, 15, 16, 17) or a fact the record contract places outside the directory by design (11 the store, 12 the commit state, 13 the rulings as events, 14 the critique text). No entry is a reader miss: nothing the administrator reported missing is in the directory.
