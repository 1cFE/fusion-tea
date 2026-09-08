---
date: 2026-09-07
researcher: Codex lifecycle research subagent
topic: Close component lifetime into availability for the stellarator demo
tags: [stellarator, lifetime, availability, replacement, outages, lcoe]
research_type: model-and-domain
status: pending-review
---

# Item 4 prework: close component life into availability

Research date: 2026-09-07. Researcher: lifecycle subagent. Status: research draft for coordinator synthesis, no implementation or PM mutation. All recommendations and proposed parameter choices below are [AGENT]. Source facts are evidence, not owner requirements. This serves RQ-1, RQ-2 and RQ-5 in `modeling_project/OVERVIEW.md` and recommendation 4 of `.project/reports/2026-09-07-1549-status-report.md`.

## Answer

The next credible increment can connect the existing peak-driven first-wall life to a bundled in-vessel replacement calendar, scheduled downtime, residual unplanned downtime, electricity sold and replacement cost. The source already gives the missing scheduled-outage anchor: Stellaris estimates **seven months overall** for replacing in-vessel assemblies, including the breeder blankets. Five months is its target. The paper's 90% availability is also a target, not the result of the seven-month estimate.

Use a deterministic finite-horizon calendar with one bundled first-wall/blanket/divertor event initially. Compute physical damage life independently of availability; use that life to advance an operating-time clock; insert real calendar downtime; charge replacement events at their actual dates. Publish the clock and event outputs. Residual unplanned downtime remains a transparent assumption until a reliability basis exists. A steady-cycle formula is a useful verification oracle and bounded first option, but feeding its average availability into today's periodic CAS72 formula does not produce the same event dates.

This does not yet establish a complete plant lifetime model: divertor-specific failure limits, replacement labor/waste handling costs and magnet life remain material gaps. A lifecycle goal should explicitly disposition these gaps rather than presenting first-wall coupling as full RAMI coverage.

Until the remaining component scopes have dispositions, label the reported result **equivalent availability conditional on the in-vessel maintenance calendar**, not a prediction of total plant availability. The residual unplanned fraction covers specified unexpected failures only; it does not account for other scheduled maintenance or known component wearout.

| Maintenance class | Proposed coverage | Remaining disposition |
|---|---|---|
| First-wall/blanket/divertor bundled event | Explicit damage clock, replacement cost and overall outage | State the bundled-life assumption and unresolved separate divertor life |
| Preparation, cooldown and restart | Included in the overall event; preparation overlaps cooldown as the source states | Do not add these periods again |
| Scheduled cryogenic, turbine, vacuum and fuel-system maintenance | Not yet modeled | Establish their calendars and whether work fits wholly within in-vessel outages; overlap needs duration/resource evidence |
| Unexpected failures | Explicit residual unplanned fraction over otherwise scheduled-online time | Name included equipment and avoid adding the same failure losses elsewhere |
| Coil radiation life and other finite wearout | Not covered by the residual unplanned fraction or blanket replacement | Bound the applicable operating horizon, retire at the limit, model a sourced replacement policy, or publish an explicit life violation |

In particular, a nominal 30-calendar-year result that accumulates more operation than the source's approximately 10-FPY coil-life estimate remains conditional on a coil-life disposition. Replacing in-vessel components does not reset coil dose. Increasing the residual unplanned fraction is not an acceptable substitute for reporting this wearout limit.

## Clean-room and evidence ledger

The session is MODEL-FACING under `knowledge/holdout/aries-cs/PROTOCOL.md`. No sealed PDF, barred Helios artifact, Waganer/Araiinejad source, or concept-09 analysis was opened. The Stellaris paper is explicitly admissible. Existing library models and 1costingFE are admissible under the protocol's recorded lineage exception. No author was contacted.

New primary source: Kovari et al., “PROCESS: a systems code for fusion power plants—Part 2: Engineering,” Fusion Engineering and Design 104 (2016), 9–20, DOI `10.1016/j.fusengdes.2016.01.007`. Publisher PDF served by UKAEA: https://scientific-publications.ukaea.uk/wp-content/uploads/Preprints/CCFE-PR1605.pdf. Downloaded to `/tmp/lifetime-process-engineering.pdf`; SHA256 `f1acb2ed2d10c31bb82f4b8d6fcf5b8d7800d06d4bc465e19f305726d9f916f1`. Before substantive reading, local extracted text was screened for `aries.?cs|waganer|araiinejad|helios`, with zero matches. Scope read: Section 8 on journal p.17 (PDF p.9), its immediately surrounding prose, and references. This is a positive section-level admissibility screen, not a claim that keyword screening alone proves an entire paper clean. Printed PDF p.9 was visually inspected at `/tmp/lifetime-process-p9.png`.

