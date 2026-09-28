# Plant-closure record synthesis

Date: 2026-09-12. Administrator: [AGENT] `/root/plant_record_administrator`, fresh record-only reader. Evidence version: frozen numerical record `e1ba37f4`, plus the post-record validation addendum committed at `59351f7d`. SHA256 of the committed [snapshot.json](snapshot.json) read: `1bd0c001f9a9eddf437baed223c51e91b787fac1cfbdf33b0cb1868ce8f5d40f`.

Scope: [administrator brief](reviews/administrator-brief.md). This reading uses only files inside this committed record. No model, oracle, package or runtime was executed or opened; no external reference or goal trail was followed. “Recorded” identifies retained observations; “Interpretation” identifies this administrator's conclusions; missing facts are stated separately. The completion addendum in [record.md](record.md) supersedes its opening preparation status; the later validation addendum leaves the numerical snapshot unchanged.

## What the study set out to do

Recorded objective: attribute the effects of the primary loop, cycle and lifecycle calendar at the design point and selected historical anchors; reread the inherited design window under fixed-loop and capacity-sized assumptions; expose fuel, divertor, vacuum and calendar consequences for a later engineering assessment. The intake records the owner ruling “Approve all four as sensitivities” for availability control, outage duration, unplanned downtime and burn fraction. Their absent resisting models remain findings. The other engineered controls and windows are agent-framed diagnostics. [Record intake and completed reading](record.md), [axis declaration](axes.json).

## What it found

Recorded coverage has three distinct layers:

| Evidence | Coverage and permissible meaning |
|---|---|
| Primary native result | 371 distinct risk-selected cases; 125 current old-ten, 19 intermediate-fourteen and 19 current-eighteen passes. |
| Complete oracle scan | Every inherited correlation and exclusion, under both loop assumptions. The reduced native selection covers all available predicate-view minima, 73 observed verdict patterns, 84 edge checks, comparison blocks and the calendar transect. |
| Stopped exhaustive native attempt | 2,525 completed cases; the first 844 independently checked. Ordered supporting prefix, excluded from primary counts; neither random nor representative. |

[Execution reading](execution-reading.md), [reduction amendment](preparation/reduction-amendment.md), [reduced selection](preparation/reduced-selection.json), [interrupted execution summary](results/interrupted-execution-summary.json).

Administrator static checks reproduce the native counts above, all eighteen predicate totals, the fourteen oracle groups’ counts/minima and the four complete factorials’ interaction residuals. Corner values match the native CSV. All nineteen full-predicate passes have physical TBR margin approximately −0.116, so the held-floor predicate does not establish breeding adequacy. [Native values](results/native-points.csv), [oracle summary](results/oracle-window-summary.json), [factorials](results/closure-factorial.json).

At the design point, the live closure yields 1,013.931933 MW net, primary LCOE 224.269233 $/MWh and 1cfe-form LCOE 220.012564 $/MWh. Installed heating is 100 MW wallplug / 50 MW coupled; signed operating demand is 98.159202 / 49.079601 MW. Source heat is 3,125.932277 MW, pump draw and recovered fluid work each 175.280934 MW, and IHX duty 3,301.213211 MW. The 480 °C cycle fit gives efficiency 0.411357; the calendar gives availability 0.902778, 27.083333 productive full-power years and five replacements. The design point fails divertor heat: 10.517842 against 10 MW/m². Its physical TBR is 1.074 against required 1.19; its coil-life margin is −17.083333 full-power years, which is also outside the eighteen-predicate acceptance set. [Baseline channels and verdicts](results/baseline_result.json).

The baseline all-held control uses pump 195 MW, recovered pump fraction 0.5, thermal efficiency 0.333 and availability 0.85. It uses the current operating-heating basis, so it is not a rerun of the historical installed-heating model. Historical cost differences also contain upstream revision changes. [Factorial inputs](results/closure-factorial.json), [historical comparison](results/historical-comparison.json).

