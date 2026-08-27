# Design Review: Native Research Acquisition and Registration Seam

**Design:** `.project/active/goal-research-seam/design.md`
**Spec:** `.project/active/goal-research-seam/spec.md` (approved 2026-08-25)
**Review File:** `.project/active/goal-research-seam/design-review.md`
**Date:** 2026-08-25
**Reviewer:** fresh stage session (not the authoring session)

---

## The Point

When the model-development loop decides "this needs research," the round has to end with evidence that is actually in the repository. Every source registered at a repo path citable under MR-4, carrying enough provenance to re-fetch and verify it, holdout-checked before a byte was written. No hand-written index entries anywhere in the path. A source that cannot be brought in is queued for a human with a reason. A search that finds nothing is recorded as a negative result the next invocation has to read.

This matters now because the goal layer this epic builds calls `research` as a seam — question and limits in, registered sources or a bounded negative out — and a goal round may not silently absorb the manual repair WI-031 did by hand (`knowledge/SOURCE_INDEX.md:190-218` written by hand, `MANIFEST.jsonl` untouched, holdout checked by counting strings).

Underneath both: the owner's first stated want for this harness is documentation and clean patterns "so that it can be easily operated and managed by a human." A seam that passes its suite and cannot be operated by a non-builder has failed the point.

## Fundamental Assessment

**Concerns — verdict Revise.** The approach is right and the design is unusually well grounded. I spot-checked every load-bearing code claim (below); they hold, with one exception that matters a great deal. "One write door plus one bookkeeper, with identity coming from the bytes" is the correct shape for this problem, it is simpler than the alternatives it rejects, and it reuses the existing writer rather than forking it. I would not ask for a different architecture.

Three things stop this from being approvable as written.

- **A structural smell fired.** The `--holdout-ack` override moves ownership of a quarantine invariant from `PROTOCOL.md` and the owner to whoever runs the script, and the design does not say that is what it is doing. Per the review rubric this escalates into the judgment rather than sitting in the rubric. I am not recommending Rework, because the fix is to delete one flag, not to rethink the design — but this is the top must-fix and it is the highest-consequence finding in the document. (C2)
- **One empirical claim is false, and I proved it false.** The design's provenance check — recompute the raw hash from the artifact on disk and require it to equal the frontmatter hash, else `BLOCKER` — cannot succeed for any page that is not served as UTF-8. `raw.html` is written as re-encoded text, not as the fetched bytes. The offline fixture will be UTF-8 and will hide this. (C1)
- **Barred bytes can land in the repo outside the rollback ladder.** On the local-PDF path the input is copied into `knowledge/raw/` *before* the content holdout scan runs, and nothing removes it afterwards. (C3)

Everything else is specification-level tightening the plan needs anyway.

### Code claims spot-checked (all verified unless noted)

| Design claim | Verdict |
|---|---|
| `append_source_index_entry` at `zotero_ingest.py:210-251`; hardcodes `Type: documentation`, empty `Use for`/`Validation`, no URL field | ✅ |
| Its anchor `## How MBSE Commands Use This File` is absent from `SOURCE_INDEX.md`; every call takes the warn-then-append branch | ✅ headings are `# Source Index`:1, `## Primary Sources`:7, `## How Sources Are Used`:220 |
| `process_local_pdf` writes no manifest row; `append_manifest_entry` called only at `:437` | ✅ (`:436` and `:525`, off by one) |
| Both manifest loaders do `entry["zotero_key"]` unconditionally; only `zotero_ingest.py` calls them (`:290`, `:310`, `:571`) | ✅ |
| Flatten logic at `:158-180`; raw copy at `:489-499`; `claude`-CLI note at `:134-138` | ✅ |
| HTML with `--output` is flat; PDF nests under the file stem; no `raw.pdf` on the local-PDF path (`extract_cli.py:541` writes `raw.html` only from `raw_source_bytes`) | ✅ |
| `file://` rejected — dispatch is `startswith(("http://","https://"))` at `extract_cli.py:407` | ✅ |
| Frontmatter `content_hash_sha256` is the raw *source bytes* (`web_backend.py:444`, `extract_cli.py:515-526`) | ✅ |
| "the URL fixture's frontmatter hash equals `sha256sum raw.html`" | ⚠️ **true only for UTF-8 pages** — see C1 |
| URL-hosted PDF goes through `_extract_pdf_url` (`:250-285`), writes `raw.pdf`, overrides source with post-redirect URL | ✅ (nested dir is named for the *temp* file stem — see A8) |
| WI-031 index block field order at `SOURCE_INDEX.md:190-218` | ✅ |
| `knowledge/research/` has exactly `pending`/`approved`/`impacts` (`cli/__init__.py:865-867`) | ✅ |
| `pyproject.toml` sets `pythonpath = ["."]`; suites under `tests/<area>/`; no test covers `zotero_ingest.py`/`zotero_lib.py` | ✅ (`markers = []` — see A4) |
| PROTOCOL §3 barred bullets, §4 derived-artifact rule, §2 demo-session scope, §80 hook | ✅ structure as described; **semantics of the exception path are not** — see C2 |

