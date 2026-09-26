## 1. Study header

- **Study id:** `20260926-aries-design-choice-interactions`
- **Package:** `aries_integrated`
- **Date executed:** 2026-09-26
- **Executor:** goal `design-space-combinations` round agent (T-003), Claude Code session
- **Mode:** execute
- **Arms:** single arm (one store; the three factorials B1, B2, B3 are declared design blocks on two sealed bases, not arms)

## 2. Intake

The owner's brief, part B, verbatim (`work/orchestration/goals/design-space-combinations/evidence/owner-brief.md`):

> B. Test interactions between design choices
> 
>   Choose a few questions where considering one parameter at a time could give the wrong answer. For example:
> 
>   - Does the preferred recuperator effectiveness depend on the blanket’s heat-source temperatures? Recovering more exhaust heat may improve cycle efficiency
>     while making it harder to accept lower-temperature reactor heat.
> 
>   - Does increasing coolant flow help enough to justify its equipment and power demands? More heat removal need not mean more net electricity or lower LCOE.
>   - Does a change in plasma profile alter which equipment becomes limiting? The same downstream equipment should reveal how a core choice changes fuel-
>     processing and cooling requirements.
> 
>   Run paired or small factorial studies: vary the choices together, explain any ranking reversals, and check whether the explanation survives reasonable
>   assumption changes. A finding need not be surprising to a specialist; it needs to reveal something the individual component calculations would conceal.
> 
>   The stopping condition should be concrete: demonstrate several previously untested, compatible combinations without new physics definitions; characterize
>   the failed combinations; and explain at least one tested interaction—or report that none was established.

[AGENT] Executor additions: the study runs on the unchanged WI-092 package identity (executable `f739dbce…`, semantic `78dd23bf…`, live manifest pin `06e0627c…`). Canonical bases are the verbatim stored input maps of two sealed cases: `nominal-calculated` (423 MW, series exchangers, 1,400 kg/s, recuperation 0.8, calculated plasma 1,835 MW; `20260925-aries-revised-reference-network`) and `resized-compressor-1700-network-scaledflows-0.85` (891 MW, published network, 1,700 kg/s, recuperation 0.95, supplied 2,436 MW; `20260925-aries-flow-scaling-check`), both replayed bit-exactly on this identity by the prior goal and by this goal's T-002 control. Every other case composes declared changes on a named base (`config.json` → `proposed-points.json`; six aliases name grid cells that coincide with a base or another cell and are not re-run). B1: recuperation {0.5, 0.8, 0.95} × source temperature level (the three branch hot limits shifted −60 / 0 / +60 K together, a declared scenario at unchanged duty) on both bases, plus the four N corners at turbine efficiency 0.90. B2: helium primary flow {2,600, 3,261, 3,900} × pump law {cubic proxy, fixed} × recuperation {0.8, 0.95} on N with the pump capacity held at 3,261; and flow {3,359, 4,000, 4,700} × pump law on A at recuperation 0.95 and level −60 K, where the helium stage binds, with the capacity held at 3,359. B3: density amplitude {4.75, 5.0, 5.5, 5.75} × 10²⁰ × hollowness {0.66, 0.60} × exchanger arrangement {series, network} on N with every rating unchanged. The B3 and B2-A windows were fixed after the r1 oracle scan (§ 11). Nothing is optimized; no rating is changed from demand; the reading reports main effects, the difference-of-differences interaction, ranking reversals and the limiting check per case.

## 3. Objective and result

- **LCOE objective channel(s):** `aries_integrated_plant__lifecycle_price__evaluate__lcoe` (the manifest headline; equal to `aries_integrated_plant__lifecycle_accounts__evaluate__lcoe_sum`), no-breeding-credit convention on every point.
- **LCOE result:** 685.695 USD2004/MWh at `A-control` to 2961.187 at `b3-N-amp4.75e20-hol0.60-net0`; the two controls reproduce their sealed values (N 1119.408, A 685.695).

The LCOE is read, not optimized: on this package it is dominated by purchased tritium (prior goal L-001), so the study's readings are on net electricity, unmet heat and the check verdicts, with the LCOE reported as the consequence. Over the 52 points the LCOE moves with net electricity (denominator) and with fusion power (tritium purchases); no case is tuned.

