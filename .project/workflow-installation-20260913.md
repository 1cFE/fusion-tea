# Modeling workflow installation

**Installed:** 2026-09-13. **Target:** `/home/reid/1cfe/fusion-tea-codex-test`.

[OWNER] Requested installation of the repaired and trialed workflow into this worktree. [AGENT] Adapted the revised legacy command sources from `/home/reid/1cfe/agentic-mbse` into the existing native skill envelopes, retaining native adapter loading, explicit supporting-skill references, and host tool names. This is a local instruction update; neither toolkit source checkout was modified during installation.

## Installed assets

- Eleven workflow skills: spec, design, plan, implement, review, audit, quick, orchestrate, research, backlog, and status.
- Four supporting skills: model-validation, project-structure, requirements-tracking, and toolkit-awareness.
- The modeling process, modeling guide, and epic guide.
- Fourteen pattern documents under `.agentic-mbse/patterns/`. Use these copies for the patterns named by the guide and skills; the pinned runtime may contain older documentation.
- The Codex adapter and its embedded copies in five expert roles. They retain author continuity and require fresh non-author contexts for independent criticism. Expert role bodies, names, descriptions, documentation locations, and sandbox settings are preserved.

The native ownership-aware installer wrote 38 payloads and updated `.agentic-mbse/install.json`. No managed-file conflicts were found. All previous affected files and the original manifest are backed up under `.codex-test/workflow-update-20260913/before/`. The three previously untracked guides also have sibling `.backup` copies created by the installer.

## Verification

Native Codex app-server `skills/list` with forced reload discovers all 30 repository skills without errors, including the 15 updated skills and five local aliases. All 38 installed payload hashes match both the prepared bundle and the managed manifest. All seven required technical reference names resolve locally. Expert-role metadata and permissions are unchanged.

Hash checks confirm 3,535 protected files unchanged, including existing project records, source registries, study code/data, local goal/study skill bundles, dependency pins, launcher, and Codex configuration. The five local skill aliases remain unchanged. `PYTHONDONTWRITEBYTECODE=1 .codex-test/run python -m pytest -p no:cacheprovider tests/test_dependency_provenance.py -q` passed all three tests.

Evidence: `.codex-test/workflow-update-20260913/verification.json`, `plan.json` (source origins and before/after hashes), `actions.json`, `payload/`, and `before/`. Preparation and application scripts are retained there. The source workflow is committed in agentic-mbse as `d20069b` (Simplify modeling workflows around outcomes and focused evidence). Native adapter/envelope and local-reference adaptations are specific to this installation; the payload hashes identify the installed bytes.

## Use and limits

Start a fresh Codex session in this worktree so ongoing agents do not retain previously loaded instructions. The native skill catalog remains `.agents/skills/`; the adapter explains that slash-style references in shared prose mean the corresponding Codex skills. Use `.codex-test/run` for Python/toolkit commands. Local goal/study procedures and reserved owner decisions continue to apply.

This update keeps the earlier setup's separation between instruction assets and the pinned executable runtime. No dependency synchronization, runtime package replacement, model regeneration, goal/study execution, or trust/configuration change occurred during installation. The owner subsequently requested committing the instruction assets. The previously reproduced L6 EXPOSE-validator issue is not repaired by this instruction installation.

The native source branch and original extracted wheel still contain their earlier workflow text. Reinstalling that older pack can replace these managed payloads; retain this bundle when reproducing this installation. Subsequent general distribution should port these revisions into the maintained native source before rebuilding its pack.

The earlier [setup record](codex-test-setup.md) remains authoritative for runtime setup. The [repair/trial report](/home/reid/1cfe/fusion-tea/.project/reports/20260912-workflow-repairs-and-trials.md) describes the evidence behind this revision; installation verification does not rerun those behavioral trials.
