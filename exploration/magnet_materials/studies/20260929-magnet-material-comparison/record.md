# REBCO versus Nb₃Sn winding alternatives at matched duty

**Executed and verified against the integration `CANDIDATE` pin.** Every declared case ran through the stock lifecycle and every stored point agrees with the independent oracle on every non-constant channel, with every verdict re-derived. The integration seam issued the pin on its second run (`integration-r2`, all ten gates pass); its first run (`integration-r1`) refused at the repository-scope gate 5 because the two new canonical SysML files were not registered in `tests/model_families.py`, which commit `c4195090a` repaired without changing a package byte. The results below are from the pinned run; the unpinned first execution was replaced and reproduced identically. This record is the executor's factual deposit; the goal-level interpretation is written by the coordinator.

## 1. Study header

- **Study id:** `20260929-magnet-material-comparison`
- **Package:** `magnet_materials_tea` (`exploration/magnet_materials/magnet_materials_tea`)
- **Date executed:** 2026-09-29
- **Executor:** T-006 study executor (fresh agent), brief `work/orchestration/goals/magnet-material-comparison/evidence/briefs/t006-study-execute.md`
- **Mode:** execute
- **Arms:** single arm, `arm-declared-cases`

## 2. Intake

The owner's goal and scope, in their own words, verbatim.

> For the same specified magnetic duty in a supported operating range, how do explicit REBCO and Nb₃Sn winding alternatives compare in current margin, conductor inventory, winding fit, refrigeration demand, and subsystem cost, and which assumptions determine the preference?

[OWNER-VERBATIM] `evidence/owner-brief.md` § Engineering question, ratified through the goal.

[AGENT] Scope, in the executor's words: the declared case set of `exploration/magnet_materials/studies/declare_cases.py` (2832 cases) evaluated through the WI-099 package against comparison contract r3. Anchors D (EU DEMO TF, primary) and S (Stellaris, secondary); fields 8–13 T on both anchors and the REBCO-only extension 14, 16, 18, 20 T on D; pairings common-P, native and common-C; rule families reference, both-temperature and both-fraction; the reference, insufficient and generous element offers and the insufficient refrigerator; 36 one-at-a-time variants as re-evaluated reference offers and as variant offers. Every case is retained whatever its status. Quantities compared: current margin, superconductor and material inventory, winding fit, cold load and refrigerator electrical demand, and annualized subsystem cost with the matched-pair cost difference and break-even REBCO price.

## 3. Objective and result

- **LCOE objective channel(s):** none; the package has no LCOE. Objective channels per the manifest: `magnet_subsystem__subsystem__pair__cost_difference` (annualized REBCO minus Nb₃Sn, USD2021/yr; ranked only where `pair__rankable` = 1), `magnet_subsystem__subsystem__nb3sn__annualized__annualized_cost`, `magnet_subsystem__subsystem__rebco__annualized__annualized_cost`, `magnet_subsystem__subsystem__pair__breakeven_rebco_price_per_m`.
- **LCOE result:** not applicable. Objective result: at the pinned baseline (anchor D, 10 T, common-P, reference offers) the cost difference is 237,622,172.78 USD/yr (Nb₃Sn 48.52 M, REBCO 286.14 M USD/yr; break-even REBCO price 11.25 USD/m). Over the 610 rankable pairs (both offers pass every evaluated check) the cost difference ranges from −12.18 M to +483.44 M USD/yr, median 206.36 M; the break-even REBCO price ranges 6.62–24.63 USD/m, median 11.25. Source: `results/summary.json` § objective.

REBCO is the dearer subsystem in 598 of the 610 rankable pairs. The 12 pairs where Nb₃Sn is dearer (6 stored points, each with one alias) are all the REBCO-at-10 USD/m volume-price variant on anchor D at 9, 10 and 11 T, common-P and native pairings. Rankable pairs sit on anchor D (574: 530 at 8–11 T under common-P and native, 24 at 8–11 T under common-C, 8 at 12 T of which 6 are common-C and one per common-P and native pairing is the layer-1 steel-base variant offer, and 12 at 13–14 T under common-C only, where Nb₃Sn is edge or law-only) and on anchor S under the common-C pairing only (36: 24 at 8–11 T, 12 at 12–13 T). The remaining 2222 cases carry no ranking because at least one offer fails a check or is unsupported.

## 4. Constraint outcomes

Every executing constraint, by qualified identity, with its status over the 2832 declared cases (`results/cases.json`; per-point counts over the 2310 stored points in `results/summary.json`). No verdict was indeterminate.

