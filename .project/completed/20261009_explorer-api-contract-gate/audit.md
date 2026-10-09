# Audit: Concept Explorer API Contract Gate

**Verdict:** Needs Work
**Audited:** 2026-10-08
**Branch:** `feat/explorer-api-contract-gate` (worktree `../fusion-tea-explorer-api-gate`), since `f96ad312c`
**Commit:** `239f97529`

---

## The Point

The public page `1cf.energy/tools/concepts/` runs a copy of the explorer frontend frozen at fusion-tea `10f7b9b1f1466d2057a211bf25f09fc35d80a12b`. That copy fetches everything from the live API at `concepts.1cf.energy`, and Railway redeploys that API on every push to `main`. fusion-tea changes its own JavaScript in step with the API, but the website keeps the old copy, so a push can break the website while `concepts.1cf.energy` keeps working. Nothing on the fusion-tea side noticed before this item.

The owner asked for this dependency to be guarded (2026-10-08): "...so we don't break anything", then "what would tests look like to protect the API?". The obligation, as ratified: a push that would break the website does not deploy, and every other push deploys as before with no manual step. Three orchestrator-grade exceptions were accepted and surfaced to the owner: false blocks, new concepts the website doesn't list, and CI infrastructure failures hold a deploy until someone acts. Only the new website-contract tests and `test_cors.py` gate deploys (owner option "3").

## Summary

The gate is well built, and almost everything it claims holds up when re-run. HEAD's check is green, re-recording at the pin reproduces `contract.txt` byte for byte, four breaks of my own fail with named keys, 13 of 15 rule mutations turn a self-test red, and every RUNBOOK example I ran behaves as written. One gap blocks certification: renaming a request-body field the website sends passes the gate whenever the server gives the new name a default, which silently kills the website's sliders or override toggle. Spec criterion 1 and the spec-stage product-lens falsifier (spec-F3) both name this case.

## Product Judgment

**Is this the right piece of work? Yes.** It is the "protect" half the owner asked for, scoped to option "3", and it changes nothing in the explorer's API, data or frontend. The mechanism is sound: record what the pinned frontend got, replay on every push, clear false blocks only by a written waiver. The docs let someone who never reads the code operate it.

**Where it falls short of the point.** The owner's goal is "so we don't break anything". The gate only sees a broken request when the server rejects it. A request field that the server now silently ignores breaks the website with no rejection, and the gate passes it (Blocker B1). Pydantic's default is to ignore unknown fields, and this codebase's own convention for request fields is optional-with-a-default (`models.py:622-625`), so this is a likely way to break the website, not a corner case.

**Product-lens (audit block in `product-lens.md`).** No DON'T finding and no BLOCK. Its three DO findings are still true in the code and docs, and appear below as Advisory A5, A6 and A9. The lens marked spec-F3 "FIXED" by citing the request self-tests; my probes show the rename variant of spec-F3's own falsifier is not caught, so spec-F3 is only partly fixed.

