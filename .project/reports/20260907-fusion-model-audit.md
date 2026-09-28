# Fusion model audit

**Date:** 2026-09-07. **Audited model revision:** `b244abd8baf463dbad447935f86d0da5278ee751`. **Scope:** all 25 current SysML files under `models/`, both executable family copies, their calculation implementations, and the relevant validation and source evidence. **Requested by owner:** audit the math, modeling/abstraction practices, and extensibility; flag issues. All findings and recommendations below are **[AGENT] audit judgments**, not newly settled requirements or changes to the modeling backlog.

## Assessment

The models execute, but they are not yet a reliable basis for unrestricted cross-concept optimization. The most serious findings are corrupted source values in the Osiris baseline, disconnected representations of the same physical quantity, an IFE viability check that admits negative net power, and a stellarator operating balance that consumes installed heating rather than the heating needed to hold the selected plasma state.

The stellarator model is substantially stronger than the IFE model. Its geometry, plasma profiles, ash, pressure, field, wall loading, component costs, replacement schedule, and LCOE form a working calculation chain. Its executable tests pass at the audited point. Several engineering limits still depend on held assumptions, and the word “feasible” must be read as satisfaction of the implemented checks within those assumptions.

This report contains **20 findings: 9 high, 10 medium, and 1 low**. “High” means a wrong answer or a materially misleading comparison can result in a plausible use of the model. “Medium” means a bounded correctness, reuse, or verification gap. Known limitations are identified explicitly; they are not presented as newly discovered implementation mistakes.

| ID | Severity | Finding | Classification |
|---|---|---|---|
| F01 | High | Osiris baseline copies corrupted extracted numbers | Source/data defect |
| F02 | High | HIF beam energy, bank energy, repetition rate, and output power can disagree | Model dependency defect |
| F03 | High | IFE viability can pass a net electricity consumer | Mathematical/constraint defect |
| F04 | High | MFE operating power balance uses installed heating | Cross-system consistency defect |
| F05 | Medium | Equal interest and escalation rates divide by zero; other removable singularities remain | Mathematical domain defect |
| F06 | High | One machine has two independently settable major radii | Model dependency defect |
| F07 | High | Invalid coil geometry can produce a negative “peak field” that passes its upper bound | Domain/constraint defect |
| F08 | High | IFE costs do not populate the promised CAS interface; MFE accounting mixes typed and scalar structures | Accounting/abstraction gap |
| F09 | High | Monetary and financing bases are not normalized across concepts | Comparison limitation |
| F10 | Medium | “Generic MFE” unconditionally contains stellarator-specific physics and ECRH wiring | Extensibility defect |
| F11 | Medium | Module-count parameter only scales part of the plant | Known single-module limitation, unenforced |
| F12 | High | Replacement frequency does not reduce availability | Known lifecycle limitation |
| F13 | Medium | Pumping, conversion, and heat rejection do not form a closed thermal system model | Known engineering limitation |
| F14 | Medium | Magnet checks do not establish conductor current capability or configuration validity | Known/remaining magnet limitation |
| F15 | Medium | TBR, divertor, and fuel-cycle feasibility are much shallower than their cost outputs | Known breadth limitation |
| F16 | Medium | Oracle parity and constraint coverage overstate independent physical validation | Verification gap |
| F17 | Medium | Citations are broken or stale despite 100% documentation coverage | Traceability defect |
| F18 | Medium | Reusable definitions, fixed values, and parameter metadata do not consistently support specialization | SysML/reuse gap |
| F19 | Medium | The SysML radiation equations omit the W-to-MW conversion present in executable code | Mathematical documentation defect |
| F20 | Low | Time conventions, names, and guidance contain smaller inconsistencies | Maintenance/precision gap |

## Evidence and limits of the audit

The audit used agentic-mbse’s `model-validation`, `source-traceability`, `sysml-conventions`, and `requirements-tracking` guidance, its `audit-models` verification obligations, and its detailed plant, definition/usage, and semantic-operator patterns. Project requirements override generic guidance where they differ: notably plain `Real` values under AD-001 and path-based citations under MR-4. Absence of a traceability-matrix row is therefore not automatically a project violation.

The canonical tree contains two families: 11 IFE files and 17 MFE files, sharing three files. The family regression tests establish byte equality with the exploration copies. They are not three independently maintained mathematical models for this audit. Archived models, proof-of-concept magnets, and construct/codegen probes are historical fixtures, not additional supported reactor predictions; this report does not certify those fixtures. Quarantined holdout material was not inspected.

The report is a full current-model structural and equation review, with targeted numerical/source verification and reproduced counterexamples. It is **not a certification that every scalar agrees with a primary source**. The evidence directory contains a 415-row census of numeric-bearing expression lines; these include arithmetic expressions and defaults, not 415 independently sourced parameters. Rows not explicitly source-verified here retain unverified status. In particular, calibration to a design point does not validate an off-design scaling law.

The source image, rather than extracted Markdown, was checked for the Osiris operating table, Meier’s driver-cost equation, and the two newly introduced stellarator coil-geometry scalings. The inspected local 1costingFE source was exactly its cited `02543850089be175ea7c28b92a8b2a4184e1637e` revision. Current agentic-mbse pattern documentation came from checkout `88e24896b96788f77ca3eca052a725adbe909753`; execution used the installed project environment without dependency synchronization. TEAx was `/home/reid/1cfe/teax` at `8d877460ac4f6f264561d916e40c1708adb13397`.

