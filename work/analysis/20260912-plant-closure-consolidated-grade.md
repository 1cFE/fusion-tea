# Consolidated plant-closure grade

[AGENT] **17 of 23 scored cells meet their targets; six remain below.** All three applicability records are confirmed. Compared with the latest historical cell grades under the same rubric, lifetime/calendar, divertor heat, vacuum estimates, primary-loop response, cycle response and availability now reach target. Cycle physics reaches the higher temperature-constrained anchor. Achieved breeding, loop equipment costs, buildings, fuel inventory/startup, processing costs and estimate quality remain below target.

This is a depth grade and proposed disposition packet, not demo acceptance. The design point still violates divertor heat. All nineteen selected cases that pass the eighteen modeled predicates retain a physical TBR margin near −0.116. The required validation battery is not green: 130 passes/120 failures; writer failure behavior remains uncertified. Owner acceptance, comparison decisions and reveal remain separate.

## Evidence and grading method

Grader: `/root/plant_fresh_grader`, 2026-09-12. This non-author session wrote only the earlier static inventory and this grading; it authored no rubric, model or study execution. Authority is the committed T-015 brief at `7876b4e7`, C-001.r1 PASS and the separate Round 4 PASS. The checkpoint expressly permits grading existing evidence while retaining failed validation requirements.

Rubric: `.project/active/demo-depth-rubric/rubric.md@dc0f0b6dc6512b29e1307da647f3a508a1f5356d`. Canonical model: `641c10512076cc21fac78715de2effc2c33b9194`. Inspection HEAD: `7876b4e7accbdb322988700949cc18b7c43812ef`. Scoped diff shows no changed SysML or generated executable since the model revision; `models/README.md` has an intervening catalog/documentation update, which gives no numerical repair credit. Current working-tree model/generated diff is empty.

Accepted package: indicator `609e6cca0a4f329e834b52369a425541ca167bfdfe8608879d900a27ccedf06d`; semantic `15ed665c374729a984f29fa753f444677805939ffb195933419b3489debbd47e`; executable `cbdb2a365f39c7863a038a48ba10356a783d3af3ab61b020c8bbba50cfcab37c`. Study freeze `e1ba37f4`, validation addendum `59351f7d`, fresh synthesis `ca7529d7`. No model/oracle run or new source acquisition was performed for grading.

The highest fully supported row-specific anchor is scored. Complete conjunctions remain intact. Computed throughput does not fill missing inventory/startup; required TBR does not replace achieved neutronics. Conversely, a pressure-conditional pumping estimate can meet the vacuum calculation anchor without claiming an installed train. A sourced fit-temperature boundary can meet the cycle's temperature-limit alternative without claiming materials qualification. Correctness/process defects attach as integrity findings, as required by protocol, rather than becoming invented depth levels.

The complete protocol records are [cells.json](../orchestration/goals/plant-closure/evidence/T-015_grading/cells.json). [Static inventory](../orchestration/goals/plant-closure/evidence/T-013_grading/static-evidence.md) records canonical definitions, instance bindings, handwritten implementations, claim-specific audits and directly viewed source renders. The evidence grades and limits there are preserved. In particular, WI-045/046/047 implementation/integration evidence does not become a distinct independent item audit through this grade.

In the following text, study result filenames refer to `exploration/stellarator_e2e/studies/20260912-plant-closure/results/` at `e1ba37f4`. `native-points.csv` c0000 is the ordinary stored baseline. `baseline_result.json` is explicitly a preparatory unstored result and is used only as a matching channel reference, not relabeled a study case. Current execution identity is carried by `package_identity.json` and the stored-case verifier compatibility record.

## Cell results

