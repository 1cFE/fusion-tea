# Review — stellaris-evolution.html

page: /home/reid/1cfe/fusion-tea/docs/write-up/stellaris-evolution.html
source: /home/reid/1cfe/fusion-tea/docs/write-up/stellaris-evolution.md
reviewed against: docs/write-up/html-render-prompt.md, docs/write-up/writing-prompt.md, docs/write-up/write-up.css, /home/reid/.claude/skills/_my_mental_model_v2/feedback/html.md, /home/reid/.claude/skills/_my_mental_model_v2/feedback/synthesis.md

## Findings

1. Section 5, first bullet, leaves “Part 3 walks this goal.” as plain text. The opening links Part 3, but this later reference has no working link. (Cites: writer prompt, “Turn a reference to another section into a working in-page link”; shared HTML feedback, “Concept left for the reader to scroll for,” which requires section references to work as links.)

2. The evidence summary at `#frame-record` reads “All 29 frames: counts and recorded results.” It repeats the rejected pattern of a count and colon-joined summary instead of a plain heading. (Cites: writer prompt, disclosure summaries; shared HTML feedback, “Dropdown summary line written as a double clause,” explicitly including counts.)

3. The page includes large inline styles for toolbar, panel typography, colors, warnings, buttons, source labels and code presentation, as well as diagram layout. Examples are `.panel h3`, `.warning`, `.evo .evo-src`, and `.evo pre`. The shared stylesheet is linked, but these additional presentation rules exceed the permitted small style block for diagram layout. The support-specific exception exempts viewer scripts, without granting an equivalent style exception. (Cites: writer prompt, “Style” and “Part 4, support 1.”)

## Mechanical fidelity check

Compared all 37 source blocks (7 headings, 9 paragraphs and 21 list items) with static article blocks in DOM order. All match after the permitted repository-link replacements and the visual spacing between heading-number spans and heading text. No source blocks were dropped, reordered or reworded. All seven source headings retain their GitHub-style anchors. The main-post link remains `.md`; support links use `.html`. Frame references become links to frame records. The source has no tables, figures or code blocks.

This check covers static article HTML. Inline vendor code and embedded snapshot payloads were not printed or treated as article prose. Viewer scripts are exempt as specified. No domain-source verification was attempted.

## Added text inventory

### Page metadata and contents rail

The browser title is “Stellarator model evolution”. The rail adds “1cFE write-up · Part 4”, “Modeling Stellaris”, “↗ Model evolution viewer”, and “↗ Frame records”, and repeats the six numbered source section titles.

### Viewer before section 1

Model evolution viewer

Step through the goals with the slider or arrows. Select a part to open it, then select a calculation to see its inputs and equations. Frame links in the themes return here. Expand gives the graph the whole window.

The interactive graph needs JavaScript. All six themes and the frame records below remain available.

Static toolbar labels: “Snapshot” (hidden file picker), “Expand all”, “Collapse all”, “Fit”, “Reset layout”, “Spacing”, “1×”, and “Find”.

### Sections 1–6

No new narrative text. Each repository citation replaces its link with its original label followed by a colon and the repository path, such as `record: work/orchestration/goals/magnet-closure/trail.md`. The block comparison includes every such replacement. Frame numbers acquire links without new wording.

### Frame records after section 6

In the record All 29 frames: counts and recorded results

Counts come from each committed snapshot. Results below are the viewer’s agent condensations of the cited records; they have not been owner-reviewed. The six themes above use the checked write-up text.

Table headings: Frame; Calculations / checks / parts; Recorded result and source.

#### 1. Starting point: the migrated model

Counts: 55 / 6 / 14.

The model as the first goals found it: 55 calcs and 6 checks, every calc scoped to the plant root. It follows the migration to the current snapshot format and work item WI-030, which added a computed volume-averaged beta and a conductor peak-field limit. The first two goals, cryo-volume-basis and p-pump-basis, examined this version. p-pump-basis found the 1 MW pumping power indefensible and routed the fix to WI-033; the regenerated model first appears in the next frame.

Source text: commits 89f78130 and ba5c9945; work/orchestration/goals/cryo-volume-basis/; work/orchestration/goals/p-pump-basis/; .project/completed/CHANGELOG.md (Goal Harness Item 5)

#### 2. Rerunning the model with pumping power corrected to 195 MW

Counts: 55 / 6 / 14.

The goal regenerated the model package so it carried the pumping power already corrected from 1 MW to 195 MW, then ran a study on it. The recirculating-power check now fails at 184 swept points instead of 32. LCOE at the baseline design rose from 275.264 to 333.067 $/MWh (+21.0%), with all six checks still passing there.

