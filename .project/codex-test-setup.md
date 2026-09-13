# Codex test workspace

Prepared 2026-09-10. Instruction assets were subsequently updated on 2026-09-13; see [workflow installation](workflow-installation-20260913.md). The runtime setup below is unchanged.

## Scope and choices

- [NEED] Set up a new fusion-tea worktree, install the migrated pack, and report issues before the owner restarts the session. Source: owner request in the setup conversation; background `/tmp/handoff-20260910-062629.md`.
- [AGENT] Use `/home/reid/1cfe/fusion-tea-codex-test`, branch `test/codex-native-skills`, based on local `feat/demo-maturation` at `a9ec0b76e2a3c6bb05bc27667f22c47c78c93909`.
- [AGENT] Install Codex skills separately from the pinned modeling runtime. Use `install-commands --assistant codex` to preserve existing project records. Keep setup changes uncommitted for inspection.

## Installed identity

The tested wheel is `agentic_mbse-0.1.3-py3-none-any.whl`, SHA256 `544c3a8805cfed8e841221ec3767fb2c451ab1fdda55cb2a8f1faeb729cb1f42`. A copy and its extracted installation are retained under ignored `.codex-test/`; expert documentation paths refer to that installation. This build includes uncommitted audit fixes from the migration source and must not be identified by version or source HEAD alone. The source migration records remain at `/home/reid/1cfe/agentic-mbse-native-skills/.project/active/native-skills/`.

The pack installed 25 bundles, five expert roles, runtime adapters, and a managed-file manifest. Five relative aliases expose the existing local skills: `run-goal`, `run-study`, `narrate-goal`, `concept-research-navigation`, and `browser-inspect`. Their supporting files and native runbooks remain canonical. `AGENTS.md` points to `CLAUDE.md` for project guidance. Ignored modeling guides were copied from the verified wheel.

## Runtime

Use `.codex-test/run python ...` or `.codex-test/run agentic-mbse ...` from this worktree. The launcher sources the existing license and integration environment without copying credentials, selects `/home/reid/1cfe/fusion-tea/.venv`, disables synchronization, and sets the working directory to this test worktree. The installer payload is never added to the modeling runtime's import path. Plain `uv run` without these settings would create or sync another environment.

For the integration seam, the direct sealed-interpreter procedure in `docs/integration_seam_operator_guide.md` § Running from a second checkout or worktree remains available. Runtime dependencies and sealed wheels are shared; study outputs should use paths inside this test worktree. The stellarator package alias resolves locally to `../generated`. No study or goal execution occurred during setup.

## Verification

- The wheel hash matches the handoff.
- Native Codex app-server discovery found 30 repository skills with no errors; evidence: `.codex-test/discovery.json`.
- Native config loading exposed all five expert roles using the existing user configuration. No personal trust settings were changed.
- `.codex-test/run python -m pytest tests/test_dependency_provenance.py -q`: three passed. This checks the retained runtime's immutable identities and sealed wheel provenance.
- The primary fusion-tea checkout remains clean. Its runtime packages and the migration source checkout were not modified.

## Restart and remaining prep

Open a new Codex session in this worktree. Ask it to confirm the 30 project skills, then test one fresh installed `syside-expert` spawn against its bundled documentation. Configuration loading passed; an actual role spawn in this workspace is still untested.

The modeling task and stopping point remain owner choices. Read the native goal runbook and relevant goal records when that task is selected. Before a full run, check its required generated artifacts and source binaries: ignored runtime state was not copied wholesale. Source PDFs/images may require retrieval for source inspection. Full model/study baselines were not rerun. The migration's independent re-review and full modeling execution remain uncertified as recorded in its remediation evidence.
