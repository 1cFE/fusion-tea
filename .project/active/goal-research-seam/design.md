# Design: Native Research Acquisition and Registration Seam

**Status:** Draft (revised after design review, 2026-08-25)
**Owner:** Reid W
**Created:** 2026-08-25
**Updated:** 2026-08-25
**Branch:** `feat/goal-research-seam` (commit `5b268acc`)
**Epic:** Goal Strategy and Task Harness (GSTH), Item 2

## Overview

One script-owned registration operation becomes the only door into `knowledge/`, and a fusion-tea-owned research command drives search → triage → capture → register against a bounded request, ending in exactly one of the four return classes.

## Related Artifacts

- **Spec:** `.project/active/goal-research-seam/spec.md` (approved 2026-08-25)
- **Align:** `.project/active/goal-research-seam/align.md`
- **Spec review:** `.project/active/goal-research-seam/spec-review.md`
- **Design review:** `.project/active/goal-research-seam/design-review.md` — verdict Revise, 2026-08-25; this revision addresses C1–C3 and M1–M9. Dispositions in Appendix B.
- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2
- **Required Reading:** `.project/research/20260822-120756_research-extraction-harness.md` (§4 gaps, §5 patterns P1–P10); `.project/concepts/goal-strategy-task-harness-design.md` § Native seams; `.project/concepts/goal-driven-model-development-harness.md` § Research stage; `scripts/zotero_ingest.py`, `scripts/zotero_lib.py`; `exploration/concept_analysis/scripts/lib/research.py`; `modeling_project/REQUIREMENTS.md` MR-4; `knowledge/holdout/aries-cs/PROTOCOL.md`
- **Decision records:** `.project/adr/INDEX.md` does not exist yet (Item 1 establishes it). No prior decision record constrains this design. The manifest-identity decision below is written as an ADR candidate for that home (R-F2).

## The Point

`[INHERITED: .project/concepts/goal-driven-model-development-harness.md § Success Criteria 4]` When the model-development loop decides "this needs research," the round has to end with evidence that is actually in the repository: every source registered at a repo path citable under MR-4, carrying enough provenance to re-fetch and verify it, holdout-checked before it was written. No hand-written index entries anywhere in the path. A source that cannot be brought in is queued for a human with a reason. A search that finds nothing is recorded as a negative result that the next invocation has to read.

`[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Native seams]` This matters now because the goal layer being built by this epic calls `research` as a seam — question and limits in, registered sources or a bounded negative out — and a goal round may not silently absorb the manual repair WI-031 had to do by hand (`knowledge/SOURCE_INDEX.md:190-218`, index blocks written by hand; `MANIFEST.jsonl` untouched; holdout checked by counting strings).

## Research Findings

Everything below was read or run in this worktree, or measured by the design reviewer and re-checked here.

**The writer to extend.** `append_source_index_entry` (`scripts/zotero_ingest.py:210-251`) takes a Zotero key, hardcodes `Type: documentation`, emits empty `Use for`/`Validation`, has no URL field, and inserts before `## How MBSE Commands Use This File`. That heading does not exist in `knowledge/SOURCE_INDEX.md` — the file's sections are `# Source Index` (:1), `## Primary Sources` (:7), `## How Sources Are Used` (:220). Every call today takes the fallback branch and appends after the explanatory section. Confirmed spec defect R-B1b.

**The missing manifest row.** `append_manifest_entry` (`scripts/zotero_lib.py:52-63`) is called only from the Zotero path (`zotero_ingest.py:436`); `process_local_pdf` ends at `append_source_index_entry` (`:521`). Confirmed spec defect R-B1a.

**Manifest reach.** `MANIFEST.jsonl` is read only by `scripts/zotero_lib.py` and `scripts/zotero_ingest.py` (repo-wide grep; call sites `:290`, `:310`, `:571`). Both loaders do `entry["zotero_key"]` unconditionally, so a row without that key raises `KeyError` today.

**What `agentic-mbse extract` actually does** (run 2026-08-25 against a scratch dir, since deleted):

| Input | Observed |
|---|---|
| `http://127.0.0.1:8799/page.html --save-source --output DIR` | `DIR/output.md`, `DIR/raw.html`, `DIR/metrics.json` — **flat**, no nesting (`extract_cli.py:222-230` passes `--output` straight to `extract_web_content` as `output_dir`) |
| local `coil_note.pdf --save-source --output DIR` | `DIR/coil_note/{output.md,metrics.json,decisions.json,images/}` — **nested**, and **no `raw.pdf`** even with `--save-source` (that flag only saves `result.raw_source_bytes`, populated by the arXiv shortcut, `extract_cli.py:541`) |
| `file:///…/page.html` | **rejected**: `Error: path does not exist: file:/…` — URL dispatch is `startswith(("http://","https://"))` only (`extract_cli.py:407`) |

**Two different hashes, not one.** Frontmatter `content_hash_sha256` is the digest of the bytes **as fetched** (`web_backend.py:444` hashes `fetched.content`; the PDF path hashes the input file, `extract_cli.py:515-526`). But `raw.html` is written as `fetched.text()` — decoded with the declared charset and re-encoded UTF-8 (`web_backend.py:515`). The two agree only when the page was already UTF-8. The reviewer measured a loopback page declaring `charset=iso-8859-1`: frontmatter and served bytes both `bb219ea4…`, `raw.html` on disk `9e27cbf1…`. My original single-hash check was verified against one UTF-8 fixture and generalized; it was wrong, and D1 below is rewritten around it. Related: a page whose declared charset is wrong makes `fetched.text()` raise `UnicodeDecodeError` *after* `output.md` is written, so capture can die mid-write — a `capture_failed`, handled by the staging sweep.

