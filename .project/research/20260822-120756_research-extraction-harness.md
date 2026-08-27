---
date: 2026-08-22T12:07:56-07:00
researcher: Claude
topic: "Research-and-extraction harness — closing the study → model-update loop with source acquisition"
tags: [research, harness, knowledge-management, source-acquisition, run-study, modeling-pm, agentic-mbse]
status: complete
last_updated: 2026-08-22
---

# Research: Research-and-extraction harness — closing the study → model-update loop

**Date**: 2026-08-22 12:07 PDT
**Researcher**: Claude
**Research Type**: Architecture / Integration

## Research Question

We have working entry points for three functions: updating the model (`work/` modeling PM), generating the executable (sysml-codegen), and running studies (`run-study`). The missing piece is research and extraction: when an agent reads a study result against the model and finds it needs information that is not in the repo, it should be able to fetch that information (directly or by triggering another agent), process it into the knowledge base, and carry it back into a model update. What tools, scripts, and agents do we already have for research? Where are the gaps? What existing patterns can the harness reuse?

## Summary

- **The loop has already run once, by hand.** Item 6 (run-study first consumer) found the model had no conductor-field limit and four arm values with no source. That became WI-030 (model change) and WI-031 (research round), which produced DI-007..010 and two new registered sources, then the package was regenerated and the study resumes on named keys. Every hop exists; none of the hops is mechanized, and each one used a different artifact shape to say "I need information."
- **We have one autonomous search → triage → extract loop, and it is locked inside the concept-analysis pipeline.** `exploration/concept_analysis/scripts/lib/research.py` plus `prompt_templates/research.md` is a complete, budgeted, logged acquisition agent with a good protocol (WebFetch is triage only; `add-source` is the only writer; filesystem diff is truth). It is scoped to one concept's data-gap table and writes only into `knowledge/concept_research/`. Nothing equivalent exists for the modeling PM.
- **The primitive is solid; the registration step is missing.** `agentic-mbse extract <url|pdf> --save-source` gives sanitized markdown with a content hash and raw artifacts. But no script or pm op turns that into a `knowledge/sources/` entry plus a `SOURCE_INDEX.md` block plus a manifest row. WI-031 did this in bash and hand-wrote the index entries; the manifest has no slot for a non-Zotero source. `/manage-sources` only edits the index; `/research` only reads.
- **Back-propagation is a stub.** `pm supersede-insight` raises `NotImplementedError`, and `pm impact-query` never fills `affected_work_items`. So when new information contradicts an existing insight, nothing mechanically says which model elements or work items are affected.
- **Feasible, and mostly assembly.** The harness needs four small pieces: a `register-source` operation (URL/PDF → extract → sources dir → index + manifest), one shared "research request" artifact shape used by study records, design docs, and `/research`, an acquisition mode for `/research` built from the concept-analysis protocol, and the supersession/impact ops that already have an upstream design. The study record's §15 findings router with its `Home` column is the natural join point, and the WI-016 process log is the instrumentation format the H2 hypothesis probe asked for.

## Detailed Findings

### 1. The three loops and how they join today

Each loop is closed on its own terms. The join between them is the thing this research is about.

**Study loop** (`.claude/skills/run-study/SKILL.md`, `runbook.md`, `modeling_project/STUDY_POLICY.md`)
- Fifteen execute steps plus an administer (synthesize) sequence. Tools: `scripts/study/indicators.py`, `preflight.py`, `verify.py`, the package oracle, and the study's own `study.py` on stock teax.
- The record has seventeen fixed headings (`record-template.md:16-18`). Three of them carry "the model needs to change" or "we lack information":
  - §8 "Model-development findings" table, one row per `no_constraint_response` axis: `| Axis | What should push back and is not modeled | Finding id |` (`record-template.md:133-138`). The owner's ruling does not discharge it.
  - §15 Findings: `| Id | Kind | Finding | Disposition | Home |`, with `Kind = model | process` and `Home ∈ {tool, runbook step, policy rule, skill, modeling item, research round, documented seam, unrouted}` (`record-template.md:206-216`). Mirrored into the append-only `DISCOVERY_LOG.md` (`runbook.md:288-300`).
  - §17 "What this record does not contain", and the synthesis's mandatory "What the record does not support" (`runbook.md:266-268`).
