---
Status: draft
Priority: P2
Goal: null
Created: 2026-07-04
Updated: 2026-07-04
---

# Epic Framing: Inverse Solving

**This is a framing, not a decomposition.** It exists so "cost targets driving the analysis backward" stops being an unbacked public claim and becomes a schedulable epic. No work items yet.

## The vision claim it backs

The public post claims cost targets can drive the analysis backward — from a target like $0.01/kWh to the parameter regions that could deliver it. The meta-review (`.project/research/20260704-120000_pipeline-hypothesis-meta-review.md`, gap 2) found no owner and a quiet architectural tension: the differentiable engine that could do this lives in the track being transcribed away from. Inverse capability is also a known evidence gap in the H2 comparison — the derived relations answer "what does this machine do," while the whole costing pipeline actually runs in "what machine do I need" mode (`work/active/WI-016_h2-blind-derivation/comparison.md`, D3 and the concept-01 native inverse run).

## Current state

1costingfe is JAX end-to-end: differentiable, optimizable, with working native inverse and sizing modes (the concept-01 run back-solves P_fus, T_e, n, and Ip from a 233 MWe target today). `sysml-codegen` emits plain Python — not differentiable, executed forward-only through teax (first end-to-end run: WI-013). Every formula transcribed from 1costingfe into SysML moves capability *off* the substrate that can invert it. No repo has a design sketch for inverse solving on the SysML track, and the two-track end-state decision (validation layer vs. migration target vs. parallel) is itself still open — this epic's substrate choice is downstream of that call, or forces it.

## Candidate approaches

**A. Keep JAX as the solve engine, fed by SysML-extracted parameters.**
SysML stays the source of truth for structure, parameters, and citations; inverse solves run in 1costingfe (or a JAX kernel extracted from it) with parameters exported from the models. Cost: a parameter-export bridge and a stated formula-parity obligation between the two implementations — this is exactly the R4 drift surface the meta-review flagged, so it needs the differential parity harness as a standing check. Benefit: full inverse/optimization capability today, zero new solver work, and the bridge is useful under every two-track end state.

**B. Autodiff-friendly codegen target (emit JAX instead of plain Python).**
The generated `forward()` becomes differentiable; inverse solving is gradient descent over it. Cost: a second codegen backend (or a backend switch) in `sysml-codegen`, and the AI implementation pass must emit JAX-safe bodies; the arithmetic envelope (flat `Real`, no conditionals) is actually an advantage here — it is trivially differentiable. Benefit: the SysML track becomes self-sufficient for both inverse solving and derivative-based uncertainty; one substrate, no parity obligation. Real work, in a repo with an existing Phase-6 backlog.

**C. Sweep + interpolation inversion (no gradients).**
Run the forward sweep dense, then read the target contour off the grid — "which region gives LCOE ≤ X" is a slice of the viability map WI-015/WI-012 already produce. Cost: nearly zero beyond the sweep harness; scales badly past ~4 axes and gives regions, not optima. Benefit: honest inverse *answers* (target corridors) with today's plumbing — enough to back the public claim in its corridor-mapping form, if not the optimization form.

## What a first probe would look like

One work item, two halves. (1) The cheap demonstration: on the WI-015 IFE sweep output, extract the LCOE ≤ target contour and publish it as a target corridor — approach C, days of work, makes the claim minimally true. (2) The substrate decision memo: prototype approach A on one relation (export the HIF parameters, run one 1costingfe inverse solve against them) and estimate approach B's real cost against the sysml-codegen backlog, then put the JAX-vs-generated-Python question in front of the user as a one-page decision tied to the two-track end state. The probe's success criterion is not a solver — it is one committed corridor figure plus a decided substrate, so formulas stop migrating away from invertibility by accident.