A URL-hosted PDF goes through `_extract_pdf_url` (`:250-285`), which does write `raw.pdf` and overrides the frontmatter source with the post-redirect URL; its nested directory is named for the *temp* file's stem (`:279`), so nothing may be derived from that directory name.

**Extraction invokes Claude for `--index --summarize`.** `zotero_ingest.py:134-138` records that the `claude` CLI refuses to run inside a Claude Code session. The seam is agent-invoked by construction, so it cannot use those flags.

**Rollback referent.** `run_analysis.py cmd_add_source` (`exploration/concept_analysis/scripts/run_analysis.py:980-1075`) does duplicate check → mkdir companion → extract → flatten → symlink inside `try/except` with `shutil.rmtree`. It protects one directory; it has no index or manifest to undo.

**Index-block referent.** The two WI-031 blocks (`knowledge/SOURCE_INDEX.md:190-218`) order fields `### Title`, `Type`, `Location`, `Use for`, `Validation`, `Caveat`, then `#### Extended Metadata` with `Source URL`, `Raw SHA256`, `Extracted Path`, `Extract SHA256`, `Date Added`.

**Holdout source of truth.** `PROTOCOL.md` §3 carries **two** path lists — `### Barred` (:29-37) and `### Barred by default, documented-exception path` (:39-44, the Waganer and Araiinejad costing docs, which §5 records as carrying ARIES-CS data points). §3's principle is flat: any artifact carrying ARIES-CS-specific design or cost data is inadmissible until reveal, with no exception for *admitting* a new artifact. The §3 exception path grants *reading* two named in-repo sources, requires owner approval, and is logged in §6. §4 bars referencing sealed or barred content in any derived artifact. §80 names a PreToolUse hook, which cannot see a fetch inside a script.

**Registry drift already exists.** `knowledge/sources/` holds 14 entries — 13 directories plus a loose `COST_MODELING.md` — against 11 manifest rows. The two WI-031 URL sources (`iter_cryoplant_iter_org`, `eu_demo_rw_tf_coil_conductor_dematte_bruzzone`) have no row, which is the defect this item exists to stop repeating. Also `iter_cryoplant_iter_org` holds *two* extractions under one slug with one index block, which the one-slug-one-row-one-block model cannot express.

**Test ground.** `pyproject.toml` sets `pythonpath = ["."]` and `markers = []`; suites live under `tests/<area>/` with `tests/conftest.py` for shared fixtures. **No test anywhere covers `zotero_ingest.py` or `zotero_lib.py`** — R-E5's "affected regressions" set is empty until this item writes one. `.gitignore` has no entry covering a staging directory.

**Homes.** `knowledge/research/` has exactly three tool-known subdirectories — `pending`, `approved`, `impacts` (`agentic-mbse/src/agentic_mbse/cli/__init__.py:865-867`); nothing scans the directory broadly, so a new sibling is safe. `.claude/commands/` is git-tracked with one project-owned command (`manage-concept.md`); the upstream `/research` is a gitignored symlink into the pinned package.

## Core Concept

The seam is **one write door plus one bookkeeper**.

The write door is a registration operation: a Python module with a CLI that takes a URL or a local PDF plus caller-supplied metadata, captures with `agentic-mbse extract` into a staging directory, checks the holdout rules against the captured content, and only then commits four artifacts together — the source directory, the raw copy, one manifest row, one index block. It is the only code that writes into `knowledge/` outside staging, and it is callable by an operator, by an agent, or by another script.

The bookkeeper is a second small CLI that owns the parts of an invocation that cannot be left to prompt text: validating the bounded request, refusing to start when a durable negative already answers that request, keeping the instrumented run record, counting captures against the request's limit through receipts the write door itself writes, and emitting exactly one return class computed from those receipts rather than from the agent's report.

On top of those sits a fusion-tea-owned `/research-acquire` command carrying the search and triage protocol — the only part that needs a model. It calls the two CLIs; it never writes registry files itself.

The insight is that **identity comes from the bytes, not from the ledger**. `agentic-mbse extract` already records the SHA-256 of the source as fetched, for both URLs and local PDFs, in the output's frontmatter. That number is the durable manifest identity a non-Zotero source has always been missing, and it makes duplicate detection and re-fetch verification the same check. Nothing has to be pushed through Zotero to get an identity. What the repository *stores* is a second, separate number — the digest of the artifact as it sits on disk — because those two are not the same thing (Research Findings, above).

The composition is deliberate: `agentic-mbse extract` stays the capture primitive unchanged (it is pinned, `tests/test_dependency_provenance.py`); `zotero_lib` keeps owning paths, hashing, slugging and manifest I/O; `append_source_index_entry` is extended rather than replaced, and the Zotero batch path becomes a caller of the same writer.

## Key Bets

