# Coupled requirements and selected formulation

[AGENT] Entering revision c4d720db886213de94bf2dc4c3131a3453dca690. Existing baseline and immutable contract copies are in entering/. Dependency detail is in coupled-dependencies.md. Native work item WI-064 owns the proposed optional sizing behavior and its acceptance evidence.

## Variable roles

| Role | Quantities |
|---|---|
| Physical independent choices | Major/minor plasma radius, coil ampere-turns, independently allocated exterior radial thickness and transverse cavity, fixed50kA turn current, pack aspect/construction, extra inventory multiplier |
| Derived quantities | Actual peak field, required tape capacity/count, conductor and pack area, effective pack current density, coil length, tape metres, cold material, fit margins, energy/support/thermal/cost consequences |
| Held calibration/transfer facts | Peak-to-axis reference ratio, reference coil radius/circumference/energy, set current and pack area/perimeter distribution factors, stress transfer/modulus, thermal support geometry |
| Material-performance assumptions | 20K, 200A/4mm at20T, exponent0.6, 6mm by56µm tape, material/orientation factors, assembly retention |
| Acceptance limits | Allowable operating fraction0.8, selected field ceiling24.9T principal case, existing plant predicate limits, unchanged walls/clearances |

[AGENT] Existing selected-envelope sensitivity to30T is historical evidence. The principal joint search holds24.9T rather than raising the acceptance ceiling. Improved-performance sensitivities cannot overcome the separate field predicate. Coil ampere-turns and machine dimensions may change field demand physically. Any comparison to historical30T scenarios is explicitly historical and retains its own acceptance assumption.

## Why a native increment

[INHERITED: STUDY_POLICY §§3–5] Required coupled quantities belong inside the model. An outer harness solve is barred. [AGENT] Current package can evaluate a chosen inventory but cannot derive the minimum current-required inventory; WI-064 adds only that missing calculation. Its optional mode preserves historical reference coordinates. Independent allocation precedes field, so no fixed-point iteration is required; field does not depend on selected pack size in the inherited peak-field approximation. Pack self-field/shape effects are a missing physical dependency and limit qualification.

[AGENT] Default current-driven study uses1.01 times minimum continuous inventory. This is an explicit physical1% excess inventory, leaving allowance0.8 unchanged; it avoids presenting roundoff at the exact equality as physical failure/pass. Exact multiplier1 cases are retained as sizing residual diagnostics, with every native predicate left unchanged.

## Existing evidence reused

[INHERITED] WI-062 reviewed performance normalization/domain and statistical construction transfer; WI-061 local fit and independent allocation interpretation; WI-060 physical tape procurement; WI-059 bore length, thermal and support inventory; WI-063 sheet stock and unpriced manufacturing ledger. No new external fact is required for algebraic inversion. Missing construction/angle qualification remains a limitation, not a reason to fit new performance factors.
