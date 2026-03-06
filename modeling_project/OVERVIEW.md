# Fusion TEA — Investigation Scope

**Project**: Fusion TEA (Techno-Economic Analysis)
**Purpose**: Investigate the economics of nuclear fusion across fundamentally different approaches
**Start Date**: 2026-01-05
**Status**: Active — Investigation scoping (DEMO epic)

---

## What We're Doing

We are building a comparative techno-economic analysis of fusion power across the full landscape of approaches — magnetic confinement, inertial confinement, magnetized target, and exotic concepts. The goal is not to model one reactor design in detail, but to understand how fusion economics work across approaches that differ in confinement mechanism, fuel cycle, energy conversion, and engineering complexity.

The analysis is built in SysML v2 using the agentic-mbse toolchain. Models are validated against reference implementations (PyFECONS) where overlap exists, and all cost parameters trace to domain literature.

### Why This Matters

Fusion has dozens of competing approaches at various stages of maturity. Decision-makers — investors, policymakers, researchers — need structured comparisons, not just headline LCOE numbers. This project builds the analytical infrastructure to produce those comparisons: a taxonomy of the concept space, reusable cost modeling patterns, and traceable parameter chains from source literature to model outputs.

---

## Research Questions

These questions drive all downstream work — taxonomy, source selection, modeling targets, and comparison methodology.

### RQ-1: What are the dominant cost drivers for fusion power, and how do they differ across confinement approaches?

CAS22 (reactor plant equipment) is ~60% of cost for magnetic confinement tokamaks, but inertial, magnetized target, and exotic approaches have fundamentally different power core structures, drivers, and balance-of-plant requirements. Understanding where the money goes for each approach is the foundation of any meaningful comparison.

### RQ-2: What LCOE range is credible for each major fusion approach, and what assumptions drive those estimates?

Published LCOE figures vary enormously (30–200+ $/MWh) and depend critically on assumptions about plant availability, magnet or driver cost, neutron economy, rep rate, and thermal conversion efficiency. We need to decompose LCOE into its constituent assumptions — not cite headline numbers.

### RQ-3: Which cost structures are shared across fusion concepts, and where do they fundamentally diverge?

This directly informs modeling architecture. Shared structures (e.g., thermal power conversion, buildings, site work) become reusable library components. Divergent structures (e.g., magnet systems vs. laser drivers vs. pulsed power) become concept-specific designs. The answer determines how much modeling reuse is achievable.

### RQ-4: What is the state of cost estimation maturity across fusion approaches?

An ARIES tokamak study with AACE Class 3-4 estimates is fundamentally different from a startup whitepaper with Class 5 estimates. Understanding estimation maturity for each concept frames how much confidence to place in any comparison and where the biggest knowledge gaps lie.

### RQ-5: Which cost and performance parameters exhibit both high sensitivity and high uncertainty?

A parameter that moves LCOE by 2x if wrong AND is poorly constrained by available data is more important than one that's well-known or low-impact. This is the "where should attention focus" question — identifying the highest-leverage unknowns across the fusion landscape.

---

## Comparison Axes

These are the dimensions along which fusion concepts will be compared. Every concept model must produce outputs along these axes to enable apples-to-apples comparison.

| Axis | What It Measures | Why It Matters |
|------|-----------------|----------------|
| **LCOE ($/MWh)** | Total lifecycle cost per unit energy produced | The bottom line — enables comparison with other energy sources |
| **Capital cost by CAS category** | Where the money goes (CAS20 breakdown) | Identifies dominant cost drivers per concept |
| **Capacity factor** | Plant availability × thermal efficiency | Huge LCOE sensitivity; varies significantly between pulsed and steady-state concepts |
| **Fuel cycle economics** | Tritium breeding requirements, fuel cost, fuel availability | D-T concepts need breeding blankets; aneutronic concepts avoid them but face other challenges |
| **Technology readiness** | Maturity of key subsystems | Distinguishes "ready to build" from "needs breakthroughs" |
| **Estimation confidence** | AACE class of the cost estimate | Frames how seriously to take the numbers |
| **Sensitivity-risk profile** | Parameters that are high-sensitivity AND high-uncertainty | Identifies where better data or engineering would most change the economic picture |

---

## Scope

### What's In