- **B1.** The SHA-256 of the source as fetched is a stable identity for the sources this project registers — a re-fetch of the same document yields the same bytes often enough that hash equality means "same source." *If false → duplicates slip past the post-capture check for dynamic pages; only the pre-fetch URL check catches them, so the same document lands twice under two slugs.*
- **B2.** `agentic-mbse extract` keeps the capture contract observed above: flat output for HTML with `--output`, a nested stem directory for PDFs, and a frontmatter `content_hash_sha256` that is the digest of the source as fetched — **not** of `raw.html` as written. *If false → the flatten, hash and provenance plumbing at the seam boundary break together, and R-B5 cannot be satisfied without an upstream change.* (Previously this bet claimed the frontmatter hash matched the artifact on disk. That was measured false; see C1 in Appendix B.)
- **B3.** A term scan over the captured content, with every hit routed to a human and no in-code override, is enough holdout safety at the registry boundary. *If false → an artifact carrying ARIES-CS design or cost data but no matching term gets registered, and the demo's clean-room claim is damaged in a way no later check recovers.* The path bar does not back this up (D12, Risks).
- **B4.** Making the request, negative and capture-count bookkeeping script-owned is what makes R-D6 and R-A2 bind; an agent obeying prompt text does not. *If false → the bookkeeper is pure overhead and a paragraph in the command file would have done the same job.*
- **B5.** A loopback HTTP fixture set that includes a non-UTF-8 page exercises the same capture code path a live fetch does, so an offline green suite predicts live behaviour. *If false → the suite passes and live acquisition still fails; epic Item 5 is the backstop that would find it.* The single UTF-8 fixture I first proposed is exactly how this bet failed once already.

## Key Decisions

