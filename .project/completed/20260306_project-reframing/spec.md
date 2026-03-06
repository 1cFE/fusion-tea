# Spec: Project Reframing — Investigation Strategy & Fresh Start

**Status:** Draft
**Owner:** Reid W
**Created:** 2026-03-01 22:10 PST
**Complexity:** MEDIUM
**Branch:** processing-work
**Epic:** `.project/backlog/epic-full-workflow-demo.md` — Items 2a + 2b (merged)

---

## Business Goals

### Why This Matters

Every agent session, tool invocation, and CLAUDE.md read currently tells the reader: "We're modeling CATF MFE tokamaks first, then expanding." That's no longer the intent. The project has pivoted to a broad comparative investigation of fusion economics across fundamentally different approaches. Until the project documents, requirements, and processes reflect this, all downstream work (research, taxonomy, modeling) builds on a stale foundation.

This isn't just a document refresh — it's building the **strategy** for how we approach fusion modeling. The strategy defines what questions we're asking, how we organize the concept space, what patterns our models must follow to enable cross-concept comparison, and what process we follow from investigation through to results.

### Success Criteria

- [ ] Investigation strategy is written down: research questions, comparison axes, in/out of scope, "done" definition
- [ ] Modeling requirements define concept-agnostic patterns that enable cross-concept reuse and comparison
- [ ] Process requirements define the investigation arc: taxonomy → concept analysis → modeling patterns → models
- [ ] Source selection criteria exist: what literature types we need, what existing sources cover, where gaps are
- [ ] `CLAUDE.md` accurately describes the current project state for all future sessions
- [ ] `OVERVIEW.md` is the investigation scope document (not a template)
- [ ] Stale knowledge artifacts (KNOWLEDGE.md DI-XXX entries, ARCHITECTURE.md AD-XXX entries, REQUIREMENTS.md PR-XXX entries) are cleared — fresh start, git history preserves the old
- [ ] CATF-specific backlog items (WI-006→018) archived
- [ ] Existing SysML models archived (moved out of `models/`, preserved but not active)
- [ ] No project document contradicts another or references the CATF-first roadmap as current
- [ ] Interactive workflow explainer exists with Stage 1 (Investigation Scope) populated from this work
- [ ] Remaining explainer stages are stubbed with descriptions of what artifacts will fill them

### Priority

P0 gate for the DEMO epic. Nothing else in the epic can proceed coherently until this is done.

---

## Problem Statement

### Current State

- `OVERVIEW.md`: Generic template with "Reference Implementation: CATF MFE" framing
- `CLAUDE.md`: Says "Start with CATF MFE as the reference design before generalizing"
- `ARCHITECTURE.md`: 5 architectural decisions (AD-001→005) all oriented around CATF MFE implementation
- `REQUIREMENTS.md`: 7 modeling requirements (PR-001→007) all CATF-specific (PyFECONS validation, specific attribute patterns)
- `KNOWLEDGE.md`: 14 domain insights (DI-001→014) from CATF-oriented research
- `BACKLOG.md`: 18 work items, WI-006→018 are a CATF-first implementation roadmap
- `SOURCE_INDEX.md`: 6 sources ingested, 4 of 6 have empty "Use for" / "Validation" fields
- `models/`: Foundation package, power balance calcs, and test models — all built for CATF approach
- Validation matrix, traceability matrix exist but reference the old framing

### Desired Outcome

A coherent set of project documents that define:
1. **What we're investigating** — broad fusion TEA, not a single concept
2. **How we'll organize the space** — process for building taxonomy and understanding concept similarities/differences
3. **What patterns our models must follow** — concept-agnostic requirements that maximize reuse
4. **What we need to learn from literature** — source selection criteria tied to investigation goals
5. **What "done" looks like** — bounded scope for this epic

---

## Scope

### In Scope

- **Investigation strategy**: Research questions, comparison axes, scope boundaries, "done" definition
- **Modeling requirements**: Concept-agnostic patterns for cross-concept models (CAS structure, costed component patterns, reuse strategies)
- **Process requirements**: The investigation arc and how each phase feeds the next
- **Source selection criteria**: What types of literature we need and gap analysis against existing corpus
- **Document rewrites**: OVERVIEW.md, CLAUDE.md
- **Document clearing**: KNOWLEDGE.md (clear DI-XXX entries), ARCHITECTURE.md (clear AD-XXX entries), REQUIREMENTS.md (clear PR-XXX entries)
- **Archival**: CATF-specific backlog items (WI-006→018), existing SysML models in `models/`
- **Backlog restructuring**: Reflect investigation-driven work structure
- **Interactive workflow explainer**: Bootstrap the HTML explainer and populate Stage 1 with artifacts from this work. The explainer is built incrementally — each subsequent epic item adds its stage's content.

### Out of Scope

- Building the taxonomy (emerges from research in later items)
- Ingesting new sources (separate epic item)
- Detailed modeling plan for any specific concept
- Doing research against existing sources
- Writing actual SysML models
- Explainer content for stages beyond Stage 1 (populated by later work items)

