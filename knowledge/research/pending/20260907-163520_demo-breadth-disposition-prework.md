---
date: 2026-09-07
researcher: Codex breadth research agent
topic: Stellarator demo breadth dispositions before comparison
tags: [stellarator, clean-room, tritium, divertor, vacuum, buildings, uncertainty]
research_type: domain-and-model
status: pending-review
---

# Breadth dispositions: fuel, exhaust, vacuum, buildings, and uncertainty

## Scope and authority

This draft addresses recommendation 5 in `.project/reports/2026-09-07-1549-status-report.md`. Every proposed treatment, equation specialization, acceptance test, effort estimate, and comparison disposition below is `[AGENT]`. These proposals neither change the frozen rubric nor certify a score, and they do not imply owner acceptance of limitations. The parent report owns the comparison contract, integrated heat ledger, primary loop, lifetime closure, and implementation sequencing.

The comparison dispositions are evidence labels, not waivers of the ratified Anchor-B contract. Under `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md:119`, B-2 still requires all three structural correspondences and fails when a first-order subsystem correspondence is absent. B-3/B-4 still require the applicable derived-quantity and component-cost comparisons within their bands; a missing or not-comparable required channel cannot count as a pass or silently leave the assessed set. Only the existing C220107 treatment and sizing-axis reallocation have recorded exclusions. Any further acceptance exception would require an explicit owner amendment. R10's lack of a pre-named B-2 row does not exempt a first-order fuel-cycle subsystem from B-2's actual completeness test.

This was a model-facing clean-room session. It read `knowledge/holdout/aries-cs/PROTOCOL.md` only inside the quarantine, no sealed PDFs or barred artifacts. Source discovery used named admissible Stellaris materials and institution-specific primary-source searches. No authors were contacted and no production model, registry, grading, or PM state was edited. Model inspection was at `75f46dc8d8b900a27b9a823242528eb1a1a206b6`.

## Findings that change the work

- A useful fuel-cycle calculation is available without claiming computed neutronics. Compute burn, throughput, working inventory, startup demand, and required breeding separately; keep achieved TBR a source-conditioned input until geometry-dependent neutronics exists.
- Existing fuel-cost assumptions contain a conditional consistency warning. Interpreting the held 99% recovery as physical tritium recovery at 5% single-pass burn requires a breeding ratio of at least 1.19 before decay and other losses. The model's 1.074 TBR would not cover that interpretation. However, the existing recovery factor prices blended D/Li feedstock, so this is a parameter-semantics conflict to resolve, not proof that the present physical design cannot fuel itself.
- The clean Stellaris paper supplies a usable divertor reference with explicit limitations. Its radiated fraction, transport cases, and peak target fluxes are verified against raw PDF pages 14–15. Its heat-load calculation does not establish recycling, ash removal, neutral compression, or transient tolerance.
- Vacuum has a credible forward-calculation path once fuel throughput is available. The pressure must be the gas pressure at the specified exhaust boundary, and throughput counts gas molecules after recombination. Neither vessel volume nor coolant pumping power supplies that quantity.
- Buildings can remain a cost proxy only with an explicit comparison limitation. A new geometry-scaled proxy would still need independent enclosure and handling assumptions; multiplying the current lump by reactor volume would not establish layout depth.
- Deterministic shared-driver scenarios can supply an honest uncertainty envelope now. They do not support probability-of-success, confidence-level, or P90 language. AACE estimate class is a claim about deliverable maturity, not a way to manufacture a numerical error bar.

## Current seams and minimum credible treatment

### Tritium adequacy and fuel cycle: R2c and R10

The live model holds `tbr=1.074` and compares it to a held `tbr_floor=1.05` in `models/designs/stellarator_09/stellarator_plant.sysml:1233` and `:1258`. Its annual fuel calculation converts fusion energy to reactions and multiplies a D-plus-Li-6 price by a recovery correction in `models/library/analyses/mfe_account_costs.sysml:734`. The plant's `burn_fraction=0.05` and `fuel_recovery=0.99` bindings are at `stellarator_plant.sysml:1101`. Fuel handling capital scales with net electric power at `:1009`, startup fuel is a power-scaled cost provision at `:1024`, and processing electrical power is held at `:793`. None of those is a tritium stock or physical processing flow.