| Cell | Score / target | Target met | Evidence conclusion |
|---|---|---|---|
| R1.P | 3 / 3 | Yes | ISS04/ash/radiation demand and beta respond to design inputs; 61 sustainment and 24 beta violations in the selected set demonstrate actual resistance. The native baseline W_th is 519.914214 MJ and demand is 49.079601 MW coupled. Temperature/density remain chosen coordinates, which the coupled power balance tests. |
| R2a.P | 3 / 3 | Yes | All six additional radial outputs have selected-case identities; computed wall peak produces 63 qualified violations. Common R reaches the radial/wall chain; calibration and source-shaped wall transfer remain fixed assumptions. |
| R2b.P | 3 / 3 | Yes | Native baseline life is 4.523926 FPY, five replacements and availability 0.902778. The retained a=1.9→2.0 pair changes replacements 5→4 and availability 0.902778→0.914683, so life reaches the actual schedule and availability. |
| R2c.P | 1 / 3 | No | The achieved binding 1.074 and floor 1.05 pass every selected held-floor check; required TBR at default recovery/burn is 1.19 and reported margin −0.116. No achieved-neutronics producer exists. |
| R3.P | 3 / 3 | Yes | Computed coil field, bore-sensitive peak, winding stress and cold load are verified at the common radius; 13 stress and 80 peak-field violations occur. The retained sizing equation and earlier independently graded sizing intervention remain applicable because the canonical relation is preserved; current field/geometry responses are newly exercised. |
| R4.P | 2 / 2 | Yes | Installed 100 MW wall-plug gives 50 MW coupled capacity while operating demand draws 98.159202 MW wall-plug for 49.079601 MW coupled. Reserve controls and mapped source-efficiency variation preserve the separate chains and stated deposition assumption. |
| R5.P | 3 / 3 | Yes | Computed nonradiated target load at the fixed source transport/geometry gives baseline 10.517842 MW/m² against 10. The qualified fence fails 319 selected cases; the alternative source case and engineered radiation interventions produce actual flux response. |
| R6.P | 2 / 2 | Yes | Computed radial shell geometry and species-resolved gas load both have verified outputs. Baseline throughput is 78.013726 Pa·m³/s and required speed 78.013726 m³/s at declared 1 Pa/300 K. This satisfies a conditional pumping estimate, not installed equipment adequacy. |
| R7.P | 3 / 3 | Yes | Native baseline source heat 3125.932277 MW produces 3009.755707 kg/s flow, 300319.896464 Pa per-path loss and 175.280934 MW pump draw; the loop reaches net/recirculation and capacity predicates. Selected cases include 183 capacity and 107 recirculation violations, with factorial and loop-count interventions. |
| R8.P | 3 / 2 | Yes | At 480 °C turbine inlet the fit gives 0.411356554 efficiency. Cases c0104/c0107 at 383/643 °C violate the temperature domain; c0105/c0106 at 384/642 °C meet its boundary. The modeled temperature response changes power/cost and is constrained, satisfying the explicit temperature-limit alternative in the higher anchor. |
| R10.P | 1 / 2 | No | Annual feed and operating burn/injection/exhaust are verified under held burn/recovery fractions and computed calendar availability. Dormant inventory/growth/extraction inputs are disclosed; startup and inventory are not outputs. Additional throughput does not earn partial credit for the target conjunction. |
| R11.P | 3 / 3 | Yes | The deterministic live calendar supplies the actual fuel and both price consumers. The same sampled count step lowers fixed-loop LCOE 179.796468→176.907586 $/MWh; dates, replacement PV, time balance and dated-energy shadow are checked. Outage duration is an assumed input, not an independently derived maintenance result. |
| R2.S | 3 / 3 | Yes | Blanket, shield, structure and divertor accounts have separate engineered quantities; blanket+divertor form the replacement numerator, while shield/structure are life-of-plant. Selected-case replacement-numerator identities and life-dependent PV/CAS72 verify this separation. |
| R3.S | 3 / 3 | Yes | Winding, casing/structure, power supplies and cryoplant have separate quantity/performance drivers and source-basis accounts. Selected-case checks cover their amounts, cold-load response and winding+structure rollup; no shared lump substitutes for all four. |
| R4.S | 2 / 2 | Yes | Installed delivered capacity remains the ECRH procurement operand; reserve and efficiency cases verify the channel and account. Operating demand is not silently substituted into installed cost. |
| R5.S | 2 / 2 | Yes | Divertor cost follows computed thermal power with an explicit inherited rate/power-law source and CAS home. The row expressly permits a thermal-power proxy; the reported area shadow is not its cost driver. |
| R6.S | 2 / 2 | Yes | Shell-volume cost is verified at baseline ($120.841903 million) and all selected geometries, with inherited rate/power scaling. Gas-load pumping equipment is explicitly outside this account. |
| R7.S | 2 / 3 | No | Primary/intermediate coolant and auxiliary-cooling costs follow plant power; the intermediate/auxiliary terms have computed thermal-power drivers and inherited source basis. This earns parametric costing, while no pump/pipe/IHX equipment subaccounts exist. |
| R8.S | 2 / 2 | Yes | Turbine/electric/misc costs follow computed gross-power drivers with source-based rates; heat rejection retains the thermal-power proxy. All four output/account mappings are verified, with the heat-rejection limitation retained rather than recast as rejected-duty sizing. |
| R9.S | 2 / 3 | No | Grouped fixed/fusion/staffing/thermal-electric/thermal/gross-electric building bases and the handling proxy execute with declared power drivers. There is no layout-derived building-volume or hot-cell-throughput chain. |
| R10.S | 1 / 2 | No | The annual fuel line and CAS80 wrapper are verified, alongside an independent fuel-handling power proxy. Computed processing throughput does not drive a processing-equipment cost account. |
| R11.S | 2 / 2 | Yes | Calendar replacement PV becomes CAS72 and joins annual O&M; finite-sum ledgers and dated events verify life-dependent levelization. O&M and decommissioning remain aggregated and the in-vessel replacement is bundled. |
| R12.S | 2 / 3 | No | Selected-case account identities cover contingency, indirects, IDC, annual wrappers and both LCOEs. The baseline finance ledger independently reports capital charges, annual cost and energy, rather than inferring numerators from LCOE. No model estimate class or uncertainty treatment is established. |
| R1.S | not_applicable | Applicability confirmed | S is not applicable: the plasma has no hardware or cost account of its own; its structure is the calc spine, and its cost lives in rows 3/4. |
| R9.P | not_applicable | Applicability confirmed | Buildings carry no plasma physics; their depth is structural |
| R12.P | not_applicable | Applicability confirmed | The economics layer's depth is structural. |

The six new target-reaching physics changes are R2b.P **2→3**, R5.P **1→3**, R6.P **1→2**, R7.P **1→3**, R8.P **1→3**, and R11.P **1→3**. All other scores match the latest historical reading for their cell, after re-evaluation here. Those historical comparisons use `grading.md`, `grading-r1-regrade.md`, `grading-r3-regrade.md`, and `grading-r4-regrade.md` under the same rubric; they are depth comparisons across model revisions, not attribution of all economic changes to this study.

R8.P earns 3 because the literal anchor permits a **materials or temperature limit**. The cycle's temperature-dependent calculation and native edge cases demonstrate the temperature alternative. R11.P earns 3 because computed life changes the dated schedule, availability and economics; this does not claim that the held outage estimate itself is computed from maintenance resources. R5.S stays 2: bundled replacement of an aggregate divertor account does not supply modeled target/cassette units. These distinctions apply the actual row anchors without adding or dropping conjuncts.

## Below-target dispositions and acceptance consequences

[AGENT] Each disposition below is proposed **bounded** use. None is owner acceptance. Under the unchanged comparison specification, B-2 requires all three structural correspondences, B-3 uses model/reference ratios in [1/3, 3], and B-4 uses [0.5, 2.0]. A missing or noncomparable quantity is not a pass. This grade performs no held-out comparison and determines no B-2/B-3/B-4 verdict. Fuel and availability lack dedicated homes in the frozen B-2 frame; their omissions remain explicit rather than disappearing in aggregation.

### R2c.P — bounded, below target

- **B-2:** The blanket/build structure exists, but its source-conditioned TBR is not evidence of neutronic correspondence at another design.
- **B-3:** No computed achieved-TBR response or self-sufficiency ratio can be supplied; 1.074 versus required 1.19 remains adverse conditional evidence.
- **B-4:** Blanket volume cost cannot certify a breeding-qualified blanket; any component comparison must retain the missing neutronic qualification.
- **Missing evidence and next owner:** Admissible configuration-specific neutronics and recovery/extraction semantics; modeling/research owner, with source adoption and residual ruling reserved to the methodology owner.

### R7.S — bounded, below target