| `constraint_id` | `source_local_identity` | Status | Note |
|---|---|---|---|
| `magnet_subsystem__subsystem__nb3sn__acceptance_ok__6ecc44a52542ba77` | `acceptance_ok` | satisfied 2045, violated 787 | Nb₃Sn: supported status and rule margin ≥ 0; violated at every 16–20 T evaluation (unsupported, 540), under every insufficient offer at a supported, edge or law-only field (117), and where fixed reference hardware misses the rule under the three −0.6 % strain variants and the BEAS II and BEAS TFEU10-12 grade variants (130); over 2310 stored points 1635/675 |
| `magnet_subsystem__subsystem__nb3sn__fit_ok__768d741c21386f93` | `fit_ok` | satisfied 843, violated 1989 | Nb₃Sn: gross turn area ≤ envelope; violated on anchor D common-P and native from 12 T up (83–84 of 84 per field, plus one 11 T case per pairing under the layer-8 steel variant offer) and under common-C at 18–20 T (21), and at every anchor S common-P and native case (960); over 2310 stored points 713/1597 |
| `magnet_subsystem__subsystem__nb3sn__copper_ok__a4ff5a6abedecdd2` | `copper_ok` | satisfied 2746, violated 86 | Nb₃Sn: supplied copper ≥ allowance requirement; violated only under insufficient element offers (86 of 144); over 2310 stored points 2224/86 |
| `magnet_subsystem__subsystem__nb3sn__steel_ok__5d849655e24deaf4` | `steel_ok` | satisfied 2780, violated 52 | Nb₃Sn: supplied steel ≥ allowance requirement; violated only where a steel-basis variant re-evaluates fixed hardware (layer-8 base 32, no field scaling 20); over 2310 stored points 2258/52 |
| `magnet_subsystem__subsystem__nb3sn__capacity_ok__c900a95e873755be` | `capacity_ok` | satisfied 2648, violated 184 | Nb₃Sn: installed cold-stage rating ≥ cold load; violated under every insufficient refrigerator (144), cold-load ×2 (32; rating list exhausted at 18 and 20 T), 60 m turn length (4) and the ×2 variant offers above 75 kW (4); over 2310 stored points 2126/184 |
| `magnet_subsystem__subsystem__rebco__acceptance_ok__904ca5528ef92aa4` | `acceptance_ok` | satisfied 2596, violated 236 | REBCO: supported everywhere; violated under every insufficient offer (144) and where a re-evaluated reference offer misses the rule under T* 17 K (30), degradation 0.80 (32) or the power-law shape (30); over 2310 stored points 2074/236 |
| `magnet_subsystem__subsystem__rebco__fit_ok__977ffb782260e056` | `fit_ok` | satisfied 1932, violated 900 | REBCO: gross turn area ≤ envelope; violated on anchor D common-P from 13 T up (83–84 of 84 per field, plus one 12 T case) and at every anchor S common-P case (480); over 2310 stored points 1578/732 |
| `magnet_subsystem__subsystem__rebco__copper_ok__b9db08c2aa4dd8f9` | `copper_ok` | satisfied 2784, violated 48 | REBCO: supplied copper ≥ allowance requirement; violated only under insufficient element offers (48 of 144); over 2310 stored points 2262/48 |
| `magnet_subsystem__subsystem__rebco__steel_ok__4f587fec2c667312` | `steel_ok` | satisfied 2790, violated 42 | REBCO: supplied steel ≥ allowance requirement; violated only under the steel-basis variants (layer-8 base 16, no field scaling 26); over 2310 stored points 2268/42 |
| `magnet_subsystem__subsystem__rebco__capacity_ok__ea481269af095f7f` | `capacity_ok` | satisfied 2650, violated 182 | REBCO: installed cold-stage rating ≥ cold load; violated under every insufficient refrigerator (144), cold-load ×2 (32), 60 m turn length (2) and the ×2 variant offers above 75 kW (4); over 2310 stored points 2128/182 |

The MR-7 acceptance tests of contract § 5 are visible in these counts: every insufficient element offer fails acceptance (0 of 144 pass per material) and every insufficient refrigerator fails capacity (0 of 144 pass per material), while generous offers pass acceptance wherever the conductor is supported (Nb₃Sn 117 of 144, the 27 failures being the 16–20 T unsupported evaluations; REBCO 144 of 144). Per-check counts, near-threshold counts and the status breakdown by anchor and field are in `results/summary.json` § materials.

## 5. Framing

**As proposed at intake.**

| Axis | Framing proposed | Why |
|---|---|---|
| `duty` | search | The field point walks Nb₃Sn across its supported, edge, law-only and unsupported bands and both materials across the fit boundary of a fixed envelope; verdict structure is the point of the axis. |
| `nb3sn-offer` | search | The insufficient, reference and generous element offers and the insufficient refrigerator are chosen to straddle the acceptance, fit and capacity verdicts (MR-7 tests). |
| `rebco-offer` | search | Same construction as `nb3sn-offer`. |
| `nb3sn-conductor-assumptions` | sensitivity | One-at-a-time variants of strand grade, strain, margin rule and construction rule, re-evaluated on fixed hardware and as variant offers; the question is how the preference moves, with no boundary claim in assumption space. |
| `rebco-conductor-assumptions` | sensitivity | One-at-a-time variants of anchor Ic, shape, T*, degradation and construction rule; same reasoning. |
| `cryogenic-assumptions` | sensitivity | Cold-load multiplier, efficiency and capital basis, turn length; how demand and cost respond. |
| `economic-assumptions` | sensitivity | Prices, capital recovery, electricity; the break-even price is the reported response. Nothing in the model bounds a price. |

**As judged after the run.**