Registered primary source: Lion et al., Stellaris design paper, DOI `10.1016/j.fusengdes.2025.114868`, KIT record https://publikationen.bibliothek.kit.edu/1000179851. Authoritative local PDF: `knowledge/concept_research/09-qi-stellarator-hts/iter-02/sources/publikationen-1000179851-172386752/tmpissrtbos/raw.pdf`; registered SHA256 `7fd72c1242ce3a17a9c4b9a4597fcb9ff5296b942b2d8343a0b463539d8d3865`. Printed pp.21, 28 and 29 were visually checked using `/tmp/lifetime-stellaris-p21.png`, `/tmp/lifetime-stellaris-p28.png`, `/tmp/lifetime-stellaris-p29.png`. These page numbers are PDF page numbers as well. Extracted Markdown tables are not the authority; the source index records their corrupted reconstruction history.

Additional primary software documentation checked: https://ukaea.github.io/PROCESS/eng-models/plant-availability/ (accessed 2026-09-07). The live page describes separate blanket/divertor replacement and unplanned outages, but its displayed ST availability equation uses the wrong sign for overlap. Its expression subtracts `U_planned*U_unplanned` from availability; the printed 2016 paper Eq.54 adds that overlap back. Use the printed equation and independent arithmetic, not that rendered formula. No PROCESS source code was adopted.

## What the model actually does today

| Surface | Current behavior and exact reference | Consequence |
|---|---|---|
| Damage driver | `models/library/analyses/mfe_account_costs.sysml:795`, `'Levelized Replacement Cost'`, takes the computed peak; generic binding `models/designs/generic_mfe/mfe_plant.sysml:931` | WI-041 already connected the right wall-load basis to lifetime, but only inside cost arithmetic |
| Physical life | `exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py:80` computes `clip(Phi/max(q,1e-6),0.5,N*A)` | Raw damage life, a numerical lower bound, and a horizon cutoff are currently collapsed into one value |
| Calendar interval | Same file: `L_cal=L_FPY/A` | Held availability schedules replacements; replacements cannot determine availability |
| Number and dates | Same file: `n=max(0,ceil(N/L_cal)-1)`; dates `k*L_cal` | End-of-life replacement is excluded, but no physical outage exists |
| Cost per event | `models/designs/generic_mfe/mfe_plant.sysml:921`, `(blanket.capital_cost+divertor.capital_cost)*n_mod` | Both components share one life and are wholly repurchased together; this is an inherited accounting assumption |
| Held availability | `models/designs/stellarator_09/stellarator_plant.sysml:1058`, `0.85`, cited to 1costingFE reference | Neither sourced Stellaris reliability nor a model output |
| Fuel | Generic plant `:894`, CAS80 binding; `verify_stellaris.py:589` | Consumption follows the same held availability |
| Energy | `models/library/analyses/mfe_lcoe_dcf.sysml:63`, `8760*P_net*A`; other LCOE channel in `mfe_account_costs.sysml:956` | Every fixed annual charge is divided by assumed production |
| Fixed O&M | `models/library/analyses/mfe_account_costs.sysml:403`, staffing-like power scaling, then CAS71 annual levelization | Staff costs are per calendar year, not per full-power year; do not multiply all O&M by availability |
| Oracle and package | `exploration/stellarator_e2e/verify_stellaris.py:350`, `:612`, `:628`, `:638`; generated handwritten stage above | Both calendar and costing need an independently derived verification path |

1costingFE pin `02543850089be175ea7c28b92a8b2a4184e1637e` is still the local HEAD. Its `_core_lifetime_fpy` is at `src/costingfe/model.py:102`; replacement annuity at `src/costingfe/layers/economics.py:53`; CAS72 composition at `src/costingfe/layers/costs.py:359`. `model.py:1522` leaves stellarator availability as an input; the disruption penalty that can alter availability is tokamak-only. This source provides a costing precedent, not the missing stellarator maintenance closure. Owner ruling in `.project/concepts/stellarator-demo-maturation.md` retires ongoing 1costingFE reproduction as a maturation duty.

