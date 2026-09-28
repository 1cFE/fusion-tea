# Independent diagnostic design review

[AGENT] Reviewer: source-review agent, 2026-09-20. I did not author the failure-propagation design, probe or native implementation. Reviewed `design.md`, `implementation-plan.md`, the retained probe, and the current native executor/evaluator/evidence interfaces. This reviews the proposed diagnostic contract, not implementation correctness or scientific validity of a model run.

Verdict: **PASS for the bounded additive design**, subject to implementing the stated validation obligations. No reference execution or runtime adoption is approved by this review. Coordinator release remains an execution coordination step.

## Finding resolved during review

**R1 — Invalid intermediate numbers must stop their branch.** The initial publication-only filter could allow a module to emit infinity and a descendant to convert it into a plausible finite zero. The revised design checks numeric scalar/root publications before the producer is marked completed, atomically removes the whole producer's publications on failure, records `unavailable_numeric_output` and blocks descendants. The implementation plan now requires the infinity-to-zero counterexample test. This resolves the design blocker; implementation review must verify the actual execution order.

## Accepted boundaries

- The separate diagnostic method returns its own evidence type and schema. It does not synthesize ordinary model evidence, a completed study case, aggregate predicate satisfaction or a replacement comparison result.
- A module exception and a blocked descendant remain different records. Current generic `ValueError` guards do not establish a machine-readable scientific unsupportedness category. Preserve exception details and causal roots without turning exceptions into physical constraint violations.
- Independent continuation follows declared native dependencies and reuses native binding/execution. A failed multi-output module contributes no outputs. Defaults cannot become fallback values for failed providers. Each ExitPoint binding receives its own availability record even when the aggregate ExitPoint is blocked.
- A completed false predicate remains violated; a blocked or missing predicate is unavailable. Structured native indeterminate results remain distinct. Unknown status tokens must fail closed or be explicitly unsupported, rather than guessed into a known verdict.
- Graph-independent LCOE arithmetic may be retained only as a conditional diagnostic. The consumer must apply the current model-definedness overlay, preserve unsuccessful/unknown engineering predicates and withhold whole-plant acceptance. Finite arithmetic alone is not a scientifically qualified prediction.
- Source pins, model fingerprint, input digest and diagnostic schema/version distinguish this experiment from ordinary historical evidence. Historical failure records stay intact.

## Implementation checks that remain

[AGENT] The author must demonstrate the diamond graph, two independent failures, partial multi-output rollback, invalid intermediate blocking, missing/default behavior, fresh-context isolation, unknown predicate vocabulary and unchanged ordinary fail-fast/success behavior. The real-package synthetic-fault check must compare every retained independent finite result and predicate with the unchanged baseline, while preserving each other failure that actually occurs. Do not report expected graph counts as executed recovery before that check runs.

[AGENT] Every unavailable publication, including a missing structured publication, must prevent a `complete_diagnostic` headline. Neither headline permits a scientific feasibility claim. Retain precise module failure versus descendant blocking versus numeric invalidity in the serialized record.

[AGENT] Channel rollback is not a transaction over arbitrary Python side effects. Dataflow independence assumes modules respect the existing interface and do not mutate upstream payloads or shared external state. Record that limit; a new general transactional execution system is outside this design. Tests should use the actual native context and declared bindings rather than a second executor in the consumer.
