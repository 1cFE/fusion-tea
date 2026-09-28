# Final whole-plant study review brief

[AGENT] Continue the existing independent review with the new study evidence. Reuse implementation-integration-review.md at executable `6915694e74919ebb764445dfc7f0782eda85a9de29fa44c4b55ffa415c1eb30f`; no model or physical equation change is planned. Reviewers must name any actual identity change before reusing coverage.

## Question

Does the final engineering conclusion follow from a verified whole-plant comparison with the same declared reactor within each pair, a fresh native equipment reranking, visible failed cases and proportionate assumptions?

## Entry evidence

The study record is `exploration/whole_plant_conversion/studies/20260927-design-study-whole-plant-conversion/`. Read its record.md, preparation/summary.json, preparation/case-membership.json, preparation/predicate-catalog.json, preparation/window.json, results/cases.json, results/verification_summary.json and results/presentation/ tables/figures. The full owner brief and reviewed configuration mapping are the requirements/source entry points. The coordinator will name the final result files when ready.

## Required checks

- Confirm exact package and manifest identities, all native lifecycle/preflight/verification gates, complete attempted-case retention and no numerical-error suppression.
- Check native reranking separately for each scenario/source/branch. The metric must be model-owned whole-plant LCOE, with applicable shared and branch predicates satisfied. Old subsystem winners may serve as controls only. Duplicate full points retain every catalog alias.
- Check finite catalog coverage and the reason any nominal failure is excluded from a sensitivity reranking. Performance changes must admit newly passing offers where supported; invariant-failure pruning must have evidence. Explain uncaught window edges and unequal technology freedoms.
- Verify all common inputs within selected pairs match. Follow any branch-dependent source or account consequence. Reuse prior complete inventory/source/MR-7 review unless a changed path demands another check.
- Check power and cost breakdowns against published native outputs. Graphical normalization may show native PV components per native energy PV; it must reconcile to native LCOE and introduce no new model formula or missing expense.
- Check any economic crossover by native evaluation and state held-hardware versus reranked meaning. Failed points must not draw a winner curve. Engineered stresses must not be presented as established credible uncertainty intervals.
- Review plots, proposed article text and answer for a readable causal explanation, clear supplied-source/transport/fit/price qualifications, and the exact unsupported 3000 MW conditions. Reports must use the explicit configuration account mapping, not incorrect generated CAS labels.
- Check required endpoint deliverables and proposed goal finding dispositions. Formal closure remains owner-held.

## Return and ownership

Write `evidence/final-results-review.md`, verdict PASS, FINDINGS or OWNER_GATE, with exact evidence identities, concrete findings/dispositions and remaining limitations. Own that review and any bounded independent probes beneath `evidence/final-results-review/`; do not change the package, study evidence, report code or owner write-ups. Budget: up to 40 tool calls and a substantive return; stop with named missing evidence rather than a weak pass. Wait for coordinator native-ready dispatch before judging result claims.
