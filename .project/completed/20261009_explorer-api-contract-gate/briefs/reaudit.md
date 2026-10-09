Focused re-audit of work item `explorer-api-contract-gate`, round 2 of 2. Round 1 is in `.project/active/explorer-api-contract-gate/audit.md` (verdict Needs Work, blocker B1, advisories A1–A9). The fixes are commits `ab252b1f6..0d92ae7a2`; the plan's Implementation Notes have an "Audit fixes" entry. Append a "## Round 2" section to `audit.md`; don't rewrite round 1. Update the tracking checkboxes as your command says. Don't commit.

## Where you are

- Git worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`. Never write under `/home/reid/1cfe/fusion-tea`. Never push, open a PR, or change remotes or upstreams.
- No Docker. Run `exploration/concept_explorer/website_contract/gate.sh`, which builds its own `uv` venv in a temp directory.
- Skip the product-lens pass; it ran in round 1 and its findings are A5 and A6.

## Scope

1. **B1.** Re-do your own round-1 breaks (rename `apply_analyst_overrides`, separately `overrides`, each with a default) in a scratch clone, and confirm each fails. Then try to get around the new rule: rename a field of the state body; switch a request model to accept arbitrary extra fields; move a field into a nested model. For each, say whether the website breaks and whether the gate fails. Check the design amendment says what the code does.
2. **A1–A8.** One line each: fixed and verified, or not. Mutation-check the new tests for A1–A3 yourself on a sample.
3. **Regressions.** `gate.sh` is green on HEAD. `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` reproduces `contract.txt` byte for byte. The scope check against `f96ad312c` still shows no change to the explorer's API, data or frontend. Look over the fix diffs for new dead code or duplication.
4. **Certification.** If B1 holds, check spec criterion 1 and any other branch-verifiable criteria with evidence. Leave owner-acceptance items unchecked.

Finish with a verdict (Certified, or Needs Work with a must-fix list), then `ARTIFACT: .project/active/explorer-api-contract-gate/audit.md`.
