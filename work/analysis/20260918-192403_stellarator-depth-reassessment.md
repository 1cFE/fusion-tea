# Stellarator model depth reassessment — September 18, 2026

## Assessment

**17 of 23 scored entries meet their targets. Six remain below target. No score changed from September 12.** All three not-applicable entries were reassessed and remain not applicable; no entry is ungraded. New magnet, divertor and study work adds useful detail and stronger evidence within existing levels, but does not complete another level's requirements.

The rubric measures how much the model calculates and how fully it represents equipment and costs. It does not certify that the assumptions are physically correct, that a design can be built, or that every test passes. The current reference case still fails the divertor heat, conductor-current and winding-pack fit checks. A different, explicitly declared operating scenario has a sampled passing neighborhood.

The assessment uses [the existing rubric](../../.project/active/demo-depth-rubric/rubric.md) at revision `dc0f0b6dc6512b29e1307da647f3a508a1f5356d`, unchanged from [September 12](20260912-plant-closure-consolidated-grade.md). The companion [cell records](20260918-192403_stellarator-depth-reassessment.cells.json) preserve every exact satisfied criterion, old/current score, target, applicability decision, model/runtime/study reference, next-level blocker and attached validation finding. This is an independent assessment by agents who did not author the rubric, model or retained studies.

### What the levels mean

**P means physics depth. S means structure and costing depth.** They are graded separately and never averaged. A cost account is a named place in the plant cost total; the project calls its hierarchy the Cost Account Structure (CAS).

| Level | Physics (P) | Structure and costs (S) |
|---|---|---|
| 0 | Behavior is absent. | No subsystem or cost account exists. |
| 1 | A value is supplied or assumed. | A named aggregate cost exists. |
| 2 | Design inputs calculate an output, and execution is verified. | Cost follows an engineering quantity with a source and account mapping. |
| 3 | A calculated result meets a limit that constrains operation or design. | Independently sized components have appropriate cost and lifecycle treatment. |
| 4 | Interacting physics close across subsystem boundaries, with independent checks and a justified search range. | A design-based estimate covers the equipment lifecycle and states its uncertainty. |

The individual area's criterion also has to be satisfied completely. For example, calculated tritium throughput does not substitute for missing inventory and startup stock. Equipment counts do not establish equipment costs. A held breeding ratio compared with a held minimum remains P1. Missing evidence would mean “ungraded,” not zero.

### Scores

Each line is a separately graded entry. “Met” means at or above the target. The three subdivisions of area 2 remain separate.

| Plant area | Entry | September 12 | Current | Target | Met |
|---|---|---:|---:|---:|---|
| 1. Plasma and operating point | R1.P | 3 | 3 | 3 | Yes |
| 1. Plasma and operating point | R1.S | N/A | N/A | N/A | N/A |
| 2. Build, wall, blanket and lifetime | R2.S | 3 | 3 | 3 | Yes |
| 2. Build, wall, blanket and lifetime: build/wall | R2a.P | 3 | 3 | 3 | Yes |
| 2. Build, wall, blanket and lifetime: lifetime | R2b.P | 3 | 3 | 3 | Yes |
| 2. Build, wall, blanket and lifetime: breeding | R2c.P | 1 | 1 | 3 | **No** |
| 3. Magnets and cryogenics | R3.P | 3 | 3 | 3 | Yes |
| 3. Magnets and cryogenics | R3.S | 3 | 3 | 3 | Yes |
| 4. Heating and plasma control | R4.P | 2 | 2 | 2 | Yes |
| 4. Heating and plasma control | R4.S | 2 | 2 | 2 | Yes |
| 5. Divertor | R5.P | 3 | 3 | 3 | Yes |
| 5. Divertor | R5.S | 2 | 2 | 2 | Yes |
| 6. Vessel and vacuum | R6.P | 2 | 2 | 2 | Yes |
| 6. Vessel and vacuum | R6.S | 2 | 2 | 2 | Yes |
| 7. Primary heat transport | R7.P | 3 | 3 | 3 | Yes |
| 7. Primary heat transport | R7.S | 2 | 2 | 3 | **No** |
| 8. Power conversion and electrical plant | R8.P | 3 | 3 | 2 | Yes |
| 8. Power conversion and electrical plant | R8.S | 2 | 2 | 2 | Yes |
| 9. Buildings and handling | R9.P | N/A | N/A | N/A | N/A |
| 9. Buildings and handling | R9.S | 2 | 2 | 3 | **No** |
| 10. Fuel and tritium | R10.P | 1 | 1 | 2 | **No** |
| 10. Fuel and tritium | R10.S | 1 | 1 | 2 | **No** |
| 11. Availability and maintenance | R11.P | 3 | 3 | 3 | Yes |
| 11. Availability and maintenance | R11.S | 2 | 2 | 2 | Yes |
| 12. Cost rollup and financing | R12.P | N/A | N/A | N/A | N/A |
| 12. Cost rollup and financing | R12.S | 2 | 2 | 3 | **No** |