- The record points back at the model by value through `studies/manifest.json` (`study-package-manifest/v1`): package path, three fingerprints, an objective catalog of qualified channel names, the baseline point, and per-arm entry-model maps. Constraints are always named by `constraint_id` + `source_local_identity`.
- Policy constraints that bind acquisition: no unsourced bounds, record the gap instead (`STUDY_POLICY.md:43`, anti-pattern 6 at `:104`); holdout seal on ARIES-CS material; indicators inform but never gate.

**Model-update loop** (`.claude/commands/spec-model.md` → `design-model.md` → `plan-model.md` → `implement-model.md`, `backlog.md`)
- `pm add-item` creates the BACKLOG row; `/spec-model` writes `work/active/WI-XXX_*/spec.md` and SV rows in `VALIDATION_MATRIX.md`; `/implement-model` writes `models/**/*.sysml`, calls `pm trace-element`, `pm add-insight`, `pm promote-requirement`; `pm close-item` archives.
- Where the lifecycle goes looking for sources: `/spec-model` reads `SOURCE_INDEX.md` and says "If sources aren't specified, stop and ask" (`spec-model.md:36, :119`). `/design-model` dispatches research agents over SOURCE_INDEX codebases and "Web search for physics, material properties, standards not covered by configured sources" (`design-model.md:57-58`), and offers "Need more data → use `/research`" (`:85`). `/implement-model` does not look for sources; it consumes what design recorded.
- The citation pattern WI-030 used is the one to preserve: the same file:line or image reference appears in the approved research doc, the SysML doc comment `Ref`, and the `traceability_matrix.csv` `Source_Location` column, with the matrix `Requirement` column closing back to the spec's MR (`models/library/analyses/mfe_plasma_scaling.sysml:257-289`, `data/traceability_matrix.csv:50-52`).

**Codegen loop**
- `uv run sysml-codegen generate --models exploration/stellarator_e2e/models --output exploration/stellarator_e2e/generated --overwrite --smart-regen --preserve-handwritten` (WI-030 `plan.md:130, :151`), then snapshot and census recapture, then `tests/models/test_model_family_spines.py` byte-identity checks, `preflight.py gates`, `verify.py` on the re-pinned manifest.
- Pins enforced by `tests/test_dependency_provenance.py:12-35`.
- Resume contract back to the study is concrete: Item 6 Phase 3 restarts only when `model_contract.json` resolves the six new entry names and `peak_field_ok` as a constraint id (`run-study-first-consumer/plan.md:177`).

**The one manual trace of the join.** Read in order:
1. Owner align: "I want the design stage to actually do some research here … and it may require new modeling" (`.project/active/run-study-first-consumer/align.md:17-19`).
2. Coding-PM research doc named the gap: `.project/research/20260821-141439_item6-ab-candidates.md`. The model has no conductor-field-limit constraint, and the Nb3Sn and sCO2 arms need values with no in-repo source.
3. `design.md` Appendix A arm tables carry a `source` column per value; the unsourced cells are the request (`design.md:188-220`).
4. Two modeling-PM items minted by `pm add-item`: WI-030 (model) and WI-031 (research). WI-031's spec body is a `| value | consumer | what is needed | where to look first |` table (`work/completed/20260822_WI-031_research-round-item6-values/spec.md:16-21`).
5. `/research` produced `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md`. Two of its four findings ended "citation pending ingestion".
6. The ingestion was done the same day by an agent in bash: `agentic-mbse extract` on two URLs straight into `knowledge/sources/iter_cryoplant_iter_org/` and `knowledge/sources/eu_demo_rw_tf_coil_conductor_dematte_bruzzone/`, with SOURCE_INDEX blocks written by hand (`knowledge/SOURCE_INDEX.md:190-218`, Caveat lines say "not through Zotero; no Zotero key"). `MANIFEST.jsonl` still has 11 rows. DI-007..010 appended.
7. WI-030 regenerated the package; Item 6 resumes when the contract resolves the new names.

