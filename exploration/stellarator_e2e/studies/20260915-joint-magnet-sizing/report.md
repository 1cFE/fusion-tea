# Current-driven magnet sizing: bounded study report

**No default-performance design in the investigated sample passes all twenty predicates.** All 324 default cases pass current capacity; 154 also pass pack fit, but none passes the other eighteen constraints together. This is a useful bounded negative result: supplying sufficient conductor inventory removes the old current shortfall and exposes the remaining plant-level conflicts. It does not establish global infeasibility. The full study contains 347 unique native cases and 351 report rows. The only all-twenty pass belongs to a historical 30 T, orientation-factor-three control, outside the default comparison. [Results](results/analysis.json), [selection](preparation/final-selection.json).

These numbers require the sealed executable fingerprint `8e4aa8eaebf2667a74565e6e66fc9ce5947c6d27ccfc210f8452e82d87fba45f` and TEAx revision `8d877460ac4f6f264561d916e40c1708adb13397` recorded in the [integration return](preparation/integration-return.json). The model's priced magnet subtotals and LCOEs remain conditional estimates with mixed price bases and unresolved manufacturing scope.

## Question and controlled assumptions

The question is whether one internally consistent magnet inventory can carry the current, fit the declared casing allocation and satisfy the existing plant constraints. The principal construction is 6 mm wide, 56 µm full-composite tape at 20 K, with inherited pack fractions and square section. Material, orientation and retention factors are unity. The allowable operating fraction remains 0.8 and the selected field ceiling remains 24.9 T. A multiplier of 1.01 buys one percent additional physical inventory above the calculated minimum; it does not change either acceptance criterion. [Protocol](protocol.md).

Turn current is held at 50 kA. Changing coil ampere-turns changes the modeled continuous series-turn count, `NI/50,000`: 15.4 MA-turn corresponds to 308 turns, and 16.2 MA-turn to 324. These are homogenized quantities, not integer cable-stack or manufacturable winding specifications. Greater conductor capability reduces parallel inventory; it does not silently raise the independently selected field ceiling.

The window is engineered. An initial 256-point default grid was followed by 60 targeted default refinement points and retained local allocation/performance controls. The initial bounds span major radius 12.7–15.0 m, minor radius 1.3–1.9 m, coil ampere-turns 15.4–18 MA-turn, radial allocation 0.30–0.75 m and transverse cavity 0.40–0.75 m. These are declared exploration bounds, not sourced space guarantees. The final scan retains 352 proposal rows, including the separate exact-boundary diagnostic; there are no unsupported selected proposals. Native execution deduplicates repeated physical points. [Selection](preparation/final-selection.json), [initial scan](results/initial-oracle-scan.json), [refinement](results/refinement-oracle-scan.json).

| Cohort | Cases | Current passes | Fit passes | Other18 intersection | All20 passes |
|---|---:|---:|---:|---:|---:|
| default-grid | 256 | 256 | 92 | 0 | 0 |
| default-refinement | 60 | 60 | 60 | 0 | 0 |
| allocation-bracket | 9 | 9 | 3 | 0 | 0 |
| performance-sensitivity | 16 | 16 | 9 | 0 | 0 |
| historical-controls | 4 | 1 | 2 | 4 | 1 |
| shape-sensitivity | 2 | 2 | 2 | 0 | 0 |
| All unique native cases | 347 | 343 | 167 | 4 | 1 |

Family rows can overlap through deduplicated aliases; they must not be summed. The default total includes eligible reference and allocation cases beyond the initial and refinement grids.

## Inventory and accommodation at the reference

At the reference field of 24.9 T, available tape current is 263.039 A. The minimum reference conductor needs 237.608 parallel tapes; with the physical reserve it carries 239.984. Entering mode0 carried only 112.709 reference-effective tapes. Required conductor area is 0.000887068 m² before reserve and 0.000895939 m² after reserve. The selected pack area grows from 0.129600 to 0.275949 m². These are tape/composite and residual-volume calculations, not a new empirical current law. [Reference cases](results/analysis.json), [entering attribution](results/comparison-entering.json).

