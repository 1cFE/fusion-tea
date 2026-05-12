# Trace Revision — Prompt

You produced a stage-gate down-selection trace in an earlier pass. A reviewer critiqued it. Your job now is to produce a **revised trace** that addresses the critique's must-fix defects.

## Inputs (below)

1. **Methodology** — `concept_part2.md` §Per-stage factors and §Evaluation procedure.
2. **Your original trace.**
3. **Critique of that trace.**

## Rules for the revision

- Address every defect in the critique's "Defects (must-fix before publication)" section.
- **Commit poles cleanly** on every ecosystem-relational F-factor. If the underlying reality has genuinely different poles for different components (REBCO vs. Li-6, for instance), pick the pole that dominates the relevant decision (typically: weight by CAPEX share or by criticality at the relevant stage) and state the weighting choice in one short clause. Do not duck into "mixed."
- **One stage and one factor** for each dominant coordinate. If two are genuinely close, name the second only as a footnote in the rationale sentence, not in the coordinate itself.
- **Anchor every quantitative claim** to the dossier, analysis, synthesis, explorer JSON, or ecosystem brief — or remove it. No new numbers introduced.
- **Use rubric vocabulary** — volume / R&D / mixed (the three allowed choices for F4.b); failure pole / leverage pole; slack / bottleneck; the F/E codes verbatim. Avoid "leaning," "mixed-leaning-X."
- **Don't soften slack/bottleneck tags.** "Bottleneck-likely" should be "bottleneck" if the trajectory points there; otherwise "slack."
- Where the critique flags a soft issue, address it if it doesn't require new information; otherwise leave it.

## What NOT to do

- Do not re-litigate the critique. Do not include a response section. Produce the revised trace, nothing else.
- Do not add factors not in the original. Do not invent new evidence.
- Do not change the underlying analytical conclusions unless the critique demonstrates they're wrong. Pole commitments and number anchoring should change; the dominant failure and leverage *factor identities* should usually stay.
- If the critique flagged a methodology gap (e.g., F-factor used as proxy for an out-of-vocabulary concern), note it in a new final section `## Methodology friction encountered` — ONE-line note, do not propose a fix.

## Output

The complete revised trace document, same structure as the original. Begin with `# Trace: <slug>` and end with the methodology-friction note (if any). Nothing before or after.
