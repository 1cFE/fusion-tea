# Audit: study verifier multiplication operands

**Verdict:** Certify
**Audited:** 2026-09-10
**Branch:** test/codex-native-skills
**Commit:** 588eeae88acd35f8674ba5807225ba9f1d8edd63
**Reviewer:** Fresh independent audit agent; did not author the implementation.

## The Point

The native verifier must independently check the multiplication already present in the audited IFE viability heuristic, `(eta * gain_in) >= threshold`. The package-preparation reproducer previously refused this expression. Supporting its operand grammar allows verification to proceed without rewriting the model, trusting generated predicate execution, or omitting a constraint. This correction supplies that capability; it does not establish package readiness or an economic comparison result.

## Summary

The bounded recursive evaluator implements the specified grammar and retains the existing comparison, negation and binding behavior. Fresh operand tests, independent direct checks and the unchanged historical reproducer pass. The recorded final combined regression run supplies the broader MFE evidence, with its inherited skip stated below.

## Product Judgment

This is the right piece of work: the producer that re-derives verdicts now understands the multiplication required by the actual IFE predicate. A fresh child derived its oracle from durable product sources before reading the implementation. The complete [product-lens ledger](product-lens.md) contains one CLEAR block, no unresolved finding, and no epic gate reference. No structural or product-drift smell fired. Arithmetic is evaluated from explicit bindings and catalog IR; ownership of independent verification stays with the existing verifier.

## Findings

### Plan completion

All implementation tasks are verified. The initial existing-suite run is correctly described as mixed-revision evidence, not a clean baseline. The fresh audit and product lens complete the remaining certification task. Closure and archive remain outside this audit.

### Spec conformance

- SC1 [INFERRED], verified: the actual IFE catalog is used at below/equal/above threshold values with qualified input bindings (`tests/study/test_verify_operands.py:15`, `:28`). Comparison and negation remain at `scripts/study/verify.py:207`; 36 independent direct checks covered all six operators across below/equal/above values with and without negation.
- SC2 [INFERRED], verified: recursive binary multiplication adds both child occurrence counts, including repeated features (`scripts/study/verify.py:174`). The retained tests cover literals, nested products, repeated references, missing bindings, unsupported operators/kinds and arities 0/1/3 (`tests/study/test_verify_operands.py:35`, `:48`, `:56`, `:68`, `:79`, `:86`). Refusals name the constraint through `VerifyError`. Fresh direct checks also exercised products on both sides, an oracle-channel leaf, input override precedence, missing multiplication operands and subtraction refusal.
- SC3 [INFERRED], verified within the stated regression evidence: the literal and feature branches preserve previous behavior, and the top-level whitelist and negation are unchanged. The final combined log records 31 passed and one inherited skip; its tests cover all fourteen current MFE catalog constraints (`tests/study/test_verify.py:97`). Inspection of the implementation commit and its whitespace-only follow-up found no changed model, generated package, manifest, runtime dependency, stored study or pending comparison pin.
- SC4 [INFERRED], verified: evaluation uses only the existing binding resolver and Python multiplication (`scripts/study/verify.py:140`, `:197`). No generated predicate call or IFE-specific identifier appears in the generic extension.
- SC5 [INFERRED], verified: meaningful tests are retained, this independent audit and the fresh product lens are recorded, and the exact supported grammar is documented below. The independent audit does not upgrade these agent-originated criteria to owner requirements.

### Design conformance

Implementation follows the design: one operand helper returns value and resolved-feature count, recursively handles exactly binary multiplication, and delegates feature lookup to the existing resolver. The existing comparison loop sums those counts. No undocumented architectural deviation was found.

### Code integrity

No blocking issue found. The helper has one purpose, shallow branching and no silent success fallback. Its context parameters serve the same leaf-resolution operation. Unsupported arithmetic refuses explicitly. The tests exercise the real catalog expression and independently specified numerical outcomes; none passes by choosing between duplicate production routes. Relevant saved feedback on fallbacks, workarounds, test strategy and preserving written requirements was checked.

### Supported grammar and limits

Operands support numeric literals, explicitly bound feature references, and recursively nested binary `*` nodes. Every other arithmetic operator is unsupported, including addition, subtraction, division, exponentiation, remainder and unary arithmetic. Invocation and other operand kinds are unsupported. Multiplication requires exactly two operands. The top level still requires a binary comparison using `<`, `<=`, `>`, `>=`, `==` or `!=`, with the existing entry-level negation flag; logical compounds and arbitrary KerML expressions are not added. General malformed-JSON/schema validation and non-finite arithmetic policy are not part of this correction.

## Certification

- Fresh command: `.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/study/test_verify_operands.py -q'` — 14 passed in 0.06 seconds.
- Fresh direct interpreter checks in the same launcher — 39 assertions passed: 36 literal comparisons/negations, one channel/input product on both comparison sides, and two named refusals.
- Fresh unchanged T-002 reproducer: `PYTHONPATH="$PWD" .codex-test/run python .project/active/ife-native-study-package/probe_verifier.py` — `SUPPORTED`, verdict `[true, 3]`. Historical prerequisite inspected at `5d245388`; historical records preserved.
- Inspected [final-tests.txt](final-tests.txt) — 31 passed, one skipped in 163.01 seconds after code edits. Inspected code/test diffs at `85346980` and whitespace normalization at `588eeae8`. `git diff --check` passed.
- Certification status and verified success-criterion checkboxes are updated in the spec; the final plan checkbox is marked. The coding-PM status pointer is added to CURRENT_WORK without replacing existing owner/setup context. No epic is attached to this standalone correction.

**Not checked:** This audit did not repeat the full 163-second integration suite; it inspected its committed final evidence and ran the focused checks above. The historical proof-of-life store required by `tests/study/test_verify.py:255` is unavailable, so the recorded cross-identity test remains skipped. Native IFE package preparation, complete generated-predicate parity for that future package, model physics, financial normalization, studies, broader expression support and the pending plant-closure comparison were not certified.
