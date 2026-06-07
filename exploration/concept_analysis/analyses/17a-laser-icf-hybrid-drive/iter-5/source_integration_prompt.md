# Source Integration Assessment: Laser ICF Hybrid Drive (Xcimer Energy)

You are evaluating new source documents that have been added to a concept
that already has a completed analysis. Your job is to identify what material
information from the new sources should be incorporated into the existing
analysis, and produce structured feedback for the analysis agent.

## Existing Analysis
Read this file completely:
`/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/analysis.md`

## New Source Documents (use subagents)

Spawn one subagent per new source document. Ask each subagent:
- What new technical, economic, or performance data does this source contain?
- Does it contain information that contradicts or updates claims in the analysis?
- What LCOE-relevant parameters or cost data are present?
- What risk, timeline, or TRL information is relevant?

New sources:
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-01/sources/xcimer-energy-approach.md` (2 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-02/sources/hylife-energy-conversion-notes.md` (4 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-02/sources/xcimer-science-page.md` (17 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-02/sources/xec-20260224-commercialization-of-lfe-whtppr-shared-24-feb.md` (88 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/digital-ark-67531-metadc626683.md` (9 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/laserfocusworld-lasers-sources-article-14274951-can-high.md` (8 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/llnl-53961-llnl-releases-generalized-economics-model-fusion.md` (4 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/optica-opn-home-articles-volume-34-june-2023-features.md` (18 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/osti-biblio-7021072.md` (3 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/osti-servlets-purl-2561299.md` (23 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/osti-servlets-purl-6137961.md` (141 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/pmc-articles-pmc7658748.md` (44 KB)
- `/home/reid/1cfe/fusion-tea-cohort-rerun/knowledge/concept_research/17a-laser-icf-hybrid-drive/iter-03/sources/sciencedirect-science-article-pii-s0920379624001868.md` (2 KB)

## Analysis Goals (for reference)

# Analysis Goals

These are the objectives the analysis agent works toward. Every section of the
analysis should contribute to answering these questions.

**What is already fixed upstream (do NOT re-decide):** the concept's confinement
family, its 1costingFE archetype, the fixed list of comparable concepts, and the
named design point (plant name, maturity, native net-electric power `P_native`,
and grounding confidence) are all determined by the upstream tables and arrive
through the analysis frontmatter. They are inputs, not outputs. Your job is not
to choose a family, a nearest neighbour, or a plant — it is to *articulate the
delta* against the fixed comparables and to *extract and account for* the design
point you are given.

**The headline is the replicated 1 GWe fleet.** Every concept's comparable number
is LCOE for a 1 GWe NOAK plant, reached by *replicating* the real `P_native`
design point into a fleet of identical modules — never a monolithic 1000 MWe
machine. Override values and rationales share that frame: a relative override
means "`M` of the library's 1 GWe *fleet* cost for that account," and its
rationale is anchored to the library's modular-fleet default, not a "conventional
1 GWe plant." (The full semantics — the S/U/P cost classes and the single
invariant — are in the override-semantics policy embedded in the override-
discovery section of your prompt.)

1. **Family-Delta Articulation**: Given the fixed comparables, what does this
   design point do differently, and how does that difference move cost? Name the
   specific subsystem, the direction of the cost effect (advantage / penalty /
   neutral), and the magnitude where the data supports it. "It is a tokamak" is
   not a delta; "its all-REBCO TF coils replace the LTS magnets the comparable
   prices at $X/kg" is.

2. **Design-Point Parameter Extraction**: Extract the complete quantitative
   description (geometry, physics, performance) of the *named* design point at
   its *native* scale. Every LCOE-relevant parameter you record must describe
   that one plant — not a different machine, not a different power level, not a
   roadmap aspiration.

3. **TEA Implications**: For each family-delta, state the techno-economic
   consequence. Which differences create cost advantages, which create cost
   penalties, which are cost-neutral, and which are simply unknown for lack of
   data?

4. **Override-Candidate Discovery**: For each canonical 1costingFE account the
   archetype touches, decide whether the dossier names a company-grounded
   quantity, unit cost, or published dollar figure that justifies departing from
   the library default. The library carries the default story; an override is an
   *accountable, evidence-backed* departure from it — not a guess and not an
   optimism adjustment.

5. **Risks and Assumptions**: Are the key risks and assumptions called out, and
   is the analysis honest about what it does not know? How should each be carried
   into the TEA — as a sensitivity parameter, a scenario branch, or an explicit
   data gap?


## Instructions

1. Read the existing analysis completely
2. Spawn subagents to read each new source
3. Compare the new information against what the analysis already covers
4. Identify material gaps — information that would change the analysis's
   conclusions, parameter values, risk assessment, or modeling recommendations
5. Do NOT flag information the analysis already covers adequately
6. Do NOT flag minor/cosmetic additions — focus on material impact

## Output

Write structured feedback to this file using the Write tool:
`/home/reid/1cfe/fusion-tea-cohort-rerun/exploration/concept_analysis/analyses/17a-laser-icf-hybrid-drive/iter-5/source_integration_output.md`

Use this exact format:

# Feedback Format

Both the assessment agent and the interactive manage-concept agent produce
feedback in this format. The analysis agent (and, for model-category findings,
the model-setup agent) consume it in feedback-pass mode.

This format is machine-parsed by simple line-anchored scanning. Emit it exactly
as specified — the verdict line and the finding headers are read literally.

## Structure

Each feedback file contains, in order:
1. A **verdict line** — a line reading exactly `VERDICT: PASS` or
   `VERDICT: FINDINGS`, on its own line, with nothing after the token.
   (`VERDICT: PASS — all good` is NOT accepted; put any commentary on a
   separate line.)
2. Zero or more findings (maximum 3 per pass).

## Finding Format

Each finding is a block that begins with a `### F-N:` header (N is an integer:
`### F-1:`, `### F-2:`, …) followed by bold-key bullet lines:

```
### F-N: [Short title]
- **Target:** [Section or artifact the fix lands in — e.g. "Section 5b (Override
  Candidates)" or "model_setup.py overrides list"]
- **Category:** analysis | model
- **Finding:** [What is insufficient, missing, or incorrectly framed]
- **Recommendation:** [What the agent should do differently — specific enough to
  act on without seeing your reasoning]
- **Priority:** blocking | important | minor
```

## Category — exactly two values

Each finding MUST carry a `Category` field whose value is `analysis` or `model`:
- **`analysis`** — the fix lands in `analysis.md` (Design Point block, Section 5
  parameters, Section 5b Override Candidates, family-delta prose, framing).
- **`model`** — the fix lands in `model_setup.py` (the `overrides` list, the
  `spec` dict, sweeps/scenarios, or the two-knob helper call).

There is **no third category.** The new contract's cross-artifact failure modes
route by where the fix lives:
- `P_native` mismatch between the Design Point block and `model_setup.py` →
  `analysis` if the analysis text is wrong, `model` if the model constant is wrong.
- Override `provenance` drift (analysis YAML says `direct`, model says `derived`,
  or vice-versa) → the artifact carrying the wrong label.
- Account-namespace miss (an invented or wrong canonical code) → wherever the bad
  code appears.

## Rules
- Maximum 3 findings per pass — focus on the most impactful issues.
- Findings about numbers focus on *plausibility* (order of magnitude, physical
  reasonableness, design-point coherence), not on re-deriving calculations.
- Each finding must be specific enough to act on without access to your reasoning.
- If the analysis adequately addresses all goals: `VERDICT: PASS` with no findings.

## Example

VERDICT: FINDINGS

### F-1: Override count exceeds the High-fit band without justification
- **Target:** Section 5b (Override Candidates)
- **Category:** analysis
- **Finding:** The concept is graded High archetype-fit (expected 0–4 enabled
  overrides) but the registry enables 7, and three of them re-state the library
  default with no company-published quantity or unit cost in `rationale`.
- **Recommendation:** Disable or remove the three un-evidenced overrides
  (C220105, C220110, CAS24) so the library default stands, leaving only the
  company-grounded departures.
- **Priority:** important


**Adaptation for source integration**: The "Finding" field should describe
what new information the source provides. The "Recommendation" field should
specify exactly where and how to incorporate it into the analysis (which
section, what to add/update). The "Target" field should reference the analysis
section that needs updating.

If the new sources contain no material information beyond what the analysis
already covers, return `VERDICT: PASS`.
