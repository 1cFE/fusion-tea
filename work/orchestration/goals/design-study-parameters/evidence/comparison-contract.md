# Comparison contract: cycle flow and stage pressure ratio on the costed C-1 assembly

[AGENT] T-002 of goal `design-study-parameters`, 2026-09-26, written before any dependent work. Authority: the owner brief (`owner-brief.md` § Common execution and comparison requirements, item 2) and `goal.md` § Invariants. Numbers cited from `starting-configuration.md`, `screen-flow-ratio.md`, the sealed ARIES economics record (`exploration/aries_integrated/studies/20260925-aries-reconciled-alternative-economics/results/cases.json`, case `baseline-no-credit`, executable `f739dbce…`) and the ARIES assembly (`models/designs/aries_cs_integrated/plant.sysml`). USD2004; MW; K. Version 2: the fresh review's findings applied (`contract-review.md`, FINDINGS: one correct-before-execution on the fuel-variable term, four notes); the version-1 text is retained in the review's citations.

## 1. The question the comparison answers

For the C-1 assembly with one fixed, priced equipment inventory, which cycle mass flow and stage pressure ratio give the highest net electricity and the lowest conditional LCOE among the operating points that satisfy every evaluated check, and which check stops further improvement on each side of that region. The comparison is between operating points of one plant; a second inventory is compared only with both inventories' costs carried.

## 2. Independent choices (the swept axes)

| Axis | Entry keys (package prefix elided) | Role (MR-7) | Window | Provenance |
|---|---|---|---|---|
| Cycle mass flow, kg/s | `cycle__selected_flow` | chosen | 2,000–4,000 | engineered from the screen (§ 11) |
| Stage pressure ratio | `compressor_1__selected_ratio`, `compressor_2__selected_ratio`, `compressor_3__selected_ratio`, moved together | chosen | 1.20–1.80 | engineered from the screen |

