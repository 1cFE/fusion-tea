# Integrated stellarator depth reassessment — September 19, 2026

## 1. Assessment

**All 23 scored entries meet the existing targets, up from 17 on September 18. Six scores increase; none decreases.** The three applicability entries remain not applicable. No entry is ungraded and no rubric gap remains.

The changes are breeding **R2c.P 1 → 3**, installed cooling **R7.S 2 → 3**, facilities **R9.S 2 → 3**, fuel inventory/startup **R10.P 1 → 2**, fuel-processing cost **R10.S 1 → 2**, and estimate maturity/uncertainty **R12.S 2 → 3**. These are fresh integrated assessments, not scores inferred from goal closure.

The four questions have different answers:

- **Depth:** all targets are met under the unchanged rubric.
- **Correctness:** the current reference executes and exactly reproduces retained results. Independent comparisons support the covered calculations, but regression tests, static checks and coverage have unresolved failures or limitations.
- **Engineering adequacy:** no tested design in the latest current-package evidence passes all engineering checks. The current reference fails four of 25 authored checks, plus a separate cooling/conversion interface diagnostic.
- **Physical and cost claims:** a buildable plant, complete installed price and full uncertainty interval remain unsupported.

Authority is [rubric v1](../../.project/active/demo-depth-rubric/rubric.md) at `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`, verified unchanged. Comparison is against the [September 18 assessment](20260918-192403_stellarator-depth-reassessment.md). The [companion cell records](20260919-201643_stellarator-integrated-depth-reassessment.cells.json) contain all 26 entries with previous/current score, target, exact satisfied criterion, current model and executable references, inspected studies, next-level blockers and validation limitations. The graders did not author the rubric, model changes or retained studies.

## 2. Rubric

**P measures physics depth. S measures structure and cost depth.** They are separate scores and are never averaged. A Cost Account Structure (CAS) is the hierarchy of named costs that sums to plant totals. Levelized cost of electricity (LCOE) expresses modeled lifecycle cost per unit of generated electricity.

| Level | Physics | Structure and cost |
|---|---|---|
| 0 | Behavior absent. | No recognizable subsystem or cost home. |
| 1 | Value supplied or held. | Named aggregate cost. |
| 2 | Output calculated from design inputs and verified in execution. | Cost follows sourced engineering quantities. |
| 3 | Computed behavior is constrained and coupled to design or operation. | Separately sized components have the appropriate account and lifecycle treatment. |
| 4 | Interacting physics close across boundaries, with justified search and independent checking. | Design-based estimate with lifecycle scope, uncertainty and suitable reference validation. |

Each area's full written criterion governs. A study does not earn P4 merely by sweeping inputs, and a partial uncertainty treatment does not automatically raise every cost area to S4. Missing evidence means “ungraded,” not zero. The rubric explicitly records correctness defects separately from depth. This matters for the adverse cooling/conversion interface: the computed, constrained cycle remains present, while its physical applicability is not established.

## 3. Scores

“Previous” means September 18. Area 2's three physics entries remain separate. Area 8 remains above its P2 target at P3.

