# Full pytest gate — 2026-10-06

The full pytest gate is blocked during collection by an expired Syside license. No tests executed in the three standard full-gate attempts. A supplemental diagnostic run executed some collectable tests before a requested graceful stop; its incomplete results are recorded below. The observed failures are environmental, not evidence of a regression in the closure change.

## Runtime and scope

- Checked commit: `421966070123ad31f53b1872949779d78e2fa8ca`.
- Python 3.12.3; interpreter `/home/reid/1cfe/fusion-tea/.venv/bin/python3`.
- All three attempts sourced `/home/reid/1cfe/agentic-mbse/.env` and `.venv/integration.env` under `set -a`, without printing credentials. Attempt 3 overrode only `SYSIDE_LICENSE_KEY` in the pytest child using the existing project `.env` before importing pytest or Syside; that credential also reports expired.
- `UV_PROJECT_ENVIRONMENT=/home/reid/1cfe/fusion-tea/.venv`, `UV_NO_SYNC=true`, `UV_OFFLINE=true`, and `UV_CACHE_DIR=/tmp/fusion-tea-pre-pr-uv-cache`. No dependencies were synchronized or changed.
- `PYTHONPATH="$PWD:$STOP_PARSER_WHEEL_TARGET:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"`. The configured wheel target is `/home/reid/1cfe/fusion-tea/.venv/lib/python3.12/site-packages`; the configured TEAx root is `/home/reid/1cfe/teax`. Imported `agentic_mbse`, `sysml_codegen`, and `costingfe` all resolve under that wheel target. Runtime paths alone do not freshly certify installed wheel contents; the provenance tests did not execute.
- Full suite uses the configured `testpaths = ["tests"]`. No `-k`, test path exclusions, marker exclusions, or slow-test exclusions were added.
- Historical WI-096–100 paths were exposed only by the temporary `scripts.archived_work` context. All three attempts removed their aliases afterward; no permanent active aliases were introduced.

Exact command for attempts 1 and 2:

```bash
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python -m pytest -q
```

Exact command for attempt 3:

```bash
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python -c 'import os; from dotenv import dotenv_values; os.environ["SYSIDE_LICENSE_KEY"] = dotenv_values(".env")["SYSIDE_LICENSE_KEY"]; import pytest; raise SystemExit(pytest.main(["-q"]))'
```

## Results

| Attempt | Runtime access | Result | Log |
|---|---|---|---|
| 1 | Workspace sandbox | Exit 2; 1 collection error in 4.77 seconds; 0 tests executed | `/tmp/20261006-pre-pr-tests.log` |
| 2 | Approved escalation for license-server access | Exit 2; 1 collection error in 3.35 seconds; 0 tests executed | `/tmp/20261006-pre-pr-tests-network.log` |
| 3 | Approved escalation; existing project credential | Exit 2; 1 collection error in 3.03 seconds; 0 tests executed | `/tmp/20261006-pre-pr-tests-project-key.log` |

All three failures occur at `tests/models/test_beta_peak_field.py:14`, on `import syside`. Attempt 1 could not contact the license server. Attempts 2 and 3 reached it and returned `License expired`, using the shared and project credentials respectively. The material blocker is therefore an expired license under both existing credential sources. Runtime identity output is retained in `/tmp/20261006-pre-pr-tests-runtime.log`.

Full-suite aggregate pass, fail, and skip counts are unavailable because collection stopped. A refreshed valid Syside license is required to run the unchanged full gate. No model or physics source checks were added, and no source fixes were made for these failures.

## Supplemental diagnostic run — incomplete

An additional run retained collection errors and continued into every collectable test without exclusions. It used the same network-enabled environment and project credential as attempt 3, changing only the pytest arguments to `["-q", "--continue-on-collection-errors"]`. Its command was:

```bash
uv run --no-sync python -m scripts.archived_work -- uv run --no-sync python -c 'import os; from dotenv import dotenv_values; os.environ["SYSIDE_LICENSE_KEY"] = dotenv_values(".env")["SYSIDE_LICENSE_KEY"]; import pytest; raise SystemExit(pytest.main(["-q", "--continue-on-collection-errors"]))'
```

The coordinator requested a graceful stop once repeated environment failures dominated the diagnostic run. SIGINT was sent only to the identified pytest process group. Pytest printed its partial summary, exited 2, and the wrapper cleaned up the temporary archive aliases. The log is `/tmp/20261006-pre-pr-tests-supplemental.log`.

Partial totals: **1 failed, 654 passed, 12 skipped, 104 warnings, 468 errors in 201.37 seconds**. These are incomplete diagnostic totals, not a full-suite pass or completed gate.

