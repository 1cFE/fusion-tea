# Scratch screens — the input-expressible map rows, executed (T-002)

[AGENT] Receipt `scratch-screens.json`, produced by `scratch-screens.py` through each package's stock strict loader and evaluator (no store, no record, no package write). ARIES executable `f739dbce…`, Stellaris executable `83ea3b6c…`, both equal to the pinned identities in `goal.md`. Every number below is copied from the receipt. These are diagnostic screens: none is a design, and a refusal is a result.

## 1. ARIES package — a Stellaris-like single helium loop as the Brayton's only heat source (map H1, H10, O1)

Base: the sealed `nominal-calculated` input map (replayed first as the control: net 423.107 MW, 14 of 14 checks satisfied, no-credit LCOE 1119.408, identical to the sealed store). The Stellaris-like supply sets the source to the Stellaris fusion power (2,652.563 MW, supplied mode), partitions all blanket heat to the helium branch with a neutron multiplier chosen so the helium deposition equals the Stellaris loop duty (3,301.208 MW; source residual 0), gives the helium stage the Stellaris flow (3,009.756 kg/s), cp and hot limit (773.15 K), and sets the PbLi and divertor exchanger areas to zero (UA 0) so those stages transfer nothing. Delivered helium heat is 3,412.065 MW (deposition plus the recovered pump friction the ARIES branch model adds). All ARIES ratings, areas and the 1,600 MW compressor stay as selected; cycle flow and recuperation are the varied choices.

| case | cycle flow kg/s | recuperation | state | turbine inlet K | heater inlet K | accepted MW | unmet MW | net MW | efficiency | violated checks |
|---|---|---|---|---|---|---|---|---|---|---|
| control (ARIES nominal-calculated) | 1400 | 0.8 | completed | 788.638 | 480.477 | 2240.389 | 0.0 | 423.107 | 0.293 | none (14 satisfied) |
| flow1400-rec0.8 | 1400 | 0.8 | completed | 769.010 | 470.366 | 2171.201 | 1249.864 | 446.111 | 0.279 | `he_capacity` (delivered 3412 against the 1500 MW rating, margin −1912), `heat_removal_ok` |
| flow1400-rec0.5 | 1400 | 0.5 | completed | 768.499 | 432.974 | 2439.328 | 981.737 | 444.814 | 0.248 | same two |
| flow1400-rec0.2 | 1400 | 0.2 | completed | 767.990 | 395.781 | 2706.036 | 715.029 | 443.524 | 0.223 | same two |
| flow2500-rec0.8 | 2500 | 0.8 | completed | 695.126 | 432.305 | 3412.065 | 9.0 | 587.191 | 0.219 | `he_capacity`, `heat_removal_ok` (9 MW), `compressor_capacity` (demand 2451.520 on 1600), `rejection_capacity` |
| flow2500-rec0.5 | 2500 | 0.5 | completed | 661.272 | 398.451 | 3412.065 | 9.0 | 433.823 | 0.174 | same four |
| flow2500-rec0.2 | 2500 | 0.2 | completed | 642.431 | 379.611 | 3412.065 | 9.0 | 348.468 | 0.149 | same four |
| flow4000 (three recuperations), flow6000 (three), flow6000-area150k, flow6000-comp3200 | 4000–6000 | 0.2–0.8 | refused | — | — | — | — | ≤ 0 | — | `LCOE undefined for nonpositive net electricity` (the lifecycle body refuses; the thermal chain evaluated) |
| flow8000 (three recuperations) | 8000 | 0.2–0.8 | refused | — | — | — | — | — | — | `cooler outlet must not exceed inlet` (an intercooler domain guard) |

Reading (goal level, for the map and the next round):