| Plant area | Entry | Previous | Current | Target | Met |
|---|---|---:|---:|---:|---|
| Plasma and operating point | R1.P | 3 | **3** | 3 | Yes |
| Plasma and operating point | R1.S | N/A | **N/A** | N/A | N/A |
| Blanket, shield and replacement structure | R2.S | 3 | **3** | 3 | Yes |
| Radial build and wall load | R2a.P | 3 | **3** | 3 | Yes |
| In-vessel material lifetime | R2b.P | 3 | **3** | 3 | Yes |
| Tritium breeding | R2c.P | 1 | **3** | 3 | Yes |
| Magnets, supplies and cryogenics | R3.P | 3 | **3** | 3 | Yes |
| Magnets, supplies and cryogenics | R3.S | 3 | **3** | 3 | Yes |
| Heating and plasma control | R4.P | 2 | **2** | 2 | Yes |
| Heating and plasma control | R4.S | 2 | **2** | 2 | Yes |
| Divertor | R5.P | 3 | **3** | 3 | Yes |
| Divertor | R5.S | 2 | **2** | 2 | Yes |
| Vessel and vacuum | R6.P | 2 | **2** | 2 | Yes |
| Vessel and vacuum | R6.S | 2 | **2** | 2 | Yes |
| Primary heat transport | R7.P | 3 | **3** | 3 | Yes |
| Primary heat transport | R7.S | 2 | **3** | 3 | Yes |
| Power conversion and electrical plant | R8.P | 3 | **3** | 2 | Yes |
| Power conversion and electrical plant | R8.S | 2 | **2** | 2 | Yes |
| Buildings and handling | R9.P | N/A | **N/A** | N/A | N/A |
| Buildings and handling | R9.S | 2 | **3** | 3 | Yes |
| Fuel and tritium | R10.P | 1 | **2** | 2 | Yes |
| Fuel and tritium | R10.S | 1 | **2** | 2 | Yes |
| Availability and maintenance | R11.P | 3 | **3** | 3 | Yes |
| Availability and maintenance | R11.S | 2 | **2** | 2 | Yes |
| Cost rollup, financing and estimate quality | R12.P | N/A | **N/A** | N/A | N/A |
| Cost rollup, financing and estimate quality | R12.S | 2 | **3** | 3 | Yes |

The unchanged grades were rechecked against current declarations and executable consumers. Plasma confinement still drives operating heating and power limits. Peak wall load still drives its own constraint and the replacement calendar. Magnets retain separate sizing, stress/current/fit limits and cost children. Heating retains its installed/operating distinction; divertor load retains an executable peak limit; vessel volume and fuel-exhaust pumping remain computed. Availability still reaches the electricity denominator. Their current references and exact criteria are recorded individually in the companion JSON, rather than treating the earlier aggregate passing count as evidence.

## 4. Changes since September 18

### Breeding now responds to blanket choices

R2c.P3 meets “2c: computed TBR vs floor pushes back on blanket/build choices.” Tritium breeding ratio (TBR) is tritium produced per fusion neutron. A transport-derived response table supplies computed breeding and a numerical lower value; the live assertion compares that lower value with the larger of the design floor and the fuel requirement. The retained study shows thickness consequences for breeding, field and cost, and preserves unsupported-domain refusals. [Declaration](../../models/library/analyses/mfe_tritium_breeding.sysml:4), [implementation](../../exploration/stellarator_e2e/generated/handwritten/mfe_tritium_breeding/blanket_tritium_breeding_impl.py:13), [final grade and benchmark links](../orchestration/goals/computed-tritium-breeding/evidence/round2/final-review-and-grade.md).

The integration changes the earlier result: the fuel inventory calculation raises required TBR from the breeding goal's historical **1.190** to **1.191669922**. Current mean breeding is **1.198073920**, but its numerical lower value is **1.186145581**, so breeding fails. The table is unchanged; its requirement consumer is newer. Numerical transport/interpolation allowance does not cover uncertain materials, shape or source physics. The full-shell blanket cost inventory also differs from the transport breeder inventory; held neutron-energy multiplication is not computed transport heating.

### Cooling costs now follow equipment

R7.S3 meets “Pumps, piping, heat exchangers as separately sized subaccounts.” Seven quantity-based children replace the old cooling allowances. Machine counts/duties, pipe mass, exchanger area and metal quantities drive procurement and installation; inventories, spares, make-up and dated machine/bundle replacements have separate consequences. All 34 retained focused cases reconcile their child-account sums. [Model](../../models/library/analyses/mfe_cooling_equipment.sysml:3), [implementation](../../exploration/stellarator_e2e/generated/handwritten/mfe_cooling_equipment/cooling_equipment_impl.py:68), [final amended review](../orchestration/goals/installed-cooling-equipment-costs/evidence/round3/final-review-and-grade.md).