| Reference quantity | Entering mode0 | Current sizing, same allocation | Current sizing, allocation 0.60/0.60 m |
|---|---:|---:|---:|
| Actual peak field, T | 24.9000 | 24.9000 | 25.2973 |
| Selected pack area, m² | 0.129600 | 0.275949 | 0.278583 |
| Required radial exterior, m | 0.420000 | 0.585309 | 0.587810 |
| Required transverse cavity, m | 0.379000 | 0.548441 | 0.551005 |
| Radial fit margin, m | −0.120000 | −0.285309 | +0.012190 |
| Transverse fit margin, m | +0.021000 | −0.148441 | +0.048995 |
| Operating fraction | 1.686525 | 0.792079 | 0.792079 |
| Tape length, million m | 36.5786 | 77.8845 | 82.3720 |
| Composite conductor length, m | 321600 | 321600 | 336914 |
| Cold volume, m³ | 136.560 | 290.769 | 307.522 |
| Aggregate refrigeration, MW | 2.13776 | 2.53913 | 2.58484 |
| Magnet priced subtotal, USD billion | 1.70744 | 2.55205 | 2.69528 |
| LCOE, USD/MWh | 144.747 | 163.194 | 166.744 |

The middle column requires 0.585309 m radial exterior and 0.548441 m transverse cavity **at the held original field**. It cannot be interpreted as a solved replacement allocation: enlarging radial allocation moves the coil center and raises the actual field. The third column reevaluates that change natively. It passes fit but exceeds the unchanged 24.9 T ceiling by 0.397340 T. The reference divertor load remains 10.51784 MW/m² against 10.0 MW/m². More tape and space therefore do not make this reference plant feasible. Table values are retained in `reference`, `reference-sized` and `reference-accommodated` aliases in [analysis](results/analysis.json) and [proposals](preparation/proposals.json).

## Two informative retained failures

These cases are nearby diagnostic anchors, not demonstrated minima of a distance-to-feasibility objective. Both use 0.65 m radial allocation and 0.65 m transverse cavity.

| Quantity | Field-only failure: R12.7, a1.35, NI16.2 MA-turn | Field-passing failure: R13.1, a1.45, NI15.4 MA-turn |
|---|---:|---:|
| Actual field / selected limit, T | 26.82552 / 24.9 | 24.70597 / 24.9 |
| Minimum / installed reference tapes | 248.468 / 250.952 | 236.495 / 238.860 |
| Selected pack area, m² | 0.303552 | 0.274657 |
| Required radial exterior, m | 0.610955 | 0.584077 |
| Required transverse cavity, m | 0.574729 | 0.547179 |
| Radial / transverse fit margins, m | +0.039045 / +0.075271 | +0.065923 / +0.102821 |
| Divertor load / limit, MW/m² | 9.60371 / 10 | 11.15687 / 10 |
| Loop required / rated flow, kg/s | 208.617 / 225.078 | 245.273 / 225.078 |
| Required / installed coupled heating, MW | 9.68346 / 50 | 2.93103 / 50 |
| Peak wall load / limit, MW/m² | 3.77527 / 4.05 | 4.03504 / 4.05 |
| Stress, MPa / strain | 481.330 / 0.00160443 | 443.020 / 0.00147673 |
| Stored energy, GJ / support mass, million kg | 141.006 / 13.9990 | 130.962 / 13.2148 |
| Tape length, million m | 91.7947 | 85.5179 |
| Cold volume, m³ / refrigeration, MW | 342.700 / 2.67689 | 319.267 / 2.61802 |
| Magnet priced subtotal, USD billion | 2.97475 | 2.81435 |
| LCOE, USD/MWh | 164.050 | 155.114 |

The first passes nineteen predicates but requires a 1.92552 T reduction in actual field to meet the retained field ceiling. The second passes the field screen, current and fit, but exceeds divertor load by 1.15687 MW/m² and rated coolant flow by 20.19519 kg/s. Their positive signed auxiliary requirements also satisfy the burn lower bound. These quantified deficits identify remaining requirements; the study does not grant higher limits. [Anchor outputs and verdicts](results/analysis.json).

