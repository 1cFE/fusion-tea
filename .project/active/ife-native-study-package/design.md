# Design: IFE native study package

**Status:** Accepted execution design, agent-originated
**Created:** 2026-09-10

## The point

Make the corrected IFE model usable by the existing native study workflow, so a later study can record what one pinned machine actually predicts. The package remains the audited machine; this change supplies its missing integration inputs.

## Responsibilities

`exploration/ife_e2e/studies/` owns its annex, manifest, axis declaration, oracle adapter and stock execution route. The route publishes sealed identity and baseline evidence in the exact formats the generic tools already consume. Its stores and temporary import aliases belong to the caller's output directory, outside the sealed package. It uses the stock runner's lease and compatibility contract.

The manifest names all thirty numerical channels for verification coverage, two named predicates, and the current baseline point. These catalog entries are verification observables; declaring them does not turn them into optimization objectives. Beam energy and repetition rate each have one authoritative qualified entry key after WI-048, so no manually maintained identity tie is required.

`oracle_entry.py` maps qualified inputs into the unchanged `tests/ife_oracle.py` calculation and publishes explicit operand bindings for both predicates. The oracle computes physics and annual cash flows independently of generated arithmetic. It currently supports integral construction/operation years; the adapter makes that limitation explicit instead of inheriting silent integer truncation. It does not impose a new model constraint.

The route requires every declared numeric output on successful evidence and verifies both catalog verdicts in stored completed cases. It preserves invalid zero prices and their evidence flags. Package-facing eligibility uses the existing audited `exploration/ife_e2e/eligibility.py` rule. It does not infer generation from price magnitude alone.

Native snapshot capture and census derivation produce files beside the IFE models and in the studies directory. A reproducible preparation script records metadata from the current sealed package and verified baseline. `scripts/integrate.py` subsequently proves a fixed point; no generic producer is edited and no digest is hand-invented.

## Scope and quality choices

[AGENT] Use one implementation phase with direct tests and a fresh final audit. A separate concept stage and pre-implementation review would repeat the established package contract; the native integration gate and independent coding audit supply the useful checks. Do not extract a new shared route abstraction while adding the second package. Keep this route limited to the IFE contract and stock APIs.

[AGENT] Preserve the existing independent oracle in place so earlier test and verification imports remain stable. The annex names both the adapter and its implementation dependency; a future immutable study record must capture both. Any need to change generic seams returns to the goal as a separately owned prerequisite.

[AGENT] Import the new route and oracle by qualified modules under `exploration.ife_e2e.studies`, with repository-root `sys_path`. Reusing the existing MFE flat module names would allow Python module-cache collisions when both packages are verified in one process.
