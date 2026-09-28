# Compatibility map — which alternatives can partner, and what sits between them

[AGENT] T-001 deliverable, read from the model files and completion bodies at entry HEAD `7cb0ae46` (paths in `choice-inventory.md` § 1; alternative ids from there). Nothing here was executed: this is a reading of interfaces (quantities, units, direction) and operating ranges (domain guards, temperature and pressure windows). Every classification names the line that decides it. The scratch screens of the next task test the input-expressible rows; the assembly rows are candidates for a later round.

## 1. The two heat-supply interfaces are different

- **The Brayton (A-V1) takes primary streams directly.** Each of its three exchanger stages reads (available heat MW, primary flow kg/s, primary cp J/kg/K, UA W/K, hot limit K) and the cycle helium state; the stage is a fluid-agnostic counterflow effectiveness–NTU exchanger and the turbine inlet is root-solved (`network_heat_driven_closure_impl.py:16-40`; bracket and bisection at `:85-97`). All three branches must carry positive flow, cp and limit, but UA and available heat may be zero, and a zero-UA branch transfers nothing (lines 31-40: coefficient 0 gives capability 0 and `state_defined` 0).
- **The steam cycle (S-V1) takes a salt loop.** It reads (heat available MW, salt flow × circuits, salt hot °C, salt return °C, salt cp) and requires the salt heat to equal the heat available within max(1e-8, 1e-12 × scale) (`matched_steam_cycle_impl.py:174-180`). It has no primary-side exchanger of its own: the helium→salt exchange lives in 'Cooling Equipment' inside 'Primary Heat Transport' (S-C1), whose body fixes the salt window at 465 → 270 °C and the salt temperature rise at 195 K and refuses a helium hot leg below 738.15 K (465 °C) or a suction below 543.15 K (`cooling_equipment_impl.py:72-73, 91`).
- **The lumped fit (S-V0) takes one hot temperature.** `T2 = T_hot − 20 − 273.15` must lie in [384, 642] °C, i.e. T_hot in [677.15, 935.15] K; outside, the value is published unclamped (`mfe_power_cycle.sysml:4-50`, T2_max at `stellarator_plant.sysml:831`) and the paired constraint `cycle_domain_ok : 'Cycle Fit Domain'` (`mfe_viability.sysml:520-533`, `domain_product_in >= 0`; asserted at `mfe_plant.sysml:898` on `turbine.domain_product`; present in the Stellaris pipeline as `stellarator_09__stellaris__cycle_domain_ok__…`) reads violated.

So a steam/Brayton substitution is not a drop-in at either plant: between an ARIES blanket and the steam cycle sits a missing intermediate loop and exchanger, and between the Stellaris loop and the Brayton sits only an input mapping. The rows below say which.

## 2. Pairings

Classification: **compatible** (interface matches and ranges overlap), **incompatible** (a range or interface fact rules it out as the definitions stand), **new behavior** (a needed relationship, exchanger, property law or interface does not exist, or a reviewed body would have to change). Route: **inputs** (expressible on a live package by entry keys alone), **assembly** (a new design instance from existing definitions), **none**.

### 2a. Heat supply × conversion

