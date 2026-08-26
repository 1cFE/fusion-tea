# Spec: Native Research Acquisition and Registration Seam

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-08-25
**Complexity:** MEDIUM
**Branch:** `feat/goal-research-seam`
**Epic:** Goal Strategy and Task Harness (GSTH), Item 2

---

## Problem

Research is the one hop in the model-development loop that has no callable boundary. Everything on either side of it does: modeling has the `work/` PM, generation has sysml-codegen, studies have the run-study skill. Research has a reading command (`/research`), an extraction primitive (`agentic-mbse extract`), and a Zotero-shaped registry writer — and nothing that joins them.

The loop has already run this hop by hand, once. WI-031 needed four unsourced arm values. An agent ran `agentic-mbse extract` on two URLs in bash, wrote the `SOURCE_INDEX.md` blocks by hand (`knowledge/SOURCE_INDEX.md:190-218`), left `MANIFEST.jsonl` untouched because it has no slot for a non-Zotero source, and checked the ARIES-CS holdout by counting strings. Two findings in the approved research doc sat at "citation pending ingestion" until that manual pass closed them.

What is missing, stated plainly (`.project/research/20260822-120756_research-extraction-harness.md` §4):

- **No URL → registry operation.** `agentic-mbse extract` produces everything an index entry needs — source URL, raw hash, output path — and nothing writes the entry. `append_source_index_entry` (`scripts/zotero_ingest.py:210-251`) exists only inside the Zotero script, takes a Zotero item key, has no field for a URL, hardcodes `Type: documentation`, and leaves `Use for` and `Validation` blank.
- **No durable identity for a non-Zotero source.** `MANIFEST.jsonl` is keyed on `zotero_key` (`scripts/zotero_lib.py:25-36`). A URL source cannot be recorded, so duplicates cannot be detected.
- **No holdout enforcement in code.** The ARIES-CS protocol bars specific paths and any artifact carrying ARIES-CS design or cost data (`knowledge/holdout/aries-cs/PROTOCOL.md:27, :31-44, :56`). The escalation path it names is a PreToolUse deny hook (`:80`), which cannot see a `curl` or an `extract` call inside a script. Any path that writes into `knowledge/sources/` has to carry the blocklist itself.
- **Negative results do not travel.** "Searched, found nothing" lives in a per-concept `research_log.json` that only the same concept's next research step reads. The modeling PM has no equivalent, so the same fruitless search can be repeated silently.
- **`/research` cannot acquire.** It has WebSearch and WebFetch, no capture step, no registration step, and no warning that WebFetch output is a lossy paraphrase that must never be cited as source content.

**Why now.** `[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Native seams]` The goal layer this epic is building invokes `research` as a seam — question and limits in, registered sources or a bounded negative out — and the concept-design states explicitly that a goal round may not silently absorb this repair. `[INHERITED: .project/concepts/goal-driven-model-development-harness.md § Success Criteria 4]` The governing obligation is that when a disposition is "research round," the agent ends with each source registered: citable under MR-4 by repo path, carrying enough provenance to re-fetch and verify it, holdout-checked before it was written; no hand-written index entries remain in the path; an unfetchable source is queued for the operator with a reason; a search that finds nothing is recorded as a negative result.

## Success Criteria

- [ ] A URL and a local PDF each register through one operation into a citable repo path carrying source URL (or local origin), raw hash, extract hash, manifest identity, and a complete index block — with no hand-written `SOURCE_INDEX.md` step anywhere in the path.
- [ ] Re-registering an already-registered source is detected as a duplicate and produces no second registry entry.
- [ ] A registration that fails partway leaves no partial state: no orphan `knowledge/sources/` directory, no index block, no manifest row.
- [ ] A barred URL, title, or content case writes nothing under `knowledge/sources/` and records which rule matched, or the operator-queue outcome.
- [ ] An adequate search that finds no usable source returns a durable bounded negative recording the queries run and the candidates attempted, in a form a later request for the same thing can read before repeating it.
- [ ] The research entry surface consumes the bounded request and emits exactly one of the four return classes, with native references, while the owner's research-approval gate stays where it is and no DI is minted by acquisition.
- [ ] A duplicate, a rollback, a barred write, and a bounded negative are each proven by a test that needs no network; focused registration/acquisition tests and the affected knowledge-pipeline regressions pass.
- [ ] A non-builder can operate the seam from its own documentation: form a request, invoke it, read each of the four return classes, and act on a queued source or a bounded negative.

