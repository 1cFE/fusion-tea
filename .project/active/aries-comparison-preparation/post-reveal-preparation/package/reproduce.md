# Restore and operate post-reveal-v1

[AGENT] This archive freezes source and generated artifacts, the current native route, the new adapter/reporter, the mapping evidence, bundled teax runtime source and three sealed wheels. It requires the existing licensed Python 3.12 environment. It does not archive credentials, the interpreter, SysIDE or all third-party dependencies. The verified restoration reuses the sealed environment documented in `.project/codex-test-setup.md`. Restoring on a different machine requires provisioning that environment first; this is not an offline environment installer.

The archive members use repository-relative paths. `freeze-record.json` supplies its SHA256 and the identity-file SHA256. Verify the archive before extraction. Use an empty directory. These shell variables deliberately keep the primary checkout separate from the restored root:

```bash
PRIMARY=/home/reid/1cfe/fusion-tea
PREP=.project/active/aries-comparison-preparation/post-reveal-preparation
RESTORE=$(mktemp -d /tmp/post-reveal-v1.XXXXXX)
sha256sum "$PRIMARY/$PREP/package/post-reveal-v1.tar.gz"
tar -xzf "$PRIMARY/$PREP/package/post-reveal-v1.tar.gz" -C "$RESTORE"
TOOLS="$RESTORE/$PREP/tools"
set -a
source /home/reid/1cfe/agentic-mbse/.env
source "$PRIMARY/.venv/integration.env"
set +a
"$PRIMARY/.venv/bin/python" "$TOOLS/adapter.py" --verify
"$PRIMARY/.venv/bin/python" -m pytest "$TOOLS/test_tools.py" -q -p no:cacheprovider
```

The direct sealed interpreter is the documented secondary-checkout exception. Execution uses bundled teax source automatically; installed codegen, agentic-mbse, costingfe and dependencies remain the external sealed environment. The runtime result records package versions and teax source hashes. `--verify` checks every pinned source byte, including mapping, wheels and generated artifacts; it does not certify the operating system or every installed dependency.

For a synthetic restoration baseline, write an empty-value request, then execute it. These commands do not load the proposed reference request:

```bash
printf '%s\n' '{"schema_version":"adapter-request/v1","purpose":"synthetic_preparation","values":{}}' > "$RESTORE/synthetic.json"
"$PRIMARY/.venv/bin/python" "$TOOLS/adapter.py" --request "$RESTORE/synthetic.json" --store "$RESTORE/synthetic-attempts" --attempt baseline
"$PRIMARY/.venv/bin/python" "$TOOLS/observations.py" --attempt-dir "$RESTORE/synthetic-attempts/baseline" --output "$RESTORE/synthetic-observations.json"
"$PRIMARY/.venv/bin/python" "$TOOLS/report.py" --attempt-dir "$RESTORE/synthetic-attempts/baseline" --observations "$RESTORE/synthetic-observations.json" --store "$RESTORE/synthetic-reports" --name baseline
```

Expected baseline: completed arithmetic, 1,352 numeric outputs, 67 predicates with six violations. Expected unfilled report: all 276 rows retained, missing reference observations block comparison. Native warnings about numeric Boolean carriers are retained runtime warnings. Completed arithmetic does not establish engineering acceptance.

For separately authorized reference execution, replace the synthetic request with `mapping/proposed-reference-request.json`, whose purpose is `post_reveal_comparison`, and use the separate register named in `../execution-prompt.md`. Run/export is one command: `adapter.py` writes `model-export.json` automatically. An exit code of one retains refusal/failure evidence; it is not permission to edit the request or skip the first attempt. A hard interruption has no terminal result and can still produce an unavailable 276-row worksheet/report. Reports exclusively reserve their own first-attempt pointer and retain refused report attempts.

`observations.py` emits the historical observation schema. Its `run_kind: conditioned` selects the shared comparator's conservative arithmetic semantics; the resulting report is explicitly post-reveal and never blind. Reference unit/basis/scope/technology fields start unresolved. Fill them from cited source evidence; keep unsupported fields unavailable and include source page/table and unresolved mapping limits in `applicability_evidence` or notes. The tool checks all supplied model observations against native outputs. It does not infer scientific correspondence from matching units or values. The report retains historical criteria, accounting, C220107 exclusions and all quantity rows, while overlaying current input roles and 67 current predicates. Every independent prediction credit remains false, and engineering acceptance remains withheld.

`reference_values_loaded: false` in the execution/export means the evaluator did not load reference observations. It does not mean reference-derived input overrides were absent: those are retained in the raw request, selection and purpose. Reporting records the separate observation-file digest. Receipt hashes provide local tamper evidence, not filesystem immutability or universal read-set assurance.