---

## Dimensional Review

### 1. Spec Compliance
**Assessment:** Concerns

Coverage is otherwise complete: R-A1/A2 in the request JSON, R-A4/A5 in the return JSON, R-B0–B5 in `source_registry.py` and D1, R-B7 in D9's caller-supplied fields, R-B8 in D6, R-C1–C5 in the command and run record, R-D1–D5 in the guard and negative file, R-E1–E6 in the test table and operator guide, R-F1/F2 in Integration Strategy and Appendix A. R-B3's deferred mechanism is decided and filed as an ADR candidate, which is what the spec asked for.

The gaps:

- **R-D1 `[HARD]` and R-D4 `[HARD]` are weakened by `--holdout-ack`** (C2). R-D1 says holdout enforcement lives in the operation's own code because code is the only thing that binds. An override any caller can pass is prompt-grade enforcement wearing a flag.
- **R-B6 is silently narrowed** (M6). The spec states it unscoped; D5 keeps `profile="zotero-batch"` emitting blocks with empty `Use for`/`Validation` and no `Caveat`. The *reason* is good — per-item prose for a 30-item unattended run is not reasonable. The silence is the problem: capture-fidelity Law 4 says surface it, don't resolve it quietly, and the standing rule is to ask before omitting something the spec asked for.
- **R-A3 is not fully realizable** (M1): a run whose candidates all come back `DUPLICATE`, or a multi-candidate run with one per-candidate `BLOCKER`, has no stated class.
- **R-A2/R-A5 and R-B9 are asserted, not mechanized** (M2).
- **R-E2's offline proof does not predict live behaviour for URLs** until it includes a non-UTF-8 fixture (C1).

Provenance carried faithfully otherwise: the design treats R-B4 as the `[INHERITED]` it was regraded to, keeps the WI-031 blocks as a `[REFERENT]` for field shape without hardening their prose into a requirement, and does not promote any `[INFERRED]` spec item to settled.

### 2. Pattern Consistency
**Assessment:** Pass

Argparse CLI in `scripts/`, suite under `tests/research/`, reuse of `slugify`/`resolve_slug`/`sha256_of`/`_flatten_extraction_output`, a project-owned command beside `manage-concept.md` rather than an edit to a gitignored symlink. `run_analysis.py cmd_add_source` is correctly named as a referent and correctly described as insufficient (it protects one directory). No invented pattern where one existed. Two notes at A3 and A4.

### 3. Abstraction Quality
**Assessment:** Pass

Three modules, each earning its place: the write door, the bookkeeper, the barred set. I tried to remove each. Removing `holdout_guard.py` scatters the barred set across two callers — keep it. Removing `research_seam.py` puts the negative check and the limit count back into prose, which is the thing B4 correctly says does not bind — keep it. `source_registry.py` is the point of the item. The profile switch on one writer is the right call over two writers.

The one abstraction I would push on is the bookkeeper's `open`/`close` pair, and the push is not "remove it" but "make it do the work it claims" (M2, M3). As written it is a record-keeper that trusts the agent's report about work done by a process it never sees.

