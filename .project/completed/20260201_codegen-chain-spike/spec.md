# Spec: Codegen CalcUsage-Chain Spike

**Status:** Complete
**Owner:** Reid Westwood
**Created:** 2026-02-01 20:17:47 UTC
**Complexity:** LOW
**Branch:** visualization

---

## Business Goals

### Why This Matters

The 5 system-level CalcUsages in the solar+battery model form a dependency chain — LCOECalc consumes outputs from EnergyProductionCalc, AnnualizedOMCalc, AnnualizedFuelCalc, and AnnualizedFinancialCalc via dot-notation bindings. If sysml-codegen can't resolve these inter-calc dependencies and produce correctly wired pipeline YAML, Items 4 and 5 of the end-to-end pipeline epic will require significant unplanned work.

This spike answers that question cheaply with a minimal model before committing to the full pipeline integration.

### Success Criteria

- [ ] Clear go/no-go decision on whether codegen handles CalcUsage chains
- [ ] Any gaps or failure modes documented with estimated fix scope
- [ ] Confidence to proceed (or pivot) on Items 4-5

### Priority

P0 — runs in parallel with Item 1, blocks Items 4 and 5.

---

## Problem Statement

### Current State

- sysml-codegen works for independent top-level CalcUsages (proven)
- The extraction pipeline has `CHAIN` binding type support and topological sorting in `graph_builder.py`
- It is **unknown** whether codegen correctly resolves calc-to-calc data flow end-to-end
- It is **unknown** whether generated pipeline YAML orders modules correctly for a DAG
- No test has ever exercised a CalcUsage chain through codegen

### Desired Outcome

A tested, documented answer to: "Does sysml-codegen correctly extract a DAG of CalcUsages where one calc's output feeds as input to another, and generate correct pipeline YAML with proper module ordering and data wiring?"

---

## Scope

### In Scope

1. **Minimal chain SysML model** — 2-3 CalcDefs where Calc B takes Calc A's output as input
2. **Running codegen** on the test model
3. **Evaluating generated output** — CalcUsage discovery, pipeline YAML wiring, module ordering
4. **Documenting findings** — go/no-go decision with details

### Out of Scope

- Cost patterns or nested CalcUsages (Item 6 scope)
- Full solar+battery model (Item 1 scope)
- Filling in handwritten implementations (structure check only)
- Fixing codegen bugs (document only; fixes are separate work)
- Any changes to sysml-codegen itself

### Edge Cases & Considerations

- The minimal model should use a simple, verifiable domain (not solar/fusion) to keep focus on the chain mechanism
- Chain bindings use SysML dot notation (`calc_a.output_name`) — the model must exercise this exact syntax
- Codegen may discover CalcUsages but fail at the graph-building or YAML-generation stage — evaluate each stage independently

---

## Requirements

### Functional Requirements

1. **FR-1**: Create a minimal SysML model at `models/tests/codegen_chain_spike/` with 2-3 CalcDefs forming a dependency chain where at least one CalcDef consumes the output of another via dot-notation binding
2. **FR-2**: The minimal model MUST compile cleanly (`uv run syside check` exits 0)
3. **FR-3**: The model MUST have explicit top-level CalcUsages in a design file (matching the pattern codegen expects)
4. **FR-4**: Run `sysml-codegen generate` on the model and capture all output
5. **FR-5**: Evaluate whether codegen discovers all CalcUsages in the chain
6. **FR-6**: Evaluate whether generated pipeline YAML has correct inter-module data wiring (upstream calc outputs mapped to downstream calc inputs)
7. **FR-7**: Evaluate whether module ordering in the pipeline respects the dependency DAG
8. **FR-8**: Document findings as a go/no-go decision for Items 4-5, including:
   - What works
   - What doesn't work (if anything)
   - Estimated fix scope for any gaps found

---

## Acceptance Criteria

### Core Functionality

- [ ] Minimal chain model exists at `models/tests/codegen_chain_spike/`
- [ ] `uv run syside check models/tests/codegen_chain_spike/` exits 0
- [ ] `sysml-codegen generate` has been run on the model
- [ ] Codegen output evaluated for CalcUsage discovery completeness
- [ ] Codegen output evaluated for pipeline YAML inter-module wiring correctness
- [ ] Codegen output evaluated for correct topological module ordering
- [ ] Go/no-go decision documented with supporting evidence

### Quality & Integration

- [ ] Existing tests continue to pass (no changes to existing code)
- [ ] Model follows established SysML v2 patterns from coffee maker / solar battery references

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-end-to-end-pipeline-derisking.md` (Item 2)
- **Design:** `.project/active/codegen-chain-spike/design.md` (to be created)
- **Reference model:** `models/tests/solar_battery/design.sysml` (lines 68-97 show the chain pattern)
- **Codegen source:** `/home/reid/1cfe/sysml-codegen/`
- **Key codegen files:**
  - `src/sysml_codegen/extraction/usage_extractor.py` — CalcUsage extraction
  - `src/sysml_codegen/resolution/graph_builder.py` — dependency graph and topological sort

---

**Next Steps:** After approval, proceed to `/_my_design`