Source text: work/orchestration/goals/p-pump-fence/trail.md § Round 1 result — 2026-08-29 (Last semantic outcome); § Goal close — 2026-08-29

#### 3. Deriving the magnets from their own design

Counts: 60 / 7 / 14.

The magnet's field, a structural limit and its cost now come from the coil design instead of cited constants. The on-axis field is computed from coil current and geometry, a winding-pack stress check pushes back on coil sizing, and magnet cost is split into separately sized accounts. Baseline LCOE fell from 333.067 to 304.482 $/MWh.

Source text: work/orchestration/goals/magnet-closure/trail.md § Round 1 result — 2026-08-30; § T-004 return — 2026-08-30; § Goal close — 2026-09-01

#### 4. Checking the plasma operating point against the machine

Counts: 61 / 8 / 14.

The plasma operating point is now checked against the machine instead of typed in. A confinement relation (ISS04) links field and heating to density and temperature, and a new sustained-heating check pushes back. The study found no feasible point at the printed 50 MW of installed heating; feasibility returns at about 91 MW.

Source text: work/orchestration/goals/operating-point-closure/trail.md § Goal close — 2026-09-02; § Round 2 result — 2026-09-01 (L-005)

#### 5. Making the escape levers carry real costs

Counts: 65 / 9 / 14.

The winding pack is now sized from coil current, the cold volume is computed, and a conductor strain check was added; the design point did not move. The study still found no feasible point at the printed 50 MW. There the neutron wall load alone blocks 27 of 240 points, the conductor limit 6. The goal closed by redirect.

Source text: work/orchestration/goals/priced-levers/trail.md § Round 1 result — 2026-09-03; § Goal close — 2026-09-03; work/orchestration/goals/priced-levers/goal.md § Amendment 2026-09-03

#### 6. Making the wall-load and heating checks honest

Counts: 68 / 9 / 14.

Heating became a real chain from wall-plug power to plasma-coupled power, and the wall-load check now compares a computed peak with the paper's printed peak. The machine as designed then slightly fails the wall limit (4.088 against 4.05) and baseline LCOE rose from 307.087 to 313.513 $/MWh. A working point at the printed heating needs a fatter plasma.

Source text: work/orchestration/goals/wall-and-heating/trail.md § Goal close — 2026-09-05; § Round 2 result — 2026-09-04; commit cb355321 message (LCOE figures)

#### 7. Why the stored energy ran 9% high

Counts: 68 / 9 / 14.

The model's stored energy sat 9% above the paper's printed value because the helium ash was given the fuel's flat profile; the printed value is not a target. Computing the ash profile from the paper's own rule dropped the required heating from 90.6 to 49.1 MW against a 50 MW limit. Both failing baseline checks now pass, with nothing tuned.

Source text: work/orchestration/goals/stored-energy-basis/trail.md § Goal close — 2026-09-06; § T-001 return — 2026-09-05 (round 2)

#### 8. Ruling out plasmas the heating cannot hold

Counts: 68 / 10 / 14.

The sustainment check became two-sided: the heating a point needs must be zero or positive, and no more than what is installed. No number changed; at all 7,712 re-run points the new check failed exactly the ignited ones. The cheapest feasible machine stayed at 202 $/MWh, and the machine as designed needs 49 of its 50 MW.

Source text: work/orchestration/goals/burn-control/trail.md § Goal close — 2026-09-07

#### 9. Making a fatter plasma cost something

Counts: 70 / 10 / 14.

The magnet chain now computes conductor peak field, stored magnetic energy and casing mass from the coil bore, anchored so the design point reproduces exactly. A fatter plasma is caught by the conductor limit only where the bore is large relative to the major radius. The cheapest machine is unchanged at 202 $/MWh, because there the bore is nearly free.

Source text: work/orchestration/goals/minor-radius/trail.md § Goal close — 2026-09-08

#### 10. Compute the plant's pumping power, cycle efficiency and availability from the design

Counts: 76 / 14 / 14.

The goal replaced three fixed plant multipliers (pumping power, cycle efficiency, availability) with calculations from the design and added fuel, divertor-heat and vacuum flow calculations. The baseline LCOE fell from 322.32 to 224.61 $/MWh, and the new divertor heat check fails at the design point. A fresh grader later found 17 of 23 rubric cells at target.

Source text: work/orchestration/goals/plant-closure/trail.md (T-004, T-005, T-006 returns; Round 5 result; Owner packet acceptance 2026-09-12); work/analysis/20260912-plant-closure-consolidated-grade.md

#### 11. Fix the defects found by the fusion model audit

Counts: 77 / 18 / 14.