- **The combination executes without new behavior.** The Brayton definitions carry a single 773 K helium loop with two idle stages; the plant ledger closes (residual 0) and the screens report what they should: the helium duty package rating (1,500 MW, an ARIES selection) is exceeded by a 3,412 MW branch, and the unremoved heat is a failed check, never hidden.
- **The heat-acceptance edge is the interaction the brief asks about (B1), seen on a live package.** At 1,400 kg/s the stage accepts more heat as recuperation falls (2,171 → 2,706 MW from 0.8 → 0.2) because the heater inlet drops (470 → 396 K) below the 773 K source; net electricity barely moves (446 → 444 MW) because the efficiency falls as fast as the accepted heat rises. At 2,500 kg/s all heat is removed at every recuperation, but the turbine inlet falls with recuperation (695 → 642 K) and net falls 587 → 348 MW: the ranking of recuperation values is flat at the low flow and strongly positive at the high flow. This is a screen, not the study; the committed study quantifies it with the source temperature as a factor.
- **Where the combination stops:** at 4,000 kg/s and above the compressors (three stages at the ARIES ratios) consume more shaft work than the low-temperature expansion produces, net is nonpositive, and the lifecycle body refuses an LCOE; at 8,000 kg/s an intercooler guard refuses. Neither is a bug: a 500 °C source cannot drive a cycle designed for a 700 °C one at the ARIES pressure ratios, and re-selecting the compressor ratios is a design choice this screen did not make (the doubled-ratings case fails the same way, confirming the limit is thermodynamic, not a rating).
- **What it costs:** the fuel demand follows the supplied 2,652 MW fusion power (external tritium 151.014 against the control's 104.668 kg/year); the helium pump proxy responds to the Stellaris flow (122.650 MW at 3,010 kg/s against 156.0 at 3,261). No-credit LCOE 1,477–1,890 USD2004/MWh on the completed cases: the economics are tritium-dominated exactly as the prior goal's L-001 says, so no cost ranking is read here.

## 2. Stellaris package — salt boundary, steam temperature, loop rise (map O2, O4)

Base: package defaults (control: p_net 850.065 MW, gross 1,219.998, eta_gross 0.3689, LCOE 318.738; T_out 773.15 K; IHX approaches 35.0 / 18.785 K; 61 satisfied, 6 violated — the baseline's own six: facility occupancy, divertor heat, water electric capacity, TBR, reference conductor current, winding-pack fit).

| case | override | state | result |
|---|---|---|---|
| salt-hot-436 | `heat_transport__salt_hot_C` 436 | refused | `WI-073 salt input heat join: balance residual 490.950 exceeds arithmetic policy` — the IHX body still produces the salt flow for a 195 K rise, so the salt heat no longer equals the heat available (map row H2/O2 confirmed) |
| salt-hot-436-steam-416 | as above plus steam and reheat 416 °C | refused | same message; the join is checked before the steam side (O2 confirmed) |
| steam-416 | steam and reheat 416 °C, salt unchanged | completed | executes: eta_gross 0.3625 (from 0.3689), gross 1,198.750, p_net 829.041, LCOE 326.821; pinch gaps 30.9 / 49.0 K (from 20 / 20); but 15 additional checks flip to violated — every steam-side and cooling-water capacity screen, because 'Steam Offered Conditions' declares the rated equipment at 445 °C and marks the lowered actual conditions unsupported. The steam definitions accept the lower temperature; the *selected equipment* does not |
| loop-rise-156 | `loop_dT_blanket` 156 (hot leg 729.15 K = 456 °C) | refused | `nonpositive IHX terminal approach` — the IHX body's fixed 465 °C salt hot leg (map row H2/O4 confirmed) |
| loop-inlet-530 | `loop_T_in` 530 K | refused | `nonpositive IHX terminal approach` at the cold end (the fixed 270 °C salt return) |

Reading: the map's steam-side claims are executed facts. The Stellaris salt window is a constant inside a reviewed body, not a choice the package exposes; feeding an ARIES helium branch (456 °C) to this steam path is out of range as the bodies stand, and lowering the steam temperature alone is admissible thermodynamically but trips fifteen equipment-condition screens, which is an equipment-selection interaction of its own: a conversion-system operating change invalidates the declared conditions of the selected turbine, pumps and condenser.

## 3. What these screens do not establish

They are single evaluations, not studies; nothing is verified against an oracle; no combination is a design; no assembly was built. The 9.0 MW unremoved heat at 2,500 kg/s is read from `unmet_heat` and not decomposed. The refusal messages are the bodies' own.