- **D1. Two hashes with two jobs.** `source_id` (recorded as `raw_sha256`) is the frontmatter `content_hash_sha256` — the source **as fetched**; it is the identity used for dedupe and for re-fetch verification. `raw_artifact_sha256` is the digest of the artifact **as stored** (`raw.html` as written, `raw.pdf`, or the `knowledge/raw/` copy); it is the integrity check any later reader can recompute against the repository. Both go in the manifest row and the index block, under those names. Hard failures at step 3: frontmatter hash missing, `output.md` absent, or the stored artifact absent. The two hashes are **not** compared to each other — they are different bytes by construction for any non-UTF-8 page. *Rejected: one hash* (measured false, C1). The byte-exact-`raw.html` request folds into the R-F1 upstream filing.
- **D2. Manifest identity is `source_id`.** Rows gain `source_id`, `source_kind` (`zotero` | `url` | `local_pdf`), `source_url` or `origin_path`, `raw_sha256`, `raw_artifact_sha256`, `extract_sha256`; `zotero_key` stays for Zotero rows and is absent otherwise. Dedupe order: `zotero_key` when supplied → `source_id` → `source_url` (exact, then scheme/host-lowercased and fragment-stripped) as a **pre-fetch** check that avoids a pointless download. *Rejected: a URL-derived key* (no identity at all for local PDFs; breaks on redirects and mirrors — the WI-031 iter.org entry already covers one source at two URLs). *Rejected: pushing every URL source through Zotero first* (adds a network and API-key step into a path the spec requires to be provable offline, R-E1; Zotero workflow redesign is an epic non-goal). ADR candidate: Appendix A.
- **D3. Both entry surfaces are code, not prose.** The standalone operation (R-B0) is `scripts/source_registry.py` with an argparse CLI, because a script is callable from an operator shell, from another script, and from an agent's Bash tool, and is the only form testable offline. *Rejected: an `agentic-mbse pm` operation* (pinned dependency; an upstream filing, not this item's work). *Rejected: a skill* (not callable from code; no deterministic contract).
- **D4. The research surface is a new project-owned command**, `.claude/commands/research-acquire.md`, beside `manage-concept.md` and committed. It cites the upstream `/research` for the approval flow and does not edit it. *Rejected: editing the symlinked upstream `/research`* (tool-owned and gitignored; the edit would be reverted by the next `agentic-mbse init`). *Rejected: a skill* (the seam wants explicit invocation and a scoped tool list).
- **D5. Index anchor: fix it, fail closed.** Blocks insert before `## How Sources Are Used` (`knowledge/SOURCE_INDEX.md:220`), the real terminal section. If that heading is absent, the write raises instead of appending at end. The current warn-then-append branch is a hand-maintained invariant standing in for a real anchor — a defect, not a design element. *Rejected: adopting append-at-end* (puts new sources after the explanatory section). *Rejected: an HTML-comment anchor* (a second thing to maintain when a heading already works).
- **D6. Two writer profiles, one writer — and R-B6 is narrowed, deliberately.** `profile="seam"` requires non-empty `use_for`, `validation`, `caveat`, and `source_url`-or-`origin_path`, and refuses otherwise. `profile="zotero-batch"` reproduces today's block exactly — including the empty `Use for`/`Validation` and absent `Caveat` — so unattended Zotero ingestion of a large queue keeps working (R-B1c). **Stated deviation:** the spec's R-B6 reads unscoped; this design binds it to seam-profile blocks and preserves the Zotero batch behaviour as legacy. The reason is that per-item prose for a 30-item unattended run is not something a batch caller can supply, and inventing it would be a fallback. The presence test is written against seam-profile blocks only. `--local-pdf` moves to the seam profile and therefore **requires the three metadata flags** — a deliberate breaking change to that operator path, taken because an entry that cannot state what it is for should not be written.
- **D7. Stage, then commit in a fixed order, under a lock, with a sweep.** Detail and the failure ladder are in Architecture. **Amended 2026-08-26 (audit F1).** The sweep as first written cleared the *whole* staging root at the start of every attempt, outside the lock, so a second `register` — even one that refused on its preconditions — deleted the working directory of any attempt in flight. `register` is a standalone operator door, an agent-driven step and the Zotero batch's writer, all against one staging root, so that is a real collision, and the auditor reproduced it. Amended rule: each attempt owns `knowledge/.staging/<uuid>/` and removes it in a `finally`; the sweep runs under the registry lock and removes only entries older than four times `CAPTURE_TIMEOUT_S`. That threshold cannot reach a live attempt, because capture is hard-bounded by the subprocess timeout and commit is a few syscalls under the lock. The invariant D7 was bought for — no unscanned bytes persist across invocations — is unchanged; what changed is that collecting a killed run's leftovers no longer collects a running one's. *Rejected: compensating-delete only* (the `add-source` referent protects one directory and has no index, manifest or raw copy to undo). *Rejected: a write-ahead journal with crash recovery* (no evidence a mid-commit hard kill has happened; the epic's hardening rule bars building it) — and that rejection is paid for by `verify`, which is therefore first-build scope, not deferred (D14).
- **D8. Limits: count what we own, through receipts.** `register --run <run-dir>` writes a receipt into the run directory for every attempt and refuses when that run's `max_captures` is spent; `--run` is optional, so a standalone R-B0 call is unaffected. `close` computes the return class from receipts, not from the agent's log entries, which is how R-B9 (disk is truth) and R-A2/R-A5 get a mechanism rather than an assertion. Search count stays agent-declared into the run record and is checked at close. *Rejected: the bookkeeper counting its own invocations of `register`* (it does not invoke them — the command does, in a separate process, with no channel back). *Rejected: a dispatcher that owns WebSearch* (needs harness machinery this epic defers; hardening rule).
- **D9. Negatives are keyed, not timed.** Stored under the request key (a hash of the request's identity fields), never expiring on a clock; a changed premise produces a different key and therefore a different request. Re-searching the same request requires `--override-reason "<non-empty text>"`, recorded on the new run and appended to the negative's `reopened[]`. *Rejected: a TTL* (invents a number nothing supports).
- **D10. Title is caller-supplied; the slug derives from it.** `slugify(title)` then `resolve_slug(slug, item_key=None)` (`zotero_ingest.py:194-207`) — numeric `_2`, `_3` suffixes for genuine same-title collisions, Zotero's `_<item_key>` branch untouched. A missing title is a `BLOCKER`, not a domain-derived guess. The extraction frontmatter's `title:` is *offered* by the triage step as a suggestion. Nothing is derived from the extraction directory name, which for a URL-hosted PDF is the temp file's stem. *Rejected: deriving the title from URL or page metadata* (the caller already supplies `Use for`/`Validation`/`Caveat` under R-B7; an invented title is the kind of guess the standing rule forbids).
- **D11. The offline fixture is a loopback HTTP server, not a stub, and it includes a non-UTF-8 page.** `file://` is rejected by the CLI (observed), so the fixture URL must be HTTP; a thread-local `http.server` bound to `127.0.0.1:0` serves `tests/research/fixtures/web/`, and the seam runs the real `agentic-mbse extract` subprocess against it. *Rejected: stubbing the capture boundary* (it would prove the plumbing while hiding the flat-vs-nested, missing-`raw.pdf` and re-encoding asymmetries that are the actual integration risk). *Rejected: injecting a pre-captured raw artifact* (same blindness; kept only for the barred-content case, which uses a synthetic marker rather than any real ARIES-CS text).
- **D12. There is no in-code holdout override.** A term or path hit returns `OPERATOR_QUEUE` with the rule id and match offsets, full stop. `--holdout-ack` is deleted. Reasons, all three of which are independently sufficient: PROTOCOL §3 grants a documented exception for *reading* two named in-repo sources with owner approval logged in §6 — it is not an exception path for *admitting* a new artifact, for which §3's principle has no exception; a CLI flag is not an owner action, because the seam is agent-invoked by construction and every caller has a Bash tool, which is exactly the prompt-grade enforcement B4 condemns; and a free-text ack appended to a block's `Caveat` is a channel for barred content into a repo artifact, which R-D4 `[HARD]` exists to close. The human path is the protocol's own: the owner writes an exception into the §6 log, outside this seam. Extending the protocol with a machine-readable exception is an owner question, not a design call, and is not taken here. *Rejected: an override gated on a parsed §6 log entry* (still a protocol extension; surface it rather than resolve it).
- **D13. Two vocabularies, one stated mapping.** The registration operation returns its own lower-layer outcomes; the seam's four classes are computed from them by `close`. Table in Architecture. *Rejected: reusing the four class names inside `register`* (a duplicate that answers the request is not the same event as a run that registered nothing, and collapsing them is how a plan conflates the layers).
- **D14. `verify` ships in the first build** and reports drift against a checked-in legacy baseline; it never repairs. Repairing pre-seam drift is not this item's scope. *Rejected: deferring `verify` to a follow-on* (it is the compensating control D7 spent to reject crash recovery; deferring it removes the justification). *Rejected: backfilling the two WI-031 rows now* (a registry write outside the seam's own door, in an item whose point is that no such writes happen by hand).

## Architecture

**Flow of one registration** (`source_registry.register(...)`):