| Axis | Framing judged | Changed? | Why |
|---|---|---|---|
| `duty` | search | no | Acceptance flips with field at 13 T (edge) and 16 T (unsupported) for Nb₃Sn; fit flips at 12 T (Nb₃Sn, anchor D common-P/native) and 13 T (REBCO, anchor D common-P); on anchor S fit is decided by pairing, not field. |
| `nb3sn-offer` | search | no | Every insufficient offer fails acceptance and every insufficient refrigerator fails capacity; generous offers pass acceptance where supported. The verdict structure the offers were built to show is present. |
| `rebco-offer` | search | no | Same. |
| `nb3sn-conductor-assumptions` | sensitivity | no | Re-evaluated fixed hardware fails acceptance under the three −0.6 % strain variants and the BEAS II and BEAS TFEU10-12 grades (26 cases each); the variant offers restore acceptance except the six carried offers at 20 T. These are located flips on fixed hardware, not a boundary in assumption space. |
| `rebco-conductor-assumptions` | sensitivity | no | Fixed hardware fails acceptance under T* 17 K, degradation 0.80 and the power-law shape; variant offers restore it. No boundary claim. |
| `cryogenic-assumptions` | sensitivity | no | Cold-load ×2 fails capacity on fixed hardware (32 per material) and exhausts the rating list at 18 and 20 T; the 60 m turn length fails capacity in 4 (Nb₃Sn) and 2 (REBCO) cases. Every other cryogenic variant leaves verdicts and the preference sign unchanged. |
| `economic-assumptions` | sensitivity | no | No verdict moved under any economic variant. The preference sign changes only under the REBCO 10 USD/m volume price at 9–11 T on anchor D; the Nb₃Sn price levels and Nb₃Sn-only manufacturing move the break-even price by more than 10 %. |

## 6. Per-axis account

#### `duty` — feasible structure (search framing)
**Applies:** yes

Active constraints along the field axis, at reference offers under the reference rule family (`results/summary.json` § reference_offer_pairs): on anchor D under common-P and native, Nb₃Sn `fit_ok` is the first check to fail, at 12 T (fit margin −178.6 mm² at n = 822, gross 3929.7 mm² against the 3751.1 mm² envelope; +359.5 mm² at 11 T). REBCO fits through 12 T on common-P (+87.8 mm²) and fails from 13 T (−385.1 mm²); on native it fits at every field (≥ +2237 mm²). Nb₃Sn `acceptance_ok` fails from 16 T (unsupported status), never earlier at reference offers. Under common-C both materials fit through 14 T on anchor D and Nb₃Sn fits until 16 T (+1042 mm²) and fails from 18 T. On anchor S neither material fits the 420.8 mm² envelope under common-P at any field (Nb₃Sn −57.5 to −625.2 mm², REBCO −48.0 to −532.1 mm²); REBCO fits under native and both fit under common-C at every field 8–13 T. No constrained optimum is sought; the rankable region on anchor D is 8–11 T for common-P and native at reference offers (12 T only for the layer-1 steel-base variant offer, one pair per pairing) and 8–14 T for common-C (13–14 T with Nb₃Sn edge or law-only status), and on anchor S it is common-C only.

#### `duty` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `nb3sn-offer` — feasible structure (search framing)
**Applies:** yes

Acceptance is active at the insufficient offer everywhere (0 of 144 pass) and satisfied at the reference and generous offers wherever the conductor is supported; the reference offers sit at the rule by construction (2332 of 2832 Nb₃Sn acceptance margins within 2 % of the requirement). Copper is active only at insufficient offers (86 fail), steel never at any offer of this axis. Capacity is active at the insufficient refrigerator everywhere (0 of 144 pass). Fit is not moved by element count enough to flip except where the envelope is already marginal: 66–67 of 144 insufficient and generous offers fit, the same anchor-D low-field and common-C cases that fit at reference.

#### `nb3sn-offer` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `rebco-offer` — feasible structure (search framing)
**Applies:** yes

Same structure: acceptance active at every insufficient offer (0 of 144 pass), satisfied at every reference and generous offer (REBCO is supported at every case); copper active only at insufficient offers (48 fail); capacity active at every insufficient refrigerator (0 of 144 pass); fit unchanged by element count except at marginal envelopes (111 of 144 insufficient and generous offers fit).

#### `rebco-offer` — observed response (sensitivity framing)
**Applies:** not applicable — this axis is search-framed

#### `nb3sn-conductor-assumptions` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `nb3sn-conductor-assumptions` — observed response (sensitivity framing)
**Applies:** yes

No boundary claim is made. Where fixed reference hardware is re-evaluated: the three −0.6 % strain variants and the BEAS II (Tsui) and BEAS TFEU10-12 grade variants each fail Nb₃Sn acceptance in 26 of 32 cases (the other 6 are the 16–20 T evaluations, already violated at reference), removing all 8 rankable pairs of each variant; OST TFEU9, the 6.5 K supply and both copper-density variants flip nothing and keep the preference sign and break-even within 10 %. The steel-basis variants (in the construction-rule keys of this group) fail Nb₃Sn steel on fixed hardware in 32 (layer-8 base) and 20 (no field scaling) cases; the layer-1 base flips nothing. Variant offers under each assumption restore acceptance except the six carried-reference offers at 20 T (−0.6 % strain, all three grades, both pairings), where no element count meets the rule. Violations located: acceptance at every field of the affected variants on anchor D and S; steel at the fields where the raised requirement exceeds the supplied area (`results/cases.csv`).

#### `rebco-conductor-assumptions` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `rebco-conductor-assumptions` — observed response (sensitivity framing)
**Applies:** yes

No boundary claim is made. On fixed reference hardware, T* 17 K and the power-law shape fail REBCO acceptance in 30 of 32 cases each, degradation 0.80 in 32 of 32; T* 33 K, anchor 225 A and degradation 0.95 flip nothing and keep the preference sign and break-even within 10 %. The steel-basis variants fail REBCO steel in 16 (layer-8 base) and 26 (no field scaling) cases. Variant offers restore acceptance in every case (no carried REBCO offer).

