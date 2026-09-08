---
date: 2026-09-07
researcher: Codex
topic: Execution prework for stellarator primary-cycle, lifetime-availability, and breadth closure
tags: [stellarator, demo-maturation, thermal-hydraulics, availability, tritium, breadth, clean-room]
research_type: domain-and-model-synthesis
status: pending-review
---

# Three remaining demo seams: research and execution prework

## Answer

There is enough evidence to begin a representative helium circuit, a component-replacement calendar, and reduced fuel/exhaust calculations. There is not enough evidence to claim a complete Stellaris thermal plant, whole-plant reliability, geometry-sensitive breeding, or engineered fuel-processing/building costs. The practical route is to compute the supported dependencies, bound the remaining assumptions, and keep unsupported comparisons visible.

- **Primary loop and cycle:** calculate flow, pressure loss, electrical demand, recovered work, exchanger temperatures and temperature-compatible conversion together. Separate physical closure from pump/pipe/exchanger costing. A published DEMO circuit provides independent checks, not a Stellaris layout.
- **Lifetime and availability:** one finite calendar should determine damage accumulation, replacement dates, downtime, energy sold and replacement cost. Seven months is the paper's estimated in-vessel outage; five months and 90% availability are targets. Coil wearout and non-blanket maintenance need their own dispositions.
- **Breadth:** fuel conservation, working inventory, conditional breeding adequacy, divertor surface loading and vacuum throughput have tractable reduced models. Computed breeding versus blanket design, processing costs, and physical building layout remain source-constrained. Start uncertainty with coherent shared-input scenarios, not invented probabilities.
- **Shared prework:** settle heat ownership, operating versus installed heating, calendar versus operating time, cost-account replacement, and output publication before wiring the new calculations into the plant. These are the likely sources of cross-item rework.

This package supplies source checks, candidate equations and domains, implementation locations, validation cases, study designs, scope options, source-acquisition targets, effort estimates and a twelve-cell disposition inventory. It is research, not an approved spec, completed model increment or rubric regrade.

## Reading map

| Report | Use it for |
|---|---|
| [Primary loop and cycle](20260907-163520_primary-loop-cycle-closure-prework.md) | Full thermal circuit candidate, source tables, heat/work equations, cycle applicability, P-depth versus S-depth scope, hydraulic tests and study arms |
| [Lifetime and availability](20260907-163520_lifetime-availability-closure-prework.md) | Source outage evidence, finite-calendar algorithm and boundary examples, cost/time conventions, component coverage, replacement/availability tests |
| [Breadth dispositions](20260907-163520_demo-breadth-disposition-prework.md) | Fuel, breeding, divertor, vacuum, buildings and uncertainty; every remaining below-target cell; source requests and bounded/not-comparable proposals |

Read this synthesis first. Read the relevant specialist report before drafting that item's requirements. The formulas and numerical assumptions in those reports are candidates with stated limits, not values already installed in the model.

## Request, authority and current state

`[OWNER]` The request is to research recommendations 3, 4 and 5 of `.project/reports/2026-09-07-1549-status-report.md` and prepare execution. The active coding epic is `.project/backlog/epic_stellarator_mbse_demo.md`, especially Item 10 and the maturation context; model work is tracked separately in `work/backlog/epic-mfe-cost-modeling.md`. The epic's older overall status is not a reason to ignore its later active maturation work.

`[INHERITED: .project/concepts/stellarator-demo-maturation.md, owner corrections 2026-09-01]` Physical depth and structural/cost depth both matter. The clean-room seal remains. A real primary-loop calculation does not require reopening WI-033. Continuing reproduction of the historical 1costingFE anchor is not a maturation obligation. The rejected fixed fraction of thermal power is not a hydraulic response model. Preserve the concept's provenance when turning these into requirements.

`[AGENT]` All recommended scopes, equations, defaults, thresholds, sequencing and estimates in this package remain agent proposals. Researching the status report does not ratify its proposed reveal-readiness condition. Source estimates and targets are not owner requirements. The frozen rubric remains the scoring contract until legitimately changed; only a fresh assessment can award new grades.

Three status refinements prevent duplicate work:

1. The numeric-output defect has already been repaired upstream. The newer investigation `.project/research/20260907-161438_numeric-evidence-merge-and-demo-follow-through.md` records TEAx v3 merged at `8d877460` and current burn-control outputs persisted. The remaining 75 failures are downstream exporter coverage/signature contracts; executor revision capture is separate. Do not restart the old upstream diagnosis.
2. The rubric has **23 applicable cells**, not 21: Row 2 contains three physics subcells plus its structural cell. The initial grading and three historical regrades imply 11 cells at target and twelve outstanding cells. This is an inventory across historical pins, not today's certification. The breadth report lists all twelve.
3. Proposed comparison limitations do not waive B-2/B-3/B-4 in `.project/completed/20260821_demo-anchor-acceptance-spec/spec.md:119`. B-2 requires first-order structural correspondence; B-3 and B-4 retain their required comparison axes and bands. A missing required value remains missing and cannot become a pass by disappearing from the comparison. Any actual contract revision is an owner decision.

### Baseline identity and scale

Read-only model inspection used repository HEAD `75f46dc8d8b900a27b9a823242528eb1a1a206b6`. The current study manifest, `exploration/stellarator_e2e/studies/manifest.json`, records:

| Identity | Value |
|---|---|
| Indicator/package pin | `1d4a06b0e0e9e4e3633bdc85cc2a310e1fdb56806da447e6dea978baf17e6cc2` |
| Semantic fingerprint | `baab7e4c75412f8cb754f1876bb33c4770e6bf646ce8f46cdf49d51acb94322f` |
| Executable fingerprint | `cd2c1c4aa53544e32d1208e5dad100a7c1d9bd12dbfedb6df251b3ad28cc5656` |
| Manifest baseline | 322.31843948570247 $/MWh; ten satisfied verdicts |

Stored baseline evidence in `exploration/stellarator_e2e/studies/20260907-burn-control/results/baseline_result.json` gives thermal power 3224.352676 MW, gross-before-plant-auxiliaries 1073.709441 MW, net power 716.633806 MW, recirculation 357.075635 MW and annual CAS72 126.649656 M$/yr. At held availability 0.85, annual physical energy is 5,336,055.322 MWh. These are existing results or arithmetic on them, not new loop/lifecycle model runs.

The current power balance's local pumping sensitivity is informative: with other inputs held, `dP_net/dP_pump=(1-f_sub)*eta_th*eta_p-1=-0.838495` at `f_sub=.03`, `eta_th=.333`, `eta_p=.5`. This includes the existing recovered-pump-heat credit. It is not a derivative of the proposed coupled loop, whose heat and efficiency may both move. The formula follows `models/library/analyses/mfe_power_balance.sysml:121`.

## Shared interface contract to settle first

The table is an `[AGENT]` design candidate. A value has one producer; downstream systems consume it rather than reconstructing it with different assumptions.

| Quantity and basis | Proposed owner | Consumers and consequential rule |
|---|---|---|
| Actual operating coupled heating [MW] versus installed coupled capacity [MW] | Heating/operating-point boundary | Sustainment, exhaust, thermal power and wall-plug consumption use consistent operating power; heating capital remains installed capacity |
| Fusion source heat, core/edge radiation, direct losses and thermal destination [MW] | Shared heat ledger | Blanket, first wall, divertor and conversion receive allocations of the same source joules; radiation is a destination, not extra fusion heat |
| Circuit flow [kg/s], temperatures [K], pressure losses [Pa] | Primary-loop calculation | Fluid work and electrical demand; positive approaches and operating-domain verdicts; equipment sizes use online duty |
| Fluid work, drive losses and electrical circulation [MW] | Primary-loop calculation | Recovered heat enters the appropriate circuit once; full electrical demand is a plant auxiliary once |
| Cycle heat input, cycle-net output and rejected heat [MW] | Conversion calculation | Existing “gross” means before external plant auxiliaries; internal cycle compressors/feed pumps are already inside cycle-net efficiency |
| Neutron peak [MW/m²], surface heat peak [MW/m²], coil dose [dose/FPY] | Distinct wall/exhaust/shielding producers | Distinct damage/failure limits; matching units do not make these interchangeable |
| Physical component life [FPY] | Damage/lifetime calculation | Calendar events; no availability-dependent physical-life cap or inherited numerical floor masquerading as material evidence |
| Operating time [FPY], downtime [calendar years], dated events | One lifecycle calendar | Average energy, operating fuel, replacement PV, maintenance handling and stock decay; fixed staffing remains calendar cost |
| Isotope burn/return/breeding [atoms/s], stock [atoms or kg] | Fuel loop | Required breeding, startup stock, processing capacity and species-correct exhaust; annual use differs from installed capacity |
| New subsystem capital and replacement scope [$ with basis] | Owning assembly/account | Replace the corresponding old subtotal or retain an explicit limitation; avoid counting old proxies plus new equipment |

