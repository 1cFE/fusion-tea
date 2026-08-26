# Spec: Native Research Acquisition and Registration Seam

**Status:** Draft (revised after spec review, 2026-08-25)
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
- **The existing writer has two defects of its own**, both verified in this repo:
  - The local-PDF path registers an index entry but writes **no manifest row at all**. `append_manifest_entry` is called only from the Zotero path (`scripts/zotero_ingest.py:437`); `process_local_pdf` calls only `append_source_index_entry` (`:521`).
  - The index insertion anchor does not exist. `append_source_index_entry` inserts before `## How MBSE Commands Use This File` (`:239`); that heading is absent from `knowledge/SOURCE_INDEX.md`, so every call today takes the fallback branch, prints a warning, and appends at end of file — after the `## How Sources Are Used` section.
- **No holdout enforcement in code.** The ARIES-CS protocol bars specific paths and any artifact carrying ARIES-CS design or cost data (`knowledge/holdout/aries-cs/PROTOCOL.md:27, :31-44, :56`). The escalation path it names is a PreToolUse deny hook (`:80`), which cannot see a `curl` or an `extract` call inside a script. Any path that writes into `knowledge/sources/` has to carry the blocklist itself.
- **Negative results do not travel.** "Searched, found nothing" lives in a per-concept `research_log.json` that only the same concept's next research step reads. The modeling PM has no equivalent, so the same fruitless search can be repeated silently.
- **`/research` cannot acquire.** It has WebSearch and WebFetch, no capture step, no registration step, and no warning that WebFetch output is a lossy paraphrase that must never be cited as source content.

**Why now.** `[INHERITED: .project/concepts/goal-strategy-task-harness-design.md § Native seams]` The goal layer this epic is building invokes `research` as a seam — question and limits in, registered sources or a bounded negative out — and the concept-design states explicitly that a goal round may not silently absorb this repair. `[INHERITED: .project/concepts/goal-driven-model-development-harness.md § Success Criteria 4]` The governing obligation is that when a disposition is "research round," the agent ends with each source registered: citable under MR-4 by repo path, carrying enough provenance to re-fetch and verify it, holdout-checked before it was written; no hand-written index entries remain in the path; an unfetchable source is queued for the operator with a reason; a search that finds nothing is recorded as a negative result.

## The four return classes

Every invocation of the seam ends in exactly one of these. They are named across the epic, the concept-design, and the requirements below, so they are defined once here.

| Class | Meaning | Decided when |
|---|---|---|
| **REGISTERED** | One or more sources were captured and registered. The request is answered as far as this invocation goes. | At least one source completed capture → holdout check → registry write, and the return can name its repo path. |
| **BOUNDED_NEGATIVE** | The search ran and found nothing usable. This is a real answer, not a failure. | The search was adequate — exhausted the guidance or hit a declared limit (R-A2) — and produced no source that passed triage and holdout. |
| **OPERATOR_QUEUE** | A source was identified but could not be brought in by the seam. The work moves to a human. | A specific candidate is named and capture is blocked on something a human must resolve: paywall, login wall, repeated fetch failure, an extraction too poor to register, or a holdout judgment the code will not make on its own. |
| **BLOCKER** | The seam itself could not proceed. Nothing about the search is established. | A precondition, tooling, or contract failure: the request is malformed or missing required fields, the capture tool is unavailable or fails outside the candidate's control, the registry is not writable, or the return cannot satisfy MR-4. |

The boundary that matters: **operator queue is about a source, blocker is about the seam.** If a named candidate exists and the obstacle is that candidate's accessibility or admissibility, it is `OPERATOR_QUEUE`. If the invocation could not get far enough to say anything about any candidate, it is `BLOCKER`. A queued source is a routable outcome that preserves the request; a blocker means the request has not been attempted.

`REGISTERED` and `OPERATOR_QUEUE` can both arise in one invocation that handled several candidates. `[INFERRED]` When they do, the invocation returns `REGISTERED` and carries the queued candidates inside its return, because the request was advanced; a return of `OPERATOR_QUEUE` means nothing was registered.

## Success Criteria