## Allocation responds through the model

At the field-only anchor, increasing radial allocation from 0.50 to 0.70 m raises field from 26.61149 to 26.89763 T. Installed reference tapes rise from 249.749 to 251.357 and selected area from 0.302096 to 0.304041 m². Radial margin moves from −0.109633 to +0.088601 m; the sampled 0.60 m point still fails fit by 0.010513 m while 0.65 m passes. The magnet subtotal grows from USD2.89677 billion to USD3.00089 billion and LCOE from 162.231 to 164.658 USD/MWh. Every point remains above the field ceiling. This brackets a local fit transition only. [Allocation-bracket family](results/analysis.json).

At fixed radial allocation 0.65 m, changing transverse cavity from 0.45 to 0.65 m moves its margin from −0.124729 to +0.075271 m. Field, conductor inventory and priced magnet cost remain unchanged. This is an explicit model limitation: transverse space can clear the local fit screen without a modeled casing redesign or corresponding mass/thermal/cost penalty. It is not evidence that extra transverse space is free.

## Required performance versus assumed scenarios

For square packs, the allowed bare side is the smaller of the radial and transverse dimensions after walls, ground insulation, assembly clearance and internal build are deducted. The fixed-field capability threshold is required pack area times inventory reserve divided by that maximum side squared. It is dimensionless. At the original reference allocation the threshold is **4.79079 times default capability**. This is a required gain, not an achieved material or orientation factor. The held-field space requirement is the 0.585309/0.548441 m pair above; actual enlargement requires reevaluating field.

At the accommodated reference, field-only anchor and field-passing anchor, the corresponding thresholds are 0.95536, 0.87202 and 0.78902. Values below unity mean that the chosen space already accommodates the default inventory at that point; they say nothing about the independent field, divertor or flow failures. [Thresholds](results/analysis.json).

Each performance scenario was evaluated at four anchors. Material factors 1.10 and 1.35 and hypothetical orientation factor 2 each pass current at four and fit at three, but pass all twenty at none. The joint retention scenario applies 0.9 separately to cabling, degradation and sharing, giving combined retention 0.729; it passes current at four but fit at none because sizing buys additional inventory. At the original reference, orientation2 still leaves radial fit short by 0.131449 m. At the field-only anchor it halves area and lowers the priced magnet subtotal to USD2.03626 billion, but the field predicate remains violated. No performance premium is priced, so these reductions cannot establish a purchase saving or qualified product choice. [Scenario results](results/analysis.json).

The historical 30 T/orientation3 mode0 control is the sole all-twenty pass, at 145.030 USD/MWh. It preserves an earlier conditional comparison; it is not a default feasible result or an allowable route to increasing this study's 24.9 T limit. Two local shape diagnostics pass fit but retain divertor/flow failures and are excluded from economic ranking.

## Cost propagation and unresolved manufacturing

At unchanged reference geometry, current sizing increases tape procurement from USD0.73157 billion to USD1.55769 billion. Conductor length stays 321600 m, so the length-based winding-operation estimate remains USD0.75042 billion; it does not price increased cross-section handling effort. Support remains USD0.20908 billion because stored energy is unchanged. Extra sheet stock increases from USD0.42113 million to USD0.89669 million. The selected winding subtotal includes purchased tape, external pack materials and winding operations; adding support and separate sheet stock gives the magnet subtotal. [Native quantities](results/analysis.json).

The [account ledger](preparation/account-ledger.md) retains an illustrative USD20/tape-m price with unresolved year, a 1990 winding coefficient escalated to estimated 2026 purchasing power, mixed material proxies and an inherited all-in support rate. Ground insulation, impregnation, joints, cable manufacture, test, yield, rework and spares remain partly unpriced or of unresolved overlap with winding operations. Increased inventory is propagated through the priced subset; the difference is not a complete manufactured-magnet quote. Sheet resin is not bought twice, and total supports do not receive an additional casing-floor charge.

## Constraint census and verification

