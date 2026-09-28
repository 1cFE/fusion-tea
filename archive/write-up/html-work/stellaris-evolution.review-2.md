# Review — stellaris-evolution.html

page: /home/reid/1cfe/fusion-tea/docs/write-up/stellaris-evolution.html
source: /home/reid/1cfe/fusion-tea/docs/write-up/stellaris-evolution.md
reviewed against: docs/write-up/html-render-prompt.md; docs/write-up/writing-prompt.md; /home/reid/.claude/skills/_my_mental_model_v2/feedback/html.md; /home/reid/.claude/skills/_my_mental_model_v2/feedback/synthesis.md

## Findings

1. The page carries three local style blocks covering toolbar colors, panel typography, disclosure styling, buttons, code blocks and evidence-table behavior (lines 6–152). These extend well beyond a small diagram-layout block. The support-specific exception exempts viewer scripts, but does not exempt these styles. (Cites: writer prompt, “Style”: “A page may add a small style block for the layout of its own diagrams. Everything else comes from write-up.css.”)

2. The added legend says “A closed part wears the halo of the calcs it hides.” (line 7037). This uses personification to explain the visual encoding, while the actual rule is that a collapsed part receives the strongest change color among its contained calculations (lines 6980–6997). (Cites: writing-prompt.md, “Write as the team doing the work”: avoid metaphors doing the explaining; synthesis feedback, “Abstraction performing a verb”.)

## Mechanical fidelity comparison

Compared all 37 source blocks in sequence against parsed article blocks: 37 matched after whitespace normalization and the permitted repository-link conversion. No dropped, reordered or reworded source blocks were found. All seven source heading IDs use the expected GitHub form. Source support links become .html; the main-post link remains .md. Repository references become quiet code.path text. The frame numbers and the Part 3 reference become links. The markdown contains no tables, figures or code blocks.

The comparison reads the HTML source rather than a browser rendering. Viewer scripts are exempt from the script restriction. Evidence facts were not checked against unnamed repository files.

## Added text inventory

### Rail and page metadata

- Browser title: “Stellarator model evolution”.
- Rail eyebrow: “1cFE write-up · Part 4”; rail title: “Modeling Stellaris”; added destinations “Model evolution viewer” and “Frame records”, each marked “↗”. The six theme entries repeat the source headings.

### Viewer, before section 1

- We started with a model that could price the Stellaris design but mostly just repeated the paper's numbers back to us. Over about a month, we ran 28 goals against it to turn the model into something that actually computes the plant from its design: from 55 calculations, 6 checks and 14 parts to 199, 67 and 76. Looking back over those goals, they generally fall within six themes.
- Model evolution viewer
- Step through the goals with the slider or arrows. Select a part to open it, then select a calculation to see its inputs and equations. Frame links in the themes return here. Expand gives the graph the whole window.
- The interactive graph needs JavaScript. All six themes and the frame records below remain available.

- Static controls: “Snapshot”, “Expand all”, “Collapse all”, “Fit”, “Reset layout”, “Spacing”, “1×”, “Find”.
- Runtime controls and labels: “◀”, “▶”, “Frame”, “Jump to goal”, “Open changed parts”, “Expand” / “Collapse”, “Full screen” / “Exit full screen”, “loading…”, and the frame position.
- Legend: “new calc”, “changed calc”, “moved calc”, “A closed part wears the halo of the calcs it hides.”
- Metrics: “Calcs”, “Checks (constraints)”, “Parts”, “Attributes”, “Calc-to-calc links”, “Model source files”; values and changes come from the selected snapshot.
- Frame headings: “Question”, its provenance grade, “Where the goals started” or “Result”, “(condensed by an agent from the source below)”.
- Change headings: “Changes”, “New calcs”, “Changed calcs”, “Python body changed, model record unchanged”, “Moved calcs”, “Removed calcs”, “New checks”, “Changed checks”, “Removed checks”, “New parts”, “Removed parts”, “Documentation changed only”, “Recorded values changed”, “Attributes”.
- Empty states: “This is the starting model. Step forward to see what each goal changed.”; “The snapshot changed only in text the viewer does not compare (for example source citations).”
- Calculation inspection adds snapshot-dependent identifiers, inputs, equations, source code and diffs. These are reference payloads rather than additions to the six themes; they are not reproduced wholesale here.