- [ ] **SC1** — A URL and a local PDF each register through one operation into a citable repo path carrying source URL (or local origin), raw hash, extract hash, manifest identity, and a complete index block — with no hand-written `SOURCE_INDEX.md` step anywhere in the path.
- [ ] **SC2** — The registration operation is callable on its own, by an operator or by another surface (a design session, a study administer), not only from inside the research entry surface.
- [ ] **SC3** — Re-registering an already-registered source is detected as a duplicate and produces no second registry entry.
- [ ] **SC4** — A registration that fails partway leaves no partial state: no orphan `knowledge/sources/` directory, no index block, no manifest row.
- [ ] **SC5** — A barred URL, title, or content case writes nothing under `knowledge/sources/` and records which rule matched, or the operator-queue outcome.
- [ ] **SC6** — An adequate search that finds no usable source returns a durable bounded negative recording the queries run and the candidates attempted, and a later invocation against that same request surfaces the prior negative instead of silently re-searching.
- [ ] **SC7** — The research entry surface consumes the bounded request and emits exactly one of the four return classes, with native references, while the owner's research-approval gate stays where it is and no DI is minted by acquisition.
- [ ] **SC8** — The whole capture → holdout → register chain is proven end-to-end offline, for both a URL input and a local PDF input, against fixtures rather than the live network. A duplicate, a rollback, a barred write, and a bounded negative are each proven the same way. Focused registration/acquisition tests and the affected knowledge-pipeline regressions pass.
- [ ] **SC9** `[INHERITED: epic Item 2 deliverables]` — A non-author walks the seam's operator documentation and can, from it alone, form a bounded request, invoke the operation, identify which of the four return classes came back, and act on a queued source and on a bounded negative.

## Known Requirements

### A. Request and return contract

- **[INHERITED: `.project/research/20260822-120756_research-extraction-harness.md` §4.2, §5 P4; epic Item 2 scope 1]** **R-A1** — One bounded request shape carries, at minimum: a request id, the value or question sought, the consumer (study finding `<study-id>#<n>`, `WI-XXX`, model element, or design/spec reference), the gap type, the priority, and where to look first. The same shape serves a study record's §15 row, a design table's unsourced cell, and a hand-written intake.
- **[INHERITED: `goal-strategy-task-harness-design.md` § Native seams]** **R-A2** — The request also carries the source/search limits for the invocation, so an invocation that hits a limit ends inside the contract rather than by exhaustion.
- **[INHERITED: `goal-strategy-task-harness-design.md` § Native seams; `goal-driven-model-development-harness.md` § Research stage]** **R-A3** — Every invocation ends in exactly one of the four return classes defined above, and the class is decidable from those definitions without a judgment call the spec has not made.
- **[INFERRED]** **R-A4** — Every return resolves to native references — repo-relative paths, DI/WI ids, or request ids — not prose alone. A reader must be able to reach the evidence from the return without reconstructing what the agent did.
- **[INFERRED]** **R-A5** — When a return is bounded by a declared limit rather than by exhausting the search, the return names which limit was reached.

### B. Registration operation

- **[INHERITED: `goal-driven-model-development-harness.md:90` US-7 ("As a research agent **or an operator**, I can register a URL or PDF with one command"); research doc rec 1]** **R-B0** — Registration is a standalone operation with its own entry point. An operator, a design session, or a study administer can call it directly; the research entry surface (R-C1) is one caller among several, not the only door into `knowledge/sources/`.
- **[INHERITED: epic Item 2 scope 2]** **R-B1** — Registration extends the existing source-index writer (`scripts/zotero_ingest.py:210-251`, `scripts/zotero_lib.py`); there is no second registry implementation. The extension takes an explicit position on each of the two verified defects in that writer:
  - **R-B1a** `[INFERRED]` — Every source registered through the operation, local PDF included, gets a manifest row. The local-PDF path writes none today (`zotero_ingest.py:521` vs `:437`); leaving that as-is would violate R-B3.
  - **R-B1b** `[INFERRED]` — The index insertion anchor is either fixed or its current append-at-end behavior is adopted deliberately and recorded. What is not acceptable is inheriting a warning-emitting fallback as if it were the design.
  - **R-B1c** `[INHERITED: epic Item 2 scope 2]` — The Zotero path's *behavioral contract* is preserved: existing `SOURCE_INDEX.md` entries stay valid, Zotero-key dedupe keeps working, and its regressions keep passing. "Extend, don't duplicate" binds the contract, not the defects.
