# Epic: Full Workflow Demo — Fusion TEA

**Epic ID**: DEMO
**Status**: Complete
**Priority**: P0
**Created**: 2026-03-01
**Estimated Effort**: TBD (pending decomposition)

---

## Executive Summary

Investigate fusion technologies for techno-economic analysis using the full agentic-mbse workflow. This serves a dual purpose: it produces the real analytical foundation for comparing fusion approaches on cost, and it creates a documented trail demonstrating how the toolchain works end-to-end.

The workflow arc: define investigation scope → build domain frameworks (taxonomy/ontology) → ingest literature → research sources → plan first modeling exercise → build models → track on dashboard → visualize results. Each step codifies knowledge in durable, committed artifacts.

**Critical Success Factor**: Someone could follow the committed artifacts from this epic and understand both the fusion domain structure AND how to reproduce the workflow on a different domain.

---

## Why This Epic?

### What It Produces

- A durable framework for organizing the fusion concept space:
  - Taxonomy of fusion approaches (confinement types, fuel cycles, etc.)
  - Generalized cost structure that applies across concepts
  - Mapping of existing approaches (including startup concepts) into this framework
- A complete workflow walkthrough with committed artifacts at every phase:
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

### Iterative source ingestion

Don't try to build the perfect corpus upfront. Ingest an initial set, do research, and if gaps emerge, ingest more. The pipeline should support this naturally.

### Failures are content

If something doesn't work (extraction quality issues, validation failures, data gaps), document it. A real workflow has rough edges — showing how to handle them is more valuable than a polished happy path.

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
**R3.3**: Extraction quality metrics (`metrics.json`, `decisions.json`) are captured
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
- [ ] 5+ fusion sources ingested through the Zotero → extract → register pipeline
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

**Objective**: Verify the extraction pipeline works correctly on the fusion corpus.

**Outcome**: All 6 sources extracted. All pipeline components pass (`--check`). Verdict: **PROCEED WITH CAVEATS** (see `.project/active/extraction-validation/results.md`).

**Location**: `.project/active/extraction-validation/`

---

### Item 2a: Define Investigation Scope & Project Documents [1 day] ✅ COMPLETE

**Type**: Research/Writing

**Objective**: Define the broad investigation scope for fusion TEA across all confinement approaches, and ensure all project documents reflect it.

**Outcome**: Investigation scope defined in `modeling_project/OVERVIEW.md` — 5 research questions, 7 comparison axes, two-stage process (taxonomy → concept modeling), iterative source strategy. `CLAUDE.md` and all project docs aligned.

**Location**: `.project/active/project-reframing/`

**Deliverables**:
- `modeling_project/OVERVIEW.md` — investigation scope document
- `CLAUDE.md` — project context for agent sessions
- Aligned project docs (`ARCHITECTURE.md`, `REQUIREMENTS.md`, `work/BACKLOG.md`)

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

### Item 3: IFE Source Ingestion [0.5 day] ✅ COMPLETE

**Type**: Execution

**Objective**: Ingest the 5 `demo-ife` tagged papers through the Zotero pipeline, register in SOURCE_INDEX.md, and populate the "Source Ingestion" section of the demo.

**Current State**:
- 5 IFE papers tagged `demo-ife` in Zotero, spanning 1986–2026:
  - GI92TAS2: Economic studies for heavy-ion-fusion electric power plants (1986)
  - BQWVRWCF: Energy from Inertial Fusion (1992)
  - VKWLFRFK: Accelerators for Inertial Fusion Energy Production (2013)
  - WQVP4WBW: Affordable, manageable, practical, and scalable (AMPS) high-yield inertial fusion (2025)
  - 4PLGW7RA: Commercialization of laser fusion energy (2026)
- Hawker 2020 (simplified IFE economic model) already extracted and registered

**Scope**:
1. Run `zotero_ingest.py` with the `demo-ife` tag to extract all 5 papers
2. Register each in `knowledge/SOURCE_INDEX.md` with IFE-relevant "Use for" descriptions
3. Spot-check 1–2 extractions for cost table quality (especially the 1986 HIF economics paper — richest cost data)
4. Add content to demo/index.html section 5 — show the pipeline in action: Zotero tag → extraction → registration, with artifact snippets

