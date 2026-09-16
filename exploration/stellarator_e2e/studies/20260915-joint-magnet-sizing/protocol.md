# Joint magnet sizing protocol

[OWNER-VERBATIM] "Determine the conductor inventory and geometric accommodation required by the current-capacity requirement, propagate their consequences through the existing model, and establish whether a bounded feasible region exists. A well-supported finding that no feasible design exists within the investigated assumptions is a successful answer."

[OWNER-VERBATIM] "Do not relax allowable operating fraction, field limits, fit clearances or other acceptance criteria to create a pass. Do not tune material normalization or orientation gains to recover the reference design."

[AGENT] Current-sizing mode1, fixed50kA turn current, square pack and inherited composition, 6mm by56µm tapes at20K. Default material/orientation/retention factors1. Allowable fraction0.8 and selected field ceiling24.9T remain fixed. Inventory multiplier1.01 is explicitly1% additional physical inventory over minimum; mode1/multiplier1 diagnostics record signed boundary residuals without altering exact predicates. All20 predicates evaluated separately; report current, fit, other18 and all20.

## Bounded staged scope

[AGENT] First reproduce entering reference and representative prior nominal/allocated/assumed-orientation passes as historical controls, with their own fixed selected envelopes. Main study never adopts30T to recover feasibility. Match each change against entering mode0 at identical coordinates, using frozen entering oracle and reference native evidence.

[AGENT] Then solve current demand natively at reference and off-design points. Allocation is independent and field precedes sizing; this model has no iterative cycle. Verify native/oracle scalar relative tolerance1e-9, absolute1e-9 in named units; report fractional current/count/area closure residuals. Keep exact-boundary native predicate signs separately from physical closure. Refused/domain-invalid proposals remain in scan diagnostics with reason and coordinates; no nonconverged design is omitted. No iteration/convergence claim is needed for the acyclic solve.

[AGENT] Engineered initial scan: R12.7–15.0m, a1.3–1.9m, ampere-turns15.4–18MA, radial allocation0.30–0.75m and transverse cavity0.40–0.75m. These extend historical geometry/current sensitivities modestly and span the analytically estimated~0.58m radial/~0.55m transverse demand; they are applicability assumptions, not sourced available space. Existing guards require20–32T actual field and valid radial build. Independently chosen allocation pairs are principal configurations; local radial/transverse variations separately test fit. Bounds may be tightened after retained oracle scan; a small expansion requires recorded engineering rationale and native domain compliance. At most400 native cases; no outer evaluator solve or adaptive execution.

[AGENT] Performance sensitivities after default results: sample-derived material factors1.10/1.35 (construction transfer, not qualified product), orientation factor2 only as a separately labeled hypothetical scenario, and0.9 retention per mechanism. No multiplier is inferred from the gain needed to pass. Required gains are analytical thresholds, never achieved capability. Fixed geometry/allocated space permits comparison of inventory and priced cost changes; no performance premium is modeled. A small separately labeled shape sensitivity is allowed only as local fit diagnostics, not an economically comparable redesigned magnet.

## Interpretation limits

[INHERITED] Pack self-field/shape correction, detailed wall/support sizing, actual transverse casing thermal/mass response, bridge redesign, coil-to-coil clearance and field-angle map are absent. Required space is not proof of available space. Scalar current sizing establishes internal consistency under shared performance assumptions; native predicate pass does not independently qualify the conductor. Price-year and unpriced manufacturing limitations remain as in WI-063. No global infeasibility or optimum follows from finite sampling; a broader search may change sampled feasibility/cost and cannot remove these missing physics.

## Exact-boundary numerical diagnostic

[AGENT] Reference multiplier1 native margin is−3.33e−16 while the independent algebra gives0; their exact Boolean current verdicts differ. Both are retained in results/exact-boundary-diagnostic.json, including every native output/response and oracle channel. This separate native implementation diagnostic is outside the prepared-list scientific cohort and cheapest-feasible comparison. The fixed1.01 physical multiplier is used for that cohort as declared before scanning; no predicate tolerance or sign is changed. The reference remains physically rejected by fit/divertor in either calculation.