| Anchor | All-held → all-live primary LCOE | Loop / cycle / calendar single effects | Combined change | Interaction residual |
|---|---|---|---|---|
| 20260907-minor-radius:c2823 | 199.016452 → 232.988396 | 179.607328 / -37.117261 / -9.855355 | 33.971944 | -98.662768 |
| 20260907-minor-radius:c3343 | Unavailable | Four held-loop corners execute; four live-loop corners excluded | — | — |
| 20260907-minor-radius:c3598 | 203.883704 → 285.871050 | 328.861145 / -37.964194 / -8.191946 | 81.987346 | -200.717659 |
| 20260907-minor-radius:c7752 | 208.931347 → 241.019183 | 176.954581 / -40.036493 / -7.878911 | 32.087836 | -96.951340 |
| baseline | 321.642816 → 224.269233 | -16.473862 / -74.307672 / -17.098515 | -97.373583 | 10.506466 |

All entries are $/MWh. Single effects are measured from all-held; the residual is the combined change minus their sum. Interpretation: the baseline benefit does not transfer unchanged to larger anchors. Loop penalties dominate those three anchors and interact strongly with cycle conversion. At baseline, the sequential loop → cycle → calendar contributions are −16.473862, −68.275313 and −12.624408 $/MWh. [All corners, pair and triple interactions for both LCOEs](results/closure-factorial.json), [capital/annual-cost/energy bridges](results/lcoe-bridges.json).

The unavailable c3343 live-loop corners are arithmetic exclusions, not evaluated predicate failures. The retained diagnostic classifies 195 unique complex-output cases: negative net power enters fractional cost powers and square-root land scaling. This diagnoses the numerical domain failure; it does not substitute an executed physical verdict. Excluded correlations remain outside all completed-case denominators. [Complex-domain diagnostics](preparation/complex-domain-diagnostics.json), [complete correlations](preparation/correlation.json).

The following are complete-oracle window results, with selected minima separately native-verified. The 10/14/18 columns are named predicate views, not interchangeable plant qualifications.

| Loop assumption / inherited arm / installed MW | Eligible / excluded | 10 / 14 / 18 passes | Old-ten minimum | Full-eighteen minimum (historical ID) |
|---|---|---|---|---|
| fixed / fence-p100 / 100 | 3624 / 127 | 291 / 132 / 132 | 183.715298 | 191.758169 (c0960) |
| fixed / reread-p220 / 220 | 360 / 0 | 76 / 42 / 42 | 230.937913 | 256.533374 (c7650) |
| fixed / search-p220 / 220 | 3623 / 127 | 522 / 227 / 227 | 189.137406 | 198.002590 (c4609) |
| fixed / transect-a / 100 | 34 / 2 | 6 / 0 / 0 | 197.779962 | None |
| fixed / transect-a / 220 | 35 / 2 | 10 / 0 / 0 | 202.283058 | None |
| fixed / transect-ash / 100 | 10 / 0 | 1 / 0 / 0 | 205.837741 | None |
| fixed / transect-ash / 220 | 5 / 0 | 2 / 0 / 0 | 217.456262 | None |
| sized / fence-p100 / 100 | 3690 / 61 | 294 / 132 / 132 | 160.600365 | 191.758169 (c0960) |
| sized / reread-p220 / 220 | 360 / 0 | 76 / 42 / 42 | 230.937913 | 264.896348 (c7650) |
| sized / search-p220 / 220 | 3689 / 61 | 524 / 224 / 224 | 163.803945 | 198.002590 (c4609) |
| sized / transect-a / 100 | 34 / 2 | 13 / 0 / 0 | 157.504066 | None |
| sized / transect-a / 220 | 35 / 2 | 21 / 0 / 0 | 160.532628 | None |
| sized / transect-ash / 100 | 10 / 0 | 1 / 0 / 0 | 198.768320 | None |
| sized / transect-ash / 220 | 5 / 0 | 2 / 0 / 0 | 209.864994 | None |

Costs are primary $/MWh. Fourteen and eighteen minima coincide in every populated group. [Full oracle rows and historical verdict flips](results/oracle-historical-comparison.json), [minima with inputs and aspect ratios](results/oracle-window-summary.json).

The full-set 100 MW minimum is c0960: R=12.7 m, a=1.7 m, coil current 13 MA, central electron density 4.048×10²⁰ m⁻³, ion temperature 14.63 keV, source efficiency 0.5, ash ratio 8 and 14 loops; aspect ratio 7.470588. The 220 MW search minimum c4609 has the same physical tuple with installed power raised to 220 MW. Their 1cfe-form costs are 188.126770 and 194.236275 $/MWh. The narrower 220 MW reread minimum c7650 retains R=12.7 m, a=1.3 m, 14.75 MA, density 4.554×10²⁰ m⁻³, temperature 14.63 keV, efficiency 0.6 and ash ratio 8; it uses 14 fixed or 12 sized loops. No full-set 120 MW minimum is established: that level occurs only in the reserve controls, with no full-predicate pass. All minor-radius and ash transect full sets are empty. [Window summary](results/oracle-window-summary.json), [held package inputs](results/package-inputs.json), [native arm counts](results/report-summary.json).

