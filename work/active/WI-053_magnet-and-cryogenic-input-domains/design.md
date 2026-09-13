---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts:
  Spec: ./spec.md
---

# Design

[AGENT] Use the established output-only calculation and typed native manual completion pattern from WI-052. Keep the two existing calculation interfaces and their plant bindings. Put normative domain conditions and valid equations in the canonical calculation documentation; executable manual bodies enforce those domains before evaluating the unchanged expression sequence. Copy canonical definitions to their existing family twins and regenerate the package with an explicit preserved seed inventory.

The field calculation belongs to the magnet analytical chain: plant radius and radial-build coil centre feed live clearance, and independent reference anchors normalize the field before conductor-limit evaluation. Cryogenic electrical demand belongs to the refrigeration chain: cold-mass load and temperatures determine wall-plug load consumed by the plant power balance. No physical ownership or public producer/consumer relationship changes.

The installed constraint pattern distinguishes evaluated assertions from runtime rejection. Assertion verdicts deliberately do not raise; require/assume constraints are cataloged without execution. Neither establishes pre-arithmetic rejection. Manual completion can raise a named ValueError at the calculation boundary, as existing native manual calculations already do. A new shared exception or tooling policy adds no value to this bounded correction. Verify the actual generated wrapper and PreparedEvaluator behavior before treating this choice as demonstrated.

For field arithmetic, test live clearance first, then reference clearance; only after both pass compute the existing bore factors, ratio and ordered product. For cryogenic arithmetic, check T_cold > 0 and T_amb > T_cold before evaluating cold load, Carnot COP, actual COP and electrical demand. Use negated positive comparisons to refuse NaN when it reaches these guards; this does not claim generic finite-number validation. Do not clip negative outputs or modify engineering predicates. Valid default temperatures preserve zero-load and direct-power behavior.

Retain Source/Ref/Basis citations and the existing equations verbatim in normative documentation. This is an algebraic domain repair, not new calibration or a claim of physical validation of the anchored shape. Internal intermediate attributes become implementation locals; no existing public output is removed. The resulting catalog correctly identifies both calculations as requiring manual completion.

Consumer handoff: current verify_stellaris.py mirrors both equations and needs matching bounded refusals. Existing T_amb public oracle coverage remains outside scope unless the coordinator identifies a prerequisite. Package regeneration must preserve the eight actual existing manual/helper seeds and the two new bodies. Historical studies and original numerical evidence remain untouched.
