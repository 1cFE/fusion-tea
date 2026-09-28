# Joint magnet sizing and feasibility

[AGENT] **The investigated sample contains no default-performance design that satisfies all existing plant constraints.** Current-driven inventory closes the current calculation in all 324 default cases; 154 also fit their independently declared casing. None passes the other eighteen predicates. This is a bounded negative answer, not proof of global infeasibility. The sixteen performance scenarios and two local shape diagnostics also produce no combined pass under the unchanged 24.9 T field limit.

[AGENT] WI-064 implements the missing native sizing calculation. The generated package and independent oracle agree across 347 executed cases, including five entering/historical controls. The sole combined pass is a historical control with a 30 T selected envelope and assumed orientation factor 3. It is outside the main acceptance assumptions and supplies no newly qualified solution. Final independent [review](evidence/final-review.md) is **PASS** for the frozen study and bounded technical answer.

## What changed

[AGENT] The optional current-sizing mode derives tape inventory from the actual field and the selected allowable operating fraction. Legacy mode remains the default and reproduces the entering package. The sizing equations do not improve tape performance or tune reference current density:

```text
available current per tape = inherited field/temperature/construction law
required parallel tapes = turn current / (allowable fraction × available current per tape)
required conductor area = required tapes × tape cross-section / tape fraction
turns = coil ampere-turns / turn current
required pack area = turns × required conductor area
selected inventory and area = 1.01 × required inventory and area
selected effective current density = coil ampere-turns / selected pack area
```

[AGENT] The 1.01 multiplier buys 1% additional physical inventory; it does not change the acceptance criterion. All main cases hold turn current at 50 kA, allowable fraction at 0.80, 6 mm × 56 µm tape at 20 K, inherited 9% tape fraction, square pack and unchanged clearances/walls. Varying ampere-turns changes continuous effective turn count, field, conductor length and their modeled consequences. No free turn-current substitution is claimed. Tape counts and turns remain continuous engineering quantities, not an integer cable/coil manufacturing design.

[AGENT] Independent physical choices are major/minor radius, coil ampere-turns, radial coil allocation and transverse cavity allocation. Tape dimensions, composition and turn current are held construction choices. Material/orientation/retention factors are held assumptions or separately labeled sensitivities. The field normalization, length/volume factors and cost rates are inherited calibration assumptions. Allowable operating fraction, field ceiling and all plant/fit limits are acceptance criteria. Tape count, pack dimensions, density, lengths, loads and priced costs are derived. Full roles and missing dependencies are in [the requirements map](evidence/coupled-requirements.md) and [dependency map](evidence/coupled-dependencies.md).

## Required inventory and accommodation

[AGENT] The entering reference has 15.4 MA-turns and 308 effective turns. At 24.9 T, the inherited law supplies 263.039 A per tape. The minimum inventory is **237.608 parallel tapes per reference conductor**, compared with the entering 112.709. With the declared reserve, it becomes **239.984 tapes**, conductor area **895.939 mm²** and pack area **0.275949 m²**. The selected density is 55.8074 A/mm²; that reduction from 118.827 A/mm² represents purchased inventory.

[INHERITED] The calibrated coil set distinguishes reference-coil loading from the set-average inventory per conductor metre. Its pack-volume and ampere-turn distribution factors give 242.178 set-effective tapes at the same current-sized reference, versus 239.984 reference-effective tapes. Procurement uses the one total tape volume; the current checker reconstructs reference loading with the declared factor ratio. These are two normalizations of the same inventory, not interchangeable counts or separately purchased tape. They do not establish the weakest local cable capacity. The algebra and factor boundary are independently reviewed in [source-design-review.md](evidence/source-design-review.md).

| Native case | Actual field, T | Minimum / selected parallel tapes | Selected pack side, m | Required cavity x × y, m | Independent allocation: radial exterior / transverse cavity, m | Current / fit / all 20 |
|---|---:|---:|---:|---:|---:|---|
| Current-sized reference | 24.9000 | 237.608 / 239.984 | 0.525309 | 0.535309 × 0.548441 | 0.30 / 0.40 | Pass / fail / fail |
| Same plasma and current, larger allocation | 25.2973 | 239.875 / 242.274 | 0.527810 | 0.537810 × 0.551005 | 0.60 / 0.60 | Pass / pass / fail |
| R 12.7 m, a 1.35 m, 16.2 MA-turns | 26.8255 | 248.468 / 250.952 | 0.550955 | 0.560955 × 0.574729 | 0.65 / 0.65 | Pass / pass / fail |
| R 13.1 m, a 1.45 m, 15.4 MA-turns | 24.7060 | 236.495 / 238.860 | 0.524077 | 0.534077 × 0.547179 | 0.65 / 0.65 | Pass / pass / fail |