Two current seams deserve an explicit choice:

- **Installed versus operating heating.** The baseline publishes 50 MW coupled capacity but requires 49.0796008 MW for the chosen operating point. The present thermal/electric accounting uses the installed chain (`models/designs/generic_mfe/mfe_plant.sysml:448`, `:456`). Recommendation: define operating coupled power explicitly and use installed capacity as its ceiling. First run a compatibility arm reproducing today's 50 MW accounting, then isolate dispatch-consistent accounting. Do not blend that change into a pump/cycle attribution without naming it. At other points the difference can be much larger than the baseline's 0.9203992 MW.
- **Time integration versus online duty.** Availability reduces accumulated operating time and energy, not online fusion heat, coolant flow, compressor rating or fuel-processing capacity. Tritium decay continues during outages. Maintenance cooling and imported electricity are separate unresolved duties; an inactive mathematical zero-flow case is not a decay-heat cooling model.

The heat ledger can remain small. Start with conservation and explicit heat-grade partitions, not spatial CFD. The source's divertor case assumes 90% radiation; its conservative first-wall cooling case uses 100%. They are different cases, not simultaneously additive loads. Separate radiation and particle-load peaks sum to an upper bound unless their surface maxima coincide. The specialist reports retain these distinctions.

## What is ready, and what the next source round must deliver

| Area | Evidence available now | Specific missing deliverable and consequence |
|---|---|---|
| Helium thermal/hydraulic reference | Moscato: 8 MPa, 300–500°C, 2025.7 kg/s, 2101.7 MW, component losses, loop/equipment counts, exchanger duties | Choose and label transfer to a representative Stellaris loop. Resolve circulator shaft/electric boundary and efficiencies; verify properties over selected conditions. Broad geometry scaling remains unsupported |
| Power conversion | PROCESS paper/code correlations with temperature ranges and heat-grade conventions; generic compressor/property sources | Pin the selected paper or code version; choose sink, exchanger approaches and low-grade treatment. No source supports unconditional 47% sCO2 efficiency at any available hot temperature |
| Primary-system cost | Current aggregate accounting plus published example equipment quantities | Component cost basis with capacity, material, pressure, installation scope, currency/year and scaling domain. Without it, diameter/loop-count economic optima are not credible |
| Planned maintenance | Stellaris first-wall 4–6 FPY estimate and seven-month in-vessel outage estimate; PROCESS scheduling precedent | Review physical damage allowance, component grouping and payment/terminal policy. Unplanned reliability remains a stated scenario, not a sourced probability |
| Whole-plant service life | Source coil estimate about 10 FPY; known separate divertor/plant systems | Explicit component coverage and horizon/retire/replace/violation decision. Source geometry's coil estimate is not a shield-thickness response curve |
| Fuel and breeding adequacy | Reaction conservation, NIST half-life, source-conditioned achieved TBR1.074 | Isotope-specific recovery, extraction, residence times, reserves, startup delays and throughput-cost reference. Required TBR calculation does not compute achieved neutronics |
| Divertor | Two source transport/capture/peak-load cases, 5 and 9.5 MW/m², adopted 10 MW/m² steady limit | Physical target area/response, irradiated allowable, erosion and transient treatment. Fixed-geometry reduced response is available; target-life prediction is not |
| Vacuum | Gas conservation and conductance-limited speed equations | Exhaust boundary pressure/temperature, gas composition and bypass, duct/pump data and regeneration schedule. A vacuum shell volume is not a pumping specification |
| Buildings and hot cell | Current grouped proxy; source maintenance architecture and generic functional evidence | Actual enclosure/access/handling quantities, campaign occupancy and installed civil rates. Preserve bounded aggregate cost until numerical layout evidence exists |
| Uncertainty | Existing scenario route, account structure, public estimate-maturity and risk guidance | Per-input ranges/bases and shared drivers; complete classification source if claiming an estimate class. Scenario envelope needs no unsupported probability distribution |

