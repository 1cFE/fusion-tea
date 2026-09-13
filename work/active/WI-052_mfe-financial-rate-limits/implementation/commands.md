
- `native`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/package /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/native.json`; exit 0; `entering/native.log`.

- `validation-canonical`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/models`; exit 1; `entering/validation-canonical.log`.

- `validation-family`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/models`; exit 1; `entering/validation-family.log`.

- `validation-mirror`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/models`; exit 1; `entering/validation-mirror.log`.

- `pytest-models`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python -m pytest tests/models/ -v -ra --tb=short --junitxml=/tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/pytest-models.xml`; exit 0; `entering/pytest-models.log`.

- `pytest-study`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python -m pytest tests/study/ -v -ra --tb=short --junitxml=/tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/pytest-study.xml`; exit 1; `entering/pytest-study.log`.

- `candidate-native`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/generated /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native-results.json`; exit 0; elapsed 12.547s; `implementation/candidate-native.log`.

- `candidate-native`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/generated /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native-results.json`; exit 0; elapsed 13.126s; `implementation/candidate-native.log`.

- `validation-canonical`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/models`; exit 1; elapsed 5.708s; `implementation/validation-canonical.log`.

- `issues-canonical`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/validation_issues.py /tmp/fusion-mfe-financial-rate-limits/models /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/issues-canonical.json`; exit 0; elapsed 6.042s; `implementation/issues-canonical.log`.

- `validation-mirror`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/models`; exit 1; elapsed 4.536s; `implementation/validation-mirror.log`.

- `issues-mirror`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/validation_issues.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/models /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/issues-mirror.json`; exit 0; elapsed 4.524s; `implementation/issues-mirror.log`.

- `validation-family`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/final-models`; exit 1; elapsed 4.532s; `implementation/validation-family.log`.

- `issues-family`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/validation_issues.py /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/final-models /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/issues-family.json`; exit 0; elapsed 4.807s; `implementation/issues-family.log`.

- `entering-issues-family`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/validation_issues.py /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/models /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/issues-family.json`; exit 0; elapsed 4.627s; `implementation/entering-issues-family.log`.

- `candidate-native`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/generated /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native-results.json`; exit 0; elapsed 13.794s; `implementation/candidate-native.log`.

- `pytest-study`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python -m pytest tests/study/ -v -ra --tb=short -o junit_family=xunit1 --junitxml=/tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/pytest-study.xml`; exit 1; elapsed 743.853s; `implementation/pytest-study.log`.

- Traceability creation: `.codex-test/run agentic-mbse pm trace-element --element ''"'"'LCOE DCF'"'"'' --file models/library/analyses/mfe_lcoe_dcf.sysml --type calc_def --source-type codebase --source-doc 'Native MFE DCF equations; inherited 1costingFE economics.py' --source-location 'models/library/analyses/mfe_lcoe_dcf.sysml:4; economics.py:6-10 and 88-92 (inherited); WI-052 design Numerical method and justification' --confidence medium --assumptions 'Midpoint construction multiplier; annual-equivalent energy; exact zero-interest CRF; stable equivalent positive Real-duration finance. External citation inherited, not reverified.'`; exit 0; `traceability-command.log`. Existing Calendar cell amendment followed the parent-routed native implement-model §3 procedure recorded in validation-report.md.

- `.codex-test/run agentic-mbse pm update-validation SV-090 --status passing` and corresponding SV-091 command: both exit 0. SV-092 intentionally remains pending.

- `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/implementation/differentials.py`: exit 1 on the 22 explicitly unresolved new downstream regression nodes; all validation issue identities and inherited regression reasons match. See differential-check.log.
