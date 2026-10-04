# REBCO versus Nb₃Sn: subsystem result and conditional plant map

[AGENT] Round 2 draft answer, 2026-10-04. Numerical execution is sealed at `a9683fa1d`; independent integrated interpretation review is pending. Formal goal closure remains owner-held. The exact independently reviewed Round 1 answer is preserved at [answer-round1.md](answer-round1.md).

[OWNER-VERBATIM] “Across explicit assumptions about confinement and coil geometry, when does each material give lower LCOE—and are those conditions supported by evidence?” [Goal Amendment 2](goal.md).

## Answer

[AGENT] At the declared reference prices, Nb₃Sn gives the lower modeled LCOE in all eight cells where both materials have a design that passes the ranking checks. The tested REBCO price needed to reverse that preference ranges from 5.7 to 37.7 USD2021/m. In the ninth cell, the Stellaris-ratio geometry at confinement multiplier 1.0, no tested Nb₃Sn design passes the ranking checks; the nearest fails recirculating power, so there is no material ranking. Higher REBCO field capability helps the plant reach an operating point there; it does not establish that the same plant could instead use Nb₃Sn cheaply.

[AGENT] The evidence does not establish which material should be selected for a real plant. Every comparative cell applies confinement or coil-geometry assumptions outside the named source configurations. Numerical agreement is strong, but the completed comparison is conditional on those transfers, the supplied-equipment policy and incomplete plant accounting. No evaluated design passes breeding; divertor is another open plant gap. The answer is an assumption map with explicit limitations, not a plant-qualified material recommendation.

Evidence: [sealed study](../../../../exploration/stellarator_materials/studies/20260930-magnet-material-plant-map/record.md) §§ 3–4, 13, 15; [data and methods](evidence/round2-report/README.md). The snapshot is `d494d0e92768ff6ed2498c32f9d24fc1cee9e8562cf863e269f92a01eed46de7`. All numbers below come from that record's `results/summary.json` and `results/cases.csv`.

## What the whole-plant comparison adds to Round 1

[AGENT] Round 1 compares genuinely different supplied conductor windings at matched subsystem duty. At its 10 T reference point, annualized winding-plus-refrigeration costs are 48.5 M USD/yr for Nb₃Sn and 286.1 M for REBCO, with a REBCO break-even tape price of 11.25 USD2021/m. Round 2 places both conductor definitions and temperature-staged refrigeration inside the Stellaris plant model, lets the declared policy propose explicit per-material hardware and operating choices, and evaluates each supplied design without resizing it in the plant calculation. Round 1 annualization is not added to plant costs. [Round 1 answer](answer-round1.md); [accounting contract](evidence/plant-contract.md) § 6.

[AGENT] The plant basis changes before any optimization: the untouched reference is 318.74 USD/MWh, while the material REBCO instance at the same supplied design is 412.43. The +93.70 difference includes conductor-basis +57.44, capital multipliers +28.77 and CAS22 tail +8.04, offset by refrigerator capital −0.34 and net electricity −0.21. Comparing a new-material point to 318.74 without this bridge would misattribute a purchasing-basis change to physics. The bridge is an accounting reconciliation; it is not a passing magnet design (the small pack-area residual remains reported).

[AGENT] Of 189 retained equal-duty base pairs, 27 have both designs passing the ranking checks at the same operating point. REBCO is dearer in all 27 by 122.8–370.7 USD/MWh at 80 USD2021/m tape. Up to 38% of a pair's difference is carried by capital multipliers and CAS22 tail, so a plant comparison cannot be reduced to conductor purchase minus cryo electricity alone. Sealed record § 3, “Before the map.”

## The assumption map

[AGENT] Best means lowest LCOE among the tested base designs passing the contract's ranking checks, at REBCO tape 80 USD2021/m and Nb₃Sn strand 8 USD2021/m. LCOE uses the inherited mixed-year plant cost basis. At each lower tape price, the best REBCO design is reselected. The break-even uses the envelope of tested REBCO designs against the cell's best tested Nb₃Sn design; eight crossings were independently checked by package evaluation. This is not a continuous optimum.

