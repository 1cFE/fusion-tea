---
Status: completed
Scale: standard
Epic: Pipeline De-Risk & Demonstration
Owner: reid
Created: 2026-07-04
Updated: '2026-07-05'
---

# WI-014: SysML Wiring Construct Validation

## Problem

The WI-010 plant idiom (sketched in `work/active/WI-009_mfe-cost-structure-library/design.md`, "Structure ↔ behavior binding") depends on two SysML v2 wiring constructs:

1. **Usage-level calc chaining** — a calc usage's input bound to another calc usage's result (`in x = someCalc.result`) inside a `part def`.
2. **Part-level `assert constraint`** whose inputs are calc outputs.

The epic flags these as unexercised. Corpus reality is slightly better but still leaves the exact combination unproven:
- `hif_plant.sysml:199` chains calc results, but inside a part *usage*, not a part def.
- `ife_plant.sysml:155` has a part-def-level `assert constraint`, but its inputs are plain attributes (`driver.efficiency`), not calc results.

Neither construct has been (a) evaluated numerically through syside, or (b) run through sysml-codegen extraction.

## Scope

Build a minimal toy model at `exploration/construct_validation/` exercising both constructs exactly as the WI-009 sketch draws them, then validate at three depths:

1. **Parse** — `syside check` clean (Level 1).
2. **Evaluate** — chained calc computes the correct number via the syside Python API (Compiler.evaluate), not just parses.
3. **Extract** — sysml-codegen extraction over the toy; both constructs survive into the computation graph, or the gap is characterized at file:line of the extractor.

## Acceptance criteria

- [ ] Toy model (2 files max): two chained calc defs used inside a part def with usage-level binding, a derived attribute reading a calc result, and a part-level asserted constraint taking calc outputs.
- [ ] `uv run syside check` clean, or the rejection precisely characterized.
- [ ] Numeric evaluation of the chain proven correct against a hand computation.
- [ ] Codegen extraction outcome characterized for both constructs.
- [ ] Learning record in `work/learnings/` — the copy-paste-ready idiom for WI-010, or the gap + recommended alternative.
- [ ] `findings.md` with a verdict for the WI-010 plant idiom: usable as sketched / needs modification / blocked.

## Out of scope

Any MFE model authoring (WI-009–011); fixing codegen if extraction fails (file the gap, don't patch).