#### `cryogenic-assumptions` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `cryogenic-assumptions` — observed response (sensitivity framing)
**Applies:** yes

No boundary claim is made. Cold-load ×2 fails capacity on fixed hardware in 32 cases per material and, at 18 and 20 T on anchor D, exhausts the rating list so that the variant offer (75 kW) also fails (4 per material, demand 75.8–82.0 kW). Cold-load ×0.5, the 20 K input-power and capital-basis variants, constant η 0.24, the combined unfavourable 20 K case and the 45 m turn length flip no verdict and keep the sign and break-even within 10 %; the 60 m turn length fails capacity in 4 Nb₃Sn and 2 REBCO cases. For anchor D at 11 T and above the policy's listed rating is 50 kW, outside the Green fit range (0.01–35 kW), so `green_extrapolated` = 1 in 1187 Nb₃Sn and 1129 REBCO cases (all anchor D); electrical demand at anchor D is 21.6–23.6 MW (Nb₃Sn) and 17.3–18.0 MW (REBCO) at reference offers, about 16 MW of each being the common 77 K intercept stage.

#### `economic-assumptions` — feasible structure (search framing)
**Applies:** not applicable — this axis is sensitivity-framed

#### `economic-assumptions` — observed response (sensitivity framing)
**Applies:** yes

No boundary claim is made, and no verdict moved under any economic variant. The cost-difference sign holds under every economic variant except REBCO at 10 USD/m, which makes Nb₃Sn dearer at 9, 10 and 11 T on anchor D (6 of 8 rankable pairs of that variant; 8 T stays REBCO-dearer). Nb₃Sn at 5.4 and 13.5 USD/m and Nb₃Sn-only manufacturing move the break-even REBCO price by more than 10 %; capital recovery 0.05/0.11, electricity 30/120 USD/MWh, REBCO 30 USD/m and manufacturing on both keep it within 10 %. No constraint responds to this axis in fact (§ 8).

## 7. Axis groups

Every declared qualified entry key, with its per-key provenance. Key prefix `magnet_subsystem__subsystem__` is omitted in the table; the full keys are in `axes.json` (sha256 `adf6d76840d701ec3eac3dd5659ce8c1037e44bfd6fd654a57f843eadef707a8`). Every key is `fan_out`: each design § 6 attribute emits exactly one entry key, and no tie is declared.

| Axis | Entry key | Provenance | Note |
|---|---|---|---|
| `duty` | 7 keys: `duty__B_peak`, `duty__B_ref`, `duty__I_ref`, `duty__available_area`, `duty__coils`, `duty__turns`, `duty__turn_length` | `fan_out` (every key) | `B_peak` is the field point; `turn_current` = `I_ref`·`B_peak`/`B_ref` is a derived channel, not a key. |
| `nb3sn-offer` | 9 keys: `nb3sn__n_elements`, `nb3sn__cabling_factor`, `nb3sn__cable_void`, `nb3sn__cu_space`, `nb3sn__steel_area`, `nb3sn__misc_area`, `nb3sn__solder_area`, `nb3sn__ins_fraction`, `nb3sn__rating_cold` | `fan_out` (every key) | The supplied offer (MR-7 chosen role). |
| `rebco-offer` | 9 keys: `rebco__n_elements`, `rebco__cabling_factor`, `rebco__cable_void`, `rebco__cu_space`, `rebco__steel_area`, `rebco__misc_area`, `rebco__solder_area`, `rebco__ins_fraction`, `rebco__rating_cold` | `fan_out` (every key) | The supplied offer (MR-7 chosen role). |
| `nb3sn-conductor-assumptions` | 26 keys: `nb3sn__T_supply`, `nb3sn__nuclear_rise`, `nb3sn__margin_rise`, `nb3sn__fraction_rule`, `nb3sn__acceptance_rule`, `nb3sn__strand_diameter`, `nb3sn__strand_copper_fraction`, `nb3sn__p`, `nb3sn__q`, `nb3sn__C1`, `nb3sn__Ca1`, `nb3sn__Ca2`, `nb3sn__eps0a`, `nb3sn__Bc20`, `nb3sn__Tc0`, `nb3sn__conductor__eps_intrinsic_in`, `nb3sn__J_cu_rule`, `nb3sn__cu_void`, `nb3sn__cu_per_kA_rule`, `nb3sn__steel_per_kA_rule`, `nb3sn__B_steel_ref`, `nb3sn__steel_B_scaling`, `nb3sn__element_density`, `nb3sn__rho_cu`, `nb3sn__rho_steel`, `nb3sn__rho_solder` | `fan_out` (every key) | `eps_intrinsic` binds at the calc input (implementation notes, deviation 1). |
| `rebco-conductor-assumptions` | 28 keys: `rebco__T_supply`, `rebco__nuclear_rise`, `rebco__margin_rise`, `rebco__fraction_rule`, `rebco__acceptance_rule`, `rebco__tape_width`, `rebco__tape_thickness`, `rebco__tape_copper_fraction`, `rebco__anchor_ic`, `rebco__shape_mode`, `rebco__g8`, `rebco__g10`, `rebco__g12`, `rebco__g15`, `rebco__g20`, `rebco__alpha`, `rebco__T_star`, `rebco__degradation`, `rebco__J_cu_rule`, `rebco__cu_void`, `rebco__cu_per_kA_rule`, `rebco__steel_per_kA_rule`, `rebco__B_steel_ref`, `rebco__steel_B_scaling`, `rebco__element_density`, `rebco__rho_cu`, `rebco__rho_steel`, `rebco__rho_solder` | `fan_out` (every key) | — |
| `cryogenic-assumptions` | 42 keys: `nb3sn__nuclear_density`, `nb3sn__cold_volume`, `nb3sn__radiation_ref`, `nb3sn__conduction_ref`, `nb3sn__T_conduction_ref`, `nb3sn__n_leads`, `nb3sn__f_lead`, `nb3sn__L0`, `nb3sn__p_joint_ref`, `nb3sn__I_joint_ref`, `nb3sn__shield_static`, `nb3sn__load_multiplier`, `nb3sn__eta_mode`, `nb3sn__eta_const`, `nb3sn__green_a`, `nb3sn__green_b`, `nb3sn__f_carnot_shield`, `nb3sn__capital_mode`, `nb3sn__green_c`, `nb3sn__green_d`, `nb3sn__T_green`, and the same 21 under `rebco__` | `fan_out` (every key) | Each material part carries its own copy; the case generator sets both equal except where the variant is material-specific. |
| `economic-assumptions` | 15 keys: `economics__crf`, `economics__availability`, `economics__electricity_price`, `economics__hours`, `economics__usd2015_to_2021`, `nb3sn__price_cu`, `nb3sn__price_steel`, `nb3sn__price_solder`, `nb3sn__element_price_per_m`, `nb3sn__manufacturing_per_m`, `rebco__price_cu`, `rebco__price_steel`, `rebco__price_solder`, `rebco__element_price_per_m`, `rebco__manufacturing_per_m` | `fan_out` (every key) | — |