## Current model and executable

The assessed checkout is **`e78099cb93ab36b57debf70045cc9c4e7bcfcdd8`**. Its latest model-tree commit is `5dd9cbd0292a6f439a790048203bdba1ca124702` (September 16 source-attribution corrections); its latest generated-package commit is `48b65159d8a704aae9eb3c97d77a2079186bf7de` (September 15 divertor account). There are no uncommitted model or generated-package changes.

Fresh checks establish these identities, rather than relying on an archive label:

- Executable: `f52729e684f513d1b210c75f523340085786440fa2828490309b96493755fd14`.
- Model semantics: `8ea7a4c353455698deaa1026d3d3d547d572e08c6ceb58c2bb9cfea26c0120e0`.
- Indicator inputs: `6e427038e8515501e9c42c39823f85e3b0bcbd9f54f830b2779a792851f02551`.

All **296 sealed executable artifacts** pass their byte checks. The current lineage checker passes, including the actual twelve-file indicator read set and two negative coverage checks. Model, package and oracle sources are unchanged from the reviewed integration checkpoint `fe104e8d`. Model/package files are also unchanged from the latest study's entering revision `d53d6ec5`.

### Difference from the saved r2 comparison

**There is no model or executable difference.** All **340 model/package files** inspected inside the actual r2 archive are byte-identical to the current files. The archive hash remains `fa42cb32c1a51989871ba15a3bf2c51ca0a88c9a506b27c8e314c88b42960a21`. The comparison interface and the study choose different inputs to the same executable:

| Case | Profile exponents | Magnet inventory mode | Inventory reserve | Main result |
|---|---|---|---|---|
| Current manifest baseline | 0.33 / 1.19 | Legacy sizing | 1.00 | $144.7474/MWh; 1,012.608 MW net; divertor/current/fit fail. |
| r2 forward control | 0.35 / 1.20 | Current-driven sizing | 1.00 | $162.8711/MWh; 1,003.739 MW net; divertor/current/fit fail. |
| r2 Table 5-conditioned control | 0.35 / 1.20 | Current-driven sizing | 1.00 | $162.9470/MWh; 1,003.767 MW net; same three failures. |
| Latest neighborhood anchor | 0.35 / 1.20 | Current-driven sizing | 1.01 | $150.4295/MWh; 1,010.112 MW net; all twenty screens pass. |

Profile exponents describe the assumed spatial shapes of density and temperature. The Table 5 control also supplies published reference geometry/current. The neighborhood changes geometry, current, density, temperature and cooling accommodation; it uses 18 representative loops and 0.65 m radial/transverse allocations. These are separate input scenarios, not silent changes to defaults or r2. The prices are conditional levelized costs of electricity (LCOE), not complete installed plant estimates. Evidence: latest study [baseline](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/baseline_result.json), [case accounts](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/analysis.json), [report](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/report.md), and [r2 independent verification](../../.project/active/aries-comparison-preparation/replacement-r2/evidence/independent-verification.json).

### Uncommitted work preserved

At intake, five tracked files were modified: `.project/CURRENT_WORK.md`, `.project/active/aries-comparison-preparation/draft.md`, `.project/execution/ENTRIES.md`, `.project/feedback/ENTRIES.md`, and `knowledge/holdout/aries-cs/PROTOCOL.md`. Untracked files comprise triage notes, comparison preparation/review prompts, readiness explanation/review/HTML files and a goal narrative. The complete intake status is preserved in the companion JSON. These files were not treated as executable repairs or altered by this assessment. The protocol's existing exposure disclosures remain in force; no sealed or barred material or excluded concept was opened.

## Changes since September 12

### Magnets have more explicit sizing and cost consequences

