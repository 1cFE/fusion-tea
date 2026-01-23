---
date: 2026-01-19T19:42:06-08:00
researcher: Claude
topic: "E2E Product Vision Gap Analysis"
tags: [research, architecture, ux, product-vision]
status: complete
last_updated: 2026-01-19
---

# Research: E2E Product Vision Gap Analysis

**Date**: 2026-01-19
**Researcher**: Claude
**Research Type**: Architecture / UX / Product Strategy

## Research Question

What are the gaps between the current `design-intent` documentation (focused on visualization) and the broader `product-vision.md` (RESEARCH → MODEL → SIMULATE pipeline)? How should we close these gaps with coherent abstractions, data types, and user workflows?

## Summary

- **design-intent** is visualization-focused: covers MODEL viewing, agent interaction, and export; doesn't address RESEARCH, CODEGEN, or SIM stages
- **product-vision** defines a 4-stage pipeline (RESEARCH → MODEL → CODEGEN → SIM) with distinct outputs and UX needs per stage
- The current visualization POC is solid but only covers the **structural view** portion of the MODEL stage
- Major gaps exist in: Research Data Management, Modeling PM/Workflow Integration, Codegen UX, and Simulation Study Definition
- Closing these gaps requires unified data models (ViewContexts), a central orchestration layer, and stage-aware navigation patterns

---

## Detailed Findings

### 1. Current State Analysis

#### 1.1 What design-intent Covers

The design-intent folder comprehensively addresses **visualization of SysML models**:

| Document | Coverage |
|----------|----------|
| `personas.md` | 3 personas (Domain Engineer, Model Developer, Stakeholder) - well-defined |
| `user-stories.md` | 35+ user stories across 3 use cases (Agentic Development, Agent-Assisted Viz, Export) |
| `requirements.md` | FR-1 through FR-4, NFR-1 through NFR-5 - visualization and integration |
| `concepts.md` | Vision, view types (Structural, Functional, Cost), interaction patterns, layouts, agent commands |
| `technical/` | Tool research, extraction API design, AST exploration |

**Key Focus**: Interactive model visualization with agent narration, targeting the "Model as Conversation Partner" metaphor.

#### 1.2 What product-vision.md Defines

The product vision defines a broader 4-stage pipeline:

```
RESEARCH → MODEL → SIMULATE (Codegen + Sim)
```

Each stage has distinct:
- **Actions** (what users do)
- **Impacts** (what changes)
- **Challenges** (open problems)
- **Outputs** (artifacts produced)
- **UX + Visualization** needs

#### 1.3 What Currently Exists in Code

Based on codebase exploration:

| Component | Stage | Status |
|-----------|-------|--------|
| SysML models | MODEL | Exists (`models/library`, `models/designs`) |
| syside parsing | MODEL | Works via `agentic_mbse.sysml.syside_adapter` |
| Structural extraction | MODEL | Complete (`proof_of_concept/extraction/visualization.py`) |
| Cytoscape visualization | MODEL | POC complete with cost annotations |
| Web server | MODEL | FastAPI server working |
| sysml-codegen | CODEGEN | Full pipeline generation exists |
| TEAx framework | SIM | External (`~/teax`) |
| Research database | RESEARCH | **Does not exist** |
| Modeling PM | MODEL | **Does not exist** |
| Study definition | SIM | **Does not exist** |

---

### 2. Gap Analysis

#### Gap 1: RESEARCH Stage is Unaddressed

**Product Vision Says:**
- Ingest research papers
- Use external literature research tools
- Capture conversation notes
- Output: DATABASE, MODELING PM (New Items)
- UX: Read/comment papers, modify tags, AI search/synthesis, highlight → create work item

**Design-Intent Says:** Nothing.

**Current Code:** No research data storage, no paper ingestion, no tagging system.

**Impact:** The entire "justified assumptions and traceability" value proposition depends on research integration.

---

#### Gap 2: Modeling PM / Workflow Management Missing

**Product Vision Says:**
- Process "features" from modeling backlog
- Provide input to resolve ambiguities
- Manage agentic modeling stages: Review spec → Design input → Review changes → Initiate work items
- Output: MODELING PM (Updates), SYSML MODELS

