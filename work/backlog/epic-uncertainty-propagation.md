---
Status: draft
Priority: P2
Goal: null
Created: 2026-07-04
Updated: 2026-07-04
---

# Epic Framing: Uncertainty Propagation

**This is a framing, not a decomposition.** It exists so "uncertainty made explicit" stops being an unbacked public claim and becomes a schedulable epic. No work items yet.

## The vision claim it backs

The program's public framing is corridor *mapping* — and a corridor without uncertainty bands is a line. The blog post claims uncertainty made explicit; the meta-review (`.project/research/20260704-120000_pipeline-hypothesis-meta-review.md`, gap 1) found no owner, no design sketch, in any repo. DI-006 makes the need concrete: center-of-range inputs do not produce center-of-range LCOE ($252.30/MWh at Hawker defaults vs. $68.69 at a realistic point), so single-point evaluation actively misleads. Parametric results should report distributions, not midpoints — that insight is in the registry and nothing acts on it.

## Current state

The parameter metadata already exists and is dead. `'Economic Parameter'` (AD-002) carries value/min/max/sensitivity on all 14 IFE parameters (`models/library/cost_structure/ife_cost_parameters.sysml`); Hawker's Table 3 supplied ranges and Pearson coefficients for every one. Nothing downstream consumes any of it: constraint coverage counts the attributes, no execution path reads them. The sweep designs (WI-015, WI-012) are deterministic grid classification. The one uncertainty analysis anywhere near the project is Hawker's own 10-million-sample Monte Carlo — in the source paper, not in our pipeline.

## Candidate approaches

**A. Range sweeps through the generated `forward()` (min/mid/max per parameter).**
Cheapest credible thing, per the meta-review's own recommendation. Reuses the WI-015 sweep harness verbatim; output is an LCOE band per concept instead of a point. Cost: days once WI-015 exists. Benefit: bands on every headline number; kills the misleading-midpoint problem. Limit: corner combinations without probability weighting — a bound, not a distribution, and correlated parameters overstate the spread.

**B. Monte Carlo over the generated pipeline.**
Sample parameter distributions (Hawker's Table 3 gives ranges and linear/log sampling spaces for the IFE family already), run the generated `forward()` per sample, report percentiles and rank sensitivities. Cost: a sampling harness plus per-sample runtime — plain-Python generated code makes 10⁴–10⁶ evaluations a real (measurable, probably tolerable for 0D models) cost; distributions must be chosen and cited per MR-4, which is genuine sourcing work beyond min/max. Benefit: actual distributions and a sensitivity ranking we can check against Hawker's published Pearson coefficients — a ready-made validation anchor no other approach has.

**C. Analytic/derivative propagation (first-order, or via a differentiable engine).**
Linearized error propagation through the calc chain, or autodiff if execution moves to a JAX-class target (see the inverse-solving framing — the substrate question is shared). Cost: either new codegen machinery or a substrate decision that doesn't exist yet; first-order results are wrong exactly where DI-006 says the models are nonlinear. Benefit: near-free per-point uncertainty once built; shares infrastructure with inverse solving. Premature as a first move.

## What a first probe would look like

One work item, on the WI-015 IFE demonstration (once it exists): take the 14 Hawker parameters with their already-modeled min/max, run approach A (and B if the harness makes it cheap — the sampling spec is sitting in Hawker Table 3), and produce one figure: the HIF LCOE band with the DI-006 point values marked on it. Success criteria: (a) the band is computed from model-carried metadata, not hand-entered ranges — proving the dead attributes can drive analysis; (b) the Monte Carlo sensitivity ranking, if run, is compared against Hawker's published Pearson ordering as the validation check. The probe's real question: is anything beyond the parameter defs needed from the SysML side, or is uncertainty purely a harness concern? The answer decides whether this epic touches the models at all.
