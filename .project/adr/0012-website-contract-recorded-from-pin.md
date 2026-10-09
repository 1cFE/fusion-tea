---
id: 0012
title: The website contract is recorded from the pinned commit
date: 2026-10-08
owner: Reid W
status: active
amended_by: []
superseded_by: null
provenance: "[AGENT] (orchestrator, 2026-10-08)"
seams: ["1cFE/website pinned explorer frontend", "exploration/concept_explorer API"]
supersedes: null
promoted_to: null
---

## Decision

The deploy gate's contract, `exploration/concept_explorer/website_contract/contract.txt`, is a recording. `gate.sh record <sha>` runs the pinned commit's own server from a `git archive` extract of that commit, makes every request the pinned frontend makes, and writes down the JSON kinds at every response path and the concepts in every list the frontend joins or links. On each push the gate makes the same kinds of requests against the checkout and fails on any change the pinned frontend could break on. A false block clears only through a hand-written entry in `waivers.toml`, with a reason, evidence and a date. Failures of the CORS rule and the Files rule are fixed, never waived. The pin lives only in `contract.txt`'s header, and a daily drift job compares it with the pin the public website links.

## Why

The website's frozen frontend can only depend on what the pinned server sent it, so a recording at the pin is complete for every path the pinned data populated, without anyone listing fields by hand. A path the pin never populated fails closed the first time it carries data (the Unpopulated rule), until someone checks the pinned JavaScript and waives it.

Recording is a pure function of the pin: the extract holds only the pinned commit, it installs the pin's own serving set, and the test tools resolve with `--exclude-newer` at the pin's commit time. So re-recording can't clear a block. Only a waiver can, and a waiver is a deliberate, reviewable record of what changed and why the website doesn't need it (`spec-review.md` L2-2). The recording reproduced byte for byte at `10f7b9b1f1466d2057a211bf25f09fc35d80a12b` on this branch.

The price is false blocks on fields nothing reads. Replaying history from 2026-04-01 measured 5 false-block pairs out of 23 replayable pairs that don't add a concept (22%) on the design's count, or 5 of 27 (19%) counting four findings-only replays. No pair needed more than 2 waiver lines, no trip came from a misclassified map or record, and the newest false block is `84422dd08` (2026-06-15). The orchestrator accepted that direction because missing a real break is worse than a false block; whether to soften the Shape and Unpopulated rules is parked with the owner (`.project/active/explorer-api-contract-gate/plan.md`, Phase 1 Results and the orchestrator note on the Phase 2 correction; `phase1/report.md`).

## Invariants established

- `contract.txt` is never edited by hand. It changes only by `gate.sh record <sha>`, at a website re-pin.
- Recording refuses when a `fetch(` site in the pinned `static/js/` or `templates/` is uncited, or when a cited JavaScript file's blob differs from the previous header, until a developer re-verifies the request list and passes `--js-reverified`.
- Every waiver has `match`, `reason`, `evidence` and `date`. An `unpopulated` waiver's evidence cites the pinned JavaScript that reads the path (`file.js:N`), or says `unread:` and the search terms that found no reader (orchestrator, 2026-10-08).
- The gate fails, unwaivably, when the server touches a tracked file the checkout lacks or `.dockerignore` keeps out of Railway's image.
- Design: `.project/active/explorer-api-contract-gate/design.md`, decisions D1, D2 and D7 to D9 and invariants I1 to I3 and I6.

## Rejected alternatives

- A hand-written list of the fields the pinned JavaScript reads: not chosen, because only an audit could show it complete.
- A diff of the API's OpenAPI schema: not chosen, because it is blind to nulls in real data and to the untyped endpoints.
- Regenerating the snapshot, or a CI job that re-records it, to clear a block: not chosen, because it would clear real breaks as easily as false ones.
- Recording each concept's responses separately: not chosen, because it is about 45,000 lines and blocks content changes both sites share.
- Reading the website's pin from its private repo with a token: not chosen; a cross-repo secret is reserved for the owner.