### 4. Duplication Avoidance
**Assessment:** Pass

Extends the existing writer instead of forking it; the Zotero path becomes a caller of the same code. No second registry. The `verify` operation is new but has no counterpart.

### 5. Data Structure Clarity
**Assessment:** Concerns

The manifest row and the return JSON are stated. The negative record's shape is not, anywhere, and R-D5 sets five minimum contents for it (A2). The registration operation's own return vocabulary is used in the flow (`DUPLICATE`, `BLOCKER`, `OPERATOR_QUEUE`, `REGISTERED`) but never declared as a distinct vocabulary from the seam's four classes (M1), which is precisely how a plan conflates them.

### 6. Route Safety
**Assessment:** Concerns

The routes here are the four return classes and the single write door. Three holes: an undeclared class mapping (M1), a bypassable capture counter (M2), and an override flag that is a catch-all past the safety check (C2). The write door itself is well defended — staging outside `knowledge/sources/`, `os.rename` on the same filesystem, `flock` over the whole commit — except for the `knowledge/raw/` copy that escapes it (C3).

### 7. Bets & Decisions Integrity
**Assessment:** Concerns

The bets are real bets, each with a stated falsification, which is more than most designs manage. B1, B3, B4 and B5 are honest and correctly risky.

**B2 is false as stated.** It bets that `content_hash_sha256` equals "the raw bytes' digest" — meaning, in the design's own step 3, the digest of the raw artifact on disk. It does not, for non-UTF-8 pages (C1). This is the empirical-grounding failure the brief asked me to hunt for: the claim was verified against one UTF-8 fixture and generalized.

**Hidden bets I surfaced:**

- *That the raw artifact on disk is the byte stream that was hashed.* Now falsified (C1).
- *That an `--holdout-ack` flag is an owner action.* Nothing makes it one; the seam is agent-invoked by construction and every agent here has Bash (C2).
- *That the goal layer will only accept a `close`-emitted `return.json`.* This is what actually makes R-D6 bind, and the design never says it (M3).
- *That `verify` runs clean on today's repository.* It does not: 14 entries under `knowledge/sources/`, 11 manifest rows, two legacy sources with no row, one stray file (M4).

Decisions D1–D11 each name the alternative and why it lost, and the rejections are specific rather than decorative. D6's rejection of crash-recovery machinery is correctly grounded in the epic's `[OWNER]` hardening rule — but it spends `verify` as the compensating control, which makes deferring `verify` incoherent (M4).

### 8. Reader Comprehension
**Assessment:** Pass

"One write door plus one bookkeeper," then "identity comes from the bytes, not from the ledger," is a mental model a tired reader gets on one pass. Research Findings leads with what was run and observed. The failure ladder is stated as a ladder, in order, with the uncovered state named out loud rather than buried — the honesty here is the reason I could review it adversarially at all. No coined labels standing in for explanation.

---

## Issues by Severity

### Critical

- **C1 — The provenance check cannot pass for non-UTF-8 pages, and the fixture hides it.** `web_backend.py:515` writes `raw.html` as `fetched.text()` — the response bytes decoded with the declared charset and re-encoded as UTF-8 — while the frontmatter hash is `sha256(fetched.content)`, the bytes as fetched (`:444`). They agree only when the page is already UTF-8.
  Measured this session against a loopback server declaring `charset=iso-8859-1`:
  ```
  content_hash_sha256      : bb219ea41847cdcc1864e1b354f820bdfbe0c01de05df1260bfd1f54a9cda3f5
  sha256(raw.html on disk) : 9e27cbf12bb1d7c9b39d4499b841675b178244b964955c9bfaa62a54c1e51a8f
  sha256(bytes served)     : bb219ea41847cdcc1864e1b354f820bdfbe0c01de05df1260bfd1f54a9cda3f5
  ```
  Consequences: Architecture step 3 returns `BLOCKER` for every such live URL; the Required Invariant "`source_id` recomputed from the raw artifact equals the frontmatter hash" is unsatisfiable from `raw.html`; B2 is false; and B5's argument ("an offline green suite predicts live behaviour") fails in exactly the way B5 warned about, because the fixture will be UTF-8. Related: a page whose declared charset is wrong makes `fetched.text()` raise `UnicodeDecodeError` *after* `output.md` is written, so capture dies mid-write.
  Suggested resolution: record two hashes with different jobs — `source_id`/`raw_sha256` = the frontmatter hash of the source bytes (the identity, which is what dedupe and re-fetch verification need), and `raw_artifact_sha256` = the digest of the file as it sits in the repo (the integrity check, recomputable by any later reader). Verify the *artifact* against the second, not the first. Keep a `BLOCKER` only when the frontmatter hash is missing or `output.md` is absent. Add a non-UTF-8 page to the loopback fixture set so R-E2 proves this. Fold the byte-exact-`raw.html` request into the R-F1 upstream filing that already exists — the filing now has a third concrete asymmetry to carry.

