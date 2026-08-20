# Brief: plan for "Indicator Tool and Package Manifest" (RUN-STUDY Item 3)

Work item home: `.project/active/run-study-indicators/` — spec.md and design.md are ACCEPTED
(design carries all review fixes M1-5 + S1-6 + N1/N5; its Next-Stage Handoff lists what is
fixed: two-module split, CLI, gate order, 12 invariants, both digest recipes, 10 test files,
package_copy factory rules). Write plan.md: phased execution with checkboxes.

Planning constraints:
- Honor the design's "De-risk first": the synthetic two-pipeline fixture is built before the
  mechanical-failure suite.
- Phase order should get the known-answer tests passing against the real package early (the
  spike's `indicators.json` at `.project/active/run-study-reachability-spike/` is the diff
  reference for shared fields).
- The stellarator `manifest.json` authoring phase uses `--print-fingerprint` output; include
  the `uv add jsonschema` dependency step.
- Include the design's Validation Approach as explicit per-phase checks (pytest green at each
  phase, grep-clean test, byte-determinism test, schema validation of real output).
- Every phase runs `uv run python -m pytest tests/study` before its checkbox is ticked.
- Note what each phase commits.
