# Completion audit commands

[AGENT] All commands ran from `/tmp/fusion-mfe-financial-rate-limits` on reviewed revision `614032136b7918a47a889a73147ca51dc15511e2`. Python/model commands use `.codex-test/run`, without synchronization or installation. Evidence files below are relative to this directory unless stated otherwise.

| Command after `.codex-test/run` | Exit and evidence |
|---|---|
| `python -m pytest tests/study/test_financial_consumers.py tests/study/test_major_radius.py tests/study/test_known_answers.py -q --basetemp=/tmp/wi052-completion-audit-tests --junitxml=.project/active/mfe-financial-study-package/audit-evidence/fresh.xml` | 0; 359 passed, coding `audit-evidence/fresh.log` |
| `python .project/active/mfe-financial-study-package/implementation/refresh_metadata.py /tmp/wi052-audit-metadata` | 0; coding `audit-evidence/metadata.log`; hashes checked against retained producer record |
| `python work/active/WI-052_mfe-financial-rate-limits/implementation/native_probe.py /tmp/fusion-mfe-financial-rate-limits/exploration/stellarator_e2e/generated /tmp/fusion-mfe-financial-rate-limits/work/active/WI-052_mfe-financial-rate-limits/completion-audit-evidence/native.json` | 0; native.log/json; all ten cases exactly reproduce prior independent audit |
| `agentic-mbse validate --complete exploration/stellarator_e2e/models` | 1; validation.log; ten retained L2 and 229 retained L6 issues |
| `python work/active/WI-052_mfe-financial-rate-limits/implementation/validation_issues.py exploration/stellarator_e2e/models work/active/WI-052_mfe-financial-rate-limits/completion-audit-evidence/issues.json` | 0; issues.log/json; complete issue capture |
| `python work/active/WI-052_mfe-financial-rate-limits/completion-audit-evidence/check.py` | Final 0; check.log/checks.json/validation-identities.json. Earlier 1 in check-initial.log was duplicate pytest symlink matching; corrected to exact numbered directory. |
| `agentic-mbse pm update-validation SV-092 --status passing` | 0; sv092.log; only that status changed |

The exact 22 affected-node rerun was inspected from committed author JUnit and joined independently, not repeated. Prior numerical, generation and broad regression evidence remains immutable. Runtime import links and disposable study SQLite stores remain in the scratch locations; published scalar comparisons are retained here and in coding audit evidence.
