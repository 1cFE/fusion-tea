# Design: Native Research Acquisition and Registration Seam

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-25
**Updated:** 2026-08-25
**Branch:** `feat/goal-research-seam` (commit `5b268acc`)
**Epic:** Goal Strategy and Task Harness (GSTH), Item 2

## Overview

One script-owned registration operation becomes the only door into `knowledge/sources/`, and a fusion-tea-owned research command drives search → triage → capture → register against a bounded request, ending in exactly one of the four return classes.

## Related Artifacts

- **Spec:** `.project/active/goal-research-seam/spec.md` (approved 2026-08-25)
- **Align:** `.project/active/goal-research-seam/align.md`
- **Spec review:** `.project/active/goal-research-seam/spec-review.md`
- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2
- **Required Reading:** `.project/research/20260822-120756_research-extraction-harness.md` (§4 gaps, §5 patterns P1–P10); `.project/concepts/goal-strategy-task-harness-design.md` § Native seams; `.project/concepts/goal-driven-model-development-harness.md` § Research stage; `scripts/zotero_ingest.py`, `scripts/zotero_lib.py`; `exploration/concept_analysis/scripts/lib/research.py`; `modeling_project/REQUIREMENTS.md` MR-4; `knowledge/holdout/aries-cs/PROTOCOL.md`
- **Decision records:** `.project/adr/INDEX.md` does not exist yet (Item 1 establishes it). No prior decision record constrains this design. The manifest-identity decision below is written as an ADR candidate for that home (R-F2).

## The Point

`[INHERITED: .project/concepts/goal-driven-model-development-harness.md § Success Criteria 4]` When the model-development loop decides "this needs research," the round has to end with evidence that is actually in the repository: every source registered at a repo path citable under MR-4, carrying enough provenance to re-fetch and verify it, holdout-checked before it was written. No hand-written index entries anywhere in the path. A source that cannot be brought in is queued for a human with a reason. A search that finds nothing is recorded as a negative result that the next invocation has to read.

`[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Native seams]` This matters now because the goal layer being built by this epic calls `research` as a seam — question and limits in, registered sources or a bounded negative out — and a goal round may not silently absorb the manual repair WI-031 had to do by hand (`knowledge/SOURCE_INDEX.md:190-218`, index blocks written by hand; `MANIFEST.jsonl` untouched; holdout checked by counting strings).

## Research Findings

Everything below was read or run in this worktree.

**The writer to extend.** `append_source_index_entry` (`scripts/zotero_ingest.py:210-251`) takes a Zotero key, hardcodes `Type: documentation`, emits empty `Use for`/`Validation`, has no URL field, and inserts before `## How MBSE Commands Use This File`. That heading does not exist in `knowledge/SOURCE_INDEX.md` — the file's sections are `# Source Index` (:1), `## Primary Sources` (:7), `## How Sources Are Used` (:220). So every call today takes the fallback branch and appends after the explanatory section. Confirmed spec defect R-B1b.

**The missing manifest row.** `append_manifest_entry` (`scripts/zotero_lib.py:52-63`) is called only from the Zotero path (`zotero_ingest.py:437`); `process_local_pdf` ends at `append_source_index_entry` (`:521`). Confirmed spec defect R-B1a.

**Manifest reach.** `MANIFEST.jsonl` is read only by `scripts/zotero_lib.py` and `scripts/zotero_ingest.py` (repo-wide grep). Both loaders do `entry["zotero_key"]` unconditionally, so a row without that key raises `KeyError` today.

**What `agentic-mbse extract` actually does** (run 2026-08-25 against a scratch dir, then deleted):

| Input | Observed |
|---|---|
| `http://127.0.0.1:8799/page.html --save-source --output DIR` | `DIR/output.md`, `DIR/raw.html`, `DIR/metrics.json` — **flat**, no nesting (`extract_cli.py:222-230` passes `--output` straight to `extract_web_content` as `output_dir`) |
| local `coil_note.pdf --save-source --output DIR` | `DIR/coil_note/{output.md,metrics.json,decisions.json,images/}` — **nested**, and **no `raw.pdf`** even with `--save-source` (that flag only saves `result.raw_source_bytes`, populated by the arXiv shortcut, `extract_cli.py:541`) |
| `file:///…/page.html` | **rejected**: `Error: path does not exist: file:/…` — URL dispatch is `startswith(("http://","https://"))` only (`extract_cli.py:407`) |

