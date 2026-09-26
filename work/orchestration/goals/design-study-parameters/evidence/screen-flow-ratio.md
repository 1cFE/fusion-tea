# Scratch screen: cycle flow × stage pressure ratio on the C-1 assembly

[AGENT] T-001 of goal `design-study-parameters`, 2026-09-26. Diagnostic receipts on the existing WI-093 package `combinations_tea` (executable `78016859…`), C-1 assembly, every input at its design value except the cycle flow, the three stage ratios (moved together) and the five ratings, which are the re-selected set (3,200 / 7,000 / 3,600 / 5,000 / 3,500 MW) as case inputs. Source: `screen-flow-ratio.json` (produced by `screen-flow-ratio.py`; per-point receipts in the session scratchpad, not retained). Not a study: no manifest, no oracle, no record; the grid is coarse and engineered, and every number here is a native output of the package except the ARIES-inventory verdicts, which are computed from the stored demands against the ARIES ratings (1,600 / 3,500 / 1,800 / 2,500 / 1,500) and are labelled as such. MW; temperatures K.

## 1. Controls

The five WI-093 C-1 cases re-run first and reproduce every stored C-1 output of their sealed receipts exactly (`controls[*].reproduces_sealed_c1_outputs: true`). The package tree is git-clean after the run.

## 2. The map

Net electricity (MW) with the unmet heat (u, MW) beneath it; `*` marks a point at which every one of the eight checks is satisfied with the re-selected inventory. Flows in kg/s down, stage ratios across (each of the three stages at the ratio shown; the ARIES value is 1.5183).

| flow \ ratio | 1.20 | 1.30 | 1.35 | 1.40 | 1.45 | 1.5183 | 1.60 | 1.70 | 1.80 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1,500 | 151.3 (u 1,814) | 281.6 (u 1,502) | 326.5 (u 1,365) | 360.1 (u 1,240) | 384.0 (u 1,126) | 402.9 (u 983) | 408.0 (u 831) | 392.9 (u 668) | 359.1 (u 526) |
| 2,000 | 261.9 (u 1,359) | 421.7 (u 959) | 474.3 (u 785) | 512.0 (u 626) | 536.8 (u 480) | 552.6 (u 300) | 548.5 (u 108) | **441.6\*** | **333.5\*** |
| 2,500 | 349.4 (u 951) | 522.7 (u 481) | 575.2 (u 278) | 609.2 (u 94) | **575.6\*** | **426.6\*** | **230.1\*** | **150.5\*** | 103.1 (compressor) |
| 3,000 | 414.1 (u 589) | 586.5 (u 65) | **531.0\*** | **414.6\*** | **282.6\*** | **84.8\*** | 12.2 (compressor) | −48.8 | −127.2 |
| 3,500 | 459.0 (u 266) | **440.6\*** | **310.1\*** | **157.6\*** | −10.5 | −98.2 | −156.6 | −248.8 | −366.2 |
| 4,000 | **476.3\*** | **255.7\*** | **89.2\*** | −99.5 | −187.4 | −242.6 | −331.7 | −462.9 | refused |

The one refusal (4,000 kg/s at 1.80) is the Brayton body's own guard, `cooler outlet must not exceed inlet` (the recuperator's hot side would leave colder than the precooler target). Nonpositive net points executed here because C-1 has no lifecycle part; on a costed package the lifecycle body refuses an LCOE for nonpositive net (`LCOE undefined for nonpositive net electricity`), so those points will be refusals of the whole evaluation, not stored points with a violated check.

## 3. What binds where

