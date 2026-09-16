# Coordinator validation

[AGENT] 2026-09-16. Frozen study at a16e7256: package untouched; record and custody snapshots retained. Three study record checks pass (`.codex-test/run python -m pytest tests/study/test_records.py -k 20260916-bounded-feasibility-transfer -q`). `evidence/check_transfer.py` passes 3 anchors, 6 one-input contrasts, 3 transverse changes and 4 loop changes from retained native outputs. Study worker's all-point/generic/store checks are executor checks, not independent review.

[AGENT] Post-freeze executor synthesis explicitly records H1's failed 5–95% feasible-fraction expectation and the absence of a separately measured baseline wall-clock receipt. Native runtime is 88.029 seconds for 71 cases. No scientific output, coordinate or verdict changed. Local evidence commit includes all 234 required files, including native stores and content-addressed evidence that required force-staging because of ordinary ignore rules. Unrelated user files were not staged.

[AGENT] Four additional template/orchestration contract checks pass (`.codex-test/run python -m pytest tests/study/test_record_template.py tests/orchestration/test_goal_contract.py -q`). Seven relevant record/contract checks pass in total. No production model or test implementation changed, so no broad model-regression rerun was required.

[AGENT] Round 2 correction re-ran the three current-study record checks after the append-only native record erratum; all pass. No model, native case or oracle calculation reran. The correction changes coverage classification and prose, not the frozen 228 artifact entries. Final independent numerical coverage remains reusable subject to the reviewer checking the exact nine-point exception and corrected scope.