### Sections 1–6

No new explanatory prose. Each repository-link label gains a colon and its repository path, as permitted. Frame numbers become interactive links. “Part 3” becomes a link.

### Frame records, after section 6

- In the recordFrame records
- Counts come from each committed snapshot. Results below are the viewer’s agent condensations of the cited records; they have not been owner-reviewed. The six themes above use the checked write-up text.
- Table headings: “Frame”; “Calculations / checks / parts”; “Recorded result and source”.

#### 1. Starting point: the migrated model

55 / 6 / 14

The model as the first goals found it: 55 calcs and 6 checks, every calc scoped to the plant root. It follows the migration to the current snapshot format and work item WI-030, which added a computed volume-averaged beta and a conductor peak-field limit. The first two goals, cryo-volume-basis and p-pump-basis, examined this version. p-pump-basis found the 1 MW pumping power indefensible and routed the fix to WI-033; the regenerated model first appears in the next frame.commits 89f78130 and ba5c9945; work/orchestration/goals/cryo-volume-basis/; work/orchestration/goals/p-pump-basis/; .project/completed/CHANGELOG.md (Goal Harness Item 5)

#### 2. Rerunning the model with pumping power corrected to 195 MW

55 / 6 / 14

The goal regenerated the model package so it carried the pumping power already corrected from 1 MW to 195 MW, then ran a study on it. The recirculating-power check now fails at 184 swept points instead of 32. LCOE at the baseline design rose from 275.264 to 333.067 $/MWh (+21.0%), with all six checks still passing there.work/orchestration/goals/p-pump-fence/trail.md § Round 1 result — 2026-08-29 (Last semantic outcome); § Goal close — 2026-08-29

#### 3. Deriving the magnets from their own design

60 / 7 / 14

The magnet's field, a structural limit and its cost now come from the coil design instead of cited constants. The on-axis field is computed from coil current and geometry, a winding-pack stress check pushes back on coil sizing, and magnet cost is split into separately sized accounts. Baseline LCOE fell from 333.067 to 304.482 $/MWh.work/orchestration/goals/magnet-closure/trail.md § Round 1 result — 2026-08-30; § T-004 return — 2026-08-30; § Goal close — 2026-09-01

#### 4. Checking the plasma operating point against the machine

61 / 8 / 14

The plasma operating point is now checked against the machine instead of typed in. A confinement relation (ISS04) links field and heating to density and temperature, and a new sustained-heating check pushes back. The study found no feasible point at the printed 50 MW of installed heating; feasibility returns at about 91 MW.work/orchestration/goals/operating-point-closure/trail.md § Goal close — 2026-09-02; § Round 2 result — 2026-09-01 (L-005)

#### 5. Making the escape levers carry real costs

65 / 9 / 14

The winding pack is now sized from coil current, the cold volume is computed, and a conductor strain check was added; the design point did not move. The study still found no feasible point at the printed 50 MW. There the neutron wall load alone blocks 27 of 240 points, the conductor limit 6. The goal closed by redirect.work/orchestration/goals/priced-levers/trail.md § Round 1 result — 2026-09-03; § Goal close — 2026-09-03; work/orchestration/goals/priced-levers/goal.md § Amendment 2026-09-03

#### 6. Making the wall-load and heating checks honest

68 / 9 / 14

Heating became a real chain from wall-plug power to plasma-coupled power, and the wall-load check now compares a computed peak with the paper's printed peak. The machine as designed then slightly fails the wall limit (4.088 against 4.05) and baseline LCOE rose from 307.087 to 313.513 $/MWh. A working point at the printed heating needs a fatter plasma.work/orchestration/goals/wall-and-heating/trail.md § Goal close — 2026-09-05; § Round 2 result — 2026-09-04; commit cb355321 message (LCOE figures)