The goal repaired defects from a 20-finding model audit. Heating now uses operating demand separately from installed capacity, the plant owns one major radius, finance formulas handle zero and equal rates, and magnet, cryogenic, winding and primary-loop inputs are range-checked. Six findings have bounded corrections, nine are partial and five remain open, so the goal is unanswered.

Source text: work/orchestration/goals/fusion-audit-remediation/trail.md (Round 4, 5, 7-11 results; T-051 return and Round 12 result, 2026-09-13); work/orchestration/mfe-financial-rate-limits.md

#### 12. Restructure the model into nested physical parts without changing its numbers

Counts: 77 / 18 / 23.

The goal reorganized the stellarator model into nested physical parts with declared ports and connections, leaving every calculation definition untouched. At the baseline all 158 output channels and 18 verdicts matched the previous package, and LCOE stayed at 224.27. A wider two-package comparison matched on all 769 points reached before the owner stopped it.

Source text: work/orchestration/goals/structural-decomposition/trail.md (Amendment 2026-09-13 after T-004, lines 108-118)

#### 13. Price the winding pack and conductor so magnet results can move off the reference design

Counts: 80 / 18 / 23.

The goal split winding-pack cost into explicit material inventory, tape procurement and winding operations, then added a priced conductor field-capability setting. A 108-case study found magnet sizing, limits and component costs respond consistently, but the evidence does not qualify an engineering design range. The reference LCOE became 142.507 $/MWh, a replacement estimate, not demonstrated savings.

Source text: work/orchestration/goals/magnet-design-transfer/transfer-claim.md; work/orchestration/goals/magnet-design-transfer/trail.md (Round 2 result; Goal close 2026-09-14)

#### 14. Make winding length, cooling load and support structure follow the coil the model builds

Counts: 86 / 18 / 23.

The goal made winding length follow the coil bore, added lead, radiation and support heat loads to refrigeration at two temperature stages, and priced a total support-mass fit. Design-point LCOE rose from 142.51 to 146.31 $/MWh and refrigeration power from 0.864 to 2.138 MW. The cheapest sampled feasible machine stayed at R = 12.7 m, a = 1.7 m.

Source text: work/orchestration/goals/magnet-coil-realism/answer.md

#### 15. Price conductor tape by its physical length

Counts: 86 / 18 / 23.

Tape procurement now prices the same composite-tape length the model builds, and the field-envelope multiplier is applied once. At the reference point tape cost falls from $804.00 million to $731.57 million, and LCOE from $146.31 to $144.74/MWh. Only three of 64 study cases satisfy all eighteen constraints, and all three use an extrapolated 30 T envelope.

Source text: work/orchestration/goals/tape-procurement-consistency/answer.md

#### 16. Check that the winding pack fits inside its casing

Counts: 87 / 19 / 23.

The model gained a fit check that compares the winding pack plus insulation and clearance against an independently set casing interior. The reference fails: it needs 370 mm radially and has 250 mm. Across 116 study cases, passes drop from 45 to twelve, and all three earlier nominal-geometry passes are rejected.

Source text: work/orchestration/goals/winding-pack-casing-fit/answer.md

#### 17. Estimate conductor critical current and operating margin

Counts: 88 / 20 / 23.

The model now estimates the reference conductor's critical current from its tape inventory and checks operating current against an allowed fraction of 0.80. The reference fails: 29.65 kA critical current against 50.00 kA operating current, a margin of −26.28 kA. In the 295-case study, all thirteen combined passes depend on an assumed orientation factor of 3.

Source text: work/orchestration/goals/absolute-conductor-current-margin/answer.md

#### 18. Account for what the magnet manufacturing charges cover

Counts: 89 / 20 / 23.

The goal mapped what each magnet procurement and manufacturing charge covers and found no demonstrated duplicate charge. It added a conditional inter-pancake insulation stock cost of $421,131.97 and made the steel support rate one explicit $18/kg all-in assumption. LCOE moves from $144.738301 to $144.747431/MWh, and the remaining process costs stay unpriced and visible.

Source text: work/orchestration/goals/magnet-manufacturing-cost-completeness/answer.md; work/orchestration/goals/magnet-manufacturing-cost-completeness/account-ledger.md

#### 19. Size the magnet tape inventory from the required current

Counts: 90 / 20 / 23.

The model gained an optional mode that sizes tape inventory from the actual field and the allowed operating fraction; legacy mode stays the default. In 324 default cases the current check always passes and 154 also fit their casing, but none passes the other eighteen constraints. This is a bounded negative answer, not proof of global infeasibility.

Source text: work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md

#### 20. Trace divertor heat from plasma exhaust to peak load

Counts: 90 / 20 / 23.

The model now reports where plasma heating power goes: radiated, deposited on the divertor target, or uncaptured, plus the area implied by the source heat profile. The peak-load formula, the 10 MW/m² limit and every existing constraint are unchanged. The reference peak stays 10.517842 MW/m², and none of 27 study cases passes all 20 constraints.