The 27 fixed design values (law domains, `T_shield`, `T_amb`, `eps_max`, NIST `k_b`, `k_c`, `k_e`, `k_f`, `k_h` per material) are entry keys held at their design values in every case and are not axes.

## 8. Indicators and rulings

Per proposed axis, including axes proposed and declined. All seven groups were traced in one run (`indicators.json`, no `--group` subset); none was declined.

| Axis | Indicator | Ruling | Note |
|---|---|---|---|
| `duty` | `constraints_reachable` | not required | Swept. All ten constraints and all four objectives reachable. |
| `nb3sn-offer` | `constraints_reachable` | not required | Swept. The five Nb₃Sn constraints reachable; the five REBCO constraints and `annualized_rebco` unreachable, as the parts are independent. |
| `rebco-offer` | `constraints_reachable` | not required | Swept. Mirror of `nb3sn-offer`. |
| `nb3sn-conductor-assumptions` | `constraints_reachable` | not required | Swept. Five Nb₃Sn constraints reachable, REBCO's unreachable. |
| `rebco-conductor-assumptions` | `constraints_reachable` | not required | Swept. Five REBCO constraints reachable, Nb₃Sn's unreachable. |
| `cryogenic-assumptions` | `constraints_reachable` | not required | Swept. Only `capacity_ok` (both materials) reachable; acceptance, fit, copper and steel unreachable. |
| `economic-assumptions` | `constraints_reachable` | not required | Swept. Only `capacity_ok` reachable, and only because `usd2015_to_2021` enters the refrigeration module (for refrigerator capital) and the trace is module-level; the executor's recorded judgment is `unresisted`: no constraint responds to a price, finance or electricity input, and the run confirmed no verdict moved (§ 6). |

**Not derivable, disclosed in every record.** These are not decidable from the indicator run and no indicator output claims them: monotonicity of any channel in any axis; identity of the same physical quantity across differing key names; intra-module operand dependency. `constraints_reachable` is a *possible* path and never a statement that a constraint responds. `unresisted` is the agent's recorded judgment, never a tool output.

**Model-development findings.** No axis reported `no_constraint_response`, so no owner ruling was required before execution and no finding is owed by that rule. The `economic-assumptions` judgment `unresisted` is carried as finding `20260929-magnet-material-comparison#3` under the same intent (§ 15): nothing pushes back on a price or finance assumption, and the model reports a break-even price rather than bounding one.

| Axis | What should push back and is not modeled | Finding id |
|---|---|---|
| `economic-assumptions` | No cost ceiling, price floor or budget bound exists in the model; the comparison reports a break-even price as its only response to prices. (Judgment-based, not a `no_constraint_response` indicator.) | `20260929-magnet-material-comparison#3` |

## 9. Preflight results

Every mechanical gate that ran, with its outcome. The identity and baseline gates read `results/package_identity.json` and `results/baseline_result.json`, deposited by `run_baseline.py` through `study_route.execute_baseline` with this record's manifest; the results document is `results/preflight_results.json`.

| Gate | Outcome | Detail |
|---|---|---|
| Declared-group key validation | pass | 136 declared keys across 7 groups, all package inputs |
| Suffix-sibling scan (warnings only) | pass | no warnings; the per-group `sibling_candidates` are the other material's same-named attributes, each declared in its own group |
| Baseline gate against the pinned headline | pass | `pair__cost_difference` 237,622,172.77682102 reproduces at relative deviation 0; 5/5 pinned verdicts match (`results/baseline_result.json`) |
| Manifest / package fingerprint match | pass | both recorded package fingerprints match the package on disk (`results/package_identity.json`: kind sealed, digest `7075e929…2e3f`, 0 allowed-modified files) |
| Package cleanliness | pass | package tree byte-untouched at preflight, after the study run (`execute_study.py`), after the stock verification (`verify.py`) and at snapshot time (`snapshot.json` `package.git_clean` true) |