| Geometry / confinement multiplier | REBCO / Nb₃Sn LCOE, USD/MWh | REBCO break-even, USD2021/m | Winner at 80 / 30 / 10 | Comparison evidence |
|---|---:|---:|---|---|
| anchored / 1.0 | 587.2 / none | none | no comparison | U |
| anchored / 1.4 | 429.7 / 347.6 | 37.66 | Nb3Sn / REBCO / REBCO | U |
| anchored / 1.8 | 481.1 / 348.7 | 26.20 | Nb3Sn / Nb3Sn / REBCO | U |
| helias / 1.0 | 533.0 / 390.0 | 33.18 | Nb3Sn / REBCO / REBCO | U |
| helias / 1.4 | 469.4 / 324.4 | 19.53 | Nb3Sn / Nb3Sn / REBCO | U |
| helias / 1.8 | 470.9 / 321.1 | 5.68 | Nb3Sn / Nb3Sn / Nb3Sn | U |
| arm / 1.0 | 558.5 / 378.2 | 28.34 | Nb3Sn / Nb3Sn / REBCO | U |
| arm / 1.4 | 466.2 / 309.9 | 13.36 | Nb3Sn / Nb3Sn / REBCO | U |
| arm / 1.8 | 488.7 / 307.7 | 11.10 | Nb3Sn / Nb3Sn / REBCO | U |

![Conditional assumption map](evidence/round2-report/assumption-map.png)

[INHERITED: evidence/plant-contract.md §§ 3.1–3.2] S denotes support at the source configuration, A an analogue, D a derivation, and U an unsupported transfer or supplied assumption. [AGENT] Both best designs in every comparative cell carry confinement U and geometry U; the weaker comparison label is therefore U. The map data contains the per-material labels, case ids, field, radius, power-short and divertor flags. Beta-limit evidence is A and the equipment/structure policies carry U. The figure's labels are physical evidence grades, separate from numerical screening status. [Detailed label reasoning](evidence/round2-report/README.md#evidence-labels).

[AGENT] The anchored ratio is supported at the original Stellaris coil set and pack, but the selected packs differ. HELIAS cells transfer a sourced 2.12 peak/axis ratio into the Stellaris geometry; a ratio with source evidence does not establish an actual coil set. The pack-size arm transfers a slope derived from Helias-5 data to Stellaris and extrapolates it at several leading Nb₃Sn designs. The confinement factors come from specific source configurations, without a validity band spanning these designs. This is why the apparently precise winners remain conditional.

[AGENT] Eight of the 17 selected best designs are below matched fusion power, and ten violate the stricter 0.04 beta screen while passing the ranking's 0.05 screen. The table compares best tested plants under the declared rules; it is not uniformly a matched-fusion-power comparison. Five of eight Nb₃Sn leaders use the 13 T law-edge band. The REBCO 24.9 T leaders extend beyond the conductor law's measured extents. All designs retain their actual flags in the sealed record.

## What field, size and confinement change

[AGENT] More field does not consistently make expensive REBCO competitive. In the anchored / 1.4 cell at R=12.7 m, the crossing falls from 37.66 USD/m at the 18 T target to 30.08 at 20 T, 27.44 at 22 T and 19.63 at 24.9 T. At the 30 USD/m scenario, the 18 T candidate can beat the cell's Nb₃Sn comparator while the highest-field candidate cannot. Additional conductor inventory and plant consequences offset the field benefit under this policy. Source case ids and crossings are in [interactions.csv](evidence/round2-report/interactions.csv).

[AGENT] Size also changes the price required to compete. At anchored / 1.4, the best crossing falls from 37.66 at R=12.7 m to 26.99 at 15 m and about 7 USD/m at 22 m. These are envelopes over other tested design choices, including minor radius, not a pure sensitivity to major radius with hardware fixed. The arm cells show non-monotonic field responses. A negative crossing means a tested design cannot beat the cell comparator even with zero-priced tape under the unchanged other costs; it does not imply a physically negative conductor price.

