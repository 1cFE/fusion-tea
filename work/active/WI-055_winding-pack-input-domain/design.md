---
Status: active
Created: 2026-09-13
Updated: 2026-09-13
Related Artifacts: spec.md, plan.md
---

# Design

[AGENT] Use the established native typed manual completion pattern. Winding sizing owns finite nonnegative current magnitude and finite positive density. It retains local zero area. Winding stress owns its nonzero side denominator. Plasma sustainment owns its nonzero field denominator: its Albajar calculation divides by B, and its confinement calculation subsequently divides by tau_E, which becomes zero at zero field. The exact narrow consumer additions are authorized by the coordinator's T-042 amendment at `eb341aee`; they preserve supported meaning and standalone axis-field zero behavior.

The magnet occurrence owns I_coil and j_wp. Existing bindings feed sizing and axis field; sizing feeds cold volume and stress; axis field feeds peak field and plasma sustainment. These existing relationships already connect the winding and plasma functions to the physical magnet occurrence. Keep those relationships and all public inputs/outputs. No new checked-current producer or global energized-coil restriction is needed. Independent consumer guards make the zero refusal deliberate regardless of which zero-denominator branch is scheduled first.

Sizing: before `(I_coil / j_wp) ** 0.5 / 1000.0`, reject nonfinite I_coil, I_coil<0, nonfinite j_wp or j_wp<=0 with named ValueError. Stress: reject wp_side==0 with named ValueError before the unchanged `k_sigma * I_coil * B_peak_in / wp_side`. Sustainment: reject B_in==0 with the existing SustainmentError before the unchanged sustainment chain. These two consumer checks cover the demonstrated zero propagation only; other domains remain inherited.

Keep valid expression order exactly. Sizing and stress become output-only canonical definitions with normative documented equations and manual-required bodies. Sustainment already has a manual body; add its zero-domain contract to both model and implementation. Preserve the other nine entering manual/helper seeds. Regeneration must retain twelve normative seeds, with only the existing sustainment seed changed and two new manual bodies. Current seed helpers must migrate separately; historical WI-053 helpers and receipts remain frozen.

Source/domain evidence is in `evidence/source-domain.md`. Correct paired stress to `1000 k_sigma B_peak sqrt(I_coil j_wp)` for amperes/A/mm²/metres. State fixed-field versus linked-field scaling explicitly. Table examples are comparison anchors, never calibration bounds.

Checks: kept component tests exercise public generated wrappers, magnitudes/nonfinite/both signed zeros and unaltered standalone axis zero. Native tests exercise ordinary public overrides and full outputs; zero may raise either named consumer error. Independent current-density/area and stress dimensional identities, six printed coil examples, and fixed-density current scaling establish the equation meaning. Positive native controls and ten existing financial cases compare full entering/candidate outputs and reports exactly. Reuse WI-054 all-level issue identities, run affected all-level checks and model regressions, and attribute new consumer failures separately. No independent completion verdict is claimed by the author.