The prior work's live question is already precise: `work/orchestration/goals/wall-and-heating/learnings.md:89` (L-011) records that the cost chain charges replacement capital but holds availability at 0.85 regardless of replacement count. Its size-matched wall/heating pairs are comparisons between different designs, not local derivatives. Preserve that distinction in reruns. WI-041 spec explicitly left availability coupling as a follow-on; WI-029 design documents the replacement, escalation and IDC conventions that must be restated when changed.

## Parameter readiness

| Quantity | Evidence, force and verification | Readiness |
|---|---|---|
| First-wall damage lifetime | Stellaris Table 6, printed p.21: peak 10.7 DPA/FPY and estimated first-wall structural life approximately 4–6 FPY; image checked | Source model estimate, not a demonstrated lifetime. Cross-check current life against this band |
| Existing fluence limit | `stellarator_plant.sysml:1109`: 18 MW yr/m²; 1costingFE `data/defaults/costing_constants.yaml:153`, legacy ARIES FS 200 dpa annotation | Admissible inherited library assumption; not independently established as the appropriate Stellaris material damage limit |
| Scheduled outage | Stellaris Section 2.11, printed p.29: preliminary overall estimate seven months for in-vessel assemblies including full breeder-blanket replacement | Best clean concept-specific anchor; suitable as a cited estimated input with sensitivity |
| Outage target | Same paragraph: five-month target, four-year operation between major maintenance, approximate 4.5-year cycle and 90% overall availability target | Target scenario and validation of intended arithmetic; cannot be relabeled achieved availability |
| Preparation/restart | Section 2.11, printed p.28: approximately 30 days cooldown, preparation within that period, approximately 30 days recommissioning | Supports overlap bookkeeping. These are inside the overall estimate, not extra downtime added to seven months |
| Scope of replacement | Section 2.11 pp.28–29: first-wall tiles, blanket modules and divertor plates; in-vessel work and hot-cell processing described separately | Supports bundled conceptual outage; exact correspondence to the full installed cost accounts remains an assumption |
| Divertor damage | Section 2.8 near printed p.20; extracted lines 1757–1759 report separate ARC/NRT rates | Separate allowable damage/erosion life has not been established. Do not derive divertor lifetime by applying first-wall material limits |
| Unplanned availability | No clean Stellaris plant-level failure/repair dataset established | Gap. Carry an explicit bounded assumption, not 0.85 relabeled as residual reliability |
| Replacement labor, handling, disposal | Operations described in Section 2.11; no unit cost model established | Gap. Current CAS72 only repurchases equipment. Separate future event costs from fixed staffing and initial spares |
| Magnet life | Table 6 p.21 also prints an approximately 10-FPY coil life on the stated 99th-quantile basis | Important remaining limitation for a 30-calendar-year plant. Requires shielding/lifetime disposition; bundling blanket outages does not settle it |

The agreement `18/4.05=4.444 FPY` with the paper's 4–6 band is a cross-check, not proof that the old 200-dpa annotation and the paper's ARC-DPA allowance represent the same damage convention. If a new damage coefficient is fitted to 4–6 FPY, label that as source-point calibration. Do not quietly swap NRT and ARC-DPA.

## Equations and domains

### Common physical basis

Define accumulated full-power time `f(t)=integral r_fusion(t) dt`, where `r_fusion` is power divided by the chosen full-power reference and `t` is calendar years. For a constant design point, online operation accrues one FPY per calendar year online. Damage is `D(t)=q_peak*f(t)` on the simple fluence model, and unconstrained physical life is `L=Phi_limit/q_peak`. During planned shutdown, `df/dt=0`.

Require `N>0`, `Phi_limit>0`, `q_peak>=0`, outage duration `d>=0`, cost per event `C>=0`, and residual productive fraction `0<b<=1`. Treat `q_peak=0` as infinite neutron-damage life. Invalid negatives are infeasible inputs; they are not repaired by replacing them with `1e-6`. A zero productive fraction must report zero energy and undefined/infinite LCOE, not crash or silently return a plausible cost. Discount support should cover `i=0` explicitly via `CRF=1/N`; today's formulas divide by zero there. If negative discount is supported, require `i>-1` and document it.

