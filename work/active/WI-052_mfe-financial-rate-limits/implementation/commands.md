
- `native`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/package /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/native.json`; exit 0; `entering/native.log`.

- `validation-canonical`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/models`; exit 1; `entering/validation-canonical.log`.

- `validation-family`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/models`; exit 1; `entering/validation-family.log`.

- `validation-mirror`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run agentic-mbse validate --complete /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/models`; exit 1; `entering/validation-mirror.log`.

- `pytest-models`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python -m pytest tests/models/ -v -ra --tb=short --junitxml=/tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/pytest-models.xml`; exit 0; `entering/pytest-models.log`.

- `pytest-study`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python -m pytest tests/study/ -v -ra --tb=short --junitxml=/tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/entering/pytest-study.xml`; exit 1; `entering/pytest-study.log`.

- `candidate-native`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/generated /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native-results.json`; exit 0; elapsed 12.547s; `implementation/candidate-native.log`.

- `candidate-native`: `/tmp/fusion-mfe-financial-rate-limits/.codex-test/run python /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/generated /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/implementation/native-results.json`; exit 0; elapsed 13.126s; `implementation/candidate-native.log`.
