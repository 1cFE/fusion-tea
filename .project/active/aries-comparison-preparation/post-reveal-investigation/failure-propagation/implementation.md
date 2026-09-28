# Implemented native diagnostic continuation

[AGENT] Final independent [implementation review](implementation-review.md): **PASS**. The reviewed candidate passes 14 focused tests and 11 existing upstream regressions, with final synthetic verification under `evidence/synthetic-v2/`. The shared runtime remains unchanged.

[AGENT] The isolated native runtime now exposes `PreparedEvaluator.diagnose()`. Ordinary `evaluate()` remains fail-fast. The new API returns immutable `DiagnosticEvidence`, which has neither the ordinary `outputs` nor `responses` study protocol. The diagnostic keeps finite independent results, identifies module exceptions and blocked descendants, and never creates a completed study case or an aggregate constraint report for missing predicates.

The synthetic conductor fault retained **1,341 of 1,352 numeric outputs and 66 of 67 predicates**. Every retained numeric value and predicate exactly matched the unchanged ordinary baseline. Five retained predicates were violated; the conductor-current predicate became unavailable. The blocked aggregate report remained unavailable. A fresh call after the fault reproduced the baseline exactly. Invalid input mappings remained refused before execution. Evidence: `evidence/synthetic-v2/verification.json` and its full diagnostic documents.

Both LCOE arithmetic outputs survived this synthetic conductor fault because their current graph dependencies use supplied inventory and offers. They are conditional economic diagnostics. Conductor-independent is not field-independent: field feeds plasma and economic dependencies elsewhere. These numbers establish no scientifically supported transfer to reference geometry, no whole-plant feasibility and no conductor-qualified cost prediction. `scientific_qualification` is explicitly `not_established`; model-definedness flags remain a separate recorded overlay.

Only three native files differ from the adopted runtime: `simkit/core/pipeline_executor.py`, `simkit/evaluation/evaluator.py`, and the added `simkit/evaluation/diagnostics.py`. The source snapshot is under `native-teax/`, with exact original hashes in `native-base.json`, resulting hashes in `implementation-identity.json`, and the portable delta in `native-diagnostics.patch`. The shared TEAx checkout, generated models, frozen runtime and historical results were not edited.

Fourteen focused tests cover independent continuation, the ordinary failure path, infinity/NaN/complex intermediate blocking, multi-output rollback, two independent failures, fresh-context behavior, absence of implicit fallback, missing publication, and predicate vocabulary distinctions. They use native graph/binding/execution machinery. The real-package verification additionally covers typed-input refusal, exact baseline parity and the complete current predicate inventory. Runtime Boolean-carrier serializer warnings are retained in the execution log.

Reproduce from the repository's sealed environment:

```bash
BASE=.project/active/aries-comparison-preparation/post-reveal-investigation/failure-propagation
.codex-test/run python -m pytest "$BASE/native-teax/tests" -q -p no:cacheprovider
.codex-test/run python "$BASE/diagnose.py" --out /tmp/native-partial-diagnostic-fresh
```

The output directory must not exist. The diagnostic script accepts no reference request and always uses unchanged baseline defaults with one explicitly injected synthetic conductor exception. Runtime identity and input digest are retained in every diagnostic record. The local source patch has not been installed or adopted as the shared runtime. A separate decision is needed before any actual reference diagnostic execution.

Review scope: validate the native loop's data dependencies and atomic publication, unavailable-state serialization, separate evidence type, ordinary-contract preservation, and all retained parity assertions. Dataflow isolation assumes modules obey the native functional interface. Channel rollback cannot undo arbitrary upstream-object mutations or external side effects.

Eleven existing upstream regressions also passed against this isolated runtime: the native executor's original failure-context tests, multi-output tests and prepared-evaluator tests. `evidence/upstream-regressions-v2.txt` retains the final run. This includes the original nonfinite-to-indeterminate ordinary evaluation behavior; diagnostic finite-publication checks do not change that historical contract.

The initial implementation checked scalar/root publications. Review preparation identified an additional route through a numeric field reference inside a structured object. The final diagnostic loop also checks resolved declared-numeric inputs before invoking a module, preserving typed structured predicate evidence while blocking a numeric infinity-to-zero mask. Fourteen focused tests and eleven original upstream regressions pass on this version. `evidence/synthetic-v1/` retains the initial implementation verification; `evidence/synthetic-v2/` is the final candidate, with the same 1,341 retained numeric values and 66 available predicates. An initial additional test incorrectly mutated a frozen binding; its failed test log and corrected `model_copy` test are retained.