Keep physical life separate from the horizon. The existing `0.5 FPY` floor prevents a numerical gradient blowup; it is not a material property and can hide the very high-load economics this goal seeks to measure. A model-domain limit or explicit infeasibility flag is more honest than extending a component's life. The cap `N*A` becomes a circular dependency if reused as physical life in a computed-availability model. Retain end-of-life logic in the calendar instead.

### Option A: steady repeated-cycle approximation

For one bundled event of physical life `L`, duration `d`, and productive fraction `b=1-u` during scheduled-online periods, those periods take `x=L/b` calendar years. The complete cycle takes `x+d`. Thus `A_inf=L/(L/b+d)`, planned fraction is `d/(L/b+d)` and the unplanned fraction of total calendar time is `u*(L/b)/(L/b+d)`. These fractions sum with `A_inf` to one. This incorporates the fact that unexpected outages postpone the next damage limit.

A commonly used independent-fraction approximation is `A=(1-U_planned)*(1-U_unplanned)`. Its correct expansion is `1-U_planned-U_unplanned+U_planned*U_unplanned`, as PROCESS Eq.54 prints. If `U_planned` was computed from pure FPY as `d/(L+d)`, that is a different approximation from the clock model above. Declare which clock definition is intended rather than mixing their equations.

Illustrative arithmetic, not model runs or a proposed reliability prior: at `L=18/4.05=4.444 FPY`, seven months and `u=0,0.05,0.10` give repeated-cycle availability `0.883978,0.844679,0.804919`. Five months gives `0.914286,0.872310,0.829971`. Interpreting the paper's four years of operation as four full-power operating years for this illustration, five months off give `4/(4+5/12)=0.905660`; seven months give `0.872727`, before unplanned losses. The four-year phrase is an operating assumption in the paper, not measured FPY. The seven-month estimate therefore does not itself attain the 90% target.

Option A is inexpensive and useful for sensitivity or an independent asymptotic check. Its limitation is a smeared lifetime energy denominator paired with a discrete replacement numerator. Using `L/A_inf` for every replacement date puts the first event at `L/b+d`; damage actually reaches its first limit at `L/b`. That is an entire outage of timing error in the first cost event.

### Option B: deterministic finite-horizon calendar, recommended

Start at operation commissioning, `t=0`, with new in-vessel components already paid in capital. Advance a scheduled-online interval until its damage life is reached or the calendar horizon `N` ends. Over an interval of length `delta_t`, productive time increases by `b*delta_t`; unplanned downtime increases by `(1-b)*delta_t`. When damage life is reached, record an outage at that exact date. Charge the replacement event using a declared payment convention (outage start is the smallest continuation of the existing event convention), advance calendar time by the outage duration, and reset only replaced components' damage clocks. Nothing ages by fusion fluence during this outage.

For one identical bundled event, the kth outage starts at `t_k=k*(L/b)+(k-1)*d`, with `k>=1`. This offers a closed independent check on an interval-based implementation. Explicit end-of-life policy is needed: recommended initially, buy a replacement only if restart can occur strictly before `N`; if the final damage limit is reached too late for restart, cease production at that date and report early-retirement downtime instead of purchasing a terminal replacement. Other choices, such as a minimum profitable remaining run, are later optimization policies rather than implicit guards.

Return productive FPY `F`, planned downtime `T_p`, unplanned downtime `T_u`, terminal nonproductive time `T_terminal`, replacement count and dates. Verify `F+T_p+T_u+T_terminal=N`. The plant-average equivalent availability is `A=F/N`; annualized physical energy is `8760*P_net*F/N`. Event PV is `sum C_k/(1+i)^t_k`, then CAS72 equals `CRF(i,N)*PV` under the existing dollar convention. Do not pass average `A` back into the old periodic CAS72 function; that would construct a second calendar.

This produces finite-horizon cost and energy consistency on the project's existing annual-equivalent LCOE convention. It does **not** by itself give exact discounted energy for uneven yearly production. For exact DCF, use the same calendar to build `E_y` and calculate `PV_energy=sum E_y/(1+i)^y`, with matching dated fuel and other variable costs; then `LCOE=PV_total_cost/PV_energy`. The initial item should either implement that together, or keep the existing annual-equivalent convention and quantify the exact-DCF discrepancy as a shadow check. Preserve the owner's existing capital/IDC convention unless the new item explicitly restates a change.