- **C2 — `--holdout-ack` invents an exception path the protocol does not grant, records it in the wrong place, and is not owner-gated.** *(This is the fired structural smell: ownership of a quarantine invariant moves from `PROTOCOL.md` and the owner to the caller, and the design does not say so.)*
  Against the protocol as written: §3's "Barred by default, documented-exception path" covers exactly two named sources already in the repo (`knowledge/sources/aries_cost_account_documentation/**`, `knowledge/sources/tea_dt_mfe_cost_analysis/**`), grants an exception only for *reading* them in a demo session, requires the **owner** to approve it in writing, and requires it **logged in §6** with date, scope and rationale. It is not an exception path for admitting a *new* artifact that carries ARIES-CS content — for that, §3's principle is flat: "any artifact carrying ARIES-CS-specific design or cost data is inadmissible until reveal," with no exception.
  Against the design's own reasoning: B4 argues that script-owned enforcement is what binds and that an agent obeying prompt text does not. "An owner may re-run with `--holdout-ack`" is prompt text. The seam is agent-invoked by construction and every caller has a Bash tool; nothing distinguishes an owner's invocation from an agent's.
  Against R-D4 `[HARD]` and PROTOCOL §4: the ack reason is free text appended to the block's `Caveat` in `SOURCE_INDEX.md`. R-D4 says a match record names the rule and never copies barred design or cost content into a repo artifact. A free-text field written at the moment someone is arguing a barred match away is exactly the channel that rule exists to close.
  Also note the refusal list is narrower than it reads: "refused for barred-path destinations" does almost nothing, because a registration writes a *new* slug and `resolve_slug` appends `_2` on collision, so re-registering the barred Helios paper lands at `overview_of_the_helios_design_a_practical_planar_coil_2` and never matches the barred path (see M9).
  Suggested resolution: delete the flag. A content term hit is always `OPERATOR_QUEUE` — that is what the class is for, and the design already routes every hit to a human. The human path is the protocol's own: the owner writes an exception into the §6 log, and only then may the source be registered. If any in-code override survives, it must be gated on a §6 log entry the guard parses, keyed to the specific source, not on a CLI string — and the design must state plainly that it is extending the protocol, which is an owner question rather than a design call.

- **C3 — Barred bytes reach the repo outside the ladder (local-PDF path), and staging is never swept.** Architecture step 2 copies the input PDF into `knowledge/raw/` before the content scan at step 4. On a holdout hit, step 4 says "discard staging" — the `knowledge/raw/` copy stays. So does it on a step-5 `DUPLICATE`, and on any commit rollback: the failure ladder never mentions it. Separately, `knowledge/.staging/<uuid>/` holds captured content that has not yet been scanned; a hard kill leaves it in the worktree with nothing to sweep it.
  Suggested resolution: copy and hash the PDF inside staging, scan there, and move it into `knowledge/raw/` inside the commit under the lock; add its removal to every rung of the ladder; sweep stale `knowledge/.staging/*` at the start of `register`; add `knowledge/.staging/` to `.gitignore` (nothing there today). Restate the invariant as "no byte is written under `knowledge/` outside `.staging/` before the content scan passes" — the current wording says `knowledge/sources/` and is technically true while the leak exists.