**Design-Intent Says:**
- US-1.9: "See agent's progress as it works"
- FR-2.3: "Display agent progress/status"
- Mentions re-render on commits

**Gap:** No work item management, no workflow state machine, no backlog integration in UX.

**Current Code:** Project management is in `.project/` markdown files (manual, not integrated with UI).

---

#### Gap 3: Codegen UX Not Designed

**Product Vision Says:**
- Design selection for codegen
- View of design parameters
- Overview of what designs are "compiled" for execution
- Output: TEAx Python, Design Parameters (JSON)

**Design-Intent Says:** Nothing specific about codegen UX.

**Current Code:** `sysml-codegen` CLI exists but no UX layer. User runs CLI manually.

**Impact:** The transition from MODEL → CODEGEN is a manual CLI step, breaking the end-to-end flow.

---

#### Gap 4: Simulation Study Definition & Results Not Designed

**Product Vision Says:**
- Define, set up, and run studies
- Execute single simulations, parameter sweeps, AI-led optimization
- Visualize: Costing/LCOE overlays, study results plots & tables
- Output: Numerical Results Database

**Design-Intent Says:**
- Cost View concept exists (`.project/design-intent/concepts.md:95-106`)
- US-1.12: "What-if questions"
- US-1.13: "Compare design variants side-by-side"

**Gap:** No study definition UX, no parameter sweep interface, no results database, no comparison visualization.

**Current Code:** TEAx can run pipelines but no UI for study definition or results exploration.

---

#### Gap 5: Cross-Stage Navigation Missing

**Product Vision Says:**
> "Because workflows are not always linear, a key feature is the ability to highlight any context and use to initiate action for any other stage."

**Design-Intent Says:** Focused on within-MODEL navigation (zoom, highlight, expand).

**Gap:** No mechanism to go from research finding → model update, or from simulation result → model adjustment.

---

#### Gap 6: Database / Persistence Layer

**Product Vision Outputs:**
- `DATABASE` (Research)
- `MODELING PM` (Model)
- `Design Parameters (JSON)` (Codegen)
- `Numerical Results Database` (Sim)

**Current State:** All outputs are files (SysML text, JSON, markdown). No unified database.

**Gap:** No query interface, no change tracking beyond git, no structured metadata.

---

### 3. Existing Abstractions to Build Upon

#### 3.1 ViewResult (Extraction Layer)

From `proof_of_concept/extraction/types.py`:

```python
class StructuralViewResult(TypedDict):
    nodes: list[StructuralNode]
    edges: list[ContainmentEdge]
    metadata: dict  # view type, root, total_nodes, etc.
```

This is the core "rendered view" abstraction. Can be extended for other view types.

#### 3.2 ComputationGraph (Codegen Layer)

From `sysml-codegen/resolution/models.py`:

```python
class ComputationGraph(BaseModel):
    modules: list[PipelineModule]
    entry_point_groups: list[ParameterGroup]
```

This is the "executable design" abstraction - the bridge between MODEL and SIM.

#### 3.3 Personas & User Stories

design-intent defines three clear personas with prioritized capabilities:

| Persona | Primary Stage Focus |
|---------|-------------------|
| Domain Engineer | MODEL, SIM |
| Model Developer | MODEL, CODEGEN |
| Stakeholder | SIM (results only) |

---

## Proposal: Closing the Gaps

### 4.1 Architectural Philosophy: Document-Centric, Not Application State

**Key Insight**: Claude Code manages context by reading documents. There is no need for explicit "Context" objects or session state. The architecture should be:

1. **Documents with rich YAML frontmatter** as the source of truth
2. **Skills per stage** that guide Claude's behavior
3. **Cross-references in documents** (depends_on, used_by) for navigation
4. **Visualization as a view INTO documents**, not separate application state