The model now traces winding length from the coil bore, buys physical tape length, separates material and winding accounts, represents two-stage coil cooling and total support inventory, and includes conditional insulation stock. Absolute conductor-current capacity, a local casing-fit check and optional current-driven inventory sizing now constrain the design. These are substantial additions inside **R3.P3/S3**.

They do not establish the next level. The conductor estimate retains construction, temperature, field-angle and strain assumptions; the latest anchor exceeds the approximately 24 T measurement extent. A centered rectangular pack-fit calculation does not establish the complete three-dimensional coil fit. Fabrication, installation, joints, qualification, yield and spares remain incompletely priced; no estimate uncertainty has been established. Current evidence includes the [conductor model](../../models/library/analyses/mfe_conductor_current.sysml:3), [fit model](../../models/library/analyses/mfe_winding_pack_fit.sysml:3), [procurement implementation](../../exploration/stellarator_e2e/generated/handwritten/mfe_winding_pack_cost/winding_pack_procurement_cost_impl.py:15), and [manufacturing account ledger](../orchestration/goals/magnet-manufacturing-cost-completeness/account-ledger.md).

### Divertor power destinations are clearer

The divertor is the surface that receives much of the plasma exhaust. The new [heat ledger](../../models/library/analyses/mfe_divertor_heat.sysml:42) separates radiation, captured target power and uncaptured transport, and defines a peak-equivalent area from the source calculation. It preserves the entering reference peak: **10.51784 MW/m² against a 10 MW/m² limit**. Its [implementation](../../exploration/stellarator_e2e/generated/handwritten/mfe_divertor_heat/divertor_heat_ledger_impl.py:14) and retained [acceptance record](../active/WI-065_divertor-deposited-power-and-peak-area-account/audit.md) support that account.

**R5 stays P3/S2.** Physical wetted area, target sharing, radiation deposition and a transferable exhaust/detachment model remain unsupported. The cost still scales with thermal power; target cassettes and their own erosion-driven replacement lives are absent.

### Cooling studies quantify requirements, not installed costs

The September 16 study calculated the representative-loop requirements: fourteen loops at its reference and sixteen at the informative higher-duty case. Eighteen of twenty selected cases passed the loop screen, but none passed every plant screen. Its retained comparison checked **4,520 scalar values and 400 predicates**. See the [study record](../../exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/record.md) and [verification](../../exploration/stellarator_e2e/studies/20260916-primary-loop-sizing/results/verification_summary.json).

The latest anchor's eighteen-loop scenario implies 36 representative circulators and eighteen intermediate heat exchangers, carrying about 3,013.915 MW total duty. These counts do not specify manufactured equipment or its installed price. **R7 stays P3/S2:** flow and pressure loss drive pumping and net power, but pumps, piping and exchangers still lack separate sized cost accounts. The source-to-helium cooling transfer also remains conditional.

### Stellaris reconciliation improved attribution and exposed remaining disagreement

The reconciliation corrected source attribution and separated supplied reference quantities from independent predictions. It did not silently retune production equations to match the source. Eight reconstruction/scaling cases produced **1,808 scalar and 160 predicate agreements** with the independent implementation; none passed all twenty plant checks. At the source-conditioned point, calculated auxiliary heating remains **44.0038 MW**, despite the published ignition claim. Substituting the published stored-energy/confinement and fusion-alpha terms while retaining model radiation leaves **46.5831 MW** unresolved demand.

**R1 stays P3 and R4 stays P2.** The model calculates coupled confinement/heating response, but has not independently reproduced source ignition or closed deposition and hardware geometry. A source-conditioned value gets no independent prediction credit. Evidence: [reconciliation](../orchestration/goals/stellaris-reference-reconciliation/reconciliation.md), [power-balance diagnostics](../orchestration/goals/stellaris-plasma-power-balance/evidence/diagnostics.json), [radiation diagnostics](../orchestration/goals/stellaris-plasma-power-balance/evidence/radiation-diagnostics.json), and [independent review](../orchestration/goals/stellaris-plasma-power-balance/evidence/final-review.md).

### A passing neighborhood now exists within declared assumptions

The September 17 study retained **103 valid all-screen passes among 334 selected native cases**, plus a separate baseline. **43 of 45 neighborhood checks passed** under the 1.01 purchased-inventory scenario. The smallest passing tested-neighbor margins were about **0.0261 T** for peak field and **0.0315 MW/m²** for divertor heat. The original broad screen found only five passes among 512 candidates, so the selected pass fraction is not a probability of feasibility.