The integrated baseline has fourteen circuits. Its represented cooling equipment is **$6.471 billion**, with **$55.674 million/year** of annualized cooling replacements. Eighteen-circuit historical study prices are different scenarios. The later uncertainty change exposes one shared fabrication rate for initial exchanger/pipe and replacement-bundle costs, preserving nominal results rather than applying independent price changes to the same underlying material basis.

### Facilities now have layout and maintenance drivers

R9.S3 meets “Building set sized by volume/function from layout drivers, incl. hot cell and remote-handling facilities.” Twenty-five civil components have their own dimensions, concrete, reinforcement, formwork and cost. Reactor size, exchanger envelope, equipment counts, dated replacement inventory and handling paths drive building and storage needs. Five checks expose readiness, capacity, outage and route failures. The 48-case study includes counterexamples; it does not simply assume that facilities can handle the maintenance plan. [Model](../../models/library/analyses/mfe_facilities.sysml), [final amended review](../orchestration/goals/layout-based-facilities/evidence/final-review-and-grade.md).

All **622 shared buildings/calendar/heat-transport/turbine outputs** in the retained facilities default case exactly match the latest integrated baseline. This supports reuse after the fuel and shared-price changes. Facilities check the existing maintenance calendar; they do not silently extend outages or increase availability to make the design pass.

### Fuel stock and processing now have distinct physical and cost drivers

R10.P2 meets “Tritium inventory, startup requirement, and processing throughput forward-computed, verified.” Running inventories, delay-based startup supply, radioactive decay, reserve stock and isotope-specific flows are computed. The current conservative startup requirement is **4.400 kg tritium**. Inventory and decay enter the running breeding requirement, but annual maintained-stock makeup remains diagnostic; availability-dependent self-sufficiency is not yet a complete P3 constraint. [Inventory implementation](../../exploration/stellarator_e2e/generated/handwritten/mfe_fuel_cycle/fuel_inventory_impl.py:47), [final review and correction](../orchestration/goals/fuel-inventory-and-startup/evidence/final-review-and-grade.md).

R10.S2 meets “Processing-plant cost follows computed throughput with source basis.” The active account uses **12.912 kg/day of running deuterium-plus-tritium exhaust**, including **7.743 kg/day tritium**, rather than net electric power or annual average flow. Availability changes annual activity, not installed running capacity. Four historical price rows share a throughput scale; this is parametric costing, not independently engineered processing subsystems. [Cost implementation](../../exploration/stellarator_e2e/generated/handwritten/mfe_fuel_cycle/fuel_processing_cost_impl.py:30), [source transfer and final review](../orchestration/goals/throughput-based-fuel-processing-costs/evidence/final-review-and-grade.md).

The complete old fuel-handling account is replaced once. Direct process installation and its contingency are excluded from generic freight, and explicit installation is excluded from generic installation. Package-local controls and central supervisory controls have distinct declared ownership; the latter's residual allowance remains uncalibrated. Physical recycling recovery and recurring-price recovery remain different assumptions. Startup stock is calculated but not purchased through a new startup-stock cost formula.

### Estimate maturity and partial uncertainty are explicit

R12.S3 meets “3-digit functional subaccounts where cost concentrates, plus a stated estimate class and uncertainty treatment.” The actual direct estimate reconciles through 23 disjoint rows. Cooling, magnets and facilities make up **73.478%** of represented direct costs and have substantive child calculations. The estimate is provisionally described as **generic Class 5**, meaning an early conceptual estimate judged from available design deliverables. This is not certification, a claimed engineering-completion percentage or an automatic accuracy band. [Account review](../orchestration/goals/cost-estimate-maturity-and-uncertainty/evidence/account-review.md), [method review and final addendum](../orchestration/goals/cost-estimate-maturity-and-uncertainty/evidence/method-review.md).

