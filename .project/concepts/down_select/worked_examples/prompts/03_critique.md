# Trace Critique — Prompt

You are reviewing a stage-gate down-selection trace produced by an earlier pass. Your job is to identify weaknesses an investor or methodology reviewer would catch — not to rewrite the trace.

## Inputs (below)

1. **Methodology** — `concept_part2.md` §Per-stage factors and §Evaluation procedure (the rubric the trace was supposed to follow).
2. **The trace** — the document under review.

## What to look for

Be specific, terse, and willing to disagree with the trace. The biggest failures of analytical traces in this format are:

- **Hedged pole commitments.** Ecosystem-relational F-factors must commit to "failure pole" or "leverage pole." Any phrase like "mixed," "depends on subline," or "leans toward X" without an explicit committed pole is a defect to flag — unless the trace genuinely justifies splitting along sublines, in which case note whether the split is principled or a dodge.
- **Dominant-coordinate hedging.** The dominant failure mode and dominant leverage should each name ONE stage and ONE factor. "X with Y as close second" is acceptable if Y is genuinely close; "either X or Y" is a dodge.
- **Slack/bottleneck assertions without numeric anchor.** Each slack/bottleneck claim should rest on a comparison the ecosystem brief or analysis actually supports. Flag claims that read confident but cite nothing.
- **Numbers that don't reconcile.** Cross-check quantitative claims against what the inputs (dossier, analysis, synthesis, explorer) actually say. Flag any number that appears to be invented or inconsistent across the trace.
- **Missing factor assessments.** Every F/E code listed in the §Evaluation procedure template must be addressed. Flag any silent omission.
- **Methodology drift.** The trace is supposed to apply the methodology vocabulary precisely. Flag uses of non-rubric terms ("scalability," "TRL gap," etc.) where the rubric has a specific code that should be used.
- **Deep-dive recommendations that don't follow from the trace.** The "what this trace surfaces" section should be a direct consequence of the dominant coordinates, not generic.

## What NOT to do

- Do not rewrite the trace. Do not propose a corrected version of any section.
- Do not editorialize about the underlying concept. Focus on the trace's internal quality.
- Do not flag style. Focus on analytical defects.

## Output format

Markdown. Two top-level sections:

```
# Critique: <concept slug>

## Defects (must-fix before publication)
- <one-sentence defect, with quote or section reference>
- ...

## Soft issues (optional polish)
- <one-sentence note>
- ...

## Overall verdict
- One sentence: is the trace publication-ready as a worked example for the methodology explainer? If not, what is the single biggest blocker?
```

If there are no defects, say so directly under "Defects" with a one-line "none — trace is sound." Do not invent issues to fill space.