The specialist reports contain exact retrieval targets. Highest-value requests are Moscato's preliminary circulator design, clean UKAEA fuel-cycle inventory work, W7-X/ITER exhaust technical specifications, Stellaris maintenance drawings, and cost sources with actual equipment scope. Use native source acquisition/registration before making new references MR-4 model authority. Do not contact authors without separate direction.

Two cheap consistency checks already narrow the problem:

- Total published IHX duty is 2231.1 MW, or 129.4 MW above blanket source heat, close to the published 130.8 MW total circulator figure. This supports including fluid work in loop heat while leaving motor/electrical semantics unresolved. Source Table 2 prints an inconsistent MPa pressure-drop label; Table 3's kPa basis is physically consistent with an 8 MPa loop. Both were checked on the raw PDF.
- At 5% single-pass burn, 99% permanent tritium recovery would require `TBR>=1+(1-.05)/.05*(1-.99)=1.19` before decay and other losses. The held 1.074 would not cover that interpretation. Today's 99% factor prices blended D/Li feedstock, so this is a conditional semantics conflict, not a proven physical tritium deficit. Do not silently improve recovery to erase it.

## Recommended work decomposition

These are `[AGENT]` scopes for the next planning conversation, not newly minted work items or a replacement for WI-044.

```text
Shared basis + source choices
  ├─ Heat ledger → representative loop → compatible cycle → equipment costs
  ├─ Life + component policy → calendar → replacement/energy economics
  └─ Fuel flows → inventory/adequacy → vacuum sizing
       Heat ledger → divertor surface-load response

Geometry/transport disposition (WI-044) ──→ transfer validity for final studies
Calendar + geometry ──→ building/RH disposition
Selected model slices + exporter follow-through ──→ same-pin studies
Same-pin studies + uncertainty + breadth dispositions ──→ fresh grading/comparison decision
```

1. **Basis and disposition packet.** Approve the heat/time/isotope meanings, one representative loop boundary, a maintenance scope and the breadth limitations. Inventory source-ready numbers versus selected assumptions. A focused spec can reuse the tables here rather than research the whole area again.
2. **Thermal physical closure.** Add the shared heat ledger and representative circuit; add conversion conditional on its temperature domain. Check a published circuit independently. Keep existing cost limitations visible until the equipment slice replaces them. First study is fixed geometry, not a new size optimizer.
3. **Lifecycle closure.** Implement the deterministic finite calendar and component-scope disclosure. Drive cost and energy from it. Use seven months as the estimate arm and five months as the target arm. Retain the existing annual-equivalent economics initially with a shadow exact-dated-energy check, unless the owner chooses full DCF expansion.
4. **Breadth physical calculations.** Add fuel flows/inventory and conditional adequacy; then gas throughput/vacuum capacity. Add divertor response on the agreed heat ledger. Keep achieved-TBR geometry transfer, absolute erosion life and uncalibrated process costs explicit limitations.
5. **Cost and estimate closure.** Replace sourced primary equipment costs without duplicated subtotals. Assemble account evidence maturity and shared-driver scenarios. Either source physical building/process estimates or preserve their below-target dispositions for owner review.
6. **One integrated evidence round.** At a selected current geometry/physics pin, execute baseline/attribution/threshold cases, publish every operand, assess changed rows and confirm unchanged ones. The comparison decision includes remaining limitations; it does not silently lower the written contract.

Independent source work and standalone calculations can proceed concurrently after the shared basis is chosen. Integrating changes to `mfe_plant.sysml`, the stellarator instance, account costs and the oracle needs one coordinated owner because every track touches them. This is where apparent parallel speed can turn into rework.

Effort is source-dependent. Specialist estimates use different units (sessions versus workdays) and should not be summed as a promise. A planning envelope for the reduced physical models plus integration is roughly 2–4 engineer-weeks, excluding source-access waits, deep component costing, geometry-sensitive neutronics, full transport and detailed layout. `[AGENT]` This assumes an accepted source/basis packet and existing handwritten-stage/toolchain support. A held-assumption sensitivity/disposition-only pass is smaller but does not earn the same physical or structural depth.

## Validation and study prework

The reports give per-calculation tests. An integrated plan should preserve the following attribution structure:

| Run family | What is held | What it establishes |
|---|---|---|
| Compatibility baseline | Current pin, held pump/cycle/availability and accounting | No-change reconstruction before attribution; every current verdict/operand visible |
| Heat/loop increment | One accepted operating geometry and plasma point | Flow/loss/work/temperature conservation; pump heat and cycle internal work counted once |
| Calendar increment | Same online power and component prices | Lost production versus replacement-PV contributions; first event and horizon edge behavior |
| Fuel/exhaust increment | Same fusion point and source geometry | Isotope closure, conditional breeding, gas speed and source-paired target loads |
| Coupled scenarios | Same named common assumptions across all components | Interaction effects and feasible/not-comparable outcomes, not independent output perturbations |
| Geometry transfer | WI-044 disposition and stated transport/heat-routing mappings | Which reduced models remain valid when size changes; no free unpriced expansion |

Use independent exact cases: zero pressure drop; source heat/flow identity; one circuit versus parallel circuits; zero damage; first replacement at physical-life/online-productive-fraction; retirement equality on either side; zero discount; fully recovered isotope stream; factor-of-two gas throughput; source divertor case pairs; and a shared-cost driver reaching its intended accounts exactly once. A calibrated source point is a reconstruction, not independent validation of an off-design law.

For lifecycle studies, re-run the wall/heating comparisons at the accepted current two-sided burn condition. Keep both fixed wall-plug and fixed coupled-heating parameterizations. The historical L-011 matched-size pairs are named historical comparisons, not nearest-neighbor derivatives. Trace integer replacement thresholds with small wall-load transects; a grid optimum alone can hide the mechanism. Historical records stay at their own pins and are never overwritten to look current.

For uncertainty, report unweighted scenario minima/maxima, validity failures and missing accounts. No P90/confidence/probability label is justified by these scenarios. Separate deterministic contingency from modeled risks and show overlap explicitly. A design lever without corresponding physical or cost consequences is bounded, not offered as a free optimizer variable.

## Implementation and toolchain handoff

| Surface | Expected work |
|---|---|
| `models/library/analyses/mfe_power_balance.sysml` and candidate loop/thermal calc files | Distinct source heat/work/electric boundaries and cycle outputs; generic equations with explicit units/domains |
| `models/library/analyses/mfe_account_costs.sysml` and candidate lifecycle/fuel calcs | Retire duplicate periodic replacement calendar; owned component costs; flows versus purchases |
| `models/designs/generic_mfe/mfe_plant.sysml` | Shared producers, availability consumers, subassembly/cost wiring; review dormant generic behavior explicitly |
| `models/designs/stellarator_09/stellarator_plant.sysml` | Sourced instance inputs, scenario assumptions and feasibility assertions |
| `exploration/stellarator_e2e/models/` | Byte-identical model twins through the established family structure |
| `exploration/stellarator_e2e/generated/handwritten/` | Preserve or deliberately revise manual-stage contracts; verify regeneration twice after interface changes |
| `exploration/stellarator_e2e/verify_stellaris.py` | Independently derived thermal, calendar, fuel and cost checks, not imports of production calculations |
| `exploration/stellarator_e2e/studies/oracle_entry.py` | Explicit entry-to-input/output maps and computed operand bindings; reject undeclared inputs |
| `exploration/stellarator_e2e/studies/study_route.py` and study exporters | Required outputs, current verdict inventory, finite/nonblank publication and declared invalid cases |
| Snapshot, manifest, census, six known-answer fixtures and validation/trace rows | Re-derived evidence after model changes, not hand-patched expected numbers |

Current oracle mapping is explicit, not reflective. A new input does not automatically become an authorized study lever; the general mapping currently lacks `p_pump`, while historical specialized studies have their own mappings. Availability becoming computed also retires or renames the old direct availability lever. Likewise, a future TBR computed producer would need a channel operand instead of the current input binding. These are interface migrations to specify, not incidental test fixes (`studies/oracle_entry.py:51`, `:128`, `:233`, `:345`).

Use the completed WI-043 plan's regeneration and re-pin recipe at `work/completed/20260907_WI-043_two-sided-sustainment-condition/plan.md:109` and `:139`, adjusted to the new calc interfaces. Its evidence found eight literal verdict-count sites, so adding assertions requires a whole-consumer inventory. A changed handwritten interface can be restenciled despite the preserve flag; port the implementation to the new signature and verify a subsequent regeneration preserves it. Snapshot → manifest → census → fixtures → single runner remains the dependency order.