This aligns with the existing knowledge architecture research (see `fusion_modeling/project/research/input_data_control/`).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DOCUMENT-CENTRIC ARCHITECTURE                       │
│                                                                             │
│  Claude Code reads documents → builds context → takes action → updates docs │
└─────────────────────────────────────────────────────────────────────────────┘

  RESEARCH Documents          MODEL Documents           SIM Documents
  ┌─────────────────┐        ┌─────────────────┐       ┌─────────────────┐
  │ sources/*.md    │        │ models/**/*.sysml│      │ studies/*.yaml  │
  │ - YAML metadata │───────▶│ - doc comments   │─────▶│ - parameters    │
  │ - depends_on    │        │ - SOURCE_INDEX   │      │ - results refs  │
  │ - used_by       │        │ - work items     │      │ - comparisons   │
  └─────────────────┘        └─────────────────┘       └─────────────────┘
         │                          │                         │
         │    Skills guide Claude's behavior per stage        │
         ▼                          ▼                         ▼
  ┌─────────────────┐        ┌─────────────────┐       ┌─────────────────┐
  │ /research skill │        │ /design-model   │       │ /run-study skill│
  │ /manage-sources │        │ /implement-model│       │ /compare-results│
  └─────────────────┘        └─────────────────┘       └─────────────────┘
```

### 4.2 How Context Works (Without Explicit State Objects)

**Context IS:**
- The conversation history Claude maintains
- The documents Claude has read in this session
- The frontmatter metadata Claude extracts from those documents

**Cross-stage navigation:**
- Claude reads a document → sees `used_by: MODEL-TF-COIL` → can navigate there
- Claude reads simulation results → sees source design path → can inspect model
- No UI routing needed - just document references

**Stage awareness:**
- Skills tell Claude what to do in each context
- YAML frontmatter tells Claude what type of document it's looking at
- Claude infers the "stage" from document type, not from application state

### 4.3 Domain Data Types (As YAML Frontmatter)

These are not TypeScript interfaces for an application - they're **YAML frontmatter schemas** for markdown/YAML documents that Claude reads.

#### Research Source Document (`sources/papers/*.md`)

```yaml
---
doc_id: "SRC-2024-001"
title: "Techno-economic analysis of compact tokamak reactors"
type: "research_paper"
version: "1.0.0"

# Temporal metadata
published_at: 2024-03-01T00:00:00Z
ingested_at: 2025-01-10T14:22:00Z
valid_from: 2024-03-01

# Source provenance
source:
  category: "public"  # public | internal | user | generated
  origin: "MIT Plasma Science"
  url: "https://doi.org/10.1234/example"

# Authority/trust
authority:
  level: "high"  # high | moderate | low | none
  precedence: "high"  # How heavily to rely on this

# Forward references - what uses this document
used_by:
  - id: "WORK-2025-003"
    type: "work_item"
    relationship: "informed_by"
  - id: "models/library/physics/power_balance.sysml"
    type: "sysml_model"
    relationship: "modeled_from"

# Content markers for section-level tracking
content_markers:
  - marker_id: "sec-magnet-costs"
    line_range: [45, 120]
    modeled_in: "models/library/costs/magnet_costs.sysml"
    status: "complete"

tags: [magnets, LCOE, tokamak, CATF]
---

# Techno-economic analysis of compact tokamak reactors

[Document content...]
```

#### Work Item Document (`.project/backlog/*.md`)

```yaml
---
id: "WORK-2025-003"
title: "Model magnet cost scaling"
type: "feature"  # feature | bug | research
status: "design"  # backlog | spec | design | implement | review | done

# Decision binding
binding: "soft"  # hard | soft | direction | assumption
valid_until: 2026-06-22

# Traceability
informed_by:
  - id: "SRC-2024-001"
    section: "sec-magnet-costs"
impacts:
  - "models/library/costs/magnet_costs.sysml"
  - "models/designs/catf_mfe/cost_model.sysml"

ai_context: "When modeling magnet costs, reference this work item for approach"
---

## Description
Model the scaling of superconducting magnet costs based on field strength and mass...

## Acceptance Criteria
- [ ] Cost model captures B_max dependency
- [ ] Validated against PyFECONS algorithm
```

#### Study Definition (`studies/*.yaml`)

```yaml
# studies/lcoe_sensitivity_bmax.yaml
study_id: "STUDY-2025-001"
name: "LCOE Sensitivity to Magnetic Field"
type: "sweep"  # single | sweep | optimization
created_at: 2025-01-15T10:00:00Z

# Source design
design:
  path: "models/designs/catf_mfe"
  build_id: "BUILD-2025-042"  # Links to codegen artifact

# Parameter sweep definition
parameters:
  - name: "b_max"
    base_value: 12.0
    unit: "T"
    sweep:
      type: "range"
      min: 8.0
      max: 18.0
      steps: 11

# Results (populated after runs complete)
runs:
  - run_id: "RUN-001"
    parameters: {b_max: 8.0}
    status: "complete"
    results: {lcoe: 52.3, capital_cost: 4200}
  - run_id: "RUN-002"
    parameters: {b_max: 9.0}
    status: "complete"
    results: {lcoe: 45.1, capital_cost: 3900}
```

### 4.4 User Flow: Document-Based Stage Transitions

With a document-centric approach, "navigation" happens through Claude following references:

**Research → Model:**
```
User: "I found useful magnet cost data in SRC-2024-001, section 3.2"
Claude: Reads the source document
        Sees content_markers show sec-magnet-costs not yet modeled
        Creates work item document with informed_by reference
        Updates source document with used_by forward reference
User: "Now model the magnet costs"
Claude: Reads work item → sees informed_by → reads source section
        Creates/updates SysML model with doc comments citing source
```

**Model → Codegen:**
```
User: "Generate simulation code for CATF design"
Claude: Reads models/designs/catf_mfe/
        Runs sysml-codegen (via skill)
        Creates build artifact record in .project/builds/
        Links build to source design path
```

**Codegen → Sim:**
```
User: "Create a parameter sweep study for B_max"
Claude: Reads available builds → finds CATF build
        Creates study YAML with design reference
        Executes runs via TEAx
        Populates results in study document
```

**Sim → Model (feedback loop):**
```
User: "The results show magnets are 35% of cost. Let's optimize."
Claude: Reads study results → sees design path
        Reads model → traces cost to specific parts
        Can suggest or create new work item
        Work item references study results + model elements
```

**The key insight**: No UI routing or application state needed. Claude's context from the conversation + documents it reads IS the state.

### 4.5 Visualization Role: View INTO Documents

The visualization POC (Cytoscape structural view) is correct - it's a **view INTO the SysML model documents**. The same pattern applies to other stages:

| Stage | Document Types | Visualization Role |
|-------|---------------|-------------------|
| RESEARCH | `sources/*.md` | Source explorer with frontmatter filtering, content markers |
| MODEL | `models/**/*.sysml` | Structural/cost/dependency views (current POC) |
| CODEGEN | Build records, generated code | Pipeline DAG visualization, artifact browser |
| SIM | Study YAML, results JSON | Parameter sweep plots, LCOE breakdowns |

**Key principle**: Visualization renders document content. It doesn't maintain separate state. When the user interacts with visualization, they're selecting document elements that Claude can then reason about.

### 4.6 Skills for Each Stage

Rather than application-level routing, skills guide Claude's behavior:

```
RESEARCH Stage Skills:
  /manage-sources   - Add, tag, update source documents
  /research         - Search across sources, synthesize findings

