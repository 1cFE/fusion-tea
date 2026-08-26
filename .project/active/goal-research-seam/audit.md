# Audit: Native Research Acquisition and Registration Seam (GSTH Item 2)

**Verdict:** Needs Work — two HIGH findings, three MEDIUM, three LOW
**Audited:** 2026-08-26
**Branch:** `feat/goal-research-seam` (worktree `../fusion-tea-goal-research-seam`)
**Commit:** `fb0829ea`
**Auditor:** fresh non-author session

---

## The Point

Research is the one hop in the model-development loop with no callable boundary. Everything either side of it has one — modeling has `work/`, generation has sysml-codegen, studies have the run-study skill. Research has a reading command, an extraction primitive, and a Zotero-shaped registry writer, and nothing that joins them.

Item 2 repairs that at the producer. A bounded request goes in; exactly one of four returns comes out. Every registered source is citable under MR-4 by repo-relative path, carries provenance to re-fetch and verify it, has a durable identity even when it never passed through Zotero, and was hold-out checked in code before anything was written. No hand-written `SOURCE_INDEX.md` step survives in the path. A source that cannot be brought in is queued for a person with its reason. An adequate search that finds nothing is a durable negative that blocks a silent repeat. Registration never mints a DI; the owner's approval gate stays where it is.

And the whole thing has to be operable by someone who did not build it. That is the owner's first stated want for this harness, and it is why SC9 exists.

---

## Summary

This is careful work. The code reads like one person thought hard about it: no sentinel-branching, no silent fallbacks, no dead code, error paths that fail in the direction that matters, and a hold-out guard that parses the protocol rather than copying it and refuses to answer at all if that parse comes out the wrong shape. The plan's Implementation Notes are unusually honest — every deviation is recorded with its reason, including one ("the upstream filing is left uncommitted in the other repo") that no one would have caught.

Two things are wrong, and both are real.

The first is a concurrency defect in `source_registry.py`: the staging sweep deletes every in-flight registration's working directory, outside the commit lock. I reproduced it deterministically. The second is a contract gap: a candidate blocked at triage — a paywall, the spec's own first-named reason to queue a source — cannot reach `OPERATOR_QUEUE`. The run closes `BOUNDED_NEGATIVE` and writes a durable negative that then blocks the request from being searched again. Both operator documents teach the exact sequence that triggers it.

Neither is deep. Both need fixing before this ships.

---

## Product Judgment

**Ledger gate: CLEAR.** I scanned every block in `.project/active/goal-research-seam/product-lens.md`, not only the most recent. `spec-F1` (BLOCK) is resolved by citation in the post-finding spec revision; `design-F1` (BLOCK) is resolved by citation against revision `81378776`, verified in the revision diff. No unresolved `BLOCK` stands. The epic carries no live Product-Lens block that binds Item 2 (`epic-plan-F1` and `epic-plan-F2` are both recorded FIXED and both land in other items).

*Instruction-provenance note:* `~/.claude/scripts/product-lens.md` is unreadable from this worktree session (path outside the allowed working directory; non-interactive, so no permission grant is possible) — the same limitation the spec and design blocks record. The lens was run inline in the §3 ledger format those blocks establish, and this session did not spawn a subagent for it.

**Is this the right piece of work?** Yes. The point above is what got built, and it got built at the producer rather than pushed onto consumers. Three things I checked specifically because they are where this kind of item usually goes wrong:

- **The repair is at the producer.** `zotero_ingest.py`'s two verified defects were fixed rather than worked around — the local-PDF path now writes a manifest row, and the missing index anchor now raises instead of warning-and-appending. The pinned `agentic-mbse` was not edited; its four measured asymmetries are filed upstream with the actual hashes.
- **The hold-out invariant did not change owners.** `--holdout-ack` is gone. There is no waiver in code (`grep -rn holdout_ack scripts/ tests/` is empty), the guide states plainly that there will not be one, and the human path is the protocol's own §6 log. This was the design review's top must-fix and it was fixed properly, not softened.
- **Nothing from the hardening path crept in.** No event ledger, no idempotency keys, no crash recovery, no dispatcher. `verify` is the compensating control and it ships, which is what makes the absence of recovery machinery an honest choice rather than a gap.