[AGENT] Improving the supplied confinement multiplier does not guarantee cheaper plants under the burn-control and operating-point policy. Some high-field designs become ignited or require a lower-power companion, and the preferred field or size changes. The cell's break-even falls from 37.66 to 26.20 in the anchored geometry, from 33.18 to 19.53 to 5.68 in the HELIAS hybrid, and from 28.34 to 13.36 to 11.10 in the transferred-arm geometry. These shifts quantify interactions among the declared choices; they do not validate a common confinement multiplier for both physical coil configurations.

![Field and size interactions](evidence/round2-report/field-size-interactions.png)

## Where the cost difference comes from

[AGENT] In anchored / 1.4, REBCO's best tested design is 82.08 USD/MWh dearer. The difference includes conductor +69.64, radial-build savings −23.63, other winding −6.15, buildings −9.67 and packages −7.14, but also net-electricity +39.01, multipliers +11.83 and CAS22 tail +5.35, with the remaining groups closing the balance. Net powers are 867.86 MW for REBCO and 906.67 for Nb₃Sn; cryo demand is 1.45 versus 8.66 MW, yet the cheaper cryogenics does not alone determine net plant performance. Every account group and its paired case ids are retained in [decomposition.csv](evidence/round2-report/decomposition.csv).

![Whole-plant LCOE difference](evidence/round2-report/lcoe-decomposition.png)

[AGENT] The 2021→2026 CPI variant leaves Nb₃Sn the winner in all eight comparable cells at the reference tape price. A sourced-analogue coupling-factor variant changes the HELIAS / 1.8 crossing from 5.68 to 18.32 USD/m; the 86 kA variant changes it to 4.28. Common-P construction for REBCO shifts the arm / 1.8 crossing from 11.10 to 15.34. These are consequential uncertainties because they can change a preference at 10 USD/m. Neither variant qualifies the hybrid geometry. Strain, structure-mass and package-purchase-exponent variants are retained in sealed record § 3. CPI-, strain- and structure-specific crossing prices were not executed and are not invented here.

## Checks, limits and next evidence

[AGENT] All 2,921 declared cases are retained: 1,081 pass the ranking checks, 1,638 fail, 175 are ignited, 23 are capacity-limited, and four are matching package/oracle domain refusals. Numerical verification compares about 4.15 million covered scalar outputs and every one of 73 predicates per evaluated case with zero disagreements. Constants and two static-load channels lack independent comparison; the latter have only identity checks. The r5a absolute tolerance protects near-zero numerical differences, not physical constraint violations. Sealed record § 13.

[AGENT] No real plant passes all engineering checks. Breeding fails everywhere. Four selected leaders fail divertor, although restricting to the divertor-passing subset leaves the material winner unchanged in the eight comparable cells. Every evaluated design re-supplies 25 quantities without cost response. Installed capacities are supplied by a declared offer policy, not automatically repaired by the model. The study exposes those assumptions; their accounting remains incomplete.

[AGENT] To turn the conditional map into a credible physical selection, the missing evidence is configuration-specific coil geometry and current/field verification across the selected pack sizes; confinement and plasma validity at the selected axis fields, profiles and beta; breeding and divertor geometry with coupled heat-removal consequences; and priced capacity/manufacturing/maintenance offers for the currently free quantities. Source-supported ingredients, source-math checks and numerical regression cannot replace those data. No new acquisition, solver or follow-up modeling task is launched by this answer.

## Completion and delivery

[AGENT] Round 1's subsystem answer remains independently reviewed. Round 2's conditional numerical map, accounting, interaction figures, failed-case retention and replay instructions are delivered as a draft. Source-supported physical preference is not established. Independent coupled integration/interpretation review, finding-disposition acceptance and final round assurance remain pending; no goal closure is claimed.

[Replay and rebuild instructions](evidence/round2-report/README.md#numerical-replay), [provenance hashes](evidence/round2-report/provenance.json), [proposed narrative](evidence/round2-report/proposed-narrative.md), and [proposed finding dispositions](evidence/round2-report/proposed-dispositions.md). The article remains unchanged.
