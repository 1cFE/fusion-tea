# Independent partial-assessment preflight review

[AGENT] Reviewer `/root/partial_review` inspected `tools/assess.py`, `reporting.py`, `definedness.py`, `qualification.py` and their tests against the partial-assessment spec, field audit and accepted native-runtime review. This is a pre-execution review; no reference evaluation was performed.

The reporting and dependency policy meet the scoped scientific boundary. Both field findings propagate conservatively through the native graph, including unavailable publications. The report preserves native predicate status separately from field applicability and definedness. Raw arithmetic survives model-definedness suppression, while supported predictions and comparison success remain withheld. Six named guards cover four module-wide definedness flags and two output-specific heat-exchanger availability flags. This is a declared guard scope, not certification of every model assumption.

Independently ran the focused tests through `.codex-test/run`: **18 passed**. [Receipt](review-tests.txt). Tests include field-path continuity, missing/ambiguous roots, missing publication coverage, raw LCOE retention without certification, false/missing/malformed guard suppression, specific UA guards and indeterminate predicate preservation. These tests consume synthetic evidence and a generated graph; they do not test a new numerical reference execution.

## Finding R1 — imported runtime identity

**Resolved before execution.** The first reviewed runner verified runtime files on disk and prepended their directory to the import path, but did not check imported native module origins or compare the active source digest with the accepted identity. The corrected runner checks executor, evaluator and diagnostics origins and requires the adopted source digest before numerical execution. Independent rerun passes **22 tests**, including wrong-origin and wrong-digest refusal, immutable first-attempt custody and retained pre-execution identity refusal. [Final test receipt](review-tests-final.txt). Selected typed inputs are also checked for mutation after evaluation.

**PASS for the scoped runner preflight.** The adoption manifest is pending at this checkpoint. Final acceptance must verify its actual pins, the retained attempt receipt, original input equality, full row/predicate identity and unchanged historical evidence. This review does not certify the unqualified field model or establish supported whole-plant economics.