## 4. Constraint outcomes

Every executing constraint by qualified identity; statuses aggregated over the 52 stored points (per-point verdicts in `results/cases.json` and `cases.csv`).

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `aries_integrated_plant__compressor_capacity__capacity_ok__a45f9cf05e8aa7ab` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__divertor_capacity__capacity_ok__be7081920ad8e8ed` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__divertor_pump__capacity_ok__d6730c7060447f4c` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__fuel_capacity__capacity_ok__8eb5888bfe62cd64` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__fuel_inventory__capacity_ok__37f4667fbfb616d0` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__generator_capacity__capacity_ok__60b43f15d48ff161` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__he_capacity__capacity_ok__db2733d1d5baf3cf` | `capacity_ok` | violated at 1 of 52 | b2-A-flow4700-pump0-rec0.95-lvl-60 |
| `aries_integrated_plant__he_pump__capacity_ok__fcee5ee009fe5180` | `capacity_ok` | violated at 8 of 52 | b2-A-flow4000-pump0-rec0.95-lvl-60; b2-A-flow4000-pump1-rec0.95-lvl-60; b2-A-flow4700-pump0-rec0.95-lvl-60; b2-A-flow4700-pump1-rec0.95-lvl-60; b2-N-flow3900-pump0-rec0.8; b2-N-flow3900-pump0-rec0.95; b2-N-flow3900-pump1-rec0.8; b2-N-flow3900-pump1-rec0.95 |
| `aries_integrated_plant__pbli_capacity__capacity_ok__55a012a287da9395` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__pbli_pump__capacity_ok__79d116aa320dd4fb` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__plant_ledger__balances_ok__9af2e85b5e4e5535` | `balances_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__plant_ledger__heat_removal_ok__695378663bcd8d07` | `heat_removal_ok` | violated at 11 of 52 | b1-A-rec0.95-lvl-60; b1-N-rec0.95-lvl-60-eta0.90; b2-A-flow3359-pump0-rec0.95-lvl-60; b2-A-flow4000-pump0-rec0.95-lvl-60; b2-A-flow4000-pump1-rec0.95-lvl-60; b2-A-flow4700-pump0-rec0.95-lvl-60; b2-A-flow4700-pump1-rec0.95-lvl-60; b3-N-amp5.50e20-hol0.66-net1; b3-N-amp5.75e20-hol0.60-net1; b3-N-amp5.75e20-hol0.66-net0; b3-N-amp5.75e20-hol0.66-net1 |
| `aries_integrated_plant__rejection_capacity__capacity_ok__295420bc9fb25608` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |
| `aries_integrated_plant__turbine_capacity__capacity_ok__089f9e8e61919ec1` | `capacity_ok` | satisfied at all 52 | never violated in the swept space |

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `recuperation` | sensitivity | operating role; A3 nominal 0.8 (WI-089); no boundary is sought, the factorial response is |
| `he_limit` | sensitivity | source role; Source-supported blanket-helium outlet 729.15 K (reference-case contract § 2), shifted −60/0/+60 K with the other two limits as one temperature-level scenario at unchanged duty.; no boundary is sought, the factorial response is |
| `divertor_limit` | sensitivity | source role; Source-supported divertor-helium outlet 973.15 K, shifted with the level scenario.; no boundary is sought, the factorial response is |
| `pbli_limit` | sensitivity | source role; Source-supported PbLi outlet 1011.15 K, shifted with the level scenario.; no boundary is sought, the factorial response is |
| `he_flow` | sensitivity | operating role; Raffray blanket-helium flow 3261 kg/s; no boundary is sought, the factorial response is |
| `he_pump_mode` | sensitivity | assumed role; E3 (WI-090): mode 0 cubic proxy from 156 MW at 3261 kg/s; no boundary is sought, the factorial response is |
| `density_amplitude` | sensitivity | operating role; WI-083 reference amplitude 5.0e20; no boundary is sought, the factorial response is |
| `hollowness` | sensitivity | operating role; WI-081 reference hollowness 0.66; no boundary is sought, the factorial response is |
| `network_mode` | sensitivity | operating role; WI-092 N1: 0 series (reviewed), 1 published series-then-parallel with the supplied split 0.85.; no boundary is sought, the factorial response is |
| `turbine_efficiency` | sensitivity | assumed role; A3 0.93 (WI-089); no boundary is sought, the factorial response is |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `recuperation` | sensitivity | no | response observed on both bases; the binding at 0.95/−60 K on A is a located violation, not a boundary claim |
| `he_limit` | sensitivity | no | inert on N and on A below 0.95 (all heat removed); acts only through the bound helium stage |
| `divertor_limit` | sensitivity | no | inert at every point (the divertor stage never binds) |
| `pbli_limit` | sensitivity | no | inert at every point (the PbLi stage never binds) |
| `he_flow` | sensitivity | no | response sign depends on the pump law; violations located (pump screen at 3,900 and 4,000–4,700; helium rating at 4,700 cubic) |
| `he_pump_mode` | sensitivity | no | the law changes the sign of the flow response |
| `density_amplitude` | sensitivity | no | monotone rise of fusion power, net and tritium over the window; heat-removal violation located at 5.75e20 (series) and 5.5e20 (network) at hollowness 0.66 |
| `hollowness` | sensitivity | no | 0.60 lowers fusion power ≈ 11 % and moves the binding out of the window |
| `network_mode` | sensitivity | no | inert where all heat is removed; changes the binding point and the net ranking at the top of the density window |
| `turbine_efficiency` | sensitivity | no | 0.90 moves the N corner (0.95, −60 K) into a bound state (36 MW unmet) |