Models and PM registries were not changed. The retained probe imports the sealed package, exercises generated arithmetic, and writes its results beside the report. The stellarator runner also rewrote its normal ignored run-output directory. Model hashes and the executable fingerprint are in [probe-results.json](20260907-fusion-model-audit-evidence/probe-results.json).

## Findings

### F01 — High: the Osiris baseline does not match its cited source image

The HIF design is described as the Osiris baseline, but several values match corrupted extraction text rather than the printed table. The decisive source is [the operating-parameters table image](../../knowledge/sources/energy_from_inertial_fusion/images/page_007_table_0.png). Its Osiris column is visually unambiguous.

| Quantity | Model | Printed Osiris value | Relative discrepancy | Verdict | Model location |
|---|---:|---:|---:|---|---|
| Beam energy | 5.0 MJ | 5.0 MJ | 0% | PASS | `models/designs/hif_ife/hif_plant.sysml:31` |
| Gain | 80 | 87 | −8.05% | FAIL | `hif_plant.sysml:87` |
| Repetition rate | 3.5 Hz | 4.6 Hz | −23.91% | FAIL | `hif_plant.sysml:33`, `:78` |
| Driver efficiency | 35% | 28% | +25.00% | FAIL | `models/designs/hif_ife/hif_driver.sysml:80` |
| Thermal efficiency | 43% | 45% | −4.44% | WARN | `hif_plant.sysml:100` |
| Thermal power | 2,054 MW | 2,504 MW | −17.97% | FAIL | `hif_plant.sysml:154` |
| Net electric power | 1,000 MW | 1,000 MW | 0% | PASS | `hif_plant.sysml:166` |

The same corrupted extraction reports yield 412 MJ instead of 432 MJ and COE 3.6 instead of 5.6 cents/kWh. The model’s gain rationale repeats 412. The printed numbers have ordinary rounding differences of their own: 432/5 = 86.4 rather than exactly 87. That is distinct from the much larger transcription errors above.

**Consequence:** driver cost, fusion output, parasitic power, Meier reactor cost, and both electricity-cost interpretations start from an incorrectly identified reference machine. Passing the existing broad cost-range checks does not repair this.

**Recommendation:** rebuild one image-verified Osiris parameter record, distinguish historical source facts from later assumptions such as 90% availability, and rerun the two cost chains. Do not simply replace the literals independently; F02 must also be resolved so the quantities remain consistent.

### F02 — High: HIF representations of the same machine are disconnected

`models/designs/hif_ife/hif_driver.sysml:80-83` fixes efficiency, bank energy, and lifetime while `beam_energy_mj` separately drives Meier’s cost. Bank energy should follow beam energy divided by efficiency under the model’s own stated convention, but it is held at 14.286 MJ. Likewise, `pulse_rate_ref` controls driver procurement while plant `frequency` controls shots and output. The two rates are independently settable.

At the baseline the energy mismatch is only rounding: 0.35 × 14.286 MJ = 5.0001 MJ. During a beam-energy sweep it becomes structural. Doubling beam energy from 5 to 10 MJ leaves Hawker’s fusion energy unchanged, while its driver capital term decreases by about 21.05%: Meier’s cost rises by 1.57895×, but gamma divides that cost by twice the beam-derived bank energy and Hawker multiplies it by the unchanged bank-energy literal. The generation test explicitly expects beam energy to reach only the Meier calc (`tests/models/test_model_family_spines.py:93-96`), so this test preserves the missing physical dependency.

The power representations also disagree at the baseline. Hawker’s present inputs imply **592.312 MW net**, while Meier’s denominator uses a separately fixed **1,000 MW** (`models/designs/hif_ife/hif_plant.sysml:151-175`). These can be two historical calculation cases, but they are not independent validations of one consistently modeled operating point.

**Recommendation:** choose one authoritative beam energy, efficiency, and operating repetition rate; derive bank energy and relevant power quantities. If the Meier reference case intentionally remains separate, model it as a named reference case with explicit differences rather than a second output of the same apparent plant state.

### F03 — High: IFE viability does not enforce positive net output

`models/library/analyses/fusion_cycle.sysml:29-51` checks only `eta × gain >= 10`. Hawker’s implemented net power requires `eta × gain × blanket_multiplier × thermal_efficiency > 2` (`models/library/analyses/ife_lcoe.sysml:64-65`). The former does not imply the latter over the library’s own stated ranges.

**Counterexample:** efficiency 0.1, gain 100, blanket multiplier 0.6, and thermal efficiency 0.3. The viability assertion passes at 10. The cycle gain is 1.8, so net power is **−0.2 times bank-energy input power**. LCOE can then be negative or otherwise misleading rather than rejected as a non-generating plant.

There is also an output-basis mismatch: `recirculating_fraction` reports driver-only recirculation, while Hawker subtracts driver plus an equal cooling allowance. At the current HIF point these are **7.2223%** and **14.4446%**. The library calc documents the driver-only meaning, but the plant output name loses it.