**Out of Scope**:
- Fixing extraction quality issues (document and move on)
- Researching source content (that's Item 4)

**Success Criteria**:
- [x] All 5 `demo-ife` papers extracted and stored in `knowledge/sources/`
- [x] All 5 registered in SOURCE_INDEX.md with IFE-specific descriptions
- [x] At least 1 extraction spot-checked for cost table quality, results documented
- [x] Demo section 5 (Source Ingestion) populated with real pipeline artifacts
- [x] All changes committed

**Estimated Effort**: 0.5 day

**Dependencies**: Items 1, 2b

**Deliverables**:
- 5 new extracted sources in `knowledge/sources/`
- Updated `knowledge/SOURCE_INDEX.md`
- Demo section 5 populated

---

### Item 4: IFE Domain Research [1 day] ✅ COMPLETE

**Type**: Research

**Objective**: Research 3+ IFE sources to produce DI-XXX entries, extracting cost parameters, LCOE drivers, and CAS-relevant structure needed for modeling. Identify which IFE sub-concept has the richest data for the modeling exercise.

**Outcome**: 8 sources researched in a single `/research` session. 5 domain insights registered (DI-001 through DI-005). Modeling target selected: generic driver-agnostic IFE model (Hawker 14-parameter framework) with HIF as first instantiation.

**Location**: `.project/active/ife-domain-research/`

**Success Criteria**:
- [x] At least 3 IFE sources researched (8 sources covered)
- [x] 5+ DI-XXX entries in KNOWLEDGE.md covering IFE cost structure, parameters, and sensitivities
- [x] Written recommendation for which IFE sub-concept to model, with rationale
- [x] Demo section 6 (Domain Research) populated with real knowledge artifacts
- [x] All changes committed

**Deliverables**:
- DI-001 through DI-005 in `knowledge/KNOWLEDGE.md`
- Research report at `knowledge/research/approved/20260302-165055_ife-system-modeling-first-pass.md`
- Modeling target recommendation at `modeling_project/intent/IFE Modeling Target Selection.md`
- Demo section 6 populated (chat transcript, report highlights, DI cards, trace chain)

---

### Item 5: IFE Modeling Epic Setup [0.5 day] ✅ COMPLETE

**Type**: Setup/Planning

**Objective**: Set up the IFE modeling epic in the modeling PM and demonstrate the dashboard with real work items.

**Outcome**: IFE Cost Modeling epic (P0) created with 3 work items (WI-006, WI-007, WI-008) via `/backlog add`. Dashboard output captured and embedded in demo Section 7. Stale historical items (WI-004/005) cleaned from BACKLOG.md.

**Location**: `.project/active/ife-modeling-epic-setup/`

**Success Criteria**:
- [x] Modeling epic registered in `work/BACKLOG.md` with 3 work items
- [x] Dashboard runs and shows the epic + items
- [x] Dashboard output captured (embedded in demo + JSON at `data/dashboard-snapshot.json`)
- [x] All changes committed

**Deliverables**:
- Modeling epic and work items in `work/BACKLOG.md`
- Epic file at `work/backlog/epic-ife-cost-modeling.md`
- Dashboard output in `data/dashboard-snapshot.json`
- Demo Section 7 populated with chat transcript, epic callout, dashboard terminal block

---

### Item 6: IFE Cost Model — Spec Through Implementation [1.5 days] ✅ COMPLETE

**Type**: Modeling

**Objective**: Follow the full modeling PM workflow (spec → design → plan → implement) for a single IFE concept, running the validation stack at each stage. This is the core of the demo — showing the complete modeling pipeline with real domain content.

**Scope**:
1. **Spec** (`/spec-model`): Define what the IFE cost model covers — which CAS categories, what parameters, what sources provide the data, what the validation criteria are. Traces to DI-XXX entries from Item 4.
2. **Design** (`/design-model`): SysML architecture — library patterns for IFE (driver, target, chamber, BOP), concept-specific parts, calculation chains from physics parameters to LCOE.
3. **Plan** (`/plan-model`): Phased implementation with validation checkpoints at each phase.
4. **Implement** (`/implement-model`): Build the SysML v2 model, run validation at all 6 levels, document results including any failures.
5. Capture validation stack results as a key demo artifact — show what passes, what fails, and why.

**Concept selection**: Deferred to after Item 4 research. Candidates:
- **Generic IFE** (Hawker's 14-parameter model) — broadest coverage, technology-agnostic
- **Heavy Ion Beam IFE** — dedicated economics papers, well-defined driver cost structure
- **Laser indirect-drive IFE** — most current data (2025–2026 papers)

**Out of Scope**:
- Modeling multiple IFE concepts (one is sufficient for the demo)
- Achieving all-pass on validation (documenting failures is part of the demo)
- Cross-concept comparison (Item 7 stubs this)

**Success Criteria**:
- [x] Complete work item in `work/active/` with spec, design, plan artifacts
- [x] SysML v2 model in `models/designs/` with IFE cost structure
- [x] All 6 validation levels run, results captured regardless of pass/fail
- [x] Model parameters trace to DI-XXX entries and source documents
- [x] Modeling decisions documented in work item artifacts
- [x] Demo section 7 (Concept Modeling) populated with modeling workflow + validation results
- [x] All changes committed

**Estimated Effort**: 1.5 days

**Dependencies**: Item 5 (modeling epic and work items registered)

**Deliverables**:
- Work item artifacts in `work/active/`
- SysML model in `models/designs/`
- Validation results
- Demo section 7 populated

---

### Item 7: Visualization & Demo Completion [0.5–1 day] ✅ COMPLETE

**Type**: Implementation/Polish

**Objective**: Generate cost visualizations from model data, complete all demo sections, and polish the explainer for presentation.

**Scope**:
1. **Visualizations**: At minimum — CAS cost breakdown chart (component hierarchy with costs) and LCOE decomposition showing subsystem contributions. Generated from model data, not hand-drawn.
2. **Dashboard capture**: Final dashboard showing completed work items, validation status, traceability coverage.
3. **Demo completion**: Populate remaining demo sections:
   - Section 7 (Concept Modeling) — final polish with visualization embeds
   - Section 8 (Cross-Concept) — "here's what comes next" framing: we've modeled one IFE concept, the framework supports adding MFE, MIF, etc.
4. **Narrative polish**: Ensure the demo reads as a coherent story from investigation scope through results. Each section should show what went in, what came out, and why it matters.

**Out of Scope**:
- Building a second concept model for actual cross-concept comparison
- New features in agentic-mbse visualization tooling

**Success Criteria**:
- [x] At least one cost visualization generated from model data
- [x] LCOE decomposition showing subsystem contributions
- [x] Final dashboard output captured
- [x] All demo sections populated (sections 5–8)
- [x] Demo reads as a coherent end-to-end narrative
- [x] All changes committed

**Estimated Effort**: 0.5–1 day

**Dependencies**: Item 6 (need model and validation results to visualize)

**Deliverables**:
- Visualization artifacts in `data/` or `demo/`
- Completed `demo/index.html`

---

## Summary

| Item | Focus | Effort | Demo Requirement | Status |
|------|-------|--------|------------------|--------|
| 1 | Extraction Pipeline Validation | 0.5 day | (prerequisite) | ✅ Complete |
| 2a | Investigation Scope & Project Docs | 1 day | (prerequisite) | ✅ Complete |
| 2b | Workflow Explainer Shell | 0.5 day | HTML explainer | ✅ Complete |
| 3 | IFE Source Ingestion | 0.5 day | PDF ingestion from Zotero | ✅ Complete |
| 4 | IFE Domain Research | 1 day | Knowledge pipeline | ✅ Complete |
| 5 | IFE Modeling Epic Setup | 0.5 day | Dashboard with epic + work items | ✅ Complete |
| 6 | IFE Cost Model (full workflow) | 1.5 days | Validation stack in action | ✅ Complete |
| 7 | Visualization & Demo Completion | 0.5–1 day | SysML model visualizations | ✅ Complete |

**Remaining effort**: None — all items complete

---

## Open Questions

None currently open.

---

## Dependencies

**External**:
- Zotero library populated with IFE papers tagged `demo-ife`
- Network access for Zotero API and Claude API

**Internal (sequencing)**:
```
Items 1 + 2a + 2b + 3 (complete)
    → Item 4 (research IFE sources, recommend modeling target)
        → Item 5 (modeling epic setup, dashboard)
            → Item 6 (IFE cost model: spec → design → plan → implement)
                → Item 7 (visualization, demo polish)
```

- Demo/index.html is updated incrementally — each item adds its section
- The IFE modeling target decision gates Item 5 (epic work items) and Item 6 (model scope)

---

## Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| IFE source data insufficient for CAS-level modeling | Medium — shallow model | Hawker + HIF economics papers provide parametric data. Fall back to generic IFE (14-parameter model) if concept-specific data is too thin. |
| Dashboard not ready for fusion-tea | Medium — demo gap | Assess in Item 5. Use what's available; capture whatever output the dashboard produces. |
| Validation stack failures on IFE model | Low — failures ARE content | Document failures honestly. Showing how the stack catches issues is more valuable than an all-green report. |
| Modeling scope creep within IFE | Medium — epic stalls | One concept, CAS level 2. Better to complete narrow piece well than stall on breadth. |

---

**Last Updated**: 2026-03-03
**Next Action**: Epic complete. All 7 items delivered.