The investigation covers fusion power approaches across all major confinement categories: magnetic confinement (tokamaks, stellarators, mirrors), inertial confinement (laser, heavy-ion), magnetized target fusion, and exotic concepts. The initial candidate set includes ~36 concepts (see `modeling_project/intent/Initial Fusion Concept Candidates.csv`). Literature review may surface additional approaches.

All concepts are captured in the taxonomy (Stage 1). A subset of ~13 concepts with assigned investigators are selected for deeper cost modeling (Stage 2) — see the Investigation Process section for details.

### What's Out

- Detailed engineering design of any single concept (we model economics, not physics)
- Non-electric applications of fusion (neutron sources, space propulsion, industrial heat)
- Fission-fusion hybrids (different economic structure entirely)
- Concepts with zero public technical data (noted in taxonomy, cannot model)

---

## "Done" Criteria

### V1 — This Epic (DEMO)

The epic is complete when:

1. **Taxonomy** exists as a committed artifact, covering MFE, IFE, MIF, and other categories with subcategories mapping the full ~36+ concept landscape
2. **At least two concepts** from different top-level categories have been modeled to CAS level 2 cost breakdown
3. **Cross-concept comparison** exists along at least 3 of the 7 comparison axes
4. **Full traceability**: every quantitative value in the models cites its source
5. **Interactive workflow explainer** shows the full arc from investigation scope through results, with real artifacts embedded at each stage

This is bounded: two concepts from different families, compared on 3+ axes. Not the full landscape — enough to prove the methodology works end-to-end.

### Beyond V1 — Project Goals

- All ~13 selected concepts modeled to the depth their available data supports
- Sensitivity-risk analysis identifies the highest-leverage parameters across the landscape
- Cross-concept comparison on all 7 axes with normalized presentation
- Coverage sufficient to inform: "Given limited R&D resources, where do the economics point?"
- Taxonomy maintained as a living artifact, updated as new concepts emerge

---

## Source Strategy

### Data Needs by Modeling Depth

Rather than prescribing specific sources upfront, we define the data layers needed at each depth level. Sources are selected to fill these layers as the investigation progresses.

| Layer | Data Need | Supports |
|-------|-----------|----------|
| **L1: Conceptual Model** | How does this approach work? Confinement mechanism, fuel cycle, energy conversion pathway, key engineering subsystems | Stage 1 taxonomy |
| **L2: Physics & Requirements** | Plasma parameters, confinement performance, burn conditions, power requirements | Stage 1 enrichment |
| **L3: Structural Composition** | What physical systems are needed? Magnets/lasers/drivers, blanket/shield, power conversion, BOP — bill of materials at subsystem level | Stage 2 CAS structure |
| **L4: Energy Balance** | Power flows, thermal conversion efficiency, recirculating power, availability, duty cycle | Stage 2 performance model |
| **L5: Costing** | Capital costs by subsystem, O&M estimates, fuel costs, scaling relationships, basis of estimate | Stage 2 cost model |

### Reuse Principle

Where concepts share structural or physical characteristics, data and model elements can be shared under documented assumptions. For example:
- All D-T concepts need tritium breeding blankets (shared L3/L4 structure)
- All thermal conversion plants share balance-of-plant elements (turbine, cooling, electrical)
- CAS30-60 (indirect costs, buildings, financial) are largely concept-agnostic

Identifying these shared elements is a key output of the concept analysis phase (Phase PR-2).

### Iterative Selection

Source selection is iterative. Start with the existing corpus, begin research, and let gaps surface organically. When a specific concept needs L3-L5 data that doesn't exist in the corpus, that's when we seek new sources. The existing 7 sources (see `knowledge/SOURCE_INDEX.md`) provide initial coverage across MFE, IFE, and the CAS framework.

---

## Traceability Requirements

The value of this analysis depends entirely on whether a reader can verify any number they see. This is critical because:
- Early-stage fusion concepts have sparse data — filling gaps requires assumptions and judgment
- LLM agents perform significant portions of the research and modeling, and are susceptible to hallucination
- A comparison is only as credible as its weakest-sourced parameter

### What Traceability Means

1. Every quantitative value MUST cite its source: document, location (page/section/table), and how the value was derived
2. Every assumption MUST be explicitly labeled, with rationale for the assumed value
3. Judgment calls MUST be flagged with reasoning — not buried as implicit choices
4. Parameters without source data MUST NOT be silently invented — they must be marked as assumed or estimated, with basis