A 26-entry register describes the actual accounts, missing scope and assumptions. Four selected uncertainties are quantified together: a shared stainless fabrication basis, interpretation of civil source “TN” units, containment price date and possible insulation-stock inclusion. Thirty-six combinations yield a **conditional partial envelope of $15.948–19.304 billion overnight and $244.882–290.376/MWh**, retaining existing 10% contingency. Thirty-six paired zero-contingency diagnostics and two downtime stresses are separate populations. This is not a confidence interval or complete-plant cost range. [Register](../orchestration/goals/cost-estimate-maturity-and-uncertainty/uncertainty-register.md), [results](../../exploration/stellarator_e2e/studies/20260919-cost-estimate-maturity-and-uncertainty/results/summary.json), [final grade](../orchestration/goals/cost-estimate-maturity-and-uncertainty/evidence/final-review-and-grade.md).

## 5. Remaining gaps and limitations

**Unmet rubric targets: none.** The limitations below constrain use of the result; they do not silently raise the agreed targets.

- **Plasma, build and magnets:** empirical confinement/radiation and fixed profiles retain reference discrepancies. Simplified wall shape and damage clocks do not establish full transport/damage closure. Conditional conductor performance, extrapolation, stress and local rectangular fit do not qualify the complete nonplanar coil set.
- **Heating, divertor and vacuum:** held efficiencies do not supply launcher/deposition geometry. The divertor peak screen omits total radiation deposition, erosion and detachment closure. Required pumping speed does not select or price a pumping train with ducts, conductance and regeneration.
- **Cooling and conversion:** the cycle uses a **480°C** fit argument while the salt supply is **465°C**. The **15°C adverse gap** is exposed as `cycle_interface_ok = 0`, outside the 25 authored predicates. Primary hydraulic routing, salt head and exchanger construction retain transfer assumptions. A steam generator has an account owner, but actual price inclusion is unresolved.
- **Facilities and maintenance:** provisional room and equipment envelopes do not establish load support, shielding, contamination or collision-free handling. Doors, cranes, carriers, rails and services remain incompletely priced. Cooling replacements are priced, but additional field outage time is assumed coincident. Unplanned downtime is zero at baseline; coil-life shortfall remains a diagnostic.
- **Fuel:** residence-time transfer, stock availability, extraction, storage, safety equipment, processing replacements and running expense remain incomplete. Calculated startup mass is not a sourced procurement bill. Annual availability, decay and supply do not yet close a self-sufficiency constraint.
- **Costs:** magnet qualification/manufacture, cooling auxiliaries, handling/services and wider fuel scope remain unresolved. Mixed price years and inflation conversion do not prove present vendor prices. Missing equipment is unpriced scope, not zero-cost equipment covered by contingency. O&M and decommissioning remain aggregate, so R11.S stays 2 despite added cooling replacement detail.

Known arithmetic overlaps were checked: active account selection excludes legacy diagnostic totals; delivered cooling and installed facilities are excluded from duplicate freight; explicit fuel installation is excluded appropriately; tape constituents and support inventories are not purchased twice; the two financing/LCOE forms are alternatives rather than additive charges. Unresolved vendor inclusion and insulation/winding coverage remain explicit uncertainties. These checks support the represented account sum, not completeness of the installed plant price.

## 6. Validation and current model results

### Assessed identity and inputs

Checkout: **`9e07184f1301ad0d4ebdba5ae9bbe5fa97f1f1ef`**. Latest canonical-model and generated-package commit: **`fe7205533b191fb538ade6a6ed89d59d04545b82`**. Current canonical models, staged model copies, generated package and oracle surfaces have no differences from that candidate. No uncommitted canonical-model or generated-package changes were found. Later commits and the existing uncommitted writing/status/comparison material were preserved; the full intake status is retained in [identity evidence](20260919-201643_stellarator-integrated-depth-reassessment.evidence/identity.json).

- Executable fingerprint: `b032da4a3971979792bc024bf9cd1a41a2d83d340bad5b59ef3e1a9aeaa77236`.
- Model semantic fingerprint: `ea1555ea133db8ed7ba1c638b29ddf540ba99d811bfcf7d9ef9454b626d3a28a`.
- Indicator-input fingerprint: `e48d5218b6e3be2775a94269a461dccd259fccc5fc41fed7c135dc1336bfe284`.
- Fresh seal verification covers **369 sealed artifacts**. The separate implementation inventory covers **370 package files**, including the package contract itself; these are different counts, not a discrepancy.