- **[HARD]** **R-B2** — Every registered source is citable under MR-4: `Source` resolves to a repo-relative file path (`modeling_project/REQUIREMENTS.md:49, :54`). A registration that cannot produce such a path is not a registration.
- **[INHERITED: epic Item 2 scope 2 and epic SC1]** **R-B3** — Every registered source carries a durable manifest identity, including sources that never passed through Zotero, and that identity is sufficient to detect a duplicate before a second entry is written. The *mechanism* — content hash, URL key, or push-through-Zotero — is deliberately deferred to design `[OWNER 2026-08-25]` (`align.md:8`); the requirement itself is inherited from the epic, not owner-originated.
- **[INHERITED: epic Item 2 scope 2; `align.md:14` `[AGENT]`]** **R-B4** — The operation registers both a URL and a local PDF, and capture uses `agentic-mbse extract <url|pdf> --save-source` as it stands. `agentic-mbse` is pinned by SHA and the pin is test-enforced (`tests/test_dependency_provenance.py`), so a needed change there is an upstream filing, not an in-repo edit. `[INFERRED]` The two input kinds are not symmetric: for a URL, `--save-source` writes the fetched raw artifact; for a local PDF there is no fetch and the raw artifact is the input file, which the existing path handles by copying into `knowledge/raw/` and hashing there (`zotero_ingest.py:489-499`). R-B5's raw hash must be satisfiable both ways.
- **[INHERITED: epic Item 2 scope 2]** **R-B5** — The registered entry records provenance sufficient to re-fetch and verify: source URL or local origin, raw artifact hash, extract hash, extracted path, and date added.
- **[INHERITED: research doc rec 1] [REFERENT: `knowledge/SOURCE_INDEX.md:190-218`]** **R-B6** — A registered index block has `Use for`, `Validation`, `Caveat`, and `Source URL` (or local origin) present and non-empty. That is the checkable bar. The two hand-written WI-031 entries are the referent for what those fields should say — `Use for` names what the source establishes and which RQ it serves, `Validation` says how to check its numbers, `Caveat` says what limits its authority — but the test asserts presence, not prose quality.
- **[INFERRED]** **R-B7** — The caller supplies `Use for`, `Validation`, and `Caveat` at registration time, drawn from the request (R-A1) and from the triage and instrumented record (R-C5). The request shape does not have to carry them, and registration does not invent them.
- **[INHERITED: `goal-driven-model-development-harness.md` § Success Criteria 4]** **R-B8** — Registration is atomic against its own artifacts: a failure at any step leaves no partial source directory, index block, or manifest row. `run_analysis.py add-source` (`exploration/concept_analysis/scripts/run_analysis.py:980-1075`) already does dedupe-flatten-rollback for the concept-research tree and is the working referent.
- **[INFERRED]** **R-B9** — What landed on disk is the truth of what was registered; the acquiring agent's self-report is advisory. Every existing loop in this repo already works this way (`research.py` diffs `find_sources()`; the study loop pins fingerprints).

### C. Acquisition mode

- **[INHERITED: epic Item 2 scope 3]** **R-C1** — A fusion-tea-owned research entry surface runs search → triage → capture → holdout check → register against a bounded request, calling the R-B0 operation rather than reimplementing it. `[AGENT, strong default]` The research doc recommends forking or wrapping `/research` rather than editing the symlinked upstream command (`recommendation 3`); the upstream command is tool-owned and must not be edited in place.
- **[HARD]** **R-C2** — WebFetch output is triage-only: it establishes accessibility and relevance and is never registered, quoted, or cited as source content. It passes through a summarizer and is lossy (`exploration/concept_analysis/prompt_templates/research.md:56-58, :102`).
- **[NEED]** **R-C3** — Registration and insight approval are separate operations with an explicit approval gate between them. Acquisition may register a source; it must not mint a DI. `[OWNER 2026-08-25]` "Acquisition may register sources but must not automatically mint DIs. This does not require a separate session or goal round: an approved DI may be created later in the same broader workflow through the native research-approval operation" (`align.md:9`).
- **[INHERITED: epic Item 2 scope 3]** **R-C4** — The owner's existing research approval gate stays exactly where it is (research document, then insights).
- **[INHERITED: research doc §5 P1/P5; epic Item 2 scope 4]** **R-C5** — Each invocation writes an instrumented record of what was searched, what was triaged and with what decision, what was captured, what failed and why, and what was queued. This record is the input to R-D5 and R-B7, and the readable evidence a reviewer checks.

### D. Safety and negative evidence