| # | supply | conversion | classification | route | what decides it |
|---|---|---|---|---|---|
| H1 | S-C1 Stellaris helium loop (T_out 773.15 K, mdot 3,010 kg/s, q_ihx 3,301 MW) | A-V1 Brayton | **compatible** | inputs (ARIES package: `heat_exchangers__he_flow` 3010, `he_limit` 773.15, `deposition` literal He 3301 in heat_mode 1 with PbLi and divertor literals 0, `pbli_hx`/`divertor_hx` `selected_area` 0 so their UA is 0; a re-chosen `cycle__selected_flow`) and assembly ('Primary Coolant Loop' or 'Primary Heat Transport' outputs bound to the He stage) | the He stage reads exactly the loop's outputs; the closure bracket [308.15, 773.15] K contains a root whenever the cycle capacity rate can carry the heat; the two idle branches keep positive dummy flow, cp and limit (a representation quirk, disclosed, no behavior change). Expected: turbine inlet below 773 K, low efficiency; whether the supplied ratings pass is the screen's business. MR-7: the loop's flow-from-duty direction is inherited and disclosed |
| H2 | A-C1-He ARIES blanket helium branch (limit 729.15 K = 456 °C, 940 MW literal) | S-V1 steam via S-C1's IHX | **incompatible (range)** | none as the bodies stand | `cooling_equipment_impl.py:72-73`: helium hot must exceed 738.15 K; 729.15 K gives a nonpositive hot approach and raises. The steam cycle's `salt_hot_C` entry key cannot repair it: lowering it alone breaks the `salt input heat join` because the IHX body still produces salt flow for a 195 K rise (`:91`, `:178-180`) |
| H2′ | A-C1-He | S-V1 steam with a *supplied* salt boundary (no exchanger represented) | **compatible at the steam interface; the He→salt exchanger is unrepresented** | assembly (bind heat_available, salt flow, salt hot ≤ 436 °C at a 20 K approach, salt return, cp as supplied values; steam ≤ ~416 °C; condenser 20–60 °C) | the steam body's domain admits steam down to saturation at 6.2 MPa (≈ 278 °C) and reports the pinch through `main_admission_ok`; executes and reports efficiency at the lower steam temperature; the missing exchanger is disclosed as a modeling gap, not credited |
| H3 | A-C1-div ARIES divertor helium circuit (limit 973.15 K = 700 °C, 374.75 MW literal) | S-V1 steam via S-C1's IHX | **compatible** | assembly (a second 'Primary Heat Transport' instance with q_source = divertor deposition, loop_T_in and loop_dT_blanket chosen so that hot > 465 °C and suction > 270 °C) | both IHX approaches positive; the loop hydraulics (n_loops, mdot_loop from duty and rise) are supplied choices; the steam cycle then runs on the salt at 465/270 °C exactly as in Stellaris. Only the divertor's 375 MW would reach the steam cycle |
| H4 | A-C1-PbLi (limit 1011.15 K, 1,555 MW) | S-V1 steam | **new behavior** | none | no PbLi→salt or PbLi→steam exchanger exists; 'Cooling Equipment' is helium-specific (helium properties, circulator law); the only PbLi-capable stage is the fluid-agnostic counterflow inside the Brayton closure, which cannot be instantiated apart from the Brayton solve |
| H5 | A-C1 full three-branch network | S-V1 steam | **new behavior** | none | H4, plus the steam cycle reads one salt hot/return pair and 'Cooling Equipment' one IHX duty: merging several primary loops into one salt loop (mixing or series on the salt side) has no definition ('Salt Branch Distributor' splits salt between main and reheat, it does not merge sources) |
| H6 | A-C1-He (456 °C) | S-V0 lumped fit | **compatible** | assembly (bind T_hot = branch hot limit or the closure's `he_hot`; heat = delivered) | T2 = 456 − 20 = 436 °C, inside [384, 642] |
| H7 | A-C1-div (700 °C) or A-C1-PbLi (738 °C) | S-V0 lumped fit | **incompatible (range)** | assembly executes but the domain constraint reads violated | T2 = 680 and 718 °C exceed T2_max 642 °C; published unclamped and `cycle_domain_ok` reads violated (`mfe_viability.sysml:520`, `mfe_plant.sysml:898`) |
| H8 | A-C1 full | S-V0 lumped fit | **new behavior (interpretation)** | none | the fit takes one hot temperature; applying it to three loops needs a combining rule (the lumped-heater reading the prior goal left as a hypothesis, L-010/L-013); a per-branch fit summed is a new relationship, not a definition |
| H9 | S-C1 Stellaris loop | S-V0 lumped fit | already used (Stellaris's own dormant/legacy mode) | inputs | not previously untested |
| H10 | A-C1 single-branch arrangement (two branches idle) | A-V1 | **compatible** | inputs (ARIES package) | a coolant *arrangement* neither plant uses: same closure, UA 0 on two stages; distinct from H1 only in which source values are supplied |

### 2b. Plasma / core source × downstream chain

| # | source | consumer | classification | route | what decides it |
|---|---|---|---|---|---|
| P1 | S-P1 Stellaris parabolic plasma (p_fus) | ARIES deposition → branches → Brayton → fuel → capacity screens | **compatible** | assembly ('Fusion Source Selector' `calculated_power_in` bound to a 'Plasma' instance's `p_fus`, mode 1; B supplied as a value) | 'Integrated Heat Source' and 'Fuel Cycle Flows' read fusion power in MW and nothing else from the core (`plant.sysml:20` is the assembly's only read of the plasma; `:45-59` and `:122-135`; `integrated_heat_source_impl.py:8`); the sustainment chain runs standalone inside 'Plasma' (`mfe_plasma.sysml:100-149`, only B is wired from outside). Range: the sustainment iteration must converge at the chosen (R, a, n_e0, T_i0, B), which is a test, not a reading |
| P2 | A-P1 ARIES hollow profile (fusion_power_MW) | Stellaris 'MFE Power Plant' | **incompatible (interface) → new behavior** | none | the plant consumes p_rad, p_aux_required, p_alpha_heat, n_T0, fuel_volume and alpha_n from the plasma besides p_fus (`mfe_plant.sysml:115-117, 155-159`; 21 grep lines across the two generic files); A-P1 publishes fusion power, pressure, mean density and stored energy only (`supplied_profile_plasma.sysml:45-52`). Supplying the five missing values as literals would change their role from calculated to chosen (an MR-7 role change, reserved) |
| P3 | A-P1 | Stellaris 'Blanket' ('Reactor Source Heat': q_source = mn·p_n + p_alpha + p_input) and 'Fuel Cycle' (p_fus) taken alone | **compatible** | assembly | both read p_fus in MW (`mfe_power_balance.sysml:188-193`; `mfe_plant_systems.sysml:717`) |
| P4 | A-P0 reference literal | any | already used | inputs | the supplied-source mode is ARIES's own |
| P5 | S-P1 at ARIES-like geometry and field (R 7.75, a 1.7, B 5.7 T, hollow amplitude as n_e0) | S downstream | **compatible interface; range unknown** | inputs (Stellaris package) | the sustainment guards are convergence guards, not a printed window; a scan says where it holds. Not a cross-combination of definitions, an operating-parameter cross-assignment |

### 2c. Equipment selection and checks

| # | pattern | applied to | classification | route | what decides it |
|---|---|---|---|---|---|
| E1 | A-E1 'Selected Inventory Purchase' (linear on selected quantity) | Stellaris equipment leaves (e.g. a selected circulator rating with a reference price) | **compatible** | assembly | the law reads (quantity, reference quantity, reference cost, price factor, mode) only; the Stellaris 'Cooling Equipment' exposes design points and masses that can serve as selected quantities |
| E2 | S-E1 'Cooling Equipment' (mass-based helium/salt equipment, IHX check, rated screens) | an ARIES helium circuit | **compatible only above the IHX window** | assembly (H3); **incompatible** for the blanket helium branch (H2) | same range fact as H2/H3; the body brings the loop hydraulics with it |
| E3 | 'Offered Capacity Screen' | both plants | already shared (32 + 12 instances; one copied body) | — | reuse in place, the existing evidence of a definition working with different partners |
| E4 | ARIES pump proxy ('Selected Flow Pump' mode 0 cubic on flow) | the Stellaris helium circulator | **compatible** | assembly | the proxy reads flow, reference flow/power/efficiency; Stellaris's own circulator law is inside 'Cooling Equipment'/'Primary Coolant Loop' (isentropic work from dp); two laws for one machine is a *modeling* choice, disclosed |

### 2d. Operating-parameter cross-assignments (inputs only, both packages)

| # | assignment | package | classification | note |
|---|---|---|---|---|
| O1 | ARIES Brayton at a Stellaris-like source (H1's input form) | ARIES | compatible | the screen of the next task |
| O2 | Stellaris steam at a lowered steam temperature (416 °C) with `salt_hot_C` lowered to 436 °C | Stellaris | **expected refusal** (`salt input heat join`) | demonstrates that the salt window is fixed in the IHX body (H2); run as a scratch case so the claim is executed, not asserted |
| O3 | ARIES recuperation and cycle flow at Stellaris-like values | ARIES | compatible | already covered by the prior goal's studies (L-002/L-005) |
| O4 | Stellaris loop rise and pressure at ARIES-like values (dT 156 K, 456 °C hot) | Stellaris | **expected refusal** (IHX hot approach) | the same fact as H2 seen from the Stellaris side |

## 3. Candidates for the next round's assemblies (previously untested, compatible, existing definitions)

- **C-1 (H1):** Stellaris helium loop → ARIES Brayton with the ARIES ratings and screens. Tests whether a lower-temperature single loop can be carried by the Brayton definitions at all and which rating binds.
- **C-2 (P1):** Stellaris parabolic plasma → ARIES deposition, branches, Brayton, fuel and capacity chain. Tests the brief's third question in its cross-plant form: the same downstream equipment under a different core.
- **C-3 (H3):** ARIES divertor helium circuit → Stellaris IHX and salt loop → matched steam cycle with the Stellaris steam ratings. The only ARIES stream the steam path can take as the bodies stand.
- **C-4 (H6):** ARIES blanket helium branch → lumped efficiency law. The cheapest conversion alternative and the one whose domain constraint speaks.
- **C-5 (E1):** the ARIES selected-purchase law on Stellaris cooling equipment, as a costing alternative under one assembly.

Failed or new-behavior set to characterize in the answer: H2 (range, fixed salt window), H4/H5 (PbLi and multi-source salt: missing exchanger and merge definitions), H7 (fit domain), H8 (combining rule), P2 (missing sustainment outputs).

## 4. What this map does not establish

That any assembly executes, or passes its screens; those are results. That the sustainment chain converges at cross-plant conditions (P1, P5). Whether the two idle branches in H1/H10 leave any residual in the ledger (the scratch screen reads the residual channels). The map reads the bodies as committed at `7cb0ae46`; a later body change voids the row that cites it.

## 5. Review corrections applied

[AGENT] Fresh review `map-review.md` (FINDINGS, no misclassified row): line cites corrected in § 1 and rows H7, P1, P2; the 'Cycle Fit Domain' mechanism, which the reviewer could not find in the files the brief named, is now cited to its actual definition, assertion and pipeline constraint; P2 strengthened with `alpha_n`. No classification changed.