- **B-2:** Coolant and auxiliary-cooling homes exist, but separately represented pump/pipe/IHX equipment correspondence is missing.
- **B-3:** Computed flow, loss, work and IHX duty can be compared only within the representative-circuit transfer; minimum loop count does not demonstrate buildable equipment.
- **B-4:** Existing power proxies cannot be presented as sized pump/pipe/IHX estimates or an equipment-cost optimum; missing comparable costs cannot count as a pass.
- **Missing evidence and next owner:** Sourced sizing and installed procurement/fabrication costs for pumps, piping and IHX; thermal/equipment modeling owner, source approval by owner.

### R9.S — bounded, below target

- **B-2:** Grouped building and handling accounts do not establish volume/function/layout correspondence, especially for hot cell and remote handling.
- **B-3:** No model-owned building volume or handling-throughput output supports a derived-quantity comparison for that scope.
- **B-4:** Power-scaled bases may be labeled and compared only as those proxies; they do not supply layout-based facility costs.
- **Missing evidence and next owner:** Admissible layout, component handling paths/throughput and building-rate basis; facility/RH modeling owner, owner rules on any residual or comparison amendment.

### R10.P — bounded, below target

- **B-2:** Fuel cycle has no dedicated B-2 home in the frozen frame; keep that omission visible if the comparison treats it as first-order.
- **B-3:** Operating throughput is computed, but startup stock and inventory are unavailable; the complete target cannot be marked passed from throughput alone.
- **B-4:** Annual feedstock costs omit inventory/startup capital and processing equipment consequences; no complete fuel-system cost follows.
- **Missing evidence and next owner:** Residence times, extraction/retention and reserve/startup policy with source authority; fuel-cycle modeling/research owner and methodology owner for source/semantics decisions.

### R10.S — bounded, below target

- **B-2:** A feedstock line and power proxy are not processing-plant decomposition; the absent B-2 fuel-cycle home remains visible.
- **B-3:** Flow outputs do not size processing subsystems or prove a resisting capacity.
- **B-4:** No throughput-priced processing plant exists; do not compare annual fuel expenditure as though it were processing equipment capital.
- **Missing evidence and next owner:** Sourced processing capacities and cost relation tied to throughput; fuel-cycle/economic modeling owner, owner source approval.

### R12.S — bounded, below target

- **B-2:** CAS arithmetic/decomposition is available, but universal typed/scalar/dialect account correspondence remains unresolved and must be checked explicitly.
- **B-3:** Both price forms are verified only at selected finite, fixed-finance, single-module inputs; normalized cross-concept and zero/equal-rate claims are unavailable.
- **B-4:** No model estimate class/uncertainty treatment is established; the B-4 acceptance band itself does not bestow AACE estimate maturity, and cost scope/currency/year must match before a ratio is meaningful.
- **Missing evidence and next owner:** Declared estimate maturity/uncertainty and common monetary/account/timing basis; coding/economic-model owners for concrete defects, methodology owner for finance/comparison/residual decisions.

## Integrity and applicability findings

- **I-validation — unmet requirement, all executed claims.** The post-record focused battery has 130 passes/120 failures. Ninety-seven failure names match the retained consumer audit; eleven concern the earlier radius record; eleven plant-record failures occur in the legacy fixture at the absent `CHANNELS` API before export; one is the known narrative-reference failure. The broader run stopped after 147 passes/one environment-sensitive precondition failure. No completed green broad suite exists. Finite published values and arithmetic agreement do not certify rejection of missing, null or nonfinite values by the local writer. C-001 permits this existing-evidence grade but does not waive either validation or failure-path requirements. Consequence: do not present publication safeguards or workflow validation as certified; route the API/failure-path contract to the coding/tooling owner before claiming that acceptance condition. Evidence: study `addendum/20260912-post-record-validation/{reading.md,test-accounting.json}@59351f7d`, checkpoint review and Round 4 review.
- **I-coverage — selected native execution, all search/minimum claims.** Primary evidence is 371 selected native cases, with 125/19/19 passes under named ten/fourteen/eighteen-predicate views. Full-window counts, flips and minima come from the complete oracle scan, with selected minima native-verified. The stopped 2,525-case prefix is separate supporting evidence, not part of those counts. Four live-loop c3343 factorial corners remain arithmetic exclusions. The 84 edge checks include 36 caught and 48 uncaught endpoints; eight other groups lack a full-set anchor. No full-native-grid, enclosed region, continuous boundary or global optimum is claimed. Evidence: `report-summary.json`, `correlation.json`, `oracle-window-summary.json`, `closure-factorial.json` and the frozen reduction record.
- **I-numerical-scope — verified arithmetic, not scientific validation.** All 371 selected cases have checks for 141 oracle channels, eighteen predicates and seventeen additional scalar identities; generic verification independently reruns 128 cases covering 73 observed verdict patterns, worst relative deviation 7.7964e-16. The seventeen extra outputs remain outside the shared oracle interface, and 147 globally unsupported inputs remain unsupported. Independent computation, source verification, integration checks and physical validity are distinct evidence grades. Shared thresholds and assumptions are not independently validated by their reproduction. Evidence: `all-channel-verification.json`, `verification_summary.json` and the fresh final review.
- **I-source-process — historical boundaries, all cells.** Preserve the original seven-file quarantine hashing violation as unauthorized byte access. A later guard prevents recurrence but does not establish historical compliance; no scientific-use allegation follows from hashing alone. The retained old administrator raw-spawn record limit also remains. This grader performed no protected-source access, source adoption or new source research. Claim-specific WI-050/WI-051/consumer audits preserve their bounded scopes; missing independent WI-045/046/047 item audits remain missing. The three source renders directly viewed during static preparation support only their stated printed fits, exhaust cases and maintenance estimate.
- **I-engineering — R2c/R3/R5/R6/R7/R8/R10/R11 and associated costs.** Achieved TBR is held; negative required-breeding margin is outside the predicate set. Coil-life margin is reported, not constrained. Representative hydraulic loss and source-point compressor calibration do not establish Stellaris circuit design; reconstructed 129.4 MW fluid work differs from printed 130.8 MW circulator total, and unity drive efficiency makes electrical draw a lower bound. Cycle fits do not qualify materials. Vacuum pressure and gas temperature are declared; conductance/train capacity, fuel inventory/startup, processing capacity, reliability and maintenance resources remain absent. Source-low divertor transport is anchor-specific, while full windows hold 0.90 radiation and the 9.5 MW/m² reference case. Radius-scaled target flux remains a shadow. Consequence: predicate satisfaction cannot become a buildable, self-sufficient or equipment-cost-optimal plant claim.
- **I-finance-domain — R3/R7/R9/R11/R12 and all price comparisons.** Fixed discount 0.07, inflation 0.02, eight construction years, thirty operating years and one stellarator/ECRH module avoid selected singularities; they do not repair equal/zero-rate MFE annuities, DCF/IDC or held-calendar limits. Live-calendar zero-CRF handling is separate. Positive-bore/numerical screens do not repair general geometry/critical-current/pack-fit domains. Account dialect, currency/year and construction conventions are inherited and not normalized across concepts. Financial production remains held outside this checkout. Consequence: preserve exclusions and exact account/finance meanings before any B-3/B-4 ratio; no cross-concept comparability clearance follows.
- **I-presentation — actual bindings govern.** The generic divertor comment still says installed heat while its actual producer is operating heat; the assessment's inventory shorthand exceeds the explicitly absent inventory/startup outputs. Executable radiation includes the conversion missing from some displayed prose. These documentation gaps remain findings and add no scientific-use or million-fold execution-error allegation.

