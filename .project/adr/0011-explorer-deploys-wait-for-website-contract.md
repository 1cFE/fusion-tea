---
id: 0011
title: Explorer deploys wait for the website-contract workflow
date: 2026-10-08
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[AGENT] (ratified by owner, 2026-10-08: option \"3\" and the Align intent) that pushes which would break the website don't deploy; [AGENT] (orchestrator, 2026-10-08) the holds on false blocks, new concepts and CI infrastructure failures"
seams: ["Railway deploy of concepts.1cf.energy", "1cFE/website pinned explorer frontend", ".github/workflows push triggers"]
supersedes: null
promoted_to: null
---

## Decision

Railway's deploy of `concepts.1cf.energy` waits for the push-triggered GitHub Actions workflows ("Wait for CI", an owner-only dashboard setting on service `1cfe-fusion-tea-explorer`), and skips the deploy when one fails. The `website-contract` workflow (`.github/workflows/website-contract.yml`, running `exploration/concept_explorer/website_contract/gate.sh`) is the only push workflow that may fail, and it fails when a push would break the website's pinned copy of the explorer frontend. This changes two clauses of hosting FR-6 (`.project/completed/20260821_explorer-web-hosting/spec.md:114`): "without a hand-authored GitHub Actions workflow" no longer holds, and "with no manual deploy step" now holds only for pushes the gate passes.

## Why

The decision has two grades, and each part is challenged differently.

**Owner-ratified: pushes that would break the website don't deploy.** `[AGENT] (ratified by owner, 2026-10-08: option "3" and the Align intent)`. The owner asked for the website dependency to be protected ("...so we don't break anything", then "what would tests look like to protect the API?", 2026-10-08). The agent recommended blocking the deploy, not only reporting a failure; the owner selected option "3", which gates deploys, and approved the Align intent "pushes that would break the website don't deploy" (`.project/active/explorer-api-contract-gate/briefs/00_align.md`, spec Known Requirements). A report-only check would leave the website broken until someone read it. Only the website-contract tests and `test_cors.py` gate deploys; the red explorer suite joins after its own repair (spec, option "3").

**Orchestrator-grade: three kinds of push that wouldn't break the website still wait for someone.** `[AGENT] (orchestrator, 2026-10-08)`, surfaced to the owner the same day (`spec-review.md` L2-2, `design-review.md` M7).
- A false block: the gate fails on a change the pinned frontend doesn't depend on. One waiver line in `waivers.toml` clears it. Replaying history from 2026-04-01 measured 5 false-block pairs out of 23 replayable pairs that don't add a concept (22%) on the design's count, or 5 of 27 (19%) counting four findings-only replays. No pair needed more than 2 waiver lines, and the newest false block is `84422dd08` (2026-06-15). All five were removals or new nulls on fields the pinned JavaScript never reads. The 22% misses the orchestrator's own 20% line by one pair; the orchestrator continued without softening the rules, and whether to soften the Shape and Unpopulated rules is parked with the owner (`plan.md`, Phase 1 Results and the orchestrator note on the Phase 2 correction).
- A new concept the website doesn't list: it would be a dead link on the website. It clears by adding it to `omit_list.yaml` until the website re-pins, which hides it on `concepts.1cf.energy` too, or by a waiver, which accepts the dead link.
- A CI infrastructure failure (an install that fails three times, a timeout): a new push clears it.

The orchestrator judged these acceptable because missing a real break is worse than a held deploy (`spec-review.md` L2-2), and each hold clears with a deliberate, recorded act rather than by regenerating the contract.

## Invariants established

- Only `website-contract.yml` and `notify_visualization.yml` run on push, and `notify_visualization.yml` can't fail (its `curl` ends in `|| echo "::warning::…"`). The self-test `test_push_workflows_equal_the_reviewed_list` in `exploration/concept_explorer/tests/test_website_contract.py` fails the gate when a push workflow is added; a new one must be unable to fail before it joins the reviewed list.
- The gate workflow has no path, branch or tag filter and no concurrency cancel, because Railway never blocks on a skipped or cancelled run. `gate.sh` runs under `timeout 480`, so a hang ends as a failure.
- A held deploy is recovered by a new push or an owner redeploy in Railway. Re-running a failed gate isn't relied on until the owner has seen what Railway does with it.
- Turning "Wait for CI" off is the emergency bypass, and it is owner-only. The steps are in `.project/completed/20260821_explorer-web-hosting/RUNBOOK.md`, section "Deploy gate".

## Rejected alternatives

- Report the gate's failure without blocking the deploy: not chosen, because the website would stay broken until someone noticed (owner option "3").
- Gate deploys on the whole explorer test suite: not chosen, because it is red (32 failed, 306 passed on 2026-10-08) and none of its tests checks what the website's pinned frontend reads (owner option "3").