1. **Pre-checks, no writes.** Sweep stale `knowledge/.staging/*` — under the lock, age-thresholded (D7 amendment). Required fields present (else `precondition_failed`). Holdout path bar on the *input identity* — a `--local-pdf` path or a URL under a barred repo path — and term scan on URL and title (else `holdout_hit`). Dedupe by `zotero_key` / `source_url` against the manifest (else `duplicate`, naming the existing slug and path). Receipt-count check when `--run` is given (else `limit_reached`).
2. **Capture into staging.** `agentic-mbse extract <src> --save-source --output knowledge/.staging/<uuid>/ --budget <n>` as a subprocess; flatten a nested PDF stem directory the way `_flatten_extraction_output` does (`zotero_ingest.py:158-180`). For a local PDF the input is copied **into staging**, not into `knowledge/raw/`, because `--save-source` writes no `raw.pdf` on that path and nothing unscanned may land outside staging.
3. **Verify provenance** (D1). Read frontmatter `content_hash_sha256` → `source_id`/`raw_sha256`. Digest the stored artifact → `raw_artifact_sha256`. Digest `output.md` → `extract_sha256`. Hard failure if the frontmatter hash is missing, `output.md` is absent, or the stored raw artifact is absent. No comparison is made between the two raw hashes.
4. **Content holdout scan** over `output.md` and the stored raw artifact. A hit → discard staging, return `holdout_hit` with the rule id and match offsets only.
5. **Post-capture dedupe** by `source_id`. A hit → discard staging, return `duplicate` with the existing slug and path.
6. **Commit**, holding an `fcntl.flock` on `knowledge/.registry.lock`: (a) resolve the slug and `os.rename` staging → `knowledge/sources/<slug>` — one atomic syscall, same filesystem; (b) move the staged raw copy into `knowledge/raw/` (local-PDF path only); (c) record the manifest's byte length, append the row, flush; (d) insert the index block before `## How Sources Are Used`.
7. **Return** `registered` with slug, repo-relative path, `source_id`, and all three hashes.

**The failure ladder.** Before (a): remove the staging tree; nothing else was touched. After (a): remove the renamed source directory. After (b): also remove the `knowledge/raw/` copy — every rung from here down removes it. After (c): also truncate the manifest back to the recorded byte length. The riskiest write — the index read-modify-write — is last so its failure only has to undo cheap, exactly-known things.

**Two uncovered windows**, both from a hard kill inside the lock, both `verify`-detectable: between (a) and (c), an orphan source directory with no row and no block; between (c) and (d), a manifest row with no index block. Neither is repaired automatically. `source_registry.py verify` reports both, plus source directories absent from the manifest and rows whose path does not resolve. It reads a checked-in baseline listing the pre-seam legacy entries — the two WI-031 sources with no row, and the loose `COST_MODELING.md` — and reports them as a distinct `legacy` class so the first run does not read as a broken tool. `verify` never writes to the registry.

**Vocabulary mapping** (D13). `register` returns one of `registered`, `duplicate`, `holdout_hit`, `capture_failed`, `precondition_failed`, `limit_reached`. `close` aggregates the run into one seam class, in this precedence.

**Corrected 2026-08-26 (audit F2).** This table originally sourced `OPERATOR_QUEUE` from receipts only. That was narrower than the spec, which names "paywall, login wall" first among the causes (`spec.md:39`) — and a candidate blocked at those never reaches `register`, so it leaves no receipt. The consequence was not cosmetic: the documented triage step (`log --failure --reason "paywalled"`) closed the run `BOUNDED_NEGATIVE` and wrote a durable negative that then blocked the request, burying a named, human-resolvable source under "nothing there." The spec's class table is the authority and the design was wrong. `close` now reads the queue from both places a blocked candidate can be found.

This does not weaken R-B9. Each source stays authoritative over what only it can know: `registered[]` still comes from receipts alone, so nothing the agent logs can add a source that never landed. `queued[]` is inherently agent-observed — only the agent saw the paywall — and a triage failure asserts nothing about what was registered.

| What the run shows | Seam class | Why |
|---|---|---|
| any `registered` | `REGISTERED` | the request advanced; queued and blocked candidates ride inside the return |
| no `registered`, ≥1 `duplicate` whose candidate was triaged **keeper** | `REGISTERED`, entry marked `pre_existing: true` | the return names a citable repo path that answers the request; the only untrue thing would be claiming this invocation wrote it, which the flag records. `BOUNDED_NEGATIVE` would be false — the search found a usable source |
| otherwise, ≥1 `holdout_hit` / `capture_failed` / candidate-scoped `precondition_failed` **receipt**, or ≥1 `log --failure` entry with disposition `queued` | `OPERATOR_QUEUE` | a named candidate is blocked on something a human must resolve, whether it was blocked at triage or at registration |
| otherwise, search adequate or `limit_reached` | `BOUNDED_NEGATIVE` | names the limit when one was reached (R-A5) |
| run-scoped `precondition_failed` **and zero registrations** | `BLOCKER` | nothing about the search is established |

A run-scoped fault after something already registered stays `REGISTERED` and carries the fault in the return, because what is on disk is established fact (R-B9). The keeper/rejected disposition in the second row is the triage decision R-C5 already requires to be recorded; it is not a new judgment. A `log --failure` entry defaults to disposition `queued`, because "a source was identified but could not be brought in" is the spec's own OPERATOR_QUEUE definition and defaulting the other way writes a blocking negative over a candidate somebody could still fetch; `closed` is available for a candidate nobody should chase, and those stay recorded in the negative's `failures[]`. A candidate seen and judged useless is `log --candidate --triage rejected`, which is a different event and never queues.

**Flow of one research invocation** (`/research-acquire`):

`research_seam.py open <request.json>` → validates the request, computes the request key, and either prints the prior negative and exits non-zero (unless `--override-reason` is given) or creates the run directory. → The command searches and triages (WebFetch is triage-only, R-C2), logging each candidate with `research_seam.py log`. → For each keeper it calls `source_registry.py register --run <run-dir> …`, which writes a receipt. → `research_seam.py close` reads the receipts and the filesystem, computes the class from the table above, writes `return.json`, and writes the negative file when the class is `BOUNDED_NEGATIVE`.

