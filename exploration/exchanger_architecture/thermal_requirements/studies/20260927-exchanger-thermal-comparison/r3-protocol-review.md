# Round 3 independent protocol review

2026-09-27. [AGENT] Continuing independent reviewer. Scope: `r3-study-contract.md`, `r3-cost-boundary.md` and the accepted WI-097 design. Reused the source and design reviews, including the corrected finite-transfer oracle requirement. No changing implementation code was inspected and no main study was executed.

**Verdict: PASS for study preparation. No blocking scientific or accounting flaw found.** Native execution remains subject to the accepted design's implementation and integration checks. The recommendations below make the finite candidate plan concrete; they are agent-selected study choices, not new source requirements or an owner gate. Record adopted values and any changes in preparation before main results are ranked.

## Fair comparison and scope

- Freeze the accepted design catalogue: original UA `(50,50,50)`, offer A `(12,12,2)` and offer B `(18,18,2)` MW/K at U=1000 W/m²/K. Corresponding selected areas are `(50000,50000,50000)`, `(12000,12000,2000)` and `(18000,18000,2000)` m². The older tuples in the cost memo are explicitly examples and must not enter preparation as additional accepted offers without a recorded amendment.
- Give both architectures every common load, offer, flow range, controller limit, conductance assumption and fuel/finance setting. Keep the network split as its legitimate extra operating freedom. Retain equal-flow passing pairs as a diagnostic alongside each architecture's independently selected best passing operation, as required by the design. At equal flow and complete heat acceptance, the ideal cycle should give equal electricity under common losses; a discrepancy requires explanation before ranking.
- Use common loads 1650, 1835.4512830147435, 1950 and 2000 MW. Keep 2200 and 2300 MW as explicit source-cap failures. Original-inventory controls should execute first for both topologies. The already reviewed `Q >= UA*30` contradiction supports the original divertor's infeasibility throughout the stated capped source domain; a large original-inventory mesh adds little to that proof.
- Compare best operations within each common offer before comparing offers. Equal retained purchase budgets do not establish which inventory is available or cheapest to procure. A network-only passing region supports a tested feasibility difference, with no paired LCOE or allowance against a failed series case.

## Practical finite search

An initial native candidate mesh of secondary flow 1100–1650 kg/s in 25 kg/s steps and network split 0.40–0.90 in 0.025 steps gives 4048 distinct maps across four loads and two offers: 23 flow values × (one series map + 21 network splits) × eight load/offer groups. Add original and source-cap controls separately. This is a practical starting domain based on retained development evidence, not a physical search bound.

Before freezing that mesh, use the independent oracle to inspect margins between samples and at domain edges. Retain the known passing development points and seed candidate interiors from the reviewed admissible-UA conditions so that a coarse mesh does not discard a known narrow feasible window. Extend a flow or split edge when its margins or objective trend leave a potentially competitive region open, subject to actual input and purchased-equipment bounds. Record whether each stopping edge is a model bound, a justified analytic exclusion or an unresolved study boundary. Oracle-proposed candidates must still pass native evaluation and independent verification.

Refine every sampled component that could compete with the leading objective, including relevant failures on either side. For network cases, refine flow and split together; following only the currently best coarse split can miss a lower-flow feasible window. Use local subdivision and explicit neighboring failures rather than assuming a single globally monotone feasible interval. A failed coarse group alone is insufficient evidence of continuous infeasibility.

Retain the protocol's final targets: flow brackets at most 0.1 kg/s and relevant split spacing at most 0.001, followed by halving both spacings and checking net-output movement below 0.2 MW and LCOE movement below 0.1 USD2004/MWh. Report the actual changes and unresolved bounds for both architectures. For an advantage claim, use the combined observed refinement uncertainty of the pair, not only the network's change. These are empirical stability checks within explored regions, not a global error bound. A practical retained-map cap of 12000 for the main comparison and local refinement can be declared in advance; if exhausted, preserve the unresolved regions and report best-tested cases. Sensitivity cases should have a separately declared allowance rather than silently consume the main refinement budget.

## Finite sensitivity set

Start at the exact N load for both offers, then repeat the scenarios that materially change the comparison at the highest common passing load. Apply the same operating search permissions to both topologies and reselect operations when feasibility changes. A scenario with no passing pair remains a failed or unresolved comparison; do not substitute the failing old leader's cost.