The table separates default cases from the full cohort. Counts are passes; default denominator324, full denominator347. The other-eighteen intersection is zero for defaults and four for the full cohort; individual predicate passes cannot be combined across different points. The [predicate catalog](results/predicate-catalog.json) retains full qualified identities and the [native cases](results/native-cases.json) retain every point verdict.

| Predicate | Default passes | All-cohort passes |
|---|---:|---:|
| `wp_stress_ok` | 324 | 347 |
| `cond_strain_ok` | 324 | 347 |
| `recirc_ok` | 323 | 346 |
| `cycle_domain_ok` | 324 | 347 |
| `beta_ok` | 324 | 347 |
| `heating_couple_positive_ok` | 324 | 347 |
| `divertor_heat_ok` | 77 | 85 |
| `heating_source_upper_ok` | 324 | 347 |
| `net_positive` | 324 | 347 |
| `burn_hold_ok` | 134 | 157 |
| `wall_load_ok` | 230 | 253 |
| `tbr_ok` | 324 | 347 |
| `heating_couple_upper_ok` | 324 | 347 |
| `peak_field_ok` | 167 | 182 |
| `reference_conductor_current_ok` | 324 | 343 |
| `sustainment_ok` | 249 | 272 |
| `loop_capacity_ok` | 92 | 109 |
| `wp_fit_ok` | 154 | 167 |
| `heating_source_positive_ok` | 324 | 347 |
| `loop_pressure_ok` | 324 | 347 |

All 75,646 mapped scalar comparisons and 6,940 exact predicate comparisons pass across the 347 native cases. Scalar tolerance is relative1e−9 and absolute1e−9 in the reported channel units. Sixteen unmapped older native channels remain explicitly listed; this is not an all-channel independent validation claim. Frozen entering-oracle comparisons preserve mode0 and separate mode1 physical deltas at all selected points; the older native runtime was not rerun. [Oracle comparison](results/oracle-all-points.json), [entering comparison](results/comparison-entering.json).

Maximum absolute fractional closure residuals are 1.22e−15 for reference tape count, 5.55e−16 for selected pack area and 1.33e−15 for operating fraction. The separate multiplier1 diagnostic gives native current margin −3.33e−16 versus oracle zero, hence different exact Boolean verdicts. Both remain recorded without clipping or tolerance changes. The cohort's multiplier1.01 buys physical reserve and yields operating fraction0.8/1.01; it does not alter the predicate. [Residuals](results/sizing-residuals.json), [boundary diagnostic](results/exact-boundary-diagnostic.json).

## Hypotheses and supported conclusion

**H1: a useful bounded feasible region is found.** Not demonstrated. The default feasible fraction is0/324, or0%, outside the 5–95% diagnostic band. There is no default feasible anchor and no feasible-region boundary or cost optimum to report. Endpoint checks from the rejected field-passing anchor cannot bracket such a region. This is not a failed study: it supports the owner's explicitly acceptable bounded negative outcome. It does not prove that untested points inside or beyond the window are infeasible. [Edge-scan interpretation](results/edge-scan.json).

**H2: current sizing belongs inside the model.** Supported for this conditional implementation. Current demand, tape capability, tape count and pack area now determine one selected physical inventory before fit, procurement and downstream calculations. The unchanged independent current reconstruction checks that selected inventory. Native/oracle agreement and closure establish computational consistency, not independent material qualification.

**H3: the coupled calculation has a consistent solution path.** Supported for independently chosen allocation. The path is allocation → coil center/actual field → current-sized inventory → pack dimensions and downstream consequences → comparison with the original allocation. It is acyclic; no iteration was performed and there are no concealed convergence exclusions. Solving for a self-consistent minimum allocation would be a different operation because field changes with allocation.

Missing pack self-field/shape effects, local field-angle and strain maps, casing/support design, three-dimensional interference, transverse mass/thermal response and manufacturing evidence limit all feasibility claims. The study identifies inventory and accommodation requirements and the residual plant conflicts under held criteria. It supports neither engineering qualification nor global impossibility.