**Recommendation:** assert positive net electric power on the actual LCOE power balance; retain the eta-gain rule as a separate heuristic. Expose gross, driver, other parasitic, and net powers from one calculation, and distinguish driver-only from total recirculation.

### F04 — High: installed heating is charged as continuously operating heating

The new sustainment pair correctly checks `0 <= required heating <= installed heating`. However, the electricity balance reads `heat.p_coupled` and `heat.p_wallplug_total` (`models/designs/generic_mfe/mfe_plant.sysml:481-504`), both computed from installed wall-plug power. It does not read the computed operating requirement. The capacity check is at `models/designs/stellarator_09/stellarator_plant.sysml:1342-1361`.

At the baseline the difference is small: required 49.0796 MW versus 50 MW installed, leaving a **0.9204 MW plasma-heating surplus** if all modeled heating is actually applied. At a feasible point requiring zero auxiliary heating, the current 100 MW electrical draw and 50 MW coupled input remain in the power balance. With the other modeled loads held, turning off that unused heating increases net output by **83.8495 MW**, including the model’s thermal and subsystem-power effects. This is an algebraic counterfactual, not a rerun or corrected LCOE claim.

**Consequence:** a point may satisfy the heating-capacity inequalities while the power flow priced by LCOE is not the power flow that holds that point. Heating-capacity sweeps also impose a fictitious continuous operating penalty on installed reserve capacity.

**Recommendation:** separate installed capacity, startup/access operation, and sustained operating demand. Cost the installed system; compute operating electrical draw from the sustained demand and the relevant efficiency or part-load model. Keep capacity and burn-control constraints on the same operating state.

### F05 — Medium: removable financial singularities were not carried through

`models/library/analyses/mfe_account_costs.sysml:724-726` divides by `interest_rate - inflation_rate_in`. At both rates equal to 0.02, the generated implementation raises `ZeroDivisionError`. The cited upstream function explicitly handles this limit (`/home/reid/1cfe/1costingfe/src/costingfe/layers/economics.py:41-46`). The lost branch is therefore a concrete source-porting error.

For a $1 million annual stream, 30 operating years, and eight construction years, the correct continuous limit is **$1,538,661.774/year** after levelization. The probe reproduces the exception and independently evaluates that limit.

Zero discount also divides by zero in the generic DCF core (`models/library/analyses/mfe_lcoe_dcf.sysml:49-50`), IFE PV factors (`ife_lcoe.sysml:108-120`), IDC (`mfe_account_costs.sysml:665-667`), and replacement annuity implementation. Some are inherited limitations rather than lost upstream branches. For the probe’s $1 billion capital, $10 million annual cost, 1 GW, 85% availability, and 30 years, the zero-discount LCOE limit is **$5.81968/MWh**.

**Recommendation:** implement the equal-rate and zero-rate limits, with numerically stable nearby evaluation. Validate positive lifetime and the chosen construction-time domain. Add tests at and close to the singularities, not just the baseline rates.

### F06 — High: machine major radius has two independent owners

Stellaris sets both `magnet.R0 = 12.7` and plant `R = 12.7` (`models/designs/stellarator_09/stellarator_plant.sysml:139`, `:525`). Geometry and sustainment use plant `R`; field, winding length, stored magnetic energy, and peak field use magnet `R0` (`models/designs/generic_mfe/mfe_plant.sysml:136-140`, `:244`, `:273-327`). There is no binding or equality assertion joining them.

This puts one intended machine invariant in study orchestration rather than in the model. Changing only plant radius changes volume and radial-build costs without the corresponding field/coil-length response. Changing only magnet radius creates the converse inconsistency. The study adapter explicitly exposes both entries (`exploration/stellarator_e2e/studies/oracle_entry.py:34-40`).

There is a related oracle defect: `_sustainment` reads `p["magnet_R0"]` (`exploration/stellarator_e2e/verify_stellaris.py:111`), whereas the SysML sustainment calc binds plant `R`. Existing coordinated radius studies conceal this discrepancy.

**Recommendation:** bind both domains to one plant geometry value. If different radii are physically intended, name their reference surfaces and model the relation. Test an ordinary public radius mutation end to end without a study-specific tie.

### F07 — High: model-domain validity is not enforced

The peak-field shape contains `R / (R - a_coil)` (`models/library/analyses/mfe_plasma_scaling.sysml:480-489`). No assertion requires positive inboard clearance. With R = 12.7 m and coil-centre radius 13 m, the generated calc returns **−792.65 T**; its upper-bound-only field test would accept that number as below 24.9 T. At equality the calculation divides by zero. This counterexample concerns the field calc and its paired constraint; it is not a claim that the complete plant successfully executes that point.

Similar missing domains include nonnegative layer thicknesses, positive radii/current density, efficiencies in their physical ranges, `0 < T_cold < T_ambient`, positive heat capacity factors, and nonnegative powers. Several equations can emit finite but nonsensical values before any existing physical fence notices. Having every authored constraint executable does not establish that all necessary constraints were authored.

**Recommendation:** distinguish invalid model inputs from physically evaluated but infeasible designs. Validate algebraic domains before numerical execution and assert geometric/physical compatibility at the owning subsystem. Do not rely solely on the range of a particular study grid.

