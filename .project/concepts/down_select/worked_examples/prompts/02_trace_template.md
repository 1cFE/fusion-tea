# Per-Concept Stage-Gate Trace — Prompt Template

You are applying a stage-gate down-selection methodology to a single fusion concept and producing an analytical trace. This is the calibration case for the methodology — your output will be read closely and used as the worked example in an explainer document. Quality bar: an investor sophisticated about fusion should find the trace discriminating and non-obvious.

## What you are producing

A markdown document filling out the trace template below for the target concept. The template comes verbatim from the methodology doc (`concept_part2.md` §Evaluation procedure). Every section must be populated — do not omit factors. If a factor is genuinely not assessable from the inputs, state that explicitly with `[insufficient data: <what would be needed>]` rather than hand-waving.

## Inputs (provided below as separate sections)

1. **Methodology**: the §Per-stage factors and §Evaluation procedure sections from `concept_part2.md`. This is your rubric. The F-factor codes (F2.a, F2.b, etc.), E-factor codes (E2.a, E3.a, etc.), pole concepts (failure / leverage), and slack/bottleneck qualifiers are the controlled vocabulary. Use them exactly as defined.
2. **Ecosystem markets brief** — facts about adjacent-industry markets for critical components. Use this to score the leverage pole of ecosystem-relational F-factors and the distinct E-factors. Cite inline when you draw on it.
3. **Target concept inputs** — the concept's dossier, prior analysis, prior synthesis, and explorer JSON (cost decomposition + sensitivities).

## How to think

- The methodology distinguishes **intrinsic F-factors** (no positive pole — only "less broken"), **ecosystem-relational F-factors** (sign-neutral, two poles, slack/bottleneck qualifier where applicable), and **distinct E-factors** (independent leverage mechanisms, no failure counterpart). Be precise about which kind each factor is — the framing changes the assessment.
- For ecosystem-relational F-factors, **explicitly name the pole** (failure or leverage) the concept lands on, and the slack/bottleneck status if it applies. Don't just summarize the situation — commit.
- The two **dominant-coordinate** outputs (dominant failure mode, dominant leverage) are the most important parts of the trace. They feed the spanning algorithm. They should pick the single biggest factor across all four stages, not summarize each stage.
- Distinguish what the inputs say from what you're inferring. The dossier and synthesis are high-quality but they don't directly address ecosystem-relational factors — that's where the ecosystem brief and judgment come in.

## Output format (fill verbatim, in order)

```
# Trace: <concept slug>

## Stage 1 (time-to-Stage-2 discount)
- Current TRL / Q achieved:
- Estimated capital and time to Stage-2 entry:
- Paradigm co-development depth:
- Open scientific heritage:
- Workforce depth:
- Discount applied (low / moderate / heavy) with one-sentence rationale:

## Stage 2 (FOAK affordability)
- F2.a (minimum-viable-plant capital cost):
- F2.b (build-time risk):
- F2.c (regulatory framework state) — pole + rationale:
- F2.d (critical component supply maturity) — pole + slack/bottleneck + rationale:
- E2.a (crossover platform attracts non-fusion investment):
- E2.b (intra-fusion early-mover supply-chain effect):
- Plausible FOAK buyer (per market-wedge taxonomy):
- **Dominant failure factor at Stage 2**: <code> — one-sentence rationale
- **Dominant leverage factor at Stage 2**: <code> — one-sentence rationale

## Stage 3 (chasm crossing)
- F3.b (site-specialization fraction):
- F3.c (replication unit size for one buyer):
- F3.a (supply-chain maturity at chasm scale) — pole + slack/bottleneck + rationale:
- F3.d (regulatory amortization path) — pole + rationale:
- E3.a (intra-fusion fleet co-development):
- E3.b (shared sub-problem solution leverage):
- Most plausible chasm-crossing path:
- **Dominant failure factor at Stage 3**: <code> — rationale
- **Dominant leverage factor at Stage 3**: <code> — rationale

## Stage 4 (learning-curve descent)
- F4.b (volume-driven vs. R&D-driven learning mechanism):
- F4.d (modularization-vs-scale crossover):
- F4.a (cost-reduction knobs and non-fusion ride-along) — pole + rationale:
- F4.c (specialty-input external-market position) — pole + rationale:
- E4.a (crossover platform revenue funds R&D):
- E4.b (talent inflow from adjacent industries):
- Plausible learning-curve mechanism (volume / R&D / mixed):
- **Dominant failure factor at Stage 4**: <code> — rationale
- **Dominant leverage factor at Stage 4**: <code> — rationale

## Cross-stage carriers
- Tritium / Li-6 / Be supply — where it bites hardest:
- First-wall / divertor / blanket lifetime — where it bites hardest:
- HTS conductor cost trajectory — where it bites hardest:
- Fuel-ecosystem R&D position:
- Workforce / intellectual depth carrier:

## Dominant failure mode (single biggest gate across all stages)
- Stage and F-factor (at failure pole):
- One-sentence rationale:

## Dominant leverage (single biggest tailwind across all stages)
- Stage and factor (ecosystem-relational F-factor at leverage pole OR distinct E-factor):
- One-sentence rationale:
- Slack vs. bottleneck status if applicable:

## What this trace surfaces for the deep-dive
- Output format implication (SysML model vs. 1costingfe extension) per concept_part2 §"What this means for the deep-dive":
- The 2–3 highest-value questions a deep-dive should answer for this concept:
```

## Quality bar

- Every F/E code populated or marked `[insufficient data]`.
- Both dominant coordinates committed at the bottom — no hedging like "either X or Y."
- Ecosystem-relational factors **explicitly state the pole** (the word "failure pole" or "leverage pole" appears).
- Citations to dossier/synthesis/ecosystem-brief inline where claims are non-obvious.
- No invented quantitative numbers. If the inputs don't supply a number, name the qualitative state.
