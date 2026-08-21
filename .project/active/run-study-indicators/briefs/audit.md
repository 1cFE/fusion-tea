# Brief: audit "Indicator Tool and Package Manifest" (RUN-STUDY Item 3)

Audit the completed implementation against `.project/active/run-study-indicators/`
(spec.md, design.md, plan.md phase notes). Deliverables: scripts/study/indicators.py,
scripts/study/manifest.py, scripts/study/schemas/*.v1.schema.json (three),
exploration/stellarator_e2e/studies/manifest.json, tests/study/ (ten+ files).

Context: the implement session hit its wall-clock timeout AFTER its final commit — all 7
phases committed but no wrap-up message exists. The orchestrator then applied three
coordination fixes for Item 4 (tool_source_digest files list + schema, test_generic
subset assertions) — commit "RUN-STUDY Item 3: coordination fixes". Treat those as part
of the delivered state.

Standard audit: plan-vs-reality gaps, TODO/placeholder code, unticked-but-claimed work,
spec requirements with no implementation, invariant violations. Run the suite yourself
(`uv run python -m pytest tests/study -q`). Check specifically:
1. All 12 design invariants have enforcing tests (map them; name any unenforced).
2. Known-answer expectations match the Item 1 fixture contract field-for-field and were
   NOT patched (diff against .project/active/run-study-reachability-spike/findings.md
   and indicators.json).
3. The spec's success criteria list — tick what's verified, name what isn't.
4. Error messages locate faults per spec (spot-check 3 mechanical failure paths by running).
5. The manifest is data-only and its pinned digest matches the live package.
6. plan.md phase notes: every deviation recorded, none silent (the final phase's notes may
   be thin because of the timeout — reconstruct from commits if needed and say so).

Write `.project/active/run-study-indicators/audit.md`, verdict PASS / PASS-WITH-FIXES /
FAIL. Do not edit deliverables.