## Proposed demo paragraph

[AGENT — proposed wording for owner acceptance] At the current package, the design point produces 1,013.932 MW net at 224.269 $/MWh in the primary price convention, or 220.013 $/MWh in the comparison convention. Computing the loop, cycle and calendar lowers the primary price from the current-package all-held control's 321.643 $/MWh by 16.474, 68.275 and 12.624 $/MWh respectively along that declared sequential path; this is corrected operating-heating attribution, not a rerun of the historical installed-heating model. The complete oracle window's lowest eighteen-predicate candidates at 100 and 220 MW installed wall-plug heating are 191.758 and 198.003 $/MWh, both independently checked as selected native cases at R=12.7 m, a=1.7 m, aspect ratio 7.470588, 13 MA coil current and 14 loops. These are sampled, assumption-conditioned candidates, not global or equipment-cost optima: only 371 selected cases ran in the primary native study, the c3343 factorial is incomplete, and all nineteen full-predicate passes retain negative physical TBR margin near −0.116. The design point still exceeds the divertor heat limit at 10.518 versus 10 MW/m² and has a −17.083 FPY coil-life margin. Missing fuel inventory/startup, installed vacuum equipment, loop costs, materials and reliability evidence limit engineering claims. Post-record validation remains non-green at 130 passes/120 failures, and writer failure behavior is not certified.

Evidence for this wording: `native-points.csv` c0000/c0113/c0130; `closure-factorial.json` baseline corners; `lcoe-bridges.json`; `oracle-window-summary.json` fixed/sized fence-p100 and search-p220 groups; `correlation.json` maps historical c0960/c4609 to native c0113/c0130. At both minima, density is 4.048×10²⁰ m⁻³, ion temperature 14.63 keV, source efficiency 0.5 and ash ratio 8. Their comparison-form prices are 188.126770 and 194.236275 $/MWh. The narrower 220 MW reread arm has different minima (256.533374 fixed / 264.896348 sized); it is not silently substituted for the 220 MW search arm.

The single-closure baseline effects measured independently from all-held are −16.473862 / −74.307672 / −17.098515 $/MWh. They do not add to the total because interaction residual is +10.506466 $/MWh. The sequential paragraph explicitly assigns that interaction through the loop→cycle→calendar order. Larger historical anchors have loop penalties rather than the baseline benefit; their complete factorials remain in the result, while c3343 remains incomplete.

## Owner-held conditions

This report completes the existing-evidence grade, not the goal's acceptance. The owner can accept, correct or decline the proposed bounded packet and demo wording. The six missing target conjunctions and unmet validation/failure-path requirements remain unresolved; a bounded disposition cannot count as a B-2/B-3/B-4 pass or silently relax those rules. Any residual acceptance, comparison-contract amendment, financial normalization, source adoption or reveal requires its existing owner decision. No new numerical cases or source searches are requested merely to make this consolidation complete.

## Exact per-cell anchors and next-level limits

The machine-readable records contain every required protocol field. The following reproduces each satisfied anchor and its next-level explanation; model references and behavior citations are included so this report is reviewable without inheriting a prior score.

### R1.P — 3

**Anchor satisfied:** “An achievable operating point: a confinement/transport relation links field and heating to density and temperature, and a beta, density, or power limit pushes back on the choice”

**Model evidence:** `models/library/analyses/mfe_plasma_sustainment.sysml:4`; `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py:1`; `models/designs/generic_mfe/mfe_plant.sysml:255`; `models/designs/generic_mfe/mfe_plant.sysml:279`; `models/designs/stellarator_09/stellarator_plant.sysml:714`; `models/designs/stellarator_09/stellarator_plant.sysml:1555`; `models/designs/stellarator_09/stellarator_plant.sysml:1593`; `models/designs/stellarator_09/stellarator_plant.sysml:1610`; `models/library/analyses/mfe_plasma_scaling.sysml:4`; `models/library/analyses/mfe_plasma_scaling.sysml:147`; `exploration/stellarator_e2e/generated/handwritten/mfe_plasma_scaling/dt_fusion_power_impl.py:1`.

**Behavior evidence:** ISS04/ash/radiation demand and beta respond to design inputs; 61 sustainment and 24 beta violations in the selected set demonstrate actual resistance. The native baseline W_th is 519.914214 MJ and demand is 49.079601 MW coupled. Temperature/density remain chosen coordinates, which the coupled power balance tests. Read `native-points.csv`, both verification certificates, and `axis-accounts.json`, `constraint-catalog.json`.

**Why not next:** The next anchor requires jointly closed operating-point/magnet/heating design search over a justified range; the present sensitivity grid and inherited empirical/domain limits do not establish that closure.

### R2a.P — 3

**Anchor satisfied:** “2a: wall-load limit pushes back on the design”

**Model evidence:** `models/library/analyses/mfe_plasma_scaling.sysml:52`; `models/library/analyses/mfe_plasma_scaling.sysml:236`; `models/library/analyses/mfe_plasma_scaling.sysml:272`; `models/library/analyses/mfe_plasma_scaling.sysml:341`; `models/designs/generic_mfe/mfe_plant.sysml:177`; `models/designs/generic_mfe/mfe_plant.sysml:395`; `models/designs/generic_mfe/mfe_plant.sysml:413`; `models/designs/generic_mfe/mfe_plant.sysml:422`; `models/designs/stellarator_09/stellarator_plant.sysml:1488`; `models/designs/stellarator_09/stellarator_plant.sysml:1516`; `models/designs/stellarator_09/stellarator_plant.sysml:1564`.