## Known Requirements

### A. Request and return contract

- **[INHERITED: `.project/research/20260822-120756_research-extraction-harness.md` §4.2, §5 P4; epic Item 2 scope 1]** **R-A1** — One bounded request shape carries, at minimum: a request id, the value or question sought, the consumer (study finding `<study-id>#<n>`, `WI-XXX`, model element, or design/spec reference), the gap type, the priority, and where to look first. The same shape serves a study record's §15 row, a design table's unsourced cell, and a hand-written intake.
- **[INHERITED: `goal-strategy-task-harness-design.md` § Native seams]** **R-A2** — The request also carries the source/search limits for the invocation, so an invocation that hits a limit ends inside the contract rather than by exhaustion.
- **[INHERITED: `goal-strategy-task-harness-design.md` § Native seams; `goal-driven-model-development-harness.md` § Research stage]** **R-A3** — Every invocation ends in exactly one of four return classes: registered sources, bounded negative, operator queue, or blocker.
- **[INFERRED]** **R-A4** — Every return resolves to native references — repo-relative paths, DI/WI ids, or request ids — not prose alone. A reader must be able to reach the evidence from the return without reconstructing what the agent did.
- **[INFERRED]** **R-A5** — When a return is bounded by a declared limit rather than by exhausting the search, the return names which limit was reached.

### B. Registration operation

- **[INHERITED: epic Item 2 scope 2]** **R-B1** — Registration extends the existing source-index writer (`scripts/zotero_ingest.py:210-251`, `scripts/zotero_lib.py`). No second registry implementation, and the Zotero path keeps working unchanged.
- **[HARD]** **R-B2** — Every registered source is citable under MR-4: `Source` resolves to a repo-relative file path (`modeling_project/REQUIREMENTS.md:49, :54`). A registration that cannot produce such a path is not a registration.
- **[NEED]** **R-B3** — Every registered source carries a durable manifest identity, including sources that never passed through Zotero, and that identity is sufficient to detect a duplicate before a second entry is written. `[OWNER 2026-08-25]` The mechanism — content hash, URL key, or push-through-Zotero — is deliberately left to design (`align.md:8`).
- **[INHERITED: epic Item 2 scope 2; `align.md:14` `[AGENT]`]** **R-B4** — The operation registers both a URL and a local PDF, and capture uses `agentic-mbse extract <url|pdf> --save-source` as it stands. `agentic-mbse` is pinned by SHA and the pin is test-enforced (`tests/test_dependency_provenance.py`), so a needed change there is an upstream filing, not an in-repo edit.
- **[INHERITED: epic Item 2 scope 2]** **R-B5** — The registered entry records provenance sufficient to re-fetch and verify: source URL or local origin, raw artifact hash, extract hash, extracted path, and date added.
- **[REFERENT: `knowledge/SOURCE_INDEX.md:190-218`]** **R-B6** — The two hand-written WI-031 entries are the bar for what an index block contains. They are richer than the current script's output: they fill `Use for` with what the source establishes and which RQ it serves, `Validation` with how to check its numbers, `Caveat` with what limits its authority, and they carry a `Source URL` line. Registration produces blocks of that quality; a generated block with `Use for` and `Validation` blank does not meet this requirement.
- **[INHERITED: `goal-driven-model-development-harness.md` § Success Criteria 4]** **R-B7** — Registration is atomic against its own artifacts: a failure at any step leaves no partial source directory, index block, or manifest row. `run_analysis.py add-source` (`exploration/concept_analysis/scripts/run_analysis.py:980-1075`) already does dedupe-flatten-rollback for the concept-research tree and is the working referent.
- **[INFERRED]** **R-B8** — What landed on disk is the truth of what was registered; the acquiring agent's self-report is advisory. Every existing loop in this repo already works this way (`research.py` diffs `find_sources()`; the study loop pins fingerprints).

