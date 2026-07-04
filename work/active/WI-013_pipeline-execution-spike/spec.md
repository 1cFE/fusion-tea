---
Status: active
Scale: standard
Epic: "Pipeline De-Risk & Demonstration"
Owner: reid
Created: 2026-07-04
Updated: 2026-07-04
---

# WI-013: Pipeline Execution Spike

## Goal

Close the never-executed gap: run a sysml-codegen-generated pipeline end-to-end through the teax executor and assert numeric output. Generation baselines exist (solar_battery, chain_spike, catf_mfe); nobody has ever executed the generated code. This spike proves — or precisely characterizes the failure of — the assembled path: generate → AI implementation pass fills calc bodies → teax `execute_pipeline()` → numbers.

## Approach

1. Use the solar_battery fixture (`~/1cfe/sysml-codegen/tests/fixtures/solar_battery_model/`) — generation is known-good there, so any failure isolates to the execution path.
2. Run `sysml-codegen generate` to produce the full package (modules, schemas, YAML pipeline, registry) under `exploration/pipeline_spike/`.
3. Act as the AI implementation pass: fill each generated implementation stencil with a faithful translation of its SysML calc def expression, reading the `.sysml` sources directly.
4. Build input JSON from the design values in `design.sysml`, then execute the YAML pipeline through teax `execute_pipeline()` (battery-tea-demo is the reference pattern).
5. Hand-compute expected outputs from the SysML expressions; assert executed outputs match.
6. Establish constraint-predicate status: emitted and evaluable, or confirmed stubbed (codegen Phase 6), with file:line evidence.

## Success Criteria

- [ ] The generated solar_battery pipeline executes under the teax executor without harness-side rewrites of generated files (or every unavoidable touch is documented).
- [ ] Executed numeric outputs match hand-computed expectations from the SysML expressions (exact arithmetic shown; tolerance only for float representation).
- [ ] Every implementation body is a mechanical translation of its SysML expression; any expression that cannot be translated mechanically is flagged.
- [ ] Constraint-predicate status characterized with file:line pointers.
- [ ] Findings document at `work/active/WI-013_pipeline-execution-spike/findings.md` labels every gap as a codegen or teax finding.

A precise gap report counts as success if the executor path is broken — the deliverable is knowledge, not heroics.