Calendar count changes are discrete. For the retained a=1.9→2.0 m pair, replacements fall 5→4 and availability rises 0.902778→0.914683; primary LCOE falls 179.796468→176.907586 for fixed loops and 174.381402→171.477386 for sized loops. These are sampled transitions, not solved continuous boundaries. The baseline replacement starts derived from stored operands are years 4.523926, 9.631185, 14.738445, 19.845704 and 24.952964 after operation begins. They are study-derived dates, not native scalar outputs. Computed mode requires restart strictly before the horizon; held mode retains periodic events. [Calendar steps](results/calendar-steps.json), [complete transect](results/calendar-transect.json), [derived event tables](results/derived-event-tables.json).

Both LCOEs retain finite discounted sums with discount 0.07, inflation 0.02, eight construction years and thirty operating years. Availability scales accumulated energy and fuel, not online loop or exhaust duty. The deterministic schedule and downtime settings are conditional envelopes, not reliability probabilities. [Finance ledgers](results/finance-ledgers.json), [execution reading](execution-reading.md).

## Framing verdict per axis

Recorded framing is sensitivity for all thirty axes; search framing is not applicable. The following conditional meanings are this administrator's reading of the declared controls and paired families. Aggregate bins combine coordinated changes and cannot establish causal slopes. Exact values, objective ranges and per-value violation counts are in [axis accounts](results/axis-accounts.json); paired identities are in [correlations](results/correlation.json).

| Axis | Observed values or extent | Framing and conditional meaning |
|---|---|---|
| `R` | 11.2, 12.7, 14.2, 15.7, 17.2 | Sensitivity; inherited geometry and sampled endpoint diagnostics, under model-owned common radius. |
| `T2_max` | 642, 750 | Sensitivity/control; upper domain bound changes with the complete cycle-fit choice. |
| `T2_min` | 135, 384 | Sensitivity/control; lower domain bound changes with the complete cycle-fit choice. |
| `T_i0` | 13, 14.63, 16, 17, 18 | Sensitivity; inherited plasma temperatures, coupled to other window coordinates. |
| `T_offset_fit` | 273 | Held control; printed logarithm offset, no independent response measured. |
| `a` | 1.3–3.2 (20 sampled values) | Sensitivity; inherited geometry and calendar transects; full-set transect has no feasible anchor. |
| `a_fit` | 0.1802, 0.4347 | Sensitivity/control; fit slope paired with intercept and domain, not an independent knob. |
| `availability_direct` | 0, 0.85 | Owner-approved sensitivity; 0 selects computed calendar, 0.85 held availability; reliability resistance missing. |
| `b_fit` | 0.7823, 2.5043 | Sensitivity/control; fit intercept paired with slope and domain. |
| `burn_fraction` | 0.025, 0.05, 0.1 | Owner-approved sensitivity; fuel throughput and cost conditional on absent processing-capacity resistance. |
| `cycle_live` | 0, 1 | Sensitivity/control; held/live conversion attribution at complete factorial corners. |
| `dT_approach` | 20 | Held control; 20 K approach, no independent response measured. |
| `delta_eta` | 0 | Held control; zero additional fit correction, no independent response measured. |
| `f_loss` | 0.8, 1, 1.2 | Sensitivity; representative hydraulic-loss scale, conditional on calibrated circuit. |
| `f_rad_total` | 0.8, 0.9, 0.95 | Sensitivity; engineered total-radiation sweep; full windows use 0.90. |
| `loop_T_in` | 476.15, 477.15, 573.15, 735.15, 736.15 | Sensitivity; temperatures test fit limits; fit-domain satisfaction is not materials qualification. |
| `loop_dT_blanket` | 166.6667, 200, 250 | Sensitivity; coordinated flow/temperature cases, not an isolated derivative. |
| `loop_live` | 0, 1 | Sensitivity/control; held/live pump and recovered-work attribution. |
| `magnet__I_coil` | 13000000–18000000 (10 sampled values) | Sensitivity; inherited magnet/plasma coordinates and sampled endpoint diagnostics. |
| `n_e0` | 303600000000000000000, 354200000000000000000, 404800000000000000000, 455400000000000000000, 506000000000000000000, 556600000000000000000 | Sensitivity; inherited density coordinates and sampled endpoint diagnostics. |
| `n_loops` | 6–56 (27 sampled values) | Sensitivity/sizing control; fixed versus capacity-sized circuit count without equipment cost optimization. |
| `outage_years` | 0.4166667, 0.5833333, 0.8333333 | Owner-approved sensitivity; 5/7/10 months; maintenance resources and access resistance missing. |
| `p_wallplug_heat` | 100, 120, 220 | Sensitivity/reserve control; installed procurement and capacity; operating demand remains separate. |
| `q_target_ref` | 5, 9.5 | Sensitivity; source alternative transport cases at fixed radiation; source-low results only at selected anchors. |
| `unplanned_fraction` | 0, 0.05, 0.1 | Owner-approved sensitivity; 0/5/10% residual downtime without a modeled reliability response. |
| `eta_source_heat` | 0.45, 0.5, 0.6 | Sensitivity; inherited conversion efficiencies, coupling efficiency held at 1.0. |
| `tau_ratio_ash` | 2, 4, 8, 12, 16 | Sensitivity; inherited residence ratios and source-shaped helium/electron profiles; no full-set transect anchor. |
| `p_pump_direct` | 0, 195 | Sensitivity/control; coordinated direct pump term with loop selector; no additional sound-negative ruling. |
| `eta_p_direct` | 0, 0.5 | Sensitivity/control; coordinated direct recovery fraction with loop selector; no additional sound-negative ruling. |
| `eta_th_direct` | 0, 0.333 | Sensitivity/control; coordinated direct efficiency with cycle selector; no additional sound-negative ruling. |