#### 7. Why the stored energy ran 9% high

68 / 9 / 14

The model's stored energy sat 9% above the paper's printed value because the helium ash was given the fuel's flat profile; the printed value is not a target. Computing the ash profile from the paper's own rule dropped the required heating from 90.6 to 49.1 MW against a 50 MW limit. Both failing baseline checks now pass, with nothing tuned.work/orchestration/goals/stored-energy-basis/trail.md § Goal close — 2026-09-06; § T-001 return — 2026-09-05 (round 2)

#### 8. Ruling out plasmas the heating cannot hold

68 / 10 / 14

The sustainment check became two-sided: the heating a point needs must be zero or positive, and no more than what is installed. No number changed; at all 7,712 re-run points the new check failed exactly the ignited ones. The cheapest feasible machine stayed at 202 $/MWh, and the machine as designed needs 49 of its 50 MW.work/orchestration/goals/burn-control/trail.md § Goal close — 2026-09-07

#### 9. Making a fatter plasma cost something

70 / 10 / 14

The magnet chain now computes conductor peak field, stored magnetic energy and casing mass from the coil bore, anchored so the design point reproduces exactly. A fatter plasma is caught by the conductor limit only where the bore is large relative to the major radius. The cheapest machine is unchanged at 202 $/MWh, because there the bore is nearly free.work/orchestration/goals/minor-radius/trail.md § Goal close — 2026-09-08

#### 10. Compute the plant's pumping power, cycle efficiency and availability from the design

76 / 14 / 14

The goal replaced three fixed plant multipliers (pumping power, cycle efficiency, availability) with calculations from the design and added fuel, divertor-heat and vacuum flow calculations. The baseline LCOE fell from 322.32 to 224.61 $/MWh, and the new divertor heat check fails at the design point. A fresh grader later found 17 of 23 rubric cells at target.work/orchestration/goals/plant-closure/trail.md (T-004, T-005, T-006 returns; Round 5 result; Owner packet acceptance 2026-09-12); work/analysis/20260912-plant-closure-consolidated-grade.md

#### 11. Fix the defects found by the fusion model audit

77 / 18 / 14

The goal repaired defects from a 20-finding model audit. Heating now uses operating demand separately from installed capacity, the plant owns one major radius, finance formulas handle zero and equal rates, and magnet, cryogenic, winding and primary-loop inputs are range-checked. Six findings have bounded corrections, nine are partial and five remain open, so the goal is unanswered.work/orchestration/goals/fusion-audit-remediation/trail.md (Round 4, 5, 7-11 results; T-051 return and Round 12 result, 2026-09-13); work/orchestration/mfe-financial-rate-limits.md

#### 12. Restructure the model into nested physical parts without changing its numbers

77 / 18 / 23

The goal reorganized the stellarator model into nested physical parts with declared ports and connections, leaving every calculation definition untouched. At the baseline all 158 output channels and 18 verdicts matched the previous package, and LCOE stayed at 224.27. A wider two-package comparison matched on all 769 points reached before the owner stopped it.work/orchestration/goals/structural-decomposition/trail.md (Amendment 2026-09-13 after T-004, lines 108-118)

#### 13. Price the winding pack and conductor so magnet results can move off the reference design

80 / 18 / 23

The goal split winding-pack cost into explicit material inventory, tape procurement and winding operations, then added a priced conductor field-capability setting. A 108-case study found magnet sizing, limits and component costs respond consistently, but the evidence does not qualify an engineering design range. The reference LCOE became 142.507 $/MWh, a replacement estimate, not demonstrated savings.work/orchestration/goals/magnet-design-transfer/transfer-claim.md; work/orchestration/goals/magnet-design-transfer/trail.md (Round 2 result; Goal close 2026-09-14)

