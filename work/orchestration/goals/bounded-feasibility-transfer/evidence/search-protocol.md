# Pre-execution search protocol

[AGENT] Written before evaluation, 2026-09-16. The unchanged WI-065 package is the scientific basis. Reuse source/math and native coverage from joint-magnet-sizing-feasibility, divertor-peak-heat-load and primary-loop-sizing final reviews at entering HEAD a3ea15e88ee6c48de44d5880751636e7c9615776. No new physical equation or source interpretation is proposed. The current run must still pass identity/baseline/preflight and independently verify its changed coordinates.

## Evidence reused and constraint map

| Evidence | Reused meaning | Expected search response |
|---|---|---|
| Joint magnet study 02af7123 | Current sizing buys inventory; independent cavity allocation affects field, demand and fit; lower-field case fails divertor/flow | Smaller radial allocation can lower field but consume fit margin. Current reduction lowers field while affecting confinement, heating and burn/sustainment. |
| Divertor study ac1b529b | Peak scales with non-radiated heating at held source profile; separate radius-scaled peak is unqualified | Geometry/current change plasma heating; retain burn validity and the unchanged peak predicate. No free footprint improvement. |
| Primary-loop study 75772eba | Sixteen loops clear informative flow rejection; reference clears at fourteen | Integer count can lower per-loop flow and pump work, with unpriced installed equipment. No credible cost optimum. |
| Manufacturing/conductor/fit answers | Construction/performance transfer, factory remainder and physical accommodation remain conditional | A numerical pass is a reduced-model screen, not qualified hardware or accurate cost. |

## Variables, bounds and roles

[AGENT] Main search inputs are R = 10.5–13.5 m, a = 1.10–1.55 m, coil ampere-turns = 12.0–16.2 MA-turns, radial exterior allocation = 0.58–0.70 m, transverse cavity = 0.55–0.70 m, and integer primary loops = 12–18. These engineered bounds extend the prior sampled lower-radius edge to test the lower-power direction and bracket its informative cases. They are not source-qualified applicability intervals. Reference controls retain their historical 0.30/0.40 allocation outside the main-search accommodation window.

[AGENT] Current-sizing mode = 1 and physical inventory reserve = 1.01 are fixed for main cases. Inventory, effective density and pack dimensions are predictions, never independent feasibility knobs. Hold 50 kA turn current, square pack, material/orientation/cabling/degradation/sharing factors, 20 K operating temperature, tape construction, field normalization, 24.9 T ceiling, operating allowance, wall/clearance, transport profiles, density/temperature profiles, radiation = 0.90, source divertor profile, reference anchors, source coolant properties and all acceptance limits at inherited values. Legacy reference is a separately identified reproduction control. No alternative operating/transport scenario is planned.

[AGENT] Allocation and loop-count choices are explicit conditional engineering configurations. Stage 1 fixes 0.60/0.60 m and sixteen loops to expose geometry/current conflicts; alternatives are tested only in refinement. Transverse accommodation lacks full mass/thermal/structural cost response, and added loops lack installed pricing. These inputs can test physical screens, never a credible economic optimum.

## Execution budget and staged selection

[AGENT] First run the exact pinned native baseline and all preflight gates. Initial oracle stage: 64 reproducible Latin-hypercube geometry/current points across the above window plus prior reference/current-sized/allocated/field-only/divertor-only controls. Each point evaluates all twenty predicates and retains every failure/refusal. Do not filter negative auxiliary-heating points into a physical success; report account validity as well as authored predicates. The initial stage is space-filling context, not a boundary claim.

[AGENT] After inspecting failures and normalized constraint deficits, declare the next exact finite prepared candidate list before evaluating it. Refine around cases with the smallest worst normalized deficit or a combined pass. At most 500 distinct oracle coordinates total, at most 80 unique native cases including baseline. Stop on budget exhaustion, a named unsupported dependency or adequate local pass/rejection sampling. Bounds cannot grow silently. If a pass exists, spend the remaining budget on small two-sided perturbations of each continuous design variable, integer loop neighbors and at least several combined perturbations. These establish only a sampled neighborhood; neither corner samples nor continuity imply the whole box passes.

[AGENT] Select native cases for informative failures, all transfer controls and a feasible anchor/neighborhood if found. Use stock PreparedListStrategy, retain all 242 numeric outputs and twenty qualified predicate verdicts, compare all 226 independently mapped scalars at relative/absolute 1e-9 and exact rederived predicates. The sixteen unmapped scalars and inherited static L2/L6/read-set limitations remain disclosed. Native baseline runtime will set the practical refinement cost; re-exporting evidence never justifies rerunning points.

## Transfer checks and economics

[AGENT] Use matched smaller/reference/larger geometry points with explicit current/allocation choices from the same sample. Add one-input contrasts where needed to distinguish geometric change from current change; retain all violations. Verify radius/current/field/inventory, heating/divertor, flow/pump/power, and cost/calendar dependencies using the current independent oracle and unchanged source/mathematical reviews. Report held proxies and unsupported substitutions explicitly.

[AGENT] Report modeled costs conditionally. Reuse the independently reviewed primary-loop annualized break-even formula only on matched loop-count pairs: (LCOE_base − LCOE_N) × annual net MWh_N. This is an annual budget for omitted incremental costs, not an installed quote or net saving. Equipment counts remain conditional 2N circulators/N IHXs and required duty, not hardware ratings. No search ranking by LCOE is authorized.