### F08 — High: the CAS interface is only partly realized

The standard interface declares `capital_cost` and `cas_code` (`models/library/foundation/costed_component.sysml:17-18`). None of the current SysML files assigns `cas_code`. The shared CAS types also leave account names and many scope values unspecified (`models/library/cost_structure/cas_hierarchy.sysml:19-20`). A title containing an account number is not a populated account identifier.

IFE is the clearest functional gap. Its driver and target factory inherit costed types, but no usage binds their `capital_cost`. The chamber’s blanket, shield, and structure have no costs either (`models/designs/generic_ife/ife_subsystems.sysml:123-190`). Hawker’s private cost expression computes a total independently of those parts (`models/library/analyses/ife_lcoe.sysml:85-98`). Traversing the advertised costed-component interface cannot recover the IFE investment or reconcile it to LCOE.

MFE binds many component costs correctly, but newer accounts such as remote handling, coolant, CAS28, owner costs, supplementary costs, and indirect costs are calc/scalar features rather than consistently typed cost-bearing account parts (`models/designs/generic_mfe/mfe_plant.sysml:707-889`). Adding a component does not automatically place it in the explicit rollup lists at `:689`, `:795`, and `:806`.

There are two accounting dialects: shared types use ARIES’s CAS20 land and CAS90 indirect categories; the MFE scalar spine uses 1costingFE’s CAS10 preconstruction, CAS20 direct aggregate, CAS30 indirect, and annualized CAS90. The 25/26 heat-rejection/miscellaneous swap is already explicitly disclosed in `mfe_subsystems.sysml:17-21` and is not itself an undisclosed error. The broader dialect mapping is not represented in the account interface.

**Recommendation:** populate stable account identifiers and make dialect/version explicit. Ensure each model’s accounted capital and annual costs reconcile to its LCOE numerator. Either adopt cost-bearing account parts consistently or deliberately revise the promised interface to support a uniform account ledger. Preserve distinct physical parts and accounting classifications rather than assuming they always form the same tree.

### F09 — High: cross-concept LCOEs do not share a comparison basis

HIF combines Meier’s 1988-dollar driver/reactor costs, later Hawker assumptions with “generic” year-dollars, and an Osiris source table explicitly labeled 1992 cents/kWh (`models/designs/hif_ife/hif_driver.sysml:17-20`; `hif_plant.sysml:43-50`, `:131-145`). The MFE model supplies dollar-valued 1costingFE inputs but no common machine-readable currency year or common comparison-case finance record.

The financial methods also differ: Meier combines fixed charge and O&M rates, IFE discounts evenly spread construction cash flows, and the MFE headline uses a midpoint IDC approximation with already levelized operating costs. The MFE comparison channel deliberately uses a different IDC convention. These methods are documented, and the MFE design correctly keeps reported CAS60 out of the headline capital base; I found no additional IDC double count there.

**Consequence:** identical `$ / MWh` labels do not establish comparability. Dollar-year normalization, operating life, real versus nominal discount/escalation treatment, construction schedule, and cost scope can move rankings independently of technology.

**Recommendation:** retain historical reproduction cases, then define a separate normalized comparison case with currency/base year, financing convention, plant life, availability treatment, and included accounts. Carry these fields with exported results. Do not convert historical cents/kWh to current dollars by unit conversion alone.

### F10 — Medium: the generic MFE plant has become a stellarator/ECRH template

The plant calls itself confinement-agnostic (`models/designs/generic_mfe/mfe_plant.sysml:18`) but unconditionally instantiates an ISS04/rotational-transform sustainment calculation (`:209-257`). A tokamak does not acquire a correct confinement/current-drive closure merely by providing values for `iota_23` and `f_ren`. Selecting the DT fusion calc’s positive-reactivity 0D bypass does not bypass this separate sustainment calculation.

The heating mix is also inconsistent outside ECRH-only usage. The one heating chain’s delivered power always enters the ECRH cost slot, while NBI/ICRF/LHCD powers only enter separate capital terms (`:604-619`). Those additional powers do not feed the operating power chain automatically.

**Recommendation:** retain common plant/cost interfaces but specialize or compose confinement and heating-method analyses. A new concept should supply the physics strategy it actually uses, rather than fill irrelevant stellarator inputs. Keep model-family names honest about supported scope until that separation exists.

### F11 — Medium: multiple modules are advertised numerically but not modeled consistently

`n_mod` is a public `Real` defaulting to one (`models/designs/generic_mfe/mfe_plant.sysml:624-625`). It reaches BOP, some tail costs, fuel, replacement, and the 1cfe-form energy denominator. It does not reach building/preconstruction/O&M calcs, which retain their own default module counts (`:654-679`), and the headline DCF denominator has no module multiplier (`:1010-1018`). Reactor-equipment capital is also not consistently replicated.

The source comments disclose a single-module demo. That makes the present baseline valid on this issue, but changing the exported count cannot produce a consistent multi-module plant.

**Recommendation:** enforce `n_mod = 1` as the current supported domain, or complete plant-total versus per-module accounting and test two modules. If counts are represented as `Real` for the execution interface, enforce positive integrality explicitly.

### F12 — High: component life changes cost but not downtime