**Why R-D6 binds** (the whole chain, stated because no single link does it): the goal layer accepts only a `return.json` emitted by `close`; `close` refuses without a run directory; `open` is the only producer of a run directory; `open` enforces the negative check. A direct `source_registry.py register` call — required by R-B0 — is outside this chain **by design**, because it is a registration, not a search: it answers no request and produces no return, so there is no negative for it to skip.

**Boundaries.** `source_registry.py` touches only `knowledge/`. `research_seam.py` touches only `knowledge/research/requests/`. Neither writes into `.project/` or `work/`: the join lives in the shared knowledge base.

## Required Invariants

- No byte is written under `knowledge/` outside `knowledge/.staging/` before the content holdout scan passes.
- Each `register` attempt owns its own staging directory and removes it in a `finally`; stale staging from a killed run is swept under the registry lock, so unscanned captured content never persists across invocations and no attempt sweeps another's working directory (D7, amended 2026-08-26).
- Every `knowledge/sources/<slug>/` created by the operation has exactly one manifest row and exactly one index block; `verify` asserts this repo-wide, modulo the legacy baseline.
- Every registered source records both `raw_sha256` (identity, as fetched) and `raw_artifact_sha256` (integrity, as stored), and the stored artifact's digest equals the second.
- Every seam-profile index block has non-empty `Use for`, `Validation`, `Caveat`, and a `Source URL` or local origin.
- Every registered source's `Location` is a repo-relative path that resolves (MR-4).
- No return artifact exists without a run record; no `BOUNDED_NEGATIVE` return exists without a negative file under its request key.
- No holdout match is ever waived in code; no repo artifact — record, fixture, return, or index block — contains barred ARIES-CS design or cost text. Matches are recorded as rule id, count and offsets (R-D4).

## Component Overview

- **`scripts/source_registry.py`** — the registration operation and its CLI (`register`, `verify`). Owns the staging sweep, capture invocation, provenance verification, dedupe, commit/rollback, receipts, and both writer profiles. The single door.
- **`scripts/holdout_guard.py`** — the barred set. Parses **both** §3 path lists of `knowledge/holdout/aries-cs/PROTOCOL.md` — `### Barred` and `### Barred by default, documented-exception path` — and fails closed on either. Because a reformatted bullet would fail *open* by silently shortening the list, the test pins the parsed set by exact content and count, not merely "it parsed." Carries the term list — `aries-cs`, `ariescs`, `aries.ucsd.edu`, and the four sealed-paper stems — matched after normalization (casefold, strip hyphens of any kind including U+2010/U+2011 and soft hyphens, collapse whitespace) so that PDF hyphenation and line-broken forms still match. A hit is never adjudicated and never waived in code (D12): it returns `holdout_hit`. The path bar applies to the **input identity** — a `--local-pdf` under a barred path, or a URL naming one — never to the destination slug, which is newly minted and could never match.
- **`scripts/zotero_lib.py` (extended)** — manifest row schema, `load_manifest_rows()` for `source_id`-keyed access, and a manifest truncation helper. `load_manifest`/`manifest_keys` keep their `zotero_key` semantics for the three existing call sites but must tolerate rows without that key before any non-Zotero row is written. Constants, `slugify`, `sha256_of` unchanged.
- **`scripts/zotero_ingest.py` (extended)** — `append_source_index_entry` gains `source_url`/`origin`, `use_for`, `validation`, `caveat`, `source_kind`, both raw hashes and the profile switch, with the anchor fixed per D5. `process_zotero_item` and `process_local_pdf` become callers of `source_registry.register`; the local-PDF path thereby gets its manifest row (R-B1a).
- **`scripts/research_seam.py`** — request schema and validation, request-key derivation, negative lookup/write/reopen, run record (`run.jsonl` + `process_log.md`), receipt reading, class computation and return emission.
- **`.claude/commands/research-acquire.md`** — the acquisition protocol: bounded request in; search → triage → capture → register → close; WebFetch is triage-only and never quoted or cited; no DI is minted (R-C3), and the owner's `/research` approval gate is where insights are still made (R-C4).
- **`knowledge/research/requests/`** — `<request-id>.json`, `negatives/<request-key>.json`, `runs/<request-id>/<utc-stamp>/{run.jsonl,process_log.md,receipts/,return.json}`.
- **`docs/research_seam_operator_guide.md`** — R-E6 operator documentation: forming a request, invoking both entry points, reading the four return classes, and three operator actions — act on a queued source, act on a bounded negative, read a `verify` report. It states the term-scan blind spot (B3) and the ARIES-CS exception route (PROTOCOL §6, owner-only, outside this seam).

Shapes, kept minimal (R-A1, R-A4, R-D5):

```jsonc
// request
{"request_id","question","consumer","gap_type","priority","where_to_look":[],
 "limits":{"max_searches":N,"max_captures":N}}
// negative — R-D5's five minimums
{"request_key","request_id","queries":[],"candidates":[{"ref","triage","note"}],
 "failures":[{"ref","reason"}],"adequacy":"exhausted|limit_reached","reopened":[]}
// return
{"request_id","run","class":"REGISTERED|BOUNDED_NEGATIVE|OPERATOR_QUEUE|BLOCKER",
 "registered":[{"slug","path","source_id","pre_existing"}],"queued":[{"candidate","reason"}],
 "negative":"<path>","limit_reached":"max_captures|max_searches|null","reason"}
```

