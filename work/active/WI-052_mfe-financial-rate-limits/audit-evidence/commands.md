# Audit commands

All commands ran from `/tmp/fusion-mfe-financial-rate-limits` with `.codex-test/run` and no dependency synchronization. Audit target: `75d21061b608bc9cad472f68b951f5cdf7847abe`.

- `.codex-test/run python -m pytest tests/models/test_mfe_financial_rate_limits.py tests/models/test_mfe_financial_calendar.py tests/models/test_lifecycle_calendar.py tests/models/test_model_family_spines.py -q -o junit_family=xunit1 --junitxml=work/active/WI-052_mfe-financial-rate-limits/audit-evidence/focused.xml`: exit 0, 139 passed; focused.log.
- `.codex-test/run agentic-mbse validate --complete exploration/stellarator_e2e/models`: exit 1, four levels pass; retained L2/L6 fail; validation.log.
- `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py exploration/stellarator_e2e/generated work/active/WI-052_mfe-financial-rate-limits/audit-evidence/native.json`: exit 1, relative-path import failure; native.log.
- Retry with absolute package/destination paths in the same destination: exit 1, existing scratch symlink; native-retry.log.
- `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/generated /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/audit-evidence/native-absolute/native.json`: exit 0; native-absolute/native.log and native.json. Audit-created loader symlinks were removed after execution; the production package was unchanged.
- `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/audit-evidence/check.py`: initial extra-grid exit 1 on insufficient-precision subnormal reference, retained check-initial.log; final stated-window grid exit 0, 282 checks; check.log and checks.json. Initial subnormal result is not accepted numerical evidence.
- `.codex-test/run python work/active/WI-052_mfe-financial-rate-limits/audit-evidence/validation-identities.py`: exit 0; validation-identities.json, all three surfaces and six levels matched by inspected identity normalization.