#### 14. Make winding length, cooling load and support structure follow the coil the model builds

86 / 18 / 23

The goal made winding length follow the coil bore, added lead, radiation and support heat loads to refrigeration at two temperature stages, and priced a total support-mass fit. Design-point LCOE rose from 142.51 to 146.31 $/MWh and refrigeration power from 0.864 to 2.138 MW. The cheapest sampled feasible machine stayed at R = 12.7 m, a = 1.7 m.work/orchestration/goals/magnet-coil-realism/answer.md

#### 15. Price conductor tape by its physical length

86 / 18 / 23

Tape procurement now prices the same composite-tape length the model builds, and the field-envelope multiplier is applied once. At the reference point tape cost falls from $804.00 million to $731.57 million, and LCOE from $146.31 to $144.74/MWh. Only three of 64 study cases satisfy all eighteen constraints, and all three use an extrapolated 30 T envelope.work/orchestration/goals/tape-procurement-consistency/answer.md

#### 16. Check that the winding pack fits inside its casing

87 / 19 / 23

The model gained a fit check that compares the winding pack plus insulation and clearance against an independently set casing interior. The reference fails: it needs 370 mm radially and has 250 mm. Across 116 study cases, passes drop from 45 to twelve, and all three earlier nominal-geometry passes are rejected.work/orchestration/goals/winding-pack-casing-fit/answer.md

#### 17. Estimate conductor critical current and operating margin

88 / 20 / 23

The model now estimates the reference conductor's critical current from its tape inventory and checks operating current against an allowed fraction of 0.80. The reference fails: 29.65 kA critical current against 50.00 kA operating current, a margin of −26.28 kA. In the 295-case study, all thirteen combined passes depend on an assumed orientation factor of 3.work/orchestration/goals/absolute-conductor-current-margin/answer.md

#### 18. Account for what the magnet manufacturing charges cover

89 / 20 / 23

The goal mapped what each magnet procurement and manufacturing charge covers and found no demonstrated duplicate charge. It added a conditional inter-pancake insulation stock cost of $421,131.97 and made the steel support rate one explicit $18/kg all-in assumption. LCOE moves from $144.738301 to $144.747431/MWh, and the remaining process costs stay unpriced and visible.work/orchestration/goals/magnet-manufacturing-cost-completeness/answer.md; work/orchestration/goals/magnet-manufacturing-cost-completeness/account-ledger.md

#### 19. Size the magnet tape inventory from the required current

90 / 20 / 23

The model gained an optional mode that sizes tape inventory from the actual field and the allowed operating fraction; legacy mode stays the default. In 324 default cases the current check always passes and 154 also fit their casing, but none passes the other eighteen constraints. This is a bounded negative answer, not proof of global infeasibility.work/orchestration/goals/joint-magnet-sizing-feasibility/answer.md

#### 20. Trace divertor heat from plasma exhaust to peak load

90 / 20 / 23

The model now reports where plasma heating power goes: radiated, deposited on the divertor target, or uncaptured, plus the area implied by the source heat profile. The peak-load formula, the 10 MW/m² limit and every existing constraint are unchanged. The reference peak stays 10.517842 MW/m², and none of 27 study cases passes all 20 constraints.work/orchestration/goals/divertor-peak-heat-load/answer.md

#### 21. Calculate tritium breeding from the blanket

92 / 20 / 23

The model now calculates the tritium breeding ratio from blanket thickness using neutron-transport results, replacing the manually assigned 1.074, and fails designs that breed too little. The current 0.80 m blanket fails: its numerical lower estimate of 1.18615 is below the 1.190 fuel requirement. The 0.825–1.00 m samples pass breeding but violate the peak-field limit.work/orchestration/goals/computed-tritium-breeding/answer.md

#### 22. Installed cooling equipment costs

97 / 20 / 30

