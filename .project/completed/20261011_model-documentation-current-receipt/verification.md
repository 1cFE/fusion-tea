# Current receipt verification

Implemented against committed native documentation/evidence `4ca1f299`. The three-line test diff selects WI-054's `evidence/mfe-candidate-package-hashes.json`; the complete current package-inventory comparison, WI-051 source/snapshot receipts and historical manual-seed assertions are unchanged. WI-053's receipt remains untouched. Native report and identity/preservation evidence are owned by `work/active/WI-054_faithful-model-equations-and-citations/` at that revision.

Coordinator execution: `.codex-test/run python -m pytest tests/models/test_mfe_major_radius.py::test_current_contract_edges_and_fresh_package_agreement -q --tb=short --junitxml=.project/active/model-documentation-current-receipt/verification.xml` returned exit 0, one pass. `git diff --check` on the changed test passed. This resolves the one newly failing node in the author's 305-pass/one-failure focused run; it does not constitute a fresh full-suite run or independent certification.

The fresh native completion auditor must inspect this current dependency and independently rerun the node before T-039's final acceptance. No numerical expectations, historical records, production or oracle changed.

## T-040 source-preservation verification

The independent audit found an additional new failure in `test_binding_documentation_and_source_preservation`. The current test now compares the full executable token sequence for precisely four documentation-changed files with WI-054's frozen entering record at `4ca1f299`. It retains exact canonical/twin bytes, radius binding/documentation assertions, the cryoplant's existing outside-calculation check and other historical byte comparisons. No production or numerical expectation changed.

The first current-radius-module invocation returned 63 passes and one source-preservation failure (`radius-first-attempt.xml`). Its first three-file correction exposed the same stale comment comparison in the Economic Parameter archived citation; the isolated diagnostic is retained in `source-first-attempt.xml`. The dated scope/spec amendment adds only that fourth documented file. Rerunning the affected node returns one pass (`source-verification.xml`), with the 63 unaffected cases retained from the preceding run. This is not a claim of a single fresh 64-pass invocation. All runs used `.codex-test/run`; the full module used the documented TEAx PYTHONPATH and STUDY_REQUIRE_TEAX=1. `git diff --check` on the changed test and coding documents passes.

Final code and expected-token data are separate: the comparison reads committed WI-054 entering tokens, not tokens calculated from current production as its own expected value. The native auditor must independently check this preservation boundary and rerun the repaired node. The original failed JUnit and historical receipts/drivers are preserved.

## Independent acceptance

Native completion audit `work/analysis/20260913-154724_audit_WI-054_faithful-model-equations-and-citations.md@d966f13a` explicitly verifies these current-consumer dependencies. The independent rerun passes both repaired nodes; in-memory mutations show the token comparison rejects numeric/operator/type/quoted-identifier/binding changes while permitting comments. Native handwritten executable preservation is separately verified. This bounded evidence satisfies the small coding contract without a new production feature or shared utility. No whole-project test or source-transcription certificate follows.