- **Low ratio, any flow: heat removal.** Below a flow-dependent ratio the cycle cannot take all 3,301.2 MW: a lower ratio leaves the turbine exhaust hotter, the recuperator raises the heater inlet (423 K at the design point, 481 K at 2,500 / 1.40, 559 K at 2,500 / 1.20), and the exchanger's capability against the 773 K source falls below the delivered heat (`he_capability` 3,836 → 3,207 → 2,350 MW at 2,500 kg/s). At 1,500 kg/s no ratio in 1.20–1.80 removes all the heat (983 MW unmet at the ARIES ratio); the cycle stream is too small to carry it.
- **High ratio at 3,000 kg/s and above: net power.** More flow at a given ratio lowers the turbine inlet (the same heat over more helium: 677.5 K at 2,500 / 1.518, 590.1 at 3,000, 552.7 at 3,500) while the compressors, whose work is proportional to flow, keep their cost; net turns negative at 3,000 / 1.70, 3,500 / 1.45 and 4,000 / 1.40. The recuperator bypass engages (`bypass_active` 1) wherever the turbine exhaust is colder than the compressor outlet (2,000 / 1.80; 2,500 / 1.70 and above; 3,000 / 1.60 and above), the regime in which recuperation has nothing to recover.
- **High ratio with the re-selected inventory: the 3,200 MW compressor** at 2,500 / 1.80 (3,574 MW demand), 3,000 / 1.60 (3,347) and every point beyond; the turbine (7,000), generator (3,600), rejection (5,000; rejected heat 1,430–3,513 across the map) and helium duty (3,500 against a constant 3,301.2) ratings never bind.
- **The ARIES-selected inventory admits no passing point anywhere on the map.** Its 1,500 MW helium duty package is below the loop's constant 3,301.2 MW delivered heat at every point, and its 1,600 MW compressor is exceeded at every point that removes all the heat (the smallest passing compressor demand is 1,632 MW at 4,000 / 1.20; the next 2,064 at 3,000 / 1.35); its 2,500 MW rejection package is exceeded at most of them. So the re-selection WI-093 made is not optional for this loop: it is the separate hardware selection the brief asks to declare and price before the main sweep, and the ARIES-rated set is a bounded negative for this heat source.

## 4. The all-checks window and the ridge

With the re-selected inventory the passing region is a band from (2,000 kg/s, ratio ≥ 1.70) through (2,500, 1.45–1.70), (3,000, 1.35–1.518), (3,500, 1.30–1.40) to (4,000, 1.20–1.35): its lower edge is the heat-removal boundary, its upper edge the net-positive boundary at 3,000 kg/s and above and the compressor rating at 2,500 and 3,000. Along the lower edge, the best passing point at each flow is 2,000 / 1.70 (441.6), **2,500 / 1.45 (575.6)**, 3,000 / 1.35 (531.0), 3,500 / 1.30 (440.6), 4,000 / 1.20 (476.3). The coarse-grid best passing point is 2,500 kg/s at ratio 1.45, 575.6 MW net, 149 MW (35 %) above the starting point's 426.6, with 0 unmet, compressor demand 2,161 on 3,200, rejected 2,469 on 5,000. The electricity-only best on the grid is one ratio step lower, 2,500 / 1.40 at 609.2 MW with 93.8 MW unremoved, and 3,000 / 1.30 at 586.5 with 65.0 unremoved: the ridge of net runs along and just inside the failing side of the heat-removal boundary, so the true best passing point is a constrained optimum on that boundary between grid cells (between 1.40 and 1.45 at 2,500 kg/s, between 1.30 and 1.35 at 3,000), and no grid will report it as a global optimum. The response is not flat: net moves by 100–200 MW across one ratio step near the boundary.

## 5. What this fixes for the contract and the study

- The study window is engineered from this scan: flow 2,000–4,000 kg/s and stage ratio 1.20–1.80, with the grid refined toward the heat-removal boundary (steps of 0.025 in ratio between 1.30 and 1.50 at 2,250–3,250 kg/s), and the nonpositive-net corner excluded by an oracle scan before execution because the costed package refuses it.
- The inventory for the main sweep is the re-selected set, priced through the ARIES purchase law; the ARIES-selected set is recorded as the alternative that admits no passing point and is priced for the record; a third inventory is not needed by this screen (no rating other than the compressor binds inside the window; the compressor at 3,200 MW binds only above the net-positive edge at 3,000 kg/s and at 2,500 / 1.80, where net is already 103 MW).
- The fixed-efficiency question: the passing band spans stage ratios 1.20–1.70 and flows 2,000–4,000 kg/s at the ARIES machines' fixed 0.89 / 0.93 efficiencies; the flow range is ±60 % about the design point, which is outside what a fixed-efficiency approximation of one machine can be presumed to cover. The contract states this as the model assumption the study's sensitivities test (efficiency offsets), with an off-design map named as the missing model.
- The recuperator bypass regime (high ratio) is part of the map and is reported, not filtered.