The model now sizes and separately prices helium circulators, salt pumps, piping and helium-to-salt heat exchangers, with installation, spares, coolant inventories and scheduled replacements. For the selected 18-circuit design, the old $205 million cooling allowance became an $8.2 billion equipment estimate, and electricity cost rose from $150 to $311/MWh. Independent review passed it at the target depth.work/orchestration/goals/installed-cooling-equipment-costs/answer.md

#### 23. Buildings sized from equipment and maintenance needs

133 / 25 / 57

The model now derives 25 separately costed buildings and transfer links from equipment dimensions, component movement space and dated maintenance inventories, including shielded maintenance wings and remote-handling routes. At the 14-circuit reference, plant capital rose $199 million and electricity cost went from $270.8 to $273.5/MWh. Independent review passed it at the target depth.work/orchestration/goals/layout-based-facilities/answer.md

#### 24. Fuel inventory, startup stock and processing throughput

134 / 25 / 64

The model now calculates tritium held in the fuel system, startup supply and processing throughput from explicit assumptions. At the reference point it holds 4.418 kg of tritium, needs 4.400 kg of initial external supply and processes 7.743 kg of tritium per operating day. Fuel-processing costs and electricity cost are unchanged. Independent review passed it at the target depth.work/orchestration/goals/fuel-inventory-and-startup/answer.md

#### 25. Fuel-processing cost that follows throughput

135 / 25 / 64

Fuel-processing capital now follows the calculated running exhaust flow through a sourced scaling relationship, replacing the old allowance once. At the reference point the account fell from $120.7 million to $22.8 million, and electricity cost from $273.455 to $271.584/MWh. These are matched model results, not procurement savings. Independent review passed it at the target depth.work/orchestration/goals/throughput-based-fuel-processing-costs/answer.md

#### 26. Cost-estimate maturity and uncertainty

135 / 25 / 64

The goal assessed the estimate as a provisional Class 5 conceptual estimate and mapped 23 direct cost accounts; cooling, magnets and facilities hold 73% of direct cost. It added one shared stainless fabrication-price input to the model. Across 36 source alternatives, capital spans $15.9–19.3 billion and electricity cost $245–290/MWh. This is a partial envelope, not a confidence interval.work/orchestration/goals/cost-estimate-maturity-and-uncertainty/answer.md

#### 27. Getting the current model ready for comparison

138 / 28 / 76

A water-state steam cycle now connects salt heat to electricity, replacing a conversion fit that bypassed the 465°C salt supply. At the raw baseline, net electricity fell from 1,009 to 850 MW and electricity cost rose from $271.6 to $318.7/MWh. The owner adopted the independently reproduced package as r3. Four engineering failures remain visible.work/orchestration/goals/current-model-comparison-readiness/answer.md; work/orchestration/goals/current-model-comparison-readiness/approval-packet.md

#### 28. Keeping supplied design choices through evaluation

199 / 67 / 76

The model now evaluates and costs supplied designs without silently selecting different hardware. Round 1 preserved supplied magnet, facility, fuel-processor and cooling choices. Round 2 made equipment prices follow the chosen purchase and added 33 capacity checks, for 67 in total. Independent review passed both rounds. The baseline still fails six engineering checks.work/orchestration/goals/preserve-model-design-choices/answer.md

#### 29. How far the repaired model can be evaluated

199 / 67 / 76

Broad readiness is not established: the intended size range exceeds the current breeding-geometry and conductor support. The model now refuses invalid compressor suction conditions explicitly and gives useful conductor-domain messages. It does not expand the supported design space. File-read verification and a synthetic comparison adapter were completed within their documented limits.work/orchestration/goals/model-evaluation-domain-readiness/answer.md

### Additional interactive frame questions

The interactive viewer repeats the frame titles and results listed above. It additionally exposes the following question text and source pointers from its embedded data.