CAS72 computes a fluence-driven replacement interval and a discrete number of replacements (`models/library/analyses/mfe_account_costs.sysml:796-887`). The plant binds that cost, but availability remains the independent 0.85 literal (`models/designs/stellarator_09/stellarator_plant.sysml:1117`). No replacement duration, maintenance overlap, access sequence, or unplanned outage model connects the schedule to annual energy.

**Consequence:** a design with more frequent in-vessel replacement pays for replacement hardware but retains identical availability. This can favor high damage rates or aggressive operating points for an incomplete reason. The 0.5-FPY lifetime clipping floor is also a numerical/source convention, not proof that a component survives that long under arbitrary load.

**Status:** already recognized by the lifetime/availability prework; not a new implementation regression. **Recommendation:** connect scheduled maintenance to availability, or quantify an availability bound tied to replacement count and duration. Keep scheduled cost, outage cost, and plant life on one calendar.

### F13 — Medium: the thermal system cannot substantiate efficiency/pumping tradeoffs

The model holds primary pumping at 195 MW, conversion efficiency at 0.333, and pumping-heat recovery at 0.5 (`models/designs/stellarator_09/stellarator_plant.sysml:779-808`). There is no pressure-drop, mass-flow, temperature-rise, or cycle calculation joining these values. Heat-rejection capital scales with total thermal power, not an explicitly calculated rejected-heat duty (`models/designs/generic_mfe/mfe_plant.sysml:636-639`). This follows the costing source; it is not a transcription error.

Changing thermal efficiency can therefore improve LCOE without buying the cycle, materials, cooling, or operating conditions that make the efficiency possible. Changing blanket geometry or fusion output does not make pumping respond. The source-based primary-loop/cycle prework already identifies this limitation.

**Recommendation:** introduce the smallest sourced thermal/pumping closure needed for the intended studies. Until then, present efficiency and pumping sweeps as conditional assumptions, with their coupling and plausible envelope stated. Cost and constrain heat rejection against a defined heat balance if it is to become a design lever.

### F14 — Medium: magnet feasibility remains a set of calibrated screening checks

The current revision **does include WI-044**: coil bore changes conductor peak field, magnetic stored energy, and casing mass. The printed source forms were checked. It would be incorrect to report the earlier “minor radius has no magnet consequence” finding as current.

Remaining limitations matter to optimization. Winding-pack area is `I/j_wp`, while conductor procurement is proportional to current × winding length at a held $/kA-m (`models/library/analyses/mfe_magnet_field.sysml:113-118`; `mfe_magnet_cost.sysml:70-109`). There is no conductor critical-current surface relating field, temperature, strain, orientation, tape fraction, and operating margin. Field, stress, and axial strain ceilings cannot substitute for that relation. Varying `j_wp` or cryogenic temperature therefore does not establish that the selected conductor can carry the current.

The coil-geometry forms hold configuration coefficients; coil count and geometry changes are not automatically new valid equilibria. The documented peak-field approximation drops the source’s winding-pack term because its coefficient is unprinted (`models/library/analyses/mfe_plasma_scaling.sysml:419-462`). The winding length remains proportional only to major radius, and casing mass is anchored to the disclosed 63-tonne cast-part floor. Winding-pack size and radial-build coil thickness are independently specified; there is no check that the sized pack and casing fit the chosen coil envelope. These are incomplete geometry/engineering relations, not exact coil engineering.

**Recommendation:** bound studies by the calibrated configuration and report the casing lower bound. Add a sourced conductor operating-margin relation when current-density or temperature studies require it. Distinguish a satisfied scalar screening check from validated coil design.

### F15 — Medium: breeding and exhaust limits are not derived from the design being priced

TBR is held at 1.074 and compared with 1.05 (`models/designs/stellarator_09/stellarator_plant.sysml:1295-1319`). It does not change when blanket thickness, material inventory, standoff, or penetrations change. The shield cost and cryogenic nuclear-heating input likewise do not form a neutron-transport closure. Thinner shielding can save volume/cost without increasing the nuclear heating of the coils in the model.

The divertor cost follows thermal power, but there is no exhaust-power-to-area-to-heat-flux limit. Fuel cost follows reaction rate and recovery, but no tritium inventory, processing time, startup stock, or breeding-inventory balance establishes fuel-cycle operability (`models/library/analyses/mfe_account_costs.sysml:732-792`). The sole generic TBR floor is a screening condition, not a dynamic self-sufficiency proof.

**Status:** these are known breadth gaps, consistent with the pending breadth prework. **Recommendation:** keep the held TBR as a reference fact and give geometry-changing studies an explicit validity limit. Add bounded exhaust, shielding/heating, and fuel-inventory relations before using those quantities to rank designs as buildable.

### F16 — Medium: verification is strongest at translation, weakest at independent physics

The oracle describes itself as mirroring the model line for line and uses the same discretization, coefficients, guards, and fixed-point iteration (`exploration/stellarator_e2e/verify_stellaris.py:1-17`, `:47-53`). This is valuable translation/regression verification. It cannot detect a source error copied into both versions, as F01 illustrates in the IFE verification scripts. It also cannot establish that the radiation fit or a calibrated geometry scaling is valid outside its source domain. The standalone `scripts/verify_ife_lcoe.py` checks a separate hardcoded HIF example and prints 250 MW, rather than the current authored plant's 592 MW; its PASS should not be treated as current-instance validation.

