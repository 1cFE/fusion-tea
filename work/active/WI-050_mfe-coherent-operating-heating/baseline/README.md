# Entering model-test baseline

[AGENT] Captured before production mutation, at accepted-spec revision `54a0725e`. The design prototype runs only in its separate owned directory. Native assessment baseline scalar outputs remain at `work/analysis/20260911-190758_mfe-operating-state-evidence/baseline/all_outputs.json@0dce6053` and are not overwritten.

Command from repository root:

```bash
.codex-test/run bash -c 'PYTHONPATH="$PWD:$STOP_PARSER_TEAX_ROOT/packages/teax-simkit" STUDY_REQUIRE_TEAX=1 python -m pytest tests/models -q'
```

Full output is retained in `tests-models.log`. This is the entering battery, not repair verification or a new integration candidate.

Result: 355 passed, 13 skipped in 20.94 seconds; exit 0. No entering model-test failure. Skips remain visible in the retained log; this run does not convert skipped coverage into verification.