| Effect | Suggested finite scenarios | Interpretation and checks |
|---|---|---|
| Approach requirement | 15, 30 and 45 K at all six primary-HX terminals | Separate conditional requirements; keep returns, caps and selected equipment unchanged. |
| Conductance | Common U multiplier 0.8, 1.0 and 1.2 at fixed area; then vary the binding branch alone at the same endpoints | Constant U under changed primary flow is an admitted model assumption. These points illustrate sensitivity and do not bound actual heat-transfer uncertainty. |
| Cycle pressure loss | Common supplied loss at its retained baseline and ±0.02, clipped to the valid domain; separately add network-only increments 0.01 and 0.02 to baseline | Preserve the native parameter's meaning and permitted domain. Common-loss cases test operating robustness; differential cases expose an omitted topology penalty. Neither predicts piping losses. |
| Primary pumping | Multiply supplied primary pump powers together by 0.8 and 1.2, preserving each native recovery rule; inspect any newly binding individual loop | Recompute delivered duties, required hot states, accepted heat and net electricity. Record equipment failures and which electrical/recovered-heat terms changed. No automatic bypass pump saving. |
| Controller range | Common per-loop maximum bypass fractions 0.75, 0.90 and 1.0; refine a decisive limit around the observed required fraction if these change feasibility | Apply identical supplied bounds to both topologies. Report all three solved requirements; these limits are analyst scenarios, not valve ratings. |
| Pump boundary convention | Main aggregate returns and the explicitly post-pump alternative | Subtract the actually booked recovered pump heat divided by total primary heat-capacity rate from each target, leave delivered duty unchanged and rerun. If combined with a pump-power scenario, recompute this shift from that scenario's heat recovery. |
| Fuel and HX prices | Nominal and zero tritium price; retained-budget and inherited linear area-price cases | Zero price must cover both initial stock and purchases. Price-only cases may reuse a verified thermal operation but must retain complete native cost accounting and extrapolation status. |

These values are recommendations for a bounded experiment, not requirements inferred from Raffray. Begin with one changed assumption at a time. If more than one perturbation materially threatens the same reported advantage, add a small combined adverse scenario and reselect operations rather than presenting separate one-factor successes as joint robustness. Preserve numerical failures separately from engineering failures.

## Allowance arithmetic and missing scope

The cost memo's two-sided equations are correct. With annual represented cost `A_i`, unrepresented incremental annual cost `B_i`, and adjusted annual electricity `E_i`, network break-even is `B_N = (E_N/E_S)*(A_S+B_S)-A_N`. If `B_S=B_c` and `B_N=B_c+DeltaB`, then `DeltaB_max=(E_N/E_S)*A_S-A_N+B_c*(E_N/E_S-1)`. A common unknown cost does not cancel when electricity differs.

For each passing pair, retain the algebraic dependence on the common cost and show explicitly labelled slices, for example `B_c=0` and `B_c=0.1*A_S`. Such a slice is illustrative, not a procurement estimate. Report signed allowances; a negative allowance means the chosen network case already needs a cost advantage to tie. State annual cost units, year-dollar convention and whether a displayed capital equivalent is direct or overnight. The memo's direct-purchase conversion `g_D=0.103144848466/year` applies only under the declared finance, generic overhaul and terminal assumptions, with extra maintenance/replacement accounted separately.

External purely dissipative power can enter the annual-energy denominator once. Coupled pump or pressure-loss changes must come from their re-evaluated native case, so their electrical effects are not subtracted a second time. Both adjusted net outputs must remain positive. Added scope is incremental beyond the retained piping, secondary-transport and control allowances; zero represented increment does not establish free hardware or complete existing coverage.

## Release boundary

Preparation should retain the final catalogue, numerical domain, explicit scenario inputs, candidate-selection rules, evaluation budget and source/control/price provenance. Main execution may proceed after the accepted native integration release, with complete verification of retained candidates and the design's original-inventory numerical failure fixtures. Final review must check actual refinement receipts, matched passing pairs, equal-flow consistency, sensitivity reselection and allowance inputs before accepting an architecture conclusion. No additional scientific choice requires owner approval under the recorded delegation.

## Preparation-script follow-up

The coordinator subsequently requested inspection of `r3-prepare-study.py`. This is preparation code, not the changing native implementation. Its wider initial oracle domain, flow 500–2400 kg/s by 50 and split 0.10–0.90 by 0.05, is a reasonable replacement for the suggested initial mesh above. It keeps explicit proposal maps and distinguishes oracle scouting from native evidence. Refining every observed pass/fail transition and every coarse split-local maximum is an appropriate start. The stated final flow bracket of 0.025 kg/s exceeds the requested resolution.

**Preparation verdict: FINDINGS. Correct P1 and P2 before treating its selected cases as the accepted refined comparison.** These are executable search issues; the scientific protocol remains accepted.

### P1 — Coarse misses currently stop the search

`line()` only refines flow intervals whose endpoints differ in pass status. `search()` only refines split if a coarse line has a pass. A feasible interval narrower than 50 kg/s can sit between two failures; if this happens on every coarse split, the group receives no local search. The retained development evidence already supplies useful passing seeds and the design provides admissible-UA interval conditions.

Add known passing development operations to the relevant load/offer lines and locally refine around them even if the coarse mesh finds no pass. Use oracle thermal margins or the admissible-UA conditions to seed promising same-status intervals, including sensitivity groups. For a group still without a discovered pass, record the additional interval checks and retain the claim as no pass found in this sampled domain. A native failure of a former thermal-only passing seed is useful evidence, not a reason to silently discard its neighborhood. A complete global proof is not required.