An independent synthetic calendar check: set `L=4 FPY`, `b=1`, `d=7/12 yr`, and `N=10 yr`. Outages start at years `4` and `8+7/12`; restart occurs at `4+7/12` and `9+2/12`. There are two replacements, `7/6 yr` planned downtime and `53/6=8.833333 FPY` production, so finite-horizon `A=0.883333`. At `N=8.7 yr`, the second damage limit is reached at `8+7/12` and a replacement cannot finish before retirement: buy only the first replacement, accrue `8 FPY`, retain `7/12 yr` prior planned downtime, and report `8.7-(8+7/12)` terminal downtime. At `N=9+2/12`, restart would fall exactly on retirement, so the same one-replacement policy applies; just above this boundary, the second replacement is purchased. These intentionally discontinuous cases test the declared terminal policy and cannot be verified by the old `ceil(N/(L/A))-1` shortcut.

### Option C: separate component schedules and task/resource model

Give the blanket/first-wall assembly and divertor different lives and event costs. Trigger the earliest remaining life; a blanket event can also replace the divertor if the chosen maintenance policy says so. That is early replacement and must reset its clock and charge its cost, not silently extend it. Simultaneous tasks on independent workfronts can overlap; shared access, cooldown, conditioning and finite crews prevent arbitrary `max(d_blanket,d_divertor)` or arbitrary addition from being correct. General outage time is the union of occupied calendar intervals after precedence and resource constraints.

PROCESS p.17 supports the need for distinct lifetimes, combined maintenance and intermediate divertor outages. Its divertor load-to-life scaling is explicitly a weak scaling whose absolute values are not reliable. Its remote-handler count fit is for DEMO access, so it is not a Stellaris maintenance law. Option C should wait for a credible divertor lifetime/allowable and specific workfront data. Full stochastic RAMI simulation is a later option once failure/repair distributions are sourced.

## Cost and energy safeguards

- Keep initial installed first-wall/blanket/divertor in capital. Charge only subsequent replacements in CAS72.
- Replace the original 0.85 producer in every relevant consumer: fuel, replacement calendar, headline LCOE and comparison LCOE. Retain it only as an explicitly separate legacy comparison input if needed.
- Do not add lost electricity as a cost while also removing it from the LCOE denominator. Outage electricity imports would be a separate purchased-energy cost if modeled; that basis has not been established here.
- Keep fixed staffing costs per calendar year. Add actual maintenance labor, consumables and waste cost only after checking for overlap with staffing, capital spares and handling facilities. The current event base is installed component cost, not a detailed remove/replace invoice.
- Separate nominal/real dollar convention from calendar logic. Current CAS71 and CAS80 escalate; current CAS72 discounts a constant event amount without escalation. Either retain and disclose this inherited convention or change it explicitly across the related cash flows.
- Availability equals electrical capacity factor only for the modeled steady-state plant at fixed net power without load following, derating or separate pulse duty. Multiplying availability by thermal efficiency a second time is wrong after `P_net` already includes the cycle. `modeling_project/OVERVIEW.md` comparison-axis prose currently says “capacity factor = availability × thermal efficiency”; flag this as stale terminology rather than inheriting it into the new requirement.
- The neutron wall fence stays a material/physics constraint. Economic self-penalty alone does not prove a material regime feasible; the previous wall/heating evidence established this failure mode.

## Integration contract and implementation surface

Add a concept-agnostic lifecycle calc, plausibly `models/library/analyses/mfe_lifecycle.sysml`, with named inputs for peak load, physical fluence allowance, horizon, total scheduled outage, residual unplanned fraction and event cost. Put the Stellaris seven-month estimate and any selected reliability scenarios in `models/designs/stellarator_09/stellarator_plant.sysml`. Put the generic wiring and component replacement scope in `models/designs/generic_mfe/mfe_plant.sysml`. A first-wall/blanket/divertor bundled policy can be explicit without inventing a detailed new structural tree.

Required scalar outputs: `physical_life_fpy`, `replacement_count`, `productive_fpy`, `planned_downtime_years`, `unplanned_downtime_years`, `terminal_downtime_years`, `availability`, `replacement_cost_pv`, `cas72_annual`, and `annual_energy_mwh`; event dates and scope should also be available as a diagnostic artifact. Downstream bindings must read calc-output producers because of the exact-route codegen's existing alias limitations. Multi-output numeric projection itself is repaired, as recorded below.

