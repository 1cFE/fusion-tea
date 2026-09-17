# ARIES comparison preparation and design-point checks

**Status:** Draft for owner review. **Date:** 2026-09-14. **Inspected branch:** `feat/integrated`, HEAD `3dda522e56b8c0a3cb57932b9903a9fb36554c60`. This document proposes preparation work; it does not open a modeling goal, approve residuals, change acceptance bands, or authorize reveal.

## Purpose and authority

[OWNER-VERBATIM] “Get a good defensible model that can reasonably be scaled/adapted to test against ARIES design points (physics and costing)” and “Then do the ARIES test.” [OWNER] Draft the comparison preparation and include some design-point checking.

[AGENT] Prepare a defensible fixed-design-point comparison: identify independent predictions, reconcile their physical and accounting meanings, exercise a few informative points, and explain where the model cannot support the comparison. Recommendations and proposed checks below are agent-originated, not settled requirements.

**Required reading:** [quarantine protocol](../../../knowledge/holdout/aries-cs/PROTOCOL.md), [ratified acceptance specification](../../completed/20260821_demo-anchor-acceptance-spec/spec.md), [current magnet transfer claim](../../../work/orchestration/goals/magnet-design-transfer/transfer-claim.md), [remediation assessment](../../../work/analysis/20260913-171817_fusion-audit-current-assessment.md). The remediation assessment predates the magnet work; its residuals must be reassessed rather than copied as current verdicts.

[INHERITED: acceptance specification B-0–B-8, ratified 2026-07-19] Structural correspondence, derived quantities and component costs remain the formal axes. Use model/reference ratios: derived quantities within [1/3, 3], component costs within [0.5, 2]. C220107 remains excluded or footnoted. Optimized sizing is a separate optional post-reveal exercise. A miss remains a finding; preparation cannot silently narrow the denominator of assessed quantities or change the bands. Use the explicit ratio endpoints for implementation; the specification's log10 shorthand is not exactly equivalent and should be flagged in any report-generator review.

[INHERITED: PROTOCOL §§3–6] Sealed content stays unread. This draft uses no ARIES-specific point values. After owner-triggered reveal, reference extraction and comparison-derived material belong only in the protocol's designated locations. Model corrections motivated by revealed content cannot improve the original frozen blind result.

## Starting evidence

[INHERITED: magnet transfer claim and study at `fa195fa4`] WI-040/038 have independently audited implementations and a 108-case transfer study. It establishes conditional numerical response at engineered points, not a source-qualified geometry interval or an engineering-qualified conductor range. Sixteen native outputs lack independent oracle computation. All five cases satisfying the eighteen modeled predicates use extrapolated conductor envelopes. Reuse this evidence with its actual pin and limits.

[INHERITED: transfer claim] The reported reference LCOE is now about 142.507 $/MWh. The change from the earlier baseline includes replacing an unsplit magnet estimate with selected procurement and winding-operation terms; it is not demonstrated cost savings. Reconciliation of that accounting change is a useful first check before comparing costs externally.

## 1. Comparison manifest

[AGENT] Build one table before reveal with the following fields for each comparison quantity. Reference-specific fields remain empty until reveal. Bind output names and units from the selected package contract rather than copying old flat keys.

| Field | Meaning |
|---|---|
| Axis and physical/account quantity | B-2, B-3 or B-4; precise quantity being compared |
| Model producer | Package channel(s), units, owning subsystem and source basis |
| Input or prediction | Whether the value is supplied, held, independently calculated, or derived from another compared value |
| Boundary | Included equipment, heat/power boundary, capital versus annual expense, plant-total versus per-module |
| Reference mapping | Publication location, units, included scope and extraction uncertainty; fill after reveal |
| Basis adjustment | Explicit unit, currency-year or accounting transformation with its source and calculation |
| Validity | Applicable configuration/technology, source range, extrapolation and held assumptions |
| Evidence and outcome | Independent check, raw values, adjusted values, ratio, formal verdict or unresolved applicability |