## Non-Goals

- Re-registering a *changed* source. A URL whose bytes differ from an existing row is refused as a duplicate naming the existing entry; supersession is an epic non-goal.
- Repairing pre-seam registry drift, or expressing the multi-extraction `iter_cryoplant_iter_org` entry in the one-slug-one-row-one-block model. `verify` reports both as legacy (D14).
- Any in-code path that waives a holdout match (D12), and any change to `PROTOCOL.md`.
- Scoring extraction quality. A cookie wall over 100 characters still "extracts"; judging that stays with the triaging agent, which queues a poor extraction for the operator.
- Enforcing search counts in code (D8), live-network proof (Item 5), DI minting (R-C3), Zotero push, paywall bypass.
- Crash-recovery machinery for the commit sequence (D7).

## Implementation Notes

- Registry paths must be injectable. `zotero_lib` defines `SOURCES_DIR` etc. as CWD-relative `Path` constants; tests need a temp tree without `chdir`. Add a small paths object defaulting to those constants and thread it through the new code; do **not** change the constants themselves.
- Prefer adding `load_manifest_rows()` over re-keying `load_manifest` — three existing call sites depend on its current semantics.
- Staging must be on the same filesystem as `knowledge/sources/` for `os.rename` to be atomic — hence `knowledge/.staging/`, which must be added to `.gitignore` (nothing covers it today).
- Register a `slow` marker in `pyproject.toml` (`markers = []` today) or the PDF-chain mark is a warning.
- Reuse the flatten logic rather than re-deriving it (`zotero_ingest.py:158-180`).
- The PDF pipeline loads table-detection weights and takes ~15 s per document even at `--budget 0`; mark the PDF chain test slow.
- Nothing may pass `--index`/`--summarize` (Research Findings).

## Potential Risks

- **Term-list blindness (B3), unmitigated.** A source carrying ARIES-CS design data without a matching term registers cleanly. The path bar does **not** back this up: PROTOCOL's barred paths are read bars on existing repo artifacts, and a registration mints a new slug, so a destination path never matches. The bar's real job is narrower and still worth having — refusing a barred repo path handed in as a `--local-pdf` input. The residual risk stands undiluted and is disclosed in the operator guide.
- **PROTOCOL.md parse fragility, in both directions.** A parse error stops all registrations, which is the right direction. A reformatted bullet silently shortening the list would fail open, which is why the test pins the parsed set exactly (M8).
- **Breaking `--local-pdf` (D6).** That flag now errors without the three metadata flags. The error names them; the operator guide covers it.
- **First `verify` run shows drift.** 13 source directories and a loose file against 11 rows. The baseline classes them as legacy; without that, the tool reads as broken (M4).
- **Concurrent runs** corrupting the index read-modify-write. Mitigated by the commit lock; two seam runs serialize.
- **Dynamic pages defeating hash dedupe (B1).** Bounded by the pre-fetch URL check; same-document-different-bytes surfaces as a refused duplicate rather than a silent second entry.

## Integration Strategy

The Zotero batch path keeps its behaviour and becomes a caller of the shared writer, so `SOURCE_INDEX.md` entries written before today stay valid and Zotero-key dedupe keeps working (R-B1c). `/research` is untouched; `/research-acquire` is the acquiring sibling and hands finished research documents to `/research`'s existing approval flow, where DIs are minted as they are today. The run record is the P5-style instrumented evidence the H2 probe asked for, produced at no extra cost.

Two upstream filings are made during implementation and listed as deliverables (R-F1): the `approve-research` empty-insight-list refusal (`pm/operations.py:664-668`), and a request that `extract` expose a `--register` hook or return a provenance JSON — the latter now carrying four concrete asymmetries: flat vs nested output, `--save-source` writing no `raw.pdf` on the local-PDF path, no `file://` support, and `raw.html` written re-encoded rather than as the fetched bytes.

## Validation Approach

New suite `tests/research/`, with `conftest.py` providing `local_site` (threaded `http.server` on `127.0.0.1:0` over `tests/research/fixtures/web/`, serving at least one UTF-8 page and one page declaring `charset=iso-8859-1`) and `knowledge_tree` (a temp registry tree: minimal `SOURCE_INDEX.md` with the real headings, empty `MANIFEST.jsonl`, empty baseline).

