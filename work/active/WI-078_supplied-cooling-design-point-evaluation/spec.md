---
Status: active
Scale: standard
Owner: codex
Created: 2026-09-20
Updated: 2026-09-20
---

# Supplied cooling design point evaluation

[NEED] Preserve supplied design choices through physical relationships, generated/native evaluation and downstream inventory/cost, under MR-7. Source: work/orchestration/goals/preserve-model-design-choices/evidence/owner-prompt.md. The initial inventory and controlling requirement preserve owner versus agent provenance.

[INFERRED] The bounded proposed role/binding contract and acceptance cases are in work/orchestration/goals/preserve-model-design-choices/evidence/cooling-binding-plan.md. Implementation is dependent on its fresh independent design review. Existing empirical/source limits and historical packages/studies remain unchanged; new physical qualification is not inferred from supplied-design evaluation.

## Plan

- [x] Exact binding plan independently reviewed; architecture-review-r2.md approved the narrowed contract plus accepted represented-fill correction.
- [x] Native model and normative seeds implement selected roles; analysis and owned structure twins agree. Evidence: evidence/twins.json, evidence/parser.json; native generated integration remains below.
- [ ] Regenerated current public interface and active consumers migrated; historical replay preserved.
- [ ] Applicable insufficient/sufficient, fixed-hardware/demand and unsupported-domain acceptance run through native route.
- [ ] Affected regressions and independent integrated review support scoped MR-7 disposition.

## Implementation evidence — 2026-09-20

[AGENT] WI-078 seeds separate selected helium/salt price points and purchased stocks from operating heat/flow/work. The primary-loop offered flow ceiling is independent of its hydraulic calibration flow. Required represented fill and optional reserve target remain distinct; two signed kg margins and their conjunction preserve shortage, while `represented_fill_defined` distinguishes active evaluation and `inventory_complete` stays false. Fixed HX/pipe scenario retained.

[AGENT] `tests/models/test_supplied_cooling_design.py`: 20 local tests passed, six native cases explicitly skipped pending coordinator regeneration. Canonical 48-file parser: zero errors. Local checks cover demand-independent selected prices, stock shortages/surplus, independent source-domain flags, fixed IHX failure, oracle agreement and offered-flow/hydraulic independence. These are not native acceptance or off-design machine qualification.

[AGENT] Coordinator owns generic-plant assertions, active study mapping/verify_stellaris, generated ABI integration and full native regressions. New seeds are `seeds/cooling_equipment_impl.py` and `seeds/primary_coolant_loop_impl.py`; historical seeds untouched. Both normative wrappers obtain return order from the emitted output schema model_fields at invocation, avoiding stale tuple-order constants. Preserve old study packages. Review and native acceptance remain open.

[AGENT] Native follow-up: all six supplied-cooling native cases executed and passed in the combined run (47 passes, six initial stale historical-route failures). Current historical-driver tests now explicitly evaluate retained hydraulic perturbations on the current supplied design with legacy/direct cycle closure, comparing all mapped native/oracle outputs; four cases pass. Two retired automatic magnet-selection proposals are explicitly rejected rather than silently translated. The remaining 23 equipment/account tests passed in the intermediate migrated-suite run. Evidence: evidence/migrated-regressions.txt (includes subsequently corrected override-only-input assumption and mismatched cycle-mode failures), evidence/migrated-primary-controls.txt (four corrected controls pass). No historical evidence was changed. Boolean serialization warnings remain visible. Final integrated review and regenerated identity remain coordinator-owned.

[AGENT] Added explicit demand-matched proxy and missing installed-equipment-adequacy disclosures to canonical/twin Turbine Plant, Electric Plant, Heat Rejection and Cryoplant documentation, plus the current study route's result-interpretation contract. No equations, outputs or result schemas changed. Parser remains zero errors. Since these source docs postdate the first generated candidate, final generation identity must include them.
