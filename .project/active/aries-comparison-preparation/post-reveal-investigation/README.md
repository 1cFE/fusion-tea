# Post-reveal field investigation

The source check and independent field audit are complete. ARIES reports 5.70 T on axis and 15.08 T maximum winding-pack field. The latter was already recorded in the original comparison evidence. The model's 56.62 T diagnostic is reproducible arithmetic, but its transfer to the changed geometry is scientifically unqualified. The investigation does not establish a corrected field or a same-design error against ARIES.

- [Findings log for the write-up](findings.md): observed facts, evidence, interpretations, implementation results and remaining work.
- [Source review](source-review/source-review.md): page-verified fields, definitions, technology and revision distinctions.
- [Field audit](field-audit/audit.md): exact reconstruction, source-equation limitations and geometry/interface restrictions; [independent cross-review](source-review/field-audit-review.md).
- [Native diagnostic implementation](failure-propagation/implementation.md): additive independent-branch execution in an isolated source snapshot; [independent implementation review](failure-propagation/implementation-review.md).
- [Recommended next scientific work](next-work.md): explicit field applicability and a qualified geometry-dependent field calculation before another reference comparison.

The diagnostic implementation retains 1,341 numeric results and 66 predicates under a synthetic conductor failure, with exact baseline parity. Five retained checks remain violated and one becomes unavailable. Fourteen focused tests and eleven existing native regressions pass. This is a separate diagnostic capability, not an installed shared-runtime upgrade, a complete study result or a scientifically qualified LCOE prediction.

Original model equations, empirical ranges, packages and reference attempts remain unchanged. No reference request was rerun. The scope and owner instruction are in [spec.md](spec.md); exact preservation is recorded in [the verification receipt](evidence/preservation-after.json).