**Integration seam** (`scripts/integrate.py`, audited work `work/active/WI-099_magnet-conductor-alternatives@c4195090a`, out-dir `work/orchestration/goals/magnet-material-comparison/evidence/integration-r2/`, return `integration_return.json`, class `CANDIDATE`, exit 0; copied to `results/integration_return_used.json`). Pin `2d10694e8b9b2f4b84d53cbf4417f99d406f82d177a1181b25582eb0ee7ea6ee` (the manifest's indicator-inputs digest), semantic `4d37dbaf827df325d2a0dd19ee4c44c623cf3e67ed7f44552a1ae46b2ef1c2f6`, executable `7075e929abf1133e5dc6d21ac7f65b370e6e88cd322906fc88501270c9592e3f`:

| Seam gate | Outcome | Detail |
|---|---|---|
| 0 preconditions | pass | inputs resolve, environment complete, simkit imports, package git-clean |
| 1a pinned-packages | pass | `tests/test_dependency_provenance.py` passed |
| 1b teax-revision | pass | teax at `8d877460ac4f6f264561d916e40c1708adb13397`, as expected |
| 2 regeneration | pass | regeneration through `magnet_materials_tea` rewrote no byte outside `handwritten/` |
| 3 handwritten-preservation | pass | 27 files under `handwritten/` byte-identical |
| 4 census-snapshot | pass | snapshot recaptures byte-identically; 163 entry points re-derive to the census as bound |
| 5 model-family-spine | pass | `tests/models/test_model_family_spines.py` passed (15 checks) |
| 6 manifest | pass | manifest identity, pin `2d10694e…` and resolved reference coverage pass |
| 7 preflight | pass | baseline Python read coverage `20312631…`; all six preflight gates pass on the seam's own baseline |
| 8 verification | pass | oracle parity holds and every verdict re-derived (seam sample over its baseline store) |
| 9 lineage | pass | live semantic and executable fingerprints are the lineage the request named |

**First attempt** (`integration-r1/integration_return.json`, audited work `@2869c34aa`, class `BLOCKER`, exit 1): gates 0–4 passed; gate 5 `model-family-spine` refused (scope `repo`, condition `repo-lineage-broken`: `test_owned_paths_cover_every_canonical_file` found `analyses/magnet_conductor_alternatives.sysml` and `designs/magnet_materials/magnet_subsystem.sysml` unregistered); gates 6–9 not reached. Commit `c4195090a` registered `SOURCE_COLLECTIONS["magnet_materials"]` in `tests/model_families.py`; the package bytes and both fingerprints are unchanged, as gates 2–4 and 9 of the second run confirm. Both out-dirs are kept.

## 10. Execution route and why

- **Route:** study-local direct-API, `exploration/magnet_materials/studies/study_route.py:run_cases` (stock `ProvisionalPackageLoader`, `PreparedEvaluator`, `StudyRunner`, `PreparedListStrategy`, `StudyStore`, `StudyQuery`), driven by `execute_study.py` in this record.
- **Why this route:** the candidate set is a declared list of coordinated cases (an anchor's seven duty attributes, an offer's nine quantities, a pairing's construction rules and a variant's assumption all move together), not a Cartesian grid, so the `teax-study` CLI does not apply. The route was exercised at step 5 (baseline) and gated at step 6 before this rationale was written. Each declared case is mapped to the complete 163-key entry map by `study_route.case_point`; 2310 distinct entry maps were evaluated once each and all 2832 declared cases are exported with their aliases (`results/case_aliases.json`: 506 alias groups, 522 aliased cases). Every stored point completed; 52 s wall time (`results/execution-context.json`).

**Glue disclosure.** Glue ledger: none. No adapter on this route, so nothing is harness-supplied; the model computes every channel from the case inputs. One disclosure that is not glue: the oracle is bound through the record-local `oracle_entry.py` named by this record's manifest, because the module the stock `studies/manifest.json` names does not exist; the adapter maps names only (entry keys to design § 6 attributes, oracle outputs to channel names, assert operands to their bound channels) and no physics or tolerance. `execute_study.py` checked the `CANDIDATE`'s pin and both fingerprints against the manifest and the reviewed interface before running (`results/execution-context.json`: `integration_class: CANDIDATE`, `without_candidate: false`). An earlier execution of the same list, run before the pin existed under a disclosed deviation, was replaced; the pinned run reproduced every output, verdict and candidate id of it exactly.

## 11. Study definition and window provenance

The candidate range is the declared case list, not a swept window. Before any point ran, every one of the 2832 cases was evaluated with the independent oracle (`oracle_scan.py`, `results/oracle_scan.json`): Nb₃Sn status supported 1760, edge 352, law-only 180, unsupported 540; REBCO supported 2832; Nb₃Sn passing every check 634, REBCO 1598; 610 rankable pairs (D 574, S 36; common-P 266, native 266, common-C 78); REBCO dearer in 598 and Nb₃Sn dearer in 12; near-threshold margins (within 2 % of the requirement) at acceptance in 2332 Nb₃Sn and 2416 REBCO cases and at copper and steel in nearly every case, both by construction of the offer policy (the smallest passing element count; areas rounded up to 1e−6 mm², design D1); the six carried-reference Nb₃Sn offers and the eight rating-list-exhausted offers noted in `oracle-notes.md` are present. No nonfinite oracle output occurred. The scan fixed nothing: no case was excluded on its status, and the executed list equals the declared list.

The window is engineered: it is the contract's declared grid of anchors, fields, pairings, rule families, offers and variants, and the offers are the declared policy's, not a sourced operating envelope. That costs any claim of a continuous feasible boundary or an optimum; the record locates verdict flips at declared points only. No validity mask was applied.

## 12. Cross-fingerprint correlation and what it means

Single fingerprint — no cross-arm correlation needed. Every stored point in both stores ran under executable fingerprint `7075e929abf1133e5dc6d21ac7f65b370e6e88cd322906fc88501270c9592e3f` and model contract `4d37dbaf827df325d2a0dd19ee4c44c623cf3e67ed7f44552a1ae46b2ef1c2f6`; the compatibility tuples are in `snapshot.json` under `stores[]`.

## 13. Verification

**Passed, twice, over every stored point.** The stock verifier (`scripts/study/verify.py`, `--sample-size 2310` so that the stratified sample covers all 2310 study points and the baseline point; 34 verdict strata observed) compared the 16 objective and operand channels at relative deviation below 1e−9 or the declared absolute tolerance of 1e−9 per unit and re-derived all ten verdicts from the oracle's operands: outcome pass, worst relative deviation 3.32e−5 on `nb3sn__conductor__acceptance_margin` = 7.88e−7 K (absolute error 2.6e−11 K, inside the contract's absolute clause). The full comparison (`verify_all.py`, `results/verification_full.json`) then compared all 128 non-constant channels of every stored point under the same rule and re-derived every verdict: 0 disagreements, 0 verdict mismatches; worst relative deviation 3.32e−5 (the same near-zero margin, Brent versus bisection root), worst absolute error 1.19e−7 USD/yr on an annualized cost of order 1e8 (relative 1e−16). No nonfinite value occurred on either side. This licenses the statement that the generated package reproduces the independently written equations of the contract and design at every executed case, to the contract's tolerance, and that every recorded verdict follows from the oracle's own operands.

