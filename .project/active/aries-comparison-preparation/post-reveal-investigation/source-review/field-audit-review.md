# Independent review of the field audit

[AGENT] Reviewer: source-review agent, 2026-09-20. I authored the separate ARIES source review, not `field-audit/audit.md` or its reconstruction. This review independently checks the field arithmetic and source interpretation. Verdict: **PASS** for the audit's bounded conclusions. It does not validate the transferred field model or authorize a replacement experiment.

## Checked evidence

[AGENT] Independently calculated the axis and peak formulas from the retained receipt's effective inputs. The result is 14.748387096774191 T on axis and 56.61785714285713 T peak, agreeing with the audited calculation and refusal diagnostic. Verified every source-file hash in the arithmetic receipt and every source-evidence hash against current bytes. No plant/native evaluation was run. [Check receipt](field-audit-review-checks.json).

[AGENT] Directly viewed the primary Lion 2021 Equation 39 image, not only the implementation comment. It includes both `a0(C)` and `R*a1(C)/sqrt(Awp)` inside the bracket multiplying `mu0*I*N/(R−a_coil)`. The surrounding retained extraction states that the parameters are fitted from finite-pack magnetic calculations as pack area varies. Its section 2 fixes coil number and shape, permits overall geometric scaling, and describes changing plasma minor radius at constant coil radius. The registered original full PDF is absent; the audit correctly discloses reliance on the primary equation image plus extracted context.

[AGENT] Also inspected Stellaris Tables 2, 3 and 8 directly. They support the aggregate calibration inputs, distinct coil families and centre-filament convention. I suggested one source-precision clarification: Table 2 prints a 24.9 T peak, while Table 8 prints 24.6 T for family 0 and gives 324 turns at 47.6 kA, rather than the model's held 308 turns at 50 kA. Those distinctions should remain visible; one calibration match does not reconstruct the detailed winding. No new baseline or parameter change follows from this observation.

## Findings accepted

- The arithmetic and units are consistent. The high value does not require a turns/current conversion error. That does not establish scientific applicability.
- The normalized omitted bracket depends on an unidentified coefficient fraction and changing `R/sqrt(Awp)`. One anchor cannot identify that dependence. The audit correctly avoids choosing a coefficient, claiming an error bound or asserting a corrected field.
- The proposed similarity class is physically motivated: fixed normalized coil geometry and current distribution, with all relevant lengths including the pack scaling together, preserves the dimensionless geometry. A radius-only restriction around the baseline would not express that physics. The current one-dimensional representation does not prove those conditions.
- A layer-stack coil-centre proxy is not demonstrated to equal the source's average minor coil radius for a nonplanar coil set. Non-similar changes therefore leave both the axis-field linkage and peak-field transfer unqualified.
- Unsupported transfer means the prediction lacks demonstrated applicability. It does not mean the physical design is impossible, nor that the large calculated field is known to be false.
- The ARIES 15.08 T maximum and the held-design 56.62 T diagnostic are not a same-design error metric. The audit preserves coil count, current families, geometry and technology distinctions.
- Recovering arithmetic independent of the conductor failure does not establish independence from the unqualified field assumptions. In particular, any recovered economic result needs a separate scientific-dependency and definedness assessment.

[AGENT] No blocking finding remains in the audit's reasoning. The suggested source-detail clarification prevents overreading baseline calibration; it does not change the audit conclusion. A future scientific repair needs its own specification and review, preserving supplied choices and validating a configuration-specific field model rather than fitting the ARIES result.

[AGENT] Final audit follow-up: the author incorporated the source precision clarification and added a bounded design-choice discussion. The latter distinguishes explicit contiguous-layer geometry coupling from automatic adequacy sizing and identifies downstream inventory/cost effects without asserting a new confirmed MR-7 violation. This is consistent with the review's supported-use conclusion. Verdict remains PASS.
