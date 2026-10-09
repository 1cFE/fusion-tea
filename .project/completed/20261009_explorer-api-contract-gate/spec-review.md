# Spec Review: Concept Explorer API Contract Gate

**Spec:** `.project/active/explorer-api-contract-gate/spec.md` (as committed in `d65a9f579`)
**Contract:** `claude-pack/commands/_my_spec.md` (not readable from this session; the review uses the generation rules restated in `/_my_spec_review`)
**Review File:** `.project/active/explorer-api-contract-gate/spec-review.md`
**Date:** 2026-10-08

---

## Reality Check

**Sound.** The spec is about the right work item, its Problem section is accurate, and its core requirements point the right way.

What I checked and found true:

- **Frontend unchanged since the pin.** Between the pin `10f7b9b1f` and `origin/main` `f96ad312c`, only `server.py` (the CORS wrapper) and `tests/test_cors.py` changed under `exploration/concept_explorer/`. `static/`, `templates/`, `data/` and `omit_list.yaml` are identical.
- **Endpoints and request bodies.** Every path, method and body field in the endpoint `[HARD]` matches the pinned JS, with one exception (L1-1).
- **The 37 concept IDs are served on `main`.** `data/` holds 40 concept files, and `omit_list.yaml` drops `26`, `27` and `34`. The result is exactly the spec's 37 IDs.
- **Other push workflows.** The only other one is `notify_visualization.yml`. It has a path filter, and its `curl` has no `--fail`.