**Behavior evidence:** All six additional radial outputs have selected-case identities; computed wall peak produces 63 qualified violations. Common R reaches the radial/wall chain; calibration and source-shaped wall transfer remain fixed assumptions. Read `native-points.csv`, both verification certificates, and `oracle-historical-comparison.json`.

**Why not next:** The next anchor requires searched and independently checked neutronics/damage closure across the build; a fixed source peak calibration and ordered radial geometry do not supply it.

### R2b.P — 3

**Anchor satisfied:** “2b: lifetime feeds replacement schedule and availability”

**Model evidence:** `models/library/analyses/mfe_lifecycle.sysml:4`; `exploration/stellarator_e2e/generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py:101`; `models/designs/generic_mfe/mfe_plant.sysml:1148`; `models/designs/generic_mfe/mfe_plant.sysml:1185`; `models/designs/stellarator_09/stellarator_plant.sysml:1271`; `models/designs/stellarator_09/stellarator_plant.sysml:1289`.

**Behavior evidence:** Native baseline life is 4.523926 FPY, five replacements and availability 0.902778. The retained a=1.9→2.0 pair changes replacements 5→4 and availability 0.902778→0.914683, so life reaches the actual schedule and availability. Read `native-points.csv`, both verification certificates, and `calendar-steps.json`, `derived-event-tables.json`.

**Why not next:** The next anchor requires neutronics/damage closure across the build; the bundled fluence-to-life calendar lacks material-specific damage, separate divertor life and shielding-dependent coil life.

### R2c.P — 1

**Anchor satisfied:** “Thickness, lifetime, or TBR held as cited values”

**Model evidence:** `models/designs/stellarator_09/stellarator_plant.sysml:1522`; `models/designs/stellarator_09/stellarator_plant.sysml:1526`; `models/designs/stellarator_09/stellarator_plant.sysml:1568`; `models/library/analyses/mfe_fuel_cycle.sysml:87`; `models/designs/generic_mfe/mfe_plant.sysml:1078`.

**Behavior evidence:** The achieved binding 1.074 and floor 1.05 pass every selected held-floor check; required TBR at default recovery/burn is 1.19 and reported margin −0.116. No achieved-neutronics producer exists. Read `native-points.csv`, both verification certificates, and `report-summary.json`.

**Why not next:** The next anchor requires achieved TBR computed from blanket configuration, whereas the model holds achieved TBR and computes only the required ratio.

### R3.P — 3

**Anchor satisfied:** “A stress or current-density limit pushes back on coil sizing and field choice”

**Model evidence:** `models/library/analyses/mfe_magnet_field.sysml:4`; `models/library/analyses/mfe_magnet_field.sysml:48`; `models/library/analyses/mfe_magnet_field.sysml:84`; `models/library/analyses/mfe_magnet_field.sysml:197`; `models/library/analyses/mfe_plasma_scaling.sysml:419`; `models/designs/generic_mfe/mfe_plant.sysml:289`; `models/designs/generic_mfe/mfe_plant.sysml:300`; `models/designs/generic_mfe/mfe_plant.sysml:333`; `models/designs/generic_mfe/mfe_plant.sysml:360`; `models/designs/generic_mfe/mfe_plant.sysml:370`; `models/designs/generic_mfe/mfe_plant.sysml:1248`; `models/designs/generic_mfe/mfe_plant.sysml:1254`; `models/designs/generic_mfe/mfe_plant.sysml:1265`; `models/designs/stellarator_09/stellarator_plant.sysml:170`.

**Behavior evidence:** Computed coil field, bore-sensitive peak, winding stress and cold load are verified at the common radius; 13 stress and 80 peak-field violations occur. The retained sizing equation and earlier independently graded sizing intervention remain applicable because the canonical relation is preserved; current field/geometry responses are newly exercised. Read `native-points.csv`, both verification certificates, and `oracle-historical-comparison.json`, `axis-accounts.json`.

**Why not next:** The next anchor requires coil-set closure with confinement and geometry in a checked design search; sampled common-radius responses leave pack/casing fit, conductor-current qualification and the physical geometry domain unresolved.

### R4.P — 2

**Anchor satisfied:** “Wall-plug → coupled-power chain computed with a stated deposition assumption, verified”

**Model evidence:** `models/library/analyses/mfe_heating_chain.sysml:4`; `models/library/analyses/mfe_heating_chain.sysml:79`; `models/designs/generic_mfe/mfe_plant.sysml:523`; `models/designs/generic_mfe/mfe_plant.sysml:534`; `models/designs/generic_mfe/mfe_plant.sysml:539`; `models/designs/stellarator_09/stellarator_plant.sysml:743`; `models/designs/stellarator_09/stellarator_plant.sysml:746`.

**Behavior evidence:** Installed 100 MW wall-plug gives 50 MW coupled capacity while operating demand draws 98.159202 MW wall-plug for 49.079601 MW coupled. Reserve controls and mapped source-efficiency variation preserve the separate chains and stated deposition assumption. Read `native-points.csv`, both verification certificates, and `axis-accounts.json`.

**Why not next:** The next anchor requires a modeled port, coupling or geometry limit on the required heating response; constant efficiencies and a direct installed-capacity ceiling do not supply that mechanism.

### R5.P — 3

**Anchor satisfied:** “A heat-flux or erosion limit pushes back on operation or geometry”

**Model evidence:** `models/library/analyses/mfe_divertor_heat.sysml:4`; `models/designs/generic_mfe/mfe_plant.sysml:1101`; `models/designs/generic_mfe/mfe_plant.sysml:1287`; `models/designs/stellarator_09/stellarator_plant.sysml:1531`.

**Behavior evidence:** Computed nonradiated target load at the fixed source transport/geometry gives baseline 10.517842 MW/m² against 10. The qualified fence fails 319 selected cases; the alternative source case and engineered radiation interventions produce actual flux response. Read `native-points.csv`, both verification certificates, and `constraint-catalog.json`, `axis-accounts.json`.