**One structural smell fires, and I am escalating it rather than resolving it.** *Correctness depends on downstream knowledge of an internal representation* — the return class is computed only from `register` receipts, so an operator who follows the documented triage step (`log --failure --reason "paywalled"`) and never calls `register` gets a class that contradicts the spec's own definition, and a durable negative that blocks the request. The documents teach the failing sequence. This is F2 below and it is why the verdict is Needs Work.

A second smell, *two representations manually kept synchronized*, fires weakly: `raw_artifact_sha256` is derived twice by two different routes for the manifest and for the index block (F7). They agree today. I am not treating it as controlling.

---

## SC map — verified independently

| SC | Named proof | My result |
|---|---|---|
| **SC1** — URL and local PDF each register through one operation into a citable path with full provenance and a complete index block | `test_register_url_chain.py` (13), `test_register_pdf_chain.py` (4) | **MET.** Green. Read the chain at `source_registry.py:218-244` (capture → scan → commit) and confirmed the index block is written by `append_source_index_entry(profile="seam")` — no hand-written step anywhere. |
| **SC2** — the operation is callable on its own | `test_command_contract.py`, CLI | **MET.** I invoked `source_registry.py register` directly, with no request, no run and no command. It works and refuses correctly. |
| **SC3** — duplicate detected, no second entry | `test_duplicate.py` (5) | **MET.** Green. Two dedupe routes read as intended: input identity before the fetch (`:370-387`), `source_id` after it (`:397`). |
| **SC4** — a failure partway leaves no partial state | `test_rollback.py` (6, parametrized over all three commit rungs) | **MET.** Green. `_roll_back` (`:546`) undoes exactly its own rungs; failure injection replaces the real rung functions, so the production path runs. |
| **SC5** — barred case writes nothing, records the rule | `test_holdout.py` (5) | **MET.** Green, and I saw it myself: a barred URL returns `holdout_hit` with `rule_id: term:aries-cs` and offsets, exit 1, nothing written. `_holdout_refusal` (`:350`) records the rule and never the content. |
| **SC6** — durable bounded negative; a later invocation surfaces it instead of re-searching | `test_negative.py` (8) | **MET, with F4 noted.** Green, and I walked it end to end: negative written on close, second `open` refused with exit 3 and the file path, `--override-reason` appended to `reopened[]` with the new run. The blocking is real, not advisory. F4 concerns whether the artifact survives a clean checkout. |
| **SC7** — the entry surface consumes the request and emits exactly one of four classes, gate untouched, no DI minted | `test_return_contract.py` (17), `test_command_contract.py` | **NOT MET.** Exactly-one holds, and the DI/approval separation is clean (`research-acquire.md` rules 2 and 4 are explicit and the command mints nothing). But the class is wrong for the spec's own first-named queue case. See **F2**. |
| **SC8** — the whole chain proven offline for both input kinds; duplicate, rollback, barred write, bounded negative each proven; affected regressions pass | full `tests/research/` | **MET as run, with F3 noted.** `120 passed in 64s` — I re-ran it three times clean. `tests/orchestration/`: 1 passed. `source_registry.py verify`: **0 faults, 3 legacy**, exit 0. `tests/test_dependency_provenance.py`: 2 passed, 1 failed on `KeyError: STOP_PARSER_WHEEL_TARGET` — pre-existing, environmental, and the two tests that assert the pin itself both pass. F3 is that the suite is not hermetic. |
| **SC9** — a non-author walks the documentation and can operate the seam from it alone | this audit | **NOT MET.** I did the walk. Most of it worked well. Two defects, one of them load-bearing. See the walk report. |

---

## SC9 walk report