| Requirement | Test | Shape |
|---|---|---|
| R-E2 (URL chain) | `test_register_url_chain.py` | fixture URL → real `extract` → holdout → commit; asserts source dir, one manifest row carrying `source_id`, `raw_sha256`, `raw_artifact_sha256`, `extract_sha256`, one seam-profile index block with all four required fields, `Location` resolves |
| C1 / B5 | same file, non-UTF-8 case | the `iso-8859-1` fixture registers successfully; `raw_sha256` equals the frontmatter hash, `raw_artifact_sha256` equals the digest of `raw.html` on disk, and the two differ |
| R-E2 (PDF chain) | `test_register_pdf_chain.py` | generated fixture PDF; same assertions plus the `knowledge/raw/` copy appearing only after commit and the flattened layout; marked slow |
| R-E3 (duplicate) | `test_duplicate.py` | same URL twice, and same bytes at a different URL; no second row, no second block; `close` maps a keeper duplicate to `REGISTERED` with `pre_existing: true` |
| R-E3 (rollback) | `test_rollback.py` | failures injected at each rung — before rename, after rename, after manifest append; asserts no source dir, no `knowledge/raw/` copy, manifest byte-identical, index byte-identical |
| R-E3/R-D1/R-D4 (holdout) | `test_holdout.py` | barred URL, barred title, barred `--local-pdf` input path, and a fixture page carrying a **synthetic** marker; asserts nothing under `knowledge/` outside staging, staging discarded, rule id and offsets recorded, no fixture or record containing real ARIES-CS content; asserts no override flag exists |
| R-D1 (guard) | `test_holdout_guard_parse.py` | both §3 lists parsed; exact expected path set and count pinned; a reformatted-bullet fixture fails closed |
| R-D5/R-D6 (negative) | `test_negative.py` | adequate zero-source run writes the negative with all five R-D5 fields; a second `open` on the same request refuses; `--override-reason` proceeds and appends to `reopened[]` |
| R-A2/A3/A5, R-B9 | `test_return_contract.py` | every row of the mapping table; receipts drive the class; a run that registered a source but claims `BOUNDED_NEGATIVE` is corrected from receipts; the `max_captures`+1 registration is refused and the return names the limit |
| R-B8 / D14 | `test_verify.py` | orphan directory, row-without-block, and unresolvable path each reported; baseline legacy entries reported as `legacy`, not as faults; `verify` writes nothing |
| R-E5 | `test_zotero_path_contract.py` | **characterization test written before the refactor.** Pins block field names and order, manifest row shape, and Zotero-key dedupe behaviour. Deliberately does **not** pin insertion position, because today's position is the warn-then-append fallback D5 removes; the position assertion is written against the fixed anchor. `tests/test_dependency_provenance.py` (the pin) is the only other affected suite. |

SC9 is verified by a non-author walking `docs/research_seam_operator_guide.md` and performing the three operator actions; that walk happens at `/_my_audit`.

## Next-Stage Handoff

- **Fixed:** the two-hash split; the four return classes and the mapping table; the commit order, ladder and sweep; one write door with no holdout override; receipts as the capture-count mechanism; `verify` in the first build; the loopback fixture set including a non-UTF-8 page.
- **Open for the plan:** exact field spellings in the manifest row, request, negative and receipt; the baseline file's format and location; the wording of the operator guide.
- **De-risk first:** the `zotero_lib` loader tolerance plus the characterization test, before any non-Zotero row exists. Everything else builds on a manifest both readers can still read.

---

## Appendix A — ADR candidate (R-F2)

Filed 2026-08-25 as `.project/adr/008-source-identity-raw-bytes-sha256.md`, after Item 1 landed the register (commit `007d9488`, imported path-scoped).

**Title:** Non-Zotero source identity is the SHA-256 of the source as fetched.
**Grade:** `[AGENT]`, delegated by the owner at Align (`align.md:8`, "make sure you use your judgement").
**Context:** `MANIFEST.jsonl` was keyed on `zotero_key`, so a URL source had no durable identity and duplicates could not be detected (spec R-B3).
**Decision:** `source_id = raw_sha256 =` the extraction frontmatter's `content_hash_sha256`, the digest of the source as fetched. A second recorded hash, `raw_artifact_sha256`, covers the artifact as stored; the two are different bytes whenever the fetched page was not UTF-8, and are never compared. Dedupe: `zotero_key` → `source_id` → `source_url` (pre-fetch only).
**Consequences:** identity is carried by the extraction output with no service call, which is what lets the chain be proven offline; artifact integrity is separately recomputable by any later reader; a re-fetch whose bytes changed is refused as a duplicate rather than superseded; manifest readers must tolerate rows without `zotero_key`.
**Rejected:** URL-derived key (no identity for local PDFs; redirects and mirrors); push-through-Zotero (network and manual step inside an offline-provable path); a single hash serving both jobs (measured false for non-UTF-8 pages).

## Appendix B — Design-review dispositions

| Finding | Disposition |
|---|---|
| C1 two hashes | Accepted as proven. D1, B2, step 3, invariants, manifest/index fields, non-UTF-8 fixture, R-F1 filing. |
| C2 `--holdout-ack` | **Deleted**, ruled by the orchestrator. D12 records the reasoning. Path bar re-scoped to input identity. |
| C3 raw copy and sweep | Accepted. Copy staged and committed at rung (b); sweep at step 1; ladder and invariant restated over `knowledge/`. |
| M1 class mapping | Accepted. D13 plus the mapping table; all-duplicates-keeper → `REGISTERED` with `pre_existing`. |
| M2 counting mechanism | Accepted. `register --run` receipts; `close` computes from receipts (D8). |
| M3 R-D6 chain | Accepted. Chain stated; standalone `register` stated as outside R-D6 by design. |
| M4 `verify` scope | Accepted. First-build (D14); legacy baseline reported, never repaired. |
| M5 uncovered windows | Accepted. Both windows named. |
| M6 R-B6 narrowing | Accepted. Stated as a deviation in D6. |
| M7 characterization test | Accepted. What it pins and what it does not is stated. |
| M8 both barred lists | Accepted. Both parsed; parsed set pinned by content and count. |
| M9 path-bar claim | Accepted. Mitigation claim dropped; the bar's real job stated; B3 stands undiluted. |
| A1–A8 | All folded in: hyphen normalization; negative fields; `load_manifest_rows`; `slow` marker; `.gitignore`; guide's third action; `iter_cryoplant` noted outside the model; temp-stem directory name noted. |

---

**Next Step:** After approval → `/_my_plan`.