| Observed category | Count | Evidence and cause |
|---|---:|---|
| Test failure | 1 | `tests/models/test_computed_tritium_breeding.py:218`: code-generation subprocess fails because Syside reports an expired license. |
| Browser setup errors | 226 | Missing `greenlet` prevents importing Playwright: 118 at `tests/model_viz/conftest.py:29`, 91 at `tests/model_viz_v2/conftest.py:30`, and 17 at `tests/model_viz_evolution/conftest.py:51`. |
| Model code-generation setup errors | 235 | `tests/models/optional_magnet_analysis.py:47`: shared fixture assertion fails after exact-route validation reports the expired license. |
| Model parsing setup errors | 6 | Two each at `tests/models/test_example.py:43`, `tests/models/test_example.py:54`, and `tests/models/test_foundation.py:73`; Syside reports the expired license. |
| Collection error | 1 | `tests/models/test_beta_peak_field.py:14`: expired license. |

The observed failure and errors are environment failures in existing tests. No independent regression in the closure change was observed in this partial run. The missing browser dependency was not installed, and the license was not replaced. The incomplete run does not establish the behavior of tests that had not executed when it stopped.

## Browser groups with isolated optional dependency

The coordinator recovered the existing cached Python 3.12 `greenlet` 3.3.2 wheel, matching `uv.lock`, and verified 95 wheel RECORD hashes. Its package and distribution metadata were copied only to `/tmp/fusion-tea-pre-pr-optional`; `.venv` and project dependencies were not synchronized or changed. The receipt is `/tmp/fusion-tea-pre-pr-greenlet.json`.

The three whole browser groups ran with approved localhost/browser access, the same sourced integration environment, and `PYTHONPATH="$PWD:/tmp/fusion-tea-pre-pr-optional:$STOP_PARSER_WHEEL_TARGET:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit"`. No archive wrapper was needed. Exact command:

```bash
uv run --no-sync python -m pytest -q tests/model_viz tests/model_viz_v2 tests/model_viz_evolution
```

Result: **153 passed, 108 errors in 93.65 seconds**, exit 1. Log: `/tmp/20261006-pre-pr-tests-browser.log`. The cached optional dependency resolved the missing-`greenlet` import errors and allowed real browser execution.

All 108 remaining errors are a combined-group fixture lifecycle issue: 91 at `tests/model_viz_v2/conftest.py:31` and 17 at `tests/model_viz_evolution/conftest.py:52`. Each group owns a distinct session-scoped browser fixture that starts a Playwright sync manager; the first group's manager remains live when the next group starts its manager. Playwright refuses with `It looks like you are using Playwright Sync API inside the asyncio loop.` These existing fixture errors are independent of the Syside license and the closure change. No source fix was made during this run.

## Authorized test harness repair

- [INFERRED] All three browser groups must share one session-scoped Playwright sync manager so the combined pytest invocation can run their browser fixtures without a competing event loop. Source: the combined run's 108 identical setup errors and the coordinator's authorization to repair that lifecycle.
- [AGENT] Retain each group's session-scoped Chromium browser and page guards/assertions. Missing Playwright must fail loudly. Change only test fixtures; no product, model, or snapshot changes.

Implemented in `tests/conftest.py`, `tests/model_viz/conftest.py`, `tests/model_viz_v2/conftest.py`, and `tests/model_viz_evolution/conftest.py`. The root lazy session fixture starts and stops the sync manager once. Each group still launches and closes its own Chromium browser. Page guards, assertions, snapshot checks, and install-help failures remain in place.

The same combined three-group command now exits 0: **261 passed in 206.52 seconds**, with no exclusions or skips. The runtime still uses the verified cached `greenlet` in `/tmp`; no dependencies were synchronized or installed into `.venv`. Log: `/tmp/20261006-pre-pr-tests-browser-repaired.log`. The initial 153-pass/108-error result above is retained as the reproducer; this final result verifies the fixture repair.

Targeted `uv run --no-sync ruff check` and `uv run --no-sync ruff format --check` pass on all four changed fixture files. `git diff --check` also passes. Formatting was applied while the browser run was underway; `ast.dump` comparison verified exact syntax-tree equivalence for all four files against their lifecycle-fixed pre-format versions. That reference is `/tmp/20261006-pre-pr-browser-asts.json`. No test logic changed in the formatting finish.

The browser gate now passes in one pytest process. The full pytest gate remains blocked by the expired Syside license; the browser result does not replace that missing full-suite result.

## 2026-10-07 completed retry supersedes the license blocker

The project `.env` key now imports SysIDE successfully. After correcting temporary browser-overlay metadata pollution and restarting the full suite, the complete run exits 1: 5,717 passed, 148 failed, 24 errors, 58 skipped, one xfailed and 660 warnings in 7,377.55 seconds. No `License expired` appears in the completed log. [Retry record](20261007-pre-pr-test-retry.md) supplies the command, receipt and failure inventory. The gate is now FAILED on tests, not blocked on license collection.