So the handoff artifacts, in order, were: align prose → coding research doc → design table with a source column → WI-031 spec table → approved research doc → SOURCE_INDEX block + DI. Five shapes for one message: "I need a value, here is who consumes it, here is where to look."

### 2. Inventory: what we have for research and extraction

| Asset | Where | What it does | Writes to | Scope limit |
|---|---|---|---|---|
| `/research` (modeling PM) | `.claude/commands/research.md` → agentic-mbse | Read SOURCE_INDEX, KNOWLEDGE, OVERVIEW; research via subagents and WebSearch/WebFetch; `pm save-research`; user approves; `pm approve-research` appends DI-XXX | `knowledge/research/pending|approved/`, `KNOWLEDGE.md` | Reads sources; never extracts or registers one. No warning that WebFetch returns a paraphrase. |
| `/_my_research` (coding PM) | `~/.claude/commands/_my_research.md` | Codebase/feasibility research | `.project/research/` | No approval gate, no DI, no source registration |
| `/manage-sources` | `.claude/commands/manage-sources.md` | Conversational add/remove/view of SOURCE_INDEX entries; `ls` check; optional settings permission | `SOURCE_INDEX.md` | Edits the index only; no fetch, hash, manifest, or extended metadata |
| `agentic-mbse extract <url|pdf>` | `~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py:196-285` | HEAD-classifies URL; HTML → sanitize → trafilatura (arXiv → pandoc); PDF → pipeline. Frontmatter `source, source_type, extracted_at, content_hash_sha256, backend`. `--save-source` keeps `raw.html`/`raw.pdf`. `--urls-from` batch. | any `--output` dir | Hash is of raw bytes, not output. No retries, no JS, 30 s timeout. Login walls >100 chars "succeed". No per-URL provenance in batch mode. |
| `run_analysis.py add-source <concept> <url|pdf>` | `exploration/concept_analysis/scripts/run_analysis.py:980-1075` | Slugify, dedupe across iterations, extract with `--save-source`, flatten, symlink `name.md → name/output.md`, rollback on failure | `knowledge/concept_research/<id>/iter-NN/sources/` | Concept-scoped placement |
| `analyze --research` research step | `scripts/lib/research.py:22-117`, `prompt_templates/research.md` | Agent reads analysis §6 data gaps (`not-yet-sourced` only), WebSearch ≤5, WebFetch triage only, `add-source` ≤3, writes `research_output.json`; orchestrator diffs `find_sources()` before/after and appends `research_log.json` | concept research dir, per-concept log | Only callable inside the analysis loop; gap table is prose; budgets are prompt text, not enforced |
| source-integration step | `scripts/lib/loop.py:1037-1116`, `prompt_templates/source_integration.md` | One subagent per new source; material deltas only; shared feedback schema `VERDICT` + `### F-N` blocks | `iter-N/source_integration_output.md` → next analyze pass | Feedback vocabulary is analysis-specific |
| `resurface_orig.py` | `exploration/concept_analysis/scripts/resurface_orig.py` | Same agent pattern applied to re-sourcing paraphrased files; outcome enum `success|fail_js|fail_404|fail_paywall|fail_timeout|duplicate|skipped` | per-file report + `summary.json` | One-off tool |
| `zotero_ingest.py` | `scripts/zotero_ingest.py` | Zotero diff → download → extract → `append_source_index_entry` (`:210-251`) → `append_manifest_entry`. `--local-pdf` does the same minus manifest (`:474-528`) | `knowledge/raw/`, `knowledge/sources/<slug>/`, `SOURCE_INDEX.md`, `MANIFEST.jsonl` | No URL input; manifest keyed on `zotero_key` (`zotero_lib.py:25-36`); index writer hardcodes `Type: documentation` and leaves `Use for`/`Validation` blank |
| `concept-research-navigation` skill | `.claude/skills/concept-research-navigation/SKILL.md` | How to read and trust existing research: quality tiers, image inspection, authority hierarchy | — | Teaches consumption, not acquisition |
| `source-traceability` skill | symlink to agentic-mbse | The DI → PR → element → doc-comment chain, SOURCE_INDEX format, citation patterns | — | Teaches citation, not acquisition |
| `memory-handler` agent + `memory/*.md` | `.claude/agents/memory-handler.md`, `scripts/lib/memory.py` | Tag-matched notes injected into analyze prompts | `exploration/concept_analysis/memory/` | Not read by the research step; negative search results live only in `research_log.json` |
| `record-learning` skill | `work/learnings/RAW_LEARNINGS.md` | Append-only modeling learnings | `RAW_LEARNINGS.md` | Modeling syntax/patterns, not domain facts |
| `orchestrate-stage.sh` | `~/.claude/scripts/orchestrate-stage.sh` | Run or resume one `/_my_*` stage as a headless `claude -p` subagent; returns `{session_id, result, cost, is_error}` | `.orchestrate-logs/` | Coding PM stages only, by name |
| `pm save-research / approve-research / add-insight / trace-element / impact-query` | `~/1cfe/agentic-mbse/src/agentic_mbse/pm/operations.py` | Research file lifecycle, DI append, matrix rows, DI→element lookup | `knowledge/research/`, `KNOWLEDGE.md`, `traceability_matrix.csv` | `approve-research` refuses an empty insight list (`:664-668`); `impact_query.affected_work_items` always `[]` (`:855`) |
| `pm supersede-insight` | `operations.py:1189-1208` | Raises `NotImplementedError` | — | Designed in agentic-mbse `workflows.md § 6.1` (`.project/concepts/architecture-redesign/workflows.md:560-618`), not built |