The CLI’s L4 “100% executable share” measures authored constraints, not engineering coverage. L5 “100% documentation” measures doc presence, not citation resolution or factual accuracy. L2 reports failure on literal bindings that are deliberately sourced. L6 rejects supported EXPOSE and aggregation forms even while family generation and execution tests pass. These mismatched meanings should not be collapsed into one green/red quality claim.

One concrete inherited numerical concern is the piecewise tungsten radiation fit: immediately below 0.1 keV it approaches `5e-30 W·m³`, while at 0.1 keV it becomes `1.5e-31 × sqrt(0.1)`, a drop by about 105× (`exploration/stellarator_e2e/verify_stellaris.py:66-74`; upstream `radiation.py:83-96`). There are other branch jumps. This is faithfully copied source behavior, not a transcription defect, but its contribution to integrated radiation and temperature derivatives deserves an independent accuracy/convergence check before optimizing across those profile temperatures.

**Recommendation:** keep translation tests, add independent identities and source-image baselines, and add numerical convergence/alternative quadrature checks for manual integrals. Establish finite domains and boundary cases per calc. Separate syntax, execution conformance, numerical analysis, source validation, and engineering coverage in the audit status. Map known L6 residue to tested exceptions rather than ignoring all residue.

### F17 — Medium: the traceability chain contains broken and misleading references

Confirmed missing paths include `work/active/WI-006_ife-cost-structure-library/spec.md` in `models/library/foundation/economic_parameter.sysml:9`, `work/active/WI-035_magnet-closure/design.md` in `models/library/analyses/mfe_magnet_cost.sysml:187`, and the archived WI-041 design path in `models/designs/stellarator_09/stellarator_plant.sysml:1285`. These are live citations invalidated by archiving. The report’s [path census](20260907-fusion-model-audit-evidence/path-census.json) is a lexical aid; split-line and shorthand references need human interpretation, so not every `exists: false` row is a confirmed broken citation.

Other live comments cite only `Hawker 2020 Table 1` or `stellaris-design-details.md`, not MR-4’s resolvable paths. The parameter ranges/correlations are actually in Hawker Table 3. The conductor strain binding still says the Pierro 20 K measurements are paywalled and queued (`stellarator_plant.sysml:267`), while `knowledge/SOURCE_INDEX.md` now registers the paper and its measurements. `modeling_project/REQUIREMENTS.md` names `scripts/trace_audit.py` as enforcement, but that file is absent.

**Recommendation:** repair durable citation targets during archive operations, resolve shorthand citations in live models, and update stale source-status statements. Validate path resolution and source-image fidelity separately from doc presence. Do not silently treat a known source contradiction as a new parameter assumption.

### F18 — Medium: reusable definitions and metadata are not consistently reusable

Shared IFE and MFE subsystem definitions live under `models/designs/generic_*`, including blanket, turbine, electric plant, and target factory. They are reused as types, but their placement contradicts the project’s stated definition/library boundary. The MFE magnet exception was already corrected by AD-007; the same reasoning applies to the remaining shared definitions.