MODEL Stage Skills:
  /spec-model       - Define requirements from sources
  /design-model     - Create SysML structure
  /implement-model  - Generate SysML code
  /audit-models     - Validate against sources

CODEGEN Stage Skills:
  /generate-sim     - Run sysml-codegen for a design (new)
  /validate-build   - Check generated code (new)

SIM Stage Skills:
  /define-study     - Create study YAML (new)
  /run-study        - Execute via TEAx (new)
  /analyze-results  - Interpret and compare runs (new)
```

MODEL skills already exist in agentic-mbse. The gaps are:
- RESEARCH skills need SOURCE_INDEX integration
- CODEGEN and SIM skills don't exist yet

### 4.7 Implementation Roadmap (Document-Centric)

**Phase 1: Document Infrastructure (Week 1-2)**
- Define YAML frontmatter schemas for all document types
- Create validation scripts (python-frontmatter based)
- Implement bidirectional link maintenance script
- Set up git pre-commit hooks for schema validation
- Enhance SOURCE_INDEX.md with machine-readable format

**Phase 2: Research Stage Foundation (Week 3-4)**
- Create `/manage-sources` skill
- Implement source document templates with full frontmatter
- Add content markers for section-level tracking
- Build document search skill (frontmatter-based filtering)
- Connect to existing `/research` skill

**Phase 3: Model-Research Integration (Week 5-6)**
- Update work item documents with `informed_by` references
- Add `used_by` forward references to source documents
- Enhance SysML doc comments to cite sources
- Create "what's modeled" status dashboard (skill-based)
- Integrate visualization to show source traceability

**Phase 4: Codegen Skills (Week 7-8)**
- Create `/generate-sim` skill wrapping sysml-codegen
- Define build artifact document schema
- Add build status tracking in `.project/builds/`
- Link builds to source designs in frontmatter
- Visualize pipeline DAG from generated YAML

**Phase 5: Sim Stage Skills (Week 9-10)**
- Create study YAML schema
- Build `/define-study` skill for study creation
- Integrate TEAx execution via `/run-study` skill
- Populate results back into study documents
- Add `/analyze-results` skill for interpretation

**Phase 6: Cross-Stage Visualization (Week 11-12)**
- Extend visualization POC to show source references
- Add results overlay on model cost views
- Create study comparison visualizations
- Export enhancements (full traceability reports)

---

## Code References

- Visualization POC: `proof_of_concept/extraction/visualization.py:1-601`
- Web server: `proof_of_concept/web/server.py:1-68`
- Frontend: `proof_of_concept/web/static/index.html:1-847`
- sysml-codegen CLI: `~/1cfe/sysml-codegen/src/sysml_codegen/cli/__init__.py:1-680`
- ComputationGraph: `~/1cfe/sysml-codegen/src/sysml_codegen/resolution/models.py`
- SysideAdapter: `~/1cfe/agentic-mbse/src/agentic_mbse/sysml/syside_adapter.py`

---

## Architecture Insights

1. **Document-Centric**: Claude manages context by reading documents - no explicit application state needed
2. **Skills as Stage Handlers**: Each stage has skills that guide Claude's behavior, not UI routes
3. **Cross-References as Navigation**: `depends_on` and `used_by` fields enable cross-stage tracing
4. **Visualization as Document View**: Renders document content, doesn't maintain separate state
5. **File-First Always**: Git-tracked YAML/markdown with SQLite index for queries (per knowledge architecture research)
6. **Traceability is Key**: Primary value is connecting research → model → results through document links

---

## Feasibility Assessment

**Can this be implemented?** Yes - it aligns well with existing infrastructure:

1. **Low Risk**: MODEL visualization POC is complete and follows the right pattern (view into documents)
2. **Low Risk**: Document schemas build on existing knowledge architecture research
3. **Low Risk**: Skills pattern is established in agentic-mbse
4. **Medium Risk**: CODEGEN skill requires wrapping CLI, but sysml-codegen exists
5. **Medium Risk**: SIM integration depends on TEAx stability

**Key Insight**: The document-centric approach is SIMPLER than the original proposal - no new state management, just document schemas and skills.

**Prerequisites:**
- Define YAML frontmatter schemas (building on input_data_control research)
- Implement skills for missing stages
- Extend visualization to show document cross-references

---

## Recommendations

1. **Update design-intent docs** to include all four stages as "views into documents" rather than separate application modes
2. **Define YAML frontmatter schemas** for sources, work items, builds, and studies (extending existing knowledge architecture research)
3. **Create skills for missing stages** (codegen, sim) following the existing agentic-mbse pattern
4. **Extend visualization** to show document cross-references (source traceability, build lineage)
5. **Leverage existing infrastructure** - python-frontmatter, SQLite index, dependency graph (all researched in input_data_control/)
6. **Implement SOURCE_INDEX integration** to connect research sources to modeling workflow

---

## Open Questions

1. **Frontmatter Schema Versioning**: How to evolve schemas without breaking existing documents? (Recommendation: `schema_version` field + adapters)
2. **Visualization Scope**: Should visualization be a standalone web app or Claude Code extension? (Recommendation: Start standalone, consider MCP integration)
3. **TEAx Integration**: How tightly coupled should sim skills be to TEAx? (Recommendation: Abstract behind skill, allow other backends)
4. **Study Persistence**: Where do results live - study YAML or separate files? (Recommendation: Summary in YAML, full results in JSON)
5. **Link Maintenance**: Manual vs. automated forward reference updates? (Recommendation: Git hook + on-demand script)