- Frame 2: With `p_pump` re-based to 195 MW, where does the `recirc_ok` fence move, and what happens to LCOE? Source: work/orchestration/goals/p-pump-fence/goal.md § Question
- Frame 3: Can the magnet system's field, feasibility, and cost be derived from its own engineering design — coil geometry and current giving the peak field, a stress or current-density limit that pushes back on coil sizing, and magnet cost split into separately sized winding-pack / structure / cryoplant accounts — instead of cited constants? Source: work/orchestration/goals/magnet-closure/goal.md § Question
- Frame 4: Can the plasma operating point be solved from the machine — a confinement or transport relation linking field and heating power to density and temperature, with a beta, density, or power limit pushing back on the choice — instead of prescribed as typed-in density, temperature, and profile inputs? Source: work/orchestration/goals/operating-point-closure/goal.md § Question
- Frame 5: Can the two levers the machine would use to escape the deadlock — conductor grade and heating power — be made to carry their real consequences, so the model charges honestly for using them? Source: work/orchestration/goals/priced-levers/goal.md § Question
- Frame 6: Can the two fences that actually bound the machine at the printed 50 MW of installed heating — neutron wall load and sustained heating — be made honest, so that the wall-load check measures what it claims to measure, the heating system carries real structure, and the model charges truthfully for escaping from between them? Source: work/orchestration/goals/wall-and-heating/goal.md § Question
- Frame 7: Does the pinned baseline's `sustainment_ok` violation, and the committed "no feasible driven point at the printed 100 MW wall-plug on the design geometry" result, survive when the model's stored thermal energy is set to the paper's printed 504.65 MJ? If not, what in the profile integral produces the +9.2 % — and is the printed value the right target? Source: work/orchestration/goals/stored-energy-basis/goal.md § Question
- Frame 8: Can the sustainment check become the operating-point condition the sister systems codes use — the power balance closes with an auxiliary heating that is zero or positive and no larger than what is installed — so that a point whose alpha heating exceeds its losses is declared no operating point of this model, and once it is, what do the feasibility counts, the cheapest machine, and the reading of the machine as designed become? Source: work/orchestration/goals/burn-control/goal.md § Question
- Frame 9: Once the magnet chain computes the conductor peak field, the stored magnetic energy and the coil casing mass from coil geometry — the sourced shapes, anchored at the design point — does the minor radius stop being a free ride, and where do the feasible region and the cheapest feasible machine sit, at what aspect ratio, once it does? Source: work/orchestration/goals/minor-radius/goal.md § Question
- Frame 10: Once the primary coolant loop, the power cycle and the maintenance calendar are computed from the design instead of held, and the fuel, exhaust and vacuum flows are carried as reduced calculations with every missing input surfaced, does the machine as designed still close and where does the cheapest feasible machine move — and which of the twelve rubric cells still below target can a fresh grader move to target or to a written disposition at one pin? Source: work/orchestration/goals/plant-closure/goal.md § Question
- Frame 11: Can the current IFE and MFE models resolve all 20 audit findings with independently checked corrections, while making every remaining source, engineering, and comparison limitation explicit and enforceable within each model's supported use? Source: work/orchestration/goals/fusion-audit-remediation/goal.md § Question
- Frame 12: Can the Stellaris model be restructured so its SysML reads as the machine it represents — subsystems decomposed into the physical parts the source describes, the energy topology declared as ports and connections, every attribute living on the part it belongs to — such that the generated package computes the same LCOE and the same verdicts, the model renders as a hierarchy rather than a flat list, and a subsystem definition can be swapped for a trade study without editing the calcs? Source: work/orchestration/goals/structural-decomposition/goal.md § Question
- Frame 13: Within a documented geometry and conductor-technology range, do magnet sizing, operating limits, and component costs respond consistently enough to support a defensible design-point transfer? Source: work/orchestration/goals/magnet-design-transfer/goal.md § Question
- Frame 14: Does the magnet's winding length, cold load and structure follow the coil the model builds — the bore the radial build sets, the leads and shield a 20 K coil set needs, the whole support structure the source's mass shape describes — and once they do, does the machine the model favours change: what does a fatter plasma now cost at the magnet, where does the cheapest feasible machine sit, and how much of the plant's recirculating power is the cryoplant? Source: work/orchestration/goals/magnet-coil-realism/goal.md § Question
- Frame 15: How can conductor procurement cost follow one traceable physical tape inventory consistently when geometry, current, reference winding-pack current density or selected conductor envelope changes? Source: work/orchestration/goals/tape-procurement-consistency/goal.md § Question
- Frame 16: Can an explicitly defined, independently based casing interior accommodate the calculated winding-pack envelope, insulation and assembly clearances, and how does adding that geometric screen change sampled feasibility and the cheapest feasible choice? Source: work/orchestration/goals/winding-pack-casing-fit/goal.md § Question
- Frame 17: Can an admissible explicit tape-to-cable performance basis establish estimated conductor critical current, operating fraction and allowable-fraction margin for the modeled inventory? Source: work/orchestration/goals/absolute-conductor-current-margin/goal.md § Question
- Frame 18: What do the modeled magnet procurement and manufacturing charges cover, which overlaps can be demonstrated and removed, and which missing costs can be estimated or made explicit using admissible evidence and current conductor/pack geometry? Source: work/orchestration/goals/magnet-manufacturing-cost-completeness/goal.md § Question
- Frame 19: Can a magnet carry the required current at the selected operating margin, fit inside an explicitly allocated casing, and satisfy the existing plant constraints under one consistent set of construction and performance assumptions? Source: work/orchestration/goals/joint-magnet-sizing-feasibility/goal.md § Question
- Frame 20: Can the represented stellarator divertor peak heat load be traced consistently from plasma exhaust through deposition, geometry and spatial concentration, and what does that establish at the joint magnet-sizing rejection cases? Source: work/orchestration/goals/divertor-peak-heat-load/goal.md § Question
- Frame 21: Can we calculate tritium production from the modeled blanket configuration, verify that calculation, and make insufficient breeding constrain the design? Source: work/orchestration/goals/computed-tritium-breeding/goal.md § Question
- Frame 22: Can we size and separately cost the cooling system’s pumps, piping and heat exchangers from the plant’s calculated heat-removal requirements, including installation and appropriate lifecycle costs? Source: work/orchestration/goals/installed-cooling-equipment-costs/goal.md § Question
- Frame 23: Can we derive the size and cost of plant buildings and maintenance facilities from the equipment they contain and the maintenance work they must support? Source: work/orchestration/goals/layout-based-facilities/goal.md § Question
- Frame 24: Can we calculate the tritium held throughout the fuel system, the stock needed to start operation, and the processing throughput from explicit operating and fuel-system assumptions? Source: work/orchestration/goals/fuel-inventory-and-startup/goal.md § Question
- Frame 25: Can we make the cost of the fuel-processing plant follow its calculated processing demand, using applicable cost sources and explicit equipment boundaries? Source: work/orchestration/goals/throughput-based-fuel-processing-costs/goal.md § Question
- Frame 26: Can we state how well developed the plant cost estimate is, expose the functional accounts where cost is concentrated, and quantify the uncertainty that the available evidence supports? Source: work/orchestration/goals/cost-estimate-maturity-and-uncertainty/goal.md § Question
- Frame 27: Can we prepare a reproducible comparison package using the model that meets all 23 depth targets, with a justified cooling-to-electricity calculation and no unexplained validation failures affecting the comparison? Source: work/orchestration/goals/current-model-comparison-readiness/goal.md § Question
- Frame 28: Can the stellarator model and shared dependencies evaluate and cost supplied designs without silently selecting different hardware, while preserving supported physical relationships and validity limits? Source: work/orchestration/goals/preserve-model-design-choices/goal.md § Question
- Frame 29: How far can the repaired stellarator model evaluate the intended design space, with verified file-read identity coverage and a compatible comparison adapter? Source: work/orchestration/goals/model-evaluation-domain-readiness/goal.md § Question