**Why not next:** The next anchor requires exhaust/detachment closure; the fixed-target transport scaling lacks detachment control, transient/erosion response and a justified geometry transfer.

### R6.P — 2

**Anchor satisfied:** “Shell volume from the radial build and a computed gas-load/pumping estimate, verified”

**Model evidence:** `models/library/analyses/mfe_plasma_scaling.sysml:52`; `models/library/analyses/mfe_account_costs.sysml:108`; `models/designs/generic_mfe/mfe_plant.sysml:177`; `models/designs/generic_mfe/mfe_plant.sysml:688`; `models/library/analyses/mfe_vacuum.sysml:4`; `models/designs/generic_mfe/mfe_plant.sysml:1119`; `models/designs/stellarator_09/stellarator_plant.sysml:1547`; `models/designs/stellarator_09/stellarator_plant.sysml:1550`.

**Behavior evidence:** Computed radial shell geometry and species-resolved gas load both have verified outputs. Baseline throughput is 78.013726 Pa·m³/s and required speed 78.013726 m³/s at declared 1 Pa/300 K. This satisfies a conditional pumping estimate, not installed equipment adequacy. Read `native-points.csv`, both verification certificates, and `package-inputs.json`.

**Why not next:** The next anchor requires a structural or pumping-capacity limit; the declared exhaust pressure, ideal-gas throughput and required effective speed do not model an installed train or resisting capacity.

### R7.P — 3

**Anchor satisfied:** “The computed loop feeds the recirculation/net-power constraints so coolant choices push back on feasibility”

**Model evidence:** `models/library/analyses/mfe_primary_loop.sysml:4`; `models/designs/generic_mfe/mfe_plant.sysml:555`; `models/designs/generic_mfe/mfe_plant.sysml:560`; `models/designs/generic_mfe/mfe_plant.sysml:590`; `models/designs/generic_mfe/mfe_plant.sysml:1238`; `models/designs/generic_mfe/mfe_plant.sysml:1242`; `models/designs/generic_mfe/mfe_plant.sysml:1271`; `models/designs/generic_mfe/mfe_plant.sysml:1274`; `models/designs/stellarator_09/stellarator_plant.sysml:830`.

**Behavior evidence:** Native baseline source heat 3125.932277 MW produces 3009.755707 kg/s flow, 300319.896464 Pa per-path loss and 175.280934 MW pump draw; the loop reaches net/recirculation and capacity predicates. Selected cases include 183 capacity and 107 recirculation violations, with factorial and loop-count interventions. Read `native-points.csv`, both verification certificates, and `closure-factorial.json`, `oracle-window-summary.json`.

**Why not next:** The next anchor requires thermal-hydraulic state closure across the loop; a calibrated representative circuit with held density/layout and an unsized IHX does not close that boundary.

### R8.P — 3

**Anchor satisfied:** “Cycle responds to blanket/coolant temperature with a materials or temperature limit pushing back”

**Model evidence:** `models/library/analyses/mfe_power_cycle.sysml:4`; `exploration/stellarator_e2e/generated/handwritten/mfe_power_cycle/power_cycle_efficiency_impl.py:54`; `models/designs/generic_mfe/mfe_plant.sysml:577`; `models/designs/generic_mfe/mfe_plant.sysml:1278`; `models/designs/stellarator_09/stellarator_plant.sysml:930`.

**Behavior evidence:** At 480 °C turbine inlet the fit gives 0.411356554 efficiency. Cases c0104/c0107 at 383/643 °C violate the temperature domain; c0105/c0106 at 384/642 °C meet its boundary. The modeled temperature response changes power/cost and is constrained, satisfying the explicit temperature-limit alternative in the higher anchor. Read `native-points.csv`, both verification certificates, and `axis-accounts.json`, `closure-factorial.json`.

**Why not next:** The next anchor requires thermodynamic state closure with the primary loop; the printed efficiency correlation and fit-temperature fence do not solve cycle states, exchanger design or material compatibility.

### R10.P — 1

**Anchor satisfied:** “Annual feed from fusion energy with held burn/recovery fractions”

**Model evidence:** `models/library/analyses/mfe_fuel_cycle.sysml:4`; `models/library/analyses/mfe_fuel_cycle.sysml:29`; `models/library/analyses/mfe_fuel_cycle.sysml:83`; `models/designs/generic_mfe/mfe_plant.sysml:1078`; `models/designs/generic_mfe/mfe_plant.sysml:1064`; `models/designs/stellarator_09/stellarator_plant.sysml:1351`; `models/designs/stellarator_09/stellarator_plant.sysml:1359`; `models/designs/stellarator_09/stellarator_plant.sysml:1378`; `models/designs/stellarator_09/stellarator_plant.sysml:1381`; `models/designs/stellarator_09/stellarator_plant.sysml:1384`.

**Behavior evidence:** Annual feed and operating burn/injection/exhaust are verified under held burn/recovery fractions and computed calendar availability. Dormant inventory/growth/extraction inputs are disclosed; startup and inventory are not outputs. Additional throughput does not earn partial credit for the target conjunction. Read `native-points.csv`, both verification certificates, and `axis-accounts.json`, `package-inputs.json`.

**Why not next:** The next anchor requires inventory, startup requirement and throughput together; throughput is computed but residence-time inventory and startup stock are explicitly absent.

### R11.P — 3

**Anchor satisfied:** “Availability derived from the maintenance/replacement schedule and feeds the economics, pushing back on design choices”

**Model evidence:** `models/library/analyses/mfe_lifecycle.sysml:4`; `exploration/stellarator_e2e/generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py:101`; `models/designs/generic_mfe/mfe_plant.sysml:1148`; `models/designs/generic_mfe/mfe_plant.sysml:1185`; `models/designs/generic_mfe/mfe_plant.sysml:1033`; `models/designs/generic_mfe/mfe_plant.sysml:1191`; `models/designs/generic_mfe/mfe_plant.sysml:1223`; `models/designs/stellarator_09/stellarator_plant.sysml:1271`; `models/designs/stellarator_09/stellarator_plant.sysml:1288`.