**Structural smells.** Two representations kept in step by hand fired at design time (the pin vs the website's `provenance.json`; `runtime_paths.txt` vs the `.dockerignore` "MUST survive" list). Both are disposed: the daily drift job watches the first, and the unwaivable Files rule enforces the second. No new smell fired in the code.

## Blockers

**B1. A renamed request-body field that the server silently ignores passes the gate.**

- **What I did.** In a scratch clone I renamed `ComputeRequest.apply_analyst_overrides` to `use_analyst_overrides`, keeping its `True` default (`models.py:625`, `server.py:1219`). Separately, I renamed `ComputeRequest.overrides` to `param_overrides` with an empty-dict default (`models.py:621`, `server.py:1214`). Both runs of `contract.py check`: `0 failing, 0 waived, 0 stale waivers`, exit 0.
- **Why it passes.** The pinned frontend still sends the old name. Pydantic drops the unknown field, so the server returns 200 with an unchanged response shape. The rules table maps request changes only to the Status rule (design rules table; `contract_rules.py:213-223`), which fires only when the server rejects a request.
- **What breaks on the website.** With the first rename, the analyst-override toggle on the 15 concepts in the toggle coverage set does nothing: the page asks for the bare LCOE and gets the analyst-applied one. With the second, every slider on the 33 slider concepts stops changing the LCOE. `concepts.1cf.energy` keeps working because its newer JavaScript sends the new name. That is exactly the failure this item exists to stop.
- **Which requirement.** Spec Success Criterion 1, second bullet: "changing a path, method or request-body field the frontend sends". The spec-stage product lens gave this as its falsifier for spec-F3: "rename `apply_analyst_overrides` on the server ... the gate stays green". The kept self-tests cover only a newly required field and rejected values (`test_request_model_breaks_fail`), not a rename the server accepts.
- **What should change.** The gate must fail when a field the pinned frontend sends is no longer one the server reads. One shape for it is a rule that checks each sent field name against the current request schema's declared properties, with self-tests renaming each sent field of both POST bodies to an optional name. The design says "Check reads no schema", so the fix needs a design amendment through the orchestrator, not just code.

## Advisory

Ranked by importance. None of these blocks certification.

**A1. Two rule clauses can be deleted without any self-test noticing.** I removed each and ran the full self-test file: 119 passed both times.
- The Status rule's "no 200 at all where the pin had one" clause (`contract_rules.py:221-222`, plan decision 8). At this pin every template recorded only 200, so the per-instance clause covers a removed route, and Shape or Coverage cover a template that stops being sent. The clause is untested defence for a future pin.
- The CORS rule's preflight-status clause (`contract_rules.py:285`). `test_cors.py:59` covers the compute preflight's status behaviourally, but not the state preflight, and not the gate's own clause.
- Impact: a later refactor can drop either clause silently. Add one self-test for each.

**A2. A new response key with a space or dot in an untyped object crashes the check, and no waiver can clear it.** `field_path` raises on any record key holding whitespace, `.`, `[`, `]`, `{` or `}` (`json_shapes.py:58-65`). Untyped objects take their keys from data: the taxonomy tree, the findings body and `narrative.risks[]`. I added `"display name"` to the tree's root node and the check stopped with a `ValueError` traceback, exit 1. That is an additive change, which spec criterion 2 says passes. The RUNBOOK then misdiagnoses it: "A Python traceback in the contract step ... the server no longer starts or imports. A real break: fix the code" (`RUNBOOK.md:134`). It fails closed, so it can't let a break through, but it can hold every deploy with no documented way out. Report it as a named failure key instead, or skip keys that can't be written as a path, and name the case in the RUNBOOK.

**A3. A waiver for a `cors` or `files` key loads, then prints a wrong instruction.** `_check_match` accepts any rule (`waivers.py:73`). `apply_waivers` then reports the waiver as `STALE` (`waivers.py:102,107`), and the report says "Delete each STALE waiver: it matches no failure any more" (`contract.py:215-216`). I confirmed this: the `cors GET /api/manifest` key stayed `FAIL`, and the waiver printed `STALE` next to it. The RUNBOOK describes the behaviour correctly (`RUNBOOK.md:201`), but the gate's own message is false: the waiver does match a failure, it just can't clear it. Separately, the hint "A false block clears with a [[waiver]]" prints even when only unwaivable rules failed (`contract.py:211-214`). Reject a `cors` or `files` waiver at load as a configuration error that names the fix, and skip the waiver hint when every failing rule is unwaivable.

**A4. The shipped gate carries code only the unshipped Phase 1 harness uses.** `observe`'s `skip` parameter (`frontend_requests.py:182,189`) and the per-request timings (`Response.seconds` and `_timed`, `frontend_requests.py:153,195,271,278-282`) are read only by `.project/active/explorer-api-contract-gate/phase1/side.py:121-128`. Nothing in `website_contract/` or the self-tests passes `skip` or reads `seconds`. When the item closes, the harness is archived and this becomes dead surface in a module a future reader has to understand. Remove both, or move the timing into the harness.

**A5. The owner's ruling on how strict the gate is has no tracking item** (product-lens audit-F1). ADR 0011 (`.project/adr/0011-explorer-deploys-wait-for-website-contract.md:26`) and plan Phase 1 Results both say "whether to soften the Shape and Unpopulated rules is parked with the owner". Neither owner-acceptance list carries it (`spec.md:39-43`, `plan.md:601-611`). So close and pre_pr won't raise it. Add it to the owner-acceptance list.

**A6. Two docs describe held deploys as already happening** (product-lens audit-F2). README §9's opening says a deploy gate "holds back a push that would break the website" (`exploration/concept_explorer/README.md:690`). That is false from merge until the owner turns on "Wait for CI". `CLAUDE.md:258` ties it to "Wait for CI" but doesn't say the setting starts off. The RUNBOOK's decisions note names only FR-6's "no GitHub Actions" clause (`RUNBOOK.md:340`), while ADR 0011 correctly names both changed clauses. Condition the README and `CLAUDE.md` lines on the setting, and name both clauses in the RUNBOOK note.

**A7. The RUNBOOK's sequence for bringing an omitted concept back is sound, with one missing caution** (`RUNBOOK.md:226`). This is the agent-grade addition the brief asked me to check.
- **Sound.** The branch removes the omit-list line. The website imports that branch commit X. The gate is re-pinned to X, and the removal and the new contract merge together. The merge commit serves the concept, and the contract at X lists it, so the gate passes and Railway deploys. I found no ordering that avoids a window, because each site deploys on its own.
- **The cost is stated plainly.** "Whichever site updates first, the other shows a broken page or a dead link for the concept until the second catches up, so do the two close together." That is accurate: website first gives a broken page, API first gives a dead link. During the window the daily drift run may also turn red, which is expected.
- **Missing caution.** It doesn't say to keep X on `main`'s history. A squash or rebase merge leaves the website pinned to a commit that exists only on a deleted branch. The next re-pin starts with `git fetch origin` to get the website's pinned commit (`RUNBOOK.md:270`), and the website links its source tree by that SHA. Add "merge with a merge commit, so the website's pinned commit stays on `main`".

**A8. The test-tool list is spelled in three places:** `gate.sh:18` (check-mode pins), `gate.sh:81` (record-mode install) and `contract.py:61` (`TEST_TOOLS`, which writes the header's `tools` line). Adding a tool to `gate.sh` alone leaves the header's `tools` line incomplete. This is minor.

**A9. No `.project/product/` entry records the owner promise** that website-breaking pushes don't deploy (product-lens audit-F3). A cold agent could undo it, for example by adding a push workflow that can fail. The `test_push_workflows_equal_the_reviewed_list` self-test and `CLAUDE.md` already guard this, so it is `_my_close`'s call.

## Findings Detail

### Plan completion

All seven phases are complete, and their changes and validation items are present and verified. No placeholder code or TODOs in the shipped files. I re-ran the evidence the plan claims rather than trusting it:

- **The gate on HEAD.** `timeout 480 gate.sh` on `239f97529` gave `website contract (pin 10f7b9b1f): 0 failing, 0 waived, 0 stale waivers` and `119 passed`. Total 53.9 s on an i7-9750H with `nproc` 12 and a warm `uv` cache.
- **The reproduction at the pin.** `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b` exited 0. `contract.txt` is byte-identical to the committed file (`cmp`). The printed concept line is the website's 37 IDs. The closing check was green, and `git status` was clean afterwards.
- **The drift job, live.** It passed: "links the pinned fusion-tea 10f7b9b…".
- **`railway.toml`.** It parses as TOML.

Documented deviations are all recorded in the plan's Implementation Notes: the `contract.py` split and the deleted `__init__.py`, `MAP_KEYS_READ` left out while empty, the `unread:` waiver evidence form, the seventh map (the `POST /api/state` response) and `setup-uv` pinned to `v10.2.0`.

### Spec conformance

- **SC1, a break fails the gate: not fully met** (Blocker B1). Response fields, concepts, CORS and Files breaks are caught. I confirmed three breaks of my own beyond the self-tests' cases:
  - `CASAccount.cost_m_usd` made a `Decimal`, which serializes as a string deep in every compute response: 80 `shape` keys, including `shape POST /api/compute:slider .cas22_detail{*}.cost_m_usd`;
  - a new `MagnetType` value used by registry entry 01: `enum GET /api/taxonomy/registry .concepts[].magnet_type`;
  - `**/model_setup.py` added to `.dockerignore`: one `files dockerignore …/model_setup.py` key per costingfe concept.

  A fourth break, concept 07's `analysis.md` and `synthesis.md` deleted from the tree, gave two `files missing` keys. Request changes are caught only when the server rejects them; a rename to an optional field is not caught. I unchecked SC1 in the spec.
- **SC2, additive changes pass: met.** Typed fields pass, and I confirmed the self-tests. There is one narrow exception: an untyped key containing a space or dot crashes the check (A2).
- **SC3, a push workflow with no filter, green on the branch head: met on the branch.** `website-contract.yml` triggers on `push` with no filter, and mutating in a `paths:` filter turns `test_the_gate_workflow_has_no_filters` red. The GitHub-hosted run needs a push, so the box stays unchecked for owner acceptance.
- **SC4, under 5 minutes projected: met.** My local runs took 52–54 s, matching Phase 7's 56 s cold run and its 2.9-minute (3.5 conservative) projection. The real runner time is owner acceptance.
- **SC5, a written re-pin step a person can follow: met.** I ran re-pin steps 2, 3, 5 and 6 literally: no diff, and the printed lines match the RUNBOOK's wording. I also ran the refusal in step 4 at a scratch commit whose `concept_page.js` changed by one comment line. It printed "blob changed since the last recording … rerun with --js-reverified" and left `contract.txt` unchanged. Rerunning with `--js-reverified` recorded a contract that differs from the pin's in exactly the `pin` line, the regenerate line and that file's blob line. Step 1 needs the private website repo and was not run.
- **SC6, the RUNBOOK covers skipped deploys, recovery and the toggle: met.** Railway's wording is marked unconfirmed for the owner, as the spec requires.
- **Owner acceptance (three spec boxes, nine plan boxes): left unchecked.** Each needs a push or an owner-only setting.
- **`[NEED]` "so we don't break anything", `[NEED]` tests on the API: met except B1.**
- **`[INFERRED]` items** (only the contract tests and CORS gate deploys; a failing gate blocks; false blocks cleared only by a recorded waiver; every endpoint protected; contract follows the pinned frontend; real served data for every website concept): **met.** All 37 concepts are replayed on real data, including both POSTs, `/api/parameter_index` and every `/api/parameters/{name}`.
- **`[HARD]` items:** the endpoint list and POST bodies match `frontend_requests.py:59-94` and `observe` (`frontend_requests.py:182-254`). The 37 IDs equal the contract's `concepts` line. The "Wait for CI" behaviour is documented in the RUNBOOK as Railway states it.
- **Non-goals respected.** `git diff f96ad312c -- exploration/concept_explorer/static exploration/concept_explorer/templates exploration/concept_explorer/data exploration/concept_explorer/*.py` is empty. So is the same diff over `omit_list.yaml`, `Dockerfile`, `.dockerignore`, `requirements-serve.*`, `exploration/concept_analysis` and `archive`. The only change under `exploration/concept_explorer/tests/` is the new `test_website_contract.py`. The red explorer suite is untouched.

### Design conformance

The implementation follows the design.
- **Decisions D1–D12 all hold.** I checked the code for each, and ran it where I could: recorded from the pin's own server, with `require_own_server` at `pin_source.py:134`; maps and arrays unioned; requests derived at check time; in-process `TestClient` under `uv` and Python 3.12; sparse, blobless checkout with the file audit; the `.dockerignore` matcher failing closed; waivers, with `cors` and `files` unwaivable; the pin only in the header, plus daily drift; unlisted IDs failing in the manifest and in parameter `concepts[]`; triggers with no filter, `timeout 480` and no cancel; `notify_visualization.yml` unable to fail; the module split as the design's Component Overview amends D12.
- **Invariants I1–I8 all hold.** I1 is shown by my byte-identical reproduction. I2 by the refusal run. I3 by the `missing` and `dockerignore` breaks. I4 and I5 by the workflow self-tests and the `gate-filter` mutation. I6 by the waiver loader. I7 by `gate.sh`. I8 by the scope diff.
- **B1 starts in the design, not the code.** The rules table maps the request half of criterion 1 to Status only: "path or method changed; field newly required; value rejected". So the code does what the design says, and the design under-covers the spec. Neither design review caught it.

### Code integrity

**Overall.** The nine modules have clear boundaries.
- `contract.py` is a thin command line (225 lines).
- `json_shapes.py` and `contract_text.py` are pure and use only the standard library.
- `contract_rules.py` holds classify, record and the rules.
- `frontend_requests.py` holds the cited request tables and the HTTP driver.
- `waivers.py`, `pin_source.py` and `file_audit.py` each own one concern, and `drift.py` stands alone.

The Docker matcher (`file_audit.py:123-259`) is careful work. Its tests cite Docker's own cases, and it refuses syntax it doesn't implement. Error messages are actionable where I triggered them: malformed waivers, unsupported `.dockerignore` syntax, record refusals, drift verdicts.

**Mutation check.** I removed or disabled 15 rules one at a time in a second scratch clone and ran the self-tests plus `test_cors.py` each time. Thirteen turned at least one test red:

| Mutation | Tests red |
|---|---|
| shape rule | 4 |
| absent marking | 2 |
| unlisted rule | 2 |
| missing rule | 4 |
| unwaivable filter | 2 |
| literal rule | 2 |
| enum rule | 1 |
| findings coverage | 2 |
| per-instance status | 1 |
| unpopulated evidence | 1 |
| `.dockerignore` rule | 2 |
| missing-file rule | 4 |
| a `paths:` filter on the gate workflow | 1 |

Two turned nothing red: the "no 200" status clause and the preflight-status clause (A1).

**Failure honesty.** No broad `except` in the gate, and no silent fallbacks. One crash path is honest but undocumented and can't be waived (A2). One message gives a wrong instruction (A3). Speculative surface is listed in A4, duplication in A8.

---

## Certification

**Checked and run:**
- `gate.sh` on HEAD, and `gate.sh record` at the pin, with a byte-identical result.
- Seven deliberate changes in a scratch clone: four breaks caught, two request renames not caught, one crash.
- Fifteen rule mutations against the self-tests.
- Every RUNBOOK example I could run:
  - the owner's test break (step 3);
  - the `data_grounded` waiver;
  - concept 40 bare, omitted and waived, with exactly the keys and outcomes the RUNBOOK gives;
  - a `cors` waiver;
  - the `.cost_model.*.cost_m_usd` wildcard, which waived 20 keys including `cas22_detail{*}`;
  - re-pin steps 2 to 6, plus the refusal path and `--js-reverified`.
- Drift against the live site.
- The scope diff and the `railway.toml` parse.
- Docs read against the code: the RUNBOOK "Deploy gate" section, README §9, `CLAUDE.md` § Live Deployments, ADRs 0011 and 0012, and the `railway.toml` header.
- Provenance:
  - ADR 0011 splits its grade correctly: `[AGENT] (ratified by owner…)` for "breaking pushes don't deploy", and orchestrator-grade for the three holds.
  - The false-block figures match `phase1/report.md` and the plan wherever they are quoted (ADRs and RUNBOOK): 5 of 23 (22%) on the design's count, 5 of 27 (19%) combined, at most two waiver lines per pair, newest `84422dd08` on 2026-06-15.
  - No doc presents an orchestrator decision as the owner's.

**Marked:**
- **Spec:** SC1 unchecked with a pointer to B1. SC2, SC4, SC5 and SC6 stay checked, verified. SC3 and the owner-acceptance boxes stay unchecked.
- **Plan:** phase boxes stay checked, verified complete. The owner-acceptance boxes stay unchecked.
- **No epic:** this is a single item.
- **`CURRENT_WORK.md`:** updated to "needs work".

**Not checked:**
- The GitHub-hosted run and its real time.
- Railway's "Wait for CI" behaviour and wording, and what a re-run does. These need a push or the owner.
- Re-pin step 1, which needs the private website repo.
- Whether a `1costingfe` upgrade changes the compute response shape (N8, unmeasured by design).
- The Phase 1 history replay itself. I checked its figures against its report, not by re-running `phase1/replay.py`.
- The `.dockerignore` matcher against real Docker. No Docker here; I relied on its cited test cases.
- Every line of the 1,398-line self-test file. I read the break and pass groups and mutation-checked a sample.
- Whether the website's frozen JavaScript has crash points beyond the design's Appendix C.

---

## Round 2

**Verdict:** Certify
**Audited:** 2026-10-08
**Branch:** `feat/explorer-api-contract-gate`
**Commit:** `ad095351b` (fixes `ab252b1f6..0d92ae7a2`)
**Scope:** a focused re-audit per `briefs/reaudit.md`: B1, A1–A8, regressions and certification. The product-lens pass was skipped; it ran in round 1, and its findings are A5, A6 and A9.

### Summary

B1 is fixed. The new Request fields rule catches both of my round-1 renames, and every bypass the brief asked me to try fails the gate wherever it would break the website. A1 and A3–A8 are fixed and verified. A2 is only partly fixed: a new key with a space still crashes the check when some objects at a path carry it and others don't (R2-1, advisory). There are no regressions: the gate is green on HEAD, recording at the pin is byte-identical, and the explorer's API, data and frontend are untouched. Spec criterion 1 is now checked.

### B1: fixed

The rule reads each POST route's request-body properties from the served app's own `/openapi.json` (`contract_rules.py:102-124`). It fails each top-level field the pinned frontend sends that the route doesn't declare, as `request-field <template> <field>` (`contract_rules.py:325-336`). `check_tree` runs it beside the recorded rules and CORS (`contract_rules.py:374`).

I made each change below in a scratch clone of `ad095351b` and ran `contract.py check` against the committed contract.

| Change | Does the website break? | Gate | Keys |
|---|---|---|---|
| Round-1 break: `ComputeRequest.apply_analyst_overrides` renamed `use_analyst_overrides`, default `True`; the server reads the new name | Yes. The override toggle does nothing on 15 concepts | Fails, exit 1 | 3: `request-field POST /api/compute:{slider,slider-range,toggle} apply_analyst_overrides` |
| Round-1 break: `ComputeRequest.overrides` renamed `param_overrides`, default `{}` | Yes. No slider on the 33 slider concepts changes the LCOE | Fails, exit 1 | 3: the same templates, `overrides` |
| A state-body field renamed: `ExplorerState.slider_overrides` to `sliders` | No. No JavaScript on either site calls `GET /api/state`, so state is write-only | Fails, exit 1: a false block | 2: `request-field POST /api/state:{concept,compare} slider_overrides` |
| `ComputeRequest` accepts arbitrary extra fields (`extra="allow"`), plus the `apply_analyst_overrides` rename | Yes. The old name lands in the extras, which the server never reads | Fails, exit 1 | 3 |
| `ComputeRequest` accepts extra fields and drops the declared field; the handler reads it back from the extras | No | Fails, exit 1: a false block | 3 |
| `apply_analyst_overrides` moved into a nested `options: ComputeOptions` with a default | Yes. The toggle does nothing | Fails, exit 1 | 3 |
| Extra probe: the compute route hidden from OpenAPI (`include_in_schema=False`) | No | Fails closed, exit 1 | 9: every compute field |
| Extra probe: the compute handler takes an untyped `dict` body and builds the model itself | No | Fails closed, exit 1 | 9 |
| Extra probe: the old field stays declared but unread, and a new field carries the toggle | Yes. The toggle does nothing | **Passes**, 0 failing | none (R2-2) |

Every change that breaks the website fails the gate, except the last. That one is out of reach of a schema check: the field the website sends is still declared, and only the server's behavior changed. Catching it would mean comparing response values, and the spec makes "Checking numeric results" a non-goal. So B1 as round 1 stated it, a renamed request-body field that the server silently ignores, is closed.

The three false blocks fail closed and clear with one waiver line each. That is the trade the spec accepts: missing a real break is worse than a false block.

**The design amendment says what the code does.** I checked the rules-table row (`design.md:221`), the Architecture line (`design.md:209`), Core Concept's failure list (`design.md:106`), Appendix D's rename cases and Appendix E's key shape. The rule is waivable as designed, and `contract.txt` is unchanged, shown by the byte-identical re-record. One understatement: the design says the rule resolves `$ref`, and the code also unions `anyOf` and `allOf` alternatives (`contract_rules.py:117-124`). The plan's Audit fixes note says so. It is harmless.

**Self-tests.** `test_a_renamed_request_field_fails` (`test_website_contract.py:761`) renames each of the seven sent fields to an optional name. With the rule disabled, all seven went red.

### Round-1 advisories

- **A1: fixed, verified.** Disabling the "no 200 at all" clause turned `test_a_template_with_no_200_left_fails_status` red (`test_website_contract.py:652`). Disabling the preflight-status clause turned `test_a_refused_preflight_fails_cors` red (`test_website_contract.py:913`).
- **A2: partly fixed.** The case the test covers is fixed: removing the check-time skip turned the `new-key-that-cannot-be-a-path` pass case red, and removing the record-time refusal turned `test_recording_fails_on_a_key_that_cannot_be_a_path` red. A key on some but not all objects at a path still crashes the check (R2-1).
- **A3: fixed, verified.** Removing the load-time rejection turned both `test_a_cors_or_files_waiver_is_a_configuration_error` cases red (`test_website_contract.py:1098`). Making the waiver hint unconditional turned `test_the_waiver_hint_prints_only_for_a_waivable_failure[unwaivable-only]` red (`test_website_contract.py:1119`). A `*` can't stand for the rule (`waivers.py:86`), so rejecting by rule name covers every waiver that can only match `cors` or `files` keys.
- **A4: fixed, verified.** `skip`, `Response.seconds` and `_timed` are gone from `website_contract/`. The harness times requests and leaves compute unsent through its own client wrapper (`phase1/side.py`, `HarnessClient`). I re-ran `replay.py identity`: all three identity checks gave 0 failure keys, with 49 compute calls in each run that includes compute.
- **A5: fixed.** The owner's ruling on how strict the gate is sits in both owner-acceptance lists (`spec.md:44`, `plan.md:612`), pointing at ADR 0011.
- **A6: fixed.** README §9 (`README.md:690`, `:704`, `:728`) and `CLAUDE.md:258` say the gate holds deploys only once "Wait for CI" is on. The RUNBOOK's decision note names both FR-6 clauses (`RUNBOOK.md:342`).
- **A7: fixed.** The bring-back sequence says to merge with a merge commit, and why (`RUNBOOK.md:228`).
- **A8: fixed.** `website_contract/test_tools.txt` is the one list. Check mode installs from it (`gate.sh:60`), record mode takes its names (`gate.sh:75`), and `contract.py` writes the header's `tools` line from it (`contract.py:180-183`). The re-record reproduced the `tools` line byte for byte.
- **A9:** left for `/_my_close`, as the orchestrator decided.

A note on the mutation runs: my mutation clone was sparse and had no `.github/`, so the three workflow self-tests failed in every run, including an unmutated baseline. I counted only failures beyond those three.

### Regressions

- **Gate on HEAD.** `gate.sh` on `ad095351b`, exit 0: `0 failing, 0 waived, 0 stale waivers` and `133 passed`. Steps: venv 0.1 s, install 0.6 s, contract 31.5 s, self-tests 30.3 s, total 62.5 s, warm `uv` cache.
- **Re-record at the pin.** `gate.sh record 10f7b9b1f1466d2057a211bf25f09fc35d80a12b`, exit 0, record step 30.5 s. `cmp` against the committed `contract.txt`: identical. The concepts line is the website's 37 IDs. The closing check was green (133 passed, total 65.3 s), and `git status` was clean afterwards.
- **Scope against `f96ad312c`.** No change to `static/`, `templates/`, `data/`, the explorer's top-level `*.py`, `omit_list.yaml`, `Dockerfile`, `.dockerignore`, `requirements-serve.*`, `exploration/concept_analysis` or `archive`. Inside `exploration/concept_explorer/`, only `website_contract/`, `tests/test_website_contract.py` and `README.md` changed. The fixes changed no workflow.
- **Timing, spec criterion 4.** The self-tests grew by about 9 s. The plan's projection with the new step times: 63 + 2 × (0.1 + 2.6) + 2 × 31.4 + 2 × 29.5 ≈ 190 s (3.2 min), and about 225 s (3.7 min) with the conservative allowances. Still under 5 minutes, with less margin than Phase 7's 2.9 and 3.5 minutes.
- **Dead code and duplication.** Nothing new that needs action. The fixes removed a duplicate route lookup (`_operation`, now shared by `classify` and `request_fields`) and read `/openapi.json` through one helper (`_openapi`). Two small overlaps are acceptable: `_properties` repeats `classify`'s `$ref` and `anyOf` walk in a few lines, and `test_tools.txt` has two tiny readers, one in bash and one in Python. `apply_waivers` still drops `cors` and `files` keys, which `load_waivers` now never passes it; it is a cheap guard with its own test.

### New advisories

None of these blocks certification.

**R2-1. A2's fix misses one case: a new key with a space crashes the check when only some objects at a path carry it.**
- **What happens.** `flatten` counts every key toward its "absent" marking (`json_shapes.py:39`). When a key appears in fewer objects than the path has, it calls `field_path` on that key (`json_shapes.py:43`), which raises for a key holding a space or dot.
- **What I did.** I added `"display name"` to one of the tree root's five children: a `ValueError` traceback, exit 1. The same key on all five children passes. The new self-test covers only the passing kind, a key on the single root object.
- **Impact.** The partial case is the likelier one in real data: a new key on one tree node or one `narrative.risks[]` entry. It fails closed, so it can't let a break through. But it holds the deploy on an additive change, and the RUNBOOK reads a traceback as "the server no longer starts or imports. A real break" (`RUNBOOK.md:134`).
- **What should change.** Skip unwritable keys when counting at `json_shapes.py:39`, and add a pass case with the key on one of several objects.

**R2-2. A field the server still declares but no longer reads passes the gate.** If a change keeps `apply_analyst_overrides` declared but reads a new field instead, the website's toggle stops working and the gate stays green. A schema check can't see this, and catching it would mean comparing response values, which the spec excludes. Record it as a known limit in the design's Request fields row, so nobody reads the rule as "the server uses every field it declares". No code change.

**R2-3. The docs call a renamed state field a website break, but it is a false block.** No JavaScript on either site calls `GET /api/state`, so nothing reads back what the website posts. README §9 says a renamed field "breaks the website's ... saved state" (`README.md:718`). The RUNBOOK's test for a `request-field` key calls it "a real break" when "the server now reads the value under another name" (`RUNBOOK.md:179`), which a renamed state field meets. The error is in the safe direction: someone would undo a harmless change instead of waiving it. Say that a `POST /api/state` field is a false block, because the website never reads state back.

**R2-4. The `anyOf` and `allOf` handling in `_properties` is untested** (`contract_rules.py:122-123`). Removing it turned no test red. Both request bodies are plain `$ref`s today, so it is unused. If a body later became optional (`ComputeRequest | None`), the rule would need it; without it, every field would fail, which fails closed. Add one self-test with an optional body, or drop the loop.

### Certification

B1 holds, so this round certifies.

**Marked:**
- **Spec:** criterion 1 checked, with this round as its evidence; its "not met" note replaced. Status line updated. Criteria 2, 4, 5 and 6 stay checked, re-verified by the green gate, the 133 self-tests including the additive pass cases, the timing re-projection, the re-record and the RUNBOOK lines the fixes touched. Criterion 2 keeps the narrow exception in R2-1, as round 1 kept it for A2. Criterion 3 and the four owner-acceptance boxes stay unchecked; each needs a push or an owner-only setting.
- **Plan:** phase boxes stay checked. Owner-acceptance boxes stay unchecked. Status line updated.
- **No epic:** this is a single item.
- **`CURRENT_WORK.md`:** updated to "certified".

**Not checked:**
- The GitHub-hosted run, its real time, and Railway's "Wait for CI" behavior. These need a push or the owner.
- Re-pin step 1, which needs the private website repo.
- The `.dockerignore` matcher against real Docker.
- The Phase 1 history replay itself (`replay.py pairs`). I re-ran only its identity checks.
- Every line of the 1,524-line self-test file. I read the new and changed tests and mutation-checked eight clauses.
- The product-lens pass, skipped per the brief.
- What the server does with a declared field's value (R2-2).
