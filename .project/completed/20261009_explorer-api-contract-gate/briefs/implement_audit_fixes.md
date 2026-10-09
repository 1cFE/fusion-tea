Fix the audit findings for work item `explorer-api-contract-gate`. Read `.project/active/explorer-api-contract-gate/audit.md` in full, then the plan's Working Rules and the Implementation Notes. The orchestrator's decisions for each finding are below; they are agent-grade (orchestrator, 2026-10-08).

## B1 (blocker): a design amendment, then the rule

**Amendment.** Add a **Request fields** rule. For each POST template in the request list, every top-level field name the pinned frontend sends must be a declared property of the current server's request-body schema for that route. Read that schema from the in-process app's own `/openapi.json`, resolving `$ref`. Nested data-keyed maps such as `overrides` aren't checked by key. A missing field fails with key `request-field <template> <field>`. It is waivable, because a field the server sets itself (for example `timestamp`) can be dropped harmlessly. The design's "Check reads no schema" becomes "Check reads no response schema; the Request fields rule reads the current server's request schemas." The request list is already cited code tied to the pin by the JS blob check, so `contract.txt` doesn't change and recording at the pin must stay byte-identical.

Apply the amendment to `design.md`: the rules table, the line quoted above, Appendix D and Appendix E. Add one line in the design's header or Related Artifacts saying it was amended after audit B1. Then implement test-first. Self-tests must rename each sent field of both POST bodies (`POST /api/compute` and `POST /api/state`) to a new optional name and show the rule fails. A new optional request field still passes.

## Advisories

- **A1:** add self-tests that fail when the Status rule's "no 200 at all" clause or the CORS preflight-status clause is removed. Prove it by mutating each clause and watching the test go red, then restore.
- **A2:** in check mode, a response key that can't be written as a path segment is new by construction, since the contract can't hold it. Treat it as additive: skip it and its subtree, with no crash. Record mode keeps failing loudly. Add a self-test.
- **A3:** reject a waiver whose `match` can only match `cors` or `files` keys at load time, with a clear error. Print the "clear it with a waiver" hint only when a waivable failure exists.
- **A4:** move the Phase-1-only `skip` option and timings out of the shipped modules into the Phase 1 harness. Confirm the harness's identity checks still run and give zero keys.
- **A5:** add "the owner's ruling on how strict the gate is (false blocks)" to the owner-acceptance lists in `spec.md` and `plan.md`, pointing at ADR 0011.
- **A6:** README §9 and `CLAUDE.md` say the gate holds deploys only after the owner turns on "Wait for CI". Until then a red gate is a warning only.
- **A7:** the RUNBOOK's bring-back sequence says to merge that branch with a merge commit, not a squash or rebase, so the commit the website pinned stays on `main`'s history. Say why in one clause.
- **A8:** one source for the test-tool list.
- **A9:** leave it for `/_my_close`. Don't create a `.project/product/` entry.

## Rules

- Worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`. Never write under `/home/reid/1cfe/fusion-tea`. Never push, never open a PR, never change remotes or upstreams.
- Commit in logical pieces (the B1 amendment plus rule in one; advisories grouped sensibly), staging files by name. Each message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- Hold the bar on code quality, as before. No behavior change beyond what each finding requires.
- At the end, `gate.sh` is green on HEAD, and `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` reproduces `contract.txt` byte for byte.
- Add a short "Audit fixes" entry to the plan's Implementation Notes. Don't re-check spec criterion 1; the re-audit does that.

Final message: one line per finding saying what changed and how it was verified, plus gate timings. Finish with `ARTIFACT: .project/active/explorer-api-contract-gate/plan.md`.