Some reusable types encode design values as fixed bindings. For example `models/designs/hif_ife/hif_driver.sysml:80-83` fixes efficiency and bank energy in the driver definition. A generated package may expose a runtime parameter, but that is not the same as legal SysML specialization overriding a fixed binding. SysML 2.0 distinguishes fixed values, which remain binding assertions, from overridable defaults (Part 1, §§7.13.1 and 7.13.4, [OMG specification](https://www.omg.org/spec/SysML/2.0/Language/PDF)). This is a reuse risk, not a claim that the current baseline fails parsing.

The `Economic Parameter` pattern carries min/max/value/Pearson correlation, but the executable plants bind independent plain scalars and do not consume those bundles. It also omits the linear/log sampling choice present in Hawker Table 3. `driver_energy` labels the 0.5–50 MJ range as bank energy, whereas Table 3 calls it target energy (`models/library/cost_structure/ife_cost_parameters.sysml:108-119`; source `output.md:470`). That metadata should not be used as a source-faithful Monte Carlo specification without reconciling the energy convention.

**Recommendation:** put shared definitions in the library, instance facts in designs, and overridable reference choices in actual defaults. Connect metadata to public parameter identities and preserve distribution semantics. Treat Pearson coefficients as properties of the source’s sampled experiment, not universal physical sensitivities of every HIF design.

### F19 — Medium: the radiation equations in SysML prose are dimensionally wrong

The radiation block in `models/library/analyses/mfe_plasma_sustainment.sysml:76-84` labels the bremsstrahlung and line-radiation expressions as MW but omits the `1e-6` conversion. The executable implementation correctly applies that factor to both terms (`exploration/stellarator_e2e/generated/handwritten/mfe_plasma_sustainment/plasma_sustainment_impl.py:250-258`). The tungsten cooling curve is explicitly in W·m³ in the cited upstream source.

This does **not** mean executed radiation power is a million times wrong. It means the model-resident mathematical contract and the normative handwritten implementation disagree on units. That matters because another implementation regenerated from the written equations could be wrong while appearing faithful.

**Recommendation:** amend the displayed equations and unit annotations to match the implementation. Add a dimensional worked example for each manual calculation. AD-001 makes this documentation part of the dimensional safety mechanism.

### F20 — Low: smaller inconsistencies should be cleaned up with nearby work

- IFE counts shots using 365.25 days but electrical energy using 365 days (`models/library/analyses/ife_lcoe.sysml:71-74`, `:101`). Hawker Eq. 2.9 uses 365 days. This overcounts shot-related annual costs by **0.0685%** relative to the model’s energy year. It is below the audit’s 1% numerical threshold but avoidable.
- MFE power balance uses the full `3.52/17.58` energy split while wall loading and sustainment default to 0.2002. The discrepancy is small, and the wall calibration cancels its own chosen fraction, but a single fuel-energy convention would avoid drift.
- The plasma-geometry comment says the stellarator shape factor is below one, while this instance uses 1.0031567 (`models/library/analyses/mfe_plasma_scaling.sysml:12-18`; `models/designs/stellarator_09/stellarator_plant.sysml:534`). The numeric calibration need not be wrong; the universal wording is.
- `models/README.md` omits the MFE library and design catalog and says tokamak work would revive the archive. Several plant/runner headers still state two or six constraints although the current stellarator package evaluates ten.

## What checked out

- **Power balance algebra:** in the stated no-direct-conversion regime, neutron/alpha splitting, recovered heating/pump heat, gross electric power, parasitic sums, engineering Q, and net power are algebraically consistent. F04 concerns which heating state is supplied, not the subtraction itself.
- **Profile integration:** the implemented fuel-temperature profiles use the appropriate `2ρ dρ` effective-radius volume weight; line-averaged density uses `dρ`. Electron quasi-neutrality, the species pressure integral, `W = 3pV/2`, and beta share one pressure result. Substituting `P = W/τ` into ISS04 correctly yields `τ = (C W^-0.61)^(1/0.39)`.
- **Radial build:** at the circular baseline, cumulative radii and toroidal shell differences are coherent. For general elongation, the surface-area expression is a scaling approximation, not the exact perimeter of an elliptical section; its reusable domain should say so.
- **Magnet arithmetic:** ampere-metre procurement units, winding-pack area conversion from A/mm², field/current dependence, and the anchored WI-044 inductance scaling have coherent units. The source image confirms the bore factor and inductance form; the omitted configuration term is disclosed.
- **DCF:** away from the singularities in F05, the IFE PV factors reproduce end-of-year sums for constant streams. The MFE CRF and disclosed midpoint IDC formula are coherent. The reported alternative IDC account is excluded from the headline capital base as documented.
- **Replacement:** current CAS72 excludes a replacement at the end of operating life, discounts discrete events, and preserves the source’s clipping guards. Baseline and three guard cases pass. This verifies the calculation, not the missing outage model.
- **Meier driver formula:** the image confirms `(0.32 + 0.088 E_d)(1.25 + 0.05 N_c)(1 + 0.0088(ν−5))` billion dollars. At 5 MJ, one chamber, and 5 Hz it gives **$0.988 billion**. The formula is correct; the case identification and linked inputs are not.

## Validation run results

| Check | Result | Interpretation |
|---|---|---|
| `pytest tests/models -q` | **48 passed, 13 skipped** | Includes family generation, snapshot equivalence, twin equality, and mutation wiring. Skips are not counted as verified requirements. |
| IFE public generation/execution and occurrence mutation suites | **20 passed** | Ran with actual installed package root and TEAx checkout configured; confirms live/snapshot execution and current public mutations. |
| Stellarator single-pass runner | **PASS** | Ten modeled verdicts satisfied; 30 selected numeric oracle comparisons at relative tolerance `1e-9`, headline anchors, CAS72 guards, and pressure/beta identity checks passed. Its “BIT-EXACT” log label is stronger than the actual tolerance test. |
| `scripts/verify_ife_lcoe.py` | **PASS** | Formula mirror/range check; does not validate Osiris source values. |
| `scripts/verify_hif_costs.py` | **PASS** | Broad reference/range checks; does not catch F01/F02. |
| Retained audit probe | **Reproduced F03–F07 counterexamples** | Direct generated calls for the two financial exceptions and negative peak field; explicit IFE/power-flow arithmetic. |

| CLI level | Canonical tree | IFE family | MFE family |
|---|---|---|---|
| L1 syntax | PASS, 25 files | PASS, 11 files | PASS, 17 files |
| L2 structure | FAIL label, 12 literal-binding warnings | FAIL label, 2 warnings | FAIL label, 10 warnings |
| L3 dataflow | PASS, no cycles | PASS | PASS |
| L4 constraint coverage | 11/11 admitted numerical | 1/1 | 10/10 |
| L5 documentation | 96/96 documented | 28/28 | 79/79 |
| L6 architecture/readiness | 236 issues | 26 issues | 210 issues |

L2 reports zero unbound inputs, zero undefined bindings, and zero self-bindings. L6 includes incomplete definition-level values and unsupported dotted EXPOSE expressions that the tested family routes do handle. The report does not classify all 236 diagnostics as broken runtime connections. The CLI exit code remains nonzero, so “all six levels pass” would also be inaccurate.

The first test attempts encountered the sandbox’s read-only uv cache and missing test environment variables. Reruns used `UV_CACHE_DIR=/tmp/fusion-audit-uv`, `--no-sync`, the installed site-packages directory as `STOP_PARSER_WHEEL_TARGET`, and the actual TEAx checkout on `PYTHONPATH`. No dependencies were installed or changed. Historical study sweeps and their publication tests were not rerun; their recorded results are not presented as fresh audit execution.

## Project requirements and decisions

| Requirement | Audit assessment |
|---|---|
| MR-1 CAS decomposition | Partial: good MFE arithmetic hierarchy; IFE costs bypass populated accounts; account dialects need mapping. F08. |
| MR-2 costed interface | Not satisfied throughout: unpopulated IFE capital attributes and scalar-only MFE accounts. F08. |
| MR-3 library/design separation | Partial: calculations are in the library; many shared part definitions remain in designs and the generic MFE plant embeds a particular physics family. F10/F18. |
| MR-4 quantitative citations | Not satisfied throughout: F01 source mismatches and F17 missing/stale paths. Doc presence is not evidence of numeric accuracy. |
| MR-5 standard outputs | Intent remains incomplete: currency/finance metadata and comparable CAS costs are absent. F08/F09. |
| MR-6 documented patterns | Substantial evidence exists in agentic-mbse patterns and the migration ledger; implementation/guidance divergence remains. F16/F18. |
| PR-1 taxonomy first | Historical sequencing not re-certified by this project health audit; taxonomy work artifacts exist. |
| PR-2 shared/divergent concept analysis | Historical analysis exists; current reuse boundaries still need correction. F10/F18. |
| PR-3 patterns before production | Patterns and retained construct tests exist; chronological compliance for every historical work item was not re-audited. |
| PR-4 iterative feedback | Evident in WI-041/042/043/044 and their source-driven amendments; not a numerical pass/fail rule. |
| PR-5 committed artifacts | Model/test/evidence chain exists at the audit pin; durable citation repair is incomplete. F17. |

| Architecture decision | Audit assessment |
|---|---|
| AD-001 plain Real | Followed; units therefore require explicit checking. F19 is a failure of that mitigation. |
| AD-002 economic metadata | Type exists; its connection to execution and distributions is incomplete. F18. |
| AD-003 closed-form IFE DCF | Followed; constant-stream algebra correct away from zero discount. |
| AD-004 library directories | Followed for library contents; reusable types still misplaced under designs. |
| AD-005 typed CAS specializations | Types exist; identity/classification and account coverage are incomplete. F08. |
| AD-006 pure calculations separate from parameter bundles | Followed structurally; metadata-to-runtime traceability needs completion. |
| AD-007 magnet definition in library | Followed. |

SV-001/003/004/005/006/007/009/010/015 are supported in their narrow structural or dimensional senses, subject to the findings above. SV-008/012/013/014 scripts reran successfully. SV-011’s source-fidelity interpretation is challenged by F01. SV-002’s “classification” claim is stronger than the actual populated CAS metadata. Recent MFE baseline/identity assertions are supported by the single runner and family tests; historical off-design SV rows retain their existing evidence rather than receiving a new audit certification. The validation registry was not rewritten.

## Recommended order of work

1. Correct the Osiris source record and the HIF physical dependency chain together. Add a negative-net-power IFE rejection case.
2. Separate installed heating capacity from operating heating in the MFE power balance. Give major radius one owner and enforce basic model domains.
3. Repair financial limit cases and add independent source/identity tests. Repair live citations at the same time as the affected model changes.
4. Make account and monetary comparison contracts explicit before publishing cross-concept rankings.
5. Use the existing thermal, lifetime/availability, and breadth prework to close the engineering dependencies needed by the next studies. Preserve declared lower bounds and calibration limits until evidence replaces them.

## Evidence index

- [Reproduction script](20260907-fusion-model-audit-evidence/probe.py), [results and model hashes](20260907-fusion-model-audit-evidence/probe-results.json), [numeric-expression census](20260907-fusion-model-audit-evidence/numeric-census.json), and [candidate source-path census](20260907-fusion-model-audit-evidence/path-census.json).
- [Canonical validator output](20260907-fusion-model-audit-evidence/validation-canonical.txt), [IFE validator output](20260907-fusion-model-audit-evidence/validation-ife.txt), and [MFE validator output](20260907-fusion-model-audit-evidence/validation-mfe.txt).
- [Model tests](20260907-fusion-model-audit-evidence/tests-models.txt), [IFE execution/mutation tests](20260907-fusion-model-audit-evidence/tests-ife-execution.txt), [stellarator runner](20260907-fusion-model-audit-evidence/stellarator-run.txt), [IFE mirror check](20260907-fusion-model-audit-evidence/ife-mirror.txt), and [HIF mirror check](20260907-fusion-model-audit-evidence/hif-mirror.txt).

Every current model file is listed with a content hash in `probe-results.json`. All analysis files were reviewed for their expressions, bindings, dimensional conventions, and applicability; part and parameter files were reviewed for specialization, cost coverage, source provenance, and extension behavior. No result in this report depends on reading the quarantined comparison target.
