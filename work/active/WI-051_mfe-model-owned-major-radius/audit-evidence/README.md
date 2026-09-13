# Independent WI-051 audit evidence

[AGENT] Audit of committed implementation `641c1051`, completed 2026-09-12 UTC. [Verdict](../../../analysis/20260912-003541_audit_WI-051.md). The auditor authored only audit evidence/report, the item audit pointer, an independent-audit plan entry and the earned native SV-089 update.

## Executed commands

Commands ran from the repository root. Each top-level script below exited 0. Native complete validation children exited 1 as recorded in their command JSON. Every Python/model/PM child used `.codex-test/run`; TEAx commands used the launcher-contained environment shown here.

```bash
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; exec .codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/audit-evidence/run_tests.py'
.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/audit-evidence/replay.py
.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/implementation/run_acceptance.py work/active/WI-051_mfe-model-owned-major-radius/audit-evidence/acceptance
.codex-test/run bash -c 'export PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1; exec .codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/audit-evidence/old_runner.py'
.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/audit-evidence/check.py
.codex-test/run python work/active/WI-051_mfe-model-owned-major-radius/audit-evidence/citations.py
.codex-test/run agentic-mbse pm update-validation --help
.codex-test/run agentic-mbse pm update-validation SV-089 --status passing
```

Corresponding outputs: `tests.log`, `replay.log`, `acceptance.log`, `old-runner.log`, `check.log`, `citations.log`, `SV-089.log`. Complete native validation CLI commands/exits are in `entering-validation-command.json` and `current-validation-command.json`. Actual production execution commands/exits are in `acceptance/commands.jsonl` and `acceptance/cli-checks.json`.

## Reproduction and retained payloads

`replay.py` and `old_runner.py` intentionally require absent destinations. To reproduce, copy those scripts into a new sibling audit evidence directory before running; do not rerun them into these retained destinations. The acceptance runner accepts a new destination argument. `check.py` reads the corresponding independent replay; do not overwrite this record for a new attempt.

`run_tests.py` executes the unchanged kept suite. Its narrow write guard intercepts only the three retained implementation JSON writes, first requiring exact byte-equivalent text, then writes the duplicate into this directory. It neither changes test assertions nor fakes results. `test-redirects.txt` names the affected files. Tests generate and execute real packages in temporary directories.

`comparison.json` carries every expected/actual scalar, exact named verdicts, all 50 cost/finance modules, ratios, identities, full census and changed bindings. `complete-input-records.json` retains complete old/new parameter records and JSON defaults. `numerics.md` is the human-readable table. `generation.json` lists all package/source hashes and classifies every implementation body. `source-seeds.json` and `snapshot-seeds.json` show the four exact pre-generation seeds; `body-diffs/` retains all 28 regenerated text diffs. `diagnostic-delta.json` retains all L2/L6 diagnostics, normalized by identical source-line mapping, with empty added/removed sets. `regression.json` records every entering/current node and skip reason. `protection.json` retains actual protected deltas and exact parent-commit reconciliation.

`.gitignore` excludes only redundant runtime exports, import links and caches. Full aggregate actual results, per-case input JSON/generated pipeline copies, generated packages, snapshots, original-runner source copies and failures remain retained. No expectation or original evidence was rewritten.
