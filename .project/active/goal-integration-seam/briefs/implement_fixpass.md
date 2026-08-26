The audit is in: POSITIVE (Certify) — read `.project/active/goal-integration-seam/audit.md`. Quality fix pass before close: address all six findings. Bounded scope — findings only, no new surface.

1. **Finding 1 (the real one):** the refusing/could-not-run gate's own row must carry its true status; `not reached` is only for gates after the stop. Fix the return construction, align with D4's vocabulary as designed, add/extend a test that asserts the stopping gate's row index and status (the audit notes the refusal tests currently step over that index), and confirm `docs/integration_seam_operator_guide.md:144` becomes true rather than editing it to match the bug.
2. **Finding 2:** a seam-internal error mid-sequence names the gate it actually died at, not `preconditions` (`scripts/integrate.py:1442`). Test via an induced fault like the auditor's.
3. **Finding 3:** pin the exit-2 path (seam-internal error) with a test.
4. **Finding 4:** state the citation resolution base for `--out-dir` outside the repo in the guide (one sentence), or normalize — your call, record it.
5. **Finding 5:** use or remove the discarded `clean.json` path (`:551` vs `:1428`).
6. **Finding 6:** fix `plan.md:670`'s stale `set -a; source` recipe to the `--env-file` form.
Also the audit's two SC6 blemishes: guide mentions that `candidate.package` is the resolved symlink target; fix or document the lineage-refusal `not reached` print (falls out of finding 1).

One commit, message prefix `impl(goal-integration-seam) audit fix pass:`. Suite green (`tests/study` + regression gate), R-B2 diff still empty. End with `ARTIFACT: .project/active/goal-integration-seam/plan.md`.
