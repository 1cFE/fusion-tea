# Design: study verifier multiplication operands

**Status:** Accepted bounded design, agent-originated
**Created:** 2026-09-10

## The point

The native verifier must be able to check the multiplication already present in the audited IFE heuristic. Rewriting the model or omitting the predicate would weaken the evidence. Extend only the operand grammar that the real reproducer needs.

## Implementation

Extract the current literal/feature operand evaluation into one helper returning `(value, resolved_feature_count)`. Add binary `*` as a recursive case; each leaf still uses the existing explicit binding resolver. Reject every other operator and incorrect arity with the constraint identifier in the error. `derive_verdict` retains its top-level comparison whitelist, two-operand check and negation behavior, summing the helper's occurrence counts.

The helper evaluates arithmetic from oracle channels and declared inputs. It never calls the generated predicate. Existing comparison results and summary schemas stay unchanged. Tests use the actual IFE catalog plus synthetic nested/refusal cases and the existing MFE verifier suite.

[AGENT] One implementation phase and a fresh final audit are sufficient for this localized extension. Separate shaping and design-review stages would repeat this existing contract without reducing the main risk; real predicate and regression tests address that risk directly.