[AGENT] Each radial exterior contains two 25 mm walls; compare the required x dimension with its interior, not its exterior. At the current-sized reference, required radial exterior is 0.585309 m versus 0.30 m allocated, and transverse cavity is 0.548441 m versus 0.40 m allocated. The deficits are **285.309 mm radial and 148.441 mm transverse**. These are requirements at that evaluated field, not proof that the plant has space for them.

[AGENT] Keeping the original allocation and field would require **4.79079 times default tape performance** to fit the current-sized square pack with the same reserve. This is a required threshold, not an inferred orientation gain or achieved capability. It would still leave the reference divertor failure.

## Geometry feedback and numerical closure

[AGENT] The represented dependency is acyclic: independently allocated coil thickness changes coil position and actual field; that field sets inventory; inventory sets pack dimensions; fit compares demand with the allocation. Every sampled allocation is reevaluated through this complete path. No iterative solver or nonconverged design exists in this formulation. A fixed-field required cavity is only a diagnostic and is not substituted as automatically available space.

[AGENT] Enlarging the reference allocation from 0.30/0.40 m to 0.60/0.60 m illustrates the feedback. Field rises from 24.9000 to 25.2973 T, conductor length from 321.600 to 336.914 km, stored energy from 111.000 to 121.823 GJ, and modeled support mass from 11.616 to 12.490 million kg. Tape procurement rises from 77.8845 to 82.3720 million metres; refrigeration rises from 2.53913 to 2.58484 MW. Fit closes, but the field exceeds the unchanged ceiling by 0.397340 T. [All native quantities](../../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/results/analysis.json).

[AGENT] Across the 342 current-sized native cases, maximum fractional tape-count, pack-area and operating-fraction closure residuals are respectively 1.22e−15, 5.55e−16 and 1.33e−15. The all-point scalar tolerance is relative 1e−9, absolute 1e−9 in each named unit; exact predicate operators remain unchanged. A separately retained multiplier-one reference diagnostic has native current margin −3.33e−16 versus oracle zero and therefore different exact Boolean verdicts. Both are retained outside the prepared-list cohort; neither sign was clipped. The declared reserve is real tape, and the reference still fails fit/divertor either way.

[INHERITED] The model lacks pack self-field and shape-dependent field correction, detailed casing-wall/structural design, full transverse casing mass/thermal response, coil-to-coil interference, bridge redesign and complete field-angle mapping. Existing stress, support and thermal proxies respond only through their represented paths. The two aspect-ratio cases are local fit diagnostics and are excluded from economic design ranking. These gaps prevent an engineering qualification claim; they do not justify assigning free benefit to unmodeled geometry.

## What prevents a sampled pass

[AGENT] The default cohort spans R 12.7–15.0 m, a 1.15–1.9 m, ampere-turns 14.6–18 MA, and declared allocation configurations covering 0.30–0.75 m radial and 0.40–0.75 m transverse space. It combines a 256-point initial grid, 60-point targeted refinement, reference aliases and local allocation brackets. These are explicit engineering assumptions within the existing model's guards, not sourced device accommodation limits. The [window review](evidence/window-review.md) explains the refinement and held criteria.

[AGENT] Of 324 default cases, 247 violate divertor heat, 232 loop capacity, 190 burn hold, 170 fit, 157 peak field, 94 wall loading, 75 sustainment and one recirculating-power limit. Counts overlap. All twenty predicates are evaluated in the [native record](../../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/record.md); current, fit and the other eighteen remain separate.

- [AGENT] The R 12.7 m, a 1.35 m, 16.2 MA-turn case fails **only field**: 26.825521 T against 24.9 T, a required reduction of **1.925521 T (7.18% of actual field)** with its other performance retained. Its divertor load is 9.603709 MW/m² and loop capacity margin +16.460603 kg/s. No independent field-reduction mechanism preserving those quantities was supplied.
- [AGENT] The R 13.1 m, a 1.45 m, 15.4 MA-turn case passes field/current/fit but needs divertor peak load reduced from **11.156873 to 10 MW/m²** and required flow reduced from **245.272965 to 225.077778 kg/s per loop**. These are deficits of 1.156873 MW/m² and 20.195188 kg/s, about 10.37% and 8.23% of their actual demands. The predicate uses peak target load, not the separate area-scaled diagnostic. This is a quantified demand reduction, not an enlarged acceptance limit.
- [AGENT] The reference itself requires divertor load reduced from 10.517842 to 10 MW/m² even after current closure. Increasing its allocation also introduces the field failure described above.

[AGENT] These are necessary changes at named sampled points, not sufficient prescriptions for a redesigned plant. Changing geometry/current also changes heating and heat removal. The model must reevaluate any proposed physical correction. The sample's zero default feasible fraction fails the study's desired 5–95% boundary-search diagnostic; endpoint rejections from an already rejected anchor do not bracket a feasible region. A wider or denser search could find a pass between or outside the sampled coordinates. It would not resolve absent construction, angle, geometry or cost evidence. No global infeasibility or optimum is asserted.