- **[HARD]** **R-D1** — Holdout enforcement lives in the operation's own code. A PreToolUse hook cannot see a fetch inside a script (`knowledge/holdout/aries-cs/PROTOCOL.md:80`), so code is the only enforcement that binds a path writing into `knowledge/sources/`. The barred set is the sealed papers, the barred artifacts in §3, and the principle that any artifact carrying ARIES-CS-specific design or cost data is inadmissible while sealed (`:27`).
- **[INHERITED: epic Item 2 scope 4]** **R-D2** — Enforcement happens at two points: URL and title before capture, and content before any registry write. This structure is the epic's, and is challengeable on evidence — the requirement it serves is R-D1.
- **[INHERITED: `goal-driven-model-development-harness.md` § Success Criteria 4]** **R-D3** — A barred case writes nothing into `knowledge/sources/` and records the matched rule. A source that cannot be fetched is queued for the operator with the reason, and a queued source stays outside the registry.
- **[HARD]** **R-D4** — The record of a barred match, and any test fixture standing in for one, names the rule that matched and never copies barred ARIES-CS design or cost content into a repo artifact. The derived-artifact rule bars referencing sealed or barred content anywhere (`knowledge/holdout/aries-cs/PROTOCOL.md:56`); a bibliographic reference to a barred path is not data (`:27`).
- **[INHERITED: `goal-driven-model-development-harness.md` § Research stage]** **R-D5** — A search that finds nothing usable produces a durable bounded negative recording, at minimum: the request it answers, the queries run, the candidates seen with their triage dispositions, the failures with reasons, and why the search is considered adequate (exhausted or limit-reached).
- **[INHERITED: `goal-driven-model-development-harness.md:114`]** **R-D6** — A recorded negative **blocks** a silent repeat. An invocation whose request matches a recorded negative surfaces that prior result and does not re-search unless the caller supplies an explicit override reason, which is recorded with the new attempt. Reading the prior negative is not optional and not advisory.

### E. Verification