Frontmatter carries `content_hash_sha256` of the **raw source bytes** for both kinds (`frontmatter.py:22-57`; `web_backend.py:444` hashes `fetched.content`; the PDF path hashes the input file, `extract_cli.py:515-526`). Verified: the URL fixture's frontmatter hash equals `sha256sum raw.html`, and the PDF fixture's equals `sha256sum coil_note.pdf`. A URL-hosted PDF goes through `_extract_pdf_url` (`:250-285`), which does write `raw.pdf` and overrides the frontmatter source with the post-redirect URL.

**Extraction invokes Claude for `--index --summarize`.** `zotero_ingest.py:134-138` records that the `claude` CLI refuses to run inside a Claude Code session. The seam is agent-invoked by construction, so it cannot use those flags.

**Rollback referent.** `run_analysis.py cmd_add_source` (`exploration/concept_analysis/scripts/run_analysis.py:980-1075`) does duplicate check → mkdir companion → extract → flatten → symlink, all inside `try/except` with `shutil.rmtree` compensating delete. It protects one directory; it has no index or manifest to undo.

**Index-block referent.** The two WI-031 blocks (`knowledge/SOURCE_INDEX.md:190-218`) order fields `### Title`, `Type`, `Location`, `Use for`, `Validation`, `Caveat`, then `#### Extended Metadata` with `Source URL`, `Raw SHA256`, `Extracted Path`, `Extract SHA256`, `Date Added`.

**Holdout source of truth.** `PROTOCOL.md` §3 lists barred repo paths as markdown bullets under `### Barred` and `### Barred by default, documented-exception path`; §4 bars referencing sealed or barred content in any derived artifact; §2 scopes the block to demo sessions; §80 names a PreToolUse hook as the escalation path, which cannot see a fetch inside a script.

**Test ground.** `pyproject.toml` sets `pythonpath = ["."]`; suites live under `tests/<area>/` (`tests/study/`, `tests/scoring_v2/`, `tests/models/`) with `tests/conftest.py` for shared fixtures. **There is no test anywhere covering `zotero_ingest.py` or `zotero_lib.py`** — R-E5's "affected regressions" set is empty until this item writes one.

**Homes.** `knowledge/research/` has exactly three tool-known subdirectories — `pending`, `approved`, `impacts` (`agentic-mbse/src/agentic_mbse/cli/__init__.py:865-867`); nothing scans the directory broadly, so a new sibling is safe. `.claude/commands/` is git-tracked with one project-owned command (`manage-concept.md`); the upstream `/research` is a gitignored symlink into the pinned package.

## Core Concept

The seam is **one write door plus one bookkeeper**.

The write door is a registration operation: a Python module with a CLI that takes a URL or a local PDF plus caller-supplied metadata, captures with `agentic-mbse extract` into a staging directory outside `knowledge/`, checks the holdout rules against the captured content, and only then commits three artifacts together — the source directory, one manifest row, one index block. It is the only code that writes into `knowledge/sources/`, and it is callable by an operator, by an agent, or by another script.

The bookkeeper is a second small CLI that owns the parts of an invocation that cannot be left to prompt text: validating the bounded request, refusing to start when a durable negative already answers that request, keeping the instrumented run record, counting captures against the request's limit, and emitting exactly one return class checked against what actually landed on disk.

On top of those sits a fusion-tea-owned `/research-acquire` command carrying the search and triage protocol — the only part that needs a model. It calls the two CLIs; it never writes registry files itself.

The insight is that **identity comes from the bytes, not from the ledger**. `agentic-mbse extract` already computes and records the SHA-256 of the raw source for both URLs and local PDFs, in the output's frontmatter. That single number is the durable manifest identity a non-Zotero source has always been missing, it is recomputable from the artifact on disk, and it makes duplicate detection and re-fetch verification the same check. Nothing has to be pushed through Zotero to get an identity.

The composition is deliberate: `agentic-mbse extract` stays the capture primitive unchanged (it is pinned, `tests/test_dependency_provenance.py`); `zotero_lib` keeps owning paths, hashing, slugging and manifest I/O; `append_source_index_entry` is extended rather than replaced, and the Zotero batch path becomes a caller of the same writer.