### P2 — Final neighbors must update selection and stability evidence

`search()` proposes final split neighbors but never compares them with the selected best case. A better passing final neighbor can therefore be executed while `best_scan_id` still identifies an inferior point. Update the final selection across all passing final probes, and refine the flow boundary at any newly competitive split rather than testing its split only at the old flow. Iterate until the stated local stopping rule or declared budget is met.

The split refinement list records values at 0.005, 0.001 and 0.0005 spacing, but the script does not assess the 0.2 MW/0.1 USD/MWh stability targets, and its final flow probes do not retain an explicit halving receipt. Record and classify both resolutions' objective changes, the selected coordinates and the remaining neighboring failures. Combine both architectures' changes when reporting a paired advantage. A cap exhausted before stability is an unresolved refined comparison, not a precise winner.

### Other preparation details

- The existing `edge_passes` field is useful. Turn a competitive boundary pass into edge expansion or an explicit unresolved-boundary classification. Refinement around a boundary split may extend beyond 0.10–0.90, but that does not itself show the full admissible split interval was checked.
- `propose()` currently excludes every nonpositive-net oracle case, including deliberately requested scan-edge controls. Preserve finite executed failure controls when selected, or record their deliberate exclusion and reason separately; positive-net is a ranking condition, not a general evidence-retention condition. Refused oracle cases should remain visible and must not be silently relabelled engineering failures.
- The catalogue is correctly frozen to original/A/B. The coordinator has committed to add equal-flow passing pairs and correct the post-pump input keys before execution. Verify the alternate return shift against the evaluated recovered-heat channel, especially if later combined with a pump multiplier.
- The initial scenario list uses common loss 0.02/0.08 and bypass limits 0.25/0.50. These are defensible labelled analyst scenarios in place of the recommendations above. Differential pressure loss still needs an explicit matched comparison: the network at changed loss against series at baseline, as well as the common-loss pair. Restricting the first sensitivity search to offer B at N is acceptable as an initial tranche; do not extend its robustness claims to offer A or higher loads without checking the decisive cases there.
- Add an explicit evaluation budget and checkpoint strategy before a potentially long oracle scan. The retained outputs should state how many groups completed and which refinement or sensitivity work remains if that budget is reached.

This follow-up does not introduce an owner gate. P1/P2 can be corrected under existing delegated authority, after which a narrow recheck can release the preparation result. Native implementation review and preflight remain separate execution gates.

## Corrective preparation recheck — 2026-09-27

**Verdict: PASS for oracle scouting and preparation. P1/P2 are substantively resolved.** The script parses successfully. I checked the retained development file: all 697 thermal-passing seed rows contain the required keys, use the expected matched-small/matched-medium offer names and carry integer topology modes. This review did not run the physics scan or certify any selected result.

P1: `line()` now includes known passing development flows for their matching load, offer and split, including recomputation under sensitivity scenarios. Same-status failed intervals in the 900–1800 kg/s neighborhood receive quarter, midpoint and three-quarter samples, reducing their initial spacing to at most 12.5 kg/s. Every observed transition is then bracketed to 0.025 kg/s. This is adequate for the declared finite, sampled-domain experiment. It does not prove that narrower islands or outer-domain islands are absent; retain that limit for groups without a found pass.

P2: final split neighbors now compete for the selected result, and their flow lines are searched again. The final `best_scan_id` follows those comparisons. Refinement levels, objective changes and explicit stability booleans are retained. A failed stability check must trigger further refinement or an unresolved classification before a quantitative advantage claim; the script's ability to propose such a point does not make it accepted.

One receipt needs careful interpretation: `flow_halving` currently includes any subsequent improvement obtained by changing split. It is a combined final-neighborhood change, not an isolated flow-halving experiment. Label it accordingly. If the winning split changes during the final sweep, check the final half-flow-step neighborhood at that winning split before reporting completed refinement. This is a final-result verification obligation, not a reason to block the initial oracle scan.

The script now declares a 200000-point oracle limit and checkpoints each completed search group. A budget interruption within a group can leave that current group's rows unwritten; keep completed checkpoints and label the unfinished group unresolved rather than treating partial memory state as complete evidence. Equal-flow controls have been added; their passing status must be checked, since increasing flow by 0.1 kg/s does not prove continued feasibility in a nonmonotone domain. The post-pump heat-capacity inputs now refer to the exchanger assembly's supplied primary flows and specific heats; the resulting recovered-heat shift still needs numerical confirmation during preparation.

The coordinator has retained the obligations to expand or disclose competitive search edges and to record why nonpositive-net controls were excluded from native proposals. Those exclusions remain visible in the oracle scan, but `propose()` itself still returns without an exclusion receipt. Record the reasons in the preparation evidence before execution release. Final all-point native verification, matched comparisons, actual refinement receipts and the separate implementation/preflight gates remain required. No renewed owner choice is needed.
