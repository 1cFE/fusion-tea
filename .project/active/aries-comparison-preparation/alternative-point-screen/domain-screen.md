# Frozen-model domain screen

[AGENT] **None of the alternative geometries tabulated in Lyon Tables VII, IX or X enters the frozen model's breeding domain.** Every listed major radius differs from the required 12.7 m. This exclusion holds even if missing current, density and winding data become available. It is a limit of this model's response table, not evidence that any ARIES design is physically infeasible.

[AGENT] The inspected package is the adopted `post-reveal-v1` archive, SHA256 `d65d6ea44517dba3d9012d06706e74fe3006247e2809f6b4bdd64edd85ab5a7a`. The [machine-readable rules](evidence/domain-rules.json) retain frozen member hashes and exact equation/guard excerpts. All six inspected executable files match their live counterparts. [The reproduction script](evidence/domain-screen.py) reads the archive and performs literal extraction and scalar comparisons only. It imports no model implementation and runs no plant.

## The decisive geometry condition

[AGENT] The breeding implementation requires exact Python equality at every fixed coordinate. There is **no nonzero tolerance** and no radius interpolation. Required values are R = 12.7 m, a = 1.3 m, elongation = 1, vacuum = 0.10 m, first wall = 0.05 m, reflector = 0.20 m, high-temperature shield = 0.20 m, structure = 0.15 m, gap = 0.10 m and vessel = 0.10 m. Only blanket thickness interpolates, on the inclusive interval 0.60–1.00 m. See frozen `blanket_tritium_breeding_impl.py:17–30` in the rule evidence.

| Published family | Major radii, m | Independent exclusion |
|---|---|---|
| VII blanket options: reference, ARE-1, ARE-2, ARE-3 | 7.75, 10.13, 7.75, 7.90 | Every R differs from 12.7 |
| IX configurations: reference, SNS, MHH2 | 7.75, 8.96, 9.25 | Every R differs from 12.7 |
| X FS/He net-power scan | 7.75, 8.55, 9.32, 10.11, 10.90 | Largest R remains 1.80 m below required R |
| X SiC net-power scan | 7.75, 7.75, 8.10, 8.74, 9.42 | Largest R remains 3.28 m below required R |

[INHERITED: source-screen agent's visual table inspection] These are 17 column occurrences, including repeated reference geometries, not 17 distinct reactors. Table VIII supplies a component material/geometry recipe rather than an additional independent plant-point family. The [source-point inventory](evidence/source-points.json) owns publication identities and exact table transcriptions; the domain script consumes and hashes it directly. Table X columns run through net-electric targets of 1, 1.25, 1.5, 1.75 and 2 GW.

[AGENT] An unsupported geometry returns seven zero carriers, including `defined_flag=0`. Those zeros are not physical tritium predictions. Fuel inventory and adequacy lose definedness where they depend on this result. An emitted LCOE would not remedy that failure. Conversely, matching all fixed coordinates would establish only interpolation applicability within the declared material/source/opening scenario. It would not validate shaped stellarator neutronics or prove adequate breeding.

## Other independent limits

| Surface | Frozen condition and implication |
|---|---|
| Conductor | Exactly 20 K, 56 µm tape thickness, width 4–6 mm and calculated peak field 20–32 T. Above 24 T requires explicit extrapolation permission. This is a particular approximate REBCO model; it does not qualify a published Nb3Sn coil. Published axis field cannot be substituted for conductor peak field. |
| Current and winding choices | Installed reference-coil turns and per-turn current are separate supplied choices. An aggregate current cannot identify both. Table X supplies neither; density/profile and pack/cavity correspondence also remain unestablished. Holding defaults would evaluate our selected design at source scalars, not reconstruct the published alternative. |
| Magnetic field | Executable positive-clearance checks permit arithmetic; they do not validate the field transfer. The field audit and qualification investigation leave actual coil geometry, signed current-family distribution, finite-pack placement and a matching field-evaluation definition unresolved. No listed alternative is scientifically qualified by merely having a radius closer to the anchor. |
| Primary coolant | The frozen repair requires finite pressure with `p_loop > pressure_drop >= 0`. This is mathematical admission, separate from equipment adequacy. The older coverage map's missing-suction-guard finding is historical; the frozen package contains the repair. |
| Equipment | Helium capacity credit requires supplied point-state identity, with eight-ULP numerical tolerance on suction temperature/pressure, discharge pressure, hot temperature, heat capacity and gamma. That tolerance is not an operating envelope. Steam, salt and water equipment likewise lack qualified general off-design maps. |
| Power cycle | The matched steam calculation fixes main/extraction pressures at 6.2/0.8 MPa, caps steam/reheat at 455°C and admits condenser temperatures 20–60°C. Coupled work, bleed and two-phase endpoint checks remain necessary. These conditions do not represent the reference Brayton cycle. |
| Prices and LCOE | Supplied package prices are not independent predictions of installed ARIES costs. Dollar basis, equipment scope and technology remain unresolved. The separate ARIES PbLi heat-removal path is absent. Arithmetic completion cannot establish a comparable, supported whole-plant LCOE. |

[INHERITED] Detailed domain context is in the [readiness coverage map](../../../../work/analysis/model-evaluation-domain-readiness/coverage-map.md) and [closed readiness answer](../../../../work/orchestration/goals/model-evaluation-domain-readiness/answer.md). Scientific field limits are in the [field audit](../post-reveal-investigation/field-audit/audit.md) and [qualification report](../field-qualification/report.md). Quantity/account comparability is in the [final assessment](../final-assessment/report.md). These records carry remaining empirical and source-transfer qualifications beyond executable guards.

## Useful work that remains possible

[AGENT] The published tables remain useful subsystem evidence. They can test whether the model represents the required blanket/coolant architecture, whether account scopes correspond, and whether material or technology changes are actually expressible. They can also support descriptive comparisons of matched geometric quantities. The final assessment already demonstrates that these checks yield useful findings without supported full-plant operation.

[AGENT] New numerical subsystem tests would need their own matched inputs and scope. A blanket mass check needs the actual blanket geometry, material fractions and density basis; a conductor check needs matching conductor technology, temperature and peak-field definition; a winding check needs separate turns, per-turn current and pack geometry. These tables alone do not supply a complete independent test. Feeding a published output back as an input would condition the test and cannot earn prediction credit for that output.

[AGENT] Relative field tests under proportional currents at fixed complete geometry, or complete geometric similarity, remain scientifically justified under the documented linear magnetostatic assumptions. The alternative radius columns do not prove either condition. Testing the approximation's own arithmetic would verify implementation, not qualify its ARIES field prediction.

[AGENT] No alternate full-plant run is justified as an applicability test by these points: the radius guard already gives the answer. No input was fitted, guard widened, equipment resized or price adjusted. No whole-plant feasibility verdict or new LCOE is reported.