The 84 retained endpoint checks use six full-set anchors across fixed/sized fence, reread and search windows. At the 100 MW fence, both R and a endpoints, high current, high density and both temperature endpoints are caught; low current/density and held source-efficiency/ash endpoints are uncaught. At the 220 MW search, low temperature is also uncaught. In the narrower 220 MW reread, only low current, high density and high temperature endpoints are caught; singleton R/a and the remaining endpoints are uncaught. These patterns apply under both loop assumptions. No full-eighteen anchor exists for the a or ash transects. A failed endpoint is sampled predicate evidence; an uncaught endpoint remains uncaught. [Window-edge reading](execution-reading.md#window-edges), [edge evidence](preparation/window-edges.json).

## Constraint structure

The old-ten view comprises stress, conductor strain, recirculation, beta, positive net power, burn hold, wall load, held TBR floor, peak field and sustainment. Fourteen adds cycle domain, divertor heat, loop capacity and loop pressure. Eighteen adds separate lower/upper bounds for source and coupling efficiencies. [Qualified catalog](results/constraint-catalog.json), [historical comparison](results/historical-comparison.json).

| Qualified constraint | Satisfied | Violated |
|---|---|---|
| `stellarator_09__stellaris__wp_stress_ok__f38a102195da1dd0` | 358 | 13 |
| `stellarator_09__stellaris__cond_strain_ok__251d4c803804ab60` | 371 | 0 |
| `stellarator_09__stellaris__recirc_ok__afc3be66f0a3421b` | 264 | 107 |
| `stellarator_09__stellaris__cycle_domain_ok__ba3fa9c3653b3fd3` | 369 | 2 |
| `stellarator_09__stellaris__beta_ok__82b78aad420730d5` | 347 | 24 |
| `stellarator_09__stellaris__heating_couple_positive_ok__697e87be76f504b7` | 371 | 0 |
| `stellarator_09__stellaris__divertor_heat_ok__26b4658f9fdfd7b7` | 52 | 319 |
| `stellarator_09__stellaris__heating_source_upper_ok__14ddae450a8eda6f` | 371 | 0 |
| `stellarator_09__stellaris__net_positive__484521d56c02667a` | 371 | 0 |
| `stellarator_09__stellaris__burn_hold_ok__03c3f94b878e5b58` | 281 | 90 |
| `stellarator_09__stellaris__wall_load_ok__ab2c790419af93bb` | 308 | 63 |
| `stellarator_09__stellaris__tbr_ok__2cd198f674d413e4` | 371 | 0 |
| `stellarator_09__stellaris__heating_couple_upper_ok__6cc9307cc149d650` | 371 | 0 |
| `stellarator_09__stellaris__peak_field_ok__49c6b8228a73cac5` | 291 | 80 |
| `stellarator_09__stellaris__sustainment_ok__77add152ed8eafce` | 310 | 61 |
| `stellarator_09__stellaris__loop_capacity_ok__d77f6027ceb27852` | 188 | 183 |
| `stellarator_09__stellaris__heating_source_positive_ok__1e184791591370e5` | 371 | 0 |
| `stellarator_09__stellaris__loop_pressure_ok__5905ab54f5e8a945` | 371 | 0 |

Administrator recount from [native-points.csv](results/native-points.csv) matches [report-summary.json](results/report-summary.json). Counts overlap; failures cannot be added to obtain a unique rejected-case count. Divertor heat (319 violations), loop capacity (183) and recirculation (107) are the largest observed rejection counts in this selected set. Zero observed violations is conditional on executed inputs and exclusions.

Sustainment tests signed auxiliary demand against installed coupled capacity; burn hold tests the same demand against zero. Native stored energy uses W_th=1.5 p_avg V in MJ with source-shaped helium/electron profiles. Negative demand is not clipped. The held TBR-floor predicate passes 1.074≥1.05 while physical required TBR at default burn/recovery is 1.19. Fuel recovery remains 0.99. A radius-scaled divertor shadow is reported but never replaces the fixed-target predicate. [Baseline evidence](results/baseline_result.json), [interface limits](context/ANNEX.md).

## Findings carried forward

All IDs below have prefix `20260912-plant-closure#`. Dispositions and homes are recorded facts, not new routing or owner decisions. [Complete findings register](record.md#execution-findings), [machine-readable findings](preparation/findings.json).

| ID | Finding | Recorded disposition / home |
|---|---|---|
| 1 | No reliability resistance for computed versus held availability. | Owner-approved sensitivity only; reliability missing; unrouted. |
| 2 | No maintenance-resource/access resistance for outage duration. | Retain conditional 5/7/10-month comparison; unrouted. |
| 3 | No reliability response to residual unplanned downtime. | Retain conditional 0/0.05/0.10 comparison; unrouted. |
| 4 | Burn fraction lacks processing-capacity resistance. | Retain 0.025/0.05/0.10 sensitivity and fuel-capacity gap; unrouted. |
| 5 | 19 of 371 native cases satisfy all modeled predicates. | Sampled model satisfaction only; documented current-plant-comparison seam. |
| 6 | Representative loop/cycle lack separately sized costs and materials qualification. | Retain bounded source/calibration transfer; later assessment remains separate; unrouted. |
| 7 | Throughput and pressure-conditional pumping leave inventory, startup and vacuum train missing. | Retain missing source inputs and complete engineering questions; unrouted. |
| 8 | Required TBR/margin is separate from the held-floor predicate. | Retain conditional deficit without recovery tuning; documented breeding-adequacy seam. |
| 9 | Three changing direct controls were initially undeclared. | Corrected before baseline/scan; [pre-execution disposition](reviews/pre-execution-disposition.md). |
| 10 | Serial oracle scan stopped for performance. | Isolated parallel evaluations substituted; exact control equality retained; [operational note](execution/scan-operational-note.md). |
| 11 | Historical quarantine hashing violation and claim-specific audit limits persist. | No historical compliance or independent item-audit claim added; [consumer audit](context/consumer-audit.md). |
| 12 | Owner stopped exhaustive replay and requested reduction. | Primary counts use 371-case store; full oracle and stopped-prefix evidence remain separate; [reduction amendment](preparation/reduction-amendment.md). |
| 13 | Generic publication fixture requires an absent legacy API; focused validation is not green. | Executor proposes bounded numerical use with explicit API gap; direct-writer failure behavior and API compatibility remain tooling follow-up; [validation addendum](addendum/20260912-post-record-validation/reading.md). |

The fresh final review approved the executor's correctness, honesty and readability without a material correction. It expressly did not approve a then-unwritten final snapshot, administrator synthesis, grading or owner acceptance. This reading records that scope; it does not enlarge it. [Final review](reviews/final-review.md), [disposition](reviews/final-disposition.md).

## What the record does not support

There is no green validation-suite result. The post-freeze focused battery reports 130 passes / 120 failures; record-closure and numeric-evidence tests passed. Of the failures, 97 case names match the retained consumer audit, eleven concern the earlier radius record, eleven concern this plant record and one is the known narrative-reference check. The plant failures occur in a generic fixture before export: it expects module-level `CHANNELS` and later `export`, while this study uses `channels()` and [execution/execute.py](execution/execute.py). This is a test/entrypoint compatibility gap; it neither demonstrates missing published values nor certifies the local CSV writer’s failure behavior. The broader run was interrupted after 147 passes and one environment-sensitive precondition failure. The inherited broad-validation requirement remains incompletely met. The executor’s proposed bounded numerical use is a recorded proposal, not an administrator waiver. [Post-record addendum](addendum/20260912-post-record-validation/reading.md), [exact failure accounting](addendum/20260912-post-record-validation/test-accounting.json).

Missing engineering facts: achievable reliability/availability, maintenance staffing and access constraints, a resisting fuel-processing capacity, separately sized pump/pipe/IHX cost curves, qualified cycle materials, fuel residence inventories and startup stocks, and an installed vacuum train with conductance and capacity limits. Baseline vacuum speed 78.013726 m³/s is conditional on exhaust pressure 1 Pa and gas temperature 300 K. It is not equipment sizing evidence. The negative physical TBR margin and coil-life margin are not repaired by the modeled-predicate passes. [Baseline](results/baseline_result.json), [package inputs](results/package-inputs.json), [findings](preparation/findings.json).

Source/calibration transfer remains bounded. The representative helium circuit transfers a calibrated reference into this plant; its 129.4 MW fluid-work reconstruction differs from the source's 130.8 MW circulator total. Unity drive/extraction efficiencies make the electrical boundary a lower bound. The cycle comparison transfers complete printed fits: Rankine 0.1802 ln(T2_C+273)−0.7823 over 384–642 °C and sCO2 0.4347 ln(T2_C+273)−2.5043 over 135–750 °C, at zero additional correction. The Rankine benchmark adjustment is already inside the printed fit. Domain checks and arithmetic reproduction do not establish materials suitability or scientific validation. These facts are inherited from [the retained loop/cycle design](context/WI045-design.md); no underlying source was reopened.

No global optimum, continuous feasibility boundary, probability of success or buildability conclusion follows. The source-low transport result is anchor-specific; full windows hold radiation 0.90 and reference transport 9.5 MW/m². Fixed and capacity-sized loops are assumptions without optimized equipment costs. [Execution reading](execution-reading.md).

Numerical verification is extensive within its interface: the retained all-case result reports 141 oracle channels, eighteen rederived predicates, seventeen additional local scalar identities and physical/calendar/finance ledgers over 371 cases; the generic verifier checks 128 cases covering 73 observed verdict patterns and its named 25 channels. This administrator did not rerun either verifier. Seventeen extra outputs remain outside the shared oracle interface; 147 globally unsupported input overrides remain unsupported although every changing study input is mapped. Shared thresholds and source assumptions remain shared. Zero/equal-rate finance, multimodule and cross-concept normalization are not certified. [All-channel verification](results/all-channel-verification.json), [generic verification](results/verification_summary.json), [final review](reviews/final-review.md).

Re-execution cannot be reconstructed from this directory alone: the sealed package and runtime installation are not copied, and both native stores are local and gitignored. The committed reduced exports support this reading; they do not supply exhaustive native coverage of the full oracle window. Snapshot gaps explicitly retain these limits. [Snapshot](snapshot.json).

Historical audit/process scope remains unchanged. The retained consumer audit covers a bounded migration, reports historical failures and a forbidden seven-file quarantine hashing incident, and distinguishes corrected recurrence prevention from historical compliance. Implementation/integration evidence is not relabeled an independent item audit, and no scientific-use allegation follows from the hashing incident. This administration does not add source authority, resolve archival dependencies, grade the plant, mutate discovery records, accept a final packet or authorize reveal. [Retained consumer audit](context/consumer-audit.md), [executor scope](execution-reading.md#verification).