The enforcement mechanism is defined in MR-4 (`modeling_project/REQUIREMENTS.md`) and the traceability system spec (`.project/active/traceability-system/spec.md`). The requirement here is on the outcome: **a reader can trace any number in the analysis back to its origin, and can distinguish sourced data from assumptions from judgments.**

---

## Investigation Process

The investigation has two stages that are generally sequential but largely orthogonal. Stage 1 (Taxonomy) must come first because having an overall framework for comparing approaches is a prerequisite to modeling any individual one. Stage 2 (Concept Modeling) then proceeds concept-by-concept.

Both stages share the same internal cycle structure, but apply it to different questions and produce different artifacts.

### Stage 1: Taxonomy (Breadth)

Build the framework for organizing and comparing the full fusion concept landscape — all ~36+ concepts captured at classification depth.

**The question:** How do we classify and compare fusion approaches? What are the distinguishing dimensions? Where do concepts share structure and where do they diverge?

**Depth:** Conceptual model per concept — confinement mechanism, fuel type, operation mode, energy conversion pathway, key engineering subsystems, and companies/programs pursuing each approach. Data layers L1-L2.

**Exit criteria:** A formalized framework for presenting and comparing design concepts — the specific artifact format is TBD, but it must organize the concept space along meaningful dimensions and support concept selection for Stage 2.

### Stage 2: Concept Modeling (Depth)

Model individual concepts in SysML v2, one at a time, using the taxonomy framework to guide what's shared vs. concept-specific. The initial set includes ~13 concepts with assigned investigators, spanning the major approach categories:

- **Magnetic confinement:** HTS Compact Tokamak (CFS), Spherical Tokamak (TE), Modular HTS Stellarator (Type One/Renaissance), Magnetic Mirror D-T (Realta), Magnetic Mirror p-B11 (Pale Blue), Levitated Dipole (OpenStar), p-B11 FRC (TAE)
- **Inertial confinement:** Laser ICF Indirect Drive (Inertia/Xcimer), Heavy Ion Beam ICF (Intensity)
- **Magnetized target:** MagLIF (Pacific/Europa), FRC with Direct Conversion (Helion)
- **Other:** Electrostatic Hybrid (Avalanche), Muon-Catalyzed Fusion (Acceleron)

**The question:** For a given fusion concept, what does the cost structure look like? What are the dominant cost drivers, sensitivities, and uncertainties?

**Depth:** CAS level 2-3 cost models with traceable parameters. Data layers L3-L5. Depth depends on available data — some concepts will support full CAS-level modeling, others only parametric estimates. The estimation confidence axis captures this difference.

**Exit criteria:** Per-concept — a validated SysML v2 model passing all validation levels. Cross-concept — comparison along the defined axes.

### The Internal Cycle

Each stage (and each concept within Stage 2) follows the same cycle with three phases and two feedback loops:

```
                    ┌─────────────────────────────────┐
                    │                                 │
                    ▼                                 │
        ┌───────────────────┐                         │
        │  1. INFORMATION   │                         │
        │     GATHERING &   │◄──────────┐             │
        │     SYNTHESIS     │           │             │
        └────────┬──────────┘           │             │
                 │                      │             │
            exit criteria met      data gaps      data gaps or
                 │                 identified      issues found
                 ▼                      │             │
        ┌───────────────────┐           │             │
        │  2. WORK          ├───────────┘             │
        │                   │                         │
        └────────┬──────────┘                         │
                 │                                    │
            work complete                             │
                 │                                    │
                 ▼                                    │
        ┌───────────────────┐                         │
        │  3. ANALYSIS &    ├─────────────────────────┘
        │     VISUALIZATION │
        └───────────────────┘
```

#### Phase 1: Information Gathering & Synthesis

A cycle of source ingestion and domain research, driven by questions.

```
Question → Source Ingestion → Domain Research → Gaps identified?
                ▲                                    │
                └──── yes: find & ingest sources ────┘
                      no: exit criteria met → proceed to Work
```

- **Source ingestion**: PDFs and technical documents are ingested through the Zotero → extract → register pipeline, producing structured extractions
- **Domain research**: Research is conducted against ingested documents, producing domain insights (DI-XXX entries in KNOWLEDGE.md)
- **Gap identification**: An initial research pass will identify knowledge gaps — topics where the existing corpus is insufficient. This triggers literature searches, ingestion of new sources, and further research
- **Exit criteria** are tied to the questions that initiated the cycle:
  - For taxonomy: sufficient understanding to produce a concept analysis across the target landscape
  - For a specific concept model: data layers L1-L5 populated to the depth available data supports