### C. Acquisition mode

- **[INHERITED: epic Item 2 scope 3]** **R-C1** — A fusion-tea-owned research entry surface runs search → triage → capture → holdout check → register against a bounded request. `[AGENT, strong default]` The research doc recommends forking or wrapping `/research` rather than editing the symlinked upstream command (`recommendation 3`); the upstream command is tool-owned and must not be edited in place.
- **[HARD]** **R-C2** — WebFetch output is triage-only: it establishes accessibility and relevance and is never registered, quoted, or cited as source content. It passes through a summarizer and is lossy (`exploration/concept_analysis/prompt_templates/research.md:56-58, :102`).
- **[OWNER 2026-08-25]** **R-C3** — Registration and insight approval are separate operations with an explicit approval gate between them. Acquisition may register a source; it must not mint a DI. This is not a session boundary: an approved DI may follow later in the same broader workflow through the native research-approval operation (`align.md:9`).
- **[INHERITED: epic Item 2 scope 3]** **R-C4** — The owner's existing research approval gate stays exactly where it is (research document, then insights).
- **[INHERITED: research doc §5 P1/P5; epic Item 2 scope 4]** **R-C5** — Each invocation writes an instrumented record of what was searched, what was triaged and with what decision, what was captured, what failed and why, and what was queued. This record is the input to R-D3 and the readable evidence a reviewer checks.

### D. Safety and negative evidence

- **[HARD]** **R-D1** — The holdout blocklist is enforced by the operation itself, at two points: URL and title before capture, and content before any write into `knowledge/sources/`. A PreToolUse hook cannot see a fetch inside a script (`knowledge/holdout/aries-cs/PROTOCOL.md:80`), so code is the only enforcement that binds. The barred set is the sealed papers, the barred artifacts in §3, and the principle that any artifact carrying ARIES-CS-specific design or cost data is inadmissible while sealed (`:27`).
- **[INHERITED: `goal-driven-model-development-harness.md` § Success Criteria 4]** **R-D2** — A barred case writes nothing into `knowledge/sources/` and records the matched rule. A source that cannot be fetched is queued for the operator with the reason, and a queued source stays outside the registry.
- **[HARD]** **R-D2a** — The record of a barred match, and any test fixture standing in for one, names the rule that matched and never copies barred ARIES-CS design or cost content into a repo artifact. The derived-artifact rule bars referencing sealed or barred content anywhere (`knowledge/holdout/aries-cs/PROTOCOL.md:56`); a bibliographic reference to a barred path is not data (`:27`).
- **[NEED]** **R-D3** — A search that finds nothing usable produces a durable bounded negative that records, at minimum: the request it answers, the queries run, the candidates seen with their triage dispositions, the failures with reasons, and why the search is considered adequate (exhausted or limit-reached). Durable means a later invocation against the same request can read it before searching, so the same fruitless search is not silently repeated. `[INHERITED: goal-driven-model-development-harness.md § Research stage]` A recorded negative is a legitimate result that re-routes the finding, not a failure to retry.

### E. Verification

- **[NEED]** **R-E1** — A duplicate, a failed registration and its rollback, a barred write, and a bounded negative are each provable by a test that needs no network. Fixtures and local files stand in for live capture; live network acquisition proof belongs to epic Item 5 (`align.md:13`).
- **[INHERITED: project testing preference]** **R-E2** — Tests exercise the failure chain across the seam boundary — request in, holdout check, capture, registry write, return out — rather than isolated happy paths of each function.
- **[INFERRED]** **R-E3** — The affected knowledge-pipeline regressions (the Zotero ingest path and anything reading `SOURCE_INDEX.md` / `MANIFEST.jsonl`) still pass, since R-B1 extends a live writer.
- **[INHERITED: epic Item 2 deliverables]** **R-E4** — Operator documentation for this seam ships with it: enough for a non-builder to form a bounded request, invoke the seam, read each of the four return classes, and act on a queued source or a bounded negative. This is the seam's own operating documentation; the loop-wide operator document (`GOAL_RUNBOOK.md`) belongs to Item 1.