The explicit manifest proposal is major radius **12.7 m**, minor radius **1.3 m**, and live availability mode **0**. Executable defaults supply profile exponents **0.33/1.19**, central ion temperature **14.63 keV**, peak electron density **5.06×10²⁰/m³**, legacy magnet sizing with inventory multiplier **1.00**, fourteen cooling circuits, active cooling/facilities/fuel inventory/processing, **5%** single-pass burn, and held **99%** physical recovery. Heating capacity is **100 MW electrical / 50 MW coupled**. Financial defaults are eight construction years, thirty operating years, 7% discount and 10% direct contingency; unplanned downtime is zero. All **490 input values**, grouped by source file, are preserved in the identity JSON so this summary is not the reproducibility contract.

### Current results and scenario separation

| Evidence population | Model and input scope | Result |
|---|---|---|
| Fresh current baseline | Current executable; manifest proposal plus current defaults | **$17.918171B overnight; $271.584320/MWh; 1,008.898 MW net; availability 0.902778. Four of 25 checks fail.** |
| Current alternative LCOE form | Same baseline, separately defined comparison financing convention | **$266.458931/MWh**. Do not add its construction-interest treatment to the headline form. |
| Latest frozen uncertainty population | Same executable, fixed fourteen-circuit design; 36 source alternatives, 36 contingency diagnostics, 2 downtime stresses | 74 completed; **zero passes of all 25 checks**. Source-only partial envelope stated above. |
| Saved r2 comparison | Preserved older executable and its explicitly conditioned controls | Historical comparison evidence only. Not re-executed as current. |
| September 17 feasible neighborhood | Earlier executable, eighteen-loop design and different profiles/geometry/current/inventory inputs | Historical **103/334** passing and **$150.43/MWh** remain historical; no current reproduction is claimed. |

The saved r2 archive still hashes to `fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21`. A fresh comparison restricted to admitted model/executable members finds **266 of 340 identical and 74 different**. New current files are additional to those archived members. The September 18 assertion of model/package identity is therefore no longer true. [Archive comparison receipt](20260919-201643_stellarator-integrated-depth-reassessment.evidence/r2-comparison.json).

### Newly executed checks

All Python/modeling commands used `.codex-test/run`. One fixed baseline was executed through the current stock route; **all 956 outputs and all 25 verdicts exactly match** the latest integration baseline. No search or new scientific study was started. Git/hash checks verified current identity, defaults and archive differences. The subsystem readers also checked all 34 retained cooling child sums and 622 shared facilities/current outputs. [Fresh baseline](20260919-201643_stellarator-integrated-depth-reassessment.evidence/baseline_result.json), [subsystem checks](20260919-201643_stellarator-integrated-depth-reassessment.evidence/cooling-facilities-checks.json).

| Newly run scope | Outcome | Practical consequence |
|---|---|---|
| `tests/models` | **2,205 passed; 46 failed; 46 setup errors; 13 skipped**, 144 warnings; exit 1 | Broad model regression is not clean. Skips are unverified. |
| Two older study consumers plus dependency provenance | **181 passed; 20 failed**; exit 1 | Public replay/contract coverage remains broken; this is not the full study suite. |
| Current fixed baseline | **956 exact output matches; 25 exact verdict matches** | Current baseline reproduces the reviewed integrated candidate, including its four failed engineering checks. |

Full logs are retained: [model tests](20260919-201643_stellarator-integrated-depth-reassessment.evidence/model-tests.log), [consumer tests](20260919-201643_stellarator-integrated-depth-reassessment.evidence/consumer-tests.log). The observed failures include obsolete input/output/predicate counts, superseded breeding values and historical scenarios that no longer disable every new subsystem. All 46 radius setup errors share one comparison of **956 actual outputs against 261 historical expected outputs**; no expected channel is missing. Baseline and radius-control execution completed before that assertion, but subsequent acceptance checks did not run.