#### Phase 2: Work

The "building" phase — producing the durable artifacts that encode what was learned.

- **For taxonomy**: The artifact format is TBD, but we expect a formalized framework for presenting and comparing fusion design concepts — a decision tree, classification scheme, or structured comparison matrix. This emerges from concept analysis during the taxonomy stage.
- **For concept modeling**: The established agentic-mbse work loop — epic → work items → spec → design → plan → implement. The Dashboard tracks progress through this loop, showing validation status and traceability coverage.

If data gaps are discovered during work (e.g., a parameter is needed but wasn't captured during research), the cycle returns to Information Gathering.

#### Phase 3: Analysis & Visualization

Interpreting and presenting what the work produced.

- **For taxonomy**: Visualizations of the concept space, comparison matrices, gap maps
- **For concept modeling**: Cost breakdowns, LCOE decompositions, cross-concept comparison charts along the defined axes, sensitivity-risk profiles

If analysis reveals issues (e.g., a cost driver that doesn't make sense, a comparison that's skewed by inconsistent assumptions), the cycle feeds back:
- To **Information Gathering** if the issue is missing or incorrect data
- To **Work** if the issue is in the model or framework itself

### Sequencing and Overlap

```
Investigation Scope (this document)
        │
        ▼
Stage 1: Taxonomy ─── Info Gathering ──► Work ──► Analysis
        │                                            │
        │  (taxonomy framework provides structure)   │
        ▼                                            │
Stage 2: Concept Modeling (repeated per concept)     │
        │                                            │
        ├── Concept A ── Info ──► Work ──► Analysis  │
        ├── Concept B ── Info ──► Work ──► Analysis  │
        └── ...                                      │
                                                     │
Cross-Concept Comparison ◄───────────────────────────┘
```

Stage 2 concepts can proceed in parallel if resources allow, but each follows its own cycle. The taxonomy framework from Stage 1 provides the shared structure that makes cross-concept comparison possible at the end.

---

## Technology Stack

**Core Tools:**
- **SysML v2** (via SysIDE / `syside` CLI) — Formal modeling language for structure, behavior, and analysis
- **Python 3.11+** (via `uv`) — Scripting, analysis, and automation
- **agentic-mbse** — MBSE workflow commands, 6-level validation, PDF extraction (v4 pipeline)
- **sysml-codegen** — Code generation from SysML models
- **Git** — Version control; all artifacts committed

**Data Pipeline:**
- **Zotero** → PDF ingestion and metadata management
- **agentic-mbse extract** → Structured document extraction with quality metrics
- **Domain research workflow** → DI-XXX entries in KNOWLEDGE.md

---

## Project Structure

```
fusion-tea/
├── CLAUDE.md                    # Project context for agent sessions
├── models/
│   ├── library/                 # Reusable definitions (concept-agnostic)
│   └── designs/                 # Concept-specific model instances
├── knowledge/
│   ├── SOURCE_INDEX.md          # Registered domain sources
│   ├── KNOWLEDGE.md             # Domain insight registry (DI-XXX)
│   ├── sources/                 # Extracted source documents
│   └── research/                # Research pipeline (pending → approved → impacts)
├── modeling_project/
│   ├── OVERVIEW.md              # This file — investigation scope
│   ├── ARCHITECTURE.md          # Architectural decisions (AD-XXX)
│   ├── REQUIREMENTS.md          # Modeling requirements (MR-XXX)
│   ├── MODELING_GUIDE.md        # SysML v2 reference
│   ├── MODELING_PROCESS.md      # MBSE workflow process
│   └── intent/                  # Internal team artifacts — meeting notes, concept
│                                #   candidates, qualitative inputs that refine goals
├── work/
│   ├── BACKLOG.md               # Work item registry
│   └── backlog/                 # Epic decomposition files
├── demo/
│   └── index.html               # Interactive workflow explainer
├── data/                        # Structured data and outputs
├── scripts/                     # Automation (Zotero ingestion, etc.)
└── archive/                     # Archived CATF-era artifacts
```

---

**Last Updated**: 2026-03-02
**Next**: Phase 5 — Interactive workflow explainer (demo/index.html)