This is new behavioral evidence for the coupled model, not a depth promotion or a complete physical design. The joint search is credited. Its physical domain, coil geometry, exhaust transfer and cooling assumptions remain insufficient for P4. Achieved breeding is still assumed, and loop/manufacturing costs remain incomplete. The retained [case results](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/analysis.json), [neighborhood checks](../../exploration/stellarator_e2e/studies/20260917-pre-reveal-feasible-neighborhood/results/neighborhood-summary.json) and [independent review](../orchestration/goals/pre-reveal-feasible-neighborhood/evidence/independent-review.md) support this bounded conclusion.

### Correctness improved without changing depth

Finance rate-limit repairs address the earlier zero/near-zero/equal-rate arithmetic problems. The new targeted test run includes those repairs. Structural reorganization moved calculations into explicit subsystem parts and ports, while generation/domain fixes improved execution behavior. Neither change supplies the missing equipment, fuel-cycle or uncertainty criteria. The September 12 financial defect should therefore not be repeated as wholly unresolved; its scoped repairs are recorded in [WI-052](../active/WI-052_mfe-financial-rate-limits/implementation/scoped-tests.log).

## Remaining gaps

These are the six missing target requirements. Closing them requires the named calculation or cost evidence, not another pass through the existing screens.

| Entry | Current → target | Work or evidence needed |
|---|---|---|
| R2c.P — breeding | 1 → 3 | Calculate achieved tritium breeding from blanket/build configuration using a justified neutronics model, verify it, and let the calculated result constrain blanket choices. Required breeding alone is insufficient. |
| R7.S — cooling costs | 2 → 3 | Size pumps, piping and heat exchangers as separate equipment accounts, with sourced procurement/fabrication/installation costs and explicit rollup. |
| R9.S — facilities | 2 → 3 | Derive building volumes/functions, hot-cell capacity and remote-handling facilities from plant layout, component envelopes and maintenance throughput. |
| R10.P — fuel inventory | 1 → 2 | Calculate startup tritium stock, residence-time inventory and processing throughput together, with declared reserve/extraction assumptions and verified results. |
| R10.S — fuel-processing costs | 1 → 2 | Make processing-plant cost follow the computed throughput with a source basis and cost-account mapping. Annual fuel purchases are not processing equipment. |
| R12.S — estimate quality | 2 → 3 | State estimate maturity/class and apply an explicit uncertainty treatment alongside functional subaccounts where cost concentrates. Contingency percentages and unweighted sensitivities are insufficient. |

### Why the other entries do not advance

The following restates the remaining next-level requirements for entries already at target. Exact criteria and individual citations remain in the companion JSON.

- **Plasma and magnets (R1.P, R3.P/S):** the joint search exists, but independently justified physical closure, full coil geometry and complete cost/uncertainty boundaries do not.
- **Wall/build and lifetime (R2a.P, R2b.P, R2.S):** calculated wall load, fluence-derived life and replacement economics support P3/S3. Material-specific neutron damage across the build and fabrication estimates with uncertainty are still missing.
- **Heating (R4.P/S):** the verified electrical-input-to-plasma-power chain and installed-power cost meet P2/S2. Advancement needs a physical port/coupling/geometry limit and separately costed sources, transmission and launchers with replacement logic.
- **Divertor (R5.P/S):** heat limits constrain operation, but exhaust/detachment closure and separately lived target/cassette units are absent.
- **Vacuum (R6.P/S):** calculated vessel volume and gas throughput support P2/S2. Advancement needs vessel structural or installed pumping-capacity constraints, plus separately sized shell, ports and pumping-train costs.
- **Heat transport physics (R7.P):** representative flow/loss/work feeds plant feasibility. Full thermal-hydraulic state closure across the loop and a realized exchanger design are absent.
- **Power conversion (R8.P/S):** the temperature-dependent efficiency and executable fit-temperature limit satisfy the literal P3 alternative; power-based costs satisfy S2. Advancement needs thermodynamic state closure and separately sized turbine, electrical and heat-rejection equipment. The fit boundary does not qualify materials.
- **Availability and lifecycle (R11.P/S):** computed life changes replacement dates, availability and economics. Advancement needs maintenance logistics and separate component replacement schedules, with decomposed operations, maintenance and decommissioning costs.

R1.S remains not applicable because plasma hardware costs belong to magnets and heating. R9.P and R12.P remain not applicable because the rubric assigns facilities and integrated economics to structural depth.