[AGENT] A quantity supplied to the model cannot also count as an independent successful prediction. For example, conditioning on reference fusion power may enable a useful downstream cost diagnostic, but it does not validate the fusion-power calculation. Keep raw observations alongside every adjustment. Missing scope or reference data stays visible; the existing contract does not authorize treating “not comparable” as a pass. An essential unresolved axis requires owner disposition before claiming criterion 4 met.

## 2. Cost and finance reconciliation

[AGENT] Start with the stellarator comparison path, using existing project accounting obligations. Broader IFE/general-MFE repairs are outside this proposed preparation unless the selected comparison actually needs them.

1. Map subsystem components into disjoint accounting leaves. Sum the leaves to their parents and plant totals without adding both an aggregate and its children. Track procurement, fabrication, installation, spares, replacements and annual expenses separately, including unpriced scope.
2. Reconstruct the current magnet estimate and explain the old-to-new baseline change as added, removed, replaced and retained terms. Do not fill missing manufacturing costs with an unexplained multiplier.
3. Reconcile overnight capital, reported construction financing, annual operating costs, dated replacements and each LCOE calculation. Preserve the headline DCF and 1costingFE-form conventions as distinct channels; their difference alone is not evidence of double counting.
4. Write the proposed common-basis fields: currency/year, real or nominal rates, escalation, construction timing, operating life, availability, module basis and account scope. Select values with the owner before reveal where possible. Specify the reference conversion procedure in advance; unknown reference conventions remain unknown rather than assumed equal.
5. Keep published-basis and normalized results separately labeled. Account mapping cannot omit a poorly agreeing component. Document C220107's treatment and its effect on any displayed aggregate.

[AGENT] LCOE is a supporting diagnostic in this preparation. It does not replace the ratified per-component cost axis or introduce a new formal LCOE pass band. Current mixed-module accounting needs either consistent treatment or an explicitly accepted single-module comparison scope.

## 3. Small pre-reveal design-point check

[AGENT] Reuse the existing transfer study and validated baseline. Add at most twelve new full-model evaluations initially, only where the existing evidence does not cover the proposed check. This is a diagnostic budget, not a coverage theorem or a new two-hour sweep. Write exact points, predicted responses and tolerances before execution; a failure triggers investigation rather than silently enlarging the grid.

| Check | Proposed selection | What it can establish |
|---|---|---|
| Reference reproduction | Reuse the accepted baseline; execute once only if the relevant model/package changed | Current channel mapping, quantities, verdicts and accounting totals reproduce their recorded meaning |
| Geometry response | Reuse matched major-radius and minor-radius cases from the 108-case study | Dimensions, field demand, inventory and cost respond as their recorded equations predict; explicitly retain quantities that remain held |
| Conductor response | Reuse matched envelope cases from that study | Relative sizing/cost response under the same REBCO construction; extrapolated envelopes remain labeled |
| Coupled point | One smaller and one larger joint geometry/current point already present; add only a missing comparison | Wiring works when several inputs change; this does not establish a realizable equilibrium |
| Engineering boundaries | Selected cases immediately inside/outside one applicable field, stress or loop-capacity limit | Correct crossing, deliberate invalid-domain handling and no false successful publication; numerical epsilon and physical tolerance are distinct |
| Plant/cost response | Small matched changes in heat load or cycle temperature and one replacement-calendar transition, only if not already checked at this lineage | Equipment/cost responses, thermal identities, availability and replacement accounting are consistent or expose held proxies |

[AGENT] Report each check in layers: execution completed/refused; independent numerical check; authored constraint verdicts; source applicability; remaining engineering qualifications. A completed evaluation is not a feasible plant. A refused point is not a numerical value to include in a ratio.

[AGENT] Independent spot checks should cover the comparison's load-bearing quantities: geometric dimensions/volumes, current-density-to-area identities with units, field/energy relations within their declared approximation, thermal/electric balance including pump-work conventions, availability-time accounting, material quantity × price, and capital/annual-cost reconciliation. Reusing the same generated expression twice is translation agreement, not an independent reference. Write absolute and relative tolerances based on units and numerical precision; do not use broad ARIES agreement bands to excuse arithmetic errors.

[AGENT] Before any expensive execution, show a compact table of existing evidence reused, new points needed, expected run count, and measured per-case runtime. Re-exporting a report or changing prose should not trigger model execution.