What I could not check: the website repo (`gh api` needed an approval this non-interactive session can't get) and Railway's docs page (`WebFetch` was likewise blocked). The 37-ID list in `concepts.mjs`, the request origin, and the "Wait for CI" details (2-hour skip, other apps ignored) rest on the spec author's reading. Before relying on those details, design should re-read the source.

---

## Audit

Findings are ranked within each lens by how much they would change design.

### Lens 1 — Faithfulness

**L1-1 · Direct claim:** The endpoint `[HARD]` says the website's frontend calls `GET /api/state`. It doesn't. The pinned JS only POSTs to `/api/state`: `concept_page.js:348` and `comparison.js:133` (`git show 10f7b9b:…`). A `git grep` for `/api/` across pinned `static/` and `templates/` finds no GET of it. The server does have the route (`server.py:1236`), but no website code calls it.
- A contract built from this list would block removing an endpoint the website never calls.
- `exploration/concept_explorer/README.md:717` repeats the claim and needs the same fix.
- The rest of the list is right, and so are both POST bodies. Two cites are off by a line or two (the `/api/state` body is at `concept_page.js:351-355`, and the `comparison.js` body is at `136-141`). That is trivial.

**L1-2 · Direct claim:** The endpoint and body `[HARD]` cites fusion-tea's copy of the JS, but the contract is supposed to follow what the website actually serves. These cannot be byte-identical.
- **Why they must differ.** The pinned JS fetches relative paths like `fetch("/api/state")`. Served from `1cf.energy`, those requests would go to `1cf.energy`, not `concepts.1cf.energy`. So the website's import (`scripts/import-concepts.mjs`) must rewrite the JS or wrap `fetch`.
- **Why it matters.** Suppose that transform adds a request header. The CORS allowlist permits only `Content-Type` (`server.py`, `_ExplorerApp`), so every POST would fail. A transform could also drop calls or change methods. In any of these cases, the contract derived from fusion-tea's copy is wrong.
- **Fix.** Someone with website read access confirms the import only rewrites the API base. Then the `[HARD]` cites the website's served copy or names the transform.

**L1-3 · Question to the user:** The Non-Goal "Changes to the `1cFE/website` repo" carries no provenance, and I can't find an owner source for it. The owner's "don't write to the website repo" covers this session. That is not the same as a scope decision.
- The Non-Goal matters because it rules out the cheapest fix for the spec's biggest open risk: the gate's pin record going stale when the website re-pins (Open Question 1, product-lens spec-F5).
- One line in the website's re-pin checklist would close most of that gap. It would say: "after re-pinning, update fusion-tea's pin record."
- **Is a docs-only line in the website's re-pin checklist in bounds, done by you?** If yes, the Non-Goal should narrow to "no website-side code or CI." If no, it should be marked `[AGENT]` with its reason, so design can challenge it.

**L1-4 · Rewrite request:** Changing hosting FR-6 rests on two different provenance claims.
- **FR-6 is owner-grade.** The hosting spec's FR list is "from the owner's request unless marked [INFERRED]" (`.project/completed/20260821_explorer-web-hosting/spec.md:107`), and FR-6 is unmarked. It promises redeploys "without a hand-authored GitHub Actions workflow".
- **The two claims disagree.** This spec tags the override "agent recommendation, owner approved moving to spec". The product-lens disposition for spec-F4 says it was "owner-ratified via option 3".
- **The authority does exist.** Option 3 ("gate deploys only on…") and the Align intent the owner ratified both say pushes that would break the website don't deploy.
- **Fix.** The spec should cite the ratification that covers blocking (option 3 / Align), not "approved moving to spec". It should also name the clause that changes: "without a hand-authored GitHub Actions workflow." The `railway.toml` header comment cites FR-6 for "no GitHub Actions" and will go stale. That fix belongs in implementation.

### Lens 2 — Problem & Approach

**L2-1 · Direct claim + rewrite request:** Success criterion 1 defines a breaking change by name only: removing or renaming a field. It misses the commonest real break, which is a field that keeps its name but changes type or becomes null.
- **Why it's common.** The pinned JS has about 130 calls like `toFixed`, `map` and `forEach`, spread over 16 render files (`cas_breakdown.js`, `tornado.js`, `view_*.js` and others). A number that becomes a string breaks them, and so does a value that becomes null for one concept after a data regeneration. A presence-only contract passes both.
- **Why it matters for the data requirement.** The spec's `[INFERRED]` requirement to check real served data for every concept pays off mainly when the contract checks types and nulls, because those are what a data regeneration changes per concept.
- **The request side has the same gap.** `comparison.js` sends `current_concept_id: null` and `timestamp: ""`. The server accepts both today (`models.py:605`, `models.py:614`). Making either one stricter, for example a non-null ID or a datetime timestamp, returns 422 to the website. That is not clearly "changing a request-body field."
- **Fix.** Criterion 1 needs to say whether type, null and accepted-value changes count as breaking. I'd say they do.

**L2-2 · If-then tradeoff:** The spec never says whether a false block is acceptable: a deploy held back for removing a field the website doesn't read. That answer picks the contract's derivation.
- **If false blocks are acceptable,** the cheapest complete contract is the API's response schemas at the pin. 9 of the 11 website endpoints have pydantic response models (`server.py:1230-1240`), so FastAPI's OpenAPI output already describes their types. Add a real-data type check for the two untyped endpoints: `/findings` and `/taxonomy/tree`. This is mechanical, type-aware, and needs no JS parsing.
- **If false blocks are not acceptable,** the contract has to be the fields the JS actually reads. Those reads are spread across 16 files, so listing them by hand is real work and easy to get incomplete.
- The spec's Open Question "How the contract is derived" offers only the JS-reading options.
- A related call: `POST /api/state` is fire-and-forget (errors only reach the console), and `/api/parameter_index` is best-effort. Neither breaks the page visibly. "Don't break anything" argues for protecting them anyway, but that is the owner's call.

**L2-3 · Direct claim:** "The contract follows the website's pinned frontend" is the right bet, and I re-derived it. It survives because the opposite (follow current `static/js`) fails in exactly the case this item exists for. But the Open Question on how the gate learns the pin frames the private-repo problem as harder than it is. Two routes are missing:
- **The pin is a fusion-tea commit.** The pinned JS and the served concept set at that commit both live in fusion-tea's own git history. The only thing fusion-tea lacks is one SHA, not a copy of the contract.
  - Caveat: the ID set at the pin equals the website's list only if the website import enforces it, which README §9 says it does.
  - Caveat: CI checkouts are shallow by default.
- **The website's served frontend is public.** The repo is private, but `1cf.energy/tools/concepts/` is public. A scheduled, non-blocking check could read the served assets and flag drift with no token.
  - Unverified: whether the website bundles or minifies them, and whether the pin is visible in the served files.
  - This check must not block deploys, or `1cf.energy` uptime would hold back fusion-tea deploys.
- **Fix.** Add these to the Open Question's option set. With them, a hand-kept pin record plus visible drift becomes a cheap route, not a gap to accept.

### Lens 3 — Pipeline Risk

**L3-1 · Rewrite request:** Three success criteria can only be met or observed through owner-only steps (push, the Railway toggle, the Railway dashboard). Each should split into an agent-verifiable part and an owner acceptance step.
- **Criterion 1** ("fails a GitHub check… shown on a scratch branch") needs two things. It needs a push, which is reserved for the owner. It also needs a workflow that runs on branches other than `main`.
  - Agent part: show each deliberate break failing the exact command the workflow runs. Keep the breaks as permanent self-tests, so the evidence survives the next re-pin.
  - Owner part (optional): confirm one break on a pushed branch.
- **Criterion 3** ("Railway is seen waiting") is the product-lens fix for spec-F1, and that fix is right. But it is entirely an owner observation.
  - Agent part: the workflow is a GitHub Actions `on: push` workflow covering `main`, with no path or branch filter that could skip a run, and it is green on the branch head.
  - Owner part, after merge: Railway shows the deploy waiting, then deploying.
  - Also say plainly that the failure path on `main` is never observed, since nobody should push a break to production. It rests on Railway's docs.
- **Criterion 4** ("green on the day 'Wait for CI' is turned on") is an ordering instruction for the owner, not an outcome. Rewrite it as an outcome: turning the setting on doesn't hold back the first deploy. The agent part is a green gate on the merge commit.

**L3-2 · If-then tradeoff:** No criterion bounds the gate's run time. Today a passing push deploys within the Docker build time. Under "Wait for CI", every deploy also waits for the gate. A real-data contract over 37 concepts with `/api/compute` could add several minutes (the existing suite takes about 6). **If** you care how quickly a data edit reaches the site, add a rough bound to the criteria. **If** a few added minutes are fine, say so, and design can choose depth freely.

### Lens 4 — Hygiene

No material findings.

### Lens 5 — Reader Comprehension

No material findings. The spec reads in one pass.

### Product-lens dispositions

No disposition is wrong. Three are extended above, not re-raised:

- **spec-F3** was accepted for field names. L2-1 extends it to types and null values.
- **spec-F1** was accepted. L3-1 splits the resulting criterion by who can observe it.
- **spec-F5** was deferred. L2-3 adds the two missing routes to its option set.

---

## Engagement Summary

**Overall take:** This is the right item with the right core bet. Three things are wrong in the spec: its definition of "breaks the website" is too narrow (types and nulls), it is silent on how strict the gate should be (false blocks), and one `[HARD]` claim is false. Its criteria also mix agent work with owner-only observations, so no one can tell when the agent's part is done.

**Here's what I need you to weigh in on:**

1. **[L2-1]** Should a field changing type, or turning null for some concept, count as breaking the website? I recommend yes. It is the likeliest break after a data regeneration, and the current criterion misses it.
2. **[L2-2]** Is it acceptable for the gate to hold back a deploy that removes a field the website doesn't read? If yes, design can use the API's schemas at the pin, which is cheap and complete. If no, design has to list fields the JS reads across 16 files.
3. **[L1-3, L2-3]** Is a one-line note in the website's re-pin checklist ("update fusion-tea's pin record") in bounds, done by you? It is the cheapest fix for a stale pin record. Either way, design should weigh the two no-token routes in L2-3.
4. **[L3-1]** Accept splitting criteria 1, 3 and 4 into agent-verifiable parts and owner acceptance steps after merge.
5. **[L1-1, L1-2]** Fix the false `GET /api/state` claim (here and in README §9). Confirm the website import only rewrites the API base, so the endpoint list holds for the website's served copy.
6. **[L3-2]** Is there a limit on how much the gate may delay deploys?

---

## Resolutions

Recorded 2026-10-08 by the orchestrator, under the owner's go-ahead for the run ("looks good, proceed"). These are agent-grade decisions, not owner answers. The owner reserved only the gates in `briefs/00_align.md`; none of these findings touches one. The orchestrator held the spec's authoring context and applied the edits directly.

- **L1-1 · Accepted.** Verified: the pinned JS only POSTs to `/api/state` (`concept_page.js:348`, `comparison.js:133`). Fixed in the spec's endpoint `[HARD]` and in `exploration/concept_explorer/README.md` §9.
- **L1-2 · Resolved by check.** Website `src/data/concepts.mjs` (`conceptsScriptAdaptations`) rewrites `"/api/` and `` `/api/ `` to `https://concepts.1cf.energy/api/` and `` `/static/images/ `` to the same origin, and otherwise retargets links, DOM mount points and colours. No header, method or call changes. Added as a `[HARD]` with that cite. The image rewrite surfaced a latent dependency: concept illustrations load from the live server. All 40 `illustration` fields are null today, so it is an Open Question line, not a requirement.
- **L1-3 · Non-Goal re-graded `[INFERRED]`.** This run has no write access to the website repo. The one-line re-pin checklist note is a recommended owner follow-up, recorded in the Non-Goal.
- **L1-4 · Accepted.** The blocking requirement now cites option "3" and the Align intent, names the FR-6 clause it changes, and flags the `railway.toml` header comment for update during implementation.
- **L2-1 · Accepted.** Type changes, null where a value is expected, and rejecting a value the frontend sends today all count as breaking. Criterion 1 rewritten.
- **L2-2 · Decided: false blocks are acceptable; missed breaks are not.** Reason: the owner's "so we don't break anything". Guardrail: clearing a false block takes a deliberate record of what changed and why the website doesn't need it, not a wholesale snapshot regeneration, so the gate doesn't train people to regenerate it reflexively. `POST /api/state` and `/api/parameter_index` are protected too. Derivation stays with design, which must show completeness against the pinned JS.
- **L2-3 · Accepted.** Both no-token routes added to the pin Open Question. A token remains an owner-reserved gate.
- **L3-1 · Accepted.** Criteria split into "verifiable on this branch" and "owner acceptance after merge". Deliberate breaks become kept self-tests. The unobserved failure path on `main` is stated plainly.
- **L3-2 · Decided: under 5 minutes.** The gate workflow finishes in under 5 minutes on a GitHub-hosted runner. Added as a criterion.

No second review round: L1-1, L1-2 and L1-4 are objectively checked edits, and the rest apply decisions the review framed. Design review will test the result.

---

**Verdict:** Revise

**Next Steps:** Record resolutions above, then re-run `/_my_spec` (or return to the spec-agent session) pointed at this review. The reviewer does not edit the spec. L1-1 and L1-4 are objectively checkable edits and don't need a re-review. L2-1, L2-2 and L1-3 change the contract the design builds against, so the owner should answer them before `/_my_design`.
