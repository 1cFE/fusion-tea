Implement **Phases 6 and 7** of `.project/active/explorer-api-contract-gate/plan.md`. Phases 1–5 and the module split are committed. Read the plan's Working Rules, Plan-Level Decisions and all Implementation Notes (including the orchestrator notes on the false-block rate), then the `design.md` sections the plan links, especially Integration Strategy and Appendix E.

## Phase 6 (docs and ADRs): points to get right

- **Audience.** The RUNBOOK "Deploy gate" section is for a person who will never read the gate's code: the owner, or an engineer on the day a deploy didn't happen. Write it per `~/.claude/rules/working-voice.md` (lead with the point, plain words, one idea per sentence, numbered steps). Every procedure the spec names must be followable from the RUNBOOK alone: a skipped deploy and how to get one out, clearing a false block with a waiver, a new concept (both paths and their costs; the Phase 3 notes found the waive path usually needs Shape waivers too, for fields a new concept leaves null), the re-pin step, a red drift run, the emergency bypass, and turning "Wait for CI" on and off.
- **Owner steps** are written as steps for the owner, never performed: "Wait for CI", branch protection, and the optional scratch-branch check. No secrets are needed; say so.
- **ADRs** via `.project/scripts/adr.sh new`. ADR (a) splits its grade: "pushes that would break the website don't deploy" is `[AGENT] (ratified by owner, 2026-10-08: option "3" and the Align intent)`; false blocks, new-concept blocks and infrastructure holds are orchestrator-grade. It names both FR-6 clauses it changes. ADR (b) is agent-grade. Both state the measured false-block rate honestly (5 of 23 on the design's count, 5 of 27 combined, newest 2026-06-15).
- **`CLAUDE.md`** gets the line from the design (any failing push-triggered workflow skips the production deploy) and loses "No CI runs first". Keep the section short; it is a pointer to the RUNBOOK and README §9, not a second copy.
- **`railway.toml`** header cites the gate and ADR (a) instead of FR-6's "no GitHub Actions". It stays valid TOML.
- Markdown: one line per paragraph, never hard-wrapped.

## Phase 7

As planned: run `gate.sh` from a fresh shallow, sparse, blobless clone of this branch the way CI does, time each step, and fill the spec-criteria evidence table. Leave the owner-acceptance list unchecked. Mark the spec's branch-verifiable criteria only where the evidence is in hand, and cite it.

## Rules for this session

- Worktree `/home/reid/1cfe/fusion-tea-explorer-api-gate`, branch `feat/explorer-api-contract-gate`. Never write under `/home/reid/1cfe/fusion-tea`.
- Never push, never open a PR, never change remotes or upstreams. Stage files by name; each commit message ends with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.
- No Docker. `uv` scratch venvs in temp directories, cleaned up.
- Don't change the explorer's API, data or frontend.

## Stop

Stop after Phase 7 is committed. Final message: what Phase 6 changed (one line per file), the Phase 7 timing table and its projection, the spec-criteria table's verdicts, the owner-acceptance list as written, and any deviation. Finish with `ARTIFACT: .project/active/explorer-api-contract-gate/plan.md`.
