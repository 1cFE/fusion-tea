# Published alternative points: bounded source screen

[AGENT] The screened Lyon tables identify alternative configurations and power levels, but do not supply a complete independent full-plant input deck for any alternate point. They can support narrower source comparisons. Whether the frozen implementation supports those comparisons is a separate domain assessment.

[INHERITED: owner authorization relayed by coordinator] This screen uses the previously revealed retained ARIES source. It makes no plant run and changes no model, mapping, original result, or historical report. The inventory covers Lyon Tables VII–X and their surrounding case definitions. It is not an exhaustive inventory of ARIES publications or every plotted contour.

## Inventory and field meanings

| Published family | Explicit operating rows | Published geometry and fields | Source |
|---|---|---|---|
| Reference ARE; full-thickness FS/He ARE-1; tapered SiC ARE-2; full-thickness SiC ARE-3 | Four 1 GW net-electric rows | R = 7.75, 10.13, 7.75, 7.90 m; axis B = 5.70, 4.64, 5.64, 5.17 T; peak coil B = 15.1, 12.4, 15.0, 14.4 T | Table VII, PDF p23 / printed p716 |
| Reference ARE; SNS; MHH2 | Three 1 GW net-electric rows | R/a = 7.75/1.70, 8.96/1.49, 9.25/3.48 m; axis B = 5.70, 6.80, 3.76 T; peak coil B = 15.1, 16, 11.4 T | Table IX, PDF p27 / printed p720 |
| ARE FS/He power variation | Five rows: 1, 1.25, 1.5, 1.75, 2 GW net electric | R = 7.75, 8.55, 9.32, 10.11, 10.90 m; axis B = 5.70, 7.61, 8.07, 10, 10 T; peak B absent | Table X, PDF p28 / printed p721 |
| ARE SiC power variation | Five rows at the same net-electric levels | R = 7.75, 7.75, 8.10, 8.74, 9.42 m; axis B = 5.64, 5.64, 6.89, 7.75, 8.27 T; peak B absent | Table X, PDF p28 / printed p721 |
| SiC blanket/shield component recipe | No independent operating point | Component thicknesses, coverage, composition, densities, 2004 unit costs, and generic structural thicknesses | Table VIII, PDF p25 / printed p718 |

[AGENT] The 17 table rows include repeated reference cases. Their exact values and page hashes are in [source-points.json](evidence/source-points.json). Important numeric tables were visually checked against retained PDF renders. Text extraction has displaced columns, so the images control numeric transcription.

[INHERITED: Lyon Table I, PDF p4 / printed p697] Published geometric aspect ratios are ARE 4.55, SNS 6.00, and MHH2 2.66. Minor radius is directly tabulated in Table IX only. A value obtained by dividing R by a rounded aspect ratio would be derived, not an independently published minor radius. Table X's field column is average field on axis. Its 10 T constraint is not a peak coil field limit.

## Reconstruction sufficiency

[AGENT] Tables VII and IX provide fusion and gross electric power, thermal efficiency, density, temperature, beta, confinement quantities, and selected cost totals. Table X provides only net-electric target, major radius, axis field, beta, peak neutron wall load, and CoE. Net electric power is a source design target/result; this screen does not assign it as a frozen-model free input.

[AGENT] The alternative tables do not supply per-turn operating current, winding count, or point-specific winding-pack and casing geometry. Table I supplies normalized maximum coil current and geometric ratios, not a complete independent finite-pack specification. No current was inferred from a field. The reference pack dimensions elsewhere in the paper do not establish alternate pack dimensions. Table VIII's coil-cover, strongback, and intercoil thicknesses are useful structural data. Figure 32 additionally labels a nominal SiC winding-pack radial depth of 19.4 cm and coil case/insulator depth of 2.2 cm. These do not identify a complete point-specific winding pack, turn allocation, current, casing geometry, or validated field map for each alternate power level.

[INHERITED: Lyon §X.F, PDF p26] SNS and MHH2 were developed in less detail than ARE. Their wall flux distributions were not calculated; the paper scaled ARE wall power-density behavior to approximate these configurations. The paper's own approximations must travel with a comparison.

[INHERITED: Lyon §X.E and Table VIII, PDF pp23–25] The SiC family changes material and coolant architecture. It removes helium coolant/manifolds and helium pumping, uses LiPb cooling in blanket and shield, and water cooling at the vacuum vessel. It changes safety-credit assumptions and replacement economics. It is not the FS/He plant with a substituted radius or thermal efficiency.

## Economic basis and source inconsistencies

[INHERITED: Lyon §X.G, PDF p27; Table VIII, PDF p25] Table X CoE uses year-2004 mills/kWh. Table VIII component unit prices use year-2004 dollars/kg. Tables VII and IX are within the same study costing framework. Tables XI–XII are a different cross-study comparison context, with costs converted to 1992 dollars; those rows were not merged into the operating-point deck.

[INHERITED: Lyon §VI.D and §X.E] The reference uses 85% availability, 40 full-power years, and a 1.93 direct-to-capital multiplier. SiC uses LSA 1 rather than LSA 2, a 0.87 indirect/direct ratio rather than 0.93, a 0.70 O&M factor rather than 0.85, and 0.25 rather than 0.50 mills/kWh decommissioning allowance in 1992 dollars. Reconstructing one case must retain its own economic assumptions. The coordinator separately examines the source's CoE equation.

[AGENT] Preserve three disagreements without resolving them silently: Table I gives SNS 18 coils while §X.F calls it 24-coil; the SiC 1 GW peak wall load is 3.63 MW/m² in Table VII but 3.62 in Table X; reference total core cost is 865 M$ in VII but 869 M$ in IX. The cross-study Table XI SiC column also uses axis B = 5.70 T and beta = 6.4%, whereas VII's ARE-2 gives 5.64 T and 5.45%. Table XI therefore cannot silently fill missing values for VII's ARE-2 point.

## What the sources support next

[AGENT] The source tables support checking published R/a, separating axis and peak fields, comparing coolant/material architectures, checking Table VIII material arithmetic, and investigating the source accounting equation under its own assumptions. They do not alone establish an alternative supported full-plant prediction. That would additionally need independent controls, complete applicable geometry and winding data, matched coolant architecture and costs, and a domain check against the frozen implementation.

[AGENT] Plotted radius/field/constraint sensitivity families and the cross-study ARIES-RS, ARIES-AT, SPPS, HSR, and helical-reactor comparisons are present in the paper but not digitized as alternate full-plant decks here. Figure 33's SiC major-radius variation is a plot family, not additional fully tabulated independent cases. This bounded screen makes no claim that an unexamined publication cannot supply better inputs.