### 3. The knowledge chain and where it breaks

```
external web / PDF
   │  (a) no registration path for a URL
   ▼
knowledge/sources/<slug>/output.md  ──►  SOURCE_INDEX.md  (+ MANIFEST.jsonl, Zotero only)
   │
   │  /research reads; writes pending → approved
   ▼
KNOWLEDGE.md DI-XXX
   │  pm promote-requirement
   ▼
REQUIREMENTS.md PR-XXX
   │  pm trace-element
   ▼
traceability_matrix.csv  ──►  model element doc comment  ──►  generated package  ──►  study record
   ▲                                                                                   │
   │  (b) supersede-insight stub; impact_query has no work items                       │
   └──────────────── (c) §15 Home = "research round" is prose, nothing consumes it ─────┘
```

- **(a) Acquisition to registry.** `extract` produces everything an index entry needs (URL, raw hash, output path) but nothing writes the entry. `append_source_index_entry` exists only inside `zotero_ingest.py`, takes `pdf_sha256` and `item_key`, and has no field for a URL. The WI-031 entries were hand-written and are richer than the script would produce (they fill `Use for`, `Validation`, `Caveat`, and the `Source URL` line). Prior research already flagged this: "should extract auto-register in SOURCE_INDEX" is open question 2 in `.project/research/20260203-knowledge-database-architecture.md:747`, and the risk "SOURCE_INDEX becoming stale if sources added without registering" is at `:695`.
- **(b) Registry back to model.** `workflows.md § 6.1` specifies supersession: mark old DI superseded, assign new, query the matrix, write `knowledge/research/impacts/DI-XXX_superseded.md`, prompt for a work item. Upstream backlog item ITEM-PM-STUBS-001 (`~/1cfe/agentic-mbse/.project/backlog/BACKLOG.md:181-193`, P2, Ready) covers it. Until then, new information that contradicts a DI is handled by hand, and `DI-006`'s four-month digit corruption (`HYPOTHESIS_DOSSIER.md`, H1 limits) shows what an unchecked summary layer costs.
- **(c) Study to research.** §15's `Home` column can say `research round`, and `DISCOVERY_LOG.md` indexes it, but nothing reads either. The request that actually reached `/research` was WI-031's hand-written spec table.