Existing files requiring a coordinated change: `models/library/analyses/mfe_account_costs.sysml`; `models/library/analyses/mfe_lcoe_dcf.sysml` if energy convention changes; generic and stellarator plant files above; their byte-identical twins under `exploration/stellarator_e2e/models/`; the handwritten replacement/lifecycle implementation under `exploration/stellarator_e2e/generated/handwritten/`; `exploration/stellarator_e2e/verify_stellaris.py`; `exploration/stellarator_e2e/studies/oracle_entry.py`; snapshot/manifest/parameter surfaces; generated package, census and expected data; `data/traceability_matrix.csv` and validation rows in the modeling PM through its scripts.

WI-041 established that changing a handwritten calc interface makes codegen restencil it, so restoration and subsequent regeneration must be verified. The newer `.project/research/20260907-161438_numeric-evidence-merge-and-demo-follow-through.md` establishes that TEAx's schema-v3 numeric-exit repair merged on 2026-09-06 and the current burn-control record stores multi-output heating/sustainment numbers correctly. The remaining work is fusion-tea exporter adoption of `required_channels`, signature-aware exporter test invocation, and separate general executor-revision capture. The lifecycle study must use these publication contracts and verify actual persisted outputs. The upstream TEAx/sysml-codegen repair is not an unresolved lifecycle dependency. Schema-v2 historical records retain their original limits.

At the primary-cycle interface, `P_net`, `Q_source`, pumping work and component capacities describe the online design point. Lifecycle availability scales accumulated operation and sold energy; it does not derate those instantaneous loads before sizing the loop. If operating power varies within one lifetime, integrate both damage and electrical production over the actual state history instead of using one undifferentiated availability multiplier. Planned-outage auxiliaries, decay-heat cooling and grid imports need a separate operating-state boundary if later modeled; the first lifecycle increment should state their omission rather than treating every outage as a physically zero-heat, zero-flow condition.

## Verification and study matrix

| Case | Expected evidence |
|---|---|
| No scheduled outage, `u=0` | `F=N`, `A=1`; replacement cost can still be nonzero when replacement duration is zero |
| No damage (`q=0`) or life beyond horizon | No replacement, no planned outage, `A=b`; no division by zero |
| Positive short life/high wall load | More frequent replacement and reduced production; a half-FPY floor cannot silently flatten this effect |
| First event | Outage begins at `L/b`, not `L/A_inf`; no initial equipment charged again |
| End-of-life equality and adjacent floating values | Explicit strict-before-retirement event rule, no spurious terminal purchase, stable event count |
| Horizon ends during prospective outage | Applied early-retirement policy, time balance closes, no full event cost hidden behind an empty final run |
| Zero discount | Direct sum of event costs divided by horizon; compare against explicit time-discounted list for positive rate |
| Long horizon | Calendar mean approaches `L/(L/b+d)`; finite-horizon terminal effect reported |
| `u` and outage perturbations | Higher residual downtime cannot increase productive FPY; cost steps may move as events are deferred |
| Combined tasks | No duplicated cooldown/restart; combined event cost includes each purchased component once |
| Component split extension | Earlier of remaining lifetimes triggers; partial/early replacement resets only selected clocks |
| Energy/fuel bookkeeping | Fuel follows productive time; fixed staffing persists during outage; no lost-sales cost added twice |
| Package publication | Every named output present and finite where defined; declared zero/undefined cases explicit; model/package/executor pins captured |

Rerun wall/heating scenarios at a current accepted physics pin, including the two-sided burn condition. Preserve historical records at their old pins. Include fixed wall-plug arms (100 and 220 MW from the prior study) and fixed delivered-heating arms so heating-efficiency and lifetime consequences can be separated. Include the historical size-matched L-011 pairs as named transfer cases, alongside any new optima; do not claim they are nearest-neighbor derivatives. Cross source outage estimate (seven months), target (five months), declared longer-duration stress scenarios, and explicit residual-unplanned scenarios. A stress scenario is analyst evidence, not a sourced probability distribution.