### Major

- **M1 — The registration vocabulary and the seam's four classes are never layered explicitly.** `register` returns `DUPLICATE`; the seam has no such class. Unstated: what class a run gets when every candidate is a duplicate (not `REGISTERED` — nothing was written; not `BOUNDED_NEGATIVE` — the search found a usable source, which is already in the repo and answers the request), and how a per-candidate `BLOCKER` aggregates in a run where other candidates registered. R-A3 requires the class be decidable without a judgment the spec has not made. Give the plan a one-table mapping from the registration vocabulary to the four classes plus the aggregation rule `close` applies.
- **M2 — Capture counting and "disk is truth" are asserted without a mechanism.** The design says the bookkeeper "counts" registrations against `max_captures`, but `register` is a separate process invoked by the command, with no channel back. And `close`'s disk check is one-directional: it catches a claimed `REGISTERED` with nothing on disk, not a run that registered a source and reported `BOUNDED_NEGATIVE`. One mechanism closes both: `register --run <run-dir>` writes a receipt into the run directory and refuses when that run's `max_captures` is spent; `close` reads receipts rather than the agent's log entries. `--run` stays optional so R-B0's standalone call is unaffected.
- **M3 — R-D6's binding argument stops one link short.** "A `close` without a matching run directory is refused" binds only a run that calls `close`. What actually binds is the chain: the goal layer accepts only a `return.json` emitted by `close`; `close` refuses without a run directory; `open` is the only producer of one; `open` enforces the negative. State that chain. Also state plainly that a direct `source_registry.py register` call — required by R-B0 — is outside R-D6 by design, because it is a registration, not a search. Right now a reader has to work out whether the standalone door is a hole.
- **M4 — `verify` cannot be "open for the plan."** Three places make it load-bearing: the failure ladder names it the documented recovery for the uncovered commit window, D6 rejects crash-recovery machinery *because* `verify` reports the state instead, and the Required Invariants name it as the assertion mechanism. Deferring it removes the compensating control that justified the deferral. Second problem: repo-wide `verify` fails on today's data — `knowledge/sources/` holds 14 entries against 11 manifest rows; `iter_cryoplant_iter_org` and `eu_demo_rw_tf_coil_conductor_dematte_bruzzone` (both WI-031) have no row, and `COST_MODELING.md` is a loose file, not a source directory. Decide the legacy disposition: backfill rows for the two WI-031 sources, or have `verify` report pre-seam entries as a distinct legacy class. Either is fine; silence is not, because the first `verify` run will look like a broken tool.
- **M5 — The failure ladder mis-states its uncovered window.** A hard kill after (a) `os.rename` and before (b) the manifest append leaves an orphan source directory with no row and no block — a second uncovered state, not the one named. Both are `verify`-detectable and both should be listed. The claim "the one state this does not cover" is what a plan will trust.
- **M6 — R-B6 is narrowed without surfacing it.** D5 lets the Zotero batch profile keep writing blocks with empty `Use for`/`Validation` and no `Caveat`, which R-B6 forbids unscoped. Say so in the design as a stated deviation with D5's reason, so the plan writes the presence test against seam-profile blocks and does not later "discover" the conflict.
- **M7 — The characterization test and D4 conflict as written.** The R-E5 test pins today's Zotero and local-PDF output "so the extension cannot change them silently," but today's output *is* the warn-then-append-at-end fallback that D4 removes. Say what it pins (block fields, field order, manifest row shape, dedupe behaviour) and what it deliberately does not (insertion position), or step one of the refactor fails its own guard.
- **M8 — The holdout guard parses only half the protocol's path list.** `### Barred by default, documented-exception path` — the Waganer and Araiinejad costing docs — is a separate section, and those two are precisely the sources PROTOCOL §5 records as carrying ARIES-CS data points. Parse both sections. Also, "fails closed if that section cannot be parsed" defends against a parse *error*; the realistic failure is a bullet reformatted into a shape the parser skips, yielding a shorter list and failing open. Pin the parsed set by exact content and count in the test, not just "it parsed."
- **M9 — The path bar cannot mitigate what the Risks section credits it with.** PROTOCOL's barred paths are read bars on existing repo artifacts; a registration writes a new slug, so a destination path effectively never matches. Term-list blindness (B3) therefore has no path-bar backstop. Either state the bar's real job — refusing a barred repo path handed in as a `--local-pdf` input, which is a genuine and worthwhile check — or drop the mitigation claim and let B3's risk stand undiluted, which is the more honest option given B3 is disclosed in the operator guide anyway.

