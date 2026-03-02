# Epic: Full Workflow Demo — Clean-Slate Fusion TEA

**Epic ID**: DEMO
**Status**: Draft
**Priority**: P0
**Created**: 2026-03-01
**Estimated Effort**: TBD (pending decomposition)

---

## Executive Summary

Initiate a broad investigation of fusion technologies for techno-economic analysis, using the full agentic-mbse workflow from scratch. This serves a dual purpose: it produces the real analytical foundation for comparing fusion approaches on cost, and it creates a documented trail demonstrating how the toolchain works end-to-end.

The workflow arc: define investigation scope → build domain frameworks (taxonomy/ontology) → ingest literature → research sources → plan first modeling exercise → build models → track on dashboard → visualize results. Each step codifies knowledge in durable, committed artifacts.

**Critical Success Factor**: Someone could follow the committed artifacts from this epic and understand both the fusion domain structure AND how to reproduce the workflow on a different domain.

---

## Why This Epic?

### Current State

- agentic-mbse has two major unreleased changes:
  - **Validation stack restructure** (8→6 levels, `valstack-cleanup` branch)
  - **PDF extraction pipeline v4** (`doc-ingest-clean` branch — 8-step orchestration, quality gates, ensemble table detection)
- fusion-tea's ingestion automation (`zotero_ingest.py`) was built against the old extraction interface — needs re-validation
- Existing modeling work (solar+battery, coffee maker) was de-risking/POC — not the target fusion domain
- 6 fusion sources are ingested but none have been systematically researched or connected to modeling decisions
- No end-to-end documentation exists showing the complete workflow from goals to results
- The agentic-mbse modeling dashboard hasn't been exercised in fusion-tea

### Future State

- agentic-mbse is current (validation restructure + extraction v4 integrated)
- Ingestion pipeline re-validated against the new extraction backend
- A durable framework exists for organizing the fusion concept space:
  - Taxonomy of fusion approaches (confinement types, fuel cycles, etc.)
  - Generalized cost structure that applies across concepts
  - Mapping of existing approaches (including startup concepts) into this framework
- A complete workflow walkthrough exists with committed artifacts at every phase:
  1. Investigation scope and objectives defined
  2. Domain frameworks (taxonomy/ontology) established
  3. Curated corpus ingested with quality metrics
  4. Domain insights extracted as DI-XXX entries
  5. First modeling exercise identified and planned from research findings
  6. SysML models passing all 6 validation levels
  7. Dashboard showing project status and traceability
  8. Cost structure visualizations
- Each step demonstrates how knowledge is codified — from broad domain understanding down to concrete model parameters
- These artifacts are the real foundation for ongoing fusion TEA work, not a throwaway demo

---

## Strategy

### Use the pipeline, don't just test it

This epic exercises the agentic-mbse workflow on a real problem. Validation happens as a natural consequence of use, not as a separate testing activity. When things break or need adjustment, that's expected — fix it, document it, keep going.

### Broad-then-deep: frameworks before models

Don't jump to modeling a specific concept. Start by understanding the space:
- What are we trying to learn? (Costing and TEA across fundamentally different fusion approaches)
- How do we organize this space? (Taxonomy of concepts, generalized cost structures)
- Where should we start modeling? (Emerges from the frameworks and research, not assumed upfront)

The first modeling target is an output of the investigation, not an input.

### Knowledge codification at every step

Each phase of work should visibly transform knowledge from one form to another:
- Unstructured PDFs → structured extractions → domain insights (DI-XXX)
- Broad investigation goals → organized taxonomy → specific modeling requirements
- Research findings → model parameters with traced sources

Highlighting these transformations IS the demo.

### Prerequisites as gating, not as epic scope

Updating agentic-mbse and re-validating the ingestion pipeline are prerequisites. They must complete before the workflow begins, but they're infrastructure maintenance, not part of the demonstrated workflow.

### Iterative source ingestion

Don't try to build the perfect corpus upfront. Ingest an initial set, do research, and if gaps emerge, ingest more. The pipeline should support this naturally.

### Failures are content

If something doesn't work (extraction quality issues, validation failures, data gaps), document it. A real workflow has rough edges — showing how to handle them is more valuable than a polished happy path.

---

## Prerequisites

### P1: agentic-mbse branches merged

