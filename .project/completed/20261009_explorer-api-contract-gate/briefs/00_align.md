# Orchestration record: Align

**Date:** 2026-10-08
**Orchestrator:** Claude (Fable session), stage subagents on `claude-opus-5-5` per owner instruction ("use opus 5.5 subagents").
**Entry:** `spec_review`, on the owner's instruction ("/_my_orchestrate the implementation, starting with the spec review"). Single item, not an epic.

## Intent as read

The owner wants `1cf.energy/tools/concepts/` not to break silently when fusion-tea changes. Pushes that pass still deploy exactly as today. Pushes that would break the website don't deploy. The gate stays small and green, and the existing explorer suite repair stays out of scope (BACKLOG row "Concept Explorer test suite is red").

## Reserved gates

`[AGENT]` (ratified by owner 2026-10-08: "looks good, proceed"). These are decisions the orchestrator parks for the owner instead of deciding.

1. **Any cross-repo secret.** fusion-tea is public. Reading the website's private pin from CI would mean storing a token for a private repo in a public repo's Actions secrets. Design takes the no-token route (a fusion-tea-side pin record with visible drift handling) unless the owner says otherwise.
2. **Owner-only settings.** The Railway "Wait for CI" toggle, branch protection on `main`, and creating any secret. The run writes the steps and leaves them to the owner.
3. **Push, PR, `close`, `pre_pr`.**

Everything else is an execution detail the orchestrator decides and records, including whether to write an ADR for the FR-6 change and whether the gate tests the built Docker image.

## Gaps noted at Align

- The scoring-repair session in the main checkout calls the `CLAUDE.md` and README §9 edits "owner edits". They are agent-written and owner-approved. Not this item's to fix.
- `railway.toml` comments still describe a JAX compile cache, but `requirements-serve.in` pins a numpy-only `1costingfe` build. Stale, out of scope, noted only.
- No spec `[HARD]` item looked inherited. Each was checked against code, the website repo or Railway's docs. The 37-ID list and endpoint list are snapshots of today's website pin, and the design has to handle them changing.