### Minor

- **A1** — The term list misses hyphen variants. PDF extraction routinely produces `ARIES‑CS` with U+2010/U+2011, or hyphenates across a line break. Normalize (casefold, strip hyphens/whitespace, then match) rather than lengthening the list.
- **A2** — The negative record's contents are stated nowhere; R-D5 sets five minimums (request, queries run, candidates with dispositions, failures with reasons, why the search was adequate). Name the fields; defer only their spelling.
- **A3** — Re-keying `load_manifest` by `source_id` changes semantics for its three existing call sites (`zotero_ingest.py:290`, `:310`, `:571`). Prefer adding `load_manifest_rows()` and leaving `load_manifest` keyed by `zotero_key`. Blast radius is small — both loaders are called only from `zotero_ingest.py` — which is exactly why the cheap option is right.
- **A4** — `pyproject.toml:53` is `markers = []`. Register a `slow` marker there or the PDF-chain mark is a warning.
- **A5** — Nothing in `.gitignore` covers `knowledge/.staging/`; add it with the implementation (also C3).
- **A6** — The operator guide should cover a fourth action: reading and acting on a `verify` report. Two actions are listed; `verify` is the documented recovery path, so a non-builder needs it (SC9).
- **A7** — `iter_cryoplant_iter_org` holds two extractions under one slug with one index block. The one-slug-one-row-one-block model cannot express that. Not required here — but say it is outside the model, so `verify` and the guide do not surprise a reader who opens that entry.
- **A8** — A URL-hosted PDF nests its output under the *temp file's* stem (`extract_cli.py:279`), so the flattened directory name is meaningless. Harmless because D9 takes the slug from the caller's title — worth one line so the plan does not try to derive anything from the extraction directory name.

---

## Recommendations

1. **Delete `--holdout-ack`** (C2). A term hit is `OPERATOR_QUEUE`; the exception path is the owner writing into PROTOCOL §6. If an override is genuinely wanted, that is an owner question about extending the protocol, not a design call — surface it rather than resolve it.
2. **Split identity from artifact integrity** (C1). `source_id` = frontmatter hash of the source bytes; a second recorded hash covers the artifact on disk. Add a non-UTF-8 page to the loopback fixtures and add the byte-exact-`raw.html` request to the R-F1 filing.
3. **Move the `knowledge/raw/` copy inside the commit, and sweep staging** (C3). Restate the pre-scan invariant over `knowledge/` rather than `knowledge/sources/`.
4. **Add the class-mapping table and the receipt mechanism** (M1, M2). One table and one `--run` flag close R-A3, R-A2/A5 and R-B9 together.
5. **Pull `verify` into the first build and state the legacy disposition** (M4). It is the compensating control D6 spent to reject crash recovery; it cannot be the deferred item.
6. **Fix the smaller factual and scoping statements** (M3, M5–M9): the R-D6 binding chain, the second uncovered kill window, the R-B6 narrowing, what the characterization test pins, both barred sections, and what the path bar really covers.

None of this changes the architecture. Item 2 is budgeted at 2 days; these are edits to the design document plus roughly one extra test fixture and one extra CLI flag in the build.

---

## Resolutions

*(Stage 4 — to be filled in as the owner or orchestrator dispositions each finding. Nothing recorded yet; this review was produced in a non-interactive stage session.)*

---

**Overall:** Revise
**Next Steps:** Record resolutions above, then return to the design-agent session (or re-run `/_my_design`) and point it at this review to incorporate. The reviewer does not edit the design. C2 is the one finding that may need the owner rather than the design agent: deleting the flag is a design call, keeping any form of override is a protocol change and therefore an owner call.