### 4. Gaps, stated plainly

1. **No URL/PDF → `knowledge/sources/` + `SOURCE_INDEX.md` + manifest operation.** Closest pieces: `process_local_pdf` (`zotero_ingest.py:474-528`) and `add-source` (`run_analysis.py:980-1075`). Neither is reachable from `/research`.
2. **No shared "research request" artifact.** The same message was carried as align prose, a coding research doc, a design table column, a WI spec table, and a record §15 row. The concept-analysis pipeline has the closest thing to a schema (`output_template.md:170-176`: `| # | Gap Description | Section | Gap Type | Criticality | Source Recommendation |`, types `truly-unknown | proprietary | not-yet-sourced | derivable`), but it is markdown read by an LLM; there is no parser.
3. **`/research` cannot acquire.** It has WebSearch and WebFetch, no `extract` step, no registration step, and does not warn that WebFetch output is a Haiku paraphrase that must never be cited (the rule the concept-analysis prompt states three times, `research.md:56-58, :102`). The 2026-03-28 feasibility research recommended updating research prompts to use extract instead of WebFetch (`20260328-source-capture-pipeline-feasibility.md:336`); done for concept analysis, not for `/research`.
4. **Supersession and impact are stubs** (above).
5. **`approve-research` refuses zero insights** (`operations.py:664-668`); the WI-030 report was moved to `approved/` by hand. Already logged in CURRENT_WORK as an owed upstream filing.
6. **No holdout enforcement on acquisition.** PROTOCOL.md bars specific paths and any artifact carrying ARIES-CS design or cost data (`knowledge/holdout/aries-cs/PROTOCOL.md:27, :31-44, :56`). The WI-031 agent checked by string count ("0 ARIES-CS mentions") by hand. An acquisition step that writes into `knowledge/sources/` needs a blocklist check on the URL/title and on the fetched content before registration.
7. **Negative results do not travel.** "Searched X, found nothing" lives in a per-concept `research_log.json` that only the next research step in that concept reads, and `--force` deletes it. The modeling PM has no equivalent at all; WI-031's "Search-snippet only (not fetched)" list is prose in the approved doc.
8. **Research budgets are prompt text.** `max_searches`/`max_extractions` are enforced only by the agent obeying the prompt (`research.py:60-61`, `research.md:107-108`).
9. **Extraction quality is not checked.** `metrics.json` holds structural counts only; a cookie wall over 100 chars extracts "successfully" (`web_backend.py:423-440`). The concept-analysis protocol compensates with a quality hierarchy and a news-site allow list in the prompt.

### 5. Patterns available to reuse

**P1. The research-step contract** (`research.py`, `research.md`). Transferable as-is: template variables in; `gaps_attempted[] {gap_id, queries[], candidates[{url,title,triage,notes}], extracted[], failed[{url,reason}], status: closed|partial|failed|skipped}` out; append-only log rendered back as "prior attempts, don't retry CLOSED/FAILED"; filesystem diff before/after as the only truth about what was acquired; the agent's JSON is advisory. Specific and replaceable: the `add-source` CLI shape, the concept handle, the fusion site list.

**P2. The triage protocol** (`research.md:38-110`). WebFetch for accessibility and relevance only; one URL per extract call; never write a source by hand; dedupe by domain+title; peer-reviewed > government report > institutional page > press release > news; JS-heavy company sites → reliably extractable trade press.