## 6. Per-axis account

#### `recuperation` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `recuperation` — observed response (sensitivity framing)
**Applies:** yes

On N (1,400 kg/s, series): net 269.631 / 423.107 / 557.114 MW at 0.5 / 0.8 / 0.95 at every level, all heat removed, no violation. On A (1,700 kg/s, network): 463.066 / 691.524 / 891.002 at levels 0 and +60 K; at −60 K the 0.95 point falls to 745.301 with 162.118 MW unmet (helium stage 152.431) and `heat_removal_ok` violated, the only violation of the B1 grid. Heater inlet rises with recuperation (A: 431.023 / 505.183 / 569.936 K) toward the lowered helium limit 669.15 K, which is the mechanism. The difference of differences on net, (0.95 − 0.5) at +60 K minus the same at −60 K, is -0.000 MW on N and 145.701 MW on A; the ranking 0.95 > 0.8 > 0.5 holds at every level on both bases. With turbine efficiency 0.90 the N corner (0.95, −60 K) binds too (36.102 MW unmet, net 515.682) and the N difference of differences becomes 32.308 MW. No boundary claim is made.

#### `he_limit` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `he_limit` — observed response (sensitivity framing)
**Applies:** yes

Acts only where the helium stage is capacity-limited: inert on N at every recuperation and on A at 0.5 and 0.8; at A/0.95 the −60 K shift binds the stage (see `recuperation`). The −60 K shift at N/0.95 binds only under the 0.90 turbine-efficiency assumption. Violations located: `b1-A-rec0.95-lvl-60`, `b1-N-rec0.95-lvl-60-eta0.90` (`heat_removal_ok`). No boundary claim is made.

#### `divertor_limit` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `divertor_limit` — observed response (sensitivity framing)
**Applies:** yes

Inert at every point: the divertor stage never binds within ±60 K on either base (its capability exceeds its 375 MW duty throughout). No boundary claim is made.

#### `pbli_limit` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `pbli_limit` — observed response (sensitivity framing)
**Applies:** yes