Source text: work/orchestration/goals/divertor-peak-heat-load/answer.md

#### 21. Calculate tritium breeding from the blanket

Counts: 92 / 20 / 23.

The model now calculates the tritium breeding ratio from blanket thickness using neutron-transport results, replacing the manually assigned 1.074, and fails designs that breed too little. The current 0.80 m blanket fails: its numerical lower estimate of 1.18615 is below the 1.190 fuel requirement. The 0.825–1.00 m samples pass breeding but violate the peak-field limit.

Source text: work/orchestration/goals/computed-tritium-breeding/answer.md

#### 22. Installed cooling equipment costs

Counts: 97 / 20 / 30.

The model now sizes and separately prices helium circulators, salt pumps, piping and helium-to-salt heat exchangers, with installation, spares, coolant inventories and scheduled replacements. For the selected 18-circuit design, the old $205 million cooling allowance became an $8.2 billion equipment estimate, and electricity cost rose from $150 to $311/MWh. Independent review passed it at the target depth.

Source text: work/orchestration/goals/installed-cooling-equipment-costs/answer.md

#### 23. Buildings sized from equipment and maintenance needs

Counts: 133 / 25 / 57.

The model now derives 25 separately costed buildings and transfer links from equipment dimensions, component movement space and dated maintenance inventories, including shielded maintenance wings and remote-handling routes. At the 14-circuit reference, plant capital rose $199 million and electricity cost went from $270.8 to $273.5/MWh. Independent review passed it at the target depth.

Source text: work/orchestration/goals/layout-based-facilities/answer.md

#### 24. Fuel inventory, startup stock and processing throughput

Counts: 134 / 25 / 64.

The model now calculates tritium held in the fuel system, startup supply and processing throughput from explicit assumptions. At the reference point it holds 4.418 kg of tritium, needs 4.400 kg of initial external supply and processes 7.743 kg of tritium per operating day. Fuel-processing costs and electricity cost are unchanged. Independent review passed it at the target depth.

Source text: work/orchestration/goals/fuel-inventory-and-startup/answer.md

#### 25. Fuel-processing cost that follows throughput

Counts: 135 / 25 / 64.

Fuel-processing capital now follows the calculated running exhaust flow through a sourced scaling relationship, replacing the old allowance once. At the reference point the account fell from $120.7 million to $22.8 million, and electricity cost from $273.455 to $271.584/MWh. These are matched model results, not procurement savings. Independent review passed it at the target depth.

Source text: work/orchestration/goals/throughput-based-fuel-processing-costs/answer.md

#### 26. Cost-estimate maturity and uncertainty

Counts: 135 / 25 / 64.

The goal assessed the estimate as a provisional Class 5 conceptual estimate and mapped 23 direct cost accounts; cooling, magnets and facilities hold 73% of direct cost. It added one shared stainless fabrication-price input to the model. Across 36 source alternatives, capital spans $15.9–19.3 billion and electricity cost $245–290/MWh. This is a partial envelope, not a confidence interval.

Source text: work/orchestration/goals/cost-estimate-maturity-and-uncertainty/answer.md

#### 27. Getting the current model ready for comparison

Counts: 138 / 28 / 76.

A water-state steam cycle now connects salt heat to electricity, replacing a conversion fit that bypassed the 465°C salt supply. At the raw baseline, net electricity fell from 1,009 to 850 MW and electricity cost rose from $271.6 to $318.7/MWh. The owner adopted the independently reproduced package as r3. Four engineering failures remain visible.

Source text: work/orchestration/goals/current-model-comparison-readiness/answer.md; work/orchestration/goals/current-model-comparison-readiness/approval-packet.md

#### 28. Keeping supplied design choices through evaluation

Counts: 199 / 67 / 76.

The model now evaluates and costs supplied designs without silently selecting different hardware. Round 1 preserved supplied magnet, facility, fuel-processor and cooling choices. Round 2 made equipment prices follow the chosen purchase and added 33 capacity checks, for 67 in total. Independent review passed both rounds. The baseline still fails six engineering checks.

Source text: work/orchestration/goals/preserve-model-design-choices/answer.md

#### 29. How far the repaired model can be evaluated

Counts: 199 / 67 / 76.

Broad readiness is not established: the intended size range exceeds the current breeding-geometry and conductor support. The model now refuses invalid compressor suction conditions explicitly and gives useful conductor-domain messages. It does not expand the supported design space. File-read verification and a synthetic comparison adapter were completed within their documented limits.

Source text: work/orchestration/goals/model-evaluation-domain-readiness/answer.md