**P3. The findings router** (`record-template.md:206-216`). `| Id | Kind | Finding | Disposition | Home |` with a closed `Home` vocabulary and `unrouted` as a stated state. A harness can consume rows whose `Home` is `research round` or `modeling item`, keyed by `<study-id>#<n>`, and `DISCOVERY_LOG.md` is already the cross-study index.

**P4. The request table** (WI-031 spec, `design.md` Appendix A). `| value | consumer | what is needed | where to look first |`. This is the human-shaped version of P1's gap row. One schema could serve both.

**P5. The instrumented process log** (`work/completed/20260705_WI-016_h2-blind-derivation/process_log.md`). Three sections: firewall events, a numbered search/consultation record (`| # | Action | What it contributed |`, dead ends marked), judgment calls. The meta-review's recommendation 7 asks for exactly this: "the agent research loop instrumented (what was searched, what was found, where the human intervened). The deliverable is as much the process record as the model" (`.project/research/20260704-120000_pipeline-hypothesis-meta-review.md:108`). P1's `research_output.json` is the machine form; P5 is the readable form.

**P6. The citation invariant** (WI-030). Same reference in research doc, doc comment `Ref`, and matrix `Source_Location`; matrix `Requirement` closes to the MR. Any acquired source must be able to land in this chain, which means it needs a repo-relative path under `knowledge/sources/` (MR-4: `Source` MUST be a file path, `REQUIREMENTS.md:54`).

**P7. Headless stage dispatch** (`orchestrate-stage.sh`). Compose prompt, run `claude -p`, return `{session_id, result}`; orchestrator keeps judgment. The concept-analysis loop does the same with `invoke_claude_validated` and retries (`lib/claude.py:299-336`). Either can run a research step as "trigger another agent".

**P8. Feedback schema** (`prompt_templates/config/feedback_format.md`). `VERDICT: PASS|FINDINGS` then ≤3 `### F-N` blocks with `Target`, `Category`, `Finding`, `Recommendation`, `Priority`. The source-integration step uses it to say "these new sources materially change the analysis". A modeling-PM equivalent would say "these new sources materially change DI-XXX / element Y".

**P9. Registry writer** (`zotero_ingest.py:210-251`). `append_source_index_entry(title, slug, item_key, pdf_sha256, extract_sha256)` inserts before `## How MBSE Commands Use This File`. Extend rather than replace: add `source_url`, `source_kind`, and `use_for`/`validation` text, and a manifest row keyed on URL hash when there is no Zotero key.

**P10. Resume contract by contract.** Item 6's Phase 3 gate is "the regenerated `model_contract.json` resolves these names" (`plan.md:177`). The harness can use the same test to know when a research → model → regenerate cycle has actually landed.

## Code References

