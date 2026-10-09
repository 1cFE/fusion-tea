The re-audit certified the item (Round 2 in `audit.md`). Fix its three small advisories, then stop:

- **R2-1:** check must not crash when a new unwritable key appears on only some objects at a path (`json_shapes.py:39-43`). Add a self-test using the case the auditor reproduced (one of several tree child nodes carries a key with a space), and confirm the test goes red without the fix.
- **R2-3:** README §9 and the RUNBOOK call a renamed `POST /api/state` field a real break. It is a false block (neither site reads state back), cleared by a waiver. Correct both, in one sentence each.
- **R2-4:** add a self-test for the optional-request-body branch in `_properties`, and confirm it goes red when that branch is removed.

Also name R2-2 in the design's Non-Goals as a residual, in one line: a server that keeps declaring a field but stops reading it passes, because catching it needs value comparison.

Same rules as before: never write under `/home/reid/1cfe/fusion-tea`; never push, open a PR, or change remotes or upstreams; stage by name; the commit message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. One commit. At the end, `gate.sh` is green and `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` reproduces `contract.txt` byte for byte. Add one line to the plan's "Audit fixes" notes.

Final message: one line per item with its verification, and the gate's totals. Finish with `ARTIFACT: .project/active/explorer-api-contract-gate/plan.md`.