Both changes are merged to the `doc-ingest-clean` branch (not yet PR'd to main — validation comes first):

1. **Validation stack restructure** (`valstack-cleanup` → merged): 8→6 levels, ADR-002 consolidation into L6
2. **Extraction pipeline v4** (`doc-ingest-clean`): 8-step orchestrated pipeline replacing old extraction

fusion-tea is synced (`uv sync` done, agentic-mbse 0.1.0 editable from `../agentic-mbse`).

---

## Requirements

### R1: Investigation Scope & Objectives

The work begins with a broad question — not a predetermined modeling target.

**R1.1**: Define the investigation scope: what are we trying to learn about fusion economics? (Costing and TEA across fundamentally different fusion approaches, not just one concept)
**R1.2**: Define the comparison axes and end objectives (e.g., LCOE across concepts, cost driver identification, sensitivity to technology assumptions)
**R1.3**: Scope must be captured in a durable artifact, committed to the project
**R1.4**: Scope must be broad enough to motivate taxonomy work (R2) but bounded enough to define "done" for this epic

### R2: Domain Frameworks (Taxonomy / Ontology)

Before modeling any specific concept, establish frameworks for organizing the fusion design space.

**R2.1**: Develop a taxonomy of fusion approaches — how do you generalize a fusion "concept"? (Confinement type, fuel cycle, energy conversion, scale, etc.)
**R2.2**: Categorize existing approaches into this taxonomy (including startup concepts, traditional programs, novel approaches)
**R2.3**: Identify a generalized cost structure that can apply across concepts (what cost categories are universal vs. concept-specific?)
**R2.4**: Frameworks must be informed by domain literature (R3/R4), not invented from first principles alone
**R2.5**: Frameworks must be durable artifacts — not just chat analysis, but committed documentation that future modeling work builds on

### R3: Source Ingestion

**R3.1**: Curate and ingest fusion domain literature sufficient to inform both the taxonomy (R2) and eventual modeling work
**R3.2**: All sources flow through the Zotero → extract → register pipeline
**R3.3**: Extraction uses the v4 pipeline; quality metrics (`metrics.json`, `decisions.json`) are captured
**R3.4**: Critical cost data tables are spot-checked for extraction quality
**R3.5**: SOURCE_INDEX.md is current with all ingested sources
**R3.6**: Source selection is iterative — initial set based on R1 scope, expanded as research (R4) reveals gaps

### R4: Domain Research

**R4.1**: Ingested sources are researched using the `/research` workflow, producing DI-XXX entries in `knowledge/KNOWLEDGE.md`
**R4.2**: Research feeds the taxonomy (R2): identifying how sources categorize fusion concepts, what cost structures they use, what parameters they track
**R4.3**: Research identifies: key cost parameters and ranges, scaling relationships, technology assumptions, and data gaps
**R4.4**: Research findings must be sufficient to identify a tangible first modeling exercise (R5)
**R4.5**: If research reveals the corpus is insufficient, additional sources are ingested (loop back to R3)

### R5: First Modeling Exercise

The modeling target emerges from R1-R4, not from upfront assumptions.

**R5.1**: Identify a specific, bounded first piece of modeling work based on the frameworks (R2) and research (R4)
**R5.2**: A modeling plan exists that traces to research findings (DI-XXX references) and taxonomy elements
**R5.3**: The plan defines which SysML elements to create and their validation criteria
**R5.4**: Data gaps are documented with assumed values and their sources
**R5.5**: The plan prioritizes for maximum insight — better to complete a narrow piece well than stall on breadth

### R6: Model Construction

**R6.1**: SysML v2 models use established library patterns (`'Costed Component'`, CAS categories)
**R6.2**: Models pass all 6 validation levels
**R6.3**: Models trace to domain sources via traceability matrix
**R6.4**: Cost calculations are compared against PyFECONS reference values where overlap exists (match or deviation explained)
**R6.5**: Modeling decisions and trade-offs are documented as they happen

### R7: Dashboard & Progress Tracking

**R7.1**: The agentic-mbse dashboard shows validation status and traceability coverage for the models
**R7.2**: Dashboard is runnable with a single command
**R7.3**: Dashboard state is captured at least once (screenshot or report)

### R8: Visualization

**R8.1**: At minimum: structural cost breakdown diagram (component hierarchy with costs)
**R8.2**: Visualizations are generated from model data, not hand-drawn
**R8.3**: LCOE breakdown showing subsystem contributions

### R9: Documentation Trail (cross-cutting)

This is not a separate phase — it's a property of how all other work is done.

**R9.1**: Each phase produces a committed artifact — scope doc, taxonomy, ingested sources, research entries, modeling plan, models, dashboard output, visualizations
**R9.2**: At each step, it should be clear how knowledge was transformed (PDFs → extractions → insights → frameworks → model parameters)
**R9.3**: Decisions and rationale are captured alongside outputs
**R9.4**: Workarounds and rough edges are documented honestly

### R10: Interactive Workflow Explainer

The primary deliverable for the "demo" aspect — a self-contained HTML file that captures and presents artifacts from each stage of the workflow.

**R10.1**: The explainer has stage navigation across the top, allowing a reader to cycle through the workflow stages in order
**R10.2**: Each stage contains embedded snippets of real artifacts from that stage's work — images (screenshots, diagrams), rendered markdown, or interactive elements (embedded visualizations, expandable sections)
**R10.3**: The explainer is built incrementally — each work item that completes a stage adds its content
**R10.4**: The explainer is self-contained (single HTML file or HTML + local assets) and viewable by opening in a browser
**R10.5**: The explainer shows the knowledge transformation at each stage — what went in, what came out, why it matters

---

## Success Criteria

- [ ] Investigation scope and objectives are written down and committed before other work begins
- [ ] A taxonomy of fusion approaches exists as a committed artifact, categorizing existing concepts
- [ ] A generalized cost structure is defined that applies across fusion concepts
- [ ] 5+ fusion sources ingested through the Zotero → extract → register pipeline with v4 extraction
- [ ] At least 3 sources researched with DI-XXX entries in KNOWLEDGE.md
- [ ] Research findings visibly informed the taxonomy and the choice of first modeling target
- [ ] A first modeling exercise is identified, planned, and traced to research findings
- [ ] At least one SysML model passes all 6 validation levels
- [ ] Model cost outputs are compared against PyFECONS reference values (match or deviation explained)
- [ ] Dashboard has been run and output captured
- [ ] At least one cost visualization is generated from model data
- [ ] An interactive HTML explainer exists with stage-by-stage navigation showing the full workflow
- [ ] Each completed stage has embedded artifacts (images, rendered markdown, interactive elements) in the explainer
- [ ] All artifacts are committed to git (not ephemeral)

---

## Scope Boundaries

**In scope**:
- The complete workflow arc from investigation scope through visualization
- Building domain frameworks (taxonomy/ontology) that organize the fusion concept space
- Real fusion domain content (not toy examples)
- Identifying and executing one tangible modeling exercise that emerges from the investigation
- Honest documentation including failures and workarounds

**Out of scope**:
- Modeling every fusion concept (the taxonomy maps the space; we model one piece deeply)
- Rewriting agentic-mbse documentation (we produce artifacts, not tutorials)
- Perfecting extraction quality on every source (document issues, move on)
- Building new agentic-mbse features (use what exists; file issues for gaps)

---

## Backlog Items

### Item 1: Extraction Pipeline Validation [0.5 day] ✅ COMPLETE

**Type**: Validation/Execution

**Objective**: Verify that the v4 extraction pipeline works correctly on our existing fusion corpus and is acceptable for the investigation ahead.

**Current State**:
- ✅ agentic-mbse `doc-ingest-clean` branch checked out with both merges (valstack + extraction v4)
- ✅ fusion-tea synced via `uv sync` — CLI available
- ✅ 6 existing extracted sources in `knowledge/sources/` (extracted with old pipeline)
- ✅ v4 pipeline validated — all components pass, re-extraction complete
- ✅ `--check` run — pymupdf4llm, gmft, img2table, pandoc, claude all pass

**Scope**:
1. **Installation verification** (`--check`):
   - Run `uv run agentic-mbse extract --check` to verify all dependencies are installed and the pipeline runs correctly against the built-in test corpus
   - Document any missing optional dependencies (GMFT, Img2Table, Docling, Pandoc)
2. **Quality gate preview** (`--dry-run`):
   - Run `--dry-run` on 2-3 existing source PDFs to see what the v4 quality gate would decide (which pages need enhancement, what issues it detects)
   - Compare quality gate assessment against known issues (e.g., Hawker strikethrough)
3. **Full re-extraction**:
   - Re-extract all 6 existing PDFs with the v4 pipeline (`--force`)
   - Use consistent settings: `--budget 50 --model opus --index --summarize`
   - Compare output quality against existing `output.md` files (diff key sections, check tables, check cost data)
4. **Verdict**:
   - Document results: what improved, what regressed, any new issues
   - Acceptability decision: good enough to proceed, or needs fixes before continuing?

**Out of Scope**:
- Fixing extraction bugs in agentic-mbse (file issues if found)
- Re-validating `zotero_ingest.py` integration (that's for when we ingest new sources)
- New source ingestion

**Success Criteria**:
- [x] `--check` runs without errors
- [x] `--dry-run` output reviewed for at least 2 sources
- [x] All 6 sources re-extracted with v4 pipeline
- [x] Quality comparison documented (vs. previous extraction)
- [x] Acceptability verdict recorded — **PROCEED WITH CAVEATS**

**Estimated Effort**: 0.5 day (minimal planning — mostly execution)

**Location**: `.project/active/extraction-validation/`

**Dependencies**: P1 (agentic-mbse branches merged and synced)

**Deliverables**:
- `.project/active/extraction-validation/results.md` — comparison report and verdict

---

### Item 2a: Define Investigation Scope & Refresh Project Documents [1 day] ✅ COMPLETE

**Type**: Research/Writing

**Objective**: Answer the question "We want to broadly investigate fusion technologies for TEA — what does that mean concretely?" and make the project documents reflect the answer.

**The Problem**:

The project currently says "we're modeling CATF MFE tokamaks, then expanding later." But we've realized the right starting point is broader: we want to understand the economics of fusion across fundamentally different approaches. This changes what questions we're asking, what literature we need, and how we organize the work.

The existing project documents (OVERVIEW, ARCHITECTURE, REQUIREMENTS, BACKLOG, CLAUDE.md) all assume CATF-first. Before we can do any meaningful new work, these need to reflect what we're actually doing. Otherwise every tool, every command, every agent reads the wrong context.

**The Actual Work**:

1. **Think through the investigation framing**:
   - We're doing costing and TEA. Not just for one reactor — for a landscape of approaches.
   - What questions are we trying to answer? (e.g., "Which fusion approaches have a credible path to competitive LCOE?" / "What are the dominant cost drivers and how do they differ across concepts?" / "Where are the biggest uncertainties?")
   - What are the comparison axes that matter? (LCOE, capital cost breakdown, capacity factor assumptions, fuel cycle economics, technology readiness)
   - What's in scope? Traditional MFE (tokamaks, stellarators, mirrors), IFE (laser, heavy-ion), magneto-inertial, startup concepts (Commonwealth, TAE, Helion, etc.), or some subset?
   - What defines "done" for THIS epic vs. ongoing project work?

2. **Derive what literature we need**:
   - Given the investigation scope, what kinds of sources should we seek? (Cost studies, design reports, comparison papers, startup technical disclosures)
   - What do the 6 existing sources already cover? Where are the gaps?
   - Produce a prioritized list of source types/topics to guide ingestion

3. **Write it down in project documents**:
   - `modeling_project/OVERVIEW.md` — the primary artifact. Rewrite to capture the investigation scope, the questions, the comparison axes, the "done" definition, and the source strategy.
   - `CLAUDE.md` — this is what every agent session reads first. It currently says "Start with CATF MFE as the reference design." It needs to accurately describe what we're doing now, what tools are available (6-level validation, v4 extraction pipeline), and how the project is structured. Stale CLAUDE.md means every future session starts with the wrong mental model.
   - Other project docs (`ARCHITECTURE.md`, `REQUIREMENTS.md`, `work/BACKLOG.md`) — update or archive anything that contradicts the new framing. The concept-agnostic content in these files is still valid; the CATF-specific roadmap (WI-006→018) needs to be archived since those work items will be re-derived from the investigation.

**What We're NOT Doing**:
- Building the taxonomy (that's later work, informed by research against sources)
- Ingesting new sources (separate item)
- HTML explainer (Item 2b)
- Detailed modeling plan (emerges from research)

**Success Criteria**:
- [x] The investigation scope is written down: what questions, what comparison axes, what's in/out of scope, what "done" means
- [x] Source selection criteria exist: what literature do we need, what do we already have, what's missing
- [x] `CLAUDE.md` accurately describes the current project (investigation scope, toolchain state, project structure)
- [x] Project documents don't contradict each other or reference a CATF-first roadmap
- [x] CATF-specific backlog items archived (not deleted — they may be relevant once a first modeling target is chosen)
- [x] All changes committed

**Estimated Effort**: 1 day

**Location**: `.project/active/project-reframing/`

**Dependencies**: Item 1 (confirms toolchain works; we need to know the tools are ready before committing to a scope that assumes them)

**Deliverables**:
- Revised `modeling_project/OVERVIEW.md` — the investigation scope document
- Updated `CLAUDE.md` — accurate project context for all future sessions
- Revised/archived project docs as needed to eliminate contradictions

---

### Item 2b: Start the Workflow Explainer [0.5 day] ✅ COMPLETE

**Type**: Implementation

**Objective**: Create an HTML document that captures what we're doing and why, starting with the work from Item 2a. This grows over time as we do more work — each item adds a section showing what happened, with real artifacts embedded.

**The idea**: We want something we can share that walks through the full process of investigating fusion economics using agentic-mbse. Not a tutorial — a narrated record of what we actually did. It starts with "here's the question we're asking and how we set up the project" and eventually covers ingestion, research, taxonomy, modeling, and results.

**For this item**: Build the HTML shell and populate it with the first section — the investigation scope and project setup from Item 2a. Snippets of the scope document, screenshots of the project structure, whatever makes sense to show what "getting started" looked like.

**Success Criteria**:
- [x] HTML file exists, opens in a browser, looks presentable
- [x] First section captures the 2a work with embedded artifacts (markdown excerpts, images, etc.)
- [x] Easy to add new sections as future work items complete
- [x] Committed to git

**Estimated Effort**: 0.5 day

**Location**: `.project/active/workflow-explainer/`

**Dependencies**: Item 2a

**Deliverables**:
- `demo/index.html` (or similar)

---

*Further items TBD after decomposition.*

---

## Open Questions

1. **Dashboard readiness**: What's the current state of the agentic-mbse dashboard? Does it need setup work?
2. **Clean slate vs. build on existing**: Re-ingest all 6 existing sources with v4, or start fresh with new source selection?
3. **Branch strategy**: New branch from main, or continue on `processing-work`?

---

## Dependencies

**External**:
- ✅ `valstack-cleanup` merged into `doc-ingest-clean` (done)
- ✅ `doc-ingest-clean` checked out and synced (done)
- Zotero library populated with target fusion documents (needed for R3)
- Network access for Zotero API and Claude API

**Internal (sequencing)**:
- P1 + P2 → R1 (scope) → R3 (initial ingest) → R4 (research) ↔ R2 (taxonomy, iterates with research) → R5 (identify first modeling exercise) → R6 (build models) → R7 + R8 (dashboard + viz)
- R3 and R4 iterate: research may reveal need for more sources
- R2 and R4 iterate: taxonomy is informed by research, research is guided by taxonomy gaps
- R9 (documentation trail) is continuous throughout

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| v4 extraction produces worse results than old pipeline | Medium — may need upstream fixes | Item 1 validates before proceeding. Known issues are documented. |
| Extraction v4 breaks zotero_ingest.py | Medium — delays ingestion | P2 explicitly validates this before epic begins. |
| Dashboard not ready for fusion-tea | Medium — R6 scoped down | Assess in prerequisites. Use what's available. |
| Source literature insufficient for LCOE | Medium — shallow results | Start with known high-value sources (ARIES). R3.6 allows iterative addition. |
| Taxonomy work expands indefinitely | Medium — never reaches modeling | R1.4 bounds the scope. Taxonomy must be "good enough to pick a first target," not perfect. |
| Modeling scope creep | Medium — epic stalls | R5.5 prioritizes. Better to complete a narrow piece well than stall on breadth. |

---

**Last Updated**: 2026-03-02
**Next Action**: Items 1, 2a, and 2b complete. Next: Item 3 (Source Ingestion) or decompose remaining epic items based on investigation strategy in `modeling_project/OVERVIEW.md`. Work artifacts at `.project/active/project-reframing/` (Items 2a+2b) and `.project/active/extraction-validation/` (Item 1).