I read `docs/research_seam_operator_guide.md` before the design or the plan. I had read `spec.md` first, which means I knew the four return classes going in — that contaminates the walk mildly and I am saying so rather than claiming a cleaner test than I ran. Everything below is what the guide alone got me.

**What worked, without help.**

- **Forming a request.** The JSON example (`:71-81`) is complete and I copied it directly. The explanation of what makes two requests the same — key over `question`, `consumer`, `gap_type`, `where_to_look`, sorted, with `priority` and `limits` deliberately outside it — is the single best paragraph in the document. It told me *why*, so I could predict what a change would do instead of guessing.
- **Opening a run.** `open` worked first try. The `$(... | tail -1)` idiom in the guide is needed because the command prints a human line and then the path; slightly awkward, correctly documented.
- **The bounded negative, all three actions.** Accept, re-open, change the request. I ran the re-open: `open` refused with exit 3 and named the negative file, `--override-reason` was accepted and appended to `reopened[]` with the new run and a timestamp. The guide's claim that "a negative never expires on a clock — it is keyed on the request" is exactly what the code does.
- **Reading a `verify` report.** The guide predicts "three legacy entries and zero faults: the two WI-031 URL sources … and the loose `COST_MODELING.md`." That is character-for-character what I got. The `legacy` vs `fault` distinction is the right one to have drawn and it is explained in two sentences.
- **The two hashes.** I understood why they differ and when, from `:56-63` alone, before reading any design document.
- **"What this does not protect you from."** This section is the reason I trust the rest. It states the term-scan blind spot undiluted, explains why the path bar does not cover for it, and says "read what you register. Judgement is still yours." That is honest documentation.

**Where the guide failed me.**

1. **`--title` is documented as optional and is required.** Line 30: "`--title` is new and optional; without it the title is still derived from the filename." The CLI declares it `required=True` (`source_registry.py:835`). Omitting it exits 2 with an argparse error. I hit this on my first `--local-pdf` attempt. (**F5**, MEDIUM.)
2. **The guide's own example for a paywalled candidate produces the wrong return class.** Line 100 shows `log "$RUN" --failure https://example.org/b --reason "paywalled"`. I did exactly that, then closed. The return was `BOUNDED_NEGATIVE` with `queued: []` — and a durable negative was written that now blocks the request. But the guide's *own* "Act on a queued source" section leads with "**Paywall or login wall**," and the spec names paywall first among the reasons to queue. The guide taught me a sequence that silently produces the opposite of what its next section says to expect. (**F2**, HIGH.)
3. **No offline invocation is documented.** The brief asked me to invoke the seam offline. `--local-pdf` is offline in the network sense, but the guide never says how to exercise the URL path without the live network — the loopback-HTTP fixture exists in the test suite and is invisible to an operator. Minor for day-to-day use, real for anyone trying to satisfy themselves the thing works before trusting it. (**F8**, LOW.)
4. **`log --triage` values are never listed.** The guide uses `keeper`; the allowed set is `keeper|rejected`. I guessed `reject` and got an argparse error. Trivially recoverable. (**F8**, LOW.)

**Verdict on SC9:** the guide is well above the bar for prose quality and honesty, and I could operate most of the seam from it. I am not marking SC9 met, because on the one path where being misled has a durable consequence — a blocking negative written for a request that has a known, named, human-resolvable candidate — the guide led me straight into it.

---

## Findings

### Plan completion

All 9 phases complete; zero unchecked boxes; every phase carries filled Implementation Notes with Actual Changes, Issues and Deviations. No TODO, FIXME, placeholder or `NotImplemented` anywhere in `source_registry.py`, `research_seam.py`, `holdout_guard.py`, `research-acquire.md` or the operator guide.

**The four recorded deviations are genuinely recorded and consistent with the design's authority:**