`docs/integration_seam_operator_guide.md` is the operator authority. The integration seam proves that an already regenerated, audited, committed package reproduces; it does not perform an unfinished modeling item's regeneration for it. Carry the selected model/package, source bytes, toolchain and executor identity in the evidence. No integration, generation, study run or commit was performed during this research.

Suggested diagnostic commands for the eventual item, not results claimed here:

```bash
UV_CACHE_DIR=/tmp/fusion-tea-uv-cache uv run agentic-mbse validate models --complete
UV_CACHE_DIR=/tmp/fusion-tea-uv-cache uv run python -m pytest tests/models -q
UV_CACHE_DIR=/tmp/fusion-tea-uv-cache uv run python -m pytest tests/study/test_study_publication_fail_closed.py -q --tb=short
```

Load the license and pinned dependencies as the operator guide requires without printing secrets. Establish a before/after failure census; the documented 75 exporter failures are not evidence that the new physical equations fail, and a selected-path pass does not clear that known debt. The current migration report already gives the failing exporter/signature inventory.

## Decisions to carry into scoping

| Decision | Recommendation `[AGENT]` | What choosing otherwise changes |
|---|---|---|
| Representative versus plant-specific loop | Source-calibrated representative circuit with limited transfer domain | Plant-specific circuit needs layout/channel/component evidence first |
| One versus two cycles initially | One temperature-compatible cycle, then a matched-heat second arm | Two simultaneous cycles add exchanger/low-grade convention decisions before useful first evidence |
| Lifetime mechanism | Finite deterministic calendar; explicit initial bundled policy | Steady average is smaller but has known replacement-date inconsistency if fed into old CAS72 |
| Energy economics | Retain annual-equivalent convention with shadow dated-energy discrepancy | Exact DCF requires dated energy and variable costs, not only new replacement dates |
| Incomplete plant lifetimes | Report conditional availability and explicit uncovered life/horizon constraints | Full-plant claim needs coil/divertor and other scheduled-maintenance coverage |
| Breeding depth | Source-conditioned achieved TBR plus computed required TBR | Geometry-sensitive achieved TBR needs clean neutronics cases and validated transfer model |
| Uncalibrated physical/cost scope | Explicit bounded/not-comparable evidence subject to the comparison contract | Meeting every S3/P3 target may require additional sources and substantial new engineering |
| Final study timing | Fixed-geometry component work now; geometry-sensitive integrated claims after WI-044 disposition | Earlier broad geometry studies carry unresolved transfer validity and may need rerunning |

No decision in this table has been made for the owner. The first useful next step is reviewing the shared basis and scope choices, then writing the selected model requirements. The package deliberately identifies source gaps where more research cannot honestly manufacture an engineering answer.

## Research verification, limitations and insight review

Three independent research tracks were cross-reviewed for heat accounting, time/availability scope, source interpretation and comparison-contract implications. The coordinator read the specialist reports, current model seams, prior owner corrections, wall/heating learnings, source evidence and the newer publication investigation. Critical Stellaris and Moscato quantities were checked against raw PDF page images; source hashes and precise locations are in the reports. New public sources include institutional PROCESS, NASA/NIST, ITER, CERN, AACE and GAO material, with read-depth/access limitations documented. No sealed holdout PDF or barred source body was used; the model-facing clean-room protocol remains in force.

Completed here: source/document/code inspection, raw-page verification, algebraic and synthetic numerical checks, historical rubric inventory and prework synthesis. Not completed here: new engineering model execution, new property validation, detailed source registration, production test reruns, rubric certification or source-parameter approval. Temporary page images can be recreated from cited registered PDFs; newly fetched PROCESS evidence has a URL and hash but still needs native registration before model use.

Each specialist report proposes domain insight candidates with context, model implications and analysis implications. No DI IDs were allocated. DI-007's cycle independence remains correct for the old preset model but needs scoped application once exchanger conditions couple the systems. DI-008's amended pumping basis remains intact. DI-006's nonlinear uncertainty warning is consistent with shared-driver scenarios. The overview's “capacity factor = availability × thermal efficiency” sentence and the live PROCESS overlap-sign typo are recorded discrepancies, not new authority. No accepted insight was silently changed or superseded.

Review the research package and each proposed insight separately through the requested research workflow. Approval, accepted limitations, new model items and any changed comparison requirements remain owner decisions.