## Performance sensitivities and cost

[AGENT] At four anchors, four scenarios were evaluated: material factor 1.10, material factor 1.35, hypothetical orientation factor 2, and joint retention of 0.9 for each of cabling, degradation and sharing (combined factor 0.729). Each scenario has four current passes and zero combined passes. The two material scenarios and orientation scenario each have three fit passes; joint retention produces none. No local orientation gain was inferred from feasibility. The existing 20 K normalization and 6 mm × 56 µm construction transfer remain conditional; fields beyond approximately 24 T retain explicit source extrapolation. No new research was needed to perform this conditional calculation; missing exact-product/angle measurements remain a limit.

| Case | Physical tape, million m | Priced magnet subtotal, $ billion | LCOE, $/MWh | Feasibility meaning |
|---|---:|---:|---:|---|
| Entering reference, unchanged legacy mode | 36.5786 | 1.70744 | 144.747 | Fails current, fit and divertor |
| Current-sized reference, original allocation | 77.8845 | 2.55205 | 163.194 | Fails fit and divertor |
| Current-sized reference, 0.60/0.60 m allocation | 82.3720 | 2.69528 | 166.744 | Fails field and divertor |
| Field-only rejection, R 12.7 / a 1.35 / 16.2 MA-turns | 91.7947 | 2.97475 | 164.050 | Fails field |
| Field-passing rejection, R 13.1 / a 1.45 / 15.4 MA-turns | 85.5179 | 2.81435 | 155.114 | Fails divertor and loop capacity |

[AGENT] There is **no cheapest feasible default or enhanced main-limit choice** in this sample. The sole historical 30 T/orientation-3 control passes at 27.777881 T and $145.030/MWh, with 0.50 m radial allocation, its historical density multiplier 1.2 and 17 MA-turns. That historical scenario is not a newly permissible design or evidence of orientation capability.

[INHERITED] Costs retain the $20 per physical tape-metre scenario, unchanged composite-conductor winding-length law, additional insulation stock and effective all-in support account. The larger pack does not gain a qualified cross-section-dependent fabrication-effort law. Supplier/performance premiums, yield/spares, joints, installed ground insulation, detailed casing manufacturing and other unpriced factory scope remain unresolved, as do mixed price-year bases. These subtotals are model consequences, not complete quotes. [Inherited account ledger](../magnet-manufacturing-cost-completeness/account-ledger.md).

## Evidence and disposition

[AGENT] Frozen study checkpoint: `02af7123`; implementation checkpoint: `a8589d6b`; entering checkpoint: `c4d720db886213de94bf2dc4c3131a3453dca690`. The single integration pin is `0a1c038663c848e11cff933215a8d15eb96b6650319003b9cf092ecbbc40e52c`. The [frozen study snapshot](../../../../exploration/stellarator_e2e/studies/20260915-joint-magnet-sizing/snapshot.json) digest is `330e0ac2411ce50ff59bd109bcce8c18a5c3d97141cb013a7b870c1689990154`. The 347 unique native cases have 351 report aliases; all evaluated successfully. The staged oracle scans and 38 endpoint diagnostics are retained. The frozen entering oracle was evaluated at matched coordinates; all five legacy controls preserve prior quantities/verdicts. New-mode changes are attributed to inventory and geometry. Older native runtimes were not rerun.

[AGENT] All-point verification passes 75,646 scalar and 6,940 exact predicate comparisons. Generic native-store verification independently samples 34 rows covering every observed verdict combination. All 511 frozen artifact digests and 347 native case/input/output/report joins pass coordinator checks. Native model/generated/independent-oracle component and coupled audits are linked from [WI-064 audit](../../../active/WI-064_current-driven-magnet-inventory-sizing/audit.md). Static validation retains inherited L2 placeholders and L6 unsupported EXPOSE diagnostics, with six added diagnostics explicitly attributed; the omitted integration read-set check and Boolean serializer warnings remain disclosed. Passing numerical evidence does not imply a clean full static validator.

[AGENT] [Finding dispositions](evidence/finding-dispositions.md) route 31 prior findings and seven new sightings while preserving historical failures and remaining seams. [The round trail](trail.md) records independent assurance and accepted learnings. Technical work and independent assurance are complete; formal goal closure and native item archival remain owner-held. No merge or push is performed.

[AGENT] **Internal sizing consistency is demonstrated. Conditional joint feasibility is not demonstrated for the default or enhanced main-limit samples. Engineering qualification remains open.**

[AGENT] Final assurance independently reconstructs 5,552 sizing/fit/threshold identities, rederives all 6,940 predicates, checks all 75,646 current and 73,564 entering-attribution scalar comparisons, and replays five varied current points plus all five entering controls. All 38 joined finding dispositions and L-001–L-003 are accepted. Final record/template/goal checks pass 68 tests; the completion check after disposition append is recorded in the trail.