- **`pythonpath = [".", "scripts"]`** (`plan.md:592`) — recorded with its reason (`zotero_ingest` does a bare `from zotero_lib import`) and with the check that no other suite's result changes. Verified: the only `pyproject.toml` change on this branch is two lines inside `[tool.pytest.ini_options]`; `uv.lock` is untouched.
- **`register(source, metadata)` instead of `register(url=..., title=...)`** (`plan.md:634`) — recorded, and justified by the standing rule against sentinel-branching optionals. This is the deviation I would most want to see, because it is the plan being overruled by a quality rule rather than by convenience. It is the right call and the code is better for it (`source_registry.py:59-149`).
- **Receipt gains a `captured` field** (`plan.md:649`) — recorded, with the reason (`max_captures` counts captures; a pre-fetch refusal spends none) and the explicit note that nothing was removed from the pinned shape. Implementation matches (`:808`, `:816-821`).
- **BLOCKER-vs-QUEUE precedence** (`plan.md:681`) — recorded, resolved against the spec's own boundary, and stated in the function docstring where a reader will find it (`research_seam.py:216-229`). Consistent with spec `:42`.

Two things the notes disclose that I want to keep visible rather than bury:

- **The upstream `agentic-mbse` filing is uncommitted in that repository** (`plan.md:696`). Both entries exist — `PM-APPROVE-RESEARCH-EMPTY-INSIGHTS` and `EXTRACT-PROVENANCE-HOOK`, at `~/1cfe/agentic-mbse/.project/backlog/BACKLOG.md:73` and `:88`. R-F1 is satisfied in substance. Someone still has to commit them in the other repo, and the notes say so plainly rather than claiming the filing is done.
- **Phase 8 declines to self-certify SC9** (`plan.md:702`): "it cannot assert a stranger understood it." Correct, and the reason this audit had something real to do.

### Spec conformance

See the SC map above. SC1–SC6 and SC8 verified met; SC7 and SC9 not met, for the reasons given.

**Tagged requirements spot-checked beyond the SC map:**

