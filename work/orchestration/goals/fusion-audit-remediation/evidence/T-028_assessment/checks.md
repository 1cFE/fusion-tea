# T-028 document checks

[AGENT] `.codex-test/run python -m pytest tests/study/test_records.py -q -k 'findings_join or joined_disposition' -o cache_dir=/tmp/t028-pytest-cache` passed 14 checks and deselected 26 unrelated checks. Output retained in `record-joins.log`. This suite reads records/logs; it does not execute models or open historical SQLite stores.

A direct `.codex-test/run python` read-only check extracted the main report table’s first-column F IDs and asserted exact ordered equality to F01–F20. It extracted each IFE record’s first-column finding IDs and compared them with its discovery log’s Record column under the same study prefix. Both study joins matched. Console result: `PASS: F01-F20 appear once each in summary; both IFE record/log joins match.`

`git diff --check` passed. No broad model/consumer batteries were repeated and no certificate is upgraded by these document checks. The known unrelated historical narrative-reference failure was excluded by selecting only the changed discovery-log contract.