The three stage ratios are three independent chosen inputs. Moving them together is a declared scenario (the ARIES designer's equal-stage choice, `plant.sysml:152-234`), not a physical tie, and the record says so; unequal stage ratios are outside this contract. Both axes are inputs no calculation in the package produces (STUDY_POLICY § 2.1). Nothing else is swept in the main study.

## 3. Quantities held equal

| Held equal | Value | Basis |
|---|---|---|
| Supplied blanket heat; the fusion power behind it | 3,125.9323 MW; 2,652.563 MW | `[INHERITED: Stellaris baseline]` |
| Loop inlet, rise, pressure, loop count, rated flow, pump-law constants | 573.15 K, 200 K, 8 MPa, 14, 225.0778 kg/s, dp_ref 329,187.19 Pa, f_loss 1, eta_is 0.7728, eta_drive 1 | `[INHERITED: Stellaris]` |
| Cycle low temperature, return pressure, cp, gamma | 308.15 K, 4.2857 MPa, 5,193 J/kgK, 5/3 | `[INHERITED: ARIES]` |
| Compressor efficiency, turbine efficiency, pressure loss, recuperation | 0.89, 0.93, 0.045, 0.8 | `[INHERITED: ARIES]`; fixed numbers with no map (§ 8, S1) |
| Intercooler and precooler targets | 308.15 K | `[INHERITED: ARIES]` |
| Exchanger area and U | 50,000 m², 1,000 W/m²K (UA 50 MW/K) | `[INHERITED: ARIES]`; equipment, priced (§ 5) |
| Auxiliary register | heating 20 MW at 0.5; cryo 10; fuel base 5; control 5; other 5; generator 0.98; motor 0.95; the balance's exhaust-driven fuel term held at 0 as in C-1 (the fuel chain's exhaust rate is computed for the fuel cost but not wired into the balance, so the C-1 controls replay bit-exactly; the term's value, 1e-22 × the exhaust rate ≈ 1.8 MW, is a disclosed constant omission and is run as an S2 case) | `[INHERITED: ARIES A-register]`; constants of the sweep (S2) |
| Equipment inventory and its prices | inventory I-R (§ 5) | declared |
| Rest-of-plant capital | 2,158,230,133.33 USD2004 | derived § 6; `[ASSUMED: held equal]` (S4) |
| Fuel term | calculated from the fixed 2,652.563 MW by the existing fuel chain; no-credit convention; 30 MUSD/kg; 10 kg stock; 1,000 s residence; 0.05 burn fraction; 0.99 exhaust recovery | `[INHERITED: ARIES E6 conventions]`; constant of the sweep (S5) |
| Replacement scope | 72,231,350 USD2004 per event at 5 full-power years, event factor 1 | `[ASSUMED: the ARIES nominal scope, held equal]` |
| O&M; consumables; import price | 70 MUSD/year; 5 MUSD/year; 50 USD/MWh (import channel; zero at every passing point) | `[INHERITED: ARIES E7, E10]` |
| Finance | 5 % real; 6 construction years, one midpoint adjustment; 40 calendar years; availability 0.85; indirect 20 %; contingency 20 % of direct + indirect; owner 5 %; terminal 10 %; salvage 2 %; overhaul 5 % at year 20; supply service 0 | `[INHERITED: ARIES F1–F9]` |
| Energy tolerance | 1e-6 MW | `[ASSUMED]` (WI-093) |

## 4. Calculated consequences (read per point)

Turbine inlet and heater inlet temperatures; accepted and unmet heat; exchanger capability and the helium hot-bound margin; compressor work (three stages), turbine work, net shaft, gross, auxiliaries, net electricity; rejected heat; recuperator bypass state; the five rating margins and the loop margin; annual net energy (8,760 × net × 0.85); the purchases (constants within an inventory), direct, overnight and financed capital; the LCOE and its eleven contributions (capital, O&M, tritium, deuterium, consumables, imports, supply service, replacement, overhaul, terminal, salvage); the eight check verdicts. The delta against the starting point (case `c1-aries-ratios-reselected-ratings`: 2,500 kg/s, 1.5183, net 426.579) is presentation arithmetic on stored channels: Δnet, ΔLCOE and the per-contribution ΔLCOE, of which, within one inventory, every term is the denominator effect of Δnet (every numerator term is a constant of the sweep). "Plant-side" LCOE (the sum of the contributions other than tritium, deuterium and supply service) is reported beside the fuel-inclusive figure so the fuel convention's weight is visible.

## 5. Permitted equipment reselections

Two inventories, both declared here and priced through the existing linear purchase law from the ARIES reference points (WI-090 E4: capital = reference cost × price factor × selected / reference; extrapolation flagged outside 0.5–1.5 of the reference), plus the fixed conversion-services budget (62,911,600) and the exchanger (50,000 m², 58,325,700):

| Item (reference rating, reference cost) | I-R, the re-selected inventory (main sweep) | I-A, the ARIES-selected inventory (recorded alternative) |
|---|---|---|
| Compressor (1,600 MW shaft, 78,639,500) | 3,200 MW → 157,279,000 (extrapolated flag: ratio 2.0) | 1,600 MW → 78,639,500 |
| Turbine (3,500 MW shaft, 125,823,200) | 7,000 MW → 251,646,400 (extrapolated) | 3,500 → 125,823,200 |
| Generator (1,800 MW electric, 47,183,700) | 3,600 MW → 94,367,400 (extrapolated) | 1,800 → 47,183,700 |
| Heat rejection (2,500 MW thermal, 56,086,000) | 5,000 MW → 112,172,000 (extrapolated) | 2,500 → 56,086,000 |
| Helium duty package (1,500 MW thermal, 32,403,166.67) | 3,500 MW → 75,607,388.89 (extrapolated) | 1,500 → 32,403,166.67 |
| Exchanger (50,000 m², 58,325,700) | 50,000 m² → 58,325,700 | same |
| Conversion services (fixed) | 62,911,600 | same |
| Priced total | 812,309,488.89 | 461,372,866.67 |

I-R is the set WI-093 selected as case inputs; all five of its ratings are beyond 1.5× their reference (four at 2.0, the helium duty package at 2.33), so the law flags every one extrapolated and the answer reports that flag on every I-R price. The screen (`screen-flow-ratio.md` § 3) shows I-A admits no point in the window that removes all the heat, so I-A is priced for the record and its cases are reported as failed selections, never re-sized. No other reselection occurs in the main study; no rating is computed from a demand; a case that exceeds a rating stays a failed case with its booked price. One optional priced hardware alternative is declared for the sensitivities (S6): a 75,000 m² exchanger (ratio 1.5, price 87,488,550, not extrapolated), run only as a labelled alternative inventory, never as a point-by-point resize.

## 6. Accounting boundary

**Energy** (from `starting-configuration.md` § 4): net = 0.98 × max(turbine work − Σ compressor work, 0) − import − (loop pumps 175.281 + heating 40 + cryo 10 + fuel 5 + fuel-variable + control 5 + other 5); the balance's exhaust-driven fuel term stays 0 as in C-1 so the controls replay bit-exactly (its value with the assembled fuel chain, 1e-22 × the exhaust rate ≈ 1.8 MW, a constant, is a disclosed omission run as an S2 case); loop friction heat (175.281) enters the cycle through the delivered heat once. Omitted and disclosed: heat-rejection pumping (order 12–16 MW, varying by a few MW across the sweep; bounded in S2), the blanket return-temperature seam, magnet and plasma loads beyond the register. No import case exists at a passing point.

**Cost.** Direct capital = rest-of-plant + the priced items of the inventory + the initial tritium stock (10 kg × 30 MUSD = 300 MUSD). The rest-of-plant constant is the ARIES direct source scope at the sealed 423 MW baseline (`direct_source_scope__evaluate__total` 2,619,603,000) less the seven items this assembly prices at their ARIES reference values (461,372,866.67): 2,158,230,133.33 USD2004. It is held equal across every point and both inventories, labelled `[ASSUMED]`, and its meaning is stated plainly: an ARIES-scope reactor, buildings, electrical and heat-transport plant standing in for the unpriced Stellaris side of this assembly (whose own equipment, the 28 circulators included (`baseline.json` `heat_transport__equipment__circulator_count`), is costed in the Stellaris package in a different currency year and is not mixed in); it still carries ARIES items with no function in this assembly (the PbLi and divertor exchangers, duty packages and three pumps, about 240 MUSD, and the 151 MUSD LiPb inventory), which is ranking-neutral and part of why the absolute figure is conditional; it sets the absolute LCOE and the weight of the denominator effect, not the operating ranking (S4 tests ×0.5 and ×2). Overnight = direct × (1 + 0.20) × (1 + 0.20) + 0.05 × direct, as the ARIES chain computes it; financed once at the six-year midpoint at 5 % real. Annual operating = O&M 70 + tritium (calculated: burn + loss + decay − feed, purchased at 30 MUSD/kg; no-credit feed 0) + deuterium (calculated) + consumables 5 + imports (0). Replacements: 72,231,350 per event, 6 events over 40 years at 0.85 availability and 5 fpy. Terminal 10 % gross, salvage 2 %, overhaul 5 % at year 20. LCOE = present value of all costs ÷ present value of annual net energy, from 'Lifecycle Cashflow Accounts' with its eleven contributions summing to the total. Currency: constant USD2004 throughout; no year conversion. Nothing is counted twice: the priced items are removed from the rest-of-plant before it is added back; the fuel stock is capital and the annual makeup is operating; the loop pump electricity is subtracted once in the balance and its friction heat delivered once.

**The primary metrics.** (i) Net electricity among all-checks-satisfied points, and the check that bounds the passing region on each side. (ii) ΔLCOE against the starting point at held-equal fuel under the no-credit convention, with the plant-side ΔLCOE and the tritium ΔLCOE shown separately (within one inventory both are denominator effects of Δnet, since no numerator term varies with flow or ratio, the reviewer confirming this from the ledger and lifecycle bodies; between inventories the capital difference enters). Absolute LCOE is reported as conditional on the rest-of-plant constant and the fuel convention, and the feed100 scenario (S5) shows how far the fuel convention moves it without changing the operating ranking.

## 7. Failure conditions

| Condition | How it is read | Treatment |
|---|---|---|
| Unmet heat > 1e-6 MW | `checks__heat_removal_ok` violated | failed: retained, plotted and marked; never a winner; its net and LCOE reported with the flag "not steady" |
| Any rating margin < 0 (I-R or I-A) | the `*_capacity__capacity_ok` verdicts | failed selection: retained and marked; the booked price is the selected rating's |
| Loop flow above its rated ceiling | `checks__loop_capacity_ok` | constant of the sweep (margin 10.10 kg/s at every point); reported |
| Net ≤ 0 | the lifecycle body refuses (`LCOE undefined for nonpositive net electricity`) | a refusal of the whole evaluation: excluded from the executed grid by the oracle scan, reported as the scanned net-positive edge with the oracle's net values, never a stored point |
| Recuperator hot side colder than the precooler target | the Brayton body refuses (`cooler outlet must not exceed inlet`) | as above (seen at 4,000 kg/s / 1.80) |
| Recuperator bypass engaged | `recuperator__evaluate__bypass_active` = 1 | not a failure; reported as the regime where recuperation recovers nothing |

A point is a candidate for "best" only when all eight checks are satisfied on its inventory. The best tested point is reported as the best sampled point on the grid, with the boundary located to the grid's resolution; no interpolated optimum is claimed.

## 8. Scientific support and applicability

Unsupported by declaration, carried into every reading: (a) the compressors and turbine keep fixed isentropic efficiencies (0.89, 0.93) at every flow and ratio; no off-design map exists in the library, so the passing band's span (flow −20 % to +60 % about the 2,500 kg/s design point, ratio 1.20–1.80) exceeds what a fixed efficiency of one machine can be presumed to cover; the study tests the effect of uniform efficiency offsets (S1), which cannot test a penalty that grows with distance from the design point, and names the off-design map as the missing model; the answer states the operating comparison as "at fixed machine efficiencies", treats the best passing point near the design flow (2,500 kg/s, a ratio within 5 % of the design 1.518) as the operating claim, and reports rankings between flows far from 2,500 kg/s (for example 4,000 / 1.20 against 2,000 / 1.70) as model exploration at fixed efficiency, not an operating claim; (b) the recuperator has no purchase, rating or screen (economics goal L-003) and its effectiveness is not a lever here; (c) heat-rejection pumping is not in the balance; (d) the loop returns helium colder than the Stellaris blanket inlet (513 K against 573 K at the design point; the value moves with the sweep) and no blanket-inlet requirement is checked: a real loop would bypass or change its rise, which changes no cycle result but is a limit of the comparison; (e) the rest-of-plant is an ARIES-scope constant; (f) fuel breeding is unsupported (no-credit convention; the feed100 scenario is an assumption); (g) the loop's pump law is the Stellaris relation with its constants, not a hydraulic model (S3). The comparison is between engineering-check outcomes of one model; passing every check does not qualify a design.

## 9. Materiality and tolerances

- Replay: the starting point and the four other C-1 cases replay bit-exactly on the costed package for every C-1 channel they share (the pre-change control); a difference is a changed-behavior finding, never absorbed.
- Verification (runbook step 10): every stored point against the package-owned oracle at relative deviation < 1e-9, or an absolute class declared in the new package's manifest before execution: the closure residual 1e-7 MW (the ARIES class, same body); the lifecycle `idc` 2 ULP of the capital magnitude (the ARIES class, same body); the four kg/year fuel classes at 1e-9 (the ARIES classes, same bodies). No class is added or relaxed after a result is seen; a refusal outside them is an owner gate.
- Materiality for the reading: a net difference below 5 MW (1.2 % of the starting net) and a ΔLCOE below 1 % of the base are immaterial and are not used to rank; the heat-removal boundary is located to the refined grid's resolution (0.025 in ratio, 250 kg/s in flow) and reported as a band, not a line.
- Every point's identity: `<study-id>:<candidate>`; every plotted point carries its case name and its verdict set.

## 10. Declared sensitivities

Run at the matched pair (the starting point and the best passing I-R point of the main grid) and at that point's two boundary neighbours (one ratio step lower, one flow step higher), so each shows whether the best passing point moves and by how much; each holds every other quantity of § 3 equal and states the fuel term's share separately.

| Id | Assumption | Levels | What it tests |
|---|---|---|---|
| S1 | Machine efficiency (fixed-efficiency treatment) | compressor 0.85 / 0.89 / 0.92; turbine 0.90 / 0.93 / 0.95 (WI-090 ranges) | whether the location of the best passing point and the boundary depend on the assumed efficiencies; the missing map's first-order effect |
| S2 | Auxiliaries | register ×0.5 / ×1 / ×1.5; the balance's exhaust-driven fuel term set by input override (`electrical.fuel_exhaust`) to the assembled fuel chain's stored exhaust rate (≈ 1.8 MW; the reviewer's note: an override, so the main package needs no rewired variant); plus a labelled Stellaris-equivalent register (heating 100 MW wall-plug, cryo 2.14, cooling-water pumping 13.02 in place of the ARIES 60 MW) | that a constant auxiliary shifts absolute net and LCOE and the net-positive edge, not the ranking; the rejection-pumping omission bounded |
| S3 | Pumping law | loop `dp_loop_ref` ×0.5 / ×1 / ×2 (the pump-power constant; it moves both the pump electricity and the friction heat delivered) | whether the boundary and the best point move with the loop's pumping assumption |
| S4 | Equipment prices and the rest-of-plant | price factor ×0.5 / ×1.5 on the I-R purchases (E4); rest-of-plant ×0.5 / ×2 | the USD/MWh value of a net gain and the I-R against I-A comparison, not the operating ranking |
| S5 | Fuel convention | no-credit (base) / feed100 with 30 MUSD/year service | that the fuel term is a held-equal denominator effect that cannot reorder operating points, and how far it moves absolute LCOE |
| S6 (optional) | Exchanger area as a priced hardware alternative | 75,000 m² at 87,488,550 | whether a bigger exchanger moves the heat-removal boundary to a lower ratio and pays for itself; run only if the round's budget allows, reported as a separate inventory |

## 11. Study window and grid (engineered from the screen)

Flow {2,000, 2,250, 2,500, 2,750, 3,000, 3,250, 3,500, 4,000} × ratio {1.20, 1.25, 1.30, 1.325, 1.35, 1.375, 1.40, 1.425, 1.45, 1.475, 1.50, 1.5183, 1.55, 1.60, 1.70, 1.80}, minus the points the oracle scan refuses (nonpositive net or the Brayton guard), which are reported from the scan as the edge. The refinement (0.025 steps between 1.30 and 1.50) follows the heat-removal boundary found by the screen; it is engineered, not sourced. I-A is evaluated at the same points as a second block. The sensitivities of § 10 are a third block. Window provenance and the scan are recorded in the study record § 11 (runbook step 7).

## 12. What would change the conclusion

The fresh review finding the fixed-efficiency treatment indefensible over the window (then the study's operating claim narrows to the ratio range near the design point, or the round closes on a strategy blocker); a premise conflict on the fuel or rest-of-plant constant (owner gate); the costed assembly failing to replay the C-1 controls (changed behavior, surfaced); a verifier refusal outside the declared classes (owner gate).

## 13. Questions for the fresh review

1. Is any held-equal quantity in § 3 actually moved by the swept axes through a path the contract misses, or any calculated consequence in § 4 actually a hidden choice (MR-7)? Entry: `models/designs/combinations/combinations_loop_brayton.sysml`, the 'Plant Electrical Balance' and 'Network Heat Driven Closure' bodies, `starting-configuration.md` § 4.
2. Is the cost boundary in § 6 single-counted and complete for the comparison it claims (the rest-of-plant derivation; the fuel stock as capital and makeup as operating; the loop friction once)? Entry: `plant.sysml` lines 1595–2231 (fuel inventory, direct/indirect/contingency/owner, ledger, lifecycle), the `equipment_cost_ledger_impl.py` and `lifecycle_cashflow_accounts_impl.py` bodies, the sealed channels named in § 6.
3. Is "ΔLCOE within one inventory is a pure denominator effect of Δnet" correct given the chain (imports are zero at passing points; the fuel-variable electric term is constant)? Entry: the same bodies.
4. Is the fixed-efficiency treatment across the window a defensible operating approximation to state and test, or must the claim be narrowed before execution? Entry: § 8 (a), `ideal_gas_brayton_components.sysml` and its compressor/expander bodies, `screen-flow-ratio.md` § 5.
5. Do the two inventories and the I-A "no passing point" reading follow from the screen's demands and the ratings (§ 5, `screen-flow-ratio.json`)?
