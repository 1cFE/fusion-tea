# Stage brief: spike — regeneration determinism (GSTH Item 3 de-risk)

**From**: orchestrator (`/_my_orchestrate`), 2026-08-26. Throwaway-code spike; keep only the finding.

## The assumption to confirm or refute

`.project/active/goal-integration-seam/spec.md` R-D4: the seam's re-run contract assumes the pinned `sysml-codegen generate --smart-regen --preserve-handwritten`, run a second time **in place on an already-sealed package**, leaves the tree git-clean and both fingerprints (semantic, executable) unmoved. WI-030 checked the nearest thing — generate twice against a *scratch target* and `diff -r` (`work/completed/20260822_WI-030_computed-beta-peak-field/plan.md:158`, result `:291`) — but never a re-run in place onto its own output.

## Why it matters

If in-place regeneration is byte-stable, the seam can re-run the full gate sequence idempotently (R-B4, no gate skipped). If not, R-B4 needs a stated exemption for regeneration and the design changes shape. Design is blocked on this answer.

## How to run it

- Work in scratch: copy the sealed stellarator package tree (`models/` + whatever the generate target needs — see `.project/completed/20260821_stellarator-model-migration/plan.md` Phase 2/3 for the exact command and target, and `work/completed/20260822_WI-030_computed-beta-peak-field/plan.md:151` for the WI-030 invocation) into a scratch git clone or worktree so the real repo is never dirtied.
- Use the **pinned** codegen as installed (never a local checkout). Env gotchas: `set -a; source ~/1cfe/agentic-mbse/.env; set +a` for `SYSIDE_LICENSE_KEY`; teax via `STOP_PARSER_TEAX_ROOT`; see `tests/study/conftest.py:230` and project memory.
- Sequence: confirm the copied tree is sealed/clean → run generate in place → record `git status --porcelain`, semantic + executable fingerprints (see `scripts/study/identity.py` for how they're derived) → run generate again in place → compare tree cleanliness and both fingerprints.
- If the first in-place regenerate already moves the tree, that itself is the finding — characterize what moved (timestamps? ordering? content?) before concluding.

## Return

Report: CONFIRMED (byte-stable in place, evidence) or REFUTED (what moves, at what step, with the diff character), plus any operational surprises a design should know (runtime, env preconditions). Write the finding to `.project/active/goal-integration-seam/spike_regen_determinism.md` and end with `ARTIFACT: <that path>`. Leave no changes in the real repo.