The primary-source distinction is straightforward: ITER recycles unconsumed fuel and exhausts helium and impurities through a tritium plant; it identifies exhaust processing, isotope separation, storage/delivery, detritiation, and analysis functions. Its published burn fraction is an ITER design fact, not a stellarator default. [ITER Fuelling, Fuel cycle and Tritium Plant](https://www.iter.org/machine/supporting-systems/fuelling), accessed 2026-09-07.

The existing Stellaris achieved-TBR source is available and verified. Raw PDF page 19 reports `1.1070 ± 0.0002` from its transport calculation including its maintenance and conceptual divertor geometry, then reduces the result by 3% for heating ports to obtain `1.074`. The statistical tally error is not a total model uncertainty or an uncertainty on geometry transfer. Source: registered KIT raw PDF `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`, p. 19; text locator `knowledge/concept_research/09-qi-stellarator-hts/iter-01/sources/stellaris-design-details.md:1649`. Visual witness produced and read at `/tmp/breadth-stellaris-19.png`.

`[AGENT]` Minimum treatment: introduce a fuel-loop inventory calculation and an adequacy comparison conditional on achieved breeding. Keep net TBR as the source's complete result at the source geometry. Do not add another 3% port loss to 1.074. At changed blanket coverage, coolant/materials, enrichment, divertor interception, or port/maintenance geometry, report TBR as not transferred unless a sourced response model covers the change. Computing `TBR_available - TBR_required` can be useful adequacy analysis without satisfying R2c's specific demand that blanket configuration compute TBR.

Candidate conservation equations use T atoms/s to avoid confusing isotope mass with molecular gas load:

```text
B = P_fus[MW] * 1e6 / E_DT[J/reaction]                    # burned T atoms/s at full power
F = B / f_burn                                          # T atoms/s entering plasma
U = F - B                                              # unburned T atoms/s exhausted
L_recycle = (1 - r_T_recycle) * U                        # permanently unrecovered T atoms/s
J_breed = TBR_gross * B                                 # T atoms/s produced in blanket
I_i = J_i * tau_i                                       # T atoms in inventory segment i, residence approximation
I_work = sum(I_i)                                       # include plasma, exhaust, processing, breeder extraction, storage separately
lambda = ln(2) / t_half[s]
TBR_required = (B + L_recycle + L_other + lambda*I_total + G_stock) / (eta_extract * B)
adequacy_margin = TBR_available - TBR_required
```

`[AGENT]` Here `eta_extract` means recovery from breeding into usable supply and must not include the same neutron-geometry/port penalties already in `TBR_available`; `r_T_recycle` belongs to the unburned isotope stream. `G_stock` is a deliberately specified stock-growth requirement, zero for a single mature plant that only sustains itself. Exclude zero-fusion states from ratio arithmetic and evaluate their inventory decay separately. A duty factor multiplies operating sources and burns, while stock decays through calendar downtime too. Tritium's half-life can use the NIST evaluated `4500 ± 8 days`, with 8 days a standard uncertainty; derive seconds using 86,400 s/day. [Lucas and Unterweger, NIST, 2000, p. 541](https://nvlpubs.nist.gov/nistpubs/jres/105/4/j54luc2.pdf).

`[AGENT]` Startup must be a time-sequence result or explicitly a residence-time approximation. Filling working inventories plus an arbitrary number of days of full injection double-counts recycle in some schedules. Prefer a minimal stock balance using the same residence delays: compute cumulative external injection demand minus usable returned/bred supply during startup; minimum startup stock is the largest deficit plus a declared reserve. Show `I_work`, `I_start_min`, reserve, and purchased initial stock separately. A small piecewise constant delay calculation is sufficient; a multi-plant tritium economy is not required by this proposal.

`[AGENT]` The conditional warning follows directly: `1+(1-0.05)/0.05*(1-0.99)=1.19`. Under lossless extraction, zero decay, and zero stock growth, `r_T_recycle` would need to be at least `1-(1.074-1)*0.05/(1-0.05) ≈ 0.996105` for the available ratio 1.074. This derived threshold is a consistency example, not a recommended parameter. Resolve whether the existing cost factor is intended to represent permanent isotope loss before wiring it into physical adequacy. Existing cost parameters can be renamed/rebound through a modeling item after that meaning is decided; silently raising recovery would erase the finding.

`[AGENT]` For R10.S, do not swap `p_net` for throughput inside the existing 0.7 exponent and call the unchanged constant sourced. A processing cost requires a reference throughput, isotope composition, inlet/outlet specification, technology, containment scope, cost year/currency, reference installed price, and scaling basis. Until those are retrieved, fuel throughput/inventory can be modeled while processing capital remains bounded or not comparable. Startup purchase belongs in the existing startup-cost home; recurring makeup belongs in annual fuel. Processing electrical demand must have a separately sourced specific-energy or equipment-duty basis; 10 MW remains a declared assumption until then.

Readiness: reaction-rate and decay equations are ready; existing burn/recovery assumptions are available but not verified reactor performance. Residence times, isotope-specific loss/recovery, breeder-extraction efficiency, reserves, gas puff/pellet bypass flows, startup sequence, and throughput-cost parameters are not ready. A useful retrieval target is Lord et al., UKAEA-STEP-PR(24)12, *Fusing together a design for sustained fuelling and tritium self-sufficiency*; the [primary abstract](https://scientific-publications.ukaea.uk/papers/fusing-together-a-design-for-sustained-fuelling-and-tritium-self-sufficiency/) was read and supplies conceptual scope only. Retrieve and clean-screen its full paper, process topology, inventory/residence-time assumptions, and technology basis before assigning numbers. The STEP blanket technology is not a Stellaris material substitution. No numeric STEP parameters were adopted here.

Acceptance proposals:

- Reaction count times per-reaction energy reconstructs fusion power; T and D burn each equal reaction count. Full-power annual consumption scales with duty time, while installed flow capacity does not shrink with availability.
- At `r_T_recycle=1`, recycle loss is zero for every valid burn fraction. Lower burn at fixed fusion leaves burn unchanged and increases injected/exhaust flow and the corresponding residence inventory.
- A closed, lossless loop with unit breeding and no decay/stock growth balances exactly. Known nonzero losses increase required breeding. The conditional 1.19 example is reproduced with its semantics stated.
- Pure stored tritium with no flows decays by half after 4500 days. Startup balance never spends tritium before it arrives and does not count recycle as new supply.
- Two blanket geometries outside the TBR source basis cannot both publish source-validated breeding merely because the same held ratio was retained.
- Costs expose startup stock, recurring makeup, and processing plant separately. A source gap produces a named missing/comparison-limited channel, not a zero-cost subsystem.

Focused study: hold one physically feasible operating point, then vary burn fraction, true isotope recovery, residence delays, and reserve as assumption sensitivities. Report minimum startup stock, required breeding, returned fraction, processing throughput, and adequacy across the stated achieved-TBR scenarios. This is an assumption study, not a design optimizer with free recovery efficiency.

### Divertor surface heat exhaust: R5

Current divertor capital is `base*(plant_p_th/1000 MW)^0.5`, with no divertor surface-load output (`models/library/analyses/mfe_account_costs.sysml:168`). Its replacement cost shares the first-wall/blanket neutron-fluence event (`:794`). First-wall neutron load is not a substitute for target surface heat flux, even though both can be expressed in MW/m².

Ready primary source: Stellaris raw PDF pages 14–15, §2.6, verified by viewing `/tmp/breadth-stellaris-14.png` and `/tmp/breadth-stellaris-15.png`. The paper assumes 90% of net core heating radiates before reaching the divertor: 500 MW becomes 50 MW non-radiated exhaust. At the same target geometry its two transport cases are `(T_LCFS=100 eV, chi_perp=3 m²/s)` and `(200 eV, 1 m²/s)`, with target capture 97% and 99%, peak loads 5 and 9.5 MW/m², and an adopted steady-state threshold 10 MW/m². Approximately 200 mm strike width is reported. These are a coupled pair of model assumptions/results, not independent bounds that can be mixed to create an optimistic case. Text locator: `stellaris-design-details.md:1207`.

The same source explicitly leaves recycling efficiency, ash removal, neutral compression, and erosion for later work (raw PDF p. 14), and leaves transients including detachment loss for future study (p. 15). It also says the heat-transport model lacks the neutral and fluid treatment needed to characterize detachment fully. Its point is an engineering referent with a declared operating assumption, not evidence of reactor-scale detachment probability. Section 2.7 on p. 15 separately assumes 100% of heating power is radiated to estimate conservative first-wall loading. That is a distinct load case from §2.6's 90% radiation/10% non-radiated divertor case; the two cannot be combined as one nominal energy partition.

`[AGENT]` Minimal surface-heat ledger, dependent on the parent's installed-versus-operating-heating resolution:

```text
P_heat_abs = P_alpha_abs + P_aux_operating               # MW actually deposited in core
P_sep = P_heat_abs - P_rad_core - dW_dt                  # MW crossing the defined core boundary
P_rad_edge = f_rad_edge * P_sep                         # MW, edge fraction only
P_target_nonrad = f_target * (P_sep - P_rad_edge)        # MW to divertor targets
P_other_nonrad = (1-f_target)*(P_sep-P_rad_edge)          # MW elsewhere
P_target_rad = view_fraction_target * (P_rad_core+P_rad_edge)
q_nonrad_peak = K_nonrad*P_target_nonrad/A_wetted
q_rad_peak = K_rad*P_target_rad/A_target
q_target_peak_sum_bound = q_nonrad_peak + q_rad_peak     # upper bound if individual spatial maxima differ
```

`[AGENT]` A true combined peak requires co-located surface fields: `q_target_peak=max_x[q_nonrad(x)+q_rad(x)]`. Adding each contribution's individual maximum gives an upper bound unless those maxima occur at the same surface location. The published 5/9.5 MW/m² anchors describe the non-radiated target heat calculation; they do not establish a combined radiation-plus-particle peak. Preserve that distinction in field names, reference reproduction, and constraint interpretation.

`[AGENT]` Negative `P_sep` is a violated balance/regime, not zero exhaust produced by clipping. Direct fast-alpha loss to surfaces is a separate load if absorbed alpha power excludes it. Source absorbed/retained/synchrotron radiation conventions must agree with the heat ledger before claiming closure. Radiation is redistributed heat, not automatically energy lost from the plant. Temperature-grade recovery belongs to the parent primary-loop/cycle work; adding radiation again to total recovered fusion heat double-counts it.

`[AGENT]` The source's 90% is a total upstream radiated fraction, not an additional edge fraction after subtracting modeled core radiation. For a consistent calibration with total fraction `f_total`, derive `f_edge=(f_total*P_heat_abs-P_rad_core)/P_sep` and require `0≤f_edge≤1`; inconsistent input assumptions should be reported. This reconciles the source reference without forcing its two operating examples into the current model baseline.

`[AGENT]` A first bounded response can use each source case separately: `q_nonrad_peak=q_nonrad_peak_ref*(P_nonrad/P_nonrad_ref)` at fixed geometry and transport. The equivalent `A_effective=P_target_nonrad/q_nonrad_peak` is 9.7 m² for the low case and about 5.21 m² for the high case; these are derived peak-equivalent areas, not fabricated physical target area or a bill-of-materials quantity. An extra `A_effective_ref/A_effective` factor under a geometry change is an unmeasured extrapolation until new transport/geometry calculations support it. Radiation is a separate surface contribution and cannot be implicitly included by renaming the source anchors. Do not allow freely expanded target area to remove the heat limit without effects on neutron interception, breeding, maintenance, cost, and the allowable coil/port geometry.

Readiness: the two fixed-geometry heat anchors and their limits are verified and ready for bounded response. Physical target area, emissivity/view factors, allowable irradiation-dependent target temperature/heat-flux limits, and geometry-transfer rules need further evidence. The 10 MW/m² threshold is a conceptual steady-state limit adopted by the source; it does not certify irradiated component lifetime. R5 can acquire a computed feasibility fence while detachment remains a declared operating requirement. Divertor erosion life remains not comparable pending a target-life model; scheduled replacement uses the lifetime work's explicit class mapping.

Acceptance proposals:

- The reference case reproduces 500→50 MW and both paired peak loads with no fitted adjustment beyond the published assumptions.
- The 90% nominal divertor-radiation case and 100% conservative first-wall-radiation case remain separate records. The sum of separate radiation and non-radiation peak values is labelled a bound; a claimed true combined maximum requires co-located spatial fields.
- Core radiation plus edge radiation plus non-radiated exhaust equals actual deposited heat at steady state; include radiation intercepted by targets and direct alpha losses explicitly when those are counted.
- At fixed geometry, doubling non-radiated heat doubles the non-radiative peak in the reduced model and can cross the threshold; improve radiation only through the declared bounded assumption.
- No output maps neutron MW/m² to target surface MW/m². Neutron damage life and thermal/erosion life keep separate names and limits.
- A geometry or topology change outside source support marks the prediction outside its validity basis; no extrapolated target area is published as engineered hardware.

Focused study: at one fixed target geometry, run the paired source transport cases across required heating and total/edge radiation assumptions. Report heat partition, target peak, margin, first-wall radiative load, and vacuum/fuel assumptions together. Include one detachment-loss stress case as a declared off-normal load, with no claim about its probability or permissible duration.

### Vessel and vacuum throughput: R6

The shell volume already follows radial build, while the model explicitly omits gas-load pumping (`models/library/analyses/mfe_account_costs.sysml:108`). ITER's primary description distinguishes torus exhaust, neutral-beam, and cryostat vacuum pumps; the machine must exhaust unburned fuel, helium ash, and impurities. [ITER Vacuum System](https://www.iter.org/machine/supporting-systems/vacuum-system). This supports scope separation; its equipment counts and evacuation times do not set stellarator sizes.

`[AGENT]` Compute species-resolved gas throughput after recombination. For neutral gas `Q_i=dotN_molecules_i*k_B*T_gas` in Pa·m³/s; molecular D₂/T₂/DT and atomic helium have different particle counts for the same number of isotope nuclei. Add gas puff/pellet bypass, impurity seeding, leakage, and outgassing on an explicit boundary. Required effective speed is `S_eff=Q_total/p_exhaust` in m³/s at that boundary. Pump-inlet speed and effective vessel speed differ because duct conductance intervenes: `1/S_eff=1/S_pump+1/C_duct` for the simple linear conductance case. Check the flow regime before using pressure-independent molecular conductance. These relations are supported by [Franchetti, CERN Vacuum I, slides 24–27 and 43–46](https://cas.web.cern.ch/sites/default/files/lectures/bilbao-2011/franchetti1.pdf), accessed 2026-09-07; the publisher's alternate proceedings PDF returned a bot challenge and was not used as content.

`[AGENT]` Treat torus exhaust pressure as a neutral-gas boundary condition with a stated location. It is neither plasma pressure nor the pre-shot ultimate vessel vacuum. Cryopump regeneration can require installed parallel/spare units; an average operating fraction alone does not prove continuous pumping. Pumping capacity, cryogenic load, and electrical power are distinct channels. Keep vacuum electrical demand separate from coolant circulation and tritium-process power, with overlapping equipment explicitly allocated once.

Readiness: conservation and speed equations are ready; gas-load inputs follow the fuel calculation. Exhaust pressure, gas temperature, duct geometry/conductance, species-dependent pumping speeds, regeneration duty, auxiliary gas loads, and pump capital/electrical parameters need sources. The already allowed 1costingFE pumping term can be inspected for account scope and a first implementation cross-check at `src/costingfe/layers/cas22.py:515` vicinity, but copying a costing term is not independent pump engineering. Exact new-source retrieval targets: ITER torus cryopump technical design documents linked from the official vacuum page for throughput/capture/regeneration; W7-X pumping/compression work referenced by Stellaris §2.6 and ref. [214] for the reactor-relevant geometry limitation. Screen each full text before extracting values.

Acceptance proposals: count molecules versus isotope atoms correctly; doubling gas load at held pressure doubles required effective speed; increasing duct conductance approaches bare pump speed without exceeding it; a pumping specification that cannot meet required speed produces an explicit capacity shortfall; standby/regeneration occupancy must sum consistently and preserve continuous capacity. A full pumpdown transient is a separate startup/maintenance input and is not earned by an operating throughput calculation.

Focused study: couple fuel burn/recycle and impurity-gas assumptions to throughput, then compare high/low conductance cases at one stated exhaust pressure. Report required speed and equipment scope before assigning cost significance. Fuel throughput and neutral compression uncertainty will probably dominate the bookkeeping effort; that expectation is an agent inference, not a measured sensitivity result.

### Buildings, site, hot cell, and remote handling: R9

The current buildings calculation groups 18 base costs into six power-scaling classes (`models/library/analyses/mfe_account_costs.sysml:304`), with reactor building and hot cell in the fusion-power-scaled base (`stellarator_plant.sysml:417`). Remote handling is separately power-scaled. This is an explicit source-based parametric estimate, but it does not know the enclosure volume, module dimensions, lifting path, work stations, or storage throughput.

ITER's official hot-cell description identifies remote transfer, maintenance/refurbishment, testing, waste treatment/packaging, and interim storage functions. [ITER Hot Cell](https://www.iter.org/machine/supporting-systems/hot-cell), accessed 2026-09-07. It supports a functional decomposition, not transfer of ITER dimensions or unit costs.

`[AGENT]` Minimum treatment for the coming comparison: preserve and label the present building-cost proxy, carry a stated uncertainty envelope, and report physical building dimensions and RH capability as not comparable. Keep that explicit R9 disposition in the comparison packet even if the aggregate CAS21 number is displayed. This does not meet the written S3 target.

`[AGENT]` If the geometry/maintenance work makes R9 worth computing before reveal, use a reactor enclosure envelope from outer coil/cryostat dimensions plus separately justified access/crane clearances. A candidate volume is `V_building=L_envelope*W_envelope*H_envelope`; it is only a functional envelope, not a structural design. Hot-cell working stations follow arrival rate and processing occupancy: `N_positions ≥ arrival_rate*residence_time`, with peak campaigns and discrete maintenance sequences checked separately. Storage bays follow simultaneous inventory, cooling time, and largest transported module footprint. Cost requires function-specific installed $/m³ or $/m² and explicit heavy civil/shielding/containment scope, with remote-handling equipment outside building shell cost where appropriate. The arrival rate and processing duration must be the same ones used in the availability schedule.

Readiness: current proxy and aggregate account definitions are ready; enough functional scope exists to specify the model. Numerical enclosure clearances, module/cask swept volumes, station processing durations, buffer requirements, cost rates/year/location, shielding classes, and seismic/civil basis are not ready. Exact retrieval target: Stellaris §2.11 and Figs. 58–60 for its module routing/maintenance envelopes, then concept-compatible civil cost references with actual scope and quantity (not the barred costing documents). More rooms or a multiplied volume alone would not justify S3.

Acceptance proposals: changing machine envelope changes containment volume at fixed power; longer processing time or a concentrated replacement campaign never lowers required hot-cell capacity; shared maintenance events enter RH throughput, storage, and outage exactly once; physical dimensions lacking source basis remain reported unknown. A proxy sensitivity study changes functional cost drivers in shared groups and reports only the aggregate economic consequence, not an inferred layout.

### Estimate quality and correlated uncertainty: R12

The existing rollup is already granular where many costs concentrate; the initial grader specifically found the missing S3 conjunct to be estimate maturity/uncertainty (`.project/active/demo-depth-rubric/grading.md:286`). More accounts alone would not fix that. Existing contingency is a deterministic fraction of direct cost (`models/library/analyses/mfe_account_costs.sysml:255`), not an uncertainty distribution.

The official AACE public sample of RP 18R-97, dated August 7, 2020, says estimate class is determined by the maturity of defining deliverables; accuracy also depends on other risks. It is process-industry guidance, not a fusion-specific certification. Only seven sample PDF pages were available/read, not the complete 21-page RP. [AACE RP 18R-97, §§1 and 3](https://web.aacei.org/docs/default-source/toc/toc_18r-97.pdf). `[AGENT]` Prepare an evidence inventory by functional account and state a provisional conceptual estimate maturity; complete the required generic/power-industry classification cross-check before claiming a class. Do not take a typical class accuracy band and report it as this model's probability interval.

GAO's cost guide distinguishes sensitivity from risk/uncertainty analysis and calls for distributions tied to data and correlations between cost elements. Shared risk drivers can affect multiple accounts in the same scenario. [GAO-20-195G, Chapter 12, pp. 144 and 155–158](https://www.gao.gov/assets/gao-20-195g.pdf), accessed 2026-09-07. `[AGENT]` For current sparse data, use declared shared-driver scenarios. Describe observed scenario minima/maxima and unresolved coverage, with no probability attached. Add a probabilistic model only after distributions, dependency assumptions, and calibration evidence have been defended.

`[AGENT]` Suggested dependency groups are engineering proposals: common fabrication/productivity across manufactured components; conductor technology/quantity/price across coil cost and cryogenics; common construction duration/rate across expenditure timing and IDC; geometry across material quantities, heat loads, and maintenance; irradiation/material assumptions across lifetime, replacement, storage and availability. These are shared causes, not arbitrary independent ± percentages on every output. Derive correlated outputs by running the same input scenario through the model. Separately show remaining cost-rate uncertainty and model-form alternatives. Contingency and explicit modeled risks must have an inclusion/exclusion ledger so the same risk is not charged twice.

`[AGENT]` If distributions later become justified, the total-cost covariance identity is `Var(sum C_i)=sum Var(C_i)+2*sum_{i<j}Cov(C_i,C_j)`; dependent physics outputs should normally inherit variation from common inputs. A covariance matrix must be positive semidefinite, but that mathematical check alone does not validate expert correlations. Feasibility failures and absent estimates remain outcomes and cannot be dropped before reporting an economic range. The model's nonlinear LCOE means midrange inputs need not give midrange output, consistent with already captured DI-006; no DI supersession is needed for that point.

Readiness: current accounting and deterministic scenario infrastructure are present; source-based numerical uncertainty ranges for many new flows/costs are not. The source packet should retrieve RP 17R-97 and the applicable power-industry classification guidance identified through the [AACE classification guide](https://library.aacei.org/pgd01/pgd01.shtml), plus actual quote/calibration evidence for any cost distribution. This is a targeted source gap; Monte Carlo itself is not the missing scientific evidence.

Acceptance proposals: zero perturbation reproduces the candidate baseline; one common driver reaches all linked accounts once; identical scenarios reproduce exactly at the pinned executable; changing only fixed source cost rates does not change physical verdicts; changed outage assumptions do reach energy and replacement economics; invalid/non-comparable points remain visible; report language contains no probability claim for unweighted scenarios. A scenario that changes both engineering and cost explicitly decomposes those contributions.

## Row-by-row comparison disposition proposal

Every entry is `[AGENT]`; “modeled” means a proposed deliverable with independent verification, not an already earned grade. The list includes every still-below-target cell implied by the initial rubric plus the three reported regrades. It is a disposition inventory, not a consolidated regrade. Rows at target remain subject to the parent's same-pin assessment.

| Cell | Proposed disposition before comparison | Minimum evidence or explicit limitation |
|---|---|---|
| R2b.P | Modeled through lifetime/availability work; bounded if the owner accepts incomplete outage basis | Component life drives actual scheduled replacement and availability. Irradiation-life uncertainty travels with results. |
| R2c.P | Bounded at source geometry; not comparable for unsupported changed blanket geometry/materials | Source-conditioned net TBR plus computed fuel adequacy. A formula for required TBR does not earn computed-neutronics depth. |
| R5.P | Modeled reduced heat calculation under bounded source transport/radiation assumptions | Computed target heat and a steady-state fence. Reactor detachment, erosion, and transient tolerance explicitly unestablished. |
| R6.P | Modeled throughput/speed; bounded pressure/conductance assumptions until sourced | Vessel volume plus species-correct gas load and effective pumping speed. Separate operating exhaust from startup pumpdown. |
| R7.P | Modeled in primary-loop work; explicitly bounded residual auxiliaries | Flow/pressure-drop pumping and shared heat ledger reach net/recirculation feasibility; vacuum and process electricity retain distinct scope. |
| R7.S | Modeled only for sourced pumps/piping/exchangers; otherwise bounded and flagged below target | Separate engineered subaccounts with no arbitrary split of the old total. |
| R8.P | Modeled in cycle work, with stated temperature-grade/technology validity | Efficiency responds to source temperatures and cycle state assumptions; scenario substitutes remain bounded assumptions. |
| R9.S | Bounded current cost proxy; physical layout/RH capability not comparable | Defined aggregate scope and uncertainty; geometry-driven functional enclosure is an optional deeper slice after geometry and maintenance inputs exist. |
| R10.P | Modeled burn/throughput/working inventory/startup balance with bounded process assumptions | Atoms/molecules, on-time versus calendar-time, actual losses, and delays explicitly defined. |
| R10.S | Bounded current processing/startup costs; not comparable at engineered processing level until cost basis retrieved | A throughput-cost reference with technology, scope, currency/year, and scaling basis is required to earn the target. |
| R11.P | Modeled through lifecycle work; bounded residual unscheduled downtime | One consistent event schedule supplies outage, availability, and replacement/handling consequences. |
| R12.S | Modeled uncertainty treatment with bounded scenarios and provisional maturity statement | Reconciled concentration accounts, source maturity inventory, shared-driver envelope, required classification cross-check; no inferred confidence level. |

The status summary's denominator “21 applicable cells” omits the two extra physics subcells in Row 2. The written rubric has 23 applicable cells: Row 1 has one; Row 2 has four; Rows 3–8 have twelve; Row 9 has one; Rows 10–11 have four; Row 12 has one. The initial grading plus the three reported regrades directionally gives 11 at target and the twelve remaining cells listed above. This is a reconciliation of historical evidence across pins, not a current regrade.

## Execution slices, dependencies, and effort

These are `[AGENT]` sizing estimates in focused engineering workdays, excluding external source-access waits and full 3D design/transport calculations. They should be merged with the parent's thermal/lifetime sequence, not registered as a separate competing plan.

| Slice | Deliverable | Dependencies | Effort |
|---|---|---|---|
| Breadth source/semantics packet | Fuel isotope-flow meanings, radiation boundary, disposition matrix, exact missing-source requests | Current model and candidate comparison contract | 0.5–1 day |
| Fuel mass/inventory adequacy | Burn/throughput/residence/startup calculation and conditional breeding comparison, independent reference cases | Isotope-specific source parameters; lifetime duty schedule interface | 1–2 days after source readiness |
| Divertor reduced heat model | Paired source scenarios, conservation ledger, target heat fence, response-validity disclosure | Actual operating heating; core/edge radiation boundary; geometry basis | 1–2 days |
| Vacuum sizing | Species gas throughput, conductance-limited speed, capacity/duty outputs | Fuel/impurity flows, exhaust pressure and duct/pump evidence | 0.5–1.5 days |
| Buildings disposition | Preserve bounded proxy, scope ledger, comparison limitation | Candidate geometry and maintenance evidence | 0.5 day |
| Optional functional layout depth | Containment envelope/hot-cell occupancy and sourced cost functions | WI-044 envelope, lifetime event schedule, processing/clearance/civil rates | 2–4 days; source-constrained |
| Estimate maturity and envelope | Account evidence table, shared-driver scenarios, coherent cost/feasibility report | Thermal/lifetime/breadth channels and repaired publication contract | 1–2 days |
| Integrated study and handoff | Re-run affected channels, fresh grader evidence map, uncertainty and comparison dispositions at one pin | All selected slices; parent handles integration | Budget with parent plan |

Decision consequence: R2c computed neutronics, R10 processing cost, and R9 physical layout are the clearest candidates for explicit bounded/not-comparable dispositions. They should not be silently claimed complete to keep a schedule. A full geometry-sensitive TBR surrogate would require clean training cases, verified material/nuclear-data definitions, held-out validation and an applicability domain; one paper's TBR point cannot supply them.

## Candidate domain insights, without IDs

1. **Tritium burn and circulating throughput are different quantities.** Context: fusion reaction rate fixes burn; low single-pass burn increases circulation and loss exposure. Model implication: give isotope flow, inventory delay, recovery, and usable breeding distinct boundaries. Analysis implication: the required breeding margin depends on recovery and stock, so a held TBR floor alone cannot establish self-sufficiency. Source basis: ITER fuel-loop description plus the explicitly derived conservation equations above. This does not supersede an existing fuel-cycle DI.
2. **Stellaris divertor heat anchors are conditional transport cases.** Context: source p. 15 combines a 90% radiated fraction with paired transport/capture/peak results. Model implication: preserve each case's assumptions and heat boundary; source-based geometric extrapolation is not established. Analysis implication: detachment/radiation sensitivity belongs beside target heat feasibility, and radiation must not be removed twice.
3. **Gas-load pumping and coolant circulation have separate duties and units.** Context: vacuum speed depends on gas throughput, pressure and conductance; coolant power follows thermal-hydraulic flow. Model implication: distinct systems and non-overlapping electric/cost homes. Analysis implication: neither a vessel-volume cost nor primary coolant MW is evidence of adequate exhaust.
4. **Estimate maturity does not determine this model's error distribution.** Context: AACE class follows definition deliverables; GAO risk analysis uses supported distributions/dependencies. Model implication: track evidence maturity separately from uncertain parameters and shared causes. Analysis implication: scenario envelopes are useful without probability claims. Extends the nonlinear-output warning in DI-006; no supersession proposed.

## Sources and read-depth handoff

The main agent should read this whole draft. For model claims it should fully read the compact relevant calc definitions (`mfe_power_balance.sysml`, `mfe_plasma_sustainment.sysml`) if incorporating interface recommendations, and the specific fuel/vessel/divertor/building/cost clauses at `mfe_account_costs.sysml:108`, `:168`, `:255`, `:304`, `:734`, and `:794`; no need to reopen unrelated account definitions. Full-file reading is appropriate for the short grade/rubric/contract artifacts when producing the final integrated report. Historical gradings carry superseded line numbers and pins; present model locations above were inspected directly.

Primary source excerpts suffice for these breadth conclusions: Stellaris raw PDF pp. 14–15 and 19, source text §§2.6 and TBR paragraph; ITER Fuelling (Fuel cycle/Tritium Plant), Vacuum System, and Hot Cell pages; CERN slides 24–27 and 43–46; NIST abstract and half-life-unit explanation; GAO Chapter 12 risk/correlation passages; AACE public sample §§1/3. The raw Stellaris pages were visually verified locally; the source URL/DOI is the already registered KIT paper, `10.1016/j.fusengdes.2025.114868`. Full papers, including future STEP/W7-X source targets, need independent clean-room screening before reading beyond the screened landing-page content. Nothing is registered as new authority by this draft.

Source limitations are part of the findings: Stellaris numerical table extractions are unreliable, so the quoted new anchors were checked against the raw PDF; the CERN proceedings route returned a bot page, while the official lecture deck was readable; AACE is only a public sample, not complete classification evidence; UKAEA STEP was an abstract only; no independently supported new fuel processing cost, layout cost, residence-time, or vacuum equipment calibration was retrieved. Those gaps constrain the proposed comparison disposition, not the ability to implement conservation bookkeeping.