**Not covered.** (1) The nine constant formula channels (`eps_min`, `k_a`, `k_d`, `k_g`, `k_i` per material) are fixed design values the oracle carries as its own constants; they were excluded and listed, not compared. (2) The 27 fixed design values and every case input are fed identically to the package and the oracle, so parity verifies the package's arithmetic given those values, not the values. (3) The oracle was written from the contract and design, not from sources; source fidelity rests on the T-004 checks (§ 14), and the design ambiguities the oracle author resolved (`oracle-notes.md` A1–A21) are shared readings, not independent evidence. (4) Alias cases were verified once per stored point, not once per declared case. (5) The absolute-tolerance clause was declared in this record's manifest (16 channels) from the contract's § 8 wording; the stock `studies/manifest.json` declares none. (6) `verify.py` records `teax.revision: "unrecorded"`; the seam return records the checkout at `8d877460…`. (7) The seam's own gate-8 verification sampled only its baseline store; the study store is covered by the two verifications above, not by the seam.

## 14. Review outcomes

| Lens | Verdict | Disposition |
|---|---|---|
| Contract review r1→r3 and design review (`evidence/contract-review.md`, same independent reviewer; § Recheck r3: FINDINGS with one blocking design change D1; § Recheck D1–D7: PASS) | PASS at r3 | Reused as valid coverage: same contract revision, same design (with § 7 clarifications), same package lineage. No new or reinterpreted equation entered this study, so no further pre-execution critic was convened. |
| Independent check A, Nb₃Sn law and data (`evidence/check-nb3sn.md` § Recheck r3) | PASS, one advisory (−0.6 % strain) | Reused; the advisory's case (grade effect at −0.6 %) is in the case set as the three strain variants. |
| Independent check B, REBCO, cryogenics, cost (`evidence/check-rebco-cryo-cost.md` § Recheck r2) | resolved findings | Reused; the 20 K input-power factor and capital-basis sensitivities it required are in the case set. |
| Coordinator check of this record's preparation | executor self-check | Axis groups cover all 136 design attributes exactly once; manifest validates with the stock fingerprints; adapter maps names only. Not an independent review. |
| Integration seam (`scripts/integrate.py`) | CANDIDATE, ten gates pass (`integration-r2`) | Pin and fingerprints recorded (§ 9, § 16). First attempt refused at gate 5, scope repo; resolved by `c4195090a` (finding #1). |
| Stock verification (`scripts/study/verify.py`) | PASS over all 2311 stored rows | § 13. |
| Full-channel verification (`verify_all.py`) | PASS, 128 channels × 2310 points, 10 verdicts re-derived | § 13. |

No administrator reading was requested; none is claimed. Any independent reading of this record must come from a fresh non-author session.

## 15. Findings

Each finding gets an id used verbatim in `DISCOVERY_LOG.md`, of the form study-id#n; first-sighting rows for all seven are appended there.

| Id | Kind | Finding | Disposition | Home |
|---|---|---|---|---|
| `20260929-magnet-material-comparison#1` | process | The integration seam's first run refused at gate 5 (`model-family-spine`, scope repo, `repo-lineage-broken`): `models/library/analyses/magnet_conductor_alternatives.sysml` and `models/designs/magnet_materials/magnet_subsystem.sysml` were not registered in `tests/model_families.py`, so no `CANDIDATE` pin existed for this package. | Resolved by registration: commit `c4195090a` adds `SOURCE_COLLECTIONS["magnet_materials"]` (package bytes unchanged); the second seam run (`integration-r2`) returned `CANDIDATE` and the study was re-executed against its pin. | `tests/model_families.py` (registration, commit `c4195090a`) |
| `20260929-magnet-material-comparison#2` | process | The stock `exploration/magnet_materials/studies/manifest.json` names oracle module `exploration.magnet_materials.studies.oracle_entry`, which does not exist; the stock verifier cannot run from that manifest. | This record binds the oracle through its own `oracle_entry.py` and declares the contract's absolute tolerance clause in its manifest copy. The package-level module and tolerance declarations remain to be written. | `exploration/magnet_materials/studies/manifest.json` (WI-099) |
| `20260929-magnet-material-comparison#3` | model | Nothing in the model pushes back on a price, finance or electricity assumption: the economic axis reaches no constraint in fact (the trace's `capacity_ok` reachability is a module-level artifact of `usd2015_to_2021` entering the refrigeration module), and the preference sign reverses under REBCO at 10 USD/m at 9–11 T without any verdict moving. | Sensitivity-framed and reported as break-even price; declared seam. | `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` § 8 (break-even reporting) |
| `20260929-magnet-material-comparison#4` | model | On anchor D under construction P (common-P and native), Nb₃Sn fails fit at 12 T at its reference offer (−178.6 mm², 4.8 % of the envelope, n = 822), so the primary matched comparison ranks 8–11 T there at reference offers (12 T only for the layer-1 steel-base variant offer); under common-C both materials fit through 14 T. Every turn is sized at peak field with pack-average steel (contract § 2 stated limits, N2). | Fact of the run under a declared conservatism; no material limit is claimed. | `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` § 2 (N2) |
| `20260929-magnet-material-comparison#5` | model | On anchor S neither material fits the 420.8 mm² envelope under construction P at any field 8–13 T (Nb₃Sn −57.5 to −625.2 mm², REBCO −48.0 to −532.1 mm²); only the common-C pairing ranks (36 pairs). Fit on the compact anchor is a construction verdict, as the contract's § 2 role for S anticipated. | Fact of the run; declared seam. | `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` § 2 (anchor S role and stated limits) |
| `20260929-magnet-material-comparison#6` | model | For anchor D at 11 T and above the policy's listed cold-stage rating is 50 kW, outside the Green refrigerator fit range (0.01–35 kW): `green_extrapolated` = 1 in 1187 Nb₃Sn and 1129 REBCO cases, so refrigerator efficiency and capital at most anchor-D duty points are extrapolations of the fitted laws. | Flagged per case in the store; no verdict depends on the flag. | `work/orchestration/goals/magnet-material-comparison/evidence/comparison-contract.md` § 6 (refrigerator laws) |
| `20260929-magnet-material-comparison#7` | process | 522 of 2832 declared cases carry entry maps byte-identical to another declared case (economics-only variants whose variant offer equals the re-evaluated reference; variants whose value equals the pairing's reference), so the lifecycle stored 2310 points. | Every declared case exported with its aliases (`results/case_aliases.json`); no case dropped. | `exploration/magnet_materials/studies/declare_cases.py` (case generator; the duplication is by design of the variant grid) |

## 16. Snapshot

- **File:** `snapshot.json`
- **sha256:** `9f16a48c904b4949509ebe4a76e949dab58198c954af0fee6f43c09226a7596a`
- **Schema version:** `1`

No snapshot content is restated here.

## 17. What this record does not contain

- The unpinned first execution's results: they were replaced by the pinned run (identical outputs, verdicts and candidate ids) and are not kept; only the first seam attempt's return (`integration-r1/`) remains, cited in `snapshot.json`.
- No goal-level interpretation, preference call, figures or answer: §§ 3–6 and 13 are factual; the coordinator writes the reading.
- No administrator synthesis (`synthesis.md`).
- No sealed copy of the package or of the oracle sources; the record cites them by path and digest (`snapshot.json`), and `git status` at execution shows the package clean at repository commit `c4195090aba1beef344c983a61364d355eab5a34`.
- No source-fidelity evidence of its own: the oracle and the package were both written from contract r3 and the design; the source checks are cited, not repeated.
- No evaluation of stress, quench, irradiation, AC loss, joints and leads, layer grading, field change from winding size, or plasma performance (contract § 9).
- No `pkg_link` import alias: the loader's symlink under `results/native/` and `results/_work/` was removed after each run (`.gitignore` also ignores it).
- **Not in git (machine-local, digests in `snapshot.json` `arms[].artifacts`):** `results/cases.json` (68 MB), `results/oracle_scan.json` (6.4 MB), `results/native/` (store 45 MB and 2310 artifact files, 37 MB) and `results/_work/` (baseline store and artifact), per `.gitignore` at commit `c4195090a`; also the declared case list `exploration/magnet_materials/studies/cases.json` (12.3 MB; sha256 in `results/cases_declared.json`, regenerated deterministically by `declare_cases.py`). They stay on the machine that ran the study. What is in git: `record.md`, `snapshot.json`, `indicators.json`, `axes.json`, `manifest.json`, the record scripts, and under `results/` the baseline and identity documents, preflight, both verification summaries, `summary.json`, `cases.csv` (6.3 MB, every channel and verdict per declared case), `case_aliases.json`, `cases_declared.json`, `constraint_catalog.json`, `manifest_used.json`, `integration_return_used.json` and `execution-context.json`.