There are also concrete consumer defects. The old heating replay uses incorrect direct-oracle facility parameter names, comparing legacy building cost with a still-active layout account. A coil replay leaves new salt-pump shaft heat enabled, explaining its 5.676 MW historical thermal mismatch. A reserve-invariance test reaches its obsolete predicate-count assertion after its earlier invariants pass. These findings explain particular stopping points, not all unreached assertions. [Replay triage](20260919-201643_stellarator-integrated-depth-reassessment.evidence/failure-triage-cooling.md).

Two frozen-versus-current conductor-area comparisons differ by one and two binary64 rounding units (ULPs). They are algebraically equivalent operation sequences, but exact zero-margin current acceptance can be sensitive to rounding. Later predicate checks in those cases were not reached. The current baseline and uncertainty population have no mapped predicate disagreements; that does not certify every exact-boundary scenario. [Radius and boundary triage](20260919-201643_stellarator-integrated-depth-reassessment.evidence/failure-triage-radius.md). No test, tolerance or model was repaired during this assessment.

The first scratch baseline command used the wrong import-directory suffix and stopped before evaluation; correcting it to the documented stock package directory allowed execution. Six numeric Boolean defaults emitted serializer warnings during the successful baseline. Neither event was a model repair or evidence of physical failure.

### Reused checks and limits

The latest frozen study at **`82bf78f8`** applies to the unchanged current scientific surface. Its final independent review checked **565 committed artifacts**; retained verification compares **69,116 mapped scalars and 1,850 predicates**, with no mapped disagreement. Frozen reproduction compares **70,744 native outputs** and all verdicts across 74 cases. These counts overlap and must not be summed as independent validation. Original-source image/page checking is reused through the final independent source reviews; no new source validation is claimed.

The unchanged MFE static receipt passes levels 1, 3, 4 and 5, but fails **level 2 with 10 placeholder-binding warnings** and **level 6 with 1,082 architecture/readiness issues**, including derived-attribute extraction limitations. Its normalized issue comparison records no change against the prior candidate. The exact supported package executes, but the general validator is not clean. [Static receipt](../active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/static.log), [issue comparison](../active/WI-071_shared-fabrication-rate-for-estimate-uncertainty/evidence/static-delta.log).

**Twenty-two numeric outputs lack independent oracle mapping**, and the latest integration did not run the manifest read-set coverage check. Baseline equality and a valid package seal do not fill those gaps. No fresh complete six-level run, full study-test suite, source experiment or engineering qualification was performed. No model or historical artifact was repaired.

## 7. ARIES readiness

This assessment establishes that the **current integrated model reaches all existing depth targets**. It also establishes that current software validation has unresolved failures, the tested current designs remain physically inadequate under their own checks, and the represented price has missing scope and only partial uncertainty treatment.

Meeting depth targets is separate from authorization to reveal held-out material. The [holdout protocol](../../knowledge/holdout/aries-cs/PROTOCOL.md) remains sealed; no barred material, sealed paper or excluded concept was opened. Its pre-existing exposure disclosures remain in force. This assessment does not alter them or claim a new clean-history certification.

The current model also differs materially from saved r2. Deciding whether to replace that comparison package requires an explicit choice of model, inputs, comparison scope and preserved history. This report supplies evidence for that decision; it neither replaces the archive nor authorizes reveal. No HTML, model, threshold, rubric target or frozen package was changed. No merge or push occurred.

### Replacement summary for the readiness HTML

**The current integrated stellarator model meets 23 of 23 depth targets, up from 17 on September 18.** Breeding, cooling equipment, facilities, fuel inventory, fuel-processing cost and estimate uncertainty now meet their targets together. The current reference reproduces at **$17.918B overnight and $271.584/MWh**, but fails divertor, breeding, conductor-current and winding-fit checks; the cooling/conversion interface also remains adverse. No design in the latest 74-case population passes every engineering check. The **$244.882–290.376/MWh** source-alternative envelope covers selected uncertainties only. Regression/static failures and incomplete cost/physical coverage remain. Saved r2 is an older model; depth completion neither replaces it nor authorizes ARIES reveal.
