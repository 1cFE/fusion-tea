# Integration file-read coverage

[NEED] Execute a file-read identity gate with negative tests and explicit observational limits. Source: `work/orchestration/goals/model-evaluation-domain-readiness/goal.md`, Answered when and tooling review invariant.

[INFERRED] Gate 6 must resolve pipeline EntryPoint references and invoke the existing manifest coverage assertion. That assertion currently checks resolved path membership, not dynamic reads or content changes. The indicator report already calls it (`scripts/study/indicators.py:819`); the integration comment claiming nothing calls it is incorrect.

[INFERRED] The baseline route subprocess must observe Python file opens from before route import through execution, refuse undeclared package/data dependencies and detect observed dependency changes, retain an evidence report even on refusal, and prevent a candidate when the check fails.

[INFERRED] No model quantity, binding, variable role or price consumer changes. MR-7 compliance is unchanged for this tooling-only scope. Historical reports stay immutable.

[INFERRED] Verification must include actual undeclared input and dependency reads, an external/symlink escape, a changed dependency, successful declared reads and failed-attempt evidence. Public-input consumption tests alone do not satisfy this requirement.