Publish changes in wall peak, life, event count/dates, annual sold MWh, CAS72, CAS71, fuel and LCOE. Report which ranking changes come from lost production versus component repurchase and which come from integer replacement thresholds. A small wall-load transect across each threshold is more diagnostic than only optimizing the entire design grid. Hold geometry transfer assumptions and current wall fence explicit; if WI-044 changes the wall anchor, regenerate all lifecycle acceptance figures at its chosen pin.

## Feasibility, dependencies and decisions before a model goal

The arithmetic is tractable with the existing handwritten-stage pattern. The expensive part is making the time, cost and publication contracts coherent across every consumer and establishing what is assumed about failures. Rough engineering estimate [AGENT], not a commitment: 1–2 focused days for source capture/spec/design and a shadow clock, 2–4 days for calendar/cost integration and independent verification, then 1–2 days for review, source-sensitive study reruns and re-grade. Option A alone is smaller; component-separated schedules or exact DCF can expand the work materially. Exporter-contract follow-through and a stable geometry/power pin are integration dependencies; the numeric-exit runtime repair has already landed.

Proposed decisions for the next goal: bundled versus separate components; existing fluence allowance versus source-calibrated damage model; treatment and scope of residual unplanned downtime; five-month target versus seven-month estimate as the main scenario; cost payment time and escalation; terminal replacement policy; annual-equivalent versus exact dated energy; and disposition of divertor/magnet life. Recommendations above make these choices reviewable. No owner approval or source-derived reliability prior is claimed here.

## Candidate insights for approval

1. **Stellaris maintenance estimate differs from its availability target.** Context: Section 2.11 distinguishes a five-month target from a seven-month preliminary whole-outage estimate. Model implication: use an estimated outage parameter with explicit target/stress scenarios, not a fixed 90% result. Analysis implication: show the target gap before unexpected outages.
2. **A damage-life clock and a calendar clock must be separate.** Context: FPY is accumulated operation, while outage duration and discount dates are calendar time. Model implication: one calendar must drive both replacement costs and sold energy. Analysis implication: more frequent replacement can move both numerator and denominator; integer steps are expected behavior.
3. **Inherited numerical lifetime guards are not physical lifetime evidence.** Context: 1costingFE's 0.5-FPY floor is documented as a gradient guard and `N*A` as a horizon cap. Model implication: separate physical life, numerical domain and terminal policy. Analysis implication: disclose invalid high-load regimes instead of granting artificial life.
4. **Bundled in-vessel replacement is a bounded first model, not full plant lifetime closure.** Context: separate divertor behavior and the paper's limited coil-life estimate remain outside the wall chain. Model implication: expose component scope and unresolved life constraints. Analysis implication: distinguish availability under a specified maintenance policy from whole-plant reliability prediction.

No accepted DI entry was found that this work directly supersedes. L-011 is confirmed and extended; it is goal learning, not a registered DI. The overview's capacity-factor sentence and live PROCESS overlap typo are specific corrections to flag, not new model authority.

## Coordinator reading guide

Essential full-read files for synthesis: this draft; `exploration/stellarator_e2e/generated/handwritten/mfe_account_costs/levelized_replacement_cost_impl.py` (short executable contract); `models/library/analyses/mfe_lcoe_dcf.sysml`; `work/orchestration/goals/wall-and-heating/learnings.md` (especially L-011); `work/completed/20260905_WI-041_source-anchored-wall-load-fence/spec.md`; `work/completed/20260802_WI-029_handshake-lcoe-construction/design.md` if revisiting cost conventions. Source evidence is better read by the verified excerpts: Stellaris raw PDF pp.21, 28–29 and PROCESS raw PDF p.9/journal p.17, not their complete papers. Generic plant `:870–1015`, account costs `:795–890`, and oracle `:350–375`, `:580–640` are targeted implementation excerpts. The full giant plant/oracle files need reading by the eventual implementer, not by every research consumer.

Useful source URLs: https://publikationen.bibliothek.kit.edu/1000179851 ; https://doi.org/10.1016/j.fusengdes.2025.114868 ; https://scientific-publications.ukaea.uk/wp-content/uploads/Preprints/CCFE-PR1605.pdf ; https://doi.org/10.1016/j.fusengdes.2016.01.007 ; https://ukaea.github.io/PROCESS/eng-models/plant-availability/ . The new PROCESS PDF remains in `/tmp`; register/ingest only via the main research workflow if it is retained as model authority.