## Validation limitations

### Newly checked

All new commands used `.codex-test/run`. Identity checks, current lineage, archive/model equality and **542 retained snapshot path/hash occurrences** passed; no mismatch was found. The fresh test batches produced **815 passes and eight failures** in total:

| Targeted batch | Result | Meaning |
|---|---|---|
| Dependency identity; current-driven sizing; conductor current; loop domains; divertor account; financial rate limits | 625 passed; 11 serialization warnings | Supports these specific current implementation and domain checks. |
| Major-radius and winding study consumers | 190 passed; 8 failed | Reproduces unresolved consumer-contract failures on the current checkout. |

The eight failures are two major-radius contract/replay tests; one winding error-message expectation; three winding output-set checks; one adapter-coverage check; and one native winding output-count check. Examples are 313 actual inputs against a 310 expectation and 242 actual outputs against a 228 expectation. The wrong-message case still rejects the invalid input, but with a different error. These are not waived: tests that stop at a failed contract assertion do not certify the later numerical comparison. Exact commands, full logs and test identifiers are embedded in the companion JSON. No test or production code was changed.

### Reused evidence and unresolved limits

The latest study's original native records and independent reviews are reused because source and executable continuity were established. Their local all-point verification compares **75,484 scalar pairs** and **6,680 predicate pairs**. Sixteen of the 242 numeric output channels remain outside that independent oracle mapping, including some finance/radial-build channels; the large comparison count does not cover every output.

The **generic strict verifier did not pass**. At inventory reserve 1.0, three current-boundary predicates disagree: the native implementation produces tiny negative margins while the independent implementation produces zero. Six associated scalar comparisons fail strict relative comparison near zero. All native signs and failures are retained. The separate local summary passes its scalar absolute/relative tolerance with those explicit predicate exceptions; it is not a replacement generic-verifier pass. All 6,680 predicates reconstructed from native operands agree with the native verdicts. These findings attach to R3.P and the interpretation of feasibility, not an invented lower depth score.

Static validation is also not completely clean. The retained WI-065 record reports passing levels 1/3/4/5, ten level-2 literal-binding warnings and 304 level-6 scanner diagnostics. The current executable resolves the interfaces used by these studies, but that does not erase the static findings. This assessment did not rerun the broad suite or recertify general publication failure paths; September 12's historical failures remain historical evidence, not today's full-suite result.

Physical limitations remain attached to their affected entries:

- **R2c.P/R10.P:** supplied achieved breeding is **1.074**, while required breeding is **1.190** under the retained fuel assumptions. Passing the held **1.05** floor does not establish self-sufficiency.
- **R1.P/R4.P:** source ignition remains unreproduced; numerical agreement between implementations cannot resolve missing source energy/radiation detail.
- **R3.P/S:** material performance, field-angle transfer, full coil fit and manufacturing qualification remain conditional; the exact-current discrepancy remains explicit.
- **R5.P/R7.P/R8.P:** source-specific exhaust, representative helium hydraulics and cycle fits have limited physical transfer. Equipment counts and temperature-domain checks do not certify hardware or material compatibility.
- **R2b.P/R11.P:** availability assumes zero unplanned downtime and bundled in-vessel replacement. The baseline coil-life margin remains **−17.0833 full-power years**, reported but not enforced as a lifetime constraint.
- **R7.S/R9.S/R10.S/R12.S:** missing equipment, layout, processing and estimate-uncertainty scope limits prices. Mixed price years remain; some cost expressions cannot evaluate negative net power before a feasibility verdict is returned.

The results can support transparent conditional comparisons and identify model-development priorities. They cannot establish a buildable, breeding-self-sufficient plant, complete installed cost, continuous feasible region or global economic optimum. No new search, model adjustment, rubric revision or reveal was performed.

## Replacement readiness summary

The September 18 reassessment meets **17 of 23 depth targets**, unchanged from September 12. Magnet sizing/costing, divertor accounting and retained feasibility evidence improved within existing levels. The latest study found **103 passing selected cases and 43 of 45 passing neighborhood checks** under declared assumptions; r2's reference failures remain. Six gaps persist: achieved breeding, installed cooling costs, layout-based facilities, fuel inventory/startup, throughput-based processing costs and estimate uncertainty. Targeted verification produced **815 passes and eight consumer-test failures**; current-boundary disagreements and physical qualification limits remain explicit.