- `.claude/skills/run-study/record-template.md:133-138, :206-216` — §8 model-development findings and §15 findings router
- `.claude/skills/run-study/runbook.md:215-227, :288-300` — findings register step, `DISCOVERY_LOG.md`
- `modeling_project/STUDY_POLICY.md:43, :104` — no-fallbacks rule
- `.project/active/run-study-first-consumer/align.md:17-26`, `design.md:188-220`, `plan.md:177` — the manual trace and the resume gate
- `work/completed/20260822_WI-031_research-round-item6-values/spec.md:16-21` — the request table
- `knowledge/research/approved/20260821-165616_wi031-item6-second-arm-values.md` — "citation pending ingestion" and the post-approval ingest note (line 148)
- `knowledge/SOURCE_INDEX.md:190-218` — the two hand-written URL-source entries
- `exploration/concept_analysis/scripts/lib/research.py:22-117, :120-204` — research step, log, prior-attempts rendering
- `exploration/concept_analysis/prompt_templates/research.md:38-110, :120-174` — protocol and output JSON
- `exploration/concept_analysis/prompt_templates/output_template.md:170-176` — gap inventory schema
- `exploration/concept_analysis/scripts/lib/loop.py:128-213, :1037-1116` — producer dispatch, source-integration
- `exploration/concept_analysis/scripts/run_analysis.py:980-1075` — `add-source`
- `scripts/zotero_ingest.py:210-251, :474-528` — `append_source_index_entry`, `process_local_pdf`
- `scripts/zotero_lib.py:25-36, :52-63` — manifest keyed on `zotero_key`
- `~/1cfe/agentic-mbse/src/agentic_mbse/cli/extract_cli.py:196-285` — URL routing; `extraction/web_backend.py:177-192, :397-440`; `extraction/html_sanitize.py:89-150`; `extraction/frontmatter.py:22-57`
- `~/1cfe/agentic-mbse/src/agentic_mbse/pm/operations.py:337, :638-727, :810-861, :1189-1208` — save/approve research, impact query, supersede stub
- `~/1cfe/agentic-mbse/.project/concepts/architecture-redesign/workflows.md:560-682` — supersession and inline-capture design
- `~/1cfe/agentic-mbse/.project/backlog/BACKLOG.md:181-193` — ITEM-PM-STUBS-001
- `~/1cfe/agentic-mbse/.project/concepts/resilient-document-ingestion.md` — draft concept: DOI/arXiv discovery, per-document provenance JSON, triage report (no backlog item)
- `work/completed/20260705_WI-016_h2-blind-derivation/process_log.md` — instrumented research loop record
- `modeling_project/HYPOTHESIS_DOSSIER.md` H2; `.project/research/20260704-120000_pipeline-hypothesis-meta-review.md:27-34, :104-108` — H2 status and the instrumented-probe recommendation
- `knowledge/holdout/aries-cs/PROTOCOL.md:27, :31-44, :56, :80` — acquisition constraints
- `~/.claude/scripts/orchestrate-stage.sh` — headless stage runner
- `.project/research/20260328-source-capture-pipeline-feasibility.md:326-350`, `20260203-knowledge-database-architecture.md:695, :747` — prior recommendations still open

## Architecture Insights

- **Two PM systems, one knowledge base.** The study and codegen loops are coding-PM (`.project/`); model updates and `/research` are modeling-PM (`work/`, `knowledge/`). CLAUDE.md forbids cross-referencing their state, but the knowledge base is shared ground. The join should live in `knowledge/` artifacts and `pm` operations, not in either PM's state files.
- **Every existing loop treats the filesystem as truth and the agent's report as advisory.** The research step diffs `find_sources()`; the study loop pins fingerprints and refuses dirty packages; the spines test byte-compares generated trees. A research harness should keep that: the registration op reports what landed on disk, and the index entry is derived from the extraction artifacts, not from what the agent says it fetched.
- **The gap row is the unit of work.** Concept analysis, the WI-031 spec, and the design table all converge on the same five fields: what value, who consumes it, what kind of gap, priority, where to look. The harness's contract is that row plus an outcome enum.
- **H2 is the hypothesis this serves.** The meta-review found the research → model derivation step "is not tested by any planned work" and is "the bottleneck that determines whether 13 concepts is months or years" (`:85`). The dossier rates H2 "substantially validated, one family, one probe". A harness that records what was searched, what was found, what was registered, and what changed in the model is the instrument that probe needs.
- **Holdout is a first-class constraint, not an afterthought.** The seal applies to stellarator-demo research sessions. Any acquisition path that can write into `knowledge/sources/` needs the blocklist in code, because the escalation path PROTOCOL.md names is a PreToolUse deny hook (`:80`), which will not see a `curl` inside a script.

## Feasibility Assessment

Feasible, and mostly assembly of pieces that exist. Ordered by leverage:

1. **`register-source` operation** (fusion-tea script or agentic-mbse pm op). Input: URL or local PDF, title, `use_for`, optional `validation`/`caveat`. Does: holdout check on URL/title → `agentic-mbse extract --save-source --output knowledge/sources/<slug>/` → holdout check on content → hash `output.md` → index block with Source URL, raw/extract SHA256, `Use for`, `Validation`, `Caveat` → manifest row keyed on URL hash. Extends `append_source_index_entry`; mirrors `add-source`'s dedupe, flatten, rollback. Small: under a day.
2. **Research request schema.** One JSON or markdown-table shape carrying `{id, value_or_question, consumer (study-id#n | WI-XXX | element), gap_type, priority, where_to_look, status, outcome}`. Emitted by the study record's §15 rows with `Home = research round` and by `design.md` source columns; consumed by `/research`; answered by DI ids and registered source paths. Also small, but it needs an owner ruling on where the canonical file lives (see Open Questions).
3. **`/research` acquisition mode.** Take the P1/P2 protocol from `prompt_templates/research.md`, replace `add-source` with `register-source`, add the WebFetch-is-triage-only rule, write a `research_output.json` beside the pending doc, and append a P5-style process log section to the report. The existing `/research` approval flow stays as the human gate.
4. **Supersession and impact.** Upstream ITEM-PM-STUBS-001. Without it the harness can register and insert but not mechanically find what an updated value invalidates.
5. **Dispatch.** Either `orchestrate-stage.sh` pattern or the concept-analysis `invoke_claude_validated` pattern can run the research step headless from a study administer or a design session. Not on the critical path; the first version can be a skill an agent invokes interactively.

Risks: extraction quality on non-arXiv HTML (the upstream epic dropped that scope at close); cost per extraction ($5–50 per the concept-analysis README); holdout leakage if the blocklist is incomplete; prompt-enforced budgets. All known, none blocking.

## Recommendations

1. **Build `register-source` first.** It removes the hand step WI-031 had to do and gives `/research`, `/design-model`, and future study administers one door into `knowledge/sources/`. Keep the hand-written WI-031 entries as the referent for what a good index block contains.
2. **Adopt one research-request row** and put it in the three places it already almost exists: §15 of the study record, the design doc's arm tables, and the `/research` intake. Don't add a fourth PM state file.
3. **Fork `/research` into a fusion-tea command** (or wrap the upstream one) with acquisition mode, rather than editing the symlinked upstream command in place. Upstream can absorb it later.
4. **Instrument from day one.** Every run writes the P1 JSON and a P5 process log. That record is the H2 evidence the meta-review asked for, at no extra cost.
5. **File two upstream items now**: the `approve-research` empty-list refusal, and a note that `extract` should have a `--register` or return a provenance JSON (`resilient-document-ingestion.md` already sketches it).
6. **Defer dispatch automation.** Prove the loop interactively on the next Item 6 gap, then wire `orchestrate-stage.sh` or a `run_research_step` port.

Suggested next stage: `/_my_spec` for the harness with items 1–3 in scope and 4–6 as explicit non-goals.

## Open Questions

1. **Where does the canonical research-request list live?** Options: only inside the artifacts that emit it (study record §15, design table) with `/research` reading them by path; or a single `knowledge/research/requests/` queue. The first respects the two-PM separation; the second makes the harness easier to drive headless.
2. **Manifest identity for non-Zotero sources.** `MANIFEST.jsonl` is keyed on `zotero_key`. Use the raw content hash? Or push every URL source into Zotero first so the existing pipeline owns it? The second keeps one ledger but adds a manual step back.
3. **Holdout check depth.** Title/URL blocklist is cheap; content scan for ARIES-CS design or cost data is a judgment call the agent makes today by string count. What is the minimum the harness must do in code before a write to `knowledge/sources/`?
4. **Should `/research` acquisition be allowed to mint a DI in the same run**, or must registration and insight approval stay two owner gates? Today they are two gates; the WI-031 ingest-then-DI sequence suggests the owner wants to see the source before the insight.
5. **Budget enforcement.** Keep budgets as prompt text (current) or enforce in the dispatcher by counting `register-source` calls? The latter needs the dispatcher to own the tool.