- **[INFERRED — basis: `align.md:13`, an orchestrator reading recorded as `[AGENT]`, unchallenged]** **R-E1** — The seam is provable without network access. Fixtures — a fixture URL or captured HTML/PDF injected at the capture boundary, and a local file — stand in for live fetching. Live *network* acquisition proof belongs to epic Item 5; the capture → holdout → register chain itself is proven here.
- **[NEED]** **R-E2** — The offline proof covers the whole chain for both input kinds, not just its failure modes: a fixture URL input and a local PDF input each run extract → holdout check → registry write and produce a citable, hashed, manifest-identified entry. SC1 is verified inside this item.
- **[INFERRED]** **R-E3** — A duplicate, a failed registration and its rollback, a barred write, and a bounded negative are each provable offline as well.
- **[INFERRED]** **R-E4** — Tests exercise the failure chain across the seam boundary — request in, holdout check, capture, registry write, return out — rather than isolated happy paths of each function. (The project's stated preference; no repo artifact states it, so this is an inference, not an inheritance.)
- **[INFERRED]** **R-E5** — The affected knowledge-pipeline regressions (the Zotero ingest path and anything reading `SOURCE_INDEX.md` / `MANIFEST.jsonl`) still pass, per R-B1c.
- **[INHERITED: epic Item 2 deliverables]** **R-E6** — Operator documentation for this seam ships with it, covering request formation, invocation of both the standalone operation and the research surface, all four return classes, and the two operator actions (act on a queued source; act on a bounded negative). Verified by SC9: a non-author walks it.

### F. Deliverable homes

- **[INHERITED: research doc rec 5]** **R-F1** — The two upstream `agentic-mbse` filings this work depends on are made during implementation and listed as deliverables: the `approve-research` empty-insight-list refusal (`pm/operations.py:664-668`), and a request that `extract` expose a `--register` hook or return a provenance JSON. Filing them is this item's job; the upstream fix is not.
- **[INHERITED: `align.md:15`]** **R-F2** — This item's durable decisions — the R-B3 manifest identity above all — are filed as architecture records in the ADR home Item 1 establishes. The coordination happens at design time; this item does not create or edit that home itself.

## Non-Goals

From the epic's Item 2 out-of-scope list:

- Insight supersession and work-item impact propagation (`pm supersede-insight` / `impact-query`). These are upstream stubs (ITEM-PM-STUBS-001); without them, new information that contradicts a DI is still handled by hand.
- Paywall bypass, Zotero workflow redesign, cross-concept source sharing, and automated research approval.
- Goal-layer routing, dispatch, or shadow copies of research state. This item builds the seam; the goal layer that calls it is Items 1, 4, and 5.

Also out of scope here:

- Live-network acquisition proof — epic Item 5 owns it. Everything else about the chain is proven offline in this item (R-E2).
- Edits inside pinned `agentic-mbse`. A needed change there is an upstream filing (R-F1).
- `CLAUDE.md`, the run-study runbook, `DISCOVERY_LOG.md`, `GOAL_RUNBOOK.md`, and the ADR home. Item 1 owns those files and runs concurrently on another branch (`align.md:15`).
- Reserved gates beyond the standing defaults `[NEED]`. The DI gate (R-C3) is the only one this item adds; merge/push and item close stay owner-held; final quality is on the orchestrator (`align.md:10`).

**Decision record — no research critic in this item.** The concept lists a research critic checking provenance, holdout disclosure, paraphrase, and insight conflicts (`goal-driven-model-development-harness.md:114, :136`). It is deliberately not part of Item 2. The concept-design's review topology replaced per-stage critics with one lightweight fresh non-author checkpoint plus the end-of-round review, both owned by Item 1, and the epic's resolution of `epic-plan-F2` states plainly that this "is not a critic at every native stage." The substance of three of the four lenses is carried mechanically here instead — R-C2 (no paraphrase), R-D1 (code-enforced holdout), R-B2 (MR-4 path) — and the fourth, conflict with existing insights, sits behind the untouched DI approval gate (R-C3, R-C4).

## Open Questions / Deferred to design

- **Manifest identity mechanism** — content hash of the raw artifact, a URL-derived key, or pushing every URL source through Zotero first. Deliberately deferred by the owner (`align.md:8`). Whatever design picks must satisfy R-B3 and lands as an ADR per R-F2.
- **The index insertion anchor** — whether R-B1b fixes the missing `## How MBSE Commands Use This File` marker, adds a real anchor, or adopts append-at-end. The requirement is that design decide it, not that it be fixed.
- **Where the entry surface lives** — fusion-tea command, skill, or script, and how it relates to the symlinked upstream `/research`. Separately, what shape the standalone R-B0 entry point takes.
- **Where the request and return artifacts live, and in what format.** The research doc's open question 1: only inside the artifacts that emit a request (study record §15, design table), or a single queue directory. The first respects the two-PM separation; the second is easier to drive headless. This also decides where the R-D5 negative record lives and how R-D6's match lookup finds it.
- **Holdout content-scan mechanics** — the minimum check in code before a write. Today the check is a hand string count. Research doc open question 3.
- **Rollback implementation** — staging directory, transactional write order, or compensating delete, and how far the guarantee extends across the three artifacts (source dir, index, manifest).
- **Limit enforcement** — whether search/capture limits (R-A2) are prompt text as they are today (`research.py:60-61`) or counted by the surface that owns the capture call. Research doc open question 5.
- **Negative-result lifetime** — whether a bounded negative expires or is re-openable when the request's premise changes, and what counts as an adequate R-D6 override reason.
- **Fixture shape for the offline proof** — loopback HTTP server, captured raw artifact injected at the capture boundary, or a stubbed capture step. R-E2 sets the bar; the mechanism is design's.
- **Slug and title derivation** for URL sources, and how a collision resolves against `resolve_slug` (`scripts/zotero_ingest.py`).

---

## Related Artifacts

- **Epic:** `.project/backlog/epic_goal_strategy_task_harness.md` § Item 2
- **Align:** `.project/active/goal-research-seam/align.md` — owner rulings, 2026-08-25
- **Spec review:** `.project/active/goal-research-seam/spec-review.md` — verdict Revise, 2026-08-25; this revision addresses it
- **Required Reading:**
  - `.project/research/20260822-120756_research-extraction-harness.md` — inventory, gaps §4, reusable patterns §5
  - `.project/concepts/goal-strategy-task-harness-design.md` § Native seams
  - `.project/concepts/goal-driven-model-development-harness.md` § Research stage, § Success Criteria 4, US-7
  - `scripts/zotero_ingest.py`, `scripts/zotero_lib.py` — the writer to extend, manifest identity today
  - `exploration/concept_analysis/scripts/lib/research.py`, `exploration/concept_analysis/prompt_templates/research.md` — acquisition protocol referent
  - `modeling_project/REQUIREMENTS.md` MR-4; `knowledge/holdout/aries-cs/PROTOCOL.md`
  - `knowledge/SOURCE_INDEX.md:190-218` — index-block referent
- **Product-lens:** `.project/active/goal-research-seam/product-lens.md`
- **Design:** `.project/active/goal-research-seam/design.md` (to be created)

---

**Next Steps:** Record resolutions in `spec-review.md`, then proceed to `/_my_design`.
