# Brief: plan for "Quality Tools and Era Adapter Promotion" (RUN-STUDY Item 4)

Work item home: `.project/active/run-study-quality-tools/` — spec.md and design.md rev 2 are
ACCEPTED (design carries all review fixes L1-L6 + S1-S5 + notes; its Review disposition and
Next-Stage Handoff say exactly what is fixed). Write plan.md: phased execution, checkboxes,
per-phase validation and commits.

Planning constraints:
- Honor the design's de-risk order: `test_operand_bindings.py` (L1/D12 — the one belief that
  broke under review) is de-risk 1 and comes before verify.py is built on it.
- The probes (`probe_effective_fingerprint.py`) already proved the identity/lineage mechanics;
  the plan turns them into committed tests, not re-derivations.
- Item 3 is DELIVERED and green (134 tests). Its manifest.json oracle-block VALUES change in
  this item once oracle_entry.py exists (design Coordination ask 1 to Item 3, applied by this
  item as a data-only edit, explicitly authorized by the orchestrator). Plan that as its own
  step with the manifest digest consequence noted.
- Promotion equivalence: the 19-point availability sweep in the default suite, the 948-point
  grid behind `-m slow` (D11) — plan both runs and the byte-compare against the committed CSVs.
- The era worktree (/home/reid/1cfe/teax-v1-era @ fa0e06a) is a read-only dependency; the plan
  must state how tests locate it and what happens when it is absent (skip with a loud reason,
  or fail? follow the design if it says; otherwise decide and record).
- Every phase: `uv run python -m pytest tests/study -q` green (the WHOLE study suite — Item 3's
  134 must stay green) before ticking. Never run the full repo pytest suite — a pre-existing
  side-effecting test (tests/scoring_v2/test_score_explorer_build.py) regenerates live data
  files; scope all pytest invocations to tests/study.
- Note what each phase commits.