## Key Bets

- **B1.** The SHA-256 of the raw source bytes is a stable identity for the sources this project registers — a re-fetch of the same document yields the same bytes often enough that hash equality means "same source." *If false → duplicates slip past the post-capture check for dynamic pages; only the pre-fetch URL check catches them, so the same document lands twice under two slugs.*
- **B2.** `agentic-mbse extract` keeps the capture contract observed above: flat output for HTML with `--output`, a nested stem directory for PDFs, `content_hash_sha256` in frontmatter equal to the raw bytes' digest. *If false → the flatten, hash and provenance plumbing at the seam boundary all break at once, and R-B5 cannot be satisfied without an upstream change.*
- **B3.** A path bar plus a term scan, with every hit routed to a human rather than adjudicated in code, is enough holdout safety at the registry boundary. *If false → an artifact carrying ARIES-CS design or cost data but no matching term gets registered, and the demo's clean-room claim is damaged in a way no later check recovers.*
- **B4.** Making the request and negative bookkeeping script-owned is what makes R-D6 bind; an agent obeying prompt text does not. *If false → the bookkeeper is pure overhead and a paragraph in the command file would have done the same job.*
- **B5.** A loopback HTTP fixture exercises the same capture code path a live fetch does, so an offline green suite predicts live behaviour. *If false → the suite passes and live acquisition still fails; epic Item 5 is the backstop that would find it.*

## Key Decisions