## 4. A synthetic comparison rehearsal

[AGENT] Test the report machinery with synthetic data in temporary fixtures, separately from physics execution. Include exact matches, ratios exactly at each band endpoint, just-outside ratios, missing quantities, zero/negative reference denominators, unit conversions, mismatched equipment scope and C220107 exclusion/footnoting. Check component sums and preserved raw observations. Synthetic reference values are test fixtures, never physical evidence or estimates of ARIES.

## 5. Actual design-point check after reveal

[AGENT] Freeze the model, executable package, input-selection rules, comparison manifest and formal bands before the owner triggers reveal. Record source applicability and remaining gaps at that version. Use the following sequence in the designated comparison artifacts:

1. Extract the reference design-point inputs, uncertainties, component definitions and cost/finance conventions with page-level evidence. Reconcile contradictory values before execution and preserve the discrepancy record.
2. Check representability: geometry convention, profiles, conductor technology, thermal cycle and module basis must have meaningful model counterparts. The current same-REBCO envelope study does not establish transfer to another superconductor; raising or lowering B_max alone is not a technology substitution. Unsupported reference technology/configuration becomes an explicit comparison limitation, not a silent surrogate.
3. Execute the frozen forward model with the declared reference inputs. Compare its independent outputs for B-2/B-3/B-4, retaining all constraint violations and extrapolation flags. Do not tune held coefficients to improve ratios.
4. If useful, run a separately labeled conditioned diagnostic: supply one reference subsystem output through a pre-existing supported input seam and examine downstream predictions. This can distinguish an upstream physics discrepancy from a cost discrepancy. It is not the blind forward result and cannot replace a failed formal verdict. No seam is invented after reveal to claim a better blind test.
5. Report the fixed-point comparison first. Optimization, redesigned geometry and vintage-assumption searches remain the optional Item 9 exercise.

## 6. Remaining limitations and proposed treatment

| Area | Proposed treatment before reveal | Why it matters |
|---|---|---|
| Magnet geometry and technology | Inventory supported inputs and source applicability; price selected component scope explicitly; seek additional evidence only for a declared transfer claim | The current conditional REBCO study cannot establish another conductor technology, pack/casing fit or arbitrary configuration validity |
| Breeding | Distinguish required from achieved TBR; retain negative adequacy margins and held neutronics | A geometry-driven power/cost prediction can be reported conditionally; self-sufficiency is not established |
| Coil lifetime | Show productive-life demand versus the retained allowance; identify absent shielding/replacement consequences | Lifecycle economics may omit a material replacement or operating restriction |
| Thermal equipment | Check that changed heat duty has a corresponding equipment-cost response or label the retained proxy and unpriced scope | A physically responsive loop calculation can still underprice the larger plant |
| Maintenance | Reconcile the implemented bundled calendar; disclose unmodeled equipment, access and reliability | Availability scenarios are assumptions, not reliability predictions |
| Accounting and finance | Resolve mappings and comparison conventions; retain irreducible scope differences explicitly | Agreement can otherwise result from incompatible cost boundaries |

[AGENT] Fix errors in the existing comparison path before freezing it. Additional capability work should answer a specific missing comparison obligation. Owner acceptance is needed for residual scope and finance choices; merely listing an issue here does not resolve it. The reviewed magnet answer is conditional, and work-item closure does not convert its residuals into accepted engineering assumptions.

## Review decisions and delivery

[AGENT] Recommended immediate deliverable: the filled model-side manifest, an accounting bridge for the current baseline, an evidence-reuse table plus the small check plan, and a residual/applicability table. Run the synthetic rehearsal and only the justified missing points after that plan is reviewed. Refresh the depth assessment at the chosen freeze when relevant evidence has changed; reuse unaffected checks.

Owner decisions to make concrete from this packet: which conditional claims are acceptable for the demo; the common monetary/finance basis and normalization procedure; supported module/configuration/technology scope; and which essential gaps require work before freezing. Reveal remains a separate owner act. This draft does not require every engineering gap to be filled, and it does not imply that accepted limitations satisfy a formal comparison axis they prevent us from evaluating.