## Non-Goals

From the epic's Item 2 out-of-scope list:

- Insight supersession and work-item impact propagation (`pm supersede-insight` / `impact-query`). These are upstream stubs (ITEM-PM-STUBS-001); without them, new information that contradicts a DI is still handled by hand.
- Paywall bypass, Zotero workflow redesign, cross-concept source sharing, and automated research approval.
- Goal-layer routing, dispatch, or shadow copies of research state. This item builds the seam; the goal layer that calls it is Items 1, 4, and 5.

Also out of scope here:

- Live-network acquisition proof — epic Item 5 owns it.
- Edits inside pinned `agentic-mbse`. A needed change there is an upstream filing.
- `CLAUDE.md`, the run-study runbook, `DISCOVERY_LOG.md`, `GOAL_RUNBOOK.md`, and the ADR home. Item 1 owns those files and runs concurrently on another branch (`align.md:15`).
- Reserved gates beyond the standing defaults. `[OWNER 2026-08-25]` The DI gate (R-C3) is the only one this item adds; merge/push and item close stay owner-held; final quality is on the orchestrator (`align.md:10`).

## Open Questions / Deferred to design

- **Manifest identity mechanism** — content hash of the raw artifact, a URL-derived key, or pushing every URL source through Zotero first. Deliberately deferred by the owner (`align.md:8`). Whatever design picks must satisfy R-B3.
- **Where the entry surface lives** — fusion-tea command, skill, or script, and how it relates to the symlinked upstream `/research`.
- **Where the request and return artifacts live, and in what format.** The research doc's open question 1: only inside the artifacts that emit a request (study record §15, design table), or a single queue directory. The first respects the two-PM separation; the second is easier to drive headless. This also decides where the R-D3 negative record lives and how a later invocation finds it.
- **Holdout content-scan mechanics** — the minimum check in code before a write. Today the check is a hand string count. Research doc open question 3.
- **Rollback implementation** — staging directory, transactional write order, or compensating delete, and how far the guarantee extends across the three artifacts (source dir, index, manifest).
- **Limit enforcement** — whether search/capture limits (R-A2) are prompt text as they are today (`research.py:60-61`) or counted by the surface that owns the capture call. Research doc open question 5.
- **Negative-result lifetime** — whether a bounded negative expires or is re-openable when the request's premise changes, and what a caller must do to legitimately re-run a search that previously returned nothing.
- **Slug and title derivation** for URL sources, and how a collision resolves against `resolve_slug` (`scripts/zotero_ingest.py`).

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2
- **Align:** `.project/active/goal-research-seam/align.md` — owner rulings, 2026-08-25
- **Required Reading:**
  - `.project/research/20260822-120756_research-extraction-harness.md` — inventory, gaps §4, reusable patterns §5
  - `.project/concepts/goal-strategy-task-harness-design.md` § Native seams
  - `.project/concepts/goal-driven-model-development-harness.md` § Research stage, § Success Criteria 4
  - `scripts/zotero_ingest.py`, `scripts/zotero_lib.py` — the writer to extend, manifest identity today
  - `exploration/concept_analysis/scripts/lib/research.py`, `exploration/concept_analysis/prompt_templates/research.md` — acquisition protocol referent
  - `modeling_project/REQUIREMENTS.md` MR-4; `knowledge/holdout/aries-cs/PROTOCOL.md`
  - `knowledge/SOURCE_INDEX.md:190-218` — index-block referent
- **Product-lens:** `.project/active/goal-research-seam/product-lens.md`
- **Design:** `.project/active/goal-research-seam/design.md` (to be created)

---

**Next Steps:** After approval, proceed to `/_my_spec_review`, then `/_my_design`.