### Edge Cases & Considerations

- Some old knowledge artifacts contain legitimately useful patterns (e.g., CAS hierarchy structure, NumericalFunctions::sum for cost rollup). These should be captured in the new requirements/process documents where relevant — not preserved as legacy DI-XXX entries.
- The existing foundation package (types, units, materials) and power balance calcs represent real validated work. Archiving preserves them; they can be revived when tokamak modeling begins.
- `SOURCE_INDEX.md` has 6 registered sources that are still valid extracted documents. The source registrations stay; the empty "Use for" fields get addressed when source selection criteria are defined.

---

## Requirements

### Investigation Strategy Requirements

1. **ISR-1**: The investigation MUST define 3-5 research questions that scope what we're trying to learn about fusion economics. These questions drive all downstream work — taxonomy, source selection, modeling targets.

2. **ISR-2**: The investigation MUST define comparison axes — the dimensions along which fusion concepts will be compared (e.g., LCOE, capital cost breakdown by CAS category, capacity factor assumptions, fuel cycle economics, technology readiness).

3. **ISR-3**: The investigation MUST define scope boundaries — what classes of fusion concepts are in/out (traditional MFE, IFE, magneto-inertial, startup concepts, or a specified subset), and what level of modeling depth is intended.

4. **ISR-4**: The investigation MUST define a "done" criterion for this epic that is bounded and achievable — broad enough to demonstrate the full workflow, narrow enough to complete.

5. **ISR-5**: The investigation MUST produce source selection criteria — what types of literature are needed (cost studies, design reports, concept comparisons, startup disclosures) and how to prioritize them.

6. **ISR-6**: The investigation SHOULD include a gap analysis of the existing 6 sources against the selection criteria — what's covered, what's missing, what topics need new sources.

### Modeling Requirements

> These replace the old PR-XXX entries. They define patterns that all models MUST follow to enable cross-concept comparison and maximum reuse.

7. **MR-1**: All models MUST use the CAS (Cost Account Structure) hierarchy as the primary cost decomposition. This is the one structural pattern known to work across MFE, IFE, and MIF concepts. [Carries forward the useful core of old DI-001]

8. **MR-2**: All cost-bearing components MUST implement a standard costed component interface with at minimum: capital_cost, and cost breakdown categories sufficient for cross-concept comparison. [Carries forward the useful core of old DI-003]

9. **MR-3**: Library definitions MUST be concept-agnostic. Concept-specific values, assemblies, and parameters MUST live in `designs/{concept}/`. [Carries forward AD-002 principle]

10. **MR-4**: All cost parameters MUST cite their source — at minimum the document and location from which the value was derived. [Carries forward the useful core of old DI-014]

11. **MR-5**: The modeling requirements SHOULD define a standard output schema for cross-concept comparison — a common set of outputs every concept model must produce to enable apples-to-apples comparison. [INFERRED — necessary for the comparison axes to work]