**Behavior evidence:** The deterministic live calendar supplies the actual fuel and both price consumers. The same sampled count step lowers fixed-loop LCOE 179.796468→176.907586 $/MWh; dates, replacement PV, time balance and dated-energy shadow are checked. Outage duration is an assumed input, not an independently derived maintenance result. Read `native-points.csv`, both verification certificates, and `calendar-steps.json`, `derived-event-tables.json`, `finance-ledgers.json`.

**Why not next:** The next anchor requires maintenance sequence/logistics closure; held outage duration, assumed unplanned fraction and a bundled replacement calendar do not model staffing, access, component reliability or other maintenance classes.

### R2.S — 3

**Anchor satisfied:** “Replaceable units vs life-of-plant components separately sized; replacement logic follows computed life”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:22`; `models/library/analyses/mfe_account_costs.sysml:52`; `models/library/analyses/mfe_account_costs.sysml:82`; `models/designs/generic_mfe/mfe_plant.sysml:665`; `models/designs/generic_mfe/mfe_plant.sysml:673`; `models/designs/generic_mfe/mfe_plant.sysml:681`; `models/designs/generic_mfe/mfe_plant.sysml:1131`; `models/designs/generic_mfe/mfe_plant.sysml:1148`.

**Behavior evidence:** Blanket, shield, structure and divertor accounts have separate engineered quantities; blanket+divertor form the replacement numerator, while shield/structure are life-of-plant. Selected-case replacement-numerator identities and life-dependent PV/CAS72 verify this separation. Read `native-points.csv`, both verification certificates, and `finance-ledgers.json`.

**Why not next:** The next anchor requires a design-based estimate per component class with fabrication basis and uncertainty; current volume proxies and bundled replacement omit that estimate treatment.

### R3.S — 3

**Anchor satisfied:** “Winding pack, structure, power supplies, cryoplant costed as separately sized sub-accounts”

**Model evidence:** `models/library/analyses/mfe_magnet_cost.sysml:56`; `models/library/analyses/mfe_magnet_cost.sysml:103`; `models/library/analyses/mfe_magnet_cost.sysml:141`; `models/library/analyses/mfe_magnet_cost.sysml:178`; `models/library/analyses/mfe_account_costs.sysml:140`; `models/library/analyses/mfe_account_costs.sysml:559`; `models/designs/generic_mfe/mfe_plant.sysml:635`; `models/designs/generic_mfe/mfe_plant.sysml:646`; `models/designs/generic_mfe/mfe_plant.sysml:654`; `models/designs/generic_mfe/mfe_plant.sysml:695`; `models/designs/generic_mfe/mfe_plant.sysml:851`.

**Behavior evidence:** Winding, casing/structure, power supplies and cryoplant have separate quantity/performance drivers and source-basis accounts. Selected-case checks cover their amounts, cold-load response and winding+structure rollup; no shared lump substitutes for all four. Read `native-points.csv`, both verification certificates, and `axis-accounts.json`.

**Why not next:** The next anchor requires design-based fabrication/installation and stated uncertainty; independently driven subaccounts retain empirical casing scaling and fabrication markups without a qualified estimate uncertainty model.

### R4.S — 2

**Anchor satisfied:** “Cost follows installed heating power with source basis”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:196`; `models/designs/generic_mfe/mfe_plant.sysml:717`; `models/designs/stellarator_09/stellarator_plant.sysml:743`.

**Behavior evidence:** Installed delivered capacity remains the ECRH procurement operand; reserve and efficiency cases verify the channel and account. Operating demand is not silently substituted into installed cost. Read `native-points.csv`, both verification certificates, and `axis-accounts.json`.

**Why not next:** The next anchor requires separately costed sources, transmission and launchers with appropriate replacement logic; current installed-power procurement remains an aggregate.

### R5.S — 2

**Anchor satisfied:** “Cost follows divertor thermal power or area with source basis”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:168`; `models/designs/generic_mfe/mfe_plant.sysml:703`; `models/designs/generic_mfe/mfe_plant.sysml:1131`.

**Behavior evidence:** Divertor cost follows computed thermal power with an explicit inherited rate/power-law source and CAS home. The row expressly permits a thermal-power proxy; the reported area shadow is not its cost driver. Read `native-points.csv`, both verification certificates, and `finance-ledgers.json`.

**Why not next:** The next anchor requires targets/cassettes represented as replaceable units; a single thermal-scaled divertor account bundled with blanket replacement does not identify those units or their computed lives.

### R6.S — 2

**Anchor satisfied:** “Cost follows computed shell volume/mass with source basis”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:108`; `models/designs/generic_mfe/mfe_plant.sysml:177`; `models/designs/generic_mfe/mfe_plant.sysml:688`.

**Behavior evidence:** Shell-volume cost is verified at baseline ($120.841903 million) and all selected geometries, with inherited rate/power scaling. Gas-load pumping equipment is explicitly outside this account. Read `native-points.csv`, both verification certificates, and `package-inputs.json`.

**Why not next:** The next anchor requires separately sized shell, ports and pumping train; the current shell calculation omits port and train sizing/costs.

### R7.S — 2

**Anchor satisfied:** “Costs follow loop thermal power or flow quantities with source basis”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:526`; `models/library/analyses/mfe_account_costs.sysml:559`; `models/designs/generic_mfe/mfe_plant.sysml:839`; `models/designs/generic_mfe/mfe_plant.sysml:851`; `models/designs/stellarator_09/stellarator_plant.sysml:830`.

**Behavior evidence:** Primary/intermediate coolant and auxiliary-cooling costs follow plant power; the intermediate/auxiliary terms have computed thermal-power drivers and inherited source basis. This earns parametric costing, while no pump/pipe/IHX equipment subaccounts exist. Read `native-points.csv`, both verification certificates, and `lcoe-bridges.json`.

**Why not next:** The next anchor requires separately sized pumps, piping and heat exchangers; coolant/aux-cooling power proxies do not purchase or cost that equipment.

### R8.S — 2

**Anchor satisfied:** “Costs follow computed gross/net power with source basis”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:226`; `models/designs/generic_mfe/mfe_plant.sysml:732`; `models/designs/generic_mfe/mfe_plant.sysml:737`; `models/designs/generic_mfe/mfe_plant.sysml:742`; `models/designs/generic_mfe/mfe_plant.sysml:747`.

**Behavior evidence:** Turbine/electric/misc costs follow computed gross-power drivers with source-based rates; heat rejection retains the thermal-power proxy. All four output/account mappings are verified, with the heat-rejection limitation retained rather than recast as rejected-duty sizing. Read `native-points.csv`, both verification certificates, and `lcoe-bridges.json`.