- **R-B2 `[HARD]` (MR-4 citable path)** — met. `RegistrationResult.location` is `knowledge/sources/<slug>/`, asserted to resolve on disk in `test_register_url_chain.py`.
- **R-C2 `[HARD]` (WebFetch is triage-only)** — met, and enforced structurally: `research-acquire.md` rule 1 states it four ways, and `test_command_contract.py` asserts it. The only thing that becomes a source is what `register` captured.
- **R-C3 `[NEED]` / R-C4 (no DI minting; approval gate untouched)** — met. Nothing in either script or the command touches `pm add-insight` or `approve-research`.
- **R-D1 `[HARD]` (hold-out in the operation's own code)** — met. `holdout_guard.py` is called at two points from inside `_attempt`, not from a hook.
- **R-D4 `[HARD]` (no barred content in any artifact, fixtures included)** — met. `grep -rni aries tests/research/fixtures/` is empty. `marker.html` trips the scan with a single bibliographic filename stem and nothing else, which is the §3 carve-out used correctly.
- **R-D6 (a negative blocks a silent repeat)** — met, and I proved it by hand.
- **Non-goals respected** — no goal-layer routing, no dispatch, no shadow state, no supersession path, no paywall bypass. Verified by grep and by reading.

**Safety invariants, all four checked:**

| Invariant | Result |
|---|---|
| `grep -rni aries tests/research/fixtures/` empty (R-D4) | **Empty.** |
| No in-code hold-out waiver (`grep -rn holdout_ack scripts/ tests/`) | **No matches.** Confirmed by reading `_build_parser` — no such flag exists, and `holdout_guard.py:9-10` states there is none. |
| Nothing lands under `knowledge/` before the content scan | **Confirmed, in the design's stated form.** `_attempt` (`:218-246`) orders: sweep → pre-capture refusal → staging mkdir → capture into staging → **content scan** (`_post_capture_refusal`, `:333`) → commit. Raw bytes do land under `knowledge/.staging/` before the scan, which is the invariant as the design restated it after `design-F3`: staging is gitignored (`.gitignore:35`), swept on entry, and removed in a `finally`. Nothing reaches `knowledge/sources/`, `knowledge/raw/`, the manifest or the index before the scan. |
| `agentic-mbse` pin untouched | **Untouched.** Whole-branch `pyproject.toml` diff is the two pytest lines; `uv.lock` unchanged; the two pin-asserting tests pass. |

**Scope containment, all three checked:**

| Check | Result |
|---|---|
| Item 1's files untouched | **Clean.** `git diff --name-only 6b3d709d~1..HEAD` matches none of `CLAUDE.md`, `.claude/skills/run-study/runbook.md`, `DISCOVERY_LOG`, `GOAL_RUNBOOK`. |
| ADR import path-scoped from `007d9488` | **Confirmed.** `b84046dc` touches only `.project/adr/*`, `.project/scripts/adr.sh`, and the two `tests/orchestration/` files. Item 1's item-directory edits are not imported, and the commit message says so. `ba56783d` adds ADR-008 (R-F2) and amends the design appendix and plan handoff to point at the filed record. |
| No hardening-path mechanism | **Clean.** `grep -rniE "event.?ledger|idempot|crash.?recover|dispatcher"` over the three scripts and the command finds nothing. |

### Design conformance

The implementation follows the design closely, and where it departs it says so. `source_registry.py` is the single write door; `research_seam.py` touches only `knowledge/research/requests/`; neither writes into `.project/` or `work/` — the boundary at `design.md:139` holds. D1's two-hash split, D2's URL normalization, D5's raising anchor, D6's Zotero profile, D8's receipts, D9's request key, D10's slug resolution, D12's absent override, D13's mapping table and D14's `verify`-with-legacy-baseline are all present and behave as described.

**One design-level gap, inherited faithfully by the code.** D13's mapping table (`design.md:127`) sources `OPERATOR_QUEUE` from exactly three receipt outcomes. It never considers a candidate blocked at triage that never reaches `register`. The spec's definition (`spec.md:39`) names "paywall, login wall" first among the causes. The code implements D13 correctly; D13 is narrower than the spec, and the narrowing was not recorded as a decision. This is **F2**.

### Code integrity

**F1 — HIGH — `scripts/source_registry.py:227`, `:252-258`.** `_sweep_staging` deletes *every* entry under the shared staging root at the start of every attempt, and it runs outside the commit lock and before the precondition check. Any second `register` invocation destroys an in-flight registration's staging directory — including an invocation that does nothing at all, since the sweep precedes `_pre_capture_refusal`.

*Reproduced deterministically.* With `tests/research/test_zotero_paths_are_callers.py` running, I issued fifteen `register --local-pdf /tmp/nope.pdf` calls that each return `precondition_failed`. The test failed with `capture_failed: FileNotFoundError: [Errno 2] No such file or directory: 'knowledge/.staging/99295f7b1adf49ccabe423484a2e12fd/.rawin/widget_coil_note.pdf'`. Same failure appeared unprompted in my first full-suite run, which overlapped my own CLI calls.

This is not a test-only problem. `register` is a standalone operator door (R-B0, SC2) *and* is driven by the agent command *and* is called by the Zotero batch — all against `default_paths()`, so all sharing one staging root. The design took concurrency seriously enough to add `_registry_lock` (`:560`, "serialize commits so two runs cannot interleave"); the sweep sits outside it and undoes that care.

*What should change:* the sweep must not delete another attempt's live staging. Either take the lock for it and remove only entries older than a threshold, or scope it to this process's own leftovers (pid- or uuid-tagged), or drop it in favour of the existing `finally: rmtree` plus an explicit operator-run cleanup. The sweep exists to satisfy `design-F3` (no unscanned bytes persist after a crash), so whatever replaces it has to keep that.

**F2 — HIGH — `scripts/research_seam.py:180-183`, `design.md:127`, `docs/research_seam_operator_guide.md:100`, `.claude/commands/research-acquire.md:53`.** A candidate blocked at triage cannot reach `OPERATOR_QUEUE`. `queued[]` is built only from receipts whose outcome is in `QUEUEING_OUTCOMES`, and a receipt exists only when `register --run` was called. `log --failure` entries never become queue entries.

*Failure scenario, run:* an agent following `research-acquire.md` step 3 uses WebFetch to triage `https://example.org/b`, finds it paywalled, and records `log --failure ... --reason "paywalled"` — the documented sequence. It never calls `register`, because there is nothing to register. `close` returns `class: BOUNDED_NEGATIVE`, `queued: []`, `reason: "the search ran and found no usable source"`, and **writes a durable negative** at `negatives/<key>.json`. That negative then makes `open` refuse the request (exit 3) until someone supplies an override.

So a request with a real, named, human-resolvable candidate is recorded as "nothing there" and is blocked from being searched again. That inverts two things at once: the spec's queue-versus-blocker boundary (`spec.md:39, :42`), and the purpose of R-D6, which is to stop *fruitless* repeats — not to bury a source behind a paywall.

*What should change:* the class computation needs to see triage failures. Either `_seam_class` takes `log --failure` entries as a queue source alongside receipts, or `log --failure` writes a receipt of its own so the receipts-are-truth rule (R-B9) still holds — the second is more consistent with the design. Whichever, `design.md:127`'s table and both operator documents need to match.

**F3 — MEDIUM — `tests/research/conftest.py:66-75`.** `_point_legacy_constants_at` redirects `SOURCES_DIR`, `SOURCE_INDEX_PATH`, `MANIFEST_PATH` and `RAW_DIR` at the temp tree, but not `STAGING_DIR`, `LOCK_PATH` or `BASELINE_PATH` (`scripts/zotero_lib.py:24-26`). Any test path that reaches `default_paths()` therefore stages into the **real repository's** `knowledge/.staging` and takes the **real** `knowledge/.registry.lock`. The worktree carries a `knowledge/.staging` directory created by test runs; it is gitignored, which is presumably why nobody noticed.

Consequences: the suite is not hermetic, two concurrent pytest processes interfere, and — via F1 — any operator `register` run during a test run breaks the tests. This is also what made SC8's proof look flaky to me on first run.

*What should change:* patch all seven constants, or have the Zotero-caller tests pass an injected `RegistryPaths` the way the seam tests do.

**F4 — MEDIUM — `knowledge/research/requests/` (no `.gitignore` entry, no tracking).** The bounded negatives, run records and receipts are written to a path that is neither tracked nor ignored. After a walk they show up as untracked repo noise; on a fresh clone they do not exist at all. R-D5 requires a *durable* negative and R-D6 requires a later invocation to find it — both hold within one working tree and neither survives a clean checkout or reaches another operator. `design.md:160` fixes the location but no artifact states the persistence policy, and the guide never tells an operator to commit anything.

*What should change:* decide and record it. Either these are committed evidence (say so in the guide and in the command's step 6) or they are local scratch (gitignore them and say what makes a negative durable instead).

**F5 — MEDIUM — `docs/research_seam_operator_guide.md:30` vs `scripts/source_registry.py:835`.** The guide says `--title` is optional for `--local-pdf` and derived from the filename when omitted. `argparse` declares it `required=True`. Omitting it exits 2. Either the flag becomes genuinely optional with the documented filename derivation, or the guide line is corrected — the guide's version is the nicer behaviour and matches what `zotero_ingest` did before.

**F6 — LOW — `scripts/holdout_guard.py:130-137`.** `_repo_relative` trims a worktree prefix by searching for the hardcoded literal `"/fusion-tea"`. A checkout under any other directory name leaves the path absolute, so it can never match a `knowledge/holdout/...` glob and the path bar silently does not fire. It fails open, which is the wrong direction for this module specifically — everything else in the file is scrupulous about failing closed. Mitigated in practice by the term scan on the same string and by the post-capture content scan, so the exposure is narrow. *What should change:* derive the repo root from the module's own location or from `git rev-parse --show-toplevel`, not from a name.

**F7 — LOW — `scripts/source_registry.py:627` vs `:664`.** `raw_artifact_sha256` is derived twice by two routes: the manifest row uses `_sha256(raw_copy)` (the file after rung (b) moved it), the index block uses `captured.raw_artifact_sha256` (the staged copy, computed at `:472`). They are the same bytes today because `shutil.move` preserves content, so the two agree. It is still one value with two derivations that must stay in step, and if they ever drift the manifest and index disagree silently with nothing checking. `verify` does not compare them. *What should change:* compute it once and pass the same value to both.

**F8 — LOW — operator guide gaps.** `log --triage` never lists its allowed values (`keeper|rejected`; I guessed wrong and got an argparse error), and no offline invocation is documented — the loopback-HTTP fixture that makes the URL path testable without the network exists only in the test suite. Both are small; both cost a non-author a minute.

**No issues found** in these areas, which I checked specifically: sentinel-mode functions (the `Source` protocol at `:59-149` is the correct shape and adding the Zotero kind added no branch); policy in utilities; broad `except Exception` swallowing errors (the one broad except at `:530` re-raises as `RegistrationError` after rolling back, which is the honest form); optional parameters papering over missing data (the three prose fields are required for the seam profile and empty only for the unattended batch, with `design.md` D6 stating why); backwards-compatibility shims with no caller; dead code.

---

## Certification

**Not certified.** Two HIGH findings stand: F1 (concurrent registrations destroy each other) and F2 (a triage-blocked candidate is misclassified as a bounded negative and blocks its own request). F2 also controls the leading Product Judgment as an escalated structural smell.

**What I verified and marked:**

- Spec success criteria **SC1–SC6 and SC8** marked `[x]`, each against the named tests re-run by me plus my own reading of the implementation.
- **SC7 and SC9 left unmarked**, for the reasons in the SC map and the walk report.
- Plan phases: all 9 already marked complete by the implementer and verified so by me — files exist, notes filled, deviations recorded. No plan checkbox changed.
- Epic Item 2 heading left as-is; the item is not fully certified.

**Not checked:**

- **The live registration chain end to end.** I did not run a real `agentic-mbse extract` capture. SC1's proof rests on the implementer's tests, which I re-ran green and read, not on my own capture. My hands-on coverage of `register` was the refusal paths — precondition, missing file, hold-out hit — plus reading the commit and rollback code.
- **`raw_artifact_sha256` correctness against a real re-encoded page.** F7 is a structural observation; I did not verify the latin1 fixture's two hashes myself.
- **The whole-repo test sweep.** I ran `tests/research/`, `tests/orchestration/` and `tests/test_dependency_provenance.py`. I did not re-run the 700-test full suite; the Phase 9 claim that failure counts match the Phase 1 baseline is taken on the implementer's record, not independently reproduced.
- **The upstream `agentic-mbse` filings' content.** I confirmed both entries exist at the recorded lines. I did not read them for accuracy, and I did not verify whether the working-tree edit in that repository has since been committed (checking required a permission this session did not have).
- **`tests/models/`** — needs a syside licence key to collect; excluded, as it was throughout this item.
- **Prose quality of the `Use for` / `Validation` / `Caveat` fields** on anything registered. R-B6 sets a presence bar and the tests assert presence; nobody is checking that the sentences are good, and the guide correctly says judgement stays with the operator.

---

## Related Artifacts

- Spec: `.project/active/goal-research-seam/spec.md`
- Design: `.project/active/goal-research-seam/design.md` (rev `81378776`)
- Plan: `.project/active/goal-research-seam/plan.md`
- Product-lens ledger: `.project/active/goal-research-seam/product-lens.md`
- ADR-008: `.project/adr/008-source-identity-raw-bytes-sha256.md` (R-F2)
- Epic: `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2