12. **MR-6**: The project SHOULD define modeling patterns (documented templates/examples) for common structures BEFORE building production models. Pattern definition is a distinct step from model building. [From user's process description]

### Process Requirements

> These define how the investigation progresses from broad understanding to specific models.

13. **PR-1**: The process MUST begin with taxonomy development — organizing the fusion concept space into a structured classification before selecting modeling targets. Taxonomy is informed by domain literature, not invented from first principles.

14. **PR-2**: After taxonomy, the process MUST include a concept analysis phase — understanding the similarities and differences between concepts we intend to model, specifically identifying what cost structures, physics models, and engineering parameters they share vs. where they diverge.

15. **PR-3**: Based on the concept analysis, the process MUST produce documented modeling patterns — reusable templates and conventions that capture the shared structure and define where concept-specific specialization occurs. This happens BEFORE production modeling begins.

16. **PR-4**: The process SHOULD be iterative — research may reveal taxonomy gaps, concept analysis may reveal literature gaps, pattern definition may reveal taxonomy gaps. The process accommodates this.

17. **PR-5**: Each phase of the process MUST produce committed artifacts. Knowledge transforms are visible: PDFs → structured extractions → domain insights → taxonomy → concept analysis → modeling patterns → models → results.

### Workflow Explainer Requirements

> The explainer is built alongside the work, not after. Each phase of the epic adds its stage content as a natural byproduct. This work item bootstraps the structure and populates Stage 1.

18. **ER-1**: An interactive HTML explainer MUST exist as a self-contained file (or HTML + local assets) viewable by opening in a browser. No server required.

19. **ER-2**: The explainer MUST have section navigation allowing a reader to move through the content in order. The structure separates infrastructure explanation (how the system works) from investigation pipeline (how the work proceeds):
    - **Sections 1-4 (Infrastructure):** The Question (investigation scope), The Scaffold (project structure and setup), The Workflow (commands and work item lifecycle), The Harness (quality mechanisms — YAML state, dashboard, traceability)
    - **Bridge:** The Process (investigation process diagram and internal cycle from OVERVIEW.md)
    - **Sections 5-9 (Pipeline):** Source Ingestion, Domain Research, Taxonomy, Concept Modeling, Cross-Concept Comparison
    Each section is populated with real content as the corresponding work completes.

20. **ER-3**: Each stage MUST support embedded real artifacts — rendered markdown snippets, images (screenshots, diagrams), expandable sections. These are curated, not auto-generated.

21. **ER-4**: For this work item, Sections 1-4 and the Process bridge MUST be populated with real content from the work done here — research questions, comparison axes, scope boundaries, project structure, workflow commands, quality mechanisms, and the investigation process diagram.

22. **ER-5**: Remaining stages MUST be stubbed with titles and brief descriptions of what artifacts will be embedded when that stage's work completes. Each stub SHOULD indicate the knowledge transformation that stage performs (what goes in, what comes out).

23. **ER-6**: The explainer SHOULD be designed so that adding a new stage's content is straightforward — a later work item can add its artifacts without restructuring the whole file.

### Document Requirements

24. **DR-1**: `CLAUDE.md` MUST accurately describe the current project — investigation scope, available toolchain (agentic-mbse with 6-level validation, v4 extraction), project structure, and how to use `uv`.

25. **DR-2**: `modeling_project/OVERVIEW.md` MUST be the investigation scope document — research questions, comparison axes, scope boundaries, "done" criteria, source strategy.

26. **DR-3**: `knowledge/KNOWLEDGE.md` MUST be cleared of existing DI-XXX entries. Fresh start; entries will be re-derived from research in later work items.

27. **DR-4**: `modeling_project/ARCHITECTURE.md` MUST be cleared of existing AD-XXX entries. Architectural decisions will be re-derived from the investigation strategy and modeling pattern work.

28. **DR-5**: `modeling_project/REQUIREMENTS.md` MUST be cleared of existing PR-XXX entries and populated with the new modeling requirements (MR-1 through MR-6) from this spec.

29. **DR-6**: `work/BACKLOG.md` MUST archive CATF-specific items (WI-006→018). The backlog structure SHOULD reflect the investigation-driven workflow.

30. **DR-7**: Existing SysML models in `models/library/` and `models/tests/` MUST be archived — moved to an archive location, not deleted. They can be revived when tokamak modeling begins.

31. **DR-8**: `knowledge/SOURCE_INDEX.md` SHOULD have its source entries updated with meaningful "Use for" descriptions tied to the investigation scope, where applicable.

32. **DR-9**: `data/traceability_matrix.csv` and `modeling_project/VALIDATION_MATRIX.md` SHOULD be cleared or archived if they reference the old framing.

---

## Acceptance Criteria

### Investigation Strategy
- [ ] 3-5 research questions written that scope the fusion TEA investigation
- [ ] Comparison axes defined and documented
- [ ] In/out of scope boundaries explicit
- [ ] "Done" criteria for this epic are bounded and testable
- [ ] Source selection criteria exist with gap analysis against current 6 sources

### Modeling & Process
- [ ] MR-1 through MR-6 are documented as the project's modeling requirements
- [ ] PR-1 through PR-5 are documented as the investigation process
- [ ] Requirements are written as enforceable standards, not aspirational prose

### Documents
- [ ] OVERVIEW.md is a real investigation scope document (not a template)
- [ ] CLAUDE.md accurately describes the project as it exists now
- [ ] KNOWLEDGE.md, ARCHITECTURE.md, REQUIREMENTS.md cleared of stale entries
- [ ] BACKLOG.md reflects investigation-driven work, CATF items archived
- [ ] SysML models archived out of `models/`
- [ ] No two project documents contradict each other

### Workflow Explainer
- [ ] HTML explainer exists and opens in a browser
- [ ] Section navigation works — can move through all sections
- [ ] Sections 1-4 (The Question, The Scaffold, The Workflow, The Harness) populated with real content
- [ ] Process bridge populated with investigation process diagram and internal cycle
- [ ] Pipeline sections (5-9) stubbed with descriptions and expected artifact types
- [ ] Each pipeline stub indicates the knowledge transformation for that stage
- [ ] Adding future section content doesn't require restructuring the explainer

### Integrity
- [ ] All changes committed to git
- [ ] A reader encountering this project for the first time gets an accurate picture

---

## Related Artifacts

- **Epic:** `.project/backlog/epic-full-workflow-demo.md` — Items 2a + 2b (merged)
- **Plan:** `.project/active/project-reframing/plan.md` (to be created — next step)
- **Current OVERVIEW:** `modeling_project/OVERVIEW.md`
- **Current CLAUDE.md:** `CLAUDE.md`
- **Current BACKLOG:** `work/BACKLOG.md`
- **Explainer:** `demo/explainer.html` (or `demo/index.html` + `demo/assets/`) — to be created

---

## Note on Workflow

Per user direction, there is no `design.md` for this work item. The flow is:
- **spec.md** (this document) → **plan.md** (phased execution with checkboxes)

The plan will have phases that progressively flesh out the investigation strategy, modeling requirements, process requirements, and then update each document.

---

**Next Steps:** After approval, proceed to `/_my_plan`
