# WI-076 implementation checklist

[AGENT] Implements the exact contract in `work/orchestration/goals/preserve-model-design-choices/evidence/facilities-binding-plan.md`. Independent approval: `architecture-review-r2.md`, facilities section. MR-7 scope is represented fit, material capacity, queue capacity and selected-geometry costs; no new physical qualification.

- [x] Reviewed exact binding contract and independent approval.
- [x] Capture full entering inputs, selected dimensions/positions/partitions/parcel with provenance.
- [x] Implement normative supplied-design seed and meaningful low/high/fixed-design tests.
- [x] Bind selected parameters and margin outputs in canonical SysML and twins.
- [x] Migrate live independent facility oracle without changing historical records.
- [x] Focused parser and local behavioral tests.
- [x] Coordinator regenerates and validates native interfaces, constraints and downstream costs.
- [x] Independent integrated review and disposition.

Only the coordinator regenerates the global package or edits global plant constraint inventories. Author owns facility analysis, Buildings block, stellarator buildings literals, new seed/test and live facility oracle. Historical WI-068 artifacts remain unchanged.

## Final technical acceptance

[AGENT] Technical acceptance passed fresh non-author [final integrated review](../../orchestration/goals/preserve-model-design-choices/evidence/final-review.md). Native integration returned CANDIDATE at implementation commit `b11567eb693a4fd6f45a487f75dc5244fb433774`, with all ten gates passing. The broad regression sweep and complete reruns of its two corrected test files are accepted composite evidence; see WI-075 `integration/regression-accounting.json`. Scientific limits and the existing unexecuted read-set coverage check remain disclosed in the goal answer. This active record is retained for provenance; formal goal closure and archival remain owner-held.
