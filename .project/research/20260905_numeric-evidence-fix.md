# Numeric study evidence repair

## Requirements and scope

- [NEED] The owner requested the cleanest complete fix across relevant repositories, implemented in new worktrees and branches from `main`, pushed with one PR per affected repository (2026-09-05).
- [INHERITED] The investigation at `fusion-tea:.project/research/20260905-091948_blank-study-column-root-cause.md` found that TEAx omits plain numeric exit values, local exporters write missing values as blank cells, and verification silently drops missing comparisons. That report lives on the owner's working branch; its reproduction traced module output through reopened study evidence.
- [INFERRED] Publish supported numeric exit values in TEAx, retain exit names, and enforce a new bound evidence version so an old store cannot silently mix evidence coverage.
- [INFERRED] Use each exporter's existing column map for execution admission and export. Refuse absent or null required outputs before a bulk study or CSV publication. Validate all returned completed cases, including resumed cases.
- [INFERRED] Verification must refuse missing numeric coverage for the objectives and predicate operands it already claims to compare. This does not add a permanent oracle obligation or expand that comparison set to every export column.
- [INFERRED] Assert explicit mixed-output values through real evaluation, persistence, reopening and querying in TEAx and codegen; test fusion-tea's real package and every local exporter on `main`.

## Design decisions

These decisions are agent-originated. TEAx owns numeric publication and evidence schema `v3`; codegen retains its existing supported scalar-field emission. Fusion-tea reuses its column maps through a `required_channels` route argument, binds that map into the study definition fingerprint, and checks one proposal's actual evidence before opening the study store. This costs one extra evaluation per invocation and avoids a second metadata schema or copying TEAx's projection predicate. Every exported case remains checked independently.

The three local exporters on `main` are in scope. Five later exporters in the report are on unmerged study branches and will need to use the same helper when those branches integrate. Historical CSVs and stores remain evidence of their original runs; missing values cannot be recovered by re-querying. A v3 rerun starts a fresh store and records the TEAx revision without changing the generated package's fingerprint.

## Validation

The numeric-evidence and publication suites pass all 35 tests. They cover all three local exporters, absent/null values in first and later rows, preservation of existing CSV bytes, declaration changes refusing store resume, and incomplete persisted evidence refusing after a complete admission check. A separate agent reviewed the full fusion-tea change and found no blocking defect. Shared route, verifier, and changed tests pass Ruff; historical exporters retain their pre-existing style findings.

The real `main` package's five formerly blank power-balance fields and wrapped LCOE survive a reopened v3 store. A separate read-only reproduction against the owner's newer sealed heating package also passed: four stored values `100 / 50 / 50 / 0.5`, 98 numeric outputs instead of 60, and the historical exporter emitted `50.0`; LCOE stayed `313.5134115016116`. Temporary trace: `/tmp/fixed-heating-acceptance-trace.json`. No historical artifact was rewritten.

Runtime prerequisite: [TEAx PR #5](https://github.com/rwestwood89/teax/pull/5). Its 432 tests pass. The companion codegen real-runtime lane passes 96 tests and demonstrates that the new acceptance fails against the old TEAx projection. The complete fusion-tea study suite, including integration-seam regeneration, lineage, preflight and oracle verification, passed: 375 passed, 1 skipped in 387 seconds.

Worktree validation reused the primary sealed interpreter with its two environment files, `STOP_PARSER_TEAX_ROOT=/tmp/teax-numeric-evidence`, `STUDY_REQUIRE_TEAX=1`, `PYTHONPATH` containing only the fusion worktree, and `UV_CACHE_DIR=/tmp/fusion-evidence-uv-cache`, `UV_PROJECT_ENVIRONMENT=/home/reid/1cfe/fusion-tea/.venv`, `UV_NO_SYNC=1` for regeneration subprocesses. The command was `/home/reid/1cfe/fusion-tea/.venv/bin/python -m pytest tests/study -q --tb=short`. The first attempt hit a read-only uv cache; the corrected environment passed without changing production code. The historical exporters retain 21 existing Ruff style findings, matching their `main` baseline; changed shared code and tests are lint-clean.