**Why not next:** The next anchor requires turbine island, electrical plant and heat sink as separately sized subaccounts; four power-scaled totals do not decompose those facilities.

### R9.S — 2

**Anchor satisfied:** “Grouped building bases scaled by plant power with source basis”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:304`; `models/library/analyses/mfe_account_costs.sysml:366`; `models/library/analyses/mfe_account_costs.sysml:476`; `models/designs/generic_mfe/mfe_plant.sysml:760`; `models/designs/generic_mfe/mfe_plant.sysml:775`; `models/designs/generic_mfe/mfe_plant.sysml:816`.

**Behavior evidence:** Grouped fixed/fusion/staffing/thermal-electric/thermal/gross-electric building bases and the handling proxy execute with declared power drivers. There is no layout-derived building-volume or hot-cell-throughput chain. Read `native-points.csv`, both verification certificates, and `finance-ledgers.json`.

**Why not next:** The next anchor requires volume/function sizing from layout drivers including hot cell and remote handling; grouped power-scaled bases and a handling proxy lack those drivers.

### R10.S — 1

**Anchor satisfied:** “Annual fuel cost line with a CAS home”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:732`; `models/library/analyses/mfe_account_costs.sysml:449`; `models/designs/generic_mfe/mfe_plant.sysml:1033`; `models/designs/generic_mfe/mfe_plant.sysml:869`; `models/designs/generic_mfe/mfe_plant.sysml:1078`.

**Behavior evidence:** The annual fuel line and CAS80 wrapper are verified, alongside an independent fuel-handling power proxy. Computed processing throughput does not drive a processing-equipment cost account. Read `native-points.csv`, both verification certificates, and `finance-ledgers.json`.

**Why not next:** The next anchor requires processing-plant cost driven by computed throughput with source basis; the annual feedstock line and power-scaled fuel-handling proxy are not that relation.

### R11.S — 2

**Anchor satisfied:** “Levelized replacement follows computed component life”

**Model evidence:** `models/library/analyses/mfe_lifecycle.sysml:4`; `exploration/stellarator_e2e/generated/handwritten/mfe_lifecycle/lifecycle_calendar_impl.py:101`; `models/designs/generic_mfe/mfe_plant.sysml:1131`; `models/designs/generic_mfe/mfe_plant.sysml:1148`; `models/designs/generic_mfe/mfe_plant.sysml:1162`; `models/designs/generic_mfe/mfe_plant.sysml:782`; `models/designs/generic_mfe/mfe_plant.sysml:960`.

**Behavior evidence:** Calendar replacement PV becomes CAS72 and joins annual O&M; finite-sum ledgers and dated events verify life-dependent levelization. O&M and decommissioning remain aggregated and the in-vessel replacement is bundled. Read `native-points.csv`, both verification certificates, and `derived-event-tables.json`, `finance-ledgers.json`.

**Why not next:** The next anchor requires replacement per component class plus decomposed O&M and decommissioning; one in-vessel bundle and aggregate staffing/decommissioning proxies do not satisfy the conjunction.

### R12.S — 2

**Anchor satisfied:** “2-digit CAS coverage with computed contingency, indirects, IDC, levelization, and LCOE”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:255`; `models/library/analyses/mfe_account_costs.sysml:276`; `models/library/analyses/mfe_account_costs.sysml:645`; `models/library/analyses/mfe_account_costs.sysml:672`; `models/library/analyses/mfe_account_costs.sysml:806`; `models/library/analyses/mfe_account_costs.sysml:828`; `models/library/analyses/mfe_account_costs.sysml:858`; `models/library/analyses/mfe_lcoe_dcf.sysml:4`; `models/designs/generic_mfe/mfe_plant.sysml:920`; `models/designs/generic_mfe/mfe_plant.sysml:934`; `models/designs/generic_mfe/mfe_plant.sysml:983`; `models/designs/generic_mfe/mfe_plant.sysml:1191`; `models/designs/generic_mfe/mfe_plant.sysml:1215`; `models/designs/generic_mfe/mfe_plant.sysml:1223`.

**Behavior evidence:** Selected-case account identities cover contingency, indirects, IDC, annual wrappers and both LCOEs. The baseline finance ledger independently reports capital charges, annual cost and energy, rather than inferring numerators from LCOE. No model estimate class or uncertainty treatment is established. Read `native-points.csv`, both verification certificates, and `finance-ledgers.json`, `lcoe-bridges.json`.

**Why not next:** The next anchor requires concentrated functional subaccounts plus stated estimate class and uncertainty treatment; account arithmetic, markups and unweighted sensitivities do not supply the latter conjunction.

### R1.S — not_applicable

**Anchor satisfied:** “S is not applicable: the plasma has no hardware or cost account of its own; its structure is the calc spine, and its cost lives in rows 3/4.”

**Model evidence:** `models/library/analyses/mfe_plasma_scaling.sysml:4`; `models/library/analyses/mfe_plasma_sustainment.sysml:4`; `models/designs/generic_mfe/mfe_plant.sysml:635`; `models/designs/generic_mfe/mfe_plant.sysml:717`.

**Why not next:** No next level applies because the frozen rubric assigns this dimension not_applicable.

### R9.P — not_applicable

**Anchor satisfied:** “Buildings carry no plasma physics; their depth is structural”

**Model evidence:** `models/library/analyses/mfe_account_costs.sysml:304`; `models/library/analyses/mfe_account_costs.sysml:476`; `models/designs/generic_mfe/mfe_plant.sysml:760`; `models/designs/generic_mfe/mfe_plant.sysml:816`.

**Why not next:** No next level applies because the frozen rubric assigns this dimension not_applicable.

### R12.P — not_applicable

**Anchor satisfied:** “The economics layer's depth is structural.”

**Model evidence:** `models/library/analyses/mfe_lcoe_dcf.sysml:4`; `models/library/analyses/mfe_account_costs.sysml:645`; `models/library/analyses/mfe_account_costs.sysml:672`; `models/designs/generic_mfe/mfe_plant.sysml:1191`; `models/designs/generic_mfe/mfe_plant.sysml:1223`.

**Why not next:** No next level applies because the frozen rubric assigns this dimension not_applicable.