Inert at every point within ±60 K: the PbLi stage never binds on either base in this window (the prior goal's series-order PbLi limit appears at the source-conditioned inputs, not at these bases). No boundary claim is made.

#### `he_flow` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `he_flow` — observed response (sensitivity framing)
**Applies:** yes

On N nothing more is removed at any flow (all heat is already removed); under the cubic pump law net falls -26.888 then -38.742 MW per step at 0.8 (LCOE +66.888 then +112.831), under the fixed law nothing changes; at 3,900 kg/s the helium pump capacity screen (3,261) is violated under both laws. On A where the helium stage binds (0.95, −60 K): fixed law +1.411 then +0.849 MW net per step with unmet heat -1.570 then -0.945 MW (the stage is limited by the cycle-side inlet temperature, not by primary flow); cubic law -116.004 then -178.296 MW net with unmet heat +104.555 then +160.975 MW, because 90 % of the pump power is recovered as friction heat into the very stage that cannot remove it; at 4,700 kg/s cubic the helium duty rating (1,500 MW) is also violated (margin −17.057). Violations located: pump screen at N/3,900 (all four cells) and A/4,000–4,700 (all four); `heat_removal_ok` on every A cell; `he_capacity` at A/4,700 cubic. No boundary claim is made.

#### `he_pump_mode` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `he_pump_mode` — observed response (sensitivity framing)
**Applies:** yes

Changes the sign of the flow response: under the cubic proxy more flow costs net (N) or costs net and adds unmet heat (A); under the fixed law flow is free of power cost and the only response is the capacity screen. The two laws bracket a missing pump map. No boundary claim is made.

#### `density_amplitude` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `density_amplitude` — observed response (sensitivity framing)
**Applies:** yes

Fusion power 1,477–2,427 MW over 4.75–5.75e20 (with hollowness), net 132.275–820.519 MW, external tritium 84.331–138.242 kg/year; no violation up to 5.5e20 in series and 5.0e20 in network at hollowness 0.66; `heat_removal_ok` violated at 5.75e20 (series 149.872 MW unmet; network 114.954) and at 5.5e20 network (45.224) and 5.75e20/0.60 network (26.086). The fuel-processing rating (3e22 atoms/s) keeps a margin of at least 1.363e22 throughout; the compressor margin is constant (227.149, set by cycle flow); the helium duty rating margin falls 751.046 → 359.792 but stays positive. No boundary claim is made.

#### `hollowness` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `hollowness` — observed response (sensitivity framing)
**Applies:** yes

0.60 lowers fusion power by ≈ 10.8 % at 5.0e20 (1,835.451 → 1,636.463 MW) and net by 161 MW; it moves the helium-stage binding beyond the window in series and to 5.75e20 in the network. No boundary claim is made.

#### `network_mode` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `network_mode` — observed response (sensitivity framing)
**Applies:** yes

Inert where all heat is removed (identical channels at every unbound point, prior goal L-006). At 5.5e20/0.66 the network binds first (45.224 MW unmet, net 703.212 against series 735.759); at 5.75e20/0.66 the network removes more (114.954 against 149.872 unmet) and yields more net (820.519 against 795.389): the arrangement ranking reverses between the two amplitudes. No boundary claim is made.

#### `turbine_efficiency` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `turbine_efficiency` — observed response (sensitivity framing)
**Applies:** yes

0.90 at the four N corners: net −44.318 MW at 0.5 (both levels) and −9.124 / −41.432 at 0.95 (+60 / −60 K); the (0.95, −60 K) corner becomes bound (36.102 MW unmet) because the hotter exhaust raises the heater inlet. No boundary claim is made.

## 7. Axis groups

Declared in `axes.json` (record-local) and expanded from `config.json`; every group has one entry key (`fan_out`); no ties (the three hot limits are separate source-role groups shifted together by the design, a declared scenario, never a claimed physical identity).

| Axis | Entry key | Provenance | Units | Role |
|---|---|---|---|---|
| `recuperation` | `aries_integrated_plant__cycle__recuperator_effectiveness` | fan_out | 1 | operating |
| `he_limit` | `aries_integrated_plant__heat_exchangers__he_limit` | fan_out | K | source |
| `divertor_limit` | `aries_integrated_plant__heat_exchangers__divertor_limit` | fan_out | K | source |
| `pbli_limit` | `aries_integrated_plant__heat_exchangers__pbli_limit` | fan_out | K | source |
| `he_flow` | `aries_integrated_plant__heat_exchangers__he_flow` | fan_out | kg/s | operating |
| `he_pump_mode` | `aries_integrated_plant__he_pump__pump_mode` | fan_out | 1 | assumed |
| `density_amplitude` | `aries_cs_plasma_integration__plasma__amplitude` | fan_out | m^-3 | operating |
| `hollowness` | `aries_cs_plasma_integration__plasma__hollowness` | fan_out | 1 | operating |
| `network_mode` | `aries_integrated_plant__heat_exchangers__network_mode` | fan_out | 1 | operating |
| `turbine_efficiency` | `aries_integrated_plant__cycle__turbine_efficiency` | fan_out | 1 | assumed |

## 8. Indicators and rulings

All ten proposed axes were traced; none declined; none reports `no_constraint_response`, so no pre-execution ruling is owed. `indicators.json` is in the record directory (tool source digest inside it).

| Axis | Indicator | Ruling | Missing response (disclosed) |
|---|---|---|---|
| `density_amplitude` | constraints_reachable (11 of 14 constraints on a possible path: compressor_capacity, divertor_capacity, fuel_capacity, fuel_inventory, generator_capacity, he_capacity, pbli_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | Fixed-hardware source-demand change; no confinement or transport qualification. |
| `divertor_limit` | constraints_reachable (6 of 14 constraints on a possible path: compressor_capacity, generator_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | As he_limit. |
| `he_flow` | constraints_reachable (10 of 14 constraints on a possible path: compressor_capacity, divertor_capacity, generator_capacity, he_capacity, he_pump, pbli_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | No hydraulic or pressure-drop model; the cubic pump proxy and the pump capacity screen are the only responses. |
| `he_limit` | constraints_reachable (6 of 14 constraints on a possible path: compressor_capacity, generator_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | No blanket thermal-hydraulic model links the outlet temperature to duty and flow; coolant and material limits are not checked; the branch return temperature is computed. |
| `he_pump_mode` | constraints_reachable (10 of 14 constraints on a possible path: compressor_capacity, divertor_capacity, generator_capacity, he_capacity, he_pump, pbli_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | No pump map; the two laws bracket the pump-power response to flow. |
| `hollowness` | constraints_reachable (11 of 14 constraints on a possible path: compressor_capacity, divertor_capacity, fuel_capacity, fuel_inventory, generator_capacity, he_capacity, pbli_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | As density_amplitude. |
| `network_mode` | constraints_reachable (6 of 14 constraints on a possible path: compressor_capacity, generator_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | The split is a stand-in for the unmodelled branch hydraulic balance. |
| `pbli_limit` | constraints_reachable (6 of 14 constraints on a possible path: compressor_capacity, generator_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | As he_limit. |
| `recuperation` | constraints_reachable (6 of 14 constraints on a possible path: compressor_capacity, generator_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | The recuperator has no purchase, rating or screen (economics goal L-003); only the thermal closure and the downstream ratings respond. |
| `turbine_efficiency` | constraints_reachable (6 of 14 constraints on a possible path: compressor_capacity, generator_capacity, plant_ledger, rejection_capacity, turbine_capacity) | none owed (no `no_constraint_response` axis); the owner brief part B names these levers for paired studies | No turbine map. |

**Not derivable, disclosed.** Monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a possible path, never a statement that a constraint responds; `unresisted` is the executor's judgment, never a tool output.

**Model-development findings.** None is owed by a `no_constraint_response` ruling; the missing responses disclosed above are carried to § 15 where the run makes them material.

## 9. Preflight results

Overall: **pass** (`preparation/preflight_results.json`, run on the r2 preparation; the r1 gates under `preparation-r1/` also passed).

| Gate | Outcome | Detail |
|---|---|---|
| declared_keys | pass | 10 declared keys across 10 groups, all package inputs |
| sibling_scan | pass | warnings: 2 |
| identity | pass | kind sealed, digest f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4 recomputed from 0 allowed-modified file(s) and 0 declared source(s); every other sealed artifact matches |
| manifest_currency | pass | both recorded package fingerprints match the package on disk |
| baseline_headline | pass | aries_integrated_plant__lifecycle_price__evaluate__lcoe reproduces at relative deviation 0.000e+00; 2/2 pinned verdicts match |
| package_clean | pass | package tree is byte-untouched (git clean) |

## 10. Execution route and why

- **Route:** study-local direct-API (stock `StudyRunner` with `PreparedListStrategy` over complete declared input maps, through `interactions_support.py`, which reuses the reconciliation composer `reconciliation_support.proposals` and the retained predecessor executor `20260922-aries-integrated-lcoe/execute_study.py`).
- **Why this route:** the declared cases are named full maps composed on canonical bases (the verbatim stored inputs of two sealed cases, checked against this package's executable fingerprint); the strict loader, fingerprints, store lease and full-map exporter are reused unchanged; the live manifest and the round-2 integration CANDIDATE are reused without re-pin because the package identity is unchanged (as the three prior studies on this identity did).

**Glue disclosure.** glue ledger: none. No adapter on this route, so nothing is harness-supplied.

## 11. Study definition and window provenance

The candidate set was scanned with the package-owned independent oracle before execution, twice. The r1 scan (`preparation-r1/oracle-window-scan.json`, 43 points) refused 8 B3 points (`nonpositive net electricity: LCOE undefined` at density amplitude 4.0e20 for every hollowness and arrangement, and at hollowness 0.30 for every amplitude) and showed the source temperature level inert on the N base at every recuperation (net 269.631 / 423.107 / 557.114 at −60, 0 and +60 K alike) because every stage removes all its heat there. An oracle-only probe (`work/orchestration/goals/design-space-combinations/evidence/window-probe.txt`) then read the density window (amplitude 4.5–5.75e20 × hollowness 0.66–0.50 on N) and the binding case (A at recuperation 0.95 and level −60 K, flow 3,359–4,700 × pump law). The r2 windows are **engineered** from that probe: amplitude 4.75–5.75e20 with hollowness 0.66 and 0.60 (net positive at the low corner, 132 MW at 4.75e20/0.60, and the helium stage bound at the high corner, 150 MW unmet at 5.75e20/0.66); the added B2-A block where the helium stage already binds (162 MW unmet at 3,359 kg/s). The r2 scan (`oracle-window-scan.json`): 52 of 52 evaluated, 0 refused. Windows for recuperation, the three limits, flow, pump law, arrangement and turbine efficiency are engineered from the bases' sourced values (`axis-plan.json` basis fields). No validity mask is applied. Restated windows: none (this is the first study of these levers on this package). Tolerances: the live manifest's ten declared absolute classes (`manifest.json` `absolute_tolerances`, six MW/USD classes from the reconciliation goal and four kg/year classes from the economics goal) apply unchanged; no new class is declared for this study, and a verifier refusal outside them is surfaced to the goal as an owner gate, never absorbed.

## 12. Cross-fingerprint correlation and what it means

Single arm, single store, single package identity: executable `f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4`, semantic `78dd23bf4c4a2d431ce8223d973db08e955e6f378175623ced8b976db4231f93`, indicator-input fingerprint equal to the live manifest pin `06e0627c…` (preflight `manifest_currency` pass). No cross-arm correlation is needed: nil, single fingerprint. The two sealed bases carry the same executable fingerprint (checked by `interactions_support.canonical_inputs`).

## 13. Verification

**Outcome: pass.** `verify.py` sampled all 52 completed cases of the one store (`--sample-size 52`, stratified by verdict combination then filled), compared 364 scalar channels against the package-owned oracle at relative deviation below 1e-9 or the manifest's ten declared absolute classes, and re-derived all 14 verdicts from the oracle's own operands with no mismatch (`results/verification_summary.json`). Worst case named by the summary: `plant_ledger__evaluate__residual_magnitude` at `20260926-aries-design-choice-interactions:c0025`, 5.737e-09 MW, inside its 1e-7 MW class. The package tree was git-clean after execution and after verification.

**Not covered.** Values fed identically to both sides (every swept and held input) are not independently verified; the oracle checks the implementation of the model's assumptions, not their scientific qualification; the glue ledger is empty so nothing is harness-supplied; per-point operand values of multi-field outputs are recorded as channels here (this package exports single-field channels), so the B2 pump-electric and B1 heater-inlet readings are stored channels, not oracle-derived columns.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Compatibility map and choice inventory the axes rest on (fresh reviewer, goal T-001) | FINDINGS, no misclassified row; line cites and one mechanism cite corrected | `work/orchestration/goals/design-space-combinations/evidence/map-review.md` |
| Control replay of the N base on this identity (coordinator, goal T-002) | bit-identical to the sealed `nominal-calculated` (net 423.107, 14 of 14 satisfied) | `…/evidence/scratch-screens.json` |
| Pre-execution checkpoint (coordinator, goal C-001.r1) | PASS as a coordinator check; no review trigger met; reused coverage cited; window revision recorded | goal trail |
| All-point verification against the oracle (executor) | pass, 52 of 52, 364 channels, 14 verdicts | § 13 |
| Round-1 review of this reading | pending at the round result | goal trail |

## 15. Findings

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260926-aries-design-choice-interactions#1` | model | The heat-source temperature level (all three branch outlet limits shifted ±60 K at unchanged duty and flow) has no effect on any plant-ledger channel where every stage removes all its heat: identical channels at every N point and at every A point below recuperation 0.95. It acts only through a bound stage: at A/0.95/−60 K the helium stage leaves 162.118 MW unremoved and net falls 891.002 → 745.301. | Result to the goal answer (B1); extends prior L-006 from arrangement to source temperature. | work/orchestration/goals/design-space-combinations/answer.md |
| `20260926-aries-design-choice-interactions#2` | model | The recuperation × source-temperature interaction is a limiting-check change, not a ranking reversal, within ±60 K: `heat_removal_ok` flips only at (0.95, −60 K); the difference of differences on net is 145.701 MW on A and 0.000 on N; 0.95 stays preferred at every level on both bases. The mechanism (heater inlet rising with recuperation toward the lowered helium limit) also predicts the 0.90-turbine-efficiency result, where the N corner binds (36.102 MW); the interaction's presence at the N operating point depends on that assumption, its presence at A does not. | Result to the goal answer (B1) with the assumption dependence stated. | work/orchestration/goals/design-space-combinations/answer.md |
| `20260926-aries-design-choice-interactions#3` | model | The sign of the helium-flow effect on net depends on the pump-power law: under the cubic proxy more flow costs net on N (−26.888 / −38.742 MW per step at 0.8) and, on the bound A case, adds unmet heat (+104.555 / +160.975 MW) and costs net (−116.004 / −178.296 MW) because 90 % of the pump power is recovered into the stage that cannot remove it, failing the helium duty rating at 4,700 kg/s; under the fixed law flow changes nothing but the pump capacity screen, which fails at +20 % under both laws. More flow never removed more of the bound stage's heat (fixed law: −1.570 / −0.945 MW), because that stage is limited by the cycle-side inlet temperature. | Result to the goal answer (B2); model-development note: no hydraulic or pump-map model, the friction-recovery path of the proxy is the only mechanism. | work/orchestration/goals/design-space-combinations/answer.md |
| `20260926-aries-design-choice-interactions#4` | model | Over the density window the first check to bind as core output rises is heat removal at the helium stage, never the fuel-processing rating (margin ≥ 1.363e22 atoms/s) nor the compressor (constant margin set by cycle flow); the exchanger arrangement changes where it binds and the net ranking reverses between 5.5e20 (series 735.759 > network 703.212) and 5.75e20 (network 820.519 > series 795.389) at hollowness 0.66; hollowness 0.60 lowers fusion power ≈ 10.8 % and moves the binding out of the window in series. | Result to the goal answer (B3). | work/orchestration/goals/design-space-combinations/answer.md |
| `20260926-aries-design-choice-interactions#5` | process | The helium, PbLi and divertor pump capacity screens sit at margin 0 at every base by the WI-090 demand-matched convention (capacities selected equal to the flows), so a smallest-normalized-margin reading of the limiting equipment lists them first; the reporting excludes nothing and the reading uses the violated set and the next positive margins. | Disclosed here and in the reporting module's output. | exploration/aries_integrated/studies/interactions_reporting.py |
| `20260926-aries-design-choice-interactions#6` | process | The r1 oracle scan refused eight B3 points (nonpositive net at 4.0e20 for every hollowness and at hollowness 0.30 for every amplitude) and showed the temperature level inert on N; the windows were fixed by an oracle-only probe and the r1 preparation retained under `preparation-r1/`. | Recorded in § 11; no native point was spent on a refused window. | this record § 11 |
| `20260926-aries-design-choice-interactions#7` | model | The temperature-level scenario holds each branch's duty and primary flow fixed while shifting its outlet limit; no blanket thermal-hydraulic model links the three, so the level is a consistent scenario only as a question about the exchanger stages, not about a redesigned blanket. A blanket model that couples outlet temperature, flow and duty is the missing relationship. | Declared seam under the brief's no-new-definitions rule; offered to the owner in the goal answer, not opened. | work/orchestration/goals/design-space-combinations/answer.md |

## 16. Snapshot

- **`snapshot.json` sha256:** `25f6bb69fb90b4797fcccbc8c76cc91c0b442093d6f554670430827f6fca824c`
- **Snapshot schema version:** `1`
- **Study id:** `20260926-aries-design-choice-interactions`; **cases:** 52; **numeric outputs per case:** [551]; **verified numeric channels per case:** 364; **exact verdicts per case:** 14; **all evaluated checks satisfied:** 37 of 52.
- **Fingerprints:** indicator inputs `{'recipe': 'indicator-input-fingerprint/v1', 'digest': '06e0627ca37475e7ceaaaefa245e71f2fdfe4acca2af8ccae4a7a049396e9021', 'files': [{'path': 'contracts/model_contract.json', 'sha256': '17d04c97c2055781c84e5e5cb3e3236e12d9d6b85f82dcde09903c8a0da4bd83'}, {'path': 'inputs/integrated_equipment_costs_params.json', 'sha256': 'f01101299ec8c01d45040d2516e754a3829a486719147618218aaf9d226efaa3'}, {'path': 'inputs/mfe_account_costs_params.json', 'sha256': '530c372ebbabec1f846ebed1bdacfb40acab7ebbee241325d9f8a9712cbe585d'}, {'path': 'inputs/mfe_plasma_scaling_params.json', 'sha256': '5de7534cbb8649f962d9c3c59af5f9420543a522de73fbeaae4d1d99074b5c96'}, {'path': 'inputs/mfe_viability_params.json', 'sha256': '36c21e77fec86bc7a986d33124a3424aced99da7a6096bc8eb477f56e3e5a491'}, {'path': 'inputs/plant_params.json', 'sha256': 'f76d6253adde13c357b4306345380b85ec10133771f6b372a401f300cfd031f1'}, {'path': 'inputs/plasma_integration_params.json', 'sha256': '716d2e93ba2294a46860a32c042f3290fc4ed2713ab5a8845a98bdd328d066a0'}, {'path': 'pipelines/pipeline.yaml', 'sha256': '44cc68a58310f41b0e16a5d2b3553b50b9851fdaff31769bec5444bab030052a'}]}`; executable `f739dbce67699b7adfae7c1adf5599ab7c30e85987caad53e0f8affd9b880ce4`; semantic `78dd23bf4c4a2d431ce8223d973db08e955e6f378175623ced8b976db4231f93`; TEAx revision `8d877460ac4f6f264561d916e40c1708adb13397`; repo commit at execution `b98cab9550ae61f494706426d39b1f827858302d`.
- **Store:** `results/native/20260926-aries-design-choice-interactions.db`; **arm:** `arm-interactions`, glue ledger none; **hashed artifacts:** 229; sealed package bytes in `sealed-package.tar.gz`; retained tool, route, model and evidence sources under `results/sources/`.

## 17. What this record does not contain

- **Oracle-derived operand columns.** None beyond the stored channels; every reading is a stored channel or a difference of two.
- **A hydraulic or pump-map model.** The cubic proxy and the fixed law are declared assumptions; the B2 sign result is a property of those two laws.
- **A blanket thermal-hydraulic model.** The temperature level is a scenario at fixed duty and flow (finding #7).
- **Confinement or transport qualification.** Density amplitude and hollowness are fixed-hardware source-demand changes (WI-083 limits).
- **A cost ranking.** The LCOE is tritium-dominated on this package; no case is ranked by LCOE.
- **A boundary claim.** All axes are sensitivity-framed; violations are located, not bounded.
- **The B1 interaction at the N operating point independent of the turbine-efficiency assumption.** At 0.93 it is absent, at 0.90 present (finding #2).
- **Runs of the refused r1 windows.** Eight points were removed after the oracle scan; none executed natively.