- **D1. Manifest identity is the raw-bytes SHA-256** (`source_id`), read from the extraction frontmatter and independently recomputed from the raw artifact on disk; the two must agree or the registration fails (`BLOCKER`). Rows gain `source_id`, `source_kind` (`zotero` | `url` | `local_pdf`), `source_url` or `origin_path`, `raw_sha256`, `extract_sha256`; `zotero_key` stays present for Zotero rows and is `null` otherwise. Dedupe order: `zotero_key` when supplied → `source_id` → `source_url` (exact, then scheme/host-lowercased and fragment-stripped) as a **pre-fetch** check that avoids a pointless download. *Rejected: a URL-derived key* (no identity at all for local PDFs; breaks on redirects, mirrors and CDN links — the WI-031 iter.org entry already covers one source at two URLs). *Rejected: pushing every URL source through Zotero first* (adds a network + API-key step into a path the spec requires to be provable offline (R-E1), and Zotero workflow redesign is an epic non-goal). This is the R-F2 ADR candidate; see Appendix A.
- **D2. Both entry surfaces are code, not prose.** The standalone operation (R-B0) is `scripts/source_registry.py` with an argparse CLI, because a script is callable from an operator shell, from another script, and from an agent's Bash tool, and is the only form that can be tested offline. *Rejected: an `agentic-mbse pm` operation* (pinned dependency; would be an upstream filing, not this item's work). *Rejected: a skill* (not callable from code; no deterministic contract).
- **D3. The research surface is a new project-owned command**, `.claude/commands/research-acquire.md`, sitting beside `manage-concept.md` and committed to the repo. It cites the upstream `/research` for the approval flow and does not edit it. *Rejected: editing the symlinked upstream `/research`* (tool-owned and gitignored; the edit would be silently reverted on the next `agentic-mbse init`). *Rejected: a skill* (the seam wants explicit invocation and a scoped tool list, which is what a command frontmatter gives).
- **D4. Index anchor: fix it, fail closed.** Blocks insert before `## How Sources Are Used` (`knowledge/SOURCE_INDEX.md:220`), the real terminal section. If that heading is absent, the write raises instead of appending at end. The current warn-then-append branch is a hand-maintained invariant standing in for a real anchor — a defect, not a design element, so it is removed rather than adopted. *Rejected: adopting append-at-end* (puts new sources after the explanatory section). *Rejected: adding an HTML-comment anchor* (a second thing to maintain when a heading already works).
- **D5. Two writer profiles, one writer.** `profile="seam"` requires non-empty `use_for`, `validation`, `caveat`, `source_url`-or-`origin_path` and refuses otherwise (R-B6); `profile="zotero-batch"` reproduces today's block exactly so unattended Zotero ingestion of a large queue keeps working (R-B1c). `--local-pdf` moves to the seam profile and therefore **requires the three metadata flags** — a deliberate breaking change to that operator path, taken because an entry that cannot state what it is for should not be written. *Rejected: putting the Zotero batch path on the seam profile too* (would require per-item prose for a 30-item unattended run).
- **D6. Stage, then commit in a fixed order, under a lock.** Detail and the failure ladder are in Architecture below. *Rejected: compensating-delete only* (the `add-source` referent protects one directory and has no index or manifest to undo). *Rejected: a write-ahead journal with crash recovery* (no evidence a mid-commit hard kill has ever happened; the epic's hardening rule bars building it, and `verify` reports the state instead).
- **D7. Limits: count what we own, declare what we don't.** The bookkeeper counts capture/registration attempts against `limits.max_captures` and refuses past it, so the invocation ends inside the contract naming the limit (R-A2/R-A5). Search count stays agent-declared into the run record and is checked at close. *Rejected: a dispatcher that owns WebSearch and counts calls* (needs harness machinery this epic explicitly defers; hardening rule).
- **D8. Negatives are keyed, not timed.** A negative is stored under the request key (a hash of the request's identity fields) and never expires on a clock; a changed premise produces a different key and therefore a different request. Re-searching the same request requires `--override-reason "<non-empty text>"`, recorded on the new run and appended to the negative's `reopened[]`. *Rejected: a TTL* (invents a number nothing supports).
- **D9. Title is caller-supplied; the slug derives from it.** `slugify(title)` then `resolve_slug(slug, item_key=None)` (`zotero_ingest.py:194-207`) — numeric `_2`, `_3` suffixes for genuine same-title collisions, Zotero's `_<item_key>` branch untouched. A missing title is a `BLOCKER`, not a domain-derived guess (no fallbacks). The extraction frontmatter's `title:` is *offered* by the triage step as a suggestion for the caller to accept. *Rejected: deriving the title from URL or page metadata* (the caller already supplies `Use for`/`Validation`/`Caveat` under R-B7; title belongs in that set, and an invented title is exactly the kind of guess the standing rule forbids).
- **D10. The offline fixture is a loopback HTTP server, not a stub.** `file://` is rejected by the CLI (observed), so the fixture URL must be HTTP; a thread-local `http.server` bound to `127.0.0.1:0` serves `tests/research/fixtures/web/`, and the seam runs the real `agentic-mbse extract` subprocess against it. *Rejected: stubbing the capture boundary* (it would prove the plumbing while hiding the flat-vs-nested and raw-artifact asymmetries that are the actual integration risk). *Rejected: injecting a pre-captured raw artifact* (same blindness; kept only as the mechanism for the barred-content case, which uses a synthetic marker rather than any real ARIES-CS text).
- **D11. The seam never passes `--index`/`--summarize` to `extract`.** Those invoke the `claude` CLI, which refuses to run inside a Claude Code session (`zotero_ingest.py:134-138`), and the seam is agent-invoked by construction. `--budget` is caller-supplied and defaults to `0`.

## Architecture

**Flow of one registration** (`source_registry.register(...)`):

1. **Pre-checks, no writes.** Required fields present (else `BLOCKER`). URL/title against the holdout path bar and term scan (else `OPERATOR_QUEUE`, matched rule recorded). Dedupe by `zotero_key` / `source_url` against the manifest (else `DUPLICATE`, naming the existing slug and path).
2. **Capture into staging.** `agentic-mbse extract <src> --save-source --output knowledge/.staging/<uuid>/ --budget <n>` as a subprocess; flatten a nested PDF stem directory the way `_flatten_extraction_output` does (`zotero_ingest.py:158-180`). For a local PDF, copy the input into `knowledge/raw/` first, exactly as `process_local_pdf` does today (`:489-499`), because `--save-source` writes no `raw.pdf` on that path.
3. **Verify provenance.** Read frontmatter `content_hash_sha256`; recompute the digest from the raw artifact (`raw.html`, `raw.pdf`, or the `knowledge/raw/` copy); mismatch or missing `output.md` → `BLOCKER`. Hash `output.md` for `extract_sha256`.
4. **Content holdout scan** over `output.md` and the raw artifact (see Component Overview). A hit → discard staging, return `OPERATOR_QUEUE` with the rule and match locations only.
5. **Post-capture dedupe** by `source_id` against the manifest. A hit → discard staging, return `DUPLICATE`.
6. **Commit**, holding an `fcntl.flock` on `knowledge/.registry.lock`: (a) resolve the slug and `os.rename` staging → `knowledge/sources/<slug>` — one atomic syscall, same filesystem; (b) record the manifest's byte length, append the row, flush; (c) insert the index block before `## How Sources Are Used`.
7. **Return** `REGISTERED` with slug, repo-relative path, `source_id`, both hashes.

**The failure ladder.** Before (a): remove the staging tree; nothing else was touched. After (a), before (b): remove the renamed source directory. After (b), before (c): truncate the manifest back to the recorded byte length and remove the source directory. The riskiest write — the index read-modify-write — is last precisely so its failure only has to undo two cheap, exactly-known things. A hard kill *between* (b) and (c) is the one state this does not cover; `source_registry.py verify` reports manifest rows without index blocks and source directories without rows, and is the documented recovery path.

**Flow of one research invocation** (`/research-acquire`):

`research_seam.py open <request.json>` → validates the request, computes the request key, and either prints the prior negative and exits non-zero (unless `--override-reason` is given) or creates the run directory. → The command searches and triages (WebFetch is triage-only, R-C2), logging each candidate with `research_seam.py log`. → For each keeper it calls `source_registry.py register …`, which the bookkeeper counts against `max_captures`. → `research_seam.py close --class …` reads the run record and the filesystem, checks the claimed class against what landed (R-B9), writes `return.json`, and writes the negative file when the class is `BOUNDED_NEGATIVE`. A `close` without a matching run directory is refused — that is the structural reason a run cannot skip the negative check.

**Boundaries.** `source_registry.py` touches only `knowledge/`. `research_seam.py` touches only `knowledge/research/requests/`. Neither writes into `.project/` or `work/`, which is how the two-PM rule is kept: the join lives in the shared knowledge base.

## Required Invariants

- No byte is written under `knowledge/sources/` before the content holdout scan passes.
- Every `knowledge/sources/<slug>/` created by the operation has exactly one manifest row and exactly one index block; `verify` asserts this repo-wide.
- `source_id` recomputed from the raw artifact equals the frontmatter hash, or nothing is committed.
- Every seam-profile index block has non-empty `Use for`, `Validation`, `Caveat`, and a `Source URL` or local origin.
- Every registered source's `Location` is a repo-relative path that resolves (MR-4).
- No return artifact exists without a run record; no `BOUNDED_NEGATIVE` return exists without a negative file under its request key.
- No repo artifact — record, test fixture, or return — contains barred ARIES-CS design or cost text; matches are reported as rule id, count and offsets (R-D4).

## Component Overview

- **`scripts/source_registry.py`** — the registration operation and its CLI (`register`, `verify`). Owns staging, capture invocation, provenance verification, dedupe, commit/rollback, and both writer profiles. The single door into `knowledge/sources/`.
- **`scripts/holdout_guard.py`** — the barred set. Parses the `### Barred` bullets of `knowledge/holdout/aries-cs/PROTOCOL.md` into repo paths at load time and fails closed if that section cannot be parsed (a PROTOCOL edit that breaks the parse stops registrations rather than silently un-barring). Carries the term list — `aries-cs`, `aries cs`, `ariescs`, `aries.ucsd.edu`, and the four sealed-paper stems — matched case-insensitively against URL, title, `output.md` and the raw artifact. A term hit is never adjudicated in code: it returns `OPERATOR_QUEUE`. An owner may re-run with `--holdout-ack "<reason>"`, which is recorded in the run record and appended to the block's `Caveat`; the ack is refused outright for the sealed-paper paths and for barred-path destinations. Applied at the registry boundary for *every* caller, which is stricter than PROTOCOL §2's demo-session scope and deliberately so: a registered source is readable by every later session.
- **`scripts/zotero_lib.py` (extended)** — manifest row schema, key-tolerant loaders (`load_manifest` keyed by `source_id`, with a `zotero_key` index preserved for the existing dedupe), manifest truncation helper. Existing constants, `slugify`, `sha256_of` unchanged.
- **`scripts/zotero_ingest.py` (extended)** — `append_source_index_entry` gains `source_url`/`origin`, `use_for`, `validation`, `caveat`, `source_kind` and the profile switch, with the anchor fixed per D4. `process_zotero_item` and `process_local_pdf` become callers of `source_registry.register`; the local-PDF path thereby gets its manifest row (R-B1a).
- **`scripts/research_seam.py`** — request schema and validation, request-key derivation, negative lookup/write/reopen, run record (`run.jsonl` + `process_log.md`), capture counting, return emission and class check.
- **`.claude/commands/research-acquire.md`** — the acquisition protocol: bounded request in; search → triage → capture → register → close; WebFetch is triage-only and never quoted or cited; no DI is minted (R-C3), and the owner's `/research` approval gate is where insights are still made (R-C4).
- **`knowledge/research/requests/`** — `<request-id>.json` (requests), `negatives/<request-key>.json`, `runs/<request-id>/<utc-stamp>/{run.jsonl,process_log.md,return.json}`.
- **`docs/research_seam_operator_guide.md`** — R-E6 operator documentation: forming a request, invoking both entry points, reading the four return classes, and the two operator actions.

Request and return shapes, kept minimal (R-A1, R-A4):

```jsonc
// request
{"request_id","question","consumer","gap_type","priority","where_to_look":[],
 "limits":{"max_searches":N,"max_captures":N}}
// return
{"request_id","run","class":"REGISTERED|BOUNDED_NEGATIVE|OPERATOR_QUEUE|BLOCKER",
 "registered":[{"slug","path","source_id"}],"queued":[{"candidate","reason"}],
 "negative":"<path>","limit_reached":"max_captures|max_searches|null","reason"}
```

## Non-Goals

- Re-registering a *changed* source. A URL whose bytes differ from an existing row is refused as a duplicate naming the existing entry; supersession is an epic non-goal (`pm supersede-insight` is an upstream stub).
- Scoring extraction quality. A cookie wall over 100 characters still "extracts"; judging that stays with the triaging agent, which queues a poor extraction for the operator.
- Enforcing search counts in code (D7), live-network proof (Item 5), DI minting (R-C3), Zotero push, paywall bypass.
- Crash-recovery machinery for the commit sequence (D6).

## Implementation Notes

- Registry paths must be injectable. `zotero_lib` defines `SOURCES_DIR` etc. as CWD-relative `Path` constants; tests need a temp tree without `chdir`. Add a small paths object defaulting to those constants and thread it through the new code; do **not** change the constants themselves (other callers read them).
- `load_manifest`/`manifest_keys` currently raise `KeyError` on a row without `zotero_key`. Make them key-tolerant *before* writing any non-Zotero row, or the first seam registration breaks Zotero ingestion.
- Staging must be on the same filesystem as `knowledge/sources/` for `os.rename` to be atomic — hence `knowledge/.staging/`, gitignored, not `/tmp`.
- Reuse the flatten logic rather than re-deriving it (`zotero_ingest.py:158-180`); it already handles the "several subdirs during re-extraction" case.
- The PDF pipeline loads table-detection weights and takes ~15 s per document even at `--budget 0`; mark the PDF chain test slow.
- Nothing may pass `--index`/`--summarize` (D11).

## Potential Risks

- **Term-list blindness (B3).** A source carrying ARIES-CS design data without a matching term registers cleanly. Mitigation: the path bar is exact and parsed from PROTOCOL.md; the triaging agent is still instructed to check; the failure is disclosed in the operator guide rather than papered over.
- **PROTOCOL.md parse fragility.** A reformatting of §3 stops all registrations. That is the intended direction of failure, and a test pins the expected parse result so the break surfaces in CI rather than at a write.
- **Breaking `--local-pdf` (D5).** Existing muscle memory for that flag now errors without the three metadata flags. Mitigation: the error names the missing flags; the operator guide covers it.
- **Concurrent runs** corrupting the index read-modify-write. Mitigated by the commit lock; two seam runs simply serialize.
- **Dynamic pages defeating hash dedupe (B1).** Bounded by the pre-fetch URL check; a same-document-different-bytes case surfaces as a refused duplicate rather than a silent second entry.

## Integration Strategy

The Zotero batch path keeps its behaviour and becomes a caller of the shared writer, so `SOURCE_INDEX.md` entries written before today stay valid and Zotero-key dedupe keeps working (R-B1c). `/research` is untouched; `/research-acquire` is the acquiring sibling and hands finished research documents to `/research`'s existing approval flow, where DIs are minted as they are today. The run record is the P5-style instrumented evidence the H2 probe asked for, produced at no extra cost.

Two upstream filings are made during implementation and listed as deliverables (R-F1): the `approve-research` empty-insight-list refusal (`pm/operations.py:664-668`), and a request that `extract` expose a `--register` hook or return a provenance JSON — the latter now with the concrete asymmetries this design had to work around (flat vs nested output, `--save-source` writing no `raw.pdf` on the local-PDF path, no `file://` support).

## Validation Approach

New suite `tests/research/`, with `conftest.py` providing `local_site` (threaded `http.server` on `127.0.0.1:0` over `tests/research/fixtures/web/`) and `knowledge_tree` (a temp registry tree: minimal `SOURCE_INDEX.md` with the real headings, empty `MANIFEST.jsonl`).

| Requirement | Test | Shape |
|---|---|---|
| R-E2 (URL chain) | `test_register_url_chain.py` | fixture URL → real `extract` → holdout → commit; asserts source dir, one manifest row with `source_id`, one index block with all four required fields, `Location` resolves |
| R-E2 (PDF chain) | `test_register_pdf_chain.py` | generated fixture PDF, same assertions plus the `knowledge/raw/` copy and the flattened layout; marked slow |
| R-E3 (duplicate) | `test_duplicate.py` | second registration of the same URL and of the same bytes at a different URL; no second row, no second block |
| R-E3 (rollback) | `test_rollback.py` | index write forced to fail; asserts no source dir, no row, manifest byte-identical |
| R-E3 (barred) | `test_holdout.py` | barred URL, barred title, and a fixture page containing a **synthetic** marker; asserts nothing under `knowledge/sources/`, the matched rule id recorded, and that no fixture or record contains real ARIES-CS content |
| R-E3/R-D5/R-D6 (negative) | `test_negative.py` | adequate zero-source run writes the negative; a second `open` on the same request refuses; `--override-reason` proceeds and appends to `reopened[]` |
| R-A3/R-A4/R-A5 | `test_return_contract.py` | each class emitted and checked against disk; a claimed `REGISTERED` with nothing on disk is rejected; a capture-limit run names `max_captures` |
| R-E5 | `test_zotero_path_contract.py` | **characterization test written before the refactor** — the Zotero and local-PDF paths' index/manifest output, pinned so the extension cannot change them silently. There is no existing regression to protect this; `tests/test_dependency_provenance.py` (the pin) is the only other affected suite. |

SC9 is verified by a non-author walking `docs/research_seam_operator_guide.md` and performing both operator actions; that walk happens at `/_my_audit`, not here.

## Next-Stage Handoff

- **Fixed:** the four return classes and their disk checks; `source_id` = raw-bytes SHA-256; the commit order and failure ladder; one write door; the loopback fixture.
- **Open for the plan:** exact field names in the manifest row and the request JSON; whether `verify` ships in the first build or as a follow-on task; the wording of the operator guide.
- **De-risk first:** the `zotero_lib` loader change plus the characterization test, before any non-Zotero row exists. Everything else builds on a manifest that both readers can still read.

---

## Appendix A — ADR candidate (R-F2)

To be filed into the ADR home Item 1 establishes, at coordination time; this item does not create that home.

**Title:** Non-Zotero source identity is the raw-bytes SHA-256.
**Grade:** `[AGENT]`, delegated by the owner at Align (`align.md:8`, "make sure you use your judgement").
**Context:** `MANIFEST.jsonl` was keyed on `zotero_key`, so a URL source had no durable identity and duplicates could not be detected (spec R-B3).
**Decision:** `source_id = sha256(raw source bytes)`, taken from the extraction frontmatter and re-verified against the raw artifact on disk. Dedupe: `zotero_key` → `source_id` → `source_url` (pre-fetch only). `zotero_key` remains for Zotero rows.
**Consequences:** identity is recomputable from the repository with no service call, which is what lets the whole chain be proven offline; a re-fetch whose bytes changed is refused as a duplicate rather than superseded; manifest readers must tolerate rows without `zotero_key`.
**Rejected:** URL-derived key (no identity for local PDFs; redirects and mirrors); push-through-Zotero (network and manual step inside an offline-provable path).

---

**Next Step:** After approval → `/_my_design_review` in a fresh session, then `/_my_plan`.
